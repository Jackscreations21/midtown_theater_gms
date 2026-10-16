#!/usr/bin/env python3
"""Johnny Tremain in Theatre 2 — the lighting rig, written as data.

    python tools/jt-rig.py          # writes assets/johnny-tremain/rig.json and docs/johnny-tremain/LIGHT-PLOT.md

One record per unit (position, hang point and aim in WORLD metres, the fixture, its QLC+ definition, universe and address,
what it is for), every look tag set.json's segments use resolved to per-unit levels and colours, and the per-segment
extras (the furnace, the steeple lanterns, the specials a scene calls for). midtown.html (THEATRE 2: JOHNNY TREMAIN —
THE LIGHTS) draws and lights from it; tools/jt-qlc.py turns it into the QLC+ workspace. Standard library only.

Frames (docs/johnny-tremain/CONTRACT.md): stage (x +SR, y up from the deck, z upstage of the proscenium plane) →
world = (20 + x, 0.80 + y, 2.30 + z). Hanging positions are the ones measured in LIGHTING-NEEDS.md §6, re-measured off
the scan in the page (the bridge's front rail tops out at y 7.23 at z -3.30; the splay walls at z -2.6 stand at x 13.38
and 27.01; the apron walls at 14.35 / 25.95; the SL wing wall 10.45-10.56; the SR side room's wall x 25.98 below z 3.9).
"""
import json, math, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'assets', 'johnny-tremain', 'rig.json')
SET = os.path.join(ROOT, 'assets', 'johnny-tremain', 'set.json')


def W(x, y, z):
    """stage → world"""
    return [round(20.0 + x, 3), round(0.80 + y, 3), round(2.30 + z, 3)]


# ---------------------------------------------------------------- the fixtures
# key: QLC+ manufacturer / model / mode / channels EXACTLY as the QLC+ fixture library has them (resources/fixtures/ of
# github.com/mcallegari/qlcplus, checked 2026-10-16); glb: the repo's model that draws it (assets/fixtures/, its lod/ copy);
# field: the default field angle (deg); power: brightness at its focus point relative to a nominal area light (the page
# scales each unit by its throw, so an even wash reads even); chans: the mode's channel names in order.
TYPES = {
    'lustr': dict(name='ETC Source Four LED Series 2 Lustr', glb='s4-lustr', field=26, power=1.0,
                  qlc=('ETC', 'Source Four LED Series 2 Lustr', 'Direct'),
                  chans=['Red', 'Lime', 'Amber', 'Green', 'Cyan', 'Blue', 'Indigo', 'Intensity', 'Strobe', 'Fan Control']),
    'cs-spot': dict(name='ETC ColorSource Spot', glb='source-four', field=26, power=0.9,
                    qlc=('ETC', 'ColorSource Spot', '5-Channel'), chans=['Intensity', 'Red', 'Green', 'Blue', 'Strobe']),
    'cs-par': dict(name='ETC ColorSource PAR', glb='colorsource-par', field=40, power=0.8,
                   qlc=('ETC', 'ColorSource PAR', '5-channel'), chans=['Intensity', 'Red', 'Green', 'Blue', 'Strobe']),
    's4': dict(name='ETC Source Four 750 W (tungsten) on a dimmer', glb='source-four', field=26, power=0.9,
               qlc=('Generic', 'Generic', '1 Channel'), chans=['Dimmer #1']),
    'encore': dict(name='Martin MAC Encore Performance CLD', glb='mac-viper', field=20, power=1.3, mover=(540, 268),
                   qlc=('Martin', 'MAC Encore Performance', 'CLD'),
                   chans=['Shutter / Strobe', 'Dimmer', 'Dimmer fine', 'Cyan', 'Magenta', 'Yellow', 'CTO', 'Color Wheel',
                          'Rotating Gobo Wheel', 'Gobo Indexing Angle', 'Gobo Indexing Angle fine', 'Animation Wheel Function',
                          'Animation Wheel Indexing Angle', 'Frost', 'Iris', 'Zoom', 'Zoom fine', 'Focus', 'Focus fine',
                          'Framing Blade 1 Insertion', 'Framing Blade 1 Rotation', 'Framing Blade 2 Insertion',
                          'Framing Blade 2 Rotation', 'Framing Blade 3 Insertion', 'Framing Blade 3 Rotation',
                          'Framing Blade 4 Insertion', 'Framing Blade 4 Rotation', 'Framing Blade System Rotation', 'Pan',
                          'Pan fine', 'Tilt', 'Tilt fine', 'Fixture Control', 'FX1 Selection', 'FX1 Speed', 'FX2 Selection',
                          'FX2 Speed', 'FX Synchronization']),
    'aura': dict(name='Martin MAC Aura', glb='glp-x4', field=30, power=0.9, mover=(540, 232),
                 qlc=('Martin', 'MAC Aura', 'Standard'),
                 chans=['Beam electronic shutter effect', 'Beam dimmer', 'Zoom', 'Pan', 'Pan Fine', 'Tilt', 'Tilt Fine',
                        'Fixture control settings', 'Beam color wheel effect', 'Beam Red', 'Beam Green', 'Beam Blue',
                        'Beam White', 'Beam CTC']),
    'cyc': dict(name='Chauvet Ovation CYC 1 FC', glb='elar-108', field=90, power=0.8,
                qlc=('Chauvet', 'Ovation CYC 1 FC', '7 Channel'),
                chans=['Dimmer', 'Red', 'Green', 'Blue', 'Amber', 'Lime', 'Strobe']),
    'cyc-floor': dict(name='Chauvet Ovation CYC 1 FC (ground row)', glb='colorblast', field=90, power=0.7, floor=True,
                      qlc=('Chauvet', 'Ovation CYC 1 FC', '7 Channel'),
                      chans=['Dimmer', 'Red', 'Green', 'Blue', 'Amber', 'Lime', 'Strobe']),
    'follow': dict(name="Robert Juliat D'Artagnan 934SNX followspot", glb='lycian', field=6, power=1.6, floor=True,
                   qlc=('Robert Juliat', "D'Artagnan 934SNX", '1 (1 channel)'), chans=['Dimmer']),
    'hazer': dict(name='MDG ATMe hazer', glb='hazer', field=0, power=0, floor=True,
                  qlc=('MDG', 'ATMe', '3 Channel'), chans=['Unit control', 'Haze', 'Haze control']),
    'practical': dict(name='practical on a dimmer', glb=None, field=0, power=0.35,
                      qlc=('Generic', 'Generic', '1 Channel'), chans=['Dimmer #1']),
}

units = []


def add(pid, position, typ, pos, aim, purpose, system, area=None, special=None, pool=None, gobo=None, colour='LED colour mix',
        beam=False, power=None, row=None):
    """one unit; pos = the hang point (or the floor under it), aim = its focus point, both world"""
    t = TYPES[typ]
    d = math.dist(pos, aim) if aim else 0
    field = t['field']
    if pool and d:                                   # a focused special: the field that makes this pool at this throw
        field = round(2 * math.degrees(math.atan(pool / 2 / d)), 1)
    units.append(dict(id=pid, position=position, type=typ, fixture=t['name'], pos=[round(v, 3) for v in pos],
                      aim=[round(v, 3) for v in aim] if aim else None, field=field, purpose=purpose, system=system,
                      area=area, row=row, special=special, gobo=gobo, colour=colour, beam=beam,
                      power=power if power is not None else t['power']))


# The focus height: heads (1.6 over the floor they stand on)
AREAS = {  # stage x, z, floor y
    'APR': (3.5, -1.3, 0), 'APC': (0, -1.3, 0), 'APL': (-3.5, -1.3, 0),
    'DSR': (2.85, 0.85, 0), 'DSC': (0, 0.85, 0), 'DSL': (-2.85, 0.85, 0),
    'MSR': (2.85, 2.5, 0), 'MSC': (0, 2.5, 0), 'MSL': (-2.85, 2.5, 0),
    'SHOP': (-2.4, 5.0, 0), 'LOFT': (-3.55, 4.65, 2.4), 'WHARF': (3.55, 4.7, 0.45), 'PATH': (0.2, 5.0, 0),
}
ROWS = {'AP': ['APL', 'APC', 'APR'], 'DS': ['DSL', 'DSC', 'DSR'], 'MS': ['MSL', 'MSC', 'MSR'], 'US': ['SHOP', 'LOFT', 'WHARF', 'PATH']}


def A(area, h=1.6):
    x, z, f = AREAS[area]
    return W(x, f + h, z)


