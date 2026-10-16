#!/usr/bin/env python3
"""The ground plan's checker for Johnny Tremain on Theatre 2 (assets/johnny-tremain/set.json).

Standard library only.  `python tools/jt-set-check.py` prints PASS/FAIL lines and exits non-zero on any FAIL.
`--verbose` adds the sightline table and every transition's lift moves.

What it checks (docs/johnny-tremain/set-format.md, "Rules the plan keeps", and CONTRACT.md's lifts, RULING GI):
  1. overlaps    no two non-hand pieces on in one segment overlap (oriented footprints AND their heights), the unit set
                 included; a platform (loft, wharf, step, judge's platform) carries what stands on it, the loft's
                 under-space (to 2.30) is free, the rafters are an open frame, the furnace's chimney goes through the loft
  2. support     a piece whose base is over the deck stands on a platform that is on, inside its footprint
  3. heights     nothing unflown stands taller than 4.40 over the deck; flown pieces fit their lanes and hide at out-trim
  4. deck        every on piece stands on the deck (wings, the opening, the apron; not in the SR side room)
  5. storage     the pieces parked in one wing never overlap while parked together; each sits inside its park; a
                 backstage piece passes the centre doors (2.0 wide, 3.40 high); a lift piece has a wagon and a bay
  6. lifts       the unit set never stands on a lift's footprint; every big set (a `storage.where == "lift"` wagon)
                 fits the back lift (5.0 x 2.4) and the front lift (6.0 x 2.4); in every transition where a lift moves,
                 nothing that stays on stands on its footprint
  7. sightlines  (report, and a floor) how much of the unit set's acting edges the extreme seats see past the piers
                 and the legs
"""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SET = os.path.join(HERE, '..', 'assets', 'johnny-tremain', 'set.json')
E = 0.005                                   # tolerance: touching is not overlapping

LIFTS = {                                   # CONTRACT.md (stage frame)
    'front': {'x': (-3.00, 3.00), 'z': (0.30, 2.70)},
    'back':  {'x': (-2.50, 2.50), 'z': (3.60, 6.00)},
}
ARCH_H = 4.40
PLATFORMS = {'loft': 2.40, 'wharf-deck': 0.45, 'wharf-step': 0.22, 'judge-platform': 0.30}
LOFT_UNDER = 2.30                           # the loft's under-side: anything up to here stands under it
OPEN_FRAMES = {'loft-rafters'}              # an A-frame over the loft: nothing collides with it below 4.40
PAIRS_OK = {frozenset(p) for p in [('furnace', 'loft'), ('furnace', 'loft-rafters')]}
DECK = {'x': (-9.45, 9.60), 'z': (-2.65, 6.60)}
SR_ROOM = {'x': (6.00, 9.60), 'z': (-2.65, 1.60)}       # the SR side room fills the SR wing downstage of z 1.6
APRON_X = (-5.60, 5.95)
PARKS = {                                   # the wings' parks, stage frame: rects a stored piece stands wholly inside
    # stage left since the underground's stair hole (below): behind the legs between them (x -6.20...-4.65, the legs at z
    # 0.6 / 2.6 / 4.6, lumber pile b upstage), and the strip downstage of the hole
    'SL wing': [{'x': (-6.20, -4.65), 'z': (0.65, 2.55)}, {'x': (-6.20, -4.65), 'z': (2.65, 4.55)},
                {'x': (-6.20, -5.65), 'z': (4.65, 6.40)}, {'x': (-9.30, -6.30), 'z': (0.20, 1.60)}],
    'SR wing': [{'x': (6.30, 9.40), 'z': (1.70, 6.40)}],
}
KEEP_OUT = [                                # nothing stands, parks or travels here
    ('the stair hole in the SL wing (the underground, RULING GJ)', {'x': (-9.40, -6.25), 'z': (1.70, 6.30)}),
]
DOORS = {'w': 2.0, 'h': 3.40}
LANES = {'SL': (-4.30, -0.80), 'SR': (1.05, 4.60)}
SEATS = {                                   # plan-view eyes (stage frame): the stalls' extremes and the centre
    'front row, house right (SL side)': (-5.2, -4.3),
    'front row, house left (SR side)': (4.6, -4.3),
    'widest row, house right': (-8.6, -6.8),
    'widest row, house left': (8.5, -6.8),
    'centre stalls': (0.0, -9.0),
}


