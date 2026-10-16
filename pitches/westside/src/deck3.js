(function(){
'use strict';
const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];
const deck=$('#deck'), screens=$$('.scr',deck), chrome=$('#chrome'), foot=$('#foot');
const reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
/* the pilot lives for this visit only, so a rehearsal never leaks into the meeting */
const store={get(k){try{return JSON.parse(sessionStorage.getItem(k))}catch(e){return null}},set(k,v){try{sessionStorage.setItem(k,JSON.stringify(v))}catch(e){}}};

/* ---------- fabric imagery ---------- */
function paintIn(root,force){$$('canvas[data-fab]',root).forEach(cv=>{try{Fabric.draw(cv,cv.dataset.fab,+cv.dataset.seed||1,undefined,force)}catch(e){}})}
let anim=null,animT=0;
function animate(scr){cancelAnimationFrame(anim);if(reduce)return;const cv=scr&&scr.querySelector('canvas[data-anim]');if(!cv)return;const t0=performance.now()-animT*1000;
  const step=now=>{animT=(now-t0)/1000;try{Fabric.draw(cv,cv.dataset.fab,+cv.dataset.seed||1,animT)}catch(e){return}anim=requestAnimationFrame(step)};anim=requestAnimationFrame(step)}

/* ---------- QR (decorative) ---------- */
$$('svg.qr-svg').forEach(svg=>{const r=Fabric.rng(+svg.dataset.seed||3),N=29,NS='http://www.w3.org/2000/svg';const add=(x,y,s,f)=>{const e=document.createElementNS(NS,'rect');e.setAttribute('x',x);e.setAttribute('y',y);e.setAttribute('width',s);e.setAttribute('height',s);e.style.fill=f;svg.appendChild(e)};const inF=(x,y)=>(x<8&&y<8)||(x>N-9&&y<8)||(x<8&&y>N-9);for(let y=0;y<N;y++)for(let x=0;x<N;x++){if(!inF(x,y)&&r()<.47)add(x,y,1,'var(--obj-ink)')}[[0,0],[N-7,0],[0,N-7]].forEach(([x,y])=>{add(x,y,7,'var(--obj-ink)');add(x+1,y+1,5,'var(--obj)');add(x+2,y+2,3,'var(--obj-ink)')})});

/* ---------- current screen: chrome tone, big mark, tabs, counter ---------- */
const total=screens.length;let cur=-1;
const cnt=$('#count'),ttl=$('#ttl'),tabs=$$('#tabs a');
const sc=$('#storeCount');let scAnim=null;
function countStores(){if(!sc)return;cancelAnimationFrame(scAnim);if(reduce){sc.textContent='311';return}const t0=performance.now(),D=1800;
  const step=now=>{const p=Math.min(1,(now-t0)/D),e=1-Math.pow(1-p,3);sc.textContent=String(Math.max(1,Math.round(1+e*310)));if(p<1)scAnim=requestAnimationFrame(step)};sc.textContent='1';scAnim=requestAnimationFrame(step)}
function setCurrent(i){if(i===cur||i<0)return;cur=i;if(!moving)want=i;const s=screens[i],d=s.classList.contains('tone-d');
  chrome.classList.toggle('on-d',d);foot.classList.toggle('on-d',d);chrome.classList.toggle('big',s.dataset.logo==='big');
  cnt.textContent=String(i+1).padStart(2,'0')+' / '+String(total).padStart(2,'0');ttl.textContent=s.dataset.title||'';
  tabs.forEach(a=>a.classList.toggle('on',a.dataset.chap===s.dataset.chap));
  const on=tabs.find(a=>a.classList.contains('on'));if(on){const p=on.parentElement;const l=on.offsetLeft-p.clientWidth/2+on.clientWidth/2;p.scrollTo({left:Math.max(0,l),behavior:reduce?'auto':'smooth'})}
  for(let k=Math.max(0,i-1);k<=Math.min(total-1,i+1);k++)paintIn(screens[k]);animate(s);
  $$('#menuList li a').forEach(a=>a.classList.toggle('on',a.getAttribute('href')==='#'+s.id));
  if(s.id==='scale')countStores()}
/* the screen crossing the middle of the viewport is current (works for tall stacked screens on phones too) */
if('IntersectionObserver' in window){const io=new IntersectionObserver(es=>{es.forEach(e=>{if(e.isIntersecting)setCurrent(screens.indexOf(e.target))})},{root:deck,rootMargin:'-50% 0px -50% 0px',threshold:0});screens.forEach(s=>io.observe(s))}

/* ---------- navigation: a press during a scroll counts from where we are heading, never from where we were ---------- */
let want=0,moving=false,mt;
function settle(){clearTimeout(mt);mt=setTimeout(()=>{moving=false;want=cur},180)}
deck.addEventListener('scroll',settle,{passive:true});
if('onscrollend' in window)deck.addEventListener('scrollend',()=>{clearTimeout(mt);moving=false;want=cur});
function go(i){i=Math.max(0,Math.min(total-1,i));want=i;moving=true;settle();deck.scrollTo({top:screens[i].offsetTop,behavior:reduce?'auto':'smooth'})}
function step(d){go((moving?want:cur)+d)}
$('#next').addEventListener('click',()=>step(1));$('#prev').addEventListener('click',()=>step(-1));

/* ---------- rails: buttons, a counter, arrow keys and the wheel move one card at a time ---------- */
const rails=$$('.hrail');
function railInfo(r){const kids=[...r.children];if(!kids.length)return{first:0,last:0,n:0,w:1};const w=kids[0].getBoundingClientRect().width+2;const vis=Math.max(1,Math.round(r.clientWidth/w));const first=Math.min(kids.length-1,Math.round(r.scrollLeft/w));return{first,last:Math.min(kids.length,first+vis),n:kids.length,w}}
function railNudge(r,d){const k=railInfo(r);const vis=Math.max(1,k.last-k.first);const max=Math.max(0,k.n-vis);r._t=Math.max(0,Math.min(max,(r._busy?r._t:k.first)+d));r._busy=true;clearTimeout(r._bt);r._bt=setTimeout(()=>{r._busy=false},450);r.scrollTo({left:r._t*k.w,behavior:reduce?'auto':'smooth'})}
function railAtEnd(r,d){if(r._busy){const k=railInfo(r);const vis=Math.max(1,k.last-k.first);return d>0?r._t>=k.n-vis:r._t<=0}return d>0?r.scrollLeft+r.clientWidth>=r.scrollWidth-4:r.scrollLeft<=4}
function railSync(r){const c=$(`.railctl[data-rail="${r.id}"]`);if(!c)return;const k=railInfo(r);$('.rc',c).textContent=(k.first+1)+'–'+k.last+' / '+k.n;const [p,n]=$$('button',c);p.disabled=railAtEnd(r,-1);n.disabled=railAtEnd(r,1)}
const ipGrid=$('#ipGrid');if(ipGrid)rails.push(ipGrid);
rails.forEach(r=>{r.addEventListener('scroll',()=>requestAnimationFrame(()=>railSync(r)),{passive:true});
  r.addEventListener('wheel',e=>{if(r===ipGrid&&!r.classList.contains('g2'))return;if(Math.abs(e.deltaY)<=Math.abs(e.deltaX))return;const d=e.deltaY>0?1:-1;if(railAtEnd(r,d))return;e.preventDefault();r.scrollLeft+=e.deltaY},{passive:false})});
$$('.railctl').forEach(c=>{const r=document.getElementById(c.dataset.rail);if(!r)return;$$('button[data-dir]',c).forEach(b=>b.addEventListener('click',()=>railNudge(r,+b.dataset.dir)))});
const syncRails=()=>rails.forEach(railSync);

/* ---------- keys ---------- */
function trap(e,el){const f=$$('a[href],button:not([disabled]),input,[tabindex]:not([tabindex="-1"])',el).filter(x=>x.offsetParent!==null);if(!f.length)return;const a=f[0],z=f[f.length-1];if(e.shiftKey&&document.activeElement===a){e.preventDefault();z.focus()}else if(!e.shiftKey&&document.activeElement===z){e.preventDefault();a.focus()}}
document.addEventListener('keydown',e=>{
  if(openEl){if(e.key==='Escape')close();else if(e.key==='Tab')trap(e,openEl);return}
  const tag=(e.target.tagName||'').toLowerCase();if(tag==='input'||tag==='textarea')return;if(tag==='button'&&(e.key===' '||e.key==='Enter')&&e.target.matches(':focus-visible'))return;
  if(e.key==='ArrowRight'||e.key==='ArrowLeft'){const d=e.key==='ArrowRight'?1:-1;const r=screens[cur]&&screens[cur].querySelector('.hrail, #ipGrid.g2');e.preventDefault();if(r&&!railAtEnd(r,d))railNudge(r,d);else step(d);return}
  if(['ArrowDown','PageDown',' '].includes(e.key)){e.preventDefault();step(1)}else if(['ArrowUp','PageUp'].includes(e.key)){e.preventDefault();step(-1)}else if(e.key==='Home'){e.preventDefault();go(0)}else if(e.key==='End'){e.preventDefault();go(total-1)}});

/* ---------- sheet + menu ---------- */
const scrim=$('#scrim'),sheet=$('#sheet'),sheetBody=$('#sheetBody'),menu=$('#menu');let openEl=null,lastFocus=null;
sheetBody.tabIndex=-1;
function open(el,opener){close(true);lastFocus=opener||document.activeElement;openEl=el;el.hidden=false;if(el===sheet){scrim.hidden=false;sheet.scrollTop=0;paintIn(el,true);sheetBody.focus({preventScroll:true})}else{paintIn(el,true);const f=el.querySelector('.x');if(f)f.focus()}}
function close(silent){if(!openEl)return;if(openEl===menu){q.value='';filter()}openEl.hidden=true;scrim.hidden=true;openEl=null;if(!silent&&lastFocus&&lastFocus.focus)lastFocus.focus()}
scrim.addEventListener('click',()=>close());$$('[data-close]').forEach(b=>b.addEventListener('click',()=>close()));
function openSheet(id,opener){const t=document.getElementById(id);if(!t)return;sheetBody.textContent='';sheetBody.appendChild(t.content.cloneNode(true));open(sheet,opener)}

/* ---------- toast ---------- */
const toast=$('#toast');let tt;function say(m){toast.textContent=m;toast.hidden=false;clearTimeout(tt);tt=setTimeout(()=>toast.hidden=true,1800)}

/* ---------- the pilot bag: pre-filled with the recommendation, editable, live ---------- */
const REC_DROP=['Pilot 01','@'+(document.querySelector('#account .pname')||{textContent:'@seenatwestside'}).textContent.replace(/^@/,''),'Five Functions','The Trial Room'];
const REC=['Pilot 01','@'+(document.querySelector('#account .pname')||{textContent:'@seenatwestside'}).textContent.replace(/^@/,''),'First Look','The Window','The Trial Room','Seen In','The Regulars'];
const bagList=$('#bagList'),bagEmpty=$('#bagEmpty');
function btnFor(n){return $$('[data-add]').find(b=>b.dataset.add===n)}
function metaFor(n){if(n==='Pilot 01')return mode()==='drop'?'Festive drop · one store · eight weeks':'Store launch · one opening · eight weeks';const b=btnFor(n);if(!b)return'';const s=b.closest('.scr');const g=s&&s.querySelector('[data-toggle] [aria-pressed="true"] b');return (g?g.textContent+' · ':'')+(b.dataset.meta||'')}
function mode(){const b=document.querySelector('#pilot [data-toggle] [aria-pressed="true"]');return b?b.dataset.val:'launch'}
function recSet(){return mode()==='drop'?REC_DROP:REC}
function recBag(){return recSet().filter(btnFor).map(n=>({n,rec:true}))}
let bag=store.get('ws-pilot');if(!Array.isArray(bag))bag=recBag();bag=bag.filter(x=>x&&x.n&&btnFor(x.n));
function renderBag(){$$('.pc').forEach(e=>e.textContent=bag.length);
  $$('[data-add]').forEach(b=>{const on=bag.some(x=>x.n===b.dataset.add);b.classList.toggle('added',on);b.textContent=on?'In the pilot · remove':'Add to pilot';b.setAttribute('aria-pressed',on?'true':'false')});
  if(bagList){bagList.textContent='';bag.forEach(x=>{const li=document.createElement('li');const a=document.createElement('b');a.textContent=x.n;if(x.rec){const r=document.createElement('span');r.className='rec';r.textContent='Recommended';a.appendChild(r)}
    const m=document.createElement('span');m.textContent=metaFor(x.n);const del=document.createElement('button');del.type='button';del.className='x2';del.setAttribute('aria-label','Remove '+x.n);del.textContent='×';del.addEventListener('click',()=>{bag=bag.filter(y=>y.n!==x.n);say('Removed · '+x.n);renderBag()});
    li.append(a,m,del);bagList.appendChild(li)});bagEmpty.hidden=bag.length>0}
  store.set('ws-pilot',bag)}
function toggleAdd(b){const n=b.dataset.add,i=bag.findIndex(x=>x.n===n);if(i>=0){bag.splice(i,1);say('Removed · '+n)}else{bag.push({n,rec:recSet().includes(n)});say('Added to pilot · '+n)}renderBag()}

/* ---------- one delegated click handler (works inside sheets too) ---------- */
document.addEventListener('click',e=>{
  const s=e.target.closest('[data-sheet]');if(s){e.preventDefault();openSheet(s.dataset.sheet,s);return}
  const ad=e.target.closest('[data-add]');if(ad){e.preventDefault();toggleAdd(ad);if(e.detail)ad.blur();return}
  const tb=e.target.closest('[data-toggle] button,[data-cols],.railctl button');if(tb&&e.detail)setTimeout(()=>tb.blur(),0);
  const rs=e.target.closest('[data-reset-bag]');if(rs){bag=recBag();renderBag();say('Recommended pilot restored');return}
  const c=e.target.closest('[data-copy]');if(c){const t=c.dataset.copy;const done=()=>{c.textContent='Copied';setTimeout(()=>c.textContent='Copy',1500)};
    try{navigator.clipboard.writeText(t).then(done,()=>{const r=document.createRange();r.selectNodeContents(c.previousElementSibling);const g=getSelection();g.removeAllRanges();g.addRange(r)})}catch(err){}return}
  const a=e.target.closest('a[href^="#"]');if(a){const id=a.getAttribute('href').slice(1);const i=screens.findIndex(x=>x.id===id);if(i<0)return;e.preventDefault();close(true);go(i)}});

/* ---------- index (menu) grouped by chapter, with search ---------- */
const ml=$('#menuList'),names={};$$('#tabs a').forEach(a=>names[a.dataset.chap]=a.textContent);let last='';
screens.forEach((s,i)=>{if(s.dataset.chap!==last){last=s.dataset.chap;const h=document.createElement('li');h.className='sec';h.textContent=names[last]||last;ml.appendChild(h)}
  const li=document.createElement('li');li.dataset.i=i;const a=document.createElement('a');a.href='#'+s.id;const n=document.createElement('span');n.textContent=String(i+1).padStart(2,'0');a.append(n,document.createTextNode(s.dataset.title||''));li.appendChild(a);ml.appendChild(li)});
const none=document.createElement('li');none.className='none';none.hidden=true;ml.appendChild(none);
const q=$('#menuQ');
function filter(){const v=q.value.trim().toLowerCase();const items=$$('li[data-i]',ml);
  const byTitle=items.filter(li=>li.textContent.toLowerCase().includes(v));
  const pool=v&&!byTitle.length?items.filter(li=>screens[+li.dataset.i].textContent.toLowerCase().includes(v)):byTitle;
  items.forEach(li=>li.hidden=!!v&&!pool.includes(li));$$('li.sec',ml).forEach(li=>li.hidden=!!v);
  none.hidden=!v||pool.length>0;none.textContent='No results for “'+q.value.trim()+'”'}
q.addEventListener('input',filter);
$('#menuOpen').addEventListener('click',e=>open(menu,e.currentTarget));
$('#searchOpen').addEventListener('click',e=>{open(menu,e.currentTarget);setTimeout(()=>q.focus(),30)});
$('#menuClose').addEventListener('click',()=>close());

/* ---------- toggles (pilot type) and listing density ---------- */
$$('[data-toggle]').forEach(g=>{const btns=$$('button',g);btns.forEach(b=>b.addEventListener('click',()=>{btns.forEach(x=>x.setAttribute('aria-pressed',x===b?'true':'false'));const scope=g.closest('.scr');$$('[data-show]',scope).forEach(el=>el.hidden=el.dataset.show!==b.dataset.val);paintIn(scope,true);if(scope.id==='pilot'&&bag.every(x=>x.rec))bag=recBag();renderBag()}))});
$$('[data-density]').forEach(g=>{const grid=g.closest('.scr').querySelector('.grid');$$('button[data-cols]',g).forEach(b=>b.addEventListener('click',()=>{$$('button[data-cols]',g).forEach(x=>x.setAttribute('aria-pressed',x===b?'true':'false'));grid.classList.remove('g1','g2','g4');grid.classList.add('g'+b.dataset.cols);grid.scrollTop=0;grid.scrollLeft=0;requestAnimationFrame(()=>paintIn(grid,true))}))});

/* ---------- boot ---------- */
renderBag();setCurrent(0);paintIn(screens[0],true);syncRails();
let idle=1;const rest=()=>{if(idle>=total)return;paintIn(screens[idle++]);(window.requestIdleCallback?requestIdleCallback(rest,{timeout:400}):setTimeout(rest,60))};setTimeout(rest,400);
let rt;window.addEventListener('resize',()=>{clearTimeout(rt);rt=setTimeout(()=>{screens.forEach(s=>paintIn(s));animate(screens[cur]);syncRails()},200)});
if(document.fonts&&document.fonts.ready)document.fonts.ready.then(()=>{paintIn(screens[cur]);syncRails()});
if(location.hash){const i=screens.findIndex(s=>'#'+s.id===location.hash);if(i>0)setTimeout(()=>deck.scrollTo({top:screens[i].offsetTop}),50)}
window.__deck={go,openSheet,screens};
})();