# ---------------------------------------------------------------- FOH 1: the lighting bridge (the scan's own)
# A pipe on the bridge's stage-side rail: y 6.95, z -3.15 (the rail's face is at z -3.30, its top 7.23), x 15.6…24.4.
BR_Y, BR_Z = 6.95, -3.15
bridge = [  # (x, what) SL → SR
    (15.70, ('S11', 'Loft isolation, front (S11)', W(-3.55, 2.4 + 1.6, 4.65), 3.6)),
    (16.10, ('S2', 'Narrator DSL (S2)', W(-3.6, 1.6, -1.6), 2.0)),
    (16.50, ('APL', None, None, None)),
    (16.90, ('S27a', 'Shop door 1 slice (S27)', W(-3.6, 1.2, -1.2), 1.0)),
    (17.30, ('DSL', None, None, None)),
    (17.70, ('S7', 'Cup at the gravestone (S7)', W(-2.6, 0.6, 0.8), 0.8)),
    (18.10, ('S13', 'Lavinia, rosy lift (S13)', W(-1.25, 1.6, 1.8), 1.8)),
    (18.50, ('S27b', 'Shop door 2 slice (S27)', W(-1.2, 1.2, -1.2), 1.0)),
    (18.90, ('APC', None, None, None)),
    (19.40, ('S6', 'Cups on the courtroom table (S6)', W(-0.7, 0.85, 3.0), 0.9)),
    (20.60, ('DSC', None, None, None)),
    (21.00, ('S27c', 'Shop door 3 slice (S27)', W(1.2, 1.2, -1.2), 1.0)),
    (21.40, ('S4', 'Cup pin, the wharf\'s lip (S4)', W(1.6, 0.4, -2.35), 0.5)),
    (22.20, ('APR', None, None, None)),
    (22.60, ('S27d', 'Shop door 4 slice (S27)', W(3.6, 1.2, -1.2), 1.0)),
    (23.00, ('DSR', None, None, None)),
    (23.80, ('S1', 'Narrator DSR (S1)', W(3.6, 1.6, -1.6), 2.0)),
]
for i, (x, (key, label, aim, pool)) in enumerate(bridge, 1):
    pos = [x, BR_Y, BR_Z]
    if key in AREAS:
        add(f'BR-{i:02d}', 'FOH 1 — the bridge', 'lustr', pos, A(key), f'Front light {key}', 'front', area=key)
    else:
        sp = key.rstrip('abcd') if key.startswith('S27') else key
        add(f'BR-{i:02d}', 'FOH 1 — the bridge', 'lustr', pos, aim, label, 'special', special=key, pool=pool,
            gobo='slice' if sp == 'S27' else None, colour='LED, cool white for the cups' if sp in ('S4', 'S6', 'S7') else 'LED colour mix')
# the two water movers at the bridge's ends (S17 water, S31 the boats from the house)
add('BR-M1', 'FOH 1 — the bridge', 'encore', [15.20, BR_Y, BR_Z], W(-1.5, 0, -1.0), 'Water / boats from the house (S17, S31)', 'mvFOH', gobo='water', beam=True)
add('BR-M2', 'FOH 1 — the bridge', 'encore', [24.60, BR_Y, BR_Z], W(1.5, 0, -1.0), 'Water (S17)', 'mvFOH', gobo='water', beam=True)

# ---------------------------------------------------------------- FOH 2: behind the bridge (house 1's Apron Electric line)
F2_Y, F2_Z = 7.20, -5.20
for i, (x, key) in enumerate([(15.6, 'SHOP'), (16.8, 'MSL'), (18.0, 'LOFT'), (19.4, 'MSC'), (20.6, 'PATH'), (22.0, 'WHARF'), (23.4, 'MSR')], 1):
    add(f'F2-{i:02d}', 'FOH 2 — behind the bridge', 'lustr', [x, F2_Y, F2_Z], A(key), f'Front light {key}', 'front', area=key)

# ---------------------------------------------------------------- box booms on the splay walls (side-front, crossed)
STRUCT = []      # what the units hang on: {kind, name, a, b (world), r} — pipes, booms, arms, drops; the page draws them
for side, x, wx, areas in (('HR', 13.85, 13.48, ['APR', 'DSR', 'MSR']), ('HL', 26.55, 26.92, ['APL', 'DSL', 'MSL'])):
    sgn = 1 if side == 'HR' else -1
    name = f'Box boom house {"right" if side == "HR" else "left"}'
    STRUCT.append(dict(kind='boom', name=name, a=[x, 2.55, -2.50], b=[x, 5.95, -2.50], r=0.024))
    for y in (2.9, 5.7):
        STRUCT.append(dict(kind='arm', name=name + ' wall arm', a=[wx, y, -2.50], b=[x, y, -2.50], r=0.02))
    for i, (y, key) in enumerate(zip([3.0, 4.2, 5.4], areas), 1):
        ux = x + 0.30 * sgn
        STRUCT.append(dict(kind='arm', name=name + ' side arm', a=[x, y + 0.02, -2.50], b=[ux, y + 0.02, -2.50], r=0.016))
        add(f'BB{side}-{i}', name, 'lustr', [ux, y, -2.50], A(key), f'Side-front {key}', 'box', area=key)

# ---------------------------------------------------------------- pros booms on the apron walls (apron side light)
for nm, x, wx, ux in (('Pros boom house right', 14.50, 14.37, 14.80), ('Pros boom house left', 25.80, 25.93, 25.50)):
    STRUCT.append(dict(kind='boom', name=nm, a=[x, 1.8, 0.60], b=[x, 3.8, 0.60], r=0.024))
    for y in (2.0, 3.6):
        STRUCT.append(dict(kind='arm', name=nm + ' wall arm', a=[wx, y, 0.60], b=[x, y, 0.60], r=0.02))
    STRUCT.append(dict(kind='arm', name=nm + ' side arm', a=[x, 3.02, 0.60], b=[ux, 3.02, 0.60], r=0.016))
add('PB-L', 'Pros boom house right', 'cs-spot', [14.80, 3.0, 0.60], W(1.0, 1.4, -1.3), 'Apron side light from SL', 'pros', row='AP')
add('PB-R', 'Pros boom house left', 'cs-spot', [25.50, 3.0, 0.60], W(-1.0, 1.4, -1.3), 'Apron side light from SR', 'pros', row='AP')

# ---------------------------------------------------------------- the four electrics (cross-stage pipes above the iron, out of the front row's sight)
# Heights: the front row's eye (stage 0, 0.32, -4.30) sees through the arch (header 4.40 over the deck) and, upstage of the
# masking border (z 3.0, 4.40-5.00), over the border's top: anything under 0.32 + 0.949 (z + 4.30) over the deck shows. So the
# 1st and 2nd hang at 8.5 (7.7 over the deck; their bodies' bottoms ~7.75 world), the 3rd at 10.1, the 4th at 11.6.
EY = {1: 8.50, 2: 8.50, 3: 10.10, 4: 11.60}
EZ = {1: W(0, 0, 0.6)[2], 2: W(0, 0, 2.4)[2], 3: W(0, 0, 4.2)[2], 4: W(0, 0, 5.7)[2]}   # the 4th at 5.7, clear of the masts' lane (6.33)
# never over the iron's centre walkway x 19.2…21.1 (it would shade them): units at ≤ 18.9 or ≥ 21.4
elec = {1: [], 2: [], 3: [], 4: []}


def E(n, x, typ, aim, purpose, system, **kw):
    elec[n].append((x, typ, aim, purpose, system, kw))


# 1st (stage z 0.6): DS top, apron back, the eyes, the jail bars, the wig, two movers
E(1, 15.0, 'encore', W(-3.0, 0, 1.5), 'Mover: leaves / window / the ride (S21, S29)', 'mv1', gobo='leaves', beam=True)
E(1, 16.4, 'cs-par', A('DSL'), 'Top light DSL', 'top', area='DSL')
E(1, 17.0, 's4', W(-2.8, 0.5, 1.6), 'Jail bars (S15)', 'special', special='S15', pool=2.0, gobo='bars', colour='L202 half CTB, bars gobo', beam=True)
E(1, 17.6, 'cs-par', A('APL'), 'Back light APL', 'back', area='APL')
E(1, 18.3, 'cs-spot', W(0, 1.6, 0.5), 'The eight eyes: tight cold top (S28)', 'special', special='S28', pool=1.2, beam=True)
E(1, 18.9, 'cs-par', A('DSC'), 'Top light DSC', 'top', area='DSC')
E(1, 21.4, 'cs-par', A('APC'), 'Back light APC', 'back', area='APC')
E(1, 22.0, 'cs-spot', W(3.0, 1.4, 1.2), 'Lantern reveal: the wig (S24)', 'special', special='S24b', pool=0.9)
E(1, 22.7, 'cs-par', A('APR'), 'Back light APR', 'back', area='APR')
E(1, 23.6, 'cs-par', A('DSR'), 'Top light DSR', 'top', area='DSR')
E(1, 25.0, 'encore', W(3.0, 0, 1.5), 'Mover: leaves / the ride (S21, S29)', 'mv1', gobo='leaves', beam=True)
# 2nd (stage z 2.4): MS top, DS back, the sideboard strip, two reveals, the sheet, two movers
E(2, 15.0, 'encore', W(-2.5, 0, 3.0), 'Mover: moon and cloud breakup (S18)', 'mv2', gobo='moon', beam=True)
E(2, 16.4, 'cs-par', A('MSL'), 'Top light MSL', 'top', area='MSL')
E(2, 17.0, 's4', W(-2.6, 1.1, 3.3), 'The cups on the sideboard, shuttered strip (S5)', 'special', special='S5', pool=1.8, gobo='strip', colour='L202 half CTB, shuttered 1.8 × 0.4')
E(2, 17.6, 'cs-par', A('DSL'), 'Back light DSL', 'back', area='DSL')
E(2, 18.9, 'cs-par', A('MSC'), 'Top light MSC', 'top', area='MSC')
E(2, 18.25, 'cs-spot', W(0, 1.5, 1.6), 'The sheet, backlit (S32)', 'special', special='S32', pool=3.0, beam=True)
E(2, 21.4, 'cs-par', A('DSC'), 'Back light DSC', 'back', area='DSC')
E(2, 22.0, 'cs-spot', W(0.9, 0.6, 3.0), 'Lantern reveal: the tipped chair (S24)', 'special', special='S24c', pool=0.9)
E(2, 22.7, 'cs-par', A('DSR'), 'Back light DSR', 'back', area='DSR')
E(2, 23.4, 'cs-spot', W(3.6, 1.0, 1.9), 'Lantern reveal: the dressing table (S24)', 'special', special='S24a', pool=0.9)
E(2, 24.0, 'cs-par', A('MSR'), 'Top light MSR', 'top', area='MSR')
E(2, 25.0, 'encore', W(2.5, 0, 3.0), 'Mover: moon breakup / the ride (S18, S29)', 'mv2', gobo='moon', beam=True)
# 3rd (stage z 4.2): upstage top, MS back, the loft from over it, the steeple pin
E(3, 15.6, 'cs-par', W(-3.55, 2.4 + 1.6, 3.75), 'Top light LOFT, downstage half and the ladder head (S11)', 'top', area='LOFT')
E(3, 16.6, 'cs-par', W(-3.55, 2.4 + 1.6, 5.55), 'Top light LOFT, upstage half (S11)', 'top', area='LOFT')
E(3, 17.4, 'cs-par', A('MSL'), 'Back light MSL', 'back', area='MSL')
E(3, 18.9, 'cs-par', A('PATH'), 'Top light PATH', 'top', area='PATH')
E(3, 21.4, 'cs-par', A('MSC'), 'Back light MSC', 'back', area='MSC')
E(3, 22.2, 'cs-spot', W(2.6, 3.7, 6.05), 'Steeple lanterns pin (S22)', 'special', special='S22', pool=1.0, beam=True)
E(3, 22.9, 'cs-par', A('WHARF'), 'Top light WHARF', 'top', area='WHARF')
E(3, 23.8, 'cs-par', A('MSR'), 'Back light MSR', 'back', area='MSR')
# 4th (stage z 5.8): the back wall from above, upstage back light, Otis, Rab, the volley flash, four wash movers
for x, sx in ((14.6, -4.5), (17.4, -1.8), (22.6, 1.8), (25.4, 4.5)):
    E(4, x, 'cyc', W(sx, 7.0, 6.6), 'Back brick wash from above (the sky)', 'sky', colour='LED RGBAL')
