# `assets/johnny-tremain/set.json` — the ground plan's format

The ground plan for *Johnny Tremain* on **Theatre 2** of `midtown.html`, machine-readable, for the set builder.
`format: "johnny-tremain-set/1"`. The scene-by-scene reasons are in [BREAKDOWN.md](BREAKDOWN.md); the lighting brief
is [LIGHTING-NEEDS.md](LIGHTING-NEEDS.md).

## The stage frame (every position in the file is in it)

| axis | meaning | world |
|---|---|---|
| **x** | **+x = STAGE RIGHT** (the audience's left = house left). **−x = STAGE LEFT** (house right). | world +x is stage right in this GLB |
| **z** | **+z = upstage** of the proscenium plane; **−z = the apron**. | world +z (UPSTAGE IS +Z in the Midtown GLB) |
| **y** | up from the deck | world +y |

**Origin:** the centre of the proscenium opening, on the deck, on the proscenium plane.

**To world:** `world = (20.00 + x, 0.80 + y, 2.30 + z)`. A pure translation, no flip: `HOUSE2.dx` is 20.0, the opening
is centred on the GLB's x 0.00 (piers at ±4.30), the deck is y 0.80 and the proscenium plane z 2.30.

**rotY:** degrees about +y in three.js's sense. **0 = the piece's front faces the house (−z)**; +90 faces stage
left (−x); −90 faces stage right (+x); 180 faces upstage. A glTF model whose front is +z in its own file needs 180
added when it is loaded.

**A placement** is `{x, y, z, rotY}` plus, optionally, `scale` (uniform, for the forced-perspective tents), `w` (a
narrower width than `size`), `tipped: true` (lying on its side). **x, z = the centre of the footprint; y = the
piece's BASE** over the deck (0 on the floor, 0.45 on the wharf deck, 2.40 on the loft).

## Top level

| key | what |
|---|---|
| `stage.frame` | the frame above, in words |
| `stage.measuredWorld` | Theatre 2 measured off the GLB (world metres): deck, apron, arch, back brick, side walls, wings, fly roof, the venue's hanging iron, the stage doors, the worklight, the stray scan triangles, the seating |
| `stage.measuredStage` | the same, in the stage frame, plus the fly lanes and the sightline formulas |
| `stage.vsWorklist` | his worklist's stage numbers against the measurements |
| `parks` | the named storage areas (wings, props tables, backstage, flown, on stage) |
| `pieces` | one entry per physical piece (below) |
| `scenes` | one entry per scene (below) |

## A piece

| key | what |
|---|---|
| `id` | kebab-case, unique |
| `name` | what it is |
| `worklistModel` | the exact `###` heading in his worklist, or `null` when it is "Still missing" or not in the worklist at all |
| `slot` | where its model goes: `assets/johnny-tremain/models/<id>.glb` |
| `size` | `[w, h, d]` real-world metres at rotY 0 (w along x, d along z) |
| `kind` | `unit` (the unit set, never leaves) · `travel` (furniture and scenery that comes on and off) · `hand` (props carried or set on furniture) · `flown` (in from / out to the fly tower, including dead-hung masking) |
| `count` | how many |
| `credit` | the programme credit line (CC BY / BY-SA), or `null` |
| `licenceNote` | the licence in a line: editorial-only, no-AI-use, share-alike, Fab, CC0, "no model yet" |
| `home` | an array of `count` placements: where each copy stands when it is on and nothing says otherwise |
| `storage` | where it is when off: `{where, x, y, z, rotY, note?, fits, at?}`; `where` is a `parks` key; `fits` says whether its narrow side fits that place, measured. `at` (a wing piece with several copies): one spot per copy, packed apart by the re-lay (2026-10-16). **`where: "lift"`** (a BIG SET, RULING GI): `{where: "lift", wagon, bay, fits, note}` — `wagon` names the pieces that travel together as one rigid layout (every piece with the same `wagon`), `bay` the basement bay it parks in (`MIDTOWN.under.bays`, matched by name, else the first free one it fits); it comes up the FRONT lift and goes down the BACK lift, so no x/y/z |
| `trim` | flown pieces only: `{in, out, lane, deadHung?, outSeen?}` — `in`/`out` are the piece's BOTTOM over the deck at its in- and out-trim; `lane` is the gap between the iron's pipes it flies in; `outSeen` (the masts): what some rows still see at out-trim, recorded because the fly roof leaves no higher trim — the checker passes it as INFO, not silently |
| `scenes` | when it is on (below) |
| `notes` | the designer's notes |

### `scenes` entries

- a bare number `n`: on for **every segment** of scene `n`, at `home`;
- `{n, seg?, at?, atBySeg?}`:
  - `seg`: only these segments of scene `n` (1-based; see the scene's `segments`);
  - `at`: an array of placements used instead of `home` in those segments. **An `at` shorter than `count` means only
    that many copies are on** (e.g. one kitchen bench on the loft);
  - `atBySeg`: `{ "<seg>": [placements] }` when the position changes between segments of one scene.

## A scene

| key | what |
|---|---|
| `n`, `title`, `act` | 1–26; acts 1 (1–13) and 2 (14–26) |
| `location` | in words |
| `look` | the opening lighting-intent tag (each segment has its own) — e.g. `interior-dawn-warm`, `night-exterior-moon` |
| `furnace` | `lit` / `dark`; `furnaceLitSegments` says which segments when only some are lit |
| `pieces` | every piece id on at any point in the scene (the unit set and the masking are always in it) |
| `segments` | `[{seg, location, look, pieces}]` — each place the scene moves through, in order; `pieces` lists the non-unit pieces on in that segment |
| `notes` | the staging in a few lines |

## Rules the plan keeps (check them if you move anything)

- Nothing that is not flown stands taller than **4.40** over the deck (the arch's height). The furnace's chimney and
  the loft's rafters stop exactly at 4.40.
- Flown pieces fly in the two **lanes between the venue's hanging-iron pipes**: SL lane x −4.30…−0.80, SR lane
  x +1.05…+4.60. The iron runs up/downstage at y 5.10–5.44 over the deck (world 5.90–6.24), with a walkway in the
  centre (x −0.80…+1.10). Anything wider crosses a pipe.
- An out-trim hides a piece only where NO row sees it: under the arch's header (the line from each eye through the header,
  y 4.40 at z 0) or behind the masking border — between the lines through its bottom (4.40) AND its top (5.00) at z 3.0.
  The phase-1 rule counted only the border's bottom edge, so a piece upstage of it showed over its top (the out-trims
  were raised 2026-10-16). Its top stays under the fly roof (15.20 over the deck). `tools/jt-set-check.py` computes it
  for seven eyes down the centre of the stalls (front row 0.32 at z −4.30 to the back 3.10 at z −16.30).
- The centre path (x −0.60…+1.00, between the loft's SR posts and the wharf) is kept clear to the stage doors
  (x −1.0…+1.0, 3.40 high, in the back brick at z 6.60).
- No two pieces on in the same segment overlap (checked by a script on every placement; hand props excluded).
- **The lifts (RULING GI; CONTRACT.md):** front x −3.00…+3.00, z 0.30…2.70 (brings big sets ON); back x −2.50…+2.50,
  z 3.60…6.00 (takes them OFF). The unit set never stands on either. A wagon's layout fits the back lift (5.0 × 2.4, 5 cm
  a side) and so the front. In a change where a lift moves (a wagon leaves: the back; one arrives: the front), nothing that
  stays on stage through the change stands on that lift's footprint (hand props excepted: actors carry them).
- **Keep-outs:** the underground's stair hole in the SL wing (x −9.40…−6.25, z 1.70…6.30, guard-railed; RULING GJ):
  nothing stands on it, parks on it, or glides across it between its wing spot and the stage.
  The **worklight walkway** (x −9.40…−4.30, z 0.65…1.45: the lane from the stage to Theatre 2's worklight switch on the SL
  wall, PR #5) is a FLOOR keep-out the same way for set pieces (the page's `JT.walkways`; lights may stand or hang over it). The SL wing's parks are
  therefore `parks['SL wing']`'s rects (behind the legs, and the strip downstage of the hole).
- **A shift** (the page) runs strike → re-set → big sets off (back lift → bay) → big sets on (bay → front lift) → set →
  lights; `MIDTOWN.jt.check()` proves for every shift in show order that no re-set or wagon glide sweeps through what is
  standing, that nothing shares a footprint after the set, and that each big set leaves only from the stage and arrives
  only from its bay.
- **The checker:** `python tools/jt-set-check.py` (`-v` lists the changes that move a lift) — overlaps, support (a raised
  piece stands on something on), the deck, heights and trims, storage (the wings' spots never collide while parked
  together; backstage pieces pass the centre doors), the lifts, and the sightlines from the stalls' extreme seats. The page
  has its own: `MIDTOWN.jt.check()`.
