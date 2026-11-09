from pathlib import Path
import sys,json,hashlib
import numpy as np
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R))
from run_benchmarks import direct,all_single_flips,minimum_budget_v2
counts=dict(analyses=0,witnesses=0,score_vectors=0,splits=0)
for base in [R.parent/'threshold_validation',R]:
 data=json.loads((base/'results.json').read_text());completion=json.loads((base/'completed.json').read_text())
 for f,k in [('protocol.json','protocol_sha256'),('results.json','results_sha256')]:assert hashlib.sha256((base/f).read_bytes()).hexdigest()==completion[k]
 for file in (base/'scores').glob('*.npz'):
  a=np.load(file);tr,va,te=[set(a[k].tolist()) for k in ['train_id','validation_id','test_id']]
  assert not(tr&va or tr&te or va&te);assert len(va)==len(a['validation_y'])==len(a['validation_score']);counts['score_vectors']+=1;counts['splits']+=1
 for row in data['rows']:
  a=np.load(base/'scores'/(row['run']+'.npz'));s=a['validation_score'];y=a['validation_y']
  one=all_single_flips(s,y);assert bool(max(one['disagreement_count'])>=row['d'])==(row.get('minimum_budget')==1)
  r=minimum_budget_v2(s,y,row['d'],max_budget=2,time_limit=5)
  for key in ['status','minimum_budget','certified_lower_bound']:assert r.get(key)==row.get(key)
  if row['status']=='exact':
   z=y.copy();z[row['witness_indices']]=1-z[row['witness_indices']]
   assert sum(z!=y)==row['minimum_budget'];assert abs(direct(s,z)-direct(s,y))>=row['d'];counts['witnesses']+=1
  counts['analyses']+=1
print(json.dumps(dict(status='passed',**counts),indent=2))