E(4, 15.0, 'aura', W(-3.0, 0, 3.5), 'Wash mover: back light colour, the ride', 'aura', beam=True)
E(4, 16.0, 'cs-par', A('LOFT'), 'Back light LOFT', 'back', area='LOFT')
E(3, 16.1, 'cs-spot', W(-3.3, 4.2, 4.65), 'Otis at the rafters (S12), steep top', 'special', special='S12', pool=1.5, beam=True)
E(4, 18.2, 'aura', W(-1.0, 0, 2.0), 'Wash mover: back light colour, the ride', 'aura', beam=True)
E(4, 18.9, 'cs-spot', W(0.2, 1.6, 5.0), 'Rab at the back: soft cool backlight (S33)', 'special', special='S33', pool=1.8, beam=True)
E(4, 21.4, 'cs-par', A('PATH'), 'Back light PATH', 'back', area='PATH')
E(4, 21.9, 'aura', W(1.0, 0, 2.0), 'Wash mover: back light colour, the ride', 'aura', beam=True)
E(4, 23.0, 'cs-par', A('WHARF'), 'Back light WHARF', 'back', area='WHARF')
E(4, 24.2, 'cs-par', W(0, 2.0, 1.0), 'The volley flash behind Johnny (S28), strobe', 'special', special='S28f')
E(4, 25.0, 'aura', W(3.0, 0, 3.5), 'Wash mover: back light colour, the ride', 'aura', beam=True)

for n in (1, 2, 3, 4):
    for i, (x, typ, aim, purpose, system, kw) in enumerate(sorted(elec[n], key=lambda e: e[0]), 1):
        add(f'E{n}-{i:02d}', f'{"1st 2nd 3rd 4th".split()[n - 1]} Electric', typ, [x, EY[n], EZ[n]], aim, purpose, system, **kw)

# ---------------------------------------------------------------- side booms in the wings (the dance, the ride, the specials)
# SL x 13.5 at stage z 1.1 / 3.3 / 5.3; SR in-1 inside the SR pocket (x 25.75, z 3.1), SR x 26.5 at 3.3 / 5.3.
# shin 0.4, mid 1.4, head 2.6 over the deck; each crosses to the far side of its row at that height.
def boom(code, label, x, sz, units_):
    top = max(h for h, *_ in units_) + 0.25
    z = 2.30 + sz
    sgn = 1 if x < 20 else -1                      # the side arms reach onstage
    STRUCT.append(dict(kind='boom', name=label, a=[x, 0.80, z], b=[x, 0.80 + top, z], r=0.024))
    STRUCT.append(dict(kind='base', name=label + ' base', a=[x, 0.80, z], b=[x, 0.83, z], r=0.30))
    for i, (h, typ, aim, purpose, system, kw) in enumerate(units_, 1):
        ux = x + 0.30 * sgn
        STRUCT.append(dict(kind='arm', name=label + ' side arm', a=[x, 0.80 + h + 0.02, z], b=[ux, 0.80 + h + 0.02, z], r=0.016))
        add(f'{code}-{i}', label, typ, [ux, 0.80 + h, z], aim, purpose, system, **kw)


def side(h, sx, sz, row, frm):
    tgt = {0.4: (3.2, 0.5), 1.4: (1.2, 1.3), 2.6: (-0.6, 1.7)}[h]
    x = tgt[0] * (1 if frm == 'SL' else -1)
    return (h, 'cs-spot', W(x, tgt[1], sz), f'Side light {row} from {frm} ({ {0.4: "shin", 1.4: "mid", 2.6: "head"}[h] })',
            'side' + frm, dict(row=row))


boom('SL1', 'SL boom 1 (in 1)', 13.5, 1.1, [side(0.4, -6.5, 1.1, 'DS', 'SL'), side(1.4, -6.5, 1.1, 'DS', 'SL'), side(2.6, -6.5, 1.1, 'DS', 'SL'),
     (3.4, 'cs-spot', W(-4.4, 1.6, 0.9), 'The SL in-1 doorway (S14)', 'special', dict(special='S14b', pool=1.6, beam=True))])
boom('SL2', 'SL boom 2 (in 2)', 14.15, 3.3, [side(0.4, -6.5, 3.3, 'MS', 'SL'), side(1.4, -6.5, 3.3, 'MS', 'SL'), side(2.6, -6.5, 3.3, 'MS', 'SL'),
     (3.2, 'cs-spot', W(-2.3, 0.8, 5.2), 'Bucket, boy and furnace isolation (S10)', 'special', dict(special='S10', pool=2.6)),
     (4.0, 'cs-spot', W(-1.0, 0.8, 2.5), 'Window light through the window flat (S16)', 'special', dict(special='S16', pool=2.6, gobo='window', beam=True))])
boom('SL3', 'SL boom 3 (in 3)', 14.15, 5.3, [side(0.4, -6.5, 5.3, 'US', 'SL'), side(1.4, -6.5, 5.3, 'US', 'SL'), side(2.6, -6.5, 5.3, 'US', 'SL'),
     (1.0, 'cs-spot', W(-2.6, 1.0, 5.1), 'The crucible pour: hot low snap (S9)', 'special', dict(special='S9', pool=1.0))])
boom('SR1', 'SR boom 1 (in 1, the pocket)', 25.75, 0.8, [side(1.4, 5.75, 0.8, 'DS', 'SR'), side(2.6, 5.75, 0.8, 'DS', 'SR')])
boom('SR2', 'SR boom 2 (in 2)', 26.5, 3.3, [side(0.4, 6.5, 3.3, 'MS', 'SR'), side(1.4, 6.5, 3.3, 'MS', 'SR'), side(2.6, 6.5, 3.3, 'MS', 'SR'),
     (4.0, 'cs-spot', W(-3.0, 0.6, 2.0), 'Long low light from SR: dawn, sunset (S19, S20)', 'long', dict(row='MS'))])
boom('SR3', 'SR boom 3 (in 3)', 26.5, 5.3, [side(0.4, 6.5, 5.3, 'US', 'SR'), side(1.4, 6.5, 5.3, 'US', 'SR'), side(2.6, 6.5, 5.3, 'US', 'SR'),
     (4.0, 'cs-spot', W(-3.0, 0.6, 3.6), 'Long low light from SR: dawn, sunset (S19, S20)', 'long', dict(row='US'))])

# ---------------------------------------------------------------- ground row along the back brick (behind the piles and the loft)
for i, x in enumerate([15.5, 16.8, 18.1, 21.9, 23.2, 24.5], 1):    # round the stage doors (x 19…21)
    add(f'GR-{i}', 'Ground row (the back brick)', 'cyc-floor', [x, 0.80, 8.65], [x, 4.5, 8.90], 'Back brick from below (the sky)', 'ground', colour='LED RGBAL')

# ---------------------------------------------------------------- floor, through the doors, the booth, haze
add('FL-1', 'Floor (under the loft, beside the bellows)', 'cs-par', W(-4.2, 0.0, 5.0), W(-2.2, 1.5, 5.4), 'Furnace glow on Johnny\'s face (S8)', 'special', special='S8')
add('DR-1', 'Backstage corridor, through the stage doors', 'cs-spot', [20.0, 3.0, 10.5], W(0.2, 1.5, 3.3), 'The doorway backlight (S14)', 'special', special='S14', pool=2.4, beam=True)
for i, x in enumerate([17.8, 22.2], 1):
    add(f'FS-{i}', "Theatre 2's followspot booth", 'follow', [x, 3.28, -14.90], W(3.6, 1.6, -1.6), 'Followspot (S3): Johnny anywhere, the aisle', 'follow', special='S3', pool=1.6, beam=True)
