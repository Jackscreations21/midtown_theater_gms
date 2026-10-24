import sys, math
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seg5lib import *

E = ['ens%d' % i for i in range(1, 11)]
def lab(a):
    return {'ens%d' % i: 'Ensemble %d' % i for i in range(1, 11)}.get(a)

# ======================================================================= 2-01 WHAT'D I MISS
t = lambda at: T('2-01', at)

# FILM ROUND (2026-10-24; research/seg5.md "Film round"). The Disney+ clip (frames at album time) shows: the recap with
# the town already about its business behind Burr (3-24), Hamilton and Washington climbing to the SL end of the upstage
# gallery (18) and standing there with a paper (24); Burr climbing to the top of the stair at the build (33-40), gone
# before Jefferson appears up there (44); and the company DANCING almost throughout - two clusters either side of the
# stair at the build (40), round the stair foot as he comes down (62, 70) with the scrub between (65), a line with him
# (76-90), the party (97-110), the women round him in the Paris aside (112), spread and travelling in the journey
# (125-150), a group SL behind Madison and Jefferson (152-188), a line upstage (188-205), a line from SR to centre for
# the welcome (212), and the final build (221-232).
B = 'burr'
add(B, t(0.0), *WINGS['W-DSR'], off=True, label='Burr')
go(B, [(-6.0, 4.65), (-0.5, 4.4)], t_end=t(3.4), facing=0)
go(B, [(0.5, 4.2)], t_end=t(8.0), facing=-15)             # film 8: walking DC as he tells it
go(B, [(-0.8, 3.9)], t_end=t(13.0), facing=20)
go(B, [(0.3, 4.3)], t_end=t(18.5), facing=-10)
go(B, [(-0.4, 3.9)], t_end=t(23.0), facing=10)            # film 24: DC, the company walking behind him
# film 33-40: up the stair to the top and away, before Jefferson appears there (the film's rolling stair is rolled
# centre; the page has the fixed SL stair, the one Jefferson comes down)
go(B, [(1.2, 1.0), (2.2, -2.45)], t_start=t(25.0), facing=90)
last(B)['dwell'] = 0
go(B, [(4.5, -2.45, 'g'), (4.75, -2.6, 'g'), (4.75, -3.3, 'g'), (1.6, -3.35, 'g')], t_end=t(38.4), facing=0, hold=False)
leave(B, 'G-UC', t_start=t(38.6))

# Hamilton and Washington in the recap (film 18: Hamilton climbing; 24: the two on the gallery, SL of centre, with a paper)
H, WA = 'hamilton', 'washington'
enter(H, 'W-MSL', [(2.0, -1.6), (2.2, -2.45)], t_end=t(15.6), facing=-90, label='Hamilton')
last(H)['dwell'] = 0
go(H, [(4.5, -2.45, 'g'), (4.75, -2.6, 'g'), (4.75, -3.3, 'g'), (2.3, -3.35, 'g')], t_end=t(22.4), facing=-20, hold=False)
enter(WA, 'W-MSL', [(2.0, -1.6), (2.2, -2.45)], t_end=t(16.8), facing=-90, label='Washington')
last(WA)['dwell'] = 0
go(WA, [(4.5, -2.45, 'g'), (4.75, -2.6, 'g'), (4.75, -3.3, 'g'), (3.0, -3.35, 'g')], t_end=t(24.0), facing=-60, hold=False)
stand(H, t(24.5), facing=60)
leave(H, 'G-UC', t_start=t(27.0))
leave(WA, 'G-UC', t_start=t(27.6))

E8 = E[:8]
LOOKUP = (0.6, -3.35)
# the recap: four about the town's business (film 3-24), crossing to a second place halfway
REC = [('ens1', 'W-USR', (-3.2, -1.2), 7.0, (-2.6, 0.4)), ('ens6', 'W-MSL', (3.6, 0.6), 5.0, (2.4, 1.6)),
       ('ens2', 'W-DSR', (-3.6, 2.6), 8.5, (-2.0, 2.0)), ('ens7', 'D-UC', (0.4, -1.8), 11.5, (-1.0, -0.6))]
for k, (a, via, p, te, p2) in enumerate(REC):
    enter(a, via, p, t_end=t(te), facing=face(p, (0.0, 4.0)), label=lab(a))
    go(a, [p2], t_start=t(te + 7.0 + 0.8 * k), facing=face(p2, (0.0, 4.0)))
# the build (31): two clusters either side of the stair, dancing (film 40); the other four come in for it
F_B = {'ens1': (-2.3, -0.7), 'ens2': (-2.7, 1.5), 'ens7': (-1.4, 0.5), 'ens6': (3.8, 0.8),
       'ens5': (-3.0, 0.1), 'ens3': (2.9, 2.0), 'ens4': (3.2, -0.6), 'ens8': (4.3, 2.2)}
for k, a in enumerate(['ens1', 'ens2', 'ens7', 'ens6']):
    go(a, [F_B[a]], t_end=t(30.5 + 0.2 * k), facing=face(F_B[a], (0.0, 4.0)))
LATE = {'ens5': ('W-DSR', [(-4.0, 2.9)], 30.0), 'ens3': ('W-DSL', None, 30.6), 'ens4': ('W-USL', None, 31.0),
        'ens8': ('W-MSL', None, 31.4)}
for a, (via, extra, te) in LATE.items():
    enter(a, via, F_B[a], t_end=t(te), facing=face(F_B[a], (0.0, 4.0)), label=lab(a), extra=extra)
for k, a in enumerate(E8):
    wander(a, t(31.6), t(58.0), every=4.4, look=(0.0, 4.0), ph=k)
    stand(a, t(58.4 + 0.1 * k), facing=face(F_B[a], LOOKUP))   # Jefferson appears up top: they turn to him
# W3 60.8: they drop to scrub the floor as he strides down (film 65) - an aisle left from the SL stair foot (2.2,-2.45)
# down through (2.0, 0.4) and (0.6, 2.8) to DSC
W3 = [(-3.0, -0.6), (-1.6, -0.1), (-0.2, -0.8), (1.0, -0.9), (3.1, -0.9),
      (-2.3, 1.1), (2.4, 2.0), (3.6, 0.6)]
m3 = form(E8, W3, t_end=t(63.5), stagger=0.2, facing=lambda p: face(p, (1.6, 1.2)))
# 69.5 up and dancing round him (film 70), then a line with him (film 76): eight across z 2.6, the centre left for him
F_L = [(-3.6, 2.6), (-2.6, 2.6), (-1.6, 2.6), (-0.6, 2.6), (0.6, 2.6), (1.6, 2.6), (2.6, 2.6), (3.6, 2.6)]
mL = form(E8, F_L, t_end=t(76.0), stagger=0.1, facing=lambda p: 0)
for k, a in enumerate(E8):
    wander(a, t(80.0), t(96.5), every=4.1, offs=[(0.2, 0.0), (0.0, 0.0), (-0.2, 0.0), (0.0, 0.0)], facing=0, ph=k)
# 97.8 the party (film 97-110): two rows, the centre open for him
F_P = [(-3.0, 1.0), (-1.0, 1.0), (1.0, 1.0), (3.0, 1.0), (-3.4, 2.4), (-1.6, 2.6), (1.6, 2.6), (3.4, 2.4)]
mP = form(E8, F_P, t_end=t(98.5), stagger=0.1, facing=lambda p: 0)
# 108.4 the Paris aside (film 112): three of the women round him DSL, swooning; the rest dance on in their rows
SWOON = {'ens2': (0.7, 2.8), 'ens6': (1.4, 4.35), 'ens8': (2.25, 3.3)}
for k, a in enumerate(SWOON):
    go(a, [SWOON[a]], t_start=t(108.6 + 0.3 * k), facing=face(SWOON[a], (1.4, 3.6)))
for k, a in enumerate([a for a in E8 if a not in SWOON]):
    wander(a, t(99.0), t(129.0), every=4.6, look=(0.5, 3.6), ph=k)
# 118.2 the letter: Sally (ens6) brings it to him and goes back
go('ens6', [(0.45, 4.25)], t_end=t(119.5), facing=face((0.45, 4.25), (0.0, 3.6)))
go('ens6', [SWOON['ens6']], t_start=t(124.0), facing=face(SWOON['ens6'], (0.0, 3.6)))
# 129.5 the journey (film 125-150): out to the outer ring and travelling round it with him
HRS = [-145, -105, -65, -25, 25, 65, 105, 145]
RING = [ring(3.3, h) for h in HRS]
mR = form(E8, RING, t_end=t(133.0), stagger=0.15, facing=lambda p: face(p, (0.0, 0.95)))
for k, a in enumerate(E8):
    revolve_by(a, 3.3, -60, t(135.5 + 0.1 * k), t(150.0), step=20, facing=face(ring(3.3, theta_of(cur(a)) - 60), (0.0, 0.95)))
