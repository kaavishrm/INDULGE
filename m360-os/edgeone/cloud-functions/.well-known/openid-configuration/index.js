/* /.well-known/openid-configuration: the Claude connector's sign-in (server/oauth.js). */
import {appFor} from '../../../server/boot.js';

export async function onRequest(context) {
  const env = (context && context.env) || {};
  /* the body first, before the store comes up on a cold instance (see api/m360.js) */
  let request = context.request;
  if (request.method === 'POST') {
    const text = await request.text();
    request = new Request(request.url, {method: 'POST', headers: request.headers, body: text});
  }
  const app = await appFor(env);
  return app.oauth(request);
}