add('HZ-1', 'SL wing, downstage of the understage stair (floor)', 'hazer', [11.30, 0.80, 3.65], None, 'Haze', 'haze')
add('HZ-2', 'SR wing, upstage (floor)', 'hazer', [28.80, 0.80, 8.30], None, 'Haze', 'haze')

# ---------------------------------------------------------------- practicals (each its own dimmer channel)
PRACTICALS = [
    ('P-01', 'Furnace glow (orange LED, flicker)', W(-2.4, 0.6, 5.8), 'fire', 1.8),
    ('P-02', 'Hand lantern (radio dimmer)', W(0.6, 1.0, 0.3), 'lantern', 0.6),
    ('P-03', 'Church lantern 1 (steeple)', W(2.35, 3.45, 6.05), 'candle', 0.5),
    ('P-04', 'Church lantern 2 (steeple)', W(2.85, 3.45, 6.05), 'candle', 0.5),
    ('P-05', 'Candelabra, candles 1', W(0.0, 1.1, 1.8), 'candle', 0.35),
    ('P-06', 'Candelabra, candles 2', W(0.2, 1.1, 1.8), 'candle', 0.35),
    ('P-07', 'Candelabra, candles 3', W(0.4, 1.1, 1.8), 'candle', 0.35),
    ('P-08', 'Sideboard candlesticks (pair)', W(-2.6, 1.3, 3.3), 'candle', 0.35),
    ('P-09', 'Candlesticks: the judge\'s, the Green Dragon\'s, Buckman\'s', W(-0.4, 1.0, 3.0), 'candle', 0.35),
    ('P-10', 'Torches ×2 (flicker)', W(-3.0, 1.9, 1.0), 'fire', 0.9),
    ('P-11', 'Coach lamps ×2', W(1.8, 1.6, 1.6), 'lantern', 0.4),
    ('P-12', 'Campfires ×2 (flicker)', W(-0.6, 0.3, 1.2), 'fire', 0.9),
    ('P-13', 'Distant lights, SR string (S30)', W(2.5, 1.0, 6.5), 'twinkle', 0.15),
    ('P-14', 'Distant lights, SL string (S30)', W(-2.5, 1.0, 6.5), 'twinkle', 0.15),
]
for pid, label, p, kind, power in PRACTICALS:
    add(pid, 'Practicals', 'practical', p, p, label, 'practical', colour=kind, power=power)

STRUCT.append(dict(kind='pipe', name='FOH 1 — the bridge pipe', a=[14.95, BR_Y + 0.024, BR_Z], b=[24.85, BR_Y + 0.024, BR_Z], r=0.024))
for x in (15.3, 17.5, 20.0, 22.5, 24.6):          # clamped back to the bridge's rail (its face z -3.30, top 7.23)
    STRUCT.append(dict(kind='arm', name='FOH 1 rail clamp', a=[x, BR_Y + 0.024, BR_Z], b=[x, 7.20, -3.30], r=0.016))
STRUCT.append(dict(kind='pipe', name='FOH 2 pipe', a=[15.2, F2_Y + 0.024, F2_Z], b=[23.8, F2_Y + 0.024, F2_Z], r=0.024))
for x in (15.6, 19.5, 23.4):                       # dropped from the auditorium ceiling (y 8.05)
    STRUCT.append(dict(kind='drop', name='FOH 2 drop', a=[x, F2_Y + 0.024, F2_Z], b=[x, 8.05, F2_Z], r=0.012))
for n in (1, 2, 3, 4):
    nm = f'{"1st 2nd 3rd 4th".split()[n - 1]} Electric'
    STRUCT.append(dict(kind='pipe', name=nm + ' pipe', a=[13.8, EY[n] + 0.024, EZ[n]], b=[26.2, EY[n] + 0.024, EZ[n]], r=0.024))
    for x in (14.2, 18.0, 22.0, 25.8):             # its lift lines up to the grid under the fly roof (y 16.0)
        STRUCT.append(dict(kind='drop', name=nm + ' lift line', a=[x, EY[n] + 0.048, EZ[n]], b=[x, 15.9, EZ[n]], r=0.005))
STRUCT.append(dict(kind='boom', name='Doorway stand (backstage corridor)', a=[20.0, 0.80, 10.5], b=[20.0, 3.02, 10.5], r=0.022))
STRUCT.append(dict(kind='base', name='Doorway stand base', a=[20.0, 0.80, 10.5], b=[20.0, 0.83, 10.5], r=0.35))

# ---------------------------------------------------------------- the patch
U1_SYSTEMS_FIRST = ('FOH 1', 'FOH 2', 'Box', 'Pros', '1st', '2nd', '3rd', '4th', 'Floor', 'Backstage', "Theatre 2's")


def patch_order(u):
    t = u['type']
    if t in ('encore', 'aura', 'cyc', 'cyc-floor', 'hazer', 'practical') or u['position'].startswith(('SL boom', 'SR boom')):
        uni = 2
    else:
        uni = 1
    order = ['FOH 1', 'FOH 2', 'Box boom house right', 'Box boom house left', 'Pros boom house right', 'Pros boom house left',
             '1st', '2nd', '3rd', '4th', 'Floor', 'Backstage', "Theatre 2's", 'SL boom 1', 'SL boom 2', 'SL boom 3', 'SR boom 1',
             'SR boom 2', 'SR boom 3', 'Ground', 'SL wing', 'SR wing', 'Practicals']
    if uni == 2:      # universe 2: the booms, then the movers, the sky, the haze, the practicals
        grp = {'encore': 1, 'aura': 2, 'cyc': 3, 'cyc-floor': 4, 'hazer': 5, 'practical': 6}.get(t, 0)
    else:
        grp = 0
    pos_rank = next((k for k, o in enumerate(order) if u['position'].startswith(o)), 99)
    return (uni, grp, pos_rank, units.index(u))


addr = {1: 1, 2: 1}
for u in sorted(units, key=patch_order):
    uni = patch_order(u)[0]
    n = len(TYPES[u['type']]['chans'])
    u['universe'], u['address'], u['channels'] = uni, addr[uni], n
    addr[uni] += n
for uni in (1, 2):
    assert addr[uni] - 1 <= 512, f'universe {uni} needs {addr[uni] - 1} channels'
chan = 1
for u in sorted(units, key=lambda u: (u['universe'], u['address'])):
    u['channel'] = chan; chan += 1           # the desk's channel number (hookup), in patch order
for u in units:
    t = TYPES[u['type']]
    m, mo, mode = t['qlc']
    u['qlc'] = dict(manufacturer=m, model=mo, mode=mode, channels=len(t['chans']))
    u['glb'] = f"assets/fixtures/{t['glb']}.glb" if t['glb'] else None
    u['mover'] = list(t['mover']) if 'mover' in t else None
    u['floor'] = bool(t.get('floor'))

# ---------------------------------------------------------------- the looks
C = dict(  # the period palette (LIGHTING-NEEDS.md §4), sRGB hex
    straw='ffe9c2', daywhite='fff3e0', warm='ffcf96', amber='ffb066', candle='ff9a40', fire='ff6418', hearth='ff7a28',
    steel='5c80c4', moon='86a6e0', night='34508c', cool='dce8ff', north='e4ecff', grey='c9ccd2', flatgrey='d6d6d8',
    lav='c6bce0', dove='d2cde4', dawn='d8c6e0', dawnwarm='ffd0a0', sunset='ff8a34', sunlow='ffa050', rosy='ffb8c8',
    spring='eaffd8', winter='d6e4ff', sea='5cc4b4', leaf='d8f0a0', silver='eef4ff', red='ff4030', black='000000')


def look(front=(0, 'straw'), top=(0, 'straw'), back=(0, 'straw'), box=None, sideSL=(0, 'straw'), sideSR=(0, 'straw'),
         pros=None, sky=(0, 'night'), ground=None, areas=None, rows=None, long=(0, 'sunset'), specials=None, prac=None,
         movers=None, haze=0.3, follow=0, note=''):
    """a look by system → one entry per unit: [level 0..1, colour hex] (+ for movers aim stage xyz and gobo)"""
    areas = areas or {}
    rows = rows or {}
    box = box if box is not None else (front[0] * 0.6, front[1])
    pros = pros if pros is not None else (max(sideSL[0], sideSR[0]) * 0.7, sideSL[1] if sideSL[0] >= sideSR[0] else sideSR[1])
    ground = ground if ground is not None else (sky[0] * 0.8, sky[1])
    specials = specials or {}
    prac = prac or {}
    movers = movers or {}
    out = {}

    def am(a):
        return areas.get(a, areas.get('*', 1.0))

    def rm(r):
        if r in rows:
            return rows[r]
        return max(am(a) for a in ROWS[r]) if r in ROWS else 1.0

    for u in units:
        s, lv, col = u['system'], 0.0, 'black'
        if s in ('front', 'top', 'back', 'box'):
            lv, col = {'front': front, 'top': top, 'back': back, 'box': box}[s]
            lv *= am(u['area'])
        elif s in ('sideSL', 'sideSR'):
            lv, col = sideSL if s == 'sideSL' else sideSR
            lv *= rm(u['row'])
        elif s == 'pros':
            lv, col = pros
            lv *= rm('AP')
        elif s == 'long':
            lv, col = long
            lv *= rm(u['row'])
        elif s == 'sky':
            lv, col = sky
        elif s == 'ground':
            lv, col = ground
        elif s == 'special':
            sp = u['special']
            key = 'S27' if sp.startswith('S27') else sp
            if sp in specials:
                lv, col = specials[sp]
            elif key in specials:
                lv, col = specials[key]
        elif s == 'practical':
            if u['id'] in prac:
                lv, col = prac[u['id']]
            else:
                col = {'fire': 'fire', 'candle': 'candle', 'lantern': 'candle', 'twinkle': 'amber'}[u['colour']]
        elif s == 'follow':
            lv, col = (follow, 'daywhite') if u['id'] == 'FS-1' else (0, 'daywhite')
        elif s == 'haze':
            lv, col = haze, 'black'
        elif s in ('mvFOH', 'mv1', 'mv2', 'aura'):
            m = movers.get(u['id']) or movers.get(s)
            if m:
                e = [m[0] * 1.0, C.get(m[1], m[1])]
                e.append(m[2] if len(m) > 2 else None)       # aim, stage xyz
                e.append(m[3] if len(m) > 3 else u['gobo'])  # gobo
                out[u['id']] = e
                continue
            out[u['id']] = [0, C['black'], None, u['gobo']]
            continue
        out[u['id']] = [round(min(1.0, lv), 3), C.get(col, col)]
    return dict(note=note, units=out)


