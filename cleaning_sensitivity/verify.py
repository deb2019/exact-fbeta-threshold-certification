from pathlib import Path
import sys,json,hashlib
import numpy as np
from run_sensitivity import direct,all_single_flips,minimum_budget_v2
R=Path(__file__).resolve().parent
r=json.loads((R/'results.json').read_text());c=json.loads((R/'completed.json').read_text())
for f,k in [('protocol.json','protocol_sha256'),('results.json','results_sha256')]:assert hashlib.sha256((R/f).read_bytes()).hexdigest()==c[k]
w=0
for file in (R/'scores').glob('*.npz'):
 a=np.load(file)
 for suffix in ['id','group']:
  tr,va,te=[set(a[x+'_'+suffix].tolist()) for x in ['train','validation','test']]
  assert not(tr&va or tr&te or va&te)
 assert len(a['validation_y'])==len(a['validation_score'])==len(a['validation_id'])
for x in r['rows']:
 a=np.load(R/'scores'/(x['run']+'.npz'));s=a['validation_score'];y=a['validation_y']
 one=all_single_flips(s,y);assert bool(max(one['disagreement_count'])>=x['d'])==(x.get('minimum_budget')==1)
 z=minimum_budget_v2(s,y,x['d'],max_budget=2,time_limit=5)
 for k in ['status','minimum_budget','certified_lower_bound']:assert z.get(k)==x.get(k)
 if x['status']=='exact':
  edited=y.copy();edited[x['witness_indices']]=1-edited[x['witness_indices']]
  assert sum(edited!=y)==x['minimum_budget'];assert abs(direct(s,edited)-direct(s,y))>=x['d'];w+=1
# Shared feature groups always retain the raw-arm split assignment across arms.
for d in ['blood','mammographic']:
 for seed in [20261019,20261020,20261021]:
  for m in ['LR','RF']:
   base=np.load(R/'scores'/f'{d}_{seed}_{m}_all_rows.npz')
   for arm in ['deduplicate_same_label','exclude_conflicts']:
    alt=np.load(R/'scores'/f'{d}_{seed}_{m}_{arm}.npz')
    for part in ['train','validation','test']:assert set(alt[part+'_group']).issubset(set(base[part+'_group']))
print(json.dumps(dict(status='passed',analyses=len(r['rows']),witnesses=w,score_vectors=len(list((R/'scores').glob('*.npz'))),group_disjoint_and_shared_assignment=True),indent=2))
