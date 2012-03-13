import re
from types import ClassType

def construct_all_list(namespace, cls):
    all = []
    for name, value in namespace.items():
        if isinstance(value, (ClassType, type)) and issubclass(value, cls):
            all.append(name)
    return all

def minimize_string(value):
    return re.sub(r'\s+', ' ', value).strip(' ')

PLURALIZATION_RULES = (
    (re.compile(r'ife$'), re.compile(r'ife$'), 'ives'),
    (re.compile(r'eau$'), re.compile(r'eau$'), 'eaux'),
    (re.compile(r'lf$'), re.compile(r'lf$'), 'lves'),
    (re.compile(r'[sxz]$'), re.compile(r'$'), 'es'),
    (re.compile(r'[^aeioudgkprt]h$'), re.compile(r'$'), 'es'),
    (re.compile(r'(qu|[^aeiou])y$'), re.compile(r'y$'), 'ies'),
)

def pluralize(word, quantity=None, rules=PLURALIZATION_RULES):
    if quantity == 1: 
        return word

    for pattern, target, replacement in rules:
        if pattern.search(word):
            return target.sub(replacement, word)
    else:
        return word + 's'

class StructureFormatter(object):
    def __init__(self, indent=4):
        self.indent = ' ' * indent
        self.indent_count = indent

    def format(self, structure, level=0):
        description = self._format_value(structure, level)
        if isinstance(description, list):
            description = '\n'.join(description)
        return description

    def _format_dict(self, value, level):
        inner_indent = self.indent * (level + 1)
        singles, multiples = [], []

        for k, v in sorted(value.iteritems()):
            description = self._format_value(v, level + 1)
            if isinstance(description, list):
                multiples.append('%s%r: %s' % (inner_indent, k, description[0]))
                multiples.extend(description[1:-1])
                multiples.append('%s%s,' % (inner_indent, description[-1]))
            else:
                singles.append('%s%r: %s,' % (inner_indent, k, description))

        return ['{'] + singles + multiples + ['}']

    def _format_list(self, value, level, tokens='[]'):
        inner_indent = self.indent * (level + 1)
        single_line = True

        lines = []
        for v in value:
            description = self._format_value(v, level + 1)
            if isinstance(description, list):
                single_line = False
                lines.append('%s%s' % (inner_indent, description[0]))
                lines.extend(description[1:-1])
                lines.append('%s%s,' % (inner_indent, description[-1]))
            else:
                lines.append('%s%s,' % (inner_indent, description))

        if single_line:
            single_line = tokens[0] + ', '.join(l.strip().rstrip(',') for l in lines) + tokens[1]
            if len(single_line) <= 60:
                return single_line

        return [tokens[0]] + lines + [tokens[1]]

    def _format_long_string(self, value, level):
        return repr(value)

    def _format_value(self, value, level):
        if isinstance(value, dict):
            return self._format_dict(value, level)
        elif isinstance(value, list):
            return self._format_list(value, level)
        elif isinstance(value, tuple):
            return self._format_list(value, level, '()')
        elif isinstance(value, basestring) and len(value) + (self.indent_count * level) > 70:
            return self._format_long_string(value, level)
        else:
            return repr(value)
