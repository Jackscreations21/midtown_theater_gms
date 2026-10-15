# MIDTOWN — agent entry point

The Midtown theatre: a scanned auditorium (`assets/midtown-auditorium.glb`, CC BY 4.0) with the real
Hamilton set and rig on its stage, the whole show auto-timed to the album, automatic actors with the
show's own choreography, a second house beside the first, a lobby and backstage behind both, a
first-person walk, a Build mode, and a lighting engine — in ONE HTML file, `midtown.html` (three.js
r128, no framework, no build step). `blocking.html` is the blocking editor. This repository was split
out of `gms-theater` (the Palace / "THE HOUSE" game) on 2026-10-15 with its history; the Palace stays
there. GitHub Pages serves this repository's root, so the page is `/midtown.html`.

## Read order — do this before touching anything

1. **STATE.md** — where things stand right now (open items only; finished work is in HANDOFF.md).
2. **HANDOFF.md** — the durable record: at minimum the newest NEXT SESSION block and the two newest
   "DONE" blocks. Blocks older than 2026-10-11 are the Palace's and stay for the record.
3. **FUTURE.md** — what is wanted and not built, and what is paused mid-build. Write new ideas there.
   It is not binding — a spec in `docs/superpowers/specs/` is, and its RULINGS are Jack's word.
4. **docs/guide/TRAPS.md** — bugs this page has actually had, by round. Read the Midtown rounds
   (2026-10-11 onward) before any change; add to it when you hit a new one.
5. **docs/guide/VISION.md** — the video capture pipeline, when touching `tools/vision/`.
6. The reference docs: `docs/HAMILTON-RIG.md` (the rig, the patch), `docs/hamilton-cues-format.md`
   (`assets/hamilton-show.json`), `docs/hamilton-blocking-format.md` (`assets/hamilton-blocking.json`),
   `docs/hamilton-dance-moves.md`, `docs/HAMILTON-LIGHTING-STYLE.md`, `assets/README.md` (licences —
   ETC's set and rig are non-commercial).

## The page itself

`midtown.html` is sectioned by banner comments (`HOUSE WORKS: …`, `THE SECOND HOUSE`, `THE DOORS`,
`BACKSTAGE`, `THE AUTOMATIC ACTORS`, …) and its header comment is the map. Everything reachable from the
console hangs off `window.MIDTOWN` (`show`, `lx`, `actors`, `doors`, `walk`, `house2Works`, `backstage`,
`frame()`…). Checks after any change: `MIDTOWN.show.check()`, `MIDTOWN.lx.check()` (show STOPPED),
`MIDTOWN.actors.check()`, `MIDTOWN.walls.check()`, console clean. Render what you changed and look at it.

## Serving it

Any static server over the repository root: `python -m http.server 8080` then
`http://localhost:8080/midtown.html`. The GLBs are fetched, so `file://` will not do. Jack's soundtrack
(`assets/audio/hamilton-soundtrack.mp3`) is local only and never committed; Pages falls back to the
official YouTube uploads. The Claude app's Browser pane runs the page at ~1.5 fps when the app window is
behind — timings there are 6× slow; count `requestAnimationFrame` before trusting any (TRAPS).

## Hard rules (Jack's, or learned the hard way)

- **All work via PRs to `main`. Never commit to `main` directly. Never stack PRs.**
- **Commits use the owner's GitHub no-reply address**
  (`314018971+Jackscreations21@users.noreply.github.com`). `gh` is not installed — PRs go through the
  GitHub API with the stored git credential (recipe below). PowerShell 5.1 mangles quoted
  `git commit -m` — write the message to a file and use `-F`.
- **Never `git add -A` while agent worktrees exist under `.claude/`.**
- **Never `setTimeout` for game timing** — time comes off the frame `dt`.
- **Never commit** his photographs, his soundtrack, the Broadway plot PDFs, lyrics.
- Rulings are lettered (the newest is in STATE.md); a ruling is recorded where it was made (HANDOFF.md's
  DONE block, the spec) and never re-opened for realism's sake.

## Opening a PR without `gh`

```sh
token=$(printf "protocol=https\nhost=github.com\n" | git credential fill | sed -n 's/^password=//p')
curl -s -X POST -H "Authorization: token $token" -H "Accept: application/vnd.github+json" \
  --data-binary @pr-body.json https://api.github.com/repos/Jackscreations21/midtown_theater_gms/pulls
```

with `pr-body.json` holding `{"title", "head", "base": "main", "body"}` — write the JSON to a file.

## Update the record

Before ending a session: update **STATE.md** (always) and append the session's "DONE" block to
**HANDOFF.md** (when work merged). A new trap goes into TRAPS.md.
