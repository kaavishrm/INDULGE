/* One call to the Anthropic Messages API with every failure named, shared by the page's AI (core.js, actions
   ai and aicheck) and the books (books.js). A failure comes back as a clear code and a short reason a person
   can read; the key is never in either.

     ai_key          Anthropic said 401 or 403: the key was refused
     ai_credit       402, or a 400 that speaks of credit, balance, billing or a spend limit
     ai_model        404 or a model not found, after one try on the tier's fallback model
     ai_busy         529 or overloaded, after one wait of about 1.5 s and one more try
     ai_unreachable  the call threw, or no answer came back before the deadline
     rate_limited    429
     prompt_too_large  413, or a prompt past the model's window
     unavailable     anything else (a 500, a 400 that is none of the above)

   A 400 that refuses the fallbacks parameter or the beta header we sent is tried once more with neither. At most one
   extra call per turn, whatever went wrong. The reason is the API's own message, at most 300 characters, with
   every model name replaced by "the model" and anything shaped like a key taken out. */

export const API_URL = 'https://api.anthropic.com/v1/messages';
export const REASON_MAX = 300;
/* EdgeOne stops a function at 30 seconds with a bare 504. The model's answer must be in by 27 seconds after the request
   came in: room for a cold start and the reply, and as few slow answers cut short as that allows (AI_BUDGET_MS in
   the environment changes it for tests) */
export const AI_BUDGET_MS = 27000;
/* the page's codes for a model that failed; HTTP 424 on the way out, so no edge in between swaps the body */
export const AI_DOWN = ['ai_key', 'ai_credit', 'ai_model', 'ai_busy', 'ai_unreachable'];
export const statusOf = code => code === 'rate_limited' ? 429 : code === 'prompt_too_large' ? 413 : 424;
const BUSY_WAIT_MS = 1500;
const sleep = ms => new Promise(r => setTimeout(r, ms));

/* what a person may read of the API's message: no key, no model name, no dashes, one line, 300 characters */
export function cleanReason(text, key) {
  let t = String(text == null ? '' : text);
  if (key) t = t.split(String(key)).join('a key');
  t = t.replace(/sk-ant-[A-Za-z0-9_\-]{4,}/g, 'a key')
    .replace(/\bclaude-[a-z0-9][a-z0-9.\-]*/gi, 'the model')
    .replace(/\s*[\u2012-\u2015]\s*/g, ', ')
    .replace(/!/g, '.')
    .replace(/\s+/g, ' ').trim();
  return t.length > REASON_MAX ? t.slice(0, REASON_MAX - 3).replace(/\s+\S*$/, '') + '...' : t;
}

/* one HTTP answer (or a throw) to {code, reason, retry}; retry is 'model', 'beta' or 'busy' when one more try may help */
export function classify(res) {
  if (res.thrown) {
    return {code: 'ai_unreachable', retry: null, reason: res.thrown === 'time'
      ? 'nothing, no answer came back within ' + Math.round((res.waited || 0) / 1000) + ' seconds'
      : 'nothing, the call did not get through (' + (res.msg || 'network error') + ')'};
  }
  const st = res.status;
  const err = (res.j && res.j.error) || {};
  const type = String(err.type || ''), msg = String(err.message || '');
  const said = msg || type || ('HTTP ' + st);
  if (st === 401 || st === 403 || type === 'authentication_error' || type === 'permission_error') return {code: 'ai_key', retry: null, reason: said};
  if (st === 402 || type === 'billing_error' || (st === 400 && /credit|balance|billing|spend(ing)? limit|usage limit/i.test(msg))) return {code: 'ai_credit', retry: null, reason: said};
  if (st === 404 || type === 'not_found_error' || /^model:/i.test(msg)) return {code: 'ai_model', retry: 'model', reason: said};
  /* only a refusal of the fallbacks parameter or of a beta value we sent: a 400 that merely mentions some other
     beta header (a thinking block bound to another conversation names one) fails the same way twice */
  if (st === 400 && (/fallback/i.test(msg) || /unexpected value\(s\)[\s\S]*anthropic-beta/i.test(msg))) return {code: 'unavailable', retry: 'beta', reason: said};
  if (st === 529 || type === 'overloaded_error' || /overloaded/i.test(msg)) return {code: 'ai_busy', retry: 'busy', reason: said};
  if (st === 429 || type === 'rate_limit_error') return {code: 'rate_limited', retry: null, reason: said};
  if (st === 413 || type === 'request_too_large' || /prompt is too long|too many tokens|request too large/i.test(msg)) return {code: 'prompt_too_large', retry: null, reason: said};
  return {code: 'unavailable', retry: null, reason: said};
}

/* o: {doFetch, key, req (the body), beta (the anthropic-beta header or ''), fallback (a model id or ''),
   deadline (epoch ms by which an answer must be in), wait (ms before a busy retry)}.
   Resolves {ok: true, j, model, calls} or {ok: false, code, reason, calls}; never throws */
export async function askModel(o) {
  const doFetch = o.doFetch || fetch;
  const deadline = Number(o.deadline) || (Date.now() + AI_BUDGET_MS);
  const once = async (req, beta) => {
    const left = deadline - Date.now();
    if (left < 800) return {thrown: 'time', waited: 0};
    const ctl = new AbortController();
    const timer = setTimeout(() => ctl.abort(), left);
    const headers = {'content-type': 'application/json', 'x-api-key': o.key, 'anthropic-version': '2023-06-01'};
    if (beta) headers['anthropic-beta'] = beta;
    const t = Date.now();
    try {
      const r = await doFetch(API_URL, {method: 'POST', headers, body: JSON.stringify(req), signal: ctl.signal});
      const j = await r.json().catch(() => ({}));
      if (ctl.signal.aborted) return {thrown: 'time', waited: Date.now() - t};
      return {status: r.status, ok: r.ok, j};
    } catch (e) {
      return ctl.signal.aborted ? {thrown: 'time', waited: Date.now() - t} : {thrown: 'net', msg: String((e && e.message) || e || '').slice(0, 120)};
    } finally { clearTimeout(timer); }
  };
  const fail = (f, calls) => ({ok: false, code: f.code, reason: cleanReason(f.reason, o.key), calls});
  let req = o.req, beta = o.beta || '';
  let res = await once(req, beta);
  if (res.ok) return {ok: true, j: res.j, model: req.model, calls: 1};
  const f = classify(res);
  /* the one extra call: a fallback model, the same ask without the beta, or the same ask after a short wait */
  let next = null;
  if (f.retry === 'model' && o.fallback && o.fallback !== req.model) next = {req: {...req, model: o.fallback}, beta};
  else if (f.retry === 'beta' && (beta || req.fallbacks !== undefined)) {
    const r2 = {...req};
    delete r2.fallbacks;
    next = {req: r2, beta: ''};
  } else if (f.retry === 'busy' && deadline - Date.now() > (o.wait == null ? BUSY_WAIT_MS : o.wait) + 2000) {
    await sleep(o.wait == null ? BUSY_WAIT_MS : o.wait);
    next = {req, beta};
  }
  if (!next) return fail(f, 1);
  req = next.req; beta = next.beta;
  res = await once(req, beta);
  if (res.ok) return {ok: true, j: res.j, model: req.model, calls: 2};
  const f2 = classify(res);
  /* a second beta complaint is no longer about the beta we dropped */
  return fail(f2.retry === 'beta' ? {...f2, code: 'unavailable'} : f2, 2);
}
