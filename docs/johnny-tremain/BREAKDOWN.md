# Johnny Tremain — the breakdown (Theatre 2)

Jack's comedy in two acts, 26 scenes (Act One 1–13, about 65 minutes; Act Two 14–26, about 60), on **Theatre 2** of
`midtown.html`. Read with the ground plan [`assets/johnny-tremain/set.json`](../../assets/johnny-tremain/set.json)
(format: [set-format.md](set-format.md)) and the lighting brief [LIGHTING-NEEDS.md](LIGHTING-NEEDS.md).

Sources: Jack's script (82 pages, read in full including the production notes) and his set-models worklist. The
repository is public, so **nothing here quotes the script**: staging, sets and light are described in my own words.
Positions are in the **stage frame**: **+x = stage right** (house left), **z = metres upstage of the proscenium plane**
(negative = the apron), y up from the deck; `world = (20.00 + x, 0.80 + y, 2.30 + z)`.

## The stage as measured (not as the worklist has it)

Read off `assets/midtown-auditorium.glb` (Theatre 2 is the uncut scan at x +20) and checked against `midtown.html`.

| | measured | his worklist |
|---|---|---|
| Opening | **8.60 × 4.40** (world x 15.70…24.30; deck y 0.80 to header 5.20) | 8.6 × 4.4 ✔ |
| Depth | **6.60** to the back brick (deck runs to 6.70) + **2.65** apron | 6.6 + 2.65 ✔ |
| "Side walls 11.6 apart" | **11.55 is the apron's width** (house walls at world x 14.40 / 25.95). The **stage house** walls are **~19.0 m apart** (x 10.5 / 29.6) | ✘ misread |
| Wings | **SL 5.15 m** the full depth. **SR 5.30 m** upstage of z 1.60, but **only 1.70 m** (x +4.30…+6.00) downstage of it: a side room (world x 25.95–29.56, z 0.85–3.90, ceiling 4.46) fills the SR corner | "about 1.5 m"; the 1.3 m rule is not needed |
| Fly tower | roof at **15.20 over the deck** (world y 16.0). Empty above the venue's iron | 16 m (to the house floor) ✔ |
| The venue's iron | four pipes running **up/downstage** (not across) at 5.10–5.44 over the deck, at world x 15.70, 19.2 (pair), 21.05, 24.6, z 2.6…8.9; a walkway down the centre (x 19.2…21.1) | not mentioned |
| Stage doors | a pair, **2.0 wide × 3.40 high**, upstage centre in the back brick (stage x −1…+1), swinging into the backstage crossover (4.1 m deep, the whole width) | not mentioned |

Two consequences the worklist did not have: (1) the front row sits so close and low (eye 0.32 m over the deck, 4.3 m
from the arch) that it sees **10.5 m up the back wall** through the arch — nothing taller than ~4.7 m hides when
flown out unless a masking border is hung (with the border this plan adds, ≤ ~8.9 m); (2) flown pieces must fit
the **3.5 m lanes between the iron's pipes** (SL x −4.30…−0.80, SR x +1.05…+4.60), or Jack has Theatre 2's iron cut
as house 1's was.

## The ground plan

Drawn as the house sees it — **stage right on the LEFT of the drawing**, upstage at the top:

```
 z 6.60 ════════ back brick ══════════════[ stage doors x +1…−1 ]════════════════════════
         SR wing (5.3 m)                                                    SL wing (5.15 m)
 z 6.20      ┌──── WHARF DECK top 0.45 (x +4.4…+1.0) ──┐  centre ┌──── LOFT deck 2.40 (x −0.6…−4.2) ──┐
   L3 z4.6   │ lumber   (tents / judge's bench)  crates │  path   │ lumber b │ PRESS (9→) │ FURNACE ◄ │   L3
             │                         bench           │  to the │          │            │ bellows   │
 z 3.60      └──────────── step z 3.30–3.60 ───────────┘  doors  └────────[ladder x −1.0]────────────┘ z 4.40
 z 3.00  · · · · · · · · · · · · · · · masking border (bottom 4.40) · · · · · · · · · · · · · · · · ·
   L2 z2.6                     OPEN ACTING FLOOR  z 0 … 3.30, x −4.3 … +4.3                         L2
   L1 z0.6   (SR pocket 1.7 m)                                                                      L1
 z 0     ═══════════════════ proscenium  x +4.30 … −4.30 ═════════════════════
 z −2.65 ··········· apron  x +5.95 … −5.60 (the lip; Johnny's narrator spot DSR) ···········
```

- **The unit set, upstage, never moves.** Stage left: **the loft** (3.6 × 1.8, deck at 2.40, four posts, a 1.1 m
  rail with a 0.6 m gap where **the ladder** arrives, an open A-frame of **rafters** to 4.40 that Otis pushes on);
  under its SL end **the furnace**, its mouth turned to stage right so Johnny works it in profile, the chimney up
  through the loft, **the bellows** on its downstage side. The under-loft is the Lapham kitchen's hearth corner,
  then (from Scene 9) the Observer's press room. Stage right: **the wharf deck** (3.4 × 2.6, 45 cm high, one 22 cm
  step), piles and bracing along its back, lumber and crates on it, **the bench** on its front edge.
- **Between them a 1.6 m centre path** runs from the open floor to Theatre 2's stage doors: an upstage-centre
  entrance (Rab leaving Boston, the brigade, the dead at the finale) and the route big pieces take to the backstage
  crossover.
- **The open floor** (z 0…3.3 behind the arch, plus the 2.65 m apron) is where the company builds every other
  place by standing in it. Travelling furniture sets there and leaves to the wings within ten seconds.
