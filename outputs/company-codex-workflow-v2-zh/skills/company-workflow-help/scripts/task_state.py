#!/usr/bin/env python3
"""Store and validate task records. Never execute recorded commands or grant authority.

Commands: init/show/update/validate. Exit codes: 0 success, 2 input/transition,
3 revision/lock conflict, 4 filesystem/state/evidence error. Updates refresh the
scoped candidate snapshot; existing evidence retains its original binding.
"""
import argparse
import copy
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import uuid


class StateError(Exception):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code


def require(condition, message, code=2):
    if not condition:
        raise StateError(code, message)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def strings(value, allow_empty=True):
    return isinstance(value, list) and (allow_empty or bool(value)) and all(nonempty(x) for x in value)


def relative(value):
    require(nonempty(value), 'expected a nonempty relative file path')
    path = PurePosixPath(value)
    require(not path.is_absolute() and '\\' not in value and ':' not in value
            and '..' not in path.parts and path.parts and path != PurePosixPath('.'), 'unsafe relative path')
    return path.parts


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode()


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat()


class Files:
    """Walk opened directories without following symlinks, including parents."""
    def __init__(self, root):
        require(hasattr(os, 'O_NOFOLLOW') and os.open in os.supports_dir_fd,
                'safe descriptor-relative filesystem operations are unavailable', 4)
        self.fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)

    def close(self):
        os.close(self.fd)

    def directory(self, parts, create=False):
        fd = os.dup(self.fd)
        try:
            for part in parts:
                if create:
                    try:
                        os.mkdir(part, mode=0o700, dir_fd=fd)
                    except FileExistsError:
                        pass
                child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
                os.close(fd)
                fd = child
            return fd
        except BaseException:
            os.close(fd)
            raise

    def open_file(self, path):
        parts = relative(path)
        parent = self.directory(parts[:-1])
        try:
            return os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW, dir_fd=parent)
        finally:
            os.close(parent)

    def read(self, path):
        with os.fdopen(self.open_file(path), 'rb') as stream:
            return stream.read()

    def hash(self, path, missing=False):
        try:
            result = hashlib.sha256()
            with os.fdopen(self.open_file(path), 'rb') as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b''):
                    result.update(block)
            return result.hexdigest()
        except FileNotFoundError:
            if missing:
                return None
            raise


ENDPOINTS = {'inspect', 'plan', 'prepare', 'commit', 'deliver', 'merge', 'deploy', 'production_acceptance'}
PHASES = {'requirements', 'design', 'planning', 'implementation', 'validation', 'delivery'}
TRANSITIONS = {
    'ready': {'ready', 'running', 'waiting_user', 'waiting_dependency', 'blocked', 'cancelled'},
    'running': {'running', 'ready', 'waiting_user', 'waiting_dependency', 'blocked', 'completed', 'cancelled'},
    'waiting_user': {'waiting_user', 'ready', 'running', 'blocked', 'cancelled'},
    'waiting_dependency': {'waiting_dependency', 'ready', 'running', 'blocked', 'cancelled'},
    'blocked': {'blocked', 'ready', 'running', 'waiting_user', 'waiting_dependency', 'cancelled'},
    'completed': set(), 'cancelled': set(),
}
CONTRACT_FIELDS = {'goal', 'allowed_paths', 'excluded', 'spec_refs', 'acceptance', 'delivery_endpoint',
                   'authorization', 'decision_points', 'required_artifacts', 'limits'}
PATCH_FIELDS = {'contract', 'phase', 'status', 'current_task', 'completed_items', 'next_step', 'evidence',
                'operations', 'recovery', 'budget', 'environment', 'milestones', 'contract_change_source'}
ACTIONS = {'read', 'edit', 'test', 'package', 'commit', 'push', 'merge', 'deploy', 'production_write',
           'message', 'automation', 'delegate'}


