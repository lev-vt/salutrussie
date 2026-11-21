"""Check the generated public build without publishing it."""

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import unquote, urlparse
from xml.etree import ElementTree

from site_html import BeautifulSoup


root = Path(sys.argv[1] if len(sys.argv) > 1 else 'build/release-check').resolve()
assert (root / 'sitemap.xml').is_file(), 'Build the release-check variant first'
tree = ElementTree.parse(root / 'sitemap.xml')
urls = {node.text for node in tree.findall('.//{*}loc')}
assert urls, 'Empty sitemap'
origin = urlparse(next(iter(urls))).scheme + '://' + urlparse(next(iter(urls))).netloc
assert origin.startswith('https://'), 'Public origin must use HTTPS'
assert 'Allow: /' in (root / 'robots.txt').read_text(encoding='utf-8')

issues = []
titles = defaultdict(list)
descriptions = defaultdict(list)
indexed = set()
pages = [p for p in root.rglob('index.html') if p != root / 'index.html']
for file in pages:
    route = '/' + str(file.relative_to(root).parent) + '/'
    html = file.read_text(encoding='utf-8')
    if 'fonts.googleapis.com' in html or 'fonts.gstatic.com' in html:
        issues.append(f'{route}: external font request')
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.title.get_text(strip=True) if soup.title else ''
    description = soup.select_one('meta[name=description]')
    description = description.get('content', '') if description else ''
    titles[title].append(route)
    descriptions[description].append(route)
    if len(soup.select('h1')) != 1:
        issues.append(f'{route}: expected exactly one H1')
    if len(soup.select('main')) != 1:
        issues.append(f'{route}: expected exactly one main landmark')
    identifiers = [node.get('id') for node in soup.select('[id]')]
    if any(count > 1 for count in Counter(identifiers).values()):
        issues.append(f'{route}: duplicate element ID')
    for image in soup.select('img'):
        if image.get('alt') is None or not image.get('width') or not image.get('height'):
            issues.append(f'{route}: image missing alt or dimensions')
    for control in soup.select('a[href],button'):
        if not control.get_text(' ', strip=True) and not control.get('aria-label') and not control.select('img[alt]'):
            issues.append(f'{route}: control without accessible name')
    previous_level = 1
    for heading in soup.select('h1,h2,h3,h4,h5,h6'):
        level = int(heading.name[1])
        if level > previous_level + 1:
            issues.append(f'{route}: heading level jumps from {previous_level} to {level}')
        previous_level = level
    if len(description) < 45 or len(description) > 240:
        issues.append(f'{route}: description length {len(description)}')
    lang = soup.html.get('lang') if soup.html else None
    if lang not in ('ru', 'fr', 'en') or not route.startswith('/' + lang + '/'):
        issues.append(f'{route}: language mismatch')
    canonical = soup.select_one('link[rel=canonical]')
    if canonical is None or canonical.get('href') != origin + route:
        issues.append(f'{route}: canonical mismatch')
    robots = soup.select_one('meta[name=robots]')
    is_indexed = robots is not None and robots.get('content') == 'index,follow'
    if is_indexed:
        indexed.add(origin + route)
        peers = ('ru', 'fr', 'en') if '/for-business/' in route else ('ru', 'fr')
        alternates = {a.get('hreflang'): a.get('href') for a in soup.select('link[rel=alternate]')}
        for peer in peers:
            expected = origin + '/' + peer + route[3:]
            if alternates.get(peer) != expected:
                issues.append(f'{route}: {peer} hreflang mismatch')
    elif route not in ('/ru/privacy/', '/fr/privacy/'):
        issues.append(f'{route}: unexpected noindex')
    for script in soup.select('script[type="application/ld+json"]'):
        try:
            data = json.loads(script.get_text())
            if data.get('url') != origin + route:
                issues.append(f'{route}: structured data URL mismatch')
        except json.JSONDecodeError:
            issues.append(f'{route}: invalid structured data')
    for node in soup.select('[href],[src]'):
        href = node.get('href', node.get('src', ''))
        if not href or urlparse(href).scheme or href.startswith('//') or href.startswith('#'):
            continue
        local = (file.parent / unquote(href.split('#')[0].split('?')[0])).resolve()
        if local.is_dir():
            local /= 'index.html'
        if not local.is_file() or not local.is_relative_to(root):
            issues.append(f'{route}: broken local link {href}')

for css in (root / 'assets').glob('*.css'):
    for value in re.findall(r'url\(([^)]+)\)', css.read_text(encoding='utf-8')):
        value = value.strip().strip('"\'')
        if urlparse(value).scheme or value.startswith('//'):
            issues.append(f'{css.name}: external CSS asset {value}')
            continue
        target = (css.parent / value).resolve()
        if not target.is_file() or not target.is_relative_to(root):
            issues.append(f'{css.name}: broken CSS asset {value}')

for label, values in (('title', titles), ('description', descriptions)):
    for text, paths in values.items():
        if not text or len(paths) > 1:
            issues.append(f'{label} duplicated or empty: {paths}')
if urls != indexed:
    issues.append(f'sitemap mismatch: {len(urls)} listed, {len(indexed)} indexed')
if issues:
    raise SystemExit('\n'.join(issues))
print(f'RELEASE VERIFIED: {len(pages)} pages, {len(indexed)} indexed URLs, links, SEO and basic accessibility valid')
