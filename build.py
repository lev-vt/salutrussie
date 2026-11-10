#!/usr/bin/env python3
"""SalutRussie static builder. Preserves Claude source while making a unified platform.
Run: python3 build.py. Dependencies: beautifulsoup4.
Production: SITE_ORIGIN=https://your-real-domain.example PUBLIC_RELEASE=1 python3 build.py
"""
from __future__ import annotations
import base64, json, os, re, shutil, html
from pathlib import Path
from urllib.parse import quote
from bs4 import BeautifulSoup

# Owner-approved temporary hold: do not generate placeholder testimonials.
# Original Claude review templates remain preserved in src/original/.
REVIEWS_ENABLED = False

ROOT=Path(__file__).resolve().parent
SRC=ROOT/'src'/'original'
OUT=ROOT/'dist'
ORIGIN=os.getenv('SITE_ORIGIN','').rstrip('/')
PUBLIC=os.getenv('PUBLIC_RELEASE')=='1' and ORIGIN.startswith('https://')
if os.getenv('PUBLIC_RELEASE')=='1': raise SystemExit('Commercial MVP requires owner approval. Preview only.')
OUT.mkdir(exist_ok=True)
for f in OUT.iterdir():
    if f.is_dir():shutil.rmtree(f)
    else:f.unlink()
(OUT/'assets').mkdir()
CSS={}
for lang,fn in [('ru','index-ru.html'),('fr','index.html')]:
    bs=BeautifulSoup((SRC/fn).read_text(encoding='utf-8'),'html.parser')
    CSS[lang]=bs.style.get_text()
    (OUT/'assets'/f'claude-{lang}.css').write_text(CSS[lang],encoding='utf-8')
    for photo_idx,img in enumerate(bs.select('img[src^="data:image"]')):
        src=img.get('src',''); kind,b64=src.split(',',1)
        ext='jpg' if 'jpeg' in kind else 'png'
        path=f'/assets/{lang}-original-{photo_idx}.{ext}'
        (OUT/path.lstrip('/')).write_bytes(base64.b64decode(b64))

