# Johnny Tremain — the light plot (Theatre 2)

Written by `tools/jt-rig.py` from the same data as `assets/johnny-tremain/rig.json` — edit the script, not this file. The QLC+ workspace is `assets/johnny-tremain/qlc/johnny-tremain.qxw` (`tools/jt-qlc.py`; how to open it: [`assets/johnny-tremain/qlc/README.md`](../../assets/johnny-tremain/qlc/README.md)). The brief is [LIGHTING-NEEDS.md](LIGHTING-NEEDS.md). In the page: the **T2 rig** header button, or `MIDTOWN.jtLights`.

World metres (stage → world: x + 20.00, y + 0.80, z + 2.30). "Stage" columns are the stage frame: +x stage right, z upstage of the proscenium plane, y over the deck. Units are numbered stage left → stage right (low x first), booms bottom → top.

## The rig in numbers

| fixture | QLC+ definition (manufacturer / model / mode) | ch | units |
|---|---|---|---|
| ETC ColorSource Spot | ETC / ColorSource Spot / 5-Channel | 5 | 34 |
| ETC Source Four LED Series 2 Lustr | ETC / Source Four LED Series 2 Lustr / Direct | 10 | 30 |
| ETC ColorSource PAR | ETC / ColorSource PAR / 5-channel | 5 | 24 |
| practical on a dimmer | Generic / Generic / 1 Channel | 1 | 14 |
| Martin MAC Encore Performance CLD | Martin / MAC Encore Performance / CLD | 38 | 6 |
| Chauvet Ovation CYC 1 FC (ground row) | Chauvet / Ovation CYC 1 FC / 7 Channel | 7 | 6 |
| Chauvet Ovation CYC 1 FC | Chauvet / Ovation CYC 1 FC / 7 Channel | 7 | 4 |
| Martin MAC Aura | Martin / MAC Aura / Standard | 14 | 4 |
| ETC Source Four 750 W (tungsten) on a dimmer | Generic / Generic / 1 Channel | 1 | 2 |
| Robert Juliat D'Artagnan 934SNX followspot | Robert Juliat / D'Artagnan 934SNX / 1 (1 channel) | 1 | 2 |
| MDG ATMe hazer | MDG / ATMe / 3 Channel | 3 | 2 |

