#!/usr/bin/env python3
"""Validate the csg-workflow Skill package."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_FILES = [
    "SKILL.md",
    "agents/openai.yaml",
    "references/stage-router.md",
    "references/skill-selection.md",
    "references/handoff-state.md",
    "references/project-rules.md",
    "references/missing-skills.md",
    "references/dependency-setup.md",
    "assets/templates/AGENTS.md.block",
    "assets/templates/CLAUDE.md.block",
    "assets/templates/workflow/state.md",
    "assets/templates/workflow/decisions.md",
    "assets/templates/workflow/log.md",
    "scripts/apply_rule_block.py",
    "scripts/validate_package.py",
    "scripts/check_dependencies.py",
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
    "SKILL.md",
    "references/**/*.md",
    "agents/**/*.yaml",
    "scripts/**/*.py",
    "examples/**/*.md",
    "tests/pressure-scenarios/**/*.md",
]

OLD_ENTRY_PATHS = [
    "skills/csg-workflow/SKILL.md",
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
STATE_LINE_LIMIT = 60


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


def require_headings(issues: list[str], text: str, path: str, headings: list[str]) -> None:
    for heading in headings:
        pattern = rf"^##\s+{re.escape(heading)}\s*$"
        if not re.search(pattern, text, re.MULTILINE):
            issues.append(f"{path}: missing required heading: {heading}")


def validate(root: Path) -> list[str]:
    root = root.resolve()
    issues: list[str] = []

    for rel in REQUIRED_FILES:
        if not (root / rel).is_file():
            issues.append(f"{rel}: missing required file")

    # Regression check: old nested entry must not exist
    for old_rel in OLD_ENTRY_PATHS:
        if (root / old_rel).exists():
            issues.append(f"{old_rel}: old nested entry still exists, must be removed")

    skill_path = root / "SKILL.md"
    if skill_path.is_file():
        skill_text = read_text(skill_path)
        fm = frontmatter(skill_text)
        if not fm:
            issues.append("SKILL.md: missing YAML frontmatter")
        if not re.search(r"^name:\s*csg-workflow\s*$", fm, re.MULTILINE):
            issues.append("SKILL.md: missing name: csg-workflow")
        if not re.search(r"^description:\s*.+", fm, re.MULTILINE):
            issues.append("SKILL.md: missing description")
        require_contains(
            issues,
            skill_text,
            "SKILL.md",
            [
                "CSG means Compound, Superpowers, and Gstack",
                "V1 does not",
                "Ask the user before invoking or routing into the next Skill",
                "Never rewrite a whole `AGENTS.md` or `CLAUDE.md`",
                "state-health preflight",
                "ambiguous",
            ],
        )

    agent_path = root / "agents/openai.yaml"
    if agent_path.is_file():
        agent_text = read_text(agent_path)
        require_contains(
            issues,
            agent_text,
            "agents/openai.yaml",
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

    deps_ref_path = root / "references/dependency-setup.md"
    if deps_ref_path.is_file():
        deps_text = read_text(deps_ref_path)
        require_contains(
            issues,
            deps_text,
            "references/dependency-setup.md",
            ["compound-engineering", "superpowers@claude-plugins-official", "gstack", "git clone"],
        )

    stage_router_path = root / "references/stage-router.md"
    if stage_router_path.is_file():
        stage_router_text = read_text(stage_router_path)
        require_contains(
            issues,
            stage_router_text,
            "references/stage-router.md",
            ["state-health preflight", "repair obvious mismatches", "check `docs/workflow/log.md`"],
        )

    project_rules_path = root / "references/project-rules.md"
    if project_rules_path.is_file():
        project_rules_text = read_text(project_rules_path)
        require_contains(
            issues,
            project_rules_text,
            "references/project-rules.md",
            ["state-health preflight", "check `docs/workflow/log.md`", "source of truth"],
        )

    for rel in [
        "assets/templates/AGENTS.md.block",
        "assets/templates/CLAUDE.md.block",
    ]:
        path = root / rel
        if path.is_file():
            text = read_text(path)
            if text.count(RULE_BEGIN) != 1 or text.count(RULE_END) != 1:
                issues.append(f"{rel}: expected exactly one CSG rule marker pair")
            if "完整 workflow" in text or "完整 Skill 路线表" in text:
                issues.append(f"{rel}: rule block is too broad for startup rules")
            require_contains(
                issues,
                text,
                rel,
                ["state-health preflight", "obvious mismatch", "ambiguous", "in-progress checkpoint"],
            )

    handoff_path = root / "references/handoff-state.md"
    if handoff_path.is_file():
        handoff_text = read_text(handoff_path)
        require_contains(
            issues,
            handoff_text,
            "references/handoff-state.md",
            ["State Health Preflight", "Completed Task Snapshot", "40 lines", "60 lines", "ambiguous"],
        )

    for rel in [
        "assets/templates/workflow/state.md",
        "examples/minimal-project/docs/workflow/state.md",
    ]:
        path = root / rel
        if path.is_file():
            text = read_text(path)
            require_contains(
                issues,
                text,
                rel,
                ["状态: idle.", "当前 Skill:", "恢复时下一步"],
            )
            require_headings(
                issues,
                text,
                rel,
                ["当前阶段", "项目目标", "当前主要文档", "下一步", "上一个任务", "执行中检查点", "阻塞问题", "最近验证", "不要重复讨论", "依赖状态"],
            )
            if len(text.splitlines()) > STATE_LINE_LIMIT:
                issues.append(f"{rel}: state snapshot exceeds {STATE_LINE_LIMIT} lines")

    live_state_path = root / "docs/workflow/state.md"
    if live_state_path.is_file():
        text = read_text(live_state_path)
        require_headings(
            issues,
            text,
            "docs/workflow/state.md",
            ["当前阶段", "项目目标", "当前主要文档", "下一步", "上一个任务", "执行中检查点", "阻塞问题", "最近验证", "不要重复讨论", "依赖状态"],
        )
        require_contains(
            issues,
            text,
            "docs/workflow/state.md",
            ["状态:", "当前 Skill:", "恢复时下一步"],
        )
        if len(text.splitlines()) > STATE_LINE_LIMIT:
            issues.append("docs/workflow/state.md: state snapshot exceeds 60 lines")
        if "## 已完成内容" in text:
            issues.append("docs/workflow/state.md: contains long-history section")

    for rel in [
        "assets/templates/workflow/decisions.md",
        "examples/minimal-project/docs/workflow/decisions.md",
    ]:
        path = root / rel
        if path.is_file() and "长期决定" not in read_text(path):
            issues.append(f"{rel}: missing long-term decision guidance")

    for rel in [
        "assets/templates/workflow/log.md",
        "examples/minimal-project/docs/workflow/log.md",
    ]:
        path = root / rel
        if path.is_file() and "阶段记录" not in read_text(path):
            issues.append(f"{rel}: missing stage log guidance")

    scenarios_path = root / "tests/pressure-scenarios/csg-workflow-v1.md"
    if scenarios_path.is_file():
        scenarios = read_text(scenarios_path)
        for index in range(1, 16):
            if not re.search(rf"^## AE{index}:", scenarios, re.MULTILINE):
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