CSS_ADD=r'''
/* SalutRussie v2 additions. Original Claude CSS is preserved in claude-{lang}.css. */
:root { color-scheme: light; }
body { min-width: 300px; }
.nav { max-width: 1360px; }
.nav-links { align-items:center; }
.nav-links > li { position:relative; }
.nav-links .nav-drop { position:absolute; top:calc(100% + 14px); left:-20px; padding:14px; width:275px; background:#202D4C; border:1px solid #4C5470; box-shadow:0 18px 32px rgba(0,0,0,.24); display:none; z-index:90; }
.nav-links .has-drop.is-open .nav-drop {display:grid;gap:2px}
.nav-links .nav-drop a {padding:9px 10px;display:block;font-size:13px;white-space:normal; }
.nav-links .nav-drop a:hover {background:rgba(255,255,255,.1);}
.nav-links .has-drop > button {border:0;background:transparent;color:var(--cream-text-soft);font:inherit;padding:0;cursor:pointer;}
.nav-cta { border-radius:2px; }
.nav {gap:9px;}
.sr-button {font:inherit;border:0;cursor:pointer;}
.sr-hero-kicker {color:var(--gold-soft);letter-spacing:.09em;text-transform:uppercase;font-size:12px;font-weight:700;}
.hero.v2-home h1 {font-size:clamp(39px,4.6vw,63px);max-width:800px;margin:20px 0 23px;line-height:1.12;}
.hero.v2-home .hero-lede {max-width:720px;}
.hero.v2-home .hero-actions {display:flex;gap:12px;flex-wrap:wrap;margin-top:27px;}
.sr-width {max-width:var(--maxw); margin:0 auto;padding:0 28px;}
.sr-sec {padding:76px 0;}
.sr-sec.alt {background:var(--parchment-2)}
.sr-section-head {max-width:820px; margin:0 0 34px;}
.sr-section-head h2 {font-size:clamp(30px,3.5vw,43px);margin:8px 0 12px;}
.sr-section-head p {font-size:15px;color:var(--ink-text-soft);}
.sr-grid {display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;}
.sr-card {display:flex;flex-direction:column;gap:12px;padding:28px;border:1px solid var(--line);background:var(--parchment);text-decoration:none;min-height:255px;transition:transform .2s,border-color .2s;}
.sr-card:hover {transform:translateY(-3px);border-color:var(--gold);}
.sr-card .sr-icon {display:inline-flex;align-items:center;justify-content:center;font-family:var(--font-display);border:1px solid var(--gold);color:var(--seal);width:41px;height:41px;font-size:25px;}
.sr-card h3 {font-size:24px;line-height:1.2;}
.sr-card p {color:var(--ink-text-soft);font-size:14px;line-height:1.6;}
.sr-card .sr-link {color:var(--seal);font-size:13px;font-weight:700;margin-top:auto;}
.sr-feature {background:var(--ink);color:var(--cream-text);padding:48px;display:grid;grid-template-columns:minmax(0,1.4fr) minmax(220px,.6fr);gap:30px;align-items:center;}
.sr-feature h2 {font-size:clamp(34px,4vw,48px);margin:12px 0;line-height:1.2;}
.sr-feature .sr-feature-qualifier {display:block;font-family:var(--font-body,Inter,sans-serif);font-size:clamp(18px,2.15vw,27px);font-weight:500;line-height:1.35;margin-top:9px;color:var(--cream-text);}
.sr-feature p {color:var(--cream-text-soft);font-size:15px;line-height:1.7;max-width:700px;}
.sr-feature .sr-star {font-size:93px;color:var(--gold);line-height:1;text-align:center;}
.sr-feature .btn {margin-top:24px;}
.sr-steps {display:grid;grid-template-columns:repeat(4,1fr);gap:20px;}
.sr-step {padding:24px;border-top:2px solid var(--gold);}
.sr-step b {font-family:var(--font-display);font-size:27px;color:var(--seal);}
.sr-step h3 {font-size:19px;margin:10px 0;}
.sr-step p {font-size:13px;color:var(--ink-text-soft);}
.sr-cta {padding:48px;background:var(--ink);color:var(--cream-text);display:flex;justify-content:space-between;gap:25px;align-items:center;}
.sr-cta h2 {font-size:clamp(28px,3vw,36px);}
.sr-cta p {color:var(--cream-text-soft);margin-top:12px;}
.sr-breadcrumb {padding:14px 28px;font-size:12px;color:var(--ink-text-soft);max-width:var(--maxw);margin:auto;}
.sr-breadcrumb a {text-decoration:underline;text-underline-offset:3px;}
.sr-content {max-width:770px;padding:40px 28px 64px;margin:auto;}
.sr-content p {margin:0 0 20px;line-height:1.8;}
.sr-content ul {margin:0 0 26px;padding-left:21px;line-height:1.8;}
.sr-content h2 {font-size:27px;margin:30px 0 14px;}
.sr-contact-list {display:grid;grid-template-columns:repeat(2,1fr);gap:14px;}
.sr-contact-choice {display:block;border:1px solid var(--line);background:var(--parchment-2);padding:25px;text-decoration:none;}
.sr-contact-choice strong {display:block;font-size:19px;margin-bottom:7px;}
.sr-contact-choice span {font-size:13px;color:var(--ink-text-soft);}
.sr-contact-choice:hover {border-color:var(--gold);}
.sr-meta {font-size:12px;color:var(--ink-text-soft);}
.sr-note {font-size:13px;color:var(--ink-text-soft);padding:15px 20px;border-left:3px solid var(--gold);background:var(--parchment-2);margin-top:22px;}
.sr-input {width:100%;padding:14px 16px;background:var(--parchment);color:var(--ink-text);border:1px solid var(--line);font:inherit;}
.sr-search-bar {display:flex;gap:12px;margin:24px 0;}
.sr-pills {display:flex;gap:7px;flex-wrap:wrap;margin:0 0 20px;}
.sr-pill {border:1px solid var(--line);background:transparent;color:var(--ink-text);font:inherit;font-size:12px;padding:9px 14px;cursor:pointer;}
.sr-pill[aria-pressed="true"] {color:#fff;background:var(--ink);border-color:var(--ink);}
.sr-results {margin:0 0 16px;font-size:13px;color:var(--ink-text-soft);}
.sr-hidden {display:none !important;}
.sr-result {min-height:0;}
.sr-result small {color:var(--gold);font-size:12px;font-weight:700;}
.sr-result h3 {margin-top:6px;}
.sr-footer {background:var(--ink);color:var(--cream-text-soft);padding:33px 0;}
.sr-footer .sr-width {display:flex;align-items:start;justify-content:space-between;gap:24px;flex-wrap:wrap;}
.sr-footer .sr-footer-brand {color:var(--cream-text);font-family:var(--font-display);font-size:22px;}
.sr-footer a {color:var(--cream-text-soft);font-size:12px;margin-right:14px;line-height:2.5;}
.sr-footer .sr-small {font-size:11px;max-width:390px;line-height:1.7;}
.sr-top {background:var(--ink);color:var(--cream-text);padding:54px 0;}
.sr-top h1 {font-size:clamp(34px,4.3vw,53px);max-width:900px;margin:10px 0 20px;}
.sr-top p {color:var(--cream-text-soft);max-width:780px;font-size:16px;line-height:1.75;}
.sr-eyebrow {font-size:12px;color:var(--gold-soft);letter-spacing:.12em;text-transform:uppercase;font-weight:700;}
.sr-kb-topics {display:flex;gap:9px;flex-wrap:wrap;}
.sr-kb-empty {padding:30px;color:var(--ink-text-soft);}
.sr-mobile-consult {display:none;}
.sr-theme-compat {display:none;}
/* Russian consultation chooser: source-language specific markup only */
.sr-contact-details {min-width:0;border:1px solid var(--line);background:var(--parchment-2);align-self:start;}
.sr-contact-details[open] {border-color:var(--gold);}
.sr-contact-details .sr-contact-choice {border:0;cursor:pointer;list-style:none;}
.sr-contact-details .sr-contact-choice::-webkit-details-marker {display:none;}
.sr-contact-details .sr-contact-choice:focus-visible {outline:2px solid var(--gold);outline-offset:-3px;}
.sr-contact-channels {padding:0 22px 22px;}
.sr-contact-channels p {font-size:13px;line-height:1.6;margin:0 0 10px;}
.sr-channel-links {display:flex;gap:9px;flex-wrap:wrap;margin:12px 0 20px;}
.sr-channel-links a,.sr-copy-topic {padding:10px 12px;color:var(--ink-text);border:1px solid var(--gold);background:var(--parchment);text-decoration:none;font-size:13px;line-height:1.35;}
.sr-channel-links a:hover,.sr-copy-topic:hover {background:var(--gold-soft);}
.sr-channel-caption {color:var(--ink-text-soft);}
.sr-copy-row {display:grid;gap:10px;}
.sr-draft {font-size:12px;line-height:1.6;overflow-wrap:anywhere;}
.sr-copy-topic {justify-self:start;}
/* Russian About: built with original Claude colors, fonts, portrait layout */
.sr-about-founder .founder-card h2 {font-family:var(--font-display);font-size:clamp(26px,3vw,35px);margin-bottom:8px;}
.sr-about-flow {display:grid;justify-items:center;gap:0;margin-top:24px;}
.sr-about-node {border:1px solid var(--line);padding:24px;background:var(--parchment);width:min(100%,720px);text-align:center;}
.sr-about-node h3 {font-size:24px;margin:0 0 7px;}
.sr-about-node p {font-size:14px;line-height:1.7;color:var(--ink-text-soft);margin:0;}
.sr-about-node.main {background:var(--ink);color:var(--cream-text);border-color:var(--gold);}
.sr-about-node.main p {color:var(--cream-text-soft);}
.sr-about-branches {display:grid;grid-template-columns:1fr 1fr;gap:15px;width:min(100%,890px);}
.sr-about-branches .sr-about-node {height:100%;width:100%;}
.sr-about-connector {height:35px;width:1px;background:var(--gold);}
.sr-about-cities {font-size:13px;color:var(--ink-text-soft);margin-top:24px;line-height:1.85;text-align:center;}
.sr-about-standards {max-width:820px;}
.sr-about-mission {max-width:900px;}
.sr-about-mission p {line-height:1.8;margin-bottom:14px;}
.sr-about-vision {font-family:var(--font-display);font-size:clamp(24px,2.8vw,35px);color:var(--seal);margin-bottom:20px;}
.sr-about-services .service-col p {line-height:1.7;margin-top:14px;}
.sr-about-services .service-col a {color:var(--seal);font-size:13px;font-weight:700;display:inline-block;margin-top:18px;}
@media(max-width:650px){.sr-about-branches{grid-template-columns:1fr;}.sr-about-founder .lev-photo{width:100%;max-width:400px;}}
@media(max-width:1130px) {.nav-links {gap:10px;font-size:12px;} .nav-cta {font-size:12px;padding:8px 11px}}
@media(max-width:980px) {
  .sr-grid {grid-template-columns:repeat(2,minmax(0,1fr));}
  .sr-steps {grid-template-columns:repeat(2,1fr)}
  .sr-feature {grid-template-columns:1fr;}
  .sr-feature .sr-star {display:none;}
  .nav-links .nav-drop {position:static;background:transparent;border:0;box-shadow:none;padding:8px 0 8px 12px;width:100%;}
  .nav-links .has-drop.is-open .nav-drop {display:grid;}
  .nav-links .has-drop>button {padding:10px 0;color:var(--cream-text);font-size:15px;}
  .sr-mobile-consult {display:block;}
}
@media(max-width:680px) {
  .sr-grid,.sr-contact-list {grid-template-columns:1fr;}
  .sr-steps {grid-template-columns:1fr 1fr;gap:7px;}
  .sr-feature,.sr-cta {padding:30px 23px;}
  .sr-cta {display:block;}
  .sr-cta .btn {margin-top:24px;}
  .sr-sec {padding:53px 0;}
  .sr-card {min-height:190px;padding:23px;}
  .sr-search-bar {display:block;}
  .sr-width {padding:0 20px;}
}
@media(max-width:420px) {.sr-steps {grid-template-columns:1fr;} .sr-card h3 {font-size:21px;}}
'''
(OUT/'assets'/'platform.css').write_text(CSS_ADD,encoding='utf-8')
JS=r'''(() => {
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
  const previous=b.textContent;
  b.textContent=ok?'Скопировано':'Выделите и скопируйте текст';
  if(!ok){const sel=window.getSelection();const range=document.createRange();range.selectNodeContents(el);sel.removeAllRanges();sel.addRange(range);}
  b.focus();
 }));
 document.querySelectorAll('[data-analytics-event]').forEach(el=>el.addEventListener('click',()=>{if(typeof window.ym==='function'&&window.SALUTRUSSIE_METRIKA_ID){window.ym(window.SALUTRUSSIE_METRIKA_ID,'reachGoal',el.dataset.analyticsEvent);}}));
})();'''
(OUT/'assets'/'platform.js').write_text(JS,encoding='utf-8')

