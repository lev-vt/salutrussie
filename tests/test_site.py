import unittest, re
from pathlib import Path
from urllib.parse import unquote
from bs4 import BeautifulSoup
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
    dest=(file.parent/unquote(v)).resolve()
    if dest.is_dir():dest=dest/'index.html'
    with self.subTest(file=file,link=v):self.assertTrue(dest.is_file(),str(dest))
 def test_russian_home_has_key_services(self):
  t=(ROOT/'ru/index.html').read_text()
  for needle in ['Недвижимость','Миграция','Инвестиции','Бизнес в России','Указу № 702','Полезная информация','Консультация']:
   with self.subTest(needle=needle):self.assertIn(needle,t)
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
if __name__=='__main__':unittest.main()
