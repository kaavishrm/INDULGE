/* POST /api/mcp?k=<key>: the Claude connector (server/mcp.js). Kaavish's own Claude reads and changes the OS
   through it; the key is made in Admin, by the owner alone. */
import {appFor} from '../../server/boot.js';

export async function onRequest(context) {
  const env = (context && context.env) || {};
  /* the body first, before the store comes up on a cold instance (see m360.js) */
  let request = context.request;
  if (request.method === 'POST') {
    const text = await request.text();
    request = new Request(request.url, {method: 'POST', headers: request.headers, body: text});
  }
  const app = await appFor(env);
  return app.mcp(request);
}
