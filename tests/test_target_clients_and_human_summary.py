import json
import subprocess
import tempfile
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
TARGET_CLIENT_SKILLS = (
    "company-workflow-help",
    "company-context-index",
    "company-legacy-project-onboarding",
    "company-workflow-health-check",
    "company-expert-routing",
    "company-feature-requirements",
    "company-requirements-prototype",
    "company-feature-design",
    "company-feature-planning",
    "company-implementation-runner",
    "company-bugfix-runner",
    "company-quality-validation",
)
HUMAN_SUMMARY_SKILLS = tuple(
    sorted(path.parent.name for path in LANGUAGES["en"].glob("skills/company-*/SKILL.md"))
)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class TargetClientContractTests(unittest.TestCase):
    def test_project_index_declares_target_client_baseline(self):
        required = {
            "zh": (
                "目标使用终端基线",
                "不是 TCP/HTTP 网络端口",
                "PC Web",
                "移动 Web",
                "未确认的终端默认不支持",
            ),
            "en": (
                "Target Client Baseline",
                "not TCP/HTTP network ports",
                "PC Web",
                "Mobile Web",
                "Unconfirmed clients are unsupported by default",
            ),
        }
        for language, phrases in required.items():
            for root in (LANGUAGES[language], STARTERS[language]):
                content = read(root / "specs/global/INDEX.md")
                for phrase in phrases:
                    with self.subTest(language=language, root=root.name, phrase=phrase):
                        self.assertIn(phrase, content)

        generator = read(ROOT / "scripts/generate_index.py")
        self.assertIn("目标使用终端基线", generator)
        self.assertIn("Target Client Baseline", generator)

    def test_requirements_design_and_tasks_carry_the_same_client_contract(self):
        required = {
            "zh": (
                "目标使用终端与适配边界",
                "未明确列为支持的终端不得自行适配",
                "PC Web",
                "移动 Web",
                "iOS/Android App",
                "桌面客户端",
                "大屏",
                "响应式",
                "触摸",
            ),
            "en": (
                "Target Clients and Adaptation Boundary",
                "Do not adapt clients that are not explicitly supported",
                "PC Web",
                "Mobile Web",
                "iOS/Android App",
                "Desktop client",
                "Large display",
                "responsive",
                "touch",
            ),
        }
        names = ("requirements-template.md", "design-template.md", "tasks-template.md")
        for language, phrases in required.items():
            for name in names:
                plugin = LANGUAGES[language] / "specs/global/assets" / name
                starter = STARTERS[language] / "specs/global/assets" / name
                self.assertEqual(read(plugin), read(starter))
                content = read(plugin)
                for phrase in phrases:
                    with self.subTest(language=language, file=name, phrase=phrase):
                        self.assertIn(phrase, content)

    def test_workflows_enforce_opt_in_mobile_scope(self):
        required = {
            "zh": ("目标使用终端", "不得自行增加移动端适配"),
            "en": ("target clients", "must not add mobile adaptation on its own"),
        }
        for language, root in LANGUAGES.items():
            for skill in TARGET_CLIENT_SKILLS:
                content = read(root / "skills" / skill / "SKILL.md")
                for phrase in required[language]:
                    with self.subTest(language=language, skill=skill, phrase=phrase):
                        self.assertIn(phrase, content)

        zh_prototype = read(
            LANGUAGES["zh"] / "skills/company-requirements-prototype/SKILL.md"
        )
        self.assertNotIn("桌面端和移动端视口", zh_prototype)

    def test_agents_make_client_scope_a_change_gate(self):
        required = {
            "zh": ("目标使用终端契约", "未确认移动端时", "范围变化熔断"),
            "en": ("Target Client Contract", "When mobile is unconfirmed", "scope-change circuit breaker"),
        }
        for language, phrases in required.items():
            for root in (LANGUAGES[language], STARTERS[language]):
                content = read(root / "AGENTS.md")
                for phrase in phrases:
                    with self.subTest(language=language, root=root.name, phrase=phrase):
                        self.assertIn(phrase, content)

    def test_update_templates_refreshes_managed_rules_without_overwriting_index(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            agents = project / "AGENTS.md"
            agents.write_text(
                "# Local rule\n\n"
                "<!-- codex-workflow-kit:company:start -->\n"
                "old managed rule\n"
                "<!-- codex-workflow-kit:company:end -->\n",
                encoding="utf-8",
            )
            index = project / "specs/global/INDEX.md"
            index.parent.mkdir(parents=True)
            index.write_text("# Confirmed project index\n", encoding="utf-8")

            subprocess.run(
                [
                    "bash",
                    str(ROOT / "scripts/install.sh"),
                    "update-templates",
                    str(project),
                    "--lang",
                    "zh",
                ],
                check=True,
                cwd=ROOT,
                capture_output=True,
                text=True,
            )

            self.assertTrue((project / "specs/global/assets/human-output-standard.md").is_file())
            self.assertTrue((project / "specs/global/assets/execution-record-template.md").is_file())
            updated_agents = read(agents)
            self.assertIn("# Local rule", updated_agents)
            self.assertNotIn("old managed rule", updated_agents)
            self.assertIn("目标使用终端契约", updated_agents)
            self.assertIn("人类优先总结", updated_agents)
            self.assertEqual("# Confirmed project index\n", read(index))
            generated = read(project / "specs/global/INDEX.generated.md")
            self.assertIn("目标使用终端基线", generated)
            self.assertIn("桌面客户端", generated)
            self.assertIn("大屏", generated)


class HumanFirstSummaryTests(unittest.TestCase):
    def test_every_workflow_loads_shared_policy(self):
        for root in LANGUAGES.values():
            for skill in HUMAN_SUMMARY_SKILLS:
                content = read(root / "skills" / skill / "SKILL.md")
                with self.subTest(root=root.name, skill=skill):
                    self.assertIn("../../specs/global/assets/human-output-standard.md", content)
                    self.assertTrue("回复契约门禁" in content or "Response Contract Gate" in content)

    def test_agents_scope_audit_fields_to_internal_records(self):
        for language in LANGUAGES:
            for root in (LANGUAGES[language], STARTERS[language]):
                content = read(root / "AGENTS.md")
                with self.subTest(root=root.name):
                    self.assertIn("human-output-standard.md", content)
                    self.assertIn("内部执行记录" if language == "zh" else "internal execution records", content)
                    self.assertNotIn("不得删除、改名或调换四个标题", content)
                    self.assertNotIn("must not remove, rename, or reorder the four headings", content)

    def test_release_and_packaged_verification_include_new_contract(self):
        package = json.loads(read(ROOT / "package.json"))
        self.assertEqual("0.2.37", package["version"])
        self.assertIn("test_legacy_project_migration.py", package["scripts"]["verify"])
        self.assertIn("test_target_clients_and_human_summary.py", package["scripts"]["verify"])
        self.assertIn("test_target_clients_and_human_summary.py", read(ROOT / "scripts/install.sh"))
        powershell = read(ROOT / "scripts/install.ps1")
        self.assertIn("test_target_clients_and_human_summary.py", powershell)
        self.assertIn("test_legacy_project_migration.py", powershell)
        self.assertIn("Quality validation workflow regression tests failed", powershell)
        self.assertIn("Target client and human summary regression tests failed", powershell)
        for root in LANGUAGES.values():
            manifest = json.loads(read(root / ".codex-plugin/plugin.json"))
            self.assertEqual(package["version"], manifest["version"])


if __name__ == "__main__":
    unittest.main()
