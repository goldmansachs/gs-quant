"""
Copyright 2024 Goldman Sachs.
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
import pytest

FAILED_TESTS = []
RUN_TESTS = []
LOGGED_EVENTS = []


def did_anything_fail():
    return len(FAILED_TESTS) > 0


def did_anything_run():
    return len(RUN_TESTS) > 0


def log_mock_data_event(event: str):
    LOGGED_EVENTS.append(event)


def pytest_addoption(parser):
    parser.addoption(
        '--fixmockdata', action='store_true'
    )


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "fixmockdata: marker to update mock file data"
    )


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_makereport(item, call) -> None:
    """Called to make report for the test for test item (the call phase).

    :param item:
        The item.
    """
    if call.when == 'call':
        RUN_TESTS.append(item.nodeid)
        if call.excinfo:
            FAILED_TESTS.append((item.nodeid, item))


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    terminalreporter.ensure_newline()
    terminalreporter.section("Mock File Summary")
    if not len(LOGGED_EVENTS):
        terminalreporter.write_line("Nothing Changed")
    for event in LOGGED_EVENTS:
        terminalreporter.write_line(event)


def pytest_collection_modifyitems(items):
    LOGGED_EVENTS.clear()
    FAILED_TESTS.clear()
    for item in items:
        # Skip the integration tests unless explicitly asked for
        run_fix_mock_data = item.config.getoption("fixmockdata")  # run with pytest . --fixmockdata
        if any(marker.name == 'fixmockdata' for marker in item.own_markers) and not run_fix_mock_data:
            item.add_marker(pytest.mark.skip(reason='Skipping Mock Data updating'))