def esc(x):return html.escape(str(x),quote=True)
LANGS={
 'ru':{'home':'Главная','services':'Услуги','decree':'Указ 702','kb':'Полезная информация','about':'О нас','contacts':'Контакты','consult':'Консультация','reviews':'Отзывы','prices':'Тарифы','more':'Подробнее →','discuss':'Обсудить задачу →','start':'Начать с консультации','all':'Все','articles':'Статьи','instructions':'Инструкции','news':'Новости'},
 'fr':{'home':'Accueil','services':'Services','decree':'Décret n° 702','kb':'Informations utiles','about':'Notre équipe','contacts':'Contact','consult':'Consultation','reviews':'Avis','prices':'Tarifs','more':'En savoir plus →','discuss':'Discuter de votre projet →','start':'Demander une consultation','all':'Tout','articles':'Articles','instructions':'Guides','news':'Actualités'},
}
SECTIONS={
 'migration':{'ru':('Immigration et statuts','Миграция и переезд','РВП, ВНЖ, гражданство, визы, Указ 702 и правовая помощь при простых и сложных миграционных ситуациях.'),'fr':('Immigration','Immigration et séjour','Titres de séjour, visas, nationalité russe et accompagnement juridique.') ,'symbol':'✦'},
 'real-estate':{'ru':('Недвижимость','Недвижимость','Поиск недвижимости для аренды и покупки. Проверка объекта и безопасное проведение сделки.'),'fr':('Immobilier','Immobilier en Russie','Location, acquisition, analyse de contrats et vérification juridique.'),'symbol':'⌂'},
 'business':{'ru':('Бизнес','Бизнес в России','Создание компании. Юридическое сопровождение бизнеса с иностранным участием. Налоги, избежание двойного налогообложения, бухгалтерское сопровождение.'),'fr':('Entreprises','Créer une entreprise','Constitution de sociétés et accompagnement juridique des entrepreneurs étrangers.'),'symbol':'§'},
 'investments':{'ru':('Инвестиции','Инвестиции','Выбор объектов для инвестиций. Юридическая проверка и сопровождение инвестиционных проектов в России.'),'fr':('Investissements','Investissements en Russie','Audit juridique et accompagnement de projets d’investissement.'),'symbol':'↗'},
 'legal':{'ru':('Правовая помощь','Юридическая помощь','Правовая поддержка иностранцев в России по всем сферам права.'),'fr':('Juridique','Assistance juridique','Documents, analyse des risques, litiges et solutions personnalisées.'),'symbol':'⚖'},
 'relocation':{'ru':('Переезд','Переезд и адаптация','Помощь с организационными и бытовыми вопросами переезда: транспортировка личных вещей, выбор региона проживания, профессии и направления деятельности; подбор языковых курсов, помощь в адаптации семей с детьми.'),'fr':('Installation','Installation et intégration','Assistance pratique pour préparer et organiser votre installation en Russie.'),'symbol':'◎'},
}
PROGRAMS={
 'rvp':{'ru':('Разрешение на временное проживание','РВП в России','Проверяем основание для оформления РВП, документы и применимую процедуру. В отдельных ситуациях необходим индивидуальный правовой анализ.'),'fr':('Permis de séjour temporaire','Séjour temporaire (RVP)','Vérification de l’éligibilité, des pièces et de la procédure adaptée.')},
 'vnzh':{'ru':('Вид на жительство','ВНЖ в России','Анализируем возможные основания для получения вида на жительство и последовательность действий.'),'fr':('Résidence permanente','Titre de séjour (VNZh)','Analyse des voies d’accès au titre de séjour et des documents requis.')},
 'citizenship':{'ru':('Гражданство Российской Федерации','Гражданство России','Выбираем применимое основание, проверяем документы и сопровождаем согласованную процедуру.'),'fr':('Nationalité russe','Nationalité russe','Vérification du fondement juridique et accompagnement du dossier.')},
 'visas':{'ru':('Визы','Визы в Россию','Помогаем определить подходящий визовый режим, проверить документы и последовательность оформления.'),'fr':('Visas','Visas pour la Russie','Choix du régime de visa et préparation du dossier.')},
 'students':{'ru':('Образование и РВПО','РВПО и учёба в России','Помощь иностранным студентам по вопросам статуса и документов.'),'fr':('Études','Études et séjour','Assistance aux étudiants étrangers concernant le statut et les documents.')},
 'family':{'ru':('Переезд семьи','Семейный переезд','Подбираем последовательность оформления статусов и документов для членов семьи.'),'fr':('Famille','S’installer en famille','Planifier le statut et les démarches des membres de la famille.')},
 'disputes':{'ru':('Судебная защита','Миграционные споры','Обжалование отказов и решений органов власти, защита в суде и оценка процессуальных рисков.'),'fr':('Contentieux','Contentieux migratoire','Recours contre les décisions administratives et défense devant les tribunaux.')}
}
SUBPAGES={
 'real-estate':['rent','buy','legal-check'],
 'business':['company-registration','legal-support'],
 'investments':['legal-due-diligence','project-support'],
 'legal':['document-preparation','disputes']
}
SUBLABEL={
 'rent':('Помощь с арендой жилья','Aide à la location'), 'buy':('Покупка недвижимости','Acquisition immobilière'), 'legal-check':('Юридическая проверка недвижимости','Vérification juridique'),
 'company-registration':('Открытие компании','Création d’entreprise'),'legal-support':('Юридическое сопровождение бизнеса','Conseil juridique aux entreprises'),
 'legal-due-diligence':('Юридическая проверка инвестиций','Audit juridique d’investissement'),'project-support':('Сопровождение инвестиционного проекта','Accompagnement de projets'),
 'document-preparation':('Подготовка документов','Préparation de documents'),'disputes':('Судебные споры','Contentieux juridique')}

ARTICLES=[
 {'slug':'how-to-choose-residence','topic':'migration','kind':'guide','ru':('Как выбрать основание для проживания в России','Практический ориентир: чем различаются визы, РВП и ВНЖ и почему выбор начинается с личных обстоятельств.','Сначала важно определить цель проживания, состав семьи, гражданство, миграционную историю и имеющиеся документы. Универсальной процедуры для всех иностранцев нет. Выбор маршрута требует проверки действующего закона и фактических обстоятельств.'),'fr':('Choisir son statut de séjour en Russie','Comprendre les différences entre visas, RVP et VNZh et les premières questions à examiner.','Le choix dépend de la nationalité, de la situation familiale, des documents et du projet de séjour. Les règles doivent être vérifiées au cas par cas.')},
 {'slug':'renting-a-home','topic':'real-estate','kind':'guide','ru':('Аренда квартиры в России: что проверить иностранцу','Короткий список вопросов до подписания договора аренды и внесения денежных средств.','До оплаты следует установить, кто предлагает квартиру и на каком основании, внимательно прочитать условия договора, проверить порядок возврата обеспечительного платежа и заранее обсудить миграционный учёт, если он необходим.'),'fr':('Louer un logement en Russie : les points à vérifier','Questions essentielles avant de signer un bail ou de transférer de l’argent.','Vérifiez l’identité du bailleur, les conditions du contrat, le dépôt de garantie et les démarches liées au séjour.')},
 {'slug':'starting-a-business','topic':'business','kind':'article','ru':('Открытие бизнеса в России: с чего начать иностранцу','Какие вопросы нужно решить до выбора формы компании и подписания документов.','Вначале важно описать деятельность, предполагаемых клиентов, состав участников, источники финансирования и необходимые разрешения. Форма компании и последовательность регистрации определяются после правовой и налоговой оценки конкретной модели.'),'fr':('Créer une entreprise en Russie : par où commencer ?','Questions à examiner avant de choisir la structure et de déposer les documents.','Il convient de définir l’activité, les partenaires, le financement et les contraintes réglementaires avant de choisir la structure.')},
 {'slug':'investor-checklist','topic':'investments','kind':'guide','ru':('Юридическая проверка инвестиционного проекта: базовый список','Что стоит изучить до подписания инвестиционного договора.','Проверка может включать полномочия сторон, структуру владения активами, существующие обязательства, разрешения, ограничения и условия выхода из проекта. Конкретный перечень зависит от сделки.'),'fr':('Vérifier juridiquement un projet d’investissement','Les sujets à examiner avant de signer un accord d’investissement.','La revue porte notamment sur les parties, les actifs, les obligations, les autorisations et les conditions de sortie, selon la transaction.')},
]

def path(lang,tail=''):
 return f'/{lang}/'+ (tail.strip('/')+'/' if tail.strip('/') else '')

def service_url(lang,slug):return path(lang,slug)
def meta(title,desc,lang,url,noindex=False,article=False,pub=None):
 tags=f'<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} · SalutRussie</title><meta name="description" content="{esc(desc)}"><meta name="theme-color" content="#131B2E"><meta name="robots" content="{"noindex,nofollow" if noindex or not PUBLIC else "index,follow"}">'
 tags+='<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,500&family=Inter:wght@400;500;600;700&display=swap">'
 tags+=f'<link rel="stylesheet" href="/assets/claude-{lang}.css"><link rel="stylesheet" href="/assets/platform.css"><meta property="og:type" content="{"article" if article else "website"}"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}">'
 if PUBLIC:
  tags+=f'<link rel="canonical" href="{esc(ORIGIN+url)}"><meta property="og:url" content="{esc(ORIGIN+url)}">'
  counterpart=url.replace('/ru/','/fr/',1) if lang=='ru' else url.replace('/fr/','/ru/',1)
  # Only output language references to actual generated equivalents.
  tags+=f'<link rel="alternate" hreflang="ru" href="{esc(ORIGIN+(url if lang=="ru" else counterpart))}"><link rel="alternate" hreflang="fr" href="{esc(ORIGIN+(url if lang=="fr" else counterpart))}">'
  schema={'@context':'https://schema.org','@type':'Article' if article else 'WebPage','headline':title,'url':ORIGIN+url,'inLanguage':lang,'publisher':{'@type':'Organization','name':'SalutRussie'},'author':{'@type':'Person','name':'Лев Втюрин'}}
  if article and pub: schema['datePublished']=pub
  tags+=f'<script type="application/ld+json">{json.dumps(schema,ensure_ascii=False).replace("<", "\\u003c")}</script>'
 return tags

