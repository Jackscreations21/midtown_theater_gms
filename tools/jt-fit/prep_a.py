"""Blender headless: build the intermediate sources that fit.py cannot make by keep/drop/crop alone (batch A).

    blender -b --factory-startup --python tools/jt-fit/prep_a.py -- <models src dir> <scratch out dir> <job>

Jobs (each writes <scratch out dir>/<job>-src.glb; fit it with fit.py and recipes/<job>.json, passing the scratch
dir as the src dir — the intermediate is never committed, the downloads stay in Downloads):

  loft          the loft from the Free Wooden Scaffolding Set kit: two of its braced towers stretched to a
                2.0 x 3.6 deck at 2.40 (posts ~0.2), a 1.10 rail on top - the kit's X-braced rail along both
                sides and the back, its two-bar rail along the front with a 0.60 gap at the middle for the ladder.
  loft-rafters  an open A-frame from the same kit's plain square post: four corner posts 1.20 high, an eave
                beam along each side, a ridge along the depth at 2.0, four pairs of rafters, a tie at each gable.
  steeple       steeple.glb flattened to a cut-out (depth squashed to 0.042: ~0.1 m once fitted), front view unchanged.
  ship-masts    GalleonOGA.blend given a material (it has none, so paint has nothing to colour) and flattened
                front-to-back to a silhouette, turned broadside first (the masts in a row, bow to stage right)."""
import bpy, sys, os, math, mathutils

