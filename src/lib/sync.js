// Cross-device sync through the viewer's private db subtree:
//   data/users/<id>/profile   everything except attempts, plus bookkeeping
//   data/users/<id>/att-<n>   attempts, in chunks of CHUNK (each well under 256 KiB)
// Local storage stays the instant cache; the cloud copy is merged in on load and
// whenever another device saves. Attempts and papers are unioned; everything
// else is last-writer-wins by updatedAt.
import { S, subscribe, applyRemote } from './store.js';
import { getCaps } from './caps.js';

const CHUNK = 600;
const DEVICE = (() => {
  try {
    let d = localStorage.getItem('tmua-device');
    if (!d) { d = Math.random().toString(36).slice(2, 10); localStorage.setItem('tmua-device', d); }
    return d;
  } catch (e) { return Math.random().toString(36).slice(2, 10); }
})();

let db = null, base = null, timer = null, pushing = false, again = false;
const pushed = {};           // chunk index -> JSON last written
let lastRev = 0;
let status = 'local';        // local | syncing | synced | offline
const statusListeners = new Set();
export const syncStatus = () => status;
export const onSyncStatus = fn => (statusListeners.add(fn), () => statusListeners.delete(fn));
function setStatus(s) { if (s !== status) { status = s; for (const l of statusListeners) l(s); } }

const attKey = a => `${a.qid}|${a.at}`;

export function mergeStates(local, remote) {
  if (!remote) return local;
  const tomb = new Set([...(local.tomb?.papers || []), ...(remote.tomb?.papers || [])]);
  const byKey = new Map();
  for (const a of [...(remote.attempts || []), ...(local.attempts || [])]) {
    const k = attKey(a);
    const prev = byKey.get(k);
    byKey.set(k, prev ? { ...prev, ...a, reason: a.reason || prev.reason } : a);
  }
  const attempts = Array.from(byKey.values())
    .filter(a => !a.pid || !tomb.has(a.pid))
    .sort((x, y) => x.at - y.at);
  const papers = new Map();
  for (const p of [...(remote.papers || []), ...(local.papers || [])]) if (!tomb.has(p.id)) papers.set(p.id, p);
  const newer = (remote.updatedAt || 0) > (local.updatedAt || 0) ? remote : local;
  return {
    ...newer,
    attempts,
    papers: Array.from(papers.values()),
    tomb: { papers: Array.from(tomb) },
    updatedAt: Math.max(local.updatedAt || 0, remote.updatedAt || 0),
  };
}

async function pull() {
  const prof = await db.doc(`${base}/profile`).get();
  if (!prof.exists) return null;
  const p = prof.data();
  const n = p.chunks || 0;
  const docs = await Promise.all(Array.from({ length: n }, (_, i) => db.doc(`${base}/att-${i}`).get()));
  const attempts = [];
  docs.forEach((d, i) => {
    const a = d.exists ? d.data().a || [] : [];
    pushed[i] = JSON.stringify(a);
    attempts.push(...a);
  });
  lastRev = p.rev || 0;
  return { ...(p.state || {}), attempts, updatedAt: p.state?.updatedAt || 0 };
}

async function push() {
  if (!db) return;
  if (pushing) { again = true; return; }
  pushing = true;
  setStatus('syncing');
  try {
    const { attempts, ...rest } = S();
    const n = Math.max(1, Math.ceil(attempts.length / CHUNK));
    for (let i = 0; i < n; i++) {
      const a = attempts.slice(i * CHUNK, (i + 1) * CHUNK);
      const json = JSON.stringify(a);
      if (pushed[i] === json) continue;
      await db.doc(`${base}/att-${i}`).set({ a });   // one write at a time
      pushed[i] = json;
    }
    lastRev = Date.now();
    await db.doc(`${base}/profile`).set({ state: rest, chunks: n, device: DEVICE, rev: lastRev });
    setStatus('synced');
  } catch (e) {
    setStatus(e && (e.code === 'revoked' || e.code === 'not_granted') ? 'local' : 'offline');
    if (e && (e.code === 'revoked' || e.code === 'not_granted' || e.code === 'invalid_argument')) db = null;
  } finally {
    pushing = false;
    if (again) { again = false; schedule(400); }
  }
}

function schedule(ms = 1500) {
  clearTimeout(timer);
  timer = setTimeout(push, ms);
}

export async function initSync() {
  const { db: d, user } = getCaps();
  if (!d || !user) return false;
  const id = await user.id();
  if (!id) return false;
  db = d;
  base = `data/users/${id}`;
  setStatus('syncing');
  try {
    const remote = await pull();
    if (remote) {
      const merged = mergeStates(S(), remote);
      applyRemote(merged);
    }
    await push();
  } catch (e) {
    setStatus('offline');
  }
  subscribe((st, origin) => { if (origin === 'local' && db) schedule(); });
  // Live updates from the user's other devices.
  db.doc(`${base}/profile`).onSnapshot(async snap => {
    if (!snap.exists || !db) return;
    const p = snap.data();
    if (p.device === DEVICE || (p.rev || 0) <= lastRev) return;
    try {
      const remote = await pull();
      if (!remote) return;
      const merged = mergeStates(S(), remote);
      applyRemote(merged);
      if (merged.attempts.length > remote.attempts.length || merged.papers.length !== (remote.papers || []).length) schedule();
    } catch (e) { /* next snapshot will retry */ }
  }, () => setStatus('offline'));
  window.addEventListener('pagehide', () => { if (timer) { clearTimeout(timer); push(); } });
  return true;
}
