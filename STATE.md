# STATE — 2026-10-25 (OPEN ITEMS ONLY — `midtown_theater_gms`; PRs #1–#31 merged; `main` `ba250fd`; open: `claude/festive-liskov-2f7ffa`)

**Do not trust this file for what is next without fetching first.** `git fetch`, compare `origin/main`, then read
this. **This file holds only what is open.** Everything finished is in HANDOFF.md (the "DONE" blocks, newest first)
and everything wanted-but-not-built is in FUTURE.md. Do not append finished rounds here; write them to HANDOFF.md.

## Where things stand

**2026-10-24: four PRs merged in one day** (each has a DONE block in HANDOFF.md, newest first). `main` is **`852c232`**
(#20). Nothing is local-only. **Post-merge tidy still owed:** only the remote branches (the list under NEXT below); the
worktrees and local branches are gone.

- **NEWEST: PR `claude/festive-liskov-2f7ffa` (2026-10-25, late night; HANDOFF's newest DONE block; no ruling, GW next).** The mouse re-locks after
  refusals (it used to give up for good); the Van Wezel's proscenium closed to house 1's opening round the set; house 1's three
  FOH positions there moved back and up under its ceiling (beams from there, the pools the same); a "Van Wezel house light"
  slider; a "VW doors" button for all 58. **His to decide:** the follow-spot beams pass through the FOH Truss; the trusses'
  three heights; the frame's flat finish.
- **PR #31 (MERGED `ba250fd`) `claude/broadway-street-5514f3` (2026-10-25, night; RULING GV; HANDOFF's newest DONE block): Broadway outside the three houses.**
  A street on a slant past the Midtown front and the Van Wezel's glass, 42 empty fronts with 19 real Broadway houses and
  their shows, HAMILTON and JOHNNY TREMAIN marquees on the Midtown block's new front over two new pairs of street doors, a
  pair through the Van Wezel's glass under its own marquee. The header's Street buttons are Actual time / Day / Night
  (`MIDTOWN.street`), with chaser bulbs, lit signs and lamps at night, and a "Broadway" view. **His eye on it, then his to
  decide:** the Van Wezel's lower wall stays light at night; the slant and the wedge before Midtown; the approximate
  sunrise and sunset; Circle in the Square has no front; the paved strip east of the Van Wezel is open at its far north
  corner; the houses' insides are still drawn from the street. PR #30 (`vw-hamilton`) merged first; this branch has main merged in. Rulings are at **GV** (GU is `vw-hamilton`'s), so GW is next.
- **NEWEST: PR `vw-hamilton` (2026-10-25, evening; HANDOFF's NEXT SESSION and DONE blocks, RULING GU).** Hamilton on the Van
  Wezel's stage: the set, rig, actors and light mirrored from house 1 (every cue proven the same, 909 × 3 views), the pit down
  with its wall up, the band walking in at the Five, a prompt desk stage right, house 1's desk screens on the grandMA3, the
  Van Wezel's borders and electrics raised clear. His to decide: listed in the NEXT SESSION block. Rulings at GU (GV next).
- **NEXT (before it): his eye on PR #27 (`vw-answers`, MERGED `d98673c`; HANDOFF's NEXT SESSION block and its DONE block, RULING GT).** Every one
  of his Van Wezel answers and five asks is built: the model's colours back (`VW_PHOTO_COLOURS` off), the landings' lip, the
  foyer's mullions out, the follow-spot booth bigger with tall windows and its outside the ceiling's colour, the lift's pedestal
  gone and its top black, manual pit guards ("VW guards"). Then PR `vw-pit-rail` (2026-10-25, later; HANDOFF's newest DONE
  block): the pit guards a black panelled pit wall like his photo, audience side only; walls where the foyer's glass was; the
  stage-right wing 3 m wider. His to decide (listed in the NEXT SESSION and DONE blocks): the wall down at load; the booth's
  window bays; the fascia band over the foyer's new walls.
  - Tidy: every worktree under `.claude/worktrees/` and every local branch but `main` removed (2026-10-25). STILL OWED (the
    sandbox refuses remote deletes, so Jack or a terminal): `git push origin --delete film-round orchestra-pit
    preshow-announcement record-20 record-25 sm-voices stage-manager van-wezel vw-answers vw-booths vw-round record-27`
    (all merged).
- **PR #24 (MERGED, `vw-round`): Van Wezel's doors, foyer, holes, lift and backstage.** Four Opus builders,
  merged by the lead. Jack: *"the doors in the van wezel should go all the way upo to the top of the seating and add doors to
  all the frames"* (*"i didnt mean taller door i meant more"*), *"redo the lobby for the van wezel to look mor like the one for
  the other theaters"*, *"add a backstage area to the vanwezel with dressign rooms"*, *"there are a coupla holse in the walls"*,
  *"make the stage lift at the front work"*, and *"remove all the clear stuff from the lobby"*. **His to decide:**
  - the dark pilasters 0.45 m inside portals 4, 5 and 13 on each side (you step round them): cut them back?
  - the galleries' look (solid stone, a parapet); the landings at portals 7 and 13 sit 4–5 cm under the aisle;
  - the foyer has no real light (its glow is in its materials); there is a bar each side, but the box office is house right
    only; the bar pendants hang on ~7 m rods (the ceiling is at 10.9);
  - the doors' glass panes are kept (only the foyer's glass walls and its two glass pieces went);
  - the slits between the hall's ceiling panels (the roof shows through): fill them?
  - the stage stair is now a rolling wagon (it rolls under the lip while the lift travels); the lift's edge guard is invisible;
  - the basement's stairs keep the model's labels (house right is "SR" there).
  - Tidy: the four builder branches `worktree-agent-*` and their locked worktrees under `.claude/worktrees/` (never `git add -A`).
- **#23 (MERGED): the Voices button** in the header silences the stage manager's spoken lines (God mic, spots, front of house,
  the company). It is remembered in the browser; `MIDTOWN.sm.mute(on)`.
