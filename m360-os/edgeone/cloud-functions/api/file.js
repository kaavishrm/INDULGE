/* GET /api/file?id=... : an attachment, for anyone allowed to see its room. */
import {appFor} from '../../server/boot.js';

export async function onRequest(context) {
  const app = await appFor((context && context.env) || {});
  return app.file(context.request);
}
