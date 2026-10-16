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

## Light Theatre 2 in midtown.html live from QLC+

The page's Theatre 2 rig follows QLC+ while QLC+ is sending: every fixture reads its own channels in its own QLC+ mode
(levels, colour mixing, the Encores' colour wheel and gobos, the movers' pan/tilt, the hazers' haze). A web page cannot
receive Art-Net itself, so a small relay passes it on. It needs only Python, which is already installed.

1. **Start the relay** in a terminal, from the repository folder, and leave it running:

       python tools/artnet-relay.py

   It listens for Art-Net on 127.0.0.1 (this computer only) and prints a status line every 3 seconds, e.g.
   `1 page(s) · U1 (Art-Net 0): 44 pkt/s, 1320 in · U2 (Art-Net 1): 44 pkt/s, 1320 in`. Start it **before** QLC+. If
   it says the port is in use, close QLC+, start the relay, then reopen QLC+.
2. **In QLC+, the Inputs/Outputs tab:** select **Universe 1**. In the **Art-Net** row whose device is **127.0.0.1**
   (the loopback line; QLC+ lists one Art-Net line per network card), tick **Output**. Then select **Universe 2** and tick
   Output on the same 127.0.0.1 line. Open that line's settings (the wrench icon) and check that Universe 1 sends
   **Art-Net universe 0** and Universe 2 sends **Art-Net universe 1**. Those are QLC+'s defaults. QLC+ counts its
   universes from 1 and Art-Net counts from 0. If the output IP can be set, set it to 127.0.0.1.
3. **Open the page from this computer:** `python -m http.server 8080` in the repository folder, then
   <http://localhost:8080/midtown.html>. The GitHub Pages copy may work too, but Chrome may ask permission to reach
   local devices.
4. **Press "T2 rig"** (top bar). The page starts listening when that panel first opens. Press **Theatre 2** to look at
   the stage. Then run the cue list in QLC+ (Virtual Console, Space = GO).

The last line of the T2 rig panel says what is happening:

| Status line | Meaning |
|---|---|
| `Desk: QLC+ live — U1 44 fps, U2 44 fps` | The desk has the rig. These are the packets per second QLC+ is sending. When a look is held still, QLC+ sends fewer, so the number can drop to 1 or 2. |
| `Desk: relay up, no Art-Net from QLC+` | The page reached the relay, but nothing has arrived from QLC+ in the last 5 s. Check step 2. If the relay's status line names "other universes seen", the Art-Net universe numbers are wrong. |
| `Desk: no relay — python tools/artnet-relay.py` | The relay is not running. The page checks again every 5 s while the panel is open, and every 30 s while it is closed. |

While QLC+ drives the rig, the page's own scene and look menus are held: whatever you choose is noted and comes back when
QLC+ stops. About 2 s after the relay reports QLC+ silent (5 s without a packet), the rig fades back to that look.

Not drawn: strobe, zoom, focus, iris, frost, the framing blades and the FX channels. The Generic dimmers, the practicals
and the followspots have only a level, so they show the colour the page's own looks give them. To test without QLC+, run
`python tools/artnet-test.py chase`, `full`, `blackout`, or `look <tag>` while the relay is running. `look <tag>`
sends a look exactly as the workspace's scene encodes it.

**Not yet proven with QLC+ itself.** The relay and the page were tested with `tools/artnet-test.py`, which sends real
ArtDmx packets to 127.0.0.1:6454. QLC+ was not installed for that test. One risk: QLC+'s Art-Net plugin also opens UDP
port 6454 on this computer. If QLC+ is sending but the status line still says "no Art-Net from QLC+", that is the likely
cause. Say so, and the relay can be changed to receive on the network card's address instead.

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
