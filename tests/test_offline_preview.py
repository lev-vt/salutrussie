import re,unittest
from pathlib import Path
from urllib.parse import urlsplit,unquote
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]/'preview_offline'
class OfflinePreviewTests(unittest.TestCase):
 def test_every_local_link_opens_exact_file_without_webserver(self):
  if not ROOT.is_dir():self.skipTest('Run make_offline_preview.py first')
  count=0
  for file in ROOT.rglob('*.html'):
   soup=BeautifulSoup(file.read_text(encoding='utf-8'),'html.parser')
   for node in soup.select('a[href],link[href],script[src],img[src]'):
    val=node.get('href',node.get('src',''))
    u=urlsplit(val)
    if u.scheme or u.netloc or not u.path or u.path.startswith('#'):continue
    dest=(file.parent/unquote(u.path)).resolve()
    with self.subTest(page=str(file.relative_to(ROOT)),link=val):
     self.assertTrue(dest.is_relative_to(ROOT.resolve()))
     self.assertTrue(dest.is_file(),f'Missing file: {dest}')
    count+=1
  self.assertGreater(count,1500)
 def test_opening_instructions_survive_rebuild(self):
  name="НАЧНИТЕ_ЗДЕСЬ.txt"
  self.assertEqual((ROOT/name).read_bytes(), (ROOT.parent/"src"/name).read_bytes())
 def test_primary_preview_links_are_to_html_files(self):
  soup=BeautifulSoup((ROOT/'ru/index.html').read_text(),'html.parser')
  for a in soup.select('a[href]'):
   u=urlsplit(a['href'])
   if u.path and not u.scheme and not u.netloc:
    self.assertFalse(u.path.endswith('/'),a['href'])
  self.assertIn('index.html',soup.select_one('.nav-cta')['href'])
if __name__=='__main__':unittest.main()
