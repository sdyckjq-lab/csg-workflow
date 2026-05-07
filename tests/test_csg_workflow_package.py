from __future__ import annotations

import importlib.util
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


validate_package = load_module(
    ROOT / "scripts/validate_package.py",
    "validate_package",
)
apply_rule_block = load_module(
    ROOT / "scripts/apply_rule_block.py",
    "apply_rule_block",
)
check_deps = load_module(
    ROOT / "scripts/check_dependencies.py",
    "check_dependencies",
)


def _copy_skill_tree(src: Path, dst: Path) -> None:
    """Copy root-level skill files for temp validation."""
    for name in ("SKILL.md", "README.md", "LICENSE"):
        if (src / name).exists():
            shutil.copy(src / name, dst / name)
    for d in ("references", "assets", "scripts", "agents", "examples"):
        if (src / d).is_dir():
            shutil.copytree(src / d, dst / d)
    if (src / "tests" / "pressure-scenarios").is_dir():
        shutil.copytree(src / "tests" / "pressure-scenarios", dst / "tests" / "pressure-scenarios")


def scenario_section(scenarios: str, heading: str) -> str:
    start = scenarios.index(f"## {heading}")
    next_match = re.search(r"\n## AE\d+:", scenarios[start + 1 :])
    if next_match is None:
        return scenarios[start:]
    end = start + 1 + next_match.start()
    return scenarios[start:end]