def load(path=SET):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


# ---- geometry ---------------------------------------------------------------------------------------------------
def corners(x, z, w, d, rot):
    """The footprint's four corners: w along local x, d along local z, turned rot degrees about +y (three.js)."""
    t = math.radians(rot or 0); c, s = math.cos(t), math.sin(t)
    out = []
    for u, v in ((-w / 2, -d / 2), (w / 2, -d / 2), (w / 2, d / 2), (-w / 2, d / 2)):
        out.append((x + u * c + v * s, z - u * s + v * c))
    return out


def sat(a, b):
    """Two convex polygons overlap (more than E) by the separating-axis test."""
    for poly in (a, b):
        for i in range(len(poly)):
            x0, z0 = poly[i]; x1, z1 = poly[(i + 1) % len(poly)]
            nx, nz = z1 - z0, -(x1 - x0); L = math.hypot(nx, nz) or 1; nx, nz = nx / L, nz / L
            pa = [px * nx + pz * nz for px, pz in a]; pb = [px * nx + pz * nz for px, pz in b]
            if max(pa) <= min(pb) + E or max(pb) <= min(pa) + E:
                return False
    return True


def rect(x0, x1, z0, z1):
    return [(x0, z0), (x1, z0), (x1, z1), (x0, z1)]


def bbox(poly):
    xs = [p[0] for p in poly]; zs = [p[1] for p in poly]
    return min(xs), max(xs), min(zs), max(zs)


def inside(poly, x0, x1, z0, z1, e=E):
    return all(x0 - e <= px <= x1 + e and z0 - e <= pz <= z1 + e for px, pz in poly)


# ---- the plan -----------------------------------------------------------------------------------------------------
class Plan:
    def __init__(self, d):
        self.d = d
        self.pieces = {p['id']: p for p in d['pieces']}
        self.order = [(s['n'], g['seg']) for s in d['scenes'] for g in s['segments']]

    def dims(self, p, pl):
        w, h, dd = p['size']
        if pl.get('w') is not None: w = pl['w']
        k = pl.get('scale', 1) or 1
        w, h, dd = w * k, h * k, dd * k
        if pl.get('tipped'): h, dd = dd, h     # on its side: its height lies along its depth
        return w, h, dd

    def foot(self, p, pl):
        w, h, dd = self.dims(p, pl)
        return corners(pl['x'], pl['z'], w, dd, pl.get('rotY', 0))

    def ys(self, p, pl):
        return pl.get('y', 0), pl.get('y', 0) + self.dims(p, pl)[1]

    def placements(self, pid, n, seg):
        """The placements of piece pid on in scene n segment seg, or [] when it is off."""
        p = self.pieces[pid]
        for e in p['scenes']:
            if isinstance(e, int):
                if e == n: return list(p['home'])
                continue
            if e['n'] != n: continue
            if e.get('seg') and seg not in e['seg']: continue
            if 'atBySeg' in e and str(seg) in e['atBySeg']: return list(e['atBySeg'][str(seg)])
            if 'at' in e: return list(e['at'])
            return list(p['home'])
        return []

    def on(self, n, seg):
        """{pid: [placements]} for everything on (flown pieces only when flown in)."""
        out = {}
        for pid in self.pieces:
            pl = self.placements(pid, n, seg)
            if pl: out[pid] = pl
        return out

    def wagon(self, pid):
        st = self.pieces[pid].get('storage') or {}
        return st.get('wagon') if st.get('where') == 'lift' else None