Z = dict  # area multipliers
INT_DIM_US = {'SHOP': 0.7, 'LOFT': 0.8}
water = lambda c, lv=0.7: {'mvFOH': (lv, c, None, 'water')}
LOOKS = {
    'interior-dawn-warm': look(front=(0.35, 'warm'), top=(0.25, 'warm'), back=(0.35, 'dawn'), sideSL=(0.7, 'amber'), sideSR=(0.25, 'cool'),
                               sky=(0.25, 'dawn'), areas=Z({'*': 0.5, 'LOFT': 1.0, 'SHOP': 0.8, 'MSL': 0.8, 'APR': 0.1, 'APC': 0.1, 'APL': 0.1}),
                               specials={'S11': (0.6, 'warm')}, haze=0.25, note='low amber-straw from the hearth side, the loft first'),
    'interior-morning-warm': look(front=(0.6, 'warm'), top=(0.45, 'straw'), back=(0.4, 'straw'), sideSL=(0.6, 'amber'), sideSR=(0.35, 'cool'),
                                  sky=(0.35, 'straw'), areas=Z({'*': 1.0, 'APR': 0.3, 'APC': 0.3, 'APL': 0.3}), note='the kitchen at breakfast'),
    'exterior-morning-bright': look(front=(0.9, 'daywhite'), top=(0.7, 'straw'), back=(0.6, 'straw'), sideSL=(0.6, 'straw'), sideSR=(0.6, 'straw'),
                                    sky=(0.7, 'cool'), areas=Z({'*': 0.45, 'APR': 1, 'APC': 1, 'APL': 1, 'DSR': 1, 'DSC': 1, 'DSL': 1}),
                                    note='full bright straw-white on the apron, the kitchen held behind'),
    'interior-day-warm': look(front=(0.65, 'warm'), top=(0.5, 'straw'), back=(0.45, 'straw'), sideSL=(0.3, 'warm'), sideSR=(0.75, 'straw'),
                              sky=(0.3, 'straw'), areas=Z({'*': 1.0, 'APR': 0.4, 'APC': 0.4, 'APL': 0.4}), note='warm interior daylight, a window from SR'),
    'interior-afternoon-firelit': look(front=(0.35, 'warm'), top=(0.25, 'amber'), back=(0.35, 'amber'), sideSL=(0.75, 'hearth'), sideSR=(0.15, 'cool'),
                                       sky=(0.15, 'amber'), areas=Z({'*': 0.6, 'SHOP': 1, 'MSL': 1, 'DSL': 0.8, 'APR': 0.2, 'APC': 0.2, 'APL': 0.2}),
                                       specials={'S8': (0.8, 'hearth')}, prac={'P-01': (0.8, 'fire')}, note='furnace orange dominant'),
    'dawn-interior-firelit': look(front=(0.25, 'dawn'), top=(0.15, 'dawn'), back=(0.35, 'grey'), sideSL=(0.6, 'hearth'), sideSR=(0.5, 'dawn'),
                                  sky=(0.3, 'dawn'), long=(0.4, 'dawn'), areas=Z({'*': 0.5, 'SHOP': 1, 'MSL': 1, 'APR': 0.1, 'APC': 0.1, 'APL': 0.1}),
                                  specials={'S8': (1.0, 'hearth'), 'S9': (0.0, 'fire')}, prac={'P-01': (1.0, 'fire')}, haze=0.45,
                                  note='half light, the furnace roaring; low grey-blue dawn from SR (S9 snaps up on the pour, S10 closes it down)'),
    'interior-day-grey': look(front=(0.5, 'grey'), top=(0.45, 'flatgrey'), back=(0.3, 'grey'), sideSL=(0.3, 'grey'), sideSR=(0.35, 'cool'),
                              sky=(0.25, 'grey'), areas=Z({'*': 1.0, 'APR': 0.3, 'APC': 0.3, 'APL': 0.3}), note='the kitchen desaturated, flat, cooler'),
    'exterior-day-street': look(front=(0.9, 'daywhite'), top=(0.8, 'straw'), back=(0.7, 'warm'), sideSL=(0.6, 'straw'), sideSR=(0.6, 'straw'),
                                sky=(0.75, 'cool'), specials={'S27': (0.0, 'daywhite')}, note='hard bright straw-white, a slightly warm back (the shop-door slices are the S27 cues)'),
    'exterior-day-sun': look(front=(0.85, 'daywhite'), top=(0.8, 'straw'), back=(0.7, 'warm'), sideSL=(0.55, 'straw'), sideSR=(0.65, 'straw'),
                             sky=(0.8, 'cool'), note='hard bright sun'),
    'exterior-day-bright': look(front=(0.95, 'daywhite'), top=(0.85, 'straw'), back=(0.7, 'warm'), sideSL=(0.7, 'straw'), sideSR=(0.7, 'straw'),
                                sky=(0.85, 'cool'), note='full day'),
    'interior-evening-bright': look(front=(0.75, 'north'), top=(0.6, 'cool'), back=(0.4, 'cool'), sideSL=(0.45, 'cool'), sideSR=(0.45, 'north'),
                                    sky=(0.3, 'steel'), areas=Z({'*': 1.0, 'APR': 0.35, 'APC': 0.35, 'APL': 0.35}), note="crisp cool white: Revere's shop is better lit"),
    'exterior-dusk-apron': look(front=(0.5, 'amber'), back=(0.4, 'amber'), sideSL=(0.0, 'amber'), sideSR=(0.0, 'amber'), sky=(0.3, 'night'),
                                areas=Z({'*': 0.0, 'APR': 1, 'APC': 0.6, 'APL': 0.3}), follow=0.7, specials={'S1': (0.4, 'warm')},
                                note='a travelling pool, amber, the rest dark (the followspot walks him home)'),
    'interior-day-cool': look(front=(0.7, 'north'), top=(0.55, 'cool'), back=(0.45, 'cool'), sideSL=(0.35, 'north'), sideSR=(0.55, 'north'),
                              sky=(0.35, 'cool'), areas=Z({'*': 1.0, 'APR': 0.4, 'APC': 0.4, 'APL': 0.4}), note='cool northern daylight'),
    'dawn-exterior-cold': look(front=(0.25, 'dawn'), top=(0.2, 'lav'), back=(0.4, 'lav'), sideSL=(0.1, 'lav'), sideSR=(0.5, 'dawn'), long=(0.6, 'dawn'),
                               sky=(0.45, 'lav'), ground=(0.6, 'dawnwarm'), specials={'S7': (0.8, 'silver')}, haze=0.45,
                               note='grey-lavender, low from SR, long shadows; the cup at the gravestone'),
    'interior-night-candle': look(front=(0.3, 'candle'), top=(0.25, 'candle'), back=(0.2, 'night'), sideSL=(0.25, 'amber'), sideSR=(0.2, 'amber'),
                                  sky=(0.1, 'night'), areas=Z({'*': 0.7, 'MSC': 1.0, 'APR': 0.15, 'APC': 0.15, 'APL': 0.15}),
                                  prac={'P-05': (0.8, 'candle'), 'P-06': (0.8, 'candle'), 'P-07': (0.8, 'candle'), 'P-08': (0.7, 'candle')},
                                  note='candle amber, pools on tables, deep shadows'),
    'night-interior-candle': look(front=(0.25, 'candle'), top=(0.2, 'candle'), back=(0.3, 'night'), sideSL=(0.25, 'amber'), sideSR=(0.2, 'steel'),
                                  sky=(0.1, 'night'), areas=Z({'*': 0.35, 'LOFT': 1.0, 'MSC': 0.6}),
                                  prac={'P-05': (0.6, 'candle'), 'P-09': (0.8, 'candle')}, haze=0.4,
                                  note='the loft over the Observer by candle, the street below in the dark'),
    'night-interior-lamp': look(front=(0.3, 'candle'), top=(0.25, 'candle'), back=(0.25, 'night'), sideSL=(0.2, 'amber'), sideSR=(0.15, 'steel'),
                                sky=(0.08, 'night'), areas=Z({'*': 0.3, 'MSC': 1, 'MSR': 1, 'DSC': 0.8}), prac={'P-09': (0.8, 'candle')},
                                note='the surgery again: midnight by the lamp, then the dark before dawn at Lexington'),
    'interior-morning-barred': look(front=(0.15, 'cool'), top=(0.1, 'cool'), back=(0.2, 'steel'), sideSL=(0.1, 'cool'), sideSR=(0.1, 'cool'),
                                    sky=(0.1, 'steel'), areas=Z({'*': 0.4, 'DSL': 1, 'MSL': 1}), specials={'S15': (1.0, 'cool')}, haze=0.5,
                                    note='a cool shaft through bars, the room dim'),
    'interior-day-court': look(front=(0.85, 'north'), top=(0.7, 'flatgrey'), back=(0.45, 'cool'), sideSL=(0.45, 'north'), sideSR=(0.45, 'north'),
                               sky=(0.4, 'cool'), specials={'S6': (0.9, 'silver')}, note='bright, slightly cold, flat; the four cups on the table'),
    'exterior-day-warm': look(front=(0.85, 'straw'), top=(0.75, 'warm'), back=(0.7, 'amber'), sideSL=(0.6, 'warm'), sideSR=(0.6, 'warm'),
                              sky=(0.75, 'straw'), note='warm open yard'),
    'night-interior-dark-crowd': look(front=(0.12, 'candle'), top=(0.0, 'night'), back=(0.25, 'night'), sideSL=(0.2, 'steel'), sideSR=(0.2, 'steel'),
                                      sky=(0.05, 'night'), prac={'P-02': (0.9, 'candle')}, haze=0.5, note='near-dark, one lantern, faces only'),
    'night-exterior-harbour': look(front=(0.25, 'steel'), top=(0.2, 'night'), back=(0.5, 'moon'), sideSL=(0.3, 'steel'), sideSR=(0.3, 'steel'),
                                   sky=(0.4, 'night'), movers={**water('steel', 0.8), 'mv2': (0.6, 'moon', None, 'moon')},
                                   prac={'P-02': (0.8, 'candle')}, haze=0.5, note='steel blue moonlight, water ripple on the apron, a lantern'),
    'exterior-day-overcast': look(front=(0.75, 'flatgrey'), top=(0.7, 'flatgrey'), back=(0.4, 'grey'), sideSL=(0.3, 'grey'), sideSR=(0.3, 'grey'),
                                  sky=(0.6, 'grey'), movers=water('sea', 0.35), note='flat grey-white, no shadows (the closed port)'),
    'interior-day-dovegrey': look(front=(0.65, 'dove'), top=(0.5, 'lav'), back=(0.45, 'silver'), sideSL=(0.4, 'dove'), sideSR=(0.45, 'silver'),
                                  sky=(0.3, 'lav'), areas=Z({'*': 1.0, 'APR': 0.4, 'APC': 0.4, 'APL': 0.4}), note="lavender-grey and silver: the Lytes' drawing room"),
    'night-exterior-torch': look(front=(0.25, 'steel'), top=(0.15, 'night'), back=(0.4, 'moon'), sideSL=(0.5, 'fire'), sideSR=(0.3, 'steel'),
                                 sky=(0.3, 'night'), prac={'P-10': (1.0, 'fire')}, haze=0.5, note='flickering orange against blue night'),
    'night-exterior-moon': look(front=(0.22, 'steel'), top=(0.15, 'night'), back=(0.55, 'moon'), sideSL=(0.3, 'steel'), sideSR=(0.25, 'steel'),
                                sky=(0.45, 'night'), movers={'mv2': (0.75, 'moon', None, 'moon')}, haze=0.5,
                                note='steel blue, moon breakup from high and behind; faces just readable'),
    'night-interior-moonlit': look(front=(0.15, 'steel'), top=(0.1, 'night'), back=(0.4, 'moon'), sideSL=(0.15, 'steel'), sideSR=(0.2, 'steel'),
                                   sky=(0.2, 'night'), areas=Z({'*': 0.6, 'LOFT': 1.0}), movers={'mv2': (0.45, 'moon', [-2.4, 2.4, 5.0], 'moon')},
                                   haze=0.45, note='the truckle beds, later: moonlight through the loft'),
    'night-interior-lantern': look(front=(0.05, 'candle'), back=(0.12, 'night'), sky=(0.04, 'night'),
                                   specials={'S24a': (0.7, 'candle'), 'S24b': (0.7, 'candle'), 'S24c': (0.7, 'candle')}, prac={'P-02': (1.0, 'candle')},
                                   follow=0.35, haze=0.45, note='darkness, the lantern moving, the three reveals'),
    'night-interior-hearth': look(front=(0.08, 'candle'), sideSL=(0.45, 'hearth'), sky=(0.0, 'night'), areas=Z({'*': 0.3, 'SHOP': 1}),
                                  specials={'S8': (1.0, 'hearth')}, prac={'P-01': (0.9, 'fire')}, haze=0.4, note='the hearth glow only, then the shutters'),
    'dawn-exterior-warm': look(front=(0.45, 'dawnwarm'), top=(0.25, 'lav'), back=(0.5, 'lav'), sideSL=(0.1, 'lav'), sideSR=(0.8, 'dawnwarm'),
                               long=(0.8, 'dawnwarm'), sky=(0.55, 'dawn'), ground=(0.8, 'dawnwarm'), haze=0.4, note='low warm cross-light from SR over a cool floor'),
    'exterior-afternoon-dappled': look(front=(0.55, 'warm'), top=(0.3, 'leaf'), back=(0.6, 'sunlow'), sideSL=(0.3, 'warm'), sideSR=(0.7, 'sunlow'),
                                       sky=(0.6, 'straw'), movers={'mv1': (0.8, 'leaf', None, 'leaves'), **water('sea', 0.45)}, haze=0.35,
                                       note='warm low sun through leaves + a blue-green shimmer downstage'),
    'interior-day-loft': look(front=(0.2, 'warm'), top=(0.15, 'warm'), back=(0.2, 'straw'), sideSL=(0.15, 'warm'), sideSR=(0.2, 'warm'),
                              sky=(0.2, 'straw'), areas=Z({'*': 0.35, 'LOFT': 1.0}), specials={'S11': (0.9, 'warm')}, haze=0.35,
                              note='a warm shaft into the loft, the rest dim'),
    'exterior-day-winter': look(front=(0.75, 'winter'), top=(0.6, 'winter'), back=(0.5, 'cool'), sideSL=(0.45, 'winter'), sideSR=(0.45, 'winter'),
                                sky=(0.7, 'winter'), note='pale blue-white, thin'),
    'exterior-day-spring': look(front=(0.9, 'daywhite'), top=(0.75, 'spring'), back=(0.6, 'straw'), sideSL=(0.55, 'spring'), sideSR=(0.6, 'straw'),
                                sky=(0.8, 'spring'), note='clean bright, a touch green'),
    'exterior-day-chase': look(front=(0.8, 'daywhite'), top=(0.7, 'straw'), back=(0.6, 'warm'), sideSL=(0.75, 'straw'), sideSR=(0.75, 'straw'),
                               sky=(0.8, 'spring'), movers={'mv1': (1.0, 'daywhite', None, 'none'), 'mv2': (1.0, 'warm', None, 'none'), 'aura': (0.8, 'straw')},
                               prac={'P-12': (0.7, 'fire')}, haze=0.4,
                               note='bright and fast-moving: the movers chase the horse round (S29), then the snap to one pool at the gate'),
    'exterior-dawn-grey': look(front=(0.35, 'grey'), top=(0.2, 'lav'), back=(0.45, 'grey'), sideSL=(0.15, 'grey'), sideSR=(0.4, 'dawn'), long=(0.4, 'grey'),
                               sky=(0.45, 'grey'), specials={'S28': (0.0, 'silver')}, haze=0.5,
                               note='grey, cold, low; then the isolation (the volley flash and S28 are the cues)'),
    'interior-day-stable': look(front=(0.55, 'warm'), top=(0.35, 'amber'), back=(0.5, 'amber'), sideSL=(0.3, 'warm'), sideSR=(0.65, 'sunlow'),
                                sky=(0.3, 'straw'), haze=0.45, note='warm shafts'),
    'interior-night-lamp': look(front=(0.35, 'candle'), top=(0.3, 'candle'), back=(0.15, 'night'), sideSL=(0.25, 'amber'), sideSR=(0.15, 'amber'),
                                sky=(0.05, 'night'), areas=Z({'*': 0.3, 'MSC': 1, 'MSR': 1, 'DSC': 0.8}), prac={'P-09': (0.8, 'candle')},
                                note="Warren's surgery by lamplight"),
    'interior-night-warm': look(front=(0.55, 'amber'), top=(0.45, 'candle'), back=(0.25, 'night'), sideSL=(0.4, 'amber'), sideSR=(0.35, 'amber'),
                                sky=(0.1, 'night'), areas=Z({'*': 1.0, 'APR': 0.3, 'APC': 0.3, 'APL': 0.3}), prac={'P-05': (0.7, 'candle'), 'P-06': (0.7, 'candle')},
                                note='the Dawes kitchen: warm and comic'),
    'dawn-interior-cold': look(front=(0.35, 'dawn'), top=(0.2, 'lav'), back=(0.3, 'grey'), sideSL=(0.55, 'cool'), sideSR=(0.15, 'grey'),
                               sky=(0.35, 'dawn'), specials={'S16': (0.8, 'cool')}, haze=0.45, note='first daylight, cold; the window light'),
    'exterior-afternoon-flat': look(front=(0.7, 'flatgrey'), top=(0.6, 'straw'), back=(0.4, 'grey'), sideSL=(0.35, 'straw'), sideSR=(0.35, 'straw'),
                                    sky=(0.55, 'grey'), note='flat light, feathers in the air'),
    'exterior-sunset-distant': look(front=(0.15, 'amber'), top=(0.05, 'night'), back=(0.3, 'night'), sideSL=(0.05, 'night'), sideSR=(0.35, 'sunset'),
                                    long=(0.35, 'sunset'), sky=(0.75, 'sunset'), ground=(0.9, 'sunset'), prac={'P-13': (0.8, 'amber'), 'P-14': (0.8, 'amber')},
                                    haze=0.4, note='the last of a sunset low on the back wall, the stage dim, far twinkles'),
    'night-interior-warm': look(front=(0.35, 'amber'), top=(0.25, 'candle'), back=(0.15, 'night'), sideSL=(0.2, 'amber'), sideSR=(0.2, 'amber'),
                                sky=(0.05, 'night'), areas=Z({'*': 0.8, 'APR': 0.2, 'APC': 0.2, 'APL': 0.2}),
                                specials={'S14': (0.8, 'warm')}, prac={'P-05': (0.5, 'candle')}, haze=0.45,
                                note="a low warm kitchen; the doorway's backlight beyond"),
    'exterior-morning-cold': look(front=(0.75, 'cool'), top=(0.55, 'winter'), back=(0.6, 'cool'), sideSL=(0.2, 'cool'), sideSR=(0.8, 'daywhite'),
                                  long=(0.6, 'daywhite'), sky=(0.7, 'winter'), note='bright cold morning, long shadows'),
    'exterior-afternoon-leaves': look(front=(0.6, 'warm'), top=(0.35, 'leaf'), back=(0.6, 'sunlow'), sideSL=(0.25, 'warm'), sideSR=(0.75, 'sunlow'),
                                      long=(0.5, 'sunlow'), sky=(0.65, 'straw'), movers={'mv1': (0.8, 'leaf', None, 'leaves')}, haze=0.35,
                                      note='low warm afternoon through new leaves'),
    'interior-afternoon-window': look(front=(0.3, 'warm'), top=(0.2, 'warm'), back=(0.2, 'straw'), sideSL=(0.45, 'sunlow'), sideSR=(0.1, 'warm'),
                                      sky=(0.25, 'straw'), areas=Z({'*': 0.6, 'MSL': 1, 'DSL': 1, 'MSC': 1}), specials={'S16': (0.9, 'sunlow')}, haze=0.35,
                                      note='window light in a quiet room'),
    'interior-day-empty': look(front=(0.75, 'daywhite'), top=(0.55, 'straw'), back=(0.4, 'straw'), sideSL=(0.4, 'straw'), sideSR=(0.4, 'straw'),
                               sky=(0.5, 'straw'), note='clear, bright, empty'),
    'exterior-sunset-long': look(front=(0.2, 'amber'), top=(0.0, 'amber'), back=(0.45, 'sunset'), sideSL=(0.0, 'amber'), sideSR=(0.9, 'sunset'),
                                 long=(1.0, 'sunset'), sky=(0.85, 'sunset'), ground=(1.0, 'sunset'), movers={'aura': (0.5, 'sunset')}, haze=0.45,
                                 note='the finale: a long low amber raking light from the side, long shadows across the bare set'),
}

