/* module: Claude (v55). Kaavish runs the OS from his own Claude, on his own plan, with no API key.
   The server speaks MCP at /api/mcp (edgeone/server/mcp.js). Claude signs in on this site with OAuth (oauth.js),
   the owner presses Allow once; a key link (v55) stays for apps that cannot sign in.
   Two parts, both for the owner alone:
     M.parts.ClaudeCard  Admin: the address to paste in Claude, the three steps, Disconnect, and the key link
     M.parts.ClaudeBar   HQ: type what you want done, and Claude opens with it written, ready to act on the OS
   Members never see either; the server refuses the key actions to anyone but the owner. */
'use strict';
(function () {
  const {html, React, U, UI} = M;
  const {useState, useEffect} = React;

  const NS = M.claude = {};
  const standalone = () => !!(window.M360_STANDALONE && typeof window.M360_API === 'function');
  const api = (a, body) => window.M360_API(a, body || {});
  const PREFIX = 'Use the m360 OS connector. ';
  /* a new Claude chat with the request already written; the connector does the work */
  NS.url = text => 'https://claude.ai/new?q=' + encodeURIComponent(PREFIX + String(text || '').trim());
  NS.open = text => { const w = window.open(NS.url(text), '_blank', 'noopener'); if (!w) location.href = NS.url(text); };
  NS.link = key => location.origin + '/api/mcp?k=' + key;

  function ClaudeCard() {
    const ctx = M.useCtx();
    const [st, setSt] = useState(null);
    const [fresh, setFresh] = useState('');
    const [busy, setBusy] = useState(false);
    const load = () => api('mcpstatus').then(setSt, () => setSt({on: false, err: true}));
    useEffect(() => { if (ctx.isOwner && standalone()) load(); }, []);
    if (!ctx.isOwner || !standalone()) return null;
    const make = async () => {
      setBusy(true);
      try { const r = await api('mcpkey'); setFresh(NS.link(r.key)); await load(); }
      catch (e) { M.toast((e && e.message) || 'That did not work. Try again in a moment.', true); }
      setBusy(false);
    };
    const off = async () => {
      try { await api('mcpoff'); setFresh(''); await load(); M.toast('Claude is disconnected'); }
      catch (e) { M.toast('That did not work. Try again in a moment.', true); }
    };
    const addr = location.origin + '/api/mcp';
    const copyText = (t, msg) => navigator.clipboard.writeText(t).then(() => M.toast(msg), () => M.toast('Copy is blocked here. Select it and copy it.', true));
    /* v55.1: Claude signs in on this site (OAuth); the address it needs is the plain one */
    return html`<${UI.Card} id="claude-card" title="Claude connector">
      <p class="small ink62" style=${{marginTop: 0}}>Run the OS from your own Claude, on your plan, with no API key. Claude reads and changes everything as you: tasks, clients, projects, the feed. Only you can connect it.</p>
      ${st === null ? html`<${M.Thinking} label="Checking" state="connecting"/>` : html`<div class="stack" style=${{gap: '10px'}}>
        <div class="row between small"><span>Status</span><span id="claude-state">${st.signedIn
          ? html`<${UI.Pill} kind="ink">connected<//>`
          : st.key ? html`<${UI.Pill} kind="ink">key link on<//>` : html`<${UI.Pill} kind="warm">off<//>`}</span></div>
        <div class="stack" style=${{gap: '8px'}} id="claude-steps">
          <input class="input num" id="claude-addr" readonly value=${addr} onFocus=${e => e.target.select()} aria-label="Connector address"/>
          <div class="row" style=${{gap: '8px'}}><${UI.Btn} sm=${true} id="claude-copy-addr" onClick=${() => copyText(addr, 'Address copied')}>Copy address<//></div>
          <ol class="small" style=${{margin: '4px 0 0 18px', padding: 0}}>
            <li>In Claude, open Settings, Connectors, Add custom connector. Name it m360 OS and paste the address.</li>
            <li>Press Connect. This site opens and asks you to allow it. Press Allow.</li>
            <li>Turn it on in a chat from the tools menu, or use the bar on HQ.</li>
          </ol>
          <div class="tiny ink62">Use the same browser you are signed in to here.</div>
        </div>
        ${st.on ? html`<div class="row" style=${{gap: '8px'}}><${UI.ConfirmBtn} onConfirm=${off}>Disconnect Claude<//></div>` : null}
        <details id="claude-keyfold" open=${!!fresh}>
          <summary class="small" style=${{cursor: 'pointer'}}>Key link, for apps that cannot sign in</summary>
          <div class="stack" style=${{gap: '8px', marginTop: '8px'}}>
            ${fresh ? html`<div class="stack" style=${{gap: '8px'}} id="claude-fresh">
              <div class="small">It shows once. Anyone with it can change the OS as you.</div>
              <input class="input num" id="claude-link" readonly value=${fresh} onFocus=${e => e.target.select()} aria-label="Key link"/>
              <div class="row" style=${{gap: '8px'}}><${UI.Btn} sm=${true} id="claude-copy" onClick=${() => copyText(fresh, 'Link copied')}>Copy link<//></div>
            </div>` : null}
            <div class="row" style=${{gap: '8px'}}><${UI.Btn} kind="sec" sm=${true} id="claude-make" disabled=${busy} onClick=${make}>${st.key ? 'Make a new key link' : 'Make a key link'}<//></div>
            ${st.key ? html`<div class="tiny ink62">A new key link stops the old one at once.</div>` : null}
          </div>
        </details>
      </div>`}
    <//>`;
  }
  ClaudeCard.foldTitle = 'Claude';
  ClaudeCard.foldSummary = 'run the OS from your own Claude';
  M.parts.ClaudeCard = ClaudeCard;
  M.adminCards.push(ClaudeCard);

  function ClaudeBar() {
    const ctx = M.useCtx();
    const [text, setText] = useState('');
    if (!ctx.isOwner || !standalone()) return null;
    const go = () => { const t = text.trim(); if (!t) return; NS.open(t); setText(''); };
    return html`<section class="card claude-bar" id="claude-bar">
      <div class="row" style=${{gap: '8px', flexWrap: 'wrap'}}>
        <input class="input" id="claude-ask" style=${{flex: '1 1 260px'}} value=${text} placeholder="Tell Claude what to do in the OS"
          aria-label="Tell Claude what to do in the OS" onInput=${e => setText(e.target.value)} onKeyDown=${e => { if (e.key === 'Enter') go(); }}/>
        <${UI.Btn} id="claude-go" disabled=${!text.trim()} onClick=${go}>Open in Claude<//>
      </div>
      <div class="tiny ink62" style=${{marginTop: '6px'}}>Opens your Claude with this written. Changes show here within seconds. Set it up once in Admin, Claude.</div>
    </section>`;
  }
  M.parts.ClaudeBar = ClaudeBar;
})();
