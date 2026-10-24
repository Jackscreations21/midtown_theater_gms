#!/usr/bin/env python3
"""The spotlight audit: every light meant for one person, through the whole show, against where the actors stand now.

    python -I tools/spot-audit.py --dump <DUMP DIR> [--out docs/hamilton-spot-audit.md] [--json FILE] [--dry | --fix] [--tracks 1-01,2-07]

<DUMP DIR>/<track>.json is the page's pool dump, made by tools/pool-dump.js in midtown.html (served by tools/pool-dump-serve.py):
per cue `q`, `at`, `until`, and per lit unit `ch`, `type`, `level`, `zoom`, `from`, `hit`, `hitR`, `lands`, `kind`.
assets/hamilton-pools.json is a slimmed copy of such a dump and cannot be audited: it has lost `lands`, `type` and `from`, so a
beam stopped by a wall reads as a pool on the deck behind it.

A PERSON LIGHT (the plotter's definition, RULING FP): a `special` (zoom <= 14, or a floor pool of radius <= 1 m) or any unit at
zoom <= 18.5, landing on a FLOOR (the deck, a gallery, a stair) at level >= 0.15. Beams that stop on a wall, the house or nothing
are not person lights here.

For every cue (hold >= 0.4 s) every actor is posed with tools/blocking-plot.py's pose() at 25 %, 60 % and 95 % of the hold. A person
is IN a light when within its radius + 0.3 m at her own floor height (the beam's axis followed down to it: a body on a gallery,
a stair or a piece is lit by a beam that passes there on its way to the deck; nobody below where the beam stopped), on stage
(|x| <= 7, z <= 5.3), at two of the three moments.

THE MISSES
  named:   the cue's label names a person (Burr, Ham, Eliza, GW / Washington, Lee, Laf, Jefferson, ...) who is on stage and in
           none of its person lights - unless the cue takes someone away (exits, goes, out, blackout). The head labels count:
           the Lafayette body is Jefferson in act two, ens3 is Charles Lee.
  nobody:  a `special` lit at >= 0.15 with nobody in it at any of the three moments.

THE FIXES (--dry plans them into the report; --fix writes assets/hamilton-show.json in its own style). Real cues are never edited:
a reconstructed FOLLOWER at the same moment, numbered in the gap after the real cue, carries the change.
  re-aim:  a MOVER (mac-viper, glp-x4, vl3500) lit in the cue on nobody, nearest the named person, gets `focus` = where she spends
           the hold: the midpoint of the two closest of her three sampled places, on her floor (deck 0.05, gallery 2.74). Vipers
           and X4s are tried first, VL3500s (the beam fans and back washes) last. A special on nobody is re-aimed onto a principal
           (or a named role) within 1.5 m who is in no person light (the choreography moved her off it); three or more empty
           specials of one family in a cue are a fan or a pattern and are left. Focus snaps (time 0) if the unit was dark in the
           cue before.
  swap:    (reconstructed cues only) a named person with no mover to spare gets a FREE Viper (dark in this cue and the one before),
           the one hung most nearly over her, at 70 % and zoom 13 for the cue, out in the next; its colour and gobo track.
  restore: a re-aimed or swapped unit that would carry its new focus into a later cue gets its old landing back as `focus` (and
           its old zoom) - in the first later cue where it is dark (a move in the dark), else the next cue that lights it - so
           nothing downstream moves. The dump says exactly where it landed before; that point is the focus.
  left:    a fixed unit (its focus cannot move), a wash that only looks narrow, or a special with nobody near: reported only.

Re-dump after --fix and run again: that report is the AFTER count, and a fix whose beam stopped on the way (a rail, the house
ceiling in front of the apron) shows again. Check every step with tools/pool-dump-diff.py against the dump before it: a moved
unit in a cue the tool did not write is a carry it missed. Standard library only.
"""
import importlib.util, json, math, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOW = os.path.join(ROOT, 'assets', 'hamilton-show.json')
MOVERS = {'mac-viper', 'glp-x4', 'vl3500'}
MIN_LV, SLACK, DY, NEAR = 0.15, 0.3, 0.6, 1.5
MARK = 'spot-audit 2026-10-15'

_spec = importlib.util.spec_from_file_location('blocking_plot', os.path.join(ROOT, 'tools', 'blocking-plot.py'))
BP = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(BP)