def nav(lang):
 x=LANGS[lang]; s=f'''<header class="sr-header"><nav class="nav" aria-label="{'Основное меню' if lang=='ru' else 'Navigation principale'}"><a class="brand" href="{path(lang)}" aria-label="SalutRussie">
 <svg class="seal-mark" fill="none" viewBox="0 0 60 60" aria-hidden="true"><circle cx="30" cy="30" r="27" stroke="#A9803E" stroke-width="1.2"/><circle cx="30" cy="30" r="21" stroke="#A9803E" stroke-width="0.7"/><text x="30" y="37" font-size="17" font-family="Fraunces,serif" text-anchor="middle" fill="#F1ECDE">SR</text></svg><span>SalutRussie</span></a>
<button class="burger" id="burger" aria-label="Menu" aria-controls="navLinks" aria-expanded="false">☰</button><ul class="nav-links" id="navLinks">
<li class="has-drop"><button type="button" class="sr-drop-button" aria-expanded="false" aria-controls="service-drop">{x['services']} ▾</button><div class="nav-drop" id="service-drop">'''
 for slug,data in SECTIONS.items(): s+=f'<a href="{path(lang,slug)}">{esc(data[lang][1])}</a>'
 s+=f'''</div></li><li><a href="{path(lang,'migration/decree-702')}">{x['decree']}</a></li><li><a href="{path(lang,'knowledge')}">{x['kb']}</a></li><li><a href="{path(lang,'about')}">{x['about']}</a></li><li><a href="{path(lang,'contacts')}">{x['contacts']}</a></li>
</ul><div class="lang-switch"><a href="{path('fr')}"{' class="active"' if lang=='fr' else ''}>FR</a><a href="{path('ru')}"{' class="active"' if lang=='ru' else ''}>RU</a></div><a class="nav-cta" data-analytics-event="consultation_click" href="{path(lang,'consultations')}">{x['consult']} →</a></nav></header>'''
 return s

def footer(lang):
 x=LANGS[lang]
 return f'''<footer class="sr-footer"><div class="sr-width"><div><div class="sr-footer-brand">SalutRussie</div><p class="sr-small">{'Профессиональная помощь для иностранцев в России' if lang=='ru' else 'Services juridiques et pratiques pour les étrangers en Russie. Le périmètre et le prestataire sont précisés avant tout contrat.'}</p></div><div><a href="{path(lang,'services')}">{x['services']}</a><a href="{path(lang,'consultations')}">{x['consult']}</a><a href="{path(lang,'knowledge')}">{x['kb']}</a><a href="{path(lang,'pricing')}">{x['prices']}</a><a href="{path(lang,'contacts')}">{x['contacts']}</a><br><a href="{path(lang,'privacy')}">{'Персональные данные' if lang=='ru' else 'Données personnelles'}</a><p class="sr-small">{'© 2018–2026 SalutRussie' if lang=='ru' else '© 2026 SalutRussie'} · ООО «Инновационные правовые решения»</p></div></div></footer>'''

def link_msg(lang,topic):
 txt=(f'Здравствуйте! Обращаюсь с сайта SalutRussie. Тема: {topic}. Хотел(а) бы узнать о консультации.' if lang=='ru' else f'Bonjour ! Je vous contacte via SalutRussie. Sujet : {topic}. Je souhaite réserver une consultation.')
 return 'https://wa.me/79685341915?text='+quote(txt)

def feature(lang):
 if lang=='ru':
  paragraphs=[
   'Популярная программа переезда для иностранцев, разделяющих традиционные российские ценности.',
   'Мы много работаем по Указу 702: выбираем миграционную стратегию, готовим документы, сопровождаем оформление специальной частной визы на срок до трёх месяцев и дальнейшее получение РВП.',
   'Для начала проверьте, входит ли страна вашего гражданства в перечень государств программы.'
  ]
  body=''.join(f'<p>{esc(x)}</p>' for x in paragraphs)
  return f"""<section class="sr-sec"><div class="sr-width"><div class="sr-feature"><div><span class="sr-eyebrow">СПЕЦИАЛЬНАЯ ПРОГРАММА «РАЗДЕЛЕНИЕ ЦЕННОСТЕЙ»</span><h2>Переезд в Россию по Указу 702<span class="sr-feature-qualifier">Разделение ценностей (идеологическая программа)</span></h2>{body}<a class="btn btn-primary" href="{path(lang,'migration/decree-702')}">Подробнее об Указе 702 →</a></div><span class="sr-star" aria-hidden="true">✳</span></div></div></section>"""
 return f"""<section class="sr-sec"><div class="sr-width"><div class="sr-feature"><div><span class="sr-eyebrow">PROGRAMME DE RELOCALISATION</span><h2>S’installer en Russie : décret n° 702</h2><p>Un dispositif spécifique soumis à des conditions légales. Nous évaluons votre éligibilité et vous accompagnons dans la préparation du dossier.</p><a class="btn btn-primary" href="{path(lang,'migration/decree-702')}">Découvrir le décret 702 →</a></div><span class="sr-star" aria-hidden="true">✳</span></div></div></section>"""

def cards(lang,items):
 z='<div class="sr-grid">'
 for slug,data in items:
  info=data[lang];dest=path(lang,slug)
  z+=f'<a class="sr-card" href="{dest}"><span class="sr-icon" aria-hidden="true">{esc(data.get("symbol","↗"))}</span><h3>{esc(info[1])}</h3><p>{esc(info[2])}</p><span class="sr-link">{LANGS[lang]["more"]}</span></a>'
 return z+'</div>'

def heading(lang,title,subtitle,kicker='SalutRussie'):
 return f'<div class="sr-top"><div class="sr-width"><div class="sr-eyebrow">{esc(kicker)}</div><h1>{esc(title)}</h1><p>{esc(subtitle)}</p></div></div>'

def cta(lang,title=None):
 text=title or ('Нужна помощь?' if lang=='ru' else 'Un accompagnement pour votre situation ?')
 sub='Выберите направление консультации. Объём работы и стоимость согласуем.' if lang=='ru' else 'Choisissez votre domaine de consultation. Le périmètre et les tarifs seront confirmés avant tout engagement.'
 return f'<section class="sr-sec"><div class="sr-width"><div class="sr-cta"><div><h2>{esc(text)}</h2><p>{sub}</p></div><a class="btn btn-primary" data-analytics-event="consultation_click" href="{path(lang,"consultations")}">{LANGS[lang]["start"]} →</a></div></div></section>'

def shell(lang,url,title,description,body,noindex=False,article=False):
 return '<!doctype html>\n'+f'<html lang="{lang}"><head>{meta(title,description,lang,url,noindex,article)}</head><body>{nav(lang)}<main id="main">{body}</main>{footer(lang)}<script src="/assets/platform.js" defer></script></body></html>'

