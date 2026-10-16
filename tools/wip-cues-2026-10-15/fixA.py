"""The six carry faults of the WIP (docs/WIP-cues-2026-10-15.md)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cuelib import *
head, cues, tail = load()
F = lambda q, t: find(cues, q, t)
BURR_AF = [-1.82, 0.05, 4.25]       # ch2's landing before any edit (preset 117's AF spot DSR)

# 1. ch2 after 1-01 Q38: Burr leaves (-4.4, 3.2) for the DSR lip before 63.4 - back to its own spot in Q42 (lit: it travels with him)
c = F('42', '1-01'); setch(c, 2, focus=list(BURR_AF))
note(c, '(2026-10-15: Burr\'s AF returns to its DSR spot as he comes down to it.)')
# 2. ch2 after Q65: restored dark in Q67 (out since Q66)
c = F('67', '1-01'); setch(c, 2, focus=list(BURR_AF)); note(c, '(ch2 re-marked dark to its DSR spot after Burr\'s centre line.)')
# 3. ch2 after 1-05 164.5: restored dark in 168 (out since 167)
c = F('168', '1-05'); setch(c, 2, focus=list(BURR_AF), zoom=10, cmy=None); note(c, '(ch2 re-marked dark to its DSR spot.)')
# 4. ch6 after Q62-64: its 1-01 Q37 values marked back dark in Q65
c = F('65', '1-01'); setch(c, 6, focus=[-1.2, 0.3, 0.9], cmy=[0, 33.2, 86], gobo='Cobble stone', zoom=22.7)
note(c, '(Viper 6 re-marked dark to its cobble pool after Washington\'s balcony line.)')
c = F('62', '1-01'); setch(c, 6, goboRot=None, cto=None)
# 5. 1-20: 589 sets 1 / 5 itself again (my "i": 0 removed); 587 / 587.5 touch only what 589 resets
c = F('589', '1-20'); c['ch']['1'].pop('i'); c['ch']['5'].pop('i')
c = F('587', '1-20'); d = c['ch']['1']; d.pop('goboRot'); d.pop('cto'); d.pop('time')
c = F('587.5', '1-20'); d = c['ch']['5']; d.pop('goboRot'); d.pop('cto'); d.pop('time')
# 6. 1-05 Q150: the side light g:261 stays as it was (not restored to 42)
c = F('150', '1-05'); c['ch'].pop('g:261')
save(head, cues, tail)
print('ok')