# label words -> a head label (or an actor id) they name
NAMES = [(r'\b(ham|hamilton|ah|alexander)\b', 'Hamilton'), (r'\bburr\b', 'Burr'), (r'\beliza\b', 'Eliza'), (r'\b(angelica|ang)\b', 'Angelica'),
         (r'\bpeggy\b', 'Peggy'), (r'\bmaria\b', 'Maria Reynolds'), (r'\bjames\b', 'James Reynolds'), (r'\b(gw|washington)\b', 'Washington'),
         (r'\b(laf|lafayette)\b', 'Lafayette'), (r'\b(mulligan|herc)\b', 'Mulligan'), (r'\blaurens\b', 'Laurens'), (r'\bjefferson\b', 'Jefferson'),
         (r'\bmadison\b', 'Madison'), (r'\bking\b', 'King George'), (r'\bphilip\b', 'Philip'), (r'\blee\b', 'Charles Lee'),
         (r'\bseabury\b', 'Samuel Seabury'), (r'\beacker\b', 'George Eacker'), (r'\bschuyler\b', 'Philip Schuyler'), (r'\bmartha\b', 'Martha'),
         (r'\bdolly\b', 'Dolly'), (r'\bdoctor\b', 'The Doctor'), (r'\bbullet\b', 'The Bullet')]


EXITS = re.compile(r'\b(exit|exits|goes|gone|leaves|blackout|out)\b', re.I)   # a cue that takes someone away: an empty light is the point


def named_in(label):
    s = (label or '').lower()
    out = []
    for rx, who in NAMES:
        if re.search(rx, s):
            if who == 'Philip' and 'schuyler' in s: continue
            if who == 'Washington' and 'george' in s and 'king' in s: continue
            out.append(who)
    return out


def floor_y(y):
    return 2.74 if abs(y - 2.743) < 0.3 else (0.05 if y < 0.3 else round(y, 2))


def load_show():
    raw = open(SHOW, encoding='utf-8', newline='').read()
    lines = raw.split('\n'); i0 = lines.index('"cues": [')
    j = len(lines) - 1
    while not lines[j].startswith('{"q":'): j -= 1
    return lines[:i0 + 1], [json.loads(l.rstrip(',')) for l in lines[i0 + 1:j + 1]], lines[j + 1:]


def save_show(head, cues, tail):
    body = [json.dumps(c, ensure_ascii=False, separators=(',', ':')) + (',' if k + 1 < len(cues) else '') for k, c in enumerate(cues)]
    tmp = SHOW + '.tmp'
    with open(tmp, 'w', encoding='utf-8', newline='') as f: f.write('\n'.join(head + body + tail))
    os.replace(tmp, SHOW)


def person_lights(cue):
    out = []
    for p in cue['pools']:
        if p['level'] < MIN_LV: continue
        if not (p['kind'] == 'special' or (p['kind'] in ('wash', 'special') and p['zoom'] <= 18.5)): continue
        lands = p.get('lands', '')
        if not (p.get('hit') and (lands in ('deck', 'gallery') or lands.startswith('floor'))): continue
        out.append(p)
    return out


def followspots(tracks):
    """-> on(T): the actor ids a followspot is on at show time T (assets/hamilton-follow.json, tools/blocking/follow.py). A body in
    a followspot is lit, whatever the cue's own units do, so she is not a `named` miss; the spot's fade in and out is ignored."""
    try: spots = json.load(open(os.path.join(ROOT, 'assets', 'hamilton-follow.json'), encoding='utf-8'))['spots']
    except OSError: return lambda T: set()
    L = [sorted(((tracks[e['track']]['start'] + e['at'], e) for e in es if e['track'] in tracks), key=lambda te: te[0]) for es in spots.values()]
    def on(T):
        out = set()
        for es in L:
            cur = None
            for t, e in es:
                if t > T: break
                cur = e
            if cur and not cur.get('out'): out.add(cur['who'])
        return out
    return on