def home(lang):
 ru=lang=='ru';title='Помощь иностранцам в России: миграция, недвижимость, бизнес' if ru else 'Services aux étrangers en Russie : immigration, immobilier, affaires'
 intro='Живите, работайте и развивайте бизнес в России — опираясь на наш опыт и знания' if ru else 'Vivre, s’installer et entreprendre en Russie — avec le bon accompagnement.'
 detail=('Миграция, недвижимость, создание бизнеса, инвестиции и юридическая помощь. Мы помогаем по всем вопросам в России, организуем профессиональное сопровождение.' if ru else 'Immigration, immobilier, création d’entreprise, investissement et conseil juridique. Un interlocuteur pour trouver la bonne solution et organiser votre accompagnement.')
 emblem=BeautifulSoup((SRC/('index-ru.html' if ru else 'index.html')).read_text(),'html.parser').select_one('.hero-seal')
 emblem=str(emblem) if emblem else '<div class="hero-seal" aria-hidden="true">SR</div>'
 hero=f'''<section class="hero v2-home"><div class="wrap"><div><div class="sr-hero-kicker">{'УСЛУГИ ДЛЯ ИНОСТРАНЦЕВ В РОССИИ' if ru else 'SERVICES AUX ÉTRANGERS EN RUSSIE'}</div><h1>{esc(intro)}</h1><p class="hero-lede">{esc(detail)}</p><div class="hero-actions"><a class="btn btn-primary" data-analytics-event="consultation_click" href="{path(lang,'consultations')}">{'Получить консультацию →' if ru else 'Demander une consultation →'}</a><a class="btn btn-ghost" href="{path(lang,'services')}">{'Все услуги' if ru else 'Tous nos services'}</a></div></div>{emblem}</div></section>'''
 services=f'''<section class="sr-sec" id="services"><div class="sr-width"><div class="sr-section-head"><span class="eyebrow">{'НАПРАВЛЕНИЯ' if ru else 'NOS SERVICES'}</span><h2>{'Чем мы можем помочь' if ru else 'Comment pouvons-nous vous aider ?'}</h2><p>{'Выберите интересующее вас направление — мы подскажем, с чего начать' if ru else 'Choisissez votre besoin : nous définirons l’accompagnement approprié.'}</p></div>{cards(lang,list(SECTIONS.items()))}</div></section>'''
 steps=[('01','Ваша заявка','Опишите свой вопрос своими словами в том формате, как вам удобно'),('02','Консультация','Проводим подробную консультацию, разбираем вашу ситуацию и отвечаем на все вопросы'),('03','План действий','Готовим пошаговый план действий для достижения вашей цели'),('04','Сопровождение','Сопровождаем на всех этапах согласно выбранному тарифу')] if ru else [('01','Expliquez votre projet','Présentez votre besoin sans documents sensibles au premier contact.'),('02','Choisissez une consultation','Nous définissons la prestation et le spécialiste.'),('03','Obtenez un plan','Analyse des pièces et étapes suivantes.'),('04','Accompagnement','Nous intervenons selon le périmètre convenu.')]
 process=f'''<section class="sr-sec alt"><div class="sr-width"><div class="sr-section-head"><span class="eyebrow">{'ПРОЦЕСС' if ru else 'NOTRE MÉTHODE'}</span><h2>{'Как мы работаем' if ru else 'Comment nous travaillons'}</h2></div><div class="sr-steps">'''
 for n,h,p in steps:process+=f'<div class="sr-step"><b>{n}</b><h3>{esc(h)}</h3><p>{esc(p)}</p></div>'
 process+='</div></div></section>'
 knowledge=f'''<section class="sr-sec"><div class="sr-width"><div class="sr-section-head"><span class="eyebrow">{'ЭКСПЕРТНЫЕ МАТЕРИАЛЫ' if ru else 'RESSOURCES'}</span><h2>{'Полезная информация' if ru else 'Informations utiles'}</h2><p>{'Всё, что важно знать о жизни, переезде и бизнесе в России. Делимся профессиональным опытом, объясняем законодательство, разбираем практические ситуации и рассказываем о важных изменениях.' if ru else 'Guides pratiques, analyses juridiques, articles et actualités dans un seul espace.'}</p></div>'''
 opts=[]
 for a in ARTICLES[:3]:opts.append((f'knowledge/articles/{a["slug"]}',{'symbol':'↗',lang:(a[lang][0],a[lang][0],a[lang][1])}))
 knowledge+=cards(lang,opts)+f'<p style="margin-top:25px"><a class="btn btn-ghost" href="{path(lang,"knowledge")}">{"Все материалы и поиск →" if ru else "Rechercher dans les ressources →"}</a></p></div></section>'
 about=f'''<section class="sr-sec alt"><div class="sr-width"><div class="sr-section-head"><span class="eyebrow">{'О КОМАНДЕ' if ru else 'NOTRE ÉQUIPE'}</span><h2>{'Небольшая команда профессионалов: бутик, а не масс-маркет' if ru else 'Expertise juridique et coordination des spécialistes'}</h2><p>{'Все специалисты SalutRussie придерживаются единого стандарта качества услуг. Мы делаем только то, что приближает к результату. Наш главный принцип — сначала стратегия, потом реализация' if ru else 'Chaque situation commence par l’analyse de vos besoins. Nous précisons les prestations réalisées par notre équipe et celles de nos partenaires.'}</p></div><a class="btn btn-primary" href="{path(lang,"about")}">{'О нас →' if ru else 'Notre équipe →'}</a></div></section>'''
 meta_description=('Помощь иностранцам в России: миграция, РВП, ВНЖ, Указ 702 (разделение ценностей, идеологическая программа), недвижимость, бизнес и юридическая помощь.' if ru else detail)
 return shell(lang,path(lang),title,meta_description,hero+services+feature(lang)+process+knowledge+about+cta(lang))

def about_ru():
 source=BeautifulSoup((SRC/'o-kompanii-ru.html').read_text(encoding='utf-8'),'html.parser')
 portrait=source.select_one('main img.lev-photo')['src']
 kind,data=portrait.split(',',1)
 asset='/assets/ru-o-kompanii-ru-0.jpg'
 (OUT/asset.lstrip('/')).write_bytes(base64.b64decode(data))
 body="""<div class="page-head"><div class="wrap"><span class="eyebrow">МИГРАЦИОННОЕ БЮРО</span><h1>Мы начинали как семейное бюро — сегодня работаем по всей России</h1><p>SalutRussie выросло из небольшой семейной практики в команду профессионалов. Наш основной центр находится в Москве, а сотрудничество со специалистами в регионах позволяет сопровождать клиентов в разных городах России.</p></div></div>
 <section class="sr-sec"><div class="wrap"><div class="lev-about sr-about-founder"><img class="lev-photo" src="/assets/ru-o-kompanii-ru-0.jpg" alt="Лев Втюрин — основатель SalutRussie" width="600" height="750"><div class="founder-card"><h2>Лев Втюрин</h2><span class="role">Миграционный юрист — основатель</span><p class="bio">Более 20 лет юридической практики, включая опыт международного консалтинга. Специализация — миграционное право, судебная защита и сложные миграционные ситуации.</p><p class="bio">Большой опыт правового взаимодействия с государственными органами: МВД, ФСБ, ФНС, пограничными и таможенными органами. Лично определяет стратегию сложных дел и участвует в судебной защите клиентов.</p></div></div></div></section>
 <section class="sr-sec alt"><div class="sr-width"><div class="sr-section-head"><span class="eyebrow">КОМАНДА И ГЕОГРАФИЯ</span><h2>Как устроено наше бюро</h2><p>Мы начинали как семейное бюро, а сегодня объединяем московскую команду и профессиональные связи в разных городах страны. Каждый проект ведётся по общим стандартам SalutRussie.</p></div><div class="sr-about-flow"><div class="sr-about-node main"><h3>SalutRussie — Москва</h3><p>Основной профессиональный центр<br>Лев Втюрин — основатель<br>Команда миграционных юристов</p></div><div class="sr-about-connector" aria-hidden="true"></div><div class="sr-about-branches"><div class="sr-about-node"><h3>Профильные специалисты</h3><p>Переводчики, нотариусы и другие специалисты, необходимые для решения задачи клиента</p></div><div class="sr-about-node"><h3>Региональное сотрудничество</h3><p>Профессиональные партнёры в разных городах России. Координацию сопровождения осуществляет SalutRussie</p></div></div><div class="sr-about-connector" aria-hidden="true"></div><div class="sr-about-node"><h3>Профессиональное сообщество</h3><p>Обучение миграционных юристов, единые стандарты, сотрудничество с экспертными блогерами и сообществами иностранцев</p></div></div><p class="sr-about-cities"><strong>География сотрудничества:</strong> Москва · Санкт-Петербург · Казань · Екатеринбург · Пермь · Новосибирск · Челябинск · Уфа</p></div></section>
 <section class="sr-sec"><div class="sr-width sr-about-standards"><div class="sr-section-head"><span class="eyebrow">КАЧЕСТВО</span><h2>Единые стандарты работы</h2></div><p>Мы разработали единые стандарты подготовки документов и сопровождения миграционных дел. Обучаем юристов миграционному праву и развиваем профессиональное сотрудничество.</p><p>Мы также взаимодействуем с экспертными блогерами и сообществами иностранцев, в том числе в Telegram.</p><p class="sr-about-vision">Наш главный принцип — сначала стратегия, потом реализация</p></div></section>
 <section class="sr-sec alt"><div class="sr-width sr-about-mission"><div class="sr-section-head"><span class="eyebrow">НАШ ПОДХОД</span><h2>Философия и миссия SalutRussie</h2></div><h3 class="sr-about-vision">Безопасно и легально на каждом этапе</h3><p>Мы считаем, что переезд в Россию — это гораздо больше, чем оформление визы или вида на жительство.</p><p>Наша задача — помогать иностранцам не только с юридическими вопросами, но и с практическими задачами новой жизни: поиском жилья, адаптацией, трудоустройством, открытием бизнеса и созданием законных источников дохода в России.</p><p>Мы стремимся сделать жизнь в новой стране понятнее, безопаснее и комфортнее.</p></div></section>
 <section class="services sr-sec sr-about-services"><div class="wrap"><div class="sec-head"><span class="eyebrow">НАПРАВЛЕНИЯ РАБОТЫ</span><h2>В чём мы помогаем</h2></div><div class="service-grid"><div class="service-col"><span class="num">01</span><h3>Статус и пребывание</h3><p>Миграционные программы, оформление правового статуса и защита прав иностранных граждан.</p><a href="/ru/migration/">Миграционные услуги →</a></div><div class="service-col"><span class="num">02</span><h3>Обустройство и повседневная жизнь</h3><p>Переезд, жильё, документы и практические вопросы жизни в России.</p><a href="/ru/relocation/">Переезд и адаптация →</a></div><div class="service-col"><span class="num">03</span><h3>Бизнес и налоги</h3><p>Создание компаний, юридическое сопровождение бизнеса с иностранным участием и связанные налоговые вопросы.</p><a href="/ru/business/">Бизнес в России →</a></div></div></div></section>
 <section class="sr-sec"><div class="sr-width"><div class="sr-cta"><div><h2>Обсудим вашу ситуацию?</h2><p>Расскажите, какая задача стоит перед вами. Мы подскажем, с чего начать.</p></div><a class="btn btn-primary" href="/ru/consultations/" data-analytics-event="consultation_click">Получить консультацию →</a></div></div></section>"""
 return shell('ru','/ru/about/','О нас — миграционное бюро SalutRussie','Наше миграционное бюро: основатель Лев Втюрин, московская команда, профессиональные стандарты и региональное сотрудничество.',body)

