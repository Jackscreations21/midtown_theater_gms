"""Generator for segment 6 (2-06 .. 2-10). Writes segments/seg6.json (notes from seg6-notes.txt)."""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "segments", "seg6.json")
os.makedirs(os.path.join(HERE, "segments"), exist_ok=True)
NOTES = os.path.join(HERE, "seg6-notes.txt")
LEN = {"2-06": 63.0, "2-07": 142.0, "2-08": 181.0, "2-09": 296.0, "2-10": 97.0}
ORDER = ["2-06", "2-07", "2-08", "2-09", "2-10"]

ENT = {
    "W-DSR": (-7.3, 4.6), "W-DSL": (7.3, 4.6), "W-MSR": (-8.5, 0.0), "W-MSL": (8.0, -0.5),
    "W-USR": (-8.5, -3.0), "W-USL": (8.5, -3.0), "D-UC": (1.25, -4.9), "G-UC": (0.6, -4.8),
}
PASS = (0.6, -3.35)  # where the backstage passage meets the USG
C = (0.0, 0.95)
W = {}


def face(a, b, cheat=0.7):
    """Facing from point a towards point b, cheated to `cheat` of the full turn (towards the house)."""
    ang = math.degrees(math.atan2(b[0] - a[0], b[1] - a[1]))
    return round(ang * cheat, 1)


def wp(actor, track, at, x, z, facing=None, dwell=None, off=False, y=None, label=None):
    while at > LEN[track]:
        at -= LEN[track]
        track = ORDER[ORDER.index(track) + 1]
    while at < 0:   # FILM ROUND: an entrance that starts in the change before its track
        track = ORDER[ORDER.index(track) - 1]
        at += LEN[track]
    p = {"track": track, "at": round(at, 2), "x": round(x, 3), "z": round(z, 3)}
    if y is not None:
        p["y"] = y
    if dwell is not None:
        p["dwell"] = dwell
    if facing is not None:
        p["facing"] = facing
    if off:
        p["off"] = True
    if label:
        p["label"] = label
    W.setdefault(actor, []).append(p)


def off(actor, track, at, ent, label=None):
    x, z = ENT[ent]
    wp(actor, track, at, x, z, off=True, y="gallery" if ent == "G-UC" else None, label=label)


def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def route(ent, target):
    """Via points from the entrance to the target, round the stairs and the wing posts."""
    if ent == "W-DSR":
        return [(-5.9, 4.55)]
    if ent == "W-DSL":
        return [(5.9, 4.55)]
    if ent == "W-MSR":
        return [(-4.1, -0.6)]
    if ent == "W-MSL":
        return [(4.9, -0.2)]
    if ent == "W-USR":
        return [(-4.9, -3.2)]
    if ent == "W-USL":
        v = [(5.2, -3.1)]
        if target[1] > -2.15:
            v.append((4.7, -2.0))
        elif target[0] < 2.3:
            v.append((2.0, -3.1))
        return v
    if ent == "D-UC":
        v = [(1.25, -3.9)]
        if abs(target[0]) < 0.3 and target[1] > -1.0:
            v.append((0.0, -2.4))
        return v
    return []


def plen(pts):
    return sum(dist(a, b) for a, b in zip(pts, pts[1:]))


def enter(actor, track, t_arr, ent, target, facing, label=None, speed=1.3):
    pts = [ENT[ent]] + route(ent, target) + [target]
    t0 = t_arr - plen(pts) / speed
    off(actor, track, t0, ent, label)
    t = t0
    for k in range(1, len(pts) - 1):
        t += dist(pts[k - 1], pts[k]) / speed
        wp(actor, track, t, pts[k][0], pts[k][1], dwell=0)
    wp(actor, track, t_arr, target[0], target[1], facing=facing)
    return t0


def leave(actor, track, t_leave, frm, ent, speed=1.3):
    pts = [frm] + list(reversed(route(ent, frm))) + [ENT[ent]]
    wp(actor, track, t_leave, frm[0] + 0.001, frm[1], dwell=0)
    t = t_leave
    for k in range(1, len(pts) - 1):
        t += dist(pts[k - 1], pts[k]) / speed
        wp(actor, track, t, pts[k][0], pts[k][1], dwell=0)
    t += dist(pts[-2], pts[-1]) / speed
    off(actor, track, t, ent)
    return t


def gal_enter(actor, track, t0, spot, facing, label=None, speed=1.3):
    """Up the backstage stair (offstage) and through the passage onto the USG at `spot` (x, z)."""
    off(actor, track, t0, "G-UC", label)
    t1 = t0 + 1.3
    wp(actor, track, t1, PASS[0], PASS[1], dwell=0, y="gallery")
    t2 = t1 + max(0.8, dist(PASS, spot) / speed)
    wp(actor, track, t2, spot[0], spot[1], facing=facing, y="gallery")
    return t2


def gal_enter_all(track, t_first, spots, facing, labels=False):
    """Farthest first through the passage, 1.0 s apart."""
    order = sorted(spots, key=lambda a: -dist(PASS, spots[a]))
    for k, a in enumerate(order):
        gal_enter(a, track, t_first + 1.0 * k, spots[a], facing,
                  label=("Ensemble " + a[3:]) if labels else None)


def gal_exit_all(track, t_first, spots, speed=1.5):
    """Nearest first along the USG to the passage and off at G-UC, 1.2 s apart at the passage."""
    order = sorted(spots, key=lambda a: dist(PASS, spots[a]))
    for k, a in enumerate(order):
        sp = spots[a]
        t_go = t_first + 1.2 * k
        t_pass = t_go + max(0.6, dist(PASS, sp) / speed)
        wp(a, track, t_go, sp[0] + 0.001, sp[1], dwell=0, y="gallery")
        wp(a, track, t_pass, PASS[0], PASS[1], dwell=0, y="gallery")
        off(a, track, t_pass + 1.1, "G-UC")


def lean(base, toward, d):
    vx, vz = toward[0] - base[0], toward[1] - base[1]
    n = math.hypot(vx, vz) or 1
    return (base[0] + d * vx / n, base[1] + d * vz / n)


# FILM ROUND (2026-10-24): every number re-read against the Disney+ film's frames (research/seg6.md "Film round").
# Positions below that say FILM are read off its wide shots at the album time given; the cue-round pins they replace
# are in the git history. The followspots now light the principals (follow.py SEGMENT 6), so nobody is held to a
# reconstructed special any more where the film puts them elsewhere.
PROPT = {}   # prop timings for props.py SEGMENT 6 (printed on a run; keep the two in step)

