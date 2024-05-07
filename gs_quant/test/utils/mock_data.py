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
import inspect
from pathlib import Path

from gs_quant.api.gs.data import GsDataApi
from gs_quant.test.utils.mock_request import MockRequest


class MockData(MockRequest):
    api = GsDataApi
    method = 'query_data'
    api_method = GsDataApi.query_data

    def __init__(self, mocker, save_files=False, paths=None, application='gs-quant'):
        super().__init__(mocker, save_files, paths, application)
        self.paths = paths if paths else \
            Path(next(filter(lambda x: x.code_context and self.__class__.__name__ in x.code_context[0],
                             inspect.stack())).filename).parents[1]

    def mock_calc_create_files(self, *args, **kwargs):
        import orjson

        def get_json(*i_args, **i_kwargs):
            this_json = self.api_method(*i_args, **i_kwargs)

            return this_json
        result = get_json(*args, **kwargs)
        result_json = orjson.dumps(result,
                                   option=orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_NON_STR_KEYS | orjson.OPT_SORT_KEYS)
        request_id = self.get_request_id(args, kwargs)
        self.create_files(request_id, result_json)

        return result

    def get_request_id(self, args, kwargs):
        query = args[0].as_dict()
        parts = []
        relevant_data_query_params = [k for k in
                                      ["start_date", "start_time", "end_date", "end_time", "as_of_time", "since",
                                       "dates", "where"] if k in query.keys()]

        def stringify_values(v):
            return ','.join(v) if isinstance(v, list) else str(v)

        for k in sorted(relevant_data_query_params):
            v = query[k]
            if k != 'where':
                v_str = stringify_values(v)
            else:
                v_str = '_'.join([f'{where_k}:{stringify_values(where_v)}' for where_k, where_v in v.items()])
            parts.append(f'{k}:{v_str}')
        query_str = '_'.join(parts)
        return f'{args[1]}_{query_str}'
