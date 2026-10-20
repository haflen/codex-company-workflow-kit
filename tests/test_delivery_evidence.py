"""Completion and evidence applicability, using the real state CLI and files."""
import copy
from datetime import datetime, timezone
import hashlib
import json
import subprocess
import unittest

import test_task_state as state_tests


class DeliveryEvidenceTests(unittest.TestCase):
    setUp = state_tests.TaskStateTests.setUp
    call = state_tests.TaskStateTests.call
    init = state_tests.TaskStateTests.init
    update = state_tests.TaskStateTests.update

    def evidence(self, state, identity='E1', result='pass', **extra):
        path = self.state_path.parent / f'evidence/{identity}.log'
        path.parent.mkdir(exist_ok=True)
        path.write_text(f'Original check {identity}: {result}\n')
        return dict(id=identity, acceptance_id='AC-1', check_id='unit', command='python3 test_code.py',
                    environment='local-fixture', recorded_at=datetime.now(timezone.utc).isoformat(), result=result,
                    path=str(path.relative_to(self.root)), sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                    candidate_fingerprint=state['candidate']['fingerprint'], **extra)

    def running(self, value=None):
        if value:
            self.contract_path.write_text(json.dumps(value))
        state = self.init()
        code, result = self.update({'status': 'running', 'environment': 'local-fixture'}, state['revision'])
        self.assertEqual(code, 0, result)
        return result['state']

    def complete(self, state, **patch):
        return self.update(dict(status='completed', phase='delivery', **patch), state['revision'])

    def test_latest_failure_or_skip_cannot_hide_behind_earlier_pass(self):
        state = self.running()
        for result in ('fail', 'skipped', 'unknown', 'blocked'):
            proofs = [self.evidence(state), self.evidence(state, 'E2', result)]
            self.assertEqual(self.complete(state, evidence=proofs)[0], 4)

    def test_required_check_mapping_cannot_omit_api_or_replace_it_with_unit_pass(self):
        value = state_tests.contract(); value['acceptance'][0]['check_ids'] = ['unit', 'api']
        state = self.running(value); proof = self.evidence(state)
        self.assertEqual(self.complete(state, evidence=[proof])[0], 4)
        api = self.evidence(state, 'E2', 'fail'); api['check_id'] = 'api'
        self.assertEqual(self.complete(state, evidence=[api, proof])[0], 4)

    def test_scoped_evidence_survives_unrelated_change_but_not_covered_change(self):
        value = state_tests.contract(); value['allowed_paths'].append('notes.md')
        state = self.running(value); proof = self.evidence(state, scope=['code.py'])
        code, checked = self.update({'evidence': [proof]}, state['revision'])
        self.assertEqual(code, 0, checked)
        (self.root / 'notes.md').write_text('unrelated documentation')
        _, changed = self.update({'next_step': 'closeout'}, checked['revision'])
        code, completed = self.complete(changed['state'])
        self.assertEqual(code, 0, completed)
        self.assertEqual(self.call('validate')[0], 0)
        (self.root / 'code.py').write_text('value = 99\n')
        self.assertEqual(self.call('validate')[0], 4)

    def test_covered_change_blocks_old_pass_after_snapshot_refresh(self):
        state = self.running(); proof = self.evidence(state, scope=['code.py'])
        _, checked = self.update({'evidence': [proof]}, state['revision'])
        (self.root / 'code.py').write_text('value = 99\n')
        _, changed = self.update({'next_step': 'recheck'}, checked['revision'])
        self.assertEqual(self.complete(changed['state'])[0], 4)
        new = self.evidence(changed['state'], 'E2', scope=['code.py'])
        self.assertEqual(self.complete(changed['state'], evidence=changed['state']['evidence'] + [new])[0], 0)

    def test_external_pass_requires_fresh_evidence_at_completion(self):
        value = state_tests.contract(); value['acceptance'][0]['external'] = True
        state = self.running(value); proof = self.evidence(state, external=True)
        _, checked = self.update({'evidence': [proof]}, state['revision'])
        self.assertEqual(self.complete(checked['state'])[0], 4)
        fresh = self.evidence(checked['state'], 'E2', external=True)
        self.assertEqual(self.complete(checked['state'], evidence=checked['state']['evidence'] + [fresh])[0], 0)

    def test_old_external_output_cannot_be_relabelled_with_a_new_record_id(self):
        value = state_tests.contract(); value['acceptance'][0]['external'] = True
        state = self.running(value); proof = self.evidence(state, external=True)
        proof['recorded_at'] = '2000-01-01T00:00:00+00:00'
        self.assertEqual(self.complete(state, evidence=[proof])[0], 4)

    def test_environment_drift_invalidates_unchanged_code(self):
        state = self.running(); proof = self.evidence(state)
        _, checked = self.update({'evidence': [proof]}, state['revision'])
        _, changed = self.update({'environment': 'different-deployment'}, checked['revision'])
        self.assertEqual(self.complete(changed['state'])[0], 4)

    def test_changed_acceptance_invalidates_old_evidence_even_if_code_same(self):
        state = self.running(); proof = self.evidence(state, scope=['code.py'])
        _, checked = self.update({'evidence': [proof]}, state['revision'])
        value = copy.deepcopy(state['contract']); value['acceptance'][0]['reference'] = 'TASK.md:corrected-rule'
        value['authorization']['sources'].append({'id': 'U2', 'reference': 'user:correction', 'quote': 'Use the corrected acceptance rule.'})
        code, changed = self.update({'contract': value, 'contract_change_source': 'U2'}, checked['revision'])
        self.assertEqual(code, 0, changed)
        self.assertEqual(self.complete(changed['state'])[0], 4)

    def test_missing_artifact_or_raw_log_prevents_completed(self):
        value = state_tests.contract(); value['required_artifacts'].append('dist/package.zip')
        state = self.running(value); proof = self.evidence(state)
        self.assertEqual(self.complete(state, evidence=[proof])[0], 4)
        (self.root / proof['path']).unlink()
        self.assertEqual(self.complete(state, evidence=[proof])[0], 4)

    def test_commit_and_deliver_need_authority_and_confirmed_operation_evidence(self):
        for endpoint, action in [('commit', 'commit'), ('deliver', 'push')]:
            with self.subTest(endpoint=endpoint):
                value = state_tests.contract(); value['delivery_endpoint'] = endpoint
                state = self.running(value); proof = self.evidence(state)
                self.assertEqual(self.complete(state, evidence=[proof], milestones={endpoint: ['E1']})[0], 4)
                value['authorization']['actions'].append({'action': action, 'scope': ['fixture-target'], 'source_ids': ['U1']})
                _, updated = self.update({'contract': value, 'contract_change_source': 'U1'}, state['revision'])
                state = updated['state']; proof = self.evidence(state)
                self.assertEqual(self.complete(state, evidence=[proof], milestones={endpoint: ['E1']})[0], 4)
                op = {'id': 'OP1', 'action': action, 'target': 'fixture-target', 'status': 'confirmed', 'evidence_ids': ['E1']}
                self.assertEqual(self.complete(state, evidence=[proof], milestones={endpoint: ['E1']}, operations=[op])[0], 0)
                self.state_path.unlink()  # Independent test task, never a production reset.

    def test_forged_scope_snapshot_is_recomputed_and_unknown_paths_rejected(self):
        state = self.running(); proof = self.evidence(state, scope=['code.py'], inputs={'code.py': 'fake'})
        code, checked = self.update({'evidence': [proof]}, state['revision'])
        self.assertEqual(code, 0, checked)
        self.assertEqual(checked['state']['evidence'][0]['inputs']['code.py'], state['candidate']['files']['code.py'])
        bad = self.evidence(checked['state'], 'E2', scope=['unapproved.py'])
        self.assertEqual(self.update({'evidence': checked['state']['evidence'] + [bad]}, checked['revision'])[0], 2)

    def test_confirmed_operation_cannot_drop_its_original_result_reference(self):
        state = self.running(); first = self.evidence(state); second = self.evidence(state, 'E2')
        operation = {'id': 'OP1', 'action': 'package', 'target': 'fixture', 'status': 'confirmed', 'evidence_ids': ['E1']}
        code, checked = self.update({'evidence': [first, second], 'operations': [operation]}, state['revision'])
        self.assertEqual(code, 0, checked)
        operation['evidence_ids'] = ['E2']
        self.assertEqual(self.update({'operations': [operation]}, checked['revision'])[0], 2)

    def test_git_endpoint_evidence_cannot_survive_head_drift_using_file_scope(self):
        def git(*args):
            subprocess.run(['git', '-C', str(self.root), *args], check=True, capture_output=True)
        git('init', '-b', 'fixture')
        git('config', 'user.name', 'Local Test'); git('config', 'user.email', 'test@example.invalid')
        git('add', '--', 'code.py'); git('commit', '-m', 'initial fixture')
        value = state_tests.contract(); value['delivery_endpoint'] = 'commit'
        value['authorization']['actions'].append({'action': 'commit', 'scope': ['fixture'], 'source_ids': ['U1']})
        state = self.running(value); proof = self.evidence(state, scope=['code.py'])
        op = {'id': 'OP1', 'action': 'commit', 'target': 'fixture', 'status': 'confirmed', 'evidence_ids': ['E1']}
        _, checked = self.update({'evidence': [proof], 'operations': [op], 'milestones': {'commit': ['E1']}}, state['revision'])
        git('commit', '--allow-empty', '-m', 'different head with identical code')
        _, changed = self.update({'next_step': 'inspect actual commit result'}, checked['revision'])
        self.assertEqual(self.complete(changed['state'])[0], 4)