# ---------------------------------------------------------------- 2-06 Schuyler Defeated
# FILM (2-06 clip): Eliza and Philip read the paper shoulder to shoulder at the gallery rail (18-24); Burr is on the
# deck, Hamilton comes to him; Burr is on HAMILTON'S RIGHT, i.e. Burr SR, Hamilton SL (31.9 and 44.0, two cameras),
# 1.5 m apart, mid-stage. Behind them the company brings on the Windsor chairs for Cabinet Battle #2 and sets them (from
# about 31 s to the end); at the button Burr is still there among the chairs and Hamilton walks away SL (62.2).
T = "2-06"
gal_enter("eliza", T, 0.0, (-0.35, -3.35), 40, label="Eliza")
gal_enter("laurens", T, 0.6, (0.35, -3.35), -40, label="Philip")
wp("laurens", T, 9.0, 0.35, -3.2, facing=-20, y="gallery")        # FILM: to the rail, reading out
wp("eliza", T, 11.0, -0.3, -3.2, facing=30, y="gallery")          # leans in to read it with him
wp("laurens", T, 17.0, 0.45, -3.15, facing=-45, y="gallery")      # turns to her
wp("eliza", T, 19.0, -0.35, -3.25, facing=50, y="gallery")
wp("laurens", T, 22.7, 0.4, -3.1, facing=-10, y="gallery")        # both look down at Burr
wp("eliza", T, 23.0, -0.35, -3.15, facing=10, y="gallery")
wp("eliza", T, 26.5, -0.35, -3.2, facing=60, y="gallery")
gal_exit_all(T, 27.0, {"laurens": (0.4, -3.1), "eliza": (-0.35, -3.2)})

# Burr: FILM, SR of Hamilton, mid-stage; never still for long (the handkerchief, a step, a turn).
enter("burr", T, 22.7, "W-MSR", (-0.9, 2.6), 30, label="Burr")
wp("burr", T, 26.5, -1.3, 2.9, facing=10)
wp("burr", T, 31.5, -0.9, 2.5, facing=80)                          # Hamilton is on him
wp("burr", T, 38.0, -0.7, 2.4, facing=70)
wp("burr", T, 44.0, -1.0, 2.55, facing=85)                         # FILM 44.0: the handkerchief up, at Hamilton
wp("burr", T, 50.0, -0.8, 2.65, facing=60)
wp("burr", T, 56.0, -1.1, 2.7, facing=80)
wp("burr", T, 60.0, -0.45, 2.8, facing=70)                         # the warning, at Hamilton's back
wp("burr", T, 62.6, -0.45, 2.81, facing=40, dwell=0)

# Hamilton: in from SL to Burr's left (FILM 31.9), turns away on the crack, walks off towards SL on the button
# (FILM 62.2) and stays on there, in the dark, for Cabinet Battle #2.
enter("hamilton", T, 30.6, "W-MSL", (0.75, 2.6), -80, label="Hamilton")
wp("hamilton", T, 36.0, 0.6, 2.4, facing=-95)
wp("hamilton", T, 41.0, 0.45, 2.55, facing=-80)                    # closes in
wp("hamilton", T, 46.0, 0.8, 2.7, facing=-70)
wp("hamilton", T, 51.0, 1.1, 2.9, facing=120)                      # the crack: turns away
wp("hamilton", T, 56.0, 1.0, 2.75, facing=-60)                     # looks back
wp("hamilton", T, 59.0, 1.05, 2.8, facing=60, dwell=0)
wp("hamilton", T, 62.8, 3.4, 2.3, facing=-60)                      # FILM 62.2: walking away SL

# ---------------------------------------------------------------- 2-07 Cabinet Battle #2
# Jack's ruling (cue revision 5, PR #233) stands and the film agrees: Jefferson and Madison STAGE RIGHT, Hamilton
# STAGE LEFT for the battle. FILM (2-07 clip, wide shots at 11.6, 13.6, 53.8, 68.8, 89, 101.5, 107.6, 114.6, 139.6):
#  - the company sits in the Windsor chairs set in 2-06, Burr among them SR; two more watch from the upstage gallery;
#  - Washington SITS in a gilt armchair upstage of centre for both verses (seen seated at 53.8 / 56.6, standing beside
#    it at 93.7), stands centre to hand over (68.8) and to rule (101.5-111.6);
#  - Jefferson does not keep to his side: he crosses into Hamilton's face for most of his verse (34.6, 48.6, 53.8) and
#    Hamilton raps at him across centre (80-89);
#  - the company rises (101.5) and clears with the chairs as Washington goes off SR (111.6-114.6);
#  - the two then SWAP SIDES: Hamilton SR, Jefferson SL (114.6-139.6), and close in to face to face at centre;
#  - Washington calls from the DSR corner (139.6), the two go off SR; Burr watches from the SL doorway (141.8).
T = "2-07"
CB2_SR = [(-3.1, 1.45), (-2.4, 0.5), (-1.7, -0.45)]
CB2_SL = [(1.7, -0.45), (2.4, 0.5), (3.1, 1.45)]
CB2_LOOK = (0.0, 3.2)
WSEAT = (0.3, -0.15)    # Washington's armchair (props cb2-armchair)
BSEAT = (-3.9, 0.3)     # Burr's chair (props cb2-chair-burr)
CB2 = {  # id: (seat, wing, arrival IN 2-06) -- the chairs: props.py SEGMENT_6 cb2-chair-<n>
    "ens1": (CB2_SR[0], "W-DSR", 36.0), "ens2": (CB2_SR[1], "W-MSR", 37.2), "ens3": (CB2_SR[2], "W-USR", 38.4),
    "ens4": (CB2_SL[0], "W-USL", 38.0), "ens5": (CB2_SL[1], "W-MSL", 39.4), "ens6": (CB2_SL[2], "W-DSL", 36.6),
}
CB2_OUT = {"ens1": 111.4, "ens2": 111.8, "ens3": 112.6, "ens4": 112.2, "ens5": 111.6, "ens6": 112.0}

for a, (seat, ent, arr) in CB2.items():          # 2-06: FILM, the chairs come on behind Burr and Hamilton
    k = int(a[3:])
    t0 = enter(a, "2-06", arr, ent, seat, face(seat, CB2_LOOK, 1.0), label="Ensemble " + a[3:])
    PROPT["cb2-chair-%d" % k] = [round(t0, 2), arr]
    s2 = (seat[0] + (0.8 if seat[0] < 0 else -0.8), seat[1] + 0.55)
    s3 = (seat[0], seat[1] + 0.9)
    wp(a, "2-06", 42.0 + 0.4 * k, s3[0], s3[1], facing=face(s3, seat, 1.0))          # FILM: setting the chairs, squaring
    wp(a, "2-06", 48.0 + 0.4 * k, s2[0], s2[1], facing=face(s2, (0.0, 2.6), 1.0))    # them up, the next one along
    wp(a, "2-06", 55.0 + 0.4 * k, seat[0], seat[1], facing=face(seat, CB2_LOOK, 1.0))
