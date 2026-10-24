"""Generate segments/seg3.json: 1-12 .. 1-17 blocking (Story of Tonight reprise .. That Would Be Enough)."""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TRACKS = ["1-12", "1-13", "1-14", "1-15", "1-16", "1-17"]
LEN = {"1-12": 115.0, "1-13": 193.0, "1-14": 159.0, "1-15": 106.0, "1-16": 83.0, "1-17": 178.0}
START = {}
s = 0.0
for t in TRACKS:
    START[t] = s; s += LEN[t]

ENT = {"W-DSR": (-7.3, 4.6), "W-DSL": (7.3, 4.6), "W-MSR": (-8.5, 0.0), "W-MSL": (8.0, -0.5),
       "W-USR": (-8.5, -3.0), "W-USL": (8.5, -3.0), "D-UC": (1.25, -4.9)}
WALK = 1.3

P = {}  # actor -> list of waypoint dicts


def r3(v):
    return round(v, 3)


def add(actor, track, at, x, z, facing=None, dwell=None, off=False, label=None, y=None):
    w = {"track": track, "at": round(at, 2), "x": r3(x), "z": r3(z)}
    if y is not None: w["y"] = y
    if dwell is not None: w["dwell"] = dwell
    if facing is not None: w["facing"] = round(((facing + 180) % 360) - 180, 1)
    if off: w["off"] = True
    if label: w["label"] = label
    P.setdefault(actor, []).append(w)
    return w


def clock(track, at):
    return START[track] + at


def ring(r, th):
    a = math.radians(th)
    return (r * math.sin(a), 0.95 - r * math.cos(a))


def face(frm, to, cheat=0.0):
    """facing from point frm towards point to; cheat blends toward the house (0..1)."""
    dx, dz = to[0] - frm[0], to[1] - frm[1]
    f = math.degrees(math.atan2(dx, dz))
    return f * (1 - cheat)


def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def last(actor):
    w = P[actor][-1]
    return (w["x"], w["z"])


def exit_to(actor, track, t_leave, gate, label=None, extra=0.3):
    """Walk off from the actor's last point, leaving at t_leave at 1.3 m/s, to an entrance."""
    g = ENT[gate]
    d = dist(last(actor), g)
    t = t_leave + d / WALK + extra
    add(actor, track, t, g[0], g[1], off=True, label=label)
    return t


def enter_from(actor, track, t_arrive, gate, x, z, facing, label=None, t_off=None):
    g = ENT[gate]
    d = dist(g, (x, z))
    if t_off is None:
        t_off = max(0.0, t_arrive - d / WALK - 1.0)
    add(actor, track, t_off, g[0], g[1], off=True, label=label)
    add(actor, track, t_arrive, x, z, facing=facing)


def assign(ms, slots, cur):
    """Map members to slots minimising the summed squared walk (2-opt swaps), so paths do not cross."""
    a = {m: slots[i] for i, m in enumerate(ms)}
    better = True
    while better:
        better = False
        for i, m in enumerate(ms):
            for n in ms[i + 1:]:
                d0 = dist(cur[m], a[m]) + dist(cur[n], a[n])
                d1 = dist(cur[m], a[n]) + dist(cur[n], a[m])
                if d1 < d0 - 1e-9:
                    a[m], a[n] = a[n], a[m]; better = True
    return a


def here(m, track, at):
    """The member's position at its latest waypoint at or before (track, at)."""
    best = None
    for w in P[m]:
        if clock(w["track"], w["at"]) <= clock(track, at) + 1e-9:
            if best is None or clock(w["track"], w["at"]) >= clock(best["track"], best["at"]):
                best = w
    return (best["x"], best["z"])


C = (0.0, 0.95)
ENS = ["ens%d" % i for i in range(1, 11)]

# FILM ROUND (2026-10-24): STILL ON PURPOSE (what tools/blocking/still.py still lists in this segment, kept because the
# film or a source has it so): 1-12 Burr through the scene with Hamilton (reserved; the secret told out front) and
# Hamilton listening to it; 1-13 Burr in his pool for verse 1 (the soliloquy; film 10.6, a lone figure); 1-14 Eliza on
# the gallery reading and writing her letters (film 7-58: she moves along it between long holds), Angelica with her,
# the camp listening to Lee's slander (119-137); 1-15 the three pools at the top and the four in their pictures
# (the renders), the Doctor with his back turned, the company at the edges in the dark through the seconds' scene;
# 1-16 Hamilton, hands behind his back (hamiltonsideblog; film 36), and the group round the fallen Lee.

