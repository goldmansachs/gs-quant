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

from gs_quant.api.generator.class_generator import ClassInfo, EnumInfo
from gs_quant.api.generator.service_wrappers import all_service_classes_by_module
from gs_quant.session import GsSession, Environment
from importlib.abc import PathEntryFinder, SourceLoader
from importlib.machinery import ModuleSpec
import itertools
import os


class GeneratedModuleFinder(PathEntryFinder):

    def find_spec(self, fullname, path=None, target=None):
        if 'gs_quant.target' in fullname:
            return ModuleSpec(fullname, GeneratedModuleLoader(fullname))


class GeneratedModuleLoader(SourceLoader):

    __all_modules = {}

    def __init__(self, fullname):
        self.fullname = fullname

    def get_filename(self, fullname):
        return fullname

    def get_data(self, filename):
        """exec_module is already defined for us, we just have to provide a way
        of getting the source code of the module"""

        if not type(self).__all_modules:
            if not GsSession.current:
                raise RuntimeError('Must use a GsSession to generate target modules')

            for name, class_infos in all_service_classes_by_module(GsSession.current).items():
                module = generate_module(class_infos)
                type(self).__all_modules[name] = module.encode(encoding='utf-8')

        return type(self).__all_modules[filename.split('.')[-1]]


def generate_module(class_infos):
    imports = ['datetime', ('typing', 'Any, Iterable, Union')]
    base_imports = set(itertools.chain.from_iterable(c.bases for c in class_infos if isinstance(c, ClassInfo)))
    if any(c for c in class_infos if isinstance(c, EnumInfo)):
        base_imports.add('EnumBase')
        imports.append(('enum', 'Enum'))

    imports.append(('gs_quant.api.base', ', '.join(base_imports)))

    code = ''
    for imp in imports:
        if isinstance(imp, tuple):
            code += '''from {} import {}
'''.format(imp[0], imp[1])
        else:
            code += '''import {}
'''.format(imp)

    for cls in (EnumInfo, ClassInfo):
        for info in (i for i in class_infos if isinstance(i, cls)):
            code += '''

'''
            code += info.code()

    return code


def generate_all_modules():
    from gs_quant.session import GsSession

    base_path = os.path.join(os.path.normpath(os.path.split(os.path.split(os.path.dirname(__file__))[0])[0]), 'target')
    classes_by_module = all_service_classes_by_module(GsSession.current)

    for name, class_infos in classes_by_module.items():
        module = generate_module(class_infos)

        if module:
            filename = os.path.join(base_path, name + '.py')
            with open(filename, 'w') as f:
                f.write('''"""
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
"""\n\n''')
                f.write(module)


if __name__ == "__main__":
    GsSession.use(Environment.QA)
    generate_all_modules()