# Burr's chair and Washington's armchair, brought in the same change (FILM 62.2: the armchair upstage centre)
t0 = enter("ens7", "2-06", 45.0, "W-MSR", BSEAT, 60, label="Ensemble 7")
PROPT["cb2-chair-burr"] = [round(t0, 2), 45.0]
leave("ens7", "2-06", 46.2, BSEAT, "W-MSR")
t0 = enter("ens8", "2-06", 49.0, "D-UC", WSEAT, 0, label="Ensemble 8")
PROPT["cb2-armchair"] = [round(t0, 2), 49.0]
leave("ens8", "2-06", 50.2, WSEAT, "D-UC")

enter("washington", T, 4.0, "D-UC", C, 0, label="Washington")
wp("washington", T, 6.0, 0.001, 0.95, facing=54)                   # REVIEW 3: hands Hamilton his mic
wp("washington", T, 12.4, -0.3, 0.95, facing=-55)                  # hands Jefferson the floor (FILM 11.6, 13.6)
wp("washington", T, 15.6, -0.3, 0.951, facing=-30, dwell=0)
wp("washington", T, 18.5, WSEAT[0], WSEAT[1], facing=10)           # FILM 53.8: seated in his armchair
wp("washington", T, 66.0, WSEAT[0] + 0.001, WSEAT[1], facing=10, dwell=0)
wp("washington", T, 68.5, -0.2, 2.0, facing=-60)                   # FILM 68.8: up, centre, between them
wp("washington", T, 72.0, 0.2, 2.1, facing=60)                     # gives Hamilton the floor
wp("washington", T, 74.6, 0.21, 2.1, facing=60, dwell=0)
wp("washington", T, 77.0, WSEAT[0], WSEAT[1], facing=20)           # back to the armchair
wp("washington", T, 93.0, WSEAT[0] + 0.001, WSEAT[1], facing=30, dwell=0)
wp("washington", T, 93.8, 0.75, 0.15, facing=50)                   # FILM 93.7: up beside the armchair, cutting in
wp("washington", T, 98.0, 0.751, 0.15, facing=20, dwell=0)
wp("washington", T, 100.5, 0.0, 1.7, facing=0)                     # FILM 101.5: rules, centre
wp("washington", T, 104.0, -0.05, 1.9, facing=-45)
wp("washington", T, 107.6, 0.05, 1.9, facing=40)                   # FILM 107.6: between them
wp("washington", T, 110.0, -0.1, 1.8, facing=-60)
leave("washington", T, 110.8, (-0.1, 1.8), "W-DSR")                # FILM 114.6: gone SR with the company
enter("washington", T, 139.2, "W-DSR", (-5.5, 4.45), 100)          # FILM 139.6: calls from the DSR corner
leave("washington", T, 141.0, (-5.5, 4.45), "W-DSR")

# Jefferson (lafayette) with Madison (mulligan): in from the DR wing for the roll call (FILM 4.8: already there).
enter("lafayette", T, 3.5, "W-DSR", (-1.6, 1.9), 40, label="Jefferson")
wp("lafayette", T, 13.6, -1.8, 1.8, facing=20)                     # FILM 13.6
wp("lafayette", T, 17.0, -2.2, 2.6, facing=30)                     # his verse: the DR side to start
wp("lafayette", T, 23.5, -1.2, 2.4, facing=60)
wp("lafayette", T, 30.0, 0.3, 2.3, facing=80)                      # FILM 32-34.6: across into Hamilton's face
wp("lafayette", T, 34.6, 0.7, 2.2, facing=90)
wp("lafayette", T, 39.0, -0.6, 2.6, facing=40)
wp("lafayette", T, 44.0, 0.2, 2.8, facing=70)
wp("lafayette", T, 48.6, 0.65, 2.3, facing=90)                     # FILM 48.6: at him again
wp("lafayette", T, 53.8, 0.2, 2.6, facing=60)                      # FILM 53.8: mid-stage, the room round him
wp("lafayette", T, 57.0, -0.1, 2.9, facing=10)                     # FILM 56.6: the pose to the house
wp("lafayette", T, 62.0, -0.9, 2.5, facing=40)
wp("lafayette", T, 66.0, -1.2, 2.2, facing=60)
wp("lafayette", T, 68.8, -1.0, 2.0, facing=70)                     # FILM 68.8: beside Washington
wp("lafayette", T, 74.0, -0.7, 2.1, facing=80)                     # arms folded, Hamilton comes at him
wp("lafayette", T, 80.0, -0.75, 2.05, facing=90)                   # FILM 80: Hamilton's finger in his face
wp("lafayette", T, 86.0, -0.4, 2.2, facing=70)
wp("lafayette", T, 89.0, -0.5, 2.0, facing=60)                     # FILM 89: centre-SR, arms crossed
wp("lafayette", T, 95.0, -0.9, 2.2, facing=50)
wp("lafayette", T, 101.5, -1.0, 1.9, facing=70)                    # FILM 101.5 / 107.6
wp("lafayette", T, 107.6, -1.0, 1.95, facing=80)
wp("lafayette", T, 110.0, -0.9, 1.4, dwell=0)                      # FILM 111.6: behind Washington to SL
wp("lafayette", T, 111.6, 0.35, 0.95, dwell=0)
wp("lafayette", T, 114.6, 1.6, 2.6, facing=-90)                    # FILM 114.6: the sides swapped
wp("lafayette", T, 119.0, 1.4, 2.8, facing=-95)
wp("lafayette", T, 124.0, 1.1, 2.7, facing=-80)
wp("lafayette", T, 129.0, 0.9, 2.9, facing=-90)
wp("lafayette", T, 134.0, 0.65, 2.85, facing=-85)
wp("lafayette", T, 139.6, 0.4, 2.9, facing=-90)                    # FILM 139.6: face to face at centre

