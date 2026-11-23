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
(()=>{const root=new URL('../',document.currentScript.src);const lang=document.documentElement.lang;const L=['ru','en','fr'].includes(lang)?lang:'ru';const suffix=location.pathname.slice(root.pathname.length).replace(/^(ru|en|fr)\//,'').replace(/index\.html$/,'');const tr={ru:{lang:'Язык',price:'Стоимость услуг',offer:'Оферта',privacy:'Персональные данные',pay:'Оплата',toc:'Содержание',help:'Нужна помощь?',consult:'Консультация →',author:'Редакция SalutRussie',bio:'Юридическая практика основателя с 2005 года',note:'Материал общего характера. Перед применением проверьте обстоятельства вашего дела и действующую редакцию закона.'},en:{lang:'Language',price:'Fees',offer:'Terms of service',privacy:'Privacy policy',pay:'Payment',toc:'Contents',help:'Need legal advice?',consult:'Consultation →',author:'SalutRussie editorial team',bio:'Founder in legal practice since 2005',note:'General information only. Verify the current law and your individual circumstances before relying on it.'},fr:{lang:'Langue',price:'Honoraires',offer:'Conditions de service',privacy:'Données personnelles',pay:'Paiement',toc:'Sommaire',help:'Besoin d’un conseil ?',consult:'Consultation →',author:'Rédaction SalutRussie',bio:'Fondateur juriste depuis 2005',note:'Informations générales. Vérifiez le droit applicable et votre situation avant toute démarche.'}}[L];const url=(l,s)=>new URL(l+'/'+s,root).href;const sw=document.querySelector('.lang-switch');if(sw){sw.setAttribute('aria-label',tr.lang);sw.replaceChildren(...['ru','en','fr'].map(l=>{const a=document.createElement('a');a.href=url(l,suffix.replace('migration/decree-702-design/','migration/decree-702/'));a.lang=l;a.textContent=l.toUpperCase();if(l===L){a.className='active';a.setAttribute('aria-current','page')}return a}))}const foot=document.querySelector('.sr-footer .sr-width>div:last-child');if(foot){foot.querySelectorAll('a').forEach(a=>{if(/\/pricing\/?$/.test(new URL(a.href).pathname))a.textContent=tr.price;if(/\/privacy\/?$/.test(new URL(a.href).pathname))a.textContent=tr.privacy});for(const [s,title] of [['offer/',tr.offer],['payment/',tr.pay]]){if(![...foot.querySelectorAll('a')].some(a=>a.href===url(L,s))){const a=document.createElement('a');a.href=url(L,s);a.textContent=title;foot.append(a)}}}if(!suffix.startsWith('knowledge/articles/'))return;const article=document.querySelector('main article');if(!article||article.parentElement.classList.contains('v3-page'))return;const headings=[...article.querySelectorAll('h2')].filter(h=>!h.closest('.expert-process,.expert-toc'));if(headings.length<3)return;headings.forEach((h,i)=>{if(!h.id)h.id='article-part-'+(i+1)});const grid=document.createElement('div');grid.className='v3-page';const side=document.createElement('aside');side.className='v3-side';const details=document.createElement('details');details.open=true;const summary=document.createElement('summary');summary.textContent=tr.toc;details.append(summary);const nav=document.createElement('nav');nav.setAttribute('aria-label',tr.toc);headings.forEach(h=>{const a=document.createElement('a');a.href='#'+h.id;a.textContent=h.textContent;nav.append(a)});details.append(nav);side.append(details);const box=document.createElement('div');box.className='v3-side-cta';const s=document.createElement('strong');s.textContent=tr.help;const a=document.createElement('a');a.className='btn';a.href=url(L,'consultations/');a.textContent=tr.consult;box.append(s,a);side.append(box);article.before(grid);grid.append(side,article);const body=article.querySelector('.expert-article')||article;const author=document.createElement('div');author.className='v3-author';const img=document.createElement('img');img.src=new URL('assets/founder-lev-vtiurin-cutout-2026.webp',root).href;img.alt='';const txt=document.createElement('div');const al=document.createElement('a');al.href=url(L,'about/');al.textContent=tr.author;const sm=document.createElement('small');sm.textContent=tr.bio;txt.append(al,sm);author.append(img,txt);body.prepend(author);const mq=matchMedia('(max-width:900px)');const resize=()=>details.open=!mq.matches;resize();mq.addEventListener?.('change',resize);const links=[...nav.querySelectorAll('a')];let pending=false;const update=()=>{let active=0;headings.forEach((x,i)=>{if(x.getBoundingClientRect().top<=150)active=i});links.forEach((a,i)=>i===active?a.setAttribute('aria-current','location'):a.removeAttribute('aria-current'));pending=false};addEventListener('scroll',()=>{if(!pending){pending=true;requestAnimationFrame(update)}},{passive:true});links.forEach(a=>a.addEventListener('click',()=>{if(mq.matches)details.open=false}));update()})();