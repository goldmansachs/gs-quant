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
import hashlib
import json
import logging
import os
from abc import abstractmethod
from os.path import exists
from pathlib import Path
from typing import List, Dict, Tuple, Set, Any
from unittest import mock

from gs_quant.errors import MqUninitialisedError
from gs_quant.session import GsSession, Environment
from gs_quant.test.mock_data_test_utils import log_mock_data_event

logger = logging.getLogger("mock_request")


class MockRequest:
    __looked_at_files = {}
    __cached_test_data = {}
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
            try:
                _ = GsSession.current
            except MqUninitialisedError:
                from gs_quant.session import OAuth2Session
                OAuth2Session._authenticate = mock.MagicMock(return_value=None)
                GsSession.use(Environment.PROD, 'fake_client_id', 'fake_secret', application=self.application)
            self.mocker.patch.object(self.api, self.method, side_effect=self.mock_calc)

    def mock_calc(self, *args, **kwargs):
        request_id = self.get_request_id(args, kwargs)
        request_hash = self.get_request_hash(request_id)
        file_name = f'request{request_hash}.json'
        file_path = self.paths / f'calc_cache/{file_name}'
        if not exists(file_path):
            logger.error(f'Unable to find mock test date for {self.__class__.__name__}:\n'
                         f'File {file_path} not found. Key: {request_id}')
            raise FileNotFoundError(f'File {file_name} not found in {self.paths / "calc_cache"}')
        existing_meta, mock_data = self._load_mock_data_from_file(file_path)
        test_name = self._get_current_test_name()
        file_key = (file_name, request_id, request_hash)
        used_in_test = tuple(existing_meta.get("tests", []))
        file_deets = MockRequest.__looked_at_files.setdefault(self.paths, dict())
        file_deets.setdefault(file_key, (self.__class__.__name__, used_in_test, set()))[2].add(test_name)
        return mock_data

    @staticmethod
    def _get_current_test_name():
        return os.environ.get('PYTEST_CURRENT_TEST').split(':')[-1].split(' ')[0]

    @classmethod
    def _load_mock_data_from_file(cls, file_path):
        meta = {}
        data = cls.__cached_test_data.get(file_path)
        if data is None:
            with open(file_path) as json_data:
                data = json.load(json_data)
                cls.__cached_test_data[file_path] = data
        if isinstance(data, dict) and 'mocked_data' in data:
            meta = data
            data = json.loads(data['mocked_data'])
        return meta, data

    @classmethod
    def _make_mock_file_data(cls, request_id, request_hash, cls_name, mock_data_str, used_in_tests):
        return {
            'request_id': request_id,
            'request_hash': request_hash,
            'type': cls_name,
            'tests': used_in_tests,
            'mocked_data': mock_data_str,
        }

    def create_files(self, request_id, result_json):
        request_hash = self.get_request_hash(request_id)
        cls_name = self.__class__.__name__
        ct = self._get_current_test_name()
        mock_data = self._make_mock_file_data(request_id, request_hash, cls_name, result_json.decode('utf-8'), [ct])
        with open(self.paths / f'calc_cache/request{request_hash}.json', 'w') as json_data:
            MockRequest.__saved_files.add(request_id)
            json_data.write(json.dumps(mock_data))

    @abstractmethod
    def mock_calc_create_files(self, *args, **kwargs):
        ...

    def mock_calc_create_new_files(self, *args, **kwargs):
        request_id = self.get_request_id(args, kwargs)
        request_hash = self.get_request_hash(request_id)
        file_exists = exists(self.paths / f'calc_cache/request{request_hash}.json')
        if file_exists:
            return self.mock_calc(*args, *kwargs)
        else:
            return self.mock_calc_create_files(*args, *kwargs)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @staticmethod
    def get_file_summary() -> Dict[Path, Dict[str, Set[Tuple[List[str], Tuple[str, str, str]]]]]:
        return MockRequest.__looked_at_files

    @classmethod
    def get_unused_files(cls) -> Tuple[Dict[str, Any], ...]:
        file_summary = cls.get_file_summary()
        unused_files = []
        for path, files_used in file_summary.items():
            files_names_used = set(file_name for (file_name, _, _) in files_used.keys())
            for test_file in os.listdir(path / 'calc_cache'):
                if test_file.endswith('.json') and test_file not in files_names_used:
                    full_path = path / 'calc_cache' / test_file
                    try:
                        unused_meta, _ = cls._load_mock_data_from_file(full_path)
                    except Exception:
                        unused_meta = {'tests': ['UNKNOWN']}
                    unused_details = {'file': test_file, 'full_path': full_path,
                                      'tests': tuple(unused_meta.get('tests', []))}
                    unused_files.append(unused_details)
        return tuple(unused_files)

    @classmethod
    def remove_unused_files(cls):
        unused_files = cls.get_unused_files()
        for file in unused_files:
            try:
                log_mock_data_event(f'Removing {file["file"]}. As not used.')
                os.remove(file['full_path'])
            except Exception:
                continue

    @classmethod
    def reindex_test_files(cls, report_only=False) -> Tuple[str, ...]:
        reindex_files = []
        file_summary = cls.get_file_summary()
        for path, files_used in file_summary.items():
            for file_key, (cls_name, existing_used, now_used) in files_used.items():
                file_name, request_id, request_hash = file_key
                file_path = path / 'calc_cache' / file_name
                sorted_tests = tuple(sorted(now_used))
                if existing_used == sorted_tests:
                    continue
                reindex_files.append(file_name)
                if report_only:
                    continue
                existing_meta, data = cls._load_mock_data_from_file(file_path)
                new_data = cls._make_mock_file_data(request_id, request_hash, cls_name, json.dumps(data), sorted_tests)
                cls.__cached_test_data[file_path] = new_data
                file_deets = MockRequest.__looked_at_files.get(path, dict())
                existing_looked_at = file_deets.get(file_key)
                file_deets[file_key] = (existing_looked_at[0], sorted_tests, existing_looked_at[2])
                with open(file_path, 'w') as out_file:
                    out_file.write(json.dumps(new_data, indent=4))
                log_mock_data_event(f'Updated {file_name}. As {existing_used} != {sorted_tests}')
        return tuple(reindex_files)

    @staticmethod
    def get_saved_files() -> List[str]:
        return list(MockRequest.__saved_files)

    @abstractmethod
    def get_request_id(self, args, kwargs):
        ...

    @staticmethod
    def get_request_hash(request_id: str):
        id_bytes = request_id.encode('utf-8') if isinstance(request_id, str) else request_id
        return hashlib.md5(id_bytes).hexdigest()
