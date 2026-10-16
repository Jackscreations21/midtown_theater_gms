# The spotlight audit (2026-10-15/16)

Jack: *"there are a bunch of spotlights that are off because of the choreo changing so fix the spotlights"*. Every light meant
for one person, every cue of the show, checked against where the actors stand now (the blocking after his act-1 and act-2
notes), by `tools/spot-audit.py` (its header has the rules). Set-local metres: x + is stage left, z + downstage.

## How it was run

1. The page dumped every lit unit of every cue (`tools/pool-dump.js` in the page, saved by `tools/pool-dump-serve.py`).
2. `python -I tools/spot-audit.py --dump DIR --fix` (pass 1), re-dump, `--fix` again (pass 2), re-dump, and the report-only run
   gives the after count. Two pass-2 results were taken back by hand after looking (below); the dump diff between each step was
   checked so that no cue downstream of a fix moved unless the tool wrote it (each moved unit gets its old focus back).
3. 15 fixed moments rendered and read by eye and by number (`MIDTOWN.lx.beam` landing against `MIDTOWN.actors.pose`).

## The numbers

| | before | after |
|---|---|---|
| person lights checked (cue x light) | 9615 | 9620 |
| named person in none of her cue's person lights | 82 | 17 |
| special with nobody in it | 5547 | 5476 |

Fixes written: 107 - hand 1, re-aim 85, swap 20, tried 1. Each re-aim or swap that would have
carried its new focus into a later cue is given its old landing back in the first later cue where the unit is dark, else the
next cue that lights it; Binkley's real cues are never edited - 12 reconstructed followers carry the fixes on them. Swaps
light a free Viper at 70 % for the one cue and take it out in the next.

## The named misses left, and why

| track | q | at | label | who | why left |
|---|---|---|---|---|---|
| 1-01 | 36 | 2 | Burr Enters | Burr | a real Binkley cue with no unit of its own on nobody to re-aim; adding a unit to his cue is not done |
| 1-15 | 459 | 40.4 | Hamilton/ Burr DL | Hamilton | a real Binkley cue with no unit of its own on nobody to re-aim; adding a unit to his cue is not done |
| 1-15 | 459 | 40.4 | Hamilton/ Burr DL | Burr | a real Binkley cue with no unit of its own on nobody to re-aim; adding a unit to his cue is not done |
| 1-15 | 468 | 77.1 | Hamilton/Burr Scene | Hamilton | a real Binkley cue with no unit of its own on nobody to re-aim; adding a unit to his cue is not done |
| 1-15 | 468 | 77.1 | Hamilton/Burr Scene | Burr | a real Binkley cue with no unit of its own on nobody to re-aim; adding a unit to his cue is not done |
| 1-23 | 638 | 115.1 | Burr/Men | Burr | a real Binkley cue with no unit of its own on nobody to re-aim; adding a unit to his cue is not done |
| 2-01 | 726 | 60.8 | Vamp - Jefferson strides down, beams turn | Jefferson | she / he walks through the hold: the light is on her for part of it |
| 2-05 | 864.01 | 0.4 | Ham/ Burr Enter | Hamilton | a real Binkley cue with no unit of its own on nobody to re-aim; adding a unit to his cue is not done |
| 2-05 | 864.01 | 0.4 | Ham/ Burr Enter | Burr | a real Binkley cue with no unit of its own on nobody to re-aim; adding a unit to his cue is not done |
| 2-05 | 882 | 271.4 | Burr DS | Burr | a real Binkley cue with no unit of its own on nobody to re-aim; adding a unit to his cue is not done |
| 2-16 | 1071 | 51.79 | The theatre - footlights, Eacker's box | George Eacker | the beam cannot reach the box on the SL gallery (it stops on the rail); his box needs a ruling |
| 2-16 | 1072 | 59.39 | Philip confronts Eacker - two pools | George Eacker | the beam cannot reach the box on the SL gallery (it stops on the rail); his box needs a ruling |
| 2-16 | 1073 | 64.82 | Eacker insults Hamilton - cold edge | George Eacker | the beam cannot reach the box on the SL gallery (it stops on the rail); his box needs a ruling |
| 2-22 | 1256 | 151.8 | Hamilton off box | Hamilton | a real Binkley cue with no unit of its own on nobody to re-aim; adding a unit to his cue is not done |
| 2-22 | 1259 | 166.46 | GW UL Steps | Washington | a real Binkley cue with no unit of its own on nobody to re-aim; adding a unit to his cue is not done |
| 2-22 | 1262.1 | 174.5 | ELIZA - the specials on their people | Eliza | she / he walks through the hold: the light is on her for part of it |
| 2-23 | 1280 | 56.84 | All turn to Eliza | Eliza | she / he walks through the hold: the light is on her for part of it |