def audit(dump_dir, tracks_only=None):
    d, tracks, actors = BP.load_inputs(os.path.join(ROOT, 'assets', 'hamilton-blocking.json'))
    order = sorted(tracks, key=lambda t: tracks[t]['i'])
    eos = {c['q']: c for c in json.load(open(os.path.join(ROOT, 'assets', 'hamilton-eos.json'), encoding='utf-8'))['cues']}
    _, show, _ = load_show()
    showq = {(c['track'], c['q']): c for c in show}
    follow_on = followspots(tracks)
    seq, rows = [], []                                   # seq: every cue in show order with its dump; rows: the misses
    for tid in order:
        f = os.path.join(dump_dir, tid + '.json')
        if not os.path.exists(f): continue
        for c in json.load(open(f, encoding='utf-8'))['cues']:
            sc = showq.get((tid, c['q']), {})
            label = sc.get('label') or (eos.get(c['q'], {}).get('label') if sc.get('real') else None) or c.get('label') or ''
            seq.append(dict(track=tid, q=c['q'], at=c['at'], until=c['until'], real=bool(sc.get('real')), label=label, cue=c,
                            lit={p['ch']: p for p in c['pools']}))
    for k, s in enumerate(seq):
        tid = s['track']
        if tracks_only and tid not in tracks_only: continue
        hold = s['until'] - s['at']
        s['pl'] = person_lights(s['cue'])
        s['inn'] = {}
        if hold < 0.4: continue
        T0 = tracks[tid]['start']
        samples = [s['at'] + hold * f for f in (0.25, 0.6, 0.95)]
        poses = []
        for sec in samples:
            P = {}
            for a in actors:
                p = BP.pose(a['c'], T0 + sec)
                if p and p['visible'] and abs(p['x']) <= 7.0 and p['z'] <= 5.3: P[a['id']] = p
            poses.append(P)
        s['poses'] = poses
        def who_in(L, need=2):
            """who the beam lights: its axis followed to each person's own floor height (a body on a gallery, a stair or a piece
            is lit by a beam that passes there on its way down); nobody below the point where it stopped."""
            (x, y, z), r, o = L['hit'], L['hitR'], L.get('from')
            cnt = {}
            for P in poses:
                for aid, p in P.items():
                    if abs(p['y'] - y) <= DY: cx, cz, cr = x, z, r
                    elif o and p['y'] > y and o[1] > p['y']:
                        t = (o[1] - p['y']) / (o[1] - y)
                        cx, cz, cr = o[0] + t * (x - o[0]), o[2] + t * (z - o[2]), r * t
                    else: continue
                    if math.hypot(p['x'] - cx, p['z'] - cz) <= cr + SLACK: cnt[aid] = cnt.get(aid, 0) + 1
            return sorted(a for a, n in cnt.items() if n >= need), sorted(cnt)
        lit_people = {aid for aid in {a for P in poses for a in P}             # FOLLOWSPOTS (2026-10-24): on her at two of the three moments
                      if sum(1 for sec in samples if aid in follow_on(T0 + sec)) >= 2}
        for p in s['pl']:
            inn, anyin = who_in(p)
            s['inn'][p['ch']] = (inn, anyin)
            lit_people |= set(inn)
        label_of = {aid: (p.get('label') or aid) for aid, p in poses[0].items()}
        names = named_in(s['label'])
        exiting = bool(EXITS.search(s['label'] or ''))
        for who in ([] if exiting else names):
            ids = [aid for aid, lab in label_of.items() if lab.lower() == who.lower() or (who == 'Charles Lee' and lab == 'Charles Lee')]
            if not ids:
                ids = [aid for aid, lab in label_of.items() if who.lower() in lab.lower()]
            for aid in ids:
                if aid in lit_people: continue
                if sum(1 for P in poses if aid in P) < 2: continue
                rows.append(dict(kind='named', k=k, track=tid, q=s['q'], at=s['at'], ch='', label=s['label'], expected=label_of[aid],
                                 aid=aid, inn='-', real=s['real']))
        for p in s['pl']:
            if p['kind'] != 'special': continue
            inn, anyin = s['inn'][p['ch']]
            if anyin: continue
            rows.append(dict(kind='nobody', k=k, track=tid, q=s['q'], at=s['at'], ch=p['ch'], label=s['label'],
                             expected=', '.join(names) or '-', aid=None, inn='NOBODY', real=s['real'], type=p['type'], zoom=p['zoom'],
                             hit=p['hit'], r=p['hitR']))
    return seq, rows, tracks, actors


# ---------------------------------------------------------------------------------------------------------------- the fixes
def qnum_between(a, b, taken):
    lo, hi = float(a), float(b) if b is not None else float(a) + 1
    for dec in (1, 2, 3, 4):
        step = 10 ** -dec
        x = math.floor(lo / step + 1e-9) * step + step
        while x < hi - 1e-9:
            s = f'{x:.{dec}f}'.rstrip('0').rstrip('.')
            if s not in taken and float(s) > lo: return s
            x += step
    raise ValueError(f'no number between {a} and {b}')