def basic_page(lang,url,title,desc,items=None,rich=None):
 z=heading(lang,title,desc,LANGS[lang]['services'])
 if rich:z+=rich
 if items:
  z+=f'<section class="sr-sec"><div class="sr-width"><div class="sr-section-head"><h2>{"Выберите направление" if lang=="ru" else "Choisissez votre domaine"}</h2></div>{cards(lang,items)}</div></section>'
 z+=cta(lang)
 return shell(lang,url,title,desc,z,noindex=True)

def services_ru():
 title='Все услуги для иностранцев'
 desc='Профессиональная помощь в России: выберите подходящее направление.'
 shortcuts={'migration': [('migration/decree-702','Указ 702')]+[
  (f'migration/{slug}',PROGRAMS[slug]['ru'][1]) for slug in ('rvp','vnzh','visas','citizenship')
 ]}
 for section, slugs in SUBPAGES.items():
  shortcuts[section]=[(f'{section}/{slug}',SUBLABEL[slug][0]) for slug in slugs]
 body=heading('ru',title,desc,LANGS['ru']['services'])
 body+='<section class="sr-sec"><div class="sr-width"><div class="sr-section-head"><h2>Выберите направление</h2></div><div class="sr-grid">'
 for slug, data in SECTIONS.items():
  _,name,description=data['ru']
  body+=f'<section class="sr-card"><span class="sr-icon" aria-hidden="true">{esc(data["symbol"])}</span><h3>{esc(name)}</h3><p>{esc(description)}</p>'
  if slug in shortcuts:
   body+='<ul>'
   for tail,label in shortcuts[slug]:
    body+=f'<li><a href="{path("ru",tail)}">{esc(label)}</a></li>'
   body+='</ul>'
  body+=f'<a class="sr-link" href="{path("ru",slug)}">Подробнее о направлении →</a></section>'
 body+=f'</div><p><a class="sr-link" href="{path("ru","pricing")}">Тарифы →</a></p></div></section>'
 return shell('ru',path('ru','services'),title,desc,body+cta('ru'),noindex=True)

def pricing_ru():
 title='Тарифы'
 desc='Стоимость, формат и объём согласуем до оплаты.'
 body=heading('ru',title,desc,LANGS['ru']['services'])
 body+='<div class="sr-content"><p class="sr-note">Предварительная версия. Перечень услуг и цены ожидают согласования.</p><h2>Направления</h2><ul>'
 for tail,label in [('consultations','Консультации'),('migration/decree-702','Программа 702'),('relocation','Переезд и адаптация'),('services','Все услуги')]:
  body+=f'<li><a href="{path("ru",tail)}">{esc(label)}</a></li>'
 body+='</ul></div>'
 return shell('ru',path('ru','pricing'),title,desc,body+cta('ru'),noindex=True)

def service_pages(lang):
 ru=lang=='ru'
 for slug,data in SECTIONS.items():
  info=data[lang];url=path(lang,slug)
  sub=[]
  if slug=='migration':
   for k,d in PROGRAMS.items():sub.append((f'migration/{k}',{'symbol':'↗',lang:(d[lang][0],d[lang][1],d[lang][2])}))
   sub.insert(0,('migration/decree-702',{'symbol':'✳',lang:('Указ 702' if ru else 'Décret 702','Переезд по Указу 702' if ru else 'S’installer via le décret 702','Отдельная программа с анализом условий и сопровождением.' if ru else 'Vérification d’éligibilité et accompagnement spécifique.')}))
  elif slug in SUBPAGES:
   for part in SUBPAGES[slug]:
    lab=SUBLABEL[part][0 if ru else 1];sub.append((f'{slug}/{part}',{'symbol':'↗',lang:(lab,lab,'Условия и состав услуги обсуждаются индивидуально.' if ru else 'Prestations adaptées aux besoins individuels.')}))
  rich=''
  if slug in ['real-estate','business','investments','relocation']:
   notice='На этой странице представлены направления помощи. Фактическая доступность услуг и участие профильных партнёров подтверждаются при обращении; условия и результат заранее не гарантируются.' if ru else 'Ces domaines décrivent des possibilités d’accompagnement. Disponibilité et rôle des partenaires sont confirmés lors de votre prise de contact.'
   rich=f'<div class="sr-width"><p class="sr-note">{notice}</p></div>'
  write(url,basic_page(lang,url,info[1],info[2],sub if sub else None,rich))
  for part in SUBPAGES.get(slug,[]):
   lab=SUBLABEL[part][0 if ru else 1];desc=('Обсудим ваши обстоятельства, перечень документов, юридические риски, объём работы и стоимость до начала оказания услуги.' if ru else 'Nous préciserons votre situation, les risques, les pièces, les honoraires et le périmètre de la mission.')
   write(path(lang,f'{slug}/{part}'),basic_page(lang,path(lang,f'{slug}/{part}'),lab,desc))
 for slug,d in PROGRAMS.items():
  title=d[lang][1];desc=d[lang][2];url=path(lang,'migration/'+slug)
  text=('Информация носит общий характер и не заменяет изучение документов. Основания и процедура зависят от индивидуальных обстоятельств и актуального законодательства.' if ru else 'Ces informations générales ne remplacent pas une analyse individuelle du dossier et du droit en vigueur.')
  rich=f'<div class="sr-content"><h2>{"Как начинается работа" if ru else "Première étape"}</h2><p>{esc(desc)}</p><ul><li>{"Проверка текущего миграционного статуса и документов" if ru else "Vérification du statut et des documents"}</li><li>{"Определение применимого правового основания" if ru else "Identification du fondement juridique"}</li><li>{"Подбор объёма юридической помощи" if ru else "Définition de la prestation"}</li></ul><p class="sr-note">{text}</p></div>'
  write(url,basic_page(lang,url,title,desc,rich=rich))