def check_contract(value):
    require(isinstance(value, dict) and set(value) == CONTRACT_FIELDS, 'invalid contract fields')
    require(nonempty(value['goal']), 'missing goal')
    for key in ('allowed_paths', 'excluded', 'spec_refs', 'decision_points', 'required_artifacts'):
        require(strings(value[key], allow_empty=key != 'spec_refs'), 'invalid contract ' + key)
    for path in value['allowed_paths'] + value['required_artifacts']:
        parts = relative(path)
        require(parts[0] != '.git' and parts[:2] != ('.codex-workflow', 'tasks'), 'candidate cannot include Git or task-state storage')
    require(nonempty(value['delivery_endpoint']) and value['delivery_endpoint'] in ENDPOINTS, 'unknown delivery endpoint')
    acceptance = value['acceptance']
    require(isinstance(acceptance, list) and acceptance, 'missing acceptance requirements')
    ids = []
    for item in acceptance:
        require(isinstance(item, dict) and nonempty(item.get('id')) and nonempty(item.get('reference'))
                and type(item.get('required')) is bool, 'invalid acceptance requirement')
        require('check_ids' not in item or strings(item['check_ids'], False)
                and len(set(item['check_ids'])) == len(item['check_ids']), 'invalid required check mapping')
        require(type(item.get('external', False)) is bool, 'invalid external acceptance flag')
        ids.append(item['id'])
    require(len(ids) == len(set(ids)), 'duplicate acceptance ID')
    auth = value['authorization']
    require(isinstance(auth, dict) and isinstance(auth.get('sources'), list) and auth['sources']
            and isinstance(auth.get('actions'), list), 'missing authority sources/actions')
    sources = []
    for source in auth['sources']:
        require(isinstance(source, dict) and all(nonempty(source.get(k)) for k in ('id', 'reference', 'quote')),
                'invalid authority source')
        require(not source['reference'].startswith('Example only:'), 'replace example authority with actual source')
        sources.append(source['id'])
    require(len(sources) == len(set(sources)), 'duplicate authority source ID')
    for action in auth['actions']:
        require(isinstance(action, dict) and nonempty(action.get('action')) and action['action'] in ACTIONS and strings(action.get('scope'), False)
                and strings(action.get('source_ids'), False) and set(action['source_ids']) <= set(sources),
                'action lacks a valid scope/source reference')
    limits = value['limits']
    require(isinstance(limits, dict) and type(limits.get('max_repair_rounds')) is int
            and 0 <= limits['max_repair_rounds'] <= 2, 'repair limit must be 0, 1 or 2')
    require(limits.get('token_budget') is None or type(limits['token_budget']) is int and limits['token_budget'] > 0,
            'invalid token budget')
    require(limits.get('deadline') is None or nonempty(limits['deadline']), 'invalid deadline')


def candidate(files, root, contract):
    paths = sorted(set(contract['allowed_paths'] + contract['required_artifacts']))
    hashes = {path: files.hash(path, missing=True) for path in paths}
    identity = {'kind': 'artifact', 'branch': None, 'head': None, 'files': hashes}
    try:
        head = subprocess.run(['git', '-C', str(root), 'rev-parse', '--verify', 'HEAD'],
                              text=True, capture_output=True, timeout=5)
        if head.returncode == 0:
            branch = subprocess.run(['git', '-C', str(root), 'symbolic-ref', '--quiet', '--short', 'HEAD'],
                                    text=True, capture_output=True, timeout=5)
            identity.update(kind='git', head=head.stdout.strip(), branch=branch.stdout.strip() or None)
    except FileNotFoundError:
        require(not (root / '.git').exists(), 'Git is required to inspect this candidate', 4)
    identity['fingerprint'] = digest(encoded(identity))
    return identity