- **#22 (MERGED; RULINGS GR and GS; its DONE block in HANDOFF):** the King George announcement before
  the show and the exit music after the bows. Jack: *"add this song to play befor hamilton. make it play this then when it
  ends wait 5 seconds while burr walks out then it starts the music"*, *"put the audio on github also"*, and *"make it so
  this starts playing whenever the actors start walking off after bowing at the end and dont make the lighst go out onstage
  after the bow make them stay where they where dutrign bows"*. Both recordings are COMMITTED at his word
  (`assets/audio/king-george-announcement.mp3`, `exit-music.mp3`; the soundtrack stays local). **His to decide:**
  - the house lights go out at the Play, so the announcement plays in the dark: **his answer (2026-10-24): leave it so**;
  - the announcement plays only from a Play before Burr's walk (the top of the show); Prev/Next skip it;
  - after the exit music the stage stays lit with nobody on it until Stop (no end to the show).

- **#20 Van Wezel Hall (RULING-free; HANDOFF's newest block):** a third house east of Theatre 2 (origin x 77), its own
  glazed foyer and box office, a 15 m hallway from the Midtown lobby's east end beside the bar. `assets/van-wezel-hall.glb`
  was made for Jack by another Claude session; its textures are procedural, so it is committed. It was in feet:
  `tools/van-wezel-optimise.py` scales and merges it. **His to decide:**
  - the orchestra lift lowered to the stalls (the only way onto its stage), or raised as a thrust;
  - its stalls doors swing out;
  - it is unlit, with the light baked into its colours, so it is off the House light slider;
  - only one side door can be reached.
- **#19 the orchestra pit (HANDOFF block):** under house 1's stage. The conductor's opening is 1.10 × 0.45 m, 11 cm behind
  box 21's lip (z −1.38), with the MD's head and shoulders in it. A band of nine plays on the beat. The way down is a stair
  from the crossover, a passage, and a door on E. A "Pit" button. **His to decide:**
  - the opening's size;
  - nudge the King's, Burr's and Hamilton's DSC marks ~0.2 m upstage (a toe over its back edge at moments);
  - the walker can stand on the lid over the MD;
  - head tags show through the pit ceiling.
- **#18 THE STAGE MANAGER (RULINGS GM–GQ; spec `docs/superpowers/specs/2026-10-24-stage-manager-design.md`):** walk to the
  SL prompt corner, E at the desk. Hold at every number or the two acts. The calls: House open, Half, Fifteen, Five,
  Places, Curtain. The company answers from the dressing rooms and walks to places. STANDBY / GO. The booth's operators
  swing the followspots. Front of house; the show report. **His to decide:**
  - every body is OFF at both act tops, so at GO they vanish from the wings (show them waiting?);
  - Burr's act-2 start (world −6.03, −0.49) sits behind a thin panel;
  - the booth is very dark in a show;
  - a snap pick-up jumps the operator with the unit (a dark pre-aim would move `follow.check`);
  - the operators and the walking company are not in the walk's collision grid;
  - the SL cue lamp is upstage of his masking box 4.
  
  Not built (FUTURE): a late actor, an audience filling the seats, a show relay, calling single light cues (ruled out).