enter("mulligan", T, 4.3, "W-DSR", (-2.6, 1.7), 40, label="Madison")
wp("mulligan", T, 13.6, -2.6, 1.6, facing=40)                      # FILM 13.6: at Jefferson's shoulder
wp("mulligan", T, 17.0, -2.9, 2.2, facing=30)
wp("mulligan", T, 24.0, -2.2, 2.7, facing=50)
wp("mulligan", T, 30.0, -0.9, 2.75, facing=70)                     # FILM 34.6: behind Jefferson in Hamilton's face
wp("mulligan", T, 34.6, -0.6, 2.6, facing=80)
wp("mulligan", T, 40.0, -1.6, 2.95, facing=50)
wp("mulligan", T, 48.6, -0.5, 2.95, facing=80)
wp("mulligan", T, 54.0, -1.5, 2.5, facing=60)
wp("mulligan", T, 60.0, -1.0, 3.0, facing=40)
wp("mulligan", T, 66.0, -2.0, 1.9, facing=50)
wp("mulligan", T, 72.0, -2.9, 1.3, facing=60)                      # FILM 89: standing SR among the chairs
wp("mulligan", T, 82.0, -2.75, 1.45, facing=70)
wp("mulligan", T, 92.0, -2.95, 1.35, facing=60)
wp("mulligan", T, 100.0, -2.5, 1.6, facing=70)
wp("mulligan", T, 104.0, -2.1, 1.75, facing=60)                    # FILM 107.6: beside Jefferson
leave("mulligan", T, 109.6, (-2.1, 1.75), "W-DSR")                 # FILM 114.6: off SR with the company

# Hamilton: from the SL edge to Washington for his mic (REVIEW 3), the SL side; then across to SR after the ruling.
wp("hamilton", T, 2.8, 3.4, 2.31, facing=-90, dwell=0)
wp("hamilton", T, 6.0, 0.55, 1.4, facing=-129)                     # REVIEW 3: takes his mic from Washington at C
wp("hamilton", T, 9.2, 2.4, 1.9, facing=-60)                       # FILM 11.6 / 13.6
wp("hamilton", T, 17.0, 1.5, 2.1, facing=-80)                      # FILM 34.6: arms folded, Jefferson in his face
wp("hamilton", T, 26.0, 1.65, 2.2, facing=-70)
wp("hamilton", T, 33.0, 1.45, 2.05, facing=-100)
wp("hamilton", T, 41.0, 1.9, 2.4, facing=-60)
wp("hamilton", T, 48.0, 1.5, 2.1, facing=-90)
wp("hamilton", T, 56.0, 1.75, 2.3, facing=-70)
wp("hamilton", T, 63.0, 1.95, 2.0, facing=-50)
wp("hamilton", T, 68.8, 0.6, 2.0, facing=-60)                      # FILM 68.8
wp("hamilton", T, 72.0, 0.9, 2.4, facing=-30)                      # his answer
wp("hamilton", T, 76.0, 0.3, 2.5, facing=-80)
wp("hamilton", T, 80.0, 0.0, 2.4, facing=-90)                      # FILM 80: the finger in Jefferson's face
wp("hamilton", T, 82.1, 0.6, 2.6, facing=-20)                      # the outburst: jumps on the spot (dance.py)
wp("hamilton", T, 86.0, 1.4, 2.9, facing=-40)
wp("hamilton", T, 89.0, 1.0, 2.6, facing=-60)                      # FILM 89: centre-SL, mid-stage
wp("hamilton", T, 92.5, 1.0, 1.05, facing=-160)                    # FILM 93.7: at Washington as he cuts in
wp("hamilton", T, 96.0, 1.2, 1.6, facing=-120)
wp("hamilton", T, 100.0, 1.6, 2.0, facing=-80)
wp("hamilton", T, 104.0, 1.7, 2.05, facing=-90)
wp("hamilton", T, 107.6, 1.8, 2.0, facing=-80)                     # FILM 107.6
wp("hamilton", T, 110.4, 1.2, 2.3, dwell=0)                        # FILM 111.6: walks to centre, then across
wp("hamilton", T, 112.4, 0.0, 3.05, dwell=0)
wp("hamilton", T, 114.6, -1.0, 2.6, facing=80)                     # FILM 114.6: SR now
wp("hamilton", T, 119.0, -1.2, 2.8, facing=90)
wp("hamilton", T, 124.0, -0.75, 2.7, facing=80)
wp("hamilton", T, 129.0, -0.9, 2.9, facing=95)
wp("hamilton", T, 134.0, -0.6, 2.9, facing=85)
wp("hamilton", T, 139.6, -0.4, 2.9, facing=90)                     # FILM 139.6: face to face
wp("hamilton", T, 140.3, -0.41, 2.9, facing=-100, dwell=0)          # Washington calls
leave("hamilton", T, 140.7, (-0.41, 2.9), "W-DSR")                 # off with him SR

# Burr: from his 2-06 place to his chair SR (round the outside of ens1's seat), seated with the company, up at 100.5
# and off SR with his chair; FILM 141.8: watching from the SL doorway as the two face off.
wp("burr", T, 1.2, -4.3, 2.0, dwell=0)
wp("burr", T, 3.0, BSEAT[0], BSEAT[1], facing=face(BSEAT, CB2_LOOK, 1.0))
wp("burr", T, 16.6, BSEAT[0], BSEAT[1] + 0.001, facing=face(BSEAT, (0.4, 2.3), 1.0))
wp("burr", T, 70.5, BSEAT[0] + 0.001, BSEAT[1], facing=face(BSEAT, (0.6, 2.4), 1.0))
wp("burr", T, 101.0, BSEAT[0], BSEAT[1] + 0.002, facing=face(BSEAT, (0.0, 1.8), 1.0))
tl = leave("burr", T, 110.6, (BSEAT[0], BSEAT[1] + 0.002), "W-MSR")   # with his chair
PROPT["cb2-chair-burr"] += [110.6, round(tl, 2)]
enter("burr", T, 137.6, "W-USL", (4.4, -1.4), -120)               # FILM 141.8: in the SL doorway, watching

# The company in the chairs: seated from the top of the number (dance.py sit), turning to whoever has the floor, up at
# 100.5 (FILM 101.5), off with their chairs (FILM 111.6-114.6).
for a, (seat, ent, arr) in CB2.items():
    k = int(a[3:])
    wp(a, T, 16.4 + 0.1 * k, seat[0], seat[1] + 0.001, facing=face(seat, (0.4, 2.3), 1.0))   # Jefferson's verse
    wp(a, T, 70.6 + 0.1 * k, seat[0], seat[1], facing=face(seat, (0.6, 2.4), 1.0))          # Hamilton's
    wp(a, T, 100.6 + 0.1 * k, seat[0], seat[1] + 0.001, facing=face(seat, (0.0, 1.8), 1.0))  # up: Washington rules
    tl = leave(a, T, CB2_OUT[a], (seat[0], seat[1] + 0.001), ent)
    PROPT["cb2-chair-%d" % k] += [CB2_OUT[a], round(tl, 2)]