## The specials with nobody in them, left

- 3469: a fixed unit (its focus cannot move): s4-lustr
- 1233: a mover in a fan / ring / texture (three or more empty of one family in the cue)
- 427: a mover with no principal within 1.5 m (a texture, or a pool waiting for an entrance)
- 300: a fixed unit (its focus cannot move): birdie
- 44: a fixed unit (its focus cannot move): par64
- 2: other: taken by a fix above
- 1: other: re-aim onto Angelica (1.2 m away) at (-2.86, 3.34)

Movers left empty, by track (most are the beam fans, rings and floor textures of the big numbers): 1-01 35, 1-02 30, 1-03 124, 1-04 4, 1-05 65, 1-06 36, 1-07 150, 1-08 95, 1-09 1, 1-10 30, 1-11 36, 1-12 7, 1-13 72, 1-14 80, 1-15 26, 1-16 7, 1-17 9, 1-18 19, 1-19 15, 1-20 34, 1-21 59, 1-23 76, 2-01 56, 2-02 53, 2-03 45, 2-04 16, 2-05 14, 2-06 1, 2-07 11, 2-08 14, 2-09 7, 2-10 113, 2-11 5, 2-12 6, 2-13 1, 2-14 5, 2-15 1, 2-16 55, 2-17 62, 2-18 21, 2-19 37, 2-20 55, 2-21 5, 2-22 7, 2-23 63.

## Every fix

