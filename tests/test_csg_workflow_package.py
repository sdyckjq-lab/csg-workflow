from __future__ import annotations

import importlib.util
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
    ROOT / "skills/csg-workflow/scripts/validate_package.py",
    "validate_package",
)
apply_rule_block = load_module(
    ROOT / "skills/csg-workflow/scripts/apply_rule_block.py",
    "apply_rule_block",
)
check_deps = load_module(
    ROOT / "skills/csg-workflow/scripts/check_dependencies.py",
    "check_dependencies",
)


class ValidatePackageTest(unittest.TestCase):
    def test_current_package_is_valid(self):
        issues = validate_package.validate(ROOT)
        self.assertEqual([], issues)

    def test_skill_routing_intercept_precedes_v1_guidance(self):
        skill_text = (ROOT / "skills/csg-workflow/SKILL.md").read_text(encoding="utf-8")
        intercept_start = skill_text.index("## 强制路由")
        v1_boundary_start = skill_text.index("## V1 Boundary")
        intercept = skill_text[intercept_start:v1_boundary_start]

        self.assertLess(intercept_start, v1_boundary_start)
        self.assertIn("你只做路由", intercept)
        self.assertIn("Ask the user before invoking or routing into the next Skill", intercept)
        self.assertIn("将 command-args 当作直接任务来回应", intercept)
        self.assertIn("启动调研、设计、实现", intercept)
        self.assertIn("调用 Agent 或其他工具", intercept)

    def test_skill_start_here_is_replaced_by_post_routing_guidance(self):
        skill_text = (ROOT / "skills/csg-workflow/SKILL.md").read_text(encoding="utf-8")

        self.assertNotIn("## Start Here", skill_text)
        self.assertIn("## 路由完成后", skill_text)
        self.assertIn("阶段结束时，更新 `state.md`", skill_text)

    def test_pressure_scenarios_include_command_args_intercept(self):
        scenarios = (ROOT / "tests/pressure-scenarios/csg-workflow-v1.md").read_text(encoding="utf-8")
        ae11_start = scenarios.index("## AE11: Command Args Routing Intercept")
        ae11 = scenarios[ae11_start:]

        self.assertIn("`/csg-workflow 我想加一个功能...如何设计？`", ae11)
        self.assertIn("routing context, not as a direct design task", ae11)
        self.assertIn("reads project rules and `docs/workflow/state.md`", ae11)
        self.assertIn("before any research, design, implementation, or Agent call", ae11)
        self.assertIn("asks before invoking or routing into the next Skill", ae11)

    def test_missing_skill_description_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            target = tmp_root / "skills/csg-workflow"
            target.mkdir(parents=True)
            (target / "SKILL.md").write_text("---\nname: csg-workflow\n---\n\n# Broken\n", encoding="utf-8")

            issues = validate_package.validate(tmp_root)

        self.assertTrue(any("missing description" in issue for issue in issues))

    def test_absolute_local_path_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            shutil.copytree(ROOT / "skills", tmp_root / "skills")
            shutil.copytree(ROOT / "examples", tmp_root / "examples")
            shutil.copytree(ROOT / "tests/pressure-scenarios", tmp_root / "tests/pressure-scenarios")
            shutil.copy(ROOT / "README.md", tmp_root / "README.md")
            shutil.copy(ROOT / "LICENSE", tmp_root / "LICENSE")
            skill_file = tmp_root / "skills/csg-workflow/SKILL.md"
            absolute_path = "/" + "Users/example/project"
            skill_file.write_text(skill_file.read_text(encoding="utf-8") + f"\n{absolute_path}\n", encoding="utf-8")

            issues = validate_package.validate(tmp_root)

        self.assertTrue(any("absolute local path" in issue for issue in issues))

    def test_python_script_absolute_local_path_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            shutil.copytree(ROOT / "skills", tmp_root / "skills")
            shutil.copytree(ROOT / "examples", tmp_root / "examples")
            shutil.copytree(ROOT / "tests/pressure-scenarios", tmp_root / "tests/pressure-scenarios")
            shutil.copy(ROOT / "README.md", tmp_root / "README.md")
            shutil.copy(ROOT / "LICENSE", tmp_root / "LICENSE")
            script_file = tmp_root / "skills/csg-workflow/scripts/apply_rule_block.py"
            absolute_path = "/" + "Users/example/project"
            script_file.write_text(script_file.read_text(encoding="utf-8") + f"\n# {absolute_path}\n", encoding="utf-8")

            issues = validate_package.validate(tmp_root)

        self.assertTrue(any("skills/csg-workflow/scripts/apply_rule_block.py" in issue for issue in issues))
        self.assertTrue(any("absolute local path" in issue for issue in issues))


class ApplyRuleBlockTest(unittest.TestCase):
    def test_preview_does_not_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "AGENTS.md"
            template = ROOT / "skills/csg-workflow/assets/templates/AGENTS.md.block"
            target.write_text("# Existing\n\nKeep this.\n", encoding="utf-8")

            result = apply_rule_block.apply_rule_block(target, template)

            self.assertEqual("append", result.action)
            self.assertTrue(result.changed)
            self.assertFalse(result.written)
            self.assertEqual("# Existing\n\nKeep this.\n", target.read_text(encoding="utf-8"))

    def test_write_replaces_only_marked_block(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "AGENTS.md"
            template = ROOT / "skills/csg-workflow/assets/templates/AGENTS.md.block"
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
            template = ROOT / "skills/csg-workflow/assets/templates/AGENTS.md.block"

            result = apply_rule_block.apply_rule_block(target, template)

            self.assertEqual("missing", result.action)
            self.assertFalse(result.changed)
            self.assertFalse(target.exists())

    def test_broken_marker_pair_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "AGENTS.md"
            template = ROOT / "skills/csg-workflow/assets/templates/AGENTS.md.block"
            target.write_text("# Existing\n\n<!-- BEGIN CSG-WORKFLOW RULES -->\n", encoding="utf-8")

            with self.assertRaises(apply_rule_block.RuleBlockError):
                apply_rule_block.apply_rule_block(target, template, write=True)

    def test_reversed_marker_pair_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "AGENTS.md"
            template = ROOT / "skills/csg-workflow/assets/templates/AGENTS.md.block"
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


if __name__ == "__main__":
    unittest.main()
