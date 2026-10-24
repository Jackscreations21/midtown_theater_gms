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
SEGMENT_1 = [
]
# ===== END SEGMENT 1 =====

# ===== SEGMENT 2 (1-07..1-11) =====
SEGMENT_2 = [
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
# FILM ROUND (2026-10-24; research/seg6.md "Film round"; the blocking is gen6.py's). Spot 2 (house left) takes the body
# on stage RIGHT, spot 3 (house right) stage LEFT, spot 1 the centre. His checklist rulings: 2-06 Eliza and Philip LIT;
# 2-07 each man's light on his own side, the switch to Hamilton at 1:17, NO blackout at the end (spot 3 carries
# Jefferson across into 2-08).
SEGMENT_6 = [
    # 2-06 Schuyler Defeated
    F(2, '2-06', 2.5, 'eliza', size='full', level=0.8, fade=1.5, note="his ruling (2-06 row): Eliza lit on the gallery; FILM 18-24 she reads the paper at the rail, SR of Philip"),
    F(3, '2-06', 2.6, 'laurens', size='full', level=0.8, fade=1.5, note="his ruling: Philip lit beside her, the paper in his hands (FILM 18-24)"),
    F(1, '2-06', 22.8, 'burr', size='full', level=0.85, fade=0.8, note='the new senator: Burr walks into the light (cue 938); FILM 31.9 he is SR of centre'),
    OUT(2, '2-06', 27.2, fade=1.5, note='Eliza goes by the passage (cue 939: the gallery out)'),
    OUT(3, '2-06', 27.0, fade=1.5, note='Philip goes'),
    F(3, '2-06', 30.8, 'hamilton', size='full', level=0.85, fade=0.6, note='Hamilton storms in from SL to Burr (FILM 31.9: SL of Burr)'),
    OUT(3, '2-06', 61.0, fade=1.5, note='FILM 62.2: he walks away SL into the dark'),
    OUT(1, '2-06', 62.6, fade=0.8, note='the button: Burr among the chairs'),
    # 2-07 Cabinet Battle #2
    F(1, '2-07', 4.3, 'washington', size='full', level=0.8, fade=0.8, note='FILM 4.8-13.6: Washington centre calls the cabinet, hands out the mics'),
    F(2, '2-07', 15.5, 'lafayette', size='full', level=0.9, fade=0.6, note="his ruling: Jefferson's light, stage RIGHT, for his verse; it follows him into Hamilton's face (FILM 34.6, 48.6)"),
    OUT(1, '2-07', 17.0, fade=1.5, note='Washington sits (FILM 53.8): the floor is Jefferson\'s'),
    F(1, '2-07', 66.5, 'washington', size='full', level=0.75, fade=0.8, note='FILM 68.8: Washington up, centre, hands over to Hamilton'),
    OUT(1, '2-07', 76.0, fade=1.0, note='back to his armchair'),
    OUT(2, '2-07', 77.0, fade=1.0, note="his ruling: the switch at 1:17 - Jefferson's light goes as Hamilton's comes"),
    F(3, '2-07', 77.0, 'hamilton', size='full', level=0.9, fade=0.6, note="his ruling: Hamilton's light, stage LEFT, on at 1:17 (77 s) for his answer"),
    F(1, '2-07', 93.9, 'washington', size='full', level=0.75, fade=0.6, note='FILM 93.7: Washington up beside the armchair, cutting in; then rules centre (101.5-111.6)'),
    OUT(1, '2-07', 110.6, fade=1.0, note='FILM 114.6: Washington goes SR with the room'),
    F(3, '2-07', 112.6, 'lafayette', size='full', level=0.85, move=1.0, note='FILM 114.6: the sides swap: Jefferson SL now, spot 3 swings to him'),
    F(2, '2-07', 112.6, 'hamilton', size='full', level=0.85, fade=0.6, note='FILM 114.6: Hamilton SR now; the face-off (114.6-139.6)'),
    F(1, '2-07', 139.4, 'washington', size='full', level=0.7, fade=0.4, note='FILM 139.6: Washington calls from the DSR corner'),
    OUT(2, '2-07', 140.8, fade=0.8, note='Hamilton goes off SR with him'),
    OUT(1, '2-07', 141.0, fade=0.8, note='Washington gone'),
    # 2-08 Washington on Your Side (spot 3 still on Jefferson from 2-07: no blackout between, his ruling)
    F(2, '2-08', 8.0, 'burr', size='full', level=0.85, fade=0.8, note='FILM 8.2: Burr walks on to him; Burr SR, Jefferson SL (FILM 15)'),
    F(3, '2-08', 66.5, 'burr', size='full', level=0.85, move=1.0, note='FILM 79: they have swapped, Burr SL now'),
    F(2, '2-08', 66.5, 'lafayette', size='full', level=0.9, move=1.0, note='Jefferson SR of centre (FILM 79)'),
    F(1, '2-08', 78.6, 'mulligan', size='full', level=0.85, fade=0.6, note="FILM 82: Madison in from SR for his verse"),
    F(1, '2-08', 87.0, 'lafayette', size='full', level=0.9, move=0.8, note='FILM 89-123: the row - spot 1 takes Jefferson in the centre'),
    F(2, '2-08', 87.0, 'mulligan', size='full', level=0.85, move=0.8, note='spot 2 takes Madison, SR'),
    F(2, '2-08', 155.0, 'burr', size='full', level=0.8, move=1.0, note='FILM 155-177: Burr ends far SR'),
    F(3, '2-08', 155.0, 'mulligan', size='full', level=0.8, move=1.0, note='FILM 177: Madison ends far SL'),
    F(2, '2-08', 180.6, 'washington', size='full', level=0.6, move=1.2, note="One Last Time's first picture (FILM 2-08 177 / 2-09 6.5): Washington at the desk"),
    F(3, '2-08', 180.6, 'hamilton', size='full', level=0.6, move=1.2, note='Hamilton upstage SL, reading (FILM 2-08 177)'),
    OUT(1, '2-08', 180.8, fade=1.0, note='Jefferson goes'),
    # 2-09 One Last Time: Washington SR of Hamilton all through (FILM)
    F(2, '2-09', 8.0, 'washington', size='full', level=0.8, fade=2.0, note='FILM 6.5-168: Washington at and in front of his desk'),
    F(3, '2-09', 8.0, 'hamilton', size='full', level=0.8, fade=2.0, note='FILM 6.5-168: Hamilton SL of him'),
    F(3, '2-09', 171.0, 'hamilton', size='full', level=0.95, fade=1.0, note='FILM 179: Hamilton alone DSC, reading the address'),
    F(2, '2-09', 171.0, 'washington', size='full', level=0.45, fade=1.0, note='Washington upstage of him, held low'),
    F(2, '2-09', 186.0, 'washington', size='full', level=0.9, fade=1.0, note='side by side (REVIEW 3; FILM 200-217): he takes over the reading'),
    F(3, '2-09', 186.0, 'hamilton', size='full', level=0.7, fade=1.0, note='beside him, on his left'),
    OUT(3, '2-09', 222.0, fade=2.0, note='FILM 224: Hamilton steps back; Washington alone'),
    F(3, '2-09', 249.0, 'hamilton', size=3.0, level=0.55, fade=2.0, note='FILM 239-262: the family together SR (one wide pool takes Eliza and Philip with him)'),
    F(1, '2-09', 266.0, 'washington', size='full', level=1.0, fade=1.5, note='FILM: Washington DSC in a hard white spot for the end, arms open'),
    OUT(2, '2-09', 266.5, fade=1.5, note='spot 1 has him'),
    OUT(3, '2-09', 288.0, fade=3.0, note='the family fades as the note holds'),
    F(3, '2-09', 294.6, 'king', size='full', level=0.6, fade=1.0, note='FILM: the King in from SL, watching Washington go'),
    # 2-10 I Know Him
    OUT(1, '2-10', 3.2, fade=1.5, note='FILM 1.6: Washington walks slowly upstage and off'),
    F(1, '2-10', 4.5, 'king', size='full', level=0.9, fade=1.0, note='the King alone: UC (FILM 5.2), down to DC (24), the silence, the band, the laugh'),
    OUT(3, '2-10', 5.5, fade=1.0, note='spot 1 has him'),
    F(2, '2-10', 33.3, 'ens1', size='half', level=0.6, fade=0.5, note="FILM 33.1-47.1: the Bullet at his SR shoulder, the whisper and the giggle"),
    OUT(2, '2-10', 47.0, fade=0.5, note='she goes'),
    OUT(1, '2-10', 95.6, fade=0.0, note='the blackout: he stands in it (seg 7 picks him up at 2-11 0.0)'),
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
        whos = [w for _, w in L]
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
