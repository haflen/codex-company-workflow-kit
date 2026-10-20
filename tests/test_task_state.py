"""Exercise state CLI with real directories, processes and rejected unsafe input."""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'outputs/company-codex-workflow-v2-zh/skills/company-workflow-help/scripts/task_state.py'
ENGLISH = ROOT / 'outputs/company-codex-workflow-v2/skills/company-workflow-help/scripts/task_state.py'


def contract():
    return {'goal': 'Verify scoped change', 'allowed_paths': ['code.py'], 'excluded': ['push'],
            'spec_refs': ['TASK.md'], 'acceptance': [{'id': 'AC-1', 'reference': 'TASK.md', 'required': True}],
            'delivery_endpoint': 'prepare', 'required_artifacts': ['code.py'], 'decision_points': [],
            'limits': {'max_repair_rounds': 2, 'token_budget': None, 'deadline': None},
            'authorization': {'sources': [{'id': 'U1', 'reference': 'user:current-request', 'quote': 'Modify code.py and verify; no push.'}],
                              'actions': [{'action': 'edit', 'scope': ['code.py'], 'source_ids': ['U1']}]}}


class TaskStateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='task state 中文 ')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / 'code.py').write_text('value = 1\n')
        self.state_path = self.root / '.codex-workflow/tasks/T-001/state.json'
        self.contract_path = self.root / 'input.json'
        self.contract_path.write_text(json.dumps(contract()))

    def call(self, command, *args, task_id='T-001'):
        run = subprocess.run([sys.executable, str(SCRIPT), command, '--project-root', str(self.root),
                              '--task-id', task_id, *map(str, args)], capture_output=True, text=True)
        self.assertTrue(run.stdout.strip(), run.stderr)
        result = json.loads(run.stdout)
        for field in ('ok', 'task_id', 'revision', 'status', 'errors'):
            self.assertIn(field, result)
        return run.returncode, result

    def init(self):
        code, result = self.call('init', '--contract', self.contract_path)
        self.assertEqual(code, 0, result)
        return result['state']

    def update(self, data, revision=0):
        path = self.root / 'patch.json'
        path.write_text(json.dumps(data))
        return self.call('update', '--expected-revision', revision, '--patch-file', path)

    def test_init_show_and_valid_update(self):
        state = self.init()
        self.assertEqual((state['schema_version'], state['revision'], state['status']), (1, 0, 'ready'))
        before = self.state_path.read_bytes()
        self.assertEqual(self.call('show')[1]['state'], state)
        self.assertEqual(before, self.state_path.read_bytes())
        code, result = self.update({'status': 'running', 'phase': 'implementation', 'next_step': 'verify'})
        self.assertEqual(code, 0, result)
        self.assertEqual(result['revision'], 1)
        self.assertEqual(self.call('validate')[0], 0)

    def test_init_never_overwrites_existing_state(self):
        self.init(); before = self.state_path.read_bytes()
        self.assertEqual(self.call('init', '--contract', self.contract_path)[0], 2)
        self.assertEqual(before, self.state_path.read_bytes())

    def test_revision_conflict_and_unknown_fields_preserve_data(self):
        self.init(); before = self.state_path.read_bytes()
        self.assertEqual(self.update({'status': 'running'}, revision=7)[0], 3)
        self.assertEqual(self.update({'execute': 'git push'})[0], 2)
        self.assertEqual(before, self.state_path.read_bytes())

    def test_invalid_terminal_transition_and_missing_evidence(self):
        self.init()
        self.assertEqual(self.update({'status': 'completed'})[0], 2)
        self.assertEqual(self.update({'status': 'running'})[0], 0)
        self.assertEqual(self.update({'status': 'completed'}, 1)[0], 4)
        self.assertEqual(self.update({'status': 'cancelled'}, 1)[0], 0)
        self.assertEqual(self.update({'status': 'running'}, 2)[0], 2)

    def test_corrupt_or_unknown_state_is_not_reset(self):
        self.init()
        for raw in ('{broken', json.dumps({'schema_version': 99})):
            self.state_path.write_text(raw)
            self.assertEqual(self.call('show')[0], 4)
            self.assertEqual(self.update({'status': 'running'})[0], 4)
            self.assertEqual(self.state_path.read_text(), raw)

    def test_malformed_nested_state_is_rejected(self):
        state = self.init()
        for field in ('contract', 'candidate', 'evidence', 'operations'):
            damaged = copy.deepcopy(state); damaged[field] = None
            self.state_path.write_text(json.dumps(damaged))
            self.assertEqual(self.call('validate')[0], 4, field)

    def test_ids_and_contract_paths_cannot_escape(self):
        for task_id in ('../escape', '/tmp/escape', r'..\escape', '.', ''):
            self.assertEqual(self.call('init', '--contract', self.contract_path, task_id=task_id)[0], 2)
        for filename in ('../outside', '/tmp/outside', r'..\outside'):
            value = contract(); value['allowed_paths'] = [filename]
            self.contract_path.write_text(json.dumps(value))
            self.assertEqual(self.call('init', '--contract', self.contract_path)[0], 2)

    def test_state_parent_and_state_file_symlinks_are_rejected(self):
        outside = self.root / 'outside'; outside.mkdir()
        (self.root / '.codex-workflow').symlink_to(outside, target_is_directory=True)
        self.assertEqual(self.call('init', '--contract', self.contract_path)[0], 4)
        self.assertEqual(list(outside.iterdir()), [])
        (self.root / '.codex-workflow').unlink()
        self.init(); self.state_path.unlink()
        target = outside / 'victim'; target.write_text('preserve')
        self.state_path.symlink_to(target)
        self.assertEqual(self.call('show')[0], 4)
        self.assertEqual(self.update({'status': 'running'})[0], 4)
        self.assertEqual(target.read_text(), 'preserve')

    def test_candidate_symlink_is_not_read(self):
        (self.root / 'code.py').unlink()
        outside = self.root / 'outside.txt'; outside.write_text('not scoped')
        (self.root / 'code.py').symlink_to(outside)
        self.assertEqual(self.call('init', '--contract', self.contract_path)[0], 4)

    def test_stale_or_unknown_lock_is_preserved(self):
        self.init()
        lock = self.state_path.parent / '.lock'
        for value in ('broken lock', json.dumps({'pid': 99999999, 'task_id': 'T-001', 'token': 'old'})):
            lock.write_text(value)
            code, result = self.update({'status': 'running'})
            self.assertEqual(code, 3)
            if value.startswith('{'):
                self.assertIn('process=dead', result['errors'][0])
            self.assertEqual(lock.read_text(), value)
            self.assertEqual(self.call('show')[0], 0)
            lock.unlink()

    def test_two_writers_cannot_silently_overwrite(self):
        self.init()
        path = self.root / 'patch.json'; path.write_text(json.dumps({'status': 'running'}))
        args = [sys.executable, str(SCRIPT), 'update', '--project-root', str(self.root), '--task-id', 'T-001',
                '--expected-revision', '0', '--patch-file', str(path)]
        processes = [subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) for _ in range(2)]
        results = []
        for process in processes:
            out, err = process.communicate(timeout=15)
            results.append(process.returncode)
            self.assertTrue(out, err)
        self.assertEqual(sorted(results), [0, 3])
        self.assertEqual(self.call('show')[1]['revision'], 1)

    def test_replace_failure_retains_original_bytes(self):
        self.init(); original = self.state_path.read_bytes()
        spec = importlib.util.spec_from_file_location('task_state', SCRIPT)
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        with patch.object(module.os, 'replace', side_effect=OSError('injected before replacement')):
            with self.assertRaises(module.StateError):
                module.operate(self.root, 'T-001', 'update', patch={'status': 'running'}, expected_revision=0)
        self.assertEqual(self.state_path.read_bytes(), original)
        self.assertFalse((self.state_path.parent / '.lock').exists())
        self.assertEqual(self.call('validate')[0], 0)

    def test_unresolved_operation_is_saved_without_replay(self):
        self.init()
        operation = {'id': 'op-1', 'action': 'package', 'target': 'artifact.zip', 'status': 'unknown', 'evidence_ids': []}
        code, result = self.update({'status': 'running', 'operations': [operation]})
        self.assertEqual(code, 0, result)
        self.assertEqual(result['state']['operations'], [operation])
        self.assertFalse((self.root / 'artifact.zip').exists())
        self.assertEqual(self.update({'status': 'completed'}, 1)[0], 4)

    def test_candidate_drift_is_detected_and_refresh_does_not_grant_actions(self):
        original = self.init()
        (self.root / 'code.py').write_text('value = 2\n')
        self.assertEqual(self.call('validate')[0], 4)
        code, result = self.update({'status': 'running'})
        self.assertEqual(code, 0, result)
        self.assertNotEqual(original['candidate']['fingerprint'], result['state']['candidate']['fingerprint'])
        self.assertEqual(result['state']['contract']['authorization'], original['contract']['authorization'])

    def test_english_and_chinese_tools_match(self):
        self.assertEqual(SCRIPT.read_bytes(), ENGLISH.read_bytes())

    def proof(self, state, result='pass'):
        path = self.state_path.parent / 'evidence/check.log'
        path.parent.mkdir(exist_ok=True)
        path.write_text('actual local test output\n')
        return {'id': 'E1', 'acceptance_id': 'AC-1', 'command': 'local check',
                'environment': 'local-fixture', 'recorded_at': '2026-10-07T00:00:00+00:00',
                'result': result, 'path': str(path.relative_to(self.root)),
                'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                'candidate_fingerprint': state['candidate']['fingerprint']}

    def test_valid_completion_and_evidence_tampering(self):
        state = self.init(); proof = self.proof(state)
        self.assertEqual(self.update({'status': 'running', 'environment': 'local-fixture', 'evidence': [proof]})[0], 0)
        code, result = self.update({'status': 'completed', 'phase': 'delivery'}, 1)
        self.assertEqual(code, 0, result)
        self.assertEqual(self.call('validate')[0], 0)
        (self.root / proof['path']).write_text('changed output')
        self.assertEqual(self.call('validate')[0], 4)

    def test_process_exit_before_and_after_replace_keeps_whole_state_and_lock(self):
        self.init()
        original = self.state_path.read_bytes()
        for after in (False, True):
            self.state_path.write_bytes(original)
            code = '''import importlib.util, os, sys
spec=importlib.util.spec_from_file_location('state', sys.argv[1])
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
replace=m.os.replace
def crash(*args, **kwargs):
    if sys.argv[3] == 'True': replace(*args, **kwargs)
    os._exit(79)
m.os.replace=crash
m.operate(sys.argv[2], 'T-001', 'update', patch={'status':'running'}, expected_revision=0)
'''
            child = subprocess.run([sys.executable, '-c', code, str(SCRIPT), str(self.root), str(after)], capture_output=True)
            self.assertEqual(child.returncode, 79, child.stderr)
            saved = json.loads(self.state_path.read_text())
            self.assertEqual(saved['revision'], 1 if after else 0)
            self.assertEqual(self.call('validate')[0], 0)
            self.assertTrue((self.state_path.parent / '.lock').exists())
            self.assertEqual(self.update({'status': 'running'}, saved['revision'])[0], 3)
            (self.state_path.parent / '.lock').unlink()  # Test-owned fixture; never a tool unlock path.

    def test_failed_evidence_cannot_be_removed_or_rewritten(self):
        state = self.init(); proof = self.proof(state, result='fail')
        self.assertEqual(self.update({'status': 'running', 'evidence': [proof]})[0], 0)
        self.assertEqual(self.update({'evidence': []}, 1)[0], 2)
        altered = dict(proof, result='pass')
        self.assertEqual(self.update({'evidence': [altered]}, 1)[0], 2)

    def recovery_event(self, state, kind='failure', category='implementation', message='assertion failed', proof_check='normalize-test'):
        number = len(state['evidence']) + 1
        path = self.state_path.parent / f'evidence/recovery-{number}.log'
        path.parent.mkdir(exist_ok=True)
        path.write_text(message + '\n')
        evidence = {'id': f'E{number}', 'acceptance_id': 'AC-1', 'command': 'python3 test_code.py',
                    'environment': 'local-fixture', 'recorded_at': '2026-10-07T00:00:00+00:00',
                    'result': 'pass' if kind == 'resolved' else 'fail', 'check_id': proof_check,
                    'path': str(path.relative_to(self.root)), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                    'candidate_fingerprint': state['candidate']['fingerprint']}
        event = {'id': f'R{number}', 'acceptance_id': 'AC-1', 'check_id': 'normalize-test',
                 'scope': ['code.py'], 'kind': kind, 'category': category, 'evidence_id': evidence['id'],
                 'message': message, 'expectation_ref': 'TASK.md:TDD-red' if kind == 'expected_red' else None}
        events = state['recovery'].get('events', []) + [event]
        return self.update({'status': 'running', 'environment': 'local-fixture',
                            'evidence': state['evidence'] + [evidence], 'recovery': {'events': events}}, state['revision'])

    def test_recovery_rejects_another_checks_evidence_without_changing_state(self):
        state = self.init()
        before = self.state_path.read_bytes()
        self.assertEqual(self.recovery_event(state, proof_check='different-check')[0], 2)
        self.assertEqual(before, self.state_path.read_bytes())
        _, failed = self.recovery_event(state)
        before = self.state_path.read_bytes()
        self.assertEqual(self.recovery_event(failed['state'], kind='resolved', proof_check='different-check')[0], 2)
        self.assertEqual(before, self.state_path.read_bytes())
        self.assertEqual(self.recovery_event(failed['state'], kind='resolved')[0], 0)

    def test_repair_limit_keeps_third_failure_and_stops_without_resetting_wording(self):
        state = self.init()
        for number in range(3):
            (self.root / 'code.py').write_text(f'value = {number + 2}\n')
            code, changed = self.update({'next_step': 'recheck'}, state['revision'])
            self.assertEqual(code, 0, changed)
            code, result = self.recovery_event(changed['state'], message=f'new wording {number}')
            self.assertEqual(code, 0, result)
            state = result['state']
            check = state['recovery']['assessment'][0]
            self.assertEqual(check['failures'], number + 1)
            self.assertEqual(check['next_action'], 'blocked' if number == 2 else 'repair')
        self.assertEqual(len(state['recovery']['events']), 3)
        self.assertEqual(self.update({'recovery': {}}, state['revision'])[0], 2)
        self.assertEqual(self.call('validate')[0], 0)

    def test_identical_candidate_failure_stops_early_even_if_category_changes(self):
        state = self.init()
        code, first = self.recovery_event(state)
        self.assertEqual(code, 0, first)
        code, second = self.recovery_event(first['state'], category='transient', message='different words')
        self.assertEqual(code, 0, second)
        self.assertEqual(second['state']['recovery']['assessment'][0]['next_action'], 'blocked')

    def test_unrelated_file_change_is_not_repair_progress(self):
        value = contract(); value['allowed_paths'].append('unrelated.txt')
        self.contract_path.write_text(json.dumps(value))
        _, first = self.recovery_event(self.init())
        (self.root / 'unrelated.txt').write_text('unrelated documentation change')
        _, changed = self.update({'next_step': 'recheck'}, first['revision'])
        code, second = self.recovery_event(changed['state'])
        self.assertEqual(code, 0, second)
        self.assertEqual(second['state']['recovery']['assessment'][0]['next_action'], 'blocked')

    def test_expected_red_does_not_consume_repairs_and_success_returns_original_ac(self):
        state = self.init()
        code, red = self.recovery_event(state, kind='expected_red')
        self.assertEqual(code, 0, red)
        self.assertEqual(red['state']['recovery']['assessment'][0]['failures'], 0)
        self.assertEqual(red['state']['recovery']['assessment'][0]['next_action'], 'implement')
        (self.root / 'code.py').write_text('value = 2\n')
        _, changed = self.update({'next_step': 'green'}, red['revision'])
        code, green = self.recovery_event(changed['state'], kind='resolved')
        self.assertEqual(code, 0, green)
        check = green['state']['recovery']['assessment'][0]
        self.assertEqual((check['acceptance_id'], check['next_action']), ('AC-1', 'clear'))
        self.assertEqual(self.update({'status': 'completed', 'phase': 'delivery'}, green['revision'])[0], 0)

    def test_permission_dependency_and_decision_have_distinct_recovery(self):
        state = self.init()
        for index, (category, action) in enumerate((('permission', 'blocked'), ('dependency', 'wait_dependency'),
                                                   ('decision', 'wait_user'), ('resource', 'blocked'))):
            code, result = self.recovery_event(state, category=category)
            self.assertEqual(code, 0, result)
            self.assertEqual(result['state']['recovery']['assessment'][0]['next_action'], action)
            if index < 3:
                self.state_path.unlink()  # Independent test task; production init cannot reset.
                state = self.init()

    def test_failure_cannot_be_relabelled_as_tdd_or_assessment_forged(self):
        state = self.init(); _, first = self.recovery_event(state)
        self.assertEqual(self.recovery_event(first['state'], kind='expected_red')[0], 2)
        recovery = copy.deepcopy(first['state']['recovery'])
        recovery['assessment'] = [{'next_action': 'clear'}]
        code, result = self.update({'recovery': recovery}, first['revision'])
        self.assertEqual(code, 0, result)
        self.assertEqual(result['state']['recovery']['assessment'][0]['next_action'], 'repair')

    def test_unresolved_failure_prevents_completion_despite_unrelated_pass(self):
        state = self.init(); _, failed = self.recovery_event(state)
        proof = self.proof(failed['state']); proof['id'] = 'other-pass'
        _, checked = self.update({'evidence': failed['state']['evidence'] + [proof]}, failed['revision'])
        self.assertEqual(self.update({'status': 'completed', 'phase': 'delivery'}, checked['revision'])[0], 4)

    def test_recovery_requires_real_evidence_and_valid_scope(self):
        state = self.init(); _, result = self.recovery_event(state)
        recovery = copy.deepcopy(result['state']['recovery'])
        bad = dict(recovery['events'][0], id='fake', evidence_id='missing')
        recovery['events'].append(bad)
        self.assertEqual(self.update({'recovery': recovery}, result['revision'])[0], 2)

    def test_zero_repair_budget_blocks_initial_failure(self):
        value = contract(); value['limits']['max_repair_rounds'] = 0
        self.contract_path.write_text(json.dumps(value))
        _, result = self.recovery_event(self.init())
        self.assertEqual(result['state']['recovery']['assessment'][0]['next_action'], 'blocked')

    def test_unknown_operation_cannot_be_reset_to_prepared(self):
        self.init()
        operation = {'id': 'op-1', 'action': 'package', 'target': 'out.zip', 'status': 'unknown', 'evidence_ids': []}
        self.assertEqual(self.update({'status': 'running', 'operations': [operation]})[0], 0)
        self.assertEqual(self.update({'operations': [dict(operation, status='prepared')]}, 1)[0], 2)

    def test_contract_change_needs_an_explicit_source_and_retains_history(self):
        self.init(); revised = contract(); revised['goal'] = 'Revised goal'
        self.assertEqual(self.update({'contract': revised})[0], 2)
        revised['authorization']['sources'].append({'id': 'U2', 'reference': 'user:scope-correction', 'quote': 'Correct this goal; no new external actions.'})
        code, result = self.update({'contract': revised, 'contract_change_source': 'U2'})
        self.assertEqual(code, 0, result)
        self.assertEqual(result['state']['contract_changes'][0]['source_id'], 'U2')
        self.assertFalse((self.root / 'out.zip').exists())

    def test_invalid_input_types_use_input_error_not_filesystem_error(self):
        value = contract(); value['delivery_endpoint'] = []
        self.contract_path.write_text(json.dumps(value))
        self.assertEqual(self.call('init', '--contract', self.contract_path)[0], 2)
        self.contract_path.write_text(json.dumps(contract())); self.init()
        self.assertEqual(self.update({'status': []})[0], 2)
        self.assertEqual(self.update({'phase': 'invented'})[0], 2)

    def test_evidence_symlink_and_operation_result_without_proof_are_rejected(self):
        state = self.init(); proof = self.proof(state)
        path = self.root / proof['path']; content = path.read_bytes(); path.unlink()
        outside = self.root / 'outside-evidence'; outside.write_bytes(content); path.symlink_to(outside)
        self.assertEqual(self.update({'status': 'running', 'evidence': [proof]})[0], 4)
        path.unlink(); path.write_bytes(content)
        operation = {'id': 'op-1', 'action': 'push', 'target': 'local-fixture', 'status': 'confirmed', 'evidence_ids': []}
        self.assertNotEqual(self.update({'status': 'running', 'operations': [operation]})[0], 0)

    def test_git_candidate_records_and_checks_actual_head(self):
        def git(*args):
            return subprocess.run(['git', '-C', str(self.root), *args], check=True, capture_output=True, text=True).stdout.strip()
        git('init', '-b', 'fixture'); git('config', 'user.name', 'State Test'); git('config', 'user.email', 'test@example.invalid')
        git('add', '--', 'code.py'); git('commit', '-m', 'fixture baseline')
        state = self.init()
        self.assertEqual(state['candidate']['kind'], 'git')
        self.assertEqual(state['candidate']['head'], git('rev-parse', 'HEAD'))
        self.assertEqual(state['candidate']['branch'], 'fixture')
        (self.root / 'code.py').write_text('value = 2\n')
        git('add', '--', 'code.py'); git('commit', '-m', 'fixture next candidate')
        self.assertEqual(self.call('validate')[0], 4)

    def test_candidate_record_internal_corruption_is_rejected(self):
        state = self.init(); state['candidate']['fingerprint'] = 'incorrect'
        self.state_path.write_text(json.dumps(state))
        self.assertEqual(self.call('show')[0], 4)


if __name__ == '__main__':
    unittest.main()
