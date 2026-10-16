#!/usr/bin/env python3
"""Johnny Tremain — the QLC+ workspace from the rig.

    python tools/jt-qlc.py                       # writes assets/johnny-tremain/qlc/johnny-tremain.qxw and validates it
    python tools/jt-qlc.py --library <dir>       # also checks every fixture against QLC+'s own .qxf files in <dir>
                                                 # (a folder holding e.g. ETC-s4-Lustr2.qxf, from resources/fixtures/)

Reads assets/johnny-tremain/rig.json (tools/jt-rig.py) and writes a QLC+ 4 workspace (.qxw) with:
  - every unit patched: name, universe, address, mode, channel count (QLC+ stores universe and address 0-based);
  - fixture groups by hanging position and by system;
  - one Scene per look tag set.json's segments use ("Look: <tag>", folder Looks), and one per segment that adds to its
    look (practicals, specials: "Seg 21.5 …", folder Segments);
  - a Chaser "Johnny Tremain" with one step per scene segment in show order (2 s fades, each step holds until GO), and a
    Virtual Console cue list on it (Space = next).
The XML is what QLC+'s own writers produce (engine/src: Doc, Fixture, FixtureGroup, Scene, Chaser, ChaserStep,
InputOutputMap, Universe; ui/src: App, VirtualConsole, VCFrame, VCCueList — mcallegari/qlcplus master, read 2026-10-16).
Every fixture is in QLC+'s shipped library or is a Generic dimmer, so no custom .qxf is needed (the check below says so).
Standard library only.
"""
import json, math, os, sys
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape, quoteattr

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RIG = os.path.join(ROOT, 'assets', 'johnny-tremain', 'rig.json')
OUTDIR = os.path.join(ROOT, 'assets', 'johnny-tremain', 'qlc')
OUT = os.path.join(OUTDIR, 'johnny-tremain.qxw')
QLC_VERSION = '4.14.1'
INFINITE = 4294967294          # Function::infiniteSpeed(), (uint) -2
FADE_MS = 2000

rig = json.load(open(RIG, encoding='utf-8'))
units = rig['units']
types = rig['types']
STAGE = lambda p: [20.0 + p[0], 0.80 + p[1], 2.30 + p[2]]


# ---------------------------------------------------------------- a look entry → DMX values for one unit
def rgb(hexs):
    h = hexs.lstrip('#')
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    m = max(r, g, b, 1e-6)
    return r / m, g / m, b / m


B = lambda v: max(0, min(255, int(round(v * 255))))


def pan_tilt(u, target):
    """a mover hung head-down: pan 0 = the beam swung toward the house (-z), tilt 0 = straight down → 16-bit values"""
    p = u['pos']
    d = [target[i] - p[i] for i in range(3)]
    n = math.sqrt(sum(v * v for v in d)) or 1
    d = [v / n for v in d]
    tilt = math.degrees(math.acos(max(-1, min(1, -d[1]))))
    pan = math.degrees(math.atan2(d[0], -d[2])) if tilt > 0.5 else 0.0
    prange, trange = u['mover']
    pv = max(0, min(65535, int(round((0.5 + pan / prange) * 65535))))
    tv = max(0, min(65535, int(round((0.5 + tilt / trange) * 65535))))
    return pv >> 8, pv & 255, tv >> 8, tv & 255


GOBO_SLOT = {'none': 0, None: 0, 'water': 10, 'leaves': 15, 'moon': 20, 'window': 25, 'bars': 30}   # Encore wheel slots 1-5 (indexed)


