# The film round: every segment against the footage, the stillness, the followspots (2026-10-24)

The brief for the eight segment agents. Jack, verbatim:

> *"can you look the the audio and videso agian there is still a lot of stuff wrong. ... there are also a lot of scenes
> when people ar just standing still when they should be dancing or moving. also use the 3 spotlights to make sure
> people get lit up fully when they should be. there are also a lot of scenes when people are just in the wrong place"*

He ruled (2026-10-24): the three followspots FOLLOW an actor (picked up by a cue, tracking her every frame until an OUT);
eight agents, one per segment, as in the earlier rounds.

## Your three jobs, in your segment's songs

1. **Wrong places.** Compare where our bodies stand with where the film's do, moment by moment, and move ours: who is
   on, which side, upstage/downstage, on the deck or the gallery, who is next to whom, entrances and exits.
2. **Standing still.** `python -I tools/blocking/still.py --tracks <yours>` lists every run of 8 s or more where someone on
   stage neither walks nor dances. The show as merged is 60–90 % still in most songs; the film is not. Fill it with
   what the film shows: travel, dance phrases, gestures (a rapper is never still: arms, a step, a turn on the line),
   ensemble business, the turntable walks. Still on purpose (a soliloquy, a tableau, a listener, a frozen picture) is
   fine. Say so in the generator where you keep it. Aim for numbers that look like the film, not for a percentage.
3. **The followspots.** Write the picks in YOUR section of `tools/blocking/follow.py` (its docstring is the format):
   who each of the three spots is on and when, so every principal who carries a number, a verse or a moment is fully
   lit. The film shows followspots plainly: a hard-edged bright circle on one person, usually head to toe. Follow
   what you see; where there is no footage (or the shot is tight), put a spot on whoever leads the moment and is not
   already in a special. Every segment ends with all three spots OUT. Spot 2 (house left) suits stage RIGHT (−x), spot
   3 (house right) suits stage LEFT (+x), spot 1 is centre.

His checklist notes are RULINGS: do not undo anything a row asks for or a "— Claude (10-16)" reply says was done. The
rows are in `C:\Users\jackf\AppData\Local\Temp\claude\C--Users-jackf-OneDrive-Documents-gms-theater\245f98a7-ee55-49af-9aed-42d9481950ea\scratchpad\blocking-checklist\songs\<track>.json`
(fields `status`, `notes`; read-only). Songs he marked `good` can still have stillness and wrong places fixed. Keep
what he liked about them and change only what the film contradicts.

## The sources

