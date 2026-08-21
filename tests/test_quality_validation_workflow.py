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

    def test_persisted_report_contract_binds_the_validated_candidate(self):
        required = {
            "zh": (
                "权威任务文档同级目录",
                "quality-validation-report.md",
                "仅在 `需要/强制`",
                "当前分支",
                "HEAD commit",
                "被验收路径",
                "diff SHA-256",
                "未跟踪文件",
            ),
            "en": (
                "same directory as the authoritative task document",
                "quality-validation-report.md",
                "only when validation is `required/mandatory`",
                "current branch",
                "HEAD commit",
                "validated paths",
                "diff SHA-256",
                "untracked files",
            ),
        }
        for language, root in LANGUAGES.items():
            content = read(root / "skills/company-quality-validation/SKILL.md")
            for phrase in required[language]:
                with self.subTest(language=language, phrase=phrase):
                    self.assertIn(phrase, content)

    def test_report_template_contains_transparency_identity_and_guardrails(self):
        required = {
            "zh": (
                "工作流层",
                "透明度模式",
                "Superpowers 叠加",
                "实际调用",
                "专家/插件能力",
                "未调用但采用视角",
                "被验收路径",
                "diff SHA-256",
                "未跟踪文件路径与 SHA-256",
                "安全、权限、数据完整性、金额或指标公式、迁移、回滚或恢复风险不得有条件通过",
                "接受人",
                "接受时间",
                "接受范围",
                "到期条件",
            ),
            "en": (
                "Workflow layer",
                "Trace mode",
                "Superpowers layer",
                "Actual calls",
                "Expert/plugin capabilities",
                "Not called, lens only",
                "Validated paths",
                "Diff SHA-256",
                "Untracked file paths and SHA-256",
                "Security, permission, data-integrity, money or metric-formula, migration, rollback, or recovery risks cannot receive conditional pass",
                "Accepted by",
                "Accepted at",
                "Accepted scope",
                "Expiry condition",
            ),
        }
        for language, root in LANGUAGES.items():
            content = read(root / "specs/global/assets/quality-validation-report-template.md")
            for phrase in required[language]:
                with self.subTest(language=language, phrase=phrase):
                    self.assertIn(phrase, content)

    def test_defect_routes_use_canonical_workflow_names(self):
        routes = (
            "company-bugfix-runner",
            "company-feature-requirements",
            "company-feature-design",
            "company-feature-planning",
        )
        for language, root in LANGUAGES.items():
            template = read(root / "specs/global/assets/quality-validation-report-template.md")
            skill = read(root / "skills/company-quality-validation/SKILL.md")
            for route in routes:
                with self.subTest(language=language, route=route):
                    self.assertIn(route, template)
                    self.assertIn(route, skill)

    def test_closeout_consumes_report_state_without_repeating_the_whole_suite(self):
        required = {
            "zh": (
                "重新核对独立质量验收触发矩阵",
                "权威任务文档同级目录",
                "候选指纹",
                "被验收路径发生漂移",
                "返回 `company-quality-validation`",
                "复用新鲜验收证据",
                "不得无差别重跑完整测试集",
                "不得形成递归调用",
            ),
            "en": (
                "recompute the independent quality-validation trigger matrix",
                "same directory as the authoritative task document",
                "candidate fingerprint",
                "validated paths drift",
                "return to `company-quality-validation`",
                "reuse fresh validation evidence",
                "must not indiscriminately rerun the complete test suite",
                "must not create recursive invocation",
            ),
        }
        for language, root in LANGUAGES.items():
            content = read(root / "skills/company-delivery-closeout/SKILL.md")
            for phrase in required[language]:
                with self.subTest(language=language, phrase=phrase):
                    self.assertIn(phrase, content)

    def test_release_and_packaged_verification_are_wired(self):
        package = json.loads(read(ROOT / "package.json"))
        self.assertEqual("0.2.31", package["version"])
        self.assertIn("test_quality_validation_workflow.py", package["scripts"]["verify"])
        for root in LANGUAGES.values():
            manifest = json.loads(read(root / ".codex-plugin/plugin.json"))
            self.assertEqual(package["version"], manifest["version"])
        self.assertIn("test_quality_validation_workflow.py", read(ROOT / "scripts/install.sh"))
        self.assertIn("test_quality_validation_workflow.py", read(ROOT / "scripts/install.ps1"))


if __name__ == "__main__":
    unittest.main()