# =====================================================================================
# 1-12  The Story of Tonight (Reprise) - the four friends DS centre-SL, Burr comes on SR (FILM ROUND)
# =====================================================================================
T = "1-12"
# FILM ROUND (2026-10-24; the Disney+ clip, research/seg3.md "Film round"). The four are in two pairs across the front,
# centre to SL, from the top (0.8 wide: Lafayette and Mulligan shaking hands at centre, Laurens and Hamilton to SL), and
# never still: drinking, leaning on each other, the crouching drunk dance at ~40. Burr comes on from SR and STAYS SR;
# Hamilton crosses the whole stage to him (47-50) while the three toast far SL (52: x 3-5); the two trade sides (60:
# Hamilton SR of Burr); Laurens comes over and drapes on Burr (70); all five in a line at centre (79); the friends are
# shooed off to SL (82: going out by the SL stair); Hamilton SR of centre, Burr turned upstage SL of him (104); Hamilton
# off DR. Hamilton still brings the tavern table on (segment 2's carry, at (-0.05, 2.1) by 5.0) and Lafayette strikes it.
enter_from("hamilton", T, 5.0, "W-DSL", 0.0, 2.5, 0, label="Hamilton", t_off=0.0)    # with the table (props, segment 2)
enter_from("lafayette", T, 5.5, "W-DSL", -0.7, 3.2, 60, label="Lafayette", t_off=0.2)
enter_from("laurens", T, 6.0, "W-DSL", 1.6, 3.1, -60, label="Laurens", t_off=0.0)
enter_from("mulligan", T, 6.5, "W-DSR", 0.6, 3.3, -60, label="Mulligan", t_off=0.2)
# the verse: they mill and lean on each other round the table (film 9-20: the close group, arms round shoulders)
add("lafayette", T, 10.5, -0.3, 2.95, 40)
add("hamilton", T, 11.5, 0.9, 2.85, -60)
add("mulligan", T, 12.0, 0.25, 3.0, -20)
add("laurens", T, 13.0, 1.9, 2.75, -90)
# the toast (20.3): the line across the front, Mulligan at the SR end, Hamilton at the SL end (film 30)
add("mulligan", T, 20.6, -1.0, 3.0, 20)
add("laurens", T, 20.6, 1.6, 3.05, -10)
add("lafayette", T, 21.0, 0.6, 2.95, -15)
add("hamilton", T, 20.25, 2.5, 3.1, -40)
add("lafayette", T, 29.0, 0.5, 2.65, -30)
add("laurens", T, 29.5, 1.3, 2.75, 10)
add("mulligan", T, 30.0, -0.6, 2.8, 30)
# the drunk dance (film 40: three crouched, lunging toward SR, Hamilton standing at the SL end watching)
add("mulligan", T, 36.5, -0.4, 2.6, -90)
add("laurens", T, 36.5, 1.0, 2.6, -90)
add("lafayette", T, 36.8, 0.2, 2.65, -90)
add("hamilton", T, 37.0, 2.3, 2.6, -90)
# Burr in from SR, and he stays SR (film 47 / 52: x about -3.9)
add("burr", T, 0.0, ENT["W-MSR"][0], ENT["W-MSR"][1], off=True, label="Burr")
add("burr", T, 45.75, -3.8, 1.9, 70)
add("burr", T, 50.0, -3.6, 1.9, 90)
add("hamilton", T, 50.0, -2.7, 2.1, -100)      # he crosses the stage to Burr (film 47: walking)
# the three go off to SL and toast there (film 47-52)
add("mulligan", T, 48.5, 3.2, 1.9, -30)
add("lafayette", T, 48.0, 4.2, 1.7, -60)
add("laurens", T, 49.5, 4.6, 2.2, -80)
add("lafayette", T, 56.0, 4.0, 1.4, -80)
add("laurens", T, 57.0, 4.6, 2.3, -100)
add("mulligan", T, 58.0, 3.0, 1.6, -60)
# the two trade sides (film 60: Hamilton SR of Burr)
add("burr", T, 54.85, -3.0, 2.3, -80)
add("hamilton", T, 56.5, -4.0, 2.4, 80)
add("hamilton", T, 63.0, -3.8, 2.5, 70)
add("burr", T, 66.0, -2.75, 2.4, -60)
# Laurens comes over and drapes on Burr (film 70), the other two follow
add("laurens", T, 69.5, -2.2, 2.5, -100)
add("lafayette", T, 72.0, -1.3, 2.3, -90)
add("mulligan", T, 73.0, -1.6, 3.0, -100)
# all five in a line at centre (film 79), then Hamilton shoos the three off (film 82: off by the SL stair)
add("burr", T, 78.0, -2.8, 2.4, 60)
add("hamilton", T, 78.5, -3.7, 2.5, 90)
add("laurens", T, 77.0, -2.0, 2.75, -90)
add("mulligan", T, 78.0, -1.2, 3.05, -90)
add("lafayette", T, 78.5, -0.5, 2.4, -90)
add("hamilton", T, 80.0, -3.4, 2.5, 90)
exit_to("lafayette", T, 80.6, "W-MSL")       # with the table (props: struck 80.5)
exit_to("laurens", T, 80.8, "W-USL")
exit_to("mulligan", T, 81.3, "W-DSL")
# the two alone: Burr's secret turned out to the house, then Burr goes SL of him and turns upstage (film 104)
add("hamilton", T, 84.0, -3.0, 2.8, 90)
add("burr", T, 84.5, -2.0, 2.5, -90)
add("burr", T, 90.7, -2.0, 2.7, 10)
add("hamilton", T, 91.5, -2.9, 2.9, 70)
add("burr", T, 100.0, 1.6, 2.2, 170)
add("hamilton", T, 100.5, -1.4, 2.7, 60)
add("hamilton", T, 108.25, -1.4, 2.7, -40)
exit_to("hamilton", T, 108.4, "W-DSR")
# Burr walks to his spot on the turntable for Wait for It
add("burr", T, 112.5, 0.63, 2.2, 0)
# REVIEW 3 (Disney+ clip e4NAz2TWA4I, its comments): two of the wedding guests are still there, passed out - one on the
# stairs ("Oak waking up the ensemble member on the stairs"), and at the end "Thayne helping Ephraim get up". Thayne
# Jasperson is the OBC's Seabury, so ens2; Ephraim Sykes is ens9. They come in through the deck door in the opening dark
# and slump (dance.py: kneel); at the end ens2 helps ens9 up off the SL stair and they go out the way they came.
add("ens9", T, 0.0, ENT["D-UC"][0], ENT["D-UC"][1], off=True, label="Ensemble 9")
add("ens9", T, 2.6, 2.1, -2.45, dwell=0)
add("ens9", T, 3.6, 2.55, -2.45, 0, y=0.63)  # two steps up the SL stair (0.63 m), slumped
add("ens2", T, 0.5, ENT["D-UC"][0], ENT["D-UC"][1], off=True, label="Ensemble 2")
add("ens2", T, 4.2, 1.3, -1.7, -30)          # slumped on the deck below the stair
add("ens2", T, 104.5, 1.3, -1.7, 120)
add("ens2", T, 106.3, 1.6, -2.0, 120)        # to his friend on the stair
add("ens9", T, 107.9, 2.55, -2.45, -90, dwell=0.9, y=0.63)
add("ens9", T, 109.2, 2.1, -2.45, 170, dwell=1.2)
add("ens2", T, 109.0, 1.6, -2.0, 170, dwell=0.2)
exit_to("ens2", T, 109.2, "D-UC", extra=0.0)
exit_to("ens9", T, 110.4, "D-UC", extra=0.0)

# =====================================================================================
# 1-13  Wait for It - Burr in the centre; the company on chairs at the sides and on the gallery (FILM ROUND)
# =====================================================================================
T = "1-13"
B = "burr"
# FILM ROUND (2026-10-24; research/seg3.md "Film round"): Burr is in the centre and WALKS - verse 2 takes him off toward
# SR (film 60), verse 3 has him at SR of centre (121), he works the centre on the final chorus. Kept: his pool at
# (0.63, 2.2), the step down on the boast (99.5) and at the peak (152), the turn upstage in verse 3.
for at, x, z, f in [(0.6, 0.63, 2.2, 0), (10.0, 0.85, 2.4, 25), (19.0, 1.5, 2.65, -20), (26.0, 0.9, 2.5, 0),
                    (31.15, 0.63, 2.2, 0), (44.8, 0.63, 2.4, 0), (51.1, 0.35, 2.3, -15), (57.0, -0.9, 2.1, -60),
                    (62.0, -1.8, 2.3, -30), (66.4, -0.6, 2.5, 20), (72.0, 0.63, 2.0, 0), (85.9, 0.63, 2.4, 0),
                    (92.55, 0.63, 2.2, 0), (99.5, 0.65, 2.95, 0), (106.0, 0.95, 2.5, -20), (110.5, 1.6, 2.3, 40),
                    (114.9, 0.8, 2.2, -170), (119.0, -0.4, 1.9, -160), (124.0, -0.6, 2.1, 175), (131.8, 0.0, 2.4, 0),
                    (138.0, 0.9, 2.6, 20), (146.2, 0.63, 2.6, 0), (152.0, 0.7, 3.1, 0), (159.45, 0.63, 2.3, 0),
                    (165.0, -0.6, 2.4, -30), (170.0, 0.4, 2.7, 10), (175.2, 0.63, 2.2, 0), (189.6, 0.63, 2.3, 0)]:
    add(B, T, at, x, z, f)

# FILM ROUND: the company is on CHAIRS ON THE DECK at the two sides, two each side (film 88.9, 121, 133.8): seated and
# watching him through the first two choruses, the chair dance in verse 3 (118-131: legs thrown out, lunging off the
# chairs), standing by the chairs on "what is it like in his shoes" (133.8), dancing out from them on the final chorus
# (159: the lunges) and back on them for the end. The woman far SL (ens8, cue 410) is one of the four, so she no longer
# goes at 51: she keeps her chair to the outro. Three more stand on the upstage gallery (film 88.9 / 133.8: figures up
# there; ironinkpen's "on the second floor"), and Burr's verse-3 turn upstage is to them. Each brings her own chair on
# in chorus 1 (props.py SEGMENT 3) and takes it off in the outro fade.
CH13 = {"ens8": ((4.0, 2.6), -60, "W-MSL"), "ens7": ((-4.6, 2.7), 60, "W-DSR"), "ens1": ((-3.0, 0.6), 75, "W-MSR"),
        "ens5": ((3.0, 0.6), -75, "W-MSL")}
enter_from("ens8", T, 9.5, "W-MSL", 4.0, 2.6, -60, label="Ensemble 8", t_off=0.0)   # SPOT: her chair pool ch10 (4.04, 2.64)
for k, m in enumerate(["ens7", "ens1", "ens5"]):
    p, f, g = CH13[m]
    enter_from(m, T, 30.0 + 0.6 * k, g, p[0], p[1], f, label="Ensemble %s" % m[3:])