def recovery_assessment(state):
    """Derive per-check advice, not permission to execute or retry any command."""
    events = state['recovery'].get('events', [])
    require(isinstance(events, list), 'invalid recovery events')
    evidence = {item['id']: item for item in state['evidence']}
    acceptance = {item['id'] for item in state['contract']['acceptance']}
    groups = {}; ids = set(); used_evidence = set()
    categories = {'implementation', 'transient', 'dependency', 'decision', 'permission', 'consistency', 'resource'}
    for event in events:
        require(isinstance(event, dict) and all(nonempty(event.get(k)) for k in
                ('id', 'acceptance_id', 'check_id', 'category', 'evidence_id', 'message')),
                'incomplete recovery event')
        require(event['id'] not in ids and event['evidence_id'] not in used_evidence,
                'duplicate recovery event/evidence')
        require(event['acceptance_id'] in acceptance and event['category'] in categories
                and event.get('kind') in ('failure', 'expected_red', 'resolved'), 'invalid recovery classification')
        require(strings(event.get('scope'), False) and len(set(event['scope'])) == len(event['scope'])
                and set(event['scope']) <= set(state['contract']['allowed_paths']), 'invalid recovery scope')
        require(nonempty(event.get('scope_fingerprint')), 'missing recovery scope fingerprint')
        proof = evidence.get(event['evidence_id'])
        require(proof is not None and proof['acceptance_id'] == event['acceptance_id']
                and proof.get('check_id', proof['command']) == event['check_id'],
                'recovery needs original AC and check evidence')
        ids.add(event['id']); used_evidence.add(event['evidence_id'])
        key = (event['acceptance_id'], event['check_id'], tuple(sorted(event['scope'])))
        group = groups.setdefault(key, {'acceptance_id': key[0], 'check_id': key[1], 'scope': list(key[2]),
                                      'failures': 0, 'next_action': 'clear', 'last_failure_scope': None})
        kind = event['kind']
        if kind == 'resolved':
            require(proof['result'] == 'pass' and group['next_action'] != 'clear', 'resolution needs a pending check and passing evidence')
            group['next_action'] = 'clear'
        else:
            require(proof['result'] in ('fail', 'blocked', 'unknown'), 'failure event needs nonpassing evidence')
            if kind == 'expected_red':
                require(group['failures'] == 0 and nonempty(event.get('expectation_ref'))
                        and event['category'] == 'implementation', 'expected red must precede faults and cite the prior TDD expectation')
                group['next_action'] = 'implement'
            else:
                group['failures'] += 1
                if group['next_action'] != 'blocked':
                    group['next_action'] = {'dependency': 'wait_dependency', 'decision': 'wait_user',
                                            'implementation': 'repair', 'transient': 'retry_read_only'}.get(event['category'], 'blocked')
                    if group['failures'] > state['contract']['limits']['max_repair_rounds']:
                        group['next_action'] = 'blocked'
                    if (event['category'] == 'implementation' or group.get('last_category') == 'implementation') and group['last_failure_scope'] == event['scope_fingerprint']:
                        group['next_action'] = 'blocked'
                group['last_failure_scope'] = event['scope_fingerprint']
                group['last_category'] = event['category']
        group['last_event_id'] = event['id']
    return list(groups.values())


def acceptance_fingerprint(state, acceptance_id):
    requirement = next((item for item in state['contract']['acceptance'] if item['id'] == acceptance_id), None)
    return digest(encoded({'requirement': requirement, 'spec_refs': state['contract']['spec_refs']}))


def bind_new_evidence(state, previous_count, previous_updated_at):
    """Bind declared inputs, never infer whether a check or its claimed scope is truthful."""
    ids = {item['id'] for item in state['contract']['acceptance']}
    for proof in state['evidence'][previous_count:]:
        require(proof['acceptance_id'] in ids, 'evidence references an unknown AC')
        proof['recorded_revision'] = state['revision']
        if proof.get('external'):
            proof['observation_window_start'] = previous_updated_at
        current = proof['candidate_fingerprint'] == state['candidate']['fingerprint']
        if 'scope' in proof:
            require(current, 'scoped evidence must bind the current candidate')
            require(strings(proof['scope'], False) and set(proof['scope']) <= set(state['candidate']['files']),
                    'evidence scope is outside the candidate')
            proof['inputs'] = {path: state['candidate']['files'][path] for path in proof['scope']}
        else:
            proof.pop('inputs', None)
        if current:
            proof['acceptance_fingerprint'] = acceptance_fingerprint(state, proof['acceptance_id'])
        else:
            proof.pop('acceptance_fingerprint', None)


def applicable(state, proof):
    if proof['environment'] != state['environment']:
        return False
    binding = proof.get('acceptance_fingerprint')
    if binding is None:
        if state['contract_changes']:
            return False  # Legacy evidence did not bind acceptance semantics.
    elif binding != acceptance_fingerprint(state, proof['acceptance_id']):
        return False
    if 'scope' in proof:
        return set(proof['scope']) <= set(state['candidate']['files']) and proof['inputs'] == {
            path: state['candidate']['files'][path] for path in proof['scope']}
    return proof['candidate_fingerprint'] == state['candidate']['fingerprint']


