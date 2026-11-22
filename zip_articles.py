"""Russian expert articles supplied by the site owner, rendered with the standard library.

Only public article Markdown is stored in content/articles_ru. Editorial notes and
the source archive's private context are deliberately excluded from the project.
"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path
from urllib.parse import urlparse

ARTICLE_DIR = Path(__file__).resolve().parent / 'content' / 'articles_ru'
UPDATED = '2026-11-21'

TOPICS = {
    'rvp-shared-values-702': 'migration',
    'vnzh-red-diploma': 'migration',
    'registration-foreigner-landlord': 'migration',
    'vnzh-annual-notification-2027': 'migration',
    'visa-expires-after-rvp-vnzh-filing': 'migration',
    'hqs-dismissal-visa': 'migration',
    'foreign-citizen-register-ip': 'business',
    'ip-tax-regime-ausn-usn': 'business',
    'foreign-income-accounts-russia': 'business',
    'online-kkt-ip-foreigners': 'business',
}

FLOWS = {
    'rvp-shared-values-702': ('Проверить основание', 'Подготовить въезд', 'Собрать документы', 'Подать на РВП', 'Проверить решение'),
    'vnzh-red-diploma': ('Проверить диплом', 'Сверить сроки пребывания', 'Собрать пакет', 'Подать заявление', 'Получить решение'),
    'registration-foreigner-landlord': ('Подтвердить адрес', 'Определить заявителя', 'Собрать документы', 'Подать уведомление', 'Сохранить подтверждение'),
    'vnzh-annual-notification-2027': ('Найти дату выдачи', 'Рассчитать год', 'Проверить доход', 'Подать уведомление', 'Сохранить подтверждение'),
    'visa-expires-after-rvp-vnzh-filing': ('Проверить статус подачи', 'Сверить дату визы', 'Подтвердить право пребывания', 'Решить вопрос учёта', 'Планировать поездки'),
    'hqs-dismissal-visa': ('Зафиксировать дату', 'Проверить разрешение', 'Найти работодателя', 'Подать ходатайство', 'Решить статус семьи'),
    'foreign-citizen-register-ip': ('Проверить РВП или ВНЖ', 'Подтвердить адрес', 'Подготовить Р21001', 'Подать в ФНС', 'Выбрать налоговый режим'),
    'ip-tax-regime-ausn-usn': ('Описать модель дохода', 'Проверить ограничения', 'Сравнить налоговую нагрузку', 'Уведомить ФНС', 'Контролировать условия'),
    'foreign-income-accounts-russia': ('Определить резидентство', 'Классифицировать доход', 'Проверить счёт', 'Рассчитать налог', 'Подать отчётность'),
    'online-kkt-ip-foreigners': ('Определить расчёт', 'Проверить исключения', 'Выбрать ККТ', 'Зарегистрировать кассу', 'Выдавать чеки'),
}


def _parse_file(path: Path):
    raw = path.read_text(encoding='utf-8')
    if not raw.startswith('---\n'):
        raise ValueError(f'Missing article metadata: {path}')
    front, body = raw[4:].split('\n---\n', 1)
    data = {}
    for line in front.splitlines():
        key, _, value = line.partition(':')
        if not _ or not key:
            continue
        value = value.strip()
        if value.startswith('['):
            data[key] = json.loads(value)
        elif value.startswith('"'):
            data[key] = json.loads(value)
        else:
            data[key] = value
    return data, body.strip()


EXPERT_ARTICLES = []
_BODIES = {}
for _file in sorted(ARTICLE_DIR.glob('[0-9][0-9]-*.md')):
    _meta, _body = _parse_file(_file)
    _slug = _meta['slug']
    if _slug not in TOPICS or _slug in _BODIES:
        raise ValueError(f'Unexpected or repeated article slug: {_slug}')
    _BODIES[_slug] = _body
    EXPERT_ARTICLES.append({
        'slug': _slug,
        'title': _meta['title'],
        'seo_title': _meta['seo_title'],
        'summary': _meta['meta_description'],
        'meta_description': _meta['meta_description'],
        'topic': TOPICS[_slug],
        'kind': 'article',
        'primary_query': _meta['primary_query'],
        'related_queries': _meta['secondary_queries'],
        'date_modified': UPDATED,
        'source_status': 'Owner-supplied draft; official primary sources checked selectively; individual legal advice requires case review',
        'url': f'/ru/knowledge/articles/{_slug}/',
    })
if len(EXPERT_ARTICLES) != 10:
    raise ValueError(f'Expected 10 articles, got {len(EXPERT_ARTICLES)}')
_META = {a['slug']: a for a in EXPERT_ARTICLES}


def _inline(value: str) -> str:
    """Escape text first; permit only a narrow, safe subset of Markdown."""
    tokens = []

    def reserve(match):
        label, url = match.group(1), match.group(2)
        parsed = urlparse(url)
        if parsed.scheme not in ('https', 'http') and not url.startswith('/'):
            return html.escape(match.group(0))
        href = html.escape(url, quote=True)
        target = ' target="_blank" rel="noopener noreferrer"' if parsed.scheme else ''
        tokens.append(f'<a href="{href}"{target}>{html.escape(label)}</a>')
        return f'\uFFF0{len(tokens)-1}\uFFF1'

    value = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', reserve, value)
    value = html.escape(value, quote=False)
    value = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', value)
    value = re.sub(r'`([^`]+)`', r'<code>\1</code>', value)
    for index, token in enumerate(tokens):
        value = value.replace(f'\uFFF0{index}\uFFF1', token)
    return value


def _heading_id(text: str, index: int) -> str:
    return f'section-{index}'


def _split_table(line):
    return [cell.strip() for cell in line.strip().strip('|').split('|')]


def _render_markdown(body: str):
    lines = body.splitlines()
    parts = []
    headings = []
    i = 0
    h2_index = 0
    first_para = True
    while i < len(lines):
        line = lines[i].strip()
        if not line or line == '---':
            i += 1
            continue
        h = re.match(r'^(#{1,3})\s+(.+)$', line)
        if h:
            level, label = len(h.group(1)), h.group(2)
            if level == 1:
                # The page hero supplies the only H1.
                i += 1
                continue
            if level == 2:
                h2_index += 1
                anchor = _heading_id(label, h2_index)
                headings.append((anchor, label))
            else:
                anchor = f'{_heading_id(label, h2_index)}-{len(parts)}'
            parts.append(f'<h{level} id="{anchor}">{_inline(label)}</h{level}>')
            i += 1
            continue
        if line.startswith('|') and i+1 < len(lines) and re.match(r'^\|?\s*:?-{2,}', lines[i+1].strip()):
            header = _split_table(line)
            i += 2
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                cells = _split_table(lines[i])
                if len(cells) != len(header):
                    raise ValueError(f'Invalid table row: {lines[i]}')
                rows.append(cells)
                i += 1
            table = '<div class="expert-table-wrap" role="region" tabindex="0" aria-label="Таблица: прокрутите по горизонтали"><table><thead><tr>'
            table += ''.join(f'<th scope="col">{_inline(cell)}</th>' for cell in header)
            table += '</tr></thead><tbody>'
            table += ''.join('<tr>'+''.join(f'<td>{_inline(cell)}</td>' for cell in row)+'</tr>' for row in rows)
            table += '</tbody></table></div>'
            parts.append(table)
            continue
        list_type = 'ul' if re.match(r'^[-*]\s+', line) else 'ol' if re.match(r'^\d+\.\s+', line) else None
        if list_type:
            items = []
            pattern = r'^[-*]\s+(.+)$' if list_type == 'ul' else r'^\d+\.\s+(.+)$'
            while i < len(lines) and (m := re.match(pattern, lines[i].strip())):
                items.append(f'<li>{_inline(m.group(1))}</li>')
                i += 1
            parts.append(f'<{list_type}>' + ''.join(items) + f'</{list_type}>')
            continue
        paragraph = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r'^(#{1,3})\s+|^[-*]\s+|^\d+\.\s+|^\||^---$', lines[i].strip()):
            paragraph.append(lines[i].strip())
            i += 1
        joined = ' '.join(paragraph)
        cls = ' class="expert-lead"' if first_para else ' class="expert-note"' if joined.startswith(('**Важно', '**Обратите внимание')) else ''
        parts.append(f'<p{cls}>{_inline(joined)}</p>')
        first_para = False
    return parts, headings


def render_expert_article(slug: str) -> str:
    """Return complete, accessible article body (page heading and JSON-LD supplied by build.py)."""
    if slug not in _BODIES:
        raise KeyError(slug)
    parts, headings = _render_markdown(_BODIES[slug])
    flow = FLOWS[slug]
    flow_html = '<section class="expert-process" aria-label="Карта действий"><h2>Карта действий</h2><ol>'
    flow_html += ''.join(f'<li><span>{index:02d}</span><strong>{html.escape(item)}</strong></li>' for index, item in enumerate(flow, 1))
    flow_html += '</ol></section>'
    toc = '<nav class="expert-toc" aria-label="Содержание статьи"><strong>В этой статье</strong><ol>'
    toc += ''.join(f'<li><a href="#{anchor}">{_inline(label)}</a></li>' for anchor, label in headings)
    toc += '</ol></nav>'
    # Keep the direct answer visible before the contents and process graphic.
    insert_at = 1 if parts else 0
    parts[insert_at:insert_at] = [flow_html, toc]
    related = _related(slug)
    return '<div class="expert-article">' + ''.join(parts) + related + '</div>'


def _related(slug):
    a = _META[slug]
    others = [x for x in EXPERT_ARTICLES if x['topic'] == a['topic'] and x['slug'] != slug][:3]
    links = ''.join(f'<li><a href="{x["url"]}">{html.escape(x["title"])}</a></li>' for x in others)
    service = '/ru/migration/' if a['topic'] == 'migration' else '/ru/business/'
    label = 'миграционные услуги' if a['topic'] == 'migration' else 'юридическое сопровождение бизнеса'
    return f'<aside class="expert-related"><h2>Следующие шаги</h2><p>Ознакомьтесь с материалами по смежным вопросам или изучите <a href="{service}">{label}</a>.</p><ul>{links}</ul><p><a class="expert-cta" href="/ru/consultations/">Обсудить свою ситуацию →</a></p></aside>'


def expert_article_schema(slug: str, absolute_url: str) -> dict:
    a = _META[slug]
    return {
        '@context': 'https://schema.org',
        '@type': 'Article',
        'headline': a['title'],
        'description': a['meta_description'],
        'inLanguage': 'ru-RU',
        'dateModified': UPDATED,
        'mainEntityOfPage': absolute_url,
        'url': absolute_url,
    }
