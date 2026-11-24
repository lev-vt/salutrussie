(() => {
 const menu=document.getElementById('navLinks');
 const burger=document.getElementById('burger');
 if(burger && menu) burger.addEventListener('click',()=>{const open=menu.classList.toggle('open');burger.setAttribute('aria-expanded',String(open));});
 document.querySelectorAll('.sr-drop-button').forEach(b=>b.addEventListener('click',()=>{let li=b.closest('.has-drop');let next=li.classList.toggle('is-open');b.setAttribute('aria-expanded',String(next));}));
 document.addEventListener('keydown', event => {
  if (event.key !== 'Escape') return;
  const active = document.activeElement;
  const closingMobileMenu = menu?.classList.contains('open');
  const focusTarget = closingMobileMenu && menu.contains(active)
   ? burger
   : active?.closest('.nav-drop')?.closest('.has-drop')?.querySelector('.sr-drop-button');
  menu?.classList.remove('open');
  burger?.setAttribute('aria-expanded','false');
  document.querySelectorAll('.has-drop').forEach(x => {
   x.classList.remove('is-open');
   x.querySelector('.sr-drop-button')?.setAttribute('aria-expanded','false');
  });
  focusTarget?.focus();
 });
 document.querySelectorAll('.price-tab').forEach(tab=>tab.addEventListener('click',()=>{document.querySelectorAll('.price-tab').forEach(x=>x.classList.remove('active'));tab.classList.add('active');document.querySelectorAll('.price-panel').forEach(p=>p.classList.remove('active'));document.getElementById('panel-'+tab.dataset.tab)?.classList.add('active');}));
 // Search is a static index of actual site articles and published resources, no remote service.
 const q=document.getElementById('sr-search');
 if(q){
   let active='all';let format='all';let cards=[...document.querySelectorAll('.sr-result')];
   let normalize=x=>String(x||'').toLocaleLowerCase().normalize('NFKC');
   const update=()=>{let query=normalize(q.value.trim()),count=0;
     cards.forEach(card=>{let match=(!query||normalize(card.dataset.index).includes(query))&&(active==='all'||card.dataset.topic===active)&&(format==='all'||card.dataset.format===format);card.classList.toggle('sr-hidden',!match);if(match)count++});
     const msg=document.getElementById('sr-count');if(msg)msg.textContent=count+' '+(document.documentElement.lang==='fr'?'résultats':'материалов');
     document.getElementById('sr-empty')?.classList.toggle('sr-hidden',count!==0);
   };
   q.addEventListener('input',update);
   document.querySelectorAll('[data-topic-filter]').forEach(b=>b.addEventListener('click',()=>{active=b.dataset.topicFilter;document.querySelectorAll('[data-topic-filter]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));update()}));
   document.querySelectorAll('[data-format-filter]').forEach(b=>b.addEventListener('click',()=>{format=b.dataset.formatFilter;document.querySelectorAll('[data-format-filter]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));update()}));
   update();
 }
 document.querySelectorAll('.sr-copy-topic').forEach(b=>b.addEventListener('click',async()=>{
  const el=document.getElementById(b.dataset.copyTarget);
  if(!el)return;
  const text=el.textContent||'';
  let ok=false;
  try {await navigator.clipboard.writeText(text);ok=true;}catch(e){
   const t=document.createElement('textarea');t.value=text;t.style.position='fixed';t.style.opacity='0';document.body.append(t);t.select();
   try{ok=document.execCommand('copy')}catch(e){}t.remove();
  }
  const fr=document.documentElement.lang==='fr';
  b.textContent=ok?(fr?'Copié':'Скопировано'):(fr?'Sélectionnez et copiez le texte':'Выделите и скопируйте текст');
  if(!ok){const sel=window.getSelection();const range=document.createRange();range.selectNodeContents(el);sel.removeAllRanges();sel.addRange(range);}
  b.focus();
 }));
 document.querySelectorAll('[data-analytics-event]').forEach(el=>el.addEventListener('click',()=>{if(typeof window.ym==='function'&&window.SALUTRUSSIE_METRIKA_ID){window.ym(window.SALUTRUSSIE_METRIKA_ID,'reachGoal',el.dataset.analyticsEvent);}}));
})();

/* Shared V3.1 visual components. The original HTML remains the content source. */
(()=>{
const root=new URL('../',document.currentScript.src),lang=document.documentElement.lang,L=['ru','en','fr'].includes(lang)?lang:'ru';
const suffix=location.pathname.slice(root.pathname.length).replace(/^(ru|en|fr)\//,'').replace(/index\.html$/,'').replace(/^\/|\/$/g,'');
const url=(s='',l=L)=>new URL(l+'/'+(s?s.replace(/\/$/,'')+'/':''),root).href;
const d={
ru:{nav:['Услуги','Переезд в Россию','B2B','Статьи','О нас','Контакты'],consult:'Консультация',toc:'Содержание',help:'Нужна помощь в вашем случае?',side:'Оценим ситуацию, предложим индивидуальную стратегию и согласуем сопровождение.',intro:'Сначала индивидуальная стратегия — затем сопровождение по согласованному плану.',benefits:['Юридическая практика с 2005 года','Индивидуальная правовая стратегия','Согласованные этапы работы','Юридическое сопровождение'],fees:'Стоимость услуг',offer:'Оферта',privacy:'Политика обработки данных',pay:'Оплата',author:'Редакция SalutRussie',bio:'Юридическая практика основателя с 2005 года',search:'Поиск по статьям',empty:'Ничего не найдено',menu:'Меню',lang:'Язык'},
en:{nav:['Services','Move to Russia','B2B','Articles','About us','Contact'],consult:'Consultation',toc:'Contents',help:'Need legal advice?',side:'We assess your situation, develop an individual strategy and agree the scope of support.',intro:'First an individual legal strategy, then support according to the agreed plan.',benefits:['Legal practice since 2005','Individual legal strategy','Agreed scope and stages','Legal support'],fees:'Fees',offer:'Terms of service',privacy:'Privacy policy',pay:'Payment',author:'SalutRussie editorial team',bio:'Founder in legal practice since 2005',search:'Search articles',empty:'No articles found',menu:'Menu',lang:'Language'},
fr:{nav:['Services','S’installer en Russie','B2B','Articles','À propos','Contact'],consult:'Consultation',toc:'Sommaire',help:'Besoin d’un conseil ?',side:'Nous analysons votre situation, élaborons une stratégie individuelle et convenons de l’accompagnement.',intro:'D’abord une stratégie juridique individuelle, puis l’accompagnement selon le plan convenu.',benefits:['Pratique juridique depuis 2005','Stratégie juridique individuelle','Étapes et mission convenues','Accompagnement juridique'],fees:'Honoraires',offer:'Conditions de service',privacy:'Données personnelles',pay:'Paiement',author:'Rédaction SalutRussie',bio:'Fondateur juriste depuis 2005',search:'Rechercher un article',empty:'Aucun article trouvé',menu:'Menu',lang:'Langue'}
}[L];
const el=(tag,cls,txt)=>{const x=document.createElement(tag);if(cls)x.className=cls;if(txt)x.textContent=txt;return x};
const a=(href,txt,cls)=>{const x=el('a',cls,txt);x.href=href;return x};
const glyphs={
migration:'<rect x="5" y="3" width="22" height="26" rx="2"/><circle cx="16" cy="14" r="7"/><ellipse cx="16" cy="14" rx="3" ry="7"/><path d="M9 14h14M11 10h10M11 18h10M11 25h10"/>',
property:'<path d="M3 15 16 4l13 11M6 13v15h20V13M13 28v-9h6v9"/><path d="M22 5h4v6"/>',
business:'<rect x="3" y="10" width="26" height="18" rx="3"/><path d="M11 10V6h10v4M3 17h26M13 15v4h6v-4"/>',
invest:'<path d="M5 27h23M6 24V13h5v11m5 0V9h5v15m5 0V5h3v19M4 9l7-5 5 2 8-4"/>',
legal:'<path d="M16 3v25M8 29h16M4 8h24M16 5l-9 3m9-3 9 3M7 8 2 20h10L7 8Zm18 0-5 12h10L25 8ZM2 20a5 5 0 0 0 10 0m8 0a5 5 0 0 0 10 0"/>',
relocation:'<path d="M3 12 16 4l13 8M6 13v15h20V13M11 18h10M16 14v10M11 24h10"/>',
family:'<circle cx="16" cy="9" r="5"/><path d="M7 28v-3a9 9 0 0 1 18 0v3M6 5a4 4 0 1 0 0 8m20-8a4 4 0 1 1 0 8M2 25v-3a7 7 0 0 1 5-7m23 10v-3a7 7 0 0 0-5-7"/>',
calendar:'<rect x="4" y="6" width="24" height="23" rx="3"/><path d="M9 3v6m14-6v6M4 12h24M10 17h2m4 0h2m4 0h1m-13 5h2m4 0h2m4 0h1"/>',
document:'<path d="M7 3h13l6 6v20H7zM20 3v7h6M11 15h11M11 20h11M11 25h7"/>',
book:'<path d="M3 5h8a5 5 0 0 1 5 5v19a5 5 0 0 0-5-5H3zM29 5h-8a5 5 0 0 0-5 5v19a5 5 0 0 1 5-5h8z"/>',
plan:'<circle cx="16" cy="16" r="12"/><circle cx="16" cy="16" r="7"/><circle cx="16" cy="16" r="2"/><path d="m16 16 12-12M23 4h5v5"/>',
check:'<path d="M7 4h18v24H7zM12 10l2 2 4-4M12 18l2 2 4-4M20 11h2M20 19h2"/>',
people:'<circle cx="16" cy="9" r="5"/><path d="M5 29v-3a11 11 0 0 1 22 0v3M2 7l2-2m24 0 2 2"/>',
chat:'<path d="M4 5h24v18H14l-7 6v-6H4zM9 11h14M9 16h10"/>',
globe:'<circle cx="16" cy="16" r="12"/><ellipse cx="16" cy="16" rx="5" ry="12"/><path d="M4 16h24M6 10h20M6 22h20"/>',
payment:'<rect x="3" y="6" width="26" height="20" rx="3"/><path d="M3 12h26M7 20h8"/>',
shield:'<path d="M16 3 28 8v8c0 7-6 11-12 14C10 27 4 23 4 16V8zM10 16l4 4 8-8"/>',
};
function icon(k){const n=el('span','sr-line-icon');n.setAttribute('aria-hidden','true');n.innerHTML='<svg viewBox="0 0 32 32" width="38" height="38" fill="none" stroke="currentColor" stroke-width="1.65" stroke-linecap="round" stroke-linejoin="round" focusable="false">'+(glyphs[k]||glyphs.legal)+'</svg>';return n}
function kind(s){if(/family|students/.test(s))return'family';if(/recruitment|employers/.test(s))return'people';if(/foreign-companies/.test(s))return'globe';if(/for-business|business/.test(s))return'business';if(/real-estate|renting/.test(s))return'property';if(/investment|investor/.test(s))return'invest';if(/migration|residence|visa|rvp|vnzh/.test(s))return'migration';if(/relocation/.test(s))return'relocation';if(/knowledge/.test(s))return'book';if(/contacts|consultations/.test(s))return'chat';if(/privacy/.test(s))return'shield';if(/payment|pricing/.test(s))return'payment';if(/about/.test(s))return'people';return'legal'}
const header=document.querySelector('.sr-header'),menu=document.getElementById('navLinks'),burger=document.getElementById('burger');
if(header){
 const sync=()=>document.documentElement.style.setProperty('--sr-head',Math.ceil(header.getBoundingClientRect().height)+'px');sync();if('ResizeObserver'in window)new ResizeObserver(sync).observe(header);
 if(burger)burger.setAttribute('aria-label',d.menu);

 if(menu){
 const labels=L==='ru'?{decree:'Указ 702',all:'Все услуги',catalog:'Другие услуги',categories:['Недвижимость','Бизнес в России','Инвестиции','Юридическая помощь','Переезд и адаптация']}:
 L==='fr'?{decree:'Décret 702',all:'Tous les services',catalog:'Autres services',categories:['Immobilier','Affaires en Russie','Investissements','Assistance juridique','Installation']}:
 {decree:'Decree 702',all:'All services',catalog:'Other services',categories:['Property','Business in Russia','Investments','Legal assistance','Relocation']};
 const compact=matchMedia('(max-width:1279px)');
 const routes=['real-estate','business','investments','legal','relocation'];
 const item=(s,label,cls='')=>{const li=el('li',cls);const link=a(url(s),label);const active=s==='migration'?suffix==='migration'||(suffix.startsWith('migration/')&&!suffix.startsWith('migration/decree-702')):suffix===s||suffix.startsWith(s+'/');if(active){link.classList.add('active');if(suffix===s)link.setAttribute('aria-current','page')}li.append(link);return li};
 const service=el('li','has-drop sr-desktop-services');const button=el('button','sr-drop-button',d.nav[0]+' ▾');button.type='button';button.setAttribute('aria-expanded','false');button.setAttribute('aria-controls','service-drop');const drop=el('div','nav-drop');drop.id='service-drop';drop.append(a(url('services'),labels.all),...routes.map((s,i)=>a(url(s),labels.categories[i])));service.append(button,drop);
 const closeDrop=()=>{service.classList.remove('is-open');button.setAttribute('aria-expanded','false')};
 button.addEventListener('click',()=>{const on=service.classList.toggle('is-open');button.setAttribute('aria-expanded',String(on))});
 menu.replaceChildren(service,item('migration',d.nav[1]),item('migration/decree-702',labels.decree,'sr-nav-decree'),item('for-business',d.nav[2]),item('knowledge',d.nav[3]),item('about',d.nav[4]),item('contacts',d.nav[5]),item('consultations',d.consult,'sr-mobile-consult'));
 const secondary=el('li','sr-mobile-services');secondary.append(el('span','sr-mobile-services-title',labels.catalog));const grid=el('div','sr-mobile-services-grid');grid.append(a(url('services'),labels.all),...routes.map((s,i)=>a(url(s),labels.categories[i])));secondary.append(grid);menu.append(secondary);
 const nav=header.querySelector('.nav');const quick=el('div','sr-mobile-quick');const decree=a(url('migration/decree-702'),labels.decree,'sr-quick-decree');const consultation=a(url('consultations'),d.consult,'sr-quick-consult');consultation.dataset.analyticsEvent='consultation_click';if(suffix==='migration/decree-702')decree.setAttribute('aria-current','page');quick.append(decree,consultation);nav?.after(quick);
 header.classList.add('sr-nav-v33');
 const closeMenu=()=>{menu.classList.remove('open');burger?.setAttribute('aria-expanded','false');closeDrop()};
 document.addEventListener('click',e=>{if(!header.contains(e.target))closeMenu();else if(!service.contains(e.target))closeDrop()});
 menu.querySelectorAll('a').forEach(link=>link.addEventListener('click',closeMenu));
 const reorder=()=>{const featured=menu.querySelector('.sr-nav-decree');if(!featured)return;if(compact.matches){menu.prepend(featured)}else{const migration=menu.querySelector('a[href="'+url('migration')+'"]')?.closest('li');migration?.after(featured)}};
 reorder();
 compact.addEventListener?.('change',()=>{closeMenu();reorder()});
 burger?.setAttribute('aria-label',d.menu);
 }

 const brand=header.querySelector('.brand');if(brand&&!brand.querySelector('svg')){const mark=el('span');mark.innerHTML='<svg class="seal-mark" fill="none" viewBox="0 0 60 60" aria-hidden="true"><circle cx="30" cy="30" r="27" stroke="#A9803E" stroke-width="1.2"/><circle cx="30" cy="30" r="21" stroke="#A9803E" stroke-width=".7"/><text x="30" y="37" font-size="17" font-family="Georgia,serif" text-anchor="middle" fill="#F1ECDE">SR</text></svg>';brand.prepend(mark.firstChild)}
 const sw=header.querySelector('.lang-switch');if(sw){sw.setAttribute('aria-label',d.lang);sw.querySelectorAll('a[lang]').forEach(x=>{x.hreflang=x.lang})}
}
const foot=document.querySelector('.sr-footer .sr-width>div:last-child');if(foot){foot.querySelectorAll('a').forEach(x=>{if(/\/pricing\/?$/.test(new URL(x.href).pathname))x.textContent=d.fees;if(/\/privacy\/?$/.test(new URL(x.href).pathname))x.textContent=d.privacy});for(const [s,label] of [['offer',d.offer],['payment',d.pay]])if(![...foot.querySelectorAll('a')].some(x=>x.href===url(s)))foot.append(a(url(s),label))}
if(document.body.classList.contains('d702-design'))return;
const main=document.getElementById('main');if(!main)return;
const home=main.querySelector('.hero.v2-home'),hero=main.querySelector(':scope > .sr-top, :scope > .page-head'),article=suffix.startsWith('knowledge/articles/'),legal=['offer','privacy','payment','pricing'].includes(suffix),listing=suffix==='knowledge';

if(hero&&!article&&!legal&&!listing){const w=hero.querySelector(':scope > .sr-width, :scope > .wrap');if(w){const inner=el('div','sr-ui-hero-inner'),art=el('div','sr-ui-hero-art');art.setAttribute('aria-hidden','true');if(suffix==='migration'){const img=el('img');img.src=new URL('assets/decree702-stage2-arrival.jpg',root).href;img.alt='';img.width=680;img.height=720;img.fetchPriority='high';art.classList.add('sr-ui-hero-photo');art.append(img)}else art.append(icon(kind(suffix)));w.before(inner);inner.append(w,art)}}
const commercial=Boolean(home)||hero&&!article&&!legal&&!listing&&!['contacts','consultations','about'].includes(suffix);
let endHero=home||hero;
if(commercial&&endHero){const strip=el('div','sr-ui-benefits');strip.setAttribute('aria-label',L==='ru'?'Наш подход':L==='fr'?'Notre méthode':'Our approach');const group=suffix.split('/')[0];const groups={
migration:{ru:['Выбор основания для переезда','Визы, РВП и ВНЖ','Документы и сроки','Правовая защита'],en:['Choosing a residence route','Visas and residence permits','Documents and deadlines','Legal protection'],fr:['Choix du fondement de séjour','Visas et titres de séjour','Documents et délais','Protection juridique'],icons:['plan','migration','calendar','legal']},
'for-business':{ru:['Международный найм','Рабочие визы и разрешения','Миграционный аудит','Юридическая поддержка бизнеса'],en:['International hiring','Work visas and permits','Immigration compliance','Business legal support'],fr:['Recrutement international','Visas et permis de travail','Conformité migratoire','Conseil juridique aux entreprises'],icons:['people','migration','check','business']},
'real-estate':{ru:['Проверка объекта','Договор и полномочия','Безопасные расчёты','Сопровождение сделки'],en:['Property checks','Contracts and authority','Payment arrangements','Transaction support'],fr:['Vérification du bien','Contrats et pouvoirs','Modalités de règlement','Accompagnement de la transaction'],icons:['property','document','payment','legal']},
business:{ru:['Выбор структуры','Корпоративные документы','Налоги и договоры','Юридическое сопровождение'],en:['Choosing a structure','Corporate documentation','Tax and contracts','Legal support'],fr:['Choix de la structure','Documents sociaux','Fiscalité et contrats','Accompagnement juridique'],icons:['plan','document','check','business']},
investments:{ru:['Проверка проекта','Правовые риски','Условия инвестирования','Сопровождение сделки'],en:['Project review','Legal risks','Investment terms','Transaction support'],fr:['Analyse du projet','Risques juridiques','Conditions d’investissement','Accompagnement de la transaction'],icons:['invest','shield','document','legal']},
legal:{ru:['Анализ ситуации','Документы и доказательства','Правовая стратегия','Защита интересов'],en:['Case assessment','Documents and evidence','Legal strategy','Protection of your interests'],fr:['Analyse de la situation','Documents et preuves','Stratégie juridique','Défense de vos intérêts'],icons:['check','document','plan','legal']},
relocation:{ru:['План переезда','Административные процедуры','Жильё и обустройство','Адаптация в России'],en:['Relocation plan','Administrative procedures','Housing and practical needs','Settling in Russia'],fr:['Plan d’installation','Démarches administratives','Logement et besoins pratiques','Adaptation en Russie'],icons:['plan','document','property','family']}
};const set=groups[group];(set?.icons||['calendar','plan','check','legal']).forEach((k,i)=>{const b=el('div','sr-ui-benefit');b.append(icon(k),el('span','',set?.[L]?.[i]||d.benefits[i]));strip.append(b)});endHero.after(strip);endHero=strip;if(!home){const box=el('div','sr-ui-intro');const inner=el('div','sr-ui-intro-inner');inner.append(el('p','',d.intro),a(url('consultations'),d.consult+' →','btn btn-primary'));box.append(inner);endHero.after(box);endHero=box}}
main.querySelectorAll('.sr-card').forEach(card=>{const h=card.querySelector('h3');if(!h)return;let slot=card.querySelector('.sr-icon');if(slot&&/^\d+$/.test(slot.textContent.trim()))return;let k=card.matches('a[href]')?kind(new URL(card.href).pathname):'check';if(!slot){slot=el('span','sr-icon');card.prepend(slot)}slot.setAttribute('aria-hidden','true');slot.replaceChildren(icon(k))});
if(home){main.querySelectorAll('.sr-feature').forEach(f=>{const h=f.querySelector('h2');if(!h)return;const link=f.querySelector('a[href*="decree-702"]');const old=f.querySelector('.sr-star');if(link){const figure=el('figure');const img=el('img');img.src=new URL('assets/decree702-stage2-arrival.jpg',root).href;img.alt='';img.loading='lazy';figure.append(img);if(old)old.replaceWith(figure);else f.append(figure);f.classList.add('sr-ui-feature-grid')}else if(old){old.replaceChildren(icon('legal'))}})}
if(listing&&!main.querySelector('#sr-search')){const grid=main.querySelector('.sr-grid');if(grid){const label=el('label','',d.search);label.htmlFor='sr-local-search';const input=el('input','sr-input');input.type='search';input.id='sr-local-search';input.placeholder=d.search;const wrapper=el('div','sr-search-bar');wrapper.append(input);const status=el('p','sr-results');status.setAttribute('role','status');grid.before(label,wrapper,status);const cards=[...grid.children];input.addEventListener('input',()=>{const q=input.value.toLocaleLowerCase().trim();let n=0;cards.forEach(c=>{const yes=c.textContent.toLocaleLowerCase().includes(q);c.hidden=!yes;c.classList.toggle('sr-hidden',!yes);if(yes)n++});status.textContent=n?String(n):d.empty})}}
if(!endHero||home||listing||['contacts','consultations'].includes(suffix))return;
const siblings=[...main.children].slice([...main.children].indexOf(endHero)+1);
const headings=siblings.flatMap(s=>[...s.querySelectorAll('h2')]).filter(h=>!h.closest('.expert-process,.expert-toc,.sr-cta,.sr-card,.sr-about-node,.sr-founder-panel')&&h.textContent.trim());
if(headings.length<3)return;
const ids=new Set([...document.querySelectorAll('[id]')].map(n=>n.id));
headings.forEach((h,i)=>{if(!h.id){let id='sr-part-'+(i+1);while(ids.has(id))id+='a';h.id=id;ids.add(id)}});
const layout=el('div','sr-ui-layout'),side=el('aside','sr-ui-side'),body=el('div','sr-ui-body'),details=el('details'),summary=el('summary','',d.toc),nav=el('nav');nav.setAttribute('aria-label',d.toc);
const links=headings.map((h,i)=>{const link=a('#'+h.id,'');link.append(el('span','',String(i+1)),el('span','',h.textContent.trim()));nav.append(link);return link});
details.open=true;details.append(summary,nav);side.append(details);
if(!legal){const cta=el('div','sr-ui-side-cta');cta.append(el('strong','',d.help),el('p','',d.side),a(url('consultations'),d.consult+' →','btn'));side.append(cta)}
endHero.after(layout);layout.append(side,body);siblings.forEach(n=>body.append(n));
if(article){const target=body.querySelector('.expert-article')||body.querySelector('article');if(target&&!target.querySelector('.sr-ui-author')){const author=el('div','sr-ui-author'),image=el('img');image.src=new URL('assets/founder-lev-vtiurin-cutout-2026.webp',root).href;image.alt='';image.width=45;image.height=45;image.loading='lazy';const info=el('div');info.append(a(url('about'),d.author),el('small','',d.bio));author.append(image,info);target.prepend(author)}}
const mobile=matchMedia('(max-width:900px)'),setMode=()=>{details.open=!mobile.matches};setMode();mobile.addEventListener?.('change',setMode);
summary.addEventListener('click',e=>{if(!mobile.matches)e.preventDefault()});links.forEach(link=>link.addEventListener('click',()=>{if(mobile.matches)details.open=false}));document.addEventListener('click',e=>{if(mobile.matches&&details.open&&!side.contains(e.target))details.open=false});document.addEventListener('keydown',e=>{if(e.key==='Escape'&&mobile.matches&&details.open){details.open=false;summary.focus()}});
let pending=false;function update(){const offset=(header?.getBoundingClientRect().height||76)+(mobile.matches?90:35);let index=0;headings.forEach((h,i)=>{if(h.getBoundingClientRect().top<=offset)index=i});links.forEach((x,i)=>{if(i===index)x.setAttribute('aria-current','location');else x.removeAttribute('aria-current')});pending=false}addEventListener('scroll',()=>{if(!pending){pending=true;requestAnimationFrame(update)}},{passive:true});addEventListener('resize',update);update();
})();
