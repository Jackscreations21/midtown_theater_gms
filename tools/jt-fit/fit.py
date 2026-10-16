"""Blender headless: fit one of Jack's downloaded models to a Johnny Tremain set piece.

    blender -b --factory-startup --python tools/jt-fit/fit.py -- <recipe.json> <models src dir> <out dir> [--preview[=<png dir>]]

The recipe (tools/jt-fit/recipes/<piece id>.json) says what to take from the source and how:

    {
      "id": "ladder",                       # the set.json piece id; the GLB is written as <out dir>/<id>.glb
      "src": "ladder.glb",                  # a file in the src dir; for a .zip, "src": "x.zip", "inner": "3d-model.fbx"
      "keep": ["regex", ...],               # optional: keep only mesh objects whose name matches one of these
      "drop": ["regex", ...],               # optional: delete mesh objects whose name matches (after keep)
      "rot": [0, 0, 0],                     # optional: degrees about Blender X, Y, Z, applied first (Blender is Z up;
                                            #   the piece's FRONT must end facing Blender -Y, its top +Z)
      "crop": [[0,0,0],[1,1,1]],            # optional: keep only what lies in this box, as fractions of the (rotated)
                                            #   model's bounds in X, Y, Z (cuts faces at the planes; no cap)
      "size": [w, h, d],                    # metres: the piece's set.json size (w along X, h along Z, d along Y)
      "fit": "auto" | "w" | "h" | "d" | "stretch",   # uniform scale to the largest (auto) or one size; stretch = all three
      "faces": 20000,                       # optional: decimate (collapse) the whole model to about this many faces
      "tex": 1024,                          # optional: largest texture side (default 1024)
      "jpeg": true,                         # optional: textures as JPEG (default true; false keeps PNG, e.g. alpha)
      "paint": {"color": [r,g,b], "roughness": 0.7, "metallic": 0.0},   # optional: override every material's base
      "notes": "what was cut and why"
    }

Writes <id>.glb (Y up, metres, origin at the base centre, front toward glTF +Z — the manifest's rotY 180 turns it to
the house) and, with --preview, <id>.png (a front three-quarter Workbench render) for checking by eye. Prints one
FIT line: faces before/after, the fitted size, the file size."""
import bpy, bmesh, sys, os, json, re, math, zipfile, tempfile, glob, mathutils

argv = sys.argv[sys.argv.index('--') + 1:]
recipe_path, src_dir, out_dir = argv[0], argv[1], argv[2]
pv = [a for a in argv if a.startswith('--preview')]
preview = bool(pv); preview_dir = pv[0].split('=', 1)[1] if pv and '=' in pv[0] else out_dir
R = json.load(open(recipe_path, encoding='utf-8'))
os.makedirs(out_dir, exist_ok=True)

bpy.ops.wm.read_factory_settings(use_empty=True)

# ---- load
path = os.path.join(src_dir, R['src'])
if path.lower().endswith('.zip'):
    d = tempfile.mkdtemp(prefix='jtfit'); zipfile.ZipFile(path).extractall(d)
    hits = [p for p in glob.glob(os.path.join(d, '**', '*'), recursive=True) if os.path.basename(p) == R['inner']]
    path = hits[0]
ext = os.path.splitext(path)[1].lower()
if ext in ('.glb', '.gltf'): bpy.ops.import_scene.gltf(filepath=path)
elif ext == '.fbx': bpy.ops.import_scene.fbx(filepath=path)
elif ext == '.obj': bpy.ops.wm.obj_import(filepath=path)
elif ext == '.blend':
    with bpy.data.libraries.load(path, link=False) as (a, b): b.objects = a.objects
    for o in b.objects:
        if o is not None: bpy.context.scene.collection.objects.link(o)
else: raise SystemExit('unknown source type ' + ext)

# ---- choose the parts
sc = bpy.context.scene
meshes = [o for o in sc.objects if o.type == 'MESH']
if R.get('keep'): meshes = [o for o in meshes if any(re.search(k, o.name) for k in R['keep'])]
if R.get('drop'): meshes = [o for o in meshes if not any(re.search(k, o.name) for k in R['drop'])]
if not meshes: raise SystemExit('nothing left after keep/drop')
faces0 = sum(len(o.data.polygons) for o in meshes)

# bake every kept mesh's world transform into its data, unparent, delete everything else
for o in meshes:
    mw = o.matrix_world.copy(); o.parent = None; o.matrix_world = mw
for o in list(sc.objects):
    if o not in meshes: bpy.data.objects.remove(o, do_unlink=True)
for o in meshes:
    if o.data.users > 1: o.data = o.data.copy()
    o.data.transform(o.matrix_world); o.matrix_world = mathutils.Matrix.Identity(4)

# join into one object
bpy.ops.object.select_all(action='DESELECT')
for o in meshes: o.select_set(True)
bpy.context.view_layer.objects.active = meshes[0]
if len(meshes) > 1: bpy.ops.object.join()
ob = bpy.context.view_layer.objects.active
ob.name = R['id']
me = ob.data

def bounds():
    vs = [v.co for v in me.vertices]
    lo = mathutils.Vector((min(v[i] for v in vs) for i in range(3))); hi = mathutils.Vector((max(v[i] for v in vs) for i in range(3)))
    return lo, hi

