"""Shrink the Van Wezel Hall model for midtown.html (THE THIRD HOUSE: VAN WEZEL HALL).

    python -I tools/van-wezel-optimise.py <source.glb> assets/van-wezel-hall.glb

The source is the model another Claude session made for Jack (exported by THREE.GLTFExporter: 1,039 nodes, 964
meshes, 318 materials, 49 procedural-noise PNGs, units FEET, the stage toward -z and the house toward +z). The
output is the same building, in the page's frame and cheap to draw:

  * METRES, TURNED 180 DEGREES about y (x -> -x, z -> -z): the page's convention, upstage +z and the house toward
    -z. The origin stays the model's (the proscenium line at x 0 z 0, the orchestra floor at y 0); the page moves it.
  * Every node's matrix baked into its vertices (positions, and normals by the inverse transpose).
  * DROPPED: the site round the building - Grounds (a 4000 ft plane), Sarasota Bay, Parking, North Tamiami Trail,
    the Palms (216 meshes) and the drive behind the loading dock. The terrace the building stands on (its foyer's
    floor, x +-193 z -22...185 ft) is kept.
  * MERGED by region (house, stage, lift, exterior, basement) and by look: every untextured opaque material becomes one
    vertex-coloured lit mesh per region (its base colour, plus its emissive, per vertex), every unlit one one
    vertex-coloured unlit mesh, the glass one mesh, and each textured material keeps its own mesh with its
    KHR_texture_transform scale baked into the uv. Metalness is dropped (with no environment map a metal face draws
    black); roughness is 0.85 throughout.
  * Welded (one vertex per distinct position, normal, uv and colour), uv only where there is a map, indices uint16
    where they fit; the seats parked 60 ft under the floor dropped; images carried over byte for byte.

Pure Python (no numpy on this machine). Node names in the output: '<region>: <look>' (looks: 'lit', 'unlit',
'glass', 'tex <n>'), which the page reads.
"""
import json, struct, sys, array, math

FT = 0.3048
DROP = {'Grounds', 'Sarasota Bay', 'Parking', 'North Tamiami Trail', 'Palms'}
DROP_MESH_NODES = {384}            # the drive behind the loading dock (a plane z -195...-105 ft)
STAGE = {'Stage', 'Fly loft'}
JUNK_Y = -30 * FT                  # below the basement's floor (-14.4 ft): only the parked seat copies are down there


def read_glb(path):
    b = open(path, 'rb').read()
    assert b[:4] == b'glTF'
    n = struct.unpack_from('<I', b, 12)[0]
    j = json.loads(b[20:20 + n])
    off = 20 + n
    ln = struct.unpack_from('<I', b, off)[0]
    return j, b[off + 8:off + 8 + ln]


def accessor(j, bin_, i):
    a = j['accessors'][i]
    bv = j['bufferViews'][a['bufferView']]
    comp = {5126: ('f', 4), 5125: ('I', 4), 5123: ('H', 2), 5121: ('B', 1)}[a['componentType']]
    n = {'SCALAR': 1, 'VEC2': 2, 'VEC3': 3, 'VEC4': 4}[a['type']]
    stride = bv.get('byteStride', comp[1] * n)
    base = bv.get('byteOffset', 0) + a.get('byteOffset', 0)
    out = []
    if stride == comp[1] * n:
        arr = array.array(comp[0]); arr.frombytes(bin_[base:base + a['count'] * stride])
        for k in range(a['count']): out.append(tuple(arr[k * n:(k + 1) * n]))
    else:
        for k in range(a['count']): out.append(struct.unpack_from('<' + comp[0] * n, bin_, base + k * stride))
    return out


def local(nd):
    if 'matrix' in nd:
        m = nd['matrix']; return [[m[c * 4 + r] for c in range(4)] for r in range(4)]
    t = nd.get('translation', [0, 0, 0]); x, y, z, w = nd.get('rotation', [0, 0, 0, 1]); s = nd.get('scale', [1, 1, 1])
    R = [[1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)], [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)], [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)]]
    return [[R[i][k] * s[k] for k in range(3)] + [t[i]] for i in range(3)] + [[0, 0, 0, 1]]


def mul(A, B): return [[sum(A[i][k] * B[k][jj] for k in range(4)) for jj in range(4)] for i in range(4)]


