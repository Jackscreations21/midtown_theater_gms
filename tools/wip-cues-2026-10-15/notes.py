"""Part (a): Jack's lighting notes and the blocking agents' hand-offs, applied to assets/hamilton-show.json."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cuelib import *

DUMP = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dump', 'before')
LIT = {}
def lit_before(track, q):
    """channels lit in the cue BEFORE q in this track (from the pre-edit dump); None if q is the first."""
    if track not in LIT:
        LIT[track] = json.load(open(os.path.join(DUMP, track + '.json'), encoding='utf-8'))['cues']
    prev = None
    for c in LIT[track]:
        if float(c['q']) >= float(q): break
        prev = c
    return None if prev is None else {p['ch'] for p in prev['pools']}

SNAP = {'focus': 0, 'color': 0, 'beam': 0}
def aim(c, ch, xyz, snap=None, **kw):
    """Set a mover's focus in reconstructed cue c (set-local metres). snap None: snap only if it was dark in the cue before."""
    d = setch(c, ch, focus=[round(v, 2) for v in xyz], **kw)
    if snap is None:
        before = lit_before(c['track'], c['q'])
        snap = before is not None and str(ch) not in before
    if snap:
        t = dict(d.get('time') or {}); t.update(SNAP); d['time'] = t
    return d

head, cues, tail = load()
n0 = len(cues)
F = lambda q, t: find(cues, q, t)
G = 2.74        # a gallery floor (2.743)
D = 0.05        # the deck (0.045)
WARM = [0, 5.5, 25.5]
JN = "Jack's notes 2026-10-15"

# ===================================================================== 1-01 Alexander Hamilton: "the spotlights are off"
c = F('38', '1-01'); aim(c, 2, [-4.4, D, 3.2], snap=False)
note(c, JN + ' ("the spotlights are off"): Burr\'s AF (ch2) follows him to his SR spot (-4.4, 3.2) as it drops.')
c = F('61', '1-01')
aim(c, 47, [-0.5, G, -3.35]); aim(c, 49, [0.5, G, -3.35]); aim(c, 51, [2.2, G, -3.35])
note(c, JN + ': the three sing from the upstage gallery since notes2 - the X4s re-aimed onto Lafayette (-0.5), Mulligan (0.5) and '
        'Laurens (2.2) at y 2.74 (they reach it over the rail at 34-39 deg).')
c = F('62', '1-01')
setch(c, 6, focus=[-5.45, G, 2.2], zoom=12, gobo='Open', goboRot=0, cmy=WARM, cto=0)
note(c, 'Viper 6 marked dark onto Washington\'s SR balcony for 63 (Viper 12, his usual special, cannot reach it: the balcony rail).')
c = F('63', '1-01'); c['ch'].pop('12'); setch(c, 6, i=100)
c['label'] = 'Washington special - the SR balcony'
note(c, JN + ': Washington sings from the SR balcony (-5.5, 2.2); Viper 6 takes his special (12 cannot reach).')
c = F('64', '1-01'); c['ch'].pop('12'); setch(c, 6, i=0); c['ch'].pop('48')
aim(c, 52, [5.25, G, 2.2], zoom=16)
c['label'] = 'The women - the sisters on the SL balcony'
note(c, JN + ': the three sisters sing from the SL end balcony; one X4 pool (52, zoom 16) holds all three; 48 stays dark.')
c = F('65', '1-01'); aim(c, 2, [0.0, D, 2.5])
note(c, JN + ': Burr sings this at centre (0, 2.5); his AF moved there.')

# ===================================================================== 1-04 The Story of Tonight: "just spotlights on them"
c = F('147', '1-04')
for ch, xz in ((48, (-1.3, 4.35)), (49, (-0.45, 4.6)), (50, (0.45, 4.6)), (51, (1.35, 4.35))):
    setch(c, ch, focus=[xz[0], D, xz[1]], time={'focus': 2.2})
note(c, JN + ': the four stand and come forward (84-86): their four X4 specials travel with them to the lip (focus 2.2 s).')
old147 = {k: dict(v) for k, v in c['ch'].items()}
ch1475 = {str(k): {'i': 90} for k in (48, 49, 50, 51)}
for k in range(53, 65): ch1475[str(k)] = {'i': 6}
for k in (71, 73, 74, 76): ch1475[str(k)] = {'i': 0}
ch1475['g:261'] = {'i': 10}
for k in old147:
    if k.isdigit() and int(k) >= 600: ch1475[k] = {'i': 8}
