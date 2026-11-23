#!/usr/bin/env python3
"""SalutRussie static builder. Preserves Claude source while making a unified platform.
Run: python3 build.py. Python standard library only.
Local release check: BUILD_VARIANT=release-check SITE_ORIGIN=https://example.invalid PUBLIC_RELEASE=1 python3 build.py
"""
from __future__ import annotations
import base64, json, os, re, shutil, html
from pathlib import Path
from urllib.parse import quote
from site_html import BeautifulSoup
from b2b_content import get_page
from articles_content import ARTICLES_HTML
from article_addenda import ADDENDA
from service_content import rich_section
from subpage_content import DETAILS, detail_rich
from legal_site_content import provider_block, provider_footer, LEGAL_CSS, data_notice
from zip_articles import EXPERT_ARTICLES, render_expert_article, expert_article_schema

# Owner-approved temporary hold: do not generate placeholder testimonials.
# Original Claude review templates remain preserved in src/original/.
REVIEWS_ENABLED = False

ROOT=Path(__file__).resolve().parent
SRC=ROOT/'src'/'original'
OUT=ROOT/'build'/'release-check' if os.getenv('BUILD_VARIANT')=='release-check' else ROOT/'dist'
ORIGIN=os.getenv('SITE_ORIGIN','').rstrip('/')
PUBLIC=os.getenv('PUBLIC_RELEASE')=='1' and ORIGIN.startswith('https://')
if os.getenv('BUILD_VARIANT') not in (None,'release-check'): raise SystemExit('Unsupported BUILD_VARIANT')
if os.getenv('PUBLIC_RELEASE')=='1' and not PUBLIC: raise SystemExit('PUBLIC_RELEASE requires HTTPS SITE_ORIGIN')
OUT.mkdir(parents=True,exist_ok=True)
for f in OUT.iterdir():
    if f.is_dir():shutil.rmtree(f)
    else:f.unlink()
(OUT/'assets').mkdir()
(OUT/'assets'/'fonts').mkdir()
for font_file in (ROOT/'src'/'fonts').iterdir():
    if font_file.suffix in ('.woff2','.txt'):
        shutil.copy2(font_file,OUT/'assets'/'fonts'/font_file.name)
shutil.copy2(ROOT/'src'/'fonts'/'fonts.css',OUT/'assets'/'fonts.css')
shutil.copy2(ROOT/'src'/'founder-lev-vtiurin-2026.webp',OUT/'assets'/'founder-lev-vtiurin-2026.webp')
shutil.copy2(ROOT/'src'/'founder-lev-vtiurin-cutout-2026.webp',OUT/'assets'/'founder-lev-vtiurin-cutout-2026.webp')
# User-supplied Decree 702 artwork: exact original files, no retouching or encoding.
for artwork in ('decree702-stage1-visa.jpg','decree702-stage2-arrival.jpg','decree702-stage3-documents.png','decree702-stage4-mvd.png'):
    artwork_path=ROOT/'src'/artwork
    if artwork_path.is_file():
        shutil.copy2(artwork_path,OUT/'assets'/artwork)