# per segment: what the scene adds to its look tag (practicals, specials, the followspot), keyed "scene.segment"
EXTRAS = {
    '1.1': dict(follow=0.8, specials={'S11': (0.8, 'warm')}, note='Johnny down the aisle (S3), the loft isolates'),
    '1.2': dict(specials={'S1': (0.5, 'straw')}),
    '4.1': dict(specials={'S4': (1.0, 'silver')}, movers={'mvFOH': (0.7, 'steel', None, 'water')}, prac={'P-02': (0.8, 'candle')}),
    '5.2': dict(follow=0.7),
    '6.2': dict(specials={'S9': (0.0, 'fire'), 'S10': (0.0, 'hearth')}, note='S9 snaps up on the pour, S10 closes down to the bucket'),
    '10.3': dict(specials={'S5': (0.9, 'silver'), 'S13': (0.6, 'rosy')}),
    '11.1': dict(),
    '11.2': dict(prac={'P-09': (0.7, 'candle')}, specials={'S14b': (0.5, 'warm')}),
    '13.1': dict(specials={'S11': (0.8, 'candle')}),
    '13.3': dict(movers={'mvFOH': (0.8, 'steel', None, 'water')}),
    '14.1': dict(movers={'mvFOH': (0.5, 'sea', None, 'water')}),
    '15.1': dict(specials={'S32': (0.8, 'daywhite')}, note='the sheet, backlit'),
    '17.1': dict(prac={'P-10': (1.0, 'fire')}),
    '17.2': dict(follow=0.5),
    '17.3': dict(specials={'S5': (0.8, 'silver')}, prac={'P-11': (0.7, 'candle')}),
    '17.4': dict(follow=0.35),
    '17.5': dict(prac={'P-01': (0.9, 'fire')}),
    '18.1': dict(),
    '19.1': dict(specials={'S11': (0.7, 'candle'), 'S12': (0.0, 'cool')}, note='S12 finds Otis\'s hands on the rafters (a cue)'),
    '20.1': dict(prac={'P-09': (0.8, 'candle')}),
    '20.5': dict(prac={'P-12': (0.8, 'fire')}),
    '20.7': dict(specials={'S28': (0.0, 'silver'), 'S28f': (0.0, 'daywhite')}, note='the volley flash (S28f) and the eyes (S28) are cues'),
    '21.2': dict(specials={'S14': (0.5, 'straw')}),
    '21.5': dict(specials={'S22': (0.9, 'candle')}, prac={'P-03': (1.0, 'candle'), 'P-04': (1.0, 'candle'), 'P-13': (0.6, 'amber')},
                 note='one if by land: the two church lanterns, the pin; Charlestown\'s lights'),
    '22.1': dict(),
    '22.4': dict(),
    '23.1': dict(),
    '24.1': dict(movers={'mvFOH': (0.6, 'candle', [0.0, 0.4, -2.4], 'water')}, prac={'P-10': (1.0, 'fire')}, note='the boats from the house (S31)'),
    '24.2': dict(prac={'P-13': (0.6, 'amber'), 'P-14': (0.6, 'amber')}),
    '25.2': dict(prac={'P-09': (0.6, 'candle')}),
    '26.2': dict(specials={'S33': (0.6, 'cool')}),
    '26.3': dict(follow=0.0),
}

