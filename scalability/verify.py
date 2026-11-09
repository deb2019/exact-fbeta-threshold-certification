from pathlib import Path
import json,hashlib
import numpy as np
from run_scalability import direct,all_single_flips,minimum_budget_v2
R=Path(__file__).resolve().parent
r=json.loads((R/'results.json').read_text());c=json.loads((R/'completed.json').read_text())
for f,k in [('protocol.json','protocol_sha256'),('results.json','results_sha256')]:assert hashlib.sha256((R/f).read_bytes()).hexdigest()==c[k]
w=0
for file in (R/'scores').glob('*.npz'):
 a=np.load(file);assert not set(a['train_id'])&set(a['validation_id']);assert not set(a['train_group'])&set(a['validation_group']);assert len(a['validation_id'])==len(a['validation_score'])==len(a['validation_y'])
for x in r:
 a=np.load(R/'scores'/(x['run']+'.npz'));s=a['validation_score'];y=a['validation_y']
 z=minimum_budget_v2(s,y,x['d'],max_budget=2,time_limit=5)
 for k in ['status','minimum_budget','certified_lower_bound']:assert z.get(k)==x.get(k)
 if x['status']!='timeout':assert bool(max(all_single_flips(s,y)['disagreement_count'])>=x['d'])==(x.get('minimum_budget')==1)
 if x['status']=='exact':
  edited=y.copy();edited[x['witness_indices']]=1-edited[x['witness_indices']];assert sum(edited!=y)==x['minimum_budget'];assert abs(direct(s,edited)-direct(s,y))>=x['d'];w+=1
for seed in [20261022,20261023,20261024]:
 for model in ['LR','RF']:
  full=np.load(R/'scores'/f'bank_{seed}_{model}_full.npz')
  for n in [1000,5000,10000]:
   a=np.load(R/'scores'/f'bank_{seed}_{model}_{n}.npz')
   for k in ['validation_id','validation_score','validation_y']:assert np.array_equal(a[k],full[k][:n])
print(json.dumps(dict(status='passed',analyses=len(r),witnesses=w,score_vectors=24,nested_subsets_and_group_disjointness=True),indent=2))
