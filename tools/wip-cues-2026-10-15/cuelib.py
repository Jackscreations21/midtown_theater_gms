"""Scratch helpers: read / write assets/hamilton-show.json in its own style (one compact cue per line)."""
import json, os
W = r'C:/Users/jackf/OneDrive/Documents/midtown_theater_gms/.claude/.claude/worktrees/cues'
SHOW = os.path.join(W, 'assets', 'hamilton-show.json')
EOS = os.path.join(W, 'assets', 'hamilton-eos.json')

def load():
    raw = open(SHOW, encoding='utf-8', newline='').read()
    lines = raw.split('\n')
    i0 = lines.index('"cues": [')
    head = lines[:i0 + 1]
    j = len(lines) - 1
    while not lines[j].startswith('{"q":'): j -= 1
    tail = lines[j + 1:]
    cues = [json.loads(l.rstrip(',')) for l in lines[i0 + 1:j + 1]]
    return head, cues, tail

def dump_cue(c):
    return json.dumps(c, ensure_ascii=False, separators=(',', ':'))

def save(head, cues, tail):
    body = [dump_cue(c) + (',' if k + 1 < len(cues) else '') for k, c in enumerate(cues)]
    txt = '\n'.join(head + body + tail)
    tmp = SHOW + '.tmp'
    with open(tmp, 'w', encoding='utf-8', newline='') as f: f.write(txt)
    os.replace(tmp, SHOW)

REAL_Q = {c['q'] for c in json.load(open(EOS, encoding='utf-8'))['cues']}

def find(cues, q, track=None):
    L = [c for c in cues if c['q'] == str(q) and (track is None or c['track'] == track)]
    assert len(L) == 1, (q, track, len(L))
    return L[0]

def insert(cues, new):
    """Insert a reconstructed cue in q order; checks the number is free, not a real Eos number, and that time order holds."""
    q = float(new['q'])
    assert new['q'] not in REAL_Q, ('real eos number', new['q'])
    assert all(c['q'] != new['q'] for c in cues), ('taken', new['q'])
    k = 0
    while k < len(cues) and float(cues[k]['q']) < q: k += 1
    prev, nxt = cues[k - 1], cues[k] if k < len(cues) else None
    tord = lambda c: (c['track'], c['at'])
    assert tord(prev) <= tord(new), ('time order prev', prev['q'], new['q'])
    if nxt: assert tord(new) <= tord(nxt), ('time order next', new['q'], nxt['q'])
    cues.insert(k, new)
    return new

def cue(q, track, at, label, time, ch, why):
    return {'q': str(q), 'track': track, 'at': at, 'real': False, 'label': label, 'time': time, 'ch': ch, 'why': why}

def setch(c, ch, **kw):
    """Merge keys into one channel of a reconstructed cue (per channel, per key - TRAPS: never replace the channel dict)."""
    assert not c['real'], ('real cue', c['q'])
    d = c['ch'].setdefault(str(ch), {})
    for k, v in kw.items():
        if v is None: d.pop(k, None)
        else: d[k] = v
    return d

def note(c, s):
    c['why'] = (c.get('why') or '') + ' ' + s if c.get('why') else s
