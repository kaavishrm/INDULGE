(function(){
'use strict';
const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];
const NS='http://www.w3.org/2000/svg';

/* ---------- seeded random ---------- */
function rng(seed){let a=(seed*2654435761)>>>0||1;return function(){a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}

/* ---------- textiles: procedural Indian and western fabrics, drawn as the page's imagery ---------- */
let NOISE=null;
function noiseTile(){if(NOISE)return NOISE;const c=document.createElement('canvas');c.width=c.height=160;const x=c.getContext('2d');const d=x.createImageData(160,160);const r=rng(99);for(let i=0;i<d.data.length;i+=4){const v=r()*255|0;d.data[i]=d.data[i+1]=d.data[i+2]=v;d.data[i+3]=r()*44|0}x.putImageData(d,0,0);NOISE=c;return c}
function grain(c,w,h,a){c.save();c.globalAlpha=a;c.fillStyle=c.createPattern(noiseTile(),'repeat');c.fillRect(0,0,w,h);c.restore()}
function sheen(c,w,h,s){const g=c.createLinearGradient(0,0,w,h);g.addColorStop(0,'rgba(255,255,255,'+(.1*s)+')');g.addColorStop(.45,'rgba(255,255,255,0)');g.addColorStop(1,'rgba(0,0,0,'+(.22*s)+')');c.fillStyle=g;c.fillRect(0,0,w,h);const v=c.createRadialGradient(w*.5,h*.45,Math.min(w,h)*.2,w*.5,h*.5,Math.max(w,h)*.75);v.addColorStop(0,'rgba(0,0,0,0)');v.addColorStop(1,'rgba(0,0,0,'+(.28*s)+')');c.fillStyle=v;c.fillRect(0,0,w,h)}
function folds(c,w,h,r,col){for(let i=0;i<5;i++){const x=r()*w,wd=w*(.15+r()*.25);c.save();c.translate(x,0);c.rotate(.18+(r()-.5)*.2);const g=c.createLinearGradient(-wd,0,wd,0);g.addColorStop(0,'rgba(0,0,0,0)');g.addColorStop(.5,col);g.addColorStop(1,'rgba(0,0,0,0)');c.fillStyle=g;c.fillRect(-wd,-h,wd*2,h*3);c.restore()}}
function blob(c,x,y,rad,col){const g=c.createRadialGradient(x,y,0,x,y,rad);g.addColorStop(0,col);g.addColorStop(1,'rgba(0,0,0,0)');c.fillStyle=g;c.fillRect(x-rad,y-rad,rad*2,rad*2)}
const TX={
  bandhani(c,w,h,r){c.fillStyle='#8c1a22';c.fillRect(0,0,w,h);for(let i=0;i<14;i++)blob(c,r()*w,r()*h,40+r()*120,'rgba(176,34,50,.35)');const s=10,P=8;for(let j=0,y=s/2;y<h+s;j++,y+=s*.86){for(let i=0,x=(j%2?s/2:0);x<w+s;i++,x+=s){const a=(i%P)-P/2,b=(j%P)-P/2,d=Math.abs(a)+Math.abs(b);if(!(d===0||d===2||d===4||(d===3&&r()<.15)))continue;const jx=x+(r()-.5)*1.2,jy=y+(r()-.5)*1.2,ye=d===0;c.fillStyle=ye?'#f0b43a':'#f3e2bf';c.beginPath();c.arc(jx,jy,ye?2.2:1.7,0,7);c.fill();c.fillStyle=ye?'#a3471b':'#8c1a22';c.beginPath();c.arc(jx,jy,.65,0,7);c.fill()}}sheen(c,w,h,1);grain(c,w,h,.5)},
  leheriya(c,w,h,r){const cols=['#e3a13a','#c4305f','#f2e5c9','#2f7a58','#e9b949','#c4305f','#f2e5c9','#d9622b'];c.fillStyle='#e3a13a';c.fillRect(0,0,w,h);c.save();c.translate(w/2,h/2);c.rotate(-Math.PI/5);const L=Math.hypot(w,h),bw=9;let k=0;c.globalAlpha=.92;for(let y=-L/2;y<L/2;y+=bw,k++){c.fillStyle=cols[k%cols.length];c.beginPath();c.moveTo(-L/2,y);for(let x=-L/2;x<=L/2;x+=8)c.lineTo(x,y+Math.sin(x/16+k*.7)*2.2);for(let x=L/2;x>=-L/2;x-=8)c.lineTo(x,y+bw+1+Math.sin(x/16+(k+1)*.7)*2.2);c.closePath();c.fill()}c.restore();c.globalAlpha=1;for(let i=0;i<30;i++)blob(c,r()*w,r()*h,10+r()*40,'rgba(255,240,220,.12)');sheen(c,w,h,.9);grain(c,w,h,.5)},
  chikankari(c,w,h,r){c.fillStyle='#f6f3ec';c.fillRect(0,0,w,h);c.strokeStyle='rgba(150,140,120,.5)';c.lineWidth=1;const st=70;for(let x=-st/2;x<w+st;x+=st){const ph=r()*6;c.beginPath();c.moveTo(x,0);for(let y=0;y<=h;y+=10)c.lineTo(x+Math.sin(y/28+ph)*12,y);c.stroke();for(let y=14;y<h;y+=34){const vx=x+Math.sin(y/28+ph)*12,sd=(Math.floor(y/34)%2)?1:-1;c.save();c.translate(vx,y);c.rotate(sd*.9);c.beginPath();c.ellipse(sd*9,0,9,3.6,0,0,7);c.stroke();c.restore();if(r()<.5){const fx=vx-sd*20,fy=y+10;for(let p=0;p<5;p++){const a=p/5*Math.PI*2;c.beginPath();c.ellipse(fx+Math.cos(a)*4,fy+Math.sin(a)*4,3.2,1.8,a,0,7);c.stroke()}c.fillStyle='rgba(170,160,140,.6)';c.beginPath();c.arc(fx,fy,1.2,0,7);c.fill()}}}c.fillStyle='rgba(160,150,130,.35)';const n=Math.min(1600,w*h/220);for(let i=0;i<n;i++){c.beginPath();c.arc(r()*w,r()*h,.7,0,7);c.fill()}const g=c.createLinearGradient(0,0,w,0);g.addColorStop(0,'rgba(0,0,0,.05)');g.addColorStop(.5,'rgba(255,255,255,0)');g.addColorStop(1,'rgba(0,0,0,.07)');c.fillStyle=g;c.fillRect(0,0,w,h);grain(c,w,h,.3)},
  blockprint(c,w,h,r){c.fillStyle='#efe6d2';c.fillRect(0,0,w,h);const s=46;for(let j=0,y=s/2;y<h+s;j++,y+=s*.8){for(let x=(j%2?s/2:0);x<w+s;x+=s){c.globalAlpha=.72+r()*.25;c.fillStyle='#2b3b6b';for(let p=0;p<6;p++){const a=p/6*Math.PI*2;c.beginPath();c.ellipse(x+Math.cos(a)*7,y+Math.sin(a)*7,6.5,3.2,a,0,7);c.fill()}c.fillStyle='#a8382c';c.beginPath();c.arc(x+1.2,y+.8,3.4,0,7);c.fill();const bx=x+s/2,by=y+s*.4;for(let q=0;q<4;q++){c.beginPath();c.arc(bx+Math.cos(q*Math.PI/2)*2.6,by+Math.sin(q*Math.PI/2)*2.6,1.3,0,7);c.fill()}}}c.globalAlpha=1;sheen(c,w,h,.45);grain(c,w,h,.55)},
  denim(c,w,h,r){c.fillStyle='#24385e';c.fillRect(0,0,w,h);c.lineWidth=1;let k=0;for(let x=-h;x<w;x+=2.4,k++){c.strokeStyle=k%2?'rgba(70,98,150,.55)':'rgba(15,26,48,.5)';c.beginPath();c.moveTo(x,0);c.lineTo(x+h,h);c.stroke()}for(let i=0;i<w/3;i++){const x=r()*w;c.strokeStyle='rgba(170,190,225,'+(.03+r()*.06)+')';c.beginPath();c.moveTo(x,0);c.lineTo(x+(r()-.5)*6,h);c.stroke()}blob(c,w*.55,h*.4,Math.max(w,h)*.6,'rgba(140,165,210,.22)');sheen(c,w,h,.8);grain(c,w,h,.6)},
  pinstripe(c,w,h,r){c.fillStyle='#1c2230';c.fillRect(0,0,w,h);c.strokeStyle='rgba(255,255,255,.03)';for(let x=-h;x<w;x+=2){c.beginPath();c.moveTo(x,0);c.lineTo(x+h*.5,h);c.stroke()}c.strokeStyle='rgba(225,225,230,.32)';c.lineWidth=1;for(let x=6;x<w;x+=14){c.beginPath();c.moveTo(x+.5,0);c.lineTo(x+.5,h);c.stroke()}folds(c,w,h,r,'rgba(255,255,255,.04)');sheen(c,w,h,1);grain(c,w,h,.6)},
  zari(c,w,h,r){c.fillStyle='#13392e';c.fillRect(0,0,w,h);folds(c,w,h,r,'rgba(120,200,160,.10)');const s=38;for(let j=0,y=s/2;y<h+s;j++,y+=s*.9){for(let x=(j%2?s/2:0);x<w+s;x+=s){const g=c.createLinearGradient(x-6,y-9,x+6,y+9);g.addColorStop(0,'#f3d98a');g.addColorStop(.5,'#c9a046');g.addColorStop(1,'#7f5f22');c.fillStyle=g;c.save();c.translate(x,y);c.rotate(.5);c.beginPath();c.moveTo(0,-9);c.bezierCurveTo(7,-6,7,6,0,9);c.bezierCurveTo(-5,6,-6,0,-2,-3);c.bezierCurveTo(1,-5,-1,-8,0,-9);c.fill();c.restore();c.fillStyle='rgba(230,200,120,.7)';c.beginPath();c.arc(x+s/2,y+s*.45,1.1,0,7);c.fill()}}const bh=Math.min(34,h*.12),gb=c.createLinearGradient(0,h-bh,0,h);gb.addColorStop(0,'#c9a046');gb.addColorStop(.5,'#f0d27e');gb.addColorStop(1,'#8a6a26');c.fillStyle=gb;c.fillRect(0,h-bh,w,bh);c.fillStyle='rgba(19,57,46,.85)';for(let x=0;x<w;x+=12){c.beginPath();c.moveTo(x,h-bh*.7);c.lineTo(x+6,h-bh*.3);c.lineTo(x+12,h-bh*.7);c.closePath();c.fill()}sheen(c,w,h,1);grain(c,w,h,.45)},
  rani(c,w,h,r){const g=c.createLinearGradient(0,0,w,h);g.addColorStop(0,'#c0226a');g.addColorStop(1,'#6e0d3b');c.fillStyle=g;c.fillRect(0,0,w,h);folds(c,w,h,r,'rgba(255,170,210,.22)');folds(c,w,h,r,'rgba(40,0,20,.25)');sheen(c,w,h,1);grain(c,w,h,.5)},
  marigold(c,w,h,r){c.fillStyle='#e98b12';c.fillRect(0,0,w,h);const cols=['#f6b827','#ef9d16','#d9680b','#f8c84a','#e57d0e'],n=Math.min(4200,w*h/90);for(let i=0;i<n;i++){const x=r()*w,y=r()*h,rad=2+r()*4.5;c.fillStyle=cols[(r()*cols.length)|0];c.beginPath();c.arc(x,y,rad,0,7);c.fill();c.fillStyle='rgba(120,50,0,.18)';c.beginPath();c.arc(x+rad*.3,y+rad*.3,rad*.5,0,7);c.fill()}sheen(c,w,h,.9);grain(c,w,h,.4)},
  linen(c,w,h,r){c.fillStyle='#d9cdb6';c.fillRect(0,0,w,h);for(let y=0;y<h;y+=2){c.fillStyle='rgba('+(r()<.5?'255,255,255':'90,70,40')+','+(.04+r()*.06)+')';c.fillRect(0,y,w,1)}for(let x=0;x<w;x+=2){c.fillStyle='rgba('+(r()<.5?'255,255,255':'90,70,40')+','+(.03+r()*.05)+')';c.fillRect(x,0,1,h)}c.fillStyle='rgba(120,95,60,.12)';for(let i=0;i<h/6;i++)c.fillRect(r()*w,r()*h,20+r()*60,1);sheen(c,w,h,.4);grain(c,w,h,.5)},
  ikat(c,w,h,r){c.fillStyle='#1d2a4f';c.fillRect(0,0,w,h);const cols=['#efe2c6','#b5462b','#d6a43c','#101622'];let y=4,k=0;c.globalAlpha=.85;while(y<h){const bh=22+r()*26,col=cols[k%cols.length],per=40+r()*30,amp=bh*.42,off=r()*per,cy=y+bh/2;c.fillStyle=col;for(let x=0;x<w;x++){const t=((x+off)%per)/per,tri=1-Math.abs(t*2-1),half=amp*tri+(r()-.5)*3;c.fillRect(x,cy-half+(r()-.5)*2.5,1,Math.max(0,half*2))}y+=bh+4+r()*6;k++}c.globalAlpha=1;sheen(c,w,h,.9);grain(c,w,h,.55)},
  ink(c,w,h,r){c.fillStyle='#101010';c.fillRect(0,0,w,h);folds(c,w,h,r,'rgba(255,255,255,.05)');sheen(c,w,h,1);grain(c,w,h,.8)}
};
const LIGHT_TX=new Set(['chikankari','blockprint','linen','marigold']);
function paint(cv,force){
  const w=cv.clientWidth,h=cv.clientHeight;if(!w||!h)return;
  if(!force&&cv._w===w&&cv._h===h)return;
  const dpr=Math.min(2,window.devicePixelRatio||1);cv.width=Math.round(w*dpr);cv.height=Math.round(h*dpr);
  const c=cv.getContext('2d');c.setTransform(dpr,0,0,dpr,0,0);
  const fn=TX[cv.dataset.tx]||TX.ink;try{fn(c,w,h,rng(+cv.dataset.seed||1))}catch(e){c.fillStyle='#222';c.fillRect(0,0,w,h)}
  cv._w=w;cv._h=h;
}
function paintAll(root){const list=$$('canvas[data-tx]',root||document);let i=0;(function step(){const end=Math.min(list.length,i+10);for(;i<end;i++)paint(list[i]);if(i<list.length)requestAnimationFrame(step)})()}

/* ---------- QR (decorative) ---------- */
function qr(svg){const r=rng(+svg.dataset.seed||3),N=29,ink='var(--paper-obj-ink)',bg='var(--paper-obj)';const add=(x,y,s,f)=>{const e=document.createElementNS(NS,'rect');e.setAttribute('x',x);e.setAttribute('y',y);e.setAttribute('width',s);e.setAttribute('height',s);e.style.fill=f;svg.appendChild(e)};const inF=(x,y)=>(x<8&&y<8)||(x>N-9&&y<8)||(x<8&&y>N-9);for(let y=0;y<N;y++)for(let x=0;x<N;x++){if(inF(x,y))continue;if(r()<.47)add(x,y,1,ink)}[[0,0],[N-7,0],[0,N-7]].forEach(([x,y])=>{add(x,y,7,ink);add(x+1,y+1,5,bg);add(x+2,y+2,3,ink)})}

/* ---------- the 12-month log ---------- */
const CATS={content:'Campaigns + content',creators:'Creators + collabs',experiential:'Experiential',stores:'Stores + growth',pr:'PR + business'};
const LOG=[
 {m:'Oct',y:'25',cat:'content',tx:'marigold',title:'Diwali 2025 runs on product pages',sum:'No festive film or campaign found. Shoppers\' haul videos carried the season.',body:'Diwali fell on 20–21 October. We found no Westside festive film or campaign. The season was carried by collection drops on westside.com and by shoppers\' own "Westside Diwali haul" videos on YouTube.',so:'The biggest shopping week of the year had no store-level hero moment. Seen at Westside gives each festive drop an address.',src:[['Campaign Asia, Diwali 2025 round-up','https://www.campaignasia.com/article/festive-campaigns-lighting-up-diwali-2025/505293']]},
 {m:'Nov',y:'25',cat:'content',tx:'zari',title:'Wedding season, told through blog guides',sum:'SEO style guides around KALA by E.T.A. bandhgalas. No wedding campaign found.',body:'Wedding-season content took the form of SEO guides, such as "Trending wedding outfits for men 2025", built around KALA by E.T.A. bandhgalas and pastel kurtas. We found no wedding-season campaign.',so:'This is the pilot window we recommend. India held 46 lakh weddings in six weeks last season, and no brand owns the wedding guest who shops locally.',src:[['Westside blog','https://www.westside.com/blogs/men-fashion/trending-wedding-outfits-for-men-2025-style-guide']]},
 {m:'Dec',y:'25',cat:'creators',tx:'rani',title:'Westside × W.i.S.H. "Glitz & Glam"',sum:'A sequinned party capsule with the I-pop girl group W.i.S.H.',body:'A sequinned, stage-styled party capsule with the Indian I-pop girl group W.i.S.H., sold in store and online. The launch date is approximate, inferred from page metadata.',so:'Music talent sells a party edit. Next time, route the fans to a store-hosted moment and count them.',src:[['Westside blog','https://www.westside.com/blogs/women-fashion/westside-wish-glam-collection-ipop-fashion-collaboration']]},
 {m:'Dec',y:'25',cat:'stores',tx:'pinstripe',title:'17 stores in a quarter; Kantar BrandZ No. 38',sum:'278 stores. Online +38%. Fashion LFL marginally negative.',body:'Q3 FY26 added 17 Westside stores, taking the total to 278, and online revenue grew 38%. Like-for-like growth in the fashion portfolio was marginally negative. Westside entered Kantar BrandZ India at No. 38, valued at US$3.3bn.',so:'Openings are carrying growth. Existing stores need more visits, which makes this a footfall problem.',src:[['Kantar BrandZ India 2025','https://www.kantar.com/inspiration/brands/indias-top-100-most-valuable-brands-worth-524-billion'],['ICICI Direct Q3 FY26 note','https://mailcontent.icicidirect.com/mailcontent/idirect_trent_q3fy26.pdf']]},
 {m:'Feb',y:'26',cat:'experiential',tx:'bandhani',title:'Wesness Fun Run, Mumbai: 3,500+ women',sum:'Tata Garden, 8 Feb. 4,000+ registrations. W.i.S.H. performed.',body:'On 8 February at Tata Garden, the run drew more than 4,000 registrations and over 3,500 women, with W.i.S.H. performing afterwards. Trent filed it with the exchanges as a press release. The Wesness community is about 25,000 across Mumbai, Pune, Hyderabad and Bengaluru.',so:'This is a real community. The next step is to end every run at a store with a Style Call, and count the visits.',src:[['BSE filing, 10 Feb 2026','https://www.bseindia.com/xml-data/corpfiling/AttachHis/f98f2ffa-597c-49f2-a9e7-835cfe0dc5a7.pdf']]},
 {m:'Feb',y:'26',cat:'content',tx:'linen',title:'Studiowest beauty drops',sum:'"Busy Me" sun care and "Disco Dust" glow range.',body:'Studiowest blog content introduced the "Busy Me" sun-care range and "Disco Dust", a seasonal glow range. These are dated by blog metadata only.',so:'Beauty raises basket size. Studiowest belongs in every Trial Room look.',src:[['Studiowest blog','https://westside.com/blogs/studiowest/latest-beauty-trends-right-now']]},
 {m:'Mar',y:'26',cat:'stores',tx:'pinstripe',title:'23 openings in a quarter: 300 stores',sum:'FY26 closes with 52 net additions. Online ~6% of sales.',body:'Q4 FY26 opened 23 Westside stores, ending the year at 300. Online grew 25% and stayed around 6% of sales. A Wesness promo run started from Westside Gachibowli on 1 March.',so:'About 40 openings in two quarters, with no visible launch playbook. First Look is built for this.',src:[['ICICI Direct Q4 FY26 note','https://dsijpub.s3.ap-south-1.amazonaws.com/productAttachment/BrokerRecommendation/idirect_trent_q4fy26.pdf']]},
 {m:'Apr',y:'26',cat:'creators',tx:'leheriya',title:'YNG: 4,000 creators, 6M views',sum:'Investor deck calls the creator community "self-sustaining".',body:'The Q4 FY26 investor deck calls YNG "self-sustaining": a 4,000-member community driving 6 million views, 50,000+ engagements and 12,000+ shares. YNG launched in September 2025, when four NIFT designers reworked Bombay Paisley and E.T.A.',so:'Strong reach, but reported in views. YNG creators become the first members of the Style Collective, with a store on every post.',src:[['Trent Q4 FY26 investor presentation','https://www.bseindia.com/xml-data/corpfiling/AttachHis/e08ff77d-7f68-46d2-acc6-ed26ee5c4974.pdf']]},
 {m:'Apr',y:'26',cat:'experiential',tx:'bandhani',title:'Runs that start at a store',sum:'Run2Quiz from New Commercial Street; Run2Zumba from D.N. Nagar.',body:'Wesness Run2Quiz set off from Westside New Commercial Street in Bengaluru on 12 April. Run2Zumba set off from Westside D.N. Nagar in Mumbai on 26 April. Entry cost ₹499.',so:'The store is already the start line. Make it the finish line too, with something to try on.',src:[['Wesness listings, indiarunning','https://www.indiarunning.com/wesness']]},
 {m:'Jun',y:'26',cat:'pr',tx:'ink',title:'AGM: about 50 stores a year, 700 long term',sum:'Noel Tata\'s last AGM as chairman. Q1 adds one net store.',body:'At the 23 June AGM, Trent guided to about 50 Westside openings a year and a long-term potential of around 700 stores. It was Noel Tata\'s last AGM as chairman. Q1 FY27 added one net store, taking the total to 301.',so:'Hundreds of future launches need a repeatable opening format that can be measured.',src:[['CNBC-TV18 (Nigel D\'Souza) on X','https://x.com/Nigel__DSouza/status/2069399419884380201']]},
 {m:'Jul',y:'26',cat:'pr',tx:'denim',title:'Bloomberg: "up to 100 stores a year"',sum:'CEO Shailina Parti on expansion. AI design suite: 400–500 designs a week.',body:'CEO Shailina Parti told Bloomberg that Westside plans as many as 100 openings a year, focused on Delhi, Bengaluru, Hyderabad and the north-east. An AI design suite lifts output from about 50 to 400–500 designs a week, with 30-day lead times targeted on trend pieces.',so:'Zara-like product speed is arriving. Marketing needs a weekly rhythm to match it: the Window.',src:[['Business Standard / Bloomberg, 20 Jul 2026','https://www.business-standard.com/companies/news/tata-s-fashion-brand-westside-plans-biggest-push-yet-with-100-annual-stores-126072000142_1.html']]},
 {m:'Sep',y:'26',cat:'stores',tx:'leheriya',title:'311 stores; Navratri "9 Days 9 Colours"',sum:'Q2 adds 10 stores. Trent revenue +23%.',body:'Q2 FY27 added 10 Westside stores, taking the total to 311. Trent revenue grew 23% even though the festivals fell in Q3. Westside.com ran a "9 Days 9 Colours" Navratri edit across Utsa and Vark.',so:'The festive edit exists online. Seen at Westside puts it on a rail people can visit this weekend.',src:[['ICICI Direct, Q2 FY27 update','https://www.icicidirect.com/research/equity/blog/trent-ltd-reported-its-business-update-for-q2fy27'],['Westside Navratri edit','https://www.westside.com/collections/navratri-colour-outfits-for-women']]},
 {m:'Oct',y:'26',cat:'experiential',tx:'ink',title:'FRONT ROW launches in Mumbai',sum:'150 culture-shapers, 80 looks, Tuxedo Street dance-offs, 30 New Faces.',body:'On 1 October Westside launched FRONT ROW, a fashion and culture platform. It brought together 150 culture-shapers and 80 Autumn/Winter/Festive looks, introduced the "Tuxedo Street" dance-off with three national challenges planned, and announced 30 New Faces. Umashan Naidoo, Chief Creative, Brand & Beauty, described it as more than a fashion show.',so:'A cultural platform with a cast. Host the dance-offs and the New Faces casting on shop floors, city by city.',src:[['Fashion Value Chain','https://fashionvaluechain.com/westside-unveils-front-row-fashion-platform/']]}
];
const rail=$('#rail'),chips=$('#chips');
function buildLog(){
  LOG.forEach((d,i)=>{
    const b=document.createElement('button');b.type='button';b.className='tl';b.dataset.i=i;b.dataset.cat=d.cat;
    const vis=document.createElement('div');vis.className='tl-vis';
    const cv=document.createElement('canvas');cv.dataset.tx=d.tx;cv.dataset.seed=100+i;vis.appendChild(cv);
    const mo=document.createElement('span');mo.className='tl-month';if(LIGHT_TX.has(d.tx)){mo.style.color='#141414';mo.style.textShadow='none'}
    mo.textContent=d.m;const sm=document.createElement('small');sm.textContent="'"+d.y;mo.appendChild(sm);vis.appendChild(mo);
    const body=document.createElement('div');body.className='tl-body';
    const c=document.createElement('span');c.className='cap';c.textContent=CATS[d.cat];
    const h=document.createElement('h3');h.textContent=d.title;
    const p=document.createElement('p');p.textContent=d.sum;
    const plus=document.createElement('span');plus.className='tl-plus';plus.textContent='+ Quick view';
    body.append(c,h,p,plus);b.append(vis,body);
    b.addEventListener('click',()=>openQuick(i,b));
    rail.appendChild(b);
  });
  const counts={all:LOG.length};LOG.forEach(d=>counts[d.cat]=(counts[d.cat]||0)+1);
  [['all','All']].concat(Object.entries(CATS)).forEach(([k,l],i)=>{
    const ch=document.createElement('button');ch.type='button';ch.className='chip';ch.dataset.f=k;ch.setAttribute('aria-pressed',i===0?'true':'false');
    ch.textContent=l;const n=document.createElement('span');n.className='n';n.textContent=counts[k]||0;ch.appendChild(n);
    ch.addEventListener('click',()=>{$$('.chip',chips).forEach(x=>x.setAttribute('aria-pressed',x===ch?'true':'false'));let shown=0;$$('.tl',rail).forEach(t=>{const on=k==='all'||t.dataset.cat===k;t.hidden=!on;if(on)shown++});$('#railCount').textContent=shown+(shown===1?' moment':' moments');rail.scrollTo({left:0,behavior:'smooth'});paintAll(rail)});
    chips.appendChild(ch);
  });
  $('#railPrev').addEventListener('click',()=>rail.scrollBy({left:-rail.clientWidth*.8,behavior:'smooth'}));
  $('#railNext').addEventListener('click',()=>rail.scrollBy({left:rail.clientWidth*.8,behavior:'smooth'}));
}

/* ---------- drawers / menu ---------- */
const scrim=$('#scrim');let lastFocus=null,openEl=null;
function openPanel(el,opener){closePanel(true);lastFocus=opener||document.activeElement;openEl=el;el.hidden=false;if(el.classList.contains('drawer'))scrim.hidden=false;document.body.style.overflow='hidden';paintAll(el);const f=el.querySelector('.x-btn');if(f)f.focus();if(opener&&opener.hasAttribute('aria-expanded'))opener.setAttribute('aria-expanded','true')}
function closePanel(silent){if(!openEl)return;openEl.hidden=true;scrim.hidden=true;document.body.style.overflow='';$$('[aria-expanded="true"]').forEach(b=>{if(b.id==='menuOpen'||b.id==='bagOpen')b.setAttribute('aria-expanded','false')});openEl=null;if(!silent&&lastFocus)lastFocus.focus()}
scrim.addEventListener('click',()=>closePanel());
document.addEventListener('keydown',e=>{if(e.key==='Escape')closePanel()});
$$('[data-close]').forEach(b=>b.addEventListener('click',()=>closePanel()));
function openQuick(i,opener){const d=LOG[i],q=$('#quick');$('#qKick').textContent=d.m+" '"+d.y+' · '+CATS[d.cat];$('#qTitle').textContent=d.title;$('#qBody').textContent=d.body;$('#qSo').textContent=d.so;const s=$('#qSrc');s.textContent='';d.src.forEach(([l,u],k)=>{if(k)s.appendChild(document.createTextNode(' · '));const a=document.createElement('a');a.href=u;a.target='_blank';a.rel='noreferrer';a.textContent=l;s.appendChild(a)});const cv=$('#qCanvas');cv.dataset.tx=d.tx;cv.dataset.seed=200+i;openPanel(q,opener);paint(cv,true)}
const SECTIONS=$$('#tabs a').map(a=>[a.getAttribute('href'),a.textContent]);
const ml=$('#menuList');SECTIONS.forEach(([h,t],i)=>{const li=document.createElement('li');const a=document.createElement('a');a.href=h;const n=document.createElement('span');n.textContent=String(i+1).padStart(2,'0');a.append(n,document.createTextNode(t));a.addEventListener('click',()=>closePanel(true));li.appendChild(a);ml.appendChild(li)});
$('#menuOpen').addEventListener('click',e=>openPanel($('#menu'),e.currentTarget));
$('#menuClose').addEventListener('click',()=>closePanel());
$('#bagOpen').addEventListener('click',e=>openPanel($('#bag'),e.currentTarget));
$('#addBag').addEventListener('click',e=>openPanel($('#bag'),e.currentTarget));
$('#askBag').addEventListener('click',e=>openPanel($('#bag'),e.currentTarget));
$$('[data-copy]').forEach(b=>b.addEventListener('click',()=>{const t=b.dataset.copy;const done=()=>{b.textContent='Copied';setTimeout(()=>b.textContent='Copy',1600)};try{navigator.clipboard.writeText(t).then(done,()=>sel(b))}catch(e){sel(b)}}));
function sel(b){const s=b.previousElementSibling;const r=document.createRange();r.selectNodeContents(s);const g=window.getSelection();g.removeAllRanges();g.addRange(r)}

/* ---------- journey ---------- */
const JR=[
 {k:'See',s:'A Reel with a store sticker',t:'See it, with an address.',a:'Trial Room Reels and Window reveals, each with a location sticker for the pilot store, served to people within about 5 km.',b:'Specificity. A named place and time turn "nice" into a plan, and people act on plans more than on intentions.',c:'Catchment reach · store-sticker taps'},
 {k:'Save',s:'One piece, three ways',t:'Know how to wear it.',a:'Carousels and Reels that show one hero piece across three occasions, styled by a local stylist.',b:'Fluency. When it is easy to picture wearing something, the most common reason not to buy goes away.',c:'Saves · shares'},
 {k:'Book',s:'A WhatsApp Style Call',t:'Say a small yes.',a:'A one-tap WhatsApp booking for a free 20-minute Style Call on a weekend evening, with reminders the day before and two hours before.',b:'Commitment. A small, specific yes makes the bigger action, the visit, far more likely.',c:'Bookings · show-up rate'},
 {k:'Walk in',s:'The Window + the Burst',t:'Come this week.',a:'The Friday Window drop and the 72-hour Burst give the store a reason to visit now rather than someday.',b:'Scarcity and novelty. This week\'s Window won\'t be there next week.',c:'Entries per trading day (people counter)'},
 {k:'Try on',s:'Trial room + stylist',t:'Feel it on.',a:'A stylist pulls three looks in your size, and the store team greets you within the first two minutes.',b:'Endowment. Once something is on you, giving it up feels like a loss.',c:'Stylist-assisted trials · dwell time'},
 {k:'Bill',s:'A tagged member bill',t:'Count it at the till.',a:'The drop code and stylist ID go on the WestStyleClub bill, with a small perk for using the code.',b:'Immediate reward. A benefit at the moment of purchase reinforces the visit.',c:'Bills ÷ entries · average bill · tagged bills'},
 {k:'Share',s:'The trial-room mirror',t:'Bring the next person in.',a:'A Seen at Westside mirror invites shoppers to post their look, tagged to the store.',b:'Social proof. People go where people like them are seen.',c:'Store-tagged posts · new followers by city'}
];
const jr=$('#jr');
function setJr(i){$$('.jr-step',jr).forEach((b,k)=>b.setAttribute('aria-pressed',k===i?'true':'false'));const d=JR[i];$('#jrK').textContent='Step '+(i+1)+' of 7 · '+d.k;$('#jrT').textContent=d.t;$('#jrA').textContent=d.a;$('#jrB').textContent=d.b;$('#jrC').textContent=d.c}
JR.forEach((d,i)=>{const b=document.createElement('button');b.type='button';b.className='jr-step';const c=document.createElement('span');c.className='cap';c.textContent=String(i+1).padStart(2,'0');const t=document.createElement('b');t.textContent=d.k;const s=document.createElement('small');s.textContent=d.s;b.append(c,t,s);b.addEventListener('click',()=>setJr(i));jr.appendChild(b)});
setJr(0);

/* ---------- pilot PDP ---------- */
const PILOT={
 drop:{name:'Festive drop · the wedding-guest edit',desc:'One existing Westside store becomes the address for the wedding season. Over two live weeks it gets two Window drops, a Trial Room series, Style Call evenings and a 72-hour Burst at the close. The result is read against the store\'s own baseline and three to five matched Westside stores.',
  spec:[['Store','One existing Westside in a metro mall with a people counter. We suggest Mumbai, for example D.N. Nagar, where Wesness already starts its runs.'],['Moment','Wedding season: Utsa, E.T.A. and KALA, and Studiowest, styled for the mehendi, the sangeet and the reception'],['Live','Two weeks from late November into early December, closing with the 72-hour Burst'],['Baseline','The last 12 weeks of daily entries, plus the same weeks last year. If the store has no counter history, choose the store-launch test'],['Comparator','3–5 matched Westside stores of the same city tier, size and mall type'],['Threshold','Agreed before launch. One store can reliably show a lift of about 10% or more']],
  gal:['The wedding-guest edit','Live in one store · late November','Existing Westside, metro mall','Utsa · E.T.A. · Studiowest'],
  note:'Festive drop: kickoff the week after Diwali (8 November), live through the wedding-season peak, and read before the end-of-season sale.'},
 launch:{name:'Store launch · First Look',desc:'The next new Westside opens to a neighbourhood that is already waiting. Twenty-one days of First Look before the doors open and an opening weekend of Style Calls, then a read of the first 30 days against Westside\'s recent openings.',
  spec:[['Store','The next Westside opening between January and March 2027. Westside needs about 39 more openings by March to meet its guidance of about 50 a year, so there will be candidates. A new city is best: Delhi NCR, Bengaluru, Hyderabad or the north-east, where Wesness and FRONT ROW are not yet present'],['Moment','21 days before opening, the opening weekend and days 1–30'],['Live','Pre-launch content and hoardings, then Style Calls on the opening weekend and the two weekends after'],['Baseline','First-30-day entry curves of recent comparable openings. Westside opened about 40 stores between October 2025 and March 2026'],['Comparator','The average of five recent openings, matched by size, city tier and mall type'],['Threshold','Agreed before launch, as a percentage above the matched-openings curve for days 1–30']],
  gal:['First Look','21 days before the doors open','The next new Westside','Founding members + opening weekend'],
  note:'Store launch: weeks 3–4 become the 21 days before opening plus the opening weekend, and the read runs to day 30.'}
};
function setPilot(k){const p=PILOT[k];$$('.size').forEach(b=>b.setAttribute('aria-pressed',b.dataset.pilot===k?'true':'false'));$('#pdpName').textContent=p.name;$('#pdpDesc').textContent=p.desc;const dl=$('#pdpSpec');dl.textContent='';p.spec.forEach(([a,b])=>{const dt=document.createElement('dt');dt.textContent=a;const dd=document.createElement('dd');dd.textContent=b;dl.append(dt,dd)});$('#galA').textContent=p.gal[0];$('#galAs').textContent=p.gal[1];$('#galB').textContent=p.gal[2];$('#galC').textContent=p.gal[3];$('#weeksNote').textContent=p.note;$('#bagItem').textContent=p.name}
$$('.size').forEach(b=>b.addEventListener('click',()=>setPilot(b.dataset.pilot)));
setPilot('drop');

/* ---------- chart: difference-in-differences slope ---------- */
const SER=[{n:'Pilot store',k:'pilot',a:640,b:760,c:'var(--pilot)'},{n:'Pilot without the drop (expected)',k:'exp',a:640,b:670,c:'var(--ink-3)',dash:true},{n:'Matched stores (average)',k:'comp',a:610,b:640,c:'var(--comp)'}];
function el(t,a,s){const e=document.createElementNS(NS,t);for(const k in a)e.setAttribute(k,a[k]);if(s)e.setAttribute('style',s);return e}
function chart(){
  const svg=$('#chart'),W=600,H=330,L=48,T=18,B=46,x0=L+56,x1=372,ymin=560,ymax=800;const y=v=>T+(ymax-v)/(ymax-ymin)*(H-T-B);
  [600,650,700,750,800].forEach(v=>{svg.appendChild(el('line',{x1:L,x2:x1+20,y1:y(v),y2:y(v)},'stroke:var(--grid);stroke-width:1'));const t=el('text',{x:L-8,y:y(v)+4,'text-anchor':'end'},'fill:var(--ink-3);font-size:11px;font-variant-numeric:tabular-nums');t.textContent=v;svg.appendChild(t)});
  const ax=el('line',{x1:L,x2:x1+20,y1:H-B,y2:H-B},'stroke:var(--hair);stroke-width:1');svg.appendChild(ax);
  [[x0,'Baseline','12-week average'],[x1,'Live window','2-week average']].forEach(([x,a,b])=>{const t=el('text',{x,y:H-B+18,'text-anchor':'middle'},'fill:var(--ink-2);font-size:11.5px;font-weight:500');t.textContent=a;svg.appendChild(t);const s=el('text',{x,y:H-B+33,'text-anchor':'middle'},'fill:var(--ink-3);font-size:10.5px');s.textContent=b;svg.appendChild(s)});
  const yl=el('text',{x:L-8,y:T-6,'text-anchor':'end'},'fill:var(--ink-3);font-size:10.5px');yl.textContent='entries/day';svg.appendChild(yl);
  const cross=el('line',{x1:0,x2:0,y1:T,y2:H-B},'stroke:var(--ink-3);stroke-width:1;opacity:0');svg.appendChild(cross);
  SER.forEach(s=>{svg.appendChild(el('line',{x1:x0,y1:y(s.a),x2:x1,y2:y(s.b),'stroke-linecap':'round'},'stroke:'+s.c+';stroke-width:2;'+(s.dash?'stroke-dasharray:5 5':'')));[[x0,s.a],[x1,s.b]].forEach(([x,v])=>{if(s.dash&&x===x0)return;svg.appendChild(el('circle',{cx:x,cy:y(v),r:5},'fill:'+s.c+';stroke:var(--paper);stroke-width:2'))})});
  const lab=[[760,'760','Pilot'],[670,'670','Expected'],[640,'640','Matched']];
  lab.forEach(([v,a,b])=>{const t=el('text',{x:x1+14,y:y(v)+4},'fill:var(--ink);font-size:12px;font-weight:600;font-variant-numeric:tabular-nums');t.textContent=a;const s=el('tspan',{dx:6},'fill:var(--ink-3);font-weight:400;font-size:11px');s.textContent=b;t.appendChild(s);svg.appendChild(t)});
  const bx=x1+132;svg.appendChild(el('path',{d:'M'+(bx-6)+' '+y(760)+'H'+bx+'V'+y(670)+'H'+(bx-6),fill:'none'},'stroke:var(--ink);stroke-width:1'));
  const lt=el('text',{x:bx+8,y:(y(760)+y(670))/2},'fill:var(--ink);font-size:15px;font-weight:600');lt.textContent='+90';svg.appendChild(lt);
  const lt2=el('text',{x:bx+8,y:(y(760)+y(670))/2+15},'fill:var(--ink-2);font-size:10.5px');lt2.textContent='a day · +13%';svg.appendChild(lt2);
  const tip=$('#tip'),box=$('#chartBox');
  function show(x,label){cross.setAttribute('x1',x);cross.setAttribute('x2',x);cross.style.opacity=.5;tip.textContent='';const h=document.createElement('div');h.className='h';h.textContent=label;tip.appendChild(h);SER.forEach(s=>{const v=x===x0?s.a:s.b;const r=document.createElement('div');r.className='r';const i=document.createElement('i');i.style.background=s.c;if(s.dash){i.style.background='none';i.style.borderTop='2px dashed '+s.c}const b=document.createElement('b');b.textContent=v;const n=document.createElement('span');n.textContent=s.n;r.append(i,b,n);tip.appendChild(r)});tip.hidden=false;const sc=box.clientWidth/W;let left=x*sc+14;if(left+190>box.clientWidth)left=x*sc-200;tip.style.left=Math.max(0,left)+'px';tip.style.top='8px'}
  function hide(){cross.style.opacity=0;tip.hidden=true}
  [[x0,'Baseline · 12-week average'],[x1,'Live window · 2-week average']].forEach(([x,l])=>{const r=el('rect',{x:x-70,y:T,width:140,height:H-T-B,tabindex:0,'aria-label':l},'fill:transparent;cursor:crosshair;outline:none');r.addEventListener('pointerenter',()=>show(x,l));r.addEventListener('pointerleave',hide);r.addEventListener('focus',()=>show(x,l));r.addEventListener('blur',hide);svg.appendChild(r)});
  const tb=$('#dataTbl tbody');SER.forEach(s=>{const tr=document.createElement('tr');[s.n,s.a,s.b,'+'+(s.b-s.a)].forEach(v=>{const td=document.createElement('td');td.textContent=v;tr.appendChild(td)});tb.appendChild(tr)});
  const tr=document.createElement('tr');['Lift (pilot − expected, live)','','','+90'].forEach(v=>{const td=document.createElement('td');td.textContent=v;td.style.fontWeight='600';tr.appendChild(td)});tb.appendChild(tr);
  $('#tblToggle').addEventListener('click',e=>{const t=$('#dataTbl');t.hidden=!t.hidden;e.currentTarget.setAttribute('aria-expanded',String(!t.hidden));e.currentTarget.textContent=t.hidden?'Show table':'Hide table'});
}
chart();

/* ---------- 12-month calendar ---------- */
const MONTHS=['Nov 26','Dec','Jan 27','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct'];
const LANES=[
 ['India moments',['Diwali · wedding season','Weddings · party season','End-of-season sale','Valentine\'s · weddings','Holi · spring-summer','Summer weddings','Summer holidays','End-of-season sale · monsoon','Back to college','Independence Day · Rakhi','Ganeshotsav · Onam','Navratri · Dussehra'],[]],
 ['Westside platforms',['','Party edit (W.i.S.H. precedent)','','Wesness Fun Run, Mumbai','','Wesness city runs','','Wesness city runs','','','YNG, year two','FRONT ROW, year two'],[]],
 ['Seen at Westside',['Pilot 01 live: wedding-guest edit','Read · scale decision','10-store Mumbai cluster','Wesness runs end in Style Calls','Weekly Windows: spring-summer','First Look for new openings','Trial Room: summer weddings','Second city cluster','Campus Style Collective','Sibling Style Calls for Rakhi','FRONT ROW casting in stores','Festive drop in every cluster store'],[0,5,11]]
];
const cg=$('#calGrid');const hd=document.createElement('div');hd.className='h';cg.appendChild(hd);MONTHS.forEach(m=>{const d=document.createElement('div');d.className='h';d.textContent=m;cg.appendChild(d)});
LANES.forEach(([lane,cells,acc])=>{const l=document.createElement('div');l.className='lane';l.textContent=lane;cg.appendChild(l);cells.forEach((t,i)=>{const d=document.createElement('div');if(t){d.className='ev'+(acc.includes(i)?' a':'');const s=document.createElement('span');s.textContent=t;d.appendChild(s)}cg.appendChild(d)})});

/* ---------- chrome: bar border + tab scrollspy ---------- */
const bar=$('#bar');const onScroll=()=>bar.classList.toggle('is-scrolled',window.scrollY>8);window.addEventListener('scroll',onScroll,{passive:true});onScroll();
const tabs=$$('#tabs a'),tabsIn=$('#tabs');
if('IntersectionObserver' in window){const io=new IntersectionObserver(es=>{es.forEach(e=>{if(e.isIntersecting){const id='#'+e.target.id;tabs.forEach(a=>{const on=a.getAttribute('href')===id;a.classList.toggle('on',on);if(on){const l=a.offsetLeft-tabsIn.clientWidth/2+a.clientWidth/2;tabsIn.scrollTo({left:l,behavior:'smooth'})}})}})},{rootMargin:'-40% 0px -55% 0px'});tabs.forEach(a=>{const s=$(a.getAttribute('href'));if(s)io.observe(s)})}

/* ---------- boot ---------- */
buildLog();
$$('.qr-svg').forEach(qr);
paintAll();
let rt;window.addEventListener('resize',()=>{clearTimeout(rt);rt=setTimeout(()=>paintAll(),180)});
if(document.fonts&&document.fonts.ready)document.fonts.ready.then(()=>paintAll());
})();
