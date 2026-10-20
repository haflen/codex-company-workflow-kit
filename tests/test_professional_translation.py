import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("translation_expert_dependencies", ROOT / "scripts/expert_dependencies.py")
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

class TranslationExpertTests(unittest.TestCase):
    def test_translation_is_required_and_missing_blocks(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            # Supply every other expert, so absence of translation is the only failure.
            for name, *_ in MODULE.EXPERTS:
                if name != "professional-translation":
                    path = root / "skills" / name / "SKILL.md"
                    path.parent.mkdir(parents=True)
                    path.write_text("plain expert")
            with self.assertRaisesRegex(SystemExit, "professional-translation"):
                MODULE.fail_if_missing_or_blocking(MODULE.collect_reviews(root))

    def test_provenance_distinguishes_translation_from_default_source(self):
        for suffix in ("", "-zh"):
            root = ROOT / "outputs" / ("company-codex-workflow-v2" + suffix)
            reviews = MODULE.collect_reviews(root)
            MODULE.fail_if_missing_or_blocking(reviews)
            self.assertTrue(any(r.name == "professional-translation" and r.installed for r in reviews))
            with tempfile.TemporaryDirectory() as temp:
                output = Path(temp) / "report.json"
                MODULE.write_json(reviews, output)
                data = json.loads(output.read_text())
                self.assertEqual(data["sourceOverrides"]["professional-translation"]["reference_repository"], "Tasdax123/claude-fidelity-translator")
                self.assertEqual(data["source"]["repository"], "sickn33/antigravity-awesome-skills")
            report = MODULE.render_markdown(reviews, "zh" if suffix else "en")
            self.assertIn("c9f0651b007b547bdfae103235a4567fa1acd75e", report)

    def test_both_distributions_have_routes_and_license(self):
        for suffix in ("", "-zh"):
            root = ROOT / "outputs" / ("company-codex-workflow-v2" + suffix)
            for file in ("BUNDLES.md", "EXPERTS.lock.md", "skills/company-workflow-help/SKILL.md", "skills/company-expert-routing/SKILL.md"):
                self.assertIn("professional-translation", (root / file).read_text(), file)
            skill = root / "skills/professional-translation"
            self.assertIn("Use when", (skill / "SKILL.md").read_text())
            self.assertIn("MIT License", (skill / "LICENSE").read_text())
            self.assertEqual(sorted(p.name for p in skill.iterdir()), ["LICENSE", "PROVENANCE.md", "SKILL.md"])

if __name__ == "__main__":
    unittest.main()