# 152 the company SL, dancing behind Madison and Jefferson (film 152-188)
F_SL = [(2.0, 0.0), (3.0, -0.4), (4.0, 0.2), (2.6, 1.0), (3.6, 1.3), (4.4, 2.0), (2.4, 2.1), (3.4, 2.6)]
mS = form(E8, F_SL, t_end=t(155.0), stagger=0.15, facing=lambda p: face(p, (0.0, 3.9)))
for k, a in enumerate(E8):
    wander(a, t(156.0), t(186.5), every=4.4, look=(0.0, 3.9), ph=k)
# 188.5 the hook again: a line upstage (film 188-205)
F_U = [(-3.5 + 1.0 * k, -0.6) for k in range(8)]
# the three lines from here on keep one order SR to SL, the order they sit in the cabinet V (props.py VSEAT)
ORDER8 = ['ens1', 'ens5', 'ens2', 'ens3', 'ens6', 'ens4', 'ens7', 'ens8']
mU = {}
for k, a in enumerate(ORDER8):
    mU[a] = F_U[k]; go(a, [F_U[k]], t_end=t(190.0 + 0.1 * k), facing=0)
for k, a in enumerate(E8):
    wander(a, t(191.0), t(207.0), every=4.0, offs=[(0.0, 0.4), (0.0, 0.0), (0.0, -0.3), (0.0, 0.0)], facing=0, ph=k)
# 208.3 Hamilton named: a line from SR to centre (film 212), turned on the welcome DL
F_W = [(-3.5 + 0.78 * k, 2.2) for k in range(8)]
mW = {}
for k, a in enumerate(ORDER8):
    mW[a] = F_W[k]; go(a, [F_W[k]], t_end=t(210.5 + 0.1 * k), facing=face(F_W[k], (2.6, 4.0)))
# 221.2 final build: one line across the deck
W8 = [(-3.5 + 1.0 * k, 1.9) for k in range(8)]
m8 = {}
for k, a in enumerate(ORDER8):
    m8[a] = W8[k]; go(a, [W8[k]], t_end=t(222.0 + 0.05 * k), facing=0)

# Jefferson: appears TOP CENTRE on the upstage gallery (REVIEW: the Washington/Jefferson rolling staircase
# is parked at the SL balcony and rolled centre for this entrance - PLSN, BroadwayBox/Korins; the page has no
# rolling stair, so he takes the fixed SL stair, the parked unit's place), strides along the gallery, down the
# SL stair and through an aisle in the scrubbing company to DSC
J = 'lafayette'
# NOTES3 (Jack, 2026-10-15): "jefferson come out onto the balcony at 44" - he comes out of the gallery door at top centre
# and is up there by 44.0 (was 57.9), in cue 723's top-centre Lustr pin (ch187 at (-0.23, -3.57)), and waits there for
# his descent at 60.8 (cue 725's "Jefferson appears up top" key is still at 57.9: the cue agent's)
add(J, t(42.0), *GUC[0][:2], 'g', off=True, label='Jefferson')
go(J, [(0.6, -3.35, 'g'), (0.0, -3.45, 'g')], t_end=t(44.0), facing=0)
stand(J, t(57.9), facing=0)
go(J, [(4.75, -3.3, 'g'), (4.75, -2.6, 'g'), (4.5, -2.45, 'g'), (2.2, -2.45)], t_start=t(60.8), speed=1.7)
last(J)['dwell'] = 0
go(J, [(2.0, 0.4), (0.6, 2.8), (0.0, 4.2)], t_end=t(73.0), facing=0, hold=False, speed=1.7)
# SPOT: verse 1 kept inside the DSC warm key (727, ch93 at (0, 4.45) r1.04)
go(J, [(0.9, 4.0)], t_end=t(80.0), facing=-15)
go(J, [(-0.8, 3.85)], t_end=t(87.0), facing=15)
go(J, [(0.0, 4.1)], t_end=t(95.0), facing=0)
go(J, [(1.4, 3.6)], t_start=t(108.4), facing=-30)
go(J, [(0.0, 3.6)], t_end=t(118.8), facing=40)
stand(J, t(129.8), facing=0)
go(J, [(-1.3, 2.4), (-0.8, 0.9), (0.9, 1.2), (0.5, 2.4)], t_start=t(135.5), t_end=t(150.0), facing=-60)
go(J, [(0.6, 3.85)], t_end=t(160.0), facing=-100)   # SPOT: 734 the DSC key (93) on the two of them
stand(J, t(172.0), facing=-60)
go(J, [(0.0, 4.1)], t_end=t(188.5), facing=0)
go(J, [(0.0, 4.5)], t_end=t(199.0), facing=0)
stand(J, t(209.3), facing=55)
# REVIEW 3: the welcome handshake (ironinkpen: Jefferson reaches for Washington's hand and Hamilton jumps in and takes it;
# Disney+ clip comments: Hamilton pushes past to get to Jefferson at about 214, Jefferson laughs at him at about 218)
go(J, [(1.05, 4.25)], t_start=t(211.6), t_end=t(213.0), facing=75)    # reaches for Washington
go(J, [(0.3, 4.1)], t_start=t(217.8), t_end=t(222.0), facing=-20)     # steps back, laughing
stand(J, t(233.0), facing=0)

# Madison: arrives DR on the hit, flustered (mirrored from the reconstruction's DL - see notes)
M = 'mulligan'
enter(M, 'W-DSR', (-3.5, 3.4), t_end=t(153.9), facing=60, label='Madison')
go(M, [(-0.6, 3.95)], t_end=t(163.5), facing=70)    # SPOT: his verse in the DSC key (734, ch93)
wander(M, t(164.5), t(175.0), every=3.5, look=(0.6, 3.85))   # FILM: a rapper is never still (film 165-183: at Jefferson, arms going)
go(M, [(-0.75, 3.85)], t_end=t(176.0), facing=60)
wander(M, t(177.0), t(187.5), every=3.5, look=(0.6, 3.85), ph=2)
go(M, [(-1.6, 3.9)], t_end=t(189.0), facing=20)
go(M, [(-2.0, 3.6)], t_end=t(200.0), facing=40)
wander(M, t(201.0), t(208.5), every=3.5, look=(0.0, 4.1))
stand(M, t(209.5), facing=80)
go(M, [(-1.6, 3.9)], t_end=t(222.0), facing=20)
wander(M, t(223.0), t(233.5), every=3.5, look=(0.3, 4.1), ph=1)

# Hamilton: named by the company, appears DL (mirrored, see notes)
H = 'hamilton'
enter(H, 'W-DSL', (3.5, 3.4), t_end=t(208.3), facing=-50, label='Hamilton')
go(H, [(1.85, 4.0)], t_start=t(212.2), t_end=t(213.8), facing=-80)   # REVIEW 3: jumps in and takes Jefferson's hand
go(H, [(3.0, 3.0)], t_start=t(218.6), t_end=t(222.5), facing=-60)
wander(H, t(223.5), t(233.5), every=3.5, look=(0.0, 4.2))   # FILM 226-232: in it with the company

# Washington comes on with Hamilton for the welcome (REVIEW: Jefferson reaches for Washington's hand and
# Hamilton takes it - ironinkpen staging notes), then steps to the DSC mic in the snap for the cabinet meeting
WA = 'washington'
enter(WA, 'W-DSL', (2.75, 4.25), t_end=t(210.8), facing=face((2.75, 4.25), (0.0, 4.5)), label='Washington')   # REVIEW 3: DS of Hamilton's way to Jefferson
stand(WA, t(222.6), facing=face((2.75, 4.25), (0.3, 4.1)))
wander(WA, t(223.6), t(233.8), every=3.4, look=(0.3, 4.1), ph=3)
go(WA, [(0.0, 4.4)], t_start=t(234.3), t_end=T('2-02', 0.5), facing=0)