# ---- the checks ---------------------------------------------------------------------------------------------------
def check(d, verbose=False):
    P = Plan(d); fails = []; lines = []
    ok = lambda name, msgs, extra='': (lines.append(f"{'PASS' if not msgs else 'FAIL'}  {name}{(' — ' + extra) if extra else ''}"),
                                       [lines.append('      ' + m) for m in msgs[:40]],
                                       lines.append(f'      … {len(msgs) - 40} more') if len(msgs) > 40 else None,
                                       fails.extend(msgs))

    def solid(pid, p):                       # takes part in overlaps
        if p['kind'] == 'hand': return False
        if pid in OPEN_FRAMES: return False
        if p['kind'] == 'flown' and not (p.get('trim') or {}).get('deadHung'): return False
        return True

    # 1 + 2 + 4: per segment
    over, sup, deck = [], [], []
    for n, seg in P.order:
        on = P.on(n, seg)
        items = []
        for pid, pls in on.items():
            p = P.pieces[pid]
            if p['kind'] == 'flown' and not (p.get('trim') or {}).get('deadHung'): continue
            for i, pl in enumerate(pls):
                items.append((pid, i, p, pl, P.foot(p, pl), P.ys(p, pl)))
        tag = f'{n}.{seg}'
        for a in range(len(items)):
            ida, ia, pa, pla, fa, ya = items[a]
            # 4: on the deck
            x0, x1, z0, z1 = bbox(fa)
            if not inside(fa, *DECK['x'], *DECK['z']): deck.append(f'{tag} {ida}#{ia} off the deck: x {x0:.2f}…{x1:.2f} z {z0:.2f}…{z1:.2f}')
            elif z0 < 0 - E and not inside(fa, *APRON_X, -2.65, 6.6): deck.append(f'{tag} {ida}#{ia} on the apron but past its walls: x {x0:.2f}…{x1:.2f}')
            elif sat(fa, rect(*SR_ROOM['x'], *SR_ROOM['z'])): deck.append(f'{tag} {ida}#{ia} in the SR side room')
            for name, r in KEEP_OUT:
                if sat(fa, rect(*r['x'], *r['z'])): deck.append(f'{tag} {ida}#{ia} stands on {name}')
            # 2: support
            base = ya[0]
            if base > E and pa['kind'] not in ('flown', 'hand'):
                cands = [it for it in items if it[0] in PLATFORMS and abs(PLATFORMS[it[0]] + it[3].get('y', 0) - base) < 0.01]
                cands += [it for it in items if it[0] not in PLATFORMS and (it[0], it[1]) != (ida, ia) and abs(it[5][1] - base) < 0.012]
                if not any(inside([((px + sum(q[0] for q in fa) / 4) / 2, (pz + sum(q[1] for q in fa) / 4) / 2) for px, pz in fa],
                                  *bbox(it[4])[:2], *bbox(it[4])[2:], 0.02) for it in cands):
                    sup.append(f'{tag} {ida}#{ia} at y {base:.2f} stands on nothing there (x {pla["x"]}, z {pla["z"]})')
            if not solid(ida, pa): continue
            for b in range(a + 1, len(items)):
                idb, ib, pb, plb, fb, yb = items[b]
                if not solid(idb, pb) or ida == idb and False: continue
                if frozenset((ida, idb)) in PAIRS_OK: continue
                if ya[1] <= yb[0] + E or yb[1] <= ya[0] + E: continue
                if not sat(fa, fb): continue
                # the loft: under it (to 2.30) or on it (from 2.40) is fine
                if ida == 'loft' or idb == 'loft':
                    other = yb if ida == 'loft' else ya
                    if other[1] <= LOFT_UNDER + E or other[0] >= 2.40 - E: continue
                # a platform carries what stands on its top
                if ida in PLATFORMS and abs(yb[0] - (PLATFORMS[ida] + pla.get('y', 0))) < 0.01: continue
                if idb in PLATFORMS and abs(ya[0] - (PLATFORMS[idb] + plb.get('y', 0))) < 0.01: continue
                over.append(f'{tag} {ida}#{ia} overlaps {idb}#{ib}')
    ok('overlaps: no two pieces on in a segment collide', over, f'{len(P.order)} segments')
    ok('support: every raised piece stands on something on', sup)
    ok('deck: every on piece stands on the deck (not the SR side room, not past the apron walls)', deck)

    # 3: heights, lanes, out-trims
    hi = []; info = []
    for pid, p in P.pieces.items():
        trim = p.get('trim')
        flown = p['kind'] == 'flown' and not (trim or {}).get('deadHung')
        pls = list(p['home'])
        for e in p['scenes']:
            if isinstance(e, dict):
                pls += e.get('at', []); [pls.extend(v) for v in e.get('atBySeg', {}).values()]
        for pl in pls:
            y0, y1 = P.ys(p, pl)
            if not flown and pid != 'masking-legs' and pid != 'masking-border' and y1 > ARCH_H + E:
                hi.append(f'{pid} reaches {y1:.2f} over the deck (unflown; the arch is {ARCH_H})')
        if flown:
            w = P.dims(p, p['home'][0])[0]
            for pl in p['home']:
                x0, x1 = pl['x'] - w / 2, pl['x'] + w / 2
                if not any(L[0] - E <= x0 and x1 <= L[1] + E for L in LANES.values()) and 'with the steeple' not in trim.get('lane', ''):
                    hi.append(f'{pid} x {x0:.2f}…{x1:.2f} fits neither lane between the iron\'s pipes')
                h = P.dims(p, pl)[1]
                seen = seen_flown(pl['z'], trim['out'], trim['out'] + h)
                if trim['out'] + h > FLY_TOP + E: hi.append(f'{pid} at out-trim reaches {trim["out"] + h:.2f}, over the fly roof ({FLY_TOP})')
                if seen and not trim.get('outSeen'):
                    hi.append(f'{pid} at out-trim {trim["out"]:.2f}: ' + '; '.join(f'{n} sees {a:.2f}…{b:.2f}' for n, a, b in seen))
                elif seen: info.append(f'{pid} at out-trim: ' + '; '.join(f'{n} sees {a:.2f}…{b:.2f}' for n, a, b in seen) + f' (recorded: {trim["outSeen"]})')
    ok('heights: nothing unflown over 4.40; flown pieces in a lane, under the fly roof and hidden at out-trim from every row', hi)
    for m in info: lines.append('INFO  ' + m)

    # 5: storage
    st = []
    parked = {}                                   # park -> [(pid, poly)]
    for pid, p in P.pieces.items():
        s = p.get('storage') or {}
        where = s.get('where')
        if p['kind'] in ('unit', 'hand') or where in ('on stage', 'flown'): continue   # hand props: boxed on the props tables
        if where == 'lift':
            if not s.get('wagon') or not s.get('bay'): st.append(f'{pid}: a lift piece needs storage.wagon and storage.bay')
            continue
        if where == 'backstage':
            w, h, dd = p['size']
            if min(w, dd) > DOORS['w'] - E or h > DOORS['h'] + E: st.append(f'{pid} ({w}×{h}×{dd}) does not pass the centre doors (2.0 × 3.40)')
            continue
        if where in PARKS:
            k = PARKS[where]
            n = p.get('count', 1)
            locs = s.get('at') or [s] * 1
            for i, loc in enumerate(locs):
                poly = P.foot(p, {**loc, 'rotY': loc.get('rotY', 0)})
                if not any(inside(poly, *r['x'], *r['z']) for r in k): st.append(f'{pid}#{i} is in none of the {where} parks: {tuple(round(v, 2) for v in bbox(poly))}')
                for name, r in KEEP_OUT:
                    if sat(poly, rect(*r['x'], *r['z'])): st.append(f'{pid}#{i} is parked on {name}')
                # its walk on and off: the hull of the parked and every on-stage footprint it glides between
                for e in p['scenes']:
                    n_ = e if isinstance(e, int) else e['n']
                    for seg_ in [g['seg'] for sc in P.d['scenes'] if sc['n'] == n_ for g in sc['segments']]:
                        pls = P.placements(pid, n_, seg_)
                        if i < len(pls) and pls[i].get('y', 0) <= 0.3:
                            hull = convex(poly + P.foot(p, pls[i]))
                            for name, r in KEEP_OUT:
                                if sat(hull, rect(*r['x'], *r['z'])): st.append(f'{pid}#{i} glides across {name} on its way to {n_}.{seg_}')
                parked.setdefault(where, []).append((pid, i, poly))
            if len(locs) < n and p['kind'] != 'hand':
                st.append(f'{pid}: {n} copies but {len(locs)} storage spot(s) in the {where}')
        elif where and where.startswith('props table'):
            continue
        else:
            st.append(f'{pid}: unknown storage "{where}"')
    # two pieces parked in one wing collide only if both are parked at the same moment
    offsets = {}
    for n, seg in P.order:
        on = set(P.on(n, seg))
        for where, lst in parked.items():
            for a in range(len(lst)):
                for b in range(a + 1, len(lst)):
                    pa, ia, fa = lst[a]; pb, ib, fb = lst[b]
                    if pa in on or pb in on: continue
                    if sat(fa, fb): offsets.setdefault((where, pa, ia, pb, ib), []).append(f'{n}.{seg}')
    for (where, pa, ia, pb, ib), when in offsets.items():
        st.append(f'{where}: {pa}#{ia} and {pb}#{ib} parked on top of each other ({len(when)} segments, from {when[0]})')
    ok('storage: parks hold their pieces apart; backstage pieces pass the doors; lift pieces have a wagon and a bay', st)

    # 6: lifts
    lf = []
    for pid, p in P.pieces.items():
        if p['kind'] != 'unit' and not (p.get('trim') or {}).get('deadHung'): continue
        for i, pl in enumerate(p['home']):
            for name, L in LIFTS.items():
                if sat(P.foot(p, pl), rect(*L['x'], *L['z'])): lf.append(f'unit piece {pid}#{i} stands on the {name} lift')
    wag = {}
    for n, seg in P.order:
        on = P.on(n, seg)
        for pid, pls in on.items():
            w = P.wagon(pid)
            if not w: continue
            for pl in pls:
                wag.setdefault((w, n, seg), []).extend(P.foot(P.pieces[pid], pl))
    for (w, n, seg), pts in wag.items():
        x0, x1, z0, z1 = bbox(pts)
        W, D = x1 - x0, z1 - z0
        for name, L in LIFTS.items():
            lw, ld = L['x'][1] - L['x'][0], L['z'][1] - L['z'][0]
            if W > lw - 0.1 + E or D > ld - 0.1 + E:
                lf.append(f'wagon "{w}" in {n}.{seg} is {W:.2f} × {D:.2f}: does not ride the {name} lift ({lw} × {ld}, 5 cm a side)')
    moves = []
    for k in range(1, len(P.order)):
        A, B = P.order[k - 1], P.order[k]
        onA, onB = P.on(*A), P.on(*B)
        wa = {P.wagon(p) for p in onA if P.wagon(p)}; wb = {P.wagon(p) for p in onB if P.wagon(p)}
        leave, come = wa - wb, wb - wa
        moving = (['back'] if leave else []) + (['front'] if come else [])
        if not moving: continue
        moves.append(f'{A[0]}.{A[1]} → {B[0]}.{B[1]}: {", ".join(moving)} lift' + (f'; off: {", ".join(sorted(leave))}' if leave else '') + (f'; on: {", ".join(sorted(come))}' if come else ''))
        stay = [pid for pid in onA if pid in onB and not P.wagon(pid)]
        for pid in stay:
            p = P.pieces[pid]
            if p['kind'] == 'unit' or (p.get('trim') or {}).get('deadHung'): continue
            if p['kind'] in ('flown', 'hand'): continue      # carried: an actor takes it off the lift
            for pl in onA[pid] + onB[pid]:
                for name in moving:
                    L = LIFTS[name]
                    if sat(P.foot(p, pl), rect(*L['x'], *L['z'])):
                        lf.append(f'{A[0]}.{A[1]} → {B[0]}.{B[1]}: {pid} stays on the {name} lift while it moves')
    ok('lifts: unit set off both lifts; every wagon rides both; nothing stays on a moving lift', sorted(set(lf)), f'{len(moves)} transitions move a lift')
    if verbose:
        lines.append('INFO  the transitions that move a lift:')
        for m in moves: lines.append('      ' + m)

    # 7: sightlines (plan view): the share of each unit platform's acting edge each seat sees past the piers and legs
    occ = [rect(-9.6, -4.30, -0.25, 0.0), rect(4.30, 9.6, -0.25, 0.0)]
    legs = P.pieces.get('masking-legs')
    if legs:
        for pl in legs['home']: occ.append(P.foot(legs, pl))
    def seen(eye, pt):
        ex, ez = eye; px, pz = pt
        for poly in occ:
            for i in range(4):
                a, b = poly[i], poly[(i + 1) % 4]
                if seg_x(ex, ez, px, pz, *a, *b): return False
        return True
    sl = []; table = []
    for pid, edge in (('loft', 'front+onstage'), ('wharf-deck', 'front+onstage'), ('ladder', 'all'), ('furnace', 'onstage')):
        p = P.pieces.get(pid)
        if not p: continue
        pl = p['home'][0]; x0, x1, z0, z1 = bbox(P.foot(p, pl))
        onstage_x = x1 if pl['x'] < 0 else x0
        pts = [(x0 + (x1 - x0) * i / 20, z0) for i in range(21)] if 'front' in edge or edge == 'all' else []
        if 'onstage' in edge or edge == 'all': pts += [(onstage_x, z0 + (z1 - z0) * i / 20) for i in range(21)]
        row = []
        for name, eye in SEATS.items():
            f = sum(seen(eye, q) for q in pts) / len(pts)
            row.append((name, f))
        table.append((pid, row))
        for name, f in row:
            if name.startswith('front row') or name == 'centre stalls':
                if f < 0.5 - E: sl.append(f'{pid}: the {name} sees only {f:.0%} of its acting edge')
    ok('sightlines: the front row\'s extreme seats and the centre see at least half of each unit platform\'s acting edge', sl)
    lines.append('INFO  sightlines (share of the acting edge seen, plan view, past the piers and the legs):')
    if True:
        for pid, row in table:
            lines.append('      ' + f'{pid:11s} ' + ' · '.join(f'{n.split(",")[0].replace("row", "")}{"/" + n.split(",")[1].strip()[6:8] if "," in n else ""} {f:.0%}' for n, f in row))
    return fails, lines


