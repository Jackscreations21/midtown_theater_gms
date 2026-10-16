# Johnny Tremain in Theatre 2 — the contract between the three builders (2026-10-16)

Three agents build in parallel, each in its own worktree and its own NEW banner section of `midtown.html`. The lead
merges them on `johnny-tremain`. This file is the only thing they share; if you must deviate, say so in your report.

## Jack's words (rulings)

- **GI** (2026-10-16): *"make it so there is a stage lift that is used to bring on and off big sets like the ship.
  make a front and back one. the front one is used to bring sets on and the back one to take sets off"* — and
  *"only add the stage lifts to the second stage"*. Theatre 2 only; house 1 is untouched.
- **GJ** (2026-10-16): *"also make an entire underground area for storage and stuff"* — under Theatre 2.

## Frame

Stage-relative (as `assets/johnny-tremain/set.json`): +x = stage RIGHT (world +x), z = metres upstage of the
proscenium plane, y = metres above the deck. **world = (20.00 + x, 0.80 + y, 2.30 + z).** Upstage is +z.

## The lifts (fixed numbers — do not move them without saying so)

| lift | stage x | stage z | world x | world z | size |
|---|---|---|---|---|---|
| front (brings sets ON) | −3.00 … +3.00 | 0.30 … 2.70 | 17.00 … 23.00 | 2.60 … 5.00 | 6.0 × 2.4 m |
| back (takes sets OFF) | −2.50 … +2.50 | 3.60 … 6.00 | 17.50 … 22.50 | 5.90 … 8.30 | 5.0 × 2.4 m |

- Top stop: flush with the deck, platform top at world y **0.80**. Bottom stop: the basement floor, world y
  **−4.40** (5.20 m of travel, so a 4.4 m set rides down whole). Speed about 0.4 m/s with eased ends (~14 s a run).
- **The underground agent owns** the lifts' mechanism and drawing: the hole in Theatre 2's deck, the pits, the
  platforms, guides, motion, warning lights/rails, and walker safety (an open shaft must stop the walker; a lift
  must not move a walker standing on it into a wall — refuse, or carry them, their call, reported).
- API it exposes (the sets agent codes against this and must tolerate it being absent — pieces then just appear):

```js
MIDTOWN.under.lifts.front / .back = {
  platform,          // THREE.Object3D; its local origin = the platform's TOP CENTRE; children ride with it
  footprint,         // { x:[x0,x1], z:[z0,z1] } world
  top: 0.80, bottom: -4.40,
  state,             // 'up' | 'down' | 'moving'
  go(to),            // 'up' | 'down'; returns a Promise that resolves on arrival (driven by frame dt, no setTimeout)
};
MIDTOWN.under.bays   // [{ name, x, z, w, d, y }] world floor spots in the basement where a big set can park
MIDTOWN.under.tick(dt)   // called from the frame loop
```

## The underground (GJ)

Under Theatre 2's stage house (world x ≈ 10.5…29.9, z ≈ −0.35…9.0, may run under the backstage block z 9.1…17.2),
floor y −4.40. The underground agent owns it all: the shell, the lift pits, a scenery dock where big sets park,
a track or path from the back lift's pit round to the front lift's pit (sets go down at the back and come back up
at the front — the loop), prop/furniture storage, a trap room under the deck, stairs (and a lit route) down from the
stage-left wing and from the backstage block, walkable with E-doors like the rest, its own worklights.

## Who owns what in `midtown.html`

| agent | its section banner | its global |
|---|---|---|
| underground | `THEATRE 2: THE UNDERGROUND AND THE LIFTS` | `MIDTOWN.under` |
| sets | `THEATRE 2: JOHNNY TREMAIN — THE SET` | `MIDTOWN.jt` |
| lights | `THEATRE 2: JOHNNY TREMAIN — THE LIGHTS` | `MIDTOWN.jtLights` |

Put new sections just BEFORE the `BUILD MODE` banner, in the order above. Outside your section touch as few lines as
possible (an init call, the frame-loop tick, a line in the `MIDTOWN` export, the walk's collision/floor hook) and
LIST every such line in your report — the lead merges them by hand.

- The sets agent calls `MIDTOWN.jtLights && MIDTOWN.jtLights.look(sceneN, segmentIndex)` whenever the scene changes
  (it owns the scene picker UI: a "Johnny Tremain" panel or header button; the lights agent adds no picker of its own,
  only its own panel controls if any).
- Set pieces use lit materials (MeshStandardMaterial). The lights agent makes Theatre 2's stage surfaces take light.
- Never `setTimeout` for game timing; time comes off the frame `dt`.
