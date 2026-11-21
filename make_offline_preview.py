#!/usr/bin/env python3
"""Make a file://-navigable preview from dist, without changing the production build.

Run build.py first, then run this script. The resulting `preview_offline/index.html`
works by double-click on macOS/Windows, including internal page navigation.
"""
from pathlib import Path
import re, shutil
from urllib.parse import urlsplit, urlunsplit, unquote

ROOT=Path(__file__).resolve().parent
SRC=ROOT/'dist'
DST=ROOT/'preview_offline'
if not (SRC/'index.html').is_file(): raise SystemExit('Build the site with python3 build.py first')
if DST.exists():shutil.rmtree(DST)
shutil.copytree(SRC,DST)
shutil.copyfile(ROOT/'src'/'НАЧНИТЕ_ЗДЕСЬ.txt',DST/'НАЧНИТЕ_ЗДЕСЬ.txt')
changed=0
for f in DST.rglob('*.html'):
 text=f.read_text(encoding='utf-8')
 if f==DST/'404.html':
  text=text.replace('href="/ru/"','href="ru/index.html"')
 def fix(match):
  global changed
  attr,quote,value=match.groups()
  parts=urlsplit(value)
  if parts.scheme or parts.netloc or not parts.path.endswith('/') or parts.path.startswith('//'):
   return match.group(0)
  # In file:// mode browsers do not reliably load index.html for directory URLs.
  target=(f.parent/unquote(parts.path)).resolve()
  if not target.is_relative_to(DST.resolve()) or not (target/'index.html').is_file():
   raise ValueError(f'Missing local page: {f.relative_to(DST)} -> {value}')
  newpath=parts.path+'index.html'
  fixed=urlunsplit(('', '', newpath, parts.query, parts.fragment))
  changed+=1
  return f'{attr}={quote}{fixed}{quote}'
 text=re.sub(r'\b(href|src)=(\"|\')(.*?)\2',fix,text,flags=re.I|re.S)
 f.write_text(text,encoding='utf-8')
print('OFFLINE PREVIEW READY:',len(list(DST.rglob('*.html'))),'HTML files,',changed,'directory links rewritten')
