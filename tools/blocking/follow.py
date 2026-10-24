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
SEGMENT_6 = [
]
# ===== END SEGMENT 6 =====

# ===== SEGMENT 7 (2-11..2-16) =====
SEGMENT_7 = [
]
# ===== END SEGMENT 7 =====

# ===== SEGMENT 8 (2-17..2-23) =====
# Read from the Disney+ clips for 2-17..2-21 (research/seg8.md "Film round"); 2-22 and 2-23 have no clip, so the spot is on
# whoever leads the moment. Spot 2 (house left) takes stage RIGHT, spot 3 (house right) stage LEFT, spot 1 the centre.
SEGMENT_8 = [
    # 2-17 Stay Alive (Reprise): a dark blue stage, the family warm at the table (the clip, 33-106)
    F(2, '2-17', 12.5, 'hamilton', level=0.6, note='film 2-17 14: he runs in to Philip up SR, and is with the Doctor SR to 30'),
    F(1, '2-17', 14.0, 'laurens', level=0.6, note='Philip on the table as the platform carries it round to the front (film 24.9, 33.4)'),
    F(2, '2-17', 33.0, 'hamilton', level=0.75, note='film 33.4: at the table, bent over his son'),
    F(3, '2-17', 61.5, 'eliza', level=0.75, note='film 62: Eliza in from up SR, to the table on his SR side'),
    OUT(1, '2-17', 109.6, fade=0, note='the blackout on the scream'),
    OUT(2, '2-17', 109.6, fade=0, note='the blackout'),
    OUT(3, '2-17', 109.6, fade=0, note='the blackout'),
    # 2-18 It's Quiet Uptown
    F(3, '2-18', 8.6, 'angelica', level=0.7, note='film 2-18 6.6-33.6: Angelica narrates SL, mid-stage'),
    F(1, '2-18', 31.0, 'hamilton', level=0.7, note='film 33.6, 47: alone at the centre among the circling couples'),
    OUT(3, '2-18', 52.0, fade=2.0, note='her narration done; she watches up SL in the dark'),
    F(1, '2-18', 89.35, 'hamilton', level=1.0, fade=1.5, note='film 94: the pull-in - he is the only bright thing, alone at centre'),
    F(1, '2-18', 100.0, 'hamilton', level=0.8, fade=2.0, note='down to his plea'),
    F(3, '2-18', 104.72, 'eliza', level=0.75, note='film 103-147: Eliza SL of him, still as stone'),
    F(2, '2-18', 166.0, 'angelica', level=0.7, note="Angelica's second solo DSR"),
    OUT(2, '2-18', 250.0, fade=2.0, note='Angelica goes'),
    OUT(1, '2-18', 262.0, fade=2.0, note='they leave together arm in arm (film 246: the couple at the centre till the end)'),
    OUT(3, '2-18', 262.0, fade=2.0, note='with him'),
    # 2-19 The Election of 1800
    F(3, '2-19', 5.0, 'lafayette', level=0.8, note='film 2-19 5: Jefferson walks on DSR; he crosses SL of Madison by 21'),
    F(2, '2-19', 6.8, 'mulligan', level=0.75, note='film 5-28: Madison in at the centre, then SR at the front'),
    F(1, '2-19', 19.5, 'burr', level=0.8, note='Burr up SL, then working the room (film 63.5-77) - never still'),
    F(3, '2-19', 79.0, 'lafayette', level=0.5, fade=1.5, note='the townspeople take the floor; J & M aside SL'),
    F(2, '2-19', 79.6, 'mulligan', level=0.5, fade=1.5, note='aside SL'),
    F(2, '2-19', 99.25, 'hamilton', level=0.9, move=1.2, note='film 104: Hamilton at the centre between the lines of letters'),
    OUT(3, '2-19', 121.0, fade=1.5, note='film 124-148: the two men alone'),
    OUT(2, '2-19', 134.5, fade=1.0, note='Hamilton goes up the middle to the gallery'),
    F(2, '2-19', 152.4, 'hamilton', level=1.0, note='film 152-184: the endorsement from the centre of the gallery'),
    F(3, '2-19', 152.4, 'lafayette', level=0.7, note='film 152: Jefferson SL as all eyes go up to Hamilton'),
    F(3, '2-19', 187.73, 'lafayette', level=1.0, fade=1.0, note='Jefferson wins (film 200: at centre, the company pointing)'),
    OUT(2, '2-19', 188.5, fade=1.0, note='Hamilton off the gallery'),
    OUT(3, '2-19', 229.5, fade=1.0, note='Jefferson goes'),
    OUT(1, '2-19', 236.5, fade=1.0, note='Burr alone as the band stops, then dark'),
    # 2-20 Your Obedient Servant
    F(1, '2-20', 0.2, 'burr', level=0.85, note='film 2-20 10-31: tight on Burr, in his steel shaft and at the desk'),
    F(2, '2-20', 70.0, 'hamilton', level=0.8, note='film 88-93: Hamilton at the desk, Burr SR; 129-147 Hamilton in the DSR pool'),
    OUT(1, '2-20', 147.68, fade=0, note='blackout (cue 1206)'),
    OUT(2, '2-20', 147.68, fade=0, note='blackout'),
    # 2-21 Best of Wives and Best of Women
    F(2, '2-21', 0.44, 'hamilton', size='half', level=0.6, note='film 2-21 8.4: writing at his desk, pre-dawn'),
    F(3, '2-21', 7.72, 'eliza', level=0.6, note='film 8.4: Eliza in SR, watching him; 21 behind him; 38 at his side'),
    F(2, '2-21', 16.5, 'hamilton', size='full', level=0.6, fade=1.5, note='opens out to take the two of them (film 21: her arms round him)'),
    OUT(2, '2-21', 44.0, fade=0, note='the snap FTB (cue 1238)'),
    OUT(3, '2-21', 44.0, fade=0, note='the snap FTB'),
    # 2-22 The World Was Wide Enough (no clip)
    F(2, '2-22', 3.6, 'hamilton', level=0.75, note='no clip: he rises from the chair SR and walks the ground'),
    F(3, '2-22', 9.84, 'burr', level=0.8, note='no clip: Burr narrates SL'),
    F(1, '2-22', 101.42, 'ens1', size='half', level=0.6, note='FIRE: the Bullet takes the shot at his pistol and creeps toward him'),
    F(3, '2-22', 103.42, 'burr', level=0.45, fade=1.5, note='Burr frozen in his aim through the monologue'),
    F(2, '2-22', 103.42, 'hamilton', level=1.0, fade=1.0, note="Hamilton's monologue: the one bright figure"),
    OUT(1, '2-22', 155.0, fade=1.0, note='the Bullet into the knot at the centre'),
    F(1, '2-22', 160.0, 'washington', level=0.7, note='Washington beside him, then up the SL stair'),
    F(1, '2-22', 174.5, 'eliza', level=0.8, move=1.0, note='ELIZA: she takes his hand and pulls him to centre'),
    OUT(1, '2-22', 181.0, fade=1.0, note='she goes up SR'),
    F(3, '2-22', 191.18, 'burr', level=0.8, fade=0.3, note='the shot'),
    F(1, '2-22', 226.0, 'eliza', level=0.6, note='the sisters either side of him as he rises'),
    OUT(2, '2-22', 247.5, fade=1.5, note='Hamilton off along the bridge'),
    OUT(1, '2-22', 251.5, fade=1.5, note='Eliza goes'),
    F(3, '2-22', 239.22, 'burr', level=1.0, fade=1.5, note="Burr's reckoning DSC, then alone"),
    OUT(3, '2-22', 292.8, fade=3.0, note='FTB'),
    # 2-23 Who Lives, Who Dies, Who Tells Your Story (no clip)
    F(1, '2-23', 0.44, 'washington', level=0.8, note='no clip: Washington opens at centre'),
    OUT(1, '2-23', 15.0, fade=1.0, note='back into the company'),
    F(2, '2-23', 16.76, 'lafayette', level=0.7, note='Jefferson at the top of the SR stair'),
    OUT(2, '2-23', 30.0, fade=1.0),
    F(3, '2-23', 30.01, 'mulligan', level=0.7, note='Madison DSL'),
    F(3, '2-23', 43.27, 'burr', level=0.7, note='Burr DS'),
    OUT(3, '2-23', 50.0, fade=1.0, note='the company comes down into its lines'),
    F(1, '2-23', 58.3, 'eliza', level=0.9, note='Eliza enters; she carries the number to the gasp'),
    F(2, '2-23', 88.92, 'angelica', level=0.7, note='Angelica beside her'),
    OUT(2, '2-23', 103.0, fade=1.5, note='Angelica back into the company'),
    F(3, '2-23', 114.59, 'washington', level=0.6, note="Washington behind her at the monument"),
    OUT(3, '2-23', 124.5, fade=1.5),
    F(2, '2-23', 153.42, 'hamilton', level=0.8, note='the company spreads: Hamilton revealed'),
    OUT(1, '2-23', 211.8, fade=0, note='the blackout after the gasp'),
    OUT(2, '2-23', 211.8, fade=0, note='the blackout'),
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
