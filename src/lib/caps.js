// Runtime capabilities from the claude.ai viewer. Everything here is optional:
// outside a viewer (local file, GitHub Pages) every capability stays null and
// the app runs exactly as before.
const caps = { db: null, user: null, sample: null, downloads: null, ready: false };
const listeners = new Set();

export const getCaps = () => caps;
export const onCaps = fn => (listeners.add(fn), () => listeners.delete(fn));

export async function initCaps() {
  const c = typeof window !== 'undefined' ? window.claude : null;
  if (!c || typeof c.use !== 'function') { caps.ready = true; emit(); return caps; }
  const get = name => c.use(name).catch(() => null);
  const [db, user, sample, downloads] = await Promise.all([get('db'), get('user'), get('sample'), get('downloads')]);
  Object.assign(caps, { db, user, sample, downloads, ready: true });
  emit();
  return caps;
}

// Mark a capability as refused for the rest of this view (e.g. sample not_granted).
export function dropCap(name) { caps[name] = null; emit(); }

function emit() { for (const l of listeners) { try { l(caps); } catch (e) { /* ignore */ } } }
