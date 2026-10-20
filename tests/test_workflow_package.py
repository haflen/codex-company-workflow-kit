"""Package staging is offline and never registers a plugin with the current host."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

class WorkflowPackageTests(unittest.TestCase):
    def test_verification_entry_covers_all_regressions(self):
        for name in ('package.json', 'scripts/install.sh', 'scripts/install.ps1'):
            self.assertIn('unittest discover', (ROOT / name).read_text())

    def test_npm_package_excludes_runtime_bytecode(self):
        with tempfile.TemporaryDirectory(prefix='workflow-pack-filter-') as directory:
            project = Path(directory)
            manifest = json.loads((ROOT / 'package.json').read_text())
            (project / 'package.json').write_text(json.dumps(manifest))
            folder = project / 'outputs/example/__pycache__'; folder.mkdir(parents=True)
            (folder / 'cached.pyc').write_bytes(b'runtime-cache')
            (folder.parent / 'legacy.pyc').write_bytes(b'runtime-cache')
            (folder.parent / 'SKILL.md').write_text('ship this skill')
            result = subprocess.run(['npm', 'pack', '--dry-run', '--json', '--ignore-scripts', '--cache', str(project / 'npm-cache')], cwd=project, capture_output=True, text=True)
            self.assertEqual(0, result.returncode, result.stderr)
            files = [item['path'] for item in json.loads(result.stdout)[0]['files']]
            self.assertIn('outputs/example/SKILL.md', files)
            self.assertFalse([p for p in files if '__pycache__' in p or p.endswith('.pyc')], files)

    def test_bilingual_state_and_manifest_versions_match(self):
        version = json.loads((ROOT / 'package.json').read_text())['version']
        scripts = []
        for name in ('company-codex-workflow-v2', 'company-codex-workflow-v2-zh'):
            plugin = ROOT / 'outputs' / name
            self.assertEqual((plugin / 'plugin.json').read_bytes(), (plugin / '.codex-plugin/plugin.json').read_bytes())
            self.assertEqual(version, json.loads((plugin / 'plugin.json').read_text())['version'])
            scripts.append((plugin / 'skills/company-workflow-help/scripts/task_state.py').read_bytes())
        self.assertEqual(*scripts)

    def test_staging_install_is_offline_and_preserves_project_state(self):
        with tempfile.TemporaryDirectory(prefix='workflow-package-') as directory:
            stage = Path(directory) / '中文 staging'
            state = stage / 'project/.codex-workflow/tasks/demo/state.json'
            state.parent.mkdir(parents=True); state.write_text('preserve user task')
            # Never run an old installer that would silently ignore the isolation flag.
            self.assertIn('--staging-root)', (ROOT / 'scripts/install.sh').read_text())
            stub = Path(directory) / 'reject-cli'
            stub.write_text('#!/bin/sh\necho unexpected-live-registration >&2\nexit 99\n'); stub.chmod(0o755)
            for lang, name in [('zh', 'company-codex-workflow-v2-zh'), ('en', 'company-codex-workflow-v2')]:
                result = subprocess.run(['bash', str(ROOT / 'scripts/install.sh'), 'install-plugin', '--lang', lang, '--staging-root', str(stage)], env=dict(os.environ, CODEX_CLI=str(stub)), capture_output=True, text=True)
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)
                self.assertIn('not registered', result.stdout)
                self.assertEqual([], list((stage / 'plugins' / name).rglob('.DS_Store')))
                for path in (ROOT / 'outputs' / name).rglob('*'):
                    if path.is_file() and '__pycache__' not in path.parts and path.name != '.DS_Store':
                        self.assertEqual(path.read_bytes(), (stage / 'plugins' / name / path.relative_to(ROOT / 'outputs' / name)).read_bytes())
            self.assertEqual('preserve user task', state.read_text())
            self.assertFalse((stage / '.agents/plugins/marketplace.json').exists())

    def test_managed_block_custom_content_is_review_only(self):
        with tempfile.TemporaryDirectory(prefix='workflow-managed-') as directory:
            project = Path(directory)
            original = ('# Local preamble\n<!-- codex-workflow-kit:company:start -->\n'
                        '# Old managed workflow\nCUSTOM_INSIDE_BLOCK\n'
                        '<!-- codex-workflow-kit:company:end -->\nLocal suffix\n')
            agents = project / 'AGENTS.md'; agents.write_text(original)
            result = subprocess.run(['bash', str(ROOT / 'scripts/install.sh'), 'update-templates', str(project)], capture_output=True, text=True)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertEqual(original, agents.read_text())
            generated = (project / 'AGENTS.generated.md').read_text()
            self.assertIn('Local preamble', generated)
            self.assertIn('Local suffix', generated)
            self.assertIn('FLOW-01', generated)

    def check_existing_generated_preserved(self, installer):
        for symlink in (False, True):
            with self.subTest(symlink=symlink), tempfile.TemporaryDirectory(prefix='workflow-candidate-') as directory:
                project = Path(directory)
                agents = project / 'AGENTS.md'
                original = '<!-- codex-workflow-kit:company:start -->\nOLD\n<!-- codex-workflow-kit:company:end -->\n'
                agents.write_text(original)
                candidate = project / 'AGENTS.generated.md'
                if symlink:
                    target = project / 'user-notes.md'; target.write_text('USER_REVIEWED_CANDIDATE')
                    candidate.symlink_to(target)
                else:
                    candidate.write_text('USER_REVIEWED_CANDIDATE')
                result = subprocess.run(installer + ['update-templates', str(project)], capture_output=True, text=True)
                self.assertEqual('USER_REVIEWED_CANDIDATE', candidate.read_text())
                self.assertEqual(original, agents.read_text())
                self.assertNotEqual(0, result.returncode)
                self.assertIn('AGENTS.generated.md', result.stdout + result.stderr)

    def test_existing_generated_candidate_is_never_overwritten_bash(self):
        self.check_existing_generated_preserved(['bash', str(ROOT / 'scripts/install.sh')])

    def test_existing_generated_candidate_is_never_overwritten_powershell(self):
        if not shutil.which('pwsh'):
            self.skipTest('pwsh is not installed')
        self.check_existing_generated_preserved(['pwsh', '-NoProfile', '-File', str(ROOT / 'scripts/install.ps1')])

    def test_unknown_template_content_and_task_survive_update_and_manual_rollback(self):
        with tempfile.TemporaryDirectory(prefix='workflow-update-') as directory:
            project = Path(directory) / 'project'; project.mkdir()
            agents = project / 'AGENTS.md'
            original = '# 公司 Codex 工作流\n## 上下文优先\n## 阶段边界\n## Superpowers\nUNKNOWN_CUSTOM\n'
            agents.write_text(original)
            assets = project / 'specs/global/assets'; assets.mkdir(parents=True)
            (assets / 'task-execution-policy.md').write_text('local customized policy')
            (assets / 'unknown.txt').write_text('preserve unknown')
            state = project / '.codex-workflow/tasks/demo/state.json';state.parent.mkdir(parents=True);state.write_text('existing task')
            result = subprocess.run(['bash', str(ROOT / 'scripts/install.sh'), 'update-templates', str(project)], capture_output=True, text=True)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertEqual(original, agents.read_text())
            self.assertEqual('local customized policy', (assets / 'task-execution-policy.md').read_text())
            self.assertEqual('preserve unknown', (assets / 'unknown.txt').read_text())
            self.assertTrue((project / 'AGENTS.generated.md').exists())
            self.assertTrue((project / 'specs/global/assets.generated/task-execution-policy.md').exists())
            backup = Path(directory) / 'assets-backup';shutil.copytree(assets, backup)
            shutil.copyfile(project / 'specs/global/assets.generated/task-execution-policy.md', assets / 'task-execution-policy.md')
            self.assertNotEqual('local customized policy', (assets / 'task-execution-policy.md').read_text())
            shutil.copytree(backup, assets, dirs_exist_ok=True)
            self.assertEqual('local customized policy', (assets / 'task-execution-policy.md').read_text())
            self.assertEqual('existing task', state.read_text())

if __name__ == '__main__':
    unittest.main()
