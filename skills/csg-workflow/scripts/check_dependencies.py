#!/usr/bin/env python3
"""Check whether Compound, Superpowers, and Gstack are installed."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

COMPOUND_KEY = "compound-engineering@compound-engineering-plugin"
SUPERPOWERS_KEY = "superpowers@claude-plugins-official"
GSTACK_SKILL = "gstack/SKILL.md"


def check_plugins_json(plugins_path: Path) -> dict[str, dict[str, str]]:
    results: dict[str, dict[str, str]] = {}
    if not plugins_path.is_file():
        results["compound"] = {"status": "missing", "source": "installed_plugins.json"}
        results["superpowers"] = {"status": "missing", "source": "installed_plugins.json"}
        return results

    try:
        data = json.loads(plugins_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise ValueError("installed_plugins.json is malformed")

    plugins = data.get("plugins", {}) if isinstance(data, dict) else {}

    for name, key in [("compound", COMPOUND_KEY), ("superpowers", SUPERPOWERS_KEY)]:
        entries = plugins.get(key)
        if isinstance(entries, list) and entries:
            version = entries[0].get("version", "unknown")
            results[name] = {"status": "installed", "version": version, "source": "installed_plugins.json"}
        else:
            results[name] = {"status": "missing", "source": "installed_plugins.json"}

    return results


def check_gstack(skills_dir: Path) -> dict[str, str]:
    skill_path = skills_dir / GSTACK_SKILL
    if skill_path.is_file():
        return {"status": "installed", "source": "SKILL.md file check"}
    return {"status": "missing", "source": "SKILL.md file check"}


def check_dependencies(home: Path) -> dict[str, dict[str, str]]:
    plugins_path = home / ".claude" / "plugins" / "installed_plugins.json"
    skills_dir = home / ".claude" / "skills"

    results = check_plugins_json(plugins_path)
    results["gstack"] = check_gstack(skills_dir)
    return results


def format_text(results: dict[str, dict[str, str]]) -> str:
    lines = []
    for name in ("compound", "superpowers", "gstack"):
        info = results[name]
        if info["status"] == "installed":
            version = info.get("version")
            if version:
                lines.append(f"{name}: installed (v{version})")
            else:
                lines.append(f"{name}: installed")
        else:
            lines.append(f"{name}: missing")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check csg-workflow dependency installation status")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    parser.add_argument("--home", help="Override home directory (for testing)")
    args = parser.parse_args(argv)

    home = Path(args.home) if args.home else Path.home()

    try:
        results = check_dependencies(home)
    except ValueError as exc:
        print(f"Error: {exc}")
        return 2

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(format_text(results))

    all_installed = all(v["status"] == "installed" for v in results.values())
    return 0 if all_installed else 1


if __name__ == "__main__":
    raise SystemExit(main())