for m, (p, f, g) in CH13.items():
    stand = (p[0] - 0.35 * math.copysign(1, p[0]), p[1] + 0.15)    # beside the chair, a step in toward him
    add(m, T, 132.6, stand[0], stand[1], face(stand, (0.63, 2.3)))
    add(m, T, 147.0, stand[0], stand[1], face(stand, (0.63, 2.3)))
    add(m, T, 174.6, p[0], p[1], f)                                   # back onto the chair for the end
    exit_to(m, T, 179.6 + (0.4 if m in ("ens1", "ens5") else 0.0), g)

GAL13 = [("ens6", 3.2), ("ens2", -1.8), ("ens9", 1.3)]   # entry order
GZ = -3.35
for k, (m, x) in enumerate(GAL13):
    tm = 24.0 + 1.1 * k                       # at the passage mouth, 1.1 s apart
    add(m, T, tm - 1.3, 0.6, -4.8, y="gallery", off=True, label="Ensemble %s" % m[3:])
    add(m, T, tm, 0.6, GZ, y="gallery", dwell=0)
    add(m, T, tm + abs(x - 0.6) / 1.2, x, GZ, y="gallery", facing=0)
    add(m, T, 31.15, x, GZ, y="gallery", facing=0)
    add(m, T, 115.4, x, GZ, y="gallery", facing=face((x, GZ), (0.63, 2.2)))    # Burr turns up to them: they look down at him
    add(m, T, 132.3, x, GZ, y="gallery", facing=0)
for k, (m, x) in enumerate(reversed(GAL13)):  # off the way they came, nearest the passage first, in the outro fade
    t0 = 179.0 + 1.1 * k
    add(m, T, t0, x, GZ, y="gallery", facing=0, dwell=0)
    add(m, T, t0 + abs(x - 0.6) / 1.2, 0.6, GZ, y="gallery", dwell=0)
    add(m, T, t0 + abs(x - 0.6) / 1.2 + 1.3, 0.6, -4.8, y="gallery", off=True)
for m in list(CH13) + [m for m, _ in GAL13]:
    P[m].sort(key=lambda w: clock(w["track"], w["at"]))
# Burr walks off in the dark into Stay Alive
# REVIEW: he holds his pool to its last cue (189.6), then goes in the navy hold, off before Eliza's opening is lit
_bw = [w for w in P["burr"] if w["track"] == "1-13" and w["at"] == 189.6][0]
_bw["dwell"] = 0.05
add("burr", "1-14", 1.0, ENT["W-MSR"][0], ENT["W-MSR"][1], off=True)

# =====================================================================================
# 1-14  Stay Alive - Eliza writing on the gallery; Washington's tent; Monmouth; Lee
# =====================================================================================
T = "1-14"
# FILM ROUND (2026-10-24; research/seg3.md "Film round"), over REVIEW 3:
#  - Hamilton is SEATED on a chair SL of centre from the top, writing (film 7, 18, 35), and gets up when Washington
#    calls him (46.7); a chair, not the desk (props.py SEGMENT 3: ham-chair-14, set in the dark, struck at 85.5);
#  - the redcoats are on from the top at the edges of the deck, muskets levelled at him, kneeling in the verse (film 7, 25,
#    35, 46, 58): ens7 SR, ens9 and ens10 SL; the war reports bring the four more (65.5);
#  - Eliza's gallery place is SL of centre on the upstage gallery, and she moves along it (film 7: x ~2.2; 25: ~3.6;
#    58: at its SL end); Angelica joins her there (84; she is to Eliza's SL now);
#  - Washington comes on late (film 44: he is beside the seated Hamilton; nobody at the desk in the 35 wide), so he
#    brings the desk at 40, not 17; NOTES3 (Jack) still holds: it goes off at 50 (ens2);
#  - the three friends are NOT in the camp from 29.65 (no one but Hamilton, the Bullet and the redcoats in the wides
#    at 15-58): they come on for the war reports (65.5); Laurens' cut-in on the Bullet at the top is cut (film 15/18:
#    she dances in alone toward Hamilton in his chair);
#  - Monmouth (film 99-116): the redcoats (the British, six) fight in the centre / SL, the Americans (Hamilton,
#    Laurens, Lafayette, Mulligan, Burr) hold SR, Lee runs between; Washington on the gallery at its SR end (106: at
#    the top of the SR stair), not by Eliza.
# Kept from REVIEW 3: the Bullet's slow crossing, Angelica's hug and Eliza's letter into Washington's hand up there,
# Lafayette going for Lee, Lee's slander from the SL gallery with Burr below, Hamilton's charge stopped by Washington,
# Hamilton and Laurens forehead to forehead.
GALY = "gallery"
add("eliza", T, 0.0, 0.6, -4.8, y=GALY, off=True, label="Eliza")
add("eliza", T, 2.0, 0.6, -3.35, y=GALY, dwell=0)
for at, x, z, f in [(4.5, 2.2, -3.35, 0), (14.0, 2.8, -3.3, 10), (24.0, 3.6, -3.35, -10), (34.0, 1.8, -3.35, 0),
                    (46.0, 1.5, -3.3, 10), (56.0, 4.2, -3.35, -20), (66.0, 3.0, -3.35, 0), (81.0, 2.2, -3.05, 0),
                    (84.6, 2.2, -3.05, 90), (92.0, 2.2, -3.05, 0), (97.2, 1.8, -3.2, -90), (100.0, 2.2, -3.15, 0)]:
    add("eliza", T, at, x, z, y=GALY, facing=f)               # SPOT: followspot 1 (follow.py SEGMENT 3)
add("eliza", T, 104.4, 2.2, -3.15, y=GALY, facing=0, dwell=0)
add("eliza", T, 105.8, 0.6, -3.35, y=GALY, dwell=0)
add("eliza", T, 107.1, 0.6, -4.8, y=GALY, off=True)
add("angelica", T, 81.5, 0.6, -4.8, y=GALY, off=True, label="Angelica")
add("angelica", T, 82.8, 0.6, -3.35, y=GALY, dwell=0)
add("angelica", T, 83.8, 1.6, -3.72, y=GALY, dwell=0)
add("angelica", T, 84.4, 2.9, -3.45, y=GALY, facing=-90)
add("angelica", T, 92.0, 2.9, -3.45, y=GALY, facing=-20)
add("angelica", T, 105.4, 2.9, -3.45, y=GALY, facing=-20, dwell=0)
add("angelica", T, 106.6, 1.6, -3.72, y=GALY, dwell=0)
add("angelica", T, 107.6, 0.6, -3.35, y=GALY, dwell=0)
add("angelica", T, 108.9, 0.6, -4.8, y=GALY, off=True)

W = "washington"
enter_from(W, T, 40.0, "D-UC", 0.0, 1.4, 60, label="Washington", t_off=33.0)   # with the desk (props)
for at, x, z, f in [(44.95, 0.3, 1.6, 70), (52.0, -1.4, 2.2, 40), (58.0, -3.3, 2.6, 60), (65.5, -0.3, 1.6, 0),
                    (71.0, 0.5, 1.2, -40), (77.5, -0.2, 1.4, 10), (87.1, 0.4, 1.45, -60), (90.1, 0.0, 1.4, 30)]:
    add(W, T, at, x, z, f)
