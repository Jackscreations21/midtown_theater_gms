# 1-02 Aaron Burr, Sir
from lib import *

def B(at): return S('1-02', at)

TAVERN = []   # REVIEW2 (Jack): no ensemble in Aaron Burr, Sir (was eight of the company filling the tavern)
TABLE = (-1.2, 0.3)    # NOTES3 (Jack): the picnic table, farther toward centre (t103.py and props.py use the same spot)
LAU_V, LAF_V, MUL_V = (-0.5, 1.45), (-1.85, 1.45), (-1.2, -0.85)   # NOTES3: the three verse places, at the table
HAM_L = (1.3, 1.9)     # NOTES3: where Hamilton listens to the verses from (FILM: SL, beside Burr; was (0.75, 2.3))
BURR_L = (2.6, 1.9)    # FILM (frame 545, at 109): Burr SL of Hamilton through the friends' verses (was DSR, (-3.6, 3.6))

def build():
    # FILM ROUND (2026-10-24, research/seg1.md "Film round"): the film plays the street scene at CENTRE and SL, the two
    # men walking it together (frame 96, at 18.4: Burr just SL of centre, Hamilton SL of him, both ~1.5 m up from the
    # lip; frames 425-440, at 84-88: both by the lamp SL as the friends burst in), not in Burr's AF DSR. The
    # followspots (follow.py SEGMENT 1) light them wherever they walk, so the scene no longer waits in the two pools.
    # ---- the street at night (Q80 0.5): Burr strolls on from upstage SL (film frame 30, at 5.5: he comes down from
    # the SL stair's side) to just SL of centre
    move('burr', S('1-01', 234.2), B(4.0), (2.4, -0.4), f=-150)
    move('burr', B(4.6), B(9.0), (0.5, 1.6), f=60)
    # ---- Q81 12.0 Hamilton finds him: from where 1-01 left him (centre, in his light: film frame 10) to SL of him
    # (film 18.4) (was: off DSL in the blackout and back on from there)
    move('hamilton', B(9.0), B(14.4), (2.0, 1.8), f=-100)
    turn(['burr'], B(13.0), 80)
    # the two walk the street as they talk (film: never a stand-off); Hamilton circles him
    move('hamilton', B(22.0), B(24.6), (1.5, 0.8), f=-130)
    move('burr', B(29.0), B(31.4), (-0.1, 2.0), f=60)
    # ---- Q82 37.1 Princeton: Hamilton circles in to him
    move('hamilton', B(37.1), B(39.6), (1.0, 2.5), f=-80)
    move('burr', B(44.0), B(46.4), (-0.6, 1.3), f=70)
    move('hamilton', B(48.0), B(50.8), (0.5, 1.9), f=-100)
    turn(['burr'], B(50.0), 75)
    # ---- Q83 56.0 the drink: Burr leads him SL toward the lamp (the lamp stands at (3.6, 2.2))
    move('burr', B(56.0), B(59.4), (2.3, 1.4), f=-90)
    move('hamilton', B(56.4), B(59.6), (1.3, 2.2), f=110)   # REVIEW: Burr's arm round his shoulders (fan staging account)
    # ---- Q84 62.3 Burr's advice: he steps off a pace, Hamilton walks round him
    move('burr', B(62.3), B(64.0), (2.6, 2.0), f=-110)
    move('hamilton', B(67.0), B(69.4), (0.9, 1.3), f=70)
    move('burr', B(73.0), B(75.4), (2.1, 1.0), f=-130)
    # ---- Q85 79.6 the warning
    turn(['burr'], B(79.6), -150)
    turn(['hamilton'], B(80.0), 40)

    # ---- NOTES2 (Jack): "the street light should come off right before the table comes on": one of the company
    # slips on from SL and takes the lamp off (props.py 'street-lamp', at her side) just before Q86
    put('ens10', B(77.0), WINGS['W_MSL'], off=True); W['ens10'][-1]['d'] = 0
    put('ens10', B(79.8), (4.0, 1.95), f=-90)
    exit_('ens10', B(80.2), 'W_MSL', speed=1.6)
    # ---- Q86 83.4 the friends burst in; the street becomes the tavern
    # REVIEW2 (Jack): the friends carry on a picnic table and the ensemble does NOT come on.
    # NOTES2 (Jack): "the bench should go onto upstage right. two people should carry the table on": Mulligan and
    # Laurens carry it BETWEEN them (RULING FU) from the USR wing, Lafayette a step ahead.
    # NOTES3 (Jack, 2026-10-14): "the table should come in a little farther towards center and the three guys are at
    # the table when they do their parts": it stands at TABLE (-1.2, 0.3) (was (-2.4, -1.0)): x -2.1..-0.3, z -0.48..1.08,
    # the benches included. The carry comes in further upstage (z -1.9) and turns in two steps, so the outer carrier
    # stays clear of the SR stair (x -4.8..-4.2, z -0.25..1.8). Each friend sings his verse AT it: Laurens at the front
    # bench's SL end, Lafayette at its SR end, Mulligan behind it at the centre; Hamilton listens from the DSL diagonal.
    # SPOT: the verse specials (ch51 (2.41, 3.26), ch48 (-2.41, 3.06), ch50 (0.39, 2.44)) no longer land on them: the cue
    # pass re-aims them to the three verse places below.
    # FILM: Burr and Hamilton stay SL by where the lamp stood and watch the friends take the room (frames 425-545)
    move('hamilton', B(84.0), B(85.8), (1.6, 1.3), f=-90)
    move('burr', B(84.0), B(88.0), BURR_L, f=-100)
    put('lafayette', B(82.4), WINGS['W_USR'], off=True); W['lafayette'][-1]['d'] = 0
    via('lafayette', B(85.0), (-4.0, -1.2))                                # ahead of the table, clear of the stair
    put('lafayette', B(88.4), LAF_V, f=60)                                 # the front bench, SR end: his verse place
    pair_carry('mulligan', 'laurens', 1.8, [(B(83.2), (-9.0, -1.9), -90, 'off'), (B(86.0), (-4.6, -1.9), -90, None),
                                            (B(87.6), (-2.8, -1.0), -45, None), (B(89.4), TABLE, 0, 'stop')])
    move('hamilton', B(89.6), B(91.0), HAM_L, f=-45)                       # to the DSL diagonal, watching the table
    # ---- Q87 90.9 Laurens' verse, at the front bench's SL end (round the table's SL corner)
    move('laurens', B(89.6), B(90.3), (0.1, 1.25), d=0)
    put('laurens', B(91.0), LAU_V, f=-10)
    turn(['lafayette'], B(91.2), 75)
    # Mulligan goes round the SR end to the back of the table
    move('mulligan', B(89.8), B(90.9), (-2.45, -0.7), d=0)
    put('mulligan', B(92.2), (-1.55, -0.95), f=50)
    # FILM (frames 481-545): Laurens works the room with his mug, out to centre and back to his place
    move('laurens', B(95.0), B(96.8), (0.3, 0.9), f=-30)
    move('laurens', B(99.0), B(100.6), LAU_V, f=-10)
    # ---- Q88 102.8 Lafayette's verse, at the front bench's SR end
    turn(['lafayette'], B(102.8), 5)
    move('lafayette', B(106.0), B(107.6), (-2.4, 2.0), f=40)               # FILM (frame 620): out a step, mug up
    move('lafayette', B(110.6), B(112.0), LAF_V, f=20)
    turn(['laurens'], B(103.0), -75)
    turn(['mulligan'], B(103.2), -20)
    # ---- Q89 115.6 Mulligan's verse, behind the table at its centre
    move('mulligan', B(115.0), B(115.8), MUL_V, f=0)
    turn(['laurens'], B(115.8), -150)
    turn(['lafayette'], B(115.8), 150)
    turn(['hamilton'], B(115.8), -60)
    move('mulligan', B(119.0), B(120.4), (-0.45, -0.75), f=10)             # along the back of the table and back
    move('mulligan', B(123.0), B(124.4), MUL_V, f=0)
    # ---- Q90 127.6 the toast: the four round the table
    move('hamilton', B(127.6), B(129.2), (0.1, 0.45), f=-80)               # the SL end
    move('lafayette', B(127.6), B(128.8), (-2.5, 0.45), f=80)              # the SR end
    turn(['laurens'], B(128.0), -20)
    turn(['mulligan'], B(128.0), 0)
    # ---- Q91 133.7 they turn on Burr
    # FILM: Burr keeps his distance from the rowdy table, drifting SL and back while they sing (frames 545-640)
    move('burr', B(104.0), B(106.4), (3.2, 0.9), f=-110)
    move('burr', B(121.0), B(123.6), (2.4, 2.3), f=-120)
    # FILM (frame 745, at 149): by the end Burr is on the SR side: he crosses as they turn on him
    move('burr', B(132.4), B(136.0), (-1.85, 4.15), f=45)   # SPOT: into his AF (ch2)
    turn(['hamilton', 'laurens', 'lafayette', 'mulligan'], B(134.6),
         lambda a, p: face_to(p, (-1.85, 4.15), 120))
    # ---- Q92 139.6 Burr sits it out: back to his corner
    move('burr', B(139.6), B(141.6), (-4.2, 4.1), f=40)
    turn(['laurens', 'lafayette', 'mulligan'], B(141.8), lambda a, p: face_to(p, TABLE, 110))
    turn(['hamilton'], B(141.8), 0)
    # ---- Q93 151.6 Hamilton steps up: the vamp into My Shot
    # SPOT: his DSC special is ch13 at (0, 2.40): he steps down from the table's SL end on Q92 and forward into it on
    # Q93 (just downstage of the picnic table)
    move('hamilton', B(142.4), B(143.6), (0.0, 1.7), f=0)
    move('hamilton', B(151.6), B(152.8), (0.05, 2.35), f=0)
    turn(['laurens', 'lafayette', 'mulligan'], B(152.4), lambda a, p: face_to(p, (0.05, 2.35), 120))