class EvidenceCollectorTests(unittest.TestCase):
    setUp = state_tests.TaskStateTests.setUp

    def collect(self, paths=None, checks=None, output='report.json'):
        manifest = self.root / 'paths.json'
        manifest.write_text(json.dumps({'paths': paths if paths is not None else ['code.py'], 'checks': checks or []}))
        script = state_tests.ROOT / 'outputs/company-codex-workflow-v2-zh/skills/company-delivery-closeout/scripts/collect_delivery_evidence.py'
        result = subprocess.run(['python3', '-B', str(script), '--project-root', str(self.root), '--paths-file', str(manifest), '--output', output], capture_output=True, text=True)
        self.assertTrue(result.stdout, result.stderr)
        return result.returncode, json.loads(result.stdout)

    def test_invalid_manifest_and_outside_absolute_path_return_input_error(self):
        script = state_tests.ROOT / 'outputs/company-codex-workflow-v2-zh/skills/company-delivery-closeout/scripts/collect_delivery_evidence.py'
        for content, output in [('{', 'report.json'), ('[]', 'report.json'), ('{"paths": null}', 'report.json'), ('{"paths": ["code.py"], "checks": null}', 'report.json'), ('{"paths": ["code.py"]}', str(self.root.parent / 'outside.json'))]:
            with self.subTest(content=content, output=output):
                manifest = self.root / 'paths.json'; manifest.write_text(content)
                result = subprocess.run(['python3', '-B', str(script), '--project-root', str(self.root), '--paths-file', str(manifest), '--output', output], capture_output=True, text=True)
                self.assertEqual(2, result.returncode, result.stdout + result.stderr)
                self.assertFalse(json.loads(result.stdout)['ok'])
                self.assertFalse((self.root / 'report.json').exists())

    def capture(self, code=0):
        p = self.root / 'capture.json'
        p.write_text(json.dumps({'command': ['python3', 'checks.py'], 'check_exit_code': code, 'stdout': 'raw check output', 'stderr': 'original error' if code else ''}))
        return [{'id': 'unit', 'capture_path': 'capture.json'}]

    def test_collects_unicode_untracked_paths_and_matches_state_candidate(self):
        p = self.root / '中文 文件.txt'; p.write_text('内容')
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        value = state_tests.contract(); value['allowed_paths'] = ['code.py', p.name];value['required_artifacts'] = []
        self.contract_path.write_text(json.dumps(value))
        result = subprocess.run(['python3', '-B', str(state_tests.SCRIPT), 'init', '--project-root', str(self.root), '--task-id', 'T-001', '--contract', str(self.contract_path)], capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stdout)
        state = json.loads(result.stdout)['state']
        code, report = self.collect(value['allowed_paths'])
        self.assertEqual(0, code, report)
        self.assertEqual(state['candidate'], report['candidate'])
        self.assertEqual(report, json.loads((self.root / 'report.json').read_text()))

    def test_plain_python_invocation_does_not_write_plugin_bytecode(self):
        import os
        import shutil
        plugin = self.root / 'isolated-plugin'
        source = state_tests.ROOT / 'outputs/company-codex-workflow-v2-zh/skills'
        for name in ('company-workflow-help/scripts/task_state.py', 'company-delivery-closeout/scripts/collect_delivery_evidence.py'):
            target = plugin / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source / name, target)
        manifest = self.root / 'paths.json'
        manifest.write_text(json.dumps({'paths': ['code.py']}))
        env = dict(os.environ)
        env.pop('PYTHONDONTWRITEBYTECODE', None)
        env.pop('PYTHONPYCACHEPREFIX', None)
        result = subprocess.run(['python3', str(plugin / 'company-delivery-closeout/scripts/collect_delivery_evidence.py'),
            '--project-root', str(self.root), '--paths-file', str(manifest), '--output', 'plain-report.json'],
            env=env, capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual([], list(plugin.rglob('__pycache__')))

    def test_missing_file_keeps_partial_result_and_fails(self):
        code, report = self.collect(['code.py', 'disappeared.py'])
        self.assertNotEqual(0, code)
        self.assertIsNone(report['candidate'])
        self.assertEqual(hashlib.sha256((self.root / 'code.py').read_bytes()).hexdigest(), report['files']['code.py'])
        self.assertIn('disappeared.py', str(report['errors']))

    def test_captured_failure_is_retained_and_returns_nonzero(self):
        code, report = self.collect(checks=self.capture(1))
        self.assertNotEqual(0, code)
        self.assertEqual(1, report['checks'][0]['check_exit_code'])
        self.assertEqual('not_assessed', report['acceptance'])
        self.assertNotIn('original error', json.dumps(report))

    def test_successful_capture_is_not_business_acceptance(self):
        code, report = self.collect(checks=self.capture())
        self.assertEqual(0, code, report)
        self.assertEqual('not_assessed', report['acceptance'])
        self.assertEqual(hashlib.sha256((self.root / 'capture.json').read_bytes()).hexdigest(), report['checks'][0]['sha256'])

    def test_commands_in_capture_are_never_executed(self):
        checks = self.capture(); path = self.root / 'capture.json'; data = json.loads(path.read_text())
        data['command'] = ['touch', str(self.root / 'unexpected-execution')];path.write_text(json.dumps(data))
        self.assertEqual(0, self.collect(checks=checks)[0])
        self.assertFalse((self.root / 'unexpected-execution').exists())

    def test_traversal_symlinks_and_secret_paths_fail(self):
        (self.root / '.env').write_text('SECRET=do-not-read')
        (self.root / 'link.py').symlink_to(self.root / 'code.py')
        for n, paths in enumerate((['../code.py'],['link.py'],['.env'])):
            code, report = self.collect(paths, output=f'report-{n}.json')
            self.assertNotEqual(0, code)
            self.assertNotIn('do-not-read', json.dumps(report))

    def test_malformed_capture_does_not_become_success(self):
        checks = self.capture();(self.root / 'capture.json').write_text('{broken')
        code, report = self.collect(checks=checks)
        self.assertNotEqual(0, code)
        self.assertTrue(report['errors'])

    def test_existing_output_or_candidate_output_is_not_overwritten(self):
        (self.root / 'report.json').write_text('user content')
        self.assertNotEqual(0, self.collect()[0])
        self.assertEqual('user content', (self.root / 'report.json').read_text())
        before = (self.root / 'code.py').read_bytes()
        self.assertNotEqual(0, self.collect(output='code.py')[0])
        self.assertEqual(before, (self.root / 'code.py').read_bytes())


    def test_fifo_is_rejected_without_reading_and_output_parent_symlink_is_rejected(self):
        import os
        os.mkfifo(self.root / 'pipe')
        code, report = self.collect(['pipe'])
        self.assertNotEqual(0, code)
        self.assertIn('only regular files', str(report['errors']))
        target = self.root / 'target'; target.mkdir()
        (self.root / 'alias').symlink_to(target, target_is_directory=True)
        self.assertNotEqual(0, self.collect(output='alias/report.json')[0])
        self.assertFalse((target / 'report.json').exists())

    def test_git_identity_timeout_preserves_collected_files(self):
        import importlib.util
        from unittest.mock import patch
        script = state_tests.ROOT / 'outputs/company-codex-workflow-v2-zh/skills/company-delivery-closeout/scripts/collect_delivery_evidence.py'
        spec = importlib.util.spec_from_file_location('collector_test', script)
        collector = importlib.util.module_from_spec(spec); spec.loader.exec_module(collector)
        files = collector.state.Files(self.root)
        try:
            with patch.object(collector.state, 'candidate', side_effect=subprocess.TimeoutExpired('git', 5)):
                report = collector.collect(self.root, files, {'paths': ['code.py']})
            self.assertFalse(report['ok'])
            self.assertIsNone(report['candidate'])
            self.assertTrue(report['files']['code.py'])
            self.assertIn('candidate identity unavailable', str(report['errors']))
        finally:
            files.close()

if __name__ == '__main__':
    unittest.main()
