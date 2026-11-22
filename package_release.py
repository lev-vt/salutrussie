#!/usr/bin/env python3
"""Build, validate and package SalutRussie for static hosting.

Production: python3 -B package_release.py --origin https://your-domain.example
Preview:    python3 -B package_release.py --preview
"""

from __future__ import annotations

import argparse
import hashlib
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlparse
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


ROOT = Path(__file__).resolve().parent
PACKAGES = ROOT / "build" / "packages"
PUBLIC_FILES = {".html", ".css", ".js", ".xml", ".txt", ".svg", ".jpg", ".jpeg", ".png", ".webp", ".woff2", ".ico"}
REQUIRED = {"index.html", "robots.txt", "sitemap.xml", "404.html"}
KIT_PYTHON = {
    "build.py", "site_html.py", "articles_content.py", "article_addenda.py",
    "service_content.py", "subpage_content.py", "b2b_content.py",
    "legal_site_content.py", "zip_articles.py", "verify_release.py",
    "package_release.py", "make_offline_preview.py",
}


def checked_origin(value: str) -> str:
    origin = value.rstrip("/")
    parsed = urlparse(origin)
    host = (parsed.hostname or "").lower()
    if (
        parsed.scheme != "https"
        or not host
        or "." not in host
        or parsed.username
        or parsed.password
        or parsed.port
        or parsed.path
        or parsed.params
        or parsed.query
        or parsed.fragment
        or host.endswith((".invalid", ".example", ".test", ".localhost"))
        or host in {"example.com", "example.net", "example.org", "localhost"}
        or host.endswith((".example.com", ".example.net", ".example.org"))
    ):
        raise SystemExit("Use the confirmed public HTTPS origin, for example https://domain.tld (no path or trailing slash).")
    return origin


def run_build(origin: str) -> Path:
    env = dict(os.environ, BUILD_VARIANT="release-check", PUBLIC_RELEASE="1", SITE_ORIGIN=origin)
    subprocess.run([sys.executable, "-B", "build.py"], cwd=ROOT, env=env, check=True)
    site = ROOT / "build" / "release-check"
    subprocess.run([sys.executable, "-B", "verify_release.py", str(site)], cwd=ROOT, check=True)
    return site


def collect(site: Path, preview: bool) -> list[Path]:
    if not site.is_dir():
        raise SystemExit(f"Missing generated site: {site}")
    files = sorted(p for p in site.rglob("*") if p.is_file())
    names = {p.relative_to(site).as_posix() for p in files}
    required = REQUIRED - {"sitemap.xml"} if preview else REQUIRED
    missing = required - names
    if missing:
        raise SystemExit(f"Generated site is incomplete: {', '.join(sorted(missing))}")
    for path in files:
        relative = path.relative_to(site)
        if path.is_symlink() or any(part.startswith(".") for part in relative.parts):
            raise SystemExit(f"Refusing hidden or linked file: {relative}")
        if path.suffix.lower() not in PUBLIC_FILES:
            raise SystemExit(f"Refusing non-public file type: {relative}")
        if path.suffix == ".html":
            html = path.read_text(encoding="utf-8")
            if any(marker in html.lower() for marker in ("lorem ipsum", "<!-- todo", "<!-- fixme", "example.invalid")):
                raise SystemExit(f"Unfinished content in {relative}")
            if preview and 'content="noindex' not in html and "content='noindex" not in html:
                raise SystemExit(f"Preview page is indexable: {relative}")
    robots = (site / "robots.txt").read_text(encoding="utf-8")
    if preview and "Disallow: /" not in robots:
        raise SystemExit("Preview robots.txt must block indexing")
    if not preview and "Allow: /" not in robots:
        raise SystemExit("Production robots.txt must allow indexing")
    return files


