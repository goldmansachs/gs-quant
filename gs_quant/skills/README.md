# gs_quant.skills

> ⚠️ **Experimental:** This skills package and its CLI are experimental and subject to change in future versions.

Bundled agent "skills" (SKILL.md packages) for use with Claude Code, GitHub Copilot, and other tools that read from `.claude/skills/`.


## Quick-start
To globablly install all skills

```bash
python -m gs_quant.skills install --global
```

## Layout

Each skill lives in its own directory in this package and must contain a `SKILL.md` file:

```
gs_quant/skills/
    <skill-name>/
        SKILL.md
        ...supporting files
```

## Installer CLI

A small CLI is provided to install the bundled skills into a `.claude/skills/` directory so your agent tooling can discover them.

```bash
python -m gs_quant.skills <command> [options]
```

### Commands

| Command     | Description                                                              |
| ----------- | ------------------------------------------------------------------------ |
| `list`      | List bundled skills and show whether each is installed globally/locally. |
| `install`   | Install one or more skills (defaults to all).                            |
| `uninstall` | Remove one or more skills (defaults to all).                             |

### Scope flags

`install` and `uninstall` accept mutually-exclusive scope flags:

- `--global` — target `~/.claude/skills/` (available in any project).
- `--project` — target `./.claude/skills/` (only in the current working directory).

If neither flag is provided and the terminal is interactive, you'll be prompted. In non-interactive contexts (CI, scripts) one of the flags is required.

### Selecting skills

Pass skill names as positional arguments to install/uninstall a subset. With no names, the command applies to **all** bundled skills.

```bash
python -m gs_quant.skills install --project gs-quant-overview
python -m gs_quant.skills install --global                     # all skills, global
```

### How files are placed

- **Linux/macOS:** symlinks are created from `.claude/skills/<name>` to the source directory inside the installed `gs_quant` package. Updating gs_quant updates the skill automatically.
- **Windows:** the skill directory is copied (no symlinks). After upgrading gs_quant, re-run `install` to refresh.

If a target directory already exists at the destination it is **overwritten**.

### Examples

List bundled skills and current installation state:

```bash
$ python -m gs_quant.skills list
Bundled skills (source: /path/to/site-packages/gs_quant/skills):
  gs-quant-overview  [project=linked]
```

Install all skills into the current project:

```bash
$ python -m gs_quant.skills install --project
linked gs-quant-overview -> /your/project/.claude/skills/gs-quant-overview
```

Install only a specific skill globally:

```bash
$ python -m gs_quant.skills install --global gs-quant-overview
```

Uninstall from the current project:

```bash
$ python -m gs_quant.skills uninstall --project gs-quant-overview
```

## Adding a new skill

1. Create a new directory under `gs_quant/skills/<your-skill-name>/`.
2. Add a `SKILL.md` describing the skill (frontmatter + body, per the agent tool's skill spec).
3. Add any supporting markdown/code files in the same directory.
4. The skill is automatically picked up by the installer — no registration step required.
