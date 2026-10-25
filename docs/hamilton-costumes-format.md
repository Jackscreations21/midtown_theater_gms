# `assets/hamilton-costumes.json` — the Hamilton costumes

`midtown.html`'s automatic actors wear these looks (the section "AUTOMATIC ACTORS: THE COSTUMES"). The file has two parts:
`costumes`, the looks, and `plot`, which body wears which look from when. Edit the file and reload, or hand it to
`MIDTOWN.costumes.load(obj)` from the console. `MIDTOWN.costumes.check()` tests it.

## The top level

| key | what |
|---|---|
| `what`, `design`, `sourcing`, `sources`, `women` | notes for people; the page ignores them |
| `defaults` | fields every look gets unless it gives its own (`skin`, `hair`) |
| `costumes` | `{ "<look id>": look }` |
| `plot` | `{ "<body id>": [entry, …] }` — body ids from `tools/hamilton-cast.json` |

## A plot entry

```json
{ "from": "1-08", "costume": "ham-officer", "onstage": true }
```

- `from` — an album track id (`assets/hamilton-show.json`). The look is worn from that track's start, plus `at` seconds if given.
- `costume` — a look id in `costumes`.
- `onstage` (optional) — the change is made in view at that moment, on purpose.

**When the change really happens.** A body changes off stage. The page uses the moment it last went off since the song
before `from` began, provided it came back no more than 15 s before `from` (`COS_TUNE.back`). Failing that, it changes at its
first exit inside the `from` track (the old look a little longer). Failing that, or with `onstage`, it changes at `from`'s
start, in view. `check().inView` lists every change made in view. Before a body's first entry it wears the first look.

## A look

Every field is optional; a missing one takes the file's `defaults`, then the page's own (`COS_DEF`). Colours are `#rrggbb`.

| field | what |
|---|---|
| `label`, `source` | for people. `source`: S = written down, I = read off the film or inferred |
| `coat` | a coat over the body and arms (its colour). With no coat, the arms are the shirt (or the bodice, or skin: `sleeves`) |
| `facing` | the coat's lapels, collar, cuffs and the edges of its skirts |
| `cuffs` | the coat's cuffs, if not `facing` |
| `tails` | the coat's skirts: `long` (to the knee; default), `short`, `none` (a spencer or a jacket) |
| `vest` | the waistcoat (its front under a coat; the whole torso with no coat) |
| `shirt` | the shirt (sleeves without a coat, the neckline) |
| `stock` | the neckcloth |
| `sash` | a sash across the chest (over a coat) |
| `trim` | gold: epaulettes, a coat's hem band, the crown |
| `breeches` | breeches (or leggings) |
| `legs` | `boots` (knee boots; default) or `stockings` (stockings and shoes) |
| `boots`, `cuff` | the boots' colour; a turned-down top band |
| `stockings`, `shoes` | for `legs: stockings`, and under a gown |
| `bodice` | a bodice or corset over the torso (with no coat) |
| `neck` | a bodice's neckline: `low` (skin; default) or `high` (the `shirt` colour) |
| `sleeves` | with no coat: `shirt` (default), `bodice`, `skin`, `elbow` (to the elbow, then skin) |
| `stomacher` | a panel down the bodice's front |
| `skirt` | a gown: a skirt from the waist to the floor (her arms stand a little out from her sides in it) |
| `petticoat` | the gown's front panel, where an over-gown opens |
| `hemband` | a band round the gown's hem |
| `cape`, `capeHem` | a cape from the shoulders behind; its hem's height over the floor (default to the floor; 1.0 is a shoulder cape) |
| `ermine` | `true`: the cape's collar in ermine |
| `skin`, `hair` | colours |
| `hairdo` | `queue` (default), `bun`, `loose`, `none` |
| `wig` | a wig's colour (King George's), with curls over the ears and a queue |
| `hat` | the cap's colour |
| `extras` | any of `epaulettes`, `crown`, `cap` |

## The bodies

The mannequin is the same body for everyone. Ensemble women are `ens1`, `ens6`–`ens9`; men are `ens2`–`ens5` and `ens10`. That is a
choice made here, not a ruling. The doubled tracks (Lafayette/Jefferson, Mulligan/Madison, Laurens/Philip, Peggy/Maria
Reynolds, the ensemble's named parts) are just more entries in the same body's plot.
