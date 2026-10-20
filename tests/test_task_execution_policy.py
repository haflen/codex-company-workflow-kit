"""Contract/reference consistency checks; not proof of live authorization behavior."""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
DISTRIBUTIONS = [ROOT / 'outputs' / name for name in (
    'company-codex-workflow-v2-zh', 'company-codex-workflow-v2',
    'company-codex-workflow-template-zh', 'company-codex-workflow-template')]
FIELDS = {'goal', 'allowed_paths', 'excluded', 'spec_refs', 'acceptance',
          'delivery_endpoint', 'authorization', 'decision_points', 'required_artifacts', 'limits'}


def example(root):
    text = (root / 'specs/global/assets/task-contract-template.md').read_text()
    return json.loads(re.search(r'```json\n(.*?)\n```', text, re.S).group(1))


class TaskExecutionPolicyTests(unittest.TestCase):
    def test_contract_examples_share_machine_fields(self):
        for root in DISTRIBUTIONS:
            with self.subTest(root=root.name):
                contract = example(root)
                self.assertEqual(set(contract), FIELDS)
                self.assertTrue(contract['goal'])
                self.assertEqual(contract['delivery_endpoint'], 'prepare')
                self.assertEqual(contract['allowed_paths'], ['labels.py'])
                self.assertTrue(contract['acceptance'][0]['required'])

    def test_actions_cite_existing_user_sources(self):
        for root in DISTRIBUTIONS:
            contract = example(root)
            sources = {source['id']: source for source in contract['authorization']['sources']}
            self.assertTrue(sources)
            for source in sources.values():
                self.assertTrue(source['reference'])
                self.assertTrue(source['quote'])
            for action in contract['authorization']['actions']:
                self.assertTrue(action['source_ids'])
                self.assertTrue(set(action['source_ids']) <= set(sources))
                self.assertTrue(action['scope'])
            self.assertNotIn('push', [a['action'] for a in contract['authorization']['actions']])

    def test_bilingual_distributions_share_contract_shape(self):
        values = [example(root) for root in DISTRIBUTIONS]
        for value in values[1:]:
            self.assertEqual(value, values[0])

    def test_policy_has_all_authority_rules_and_scope_examples(self):
        for root in DISTRIBUTIONS:
            text = (root / 'specs/global/assets/task-execution-policy.md').read_text()
            for rule in range(1, 8):
                self.assertIn(f'AUTH-{rule:02}', text)
            for case in ('READ_ONLY', 'PLAN_ONLY', 'BUILD_PACKAGE', 'EXPLICIT_PUSH', 'MISSING_DECISION'):
                self.assertIn(case, text)

    def test_routing_and_planning_resolve_shared_contract(self):
        for root in DISTRIBUTIONS[:2]:
            for name in ('company-workflow-help', 'company-feature-planning'):
                skill = root / 'skills' / name / 'SKILL.md'
                text = skill.read_text()
                for filename in ('task-execution-policy.md', 'task-contract-template.md'):
                    relative = '../../specs/global/assets/' + filename
                    self.assertIn(relative, text)
                    self.assertTrue((skill.parent / relative).is_file())

    def test_execution_record_references_contract_without_copying_it(self):
        for root in DISTRIBUTIONS:
            text = (root / 'specs/global/assets/execution-record-template.md').read_text()
            self.assertIn('task-contract-template.md', text)
            self.assertIn('state.json', text)
            self.assertNotIn('"authorization":', text)

    def test_planning_does_not_require_repeating_a_handoff_phrase(self):
        for root in DISTRIBUTIONS[:2]:
            text = (root / 'skills/company-feature-planning/SKILL.md').read_text()
            self.assertNotIn('任务规划阶段结束后停止，除非用户给出实现交接口令', text)
            self.assertNotIn('Stop after task planning unless the user gives the implementation handoff signal', text)


