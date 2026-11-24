#!/usr/bin/env python3
"""Prepare a separate release copy with canonical URLs, reciprocal hreflang and sitemap.
Does not deploy or modify the source. Indexing is disabled unless explicitly requested."""
import argparse, html, json, re, shutil
from pathlib import Path
from urllib.parse import urlsplit, urljoin
from xml.etree.ElementTree import Element, SubElement, ElementTree


def direct_contact_links(doc, route):
    """Give commercial CTAs a real contact-page fallback, even without JS."""
    def rewrite(match):
        tag = match.group(0)
        attrs = {key.lower(): value for key, _, value in re.findall(r'([\w:-]+)\s*=\s*(["\x27])(.*?)\2', tag, flags=re.S)}
        classes = set(attrs.get("class", "").split())
        if "hreflang" in attrs or "btn-ghost" in classes or "sr-contact-choice" in classes:
            return tag
        if not (classes & {"nav-cta", "btn", "expert-cta", "sr-quick-consult"} or attrs.get("data-analytics-event") == "consultation_click"):
            return tag
        href = html.unescape(attrs.get("href", ""))
        parsed = urlsplit(href)
        is_contact = not parsed.netloc and not parsed.scheme and re.search(r'/(?:consultations|contacts)/?
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True, help="Path to the V3 preview folder")
    parser.add_argument("--output", type=Path, required=True, help="New, nonexistent destination directory")
    parser.add_argument("--site-url", required=True, help="Confirmed production base URL, including any path prefix")
    parser.add_argument("--enable-indexing", action="store_true", help="Only after legal, technical and publication approval")
    args = parser.parse_args()
    base = args.site_url.rstrip("/") + "/"
    parsed = urlsplit(base)
    if parsed.scheme != "https" or not parsed.hostname or parsed.query or parsed.fragment or parsed.username:
        parser.error("Use a confirmed, absolute HTTPS production base URL without query, fragment or credentials.")
    if args.output.exists():
        parser.error("Output already exists; refusing to overwrite.")
    if args.source.resolve() in args.output.resolve().parents:
        parser.error("Output must be outside the source directory.")
    manifest_path = Path(__file__).with_name("v3-seo-manifest.json")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    routes = set(manifest["routes"])
    for route in routes:
        if not (args.source / route / "index.html").is_file():
            parser.error(f"Missing required route: {route}")
    actual_routes = {
        path.parent.relative_to(args.source).as_posix() + "/"
        for lang in ("ru", "en", "fr")
        for path in (args.source / lang).rglob("index.html")
        if path.parent.relative_to(args.source).as_posix() != "ru/migration/decree-702-design"
    }
    if actual_routes != routes:
        parser.error(f"Route manifest mismatch; missing: {sorted(routes - actual_routes)}; unlisted: {sorted(actual_routes - routes)}")
    shutil.copytree(args.source, args.output)
    exclusion = set(manifest["excludedFromSitemap"])
    sitemap_urls = []
    def escaped(v):
        return html.escape(v, quote=True)
    def put_tags(doc, tags):
        return re.sub(r"</head>", lambda m: tags + m.group(0), doc, count=1, flags=re.I)
    for route in sorted(routes):
        lang, suffix = route.split("/", 1)
        path = args.output / route / "index.html"
        doc = path.read_text(encoding="utf-8")
        doc = direct_contact_links(doc, route)
        canonical = base + route
        indexable = args.enable_indexing and suffix not in exclusion
        doc = re.sub(r'<meta\s+name="robots"[^>]*>', '', doc, flags=re.I)
        doc = re.sub(r'<link\s+rel="canonical"[^>]*>', '', doc, flags=re.I)
        doc = re.sub(r'<link\s+rel="alternate"\s+hreflang="[^"]+"[^>]*>', '', doc, flags=re.I)
        doc = re.sub(r'<meta\s+property="og:url"[^>]*>', '', doc, flags=re.I)
        tags = '<meta name="robots" content="' + ('index,follow' if indexable else 'noindex,follow' if args.enable_indexing else 'noindex,nofollow') + '">'
        tags += '<link rel="canonical" href="' + escaped(canonical) + '">'
        tags += '<meta property="og:url" content="' + escaped(canonical) + '">'
        if suffix not in exclusion:
            for other in ("ru", "en", "fr"):
                target = other + "/" + suffix
                if target in routes:
                    tags += '<link rel="alternate" hreflang="' + other + '" href="' + escaped(base + target) + '">'
            if not suffix:
                tags += '<link rel="alternate" hreflang="x-default" href="' + escaped(base) + '">'
        def update_schema(match):
            data = json.loads(match.group(1))
            def normalize(node):
                if isinstance(node, list):
                    return [normalize(value) for value in node]
                if not isinstance(node, dict):
                    return node
                result = {}
                for key, value in node.items():
                    if key in ("@id", "url", "image", "item") and isinstance(value, str):
                        result[key] = urljoin(canonical, value)
                    else:
                        result[key] = normalize(value)
                return result
            data = normalize(data)
            if isinstance(data, dict) and data.get("@type") == "Article":
                data["url"] = canonical
                data["mainEntityOfPage"] = {"@type": "WebPage", "@id": canonical}
                for role in ("author", "publisher"):
                    entity = data.get(role)
                    if isinstance(entity, dict):
                        if entity.get("@type") == "Organization":
                            entity["url"] = base + lang + "/"
                        elif entity.get("@type") == "Person":
                            entity["url"] = base + lang + "/about/"
            return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False).replace("<", "\\u003c") + '</script>'
        doc = re.sub(r'<script type="application/ld\+json">([\s\S]*?)</script>', update_schema, doc)
        doc = put_tags(doc, tags)
        path.write_text(doc, encoding="utf-8")
        if indexable:
            sitemap_urls.append(canonical)
    # Keep the old-design redirect out of the sitemap and index.
    root = args.output / "index.html"
    if root.is_file():
        doc = root.read_text(encoding="utf-8")
        doc = re.sub(r'<meta\s+name="robots"[^>]*>', '', doc, flags=re.I)
        tags = '<meta name="robots" content="' + ('index,follow' if args.enable_indexing else 'noindex,nofollow') + '">'
        tags += '<link rel="canonical" href="' + escaped(base) + '">'
        for lang in ("ru", "en", "fr"):
            tags += '<link rel="alternate" hreflang="' + lang + '" href="' + escaped(base + lang + "/") + '">'
        tags += '<link rel="alternate" hreflang="x-default" href="' + escaped(base) + '">'
        doc = put_tags(doc, tags)
        root.write_text(doc, encoding="utf-8")
        if args.enable_indexing:
            sitemap_urls.append(base)
    if args.enable_indexing:
        urlset = Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
        for loc in sitemap_urls:
            SubElement(SubElement(urlset, "url"), "loc").text = loc
        ElementTree(urlset).write(args.output / "sitemap.xml", encoding="utf-8", xml_declaration=True)
        (args.output / "robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: " + base + "sitemap.xml\n", encoding="utf-8")
    else:
        (args.output / "robots.txt").write_text("User-agent: *\nAllow: /\n# Non-indexable review copy; use access control for private staging.\n", encoding="utf-8")
    print(f"Prepared {len(routes)} language pages; indexable sitemap entries: {len(sitemap_urls)}. Nothing deployed.")

