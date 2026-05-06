#!/usr/bin/env python3
"""Validate the csg-workflow Skill package."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_FILES = [
    "skills/csg-workflow/SKILL.md",
    "skills/csg-workflow/agents/openai.yaml",
    "skills/csg-workflow/references/stage-router.md",
    "skills/csg-workflow/references/skill-selection.md",
    "skills/csg-workflow/references/handoff-state.md",
    "skills/csg-workflow/references/project-rules.md",
    "skills/csg-workflow/references/missing-skills.md",
    "skills/csg-workflow/assets/templates/AGENTS.md.block",
    "skills/csg-workflow/assets/templates/CLAUDE.md.block",
    "skills/csg-workflow/assets/templates/workflow/state.md",
    "skills/csg-workflow/assets/templates/workflow/decisions.md",
    "skills/csg-workflow/assets/templates/workflow/log.md",
    "skills/csg-workflow/scripts/apply_rule_block.py",
    "skills/csg-workflow/scripts/validate_package.py",
    "examples/minimal-project/README.md",
    "examples/minimal-project/docs/workflow/state.md",
    "examples/minimal-project/docs/workflow/decisions.md",
    "examples/minimal-project/docs/workflow/log.md",
    "tests/pressure-scenarios/csg-workflow-v1.md",
    "tests/test_csg_workflow_package.py",
    "LICENSE",
    "README.md",
]

SCAN_GLOBS = [
    "README.md",
    "LICENSE",
    "skills/csg-workflow/**/*.md",
    "skills/csg-workflow/**/*.yaml",
    "skills/csg-workflow/**/*.py",
    "examples/**/*.md",
    "tests/pressure-scenarios/**/*.md",
]

FORBIDDEN_PATTERNS = [
    (re.compile("/" + "Users/"), "absolute local path"),
    (re.compile("file" + "://"), "file URI"),
    (re.compile("vscode" + "://"), "editor URI"),
    (re.compile(r"\bTO" + r"DO\b"), "unfinished marker"),
    (re.compile(r"\bTB" + r"D\b"), "unfinished marker"),
    (re.compile("待" + "补|待" + "定"), "unfinished marker"),
]

RULE_BEGIN = "<!-- BEGIN CSG-WORKFLOW RULES -->"
RULE_END = "<!-- END CSG-WORKFLOW RULES -->"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def has_frontmatter(text: str) -> bool:
    return text.startswith("---\n") and "\n---\n" in text[4:]


def frontmatter(text: str) -> str:
    if not has_frontmatter(text):
        return ""
    return text.split("\n---\n", 1)[0].removeprefix("---\n")


def unique_paths(root: Path) -> list[Path]:
    seen: set[Path] = set()
    paths: list[Path] = []
    for pattern in SCAN_GLOBS:
        for path in root.glob(pattern):
            if path.is_file() and path not in seen:
                seen.add(path)
                paths.append(path)
    return paths


def require_contains(issues: list[str], text: str, path: str, terms: list[str]) -> None:
    for term in terms:
        if term not in text:
            issues.append(f"{path}: missing required text: {term}")


def validate(root: Path) -> list[str]:
    root = root.resolve()
    issues: list[str] = []

    for rel in REQUIRED_FILES:
        if not (root / rel).is_file():
            issues.append(f"{rel}: missing required file")

    skill_path = root / "skills/csg-workflow/SKILL.md"
    if skill_path.is_file():
        skill_text = read_text(skill_path)
        fm = frontmatter(skill_text)
        if not fm:
            issues.append("skills/csg-workflow/SKILL.md: missing YAML frontmatter")
        if not re.search(r"^name:\s*csg-workflow\s*$", fm, re.MULTILINE):
            issues.append("skills/csg-workflow/SKILL.md: missing name: csg-workflow")
        if not re.search(r"^description:\s*.+", fm, re.MULTILINE):
            issues.append("skills/csg-workflow/SKILL.md: missing description")
        require_contains(
            issues,
            skill_text,
            "skills/csg-workflow/SKILL.md",
            [
                "CSG means Compound, Superpowers, and Gstack",
                "V1 does not",
                "Ask the user before invoking or routing into the next Skill",
                "Never rewrite a whole `AGENTS.md` or `CLAUDE.md`",
            ],
        )

    agent_path = root / "skills/csg-workflow/agents/openai.yaml"
    if agent_path.is_file():
        agent_text = read_text(agent_path)
        require_contains(
            issues,
            agent_text,
            "skills/csg-workflow/agents/openai.yaml",
            ["display_name:", "short_description:", "default_prompt:", "$csg-workflow"],
        )

    readme_path = root / "README.md"
    if readme_path.is_file():
        readme = read_text(readme_path)
        require_contains(
            issues,
            readme,
            "README.md",
            ["CSG", "Compound", "Superpowers", "Gstack", "安装", "依赖", "兼容", "许可证", "最小示例", "第一版", "不自动安装"],
        )
        if "会自动安装" in readme:
            issues.append("README.md: claims automatic dependency installation")

    license_path = root / "LICENSE"
    if license_path.is_file() and "MIT License" not in read_text(license_path):
        issues.append("LICENSE: expected MIT License text")

    for rel in [
        "skills/csg-workflow/assets/templates/AGENTS.md.block",
        "skills/csg-workflow/assets/templates/CLAUDE.md.block",
    ]:
        path = root / rel
        if path.is_file():
            text = read_text(path)
            if text.count(RULE_BEGIN) != 1 or text.count(RULE_END) != 1:
                issues.append(f"{rel}: expected exactly one CSG rule marker pair")
            if "完整 workflow" in text or "完整 Skill 路线表" in text:
                issues.append(f"{rel}: rule block is too broad for startup rules")

    for rel in [
        "skills/csg-workflow/assets/templates/workflow/state.md",
        "examples/minimal-project/docs/workflow/state.md",
    ]:
        path = root / rel
        if path.is_file():
            text = read_text(path)
            require_contains(
                issues,
                text,
                rel,
                ["当前阶段", "项目目标", "当前主要文档", "下一步", "阻塞问题", "最近验证", "不要重复讨论"],
            )

    for rel in [
        "skills/csg-workflow/assets/templates/workflow/decisions.md",
        "examples/minimal-project/docs/workflow/decisions.md",
    ]:
        path = root / rel
        if path.is_file() and "长期决定" not in read_text(path):
            issues.append(f"{rel}: missing long-term decision guidance")

    for rel in [
        "skills/csg-workflow/assets/templates/workflow/log.md",
        "examples/minimal-project/docs/workflow/log.md",
    ]:
        path = root / rel
        if path.is_file() and "阶段记录" not in read_text(path):
            issues.append(f"{rel}: missing stage log guidance")

    scenarios_path = root / "tests/pressure-scenarios/csg-workflow-v1.md"
    if scenarios_path.is_file():
        scenarios = read_text(scenarios_path)
        for index in range(1, 11):
            if f"AE{index}" not in scenarios:
                issues.append(f"tests/pressure-scenarios/csg-workflow-v1.md: missing AE{index}")

    for path in unique_paths(root):
        text = read_text(path)
        rel = path.relative_to(root)
        for pattern, label in FORBIDDEN_PATTERNS:
            if pattern.search(text):
                issues.append(f"{rel}: contains {label}")

    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the csg-workflow package")
    parser.add_argument("--root", default=".", help="Repository root to validate")
    args = parser.parse_args(argv)

    issues = validate(Path(args.root))
    if issues:
        print("Validation failed:")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print("Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