# up to the gallery (out the deck door, up the back): Eliza's letter into his hand, then along to its SR end for Monmouth
add(W, T, 91.6, 0.95, 1.1, dwell=0)
add(W, T, 94.8, ENT["D-UC"][0], ENT["D-UC"][1], off=True)
add(W, T, 95.0, 0.6, -4.8, y=GALY, off=True)
add(W, T, 96.2, 0.6, -3.35, y=GALY, dwell=0)
add(W, T, 97.0, 1.1, -3.3, y=GALY, facing=90)
add(W, T, 98.6, 1.1, -3.3, y=GALY, facing=90, dwell=0)
WG = (-3.0, -3.35)
add(W, T, 100.6, WG[0], WG[1], y=GALY, facing=20)               # the orders: Lee yelling up at him from the deck
add(W, T, 108.4, WG[0], WG[1], y=GALY, facing=20, dwell=0)
add(W, T, 111.4, 0.6, -3.35, y=GALY, dwell=0)
add(W, T, 112.7, 0.6, -4.8, y=GALY, off=True)
add(W, T, 113.5, ENT["D-UC"][0], ENT["D-UC"][1], off=True)
for at, x, z, f in [(119.5, -0.3, 1.45, 40), (128.3, 1.25, 1.9, -120),   # he steps into Hamilton's charge at Lee
                    (137.3, 0.0, 1.4, 0), (140.0, 0.2, 1.35, -45)]:
    add(W, T, at, x, z, f)
exit_to(W, T, 144.5, "D-UC")

H = "hamilton"
H_SEAT = (2.4, 2.55)        # in his chair, writing (film 7-46); the chair 0.55 m behind him (props ham-chair-14)
add(H, T, 0.0, ENT["W-MSL"][0], ENT["W-MSL"][1], off=True)
for at, x, z, f in [(5.0, H_SEAT[0], H_SEAT[1], -30), (46.5, H_SEAT[0], H_SEAT[1], -60), (52.0, 2.2, 2.3, -90),
                    (58.0, 1.9, 2.5, -80), (65.5, -1.3, 1.4, 45), (71.5, -0.9, 2.3, 20),
                    (77.5, -1.1, 1.6, 40), (87.1, -0.6, 1.85, 70), (90.1, -0.4, 2.4, 60), (96.0, -3.8, 2.6, 90), (99.5, -3.8, 2.6, 90),
                    (105.0, -3.0, 3.4, 60), (114.1, -3.4, 3.0, 40), (122.5, -1.25, 1.0, 60),
                    (125.6, -0.6, 2.4, 60),         # he charges at Lee up on the SL gallery (round Washington) ...
                    (127.6, 0.75, 2.4, 55),
                    (137.3, -0.9, 1.6, 45),          # ... and Washington sends him back
                    (144.3, -0.9, 1.6, 90), (147.5, 1.7, 3.3, 60), (151.0, 1.8, 3.3, 90)]:
    add(H, T, at, x, z, f)
add(H, T, 158.1, 1.8, 3.3, 90, dwell=0.05)    # forehead to forehead with Laurens (ironinkpen), in his key ch2
add(H, T, 120.3, -3.4, 3.0, 20, dwell=0.05)   # he holds his flank through the heat until the ranks have opened out

L = "laurens"
enter_from(L, T, 65.5, "W-MSL", 2.0, 2.4, -20, t_off=58.0)
for at, x, z, f in [(71.5, 2.4, 1.6, -30), (77.5, 1.7, 2.0, -20), (87.1, 2.2, 0.9, -20),
                    (94.0, -2.9, 3.0, 90), (98.6, -2.9, 3.0, 90), (105.0, -2.0, 3.1, 60), (119.5, 2.0, 2.6, 60), (137.3, 1.0, 1.9, 30),
                    (144.3, 1.0, 1.9, 60), (147.5, 2.6, 3.3, -70), (151.0, 2.45, 3.3, -90)]:
    add(L, T, at, x, z, f)
add(L, T, 158.1, 2.45, 3.3, -90, dwell=0.05)
LF = "lafayette"
enter_from(LF, T, 65.5, "W-MSR", -1.8, 2.6, 20, t_off=58.0)
for at, x, z, f in [(71.5, -2.3, 1.6, 30), (77.5, -1.9, 2.1, 30), (87.1, -2.0, -0.3, 20), (93.0, -3.6, -0.5, 60), (98.6, -3.6, -0.5, 80),
                    (107.5, -1.9, 3.6, -10),          # at Lee as Washington takes over ("ready to backhand Lee")
                    (114.1, -3.8, 0.9, 40), (119.5, -0.6, -0.6, 60), (137.3, -0.9, -0.4, 30)]:
    add(LF, T, at, x, z, f)
exit_to(LF, T, 144.5, "W-MSR")
MU = "mulligan"
enter_from(MU, T, 65.5, "W-USL", 0.3, 2.9, 0, t_off=56.5)
for at, x, z, f in [(71.5, 0.6, 2.2, 0), (77.5, 0.0, 2.6, 0), (87.1, 1.6, -0.9, -40), (93.0, -3.0, 0.6, 80), (98.6, -3.0, 0.6, 90),
                    (114.1, -2.6, 0.3, 60), (119.5, 1.1, -0.4, 30), (137.3, 0.9, -0.3, 10)]:
    add(MU, T, at, x, z, f)
exit_to(MU, T, 144.5, "W-USL")

# The Bullet (ens1): in from upstage left at the top, slow (dance.py: bullet) toward Hamilton in his chair and past him,
# away SR (film 15: she dances in alone)
add("ens1", T, 5.0, ENT["W-USL"][0], ENT["W-USL"][1], off=True, label="The Bullet")
add("ens1", T, 9.0, 4.0, 0.0, dwell=0)
add("ens1", T, 14.0, 2.0, 1.4, dwell=0)
add("ens1", T, 18.0, -0.5, 1.0, dwell=0)
add("ens1", T, 19.5, -1.7, 0.4, -120)
exit_to("ens1", T, 19.5, "W-USR", label="Ensemble 1")

# FILM ROUND: the redcoats of the verse, at the edges with muskets on him (dance.py: aim, kneel, musket)
add("ens7", T, 0.5, ENT["W-DSR"][0], ENT["W-DSR"][1], off=True, label="Ensemble 7")
for at, x, z in [(3.0, -4.6, 2.8), (22.0, -4.6, 2.8), (25.0, -2.4, 1.5), (40.0, -2.4, 1.5), (44.0, -4.8, 1.0),
                 (56.0, -4.5, 0.4)]:
    add("ens7", T, at, x, z, face((x, z), H_SEAT))
add("ens9", T, 16.0, ENT["W-MSL"][0], ENT["W-MSL"][1], off=True, label="Ensemble 9")
for at, x, z in [(21.0, 4.4, 0.4), (35.0, 4.4, 0.4), (44.0, 4.9, 1.4)]:
    add("ens9", T, at, x, z, face((x, z), (0.0, 1.4)))
add("ens10", T, 16.5, ENT["W-USL"][0], ENT["W-USL"][1], off=True, label="Ensemble 10")
for at, x, z in [(23.0, 3.6, 1.3), (44.0, 3.4, 0.2)]:
    add("ens10", T, at, x, z, face((x, z), (0.0, 1.4)))
# REVIEW 3's war reports (65.5 to the snap at 87.1): the British at the corners, guns on the four friends; the three
# of the verse turn their guns on them too
WAR = {"ens1": ((-3.3, -0.9), "lafayette", "W-USR"), "ens2": ((-2.0, -1.6), "hamilton", "W-USR"),
       "ens5": ((1.8, -1.2), "mulligan", "W-MSL"), "ens6": ((3.3, -0.9), "laurens", "W-MSL")}
FR = {65.5: {"lafayette": (-1.8, 2.6), "hamilton": (-1.3, 1.4), "mulligan": (0.3, 2.9), "laurens": (2.0, 2.4)},
      77.5: {"lafayette": (-1.9, 2.1), "hamilton": (-1.1, 1.6), "mulligan": (0.0, 2.6), "laurens": (1.7, 2.0)}}
