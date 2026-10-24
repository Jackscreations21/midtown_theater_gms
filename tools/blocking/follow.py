#!/usr/bin/env python3
"""The Hamilton followspots: writes assets/hamilton-follow.json, which midtown.html plays on the show clock.

    python -I follow.py                       # validate, then write assets/hamilton-follow.json
    python -I follow.py --check [--tracks 1-03,1-04] [--blocking FILE]
                                              # also pose every target through every pick-up (tools/blocking-plot.py's pose)
                                              # against the blocking (default assets/hamilton-blocking.json) and print
                                              # every problem: a target offstage, hidden, off the stage or out of reach
    python -I follow.py --list [--tracks 1-03]   # print the plot, spot by spot, in show order

THE THREE SPOTS are the Lycians in house 1's followspot booth (assets/hamilton-rig.json `lycian-1..3`), at the back of
the house, 4 m up, 23 m from the proscenium:  1 = centre, 2 = house left (best on stage RIGHT), 3 = house right (best on
stage LEFT). Any spot reaches the whole deck and both galleries; pick the one whose side the target is on when it matters
(a long throw across the stage flattens the pool into an oval).

A spot is a pure function of the show clock, like the actors: at any moment each spot is either dark, or lit on one
actor, its beam aimed at her and sized to her, so seek = play. The page aims it every frame at where the actor IS
(the pose the actors are drawn from), so a spot FOLLOWS: nobody needs a waypoint for the light.

HOW AN ENTRY IS WRITTEN. One call per entry, in a segment's list (times are seconds into the album track, as the page's
readout and the footage frames' `at` give them):

    F(spot, track, at, who, size='full', level=1.0, fade=0.5, move=0.8, gel=None, note='')
        PICK UP `who` (an actor id: tools/hamilton-cast.json — the BODY, so act two's Jefferson is 'lafayette', Madison
        'mulligan', Philip 'laurens', Maria 'peggy', Charles Lee 'ens3'; the head label tells them apart on the page).
        If the spot is dark it snaps onto her and fades up over `fade` s. If it is already lit on someone else it PANS to
        her over `move` s (an operator swinging across) at the new size and level — write OUT then F for a dark re-pick.
        If it is lit on her already, the new size / level / gel take over over `fade` s (an iris or a level change).
          size   'full' (head to toe, ~2.2 m pool at her), 'half' (waist up, ~1.3 m), 'head' (head and shoulders, ~0.7 m),
                 or a number: the pool's diameter at her in metres.
          level  0..1 at the lamp (a xenon spot at 1.0 is the brightest thing on the stage: a principal in a full look
                 still reads at 0.6-0.8; a solo in a dark stage at 0.8-1.0).
          gel    None (open white, 6000 K) or one of the boomerang frames: 'R3314', 'R33', 'R302', 'R362', 'R54', 'R02'.
    OUT(spot, track, at, fade=1.0, note='')
        fade the spot out over `fade` s (0 = a snap, for a blackout).

    note   what the entry is for and what it was read from ("film 1-03 0:42 wide: the spot finds him on 'I am not'").
           Every entry should say why; Jack reads these.

RULES the validator holds:
  - entries of one spot are in time order and each spot has at most one entry at one moment;
  - every segment ENDS with all three spots out (an OUT at or before the end of its last track), so the segments are
    independent and a seek into any song finds them dark at its top unless that song picks them up;
  - `who` is a cast id, `track` a track id, `0 <= at <= the track's len`, sizes / levels / gels in range.
--check adds what only the blocking can tell: the target offstage (hidden) or off the stage (|x| > 7.5, z > 5.6) at the
pick-up or at any half-second while the spot is on her, and the same body on two spots at once (legal, reported).

THE EIGHT SECTIONS below are one per segment, like dance.py and props.py: an agent edits only its own.
Standard library only.
"""
import importlib.util, json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT_FILE = os.path.join(ROOT, 'assets', 'hamilton-follow.json')
SIZES = {'full': 2.2, 'half': 1.3, 'head': 0.7}
GELS = ('R3314', 'R33', 'R302', 'R362', 'R54', 'R02')

_E = []
def F(spot, track, at, who, size='full', level=1.0, fade=0.5, move=0.8, gel=None, note=''):
    return dict(spot=spot, track=track, at=at, who=who, size=size, level=level, fade=fade, move=move, gel=gel, note=note)
