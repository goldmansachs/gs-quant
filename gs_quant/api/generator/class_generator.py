"""
Copyright 2019 Goldman Sachs.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
"""

from collections import namedtuple
import inflection
import itertools
import keyword
import re
import sys


def format_docstring(doc, indent=1, trailing_newline=True):
    if not doc:
        return ''
    else:
        suffix = '\n' if trailing_newline else ''
        prefix = '    ' * indent
        return '\n{}"""{}"""'.format(prefix, doc.replace('"', "'")) + suffix


def format_default(default):
    return "'{}'".format(default) if isinstance(default, str) else default


class EnumInfo(namedtuple('EnumInfo', ('name', 'values', 'doc'))):

    def code(self):
        names = ['_' + v if keyword.iskeyword(v) or (not v) or (v[0] != '_' and not v[0].isalpha()) else v for v in self.values]
        values = ["{} = '{}'".format(inflection.transliterate(re.sub('[-. ]', '_', n)).replace('/', '_OVER_'), v).replace('(', '').replace(')', '') for n, v in zip(names, self.values)]

        code = '''class {}(EnumBase, Enum):    
    {}
    {}
    
    def __repr__(self):
        return self.value
'''.format(self.name, format_docstring(self.doc), '\n    '.join(values))

        return code


class ClassInfo(namedtuple('ClassInfo', ('name', 'property_infos', 'doc', 'required', 'bases'))):

    def code(self):
        args = [None] * len(self.required)
        kwargs = []
        init = []

        # Prior to Python 3.7 there was a maximum of 255 arguments
        add_args = sys.hexversion >= 50790640 or len(self.property_infos) <= 255

        for prop in self.property_infos:
            if prop.has_setter:
                value = prop.name if add_args else "kwargs.get('{}')".format(prop.name)
                init.append('self.__{} = {}'.format(prop.name[:-1] if prop.name.endswith('_') else prop.name, value))

            default = format_default(prop.default)

            try:
                idx = self.required.index(prop.name)
                args[idx] = '{}: {}'.format(prop.name, prop.type) if prop.type else prop.name
            except ValueError:
                if prop.has_setter:
                    kwargs.append('{}: {} = {}'.format(prop.name, prop.type, default) if prop.type else '{}={}'.format(prop.name, default))

        code = '''class {}{}:
        {}       
    def __init__(self, {}):
        super().__init__()
        {}
'''.format(self.name, '({})'.format(', '.join(self.bases)) if self.bases else '',
           format_docstring(self.doc),
           ', '.join(itertools.chain(filter(None, args), kwargs)) if add_args else '**kwargs',
           '\n        '.join(init))

        for prop in self.property_infos:
            code += '''{}        
'''.format(prop.code())

        return code


class PropertyInfo(namedtuple("PropertyInfo", ('name', 'has_setter', 'type', 'default', 'doc'))):

    def code(self):
        raw_name = self.name[:-1] if self.name.endswith('_') else self.name
        ret = 'self.__{}'.format(raw_name) if self.has_setter else format_default(self.default)

        code = '''    @property
    def {}(self){}:{}
        return {}
'''.format(self.name, ' -> {}'.format(self.type) if self.type else '', format_docstring(self.doc, 2, False), ret)

        if self.has_setter:
            code += '''
    @{}.setter
    def {}(self, value{}):
        self.__{} = value
        self._property_changed('{}')
'''.format(self.name, self.name, ': {}'.format(self.type) if self.type else '', raw_name, raw_name, raw_name)

        code = '\n    ' + code.strip()
        return code