for k, (m, (p, tgt, g)) in enumerate(WAR.items()):
    enter_from(m, T, 65.5, g, p[0], p[1], face(p, FR[65.5][tgt]), label="Ensemble %s" % m[3:], t_off=59.0 + 0.5 * k)
    add(m, T, 77.5, p[0], p[1], face(p, FR[77.5][tgt]))
    add(m, T, 85.2, p[0], p[1], face(p, FR[77.5][tgt]))
    exit_to(m, T, 85.2 + 0.3 * k, g)
for m, p, tgt in [("ens7", (-4.5, 0.4), "lafayette"), ("ens9", (4.9, 1.4), "laurens"), ("ens10", (3.4, 0.2), "laurens")]:
    add(m, T, 65.5, p[0], p[1], face(p, FR[65.5][tgt]))
    add(m, T, 77.5, p[0], p[1], face(p, FR[77.5][tgt]))
add("ens7", T, 85.3, -4.5, 0.4, -90)
exit_to("ens7", T, 85.3, "W-DSR")
add("ens9", T, 85.4, 4.9, 1.4, 90)
exit_to("ens9", T, 85.4, "W-MSL")
add("ens10", T, 82.5, 3.2, 1.6, -130)          # to Hamilton's chair, and off with it (props ham-chair-14)
exit_to("ens10", T, 85.5, "W-MSL")
# NOTES3 (Jack, 2026-10-14/15): "at 50 washington's desk should come off". No blackout there (cue 432's night raids, 44.95),
# so a free body strikes it: ens2 comes in through the deck door the desk came by, takes it from behind at 50.0 and goes
# back out with it (props.py SEGMENT 3); Washington stays at his place.
add("ens2", T, 45.6, ENT["D-UC"][0], ENT["D-UC"][1], off=True)
add("ens2", T, 50.0, 0.0, 0.3, 0, dwell=0.3)       # behind the desk (0, 0.85): it spans z 0.55-1.15
exit_to("ens2", T, 50.3, "D-UC")
# Charles Lee: ens3 walks on for his promotion, into his DL special (ch5, up from 87.1)
add("ens3", T, 80.0, ENT["W-DSL"][0], ENT["W-DSL"][1], off=True, label="Charles Lee")
add("ens3", T, 87.6, 2.45, 3.05, -20)      # SPOT: Lee's DL special (ch5 2.35-2.56, 3.02-3.33) is up from 87.1
add("ens3", T, 90.1, 2.45, 3.05, -20)
# FILM ROUND, Monmouth: six redcoats in the centre / SL, facing SR, advancing and falling back on Lee's four orders; the
# Americans hold SR (Burr among them: he dances in the war scenes, hamilton-lyrics)
BRIT = {"ens1": ((1.0, 1.4), "W-MSL"), "ens2": ((1.5, 2.6), "W-DSL"), "ens5": ((2.3, 0.7), "W-USL"),
        "ens6": ((2.9, 2.0), "W-MSL"), "ens7": ((3.5, 1.1), "W-USL"), "ens9": ((3.9, 2.6), "W-DSL")}
for k, (m, (p, g)) in enumerate(BRIT.items()):
    enter_from(m, T, 98.6, g, p[0], p[1], -90, label="Ensemble %s" % m[3:], t_off=89.5 + 0.5 * k)
    for at, dx in [(101.3, -1.0), (102.5, 0.0), (103.4, -1.0), (104.1, 0.0)]:
        add(m, T, at, p[0] + dx, p[1], -90)
    add(m, T, 105.6, p[0], p[1], -90)
    add(m, T, 114.1, p[0] + 0.4, p[1] + 0.2, -70)    # the heat: a slow sag back
    exit_to(m, T, 115.0 + 0.3 * k, g)                # off before the sepia camp (119.5)
enter_from("burr", T, 98.6, "W-MSR", -2.4, 1.6, 90, t_off=90.0)
add("burr", T, 105.6, -2.2, 1.8, 90)
add("burr", T, 114.1, -2.6, 1.8, 80)
# Burr stays: SL, under Lee on the gallery, through the slander; off SL as Lee goes
add("burr", T, 119.5, 3.8, 0.45, face((3.8, 0.45), (4.9, 1.8)))
add("burr", T, 137.3, 3.8, 0.45, 20)
exit_to("burr", T, 137.6, "W-MSL")
# Lee's battle: running back and forth in front, between the lines, yelling UP at Washington on the gallery
for at, x, z in [(98.6, 1.2, 4.0), (101.3, 1.0, 4.2), (102.5, -0.8, 4.0), (103.4, 0.9, 4.2), (104.1, -0.9, 4.0)]:
    add("ens3", T, at, x, z, face((x, z), WG))
for at, x, z, f in [(105.6, -2.4, 4.3, 45), (109.5, -1.8, 4.4, 30)]:
    add("ens3", T, at, x, z, f)
# off DR, round the back and up: along the upstage gallery onto the SL gallery, out to its DL end for the slander
_t = exit_to("ens3", T, 109.5, "W-DSR", extra=0.0)
add("ens3", T, _t + 0.3, 0.6, -4.8, y=GALY, off=True)
_t += 1.3 + 0.3
add("ens3", T, _t, 0.6, -3.35, y=GALY, dwell=0)
add("ens3", T, _t + 4.15 / 1.8, 4.75, -3.35, y=GALY, dwell=0)
add("ens3", T, _t + 4.91 / 1.8, 4.9, -2.6, y=GALY, dwell=0)
add("ens3", T, _t + 9.31 / 1.8, 4.9, 1.8, y=GALY, facing=-95)
add("ens3", T, 130.0, 4.9, 1.95, y=GALY, facing=-100)
add("ens3", T, 137.3, 4.9, 1.8, y=GALY, facing=-90, dwell=0.2)
add("ens3", T, 140.6, 4.9, -2.6, y=GALY, dwell=0)
add("ens3", T, 141.2, 4.75, -3.35, y=GALY, dwell=0)
add("ens3", T, 144.0, 0.6, -3.35, y=GALY, dwell=0)
add("ens3", T, 145.2, 0.6, -4.8, y=GALY, off=True)