# the armchair goes off with ens8 from the deck door (FILM 111.6: carried behind Washington)
enter("ens8", T, 109.6, "D-UC", (WSEAT[0], WSEAT[1] - 0.05), 0)
tl = leave("ens8", T, 110.0, (WSEAT[0], WSEAT[1] - 0.05), "D-UC")
PROPT["cb2-armchair"] += [110.0, round(tl, 2)]
# FILM 13.6 / 60: two of the company watch from the upstage gallery through the battle
gal_enter("ens7", T, 1.0, (-1.6, -3.3), 15)
gal_enter("ens9", T, 1.6, (1.5, -3.3), -15, label="Ensemble 9")
wp("ens7", T, 40.0, -1.2, -3.2, facing=30, y="gallery")
wp("ens9", T, 44.0, 1.1, -3.2, facing=-20, y="gallery")
wp("ens7", T, 80.0, -1.4, -3.25, facing=40, y="gallery")
wp("ens9", T, 84.0, 1.3, -3.25, facing=-40, y="gallery")
gal_exit_all(T, 108.0, {"ens7": (-1.4, -3.25), "ens9": (1.3, -3.25)})

# ---------------------------------------------------------------- 2-08 Washington on Your Side
# FILM (2-08 clip, the film is 3.2 s behind the album here and aligned): Burr walks on to Jefferson, who is left
# centre (8.2); Burr SR, Jefferson SL of him (15, 36, 39.8); they talk close (44-61); Burr crosses to SL (79);
# MADISON comes on from SR for his verse, and the row is MADISON SR, JEFFERSON centre, BURR SL (82-123: every wide
# shot); the company forms behind them for the chant and marches them downstage (130-145, eight of them); it scatters
# upstage (155) with Burr and Madison together centre-SR; Washington's desk is upstage SR, Washington comes to it
# (162-166) and Jefferson hands him the resignation; at the button (177) Burr is far SR, Jefferson centre, Madison
# far SL, Washington by the desk with the paper and Hamilton upstage SL of centre reading: One Last Time's first picture.
T = "2-08"
ROW = {"mulligan": (-2.7, 3.0), "lafayette": (0.0, 3.0), "burr": (2.7, 3.0)}   # FILM: Madison SR, Burr SL
wp("lafayette", T, 3.5, 0.4, 2.9, facing=-100)                     # still staring SR after them
wp("lafayette", T, 7.0, 0.41, 2.9, facing=140)                     # turns: Burr behind him
wp("lafayette", T, 10.5, 1.3, 2.6, facing=-60)                     # FILM 15
wp("burr", "2-08", 3.0, 3.0, 0.6, dwell=0)                         # from the SL doorway, round behind Jefferson
wp("burr", T, 5.6, 1.2, 1.4, dwell=0)
wp("burr", T, 8.0, -0.6, 2.4, facing=60)                           # FILM 8.2
wp("burr", T, 15.0, -1.0, 2.8, facing=70)                          # FILM 15
# Jefferson's verse: round centre and SL of it, at Burr (FILM 36-61)
wp("lafayette", T, 22.5, 0.9, 3.3, facing=-10)
wp("lafayette", T, 30.0, 0.2, 3.1, facing=-30)
wp("lafayette", T, 34.0, 1.0, 3.2, facing=-40)
wp("lafayette", T, 41.0, 1.3, 2.6, dwell=0)
wp("lafayette", T, 43.5, 0.4, 2.0, dwell=0)
wp("lafayette", T, 46.0, -0.2, 2.6, dwell=0)
wp("lafayette", T, 48.5, 0.2, 3.3, dwell=0)
wp("lafayette", T, 50.6, 0.6, 3.1, facing=-30)
wp("lafayette", T, 54.0, 0.0, 2.6, facing=-70)                     # FILM 44-61: close, at Burr
wp("lafayette", T, 59.5, 0.3, 3.4, facing=0)
wp("lafayette", T, 64.0, 0.6, 2.9, facing=-40)
wp("lafayette", T, 70.0, -0.2, 2.7, facing=30)
wp("lafayette", T, 79.0, -0.4, 2.7, facing=60)                     # FILM 79: Burr is SL of him now
wp("burr", T, 23.5, -1.3, 2.5, facing=60)
wp("burr", T, 30.0, -0.9, 2.8, facing=70)
wp("burr", T, 38.0, -1.2, 2.6, facing=80)
wp("burr", T, 44.0, -0.8, 2.5, facing=70)
wp("burr", T, 50.0, -1.3, 2.7, facing=60)
wp("burr", T, 56.0, -0.9, 2.4, facing=80)
wp("burr", T, 61.5, -0.95, 2.45, facing=70, dwell=0)
wp("burr", T, 64.0, 0.0, 1.6, dwell=0)                             # crosses upstage of Jefferson
wp("burr", T, 67.0, 2.0, 2.8, facing=-70)
wp("burr", T, 72.0, 1.6, 2.6, facing=-80)
wp("burr", T, 79.0, 2.0, 2.8, facing=-90)                          # FILM 79
enter("mulligan", T, 78.0, "W-MSR", (-2.7, 2.6), 50, label="Madison")   # FILM 82: in from SR for his verse
wp("mulligan", T, 83.0, -2.2, 2.8, facing=30)
for a, p in ROW.items():                                           # hook 3 (FILM 89-123: the row)
    wp(a, T, 88.0, p[0], p[1], facing=0)
# the drive: Jefferson round the SL half of the outer ring (the row is mirrored, so is the ring)
wp("lafayette", T, 97.1, 0.0, 3.01, dwell=0)
wp("lafayette", T, 99.4, 2.26, 3.21, dwell=0)
wp("lafayette", T, 101.7, 3.2, 0.95, dwell=0)
wp("lafayette", T, 104.0, 2.26, -1.31, dwell=0)
wp("lafayette", T, 107.1, -0.15, 3.0, facing=-20)                  # decides to quit
wp("mulligan", T, 97.1, -2.7, 3.01, dwell=0)                       # Madison presses the case from SR
wp("mulligan", T, 102.0, -2.3, 2.2, facing=40)
wp("mulligan", T, 107.0, -2.6, 2.6, facing=50)
wp("mulligan", T, 113.4, -2.6, 2.8, facing=75)
wp("burr", T, 98.5, 3.9, 3.6, facing=-30)
wp("burr", T, 115.0, 2.6, 2.8, facing=-45)
# Washington's desk, set upstage SR by the Bullet (FILM 162-177: the desk upstage SR of centre)
WDESK = (-1.5, -0.6)
t0 = enter("ens1", T, 123.0, "D-UC", (WDESK[0], WDESK[1] - 0.6), 0, label="The Bullet")
PROPT["washington-desk"] = [round(t0, 2), 123.0]
wp("lafayette", T, 123.5, 0.0, 3.0, facing=0)                      # the chant: the three in a row
wp("mulligan", T, 124.0, -2.7, 3.0, facing=0)
wp("burr", T, 124.0, 2.7, 3.0, facing=0)
# REVIEW 3 / FILM 130-145: the army forms behind them (eight now: FILM 141, 143) and marches them down
WOYS_ARMY = {
    "ens2": ((-3.6, 1.7), "W-DSR"), "ens3": ((-2.68, 1.3), "W-MSR"), "ens4": ((-0.87, 1.55), "W-USR"),
    "ens5": ((2.67, 1.3), "W-MSL"), "ens6": ((3.6, 1.7), "W-DSL"), "ens7": ((-1.8, 0.45), "W-USR"),
    "ens8": ((1.8, 0.45), "W-USL"),
}
for a, (sp, ent) in WOYS_ARMY.items():
    enter(a, T, 130.3, ent, sp, 0, label="Ensemble " + a[3:], speed=3.0)
    wp(a, T, 141.0 + 0.1 * int(a[3:]), sp[0], sp[1] + 0.6, facing=0)        # FILM 141-143: marching down with them
    wp(a, T, 148.0 + 0.1 * int(a[3:]), sp[0], sp[1] + 0.2, facing=0)
    leave(a, T, 153.0 + 0.15 * int(a[3:]), (sp[0], sp[1] + 0.2), ent, speed=2.0)   # FILM 155: scatter upstage
