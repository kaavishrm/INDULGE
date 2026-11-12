/* The one m360 OS API: POST /api/m360 {a: action, ...}. The store and the app come from server/boot.js. */
import {appFor} from '../../server/boot.js';

export async function onRequest(context) {
  const env = (context && context.env) || {};
  /* v50.6: the body is read before anything slow (setting up the store on a cold instance), which otherwise left
     the platform's request stream unreadable: "bad json" on the first request an instance served */
  let request = context.request;
  if (request.method === 'POST') {
    const text = await request.text();
    request = new Request(request.url, {method: 'POST', headers: request.headers, body: text});
  }
  const app = await appFor(env);
  return app(request);
}