# =====================================================================================
# 1-15  Ten Duel Commandments - REVIEW 2: staged from ETC's renders of Binkley's real cues (THPP Cue Photos.pdf,
# pp. 27-44, cues 450.01-476), which stand mannequins where each cue's light needs bodies:
#   450.01 the two duellists face each other in the centre pool, a second alone in each of the DR / DL pools;
#   452 #1 / 470 #9: duellists face to face at C, the seconds out at the sides; 454 #2 / 456 #3: the four in one row
#   across the middle, duellists facing, seconds facing in; 457 Company Vocal: the four facing out on the upstage arc
#   (the company is NOT on: they sing unseen); 458 #4 / 459 Ham/Burr DL / 460 #5: the four only, Hamilton and Burr
#   together right of centre; 461 Company Vocal -> 461.11 / 462 #6: a line of ten across at z ~0.5 (the strobe row
#   ch59-64 / 72-75 lands on it); 464 #7 / 466 #8: a loose cluster on the inner disc; 468 Ham/Burr scene: six or
#   seven, the company leaving; 470 #9 the four only again; 472 the count: duellists back to back at C, seconds in the
#   DR / DL specials; 474 the shot: one duellist DC at the lip (ch98), one up centre (ch18), seconds DR / DL.
# Cut (invented, and contradicted by the renders): the outer-ring opposed revolve of the duellists and seconds, the
# company line from the top, the two mirrored groups of four, the unison step on every number.
# =====================================================================================
T = "1-15"
# FILM ROUND (2026-10-24; research/seg3.md "Film round"), over the renders where the film shows otherwise:
#  - the company IS on from the top, at the edges of the deck and on the galleries, dancing in the dim light round the
#    four (film 9, 25, 45: bodies at both sides and up on the galleries, arms up) - the renders light only the
#    principals' pools; they come down into the line of #6 from there, and go back to the edges after #8, not off;
#  - #2/#3 (film 25): not a row of four but two pairs: Lee and Burr nose to nose at centre, Laurens and Hamilton
#    together SR;
#  - the Doctor comes on DS of centre with his bag (film 45), not up centre, and goes upstage after his commandment;
#  - the count (film 99-103): the company in a ring round the duellists on the turntable, dancing, the seconds in the
#    DR / DL corners (as the renders); they go after the shot.
DUEL = {"laurens": -1, "ens3": 1}          # SR / SL duellist
SEC = {"hamilton": -1, "burr": 1}           # Laurens' second SR, Lee's second SL
# the walk-on in the 1-14 FTB (158.1), placed when the three pools come up (1.6)
add("ens3", "1-14", 157.0, ENT["W-MSL"][0], ENT["W-MSL"][1], off=True, dwell=0, label="Charles Lee")
add("burr", "1-14", 157.2, ENT["W-DSL"][0], ENT["W-DSL"][1], off=True, dwell=0)
# REVIEW 3: the clip's comments at 0:01-0:07 ("intense staring", "about to kiss"): the two stand close, nose to nose
add("laurens", T, 1.6, -0.35, 1.84, 90)     # SPOT: the centre pool of preset 402 "3 pools" (ch13 -0.04, 1.84)
add("ens3", T, 1.65, 0.35, 1.84, -90)
add("hamilton", T, 1.6, -3.18, 3.86, 50)    # SPOT: the DR pool (ch12 -3.18, 3.86)
add("burr", T, 1.6, 3.35, 4.08, -50)        # SPOT: the DL pool (ch14 3.35, 4.08)
for a, s in DUEL.items():
    add(a, T, 14.9, s * 0.45, 0.95, -s * 90)                 # #1: face to face at C
for a, s in SEC.items():
    add(a, T, 16.5, s * 2.95, 1.5, -s * 60)                  # #1: out at the sides (ch11 / ch15)
# #2 / #3 (film 25): Lee and Burr nose to nose at centre, Laurens with Hamilton SR
add("laurens", T, 21.2, -3.2, 1.3, -90)
add("hamilton", T, 21.6, -3.7, 1.3, 90)
add("ens3", T, 21.8, -0.25, 0.95, 90)
add("burr", T, 22.2, 0.25, 0.95, -90)
for a in ("laurens", "hamilton", "ens3", "burr"):
    w = P[a][-1]
    add(a, T, 31.0, w["x"], w["z"], w.get("facing"))
# 457 Company Vocal: the four face out on the upstage arc
for a, p in {"hamilton": (-2.6, 0.2), "laurens": (-1.5, -0.4), "ens3": (1.5, -0.4), "burr": (2.6, 0.2)}.items():
    add(a, T, 34.6, p[0], p[1], 0)
# 458 #4
for a, p, f in [("laurens", (-2.5, -0.3), 20), ("hamilton", (-1.6, 0.5), 30), ("burr", (1.7, 1.2), -30), ("ens3", (2.9, 0.2), -20)]:
    add(a, T, 39.6, p[0], p[1], f)
# 459 "Hamilton/ Burr DL": the two seconds together right of centre, the duellists apart
add("burr", T, 42.0, 1.85, 2.05, -50)
add("hamilton", T, 43.0, 1.1, 2.75, 60)
add("laurens", T, 43.0, -0.2, -0.5, 0)
add("ens3", T, 43.0, 3.7, 2.6, -60)
# 460 #5
for a, p, f in [("laurens", (0.0, -0.5), 0), ("hamilton", (0.0, 0.9), 180), ("burr", (0.9, 2.7), 75), ("ens3", (3.7, 2.8), -90)]:
    add(a, T, 52.6, p[0], p[1], f)
# the company's places at the edges (the deck's sides and up centre), where they dance in the dim light
CO = ["ens1", "ens2", "ens5", "ens6", "ens7", "ens9"]
EDGE = {"ens1": ((-5.4, 2.6), "W-DSR"), "ens2": ((-5.0, -0.5), "W-MSR"), "ens5": ((-1.7, -2.6), "W-USR"),
        "ens6": ((1.7, -2.6), "W-USL"), "ens7": ((5.0, -0.5), "W-MSL"), "ens9": ((5.4, 2.6), "W-DSL")}
for m in CO:
    p, g = EDGE[m]
    enter_from(m, T, 6.0, g, p[0], p[1], face(p, (0.0, 1.0)), label="The Bullet" if m == "ens1" else "Ensemble %s" % m[3:])
    add(m, T, 52.0, p[0], p[1], face(p, (0.0, 1.0)))
# 461 Company Vocal -> 462 #6: the line of ten at z 0.5 (the four principals in the middle)
LZ = 0.5
LX = {"laurens": -3.15, "hamilton": -2.45, "ens1": -1.75, "ens2": -1.05, "ens5": -0.35, "ens6": 0.35, "ens7": 1.05,
      "ens9": 1.75, "burr": 2.45, "ens3": 3.15}
VIA = -1.2      # the company comes in upstage of the four and steps down into the line (clear of the Doctor)
for m in CO:
    add(m, T, 56.0, LX[m], VIA, dwell=0)
for a, x in LX.items():
    if a in ("laurens", "ens3"):
        add(a, T, 55.0, x, LZ, 0)        # the duellists are in their places first
    add(a, T, 57.3, x, LZ, 0)
    add(a, T, 58.3, x, LZ, 0, dwell=3.2 if a in CO else None)   # the company moves off the line all together at 61.5
# 464 #7 (held through 466 #8): a loose cluster on the inner disc, Hamilton and Burr outside it DR / DL
# REVIEW 3: the Odyssey Online (the Bullet): "the Bullet places herself directly at Hamilton's side ... the pair stand
# side by side for numbers six and seven of the Commandments, moving through the choreography in sync". She is beside
# him in the line at #6 already (LX); for #7 she goes with him to his place DR, and the cluster is the other five.
WEDGE_CO = [(0.0, 2.0), (-0.6, 1.35), (0.6, 1.35), (-0.3, 0.6), (0.3, 0.6)]
CO5 = [m for m in CO if m != "ens1"]
WA = assign(CO5, WEDGE_CO, {m: (LX[m], LZ) for m in CO5})
WA["ens1"] = (-2.05, 2.45)
for m in CO:
    add(m, T, 64.5, WA[m][0], WA[m][1], 0)
    add(m, T, 71.0, WA[m][0], WA[m][1], 0)
add("laurens", T, 64.5, -3.15, 0.5, 30)      # the duellists hold their line places either side of it
add("ens3", T, 64.5, 3.15, 0.5, -30)
add("hamilton", T, 64.5, -2.7, 2.5, 30)
add("burr", T, 64.5, 2.7, 2.5, -30)
# 468 the Hamilton/Burr scene: the company goes back to the edges (FILM ROUND: they are there for the count); the
# seconds negotiate in the front row (ch113 / ch112), the duellists wait in the two mid pools (ch119 / ch117)
for k, m in enumerate(["ens1"] + sorted(CO5, key=lambda q: (WA[q][1], abs(WA[q][0])))):
    x, z = WA[m]
    p = EDGE[m][0]
    t0 = 78.2 if m == "ens1" else 76.0 + 0.6 * k     # the Bullet waits for Hamilton to cross in front of her
    add(m, T, t0, x, z, 0, dwell=0)
    add(m, T, t0 + dist((x, z), p) / WALK + 0.3, p[0], p[1], face(p, (0.0, 1.0)))
    add(m, T, 95.6, p[0], p[1], face(p, (0.0, 1.0)))