def dmx(u, e):
    """→ list of (channel index, value) — every channel when lit; only the intensity channel(s) when dark"""
    t = u['type']
    lv = e[0] if e else 0.0
    col = e[1] if e else '000000'
    r, g, b = rgb(col) if lv > 0 else (0, 0, 0)
    if t == 'lustr':      # Red Lime Amber Green Cyan Blue Indigo Intensity Strobe Fan
        if lv <= 0:
            return [(7, 0)]
        amber = max(0.0, min(r, g * 1.2) - b)
        lime = max(0.0, min(g, r) - b) * 0.6
        cyan = max(0.0, min(g, b) - r)
        indigo = max(0.0, b - g) * 0.7
        ch = [r, lime, amber, g, cyan, b, indigo]
        m = max(ch) or 1
        return [(i, B(v / m)) for i, v in enumerate(ch)] + [(7, B(lv)), (8, 0), (9, 0)]
    if t in ('cs-par', 'cs-spot'):   # Intensity Red Green Blue Strobe
        if lv <= 0:
            return [(0, 0)]
        return [(0, B(lv)), (1, B(r)), (2, B(g)), (3, B(b)), (4, 0)]
    if t in ('cyc', 'cyc-floor'):    # Dimmer Red Green Blue Amber Lime Strobe
        if lv <= 0:
            return [(0, 0)]
        amber = max(0.0, min(r, g) - b)
        lime = max(0.0, min(g, r) - b) * 0.5
        return [(0, B(lv)), (1, B(r)), (2, B(g)), (3, B(b)), (4, B(amber)), (5, B(lime)), (6, 0)]
    if t in ('s4', 'practical', 'follow'):
        return [(0, B(lv))]
    if t == 'hazer':                  # Unit control, Haze, Haze control
        on = lv > 0
        return [(0, 255 if on else 0), (1, B(lv)), (2, 255 if on else 0)]
    if t == 'encore':
        if lv <= 0:
            return [(1, 0), (2, 0)]
        target = STAGE(e[2]) if len(e) > 2 and e[2] else u['aim']
        p1, p2, t1, t2 = pan_tilt(u, target)
        gobo = e[3] if len(e) > 3 else u.get('gobo')
        v = [0] * 38
        v[0] = 30                                   # shutter open
        dim = int(round(lv * 65535)); v[1], v[2] = dim >> 8, dim & 255
        v[3], v[4], v[5] = B(1 - r), B(1 - g), B(1 - b)   # CMY
        v[8] = GOBO_SLOT.get(gobo, 0); v[9] = 128
        v[11] = 13 if gobo == 'water' else 0        # the animation wheel turning for the water
        v[15] = 128; v[17] = 128                    # zoom, focus at their defaults
        for k in (20, 22, 24, 26, 27):
            v[k] = 127                              # the blades' rotations at 0
        v[28], v[29], v[30], v[31] = p1, p2, t1, t2
        return list(enumerate(v))
    if t == 'aura':      # shutter dimmer zoom pan panF tilt tiltF control wheel R G B W CTC
        if lv <= 0:
            return [(1, 0)]
        target = STAGE(e[2]) if len(e) > 2 and e[2] else u['aim']
        p1, p2, t1, t2 = pan_tilt(u, target)
        w = min(r, g, b)
        return list(enumerate([22, B(lv), 128, p1, p2, t1, t2, 0, 0, B(r - w), B(g - w), B(b - w), B(w), 0]))
    raise ValueError(t)


# ---------------------------------------------------------------- the state of every unit in a segment
def state(look_tag, extras_key):
    st = dict(rig['looks'][look_tag]['units'])
    if extras_key:
        st.update(rig['extras'][extras_key]['units'])
    return st


# ---------------------------------------------------------------- write
fid = {u['id']: i for i, u in enumerate(sorted(units, key=lambda u: (u['universe'], u['address'])))}
by_fid = sorted(units, key=lambda u: fid[u['id']])
L = []
w = L.append
w('<?xml version="1.0" encoding="UTF-8"?>')
w('<!DOCTYPE Workspace>')
w('<Workspace xmlns="http://www.qlcplus.org/Workspace" CurrentWindow="VirtualConsole">')
w(' <Creator>')
w('  <Name>Q Light Controller Plus</Name>')
w(f'  <Version>{QLC_VERSION}</Version>')
w('  <Author>tools/jt-qlc.py (Johnny Tremain, Theatre 2)</Author>')
w(' </Creator>')
w(' <Engine>')
w('  <InputOutputMap>')
w('   <BeatGenerator BeatType="Disabled" BPM="0"/>')
for k, n in sorted(rig['universes'].items()):
    w(f'   <Universe Name={quoteattr(f"Universe {k} (JT {n} ch)")} ID="{int(k) - 1}"/>')
