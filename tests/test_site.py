import unittest, re
from pathlib import Path
from urllib.parse import unquote
from site_html import BeautifulSoup
from zip_articles import EXPERT_ARTICLES
ROOT=Path(__file__).resolve().parents[1]/'dist'
class SiteTests(unittest.TestCase):
 def test_all_pages_well_formed(self):
  for file in ROOT.rglob('*.html'):
   with self.subTest(file=file):
    soup=BeautifulSoup(file.read_text(encoding='utf-8'),'html.parser')
    self.assertIsNotNone(soup.find('title'))
    self.assertIsNotNone(soup.find('html'))
    self.assertEqual(len(soup.select('h1')),0 if file in (ROOT/'index.html', ROOT/'404.html') else 1)
 def test_no_broken_internal_links(self):
  for file in ROOT.rglob('*.html'):
   soup=BeautifulSoup(file.read_text(encoding='utf-8'),'html.parser')
   for node in soup.select('[href],[src]'):
    v=node.get('href',node.get('src','')).split('#')[0].split('?')[0]
    if not v or re.match(r'^(https?\:|mailto\:|tel\:|data\:|javascript\:)',v):continue
    dest=((ROOT/unquote(v).lstrip('/')) if v.startswith('/') else (file.parent/unquote(v))).resolve()
    if dest.is_dir():dest=dest/'index.html'
    with self.subTest(file=file,link=v):self.assertTrue(dest.is_file(),str(dest))
 def test_approved_services_page_and_typography(self):
  page=BeautifulSoup((ROOT/'ru/services/index.html').read_text(encoding='utf-8'),'html.parser')
  self.assertEqual(page.h1.get_text(' ',strip=True),'Все услуги для иностранцев')
  self.assertEqual(len(page.select('.sr-services-grid>.sr-service-card')),6)
  self.assertEqual(len(page.select('.sr-services-grid>.sr-card--priority')),1)
  self.assertIn('Переезд в Россию',page.select_one('.sr-card--priority h3').get_text(' ',strip=True))
  decree=page.select_one('.sr-card--priority .sr-services-program')
  self.assertIsNotNone(decree)
  self.assertEqual(decree.get_text(' ',strip=True),'Переезд по Указу 702')
  self.assertTrue(decree.get('href','').endswith('/ru/migration/decree-702/'))
  self.assertIsNone(page.select_one('.sr-services-section .sr-section-head'))
  self.assertIn('От миграционной стратегии до недвижимости, бизнеса и юридической защиты',page.select_one('.sr-top p').get_text(' ',strip=True))
  self.assertIn('Не уверены, какая услуга вам нужна?',page.select_one('.sr-cta').get_text(' ',strip=True))
  self.assertEqual(len(page.select('.sr-services-pricing a[href]')),1)
  self.assertEqual(len(page.select('.sr-service-card>.sr-link[href]')),6)
  css=(ROOT/'assets/platform.css').read_text(encoding='utf-8')
  self.assertIn('html[lang="ru"]{--font-display:\'Inter\',sans-serif;--font-body:\'Inter\',sans-serif;}',css)
  self.assertIn('html[lang="ru"] .sr-services-grid{grid-template-columns:repeat(2,minmax(0,1fr));}',css)
  self.assertIn('html[lang="ru"] .sr-services-grid{grid-template-columns:minmax(0,1fr);gap:14px;}',css)
 def test_expanded_services_links_and_pages(self):
  page=BeautifulSoup((ROOT/'ru/services/index.html').read_text(encoding='utf-8'),'html.parser')
  cards={card.select_one('h3').get_text(' ',strip=True):card for card in page.select('.sr-services-grid>.sr-service-card')}
  expected={
   'Переезд в Россию':['Переезд по Указу 702','Визы в Россию','РВП в России','ВНЖ в России','Гражданство России','Защита в суде и государственных органах (МВД, ФСБ)'],
   'Бизнес в России':['Открытие компании','Юридическое сопровождение бизнеса','Налоговое консультирование'],
   'Инвестиции':['Юридическая проверка и сопровождение инвестиционного проекта','Подбор инвестиционных проектов'],
   'Юридическая помощь':['Консультации','Подготовка документов','Судебные споры'],
   'Переезд и адаптация':['Административные процедуры','Бытовые вопросы','Изучение русского языка']
  }
  for heading,labels in expected.items():
   with self.subTest(heading=heading):
    card=cards[heading]
    self.assertEqual([a.get_text(' ',strip=True) for a in card.select('ul li a')],labels)
    for a in card.select('ul li a'):
     self.assertTrue(a.has_attr('href'))
  for slug,title in [
   ('business/tax-consulting','Налоговое консультирование'),
   ('investments/project-selection','Подбор инвестиционных проектов'),
   ('relocation/administrative-procedures','Административные процедуры'),
   ('relocation/everyday-life','Бытовые вопросы'),
   ('relocation/russian-language','Изучение русского языка'),
   ('investments/legal-due-diligence','Юридическая проверка и сопровождение инвестиционного проекта')]:
   with self.subTest(slug=slug):
    p=ROOT/'ru'/slug/'index.html'
    self.assertTrue(p.is_file(),str(p))
    doc=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
    self.assertEqual(doc.h1.get_text(' ',strip=True),title)
    self.assertIsNotNone(doc.select_one('.sr-cta a[href]'))
  for slug,text in [('business','Налоговое консультирование'),('investments','Подбор инвестиционных проектов'),('relocation','Изучение русского языка')]:
   section=BeautifulSoup((ROOT/'ru'/slug/'index.html').read_text(encoding='utf-8'),'html.parser')
   self.assertIn(text,section.get_text(' ',strip=True))
 def test_migration_hub_wayfinding(self):
  page=BeautifulSoup((ROOT/'ru/migration/index.html').read_text(encoding='utf-8'),'html.parser')
  self.assertEqual(page.select_one('.sr-migration-top h1').get_text(' ',strip=True),'Переезд в Россию')
  self.assertIn('законный путь переезда',page.select_one('.sr-migration-top p').get_text(' ',strip=True))
  self.assertEqual(len(page.select('.sr-migration-feature')),1)
  self.assertIn('«Разделение ценностей»',page.select_one('.sr-migration-feature-aliases').get_text(' ',strip=True))
  self.assertIn('/migration/decree-702/',page.select_one('.sr-migration-feature')['href'])
  self.assertEqual(len(page.select('.sr-migration-service')),5)
  self.assertEqual([el.select_one('strong').get_text(' ',strip=True) for el in page.select('.sr-migration-service')],
   ['Визы в Россию','РВП в России','ВНЖ в России','Гражданство России','Защита в суде и государственных органах (МВД, ФСБ)'])
  self.assertEqual(len(page.select('.sr-migration-special-links a')),2)
  self.assertEqual(len(page.select('details.sr-migration-prep summary')),1)
  self.assertIn('планы своими словами',page.select_one('.sr-migration-prep').get_text(' ',strip=True))
  self.assertNotIn('Если семья переезжает из разных стран',page.get_text(' ',strip=True))
  self.assertEqual([el.select_one('strong').get_text(' ',strip=True) for el in page.select('.sr-migration-steps li')],['Разбираем ваши планы','Готовим миграционную стратегию','Сопровождаем до результата'])
  self.assertIn('Согласуем тариф',page.select_one('.sr-migration-route').get_text(' ',strip=True))
  self.assertEqual(len(page.select('.sr-migration-actions .btn')),1)
  self.assertEqual(len(page.select('.sr-migration-steps li')),3)
  self.assertEqual(len(page.select('.sr-migration-hub a[href]')),8)
  self.assertIsNone(page.select_one('.sr-migration-hub .sr-card'))
  self.assertEqual(len(page.select('.sr-migration-close a.btn[href]')),1)
  self.assertEqual(len(page.select('.sr-breadcrumbs')),1)
  self.assertEqual([el.get_text(' ',strip=True) for el in page.select('.sr-breadcrumbs a')],
   ['Главная','Все услуги'])
  self.assertIn('Лев Втюрин',page.select_one('.sr-migration-close').get_text(' ',strip=True))
 def test_all_ru_services_have_breadcrumbs(self):
  groups=['services','migration','real-estate','business','investments','legal','relocation']
  count=0
  for group in groups:
   root=ROOT/'ru'/group
   for file in root.rglob('index.html'):
    with self.subTest(page=file):
     page=BeautifulSoup(file.read_text(encoding='utf-8'),'html.parser')
     crumbs=page.select('.sr-breadcrumbs')
     self.assertEqual(len(crumbs),1)
     self.assertEqual(len(crumbs[0].select('[aria-current="page"]')),1)
     self.assertEqual(crumbs[0].select_one('a').get_text(' ',strip=True),'Главная')
     self.assertEqual(crumbs[0].select_one('[aria-current="page"]').get_text(' ',strip=True),page.h1.get_text(' ',strip=True) if group!='services' else 'Все услуги')
     self.assertLessEqual(len(crumbs[0].select('a')),3)
     count+=1
  self.assertGreaterEqual(count,29)
 def test_move_to_russia_multilingual_naming(self):
  ru=BeautifulSoup((ROOT/'ru/migration/index.html').read_text(encoding='utf-8'),'html.parser')
  fr=BeautifulSoup((ROOT/'fr/migration/index.html').read_text(encoding='utf-8'),'html.parser')
  self.assertEqual(ru.h1.get_text(' ',strip=True),'Переезд в Россию')
  self.assertEqual(fr.h1.get_text(' ',strip=True),'S’installer en Russie')
  self.assertIn('Мы поможем вам выбрать',ru.select_one('.sr-migration-top p').get_text(' ',strip=True))
  self.assertIn('«Разделение ценностей»',ru.select_one('.sr-migration-feature-aliases').get_text(' ',strip=True))
  self.assertIn('идеологическая программа',ru.select_one('.sr-migration-feature-aliases').get_text(' ',strip=True))
  cards=[a.select_one('strong').get_text(' ',strip=True) for a in ru.select('.sr-migration-service')]
  self.assertIn('Защита в суде и государственных органах (МВД, ФСБ)',cards)
  self.assertIn('Учёба в России и РВПО',ru.select_one('.sr-migration-special').get_text(' ',strip=True))
  self.assertIn('Расскажите о ваших планах.',ru.select_one('.sr-migration-close').get_text(' ',strip=True))
  self.assertNotIn('Если семья переезжает из разных стран',ru.get_text(' ',strip=True))
  with open(ROOT.parent/'docs/site-roadmap.md',encoding='utf-8') as roadmap:
   data=roadmap.read()
  self.assertIn('Фермерство в России',data)
 def test_russian_home_has_key_services(self):
  t=(ROOT/'ru/index.html').read_text()
  for needle in ['Недвижимость','Переезд в Россию','Инвестиции','Бизнес в России','Указ 702','Полезная информация','Консультация']:
   with self.subTest(needle=needle):self.assertIn(needle,t)
 def test_approved_russian_copy(self):
  root=ROOT/'ru/index.html'
  home=BeautifulSoup(root.read_text(), 'html.parser')
  self.assertEqual(home.h1.get_text(strip=True),'Живите, работайте и развивайте бизнес в России')
  self.assertIn('Мы помогаем иностранцам переехать в Россию, оформить РВП, ВНЖ и гражданство. Решаем сложные юридические вопросы, сопровождаем покупку недвижимости, инвестиции и открытие бизнеса.',home.select_one('.hero-lede').get_text(' ',strip=True))
  self.assertNotIn('Мы помогаем разобраться в вопросе и организовать профессиональное сопровождение.',home.get_text(' ',strip=True))
  for phrase in ['Выберите интересующее вас направление — мы подскажем, с чего начать','Переезд в Россию по Указу 702','Ваша заявка','План действий','Небольшая команда профессионалов: бутик, а не масс-маркет']:
   self.assertIn(phrase,home.get_text(' ',strip=True))
  self.assertNotIn('предложим партнёрскую услугу',home.get_text(' ',strip=True))
  self.assertIn('СПЕЦИАЛЬНАЯ ПРОГРАММА «РАЗДЕЛЕНИЕ ЦЕННОСТЕЙ»',home.get_text(' ',strip=True))
  self.assertIn('Разделение ценностей (идеологическая программа)',home.get_text(' ',strip=True))
  self.assertIn('специальной частной визы на срок до трёх месяцев',home.get_text(' ',strip=True))
  self.assertNotIn('постоянного проживания',home.select_one('.sr-feature').get_text(' ',strip=True))
  self.assertIn('Нужна помощь?',home.select_one('.sr-cta').get_text(' ',strip=True))
  self.assertIn('Указ 702 (разделение ценностей, идеологическая программа)',home.select_one('meta[name=description]')['content'])
  self.assertIn('Выберите направление консультации. Объём работы и стоимость согласуем.',home.select_one('.sr-cta').get_text(' ',strip=True))
 def test_approved_homepage_founder_and_navigation(self):
  home=BeautifulSoup((ROOT/'ru/index.html').read_text(encoding='utf-8'),'html.parser')
  self.assertEqual(len(home.select('main h1')),1)
  self.assertEqual(len(home.select('main .sr-founder-spot')),1)
  founder=home.select_one('.sr-founder-spot')
  self.assertIn('Лев Втюрин',founder.get_text(' ',strip=True))
  self.assertIn('Лично отвечаю за правовую стратегию и качество сопровождения каждого проекта.',founder.get_text(' ',strip=True))
  self.assertEqual(founder.select_one('img')['src'],'../assets/founder-lev-vtiurin-cutout-2026.webp')
  self.assertEqual(len(founder.select('.sr-founder-portrait-frame img')),1)
  self.assertTrue((ROOT/'assets/founder-lev-vtiurin-cutout-2026.webp').is_file())
  self.assertIn('Разрабатываем для вас индивидуальную стратегию',home.select_one('.sr-hero-method').get_text(' ',strip=True))
  self.assertNotIn('Сначала разрабатываем',home.select_one('.sr-hero-method').get_text(' ',strip=True))
  self.assertIn('сопровождаем вас на каждом этапе её реализации.',home.select_one('.sr-hero-method').get_text(' ',strip=True))
  self.assertEqual(home.select_one('.sr-hero-arrow').get_text(strip=True),'→')
  self.assertIn('Профессионально. Безопасно. Надёжно.',home.select_one('.sr-hero-values').get_text(' ',strip=True))
  self.assertEqual([a.get_text(' ',strip=True) for a in home.select('.hero-actions a')],['Получить консультацию →','Все услуги'])
  styles=(ROOT/'assets/platform.css').read_text(encoding='utf-8')
  self.assertIn('html[lang="ru"] .nav-links>li:first-child>.sr-drop-button',styles)
  self.assertIn('html[lang="ru"] .nav-links>li:nth-child(2)>a',styles)
  self.assertIn('@media(max-width:520px)',styles)
  self.assertIn('Homepage design iteration: readable Cyrillic',styles)
  self.assertIn('grid-template-columns:minmax(0,1fr) 230px',styles)
  self.assertIn('transform:scale(1)',styles)
  self.assertIn('@media(max-width:600px)',styles)
  self.assertIn('Editorial founder photo: transparent original',styles)
  self.assertIn('html[lang="ru"] .sr-founder-spot .sr-founder-portrait-frame',styles)
  self.assertIn('width:264px;height:282px;overflow:hidden;border:0;',styles)
  self.assertIn('html[lang="ru"] .sr-founder-spot{padding-bottom:0;}',styles)
  self.assertIn('grid-template-columns:264px minmax(0,1fr)',styles)
  self.assertIn('min-height:282px;overflow:hidden;padding:0 28px;border:0;box-shadow:none;background:transparent;',styles)
  self.assertIn('html[lang="ru"] .sr-founder-spot .sr-founder-portrait-frame{position:relative;',styles)

  self.assertIn('html[lang="ru"] .nav-links{font-size:15px;',styles)
  self.assertIn('html[lang="ru"] .nav-cta{font-size:14px;}',styles)
  self.assertIn('@media(max-width:1180px)',styles)
  self.assertIn('html[lang="ru"] .nav-links.open{max-height:80vh;overflow-y:auto;}',styles)
  self.assertEqual(home.h1.get_text(strip=True),'Живите, работайте и развивайте бизнес в России')
  self.assertIn('border-bottom:0;padding-bottom:0;',styles)
  self.assertIn('color:var(--cream-text-soft);letter-spacing:normal;',styles)
  self.assertIn('html[lang="ru"] .hero.v2-home .sr-hero-method{font-size:15px;line-height:1.55;}',styles)
  fr=BeautifulSoup((ROOT/'fr/index.html').read_text(encoding='utf-8'),'html.parser')
  self.assertFalse(fr.select('.sr-founder-spot'))
 def test_russian_about_founder_only(self):
  about=BeautifulSoup((ROOT/'ru/about/index.html').read_text(), 'html.parser')
  t=about.get_text(' ',strip=True)
  self.assertEqual(len(about.select('main img')),1)
  self.assertEqual(len(about.select('.sr-about-portrait img')),1)
  self.assertEqual(about.select_one('main img')['src'],'../../assets/founder-lev-vtiurin-cutout-2026.webp')
  for phrase in ['Миграционный юрист — основатель','Как устроено наше бюро','Единые стандарты работы','Философия и миссия SalutRussie','Безопасно и легально на каждом этапе']:
   self.assertIn(phrase,t)
  self.assertNotIn('Юлиан',t)
  for h in ['Статус и пребывание','Обустройство и повседневная жизнь','Бизнес и налоги']:
   self.assertIn(h,t)
 def test_russian_consultation_choices(self):
  cons=BeautifulSoup((ROOT/'ru/consultations/index.html').read_text(), 'html.parser')
  self.assertEqual(len(cons.select('details.sr-contact-details')),4)
  for det in cons.select('details.sr-contact-details'):
   self.assertEqual(len(det.select('.sr-channel-links a')),3)
   links=[a['href'] for a in det.select('.sr-channel-links a')]
   self.assertTrue(links[0].startswith('https://wa.me/'))
   self.assertEqual(links[1],'https://t.me/lev_vt')
   self.assertTrue(links[2].startswith('mailto:salutrussie@salutrussie.ru'))
   self.assertEqual(len(det.select('.sr-copy-topic')),1)
  t=cons.get_text(' ',strip=True)
  self.assertIn('Вопросы к юристу',t)
  self.assertIn('Любые вопросы к российскому юристу',t)
  self.assertIn('Ваше обращение ни к чему вас не обязывает',t)
 def test_french_consultation_channels(self):
  cons=BeautifulSoup((ROOT/'fr/consultations/index.html').read_text(), 'html.parser')
  self.assertEqual(len(cons.select('details.sr-contact-details')),4)
  for det in cons.select('details.sr-contact-details'):
   links=[a['href'] for a in det.select('.sr-channel-links a')]
   self.assertEqual(len(links),3)
   self.assertTrue(links[0].startswith('https://wa.me/'))
   self.assertEqual(links[1],'https://t.me/lev_vt')
   self.assertTrue(links[2].startswith('mailto:salutrussie@salutrussie.ru'))
   self.assertEqual(det.select_one('.sr-copy-topic').get_text(strip=True),'Copier le texte')
  self.assertIn("fr?'Copié':'Скопировано'",(ROOT/'assets/platform.js').read_text())
 def test_russian_footer(self):
  for f in (ROOT/'ru').rglob('index.html'):
   with self.subTest(page=str(f)):
    footer=BeautifulSoup(f.read_text(),'html.parser').footer.get_text(' ',strip=True)
    self.assertIn('© 2018–2026 SalutRussie',footer)
    self.assertNotIn('Состав и исполнитель услуги',footer)
    self.assertIn('Профессиональная помощь для иностранцев в России',footer)
    self.assertNotIn('SalutRussie — профессиональная помощь',footer)
 def test_languages(self):
  self.assertTrue((ROOT/'fr/index.html').exists())
  self.assertTrue((ROOT/'ru/index.html').exists())
  self.assertTrue((ROOT/'fr/knowledge/index.html').exists())
 def test_search_in_place(self):
  k=(ROOT/'ru/knowledge/index.html').read_text()
  for needle in ['id="sr-search"','data-topic-filter="business"','data-format-filter="guide"','data-index=', 'starting-a-business']:
   self.assertIn(needle,k)
 def test_preview_never_indexed(self):
  for file in ROOT.rglob('index.html'):
   self.assertIn('noindex',(file).read_text())
  self.assertIn('Disallow: /',(ROOT/'robots.txt').read_text())
 def test_no_claude_artifact_links(self):
  for f in ROOT.rglob('*.html'):
   self.assertNotIn('claude.ai/artifact/',f.read_text(),str(f))
 def test_placeholder_reviews_not_published(self):
  for lang in ('ru','fr'):
   self.assertFalse((ROOT/lang/'reviews/index.html').exists())
  for file in ROOT.rglob('*.html'):
   with self.subTest(file=file):
    text=file.read_text(encoding='utf-8')
    self.assertNotIn('Текст отзыва — сюда',text)
    soup=BeautifulSoup(text,'html.parser')
    for a in soup.select('a[href]'):
     self.assertNotRegex(a['href'],r'(^|/)reviews(/|$)')
 def test_escape_restores_submenu_aria(self):
  js=(ROOT/'assets/platform.js').read_text(encoding='utf-8')
  self.assertIn("x.querySelector('.sr-drop-button')?.setAttribute('aria-expanded','false')",js)
  self.assertIn('if(burger && menu)',js)
 def test_business_routes_and_language_switch(self):
  for lang in ('ru','en','fr'):
   for tail in ('','employers/','recruitment-partners/'):
    with self.subTest(lang=lang,tail=tail):
     route=f'{lang}/for-business/{tail}'
     soup=BeautifulSoup((ROOT/route/'index.html').read_text(encoding='utf-8'))
     self.assertEqual(soup.html.get('lang'),lang)
     self.assertEqual(len(soup.select('h1')),1)
     links={x.get_text(strip=True):x.get('href') for x in soup.select('.lang-switch a')}
     for peer in ('ru','en','fr'):
      self.assertIn(peer.upper(),links)
      self.assertIn(f'{peer}/for-business/{tail}',links[peer.upper()])
     self.assertNotIn('536',soup.main.get_text(' ',strip=True))
     if tail:
      self.assertGreater(len(soup.main.get_text(' ',strip=True)),700)
 def test_edited_legal_content_and_french_consistency(self):
  for lang in ('ru','fr'):
   decree=BeautifulSoup((ROOT/lang/'migration/decree-702/index.html').read_text())
   if lang=='ru':
    self.assertIn('garant.ru/products/ipo/prime/doc/409448235/',str(decree.main))
    self.assertIn('garant.ru/products/ipo/prime/doc/410316959/',str(decree.main))
    self.assertIn('cons_doc_LAW_37868',str(decree.main))
   else:
    self.assertIn('publication.pravo.gov.ru/document/0001202408190001',str(decree.main))
    self.assertIn('publication.pravo.gov.ru/document/0001202409200036',str(decree.main))
   self.assertNotIn('гарантированная виза',decree.main.get_text(' ',strip=True).lower())
   for slug in ('how-to-choose-residence','renting-a-home','starting-a-business','investor-checklist'):
    with self.subTest(lang=lang,slug=slug):
     article=BeautifulSoup((ROOT/lang/'knowledge/articles'/slug/'index.html').read_text())
     self.assertIn('2026',article.main.get_text(' ',strip=True))
     self.assertIsNotNone(article.select_one('article table'))
     self.assertIsNotNone(article.select_one('article details'))
     self.assertTrue(any(a.get('href','').startswith('http') for a in article.select('article a[href]')))
  about=(ROOT/'fr/about/index.html').read_text()
  self.assertNotIn('Yuliana',about)
  self.assertNotIn('Avocat en immigration',about)
  pricing=BeautifulSoup((ROOT/'fr/pricing/index.html').read_text())
  self.assertNotIn('₽',pricing.main.get_text(' ',strip=True))
  self.assertNotIn('Khlebnikova', (ROOT/'fr/contacts/index.html').read_text())
 def test_article_tables_have_keyboard_scroll_regions(self):
  for lang in ('ru','fr'):
   for slug in ('how-to-choose-residence','renting-a-home','starting-a-business','investor-checklist'):
    with self.subTest(lang=lang,slug=slug):
     article=BeautifulSoup((ROOT/lang/'knowledge/articles'/slug/'index.html').read_text())
     tables=article.select('article table')
     regions=article.select('article .sr-table-scroll[tabindex="0"]')
     self.assertEqual(len(tables),len(regions))
     self.assertTrue(all(region.get('role')=='region' and region.get('aria-label') for region in regions))
 def test_ten_complete_expert_articles(self):
  self.assertEqual(len(EXPERT_ARTICLES),10)
  listing=BeautifulSoup((ROOT/'ru/knowledge/index.html').read_text(encoding='utf-8'))
  for item in EXPERT_ARTICLES:
   slug=item['slug']
   with self.subTest(slug=slug):
    page=BeautifulSoup((ROOT/'ru/knowledge/articles'/slug/'index.html').read_text(encoding='utf-8'))
    self.assertEqual(len(page.select('h1')),1)
    self.assertGreater(len(page.select_one('.expert-article').get_text(' ',strip=True).split()),1400)
    self.assertGreaterEqual(len(page.select('.expert-toc a[href^="#"]')),10)
    self.assertGreaterEqual(len(page.select('.expert-process li')),5)
    ids={node.get('id') for node in page.select('[id]')}
    self.assertTrue(all(a['href'][1:] in ids for a in page.select('.expert-toc a[href^="#"]')))
    self.assertTrue(any(a.get('href','').startswith('https://') for a in page.select('.expert-article a[href]')))
    self.assertTrue(any(f'/{slug}/' in a.get('href','') for a in listing.select('a[href]')))
    self.assertIn('/fr/knowledge/',str(page.select_one('.lang-switch')))
    self.assertFalse((ROOT/'fr/knowledge/articles'/slug/'index.html').exists())
 def test_decree_702_russian_service_journey(self):
  page=BeautifulSoup((ROOT/'ru/migration/decree-702/index.html').read_text(encoding='utf-8'),'html.parser')
  self.assertEqual(len(page.select('main h1')),1)
  self.assertIn('Переезд в Россию по указу 702',page.title.get_text())
  for anchor in ('step0','step1','step2','step3','step4','life','faq702'):
   with self.subTest(anchor=anchor):
    self.assertIsNotNone(page.select_one(f'#{anchor}'))
  self.assertEqual(len(page.select('article .sr702-with-image img')),4)
  self.assertEqual(len(page.select('.sr702-visa-figure .sr702-visa-crop img')),1)
  self.assertEqual(len(page.select('dialog#sr702-visa-dialog')),0)
  self.assertEqual(len(page.select('[data-sr702-visa-open]')),0)
  self.assertIn('Получите при въезде и сохраните миграционную карту. Не теряйте её.',page.main.get_text(' ',strip=True))
  self.assertIn('Нотариальный перевод на русский язык вы сделаете уже в России.',page.main.get_text(' ',strip=True))
  self.assertNotIn('и нотариальным переводом на русский язык',page.main.get_text(' ',strip=True))
  self.assertEqual(len(page.select('.sr702-visual-crop')),2)
  self.assertIn('ИДЕОЛОГИЧЕСКАЯ ПРОГРАММА',page.select_one('.sr-top .sr-eyebrow').get_text(' ',strip=True))
  self.assertNotIn('Обновлено 23 ноября',page.main.get_text(' ',strip=True))
  self.assertEqual(len(page.select('#faq702 details')),6)
  self.assertGreaterEqual(len(page.select('article .sr702-stage details')),10)
  self.assertTrue(any('rvp-shared-values-702' in a.get('href','') for a in page.select('article a[href]')))
  self.assertTrue(any('consultations' in a.get('href','') for a in page.select('article a[data-analytics-event="consultation_click"]')))
  self.assertIn('https://www.garant.ru/products/ipo/prime/doc/410316959/',str(page.main))
  self.assertIn('30 суток',page.main.get_text(' ',strip=True))
  self.assertIn('на три месяца',page.main.get_text(' ',strip=True))
  self.assertNotIn('консульство обязано',page.main.get_text(' ',strip=True).lower())
  self.assertNotIn('1126',page.main.get_text(' ',strip=True))
  self.assertIn('noindex',page.select_one('meta[name="robots"]')['content'])

if __name__=='__main__':unittest.main()