def fresh_external(state, proof):
    try:
        times = [datetime.fromisoformat(value.replace('Z', '+00:00')) for value in
                 (proof['observation_window_start'], proof['recorded_at'], state['updated_at'])]
        return all(value.tzinfo is not None for value in times) and times[0] <= times[1] <= times[2]
    except (KeyError, ValueError, TypeError, AttributeError):
        return False


def check_state(state, root, task_id, input_record=False):
    require(isinstance(state, dict) and type(state.get('schema_version')) is int and state['schema_version'] == 1, 'unknown or corrupt state schema', 4)
    try:
        require(state['task_id'] == task_id and state['project_root'] == str(root), 'state identity mismatch', 4)
        require(type(state['revision']) is int and state['revision'] >= 0 and nonempty(state['updated_at']), 'invalid state revision/time', 4)
        check_contract(state['contract'])
        require(state['status'] in TRANSITIONS and state['phase'] in PHASES, 'invalid state status/phase', 4)
        require(isinstance(state['candidate'], dict) and isinstance(state['candidate']['files'], dict)
                and nonempty(state['candidate']['fingerprint']), 'invalid candidate', 4)
        snapshot = {key: value for key, value in state['candidate'].items() if key != 'fingerprint'}
        require(digest(encoded(snapshot)) == state['candidate']['fingerprint'], 'candidate record checksum mismatch', 4)
        require(strings(state['completed_items']) and isinstance(state['current_task'], str)
                and isinstance(state['next_step'], str), 'invalid progress fields', 4)
        require(state['environment'] is None or nonempty(state['environment']), 'invalid environment', 4)
        require(isinstance(state['budget'], dict) and isinstance(state['recovery'], dict)
                and isinstance(state['milestones'], dict), 'invalid recovery/budget/milestones', 4)
        require(isinstance(state['contract_changes'], list), 'invalid contract change history', 4)
        require(isinstance(state['evidence'], list) and isinstance(state['operations'], list), 'invalid evidence/operations', 4)
        ids = set()
        for evidence in state['evidence']:
            require(isinstance(evidence, dict) and all(nonempty(evidence.get(k)) for k in
                    ('id', 'acceptance_id', 'command', 'environment', 'recorded_at', 'path', 'sha256', 'candidate_fingerprint')),
                    'incomplete evidence', 4)
            relative(evidence['path'])
            require(evidence['id'] not in ids and evidence.get('result') in ('pass', 'fail', 'blocked', 'skipped', 'unknown'), 'duplicate/invalid evidence', 4)
            require(type(evidence.get('external', False)) is bool
                    and ('check_id' not in evidence or nonempty(evidence['check_id'])), 'invalid evidence check metadata', 4)
            if 'scope' in evidence:
                require(strings(evidence['scope'], False), 'invalid evidence scope', 4)
                for scoped_path in evidence['scope']:
                    relative(scoped_path)
                if not input_record:
                    require(isinstance(evidence.get('inputs'), dict) and set(evidence['inputs']) == set(evidence['scope']),
                            'missing scoped evidence binding', 4)
                    require(all(value is None or isinstance(value, str) and re.fullmatch(r'[a-f0-9]{64}', value)
                                for value in evidence['inputs'].values()), 'invalid evidence input hash', 4)
            if not input_record and 'recorded_revision' in evidence:
                require(type(evidence['recorded_revision']) is int and 0 <= evidence['recorded_revision'] <= state['revision'],
                        'invalid evidence revision', 4)
            ids.add(evidence['id'])
        operations = set()
        for operation in state['operations']:
            require(isinstance(operation, dict) and all(nonempty(operation.get(k)) for k in ('id', 'action', 'target'))
                    and operation.get('status') in ('prepared', 'unknown', 'confirmed', 'failed')
                    and strings(operation.get('evidence_ids')), 'invalid operation record', 4)
            require(operation['id'] not in operations and set(operation['evidence_ids']) <= ids, 'duplicate operation or unknown evidence', 4)
            require(operation['status'] not in ('confirmed', 'failed') or bool(operation['evidence_ids']), 'operation result needs original evidence', 4)
            operations.add(operation['id'])
        assessment = recovery_assessment(state)
        require(state['recovery'].get('assessment', []) == assessment, 'recovery assessment mismatch', 4)
    except (KeyError, TypeError, AttributeError, StateError) as exc:
        raise StateError(2 if input_record else 4, 'invalid state: ' + str(exc)) from exc