argv = sys.argv[sys.argv.index('--') + 1:]
src_dir, out_dir, job = argv[0], argv[1], argv[2]
os.makedirs(out_dir, exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene


def load(name):
    p = os.path.join(src_dir, name)
    if p.lower().endswith('.glb'): bpy.ops.import_scene.gltf(filepath=p)
    else:
        with bpy.data.libraries.load(p, link=False) as (a, b): b.objects = a.objects
        for o in b.objects:
            if o is not None: sc.collection.objects.link(o)
    bpy.context.view_layer.update()
    meshes = [o for o in sc.objects if o.type == 'MESH']
    for o in meshes:                                   # bake world transforms, drop empties
        mw = o.matrix_world.copy(); o.parent = None; o.matrix_world = mw
    for o in list(sc.objects):
        if o not in meshes: bpy.data.objects.remove(o, do_unlink=True)
    for o in meshes:
        if o.data.users > 1: o.data = o.data.copy()
        o.data.transform(o.matrix_world); o.matrix_world = mathutils.Matrix.Identity(4)
    return {o.name: o for o in meshes}


def bbox(me):
    vs = [v.co for v in me.vertices]
    lo = mathutils.Vector([min(v[i] for v in vs) for i in range(3)]); hi = mathutils.Vector([max(v[i] for v in vs) for i in range(3)])
    return lo, hi


def place(part, size, rot, centre):
    """A copy of `part`, its bounding box scaled to `size` (x, y, z, in its own axes), then turned by `rot`
    (degrees XYZ) and centred at `centre`."""
    me = part.data.copy(); lo, hi = bbox(me); c = (lo + hi) / 2; s = hi - lo
    me.transform(mathutils.Matrix.Translation(-c))
    me.transform(mathutils.Matrix.Diagonal((size[0] / s.x, size[1] / s.y, size[2] / s.z, 1)))
    me.transform(mathutils.Euler([math.radians(a) for a in rot], 'XYZ').to_matrix().to_4x4())
    me.transform(mathutils.Matrix.Translation(centre))
    o = bpy.data.objects.new(part.name + '_p', me); sc.collection.objects.link(o)
    return o


def finish(keep):
    for o in list(sc.objects):
        if o not in keep: bpy.data.objects.remove(o, do_unlink=True)
    out = os.path.join(out_dir, job + '-src.glb')
    bpy.ops.object.select_all(action='DESELECT')
    for o in keep: o.select_set(True)
    bpy.ops.export_scene.gltf(filepath=out, export_format='GLB', use_selection=True, export_yup=True)
    print('PREP', job, '->', out, sum(len(o.data.polygons) for o in keep), 'faces', flush=True)


def flatten(objs, k, colour=None):
    """Squash the model front-to-back (Blender Y) by k about its centre; give it a material if it has none."""
    for o in objs:
        lo, hi = bbox(o.data); cy = (lo.y + hi.y) / 2
        o.data.transform(mathutils.Matrix.Translation((0, cy, 0)) @ mathutils.Matrix.Diagonal((1, k, 1, 1)) @
                         mathutils.Matrix.Translation((0, -cy, 0)))
        if colour and not [m for m in o.data.materials if m]:
            m = bpy.data.materials.new('wood'); m.use_nodes = True
            b = next(n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
            b.inputs['Base Color'].default_value = (*colour, 1); b.inputs['Roughness'].default_value = 0.85
            o.data.materials.append(m)


if job in ('loft', 'loft-rafters'):
    kit = load('scaffolding.glb')
    tower, xrail, rail, post = kit['defaultMaterial.002'], kit['defaultMaterial.004'], kit['defaultMaterial.008'], kit['defaultMaterial.009']
    keep = []
    if job == 'loft':
        W, D, H, R, T = 2.0, 3.6, 2.4, 1.1, 0.18          # deck width, depth, top; rail height; rail thickness
        for y0 in (-D / 2, 0):                              # two towers end to end make the 3.6 deck
            keep.append(place(tower, (W, D / 2, H), (0, 0, 0), (0, y0 + D / 4, H / 2)))
        zr = H + R / 2; xi = W / 2 - T / 2
        for sx in (-1, 1):                                  # the X-braced rail along each side (the kit rail runs along Y)
            for y0 in (-D / 2, 0):
                keep.append(place(xrail, (T, D / 2, R), (0, 0, 0), (sx * xi, y0 + D / 4, zr)))
        keep.append(place(xrail, (T, W, R), (0, 0, 90), (0, D / 2 - T / 2, zr)))           # the back
        gap = 0.6; L = (W - gap) / 2                        # the front: two-bar rail, a gap at the middle for the ladder
        for sx in (-1, 1):
            keep.append(place(rail, (T, L, R), (0, 0, 90), (sx * (gap / 2 + L / 2), -D / 2 + T / 2, zr)))
    else:
        W, D, E, RZ, t = 2.0, 3.6, 1.2, 2.0, 0.14          # width, depth, eave height, ridge height, timber
        xe = W / 2 - t / 2; ye = D / 2 - t / 2
        for sx in (-1, 1):
            for sy in (-1, 1):
                keep.append(place(post, (t, t, E), (0, 0, 0), (sx * xe, sy * ye, E / 2)))     # corner posts
            keep.append(place(post, (t, t, D), (90, 0, 0), (sx * xe, 0, E + t / 2)))        # eave beams along the depth
        keep.append(place(post, (t, t, D), (90, 0, 0), (0, 0, RZ - t / 2)))                # ridge
        dx, dz = xe, (RZ - t / 2) - (E + t / 2); L = math.hypot(dx, dz); a = math.degrees(math.atan2(dx, dz))
        for y in (-ye, -ye / 3, ye / 3, ye):                # four trusses: a pair of rafters each
            for sx in (-1, 1):
                keep.append(place(post, (t, t, L + t), (0, -sx * a, 0), (sx * xe / 2, y, E + t / 2 + dz / 2)))
        for sy in (-1, 1):                                  # a tie across each gable at the eaves
            keep.append(place(post, (t, t, W), (0, 90, 0), (0, sy * ye, E + t / 2)))
    finish(keep)
elif job == 'steeple':
    objs = list(load('steeple.glb').values())
    flatten(objs, 0.042)
    finish(objs)
elif job == 'ship-masts':
    objs = list(load('GalleonOGA.blend').values())
    for o in objs: o.data.transform(mathutils.Matrix.Rotation(math.radians(90), 4, 'Z'))   # broadside to the house
    flatten(objs, 0.01, colour=(0.16, 0.10, 0.06))
    finish(objs)
else:
    raise SystemExit('unknown job ' + job)
