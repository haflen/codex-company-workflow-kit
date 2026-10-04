import unittest
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = (
    "company-context-index", "company-feature-requirements",
    "company-feature-design", "company-feature-planning",
    "company-bugfix-runner", "company-implementation-runner",
    "company-quality-validation", "company-delivery-closeout",
    "company-workflow-health-check", "company-requirements-prototype",
    "company-spike-research",
)


class DocumentOwnershipTests(unittest.TestCase):
    def test_bootstrap_packages_policy_and_generated_index(self):
        for lang in ("zh", "en"):
            with tempfile.TemporaryDirectory() as folder:
                project = Path(folder) / "project"
                subprocess.run(
                    ["bash", str(ROOT / "scripts/install.sh"), "bootstrap-project", str(project), "--lang", lang],
                    check=True, capture_output=True, text=True,
                )
                self.assertTrue((project / "specs/global/assets/document-ownership.md").is_file())
                self.assertIn("document-ownership.md", (project / "specs/global/INDEX.md").read_text())
                self.assertIn("document-ownership.md", (project / "AGENTS.md").read_text())

    def test_shared_policy_is_packaged_in_both_languages(self):
        for suffix in ("", "-zh"):
            plugin = ROOT / f"outputs/company-codex-workflow-v2{suffix}"
            starter = ROOT / f"outputs/company-codex-workflow-template{suffix}"
            relative = "specs/global/assets/document-ownership.md"
            policy = (plugin / relative).read_text()
            self.assertEqual(policy, (starter / relative).read_text())
            for case in ("OWN-01", "OWN-02", "OWN-03", "OWN-04", "OWN-05", "OWN-06"):
                self.assertIn(case, policy)
            for field in ("work-item-id", "owner-path", "record-path", "release-target"):
                self.assertIn(field, policy)

    def test_all_document_writers_and_reviewers_load_policy(self):
        for suffix in ("", "-zh"):
            plugin = ROOT / f"outputs/company-codex-workflow-v2{suffix}"
            for skill in SKILLS:
                with self.subTest(language=suffix, skill=skill):
                    self.assertIn("document-ownership.md", (plugin / "skills" / skill / "SKILL.md").read_text())
            for name in ("company-codex-workflow-v2", "company-codex-workflow-template"):
                base = ROOT / "outputs" / f"{name}{suffix}"
                self.assertIn("document-ownership.md", (base / "AGENTS.md").read_text())
                self.assertIn("document-ownership.md", (base / "specs/global/INDEX.md").read_text())

    def test_unconditional_feature_routing_removed(self):
        obsolete = (
            "小变更可使用 `specs/features/", "小需求可保存到 `specs/features/",
            "每个功能创建 `specs/features/", "Save small work under `specs/features/",
            "Small changes may use one compact feature spec under `specs/features/",
            "For each feature, create `specs/features/",
        )
        for file in (ROOT / "outputs").rglob("*.md"):
            content = file.read_text()
            for phrase in obsolete:
                self.assertNotIn(phrase, content, str(file))


if __name__ == "__main__":
    unittest.main()
