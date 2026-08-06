import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "asset_boundaries.py"


def load_module():
    spec = importlib.util.spec_from_file_location("asset_boundaries", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load asset boundary validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class AssetBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.project = Path(self.temp.name)
        (self.project / "specs").mkdir()
        (self.project / "docs").mkdir()
        (self.project / "frontend" / "client-portal").mkdir(parents=True)
        (self.project / "frontend" / "client-portal" / "package.json").write_text("{}\n")

    def tearDown(self):
        self.temp.cleanup()

    def generate(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "generate", str(self.project), "--lang", "en"],
            text=True,
            capture_output=True,
            check=True,
        )
        config = self.project / ".codex-workflow" / "asset-boundaries.json"
        return result, config

    def check_paths(self, *paths, expected=0):
        command = [sys.executable, str(SCRIPT), "check", str(self.project), "--lang", "en"]
        for path in paths:
            command.extend(["--path", path])
        result = subprocess.run(command, text=True, capture_output=True)
        self.assertEqual(expected, result.returncode, result.stdout + result.stderr)
        return result

    def test_generate_detects_engineering_root_without_personal_absolute_paths(self):
        _, config_path = self.generate()
        config = json.loads(config_path.read_text())

        self.assertEqual("generated-review-required", config["status"])
        self.assertIn(
            "frontend/client-portal",
            [entry["path"] for entry in config["engineeringRoots"]],
        )
        self.assertNotIn(str(self.project), config_path.read_text())

    def test_rejects_package_manifest_under_specs(self):
        self.generate()
        result = self.check_paths("specs/feature/contracts/package.json", expected=2)
        self.assertIn("AB001", result.stdout)

    def test_rejects_suffix_based_manifests_under_documentation_roots(self):
        self.generate()
        result = self.check_paths(
            "specs/App.csproj",
            "docs/Product.sln",
            expected=2,
        )
        self.assertEqual(2, result.stdout.count("AB001"), result.stdout)

    def test_rejects_dependency_tree_under_docs(self):
        self.generate()
        result = self.check_paths("docs/demo/node_modules/ajv/index.js", expected=2)
        self.assertIn("AB002", result.stdout)

    def test_rejects_executable_test_under_specs(self):
        self.generate()
        result = self.check_paths("specs/v1/contracts/assertions/schema.test.mjs", expected=2)
        self.assertIn("AB003", result.stdout)

    def test_rejects_machine_contract_tree_under_specs(self):
        self.generate()
        result = self.check_paths("specs/v1/contracts/stp-ui-v1.schema.json", expected=2)
        self.assertIn("AB004", result.stdout)

    def test_allows_markdown_under_specs_and_code_under_engineering_root(self):
        self.generate()
        self.check_paths(
            "specs/v1/design.md",
            "frontend/client-portal/src/contracts/clientTypes.ts",
        )

    def test_explicit_exception_allows_declared_machine_contract(self):
        _, config_path = self.generate()
        config = json.loads(config_path.read_text())
        config["exceptions"] = [
            {
                "path": "specs/contracts/openapi.schema.json",
                "type": "machine-contract",
                "reason": "canonical API contract",
                "owner": "backend",
                "validation": "openapi lint",
            }
        ]
        config_path.write_text(json.dumps(config, indent=2) + "\n")

        self.check_paths("specs/contracts/openapi.schema.json")

    def test_machine_contract_exception_does_not_bypass_package_or_test_rules(self):
        _, config_path = self.generate()
        config = json.loads(config_path.read_text())
        config["exceptions"] = [
            {
                "path": "specs/contracts",
                "type": "machine-contract",
                "reason": "canonical contracts",
                "owner": "platform",
                "validation": "contract lint",
            }
        ]
        config_path.write_text(json.dumps(config, indent=2) + "\n")

        self.check_paths("specs/contracts/openapi.yaml")
        self.assertIn(
            "AB001",
            self.check_paths("specs/contracts/package.json", expected=2).stdout,
        )
        self.assertIn(
            "AB003",
            self.check_paths("specs/contracts/schema.test.mjs", expected=2).stdout,
        )

    def test_rejects_named_api_contracts_under_documentation_roots(self):
        self.generate()
        result = self.check_paths(
            "specs/api/openapi.yaml",
            "docs/api/swagger.json",
            "specs/events/asyncapi.yml",
            expected=2,
        )
        self.assertEqual(3, result.stdout.count("AB004"), result.stdout)

    def test_confirm_changes_status_without_changing_roots(self):
        _, config_path = self.generate()
        before = json.loads(config_path.read_text())
        subprocess.run(
            [sys.executable, str(SCRIPT), "confirm", str(self.project), "--lang", "en"],
            text=True,
            capture_output=True,
            check=True,
        )
        after = json.loads(config_path.read_text())

        self.assertEqual("confirmed", after["status"])
        self.assertEqual(before["engineeringRoots"], after["engineeringRoots"])

    def test_existing_config_is_preserved_and_generated_candidate_is_written(self):
        _, config_path = self.generate()
        config_path.write_text('{"sentinel": true}\n')
        subprocess.run(
            [sys.executable, str(SCRIPT), "generate", str(self.project), "--lang", "en"],
            text=True,
            capture_output=True,
            check=True,
        )

        self.assertEqual({"sentinel": True}, json.loads(config_path.read_text()))
        self.assertTrue((config_path.parent / "asset-boundaries.generated.json").exists())

    def test_dot_prefixed_tooling_root_is_not_changed_during_normalization(self):
        module = load_module()

        self.assertEqual(
            ".codex-workflow/bin/asset_boundaries.py",
            module.normalize_relative(
                self.project,
                ".codex-workflow/bin/asset_boundaries.py",
            ),
        )

    def test_confirmed_config_allows_installed_boundary_checker(self):
        _, config_path = self.generate()
        config = json.loads(config_path.read_text())
        config["status"] = "confirmed"
        config_path.write_text(json.dumps(config, indent=2) + "\n")

        self.check_paths(".codex-workflow/bin/asset_boundaries.py")

    def test_context_index_reads_generated_boundary_shape(self):
        self.generate()
        index_script = ROOT / "scripts" / "generate_index.py"
        output = self.project / "specs" / "global" / "INDEX.generated.md"
        subprocess.run(
            [
                sys.executable,
                str(index_script),
                str(self.project),
                "--lang",
                "zh",
                "--output",
                str(output),
            ],
            text=True,
            capture_output=True,
            check=True,
        )

        content = output.read_text()
        self.assertIn("generated-review-required", content)
        self.assertIn("frontend/client-portal", content)

    def test_changed_mode_checks_only_git_changed_and_untracked_paths(self):
        self.generate()
        subprocess.run(["git", "init", "-q"], cwd=self.project, check=True)
        misplaced = self.project / "specs" / "feature" / "package.json"
        misplaced.parent.mkdir(parents=True)
        misplaced.write_text("{}\n")

        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "check",
                str(self.project),
                "--lang",
                "en",
                "--changed",
            ],
            text=True,
            capture_output=True,
        )

        self.assertEqual(2, result.returncode, result.stdout + result.stderr)
        self.assertIn("AB001 specs/feature/package.json", result.stdout)

    def test_full_audit_detects_dependency_directory_without_traversing_it(self):
        self.generate()
        dependency = self.project / "specs" / "demo" / "node_modules" / "lib"
        dependency.mkdir(parents=True)
        (dependency / "index.js").write_text("module.exports = {}\n")

        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "check",
                str(self.project),
                "--lang",
                "en",
                "--all",
            ],
            text=True,
            capture_output=True,
        )

        self.assertEqual(2, result.returncode, result.stdout + result.stderr)
        self.assertIn("AB002 specs/demo/node_modules", result.stdout)

    def test_full_audit_detects_generated_output_directories_under_docs(self):
        self.generate()
        build = self.project / "specs" / "build"
        dist = self.project / "docs" / "dist"
        build.mkdir(parents=True)
        dist.mkdir(parents=True)
        (build / "package.json").write_text("{}\n")
        (dist / "app.test.js").write_text("throw new Error('should not run')\n")

        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "check",
                str(self.project),
                "--lang",
                "en",
                "--all",
            ],
            text=True,
            capture_output=True,
        )

        self.assertEqual(2, result.returncode, result.stdout + result.stderr)
        self.assertIn("AB006 specs/build", result.stdout)
        self.assertIn("AB006 docs/dist", result.stdout)

    def test_accept_generated_promotes_candidate_and_keeps_backup(self):
        _, config_path = self.generate()
        original = json.loads(config_path.read_text())
        original["exceptions"] = [
            {
                "path": "specs/contracts/openapi.yaml",
                "type": "machine-contract",
                "reason": "canonical contract",
                "owner": "platform",
                "validation": "openapi lint",
            }
        ]
        config_path.write_text(json.dumps(original, indent=2) + "\n")
        (self.project / "backend").mkdir()
        (self.project / "backend" / "pom.xml").write_text("<project/>\n")
        subprocess.run(
            [sys.executable, str(SCRIPT), "generate", str(self.project), "--lang", "en"],
            text=True,
            capture_output=True,
            check=True,
        )

        candidate = config_path.parent / "asset-boundaries.generated.json"
        candidate_data = json.loads(candidate.read_text())
        self.assertIn("backend", [entry["path"] for entry in candidate_data["engineeringRoots"]])
        self.assertEqual(original["exceptions"], candidate_data["exceptions"])

        subprocess.run(
            [sys.executable, str(SCRIPT), "accept-generated", str(self.project), "--lang", "en"],
            text=True,
            capture_output=True,
            check=True,
        )

        accepted = json.loads(config_path.read_text())
        self.assertEqual("confirmed", accepted["status"])
        self.assertIn("backend", [entry["path"] for entry in accepted["engineeringRoots"]])
        self.assertTrue((config_path.parent / "asset-boundaries.backup.json").exists())
        self.assertFalse(candidate.exists())

    def test_accept_generated_rejects_malformed_candidate_without_replacing_config(self):
        _, config_path = self.generate()
        original = config_path.read_text()
        subprocess.run(
            [sys.executable, str(SCRIPT), "generate", str(self.project), "--lang", "en"],
            text=True,
            capture_output=True,
            check=True,
        )
        candidate = config_path.parent / "asset-boundaries.generated.json"
        malformed = json.loads(candidate.read_text())
        malformed["engineeringRoots"] = "frontend/client-portal"
        candidate.write_text(json.dumps(malformed, indent=2) + "\n")

        result = subprocess.run(
            [sys.executable, str(SCRIPT), "accept-generated", str(self.project), "--lang", "en"],
            text=True,
            capture_output=True,
        )

        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("engineeringRoots must be a list", result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(original, config_path.read_text())
        self.assertTrue(candidate.exists())

    def test_detects_additional_common_project_markers(self):
        (self.project / "python-service").mkdir()
        (self.project / "python-service" / "requirements.txt").write_text("pytest\n")
        (self.project / "dotnet-service").mkdir()
        (self.project / "dotnet-service" / "Service.csproj").write_text("<Project/>\n")

        _, config_path = self.generate()
        roots = [entry["path"] for entry in json.loads(config_path.read_text())["engineeringRoots"]]

        self.assertIn("python-service", roots)
        self.assertIn("dotnet-service", roots)

    def test_changed_mode_has_actionable_message_outside_git(self):
        self.generate()
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "check",
                str(self.project),
                "--lang",
                "zh",
                "--changed",
            ],
            text=True,
            capture_output=True,
        )

        self.assertEqual(1, result.returncode)
        self.assertIn("尚未初始化 Git", result.stderr)
        self.assertIn("audit-assets", result.stderr)


