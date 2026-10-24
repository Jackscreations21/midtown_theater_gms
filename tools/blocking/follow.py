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
# The film round (2026-10-24; tools/blocking/research/seg5.md "Film round"). Bodies: Jefferson 'lafayette', Madison 'mulligan',
# Philip 'laurens', Maria 'peggy', James Reynolds 'ens4'. Spot 1 centre, 2 house left (stage RIGHT), 3 house right (stage LEFT).
SEGMENT_5 = [
    # 2-01 What'd I Miss
    F(1, '2-01', 3.4, 'burr', level=0.8, note='Burr\'s recap DC (film 8-24: he alone carries it, the town dim behind him)'),
    F(3, '2-01', 17.5, 'hamilton', size=3.0, level=0.7, note='Hamilton and Washington on the SL end of the gallery in the recap (film 18-24: lit up there); one wide pool on the two'),
    OUT(3, '2-01', 26.8, note='they go in through the gallery door'),
    OUT(1, '2-01', 38.2, fade=0.8, note='Burr at the top of the stair, going (film 40)'),
    F(1, '2-01', 44.0, 'lafayette', level=1.0, note='Jefferson appears up top (film 44-57: the hard white pool on him alone; NOTES3 balcony at 0:44); the spot stays on him the whole number'),
    F(2, '2-01', 154.0, 'mulligan', level=0.85, note='Madison on DR (film 152), followed through his verse and the welcome'),
    F(3, '2-01', 208.6, 'hamilton', size=3.0, level=0.85, note='Hamilton named, DL with Washington (film 212: the pair SL); one wide pool on the two'),
    OUT(1, '2-01', 234.2, fade=0, note='the snap to the cabinet (cue 739.5)'),
    OUT(2, '2-01', 234.2, fade=0, note='the snap'),
    OUT(3, '2-01', 234.2, fade=0, note='the snap'),
    # 2-02 Cabinet Battle #1 (no clip; Cabinet Battle #2's film 45: the rapper in a hard pool, the other lit at his side)
    F(1, '2-02', 0.6, 'washington', level=0.9, note='Washington the MC at the DSC mic'),
    OUT(1, '2-02', 9.4, note='he goes up to his chair'),
    F(2, '2-02', 13.0, 'lafayette', level=0.9, note='Jefferson\'s verse SR (his spot, NOTES3), held on him through the battle'),
    F(3, '2-02', 44.8, 'hamilton', level=0.9, note='Hamilton\'s interjection, then held on him through his verse and to the end'),
    F(1, '2-02', 78.6, 'washington', level=0.8, note='Washington up to hand over'),
    OUT(1, '2-02', 84.0, note='back to his chair'),
    F(1, '2-02', 146.6, 'washington', level=0.85, note='Washington stops it, and takes Hamilton aside (the reprimand)'),
    OUT(2, '2-02', 167.5, note='Jefferson goes off DSR'),
    OUT(1, '2-02', 210.6, note='Washington goes off upstage'),
    OUT(3, '2-02', 214.0, fade=1.0, note='Hamilton alone in the button, into the dark'),
    # 2-03 Take a Break
    F(3, '2-03', 1.0, 'eliza', size=2.8, level=0.7, note='Eliza and Philip at the piano SL (film 10-30); one pool on the two'),
    F(1, '2-03', 29.0, 'angelica', level=0.8, note='Angelica\'s letter from the gallery (film 30, 50)'),
    OUT(1, '2-03', 58.4, note='she fades back'),
    F(3, '2-03', 76.0, 'laurens', level=0.9, note='Philip\'s poem beside the piano SL (film 76-100; no longer in the DSC special, so the spot carries him)'),
    OUT(3, '2-03', 101.5, note='he goes back to the piano'),
    F(1, '2-03', 104.5, 'eliza', size=2.8, level=0.8, note='the duet DC, Eliza and Hamilton hand in hand (film 106-126); one pool on the two'),
    OUT(1, '2-03', 127.5, note='he goes back to the desk'),
    F(2, '2-03', 131.6, 'angelica', level=0.9, note='Angelica on the SR stair top (film 132-180: lit there), down it and to the family; her gallery key cannot reach her there'),
    F(1, '2-03', 184.5, 'eliza', level=0.85, note='Eliza runs to her sister (film 189) and through the trio'),
    F(3, '2-03', 182.5, 'hamilton', level=0.85, note='Hamilton SL of them, staying behind (film 189-245)'),
    OUT(1, '2-03', 265.8, note='the family goes'),
    OUT(2, '2-03', 266.4, note='the family goes'),
    OUT(3, '2-03', 279.0, fade=2.0, note='Hamilton alone at the desk into the dark'),
    # 2-04 Say No to This
    F(2, '2-04', 0.8, 'burr', level=0.8, note='Burr tells it SR (cue 780.01)'),
    F(3, '2-04', 16.0, 'peggy', level=0.75, gel='R02', note='Maria at her door SL (film 10: lit in the street); a warm frame, the red dress'),
    F(1, '2-04', 20.6, 'hamilton', level=0.85, note='Hamilton, the whole number (film 61-233: the pool goes with him)'),
    OUT(2, '2-04', 22.5, note='Burr goes up to watch from the back, in the dark'),
    F(2, '2-04', 131.0, 'ens4', level=0.8, note='James Reynolds DR with his letter (film 133-155)'),
    OUT(2, '2-04', 153.6, note='James goes off DSR'),
    F(2, '2-04', 232.4, 'ens4', level=0.7, note='James back SR for the money (film 233)'),
    OUT(3, '2-04', 234.0, note='Maria goes'),
    OUT(2, '2-04', 234.4, note='James goes'),
    OUT(1, '2-04', 236.0, fade=0.8, note='the fade to black (cue 834)'),
    # 2-05 The Room Where It Happens
    F(1, '2-05', 5.6, 'burr', level=0.8, note='Burr, the narrator, the whole number (film: he carries it in a pool of his own)'),
    F(3, '2-05', 5.0, 'hamilton', level=0.75, note='Hamilton with Burr SL (film 10-40), then at the table and back'),
    F(2, '2-05', 97.6, 'lafayette', level=0.85, note='Jefferson\'s account DSL and his approach to Madison (film 100-117)'),
    OUT(2, '2-05', 118.2, note='the three into the room: the table special has them'),
    F(2, '2-05', 142.4, 'mulligan', level=0.85, note='Madison weighs it DSR (film 145) and the deal with Jefferson (film 165)'),
    OUT(2, '2-05', 175.4, note='the third entry'),
    OUT(3, '2-05', 271.2, note='Hamilton leaves with his chair (882)'),
    OUT(1, '2-05', 314.5, fade=0.3, note='the last click-boom: the button special has him (892/894)'),
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