def normal_matrix(M):
    a = [[M[i][k] for k in range(3)] for i in range(3)]
    det = (a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1]) - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0]) + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0]))
    inv = [[(a[(c + 1) % 3][(r + 1) % 3] * a[(c + 2) % 3][(r + 2) % 3] - a[(c + 1) % 3][(r + 2) % 3] * a[(c + 2) % 3][(r + 1) % 3]) / det for c in range(3)] for r in range(3)]
    return [[inv[c][r] for c in range(3)] for r in range(3)], det   # the inverse's transpose


def main(src, dst):
    j, bin_ = read_glb(src)
    nodes, mats = j['nodes'], j['materials']
    parent = {c: i for i, nd in enumerate(nodes) for c in nd.get('children', [])}
    TURN = [[-FT, 0, 0, 0], [0, FT, 0, 0], [0, 0, -FT, 0], [0, 0, 0, 1]]     # feet -> metres, turned 180 about y
    world = {}

    def W(i):
        if i not in world: world[i] = mul(W(parent[i]), local(nodes[i])) if i in parent else mul(TURN, local(nodes[i]))
        return world[i]

    def names(i):
        out = []
        while True:
            out.append(nodes[i].get('name', ''));
            if i not in parent: return out
            i = parent[i]

    def region(path):
        top = path[-1]
        if top == 'Exterior': return 'exterior'
        if top == 'Basement': return 'basement'
        if 'Orchestra lift' in path: return 'lift'          # its own, so the page can move it
        return 'stage' if any(p in STAGE for p in path) else 'house'

    groups, dropped, kept, junk = {}, 0, 0, [0]
    for i, nd in enumerate(nodes):
        if 'mesh' not in nd: continue
        path = names(i)
        if any(p in DROP for p in path) or i in DROP_MESH_NODES: dropped += 1; continue
        kept += 1
        M = W(i); Nm, det = normal_matrix(M)
        for p in j['meshes'][nd['mesh']]['primitives']:
            assert p.get('mode', 4) == 4
            m = mats[p['material']]; pbr = m.get('pbrMetallicRoughness', {})
            col = pbr.get('baseColorFactor', [1, 1, 1, 1]); em = m.get('emissiveFactor', [0, 0, 0])
            unlit = 'KHR_materials_unlit' in m.get('extensions', {})
            if m.get('alphaMode') == 'BLEND': look, key = 'glass', ('glass', json.dumps(col))
            elif 'baseColorTexture' in pbr:
                look = 'tex'
                key = ('tex', json.dumps({k: v for k, v in m.items() if k != 'name'}, sort_keys=True))
            else: look, key = ('unlit' if unlit else 'lit'), None
            g = groups.setdefault((region(path), look, key), {'mat': m, 'pos': [], 'nrm': [], 'uv': [], 'col': [], 'idx': []})
            P = accessor(j, bin_, p['attributes']['POSITION']); N = accessor(j, bin_, p['attributes']['NORMAL'])
            U = accessor(j, bin_, p['attributes']['TEXCOORD_0']) if 'TEXCOORD_0' in p['attributes'] else [(0, 0)] * len(P)
            idx = [t[0] for t in accessor(j, bin_, p['indices'])] if 'indices' in p else list(range(len(P)))
            sc = [1, 1]
            tt = pbr.get('baseColorTexture', {}).get('extensions', {}).get('KHR_texture_transform')
            if tt:
                assert set(tt) <= {'scale'}, tt
                sc = tt['scale']
            c = [min(1.0, col[k] + em[k]) for k in range(3)]
            base = len(g['pos']) // 3
            for (x, y, z), (a, b, cc), (u, v) in zip(P, N, U):
                g['pos'] += [M[0][0] * x + M[0][1] * y + M[0][2] * z + M[0][3], M[1][0] * x + M[1][1] * y + M[1][2] * z + M[1][3], M[2][0] * x + M[2][1] * y + M[2][2] * z + M[2][3]]
                nx, ny, nz = Nm[0][0] * a + Nm[0][1] * b + Nm[0][2] * cc, Nm[1][0] * a + Nm[1][1] * b + Nm[1][2] * cc, Nm[2][0] * a + Nm[2][1] * b + Nm[2][2] * cc
                l = math.sqrt(nx * nx + ny * ny + nz * nz) or 1
                g['nrm'] += [nx / l, ny / l, nz / l]
                g['uv'] += [u * sc[0], v * sc[1]]
                if look in ('lit', 'unlit'): g['col'] += c
            if det < 0:                                     # a mirrored node: keep the winding (TURN is not one)
                for t in range(0, len(idx), 3): idx[t + 1], idx[t + 2] = idx[t + 2], idx[t + 1]
            Y = g['pos']
            for t in range(0, len(idx), 3):                 # the seats parked 60 ft under the floor (unused copies) go
                a, b, cc = (base + idx[t + q] for q in range(3))
                if max(Y[3 * a + 1], Y[3 * b + 1], Y[3 * cc + 1]) < JUNK_Y: junk[0] += 1; continue
                g['idx'] += [a, b, cc]

    # write
    out = {'asset': {'version': '2.0', 'generator': 'tools/van-wezel-optimise.py (from a THREE.GLTFExporter model)'},
           'scene': 0, 'scenes': [{'nodes': []}], 'nodes': [], 'meshes': [], 'materials': [], 'accessors': [], 'bufferViews': [],
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
    order = sorted(groups, key=lambda k: (k[0], k[1], str(k[2])))
    for k in order:
        g = groups[k]; reg, look, _ = k
        m = g['mat']; pbr = m.get('pbrMetallicRoughness', {})
        if look == 'lit': mat = {'pbrMetallicRoughness': {'metallicFactor': 0, 'roughnessFactor': 0.85}, 'doubleSided': True}
        elif look == 'unlit': mat = {'pbrMetallicRoughness': {'metallicFactor': 0, 'roughnessFactor': 0.9}, 'doubleSided': True, 'extensions': {'KHR_materials_unlit': {}}}
        elif look == 'glass': mat = {'pbrMetallicRoughness': {'baseColorFactor': pbr['baseColorFactor'], 'metallicFactor': 0, 'roughnessFactor': 0.08}, 'alphaMode': 'BLEND', 'doubleSided': True}
        else:
            mat = {'pbrMetallicRoughness': {'baseColorTexture': {'index': tex(pbr['baseColorTexture']['index'])}, 'metallicFactor': 0, 'roughnessFactor': pbr.get('roughnessFactor', 0.85)}, 'doubleSided': True}
            if 'baseColorFactor' in pbr: mat['pbrMetallicRoughness']['baseColorFactor'] = pbr['baseColorFactor']
            if 'emissiveFactor' in m: mat['emissiveFactor'] = m['emissiveFactor']
            if 'emissiveTexture' in m: mat['emissiveTexture'] = {'index': tex(m['emissiveTexture']['index'])}   # its transform is the base map's (the one case shares the scale)
        name = f'{reg}: {look}' + (f' {ntex}' if look == 'tex' else '')
        if look == 'tex': ntex += 1
        mat['name'] = name
        out['materials'].append(mat)
        # weld: one vertex per distinct (position, normal, uv, colour) the kept triangles use (the source repeats them)
        hasuv, hascol = look in ('tex',), bool(g['col'])
        seen, P, N, U, Cc, I = {}, [], [], [], [], []
        for v in g['idx']:
            kk = (tuple(round(x, 5) for x in g['pos'][3 * v:3 * v + 3]), tuple(round(x, 3) for x in g['nrm'][3 * v:3 * v + 3]),
                  tuple(round(x, 5) for x in g['uv'][2 * v:2 * v + 2]) if hasuv else None, tuple(g['col'][3 * v:3 * v + 3]) if hascol else None)
            w = seen.get(kk)
            if w is None:
                w = seen[kk] = len(P) // 3
                P += g['pos'][3 * v:3 * v + 3]; N += g['nrm'][3 * v:3 * v + 3]
                if hasuv: U += g['uv'][2 * v:2 * v + 2]
                if hascol: Cc += g['col'][3 * v:3 * v + 3]
            I.append(w)
        attrs = {'POSITION': acc(P, 3, minmax=True), 'NORMAL': acc(N, 3)}
        if hasuv: attrs['TEXCOORD_0'] = acc(U, 2)
        if hascol: attrs['COLOR_0'] = acc(Cc, 3)
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
          f'({kept} source meshes kept, {dropped} dropped; {junk[0]} parked triangles dropped), {len(out.get("images", []))} images, {tris} triangles, {verts} vertices, {total} bytes')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