- **The footage, already cut into frames** (the Disney+ film, one clip per number; there is no clip for 1-09, 2-02, 2-13,
  2-15, 2-22 or 2-23):
  `C:\Users\jackf\OneDrive\Documents\gms-theater\.claude\worktrees\agent-a00f4ef392ac2906d\tools\vision\cache\<clip>\`
  - `frames.json`: `frames[i]` = `{file, t, track, at, tconf, shot}`. **`at` is seconds into the album track, the same clock
    as the blocking, the cues and the page's readout.** `tconf` < 0.3 means the time is a guess there.
  - `frames/NNNNNN.jpg`: 5 per second, 1280×720. Open them with the Read tool (it shows images).
  - `shots.jpg`: the clip's cuts, as frame pairs, to find the wide shots fast.
  - Clip names: `C:\Users\jackf\Videos\hamilton-clips\` (or `video/INDEX.json` in the repository).
  - **Orientation:** the film's house cameras look upstage, so **the RIGHT of the frame is stage LEFT (+x)**. Our
    set-local frame: x + is stage left, z − is upstage, z + toward the house; deck `y` 0, the galleries 2.74.
    The set is the film's set at 1:1. The turntable rings, the two stairs, the upstage gallery and the side balconies
    are in both. `docs/guide/VISION.md` §1–§4 explain the pipeline. You do not need to run it.
  - A close-up tells you who is singing and what they are doing (gesture, dance), not where they stand. Read places
    off the wide shots.
- **Motion energy from the film** (20 tracks): `tools/vision/out/<track>.json` → `motion.company` per bar: how much the
  bodies in the frame moved. The per-person rows are unlabelled guesses. Ignore them.
- **The audio:** the album is `assets/audio/hamilton-soundtrack.mp3` (local only, never commit or copy it). The beat
  grid is `assets/hamilton-beats.json`, and `tools/blocking/beats.py` finds a bar. Stereo was tested on 2026-10-24 and
  the lead vocals are centred in both the film and the album, so left/right does not locate a singer. Do not spend time
  on it.
- **The research behind your segment:** `tools/blocking/research/seg<N>.md` and the notes file of your generator.
- **The move library:** `tools/hamilton-moves.json`, described in `docs/hamilton-dance-moves.md`. The header of
  `tools/blocking/dance.py` explains how an entry is written.

## The method, per song

1. `still.py --tracks <song>`. Read the checklist row and your research notes.
2. Walk the clip's wide shots. For a moment you check, read the film frame and plot ours at the same `at`:
   `python -I tools/blocking-plot.py assets/hamilton-blocking.json <track> <t1,t2,...> --out <your scratch>`
   (`--path <actor>` for one body's whole route, `--sheet --every 5` for a contact sheet).
3. Fix the generator, your SEGMENT section of `dance.py`, your SEGMENT section of `props.py` if furniture moves, and your
   SEGMENT section of `follow.py`.
4. Regenerate and check (from the repository root):
   ```sh
   cd tools/blocking && python -I <your generator> && python -I props.py && python -I dance.py --check <N> && cd ../..
   python -I tools/blocking-merge.py tools/blocking/segments --check   # 0 errors; the other segments' segN.json must exist: run their generators once first
   python -I tools/blocking-merge.py tools/blocking/segments           # writes assets/hamilton-blocking.json (do NOT commit it)
   python -I tools/blocking/follow.py --check --tracks <yours>         # 0 problems
   python -I tools/blocking/still.py --tracks <yours>
   ```
   The generators: seg 1 `seg1/export.py` (+ `seg1/lib.py`, `t101.py`…`t106.py`), 2 `gen_seg2.py`, 3 `seg3gen.py --space`,
   4 `gen4.py`, 5 `seg5gen.py` (+ `seg5lib.py`), 6 `gen6.py`, 7 `seg7_gen.py`, 8 `gen_seg8.py`.
   `docs/hamilton-blocking-format.md` is the format.

## Rules

- **Touch only your own files:** your generator (and its lib and notes), your segment's research file, and your
  `# ===== SEGMENT N` sections of `dance.py`, `props.py` and `follow.py`. Never edit `midtown.html`, `blocking.html`,
  `tools/blocking-merge.py`, `tools/blocking-plot.py`, another segment's anything, or the move library. If you need a
  move the library lacks, use the nearest one and list what you wanted in your report.
- **Commit only sources**, on your worktree's branch, with a plain message ending
  `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. Write the message to a file and use `git commit -F`. **Never
  commit** `assets/hamilton-blocking.json`, `assets/hamilton-follow.json` or `tools/blocking/segments/`. The lead
  regenerates them after merging the eight branches. Never commit a footage frame, the soundtrack, or lyrics.
- No browser: the lead's session owns the one browser pane. The plots and the film frames are your eyes.
- Python is the system `python` (standard library). Read and write with `encoding='utf-8'`, and write committed files with
  `newline='\n'`.
- Keep the merge at 0 errors, `dance.py --check` at 0, `props.py --check` at 0 and `follow.py --check` at 0 problems.
  Re-running your generator must reproduce your segN.json.
- Before writing a song, **record what the film shows** in your research file under a dated heading
  `## Film round (2026-10-24)`: per song, the moments you read (clip, `at`, what is where) and what you changed. That is
  the evidence Jack and the next session read.

## Your report (short: the lead reads it, not your tool calls)

Per song: one line on what changed (places, stillness before → after from `still.py`, followspot picks), and anything
you could not do. Then the moves you wished the library had, the questions only Jack can answer, and your branch's last
commit.
