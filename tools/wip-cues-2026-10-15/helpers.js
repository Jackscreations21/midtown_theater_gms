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
window.SHOTSETUP = () => { const M = MIDTOWN; M.renderer.setSize(1280, 760, false); M.camera.aspect = 1280 / 760; M.camera.updateProjectionMatrix(); };
window.CAM = { pos: [0, 4.2, 10.5], at: [0, 1.4, 0] };
window.SHOT = async (tid, sec, name, cam) => {
  const M = MIDTOWN, cv = M.renderer.domElement; SHOTSETUP();
  M.show.seek(tid, sec); M.show.settle();
  cam = cam || CAM; const G = M.actors.group; G.updateWorldMatrix(true, false);
  const p = G.localToWorld(new M.THREE.Vector3(...cam.pos)), t = G.localToWorld(new M.THREE.Vector3(...cam.at));
  M.camera.position.copy(p); if (M.orbit) { M.orbit.target.copy(t); M.orbit.update(); } M.camera.lookAt(t);
  M.frame();
  const c2 = document.createElement('canvas'); c2.width = cv.width; c2.height = cv.height; c2.getContext('2d').drawImage(cv, 0, 0);
  const blob = await new Promise(r => c2.toBlob(r, 'image/png'));
  await fetch('/save/' + name + '.png', { method: 'POST', body: blob });
  return name;
};
window.CHECK = (tid, sec, chs) => {
  const M = MIDTOWN, G = M.actors.group; G.updateWorldMatrix(true, false);
  const tr = M.show.tracks.find(t => t.id === tid), T = tr.start + sec;
  const ids = ['hamilton','burr','eliza','angelica','peggy','washington','lafayette','mulligan','laurens','king','ens1','ens2','ens3','ens4','ens5','ens6','ens7','ens8','ens9','ens10'];
  const A = ids.map(id => [id, M.actors.pose(id, T)]).filter(([, p]) => p && p.visible !== false);
  return chs.map(ch => { const s = M.lx.get(+ch); if (!s.lit) return ch + ':dark'; const b = M.lx.beam(+ch); if (!b.hit) return ch + ':nohit';
    const h = G.worldToLocal(b.hit.clone()); const r = b.radius;
    const inn = A.filter(([, p]) => Math.abs(p.y - h.y) < 0.6 && Math.hypot(p.x - h.x, p.z - h.z) <= r + 0.3).map(([id, p]) => id + '@' + Math.hypot(p.x - h.x, p.z - h.z).toFixed(2));
    return `${ch}(${h.x.toFixed(2)},${h.y.toFixed(2)},${h.z.toFixed(2)} r${r.toFixed(2)} lv${s.level.toFixed(2)}):${inn.join(',') || 'NOBODY'}`; }).join('  ');
};
window.BATCH = async (L, pre) => { const out = []; for (const [t, s, chs, cam] of L) { const n = `${pre}_${t}_${s}`; await SHOT(t, s, n, cam); out.push(n + ' ' + CHECK(t, s, chs)); } return out.join('\n'); };
window.WAITLOAD = () => new Promise(r => { const t0 = Date.now(); const f = () => { const l = document.getElementById('load'); if ((l && getComputedStyle(l).display === 'none' && window.MIDTOWN && MIDTOWN.show && MIDTOWN.actors) || Date.now() - t0 > 40000) r(); else setTimeout(f, 300); }; f(); });
'helpers ok';