def consultations(lang):
 ru=lang=='ru'
 entries=[('migration','Миграция и переезд','Immigration et séjour','РВП, ВНЖ, Указ 702, визы и гражданство','RVP, VNZh, décret 702, visas, nationalité'),('real-estate','Недвижимость','Immobilier','Аренда, договоры, покупка и юридическая проверка','Location, achat et contrats'),('business','Бизнес и инвестиции','Entreprises et investissements','Создание компании, инвестиционные сделки и сопровождение','Création de société, projets et investissements'),('legal','Вопросы к юристу','Questions juridiques','Любые вопросы к российскому юристу','Documents, contentieux et questions spécifiques')]
 s=heading(lang,'Выберите вид консультации' if ru else 'Choisissez votre consultation','Выберите направление, затем напишите нам. Стоимость, формат и объём согласуем до оплаты.' if ru else 'Choisissez un domaine. Nous confirmerons le format, le périmètre et le prix avant paiement.',LANGS[lang]['consult'])
 s+='<section class="sr-sec"><div class="sr-width"><div class="sr-contact-list">'
 for slug,r,f,rd,fd in entries:
  name=r if ru else f;summary=rd if ru else fd
  if ru:
   text=f'Здравствуйте! Обращаюсь с сайта SalutRussie. Тема: {name}. Хочу описать свою ситуацию и узнать о возможных вариантах помощи.'
   wa='https://wa.me/79685341915?text='+quote(text)
   subject=quote('Обращение с сайта SalutRussie — '+name)
   email='mailto:salutrussie@salutrussie.ru?subject='+subject+'&body='+quote(text)
   s+=f"""<details class="sr-contact-details"><summary class="sr-contact-choice"><strong>{esc(name)} <span aria-hidden="true">⌄</span></strong><span>{esc(summary)}</span></summary><div class="sr-contact-channels"><p>Выберите, как вам удобнее связаться с нами:</p><div class="sr-channel-links"><a href="{esc(wa)}" target="_blank" rel="noopener noreferrer" data-analytics-event="consultation_outbound">WhatsApp ↗</a><a href="https://t.me/lev_vt" target="_blank" rel="noopener noreferrer" data-analytics-event="consultation_outbound">Telegram ↗</a><a href="{esc(email)}" data-analytics-event="consultation_outbound">Электронная почта ↗</a></div><p class="sr-channel-caption">Для Telegram можно скопировать текст обращения и вставить его в переписку:</p><div class="sr-copy-row"><span class="sr-draft" id="draft-{slug}">{esc(text)}</span><button class="sr-button sr-copy-topic" type="button" data-copy-target="draft-{slug}" aria-label="Скопировать текст обращения">Скопировать текст</button></div></div></details>"""
  else:
   s+=f'<a class="sr-contact-choice" href="{link_msg(lang,name)}" target="_blank" rel="noopener" data-analytics-event="consultation_outbound"><strong>{esc(name)} ↗</strong><span>{esc(summary)}</span></a>'
 s+='</div><p class="sr-note">'+('Ваше обращение ни к чему вас не обязывает. Опишите свою ситуацию или задайте вопрос своими словами — так, как вам удобно. Если для решения вашего вопроса потребуется платная консультация или другая услуга, мы заранее сообщим вам стоимость.' if ru else 'Il s’agit d’une demande de consultation payante. Ne transmettez pas de documents sensibles lors du premier contact.')+'</p>'
 s+=f'<p style="margin-top:28px"><a class="btn btn-ghost" href="{path(lang,"pricing")}">{"Посмотреть действующие тарифы →" if ru else "Consulter les tarifs →"}</a></p></div></section>'
 return shell(lang,path(lang,'consultations'),'Консультации SalutRussie' if ru else 'Consultations SalutRussie','Миграционные, юридические, имущественные и бизнес-консультации' if ru else 'Consultations en immigration, immobilier, affaires et droit',s)

def knowledge(lang):
 ru=lang=='ru'
 s=heading(lang,'Полезная информация' if ru else 'Informations utiles','Экспертные статьи, практические инструкции и важные новости о России. Поиск по темам и содержанию материалов.' if ru else 'Analyses, guides pratiques et informations sur la vie en Russie. Recherchez par sujet.',LANGS[lang]['kb'])
 s+='<section class="sr-sec"><div class="sr-width"><div class="sr-section-head"><h2>'+('Найдите нужный материал' if ru else 'Rechercher une ressource')+'</h2></div>'
 s+=f'<label for="sr-search">{"Поиск по публикациям" if ru else "Recherche"}</label><div class="sr-search-bar"><input class="sr-input" id="sr-search" type="search" autocomplete="off" placeholder="{"Например: бизнес, РВП, аренда" if ru else "Ex. : entreprise, séjour, logement"}"></div>'
 topics=[('all','Все темы','Tous les sujets'),('migration','Миграция','Immigration'),('real-estate','Недвижимость','Immobilier'),('business','Бизнес','Entreprise'),('investments','Инвестиции','Investissements')]
 s+='<div class="sr-pills" role="group" aria-label="'+('Темы' if ru else 'Thèmes')+'">'
 for slug,r,f in topics:s+=f'<button type="button" class="sr-pill" data-topic-filter="{slug}" aria-pressed="{"true" if slug=="all" else "false"}">{esc(r if ru else f)}</button>'
 s+='</div><div class="sr-pills" role="group" aria-label="'+('Форматы' if ru else 'Formats')+'">'
 for slug,r,f in [('all','Все форматы','Tous les formats'),('guide','Инструкции','Guides'),('article','Статьи','Articles')]:s+=f'<button type="button" class="sr-pill" data-format-filter="{slug}" aria-pressed="{"true" if slug=="all" else "false"}">{esc(r if ru else f)}</button>'
 s+='</div><div id="sr-count" role="status" class="sr-results"></div><div class="sr-grid" id="sr-results">'
 for a in ARTICLES:
  title,summary,content=a[lang]
  blob=' '.join([title,summary,content,a['slug'],a['topic'], 'бизнес' if a['topic']=='business' else ''])
  href=path(lang,'knowledge/articles/'+a['slug'])
  s+=f'<a class="sr-card sr-result" data-topic="{a["topic"]}" data-format="{a["kind"]}" data-index="{esc(blob)}" href="{href}"><small>{"Инструкция" if a["kind"]=="guide" else "Статья" if ru else "Article"}</small><h3>{esc(title)}</h3><p>{esc(summary)}</p><span class="sr-link">{LANGS[lang]["more"]}</span></a>'
 s+='</div><div id="sr-empty" class="sr-kb-empty sr-hidden">'+('По запросу ничего не найдено.' if ru else 'Aucun résultat trouvé.')+'</div><p class="sr-note">'+('Материалы ниже — редакционные черновики для демонстрации структуры. Они требуют утверждения юристом перед индексацией и публикацией.' if ru else 'Contenus de démonstration en attente de validation juridique, non indexables avant révision.')+'</p></div></section>'
 return shell(lang,path(lang,'knowledge'),'Полезная информация' if ru else 'Informations utiles','Экспертные статьи и гайды для иностранцев в России' if ru else 'Ressources et guides pour les étrangers en Russie',s)

def article_page(lang,a):
 ru=lang=='ru';title,summary,content=a[lang];url=path(lang,'knowledge/articles/'+a['slug']);s=heading(lang,title,summary,'ПОЛЕЗНАЯ ИНФОРМАЦИЯ' if ru else 'INFORMATIONS UTILES')
 s+=f'<article class="sr-content"><p class="sr-meta">{"Авторское редактирование: ожидает проверки · Черновик" if ru else "Brouillon en attente de validation éditoriale"}</p><h2>{"Основные вопросы" if ru else "Points essentiels"}</h2><p>{esc(content)}</p><h2>{"Когда нужна консультация" if ru else "Quand demander une consultation ?"}</h2><p>{"Если вопрос касается конкретных документов, сроков, денег или правовых рисков, полезно проверить вашу ситуацию индивидуально. Материал не является юридическим заключением." if ru else "Une analyse individuelle reste utile pour toute situation particulière touchant aux documents, délais ou risques juridiques."}</p><p class="sr-note">{"Черновик. Не публиковать как актуальную юридическую консультацию без проверки правовых норм и источников." if ru else "Brouillon. Validation juridique et sources requises avant publication."}</p></article>'
 return shell(lang,url,title,summary,s+cta(lang),noindex=True,article=True)

def privacy(lang):
 ru=lang=='ru';title='Информация об обработке персональных данных' if ru else 'Informations relatives aux données personnelles';desc='Проект документа для утверждения до публикации.' if ru else 'Document à valider avant mise en ligne.'
 s=heading(lang,title,desc)
 if ru:
  s+=(
   '<article class="sr-content"><p class="sr-note">Проект уведомления для предварительной версии. Политика для рабочего сайта ожидает утверждения.</p>'
   '<h2>Что происходит на сайте</h2><p>На страницах этой сборки нет формы для отправки обращения. Подключённого счётчика аналитики в сборке нет.</p>'
   '<h2>Если вы решите связаться с бюро</h2><p>Кнопки консультаций открывают WhatsApp, Telegram или почтовое приложение. '
   'Для WhatsApp и почты подготовлен общий текст обращения. Вы отправляете сообщение в выбранном приложении самостоятельно. '
   'Кнопка копирования для Telegram помещает подготовленный текст в буфер обмена.</p>'
   '<h2>Внешние ресурсы</h2><p>Для оформления страницы браузер может загружать шрифты с серверов Google. '
   'При переходе в мессенджер или почтовое приложение применяются настройки и условия выбранного сервиса.</p></article>'
  )
  return shell(lang,path(lang,'privacy'),title,desc,s,noindex=True)
 s+=f'<div class="sr-content"><p class="sr-note">{"Этот документ — техническая заглушка, не окончательная политика. До публикации сайта требуется утвердить политику с учётом используемых сервисов, форм, аналитики и подрядчиков." if ru else "Ce document est provisoire et doit être remplacé par une politique de confidentialité approuvée avant publication."}</p><p>{"В этой демонстрационной версии нет серверной отправки анкет и подключённого счётчика аналитики. При выборе консультации открывается внешний мессенджер." if ru else "Cette démonstration ne collecte pas de formulaire sur serveur et n’intègre pas d’outil analytique. Les demandes ouvrent une messagerie externe."}</p></div>'
 return shell(lang,path(lang,'privacy'),title,desc,s,noindex=True)

