"""Blender headless: list what is inside each source model in Jack's jt-models folder.
blender -b --factory-startup --python tools/jt-fit/inventory.py -- <models dir> <out.json>
For each file: top-level objects, mesh objects with their face counts and world-space size, the whole model's size, the
images (name, pixels). Extracts .zip archives into a temp folder first. Writes a JSON; prints one line per file."""
import bpy, sys, os, json, zipfile, tempfile, glob, mathutils

argv = sys.argv[sys.argv.index('--') + 1:]
src, out = argv[0], argv[1]

def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def load(path):
    ext = os.path.splitext(path)[1].lower()
    if ext in ('.glb', '.gltf'): bpy.ops.import_scene.gltf(filepath=path)
    elif ext == '.fbx': bpy.ops.import_scene.fbx(filepath=path)
    elif ext == '.obj': bpy.ops.wm.obj_import(filepath=path)
    elif ext == '.blend':
        with bpy.data.libraries.load(path, link=False) as (a, b): b.objects = a.objects
        for o in b.objects:
            if o is not None: bpy.context.scene.collection.objects.link(o)
    else: raise ValueError(ext)

def report(path):
    meshes = [o for o in bpy.context.scene.objects if o.type == 'MESH']
    lo, hi = mathutils.Vector((1e9,) * 3), mathutils.Vector((-1e9,) * 3)
    rows = []
    for o in meshes:
        cs = [o.matrix_world @ mathutils.Vector(c) for c in o.bound_box]
        a = mathutils.Vector((min(c[i] for c in cs) for i in range(3))); b = mathutils.Vector((max(c[i] for c in cs) for i in range(3)))
        lo = mathutils.Vector((min(lo[i], a[i]) for i in range(3))); hi = mathutils.Vector((max(hi[i], b[i]) for i in range(3)))
        rows.append({'name': o.name, 'faces': len(o.data.polygons), 'size': [round(b[i] - a[i], 4) for i in range(3)], 'min': [round(a[i], 3) for i in range(3)]})
    rows.sort(key=lambda r: -r['faces'])
    imgs = [{'name': i.name, 'px': list(i.size)} for i in bpy.data.images if i.size[0]]
    return {'file': os.path.basename(path), 'objects': len(bpy.context.scene.objects), 'meshes': len(meshes),
            'faces': sum(r['faces'] for r in rows), 'size_xyz_blender': [round(hi[i] - lo[i], 4) for i in range(3)] if meshes else None,
            'parts': rows[:40], 'images': imgs[:20]}

res = []
tmp = tempfile.mkdtemp(prefix='jtinv')
files = sorted(glob.glob(os.path.join(src, '*')))
for f in files:
    paths = [f]
    if f.lower().endswith('.zip'):
        d = os.path.join(tmp, os.path.basename(f)); zipfile.ZipFile(f).extractall(d)
        paths = [p for p in glob.glob(os.path.join(d, '**', '*'), recursive=True) if os.path.splitext(p)[1].lower() in ('.glb', '.gltf', '.fbx', '.obj', '.blend')]
    elif os.path.splitext(f)[1].lower() not in ('.glb', '.gltf', '.fbx', '.obj', '.blend'): continue
    for p in paths:
        try:
            reset(); load(p); r = report(p); r['source'] = os.path.basename(f)
        except Exception as e:
            r = {'source': os.path.basename(f), 'file': os.path.basename(p), 'error': str(e)[:200]}
        res.append(r)
        print('INV', r.get('source'), '|', r.get('file'), '|', r.get('faces'), 'faces |', r.get('meshes'), 'meshes |', r.get('size_xyz_blender'), '|', len(r.get('images', [])), 'images', r.get('error', ''), flush=True)
json.dump(res, open(out, 'w'), indent=1)
