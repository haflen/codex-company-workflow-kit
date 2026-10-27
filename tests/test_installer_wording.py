"""Exercise the actual installer patterns on acceptable prose and unfinished markers."""
from pathlib import Path
import re
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]


def pattern(script):
    content = (ROOT / 'scripts' / script).read_text()
    prefix = 'risk_pattern=' if script.endswith('.sh') else '$riskPattern ='
    line = next(line.strip() for line in content.splitlines() if line.strip().startswith(prefix))
    return ''.join(re.findall(r'"([^"\n]*)"', line))


class InstallerWordingTests(unittest.TestCase):
    def test_ordinary_prose_and_code_examples_are_not_unfinished_markers(self):
        prose = ('已定与待定事项分别说明。\n收益待补时，已有运行轨迹仍可查看。\n'
                 'Return immediately with placeholder\n<input placeholder="Name">\n')
        for script in ('install.sh', 'install.ps1'):
            with self.subTest(script=script):
                result = subprocess.run(['rg', '-n', pattern(script)], input=prose, text=True, capture_output=True)
                self.assertEqual(1, result.returncode, result.stdout + result.stderr)

    def test_explicit_unfinished_markers_and_existing_risk_phrases_still_fail(self):
        for script in ('install.sh', 'install.ps1'):
            for text in ('TODO: finish this', '  - TODO: fill scope', '[TODO]', '[TBD]',
                         '## TBD: implementation', '待补：验收结果', 'placeholder: fill in',
                         '严禁自行处理', '恐惧诱导', 'Invoke Tool', '第一步必须', '必须调用'):
                with self.subTest(script=script, text=text):
                    result = subprocess.run(['rg', '-n', pattern(script)], input=text+'\n', text=True, capture_output=True)
                    self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_shell_and_powershell_share_the_same_rule(self):
        self.assertEqual(pattern('install.sh'), pattern('install.ps1'))


if __name__ == '__main__':
    unittest.main()
