// The pool dump: where every lit unit lands, cue by cue, as midtown.html draws it.  It is what tools/spot-audit.py and
// tools/blocking-pools.py read.  Paste into the console of midtown.html served by tools/pool-dump-serve.py (it saves each track
// to that server's folder), wait for the page to load, then:
//
//     await DUMPALL(0, 23); await DUMPALL(23, 46);      // two calls: one call over the whole show passes 45 s in the Browser pane
//
// Per track a file <track>.json: { track, title, len, cues: [ { q, at, until, sampled, real, label, pools: [ POOL ] } ] }.
// `until` is the next cue's GO, or for a track's last cue the track's end (the open tail of 2-23: a second); the look is read at
// `sampled` = until - 0.05 with every fade and part complete (MIDTOWN.show.seek + settle).  A cue whose hold is 0 (a follower at
// the same moment) is read at its own GO, before its parts: read the follower instead.
//
// POOL: ch, id, type, level 0-1, color, zoom, gobo, from (the lens), hit (where the beam's axis first meets anything), hitR (the
// pool's radius there), hitUp (1 a floor, 0 a wall), deck / deckR (where the axis would meet the deck plane), lands (deck,
// gallery, floor <y>, wall/vertical, house, nothing), down (degrees below horizontal), kind (special: zoom <= 14 or a floor pool
// <= 1 m; wash; side: within 25 deg of horizontal; strip: the ColorBlaze battens; followspot).  All set-local metres - the frame of
// assets/hamilton-blocking.json (MIDTOWN.actors.group, NOT MIDTOWN.set, which is turned 180 degrees).
window.DUMP = async function (tid) {
  const M = MIDTOWN, THREE = M.THREE, G = M.actors.group; G.updateWorldMatrix(true, false);
  const tr = M.show.tracks.find(t => t.id === tid);
  const cues = M.show.cues.filter(c => c.track === tid);
  const units = M.lx.units, out = [];
  const toL = v => G.worldToLocal(new THREE.Vector3(v.x, v.y, v.z));
  const r2 = v => Math.round(v * 100) / 100;
  for (let i = 0; i < cues.length; i++) {
    const c = cues[i];
    const until = i + 1 < cues.length ? cues[i + 1].at : (c.at < tr.len - 0.1 ? tr.len : c.at + 1);
    const sampled = Math.max(c.at, until - 0.05);
    M.show.seek(tid, sampled); M.show.settle();
    const pools = [];
    for (const u of units) {
      const s = M.lx.get(u);
      if (!s.lit || s.type === 'hazer') continue;
      const b = M.lx.beam(u);
      const o = toL(b.origin), dW = new THREE.Vector3(b.dir.x, b.dir.y, b.dir.z);
      const d = toL(new THREE.Vector3(b.origin.x + dW.x, b.origin.y + dW.y, b.origin.z + dW.z)).sub(o).normalize();
      const tz = Math.tan((s.zoom || 0) / 2 * Math.PI / 180), lensR = b.radius - tz * b.dist;
      const down = Math.round(Math.asin(Math.max(-1, Math.min(1, -d.y))) * 180 / Math.PI);
      const P = { ch: String(s.channels && s.channels.length ? s.channels[0] : s.id.replace(/^ch/, '')), id: s.id, type: s.type, level: r2(s.level),
        color: s.color, zoom: r2(s.zoom), gobo: s.gobo, from: [r2(o.x), r2(o.y), r2(o.z)] };
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
      P.kind = s.type === 'lycian' ? 'followspot' : /^colorblaze/.test(s.type) ? 'strip' : down < 25 ? 'side'
        : (s.zoom <= 14 || ((lands === 'deck' || lands === 'gallery' || lands.startsWith('floor')) && b.radius <= 1)) ? 'special' : 'wash';
      pools.push(P);
    }
    out.push({ q: c.q, at: c.at, until, sampled, real: c.real, label: c.label || null, pools });
  }
  await fetch('/save/' + tid + '.json', { method: 'POST', body: JSON.stringify({ track: tid, title: tr.title, len: tr.len, cues: out }) });
  return out.length;
};
window.DUMPALL = async (a = 0, b = 46) => { let n = 0; for (const id of MIDTOWN.show.tracks.map(t => t.id).slice(a, b)) n += await DUMP(id); return n; };
// Can a unit reach a place?  Aims it there now (snap) and reports where the beam really lands: [ch, x, y, z] set-local each.
// A balcony or a gallery behind a rail can pass or fail by the head's starting pose - seek to the cue before first.
window.REACH = list => {
  const M = MIDTOWN, THREE = M.THREE, G = M.actors.group; G.updateWorldMatrix(true, false);
  return list.map(([ch, x, y, z]) => {
    M.lx.aim(+ch, G.localToWorld(new THREE.Vector3(x, y, z)), 0, true);
    const b = M.lx.beam(+ch); if (!b || !b.hit) return { ch, hit: null };
    const h = G.worldToLocal(b.hit.clone());
    return { ch, hit: [h.x, h.y, h.z].map(v => +v.toFixed(2)), floor: b.normal ? b.normal.y > 0.7 : false, miss: +Math.hypot(h.x - x, h.z - z).toFixed(2) };
  });
};
'pool dump ready';