# ---- rotate
if R.get('rot'):
    rx, ry, rz = [math.radians(a) for a in R['rot']]
    me.transform(mathutils.Euler((rx, ry, rz), 'XYZ').to_matrix().to_4x4())

# ---- crop (fractions of the rotated bounds)
if R.get('crop'):
    lo, hi = bounds(); a, b = R['crop']
    bm = bmesh.new(); bm.from_mesh(me)
    for i in range(3):
        for frac, keep_pos in ((a[i], True), (b[i], False)):
            if (keep_pos and frac <= 0) or (not keep_pos and frac >= 1): continue
            co = mathutils.Vector((0, 0, 0)); co[i] = lo[i] + (hi[i] - lo[i]) * frac
            no = mathutils.Vector((0, 0, 0)); no[i] = 1
            geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
            bmesh.ops.bisect_plane(bm, geom=geom, plane_co=co, plane_no=no, clear_inner=keep_pos, clear_outer=not keep_pos)
    bm.to_mesh(me); bm.free()
    if not len(me.polygons): raise SystemExit('crop left nothing')

# ---- decimate
if R.get('faces') and len(me.polygons) > R['faces']:
    m = ob.modifiers.new('dec', 'DECIMATE'); m.ratio = max(0.001, R['faces'] / len(me.polygons))
    bpy.ops.object.modifier_apply(modifier=m.name)

# ---- scale to the piece's size: w along X, d along Y, h along Z
lo, hi = bounds(); got = hi - lo
w, h, d = R['size']; want = mathutils.Vector((w, d, h))
fit = R.get('fit', 'auto')
if fit == 'stretch':
    s = mathutils.Vector((want[i] / max(got[i], 1e-9) for i in range(3)))
else:
    ax = {'w': 0, 'd': 1, 'h': 2}.get(fit, max(range(3), key=lambda i: want[i]))
    k = want[ax] / max(got[ax], 1e-9); s = mathutils.Vector((k, k, k))
me.transform(mathutils.Matrix.Diagonal((s[0], s[1], s[2], 1)))
lo, hi = bounds(); c = (lo + hi) / 2
me.transform(mathutils.Matrix.Translation((-c.x, -c.y, -lo.z)))          # base centre at the origin
me.update()

# ---- materials: paint, textures down to tex px
tex = R.get('tex', 1024)
for mat in me.materials:
    if not mat or not mat.use_nodes: continue
    bsdf = next((n for n in mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
    if R.get('paint') and bsdf:
        p = R['paint']
        if 'color' in p:
            for l in list(bsdf.inputs['Base Color'].links): mat.node_tree.links.remove(l)
            bsdf.inputs['Base Color'].default_value = (*p['color'], 1)
        if 'roughness' in p:
            for l in list(bsdf.inputs['Roughness'].links): mat.node_tree.links.remove(l)
            bsdf.inputs['Roughness'].default_value = p['roughness']
        if 'metallic' in p:
            for l in list(bsdf.inputs['Metallic'].links): mat.node_tree.links.remove(l)
            bsdf.inputs['Metallic'].default_value = p['metallic']
for img in bpy.data.images:
    if img.size[0] and max(img.size) > tex:
        k = tex / max(img.size); img.scale(max(1, int(img.size[0] * k)), max(1, int(img.size[1] * k)))

# ---- export
out = os.path.join(out_dir, R['id'] + '.glb')
bpy.ops.object.select_all(action='DESELECT'); ob.select_set(True)
kw = dict(filepath=out, export_format='GLB', use_selection=True, export_apply=True, export_yup=True)
try: bpy.ops.export_scene.gltf(**kw, export_image_format='JPEG' if R.get('jpeg', True) else 'AUTO')
except TypeError: bpy.ops.export_scene.gltf(**kw)

lo, hi = bounds(); sz = hi - lo
print(f"FIT {R['id']}: {faces0} -> {len(me.polygons)} faces; w {sz.x:.3f} h {sz.z:.3f} d {sz.y:.3f} m (want {w} x {h} x {d}); "
      f"{os.path.getsize(out) / 1e6:.2f} MB -> {out}", flush=True)

# ---- preview: a Workbench render from the front three-quarter (the front faces -Y), textures shown
if preview:
    cam = bpy.data.objects.new('cam', bpy.data.cameras.new('cam')); sc.collection.objects.link(cam); sc.camera = cam
    r = max(sz.x, sz.y, sz.z) * 1.9 + 0.2; mid = mathutils.Vector((0, 0, sz.z / 2))
    cam.location = mid + mathutils.Vector((r * 0.55, -r * 0.85, r * 0.35))
    cam.rotation_euler = (mid - cam.location).to_track_quat('-Z', 'Y').to_euler()
    sc.render.engine = 'BLENDER_WORKBENCH'; sc.display.shading.color_type = 'TEXTURE'; sc.display.shading.light = 'STUDIO'
    sc.render.resolution_x = sc.render.resolution_y = 512; os.makedirs(preview_dir, exist_ok=True); sc.render.filepath = os.path.join(preview_dir, R['id'] + '.png')
    sc.world = sc.world or bpy.data.worlds.new('w')
    bpy.ops.render.render(write_still=True)
