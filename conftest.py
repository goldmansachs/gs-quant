# This import is needed to register the magic pylint hooks to make it skip the integration tests
# flake8: noqa
# pylint: disable=wildcard-import, unused-wildcard-import
from gs_quant.test.mock_data_test_utils import *

import os

LOG_DIR = "test_logs"
os.makedirs(LOG_DIR, exist_ok=True)

PASSED = []
SKIPPED = []
FAILED = []
ERRORS = []
WARNINGS = []

def pytest_runtest_logreport(report):
    # passed：只有 call 阶段真正执行后才算通过
    if report.when == "call" and report.passed:
        PASSED.append(report)

    # skipped 可以发生在 setup 或 call 阶段
    if report.skipped:
        SKIPPED.append(report)

    # failed 可能是测试失败（call）或 fixture/setup 错误
    if report.failed:
        if report.when == "call":
            FAILED.append(report)
        else:
            ERRORS.append(report)


def pytest_warning_recorded(warning_message, when, nodeid, location):
    WARNINGS.append(f"{nodeid} - {warning_message.message}")

def pytest_sessionfinish(session, exitstatus):
    duration = session.config._session_duration if hasattr(session.config, "_session_duration") else None

    # 计算时长，fallback
    if duration is None:
        import time
        duration = time.time() - session.config.starttime if hasattr(session.config, "starttime") else 0

    def write_md(filename, title, count, reports, is_report=True):
        with open(os.path.join(LOG_DIR, filename), "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\n")
            f.write(f"共计 {count} 条\n\n")
            f.write("---\n\n")
            if is_report:
                for rep in reports:
                    f.write(f"- {rep.nodeid}\n")
            else:
                for line in reports:
                    f.write(f"- {line}\n")

    write_md("passed.md", "通过测试 (Passed)", len(PASSED), PASSED)
    write_md("skipped.md", "跳过测试 (Skipped)", len(SKIPPED), SKIPPED)
    write_md("warnings.md", "警告 (Warnings)", len(WARNINGS), WARNINGS, is_report=False)
    write_md("errors.md", "错误 (Errors)", len(ERRORS), ERRORS)
    write_md("failures.md", "失败 (Failures)", len(FAILED), FAILED)

    # 额外写一个 summary.md，类似 499 passed, 3 skipped, 479 warnings, 331 errors in 12.02s
    total_passed = len(PASSED)
    total_skipped = len(SKIPPED)
    total_warnings = len(WARNINGS)
    total_errors = len(ERRORS) + len(FAILED)  # 错误 + 失败 一起算 errors
    total_time = f"{duration:.2f}" if isinstance(duration, float) else "N/A"

    with open(os.path.join(LOG_DIR, "summary.md"), "w", encoding="utf-8") as f:
        f.write(f"# 测试总结\n\n")
        f.write(f"{total_passed} passed, {total_skipped} skipped, {total_warnings} warnings, {total_errors} errors in {total_time}s\n")
