"""Shrink the Carol Morsani Hall model for midtown.html (THE FOURTH HOUSE: CAROL MORSANI HALL).

    python -I tools/carol-morsani-optimise.py <source.glb> assets/carol-morsani-hall.glb

The source is the model another Claude session made for Jack (exported by THREE.GLTFExporter: 2,573 nodes, 2,561 meshes,
43 materials, 19 PNGs, ten KHR_lights_punctual lights, units METRES, the stage toward -z and the lobby's glass toward +z,
the stage floor at y 0, the lobby floor at y 3.2). The output is the same building, in the page's frame and cheap to draw:

  * TURNED 180 DEGREES about y (x -> -x, z -> -z): the page's convention, upstage +z and the house toward -z. The origin
    stays the model's (the proscenium's middle on the stage floor); the page moves and turns it.
  * Every node's matrix baked into its vertices (positions, and normals by the inverse transpose).
  * DROPPED: the site (Hillsborough River, the Riverwalk, and the skyline picture across the river: an unnamed 420 x 110 m
    quad 260 m out, node 963), the lights (the page bakes its own), and the marked-out spot
    booth ("Spot booth area (to do)", its floor and back wall, and the "SPOT BOOTH - TO DO (placeholder)" group: its volume
    and its sign; the page builds the booth there).
  * MERGED by region and by look. Regions: 'curtain' (the main curtain and its valance, so the page can fly them),
    'glass' (the lobby's glass front and every glass balustrade, look 'glass'), 'house' (the rest). Looks: every
    untextured opaque material one vertex-coloured lit mesh per region ('lit'), every unlit one ('unlit'), each textured
    material its own mesh ('tex <n>', its KHR_texture_transform scale baked into the uv), the glass one mesh. Metalness
    and sheen are dropped; roughness 0.85.
  * THE SEATS: the file's 3,203 are three boxes each (a red block, a textured block round it, a thin stand; nodes 2554-2556,
    one 12-triangle box per seat, in the same order in each). They go to region 'seatcol' (the page keeps them as the walk's
    collision, undrawn) and a table in the scene's extras, 'seats': per seat its floor point x y z, its facing (the unit
    vector toward the stage) fx fz, its width, and the red block's colour r g b, every number rounded; the page draws a
    chair at each (THE FOURTH HOUSE: THE CHAIRS).
  * THE SOURCE'S VERTEX COLOURS KEPT (one mesh has them: the seats' cushions, white in their material), times the
    material's colour.
  * THE LIGHT BAKED IN, as the page bakes the Van Wezel's (VW_LIGHT): every vertex but the unlit and the glass a colour
    of 0.50 + 0.30 |n . L| + 0.20 max(0, n.y) times its own (white under a map), stored as normalised bytes; the normals are
    then dropped (the page draws it MeshBasic, unlit).
  * Welded (one vertex per distinct position, uv and colour), uv only where there is a map, indices uint16 where they
    fit; images carried over byte for byte.

Pure Python (no numpy on this machine). It borrows the reader and the matrix helpers from van-wezel-optimise.py.
Node names in the output: '<region>: <look>', which the page reads.
"""
import json, struct, sys, array, math, os, importlib.util

_vw = importlib.util.spec_from_file_location('vwopt', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'van-wezel-optimise.py'))
vw = importlib.util.module_from_spec(_vw); _vw.loader.exec_module(vw)

DROP = {'Hillsborough River', 'Riverwalk', 'Spot booth area (to do)'}
DROP_NODES = {963}                 # the skyline picture (an unnamed quad x -210...210, z 260 in the file)
CURTAIN = {'Main curtain', 'Valance'}
SEAT_NODES = {'cushion': 2554, 'shell': 2555, 'stand': 2556}   # the seats' three boxes (see above)
_L = (-0.35, 0.80, -0.48); LIGHT = tuple(x / math.sqrt(sum(y * y for y in _L)) for x in _L)   # the page's VW_LIGHT


