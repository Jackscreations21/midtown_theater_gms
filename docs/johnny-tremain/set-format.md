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
| `storage` | where it is when off: `{where, x, y, z, rotY, note?, fits}`; `where` is a `parks` key; `fits` says whether its narrow side fits that place, measured |
| `trim` | flown pieces only: `{in, out, lane, deadHung?}` — `in`/`out` are the piece's BOTTOM over the deck at its in- and out-trim; `lane` is the gap between the iron's pipes it flies in |
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
- An out-trim hides a piece only above the front row's sightline: `y = 0.32 + 0.559 (z + 4.30)` upstage of the
  masking border (z 3.0), `y = 0.32 + 0.949 (z + 4.30)` without it. The fly roof is 15.20 over the deck.
- The centre path (x −0.60…+1.00, between the loft's SR posts and the wharf) is kept clear to the stage doors
  (x −1.0…+1.0, 3.40 high, in the back brick at z 6.60).
- No two pieces on in the same segment overlap (checked by a script on every placement; hand props excluded).
