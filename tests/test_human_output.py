import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class HumanOutputTests(unittest.TestCase):
    def test_closeout_next_step_is_visible_and_scoped(self):
        for suffix, phrases in (
            ('-zh', ('**下一步：**', '最后一个独立段落', '普通问答和工作中更新',
                     '不把这条收尾要求扩展为正文固定标题', '不把进度更新当作结束任务')),
            ('', ('**Next step:**', 'last standalone paragraph', 'Ordinary Q&A and progress updates',
                  'does not impose fixed headings on the body', 'do not end the task at a progress update')),
        ):
            for distribution in ('v2', 'template'):
                root = ROOT / f'outputs/company-codex-workflow-{distribution}{suffix}'
                policy = (root / 'specs/global/assets/human-output-standard.md').read_text()
                with self.subTest(root=root):
                    for phrase in phrases:
                        self.assertIn(phrase, policy)
                    self.assertIn(phrases[0], (root / 'AGENTS.md').read_text())

    def test_next_step_preserves_authorization_and_completion_boundaries(self):
        for suffix, phrases in (
            ('-zh', ('已有授权且前置条件满足', '需要用户处理', '本任务已完成，你现在无需操作',
                     '不新增审批或扩大授权', '触发条件与责任方', '不承诺自动监控或日后通知')),
            ('', ('Already authorized and prerequisites met', 'User action required',
                  'This task is complete; no action is needed from you now', 'no new approval gate or wider authority',
                  'trigger and owner', 'do not promise automatic monitoring or future notifications')),
        ):
            root = ROOT / f'outputs/company-codex-workflow-v2{suffix}'
            policy = (root / 'specs/global/assets/human-output-standard.md').read_text()
            for phrase in phrases:
                with self.subTest(language=suffix, phrase=phrase):
                    self.assertIn(phrase, policy)

    def test_next_step_contract_reaches_guides_and_internal_record(self):
        for name in ('README.md', 'docs/company-quickstart.md', 'docs/codex-usage-guide.md'):
            with self.subTest(guide=name):
                self.assertIn('**下一步：**', (ROOT / name).read_text())
        for suffix, phrase in (('-zh', '继续执行 / 等待用户 / 已完成'),
                               ('', 'continue execution / await user / complete')):
            root = ROOT / f'outputs/company-codex-workflow-v2{suffix}'
            self.assertIn(phrase, (root / 'specs/global/assets/execution-record-template.md').read_text())

    def test_document_gates_check_content_instead_of_literal_headings(self):
        for suffix, phrases, obsolete in (
            ('-zh', ('标题可改名', '版本变更评审', '初稿不要求变更表', '不适用不是图表豁免'),
             ('“本次变化”固定放在', '`先看结论` 非空', 'L2 使用完整模板结构')),
            ('', ('Headings may be renamed', 'version-change review', 'First drafts do not require a change table', 'Not applicable is not a diagram waiver'),
             ('Place `What Changed` immediately after', '`Decision Summary` is non-empty', 'L2 uses the complete template', 'three to five conclusions')),
        ):
            for distribution in ('v2', 'template'):
                root = ROOT / f'outputs/company-codex-workflow-{distribution}{suffix}'
                policy = (root / 'specs/global/assets/document-standard.md').read_text()
                with self.subTest(root=root):
                    for phrase in phrases:
                        self.assertIn(phrase, policy)
                    for phrase in obsolete:
                        self.assertNotIn(phrase, policy)
                    agent = (root / 'AGENTS.md').read_text()
                    self.assertNotIn('新文档完整执行 `DOC-G01` 至 `DOC-G12`', agent)
                    self.assertNotIn('Apply `DOC-G01` through `DOC-G12` to new documents.', agent)

    def test_report_types_have_diagram_rules_without_weakening_design(self):
        for suffix, labels in (
            ('-zh', ('验收报告', '操作指南', '管理汇报', '步骤与判断表', '不能替代技术设计')),
            ('', ('Acceptance report', 'Operating guide', 'Management report', 'steps and decision tables', 'does not replace a technical design')),
        ):
            assets = ROOT / f'outputs/company-codex-workflow-v2{suffix}/specs/global/assets'
            policy = (assets / 'document-standard.md').read_text()
            with self.subTest(suffix=suffix):
                for label in labels:
                    self.assertIn(label, policy)
                technical_gate = next(line for line in policy.splitlines() if '| `DOC-G03` |' in line)
                self.assertIn('sequenceDiagram', technical_gate)
                self.assertIn('架构' if suffix else 'Architecture', technical_gate)
                waiver = next(line for line in policy.splitlines() if '| `DOC-G05` |' in line)
                self.assertIn('AI 自行判断无效' if suffix else 'AI-only judgment is invalid', waiver)

    def test_report_templates_are_scaffolds_but_keep_required_evidence(self):
        for suffix, note in (('-zh', '标题和章节顺序可调整'), ('', 'Headings and section order may change')):
            assets = ROOT / f'outputs/company-codex-workflow-v2{suffix}/specs/global/assets'
            for name in ('quality-validation-report-template.md', 'delivery-closeout-template.md'):
                with self.subTest(suffix=suffix, name=name):
                    content = (assets / name).read_text()
                    self.assertIn(note, content)
                    self.assertIn('document-standard.md', content)
                    self.assertIn('```mermaid', content)
                    self.assertIn('API_PENDING', content)
                    self.assertIn('execution-record-template.md', content)

    def test_shared_policy_is_packaged_and_mirrored(self):
        for suffix in ('', '-zh'):
            plugin = ROOT / ('outputs/company-codex-workflow-v2' + suffix)
            starter = ROOT / ('outputs/company-codex-workflow-template' + suffix)
            for name in ('human-output-standard.md', 'execution-record-template.md'):
                p = plugin / 'specs/global/assets' / name
                self.assertTrue(p.is_file(), str(p))
                self.assertEqual(p.read_text(), (starter / 'specs/global/assets' / name).read_text())
            for root in (plugin, starter):
                self.assertIn('human-output-standard.md', (root / 'AGENTS.md').read_text())
                self.assertIn('human-output-standard.md', (root / 'specs/global/INDEX.md').read_text())

    def test_all_workflows_load_shared_contract_without_old_appendix(self):
        for path in (ROOT / 'outputs').glob('company-codex-workflow-v2*/skills/company-*/SKILL.md'):
            content = path.read_text()
            with self.subTest(path=path):
                self.assertIn('human-output-standard.md', content)
                self.assertNotIn('审计字段只能出现在 `技术审计附录`', content)
                self.assertNotIn('Audit fields may appear only in the `Technical Audit Appendix`', content)
                self.assertNotIn('不得删除、改名或调换四个标题', content)

    def test_human_templates_declare_audience_and_internal_separation(self):
        for root in (ROOT / 'outputs').glob('company-codex-workflow-*'):
            for path in (root / 'specs/global/assets').glob('*template.md'):
                if path.name == 'execution-record-template.md':
                    continue
                with self.subTest(path=path):
                    content = path.read_text()
                    self.assertIn('human-output-standard.md', content)
                    self.assertNotIn('## 能力与执行透明度', content)
                    self.assertNotIn('## Capability and Execution Transparency', content)
                    self.assertNotIn('<details', content)
                    self.assertNotIn('<summary', content)

    def test_candidate_identity_is_retained_in_internal_template(self):
        for suffix in ('', '-zh'):
            assets = ROOT / ('outputs/company-codex-workflow-v2' + suffix) / 'specs/global/assets'
            content = (assets / 'execution-record-template.md').read_text()
            for field in ('work-item-id', 'owner-path', 'record-path', 'release-target', 'HEAD', 'SHA-256', 'full-audit'):
                self.assertIn(field, content)
            report = (assets / 'quality-validation-report-template.md').read_text()
            self.assertIn('execution-record-template.md', report)
            self.assertIn('API_PENDING', report)
            self.assertIn('CONDITIONAL_MERGED', report)

    def test_active_guides_do_not_require_public_audit_or_scripted_replies(self):
        for name in ('README.md', 'docs/company-quickstart.md', 'docs/codex-usage-guide.md', 'docs/skill-tree.md'):
            content = (ROOT / name).read_text()
            with self.subTest(file=name):
                self.assertNotIn('检查回复是否包含 `透明度模式`', content)
                self.assertNotIn('技术审计附录', content)
                self.assertNotIn('`推荐用户下一句`', content)

    def test_agent_planning_records_stay_out_of_human_templates(self):
        for suffix in ('', '-zh'):
            assets = ROOT / ('outputs/company-codex-workflow-v2' + suffix) / 'specs/global/assets'
            tasks = (assets / 'tasks-template.md').read_text()
            design = (assets / 'design-template.md').read_text()
            internal = (assets / 'execution-record-template.md').read_text()
            self.assertNotIn('Subagent', tasks)
            self.assertNotIn('实现授权状态', design)
            self.assertNotIn('Implementation authorization', design)
            self.assertTrue('子代理安排' in internal or 'Subagent Arrangement' in internal)
            self.assertTrue('停止条件' in internal or 'Stop Conditions' in internal)

    def test_no_unconditional_user_reply_phrase(self):
        for root in (ROOT / 'outputs').glob('company-codex-workflow-v2*'):
            for path in [root / 'AGENTS.md', *root.glob('skills/company-*/SKILL.md')]:
                content = path.read_text()
                with self.subTest(path=path):
                    self.assertNotIn('推荐用户下一句', content)
                    self.assertNotIn('recommended next user phrase', content.lower())
            router = (root / 'skills/company-expert-routing/SKILL.md').read_text()
            self.assertNotIn('每次路由都必须输出', router)
            self.assertNotIn('Every routing decision must output', router)
            self.assertNotIn('Every routing response must output', router)

if __name__ == '__main__':
    unittest.main()
