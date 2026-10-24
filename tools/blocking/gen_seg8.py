# Generates segments/seg8.json (Hamilton 2-17 .. 2-23 blocking). Run: python -I gen_seg8.py
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'segments', 'seg8.json')
os.makedirs(os.path.join(HERE, 'segments'), exist_ok=True)

LEN = {'2-17': 111.0, '2-18': 270.0, '2-19': 237.0, '2-20': 150.0, '2-21': 47.0, '2-22': 302.0, '2-23': 217.0}
ORDER = ['2-17', '2-18', '2-19', '2-20', '2-21', '2-22', '2-23']
OFS = {}
_s = 0.0
for _t in ORDER:
    OFS[_t] = _s; _s += LEN[_t]

def T(tr, at): return OFS[tr] + at
def TR(abs_t):
    for tr in reversed(ORDER):
        if abs_t >= OFS[tr] - 1e-9:
            return tr, abs_t - OFS[tr]
    raise ValueError(abs_t)

A = {}          # actor -> list of waypoints (with '_T')

def wp(a, tr, at, x, z, y=None, dwell=None, facing=None, off=False, label=None):
    assert 0 <= at and (at <= LEN[tr] or tr == ORDER[-1]), (a, tr, at)   # 2-23: the OPEN tail (RULING FQ)
    w = {'track': tr, 'at': round(at, 2), 'x': round(x, 3), 'z': round(z, 3)}
    if y is not None: w['y'] = y
    if dwell is not None: w['dwell'] = dwell
    if facing is not None: w['facing'] = round(facing, 1)
    if off: w['off'] = True
    if label: w['label'] = label
    w['_T'] = T(tr, w['at'])
    L = A.setdefault(a, [])
    if L: assert w['_T'] > L[-1]['_T'] + 1e-6, (a, tr, at, L[-1]['track'], L[-1]['at'])
    L.append(w)
    return w

def wpa(a, abs_t, x, z, **kw):
    tr, at = TR(abs_t)
    return wp(a, tr, at, x, z, **kw)

def last(a): return A[a][-1]

def face(p, q):
    return math.degrees(math.atan2(q[0] - p[0], q[1] - p[1]))

C = (0.0, 0.95)
def clock(r, deg, c=C):
    t = math.radians(deg)
    return (c[0] + r * math.sin(t), c[1] - r * math.cos(t))

# entrances: (off point, y, walk-throughs from the off point towards the stage)
ENT = {
    'W-DSR': ((-7.3, 4.6), None, [(-5.8, 4.75)]),
    'W-DSL': ((7.3, 4.6), None, [(5.8, 4.75)]),
    'W-USR': ((-8.5, -3.0), None, [(-3.3, -2.95)]),
    'W-USL': ((8.5, -3.0), None, [(4.75, -2.95), (4.55, -1.1)]),
    'W-MSL': ((8.0, -0.5), None, [(6.2, -0.5), (4.6, 0.45)]),
    'D-UC':  ((1.25, -4.9), None, [(1.15, -3.6)]),
    'G-UC':  ((0.6, -4.8), 'gallery', [(0.6, -3.35)]),
}

def chain_len(pts):
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:]))

USE = {}
def clash(ent, t_off, t_door, gap=1.6):
    """two bodies on one entrance route: they must pass the off point AND the door gap s apart, in the same order."""
    for u_off, u_door in USE.get(ent, []):
        if abs(t_off - u_off) < gap or abs(t_door - u_door) < gap or (t_off - u_off) * (t_door - u_door) <= 0:
            return True
    return False
def enter(a, ent, target, t_arr, facing, speed=1.3, label=None, ty=None, dwell=None, via=None):
    """off waypoint at the entrance, walk-throughs, arrival at target at t_arr (abs time)."""
    (ox, oz), oy, wts = ENT[ent]
    pts = [(ox, oz)] + list(wts) + list(via or []) + [target]
    total = chain_len(pts)
    t0 = max(0.0, t_arr - total / speed)
    floor_t = (A[a][-1]['_T'] + 0.2) if A.get(a) else 0.0
    dd = chain_len(pts[:len(wts) + 1])
    door = lambda t0: t0 + dd * (t_arr - t0) / total
    t_try = t0
    while clash(ent, t_try, door(t_try)) and t_try - 0.25 >= floor_t and (t_arr - t_try) < total / 0.6:
        t_try -= 0.25
    if not clash(ent, t_try, door(t_try)):
        t0 = t_try
    USE.setdefault(ent, []).append((t0, door(t0)))
    speed = total / (t_arr - t0)
    wpa(a, t0, ox, oz, y=oy, off=True, dwell=0, label=label)
    acc = 0.0
    for p, q in zip(pts, pts[1:-1]):
        pass
    for k in range(1, len(pts) - 1):
        acc += math.hypot(pts[k][0] - pts[k - 1][0], pts[k][1] - pts[k - 1][1])
        wpa(a, t0 + acc / speed, pts[k][0], pts[k][1], y=oy if (ent == 'G-UC' and k <= len(wts)) else None, dwell=0)
    return wpa(a, t_arr, target[0], target[1], y=ty, facing=facing, dwell=dwell)

def leave(a, ent, t_dep, speed=1.3, via=None, label=None):
    """from the actor's current position: walk-throughs, the off waypoint. Returns the off time."""
    p0 = (last(a)['x'], last(a)['z'])
    (ox, oz), oy, wts = ENT[ent]
    pts = [p0] + list(via or []) + list(reversed(wts)) + [(ox, oz)]
    total = chain_len(pts)
    dd = chain_len(pts[:len(via or []) + 2])
    n_try = 0
    while clash(ent, t_dep + total / speed, t_dep + dd / speed) and n_try < 40:
        t_dep += 0.25; n_try += 1
    USE.setdefault(ent, []).append((t_dep + total / speed, t_dep + dd / speed))
    acc = 0.0
    nvia = len(via or [])
    for k in range(1, len(pts)):
        acc += math.hypot(pts[k][0] - pts[k - 1][0], pts[k][1] - pts[k - 1][1])
        t = t_dep + acc / speed
        if k < len(pts) - 1:
            yk = oy if (ent == 'G-UC' and k > nvia) else None
            if ent == 'G-UC' and k <= nvia: yk = 'gallery'
            wpa(a, t, pts[k][0], pts[k][1], y=yk, dwell=0)
        else:
            wpa(a, t, ox, oz, y=oy, off=True, label=label)
    return t_dep + acc / speed

def circle(a, r, a0, a1, t0, t1, step=40.0, c=C, end_facing=None, end_dwell=None):
    """walk the circle from angle a0 (where she already stands, at t0) to a1, arriving t1."""
    n = max(1, int(math.ceil(abs(a1 - a0) / step - 1e-9)))
    if A[a][-1]['_T'] < t0 - 0.05:
        w = A[a][-1]
        wpa(a, t0, w['x'], w['z'], y=w.get('y'), facing=w.get('facing'), dwell=0)
    else:
        A[a][-1]['dwell'] = 0
    for k in range(1, n + 1):
        f = k / n
        ang = a0 + (a1 - a0) * f
        x, z = clock(r, ang, c)
        t = t0 + (t1 - t0) * f
        if k < n:
            wpa(a, t, x, z, dwell=0)
        else:
            if end_facing is None:
                wpa(a, t, x, z, dwell=0 if end_dwell is None else end_dwell)
            else:
                wpa(a, t, x, z, facing=end_facing, dwell=end_dwell)

def walk(a, abs_t, p, facing=None, dwell=None, y=None):
    return wpa(a, abs_t, p[0], p[1], facing=facing, dwell=dwell, y=y)

def hold(a, abs_t, facing, dwell=None):
    """a facing change on the spot (a new stop at the same place)."""
    w = last(a)
    return wpa(a, abs_t, w['x'], w['z'], y=w.get('y'), facing=facing, dwell=dwell)

ENS = ['ens%d' % i for i in range(1, 11)]

import itertools
def best_assign(srcs, dsts, center=None):
    """match sources to destinations: brute force for small sets, else by angle round `center`."""
    n = len(srcs); assert n == len(dsts)
    if n <= 7:
        best = None
        for perm in itertools.permutations(range(n)):
            c = sum(math.hypot(srcs[i][0] - dsts[j][0], srcs[i][1] - dsts[j][1]) for i, j in enumerate(perm))
            if best is None or c < best[0]: best = (c, perm)
        return [dsts[j] for j in best[1]]
    ang = lambda p: math.atan2(p[0] - center[0], -(p[1] - center[1]))
    si = sorted(range(n), key=lambda i: ang(srcs[i])); dj = sorted(range(n), key=lambda j: ang(dsts[j]))
    out = [None] * n
    for i, j in zip(si, dj): out[i] = dsts[j]
    return out
def pos(a): return (last(a)['x'], last(a)['z'])
def hungarian(srcs, dsts):
    n = len(srcs); INF = float('inf')
    cost = [[(p[0] - d[0]) ** 2 + (p[1] - d[1]) ** 2 for d in dsts] for p in srcs]
    u = [0.0] * (n + 1); v = [0.0] * (n + 1); pp = [0] * (n + 1); way = [0] * (n + 1)
    for i in range(1, n + 1):
        pp[0] = i; j0 = 0; minv = [INF] * (n + 1); used = [False] * (n + 1)
        while True:
            used[j0] = True; i0 = pp[j0]; delta = INF; j1 = 0
            for j in range(1, n + 1):
                if not used[j]:
                    cur = cost[i0 - 1][j - 1] - u[i0] - v[j]
                    if cur < minv[j]: minv[j] = cur; way[j] = j0
                    if minv[j] < delta: delta = minv[j]; j1 = j
            for j in range(n + 1):
                if used[j]: u[pp[j]] += delta; v[j] -= delta
                else: minv[j] -= delta
            j0 = j1
            if pp[j0] == 0: break
        while True:
            j1 = way[j0]; pp[j0] = pp[j1]; j0 = j1
            if j0 == 0: break
    out = [None] * n
    for j in range(1, n + 1): out[pp[j] - 1] = dsts[j - 1]
    return out


def ang_of(p, c=C):
    return math.degrees(math.atan2(p[0] - c[0], -(p[1] - c[1]))) % 360
def rad_of(p, c=C):
    return math.hypot(p[0] - c[0], p[1] - c[1])
def revolve(a, d_ang, t0, t1, step=25.0, end_facing=None):
    """the turntable carries her round C by d_ang degrees (+ clockwise seen from above, i.e. 12 -> 3)."""
    p = pos(a); r = rad_of(p); a0 = ang_of(p)
    circle(a, r, a0, a0 + d_ang, t0, t1, step=step, end_facing=end_facing)

# =====================================================================================
# 2-17 STAY ALIVE (REPRISE)   0.36 shot / 2.86 the doctor and the table / 8.66 Lose Wedge /
# 32.46 Philip to his father / 59.64 Eliza enters / 75.19 mother and son / 94.82 counting /
# 106.78 Philip dies / 109.6 blackout (scream)
# REVIEW (seg 8 reviewer): fan accounts of the Broadway staging (ironinkpen.tumblr.com, Act II notes) put Philip on a
# table on the turning platform at the centre, Hamilton at his side, Eliza entering from centre (upstage), and only
# then the table moving to the front of the stage where the platform stops (the film editor's front-facing three-shot).
# =====================================================================================
# SPOTLIGHT (seg 8 spotlight agent): Binkley's own 1104 chain puts the family DOWNSTAGE from the shot on: his shot
# pool for Philip (ch8, preset 1023 "Pools") lands at (-0.68, 4.13); the auto-follow ch7 ("AF- start move around")
# ends at (-0.83, 3.87); "DS to CTO" warms the DS pair ch7/ch9 (+-0.8, 3.95); "add Ring" brings the table wash ch98
# up on (0, 4.13). The table ends at the front (the editor's front-of-stage three-shot) - by 32.46 (REVIEW 2, below).
# REVIEW 2 (Jack's verdict: sparse and right): ETC's THPP renders of Binkley's own cues show the table carrying Philip
# ROUND THE OUTER RING - at 12 o'clock in 1104.4 "Lose Wedge" (8.66), at the SL side in 1104.5 (28.46), at the front with
# one figure (the Doctor) behind it in 1110 "add Ring" (32.46); "AF- start move around" (2.06) is an auto-follow riding
# it. ironinkpen: Philip on a table on the slowly spinning platform, Hamilton at his side, the table stopping at the
# front. Nobody in the number but the four (the Doctor has a line): the bearers and the seven gallery watchers are cut.
TABLE_F = (-0.3, 3.9)       # the table at the front, between the DS pools ch7/ch9 (angle 186 on the outer ring)
TAB_R = 2.97
# FILM ROUND (2-24, the Disney+ clip; research/seg8.md "Film round"): the family at the table, both UPSTAGE of it (Philip's
# head SL): Hamilton behind his head and chest, Eliza on Hamilton's SR side (clip 33.4 wide, 64-97 close).
H_T = (0.2, 3.3); E_T = (-0.55, 3.3); DOC_T = (-1.2, 2.7)
# FILM ROUND: two of the company catch Philip and carry him to the table UPSTAGE SR (clip 11.4-14: the bearers at SR with
# the table behind them); the platform then carries the table clockwise round by SL (the clip at 24.9: at SL under the
# stair) to the front (33.4). Was: at 12 o'clock from 8.66 with no bearers.
TAB_A0, TAB_T0, TAB_T1, TAB_A1 = 315.0, 14.0, 32.46, 186.0 + 360.0
def tab_ang(t):             # the table's angle round C (0 = 12 o'clock, clockwise)
    if t <= TAB_T0: return TAB_A0
    if t >= TAB_T1: return TAB_A1
    return TAB_A0 + (TAB_A1 - TAB_A0) * (t - TAB_T0) / (TAB_T1 - TAB_T0)
TABLE_SR = clock(TAB_R, TAB_A0)