class ValidatePackageTest(unittest.TestCase):
    def test_current_package_is_valid(self):
        issues = validate_package.validate(ROOT)
        self.assertEqual([], issues)

    def test_skill_routing_intercept_precedes_v1_guidance(self):
        skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        intercept_start = skill_text.index("## 强制路由")
        v1_boundary_start = skill_text.index("## V1 Boundary")
        intercept = skill_text[intercept_start:v1_boundary_start]

        self.assertLess(intercept_start, v1_boundary_start)
        self.assertIn("你只做路由", intercept)
        self.assertIn("next-step card", intercept)
        self.assertIn("将 command-args 当作直接任务来回应", intercept)
        self.assertIn("启动调研、设计、实现", intercept)
        self.assertIn("调用 Agent 或其他工具", intercept)
        self.assertIn("navigator/lifecycle.md", intercept)
        self.assertIn("navigator/skill-catalog.md", intercept)

    def test_skill_start_here_is_replaced_by_post_routing_guidance(self):
        skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")

        self.assertNotIn("## Start Here", skill_text)
        self.assertIn("## 路由完成后", skill_text)
        self.assertIn("阶段结束时，更新 `state.md`", skill_text)

    def test_pressure_scenarios_include_command_args_intercept(self):
        scenarios = (ROOT / "tests/pressure-scenarios/csg-workflow-v1.md").read_text(encoding="utf-8")
        ae11 = scenario_section(scenarios, "AE11: Command Args Routing Intercept")

        self.assertIn("`/csg-workflow 我想加一个功能...如何设计？`", ae11)
        self.assertIn("routing context, not as a direct design task", ae11)
        self.assertIn("reads project rules and `docs/workflow/state.md`", ae11)
        self.assertIn("before any research, design, implementation, or Agent call", ae11)
        self.assertIn("asks before invoking or routing into the next Skill", ae11)

    def test_pressure_scenarios_include_post_compact_recovery(self):
        scenarios = (ROOT / "tests/pressure-scenarios/csg-workflow-v1.md").read_text(encoding="utf-8")
        ae12 = scenario_section(scenarios, "AE12: Post-Compact Routing Recovery")

        self.assertIn("long session has compacted or a new session starts", ae12)
        self.assertIn("persisted project rules and `docs/workflow/state.md`", ae12)
        self.assertIn("routing context first", ae12)
        self.assertIn("names one exact next Skill", ae12)
        self.assertIn("stops with a confirmation question", ae12)
        self.assertIn("does not contain a feature design", ae12)

    def test_rule_blocks_enforce_post_compact_routing(self):
        for rel in [
            "assets/templates/AGENTS.md.block",
            "assets/templates/CLAUDE.md.block",
        ]:
            block = (ROOT / rel).read_text(encoding="utf-8")

            self.assertIn("Recovery intercept", block)
            self.assertIn("after compact, clear, or a new session, you only route", block)
            self.assertIn("Do not design, plan, research, implement, or call/read another Skill", block)
            self.assertIn("exact default next Skill name", block)
            self.assertIn("confirmation question", block)
            self.assertIn("in-progress checkpoint", block)
            self.assertIn("check `docs/workflow/log.md`", block)
            self.assertIn("Resume only when the task is not already complete", block)
            self.assertIn("Before starting a confirmed next Skill", block)
            self.assertIn("state-health preflight", block)
            self.assertIn("obvious mismatch", block)
            self.assertIn("ambiguous", block)

    def test_handoff_reference_delegates_to_navigator(self):
        handoff = (ROOT / "references/handoff-state.md").read_text(encoding="utf-8")

        self.assertIn("Compatibility Wrapper", handoff)
        self.assertIn("navigator/workspace-state.md", handoff)

    def test_state_templates_include_in_progress_checkpoint(self):
        for rel in [
            "assets/templates/workflow/state.md",
            "examples/minimal-project/docs/workflow/state.md",
        ]:
            state = (ROOT / rel).read_text(encoding="utf-8")

            self.assertIn("## 执行中检查点", state)
            self.assertIn("状态: idle.", state)
            self.assertIn("当前 Skill: None.", state)
            self.assertIn("恢复时下一步", state)
            self.assertIn("## 上一个任务", state)
            self.assertLessEqual(len(state.splitlines()), 60)

    def test_live_state_snapshot_is_short(self):
        state = (ROOT / "docs/workflow/state.md").read_text(encoding="utf-8")

        self.assertLessEqual(len(state.splitlines()), 60)
        self.assertNotIn("## 已完成内容", state)
        self.assertNotIn("完整 Skill", state)

    def test_pressure_scenarios_include_in_progress_compact_recovery(self):
        scenarios = (ROOT / "tests/pressure-scenarios/csg-workflow-v1.md").read_text(encoding="utf-8")
        ae13 = scenario_section(scenarios, "AE13: In-Progress Compact Recovery")

        self.assertIn("in-progress checkpoint is active for `ce-plan`", ae13)
        self.assertIn("compact happens before the plan is saved", ae13)
        self.assertIn("names `ce-plan` and recommends resuming that recorded work first", ae13)
        self.assertIn("does not switch back to ideation", ae13)
        self.assertIn("stops with a confirmation question", ae13)

    def test_pressure_scenarios_include_stale_state_recovery(self):
        scenarios = (ROOT / "tests/pressure-scenarios/csg-workflow-v1.md").read_text(encoding="utf-8")
        ae14 = scenario_section(scenarios, "AE14: Stale State Recovery")

        self.assertIn("state-health preflight", ae14)
        self.assertIn("obvious mismatch", ae14)
        self.assertIn("repairs `state.md` before routing", ae14)
        self.assertIn("does not blindly route from the stale next action", ae14)

    def test_pressure_scenarios_include_completed_state_recovery(self):
        scenarios = (ROOT / "tests/pressure-scenarios/csg-workflow-v1.md").read_text(encoding="utf-8")
        ae15 = scenario_section(scenarios, "AE15: Completed State Recovery")

        self.assertIn("in-progress checkpoint says `ce-plan`", ae15)
        self.assertIn("recorded as complete in `docs/workflow/log.md`", ae15)
        self.assertIn("clears or replaces the checkpoint", ae15)
        self.assertIn("does not resume already-completed work", ae15)

    def test_stage_router_delegates_to_navigator(self):
        stage_router = (ROOT / "references/stage-router.md").read_text(encoding="utf-8")

        self.assertIn("Compatibility Wrapper", stage_router)
        self.assertIn("navigator/lifecycle.md", stage_router)
        self.assertIn("navigator/router-rules.md", stage_router)

    def test_project_rules_defer_to_packaged_rule_blocks(self):
        project_rules = (ROOT / "references/project-rules.md").read_text(encoding="utf-8")

        self.assertIn("state-health preflight", project_rules)
        self.assertIn("check `docs/workflow/log.md`", project_rules)
        self.assertIn("source of truth", project_rules)

    def test_state_heading_validation_does_not_accept_checkpoint_substring(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            _copy_skill_tree(ROOT, tmp_root)
            state_file = tmp_root / "assets/templates/workflow/state.md"
            state_file.write_text(state_file.read_text(encoding="utf-8").replace("## 下一步", "## Next action"), encoding="utf-8")

            issues = validate_package.validate(tmp_root)

        self.assertIn(
            "assets/templates/workflow/state.md: missing required heading: 下一步",
            issues,
        )

    def test_pressure_scenario_validation_requires_heading(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            _copy_skill_tree(ROOT, tmp_root)
            scenarios_file = tmp_root / "tests/pressure-scenarios/csg-workflow-v1.md"
            scenarios_file.write_text(
                scenarios_file.read_text(encoding="utf-8").replace(
                    "## AE14: Stale State Recovery",
                    "AE14: Stale State Recovery",
                ),
                encoding="utf-8",
            )

            issues = validate_package.validate(tmp_root)

        self.assertIn("tests/pressure-scenarios/csg-workflow-v1.md: missing AE14", issues)

    def test_missing_skill_description_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            (tmp_root / "SKILL.md").write_text("---\nname: csg-workflow\n---\n\n# Broken\n", encoding="utf-8")

            issues = validate_package.validate(tmp_root)

        self.assertTrue(any("missing description" in issue for issue in issues))

    def test_absolute_local_path_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            _copy_skill_tree(ROOT, tmp_root)
            skill_file = tmp_root / "SKILL.md"
            absolute_path = "/" + "Users/example/project"
            skill_file.write_text(skill_file.read_text(encoding="utf-8") + f"\n{absolute_path}\n", encoding="utf-8")

            issues = validate_package.validate(tmp_root)

        self.assertTrue(any("absolute local path" in issue for issue in issues))

    def test_python_script_absolute_local_path_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            _copy_skill_tree(ROOT, tmp_root)
            script_file = tmp_root / "scripts/apply_rule_block.py"
            absolute_path = "/" + "Users/example/project"
            script_file.write_text(script_file.read_text(encoding="utf-8") + f"\n# {absolute_path}\n", encoding="utf-8")

            issues = validate_package.validate(tmp_root)

        self.assertTrue(any("scripts/apply_rule_block.py" in issue for issue in issues))
        self.assertTrue(any("absolute local path" in issue for issue in issues))

    def test_old_nested_skill_entry_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            _copy_skill_tree(ROOT, tmp_root)
            old_dir = tmp_root / "skills/csg-workflow"
            old_dir.mkdir(parents=True)
            (old_dir / "SKILL.md").write_text("---\nname: csg-workflow\n---\n", encoding="utf-8")

            issues = validate_package.validate(tmp_root)

        self.assertTrue(any("old nested entry still exists" in issue for issue in issues))

    def test_simulated_clone_install(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill_dir = Path(tmp) / "csg-workflow"
            skill_dir.mkdir()
            _copy_skill_tree(ROOT, skill_dir)

            self.assertTrue((skill_dir / "SKILL.md").is_file())
            self.assertFalse((skill_dir / "skills/csg-workflow/SKILL.md").exists())


class ApplyRuleBlockTest(unittest.TestCase):
    def test_preview_does_not_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "AGENTS.md"
            template = ROOT / "assets/templates/AGENTS.md.block"
            target.write_text("# Existing\n\nKeep this.\n", encoding="utf-8")

            result = apply_rule_block.apply_rule_block(target, template)

            self.assertEqual("append", result.action)
            self.assertTrue(result.changed)
            self.assertFalse(result.written)
            self.assertEqual("# Existing\n\nKeep this.\n", target.read_text(encoding="utf-8"))

    def test_write_replaces_only_marked_block(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "AGENTS.md"
            template = ROOT / "assets/templates/AGENTS.md.block"
            fixture = ROOT / "tests/fixtures/rules/existing_agents.md"
            shutil.copy(fixture, target)

            result = apply_rule_block.apply_rule_block(target, template, write=True)
            content = target.read_text(encoding="utf-8")

            self.assertEqual("replace", result.action)
            self.assertTrue(result.written)
            self.assertIn("Keep this existing Codex rule.", content)
            self.assertIn("Keep this trailing rule.", content)
            self.assertNotIn("old block", content)
            self.assertEqual(1, content.count(apply_rule_block.BEGIN))
            self.assertEqual(1, content.count(apply_rule_block.END))

    def test_missing_file_requires_explicit_creation(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "AGENTS.md"
            template = ROOT / "assets/templates/AGENTS.md.block"

            result = apply_rule_block.apply_rule_block(target, template)

            self.assertEqual("missing", result.action)
            self.assertFalse(result.changed)
            self.assertFalse(target.exists())

    def test_broken_marker_pair_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "AGENTS.md"
            template = ROOT / "assets/templates/AGENTS.md.block"
            target.write_text("# Existing\n\n<!-- BEGIN CSG-WORKFLOW RULES -->\n", encoding="utf-8")

            with self.assertRaises(apply_rule_block.RuleBlockError):
                apply_rule_block.apply_rule_block(target, template, write=True)

    def test_reversed_marker_pair_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "AGENTS.md"
            template = ROOT / "assets/templates/AGENTS.md.block"
            target.write_text(
                "# Existing\n\n<!-- END CSG-WORKFLOW RULES -->\nold\n<!-- BEGIN CSG-WORKFLOW RULES -->\n",
                encoding="utf-8",
            )

            with self.assertRaises(apply_rule_block.RuleBlockError):
                apply_rule_block.apply_rule_block(target, template, write=True)


class CheckDependenciesTest(unittest.TestCase):
    def _make_plugins_json(self, home: Path, data: dict) -> Path:
        plugins_dir = home / ".claude" / "plugins"
        plugins_dir.mkdir(parents=True)
        path = plugins_dir / "installed_plugins.json"
        path.write_text(check_deps.json.dumps(data), encoding="utf-8")
        return path

    def _make_gstack(self, home: Path) -> None:
        skill_dir = home / ".claude" / "skills" / "gstack"
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text("# Gstack\n", encoding="utf-8")

    def test_all_installed(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            self._make_plugins_json(home, {"plugins": {
                "compound-engineering@compound-engineering-plugin": [{"version": "3.0.1"}],
                "superpowers@claude-plugins-official": [{"version": "5.1.0"}],
            }})
            self._make_gstack(home)

            results = check_deps.check_dependencies(home)

        self.assertEqual("installed", results["compound"]["status"])
        self.assertEqual("installed", results["superpowers"]["status"])
        self.assertEqual("installed", results["gstack"]["status"])

    def test_all_installed_exit_code_0(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            self._make_plugins_json(home, {"plugins": {
                "compound-engineering@compound-engineering-plugin": [{"version": "3.0.1"}],
                "superpowers@claude-plugins-official": [{"version": "5.1.0"}],
            }})
            self._make_gstack(home)

            code = check_deps.main(["--home", str(home)])

        self.assertEqual(0, code)

    def test_nothing_installed(self):
        with tempfile.TemporaryDirectory() as tmp:
            results = check_deps.check_dependencies(Path(tmp))

        self.assertEqual("missing", results["compound"]["status"])
        self.assertEqual("missing", results["superpowers"]["status"])
        self.assertEqual("missing", results["gstack"]["status"])

    def test_nothing_installed_exit_code_1(self):
        with tempfile.TemporaryDirectory() as tmp:
            code = check_deps.main(["--home", str(tmp)])

        self.assertEqual(1, code)

    def test_partial_install_only_compound(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            self._make_plugins_json(home, {"plugins": {
                "compound-engineering@compound-engineering-plugin": [{"version": "3.0.1"}],
            }})

            results = check_deps.check_dependencies(home)

        self.assertEqual("installed", results["compound"]["status"])
        self.assertEqual("missing", results["superpowers"]["status"])
        self.assertEqual("missing", results["gstack"]["status"])

    def test_plugins_json_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            results = check_deps.check_dependencies(Path(tmp))

        self.assertEqual("missing", results["compound"]["status"])
        self.assertEqual("missing", results["superpowers"]["status"])

    def test_plugins_json_malformed(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            plugins_dir = home / ".claude" / "plugins"
            plugins_dir.mkdir(parents=True)
            (plugins_dir / "installed_plugins.json").write_text("not valid json {{{", encoding="utf-8")

            with self.assertRaises(ValueError):
                check_deps.check_dependencies(home)

    def test_plugins_json_malformed_exit_code_2(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            plugins_dir = home / ".claude" / "plugins"
            plugins_dir.mkdir(parents=True)
            (plugins_dir / "installed_plugins.json").write_text("not valid json {{{", encoding="utf-8")

            code = check_deps.main(["--home", str(home)])

        self.assertEqual(2, code)

    def test_gstack_dir_without_skill_md(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            (home / ".claude" / "skills" / "gstack").mkdir(parents=True)

            results = check_deps.check_dependencies(home)

        self.assertEqual("missing", results["gstack"]["status"])

    def test_empty_home_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            results = check_deps.check_dependencies(Path(tmp))
            code = check_deps.main(["--home", str(tmp)])

        for name in ("compound", "superpowers", "gstack"):
            self.assertEqual("missing", results[name]["status"])
        self.assertEqual(1, code)

    def test_version_values_are_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            self._make_plugins_json(home, {"plugins": {
                "compound-engineering@compound-engineering-plugin": [{"version": "3.0.1"}],
                "superpowers@claude-plugins-official": [{"version": "5.1.0"}],
            }})
            self._make_gstack(home)

            results = check_deps.check_dependencies(home)

        self.assertEqual("3.0.1", results["compound"]["version"])
        self.assertEqual("5.1.0", results["superpowers"]["version"])

    def test_plugins_json_unicode_decode_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            plugins_dir = home / ".claude" / "plugins"
            plugins_dir.mkdir(parents=True)
            (plugins_dir / "installed_plugins.json").write_bytes(b"\x80\x81\x82\x83")

            with self.assertRaises(ValueError):
                check_deps.check_dependencies(home)

    def test_plugins_key_not_a_dict(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            self._make_plugins_json(home, {"plugins": "not a dict"})

            results = check_deps.check_dependencies(home)

        self.assertEqual("missing", results["compound"]["status"])
        self.assertEqual("missing", results["superpowers"]["status"])

    def test_plugin_entry_not_a_list(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            self._make_plugins_json(home, {"plugins": {
                "compound-engineering@compound-engineering-plugin": "not a list",
            }})

            results = check_deps.check_dependencies(home)

        self.assertEqual("missing", results["compound"]["status"])

    def test_plugin_entry_empty_list(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            self._make_plugins_json(home, {"plugins": {
                "compound-engineering@compound-engineering-plugin": [],
            }})

            results = check_deps.check_dependencies(home)

        self.assertEqual("missing", results["compound"]["status"])

    def test_plugin_entry_non_dict_element(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            self._make_plugins_json(home, {"plugins": {
                "compound-engineering@compound-engineering-plugin": [42],
            }})

            results = check_deps.check_dependencies(home)

        self.assertEqual("missing", results["compound"]["status"])

    def test_plugins_json_permission_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            plugins_dir = home / ".claude" / "plugins"
            plugins_dir.mkdir(parents=True)
            path = plugins_dir / "installed_plugins.json"
            path.write_text("{}", encoding="utf-8")
            path.chmod(0o000)

            with self.assertRaises(ValueError):
                check_deps.check_dependencies(home)

            path.chmod(0o644)

    def test_plugin_entry_missing_version_key(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            self._make_plugins_json(home, {"plugins": {
                "compound-engineering@compound-engineering-plugin": [{"other": "data"}],
            }})

            results = check_deps.check_dependencies(home)

        self.assertEqual("installed", results["compound"]["status"])
        self.assertEqual("unknown", results["compound"]["version"])

    def test_human_readable_output_all_installed(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            self._make_plugins_json(home, {"plugins": {
                "compound-engineering@compound-engineering-plugin": [{"version": "3.0.1"}],
                "superpowers@claude-plugins-official": [{"version": "5.1.0"}],
            }})
            self._make_gstack(home)

            import io
            from contextlib import redirect_stdout
            buf = io.StringIO()
            with redirect_stdout(buf):
                check_deps.main(["--home", str(home)])

            output = buf.getvalue()

        self.assertIn("compound: installed (v3.0.1)", output)
        self.assertIn("superpowers: installed (v5.1.0)", output)
        self.assertIn("gstack: installed", output)

    def test_human_readable_output_missing_plugins(self):
        with tempfile.TemporaryDirectory() as tmp:
            import io
            from contextlib import redirect_stdout
            buf = io.StringIO()
            with redirect_stdout(buf):
                check_deps.main(["--home", str(tmp)])

            output = buf.getvalue()

        self.assertIn("compound: missing", output)
        self.assertIn("superpowers: missing", output)
        self.assertIn("gstack: missing", output)

    def test_json_output_is_valid(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            self._make_plugins_json(home, {"plugins": {
                "compound-engineering@compound-engineering-plugin": [{"version": "3.0.1"}],
            }})

            import io
            from contextlib import redirect_stdout
            buf = io.StringIO()
            with redirect_stdout(buf):
                check_deps.main(["--home", str(home), "--json"])

            parsed = check_deps.json.loads(buf.getvalue())

        self.assertEqual("installed", parsed["compound"]["status"])
        self.assertEqual("missing", parsed["superpowers"]["status"])
        self.assertEqual("missing", parsed["gstack"]["status"])


class NavigatorTest(unittest.TestCase):
    """Tests for the Skill GPS Navigator Gate 1."""

    def test_navigator_files_exist(self):
        for name in ("lifecycle.md", "skill-catalog.md", "router-rules.md",
                      "next-step-card.md", "workspace-state.md"):
            path = ROOT / "references/navigator" / name
            self.assertTrue(path.is_file(), f"missing navigator file: {name}")

    def test_card_template_exists(self):
        path = ROOT / "assets/templates/cards/next-step.md"
        self.assertTrue(path.is_file(), "missing card template")

    def test_lifecycle_enum_is_complete(self):
        lifecycle = (ROOT / "references/navigator/lifecycle.md").read_text(encoding="utf-8")
        stages = ["bootstrap", "idea", "requirements", "plan", "work",
                   "review", "qa", "delivery", "learning"]
        for stage in stages:
            self.assertIn(stage, lifecycle, f"missing stage: {stage}")

    def test_recovery_is_mode_not_stage(self):
        lifecycle = (ROOT / "references/navigator/lifecycle.md").read_text(encoding="utf-8")
        self.assertIn("recovery", lifecycle)
        self.assertIn("cross-cutting", lifecycle)
        # Line 19 says: "recovery is **not** a project stage"
        self.assertTrue(
            "not" in lifecycle and "project stage" in lifecycle,
            "lifecycle.md must state that recovery is not a project stage",
        )

    def test_skill_catalog_has_stable_aliases(self):
        catalog = (ROOT / "references/navigator/skill-catalog.md").read_text(encoding="utf-8")
        aliases = [
            "setup-state", "resume-or-clear", "requirements-discovery",
            "plan-prep", "implementation", "code-review", "qa",
            "delivery", "post-release-check", "learning-capture",
        ]
        for alias in aliases:
            self.assertIn(alias, catalog, f"missing alias: {alias}")

    def test_skill_catalog_has_resolution_order(self):
        catalog = (ROOT / "references/navigator/skill-catalog.md").read_text(encoding="utf-8")
        self.assertIn("Resolution Order", catalog)
        self.assertIn("Stable alias", catalog)
        self.assertIn("Manual fallback", catalog)

    def test_skill_catalog_has_availability_boundaries(self):
        catalog = (ROOT / "references/navigator/skill-catalog.md").read_text(encoding="utf-8")
        self.assertIn("Availability Discovery Boundaries", catalog)
        self.assertIn("Not Allowed", catalog)
        self.assertIn("Auto-run", catalog)

    def test_router_rules_require_one_default(self):
        rules = (ROOT / "references/navigator/router-rules.md").read_text(encoding="utf-8")
        self.assertIn("Exactly One Default", rules)
        self.assertIn("Tie-Break", rules)
        self.assertIn("earliest unmet", rules)

    def test_router_rules_have_prompt_injection_guard(self):
        rules = (ROOT / "references/navigator/router-rules.md").read_text(encoding="utf-8")
        self.assertIn("Prompt Injection Guard", rules)
        self.assertIn("lifecycle order", rules)
        self.assertIn("safety boundaries", rules)

    def test_next_step_card_canonical_examples_parseable(self):
        cards_file = (ROOT / "references/navigator/next-step-card.md").read_text(encoding="utf-8")
        cards = validate_package.parse_card_blocks(cards_file)
        self.assertGreaterEqual(len(cards), 9, "expected at least 9 canonical card examples")

    def test_all_lifecycle_stages_have_cards(self):
        cards_file = (ROOT / "references/navigator/next-step-card.md").read_text(encoding="utf-8")
        cards = validate_package.parse_card_blocks(cards_file)
        stages_found = set()
        for card in cards:
            cs = card.get("current_stage")
            if isinstance(cs, str) and cs in validate_package.LIFECYCLE_STAGES:
                stages_found.add(cs)
        for stage in validate_package.LIFECYCLE_STAGES:
            self.assertIn(stage, stages_found, f"no card for stage: {stage}")

    def test_card_ids_are_unique(self):
        cards_file = (ROOT / "references/navigator/next-step-card.md").read_text(encoding="utf-8")
        cards = validate_package.parse_card_blocks(cards_file)
        ids = [str(card.get("id", "")) for card in cards]
        self.assertEqual(len(ids), len(set(ids)), f"duplicate card IDs: {ids}")

    def test_cards_have_required_fields(self):
        cards_file = (ROOT / "references/navigator/next-step-card.md").read_text(encoding="utf-8")
        cards = validate_package.parse_card_blocks(cards_file)
        for card in cards:
            card_id = str(card.get("id", "unknown"))
            for field in validate_package.REQUIRED_CARD_FIELDS:
                self.assertIn(field, card, f"card '{card_id}' missing field: {field}")

    def test_card_stages_are_valid(self):
        cards_file = (ROOT / "references/navigator/next-step-card.md").read_text(encoding="utf-8")
        cards = validate_package.parse_card_blocks(cards_file)
        for card in cards:
            card_id = str(card.get("id", "unknown"))
            for field in ("current_stage", "target_stage_after_completion"):
                val = str(card.get(field, ""))
                self.assertIn(val, validate_package.LIFECYCLE_STAGES,
                              f"card '{card_id}' has invalid {field}: {val}")

    def test_card_confidence_is_valid(self):
        cards_file = (ROOT / "references/navigator/next-step-card.md").read_text(encoding="utf-8")
        cards = validate_package.parse_card_blocks(cards_file)
        for card in cards:
            card_id = str(card.get("id", "unknown"))
            conf = str(card.get("confidence", ""))
            self.assertIn(conf, validate_package.CONFIDENCE_LEVELS,
                          f"card '{card_id}' has invalid confidence: {conf}")

    def test_card_source_family_is_valid(self):
        cards_file = (ROOT / "references/navigator/next-step-card.md").read_text(encoding="utf-8")
        cards = validate_package.parse_card_blocks(cards_file)
        for card in cards:
            card_id = str(card.get("id", "unknown"))
            fam = str(card.get("source_family", ""))
            self.assertIn(fam, validate_package.SOURCE_FAMILIES,
                          f"card '{card_id}' has invalid source_family: {fam}")

    def test_card_expected_output_non_empty(self):
        cards_file = (ROOT / "references/navigator/next-step-card.md").read_text(encoding="utf-8")
        cards = validate_package.parse_card_blocks(cards_file)
        for card in cards:
            card_id = str(card.get("id", "unknown"))
            eo = card.get("expected_output")
            self.assertIsInstance(eo, list, f"card '{card_id}' expected_output not a list")
            self.assertGreater(len(eo), 0, f"card '{card_id}' expected_output is empty")

    def test_card_fallback_non_empty(self):
        cards_file = (ROOT / "references/navigator/next-step-card.md").read_text(encoding="utf-8")
        cards = validate_package.parse_card_blocks(cards_file)
        for card in cards:
            card_id = str(card.get("id", "unknown"))
            fb = card.get("fallback_if_missing")
            self.assertIsInstance(fb, list, f"card '{card_id}' fallback_if_missing not a list")
            self.assertGreater(len(fb), 0, f"card '{card_id}' fallback_if_missing is empty")

    def test_card_rendering_has_markdown(self):
        cards_file = (ROOT / "references/navigator/next-step-card.md").read_text(encoding="utf-8")
        cards = validate_package.parse_card_blocks(cards_file)
        for card in cards:
            card_id = str(card.get("id", "unknown"))
            rendering = card.get("rendering")
            self.assertIsInstance(rendering, list, f"card '{card_id}' rendering not a nested map")
            has_markdown = any(
                isinstance(item, dict) and "markdown" in item
                for item in (rendering or [])
            )
            self.assertTrue(has_markdown, f"card '{card_id}' rendering missing 'markdown'")

    def test_recovery_cards_preserve_stage(self):
        cards_file = (ROOT / "references/navigator/next-step-card.md").read_text(encoding="utf-8")
        cards = validate_package.parse_card_blocks(cards_file)
        recovery_cards = [c for c in cards if str(c.get("id", "")).startswith("recovery-")]
        self.assertGreaterEqual(len(recovery_cards), 4, "expected at least 4 recovery cards")
        for card in recovery_cards:
            card_id = str(card.get("id", "unknown"))
            cs = str(card.get("current_stage", ""))
            ts = str(card.get("target_stage_after_completion", ""))
            self.assertEqual(cs, ts,
                             f"recovery card '{card_id}' changes stage: {cs} -> {ts}")

    def test_workspace_state_has_confirmation_semantics(self):
        ws = (ROOT / "references/navigator/workspace-state.md").read_text(encoding="utf-8")
        self.assertIn("Confirmation Semantics", ws)
        self.assertIn("does", ws)
        self.assertIn("advance", ws)
        self.assertIn("current_stage", ws)
        self.assertIn("recovery_needed", ws)
        self.assertIn("Old-State Migration", ws)

    def test_workspace_state_has_card_status_enum(self):
        ws = (ROOT / "references/navigator/workspace-state.md").read_text(encoding="utf-8")
        for status in validate_package.CARD_STATUSES:
            self.assertIn(status, ws, f"missing card status: {status}")

    def test_skill_md_mentions_navigator_references(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Skill GPS", skill)
        self.assertIn("next-step card", skill)
        self.assertIn("references/navigator/lifecycle.md", skill)
        self.assertIn("references/navigator/next-step-card.md", skill)
        self.assertIn("routing context", skill)
        self.assertIn("safety boundaries", skill)

    def test_compatibility_wrappers_delegate(self):
        for rel in ("references/stage-router.md", "references/skill-selection.md",
                     "references/handoff-state.md"):
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn("Compatibility Wrapper", text, f"{rel} missing wrapper marker")
            self.assertIn("navigator/", text, f"{rel} missing delegation to navigator")

    def test_wrappers_no_split_brain(self):
        for rel in ("references/stage-router.md", "references/skill-selection.md",
                     "references/handoff-state.md"):
            text = (ROOT / rel).read_text(encoding="utf-8")
            for pattern, label in validate_package.WRAPPER_SPLIT_BRAIN_PATTERNS:
                self.assertNotRegex(text, pattern,
                                    f"{rel}: split brain — contains {label}")

    def test_pressure_scenarios_include_gate1_scenarios(self):
        scenarios = (ROOT / "tests/pressure-scenarios/csg-workflow-v1.md").read_text(encoding="utf-8")
        gate1_scenarios = {
            "AE16": ("Vague Idea to Brainstorm Card", "recommended_role: requirements-discovery"),
            "AE17": ("Completed Brainstorm to Plan Card", "recommended_role: plan-prep"),
            "AE18": ("Missing Skill Fallback Card", "fallback_if_missing"),
            "AE19": ("Post-Compact Card Recovery", "active card"),
            "AE20": ("Old-State Migration Card", "old state shape"),
            "AE21": ("Prompt Injection Route Bypass", "earliest unmet"),
        }
        for ae_num, (title, keyword) in gate1_scenarios.items():
            section = scenario_section(scenarios, f"{ae_num}: {title}")
            self.assertIn(keyword, section, f"{ae_num} missing expected content")

    def test_skill_selection_wrapper_delegates(self):
        sel = (ROOT / "references/skill-selection.md").read_text(encoding="utf-8")
        self.assertIn("Compatibility Wrapper", sel)
        self.assertIn("navigator/skill-catalog.md", sel)
        self.assertNotIn("Category Choices", sel)



class ParseCardBlocksTest(unittest.TestCase):
    """Unit tests for the card block parser in isolation."""

    def test_empty_input(self):
        cards = validate_package.parse_card_blocks("")
        self.assertEqual([], cards)

    def test_no_blocks(self):
        cards = validate_package.parse_card_blocks("# Title\nSome prose\n")
        self.assertEqual([], cards)

    def test_simple_card(self):
        text = "```next-step-card\nid: test-1\ncurrent_stage: idea\n```\n"
        cards = validate_package.parse_card_blocks(text)
        self.assertEqual(1, len(cards))
        self.assertEqual("test-1", cards[0]["id"])
        self.assertEqual("idea", cards[0]["current_stage"])

    def test_unclosed_block_kept(self):
        text = "```next-step-card\nid: unclosed\ncurrent_stage: idea\n"
        cards = validate_package.parse_card_blocks(text)
        self.assertEqual(1, len(cards))
        self.assertEqual("unclosed", cards[0]["id"])

    def test_list_field(self):
        text = "```next-step-card\nid: test-2\nexpected_output:\n  - item one\n  - item two\n```\n"
        cards = validate_package.parse_card_blocks(text)
        self.assertEqual(["item one", "item two"], cards[0]["expected_output"])

    def test_nested_map_field(self):
        text = "```next-step-card\nid: test-3\nrendering:\n  markdown: required\n  claude_question: required\n```\n"
        cards = validate_package.parse_card_blocks(text)
        rendering = cards[0]["rendering"]
        self.assertIsInstance(rendering, list)
        found = {k: v for item in rendering if isinstance(item, dict) for k, v in item.items()}
        self.assertEqual("required", found.get("markdown"))

    def test_multiple_blocks(self):
        text = "```next-step-card\nid: a\n```\n```next-step-card\nid: b\n```\n"
        cards = validate_package.parse_card_blocks(text)
        self.assertEqual(2, len(cards))
        self.assertEqual("a", cards[0]["id"])
        self.assertEqual("b", cards[1]["id"])

    def test_empty_value_becomes_list(self):
        text = "```next-step-card\nid: test-4\nwhy:\n```\n"
        cards = validate_package.parse_card_blocks(text)
        self.assertIsInstance(cards[0]["why"], list)
        self.assertEqual([], cards[0]["why"])

    def test_value_with_colon(self):
        text = "```next-step-card\nid: test-5\nwhy: Because: it is needed\n```\n"
        cards = validate_package.parse_card_blocks(text)
        self.assertEqual("Because: it is needed", cards[0]["why"])

    def test_empty_block_not_collected(self):
        text = "```next-step-card\n\n\n```\n"
        cards = validate_package.parse_card_blocks(text)
        self.assertEqual([], cards, "Empty card block should not produce a card")

    def test_list_inside_nested_map_ignored(self):
        text = "```next-step-card\nid: test-6\nrendering:\n  markdown: required\n  - stray list item\n```\n"
        cards = validate_package.parse_card_blocks(text)
        self.assertEqual(1, len(cards))
        rendering = cards[0]["rendering"]
        self.assertIsInstance(rendering, list)
        # The stray list item is silently ignored (not supported inside nested maps)
        found = {k: v for item in rendering if isinstance(item, dict) for k, v in item.items()}
        self.assertEqual("required", found.get("markdown"))


class NegativePathValidationTest(unittest.TestCase):
    """Negative-path tests for navigator validation."""

    def test_missing_navigator_file_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            _copy_skill_tree(ROOT, tmp_root)
            (tmp_root / "references/navigator/lifecycle.md").unlink()
            issues = validate_package.validate(tmp_root)
        self.assertTrue(any("references/navigator/lifecycle.md: missing required file" in i for i in issues))

    def test_missing_card_field_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            _copy_skill_tree(ROOT, tmp_root)
            cards_file = tmp_root / "references/navigator/next-step-card.md"
            cards_text = cards_file.read_text(encoding="utf-8")
            cards_text = cards_text.replace("why: The user has a vague project idea but no accepted scope.", "removed_field: oops")
            cards_file.write_text(cards_text, encoding="utf-8")
            issues = validate_package.validate(tmp_root)
        self.assertTrue(any("missing_field" in i and "why" in i for i in issues))

    def test_invalid_stage_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            _copy_skill_tree(ROOT, tmp_root)
            cards_file = tmp_root / "references/navigator/next-step-card.md"
            cards_text = cards_file.read_text(encoding="utf-8")
            # Replace the id of idea-to-brainstorm to inject an invalid stage
            cards_text = cards_text.replace(
                "id: idea-to-brainstorm\ncurrent_stage: idea",
                "id: idea-to-brainstorm\ncurrent_stage: dreaming",
            )
            cards_file.write_text(cards_text, encoding="utf-8")
            issues = validate_package.validate(tmp_root)
        self.assertTrue(any("invalid_stage" in i for i in issues),
                        f"Expected invalid_stage issue. Got: {[i for i in issues if 'stage' in i]}")

    def test_wrapper_split_brain_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            _copy_skill_tree(ROOT, tmp_root)
            wrapper = tmp_root / "references/stage-router.md"
            wrapper.write_text(
                "# Stage Router\n\n| Stage | Signals | Default Skill |\n|---|---|---|\n| Idea | vague | ce-ideate |\n",
                encoding="utf-8",
            )
            issues = validate_package.validate(tmp_root)
        self.assertTrue(any("wrapper_split_brain" in i for i in issues))

    def test_wrapper_missing_delegation_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            _copy_skill_tree(ROOT, tmp_root)
            wrapper = tmp_root / "references/stage-router.md"
            wrapper.write_text("# Stage Router\n\nSome content without navigator delegation.\n", encoding="utf-8")
            issues = validate_package.validate(tmp_root)
        self.assertTrue(any("wrapper_split_brain" in i for i in issues))

    def test_empty_routing_trace_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            _copy_skill_tree(ROOT, tmp_root)
            cards_file = tmp_root / "references/navigator/next-step-card.md"
            cards_text = cards_file.read_text(encoding="utf-8")
            cards_text = cards_text.replace(
                "routing_trace:\n  - no accepted requirements found\n  - earliest unmet lifecycle stage is idea\n  - default role for idea is requirements-discovery",
                "routing_trace:\n  - lone-item",
            )
            cards_file.write_text(cards_text, encoding="utf-8")
            issues = validate_package.validate(tmp_root)
        self.assertTrue(any("routing_trace" in i and "fewer than 2" in i for i in issues))


if __name__ == "__main__":
    unittest.main()