# Artifact link map from original Claude export.
ART_IDS={
 '6hUsaDB4CnxVmsp2EzY2vS':'/ru/','4mFKDc1f9PXtRbxg5ZZM6C':'/ru/about/','2aaZWUad7RteGK6pSKaa3D':'/ru/pricing/','VGZwTntAAdTBeB8Fd8VQK3':'/ru/migration/decree-702/','Eo5w7Xa1pSC1q6cYRozSQU':'/ru/knowledge/','NXYMnECuMBM3JQ1TcRoKAN':'/ru/reviews/','5zyLAsXhvJBAvxfYcXn4Nh':'/ru/contacts/',
 'TZjXyuotSJ4s7XECiLWWJP':'/fr/','1mwfSGrrttteyxsVxjtyEy':'/fr/about/','9W499L6tAgXggYrVjeHyZh':'/fr/pricing/','2YmXFc7bmXWgzQafnSHpfS':'/fr/migration/decree-702/','H53fJMfBNKN5FvyxPvN7xS':'/fr/knowledge/','DHtunNSrBi7nxTWtzUtbi9':'/fr/reviews/','QmiuvCuK7Vx9kKgE4eLbro':'/fr/contacts/',
}

def legacy(lang,original,url,title,desc,placeholder=False):
 bs=BeautifulSoup((SRC/original).read_text(encoding='utf-8'),'html.parser')
 main=bs.find('main')
 if not main: raise RuntimeError('missing main: '+original)
 for a in main.find_all('a',href=True):
  href=a.get('href','')
  if 'claude.ai/artifact/' in href:
   aid=href.rstrip('/').split('/')[-1]
   a['href']=ART_IDS.get(aid,path(lang,'consultations'))
  if a.get('href')=='#':
   a['href']=path(lang,'knowledge')
   # remove fake "read more" links to replace with a readable landing rather than dead link
 for el in main.select('.news-card'):
  el.decompose() if placeholder else None
 if placeholder:
  z=knowledge(lang);return z
 # Remove top-level crumb and theme divs (shell recreates header/nav/footer)
 main['id']='main'
 # If original uses data-embedded image extract all to asset files.
 for idx,img in enumerate(main.select('img[src^="data:image"]')):
  kind,b64=img['src'].split(',',1);ext='jpg' if 'jpeg' in kind else 'png';asset=f'/assets/{lang}-{original.replace(".html","")}-{idx}.{ext}';(OUT/asset.lstrip('/')).write_bytes(base64.b64decode(b64));img['src']=asset
 for tag in main.select('script,style'):tag.decompose()
 content=''.join(map(str,main.contents))
 if original.startswith('tarify'):
  disclaimer=('Цены и условия — из исходного прототипа Claude (сентябрь 2026). Проверить актуальность и состав услуг перед публикацией.' if lang=='ru' else 'Tarifs issus de la version Claude (septembre 2026). À vérifier avant publication.')
  content=f'<div class="sr-width"><p class="sr-note">{disclaimer}</p></div>'+content
 if original.startswith('otzyvy'):
  content=f'<div class="sr-width"><p class="sr-note">{"Отзывы и материалы этой страницы требуют подтверждения перед публичным размещением." if lang=="ru" else "Les avis doivent être vérifiés avant toute publication."}</p></div>'+content
 return shell(lang,url,title,desc,content+cta(lang) if not original.startswith('kontakty') else content,noindex=original.startswith(('otzyvy','tarify')))

def write(url,content):
 folder=OUT/url.strip('/')
 folder.mkdir(parents=True,exist_ok=True)
 (folder/'index.html').write_text(content,encoding='utf-8')

for lang in ('ru','fr'):
 write(path(lang),home(lang));service_pages(lang)
 write(path(lang,'services'),services_ru() if lang=='ru' else basic_page(lang,path(lang,'services'),'Tous nos services','Choisissez le domaine qui correspond à votre projet.',list(SECTIONS.items())))
 write(path(lang,'consultations'),consultations(lang))
 write(path(lang,'knowledge'),knowledge(lang))
 for a in ARTICLES:write(path(lang,'knowledge/articles/'+a['slug']),article_page(lang,a))
 write(path(lang,'privacy'),privacy(lang))
 legacy_map={'ru':{'o-kompanii-ru.html':('about','О нас','Команда SalutRussie и наш подход к работе'), 'tarify-ru.html':('pricing','Тарифы','Тарифы и услуги SalutRussie'),'dekret-702-ru.html':('migration/decree-702','Указ 702','Переезд в Россию по Указу 702'),'kontakty-ru.html':('contacts','Контакты','Связаться со специалистами SalutRussie'),'otzyvy-ru.html':('reviews','Отзывы','Отзывы клиентов SalutRussie')},'fr':{'o-kompanii.html':('about','Notre équipe','Notre cabinet et notre méthode'),'tarify.html':('pricing','Tarifs','Les services et tarifs de SalutRussie'),'dekret-702.html':('migration/decree-702','Décret n° 702','S’installer en Russie avec le décret 702'),'kontakty.html':('contacts','Contact','Contactez SalutRussie'),'otzyvy.html':('reviews','Avis','Témoignages des clients SalutRussie')}}
 for old,(slug,title,desc) in legacy_map[lang].items():
  if slug=='reviews' and not REVIEWS_ENABLED:
   continue  # Hide unverified testimonials in both languages until owner approval.
  if lang=='ru' and slug=='pricing':
   write(path(lang,slug),pricing_ru())
   continue
  write(path(lang,slug),about_ru() if lang=='ru' and slug=='about' else legacy(lang,old,path(lang,slug),title,desc))

# All links and assets are converted to relative URLs so the full dist can be previewed directly by opening index.html.
all_pages=list(OUT.rglob('*.html'))
for file in all_pages:
 root_html=file.read_text(encoding='utf-8');prefix=os.path.relpath(OUT,file.parent).replace('\\','/')
 if prefix=='.':prefix='.'
 root_html=re.sub(r'(?<=["\'])/(assets|ru|fr)/',lambda m: prefix+'/'+m.group(0).lstrip('/'),root_html)
 file.write_text(root_html,encoding='utf-8')
landing='''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0;url=ru/index.html"><title>SalutRussie — открыть сайт</title></head><body><a href="ru/index.html">Открыть русскую версию SalutRussie</a> · <a href="fr/index.html">Version française</a></body></html>'''
(OUT/'index.html').write_text(landing,encoding='utf-8')
(OUT/'404.html').write_text('<!doctype html><html lang="ru"><meta charset="utf-8"><meta name="robots" content="noindex"><title>404</title><body>Страница не найдена. <a href="ru/index.html">Главная</a></body></html>',encoding='utf-8')
if PUBLIC:
 from xml.sax.saxutils import escape
 urls=[]
 for f in OUT.rglob('index.html'):
  if f==OUT/'index.html' or 'content="noindex' in f.read_text(encoding='utf-8'):continue
  u='/'+str(f.relative_to(OUT).parent).replace('\\','/')+'/'
  urls.append(u)
 xml='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join('<url><loc>'+escape(ORIGIN+u)+'</loc></url>\n' for u in sorted(urls))+'</urlset>'
 (OUT/'sitemap.xml').write_text(xml,encoding='utf-8')
 (OUT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+ORIGIN+'/sitemap.xml\n',encoding='utf-8')
else:
 (OUT/'robots.txt').write_text('User-agent: *\nDisallow: /\n# Preview only. Do not deploy as a public indexed release.\n',encoding='utf-8')
print('BUILD SUCCESS:',len(list(OUT.rglob('index.html'))),'pages, preview mode:',not PUBLIC)
