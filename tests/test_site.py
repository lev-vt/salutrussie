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
 def test_russian_home_has_key_services(self):
  t=(ROOT/'ru/index.html').read_text()
  for needle in ['Недвижимость','Миграция','Инвестиции','Бизнес в России','Указ 702','Полезная информация','Консультация']:
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
if __name__=='__main__':unittest.main()
