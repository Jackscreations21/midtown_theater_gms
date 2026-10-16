"""The three carries the WIP-2 re-dump still showed."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cuelib import *
head, cues, tail = load()
F = lambda q, t: find(cues, q, t)
c = F('589', '1-20'); c['ch']['1']['i'] = 100; c['ch']['5']['i'] = 100
c = F('168', '1-05'); setch(c, 2, cmy=[0, 11, 44.7], cto=58)
c = F('942', '2-06')
setch(c, 17, gobo='Construction', goboIdx=-121.3); setch(c, 19, gobo='Construction', goboIdx=118.3)
note(c, '(Vipers 17 / 19 re-marked dark to their Construction gobo after the gallery keys.)')
save(head, cues, tail)
print('ok')