w('  </InputOutputMap>')
for u in by_fid:
    q = u['qlc']
    name = f"{u['id']} {u['purpose']}"[:120]
    w('  <Fixture>')
    w(f'   <Manufacturer>{escape(q["manufacturer"])}</Manufacturer>')
    w(f'   <Model>{escape(q["model"])}</Model>')
    w(f'   <Mode>{escape(q["mode"])}</Mode>')
    w(f'   <ID>{fid[u["id"]]}</ID>')
    w(f'   <Name>{escape(name)}</Name>')
    w(f'   <Universe>{u["universe"] - 1}</Universe>')
    w(f'   <Address>{u["address"] - 1}</Address>')
    w(f'   <Channels>{q["channels"]}</Channels>')
    w('  </Fixture>')
# groups: by position, then by system
groups = {}
for u in by_fid:
    groups.setdefault('Position: ' + u['position'], []).append(u)
SYS = {'front': 'Front light (areas)', 'box': 'Box booms (side-front)', 'top': 'Top light (areas)', 'back': 'Back light (areas)',
       'sideSL': 'Side light from SL (booms)', 'sideSR': 'Side light from SR (booms)', 'pros': 'Pros booms', 'long': 'Long low light from SR',
       'sky': 'Sky: the back brick from above', 'ground': 'Sky: the ground row', 'special': 'Specials', 'mvFOH': 'Movers: water (bridge)',
       'mv1': 'Movers: 1st electric', 'mv2': 'Movers: 2nd electric', 'aura': 'Movers: wash (4th electric)', 'follow': 'Followspots',
       'haze': 'Haze', 'practical': 'Practicals'}
for u in by_fid:
    groups.setdefault('System: ' + SYS[u['system']], []).append(u)
for gi, (gname, us) in enumerate(groups.items()):
    w(f'  <FixtureGroup ID="{gi}">')
    w(f'   <Name>{escape(gname)}</Name>')
    w(f'   <Size X="{len(us)}" Y="1"/>')
    for x, u in enumerate(us):
        w(f'   <Head X="{x}" Y="0" Fixture="{fid[u["id"]]}">0</Head>')
    w('  </FixtureGroup>')
# functions
fn_id = 0
scene_of = {}
functions = []


def scene_xml(fidn, name, path, st):
    out = [f'  <Function ID="{fidn}" Type="Scene" Name={quoteattr(name)} Path={quoteattr(path)}>',
           '   <Speed FadeIn="0" FadeOut="0" Duration="0"/>']
    for u in by_fid:
        vals = dmx(u, st.get(u['id']))
        out.append(f'   <FixtureVal ID="{fid[u["id"]]}">' + ','.join(f'{c},{v}' for c, v in vals) + '</FixtureVal>')
    out.append('  </Function>')
    return out


for tag in sorted(rig['looks']):
    scene_of[('look', tag)] = fn_id
    functions += scene_xml(fn_id, f'Look: {tag}', 'Looks', state(tag, None))
    fn_id += 1
steps = []
for g in rig['segments']:
    if g['extras']:
        key = ('seg', g['extras'])
        if key not in scene_of:
            scene_of[key] = fn_id
            functions += scene_xml(fn_id, f"Seg {g['scene']}.{g['seg']} {g['look']} + extras", 'Segments', state(g['look'], g['extras']))
            fn_id += 1
        steps.append((scene_of[key], g))
    else:
        steps.append((scene_of[('look', g['look'])], g))
