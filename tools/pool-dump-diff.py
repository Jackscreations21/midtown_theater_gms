#!/usr/bin/env python3
"""What moved between two pool dumps (tools/pool-dump.js), cue by cue.

    python -I tools/pool-dump-diff.py <DUMP A> <DUMP B> [track ...]

For every cue in B: each unit lit in one and not the other (+chN / -chN), and each whose level (> 0.02), landing (> 0.1 m), zoom
(> 0.2 deg), gobo or colour changed.  Run it after any cue edit against a dump made before it: every line should be a cue you
meant to change.  A re-aimed mover that carries its new focus into later cues shows up here (TRAPS, 2026-10-15).
Standard library only.
"""
import glob, json, math, os, sys


def main(argv):
    if len(argv) < 2: print(__doc__); return 2
    A, B, want = argv[0], argv[1], set(argv[2:])
    for f in sorted(glob.glob(os.path.join(B, '[12]-*.json'))):
        t = os.path.basename(f)[:-5]
        if want and t not in want: continue
        fa = os.path.join(A, t + '.json')
        if not os.path.exists(fa): continue
        a = {c['q']: c for c in json.load(open(fa, encoding='utf-8'))['cues']}
        for cb in json.load(open(f, encoding='utf-8'))['cues']:
            ca = a.get(cb['q'])
            if ca is None: print(f'{t} {cb["q"]} NEW ({len(cb["pools"])} lit)'); continue
            pa = {p['id']: p for p in ca['pools']}; pb = {p['id']: p for p in cb['pools']}
            ch = []
            for k in sorted(set(pa) | set(pb), key=lambda s: int(s[2:]) if s[2:].isdigit() else 0):
                x, y = pa.get(k), pb.get(k)
                if x is None: ch.append(f'+{k}@{y["level"]}'); continue
                if y is None: ch.append(f'-{k}'); continue
                hx, hy = x.get('hit'), y.get('hit')
                dm = math.dist(hx, hy) if hx and hy else (0 if hx == hy else 99)
                dl, dz = abs(x['level'] - y['level']) > 0.02, abs(x['zoom'] - y['zoom']) > 0.2
                dg, dc = x.get('gobo') != y.get('gobo'), x['color'] != y['color']
                if dl or dm > 0.1 or dz or dg or dc:
                    ch.append(k + (f' lv{x["level"]}>{y["level"]}' if dl else '') + (f' ({hx[0]},{hx[2]})>({hy[0]},{hy[2]})' if dm > 0.1 and hx and hy else (' hit?' if dm > 0.1 else ''))
                              + (f' z{x["zoom"]}>{y["zoom"]}' if dz else '') + (f' g{x.get("gobo")}>{y.get("gobo")}' if dg else '') + (f' {x["color"]}>{y["color"]}' if dc else ''))
            if ch: print(f'{t} {cb["q"]} @{cb["at"]}: ' + '; '.join(ch[:14]) + (f' ... +{len(ch) - 14}' if len(ch) > 14 else ''))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
