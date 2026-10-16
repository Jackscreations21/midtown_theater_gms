# tools/jt-fit — Jack's downloaded models fitted to the Johnny Tremain set pieces

- `inventory.py` — lists what is inside every source file (objects, faces, size, images).
- `fit.py` — fits ONE source model to ONE piece from a recipe (`recipes/<piece id>.json`; the format is in its docstring):
  keep/drop parts, rotate, crop, decimate, scale to set.json's size, paint, textures to 1K JPEG, export
  `assets/johnny-tremain/models/<id>.glb` (+ an optional preview PNG).
- `manifest-*.json` — each batch's lines for `assets/johnny-tremain/models/manifest.json` (merged by hand).

The sources stay in Jack's `Downloads\jt-models\` (third-party files, never committed). Run:

    blender -b --factory-startup --python tools/jt-fit/fit.py -- tools/jt-fit/recipes/<id>.json "C:/Users/jackf/Downloads/jt-models" assets/johnny-tremain/models --preview=<a scratch dir>

The export puts a piece's front toward glTF +Z, so every manifest line carries `"rotY": 180`.

Pre-steps some recipes need (each recipe's `notes` gives its exact command):
- `prep_a.py` — builds `loft`, `loft-rafters`, `steeple` and `ship-masts` sources from the kit / the galleon into a scratch folder
  (fit.py's keep/drop/crop cannot assemble them); then fit.py runs with that folder as the src dir.
- `stack_arms.py` — leans three Brown Bess copies into the stand of arms (`stacked-arms`).
- `weld.py` — merges split vertices (keeping UVs) before decimating; `saddle.glb`, `side_chair.glb` and `mahogany_table.glb`
  shred into holes without it.

Ten pieces come from CGTrader downloads and are kept local (see `assets/johnny-tremain/models/README.md`).