# ---------------------------------------------------------------- write it
setdata = json.load(open(SET, encoding='utf-8'))
segments = []
for s in setdata['scenes']:
    for g in s['segments']:
        lit = s.get('furnace') == 'lit' and (not s.get('furnaceLitSegments') or g['seg'] in s['furnaceLitSegments'])
        segments.append(dict(scene=s['n'], seg=g['seg'], title=s['title'], location=g['location'], look=g['look'], furnace=lit,
                             extras=f"{s['n']}.{g['seg']}" if f"{s['n']}.{g['seg']}" in EXTRAS else None))
tags = sorted({g['look'] for g in segments})


def resolve_extra(e):
    """an EXTRAS entry → {note, units: {id: entry}} — only the units it names (by special, practical, mover system or id)"""
    res = {}
    for u in units:
        s = u['system']
        if s == 'special':
            sp = u['special']
            v = (e.get('specials') or {}).get(sp) or (e.get('specials') or {}).get('S27' if sp.startswith('S27') else sp)
            if v:
                res[u['id']] = [round(v[0], 3), C.get(v[1], v[1])]
        elif s == 'practical' and u['id'] in (e.get('prac') or {}):
            v = e['prac'][u['id']]
            res[u['id']] = [round(v[0], 3), C.get(v[1], v[1])]
        elif s in ('mvFOH', 'mv1', 'mv2', 'aura'):
            m = (e.get('movers') or {}).get(u['id']) or (e.get('movers') or {}).get(s)
            if m:
                res[u['id']] = [m[0], C.get(m[1], m[1]), m[2] if len(m) > 2 else None, m[3] if len(m) > 3 else u['gobo']]
        elif s == 'follow' and 'follow' in e and u['id'] == 'FS-1':
            res[u['id']] = [e['follow'], C['daywhite']]
    return dict(note=e.get('note', ''), units=res)


for g in segments:          # a lit furnace adds its glow and the face light, whatever the look
    if g['furnace']:
        k = f"{g['scene']}.{g['seg']}"
        e = EXTRAS.setdefault(k, {})
        e.setdefault('prac', {}).setdefault('P-01', (0.9, 'fire'))
        e.setdefault('specials', {}).setdefault('S8', (0.8, 'hearth'))
        g['extras'] = k
missing = [t for t in tags if t not in LOOKS]
assert not missing, f'looks with no recipe: {missing}'
for k in EXTRAS:
    assert any(f"{g['scene']}.{g['seg']}" == k for g in segments), f'extras for a segment that does not exist: {k}'