def evidence_checks(files, state, complete=False):
    for item in state['evidence']:
        require(files.hash(item['path']) == item['sha256'], 'missing or changed evidence: ' + item['id'], 4)
    if not complete:
        return
    require(state['phase'] == 'delivery', 'completion requires delivery phase', 4)
    require(state['environment'] is not None, 'completion needs a recorded environment', 4)
    require(not state['contract']['decision_points'], 'unresolved decision points', 4)
    require(not state['recovery'].get('blocker'), 'unresolved blocker', 4)
    require(all(item['next_action'] == 'clear' for item in recovery_assessment(state)), 'unresolved recovery check', 4)
    require(all(op['status'] not in ('prepared', 'unknown') for op in state['operations']), 'unresolved operation; query actual result before replay', 4)
    for required in state['contract']['acceptance']:
        if required['required']:
            latest = {}
            for proof in state['evidence']:
                if proof['acceptance_id'] == required['id']:
                    latest[proof.get('check_id', proof['command'])] = proof
            checks = required.get('check_ids', list(latest))
            require(bool(checks), 'missing evidence: ' + required['id'], 4)
            for check in checks:
                proof = latest.get(check)
                require(proof is not None and proof['result'] == 'pass' and applicable(state, proof),
                        'missing applicable passing evidence: ' + required['id'] + '/' + check, 4)
                if required.get('external') or proof.get('external'):
                    require(proof.get('external') and proof.get('recorded_revision') == state['revision']
                            and fresh_external(state, proof),
                            'external check must be freshly observed and appended at completion: ' + check, 4)
    for path in state['contract']['required_artifacts']:
        require(files.hash(path, missing=True) is not None, 'missing required artifact: ' + path, 4)
    endpoint = state['contract']['delivery_endpoint']
    if endpoint not in ('inspect', 'plan', 'prepare'):
        ids = {e['id'] for e in state['evidence'] if e['result'] == 'pass' and applicable(state, e)
               and e['candidate_fingerprint'] == state['candidate']['fingerprint']}
        require(strings(state['milestones'].get(endpoint), False) and set(state['milestones'][endpoint]) <= ids,
                'missing endpoint evidence: ' + endpoint, 4)
        action = {'commit': 'commit', 'deliver': 'push', 'merge': 'merge', 'deploy': 'deploy',
                  'production_acceptance': 'test'}[endpoint]
        authorized_targets = {target for item in state['contract']['authorization']['actions']
                              if item['action'] == action for target in item['scope']}
        require(any(op['action'] == action and op['target'] in authorized_targets and op['status'] == 'confirmed'
                    and set(state['milestones'][endpoint]) <= set(op['evidence_ids']) for op in state['operations']),
                'endpoint needs scoped authority and a confirmed operation with its result evidence: ' + endpoint, 4)


def load_state(files, path, root, task_id):
    try:
        value = json.loads(files.read(path))
    except (ValueError, OSError) as exc:
        raise StateError(4, 'cannot read state; original retained: ' + str(exc)) from exc
    check_state(value, root, task_id)
    return value


def save_atomic(directory, state):
    name = '.state-' + uuid.uuid4().hex + '.tmp'
    try:
        fd = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=directory)
        with os.fdopen(fd, 'wb') as stream:
            stream.write(encoded(state)); stream.flush(); os.fsync(stream.fileno())
        os.replace(name, 'state.json', src_dir_fd=directory, dst_dir_fd=directory)
        os.fsync(directory)
    finally:
        try:
            os.unlink(name, dir_fd=directory)
        except FileNotFoundError:
            pass