FLY_TOP = 15.20 - 0.05                       # the fly roof over the deck, less a margin
BORDERS = [(3.0, 4.40, 5.00)]                # the masking border: z, bottom, top over the deck
HEADER = (0.0, 4.40)                         # the arch's header: z, its underside over the deck
def seats():
    """Eyes down the centre of the stalls: the front row (z -4.3, eye 0.32 over the deck) to the back (z -16.3, 3.1)."""
    for k in range(7):
        t = k / 6; yield (f'row {1 + round(t * 14)}', -4.3 - 12.0 * t, 0.32 + 2.78 * t)


def seen_flown(z, y0, y1):
    """The parts of a flown piece (bottom y0, top y1, at depth z) each seat sees under the header and round the border."""
    out = []
    for name, ez, ey in seats():
        at = lambda zz, yy: ey + (yy - ey) * (z - ez) / (zz - ez)        # where the line through (zz, yy) meets depth z
        hid = [(at(*HEADER), 1e9)] + [(at(bz, b0), at(bz, b1)) for bz, b0, b1 in BORDERS if bz < z]
        a = y0; vis = []
        while a < y1 - 0.01:
            cov = next(((h0, h1) for h0, h1 in hid if h0 <= a + 1e-6 < h1), None)
            if cov: a = cov[1]; continue
            nxt = min([h0 for h0, h1 in hid if h0 > a] + [y1]); vis.append((a, min(nxt, y1))); a = nxt
        vis = [(a, b) for a, b in vis if b - a > 0.02]
        if vis: out.append((name, vis[0][0], vis[-1][1]))
    return out