(OUT/'assets'/'favicon.svg').write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-label="SalutRussie">
<rect width="64" height="64" rx="12" fill="#131B2E"/>
<circle cx="32" cy="32" r="25" fill="none" stroke="#A9803E" stroke-width="1.5"/>
<circle cx="32" cy="32" r="20" fill="none" stroke="#A9803E" stroke-width=".7"/>
<text x="32" y="39" text-anchor="middle" font-family="Georgia,serif" font-size="20" fill="#F1ECDE">SR</text>
</svg>''',encoding='utf-8')
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
.sr-skip {position:absolute;left:16px;top:-100px;z-index:200;padding:10px 14px;background:#131B2E;color:#F1ECDE;border:2px solid #A9803E;text-decoration:none;}
.sr-skip:focus {top:12px;}
:where(a,button,summary,input,select,textarea,[tabindex="0"]):focus-visible {outline:3px solid #8F651E;outline-offset:3px;}
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
.sr-content h3 {font-size:20px;margin:24px 0 10px;}
.sr-content ol {margin:0 0 26px;padding-left:24px;line-height:1.8;}
.sr-content table {border-collapse:collapse;width:100%;margin:25px 0;line-height:1.5;}
.sr-table-scroll {max-width:100%;overflow-x:auto;margin:25px 0;}
.sr-table-scroll table {min-width:520px;margin:0;}
.sr-content caption {text-align:left;color:var(--ink-text-soft);font-size:13px;margin-bottom:10px;}
.sr-content th,.sr-content td {border:1px solid var(--line);padding:12px;text-align:left;vertical-align:top;}
.sr-content th {background:var(--parchment-2);}
.sr-content details {border-top:1px solid var(--line);padding:13px 0;}
.sr-content summary {cursor:pointer;font-weight:700;}
.sr-b2b-copy {max-width:900px;margin:auto;}
.sr-b2b-copy h2 {font-size:clamp(27px,3vw,36px);margin:32px 0 16px;}
.sr-b2b-copy p,.sr-b2b-copy li {line-height:1.75;}
.sr-b2b-copy ol {padding-left:24px;margin-bottom:26px;}
.sr-b2b-copy table {border-collapse:collapse;width:100%;margin:28px 0;}
.sr-b2b-copy caption {text-align:left;font-size:13px;color:var(--ink-text-soft);margin-bottom:10px;}
.sr-b2b-copy th,.sr-b2b-copy td {border:1px solid var(--line);padding:13px;text-align:left;vertical-align:top;}
.sr-b2b-copy th {background:var(--parchment-2);}
.sr-b2b-copy details {border-top:1px solid var(--line);padding:14px 0;}
.sr-b2b-copy summary {cursor:pointer;font-weight:700;}
.sr-b2b-copy .sr-grid {margin:30px 0;}
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

/* RU approved homepage, 2026-11-22. Navigation emphasis is scoped to RU only. */
.hero.v2-home .sr-hero-method{max-width:720px;margin-top:15px;font-size:16px;line-height:1.68;color:var(--cream-text);}
.hero.v2-home .sr-hero-arrow{display:inline-block;color:var(--gold-soft);font-size:1.3em;font-weight:700;line-height:1;vertical-align:-.04em;margin:0 4px;}
.hero.v2-home .sr-hero-values{max-width:720px;margin-top:13px;color:var(--gold-soft);font-size:14px;font-weight:700;line-height:1.6;letter-spacing:.02em;}
.sr-founder-spot{background:var(--parchment-2);padding:30px 0;border-bottom:1px solid var(--line);}
.sr-founder-panel{display:grid;grid-template-columns:112px minmax(0,1fr) auto;align-items:center;gap:25px;background:var(--parchment);border:1px solid var(--line);border-left:3px solid var(--gold);padding:20px 25px;}
.sr-founder-portrait{display:block;width:112px;height:140px;object-fit:cover;object-position:center 19%;border:1px solid var(--line);}
.sr-founder-copy{min-width:0;}
.sr-founder-kicker{font-size:10px;font-weight:700;letter-spacing:.1em;color:var(--seal);}
.sr-founder-copy h2{font-family:var(--font-display);font-size:clamp(24px,2.6vw,33px);line-height:1.16;margin:6px 0;}
.sr-founder-copy p{color:var(--ink-text-soft);font-size:14px;line-height:1.55;max-width:650px;margin:4px 0;}
.sr-founder-copy .sr-founder-role{font-weight:600;color:var(--ink-text);}
.sr-founder-more{display:inline-flex;align-items:center;text-decoration:none;white-space:nowrap;color:var(--seal);font-size:13px;font-weight:700;border-bottom:1px solid var(--gold);padding:8px 0;}
.sr-founder-more:hover{color:var(--seal-bright);}
html[lang="ru"] .nav-links>li:first-child>.sr-drop-button{font-weight:750;color:var(--cream-text);border-bottom:0;padding-bottom:0;}
html[lang="ru"] .nav-links>li:nth-child(2)>a{font-weight:750;color:var(--gold-soft);border-bottom:0;padding-bottom:0;}
@media(max-width:980px){
 html[lang="ru"] .nav-links>li:first-child>.sr-drop-button{display:block;width:100%;text-align:left;padding:14px 28px;border-bottom:0;line-height:1.35;}
 html[lang="ru"] .nav-links>li:nth-child(2)>a{padding:14px 28px;border-bottom:0;}
 .sr-founder-panel{grid-template-columns:100px minmax(0,1fr);gap:18px;}
 .sr-founder-portrait{width:100px;height:125px;}
 .sr-founder-more{grid-column:2;justify-self:start;}
}
@media(max-width:520px){
 .hero.v2-home .sr-hero-method{font-size:15px;}
 .hero.v2-home .sr-hero-values{font-size:13px;}
 .sr-founder-spot{padding:20px 0;}
 .sr-founder-panel{grid-template-columns:78px minmax(0,1fr);gap:12px;padding:16px;}
 .sr-founder-portrait{width:78px;height:100px;}
 .sr-founder-copy h2{font-size:25px;}
 .sr-founder-copy p{font-size:12.5px;line-height:1.5;}
 .sr-founder-kicker{font-size:9px;}
 .sr-founder-more{font-size:12px;}
}
@media(max-width:350px){.sr-founder-panel{grid-template-columns:1fr;}.sr-founder-more{grid-column:1;}.sr-founder-portrait{width:90px;height:113px;}}

/* Homepage design iteration: readable Cyrillic, consistent type, responsive hero */
html[lang="ru"]:has(.hero.v2-home){--font-display:'Inter',sans-serif;}
html[lang="ru"] .hero.v2-home{padding:52px 0 58px;}
html[lang="ru"] .hero.v2-home .wrap{grid-template-columns:minmax(0,1fr) 230px;gap:34px;align-items:center;}
html[lang="ru"] .hero.v2-home h1{font-family:'Inter',sans-serif;font-weight:700;font-size:clamp(34px,3.4vw,48px);line-height:1.13;letter-spacing:-.025em;max-width:100%;margin:14px 0 17px;text-wrap:balance;}
html[lang="ru"] .hero.v2-home .hero-lede{font-family:var(--font-body);font-size:16px;line-height:1.6;font-weight:400;color:var(--cream-text-soft);letter-spacing:normal;max-width:760px;margin-top:0;}
html[lang="ru"] .hero.v2-home .sr-hero-method{font-family:var(--font-body);font-size:16px;line-height:1.6;font-weight:400;color:var(--cream-text-soft);letter-spacing:normal;max-width:760px;margin-top:12px;}
html[lang="ru"] .hero.v2-home .sr-hero-values{display:inline-block;color:var(--cream-text);font-size:16px;line-height:1.35;font-weight:700;letter-spacing:0;padding:10px 16px;border-left:3px solid var(--gold-soft);background:rgba(255,255,255,.07);margin-top:16px;max-width:100%;}
html[lang="ru"] .hero.v2-home .hero-actions{margin-top:20px;}
html[lang="ru"] .hero.v2-home .hero-seal{display:flex;align-items:center;justify-content:center;transform:translateY(-27px);}
html[lang="ru"] .hero.v2-home .hero-seal svg{max-width:230px;}
html[lang="ru"] .sr-founder-spot{padding:26px 0;}
html[lang="ru"] .sr-founder-panel{grid-template-columns:172px minmax(0,1fr);align-items:center;gap:12px 28px;padding:22px 24px;}
html[lang="ru"] .sr-founder-portrait-frame{display:block;width:172px;height:212px;grid-row:1/span 2;overflow:hidden;border:1px solid var(--line);}
html[lang="ru"] .sr-founder-portrait{display:block;width:100%;height:100%;object-fit:cover;object-position:center;transform:scale(1);transform-origin:50% 50%;border:0;}
html[lang="ru"] .sr-founder-kicker{font-size:12px;letter-spacing:.075em;}
html[lang="ru"] .sr-founder-copy h2{font-family:'Inter',sans-serif;font-weight:700;font-size:clamp(25px,2.6vw,34px);letter-spacing:-.022em;line-height:1.15;margin:8px 0;}
html[lang="ru"] .sr-founder-copy p{font-size:15px;line-height:1.55;margin:5px 0;}
html[lang="ru"] .sr-founder-more{grid-column:2;justify-self:start;white-space:normal;font-size:13.5px;line-height:1.5;padding-bottom:3px;}
@media(max-width:980px){
 html[lang="ru"] .sr-founder-panel{grid-template-columns:154px minmax(0,1fr);gap:12px 20px;}
 html[lang="ru"] .sr-founder-portrait-frame{width:154px;height:190px;}
}
@media(max-width:900px){
 html[lang="ru"] .hero.v2-home .wrap{grid-template-columns:minmax(0,1fr);gap:0;}
 html[lang="ru"] .hero.v2-home .hero-seal{display:none;}
 html[lang="ru"] .hero.v2-home{padding:44px 0 50px;}
 html[lang="ru"] .hero.v2-home h1{font-size:clamp(31px,5.2vw,43px);}
}
@media(max-width:680px){
 html[lang="ru"] .sr-founder-panel{grid-template-columns:132px minmax(0,1fr);gap:12px 15px;padding:18px;}
 html[lang="ru"] .sr-founder-portrait-frame{width:132px;height:164px;}
 html[lang="ru"] .sr-founder-copy h2{font-size:26px;}
 html[lang="ru"] .sr-founder-copy p{font-size:13px;}
 html[lang="ru"] .sr-founder-kicker{font-size:10px;}
}
@media(max-width:600px){
 html[lang="ru"] .hero.v2-home{padding:31px 0 40px;}
 html[lang="ru"] .hero.v2-home h1{font-size:clamp(29px,7.5vw,36px);line-height:1.16;letter-spacing:-.025em;margin:13px 0 16px;}
 html[lang="ru"] .hero.v2-home .hero-lede{font-size:15px;line-height:1.55;}
 html[lang="ru"] .hero.v2-home .sr-hero-method{font-size:15px;line-height:1.55;}
 html[lang="ru"] .hero.v2-home .sr-hero-values{font-size:14.5px;line-height:1.4;padding:10px 12px;}
 html[lang="ru"] .hero.v2-home .hero-actions{flex-direction:column;align-items:stretch;}
 html[lang="ru"] .hero.v2-home .hero-actions .btn{justify-content:center;text-align:center;min-height:45px;}
}
@media(max-width:400px){
 html[lang="ru"] .sr-founder-panel{grid-template-columns:minmax(0,1fr);}
 html[lang="ru"] .sr-founder-portrait-frame{grid-row:auto;width:156px;height:182px;}
 html[lang="ru"] .sr-founder-more{grid-column:1;}
 html[lang="ru"] .sr-founder-copy h2{font-size:26px;}
 html[lang="ru"] .sr-founder-copy p{font-size:14px;}
}

/* RU header legibility: all top-level destinations are visible; prominent links remain bold */
html[lang="ru"] .nav-links{font-size:15px;gap:13px;flex-wrap:nowrap;}
html[lang="ru"] .nav-links>li>a{border-bottom:0;}
html[lang="ru"] .nav-links>li>a:hover{border-bottom:0;}
html[lang="ru"] .nav-links .has-drop>button{font-size:inherit;}
html[lang="ru"] .nav-links .nav-drop a{font-size:14.5px;}
html[lang="ru"] .nav-cta{font-size:14px;}
html[lang="ru"] .lang-switch a{font-size:12px;}
@media(max-width:1180px){
 html[lang="ru"] .nav-links{position:absolute;top:100%;left:0;right:0;display:flex;flex-direction:column;gap:0;background:var(--ink);border-bottom:1px solid var(--line-dark);max-height:0;overflow:hidden;transition:max-height .25s ease;flex-wrap:nowrap;}
 html[lang="ru"] .nav-links.open{max-height:80vh;overflow-y:auto;}
 html[lang="ru"] .nav-links li{border-top:1px solid var(--line-dark);}
 html[lang="ru"] .nav-links>li>a{display:block;padding:14px 28px;white-space:normal;}
 html[lang="ru"] .nav-links .has-drop>button{display:block;width:100%;text-align:left;padding:14px 28px;color:var(--cream-text);font-size:15px;line-height:1.35;}
 html[lang="ru"] .nav-links .nav-drop{position:static;background:transparent;border:0;box-shadow:none;padding:6px 8px 14px 16px;width:100%;}
 html[lang="ru"] .nav-links .has-drop.is-open .nav-drop{display:grid;gap:2px;}
 html[lang="ru"] .nav-links .nav-drop a{display:block;padding:11px 20px;white-space:normal;}
 html[lang="ru"] .burger{display:block;font-size:24px;padding:4px 8px;}
 html[lang="ru"] .nav-cta{display:none;}
}
/* Editorial founder photo: transparent original, no document-photo rectangle. */
/* Founder touches the lower color boundary without a frame. */
html[lang="ru"] .sr-founder-spot{padding-bottom:0;}
html[lang="ru"] .sr-founder-spot .sr-founder-panel{grid-template-columns:264px minmax(0,1fr);grid-template-rows:auto auto;gap:2px 16px;min-height:282px;overflow:hidden;padding:0 28px;border:0;box-shadow:none;background:transparent;}
html[lang="ru"] .sr-founder-spot .sr-founder-portrait-frame{position:relative;grid-row:1/span 2;grid-column:1;align-self:end;width:264px;height:282px;overflow:hidden;border:0;background:radial-gradient(ellipse at 50% 50%,rgba(169,128,62,.18),transparent 70%);}
html[lang="ru"] .sr-founder-spot .sr-founder-portrait{position:absolute;top:0;left:50%;display:block;width:264px;max-width:none;height:auto;object-fit:contain;transform:translateX(-50%);border:0;}
html[lang="ru"] .sr-founder-spot .sr-founder-copy{grid-column:2;align-self:end;padding-top:20px;}
html[lang="ru"] .sr-founder-spot .sr-founder-more{grid-column:2;align-self:start;justify-self:start;margin-bottom:23px;}
.sr-about-founder{grid-template-columns:minmax(255px,.86fr) minmax(0,1.14fr);gap:0;max-width:960px;margin:0 auto;align-items:stretch;background:var(--parchment-2);border:1px solid var(--line);border-left:3px solid var(--gold);}
.sr-about-founder .sr-about-portrait{height:360px;position:relative;overflow:hidden;background:radial-gradient(ellipse at 48% 42%,rgba(169,128,62,.21),transparent 72%);}
.sr-about-founder .lev-photo{position:absolute;top:0;left:50%;transform:translateX(-50%);width:min(100%,330px);max-width:none;height:auto;aspect-ratio:auto;object-fit:contain;object-position:center top;border:0;}
.sr-about-founder .founder-card{border:0;background:transparent;display:flex;flex-direction:column;justify-content:center;padding:32px clamp(24px,4.5vw,52px);}
.sr-about-founder .founder-card h2{font-family:var(--font-body);font-weight:700;font-size:clamp(27px,3vw,38px);line-height:1.17;}
.sr-about-founder .founder-card .role{font-size:14px;}
.sr-about-founder .founder-card p.bio{font-size:15px;line-height:1.67;max-width:52ch;}
@media(max-width:980px){
 html[lang="ru"] .sr-founder-spot .sr-founder-panel{grid-template-columns:220px minmax(0,1fr);padding:0 22px;gap:2px 16px;}
 html[lang="ru"] .sr-founder-spot .sr-founder-portrait-frame{width:220px;height:240px;}
 html[lang="ru"] .sr-founder-spot .sr-founder-portrait{width:220px;}
}
@media(max-width:760px){
 .sr-about-founder{grid-template-columns:minmax(0,1fr);}
 .sr-about-founder .sr-about-portrait{height:285px;}
 .sr-about-founder .lev-photo{width:255px;}
 .sr-about-founder .founder-card{padding:26px 24px 30px;}
}
@media(max-width:540px){
 html[lang="ru"] .sr-founder-spot .sr-founder-panel{grid-template-columns:minmax(0,1fr);grid-template-rows:auto;gap:0;padding:0;}
 html[lang="ru"] .sr-founder-spot .sr-founder-portrait-frame{grid-row:auto;grid-column:1;width:100%;height:235px;margin:0;}
 html[lang="ru"] .sr-founder-spot .sr-founder-portrait{width:220px;}
 html[lang="ru"] .sr-founder-spot .sr-founder-copy{grid-column:1;padding:15px 20px 0;}
 html[lang="ru"] .sr-founder-spot .sr-founder-more{grid-column:1;margin:10px 20px 22px;}
 html[lang="ru"] .sr-founder-spot .sr-founder-copy p{font-size:14px;}
 .sr-about-founder .sr-about-portrait{height:265px;}
 .sr-about-founder .lev-photo{width:238px;}
}

/* Unified RU typography and focused services catalog: approved 2026-11-22 */
html[lang="ru"]{--font-display:'Inter',sans-serif;--font-body:'Inter',sans-serif;}
html[lang="ru"] .sr-top h1{font-family:var(--font-body);font-weight:700;font-size:clamp(32px,4vw,46px);line-height:1.15;letter-spacing:-.025em;}
html[lang="ru"] .sr-services-section{padding-top:42px;padding-bottom:64px;}
html[lang="ru"] .sr-services-lead{margin:0 0 20px;}
html[lang="ru"] .sr-services-grid{gap:18px;}
html[lang="ru"] .sr-services-grid .sr-service-card{position:relative;min-width:0;min-height:335px;padding:26px 25px 25px;gap:13px;background:var(--parchment);border:1px solid var(--line);transition:border-color .18s ease,box-shadow .18s ease,transform .18s ease;}
html[lang="ru"] .sr-services-grid .sr-service-card:hover,html[lang="ru"] .sr-services-grid .sr-service-card:focus-within{border-color:var(--gold);box-shadow:0 8px 20px rgba(19,27,46,.08);}
html[lang="ru"] .sr-services-grid .sr-card--priority{border:1px solid var(--gold);border-top:4px solid var(--gold);background:linear-gradient(150deg,var(--parchment-2),var(--parchment) 64%);}
html[lang="ru"] .sr-services-grid .sr-card--priority .sr-icon{background:var(--gold);color:var(--ink);border-color:var(--gold);}
html[lang="ru"] .sr-services-grid .sr-service-card h3{font-family:var(--font-body);font-size:22px;line-height:1.25;font-weight:700;letter-spacing:-.02em;}
html[lang="ru"] .sr-services-grid .sr-service-card>p{font-size:14px;line-height:1.58;margin:0;min-height:0;}
html[lang="ru"] .sr-services-grid .sr-service-card ul{display:flex;flex-direction:column;gap:9px;list-style:none;padding:14px 0 0;margin:1px 0 0;border-top:1px solid var(--line);}
html[lang="ru"] .sr-services-grid .sr-service-card li{margin:0;padding:0;font-size:14px;line-height:1.45;overflow-wrap:anywhere;}
html[lang="ru"] .sr-services-grid .sr-service-card li a{color:var(--ink-text);text-decoration-color:var(--line);text-underline-offset:3px;}
html[lang="ru"] .sr-services-grid .sr-service-card li a:hover{color:var(--seal);text-decoration-color:var(--gold);}
html[lang="ru"] .sr-services-grid .sr-service-card li .sr-services-program{display:inline-block;padding:7px 10px;background:rgba(169,128,62,.14);border-left:3px solid var(--gold);color:var(--seal);font-weight:700;text-decoration:none;}
html[lang="ru"] .sr-services-grid .sr-service-card li .sr-services-program:hover{text-decoration:underline;}
html[lang="ru"] .sr-services-grid .sr-service-card>.sr-link{display:inline-flex;align-self:flex-start;align-items:center;margin-top:auto;padding-top:18px;font-size:14px;font-weight:700;line-height:1.5;text-decoration:none;}
html[lang="ru"] .sr-services-grid .sr-service-card>.sr-link:hover{text-decoration:underline;text-underline-offset:3px;}
html[lang="ru"] .sr-services-pricing{margin:24px 0 0;text-align:right;}
html[lang="ru"] .sr-services-pricing .sr-link{font-size:14px;font-weight:700;color:var(--seal);text-underline-offset:3px;}
html[lang="ru"] .sr-services-section+.sr-sec{padding-top:34px;}
@media(max-width:980px){html[lang="ru"] .sr-services-grid{grid-template-columns:repeat(2,minmax(0,1fr));}}
@media(max-width:680px){
 html[lang="ru"] .sr-services-section{padding:30px 0 48px;}
 html[lang="ru"] .sr-services-grid{grid-template-columns:minmax(0,1fr);gap:14px;}
 html[lang="ru"] .sr-services-grid .sr-service-card{min-height:0;padding:23px 21px;}
 html[lang="ru"] .sr-services-grid .sr-service-card h3{font-size:21px;}
 html[lang="ru"] .sr-services-pricing{text-align:left;}
}


/* Services wayfinding / migration hub, approved architecture 2026-11-22 */
html[lang="ru"] .sr-breadcrumbs{border-bottom:1px solid var(--line);background:var(--parchment);font-size:12px;line-height:1.5;color:var(--ink-text-soft);}
html[lang="ru"] .sr-breadcrumbs .sr-width{padding-top:12px;padding-bottom:12px;display:flex;align-items:center;gap:8px;flex-wrap:wrap;}
html[lang="ru"] .sr-breadcrumbs a{text-decoration:none;color:var(--ink-text-soft);text-underline-offset:3px;}
html[lang="ru"] .sr-breadcrumbs a:hover{text-decoration:underline;color:var(--seal);}
html[lang="ru"] .sr-breadcrumbs [aria-current="page"]{font-weight:650;color:var(--ink-text);}
html[lang="ru"] .sr-breadcrumb-separator{opacity:.52;}
html[lang="ru"] .sr-migration-top{padding:48px 0 52px;}
html[lang="ru"] .sr-migration-top h1{margin:12px 0 15px;}
html[lang="ru"] .sr-migration-top p{max-width:780px;font-size:17px;line-height:1.65;}
html[lang="ru"] .sr-migration-actions{display:flex;align-items:center;gap:22px;flex-wrap:wrap;margin-top:26px;}
html[lang="ru"] .sr-migration-jump{font-size:14px;text-underline-offset:4px;color:var(--cream-text);font-weight:600;}
html[lang="ru"] .sr-migration-hub{padding:45px 0 60px;}
html[lang="ru"] .sr-migration-section-heading{font-size:clamp(26px,3vw,36px);font-weight:700;margin:10px 0 23px;letter-spacing:-.02em;}
html[lang="ru"] .sr-migration-feature{display:grid;grid-template-columns:56px minmax(0,1fr) 20px;align-items:center;gap:20px;padding:25px 27px;color:var(--ink-text);border:1px solid var(--gold);border-left:5px solid var(--gold);background:linear-gradient(115deg,var(--parchment-2),var(--parchment) 75%);text-decoration:none;transition:border-color .18s,box-shadow .18s,transform .18s;}
html[lang="ru"] .sr-migration-feature:hover,html[lang="ru"] .sr-migration-feature:focus-visible{box-shadow:0 10px 25px rgba(19,27,46,.10);transform:translateY(-2px);}
html[lang="ru"] .sr-migration-feature-icon{display:flex;align-items:center;justify-content:center;width:55px;height:55px;background:var(--gold);color:var(--ink);font-size:29px;}
html[lang="ru"] .sr-migration-feature-copy{display:flex;flex-direction:column;gap:6px;min-width:0;}
html[lang="ru"] .sr-migration-feature-label{font-size:11px;letter-spacing:.09em;font-weight:750;color:var(--seal);}
html[lang="ru"] .sr-migration-feature-copy strong{font-size:clamp(20px,2.5vw,26px);font-weight:700;line-height:1.25;}
html[lang="ru"] .sr-migration-feature-copy>span:last-child{font-size:14px;line-height:1.6;color:var(--ink-text-soft);}
html[lang="ru"] .sr-migration-feature-arrow{font-size:21px;color:var(--seal);}
html[lang="ru"] .sr-migration-subheading{font-size:23px;font-weight:700;margin:38px 0 18px;line-height:1.3;}
html[lang="ru"] .sr-migration-links{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:13px;}
html[lang="ru"] .sr-migration-service{display:flex;align-items:center;justify-content:space-between;gap:14px;min-height:113px;padding:19px 21px;color:var(--ink-text);border:1px solid var(--line);background:var(--parchment);text-decoration:none;transition:border-color .18s,background .18s,transform .18s;}
html[lang="ru"] .sr-migration-service:hover,html[lang="ru"] .sr-migration-service:focus-visible{border-color:var(--gold);background:var(--parchment-2);transform:translateY(-2px);}
html[lang="ru"] .sr-migration-service>span:first-child{min-width:0;display:flex;flex-direction:column;gap:6px;}
html[lang="ru"] .sr-migration-service strong{font-size:18px;font-weight:700;line-height:1.35;}
html[lang="ru"] .sr-migration-service small{font-size:13px;line-height:1.5;color:var(--ink-text-soft);}
html[lang="ru"] .sr-migration-service>span:last-child{font-size:20px;color:var(--seal);align-self:center;}
html[lang="ru"] .sr-migration-service:last-child:nth-child(odd){grid-column:span 2;}
html[lang="ru"] .sr-migration-special{padding:23px 0 0;margin-top:30px;border-top:1px solid var(--line);}
html[lang="ru"] .sr-migration-special h2{font-size:22px;font-weight:700;margin:0 0 6px;}
html[lang="ru"] .sr-migration-special p{color:var(--ink-text-soft);font-size:14px;line-height:1.6;}
html[lang="ru"] .sr-migration-special-links{display:flex;gap:16px 28px;flex-wrap:wrap;margin-top:14px;}
html[lang="ru"] .sr-migration-special-links a{color:var(--seal);font-size:14px;font-weight:700;text-underline-offset:4px;}
html[lang="ru"] .sr-migration-explain{padding:56px 0;}
html[lang="ru"] .sr-migration-explain h2{font-size:27px;font-weight:700;margin:0 0 22px;}
html[lang="ru"] .sr-migration-steps{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));list-style:none;padding:0;margin:0 0 32px;gap:16px;}
html[lang="ru"] .sr-migration-steps li{border-top:2px solid var(--gold);padding:16px 12px 10px 0;min-width:0;}
html[lang="ru"] .sr-migration-steps li>span{display:block;color:var(--seal);font-weight:750;font-size:12px;letter-spacing:.09em;margin-bottom:7px;}
html[lang="ru"] .sr-migration-steps strong{display:block;font-size:17px;font-weight:700;line-height:1.35;}
html[lang="ru"] .sr-migration-steps p{margin-top:7px;color:var(--ink-text-soft);font-size:14px;line-height:1.6;}
html[lang="ru"] .sr-migration-prep{border:1px solid var(--line);background:var(--parchment);}
html[lang="ru"] .sr-migration-prep summary{display:flex;justify-content:space-between;gap:15px;align-items:center;padding:17px 20px;cursor:pointer;font-weight:700;font-size:16px;list-style:none;}
html[lang="ru"] .sr-migration-prep summary::-webkit-details-marker{display:none;}
html[lang="ru"] .sr-migration-prep summary span{font-size:23px;color:var(--seal);line-height:1;}
html[lang="ru"] .sr-migration-prep[open] summary span{transform:rotate(45deg);}
html[lang="ru"] .sr-migration-prep-content{border-top:1px solid var(--line);padding:18px 23px 23px;font-size:14px;line-height:1.7;}
html[lang="ru"] .sr-migration-prep-content ul{padding-left:22px;margin:11px 0 13px;}
html[lang="ru"] .sr-migration-prep-content li{margin-bottom:5px;}
html[lang="ru"] .sr-migration-prep-content p{margin:0 0 10px;}
html[lang="ru"] .sr-migration-prep-note a{font-weight:700;text-underline-offset:3px;color:var(--seal);}
html[lang="ru"] .sr-migration-close{padding:56px 0 72px;}
html[lang="ru"] .sr-migration-close .sr-cta p+p{margin-top:12px;}
@media(max-width:760px){
 html[lang="ru"] .sr-migration-top{padding:35px 0 42px;}
 html[lang="ru"] .sr-migration-hub{padding:34px 0 48px;}
 html[lang="ru"] .sr-migration-feature{grid-template-columns:44px minmax(0,1fr) 16px;gap:14px;padding:20px 16px;}
 html[lang="ru"] .sr-migration-feature-icon{width:44px;height:44px;font-size:23px;}
 html[lang="ru"] .sr-migration-steps{grid-template-columns:minmax(0,1fr);gap:4px;}
 html[lang="ru"] .sr-migration-explain{padding:42px 0;}
}
@media(max-width:540px){
 html[lang="ru"] .sr-migration-top p{font-size:15px;}
 html[lang="ru"] .sr-migration-actions{flex-direction:column;align-items:stretch;gap:16px;}
 html[lang="ru"] .sr-migration-actions .btn{text-align:center;justify-content:center;}
 html[lang="ru"] .sr-migration-jump{text-align:center;}
 html[lang="ru"] .sr-migration-feature{grid-template-columns:minmax(0,1fr) 16px;}
 html[lang="ru"] .sr-migration-feature-icon{display:none;}
 html[lang="ru"] .sr-migration-links{grid-template-columns:minmax(0,1fr);}
 html[lang="ru"] .sr-migration-service:last-child:nth-child(odd){grid-column:auto;}
 html[lang="ru"] .sr-migration-service{min-height:90px;padding:15px 17px;}
 html[lang="ru"] .sr-migration-service strong{font-size:16px;}
 html[lang="ru"] .sr-migration-close{padding:43px 0 52px;}
}



/* Migration hub personalized messaging and search vocabulary, 2026-11-22 */
html[lang="ru"] .sr-migration-feature-aliases{font-size:13px;line-height:1.5;color:var(--seal);font-weight:650;letter-spacing:.01em;}
html[lang="ru"] .sr-migration-service--protection strong{font-size:17px;line-height:1.35;overflow-wrap:break-word;}
html[lang="ru"] .sr-migration-close .sr-migration-close-lead{font-size:18px;font-weight:700;color:var(--ink-text);line-height:1.35;margin-bottom:10px;}
html[lang="ru"] .sr-migration-close .sr-migration-route{display:flex;flex-wrap:wrap;align-items:center;gap:7px 10px;margin-top:18px;color:var(--ink-text);font-weight:650;font-size:13px;line-height:1.6;}
html[lang="ru"] .sr-migration-close .sr-migration-route span[aria-hidden="true"]{color:var(--gold);font-size:18px;}
@media(max-width:540px){html[lang="ru"] .sr-migration-feature-aliases{font-size:12px;}html[lang="ru"] .sr-migration-service--protection strong{font-size:16px;}html[lang="ru"] .sr-migration-close .sr-migration-route{font-size:12px;}}


/* Decree 702 service journey: editorial redesign from owner's Google Sites material */
html[lang="ru"] .sr702-page{max-width:1050px;padding-top:44px;padding-bottom:65px;}
html[lang="ru"] .sr702-page h2{font-family:Inter,system-ui,sans-serif;font-size:clamp(25px,3vw,32px);line-height:1.3;margin:0 0 18px;}
html[lang="ru"] .sr702-lead{font-size:clamp(17px,2vw,20px);line-height:1.7;}
html[lang="ru"] .sr702-overview{padding:7px 0 29px;}
html[lang="ru"] .sr702-benefits{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin:30px 0 24px;}
html[lang="ru"] .sr702-benefits>div{border:1px solid var(--line);border-top:3px solid var(--gold);padding:19px 15px;background:var(--parchment);min-width:0;}
html[lang="ru"] .sr702-benefits strong{display:block;color:var(--seal);font-size:20px;line-height:1.35;margin:0 0 6px;}
html[lang="ru"] .sr702-benefits span{font-size:13px;line-height:1.5;color:var(--ink-text-soft);display:block;}
html[lang="ru"] .sr702-small{font-size:13px;color:var(--ink-text-soft);}
html[lang="ru"] .sr702-toc{border:1px solid var(--line);background:var(--parchment);padding:22px 26px;margin:25px 0 52px;}
html[lang="ru"] .sr702-toc>strong{display:block;margin-bottom:13px;color:var(--ink-text);}
html[lang="ru"] .sr702-toc>div{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px 24px;}
html[lang="ru"] .sr702-toc a{color:var(--seal);text-decoration:underline;text-underline-offset:3px;}
html[lang="ru"] .sr702-stage{padding:26px 0 40px;border-bottom:1px solid var(--line);scroll-margin-top:115px;}
html[lang="ru"] .sr702-stage-head{display:flex;align-items:flex-start;gap:17px;margin-bottom:22px;}
html[lang="ru"] .sr702-number{flex:0 0 55px;width:55px;height:55px;display:grid;place-items:center;background:#17223a;color:#F1ECDE;font-size:23px;font-weight:700;border:1px solid #A9803E;}
html[lang="ru"] .sr702-kicker{font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--seal);display:block;margin-bottom:7px;}
html[lang="ru"] .sr702-stage-head h2{margin:0;}
html[lang="ru"] .sr702-with-image{display:grid;grid-template-columns:minmax(0,1.55fr) minmax(240px,1fr);align-items:start;gap:34px;}
html[lang="ru"] .sr702-with-image figure{margin:0;min-width:0;text-align:center;}
html[lang="ru"] .sr702-with-image figure img{width:100%;height:auto;max-height:420px;object-fit:contain;display:block;border:1px solid var(--line);background:var(--parchment);border-radius:4px;}
html[lang="ru"] .sr702-with-image figcaption{font-size:12px;line-height:1.5;color:var(--ink-text-soft);padding:8px 6px;}
html[lang="ru"] .sr702-expand{background:#fff;border:1px solid var(--line);margin:13px 0 !important;padding:0 !important;}
html[lang="ru"] .sr702-expand summary{display:block;position:relative;padding:15px 47px 15px 18px;font-weight:700;cursor:pointer;list-style:none;line-height:1.5;}
html[lang="ru"] .sr702-expand summary::-webkit-details-marker{display:none;}
html[lang="ru"] .sr702-expand summary:after{content:"+";position:absolute;right:18px;top:12px;color:var(--seal);font-size:23px;}
html[lang="ru"] .sr702-expand[open] summary:after{content:"−";}
html[lang="ru"] .sr702-expand[open] summary{border-bottom:1px solid var(--line);background:var(--parchment);}
html[lang="ru"] .sr702-expand>p,html[lang="ru"] .sr702-expand>ul,html[lang="ru"] .sr702-expand>.sr702-countries{margin:16px 18px 19px !important;}
html[lang="ru"] .sr702-countries{line-height:1.85;font-size:14px;}
html[lang="ru"] .sr702-note{border-left:3px solid var(--gold);background:var(--parchment);padding:15px 18px;margin:20px 0 4px !important;line-height:1.7;}
html[lang="ru"] .sr702-final{background:var(--parchment);padding:27px 24px 38px;margin:32px -24px 0;border-bottom:0;}
html[lang="ru"] .sr702-voice{border-left:3px solid var(--gold);padding:22px 30px;background:#F9F7F1;margin:36px 0;}
html[lang="ru"] .sr702-voice p:first-child{font-size:17px;line-height:1.8;}
html[lang="ru"] .sr702-bottom{background:#17223a;color:#F1ECDE;margin:32px 0;padding:30px 34px;}
html[lang="ru"] .sr702-bottom h2{color:#F1ECDE;margin-bottom:12px;}
html[lang="ru"] .sr702-bottom p{color:#F1ECDE;}
html[lang="ru"] .sr702-sources{font-size:14px;margin-top:36px;}
html[lang="ru"] .sr702-sources a{color:var(--seal);text-underline-offset:3px;}
@media(max-width:760px){html[lang="ru"] .sr702-benefits{grid-template-columns:repeat(2,minmax(0,1fr));}html[lang="ru"] .sr702-with-image{grid-template-columns:minmax(0,1fr);gap:16px;}html[lang="ru"] .sr702-with-image figure{max-width:480px;margin:auto;}html[lang="ru"] .sr702-toc>div{grid-template-columns:minmax(0,1fr);}}
@media(max-width:430px){html[lang="ru"] .sr702-page{padding-left:17px;padding-right:17px;}html[lang="ru"] .sr702-benefits>div{padding:14px 10px;}html[lang="ru"] .sr702-benefits strong{font-size:17px;}html[lang="ru"] .sr702-number{flex-basis:43px;width:43px;height:43px;font-size:19px;}html[lang="ru"] .sr702-stage-head{gap:12px;}html[lang="ru"] .sr702-stage-head h2{font-size:23px;}html[lang="ru"] .sr702-final{margin-left:-7px;margin-right:-7px;padding-left:14px;padding-right:14px;}html[lang="ru"] .sr702-bottom{padding:24px 19px;}html[lang="ru"] .sr702-voice{padding:17px 19px;} }


/* Decree 702 review refinements: typography, reading order, and non-destructive crops */
html[lang="ru"] .sr702-page{font-family:Inter,system-ui,sans-serif;}
html[lang="ru"] .sr702-strategy{padding:12px 0 16px;margin-bottom:16px!important;font-size:17px;line-height:1.5;}
html[lang="ru"] .sr702-toc>div{grid-auto-flow:column;grid-template-rows:repeat(4,auto);grid-template-columns:repeat(2,minmax(0,1fr));}
html[lang="ru"] .sr702-toc a{text-decoration:none!important;font-weight:750;transition:color .15s ease;}
html[lang="ru"] .sr702-toc a:hover,html[lang="ru"] .sr702-toc a:focus-visible{text-decoration:underline!important;text-underline-offset:4px;}
html[lang="ru"] .sr702-visual-crop{overflow:hidden;border:1px solid var(--line);border-radius:4px;background:var(--parchment);}
html[lang="ru"] .sr702-visual-crop--arrival{aspect-ratio:680/600;}
html[lang="ru"] .sr702-visual-crop--documents{aspect-ratio:569/310;}
html[lang="ru"] .sr702-with-image .sr702-visual-crop>img{width:100%;height:auto;max-height:none;object-fit:unset;border:0;border-radius:0;display:block;}
html[lang="ru"] .sr-top .sr-eyebrow{line-height:1.65;overflow-wrap:break-word;}
@media(max-width:760px){html[lang="ru"] .sr702-toc>div{grid-auto-flow:row;grid-template-rows:none;grid-template-columns:1fr;}}
@media(max-width:430px){html[lang="ru"] .sr-top .sr-eyebrow{font-size:11px;letter-spacing:.04em;}html[lang="ru"] .sr702-strategy{font-size:15px;}}

/* Decree 702: identical Inter font, size and line-height across the three introduction paragraphs */
html[lang="ru"] .sr702-overview > p.sr702-lead,
html[lang="ru"] .sr702-overview > p.sr702-lead + p,
html[lang="ru"] .sr702-overview > p.sr702-strategy {
  font-family:Inter,system-ui,sans-serif;
  font-size:17px;
  font-weight:400;
  line-height:1.75;
  letter-spacing:normal;
}
html[lang="ru"] .sr702-overview > p.sr702-strategy {
  padding:0;
  margin-top:14px!important;
  margin-bottom:24px!important;
}
html[lang="ru"] .sr702-overview > p strong {
  font-family:inherit;
  font-size:inherit;
  line-height:inherit;
  font-weight:700;
}
@media(max-width:430px) {
 html[lang="ru"] .sr702-overview > p.sr702-lead,
 html[lang="ru"] .sr702-overview > p.sr702-lead + p,
 html[lang="ru"] .sr702-overview > p.sr702-strategy {font-size:16px;}
}



/* Stage 1: static, enlarged visa without outer white margins */
html[lang="ru"] .sr702-with-image--visa{grid-template-columns:minmax(0,1.08fr) minmax(350px,1.12fr);gap:26px;}
html[lang="ru"] .sr702-with-image--visa .sr702-visa-figure{width:100%;max-width:100%;margin:0;}
html[lang="ru"] .sr702-visa-crop{display:block;position:relative;overflow:hidden;aspect-ratio:4/3;border:1px solid var(--line);border-radius:5px;background:var(--parchment);}
html[lang="ru"] .sr702-with-image .sr702-visa-crop img{display:block;width:100%;height:100%;max-height:none;object-fit:cover;object-position:center center;transform:scale(1.045);border:0;border-radius:0;}
html[lang="ru"] .sr702-visa-figure figcaption{padding:10px 6px 0;font-size:12px;line-height:1.5;color:var(--ink-text-soft);text-align:center;}
@media(max-width:760px){html[lang="ru"] .sr702-with-image--visa{grid-template-columns:minmax(0,1fr);gap:16px;}html[lang="ru"] .sr702-with-image--visa .sr702-visa-figure{max-width:580px;margin:0 auto;}}

'''
(OUT/'assets'/'platform.css').write_text(CSS_ADD+LEGAL_CSS,encoding='utf-8')
shutil.copy2(ROOT/'assets'/'expert-articles.css',OUT/'assets'/'expert-articles.css')
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
  const fr=document.documentElement.lang==='fr';
  b.textContent=ok?(fr?'Copié':'Скопировано'):(fr?'Sélectionnez et copiez le texte':'Выделите и скопируйте текст');
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
 'en':{'home':'Home','services':'Services','decree':'Decree 702','kb':'Insights','about':'About','contacts':'Contact','consult':'Contact us','reviews':'Reviews','prices':'Fees','more':'Learn more →','discuss':'Discuss a project →','start':'Contact us','all':'All','articles':'Articles','instructions':'Guides','news':'News'},
}
SECTIONS={
 'migration':{'ru':('Immigration et statuts','Переезд в Россию','РВП, ВНЖ, гражданство, визы, Указ 702 и правовая помощь при простых и сложных миграционных ситуациях.'),'fr':('Immigration','S’installer en Russie','Titres de séjour, visas, nationalité russe et accompagnement juridique.') ,'symbol':'✦'},
 'real-estate':{'ru':('Недвижимость','Недвижимость','Аренда, покупка, договоры и юридическая проверка объекта до принятия обязательств.'),'fr':('Immobilier','Immobilier en Russie','Location, acquisition, contrats et vérification juridique avant tout engagement.'),'symbol':'⌂'},
 'business':{'ru':('Бизнес','Бизнес в России','Создание компании, корпоративные документы, юридические риски и международный найм.'),'fr':('Entreprises','Créer une entreprise','Création de sociétés, documents, risques juridiques et recrutement international.'),'symbol':'§'},
 'investments':{'ru':('Инвестиции','Инвестиции','Юридическая проверка сделки, активов и условий участия в инвестиционном проекте.'),'fr':('Investissements','Investissements en Russie','Vérification juridique des actifs, des parties et des conditions de participation.'),'symbol':'↗'},
 'legal':{'ru':('Правовая помощь','Юридическая помощь','Консультации, документы, анализ рисков и судебная защита по согласованному вопросу.'),'fr':('Juridique','Assistance juridique','Consultations, documents, analyse des risques et contentieux selon la mission convenue.'),'symbol':'⚖'},
 'relocation':{'ru':('Переезд','Переезд и адаптация','Планирование документов, жилья, прибытия и первых практических шагов семьи в России.'),'fr':('Installation','Installation et intégration','Planification des documents, du logement, de l’arrivée et des premières démarches.'),'symbol':'◎'},
}
PROGRAMS={
 'rvp':{'ru':('Разрешение на временное проживание','РВП в России','Проверяем основание для оформления РВП, документы и применимую процедуру. В отдельных ситуациях необходим индивидуальный правовой анализ.'),'fr':('Permis de séjour temporaire','Séjour temporaire (RVP)','Vérification de l’éligibilité, des pièces et de la procédure adaptée.')},
 'vnzh':{'ru':('Вид на жительство','ВНЖ в России','Анализируем возможные основания для получения вида на жительство и последовательность действий.'),'fr':('Résidence permanente','Titre de séjour (VNZh)','Analyse des voies d’accès au titre de séjour et des documents requis.')},
 'citizenship':{'ru':('Гражданство Российской Федерации','Гражданство России','Выбираем применимое основание, проверяем документы и сопровождаем согласованную процедуру.'),'fr':('Nationalité russe','Nationalité russe','Vérification du fondement juridique et accompagnement du dossier.')},
 'visas':{'ru':('Визы','Визы в Россию','Помогаем определить подходящий визовый режим, проверить документы и последовательность оформления.'),'fr':('Visas','Visas pour la Russie','Choix du régime de visa et préparation du dossier.')},
 'students':{'ru':('Образование и РВПО','Учёба в России и РВПО','Помощь иностранным студентам по вопросам статуса и документов.'),'fr':('Études','Études et séjour','Assistance aux étudiants étrangers concernant le statut et les documents.')},
 'family':{'ru':('Переезд семьи','Семейный переезд','Подбираем последовательность оформления статусов и документов для членов семьи.'),'fr':('Famille','S’installer en famille','Planifier le statut et les démarches des membres de la famille.')},
 'disputes':{'ru':('Защита','Защита в суде и государственных органах (МВД, ФСБ)','Помогаем обжаловать решения, защититься при выдворении или депортации и отстоять права в суде и компетентных государственных органах.'),'fr':('Contentieux','Contentieux migratoire','Recours contre les décisions administratives et défense devant les tribunaux.')}
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
def meta(title,desc,lang,url,noindex=False,article=False,ru_only=False,structured=None):
 tags=f'<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} · SalutRussie</title><meta name="description" content="{esc(desc)}"><meta name="theme-color" content="#131B2E"><meta name="robots" content="{"noindex,nofollow" if noindex or not PUBLIC else "index,follow"}">'
 tags+='<link rel="icon" type="image/svg+xml" href="/assets/favicon.svg"><link rel="stylesheet" href="/assets/fonts.css">'
 tags+=f'<link rel="stylesheet" href="/assets/claude-{"ru" if lang=="ru" else "fr"}.css"><link rel="stylesheet" href="/assets/platform.css"><meta property="og:type" content="{"article" if article else "website"}"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}">'
 if ru_only: tags+='<link rel="stylesheet" href="/assets/expert-articles.css">'
 if PUBLIC:
  tags+=f'<link rel="canonical" href="{esc(ORIGIN+url)}"><meta property="og:url" content="{esc(ORIGIN+url)}">'
  if not noindex:
   languages=('ru',) if ru_only else ('ru','fr','en') if '/for-business/' in url else ('ru','fr')
   for alternate in languages:
    alternate_url=re.sub(r'^/(ru|fr|en)/',f'/{alternate}/',url)
    tags+=f'<link rel="alternate" hreflang="{alternate}" href="{esc(ORIGIN+alternate_url)}">'
   schema=structured or {'@context':'https://schema.org','@type':'Article' if article else 'WebPage','headline':title,'url':ORIGIN+url,'inLanguage':lang,'publisher':{'@type':'Organization','name':'SalutRussie'}}
   if article: schema['dateModified']='2026-11-21'
   tags+=f'<script type="application/ld+json">{json.dumps(schema,ensure_ascii=False).replace("<", "\\u003c")}</script>'
 return tags

def nav(lang,url=None):
 if lang=='en':
  base='/en/for-business/'
  peer=(url or base).replace('/en/','/ru/',1)
  fr_peer=(url or base).replace('/en/','/fr/',1)
  return f'''<header class="sr-header"><nav class="nav" aria-label="Main navigation"><a class="brand" href="{base}" aria-label="SalutRussie"><svg class="seal-mark" fill="none" viewBox="0 0 60 60" aria-hidden="true"><circle cx="30" cy="30" r="27" stroke="#A9803E" stroke-width="1.2"/><text x="30" y="37" font-size="17" font-family="Fraunces,serif" text-anchor="middle" fill="#F1ECDE">SR</text></svg><span>SalutRussie</span></a><button class="burger" id="burger" aria-label="Menu" aria-controls="navLinks" aria-expanded="false">☰</button><ul class="nav-links" id="navLinks"><li><a href="{base}">For business</a></li><li><a href="{base}employers/">Employers</a></li><li><a href="{base}recruitment-partners/">Recruitment partners</a></li></ul><div class="lang-switch"><a href="{peer}">RU</a><a href="{fr_peer}">FR</a><a class="active" href="{url or base}" aria-current="page">EN</a></div><a class="nav-cta" href="mailto:salutrussie@salutrussie.ru?subject=Business%20enquiry">Contact us →</a></nav></header>'''
 x=LANGS[lang]
 fr_switch=path('fr','knowledge') if lang=='ru' and any(url==a['url'] for a in EXPERT_ARTICLES) else (url or path(lang)).replace('/ru/','/fr/',1) if lang=='ru' else url or path(lang)
 s=f'''<header class="sr-header"><nav class="nav" aria-label="{'Основное меню' if lang=='ru' else 'Navigation principale'}"><a class="brand" href="{path(lang)}" aria-label="SalutRussie">
 <svg class="seal-mark" fill="none" viewBox="0 0 60 60" aria-hidden="true"><circle cx="30" cy="30" r="27" stroke="#A9803E" stroke-width="1.2"/><circle cx="30" cy="30" r="21" stroke="#A9803E" stroke-width="0.7"/><text x="30" y="37" font-size="17" font-family="Fraunces,serif" text-anchor="middle" fill="#F1ECDE">SR</text></svg><span>SalutRussie</span></a>
<button class="burger" id="burger" aria-label="Menu" aria-controls="navLinks" aria-expanded="false">☰</button><ul class="nav-links" id="navLinks">
<li class="has-drop"><button type="button" class="sr-drop-button" aria-expanded="false" aria-controls="service-drop">{x['services']} ▾</button><div class="nav-drop" id="service-drop">'''
 for slug,data in SECTIONS.items(): s+=f'<a href="{path(lang,slug)}">{esc(data[lang][1])}</a>'
 s+=f'''</div></li><li><a href="{path(lang,'migration/decree-702')}">{x['decree']}</a></li><li><a href="{path(lang,'knowledge')}">{x['kb']}</a></li><li><a href="{path(lang,'for-business')}">{'Для бизнеса' if lang=='ru' else 'Pour les entreprises'}</a></li><li><a href="{path(lang,'about')}">{x['about']}</a></li><li><a href="{path(lang,'contacts')}">{x['contacts']}</a></li>
</ul><div class="lang-switch"><a href="{fr_switch}"{' class="active" aria-current="page"' if lang=='fr' else ''}>FR</a><a href="{(url or path(lang)).replace('/fr/','/ru/',1) if lang=='fr' else url or path(lang)}"{' class="active" aria-current="page"' if lang=='ru' else ''}>RU</a>{f'<a href="{(url or path(lang)).replace("/"+lang+"/","/en/",1)}">EN</a>' if '/for-business/' in (url or '') else ''}</div><a class="nav-cta" data-analytics-event="consultation_click" href="{path(lang,'consultations')}">{x['consult']} →</a></nav></header>'''
 return s

def footer(lang):
 if lang=='en':
  return '<footer class="sr-footer"><div class="sr-width"><div><div class="sr-footer-brand">SalutRussie</div><p class="sr-small">Russian legal support for cross-border employment projects.</p>'+provider_footer(lang)+'</div><div><a href="/en/for-business/">For business</a><a href="/en/for-business/employers/">Employers</a><a href="/en/for-business/recruitment-partners/">Recruitment partners</a><a href="mailto:salutrussie@salutrussie.ru">Contact</a><p class="sr-small">© 2018–2026 SalutRussie</p></div></div></footer>'
 x=LANGS[lang]
 return f'''<footer class="sr-footer"><div class="sr-width"><div><div class="sr-footer-brand">SalutRussie</div><p class="sr-small">{'Профессиональная помощь для иностранцев в России' if lang=='ru' else 'Assistance professionnelle aux étrangers en Russie'}</p>{provider_footer(lang)}</div><div><a href="{path(lang,'services')}">{x['services']}</a><a href="{path(lang,'consultations')}">{x['consult']}</a><a href="{path(lang,'knowledge')}">{x['kb']}</a><a href="{path(lang,'pricing')}">{x['prices']}</a><a href="{path(lang,'contacts')}">{x['contacts']}</a><br><a href="{path(lang,'privacy')}">{'Как работают каналы связи' if lang=='ru' else 'Moyens de contact'}</a><p class="sr-small">© 2018–2026 SalutRussie</p></div></div></footer>'''

def link_msg(lang,topic):
 txt=(f'Здравствуйте! Обращаюсь с сайта SalutRussie. Тема: {topic}. Хотел(а) бы узнать о консультации.' if lang=='ru' else f'Bonjour ! Je vous contacte via SalutRussie. Sujet : {topic}. Je souhaite réserver une consultation.')
 return 'https://wa.me/79685341915?text='+quote(txt)

def feature(lang):
 if lang=='ru':
  paragraphs=[
   'Специальный порядок для иностранцев, отвечающих условиям Указа 702.',
   'Помогаем проверить применимость программы, определить миграционную стратегию, подготовить документы для специальной частной визы на срок до трёх месяцев и дальнейшего обращения за РВП.',
   'Для начала проверьте, входит ли страна вашего гражданства в действующий перечень государств программы. Решение о визе и РВП принимают уполномоченные органы.'
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

def service_breadcrumbs_ru(url,title):
 parts=url.strip('/').split('/')
 names={'migration':'Переезд в Россию','real-estate':'Недвижимость','business':'Бизнес в России','investments':'Инвестиции','legal':'Юридическая помощь','relocation':'Переезд и адаптация'}
 if len(parts)<2 or parts[0]!='ru' or parts[1] not in ('services',*names):return ''
 crumbs=[('Главная',path('ru'))]
 if parts[1]=='services':
  crumbs.append(('Все услуги',None))
 else:
  crumbs.append(('Все услуги',path('ru','services')))
  if len(parts)==2:crumbs.append((names[parts[1]],None))
  else:
   crumbs.append((names[parts[1]],path('ru',parts[1])))
   crumbs.append((title,None))
 bits=[]
 for i,(label,url) in enumerate(crumbs):
  if i:bits.append('<span class="sr-breadcrumb-separator" aria-hidden="true">›</span>')
  bits.append(f'<a href="{url}">{esc(label)}</a>' if url else f'<span aria-current="page">{esc(label)}</span>')
 return '<nav class="sr-breadcrumbs" aria-label="Навигационная цепочка"><div class="sr-width">'+''.join(bits)+'</div></nav>'

def shell(lang,url,title,description,body,noindex=False,article=False,ru_only=False,structured=None):
 skip={'ru':'Перейти к содержанию','fr':'Aller au contenu','en':'Skip to content'}[lang]
 trail=service_breadcrumbs_ru(url,title) if lang=='ru' else ''
 return '<!doctype html>\n'+f'<html lang="{lang}"><head>{meta(title,description,lang,url,noindex,article,ru_only,structured)}</head><body><a class="sr-skip" href="#main">{skip}</a>{nav(lang,url)}<main id="main">{trail}{body}</main>{footer(lang)}<script src="/assets/platform.js" defer></script></body></html>'

def home(lang):
 ru=lang=='ru';title='Помощь иностранцам в России: миграция, недвижимость, бизнес' if ru else 'Services aux étrangers en Russie : immigration, immobilier, affaires'
 intro='Живите, работайте и развивайте бизнес в России' if ru else 'Vivre, s’installer et entreprendre en Russie — avec le bon accompagnement.'
 detail=('Мы помогаем иностранцам переехать в Россию, оформить РВП, ВНЖ и гражданство. Решаем сложные юридические вопросы, сопровождаем покупку недвижимости, инвестиции и открытие бизнеса.' if ru else 'Immigration, immobilier, création d’entreprise, investissement et conseil juridique. Nous analysons votre situation et construisons avec vous une stratégie adaptée.')
 emblem=BeautifulSoup((SRC/('index-ru.html' if ru else 'index.html')).read_text(),'html.parser').select_one('.hero-seal')
 emblem=str(emblem) if emblem else '<div class="hero-seal" aria-hidden="true">SR</div>'
 hero_followup=("<p class=\"sr-hero-method\">Разрабатываем для вас индивидуальную стратегию <span class=\"sr-hero-arrow\" aria-hidden=\"true\">→</span> сопровождаем вас на каждом этапе её реализации.</p><p class=\"sr-hero-values\">Профессионально. Безопасно. Надёжно.</p>" if ru else '')
 hero=f'''<section class="hero v2-home"><div class="wrap"><div><div class="sr-hero-kicker">{'УСЛУГИ ДЛЯ ИНОСТРАНЦЕВ В РОССИИ' if ru else 'SERVICES AUX ÉTRANGERS EN RUSSIE'}</div><h1>{esc(intro)}</h1><p class="hero-lede">{esc(detail)}</p>{hero_followup}<div class="hero-actions"><a class="btn btn-primary" data-analytics-event="consultation_click" href="{path(lang,'consultations')}">{'Получить консультацию →' if ru else 'Demander une consultation →'}</a><a class="btn btn-ghost" href="{path(lang,'services')}">{'Все услуги' if ru else 'Tous nos services'}</a></div></div>{emblem}</div></section>'''
 founder=("<section class=\"sr-founder-spot\" aria-label=\"Основатель и личная ответственность\"><div class=\"sr-width\"><div class=\"sr-founder-panel\"><div class=\"sr-founder-portrait-frame\"><img class=\"sr-founder-portrait\" src=\"/assets/founder-lev-vtiurin-cutout-2026.webp\" alt=\"Лев Втюрин — основатель SalutRussie\" loading=\"lazy\" width=\"112\" height=\"140\"></div><div class=\"sr-founder-copy\"><span class=\"sr-founder-kicker\">ЛИЧНАЯ ОТВЕТСТВЕННОСТЬ</span><h2>Лев Втюрин</h2><p class=\"sr-founder-role\">Основатель SalutRussie · Более 20 лет юридической практики</p><p>Лично отвечаю за правовую стратегию и качество сопровождения каждого проекта.</p></div><a class=\"sr-founder-more\" href=\"{path(lang,'about')}\">О бюро и опыте →</a></div></div></section>".replace("{path(lang,'about')}",path(lang,'about')) if ru else '')
 services=f'''<section class="sr-sec" id="services"><div class="sr-width"><div class="sr-section-head"><span class="eyebrow">{'НАПРАВЛЕНИЯ' if ru else 'NOS SERVICES'}</span><h2>{'Чем мы можем помочь' if ru else 'Comment pouvons-nous vous aider ?'}</h2><p>{'Выберите интересующее вас направление — мы подскажем, с чего начать' if ru else 'Choisissez votre besoin : nous définirons l’accompagnement approprié.'}</p></div>{cards(lang,list(SECTIONS.items()))}</div></section>'''
 steps=[('01','Ваша заявка','Опишите свой вопрос своими словами в том формате, как вам удобно'),('02','Консультация','Проводим подробную консультацию, разбираем вашу ситуацию и отвечаем на все вопросы'),('03','План действий','Готовим пошаговый план действий для достижения вашей цели'),('04','Сопровождение','Сопровождаем на согласованных этапах работы')] if ru else [('01','Expliquez votre projet','Présentez votre besoin sans documents sensibles au premier contact.'),('02','Choisissez une consultation','Nous analysons votre situation et répondons à vos questions.'),('03','Obtenez un plan','Analyse des pièces et étapes suivantes.'),('04','Accompagnement','Nous intervenons selon le périmètre convenu.')]
 process=f'''<section class="sr-sec alt"><div class="sr-width"><div class="sr-section-head"><span class="eyebrow">{'ПРОЦЕСС' if ru else 'NOTRE MÉTHODE'}</span><h2>{'Как мы работаем' if ru else 'Comment nous travaillons'}</h2></div><div class="sr-steps">'''
 for n,h,p in steps:process+=f'<div class="sr-step"><b>{n}</b><h3>{esc(h)}</h3><p>{esc(p)}</p></div>'
 process+='</div></div></section>'
 knowledge=f'''<section class="sr-sec"><div class="sr-width"><div class="sr-section-head"><span class="eyebrow">{'ЭКСПЕРТНЫЕ МАТЕРИАЛЫ' if ru else 'RESSOURCES'}</span><h2>{'Полезная информация' if ru else 'Informations utiles'}</h2><p>{'Всё, что важно знать о жизни, переезде и бизнесе в России. Делимся профессиональным опытом, объясняем законодательство, разбираем практические ситуации и рассказываем о важных изменениях.' if ru else 'Guides pratiques, analyses juridiques, articles et actualités dans un seul espace.'}</p></div>'''
 opts=[]
 if ru:
  for a in (EXPERT_ARTICLES[0],EXPERT_ARTICLES[2],EXPERT_ARTICLES[6]):
   opts.append((f'knowledge/articles/{a["slug"]}',{'symbol':'↗','ru':(a['title'],a['title'],a['summary'])}))
 else:
  for a in ARTICLES[:3]:opts.append((f'knowledge/articles/{a["slug"]}',{'symbol':'↗',lang:(a[lang][0],a[lang][0],a[lang][1])}))
 knowledge+=cards(lang,opts)+f'<p style="margin-top:25px"><a class="btn btn-ghost" href="{path(lang,"knowledge")}">{"Все материалы и поиск →" if ru else "Rechercher dans les ressources →"}</a></p></div></section>'
 about=f'''<section class="sr-sec alt"><div class="sr-width"><div class="sr-section-head"><span class="eyebrow">{'О КОМАНДЕ' if ru else 'NOTRE ÉQUIPE'}</span><h2>{'Небольшая команда профессионалов: бутик, а не масс-маркет' if ru else 'Expertise juridique et coordination des spécialistes'}</h2><p>{'Все специалисты SalutRussie придерживаются единого стандарта качества услуг. Мы делаем только то, что приближает к результату. Наш главный принцип — сначала стратегия, потом реализация' if ru else 'Chaque situation commence par l’analyse de vos besoins. Nous précisons les prestations réalisées par notre équipe et celles de nos partenaires.'}</p></div><a class="btn btn-primary" href="{path(lang,"about")}">{'О нас →' if ru else 'Notre équipe →'}</a></div></section>'''
 meta_description=('Помощь иностранцам в России: миграция, РВП, ВНЖ, Указ 702 (разделение ценностей, идеологическая программа), недвижимость, бизнес и юридическая помощь.' if ru else detail)
 return shell(lang,path(lang),title,meta_description,hero+founder+services+feature(lang)+process+knowledge+about+cta(lang))

def about_ru():
 source=BeautifulSoup((SRC/'o-kompanii-ru.html').read_text(encoding='utf-8'),'html.parser')
 portrait=source.select_one('main img.lev-photo')['src']
 kind,data=portrait.split(',',1)
 asset='/assets/ru-o-kompanii-ru-0.jpg'
 (OUT/asset.lstrip('/')).write_bytes(base64.b64decode(data))
 body="""<div class="page-head"><div class="wrap"><span class="eyebrow">МИГРАЦИОННОЕ БЮРО</span><h1>Мы начинали как семейное бюро — сегодня работаем по всей России</h1><p>SalutRussie выросло из небольшой семейной практики в команду профессионалов. Наш основной центр находится в Москве, а сотрудничество со специалистами в регионах позволяет сопровождать клиентов в разных городах России.</p></div></div>
 <section class="sr-sec"><div class="wrap"><div class="lev-about sr-about-founder"><div class="sr-about-portrait"><img class="lev-photo" src="/assets/founder-lev-vtiurin-cutout-2026.webp" alt="Лев Втюрин — основатель SalutRussie" width="600" height="750"></div><div class="founder-card"><h2>Лев Втюрин</h2><span class="role">Миграционный юрист — основатель</span><p class="bio">Более 20 лет юридической практики. Специализация — миграционное право, судебная защита и сложные миграционные ситуации.</p><p class="bio">Лично участвует в разработке правовой стратегии сложных дел и в судебной защите клиентов.</p></div></div></div></section>
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
 return shell(lang,url,title,desc,z)

def services_ru():
 title='Все услуги для иностранцев'
 desc='От миграционной стратегии до недвижимости, бизнеса и юридической защиты — помогаем решать вопросы, возникающие при переезде и жизни в России.'
 shortcuts={
  'migration':[
   ('migration/decree-702','Переезд по Указу 702'),
   ('migration/visas','Визы в Россию'),
   ('migration/rvp','РВП в России'),
   ('migration/vnzh','ВНЖ в России'),
   ('migration/citizenship','Гражданство России'),
   ('migration/disputes','Защита в суде и государственных органах (МВД, ФСБ)')
  ],
  'business':[
   ('business/company-registration','Открытие компании'),
   ('business/legal-support','Юридическое сопровождение бизнеса'),
   ('business/tax-consulting','Налоговое консультирование')
  ],
  'investments':[
   ('investments/legal-due-diligence','Юридическая проверка и сопровождение инвестиционного проекта'),
   ('investments/project-selection','Подбор инвестиционных проектов')
  ],
  'legal':[
   ('consultations','Консультации'),
   ('legal/document-preparation','Подготовка документов'),
   ('legal/disputes','Судебные споры')
  ],
  'relocation':[
   ('relocation/administrative-procedures','Административные процедуры'),
   ('relocation/everyday-life','Бытовые вопросы'),
   ('relocation/russian-language','Изучение русского языка')
  ]
 }
 shortcuts['real-estate']=[(f'real-estate/{slug}',SUBLABEL[slug][0]) for slug in SUBPAGES['real-estate']]
 body=heading('ru',title,desc,LANGS['ru']['services'])
 body+='<section class="sr-sec sr-services-section"><div class="sr-width"><div class="sr-services-lead"><span class="eyebrow">НАПРАВЛЕНИЯ ПОМОЩИ</span></div><div class="sr-grid sr-services-grid">'
 for slug,data in SECTIONS.items():
  _,name,description=data['ru']
  if slug=='investments':description='Подбор инвестиционных проектов, юридическая проверка и сопровождение сделок.'
  priority=' sr-card--priority' if slug=='migration' else ''
  body+=f'<section class="sr-card sr-service-card{priority}"><span class="sr-icon" aria-hidden="true">{esc(data["symbol"])}</span><h3>{esc(name)}</h3><p>{esc(description)}</p>'
  if slug in shortcuts:
   body+='<ul>'
   for tail,label in shortcuts[slug]:
    accent=' class="sr-services-program"' if slug=='migration' and tail=='migration/decree-702' else ''
    body+=f'<li><a{accent} href="{path("ru",tail)}">{esc(label)}</a></li>'
   body+='</ul>'
  body+=f'<a class="sr-link" href="{path("ru",slug)}">Подробнее о направлении →</a></section>'
 body+=f'</div><p class="sr-services-pricing"><a class="sr-link" href="{path("ru","pricing")}">Тарифы →</a></p></div></section>'
 consult=cta('ru').replace('Выберите направление консультации. Объём работы и стоимость согласуем.','Не уверены, какая услуга вам нужна? Опишите свою ситуацию — мы поможем определить подходящий правовой маршрут. Формат и стоимость работы согласуем заранее.')
 return shell('ru',path('ru','services'),title,desc,body+consult)

def pricing_ru():
 title='Стоимость юридических услуг'
 desc='Состав работы, формат и стоимость согласуем до начала оказания услуги.'
 body=heading('ru',title,desc,LANGS['ru']['services'])
 body+='<article class="sr-content"><p>Стоимость зависит от задачи, объёма документов, срочности и согласованного формата работы. Мы определяем эти параметры после первого описания ситуации и сообщаем условия до начала платной работы.</p><h2>Как согласуем работу</h2><ol><li>Вы кратко описываете задачу и желаемый результат.</li><li>Мы уточняем необходимые документы, правовые вопросы и границы работы.</li><li>Согласуем формат, этапы и стоимость. Решение о заказе остаётся за вами.</li></ol><h2>Направления</h2><ul>'
 for tail,label in [('consultations','Консультации'),('migration/decree-702','Программа 702'),('relocation','Переезд и адаптация'),('for-business','Для бизнеса'),('services','Все услуги')]:
  body+=f'<li><a href="{path("ru",tail)}">{esc(label)}</a></li>'
 body+='</ul><p class="sr-note">На этой странице нет универсального прайс-листа. Мы не обещаем решение государственного органа или результат спора.</p></article>'
 return shell('ru',path('ru','pricing'),title,desc,body+cta('ru'))

def pricing_fr():
 title='Honoraires et prestations'
 desc='Le périmètre, le format et les honoraires sont convenus avant toute intervention.'
 body=heading('fr',title,desc,'SERVICES')
 body+='<article class="sr-content"><p>Les honoraires dépendent du problème, du volume des pièces, du calendrier et du format convenu. Nous définissons ces éléments après un premier échange et vous indiquons les conditions avant toute mission payante.</p><h2>Comment cela fonctionne</h2><ol><li>Vous présentez brièvement votre situation et votre objectif.</li><li>Nous précisons les documents, les questions juridiques et les limites de la mission.</li><li>Nous convenons du format, des étapes et des honoraires ; vous décidez ensuite.</li></ol><h2>Par où commencer ?</h2><ul><li><a href="/fr/consultations/">Poser une question juridique</a> sans envoyer de documents sensibles dans le premier message.</li><li><a href="/fr/services/">Explorer les domaines d’intervention</a>.</li><li><a href="/fr/for-business/">Voir l’accompagnement pour les entreprises</a>.</li></ul><p class="sr-note">Il n’existe pas de forfait universel présenté ici. Une décision administrative ou judiciaire ne peut pas être promise.</p></article>'
 return shell('fr',path('fr','pricing'),title,desc,body+cta('fr'))

def about_fr():
 title='Notre cabinet juridique en Russie'
 desc='Découvrez le fondateur de SalutRussie et notre méthode de travail.'
 body='''<div class="page-head"><div class="wrap"><span class="eyebrow">NOTRE CABINET</span><h1>Une pratique juridique à taille humaine, présente pour vos projets en Russie</h1><p>SalutRussie a commencé comme un cabinet familial. Nous travaillons aujourd’hui sur des dossiers dans différentes régions de Russie, en définissant d’abord la stratégie et les étapes adaptées au cas concret.</p></div></div>
 <section class="sr-sec"><div class="wrap"><div class="lev-about sr-about-founder"><div class="sr-about-portrait"><img class="lev-photo" src="/assets/founder-lev-vtiurin-cutout-2026.webp" alt="Lev Vtiurin, fondateur de SalutRussie" width="600" height="750"></div><div class="founder-card"><h2>Lev Vtiurin</h2><span class="role">Juriste en droit migratoire, fondateur</span><p class="bio">Plus de vingt ans de pratique juridique en Russie, notamment en droit migratoire, dans les dossiers complexes et la défense devant les tribunaux.</p><p class="bio">Il étudie la situation, explique les risques et détermine avec le client les démarches à entreprendre.</p></div></div></div></section>
 <section class="sr-sec alt"><div class="sr-width"><div class="sr-section-head"><span class="eyebrow">NOTRE MÉTHODE</span><h2>Une stratégie avant les démarches</h2><p>Nous commençons par les faits et les documents. Nous définissons les questions juridiques, les options à vérifier et les étapes utiles. Le périmètre de l’accompagnement est convenu avant toute intervention.</p></div><div class="sr-steps"><div class="sr-step"><b>01</b><h3>Votre situation</h3><p>Vous décrivez votre objectif et les difficultés rencontrées.</p></div><div class="sr-step"><b>02</b><h3>Analyse</h3><p>Nous vérifions les faits, les documents et le cadre juridique applicable.</p></div><div class="sr-step"><b>03</b><h3>Plan</h3><p>Nous proposons une séquence de démarches et signalons les risques.</p></div><div class="sr-step"><b>04</b><h3>Accompagnement</h3><p>Nous intervenons dans les limites convenues ensemble.</p></div></div></div></section>
 <section class="sr-sec"><div class="sr-width sr-about-mission"><div class="sr-section-head"><span class="eyebrow">NOTRE OBJECTIF</span><h2>Agir légalement et avec méthode à chaque étape</h2></div><p>Nous accompagnons les questions de séjour, de logement, d’activité économique et d’adaptation en Russie. Nous ne promettons pas de décision administrative : chaque dossier dépend des faits et des règles applicables.</p></div></section>'''
 return shell('fr',path('fr','about'),title,desc,body+cta('fr'))

def contacts_page(lang):
 ru=lang=='ru'
 title='Контакты SalutRussie' if ru else 'Contacter SalutRussie'
 desc='Напишите нам по юридическому вопросу. Выберите удобный канал связи.' if ru else 'Décrivez votre question juridique et choisissez votre moyen de contact.'
 body=heading(lang,'Расскажите о своей задаче' if ru else 'Parlez-nous de votre projet',desc,'КОНТАКТЫ' if ru else 'CONTACT')
 body+='<section class="sr-sec"><div class="sr-width"><div class="sr-contact-list">'
 for label,href,description in [
  ('WhatsApp','https://wa.me/79685341915','Откроется чат' if ru else 'Ouvrir la conversation'),
  ('Telegram','https://t.me/lev_vt','@lev_vt'),
  ('E-mail','mailto:salutrussie@salutrussie.ru','salutrussie@salutrussie.ru')]:
  body+=f'<a class="sr-contact-choice" href="{href}"><strong>{label} →</strong><span>{description}</span></a>'
 body+='</div><p class="sr-note">'+('Опишите вопрос кратко. Стоимость и объём работы согласуем до начала. Не направляйте чувствительные документы в первом сообщении.' if ru else 'Décrivez brièvement votre situation. Nous convenons du périmètre et des honoraires avant de commencer. Évitez les documents sensibles dans votre premier message.')+'</p></div></section>'
 return shell(lang,path(lang,'contacts'),title,desc,body+provider_block(lang))

def decree_page(lang):
 ru=lang=='ru'
 url=path(lang,'migration/decree-702')
 title='Переезд в Россию по Указу 702' if ru else 'S’installer en Russie selon le décret n° 702'
 desc='Переезд в Россию по Указу 702: разделение ценностей, идеологическая программа, список стран, оформление визы, документы, РВП и юридическая помощь.' if ru else 'Conditions du dispositif, points à vérifier et préparation du dossier.'
 source='https://kremlin.ru/acts/bank/51035'
 publication='https://publication.pravo.gov.ru/document/0001202408190001'
 countries='https://publication.pravo.gov.ru/document/0001202409200036'
 if ru:
  body='''<article class="sr-content sr702-page">
<section class="sr702-overview">
 <p class="sr702-lead"><strong>Переезд в Россию по программе «разделения ценностей»</strong> — удобный маршрут для иностранцев, разделяющих традиционные российские ценности. По этой программе можно получить <strong>РВП (разрешение на временное проживание) на три года без квоты и без экзамена по русскому языку, истории и законодательству России</strong>. Также для въезда можно запросить специальную частную визу на три месяца.</p>
 <p>Мы поможем определить, подходит ли программа вам и вашей семье, заранее подготовим документы для въезда и поможем последовательно пройти все необходимые процедуры в России.</p>
 <p class="sr702-strategy"><strong>Сначала индивидуальная стратегия — затем сопровождение по согласованному плану.</strong></p>
 <div class="sr702-benefits" aria-label="Особенности программы">
  <div><strong>3 месяца</strong><span>специальная однократная частная виза</span></div>
  <div><strong>Без квоты</strong><span>не нужно участвовать в «лотерее РВП»</span></div>
  <div><strong>Без экзамена</strong><span>языковой документ для этого РВП не требуется</span></div>
  <div><strong>На 3 года</strong><span>обычный срок выданного РВП</span></div>
 </div>
 <p><a class="btn btn-primary" data-analytics-event="consultation_click" href="/ru/consultations/">Проверить свой маршрут переезда →</a></p>
</section>
<nav class="sr702-toc" aria-label="Содержание">
 <strong>Пошаговый маршрут</strong>
 <div><a href="#step0">0. Подходит ли программа</a><a href="#step1">1. Виза и подготовка к выезду</a><a href="#step2">2. Прибытие в Россию</a><a href="#step3">3. Документы и процедуры</a><a href="#step4">4. Подача в МВД</a><a href="#life">После получения РВП</a><a href="#faq702">Частые вопросы</a></div>
</nav>
<section class="sr702-stage" id="step0">
 <div class="sr702-stage-head"><span class="sr702-number">00</span><div><span class="sr702-kicker">Начните здесь · предварительная проверка</span><h2>Узнайте, подходит ли вам программа</h2></div></div>
 <p>Программа рассчитана на иностранцев, которые разделяют российские традиционные ценности и хотят переехать жить в Россию из страны своего гражданства или постоянного проживания. Перечень государств и территорий определён распоряжением Правительства России № 2560-р. При подаче заявления потребуется указать мотивы переезда в соответствии с Указом 702.</p>
 <p>Для предварительного анализа важно узнать ваше гражданство, страну постоянного проживания, сведения о предыдущих поездках в Россию и составе семьи. Гражданство страны из списка <strong>само по себе не означает автоматического получения миграционного статуса — нужно собрать необходимые документы и пройти миграционные процедуры. Однако в нашей практике это наиболее предсказуемый способ получить РВП.</strong></p><p>Если вы уже законно находитесь в России, вы также можете воспользоваться программой, в том числе при наличии рабочей или туристической визы. Порядок подачи зависит от ваших документов и региона пребывания.</p>
 <details class="sr702-expand"><summary>Посмотреть полный список стран, участвующих в программе</summary>
 <p>Страны и территории, включённые в распоряжение Правительства РФ от 17.09.2024 № 2560-р.</p>
 <div class="sr702-countries">Австралия · Австрия · Албания · Андорра · Багамские Острова · Бельгия · Болгария · Великобритания (включая коронные владения и заморские территории) · Германия · Греция · Дания · Ирландия · Исландия · Испания · Италия · Канада · Кипр · Латвия · Литва · Лихтенштейн · Люксембург · Мальта · Микронезия · Монако · Нидерланды · Новая Зеландия · Норвегия · Польша · Португалия · Республика Корея · Румыния · Сан-Марино · Северная Македония · Сингапур · Словения · США · Тайвань (Китай) · Украина · Финляндия · Франция · Хорватия · Черногория · Чехия · Швейцария · Швеция · Эстония · Япония.</div>
 <p>Порядок въезда для отдельных гражданств, в частности Украины, имеет особенности.</p>
 </details>
 <details class="sr702-expand"><summary>Если вы живёте не в стране своего гражданства</summary><p>Если у вас есть гражданство страны из перечня, но вы живёте в другой стране, вы также можете участвовать в программе. При оформлении частной визы могут быть особенности: при обращении в третьей стране потребуется подтвердить право законного длительного проживания — в ряде консульств более шести месяцев. Лучше заранее согласовать план действий с миграционным юристом и подготовить документы из страны вашего гражданства.</p></details>
 <p class="sr702-note"><strong>Наш подход:</strong> сначала составляем план действий и календарь, затем оформляем визу и покупаем билеты. Так мы последовательно движемся к вашей цели — получению РВП и переезду в Россию.</p>
</section>
<section class="sr702-stage" id="step1">
 <div class="sr702-stage-head"><span class="sr702-number">01</span><div><span class="sr702-kicker">До выезда из вашей страны</span><h2>Получение визы и подготовка документов</h2></div></div>
 <div class="sr702-with-image sr702-with-image--visa"><div>
 <p>По Указу 702 для въезда предусмотрена <strong>однократная обыкновенная частная виза на три месяца</strong>. Важно правильно подготовить документы, указать предполагаемые даты поездки и запросить подходящий срок. Даты действия визы фиксируются в решении российского консульства.</p>
 <p><strong>Самое важное — получить справку об отсутствии судимости ещё до поездки.</strong> Для подачи на РВП в России справка действует <strong>три месяца с момента выдачи</strong>. Документ нужно оформить с апостилем либо другой предусмотренной легализацией. Нотариальный перевод на русский язык вы сделаете уже в России.</p><p><strong>Особое внимание — электронным справкам и электронным апостилям.</strong> Если в вашей стране справку выдают только в электронном виде, заранее обсудите оформление с миграционным юристом. При подтверждении подлинности таких документов в разных регионах России возникают нюансы, которые лучше решить ещё до выезда.</p>
 <p>Подготовьте паспорт, документы о проживании, заявление о мотивах переезда и визовую анкету; проверьте правила того консульства, куда планируете обращаться.</p>
 </div><figure class="sr702-visa-figure"><span class="sr702-visa-crop"><img src="/assets/decree702-stage1-visa.jpg" width="595" height="842" loading="lazy" alt="Пример частной визы по Указу 702 с закрытыми личными данными"></span><figcaption>Пример частной визы по Указу 702. Персональные данные закрыты.</figcaption></figure></div>
 <details class="sr702-expand"><summary>Очень важно на этом этапе</summary><ul><li>Указывайте правильные даты поездки и запрашиваемый срок визы. Из-за ошибок при самостоятельной подаче иногда выдают визу на более короткий срок.</li><li>Правильно рассчитывайте срок действия справки об отсутствии судимости: к дате подачи в МВД она должна оставаться действительной.</li><li>Если вы уже законно находитесь в России, порядок обращения за РВП может зависеть от региона пребывания и категории вашей визы.</li><li>Специальная частная виза разрешает один въезд. Если потребуется выехать во время рассмотрения заявления, для возвращения может понадобиться новая виза.</li></ul></details>
 <p class="sr702-note"><strong>Практический совет:</strong> сначала составьте план действий и календарь с учётом даты выдачи справки об отсутствии судимости, записи в консульство и подачи документов в МВД.</p>
</section>
<section class="sr702-stage" id="step2">
 <div class="sr702-stage-head"><span class="sr702-number">02</span><div><span class="sr702-kicker">Первые дни после пересечения границы</span><h2>Прибытие в Россию: что сделать в первую очередь</h2></div></div>
 <div class="sr702-with-image"><div>
 <p><strong>Добро пожаловать в Россию!</strong></p><p>После пересечения границы нужно спокойно, но оперативно выполнить миграционные формальности, чтобы сохранить возможность получения РВП.</p>
 <ul><li>Получите при въезде и сохраните миграционную карту. Не теряйте её.</li><li>Оформите <strong>миграционный учёт по месту пребывания</strong> (его часто называют регистрацией). В гостинице уведомление отправляет администрация не позднее следующего рабочего дня; при проживании в квартире общий срок — семь рабочих дней, уведомление обычно подаёт принимающая сторона. <strong>Важно не только подать уведомление, но и получить подтверждение его принятия МВД: отрывную часть или электронный документ.</strong></li><li>Подготовьте нотариально удостоверенные переводы иностранных документов.</li><li>Выберите регион, где действительно планируете проживать и подавать документы.</li><li>При необходимости займитесь СНИЛС, Госуслугами, мобильной связью и банком: это полезные бытовые шаги, но не универсальные условия получения РВП.</li></ul>
 </div><figure><div class="sr702-visual-crop sr702-visual-crop--arrival"><img src="/assets/decree702-stage2-arrival.jpg" width="680" height="720" loading="lazy" alt="Иллюстрация поездки семьи на самолёте в Россию"></div><figcaption>Переезд — это не только документы, но и начало новой жизни.</figcaption></figure></div>
 <details class="sr702-expand"><summary>Чего нельзя делать после прибытия</summary><ul><li><strong>Не покупайте фиктивную регистрацию.</strong> Регистрация должна соответствовать реальному месту пребывания; фиктивная постановка на учёт может повлечь серьёзную ответственность, вплоть до выдворения и запрета на въезд.</li><li>Не выбирайте регион подачи только потому, что там якобы быстрее принимают документы (не слушайте таких советов). РВП всегда связано с определённым субъектом РФ. Вы сможете путешествовать по России, но должны выбрать один регион для постоянного места жительства.</li></ul></details>
</section>
<section class="sr702-stage" id="step3">
 <div class="sr702-stage-head"><span class="sr702-number">03</span><div><span class="sr702-kicker">Подготовка к обращению в МВД</span><h2>Медицинские документы, переводы и заявление</h2></div></div>
 <div class="sr702-with-image"><div>
 <p>На этом этапе готовим заявление о выдаче РВП, проверяем иностранные документы и переводы, проходим медицинское освидетельствование, оформляем необходимые идентификационные номера и выполняем другие процедуры.</p>
 <p><strong>Медицинское освидетельствование для РВП нужно проходить в России</strong>, только в уполномоченных медицинских организациях. При въезде по специальной процедуре Указа 702 медицинские документы необходимо представить в МВД в течение 30 суток со дня въезда. При документально подтверждённых уважительных причинах законом предусмотрены исключения.</p>
 <p>В выбранном регионе узнаём адрес медицинского центра, уточняем график, организуем обязательную дактилоскопию и фотографирование. СНИЛС, ИНН и другие документы для дальнейшей жизни оформляем по необходимости.</p>
 </div><figure><div class="sr702-visual-crop sr702-visual-crop--documents"><img src="/assets/decree702-stage3-documents.png" width="569" height="376" loading="lazy" alt="Иллюстрация заполнения заявления и оформления документов"></div><figcaption>Подготовка и проверка комплекта до подачи заявления.</figcaption></figure></div>
 <details class="sr702-expand"><summary>Контрольный список для подготовки РВП</summary><ul><li>Паспорт и удостоверенный перевод.</li><li>Актуальная справка о наличии или отсутствии судимости, её легализация и перевод — по применимым требованиям.</li><li>Заявление с корректно сформулированными мотивами переезда по Указу 702.</li><li>Медицинские документы установленной формы.</li><li>Фотографии, государственная пошлина и иные подтверждения по действующему перечню МВД.</li><li>Документы о семье и об основаниях для подачи.</li></ul><p>Это ориентир для подготовки, а не закрытый юридический перечень. Перед подачей желательно сверить комплект с миграционным юристом. Для документов отдельных стран бывают особенности, в том числе расхождения в написании имени, фамилии, даты и места рождения.</p></details>
 <p class="sr702-note">Мы проверяем документы на соответствие требованиям <strong>до обращения в МВД</strong>: просроченные справки, неточные переводы и ошибки в заявлении часто стоят заявителю времени и могут снизить вероятность положительного решения.</p>
</section>
<section class="sr702-stage" id="step4">
 <div class="sr702-stage-head"><span class="sr702-number">04</span><div><span class="sr702-kicker">Личная подача и ожидание решения</span><h2>Обращение за РВП в МВД России</h2></div></div>
 <div class="sr702-with-image"><div>
 <p>Заявление на РВП подаётся в территориальное подразделение МВД в порядке, действующем в выбранном регионе России. Подача требует полного комплекта документов и соблюдения миграционных правил. Мы сопровождаем заявителя и взаимодействуем с должностными лицами.</p>
 <p><strong>Подтверждение принятия заявления в МВД — один из самых важных документов.</strong> Пункт 2 статьи 5 закона № 115-ФЗ позволяет законно дожидаться решения в России после окончания первоначальной визы, если МВД приняло заявление и необходимые документы на РВП. <strong>Такое продолжение законного пребывания нужно надлежащим образом оформить и получить подтверждающие документы.</strong> В разных регионах и для разных категорий виз возможны особенности оформления.</p>
 <p>Срок рассмотрения заявления определён законом; для обычной визовой процедуры действует срок до четырёх месяцев. На практике весь путь от подготовки документов и подачи до получения решения может занимать <strong>от двух до шести месяцев</strong>. Поэтому календарь переезда лучше составить заранее.</p>
 </div><figure><img src="/assets/decree702-stage4-mvd.png" width="851" height="549" loading="lazy" alt="Здание подразделения МВД России по вопросам миграции"><figcaption>Подача заявления и взаимодействие с МВД.</figcaption></figure></div>
 <details class="sr702-expand"><summary>Особенно важно на этом этапе</summary><ul><li>Уточняйте часы приёма, способ записи и требования к документам в компетентном подразделении.</li><li>Не используйте недостоверные сведения или фиктивную регистрацию.</li><li>Храните подтверждение подачи до получения РВП и оформления документов, подтверждающих дальнейшее пребывание.</li><li>Отдельно отслеживайте миграционный учёт по фактическому месту пребывания и своевременно продлевайте его, когда это требуется.</li><li>Если планируете поездку за пределы России во время рассмотрения заявления, заранее позаботьтесь об оформлении визы для возвращения.</li></ul></details>
</section>
<section class="sr702-stage sr702-final" id="life">
 <div class="sr702-stage-head"><span class="sr702-number">✓</span><div><span class="sr702-kicker">Следующий этап жизни в России</span><h2>После получения РВП: что меняется</h2></div></div>
 <p>При положительном решении и оформлении РВП вы получаете статус временно проживающего иностранного гражданина. Обычный срок РВП — три года. Это позволяет планировать жизнь, работу и развитие бизнеса в России в пределах условий вашего статуса, но сохраняет ряд обязанностей.</p>
 <details class="sr702-expand"><summary>Что важно знать после получения РВП?</summary><ul><li>Зарегистрируйтесь по месту жительства в установленном порядке. Никогда не используйте фиктивный миграционный учёт.</li><li>Вы сможете работать в субъекте РФ, где выдано РВП, с учётом установленных законом исключений.</li><li>Вы сможете путешествовать по всей России, сохраняя место жительства и регистрацию в регионе выдачи РВП. Смена региона проживания требует соблюдения специального порядка.</li><li>Ежегодно подтверждайте проживание в России и представляйте предусмотренные законом сведения о доходах.</li><li>Чтобы сохранить РВП, не находитесь за пределами России более шести месяцев суммарно за календарный год, кроме установленных законом исключений.</li><li><strong>Через восемь месяцев проживания по РВП можно подать заявление на ВНЖ</strong>, если выполнены установленные законом требования, включая экзамен, когда он обязателен. ВНЖ обычно выдаётся без ограничения срока.</li><li>На гражданство по общему основанию можно претендовать после пяти лет постоянного проживания <strong>со дня принятия решения о выдаче ВНЖ</strong>. Для отдельных категорий предусмотрены и другие основания.</li></ul></details>
</section>
<section class="sr702-voice">
 <p>«К нам обращаются разные люди: семьи с детьми, предприниматели, будущие фермеры, высококвалифицированные специалисты, те, кому комфортно жить и работать в России, и те, кто просто решил связать свою жизнь с Россией. Я хотел объяснить программу понятным языком: показать её возможности и предупредить о действиях, которые могут осложнить переезд. Мы поможем составить индивидуальную стратегию и пройти согласованные юридические этапы вместе с вами».</p>
 <p><strong>Лев Втюрин</strong><br>Основатель SalutRussie · более 20 лет юридической практики</p>
</section>
<section class="sr702-stage" id="faq702">
 <h2>Частые вопросы о переезде по Указу 702</h2>
 <details class="sr702-expand"><summary>Нужно ли знать русский язык?</summary><p><strong>Нет.</strong> Для РВП по Указу 702 не требуется документ о знании русского языка, истории и законодательства России. За три года вы сможете выучить русский язык на уровне, необходимом для дальнейшего оформления ВНЖ.</p></details>
 <details class="sr702-expand"><summary>Можно ли переехать всей семьёй?</summary><p><strong>Да, конечно.</strong> Мы уже помогали переезжать в Россию большим и маленьким семьям из Европы и США. Маршрут и документы заранее готовим для каждого члена семьи.</p></details>
 <details class="sr702-expand"><summary>Можно ли обратиться за РВП, если я уже нахожусь в России?</summary><p><strong>Да.</strong> Важно знать, в каком регионе вы находитесь и по какой визе въехали. В отдельных регионах существуют особенности приёма документов и требования к справке об отсутствии судимости, включая её форму и способ подтверждения подлинности.</p></details>
 <details class="sr702-expand"><summary>Обязательно ли получать специальную визу по Указу 702?</summary><p><strong>Нет, не обязательно.</strong> Такая виза удобна для стандартного маршрута, но обратиться за РВП по Указу 702 можно и при законном нахождении в России по другой визе, включая электронную, туристическую, деловую или рабочую. В разных регионах есть особенности, поэтому с другой визой лучше заранее обсудить порядок подачи с миграционным юристом.</p></details>
 <details class="sr702-expand"><summary>Что делать, если срок визы заканчивается, а РВП ещё не выдано?</summary><p><strong>Пункт 2 статьи 5 закона № 115-ФЗ</strong> позволяет ожидать решение МВД в России, если заявление и необходимые документы на РВП уже приняты. Дальнейшее законное пребывание нужно документально оформить в МВД в применимом порядке. Не откладывайте это до последнего дня визы.</p></details>
 <details class="sr702-expand"><summary>Когда можно получить ВНЖ и гражданство?</summary><p>По общему маршруту заявление на ВНЖ можно подать <strong>не ранее чем через восемь месяцев проживания по РВП</strong>, если выполнены требования закона. Большинство ВНЖ выдаются без ограничения срока. На гражданство в общем порядке можно претендовать после <strong>пяти лет проживания со дня решения о выдаче ВНЖ</strong>. При наличии специальных оснований условия могут отличаться.</p></details>
</section>
<section class="sr702-bottom"><h2>Планируете переезд в Россию?</h2><p>Опишите ваше гражданство, страну проживания, состав семьи и предполагаемую дату переезда. Мы определим возможный правовой маршрут, документы и основные риски до начала затрат.</p><a class="btn btn-primary" data-analytics-event="consultation_click" href="/ru/consultations/">Получить консультацию по Указу 702 →</a></section>
<section class="sr702-sources"><h2>Правовая основа и подробная инструкция</h2>
 <ul><li><a href="https://www.garant.ru/products/ipo/prime/doc/409448235/">Указ Президента РФ от 19.08.2024 702</a>.</li>
 <li><a href="https://www.garant.ru/products/ipo/prime/doc/410316959/">Распоряжение Правительства РФ от 17.09.2024 № 2560-р</a> — перечень государств.</li>
 <li><a href="https://www.consultant.ru/document/cons_doc_LAW_37868/">Федеральный закон от 25.07.2002 № 115-ФЗ «О правовом положении иностранных граждан в Российской Федерации»</a>.</li>
 <li>Приказы МВД России, регулирующие порядок подачи и рассмотрения документов на РВП.</li></ul>
 <p>Для подробного юридического анализа читайте <a href="/ru/knowledge/articles/rvp-shared-values-702/">экспертную статью «РВП по Указу 702: условия, документы и правовые риски»</a>. Здесь изложен практический путь переезда и юридического сопровождения.</p>
</section>
</article>'''
 else:
  body='''<article class="sr-content"><p class="sr-meta">Texte sur le site de la présidence consulté le 21 novembre 2026 · Vérifiez la version en vigueur avant toute demande</p><p>Le décret présidentiel russe n° 702 du 19 août 2024 prévoit une voie spécifique pour certaines personnes qui souhaitent s’installer en Russie. Il ouvre un droit de <strong>déposer une demande</strong> de permis de séjour temporaire (RVP), sans garantir l’obtention du permis ou du visa.</p><h2>Ce que prévoit le décret</h2><ul><li>Une demande de RVP hors quota, sans document attestant la connaissance de la langue russe, de l’histoire et du droit russes, sous réserve des conditions du décret.</li><li>Un visa privé ordinaire à entrée unique de trois mois, délivré sur décision du responsable du poste diplomatique ou consulaire dans les cas prévus.</li><li>L’examen du dossier selon la procédure applicable, avec les motifs de refus prévus à l’article 7 de la loi fédérale n° 115-FZ.</li></ul><p>Lisez le <a href="SOURCE">texte du décret n° 702 sur le site de la présidence</a>, sa <a href="PUBLICATION">notice de publication officielle</a> et la <a href="COUNTRIES">liste gouvernementale des États concernés</a> (ordonnance n° 2560-r). La nationalité, le lieu de résidence permanente et la version actuelle de cette liste doivent être vérifiés pour chaque personne.</p><h2>Préparer votre dossier</h2><ol><li>Notez votre nationalité, votre résidence permanente et le lieu prévu pour la demande de visa.</li><li>Décrivez les motifs de votre projet et les membres de votre famille concernés.</li><li>Rassemblez les informations sur vos passeports, vos séjours et vos entrées précédentes en Russie.</li><li>Vérifiez les conditions du décret et les éventuels motifs de refus.</li><li>Confirmez les pièces, l’autorité compétente et les délais selon les règles en vigueur avant le dépôt.</li></ol><h2>Questions fréquentes</h2><h3>Le visa est-il garanti ?</h3><p>Non. Le décret prévoit une décision consulaire ; il ne garantit pas une réponse favorable.</p><h3>Le RVP est-il automatique ?</h3><p>Non. Le dossier reste soumis à l’examen et aux motifs de refus applicables.</p><h3>La nationalité suffit-elle ?</h3><p>Non. Il faut examiner toutes les conditions et les faits du dossier.</p><p class="sr-note">Ce guide présente le cadre général. La liste des pièces et les délais doivent être confirmés pour votre situation.</p>

</article>'''
 body=body.replace('SOURCE',source).replace('PUBLICATION',publication).replace('COUNTRIES',countries)
 return shell(lang,url,title,desc,heading(lang,title,desc,'УКАЗ 702 · РАЗДЕЛЕНИЕ ЦЕННОСТЕЙ · ИДЕОЛОГИЧЕСКАЯ ПРОГРАММА' if ru else 'DÉCRET 702')+body+cta(lang))

def b2b_page(lang,part):
 label,title,desc,body=get_page(lang,part)
 url=path(lang,'for-business'+('/'+part if part!='index' else ''))
 email='mailto:salutrussie@salutrussie.ru?subject=Business%20enquiry'
 action={'ru':'Написать о проекте','en':'Discuss a project','fr':'Présenter votre projet'}[lang]
 close=f'<section class="sr-sec"><div class="sr-width"><div class="sr-cta"><div><h2>{action}</h2><p>{"Опишите задачу без персональных данных работников. Мы предложим следующий шаг и согласуем объём работы." if lang=="ru" else "Send a short project brief without workers’ personal data. We will agree the next step and scope." if lang=="en" else "Envoyez un bref descriptif sans données personnelles des travailleurs. Nous conviendrons de la suite."}</p></div><a class="btn btn-primary" href="{email}">{action} →</a></div></div></section>'
 return shell(lang,url,title,desc,heading(lang,title,desc,label)+body+close)


def migration_hub_ru():
 title='Переезд в Россию'
 desc='Мы поможем вам выбрать законный путь переезда и проживания в России, оформить необходимые документы и защитим ваши права в сложных миграционных ситуациях.'
 body='''<div class="sr-top sr-migration-top"><div class="sr-width">
 <div class="sr-eyebrow">МИГРАЦИОННАЯ ПОМОЩЬ</div>
 <h1>Переезд в Россию</h1>
 <p>Мы поможем вам выбрать законный путь переезда и проживания в России, оформить необходимые документы и защитим ваши права в сложных миграционных ситуациях.</p>
 <div class="sr-migration-actions">
  <a class="btn btn-primary" data-analytics-event="consultation_click" href="/ru/consultations/">Обсудить мою ситуацию →</a>
  <a class="sr-migration-jump" href="#migration-services">Посмотреть услуги ↓</a>
 </div>
</div></div>
<section class="sr-sec sr-migration-hub" id="migration-services"><div class="sr-width">
 <span class="eyebrow">НАЧНИТЕ С ВАШЕЙ ЗАДАЧИ</span>
 <h2 class="sr-migration-section-heading">Выберите миграционную услугу</h2>
 <a class="sr-migration-feature" href="/ru/migration/decree-702/" aria-label="Подробнее о переезде по Указу 702">
  <span class="sr-migration-feature-icon" aria-hidden="true">✳</span>
  <span class="sr-migration-feature-copy"><span class="sr-migration-feature-label">СПЕЦИАЛЬНАЯ ПРОГРАММА</span><strong>Переезд в Россию по Указу 702</strong><span class="sr-migration-feature-aliases">«Разделение ценностей» · «идеологическая программа»</span><span>Проверим применимость программы, определим правовой маршрут и согласуем сопровождение.</span></span>
  <span class="sr-migration-feature-arrow" aria-hidden="true">↗</span>
 </a>
 <h2 class="sr-migration-subheading">Другие миграционные услуги</h2>
 <div class="sr-migration-links">
  <a class="sr-migration-service" href="/ru/migration/visas/"><span><strong>Визы в Россию</strong><small>Подберём подходящую визу и сопроводим её оформление</small></span><span aria-hidden="true">↗</span></a>
  <a class="sr-migration-service" href="/ru/migration/rvp/"><span><strong>РВП в России</strong><small>Поможем оформить разрешение на временное проживание (РВП)</small></span><span aria-hidden="true">↗</span></a>
  <a class="sr-migration-service" href="/ru/migration/vnzh/"><span><strong>ВНЖ в России</strong><small>Поможем получить вид на жительство (ВНЖ) для постоянного проживания в России</small></span><span aria-hidden="true">↗</span></a>
  <a class="sr-migration-service" href="/ru/migration/citizenship/"><span><strong>Гражданство России</strong><small>Определим подходящее основание, подготовим документы и проведём вас по этапам получения гражданства</small></span><span aria-hidden="true">↗</span></a>
  <a class="sr-migration-service sr-migration-service--protection" href="/ru/migration/disputes/"><span><strong>Защита в суде и государственных органах (МВД, ФСБ)</strong><small>Отказы, жалобы, выдворение и депортация, административные и судебные споры</small></span><span aria-hidden="true">↗</span></a>
 </div>
 <div class="sr-migration-special"><h2>Специальные ситуации</h2><p>Для студентов и семей порядок оформления может отличаться.</p>
  <div class="sr-migration-special-links"><a href="/ru/migration/students/">Учёба в России и РВПО <span aria-hidden="true">↗</span></a><a href="/ru/migration/family/">Семейный переезд <span aria-hidden="true">↗</span></a></div>
 </div>
</div></section>
<section class="sr-sec alt sr-migration-explain"><div class="sr-width">
 <h2>Как мы работаем</h2>
 <ol class="sr-migration-steps"><li><span>01</span><strong>Разбираем ваши планы</strong><p>Уточняем ваше гражданство, текущий статус, сроки документов и цели поездки или переезда в Россию.</p></li><li><span>02</span><strong>Готовим миграционную стратегию</strong><p>Разрабатываем стратегию под вашу ситуацию и составляем пошаговый план действий.</p></li><li><span>03</span><strong>Сопровождаем до результата</strong><p>Помогаем с документами и обращениями, сопровождаем вас на каждом согласованном этапе.</p></li></ol>
 <details class="sr-migration-prep"><summary>Что подготовить к первой консультации? <span aria-hidden="true">+</span></summary>
  <div class="sr-migration-prep-content"><p>Для начала достаточно описать вашу ситуацию и планы своими словами. Если есть возможность, подготовьте:</p>
   <ul><li>Гражданство и место постоянного проживания каждого заявителя.</li><li>Ваши цели, пожелания и предполагаемые даты въезда в Россию.</li><li>Копии имеющихся документов (можете прислать их заранее или мы отдельно запросим необходимое).</li><li>Сведения о семье, работе, учёбе или бизнесе, которые могут влиять на ваши планы.</li></ul>
   <p class="sr-migration-prep-note">Дополнительно: <a href="/ru/knowledge/articles/how-to-choose-residence/">как выбрать основание для проживания в России →</a></p>
  </div>
 </details>
</div></section>
<section class="sr-sec sr-migration-close"><div class="sr-width"><div class="sr-cta"><div>
 <h2>Не знаете, с чего начать?</h2>
 <p class="sr-migration-close-lead">Расскажите о ваших планах.</p>
 <p>Я — Лев Втюрин, основатель SalutRussie. Более 20 лет юридической практики. Лично отвечаю за миграционную стратегию и качество сопровождения каждого проекта.</p>
 <div class="sr-migration-route" aria-label="Этапы работы"><span>Опишите ситуацию</span><span aria-hidden="true">→</span><span>Подготовим миграционную стратегию</span><span aria-hidden="true">→</span><span>Согласуем тариф</span><span aria-hidden="true">→</span><span>Приступим к реализации плана</span></div>
 </div><a class="btn btn-primary" data-analytics-event="consultation_click" href="/ru/consultations/">Обсудить мою ситуацию →</a></div></div></section>'''
 return shell('ru',path('ru','migration'),title,desc,body)

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
  if ru and slug=='business':
   sub.append(('business/tax-consulting',{'symbol':'↗','ru':('Налоговое консультирование','Налоговое консультирование','Правовая и налоговая оценка вопросов бизнеса с иностранным участием.')}))
  if ru and slug=='investments':
   sub=[
    ('investments/legal-due-diligence',{'symbol':'↗','ru':('Юридическая проверка и сопровождение инвестиционного проекта','Юридическая проверка и сопровождение инвестиционного проекта','Проверка актива, сделки и юридическое сопровождение проекта.')}),
    ('investments/project-selection',{'symbol':'↗','ru':('Подбор инвестиционных проектов','Подбор инвестиционных проектов','Поиск и первичный отбор вариантов по согласованным критериям.')})
   ]
  if ru and slug=='relocation':
   sub=[
    ('relocation/administrative-procedures',{'symbol':'↗','ru':('Административные процедуры','Административные процедуры','Документы, контроль сроков и организация обращений.')}),
    ('relocation/everyday-life',{'symbol':'↗','ru':('Бытовые вопросы','Бытовые вопросы','Практические вопросы жилья и адаптации после переезда.')}),
    ('relocation/russian-language',{'symbol':'↗','ru':('Изучение русского языка','Изучение русского языка','Подбор подходящего формата обучения для взрослых и детей.')})
   ]
  rich=rich_section(lang,slug)
  if ru and slug=='investments':
   info=(info[0],info[1],'Подбор инвестиционных проектов, юридическая проверка и сопровождение сделок в России.')
  write(url,migration_hub_ru() if ru and slug=='migration' else basic_page(lang,url,info[1],info[2],sub if sub else None,rich))
  for part in SUBPAGES.get(slug,[]):
   lab=SUBLABEL[part][0 if ru else 1];desc=DETAILS[part][lang][0]
   rich_detail=detail_rich(lang,part)
   if ru and slug=='investments' and part=='legal-due-diligence':
    lab="Юридическая проверка и сопровождение инвестиционного проекта";desc="Проверяем актив, контрагента и условия сделки, затем сопровождаем согласованные этапы инвестиционного проекта."
    rich_detail="<section class=\"sr-sec\"><div class=\"sr-width sr-b2b-copy\"><h2>Проверка и сопровождение в одном процессе</h2><p>Юридическая проверка не гарантирует прибыль и не заменяет самостоятельную финансовую оценку инвестиции. Состав сопровождения зависит от сделки.</p><ul><li>Проверяем стороны сделки, полномочия, права на активы, ограничения, существенные договоры и споры.</li><li>Согласуем условия приобретения или участия, этапы оплаты, передачу прав и необходимые гарантии.</li><li>Готовим или проверяем договоры и сопровождаем согласованные юридические этапы реализации проекта.</li><li>Фиксируем контрольные точки, отчётность, ответственность сторон и условия выхода из проекта.</li></ul><p class=\"sr-note\">Состав услуги, привлечение профильных специалистов и стоимость согласуются индивидуально до начала работы.</p></div></section>"
   write(path(lang,f'{slug}/{part}'),basic_page(lang,path(lang,f'{slug}/{part}'),lab,desc,rich=rich_detail))
 for slug,d in PROGRAMS.items():
  title=d[lang][1];desc=d[lang][2];url=path(lang,'migration/'+slug)
  rich=detail_rich(lang,'migration-disputes' if slug=='disputes' else slug)
  write(url,basic_page(lang,url,title,desc,rich=rich))

RU_ADDITIONAL_SERVICE_PAGES=[["business/tax-consulting","Налоговое консультирование","Налоговые вопросы открытия и ведения бизнеса иностранцами в России.","<section class=\"sr-sec\"><div class=\"sr-width sr-b2b-copy\"><h2>С чем поможем</h2><p>Налоги влияют на выбор формы бизнеса, структуру платежей и содержание договоров. Мы помогаем определить вопросы и риски до принятия решений; специализированный бухгалтерский учёт или подготовка отчётности согласуются отдельно.</p><ul><li>Выбор и предварительная оценка системы налогообложения с учётом деятельности и статуса предпринимателя.</li><li>Налоговые последствия договоров, расчётов с партнёрами и участия иностранного собственника.</li><li>Подготовка правовых вопросов к бухгалтеру или налоговому специалисту, согласование необходимых документов.</li></ul><p class=\"sr-note\">Состав услуги, привлечение профильных специалистов и стоимость согласуются индивидуально до начала работы.</p></div></section>"],["investments/project-selection","Подбор инвестиционных проектов","Поиск и предварительный отбор инвестиционных проектов в России под цели и критерии клиента.","<section class=\"sr-sec\"><div class=\"sr-width sr-b2b-copy\"><h2>Как организуем подбор</h2><p>Подбор — это поиск подходящих для рассмотрения вариантов, а не обещание наличия конкретного объекта, доходности или одобрения сделки. Предложения и условия участия проверяются отдельно.</p><ul><li>Уточним инвестиционные цели, бюджет, регион, отрасль, желаемый формат участия и допустимые риски.</li><li>Определим критерии отбора и доступные для рассмотрения проекты или активы; проверим полноту исходной информации.</li><li>Подготовим перечень вопросов продавцу или партнёру, а перед сделкой согласуем юридическую проверку и сопровождение.</li></ul><p class=\"sr-note\">Состав услуги, привлечение профильных специалистов и стоимость согласуются индивидуально до начала работы.</p></div></section>"],["relocation/administrative-procedures","Административные процедуры","Помощь с организацией административных процедур после переезда в Россию.","<section class=\"sr-sec\"><div class=\"sr-width sr-b2b-copy\"><h2>Что можно организовать</h2><p>После въезда в Россию возникают разные административные задачи: адрес, документы, уведомления и обращения. Перечень действий зависит от статуса человека и региона; решения принимаются уполномоченными органами.</p><ul><li>План обращений в государственные органы и контроль важных сроков.</li><li>Подготовку перечня документов, заявлений и необходимых подтверждений.</li><li>Сопровождение предусмотренных законом административных действий по согласованному поручению.</li></ul><p class=\"sr-note\">Состав услуги, привлечение профильных специалистов и стоимость согласуются индивидуально до начала работы.</p></div></section>"],["relocation/everyday-life","Бытовые вопросы","Практическая организация повседневных вопросов при переезде и адаптации в России.","<section class=\"sr-sec\"><div class=\"sr-width sr-b2b-copy\"><h2>С чем можно обратиться</h2><p>Мы поможем составить понятный план бытовых задач и определить, какие вопросы решаются непосредственно, а для каких нужны отдельные исполнители. Условия их участия согласуем заранее.</p><ul><li>Ориентирование в вопросах жилья, аренды и взаимодействия с собственником.</li><li>Организация первых практических шагов: связь, документы и необходимые бытовые сервисы.</li><li>Составление индивидуального плана прибытия семьи, учёта потребностей детей и сроков переезда.</li></ul><p class=\"sr-note\">Состав услуги, привлечение профильных специалистов и стоимость согласуются индивидуально до начала работы.</p></div></section>"],["relocation/russian-language","Изучение русского языка","Помощь с выбором формата изучения русского языка при переезде в Россию.","<section class=\"sr-sec\"><div class=\"sr-width sr-b2b-copy\"><h2>Как поможем начать</h2><p>Помогаем с ориентирами и подбором формата обучения; проведение занятий преподавателем и стоимость обучения оговариваются отдельно. Требования к языковым экзаменам проверяются для конкретного миграционного основания.</p><ul><li>Определить цель обучения: бытовое общение, работа, учёба или подготовка к предусмотренным законом проверкам.</li><li>Подобрать подходящий формат: занятия индивидуально, в группе или дистанционно.</li><li>Составить план обучения под сроки переезда и особенности членов семьи.</li></ul><p class=\"sr-note\">Состав услуги, привлечение профильных специалистов и стоимость согласуются индивидуально до начала работы.</p></div></section>"]]
def extra_service_pages_ru():
 for tail,title,desc,rich in RU_ADDITIONAL_SERVICE_PAGES:
  url=path('ru',tail)
  body=heading('ru',title,desc,'Услуги')+rich+cta('ru')
  write(url,shell('ru',url,title,desc,body))

def consultations(lang):
 ru=lang=='ru'
 entries=[('migration','Переезд в Россию','S’installer en Russie','РВП, ВНЖ, Указ 702, визы и гражданство','RVP, VNZh, décret 702, visas, nationalité'),('real-estate','Недвижимость','Immobilier','Аренда, договоры, покупка и юридическая проверка','Location, achat et contrats'),('business','Бизнес и инвестиции','Entreprises et investissements','Создание компании, инвестиционные сделки и сопровождение','Création de société, projets et investissements'),('legal','Вопросы к юристу','Questions juridiques','Любые вопросы к российскому юристу','Documents, contentieux et questions spécifiques')]
 s=heading(lang,'Выберите вид консультации' if ru else 'Choisissez votre consultation','Выберите направление, затем напишите нам. Стоимость, формат и объём согласуем до оплаты.' if ru else 'Choisissez un domaine. Nous confirmerons le format, le périmètre et le prix avant paiement.',LANGS[lang]['consult'])
 s+='<section class="sr-sec"><div class="sr-width"><div class="sr-contact-list">'
 for slug,r,f,rd,fd in entries:
  name=r if ru else f;summary=rd if ru else fd
  text=(f'Здравствуйте! Обращаюсь с сайта SalutRussie. Тема: {name}. Хочу описать свою ситуацию и узнать о возможных вариантах помощи.' if ru else f'Bonjour ! Je vous contacte via SalutRussie au sujet de : {name}. Je souhaite décrire ma situation et connaître les possibilités d’accompagnement.')
  wa='https://wa.me/79685341915?text='+quote(text)
  subject=quote(('Обращение с сайта SalutRussie — ' if ru else 'Demande depuis SalutRussie — ')+name)
  email='mailto:salutrussie@salutrussie.ru?subject='+subject+'&body='+quote(text)
  intro='Выберите, как вам удобнее связаться с нами:' if ru else 'Choisissez votre moyen de contact :'
  mail_label='Электронная почта' if ru else 'E-mail'
  caption='Для Telegram можно скопировать текст обращения и вставить его в переписку:' if ru else 'Pour Telegram, copiez ce texte et collez-le dans la conversation :'
  copy_label='Скопировать текст' if ru else 'Copier le texte'
  s+=f"""<details class="sr-contact-details"><summary class="sr-contact-choice"><strong>{esc(name)} <span aria-hidden="true">⌄</span></strong><span>{esc(summary)}</span></summary><div class="sr-contact-channels"><p>{intro}</p><div class="sr-channel-links"><a href="{esc(wa)}" target="_blank" rel="noopener noreferrer" data-analytics-event="consultation_outbound">WhatsApp ↗</a><a href="https://t.me/lev_vt" target="_blank" rel="noopener noreferrer" data-analytics-event="consultation_outbound">Telegram ↗</a><a href="{esc(email)}" data-analytics-event="consultation_outbound">{mail_label} ↗</a></div><p class="sr-channel-caption">{caption}</p><div class="sr-copy-row"><span class="sr-draft" id="draft-{slug}">{esc(text)}</span><button class="sr-button sr-copy-topic" type="button" data-copy-target="draft-{slug}" aria-label="{copy_label}">{copy_label}</button></div></div></details>"""
 s+='</div><p class="sr-note">'+('Ваше обращение ни к чему вас не обязывает. Опишите свою ситуацию или задайте вопрос своими словами — так, как вам удобно. Если для решения вашего вопроса потребуется платная консультация или другая услуга, мы заранее сообщим вам стоимость.' if ru else 'Votre premier message ne vous engage à rien. Décrivez brièvement votre situation sans joindre de documents sensibles. Les honoraires d’une éventuelle consultation sont annoncés avant votre décision.')+'</p>'
 s+=f'<p style="margin-top:28px"><a class="btn btn-ghost" href="{path(lang,"pricing")}">{"Как определяется стоимость →" if ru else "Comprendre les honoraires →"}</a></p></div></section>'
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
  kind_label=('Инструкция' if ru else 'Guide') if a['kind']=='guide' else ('Статья' if ru else 'Article')
  s+=f'<a class="sr-card sr-result" data-topic="{a["topic"]}" data-format="{a["kind"]}" data-index="{esc(blob)}" href="{href}"><small>{kind_label}</small><h3>{esc(title)}</h3><p>{esc(summary)}</p><span class="sr-link">{LANGS[lang]["more"]}</span></a>'
 if ru:
  for a in EXPERT_ARTICLES:
   blob=' '.join((a['title'],a['summary'],a['primary_query'],*a['related_queries']))
   s+=f'<a class="sr-card sr-result expert-card" data-topic="{a["topic"]}" data-format="article" data-index="{esc(blob)}" href="{a["url"]}"><small>Экспертная статья · 2026</small><h3>{esc(a["title"])}</h3><p>{esc(a["summary"])}</p><span class="sr-link">Читать статью →</span></a>'
 s+='</div><div id="sr-empty" class="sr-kb-empty sr-hidden">'+('По запросу ничего не найдено.' if ru else 'Aucun résultat trouvé.')+'</div><p class="sr-note">'+('Материалы содержат общую информацию. Перед решением по конкретному делу проверьте действующие нормы и документы.' if ru else 'Ces textes présentent des informations générales. Vérifiez les règles et les documents applicables à votre situation.')+'</p></div></section>'
 return shell(lang,path(lang,'knowledge'),'Полезная информация' if ru else 'Informations utiles','Экспертные статьи и гайды для иностранцев в России' if ru else 'Ressources et guides pour les étrangers en Russie',s)

def article_page(lang,a):
 ru=lang=='ru';title,summary,_=a[lang];url=path(lang,'knowledge/articles/'+a['slug']);s=heading(lang,title,summary,'ПОЛЕЗНАЯ ИНФОРМАЦИЯ' if ru else 'INFORMATIONS UTILES')
 article_html=ARTICLES_HTML[a['slug']][lang]
 faq_heading='<h2>Частые вопросы</h2>' if ru else '<h2>Questions fréquentes</h2>'
 if article_html.count(faq_heading)!=1: raise ValueError(f'Missing FAQ insertion point: {lang} {a["slug"]}')
 article_html=article_html.replace(faq_heading,ADDENDA[a['slug']][lang]+faq_heading,1)
 table_label='Таблица: прокрутите по горизонтали' if ru else 'Tableau : défilement horizontal'
 article_html=article_html.replace('<table>',f'<div class="sr-table-scroll" tabindex="0" role="region" aria-label="{table_label}"><table>').replace('</table>','</table></div>')
 s+='<article class="sr-content">'+article_html+'</article>'
 return shell(lang,url,title,summary,s+cta(lang),article=True)

def expert_article_page(a):
 url=a['url']
 body=heading('ru',a['title'],a['summary'],'ЭКСПЕРТНАЯ СТАТЬЯ')
 body+='<article class="sr-content expert-shell">'+render_expert_article(a['slug'])+'</article>'
 return shell('ru',url,a['seo_title'],a['meta_description'],body+cta('ru'),article=True,ru_only=True,structured=expert_article_schema(a['slug'],ORIGIN+url))

def privacy(lang):
 notice=data_notice(lang)
 s=heading(lang,notice['title'],notice['description'])+notice['body']
 return shell(lang,path(lang,'privacy'),notice['title'],notice['description'],s,noindex=True)

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
 if lang=='ru':extra_service_pages_ru()
 write(path(lang,'services'),services_ru() if lang=='ru' else basic_page(lang,path(lang,'services'),'Tous nos services','Choisissez le domaine qui correspond à votre projet.',list(SECTIONS.items())))
 write(path(lang,'consultations'),consultations(lang))
 write(path(lang,'knowledge'),knowledge(lang))
 for a in ARTICLES:write(path(lang,'knowledge/articles/'+a['slug']),article_page(lang,a))
 if lang=='ru':
  for a in EXPERT_ARTICLES:write(a['url'],expert_article_page(a))
 write(path(lang,'privacy'),privacy(lang))
 legacy_map={'ru':{'o-kompanii-ru.html':('about','О нас','Команда SalutRussie и наш подход к работе'), 'tarify-ru.html':('pricing','Тарифы','Тарифы и услуги SalutRussie'),'dekret-702-ru.html':('migration/decree-702','Указ 702','Переезд в Россию по Указу 702'),'kontakty-ru.html':('contacts','Контакты','Связаться со специалистами SalutRussie'),'otzyvy-ru.html':('reviews','Отзывы','Отзывы клиентов SalutRussie')},'fr':{'o-kompanii.html':('about','Notre équipe','Notre cabinet et notre méthode'),'tarify.html':('pricing','Tarifs','Les services et tarifs de SalutRussie'),'dekret-702.html':('migration/decree-702','Décret n° 702','S’installer en Russie avec le décret 702'),'kontakty.html':('contacts','Contact','Contactez SalutRussie'),'otzyvy.html':('reviews','Avis','Témoignages des clients SalutRussie')}}
 for old,(slug,title,desc) in legacy_map[lang].items():
  if slug=='reviews' and not REVIEWS_ENABLED:
   continue  # Hide unverified testimonials in both languages until owner approval.
  if slug=='pricing': page=pricing_ru() if lang=='ru' else pricing_fr()
  elif slug=='about': page=about_ru() if lang=='ru' else about_fr()
  elif slug=='contacts': page=contacts_page(lang)
  elif slug=='migration/decree-702': page=decree_page(lang)
  else: page=legacy(lang,old,path(lang,slug),title,desc)
  write(path(lang,slug),page)

for lang in ('ru','en','fr'):
 for part in ('index','employers','recruitment-partners'):
  write(path(lang,'for-business'+('/'+part if part!='index' else '')),b2b_page(lang,part))

# All links and assets are converted to relative URLs so the full dist can be previewed directly by opening index.html.
all_pages=list(OUT.rglob('*.html'))
for file in all_pages:
 root_html=file.read_text(encoding='utf-8');prefix=os.path.relpath(OUT,file.parent).replace('\\','/')
 if prefix=='.':prefix='.'
 root_html=re.sub(r'(?<=["\'])/(assets|ru|fr|en)/',lambda m: prefix+'/'+m.group(0).lstrip('/'),root_html)
 file.write_text(root_html,encoding='utf-8')
landing='''<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0;url=ru/index.html"><title>SalutRussie — открыть сайт</title></head><body><a href="ru/index.html">Открыть русскую версию SalutRussie</a> · <a href="fr/index.html">Version française</a></body></html>'''
(OUT/'index.html').write_text(landing,encoding='utf-8')
(OUT/'404.html').write_text('<!doctype html><html lang="ru"><meta charset="utf-8"><meta name="robots" content="noindex"><title>404</title><body>Страница не найдена. <a href="/ru/">Главная</a></body></html>',encoding='utf-8')
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