insert(cues, cue('147.5', '1-04', 86.0, 'Just the four at the lip - the rest away', {'up': 2, 'down': 3}, ch1475,
                 JN + ': "at the end they stand up and move forward and it is just spotlights on them": the four in their specials, '
                 'the room taken almost out (a 6% blue, so the chairs\' strike, 88.2 to 1-05 2.3, reads as shadows).'))
c = F('150', '1-05')            # 1-05's top keeps its look: what 147.5 changed, restored where 150 does not set it
restore = {'48': 68.0, '49': 68.0, '50': 68.0, '51': 68.0, 'g:261': 42.0}
for k in range(53, 65): restore[str(k)] = 54.0
for k in old147:
    if k.isdigit() and int(k) >= 600 and 'i' in old147[k]: restore[k] = old147[k]['i']
for k, v in restore.items():
    if 'i' not in c['ch'].get(k, {}): setch(c, k, i=v)
note(c, '(2026-10-15: restores the levels 147.5 took down, so this top is as it was.)')

# ===================================================================== 1-05: Burr in the DSR corner (hand-off)
insert(cues, cue('164.5', '1-05', 94.6, 'Burr in the DSR corner - a low key', {'up': 2},
                 {'2': {'i': 30, 'focus': [-4.3, D, 4.35], 'zoom': 12, 'gobo': 'Open', 'goboRot': 0, 'cmy': WARM, 'cto': 0, 'time': dict(SNAP)}},
                 'Hand-off (blocking; Jack: "burr goes off too early"): Burr backs into the DSR corner (-4.3, 4.35) on 164 and watches '
                 'to 115.7; his AF Viper holds him low so he is seen.'))
c = F('167', '1-05'); setch(c, 2, i=0); note(c, "(Burr's low key out as he leaves the corner, 115.7.)")

# ===================================================================== 1-14 Stay Alive: "charles lee's spotlight is off"
c = F('440', '1-14'); setch(c, 5, i=80, focus=[1.1, D, 4.1])
note(c, JN + ' ("charles lee\'s spotlight is off"): Lee\'s Viper 5 stays on him, white, as he takes the lip for his orders.')
for q, xz, t in (('441', (-0.8, 4.0), 1.2), ('441.5', (0.9, 4.2), 0.9), ('442', (-0.9, 4.0), 0.7), ('442.5', (-2.4, 4.3), 1.5)):
    c = F(q, '1-14'); setch(c, 5, focus=[xz[0], D, xz[1]], time={'focus': t})
    note(c, 'Viper 5 follows Lee along the lip to his next mark (the snap colour flips are unchanged).')
c = F('443', '1-14'); setch(c, 5, i=60, focus=[-2.1, D, 4.35], time={'focus': 4})
note(c, 'Lee held low DSR (-2.4..-1.8, 4.3) until he goes, 109.5.')
insert(cues, cue('443.5', '1-14', 109.5, 'Lee goes - his key out', {'up': 1.5, 'down': 1.5}, {'5': {'i': 0}},
                 JN + ': Lee walks off DSR at 109.5; his special goes with him.'))
c = F('444', '1-14')
setch(c, 95, focus=[4.9, G, 1.87], zoom=12, gobo='Open', goboRot=0, cmy=WARM, cto=0)
note(c, "Viper 95 marked dark onto the SL gallery for Lee's slander (445).")
c = F('445', '1-14'); c['ch'].pop('5'); setch(c, 95, i=82)
c['label'] = 'Lee slanders Washington - Lee on the SL gallery, the camp at dusk'
note(c, JN + ': Lee speaks from the SL gallery (4.9, 1.8-1.95, y 2.74): Viper 95 (2nd Electric) takes his special; Viper 5 cannot '
        'reach the gallery (the house ceiling in front of the apron).')
c = F('446', '1-14'); setch(c, 95, i=0)

# ===================================================================== 2-06 Schuyler Defeated: "put a light on them"
c = F('935', '2-06')
setch(c, 2, i=0); setch(c, 4, i=0)
for ch, x in ((17, -0.8), (19, 0.8)):
    setch(c, ch, i=95, focus=[x, G, -3.35], cmy=WARM, cto=0, zoom=12, edge=0, iris=100, frost=0, cw='open', gobo='Open', goboRot=0, goboIdx=None)
