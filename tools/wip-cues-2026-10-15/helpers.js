// scratch page helpers: DUMP (the pool dump, same shape as the 2026-10-13 dump), DUMPALL, REACH (aim test), POSE (actor set-local)
window.DUMP = async function (tid) {
  const M = MIDTOWN, THREE = M.THREE, G = M.actors.group; G.updateWorldMatrix(true, false);
  const tr = M.show.tracks.find(t => t.id === tid);
  const cues = M.show.cues.filter(c => c.track === tid);
  const units = M.lx.units, out = [];
  const toL = v => G.worldToLocal(new THREE.Vector3(v.x, v.y, v.z));
  const r2 = v => Math.round(v * 100) / 100;
  for (let i = 0; i < cues.length; i++) {
    const c = cues[i];
    const until = i + 1 < cues.length ? cues[i + 1].at : Math.max(tr.len, c.at + 1);
    const sampled = Math.max(c.at, until - 0.05);
    M.show.seek(tid, sampled); M.show.settle();
    const pools = [];
    for (const u of units) {
      const s = M.lx.get(u);
      if (!s.lit || s.type === 'hazer') continue;
      const b = M.lx.beam(u);
      const o = toL(b.origin), dW = new THREE.Vector3(b.dir.x, b.dir.y, b.dir.z);
      const p2 = toL(new THREE.Vector3(b.origin.x + dW.x, b.origin.y + dW.y, b.origin.z + dW.z)); const d = p2.sub(o).normalize();
      const tz = Math.tan((s.zoom || 0) / 2 * Math.PI / 180), lensR = b.radius - tz * b.dist;
      const down = Math.round(Math.asin(Math.max(-1, Math.min(1, -d.y))) * 180 / Math.PI);
      const P = { ch: String(s.channels && s.channels.length ? s.channels[0] : s.id.replace(/^ch/, '')), id: s.id, type: s.type, level: r2(s.level), color: s.color, zoom: r2(s.zoom), gobo: s.gobo, from: [r2(o.x), r2(o.y), r2(o.z)] };
      let lands = 'nothing';
      if (b.hit) {
        const h = toL(b.hit), up = b.normal ? b.normal.y : 0;
        P.hit = [r2(h.x), r2(h.y), r2(h.z)]; P.hitR = r2(b.radius); P.hitUp = r2(up);
        if (up < 0.7) lands = 'wall/vertical';
        else if (h.z > 6.6 || Math.abs(h.x) > 11) lands = 'house';
        else if (h.y < 0.2) lands = 'deck';
        else if (Math.abs(h.y - 2.743) < 0.15) lands = 'gallery';
        else lands = 'floor ' + h.y.toFixed(2);
      }
      if (d.y < -1e-3) { const t = (0.045 - o.y) / d.y; if (t > 0) { P.deck = [r2(o.x + d.x * t), r2(o.z + d.z * t)]; P.deckR = r2(lensR + tz * t); } }
      P.lands = lands; P.down = down;
      P.kind = s.type === 'lycian' ? 'followspot' : /^colorblaze/.test(s.type) ? 'strip' : down < 25 ? 'side' : (s.zoom <= 14 || ((lands === 'deck' || lands === 'gallery' || lands.startsWith('floor')) && b.radius <= 1)) ? 'special' : 'wash';
      pools.push(P);
    }
    out.push({ q: c.q, at: c.at, until, sampled, real: c.real, label: c.label || null, pools });
  }
  const doc = { track: tid, title: tr.title, len: tr.len, cues: out };
  await fetch('/save/' + tid + '.json', { method: 'POST', body: JSON.stringify(doc) });
  return out.length;
};
window.DUMPALL = async (a, b) => { const ids = MIDTOWN.show.tracks.map(t => t.id).slice(a, b); let n = 0; for (const id of ids) n += await DUMP(id); return n; };
window.REACH = function (list) {
  const M = MIDTOWN, THREE = M.THREE, G = M.actors.group; G.updateWorldMatrix(true, false);
  return list.map(([ch, x, y, z]) => {
    const P = G.localToWorld(new THREE.Vector3(x, y, z));
    M.lx.aim(+ch, P, 0, true);
    const b = M.lx.beam(+ch);
    if (!b || !b.hit) return { ch, t: [x, y, z], hit: null };
    const h = G.worldToLocal(b.hit.clone()), o = G.worldToLocal(b.origin.clone());
    return { ch, t: [x, y, z], hit: [h.x, h.y, h.z].map(v => +v.toFixed(2)), up: b.normal ? +b.normal.y.toFixed(2) : null, miss: +Math.hypot(h.x - x, h.z - z).toFixed(2),
      down: +(Math.atan2(o.y - h.y, Math.hypot(o.x - h.x, o.z - h.z)) * 180 / Math.PI).toFixed(0) };
  });
};
// where every lit special-ish unit lands now, and every visible actor, set-local (after seek + settle)
window.LOOK = function (tid, sec, chs) {
  const M = MIDTOWN, THREE = M.THREE, G = M.actors.group;
  M.show.seek(tid, sec); M.show.settle(); G.updateWorldMatrix(true, false);
  const tr = M.show.tracks.find(t => t.id === tid), T = tr.start + sec;
  const acts = M.actors.list ? (typeof M.actors.list === 'function' ? M.actors.list() : M.actors.list) : [];
  const ids = (Array.isArray(acts) ? acts : []).map(a => a.id || a);
  const A = {};
  for (const id of ids) { const p = M.actors.pose(id, T); if (p && p.visible !== false) A[id] = [+p.x.toFixed(2), +p.y.toFixed(2), +p.z.toFixed(2)]; }
  const L = {};
  for (const ch of chs) { const s = M.lx.get(+ch); if (!s || !s.lit) { L[ch] = 'dark'; continue; } const b = M.lx.beam(+ch); if (!b.hit) { L[ch] = 'nohit'; continue; } const h = G.worldToLocal(b.hit.clone()); L[ch] = [+h.x.toFixed(2), +h.y.toFixed(2), +h.z.toFixed(2), 'r' + b.radius.toFixed(2), 'lv' + s.level.toFixed(2)]; }
  return { A, L };
};
'helpers ok';
