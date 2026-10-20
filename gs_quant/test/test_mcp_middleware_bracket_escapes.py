"""
Copyright 2026 Senanur Çetin.
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

import warnings
from io import StringIO
from pathlib import Path

import pytest

MIDDLEWARE_PATH = Path(__file__).resolve().parents[1] / "mcp" / "middleware.py"


def test_mcp_middleware_has_no_invalid_string_escapes():
    """MCP logging strings must not emit Python invalid-escape warnings."""
    source = MIDDLEWARE_PATH.read_text(encoding="utf-8")
    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        warnings.simplefilter("error", SyntaxWarning)
        compile(source, str(MIDDLEWARE_PATH), "exec")


@pytest.mark.parametrize(
    "marker",
    [
        r"\\[call_tool",
        r"\\[tools/list",
        r"\\[session]",
        r"\\[{session_id}]",
    ],
)
def test_mcp_middleware_escapes_rich_log_tags(marker):
    """Rich control brackets stay escaped in each logging call site."""
    source = MIDDLEWARE_PATH.read_text(encoding="utf-8")
    assert marker in source


def test_rich_print_shows_literal_brackets():
    """Rich escapes leave the bracketed log tag visible without markup."""
    rich_console = pytest.importorskip("rich.console")
    output = StringIO()
    console = rich_console.Console(
        file=output, force_terminal=False, color_system=None, width=120
    )
    console.print(r"\[call_tool :hammer_and_wrench:] using tool [green]quote[/]")
    rendered = output.getvalue()
    assert rendered.startswith("[call_tool ")
    assert "] using tool quote" in rendered
    assert chr(92) not in rendered