note(c, JN + ' ("i cant see philip and eliza put a light on them"): their keys are now Vipers 17 / 19 on the 9th Electric, on Eliza '
        '(-0.8) and Philip (0.8) at the upstage gallery rail. The apron Vipers 2 / 4 that had them were stopped 0.8 m from the lens by '
        'the house ceiling (cue notes) and are out.')
c = F('938', '2-06'); c['ch'].pop('2'); c['ch'].pop('4'); setch(c, 17, i=57.0); setch(c, 19, i=57.0)
c = F('939', '2-06'); c['ch'].pop('2'); c['ch'].pop('4'); setch(c, 17, i=0); setch(c, 19, i=0)

# ===================================================================== 2-07 Cabinet Battle #2: sides, switch, no blackout
SW = {'1': '5', '5': '1', '6': '10', '10': '6', '92': '94', '94': '92'}
for c in cues:
    if c['track'] == '2-07' and not c['real'] and 944 <= float(c['q']) <= 958:
        new = {}
        for k, v in c['ch'].items():
            k2 = SW.get(k, k)
            if k in SW and isinstance(v.get('focus'), list):
                v = dict(v); f = v['focus']; v['focus'] = [round(-f[0], 3), f[1], f[2]]
            new[k2] = v
        c['ch'] = new
        if float(c['q']) <= 957:
            note(c, JN + ' ("lights are on the wrong side of ham and jefferson"): mirrored to the ruled sides (Jefferson and Madison SR, '
                    'Hamilton SL): channels 1<->5, 6<->10, 92<->94 swapped and x -> -x.')
F('945', '2-07')['label'] = "Jefferson's verse - dark navy, Jefferson DR"
c = F('951', '2-07'); c['at'] = 77.27; c['label'] = "Hamilton's verse - dark navy, Hamilton DL"
note(c, JN + ' ("the switch between the lights happens too late"): moved from 82.1 to 77.27, the first downbeat after Washington calls '
        'him (950, 76.0); the blocking has him at his mark from 77.0.')
c = F('958', '2-07')
for k in ('1', '5', '6', '10'): c['ch'][k] = {'i': 35}
for k in [str(x) for x in range(251, 260)] + [str(x) for x in range(261, 270)]: c['ch'].pop(k, None)
c['time'] = {'up': 0, 'down': 1.5}
c['label'] = 'Button - the keys pull down, the room holds'
note(c, JN + ' ("shouldn\'t be a blackout at the end"): no snap to black: the four keys pull down to 35% over 1.5 s and the navy side '
        'light holds; 2-08\'s red top (960) cross-fades over it.')
c = F('960', '2-08')
for k in ['1', '5'] + [str(x) for x in range(251, 260)] + [str(x) for x in range(261, 270)]:
    if 'i' not in c['ch'].get(k, {}): setch(c, k, i=0)
for k in ('6', '10'): assert 'i' in c['ch'][k]
note(c, "(2026-10-15: also takes out what 2-07's button now leaves up - Vipers 1 / 5 and the side light - under its 3 s cross-fade.)")

# ===================================================================== 2-23 the curtain call
c = F('1298', '2-23')
assert c['at'] == 214.8
line = {}
for ch, x in ((23, -5.0), (1, -3.4), (2, -1.7), (4, 1.7), (5, 3.4), (24, 5.2)):
    line[str(ch)] = {'i': 70, 'focus': [x, D, 4.2], 'zoom': 22, 'gobo': 'Open', 'goboRot': 0, 'cmy': [0, 31.8, 78.4], 'cto': 0}
    if ch in (23, 2, 4, 24): line[str(ch)]['time'] = dict(SNAP)
line['8'] = {'focus': [0.0, D, 4.2]}
for k in ('13', '18', '19') + tuple(str(x) for x in (169, 168, 167, 178, 177, 179, 120, 164, 166, 174, 176, 175,
                                                     187, 186, 188, 185, 189, 190, 183, 182, 192, 181, 191, 147, 145, 116, 143)):
    line[k] = {'i': 0}
insert(cues, cue('1299', '2-23', 219.85, 'The line comes down - the front up, the back away', {'up': 4, 'down': 5}, line,
                 'Curtain call (2026-10-15): as the company walks into one line at z 4.2 (219.85-226.0) for bows 2 and 3, six apron '
                 'Vipers lay a warm front across the line (x -5..5.2) and the centre top light follows it down; the upstage floor '
                 'and gallery pools go, so nothing lights the empty back.'))