# ======================================================================= 2-02 CABINET BATTLE #1
c = lambda at: T('2-02', at)
# the snap (2-01 234.2): the line of the company sits in the V of chairs on the deck
# (REVIEW: "two rows of chairs form a V opening toward the audience", ensemble seated in them, Washington
#  seated with them - ironinkpen staging notes; cue 742 puts Washington's chair SL. Jefferson's side SR,
#  Hamilton's side SL per Jack's revision-5 ruling. The chairs themselves are not modelled.)
# (REVIEW 2: eight seats, four an arm, with Washington's chair at the SL vertex; the V itself is sourced, its size is
#  not - eight follows the company of What'd I Miss. Sides as ruled: Jefferson's SR, Hamilton's SL.)
V_SR = [(-3.8, 2.4), (-3.1, 1.45), (-2.4, 0.5), (-1.7, -0.45)]                       # downstage-out -> vertex
V_SL = [(1.7, -0.45), (2.4, 0.5), (3.1, 1.45), (3.8, 2.4)]                           # vertex -> downstage-out
WA_CHAIR = (1.0, -1.4)                                                               # SL arm, at the vertex
byx = sorted(E8, key=lambda a: m8[a][0])
seat = {a: (V_SR + V_SL)[i] for i, a in enumerate(byx)}
look = (0.0, 3.2)
for k, a in enumerate(byx):
    go(a, [seat[a]], t_start=T('2-01', 234.3 + 0.15 * k), facing=face(seat[a], look))
# the crowd reacts: they turn to whoever has the floor
for k, a in enumerate(E8):
    d = seat[a]
    stand(a, c(22.5 + 0.1 * k), facing=face(d, (-1.3, 3.7)))
    stand(a, c(86.5 + 0.1 * k), facing=face(d, (1.3, 3.7)))
    stand(a, c(147.5 + 0.1 * k), facing=face(d, (0.0, 1.4)))
# 156.5 the meeting breaks up: the crowd goes, the SR arm first (the Virginians leave that way after them)
exit_plan = {V_SR[0]: ('W-DSR', None), V_SR[1]: ('W-DSR', [(-3.9, 2.6)]), V_SR[2]: ('W-DSR', [(-3.9, 2.6)]),
             V_SR[3]: ('D-UC', None),
             V_SL[0]: ('D-UC', None), V_SL[1]: ('W-MSL', None), V_SL[2]: ('W-MSL', None),
             V_SL[3]: ('W-DSL', None)}
exit_order = [V_SR[0], V_SR[1], V_SR[2], V_SL[3], V_SL[2], V_SR[3], V_SL[1], V_SL[0]]
for a in E8:
    via, extra = exit_plan[seat[a]]
    ts = c(157.5) + 1.1 * exit_order.index(seat[a])
    leave(a, via, t_start=ts, extra=extra)

# Washington: the MC at the DSC mic, then his chair at the vertex of the SL arm (cue 742: chair SL)
go(WA, [(0.4, 1.0), WA_CHAIR], t_start=c(9.0), facing=face(WA_CHAIR, look))
go(WA, [(0.3, 0.4)], t_end=c(79.5), facing=0)          # thanks Jefferson, hands over
go(WA, [WA_CHAIR], t_start=c(82.0), facing=face(WA_CHAIR, look))
go(WA, [(0.0, 1.4)], t_end=c(148.0), facing=0)         # stops it, stands
go(WA, [(0.5, 2.0)], t_end=c(158.0), facing=-20)       # FILM ROUND: steps down to them as the room clears
go(WA, [(0.0, 1.6)], t_end=c(167.0), facing=0)
# SPOT: 761-763 Washington's pool (the dump's ch8 at (0.8, 2.2), Hamilton's ch92 at (-1.2, 2.4); mirrored with the
# ruling they land on Washington at (-0.8, 2.2) and Hamilton at (1.2, 2.4); this spot is in both versions)
go(WA, [(-0.8, 2.6)], t_end=c(176.5), facing=68)       # the private reprimand
go(WA, [(-1.2, 2.1)], t_end=c(186.0), facing=40)      # FILM ROUND: the reprimand on the move, round him
go(WA, [(-0.65, 2.4)], t_end=c(196.0), facing=60)
stand(WA, c(208.4), facing=60)
leave(WA, 'D-UC', t_start=c(211.2), speed=1.6)

# Jefferson (SR) and Hamilton (SL) - see notes for the side question
go(J, [(-1.6, 3.0)], t_start=T('2-01', 234.2), facing=45)
go(J, [(-1.3, 3.7)], t_end=c(13.0), facing=75)
stand(J, c(22.2), facing=15)
# FILM ROUND (no clip for 2-02; Cabinet Battle #2's clip, film 45: the rapper works the floor in front of the seated room,
# the other standing to one side): he works HIS side of the room, and is back on his spot by 34.5 (NOTES3 ruling below)
go(J, [(-2.1, 3.3)], t_end=c(26.5), facing=40)
go(J, [(-0.9, 3.4)], t_end=c(30.5), facing=20)
go(J, [(-1.3, 3.7)], t_end=c(34.5), facing=0)
# NOTES3 (Jack, 2026-10-15): "somewhere around 40 jefferson walks to the center when he should stay in his spot" - the
# cross to C at 35.6 (cue 745) is cut: he works the room from his spot SR and turns on Hamilton's interjection
stand(J, c(35.6), facing=0)
stand(J, c(45.4), facing=face((-1.3, 3.7), (0.8, 3.3)))
go(J, [(-1.8, 2.9)], t_end=c(53.0), facing=30)        # SPOT: near his key (747, mirrored ch94)
go(J, [(-0.6, 2.9)], t_end=c(60.0), facing=0)
go(J, [(-2.4, 3.4)], t_end=c(68.0), facing=-40)        # rallies his side of the room
go(J, [(-1.3, 3.7)], t_end=c(76.5), facing=0)          # mic drop
stand(J, c(80.0), facing=75)
go(J, [(-2.0, 3.2)], t_end=c(95.0), facing=60)        # FILM ROUND: he listens on the move, to his side (CB2 film 75: the other one shifting)
go(J, [(-1.3, 3.7)], t_end=c(104.0), facing=70)
stand(J, c(109.0), facing=60)
go(J, [(-1.7, 3.3)], t_end=c(131.0), facing=70)        # Hamilton comes at them
go(J, [(-1.5, 3.4)], t_end=c(148.0), facing=30)
# SPOT: 760's lavender pool on their way out (the dump's ch94 at (3.0, 3.6) DL, mirrored to DR by the ruling)
go(J, [(0.2, 2.5), (-1.2, 2.2), (-2.8, 3.3)], t_start=c(156.5), t_end=c(164.5), facing=60)
leave(J, 'W-DSR', t_start=c(170.5))

go(M, [(-2.6, 2.6)], t_start=T('2-01', 234.3), t_end=T('2-01', 235.6), facing=45)
go(M, [(-2.1, 3.3)], t_end=c(34.5), facing=25)         # the shared shout
go(M, [(-2.6, 2.6)], t_end=c(41.0), facing=60)
go(M, [(-2.4, 2.9)], t_end=c(70.0), facing=45)
go(M, [(-3.0, 2.2)], t_end=c(131.0), facing=60)
go(M, [(-2.6, 2.6)], t_end=c(149.0), facing=40)
go(M, [(-0.6, 1.7), (-2.2, 2.4), (-3.4, 3.0)], t_start=c(156.5), t_end=c(163.0), facing=70)
leave(M, 'W-DSR', t_start=c(167.3))

go(H, [(2.4, 2.0), (1.3, 3.7)], t_start=c(4.0), t_end=c(13.0), facing=-75)
stand(H, c(22.4), facing=-60)
go(H, [(2.0, 3.3)], t_end=c(29.0), facing=-70)        # FILM ROUND: shifting on his side as he listens (CB2 film 45)
go(H, [(1.4, 3.8)], t_end=c(37.0), facing=-60)
go(H, [(0.8, 3.3)], t_end=c(45.5), facing=face((0.8, 3.3), (-1.3, 3.7)))   # the interjection (NOTES3: at Jefferson in his spot)
go(H, [(1.4, 3.6)], t_end=c(49.5), facing=-60)
go(H, [(2.1, 3.2)], t_end=c(60.0), facing=-60)        # FILM ROUND: on the move while Jefferson rallies his side
go(H, [(1.6, 3.9)], t_end=c(70.0), facing=-50)
go(H, [(1.3, 3.7)], t_end=c(80.0), facing=-45)
stand(H, c(86.0), facing=0)
go(H, [(0.4, 3.0)], t_end=c(100.0), facing=0)          # the plan
go(H, [(1.6, 3.1)], t_end=c(106.0), facing=-20)       # SPOT: in his key (752, mirrored ch92)
go(H, [(0.2, 3.2)], t_end=c(109.5), facing=-70)        # the slavery charge, at Jefferson
go(H, [(-0.4, 3.5)], t_end=c(120.0), facing=-80)       # personal
go(H, [(0.6, 4.2)], t_end=c(127.0), facing=0)          # the war memory, to the house
go(H, [(-0.7, 2.8)], t_end=c(131.0), facing=-75)       # at Jefferson and Madison
go(H, [(0.4, 3.4)], t_end=c(138.0), facing=-30)
go(H, [(1.3, 3.7)], t_end=c(144.6), facing=0)          # mic drop
go(H, [(1.0, 3.4)], t_end=c(148.5), facing=-45)
stand(H, c(160.0), facing=-90)                          # the Virginians taunt him on their way out
go(H, [(1.9, 3.0)], t_end=c(165.0), facing=-80)       # FILM ROUND: he turns after them as they go
go(H, [(0.7, 3.2)], t_end=c(176.5), facing=-50)
stand(H, c(196.0), facing=-40)
stand(H, c(212.0), facing=0)                            # alone

