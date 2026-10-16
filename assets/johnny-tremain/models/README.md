# Johnny Tremain — the set models: where each one goes

Every piece of the set (`assets/johnny-tremain/set.json`) stands in `midtown.html`'s Theatre 2 as a **stand-in** made of boxes and
cylinders at its real size. To swap a stand-in for a real model, drop a GLB in this folder and add one line to
`manifest.json`. Nothing else changes: the page reads the manifest at load, loads each GLB it lists, fits it to the
piece's size and hides the stand-in. A piece not in the manifest keeps its stand-in (and the page fetches nothing for it).

## Where it stands (2026-10-16)

**45 pieces are fitted** from Jack's downloads by `tools/jt-fit/` (one recipe per piece in `tools/jt-fit/recipes/`; rebuild
any piece with the command in `tools/jt-fit/README.md`). **35 are committed**. **10 are local only**: the armchair, bench,
kitchen table, kitchen benches, trestle table, workbench, door frame, window flat, shop doors and warehouse corner. Those
were made from CGTrader downloads, whose royalty-free and editorial licences do not allow passing the model file on, so
they are `.gitignore`d and marked `"local": true` in the manifest. The page tries them only when it is served from this
machine; on Pages those pieces keep their stand-ins.

`ladder.glb` is CC BY-SA 4.0, because it is a changed copy of "Wooden Ladder" by romullus.

**Not fitted, so the stand-in stays:**
- **The printing press and the smashed press.** The download is a squat box with rollers, not a press.
- **The crates and the tea chests.** The crate download is a shallow open tray; a closed box would mean modelling from scratch.
- **The Observer and Afric Queen signs.** The Colonial House has no swing sign.
- **The candelabra, candlesticks, tankards and lumber piles.** Not downloaded yet.
- **The bench tools.** Optional.
- **Every piece with no worklist model.** See the table.

## The recipe (one model)

