# STATE — 2026-10-16, evening (OPEN ITEMS ONLY — `midtown_theater_gms`; PRs #1–#10 merged; nothing is local-only)

**Do not trust this file for what is next without fetching first.** `git fetch`, compare `origin/main`, then read
this. **This file holds only what is open.** Everything finished is in HANDOFF.md (the "DONE" blocks, newest first)
and everything wanted-but-not-built is in FUTURE.md. Do not append finished rounds here; write them to HANDOFF.md.

## Where things stand

- **PR `jt-shader-compile` (2026-10-16, late) is OPEN:** Jack, *"the game lags insanely bad and sometimes it gets stuck on
  cmpiling."* The JT rig's shader term loop was unrolled 32×, so each lit program took ~6.5 s to compile cold on the
  Intel chip (~70 programs: minutes on "Compiling…"; 6 s freezes as late models appeared and when the rig came on). Now
  a texture and a real loop: same picture to the pixel, same frame time. A cold load took ~10 s in the pane. `warmLate()`
  precompiles the late JT models and the actors, so the rig's first frame went from 10 s to 0.36 s. **Still slow:** a
  1080p frame on the Intel UHD is ~100 ms with the T2 rig up. If he still lags, the first question is which GPU his Chrome
  prints at load (`midtown: rendering on …`); the RTX 5060 is unverified (TRAPS, "the compile-and-lag round").
- **This repository is the Midtown theatre's own**, split out of `gms-theater` (the Palace game, "THE HOUSE") at
  Jack's word on 2026-10-15: *"can you move everything for the midtown theater to that repository."* Its history is
  `gms-theater`'s history filtered to the Midtown files (279 of them) as of `gms-theater` `main` `14af651` (the merge
  of #235), so `git log` on any Midtown file still shows every round. HANDOFF.md, FUTURE.md and TRAPS.md came across
  whole: their blocks before 2026-10-11 are the Palace's and stay for the record; the Palace itself stays in
  `gms-theater`. **Pages:** on (the repository is public; `main`, root); the page is
  `https://jackscreations21.github.io/midtown_theater_gms/midtown.html` — LIVE since 2026-10-15 (`index.html` redirects there). **The old
  link `…/gms-theater-game/midtown.html` is dead:** gms-theater's PR #236 (merged 2026-10-15) removed the Midtown
  files from that repository; only its record files keep the Midtown blocks, frozen at the split.
- **What `main` holds:** the house at 1:1 with the Hamilton set and rig, the lighting engine, the whole show
  auto-timed (891 cues), the automatic actors with the show's choreography (dance round 2, RULING GF), the video
  capture pipeline, Theatre 2 beside the first with its own followspot booth and lighting desk, one lobby behind
  both with E-key doors and a curtain in each passage, and the backstage block's SPEC with two stubs.
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
- **Rulings are at GJ (GK next).** GI (2026-10-16): Theatre 2 only, a front lift brings big sets on, a back lift takes
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
3a. **The actors' next round (from PR #234): his act-1 notes on the dancing.** Jack watched act 1 after dance round 2
   (RULING GF) and wrote verdicts into the blocking checklist https://claude.ai/artifact/4Q5Xh37ZmSinhtsJbVhAub
   (`songs`): 14 good, 7 need work (1-01 spotlights off — a CUE note; 1-02 the table farther to centre; 1-03 My Shot
   needs a real dance track; 1-04 the chairs' exit and the lead-in to 1-05; 1-05 Burr, re-check; 1-11 the rewind;
   1-14 the desk off at 50 and Lee's spotlight — a CUE note; 1-17 wait for the blackout; 1-20 Yorktown's box and
   line-up), two notes with no verdict (1-08, 1-18 — Lafayette stands IN the table: no raised standing yet). Act 2 not
   watched. **The full brief, with his words per song and the method (segment generators, `props.py`, `dance.py`,
   `MIDTOWN.actors.check()`), is HANDOFF.md's block "NEXT SESSION: HIS ACT-1 NOTES — SEVEN FIXES AND TWO SETS OF
   TIMINGS".** Read the checklist again first; he may add act 2.
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