out = dict(
    format='johnny-tremain-rig/1',
    about='The lighting rig for Johnny Tremain in Theatre 2 (tools/jt-rig.py writes this file; docs/johnny-tremain/LIGHT-PLOT.md is the plot). '
          'pos = the hang point (top of the clamp; for a floor unit the floor under it) and aim = the focus point, both WORLD metres '
          '(stage → world: x + 20.00, y + 0.80, z + 2.30). A look entry per unit is [level 0..1, colour hex] and, for a mover, '
          '[level, colour, aim (stage x, y, z) or null for its rest focus, gobo]. Universes and addresses are 1-based (as a desk shows them).',
    frame=dict(world='stage + (20.00, 0.80, 2.30)', stageRight='+x', upstage='+z'),
    types={k: dict(name=v['name'], glb=(f"assets/fixtures/{v['glb']}.glb" if v['glb'] else None), field=v['field'], power=v['power'],
                   qlc=dict(manufacturer=v['qlc'][0], model=v['qlc'][1], mode=v['qlc'][2], channels=len(v['chans'])), channelNames=v['chans'],
                   mover=list(v['mover']) if 'mover' in v else None) for k, v in TYPES.items()},
    palette={k: v for k, v in C.items()},
    areas={k: dict(x=v[0], z=v[1], floor=v[2]) for k, v in AREAS.items()},
    units=units,
    looks={t: LOOKS[t] for t in tags},
    extras={k: resolve_extra(v) for k, v in sorted(EXTRAS.items(), key=lambda kv: [int(n) for n in kv[0].split('.')])},
    segments=segments,
    universes={str(u): addr[u] - 1 for u in (1, 2)},
    structures=STRUCT,
)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(out, f, indent=1, ensure_ascii=False)
    f.write('\n')
by = {}
for u in units:
    by[u['type']] = by.get(u['type'], 0) + 1
print(f'jt-rig: {len(units)} units ({", ".join(f"{n} {t}" for t, n in sorted(by.items()))}); universe 1 {addr[1] - 1} ch, universe 2 {addr[2] - 1} ch; '
      f'{len(tags)} looks, {len(EXTRAS)} segment extras, {len(segments)} segments → {os.path.relpath(OUT, ROOT)}')

# ---------------------------------------------------------------- the plot, written from the same data
PLOT = os.path.join(ROOT, 'docs', 'johnny-tremain', 'LIGHT-PLOT.md')
f3 = lambda v: f'{v:.2f}'
st = lambda p: f'{p[0] - 20:+.2f}, {p[1] - 0.80:.2f}, {p[2] - 2.30:+.2f}'
L = []
w = L.append
w('# Johnny Tremain — the light plot (Theatre 2)\n')
w('Written by `tools/jt-rig.py` from the same data as `assets/johnny-tremain/rig.json` — edit the script, not this file. '
  'The QLC+ workspace is `assets/johnny-tremain/qlc/johnny-tremain.qxw` (`tools/jt-qlc.py`; how to open it: '
  '[`assets/johnny-tremain/qlc/README.md`](../../assets/johnny-tremain/qlc/README.md)). The brief is '
  '[LIGHTING-NEEDS.md](LIGHTING-NEEDS.md). In the page: the **T2 rig** header button, or `MIDTOWN.jtLights`.\n')
w('World metres (stage → world: x + 20.00, y + 0.80, z + 2.30). "Stage" columns are the stage frame: +x stage right, '
  'z upstage of the proscenium plane, y over the deck. Units are numbered stage left → stage right (low x first), '
  'booms bottom → top.\n')
by = {}
for u in units:
    by[u['type']] = by.get(u['type'], 0) + 1
w('## The rig in numbers\n')
w('| fixture | QLC+ definition (manufacturer / model / mode) | ch | units |')
w('|---|---|---|---|')
for k, n in sorted(by.items(), key=lambda kv: -kv[1]):
    t = TYPES[k]
    w(f"| {t['name']} | {' / '.join(t['qlc'])} | {len(t['chans'])} | {n} |")
w(f"\n**{len(units)} units** ({len(units) - by.get('practical', 0)} instruments, {by.get('practical', 0)} practicals); "
  f"universe 1 uses {addr[1] - 1} channels, universe 2 {addr[2] - 1}. Every definition ships with QLC+ (checked against "
  "the library's own .qxf files) or is a Generic dimmer: **no custom fixture files are needed.**\n")
w('## Positions\n')
w('| position | where (world) | units | what hangs there |')
w('|---|---|---|---|')
positions = {}
for u in units:
    positions.setdefault(u['position'], []).append(u)
for p, us in positions.items():
    xs = [u['pos'][0] for u in us]; ys = [u['pos'][1] for u in us]; zs = [u['pos'][2] for u in us]
    rng = lambda a: f3(min(a)) if max(a) - min(a) < 0.01 else f'{f3(min(a))}…{f3(max(a))}'
    kinds = {}
    for u in us:
        kinds[TYPES[u['type']]['name']] = kinds.get(TYPES[u['type']]['name'], 0) + 1
    w(f"| {p} | x {rng(xs)}, y {rng(ys)}, z {rng(zs)} | {len(us)} | {', '.join(f'{n} × {k}' for k, n in kinds.items())} |")
w("\nThe electrics hang on cross-stage pipes x 13.8…26.2 at 8.5 (1st, 2nd), 10.1 (3rd) and 11.6 (4th): over the venue's iron "
  "(5.9–6.2) and high enough that the front row does not see them through the arch, under the header or over the masking "
  "border (`MIDTOWN.jtLights.check()` proves it from six seats). No unit hangs over the iron's centre walkway (x 19.2…21.1). "
  "Nothing stands in either lift's travel (front x 17…23, z 2.6…5.0; back x 17.5…22.5, z 5.9…8.3; y −4.4…5.2).\n")
w('## Patch sheet (address order)\n')
w('| U | address | ch | unit | position | fixture | mode | purpose | colour |')
w('|---|---|---|---|---|---|---|---|---|')
for u in sorted(units, key=lambda u: (u['universe'], u['address'])):
    w(f"| {u['universe']} | {u['address']}–{u['address'] + u['channels'] - 1} | {u['channel']} | {u['id']} | {u['position']} | "
      f"{TYPES[u['type']]['name']} | {TYPES[u['type']]['qlc'][2]} | {u['purpose']} | {u['colour']} |")
w('\n"ch" is the desk channel (one per unit, in patch order) the hookup below uses.\n')
w('## Hookup: the area systems\n')
w('| area | centre (stage x, z) | front | box (side-front) | top | back |')
w('|---|---|---|---|---|---|')
for a, (x, z, fl) in AREAS.items():
    cell = lambda s: ', '.join(f"{u['id']} (ch {u['channel']})" for u in units if u['system'] == s and u['area'] == a) or '—'
    w(f'| {a} | {x:+.2f}, {z:+.2f}{" (floor " + str(fl) + ")" if fl else ""} | {cell("front")} | {cell("box")} | {cell("top")} | {cell("back")} |')
w('\n| system | units |')
w('|---|---|')
for s, label in (('sideSL', 'side light from SL (booms)'), ('sideSR', 'side light from SR (booms)'), ('pros', 'pros booms (apron side)'),
                 ('long', 'long low light from SR (dawn, sunset)'), ('sky', 'the back brick from above'), ('ground', 'the ground row'),
                 ('mvFOH', 'movers: water (bridge)'), ('mv1', 'movers: leaves / ride (1st)'), ('mv2', 'movers: moon / ride (2nd)'),
                 ('aura', 'wash movers (4th)'), ('follow', 'followspots'), ('haze', 'haze')):
    w(f"| {label} | {', '.join(u['id'] + ' (ch ' + str(u['channel']) + ')' for u in units if u['system'] == s)} |")
w('\n## Specials\n')
w('| special | unit | ch | from | focus (stage x, y, z) | field ° | gobo |')
w('|---|---|---|---|---|---|---|')
for u in sorted([u for u in units if u['special']], key=lambda u: (int(''.join(c for c in u['special'][1:] if c.isdigit()) or 0), u['special'])):
    w(f"| {u['special']} {u['purpose']} | {u['id']} | {u['channel']} | {u['position']} | {st(u['aim'])} | {u['field']} | {u['gobo'] or '—'} |")
w('\n## Practicals (each its own dimmer)\n')
w('| unit | ch | U / address | what | where (stage x, y, z) |')
w('|---|---|---|---|---|')
for u in units:
    if u['type'] == 'practical':
        w(f"| {u['id']} | {u['channel']} | {u['universe']} / {u['address']} | {u['purpose']} | {st(u['pos'])} |")
w('\n## Looks\n')
w(f"{len(tags)} looks, one per tag set.json's segments use, and {len(EXTRAS)} segments that add to theirs (a lit furnace, candles, "
  'lanterns, a special). In QLC+ each look is a Scene ("Look: <tag>"), each segment with extras a Scene ("Seg n.s …"), and the '
  f'chaser "Johnny Tremain" has one step per segment in show order ({len(segments)}), 2 s fades, held until GO.\n')
w('| tag | the look |')
w('|---|---|')
for t in tags:
    w(f"| `{t}` | {LOOKS[t]['note']} |")
w("\n## Decisions left (Jack's)\n")
w("- The 3rd and 4th electrics hang at 10.1 and 11.6 because the masking border (0.6 m deep at 4.4 over the deck) lets the "
  "front row see over it; a deeper border (or a second one at stage z ~4.5) would let them come down to ~8.5.\n"
  "- The movers' pan/tilt values in the QLC+ scenes assume each mover hung with its front to the house — touch up the focus "
  "on the day (QLC+'s Position tool); the Encore gobo slots (water 1, leaves 2, moon 3, window 4) stand in for the real wheel.\n"
  "- The followspots are on dimmer channels (D'Artagnan 934SNX) so the desk can fade them; the operators aim them.\n"
  "- The practicals' circuits (radio dimmers for the hand lantern and the steeple, a DMX LED for the furnace) are the "
  "production electrician's; the channels are reserved.\n")
os.makedirs(os.path.dirname(PLOT), exist_ok=True)
with open(PLOT, 'w', encoding='utf-8', newline='\n') as f:
    f.write('\n'.join(L) + '\n')
print(f'jt-rig: the plot → {os.path.relpath(PLOT, ROOT)}')
