/* GET /api/browse?u=... : reading mode, a public page rendered inside m360. */
import {appFor} from '../../server/boot.js';

export async function onRequest(context) {
  const app = await appFor((context && context.env) || {});
  return app.browse(context.request);
}
