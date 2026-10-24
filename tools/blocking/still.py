#!/usr/bin/env python3
"""Who stands still, and for how long: every stretch where someone on stage neither walks nor dances.

    python -I still.py [--blocking FILE] [--tracks 1-03,1-04] [--min SECONDS] [--all]

For each track (default all), each actor is posed every 0.5 s with tools/blocking-plot.py's pose(); she is STILL at a moment
when she is visible, on the stage (|x| <= 7.5, z <= 5.6), not walking (`moving` false) and has no dance move running
(`sit` and the gestures count as moving: they are something the body does). Runs of still at least --min seconds
(default 8) are printed with where she stands and the move she last did, then a line per track: the share of on-stage
time spent still, over the whole company and per principal. --all also prints the actors with no long run.

STILL IS NOT WRONG BY ITSELF: a soliloquy, a tableau, a listener, a held picture are still on purpose. This is the list to
read against the footage and the score, not a list of faults. Standard library only.
"""
import importlib.util, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
spec = importlib.util.spec_from_file_location('blocking_plot', os.path.join(ROOT, 'tools', 'blocking-plot.py'))
BP = importlib.util.module_from_spec(spec); spec.loader.exec_module(BP)
STEP = 0.5


def main(argv):
    path = argv[argv.index('--blocking') + 1] if '--blocking' in argv else os.path.join(ROOT, 'assets', 'hamilton-blocking.json')
    least = float(argv[argv.index('--min') + 1]) if '--min' in argv else 8.0
    _, tracks, actors = BP.load_inputs(path)
    only = argv[argv.index('--tracks') + 1].split(',') if '--tracks' in argv else sorted(tracks, key=lambda t: tracks[t]['i'])
    for tid in only:
        tr = tracks[tid]
        print('== %s %s (%.0f s)' % (tid, tr['title'], tr['len']))
        tot_on = tot_still = 0
        per = []
        for a in actors:
            runs, start, on, still, last = [], None, 0, 0, None
            n = int(tr['len'] / STEP) + 1
            for k in range(n + 1):
                sec = k * STEP
                T = tr['start'] + sec
                p = BP.pose(a['c'], T) if k < n else None
                here = p and p['visible'] and abs(p['x']) <= 7.5 and p['z'] <= 5.6
                mv = BP.dance_at(a, T) if here else None
                if mv: last = mv
                is_still = bool(here and not p['moving'] and not mv)
                if here: on += 1
                if is_still:
                    still += 1
                    if start is None: start = (sec, p)
                elif start is not None:
                    if sec - start[0] >= least: runs.append((start[0], sec, start[1], last))
                    start = None
            tot_on += on; tot_still += still
            if on: per.append((a['id'], on * STEP, still * STEP))
            for s0, s1, p, mv in runs:
                print('  %-10s %6.1f-%6.1f  %5.1f s still at (%5.1f, %5.1f)%s  [%s]' % (a['id'], s0, s1, s1 - s0, p['x'], p['z'],
                      ' up' if p['y'] > 1 else '', p['label']) + ('  last move: ' + mv if mv else ''))
        share = 100.0 * tot_still / tot_on if tot_on else 0
        print('  -- still %.0f%% of on-stage time; ' % share + ', '.join('%s %.0f%%' % (i, 100 * s / o) for i, o, s in per
              if (i in ('hamilton', 'burr', 'eliza', 'angelica', 'peggy', 'washington', 'lafayette', 'mulligan', 'laurens', 'king') or '--all' in argv) and o >= 10))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