def main(src, dst):
    j, bin_ = vw.read_glb(src)
    nodes, mats = j['nodes'], j['materials']
    parent = {c: i for i, nd in enumerate(nodes) for c in nd.get('children', [])}
    TURN = [[-1, 0, 0, 0], [0, 1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]]
    world = {}

    def W(i):
        if i not in world: world[i] = vw.mul(W(parent[i]), vw.local(nodes[i])) if i in parent else vw.mul(TURN, vw.local(nodes[i]))
        return world[i]

    groups, dropped, kept, seatsrc = {}, 0, 0, {}
    for i, nd in enumerate(nodes):
        if 'mesh' not in nd: continue
        name = nd.get('name', '')
        if name in DROP or i in DROP_NODES or (i in parent and nodes[parent[i]].get('name', '').startswith('SPOT BOOTH')): dropped += 1; continue
        kept += 1
        M = W(i); Nm, det = vw.normal_matrix(M)
        for p in j['meshes'][nd['mesh']]['primitives']:
            assert p.get('mode', 4) == 4
            m = mats[p['material']]; pbr = m.get('pbrMetallicRoughness', {})
            col = pbr.get('baseColorFactor', [1, 1, 1, 1]); em = m.get('emissiveFactor', [0, 0, 0])
            unlit = 'KHR_materials_unlit' in m.get('extensions', {})
            reg = 'curtain' if name in CURTAIN else 'seatcol' if i in SEAT_NODES.values() else 'house'
            if reg == 'seatcol': look, key = 'lit', None
            elif m.get('alphaMode') == 'BLEND' and 'baseColorTexture' not in pbr: reg, look, key = 'glass', 'glass', ('glass', json.dumps(col))
            elif 'baseColorTexture' in pbr:
                look = 'tex'
                key = ('tex', json.dumps({k: v for k, v in m.items() if k != 'name'}, sort_keys=True))
            else: look, key = ('unlit' if unlit else 'lit'), None
            g = groups.setdefault((reg, look, key), {'mat': m, 'pos': [], 'nrm': [], 'uv': [], 'col': [], 'idx': []})
            P = vw.accessor(j, bin_, p['attributes']['POSITION']); N = vw.accessor(j, bin_, p['attributes']['NORMAL'])
            U = vw.accessor(j, bin_, p['attributes']['TEXCOORD_0']) if 'TEXCOORD_0' in p['attributes'] else [(0, 0)] * len(P)
            VC = None                                       # the source's own vertex colours (the seats' cushions carry theirs only there)
            if 'COLOR_0' in p['attributes']:
                ct = j['accessors'][p['attributes']['COLOR_0']]['componentType']; sc_ = {5126: 1.0, 5121: 1 / 255, 5123: 1 / 65535}[ct]
                VC = [tuple(q * sc_ for q in t[:3]) for t in vw.accessor(j, bin_, p['attributes']['COLOR_0'])]
            idx = [t[0] for t in vw.accessor(j, bin_, p['indices'])] if 'indices' in p else list(range(len(P)))
            sc = [1, 1]
            tt = pbr.get('baseColorTexture', {}).get('extensions', {}).get('KHR_texture_transform')
            if tt:
                assert set(tt) <= {'scale'}, tt
                sc = tt['scale']
            c = [min(1.0, col[k] + em[k]) for k in range(3)]
            base = len(g['pos']) // 3
            for vi, ((x, y, z), (a, b, cc), (u, v)) in enumerate(zip(P, N, U)):
                g['pos'] += [M[0][0] * x + M[0][1] * y + M[0][2] * z + M[0][3], M[1][0] * x + M[1][1] * y + M[1][2] * z + M[1][3], M[2][0] * x + M[2][1] * y + M[2][2] * z + M[2][3]]
                nx, ny, nz = Nm[0][0] * a + Nm[0][1] * b + Nm[0][2] * cc, Nm[1][0] * a + Nm[1][1] * b + Nm[1][2] * cc, Nm[2][0] * a + Nm[2][1] * b + Nm[2][2] * cc
                l = math.sqrt(nx * nx + ny * ny + nz * nz) or 1
                g['nrm'] += [nx / l, ny / l, nz / l]
                g['uv'] += [u * sc[0], v * sc[1]]
                if look != 'glass':
                    k = 1.0 if unlit else 0.50 + 0.30 * abs((nx * LIGHT[0] + ny * LIGHT[1] + nz * LIGHT[2]) / l) + 0.20 * max(0.0, ny / l)
                    base_c = c if look in ('lit', 'unlit') else [1.0, 1.0, 1.0]
                    if VC: base_c = [base_c[q] * VC[vi][q] for q in range(3)]
                    g['col'] += [min(255, round(255 * base_c[q] * k)) for q in range(3)]
            if det < 0:                                     # a mirrored node: keep the winding (TURN is a rotation)
                for t in range(0, len(idx), 3): idx[t + 1], idx[t + 2] = idx[t + 2], idx[t + 1]
            g['idx'] += [base + t for t in idx]
            if i in SEAT_NODES.values(): seatsrc[i] = (g['pos'][3 * base:], VC)

    # the seat table, off the boxes as placed (turned): each piece is 24 vertices (a box's, indexed), 8 corners
    seats = []
    cu, cvc = seatsrc[SEAT_NODES['cushion']]; st, _ = seatsrc[SEAT_NODES['stand']]
    n = len(cu) // 72; assert n * 72 == len(cu) == len(st), (len(cu), len(st))
    for s in range(n):
        pts = sorted(set(tuple(round(v, 4) for v in cu[s * 72 + 3 * k:s * 72 + 3 * k + 3]) for k in range(24)))
        cx, cz = sum(p[0] for p in pts) / len(pts), sum(p[2] for p in pts) / len(pts)
        p0 = pts[0]; near = sorted(pts[1:], key=lambda p: sum((a - b) ** 2 for a, b in zip(p, p0)))[:3]
        edges = [(p[0] - p0[0], p[2] - p0[2]) for p in near if abs(p[1] - p0[1]) < 1e-3]   # the two horizontal edges
        to = (-cx, 2.0 - cz); tl = math.hypot(*to)                                         # toward the stage (its lip's middle, turned)
        dep = max(edges, key=lambda e: abs(e[0] * to[0] + e[1] * to[1]) / math.hypot(*e))
        wid = min(edges, key=lambda e: abs(e[0] * to[0] + e[1] * to[1]) / math.hypot(*e))
        dl = math.hypot(*dep); fx, fz = dep[0] / dl, dep[1] / dl
        if fx * to[0] + fz * to[1] < 0: fx, fz = -fx, -fz
        floor = min(st[s * 72 + 3 * k + 1] for k in range(24))
        col = cvc[s * 24] if cvc else (0.5, 0.05, 0.05)
        seats += [round(cx, 3), round(floor, 3), round(cz, 3), round(fx, 4), round(fz, 4), round(math.hypot(*wid) + 0.045, 3)] + [round(q, 3) for q in col[:3]]

    out = {'asset': {'version': '2.0', 'generator': 'tools/carol-morsani-optimise.py (from a THREE.GLTFExporter model)'},
           'scene': 0, 'scenes': [{'nodes': [], 'extras': {'seats': seats, 'seatFields': 'x y z fx fz width r g b'}}], 'nodes': [], 'meshes': [], 'materials': [], 'accessors': [], 'bufferViews': [],
           'buffers': [], 'extensionsUsed': ['KHR_materials_unlit']}
    blob = bytearray()

    def view(data, target=None):
        while len(blob) % 4: blob.append(0)
        bv = {'buffer': 0, 'byteOffset': len(blob), 'byteLength': len(data)}
        if target: bv['target'] = target
        blob.extend(data); out['bufferViews'].append(bv); return len(out['bufferViews']) - 1

    def acc(vals, n, ctype='f', minmax=False):
        a = array.array(ctype, vals)
        v = view(a.tobytes(), 34963 if ctype in 'IH' else 34962)
        d = {'bufferView': v, 'componentType': {'I': 5125, 'H': 5123, 'f': 5126}[ctype], 'count': len(vals) // n, 'type': {1: 'SCALAR', 2: 'VEC2', 3: 'VEC3'}[n]}
        if minmax: d['min'] = [min(vals[k::n]) for k in range(n)]; d['max'] = [max(vals[k::n]) for k in range(n)]
        out['accessors'].append(d); return len(out['accessors']) - 1

    texmap = {}

    def tex(i):
        if i in texmap: return texmap[i]
        t = j['textures'][i]; im = j['images'][t['source']]; bv = j['bufferViews'][im['bufferView']]
        data = bin_[bv.get('byteOffset', 0):bv.get('byteOffset', 0) + bv['byteLength']]
        out.setdefault('images', []).append({'mimeType': im['mimeType'], 'bufferView': view(data)})
        out.setdefault('samplers', [{'magFilter': 9729, 'minFilter': 9987, 'wrapS': 10497, 'wrapT': 10497}])
        out.setdefault('textures', []).append({'sampler': 0, 'source': len(out['images']) - 1})
        texmap[i] = len(out['textures']) - 1; return texmap[i]

    ntex = 0; tris = 0; verts = 0
    for k in sorted(groups, key=lambda k: (k[0], k[1], str(k[2]))):
        g = groups[k]; reg, look, _ = k
        m = g['mat']; pbr = m.get('pbrMetallicRoughness', {})
        if look == 'lit': mat = {'pbrMetallicRoughness': {'metallicFactor': 0, 'roughnessFactor': 0.85}, 'doubleSided': True}
        elif look == 'unlit': mat = {'pbrMetallicRoughness': {'metallicFactor': 0, 'roughnessFactor': 0.9}, 'doubleSided': True, 'extensions': {'KHR_materials_unlit': {}}}
        elif look == 'glass': mat = {'pbrMetallicRoughness': {'baseColorFactor': pbr['baseColorFactor'], 'metallicFactor': 0, 'roughnessFactor': 0.08}, 'alphaMode': 'BLEND', 'doubleSided': True}
        else:
            mat = {'pbrMetallicRoughness': {'baseColorTexture': {'index': tex(pbr['baseColorTexture']['index'])}, 'metallicFactor': 0, 'roughnessFactor': 0.85}, 'doubleSided': True}
            if 'baseColorFactor' in pbr: mat['pbrMetallicRoughness']['baseColorFactor'] = pbr['baseColorFactor']
            if 'emissiveFactor' in m: mat['emissiveFactor'] = m['emissiveFactor']
            if m.get('alphaMode') == 'BLEND': mat['alphaMode'] = 'BLEND'
            if 'KHR_materials_unlit' in m.get('extensions', {}): mat['extensions'] = {'KHR_materials_unlit': {}}
        name = f'{reg}: {look}' + (f' {ntex}' if look == 'tex' else '')
        if look == 'tex': ntex += 1
        mat['name'] = name
        out['materials'].append(mat)
        hasuv, hascol = look == 'tex', bool(g['col'])
        seen, P, N, U, Cc, I = {}, [], [], [], [], []
        for v in g['idx']:
            kk = (tuple(round(x, 5) for x in g['pos'][3 * v:3 * v + 3]),
                  tuple(round(x, 5) for x in g['uv'][2 * v:2 * v + 2]) if hasuv else None, tuple(g['col'][3 * v:3 * v + 3]) if hascol else None)
            w = seen.get(kk)
            if w is None:
                w = seen[kk] = len(P) // 3
                P += g['pos'][3 * v:3 * v + 3]
                if hasuv: U += g['uv'][2 * v:2 * v + 2]
                if hascol: Cc += g['col'][3 * v:3 * v + 3]
            I.append(w)
        attrs = {'POSITION': acc(P, 3, minmax=True)}
        if hasuv: attrs['TEXCOORD_0'] = acc(U, 2)
        if hascol:
            v = view(array.array('B', Cc).tobytes() + bytes(1) * ((-len(Cc)) % 4), 34962)   # (each vertex 3 bytes: no stride needed)
            out['accessors'].append({'bufferView': v, 'componentType': 5121, 'normalized': True, 'count': len(Cc) // 3, 'type': 'VEC3'}); attrs['COLOR_0'] = len(out['accessors']) - 1
        verts += len(P) // 3
        out['meshes'].append({'name': name, 'primitives': [{'attributes': attrs, 'indices': acc(I, 1, 'H' if len(P) // 3 < 65536 else 'I'), 'material': len(out['materials']) - 1}]})
        out['nodes'].append({'name': name, 'mesh': len(out['meshes']) - 1})
        out['scenes'][0]['nodes'].append(len(out['nodes']) - 1)
        tris += len(I) // 3
    while len(blob) % 4: blob.append(0)
    out['buffers'] = [{'byteLength': len(blob)}]
    js = json.dumps(out, separators=(',', ':')).encode()
    while len(js) % 4: js += b' '
    total = 12 + 8 + len(js) + 8 + len(blob)
    with open(dst, 'wb') as f:
        f.write(struct.pack('<4sII', b'glTF', 2, total))
        f.write(struct.pack('<I4s', len(js), b'JSON')); f.write(js)
        f.write(struct.pack('<I4s', len(blob), b'BIN\x00')); f.write(blob)
    print(f'{src}: {len(nodes)} nodes, {len(j["meshes"])} meshes, {len(mats)} materials -> {dst}: {len(out["meshes"])} meshes '
          f'({kept} source meshes kept, {dropped} dropped), {len(seats) // 9} seats, {len(out.get("images", []))} images, {tris} triangles, {verts} vertices, {total} bytes')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
