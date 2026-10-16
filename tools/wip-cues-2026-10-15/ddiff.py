# ddiff.py <dirA> <dirB> [tracks...] : per cue, the units whose level / landing changed between two dumps
import json, os, sys, glob, math
A, B = sys.argv[1], sys.argv[2]
want = sys.argv[3:]
for f in sorted(glob.glob(os.path.join(B, '[12]-*.json'))):
    t = os.path.basename(f)[:-5]
    if want and t not in want: continue
    fa = os.path.join(A, t + '.json')
    if not os.path.exists(fa): continue
    a = {c['q']: c for c in json.load(open(fa, encoding='utf-8'))['cues']}
    b = json.load(open(f, encoding='utf-8'))['cues']
    for cb in b:
        ca = a.get(cb['q'])
        if ca is None:
            print(f'{t} {cb["q"]} NEW ({len(cb["pools"])} lit)'); continue
        pa = {p['id']: p for p in ca['pools']}; pb = {p['id']: p for p in cb['pools']}
        ch = []
        for k in sorted(set(pa) | set(pb), key=lambda s: int(s[2:]) if s[2:].isdigit() else 0):
            x, y = pa.get(k), pb.get(k)
            if x is None: ch.append(f'+{k}@{y["level"]}'); continue
            if y is None: ch.append(f'-{k}'); continue
            dl = abs(x['level'] - y['level'])
            hx, hy = x.get('hit'), y.get('hit')
            dm = math.dist(hx, hy) if hx and hy else (0 if hx == hy else 99)
            if dl > 0.02 or dm > 0.1:
                ch.append(f'{k}' + (f' lv{x["level"]}>{y["level"]}' if dl > 0.02 else '') + (f' ({hx[0]},{hx[2]})>({hy[0]},{hy[2]})' if dm > 0.1 and hx and hy else (' hit?' if dm > 0.1 else '')))
        if ch: print(f'{t} {cb["q"]} @{cb["at"]}: ' + '; '.join(ch[:14]) + (f' ... +{len(ch) - 14}' if len(ch) > 14 else ''))