# ======================================================================= 2-03 TAKE A BREAK
b = lambda at: T('2-03', at)
EL, AN, PH = 'eliza', 'angelica', 'laurens'
PIANO_P, PIANO_E = (1.0, 1.5), (2.2, 1.1)
# (REVIEW: Eliza and Philip at the piano "on the moving platform, which spins slowly" - ironinkpen staging
#  notes; the piano group rides the inner turntable 40 degrees into its place SL of centre)
# REVIEW 2: the piano is now a prop (props.py 'piano', set in the dark at the 2-02 button), and a placed prop cannot
# ride the turntable, so the 40-degree ride is dropped: mother and son walk straight to it in the change and stay.
# Philip at the keys (the piano is SL of him, keyboard to SR), Eliza behind it leaning over to him.
# FILM ROUND (2026-10-24; seg5.md "Film round"): the clip confirms the desk SR and the piano SL (film 30). It moves:
# Angelica, up on the USG by 30 (not 45); at the SR end by 132 and on the SR stair (132-180), down it to the family SR
# (189: Eliza runs to her across the stage); Eliza at the desk with him (62) before she brings him to the piano; Philip's
# poem beside the piano SL, the parents either side of it (76-100), not DSC; and Hamilton SL of the sisters from the
# reunion on (189-266), not DR. He sits at the desk to write (film 30, 50; props.py writing-chair), Philip at the piano
# bench (film 10; props.py piano-bench).
enter(EL, 'W-MSL', PIANO_E, t_end=b(0.0), facing=-70, label='Eliza')
enter(PH, 'W-MSL', [(2.4, 2.5), PIANO_P], t_end=T('2-02', 213.0), facing=60, label='Philip')
stand(EL, b(14.0), facing=-60)
stand(PH, b(14.0), facing=40)
go(EL, [(2.3, 1.75)], t_end=b(24.0), facing=-100)       # FILM 10-30: round the piano, teaching him
go(EL, [PIANO_E], t_end=b(38.0), facing=-70)
DESK = (-1.5, 1.4)
go(H, [DESK], t_end=b(19.5), facing=0)                  # to the desk, writing to Angelica
# SPOT: her gallery key (766/774/775/776, ch18) crosses the USG at x 0 and head height near z -3.4
enter(AN, 'G-UC', (0.0, -3.45, 'g'), t_end=b(28.5), facing=0, label='Angelica')   # FILM 30: up there already
go(AN, [(-0.9, -3.65, 'g')], t_start=b(58.6), facing=0)  # she fades back
# FILM 62: Eliza comes to him at the desk and leans over him; then brings him to the piano (74)
go(EL, [(2.1, 2.3), (1.0, 2.4), (-1.0, 1.0)], t_end=b(61.5), facing=-100)
go(EL, [(1.6, 0.3), PIANO_E], t_start=b(68.5), facing=-80)
go(H, [(0.2, 1.9)], t_start=b(69.5), facing=70)         # FILM 76-84: SR of the piano, arms crossed
# Philip's poem (FILM 76-100): up from the bench to the SL side of the piano, the parents either side
go(PH, [(1.0, 2.3), (2.0, 2.4), (2.9, 2.0)], t_start=b(75.0), facing=-70)
go(PH, [(3.2, 1.5)], t_end=b(84.0), facing=-90)
go(PH, [(2.7, 2.4)], t_end=b(89.0), facing=-60)
go(PH, [(3.3, 2.0)], t_end=b(94.5), facing=-80)
go(PH, [(2.8, 1.7)], t_end=b(99.5), facing=-90)
go(H, [(0.0, 2.3)], t_end=b(86.0), facing=60)
go(H, [(0.3, 1.8)], t_end=b(95.0), facing=75)
go(PH, [(2.0, 2.4), (1.0, 2.3), PIANO_P], t_start=b(103.0), facing=40)   # back to the piano, round them
go(EL, [(2.1, 2.15), (0.6, 3.3)], t_end=b(106.0), facing=-50)         # the duet
go(H, [(-0.45, 3.15)], t_end=b(106.0), facing=50)        # SPOT: inside the duet pool (772, ch8)
go(EL, [(0.4, 2.6)], t_end=b(118.0), facing=-40)         # the lake upstate
go(H, [(-0.4, 3.1)], t_end=b(118.0), facing=40)
go(H, [DESK], t_end=b(129.0), facing=0)                  # Angelica's second letter
go(EL, [(1.9, 2.2), PIANO_E], t_end=b(130.0), facing=-40)
# FILM 132-180: she is at the SR end, on the top of the SR stair, through the letter and the comma
go(AN, [(-4.5, -3.3, 'g'), (-4.5, -0.3, 'g')], t_start=b(124.5), t_end=b(131.5), facing=40)
go(AN, [(-4.5, -1.0, 'g')], t_end=b(140.0), facing=60)
go(AN, [(-4.5, -0.3, 'g')], t_end=b(149.5), facing=45)
stand(AN, b(152.0), facing=20)                           # the comma
go(AN, [(-4.5, -0.9, 'g')], t_end=b(160.0), facing=60)
go(AN, [(-4.5, -0.3, 'g')], t_end=b(168.0), facing=30)
# she is coming: down the SR stair (FILM 170-180), and Eliza runs to her across the stage (FILM 189)
go(AN, [(-4.5, 1.85)], t_start=b(176.0), facing=60)
go(AN, [(-3.6, 2.3)], t_end=b(183.5), facing=80)
go(H, [(0.6, 2.5), (2.6, 2.6)], t_start=b(178.0), t_end=b(182.0), facing=-80)   # up from the desk, and across to SL (FILM 189: SL)
go(EL, [(2.1, 2.2), (-2.8, 2.5)], t_start=b(184.0), t_end=b(188.5), facing=-90)    # the sisters meet, SR
stand(PH, b(189.5), facing=40)
go(EL, [(-1.6, 2.6)], t_end=b(198.0), facing=-80)        # FILM 191-205: arm in arm, turning to him
go(AN, [(-2.5, 2.5)], t_end=b(199.0), facing=60)
go(H, [(2.2, 2.6)], t_end=b(200.0), facing=-90)
go(EL, [(-0.8, 2.8)], t_end=b(212.0), facing=-60)
go(AN, [(-1.9, 2.9)], t_end=b(213.0), facing=70)
go(H, [(1.6, 2.9)], t_end=b(218.0), facing=-80)          # he stays behind (FILM 216: SL of them)
go(EL, [(-0.2, 2.9)], t_end=b(226.0), facing=-70)        # the trio (FILM 226-245: Angelica, Eliza, him, SR to SL)
go(AN, [(-1.2, 2.9)], t_end=b(226.5), facing=70)
go(H, [(0.75, 3.0)], t_end=b(232.0), facing=-80)
stand(PH, b(227.0), facing=-30)                          # FILM ROUND: he stays at the piano, turned to them
go(EL, [(0.0, 3.4)], t_end=b(244.0), facing=-40)
go(H, [(0.9, 3.4)], t_end=b(246.0), facing=-80)
go(AN, [(-0.9, 3.3)], t_end=b(247.0), facing=60)
go(AN, [(-0.6, 4.1), (1.5, 4.1), (1.6, 3.2)], t_start=b(247.5), facing=-80)   # round in front of them to his other side
go(EL, [(-0.4, 3.1)], t_end=b(257.0), facing=0)          # the Schuyler motif: he between them, hands held (FILM 256-266)
go(H, [(0.6, 3.2)], t_end=b(257.0), facing=0)
go(AN, [(1.6, 3.2)], t_end=b(257.5), facing=0)
leave(EL, 'W-MSL', t_start=b(266.3), extra=[(0.2, 2.4), (2.4, 2.5), (3.0, 1.6)])
leave(AN, 'W-MSL', t_start=b(267.0), extra=[(2.6, 2.9), (3.6, 2.2)])
leave(PH, 'W-MSL', t_start=b(264.8), extra=[(1.0, 2.3), (2.4, 2.4)])
go(H, [(-0.2, 2.2), DESK], t_end=b(275.0), facing=0)     # alone at the desk into the dark