wp("ens1", T, 125.5, -0.6, -1.15, dwell=0)                         # behind the desk
wp("ens1", T, 128.0, -0.3, -0.25, dwell=0)                         # round the desk's SL end
wp("ens1", T, 130.3, 0.87, 1.3, facing=0)                          # in the line (ch74)
wp("ens1", T, 141.0, 0.87, 1.9, facing=0)
wp("ens1", T, 145.4, 0.5, 2.3, dwell=0)                            # the Bullet weaves out (974): round Burr, SL now
wp("ens1", T, 146.6, 1.9, 2.3, dwell=0)
wp("ens1", T, 147.9, 4.4, 2.7, dwell=0)
wp("ens1", T, 149.0, 4.1, 4.2, dwell=0)
wp("ens1", T, 150.4, 1.9, 4.0, facing=-60)                         # between Burr and Jefferson
leave("ens1", T, 150.8, (1.9, 4.0), "W-DSL", speed=2.0)
for a, p, f0 in (("lafayette", ROW["lafayette"], 90), ("burr", ROW["burr"], -90), ("mulligan", ROW["mulligan"], 90)):
    wp(a, T, 137.4, p[0] + 0.001, p[1], facing=f0, dwell=1.0 if a == "burr" else 0.4)   # REVIEW 3: Burr faces the wrong way
    wp(a, T, 141.0, p[0] + 0.9, p[1] + 0.4, facing=90)             # REVIEW 3: the walk, in step, to SL (and down)
wp("lafayette", T, 144.0, 0.4, 3.4, facing=10)                     # the money: Jefferson works the line
wp("mulligan", T, 144.0, -1.9, 3.3, facing=20)
wp("burr", T, 144.0, 3.2, 3.3, facing=-20)
wp("lafayette", T, 149.5, 0.0, 2.8, facing=0)                      # the digging
wp("lafayette", T, 151.0, 0.01, 2.8, facing=160, dwell=0)
wp("lafayette", T, 155.0, 1.5, 1.4, facing=150)                    # FILM 155: walks up, away from them
wp("burr", T, 151.5, 3.2, 3.31, facing=-90, dwell=0)
wp("burr", T, 155.0, -0.8, 2.75, facing=60)                        # FILM 155: Burr and Madison together
wp("mulligan", T, 155.0, 0.1, 2.85, facing=-70)
wp("burr", T, 160.0, -1.3, 3.0, facing=40)
wp("mulligan", T, 160.0, 0.6, 3.1, facing=-50)
# Washington to his desk (FILM 162-166); Jefferson writes and hands him the resignation
enter("washington", T, 161.5, "D-UC", (-0.7, -0.45), -70)
wp("lafayette", T, 161.0, 1.2, 0.5, facing=-110)                   # FILM 166: the resignation, the quill
wp("lafayette", T, 166.0, 1.21, 0.5, facing=-100, dwell=0)
wp("lafayette", T, 168.5, 0.05, -0.3, facing=-90)                  # FILM 177: Washington holds it
wp("washington", T, 169.0, -0.7, -0.45, facing=80)
wp("lafayette", T, 170.0, 0.06, -0.3, facing=-90, dwell=0)
TOP = {"burr": (-2.5, 3.65), "mulligan": (2.5, 3.65)}              # the defiant climb
for a, p in TOP.items():
    wp(a, T, 166.5, p[0], p[1], facing=0)
END = {"burr": (-4.0, 3.2), "lafayette": (0.0, 2.8), "mulligan": (4.0, 3.2)}   # FILM 177: the button
for a, p in END.items():
    wp(a, T, 174.0, p[0], p[1], facing=0)
    wp(a, T, 180.0, p[0], p[1] + 0.01, facing=0)
enter("hamilton", T, 174.5, "W-USL", (1.4, -0.8), -20)            # FILM 177: Hamilton upstage SL, reading
wp("washington", T, 177.0, -0.75, -0.4, facing=20)
leave("burr", T, 180.5, (-4.0, 3.21), "W-DSR", speed=2.0)
leave("mulligan", T, 180.5, (4.0, 3.21), "W-DSL", speed=2.0)
leave("lafayette", T, 180.5, (0.0, 2.81), "W-MSL", speed=2.0)

