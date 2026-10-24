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
