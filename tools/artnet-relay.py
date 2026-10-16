#!/usr/bin/env python3
"""Art-Net relay for Theatre 2's Johnny Tremain rig: QLC+ -> UDP 6454 -> this -> WebSocket -> midtown.html.

    python tools/artnet-relay.py                    # Art-Net universes 0 and 1 -> the rig's U1 and U2, ws://127.0.0.1:9454
    python tools/artnet-relay.py --universes 0,1 --ws-port 9454 --art-port 6454

A page cannot receive UDP, and Art-Net is UDP, so the desk talks to this and this talks to the page. Standard library only
(Node is not installed on Jack's machine). The design is the Palace's tools/artnet-relay.js (gms-theater), cut down:

  - ArtDmx (OpOutput 0x5000) on UDP 6454, bound to 127.0.0.1 only. A packet's 15-bit Port-Address is SubUni (byte 14)
    + Net (byte 15, low 7 bits) << 8. QLC+ numbers its universes from 1 in the window and its Art-Net plugin sends
    QLC+ Universe 1 as Art-Net universe 0 and Universe 2 as 1 by default; --universes lists the Port-Addresses that
    are the rig's U1 and U2, in that order (rig.json's universes are 1-based, as QLC+ shows them).
  - The Palace's guards: a packet must carry the length it declares (2..512 — a header-only packet is not a
    blackout); an older Sequence than the last one is refused (0 = the desk has sequencing off; a duplicate is
    accepted); a gap of more than 1 s forgets the baseline so a restarted desk is not refused for seconds.
  - The latest 512-byte frame per universe is kept and sent to every WebSocket client as a BINARY message:
    one byte (the rig universe, 1 or 2) + 512 channel bytes. Only on change, at most ~44 a second per universe.
  - A TEXT status message every 0.5 s: {"t": "status", "u": {"1": {"art": 0, "pps": 44, "alive": true}, ...}}.
    "alive" is a packet within the last --stale s (default 5: QLC+ idles at ~0.5 packets a second when nothing
    changes — the Palace's measured trap, TRAPS "a protocol's nominal rate is not a device's actual rate"), so a
    held look is still "the desk is live" although no frame changes.
  - The WebSocket half is RFC 6455 by hand: the accept-key handshake, unmasked server frames, ping -> pong, close
    honoured. Clients send nothing else. Listens on 127.0.0.1 only. GET /probe answers a tiny page that postMessages
    its parent: the page knocks with it in a hidden iframe (a refused iframe logs nothing; a refused WebSocket is an
    error line in Chrome's console every try). Any other HTTP request gets a one-line answer.
  - One status line every 3 s.

No SO_REUSEADDR on the UDP socket: on Windows a second bind to a port another program holds can succeed and receive
nothing; without it a collision is a loud "port in use" (the Palace's trap).
"""
import argparse, base64, hashlib, json, select, socket, struct, sys, time

ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
ap.add_argument('--universes', default='0,1', help='Art-Net Port-Addresses that are the rig\'s U1,U2 (default 0,1 = QLC+ Universe 1,2)')
ap.add_argument('--ws-port', type=int, default=9454, help='WebSocket port on 127.0.0.1 (the page connects to ws://127.0.0.1:9454)')
ap.add_argument('--art-port', type=int, default=6454, help='Art-Net UDP port (Art-Net is always 6454; this is for tests)')
ap.add_argument('--stale', type=float, default=5.0, help='seconds without a packet before a universe is "not alive"')
ap.add_argument('--rate', type=float, default=44.0, help='most frames a second sent per universe')
args = ap.parse_args()

HOST = '127.0.0.1'
ART_UNIS = [int(x) for x in args.universes.split(',') if x.strip() != '']
RIG_OF = {pa: i + 1 for i, pa in enumerate(ART_UNIS)}          # Art-Net Port-Address -> the rig's universe (1-based)
WS_GUID = b'258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
MIN_GAP = 1.0 / args.rate


def say(s):
    print(time.strftime('%H:%M:%S ') + '[artnet] ' + s, flush=True)


# ---------------------------------------------------------------- the Art-Net half
class Uni:
    def __init__(self, pa, rig):
        self.pa, self.rig = pa, rig
        self.data = bytearray(512)
        self.sent = None             # the bytes last sent to clients
        self.sent_at = 0.0
        self.last_at = 0.0           # the last packet accepted
        self.last_seq = 0
        self.stamps = []             # accepted packet times within the last second
        self.total = 0
        self.refused = 0

    def pps(self, now):
        self.stamps = [t for t in self.stamps if now - t < 1.0]
        return len(self.stamps)


unis = {pa: Uni(pa, RIG_OF[pa]) for pa in ART_UNIS}
other_unis = {}                      # Port-Addresses seen that are not ours: counted, so the status line can say so


