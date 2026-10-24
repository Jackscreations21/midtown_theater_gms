# 1-04 The Story of Tonight
from lib import *

def T(at): return S('1-04', at)

FOUR = ['lafayette', 'hamilton', 'laurens', 'mulligan']   # REVIEW: Laurens beside him (fan account); no crossing out of My Shot

def place(ps, tl, ta, fs):
    for a, p, f in zip(FOUR, ps, fs):
        move(a, tl, ta, p, f=f)

# NOTES3 (Jack, 2026-10-14): "find a better way for the chairs to come off like maybe at the end they stand up and move
# forward and it is just spotlights on them and ensemble members go and take the chairs off. find a better transition into
# the next song. they come off too early." So the four sit more of the song (back in their chairs at Q143 and again after
# the last raise), and on the last line (Q147 83.8, "fade to the friends") they stand up and come forward into a line DS,
# where the cue pass puts a special on each (FWD below); behind them four of the company come on in the dark and take the
# chairs off (props.py tavern-chair-1..4: ens9, ens10 from DSR, ens6, ens7 from DSL), and ens3 the candle table (D-UC).
# The four hold DS through the song's end and walk off DSL in 1-05's first seconds, as Burr runs on from USL (t105).
P140 = [(-1.26, 3.47), (-0.39, 3.78), (0.49, 3.79), (1.37, 3.48)]   # at their chairs (the chair 0.7 m behind)
F140 = [20, 5, -5, -20]
FWD = [(-1.3, 4.35), (-0.45, 4.6), (0.45, 4.6), (1.35, 4.35)]      # NOTES3: the line DS on the last line (specials wanted)
# who takes each chair off (tavern-chair-1..4, FOUR's order), from and back to which wing, and where she stands to lift it
# and when she leaves the wing (the one going farther leaves first, so the two from one wing do not walk on together)
STRIKERS = [('ens9', 'W_DSR', (-1.65, 2.4), 84.8), ('ens10', 'W_DSR', (-0.55, 2.62), 84.0),
            ('ens6', 'W_DSL', (0.65, 2.63), 84.2), ('ens7', 'W_DSL', (1.75, 2.4), 85.0)]


def build():
    # ---- Q140 0.0 the four by candlelight round their chairs DSC (they settle in the blackout)
    # SPOT: four warm pools, one per chair, held all song: ch48 (-1.26, 3.47), ch49 (-0.39, 3.78), ch50 (0.49, 3.79),
    # ch51 (1.37, 3.48), r 0.77. Each friend keeps to his own pool; the shapes below are small moves inside them.
    place(P140, S('1-03', 331.4), T(0.8), F140)
    # FILM ROUND (2026-10-24; film 1-04 frame 40, at 8): only Lafayette and Laurens sit; Mulligan and Hamilton are up
    # and about, talking over them (dance.py: the Q140 sit is theirs alone now). They step out downstage of the row
    # (the chairs stand behind it).
    move('mulligan', T(4.0), T(5.6), (1.7, 4.2), f=-70)
    move('hamilton', T(6.0), T(7.4), (-0.2, 4.4), f=30)
    # ---- Q141 16.0 the round: they draw together, a half-circle open to the house
    place([(-1.3, 3.65), (-0.4, 3.45), (0.5, 3.45), (1.4, 3.65)], T(16.0), T(17.6), [45, 20, -20, -45])
    # ---- Q142 22.9 the first toast: up in a line, raised
    place([(-1.26, 3.8), (-0.39, 3.85), (0.49, 3.85), (1.37, 3.8)], T(22.9), T(24.4), [0, 0, 0, 0])
    # FILM (frame 150, at 30): Laurens toasts from apart, across the stage SL, the other three together ("he's standing
    # on the other side", a clip comment: the one who will not survive); he goes round the front of Mulligan
    move('laurens', T(26.0), T(27.0), (1.0, 3.1), d=0)
    put('laurens', T(28.6), (3.0, 3.2), f=-95)
    # ---- Q143 35.1 back to the four. FILM ROUND (frame 240, at 47): they do NOT sit again here (NOTES3 had them back
    # in their chairs to Q145): they stand and talk in two pairs, the wine going round (dance.py); Laurens comes back in
    move('laurens', T(35.1), T(37.0), (1.0, 3.0), f=70)
    move('lafayette', T(35.4), T(36.8), (-1.6, 3.2), f=75)
    move('hamilton', T(35.6), T(37.0), (-0.8, 3.4), f=-100)
    move('mulligan', T(37.5), T(38.6), (1.9, 3.3), f=-100)
    move('hamilton', T(46.0), T(47.2), (-0.5, 3.0), f=60)        # he turns out to the other pair (film 240)
    move('lafayette', T(51.0), T(52.4), (-1.5, 3.7), f=40)
    # REVIEW: the four are the only ones on stage (fan staging account); the company's hum is offstage
    # ---- Q145 59.0 the second toast to the friends: up again
    place([(-1.3, 3.6), (-0.4, 3.5), (0.5, 3.5), (1.4, 3.6)], T(59.0), T(60.4), [40, 15, -15, -40])
    # ---- Q146 73.5 the last raise: the four close up DSC
    place([(-1.2, 3.6), (-0.38, 3.85), (0.47, 3.85), (1.3, 3.6)], T(73.5), T(75.0), [0, 0, 0, 0])
    # NOTES3: then back into their chairs for the song's last lines (dance.py: sit to Q147)
    place(P140, T(78.0), T(79.4), F140)
    # ---- Q147 83.8 fade to the friends: they stand up and come forward into a line DS (SPOT: a special on each, FWD)
    place(FWD, T(84.2), T(86.0), [0, 0, 0, 0])
    # the company takes the chairs off behind them in the dark (props.py SEGMENT 1) and the candle table up the centre
    for k, (e, wg, q, t0) in enumerate(STRIKERS):
        put(e, T(t0), WINGS[wg], off=True); W[e][-1]['d'] = 0
        put(e, T(88.0 + 0.2 * k), q, f=face_to(q, P140[k]))
        exit_(e, T(88.4 + 0.2 * k), wg, speed=1.6)
    put('ens3', T(84.6), WINGS['D_UC'], off=True); W['ens3'][-1]['d'] = 0
    put('ens3', T(88.4), (0.0, 2.1), f=0)
    exit_('ens3', T(88.8), 'D_UC', speed=1.8)                 # off before t105 parks him in his 1-05 wing (2.2)
    # ---- 1-05 0.0: the four walk off DSL together, SL end first, as Burr runs on from USL to DSR (t105)
    for k, a in enumerate(['mulligan', 'laurens', 'hamilton', 'lafayette']):
        exit_(a, S('1-05', 0.0 + 0.2 * k), 'W_DSL', speed=1.6)
