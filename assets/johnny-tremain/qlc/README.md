# Johnny Tremain — the QLC+ workspace

`johnny-tremain.qxw` is a QLC+ 4 workspace with the whole Theatre 2 rig for *Johnny Tremain* in it: every fixture
patched, grouped, and the show's looks and cue list ready to run. It is written by `tools/jt-qlc.py` from
`assets/johnny-tremain/rig.json` (which `tools/jt-rig.py` writes); the plot, patch sheet and hookup are
[`docs/johnny-tremain/LIGHT-PLOT.md`](../../../docs/johnny-tremain/LIGHT-PLOT.md).

## Open it

1. Install **QLC+ 4** (4.12 or newer; it was written against the 4.14 file format) from <https://www.qlcplus.org>.
2. **File → Open** (or the folder icon top left), pick `johnny-tremain.qxw`. It opens on the Virtual Console with the
   **Johnny Tremain** cue list.

**No custom fixture files are needed.** Every fixture is one QLC+ ships with (ETC Source Four LED Series 2 Lustr,
ETC ColorSource Spot and PAR, Martin MAC Encore Performance and MAC Aura, Chauvet Ovation CYC 1 FC, Robert Juliat
D'Artagnan 934SNX, MDG ATMe) or a Generic dimmer (the two tungsten Source Fours and the 14 practicals) — the generator
checked every manufacturer, model, mode and channel list against QLC+'s own library files. If an old QLC+ says a
fixture is missing, update QLC+ (the folder for your own fixture files, if ever needed, is
`C:\Users\<you>\QLC+\Fixtures` on Windows — QLC+'s Fixture Editor saves there).

## Send it to the lights

**Inputs/Outputs** tab: the workspace uses **two universes** (Universe 1: 479 channels — the front of house, the
electrics' fixed units, the floor, the doorway, the followspots; Universe 2: 489 — the booms, the movers, the sky, the
haze, the practicals). Tick an output for each:

- **Art-Net / sACN** (a node or a console on the network): pick the plugin and the network card for Universe 1, then
  Universe 2 (Art-Net universe 0 and 1 by default — set the node to match).
- **A USB DMX dongle** (ENTTEC DMX USB Pro / Open DMX, DMXking…): one dongle is one universe — tick it for Universe 1;
  Universe 2 needs a second dongle or an Art-Net node.

Nothing is patched to an output in the file, so opening it never sends anything until you choose.

## What is in it

- **128 fixtures**, named by unit and purpose (`BR-13 Cup pin, the wharf's lip (S4)`), at the addresses on the
  patch sheet (QLC+ shows them 1-based; the file stores them 0-based, as QLC+ does).
- **41 fixture groups**: one per hanging position (the bridge, FOH 2, the box booms, the four electrics, each boom, the
  ground row…) and one per system (front light, top, back, side from SL / SR, specials, the movers, the sky, haze,
  practicals) — select a group in the Simple Desk or a Scene editor to set a whole system at once.
- **Functions** (Function Manager):
  - `Looks/` — 48 Scenes, `Look: <tag>`, one for each lighting tag the scenes use (`interior-dawn-warm`,
    `night-exterior-moon`, `exterior-sunset-long`…).
  - `Segments/` — 33 Scenes for the segments that add to their look (the furnace lit, the candles, the church
    lanterns, the cup pins, the doorway…).
  - **Johnny Tremain** — a Chaser with **66 steps, one per scene segment in show order** (step notes say which:
    `21.5 New Evolutions: North Square; Copp's Hill…`). Every step fades in over 2 s and holds until the next GO.
- **Virtual Console**: a **Cue List** on that chaser. **Space** (or the ▶ / next button) is GO; click a row to jump.

## Before the first night

- The movers' pan/tilt in the scenes are computed for each mover hung **with its front to the house**; check the focus
  with the Position tool and re-record. The Encore's gobo slots (water 1, leaves 2, moon 3, window 4) stand in for the
  gobos actually loaded.
- The specials that are cues *inside* a look (the pour snapping up in 6, the volley flash and the eyes in 20, Otis's
  hands in 19, the shop-door slices in 8) are at 0 in their look — build them as their own cues in the cue list where the
  script calls them.
- Regenerate after changing the rig: `python tools/jt-rig.py` then `python tools/jt-qlc.py`.
