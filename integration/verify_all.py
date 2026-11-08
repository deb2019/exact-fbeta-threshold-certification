from pathlib import Path
import sys,subprocess,json,hashlib
R=Path(__file__).resolve().parent.parent
manifest=R/'SHA256_MANIFEST.json'
if manifest.exists():
 for f,h in json.loads(manifest.read_text()).items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h,f
results=[]
for script in ['source_benchmarks/verify_release.py','cleaning_sensitivity/verify.py','scalability/verify.py','rare_benchmark/verify.py']:
 p=subprocess.run([sys.executable,str(R/script)],cwd=R,text=True,capture_output=True,check=True)
 results.append(dict(script=script,**json.loads(p.stdout)))
assert sum(x['analyses'] for x in results)==216
assert sum(x['witnesses'] for x in results)==145
p=subprocess.run([sys.executable,str(R/'revision_experiments/verify_new.py')],cwd=R,text=True,capture_output=True,check=True)
revision=json.loads(p.stdout)
extension={}
if (R/'prepared_extension/verify.py').exists():
 q=subprocess.run([sys.executable,str(R/'prepared_extension/verify.py')],cwd=R,text=True,capture_output=True,check=True)
 extension=json.loads(q.stdout)
print(json.dumps(dict(prepared_extension=extension,revision_checks=revision,status='passed',analyses=216,witnesses=145,score_vectors=108,phases=results),indent=2))