# ======================================================================= 2-04 SAY NO TO THIS
s = lambda at: T('2-04', at)
MR = 'peggy'
enter('burr', 'W-DSR', (-3.4, 1.2), t_end=s(0.5), facing=35, label='Burr', extra=[(-3.9, 2.4)])
stand('burr', s(15.0), facing=60)
# REVIEW 3: Burr does not leave after he hands the story over - he stays in the back watching the whole number
# (Disney+ clip comments: Burr in the back watching the whole time, his smirk). Upstage SR, clear of the
# desk, the lamps and James' DR entrance; off on the button (832), ahead of James and Hamilton.
SN_BURR = (-3.5, -0.7)
go('burr', [SN_BURR], t_start=s(22.0), facing=face(SN_BURR, (0.8, 1.5)))
stand('burr', s(130.0), facing=face(SN_BURR, (-1.6, 3.0)))     # turns to Reynolds' letter, DR
stand('burr', s(153.6), facing=face(SN_BURR, (1.8, 1.5)))      # back to the pair
leave('burr', 'W-DSR', t_start=s(231.0), extra=[(-3.9, 2.4)])   # off before James and Hamilton go DSR
# SPOT: Maria's face key is ch13 throughout (preset 732 'Woman SL' (3.5, 0.24); 790-818 at (2.7, 0.8)/(3.1, 1.0);
# 820 at (0.93, 1.66)); her door is SL, Hamilton's pool ch93 at (0.42, 1.96) / (1.66, 1.75)
enter(MR, 'W-MSL', (3.1, 0.8), t_end=s(16.0), facing=-80, label='Maria Reynolds')
go(H, [(-1.4, 2.3)], t_end=s(21.5), facing=0)            # steps DS of the desk to tell it
stand(H, s(33.5), facing=60)
go(H, [(0.8, 1.9)], t_end=s(45.0), facing=60)
go(MR, [(1.6, 1.2)], t_start=s(44.8), t_end=s(47.5), facing=face((1.6, 1.2), (0.8, 1.9)))
# the walk to her door: she leads him round the turntable
go(MR, [(1.0, 0.0), (2.0, -0.6), (2.8, 0.7)], t_start=s(59.1), t_end=s(70.0), facing=face((2.8, 0.7), (0.8, 1.5)))
go(H, [(0.4, 0.6), (1.3, -0.2), (0.8, 1.5)], t_start=s(60.3), t_end=s(71.5), facing=face((0.8, 1.5), (2.8, 0.7)))
go(H, [(0.3, 2.4)], t_start=s(81.0), facing=0)           # the first chorus: he tries to leave
go(MR, [(1.7, 1.3)], t_end=s(88.0), facing=-70)
go(H, [(1.1, 1.65)], t_end=s(101.5), facing=70)
go(MR, [(1.65, 1.35)], t_end=s(102.5), facing=-70)         # the kiss, between her key and his pool
go(H, [(0.6, 2.6)], t_start=s(106.8), facing=0)          # the hits
go(H, [(0.3, 1.7)], t_end=s(114.0), facing=-120)
go(MR, [(2.7, 0.8)], t_end=s(116.0), facing=-60)         # back to her door
go(H, [(-0.7, 2.2)], t_end=s(124.0), facing=60)          # SPOT: home, DS of his desk (804, ch93 at (-0.83, 2.16))
go(MR, [(3.1, 0.6)], t_start=s(130.0), facing=-60)       # she withdraws as Reynolds' letter comes
go(H, [(-1.15, 2.65)], t_end=s(133.5), facing=-55)
# SPOT: Reynolds' letter (806-810): preset 769 'DL Ham/James' puts four of its five units DR (ch92/93/97/98 at
# x -2.5 .. -4.1, z 3.9 .. 4.6; only ch21 is DL), and the cue lights 97/98 DR - so James comes on DR, to Hamilton
enter('ens4', 'W-DSR', (-2.7, 3.8), t_end=s(131.0), facing=125, label='James Reynolds', t_off=s(125.0))
go('ens4', [(-1.5, 3.6)], t_end=s(137.0), facing=115)    # FILM ROUND 133-155: he works it, closing on him and off again
go('ens4', [(-2.3, 3.6)], t_end=s(144.0), facing=120)    # names his price
go('ens4', [(-2.8, 3.9)], t_end=s(149.5), facing=100)
leave('ens4', 'W-DSR', t_start=s(154.0))
# REVIEW 3: James comes back for the money on the last line (ironinkpen: on Hamilton's last line he hands money
# to Reynolds; Disney+ clip comment at 3:56: James takes the money and walks away) - beside him DSC, then off DSR first
# FILM ROUND (film 233, wide): the last picture is James SR, Maria centre, Hamilton SL, a gap between each
enter('ens4', 'W-DSR', (-1.1, 4.0), t_end=s(232.3), facing=75)
leave('ens4', 'W-DSR', t_start=s(234.6))
go(H, [(1.8, 1.5)], t_start=s(153.6), speed=1.9, facing=65)   # races to her door (812, ch93 at (1.66, 1.75))
go(H, [(2.1, 1.35)], t_end=s(166.0), facing=75)
go(MR, [(3.0, 0.95)], t_end=s(166.0), facing=-95)
go(H, [(1.55, 1.85)], t_end=s(173.5), facing=0)          # trapped (816, the tight ch93)
go(MR, [(2.5, 1.2)], t_end=s(177.0), facing=-75)         # her offer
go(MR, [(1.6, 0.9), (0.95, 1.6)], t_start=s(180.0), t_end=s(182.6), facing=-60)   # chorus 2: her key moves to (0.93, 1.66)
go(H, [(0.2, 2.6)], t_end=s(186.0), facing=-20)
go(H, [(0.3, 2.3)], t_end=s(205.0), facing=-100)         # gives in
go(H, [(0.8, 3.0)], t_end=s(209.0), facing=0)            # answering the hits
go(H, [(0.2, 2.3)], t_end=s(214.0), facing=-110)
go(MR, [(0.4, 3.0)], t_start=s(224.6), t_end=s(228.0), facing=0)   # FILM ROUND 220-233: she stays, centre, behind him
leave(MR, 'W-MSL', t_start=s(234.4), extra=[(1.6, 1.9), (2.6, 0.2)])
go(H, [(1.6, 4.1)], t_end=s(224.0), facing=-15)          # to the house (FILM 233: SL of her and James)
leave(H, 'W-DSL', t_start=s(236.2))   # REVIEW 3: off SL, the side Room opens on (James and Burr go DSR)

# the company in the two choruses. FILM ROUND (2026-10-24): ON THE DECK, not the galleries (Review 1 read ironinkpen's
# "second floor"; the clip shows them dancing on the floor round the couple: film 91-120 three SR behind the DSR lamp and
# one SL, 104, 155, 195-220 both sides). Six, as Review 2 cut it: three SR (in from DSR), three SL (in from MSL).
SN_POS = {'ens3': ('W-DSR', (-2.9, 0.4)), 'ens1': ('W-DSR', (-3.4, 1.6)), 'ens2': ('W-DSR', (-3.6, 2.9)),   # farthest first
          'ens8': ('W-MSL', (2.4, -1.2)), 'ens7': ('W-USL', (5.0, -0.8)), 'ens5': ('W-MSL', (4.4, 2.4))}
def sn_on(t_first, look_at, label=False):
    for k, (a, (via, dst)) in enumerate(SN_POS.items()):
        enter(a, via, dst, t_end=t_first + 0.7 * (k % 3), facing=face(dst, look_at), label=lab(a) if label else None)
def sn_off(t_first):
    for k, (a, (via, dst)) in enumerate(SN_POS.items()):
        leave(a, via, t_start=t_first + 0.7 * (2 - k % 3))
def sn_dance(t0, t1, look_at):
    for k, a in enumerate(SN_POS):
        wander(a, t0 + 0.2 * k, t1, every=4.0, look=look_at, ph=k)
sn_on(s(82.0), (0.6, 1.9), label=True)
sn_dance(s(83.0), s(104.0), (0.6, 1.9))
for k, a in enumerate(SN_POS):
    stand(a, s(104.3 + 0.1 * k), facing=face(SN_POS[a][1], (0.4, 1.5)))     # the kiss: they turn on him
