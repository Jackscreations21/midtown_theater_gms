# look.py <dumpdir> <track> <t1,t2,..> [--all]  : actors + person lights at moments (scratch helper)
import sys, os, json, math, importlib.util
W = r'C:/Users/jackf/OneDrive/Documents/midtown_theater_gms/.claude/.claude/worktrees/cues'
spec = importlib.util.spec_from_file_location('bp', os.path.join(W, 'tools', 'blocking-plot.py')); bp = importlib.util.module_from_spec(spec); spec.loader.exec_module(bp)
d, tracks, actors = bp.load_inputs(os.path.join(W, 'assets', 'hamilton-blocking.json'))
ddir, tid, times = sys.argv[1], sys.argv[2], [float(x) for x in sys.argv[3].split(',')]
allk = '--all' in sys.argv
dump = json.load(open(os.path.join(ddir, tid + '.json'), encoding='utf-8'))
for sec in times:
    T = tracks[tid]['start'] + sec
    cue = None
    for c in dump['cues']:
        if c['at'] <= sec + 1e-6: cue = c
    print(f'=== {tid} {sec}: cue {cue["q"]} @{cue["at"]}-{cue["until"]} {cue.get("label")}')
    ps = [(a, bp.pose(a['c'], T)) for a in actors]
    vis = [(a, p) for a, p in ps if p and p['visible']]
    for a, p in vis:
        print(f'   {a["id"]:<11} {str(p["label"]):<16} ({p["x"]:6.2f},{p["z"]:6.2f}) y{p["y"]:.2f}{" mv" if p["moving"] else ""}')
    for q in cue['pools']:
        if q['level'] < 0.05: continue
        pl = q['kind'] == 'special' or (q['kind'] in ('wash',) and q['zoom'] <= 18.5)
        if not pl and not allk: continue
        lands = q['lands']
        if q.get('hit') and (lands in ('deck', 'gallery') or lands.startswith('floor')): x, y, z = q['hit']; r = q['hitR']
        elif q.get('deck'): (x, z), y, r = q['deck'], 0.045, q['deckR']
        else: continue
        occ = [a['id'] for a, p in vis if abs(p['y'] - y) <= 0.6 and math.hypot(p['x'] - x, p['z'] - z) <= r + 0.3]
        print(f'      ch{q["ch"]:<4} {q["type"]:<11} {q["kind"]:<7} z{q["zoom"]:<5} lv{q["level"]:<5} ({x:6.2f},{y:5.2f},{z:6.2f}) r{r:.2f} {lands:<8} -> {",".join(occ) or "NOBODY"}')