insert(cues, cue('1300', '2-23', 239.8, 'The company gone - fade to black', {'up': 4, 'down': 4}, {'*': {'i': 0}},
                 'Curtain call (2026-10-15): the line has peeled off into the DS wings (last off 239.4); the last cue of the show, a 4 s '
                 'fade to black.'))

# ===================================================================== the other hand-offs
c = F('87', '1-02'); aim(c, 51, [-0.5, D, 1.45]); note(c, 'Hand-off 2026-10-15: on Laurens at (-0.5, 1.45).')
c = F('88', '1-02'); setch(c, 48, focus=[-1.85, D, 1.45]); note(c, 'Hand-off 2026-10-15: on Lafayette at (-1.85, 1.45).')
c = F('89', '1-02'); setch(c, 50, focus=[-1.2, D, -0.85]); note(c, 'Hand-off 2026-10-15: on Mulligan at (-1.2, -0.85) (it was on Hamilton).')
c = F('288', '1-08')
setch(c, 2, focus=[0.0, D, 3.4]); setch(c, 4, focus=[0.0, D, 2.75])
setch(c, 12, focus=[0.0, D, 3.4]); setch(c, 14, focus=[0.0, D, 2.75])
note(c, 'Hand-off 2026-10-15: the finale picture is a column, Washington (0, 3.4) in front of Hamilton (0, 2.75): keys 2 / 12 on '
        'Washington, 4 / 14 on Hamilton (they were side by side).')
c = F('587', '1-20')
setch(c, 1, i=55, focus=[0.0, D, 4.7], zoom=12, gobo='Open', goboRot=0, cmy=[0, 25, 50], cto=0, time=dict(SNAP))
note(c, 'Hand-off 2026-10-15: Hamilton is at the lip (0, 4.7) from the top: apron Viper 1 keys him.')
insert(cues, cue('587.5', '1-20', 10.0, 'Lafayette joins Hamilton at the lip - keys', {'up': 1.5},
                 {'5': {'i': 55, 'focus': [0.9, D, 4.75], 'zoom': 12, 'gobo': 'Open', 'goboRot': 0, 'cmy': [0, 25, 50], 'cto': 0, 'time': dict(SNAP)}},
                 'Hand-off 2026-10-15: Lafayette reaches the lip beside Hamilton (0.9, 4.75) at 10; both were dim to 20.2.'))
c = F('589', '1-20'); setch(c, 1, i=0); setch(c, 5, i=0)
c = F('725', '2-01'); k18 = dict(c['ch'].pop('18'))
c['label'] = 'Jefferson up top - the room eases under his key'
note(c, '(2026-10-15: his key now comes up at 44.0, cue 723.5.)')
k18['focus'] = [0.0, G, -3.45]; k18['time'] = dict(SNAP)
insert(cues, cue('723.5', '2-01', 44.0, 'Jefferson appears up top - warm-white key', {'up': 1}, {'18': k18},
                 'Hand-off 2026-10-15: Jefferson is on the upstage gallery at (0, -3.45) from 44 (it was 57.9, and its focus landed on the '
                 'back wall behind him).'))
c = F('745', '2-02'); setch(c, 8, focus=[-1.3, D, 3.7], zoom=14)
note(c, 'Hand-off 2026-10-15: Jefferson works the room from his DR spot (-1.3, 3.7), not centre: Viper 8 on him.')
c = F('1013', '2-11'); setch(c, 44, i=0, preset=None, rgb=None, w=None)
aim(c, 18, [-0.3, G, -3.1], i=80, zoom=12, gobo='Open', goboRot=0, cmy=[0, 8.6, 5.5], cto=0)
setch(c, 73, i=30)
note(c, 'Hand-off 2026-10-15: Hamilton replies from the upstage gallery (-0.3, -3.1): Viper 18 (9th Electric) is his special (the X4 '
        '44 DS special lit nobody); Jefferson, below at (-0.8, 2.2), kept low in VL 73.')
c = F('1014', '2-11'); setch(c, 44, i=0, rgb=None, w=None); setch(c, 18, i=100)
c = F('1015', '2-11'); setch(c, 18, i=0); setch(c, 73, i=0)

save(head, cues, tail)
print('cues', n0, '->', len(cues))