def OUT(spot, track, at, fade=1.0, note=''):
    return dict(spot=spot, track=track, at=at, out=True, fade=fade, note=note)


# ===== SEGMENT 1 (1-01..1-06) =====
# The film round (2026-10-24; tools/blocking/research/seg1.md "Film round" has the frames read). Spot 2 (house left) for
# stage RIGHT, spot 3 (house right) for stage LEFT, spot 1 centre. Levels: a principal inside a full look 0.6-0.8, a
# solo in a dark stage 0.85-1.0.
SEGMENT_1 = [
    # ---- 1-01 Alexander Hamilton: the clip is Disney's promo montage (looks only, no times): each narrator is a bright
    # figure in a dark city (shots 9-10, 14). So each narrator gets a spot for his verse, on the cues' own labels; Hamilton
    # carries a spot from the women's send-off to the button; the gallery singers are picked up one by one at the end.
    F(2, '1-01', 0.0, 'burr', level=0.85, fade=1.0, note='Q37: Burr\'s opening verse DSR (film shot 10 look: Burr bright against the blue)'),
    OUT(2, '1-01', 16.5, fade=1.5, note='he gives the floor to Laurens'),
    F(3, '1-01', 18.6, 'laurens', level=0.85, note='Q38 verse 2: Laurens, SL'),
    OUT(3, '1-01', 33.5, fade=1.0, note='his verse done'),
    F(2, '1-01', 33.5, 'lafayette', level=0.85, note='Q39 verse 3: Jefferson (Lafayette\'s body), SR'),
    OUT(2, '1-01', 48.4, fade=1.0, note='Q40 the hurricane'),
    F(1, '1-01', 48.4, 'mulligan', level=0.8, note='Q40: Madison (Mulligan\'s body) brings the storm'),
    OUT(1, '1-01', 56.0, fade=1.0, note='Q41 he writes: the warm returns'),
    F(2, '1-01', 56.0, 'burr', level=0.8, note='Q41: Burr narrates him writing'),
    OUT(2, '1-01', 63.4, fade=1.0, note='Q42 the company takes the story'),
    F(1, '1-01', 85.9, 'hamilton', level=0.8, fade=1.0, note='Q45: the company around Hamilton, after his single shaft (Q44)'),
    F(3, '1-01', 93.2, 'eliza', level=0.8, note='Q47 Eliza\'s verse'),
    OUT(3, '1-01', 105.0, fade=2.0, note='Q48 his mother dies: the cold drop'),
    OUT(1, '1-01', 105.2, fade=2.0, note='Q48: the cold drop'),
    F(2, '1-01', 119.8, 'burr', level=0.8, note='Q50 Burr the reader, in his AF'),
    OUT(2, '1-01', 130.0, fade=1.0, note='Q51 clerking'),
    F(1, '1-01', 130.0, 'mulligan', level=0.8, note='Q51 clerking: Mulligan drives it'),
    OUT(1, '1-01', 141.3, fade=1.0, note='Q52 the voyage'),
    F(1, '1-01', 166.3, 'hamilton', level=0.85, fade=0.8, note='Q56 the women send him off (coat, book, bag): the spot carries him from here to the button'),
    F(3, '1-01', 214.0, 'laurens', level=0.85, fade=0.3, note='Q62 Laurens alone, on the upstage gallery'),
    F(3, '1-01', 215.9, 'washington', level=0.85, move=0.8, note='Q63 Washington on the SR balcony (a long throw: the cue\'s own special is there too)'),
    F(3, '1-01', 217.4, 'eliza', size=3.0, level=0.8, move=0.8, note='Q64 the women on the SL balcony: opened up to take the three'),
    OUT(3, '1-01', 219.6, fade=0.5, note='Q65 Burr\'s confession'),
    F(2, '1-01', 219.6, 'burr', level=0.9, fade=0.4, note='Q65 Burr\'s confession, alone at centre'),
    OUT(2, '1-01', 233.9, fade=0, note='the button\'s blackout'),
    OUT(1, '1-01', 233.9, fade=0, note='the button\'s blackout'),
    # ---- 1-02 Aaron Burr, Sir: the street is dark and blue (film frames 10-440): the two men are the scene, each in a
    # spot as they walk it; the friends' verses at the table each get the third spot.
    F(3, '1-02', 0.3, 'hamilton', level=0.8, fade=1.0, note='film 1-02 frame 10 (at 1.4): he stands alone centre in a hard pool as the company clears; the spot stays with him as he crosses to Burr and walks the street SL'),
    F(1, '1-02', 4.6, 'burr', level=0.75, fade=1.5, note='Burr strolls down from upstage SL into the street (film frame 30, at 5.5); spot 1 holds him through the scene'),
    F(2, '1-02', 89.4, 'laurens', level=0.85, note='Q86/87: Laurens bursts in mug up (film frame 440) and sings his verse at the table\'s SL end'),
    F(2, '1-02', 102.8, 'lafayette', level=0.85, move=0.6, note='Q88: Lafayette\'s verse at the table\'s SR end'),
    F(2, '1-02', 115.6, 'mulligan', level=0.85, move=0.6, note='Q89: Mulligan\'s verse behind the table'),
    OUT(2, '1-02', 127.6, fade=1.5, note='Q90 the toast: the tavern\'s own light takes the four'),
    F(1, '1-02', 133.7, 'burr', size='full', level=0.9, fade=0.4, note='Q91 they turn on Burr: he crosses to SR into his AF, the spot up on him'),
    OUT(1, '1-02', 142.0, fade=2.0, note='Q92 Burr sits it out in the SR corner: let him go'),
    # ---- 1-03 My Shot: spot 3 stays on Hamilton from 1-02 (he steps DSC into the number) and carries him through it;
    # the friends' verses and Burr's warning each get a spot; the death verse puts him alone at the SR edge in spot 2
    F(3, '1-03', 6.1, 'hamilton', level=0.9, note='Q101 verse 1: he works the room (film 1-03 frames 49-251: the tavern dark round him, he is the bright one)'),
    F(2, '1-03', 94.9, 'lafayette', level=0.85, note='Q111 Lafayette\'s verse by the table SR (film frame 486: a close-up, mug in hand)'),
    F(1, '1-03', 106.8, 'mulligan', level=0.85, note='Q113 Mulligan\'s verse, centre beside Hamilton (film frame 542)'),
    OUT(1, '1-03', 117.5, fade=0.8, note='his verse done'),
    F(2, '1-03', 117.5, 'laurens', level=0.85, move=0.7, note='Q115 Laurens\'s verse just SR of centre (film frame 592); spot 2 swings from Lafayette to him'),
    F(1, '1-03', 125.0, 'burr', level=0.8, fade=1.0, note='Q117 Burr comes down from his chair to cool them down (into his AF DSR)'),
    OUT(2, '1-03', 128.0, fade=1.2, note='Burr\'s moment: the friends drop out of the light'),
    OUT(1, '1-03', 138.9, fade=1.5, note='Q118 Burr leaves the tavern'),
    OUT(3, '1-03', 159.8, fade=1.5, note='Q119 the quiet confession: Jack\'s ruling is ONE white spot at centre (the ch13 shaft), so the followspot goes'),
    F(3, '1-03', 168.2, 'hamilton', level=0.9, fade=0.3, note='Q121 chorus 2: back on him as the room comes up'),
    F(2, '1-03', 203.5, 'laurens', level=0.85, note='Q124 the rise-up: "Laurens takes the lead" (the Disney+ clip\'s 3:24)'),
    OUT(3, '1-03', 231.9, fade=1.0, note='Q127: he leaves the centre for the SR edge; spot 2 takes him there'),
    F(2, '1-03', 232.2, 'hamilton', size='full', level=1.0, move=1.2, note='Q127 the death verse: film 1-03 frames 1205-1280 -- he sings it from the SR edge by the stair, alone in a hard white pool, the company in blue at centre'),
    F(3, '1-03', 254.6, 'hamilton', level=0.9, fade=0.3, note='Q129 the snap back: he comes back to centre'),
    OUT(2, '1-03', 255.2, fade=0.3, note='Q129: spot 3 has him again'),
    OUT(3, '1-03', 331.25, fade=0, note='the button: the blackout (cue 139.5)'),
    # ---- 1-04 The Story of Tonight: four warm chair pools and the DS specials carry it (Jack's 10-16 ruling); the one
    # moment outside them is Laurens toasting from apart, SL
    F(3, '1-04', 27.0, 'laurens', size='full', level=0.6, fade=1.5, gel='R02', note='film 1-04 frame 150 (at 30): Laurens apart SL, raising his cup to the three -- out of the chair pools, so a soft spot finds him there'),
    OUT(3, '1-04', 37.5, fade=1.5, note='Q143: he is back with them'),
    # ---- 1-05 The Schuyler Sisters: the film lights the three sisters hard and bright all number long (frames 120-912:
    # three bright gowns against a warm-brown city). Spot 2 (house left) has Angelica, who works the SR half; spot 1
    # Eliza at centre; spot 3 Peggy SL. Burr's narration and his summer verse borrow a spot.
    F(2, '1-05', 4.4, 'burr', level=0.8, note='Q150: Burr runs on to DSR and introduces the scene (Jack: from USL to DSR); the spot catches him there'),
    F(2, '1-05', 21.9, 'angelica', level=0.9, move=1.0, note='Q152: Angelica revealed up from the deck door; spot 2 swings from Burr to her and stays with her'),
    F(1, '1-05', 24.2, 'eliza', level=0.85, note='Q153: Eliza revealed'),
    F(3, '1-05', 25.9, 'peggy', level=0.85, note='Q154: Peggy revealed'),
    OUT(3, '1-05', 51.0, fade=1.5, note='Q159 Angelica\'s verse: Peggy steps back'),
    F(1, '1-05', 64.9, 'burr', level=0.8, move=1.0, note='Q161: Burr sidles in to Angelica; spot 1 leaves Eliza for him (film frame 461: face to face with her)'),
    F(1, '1-05', 94.6, 'eliza', level=0.8, move=1.0, note='Q164: she rebuffs him and he backs to the DSR corner; spot 1 back to Eliza'),
    F(2, '1-05', 99.8, 'angelica', size='full', level=1.0, note='Q165 her solo: film frame 551 (at 110) -- she sings it at centre, out in front, in a hard bright pool'),
    F(3, '1-05', 115.5, 'peggy', level=0.85, fade=0.4, note='Q167 the anthem: all three sisters lit again'),
    F(2, '1-05', 117.0, 'angelica', level=0.9, fade=1.0, note='Q167: back to her full-look level'),
    OUT(2, '1-05', 183.0, fade=0.6, note='the sisters go in the button\'s last seconds'),
    OUT(1, '1-05', 183.4, fade=0.6, note='the sisters go'),
    OUT(3, '1-05', 183.0, fade=0.6, note='the sisters go'),
    # ---- 1-06 Farmer Refuted: a debate, so the two debaters each have a spot the whole scene (film shots 1-12: Seabury
    # bright on his box SL, Hamilton bright wherever he is); Burr gets one when he steps in at the end
    F(3, '1-06', 1.0, 'ens2', level=0.85, note='Q175: Seabury up on his box SL reading his paper (film shot 1, at 9: the brightest man on the stage)'),
    F(2, '1-06', 16.4, 'hamilton', level=0.9, note='Q177: Hamilton cuts in from DSR (film shot 2)'),
    F(1, '1-06', 46.1, 'hamilton', level=0.9, fade=0.3, note='Q180 the duet: he crosses SL to the box; spot 1 takes him there'),
    OUT(2, '1-06', 46.6, fade=0.8, note='spot 1 has him'),
    F(2, '1-06', 96.5, 'burr', level=0.8, note='Q186: Burr steps in to calm him (film shot 11)'),
    OUT(2, '1-06', 103.6, fade=1.0, note='Q188 the herald\'s special takes the stage'),
    OUT(1, '1-06', 103.8, fade=1.0, note='Q188: the King\'s herald'),
    OUT(3, '1-06', 103.8, fade=1.0, note='Q188: the King\'s herald'),
]
# ===== END SEGMENT 1 =====