- **Masking** (my addition; Jack's call): three pairs of black legs at z 0.6 / 2.6 / 4.6 (inner edges |x| 4.6) and
  one border at z 3.0. Without them the side seats look straight into both wings and the front rows up into the
  tower.
- **Storage:** both wings (SL ~18 m², SR ~15 m² offstage of the legs), props tables SL and SR, and the backstage
  crossover through the centre doors for pieces used in one stretch of the show. Flown: the Observer's sign, the
  steeple, the masts, the apple branches.

## Scene by scene

Look tags are the lighting intent; LIGHTING-NEEDS.md turns them into colour. "On" lists the travelling pieces and
where they stand; the unit set is on in every scene and is named only when it is used.

### ACT ONE

**1. Up and About** — Act 1 · the Lapham loft and kitchen, then the street on the apron · early morning, July 1773 · interior then exterior.
- *Unit set:* the loft (three boys in one bed), the ladder (Johnny leaps for it, Dove trips him at it), the furnace as the kitchen hearth (Mrs. Lapham at the fire).
- *On:* three-boy bed on the loft; kitchen table (x −1.8, z 2.0) with two benches; the armchair in Mr. Lapham's corner (x −3.6, z 2.3, angled to the house); the bucket. The company crosses the apron as the town (wheelbarrow, goose, the parrot in its cage).
- *Changes:* none — the show opens on the full set revealed.
- *Practicals:* optional ember in the hearth (the script keeps the furnace dark until 6).
- *Light:* darkness, a gull, a bell; Johnny enters **from the back of the house down an aisle** (followspot from the booth) and hops up onto the stage; the **loft isolates** on the three boys; the kitchen warms up below as he climbs down; at the town's entrance the **apron floods bright** as the street while the kitchen stays lit behind; his asides to the house throughout (narrator special DSR / followspot).

**2. Pride Goeth** — Act 1 · the Lapham kitchen · morning · interior.
- *On:* as 1 (no change), the great family Bible on the table.
- *Light:* warm breakfast interior; a narrator pull for the asides; the bed on the loft goes dark (struck in the 2→3 change).

**3. The Sugar Basin** — Act 1 · the Lapham shop · day · interior.
- *Unit set:* the furnace, **dark** (the script; the worklist said it glows here).
- *On:* the silversmith's bench (x −1.6, z 2.9) cluttered with tools; the polishing wheel (x +0.4, z 3.0) with Dove and Dusty; the armchair moved to the shop corner; the door frame as the shop door to the street (x +3.6, z 1.6, angled). Hand: Hancock's silver creamer, the coins, Mrs. Lapham's tart, the soap.
- *Changes in:* bench, wheel, door frame; *out:* table, benches.
- *Light:* bright working daylight from the street side (SR); Johnny turns the creamer in the light — a small lift on the bench; the girls' whispered chant to a tight close.

**4. The End of the Wharf** — Act 1 · the end of Hancock's Wharf · midnight to dawn · exterior.
- *On:* the **plank run** from mid-stage to the apron's lip (x +1.6, z −2.6…+2.6); one lantern on it. Johnny sits at its end legs dangling over the edge.
- *Changes out:* the whole shop.
- *Practicals:* the lantern.
- *Light:* **night, stars, moon**; the floor around the planks is **black water** (dark blue, a slow ripple gobo on the deck and apron); the cool breath of wind (a slight swell); **first grey of dawn on the water**, a cock crows, and the light rises on **the cup** as he unwraps it (**cup pin** at the lip) and on the two of them.

**5. Handles** — Act 1 · Paul Revere's shop, North Square · Friday evening · interior; then the bare apron.
- *On:* the bench moved to stage right (x +2.0, z 2.2) with the neat tool dress and a teapot.
- *Light:* **cleaner and better-lit than Lapham's** (cooler, crisper white); the drawing on the bench; then **Johnny crosses the empty apron homeward** — the shop fades, a travelling pool or followspot SR → SL at dusk.

**6. The Crucible** — Act 1 · the Lapham shop · Saturday afternoon, then Sunday dawn · interior.
- *Unit set:* **the furnace lit and glowing** (both halves); the bellows worked by Dusty.
- *On:* as 3 (bench, wheel, armchair, door frame); crucible, tongs, mould; the water bucket by the furnace (x −2.6, z 4.0).
- *Practicals:* the furnace glow (its own channel); the crucible of molten silver.
- *Light:* afternoon with the **furnace glow** building; Mr. Lapham's interruption; **blackout, a rooster**; **Sunday dawn, half light, the furnace roaring**; the pour — **the light of the crucible on Johnny's face** (a low orange special from the hearth side); the accident (a hard snap of the orange, then cold); **the light closes down to the bucket, the boy and the furnace** (a tight isolation at x −3.0, z 4.4), still glowing. End: the hand goes into the pocket.

**7. What Was Left** — Act 1 · the Lapham kitchen, weeks later · day · interior.
- *On:* table and benches; the **armchair moved centre** (x −0.3, z 1.2) with Johnny in it; a small kitchen chair in Mr. Lapham's corner. Furnace dark behind.
- *Light:* the same room greyer and flatter than 1–2 (time has passed); narrator asides; a gentle isolation on Mr. Lapham's corner for the last exchange.

**8. Another Boy** — Act 1 · the street · morning · exterior.
- *On:* the company carries on four shop doors in a row across the apron (x −3.6, −1.2, +1.2, +3.6; z −1.2) or stands as them. Bare stage behind.
- *Light:* bright street; **each door opens with its own slice of light** and shuts it off — faster and funnier until it is not; the street turns away and **Johnny stands alone in a shrinking pool**; Cilla enters with the lime (soften).

**9. Salt Lane** — Act 1 · the Boston Observer's print shop · day · interior.
- *On:* **the swing sign flies in** (SL lane, in front of the loft); **the press** comes on under the loft (x −2.3, z 5.2, its length up/downstage); type case (x −3.0, z 3.4, Rab sets type in profile); counter (x −1.0, z 2.2) with bread, cheese and a mug. *Must assemble in under ten seconds* — it recurs.
- *Light:* cool calm daylight (Rab's serenity); Johnny **shows the hand for the first time** — a small, quiet focus on the two at the counter.

**10. Let There Be Lyte** — Act 1 · three places in sequence · dawn, then day, then night.
- *Copp's Hill burying ground at dawn:* a single gravestone (x −2.6, z 0.9), bare stage, Johnny with the cup. **Cold dawn**, **cup pin** at the stone.
- *Lyte's counting house on Long Wharf:* a row of three tall desks and stools (x +0.9…+3.1, z 2.6), clerks perched facing the house; Lyte's great chair (x −1.4, z 1.6). Cool daylight, the clerks' scratching; Johnny pulls out the cup (followspot / pin).
- *The Lyte dining room, eight o'clock:* the long mahogany table (x +0.2, z 1.8) with six chairs (Lyte at the SR end, Lavinia at the far SL end, one empty), a candelabra on it; **the sideboard** (x −2.6, z 3.3) with three standing cups and a candlestick each end. **Candlelight**; Johnny sets the cup by its brothers: **the four cups gleam in a row** (a shuttered strip on the sideboard); Lavinia at the far end — **the light itself seems to warm for her** (a soft rosy lift); the arrest (cold).
- *Practicals:* candelabra (table) and the pair on the sideboard.

**11. Lyte v. Tremain** — Act 1 · the jail; the courtroom; the street outside · morning to noon.
- *Jail:* a cot (truckle bed #1, x −2.8, z 1.6) and a low stool. **The window is only a pattern of bars in light** (a bar gobo on the floor from high SL); next morning a little less serene.
- *Courtroom:* **the Justice raised on a platform** — the wharf deck is the platform (bench x +2.7, z 4.85, his high-backed chair behind); the dark bar rail across (x +0.6, z 2.3, a gate in it); crowd benches SL; the kitchen table inside the rail (x −0.4, z 3.0) with **the four cups** on it (**cup pin**); the judge's candlestick. The clock strikes eleven: **Rab and the hooded girl in the doorway** (a doorway backlight at the SL in-1 entrance); Isannah's charge down the room. Bright court daylight.
- *The street outside:* the empty apron in **sunshine**, a mounting block standing in for the step of Lavinia's gig.

**12. Goblin** — Act 1 · the yard behind the Observer · day · exterior.
- *On:* the sign (in) and the press seen through the door frame (x −2.3, z 3.7); a hitching rail and straw (x +1.6, z 1.0). **The company is the horse** — a lap of the yard.
- *Light:* warm open yard; room for the horse to explode and lap; Johnny's hand out holding the mane (no special — let it read).

**13. Salt-Water Tea** — Act 1 · the loft over the Observer; Old South Meeting House; the deck of the *Dartmouth* · late November, night.
- *The loft:* the **narrow trestle table** on the loft (x −2.25, z 5.6) with one bench behind it, the punch bowl, tankards; the Observers climb the ladder one at a time **until the loft is full** (a line of about six facing the house; the overflow hangs on the ladder and crowds its foot — the joke is that it is full). The press below. **Candle/lantern warmth in the loft, the stage below dark.**
- *Old South:* the loft furniture is handed down off its SL end and the loft goes dark; **the company crams the stage in the dark round a single lantern**; the war-whoop from the gallery (the house) and the boys run **down the house aisle** and out.
- *The Dartmouth:* **the ship's rail** across the arch line (x −3.0…+2.0, z 0.5); a dozen tea chests; **the masts fly in** behind the wharf; the harbour is the apron and the house — the tea goes over the rail toward the audience, and so does Dove (the script has him come up through a hatch; this stage has no trap, so he pops up from behind the tea chests). Montague watches from the apron. **Night harbour: moon, water ripple on the apron and spilling to the front rows**; the fife, the dance; Montague isolated; Johnny's interval line to the house; **the fife, blackout. END OF ACT ONE.**

### ACT TWO

**14. The Fiddler's Bill** — Act 2 · the wharf; the camp on the Common; North Square · June 1774, day.
- *The wharf by day:* the plank run, **the masts behind** (in); nobody working. Johnny comes down to the footlights. Grey, idle daylight.
- *The camp on the Common:* tents (one full size on the deck at x −2.4, z 2.3; two smaller on the wharf deck — forced perspective), **the stacked muskets** (x +0.3, z 1.6) just upstage of the **rope line** (z 1.0), redcoats with muskets. Hard bright sun; the mounted officer strikes Rab (a sharp hit on the moment); the medical officer's kindness (warm softening).
- *North Square, one o'clock:* bare, a mounting block (x +2.4, z 0.8). Noon sun; Miss Revere across the square.

**15. Commandeer** — Act 2 · the stable yard of the Afric Queen · day · exterior. Stays the whole scene.
- *On:* the door frame as the stable door (x +3.4, z 2.4, angled to the house; Goblin dances out of it); the clothesline with sheets across the yard (posts at x −2.9 and +1.5, z 1.6); Lydia's basket; **the tavern window above** = the window flat standing on the loft (Colonel Smith's red face appears in it); two tankards for Stranger.
- *Light:* bright windy day; **the sheet fills with wind like a sail** (backlit, it glows); the offstage fall into the puddle is sound; a pin on the window when Smith calls down.

**16. Queen of Spades** — Act 2 · the Lyte kitchen on Beacon Hill; the dove-grey drawing room; the kitchen again · day · interior.
- *On (played as a split stage so nothing moves):* kitchen stage right — table re-dressed (x +2.2, z 1.8), the kettle, Mrs. Bessie's chair (x +3.5, z 2.2); drawing room stage left — sofa (x −1.6, z 2.0), cheval mirror (x −3.2, z 2.6), costume pieces strewn, the military tailor on the floor.
- *Light:* the kitchen warm and below-stairs; the **drawing room dove-grey and silver-cool** (lavender-grey), Lavinia the brightest thing in it; cross-fade the two sides rather than change the set; the kitchen again for the brandy.

**17. The Haunted House** — Act 2 · the town gate on the Neck; the road; the Lyte house at Milton; the Milton road at dawn · late August, night to dawn. (One of the five long scenes.)
- *The gate, night:* **torches** on stands; a mob's howl; soldiers with torches; a guardhouse step (the mounting block, x −1.6, z 1.8); **the ruby coach: only its two lamps and a single wheel** (the half-coach at x +2.8, z 1.8, or just its lamps and wheel). **Flickering orange torchlight**; Cilla white on the box.
- *The road:* bare stage, **Warren's chaise as two chairs** side by side (z 1.0), the lantern; shapes and voices in the dark (night, moon).
- *Milton, the dining room:* Scene 10's long table with the **abandoned dinner**, chairs, the sideboard with **the four cups** (cup pin), candelabra; **Cilla lights candle after candle, twenty of them, until the room is bright** (a slow build of warm general, candle by candle).
- *Through the house by lantern:* Johnny's lantern **reveals one piece at a time** — Lavinia's dressing table (x +3.4, z 2.7), the wig on its stand (x +3.0, z 1.2), a tipped chair (x +0.9, z 3.0), the family Bible: three small **reveal specials** that come up as the lantern reaches them.
- *The kitchen hearth:* **the furnace lit** as Milton's kitchen fire; he burns the pages (a flare of the hearth); he asks the house a question and waits (**the house light may lift a touch**); **every shutter closing is a bang from offstage** — each bang a step down in the light until the house is shut.
- *Dawn on the Milton road:* empty stage, **dawn crosslight**, a company of Minute Men crossing badly with a boy's fife; Johnny and Cilla together.
- *Practicals:* torches, coach lamps, the lantern, twenty candles, the hearth.

**18. Green Apples** — Act 2 · the orchard behind the Lyte house · late afternoon · exterior; then the loft windowsill.
- *On:* the bench moved to the orchard (x −1.6, z 2.7); **the apple branches fly in** (the SL one low enough that Cilla reaches up and picks a green apple); Pumpkin at the kitchen door (the SR in-1 entrance).
- *Light:* **dappled afternoon through leaves** (a leaf breakup gobo over the bench); **the sea as light downstage** (a blue-green shimmer on the apron); then a quick isolation of **the loft's rail as the windowsill** where the apple sits, and Rab appears chewing.

**19. A Man Can Stand Up** — Act 2 · the loft over the Observer, the last meeting; then the truckle beds · fall 1774, night. (Long scene.)
- *On:* as 13 — the trestle, one bench, the punch bowl (out from the start this time), tankards — plus **the armchair on the loft** at its SR end (x −0.93, z 5.6) for Otis. Then the table is struck and **two truckle beds** go down on the loft.
- *Light:* candlelit loft, fewer men; a footstep below and Rab at the ladder's head; **Otis pushing up against the rafters** (a top/back light that finds his raised hands on the rafters — the image Johnny asks the house to keep); later **moonlight on the truckle beds**; **Johnny alone to the house** — one of the two hinges of the play: hold it, do not rush the cue.

**20. Eyes and Ears** — Act 2 · seven places, winter to April.
- *The Green Dragon's back room:* kitchen table (x −1.2, z 1.8), two benches, **the Bible and candles** (candlesticks). Candle-lit conspiracy.
- *The Afric Queen yard:* clothesline, Lydia's basket, the stable door. Cold winter day.
- *The Observer:* the sign, the press, a **drawing board** (x −0.4, z 2.6); later Dove in a chair (x +1.0, z 1.6) with ale and the brandy. Lamplight; the sleet outside (narrated).
- *The Common, the hurdles:* two hurdles (x −1.8, z 1.4 and x +1.8, z 2.6); Stranger and Johnny jumping (the company as horses). Clean spring light.
- *The encampment and **the runaway**:* tents and stacked muskets, the half-shaved officer; then the horse bolts and **the company puts up and takes down every obstacle just as the horse gets to it** (tent pegs, **two campfires**, the stacked muskets, sheep, an orchard, a wall, a clothesline) — **chase lighting**: quick shifting pools and side-light that run ahead of the horse round the stage, as fast as it can go — and **ends dead still at the Lytes' back gate** (the door frame at x +3.2, z 1.8) in one still warm pool. Pumpkin grooming in the yard.
- *The loft:* Johnny's **sea chest** (on the loft, x −1.05), the smock — a quiet warm loft special; the company's chant as **the pewter goes into the crucible** (optional low furnace glow as the melt).
- *The salt marsh by the Charles:* empty but for the hurdles and **a drum**. April, early, grey. The brigade marches down on Johnny (he faces the house — the house is the brigade); **the firing squad behind him**; **the volley and the drum roll together** (a flash/hit upstage behind him — he sees it in the faces in front); then the squad passes close and **eight small round eyes** — a tight cold special on Johnny, the muskets' muzzles glinting as they pass. No jokes; isolation to the end.

**21. New Evolutions** — Act 2 · April 15–18, 1775 · the Afric Queen; the loft; Warren's surgery; the Dawes kitchen; North Square and Copp's Hill; the surgery again. (Long scene.) **The company announces each date like a striking clock; every section quicker** — snap transitions on each call.
- *The Afric Queen:* the order pinned on the stable door; then **the campaign saddle on a stand** (x +1.6, z 1.8) with the bridle, Dove polishing. Late-afternoon stable light.
- *The loft:* the truckle beds; Rab packing, leaving; **Johnny at the loft's rail (the window)** watching Rab say goodbye below and **go off up Salt Lane — out through the centre stage doors**, into light. Church bells.
- *Warren's surgery:* sofa (x −1.6, z 2.0) and a window flat (x −3.4, z 2.2). Lamplight; soldiers marching past outside (moving shadows through the window).
- *The Dawes kitchen:* one chair (x +2.2, z 1.6), a hat. Warm, comic; the wife's face after the door closes (isolate her).
- *North Square; Copp's Hill; Salem Street; the alley:* bare stage, the gravestone. **Night, moon up, tide coming**: lights across the water in Charlestown (low twinkles far upstage); Newman drops from a shed roof (the wharf deck's edge, not the loft); **the two lanterns appear, high up in the spire** (the steeple flies in at the SR lane, its two windows lit — the steeple is a light first, the cut-out barely seen). The harbour is sound.
- *The surgery again:* Revere and Warren; almost midnight; Johnny sleeps on the floor in a blanket. **Dawn: one far drum, a single shot, a volley** — sound against a dark stage with the first grey of dawn; Pitcairn's voice across water.

**22. Yankee Doodle** — Act 2 · April 19 · Warren's surgery at dawn; the street and the Common; Salt Lane; the pasture behind Beacon Hill.
- *The surgery at dawn:* sofa, window; cold first daylight; the scarlet river in the street (red moving light past the window).
- *The street and the Common:* empty stage; children chanting; **Percy's brigade** — the company in scarlet, **the King's colour** on a pike, drums, fifes; Percy riding a white horse; a breeze lifts the flag (a light lift on the flag); bright, hard morning; then the empty ground the army has left.
- *Salt Lane, wrecked:* **the smashed press** under the loft, the sign stamped to kindling on the floor, the boys' bed (truckle) ripped; opposite it **Aunt Jenifer's kitchen**: the **feather bed** (x +2.4, z 1.8) with feathers everywhere and her chair. Flat afternoon light; feathers in the air.
- *The pasture behind Beacon Hill:* a packed hillside looking north as **the sun goes down**, **the warships' riding lights**, and **musket flashes like fireflies** far off (tiny twinkles low on the back wall).

**23. Aunt Lavinia** — Act 2 · the Lyte kitchen; the front of the house beyond as light and noise · night · interior. Stays the whole scene.
- *On:* the kitchen table (x +1.6, z 1.8) and two chairs; **the door frame at the head of the centre path** (x +0.2, z 3.3) is the doorway Lavinia stands in, hood up, saying nothing — and **the stage doors behind it open**, the backstage spilling **warm light and noise** (the household packing: carts, trunks, the portraits).
- *Light:* kitchen low and warm; **Lavinia backlit in the doorway**; her one real laugh; her hand on his widow's peak; the scarlet coat goes on (Mrs. Bessie braids his hair); Johnny struts off down the hill (out through the centre).

**24. Across the Water** — Act 2 · the ferry slip at night; Charlestown; the Cambridge road and Menotomy; a well at the Lexington line · night to the next day.
- *The ferry slip:* the plank run as the slip, a warehouse corner (x −3.4, z 2.6), a tanning shed (x +3.3, z 2.3), **two torches**. **The boats are only light and sound, coming from the auditorium** (lantern light swinging in from the auditorium side onto the apron's lip); the townsmen whistling in the dark; Colonel Smith and Stranger lifted from a dory at the slip's end — **a torch lights Stranger's face** (Johnny takes him for Rab).
- *Charlestown:* the clothesline (the uniform hung on it), a pump, the warehouse corner as the tavern corner, a flour barrel. Moonlit garden, then the tavern's interior warmth.
- *The Cambridge road and Menotomy:* empty stage, **morning**, cold and bright; the burials (hats off).
- *A well at the Lexington line:* the well (x +0.6, z 1.6) and its wooden bucket; spring day; **eight names counted on her fingers** — still the light, let the names land.

**25. Better So** — Act 2 · Lexington Green; the back chamber upstairs at Buckman's · late afternoon. (Hinge.)
- *Lexington Green:* **the tiny belfry** on the wharf deck (x +2.6, z 5.45 — far off), Buckman's as a doorway (the door frame at x −2.8, z 2.4), the Harrington steps (mounting block). **Late afternoon, the shadows of new leaves** (leaf breakup, low and warm). When Warren tells him how bad it is, **the spring world goes black** around Johnny (a snap to a single pool).
- *The back chamber:* **the armchair** (Rab's now, x +0.3, z 1.6) with pillows; a window flat (x −2.4, z 2.8); **the musket in the corner**; **the pewter candlestick** on a stool. **Window light** from SL across Rab; quiet, still. Johnny tells the house he will stop talking for a bit — the second hinge: the cue waits.

**26. Stand Up** — Act 2 · Silsbee's Cove; the lower parlour at Buckman's; Lexington Green at sunset (the finale). (Long scene.)
- *Silsbee's Cove:* **the empty red armchair** by the hearth (the furnace, dark: x −2.6, z 3.0); hens as sound; Grandsire's gun and horn gone from over the hearth. Bright, empty, still day light.
- *The lower parlour:* the kitchen table (x +1.4, z 1.8), a chair, the window flat, the musket; Warren's chaise stands **offstage**. Window light; Warren examines the hand at the window — a clean, cool light on the hand.
- *Lexington Green at sunset, the finale:* **the unit set alone** (everything struck), **every member of the company** coming on in ones and twos as the land and its people; **the long light** of a sinking sun (low raking amber from the side), the ragged men marching home with the drum and the fife; **Grandsire's old chaise** crosses (from SL, off SR) with his gun across his knees; then **the dead among the company, Rab at the back** looking off after the marching men (a soft cool backlight on him up the centre path); Johnny's last turn to the house, **the hand open at his side**; the fife alone; **blackout**.

## Every lighting special the show needs

One list for the rig. Positions in the stage frame; "y" is the focus height. The full specification is in
LIGHTING-NEEDS.md.

| # | special | target | scenes |
|---|---|---|---|
| S1 | **Narrator DSR** — Johnny's home for the asides | apron SR, x +3.6, z −1.6, ~2.0 m pool | all |
| S2 | Narrator DSL (second side) | apron SL, x −3.6, z −1.6 | all |
| S3 | **Followspot** (Theatre 2's booth) — Johnny anywhere, the aisle entrance | the whole stage and the house aisle | 1, 5, 13, 17 and every aside |
| S4 | **Cup pin — the wharf's lip** | x +1.6, z −2.35, y 0.4 | 4 |
| S5 | **Cup pin — the sideboard**: the four cups gleaming in a row (shuttered strip 1.8 × 0.4) | x −2.6, z 3.3, y 1.1 | 10, 17 |
| S6 | **Cup pin — the courtroom table** (four cups) | x −0.4, z 3.0, y 0.9 | 11 |
| S7 | Cup at the gravestone (dawn) | x −2.4, z 0.7 | 10 (and 21's graves) |
| S8 | **Furnace glow** (practical LED in the hearth, own channel) + an orange low side-light from the hearth onto Johnny's face | hearth mouth x −3.4, z 5.0; face at x −3.0, z 4.6, y 1.5 | 1–2 (optional ember), 6, 17 (Milton's hearth), 20 (optional, the pewter) |
| S9 | **The crucible pour** — a hot snap, then the cold | x −3.0, z 4.6 | 6 |
| S10 | **Bucket, boy and furnace** isolation | x −3.0, z 4.4, r 1.3 | 6 (end) |
| S11 | **Loft isolation** (the whole loft; plus the ladder head) | x −2.4, z 5.3, y 2.4; ladder head x −1.0, z 4.4 | 1, 13, 15, 18, 19, 20, 21 |
| S12 | **Otis at the rafters** — top/back light on raised hands | x −2.0, z 5.3, y 4.2 | 19 |
| S13 | **Lavinia** — the light warms for her (soft rosy lift) | far end of the table x −1.25, z 1.8 | 10 |
| S14 | **The doorway** (backlight through the door frame / the open stage doors) | x +0.2, z 3.3 (23); the SL in-1 entrance (11) | 11, 23, 21 (Rab exits) |
| S15 | **Jail bars** (gobo from high SL onto the cot) | x −2.8, z 1.6 | 11 |
| S16 | **Window light** (low side through the window flat) | from SL across x 0…−2 | 21, 22, 25, 26 |
| S17 | **Water** — rippling blue on the apron and DS floor; spills to the front rows | z −2.65…+1.0, full width | 4, 13, 14, 18 (the sea), 24 |
| S18 | **Night / moon** — cool blue top and back, a moon-and-cloud breakup | general | 4, 13, 17, 19, 21, 24 |
| S19 | **Dawn** — low warm-grey cross-light from SR | general | 4, 6, 10, 17, 21, 22 |
| S20 | **Sunset / long light** — low raking amber from SR, long shadows | general | 22 (pasture), 26 (finale) |
| S21 | **Leaf breakup** (dappled light) | DS centre / the bench | 18, 25 |
| S22 | **Steeple lanterns** (two practicals) + a tight pin | x +2.6, z 6.45, y 3.7 | 21 |
| S23 | **Lantern practicals** (hand lantern) | carried | 4, 13, 17 |
| S24 | **Lantern reveals** — three small specials that come up as the lantern reaches each piece | dressing table x +3.4, z 2.7; wig x +3.0, z 1.2; tipped chair x +0.9, z 3.0 | 17 |
| S25 | **Torches** (practicals) + orange flicker side-light | x −3.0, z 1.0 / −0.2, z 1.4 (17); −1.2, z 2.6 / +2.2, z 3.0 (24) | 17, 24 |
| S26 | **Candles** (candelabra, candlesticks: practicals) + a slow warm build | table and sideboard | 10, 11, 17, 20, 25 |
| S27 | **Shop doors** — a slice of light per door | x −3.6 / −1.2 / +1.2 / +3.6, z −1.2 | 8 |
| S28 | **The volley** — a flash behind Johnny, then **eight round eyes**: a tight cold downlight on him, low glints on passing muzzles | Johnny DS centre, x 0, z 0.5; flash upstage | 20 |
| S29 | **The runaway** — chase sequence of quick pools/side-light round the stage; snap to a still pool at the gate | the open floor; gate x +3.2, z 1.8 | 20 |
| S30 | **Fireflies / distant lights** — tiny twinkles low on the back wall over the wharf (musket flashes; warships; Charlestown) | back brick, y 0.5–1.5 | 21, 22 |
| S31 | **The boats from the house** — lantern light swinging in from the auditorium onto the apron's lip | apron lip | 24 |
| S32 | **The sheet** — backlight so the bellying sheet glows | the clothesline, z 1.6 | 15 |
| S33 | **Rab at the back** — a soft cool backlight up the centre path | x +0.2, z 5.0 | 26 |
| S34 | **House light bleed** — a touch of the house up when Johnny asks the house a real question and waits | the auditorium | 17, 26 |
| S35 | **Blackouts** — 6 (mid), 13 (end of Act One), 26 (end); snaps on the date calls in 21 | — | 6, 13, 21, 26 |

## Script against worklist: what does not match

1. **The furnace** glows in 3 and 6 in the worklist; the **script keeps it dark in 3** and lit in 6. The furnace is
   also the hearth for the Lapham kitchen (1, 2, 7), Milton's kitchen where the pages burn (**lit in 17**) and
   Silsbee's Cove (26).
2. **Not in the worklist at all:** a **sideboard** (10, 17 — the four cups stand on it), the **punch bowl** (13,
   19), plain **kitchen chairs** (nine scenes), the shop's **polishing wheel** (3, 6), the Observer's **type case**,
   **counter** and **drawing board**, a **gravestone**, a **mounting block**, a **hitching rail**, the **sofa** and
   **mirror** (16, 21, 22), Lavinia's **dressing table** and the **wig stand** (17), **torches** (17, 24), the **sea
   chest**, **hurdles**, **campfires**, the **rope line**, the **clothesline**, the **saddle stand**, a **pump**,
   **barrel**, **well** and **tanning shed** (24), the tiny **belfry** (25), the **King's colour**, a **fife**,
   the **Bibles**, the **bucket**, the **crucible and tongs**, the **parrot cage**, Hancock's **creamer**, Lyte's
   **great chair**, the Justice's **high-backed chair**, the **apple branches**, the **masking**. set.json has a slot
   for each (`worklistModel: null`).
3. **The loft is small for the Observers.** At the worklist's 3.6 × 1.8 the 'long table' meetings (13, 19) fit only
   as a narrow trestle with one bench behind it — about six in a line facing the house — and the overflow on the
   ladder. Widening it to ~4.4 × 2.2 seats a real table; it would push the ladder and narrow the centre path. Jack's
   call.
4. **Rab's musket** is, in the script, **Pumpkin's British musket** re-stocked by Rab (20, 25, 26) — a Brown Bess.
   The worklist gave Rab the Arizona replica "so it looks different from the British"; that civilian gun suits
   **Grandsire's old gun** (26) instead.
5. **The chaise** (worklist: 17, 25, 26): in the script Warren's chaise is **two chairs** in 17 and stands
   **offstage** in 26; nothing in 25. Only **Grandsire's old chaise crossing the finale** (26) needs one.
6. **The ruby coach** (worklist: 10, 17): the script never brings it on in 10, and in 17 suggests it by **its lamps
   and one wheel**.
7. **The armchair's owners:** the production note says Lapham, Hancock, Otis, Rab — but **no scene seats Hancock**
   (it is in the shop corner in 3 while he is there), and the script adds a fifth: **Grandsire's empty red armchair**
   at Silsbee's Cove (26). The script says it is **red**.
8. **Tents and stacked muskets** are in **14 and 20** (worklist: 14 / 20). **Truckle beds** are in **19, 20, 21, 22**
   (ripped) and one is the **jail cot** in 11 (worklist: 19, 21). **The cups** are also on the **courtroom table**
   (11). **Lanterns** also in **4, 13, 17**. **The drum** in 20 and 22.
9. **The Afric Queen's swing sign** is in the worklist but never in the script (kept, optional, on the stable door).
10. **Size limits the worklist assumed:** "masts 8–10 m, steeple 5–6 m, flies out of a 16 m tower" — only with a
    border: the plan uses **masts 8.0** and **steeple 5.0**; the front row would see anything taller hanging out.
11. **Dove's hatch** (13): this stage has no trap; he pops up from behind the tea chests. **Newman's drop from a shed
    roof** (21): from the wharf deck's edge (45 cm), not the loft (2.4 m).
12. **Colonial House is editorial-only** — it is the source for the door frame, the window flat, the shop doors, the
    warehouse corner and both swing signs. Previs only until its author agrees; all are simple to build from boxes.

## Piece × scene

● = on at some point in the scene (segments in set.json). Hand props included; costume (tricorns) and the previs-only
horse are not set pieces and are left out.

| piece | kind | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 |
|---|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| `wharf-deck` | unit | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● |
| `wharf-step` | unit | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● |
| `wharf-piles` | unit | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● |
| `loft` | unit | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● |
| `loft-rafters` | unit | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● |
| `ladder` | unit | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● |
| `furnace` | unit | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● |
| `bellows` | unit | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● |
| `lumber-pile-a` | unit | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● |
| `lumber-pile-b` | unit | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● |
| `crates` ×3 | unit | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● |
| `bench` | unit | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● |
| `masking-legs` ×6 | flown | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● |
| `masking-border` | flown | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● |
| `observer-sign` | flown |  |  |  |  |  |  |  |  | ● |  |  | ● |  |  |  |  |  |  |  | ● |  |  |  |  |  |  |
| `steeple` | flown |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | ● |  |  |  |  |  |
| `church-lanterns` ×2 | flown |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | ● |  |  |  |  |  |
| `ship-masts` | flown |  |  |  |  |  |  |  |  |  |  |  |  | ● | ● |  |  |  |  |  |  |  |  |  |  |  |  |
| `apple-branches` ×2 | flown |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | ● |  |  |  |  |  |  |  |  |
| `armchair` | travel | ● | ● | ● |  |  | ● | ● |  |  |  |  |  |  |  |  |  |  |  | ● |  |  |  |  |  | ● | ● |
| `kitchen-table` | travel | ● | ● |  |  |  |  | ● |  |  |  | ● |  |  |  |  | ● |  |  |  | ● |  |  | ● |  |  | ● |
| `kitchen-benches` ×2 | travel | ● | ● |  |  |  |  | ● |  |  |  | ● |  | ● |  |  |  |  |  | ● | ● |  |  |  |  |  |  |
| `kitchen-chairs` ×2 | travel |  |  |  |  |  |  | ● |  |  |  |  |  |  |  |  | ● | ● |  |  | ● | ● | ● | ● |  | ● | ● |
| `workbench` | travel |  |  | ● |  | ● | ● |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| `bench-tools` | hand |  |  | ● |  | ● | ● |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| `polishing-wheel` | travel |  |  | ● |  |  | ● |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| `water-bucket` | hand | ● |  |  |  |  | ● |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | ● |  |  |
| `crucible-and-tongs` | hand |  |  |  |  |  | ● |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| `hancock-creamer` | hand |  |  | ● |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| `parrot-cage` | hand | ● |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| `family-bible` | hand |  | ● |  |  |  |  |  |  |  |  |  |  |  |  |  |  | ● |  |  | ● |  |  |  |  |  |  |
| `three-boy-bed` | travel | ● | ● |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| `truckle-beds` ×2 | travel |  |  |  |  |  |  |  |  |  |  | ● |  |  |  |  |  |  |  | ● | ● | ● | ● |  |  |  |  |
| `feather-bed` | travel |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | ● |  |  |  |  |
| `trestle-table` | travel |  |  |  |  |  |  |  |  |  |  |  |  | ● |  |  |  |  |  | ● |  |  |  |  |  |  |  |
| `punch-bowl` | hand |  |  |  |  |  |  |  |  |  |  |  |  | ● |  |  |  |  |  | ● |  |  |  |  |  |  |  |
| `tankards` ×8 | hand |  |  |  |  |  |  |  |  |  |  |  |  | ● |  | ● |  |  |  | ● | ● |  |  |  |  |  |  |
| `lyte-table` | travel |  |  |  |  |  |  |  |  |  | ● |  |  |  |  |  |  | ● |  |  |  |  |  |  |  |  |  |
| `lyte-chairs` ×6 | travel |  |  |  |  |  |  |  |  |  | ● |  |  |  |  |  |  | ● |  |  |  |  |  |  |  |  |  |
| `sideboard` | travel |  |  |  |  |  |  |  |  |  | ● |  |  |  |  |  |  | ● |  |  |  |  |  |  |  |  |  |
| `candelabra` ×3 | hand |  |  |  |  |  |  |  |  |  | ● |  |  |  |  |  |  | ● |  |  |  |  |  |  |  |  |  |
| `candlesticks` ×3 | hand |  |  |  |  |  |  |  |  |  |  | ● |  |  |  |  |  |  |  |  | ● |  |  |  |  | ● |  |
| `lyte-cup` ×4 | hand |  |  |  | ● |  |  |  |  |  | ● | ● |  |  |  |  |  | ● |  |  |  |  |  |  |  |  |  |
| `clerk-desks` ×3 | travel |  |  |  |  |  |  |  |  |  | ● |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| `clerk-stools` ×3 | travel |  |  |  |  |  |  |  |  |  | ● |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| `low-stool` | travel |  |  |  |  |  |  |  |  |  |  | ● |  |  |  |  |  |  |  |  |  |  |  |  |  | ● |  |
| `lyte-great-chair` | travel |  |  |  |  |  |  |  |  |  | ● |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| `printing-press` | travel |  |  |  |  |  |  |  |  | ● |  |  | ● | ● |  |  |  |  |  | ● | ● | ● |  |  |  |  |  |
| `printing-press-smashed` | travel |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | ● |  |  |  |  |
| `type-case` | travel |  |  |  |  |  |  |  |  | ● |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| `counter` | travel |  |  |  |  |  |  |  |  | ● |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| `drawing-board` | travel |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | ● |  |  |  |  |  |  |
| `observer-sign-smashed` | hand |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | ● |  |  |  |  |
| `sea-chest` | travel |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | ● |  |  |  |  |  |  |
| `door-frame` | travel |  |  | ● |  |  | ● |  |  |  |  |  | ● |  |  | ● |  |  |  |  | ● | ● |  | ● |  | ● |  |
| `window-flat` | travel |  |  |  |  |  |  |  |  |  |  |  |  |  |  | ● |  |  |  |  |  | ● | ● |  |  | ● | ● |
| `shop-doors` ×4 | hand |  |  |  |  |  |  |  | ● |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| `gravestone` | travel |  |  |  |  |  |  |  |  |  | ● |  |  |  |  |  |  |  |  |  |  | ● |  |  |  |  |  |
| `mounting-block` | travel |  |  |  |  |  |  |  |  |  |  | ● |  |  | ● |  |  | ● |  |  |  |  |  |  |  | ● |  |
| `hitch-rail` | travel |  |  |  |  |  |  |  |  |  |  |  | ● |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| `judge-bench` | travel |  |  |  |  |  |  |  |  |  |  | ● |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| `judge-chair` | travel |  |  |  |  |  |  |  |  |  |  | ● |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| `bar-rail` | travel |  |  |  |  |  |  |  |  |  |  | ● |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| `ship-rail` | travel |  |  |  |  |  |  |  |  |  |  |  |  | ● |  |  |  |  |  |  |  |  |  |  |  |  |  |
| `tea-chests` ×12 | travel |  |  |  |  |  |  |  |  |  |  |  |  | ● |  |  |  |  |  |  |  |  |  |  |  |  |  |
| `plank-run` | travel |  |  |  | ● |  |  |  |  |  |  |  |  |  | ● |  |  |  |  |  |  |  |  |  | ● |  |  |
| `tents` ×3 | travel |  |  |  |  |  |  |  |  |  |  |  |  |  | ● |  |  |  |  |  | ● |  |  |  |  |  |  |
| `stacked-arms` | travel |  |  |  |  |  |  |  |  |  |  |  |  |  | ● |  |  |  |  |  | ● |  |  |  |  |  |  |
| `rope-line` | travel |  |  |  |  |  |  |  |  |  |  |  |  |  | ● |  |  |  |  |  |  |  |  |  |  |  |  |
| `redcoat-muskets` ×8 | hand |  |  |  |  |  |  |  |  |  |  |  |  |  | ● |  |  |  |  |  | ● |  | ● |  |  |  |  |
| `rab-musket` | hand |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | ● | ● |
| `grandsire-gun` | hand |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | ● |
| `powder-horn` | hand |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | ● |
| `drum` | hand |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | ● |  | ● |  |  |  |  |
| `fife` | hand |  |  |  |  |  |  |  |  |  |  |  |  | ● |  |  |  | ● |  |  |  |  | ● |  |  |  | ● |
| `flag` | hand |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | ● |  |  |  |  |
| `hurdles` ×2 | travel |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | ● |  |  |  |  |  |  |
| `campfires` ×2 | hand |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | ● |  |  |  |  |  |  |
| `clothesline` | travel |  |  |  |  |  |  |  |  |  |  |  |  |  |  | ● |  |  |  |  | ● |  |  |  | ● |  |  |
| `laundry-basket` | hand |  |  |  |  |  |  |  |  |  |  |  |  |  |  | ● |  |  |  |  | ● |  |  |  |  |  |  |
| `afric-queen-sign` | hand |  |  |  |  |  |  |  |  |  |  |  |  |  |  | ● |  |  |  |  | ● | ● |  |  |  |  |  |
| `saddle-stand` | travel |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | ● |  |  |  |  |  |
| `sofa` | travel |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | ● |  |  |  |  | ● | ● |  |  |  |  |
| `mirror` | travel |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | ● |  |  |  |  |  |  |  |  |  |  |
| `dressing-table` | travel |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | ● |  |  |  |  |  |  |  |  |  |
| `wig-stand` | hand |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | ● |  |  |  |  |  |  |  |  |  |
| `lantern` | hand |  |  |  | ● |  |  |  |  |  |  |  |  | ● |  |  |  | ● |  |  |  |  |  |  |  |  |  |
| `torches` ×2 | hand |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | ● |  |  |  |  |  |  | ● |  |  |
| `ruby-coach` | travel |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | ● |  |  |  |  |  |  |  |  |  |
| `chaise` | travel |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | ● |
| `warehouse-corner` | travel |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | ● |  |  |
| `tanning-shed` | travel |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | ● |  |  |
| `pump` | travel |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | ● |  |  |
| `flour-barrel` | travel |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | ● |  |  |
| `well` | travel |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | ● |  |  |
| `belfry` | travel |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | ● |  |
