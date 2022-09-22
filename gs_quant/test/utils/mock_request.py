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
import json
import os
from abc import abstractmethod
from os.path import exists
from typing import List
from unittest import mock

from gs_quant.session import GsSession, Environment


class MockRequest:
    __looked_at_files = {}
    __saved_files = set()
    api = None
    method = None
    api_method = None

    def __init__(self, mocker, save_files=False, paths=None, application='gs-quant'):
        # do not save tests with save_files = True
        self.save_files = save_files
        self.mocker = mocker
        self.paths = paths
        self.application = application
        if any([attr is None for attr in [self.api, self.method, self.api_method]]):
            raise NotImplementedError('Mock Subclasses must implement api and method properties')

    def __enter__(self):
        if self.save_files:
            GsSession.use(Environment.PROD, None, None, application=self.application)
            self.mocker.patch.object(self.api, self.method, side_effect=self.mock_calc_create_new_files if str(
                self.save_files).casefold() == 'new' else self.mock_calc_create_files)
        else:
            from gs_quant.session import OAuth2Session
            OAuth2Session.init = mock.MagicMock(return_value=None)
            GsSession.use(Environment.PROD, 'fake_client_id', 'fake_secret', application=self.application)
            self.mocker.patch.object(self.api, self.method, side_effect=self.mock_calc)

    def mock_calc(self, *args, **kwargs):
        request_id = self.get_request_id(args, kwargs)
        file_name = f'request{request_id}.json'
        with open(self.paths / f'calc_cache/{file_name}') as json_data:
            MockRequest.__looked_at_files.setdefault(self.paths, set()).add(file_name)
            return json.load(json_data)

    def create_files(self, request_id, result_json):
        with open(self.paths / f'calc_cache/request{request_id}.json', 'w') as json_data:
            MockRequest.__saved_files.add(request_id)
            json_data.write(result_json.decode('utf-8'))

    @abstractmethod
    def mock_calc_create_files(self, *args, **kwargs):
        ...

    def mock_calc_create_new_files(self, *args, **kwargs):
        request_id = self.get_request_id(args, kwargs)
        file_exists = exists(self.paths / f'calc_cache/request{request_id}.json')
        if file_exists:
            return self.mock_calc(*args, *kwargs)
        else:
            return self.mock_calc_create_files(*args, *kwargs)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @staticmethod
    def get_unused_files() -> List[str]:
        unused_files = []
        for test_path, files_used in MockRequest.__looked_at_files.items():
            for test_file in os.listdir(test_path / 'calc_cache'):
                if test_file.endswith('.json') and test_file not in files_used:
                    unused_files.append(test_file)
        return unused_files

    @staticmethod
    def get_saved_files() -> List[str]:
        return list(MockRequest.__saved_files)

    @abstractmethod
    def get_request_id(self, args, kwargs):
        ...