# ===== SEGMENT 2 (1-07..1-11) =====
SEGMENT_2 = [
    # 1-07 You'll Be Back: one hard white pool on the King, head to toe, the whole number (the clip: frame 60, 10.6, he
    # walks into a bright front pool at the lip, and every wide after it has him in it); out as he goes in the transition
    F(1, '1-07', 3.6, 'king', level=0.9, fade=1.5, note="film 1-07 frames 20 / 60: the reveal at the door, then the front spot follows him down to the lip"),
    OUT(1, '1-07', 204.8, fade=1.0, note="the button: he leaves SL in the dark"),
    # 1-08 Right Hand Man
    F(2, '1-08', 29.8, 'hamilton', level=0.75, note="his verse (Q206 'Ham dsc'); film frames 200 / 250: he works the group SR, the spot with him"),
    OUT(2, '1-08', 54.0, fade=0.8, note="he goes off DSR (NOTES3: off at 0:55)"),
    F(3, '1-08', 53.4, 'burr', level=0.7, note="Burr announces the General from DL"),
    OUT(3, '1-08', 68.5, note="Burr leaves DSL"),
    F(1, '1-08', 65.2, 'washington', level=0.9, fade=0.8, note="his first line (Q274.01); film frame 290: the General DSC in a hard white pool, the company dancing round him, and the spot stays on him to the end"),
    F(2, '1-08', 129.2, 'hamilton', level=0.8, note="film frame 660: Hamilton's battle verse DR"),
    OUT(2, '1-08', 142.0, note="he goes off to take the cannons"),
    F(2, '1-08', 180.5, 'burr', level=0.7, note="the tent: Burr pleads SR of the desk (film frame 1030)"),
    OUT(2, '1-08', 212.5, note="dismissed"),
    F(3, '1-08', 203.3, 'hamilton', level=0.8, note="the tent: Hamilton DL of the desk; holds him through the duet and the file"),
    OUT(1, '1-08', 318.0, fade=0.5, note="the button: blackout"),
    OUT(3, '1-08', 318.0, fade=0.5, note="the button: blackout"),
    # 1-09 A Winter's Ball (no clip): the narrator, the man, the sister he meets
    F(1, '1-09', 1.8, 'burr', level=0.85, note="Q290 Burr DSC in ch93's shaft; the spot follows him DR, back DSC and out DL to the ball"),
    F(2, '1-09', 35.2, 'hamilton', level=0.75, note="the lineup: Hamilton's refrain, then the ball"),
    F(3, '1-09', 49.5, 'angelica', level=0.75, note="Q292.5 Angelica in at the centre; Hamilton kisses her hand"),
    OUT(1, '1-09', 68.0, note="into Helpless"),
    OUT(2, '1-09', 68.0, note="into Helpless"),
    OUT(3, '1-09', 68.0, note="into Helpless"),
    # 1-10 Helpless: Eliza's number - spot 1 on her throughout; spot 2 on Hamilton from first sight; spot 3 for Angelica
    # and Papa Schuyler's moment
    F(1, '1-10', 0.5, 'eliza', level=0.85, fade=1.0, note="film frame 10: Eliza in the middle of the ball; her number, the spot never leaves her"),
    F(3, '1-10', 28.5, 'angelica', level=0.7, note="Q300.6 the sisters' triangle; Angelica brings him to Eliza from the SR stair (film frames 380 / 440)"),
    F(2, '1-10', 36.5, 'hamilton', level=0.75, note="film frame 180 (36): first sight, Hamilton at the SL stair's foot"),
    OUT(3, '1-10', 112.5, note="the letters: Angelica gives Eliza the floor"),
    F(3, '1-10', 132.8, 'ens4', level=0.7, note="Q302.5 Papa Schuyler crosses to Hamilton: the blessing"),
    OUT(3, '1-10', 141.0, note="the men share a drink"),
    OUT(1, '1-10', 248.0, fade=0.8, note="the kiss on the chord"),
    OUT(2, '1-10', 248.0, fade=0.8, note="the kiss on the chord"),
    # 1-11 Satisfied: Angelica's number - spot 1 on her from the toast to her last line; spot 2 on Hamilton when he leads;
    # spot 3 on Eliza (the UL pool, the letters) and on Hamilton at the toast replayed (DL)
    F(1, '1-11', 9.8, 'angelica', level=0.9, fade=1.0, note="the toast: Angelica DC; film frames 180 / 520 / 1100: she is in the brightest light all through"),
    F(2, '1-11', 91.2, 'hamilton', level=0.75, note="Q370 first sight replayed: he unfreezes DR and comes to her"),
    OUT(2, '1-11', 126.5, note="back to Burr: the room turns"),
    F(3, '1-11', 159.6, 'eliza', level=0.7, note="Eliza in the UL pool, frozen for the replay"),
    F(2, '1-11', 196.2, 'hamilton', level=0.75, note="Angelica fetches him from the steps; Q377 count 2, Hamilton in a spotlight (fan write-up)"),
    OUT(3, '1-11', 205.5, note="the introduction: the room's light takes over"),
    OUT(2, '1-11', 226.5, note="he goes off SL"),
    F(3, '1-11', 238.2, 'eliza', level=0.7, note="Q380 the letters: Eliza crosses to Peggy and Angelica"),
    F(2, '1-11', 243.6, 'hamilton', level=0.7, note="Q381 the night fantasy: Hamilton DR"),
    OUT(2, '1-11', 252.5, note="he goes off DSR"),
    OUT(3, '1-11', 256.0, note="the rewind forward"),
    F(3, '1-11', 270.0, 'hamilton', level=0.75, note="Q384 back at the toast: the couple DL (spot 3 for SL)"),
    OUT(3, '1-11', 300.0, note="the company falls away"),
    OUT(1, '1-11', 325.5, fade=0.3, note="Angelica alone: out on the last word, before she walks off"),
]
# ===== END SEGMENT 2 =====