# ---------------------------------------------------------------- 2-09 One Last Time
# FILM (2-09 clip; its time drifts after about 170, so the second half reads by what happens, not by `at`):
#  - Washington at the SR end of the desk, Hamilton SL of it reading the paper (5.8, 6.5);
#  - the scene is played in front of the desk with HAMILTON ON WASHINGTON'S LEFT (SL) throughout: the drinks poured
#    at the desk and the toast (61-66), the teaching close together mid-stage (78-99), Washington in front of the desk
#    and Hamilton a step SL (125), the quill handed over at the desk (168);
#  - the address: Hamilton alone DSC reading (179); then side by side, Hamilton on Washington's left (REVIEW 3; FILM
#    200-217), Hamilton stepping back as the company and the family come (224-240);
#  - the end: the company in a line across upstage, Eliza and Hamilton SR; Washington DSC in a spot, arms open, for
#    the held note (the 2-10 clip's first frames); after the cut-off he walks slowly upstage and off, the King on the
#    deck watching him go (2-10 clip 295.8). NOT the SL stair any more (the cue round's ch20 idea): the film is plain.
T = "2-09"
WBEHIND = (WDESK[0], WDESK[1] - 0.6)
wp("washington", T, 2.5, -1.5, 0.2, dwell=0)
wp("washington", T, 5.0, -2.5, -0.3, facing=150)                   # FILM 6.5: the SR end of the desk
wp("washington", T, 8.0, -2.4, -1.15, dwell=0)
wp("washington", T, 11.0, WBEHIND[0], WBEHIND[1], facing=0)        # behind it, reading the resignation
wp("washington", T, 18.0, WBEHIND[0] + 0.01, WBEHIND[1], facing=40)
wp("washington", T, 21.5, -0.6, -1.1, dwell=0)
wp("washington", T, 25.0, -0.8, 0.2, facing=60)                    # round to Hamilton
wp("washington", T, 35.0, -0.6, 0.4, facing=70)
wp("washington", T, 44.0, -0.4, 0.9, facing=0)                     # the decision
wp("washington", T, 50.0, -0.7, 0.6, facing=60)
wp("washington", T, 56.0, -1.0, 0.0, facing=170)                   # FILM 61: pours at the desk
wp("washington", T, 60.0, -0.7, 0.4, facing=60)
wp("washington", T, 66.0, -0.5, 0.6, facing=70)                    # FILM 66: the toast
wp("washington", T, 70.0, -0.4, 0.8, facing=80)
wp("washington", T, 74.0, -0.6, 1.1, facing=40)
wp("washington", T, 81.8, -0.3, 1.6, facing=30)                    # FILM 78-99: teaching, close
wp("washington", T, 86.0, 0.1, 1.8, facing=60)
wp("washington", T, 92.0, -0.5, 1.5, facing=70)
wp("washington", T, 100.0, -0.8, 1.0, facing=60)
wp("washington", T, 106.0, -0.6, 0.7, facing=80)
wp("washington", T, 113.0, -0.7, 0.8, facing=60)
wp("washington", T, 118.0, -0.4, 1.1, facing=70)
wp("washington", T, 124.0, -0.8, 0.9, facing=20)                   # FILM 125: in front of the desk
wp("washington", T, 129.0, -0.5, 1.0, facing=60)
wp("washington", T, 137.0, -0.6, 1.3, facing=20)
wp("washington", T, 144.0, -0.3, 1.5, facing=50)
wp("washington", T, 150.0, -0.6, 1.2, facing=30)
wp("washington", T, 158.0, -0.4, 1.4, facing=60)
wp("washington", T, 164.0, -0.6, 1.0, facing=40)
wp("washington", T, 168.0, -0.7, 0.3, facing=100)                  # FILM 168: the quill at the desk
wp("washington", T, 170.0, -0.8, 0.1, facing=0, dwell=13.6)        # upstage of Hamilton for the address
wp("washington", T, 184.5, -0.7, 1.2, dwell=0)
wp("washington", T, 186.0, -0.4, 2.5, facing=0)                    # REVIEW 3: side by side, Hamilton on his left
wp("washington", T, 193.0, 0.0, 3.2, facing=0)                     # takes over the reading
wp("washington", T, 200.0, -0.1, 3.3, facing=-10)
wp("washington", T, 213.0, 0.2, 3.4, facing=10)
wp("washington", T, 225.0, -0.3, 3.5, facing=20)
wp("washington", T, 238.0, -0.2, 3.1, facing=-20)
wp("washington", T, 246.0, 0.0, 2.6, facing=0)                     # the company gathers
wp("washington", T, 256.0, 0.3, 2.2, facing=-15)
wp("washington", T, 262.0, -0.3, 2.0, facing=15)
wp("washington", T, 268.0, 0.0, 1.4, facing=0)                     # FILM: arms open, the company behind him
wp("washington", T, 274.0, 0.25, 1.1, facing=-10)
wp("washington", T, 278.0, 0.0, 1.7, facing=0)
wp("washington", T, 282.8, 0.0, 2.8, facing=0)                     # FILM: DSC in his spot for the held note
wp("washington", T, 293.0, 0.01, 2.8, facing=0, dwell=0)
wp("hamilton", T, 2.0, 1.45, -0.3, dwell=0)
wp("hamilton", T, 6.0, 1.8, 0.5, facing=-60)                       # FILM 6.5: SL, the paper
wp("hamilton", T, 15.0, 1.4, 0.5, facing=-80)
wp("hamilton", T, 22.0, 0.6, 0.6, facing=-90)
wp("hamilton", T, 28.0, 0.3, 0.5, facing=-100)
wp("hamilton", T, 35.0, 0.4, 0.7, facing=-80)
wp("hamilton", T, 44.0, 1.2, 0.9, facing=-40)                      # steps off: Washington's decision
wp("hamilton", T, 50.0, 0.5, 0.7, facing=-90)
wp("hamilton", T, 56.0, 0.2, 0.4, facing=-120)
wp("hamilton", T, 60.0, 0.3, 0.5, facing=-100)                     # takes the glass
wp("hamilton", T, 66.0, 0.2, 0.6, facing=-100)                     # FILM 66: the toast
wp("hamilton", T, 69.5, 0.9, 1.0, facing=-60)                      # protests
wp("hamilton", T, 74.0, 0.6, 1.3, facing=-80)
wp("hamilton", T, 81.8, 0.6, 1.5, facing=-100)
wp("hamilton", T, 86.0, 1.0, 1.9, facing=-80)
wp("hamilton", T, 92.0, 0.6, 1.4, facing=-100)
wp("hamilton", T, 100.0, 0.9, 1.2, facing=-80)
wp("hamilton", T, 106.0, 0.4, 0.9, facing=-100)
wp("hamilton", T, 113.5, 0.9, 0.7, facing=-70)                     # his doubt
wp("hamilton", T, 120.0, 1.3, 0.8, facing=-60)
wp("hamilton", T, 125.0, 1.2, 0.6, facing=-80)                     # FILM 125
wp("hamilton", T, 132.0, 0.9, 0.9, facing=-90)
wp("hamilton", T, 140.0, 1.1, 1.0, facing=-70)
wp("hamilton", T, 150.0, 0.8, 0.8, facing=-90)
wp("hamilton", T, 158.0, 1.0, 1.1, facing=-80)
wp("hamilton", T, 164.0, 0.6, 0.6, facing=-110)
wp("hamilton", T, 168.0, 0.0, 0.25, facing=-120)                   # FILM 168: takes the quill
wp("hamilton", T, 171.5, 0.0, 3.35, facing=0)                      # FILM 179: alone DSC, reading
wp("hamilton", T, 184.0, 0.001, 3.35, dwell=0)
wp("hamilton", T, 186.0, 0.6, 2.5, facing=0, dwell=4.4)            # REVIEW 3: beside him, SL of him
wp("hamilton", T, 193.2, 0.9, 2.9, facing=-10)                     # FILM 200-217: still beside him, a step back
wp("hamilton", T, 200.0, 1.0, 3.0, facing=-20)
wp("hamilton", T, 210.0, 0.9, 2.8, facing=-10)
wp("hamilton", T, 218.0, 1.0, 2.9, facing=-20)
wp("hamilton", T, 222.0, 1.5, 1.6, dwell=0)                        # steps back
wp("hamilton", T, 230.0, 1.2, 1.2, facing=-30)
wp("hamilton", T, 236.0, 1.21, 1.2, facing=-60, dwell=0)
wp("hamilton", T, 241.5, -2.4, 2.9, facing=45)                     # to the family SR
wp("hamilton", T, 249.5, -2.4, 3.0, facing=45)
wp("hamilton", T, 256.0, -2.4, 3.05, facing=20)
enter("eliza", T, 247.0, "W-DSR", (-3.15, 3.45), 30)
enter("laurens", T, 248.5, "W-DSR", (-2.85, 2.25), 30)
wp("hamilton", T, 270.0, -2.2, 2.8, facing=60)                     # the family watches him
wp("eliza", T, 270.4, -3.15, 3.45, facing=60)
wp("laurens", T, 270.8, -2.85, 2.25, facing=70)
leave("eliza", T, 293.0, (-3.15, 3.45), "W-DSR")
leave("hamilton", T, 293.6, (-2.2, 2.8), "W-DSR")
leave("laurens", T, 294.8, (-2.85, 2.25), "W-DSR")
# The company: a line across upstage of him (FILM), out to watch and salute; off after the cut-off by the side wings.
CO9 = {
    "ens1": ((-2.6, -0.3), "W-MSR", 245.0), "ens2": ((-0.9, 0.35), "W-USR", 246.2), "ens3": ((-0.2, -0.8), "W-USR", 247.6),
    "ens4": ((0.9, -0.6), "W-USL", 249.0), "ens5": ((3.4, 0.3), "W-MSL", 245.4), "ens6": ((3.7, -0.9), "W-USL", 246.0),
    "ens7": ((-3.6, 0.5), "W-MSR", 246.6), "ens8": ((-1.9, 0.1), "W-USR", 249.6), "ens9": ((1.9, 0.0), "W-USL", 245.3),
    "ens10": ((2.6, -0.4), "W-USL", 245.8),
}
for i, (a, (sp, ent, arr)) in enumerate(CO9.items()):
    enter(a, T, arr, ent, sp, face(sp, (0.0, 3.0), 0.8), label=("Ensemble " + a[3:]) if a == "ens10" else None)
    wp(a, T, 258.0 + 0.2 * i, sp[0] + 0.2, sp[1] + 0.3, facing=face(sp, (0.0, 2.2), 0.9))   # in a step as it builds
    wp(a, T, 283.0 + 0.2 * i, sp[0] + 0.2, sp[1] + 0.31, facing=face(sp, (0.0, 2.8), 0.9))
    leave(a, T, 293.0 + 0.2 * i, (sp[0] + 0.2, sp[1] + 0.31), ent, speed=2.2)

