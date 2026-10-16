# STATE — 2026-10-15 (OPEN ITEMS ONLY — `midtown_theater_gms`; PRs #1–#4 merged, #5 open; public, Pages live; nothing is local-only)

**Do not trust this file for what is next without fetching first.** `git fetch`, compare `origin/main`, then read
this. **This file holds only what is open.** Everything finished is in HANDOFF.md (the "DONE" blocks, newest first)
and everything wanted-but-not-built is in FUTURE.md. Do not append finished rounds here; write them to HANDOFF.md.

## Where things stand

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
- **PR #5 (`worklight`, off `main`) is OPEN** (2026-10-15): https://github.com/Jackscreations21/midtown_theater_gms/pull/5 —
  *"make a worklight i can turn on for both stages"*: a caged work flood on each stage's stage-left fly wall with a wall
  switch (E while walking), `Worklight` header buttons and `MIDTOWN.worklight`; no real light, a shader term clipped to
  each stage house; the show takes Stage 1's out at every Play and Stop puts it back. Built by one Opus agent, checked by
  a second, its one bug fixed by the lead (HANDOFF.md's newest block). Record files in the PR. Post-merge: fast-forward
  `main`, delete `worklight` both sides, remove the worktree `.claude/worktrees/worklight`.
- **Rulings are at GH (GI next).** The second-house line used FF and FG on 2026-10-15 while the actors line had
  already reached GF, so those two were RENUMBERED on the split: **GG** (2026-10-15) the auditorium doors swing INTO
  the house; **GH** (2026-10-15) a closed curtain stops the walker, like a closed door. FF is the mannequin.
- Local server: any static server over the repository root, e.g. `python -m http.server 8080`, then
  `http://localhost:8080/midtown.html` (Jack's Chrome for pointer lock; the Claude Browser pane for checks only).

## PAUSED 2026-10-15 22:15 — his act-1 and act-2 notes round, mid-flight (branch `his-notes`, no PR yet)

Jack: *"work on all the notes i put for the first and second half of hamilton using opus agents … fix the spotlights"*,
then *"pause by 10:15"*. **Where it stands:** the three blocking agents' branches (`notes-seg12` `205150c`, `notes-seg34`
`37e0c69`, `notes-act2` `5bbb746`) and the engine fix (`prop-standing` `2c179e7`: an explicit `y` at a placed prop's top
stands the body on it) are MERGED into `his-notes` (`af46423`; merge 0/0, 7,323 waypoints, `actors.check()` green per the
agents; the lead has NOT rendered the merged page himself). The cue agent (branch `his-notes-cues`, worktree
`.claude/.claude/worktrees/cues` — one folder too deep, a lead's `cd` slip) was mid-way through his LIGHTING notes
(1-01, 1-04, 1-14, 2-06, 2-07, 2-23) and the hand-offs when paused; it was told to commit a WIP and write
`docs/WIP-cues-2026-10-15.md` saying where it stopped. The show-wide spotlight audit (`tools/spot-audit.py`, re-aiming
every person light to where the actors now stand) was NOT started. **Not done:** the cue work, the lead's own check of
the merged page, the one-line replies into his checklist rows, the PR, HANDOFF's DONE block (a draft is in the lead
session's scratchpad `worklight/notes-handoff.md`). **Resume:** read `docs/WIP-cues-2026-10-15.md` on `his-notes-cues`,
merge it into `his-notes` (regenerate the blocking file WITHOUT `--check` if the generators moved — `--check` does not
write), finish the cue notes and the audit (the brief is in HANDOFF's next DONE block once written; until then the
agents' reports are in the lead session), check the page, reply per row, open the PR. Worktrees to remove after: the
five under `.claude/worktrees/` and the deep one.

## Open, in the order it will bite

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
