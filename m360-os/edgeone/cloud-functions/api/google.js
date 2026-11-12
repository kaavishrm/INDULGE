/* Google's sign-in sends the browser back here: GET /api/google?code=...&state=... The core app turns
   the code into that person's tokens and sends them back into m360. */
import {appFor} from '../../server/boot.js';

export async function onRequest(context) {
  const app = await appFor((context && context.env) || {});
  return app.google(context.request);
}
