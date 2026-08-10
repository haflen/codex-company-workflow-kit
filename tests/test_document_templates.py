import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORMAL_TEMPLATES = {
    "requirements-template.md",
    "design-template.md",
    "data-model-template.md",
    "business-rules-template.md",
    "api-contract-template.md",
    "tasks-template.md",
    "spike-report-template.md",
    "hotfix-report-template.md",
    "requirements-prototype-record-template.md",
    "delivery-closeout-template.md",
}
LANGUAGES = {
    "zh": {
        "plugin": ROOT / "outputs/company-codex-workflow-v2-zh",
        "starter": ROOT / "outputs/company-codex-workflow-template-zh",
        "conclusion": "## 先看结论",
        "change": "## 本次变化",
        "waiver": "图表豁免",
    },
    "en": {
        "plugin": ROOT / "outputs/company-codex-workflow-v2",
        "starter": ROOT / "outputs/company-codex-workflow-template",
        "conclusion": "## Decision Summary",
        "change": "## What Changed",
        "waiver": "Diagram Waiver",
    },
}
SKILL_GATES = {
    "company-feature-requirements": {
        "DOC-G01",
        "DOC-G02",
        "DOC-G05",
        "DOC-G06",
        "DOC-G07",
        "DOC-G08",
        "DOC-G09",
        "DOC-G10",
        "DOC-G11",
        "DOC-G12",
    },
    "company-feature-design": {
        "DOC-G01",
        "DOC-G03",
        "DOC-G05",
        "DOC-G06",
        "DOC-G07",
        "DOC-G08",
        "DOC-G09",
        "DOC-G10",
        "DOC-G11",
        "DOC-G12",
    },
    "company-feature-planning": {
        "DOC-G01",
        "DOC-G04",
        "DOC-G05",
        "DOC-G06",
        "DOC-G07",
        "DOC-G08",
        "DOC-G09",
        "DOC-G10",
        "DOC-G11",
        "DOC-G12",
    },
    "company-requirements-prototype": {
        "DOC-G01",
        "DOC-G04",
        "DOC-G05",
        "DOC-G06",
        "DOC-G07",
        "DOC-G08",
        "DOC-G09",
        "DOC-G10",
        "DOC-G11",
        "DOC-G12",
    },
    "company-spike-research": {
        "DOC-G01",
        "DOC-G04",
        "DOC-G05",
        "DOC-G06",
        "DOC-G07",
        "DOC-G08",
        "DOC-G09",
        "DOC-G10",
        "DOC-G11",
        "DOC-G12",
    },
    "company-bugfix-runner": {
        "DOC-G01",
        "DOC-G04",
        "DOC-G05",
        "DOC-G06",
        "DOC-G07",
        "DOC-G08",
        "DOC-G09",
        "DOC-G10",
        "DOC-G11",
        "DOC-G12",
    },
    "company-context-index": {
        "DOC-G01",
        "DOC-G04",
        "DOC-G05",
        "DOC-G06",
        "DOC-G07",
        "DOC-G08",
        "DOC-G09",
        "DOC-G10",
        "DOC-G11",
        "DOC-G12",
    },
    "company-delivery-closeout": {
        "DOC-G01",
        "DOC-G04",
        "DOC-G05",
        "DOC-G06",
        "DOC-G07",
        "DOC-G08",
        "DOC-G09",
        "DOC-G10",
        "DOC-G11",
        "DOC-G12",
    },
    "company-implementation-runner": {
        "DOC-G06",
        "DOC-G07",
        "DOC-G08",
        "DOC-G09",
        "DOC-G10",
        "DOC-G11",
        "DOC-G12",
    },
    "company-workflow-health-check": {
        f"DOC-G{number:02d}" for number in range(1, 13)
    },
}
INDEX_ASSETS = {
    "document-standard.md",
    "data-model-template.md",
    "requirements-prototype-record-template.md",
    "delivery-closeout-template.md",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class DocumentTemplateContractTests(unittest.TestCase):
    def test_formal_template_set_and_starter_mirror(self):
        for language, config in LANGUAGES.items():
            plugin_assets = config["plugin"] / "specs/global/assets"
            starter_assets = config["starter"] / "specs/global/assets"
            with self.subTest(language=language, file="document-standard.md"):
                self.assertEqual(
                    read(plugin_assets / "document-standard.md"),
                    read(starter_assets / "document-standard.md"),
                )
            for name in FORMAL_TEMPLATES:
                with self.subTest(language=language, file=name):
                    self.assertEqual(
                        read(plugin_assets / name),
                        read(starter_assets / name),
                    )

    def test_common_human_reading_contract(self):
        for language, config in LANGUAGES.items():
            assets = config["plugin"] / "specs/global/assets"
            for name in FORMAL_TEMPLATES:
                with self.subTest(language=language, file=name):
                    content = read(assets / name)
                    self.assertIn("work-item-id", content)
                    self.assertIn(config["conclusion"], content)
                    self.assertIn(config["change"], content)
                    self.assertIn(config["waiver"], content)
                    self.assertIn("```mermaid", content)

    def test_required_diagram_types(self):
        for language, config in LANGUAGES.items():
            assets = config["plugin"] / "specs/global/assets"
            requirements = read(assets / "requirements-template.md")
            design = read(assets / "design-template.md")
            data_model = read(assets / "data-model-template.md")
            with self.subTest(language=language):
                self.assertIn("flowchart", requirements)
                self.assertIn("flowchart", design)
                self.assertIn("sequenceDiagram", design)
                self.assertTrue("erDiagram" in data_model or "flowchart" in data_model)
                self.assertGreaterEqual(data_model.count("```mermaid"), 2)

    def test_skill_gate_responsibilities(self):
        for language, config in LANGUAGES.items():
            for skill, gates in SKILL_GATES.items():
                content = read(config["plugin"] / "skills" / skill / "SKILL.md")
                for gate in gates:
                    with self.subTest(language=language, skill=skill, gate=gate):
                        self.assertIn(gate, content)

    def test_agents_route_to_shared_standard(self):
        for language, config in LANGUAGES.items():
            for root_name in ("plugin", "starter"):
                content = read(config[root_name] / "AGENTS.md")
                with self.subTest(language=language, root=root_name):
                    self.assertIn("document-standard.md", content)
                    self.assertIn("DOC-G01", content)
                    self.assertIn("DOC-G12", content)

    def test_indexes_route_new_assets(self):
        for language, config in LANGUAGES.items():
            for root_name in ("plugin", "starter"):
                content = read(config[root_name] / "specs/global/INDEX.md")
                for asset in INDEX_ASSETS:
                    with self.subTest(language=language, root=root_name, asset=asset):
                        self.assertIn(asset, content)


if __name__ == "__main__":
    unittest.main()