if __name__ == "__main__":
    main()
, parsed.path)
        is_channel = re.match(r'^(?:mailto:salutrussie@salutrussie\.ru(?:\?|$)|https://(?:wa\.me/79685341915|t\.me/lev_vt)(?:[/?#]|$))', href, flags=re.I)
        if not (is_contact or is_channel):
            return tag
        dest = "../" * len(route.strip("/").split("/")) + route.split("/")[0] + "/contacts/"
        tag = re.sub(r'(\bhref\s*=\s*)(["\x27])(.*?)\2', lambda m: m[1] + m[2] + dest + m[2], tag, count=1, flags=re.I|re.S)
        return tag[:-1] + ' data-sr-direct-contact="">'
    return re.sub(r'<a\b[^>]*>', rewrite, doc, flags=re.I)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True, help="Path to the V3 preview folder")
    parser.add_argument("--output", type=Path, required=True, help="New, nonexistent destination directory")
    parser.add_argument("--site-url", required=True, help="Confirmed production base URL, including any path prefix")
    parser.add_argument("--enable-indexing", action="store_true", help="Only after legal, technical and publication approval")
    args = parser.parse_args()
    base = args.site_url.rstrip("/") + "/"
    parsed = urlsplit(base)
    if parsed.scheme != "https" or not parsed.hostname or parsed.query or parsed.fragment or parsed.username:
        parser.error("Use a confirmed, absolute HTTPS production base URL without query, fragment or credentials.")
    if args.output.exists():
        parser.error("Output already exists; refusing to overwrite.")
    if args.source.resolve() in args.output.resolve().parents:
        parser.error("Output must be outside the source directory.")
    manifest_path = Path(__file__).with_name("v3-seo-manifest.json")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    routes = set(manifest["routes"])
    for route in routes:
        if not (args.source / route / "index.html").is_file():
            parser.error(f"Missing required route: {route}")
    actual_routes = {
        path.parent.relative_to(args.source).as_posix() + "/"
        for lang in ("ru", "en", "fr")
        for path in (args.source / lang).rglob("index.html")
        if path.parent.relative_to(args.source).as_posix() != "ru/migration/decree-702-design"
    }
    if actual_routes != routes:
        parser.error(f"Route manifest mismatch; missing: {sorted(routes - actual_routes)}; unlisted: {sorted(actual_routes - routes)}")
    shutil.copytree(args.source, args.output)
    exclusion = set(manifest["excludedFromSitemap"])
    sitemap_urls = []
    def escaped(v):
        return html.escape(v, quote=True)
    def put_tags(doc, tags):
        return re.sub(r"</head>", lambda m: tags + m.group(0), doc, count=1, flags=re.I)
    for route in sorted(routes):
        lang, suffix = route.split("/", 1)
        path = args.output / route / "index.html"
        doc = path.read_text(encoding="utf-8")
        canonical = base + route
        indexable = args.enable_indexing and suffix not in exclusion
        doc = re.sub(r'<meta\s+name="robots"[^>]*>', '', doc, flags=re.I)
        doc = re.sub(r'<link\s+rel="canonical"[^>]*>', '', doc, flags=re.I)
        doc = re.sub(r'<link\s+rel="alternate"\s+hreflang="[^"]+"[^>]*>', '', doc, flags=re.I)
        doc = re.sub(r'<meta\s+property="og:url"[^>]*>', '', doc, flags=re.I)
        tags = '<meta name="robots" content="' + ('index,follow' if indexable else 'noindex,follow' if args.enable_indexing else 'noindex,nofollow') + '">'
        tags += '<link rel="canonical" href="' + escaped(canonical) + '">'
        tags += '<meta property="og:url" content="' + escaped(canonical) + '">'
        if suffix not in exclusion:
            for other in ("ru", "en", "fr"):
                target = other + "/" + suffix
                if target in routes:
                    tags += '<link rel="alternate" hreflang="' + other + '" href="' + escaped(base + target) + '">'
            if not suffix:
                tags += '<link rel="alternate" hreflang="x-default" href="' + escaped(base) + '">'
        def update_schema(match):
            data = json.loads(match.group(1))
            def normalize(node):
                if isinstance(node, list):
                    return [normalize(value) for value in node]
                if not isinstance(node, dict):
                    return node
                result = {}
                for key, value in node.items():
                    if key in ("@id", "url", "image", "item") and isinstance(value, str):
                        result[key] = urljoin(canonical, value)
                    else:
                        result[key] = normalize(value)
                return result
            data = normalize(data)
            if isinstance(data, dict) and data.get("@type") == "Article":
                data["url"] = canonical
                data["mainEntityOfPage"] = {"@type": "WebPage", "@id": canonical}
                for role in ("author", "publisher"):
                    entity = data.get(role)
                    if isinstance(entity, dict):
                        if entity.get("@type") == "Organization":
                            entity["url"] = base + lang + "/"
                        elif entity.get("@type") == "Person":
                            entity["url"] = base + lang + "/about/"
            return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False).replace("<", "\\u003c") + '</script>'
        doc = re.sub(r'<script type="application/ld\+json">([\s\S]*?)</script>', update_schema, doc)
        doc = put_tags(doc, tags)
        path.write_text(doc, encoding="utf-8")
        if indexable:
            sitemap_urls.append(canonical)
    # Keep the old-design redirect out of the sitemap and index.
    root = args.output / "index.html"
    if root.is_file():
        doc = root.read_text(encoding="utf-8")
        doc = re.sub(r'<meta\s+name="robots"[^>]*>', '', doc, flags=re.I)
        tags = '<meta name="robots" content="' + ('index,follow' if args.enable_indexing else 'noindex,nofollow') + '">'
        tags += '<link rel="canonical" href="' + escaped(base) + '">'
        for lang in ("ru", "en", "fr"):
            tags += '<link rel="alternate" hreflang="' + lang + '" href="' + escaped(base + lang + "/") + '">'
        tags += '<link rel="alternate" hreflang="x-default" href="' + escaped(base) + '">'
        doc = put_tags(doc, tags)
        root.write_text(doc, encoding="utf-8")
        if args.enable_indexing:
            sitemap_urls.append(base)
    if args.enable_indexing:
        urlset = Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
        for loc in sitemap_urls:
            SubElement(SubElement(urlset, "url"), "loc").text = loc
        ElementTree(urlset).write(args.output / "sitemap.xml", encoding="utf-8", xml_declaration=True)
        (args.output / "robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: " + base + "sitemap.xml\n", encoding="utf-8")
    else:
        (args.output / "robots.txt").write_text("User-agent: *\nAllow: /\n# Non-indexable review copy; use access control for private staging.\n", encoding="utf-8")
    print(f"Prepared {len(routes)} language pages; indexable sitemap entries: {len(sitemap_urls)}. Nothing deployed.")

if __name__ == "__main__":
    main()
