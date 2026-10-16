"""Blender headless: compose the stand of stacked muskets (stacked-arms) from three Brown Bess copies.

    blender -b --factory-startup --python tools/jt-fit/stack_arms.py -- <models src dir> <out .glb> [tilt deg]

Loads brown_bess.glb (bayonet kept), stands it muzzle up, and leans three copies into a tripod: butts on a circle at
120 deg, each tilted inward so their barrel axes meet at the muzzle and the bayonets cross above it. Writes an
intermediate GLB (keep it in a scratch dir, not the repo); fit it to the piece with fit.py and
recipes/stacked-arms.json, passing that scratch dir as the src dir."""
import bpy, sys, os, math, mathutils

argv = sys.argv[sys.argv.index('--') + 1:]
src_dir, out = argv[0], argv[1]
tilt = math.radians(float(argv[2]) if len(argv) > 2 else 15.0)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=os.path.join(src_dir, 'brown_bess.glb'))
sc = bpy.context.scene
meshes = [o for o in sc.objects if o.type == 'MESH']
for o in meshes:
    mw = o.matrix_world.copy(); o.parent = None; o.matrix_world = mw
for o in list(sc.objects):
    if o not in meshes: bpy.data.objects.remove(o, do_unlink=True)
for o in meshes:
    if o.data.users > 1: o.data = o.data.copy()
    o.data.transform(o.matrix_world); o.matrix_world = mathutils.Matrix.Identity(4)
bpy.ops.object.select_all(action='DESELECT')
for o in meshes: o.select_set(True)
bpy.context.view_layer.objects.active = meshes[0]
bpy.ops.object.join()
gun = bpy.context.view_layer.objects.active
me = gun.data

# muzzle up: the source lies along X with the bayonet toward -X; Ry(+90) takes -X to +Z
me.transform(mathutils.Matrix.Rotation(math.radians(90), 4, 'Y'))
vs = [v.co for v in me.vertices]
lo = [min(v[i] for v in vs) for i in range(3)]; hi = [max(v[i] for v in vs) for i in range(3)]
# the barrel axis: the barrel cap (the muzzle) sits on it; take the centre of the top 25% below the bayonet as the axis
L = hi[2] - lo[2]
muzzle_h = L * 0.7645                                         # the muzzle (barrel cap) as a fraction of the length, bayonet above
band = [v for v in vs if muzzle_h - L * 0.2 < v.z - lo[2] < muzzle_h]
ax = sum((v.x for v in band)) / len(band); ay = sum((v.y for v in band)) / len(band)
me.transform(mathutils.Matrix.Translation((-ax, -ay, -lo[2])))   # barrel axis through the origin, butt on z=0

r = muzzle_h * math.sin(tilt)                                 # butt radius so the axes meet at the muzzle
copies = [gun]
for k in (1, 2):
    c = gun.copy(); c.data = gun.data.copy(); sc.collection.objects.link(c); copies.append(c)
for k, o in enumerate(copies):
    a = math.radians(90 + 120 * k)                            # one musket straight upstage (+Y), two to the front corners
    m = (mathutils.Matrix.Rotation(a, 4, 'Z') @ mathutils.Matrix.Translation((r, 0, 0))
         @ mathutils.Matrix.Rotation(-tilt, 4, 'Y'))          # lean the top toward the centre (-X before the turn)
    o.data.transform(m)
bpy.ops.object.select_all(action='DESELECT')
for o in copies: o.select_set(True)
bpy.context.view_layer.objects.active = copies[0]
bpy.ops.object.join()
ob = bpy.context.view_layer.objects.active; ob.name = 'stacked-arms-src'
os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
bpy.ops.export_scene.gltf(filepath=out, export_format='GLB', use_selection=True, export_apply=True, export_yup=True)
print(f'STACK {out}: {len(ob.data.polygons)} faces, tilt {math.degrees(tilt):.1f} deg, butt radius {r:.3f} src units', flush=True)
