#!/usr/bin/env python3
"""Collect explicit file identities and saved process metadata; never run checks.

Exit 0: collection succeeded, NOT business acceptance. Exit 2: invalid input;
exit 4: a file, saved check or output failed. Partial results retain all errors.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
from types import SimpleNamespace

STATE_PATH = Path(__file__).resolve().parents[2] / 'company-workflow-help/scripts/task_state.py'
SPEC = importlib.util.spec_from_file_location('workflow_state', STATE_PATH)
state = importlib.util.module_from_spec(SPEC)
# Loading the helper must not write into the installed plugin directory.
_previous_bytecode_setting = sys.dont_write_bytecode
try:
    sys.dont_write_bytecode = True
    SPEC.loader.exec_module(state)
finally:
    sys.dont_write_bytecode = _previous_bytecode_setting


def safe_path(value):
    parts = state.relative(value)
    blocked = {'.git', '.aws', '.ssh', '.gnupg', '.codex', 'credentials', 'credentials.json', 'id_rsa', 'id_ed25519'}
    state.require(not any(p.lower() in blocked or p.lower().startswith('.env') or p.lower().endswith(('.pem', '.key')) for p in parts), 'credential or private metadata path is excluded')
    state.require(parts[:2] != ('.codex-workflow', 'tasks'), 'task-state storage is excluded')
    return parts


def read_file(files, path, capture=False):
    parts = safe_path(path)
    parent = files.directory(parts[:-1])
    try:
        fd = os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent)
    finally:
        os.close(parent)
    with os.fdopen(fd, 'rb') as stream:
        state.require(stat.S_ISREG(os.fstat(stream.fileno()).st_mode), 'only regular files are supported', 4)
        sha = hashlib.sha256(); chunks = []; size = 0
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            sha.update(block); size += len(block)
            if capture:
                state.require(size <= 1024 * 1024, 'JSON capture exceeds 1 MiB', 4)
                chunks.append(block)
    return sha.hexdigest(), b''.join(chunks)


def collect(root, files, manifest):
    report = {'schema_version': 1, 'collected_at': state.now(), 'ok': False,
              'acceptance': 'not_assessed', 'candidate': None, 'files': {}, 'checks': [], 'errors': []}
    state.require(isinstance(manifest, dict) and set(manifest) <= {'paths', 'checks'}, 'expected paths/checks object')
    paths = manifest.get('paths'); checks = manifest.get('checks', [])
    state.require(state.strings(paths, False) and len(paths) == len(set(paths)), 'paths must be a nonempty unique list')
    state.require(isinstance(checks, list), 'checks must be a list')
    for path in paths:
        try:
            report['files'][path] = read_file(files, path)[0]
        except (OSError, state.StateError) as exc:
            report['files'][path] = None
            report['errors'].append({'path': path, 'error': str(exc)})
    if not report['errors']:
        # Reuse the state tool's exact identity/fingerprint format, using the bytes
        # just collected; its only subprocesses are fixed read-only Git queries.
        cached = SimpleNamespace(hash=lambda path, missing=False: report['files'][path])
        try:
            report['candidate'] = state.candidate(cached, root, {'allowed_paths': paths, 'required_artifacts': []})
        except (OSError, subprocess.SubprocessError, state.StateError) as exc:
            report['errors'].append({'error': 'candidate identity unavailable: ' + str(exc)})
    seen = set()
    for check in checks:
        try:
            state.require(isinstance(check, dict) and set(check) == {'id', 'capture_path'} and state.nonempty(check['id']), 'invalid check reference')
            state.require(check['id'] not in seen, 'duplicate check ID'); seen.add(check['id'])
            sha, raw = read_file(files, check['capture_path'], capture=True)
            saved = json.loads(raw)
            state.require(isinstance(saved, dict) and state.strings(saved.get('command'), False)
                          and type(saved.get('check_exit_code')) is int and isinstance(saved.get('stdout'), str)
                          and isinstance(saved.get('stderr'), str), 'invalid process capture')
            report['checks'].append({'id': check['id'], 'capture_path': check['capture_path'], 'sha256': sha,
                'check_exit_code': saved['check_exit_code'], 'command_sha256': state.digest(state.encoded(saved['command'])),
                'stdout_bytes': len(saved['stdout'].encode()), 'stderr_bytes': len(saved['stderr'].encode()),
                'candidate_binding': 'not_verified'})
            if saved['check_exit_code'] != 0:
                report['errors'].append({'check_id': check['id'], 'error': 'saved check failed', 'check_exit_code': saved['check_exit_code']})
        except (OSError, ValueError, TypeError, state.StateError) as exc:
            report['errors'].append({'check_id': check.get('id') if isinstance(check, dict) else None, 'error': str(exc)})
    report['ok'] = not report['errors']
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project-root', required=True, type=Path)
    parser.add_argument('--paths-file', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args(); files = None
    report = {'ok': False, 'acceptance': 'not_assessed', 'errors': []}; code = 0
    try:
        root = args.project_root.resolve(strict=True); files = state.Files(root)
        def local(path):
            if not path.is_absolute():
                return path.as_posix()
            # macOS /var and /private/var may identify the same selected root.
            # Do not resolve input symlinks: Files still rejects every symlink.
            try:
                return str(path.relative_to(args.project_root.absolute()))
            except ValueError:
                return str(path.relative_to(root))
        source = local(args.paths_file); output = local(args.output); safe_path(source); parts = safe_path(output)
        manifest = json.loads(read_file(files, source, capture=True)[1])
        state.require(isinstance(manifest, dict) and isinstance(manifest.get('paths'), list)
                      and isinstance(manifest.get('checks', []), list), 'expected paths/checks object')
        state.require(output != source and output not in manifest.get('paths', []) and
                      output not in [x.get('capture_path') for x in manifest.get('checks', []) if isinstance(x, dict)], 'output overlaps an input')
        report = collect(root, files, manifest); code = 0 if report['ok'] else 4
        parent = files.directory(parts[:-1], create=True)
        try:
            fd = os.open(parts[-1], os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=parent)
            with os.fdopen(fd, 'wb') as stream:
                stream.write(state.encoded(report)); stream.flush(); os.fsync(stream.fileno())
        finally:
            os.close(parent)
    except (OSError, ValueError, TypeError, AttributeError, state.StateError) as exc:
        report['ok'] = False; report['errors'].append({'error': str(exc)})
        code = exc.code if isinstance(exc, state.StateError) else (2 if isinstance(exc, ValueError) else 4)
    finally:
        if files:
            files.close()
    sys.stdout.buffer.write(state.encoded(report))
    return code


if __name__ == '__main__':
    raise SystemExit(main())