# Philip: handed over from seg 7 downstage of centre, his back to the house (coordinator's re-ruled mark); shot, he
# staggers, two of the company catch him and carry him upstage SR to the table; the platform carries him round to the front
wp('laurens', '2-17', 0.0, -0.4, 2.4, facing=180, dwell=0.5, label='Philip')
walk('laurens', T('2-17', 2.0), (-0.9, 1.8), facing=-150)
walk('laurens', T('2-17', 12.0), TABLE_SR, facing=0)
circle('laurens', TAB_R, TAB_A0, TAB_A1, T('2-17', TAB_T0), T('2-17', TAB_T1), step=15, end_facing=0)
hold('laurens', T('2-17', 36.36), -35)       # to his father
hold('laurens', T('2-17', 75.19), 20)        # to his mother
hold('laurens', T('2-17', 106.78), 0)        # dies

# George Eacker: handed over from seg 7 upstage on the turntable, facing away (re-ruled mark); he whirls round on
# the shot to face Philip, fires, and goes off upstage SL
wp('ens5', '2-17', 0.0, 1.6, -1.0, facing=180, dwell=0.0, label='George Eacker')
hold('ens5', T('2-17', 0.36), face((1.6, -1.0), (-0.4, 2.4)), dwell=1.2)
leave('ens5', 'W-USL', T('2-17', 1.56), speed=1.3, label='Ensemble 5')

# REVIEW 3 (coordinator's ruling, from a film clip of Blow Us All Away): seven of the company stand between Philip and
# Eacker for the count and are still on at the boundary, on a line from upstage SR to downstage SL, facing the house. At the
# shot they turn to Philip, and clear in the blackout (a comment on the clip: Eacker "goes around out of sight, shoots, and
# leaves"); ens4 stays: he is the Doctor, and goes to the inside of the table once Philip has passed.
S17 = {'ens2': (-1.34, -0.44), 'ens3': (-0.69, -0.06), 'ens4': (-0.05, 0.32), 'ens6': (1.25, 1.08),
       'ens7': (1.89, 1.46), 'ens8': (2.54, 1.84), 'ens9': (3.19, 2.22)}
S17_EX = {'ens2': 'W-USR', 'ens3': 'W-USR', 'ens6': 'W-MSL', 'ens7': 'W-MSL', 'ens8': 'W-DSL', 'ens9': 'W-DSL'}
for k, (e, p) in enumerate(S17.items()):
    wp(e, '2-17', 0.0, p[0], p[1], facing=0, dwell=0.0, label='Ensemble %s' % e[3:])
    hold(e, T('2-17', 0.36 + 0.06 * k), face(p, (-0.4, 2.4)), dwell=0.9)       # they turn to the shot
S17_GO = {'ens7': 1.3, 'ens6': 2.0, 'ens9': 1.3, 'ens8': 2.0}   # the nearer one first, in file
for e, t in S17_GO.items():
    leave(e, S17_EX[e], T('2-17', t), speed=1.5)
# FILM ROUND: the bearers (ens2, ens3) catch him either side and carry him up to the table SR (clip 11.4-14), then go off SR
walk('ens2', T('2-17', 2.0), (-1.35, 1.8), facing=90, dwell=0)
walk('ens3', T('2-17', 2.1), (-0.45, 1.8), facing=-90, dwell=0)
walk('ens2', T('2-17', 12.0), (TABLE_SR[0] - 0.55, TABLE_SR[1] + 0.35), facing=60)
walk('ens3', T('2-17', 12.0), (TABLE_SR[0] + 0.45, TABLE_SR[1] + 0.55), facing=-60)
leave('ens2', 'W-USR', T('2-17', 14.0), speed=1.3)
leave('ens3', 'W-USR', T('2-17', 14.6), speed=1.3)
# the Doctor (brown coat, the clip at 17-25): waits by the table, meets Hamilton, takes him aside SR (clip 24.9: the two far
# SR, the table SL), walks with him to the table as it reaches the front (clip 30) and stands upstage SR of it (33.4)
walk('ens4', T('2-17', 3.0), (-1.0, -0.2), facing=-60)
hold('ens4', T('2-17', 6.0), -100)
walk('ens4', T('2-17', 16.5), (-1.95, 0.15), facing=-120)
walk('ens4', T('2-17', 25.5), (-2.45, 1.85), facing=-110)
walk('ens4', T('2-17', 33.5), DOC_T, facing=37)

# Hamilton runs in by the deck door on "Lose Wedge" to Philip at the table up SR (clip 14: in upstage centre); the Doctor
# takes him aside SR; he walks to the table as the platform brings it to the front and leans over his son
enter('hamilton', 'D-UC', (-1.5, -0.6), T('2-17', 12.5), face((-1.5, -0.6), TABLE_SR), speed=2.4, label='Hamilton')
walk('hamilton', T('2-17', 17.5), (-2.4, 0.45), facing=70)
walk('hamilton', T('2-17', 25.0), (-3.0, 1.3), facing=60)
walk('hamilton', T('2-17', 33.0), H_T, facing=-5)       # facing down over the table
hold('hamilton', T('2-17', 36.36), -15)

# FILM ROUND: Eliza comes in from up SR (the clip at 62: in a doorway SR, the table to her SL) and goes to the table on
# Hamilton's SR side (68.4: beside him behind Philip). Was: from upstage centre into her special SL.
enter('eliza', 'W-USR', (-2.3, 1.6), T('2-17', 61.5), 110, speed=2.0, label='Eliza')
walk('eliza', T('2-17', 68.4), E_T, facing=15)
hold('hamilton', T('2-17', 75.5), -25)
walk('ens4', T('2-17', 94.82), (-1.9, 2.2), facing=40)      # the doctor gives up, steps back
hold('eliza', T('2-17', 94.82), 25)
hold('hamilton', T('2-17', 107.5), -10)
hold('eliza', T('2-17', 107.5), 10)

# =====================================================================================
# 2-18 IT'S QUIET UPTOWN   0 dark / 8.6 Angelica DS / 23.6 company in / 31 the move uptown /
# 38.4 his verse / 60.45 his prayer / 68 the company: the couple seen in the street / 89.35 pull in /
# 96.2 Hamilton DSC / 104.72 his plea to Eliza / 132.4 vow / 163.92 company returns /
# 193.66 ensemble / 208.28 couple centre / 215.86 her hand / 220.76 forgiveness /
# 250.04 company falls away / 260.5 fade to black
# REVIEW: the film editor (ProVideo Coalition) - the turntable carries the couple off SR as Angelica begins; two fan
# accounts - Angelica DSL at the top and DSR for her second solo, Hamilton alone in an empty circle at centre with the
# company round him, Eliza entering from upstage centre and walking down to front centre while he sings to her, the
# two swapping places, then side by side, then centre where she takes his hand; they leave together, arm in arm.
# The cue file's "Eliza's verse / Eliza's prayer" are his verse and his prayer: Eliza has no lines in this number.
# =====================================================================================
# the platform turns the family away towards SR; they are carried off in the dark
for a in ('laurens', 'hamilton', 'eliza', 'ens4'):
    revolve(a, 70, T('2-18', 0.4), T('2-18', 6.5), step=25, end_facing=-100)
leave('laurens', 'W-DSR', T('2-18', 6.8), speed=1.0)
leave('ens4', 'W-DSR', T('2-18', 7.0), speed=1.0, label='Ensemble 4')
leave('hamilton', 'W-DSR', T('2-18', 7.2), speed=1.1)
leave('eliza', 'W-DSR', T('2-18', 7.4), speed=1.1)

# Angelica narrates DSL, in black
# SPOTLIGHT: her tight special (ch4, 1121) is DS just SR of centre at (-0.71, 4.0); she stands in it, downstage of
# the couples' circle (the fan accounts' DSL would need the special re-aimed)
# FILM ROUND (the clip at 6.6 and 33.6): she stands SL, mid-stage, while he is at the centre; she drifts slowly up SL
# as the couples circle. Was: downstage of centre in her special (the fan accounts' DSL; the film agrees with them).
ANG_DS = (2.75, 1.7)
enter('angelica', 'W-DSL', ANG_DS, T('2-18', 8.6), -40, label='Angelica')
walk('angelica', T('2-18', 22.0), (2.95, 2.3), facing=-45)
walk('angelica', T('2-18', 38.5), (3.75, 1.0), facing=-60)           # outside the circling couples (r 2.9)
walk('angelica', T('2-18', 52.0), (4.1, -0.3), facing=-60)           # her special goes; she watches from UL
walk('angelica', T('2-18', 75.0), (4.3, 0.6), facing=-80)
hold('angelica', T('2-18', 89.35), face((4.3, 0.6), (0.0, 1.9)))    # turns to Hamilton
leave('angelica', 'W-USL', T('2-18', 98.0))
enter('angelica', 'W-DSR', (-3.2, 4.25), T('2-18', 166.0), 20)       # her second solo, DSR
walk('angelica', T('2-18', 190.0), (-3.55, 3.7), facing=30)          # a few steps in her solo
walk('angelica', T('2-18', 208.28), (-3.0, 4.2), facing=45)
leave('angelica', 'W-DSR', T('2-18', 250.5), speed=1.0)

# the company: couples circling the outer ring round Hamilton (the film's editor: "several couples" circle him on the
# turntable, counter-clockwise, then clockwise in his grief, the direction corrected as Eliza returns).
# REVIEW 2: four couples, not five (the number is not documented; fewer, per Jack's verdict). ens9 / ens10 stay off.
COUPLE = [0, 90, 180, 270]
QU = ENS[:8]
QU_ENS = {}
for i, base in enumerate(COUPLE):
    QU_ENS[ENS[2 * i]] = base
    QU_ENS[ENS[2 * i + 1]] = base + 14
def ent_for(ang):
    ang %= 360
    if ang < 40 or ang >= 330: return 'D-UC', None
    if ang < 170: return 'W-MSL', None
    if ang < 240: return 'W-DSR', None
    return 'W-USR', None
R1 = 2.9
# SPOTLIGHT: "Hamilton alone on the ring - his special SR" / "Pull in to Hamilton" (ch12 at (-2.43, 2.31), full,
# 68-96 s, the only bright light at 89-96): he walks out of the centre to the SR side, inside the couples' circle
H_QC = (0.0, 1.9)            # FILM ROUND: at the centre, not SR (below)
for k, e in enumerate(QU):
    a0 = QU_ENS[e]
    p = clock(R1, a0)
    ent, _ = ent_for(a0)
    enter(e, ent, p, T('2-18', 25.0 + 2.0 * (k % 2)), face(p, C) - 90, speed=1.2, label='Ensemble %s' % e[3:])
    # 27 -> 68: one slow revolution counter-clockwise (the healthy direction)
    circle(e, R1, a0, a0 - 360, T('2-18', 27.0), T('2-18', 68.0), step=45)
    # 68 -> 89.35: the wrong way round, clockwise, during his grief
    circle(e, R1, a0 - 360, a0 - 180, T('2-18', 68.0), T('2-18', 89.35), step=45, end_facing=None)
    end = clock(R1, a0 - 180)
    hold(e, T('2-18', 90.5), face(end, H_QC))
    ang = (a0 - 180) % 360
    # recede to the wings (D-UC is kept free for Eliza's entrance)
    if 100 <= ang < 180: ex = 'W-DSL'
    elif 180 <= ang < 260: ex = 'W-DSR'
    elif ang >= 260 or ang < 0: ex = 'W-USR'
    elif 0 <= ang < 30: ex = 'W-USL'
    else: ex = 'W-USL'
    if ang >= 330: ex = 'W-USR'
    leave(e, ex, T('2-18', 96.2 + 0.2 * k), speed=1.1)

# Hamilton: alone at the centre of the circle. FILM ROUND: he moves inside it (the clip at 47: among the passing couples)
# and is at the CENTRE, not SR, when the company pulls in (the clip at 94: alone mid-stage centre, the company at both
# sides reaching their arms to him). Was: out to his SR special at 70.
H_QC = (0.0, 1.9)
enter('hamilton', 'D-UC', C, T('2-18', 31.0), 0, speed=1.1)
walk('hamilton', T('2-18', 44.0), (-0.45, 1.3), facing=-30)   # his verse
walk('hamilton', T('2-18', 55.0), (0.4, 1.15), facing=25)
walk('hamilton', T('2-18', 63.0), (0.05, 1.5), facing=-5)     # his prayer
walk('hamilton', T('2-18', 76.0), (-0.5, 1.95), facing=-40)   # seen in the street
walk('hamilton', T('2-18', 86.0), H_QC, facing=10)
hold('hamilton', T('2-18', 89.35), 0)
# SPOTLIGHT: "Hamilton DSC" is Binkley's preset 151 "Ham DSC" (ch43, focus (0.27, 2.53)); her special for the plea
# (ch1, 1130) is re-aimed beside it at (1.60, 2.44). The couple's front-centre business is played there, not at z 4.
H_PLEA = (0.3, 2.45)
walk('hamilton', T('2-18', 100.0), H_PLEA, facing=60)
# Eliza comes down from upstage centre to the front, beside him; he sings to her
enter('eliza', 'D-UC', (1.45, 2.5), T('2-18', 104.72), -90, speed=1.3)
walk('hamilton', T('2-18', 112.0), (0.65, 2.35), facing=80)   # a step toward her
walk('hamilton', T('2-18', 122.0), (0.35, 2.6), facing=60)    # and back
walk('hamilton', T('2-18', 132.4), (0.7, 2.3), facing=75)     # the vow
# they swap places: he goes round behind her to her SL side
walk('hamilton', T('2-18', 144.5), (1.3, 1.35), dwell=0)
walk('hamilton', T('2-18', 146.5), (2.3, 2.45), facing=-100)
walk('eliza', T('2-18', 149.0), (0.9, 2.35), facing=80)
# side by side, she looking straight out
walk('eliza', T('2-18', 165.5), (0.5, 2.25), facing=0)
walk('hamilton', T('2-18', 166.5), (1.4, 2.35), facing=-10)
# FILM ROUND (the clip at 167: he walks round her while she stands still and the couples dance round them both; she is
# still on purpose, as in the film, all number long)
walk('hamilton', T('2-18', 174.0), (1.25, 1.55), facing=-120, dwell=0)
walk('hamilton', T('2-18', 181.0), (0.05, 1.5), facing=150, dwell=0)
walk('hamilton', T('2-18', 188.0), (-0.45, 2.3), facing=100)
walk('hamilton', T('2-18', 198.0), (-0.1, 3.0), facing=40)
walk('hamilton', T('2-18', 204.0), (1.1, 2.75), facing=-60)
# the couple go to centre together
walk('eliza', T('2-18', 208.28), (-0.35, 0.95), facing=0)
walk('hamilton', T('2-18', 208.6), (0.35, 0.95), facing=-10)
hold('eliza', T('2-18', 215.86), 0)                  # she takes his hand without looking at him
hold('hamilton', T('2-18', 216.3), -35)              # his head to her shoulder
hold('eliza', T('2-18', 220.76), 75)                 # they hold each other
hold('hamilton', T('2-18', 221.1), -75)
hold('hamilton', T('2-18', 250.04), -20)
hold('eliza', T('2-18', 250.3), 20)
# they leave together, arm in arm
leave('hamilton', 'W-MSL', T('2-18', 260.8), speed=1.0, via=[(2.4, 0.45)])
leave('eliza', 'W-MSL', T('2-18', 260.8), speed=1.0, via=[(2.3, 1.05)])