# ===== SEGMENT 3 (1-12..1-17) =====
SEGMENT_3 = [
]
# ===== END SEGMENT 3 =====

# ===== SEGMENT 4 (1-18..1-23) =====
SEGMENT_4 = [
]
# ===== END SEGMENT 4 =====

# ===== SEGMENT 5 (2-01..2-05) =====
SEGMENT_5 = [
]
# ===== END SEGMENT 5 =====

# ===== SEGMENT 6 (2-06..2-10) =====
SEGMENT_6 = [
]
# ===== END SEGMENT 6 =====

# ===== SEGMENT 7 (2-11..2-16) =====
SEGMENT_7 = [
]
# ===== END SEGMENT 7 =====

# ===== SEGMENT 8 (2-17..2-23) =====
SEGMENT_8 = [
]
# ===== END SEGMENT 8 =====

SEGMENTS = [('1-01', '1-06', SEGMENT_1), ('1-07', '1-11', SEGMENT_2), ('1-12', '1-17', SEGMENT_3), ('1-18', '1-23', SEGMENT_4),
            ('2-01', '2-05', SEGMENT_5), ('2-06', '2-10', SEGMENT_6), ('2-11', '2-16', SEGMENT_7), ('2-17', '2-23', SEGMENT_8)]


def load(path):
    return json.load(open(path, encoding='utf-8'))


