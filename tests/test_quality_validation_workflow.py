import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = {
    "zh": ROOT / "outputs/company-codex-workflow-v2-zh",
    "en": ROOT / "outputs/company-codex-workflow-v2",
}
STARTERS = {
    "zh": ROOT / "outputs/company-codex-workflow-template-zh",
    "en": ROOT / "outputs/company-codex-workflow-template",
}
ROUTING_SKILLS = (
    "company-workflow-help",
    "company-feature-planning",
    "company-implementation-runner",
    "company-bugfix-runner",
    "company-delivery-closeout",
    "company-workflow-health-check",
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class QualityValidationWorkflowTests(unittest.TestCase):
    def test_bilingual_skill_and_ui_registration(self):
        for language, root in LANGUAGES.items():
            skill_dir = root / "skills/company-quality-validation"
            skill = read(skill_dir / "SKILL.md")
            ui = read(skill_dir / "agents/openai.yaml")
            with self.subTest(language=language):
                self.assertIn("name: company-quality-validation", skill)
                self.assertIn("description: Use when", skill)
                self.assertIn('display_name: "/company-quality-validation"', ui)
                self.assertIn("$company-quality-validation", ui)

    def test_trigger_matrix_distinguishes_skip_required_and_mandatory(self):
        required = {
            "zh": (
                "V0/V1",
                "默认不触发",
                "多任务",
                "跨模块",
                "里程碑",
                "V3",
                "强制触发",
                "hotfix",
            ),
            "en": (
                "V0/V1",
                "not triggered by default",
                "multi-task",
                "cross-module",
                "milestone",
                "V3",
                "mandatory",
                "hotfix",
            ),
        }
        for language, root in LANGUAGES.items():
            content = read(root / "skills/company-quality-validation/SKILL.md")
            for phrase in required[language]:
                with self.subTest(language=language, phrase=phrase):
                    self.assertIn(phrase, content)

    def test_validation_has_bounded_outcomes_and_routes(self):
        required = {
            "zh": ("通过 / 有条件通过 / 阻断", "不得修改生产代码"),
            "en": ("pass / conditional-pass / blocked", "must not modify production code"),
        }
        for language, root in LANGUAGES.items():
            content = read(root / "skills/company-quality-validation/SKILL.md")
            for phrase in required[language]:
                self.assertIn(phrase, content, language)
            self.assertIn("company-bugfix-runner", content, language)
            self.assertIn("company-delivery-closeout", content, language)
            self.assertIn("superpowers:verification-before-completion", content, language)
            self.assertIn("testing-qa", content, language)

    def test_existing_workflows_route_through_quality_validation(self):
        for language, root in LANGUAGES.items():
            self.assertIn("company-quality-validation", read(root / "AGENTS.md"), language)
            self.assertIn("company-quality-validation", read(root / "BUNDLES.md"), language)
            for skill in ROUTING_SKILLS:
                with self.subTest(language=language, skill=skill):
                    self.assertIn(
                        "company-quality-validation",
                        read(root / "skills" / skill / "SKILL.md"),
                    )

    def test_report_template_is_mirrored_and_indexed(self):
        for language, root in LANGUAGES.items():
            plugin = root / "specs/global/assets/quality-validation-report-template.md"
            starter = STARTERS[language] / "specs/global/assets/quality-validation-report-template.md"
            with self.subTest(language=language):
                self.assertEqual(read(plugin), read(starter))
                self.assertIn("quality-validation-report-template.md", read(root / "specs/global/INDEX.md"))
                self.assertIn(
                    "quality-validation-report-template.md",
                    read(STARTERS[language] / "specs/global/INDEX.md"),
                )

    def test_release_and_packaged_verification_are_wired(self):
        package = json.loads(read(ROOT / "package.json"))
        self.assertEqual("0.2.29", package["version"])
        self.assertIn("test_quality_validation_workflow.py", package["scripts"]["verify"])
        for root in LANGUAGES.values():
            manifest = json.loads(read(root / ".codex-plugin/plugin.json"))
            self.assertEqual(package["version"], manifest["version"])
        self.assertIn("test_quality_validation_workflow.py", read(ROOT / "scripts/install.sh"))
        self.assertIn("test_quality_validation_workflow.py", read(ROOT / "scripts/install.ps1"))


if __name__ == "__main__":
    unittest.main()
