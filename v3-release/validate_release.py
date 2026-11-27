#!/usr/bin/env python3
"""Validate a locally built SalutRussie release. No network or deployment."""
import argparse
import hashlib
import json
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, unquote, urljoin, urlsplit
from xml.etree import ElementTree


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.canonical = []
        self.alternates = []
        self.robots = []
        self.links = []
        self.schemas = []
        self.h1 = 0
        self.lang = None
        self.in_schema = False
        self.buffer = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'html':
            self.lang = a.get('lang')
        if tag == 'h1':
            self.h1 += 1
        if tag == 'meta' and a.get('name', '').lower() == 'robots':
            self.robots.append(a.get('content', ''))
        if tag == 'link':
            rel = a.get('rel', '').lower().split()
            if 'canonical' in rel:
                self.canonical.append(a.get('href'))
            if 'alternate' in rel and 'hreflang' in a:
                self.alternates.append((a['hreflang'], a.get('href')))
        for key in ('href', 'src', 'poster'):
            if a.get(key):
                self.links.append(a[key])
        if tag == 'script' and a.get('type') == 'application/ld+json':
            self.in_schema = True
            self.buffer = []

    def handle_data(self, data):
        if self.in_schema:
            self.buffer.append(data)

    def handle_endtag(self, tag):
        if tag == 'script' and self.in_schema:
            self.schemas.append(''.join(self.buffer))
            self.in_schema = False


def validate(root, base, routes, excluded, indexing):
    errors = []
    languages = tuple(lang for lang in ('ru', 'en', 'fr', 'de') if lang + '/' in routes)
    base_parts = urlsplit(base)
    def fail(route, msg):
        errors.append(f'{route or "/"}: {msg}')
    def local_file(url):
        p = urlsplit(url)
        if p.scheme not in ('http', 'https') or p.netloc != base_parts.netloc:
            return None
        if not p.path.startswith(base_parts.path):
            return False
        rel = unquote(p.path[len(base_parts.path):])
        target = (root / rel).resolve()
        if target != root and root not in target.parents:
            return False
        if target.is_dir():
            target /= 'index.html'
        return target.is_file()
    def check_schema(node, route):
        if isinstance(node, list):
            for value in node:
                check_schema(value, route)
        elif isinstance(node, dict):
            for key, value in node.items():
                if key in ('@id', 'url', 'image', 'item') and isinstance(value, str):
                    if not urlsplit(value).scheme:
                        fail(route, f'relative schema {key}: {value}')
                    elif local_file(value) is False:
                        fail(route, f'missing schema target: {value}')
                else:
                    check_schema(value, route)
    expected_sitemap = set()
    asset_hashes = {}
    pages = [''] + sorted(routes)
    for route in pages:
        path = root / route / 'index.html'
        if not path.is_file():
            fail(route, 'missing HTML'); continue
        page = Page()
        page.feed(path.read_text(encoding='utf-8'))
        canonical = base + route
        suffix = route.split('/', 1)[1] if route else ''
        indexable = indexing and suffix not in excluded
        if indexable:
            expected_sitemap.add(canonical)
        if page.canonical != [canonical]:
            fail(route, f'incorrect canonical: {page.canonical}')
        expected_robots = 'index,follow' if indexable else ('noindex,follow' if indexing else 'noindex,nofollow')
        if page.robots != [expected_robots]:
            fail(route, f'incorrect robots: {page.robots}')
        if page.h1 != 1:
            fail(route, f'expected one H1, got {page.h1}')
        if route and page.lang != route.split('/')[0]:
            fail(route, f'incorrect HTML language: {page.lang}')
        expected_alts = []
        if suffix not in excluded:
            expected_alts = [(l, base + l + '/' + suffix) for l in languages if l + '/' + suffix in routes]
            if not suffix:
                expected_alts.append(('x-default', base))
        if Counter(page.alternates) != Counter(expected_alts):
            fail(route, f'incorrect hreflang: {page.alternates}')
        for link in set(page.links):
            if link.startswith('#'):
                continue
            target_url = urljoin(canonical, link)
            if local_file(target_url) is False:
                fail(route, f'missing local target: {link}')
            target = urlsplit(target_url)
            name = Path(target.path).name.lower()
            if target.netloc == base_parts.netloc and (name.endswith(('.css', '.js')) or name.startswith('favicon.')):
                asset = root / unquote(target.path[len(base_parts.path):])
                if asset.is_file():
                    if asset not in asset_hashes:
                        asset_hashes[asset] = hashlib.sha256(asset.read_bytes()).hexdigest()[:12]
                    if parse_qs(target.query).get('v') != [asset_hashes[asset]]:
                        fail(route, f'incorrect asset version: {link}')
        for schema in page.schemas:
            try:
                check_schema(json.loads(schema), route)
            except ValueError as exc:
                fail(route, f'invalid JSON-LD: {exc}')
    redirect = root / 'ru/migration/decree-702-design/index.html'
    if redirect.exists() and 'noindex' not in redirect.read_text(encoding='utf-8').lower():
        fail('ru/migration/decree-702-design/', 'legacy redirect must stay noindex')
    sitemap = root / 'sitemap.xml'
    robots = root / 'robots.txt'
    if not robots.is_file():
        fail('', 'missing robots.txt')
    if indexing:
        if not sitemap.is_file():
            fail('', 'missing sitemap.xml')
        else:
            try:
                locs = [n.text for n in ElementTree.parse(sitemap).findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
                if len(locs) != len(set(locs)) or set(locs) != expected_sitemap:
                    fail('', f'sitemap mismatch: missing {sorted(expected_sitemap - set(locs))}; extra {sorted(set(locs) - expected_sitemap)}')
            except ElementTree.ParseError as exc:
                fail('', f'invalid sitemap XML: {exc}')
        if robots.is_file() and f'Sitemap: {base}sitemap.xml' not in robots.read_text(encoding='utf-8'):
            fail('', 'robots.txt does not reference production sitemap')
    elif sitemap.exists():
        fail('', 'review copy must not contain a sitemap')
    return errors, len(pages), len(expected_sitemap)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', required=True, type=Path)
    p.add_argument('--site-url', required=True)
    p.add_argument('--indexable', action='store_true', help='Validate an explicitly approved indexable release')
    args = p.parse_args()
    base = args.site_url.rstrip('/') + '/'
    u = urlsplit(base)
    if u.scheme != 'https' or not u.hostname or u.query or u.fragment or u.username:
        p.error('Use an absolute HTTPS site URL.')
    manifest = json.loads(Path(__file__).with_name('v3-seo-manifest.json').read_text(encoding='utf-8'))
    errors, pages, sitemap = validate(args.root.resolve(), base, set(manifest['routes']), set(manifest['excludedFromSitemap']), args.indexable)
    for error in errors:
        print('ERROR:', error)
    print(f'Checked {pages} HTML pages; expected sitemap entries: {sitemap}; errors: {len(errors)}')
    raise SystemExit(bool(errors))

if __name__ == '__main__':
    main()
