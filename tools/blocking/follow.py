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
    # 1-18 Guns and Ships
    F(3, '1-18', 0.5, 'burr', level=0.8, fade=1.0, note='film 1-18 5.0-30.0: Burr alone, lit head to toe on the SL balcony for the opening, the deck dark; spot 3 (house right) is on his side'),
    F(1, '1-18', 31.4, 'lafayette', level=0.9, fade=0.3, note='film 32.1-36.0: the huddle opens and Lafayette is up on the table, a hard white circle on him'),
    OUT(3, '1-18', 41.0, note='film 38.6: Burr still up there as Lafayette lands; he loses his light as the company takes the deck'),
    F(2, '1-18', 50.0, 'washington', level=0.8, note='film 50.5-60.6: Washington comes down to Lafayette SR of the table; spot 2 (house left) on his side, then on him at his table to the button'),
    OUT(1, '1-18', 81.5, note='Lafayette runs the letter to the SL stair and goes'),
    F(3, '1-18', 90.4, 'hamilton', level=0.8, note='film 90.8-97.0: the letter reaches Hamilton on the gallery; the spot takes him down the SL stair to Eliza, the coat, and down to his DS special for the button'),
    OUT(2, '1-18', 126.0, note='the button out; History picks them up on their new sides'),
    OUT(3, '1-18', 126.0, note='the button out'),
    # 1-19 History Has Its Eyes on You
    F(3, '1-19', 1.0, 'washington', level=0.8, fade=1.0, note='film 1-19 0.9-73.4: Washington SL of the table, his song; the whole turntable is warm, the spot keeps him the brightest thing on it'),
    F(2, '1-19', 1.0, 'hamilton', level=0.6, fade=1.0, note='film: Hamilton apart SR, listening, then taking the sword (47-50)'),
    OUT(3, '1-19', 95.0, note='Washington goes in the count-in to Yorktown'),
    OUT(2, '1-19', 96.0, fade=0.5, note='spot 1 takes Hamilton to the lip for Yorktown'),
    # 1-20 Yorktown
    F(1, '1-20', 0.5, 'hamilton', level=0.9, note='film 1-20 11.9-61.9: Hamilton carries the number from the lip, the centre pool and the box; spot 1 (centre)'),
    F(3, '1-20', 10.0, 'lafayette', level=0.8, note='film 11.9-31.9: Lafayette face to face with him, SL of him'),
    OUT(3, '1-20', 32.0, note='Lafayette goes DL (Jack\'s note: off at 32)'),
    F(1, '1-20', 72.5, 'hamilton', size='full', level=0.5, fade=1.0, note='the night attack (cue 595): the stage is small pools in the dark; the spot drops to a glow on the narrator'),
    F(3, '1-20', 93.0, 'laurens', level=0.6, note='the friends\' fortunes: Laurens in his pool SL (the Bullet shakes his hand)'),
    OUT(3, '1-20', 99.0),
    F(2, '1-20', 100.1, 'lafayette', level=0.6, note='the friends\' fortunes: Lafayette at the bay DR'),
    OUT(2, '1-20', 109.0),
    F(3, '1-20', 110.0, 'mulligan', level=0.9, fade=0.3, note='film 111.9-129.9: Mulligan bursts in and has the verse, centre front'),
    OUT(3, '1-20', 130.0, note='the drill: the whole stage is up'),
    F(1, '1-20', 129.9, 'hamilton', level=0.8, fade=0.5, note='the drill and the battle: Hamilton leads it'),
    F(3, '1-20', 135.8, 'lafayette', level=0.7, note='the battle: Lafayette leads the SL wing of the charge'),
    OUT(3, '1-20', 151.0),
    F(1, '1-20', 155.5, 'hamilton', level=0.6, fade=1.0, note='"after a week": Hamilton narrates in the centre pool'),
    F(3, '1-20', 179.8, 'washington', level=0.7, note='Washington comes through the door for the terms'),
    OUT(3, '1-20', 190.0, note='he goes upstage to watch'),
    F(1, '1-20', 217.1, 'hamilton', level=1.0, fade=1.0, note='film 217.0-237.1: the tableau, Hamilton up on his box at the centre of it'),
    OUT(1, '1-20', 240.3, fade=0, note='the blackout'),
    # 1-21 What Comes Next?
    F(1, '1-21', 1.0, 'king', level=0.9, fade=0.3, note='film 1-21 1.1-96.1: the King alone at the lip, a hard white circle on him'),
    OUT(1, '1-21', 97.0, note='he goes upstage through the deck door'),
    # 1-22 Dear Theodosia
    F(2, '1-22', 4.5, 'burr', level=0.8, fade=1.5, note='film 1-22 5.0, 80.0, 159.9: two hard bright circles, Burr seated SR (spot 2, house left)'),
    F(3, '1-22', 4.5, 'hamilton', level=0.8, fade=1.5, note='film 80.0, 159.9: Hamilton SL (spot 3, house right)'),
    F(1, '1-22', 158.0, 'eliza', level=0.5, fade=1.0, note='film 159.9: Eliza in, between and behind them'),
    OUT(1, '1-22', 176.5, fade=1.5),
    OUT(2, '1-22', 176.9, fade=1.5, note='the fade'),
    OUT(3, '1-22', 176.9, fade=1.5, note='the fade'),
    # 1-23 Non-Stop
    F(3, '1-23', 0.5, 'hamilton', level=0.7, fade=1.0, note='the trial: Hamilton at the defence table SL (film 29.9-37.9)'),
    F(2, '1-23', 0.5, 'burr', level=0.7, fade=1.0, note='the trial: Burr SR of him (film 20.0, 37.9)'),
    F(3, '1-23', 68.0, 'hamilton', level=1.0, fade=0.3, note='film 70.1-82.1: the brag, standing on the table: full up'),
    F(3, '1-23', 84.0, 'hamilton', level=0.7, fade=1.0, note='down off it; the Convention, midnight at Burr\'s'),
    OUT(3, '1-23', 186.5, note='Hamilton goes into the dark'),
    OUT(2, '1-23', 205.0, note='Burr\'s reprise ends; he goes'),
    F(1, '1-23', 209.5, 'hamilton', level=0.8, note='film 209.9-244.0: Hamilton between the sisters, then at his desk, Washington\'s offer, and the finale'),
    F(2, '1-23', 209.5, 'angelica', level=0.7, note='film 209.9, 236.0: Angelica SR'),
    F(3, '1-23', 228.0, 'eliza', level=0.7, note='film 236.0, 244.0: Eliza SL, riding the turntable in to him'),
    OUT(2, '1-23', 244.5, note='Angelica goes'),
    OUT(3, '1-23', 248.5, note='Eliza goes'),
    F(2, '1-23', 258.0, 'burr', level=0.6, note='Burr counts the essays DR'),
    F(3, '1-23', 301.0, 'washington', level=0.8, note='the music drops: Washington\'s offer'),
    F(2, '1-23', 327.1, 'eliza', level=0.7, move=1.0, note='the finale: Eliza in her SR pools and special'),
    F(3, '1-23', 327.1, 'angelica', level=0.7, move=1.2, note='the finale: Angelica SL (Washington is up on the SL gallery in his own light)'),
    OUT(1, '1-23', 382.2, fade=0, note='the blackout: the end of act one'),
    OUT(2, '1-23', 382.2, fade=0, note='the blackout'),
    OUT(3, '1-23', 382.2, fade=0, note='the blackout'),
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
