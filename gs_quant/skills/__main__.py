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

import argparse
import os
import shutil
import sys
from pathlib import Path
from typing import Iterable, Optional

SKILLS_ROOT = Path(__file__).resolve().parent
SCOPE_GLOBAL = "global"
SCOPE_PROJECT = "project"


def _discover_skills() -> dict[str, Path]:
    """Return a mapping of skill name -> source directory for every bundled skill."""
    skills: dict[str, Path] = {}
    for entry in sorted(SKILLS_ROOT.iterdir()):
        if entry.is_dir() and (entry / "SKILL.md").is_file():
            skills[entry.name] = entry
    return skills


def _target_dir(scope: str) -> Path:
    if scope == SCOPE_GLOBAL:
        base = Path.home()
    elif scope == SCOPE_PROJECT:
        base = Path.cwd()
    else:
        raise ValueError(f"Unknown scope: {scope}")
    target = base / ".claude" / "skills"
    target.mkdir(parents=True, exist_ok=True)
    return target


def _resolve_skill_names(requested: Iterable[str], available: dict[str, Path]) -> list[str]:
    requested = list(requested)
    if not requested:
        return list(available)
    unknown = [name for name in requested if name not in available]
    if unknown:
        sys.stderr.write(
            "Unknown skill(s): {}\nAvailable skills: {}\n".format(", ".join(unknown), ", ".join(available) or "(none)")
        )
        sys.exit(2)
    return requested


def _remove_existing(target: Path) -> None:
    if target.is_symlink() or target.is_file():
        target.unlink()
    elif target.exists():
        shutil.rmtree(target)


def _use_symlinks() -> bool:
    return os.name != "nt"


def _install_one(source: Path, target: Path) -> str:
    _remove_existing(target)
    if _use_symlinks():
        target.symlink_to(source, target_is_directory=True)
        return "linked"
    shutil.copytree(source, target)
    return "copied"


def _prompt_scope(action: str) -> str:
    if not sys.stdin.isatty():
        sys.stderr.write("Scope is required when not running interactively. Pass --global or --project.\n")
        sys.exit(2)
    while True:
        answer = input(f"{action} (g)lobal (~/.claude/skills) or (p)roject (./.claude/skills)? [g/p] ").strip().lower()
        if answer in ("g", "global"):
            return SCOPE_GLOBAL
        if answer in ("p", "project"):
            return SCOPE_PROJECT


def _scope_from_args(args: argparse.Namespace, action: str) -> str:
    if getattr(args, "global_scope", False):
        return SCOPE_GLOBAL
    if getattr(args, "project_scope", False):
        return SCOPE_PROJECT
    return _prompt_scope(action)


def _install_status(skill: str) -> dict[str, Optional[str]]:
    """Return {scope: 'linked'|'copied'|None} per scope."""
    status: dict[str, Optional[str]] = {}
    for scope in (SCOPE_GLOBAL, SCOPE_PROJECT):
        path = _target_for_scope(scope) / skill
        if path.is_symlink():
            status[scope] = "linked"
        elif path.exists():
            status[scope] = "copied"
        else:
            status[scope] = None
    return status


def _target_for_scope(scope: str) -> Path:
    """Like _target_dir but does not create the directory (used for read-only checks)."""
    base = Path.home() if scope == SCOPE_GLOBAL else Path.cwd()
    return base / ".claude" / "skills"


def cmd_install(args: argparse.Namespace) -> int:
    available = _discover_skills()
    if not available:
        sys.stderr.write("No skills found in package.\n")
        return 1
    scope = _scope_from_args(args, "Install to")
    target_dir = _target_dir(scope)
    names = _resolve_skill_names(args.skills, available)
    for name in names:
        target = target_dir / name
        mode = _install_one(available[name], target)
        print(f"{mode} {name} -> {target}")
    return 0


def cmd_uninstall(args: argparse.Namespace) -> int:
    available = _discover_skills()
    scope = _scope_from_args(args, "Uninstall from")
    target_dir = _target_for_scope(scope)
    names = _resolve_skill_names(args.skills, available)
    for name in names:
        target = target_dir / name
        if target.is_symlink() or target.exists():
            _remove_existing(target)
            print(f"removed {name} from {target}")
        else:
            print(f"skip    {name} (not installed at {target})")
    return 0


def cmd_list(_args: argparse.Namespace) -> int:
    available = _discover_skills()
    if not available:
        print("No skills bundled with gs_quant.")
        return 0
    print(f"Bundled skills (source: {SKILLS_ROOT}):")
    for name in available:
        status = _install_status(name)
        parts = []
        for scope in (SCOPE_GLOBAL, SCOPE_PROJECT):
            mode = status[scope]
            if mode:
                parts.append(f"{scope}={mode}")
        suffix = ", ".join(parts) if parts else "not installed"
        print(f"  {name}  [{suffix}]")
    return 0


def _add_scope_flags(parser: argparse.ArgumentParser) -> None:
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--global", dest="global_scope", action="store_true", help="Target ~/.claude/skills")
    group.add_argument("--project", dest="project_scope", action="store_true", help="Target ./.claude/skills")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m gs_quant.skills",
        description="Install gs_quant agent skills into .claude/skills.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    install = sub.add_parser("install", help="Install bundled skills.")
    install.add_argument("skills", nargs="*", help="Skill name(s) to install. Defaults to all.")
    _add_scope_flags(install)
    install.set_defaults(func=cmd_install)

    uninstall = sub.add_parser("uninstall", help="Uninstall skills.")
    uninstall.add_argument("skills", nargs="*", help="Skill name(s) to uninstall. Defaults to all.")
    _add_scope_flags(uninstall)
    uninstall.set_defaults(func=cmd_uninstall)

    lst = sub.add_parser("list", help="List bundled skills and installation status.")
    lst.set_defaults(func=cmd_list)

    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
