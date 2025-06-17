# This import is needed to register the magic pylint hooks to make it skip the integration tests
# flake8: noqa
# pylint: disable=wildcard-import, unused-wildcard-import
from gs_quant.test.mock_data_test_utils import *

import os
import time

LOG_DIR = "test_logs"
os.makedirs(LOG_DIR, exist_ok=True)

PASSED = []
SKIPPED = []
FAILED = []
ERRORS = []
WARNINGS = []


def pytest_sessionstart(session):
    """
    Called after the Session object has been created and before performing collection and entering the run test loop.
    Used here to record test session start time.
    """
    session.config.starttime = time.time()


def pytest_runtest_logreport(report):
    """
    Pytest hook to process individual test phase reports.

    Categorizes test results into passed, skipped, failed, and errors.
    """
    # Only 'call' phase indicates a passed test case
    if report.when == "call" and report.passed:
        PASSED.append(report)

    # Tests can be skipped in 'setup' or 'call' phases
    if report.skipped:
        SKIPPED.append(report)

    # Failures in 'call' phase; errors in other phases (e.g. setup)
    if report.failed:
        if report.when == "call":
            FAILED.append(report)
        else:
            ERRORS.append(report)


def pytest_warning_recorded(warning_message, when, nodeid, location):
    """
    Pytest hook to record warnings emitted during test runs.
    """
    WARNINGS.append(f"{nodeid} - {warning_message.message}")


def pytest_sessionfinish(session, exitstatus):
    """
    Called after whole test run finished, right before returning the exit status to the system.

    Writes categorized test results to markdown files in the test_logs directory.
    """
    duration = getattr(session.config, "starttime", None)
    if duration is not None:
        duration = time.time() - duration
    else:
        duration = 0

    def write_md(filename, title, count, reports, is_report=True):
        path = os.path.join(LOG_DIR, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\n")
            f.write(f"Total: {count}\n\n")
            f.write("---\n\n")
            if is_report:
                for rep in reports:
                    f.write(f"- {rep.nodeid}\n")
            else:
                for line in reports:
                    f.write(f"- {line}\n")

    write_md("passed.md", "Passed Tests", len(PASSED), PASSED)
    write_md("skipped.md", "Skipped Tests", len(SKIPPED), SKIPPED)
    write_md("warnings.md", "Warnings", len(WARNINGS), WARNINGS, is_report=False)
    write_md("errors.md", "Errors", len(ERRORS), ERRORS)
    write_md("failures.md", "Failures", len(FAILED), FAILED)

    total_passed = len(PASSED)
    total_skipped = len(SKIPPED)
    total_warnings = len(WARNINGS)
    total_errors = len(ERRORS) + len(FAILED)
    total_time = f"{duration:.2f}"

    summary_path = os.path.join(LOG_DIR, "summary.md")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("# Test Summary\n\n")
        f.write(f"{total_passed} passed, {total_skipped} skipped, {total_warnings} warnings, {total_errors} errors in {total_time}s\n")
