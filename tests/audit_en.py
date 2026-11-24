#!/usr/bin/env python3
"""Read-only static audit of the complete English site, including cross-language navigation."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote, parse_qs
import json
import re

ROOT = Path(__file__).resolve().parents[1]
EN = ROOT / "v3" / "en"
CYR = re.compile(r"[А-Яа-яЁё]")
OLD_ABBR = re.compile(r"\b(?:TRP|PRP|VNZH)\b")
COMPANY = "ООО «ИННОВАЦИОННЫЕ ПРАВОВЫЕ РЕШЕНИЯ»"

class Document(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.lang = ""
        self.main = False
        self.main_count = 0
        self.hidden = 0
        self.title_open = False
        self.title = ""
        self.h1 = 0
        self.main_text = []
        self.links = []
        self.ids = []
        self.meta = {}
        self.canonical = []
        self.alternates = []
        self.images = []
        self.feed(source)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html": self.lang = a.get("lang", "")
        if tag == "main": self.main = True; self.main_count += 1
        if tag == "title": self.title_open = True
        if tag in ("script", "style"): self.hidden += 1
        if tag == "h1": self.h1 += 1
        if a.get("id"): self.ids.append(a["id"])
        if tag == "meta":
            k = a.get("name") or a.get("property")
            if k: self.meta.setdefault(k, []).append(a.get("content", ""))
        if tag == "link":
            if a.get("rel") == "canonical": self.canonical.append(a.get("href", ""))
            if a.get("rel") == "alternate" and a.get("hreflang"): self.alternates.append(a)
        if tag == "img": self.images.append(a)
        if tag in ("a","link","script","img","source"):
            u = a.get("href") or a.get("src")
            if u: self.links.append((tag, u, self.main, a))
    def handle_endtag(self, tag):
        if tag == "main": self.main = False
        if tag == "title": self.title_open = False
        if tag in ("script","style"): self.hidden = max(0,self.hidden-1)
    def handle_data(self, data):
        if self.title_open: self.title += data
        if self.main and not self.hidden: self.main_text.append(data)

def main():
    paths = sorted(EN.rglob("*.html"))
    docs = {}
    issues, notes = [], []
    titles, descriptions = {}, {}
    checked_links = 0
    def report(out, page, message):
        out.append({"page":str(page.relative_to(ROOT)), "message":message})
    def getdoc(p):
        if p not in docs: docs[p] = Document(p.read_text(encoding="utf-8"))
        return docs[p]
    for p in paths:
        raw = p.read_text(encoding="utf-8")
        d = getdoc(p)
        if re.search(r'<meta[^>]+http-equiv=["\']refresh', raw, re.I):
            report(notes,p,"Redirect alias; not counted as a substantive page")
            continue
        if d.lang != "en": report(issues,p,"Incorrect HTML language")
        if d.main_count != 1 or d.h1 != 1: report(issues,p,f"Main/H1 count: {d.main_count}/{d.h1}")
        if not d.title.strip(): report(issues,p,"Missing title")
        desc = d.meta.get("description",[])
        if len(desc)!=1 or not desc[0].strip(): report(issues,p,"Missing or duplicate description")
        if d.title in titles: report(issues,p,"Duplicate title: "+str(titles[d.title].relative_to(ROOT)))
        titles[d.title] = p
        if desc:
            if desc[0] in descriptions: report(issues,p,"Duplicate description: "+str(descriptions[desc[0]].relative_to(ROOT)))
            descriptions[desc[0]] = p
        prose = " ".join(d.main_text).replace(COMPANY,"")
        if CYR.search(prose): report(issues,p,"Unexpected Cyrillic in main text")
        if OLD_ABBR.search(prose): report(issues,p,"Deprecated residence abbreviation")
        for k,v in Counter(d.ids).items():
            if v>1: report(issues,p,"Duplicate ID: "+k)
        if not d.canonical: report(notes,p,"Canonical not yet set (preview)")
        if not d.alternates: report(notes,p,"No head link rel=alternate hreflang (preview)")
        if not any("noindex" in x for x in d.meta.get("robots",[])): report(notes,p,"Check preview indexing policy")
        for img in d.images:
            if "alt" not in img: report(issues,p,"Image without alt attribute: "+img.get("src",""))
        if "/knowledge/articles/" in p.as_posix():
            schemas = re.findall(r'<script type="application/ld\+json">([\s\S]*?)</script>',raw)
            try:
                articles = [json.loads(x) for x in schemas]
                if not any(x.get("@type")=="Article" and x.get("inLanguage")=="en" and isinstance(x.get("author"),dict) and x["author"].get("name")=="Lev Vtiurin" for x in articles):
                    report(issues,p,"Missing expected English Article schema")
            except Exception as e: report(issues,p,"Invalid JSON-LD: "+str(e))
        for tag,url,in_main,a in d.links:
            u = urlsplit(url)
            if u.scheme or u.netloc:
                if tag=="a" and (u.scheme=="mailto" or u.netloc in ("t.me","wa.me")):
                    q=parse_qs(u.query)
                    expected={"t.me":"lev_vt","wa.me":"79685341915"}.get(u.netloc)
                    if expected and u.path.strip("/")!=expected: report(issues,p,"Unexpected messaging recipient: "+url)
                    if u.scheme=="mailto" and u.path!="salutrussie@salutrussie.ru": report(issues,p,"Unexpected email recipient: "+u.path)
                    if any(CYR.search(x) for values in q.values() for x in values): report(issues,p,"Non-English contact prefill")
                continue
            checked_links+=1
            path=unquote(u.path)
            if path.startswith("/salutrussie/"): target=ROOT/path.removeprefix("/salutrussie/")
            elif path.startswith("/"): target=ROOT/path.lstrip("/")
            elif path: target=(p.parent/path).resolve()
            else: target=p
            if target.is_dir(): target=target/"index.html"
            if not target.is_file():
                report(issues,p,"Missing local target: "+url)
                continue
            if in_main and tag=="a" and target.is_relative_to(ROOT/"v3"/"ru"):
                report(issues,p,"Russian destination in English main: "+url)
            if u.fragment and target.suffix==".html" and unquote(u.fragment) not in getdoc(target).ids:
                report(issues,p,"Missing anchor: "+url)
    result={"html_files":len(paths),"substantive_pages":len(titles),"local_links_checked":checked_links,"issues":issues,"launch_notes":notes}
    Path("english-audit.json").write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
    print(f"{len(paths)} HTML files; {len(titles)} substantive pages; {checked_links} local references; {len(issues)} findings; {len(notes)} launch notes")
    for item in issues: print(item["page"]+": "+item["message"])
    # Findings are reported for human review; do not block responsive tests.
if __name__=="__main__": main()