# ---------------------------------------------------------------- 2-10 I Know Him
# FILM (2-10 clip): the King strolls on from SL as the company leaves (2-09 ~294) and stands watching Washington walk
# slowly upstage and off (295.8, 1.6); he is UC for the first verse (5.2), down to DC; the Bullet (a redcoat) is beside
# him from the start of the silence verse and stays at his SR shoulder through it (33.1-47.1), giggles, and goes.
T = "2-10"
wp("washington", T, 0.8, -0.2, 1.2, dwell=0)                       # FILM 295.8 / 1.6: slowly upstage
wp("washington", T, 3.0, -0.6, -1.2, facing=170)
leave("washington", T, 3.6, (-0.6, -1.2), "D-UC", speed=1.0)
enter("king", "2-09", 295.5, "W-DSL", (1.5, 0.9), -150, label="King George")   # FILM: in from SL, watches him go
wp("king", T, 3.8, 1.51, 0.9, facing=-160, dwell=0)
wp("king", T, 6.0, 0.0, -0.65, facing=0)                           # UC for the verse (FILM 5.2)
wp("king", T, 12.0, 0.2, -0.6, facing=-15)
wp("king", T, 24.0, 0.0, 3.45, facing=0)                           # comes down to his spot DC
wp("king", T, 33.5, 0.2, 3.4, facing=-60)                          # FILM 33.1: the messenger at his shoulder
wp("king", T, 40.6, 0.15, 3.4, facing=-40)
wp("king", T, 43.0, 0.1, 3.45, facing=-20)                         # shoos her
wp("king", T, 45.1, 0.0, 3.45, facing=0)                           # the name
enter("ens1", T, 33.0, "W-DSR", (-0.7, 3.6), 70, label="The Bullet", speed=3.2)
wp("ens1", T, 37.0, -0.68, 3.62, facing=50)
wp("ens1", T, 42.3, -0.65, 3.66, facing=40)                        # giggles
leave("ens1", T, 47.2, (-0.65, 3.66), "W-DSR", speed=3.2)          # FILM 47.1: still there
wp("king", T, 58.0, -1.0, 3.35, facing=20)                         # the band: he struts
wp("king", T, 64.0, 1.0, 3.35, facing=-20)
wp("king", T, 70.3, 0.0, 3.6, facing=0)
wp("king", T, 80.0, -0.9, 3.75, facing=15)                         # the scat chorus
wp("king", T, 84.0, 0.9, 3.75, facing=-15)
wp("king", T, 89.0, 0.0, 3.45, facing=0)                           # the announcement
wp("king", T, 92.0, -1.0, 3.7, facing=15)                          # the laugh
# SPOT (coordinator, boundary relaxed for 2-10 -> 2-11): he ENDS the segment ON STAGE at (0, 3.41), facing the house,
# at the blackout; seg 7 picks him up there at 2-11 0.0.
wp("king", T, 94.4, 0.0, 3.41, facing=0)
wp("king", T, 95.6, 0.0, 3.41, facing=0)

# ---------------------------------------------------------------- write
for a, path in W.items():   # time must increase as written: no silent sorting
    key = [(ORDER.index(p["track"]), p["at"]) for p in path]
    for k in range(1, len(key)):
        if key[k] <= key[k - 1]:
            raise SystemExit("time does not increase: %s #%d %s" % (a, k, path[k]))
seg = {"segment": 6, "tracks": ORDER, "waypoints": W,
       "notes": open(NOTES, encoding="utf-8").read().strip() if os.path.exists(NOTES) else ""}
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(seg, f, indent=1)
print("wrote", OUT, sum(len(v) for v in W.values()), "waypoints")
print("PROPT", json.dumps(PROPT))
