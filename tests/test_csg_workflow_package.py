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


class ValidatePackageTest(unittest.TestCase):
    def test_current_package_is_valid(self):
        issues = validate_package.validate(ROOT)
        self.assertEqual([], issues)

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


if __name__ == "__main__":
    unittest.main()
