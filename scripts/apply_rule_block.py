#!/usr/bin/env python3
"""Safely preview or apply a csg-workflow rule block."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


BEGIN = "<!-- BEGIN CSG-WORKFLOW RULES -->"
END = "<!-- END CSG-WORKFLOW RULES -->"


class RuleBlockError(ValueError):
    pass


@dataclass
class ApplyResult:
    changed: bool
    written: bool
    action: str
    content: str


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalize_block(block: str) -> str:
    block = block.strip() + "\n"
    if block.count(BEGIN) != 1 or block.count(END) != 1:
        raise RuleBlockError("Template must contain exactly one CSG marker pair.")
    if block.index(BEGIN) > block.index(END):
        raise RuleBlockError("Template marker order is invalid.")
    return block


def replace_or_append(existing: str, block: str) -> tuple[str, str]:
    begin_count = existing.count(BEGIN)
    end_count = existing.count(END)

    if begin_count != end_count:
        raise RuleBlockError("Target has a broken CSG marker pair; repair it manually before editing.")
    if begin_count > 1:
        raise RuleBlockError("Target has multiple CSG marker pairs; repair it manually before editing.")

    block = normalize_block(block)

    if begin_count == 1:
        start = existing.index(BEGIN)
        end_start = existing.index(END)
        if start > end_start:
            raise RuleBlockError("Target marker order is invalid; repair it manually before editing.")
        end = end_start + len(END)
        suffix = existing[end:]
        if suffix.startswith("\n"):
            suffix = suffix[1:]
        content = existing[:start].rstrip() + "\n\n" + block.rstrip() + "\n"
        if suffix:
            content += "\n" + suffix.lstrip("\n")
        return content, "replace"

    if not existing.strip():
        return block, "create"

    return existing.rstrip() + "\n\n" + block, "append"


def apply_rule_block(target: Path, template: Path, *, write: bool = False, create_missing: bool = False) -> ApplyResult:
    block = normalize_block(read_text(template))

    if not target.exists():
        if not create_missing:
            return ApplyResult(
                changed=False,
                written=False,
                action="missing",
                content="Target file is missing. Recommend running /init first, or rerun with explicit creation after user confirmation.\n",
            )
        new_content = block
        if write:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(new_content, encoding="utf-8")
        return ApplyResult(changed=True, written=write, action="create", content=new_content)

    existing = read_text(target)
    new_content, action = replace_or_append(existing, block)
    changed = new_content != existing

    if write and changed:
        target.write_text(new_content, encoding="utf-8")

    return ApplyResult(changed=changed, written=write and changed, action=action, content=new_content)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Preview or apply a csg-workflow rule block")
    parser.add_argument("--target", required=True, help="AGENTS.md or CLAUDE.md path")
    parser.add_argument("--template", required=True, help="Rule block template path")
    parser.add_argument("--write", action="store_true", help="Write the change. Default previews only.")
    parser.add_argument("--create-missing", action="store_true", help="Create a missing target file after user confirmation.")
    args = parser.parse_args(argv)

    try:
        result = apply_rule_block(Path(args.target), Path(args.template), write=args.write, create_missing=args.create_missing)
    except RuleBlockError as exc:
        print(f"Rule block update refused: {exc}")
        return 2

    if result.action == "missing":
        print(result.content, end="")
        return 1

    mode = "written" if result.written else "preview"
    print(f"Rule block {mode}: action={result.action}, changed={result.changed}")
    if not args.write:
        print(result.content, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