def build():
    """validate every section; -> (the file's dict, [errors], tracks by id)"""
    show = load(os.path.join(ROOT, 'assets', 'hamilton-show.json'))
    tracks = {t['id']: dict(t, i=k) for k, t in enumerate(show['tracks'])}
    cast = {a['id'] for a in load(os.path.join(ROOT, 'tools', 'hamilton-cast.json'))['actors']}
    errs, spots = [], {1: [], 2: [], 3: []}
    for n, (first, last, entries) in enumerate(SEGMENTS, 1):
        lo, hi = tracks[first]['i'], tracks[last]['i']
        for e in entries:
            where = 'segment %d, spot %s %s %s: ' % (n, e.get('spot'), e.get('track'), e.get('at'))
            if e.get('spot') not in spots: errs.append(where + 'spot must be 1, 2 or 3'); continue
            t = tracks.get(e.get('track'))
            if not t: errs.append(where + 'no such track'); continue
            if not lo <= t['i'] <= hi: errs.append(where + 'the track is not in this segment'); continue
            if not isinstance(e['at'], (int, float)) or not 0 <= e['at'] <= float(t['len']): errs.append(where + 'at must be 0..%s' % t['len']); continue
            if not isinstance(e.get('fade'), (int, float)) or e['fade'] < 0: errs.append(where + 'fade must be >= 0')
            if not e.get('out'):
                if e['who'] not in cast: errs.append(where + 'who %r is not a cast id' % e['who'])
                sz = e['size']
                if not (sz in SIZES or (isinstance(sz, (int, float)) and 0.3 <= sz <= 6)): errs.append(where + 'size must be full/half/head or 0.3..6 m')
                if not (isinstance(e['level'], (int, float)) and 0 < e['level'] <= 1): errs.append(where + 'level must be in (0, 1]')
                if e['gel'] is not None and e['gel'] not in GELS: errs.append(where + 'gel must be None or one of ' + ', '.join(GELS))
                if not isinstance(e.get('move'), (int, float)) or e['move'] < 0: errs.append(where + 'move must be >= 0')
            spots[e['spot']].append(dict(e, seg=n, key=(t['i'], float(e['at']))))
        for s in (1, 2, 3):                          # each segment ends dark
            mine = sorted((e for e in spots[s] if e['seg'] == n), key=lambda e: e['key'])
            if mine and not mine[-1].get('out'):
                errs.append('segment %d: spot %d is still on %s at the end of the segment (add an OUT)' % (n, s, mine[-1]['who']))
    out = {}
    for s, L in spots.items():
        L.sort(key=lambda e: e['key'])
        for a, b in zip(L, L[1:]):
            if a['key'] == b['key']: errs.append('spot %d: two entries at %s %s' % (s, a['track'], a['at']))
        out[str(s)] = [{k: v for k, v in e.items() if k not in ('seg', 'key', 'spot') and not (k == 'gel' and v is None) and not (k == 'note' and not v)}
                       for e in L]
    doc = {'what': 'The three followspots (lycian-1 centre, -2 house left, -3 house right), generated by tools/blocking/follow.py. '
                   'Per spot, entries in show order: a pick-up {track, at, who, size, level, fade, move, gel?} or {track, at, out: true, fade}. '
                   'Sizes: full 2.2 m, half 1.3 m, head 0.7 m, or the pool diameter at the actor in metres.',
           'sizes': SIZES, 'gels': list(GELS), 'spots': out}
    return doc, errs, tracks