chaser_id = fn_id
functions.append(f'  <Function ID="{chaser_id}" Type="Chaser" Name="Johnny Tremain">')
functions.append(f'   <Speed FadeIn="{FADE_MS}" FadeOut="0" Duration="{INFINITE}"/>')
functions.append('   <Direction>Forward</Direction>')
functions.append('   <RunOrder>SingleShot</RunOrder>')
functions.append('   <SpeedModes FadeIn="Common" FadeOut="Common" Duration="Common"/>')
for i, (sid, g) in enumerate(steps):
    note = f"{g['scene']}.{g['seg']} {g['title']}: {g['location']}"[:150]
    functions.append(f'   <Step Number="{i}" FadeIn="{FADE_MS}" Hold="{INFINITE}" FadeOut="0" Note={quoteattr(note)}>{sid}</Step>')
functions.append('  </Function>')
L += functions
w(' </Engine>')
appearance = ['   <Appearance>', '    <FrameStyle>None</FrameStyle>', '    <ForegroundColor>Default</ForegroundColor>',
              '    <BackgroundColor>Default</BackgroundColor>', '    <BackgroundImage>None</BackgroundImage>', '    <Font>Default</Font>', '   </Appearance>']
w(' <VirtualConsole>')
w('  <Frame Caption="">')
L += [a[1:] for a in appearance]
w('   <CueList Caption="Johnny Tremain" ID="0">')
w('    <WindowState Visible="True" X="10" Y="10" Width="720" Height="560"/>')
L += [' ' + a for a in appearance]
w(f'    <Chaser>{chaser_id}</Chaser>')
w('    <NextPrevBehavior>0</NextPrevBehavior>')
w('    <Next>')
w('     <Key>Space</Key>')
w('    </Next>')
w('    <Previous/>')
w('    <Playback/>')
w('    <Stop/>')
w('   </CueList>')
w('  </Frame>')
w('  <Properties>')
w('   <Size Width="1920" Height="1080"/>')
w('   <GrandMaster Visible="1" ChannelMode="Intensity" ValueMode="Reduce" SliderMode="Normal"/>')
w('  </Properties>')
w(' </VirtualConsole>')
w('</Workspace>')
os.makedirs(OUTDIR, exist_ok=True)
with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
    f.write('\n'.join(L) + '\n')

# ---------------------------------------------------------------- validate what was written
fails = []
NS = '{http://www.qlcplus.org/Workspace}'
try:
    tree = ET.parse(OUT)
except ET.ParseError as e:
    print(f'jt-qlc: FAIL — {OUT} does not parse: {e}'); sys.exit(1)
root = tree.getroot()
eng = root.find(NS + 'Engine')
fx = eng.findall(NS + 'Fixture')
if len(fx) != len(units):
    fails.append(f'{len(fx)} fixtures written, rig.json has {len(units)}')
used = {}
for f in fx:
    g = lambda k: f.find(NS + k).text
    i, uni, a, n = int(g('ID')), int(g('Universe')), int(g('Address')), int(g('Channels'))
    u = by_fid[i]
    t = types[u['type']]
    if (g('Manufacturer'), g('Model'), g('Mode')) != (t['qlc']['manufacturer'], t['qlc']['model'], t['qlc']['mode']):
        fails.append(f'{u["id"]}: definition {g("Manufacturer")}/{g("Model")}/{g("Mode")} is not its type\'s')
    if n != len(t['channelNames']):
        fails.append(f'{u["id"]}: {n} channels, its mode has {len(t["channelNames"])}')
    if not (0 <= a and a + n <= 512):
        fails.append(f'{u["id"]}: address {a + 1}…{a + n} is outside 1…512')
    for c in range(a, a + n):
        if (uni, c) in used:
            fails.append(f'{u["id"]}: universe {uni + 1} channel {c + 1} overlaps {used[(uni, c)]}')
        used[(uni, c)] = u['id']