add("laurens", T, 79.0, -1.83, 1.2, 30)
add("ens3", T, 79.0, 1.83, 1.2, 150)      # REVIEW 3: his back to the seconds' talk ...
add("ens3", T, 90.5, 1.83, 1.2, -31)      # ... then he turns round to Hamilton (the clip's comments at 1:32)
add("hamilton", T, 77.0, -2.6, 3.2, 70, dwell=0)     # a step DS first, round the Bullet at his side
add("hamilton", T, 79.6, 0.4, 3.6, 70)
add("burr", T, 79.0, 1.5, 3.5, -70)
add("hamilton", T, 91.0, 0.4, 3.6, 60)
add("burr", T, 91.0, 1.5, 3.5, -60)
# 470 #9: back to the #1 picture
for a, s in DUEL.items():
    add(a, T, 94.9, s * 0.45, 0.95, -s * 90)
for a, s in SEC.items():
    add(a, T, 95.6, s * 2.95, 1.5, -s * 60)
# 472 the count: back to back at C, the seconds into the DR / DL specials (ch42 / ch45, and the shot's ch97 / ch99)
add("laurens", T, 101.35, 0.0, 0.7, 180)
add("ens3", T, 101.4, 0.0, 1.2, 0)
for a, s in SEC.items():
    add(a, T, 101.0, s * 3.2, 4.0, -s * 50)                  # SPOT: ch42 (-3.01, 3.76) / ch45 (3.05, 3.68)
    add(a, T, 104.9, s * 3.2, 4.0, -s * 60)
# the paces, and the turn for the shot (474): Lee DC at the lip in ch98, Laurens up centre in ch18 (-1.62, -1.31)
add("laurens", T, 104.0, -1.5, -1.2, 15)
add("ens3", T, 104.0, 0.0, 4.75, -165)
# FILM ROUND, the count (film 101 / the overhead at 102): the company in a ring on the turntable round the duellists,
# clear of the two lines they pace along (Laurens up-left, Lee straight down), facing in; off after the shot
RING = [ring(2.45, th) for th in (40, 95, 140, 220, 265, 300)]
RA = assign(CO, RING, {m: EDGE[m][0] for m in CO})
for m in CO:
    p = RA[m]
    add(m, T, 99.2, p[0], p[1], face(p, (0.0, 0.95)))
    add(m, T, 105.2, p[0], p[1], face(p, (0.0, 0.95)))
    g = min(("W-DSR", "W-MSR", "W-USR", "W-DSL", "W-MSL", "W-USL"), key=lambda q: dist(p, ENT[q]))
    add(m, "1-16", dist(p, ENT[g]) / WALK + 0.6, ENT[g][0], ENT[g][1], off=True)
# the Doctor: on DS of centre with his bag for the commandment that names him (film 45), turns his back, then goes
# upstage centre out of the line's way, where he waits for the shot
add("ens4", T, 38.0, ENT["W-DSR"][0], ENT["W-DSR"][1], off=True, label="The Doctor")
add("ens4", T, 45.0, -2.2, 2.1, 60)
add("ens4", T, 50.0, -2.2, 2.1, 180)
add("ens4", T, 55.6, 0.0, -2.1, 180)

# =====================================================================================
# 1-16  Meet Me Inside - Lee hit DC, Washington arrives UC, the office. REVIEW 2: the company is not on (cue 476's
# render has an empty stage; the chant is sung unseen); two of them set the office furniture on the chant stab.
# =====================================================================================
T = "1-16"
# FILM ROUND (2026-10-24; research/seg3.md "Film round"): Lee, hit, staggers off to SL and goes down there with the
# Doctor at him (film 14 / 22.6: the pair far SL, then walking off); Hamilton and Laurens are far SR by the SR stair
# (film 3-14); Washington comes down to centre pointing at Lee (14); the office is the other way round: Hamilton SR of
# centre, hands behind his back, Washington SL of him (film 36-50, and 66-70 where Hamilton steps into his face).
LEE = (4.4, 2.9)
add("ens3", T, 1.5, 0.3, 4.6, -150)          # hit: he staggers where he stood for the shot ...
add("ens3", T, 6.0, LEE[0], LEE[1], -100)    # ... away to SL
add("ens3", T, 20.0, LEE[0], LEE[1], -120)
add("ens4", T, 1.5, 0.0, -2.1, 180, dwell=0)
add("ens4", T, 7.0, 3.85, 2.45, 50)          # the Doctor runs to him
add("ens4", T, 19.5, 3.85, 2.45, 60)
exit_to("ens4", T, 20.3, "W-DSL", label="Ensemble 4")
exit_to("ens3", T, 21.3, "W-DSL", label="Ensemble 3")
add("burr", T, 3.0, 2.9, 3.6, 70)
add("burr", T, 9.6, 2.9, 3.6, -150)
add("burr", T, 18.0, 2.9, 3.6, 80)
exit_to("burr", T, 19.0, "W-DSL")
# REVIEW 3: ironinkpen: "Ham and Laurens hug when Laurens comes out of the duel the winner"; the clip's comments
# (TZ1w59D5et4, 0:21): "hamilton held laurens back" - Laurens comes down to him, and stays at his side, held, until he goes
add("laurens", T, 3.0, -3.5, 1.6, -60)
add("laurens", T, 4.6, -4.7, 2.3, 120)       # the hug
add("laurens", T, 9.6, -4.7, 2.3, 100)
add("laurens", T, 17.0, -4.6, 2.35, 90)      # straining toward Lee; Hamilton holds him
add("laurens", T, 21.5, -4.7, 2.3, -60)
exit_to("laurens", T, 21.5, "W-DSR")
# REVIEW 3: hamiltonsideblog: he stands still, hands behind his back, then "steps right into Washington's face"; the
# clip's comments put it on his threat (1:10, the music cut at 70.25). Back in his place for Washington's order (74.4).
for at, x, z, f in [(2.5, -4.2, 2.8, -40), (4.6, -4.2, 2.8, -135), (9.6, -4.2, 2.8, 100), (16.5, -4.2, 2.8, 95),
                    (25.0, -4.0, 2.8, 90), (28.5, -1.3, 3.1, 60),
                    (31.6, -1.3, 3.1, 60), (43.4, -1.15, 3.2, 70), (57.0, -1.35, 3.65, 20), (63.0, -0.85, 3.3, 50),
                    (68.6, 0.5, 3.2, 85), (70.25, 0.5, 3.2, 85), (74.4, -1.3, 3.3, 60), (80.45, -1.4, 3.35, 0)]:
    add("hamilton", T, at, x, z, f)
add(W, T, 4.5, ENT["D-UC"][0], ENT["D-UC"][1], off=True)
for at, x, z, f in [(9.6, 0.4, -1.2, 30), (14.0, 1.4, 1.4, 90), (25.0, 0.5, 1.6, -60), (31.6, 1.25, 3.05, -60),
                    (43.4, 1.1, 3.2, -70), (50.0, 0.55, 3.35, -85), (57.0, 1.3, 3.1, -50), (63.0, 1.9, 2.9, -60), (70.25, 1.2, 3.2, -70), (74.4, 1.3, 3.0, 140)]:
    add(W, T, at, x, z, f)
