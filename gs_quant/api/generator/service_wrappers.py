"""
Copyright 2018 Goldman Sachs.
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

from gs_quant.errors import *
from gs_quant.api.generator.class_generator import ClassInfo, EnumInfo, PropertyInfo
from gs_quant.errors import MqError
import builtins
import inflection
import keyword
import re

__endpoints = {
    'risk': ('/calculate', '/coordinates'),
    'data': '*',
    'assets': '*'
}
__base_classes_by_parent = {
    'Instruments': 'Instrument'
}


class __Graph:

    class Node:

        def __init__(self, name):
            self.name = name
            self.inputs = set()
            self.outputs = set()

        def __repr__(self):
            return self.name

    def __init__(self):
        self.nodes = {}
        self.alias_types = {}

    def add_edge(self, from_name, to_name):
        from_node = self.nodes.setdefault(from_name, self.Node(from_name))
        from_node.outputs.add(to_name)

        to_node = self.nodes.setdefault(to_name, self.Node(to_name))
        to_node.inputs.add(from_name)

    def terminal_nodes(self):
        return [n for n in self.nodes.values() if not n.inputs]

    def find_all_inputs(self, names):
        ret = set()
        stack = list(names)

        while stack:
            name = stack.pop()
            ret.add(name)

            node = self.nodes[name]
            stack.extend(n for n in node.inputs if n not in ret)

        return ret


def _normalise_name(s):
    s = s.replace('#/properties/', '_')
    matcher = re.search('definition:/(\w+)$', s)
    if matcher:
        s = matcher.group(1)
    else:
        matcher = re.search('#/definitions/(\w+)$', s)
        if matcher:
            s = matcher.group(1)

    s = inflection.transliterate(re.sub('[-\. ]', '_', s))
    if not re.match(r'[a-z_]\w*$', s, re.I) and not keyword.iskeyword(s) and s not in dir(builtins):
        raise MqError(s + ' is not a valid Python identifier')

    return inflection.camelize(s)


def python_type_from_value(value, graph=None):
    typ = None
    json_type = value.get('type')

    try:
        ref = _normalise_name(value['$ref']) if '$ref' in value else None
    except MqError:
        return None

    if ref:
        if not graph:
            return "'{}'".format(ref)
        else:
            if ref in graph.nodes:
                return "'{}'".format(ref)
            elif ref in graph.alias_types:
                return "{}".format(graph.alias_types[ref])

    if json_type == 'string':
        fmt = value.get('format')
        if fmt == 'date':
            typ = 'datetime.date'
        elif fmt == 'date-time':
            typ = 'datetime.datetime'
        else:
            typ = 'str'
    elif json_type == 'number':
        typ = 'float'
    elif json_type == 'integer':
        typ = 'int'
    elif json_type == 'boolean':
        typ = 'bool'

    return typ


def find_refs(class_name, definitions):
    refs = {}
    union_refs = set()
    type_spec = definitions.get(class_name)

    if not type_spec:
        return refs

    graph = __Graph()
    stack = [(class_name, type_spec)]

    while stack:
        parent_name, spec = stack.pop()

        if '$ref' in spec:
            try:
                ref_name = _normalise_name(spec['$ref'])
                ref_spec = definitions.get(ref_name)

                if ref_spec:
                    ref_type = ref_spec.get('type')
                    is_enum = ref_type == 'string' and 'enum' in ref_spec
                    if ref_type in ('object', 'ref') or is_enum:
                        refs[ref_name] = is_enum
                        graph.add_edge(ref_name, parent_name)
                        if not is_enum:
                            stack.append((ref_name, ref_spec))
                    elif 'anyOf' in ref_spec or 'oneOf' in ref_spec:
                        if ref_name not in union_refs:
                            graph.add_edge(ref_name, parent_name)
                            stack.append((ref_name, ref_spec))
                    else:
                        ref_type = python_type_from_value(ref_spec)
                        if ref_type:
                            graph.alias_types[ref_name] = ref_type
            except MqError:
                pass
        elif 'type' in spec:
            typ = spec['type']
            if typ == 'array' and 'items' in spec:
                stack.append((parent_name, spec['items']))
            elif typ == 'object' and 'properties' in spec:
                for prop in spec['properties'].values():
                    stack.append((parent_name, prop))
        elif 'anyOf' in spec:
            union_refs.add(parent_name)
            stack.extend((parent_name, x) for x in spec['anyOf'])
        elif 'oneOf' in spec:
            union_refs.add(parent_name)
            stack.extend((parent_name, x) for x in spec['oneOf'])

    return graph


def generate_class_info(name, definitions, graph):
    definition = definitions[name]
    class_type = definition.get('type')
    class_doc = definition.get('description', '')

    if class_type == 'string' and 'enum' in definition:
        return EnumInfo(name, definition['enum'], class_doc)
    elif class_type == 'object':
        class_attributes = {}
        property_infos = []
        required = definition.get('required', ())

        for key, value in definition.get('properties', ()).items():
            has_setter = True

            key = inflection.transliterate(re.sub('[-\. ]', '_', key))
            if keyword.iskeyword(key):
                key += '_'

            default = value.get('default')
            if default is not None:
                if default == 'true':
                    default = True
                elif default == 'false':
                    default = False
                elif isinstance(default, str):
                    default = '''{}'''.format(default)

            ref = _normalise_name(value['$ref']) if '$ref' in value else None
            doc = value.get('description', '')
            if not doc and ref and ref in definitions:
                doc = definitions[ref].get('description', '')

            enums = value.get('enum')
            if enums and len(enums) == 1:
                # Handle cases such as type and assetClass on instruments
                default = enums[0]
                class_attributes[key] = default

                if not doc:
                    doc = default

                has_setter = False
                if key in required:
                    required.remove(key)

            if value.get('type') == 'array':
                items = value.get('items')
                if items:
                    if isinstance(items, dict) == 1:
                        param_type = python_type_from_value(items, graph)
                        if not param_type:
                            param_type ='Any'
                    elif isinstance(items, (tuple, list)):
                        param_types = [python_type_from_value(i, graph) for i in items]
                        if all(param_types):
                            param_type = 'Union[{}]'.format(', '.join(param_types))
                        else:
                            param_type = 'Any'
                    else:
                        param_type = 'Any'
                else:
                    param_type = 'Any'

                typ = "Iterable[{}]".format(param_type)
            else:
                typ = python_type_from_value(value, graph)

                if ref and not typ:
                    typ = graph.alias_types.get(ref)

                if ref and typ:
                    typ = "Union[{}, str]".format(typ)

            property_infos.append(PropertyInfo(key, has_setter, typ, default, doc))

        node = graph.nodes.get(name)
        bases = tuple(filter(None, (__base_classes_by_parent.get(i) for i in node.outputs))) or ('Base',) if node else ('Base',)
        class_info = ClassInfo(name, property_infos, class_doc, required, bases)

        return class_info


def is_instrument(class_info):
    return 'Instrument' in getattr(class_info, 'bases', ())


def generate_service_classes(session, service, all_classes, classes_by_module):
    endpoint_config = __endpoints.get(service)
    if not endpoint_config:
        raise MqError('Unsupported service ' + service)

    endpoints, definitions = session.endpoints_and_definitions(service)

    for endpoint in (e for e in endpoints if e.get('method', 'GET') in ('POST', 'PUT') and endpoint_config == '*' or e['path'] in endpoint_config):
        class_names = set()

        for class_spec in session.request_response_gen(endpoint):
            stack = [class_spec]

            while stack:
                spec = stack.pop()

                if '$ref' in spec:
                    class_name = _normalise_name(spec['$ref'])
                    if class_name not in class_names:
                        class_names.add(class_name)
                if 'type' in spec:
                    typ = spec['type']
                    if typ == 'array' and 'items' in spec:
                        stack.append(spec['items'])
                    elif typ == 'object' and 'properties' in spec:
                        for prop in spec['properties'].values():
                            stack.append(prop)
                elif 'anyOf' in spec:
                    stack.extend(x for x in spec['anyOf'])
                elif 'oneOf' in spec:
                    stack.extend(x for x in spec['oneOf'])

        for class_name in class_names:
            if class_name not in all_classes:
                instrument_class_names = set()
                graph = find_refs(class_name, definitions)
                class_names = (class_name,) + tuple(graph.nodes.keys())

                for name in class_names:
                    existing_class_info = all_classes.get(name)
                    if existing_class_info:
                        if classes_by_module[name] != service and not is_instrument(existing_class_info):
                            classes_by_module[name] = 'common'
                    else:
                        class_info = generate_class_info(name, definitions, graph)
                        if class_info is not None:
                            all_classes[name] = class_info
                            if is_instrument(class_info):
                                classes_by_module[name] = 'instrument'
                                instrument_class_names.add(name)
                            else:
                                classes_by_module[name] = service

                all_instrument_inputs = graph.find_all_inputs(instrument_class_names)
                for name in all_instrument_inputs:
                    if name in all_classes and not is_instrument(all_classes[name]):
                            classes_by_module[name] = 'common'


def all_service_classes_by_module(session):
    classes_by_module = {}
    all_classes = {}
    ret = {}

    for service in __endpoints.keys():
        generate_service_classes(session, service, all_classes, classes_by_module)

    for class_name, module in classes_by_module.items():
        ret.setdefault(module, []).append(all_classes[class_name])

    return ret
