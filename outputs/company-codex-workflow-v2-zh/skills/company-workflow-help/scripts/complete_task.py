#!/usr/bin/env python3
"""Complete local prepare tasks without duplicate phase/environment input."""
import copy
import json
import sys
# 普通调用也不向插件目录写字节码；加载后恢复调用方设置。
_previous_bytecode_setting = sys.dont_write_bytecode
try:
    sys.dont_write_bytecode = True
    import task_state as state_tool
finally:
    sys.dont_write_bytecode = _previous_bytecode_setting


def complete(root, task_id, revision, submission):
    state = state_tool.operate(root, task_id, 'show')
    need = state_tool.require
    need(revision == state['revision'], 'revision conflict; reload before completion', 3)
    need(state['status'] == 'running', 'completion requires an explicitly running task')
    need(state['phase'] in ('validation', 'delivery'), 'completion requires validation or delivery phase')
    need(state['contract']['delivery_endpoint'] == 'prepare', 'completion entry supports local prepare only')
    need(not any(x.get('external') for x in state['contract']['acceptance']),
         'external acceptance is outside this completion entry')
    need(state_tool.nonempty(state['environment']), 'missing recorded environment')
    allowed = {'evidence', 'completed_items', 'current_task', 'next_step'}
    need(isinstance(submission, dict) and set(submission) <= allowed, 'unsupported submission field')
    additions = copy.deepcopy(submission.get('evidence', []))
    need(isinstance(additions, list), 'new evidence must be a list')
    # 仅补全新证据省略的环境；显式冲突不能靠改标签通过。
    for proof in additions:
        need(isinstance(proof, dict), 'new evidence must be an object')
        need(not proof.get('external'), 'external evidence is outside this completion entry')
        need('environment' not in proof or proof['environment'] == state['environment'],
             'explicit environment mismatch; recheck actual environment, do not relabel evidence')
        proof.setdefault('environment', state['environment'])
    patch = copy.deepcopy(submission)
    # 保留历史完成项，提交只包含本次新增项。
    if 'completed_items' in submission:
        need(state_tool.strings(submission['completed_items']), 'invalid new completed items')
        patch['completed_items'] = state['completed_items'] + submission['completed_items']
    patch.update(phase='delivery', status='completed', evidence=state['evidence'] + additions)
    # 复用原工具的锁、revision 和完成门禁；show 后的并发修改仍被拒绝。
    return state_tool.operate(root, task_id, 'update', patch=patch, expected_revision=revision)


def main():
    task_id = None
    try:
        parser = state_tool.Parser(description=__doc__)
        parser.add_argument('--project-root', required=True)
        parser.add_argument('--task-id', required=True)
        parser.add_argument('--expected-revision', type=int, required=True)
        parser.add_argument('--submission', required=True)
        args = parser.parse_args(); task_id = args.task_id
        state = complete(args.project_root, task_id, args.expected_revision,
                         state_tool.input_json(args.submission))
        result = dict(ok=True, task_id=task_id, revision=state['revision'],
                      status=state['status'], errors=[], state=state)
        code = 0
    except state_tool.StateError as exc:
        result = dict(ok=False, task_id=task_id, revision=None, status=None, errors=[str(exc)])
        code = exc.code
    print(json.dumps(result, ensure_ascii=False))
    return code


if __name__ == '__main__':
    raise SystemExit(main())