**128 units** (114 instruments, 14 practicals); universe 1 uses 479 channels, universe 2 489. Every definition ships with QLC+ (checked against the library's own .qxf files) or is a Generic dimmer: **no custom fixture files are needed.**

## Positions

| position | where (world) | units | what hangs there |
|---|---|---|---|
| FOH 1 — the bridge | x 15.20…24.60, y 6.95, z -3.15 | 19 | 17 × ETC Source Four LED Series 2 Lustr, 2 × Martin MAC Encore Performance CLD |
| FOH 2 — behind the bridge | x 15.60…23.40, y 7.20, z -5.20 | 7 | 7 × ETC Source Four LED Series 2 Lustr |
| Box boom house right | x 14.15, y 3.00…5.40, z -2.50 | 3 | 3 × ETC Source Four LED Series 2 Lustr |
| Box boom house left | x 26.25, y 3.00…5.40, z -2.50 | 3 | 3 × ETC Source Four LED Series 2 Lustr |
| Pros boom house right | x 14.80, y 3.00, z 0.60 | 1 | 1 × ETC ColorSource Spot |
| Pros boom house left | x 25.50, y 3.00, z 0.60 | 1 | 1 × ETC ColorSource Spot |
| 1st Electric | x 15.00…25.00, y 8.50, z 2.90 | 11 | 2 × Martin MAC Encore Performance CLD, 6 × ETC ColorSource PAR, 1 × ETC Source Four 750 W (tungsten) on a dimmer, 2 × ETC ColorSource Spot |
| 2nd Electric | x 15.00…25.00, y 8.50, z 4.70 | 12 | 2 × Martin MAC Encore Performance CLD, 6 × ETC ColorSource PAR, 1 × ETC Source Four 750 W (tungsten) on a dimmer, 3 × ETC ColorSource Spot |
| 3rd Electric | x 15.60…23.80, y 10.10, z 6.50 | 8 | 7 × ETC ColorSource PAR, 1 × ETC ColorSource Spot |
| 4th Electric | x 14.60…25.40, y 11.60, z 8.00 | 14 | 4 × Chauvet Ovation CYC 1 FC, 4 × Martin MAC Aura, 4 × ETC ColorSource PAR, 2 × ETC ColorSource Spot |
| SL boom 1 (in 1) | x 13.80, y 1.20…4.20, z 3.40 | 4 | 4 × ETC ColorSource Spot |
| SL boom 2 (in 2) | x 13.80, y 1.20…4.80, z 5.60 | 5 | 5 × ETC ColorSource Spot |
| SL boom 3 (in 3) | x 13.80, y 1.20…3.40, z 7.60 | 4 | 4 × ETC ColorSource Spot |
| SR boom 1 (in 1, the pocket) | x 25.45, y 2.20…3.40, z 3.10 | 2 | 2 × ETC ColorSource Spot |
| SR boom 2 (in 2) | x 26.20, y 1.20…4.80, z 5.60 | 4 | 4 × ETC ColorSource Spot |
| SR boom 3 (in 3) | x 26.20, y 1.20…4.80, z 7.60 | 4 | 4 × ETC ColorSource Spot |
| Ground row (the back brick) | x 15.50…24.50, y 0.80, z 8.65 | 6 | 6 × Chauvet Ovation CYC 1 FC (ground row) |
| Floor (behind the bellows) | x 16.20, y 0.80, z 5.85 | 1 | 1 × ETC ColorSource PAR |
| Backstage corridor, through the stage doors | x 20.00, y 3.00, z 10.50 | 1 | 1 × ETC ColorSource Spot |
| Theatre 2's followspot booth | x 17.80…22.20, y 3.28, z -14.90 | 2 | 2 × Robert Juliat D'Artagnan 934SNX followspot |
| SL wing, upstage (floor) | x 11.30, y 0.80, z 8.30 | 1 | 1 × MDG ATMe hazer |
| SR wing, upstage (floor) | x 28.80, y 0.80, z 8.30 | 1 | 1 × MDG ATMe hazer |
| Practicals | x 16.60…22.85, y 1.10…4.70, z 2.60…8.80 | 14 | 14 × practical on a dimmer |

The electrics hang on cross-stage pipes x 13.8…26.2 at 8.5 (1st, 2nd), 10.1 (3rd) and 11.6 (4th): over the venue's iron (5.9–6.2) and high enough that the front row does not see them through the arch, under the header or over the masking border (`MIDTOWN.jtLights.check()` proves it from six seats). No unit hangs over the iron's centre walkway (x 19.2…21.1). Nothing stands in either lift's travel (front x 17…23, z 2.6…5.0; back x 17.5…22.5, z 5.9…8.3; y −4.4…5.2).

## Patch sheet (address order)

| U | address | ch | unit | position | fixture | mode | purpose | colour |
|---|---|---|---|---|---|---|---|---|
| 1 | 1–10 | 1 | BR-01 | FOH 1 — the bridge | ETC Source Four LED Series 2 Lustr | Direct | Loft isolation, front (S11) | LED colour mix |
| 1 | 11–20 | 2 | BR-02 | FOH 1 — the bridge | ETC Source Four LED Series 2 Lustr | Direct | Narrator DSL (S2) | LED colour mix |
| 1 | 21–30 | 3 | BR-03 | FOH 1 — the bridge | ETC Source Four LED Series 2 Lustr | Direct | Front light APL | LED colour mix |
| 1 | 31–40 | 4 | BR-04 | FOH 1 — the bridge | ETC Source Four LED Series 2 Lustr | Direct | Shop door 1 slice (S27) | LED colour mix |
| 1 | 41–50 | 5 | BR-05 | FOH 1 — the bridge | ETC Source Four LED Series 2 Lustr | Direct | Front light DSL | LED colour mix |
| 1 | 51–60 | 6 | BR-06 | FOH 1 — the bridge | ETC Source Four LED Series 2 Lustr | Direct | Cup at the gravestone (S7) | LED, cool white for the cups |
| 1 | 61–70 | 7 | BR-07 | FOH 1 — the bridge | ETC Source Four LED Series 2 Lustr | Direct | Lavinia, rosy lift (S13) | LED colour mix |
| 1 | 71–80 | 8 | BR-08 | FOH 1 — the bridge | ETC Source Four LED Series 2 Lustr | Direct | Shop door 2 slice (S27) | LED colour mix |
| 1 | 81–90 | 9 | BR-09 | FOH 1 — the bridge | ETC Source Four LED Series 2 Lustr | Direct | Front light APC | LED colour mix |
| 1 | 91–100 | 10 | BR-10 | FOH 1 — the bridge | ETC Source Four LED Series 2 Lustr | Direct | Cups on the courtroom table (S6) | LED, cool white for the cups |
| 1 | 101–110 | 11 | BR-11 | FOH 1 — the bridge | ETC Source Four LED Series 2 Lustr | Direct | Front light DSC | LED colour mix |
| 1 | 111–120 | 12 | BR-12 | FOH 1 — the bridge | ETC Source Four LED Series 2 Lustr | Direct | Shop door 3 slice (S27) | LED colour mix |
| 1 | 121–130 | 13 | BR-13 | FOH 1 — the bridge | ETC Source Four LED Series 2 Lustr | Direct | Cup pin, the wharf's lip (S4) | LED, cool white for the cups |
| 1 | 131–140 | 14 | BR-14 | FOH 1 — the bridge | ETC Source Four LED Series 2 Lustr | Direct | Front light APR | LED colour mix |
| 1 | 141–150 | 15 | BR-15 | FOH 1 — the bridge | ETC Source Four LED Series 2 Lustr | Direct | Shop door 4 slice (S27) | LED colour mix |
| 1 | 151–160 | 16 | BR-16 | FOH 1 — the bridge | ETC Source Four LED Series 2 Lustr | Direct | Front light DSR | LED colour mix |
| 1 | 161–170 | 17 | BR-17 | FOH 1 — the bridge | ETC Source Four LED Series 2 Lustr | Direct | Narrator DSR (S1) | LED colour mix |
| 1 | 171–180 | 18 | F2-01 | FOH 2 — behind the bridge | ETC Source Four LED Series 2 Lustr | Direct | Front light SHOP | LED colour mix |
| 1 | 181–190 | 19 | F2-02 | FOH 2 — behind the bridge | ETC Source Four LED Series 2 Lustr | Direct | Front light MSL | LED colour mix |
| 1 | 191–200 | 20 | F2-03 | FOH 2 — behind the bridge | ETC Source Four LED Series 2 Lustr | Direct | Front light LOFT | LED colour mix |
| 1 | 201–210 | 21 | F2-04 | FOH 2 — behind the bridge | ETC Source Four LED Series 2 Lustr | Direct | Front light MSC | LED colour mix |
| 1 | 211–220 | 22 | F2-05 | FOH 2 — behind the bridge | ETC Source Four LED Series 2 Lustr | Direct | Front light PATH | LED colour mix |
| 1 | 221–230 | 23 | F2-06 | FOH 2 — behind the bridge | ETC Source Four LED Series 2 Lustr | Direct | Front light WHARF | LED colour mix |
| 1 | 231–240 | 24 | F2-07 | FOH 2 — behind the bridge | ETC Source Four LED Series 2 Lustr | Direct | Front light MSR | LED colour mix |
| 1 | 241–250 | 25 | BBHR-1 | Box boom house right | ETC Source Four LED Series 2 Lustr | Direct | Side-front APR | LED colour mix |
| 1 | 251–260 | 26 | BBHR-2 | Box boom house right | ETC Source Four LED Series 2 Lustr | Direct | Side-front DSR | LED colour mix |
| 1 | 261–270 | 27 | BBHR-3 | Box boom house right | ETC Source Four LED Series 2 Lustr | Direct | Side-front MSR | LED colour mix |
| 1 | 271–280 | 28 | BBHL-1 | Box boom house left | ETC Source Four LED Series 2 Lustr | Direct | Side-front APL | LED colour mix |
| 1 | 281–290 | 29 | BBHL-2 | Box boom house left | ETC Source Four LED Series 2 Lustr | Direct | Side-front DSL | LED colour mix |
| 1 | 291–300 | 30 | BBHL-3 | Box boom house left | ETC Source Four LED Series 2 Lustr | Direct | Side-front MSL | LED colour mix |
| 1 | 301–305 | 31 | PB-L | Pros boom house right | ETC ColorSource Spot | 5-Channel | Apron side light from SL | LED colour mix |
| 1 | 306–310 | 32 | PB-R | Pros boom house left | ETC ColorSource Spot | 5-Channel | Apron side light from SR | LED colour mix |
| 1 | 311–315 | 33 | E1-02 | 1st Electric | ETC ColorSource PAR | 5-channel | Top light DSL | LED colour mix |
| 1 | 316–316 | 34 | E1-03 | 1st Electric | ETC Source Four 750 W (tungsten) on a dimmer | 1 Channel | Jail bars (S15) | L202 half CTB, bars gobo |
| 1 | 317–321 | 35 | E1-04 | 1st Electric | ETC ColorSource PAR | 5-channel | Back light APL | LED colour mix |
| 1 | 322–326 | 36 | E1-05 | 1st Electric | ETC ColorSource Spot | 5-Channel | The eight eyes: tight cold top (S28) | LED colour mix |
| 1 | 327–331 | 37 | E1-06 | 1st Electric | ETC ColorSource PAR | 5-channel | Top light DSC | LED colour mix |
| 1 | 332–336 | 38 | E1-07 | 1st Electric | ETC ColorSource PAR | 5-channel | Back light APC | LED colour mix |
| 1 | 337–341 | 39 | E1-08 | 1st Electric | ETC ColorSource Spot | 5-Channel | Lantern reveal: the wig (S24) | LED colour mix |
| 1 | 342–346 | 40 | E1-09 | 1st Electric | ETC ColorSource PAR | 5-channel | Back light APR | LED colour mix |
| 1 | 347–351 | 41 | E1-10 | 1st Electric | ETC ColorSource PAR | 5-channel | Top light DSR | LED colour mix |
| 1 | 352–356 | 42 | E2-02 | 2nd Electric | ETC ColorSource PAR | 5-channel | Top light MSL | LED colour mix |
| 1 | 357–357 | 43 | E2-03 | 2nd Electric | ETC Source Four 750 W (tungsten) on a dimmer | 1 Channel | The cups on the sideboard, shuttered strip (S5) | L202 half CTB, shuttered 1.8 × 0.4 |
| 1 | 358–362 | 44 | E2-04 | 2nd Electric | ETC ColorSource PAR | 5-channel | Back light DSL | LED colour mix |
| 1 | 363–367 | 45 | E2-05 | 2nd Electric | ETC ColorSource Spot | 5-Channel | The sheet, backlit (S32) | LED colour mix |
| 1 | 368–372 | 46 | E2-06 | 2nd Electric | ETC ColorSource PAR | 5-channel | Top light MSC | LED colour mix |
| 1 | 373–377 | 47 | E2-07 | 2nd Electric | ETC ColorSource PAR | 5-channel | Back light DSC | LED colour mix |
| 1 | 378–382 | 48 | E2-08 | 2nd Electric | ETC ColorSource Spot | 5-Channel | Lantern reveal: the tipped chair (S24) | LED colour mix |
| 1 | 383–387 | 49 | E2-09 | 2nd Electric | ETC ColorSource PAR | 5-channel | Back light DSR | LED colour mix |
| 1 | 388–392 | 50 | E2-10 | 2nd Electric | ETC ColorSource Spot | 5-Channel | Lantern reveal: the dressing table (S24) | LED colour mix |
| 1 | 393–397 | 51 | E2-11 | 2nd Electric | ETC ColorSource PAR | 5-channel | Top light MSR | LED colour mix |
| 1 | 398–402 | 52 | E3-01 | 3rd Electric | ETC ColorSource PAR | 5-channel | Top light LOFT, SL half (S11) | LED colour mix |
| 1 | 403–407 | 53 | E3-02 | 3rd Electric | ETC ColorSource PAR | 5-channel | Top light LOFT, SR half and the ladder head (S11) | LED colour mix |
| 1 | 408–412 | 54 | E3-03 | 3rd Electric | ETC ColorSource PAR | 5-channel | Back light MSL | LED colour mix |
| 1 | 413–417 | 55 | E3-04 | 3rd Electric | ETC ColorSource PAR | 5-channel | Top light PATH | LED colour mix |
| 1 | 418–422 | 56 | E3-05 | 3rd Electric | ETC ColorSource PAR | 5-channel | Back light MSC | LED colour mix |
| 1 | 423–427 | 57 | E3-06 | 3rd Electric | ETC ColorSource Spot | 5-Channel | Steeple lanterns pin (S22) | LED colour mix |
| 1 | 428–432 | 58 | E3-07 | 3rd Electric | ETC ColorSource PAR | 5-channel | Top light WHARF | LED colour mix |
| 1 | 433–437 | 59 | E3-08 | 3rd Electric | ETC ColorSource PAR | 5-channel | Back light MSR | LED colour mix |
| 1 | 438–442 | 60 | E4-03 | 4th Electric | ETC ColorSource PAR | 5-channel | Back light LOFT | LED colour mix |
| 1 | 443–447 | 61 | E4-04 | 4th Electric | ETC ColorSource Spot | 5-Channel | Otis at the rafters (S12) | LED colour mix |
| 1 | 448–452 | 62 | E4-07 | 4th Electric | ETC ColorSource Spot | 5-Channel | Rab at the back: soft cool backlight (S33) | LED colour mix |
| 1 | 453–457 | 63 | E4-08 | 4th Electric | ETC ColorSource PAR | 5-channel | Back light PATH | LED colour mix |
| 1 | 458–462 | 64 | E4-11 | 4th Electric | ETC ColorSource PAR | 5-channel | Back light WHARF | LED colour mix |
| 1 | 463–467 | 65 | E4-12 | 4th Electric | ETC ColorSource PAR | 5-channel | The volley flash behind Johnny (S28), strobe | LED colour mix |
| 1 | 468–472 | 66 | FL-1 | Floor (behind the bellows) | ETC ColorSource PAR | 5-channel | Furnace glow on Johnny's face (S8) | LED colour mix |
| 1 | 473–477 | 67 | DR-1 | Backstage corridor, through the stage doors | ETC ColorSource Spot | 5-Channel | The doorway backlight (S14) | LED colour mix |
| 1 | 478–478 | 68 | FS-1 | Theatre 2's followspot booth | Robert Juliat D'Artagnan 934SNX followspot | 1 (1 channel) | Followspot (S3): Johnny anywhere, the aisle | LED colour mix |
| 1 | 479–479 | 69 | FS-2 | Theatre 2's followspot booth | Robert Juliat D'Artagnan 934SNX followspot | 1 (1 channel) | Followspot (S3): Johnny anywhere, the aisle | LED colour mix |
| 2 | 1–5 | 70 | SL1-1 | SL boom 1 (in 1) | ETC ColorSource Spot | 5-Channel | Side light DS from SL (shin) | LED colour mix |
| 2 | 6–10 | 71 | SL1-2 | SL boom 1 (in 1) | ETC ColorSource Spot | 5-Channel | Side light DS from SL (mid) | LED colour mix |
| 2 | 11–15 | 72 | SL1-3 | SL boom 1 (in 1) | ETC ColorSource Spot | 5-Channel | Side light DS from SL (head) | LED colour mix |
| 2 | 16–20 | 73 | SL1-4 | SL boom 1 (in 1) | ETC ColorSource Spot | 5-Channel | The SL in-1 doorway (S14) | LED colour mix |
| 2 | 21–25 | 74 | SL2-1 | SL boom 2 (in 2) | ETC ColorSource Spot | 5-Channel | Side light MS from SL (shin) | LED colour mix |
| 2 | 26–30 | 75 | SL2-2 | SL boom 2 (in 2) | ETC ColorSource Spot | 5-Channel | Side light MS from SL (mid) | LED colour mix |
| 2 | 31–35 | 76 | SL2-3 | SL boom 2 (in 2) | ETC ColorSource Spot | 5-Channel | Side light MS from SL (head) | LED colour mix |
| 2 | 36–40 | 77 | SL2-4 | SL boom 2 (in 2) | ETC ColorSource Spot | 5-Channel | Bucket, boy and furnace isolation (S10) | LED colour mix |
| 2 | 41–45 | 78 | SL2-5 | SL boom 2 (in 2) | ETC ColorSource Spot | 5-Channel | Window light through the window flat (S16) | LED colour mix |
| 2 | 46–50 | 79 | SL3-1 | SL boom 3 (in 3) | ETC ColorSource Spot | 5-Channel | Side light US from SL (shin) | LED colour mix |
| 2 | 51–55 | 80 | SL3-2 | SL boom 3 (in 3) | ETC ColorSource Spot | 5-Channel | Side light US from SL (mid) | LED colour mix |
| 2 | 56–60 | 81 | SL3-3 | SL boom 3 (in 3) | ETC ColorSource Spot | 5-Channel | Side light US from SL (head) | LED colour mix |
| 2 | 61–65 | 82 | SL3-4 | SL boom 3 (in 3) | ETC ColorSource Spot | 5-Channel | The crucible pour: hot low snap (S9) | LED colour mix |
| 2 | 66–70 | 83 | SR1-1 | SR boom 1 (in 1, the pocket) | ETC ColorSource Spot | 5-Channel | Side light DS from SR (mid) | LED colour mix |
| 2 | 71–75 | 84 | SR1-2 | SR boom 1 (in 1, the pocket) | ETC ColorSource Spot | 5-Channel | Side light DS from SR (head) | LED colour mix |
| 2 | 76–80 | 85 | SR2-1 | SR boom 2 (in 2) | ETC ColorSource Spot | 5-Channel | Side light MS from SR (shin) | LED colour mix |
| 2 | 81–85 | 86 | SR2-2 | SR boom 2 (in 2) | ETC ColorSource Spot | 5-Channel | Side light MS from SR (mid) | LED colour mix |
| 2 | 86–90 | 87 | SR2-3 | SR boom 2 (in 2) | ETC ColorSource Spot | 5-Channel | Side light MS from SR (head) | LED colour mix |
| 2 | 91–95 | 88 | SR2-4 | SR boom 2 (in 2) | ETC ColorSource Spot | 5-Channel | Long low light from SR: dawn, sunset (S19, S20) | LED colour mix |
| 2 | 96–100 | 89 | SR3-1 | SR boom 3 (in 3) | ETC ColorSource Spot | 5-Channel | Side light US from SR (shin) | LED colour mix |
| 2 | 101–105 | 90 | SR3-2 | SR boom 3 (in 3) | ETC ColorSource Spot | 5-Channel | Side light US from SR (mid) | LED colour mix |
| 2 | 106–110 | 91 | SR3-3 | SR boom 3 (in 3) | ETC ColorSource Spot | 5-Channel | Side light US from SR (head) | LED colour mix |
| 2 | 111–115 | 92 | SR3-4 | SR boom 3 (in 3) | ETC ColorSource Spot | 5-Channel | Long low light from SR: dawn, sunset (S19, S20) | LED colour mix |
| 2 | 116–153 | 93 | BR-M1 | FOH 1 — the bridge | Martin MAC Encore Performance CLD | CLD | Water / boats from the house (S17, S31) | LED colour mix |
| 2 | 154–191 | 94 | BR-M2 | FOH 1 — the bridge | Martin MAC Encore Performance CLD | CLD | Water (S17) | LED colour mix |
| 2 | 192–229 | 95 | E1-01 | 1st Electric | Martin MAC Encore Performance CLD | CLD | Mover: leaves / window / the ride (S21, S29) | LED colour mix |
| 2 | 230–267 | 96 | E1-11 | 1st Electric | Martin MAC Encore Performance CLD | CLD | Mover: leaves / the ride (S21, S29) | LED colour mix |
| 2 | 268–305 | 97 | E2-01 | 2nd Electric | Martin MAC Encore Performance CLD | CLD | Mover: moon and cloud breakup (S18) | LED colour mix |
| 2 | 306–343 | 98 | E2-12 | 2nd Electric | Martin MAC Encore Performance CLD | CLD | Mover: moon breakup / the ride (S18, S29) | LED colour mix |
| 2 | 344–357 | 99 | E4-02 | 4th Electric | Martin MAC Aura | Standard | Wash mover: back light colour, the ride | LED colour mix |
| 2 | 358–371 | 100 | E4-06 | 4th Electric | Martin MAC Aura | Standard | Wash mover: back light colour, the ride | LED colour mix |
| 2 | 372–385 | 101 | E4-09 | 4th Electric | Martin MAC Aura | Standard | Wash mover: back light colour, the ride | LED colour mix |
| 2 | 386–399 | 102 | E4-13 | 4th Electric | Martin MAC Aura | Standard | Wash mover: back light colour, the ride | LED colour mix |
| 2 | 400–406 | 103 | E4-01 | 4th Electric | Chauvet Ovation CYC 1 FC | 7 Channel | Back brick wash from above (the sky) | LED RGBAL |
| 2 | 407–413 | 104 | E4-05 | 4th Electric | Chauvet Ovation CYC 1 FC | 7 Channel | Back brick wash from above (the sky) | LED RGBAL |
| 2 | 414–420 | 105 | E4-10 | 4th Electric | Chauvet Ovation CYC 1 FC | 7 Channel | Back brick wash from above (the sky) | LED RGBAL |
| 2 | 421–427 | 106 | E4-14 | 4th Electric | Chauvet Ovation CYC 1 FC | 7 Channel | Back brick wash from above (the sky) | LED RGBAL |
| 2 | 428–434 | 107 | GR-1 | Ground row (the back brick) | Chauvet Ovation CYC 1 FC (ground row) | 7 Channel | Back brick from below (the sky) | LED RGBAL |
| 2 | 435–441 | 108 | GR-2 | Ground row (the back brick) | Chauvet Ovation CYC 1 FC (ground row) | 7 Channel | Back brick from below (the sky) | LED RGBAL |
| 2 | 442–448 | 109 | GR-3 | Ground row (the back brick) | Chauvet Ovation CYC 1 FC (ground row) | 7 Channel | Back brick from below (the sky) | LED RGBAL |
| 2 | 449–455 | 110 | GR-4 | Ground row (the back brick) | Chauvet Ovation CYC 1 FC (ground row) | 7 Channel | Back brick from below (the sky) | LED RGBAL |
| 2 | 456–462 | 111 | GR-5 | Ground row (the back brick) | Chauvet Ovation CYC 1 FC (ground row) | 7 Channel | Back brick from below (the sky) | LED RGBAL |
| 2 | 463–469 | 112 | GR-6 | Ground row (the back brick) | Chauvet Ovation CYC 1 FC (ground row) | 7 Channel | Back brick from below (the sky) | LED RGBAL |
| 2 | 470–472 | 113 | HZ-1 | SL wing, upstage (floor) | MDG ATMe hazer | 3 Channel | Haze | LED colour mix |
| 2 | 473–475 | 114 | HZ-2 | SR wing, upstage (floor) | MDG ATMe hazer | 3 Channel | Haze | LED colour mix |
| 2 | 476–476 | 115 | P-01 | Practicals | practical on a dimmer | 1 Channel | Furnace glow (orange LED, flicker) | fire |
| 2 | 477–477 | 116 | P-02 | Practicals | practical on a dimmer | 1 Channel | Hand lantern (radio dimmer) | lantern |
| 2 | 478–478 | 117 | P-03 | Practicals | practical on a dimmer | 1 Channel | Church lantern 1 (steeple) | candle |
| 2 | 479–479 | 118 | P-04 | Practicals | practical on a dimmer | 1 Channel | Church lantern 2 (steeple) | candle |
| 2 | 480–480 | 119 | P-05 | Practicals | practical on a dimmer | 1 Channel | Candelabra, candles 1 | candle |
| 2 | 481–481 | 120 | P-06 | Practicals | practical on a dimmer | 1 Channel | Candelabra, candles 2 | candle |
| 2 | 482–482 | 121 | P-07 | Practicals | practical on a dimmer | 1 Channel | Candelabra, candles 3 | candle |
| 2 | 483–483 | 122 | P-08 | Practicals | practical on a dimmer | 1 Channel | Sideboard candlesticks (pair) | candle |
| 2 | 484–484 | 123 | P-09 | Practicals | practical on a dimmer | 1 Channel | Candlesticks: the judge's, the Green Dragon's, Buckman's | candle |
| 2 | 485–485 | 124 | P-10 | Practicals | practical on a dimmer | 1 Channel | Torches ×2 (flicker) | fire |
| 2 | 486–486 | 125 | P-11 | Practicals | practical on a dimmer | 1 Channel | Coach lamps ×2 | lantern |
| 2 | 487–487 | 126 | P-12 | Practicals | practical on a dimmer | 1 Channel | Campfires ×2 (flicker) | fire |
| 2 | 488–488 | 127 | P-13 | Practicals | practical on a dimmer | 1 Channel | Distant lights, SR string (S30) | twinkle |
| 2 | 489–489 | 128 | P-14 | Practicals | practical on a dimmer | 1 Channel | Distant lights, SL string (S30) | twinkle |

"ch" is the desk channel (one per unit, in patch order) the hookup below uses.

## Hookup: the area systems

| area | centre (stage x, z) | front | box (side-front) | top | back |
|---|---|---|---|---|---|
| APR | +3.50, -1.30 | BR-14 (ch 14) | BBHR-1 (ch 25) | — | E1-09 (ch 40) |
| APC | +0.00, -1.30 | BR-09 (ch 9) | — | — | E1-07 (ch 38) |
| APL | -3.50, -1.30 | BR-03 (ch 3) | BBHL-1 (ch 28) | — | E1-04 (ch 35) |
| DSR | +2.85, +0.85 | BR-16 (ch 16) | BBHR-2 (ch 26) | E1-10 (ch 41) | E2-09 (ch 49) |
| DSC | +0.00, +0.85 | BR-11 (ch 11) | — | E1-06 (ch 37) | E2-07 (ch 47) |
| DSL | -2.85, +0.85 | BR-05 (ch 5) | BBHL-2 (ch 29) | E1-02 (ch 33) | E2-04 (ch 44) |
| MSR | +2.85, +2.50 | F2-07 (ch 24) | BBHR-3 (ch 27) | E2-11 (ch 51) | E3-08 (ch 59) |
| MSC | +0.00, +2.50 | F2-04 (ch 21) | — | E2-06 (ch 46) | E3-05 (ch 56) |
| MSL | -2.85, +2.50 | F2-02 (ch 19) | BBHL-3 (ch 30) | E2-02 (ch 42) | E3-03 (ch 54) |
| SHOP | -2.60, +4.90 | F2-01 (ch 18) | — | — | — |
| LOFT | -2.40, +5.30 (floor 2.4) | F2-03 (ch 20) | — | E3-01 (ch 52), E3-02 (ch 53) | E4-03 (ch 60) |
| WHARF | +2.70, +4.90 (floor 0.45) | F2-06 (ch 23) | — | E3-07 (ch 58) | E4-11 (ch 64) |
| PATH | +0.20, +5.00 | F2-05 (ch 22) | — | E3-04 (ch 55) | E4-08 (ch 63) |

| system | units |
|---|---|
| side light from SL (booms) | SL1-1 (ch 70), SL1-2 (ch 71), SL1-3 (ch 72), SL2-1 (ch 74), SL2-2 (ch 75), SL2-3 (ch 76), SL3-1 (ch 79), SL3-2 (ch 80), SL3-3 (ch 81) |
| side light from SR (booms) | SR1-1 (ch 83), SR1-2 (ch 84), SR2-1 (ch 85), SR2-2 (ch 86), SR2-3 (ch 87), SR3-1 (ch 89), SR3-2 (ch 90), SR3-3 (ch 91) |
| pros booms (apron side) | PB-L (ch 31), PB-R (ch 32) |
| long low light from SR (dawn, sunset) | SR2-4 (ch 88), SR3-4 (ch 92) |
| the back brick from above | E4-01 (ch 103), E4-05 (ch 104), E4-10 (ch 105), E4-14 (ch 106) |
| the ground row | GR-1 (ch 107), GR-2 (ch 108), GR-3 (ch 109), GR-4 (ch 110), GR-5 (ch 111), GR-6 (ch 112) |
| movers: water (bridge) | BR-M1 (ch 93), BR-M2 (ch 94) |
| movers: leaves / ride (1st) | E1-01 (ch 95), E1-11 (ch 96) |
| movers: moon / ride (2nd) | E2-01 (ch 97), E2-12 (ch 98) |
| wash movers (4th) | E4-02 (ch 99), E4-06 (ch 100), E4-09 (ch 101), E4-13 (ch 102) |
| followspots | FS-1 (ch 68), FS-2 (ch 69) |
| haze | HZ-1 (ch 113), HZ-2 (ch 114) |

## Specials

| special | unit | ch | from | focus (stage x, y, z) | field ° | gobo |
|---|---|---|---|---|---|---|
| S1 Narrator DSR (S1) | BR-17 | 17 | FOH 1 — the bridge | +3.60, 1.60, -1.60 | 19.0 | — |
| S2 Narrator DSL (S2) | BR-02 | 2 | FOH 1 — the bridge | -3.60, 1.60, -1.60 | 19.0 | — |
| S3 Followspot (S3): Johnny anywhere, the aisle | FS-1 | 68 | Theatre 2's followspot booth | +3.60, 1.60, -1.60 | 5.5 | — |
| S3 Followspot (S3): Johnny anywhere, the aisle | FS-2 | 69 | Theatre 2's followspot booth | +3.60, 1.60, -1.60 | 5.8 | — |
| S4 Cup pin, the wharf's lip (S4) | BR-13 | 13 | FOH 1 — the bridge | +1.60, 0.40, -2.35 | 4.4 | — |
| S5 The cups on the sideboard, shuttered strip (S5) | E2-03 | 43 | 2nd Electric | -2.60, 1.10, +3.30 | 15.4 | strip |
| S6 Cups on the courtroom table (S6) | BR-10 | 10 | FOH 1 — the bridge | -0.40, 0.90, +3.00 | 5.2 | — |
| S7 Cup at the gravestone (S7) | BR-06 | 6 | FOH 1 — the bridge | -2.40, 0.60, +0.70 | 5.5 | — |
| S8 Furnace glow on Johnny's face (S8) | FL-1 | 66 | Floor (behind the bellows) | -3.00, 1.50, +4.60 | 40 | — |
| S9 The crucible pour: hot low snap (S9) | SL3-4 | 82 | SL boom 3 (in 3) | -3.00, 1.00, +4.60 | 17.4 | — |
| S10 Bucket, boy and furnace isolation (S10) | SL2-4 | 77 | SL boom 2 (in 2) | -3.00, 0.80, +4.40 | 34.8 | — |
| S11 Loft isolation, front (S11) | BR-01 | 1 | FOH 1 — the bridge | -2.40, 4.00, +5.30 | 18.4 | — |
| S12 Otis at the rafters (S12) | E4-04 | 61 | 4th Electric | -2.00, 4.20, +5.30 | 12.7 | — |
| S13 Lavinia, rosy lift (S13) | BR-07 | 7 | FOH 1 — the bridge | -1.25, 1.60, +1.80 | 12.0 | — |
| S14 The doorway backlight (S14) | DR-1 | 67 | Backstage corridor, through the stage doors | +0.20, 1.50, +3.30 | 27.2 | — |
| S14b The SL in-1 doorway (S14) | SL1-4 | 73 | SL boom 1 (in 1) | -4.40, 1.60, +0.90 | 34.8 | — |
| S15 Jail bars (S15) | E1-03 | 34 | 1st Electric | -2.80, 0.50, +1.60 | 15.7 | bars |
| S16 Window light through the window flat (S16) | SL2-5 | 78 | SL boom 2 (in 2) | -1.00, 0.80, +2.50 | 23.8 | window |
| S22 Steeple lanterns pin (S22) | E3-06 | 57 | 3rd Electric | +2.60, 3.70, +6.45 | 9.5 | — |
| S24a Lantern reveal: the dressing table (S24) | E2-10 | 50 | 2nd Electric | +3.40, 1.00, +2.70 | 7.7 | — |
| S24b Lantern reveal: the wig (S24) | E1-08 | 39 | 1st Electric | +3.00, 1.40, +1.20 | 8.0 | — |
| S24c Lantern reveal: the tipped chair (S24) | E2-08 | 48 | 2nd Electric | +0.90, 0.60, +3.00 | 7.1 | — |
| S27a Shop door 1 slice (S27) | BR-04 | 4 | FOH 1 — the bridge | -3.60, 1.20, -1.20 | 8.7 | slice |
| S27b Shop door 2 slice (S27) | BR-08 | 8 | FOH 1 — the bridge | -1.20, 1.20, -1.20 | 8.8 | slice |
| S27c Shop door 3 slice (S27) | BR-12 | 12 | FOH 1 — the bridge | +1.20, 1.20, -1.20 | 8.8 | slice |
| S27d Shop door 4 slice (S27) | BR-15 | 15 | FOH 1 — the bridge | +3.60, 1.20, -1.20 | 8.7 | slice |
| S28 The eight eyes: tight cold top (S28) | E1-05 | 36 | 1st Electric | +0.00, 1.60, +0.50 | 10.8 | — |
| S28f The volley flash behind Johnny (S28), strobe | E4-12 | 65 | 4th Electric | +0.00, 2.00, +1.00 | 40 | — |
| S32 The sheet, backlit (S32) | E2-05 | 45 | 2nd Electric | +0.00, 1.50, +1.60 | 26.0 | — |
| S33 Rab at the back: soft cool backlight (S33) | E4-07 | 62 | 4th Electric | +0.20, 1.60, +5.00 | 11.0 | — |

## Practicals (each its own dimmer)

| unit | ch | U / address | what | where (stage x, y, z) |
|---|---|---|---|---|
| P-01 | 115 | 2 / 476 | Furnace glow (orange LED, flicker) | -3.40, 0.60, +5.00 |
| P-02 | 116 | 2 / 477 | Hand lantern (radio dimmer) | +0.60, 1.00, +0.30 |
| P-03 | 117 | 2 / 478 | Church lantern 1 (steeple) | +2.35, 3.45, +6.45 |
| P-04 | 118 | 2 / 479 | Church lantern 2 (steeple) | +2.85, 3.90, +6.45 |
| P-05 | 119 | 2 / 480 | Candelabra, candles 1 | +0.00, 1.10, +1.80 |
| P-06 | 120 | 2 / 481 | Candelabra, candles 2 | +0.20, 1.10, +1.80 |
| P-07 | 121 | 2 / 482 | Candelabra, candles 3 | +0.40, 1.10, +1.80 |
| P-08 | 122 | 2 / 483 | Sideboard candlesticks (pair) | -2.60, 1.30, +3.30 |
| P-09 | 123 | 2 / 484 | Candlesticks: the judge's, the Green Dragon's, Buckman's | -0.40, 1.00, +3.00 |
| P-10 | 124 | 2 / 485 | Torches ×2 (flicker) | -3.00, 1.90, +1.00 |
| P-11 | 125 | 2 / 486 | Coach lamps ×2 | +2.80, 1.60, +1.80 |
| P-12 | 126 | 2 / 487 | Campfires ×2 (flicker) | -0.60, 0.30, +1.20 |
| P-13 | 127 | 2 / 488 | Distant lights, SR string (S30) | +2.50, 1.00, +6.50 |
| P-14 | 128 | 2 / 489 | Distant lights, SL string (S30) | -2.50, 1.00, +6.50 |

## Looks

48 looks, one per tag set.json's segments use, and 33 segments that add to theirs (a lit furnace, candles, lanterns, a special). In QLC+ each look is a Scene ("Look: <tag>"), each segment with extras a Scene ("Seg n.s …"), and the chaser "Johnny Tremain" has one step per segment in show order (66), 2 s fades, held until GO.

| tag | the look |
|---|---|
| `dawn-exterior-cold` | grey-lavender, low from SR, long shadows; the cup at the gravestone |
| `dawn-exterior-warm` | low warm cross-light from SR over a cool floor |
| `dawn-interior-cold` | first daylight, cold; the window light |
| `dawn-interior-firelit` | half light, the furnace roaring; low grey-blue dawn from SR (S9 snaps up on the pour, S10 closes it down) |
| `exterior-afternoon-dappled` | warm low sun through leaves + a blue-green shimmer downstage |
| `exterior-afternoon-flat` | flat light, feathers in the air |
| `exterior-afternoon-leaves` | low warm afternoon through new leaves |
| `exterior-dawn-grey` | grey, cold, low; then the isolation (the volley flash and S28 are the cues) |
| `exterior-day-bright` | full day |
| `exterior-day-chase` | bright and fast-moving: the movers chase the horse round (S29), then the snap to one pool at the gate |
| `exterior-day-overcast` | flat grey-white, no shadows (the closed port) |
| `exterior-day-spring` | clean bright, a touch green |
| `exterior-day-street` | hard bright straw-white, a slightly warm back (the shop-door slices are the S27 cues) |
| `exterior-day-sun` | hard bright sun |
| `exterior-day-warm` | warm open yard |
| `exterior-day-winter` | pale blue-white, thin |
| `exterior-dusk-apron` | a travelling pool, amber, the rest dark (the followspot walks him home) |
| `exterior-morning-bright` | full bright straw-white on the apron, the kitchen held behind |
| `exterior-morning-cold` | bright cold morning, long shadows |
| `exterior-sunset-distant` | the last of a sunset low on the back wall, the stage dim, far twinkles |
| `exterior-sunset-long` | the finale: a long low amber raking light from the side, long shadows across the bare set |
| `interior-afternoon-firelit` | furnace orange dominant |
| `interior-afternoon-window` | window light in a quiet room |
| `interior-dawn-warm` | low amber-straw from the hearth side, the loft first |
| `interior-day-cool` | cool northern daylight |
| `interior-day-court` | bright, slightly cold, flat; the four cups on the table |
| `interior-day-dovegrey` | lavender-grey and silver: the Lytes' drawing room |
| `interior-day-empty` | clear, bright, empty |
| `interior-day-grey` | the kitchen desaturated, flat, cooler |
| `interior-day-loft` | a warm shaft into the loft, the rest dim |
| `interior-day-stable` | warm shafts |
| `interior-day-warm` | warm interior daylight, a window from SR |
| `interior-evening-bright` | crisp cool white: Revere's shop is better lit |
| `interior-morning-barred` | a cool shaft through bars, the room dim |
| `interior-morning-warm` | the kitchen at breakfast |
| `interior-night-candle` | candle amber, pools on tables, deep shadows |
| `interior-night-lamp` | Warren's surgery by lamplight |
| `interior-night-warm` | the Dawes kitchen: warm and comic |
| `night-exterior-harbour` | steel blue moonlight, water ripple on the apron, a lantern |
| `night-exterior-moon` | steel blue, moon breakup from high and behind; faces just readable |
| `night-exterior-torch` | flickering orange against blue night |
| `night-interior-candle` | the loft over the Observer by candle, the street below in the dark |
| `night-interior-dark-crowd` | near-dark, one lantern, faces only |
| `night-interior-hearth` | the hearth glow only, then the shutters |
| `night-interior-lamp` | the surgery again: midnight by the lamp, then the dark before dawn at Lexington |
| `night-interior-lantern` | darkness, the lantern moving, the three reveals |
| `night-interior-moonlit` | the truckle beds, later: moonlight through the loft |
| `night-interior-warm` | a low warm kitchen; the doorway's backlight beyond |

## Decisions left (Jack's)

- The 3rd and 4th electrics hang at 10.1 and 11.6 because the masking border (0.6 m deep at 4.4 over the deck) lets the front row see over it; a deeper border (or a second one at stage z ~4.5) would let them come down to ~8.5.
- The movers' pan/tilt values in the QLC+ scenes assume each mover hung with its front to the house — touch up the focus on the day (QLC+'s Position tool); the Encore gobo slots (water 1, leaves 2, moon 3, window 4) stand in for the real wheel.
- The followspots are on dimmer channels (D'Artagnan 934SNX) so the desk can fade them; the operators aim them.
- The practicals' circuits (radio dimmers for the hand lantern and the steeple, a DMX LED for the furnace) are the production electrician's; the channels are reserved.