def art_dmx(msg, now):
    """an accepted ArtDmx packet -> its Uni (data updated), else None; every refusal is silent"""
    if len(msg) < 18 or msg[:8] != b'Art-Net\0':
        return None
    if struct.unpack_from('<H', msg, 8)[0] != 0x5000:
        return None
    pa = msg[14] | ((msg[15] & 0x7f) << 8)
    n = struct.unpack_from('>H', msg, 16)[0]
    if pa not in unis:
        other_unis[pa] = other_unis.get(pa, 0) + 1
        return None
    u = unis[pa]
    if n < 2 or n > 512 or len(msg) - 18 < n:
        u.refused += 1
        return None
    if now - u.last_at > 1.0:
        u.last_seq = 0
    seq = msg[12]
    if seq != 0 and u.last_seq != 0 and ((seq - u.last_seq) & 0xff) > 128:
        u.refused += 1
        return None
    u.last_seq = seq
    u.last_at = now
    u.stamps.append(now)
    u.total += 1
    u.data[:n] = msg[18:18 + n]
    if n < 512:
        u.data[n:] = bytes(512 - n)
    return u


udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    udp.bind((HOST, args.art_port))
except OSError as e:
    say(f'cannot listen for Art-Net on {HOST}:{args.art_port} — {e}.')
    say('      Another program has the port (QLC+ itself, or a second relay). Close QLC+, start this relay, then open QLC+.')
    sys.exit(1)
udp.setblocking(False)


# ---------------------------------------------------------------- the WebSocket half
def ws_frame(opcode, payload):
    n = len(payload)
    if n < 126:
        head = struct.pack('>BB', 0x80 | opcode, n)
    elif n < 65536:
        head = struct.pack('>BBH', 0x80 | opcode, 126, n)
    else:
        head = struct.pack('>BBQ', 0x80 | opcode, 127, n)
    return head + payload


class Client:
    def __init__(self, sock, addr):
        self.sock, self.addr = sock, addr
        self.inbuf = b''
        self.out = bytearray()
        self.open = False            # past the handshake
        self.closing = False

    def send(self, data):
        if len(self.out) > 1 << 20:  # a client that stopped reading: drop it rather than grow without end
            self.closing = True
            return
        self.out += data


clients = []
lsn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    lsn.bind((HOST, args.ws_port))
except OSError as e:
    say(f'cannot serve the page on {HOST}:{args.ws_port} — {e}. Try --ws-port <other> (and the page\'s JTL desk port).')
    sys.exit(1)
lsn.listen(8)
lsn.setblocking(False)


def handshake(c):
    end = c.inbuf.find(b'\r\n\r\n')
    if end < 0:
        if len(c.inbuf) > 16384:
            c.closing = True
        return
    head, c.inbuf = c.inbuf[:end].decode('latin1'), c.inbuf[end + 4:]
    lines = head.split('\r\n')
    hdr = {}
    for ln in lines[1:]:
        if ':' in ln:
            k, v = ln.split(':', 1)
            hdr[k.strip().lower()] = v.strip()
    key = hdr.get('sec-websocket-key')
    if not lines[0].startswith('GET ') or 'websocket' not in hdr.get('upgrade', '').lower() or not key:
        if lines[0].startswith('GET /probe'):
            # THE PAGE'S QUIET KNOCK. A refused WebSocket is logged by Chrome itself (an error line per attempt, nothing the
            # page can catch), and so is a refused fetch; a hidden iframe whose load is refused logs nothing. So the page
            # loads this in a hidden iframe every few seconds, and only when this answers (postMessage) opens the socket.
            body = b'<!doctype html><title>relay</title><script>parent.postMessage({artnetRelay: 1}, "*")</script>\n'
            c.send(b'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\nCache-Control: no-store\r\nContent-Length: %d\r\nConnection: close\r\n\r\n' % len(body) + body)
        else:
            body = b'Theatre 2 Art-Net relay: connect with ws://127.0.0.1:%d\n' % args.ws_port
            c.send(b'HTTP/1.1 426 Upgrade Required\r\nContent-Type: text/plain\r\nContent-Length: %d\r\nConnection: close\r\n\r\n' % len(body) + body)
        c.closing = True
        return
    acc = base64.b64encode(hashlib.sha1(key.encode('latin1') + WS_GUID).digest())
    c.send(b'HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Accept: ' + acc + b'\r\n\r\n')
    c.open = True
    say(f'the page connected ({sum(1 for k in clients if k.open)} connected)')
    # a new page gets every universe's current frame and the status at once
    now = time.monotonic()
    for u in unis.values():
        if u.total and now - u.last_at < args.stale:      # a desk that went quiet long ago is not handed over
            c.send(ws_frame(0x2, bytes([u.rig]) + bytes(u.data)))
    c.send(ws_frame(0x1, status_json(now)))


