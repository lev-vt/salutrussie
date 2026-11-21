"""Small HTML tree for the site's build and tests, using only the standard library.

This deliberately supports the selectors used by this repository, not general CSS.
"""
from html import escape
from html.parser import HTMLParser
import re

VOID = set('area base br col embed hr img input link meta param source track wbr'.split())


class Node:
    def __init__(self, name=None, attrs=(), parent=None, data=''):
        self.name, self.attrs, self.parent, self.data = name, dict(attrs), parent, data
        self.contents = []

    def __getitem__(self, key):
        return self.attrs[key]

    def __setitem__(self, key, value):
        self.attrs[key] = value

    def get(self, key, default=None):
        return self.attrs.get(key, default)

    def get_text(self, separator='', strip=False):
        if self.name is None:
            return self.data.strip() if strip else self.data
        parts = [x.get_text(separator, strip) for x in self.contents]
        if strip:
            parts = [x for x in parts if x]
        return separator.join(parts)

    @property
    def text(self):
        return self.get_text()

    def decompose(self):
        if self.parent:
            self.parent.contents.remove(self)
            self.parent = None

    def _descendants(self):
        for child in self.contents:
            if child.name:
                yield child
                yield from child._descendants()

    def find(self, name, **attrs):
        return next((n for n in self._descendants() if n.name == name and all(
            (key in n.attrs if value is True else n.get(key) == value)
            for key, value in attrs.items())), None)

    def find_all(self, name, **attrs):
        return [n for n in self._descendants() if n.name == name and all(
            (key in n.attrs if value is True else n.get(key) == value)
            for key, value in attrs.items())]

    def select(self, query):
        groups = [part.strip().split() for part in query.split(',')]
        result = []
        for node in self._descendants():
            if any(_selector_chain(node, group) for group in groups):
                result.append(node)
        return result

    def select_one(self, query):
        return next(iter(self.select(query)), None)

    def __getattr__(self, key):
        if key.startswith('_'):
            raise AttributeError(key)
        return self.find(key)

    def __str__(self):
        if self.name is None:
            return self.data
        if self.name == '[document]':
            return ''.join(map(str, self.contents))
        attrs = ''.join(f' {key}="{escape(str(value), quote=True)}"' if value is not None else f' {key}'
                        for key, value in self.attrs.items())
        opening = f'<{self.name}{attrs}>'
        return opening if self.name in VOID else opening + ''.join(map(str, self.contents)) + f'</{self.name}>'


def _simple_selector(node, selector):
    match = re.fullmatch(r'([\w-]+)?(?:\.([\w-]+))?(?:\[([\w-]+)(\^=|=)?(?:["\']?([^\]"\']+)["\']?)?\])?', selector)
    if not match:
        raise ValueError(f'Unsupported selector: {selector}')
    tag, cls, attr, op, value = match.groups()
    if tag and node.name != tag:
        return False
    if cls and cls not in node.get('class', '').split():
        return False
    if attr:
        actual = node.get(attr)
        if actual is None or (op == '=' and actual != value) or (op == '^=' and not actual.startswith(value)):
            return False
    return True


def _selector_chain(node, parts):
    if not parts or not _simple_selector(node, parts[-1]):
        return False
    current = node.parent
    for part in reversed(parts[:-1]):
        while current and not _simple_selector(current, part):
            current = current.parent
        if not current:
            return False
        current = current.parent
    return True


class _Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.root = Node('[document]')
        self.current = self.root

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs, self.current)
        self.current.contents.append(node)
        if tag not in VOID:
            self.current = node

    def handle_startendtag(self, tag, attrs):
        self.current.contents.append(Node(tag, attrs, self.current))

    def handle_endtag(self, tag):
        current = self.current
        while current.parent and current.name != tag:
            current = current.parent
        if current.parent and current.name == tag:
            self.current = current.parent

    def handle_data(self, data):
        self.current.contents.append(Node(parent=self.current, data=data))

    def handle_entityref(self, name):
        self.handle_data(f'&{name};')

    def handle_charref(self, name):
        self.handle_data(f'&#{name};')

    def handle_comment(self, data):
        self.handle_data(f'<!--{data}-->')


def BeautifulSoup(source, parser='html.parser'):
    if parser != 'html.parser':
        raise ValueError(parser)
    parsed = _Parser()
    parsed.feed(source)
    parsed.close()
    return parsed.root
