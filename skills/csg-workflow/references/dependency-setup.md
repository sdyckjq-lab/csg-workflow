# Dependency Setup

Use this file when csg-workflow runs for the first time, or when the user asks to check dependencies, install missing plugins, or update installed plugins.

## When to Check

- First run: `docs/workflow/state.md` has no `## 依赖状态` section, or `最后检查` is `Not recorded yet`.
- User explicitly asks to check, install, or update dependencies.
- Do not check on every run. If state.md already has a dependency section with real data, trust it unless the user requests a re-check.

## How to Check

1. Run `python3 skills/csg-workflow/scripts/check_dependencies.py`.
2. Read the output. If any plugin shows `missing`, proceed to install guidance.
3. If using `--json`, parse the JSON output for `status` fields.

## Install Commands

When one or more plugins are missing, show the user which ones and ask for confirmation before running any command.

| Plugin | Install Command |
|--------|----------------|
| Compound | `claude plugin install compound-engineering@compound-engineering-plugin` |
| Superpowers | `claude plugin install superpowers@claude-plugins-official` |
| Gstack | `git clone https://github.com/garrytan/gstack.git ~/.claude/skills/gstack` |

Suggested prompt when plugins are missing:

"The following plugins are not installed: [list]. Would you like me to install them? Press Enter to confirm."

After installation, re-run `check_dependencies.py` to verify.

## Update Commands

Only run updates when the user explicitly asks. Do not check for updates automatically.

| Plugin | Update Command |
|--------|---------------|
| Compound | `claude plugin update compound-engineering@compound-engineering-plugin` |
| Superpowers | `claude plugin update superpowers@claude-plugins-official` |
| Gstack | `cd ~/.claude/skills/gstack && git pull` |

## State Update

After checking dependencies, update `docs/workflow/state.md` with a dependency section:

```markdown
## 依赖状态

最后检查: [date]
compound: [version or missing]
superpowers: [version or missing]
gstack: [installed or missing]
```

Only update when the check result changes or on first check.

## Safety Rules

- Do not auto-install. Only show the commands and wait for the user to confirm. This is consistent with `references/missing-skills.md`.
- Never auto-detect new versions or check for updates in the background.
- If `claude plugin install` fails, report the error and suggest the user check their Claude Code authentication.
- If `git clone` for Gstack fails, suggest checking network connectivity and disk space.
- If the user declines installation, continue with the workflow using manual fallbacks described in `references/missing-skills.md`.