| track | q | at | pass | miss | ch | label | expected | action |
|---|---|---|---|---|---|---|---|---|
| 1-02 | 92 | 139.6 | 1 | named |  | Burr declines — tavern back | Burr | re-aim ch2 (mac-viper) onto Burr at (-4.2, 4.1) |
| 1-03 | 121 | 168.2 | 1 | nobody | ch74 | Chorus 2 — full company | - | re-aim onto Peggy (0.7 m away) at (1.2, -3.35) |
| 1-03 | 122 | 180 | 1 | nobody | ch74 | Chorus 2b — deep amber, the fan sweeps | - | re-aim onto Peggy (0.7 m away) at (1.2, -3.35) |
| 1-03 | 123 | 189.9 | 1 | nobody | ch74 | Call to the company — the line DS | - | re-aim onto Peggy (0.7 m away) at (1.2, -3.35) |
| 1-03 | 124 | 203.5 | 1 | nobody | ch74 | Company shout — build | - | re-aim onto Peggy (0.7 m away) at (1.2, -3.35) |
| 1-03 | 125 | 211.9 | 1 | nobody | ch74 | Bridge chant — the full stage | - | re-aim onto Peggy (0.7 m away) at (1.2, -3.35) |
| 1-03 | 126 | 220.7 | 1 | nobody | ch74 | Bridge chant b — the shafts sweep | - | re-aim onto Peggy (0.7 m away) at (1.2, -3.35) |
| 1-03 | 127 | 231.9 | 1 | nobody | ch74 | Death verse — slow motion, cold | - | re-aim onto Peggy (0.7 m away) at (1.2, -3.35) |
| 1-03 | 129 | 255 | 1 | nobody | ch74 | He shakes it off — snap back | - | re-aim onto Peggy (0.7 m away) at (1.2, -3.35) |
| 1-03 | 131 | 265.3 | 1 | nobody | ch74 | Verse 3 — the shafts close in | - | re-aim onto Peggy (0.7 m away) at (1.2, -3.35) |
| 1-03 | 132 | 275.9 | 1 | named |  | Reading and writing — Hamilton at the table | Hamilton | swap: free Viper ch98 (down 62 deg) onto Hamilton at (0.0, 2.55) |
| 1-03 | 133 | 281.2 | 1 | nobody | ch74 | The nation's state — build | - | re-aim onto Peggy (0.7 m away) at (1.2, -3.35) |
| 1-03 | 134 | 289.8 | 1 | nobody | ch74 | Verse 3 climax — hit | - | re-aim onto Peggy (0.7 m away) at (1.2, -3.35) |
| 1-03 | 134 | 289.8 | 1 | nobody | ch93 | Verse 3 climax — hit | - | re-aim onto Mulligan (1.3 m away) at (1.2, 1.6) |
| 1-03 | 135 | 296.4 | 1 | nobody | ch74 | Final chorus — full | - | re-aim onto Peggy (0.7 m away) at (1.2, -3.35) |
| 1-05 | 164 | 91.5 | 1 | named |  | Angelica rebuffs Burr | Burr | re-aim ch50 (glp-x4) onto Burr at (-3.86, 4.29) |
| 1-05 | 174.5 | 181.2 | 1 | nobody | ch91 | BUTTON — bump | - | re-aim onto Angelica (1.4 m away) at (-2.86, 3.34) |
| 1-05 | 174.5 | 181.2 | 2 | nobody | ch91 | BUTTON — bump | - | re-aim onto Angelica (1.2 m away) at (-2.86, 3.34) |
| 1-10 | 301.2 | 49.48 | 1 | named |  | Angelica crosses | Angelica | re-aim ch14 (mac-viper) onto Angelica at (2.1, -1.6) |
| 1-11 | 324 | 1.02 | 1 | named |  | Reception - Laurens calls the toast | Laurens | swap: free Viper ch92 (down 82 deg) onto Laurens at (-1.59, 1.66) |
| 1-11 | 326 | 9.62 | 1 | named |  | Angelica - maid of honour | Angelica | swap: free Viper ch93 (down 89 deg) onto Angelica at (0.0, 3.3) |
| 1-11 | 332 | 39.26 | 1 | named |  | Isolate Angelica | Angelica | swap: free Viper ch93 (down 89 deg) onto Angelica at (0.0, 3.3) |
| 1-11 | 370 | 79.77 | 1 | named |  | First sight of Hamilton | Hamilton | re-aim ch14 (mac-viper) onto Hamilton at (-3.2, 3.0) |
| 1-11 | 372 | 130.4 | 1 | named |  | Angelica's rap | Angelica | re-aim ch14 (mac-viper) onto Angelica at (-0.2, 3.7) |
| 1-11 | 386 | 296.68 | 1 | nobody | ch48 | Company echoes - beams | - | re-aim onto Peggy (1.1 m away) at (-1.84, 3.31) |
| 1-11 | 386 | 296.68 | 1 | nobody | ch51 | Company echoes - beams | - | re-aim onto Laurens (1.1 m away) at (1.84, 3.31) |
| 1-11 | 387 | 313.22 | 1 | named |  | Angelica alone - last lines | Angelica | re-aim ch14 (mac-viper) onto Angelica at (0.0, 3.6) |
| 1-12 | 400 | 0 | 1 | nobody | ch7 | Story of Tonight reprise — night tavern: blue room | - | re-aim onto Laurens (1.5 m away) at (-1.0, 2.7) |
| 1-12 | 400 | 0 | 1 | nobody | ch9 | Story of Tonight reprise — night tavern: blue room | - | re-aim onto Lafayette (1.4 m away) at (1.0, 2.6) |
| 1-12 | 402 | 38.6 | 1 | nobody | ch10 | Toast tag — back in to the table | - | re-aim onto Lafayette (1.3 m away) at (1.0, 2.6) |
| 1-12 | 402 | 38.6 | 1 | nobody | ch9 | Toast tag — back in to the table | - | re-aim onto Lafayette (1.4 m away) at (1.0, 2.6) |
| 1-14 | 443 | 105 | 1 | named |  | Washington relieves Lee | Washington | re-aim ch18 (mac-viper) onto Washington at (1.2, -3.35) |
| 1-18 | 562 | 34.2 | 1 | named |  | Lafayette enters — the cathedral of beams | Lafayette | re-aim ch20 (mac-viper) onto Lafayette at (0.0, 2.1) |
| 1-18 | 562 | 34.2 | 2 | named |  | Lafayette enters — the cathedral of beams | Lafayette | re-aim ch16 (mac-viper) onto Lafayette at (0.0, 2.1) |
| 1-18 | 563 | 42.3 | 1 | named |  | Lafayette to France — the fan opens | Lafayette | re-aim ch10 (mac-viper) onto Lafayette at (-0.97, 2.8) |
| 1-18 | 566 | 59.2 | 1 | named |  | Lafayette asks Washington for Hamilton — his speci | Lafayette | swap: free Viper ch8 (down 77 deg) onto Lafayette at (1.4, 1.6) |
| 1-20 | 586 | 0 | 1 | named |  | Yorktown — Hamilton on the box | Hamilton | re-aim ch49 (glp-x4) onto Hamilton at (0.0, 4.7) |
| 1-20 | 592 | 51.2 | 1 | named |  | Hamilton alone — facing death | Hamilton | re-aim ch98 (mac-viper) onto Hamilton at (0.0, 4.55) |
| 1-20 | 593 | 61.2 | 1 | named |  | Thinking of Eliza — warm | Eliza | hand: ch25 (10th Electric) takes Eliza on the gallery (ch97 stops on the gallery rail) |
| 1-20 | 597 | 90.4 | 1 | named |  | The friends' fortunes — Hamilton narrates | Hamilton | swap: free Viper ch93 (down 88 deg) onto Hamilton at (0.05, 3.0) |
| 1-20 | 599 | 109.9 | 1 | named |  | Mulligan enters — the tailor-spy | Mulligan | swap: free Viper ch93 (down 86 deg) onto Mulligan at (0.0, 3.6) |
| 1-20 | 600 | 120.1 | 1 | named |  | Mulligan — the rally | Mulligan | swap: free Viper ch8 (down 73 deg) onto Mulligan at (0.0, 3.6) |
| 1-23 | 640 | 125.3 | 1 | named |  | Midnight at Burr's — DR | Burr | swap: free Viper ch6 (down 72 deg) onto Burr at (-3.2, 3.6) |
| 1-23 | 656 | 312.5 | 1 | named |  | Washington's offer — the company asks | Washington | swap: free Viper ch8 (down 84 deg) onto Washington at (0.53, 1.32) |
| 1-23 | 661 | 349.8 | 1 | named |  | Washington joins the counterpoint | Washington | tried ch18 (stops on the SL gallery rail, taken back); pass 2 swapped ch100 |
| 1-23 | 661 | 349.8 | 2 | named |  | Washington joins the counterpoint | Washington | swap: free Viper ch100 (down 55 deg) onto Washington at (4.9, -1.5) |
| 1-23 | 665 | 368.7 | 1 | nobody | ch7 | My Shot — the beams fan | - | re-aim onto Burr (1.3 m away) at (1.8, 4.7) |
| 1-23 | 666 | 374 | 1 | nobody | ch7 | Hamilton's name — DSC | Hamilton | re-aim onto Burr (1.3 m away) at (1.8, 4.7) |
| 2-01 | 726 | 60.8 | 1 | named |  | Vamp - Jefferson strides down, beams turn | Jefferson | re-aim ch75 (vl3500) onto Jefferson at (3.7, -2.78) |
| 2-01 | 726 | 60.8 | 2 | named |  | Vamp - Jefferson strides down, beams turn | Jefferson | re-aim ch75 (vl3500) onto Jefferson at (3.7, -2.78) |
| 2-01 | 733 | 153.9 | 1 | named |  | Madison enters DL - special | Madison | re-aim ch6 (mac-viper) onto Madison at (-3.5, 3.4) |
| 2-01 | 737 | 208.3 | 1 | named |  | Company welcome - Hamilton DR | Hamilton | re-aim ch75 (vl3500) onto Hamilton at (1.85, 4.0) |
| 2-02 | 742 | 13 | 1 | named |  | The question set - debaters DSC, Washington SL | Washington | re-aim ch75 (vl3500) onto Washington at (1.0, -1.4) |
| 2-02 | 750 | 78.6 | 1 | named |  | Washington - back to the meeting | Washington | re-aim ch75 (vl3500) onto Washington at (0.85, -1.0) |
| 2-02 | 753 | 107.4 | 1 | nobody | ch92 | The slavery charge - stark white | - | re-aim onto Hamilton (1.3 m away) at (0.2, 3.2) |
| 2-02 | 756 | 128.9 | 1 | named |  | Hamilton turns on Jefferson and Madison | Madison | re-aim ch72 (vl3500) onto Madison at (-3.0, 2.2) |
| 2-02 | 759 | 146.4 | 1 | named |  | Washington stops it - battle over | Washington | re-aim ch72 (vl3500) onto Washington at (0.0, 1.4) |
| 2-03 | 765 | 19.5 | 1 | named |  | Hamilton at his desk - letter | Hamilton | re-aim ch72 (vl3500) onto Hamilton at (-1.5, 1.4) |
| 2-03 | 776 | 161.5 | 1 | named |  | Angelica's news - tempo returns | Angelica | re-aim ch75 (vl3500) onto Angelica at (3.09, -1.93) |
| 2-03 | 776 | 161.5 | 2 | named |  | Angelica's news - tempo returns | Angelica | re-aim ch72 (vl3500) onto Angelica at (3.09, -1.93) |
| 2-03 | 778 | 181.1 | 1 | named |  | Angelica arrives - full summer warmth | Angelica | re-aim ch75 (vl3500) onto Angelica at (2.3, 2.6) |
| 2-03 | 779.5 | 270.5 | 1 | named |  | Hamilton alone at the desk | Hamilton | re-aim ch72 (vl3500) onto Hamilton at (-1.5, 1.4) |
| 2-04 | 806 | 130.9 | 1 | named |  | James Reynolds' letter - cold special | James Reynolds | re-aim ch74 (vl3500) onto James Reynolds at (-2.7, 3.8) |
| 2-05 | 866 | 50.06 | 1 | nobody | ch13 | Company vocal | - | re-aim onto Hamilton (1.3 m away) at (0.0, -0.65) |
| 2-05 | 867.2 | 114.3 | 1 | named |  | Jefferson set the dinner - table lifts | Jefferson | re-aim ch94 (mac-viper) onto Jefferson at (0.26, 1.18) |
| 2-05 | 867.5 | 143.9 | 1 | named |  | Madison weighs it - DSR | Madison | re-aim ch59 (glp-x4) onto Madison at (-3.0, 3.7) |
| 2-05 | 868 | 193.8 | 1 | nobody | ch13 | Click Boom | - | re-aim onto Hamilton (1.3 m away) at (0.0, -0.65) |
| 2-05 | 870 | 196.3 | 1 | nobody | ch13 | to the Table | - | re-aim onto Hamilton (1.3 m away) at (0.0, -0.65) |
| 2-05 | 872 | 198.9 | 1 | named |  | Burr/ Ham DR | Hamilton | re-aim ch13 (mac-viper) onto Hamilton at (-3.2, 2.9) |
| 2-05 | 876 | 243.6 | 1 | named |  | Burr MC/ Music slow | Burr | re-aim ch13 (mac-viper) onto Burr at (0.0, 2.4) |
| 2-05 | 876.1 | 256.6 | 1 | nobody | ch13 | PD | - | re-aim onto Hamilton (1.3 m away) at (0.0, -0.65) |
| 2-07 | 943 | 0 | 1 | named |  | Cabinet Battle #2 — Washington calls the cabinet,  | Washington | re-aim ch50 (glp-x4) onto Washington at (0.0, 0.95) |
| 2-07 | 944 | 12.4 | 1 | named |  | Washington centre — hands the debate to Jefferson | Jefferson | re-aim ch51 (glp-x4) onto Jefferson at (-1.9, 1.9) |
| 2-07 | 950 | 76 | 1 | named |  | Washington turns to Hamilton — back to the blue | Hamilton | re-aim ch47 (glp-x4) onto Hamilton at (2.3, 2.2) |
| 2-08 | 969 | 97.1 | 1 | named |  | Madison and Jefferson drive — the floor turns | Jefferson | swap: free Viper ch92 (down 85 deg) onto Jefferson at (-1.37, 2.87) |
| 2-08 | 970 | 107.1 | 2 | named |  | Jefferson's decision — a white shaft | Jefferson | swap: free Viper ch93 (down 88 deg) onto Jefferson at (-0.15, 3.0) |
| 2-09 | 979 | 0 | 1 | named |  | One Last Time — Washington's office, warm room, co | Washington | swap: free Viper ch13 (down 86 deg) onto Washington at (-0.37, 0.24) |
| 2-09 | 998 | 266 | 1 | named |  | Washington heads upstage | Washington | re-aim ch13 (mac-viper) onto Washington at (0.41, 1.64) |
| 2-10 | 1003 | 0 | 1 | named |  | I Know Him — dark navy, the King to come | King George | re-aim ch61 (glp-x4) onto King George at (0.16, -0.95) |
| 2-11 | 1012 | 25.37 | 1 | named |  | Hamilton fired - stark white side light | Hamilton | swap: free Viper ch25 (down 83 deg) onto Hamilton at (0.0, -3.2) |
| 2-11 | 1015 | 37.63 | 1 | named |  | Jefferson/Madison/Burr gloat - amber | Jefferson | re-aim ch61 (glp-x4) onto Jefferson at (-0.8, 2.2) |
| 2-11 | 1015 | 37.63 | 1 | named |  | Jefferson/Madison/Burr gloat - amber | Madison | re-aim ch58 (glp-x4) onto Madison at (-1.8, 1.6) |
| 2-12 | 1019 | 21.08 | 1 | named |  | Jefferson accuses - side light hardens | Jefferson | swap: free Viper ch94 (down 84 deg) onto Jefferson at (0.7, 1.9) |
| 2-14 | 1045 | 55.49 | 1 | named |  | Angelica arrives | Angelica | re-aim ch48 (glp-x4) onto Angelica at (0.9, 3.2) |
| 2-14 | 1046 | 65.52 | 1 | named |  | Angelica turns to Eliza - two pools | Angelica | re-aim ch94 (mac-viper) onto Angelica at (0.6, 3.1) |
| 2-14 | 1046.5 | 81.17 | 1 | named |  | Angelica - climax | Angelica | re-aim ch50 (glp-x4) onto Angelica at (0.1, 3.05) |
| 2-16 | 1066 | 1.72 | 1 | named |  | Blow Us All Away - Philip, warm amber party | Philip | re-aim ch61 (glp-x4) onto Philip at (0.0, 2.8) |
| 2-16 | 1068 | 27.24 | 1 | named |  | Philip and the ladies - warm, DS keys | Philip | re-aim ch62 (glp-x4) onto Philip at (-1.6, 2.4) |
| 2-16 | 1069 | 40.1 | 1 | named |  | Off to the play - Philip DS | Philip | re-aim ch62 (glp-x4) onto Philip at (-1.6, 2.4) |
| 2-16 | 1071 | 51.79 | 1 | named |  | The theatre - footlights, Eacker's box | George Eacker | swap: free Viper ch95 (down 61 deg) onto George Eacker at (4.9, 2.5) |
| 2-16 | 1072 | 59.39 | 1 | named |  | Philip confronts Eacker - two pools | George Eacker | swap: free Viper ch95 (down 61 deg) onto George Eacker at (4.9, 2.5) |
| 2-16 | 1073 | 64.82 | 1 | named |  | Eacker insults Hamilton - cold edge | George Eacker | swap: free Viper ch95 (down 61 deg) onto George Eacker at (4.9, 2.5) |
| 2-16 | 1076 | 80.94 | 1 | named |  | Hamilton's office - warm night | Hamilton | re-aim ch62 (glp-x4) onto Hamilton at (-1.4, 1.2) |
| 2-18 | 1129 | 96.2 | 1 | named |  | Instrumental - Hamilton DSC, all else recedes | Hamilton | re-aim ch74 (vl3500) onto Hamilton at (0.3, 2.45) |
| 2-19 | 1154 | 50.28 | 1 | named |  | Burr's vamp - warm side colour | Burr | re-aim ch57 (glp-x4) onto Burr at (0.62, 1.1) |
| 2-19 | 1155 | 65.05 | 1 | named |  | Burr's campaign - warm floor and steel shafts | Burr | re-aim ch99 (mac-viper) onto Burr at (0.0, 0.95) |
| 2-19 | 1165 | 152.37 | 1 | named |  | Up to Hamilton - bump to centre | Hamilton | re-aim ch54 (glp-x4) onto Hamilton at (0.0, -3.35) |
| 2-19 | 1166 | 157.94 | 1 | named |  | Hamilton's endorsement - Hamilton DSC, company in  | Hamilton | re-aim ch74 (vl3500) onto Hamilton at (0.0, -3.35) |
| 2-19 | 1167 | 184.92 | 1 | named |  | Verdict on Burr - snap | Burr | re-aim ch74 (vl3500) onto Burr at (4.2, -1.6) |
| 2-19 | 1167 | 184.92 | 2 | named |  | Verdict on Burr - snap | Burr | swap: free Viper ch100 (down 72 deg) onto Burr at (4.2, -1.6) |
| 2-19 | 1168 | 187.73 | 1 | named |  | Jefferson wins - the company erupts | Jefferson | re-aim ch54 (glp-x4) onto Jefferson at (-0.5, 3.4) |
| 2-22 | 1241 | 71.42 | 1 | named |  | Burr's suspicion - Hamilton isolated | Burr | re-aim ch53 (glp-x4) onto Burr at (-0.03, 1.0) |
| 2-22 | 1262 | 174.5 | 1 | named |  | ELIZA | Eliza | re-aim ch12 (mac-viper) onto Eliza at (-0.14, 0.62) |
| 2-22 | 1262.1 | 174.5 | 2 | named |  | ELIZA - the specials on their people | Eliza | re-aim ch63 (glp-x4) onto Eliza at (-0.14, 0.62) |
| 2-23 | 1274 | 16.76 | 1 | named |  | Jefferson's tribute - DSR special | Jefferson | re-aim ch74 (vl3500) onto Jefferson at (-4.5, -0.45) |
| 2-23 | 1280 | 56.84 | 1 | named |  | All turn to Eliza | Eliza | re-aim ch96 (mac-viper) onto Eliza at (-0.03, 2.59) |
| 2-23 | 1280 | 56.84 | 2 | named |  | All turn to Eliza | Eliza | re-aim ch96 (mac-viper) onto Eliza at (-0.03, 2.59) |