def package(site: Path, files: list[Path], filename: str) -> Path:
    PACKAGES.mkdir(parents=True, exist_ok=True)
    destination = PACKAGES / filename
    temporary = destination.with_suffix(".zip.tmp")
    with ZipFile(temporary, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            name = path.relative_to(site).as_posix()
            entry = ZipInfo(name, date_time=(2026, 11, 22, 0, 0, 0))
            entry.compress_type = ZIP_DEFLATED
            entry.external_attr = 0o644 << 16
            archive.writestr(entry, path.read_bytes(), compress_type=ZIP_DEFLATED, compresslevel=9)
    with ZipFile(temporary) as archive:
        if archive.testzip() is not None or set(archive.namelist()) != {p.relative_to(site).as_posix() for p in files}:
            raise SystemExit("ZIP verification failed")
    temporary.replace(destination)
    digest = hashlib.sha256(destination.read_bytes()).hexdigest()
    destination.with_suffix(".sha256").write_text(f"{digest}  {destination.name}\n", encoding="ascii")
    print(f"ARCHIVE: {destination}")
    print(f"SHA256:  {digest}")
    print(f"FILES:   {len(files)}")
    return destination


def package_kit() -> Path:
    """Owner handoff with a preview and the minimal source needed for a domain-specific build."""
    missing = [name for name in KIT_PYTHON if not (ROOT / name).is_file()]
    if missing:
        raise SystemExit(f"Missing build inputs: {', '.join(sorted(missing))}")
    subprocess.run([sys.executable, "-B", "build.py"], cwd=ROOT, check=True,
                   env={key: value for key, value in os.environ.items()
                        if key not in {"SITE_ORIGIN", "PUBLIC_RELEASE", "BUILD_VARIANT"}})
    preview = ROOT / "dist"
    collect(preview, preview=True)
    paths = [ROOT / name for name in sorted(KIT_PYTHON)]
    paths += sorted((ROOT / "src" / "original").glob("*.html"))
    paths += sorted(p for p in (ROOT / "src" / "fonts").iterdir() if p.suffix in {".css", ".txt", ".woff2"})
    paths += sorted((ROOT / "content" / "articles_ru").glob("*.md"))
    paths += [ROOT / "assets" / "expert-articles.css"]
    paths += [ROOT / "src" / "НАЧНИТЕ_ЗДЕСЬ.txt", ROOT / "docs" / "PUBLISHING.md"]
    paths += sorted(p for p in preview.rglob("*") if p.is_file())
    paths += sorted((ROOT / "tests").glob("test_*.py"))
    article_count = sum("content/articles_ru" in p.as_posix() for p in paths)
    if article_count != 10:
        raise SystemExit(f"Expected ten edited article sources, found {article_count}")
    PACKAGES.mkdir(parents=True, exist_ok=True)
    destination = PACKAGES / "salutrussie-owner-build-kit-NOT-FOR-UPLOAD.zip"
    temporary = destination.with_suffix(".zip.tmp")
    with ZipFile(temporary, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for path in paths:
            if not path.is_file() or path.is_symlink():
                raise SystemExit(f"Unsafe build input: {path}")
            relative = path.relative_to(ROOT).as_posix()
            entry = ZipInfo(relative, date_time=(2026, 11, 22, 0, 0, 0))
            entry.compress_type = ZIP_DEFLATED
            entry.external_attr = 0o644 << 16
            archive.writestr(entry, path.read_bytes(), compress_type=ZIP_DEFLATED, compresslevel=9)
    with ZipFile(temporary) as archive:
        if archive.testzip() is not None:
            raise SystemExit("Owner kit ZIP verification failed")
        with tempfile.TemporaryDirectory(prefix="salutrussie-kit-check-") as temp:
            archive.extractall(temp)
            subprocess.run([sys.executable, "-B", "build.py"], cwd=temp, check=True,
                           env={key: value for key, value in os.environ.items()
                                if key not in {"SITE_ORIGIN", "PUBLIC_RELEASE", "BUILD_VARIANT"}},
                           stdout=subprocess.DEVNULL)
    temporary.replace(destination)
    digest = hashlib.sha256(destination.read_bytes()).hexdigest()
    destination.with_suffix(".sha256").write_text(f"{digest}  {destination.name}\n", encoding="ascii")
    print(f"OWNER KIT: {destination}\nSHA256:    {digest}\nFILES:     {len(paths)}")
    return destination


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--origin", help="Confirmed production origin, e.g. https://your-domain.tld")
    group.add_argument("--preview", action="store_true", help="Package the existing noindex dist/ build for review only")
    group.add_argument("--kit", action="store_true", help="Create a standalone owner build kit with source and noindex preview")
    args = parser.parse_args()
    if args.kit:
        package_kit()
        return
    if args.preview:
        site = ROOT / "dist"
        filename = "salutrussie-preview-NOT-FOR-PUBLICATION.zip"
    else:
        site = run_build(checked_origin(args.origin))
        filename = "salutrussie-publication.zip"
    package(site, collect(site, args.preview), filename)


if __name__ == "__main__":
    main()
