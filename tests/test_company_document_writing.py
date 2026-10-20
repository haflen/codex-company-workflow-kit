import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('writing_dependencies', ROOT / 'scripts/expert_dependencies.py')
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

class CompanyDocumentWritingDependencyTests(unittest.TestCase):
    def test_missing_writer_blocks_installation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name, *_ in MODULE.EXPERTS:
                if name != 'company-document-writing':
                    p = root / 'skills' / name / 'SKILL.md'
                    p.parent.mkdir(parents=True)
                    p.write_text('existing expert')
            with self.assertRaisesRegex(SystemExit, 'company-document-writing'):
                MODULE.fail_if_missing_or_blocking(MODULE.collect_reviews(root))

    def test_both_plugins_ship_internal_writer_and_reference(self):
        for suffix in ('', '-zh'):
            root = ROOT / 'outputs' / ('company-codex-workflow-v2' + suffix)
            reviews = MODULE.collect_reviews(root)
            writer = next((r for r in reviews if r.name == 'company-document-writing'), None)
            self.assertIsNotNone(writer)
            self.assertTrue(writer.installed)
            self.assertEqual('company-document-writing', writer.bundle)
            self.assertTrue((root / 'skills/company-document-writing/references/report-writing.md').is_file())
            with tempfile.TemporaryDirectory() as directory:
                target = Path(directory) / 'review.json'
                MODULE.write_json(reviews, target)
                source = json.loads(target.read_text())['sourceOverrides']['company-document-writing']
                self.assertEqual('company-authored', source['origin'])
            for filename in ('BUNDLES.md', 'EXPERTS.lock.md', 'skills/company-workflow-help/SKILL.md', 'skills/company-expert-routing/SKILL.md'):
                self.assertIn('company-document-writing', (root / filename).read_text())

if __name__ == '__main__':
    unittest.main()