class WorkflowRegressionTests(unittest.TestCase):
    def test_shell_bootstrap_installs_gate_and_preserves_existing_index(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / "frontend" / "portal").mkdir(parents=True)
            (project / "frontend" / "portal" / "package.json").write_text("{}\n")
            index = project / "specs" / "global" / "INDEX.md"
            index.parent.mkdir(parents=True)
            index.write_text("# Existing index\n")

            result = subprocess.run(
                [
                    "bash",
                    str(ROOT / "scripts" / "install.sh"),
                    "bootstrap-project",
                    str(project),
                    "--lang",
                    "zh",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertEqual("# Existing index\n", index.read_text())
            self.assertTrue((project / "specs/global/INDEX.generated.md").exists())
            self.assertTrue((project / ".codex-workflow/bin/asset_boundaries.py").exists())
            config = json.loads(
                (project / ".codex-workflow/asset-boundaries.json").read_text()
            )
            self.assertIn(
                "frontend/portal",
                [entry["path"] for entry in config["engineeringRoots"]],
            )

    def test_required_zh_workflows_reference_asset_boundary_gate(self):
        required = [
            "company-feature-design",
            "company-feature-planning",
            "company-implementation-runner",
            "company-bugfix-runner",
            "company-workflow-health-check",
            "company-context-index",
            "company-legacy-project-onboarding",
            "company-delivery-closeout",
        ]
        for skill in required:
            path = ROOT / "outputs" / "company-codex-workflow-v2-zh" / "skills" / skill / "SKILL.md"
            self.assertIn("asset-boundaries.json", path.read_text(), skill)

    def test_required_en_workflows_reference_asset_boundary_gate(self):
        required = [
            "company-feature-design",
            "company-feature-planning",
            "company-implementation-runner",
            "company-bugfix-runner",
            "company-workflow-health-check",
            "company-context-index",
            "company-legacy-project-onboarding",
            "company-delivery-closeout",
        ]
        for skill in required:
            path = ROOT / "outputs" / "company-codex-workflow-v2" / "skills" / skill / "SKILL.md"
            self.assertIn("asset-boundaries.json", path.read_text(), skill)

    def test_bilingual_project_rules_and_templates_include_gate_contract(self):
        roots = [
            ROOT / "outputs" / "company-codex-workflow-v2-zh",
            ROOT / "outputs" / "company-codex-workflow-v2",
            ROOT / "outputs" / "company-codex-workflow-template-zh",
            ROOT / "outputs" / "company-codex-workflow-template",
        ]
        for root in roots:
            self.assertIn("asset-boundaries.json", (root / "AGENTS.md").read_text())
            self.assertIn(
                "asset-boundaries.json",
                (root / "specs/global/assets/design-template.md").read_text(),
            )
            self.assertIn(
                "asset-boundaries.json",
                (root / "specs/global/assets/tasks-template.md").read_text(),
            )

    def test_installers_expose_boundary_management_commands(self):
        required = [
            "generate-asset-boundaries",
            "accept-asset-boundaries",
            "confirm-asset-boundaries",
            "check-assets",
            "audit-assets",
        ]
        for path in (ROOT / "scripts/install.sh", ROOT / "scripts/install.ps1"):
            content = path.read_text()
            for command in required:
                self.assertIn(command, content, "{} missing {}".format(path.name, command))

    def test_npm_package_includes_regression_tests_and_tracks_plugin_version(self):
        package = json.loads((ROOT / "package.json").read_text())
        plugin = json.loads(
            (
                ROOT
                / "outputs/company-codex-workflow-v2-zh/.codex-plugin/plugin.json"
            ).read_text()
        )

        self.assertIn("tests/", package["files"])
        self.assertIn("CHANGELOG.md", package["files"])
        self.assertEqual(plugin["version"], package["version"])


if __name__ == "__main__":
    unittest.main()