def check(doc, tracks, only, blocking):
    spec = importlib.util.spec_from_file_location('blocking_plot', os.path.join(ROOT, 'tools', 'blocking-plot.py'))
    BP = importlib.util.module_from_spec(spec); spec.loader.exec_module(BP)
    _, btracks, actors = BP.load_inputs(blocking)
    by = {a['id']: a for a in actors}
    probs, onto = [], {}
    for s, L in doc['spots'].items():
        for k, e in enumerate(L):
            if e.get('out') or (only and e['track'] not in only): continue
            nxt = L[k + 1] if k + 1 < len(L) else None
            t0 = btracks[e['track']]['start'] + e['at']
            t1 = (btracks[nxt['track']]['start'] + nxt['at']) if nxt else t0 + 1
            a = by.get(e['who'])
            if not a: probs.append('spot %s %s %.2f: %s has no path in the blocking' % (s, e['track'], e['at'], e['who'])); continue
            bad, T = [], t0
            while T <= t1 + 1e-9:
                p = BP.pose(a['c'], T)
                why = 'no pose' if not p else 'offstage' if not p['visible'] else 'off the stage (%.1f, %.1f)' % (p['x'], p['z']) if abs(p['x']) > 7.5 or p['z'] > 5.6 else None
                if why: bad.append((T - btracks[e['track']]['start'], why))
                onto.setdefault(round(T * 2) / 2, []).append((s, e['who']))
                T += 0.5
            if bad:
                probs.append('spot %s %s %.2f on %s: %s at %s' % (s, e['track'], e['at'], e['who'], bad[0][1],
                             ', '.join('%.1f' % b[0] for b in bad[:8]) + (' … (%d)' % len(bad) if len(bad) > 8 else '')))
    for T, L in sorted(onto.items()):
        whos = [w for _, w in set(L)]                # one spot counts once: an iris / level change on her samples its own moment twice
        for w in set(whos):
            if whos.count(w) > 1: probs.append('note: %s is on %d spots at show time %.1f' % (w, whos.count(w), T))
    return probs


