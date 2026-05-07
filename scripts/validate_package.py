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
    "references/navigator/lifecycle.md",
    "references/navigator/skill-catalog.md",
    "references/navigator/router-rules.md",
    "references/navigator/next-step-card.md",
    "references/navigator/workspace-state.md",
    "assets/templates/cards/next-step.md",
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

LIFECYCLE_STAGES = {
    "bootstrap", "idea", "requirements", "plan", "work",
    "review", "qa", "delivery", "learning",
}
CARD_STATUSES = {"idle", "proposed", "in_progress", "blocked", "completed", "recovery_needed"}
CONFIDENCE_LEVELS = {"high", "medium", "low"}
SOURCE_FAMILIES = {"compound", "superpowers", "gstack", "csg", "manual"}
STABLE_ALIASES = {
    "setup-state", "resume-or-clear", "requirements-discovery",
    "plan-prep", "implementation", "code-review", "qa",
    "delivery", "post-release-check", "learning-capture",
    "work-discipline",
}
SCALAR_FIELDS = {
    "id", "current_stage", "target_stage_after_completion", "confidence",
    "recommended_role", "recommended_skill", "source_family", "why",
    "user_goal", "prompt",
}

REQUIRED_CARD_FIELDS = [
    "id",
    "current_stage",
    "target_stage_after_completion",
    "confidence",
    "recommended_role",
    "recommended_skill",
    "source_family",
    "why",
    "user_goal",
    "prompt",
    "expected_output",
    "state_updates_on_confirm",
    "state_updates_after_success",
    "not_now",
    "fallback_if_missing",
    "rendering",
    "routing_trace",
]

NESTED_MAP_FIELDS = frozenset({"state_updates_on_confirm", "state_updates_after_success", "rendering"})

REQUIRED_STATE_UPDATE_KEYS = {"status", "active_card", "current_stage", "current_skill", "resume_action"}
REQUIRED_SUCCESS_KEYS = {"status", "current_stage", "last_completed_card", "next_checkpoint"}

WRAPPER_DELEGATION_TERMS = {
    "references/stage-router.md": ["navigator/lifecycle.md", "navigator/router-rules.md"],
    "references/skill-selection.md": ["navigator/skill-catalog.md"],
    "references/handoff-state.md": ["navigator/workspace-state.md"],
}

WRAPPER_SPLIT_BRAIN_PATTERNS = [
    (re.compile(r"^\|.*Stage.*Signals.*Default Skill", re.MULTILINE), "lifecycle table in wrapper"),
    (re.compile(r"^\|.*Category.*Default.*Optional", re.MULTILINE), "Skill selection table in wrapper"),
    (re.compile(r"^\|.*Source.*Role.*Use For", re.MULTILINE), "role mapping table in wrapper"),
]


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


def parse_card_blocks(text: str) -> list[dict[str, str | list[str | dict[str, str]]]]:
    """Parse ```next-step-card fenced blocks from text.

    Returns a list of parsed card dicts. Each value is either a string,
    a list of strings, or a list of dicts (for nested maps).

    Supports only: key: value, top-level lists, one-level nested maps.
    """
    cards: list[dict[str, str | list[str | dict[str, str]]]] = []
    in_block = False
    current: dict[str, str | list[str | dict[str, str]]] = {}
    current_list_key: str | None = None
    current_map_key: str | None = None

    for line in text.splitlines():
        stripped = line.strip()

        if stripped == "```next-step-card":
            in_block = True
            current = {}
            current_list_key = None
            current_map_key = None
            continue

        if in_block and stripped == "```":
            in_block = False
            if current:
                cards.append(current)
            continue

        if not in_block:
            continue

        # Two-space indented content
        if line.startswith("  "):
            inner = stripped
            if inner.startswith("- "):
                item = inner[2:].strip()
                if current_list_key is not None:
                    current[current_list_key].append(item)
                elif current_map_key is not None:
                    pass  # list items inside a nested map not supported
            elif ": " in inner:
                k, v = inner.split(": ", 1)
                if current_map_key is not None:
                    map_list = current[current_map_key]
                    if isinstance(map_list, list) and len(map_list) > 0 and isinstance(map_list[-1], dict):
                        map_list[-1][k] = v
                    else:
                        map_list.append({k: v})
            continue

        # Reset nested context on non-indented lines
        current_list_key = None
        current_map_key = None

        # key: value (scalar)
        if ": " in stripped:
            k, v = stripped.split(": ", 1)
            current[k] = v
            continue

        # key: (start of list or nested map)
        if stripped.endswith(":"):
            k = stripped[:-1]
            if k in NESTED_MAP_FIELDS:
                current[k] = []
                current_map_key = k
            else:
                current[k] = []
                current_list_key = k
            continue

    # Unclosed block: keep partial data so validator can report issues
    if in_block and current:
        cards.append(current)

    return cards


