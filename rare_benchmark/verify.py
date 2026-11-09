from pathlib import Path
import json,math,numpy as np
from run import load,direct,all_single_flips,minimum_budget_v2,sha
R=Path(__file__).resolve().parent;p=json.loads((R/'protocol.json').read_text());c=json.loads((R/'completed.json').read_text())
assert sha(R/'raw/ozone.zip')==p['raw_sha256'];assert sha(R/'results.json')==c['results_sha256'];assert sha(R/'protocol.json')==c['protocol_sha256']
X,y,groups=load();rows=json.loads((R/'results.json').read_text());w=0
assert len(rows)==12;assert len(list((R/'scores').glob('*.npz')))==6
for file in (R/'scores').glob('*.npz'):
 a=np.load(file);sets=[a[k] for k in ['train_id','validation_id','test_id']];assert sorted(np.concatenate(sets).tolist())==list(range(len(y)))
 for i in range(3):
  for j in range(i):assert not set(groups[sets[i]])&set(groups[sets[j]])
 assert np.array_equal(y[a['validation_id']],a['validation_y']);assert np.isfinite(a['validation_score']).all()
 s=a['validation_score'];v=a['validation_y'];one=all_single_flips(s,v)
 for row in [x for x in rows if x['run']==file.stem]:
  assert row['n']==len(v) and row['positives']==int(v.sum()) and row['g']==len(np.unique(s));assert row['d']==math.ceil(row['fraction']*len(v))
  r=minimum_budget_v2(s,v,row['d'],max_budget=2,time_limit=5)
  for k in ['status','minimum_budget','certified_lower_bound']:assert r.get(k)==row.get(k)
  if row['status']!='timeout':assert bool(max(one['disagreement_count'])>=row['d'])==(row.get('minimum_budget')==1)
  if row['status']=='exact':
   vv=v.copy();vv[row['witness_indices']]=1-vv[row['witness_indices']];assert sum(vv!=v)==row['minimum_budget'];assert direct(s,v)==row['old_k'];assert direct(s,vv)==row['new_k'];assert abs(row['new_k']-row['old_k'])>=row['d'];w+=1
print(json.dumps(dict(status='passed',analyses=len(rows),witnesses=w,score_vectors=6,all_rows_retained=True,group_disjoint=True,raw_n=len(y),raw_positives=int(y.sum())),indent=2))