sn_dance(s(110.5), s(118.8), (0.3, 1.7))
sn_off(s(119.2))
sn_on(s(183.0), (0.3, 2.3))
sn_dance(s(184.0), s(207.5), (0.3, 2.3))
for k, a in enumerate(SN_POS):
    stand(a, s(208.2 + 0.1 * k), facing=face(SN_POS[a][1], (0.8, 3.0)))     # the answering hits
sn_dance(s(211.0), s(220.0), (0.2, 2.3))
sn_off(s(220.5))

# ======================================================================= 2-05 THE ROOM WHERE IT HAPPENS
r = lambda at: T('2-05', at)
TABLE = (0.0, 0.2)
# FILM ROUND (2026-10-24): the film seats Jefferson at the table's SR side and Madison at its SL side (film 190: Jefferson
# seated SR of the table, Madison leaning on it from SL, Hamilton upstage; 212 and 252 the same) - swapped from Review 2
H_T, J_T, M_T = (0.0, -0.65), (-0.85, 0.3), (0.85, 0.3)
B = 'burr'
# REVIEW 3 (video evidence): the three "entries" into the room. The opening picture - Hamilton and Burr talking while
# Madison and Jefferson talk - is played THREE times, and each time ends with Hamilton, Jefferson and Madison walking into
# the room together the same way (reddit, Jack's notes: on Hamilton's dinner line at the top, on the end of Jefferson's
# list of what he arranged, and on Madison's go / Burr's refusal before chorus 3; a Disney+ clip comment: the opening at
# 0:31 is Hamilton's and Burr's view, 1:55 Jefferson's, 2:41 Madison's, and at 2:57 Hamilton and Burr talk exactly as at
# 0:40, Madison motioning Hamilton to come the same way both times; ironinkpen: the scene rewinds to Hamilton and Burr's
# talk while Madison advises Jefferson, and Burr's refusal matches the moment Hamilton walked away to the dinner).
# Jefferson's approach to Madison is the same both times (reddit: in Jefferson's account and again in Burr's account of
# the invitation): the same path DSR. Burr walks round the lit circle and never crosses it (reddit; ironinkpen: Burr
# wanders round the table asking Hamilton what they said to him, and Hamilton cannot hear him), and Hamilton goes to
# the house's front left (= DR, cue 872) on his line about the banks, not on the click-boom.
# They open talking on the house's right = STAGE LEFT (ironinkpen; the same account puts the 872 DR confrontation at the
# front left, so it counts from the house): they walk on from DSL and stay on the SL half.
H_TALK, B_TALK = (1.9, 2.7), (1.1, 3.5)
H_IN = [(2.0, 1.2), (1.6, -0.6), (0.7, -0.85), H_T]            # Hamilton into the room, from H_TALK (round the SL side)
H_OUT = [(0.7, -0.85), (1.6, -0.6), (2.0, 1.2), H_TALK]         # and back out of it to the same spot
J_DSR, M_DSR = (-2.2, 3.4), (-3.0, 3.7)                         # Jefferson and Madison talking DSR (867.5 Madison DSR)
J_IN = [(-1.6, 2.1), (-1.35, 0.95), J_T]                        # Jefferson into the room from J_DSR (FILM ROUND: his seat is SR)
J_OUT = [(-1.35, 0.95), (-1.6, 2.1), J_DSR]                     # his approach to Madison: the same path, out
M_IN = [(-2.1, 4.2), (-0.4, 3.0), (0.6, 1.6), (1.3, 0.85), M_T]              # Madison across in front of the room to his seat SL
M_OUT = [(1.3, 0.85), (0.6, 1.6), (-0.4, 3.0), (-2.1, 4.2), M_DSR]

# --- Hamilton
enter(H, 'W-DSL', (2.4, 3.3), t_end=r(4.6), facing=face((2.4, 3.3), (3.0, 3.9)))
go(H, [(1.2, 3.0)], t_end=r(14.0), facing=face((1.2, 3.0), (2.0, 3.7)))
go(H, [(2.3, 2.6)], t_end=r(24.0), facing=face((2.3, 2.6), (1.4, 3.3)))
go(H, [(1.4, 2.9)], t_end=r(33.0), facing=face((1.4, 2.9), (2.2, 3.6)))
go(H, [H_TALK], t_end=r(40.0), facing=face(H_TALK, B_TALK))
go(H, H_IN, t_start=r(42.3), t_end=r(46.6), facing=0)                   # ENTRY 1: off to the dinner
go(H, H_OUT, t_start=r(97.3), facing=face(H_TALK, (3.0, 3.7)))         # Jefferson's account: back out (in distress)
go(H, H_IN, t_start=r(114.6), t_end=r(118.4), facing=0)                 # ENTRY 2: the end of Jefferson's list
go(H, H_OUT, t_start=r(156.6), facing=face(H_TALK, B_TALK))            # Madison's account: the talk with Burr again
go(H, H_IN, t_start=r(175.5), t_end=r(179.3), facing=0)                 # ENTRY 3: Madison's go / Burr's refusal
# his line about the banks: the house's front left = DR (872), round the SR side of the table
go(H, [(-1.0, -0.85), (-1.9, 0.6), (-3.2, 2.9)], t_start=r(209.6), t_end=r(213.6), facing=face((-3.2, 2.9), (-2.3, 3.5)))
stand(H, r(221.0), facing=60)
go(H, [(-2.4, 2.3)], t_end=r(226.0), facing=70)        # FILM 212-235: walking, SR of centre, away from Burr
go(H, [(-3.0, 3.2)], t_end=r(231.0), facing=60)
go(H, [(-2.0, 2.8)], t_end=r(236.0), facing=80)

# --- Burr: straight lines (reddit: Burr walks in straight lines, Hamilton in arcs)
enter(B, 'W-DSL', (3.0, 3.9), t_end=r(5.4), facing=face((3.0, 3.9), (2.4, 3.3)))
go(B, [(2.0, 3.7)], t_end=r(14.5), facing=face((2.0, 3.7), (1.2, 3.0)))
go(B, [(1.4, 3.3)], t_end=r(24.5), facing=face((1.4, 3.3), (2.3, 2.6)))
go(B, [(2.2, 3.6)], t_end=r(33.5), facing=face((2.2, 3.6), (1.4, 2.9)))
go(B, [B_TALK], t_end=r(40.5), facing=face(B_TALK, H_TALK))
go(B, [(0.0, 3.9)], t_end=r(46.0), facing=0)                           # alone, DS
go(B, [(1.0, 3.6)], t_end=r(55.0), facing=-15)                         # FILM ROUND: he works the front, straight lines
go(B, [(-0.8, 3.7)], t_end=r(63.0), facing=15)
go(B, [(0.0, 4.9)], t_end=r(72.5), facing=0)                           # chorus 1
go(B, [(1.8, 4.2)], t_end=r(78.0), facing=-20)                         # FILM 75: DSL of centre, the arm up
go(B, [(0.0, 2.4)], t_end=r(85.0), facing=0)                           # FILM 85: in the middle of the four squares
go(B, [(0.2, 3.6)], t_end=r(92.0), facing=0)                           # FILM 92: DC, the arms out
go(B, [(0.0, 4.9)], t_end=r(96.5), facing=0)
stand(B, r(99.0), facing=face((0.0, 4.9), (3.0, 3.7)))                 # watches Jefferson's account (DSL)
stand(B, r(119.0), facing=0)                                            # chorus 2
go(B, [(-0.8, 3.7)], t_end=r(123.0), facing=10)                        # FILM 135: in among the dancing company
go(B, [(0.6, 3.0)], t_end=r(128.0), facing=-10)
go(B, [(0.8, 4.0)], t_end=r(134.0), facing=face((0.8, 4.0), TABLE))   # peers in at the chess game
go(B, [(1.5, 4.1)], t_end=r(145.0), facing=-60)
go(B, [B_TALK], t_start=r(157.0), t_end=r(160.5), facing=face(B_TALK, H_TALK))   # the talk replayed
go(B, [(0.0, 4.9)], t_start=r(175.6), t_end=r(178.0), facing=0)       # his refusal - chorus 3
go(B, [(-1.0, 4.0)], t_end=r(184.0), facing=10)                        # FILM ROUND: straight lines through the chorus
go(B, [(0.8, 3.8)], t_end=r(189.5), facing=-10)
go(B, [(0.0, 4.1)], t_end=r(194.0), facing=0)                          # click-boom
# round the lit circle (r about 2 m from the table), never inside it, asking Hamilton what they said to him (870 on)
go(B, [(0.0, 2.2), (1.45, 1.8), (2.05, 0.4), (1.5, -1.05), (0.0, -1.75), (-1.5, -1.05), (-2.05, 0.4), (-1.45, 1.8),
       (0.0, 2.2)], t_start=r(196.4), t_end=r(209.6), facing=180)