def validate_cards(issues: list[str], text: str, path: str) -> tuple[list[str], list[dict]]:
    """Validate all next-step-card blocks in text. Return (card_ids, cards)."""
    cards = parse_card_blocks(text)
    if not cards:
        issues.append(f"{path}: missing_card_block — no next-step-card blocks found")
        return [], []

    card_ids: list[str] = []
    seen_ids: set[str] = set()

    for card in cards:
        card_id = str(card.get("id", "unknown"))

        if card_id in seen_ids:
            issues.append(f"{path}: duplicate_card_id — '{card_id}' appears more than once. Fix: use unique IDs.")
        else:
            seen_ids.add(card_id)
            card_ids.append(card_id)

        # Check required fields
        for field in REQUIRED_CARD_FIELDS:
            if field not in card:
                issues.append(f"{path}: missing_field — card '{card_id}' missing '{field}'. Fix: add the field.")

        # Validate stage fields
        for stage_field in ("current_stage", "target_stage_after_completion"):
            val = str(card.get(stage_field, ""))
            if val and val not in LIFECYCLE_STAGES:
                issues.append(f"{path}: invalid_stage — card '{card_id}' has '{stage_field}: {val}'. Fix: use one of {sorted(LIFECYCLE_STAGES)}.")

        # Validate confidence
        conf = str(card.get("confidence", ""))
        if conf and conf not in CONFIDENCE_LEVELS:
            issues.append(f"{path}: invalid_confidence — card '{card_id}' has 'confidence: {conf}'. Fix: use high, medium, or low.")

        # Validate source_family
        fam = str(card.get("source_family", ""))
        if fam and fam not in SOURCE_FAMILIES:
            issues.append(f"{path}: invalid_source_family — card '{card_id}' has 'source_family: {fam}'. Fix: use one of {sorted(SOURCE_FAMILIES)}.")

        # Validate recommended_role
        role = str(card.get("recommended_role", ""))
        if role and role not in STABLE_ALIASES:
            issues.append(f"{path}: invalid_role — card '{card_id}' has 'recommended_role: {role}'. Fix: use one of {sorted(STABLE_ALIASES)}.")

        # Validate scalar fields are strings, not lists (parser edge case)
        for sf in SCALAR_FIELDS:
            val = card.get(sf)
            if val is not None and isinstance(val, list):
                issues.append(f"{path}: malformed_card_block — card '{card_id}' field '{sf}' is empty (parsed as list). Fix: provide a value.")

        # Validate routing_trace has at least 2 items
        rt = card.get("routing_trace")
        if isinstance(rt, list) and len(rt) < 2:
            issues.append(f"{path}: missing_field — card '{card_id}' routing_trace has fewer than 2 items. Fix: add 2-4 routing trace bullets.")

        # Validate expected_output is non-empty list
        eo = card.get("expected_output")
        if eo is not None:
            if not isinstance(eo, list) or len(eo) == 0:
                issues.append(f"{path}: missing_field — card '{card_id}' has empty expected_output. Fix: add at least one item.")
        else:
            issues.append(f"{path}: missing_field — card '{card_id}' missing 'expected_output'.")

        # Validate state_updates_on_confirm has required nested keys
        suc = card.get("state_updates_on_confirm")
        if isinstance(suc, list):
            found_keys: set[str] = set()
            for item in suc:
                if isinstance(item, dict):
                    found_keys.update(item.keys())
            missing_keys = REQUIRED_STATE_UPDATE_KEYS - found_keys
            if missing_keys:
                issues.append(f"{path}: missing_nested_key — card '{card_id}' state_updates_on_confirm missing {missing_keys}. Fix: add the keys.")
        elif suc is None:
            pass  # already caught by required field check

        # Validate state_updates_after_success has required nested keys
        sua = card.get("state_updates_after_success")
        if isinstance(sua, list):
            found_keys_s = set()
            for item in sua:
                if isinstance(item, dict):
                    found_keys_s.update(item.keys())
            missing_keys_s = REQUIRED_SUCCESS_KEYS - found_keys_s
            if missing_keys_s:
                issues.append(f"{path}: missing_nested_key — card '{card_id}' state_updates_after_success missing {missing_keys_s}. Fix: add the keys.")
        elif sua is None:
            pass

        # Validate fallback_if_missing is non-empty list
        fb = card.get("fallback_if_missing")
        if fb is not None:
            if not isinstance(fb, list) or len(fb) == 0:
                issues.append(f"{path}: missing_field — card '{card_id}' has empty fallback_if_missing. Fix: add at least one fallback.")
        else:
            issues.append(f"{path}: missing_field — card '{card_id}' missing 'fallback_if_missing'.")

        # Validate rendering has markdown
        rendering = card.get("rendering")
        if isinstance(rendering, list):
            has_markdown = any(
                isinstance(item, dict) and "markdown" in item
                for item in rendering
            )
            if not has_markdown:
                issues.append(f"{path}: missing_nested_key — card '{card_id}' rendering missing 'markdown'. Fix: add 'markdown: required'.")

    return card_ids, cards


