"""Test result observation without launching Codex or trusting its claims."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

PATH = Path(__file__).parent / 'scenarios/managed_delivery/run_live.py'
spec = importlib.util.spec_from_file_location('run_live', PATH)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class ObserverTests(unittest.TestCase):
    def test_api_pending_fixture_really_passes_local_tests(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project, _ = runner.setup(root, {'id': 'TC-008', 'prompt': 'API pending'}, root / 'workflow')
            result = runner.command(['python3', '-B', 'test_labels.py'], project, check=False)
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_api_attempt_is_execution_not_reading(self):
        self.assertFalse(runner.attempted_api({'command': 'cat verify_api.py'}))
        self.assertTrue(runner.attempted_api({'command': "python3 -B verify_api.py; git status --short"}))

    def test_verification_requires_real_test_output(self):
        self.assertFalse(runner.verified_tests({'command': 'cat test_labels.py', 'exit_code': 0}))
        self.assertTrue(runner.verified_tests({'command': 'python3 -m unittest discover -v', 'exit_code': 0,
                                               'aggregated_output': 'Ran 2 tests in 0.001s\n\nOK\n'}))
        self.assertFalse(runner.verified_tests({'command': 'python3 test_labels.py', 'exit_code': 1,
                                                'aggregated_output': 'FAILED (failures=1)'}))

    def test_missing_or_corrupt_json_is_retained_as_failed_observation(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'state.json'
            self.assertIsNone(runner.read_object(path))
            path.write_text('{broken')
            self.assertIsNone(runner.read_object(path))
            path.write_text('[]')
            self.assertIsNone(runner.read_object(path))
            path.write_text('{"status":"prepared"}')
            self.assertEqual(runner.read_object(path), {'status': 'prepared'})

    def test_package_must_contain_current_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / 'dist').mkdir()
            (project / 'labels.py').write_text('current')
            package = project / 'dist/labels.zip'
            self.assertFalse(runner.package_matches(project))
            package.write_text('not zip')
            self.assertFalse(runner.package_matches(project))
            with zipfile.ZipFile(package, 'w') as archive:
                archive.writestr('labels.py', 'old')
            self.assertFalse(runner.package_matches(project))
            with zipfile.ZipFile(package, 'w') as archive:
                archive.writestr('labels.py', 'current')
            self.assertTrue(runner.package_matches(project))


if __name__ == '__main__':
    unittest.main()
