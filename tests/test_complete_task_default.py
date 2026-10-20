"""No -B or caller env workaround: read/help paths must not modify tool files."""
import json,os,shutil,subprocess,sys,tempfile,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
PLUGINS=[R/'outputs'/name for name in ('company-codex-workflow-v2-zh','company-codex-workflow-v2')]
class DefaultInvocation(unittest.TestCase):
    def check(self,args,expected):
        for plugin in PLUGINS:
            with self.subTest(plugin=plugin.name):
                self.check_plugin(plugin,args,expected)

    def check_plugin(self,plugin,args,expected):
        with tempfile.TemporaryDirectory(prefix='tool-default 中文 ') as temp:
            p=Path(temp)
            for f in ('complete_task.py','task_state.py'):
                shutil.copy2(plugin/'skills/company-workflow-help/scripts'/f,p/f)
            before={f.name:f.read_bytes() for f in p.iterdir()}
            env=dict(os.environ)
            for key in ('PYTHONDONTWRITEBYTECODE','PYTHONPYCACHEPREFIX'): env.pop(key,None)
            proc=subprocess.run([sys.executable,str(p/'complete_task.py'),*args],cwd=p,env=env,capture_output=True,text=True)
            self.assertEqual(proc.returncode,expected,(proc.stdout,proc.stderr))
            for name,data in before.items():self.assertEqual((p/name).read_bytes(),data)
            self.assertEqual(sorted(str(f.relative_to(p)) for f in p.rglob('*') if f.is_file()),sorted(before),'read/rejected call wrote tool files')
    def test_help(self): self.check(['--help'],0)
    def test_short_help(self): self.check(['-h'],0)
    def test_missing_args(self): self.check([],2)
    def test_invalid_revision(self):self.check(['--project-root','.','--task-id','CASE','--expected-revision','bad','--submission','missing.json'],2)
    def test_missing_submission(self):self.check(['--project-root','.','--task-id','CASE','--expected-revision','1','--submission','missing.json'],2)
if __name__=='__main__':unittest.main()