def main(argv):
    doc, errs, tracks = build()
    for e in errs: print('ERROR', e)
    only = None
    if '--tracks' in argv: only = set(argv[argv.index('--tracks') + 1].split(','))
    if '--list' in argv:
        for s, L in doc['spots'].items():
            for e in L:
                if only and e['track'] not in only: continue
                print('spot %s  %s %7.2f  %s' % (s, e['track'], e['at'], 'OUT' if e.get('out') else '%s %s @%.2f%s' % (
                    e['who'], e['size'], e['level'], ' ' + e['gel'] if e.get('gel') else '')), ' -', e.get('note', ''))
    if errs: print('%d errors: nothing written' % len(errs)); return 1
    with open(OUT_FILE, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(doc, f, indent=1, ensure_ascii=False); f.write('\n')
    print('wrote %s: %s entries' % (os.path.relpath(OUT_FILE, ROOT), ', '.join('spot %s %d' % (s, len(L)) for s, L in doc['spots'].items())))
    if '--check' in argv:
        blocking = argv[argv.index('--blocking') + 1] if '--blocking' in argv else os.path.join(ROOT, 'assets', 'hamilton-blocking.json')
        probs = check(doc, tracks, only, blocking)
        for p in probs: print(p)
        print('check: %d problems' % sum(1 for p in probs if not p.startswith('note:')))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