go(B, [(-2.3, 3.5)], t_end=r(214.2), facing=face((-2.3, 3.5), (-3.2, 2.9)))   # after him, DR (872)
stand(B, r(221.0), facing=-90)
go(B, [(-0.6, 3.9)], t_end=r(226.0), facing=-60)                       # FILM 235: across the front, reaching after him
go(B, [(1.4, 3.6)], t_end=r(232.0), facing=-80)
go(B, [(0.4, 3.2)], t_end=r(238.0), facing=-70)
go(B, [(0.0, 2.4)], t_start=r(243.6), facing=0)         # Burr MC, the music slows
go(B, [(-0.9, 2.6)], t_end=r(250.0), facing=15)        # FILM 252: DS of the table, working both sides
go(B, [(0.7, 2.3)], t_end=r(256.0), facing=-15)
go(B, [(-0.8, 2.9)], t_end=r(262.0), facing=15)
go(B, [(0.8, 2.9)], t_end=r(267.0), facing=-15)
go(B, [(0.0, 4.3)], t_end=r(272.5), facing=0)           # Burr DS
go(B, [TABLE], t_end=r(277.9), facing=0)                # up on the table (deck level here)
go(B, [(0.0, 1.2)], t_start=r(294.6), t_end=r(295.2), facing=0, speed=1.8)   # jumps off
go(B, [(0.0, 2.75)], t_end=r(296.1), facing=0)         # SPOT: into 888.01's ch13 at DSC (preset 24) while it holds
go(B, [(-0.6, 2.4)], t_end=r(300.0), facing=10)
go(B, [(0.6, 2.6)], t_end=r(305.0), facing=-10)
go(B, [(0.0, 3.0)], t_end=r(310.0), facing=0)
go(B, [(0.0, 4.3)], t_end=r(314.2), facing=0)           # the final click-boom (SPOT: preset 770 'Burr DSC', ch93 at (0, 4.82))
add(B, r(314.6), 0.0, 4.3, facing=0, dwell=0.55)
go(B, [(-6.0, 4.65), WINGS['W-DSR']], t_end=r(317.5), last_off=True, hold=False)

# --- Jefferson
enter(J, 'D-UC', [(-0.4, -2.2), (-1.0, -1.4), J_T], t_end=r(45.0), facing=face(J_T, H_T), label='Jefferson', t_off=r(39.5))
stand(J, r(50.0), facing=0)                              # the three out front for the company vocal (ironinkpen)
stand(J, r(72.0), facing=face(J_T, H_T))
go(J, [(0.6, 1.2), (3.0, 3.7)], t_end=r(99.5), facing=-20)            # Jefferson's account DSL (867.1)
go(J, [(1.2, 3.9), J_DSR], t_start=r(108.5), t_end=r(112.3), facing=face(J_DSR, M_DSR))   # his approach to Madison
go(J, J_IN, t_start=r(114.8), t_end=r(118.4), facing=face(J_T, H_T))  # ENTRY 2
go(J, J_OUT, t_start=r(152.2), t_end=r(155.4), facing=face(J_DSR, M_DSR))   # the same approach, with the invitation
go(J, J_IN, t_start=r(175.6), t_end=r(179.2), facing=face(J_T, H_T))  # ENTRY 3
stand(J, r(210.0), facing=-120)
stand(J, r(247.0), facing=face(J_T, H_T))

# --- Madison
enter(M, 'D-UC', (1.2, -1.2), t_end=r(39.6), facing=face((1.2, -1.2), H_TALK), label='Madison', t_off=r(36.0))
stand(M, r(40.6), facing=face((1.2, -1.2), H_TALK))   # motions Hamilton to come
go(M, [M_T], t_start=r(42.0), t_end=r(44.4), facing=face(M_T, H_T))   # ENTRY 1
stand(M, r(50.2), facing=0)
stand(M, r(72.2), facing=face(M_T, H_T))
go(M, M_OUT, t_start=r(97.6), facing=face(M_DSR, J_DSR))               # out of the room for Jefferson's account
go(M, M_IN, t_start=r(113.6), t_end=r(118.4), facing=face(M_T, H_T))  # ENTRY 2
go(M, M_OUT, t_start=r(142.0), t_end=r(146.0), facing=20)             # Madison weighs it DSR (867.5)
stand(M, r(155.6), facing=face(M_DSR, J_DSR))                          # Jefferson's invitation
stand(M, r(175.0), facing=face(M_DSR, H_TALK))                         # motions Hamilton to come, as at the top
go(M, M_IN, t_start=r(174.6), t_end=r(179.2), facing=face(M_T, H_T))  # ENTRY 3
stand(M, r(210.2), facing=-150)

# 874 "Lose DR" (REVIEW): Hamilton walks back into the room and leaves Burr outside it; the three stay at the table
# through Burr's build and go upstage on 882 "Burr DS", before 884.
go(H, [(-1.8, 2.0), (-1.6, 0.4), (-0.9, -0.8), H_T], t_start=r(242.5), facing=0)
stand(M, r(247.2), facing=face(M_T, H_T))
leave(H, 'D-UC', t_start=r(271.6), extra=[(0.4, -2.0)])
leave(J, 'D-UC', t_start=r(272.4), extra=[(1.25, -1.2)])
leave(M, 'D-UC', t_start=r(273.4), extra=[(-0.2, -1.0), (0.6, -2.6)])

# REVIEW 3: two of the company up on the gallery shout the city names down (ironinkpen: the ensemble on the second
# floor shouts random names down while Congress fights over the capital; a Disney+ clip comment on the shouted names)
for k, (a, p) in enumerate([('ens9', (-1.6, -3.35, 'g')), ('ens10', (2.2, -3.35, 'g'))]):
    enter(a, 'G-UC', p, t_end=r(149.4 + 0.3 * k), facing=face(p, TABLE), label=lab(a))
    leave(a, 'G-UC', t_start=r(155.6 - 1.2 * k))     # the far one (ens10) first, so they do not pass on the gallery

# the company (REVIEW 2, Jack's verdict): EIGHT bodies (ens1-ens8), not ten, in the shapes ETC's renders of Binkley's real
# cues show (THPP Cue Photos 866-890; research/seg5pics): a line of four with Burr DS (866); four a side down the
# sides of the room with the table between them (867, 868, 870, 872, 876.1, 882 all show the same side groups);
# two fanning lines (884); four round the table (885); a horseshoe round the table with Burr in front (890).
# CUT (invented): the crossing diagonal lines in the three choruses, the arc during Jefferson's account, the
# chess-game ring of eight and its closing, the 194 re-form, the 256.6 loose ring, and the walked 72-degree revolve.
# R1 50.06 "Company vocal": a line of four downstage, Burr in the middle of it
R1 = {'ens1': (-3.2, 3.8), 'ens3': (-1.6, 3.8), 'ens5': (1.6, 3.8), 'ens7': (3.2, 3.8)}
R1via = {'ens1': 'W-DSR', 'ens3': 'W-DSR', 'ens5': 'W-DSL', 'ens7': 'W-DSL'}
R1t = {'ens1': 49.6, 'ens3': 50.1, 'ens5': 50.1, 'ens7': 49.6}
for a in R1:
    enter(a, R1via[a], R1[a], t_end=r(R1t[a]), facing=0, label=lab(a))
# 71.9 "Ensemble X on chairs": the line crosses up to the sides of the room and four more come on - four a side
SIDE = {'ens1': (-3.5, 1.9), 'ens3': (-3.1, 0.9), 'ens2': (-2.6, -0.3), 'ens4': (-2.15, -1.85),
        'ens7': (3.5, 1.9), 'ens5': (3.1, 0.9), 'ens6': (2.7, -0.3), 'ens8': (1.9, -1.6)}
SIDEvia = {'ens2': 'W-USR', 'ens4': 'D-UC', 'ens6': 'W-MSL', 'ens8': 'D-UC'}
LOOKC = (0.0, 1.5)
for k, a in enumerate(['ens1', 'ens3', 'ens5', 'ens7']):
    go(a, [SIDE[a]], t_start=r(71.9 + 0.2 * k), facing=face(SIDE[a], LOOKC))