- **#17 the film round (RULING GL):** every segment re-blocked against the Disney+ frames (still share 65 % → 41 %,
  `tools/blocking/still.py`). The three followspots follow actors (423 picks, `tools/blocking/follow.py`). Facings
  continuous; an unfinished turn carries into the walk. 19 light fixes. **His eye on it with the music, then the
  agents' questions** (evidence per song in `tools/blocking/research/segN.md` "Film round"):
  - 1-02/1-03: the film fills the street, tavern and death verse with the company and lights three lamps; ours keeps
    REVIEW2's cut-back company and one lamp. 1-05: the sisters' order across the stage (ours Angelica SR, Eliza C, Peggy SL).
  - 1-08: the desk stays on through the duet in the film (Hamilton sits at it at 4:44, after his 4:37 strike); the sisters
    on the side balconies (film) or the upstage gallery (ours).
  - 1-14: Hamilton in a chair, not at Washington's desk (keep the desk?); Angelica beside Eliza from 0:07?
  - 1-19, 1-22, 1-23 contradict his "good" marks (sides swapped to the film's: Burr SR, Hamilton SL in 1-22/1-23; 1-19 round
    1-18's table). Accept? Yorktown's two gowned women on the gallery: Peggy and Angelica (by gown colour only)?
  - 2-01: the film's rolling stair is the fixed SL stair here. 2-03/2-04: the piano pushed off ~178; James sets a chair ~200.
  - 2-07: the armchair's place; 2-08's row flipped to the film (Madison SR, Burr SL); 2-10: the King's stool on at ~1:24?
  - 2-11: Jefferson's 0:19 entrance now from SL; the edge watchers in 2-11/2-12 (need chairs); 2-16: the count's seven by 2:42?
  - 2-18: Eliza and Angelica nearly still (the film); 2-19: 8 voters vs the film's ~12; 2-20: Hamilton up from the desk at 1:55.
  - Moves the library lacks (the agents' wish list): a toast, a seated layer (chair dance, nodding, the King's jamming), `lie`,
    `write`, a whisper, arms folded, a crouched creep, arms-out T, a stagger, a paper held out.
  - Cue keys that no longer sit on people and the audit could not fix: 1-12, 1-16, 1-17 keys; 2-09 Q998–1000 (the SL stair
    special: Washington no longer climbs); 1-05 Q174.5 ch91 (planned, does not land); Eacker's box (2-16, as before).
- **The hallway and the booth doors (2026-10-23, PR #15 MERGED, `main` `8cdec76`):** Jack, *"make a hallway to get backstage from the lobby and make it so i
  can open the door to get into the spot booth."* A 30 m hallway up the outside of house 1's house-right wall (x −11.85…−10.00),
  from an opening beside the box office (under a BACKSTAGE sign) to the crossover's west end. A door on E across it just past
  the lobby. Its floor ramps from the lobby's 0.875 to the backstage's 0.80. Both booths' doors open on E, at the booth floor
  (y 2.10), up a 7-riser stair with a balustrade on each projection room's house-right side; the fake floor-level doors are
  gone. Walked here: lobby → hallway → crossover, and lobby → stair → booth → the spots, in both houses. Doors 18/18, under
  16/16, lx 301/313, console clean, no new shader programs. **His to decide:** whether Theatre 2's end also wants a hallway
  (only house 1's side has one); and the look (backstage-style paint, dark reveals at the openings).
- **The lag (2026-10-16, late; PRs #12 and #13 merged, `main` `b78c183`).** #12 cut the JT rig's cold compile from ~6.5 s
  to ~0.5 s a program (HANDOFF's newest DONE block). His Chrome is on the **RTX 5060** (verified 2026-10-16: `ANGLE (NVIDIA,
  NVIDIA GeForce RTX 5060 Laptop GPU …)`, pixel ratio 1, canvas 981×639). After #12, his first load still lagged for 1–2
  minutes. His long-frame record showed the page's own code done within 10 s, so the rest was Chrome's GPU process
  compiling the new shaders once. A reload lags only ~5 s. **Open:** the first load after any shader change will lag
  like that again; the textures (196, ~950 MB with mips, 160 uploaded on first sight) could go up behind the loader
  (~0.6 s); Midtown has no room culling (hiding all of house 1 saves only 20–50% of a frame).
- **This repository is the Midtown theatre's own**, split out of `gms-theater` (the Palace game, "THE HOUSE") at
  Jack's word on 2026-10-15: *"can you move everything for the midtown theater to that repository."* Its history is
  `gms-theater`'s history filtered to the Midtown files (279 of them) as of `gms-theater` `main` `14af651` (the merge
  of #235), so `git log` on any Midtown file still shows every round. HANDOFF.md, FUTURE.md and TRAPS.md came across
  whole: their blocks before 2026-10-11 are the Palace's and stay for the record; the Palace itself stays in
  `gms-theater`. **Pages:** on (the repository is public; `main`, root); the page is
  `https://jackscreations21.github.io/midtown_theater_gms/midtown.html` — LIVE since 2026-10-15 (`index.html` redirects there). **The old
  link `…/gms-theater-game/midtown.html` is dead:** gms-theater's PR #236 (merged 2026-10-15) removed the Midtown
  files from that repository; only its record files keep the Midtown blocks, frozen at the split.
- **What `main` holds (2026-10-24):** the house at 1:1 with the Hamilton set and rig, the lighting engine, the whole show
  auto-timed, the automatic actors re-blocked against the film with three followspots that follow them, the stage
  manager (calling, the company backstage, the booth's operators), the orchestra pit under house 1's stage, the video
  capture pipeline, Theatre 2 with Johnny Tremain, its lifts and underground, one lobby behind both with E-key doors,
  the backstage block, the hallways, and Van Wezel Hall east of Theatre 2 with its own foyer.
- **PR #1 (`backstage`) is MERGED** (2026-10-15, `main` `22777e6`): the backstage block — the shell (two Opus agents, cherry-picked
  from `gms-theater` worktrees as patches `66dfbf7` and `b3575a4`): one block x −10…30.2, z 9.1…17.2, floor level
  with the stages; house 1's two slots beside the set and a pair of E-key doors cut through Theatre 2's back brick
  (6 triangles, after splitting its two-triangle fills); a crossover and eight rooms with E-key doors, 26 battens, 24
  blue running lights, 2 real lights, signs, a `Backstage` view; and the fittings — 77 pieces (dressing rooms with
  bulb mirrors, the green room, the stage door, wardrobe, showers/WC, prop tables), 27k triangles, 12 meshes, with
  `MIDTOWN.backstageFittings.check()` proving every piece inside its room and clear of every door. Checked on the
  new repo's checkout: console clean, `walls`/`lx` (301/313)/`actors`/`doors` (13/13) unchanged, the fittings check
  PASS. Walk lobby → house → wing → slot → corridor → Theatre 2's doors → its stage is the agents' evidence (driven
  by hand in the pane); the lead walked none of it live.
- **PR #6 (`his-notes`) MERGED** (2026-10-16, `main` `6d65226`): https://github.com/Jackscreations21/midtown_theater_gms/pull/6 —
  *"work on all the notes i put for the first and second half of hamilton using opus agents … fix the spotlights"*:
  every note in his blocking checklist (act 1 and act 2) applied by three Opus agents, standing on a prop by a fourth,
  his lighting notes, the hand-offs and a show-wide spotlight audit (`tools/spot-audit.py`, 84 re-aims, 17 swaps) by a
  fifth; the replies are in his checklist rows (status left for him to flip). HANDOFF.md's newest DONE block. Post-merge
  protocol done the same night: `main` fast-forwarded, `his-notes` deleted both sides, every worktree removed. Pages
  serves it.
- **PR #5 (`worklight`) MERGED** (2026-10-15, `badd196`): https://github.com/Jackscreations21/midtown_theater_gms/pull/5 —
  *"make a worklight i can turn on for both stages"*: a caged work flood on each stage's stage-left fly wall with a wall
  switch (E while walking), `Worklight` header buttons and `MIDTOWN.worklight`; no real light, a shader term clipped to
  each stage house; the show takes Stage 1's out at every Play and Stop puts it back. Built by one Opus agent, checked by
  a second, its one bug fixed by the lead (HANDOFF.md's newest block). Record files in the PR. Post-merge: fast-forward
  `main`, delete `worklight` both sides, remove the worktree `.claude/worktrees/worklight`.
- **Johnny Tremain on Theatre 2 — PR #8 MERGED (2026-10-16, `main` `daa9bcd`), post-merge done (branches deleted both sides, worktrees removed):** his own play, two acts, 26 scenes — the set as
  sized stand-ins with model slots, two stage lifts and an underground under Theatre 2 (RULINGS GI, GJ), a 128-unit rig
  with 48 looks, and the QLC+ workspace `assets/johnny-tremain/qlc/johnny-tremain.qxw`. HANDOFF.md's newest DONE block.
- **Rulings are at GU (GV next).** GU (2026-10-25, PR `vw-hamilton`): with Hamilton on, the Van Wezel's lift down as its pit at load, its wall up. GT (2026-10-25): his twelve Van Wezel answers (HANDOFF's SUPERSEDED block under the newest DONE). GR–GS (2026-10-24, PR `preshow-announcement`): the announcement before 1-01, Burr's walk in its last 5 s; the exit music at the walk-off, the bows' look held. GM–GQ (2026-10-24): the stage manager spec (his answers). GL (2026-10-24, his pick): the three followspots FOLLOW an actor, picked up by a cue, tracked every frame until an OUT. GK (2026-10-16, Jack: *"dont make the railings come up when the lift moves"*): the lift
  rails stay down in the deck, so nothing guards the hole while a lift is away (PR #13, merged). GI (2026-10-16): Theatre 2 only, a front lift brings big sets on, a back lift takes
  them off. GJ (2026-10-16): an underground under Theatre 2 for storage. Earlier: **GH**. The second-house line used FF and FG on 2026-10-15 while the actors line had
  already reached GF, so those two were RENUMBERED on the split: **GG** (2026-10-15) the auditorium doors swing INTO
  the house; **GH** (2026-10-15) a closed curtain stops the walker, like a closed door. FF is the mannequin.
- Local server: any static server over the repository root, e.g. `python -m http.server 8080`, then
  `http://localhost:8080/midtown.html` (Jack's Chrome for pointer lock; the Claude Browser pane for checks only).

## Open, in the order it will bite

000. **His first real QLC+ run (PR #10 MERGED 2026-10-16, `main` `8aded0b`; it also landed #9; post-merge done — `jt-models`,
   `t2-artnet`, `record-8` deleted both sides, the worktree removed):** run `python tools/artnet-relay.py`, in QLC+
   tick Art-Net output on 127.0.0.1 for universes 1 and 2, open localhost:8080/midtown.html, press "T2 rig" — the panel
   should read "Desk: QLC+ live". Unverified with real QLC+ (not installed here). If it reads "relay up, no Art-Net",
   QLC+ holds port 6454: bind the relay to the NIC address. His models: 45 fitted (10 local-only, CGTrader); left: a real
   press model, crates/tea chests, the signs, candelabra/candlesticks/tankards/lumber (not downloaded). HANDOFF's newest block.
00. **His eye on Johnny Tremain (PR #8, merged)** — the "Johnny Tremain" button (Next/Prev or PageDown/PageUp,
   Auto), "Lifts", "Understage", "T2 rig"; Pages serves it. **His models are FITTED** (item 000; the sources stay in `Downloads\jt-models\`, refit
   any piece with `tools/jt-fit/`); still to get: Brass Candleholders (Poly Haven API, he has not said yes), Old
   lumber stack (Fab), Pewter Tankard (RenderHub). Colonial House is EDITORIAL-only (ask the author before a show).
   21 CGTrader `.tmp` copies sit in his Downloads — delete only on his word. Decisions it raises: the loft and wharf
   turned up/downstage at the sides; a second border (the 8 m masts show their lowest 3 m at out-trim; the 3rd/4th
   electrics could come down to ~8.5); the masking legs and the SL wing lost to the understage stair; backstage-stored
   pieces hidden, wagons jump bay↔lift out of sight (not driven round the loop); Dove's hatch (13.3) could use the trap
   room; the booth window faces the back shaft; E works through the booth wall; the lift tops' seams; the basement on a
   camera layer (−43 draw calls at boot); the movers' pan/tilt and gobo slots are placeholders; specials at 0 inside
   their looks need their own cues (6 pour, 20 volley/eyes, 19 Otis, 8 shop-door slices); wing booms not solid to the
   walker (SL boom 1 stands in the worklight walkway); a look costs ~15 ms on Intel UHD (`JTL.N` 32 → 16 saves ~5 ms);
   the furnace glow is drawn twice (the set's flame + the rig's practical). His script stays OUT of the repository.

0a. **His eye on the notes round** (PR #6, merged): watch both acts again with the checklist open — every row he marked has a
   "— Claude (10-16)" reply under his note; he flips the status. Decisions it raises: **2-07's switch** to Hamilton's
   lights is at 77.27 (the first downbeat after Washington's call), alternatives 79.19 / 81.11 / the old 82.1;
   **Eacker's box** (2-16: every unit stops on the SL gallery rail — move his mark, or rule him onto the deck where
   Viper 13 lands); **Binkley's real cues** with a named person in no narrow light (1-01 36, 1-15 459/468, 1-23 638,
   2-05 864.01/882, 2-22 1256/1259) — add a pin on the person, or leave his washes; **standing on a piece**: an explicit
   `y` at a prop's top now stands the body on it (Lafayette, 1-18) — the other seven "inside the piece" cases are
   candidates: Seabury's box 1-06 (y 0.5), Yorktown's box 1-20 (0.5), the Room's table 2-05 (0.8), Hamilton's desk 2-14
   (0.8), the burn bench 2-15 (0.5), Philip's table 2-17/2-18 (0.8), the duel box 2-22 (0.5); 1-11's ball couples are
   re-paired by nearest place; 1-20's rally arc was kept where it was so the drill and battle after it stand.
0. **His eye on the worklights** (PR #5, 2026-10-15): the `Worklight` header buttons, or walk to the grey switch box
   on either stage's stage-left wall just upstage of the proscenium and press E. Decisions it raises: both OFF on load
   (or Theatre 2 on by default?); the lamp high on the stage-left fly wall, mostly out of sight from the stalls and the
   walk (a stand on Theatre 2's deck, or a pipe once the rig has a gap, are the alternatives); the look (warm 0xffe4bc,
   gain 8, lift 0.08 — brighter? cooler? it rides the House light slider now); +18 draw calls at Back of house (the
   fixture could merge to ~5 meshes a stage); the Lights panel's old "Work light" slider (the engine's LOOK, which the
   show fades) now sits beside the new "Worklight" fixtures — rename one? And the walker's 0.25 m body passes through the switch box (its centre stands
   0.25 m off the wall; unseen in first person) — move the box 0.3 m up the wall, or leave it.
1. **His eye on the backstage** (`Backstage` button; walk from either wing upstage past the set into the corridor;
   E on the doors). Decisions it raises: the house-1-facing faces of the block are black (seen from the fly gallery
   over the roof); EXIT signs over all three ways onto the stages; Theatre 2's closed doors are visible from its
   stalls upstage centre; only 2 real lights (3 cost 2–6 ms); the make-up counters have closed fronts (an open one
   does not stop the walker — TRAPS); the jog's return wall stands at x 10.40 (box 21's end), not the spec's 10.20 —
   trim the slab to 10.2 or change `stageZ.jog`; `stageDoors.h2.head` was read as a height over the floor (the doors
   are 4.2 m tall — a real stage door is 2.4–3 m; his call); the brick cut starts at z 8.85 (8.80 would hole the deck).
   **Pages is LIVE** (public repository, `main`, root, 2026-10-15): the page is the URL above. `gms-theater`'s landed
   branches are deleted both sides; its Midtown files are gone (PR #236).
2. **Jack's eye on Theatre 2, its booth and desk, the doors and the long lobby** (PR #235). Decisions it raises, none
   made: Theatre 2's own show, or stays empty (its desk screens are dark until there is one); the doors' swing is
   RULED (GG: into the house); a closed curtain stopping the walker is RULED (GH: it does, like a closed door); whether
   E should also work in orbit mode (walking only now); the curtain's colour (0x7a1020, glow 0.3); whether E should
   refuse to open a pair onto a walker standing in a leaf's path (the leaf passes through them now; they walk out); the
   curtains' 48 track rings are always drawn (~3.8k triangles, frustum culling off on the instanced mesh); the 0.68 m
   void between the two
   houses' outer walls (sealed by the lobby's wall, invisible from inside); the signs ("STALLS" over house 1's doors,
   "THEATRE 2" over the new pair, "PROJECTION" on both projection rooms); Build mode's "add piece" / delete box still
   land on house 1 only (`houseScene()` — one line to include Theatre 2); house 1's desk measure costs ~1.3 s of the
   load and the faster copy Theatre 2 uses would save ~0.9 s but moves its geometry by ~1e-8 m (TRAPS); Theatre 2's
   followspot props stay full size when house 1's set is "fitted" (house 1's spots shrink with the set).
3a. **His act-1 dancing notes (from PR #234)** were applied in the notes round (PR #6, 10-16), and the film round
   (#17) went over every song again; what is open about the blocking is #17's questions at the top of this file.
3. **His re-check through the cue checklist.** The brief is the artifact https://claude.ai/artifact/FpiGBBW8LicWbaRb1nTUjg
   ("Hamilton Cue Checklist": collection `songs`, doc id = track id, fields `status` / `notes` / `updatedAt`). **Read
   it with `ArtifactData` `list` (or `query` on `status != good`) at the start of every cue round.** Nine songs carry
   notes answered once and not yet re-checked — act 1: My Shot, Farmer Refuted, Ten Duel Commandments, Guns and Ships,
   Non-Stop; act 2: Cabinet Battle #1, Cabinet Battle #2, Washington on Your Side, Who Lives. The method for a note is
   in HANDOFF.md's NEXT SESSION block for #233 (on `cue-blackouts`): render the suspect seconds, edit with a
   state-folding script, `show.check()`.
4. **The rig placements the cue photos exposed** — Jack's to rule on; the options are in FUTURE.md ("Rig placements the
   cue photos expose"): the three 10th-Electric VL3500s burning the upper brick, the back-wall foots under the gallery,
   the Deck strips pointing at the deck edge; and the six REAL cues that still throw into Midtown's house at the
   Rodgers' aims (194, 200, 300.3, 1044, 1110, 1238.01) — a focus clamp in the player, or leave them.
5. **Still not drawn / not run in the show:** Binkley's `edge` and `frost`; the 238 effect entries; the turntable
   moves (in no file); 16 channels with no rig unit; the Cabinet Battle sides still unsourced beyond his word.
6. **The player's body.** Jack, on the walk (2026-10-11), paused on his "wait a second": *"the person is too tall,
   and also give them a body."* Eye is 1.6 m (Palace 1.68; Roblox ~1.4); a visible body, maybe third person. Not
   started; start fresh off the branch tip.
7. **The Hamilton game spec is not written** (FUTURE.md PART 2 "THE HAMILTON GAME"): `midtown.html` is a preview
   page, not the second build target. Rulings letter from FF.

## Facts you need to work on the Midtown page (not history)

- **Johnny Tremain (Theatre 2).** Three sections before BUILD MODE, in order: `THEATRE 2: THE UNDERGROUND AND THE LIFTS`
  (`MIDTOWN.under`: `.lifts.front/.back` `{platform, footprint, top 0.80, bottom −4.40, state, go(to) → Promise}`, `.bays`,
  `.check()`), `… — THE SET` (`MIDTOWN.jt`: `scene(n, seg)`, `next/prev`, `check()`, `materials`; data `assets/johnny-
  tremain/set.json`, checker `tools/jt-set-check.py`), `… — THE LIGHTS` (`MIDTOWN.jtLights`: `look(n, seg)` seg 1-based,
  `check()`; data `rig.json` from `tools/jt-rig.py`; QLC+ from `tools/jt-qlc.py` — regenerate the .qxw after any rig
  change). The contract between them is `docs/johnny-tremain/CONTRACT.md`. Keep-outs: the SL wing stair hole (world x
  10.6–13.75, z 4.0–8.6) and the worklight walkway (stage x −9.4…−4.3, z 0.65…1.45). The collider regex ends
  `…|understage|jt set)$/`.

- **Theatre 2's works and the doors (PR #235, 2026-10-15).** `buildSpotBooth(root, {dx, mesh, props})` and
  `buildDeskPosition(root, {dx, scan, live})` build both houses' booths and desks; Theatre 2's cuts are `HOUSE2_CUTS`
  (`only: 'house2'`, applied by `reapplyAll` with the rest — a cut applied anywhere else vanishes on the first bake or
  undo); `MIDTOWN.house2Works` = { booth, desk, spots, cuts, cut() }. Both houses' groups share the names `followspot
  booth` / `lighting desk` (`userData.house` tells them apart) — never look a booth up by name. The doors: `DOORS`,
  `buildDoors`, `doorsTick(dt)` in the frame loop (doors and curtains both), `doorsHit` inside `builtHit` (ray-tested
  directly, NOT in the walk's grid); E while walking → `doorsUse()` (edge-triggered in the keydown listener), the target
  from `doorAim` (within `DOORS.reach` 2 m and `DOORS.aim` 50° of the look, same floor), the hint from `doorAimTick`;
  the curtains: `CURTAINS`, `buildCurtains` (measured off each passage's house end in `buildLobby`, `meas.curtains`),
  `curtainMat` / `curtainPleats` (a stripe map shades the pleats — a real vertical fold reads flat under the hemisphere).
  `MIDTOWN.doors.state()` prints every pair's and curtain's state, the walker's distance and what E would reach;
  `MIDTOWN.doors.toggle(name, open?)` drives one from the console. **The Browser pane runs the page at
  ~1.5 fps when the Claude window is not in front** (dt capped at 0.1 s, so game time crawls 6×): a 0.7 s door takes
  ~5 s of wall time there; measure with `requestAnimationFrame` before trusting any timing in the pane.
- **Two houses now (PR #235).** House 1 is `houseRoot` (`MIDTOWN.house`), the cut one with the set, rig, booth, desk
  and bakes; everything that treats scan meshes by the `Object_` name or traverses `houseRoot` (booth, lobby measure,
  `cutBeams`, `wallSplit`/`wallCheck`, `applyCut`, the rigging, the lighting check) is house 1's and must stay so.
  Theatre 2 is `house2Root` (`MIDTOWN.house2`), meshes named `h2: <name>`, its own geometry (a clone of the loaded GLB
  taken before anything touches house 1 — two clones of one GLB share buffers otherwise, TRAPS). Its materials are in
  `houseMats`, so the House light slider and the show's house fades dim both. The lobby is one room behind both
  (`LOBBY`, `buildLobby(house1, house2)`, four `doors` each with `house` and `side`).
- **Local serving:** `.claude/launch.json` (gitignored) entry `midtown`, Python `http.server` on 8080 over the repo
  root; `preview_start` it. **It dies when the Browser pane is closed** — restart before navigating. Pointer lock
  fails inside the pane; a normal Chrome window at the same URL is the better window for him. His Chrome must be
  on the RTX 5060 (set to High performance in Windows), unverified.
- **His soundtrack is local only** (`assets/audio/hamilton-soundtrack.mp3`, never committed; the one-file album). **On
  Pages the Show panel's "Use your soundtrack file…" picks the same file off his disk and remembers it** (a File System
  Access handle in IndexedDB; `MIDTOWN.show.useLocalFile(file)` / `pickLocalFile()` from the console) — no YouTube, no
  ads; the fallback to YouTube remains for a visitor with no file. The
  seek table and the loudness envelope (#233) are specific to HIS copy — a different file needs `mp3toc.py` (the
  table) and a new envelope (20 ms RMS, `255·(log10(rms)+4)/4`). Python's `http.server` has no Range requests, so the
  file loads into a Blob. **Pages falls back to the official YouTube uploads**, which seek exactly.
- **Checks after any cue edit:** `MIDTOWN.show.check()` (seek = play-through, references resolve, timeline
  monotonic); `MIDTOWN.lx.check()` 301/313 **with the show STOPPED**; console clean. Render what you changed and
  look at it (`MIDTOWN.frame()` draws one frame synchronously for a hidden pane; TRAPS "From the cue-review round").
- **Preshow and the interval:** opening the Show panel puts the show at its top paused, preset up, house up; at the
  end of 1-23 it holds (blackout, preset, house up) until Play. Works on all three clocks.
- **Bakes:** he exports `Downloads\midtown-build*.json`; append `pieces` to `BAKED` and `cuts` to `BAKED_CUTS`
  (replace only if he pressed "Edit the baked pieces" first); suffix names "(bake N)"; **tell him Clear all** after.
  **Check every baked piece's extent against Theatre 2** (x 10.2…30.0): box 21 reached into it once.
- **No test suite covers `midtown.html`**: the checks are the page's own (`MIDTOWN.show.check()`, `lx.check()`,
  `actors.check()`, `walls.check()`, `doors.state()`), the console, and renders. Node is not installed on this machine.
- **`gh` is not installed**, so the app cannot bind a PR to a session; PRs open through the API (CLAUDE.md) and
  Jack merges them on GitHub (or says the word and the lead merges through the API).
- **Never commit:** his photographs, his soundtrack, the Broadway plot PDFs, lyrics. ETC's set and rig are
  non-commercial (`assets/README.md`).

## Standing facts

Coordinates are the GLB's: Y up, metres, the deck at y 0.80, the proscenium plane at z 2.30, UPSTAGE IS +Z (the
opposite of the Palace's convention; the set model is turned 180°). House 1 at the origin, Theatre 2 at x +20
(`HOUSE2.dx`). three.js r128 from a CDN. ETC's set and rig are non-commercial (`assets/README.md`). The
mannequin is Jack's own scan (RULING FF). Every timestamp in the show file is seconds into the album track.

## Shelved

**Nothing.**
