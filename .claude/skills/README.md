# Skills

If you are contributing to the gs_quant project this directory holds [agent skills](https://docs.claude.com/en/docs/claude-code/skills) (each as a subdirectory containing a `SKILL.md`) that are picked up by Claude Code, GitHub Copilot, and other tools that read from `.claude/skills/`.

## gs_quant skills
If you are **looking for skills to help you use the gs_quant SDK** then the `gs_quant` Python package ships a set of skills inside its source tree at [gs_quant/skills/](../../gs_quant/skills/). After installing the package you can install those skills into your project (or your global `~/.claude/skills/`) by running:

```bash
python -m gs_quant.skills install
```

See the [gs_quant skills README](../../gs_quant/skills/README.md) for the full list of CLI commands, scope flags, and details on how skills are placed.