exit_to(W, T, 77.6, "W-DSL")     # holds his place through his order; goes off DL with his desk on the button
# the office furniture, set on the chant stab (cue 478): ens2 the desk from SL behind Washington, ens6 Hamilton's bench
# from SR (film 26.6: two of the company bring the bench on at SR) to centre, where 1-17 plays (film: the bench between
# the two at its top)
add("ens2", T, 21.5, ENT["W-MSL"][0], ENT["W-MSL"][1], off=True, label="Ensemble 2")
add("ens2", T, 28.5, 2.45, 2.15, -40)
exit_to("ens2", T, 29.0, "W-MSL")
add("ens6", T, 21.4, ENT["W-MSR"][0], ENT["W-MSR"][1], off=True, label="Ensemble 6")
add("ens6", T, 29.0, 0.2, 2.65, 0)
exit_to("ens6", T, 29.5, "W-MSR")

# =====================================================================================
# 1-17  That Would Be Enough - Hamilton and Eliza alone
# =====================================================================================
T = "1-17"
# FILM ROUND (2026-10-24; research/seg3.md "Film round"). The film: at the top he stands SL of the bench with his back
# to her, Eliza SR of it (film ~3); she goes to him and they hold each other standing (17-28); he pulls away, bent over
# (58), and sits on the bench (60); she stands behind him, hands on his shoulders (67-80); she sits down beside him
# (101), on his SR, and the rest of the song is the two of them side by side on the bench (106-175). The chorus revolve
# about their midpoint and the step DC together were invented and are cut. The bench is at (0.2, 1.95) (props, set in
# 1-16); he sits on its SL half, she on its SR half.
SEAT_H, SEAT_E = (0.55, 2.3), (-0.15, 2.3)
add("hamilton", T, 2.5, 1.6, 2.6, 160)                                # his back to her, SL of the bench
enter_from("eliza", T, 5.5, "W-DSR", -0.9, 2.7, 70, t_off=0.0)
add("hamilton", T, 16.5, 1.55, 2.6, -90)
add("eliza", T, 17.0, 1.0, 2.6, 90)                                   # they hold each other (film 20)
add("eliza", T, 28.5, 0.95, 2.65, 80)
add("hamilton", T, 36.0, 2.6, 3.0, 120)                              # he turns away
add("eliza", T, 40.0, 1.3, 2.4, 70)
add("hamilton", T, 46.0, 1.5, 3.4, -150)
add("eliza", T, 50.0, 0.6, 3.0, 60)
add("hamilton", T, 56.5, 1.6, 2.5, -120)                              # bent over, she reaches for him (film 58)
add("hamilton", T, 60.5, SEAT_H[0], SEAT_H[1], 0)                     # onto the bench (film 60)
add("eliza", T, 61.0, 1.5, 2.85, -110)
add("eliza", T, 66.0, 0.6, 1.45, 0)                                   # behind him, hands on his shoulders (film 67-80)
add("eliza", T, 96.0, 0.6, 1.45, 0)
add("eliza", T, 97.6, -0.75, 1.85, dwell=0)                               # round the bench's SR end
add("eliza", T, 99.6, SEAT_E[0], SEAT_E[1], 0)                        # she sits down beside him (film 101)
# NOTES3 (Jack, 2026-10-14/15): "make hamilton and eliza wait to come off till the lights are fully out". The button
# (cue 501, 175.3) fades for 2.7 s: black at 178.0, the track's very end. So they hold their places through the fade and
# leave in the dark of 1-18's top (cue 560 lights only the balcony until 31): Eliza at 1-18 0.2, Hamilton at 0.5 with
# his bench (props.py SEGMENT 4); their off waypoints at W-DSR are gen4.py's (1-18 5.9 / 7.0).
add("eliza", T, 170.1, SEAT_E[0], SEAT_E[1], 0, dwell=8.1)            # SPOT: followspot 1 (follow.py)
add("hamilton", T, 170.2, SEAT_H[0], SEAT_H[1], 0, dwell=8.3)         # SPOT: followspot 2
# NOTES3 (Jack): "burr should already be on the balcony by the time the light goes to him" - cue 560 brings the balcony
# special up at 1-18 0.0, so he is there before it: on in the fade from the SL wing's landing beside the gallery (2.48 m,
# tools/hamilton-floor.json), 4.3 m along the SL gallery (the back way through G-UC is 11.5 m, seen under the last line)
add("burr", T, 175.3, 6.6, -1.0, y="top", off=True)
add("burr", T, 176.05, 5.4, -0.6, y="gallery", dwell=0)
add("burr", T, 177.5, 5.3, 1.9, y="gallery", dwell=0)
add("burr", T, 177.8, 5.49, 2.36, y="gallery", facing=-40)           # the G&S spot (gen4.py GS); he holds it into 1-18
CARRIED = {"hamilton", "eliza", "burr"}   # their paths go on into segment 4 without an `off` at 1-17's end

# =====================================================================================
TI = {t: i for i, t in enumerate(TRACKS)}
bad = []
for a, path in P.items():
    path.sort(key=lambda w: clock(w["track"], w["at"]))
    for u, v in zip(path, path[1:]):
        if clock(v["track"], v["at"]) <= clock(u["track"], u["at"]):
            bad.append((a, u, v))
    if not path[0].get("off") or (not path[-1].get("off") and a not in CARRIED):
        bad.append((a, "not off at ends", path[0], path[-1]))
    if "label" not in path[0]:
        bad.append((a, "first waypoint unlabelled"))
for b in bad:
    print("PROBLEM", b)

NOTES = open(os.path.join(HERE, "seg3-notes.txt"), encoding="utf-8").read().strip()
out = {"segment": 3, "tracks": TRACKS, "waypoints": {a: P[a] for a in sorted(P)}, "notes": NOTES}
os.makedirs(os.path.join(HERE, "segments"), exist_ok=True)
with open(os.path.join(HERE, "segments", "seg3.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, indent=1)
print("waypoints:", sum(len(v) for v in P.values()), "actors:", len(P))

# ---- spacing check: sample linear interpolation every 0.5 s on the show clock -------------------
def pos(path, t):
    pts = [(clock(w["track"], w["at"]), w) for w in path]
    def hid(x, z, off): return off or abs(x) > 6.4 or z < -4.0
    if t <= pts[0][0]: w = pts[0][1]; return (w["x"], w["z"], hid(w["x"], w["z"], w.get("off", False)))
    if t >= pts[-1][0]: w = pts[-1][1]; return (w["x"], w["z"], hid(w["x"], w["z"], w.get("off", False)))
    for (t0, a), (t1, b) in zip(pts, pts[1:]):
        if t0 <= t <= t1:
            d = math.hypot(b["x"] - a["x"], b["z"] - a["z"])
            dw = a.get("dwell")
            dep = t0 if dw == 0 else (t0 + dw if dw is not None else max(t0, t1 - d / WALK))
            f = 0.0 if t <= dep else (t - dep) / max(1e-6, t1 - dep)
            x = a["x"] + f * (b["x"] - a["x"]); z = a["z"] + f * (b["z"] - a["z"])
            return (x, z, hid(x, z, (a.get("off") and f == 0) or (a.get("off") and b.get("off"))))
if "--space" in sys.argv:
    seen = {}
    t = 0.0
    end = START["1-17"] + LEN["1-17"]
    names = sorted(P)
    while t < end:
        ps = {a: pos(P[a], t) for a in names}
        for i, a in enumerate(names):
            for b in names[i + 1:]:
                pa, pb = ps[a], ps[b]
                if pa[2] or pb[2]: continue
                d = math.hypot(pa[0] - pb[0], pa[1] - pb[1])
                if d < 0.5:
                    key = (a, b)
                    tr = max(tt for tt in TRACKS if START[tt] <= t)
                    seen.setdefault(key, []).append((tr, round(t - START[tr], 1), round(d, 2)))
        t += 0.5
    for k, v in seen.items():
        print("CLOSE", k, v[0], "...", v[-1], "n=%d" % len(v))