def plan_fixes(seq, rows, tracks):
    """-> {seq index: {ch: params}}, the log of actions (row -> action)."""
    writes = {}
    used = {}                                             # k -> set of channels already taken in that cue
    lens = {}
    for s in seq:
        for ch, p in s['lit'].items():
            if 'from' in p: lens.setdefault(ch, p['from'])
    rig = json.load(open(os.path.join(ROOT, 'assets', 'hamilton-rig.json'), encoding='utf-8'))['units']
    vipers = {str(u['channels'][0]): u for u in rig if u['type'] == 'mac-viper' and u.get('hung')}
    def W(k, ch, **kw):
        writes.setdefault(k, {}).setdefault(str(ch), {}).update(kw); used.setdefault(k, set()).add(str(ch))
    def dark_before(k, ch):
        return k > 0 and seq[k - 1]['track'] == seq[k]['track'] and ch not in seq[k - 1]['lit']
    def target(s, aid):
        """where she spends the hold: the midpoint of the two closest of her three sampled places (so the pool holds her at two of
        the three moments, the audit's own test); one place if she is seen at only one."""
        P = [P[aid] for P in s['poses'] if aid in P]
        if len(P) == 1: a = b = P[0]
        else: a, b = min(((P[i], P[j]) for i in range(len(P)) for j in range(i + 1, len(P))), key=lambda ab: math.hypot(ab[0]['x'] - ab[1]['x'], ab[0]['z'] - ab[1]['z']))
        return [round((a['x'] + b['x']) / 2, 2), floor_y((a['y'] + b['y']) / 2), round((a['z'] + b['z']) / 2, 2)]
    def candidates(s, k):
        out = []
        for p in s['pl']:
            if p['type'] not in MOVERS or p['ch'] in used.get(k, ()): continue
            inn, anyin = s['inn'][p['ch']]
            if not anyin: out.append(p)
        return out
    for row in sorted(rows, key=lambda r: (r['k'], r['kind'] != 'named')):
        k = row['k']; s = seq[k]
        if row['kind'] == 'named':
            aid = row['aid']; t = target(s, aid)
            pref = {'mac-viper': 0, 'glp-x4': 0, 'vl3500': 1}       # a Viper or an X4 before a VL3500 (the VLs are the beam fans and back washes)
            C = sorted(candidates(s, k), key=lambda p: (pref[p['type']], math.hypot(p['hit'][0] - t[0], p['hit'][2] - t[2])))
            if C:
                p = C[0]
                W(k, p['ch'], focus=t, _snap=False, _from=p['hit'], _why=f"re-aimed onto {row['expected']}")
                row['action'] = f"re-aim ch{p['ch']} ({p['type']}) onto {row['expected']} at ({t[0]}, {t[2]})"
                row['fix'] = 'reaim'; continue
            if s['real']:                                          # Binkley's own cue: a follower may re-aim his units, not add one
                row['action'] = 'left: a real cue with no unit of its own to spare'; row['fix'] = None; continue
            # swap: a free Viper, dark here and in the cue before, hung most nearly over her
            free = []
            for ch, u in vipers.items():
                if ch in s['lit'] or ch in used.get(k, ()) or (k > 0 and ch in seq[k - 1]['lit']): continue
                o = lens.get(ch) or u['pos']
                h = math.hypot(o[0] - t[0], o[2] - t[2]); v = (o[1] if ch in lens else 6.2) - t[1]
                if v <= 0.5: continue
                down = math.degrees(math.atan2(v, h))
                if down < 40: continue
                free.append((h, ch, down))
            if free:
                h, ch, down = min(free)
                W(k, ch, i=70, focus=t, zoom=13, _snap=True, _swap=True, _why=f"a free Viper takes {row['expected']}'s special")
                row['action'] = f"swap: free Viper ch{ch} (down {down:.0f} deg) onto {row['expected']} at ({t[0]}, {t[2]})"
                row['fix'] = 'swap'
            else:
                row['action'] = 'left: no free mover near'; row['fix'] = None
        else:
            if row['type'] not in MOVERS:
                row['action'] = f"left: fixed unit ({row['type']}), its focus cannot move"; row['fix'] = None; continue
            if row['ch'] in used.get(k, ()):
                row['action'] = 'taken by a fix above'; row['fix'] = 'reaim'; continue
            x, y, z = row['hit']
            empty_same = sum(1 for r2 in rows if r2['k'] == k and r2['kind'] == 'nobody' and r2.get('type') == row['type'])
            if empty_same >= 3:                                    # three or more of one family empty at once: a fan, a ring, a texture
                row['action'] = f"left: one of {empty_same} empty {row['type']} specials in this cue (a fan / pattern)"; row['fix'] = None; continue
            lit_people = set(a for ch, (inn, _) in s['inn'].items() for a in inn)
            best = None
            for aid, p in s['poses'][0].items():
                if aid in lit_people or abs(p['y'] - y) > DY: continue
                if aid.startswith('ens') and re.match(r'Ensemble \d', p.get('label') or 'Ensemble 0'): continue   # principals and named roles only
                d = math.hypot(p['x'] - x, p['z'] - z)
                if d <= NEAR and (best is None or d < best[0]): best = (d, aid)
            if best:
                aid = best[1]; t = target(s, aid)
                lab = s['poses'][0][aid].get('label') or aid
                W(k, row['ch'], focus=t, _snap=False, _from=row['hit'], _why=f're-aimed onto {lab} (the special had nobody)')
                row['action'] = f"re-aim onto {lab} ({best[0]:.1f} m away) at ({t[0]}, {t[2]})"; row['fix'] = 'reaim'
            else:
                row['action'] = f'left: no principal within {NEAR} m (texture or a waiting pool)'; row['fix'] = None
    return writes


