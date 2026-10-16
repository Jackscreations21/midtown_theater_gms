#!/usr/bin/env python3
"""Send ArtDmx to the relay (tools/artnet-relay.py) as a desk would — the test half of the Theatre 2 desk path.

    python tools/artnet-test.py full                 # every unit at full, open white, movers at their home
    python tools/artnet-test.py blackout             # every channel 0
    python tools/artnet-test.py chase [--seconds 20] # one unit at a time around the rig, the movers sweeping, haze up
    python tools/artnet-test.py look <tag>           # a look from rig.json, encoded as tools/jt-qlc.py encodes it
    options: --host 127.0.0.1 --port 6454 --universes 0,1 --rate 44 --seconds N (how long to keep sending; default 3)

Standard library only. Reads assets/johnny-tremain/rig.json for the patch (each unit's universe, address, type) and sends
both universes at --rate packets a second with the Sequence field counting, as QLC+ does.
"""
import argparse, json, math, os, socket, struct, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rig = json.load(open(os.path.join(ROOT, 'assets', 'johnny-tremain', 'rig.json'), encoding='utf-8'))

ap = argparse.ArgumentParser()
ap.add_argument('what', choices=['full', 'blackout', 'chase', 'look'])
ap.add_argument('tag', nargs='?')
ap.add_argument('--host', default='127.0.0.1')
ap.add_argument('--port', type=int, default=6454)
ap.add_argument('--universes', default='0,1')
ap.add_argument('--rate', type=float, default=44.0)
ap.add_argument('--seconds', type=float, default=None)
a = ap.parse_args()
ART = [int(x) for x in a.universes.split(',')]
secs = a.seconds if a.seconds is not None else (20.0 if a.what == 'chase' else 3.0)


def ch(u, frames, i, v):
    frames[u['universe']][u['address'] - 1 + i] = max(0, min(255, int(round(v))))


def full_unit(u, frames, lv=1.0, pan=0.5, tilt=0.5):
    t = u['type']
    if t == 'lustr':
        for i in range(7): ch(u, frames, i, 255)
        ch(u, frames, 7, 255 * lv)
    elif t in ('cs-spot', 'cs-par'):
        ch(u, frames, 0, 255 * lv)
        for i in (1, 2, 3): ch(u, frames, i, 255)
    elif t in ('cyc', 'cyc-floor'):
        ch(u, frames, 0, 255 * lv)
        for i in (1, 2, 3): ch(u, frames, i, 255)
    elif t in ('s4', 'practical', 'follow'):
        ch(u, frames, 0, 255 * lv)
    elif t == 'hazer':
        ch(u, frames, 0, 255); ch(u, frames, 1, 255 * lv); ch(u, frames, 2, 255)
    elif t == 'encore':
        d = int(lv * 65535)
        ch(u, frames, 0, 30); ch(u, frames, 1, d >> 8); ch(u, frames, 2, d & 255)
        p, q = int(pan * 65535), int(tilt * 65535)
        ch(u, frames, 28, p >> 8); ch(u, frames, 29, p & 255); ch(u, frames, 30, q >> 8); ch(u, frames, 31, q & 255)
    elif t == 'aura':
        ch(u, frames, 0, 22); ch(u, frames, 1, 255 * lv)
        p, q = int(pan * 65535), int(tilt * 65535)
        ch(u, frames, 3, p >> 8); ch(u, frames, 4, p & 255); ch(u, frames, 5, q >> 8); ch(u, frames, 6, q & 255)
        for i in (9, 10, 11, 12): ch(u, frames, i, 255)


def look_frames(tag):
    """the look as QLC+ would send it: tools/jt-qlc.py's own encoder (imported without running its writer)"""
    src = open(os.path.join(ROOT, 'tools', 'jt-qlc.py'), encoding='utf-8').read()
    cut = src.index('# ---------------------------------------------------------------- the state of every unit')
    ns = {'__name__': 'jtqlc', '__file__': os.path.join(ROOT, 'tools', 'jt-qlc.py')}
    exec(compile(src[:cut], 'jt-qlc.py', 'exec'), ns)        # the imports, rig.json, rgb, pan_tilt, dmx — nothing written
    look = rig['looks'].get(tag)
    if not look:
        sys.exit(f'no look "{tag}" — one of: {", ".join(sorted(rig["looks"]))}')
    frames = {1: bytearray(512), 2: bytearray(512)}
    for u in rig['units']:
        for c, v in ns['dmx'](u, look['units'].get(u['id'])):
            frames[u['universe']][u['address'] - 1 + c] = v
    return frames


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
seq = 0


def send(frames):
    global seq
    # the Sequence counts 1..255 off the clock, so a second run straight after the first carries on from it (the relay
    # refuses an older Sequence than the last for 1 s — a restarted counter would lose its first packets)
    seq = int(time.time() * a.rate) % 255 + 1
    for i, pa in enumerate(ART):
        data = bytes(frames[i + 1])
        pkt = b'Art-Net\0' + struct.pack('<H', 0x5000) + struct.pack('>H', 14) + bytes([seq, 0, pa & 0xff, (pa >> 8) & 0x7f]) + struct.pack('>H', 512) + data
        sock.sendto(pkt, (a.host, a.port))


units = rig['units']
t0 = time.monotonic()
n = 0
fixed = None
if a.what == 'look':
    fixed = look_frames(a.tag)
elif a.what in ('full', 'blackout'):
    fixed = {1: bytearray(512), 2: bytearray(512)}
    if a.what == 'full':
        for u in units: full_unit(u, fixed)
print(f'artnet-test: {a.what}{" " + a.tag if a.tag else ""} -> {a.host}:{a.port}, Art-Net universes {ART}, {a.rate:.0f} packets/s for {secs:.0f} s', flush=True)
while True:
    t = time.monotonic() - t0
    if t > secs:
        break
    if fixed is not None:
        frames = fixed
    else:                                    # the chase: one unit at a time, 4 a second; the movers sweep; haze at half
        frames = {1: bytearray(512), 2: bytearray(512)}
        k = int(t * 4) % len(units)
        for i, u in enumerate(units):
            if u['type'] in ('encore', 'aura'):
                full_unit(u, frames, 1.0, 0.5 + 0.08 * math.sin(t * 1.3 + i), 0.5 + 0.06 + 0.04 * math.sin(t * 0.9 + i))
            elif u['type'] == 'hazer':
                full_unit(u, frames, 0.5)
            elif i == k:
                full_unit(u, frames)
    send(frames)
    n += 1
    time.sleep(max(0.0, t0 + n / a.rate - time.monotonic()))
print(f'artnet-test: sent {n} packets per universe', flush=True)