def lock_owner(files, folder, task_id):
    try:
        owner = json.loads(files.read(folder + '/.lock'))
        pid = owner.get('pid')
        if type(pid) is not int or pid <= 0:
            return 'owner/process unknown'
        try:
            os.kill(pid, 0)  # Existence probe only; never terminate or unlock.
            process = 'alive'
        except ProcessLookupError:
            process = 'dead'
        except PermissionError:
            process = 'unknown'
        return f'pid={pid}, process={process}, task_matches={owner.get("task_id") == task_id}'
    except (OSError, ValueError, AttributeError, StateError):
        return 'owner/process unknown'


def operate(project_root, task_id, command, contract=None, patch=None, expected_revision=None):
    require(isinstance(task_id, str) and re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,127}', task_id), 'unsafe task ID')
    require(command in ('init', 'show', 'update', 'validate'), 'unknown command')
    files = None; directory = None; lock = None
    try:
        root = Path(project_root).resolve(strict=True)
        files = Files(root)
        folder = '.codex-workflow/tasks/' + task_id
        path = folder + '/state.json'
        if command in ('show', 'validate'):
            state = load_state(files, path, root, task_id)
            if command == 'validate':
                require(candidate(files, root, state['contract']) == state['candidate'], 'candidate changed; recheck affected evidence', 4)
                evidence_checks(files, state, complete=state['status'] == 'completed')
            return state
        if command == 'init':
            check_contract(contract)
        else:
            require(isinstance(patch, dict) and patch and set(patch) <= PATCH_FIELDS, 'unknown or empty update fields')
            require(type(expected_revision) is int and expected_revision >= 0, 'expected revision must be nonnegative integer')
        directory = files.directory(relative(folder), create=command == 'init')
        try:
            fd = os.open('.lock', os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=directory)
        except FileExistsError:
            raise StateError(3, 'task lock exists (' + lock_owner(files, folder, task_id) + '); verify actual state; lock retained')
        lock = encoded({'pid': os.getpid(), 'task_id': task_id, 'token': uuid.uuid4().hex, 'created_at': now()})
        with os.fdopen(fd, 'wb') as stream:
            stream.write(lock); stream.flush(); os.fsync(stream.fileno())
        if command == 'init':
            try:
                files.read(path)
            except FileNotFoundError:
                pass
            else:
                raise StateError(2, 'task already exists; init never overwrites')
            state = {'schema_version': 1, 'task_id': task_id, 'project_root': str(root), 'revision': 0,
                     'updated_at': now(), 'contract': copy.deepcopy(contract), 'phase': 'requirements', 'status': 'ready',
                     'current_task': '', 'completed_items': [], 'next_step': '', 'candidate': candidate(files, root, contract),
                     'evidence': [], 'operations': [], 'recovery': {}, 'budget': {}, 'environment': None,
                     'milestones': {}, 'contract_changes': []}
        else:
            state = load_state(files, path, root, task_id)
            require(state['revision'] == expected_revision, 'revision conflict; reload before updating', 3)
            require(nonempty(patch.get('status', state['status']))
                    and patch.get('status', state['status']) in TRANSITIONS[state['status']], 'invalid status transition')
            previous_ops = {op['id']: op for op in state['operations']}
            previous_evidence = state['evidence']
            previous_contract = state['contract']
            previous_updated_at = state['updated_at']
            previous_recovery = state['recovery'].get('events', [])
            state = copy.deepcopy(state)
            state.update({key: value for key, value in patch.items() if key != 'contract_change_source'})
            require(isinstance(state['evidence'], list) and state['evidence'][:len(previous_evidence)] == previous_evidence,
                    'evidence history is append-only; record a new check instead of rewriting a result')
            require(isinstance(state['recovery'], dict) and isinstance(state['recovery'].get('events', []), list)
                    and state['recovery'].get('events', [])[:len(previous_recovery)] == previous_recovery,
                    'recovery history is append-only; do not reset repair counts')
            current_ops = {op.get('id'): op for op in state['operations']} if isinstance(state['operations'], list) and all(isinstance(op, dict) for op in state['operations']) else {}
            for key, previous in previous_ops.items():
                require(key in current_ops and all(current_ops[key].get(k) == previous[k] for k in ('action', 'target')),
                        'operation identity/history cannot be removed or rewritten')
                require(strings(current_ops[key].get('evidence_ids'))
                        and set(previous['evidence_ids']) <= set(current_ops[key]['evidence_ids']),
                        'operation result evidence references cannot be removed')
                if previous['status'] == 'confirmed':
                    require(current_ops[key].get('status') == 'confirmed', 'confirmed operation cannot be replayed')
                if previous['status'] in ('unknown', 'failed'):
                    require(current_ops[key].get('status') != 'prepared', 'query unresolved results; use a new operation for a verified retry')
            check_contract(state['contract'])
            if state['contract'] != previous_contract:
                source_id = patch.get('contract_change_source')
                sources = {source['id']: source for source in state['contract']['authorization']['sources']}
                require(nonempty(source_id) and source_id in sources, 'contract change requires an explicit real source reference')
                state['contract_changes'].append({'source_id': source_id, 'source': sources[source_id],
                                                  'previous_sha256': digest(encoded(previous_contract)),
                                                  'current_sha256': digest(encoded(state['contract'])), 'recorded_at': now()})
            state['candidate'] = candidate(files, root, state['contract'])
            state['revision'] += 1; state['updated_at'] = now()
        # Validate event/evidence shape before derivation; existing assessment is output only.
        supplied_recovery = state['recovery']
        state['recovery'] = {}
        check_state(state, root, task_id, input_record=True)
        state['recovery'] = supplied_recovery
        bind_new_evidence(state, len(previous_evidence) if command == 'update' else 0,
                          previous_updated_at if command == 'update' else state['updated_at'])
        previous_count = len(previous_recovery) if command == 'update' else 0
        for event in state['recovery'].get('events', [])[previous_count:]:
            require(isinstance(event, dict) and strings(event.get('scope'), False)
                    and set(event['scope']) <= set(state['contract']['allowed_paths']), 'invalid recovery scope')
            event['scope_fingerprint'] = digest(encoded({path: state['candidate']['files'][path] for path in event['scope']}))
        state['recovery']['assessment'] = recovery_assessment(state)
        for event in state['recovery'].get('events', [])[previous_count:]:
            proof = next(item for item in state['evidence'] if item['id'] == event['evidence_id'])
            require(proof['candidate_fingerprint'] == state['candidate']['fingerprint'],
                    'new recovery event needs evidence for the current candidate')
        check_state(state, root, task_id, input_record=True)
        evidence_checks(files, state, complete=state['status'] == 'completed')
        save_atomic(directory, state)
        return state
    except StateError:
        raise
    except (OSError, ValueError, TypeError, KeyError, subprocess.SubprocessError) as exc:
        raise StateError(4, str(exc)) from exc
    finally:
        if lock is not None and files is not None:
            try:
                if files.read(folder + '/.lock') == lock:
                    os.unlink('.lock', dir_fd=directory)
            except (OSError, StateError):
                pass  # Never delete a replaced/unverifiable lock.
        if directory is not None:
            os.close(directory)
        if files is not None:
            files.close()


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise StateError(2, message)


