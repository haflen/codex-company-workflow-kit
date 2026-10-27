"""Validate shipped routing assets, not live dispatch or process-stop behavior."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PACKAGES = ('company-codex-workflow-v2', 'company-codex-workflow-v2-zh')


class MultiAgentDeliveryAssetsTests(unittest.TestCase):
    def test_entry_and_router_link_to_same_shipped_reference(self):
        for package in PACKAGES:
            with self.subTest(package=package):
                skills = ROOT / 'outputs' / package / 'skills'
                target = skills / 'company-expert-routing/references/multi-agent-delivery.md'
                self.assertTrue(target.is_file())
                for skill in ('company-workflow-help', 'company-expert-routing'):
                    source = skills / skill / 'SKILL.md'
                    links = re.findall(r'\]\(([^)]+multi-agent-delivery\.md)\)', source.read_text())
                    self.assertEqual(1, len(links), source)
                    self.assertEqual(target.resolve(), (source.parent / links[0]).resolve())
                self.assertFalse((target.parent / 'SKILL.md').exists(), 'Reference must not become another skill')

    def test_dedicated_agent_entry_is_shipped_and_links_resolve(self):
        for package in PACKAGES:
            skills = ROOT / 'outputs' / package / 'skills'
            entry = skills / 'company-agent-routing/SKILL.md'
            with self.subTest(package=package):
                self.assertTrue(entry.is_file(), 'Explicit multi-agent selection needs a discoverable skill')
                content = entry.read_text()
                self.assertIn('name: company-agent-routing\n', content)
                references = re.findall(r'\]\(([^)]+\.md)\)', content)
                self.assertTrue(references)
                for link in references:
                    self.assertTrue((entry.parent / link).is_file(), link)
                for caller in ('company-workflow-help', 'company-expert-routing'):
                    text = (skills / caller / 'SKILL.md').read_text()
                    links = re.findall(r'\]\(([^)]+company-agent-routing/SKILL\.md)\)', text)
                    self.assertTrue(links, caller)
                    self.assertTrue(all((skills / caller / link).resolve() == entry.resolve() for link in links))

    def test_bilingual_dispatch_packets_preserve_same_contract(self):
        required = {
            'task_id', 'role', 'authority_source', 'goal_and_endpoint',
            'acceptance', 'candidate_fingerprint', 'inputs', 'allowed_paths',
            'forbidden_actions', 'immutable_contract', 'editable_contract',
            'verification', 'budget', 'output_location', 'runtime_ownership',
            'stop_conditions', 'result_format',
        }
        for package in PACKAGES:
            with self.subTest(package=package):
                reference = ROOT / 'outputs' / package / 'skills/company-expert-routing/references/multi-agent-delivery.md'
                packets = re.findall(r'```text\n(.*?)\n```', reference.read_text(), re.S)
                self.assertEqual(1, len(packets))
                fields = re.findall(r'^([a-z_]+):', packets[0], re.M)
                self.assertEqual(len(fields), len(set(fields)), 'Duplicate packet fields are ambiguous')
                self.assertEqual(required, set(fields))
                self.assertIn('executor | independent reviewer | explorer', packets[0])

    def test_reference_relative_markdown_links_resolve(self):
        sources = [ROOT / 'docs/multi-agent-quickstart.md']
        for package in PACKAGES:
            for skill in ('company-workflow-help', 'company-expert-routing',
                          'company-feature-requirements', 'company-quality-validation'):
                sources.append(ROOT / 'outputs' / package / 'skills' / skill / 'SKILL.md')
            sources.append(ROOT / 'outputs' / package / 'skills/company-expert-routing/references/multi-agent-delivery.md')
        for source in sources:
            for link in re.findall(r'\]\(([^)]+\.md(?:#[^)]+)?)\)', source.read_text()):
                if '://' not in link:
                    path, _, anchor = link.partition('#')
                    target = source.parent / path
                    self.assertTrue(target.is_file(), f'{source}: {link}')
                    if anchor:
                        # A path can resolve while its review-section anchor is broken.
                        headings = re.findall(r'^#{1,6} (.+)$', target.read_text(), re.M)
                        anchors = {re.sub(r'[^\w\- ]', '', heading.lower()).replace(' ', '-')
                                   for heading in headings}
                        self.assertIn(anchor, anchors, f'{source}: {link}')

    def test_lifecycle_routes_to_existing_phase_skills_in_both_packages(self):
        # An implementation-only route cannot satisfy these upstream/downstream handoffs.
        phases = (
            ('Business understanding', '业务理解', {'company-context-index'}),
            ('Requirements', '需求', {'company-feature-requirements'}),
            ('Design', '设计', {'company-feature-design'}),
            ('Planning', '任务', {'company-feature-planning'}),
            ('Implementation', '实现', {'company-implementation-runner', 'company-bugfix-runner'}),
            ('Quality validation', '质量验收', {'company-quality-validation'}),
            ('Closeout', '收口', {'company-delivery-closeout'}),
            ('Handoff when needed', '按需交接', {'company-thread-handoff'}),
        )
        for package in PACKAGES:
            reference = ROOT / 'outputs' / package / 'skills/company-expert-routing/references/multi-agent-delivery.md'
            rows = [line.strip('|').split('|') for line in reference.read_text().splitlines() if line.startswith('|')]
            for en, zh, expected in phases:
                phase = zh if package.endswith('-zh') else en
                with self.subTest(package=package, phase=phase):
                    matches = [row for row in rows if row[0].strip() == phase]
                    self.assertEqual(1, len(matches), 'Each phase needs one unambiguous route')
                    self.assertEqual(4, len(matches[0]), 'Route must retain its expert and handoff columns')
                    links = re.findall(r'\]\(([^)]+/SKILL\.md)\)', matches[0][1])
                    self.assertEqual(expected, {(reference.parent / link).resolve().parent.name for link in links})
                    for link in links:
                        target = (reference.parent / link).resolve()
                        self.assertTrue(target.is_file(), target)
                        self.assertIn(f'name: {target.parent.name}\n', target.read_text())


if __name__ == '__main__':
    unittest.main()