for k, a in enumerate(['ens2', 'ens6', 'ens4', 'ens8']):
    enter(a, SIDEvia[a], SIDE[a], t_end=r(74.0 + 0.3 * k), facing=face(SIDE[a], LOOKC), label=lab(a))
# they hold the sides of the room to Burr's build, turned to whoever has the moment
# REVIEW 3: re-timed to the replayed scene - Jefferson's approach DSR (109), the talk replayed SL (160.5), the walk-in
# into chorus 3 (176), and Hamilton DR on the banks line (211, not 199.2)
# FILM ROUND (2026-10-24): the film's company is never parked - it dances and shifts through every section (film 120-140,
# 190, 235, 252, 260-268; still only on the four squares of chorus 1, film 85). They keep their side of the room and
# travel round their places, turned to whoever has the moment.
for (s0, s1, at) in [(97.3, 108.6, (3.0, 3.7)), (109.0, 118.2, (-2.6, 3.55)), (118.6, 143.8, LOOKC), (144.2, 160.0, (-3.0, 3.7)),
                     (160.5, 175.6, (1.5, 3.1)), (176.0, 210.5, LOOKC), (211.0, 243.6, (-2.7, 3.2)), (244.0, 271.6, (0.0, 2.4))]:
    for k, a in enumerate(E8):
        stand(a, r(s0 + 0.1 * k), facing=face(SIDE[a], at))
        wander(a, r(s0 + 0.1 * k), r(s1), every=4.5, look=at, ph=k)
for k, a in enumerate(E8):
    stand(a, r(272.0 + 0.1 * k), facing=face(SIDE[a], (0.0, 4.3)))
# 277.9 "Art of Bink": two lines fanning out downstage from the table, Burr at it
srl = [(-1.4, -0.4), (-2.2, 0.4), (-2.9, 1.3), (-3.5, 2.3)]
LN = {'ens4': srl[0], 'ens2': srl[1], 'ens3': srl[2], 'ens1': srl[3]}
for a, b2 in [('ens8', 'ens4'), ('ens6', 'ens2'), ('ens5', 'ens3'), ('ens7', 'ens1')]:
    LN[a] = (-LN[b2][0], LN[b2][1])
for k, a in enumerate(E8):
    go(a, [LN[a]], t_start=r(275.8 + 0.1 * k), t_end=r(277.9 + 0.05 * k), facing=face(LN[a], (0.0, 3.0)))
# 284.4 "Girls Diamonds&Lace": the second and third of each line step in round the table, back for the cloth pull
VT = {'ens2': (-0.8, 0.55), 'ens3': (-1.3, 1.15), 'ens6': (0.8, 0.55), 'ens5': (1.3, 1.15)}
for a in VT:
    go(a, [VT[a]], t_end=r(285.0), facing=face(VT[a], TABLE))
    go(a, [LN[a]], t_start=r(291.4), t_end=r(293.8), facing=face(LN[a], (0.0, 3.0)))
# 296.9 "Dance": a horseshoe round the table, open downstage, Burr in front of it
HS = {'ens1': -145, 'ens3': -110, 'ens2': -70, 'ens4': -30, 'ens8': 30, 'ens6': 70, 'ens5': 110, 'ens7': 145}
for k, a in enumerate(E8):
    p = ring(2.0, HS[a], 0.0, 0.3)
    go(a, [p], t_end=r(298.5 + 0.05 * k), facing=face(p, (0.0, 2.6)))
# the button, then out in the blackout
for k, a in enumerate(E8):
    p = cur(a)
    if p[1] < -0.5:
        via = 'D-UC'
    elif p[0] > 0:
        via = 'W-DSL' if p[1] > 2.0 else 'W-MSL'
    else:
        via = 'W-DSR'
    extra = [(-3.9, 2.6)] if (via == 'W-DSR' and p[1] < 2.2) else None
    leave(a, via, t_start=r(315.0), t_end=r(317.4), extra=extra)

if __name__ == '__main__':
    msgs = checks(verbose=True)
    print(len(msgs), 'messages')
    print({a: len(L) for a, L in W.items()}, sum(len(L) for L in W.values()))

NOTES = (
 "Segment 5 (2-01..2-05). Research, sources and the reviews: research/seg5.md. Generated by tools/blocking/seg5gen.py. "
 "REVIEW 2 (Jack: the ensemble is used too much): eight ensemble (ens1-8), not ten; invented formations cut. "
 "2-01 What'd I Miss: Burr recaps alone DSC and leaves SR; the company (8) comes on for the build to Jefferson and waits on "
 "the floor, kneels scrubbing as Jefferson appears TOP CENTRE on the USG and comes down the SL stair (the real rolling "
 "staircase parks at the SL balcony - PLSN, Korins; ironinkpen, WatchMojo), then stays in place and watches; Sally (ens6) "
 "brings the letter; Madison enters DR, Hamilton and Washington appear DL together for the welcome; one line for the final build. "
 "SIDES (Jack's revision-5 ruling): Jefferson+Madison STAGE RIGHT, Hamilton STAGE LEFT, Washington with Hamilton's side. "
 "2-02 Cabinet Battle #1: Washington MCs at the DSC mic then sits in his chair at the SL vertex of a V of chairs opening to "
 "the house, the eight seated in the V (ironinkpen; chairs are props); debaters' pools at x -/+1.3 z 3.7; "
 "Virginians exit DSR; Washington and Hamilton DC; Washington exits through the upstage door. "
 "2-03 Take a Break (no ensemble): desk SR of centre (THPP 'Desk Mid SR'), the piano SL of centre (a prop; Philip at the keys); "
 "Angelica on the USG, down the SL stair at 164-177; Philip's poem DSC; family exits SL. "
 "2-04 Say No: desk, Burr SR, Maria SL and three street lamps from the THPP cue photos 782/784; her door SL in her key (ch13); "
 "James Reynolds (ens4) DR where preset 769 points; six of the company on the galleries (USG, SR arm, SL gallery) for both "
 "choruses (ironinkpen). "
 "2-05 Room: THPP cue photos 866-892 - a line of four with Burr DS (866), four a side down the sides of the room (867-882), "
 "the round table USC with Jefferson SL / Madison SR / Hamilton upstage of it, Burr+Ham DR at 872, Hamilton back to the table "
 "at 874, the three out upstage on 882, two fanning lines (884), four round the table (885), a horseshoe round the table "
 "for the dance (890), Burr DC at 892; Burr stands at deck level where the table is. "
 "REVIEW 3 (video text: Disney+ clip comments, Ham4Ham captions, ironinkpen, reddit): 2-01 Hamilton takes the hand "
 "Jefferson offers Washington (212-214); 2-04 Burr stays upstage SR watching the whole number and James comes back DSC for "
 "the money on the last line, Hamilton off SL; 2-05 Hamilton and Burr open on SL (the house's right), the opening is "
 "replayed twice (97-118 Jefferson's account, 152-179 Madison's) and each ends with the three walking into the room the "
 "same way (46.6, 118.4, 179.3), Jefferson's approach to Madison DSR the same both times, Burr walks round the lit circle "
 "196.4-209.6 without crossing it, Hamilton goes DR on his banks line (213.6, not 198.9), two of the company shout the "
 "city names from the gallery (149-157). "
 "NOTES3 (Jack, 2026-10-15): 2-01 Jefferson comes out onto the upstage gallery at top centre by 44.0 (was 57.9), in the "
 "lit top-centre pin, and waits there for his descent at 60.8. "
 "NOTES3 (Jack, 2026-10-15): 2-02 Jefferson no longer crosses to centre at 35.6: he stays at his spot SR (-1.3, 3.7) "
 "until 53, and Hamilton's interjection (45.5) is aimed at him there. "
 "FILM ROUND (2026-10-24, the Disney+ frames; research/seg5.md 'Film round'): 2-01 the town on in the recap, Hamilton and "
 "Washington on the gallery 15-27, Burr up the SL stair and off by 40, the company dancing and travelling throughout (two "
 "clusters, the scrub, a line, the party rows, round him, the ring, SL group, upstage line, SR-centre line); 2-02 the "
 "debaters work their own sides (Jefferson back on his spot by 34.5); 2-03 Angelica up by 28.5 and down the SR stair, the "
 "poem beside the piano, the sisters meet SR with Hamilton SL; 2-04 the company on the DECK, the last picture James SR, Maria "
 "centre, Hamilton SL; 2-05 Jefferson at the table's SR side and Madison SL, the company travelling and dancing throughout."
)
if __name__ == '__main__':
    import os
    os.makedirs(SP + '/segments', exist_ok=True)
    dump(SP + '/segments/seg5.json', NOTES)
