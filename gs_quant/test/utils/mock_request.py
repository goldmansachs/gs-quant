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
from typing import List, Dict, Tuple, Any, NamedTuple
from unittest import mock

from gs_quant.errors import MqUninitialisedError
from gs_quant.session import GsSession, Environment
from gs_quant.test.mock_data_test_utils import log_mock_data_event

logger = logging.getLogger("mock_request")


class MockFileKey:

    def __init__(self, request_id):
        self.request_id = request_id.decode('utf-8') if isinstance(request_id, bytes) else request_id
        self.request_hash = self.get_hash(self.request_id)
        self.file_name = f'request{self.request_hash}.json'

    @staticmethod
    def get_hash(request_id: str):
        id_bytes = request_id.encode('utf-8')
        return hashlib.md5(id_bytes).hexdigest()

    def __eq__(self, other):
        return self.file_name == other.file_name and self.request_id == other.request_id and \
            self.request_hash == other.request_hash

    def __hash__(self):
        return hash((self.file_name, self.request_id, self.request_hash))

    def __repr__(self):
        return f"MockFileKey({self.request_hash})"


class MockFileRecord(NamedTuple):
    """a docstring"""
    foo: int
    bar: str
    used_in_tests: set


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
                self.save_files).casefold() == 'new' else self.mock_calc_check_and_create_files)
        else:
            try:
                _ = GsSession.current
            except MqUninitialisedError:
                from gs_quant.session import OAuth2Session
                OAuth2Session._authenticate = mock.MagicMock(return_value=None)
                GsSession.use(Environment.PROD, 'fake_client_id', 'fake_secret', application=self.application)
            self.mocker.patch.object(self.api, self.method, side_effect=self.mock_calc)

    def full_file_path(self, mock_file_key: MockFileKey):
        return self.build_file_path(self.paths, mock_file_key)

    @staticmethod
    def build_file_path(base_path, mock_file_key: MockFileKey):
        return base_path / 'calc_cache' / mock_file_key.file_name

    def mock_calc(self, *args, **kwargs):
        request_id = self.get_request_id(args, kwargs)
        mfk = MockFileKey(request_id)
        file_path = self.full_file_path(mfk)
        if not exists(file_path):
            logger.error(f'Unable to find mock test date for {self.__class__.__name__}:\n'
                         f'File {file_path} not found. Key: {request_id}')
            raise FileNotFoundError(f'File {mfk.file_name} not found in {self.paths / "calc_cache"}')
        existing_meta, mock_data = self._load_mock_data_from_file(file_path)
        self._record_file_used_in_test(mfk)
        return mock_data

    def _record_file_used_in_test(self, mfk: MockFileKey):
        test_name = self._get_current_test_name()
        file_deets = MockRequest.__looked_at_files.setdefault(self.paths, dict())
        file_deets.setdefault(mfk, (self.__class__.__name__, set()))[1].add(test_name)

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
    def _make_mock_file_data(cls, mfk: MockFileKey, cls_name, mock_data_str, used_in_tests):
        return {
            'request_id': mfk.request_id,
            'request_hash': mfk.request_hash,
            'type': cls_name,
            'tests': used_in_tests,
            'mocked_data': mock_data_str,
        }

    def create_files(self, request_id, result_json):
        cls_name = self.__class__.__name__
        ct = self._get_current_test_name()
        mfk = MockFileKey(request_id)
        file_path = self.full_file_path(mfk)
        mock_data = self._make_mock_file_data(mfk, cls_name, result_json.decode('utf-8'), [ct])
        with open(file_path, 'w') as file_data:
            MockRequest.__saved_files.add(request_id)
            file_data.write(json.dumps(mock_data, indent=4))
        log_mock_data_event(f'Created {mfk.file_name}.')
        self._record_file_used_in_test(mfk)

    @abstractmethod
    def mock_calc_create_files(self, *args, **kwargs):
        ...

    def mock_calc_check_and_create_files(self, *args, **kwargs):
        # Check if we have already saved this file in this test run, in which case skip re-saving it
        request_id = self.get_request_id(args, kwargs)
        if request_id in MockRequest.__saved_files:
            res = self.mock_calc(*args, **kwargs)
            # This file was remade this session so we need to reindex it here
            self._reindex_single_file(MockFileKey(request_id))
            return res
        return self.mock_calc_create_files(*args, **kwargs)

    def mock_calc_create_new_files(self, *args, **kwargs):
        request_id = self.get_request_id(args, kwargs)
        full_file_path = self.full_file_path(MockFileKey(request_id))
        file_exists = exists(full_file_path)
        if file_exists:
            return self.mock_calc(*args, **kwargs)
        else:
            return self.mock_calc_create_files(*args, **kwargs)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @staticmethod
    def get_file_summary() -> Dict[Path, Dict[MockFileKey, Tuple[List[str], Tuple[str, str, str]]]]:
        return MockRequest.__looked_at_files

    @classmethod
    def get_unused_files(cls, log=False) -> Tuple[Dict[str, Any], ...]:
        file_summary = cls.get_file_summary()
        unused_files = []
        for path, files_used in file_summary.items():
            files_names_used = set(m.file_name for m in files_used.keys())
            for test_file in os.listdir(path / 'calc_cache'):
                if test_file.endswith('.json') and test_file not in files_names_used:
                    full_path = path / 'calc_cache' / test_file
                    try:
                        unused_meta, _ = cls._load_mock_data_from_file(full_path)
                    except Exception:
                        unused_meta = {'tests': ['UNKNOWN']}
                    if log:
                        log_mock_data_event(f'Noticed UNUSED {test_file}.')
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
    def reindex_test_files(cls, report_only=False, log=False) -> Tuple[str, ...]:
        reindex_files = []
        file_summary = cls.get_file_summary()
        for path, files_used in file_summary.items():
            for mock_file_key, (cls_name, now_used) in files_used.items():
                updated = cls._update_single_file_with_new_tests(path, mock_file_key, now_used, report_only, log)
                if updated:
                    reindex_files.append(mock_file_key.file_name)
        return tuple(reindex_files)

    @classmethod
    def _update_single_file_with_new_tests(cls, base_path, mock_file_key, new_tests, report_only, log):
        full_file_path = cls.build_file_path(base_path, mock_file_key)
        existing_meta, data = cls._load_mock_data_from_file(full_file_path)
        existing_used = tuple(existing_meta.get('tests', []))
        sorted_tests = tuple(sorted(new_tests))
        if existing_used == sorted_tests:
            return False
        if report_only:
            if log:
                missing = set(existing_used) - set(sorted_tests)
                extra = set(sorted_tests) - set(existing_used)
                missing_txt = f" {len(missing)} test(s) are listed in the file but weren't used: {missing}." \
                    if len(missing) else ""
                extra_txt = f" {len(extra)} test(s) that accessed this file were NOT listed in the file : {extra}." \
                    if len(extra) else ""
                log_mock_data_event(f'Noticed BAD INDEX {mock_file_key.file_name}. {missing_txt}{extra_txt}')
            return True

        new_data = cls._make_mock_file_data(mock_file_key, existing_meta['type'], json.dumps(data), sorted_tests)
        # update the cached in memory test data with new contents
        cls.__cached_test_data[full_file_path] = new_data
        # Write the updated mock file
        with open(full_file_path, 'w') as out_file:
            out_file.write(json.dumps(new_data, indent=4))
        log_mock_data_event(f'Updated {mock_file_key.file_name}. As {existing_used} != {sorted_tests}')
        return True

    def _reindex_single_file(self, mock_file_key: MockFileKey):
        file_summary = self.get_file_summary()
        by_path = file_summary.get(self.paths, dict())
        mock_file_usage = by_path.get(mock_file_key)
        if mock_file_usage is None:
            return
        test_used = mock_file_usage[1]
        self._update_single_file_with_new_tests(self.paths, mock_file_key, test_used, report_only=False, log=True)

    @staticmethod
    def get_saved_files() -> List[str]:
        return list(MockRequest.__saved_files)

    @abstractmethod
    def get_request_id(self, args, kwargs):
        ...
