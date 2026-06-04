"""
Copyright 2026 Goldman Sachs.
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

import os
import sys
from pathlib import Path

import pytest

from gs_quant.skills import __main__ as installer


@pytest.fixture
def isolated_home(tmp_path, monkeypatch):
    home = tmp_path / "home"
    project = tmp_path / "project"
    home.mkdir()
    project.mkdir()
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: home))
    monkeypatch.chdir(project)
    return home, project


def test_discover_skills_finds_overview():
    skills = installer._discover_skills()
    assert "gs-quant-overview" in skills
    assert (skills["gs-quant-overview"] / "SKILL.md").is_file()


@pytest.mark.skipif(os.name == "nt", reason="symlink path not used on Windows")
def test_install_global_symlink(isolated_home):
    home, _ = isolated_home
    rc = installer.main(["install", "--global", "gs-quant-overview"])
    assert rc == 0
    target = home / ".claude" / "skills" / "gs-quant-overview"
    assert target.is_symlink()
    assert (target / "SKILL.md").is_file()
    assert Path(os.readlink(target)) == installer._discover_skills()["gs-quant-overview"]


def test_install_project_copy_on_windows(isolated_home, monkeypatch):
    _, project = isolated_home
    monkeypatch.setattr(installer, "_use_symlinks", lambda: False)
    rc = installer.main(["install", "--project", "gs-quant-overview"])
    assert rc == 0
    target = project / ".claude" / "skills" / "gs-quant-overview"
    assert target.is_dir() and not target.is_symlink()
    src = installer._discover_skills()["gs-quant-overview"]
    assert (target / "SKILL.md").read_text() == (src / "SKILL.md").read_text()


def test_install_overwrites_existing(isolated_home):
    _, project = isolated_home
    target = project / ".claude" / "skills" / "gs-quant-overview"
    target.mkdir(parents=True)
    (target / "stale.txt").write_text("stale")
    rc = installer.main(["install", "--project", "gs-quant-overview"])
    assert rc == 0
    assert not (target / "stale.txt").exists()


def test_install_default_all(isolated_home):
    _, project = isolated_home
    rc = installer.main(["install", "--project"])
    assert rc == 0
    target_dir = project / ".claude" / "skills"
    for name in installer._discover_skills():
        assert (target_dir / name).exists()


def test_uninstall_removes_symlink(isolated_home):
    _, project = isolated_home
    installer.main(["install", "--project", "gs-quant-overview"])
    target = project / ".claude" / "skills" / "gs-quant-overview"
    assert target.exists() or target.is_symlink()
    rc = installer.main(["uninstall", "--project", "gs-quant-overview"])
    assert rc == 0
    assert not target.exists() and not target.is_symlink()


def test_uninstall_removes_copy(isolated_home, monkeypatch):
    _, project = isolated_home
    monkeypatch.setattr(installer, "_use_symlinks", lambda: False)
    installer.main(["install", "--project", "gs-quant-overview"])
    target = project / ".claude" / "skills" / "gs-quant-overview"
    assert target.is_dir()
    rc = installer.main(["uninstall", "--project", "gs-quant-overview"])
    assert rc == 0
    assert not target.exists()


def test_uninstall_missing_is_warning(isolated_home, capsys):
    rc = installer.main(["uninstall", "--project", "gs-quant-overview"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "skip" in out


def test_list_reports_state(isolated_home, capsys):
    installer.main(["install", "--project", "gs-quant-overview"])
    capsys.readouterr()
    rc = installer.main(["list"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "gs-quant-overview" in out
    assert "project=" in out


def test_invalid_skill_name_errors(isolated_home):
    with pytest.raises(SystemExit) as exc:
        installer.main(["install", "--project", "does-not-exist"])
    assert exc.value.code == 2


def test_non_tty_without_scope_errors(isolated_home, monkeypatch):
    monkeypatch.setattr(sys.stdin, "isatty", lambda: False)
    with pytest.raises(SystemExit) as exc:
        installer.main(["install", "gs-quant-overview"])
    assert exc.value.code == 2


def test_interactive_prompt(isolated_home, monkeypatch):
    _, project = isolated_home
    monkeypatch.setattr(sys.stdin, "isatty", lambda: True)
    monkeypatch.setattr("builtins.input", lambda _prompt: "p")
    rc = installer.main(["install", "gs-quant-overview"])
    assert rc == 0
    assert (project / ".claude" / "skills" / "gs-quant-overview").exists()
