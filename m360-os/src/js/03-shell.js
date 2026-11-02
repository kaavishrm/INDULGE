/* m360 OS shell: gates, the sections, founder HQ, the v7 frame (glass sidebar, island, phone capsule and tab bar), the buddy in its dock. */
'use strict';
(function () {
  const {html, React, U, UI} = M;

  /* ---------- gates ---------- */
  M.Gate = function Gate({title, line, children}) {
    return html`<div class="gate"><div>
      <${M.Mark} width="150px"/>
      <h1>${title}</h1>
      ${line ? html`<p>${line}</p>` : null}
      ${children ? html`<div class="g-act">${children}</div>` : null}
    </div></div>`;
  };
  /* v38: a page that throws while it draws shows this card, with the menu still there, never a white screen.
     One odd document from anyone must not take the app down for everyone. Moving to another page resets it */
  class Crash extends React.Component {
    constructor(p) { super(p); this.state = {bad: false}; }
    static getDerivedStateFromError() { return {bad: true}; }
    componentDidCatch(e) { try { console.error('m360 page stopped:', e && e.message ? e.message : e); } catch (x) { /* quiet */ } }
    render() {
      if (!this.state.bad) return this.props.children;
      const card = html`<div class="crash-card" role="alert" id="page-crash">
        <h2>This page did not load</h2>
        <p>Your work is saved. Reload to try again, or open another page.</p>
        <button type="button" class="btn" onClick=${() => location.reload()}>Reload</button>
      </div>`;
      return this.props.whole ? html`<${M.Gate} title="m360 did not load" line="Your work is saved. Reload to try again."><button type="button" class="btn" onClick=${() => location.reload()}>Reload</button><//>` : card;
    }
  }
  M.Crash = Crash;
  const GATES = {
    boot: {t: 'Signing you in', l: 'One moment.'},
    nohost: {t: 'Open this inside Claude', l: 'm360 OS runs on claude.ai. Open the shared link there.'},
    nocap: {t: 'Workspace unavailable', l: 'The workspace could not load. Reload in a moment.'},
    noid: {t: 'Sign in to continue', l: 'Sign in to your Claude account, then reload this page.'},
    roster: {t: 'Not on the roster yet', l: "You're signed in, but not on the team roster yet. Kaavish adds you from Admin."}
  };
  M.GateFor = mode => {
    if (mode === 'noid' && M.parts.SignIn) return html`<${M.parts.SignIn}/>`;
    const g = GATES[mode] || GATES.nocap;
    return html`<${M.Gate} title=${g.t} line=${g.l}/>`;
  };

  /* ---------- sections and their tabs ---------- */
  const SECTIONS = {
    home: {label: 'Home', icon: 'today', page: 'Home'},
    work: {label: 'Work', icon: 'tasks', page: 'Work', tabs: [
      {k: 'tasks', label: 'My tasks', route: 'tasks'}, {k: 'projects', label: 'Projects', route: 'projects'},
      {k: 'calendar', label: 'Calendar', route: 'calendar'}, {k: 'reviews', label: 'Reviews', route: 'reviews'},
      {k: 'week', label: 'The week', route: 'week'}]},
    /* v37: three tabs. People we are talking to, proposals in the pipeline, clients we work for. The older
       views (prospects, crm, handshake) still open by their own hash and sit behind "More tools" */
    accounts: {label: 'Accounts', icon: 'clients', page: 'Accounts', tabs: [
      {k: 'talks', label: 'People', route: 'talks'}, {k: 'pipeline', label: 'Pipeline', route: 'pitches'},
      {k: 'clients', label: 'Clients', route: 'clients'}]},
    vibe: {label: 'Vibe', icon: 'feed', page: 'Vibe', tabs: [
      {k: 'feed', label: 'Feed', route: 'feed'}, {k: 'crew', label: 'Crew', route: 'people'},
      {k: 'pulse', label: 'Pulse and ideas', route: 'voice'}, {k: 'scores', label: 'Leaderboard', route: 'scores'}, {k: 'music', label: 'Music', route: 'music'},
      /* the office, team scope (the founder's own office is under HQ) */
      {k: 'office', label: 'Office', route: 'office', member: true}]},
    break: {label: 'Break', icon: 'breath', page: 'Break', tabs: [
      {k: 'play', label: 'Daily', route: 'play'}, {k: 'reset', label: 'Reset', route: 'reset'}, {k: 'care', label: 'Care', route: 'care'}, {k: 'reflect', label: 'Reflect', route: 'reflect'}]},
    base: {label: 'Base', icon: 'database', page: 'Base', tabs: [
      {k: 'people', label: 'People', route: 'base'}, {k: 'companies', label: 'Companies', route: 'companies'}, {k: 'import', label: 'Import', route: 'import'}]},
    chat: {label: 'Chat', icon: 'send', page: 'Chat'},
    workspace: {label: 'Workspace', icon: 'mail', page: 'Workspace', tabs: [
      {k: 'mail', label: 'Mail', route: 'mail'}, {k: 'gcal', label: 'Calendar', route: 'gcal'}, {k: 'drive', label: 'Drive', route: 'drive'}]},
    web: {label: 'Web', icon: 'link', page: 'Web'},
    radar: {label: 'Radar', icon: 'radar', page: 'Radar', tabs: [
      {k: 'news', label: 'News', route: 'radar'}, {k: 'awards', label: 'Awards', route: 'awards'}, {k: 'watch', label: 'Watch', route: 'watch'}]},
    me: {label: 'Me', icon: 'people', page: 'Me', tabs: [
      {k: 'profile', label: 'Profile', route: 'me'}, {k: 'character', label: 'Character', route: 'character'}, {k: 'notes', label: 'Notes', route: 'notes'}, {k: 'trophies', label: 'Trophies', route: 'trophies'}, {k: 'leave', label: 'Leave', route: 'leave'},
      {k: 'handbook', label: 'Handbook', route: 'handbook'}, {k: 'hiring', label: 'Hiring', route: 'hiring'},
      /* what the m360 COO does, read only (the founder runs it from HQ) */
      {k: 'coo', label: 'COO', route: 'coo', member: true}]},
    hq: {label: 'HQ', icon: 'command', page: 'HQ', founder: true, tabs: [
      {k: 'brief', label: 'Intelligence', route: 'hq'}, {k: 'dashboard', label: 'Dashboard', route: 'command'},
      {k: 'coo', label: 'COO', route: 'coo'}, {k: 'office', label: 'Office', route: 'office'},
      {k: 'hiring', label: 'Hiring', route: 'hiring'}]},
    admin: {label: 'Admin', icon: 'desk', page: 'Admin', founder: true},
    books: {label: 'Books', icon: 'log', page: 'Books', founder: true, owner: true, tabs: [
      {k: 'overview', label: 'Overview', route: 'books'}, {k: 'invoices', label: 'Invoices', route: 'invoices'},
      {k: 'statement', label: 'Bank', route: 'statement'}, {k: 'expenses', label: 'Expenses', route: 'expenses'}, {k: 'payroll', label: 'Payroll', route: 'payroll'},
      {k: 'letters', label: 'Letters', route: 'letters'}, {k: 'billing', label: 'Setup', route: 'billing'}]},
    map: {label: 'What\'s here', icon: 'map', page: 'Map'}
  };
  M.SECTIONS = SECTIONS;

  /* every hash, old or new, lands in one section and tab */
  function resolve(page, id, isFounder, isOwner) {
    switch (page) {
      case 'books': case 'accounts-books': case 'ledger': return isOwner ? {s: 'books', t: 'overview'} : {s: 'home'};
      case 'invoices': case 'invoice': return isOwner ? {s: 'books', t: 'invoices', id} : {s: 'home'};
      case 'expenses': case 'expense': return isOwner ? {s: 'books', t: 'expenses', id} : {s: 'home'};
      case 'payroll': case 'payslips': return isOwner ? {s: 'books', t: 'payroll', id} : {s: 'home'};
      case 'letters': case 'letter': return isOwner ? {s: 'books', t: 'letters', id} : {s: 'home'};
      case 'billing': return isOwner ? {s: 'books', t: 'billing', id} : {s: 'home'};
      case 'statement': case 'statements': case 'bank': return isOwner ? {s: 'books', t: 'statement', id} : {s: 'home'};
      case 'home': case 'today': return {s: 'home'};
      case 'map': case 'explore': case 'whats-here': case 'help': return {s: 'map', id};
      case 'break': case 'wellness': case 'games': case 'play': case 'daily': case 'five': return {s: 'break', t: 'play'};
      case 'reset': case 'meditate': case 'breathe': return {s: 'break', t: 'reset'};
      case 'care': case 'reminders': return {s: 'break', t: 'care'};
      case 'reflect': case 'wrapped': return {s: 'break', t: 'reflect'};
      case 'work': return {s: 'work', t: 'tasks'};
      case 'projects': return {s: 'work', t: 'projects', id};
      case 'week': return {s: 'work', t: 'week'};
      case 'calendar': return {s: 'work', t: 'calendar'};
      case 'reviews': case 'review': return {s: 'work', t: 'reviews'};
      case 'trophies': return {s: 'me', t: 'trophies'};
      case 'character': case 'avatar': case 'look': return {s: 'me', t: 'character'};
      case 'clients': return {s: 'accounts', t: 'clients', id};
      case 'accounts': case 'talks': case 'talk': case 'conversations': return {s: 'accounts', t: 'talks', id};
      case 'pitches': case 'pipeline': return {s: 'accounts', t: 'pipeline'};
      case 'prospects': case 'followups': case 'follow-ups': return {s: 'accounts', t: 'prospects', id};
      case 'crm': return {s: 'accounts', t: 'crm'};
      case 'handshake': case 'dm': case 'dms': return {s: 'accounts', t: 'handshake', id};
      case 'web': case 'browser': return {s: 'web'};
      case 'chat': case 'dm': return {s: 'chat', id};
      case 'mail': case 'gmail': case 'workspace': return {s: 'workspace', t: 'mail'};
      case 'gcal': case 'meetings': return {s: 'workspace', t: 'gcal'};
      case 'drive': return {s: 'workspace', t: 'drive'};
      case 'vibe': case 'feed': return {s: 'vibe', t: 'feed'};
      case 'people': case 'crew': return {s: 'vibe', t: 'crew', id};
      case 'voice': case 'pulse': return {s: 'vibe', t: 'pulse'};
      case 'scores': return {s: 'vibe', t: 'scores'};
      case 'music': case 'playlist': return {s: 'vibe', t: 'music'};
      case 'notes': case 'note': return {s: 'me', t: 'notes', id};
      case 'base': case 'contacts': case 'people-base': return {s: 'base', t: 'people', id};
      case 'companies': case 'orgs': return {s: 'base', t: 'companies', id};
      case 'import': return {s: 'base', t: 'import'};
      case 'radar': case 'news': return {s: 'radar', t: 'news'};
      case 'awards': return {s: 'radar', t: 'awards'};
      case 'watch': return {s: 'radar', t: 'watch'};
      case 'me': case 'profile': return {s: 'me', t: 'profile'};
      case 'tasks': return {s: 'work', t: 'tasks', id};
      case 'leave': return {s: 'me', t: 'leave'};
      case 'handbook': return {s: 'me', t: 'handbook', id};
      case 'hiring': return isFounder ? {s: 'hq', t: 'hiring', id} : {s: 'me', t: 'hiring', id};
      case 'hq': return isFounder ? {s: 'hq', t: 'brief'} : {s: 'home'};
      case 'command': return isFounder ? {s: 'hq', t: 'dashboard'} : {s: 'home'};
      /* the m360 COO: the founder's tab under HQ, the charter under Me for everyone else */
      case 'coo': return isFounder ? {s: 'hq', t: 'coo'} : {s: 'me', t: 'coo'};
      /* the virtual office: the founder's under HQ, the team's under Vibe */
      case 'office': case 'studio': case 'coo-office': return isFounder ? {s: 'hq', t: 'office'} : {s: 'vibe', t: 'office'};
      case 'admin': case 'desk': return isFounder ? {s: 'admin'} : {s: 'home'};
      default: return {s: isFounder ? 'hq' : 'home'};
    }
  }
  M.resolveRoute = resolve;

  /* badge counts, derived live */
  M.badges = function badges(ctx) {
    const out = {};
    const reads = ((ctx.coll.acks.map[ctx.uid] || {}).s) || {};
    const unread = Object.keys(ctx.coll.handbook.map)
      .filter(id => (reads[id] || 0) < (ctx.coll.handbook.map[id].updated || 0)).length;
    const myEvals = ((ctx.coll.evals.map[ctx.uid] || {}).e) || {};
    const evals = Object.keys(ctx.coll.candidates.map).filter(cid => {
      const c = ctx.coll.candidates.map[cid];
      return (c.evaluators || []).includes(ctx.uid) && !c.decision && !myEvals[cid];
    }).length;
    out.handbook = unread; out.hiring = evals; out.me = unread + evals;
    out.reviews = (M.reviews ? M.reviews.queue(ctx).filter(t => M.reviews.canReview(ctx, t)).length : 0);
    out.work = out.reviews;
    out.inbox = M.inbox ? M.inbox.unread(ctx) : 0;
    out.chat = (M.rooms && ctx.coll.chat) ? M.rooms.unreadRooms(ctx) : 0;
    if (ctx.isFounder) {
      let pend = 0;
      for (const lu of Object.keys(ctx.coll.leave.map)) {
        const dec = (ctx.coll.leavedec.map[lu] || {}).d || {};
        for (const r of ((ctx.coll.leave.map[lu] || {}).reqs || [])) if (!dec[r.id]) pend++;
      }
      out.join = (M.team && M.team.requests) ? M.team.requests(ctx).length : 0;
      if (ctx.isOwner && M.books) { const td = U.todayStr(); out.books = M.books.invoices(ctx).filter(i => { const st = M.books.status(i, td); return st === 'overdue' || (st === 'part' && i.due && i.due < td); }).length; }
      /* the Admin item counts leave waiting, corrections waiting and people waiting to join */
      out.admin = pend + (M.fixes && M.fixes.pending ? M.fixes.pending(ctx).length : 0) + (out.join || 0);
      out.hq = ctx.flags.filter(f => f.severity === 'high').length;
    }
    return out;
  };
  const Badge = ({n}) => n > 0 ? html`<span class="badge">${n > 99 ? '99' : n}</span>` : null;

  /* the tabs a viewer sees in a section (Hiring under Me only for panel members) */
  function visibleTabs(ctx, section, b) {
    return (SECTIONS[section].tabs || []).filter(t => {
      if (section === 'me' && t.k === 'hiring') return !ctx.isFounder && ((b.hiring || 0) > 0 || Object.keys(ctx.coll.candidates.map).some(id => (ctx.coll.candidates.map[id].evaluators || []).includes(ctx.uid)));
      if (t.founder) return !!ctx.isFounder;
      if (t.member) return !ctx.isFounder;
      return true;
    });
  }

  /* section tabs, used by every section page (the sidebar lists them on wide screens) */
  M.SectionTabs = function SectionTabs({section, active}) {
    const ctx = M.useCtx();
    const b = M.badges(ctx);
    const tabs = visibleTabs(ctx, section, b);
    if (tabs.length < 2) return null;
    return html`<nav class="tabs section-tabs" aria-label=${SECTIONS[section].label}>
      ${tabs.map(t => html`<button key=${t.k} type="button" class=${'tab' + (t.k === active ? ' active' : '')} title=${M.map ? M.map.blurbOf(section, t.k) : ''}
        onClick=${() => M.nav('#' + t.route)}>${t.label}<${Badge} n=${b[t.k] || 0}/></button>`)}
    </nav>`;
  };

  /* ---------- the New menu: every create action in one place ---------- */
  function NewMenu({onClose, onTask, onAsk}) {
    const ctx = M.useCtx();
    /* phones: a bottom sheet like More, Inbox and Ask, in reach of a thumb; the sheet closes itself */
    const phone = M.usePhone();
    const ref = React.useRef(null);
    const [pos, setPos] = React.useState(null);
    React.useLayoutEffect(() => {
      if (phone) return;
      const t = ref.current && ref.current.parentElement.querySelector('.new-trigger');
      if (!t) return;
      const r = t.getBoundingClientRect();
      const w = Math.min(300, window.innerWidth - 32);
      /* v40: from the glass sidebar the menu opens beside it, level with the button */
      const side = t.closest('.sidebar');
      if (side) { const sr = side.getBoundingClientRect(); setPos({top: Math.max(12, Math.min(r.top, window.innerHeight - 440)), left: sr.right + 12, width: w}); return; }
      setPos({top: r.bottom + 8, left: Math.max(16, Math.min(r.left, window.innerWidth - w - 16)), width: w});
    }, [phone]);
    React.useLayoutEffect(() => {
      if (phone) return undefined;
      const away = e => { if (ref.current && !ref.current.contains(e.target) && !e.target.closest('.new-trigger')) onClose(); };
      const esc = e => { if (e.key === 'Escape') onClose(); };
      document.addEventListener('pointerdown', away);
      document.addEventListener('keydown', esc);
      return () => { document.removeEventListener('pointerdown', away); document.removeEventListener('keydown', esc); };
    }, [phone]);
    const run = fn => () => { onClose(); fn(); };
    const items = [
      {k: 'task', label: 'Task', sub: 'for you or anyone', icon: 'tasks', go: onTask},
      /* a private follow-up: how the founder reaches Prospects on the phone, where Accounts sits under More */
      {k: 'followup', label: 'Follow-up', sub: 'someone you are talking to', icon: 'bell', go: () => M.intend('#prospects', 'capture')},
      {k: 'post', label: 'Update or win', sub: 'on the feed', icon: 'feed', go: () => M.intend('#feed', 'post')},
      {k: 'kudos', label: 'Kudos', sub: 'thank someone', icon: 'scores', go: () => M.intend('#feed', 'kudos')},
      {k: 'leave', label: 'Leave request', sub: 'days off', icon: 'leave', go: () => M.nav('#leave')},
      {k: 'project', label: 'Project', sub: 'with a template', icon: 'projects', go: () => M.intend('#projects', 'project')},
      ctx.isFounder ? {k: 'pitch', label: 'Pitch', sub: 'into the pipeline', icon: 'pitches', go: () => M.intend('#pitches', 'pitch')} : null,
      {k: 'ask', label: 'Ask m360', sub: 'anything, or hand out work', mark: true, go: onAsk}
    ].filter(Boolean);
    /* the AI keeps its spark; the paper plane is the Chat tab's alone */
    const list = items.map(it => html`<button key=${it.k} type="button" role="menuitem" class="newmenu-item" onClick=${run(it.go)}>
        ${it.mark ? html`<span class="spark" aria-hidden="true" style=${{width: '20px', flex: 'none', textAlign: 'center', fontSize: '16px'}}>\u2726</span>` : html`<${M.icons[it.icon]}/>`}<span class="grow"><b>${it.label}</b><span>${it.sub}</span></span>
      </button>`);
    if (phone) return html`<${UI.Drawer} open=${true} onClose=${onClose} title="New">
      <div class="newmenu newmenu-sheet" ref=${ref} role="menu" aria-label="New">${list}</div>
    <//>`;
    return html`<div class="newmenu" ref=${ref} role="menu" aria-label="New"
      style=${pos || {visibility: 'hidden'}}>
      ${list}
    </div>`;
  }

  /* ---------- banners above the page: lock, alert, preview ---------- */
  /* everyone but the owner sees the lock line while settings.locked is on (v39: admins are locked too) */
  function LockBanner() {
    const ctx = M.useCtx();
    if (!ctx.locked || ctx.isOwner) return null;
    const note = String(ctx.settings.lockNote || '').trim();
    return html`<div class="lockbar" id="lock-banner" role="status">
      <span>m360 is locked for changes right now.${note ? ' ' + note : ''}</span>
    </div>`;
  }
  /* the founder's alert, shown to everyone until its date, dismissable for the day on this device */
  const alertKey = a => String(a.at || 0) + ':' + U.todayStr();
  function AlertBanner() {
    const ctx = M.useCtx();
    const [hidden, setHidden] = React.useState(() => M.prefs.get('alertSeen', ''));
    const a = ctx.settings.alert;
    if (!a || !String(a.text || '').trim()) return null;
    if (!a.until || a.until < U.todayStr()) return null;
    if (hidden === alertKey(a)) return null;
    const dismiss = () => { M.prefs.set('alertSeen', alertKey(a)); setHidden(alertKey(a)); };
    return html`<div class="alertbar" id="alert-banner" role="status">
      <span class="grow">${String(a.text).slice(0, 140)}</span>
      <button type="button" class="iconbtn" aria-label="Dismiss" title="Dismiss for today" onClick=${dismiss}><${M.icons.x}/></button>
    </div>`;
  }
  /* view as: a sticky ink bar while the founder previews the app as someone else */
  function PreviewBar() {
    const ctx = M.useCtx();
    if (!ctx.viewAs) return null;
    return html`<div class="previewbar" id="preview-bar" role="status">
      <${UI.Avatar} id=${ctx.viewAs} size=${26}/>
      <span class="grow">Viewing as <b><${UI.Name} id=${ctx.viewAs}/></b>. Preview only, nothing saves.</span>
      <button type="button" class="btn sm" onClick=${() => M.viewAs.set(null)}>Exit</button>
    </div>`;
  }
  M.parts.LockBanner = LockBanner;
  M.parts.AlertBanner = AlertBanner;
  M.parts.PreviewBar = PreviewBar;

  /* ---------- the shortcut sheet ---------- */
  function Keys({onClose}) {
    const mod = M.isMac ? '\u2318' : 'Ctrl';
    const rows = [[mod + ' K', 'Search or do anything'], ['/', 'Same, from anywhere'], ['n', 'New task'], ['i', 'Inbox'], ['f', 'Focus timer'], ['b', 'Slow breathing, five minutes'],
      ['g then h', 'Home'], ['g then w', 'Work'], ['g then a', 'Accounts'], ['g then v', 'Vibe'], ['g then m', 'Me'], ['g then c', 'Calendar'], ['g then r', 'Reviews'],
      ['Ctrl + Option, held', 'Talk to m360, let go to send'], ['Ctrl + Option + L', 'Conversation mode, on and off'], ['?', 'This sheet']];
    return html`<${UI.Drawer} open=${true} onClose=${onClose} title="Keyboard shortcuts">
      <div class="keys">${rows.map(r => html`<${React.Fragment} key=${r[0]}><span class="kbd">${r[0]}</span><span>${r[1]}</span><//>`)}</div>
    <//>`;
  }

  /* ---------- shell ---------- */
  /* v40: the v7 frame. A glass sidebar 12px from the edges (slim 80px icons, 248px with names, [ toggles,
     remembered per browser), the live mark at its top, the island at the top of the canvas for everything the
     OS says, and on a phone a glass capsule, a glass tab bar with a black lens and a full screen menu.
     Ids and classes the tests and the tour point at stay on the new parts (sidebar, side-item, side-tools,
     bellbtn, new-trigger, side-foot, topbar, tabbar, tab-item) */
  const LiveMark = props => (M.parts.LiveMark ? html`<${M.parts.LiveMark} ...${props}/>` : html`<${M.Mark} width="76px"/>`);
  const panelIcon = () => html`<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3.5" y="4.5" width="17" height="15" rx="3.5"/><path d="M9.5 4.5v15"/></svg>`;
  const SPARK = '✦';

  /* the full screen menu on a phone: every place, grouped, staggering in */
  function PhoneMenu({groups, active, badges, onGo, onClose}) {
    const [on, setOn] = React.useState(false);
    const gone = React.useRef(false);
    const close = React.useCallback(() => { if (gone.current) return; gone.current = true; setOn(false); setTimeout(onClose, M.reduced() ? 0 : 300); }, [onClose]);
    React.useEffect(() => {
      document.documentElement.classList.add('mn-open');
      const r = requestAnimationFrame(() => requestAnimationFrame(() => setOn(true)));
      const f = e => { if (e.key === 'Escape') { e.stopPropagation(); close(); } };
      window.addEventListener('keydown', f);
      return () => { cancelAnimationFrame(r); document.documentElement.classList.remove('mn-open'); window.removeEventListener('keydown', f); };
    }, []);
    let j = 0;
    return html`<div class=${'pmenu' + (on ? ' open' : '')} id="pmenu" role="dialog" aria-modal="true" aria-label="Menu">
      <div class="pmenu-top"><span class="pm"><${LiveMark}/></span>
        <button type="button" class="shx" aria-label="Close menu" onClick=${close}><${M.icons.x}/></button></div>
      <div class="pmenu-list">
        ${groups.map(g => html`<div key=${g.g || 'top'}>${g.g ? html`<div class="grp">${g.g}</div>` : null}
          ${g.items.map(k => { const s = SECTIONS[k]; const jj = j++; return html`<button key=${k} type="button" class=${'mi' + (active === k ? ' on' : '')} style=${{'--j': jj}}
            aria-current=${active === k ? 'page' : null} onClick=${() => { onGo(k); close(); }}>
            <${M.icons[s.icon]}/><span>${s.label}</span><${Badge} n=${badges[k] || 0}/></button>`; })}
        </div>`)}
      </div>
    </div>`;
  }

  M.Shell = function Shell() {
    const ctx = M.useCtx();
    const route = M.useRoute();
    const [moreOpen, setMoreOpen] = React.useState(false);
    const [askOpen, setAskOpen] = React.useState(false);
    const [newOpen, setNewOpen] = React.useState(false);
    const [newTask, setNewTask] = React.useState(false);
    const [palOpen, setPalOpen] = React.useState(false);
    const [inboxOpen, setInboxOpen] = React.useState(false);
    const [keysOpen, setKeysOpen] = React.useState(false);
    const [askInitial, setAskInitial] = React.useState('');
    const [sbx, setSbx] = React.useState(() => document.documentElement.classList.contains('sbx'));
    const sideRef = React.useRef(null), tabRef = React.useRef(null);
    const meProf = M.useProfiles(ctx.uid ? [ctx.uid] : [])[ctx.uid];
    const askAt = initial => { if (M.assistant && M.assistant.open) M.assistant.open(initial || ''); else { setAskInitial(initial || ''); setAskOpen(true); } };
    /* the Ask bar: the island grows into it when the island is here, the palette opens as before when not */
    const isl = M.island;
    const openBar = from => { if (isl) isl.cmd('', from); else setPalOpen(true); };
    const toggleBar = () => { if (isl) { if (isl.isCmd()) isl.close(); else isl.cmd(''); } else setPalOpen(x => !x); };
    React.useEffect(() => {
      if (!isl) return undefined;
      isl.onCmd(open => setPalOpen(!!open));
      return () => isl.onCmd(null);
    }, []);
    React.useEffect(() => { if (!palOpen && isl && isl.isCmd()) isl.close(); }, [palOpen]);
    React.useEffect(() => (M.chrome ? M.chrome.sb.on(setSbx) : undefined), []);

    React.useEffect(() => {
      if (!route.page) M.nav(ctx.isFounder ? '#hq' : '#home');
      else if (!ctx.isFounder && ['command', 'desk', 'hq', 'admin'].indexOf(route.page) >= 0) M.nav('#home');
    }, [route.page, ctx.isFounder]);

    /* keys: Cmd K and / for the Ask bar; single letters when nothing is focused ([ lives with the sidebar) */
    React.useEffect(() => {
      let g = 0;
      const typing = e => { const t = e.target; return t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.tagName === 'SELECT' || t.isContentEditable); };
      const on = e => {
        if ((e.metaKey || e.ctrlKey) && String(e.key).toLowerCase() === 'k') { e.preventDefault(); toggleBar(); return; }
        if (typing(e) || e.metaKey || e.ctrlKey || e.altKey) return;
        if (document.querySelector('.drawer, .pal, .breathe, .pmenu, [data-hotkeys]')) return;
        const k = e.key;
        if (g && Date.now() - g < 900) {
          g = 0;
          const to = {h: '#home', w: '#tasks', a: '#clients', v: '#feed', m: '#me', c: '#calendar', r: '#reviews', q: '#hq'}[k];
          if (to) { e.preventDefault(); M.nav(to); }
          return;
        }
        if (k === 'g') { g = Date.now(); return; }
        if (k === '/') { e.preventDefault(); openBar(); }
        else if (k === 'n') { e.preventDefault(); setNewTask(true); }
        else if (k === 'i') { e.preventDefault(); setInboxOpen(true); }
        else if (k === 'f') { e.preventDefault(); M.focus && M.focus.open(); }
        else if (k === 'b') { e.preventDefault(); M.breathe && M.breathe.open('slow'); }
        else if (k === '?') { e.preventDefault(); setKeysOpen(true); }
      };
      window.addEventListener('keydown', on);
      /* Ask m360 opens the buddy's pop-up at the dock; only its expand button opens the wide drawer */
      const open = e => askAt(e && e.detail && e.detail.initial);
      const wide = e => { setAskInitial((e && e.detail && e.detail.initial) || ''); setAskOpen(true); };
      const inbox = () => setInboxOpen(true);
      const keys = () => setKeysOpen(true);
      window.addEventListener('m360:ask', open); window.addEventListener('m360:askwide', wide); window.addEventListener('m360:inbox', inbox); window.addEventListener('m360:keys', keys);
      return () => { window.removeEventListener('keydown', on); window.removeEventListener('m360:ask', open); window.removeEventListener('m360:askwide', wide); window.removeEventListener('m360:inbox', inbox); window.removeEventListener('m360:keys', keys); };
    }, []);

    /* v39: an open inbox or search holds one history entry, so the phone's back button closes it and leaves the page as it is */
    const ovOpen = palOpen || inboxOpen;
    const ovRef = React.useRef(false), ovWas = React.useRef(false);
    ovRef.current = ovOpen;
    React.useEffect(() => {
      if (ovOpen) {
        ovWas.current = true;
        try { if (!(history.state && history.state.m360ov)) history.pushState({m360ov: 1}, '', location.href); } catch (e) { /* framed: no history */ }
        return undefined;
      }
      if (!ovWas.current) return undefined;
      ovWas.current = false;
      /* closed from inside: give the entry back, unless a row opened a page, which then sits after it */
      const t = setTimeout(() => { try { if (!ovRef.current && history.state && history.state.m360ov) history.back(); } catch (e) { /* fine */ } }, 120);
      return () => clearTimeout(t);
    }, [ovOpen]);
    React.useEffect(() => {
      const on = e => {
        const ours = !!(e.state && e.state.m360ov);
        if (ovRef.current && !ours) { setPalOpen(false); setInboxOpen(false); }
        else if (!ovRef.current && ours) { try { history.back(); } catch (err) { /* fine */ } }
      };
      window.addEventListener('popstate', on);
      return () => window.removeEventListener('popstate', on);
    }, []);

    const r = resolve(route.page, route.id, ctx.isFounder, ctx.isOwner);
    const sec = SECTIONS[r.s] || SECTIONS.home;
    const Page = M.pages[sec.page];
    const b = M.badges(ctx);
    /* the bell swings when a row that speaks arrives (silent rows only list), and never for the first full
       snapshot of what was already there: the count is taken once every collection has arrived */
    const loudReady = !!(M.inbox && M.inbox.loaded && M.inbox.loaded(ctx));
    const loud = loudReady && M.inbox.loud ? M.inbox.loud(ctx) : 0;
    const loudWas = React.useRef(null);
    React.useEffect(() => {
      if (!loudReady) return;
      const was = loudWas.current;
      loudWas.current = {uid: ctx.uid, n: loud};
      if (!was || was.uid !== ctx.uid) return;
      if (loud > was.n && M.fx && M.fx.ring) document.querySelectorAll('.bellbtn svg').forEach(el => M.fx.ring(el, {amplitude: 14, passes: 4, duration: 640}));
    }, [loud, loudReady, ctx.uid]);
    const go = k => { setMoreOpen(false); M.nav('#' + k); };

    /* the mark's mood follows the day: alert at four or more things waiting, calm at none */
    const waiting = ctx.isFounder ? (b.hq || 0) + (b.admin || 0) : (ctx.flags || []).filter(f => f.uid === ctx.uid && f.severity !== 'low').length;
    React.useEffect(() => { if (M.mark) M.mark.mood(waiting); }, [waiting]);
    /* the pill slides to the page, the lens to the tab; the mark nods when the page changes */
    const where = r.s + '/' + (r.t || '');
    const whereWas = React.useRef(where);
    React.useEffect(() => {
      if (M.chrome) { M.chrome.sb.mount(sideRef.current); M.chrome.sb.place(false); M.chrome.tb.place(tabRef.current); }
      if (whereWas.current !== where) {
        /* a new section opens at its top; a tab inside the same section keeps the place */
        if (whereWas.current.split('/')[0] !== r.s) window.scrollTo(0, 0);
        whereWas.current = where; if (M.mark && M.chrome && M.chrome.phone()) M.mark.nod();
      }
    });
    React.useEffect(() => {
      const f = () => { if (M.chrome) M.chrome.tb.place(tabRef.current, true); };
      window.addEventListener('resize', f);
      return () => window.removeEventListener('resize', f);
    }, []);

    const mainKeys = ['home', 'chat', 'work', 'accounts', 'workspace', 'base', 'radar', 'web', 'vibe', 'break', 'me'];
    const founderKeys = ctx.isFounder ? (ctx.isOwner ? ['hq', 'books', 'admin'] : ['hq', 'admin']) : [];
    let j = 0;
    const item = k => {
      const s = SECTIONS[k];
      const on = r.s === k;
      /* with names showing, the open section lists its tabs under it; slim, the page's own tab row does */
      const subs = on && sbx ? visibleTabs(ctx, k, b) : [];
      const jj = j++;
      return html`<${React.Fragment} key=${k}>
        <button type="button" data-k=${k} data-t=${s.label} style=${{'--j': jj}} aria-current=${on ? 'page' : null}
          class=${'nv side-item' + (on ? ' on active' : '') + (s.founder ? ' founder' : '')} title=${sbx && M.map ? M.map.blurbOf(k) : ''} onClick=${() => go(k)}>
          <${M.icons[s.icon]}/><span class="nl grow">${s.label}</span><${Badge} n=${b[k] || 0}/>
        </button>
        ${subs.length > 1 ? html`<div class="side-subs">
          ${subs.map(t => html`<button key=${t.k} type="button" class=${'side-sub' + (r.t === t.k ? ' active' : '')} title=${M.map ? M.map.blurbOf(k, t.k) : ''}
            onClick=${() => { setMoreOpen(false); M.nav('#' + t.route); }}>
            <span class="grow">${t.label}</span><${Badge} n=${b[t.k] || 0}/></button>`)}
        </div>` : null}
      <//>`;
    };
    const newMenu = where2 => newOpen === where2 ? html`<${NewMenu} onClose=${() => setNewOpen(false)}
      onTask=${() => setNewTask(true)} onAsk=${() => askAt('')}/>` : null;

    /* phone tabs: the four places each role opens most, then More and the round Ask button */
    const tabKeys = ctx.isFounder ? ['hq', 'home', 'work', 'chat'] : ['home', 'work', 'chat', 'vibe'];
    const allKeys = mainKeys.concat(founderKeys).concat(['map']);
    const moreKeys = allKeys.filter(k => tabKeys.indexOf(k) < 0);
    const moreBadge = moreKeys.reduce((n, k) => n + (b[k] || 0), 0);
    const moreOn = moreKeys.indexOf(r.s) >= 0;
    const ti = tabKeys.indexOf(r.s) >= 0 ? tabKeys.indexOf(r.s) : (moreOn ? tabKeys.length : -1);
    const menuGroups = [{g: '', items: mainKeys}].concat(founderKeys.length ? [{g: 'founder', items: founderKeys}] : []).concat([{g: 'help', items: ['map']}]);
    const meName = html`<${UI.Name} id=${ctx.uid} fallback="You"/>`;
    const meSub = [(ctx.member && ctx.member.empId) || '', (ctx.member && ctx.member.title) || ''].filter(Boolean).join(' · ');
    const mod = M.isMac ? '⌘K' : 'Ctrl K';

    return html`<div class=${'app' + (sbx ? ' is-sbx' : '')}>
      <aside class="sidebar" id="side" ref=${sideRef} aria-label="Pages">
        <button type="button" class="sbt" aria-label="m360, back to top" onClick=${() => { if (M.mark) M.mark.spin(); if (M.chrome) M.chrome.glide(0); else window.scrollTo(0, 0); }}><${LiveMark}/></button>
        <div class="new-wrap sb-new">
          <button type="button" class="nv sbt-new new-trigger" data-t="New" data-kb="n" aria-label="New" aria-expanded=${newOpen === 'side' ? 'true' : 'false'}
            onClick=${() => setNewOpen(x => x === 'side' ? false : 'side')}><span class="sb-plus"><${M.icons.plus}/></span><span class="nl">New</span></button>
          ${newMenu('side')}
        </div>
        <nav class="snav side-scroll"><span class="sp sp-h"></span><span class="sp sp-a"></span><i class="sb-here"></i>
          ${mainKeys.map(item)}
          ${founderKeys.length ? html`<div class="sgl side-group"><span>founder</span></div>` : null}
          ${founderKeys.map(item)}
          <div class="sgl side-group"><span>help</span></div>
          <button type="button" data-k="map" data-t="What's here" style=${{'--j': j++}} aria-current=${r.s === 'map' ? 'page' : null}
            class=${'nv side-item side-map' + (r.s === 'map' ? ' on active' : '')} id="side-map" title="Every place in m360, in one line each" onClick=${() => go('map')}>
            <${M.icons.map}/><span class="nl grow">What's here</span>
          </button>
        </nav>
        <div class="sfoot">
          ${M.parts.FocusPill ? html`<${M.parts.FocusPill}/>` : null}
          <div class="side-tools">
            <button type="button" class="nv iconbtn bellbtn" aria-label="Inbox" data-t="Inbox" data-kb="i" style=${{'--j': j++}} onClick=${() => setInboxOpen(true)}>
              <${M.icons.bell}/><span class="nl">Inbox</span><${Badge} n=${b.inbox || 0}/></button>
            <button type="button" class="nv iconbtn sb-ai" aria-label="Ask m360" data-t="m360 AI" style=${{'--j': j++}} onClick=${() => askAt('')}>
              <span class="sb-spark" aria-hidden="true">${SPARK}</span><span class="nl">m360 AI</span></button>
          </div>
          <button type="button" class="nv side-ask" id="sAsk" data-t="Ask m360" data-kb=${mod} style=${{'--j': j++}} onClick=${e => openBar(e.currentTarget)}>
            <${M.icons.search}/><span class="nl">Ask m360</span><kbd class="sb-kb">${mod}</kbd></button>
          <button type="button" class="nv" id="sTog" data-t=${sbx ? 'Collapse' : 'Expand'} data-kb="[" aria-expanded=${sbx ? 'true' : 'false'} style=${{'--j': j++}}
            onClick=${() => { if (M.chrome) M.chrome.sb.toggle(); }}>${panelIcon()}<span class="nl">${sbx ? 'Collapse' : 'Expand'}</span></button>
          <button type="button" class="nv side-foot" data-t=${(meProf && meProf.name) || 'Me'} style=${{'--j': j++}} onClick=${() => go('me')}>
            <${UI.Avatar} id=${ctx.uid} size=${24}/>
            <span class="nl"><span class="nm">${meName}</span><small class="ti num">${meSub}</small></span>
          </button>
        </div>
      </aside>

      <header class="topbar pbar lgx" id="pbar">
        <button type="button" class="pm" aria-label="m360, back to top" onClick=${() => { if (M.mark) M.mark.spin(); if (M.chrome) M.chrome.glide(0); else window.scrollTo(0, 0); }}><${LiveMark}/></button>
        <button type="button" class="where" aria-haspopup="dialog" aria-expanded=${moreOpen ? 'true' : 'false'} onClick=${() => setMoreOpen(true)}>
          <span>${sec.label}</span><${M.icons.chevD}/></button>
        ${M.parts.FocusPill ? html`<${M.parts.FocusPill} compact=${true}/>` : null}
        <div class="new-wrap">
          <button type="button" class="iconbtn new-trigger" aria-label="New" aria-expanded=${newOpen === 'top' ? 'true' : 'false'} onClick=${() => setNewOpen(x => x === 'top' ? false : 'top')}><${M.icons.plus}/></button>
          ${newMenu('top')}
        </div>
        <button type="button" class="iconbtn bellbtn" aria-label="Inbox" onClick=${() => setInboxOpen(true)}><${M.icons.bell}/><${Badge} n=${b.inbox || 0}/></button>
        <button type="button" class="mbtn" onClick=${() => go('me')} aria-label="Me"><${UI.Avatar} id=${ctx.uid} size=${32}/></button>
      </header>

      <main class="main" id="main">
        <div key=${r.s} class=${'content view' + (['work', 'accounts', 'hq'].indexOf(r.s) >= 0 ? ' wide' : '')}>
          <${PreviewBar}/>
          <${AlertBanner}/>
          <${LockBanner}/>
          ${Page ? html`<${Crash} key=${r.s + '/' + (r.t || '') + '/' + (r.id || '')}><${Page} tab=${r.t} id=${r.id}/><//>` : html`<${UI.Card} title="Loading"><${UI.Empty} text="One moment."/><//>`}
        </div>
      </main>

      ${M.parts.Buddy ? html`<${M.parts.Buddy}/>` : null}

      <nav class="tabbar" id="tabbar" ref=${tabRef} aria-label="Tabs" style=${{'--tn': tabKeys.length + 1, '--ti': Math.max(0, ti)}} data-mark=${ti >= 0 ? '1' : '0'}>
        <div class="tbg lgx"><span class="tb-lens" aria-hidden="true"></span>
          ${tabKeys.map(k => html`<button key=${k} type="button" aria-current=${r.s === k ? 'page' : null}
            class=${'tab-item ptab' + (r.s === k ? ' active' : '')} onClick=${() => { M.haptic.buzz('tick'); go(k); }}>
            <${M.icons[SECTIONS[k].icon]}/><span>${SECTIONS[k].label}</span><${Badge} n=${b[k] || 0}/>
          </button>`)}
          <button type="button" class=${'tab-item ptab' + (moreOn ? ' active' : '')} aria-haspopup="dialog" onClick=${() => { M.haptic.buzz('tick'); setMoreOpen(true); }}>
            <${M.icons.more}/><span>More</span>${moreBadge > 0 ? html`<i class="tdot" aria-label=${moreBadge + ' waiting'}></i>` : null}
          </button>
        </div>
        <button type="button" class="tb-ask lgx" aria-label="Ask m360" onClick=${e => openBar(e.currentTarget)}><${M.icons.search}/></button>
      </nav>

      ${moreOpen ? html`<${PhoneMenu} groups=${menuGroups} active=${r.s} badges=${b} onGo=${go} onClose=${() => setMoreOpen(false)}/>` : null}

      ${askOpen && M.parts.Ask ? html`<${M.parts.Ask} initial=${askInitial} onClose=${() => { setAskOpen(false); setAskInitial(''); }}/>` : null}
      ${palOpen && M.parts.Palette ? (isl && window.ReactDOM && window.ReactDOM.createPortal
        ? window.ReactDOM.createPortal(html`<${M.parts.Palette} island=${true} onClose=${() => setPalOpen(false)} onAsk=${q => askAt(q)}/>`, isl.slot())
        : html`<${M.parts.Palette} onClose=${() => setPalOpen(false)} onAsk=${q => askAt(q)}/>`) : null}
      ${inboxOpen && M.parts.Inbox ? html`<${M.parts.Inbox} onClose=${() => setInboxOpen(false)}/>` : null}
      ${keysOpen ? html`<${Keys} onClose=${() => setKeysOpen(false)}/>` : null}
      ${M.parts.FocusHost ? html`<${M.parts.FocusHost}/>` : null}
      ${M.parts.HolidayWatch ? html`<${M.parts.HolidayWatch}/>` : null}
      ${M.parts.FixHost ? html`<${M.parts.FixHost}/>` : null}
      ${M.parts.BooksWatch ? html`<${M.parts.BooksWatch}/>` : null}
      ${M.parts.CareWatch ? html`<${M.parts.CareWatch}/>` : null}
      ${M.parts.FollowWatch ? html`<${M.parts.FollowWatch}/>` : null}
      ${M.parts.BreatheHost ? html`<${M.parts.BreatheHost}/>` : null}
      ${M.parts.DayRateHost ? html`<${M.parts.DayRateHost}/>` : null}
      ${M.parts.ChatWatch ? html`<${M.parts.ChatWatch}/>` : null}
      ${M.parts.InboxWatch ? html`<${M.parts.InboxWatch}/>` : null}
      ${M.parts.PmWatch ? html`<${M.parts.PmWatch}/>` : null}
      ${M.parts.LiveWatch ? html`<${M.parts.LiveWatch}/>` : null}
      <${NewerBuild}/>
      ${M.parts.Notices ? html`<${M.parts.Notices}/>` : null}
      ${M.parts.MusicDock ? html`<${M.parts.MusicDock}/>` : null}
      ${newTask && M.parts.TaskDrawer ? html`<${M.parts.TaskDrawer} taskId=${null} defaults=${{owner: ctx.uid}} onClose=${() => setNewTask(false)}/>` : null}
      <${M.ToastHost}/>
    </div>`;
  };

  /* the server has a newer build than this tab: one line at the top, with a reload */
  function NewerBuild() {
    const [b, setB] = React.useState(window.M360_NEWER || '');
    React.useEffect(() => { const f = e => setB(e.detail || 'new'); window.addEventListener('m360:newer', f); return () => window.removeEventListener('m360:newer', f); }, []);
    if (!b) return null;
    return html`<div class="newer" id="newer-build" role="status">
      <span>A newer m360 is up (build ${b}). Reload to get it.</span>
      <button type="button" class="btn sm on-dark" onClick=${() => location.reload()}>Reload</button>
      <button type="button" class="iconbtn on-dark" aria-label="Later" onClick=${() => setB('')}><${M.icons.x}/></button>
    </div>`;
  }

  /* shared hero for section pages */
  /* phones: a short hero (no sub line, no map link; the More sheet carries the map) and one sideways
     row of stats, so the page starts above the fold */
  M.SectionHero = function SectionHero({color, micro, title, sub, children, right}) {
    const phone = M.usePhone();
    const mk = M.map && !phone && title !== 'What\'s in m360' ? M.map.keyFor(title) : '';
    /* v40: size and padding come from the CSS (48px title, flame full stop; 36px on a phone) */
    return html`<header class=${'hero section-hero' + (color === 'ink' ? ' ink' : '')}>
      <div class="row between" style=${{alignItems: 'flex-start'}}>
        <div class="grow">
          ${micro ? html`<${UI.Micro}>${micro}<//>` : null}
          <h1 class="hi">${title}</h1>
          ${sub && !phone ? html`<div class="sub" style=${{marginTop: '10px', maxWidth: '60ch'}}>${sub}</div>` : null}
          ${mk ? html`<button type="button" class="linky tiny hero-map" onClick=${() => M.nav('#map/' + mk)}>What's in ${title}</button>` : null}
        </div>
        ${right || null}
      </div>
      ${children ? html`<div style=${{marginTop: '16px'}}>${children}</div>` : null}
    </header>`;
  };
})();