fn = {int(f.get('ID')): f for f in eng.findall(NS + 'Function')}
nfix = {int(f.find(NS + 'ID').text): int(f.find(NS + 'Channels').text) for f in fx}
for f in fn.values():
    if f.get('Type') == 'Scene':
        for v in f.findall(NS + 'FixtureVal'):
            k = int(v.get('ID')); nums = [int(x) for x in (v.text or '').split(',') if x != '']
            if k not in nfix: fails.append(f'scene {f.get("Name")}: fixture {k} does not exist')
            if len(nums) % 2: fails.append(f'scene {f.get("Name")}: fixture {k} has an odd value list')
            for c, val in zip(nums[::2], nums[1::2]):
                if not (0 <= c < nfix.get(k, 0)) or not (0 <= val <= 255):
                    fails.append(f'scene {f.get("Name")}: fixture {k} channel {c} value {val} out of range')
chasers = [f for f in fn.values() if f.get('Type') == 'Chaser']
for c in chasers:
    st = c.findall(NS + 'Step')
    if len(st) != len(rig['segments']):
        fails.append(f'chaser {c.get("Name")}: {len(st)} steps for {len(rig["segments"])} segments')
    for s in st:
        if int(s.text) not in fn or fn[int(s.text)].get('Type') != 'Scene':
            fails.append(f'chaser step {s.get("Number")} references function {s.text}, not a scene')
cl = root.find(f'{NS}VirtualConsole/{NS}Frame/{NS}CueList/{NS}Chaser')
if cl is None or int(cl.text) not in fn:
    fails.append('the cue list does not point at a function')
for gr in eng.findall(NS + 'FixtureGroup'):
    for h in gr.findall(NS + 'Head'):
        if int(h.get('Fixture')) not in nfix:
            fails.append(f'group {gr.find(NS + "Name").text}: fixture {h.get("Fixture")} does not exist')
# against QLC+'s own library files, when given: every non-generic fixture's manufacturer, model, mode and channel names
lib = sys.argv[sys.argv.index('--library') + 1] if '--library' in sys.argv else None
libnote = 'not checked against the library files (pass --library <dir>)'
if lib:
    FD = '{http://www.qlcplus.org/FixtureDefinition}'
    defs = {}
    for name in os.listdir(lib):
        if name.endswith('.qxf'):
            r = ET.parse(os.path.join(lib, name)).getroot()
            defs[(r.find(FD + 'Manufacturer').text, r.find(FD + 'Model').text)] = {m.get('Name'): [c.text for c in m.findall(FD + 'Channel')] for m in r.findall(FD + 'Mode')}
    checked = 0
    for k, t in types.items():
        q = t['qlc']
        if q['manufacturer'] == 'Generic':
            if q['model'] != 'Generic' or q['mode'] != f"{q['channels']} Channel":
                fails.append(f'{k}: a generic dimmer must be Generic / Generic / "<n> Channel"')
            continue
        d = defs.get((q['manufacturer'], q['model']))
        if d is None:
            fails.append(f'{k}: {q["manufacturer"]} {q["model"]} is not in the library files given'); continue
        if q['mode'] not in d:
            fails.append(f'{k}: mode "{q["mode"]}" not in {sorted(d)}'); continue
        if d[q['mode']] != t['channelNames']:
            fails.append(f'{k}: mode "{q["mode"]}" channels {d[q["mode"]]} differ from rig.json\'s'); continue
        checked += 1
    libnote = f'{checked} fixture types matched QLC+\'s library files exactly (manufacturer, model, mode, channel names), the rest Generic dimmers'
size = os.path.getsize(OUT)
nscenes = sum(1 for f in fn.values() if f.get('Type') == 'Scene')
print(f'jt-qlc: {"PASS" if not fails else "FAIL"} — {os.path.relpath(OUT, ROOT)} ({size / 1024:.0f} KB) parses; {len(fx)} fixtures in '
      f'{len(rig["universes"])} universes ({", ".join(f"U{k} {v} ch" for k, v in sorted(rig["universes"].items()))}), no overlaps, all ≤ 512; '
      f'{len(eng.findall(NS + "FixtureGroup"))} groups; {nscenes} scenes; chaser "Johnny Tremain" {len(steps)} steps, every one a scene; cue list on it; {libnote}'
      + ('' if not fails else '\n  ' + '\n  '.join(fails)))
sys.exit(1 if fails else 0)
