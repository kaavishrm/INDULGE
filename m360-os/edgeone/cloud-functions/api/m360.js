/* The one m360 OS API: POST /api/m360 {a: action, ...}.
   Storage (v50): Supabase (store-supabase.js), with the EdgeOne Pages Blob store as the fallback while the site
   moves across; the Blob store alone when Supabase cannot be reached.
   v50.1: no setting to paste. The database and its publishable key are named below (a publishable key is
   public by design; the table's row policy is the lock). The lock's key is the server's own: a random name kept
   as an empty blob under ks/m360store~ (the full Blob store still takes an empty value), registered once with
   the database through m360_claim while its claim window is open, and checked by its SHA-256 from then on.
   Environment variables, when set, win: M360_STORE_URL, M360_STORE_ANON, M360_STORE_KEY. */
import {getStore} from '@edgeone/pages-blob';
import {createApp} from '../../server/core.js';
import {supabaseStore, hybridStore, ownKey} from '../../server/store-supabase.js';

const STORE_URL = 'https://fqhmszoclzfwzttvrwng.supabase.co';
const STORE_ANON = 'sb_publishable_8WT3XhPAsVSzzzoV4PiPAQ__0HGkBls';

let app = null, store = null, triedAt = 0;

export async function onRequest(context) {
  const env = (context && context.env) || {};
  /* an instance that came up on the old store alone tries Supabase again every half minute */
  if (app && globalThis.__m360store && globalThis.__m360store.mode === 'edge' && Date.now() - triedAt > 30000) app = null;
  if (!app) {
    triedAt = Date.now();
    const blob = getStore({name: 'm360', consistency: 'strong'});
    const edge = {
      get: (key, opts) => blob.get(key, opts),
      /* opts.onlyIfNew: the create-only write the per-document lock uses (core.js withLock) */
      set: (key, value, opts) => (opts && opts.onlyIfNew ? blob.set(key, value, {onlyIfNew: true}) : blob.set(key, value)),
      delete: key => blob.delete(key),
      list: opts => blob.list(opts)
    };
    store = edge;
    const url = env.M360_STORE_URL || STORE_URL, anon = env.M360_STORE_ANON || STORE_ANON;
    /* what happened is kept for the owner's storestatus (core.js) */
    const info = globalThis.__m360store = {mode: 'edge', at: Date.now(), error: null};
    let key = env.M360_STORE_KEY || '';
    if (!key) { try { key = await ownKey(edge, {url, anon, info}); } catch (e) { info.error = String((e && e.stack) || e).slice(0, 400); } }
    if (key) { store = hybridStore(supabaseStore({url, anon, key}), edge); info.mode = 'supabase'; }
    app = createApp({store, env});
  }
  /* v50.4: the move runs from the owner's storemigrate action (core.js), in big parallel batches, never inside
     ordinary requests, which only read through the old store until it is done */
  globalThis.__m360migrate = store && store.migrate ? (ms => store.migrate(ms)) : null;
  return app(context.request);
}