def apply_fixes(seq, writes):
    head, cues, tail = load_show()
    REAL = {c['q'] for c in json.load(open(os.path.join(ROOT, 'assets', 'hamilton-eos.json'), encoding='utf-8'))['cues']}
    taken = REAL | {c['q'] for c in cues}
    byq = {(c['track'], c['q']): c for c in cues}
    followers = {}
    def target_cue(k):
        s = seq[k]; c = byq[(s['track'], s['q'])]
        if not c['real']: return c
        if k in followers: return followers[k]
        idx = cues.index(c); nxt = cues[idx + 1]['q'] if idx + 1 < len(cues) else None
        q = qnum_between(c['q'], nxt, taken); taken.add(q)
        f = {'q': q, 'track': c['track'], 'at': c['at'], 'real': False, 'label': f"{s['label'] or 'Q' + c['q']} - the specials on their people",
             'time': {'up': 1}, 'ch': {}, 'why': f'{MARK}: a follower of real cue {c["q"]} (its content is ETC\'s and stays): the spotlight fixes below.'}
        cues.insert(idx + 1, f); followers[k] = f
        return f
    def put(k, ch, params, why):
        c = target_cue(k)
        d = c['ch'].setdefault(str(ch), {})
        for kk, v in params.items(): d[kk] = v
        if why and why not in (c.get('why') or ''): c['why'] = (c.get('why') + ' ' if c.get('why') else '') + f'({MARK}: ch{ch} {why}.)'
    n = {'reaim': 0, 'swap': 0, 'restore': 0, 'followers': 0}
    # channel runs: what each written channel does after its last write
    last_k = {}
    for k in sorted(writes):
        for ch in writes[k]: last_k.setdefault(ch, []).append(k)
    for k in sorted(writes):
        for ch, w in writes[k].items():
            p = {kk: v for kk, v in w.items() if not kk.startswith('_')}
            snap = w.get('_snap') or (k > 0 and seq[k - 1]['track'] == seq[k]['track'] and ch not in seq[k - 1]['lit'])
            if snap: p['time'] = {'focus': 0, 'color': 0, 'beam': 0}
            put(k, ch, p, w.get('_why'))
            n['swap' if w.get('_swap') else 'reaim'] += 1
    # restores: for each written channel, after each run of writes, give back its old landing before it is next used
    for ch, ks in last_k.items():
        ks = sorted(ks)
        for j, k in enumerate(ks):
            nxt_write = ks[j + 1] if j + 1 < len(ks) else None
            if nxt_write == k + 1: continue                  # the next cue re-aims it again: it carries on
            w = writes[k][ch]
            before = seq[k]['lit'].get(ch)                     # how it landed here before the fix (None: it was dark here: a swap)
            # where does it land next, untouched? the first later cue that lights it
            m = k + 1
            while m < len(seq) and ch not in seq[m]['lit'] and m != nxt_write: m += 1
            if m >= len(seq) or m == nxt_write:
                if w.get('_swap') and k + 1 < len(seq): put(k + 1, ch, {'i': 0}, 'out after its swap'); n['restore'] += 1
                continue
            later = seq[m]['lit'][ch]
            ref = before or None
            carried = ref is None or (ref.get('hit') and later.get('hit') and math.dist(ref['hit'], later['hit']) < 0.06)
            if w.get('_swap'):
                put(k + 1, ch, {'i': 0}, 'out after its swap'); n['restore'] += 1
            if not carried and not w.get('_swap'): continue
            # restore its old landing (and zoom) in the first dark cue between, else in cue m
            r = k + 1 if w.get('_swap') else None
            if r is None:
                r = next((x for x in range(k + 1, m) if ch not in seq[x]['lit']), m)
            if r == k + 1 and w.get('_swap') and r == m: r = m
            h = later['hit']
            rp = {'focus': [round(h[0], 2), round(h[1], 2), round(h[2], 2)]}      # exactly where it landed (a step at 0.23 is not the deck)
            if w.get('_swap') or abs(later['zoom'] - (w.get('zoom') or later['zoom'])) > 0.2: rp['zoom'] = later['zoom']
            put(r, ch, rp, 'given back its own focus' + (' in the dark' if r < m else ''))
            n['restore'] += 1
    n['followers'] = len(followers)
    save_show(head, cues, tail)
    return n