1. Do the worklist's routine in Blender (import, scale, decimate if it says so, retexture if it says so).
2. Export **glTF Binary (.glb)**, Y up (Blender's default), **named exactly as the table says** (`<piece id>.glb`), into this folder.
3. Add its line to `manifest.json` inside `"models": { }` (comma between lines):
   ```json
   "ladder": { "file": "ladder.glb", "rotY": 0, "fit": "auto" }
   ```
   - `rotY` (degrees): turns the model before fitting, if its front does not face the audience. Front means the side
     that faces the house when the piece stands at rotY 0 in set.json. A Sketchfab model whose front is +Z needs `180`.
   - `fit`: `auto` scales the model (uniformly, never stretched) so its LARGEST target dimension matches; or `"w"`, `"h"`,
     `"d"` to match that one (e.g. `"h"` for a chair whose width the model gets differently). The model is then centred on
     the piece's footprint with its lowest point on the floor.
4. Reload the page. The Johnny Tremain panel says how many models are slotted; **Check** (or `MIDTOWN.jt.check()` in
   the console) measures the fitted size. A model that fails to load is a console warning and the stand-in stays.
5. A CC BY / CC BY-SA model needs its line in `docs/johnny-tremain/PROGRAMME-CREDITS.md` kept (it is already there).

Size: keep each GLB small (the worklist's decimate targets); the page loads them all at start. Textures 1K–2K.

## Every piece

Size is **width × height × depth** in metres (width across the stage, depth up/down stage, at rotY 0). Pieces with
**no worklist model** ("—") are the ones the worklist lists as Still missing, or never had: model them from scratch, or
leave the stand-in. **×n** = how many copies stand on stage (one model serves them all).

| piece id → file | what it is | worklist model | size w × h × d (m) | ×n | licence |
|---|---|---|---|---|---|
| `wharf-deck.glb` | Wharf deck (the unit platform, stage right) | Rustic Wooden Dock | 2 × 0.45 × 3.35 | 1 | CC BY: print the credit line |
| `wharf-step.glb` | Wharf step | Rustic Wooden Dock | 2 × 0.22 × 0.3 | 1 | CC BY: print the credit line |
| `wharf-piles.glb` | Wharf piles and bracing (upstage edge) | The Wharf – Fishing Harbor Wood | 2 × 1.4 × 0.2 | 1 | CC BY: print the credit line |
| `loft.glb` | The loft (deck, four posts, rail) | Free Wooden Scaffolding Set | 2 × 3.5 × 3.6 | 1 | CC BY: print the credit line |
| `loft-rafters.glb` | Loft rafters (open A-frame over the loft) | Free Wooden Scaffolding Set | 2 × 2 × 3.6 | 1 | CC BY: print the credit line |
| `ladder.glb` | Loft ladder | Wooden Ladder | 0.45 × 2.9 × 0.8 | 1 | CC BY-SA 4.0: a changed copy passed on (the stage file shared) must carry CC BY-SA |
| `furnace.glb` | Lapham furnace (hearth, hood, chimney) | Forge And Bellow | 1 × 4.4 × 0.8 | 1 | CC BY: print the credit line |
| `bellows.glb` | Furnace bellows | Bellows | 0.4 × 0.5 × 1.1 | 1 | CC BY: print the credit line |
| `lumber-pile-a.glb` | Lumber pile on the wharf | Old lumber stack (Megascans) | 1.2 × 0.7 × 0.55 | 1 | Fab licence (not CC): read the Fab page's licence panel on download; no credit line |
| `lumber-pile-b.glb` | Lumber pile under the loft | Old lumber stack (Megascans) | 0.8 × 0.6 × 1.6 | 1 | Fab licence (not CC): read the Fab page's licence panel on download; no credit line |
| `crates.glb` | Wharf crates | Wooden Crate 1 | 0.5 × 0.5 × 0.5 | 3 | CC0 (ShareTextures) |
| `bench.glb` | The bench (the unit set's one plain bench) | Wooden table with benches | 1.6 × 0.45 × 0.35 | 1 | CGTrader royalty-free, NO AI USE; no credit |
| `masking-legs.glb` | Black masking legs (3 pairs, dead-hung) | — | 1.6 × 5 × 0.05 | 6 | no model yet (worklist 'Still missing' or not in the worklist): model from scratch |
| `masking-border.glb` | Black masking border (dead-hung) | — | 12.4 × 0.6 × 0.05 | 1 | no model yet (worklist 'Still missing' or not in the worklist): model from scratch |
| `observer-sign.glb` | The Boston Observer's swing sign (the spyglass man) | Colonial House | 0.9 × 0.8 × 0.1 | 1 | EDITORIAL ONLY: previs use only until the author grants permission for a ticketed show |
| `steeple.glb` | Christ Church steeple cut-out (with the two lantern windows) | Church steeple with cross | 1.8 × 5 × 0.1 | 1 | CC BY: print the credit line |
| `church-lanterns.glb` | The two church lanterns (in the steeple) | Colonial Style Lantern | 0.3 × 0.45 × 0.3 | 2 | CC BY: print the credit line |
| `ship-masts.glb` | Tea ship's masts and rigging (silhouette) | Pirate Ship (galleon) | 3.1 × 8 × 0.1 | 1 | CC0 (OpenGameArt) |
| `apple-branches.glb` | Apple branches (two cut-out borders) | — | 3.2 × 1.1 × 0.6 | 2 | no model yet (worklist 'Still missing' or not in the worklist): model from scratch |
| `armchair.glb` | The armchair (red, bow-back Windsor with arms) | Windsor Chair | 0.65 × 1 × 0.6 | 1 | CGTrader royalty-free, NO AI USE (may not be fed to AI training); no credit |
| `kitchen-table.glb` | Kitchen table (scrubbed pine; re-dressed per house) | Wooden table with benches | 1.8 × 0.74 × 0.8 | 1 | CGTrader royalty-free, NO AI USE; no credit |
| `kitchen-benches.glb` | Kitchen benches | Wooden table with benches | 1.6 × 0.45 × 0.3 | 2 | CGTrader royalty-free, NO AI USE; no credit |
| `kitchen-chairs.glb` | Plain kitchen chairs | — | 0.45 × 0.9 × 0.45 | 2 | no model yet (worklist 'Still missing' or not in the worklist): model from scratch |
| `workbench.glb` | Silversmith's bench (notched top) | Workbench and workshop accessories | 1.8 × 0.9 × 0.7 | 1 | CGTrader royalty-free; no credit |
| `bench-tools.glb` | Silversmith's tools (cluttered and neat dress) | Free Blacksmith Tool Set | 0.8 × 0.15 × 0.4 | 1 | itch.io free / pay-what-you-want, not CC; credit optional |
| `polishing-wheel.glb` | Polishing wheel (treadle) | — | 0.8 × 1.1 × 0.6 | 1 | no model yet (worklist 'Still missing' or not in the worklist): model from scratch |
| `water-bucket.glb` | Water bucket | — | 0.32 × 0.3 × 0.32 | 1 | no model yet (worklist 'Still missing' or not in the worklist): model from scratch |
| `crucible-and-tongs.glb` | Crucible, tongs and the mould | — | 0.4 × 0.15 × 0.2 | 1 | no model yet (worklist 'Still missing' or not in the worklist): model from scratch |
| `hancock-creamer.glb` | Hancock's silver cream pitcher (winged handle) | — | 0.15 × 0.15 × 0.1 | 1 | no model yet (worklist 'Still missing' or not in the worklist): model from scratch |
| `parrot-cage.glb` | Parrot in a cage | — | 0.4 × 0.6 × 0.4 | 1 | no model yet (worklist 'Still missing' or not in the worklist): model from scratch |
| `family-bible.glb` | The great family Bible | — | 0.35 × 0.12 × 0.45 | 1 | no model yet (worklist 'Still missing' or not in the worklist): model from scratch |
| `three-boy-bed.glb` | The three-boy bed (on the loft) | Indian Bed (Charpayi) | 1.9 × 0.5 × 1.4 | 1 | CC BY: print the credit line |
| `truckle-beds.glb` | Truckle beds | Trundle Bed | 0.9 × 0.3 × 1.8 | 2 | TurboSquid royalty-free; Maya-only file (needs converting) |
| `feather-bed.glb` | Aunt Jenifer's feather bed | Indian Bed (Charpayi) | 1.4 × 0.8 × 1.9 | 1 | CC BY: print the credit line |
| `trestle-table.glb` | Loft trestle table (the Observers' long table) | Wooden table with benches | 1.8 × 0.74 × 0.6 | 1 | CGTrader royalty-free, NO AI USE; no credit |
| `punch-bowl.glb` | Punch bowl | — | 0.4 × 0.2 × 0.4 | 1 | no model yet (worklist 'Still missing' or not in the worklist): model from scratch |
| `tankards.glb` | Pewter tankards | Pewter Tankard | 0.1 × 0.17 × 0.1 | 8 | RenderHub free, commercial use; credit optional |
| `lyte-table.glb` | Lyte's dining table (mahogany, Marlborough legs) | Mahogany Table (c.1880) | 2.2 × 0.73 × 1.1 | 1 | CC BY: print the credit line |
| `lyte-chairs.glb` | Lyte's dining chairs | Side Chair, Pergolesi style c.1785 | 0.5 × 0.95 × 0.5 | 6 | CC0 (Smithsonian) |
| `sideboard.glb` | Lyte's sideboard | — | 1.8 × 0.95 × 0.55 | 1 | no model yet (worklist 'Still missing' or not in the worklist): model from scratch |
| `candelabra.glb` | Candelabra and candlesticks (Lyte's) | Brass Candleholders | 0.35 × 0.5 × 0.35 | 3 | CC0 (Poly Haven) |
| `candlesticks.glb` | Single candlesticks | Brass Candleholders | 0.12 × 0.35 × 0.12 | 3 | CC0 (Poly Haven) |
| `lyte-cup.glb` | The Lyte cup (hero) and its three brothers | Antique Silver Goblets Type A | 0.12 × 0.29 × 0.12 | 4 | CC BY: print the credit line |
| `clerk-desks.glb` | Clerks' high desks | Desk (lectern) | 0.9 × 1.15 × 0.6 | 3 | CC BY: print the credit line |
| `clerk-stools.glb` | Clerks' tall stools | Painted Wooden Stool | 0.35 × 0.75 × 0.35 | 3 | CC0 (Poly Haven) |
| `low-stool.glb` | Low stool | Painted Wooden Stool | 0.35 × 0.58 × 0.35 | 1 | CC0 (Poly Haven) |
| `lyte-great-chair.glb` | Lyte's great chair (counting house) | — | 0.8 × 1.2 × 0.75 | 1 | no model yet (worklist 'Still missing' or not in the worklist): model from scratch |
| `printing-press.glb` | The Observer's press (intact) | Gutenberg-style printing press | 1.1 × 1.95 × 2 | 1 | CC BY: print the credit line |
| `printing-press-smashed.glb` | The Observer's press (smashed) | Gutenberg-style printing press | 1.5 × 1.2 × 2.2 | 1 | CC BY: print the credit line |
| `type-case.glb` | Type case on its stand | — | 1 × 1.4 × 0.5 | 1 | no model yet (worklist 'Still missing' or not in the worklist): model from scratch |
| `counter.glb` | Print-shop counter | — | 1.6 × 1 × 0.6 | 1 | no model yet (worklist 'Still missing' or not in the worklist): model from scratch |
| `drawing-board.glb` | Drawing board (sloped table) | — | 1 × 1 × 0.8 | 1 | no model yet (worklist 'Still missing' or not in the worklist): model from scratch |
| `observer-sign-smashed.glb` | The Observer's sign, stamped to kindling | Colonial House | 0.9 × 0.15 × 0.6 | 1 | EDITORIAL ONLY: previs use only until the author grants permission for a ticketed show |
| `sea-chest.glb` | Johnny's sea chest | — | 0.9 × 0.5 × 0.5 | 1 | no model yet (worklist 'Still missing' or not in the worklist): model from scratch |
| `door-frame.glb` | Free-standing door frame (with door) | Colonial House | 1.3 × 2.4 × 0.3 | 1 | EDITORIAL ONLY: previs use only until the author grants permission for a ticketed show |
| `window-flat.glb` | Free-standing window flat | Colonial House | 1 × 2 × 0.1 | 1 | EDITORIAL ONLY: previs use only until the author grants permission for a ticketed show |
| `shop-doors.glb` | Street of shop doors (carried by the company) | Colonial House | 1 × 2.1 × 0.1 | 4 | EDITORIAL ONLY: previs use only until the author grants permission for a ticketed show |
| `gravestone.glb` | Gravestone | — | 0.6 × 0.9 × 0.12 | 1 | no model yet (worklist 'Still missing' or not in the worklist): model from scratch |
| `mounting-block.glb` | Mounting block / step | — | 0.6 × 0.45 × 0.45 | 1 | no model yet (worklist 'Still missing' or not in the worklist): model from scratch |
| `hitch-rail.glb` | Hitching rail and straw | — | 2.5 × 1.1 × 0.4 | 1 | no model yet (worklist 'Still missing' or not in the worklist): model from scratch |
| `judge-platform.glb` | the Justice's platform (a low rostrum under the judge's bench and chair) | — | 2.8 × 0.3 × 1.8 | 1 | no model yet (worklist 'Still missing' or not in the worklist): model from scratch |
| `judge-bench.glb` | The Justice's bench | Courtroom Judge Desk | 2.4 × 1.5 × 0.9 | 1 | CC BY: print the credit line |
| `judge-chair.glb` | The Justice's high-backed chair | — | 0.6 × 1.4 × 0.6 | 1 | no model yet (worklist 'Still missing' or not in the worklist): model from scratch |
| `bar-rail.glb` | The bar rail (court) | Wooden Fence Painted White | 3.6 × 1 × 0.1 | 1 | CC BY: print the credit line |
| `ship-rail.glb` | The Dartmouth's rail | Rustic Wooden Dock | 4.8 × 1 × 0.25 | 1 | CC BY: print the credit line |
| `tea-chests.glb` | Tea chests | Wooden Crate 1 | 0.5 × 0.5 × 0.5 | 12 | CC0 (ShareTextures) |
| `plank-run.glb` | Plank run to the lip (the wharf's end; the ferry slip) | Rustic Wooden Dock | 1.2 × 0.08 × 5.2 | 1 | CC BY: print the credit line |
| `tents.glb` | Camp tents (forced perspective, 3 sizes) | Stylized Low-Poly Medieval Camping Tent | 2.1 × 2 × 2.1 | 3 | CC BY: print the credit line |
| `stacked-arms.glb` | Stand of stacked muskets | British Land Pattern Musket (Brown Bess) | 0.9 × 1.6 × 0.9 | 1 | CC BY: print the credit line |
| `rope-line.glb` | Rope line on stanchions | — | 5 × 0.9 × 0.1 | 1 | no model yet (worklist 'Still missing' or not in the worklist): model from scratch |
| `redcoat-muskets.glb` | Redcoats' muskets | British Land Pattern Musket (Brown Bess) | 0.06 × 1.58 × 0.12 | 8 | CC BY: print the credit line |
| `rab-musket.glb` | Rab's musket (Pumpkin's, re-stocked) | British Land Pattern Musket (Brown Bess) | 0.06 × 1.58 × 0.12 | 1 | CC BY: print the credit line |
| `grandsire-gun.glb` | Grandsire Silsbee's old gun | 18th Century Musket Replica | 0.06 × 1.5 × 0.12 | 1 | CC BY: print the credit line |
| `powder-horn.glb` | Powder horn | Powder Horn 1775 (Massachusetts Historical Society) | 0.33 × 0.1 × 0.1 | 1 | CC BY: print the credit line |
| `drum.glb` | Regimental drum | Rope-Tuned Wooden Drum | 0.4 × 0.4 × 0.4 | 1 | CC BY: print the credit line |
| `fife.glb` | Fife | — | 0.4 × 0.02 × 0.02 | 1 | no model yet (worklist 'Still missing' or not in the worklist): model from scratch |
| `flag.glb` | The King's Colour on a pike | — | 1.5 × 3 × 0.05 | 1 | no model yet (worklist 'Still missing' or not in the worklist): model from scratch |
| `hurdles.glb` | Jumping hurdles (two rails) | — | 2.4 × 0.9 × 0.3 | 2 | no model yet (worklist 'Still missing' or not in the worklist): model from scratch |
| `campfires.glb` | Camp fires (practicals) | — | 0.6 × 0.3 × 0.6 | 2 | no model yet (worklist 'Still missing' or not in the worklist): model from scratch |
| `clothesline.glb` | Clothesline on two posts, with sheets | — | 4.4 × 1.9 × 0.1 | 1 | no model yet (worklist 'Still missing' or not in the worklist): model from scratch |
| `laundry-basket.glb` | Lydia's basket of wet sheets | Laundry Baskets | 0.65 × 0.3 × 0.45 | 1 | CC BY: print the credit line |
| `afric-queen-sign.glb` | The Afric Queen's swing sign | Colonial House | 0.9 × 0.6 × 0.05 | 1 | EDITORIAL ONLY: previs use only until the author grants permission for a ticketed show |
| `saddle-stand.glb` | Saddle stand with the campaign saddle and bridle | Leather Riding Saddle Set – Tooled & Worn | 0.5 × 1.2 × 0.9 | 1 | CC BY: print the credit line |
| `sofa.glb` | Sofa (dove-grey drawing room; Warren's surgery) | — | 1.9 × 0.9 × 0.8 | 1 | no model yet (worklist 'Still missing' or not in the worklist): model from scratch |
| `mirror.glb` | Cheval mirror | — | 0.7 × 1.9 × 0.4 | 1 | no model yet (worklist 'Still missing' or not in the worklist): model from scratch |
| `dressing-table.glb` | Dressing table (Lavinia's room, Milton) | — | 1 × 1.5 × 0.5 | 1 | no model yet (worklist 'Still missing' or not in the worklist): model from scratch |
| `wig-stand.glb` | Wig stand with Lyte's best wig | — | 0.3 × 1.6 × 0.3 | 1 | no model yet (worklist 'Still missing' or not in the worklist): model from scratch |
| `lantern.glb` | Hand lantern | Colonial Style Lantern | 0.3 × 0.45 × 0.3 | 1 | CC BY: print the credit line |
| `torches.glb` | Torches on stands | — | 0.3 × 1.8 × 0.3 | 2 | no model yet (worklist 'Still missing' or not in the worklist): model from scratch |
| `ruby-coach.glb` | The Lytes' ruby coach (half-coach) | 19th Century Carriage | 2 × 2.1 × 1.3 | 1 | CC BY: print the credit line |
| `chaise.glb` | Two-wheeled chaise (Grandsire's) | — | 1.6 × 1.8 × 2.6 | 1 | no model yet (worklist 'Still missing' or not in the worklist): model from scratch |
| `warehouse-corner.glb` | Warehouse / tavern corner (an L of two flats) | Colonial House | 1.6 × 3.6 × 0.6 | 1 | EDITORIAL ONLY: previs use only until the author grants permission for a ticketed show |
| `tanning-shed.glb` | Tanning shed (lean-to) | — | 1.6 × 2.2 × 1.2 | 1 | no model yet (worklist 'Still missing' or not in the worklist): model from scratch |
| `pump.glb` | Village pump | — | 0.4 × 1.4 × 0.6 | 1 | no model yet (worklist 'Still missing' or not in the worklist): model from scratch |
| `flour-barrel.glb` | Flour barrel | — | 0.6 × 0.85 × 0.6 | 1 | no model yet (worklist 'Still missing' or not in the worklist): model from scratch |
| `well.glb` | Well with windlass | — | 1.2 × 1.8 × 1.2 | 1 | no model yet (worklist 'Still missing' or not in the worklist): model from scratch |
| `belfry.glb` | Lexington meeting house's tiny belfry | — | 0.9 × 1.4 × 0.9 | 1 | no model yet (worklist 'Still missing' or not in the worklist): model from scratch |

The manifest line for any of them is `"<piece id>": { "file": "<piece id>.glb", "rotY": 0, "fit": "auto" }`.

**Editorial-only models** (the Colonial House pieces: the door frame, window flat, shop doors, signs, warehouse corner) are
fine in this previs; the worklist says to get the author's permission before any of it appears in the real show.