def validate_navigator(issues: list[str], root: Path) -> None:
    """Validate navigator reference files."""
    # lifecycle.md
    path = root / "references/navigator/lifecycle.md"
    if path.is_file():
        text = read_text(path)
        for stage in LIFECYCLE_STAGES:
            if stage not in text:
                issues.append(f"references/navigator/lifecycle.md: missing stage '{stage}' in lifecycle")
        if "recovery" not in text:
            issues.append("references/navigator/lifecycle.md: missing recovery mode documentation")
        if "earliest unmet" not in text:
            issues.append("references/navigator/lifecycle.md: missing tie-break rule")
        require_contains(issues, text, "references/navigator/lifecycle.md",
                         ["Lifecycle Enum", "Routing Matrix", "Tie-Break Rule"])

    # skill-catalog.md
    path = root / "references/navigator/skill-catalog.md"
    if path.is_file():
        text = read_text(path)
        require_contains(issues, text, "references/navigator/skill-catalog.md",
                         ["Stable Alias Layer", "Resolution Order", "Availability Discovery",
                          "setup-state", "requirements-discovery", "implementation",
                          "ce-brainstorm", "ce-plan", "ce-work"])

    # router-rules.md
    path = root / "references/navigator/router-rules.md"
    if path.is_file():
        text = read_text(path)
        require_contains(issues, text, "references/navigator/router-rules.md",
                         ["Exactly One Default", "Confidence", "Tie-Break",
                          "Confirmation Boundary", "Prompt Injection Guard",
                          "lifecycle order", "confirmation rules", "safety boundaries"])

    # next-step-card.md — parse and validate all cards
    path = root / "references/navigator/next-step-card.md"
    if path.is_file():
        text = read_text(path)
        require_contains(issues, text, "references/navigator/next-step-card.md",
                         ["Required Card Fields", "Fenced Block Syntax", "Canonical Card Examples",
                          "Renderer Rules", "Prompt Injection Guard"])
        card_ids, cards = validate_cards(issues, text, "references/navigator/next-step-card.md")

        # Check that every lifecycle stage has at least one card
        stages_with_cards: set[str] = set()
        for card in cards:
            cs = card.get("current_stage")
            if isinstance(cs, str) and cs in LIFECYCLE_STAGES:
                stages_with_cards.add(cs)

        for stage in LIFECYCLE_STAGES:
            if stage not in stages_with_cards:
                issues.append(f"references/navigator/next-step-card.md: no canonical card for stage '{stage}'")

    # workspace-state.md
    path = root / "references/navigator/workspace-state.md"
    if path.is_file():
        text = read_text(path)
        require_contains(issues, text, "references/navigator/workspace-state.md",
                         ["State-Health Preflight", "Card Status Enum",
                          "Confirmation Semantics", "Old-State Migration",
                          "Recovery-Mode", "Post-compact", "Repeat confirmation",
                          "Conflicting evidence"])
        # Check status enum values
        for status in CARD_STATUSES:
            if status not in text:
                issues.append(f"references/navigator/workspace-state.md: missing card status '{status}'")


def validate_card_template(issues: list[str], root: Path) -> None:
    """Validate the next-step card template."""
    path = root / "assets/templates/cards/next-step.md"
    if path.is_file():
        text = read_text(path)
        require_contains(issues, text, "assets/templates/cards/next-step.md",
                         ["Display Hierarchy", "next-step-card", "recommended_role",
                          "current_stage", "target_stage_after_completion"])


def validate_wrappers(issues: list[str], root: Path) -> None:
    """Validate compatibility wrappers have delegation text and no split-brain."""
    for rel, required_terms in WRAPPER_DELEGATION_TERMS.items():
        path = root / rel
        if not path.is_file():
            continue
        text = read_text(path)

        # Must mention navigator docs it delegates to
        for term in required_terms:
            if term not in text:
                issues.append(f"{rel}: wrapper_split_brain — missing delegation to '{term}'. Fix: add delegation text pointing to navigator docs.")

        # Must contain "Compatibility Wrapper" or "superseded"
        if "Compatibility Wrapper" not in text and "superseded" not in text:
            issues.append(f"{rel}: wrapper_split_brain — missing wrapper marker. Fix: add '(Compatibility Wrapper)' to title or 'superseded' notice.")

        # Must not contain full tables (split-brain guard)
        for pattern, label in WRAPPER_SPLIT_BRAIN_PATTERNS:
            if pattern.search(text):
                issues.append(f"{rel}: wrapper_split_brain — contains {label}. Fix: remove full tables, keep only delegation text.")


def validate_skill_md(issues: list[str], root: Path) -> None:
    """Validate SKILL.md with navigator-aware checks."""
    skill_path = root / "SKILL.md"
    if not skill_path.is_file():
        return
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
            "Skill GPS",
            "next-step card",
            "references/navigator/lifecycle.md",
            "references/navigator/skill-catalog.md",
            "references/navigator/router-rules.md",
            "references/navigator/next-step-card.md",
            "references/navigator/workspace-state.md",
            "routing context",
            "safety boundaries",
        ],
    )


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

    validate_skill_md(issues, root)

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
        for index in range(1, 22):
            if not re.search(rf"^## AE{index}:", scenarios, re.MULTILINE):
                issues.append(f"tests/pressure-scenarios/csg-workflow-v1.md: missing AE{index}")

    # Navigator validation
    validate_navigator(issues, root)
    validate_card_template(issues, root)
    validate_wrappers(issues, root)

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
