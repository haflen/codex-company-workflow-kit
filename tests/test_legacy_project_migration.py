import hashlib
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / "scripts/install.sh"
NODE_WRAPPER = ROOT / "bin/codex-company-workflow.js"
ZH_STARTER = ROOT / "outputs/company-codex-workflow-template-zh/AGENTS.md"
FULL_PLUGINS = {
    "zh": ROOT / "outputs/company-codex-workflow-v2-zh/AGENTS.md",
    "en": ROOT / "outputs/company-codex-workflow-v2/AGENTS.md",
}
MARKER_BEGIN = "<!-- codex-workflow-kit:company:start -->"
MARKER_END = "<!-- codex-workflow-kit:company:end -->"


def run_installer(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["bash", str(INSTALLER), *args],
        check=True,
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


def legacy_agents(language: str = "zh") -> str:
    if language == "zh":
        return (
            "# 公司 Codex 工作流\n\n"
            "## 上下文优先\n\n旧版上下文规则。\n\n"
            "## 阶段边界\n\n旧版阶段规则。\n\n"
            "## Superpowers\n\n旧版能力规则。\n"
        )
    return (
        "# Company Codex Workflow\n\n"
        "## Context First\n\nLegacy context rule.\n\n"
        "## Phase Boundaries\n\nLegacy phase rule.\n\n"
        "## Superpowers\n\nLegacy capability rule.\n"
    )


class LegacyProjectMigrationTests(unittest.TestCase):
    def test_update_templates_stages_agents_candidate_for_unmarked_legacy_file(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            original = legacy_agents()
            agents = project / "AGENTS.md"
            agents.write_text(original, encoding="utf-8")

            result = run_installer("update-templates", str(project), "--lang", "zh")

            self.assertEqual(original, agents.read_text(encoding="utf-8"))
            candidate = project / "AGENTS.generated.md"
            self.assertTrue(candidate.is_file())
            candidate_text = candidate.read_text(encoding="utf-8")
            self.assertEqual(1, candidate_text.count(MARKER_BEGIN))
            self.assertIn("人类优先总结", candidate_text)
            self.assertIn("migrate-project", result.stdout)

    def test_migrate_project_backs_up_and_replaces_unmarked_legacy_rules(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            original = ZH_STARTER.read_text(encoding="utf-8")
            agents = project / "AGENTS.md"
            agents.write_text(original, encoding="utf-8")
            index = project / "specs/global/INDEX.md"
            index.parent.mkdir(parents=True)
            index.write_text("# Confirmed project index\n", encoding="utf-8")
            templates = project / "specs/global/assets"
            templates.mkdir()
            (templates / "local-template.md").write_text("local\n", encoding="utf-8")
            source_file = project / "src/service.bin"
            source_file.parent.mkdir()
            source_file.write_bytes(b"\x00business-source\xff")
            source_hash = hashlib.sha256(source_file.read_bytes()).hexdigest()

            run_installer("migrate-project", str(project), "--lang", "zh")

            updated = agents.read_text(encoding="utf-8")
            self.assertEqual(1, updated.count(MARKER_BEGIN))
            self.assertEqual(1, updated.count(MARKER_END))
            self.assertNotIn("# Codex 公司项目工作流", updated)
            self.assertIn("人类优先总结", updated)
            backups = list((project / ".codex-workflow/backups").glob("AGENTS.*.bak"))
            self.assertEqual(1, len(backups))
            self.assertEqual(original, backups[0].read_text(encoding="utf-8"))
            self.assertEqual(
                hashlib.sha256(original.encode()).hexdigest(),
                hashlib.sha256(backups[0].read_bytes()).hexdigest(),
            )
            self.assertEqual("# Confirmed project index\n", index.read_text(encoding="utf-8"))
            self.assertTrue((project / "specs/global/INDEX.generated.md").is_file())
            self.assertTrue((project / "specs/global/assets.generated").is_dir())
            self.assertTrue((project / ".codex-workflow/install.json").is_file())
            self.assertEqual(source_hash, hashlib.sha256(source_file.read_bytes()).hexdigest())

    def test_migrate_project_refuses_unknown_mixed_legacy_rules(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            original = ZH_STARTER.read_text(encoding="utf-8") + (
                "\n## 项目本地规则\n\nKEEP_LOCAL_RULE\n"
            )
            agents = project / "AGENTS.md"
            agents.write_text(original, encoding="utf-8")

            result = subprocess.run(
                ["bash", str(INSTALLER), "migrate-project", str(project), "--lang", "zh"],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )

            self.assertNotEqual(0, result.returncode)
            self.assertEqual(original, agents.read_text(encoding="utf-8"))
            self.assertIn("KEEP_LOCAL_RULE", agents.read_text(encoding="utf-8"))
            self.assertTrue((project / "AGENTS.generated.md").is_file())
            backups = list((project / ".codex-workflow/backups").glob("AGENTS.*.bak"))
            self.assertEqual(1, len(backups))

    def test_migrate_project_refuses_local_preamble_before_legacy_rules(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            original = "# Project preamble\n\nKEEP_LOCAL_RULE\n\n" + ZH_STARTER.read_text(
                encoding="utf-8"
            )
            agents = project / "AGENTS.md"
            agents.write_text(original, encoding="utf-8")

            result = subprocess.run(
                ["bash", str(INSTALLER), "migrate-project", str(project), "--lang", "zh"],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )

            self.assertNotEqual(0, result.returncode)
            self.assertEqual(original, agents.read_text(encoding="utf-8"))
            self.assertTrue((project / "AGENTS.generated.md").is_file())
            self.assertEqual(
                1, len(list((project / ".codex-workflow/backups").glob("AGENTS.*.bak")))
            )

    def test_migrate_project_recognizes_current_full_bilingual_distributions(self):
        for language, source in FULL_PLUGINS.items():
            with self.subTest(language=language), tempfile.TemporaryDirectory() as directory:
                project = Path(directory)
                (project / "AGENTS.md").write_text(
                    source.read_text(encoding="utf-8"), encoding="utf-8"
                )

                run_installer("migrate-project", str(project), "--lang", language)

                updated = (project / "AGENTS.md").read_text(encoding="utf-8")
                self.assertEqual(1, updated.count(MARKER_BEGIN))
                self.assertEqual(
                    1,
                    len(list((project / ".codex-workflow/backups").glob("AGENTS.*.bak"))),
                )

    def test_migrate_project_recognizes_024_bilingual_full_distributions(self):
        commit_check = subprocess.run(
            ["git", "cat-file", "-e", "c8afa28^{commit}"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if commit_check.returncode != 0:
            self.skipTest("Git history is unavailable in the packaged test environment")
        paths = {
            "zh": "outputs/company-codex-workflow-v2-zh/AGENTS.md",
            "en": "outputs/company-codex-workflow-v2/AGENTS.md",
        }
        for language, path in paths.items():
            with self.subTest(language=language), tempfile.TemporaryDirectory() as directory:
                original = subprocess.run(
                    ["git", "show", f"c8afa28:{path}"],
                    check=True,
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                ).stdout
                project = Path(directory)
                (project / "AGENTS.md").write_text(original, encoding="utf-8")

                run_installer("migrate-project", str(project), "--lang", language)

                self.assertEqual(
                    1,
                    (project / "AGENTS.md").read_text(encoding="utf-8").count(MARKER_BEGIN),
                )

    def test_migrate_project_rejects_force_before_overwriting_project_assets(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            original = ZH_STARTER.read_text(encoding="utf-8")
            agents = project / "AGENTS.md"
            agents.write_text(original, encoding="utf-8")
            bundle = project / "BUNDLES.md"
            bundle.write_text("local bundle\n", encoding="utf-8")

            result = subprocess.run(
                [
                    "bash",
                    str(INSTALLER),
                    "migrate-project",
                    str(project),
                    "--lang",
                    "zh",
                    "--force",
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )

            self.assertNotEqual(0, result.returncode)
            self.assertEqual(original, agents.read_text(encoding="utf-8"))
            self.assertEqual("local bundle\n", bundle.read_text(encoding="utf-8"))

    def test_migrate_project_recognizes_utf8_bom_starter(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            original = "\ufeff" + ZH_STARTER.read_text(encoding="utf-8")
            agents = project / "AGENTS.md"
            agents.write_text(original, encoding="utf-8")

            run_installer("migrate-project", str(project), "--lang", "zh")

            updated = agents.read_text(encoding="utf-8")
            self.assertEqual(1, updated.count(MARKER_BEGIN))
            self.assertNotIn("\ufeff", updated)
            backup = next((project / ".codex-workflow/backups").glob("AGENTS.*.bak"))
            self.assertEqual(original, backup.read_text(encoding="utf-8"))

    def test_update_templates_keeps_custom_rules_and_adds_one_managed_block(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            agents = project / "AGENTS.md"
            agents.write_text("# Product rules\n\nKeep this local rule.\n", encoding="utf-8")

            run_installer("update-templates", str(project), "--lang", "en")

            updated = agents.read_text(encoding="utf-8")
            self.assertIn("Keep this local rule.", updated)
            self.assertEqual(1, updated.count(MARKER_BEGIN))
            self.assertIn("Human-First Summary", updated)
            self.assertFalse((project / "AGENTS.generated.md").exists())

    def test_force_template_update_backs_up_existing_assets_before_replacement(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=project, check=True)
            assets = project / "specs/global/assets"
            assets.mkdir(parents=True)
            local_template = assets / "quality-validation-report-template.md"
            local_template.write_text("LOCAL_TEMPLATE\n", encoding="utf-8")
            project_only_template = assets / "project-only-template.md"
            project_only_template.write_text("KEEP_PROJECT_ONLY\n", encoding="utf-8")

            run_installer(
                "update-templates",
                str(project),
                "--lang",
                "zh",
                "--force",
            )

            backups = list(
                (project / ".codex-workflow/backups").glob("assets.*")
            )
            self.assertEqual(1, len(backups))
            self.assertEqual(
                "LOCAL_TEMPLATE\n",
                (backups[0] / "quality-validation-report-template.md").read_text(
                    encoding="utf-8"
                ),
            )
            updated = local_template.read_text(encoding="utf-8")
            self.assertIn("## 先看结论", updated)
            self.assertLess(updated.index("## 先看结论"), updated.index("## 元信息"))
            self.assertEqual(
                "KEEP_PROJECT_ONLY\n",
                project_only_template.read_text(encoding="utf-8"),
            )
            ignored = subprocess.run(
                ["git", "check-ignore", "-q", str(backups[0])],
                cwd=project,
            )
            self.assertEqual(0, ignored.returncode)

    def test_powershell_exposes_equivalent_migration_command(self):
        content = (ROOT / "scripts/install.ps1").read_text(encoding="utf-8")
        self.assertIn("migrate-project", content)
        self.assertIn("function Migrate-Project", content)
        self.assertIn("Backed up project templates", content)
        self.assertIn(".codex-workflow/backups/", content)
        self.assertIn("$_.Trim() -eq $pattern", content)

    def test_powershell_force_template_update_when_available(self):
        pwsh = shutil.which("pwsh")
        if not pwsh:
            self.skipTest("pwsh is not installed")
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=project, check=True)
            assets = project / "specs/global/assets"
            assets.mkdir(parents=True)
            local_template = assets / "quality-validation-report-template.md"
            local_template.write_text("LOCAL_TEMPLATE\n", encoding="utf-8")
            project_only_template = assets / "project-only-template.md"
            project_only_template.write_text("KEEP_PROJECT_ONLY\n", encoding="utf-8")

            subprocess.run(
                [
                    pwsh,
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-File",
                    str(ROOT / "scripts/install.ps1"),
                    "update-templates",
                    str(project),
                    "-Lang",
                    "zh",
                    "-Force",
                ],
                check=True,
                cwd=ROOT,
                capture_output=True,
                text=True,
            )

            backups = list((project / ".codex-workflow/backups").glob("assets.*"))
            self.assertEqual(1, len(backups))
            self.assertEqual("LOCAL_TEMPLATE\n", read(backups[0] / local_template.name))
            self.assertEqual("KEEP_PROJECT_ONLY\n", read(project_only_template))
            self.assertIn("## 先看结论", read(local_template))
            ignored = subprocess.run(
                ["git", "check-ignore", "-q", str(backups[0])], cwd=project
            )
            self.assertEqual(0, ignored.returncode)

    def test_powershell_executes_migration_when_available(self):
        pwsh = shutil.which("pwsh")
        if not pwsh:
            self.skipTest("pwsh is not installed")
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / "AGENTS.md").write_text(
                ZH_STARTER.read_text(encoding="utf-8"), encoding="utf-8"
            )
            subprocess.run(
                [
                    pwsh,
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-File",
                    str(ROOT / "scripts/install.ps1"),
                    "migrate-project",
                    str(project),
                    "-Lang",
                    "zh",
                ],
                check=True,
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertTrue((project / ".codex-workflow/install.json").is_file())
            updated = (project / "AGENTS.md").read_text(encoding="utf-8")
            self.assertEqual(1, updated.count(MARKER_BEGIN))
            self.assertEqual(1, updated.count(MARKER_END))
            self.assertNotIn("# Codex 公司项目工作流", updated)
            backup = next((project / ".codex-workflow/backups").glob("AGENTS.*.bak"))
            self.assertEqual(
                ZH_STARTER.read_bytes(),
                backup.read_bytes(),
            )

    def test_duplicate_managed_blocks_are_rejected_without_changes(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            block = f"{MARKER_BEGIN}\nold\n{MARKER_END}"
            original = f"# Local\n\n{block}\n\n{block}\n"
            agents = project / "AGENTS.md"
            agents.write_text(original, encoding="utf-8")

            result = subprocess.run(
                ["bash", str(INSTALLER), "update-templates", str(project), "--lang", "zh"],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )

            self.assertNotEqual(0, result.returncode)
            self.assertEqual(original, agents.read_text(encoding="utf-8"))

    def test_node_wrapper_executes_migration(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / "AGENTS.md").write_text(
                ZH_STARTER.read_text(encoding="utf-8"), encoding="utf-8"
            )

            subprocess.run(
                ["node", str(NODE_WRAPPER), "migrate-project", str(project), "--lang", "zh"],
                check=True,
                cwd=ROOT,
                capture_output=True,
                text=True,
            )

            self.assertTrue((project / ".codex-workflow/install.json").is_file())
            self.assertEqual(
                1,
                (project / "AGENTS.md").read_text(encoding="utf-8").count(MARKER_BEGIN),
            )


if __name__ == "__main__":
    unittest.main()