def read_frames(c):
    buf = c.inbuf
    off = 0
    while len(buf) - off >= 2:
        b0, b1 = buf[off], buf[off + 1]
        op, masked, n, h = b0 & 0x0f, b1 & 0x80, b1 & 0x7f, 2
        if n == 126:
            if len(buf) - off < 4:
                break
            n = struct.unpack_from('>H', buf, off + 2)[0]
            h = 4
        elif n == 127:                                   # the page never sends anything that long
            c.closing = True
            return
        ml = 4 if masked else 0
        if len(buf) - off < h + ml + n:
            break
        mask = buf[off + h:off + h + 4] if masked else None
        body = bytearray(buf[off + h + ml:off + h + ml + n])
        if mask:
            for i in range(len(body)):
                body[i] ^= mask[i & 3]
        off += h + ml + n
        if op == 0x8:                                    # close: answer and go
            c.send(ws_frame(0x8, b''))
            c.closing = True
            break
        if op == 0x9:                                    # ping -> pong
            c.send(ws_frame(0xA, bytes(body)))
    c.inbuf = buf[off:]


def status_json(now):
    return json.dumps({'t': 'status', 'u': {str(u.rig): {'art': u.pa, 'pps': u.pps(now), 'alive': u.total > 0 and now - u.last_at < args.stale}
                                             for u in unis.values()}}).encode()


def drop(c, why=''):
    try:
        c.sock.close()
    except OSError:
        pass
    if c in clients:
        clients.remove(c)
        if c.open:
            say(f'the page left{why} ({sum(1 for k in clients if k.open)} connected)')


# ---------------------------------------------------------------- go
say(f'Art-Net in on udp {HOST}:{args.art_port}: ' + ', '.join(f'Art-Net universe {pa} -> the rig\'s U{RIG_OF[pa]} (QLC+ Universe {RIG_OF[pa]})' for pa in ART_UNIS))
say(f'the page connects to ws://{HOST}:{args.ws_port} — open midtown.html, press "T2 rig". Ctrl+C stops.')
last_status = last_line = 0.0
sent_count = 0
try:
    while True:
        now = time.monotonic()
        # when is the next thing due: a held-back frame, the status message
        due = [last_status + 0.5]
        for u in unis.values():
            if u.total and u.sent != u.data:
                due.append(u.sent_at + MIN_GAP)
        timeout = max(0.0, min(due) - now)
        rl = [udp, lsn] + [c.sock for c in clients]
        wl = [c.sock for c in clients if c.out]
        try:
            r, w, _ = select.select(rl, wl, [], min(timeout, 0.25))
        except (OSError, ValueError):
            for c in list(clients):
                if c.sock.fileno() < 0:
                    drop(c)
            continue
        now = time.monotonic()
        if udp in r:
            for _ in range(256):                         # drain what is queued
                try:
                    msg, _a = udp.recvfrom(2048)
                except (BlockingIOError, InterruptedError):
                    break
                except ConnectionResetError:             # Windows reports an ICMP "port unreachable" on a UDP socket
                    continue
                art_dmx(msg, now)
        if lsn in r:
            try:
                s, a = lsn.accept()
                s.setblocking(False)
                s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                clients.append(Client(s, a))
            except OSError:
                pass
        for c in list(clients):
            if c.sock in r:
                try:
                    d = c.sock.recv(65536)
                except (BlockingIOError, InterruptedError):
                    d = None
                except OSError:
                    drop(c); continue
                if d == b'':
                    drop(c); continue
                if d:
                    c.inbuf += d
                    if not c.open:
                        handshake(c)
                    if c.open:
                        read_frames(c)
        # the frames: each universe that changed, no faster than --rate
        for u in unis.values():
            if u.total and u.sent != u.data and now - u.sent_at >= MIN_GAP:
                u.sent = bytearray(u.data)
                u.sent_at = now
                f = ws_frame(0x2, bytes([u.rig]) + bytes(u.data))
                for c in clients:
                    if c.open:
                        c.send(f)
                sent_count += 1
        if now - last_status >= 0.5:
            last_status = now
            f = ws_frame(0x1, status_json(now))
            for c in clients:
                if c.open:
                    c.send(f)
        for c in list(clients):
            if c.out:                                    # non-blocking: what the socket takes now, the rest next time
                try:
                    k = c.sock.send(c.out)
                    del c.out[:k]
                except (BlockingIOError, InterruptedError):
                    pass
                except OSError:
                    drop(c); continue
            if c.closing and not c.out:
                drop(c)
        if now - last_line >= 3.0:
            dt = now - last_line if last_line else 3.0
            last_line = now
            parts = []
            for u in unis.values():
                age = now - u.last_at
                parts.append(f'U{u.rig} (Art-Net {u.pa}): ' + (f'{u.pps(now)} pkt/s, {u.total} in' + (f', {u.refused} refused' if u.refused else '')
                                                               + ('' if age < args.stale else f', quiet {age:.0f} s') if u.total else 'nothing yet'))
            extra = f' · other universes seen: {", ".join(map(str, sorted(other_unis)))}' if other_unis else ''
            say(f'{sum(1 for k in clients if k.open)} page(s) · ' + ' · '.join(parts) + f' · {sent_count / dt:.0f} frames/s to the page{extra}')
            sent_count = 0
except KeyboardInterrupt:
    say('stopped')