def input_json(path):
    require(path is not None, 'missing JSON input file')
    try:
        return json.loads(Path(path).read_text())
    except (OSError, ValueError) as exc:
        raise StateError(2, 'invalid JSON input: ' + str(exc)) from exc


def main():
    task_id = None
    try:
        parser = Parser(description=__doc__)
        parser.add_argument('command', choices=('init', 'show', 'update', 'validate'))
        parser.add_argument('--project-root', required=True)
        parser.add_argument('--task-id', required=True)
        parser.add_argument('--contract')
        parser.add_argument('--expected-revision', type=int)
        parser.add_argument('--patch-file')
        args = parser.parse_args(); task_id = args.task_id
        state = operate(args.project_root, task_id, args.command,
                        contract=input_json(args.contract) if args.command == 'init' else None,
                        patch=input_json(args.patch_file) if args.command == 'update' else None,
                        expected_revision=args.expected_revision)
        result = {'ok': True, 'task_id': task_id, 'revision': state['revision'], 'status': state['status'], 'errors': [], 'state': state}
        code = 0
    except StateError as exc:
        result = {'ok': False, 'task_id': task_id, 'revision': None, 'status': None, 'errors': [str(exc)]}
        code = exc.code
    print(json.dumps(result, ensure_ascii=False))
    return code


if __name__ == '__main__':
    raise SystemExit(main())
