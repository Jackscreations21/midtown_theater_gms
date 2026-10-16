import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cuelib import *
head, cues, tail = load()
rig = json.load(open(os.path.join(W, 'assets', 'hamilton-rig.json'), encoding='utf-8'))['units']
chs = sorted({int(ch) for u in rig for ch in u['channels'] if u['type'] != 'hazer'})
c = find(cues, '1300', '2-23')
c['ch'] = {str(k): {'i': 0} for k in chs}
save(head, cues, tail)
print(len(chs), 'channels zeroed in 1300')