# ---------------------------------------------------------------------------------------------------------------- the report
def report(rows, seq, path, title, counts_before=None):
    n_pl = sum(len(s.get('pl', [])) for s in seq if s.get('poses'))
    named = [r for r in rows if r['kind'] == 'named']; nob = [r for r in rows if r['kind'] == 'nobody']
    acts = {}
    for r in rows:
        key = (r.get('action') or 'not fixed (report only)').split(' ')[0].rstrip(':')
        acts[key] = acts.get(key, 0) + 1
    L = [f'# The spotlight audit - {title}', '',
         'Made by `tools/spot-audit.py` (its header says how): every person light of every cue against the actors as they stand now,',
         'posed at 25 / 60 / 95 % of each hold. Set-local metres. "named" = the cue names someone who is in none of its person lights;',
         '"nobody" = a special with nobody in it.', '',
         f'- cues audited: {sum(1 for s in seq if s.get("poses"))}; person lights checked (cue x light): {n_pl}',
         f'- misses: {len(rows)} ({len(named)} named, {len(nob)} nobody)']
    if counts_before: L.append(f'- before the fixes: {counts_before}')
    L += ['- actions: ' + ', '.join(f'{k} {v}' for k, v in sorted(acts.items())), '',
          '| track | q | at | ch | label | expected | in it | action |', '|---|---|---|---|---|---|---|---|']
    for r in rows:
        lab = (r['label'] or '').replace('|', '/')[:60]
        L.append(f"| {r['track']} | {r['q']} | {r['at']} | {r['ch'] and 'ch' + r['ch']} | {lab} | {r['expected']} | {r['inn']} | {r.get('action', '')} |")
    with open(path, 'w', encoding='utf-8', newline='\n') as f: f.write('\n'.join(L) + '\n')


def main(argv):
    if '--dump' not in argv: print(__doc__); return 2
    dump = argv[argv.index('--dump') + 1]
    out = argv[argv.index('--out') + 1] if '--out' in argv else os.path.join(ROOT, 'docs', 'hamilton-spot-audit.md')
    only = set(argv[argv.index('--tracks') + 1].split(',')) if '--tracks' in argv else None
    seq, rows, tracks, actors = audit(dump, only)
    named = sum(1 for r in rows if r['kind'] == 'named'); nob = len(rows) - named
    n_pl = sum(len(s.get('pl', [])) for s in seq if s.get('poses'))
    print(f'person lights checked {n_pl}; misses {len(rows)} (named {named}, nobody {nob})')
    if '--fix' in argv or '--dry' in argv:
        writes = plan_fixes(seq, rows, tracks)
        if '--fix' in argv:
            n = apply_fixes(seq, writes)
            print('fixes:', n)
    else:
        for r in rows: r.setdefault('action', 'reported')
    before = argv[argv.index('--before') + 1] if '--before' in argv else None
    report(rows, seq, out, 'before the fixes' if '--fix' in argv else 'as the cues stand', before)
    if '--json' in argv:
        json.dump([{k: v for k, v in r.items() if k != 'k'} for r in rows], open(argv[argv.index('--json') + 1], 'w', encoding='utf-8'), indent=0)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