# the company returns: the couples circle again, now counter-clockwise (the healthy direction, as Eliza's return begins
# the healing; SPOTLIGHT: on the outer ring, r 2.75, clear of the couple keyed at z 2.3), then open out to the sides and
# watch the forgiveness (ironinkpen: the company off to the sides, observing), and fall away (1140).
# REVIEW 2: the writer's standing ring and second lap are cut (invented).
R2 = 2.75
QU_SIDE = [(-3.65, -1.3), (-3.6, -0.1), (-3.65, 2.0), (-3.4, 3.0), (3.7, -1.2), (3.75, 0.0), (3.75, 1.2), (3.55, 2.4)]
for k, e in enumerate(QU):
    base = COUPLE[k // 2] + (20 if k % 2 else 0)
    p = clock(R2, base)
    ent, _ = ent_for(base)
    vq = [(-2.9, 3.4)] if ent == 'W-DSR' else None     # upstage of Angelica, who is on DSR now
    enter(e, ent, p, T('2-18', 167.2 + 2.0 * (k % 2)), face(p, C) - 90, speed=1.2, via=vq)
    circle(e, R2, base, base - 360, T('2-18', 169.6), T('2-18', 204.0), step=45)
QS = dict(zip(QU, hungarian([pos(e) for e in QU], QU_SIDE)))
for k, e in enumerate(QU):
    q = QS[e]
    walk(e, T('2-18', 208.0 + 0.3 * k), q, facing=face(q, C) * 0.8)
    ex = ('W-USR' if q[1] < 0.5 else 'W-DSR') if q[0] < 0 else ('W-USL' if q[1] < 0.5 else 'W-MSL')
    leave(e, ex, T('2-18', 250.04 + 0.4 * k), speed=1.0)

# =====================================================================================
# 2-19 THE ELECTION OF 1800   0.6 company look / 7.56 Jefferson DSR / 19.5 Burr UL /
# 36.04 Madison DR / 50.28 Burr's vamp / 65.05 Burr's campaign / 78.94 townspeople /
# 92.96 letters / 99.25 Hamilton UC / 107.13 split stage / 121.52 Burr meets Hamilton DSC /
# 141.64 deadlock / 152.37 to Hamilton / 157.94 Hamilton's endorsement /
# 184.92 Burr UL / 187.73 Jefferson wins / 201.77 Jefferson and Burr DC / 215.1 to the crowd /
# 229.72 band stops, Burr alone
# REVIEW: fan account (ironinkpen.tumblr.com, Act II): Jefferson and Madison open it (Madison enters wiping his eyes);
# Burr darts from person to person with pamphlets; the townspeople line up facing the house while Burr crouches and
# weaves between them; the company in two parallel lines facing each other, holding their letters out to Hamilton;
# Burr and Hamilton nearly alone for their exchange; Hamilton gives his endorsement from the centre of the upper level
# (the upstage gallery); Burr left alone on the deck.
# =====================================================================================
J = 'lafayette'; M = 'mulligan'
# FILM ROUND (2026-10-24; research/seg8.md "Film round"): the Disney+ clip read against the album clock. What it changed:
#  - the top (clip 5, the high wide): the stage EMPTY but for Jefferson walking on DSR and Madison at the centre; the
#    company comes on for Burr's vamp (clip 63.5: walking on SR as Burr works the room). Was: the eight on from 3.4.
#  - 21-28: both at the front, Madison SR and Jefferson SL of him, then face to face (Madison wiping his eyes).
#  - 63.5: Burr at the centre with Jefferson and Madison just SL of him, going up; 77: the company everywhere, dancing,
#    their papers overhead, Burr SR among them. Was: the eight standing still 3-79.
#  - 104: Hamilton at the CENTRE, his back to us, the company in two lines from the sides, down SR and SL, facing him.
#    Was: Hamilton UC at the head of an up-and-down alley.
#  - 124-148: the two men ALONE. Was: the company stood upstage through it.
#  - 152: the company back, bunched upstage centre, backs to us, looking up at Hamilton on the gallery; Jefferson and
#    Madison SL, Burr far SR (167: SR front, looking up). Was: Jefferson and Madison SR, Burr SL.
#  - 167: the company dancing (turns, arms out) mid-stage; 184.5: Burr at centre front, the company in an arc behind him.
#    Was: Burr up SL for the verdict.
# SPOTLIGHT: their apron specials (Jefferson ch2 at (-1.99, 3.58), Madison ch5 at (-0.97, 3.79)); the followspots now
# carry them when the film moves them off those.
J_DSR = (-2.3, 3.7); M_DR = (-1.1, 3.85)
enter(J, 'W-DSR', J_DSR, T('2-19', 5.0), 15, label='Jefferson')
enter(M, 'D-UC', (-0.4, 1.6), T('2-19', 6.8), -40, label='Madison')    # wiping his eyes
hold(J, T('2-19', 7.56), 15)
walk(M, T('2-19', 13.0), (-1.9, 3.6), facing=60)
walk(J, T('2-19', 14.0), (-0.2, 3.75), facing=20)
walk(J, T('2-19', 19.5), (0.9, 3.7), facing=-70)
walk(M, T('2-19', 27.0), (-0.55, 3.55), facing=90)        # face to face
hold(J, T('2-19', 27.4), -90)
walk(M, T('2-19', 36.04), M_DR, facing=-20)
walk(J, T('2-19', 37.0), (0.6, 3.3), facing=-40)
walk(J, T('2-19', 45.0), (1.4, 3.0), facing=-60)
walk(J, T('2-19', 56.0), (1.6, 0.2), facing=-80)          # up with Burr as he works the room
walk(M, T('2-19', 57.0), (0.8, -0.15), facing=-60)
walk(J, T('2-19', 79.0), (3.7, 1.0), facing=-70)          # the townspeople take the floor; J & M aside SL
walk(M, T('2-19', 79.6), (4.0, 1.9), facing=-80)
hold(J, T('2-19', 92.96), 160)                            # Madison urges the letter to Hamilton
hold(M, T('2-19', 93.5), -20)
J_SPLIT = (3.4, -0.5); M_SPLIT = (4.1, 0.4)
walk(J, T('2-19', 107.13), J_SPLIT, facing=-60)
walk(M, T('2-19', 107.6), M_SPLIT, facing=-70)
hold(J, T('2-19', 121.52), -100)
walk(J, T('2-19', 147.0), (2.6, 2.6), facing=-100)
walk(J, T('2-19', 152.37), (1.8, 3.3), facing=180)        # all eyes up to Hamilton
walk(M, T('2-19', 152.9), (4.0, 3.2), facing=-150)
walk(J, T('2-19', 190.5), (-0.5, 3.4), facing=0)          # Jefferson wins: to DC
hold(J, T('2-19', 201.77), 40)                            # with Burr
hold(J, T('2-19', 215.1), 180)                            # to the crowd
hold(J, T('2-19', 228.63), 0)
leave(J, 'W-DSR', T('2-19', 230.0))
walk(M, T('2-19', 195.0), (2.5, 3.5), facing=-80)
leave(M, 'W-DSL', T('2-19', 230.3))

B_UL = (4.2, -1.6)
enter('burr', 'W-USL', B_UL, T('2-19', 19.5), -30, label='Burr')
walk('burr', T('2-19', 30.0), (2.9, -0.7), facing=-60)    # FILM ROUND: he is never still, the pamphlet in his hand
walk('burr', T('2-19', 41.0), (3.7, 0.6), facing=-80)
# the vamp: Burr from voter to voter with his pamphlets, then the centre of their ring
# REVIEW 3 (video): the Disney+ clip's comments at its 1:06-1:08 (album ~61, the clip runs ~5 s ahead) laugh at Burr
# "walking on like a rectangle"; Blankenbuehler (Broadway Direct, 2020): "Most staging around Burr is linear. It's square."
# So his round of the voters is a rectangle of straight legs with square corners (a stop at each, his pamphlet to a voter):
# across between the two rows, down between the front-row voters, along the front, back up, and in to the centre.
for t, p, f in ((52.5, (2.7, 1.25), -90), (55.8, (-1.3, 1.25), -90), (57.6, (-1.3, 3.2), 90), (59.8, (1.3, 3.2), 90),
                (61.6, (1.3, 1.25), -90)):
    walk('burr', T('2-19', t), p, facing=f, dwell=0.3)
walk('burr', T('2-19', 62.6), C, facing=0)
hold('burr', T('2-19', 65.05), 0)                  # the company chants for him
walk('burr', T('2-19', 70.0), (-1.0, 1.8), facing=-60)   # FILM ROUND (77): SR among the dancing company
walk('burr', T('2-19', 76.0), (-2.0, 2.6), facing=30)
# the townspeople's line: he crouches and weaves behind it, lunges at the one who likes him
for t, p, f in ((81.5, (2.9, 2.45), 0), (84.0, (1.35, 2.45), 0), (86.5, (-0.35, 2.45), 0)):
    walk('burr', T('2-19', t), p, facing=f, dwell=0.5)
walk('burr', T('2-19', 88.5), (-1.65, 2.55), facing=0, dwell=1.0)
walk('burr', T('2-19', 91.5), (-3.6, 3.1), facing=60)
walk('burr', T('2-19', 103.5), (-1.3, 3.7), dwell=0)
walk('burr', T('2-19', 105.5), (1.3, 3.7), dwell=0)
walk('burr', T('2-19', 107.13), (2.2, 3.55), facing=-40)
walk('burr', T('2-19', 121.52), (0.8, 3.45), facing=-70)   # meets Hamilton DSC (film 124: SL of him; SPOTLIGHT: ch1 of 1162)
walk('burr', T('2-19', 130.0), (1.1, 3.0), facing=-80)
walk('burr', T('2-19', 138.0), (0.6, 3.6), facing=-70)
walk('burr', T('2-19', 145.0), (-2.3, 3.0), facing=40)     # FILM ROUND (152-167): far SR, then SR front
hold('burr', T('2-19', 158.5), face((-2.3, 3.0), (0.0, -3.35)))   # looks up at Hamilton's endorsement
walk('burr', T('2-19', 166.0), (-1.9, 2.5), facing=165)
walk('burr', T('2-19', 175.0), (-2.6, 3.3), facing=150)
walk('burr', T('2-19', 182.0), (0.0, 3.3), facing=0)       # FILM ROUND (184.5): centre front for the verdict
hold('burr', T('2-19', 184.92), 0)                 # the verdict on him
walk('burr', T('2-19', 188.5), (1.6, 2.6), facing=-60)
walk('burr', T('2-19', 201.77), (0.5, 3.4), facing=-40)
hold('burr', T('2-19', 215.1), -20)
walk('burr', T('2-19', 229.72), (0.7, 3.2), facing=0)  # alone in his special (ch1 at (0.87, 3.16))

# Hamilton: in for the letters at the CENTRE, his back to the house (FILM ROUND, 104), down to Burr, then up to the gallery
H_LET = (0.0, 1.0)
enter('hamilton', 'D-UC', (0.0, 0.3), T('2-19', 99.25), 0, speed=1.1)
walk('hamilton', T('2-19', 104.0), H_LET, facing=180)
hold('hamilton', T('2-19', 114.0), -100)
hold('hamilton', T('2-19', 118.0), 100)
walk('hamilton', T('2-19', 121.52), (-0.75, 3.45), facing=70)    # SPOTLIGHT: in ch4 of 1162
walk('hamilton', T('2-19', 128.0), (-0.45, 3.05), facing=85)
leave('hamilton', 'D-UC', T('2-19', 135.0), speed=1.3, via=[(0.0, 0.6), (0.0, -2.7)])   # up the middle
enter('hamilton', 'G-UC', (0.0, -3.35), T('2-19', 152.37), 0, ty='gallery')
hold('hamilton', T('2-19', 157.94), 0)
walk('hamilton', T('2-19', 168.0), (-0.7, -3.35), facing=10, y='gallery')    # FILM ROUND (167): a little SR of centre
walk('hamilton', T('2-19', 180.0), (0.2, -3.35), facing=0, y='gallery')      # (184.5): back to the centre
hold('hamilton', T('2-19', 184.92), 45)
leave('hamilton', 'G-UC', T('2-19', 188.5), speed=1.3)

# the voters: eight (REVIEW 2: fewer than the film's dozen, Jack's verdict). FILM ROUND: on for Burr's vamp, not at the top;
# they mill and dance with their papers (65-79), line up facing the house (80), make two lines from the sides to Hamilton at
# the centre (95), clear for the two men (121.5), come back bunched upstage under the gallery (150), dance mid-stage (160),
# make an arc behind Burr (182) and point at him when Jefferson wins (dance.py).
VOT = ENS[:8]
CROWD = [(-2.0, 2.3), (-0.65, 2.4), (0.65, 2.3), (2.0, 2.4),
         (-1.95, 0.1), (-0.65, 0.3), (0.65, 0.1), (1.95, 0.3)]
CROWD_ENT = ['W-DSR', 'W-DSR', 'W-DSL', 'W-DSL', 'W-USR', 'D-UC', 'D-UC', 'W-USL']
for k, e in enumerate(VOT):
    p = CROWD[k]
    enter(e, CROWD_ENT[k], p, T('2-19', 48.0 + 0.3 * k), face(p, C) * 0.5, speed=1.6, label='Ensemble %s' % e[3:])
    hold(e, T('2-19', 50.28 + 0.15 * k), face(p, C) * 0.5)          # Burr's vamp: they watch him work the room
def formation(t, spots, facing_fn, stagger=0.15):
    """move the eight from where they are to these spots (matched to keep paths short), arriving t + k*stagger."""
    dst = hungarian([pos(e) for e in VOT], spots)
    for k, e in enumerate(VOT):
        walk(e, t + stagger * k, dst[k], facing=facing_fn(dst[k]))
    return dict(zip(VOT, dst))
# the campaign: the room mills round Burr (FILM ROUND, 63.5-77)
formation(T('2-19', 67.5), [(-3.0, 1.2), (-1.6, 0.4), (-0.3, 2.7), (1.0, 1.9), (2.4, 0.6), (3.1, 2.5), (1.6, 3.4), (-2.9, 3.1)],
          lambda p: face(p, C), stagger=0.2)
formation(T('2-19', 73.5), [(-3.4, 1.9), (-1.0, 0.1), (0.5, 2.9), (1.7, 1.2), (3.0, 0.1), (2.7, 3.3), (-0.4, 3.7), (-1.2, 3.5)],
          lambda p: face(p, C) + 180, stagger=0.2)
# the townspeople: a line facing the house (ironinkpen)
formation(T('2-19', 80.0), [(-2.8 + 0.8 * i, 3.3) for i in range(8)], lambda p: 0, stagger=0.1)
# the letters: two lines from the sides down SR and SL, facing Hamilton at the centre, papers held out (FILM ROUND, 104)
LINES = [(-1.25 - 0.7 * i, 1.25 + 0.5 * i) for i in range(4)] + [(1.25 + 0.7 * i, 1.25 + 0.5 * i) for i in range(4)]
AL = formation(T('2-19', 97.0), LINES, lambda p: face(p, H_LET), stagger=0.15)
# REVIEW 3 (video): "Jon Rua getting all up in his face" (album ~101-111) - Rua is the Charles Lee body, ens3: out of his
# line into Hamilton's face, and back.
walk('ens3', T('2-19', 110.0), (0.05, 0.4), facing=0)
walk('ens3', T('2-19', 113.4), AL['ens3'], facing=face(AL['ens3'], H_LET))
# the two men's exchange: the company clears (FILM ROUND, 124-148 the two alone)
for k, e in enumerate(VOT):
    leave(e, 'W-USR' if last(e)['x'] < 0 else 'W-USL', T('2-19', 121.6 + 0.25 * k), speed=1.4)
# the endorsement: they come back bunched under the gallery, backs to the house, looking up at him (FILM ROUND, 152)
UNDER = [(-1.4, -0.9), (-0.7, -1.0), (0.0, -0.9), (0.7, -1.0), (1.4, -0.9), (-1.0, -0.2), (0.0, -0.25), (1.0, -0.2)]
for k, e in enumerate(VOT):
    p = UNDER[k]
    ent = 'W-USR' if p[0] < -0.3 else ('W-USL' if p[0] > 0.3 else 'D-UC')
    enter(e, ent, p, T('2-19', 150.0 + 0.3 * k), 180, speed=1.4, label='Ensemble %s' % e[3:])
    hold(e, T('2-19', 157.94 + 0.1 * k), 180)                         # up to Hamilton on the gallery
# they dance out mid-stage (FILM ROUND, 167: turns, arms out), and make an arc behind Burr for the verdict (184.5)
formation(T('2-19', 162.0), [(-3.0, 0.6), (-1.8, 1.6), (-0.6, 0.6), (0.6, 1.6), (1.8, 0.6), (3.0, 1.6), (-1.0, 2.6), (0.9, 2.5)],
          lambda p: 0, stagger=0.2)
formation(T('2-19', 170.0), [(-3.2, 1.4), (-2.0, 0.4), (-0.8, 1.6), (0.4, 0.5), (1.6, 1.7), (2.9, 0.5), (-0.1, 2.5), (2.6, 2.2)],
          lambda p: 0, stagger=0.2)
ARC19 = [(-3.6, 2.6), (-2.6, 2.0), (-1.5, 1.6), (-0.5, 1.45), (0.5, 1.45), (1.5, 1.6), (2.6, 2.0), (3.6, 2.6)]
formation(T('2-19', 182.0), ARC19, lambda p: 0, stagger=0.1)
for k, e in enumerate(VOT):
    q = pos(e)
    hold(e, T('2-19', 191.0 + 0.12 * k), face(q, (-0.5, 3.4)) * 0.8)   # Jefferson wins: to him
for k, e in enumerate(VOT):
    x = last(e)['x']
    ex = 'W-USR' if x < -0.5 else 'W-USL'
    leave(e, ex, T('2-19', 223.5 + 0.3 * k), speed=1.5)    # gone before the band stops (229.72): Burr alone

# =====================================================================================
# 2-20 YOUR OBEDIENT SERVANT   0.2 Burr in a steel shaft / 17.38 the steel fan /
# 28.44 tight on Burr / 32.54 minuet, Burr's desk centre / 38.59 he writes / 67.44 the letter goes /
# 74.81 Hamilton replies / 92 Burr's aside / 102.18 the reply goes / 111.09 escalates /
# 119.69 / 128.19 the challenge / 134.46 / 136.61 both sign, the company surrounds them /
# 147.68 blackout
# REVIEW: fan account (ironinkpen): ONE desk at centre that both men use - Burr at it first, an ensemble member carries
# his letter to Hamilton, Hamilton takes the desk to write his list while Burr stands SL and several of the company
# bring Burr the long letter a page at a time; for Weehawken one of the company stands SL and one SR staring out.
# The film editor: the company leans toward the two men.
# =====================================================================================
DESK = (0.0, 0.6)
# FILM ROUND (2026-10-24; research/seg8.md "Film round"): the Disney+ clip against the album clock.
#  - 31.4: Burr centre, four dancers crouched round him in red; 40-47: the company dancing hard round the desk he sits at
#    (lunges, turns, a slide). Was: the six walked to the sides at 33.5 and stood.
#  - 91-93: Burr stands SR, Hamilton at the desk, the company behind the desk with him (one waving a page). Was: Burr SL.
#  - 115: Hamilton up from the desk, standing SR of centre, Burr centre-SL; 129-147: Hamilton in a pool DSR, Burr in a
#    pool DSL, a second beside each from 142, the company in a line upstage, facing out. Was: Hamilton at the desk to the
#    blackout, Burr SL from 73, the company at the sides.
B_SR = (-2.7, 2.7); B_SL = (2.3, 3.2); H_SR = (-2.3, 3.2)
walk('burr', T('2-20', 9.0), (-0.35, 3.05), facing=-20)     # the rant (SPOTLIGHT: inside his steel shaft ch93)
walk('burr', T('2-20', 17.38), (0.0, 2.2), facing=0)
walk('burr', T('2-20', 32.54), DESK, facing=0)              # sits at the desk centre
hold('burr', T('2-20', 67.44), 0)                           # signs
hold('burr', T('2-20', 70.0), 0)
walk('burr', T('2-20', 72.5), (-1.6, 0.0), facing=-120, dwell=0)   # up round behind Hamilton coming to the desk
walk('burr', T('2-20', 77.0), B_SR, facing=75)              # gives up the desk, stands SR (FILM ROUND, 91)
hold('burr', T('2-20', 92.0), 80)                           # his aside, towards Hamilton
walk('burr', T('2-20', 99.0), (-1.2, 2.55), facing=40)
walk('burr', T('2-20', 111.0), (0.9, 2.6), facing=-80)      # (115: centre-SL)
walk('burr', T('2-20', 128.5), B_SL, facing=-80)            # the challenge, in the DSL pool (129)
hold('burr', T('2-20', 136.61), -10)
leave('burr', 'W-DSL', T('2-20', 148.0), speed=1.3)

enter('hamilton', 'W-DSR', (-2.4, 2.5), T('2-20', 70.0), 60, speed=1.3)
walk('hamilton', T('2-20', 74.81), DESK, facing=0)         # takes the desk, writes his list
walk('hamilton', T('2-20', 116.0), (-1.4, 2.0), facing=60)  # FILM ROUND (115): up from the desk
hold('hamilton', T('2-20', 119.69), 80)                     # refuses: towards Burr
walk('hamilton', T('2-20', 128.5), H_SR, facing=60)         # in the DSR pool (129)
hold('hamilton', T('2-20', 136.61), 10)

# REVIEW 2: six of the company, from the sides. REVIEW 3 (video): on for Burr's rant, swaying (dance.py); the Bullet (ens1)
# brings Burr his quill (album ~41); Charles Lee (ens3) holding his side (~60.5); ens7 teases Burr with the last page.
# FILM ROUND: three SR (the page-bringers, since Burr now stands SR) and three SL; they dance round the desk 38-47.
OS_HOME = {'ens7': (-3.9, -0.9), 'ens8': (-4.1, 0.3), 'ens9': (-3.95, 1.5),
           'ens1': (3.7, -0.7), 'ens6': (3.5, 0.55), 'ens10': (4.25, 2.35)}
OS_ENT = {'ens7': 'W-USR', 'ens8': 'W-USR', 'ens9': 'W-DSR', 'ens1': 'W-USL', 'ens6': 'W-MSL', 'ens10': 'W-DSL'}
OS_FAN = [clock(3.0, a) for a in (300, 330, 15, 40, 65, 90)]
FAN = dict(zip(OS_HOME, hungarian([OS_HOME[e] for e in OS_HOME], OS_FAN)))
for k, e in enumerate(OS_HOME):
    p = FAN[e]
    enter(e, OS_ENT[e], p, T('2-20', 16.4 + 0.3 * k), face(p, (0.0, 2.2)), speed=1.3, label='Ensemble %s' % e[3:])
# FILM ROUND (40): in round the desk to dance (dance.py), then out to their places at the sides
DRING = [clock(2.0, a, (0.0, 0.9)) for a in (250, 295, 335, 25, 65, 110)]
DR = dict(zip(OS_HOME, hungarian([pos(e) for e in OS_HOME], DRING)))
for k, e in enumerate(OS_HOME):
    walk(e, T('2-20', 35.0 + 0.2 * k), DR[e], facing=face(DR[e], DESK))
walk('ens1', T('2-20', 38.4), (0.6, 0.45), facing=-90, dwell=0.8)      # the quill, from his SL side
walk('ens1', T('2-20', 41.0), DR['ens1'], facing=face(DR['ens1'], DESK))
for k, e in enumerate(OS_HOME):
    p = OS_HOME[e]
    walk(e, T('2-20', 49.0 + 0.4 * k), p, facing=face(p, DESK) * 0.6)
enter('ens3', 'W-USR', (-2.8, -2.0), T('2-20', 60.5), 70, speed=1.0, label='Charles Lee')
leave('ens3', 'W-USR', T('2-20', 63.0), speed=1.2, label='Ensemble 3')
# the courier: ens6 takes Burr's letter from the desk across to Hamilton
cr = 'ens6'
walk(cr, T('2-20', 67.6), (0.55, 1.1), dwell=0.6, facing=-120)
walk(cr, T('2-20', 70.8), (-1.75, 2.2), facing=-110, dwell=0.8)
walk(cr, T('2-20', 76.5), OS_HOME[cr], facing=face(OS_HOME[cr], DESK))
# the pages of Hamilton's list, brought to Burr one at a time (now from SR, where he stands)
for e, t, stop in (('ens7', 79.5, (-2.1, 2.3)), ('ens8', 83.5, (-2.15, 3.2)), ('ens9', 87.5, (-2.3, 2.0))):
    home = OS_HOME[e]
    walk(e, T('2-20', t), stop, facing=face(stop, B_SR), dwell=0.8)
    walk(e, T('2-20', t + 4.2), home, facing=face(home, DESK))
# FILM ROUND (93): two stand behind his desk as he writes (they sway, dance.py)
walk('ens1', T('2-20', 78.0), (0.85, -0.35), facing=0)
walk('ens10', T('2-20', 79.0), (-0.85, -0.4), facing=0)
# Hamilton's signed reply goes across: ens7 takes it from the desk; "hands burr the paper then takes it away then gives it
# back and laughs at him" (REVIEW 3, the clip at ~100-108)
walk('ens7', T('2-20', 103.2), (-0.6, 1.05), dwell=0.6, facing=120)
walk('ens7', T('2-20', 105.6), (-0.65, 2.2), facing=-110)
walk('ens7', T('2-20', 106.6), (-0.3, 1.95), facing=-110)            # snatches it back
walk('ens7', T('2-20', 107.6), (-0.65, 2.2), facing=-110, dwell=0.4)  # and gives it again
walk('ens7', T('2-20', 111.2), OS_HOME['ens7'], facing=face(OS_HOME['ens7'], DESK))
walk('ens1', T('2-20', 109.0), OS_HOME['ens1'], facing=face(OS_HOME['ens1'], DESK))
walk('ens10', T('2-20', 109.5), OS_HOME['ens10'], facing=face(OS_HOME['ens10'], DESK))
# 111.09 escalates: the country leans in (half a metre toward the desk)
for k, e in enumerate(OS_HOME):
    h = OS_HOME[e]; d = math.hypot(DESK[0] - h[0], DESK[1] - h[1])
    q = (h[0] + 0.5 * (DESK[0] - h[0]) / d, h[1] + 0.5 * (DESK[1] - h[1]) / d)
    walk(e, T('2-20', 113.0 + 0.3 * k), q, facing=face(q, DESK))
# FILM ROUND (129): the jury, a line upstage facing out; (142) a second beside each man for Weehawken
JURY = [(-3.5, -1.6), (-2.1, -1.7), (-0.7, -1.75), (0.7, -1.75), (2.1, -1.7), (3.5, -1.6)]
JY = dict(zip(OS_HOME, hungarian([pos(e) for e in OS_HOME], JURY)))
for k, e in enumerate(OS_HOME):
    walk(e, T('2-20', 126.0 + 0.3 * k), JY[e], facing=0)
SECONDS = {'ens8': (H_SR[0] + 0.75, H_SR[1] + 0.15), 'ens6': (B_SL[0] + 0.75, B_SL[1] + 0.15)}
for e, p in SECONDS.items():
    walk(e, T('2-20', 140.5), p, facing=0)
for k, e in enumerate(OS_HOME):
    hold(e, T('2-20', 141.5 + 0.1 * k), 0)

# =====================================================================================
# 2-21 BEST OF WIVES AND BEST OF WOMEN   0.44 pre-dawn, Hamilton at his desk / 7.72 Eliza behind him /
# 19.96 her plea / 34.9 she goes / 40.16 Hamilton alone / 44.0 FTB
# REVIEW: fan account (ironinkpen): Hamilton at a desk near SR; Eliza comes up behind him and puts her arms round him;
# she starts back to bed and he catches her hand to stop her for his last words.
# =====================================================================================
for k, e in enumerate(OS_HOME):
    s = (last(e)['x'], last(e)['z'])
    if s[0] < -0.5 and s[1] < 0.5: ex = 'W-USR'
    elif s[0] < -0.5: ex = 'W-DSR'
    elif s[0] > 3.3: ex = 'W-MSL'
    elif s[0] > 0.5 and s[1] > 1.0: ex = 'W-DSL'
    elif s[0] > 0.5: ex = 'W-MSL'
    else: ex = 'D-UC'
    leave(e, ex, T('2-20', 148.0 + 0.2 * k), speed=1.5)
H_DESK = (-2.8, 2.6)
walk('hamilton', T('2-21', 0.44), H_DESK, facing=0)          # the desk, now near SR, in the dark
E_BEHIND = (-2.6, 1.6)      # REVIEW 2: behind his chair (props.py), not in it
# FILM ROUND (the clip at 8.4: she stands apart SR of him, watching him write; 21: behind his chair, her arms round him;
# 38: standing at his SR side, he holding her hand). Was: straight in behind him at 7.72, then at his side for the plea.
enter('eliza', 'W-DSR', (-4.2, 2.3), T('2-21', 7.72), 80, speed=1.3)
walk('eliza', T('2-21', 16.5), E_BEHIND, facing=10)            # behind him; her arms round him (dance.py comfort)
hold('hamilton', T('2-21', 21.0), 40)
walk('eliza', T('2-21', 35.6), (-2.3, 1.6), dwell=0)              # starts back to bed, round behind his chair;
walk('eliza', T('2-21', 36.6), (-3.3, 1.45), facing=40)           # he catches her hand
hold('hamilton', T('2-21', 35.5), -70)
hold('hamilton', T('2-21', 40.16), -30)
leave('eliza', 'W-DSR', T('2-21', 41.0), speed=1.1)
# REVIEW 2: he stays at the desk through the FTB: The World Was Wide Enough opens with him rising from his chair, where he
# has been writing to Eliza (hamilton-lyrics, "The World Was Wide Enough staging")

# =====================================================================================
# 2-22 THE WORLD WAS WIDE ENOUGH   3.1 the count begins / 9.84 Burr narrates SL /
# 21.86 Hamilton surveys the ground SR / 34.45 his place / 46.18 Philip's ground UR /
# 58.5 Burr's confession / 71.42 Hamilton / 83.13 Burr's daughter / 94.36 the count /
# 101.42 FIRE (freeze) / 103.42 the monologue / 129.9 Hamilton DR / 142.4 centre pose /
# 149.9 to centre / 151.8 off the box / 155.46 eyes up / 162.5 Philip UR / 166.46 GW UL steps /
# 168.94 restore / 174.5 Eliza / 185.28 the fight / 191.18 the shot / 200.67 Burr ushered SL /
# 206.92 Hamilton rowed away / 215.22 the city mourns / 239.22 Burr DSC / 252.44 the replay /
# 266.44 Burr centre / 281.83 tight / 292.8 FTB
# REVIEW: fan accounts of the Broadway staging (hamilton-lyrics.tumblr.com "The World Was Wide Enough staging";
# ironinkpen, Act II) and the cast/swing posts on BroadwayWorld: Hamilton and his second come down from upstage right,
# Burr and his second to SL; the seconds meet at centre; Philip appears and walks away upstage before Hamilton can reach
# him; at the count the company clears and the duellists meet at centre and turn; the Bullet catches Burr's shot and
# drifts slowly TOWARD CENTRE along the line between the men; the company returns for the monologue (dancing behind
# Hamilton DR, a pose round him on the box, a pose round the Bullet at centre, then blown out to the edges as if by an
# explosion); Washington appears beside him and runs up to the upper level; Philip is up on the bridge; Eliza takes
# his hand, pulls him to centre, then walks off diagonally upstage right; the company scatters, leaving the two men;
# after the shot an ensemble member holds Burr back, two others sit either side of Hamilton miming rowing while the
# platform turns; Hamilton rises facing upstage with Eliza and Angelica either side of him and walks up the stairs
# towards the bridge; the company mirrors the women, turns out, closes round Burr DSC and falls back; all leave but Burr.
# =====================================================================================
# SPOTLIGHT (seg 8 spotlight agent), from Binkley's real 1238-1270 chain in hamilton-eos.json:
#  - FIRE (1242): the duel pools of preset 1123 - ch17 (-2.10, 0.26) and ch19 (3.12, 3.02): Hamilton SR, Burr SL
#  - before the count: Hamilton's SR shaft ch11 (-2.38, 1.69), Burr's SL special ch2 (3.0, 2.75)
#  - the monologue: Burr's own pool, preset 1126 "Burr", ch19 at (2.71, -0.04) from 1248 (full in 1250); the turntable
#    has carried him round; ch49 (-0.69, 1.53) is up near the centre 129.9-149.9 (the Bullet's hold)
#  - the box: preset 24 "DSC -Z-", ch43 (0.0, 3.43)
#  - ELIZA / "Freedom" Fight / the shot (1262-1270): ch12 preset 1130 (-2.0, -0.99) and ch91 preset 1137 (-2.68, -1.93)
#    SR-upstage, ch14/ch95 preset 1137 (2.26, 3.65)/(1.57, 3.43) DSL: the duel line has turned. Kept on the ruled
#    sides (Hamilton SR, Burr SL), Hamilton takes the SR-upstage pools and Burr the DSL ones.
HD = (-2.1, 0.35)                 # FIRE, in ch17
BD = (3.05, 2.95)                 # FIRE, in ch19 (and his SL special ch2 before the count)
H_PLACE = (-2.45, 1.55)           # his place before the count, in ch11
B_MON = (2.71, -0.04)             # Burr in the monologue, ch19 / preset 1126
H_SHOT = (-2.2, -1.15)            # at the shot, ch12 / ch91
B_SHOT = clock(2.85, 146)         # at the shot, ch95 / ch14
BULLET_HOLD = (-0.4, 1.2)         # ch49, near the turntable's centre
_L = math.hypot(BD[0] - HD[0], BD[1] - HD[1])
_U = ((BD[0] - HD[0]) / _L, (BD[1] - HD[1]) / _L)
_MID = ((HD[0] + BD[0]) / 2, (HD[1] + BD[1]) / 2)
H_CNT = (_MID[0] - 0.3 * _U[0], _MID[1] - 0.3 * _U[1]); B_CNT = (_MID[0] + 0.3 * _U[0], _MID[1] + 0.3 * _U[1])
B_PISTOL = (BD[0] - 0.65 * _U[0], BD[1] - 0.65 * _U[1])
def arc(a, c0, c1, r0, r1, t0, t1, n, end_facing):
    """carried by the turntable from angle c0 to c1 (degrees, round C) while the radius goes r0 -> r1"""
    if A[a][-1]['_T'] < t0 - 0.05:
        w = A[a][-1]; wpa(a, t0, w['x'], w['z'], facing=w.get('facing'), dwell=0)
    else:
        A[a][-1]['dwell'] = 0
    for k in range(1, n + 1):
        f = k / n; x, z = clock(r0 + (r1 - r0) * f, c0 + (c1 - c0) * f)
        if k < n: wpa(a, t0 + (t1 - t0) * f, x, z, dwell=0)
        else: wpa(a, t1, x, z, facing=end_facing)
# the company comes on with the duel music, a sombre upstage arc
ARC22 = {'ens5': 330, 'ens6': 350, 'ens7': 10, 'ens8': 30, 'ens9': 50, 'ens10': 70}
for k, (e, a) in enumerate(ARC22.items()):
    p = clock(3.5, a)
    ent = 'W-USR' if a > 300 else ('D-UC' if a < 40 else 'W-USL')
    enter(e, ent, p, T('2-22', 5.0 + 0.8 * k), face(p, C) * 0.6, speed=1.3, label='Ensemble %s' % e[3:])
# FILM ROUND (no clip for 2-22): the arc does not stand 90 s - it walks slowly a quarter-turn's worth round the ring and
# back as the duel is set (invented, slow; hamilton-lyrics has the platform turning through the number)
for k, (e, a) in enumerate(ARC22.items()):
    circle(e, 3.5, a, a + 22, T('2-22', 24.0), T('2-22', 46.0), step=11, end_facing=face(clock(3.5, a + 22), C) * 0.6)
    circle(e, 3.5, a + 22, a, T('2-22', 64.0), T('2-22', 88.0), step=11, end_facing=face(clock(3.5, a), C) * 0.6)
# Burr and Van Ness (ens2) come on SL
enter('burr', 'W-MSL', (3.2, 2.3), T('2-22', 9.84), -40, label='Burr')
enter('ens2', 'W-MSL', (3.85, 1.3), T('2-22', 11.4), -60, label='Ensemble 2')
# Hamilton and Pendleton (ens3) walk down from upstage right; the Doctor (ens4) follows
# REVIEW 2: Hamilton rises from the desk DR (hamilton-lyrics), goes round it and up to UR, and comes down with his second;
# the Doctor (ens4) and Pendleton (ens3) take the desk and the chair off SR first (props.py)
hold('hamilton', T('2-22', 3.6), 0, dwell=0.6)
walk('hamilton', T('2-22', 6.0), (-2.0, 1.95), facing=-150)
walk('hamilton', T('2-22', 17.0), (-2.6, -1.2), facing=160)
# NOTES3 (Jack, 2026-10-15): "the ham desk should come off during the blackout at the end of this [2-21]" - the desk is
# struck in the 2-21 FTB (props.py), so the Doctor (ens4) no longer walks on at 6.6 to take it; Pendleton (ens3) still
# takes the chair
enter('ens3', 'W-DSR', (-3.45, 2.15), T('2-22', 8.6), 90, speed=1.6, label='Ensemble 3')
leave('ens3', 'W-DSR', T('2-22', 9.0), speed=1.6, via=[(-4.0, 3.2)])
enter('ens3', 'W-USR', (-3.3, -0.85), T('2-22', 18.6), 160, label='Ensemble 3')
enter('ens4', 'W-USR', (-3.3, -0.6), T('2-22', 25.0), 60, label='The Doctor')
walk('hamilton', T('2-22', 21.86), (-2.65, 1.95), facing=-30)   # surveys the ground SR (in ch11)
walk('ens3', T('2-22', 22.8), (-3.75, 0.6), facing=60)
hold('burr', T('2-22', 22.5), -60)
walk('burr', T('2-22', 27.0), (3.3, 3.2), facing=-25)
walk('hamilton', T('2-22', 26.0), (-3.3, 3.0), facing=40)
walk('hamilton', T('2-22', 31.0), (-2.2, 3.4), facing=-20)
walk('hamilton', T('2-22', 34.45), H_PLACE, facing=face(H_PLACE, BD))
walk('burr', T('2-22', 34.45), BD, facing=face(BD, H_PLACE))
# FILM ROUND (no clip for 2-22): Burr keeps moving while he narrates (hamilton-lyrics: "Hamilton freezes while Burr keeps
# moving"), a few straight legs SL before his confession
walk('burr', T('2-22', 44.0), (3.7, 2.2), facing=-70)
walk('burr', T('2-22', 52.0), (3.0, 3.5), facing=-40)
walk('ens2', T('2-22', 27.0), (3.75, 0.55), facing=face((3.75, 0.55), BD))
# the seconds meet at centre and check the pistols, then go back
walk('ens2', T('2-22', 40.0), (0.4, 0.95), facing=-90)
walk('ens3', T('2-22', 40.3), (-0.4, 0.95), facing=90)
hold('ens2', T('2-22', 43.5), -90)
walk('ens2', T('2-22', 47.0), (3.75, 0.55), facing=face((3.75, 0.55), BD))
walk('ens3', T('2-22', 47.0), (-3.75, 0.6), facing=60)
# Philip's ground: Philip appears UR; Hamilton goes to him; he turns and walks away upstage
# SPOTLIGHT: the "philip" preset (1167, ch19) is caught by the upstage gallery at (-2.32, -3.32): he appears up there,
# on the bridge, as he does again for "Phillip UR"
enter('laurens', 'G-UC', (-2.35, -3.35), T('2-22', 46.18), 20, label='Philip', ty='gallery')
walk('hamilton', T('2-22', 49.0), (-2.5, -1.0), facing=180)
leave('laurens', 'G-UC', T('2-22', 52.5), speed=1.1)
walk('hamilton', T('2-22', 56.0), H_PLACE, facing=face(H_PLACE, BD))
walk('burr', T('2-22', 58.5), (2.6, 3.4), facing=-15)   # his confession, out to us
# REVIEW 3 (hamilton-lyrics' staging account, re-read for this pass): for the last chance to negotiate the seconds step into
# a pool at centre; Hamilton freezes while Burr keeps moving; Burr crosses toward Hamilton CUTTING THROUGH the seconds, who
# kneel as he passes; he points and shouts at Hamilton; he goes back past them and they rise. The seconds face each other
# across Burr's line (z 0.95) so he passes between them; Burr's legs are straight, with stops (his rule).
walk('ens2', T('2-22', 66.0), (0.0, 0.3), facing=0)
walk('ens3', T('2-22', 66.3), (0.0, 1.6), facing=180)
walk('burr', T('2-22', 72.9), (1.6, 1.0), facing=-90)   # reads Hamilton: toward him
walk('burr', T('2-22', 75.0), (-0.9, 1.0), facing=-95)  # through the seconds; points at him (dance.py)
hold('hamilton', T('2-22', 72.0), 75)
walk('burr', T('2-22', 79.5), (1.6, 1.0), facing=90)    # back past them
walk('burr', T('2-22', 83.13), (3.1, 3.3), facing=0)    # his daughter
walk('ens2', T('2-22', 87.0), (3.75, 0.55), facing=face((3.75, 0.55), BD))
walk('ens3', T('2-22', 87.3), (-3.75, 0.6), facing=60)
# the count: the company clears; the two meet at centre and pace out
walk('hamilton', T('2-22', 94.36), H_CNT, facing=face(H_CNT, HD))
walk('burr', T('2-22', 94.36), B_CNT, facing=face(B_CNT, BD))
walk('hamilton', T('2-22', 100.6), HD, facing=face(HD, BD))
walk('burr', T('2-22', 100.6), BD, facing=face(BD, HD))
# the turntable carries the frozen Burr round to his monologue pool, and later on to the DSL end of the line
arc('burr', ang_of(BD), ang_of(B_MON), rad_of(BD), rad_of(B_MON), T('2-22', 104.0), T('2-22', 128.0), 4, face(B_MON, (-3.5, 3.4)))
# REVIEW 3: Blankenbuehler (Playbill; Broadway Direct): "in the duel ... the person who kills him always rotates the wrong
# way" - the killer turns with inevitability, COUNTER-clockwise; "when Hamilton dies, he turns right" (clockwise). The
# second leg used to run clockwise (70 -> 146 deg). hamilton-lyrics: the turntable stops while Hamilton is on the box and
# starts again on the phrase after it (151.8, off the box), Burr carried "to downstage right". So the platform carries
# the frozen Burr on round counter-clockwise from 151.8: up past 12 o'clock, down the SR side (Binkley's own "Burr R" preset
# is up at ELIZA, 1262), across the front, to the DSL end of the line for the shot - the ruled sides are kept.
arc('burr', ang_of(B_MON), 146 - 360, rad_of(B_MON), 2.85, T('2-22', 151.8), T('2-22', 187.0), 12, face(B_SHOT, H_SHOT))
BURR_RIDE = [clock(2.85, a) for a in range(185, 260, 8)]   # the part of his ride that passes the blown-out company
leave('ens2', 'W-MSL', T('2-22', 94.4), speed=1.2)
leave('ens3', 'W-USR', T('2-22', 94.4), speed=1.2)
leave('ens4', 'W-USR', T('2-22', 94.6), speed=1.2)
for k, (e, a) in enumerate(ARC22.items()):
    leave(e, 'W-USR' if a > 300 else ('D-UC' if a < 40 else 'W-USL'), T('2-22', 94.4 + 0.3 * k), speed=1.2)

# The Bullet: catches the shot at Burr's pistol at FIRE, drifts slowly along the line to centre, then on to Hamilton
BL = 'ens1'
enter(BL, 'W-USL', B_PISTOL, T('2-22', 100.4), face(B_PISTOL, HD), speed=1.0, label='The Bullet')
hold(BL, T('2-22', 101.42), face(B_PISTOL, HD), dwell=0)
# REVIEW 3 (video text): she never stops - Dance Magazine, "she traverses across the stage toward him in slow motion";
# hamilton-lyrics: "the bullet creeps closer throughout", and "at 'eyes up' the bullet girl reaches center" (155.46), where
# the company poses round her and lifts her (Blankenbuehler, Broadway Direct: "every cast member joins her to help slow
# down the bullet"). Was: at the centre by 129.0 and held there 40 s. Now a steady creep of about 0.06 m/s, through ch49's
# pool near the centre (lit 129.9-149.9, (-0.69, 1.53)), to the centre at "Eyes UP"; held in the knot until ELIZA (174.5),
# when the knot is blown away; then on to him for the shot.
walk(BL, T('2-22', 129.9), (0.6, 1.75), facing=face((0.6, 1.75), HD), dwell=0)
walk(BL, T('2-22', 149.9), (-0.45, 1.5), facing=face((-0.45, 1.5), HD), dwell=0)
walk(BL, T('2-22', 155.46), BULLET_HOLD, facing=face(BULLET_HOLD, HD), dwell=19.0)
walk(BL, T('2-22', 191.18), (-1.75, -0.6), facing=face((-1.75, -0.6), H_SHOT))
leave(BL, 'W-DSR', T('2-22', 193.0), speed=1.3)

# Hamilton's monologue: he moves through the frozen picture
hold('hamilton', T('2-22', 103.42), face(HD, BD))
walk('hamilton', T('2-22', 115.0), (-2.7, 3.6), facing=20)
walk('hamilton', T('2-22', 129.9), (-3.5, 3.4), facing=15)     # Legacy / Hamilton DR, off the turntable
walk('hamilton', T('2-22', 140.4), (-2.0, 4.7), dwell=0)
walk('hamilton', T('2-22', 142.4), (0.0, 3.45), facing=0)      # "America" centre pose (on a box), preset 24
hold('hamilton', T('2-22', 149.9), 0)
H_EYES = (1.5, 3.75)
walk('hamilton', T('2-22', 153.0), (0.7, 3.95), facing=0)      # off the box
walk('hamilton', T('2-22', 155.46), H_EYES, facing=160)        # eyes up
hold('hamilton', T('2-22', 162.5), face(H_EYES, (-3.0, -3.35)))     # Philip on the bridge
hold('hamilton', T('2-22', 166.46), face(H_EYES, (3.35, -2.45)))    # Washington on the SL steps
hold('hamilton', T('2-22', 168.94), 0)
hold('hamilton', T('2-22', 174.5), -120)                       # Eliza
walk('hamilton', T('2-22', 176.5), (0.95, 2.6), facing=-110)   # she pulls him to centre
walk('hamilton', T('2-22', 185.0), (-2.6, 1.0), dwell=0)       # the fight: back to his place
walk('hamilton', T('2-22', 188.0), H_SHOT, facing=face(H_SHOT, B_SHOT))   # aims at the sky
H_HIT = (-2.4, -0.85)
walk('hamilton', T('2-22', 193.38), H_HIT, facing=40)          # hit
# Washington appears beside him, then runs up the SL stair: on the steps for "GW UL Steps", off along the gallery
enter('washington', 'W-DSL', (2.3, 3.0), T('2-22', 160.0), -90, speed=1.6, label='Washington')
walk('washington', T('2-22', 161.0), (2.3, 3.0), facing=-120, dwell=0)
walk('washington', T('2-22', 162.0), (1.75, 1.8), dwell=0)
walk('washington', T('2-22', 163.6), (1.9, -0.6), dwell=0)
walk('washington', T('2-22', 164.6), (2.2, -2.45), dwell=0)
wpa('washington', T('2-22', 166.46), 3.35, -2.45, y='top', facing=-30, dwell=3.0)
wpa('washington', T('2-22', 171.5), 4.5, -2.45, y='gallery', dwell=0)
wpa('washington', T('2-22', 172.3), 4.5, -3.3, y='gallery', dwell=0)
wpa('washington', T('2-22', 175.5), 0.6, -3.35, y='gallery', dwell=0)
wpa('washington', T('2-22', 176.7), 0.6, -4.8, y='gallery', off=True)
# Philip up on the bridge
wpa('laurens', T('2-22', 158.9), 0.6, -4.8, y='gallery', off=True, dwell=0)
wpa('laurens', T('2-22', 160.0), 0.6, -3.35, y='gallery', dwell=0)
wpa('laurens', T('2-22', 162.5), -3.0, -3.35, y='gallery', facing=20)
wpa('laurens', T('2-22', 169.0), -3.0, -3.35, y='gallery', facing=20, dwell=0)
wpa('laurens', T('2-22', 171.8), 0.6, -3.35, y='gallery', dwell=0)
wpa('laurens', T('2-22', 172.9), 0.6, -4.8, y='gallery', off=True)
# Eliza: in from upstage SL, takes his hand and pulls him to centre, then walks off diagonally upstage right
enter('eliza', 'W-USL', (0.85, 2.45), T('2-22', 174.0), 60, speed=1.4)
walk('eliza', T('2-22', 176.5), (0.3, 2.1), facing=75)
walk('eliza', T('2-22', 181.0), (-0.6, -0.9), dwell=0)
leave('eliza', 'W-USR', T('2-22', 181.1), speed=1.3)

# the company in the monologue. REVIEW 2, against ETC's THPP renders of Binkley's real cues and hamilton-lyrics: in
# 1248 "Legacy/ Hamilton DR" a handful stand in pools round the outer ring behind him (the writer's 3x3 block DR is cut);
# at the box ("America" Center pose, 1250) they make the My Shot pose round him (hamilton-lyrics); in 1254 "to center"
# and 1256 they stand in a ring round the centre; in 1258 "Eyes UP" to 1260 Restore they are one tight knot at the
# centre round the Bullet (who is lifted); then they are blown out to the edges and scatter before the shot. Eight, not
# nine: ens10 is used only for the 'mum' figure on the gallery; ens9 brings the box on, poses, and takes it off as
# Hamilton steps down, so the ring and the knot are seven.
MON = ['ens2', 'ens3', 'ens4', 'ens5', 'ens6', 'ens7', 'ens8']
BEHIND = [clock(3.5, a) for a in (245, 280, 315, 350, 25, 95, 125)]
def mon_ent(p):
    a = ang_of(p)
    if a >= 330 or a < 60: return 'D-UC'
    if a < 110: return 'W-MSL'
    if a < 180: return 'W-DSL'
    return 'W-USR'
BH = dict(zip(MON, BEHIND))
for k, e in enumerate(MON):
    p = BH[e]
    enter(e, mon_ent(p), p, T('2-22', 122.0 + 1.1 * k), face(p, C) * 0.3, label='Ensemble %s' % e[3:])
# the box: ens9 brings it on from SL and sets it DSC (preset 24's spot), then joins the pose
BOX = (0.0, 3.45)
enter('ens9', 'W-DSL', (0.6, 3.05), T('2-22', 137.0), -60, speed=1.3, label='Ensemble 9')
MON = MON + ['ens9']
POSE = [clock(1.4, a, BOX) for a in (-60, -20, 20, 60)] + [clock(2.2, a, BOX) for a in (-80, -40, 40, 80)]
P1 = dict(zip(MON, hungarian([pos(e) for e in MON], POSE)))
def seg_dist(a, b, q):
    dx, dz = b[0] - a[0], b[1] - a[1]; L2 = dx * dx + dz * dz or 1e-9
    f = max(0.0, min(1.0, ((q[0] - a[0]) * dx + (q[1] - a[1]) * dz) / L2))
    return math.hypot(a[0] + f * dx - q[0], a[1] + f * dz - q[1]), f
def walk_round(e, t1, dst, facing, r=0.9):
    """walk to dst arriving t1, stepping round the Bullet (on the side the path is already on) if it passes her"""
    a0 = pos(e)
    d_, f_ = seg_dist(a0, dst, BULLET_HOLD)
    if d_ < r and 0.0 < f_ < 1.0:
        mx, mz = a0[0] + f_ * (dst[0] - a0[0]), a0[1] + f_ * (dst[1] - a0[1])
        ux, uz = mx - BULLET_HOLD[0], mz - BULLET_HOLD[1]; L = math.hypot(ux, uz)
        if L < 1e-6: ux, uz, L = 0.0, 1.0, 1.0
        via = (BULLET_HOLD[0] + (r + 0.1) * ux / L, BULLET_HOLD[1] + (r + 0.1) * uz / L)
        d1 = math.hypot(via[0] - a0[0], via[1] - a0[1]); d2 = math.hypot(dst[0] - via[0], dst[1] - via[1])
        tv = t1 - d2 / 1.3
        walk(e, max(tv, last(e)['_T'] + 0.3 + d1 / 3.0), via, dwell=0)
    walk(e, t1, dst, facing=facing)
for k, e in enumerate(MON):
    walk_round(e, T('2-22', 142.4 + 0.1 * k), P1[e], face(P1[e], BOX))
# off the box (1256): ens9 takes it off SR as Hamilton steps down to SL
walk('ens9', T('2-22', 153.6), (-0.65, 3.2), facing=90, dwell=0.4)
leave('ens9', 'W-DSR', T('2-22', 154.0), speed=1.4)
MON = [e for e in MON if e != 'ens9']
# "to center" (1254): a ring round the centre
RC = [clock(1.9, 25.7 + (360.0 / 7) * k) for k in range(7)]
P15 = dict(zip(MON, hungarian([pos(e) for e in MON], RC)))
for k, e in enumerate(sorted(MON, key=lambda e: P15[e][1])):
    walk_round(e, T('2-22', 149.9 + 0.2 * k), P15[e], face(P15[e], C))
# "Eyes UP" (1258): the knot round the Bullet at the centre
RB = [clock(0.8, 25.7 + (360.0 / 7) * k, BULLET_HOLD) for k in range(7)]
P2 = dict(zip(MON, hungarian([pos(e) for e in MON], RB)))
for k, e in enumerate(sorted(MON, key=lambda e: P2[e][1])):     # the upstage places fill first
    walk(e, T('2-22', 155.46 + 0.3 * k), P2[e], facing=face(P2[e], BULLET_HOLD))
# SPOTLIGHT: ens10 is the 'mum' figure on the gallery (preset 1168, ch17 at 99.6% in "GW UL Steps", caught by the
# gallery at (0.72, -3.09))
enter('ens10', 'G-UC', (0.75, -3.35), T('2-22', 165.6), -20, speed=1.3, ty='gallery')
leave('ens10', 'G-UC', T('2-22', 169.0), speed=1.3)
BLOWN = []                  # REVIEW 3: spots already taken (two used to land on one spot)
def blown(a0):
    for d in (0, 12, -12, 24, -24, 36, -36, 48, -48):
        q = clock(3.4, a0 + d)
        if min(math.hypot(q[0] - o[0], q[1] - o[1]) for o in (H_EYES, (0.95, 2.6), (0.85, 2.45), H_SHOT, (-2.6, 1.0), (-1.2, 0.15)) + tuple(BURR_RIDE) + tuple(BLOWN)) > 1.0:
            BLOWN.append(q); return q
    q = clock(3.4, a0); BLOWN.append(q); return q
# REVIEW 3 (hamilton-lyrics): "at Eliza's cue, the ensemble scatters from center and freezes around the stage, as if blown off
# their feet by an explosion" - on ELIZA (1262, 174.5), not Restore (was 169.6); the 1262 render has the knot gone.
BL_Q = hungarian([P2[e] for e in MON], [blown(ang_of(P2[e])) for e in MON])     # REVIEW 3: matched, so no two cross
for k, e in enumerate(MON):
    q = BL_Q[k]
    hold(e, T('2-22', 174.4), face(P2[e], BULLET_HOLD))
    walk(e, T('2-22', 175.4 + 0.08 * k), q, facing=face(C, q))      # blown out to the edges
for k, e in enumerate(MON):
    a = ang_of(pos(e))
    if 120 <= a < 240: ex = 'W-DSR' if a >= 180 else 'W-DSL'
    elif 240 <= a < 330: ex = 'W-USR'
    elif 30 <= a < 120: ex = 'W-USL'
    else: ex = 'D-UC'
    leave(e, ex, T('2-22', 184.0 + 0.2 * k), speed=1.6)

# after the shot: Burr starts toward him and is held back (ens2); two sit either side of Hamilton and row
walk('burr', T('2-22', 193.4), (0.8, 2.6), facing=-130)
enter('ens2', 'W-MSL', (0.15, 1.95), T('2-22', 197.6), 45, speed=2.2)
B_AWAY = (2.2, 3.35)            # SPOTLIGHT: "Burr is ushered away - Burr SL" is ch1 at (2.01, 3.37)
walk('burr', T('2-22', 200.67), B_AWAY, facing=-50)
walk('ens2', T('2-22', 201.3), (1.45, 2.75), facing=60)
leave('ens2', 'W-MSL', T('2-22', 205.0), speed=1.2)
HA = ang_of(H_HIT); HR = rad_of(H_HIT)
# REVIEW 3: Blankenbuehler (Broadway Direct): "When we resist fate, we turn right. So when Hamilton dies, he turns right" -
# and (Playbill) "the person who gets shot rotates the way of resisting fate, which to me is clockwise". The rowers' ride
# was counter-clockwise (307 -> 262 deg, down the SR side); now it is clockwise, 307 -> 352, up toward 12 o'clock. That
# leaves him upstage, so "Hamilton walks upstage ... climbs the back stairs toward the bridge" (hamilton-lyrics) is the SL
# stair (its foot is upstage at (2.2, -2.45)) and the USG, off by G-UC at 248 - a comment on the film: "4:08-4:11 ...
# Hamilton making his way [out] in the background" (the official audio runs with the album).
enter('ens8', 'W-USR', clock(HR, HA - 14), T('2-22', 201.5), 180, speed=2.0, label='Ensemble 8')
enter('ens9', 'D-UC', clock(HR, HA + 14), T('2-22', 201.8), 0, speed=1.6, label='Ensemble 9')
for e, d in (('hamilton', 0), ('ens8', -14), ('ens9', 14)):
    circle(e, HR, HA + d, HA + 45 + d, T('2-22', 202.2), T('2-22', 213.0), step=8, end_facing=90)
leave('ens8', 'W-USR', T('2-22', 213.4), speed=1.5)
leave('ens9', 'D-UC', T('2-22', 213.6), speed=1.5)
# Hamilton rises, facing upstage; Eliza and Angelica either side of him; he walks upstage and up the SL stair to the bridge
H_RISE = clock(HR, HA + 45)
E_D = (H_RISE[0] - 0.8, H_RISE[1] + 0.4); A_D = (H_RISE[0] + 0.8, H_RISE[1] + 0.4)
hold('hamilton', T('2-22', 222.0), 180)
enter('eliza', 'W-USR', E_D, T('2-22', 226.0), 160, speed=1.2)
enter('angelica', 'D-UC', A_D, T('2-22', 226.5), -160, speed=1.2, label='Angelica')
walk('hamilton', T('2-22', 234.6), (0.5, -2.75), dwell=0)
walk('hamilton', T('2-22', 236.4), (2.2, -2.45), dwell=0)                   # the foot of the SL stair
wpa('hamilton', T('2-22', 241.2), 4.5, -2.45, y='gallery', dwell=0)        # its top
wpa('hamilton', T('2-22', 242.3), 4.5, -3.3, y='gallery', dwell=0)
wpa('hamilton', T('2-22', 247.0), 0.6, -3.35, y='gallery', dwell=0)
wpa('hamilton', T('2-22', 248.2), 0.6, -4.8, y='gallery', off=True)
hold('eliza', T('2-22', 233.0), face(E_D, A_D))        # the women turn to each other
hold('angelica', T('2-22', 233.3), face(A_D, E_D))
# REVIEW 3 (hamilton-lyrics): "the ensemble AND THE SISTERS walk downstage, close around Burr, then collapse and back away.
# Eliza and Angelica remain standing straight" - then the rest of the cast goes, leaving Burr. The sisters come down behind
# the closing company and stand; they leave with it.
walk('eliza', T('2-22', 243.5), (-0.9, 0.4), facing=face((-0.9, 0.4), (0.15, 2.95)))
walk('angelica', T('2-22', 243.7), (1.2, 0.4), facing=face((1.2, 0.4), (0.15, 2.95)))
leave('eliza', 'W-USR', T('2-22', 252.0), speed=1.0)
leave('angelica', 'D-UC', T('2-22', 253.5), speed=1.0)
# the city mourns: the company mirrors the women, then turns out, closes round Burr DSC and falls back
MOURN = ['ens3', 'ens4', 'ens5', 'ens6', 'ens7', 'ens10']
MP = [(-2.0, -0.3), (-1.2, -0.3), (-0.4, -0.3), (0.4, -0.3), (1.2, -0.3), (2.0, -0.3)]
MENT = ['W-DSR', 'W-DSR', 'D-UC', 'D-UC', 'W-USL', 'W-USL']   # REVIEW 3: the SR pair by W-DSR (the rowers leave by W-USR)
for k, (e, p, en) in enumerate(zip(MOURN, MP, MENT)):
    enter(e, en, p, T('2-22', 221.0 + 1.6 * (k % 2) + 0.4 * k), 0, speed=1.1)   # REVIEW 3: +3 s, after the rowers are off
    hold(e, T('2-22', 233.5 + 0.1 * k), 90 if k % 2 == 0 else -90)     # in pairs, facing each other like the women
BURR_DSC = (0.15, 2.95)        # SPOTLIGHT: "Burr DSC" is ch5 at (0.17, 2.75)
RING_B = [clock(1.35, a, BURR_DSC) for a in (-75, -45, -15, 15, 45, 75)]
RBP = dict(zip(MOURN, hungarian([pos(e) for e in MOURN], RING_B)))
for k, e in enumerate(MOURN):
    hold(e, T('2-22', 239.22 + 0.1 * k), 0)                       # turn out
    walk(e, T('2-22', 243.5 + 0.1 * k), RBP[e], facing=face(RBP[e], BURR_DSC))
    q = clock(2.0, ang_of(RBP[e], BURR_DSC), BURR_DSC)
    walk(e, T('2-22', 247.0 + 0.1 * k), q, facing=face(q, BURR_DSC))   # fall back
    a = ang_of(q, BURR_DSC)
    leave(e, 'W-USR' if q[0] < -0.5 else ('W-USL' if q[0] > 0.5 else 'D-UC'), T('2-22', 250.0 + 0.4 * k), speed=1.0)
hold('burr', T('2-22', 215.22), -25)
walk('burr', T('2-22', 228.0), (2.75, 2.75), facing=-60)    # FILM ROUND (no clip): a few steps as the city mourns
walk('burr', T('2-22', 239.22), BURR_DSC, facing=0)          # his reckoning DSC
hold('burr', T('2-22', 252.44), -45)                        # replays the moment
walk('burr', T('2-22', 259.0), (0.6, 3.15), facing=-30)
walk('burr', T('2-22', 266.44), (-0.1, 2.75), facing=0)    # alone, centre (SPOTLIGHT: ch4 at (-0.09, 2.75))
hold('burr', T('2-22', 281.83), 0)

# =====================================================================================
# 2-23 WHO LIVES, WHO DIES, WHO TELLS YOUR STORY   0.44 Washington centre / 12.89 title chorus /
# 16.76 Jefferson (top of the SR stair) / 30.01 Madison DSL / 43.27 Burr DS / 49.23 builds /
# 56.84 Eliza enters, all turn to her / 62.48 Eliza down front / 76.34 her work / 88.92 Angelica /
# 94.94 Angelica gone / 104.08 her years / 114.59 Washington's monument / 119.94 Washington bows his head /
# 126.93 the company closes in behind her / 153.42 it spreads upstage: Hamilton revealed / 156.78 he comes down /
# 170.96 hand in hand at centre / 197.16 he walks her down and gives her away / 204.04 to the house /
# 210.98 the gasp / 211.8 blackout / 214.8 bows
# REVIEW: fan accounts (hamilton-lyrics.tumblr.com "Who Lives, Who Dies, Who Tells Your Story"; ironinkpen Act II):
# Washington opens at centre; Jefferson at the top of the SR staircase with Burr on the floor looking up at him, then
# Burr crosses to watch Madison DSL; the company circles down into three diagonal lines UR->DL; Eliza enters at the
# end of that chorus and everyone turns to her; Jefferson, Madison and Philip form a small triangle behind her for the
# soldiers; Angelica and Eliza sing to each other; Washington comes up behind her and smiles at the monument; the company
# closes in behind her and then spreads upstage, revealing Hamilton where she first entered; he comes down past her,
# they stand side by side facing upstage, see each other, go up to centre where she takes his hand; on the last line
# he walks her down and gives her away; she gasps in a small pool DSC. Curtain call (Harmon Writes; BroadwayWorld
# forum): the company in cream, ensemble among the leads, Hamilton and Eliza at the centre.
# =====================================================================================
OUTER = {a: clock(3.3, a) for a in (240, 270, 300, 330, 30, 60, 90, 120)}
INNER = {a: clock(2.0, a) for a in (250, 277.5, 305, 332.5, 27.5, 55, 82.5, 110)}
W_SLOT = (-0.45, -2.45)
F = {
    J: OUTER[240], M: OUTER[120], 'angelica': INNER[250], 'burr': INNER[110],
    'peggy': INNER[277.5], 'laurens': INNER[82.5],
    'ens1': INNER[305], 'ens2': INNER[332.5], 'ens3': INNER[27.5], 'ens4': INNER[55],
    'ens5': OUTER[270], 'ens6': OUTER[300], 'ens7': OUTER[330], 'ens8': OUTER[30], 'ens9': OUTER[60], 'ens10': OUTER[90],
}
F_LABEL = {J: 'Jefferson', M: 'Madison', 'angelica': 'Angelica', 'peggy': 'Maria Reynolds', 'laurens': 'Philip',
           'washington': 'Washington'}
F_ENT = {M: 'W-DSL', 'angelica': 'W-DSR', 'peggy': 'W-DSR', 'laurens': 'W-MSL',
         'ens1': 'W-USR', 'ens2': 'W-USR', 'ens3': 'W-USL', 'ens4': 'W-USL', 'ens5': 'W-USR', 'ens6': 'W-USR',
         'ens7': 'D-UC', 'ens8': 'D-UC', 'ens9': 'W-USL', 'ens10': 'W-MSL', 'washington': 'W-DSL'}
FON = dict(F); FON['washington'] = (0.0, 4.0)
# the company files on in the dark after the FTB (Burr is already on; Jefferson goes up to the SR stair top)
walk('burr', T('2-23', 0.2), F['burr'], facing=0)
groups = {}
for a in FON:
    if a in ('burr', J): continue
    groups.setdefault(F_ENT[a], []).append(a)
for ent, members in groups.items():
    (ox, oz), oy, wts = ENT[ent]
    def dist_of(a):
        return chain_len([(ox, oz)] + list(wts) + [FON[a]])
    members.sort(key=lambda a: -dist_of(a))     # the farthest goes first
    n = len(members)
    for i, a in enumerate(members):
        t_arr = T('2-23', 3.0) - 1.8 * (n - 1 - i) if a != 'washington' else T('2-23', 0.44)
        lbl = F_LABEL.get(a) or 'Ensemble %s' % a[3:]
        enter(a, ent, FON[a], t_arr, 0, speed=1.35, label=lbl)
        first_off = [x for x in A[a] if x.get('off')][-1]
        if first_off['_T'] < T('2-22', 292.8): print('NOTE early finale entrance', a, first_off['track'], first_off['at'])
walk('washington', T('2-23', 15.0), W_SLOT, facing=0)        # back into the company
# FILM ROUND (no clip for 2-23; hamilton-lyrics: "the company circles down"): the company does not stand 45 s in its rings -
# it walks them slowly round (the outer ring 15 degrees, the inner 10) before it comes down into the three lines at 50
for e in ENS[4:]:
    revolve(e, 15, T('2-23', 5.0), T('2-23', 46.0), step=8)
for e in ENS[:4] + ['angelica', 'peggy']:
    revolve(e, 10, T('2-23', 5.0), T('2-23', 46.0), step=8)
# Jefferson: up the backstage stair, along the gallery, to the top of the SR stair
wpa(J, T('2-23', 8.0), 0.6, -4.8, y='gallery', off=True, dwell=0, label='Jefferson')
wpa(J, T('2-23', 9.1), 0.6, -3.35, y='gallery', dwell=0)
wpa(J, T('2-23', 13.1), -4.5, -3.3, y='gallery', dwell=0)
wpa(J, T('2-23', 16.6), -4.5, -0.45, y='gallery', facing=30)
wpa(J, T('2-23', 27.0), -4.5, -0.3, y='gallery', dwell=0)
walk(J, T('2-23', 32.0), (-4.5, 1.85), dwell=0)
walk(J, T('2-23', 35.0), F[J], facing=0)
# Burr on the floor looks up at Jefferson, crosses to watch Madison, takes his own lines DS, then SL
walk('burr', T('2-23', 16.76), (-2.4, 2.9), facing=face((-2.4, 2.9), (-4.5, -0.45)))
walk('burr', T('2-23', 30.01), (1.3, 3.0), facing=55)
walk(M, T('2-23', 30.01), (2.6, 3.9), facing=-15)
walk(M, T('2-23', 42.0), F[M], facing=0)
walk('burr', T('2-23', 43.27), (0.6, 3.7), facing=0)
walk('burr', T('2-23', 47.5), F['burr'], facing=-20)
# the company builds: three diagonal lines, upstage right to downstage left
LIN = [J, M, 'burr', 'angelica', 'peggy', 'laurens', 'washington'] + ENS
U = (0.781, 0.625); V = (0.625, -0.781); CEN = (0.2, 1.4)
DIAG = []
for s, cnt in ((-1.3, 6), (0.0, 6), (1.3, 5)):
    for i in range(cnt):
        t = (i - (cnt - 1) / 2.0) * 1.0
        DIAG.append((CEN[0] + t * U[0] + s * V[0], CEN[1] + t * U[1] + s * V[1]))
DG = dict(zip(LIN, hungarian([pos(a) for a in LIN], DIAG)))
for k, a in enumerate(LIN):
    walk(a, T('2-23', 50.0 + 0.1 * k), DG[a], facing=20)
SLOT = dict(F); SLOT['washington'] = W_SLOT
ELIZA_IN = (0.1, -1.4)
for k, a in enumerate(LIN):
    walk(a, T('2-23', 56.0 + 0.08 * k), SLOT[a], facing=face(SLOT[a], ELIZA_IN) * 0.7)
for k, a in enumerate(LIN):
    hold(a, T('2-23', 62.6 + 0.08 * k), face(SLOT[a], (0.0, 4.0)) * 0.7)
# FILM ROUND (no clip): slow, deliberate - on "her work" the company takes a slow step in toward her, and on "her years"
# steps back (Jefferson, Madison and Philip make the soldiers' triangle meanwhile; Angelica goes to her)
STEPPERS = ENS + ['peggy', 'burr', 'washington']
def toward(p, q, d):
    L = math.hypot(q[0] - p[0], q[1] - p[1]) or 1.0
    return (p[0] + d * (q[0] - p[0]) / L, p[1] + d * (q[1] - p[1]) / L)
for k, a in enumerate(STEPPERS):
    s = toward(SLOT[a], (0.0, 4.0), 0.5)
    walk(a, T('2-23', 80.0 + 0.1 * k), s, facing=face(s, (0.0, 4.0)) * 0.7)
    walk(a, T('2-23', 108.0 + 0.1 * k), SLOT[a], facing=face(SLOT[a], (0.0, 4.0)) * 0.7)
# Eliza: enters where the company parts, everyone turns to her; she comes down to the front
enter('eliza', 'D-UC', ELIZA_IN, T('2-23', 58.3), 0, label='Eliza', dwell=0)
walk('eliza', T('2-23', 62.48), (0.0, 4.0), facing=0)
# SPOTLIGHT: her shaft (ch93 at (0, 3.62), full from 62.48 to the gasp) keeps her; the triangle stands just outside it
hold('eliza', T('2-23', 80.0), 15)                               # her work: interviewing the soldiers
for a, p in ((J, (-0.85, 2.85)), (M, (0.85, 2.85)), ('laurens', (0.0, 2.2))):
    walk(a, T('2-23', 78.5), p, facing=0)
    walk(a, T('2-23', 86.5), F[a], facing=face(F[a], (0.0, 4.0)) * 0.7)
walk('angelica', T('2-23', 88.92), (-2.1, 4.1), facing=60)      # at her side (ch4 re-aimed to (-1.54, 3.16))
walk('eliza', T('2-23', 89.9), (-1.15, 3.75), facing=-60)
hold('angelica', T('2-23', 95.5), 0)                             # her burial: Angelica turns out
walk('eliza', T('2-23', 96.5), (-0.35, 3.5), facing=-40)         # back into her shaft
walk('angelica', T('2-23', 103.0), F['angelica'], facing=face(F['angelica'], (0.8, 4.1)) * 0.7)
# Eliza's small circle, inside her shaft
walk('eliza', T('2-23', 100.0), (-0.2, 3.25), dwell=0)
walk('eliza', T('2-23', 102.0), (0.35, 3.4), dwell=0)
walk('eliza', T('2-23', 104.0), (0.4, 3.95), dwell=0)
walk('eliza', T('2-23', 106.0), (0.1, 4.0), facing=-10)
# Washington comes up behind her and smiles; bows his head
walk('eliza', T('2-23', 115.0), (-0.3, 3.8), facing=-15)       # FILM ROUND (no clip): she moves a little in her shaft
walk('eliza', T('2-23', 121.0), (0.1, 4.05), facing=10)
walk('washington', T('2-23', 114.59), (0.6, 3.25), facing=15)
hold('washington', T('2-23', 119.94), 15)
# the company closes in behind her (two rows round her)
def garc(r, phi): return (r * math.sin(math.radians(phi)), 4.4 - r * math.cos(math.radians(phi)))
ROW1 = [garc(3.0, phi) for phi in (-75, -55, -35, -12, 12, 35, 55, 75)]
ROW2 = [garc(4.3, phi) for phi in (-70, -52.5, -35, -17.5, 0, 17.5, 35, 52.5, 70)]
CLOSE = [a for a in F] + ['washington']
G = dict(zip(CLOSE, hungarian([pos(a) for a in CLOSE], ROW1 + ROW2)))
for k, a in enumerate(CLOSE):
    walk(a, T('2-23', 124.5 + 0.15 * k), G[a], facing=face(G[a], (0.0, 4.4)) * 0.5)
walk('eliza', T('2-23', 126.93), (0.0, 3.95), facing=0)
walk('eliza', T('2-23', 135.0), (0.35, 3.85), facing=-10)
walk('eliza', T('2-23', 147.0), (-0.1, 4.0), facing=0)
# Hamilton comes on behind them, where she first entered
enter('hamilton', 'D-UC', (0.0, -1.6), T('2-23', 150.0), 0, speed=1.0, label='Hamilton')
# the company spreads upstage: he is revealed
SPREAD = [clock(3.4, a) for a in (225, 250, 275, 300, 325, 35, 60, 85, 110, 135)] + \
         [clock(2.3, a) for a in (240, 270, 300, 330, 30, 60, 90)]
SP = dict(zip(CLOSE, hungarian([pos(a) for a in CLOSE], SPREAD)))
for k, a in enumerate(CLOSE):
    walk(a, T('2-23', 153.42 + 0.12 * k), SP[a], facing=face(SP[a], (0.0, 3.0)) * 0.6)
hold('eliza', T('2-23', 156.78), -20)
# he comes down past her; side by side facing upstage; they see each other; up to centre, her hand in his
walk('hamilton', T('2-23', 163.0), (0.7, 4.15), facing=0)
hold('hamilton', T('2-23', 165.0), 180)
hold('eliza', T('2-23', 165.3), 180)
hold('hamilton', T('2-23', 167.0), -90)
hold('eliza', T('2-23', 167.2), 90)
# SPOTLIGHT: "Hamilton leads her DS - a golden-white key" is ch5 at (-0.56, 2.96), up to the final refrain
walk('eliza', T('2-23', 172.0), (-0.85, 2.6), facing=90)
walk('hamilton', T('2-23', 172.2), (-0.15, 2.6), facing=-90)
walk('washington', T('2-23', 183.36), (-0.5, 1.45), facing=0)  # Washington behind them
# FILM ROUND (no clip): slow and deliberate - the spread company draws in a little toward the couple, twice
for k, a in enumerate([a for a in CLOSE if a != 'washington']):
    s1 = toward(SP[a], (0.0, 3.0), 0.4); s2 = toward(s1, (0.0, 3.0), 0.3)
    walk(a, T('2-23', 188.0 + 0.1 * k), s1, facing=face(s1, (0.0, 3.0)) * 0.6)
    walk(a, T('2-23', 203.0 + 0.1 * k), s2, facing=face(s2, (0.0, 3.0)) * 0.6)
# the last line: he walks her down and gives her away; she goes into her pool DSC
# SPOTLIGHT: her shaft ch93 (0, 3.62) r 0.7 is the gasp's pool; she stands in it alone, the men step back out of it
walk('eliza', T('2-23', 199.6), (0.0, 4.2), facing=0)
walk('hamilton', T('2-23', 199.4), (0.55, 3.85), facing=-30)
walk('hamilton', T('2-23', 204.04), (0.85, 2.75), facing=-15)
walk('washington', T('2-23', 204.5), (-0.85, 2.75), facing=15)
hold('eliza', T('2-23', 204.04), 0)                               # to the house
hold('eliza', T('2-23', 210.98), 0)                               # the gasp
# BOWS - NOTES3 (Jack, 2026-10-15): "after the blackout everyone stays where they are and when the lights come back up they
# bow then they go in the line and bow twice then they leave the stage." (Replaces the two rows walked into in the dark.)
#  211.8   the blackout (cue 1297): everyone holds where the finale left them, and turns to the house in the dark (212.6)
#  214.8   the lights come back (cue 1298, up 3 s: Jack's revision 5)
#  216.13  bow 1 where they stand (dance.py: `bow`, bar 67, 4 counts, to 219.69)
#  219.8-226.0  into ONE line downstage at z 4.2, 0.58 m apart (x -5.22 .. 5.8): the ensemble at the ends, the principals
#          in the middle, Hamilton at centre (0, 4.2) with Eliza beside him SL; King George (not in the
#          finale) walks on from DSL into his place in the line, downstage of the others' arrivals
#  226.80  bow 2, 230.36 bow 3, together (dance.py: bars 70 and 71, 4 counts each, to 233.91)
#  234.2   the line splits at the centre and files off both sides into the downstage wings, peeling from the ends
#          (Hamilton and the SR half W-DSR, the SL half W-DSL); Eliza and then Hamilton are the last off, SR (in the wing by 239.8)
# The `at`s past 217 are 2-23's OPEN tail (RULING FQ).
# The line's 20 places, SR to SL: 4 ensemble, 5 principals, HAMILTON (centre, (0, 4.2)), 4 principals, 6 ensemble (the
# finale leaves more bodies SR, so the principals' block is shifted one place SR to keep Hamilton in the middle). Within
# each group the places go in the order of where the finale left them, SR to SL, and everyone leaves together and arrives
# together, so nobody walks through anybody (an order-keeping walk; a nearest-place assignment crossed 16 pairs).
# Eliza, just SR of Hamilton, is beside him; King George (not in the finale) walks on from DSL into the last
# principals' place.
LINE_Z, LINE_DX, HAM_I = 4.2, 0.58, 9
SLOT = [(round(LINE_DX * (i - HAM_I), 3), LINE_Z) for i in range(20)]
PRIN = sorted(['laurens', 'lafayette', 'washington', 'burr', 'angelica', 'peggy', 'mulligan', 'eliza'], key=lambda a: pos(a)[0])
PRIN = PRIN[:5] + ['hamilton'] + PRIN[5:] + ['king']
LINEP = dict(zip(PRIN, SLOT[4:14]))
LINEP.update(zip(sorted(ENS, key=lambda a: pos(a)[0]), SLOT[0:4] + SLOT[14:20]))
assert LINEP['hamilton'] == (0.0, LINE_Z) and abs(LINEP['eliza'][0]) < 0.6, LINEP
LINE = sorted(LINEP, key=lambda a: LINEP[a][0])
BOW_DARK, BOW_TURN, BOW_GO, LINE_AT, EXIT_AT = 211.9, 212.6, 219.8, 226.0, 234.2
for a in LINE:
    if a == 'king':
        continue
    hold(a, T('2-23', BOW_DARK), last(a).get('facing', 0))       # stays where she is through the dark
    hold(a, T('2-23', BOW_TURN), 0)                                 # turns to the house in the dark
    hold(a, T('2-23', BOW_GO), 0, dwell=0.05)                       # bow 1 (dance.py), then all into the line together
    assert math.hypot(LINEP[a][0] - last(a)['x'], LINEP[a][1] - last(a)['z']) <= 1.4 * (LINE_AT - BOW_GO), a
    walk(a, T('2-23', LINE_AT), LINEP[a], facing=0)
enter('king', 'W-DSL', LINEP['king'], T('2-23', LINE_AT - 0.6), 0, speed=1.3, label='King George', via=[(LINEP['king'][0] + 0.05, 4.85)])
for a in LINE:                                                      # off both sides, the line filing into the wings
    (ox, oz), _, wts = ENT['W-DSR' if LINEP[a][0] <= 0 else 'W-DSL']   # Hamilton (x 0) goes off SR, behind Eliza
    turn = wts[0]
    k = sorted([b for b in LINE if (LINEP[b][0] <= 0) == (LINEP[a][0] <= 0)], key=lambda b: -abs(LINEP[b][0])).index(a)
    t1 = T('2-23', EXIT_AT) + (0.55 + LINE_DX * k) / 1.3          # the k-th from the end reaches the turn k places behind
    wpa(a, t1, turn[0], turn[1], dwell=0)
    wpa(a, t1 + math.hypot(ox - turn[0], oz - turn[1]) / 1.3, ox, oz, off=True)
# =====================================================================================
out = {'segment': 8, 'tracks': ORDER, 'waypoints': {}, 'notes': ''}
for a in ['hamilton', 'burr', 'eliza', 'angelica', 'peggy', 'washington', 'lafayette', 'mulligan', 'laurens', 'king'] + ENS:
    if a in A:
        out['waypoints'][a] = [{k: v for k, v in w.items() if not k.startswith('_')} for w in A[a]]
NOTES = os.path.join(HERE, 'seg8-notes.txt')
if os.path.exists(NOTES):
    out['notes'] = open(NOTES, encoding='utf-8').read().strip()
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
    f.write('{\n "segment": 8,\n "tracks": ' + json.dumps(ORDER) + ',\n "waypoints": {\n')
    names = list(out['waypoints'])
    for n, a in enumerate(names):
        f.write('  ' + json.dumps(a) + ': [')
        f.write(','.join('\n   ' + json.dumps(w) for w in out['waypoints'][a]))
        f.write('\n  ]' + (',' if n + 1 < len(names) else '') + '\n')
    f.write(' },\n "notes": ' + json.dumps(out['notes']) + '\n}\n')
print('wrote', OUT, sum(len(v) for v in out['waypoints'].values()), 'waypoints')

