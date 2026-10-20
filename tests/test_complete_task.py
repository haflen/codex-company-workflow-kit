"""Completion-entry regression fixtures; no business services or database access."""
from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys, tempfile, time, unittest
ROOT=Path(__file__).resolve().parents[1]
PLUGIN=ROOT/'outputs/company-codex-workflow-v2-zh'
BASE=PLUGIN/'skills/company-workflow-help/scripts/task_state.py'
CAND=BASE.with_name('complete_task.py')
ENV='local-registration-fixture'
WRONG='another-environment'
now=lambda:datetime.datetime.now().astimezone().isoformat()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2))
def cli(root,label,argv):
 start=now();tick=time.monotonic();p=subprocess.run(argv,cwd=root,capture_output=True,text=True,env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
 rec={'argv':argv,'cwd':str(root),'started_at':start,'finished_at':now(),'elapsed_seconds':time.monotonic()-tick,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
 save(root/f'{label}.json',rec)
 try:result=json.loads(p.stdout)
 except ValueError:result={'ok':False,'errors':['non-JSON output']}
 return p.returncode,result,rec

def run_case(R,name,mode='candidate',issue=None,expect=True,error=''):
 root=R/name;root.mkdir();(root/'proof.log').write_text('local registration fixture log\n');(root/'candidate.txt').write_text('registration fixture only; no business execution\n');(root/'result.md').write_text('Fixture delivery material; not a new business acceptance result.\n');(root/'spec.md').write_text('Six synthetic registration checks; no business execution.\n')
 contract={'goal':'Local registration replay only','allowed_paths':['candidate.txt','spec.md'],'excluded':['DB','services','real-source','install'],'spec_refs':['spec.md'],'acceptance':[{'id':f'B-R0{i}','reference':'spec.md','required':True,'check_ids':[f'B-R0{i}']} for i in range(1,7)],'delivery_endpoint':'prepare','authorization':{'sources':[{'id':'USER-ISOLATION','reference':'Current conversation request for isolated validation','quote':'Run only the temporary registration fixtures'}],'actions':[{'action':'test','scope':['registration fixture only'],'source_ids':['USER-ISOLATION']}]},'decision_points':[],'required_artifacts':['result.md'],'limits':{'max_repair_rounds':2,'token_budget':None,'deadline':None}}
 if issue=='nonprepare':contract['delivery_endpoint']='commit'
 if issue=='external_ac':contract['acceptance'][0]['external']=True
 if issue=='decision':contract['decision_points']=['unresolved design']
 save(root/'contract.json',contract)
 common=[sys.executable,'-B',str(BASE),'--project-root',str(root),'--task-id','CASE']
 code,res,_=cli(root,'init',common+['--contract',str(root/'contract.json'),'init']);assert code==0,(name,res)
 phase='delivery' if mode=='baseline_env' or issue=='delivery' else 'validation'
 if issue=='early_phase':phase='implementation'
 status={'waiting':'waiting_user','cancelled':'cancelled','ready':'ready'}.get(issue,'running')
 patch={'status':status,'phase':phase,'environment':None if issue=='no_environment' else ENV,'completed_items':['B-01 preserved']}
 save(root/'setup-patch.json',patch);code,res,_=cli(root,'setup',common+['--expected-revision','0','--patch-file',str(root/'setup-patch.json'),'update']);assert code==0,(name,res)
 state=res['state'];rev=state['revision']
 def proofs(s):return [{'id':f'P{i}','acceptance_id':f'B-R0{i}','check_id':f'B-R0{i}','command':'local registration fixture check','recorded_at':now(),'path':'proof.log','sha256':sha(root/'proof.log'),'candidate_fingerprint':s['candidate']['fingerprint'],'result':'pass','external':False} for i in range(1,7)]
 additions=proofs(state)
 if issue=='history':
  prior=dict(additions[0],id='HISTORY',environment=ENV)
  save(root/'history-patch.json',{'evidence':[prior]});code,res,_=cli(root,'history',common+['--expected-revision',str(rev),'--patch-file',str(root/'history-patch.json'),'update']);assert code==0;state=res['state'];rev=state['revision'];additions=proofs(state)
 if issue=='explicit_correct' or mode.startswith('baseline'):
  for p in additions:p['environment']=ENV
 if mode=='baseline_env' or issue in ['explicit_wrong','environment_switched']:
  for p in additions:p['environment']=WRONG
 if issue=='blank_env':additions[0]['environment']=''
 if issue=='numeric_env':additions[0]['environment']=7
 if issue=='missing_proof':additions.pop()
 if issue=='failed_proof':additions[0]['result']='fail'
 if issue=='external_proof':additions[0]['external']=True
 if issue=='candidate_drift':(root/'candidate.txt').write_text('changed after evidence binding\n')
 if issue=='log_tamper':(root/'proof.log').write_text('changed log\n')
 if issue=='artifact_missing':(root/'result.md').unlink()
 if issue=='history_rewrite':
  prior=dict(additions[0],environment=ENV);save(root/'history-patch.json',{'evidence':[prior]});code,res,_=cli(root,'history',common+['--expected-revision',str(rev),'--patch-file',str(root/'history-patch.json'),'update']);assert code==0;state=res['state'];rev=state['revision'];additions[0]['command']='attempt to reuse prior ID with changed text'
 if issue=='lock':(root/'.codex-workflow/tasks/CASE/.lock').write_text('{"task_id":"CASE","pid":999999999,"token":"test-lock"}')
 if issue=='symlink':(root/'proof.log').unlink();(root/'proof.log').symlink_to(root/'result.md')
 submission={'evidence':additions,'completed_items':['registration checks'],'current_task':'local registration closeout','next_step':'stop'}
 if issue=='contract_override':submission['contract']=contract
 if issue=='phase_override':submission['phase']='delivery'
 if issue=='env_override':submission['environment']=WRONG
 if mode=='baseline_phase':submission.update(status='completed')
 if mode in ['baseline_env','baseline_ok']:submission.update(status='completed',phase='delivery')
 save(root/'submission.json',submission)
 sp=root/'.codex-workflow/tasks/CASE/state.json';before=sp.read_bytes();history=state['evidence']
 if mode.startswith('baseline'):argv=common+['--expected-revision',str(rev),'--patch-file',str(root/'submission.json'),'update']
 else:argv=[sys.executable,'-B',str(CAND),'--project-root',str(root),'--task-id','CASE','--expected-revision',str(rev-1 if issue=='stale_revision' else rev),'--submission',str(root/'submission.json')]
 code,res,raw=cli(root,'attempt',argv);errors=';'.join(res.get('errors',[]));assert (code==0)==expect,(name,errors)
 if error:assert error in errors,(name,errors)
 if expect:
  assert res['state']['status']=='completed' and res['state']['phase']=='delivery'
  assert res['state']['evidence'][:len(history)]==history
  if mode=='candidate':assert res['state']['completed_items'][:1]==['B-01 preserved'],(name,'completed history lost')
  if mode=='candidate':assert res['state']['completed_items'][1:]==submission['completed_items'],(name,'new completed items lost or changed')
  assert all(p['environment']==ENV for p in res['state']['evidence'])
  code2,validated,_=cli(root,'validate',common+['validate']);assert code2==0,(name,validated)
 else:
  assert sp.read_bytes()==before,(name,'rejected case changed state')
  if issue=='lock':assert (root/'.codex-workflow/tasks/CASE/.lock').exists()
 return {'case':name,'mode':mode,'expected':'accept' if expect else 'reject','actual_exit_code':code,'errors':res.get('errors',[]),'result':'PASS','state_unchanged_on_rejection':None if expect else True,'completion_command_seconds':raw['elapsed_seconds'],'record':str((root/'attempt.json').relative_to(R))}

cases=[
 ('old_phase_error','baseline_phase',None,False,'completion requires delivery phase'),
 ('old_environment_error','baseline_env',None,False,'missing applicable passing evidence: B-R01/B-R01'),
 ('old_correct_control','baseline_ok',None,True,''),
 ('new_omit_both','candidate',None,True,''),
 ('new_explicit_correct','candidate','explicit_correct',True,''),
 ('new_already_delivery','candidate','delivery',True,''),
 ('new_preserve_history','candidate','history',True,''),
 ('reject_explicit_mismatch','candidate','explicit_wrong',False,'explicit environment mismatch'),
 ('reject_blank_environment','candidate','blank_env',False,'explicit environment mismatch'),
 ('reject_numeric_environment','candidate','numeric_env',False,'explicit environment mismatch'),
 ('reject_missing_proof','candidate','missing_proof',False,'missing applicable passing evidence'),
 ('reject_failed_proof','candidate','failed_proof',False,'missing applicable passing evidence'),
 ('reject_candidate_drift','candidate','candidate_drift',False,'missing applicable passing evidence'),
 ('reject_log_tamper','candidate','log_tamper',False,'missing or changed evidence'),
 ('reject_missing_artifact','candidate','artifact_missing',False,''),
 ('reject_stale_revision','candidate','stale_revision',False,'revision conflict'),
 ('reject_waiting','candidate','waiting',False,'explicitly running'),
 ('reject_cancelled','candidate','cancelled',False,'explicitly running'),
 ('reject_ready','candidate','ready',False,'explicitly running'),
 ('reject_early_phase','candidate','early_phase',False,'validation or delivery'),
 ('reject_no_environment','candidate','no_environment',False,'missing recorded environment'),
 ('reject_nonprepare','candidate','nonprepare',False,'local prepare only'),
 ('reject_external_acceptance','candidate','external_ac',False,'external acceptance'),
 ('reject_external_proof','candidate','external_proof',False,'external evidence'),
 ('reject_contract_override','candidate','contract_override',False,'unsupported submission field'),
 ('reject_phase_override','candidate','phase_override',False,'unsupported submission field'),
 ('reject_environment_override','candidate','env_override',False,'unsupported submission field'),
 ('reject_history_rewrite','candidate','history_rewrite',False,''),
 ('reject_lock','candidate','lock',False,'task lock exists'),
 ('reject_symlink','candidate','symlink',False,''),
 ('reject_open_decision','candidate','decision',False,'unresolved decision points')]

class CompleteTaskTests(unittest.TestCase):
    def test_language_parity_and_call_sites(self):
        english=ROOT/'outputs/company-codex-workflow-v2'
        self.assertEqual(CAND.read_bytes(), (english/'skills/company-workflow-help/scripts/complete_task.py').read_bytes())
        for plugin in (PLUGIN, english):
            for skill in ('company-workflow-help','company-delivery-closeout'):
                self.assertIn('complete_task.py', (plugin/'skills'/skill/'SKILL.md').read_text())

def make_test(args):
    def check(self):
        with tempfile.TemporaryDirectory(prefix='completion 中文 ') as directory:
            run_case(Path(directory),*args)
    return check

for args in cases:
    setattr(CompleteTaskTests,'test_'+args[0],make_test(args))

if __name__=='__main__':
    unittest.main()