class PhaseContinuityTests(unittest.TestCase):
    def test_every_phase_reads_shared_continuity_contract(self):
        names = ('workflow-help', 'feature-requirements', 'feature-design', 'feature-planning',
                 'implementation-runner', 'bugfix-runner', 'quality-validation', 'delivery-closeout', 'thread-handoff')
        for root in DISTRIBUTIONS[:2]:
            for name in names:
                text = (root / 'skills' / ('company-' + name) / 'SKILL.md').read_text()
                self.assertIn('../../specs/global/assets/task-execution-policy.md', text, name)
                self.assertIn('FLOW-', text, name)

    def test_removed_blanket_stop_and_phrase_rules(self):
        banned = ('需求阶段结束后停止。', '设计阶段结束后停止，除非',
                  '必须停下让用户确认', '等用户明确确认新范围并给出实现交接口令',
                  'Stop after requirements.', 'Stop after design unless',
                  'then stop for user confirmation', 'use the implementation handoff phrase before',
                  'must-stop`: `V3`,', '`必须停下`：`V3`，')
        for root in DISTRIBUTIONS[:2]:
            for file in (root / 'skills').glob('company-*/SKILL.md'):
                if file.parent.name in ('company-workflow-help', 'company-feature-requirements', 'company-feature-design',
                                        'company-feature-planning', 'company-implementation-runner'):
                    for old in banned:
                        self.assertNotIn(old, file.read_text(), str(file))

    def test_continuity_table_preserves_decisions_and_validation(self):
        for root in DISTRIBUTIONS:
            policy = (root / 'specs/global/assets/task-execution-policy.md').read_text()
            for rule in range(1, 8):
                self.assertIn(f'FLOW-{rule:02}', policy)
            self.assertIn('API_PENDING', policy)
            self.assertIn('V3', policy)
            self.assertIn('task_state.py', policy)
            self.assertIn('task-execution-policy.md', (root / 'AGENTS.md').read_text())

    def test_host_approval_requirement_is_distinct_from_a_rejected_request(self):
        for root in DISTRIBUTIONS:
            policy = (root / 'specs/global/assets/task-execution-policy.md').read_text()
            for boundary in ('APPROVAL-01', 'approval_required', 'approval_denied',
                             'unknown_effect', 'no_approval_entry'):
                self.assertIn(boundary, policy, str(root))
        for root in DISTRIBUTIONS[:2]:
            closeout = (root / 'skills/company-delivery-closeout/SKILL.md').read_text()
            self.assertIn('APPROVAL-01', closeout)


    def test_context_reading_is_scoped_without_dropping_safety_gates(self):
        for root in DISTRIBUTIONS:
            policy = (root / 'specs/global/assets/task-execution-policy.md').read_text()
            for marker in ('READ-01', 'AUTH-01', 'FLOW-03', 'EVIDENCE-01', 'REPAIR-01', 'APPROVAL-01'):
                self.assertIn(marker, policy)
            self.assertIn('READ-01', (root / 'AGENTS.md').read_text())
        for root in DISTRIBUTIONS[:2]:
            for name in ('workflow-help', 'implementation-runner', 'bugfix-runner', 'context-index'):
                self.assertIn('READ-01', (root / 'skills' / ('company-' + name) / 'SKILL.md').read_text())


    def test_experience_candidates_require_provenance_and_controlled_adoption(self):
        for root in DISTRIBUTIONS:
            template = root / 'specs/global/assets/experience-candidate-template.md'
            self.assertTrue(template.is_file(), str(template))
            text = template.read_text()
            for field in ('source_refs', 'applicability', 'candidate_version', 'counterexamples', 'verification', 'security_review', 'adoption_authority', 'rollback', 'proposed', 'withdrawn'):
                self.assertIn(field, text)
        for root in DISTRIBUTIONS[:2]:
            for name in ('company-skill-evolution-lab', 'company-skill-security-review'):
                text = (root / 'skills' / name / 'SKILL.md').read_text()
                self.assertIn('EXPERIENCE-01', text)
                self.assertIn('experience-candidate-template.md', text)

    def test_native_waits_record_real_identity_and_reject_stale_events(self):
        for root in DISTRIBUTIONS:
            policy = (root / 'specs/global/assets/task-execution-policy.md').read_text()
            for marker in ('WAIT-01', 'mechanism_id', 'candidate_fingerprint', 'last_event_id', 'cancelled', 'manual_resume'):
                self.assertIn(marker, policy)
        for root in DISTRIBUTIONS[:2]:
            for name in ('company-workflow-help', 'company-thread-handoff'):
                self.assertIn('WAIT-01', (root / 'skills' / name / 'SKILL.md').read_text())

    def test_delegation_results_need_current_candidate_and_serial_fallback(self):
        for root in DISTRIBUTIONS[:2]:
            for name in ('company-implementation-runner', 'company-expert-routing'):
                text = (root / 'skills' / name / 'SKILL.md').read_text()
                for marker in ('DELEGATE-01', 'candidate_fingerprint', 'result_id', 'budget', 'serial'):
                    self.assertIn(marker, text)

if __name__ == '__main__':
    unittest.main()
