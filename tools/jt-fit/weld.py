"""Blender headless: weld a source's split vertices so fit.py's decimate does not shred it.

    blender -b --factory-startup --python tools/jt-fit/weld.py -- <source .glb> <out .glb> [--dist=0.0003] [--faces=N]

Some sources (AI-made or scanned meshes exported to glTF, e.g. saddle.glb) arrive with every UV seam and every
65k-vertex chunk split into separate vertices. Blender's collapse decimate cannot merge across those splits, so at a low
ratio it leaves a cloud of loose triangles (holes everywhere). This joins all mesh objects into one, merges vertices
closer than --dist (UVs live on the loops, so the texture survives), optionally pre-decimates to about --faces, and writes
a GLB. Point a recipe's "src" at that GLB (run fit.py with the folder it was written to as the src dir).
The welded GLB is a derived copy of a third-party source: write it to a scratch folder, never into the repository."""
import bpy, bmesh, sys

argv = sys.argv[sys.argv.index('--') + 1:]
src, out = argv[0], argv[1]
opt = dict(a[2:].split('=', 1) for a in argv[2:] if a.startswith('--') and '=' in a)
dist = float(opt.get('dist', 0.0003)); faces = int(opt.get('faces', 0))

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=src)
ms = [o for o in bpy.context.scene.objects if o.type == 'MESH']
bpy.ops.object.select_all(action='DESELECT')
for o in ms: o.select_set(True)
bpy.context.view_layer.objects.active = ms[0]
if len(ms) > 1: bpy.ops.object.join()
ob = bpy.context.view_layer.objects.active; me = ob.data
v0, f0 = len(me.vertices), len(me.polygons)
bm = bmesh.new(); bm.from_mesh(me)
bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=dist)
bm.to_mesh(me); bm.free()
try: bpy.ops.mesh.customdata_custom_splitnormals_clear()
except Exception: pass
v1 = len(me.vertices)
if faces and len(me.polygons) > faces:
    m = ob.modifiers.new('dec', 'DECIMATE'); m.ratio = faces / len(me.polygons)
    bpy.ops.object.modifier_apply(modifier=m.name)
bpy.ops.export_scene.gltf(filepath=out, export_format='GLB', use_selection=True)
print(f"WELD {src}: {v0} verts / {f0} faces -> welded {v1} verts -> {len(me.polygons)} faces -> {out}", flush=True)