def convex(pts):
    P_ = sorted(set(pts)); cr = lambda o, a, b: (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0]); lo, up = [], []
    for q in P_:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], q) <= 0: lo.pop()
        lo.append(q)
    for q in reversed(P_):
        while len(up) >= 2 and cr(up[-2], up[-1], q) <= 0: up.pop()
        up.append(q)
    return lo[:-1] + up[:-1]


def seg_x(ax, az, bx, bz, cx, cz, dx, dz):
    """Segments a-b and c-d properly intersect."""
    def o(px, pz, qx, qz, rx, rz): return (qx - px) * (rz - pz) - (qz - pz) * (rx - px)
    d1, d2 = o(cx, cz, dx, dz, ax, az), o(cx, cz, dx, dz, bx, bz)
    d3, d4 = o(ax, az, bx, bz, cx, cz), o(ax, az, bx, bz, dx, dz)
    return (d1 > 1e-9) != (d2 > 1e-9) and (d3 > 1e-9) != (d4 > 1e-9) and abs(d1) > 1e-9 and abs(d2) > 1e-9


def main():
    d = load(sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('-') else SET)
    fails, lines = check(d, '--verbose' in sys.argv or '-v' in sys.argv)
    print('\n'.join(lines))
    print(f"\njt-set-check: {'PASS' if not fails else 'FAIL'} — {len(d['pieces'])} pieces, {sum(len(s['segments']) for s in d['scenes'])} segments, {len(fails)} problem(s)")
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
