from pathlib import Path
import json,sys,hashlib
import numpy as np
from fractions import Fraction
R=Path(__file__).resolve().parent
BASE=R.parent/'base' if (R.parent/'base').exists() else R.parent
sys.path.insert(0,str(BASE/'threshold_validation'))
from run_validation import all_single_flips,minimum_budget_v2

def winner(s,y):
 order=np.argsort(-s,kind='stable');a=0;P=int(sum(y));best=Fraction(0);k=0
 for j,i in enumerate(order):
  a+=int(y[i])
  if j+1<len(s) and s[i]==s[order[j+1]]:continue
  f=Fraction(a,4*P+j+1)
  if f>best:best=f;k=j+1
 return k

def main():
 vectors=analyses=witnesses=0;counts={}
 for p in sorted((R/'results').glob('*/completed.json')):
  rows=json.loads((p.parent/'results.json').read_text());assert len(rows)==12==json.loads(p.read_text())['analyses'];cache={}
  for row in rows:
   run=row['run']
   if run not in cache:
    z=np.load(p.parent/(run+'.npz'));s=z['validation_score'];y=z['validation_y'];assert np.isfinite(s).all()
    assert len(s)==len(y)==len(z['validation_id'])
    for a,b in [('train_id','validation_id'),('train_id','test_id'),('validation_id','test_id')]:assert not set(z[a])&set(z[b])
    cache[run]=(s,y,winner(s,y),int(max(all_single_flips(s,y)['disagreement_count'])));vectors+=1
   s,y,k,one=cache[run];assert row['max_single_edit_disagreement']==one
   status=row['status'];counts[status]=counts.get(status,0)+1;analyses+=1
   if status!='timeout':assert (one>=row['d'])==(row.get('minimum_budget')==1)
   if status=='exact':
    yy=y.copy();idx=row['witness_indices'];yy[idx]=1-yy[idx];assert len(set(idx))==row['minimum_budget'];assert winner(s,yy)==row['new_k'];assert abs(winner(s,yy)-k)>=row['d'];witnesses+=1
   # Replay completed budget verdicts, allowing more time under changed load.
   if status!='timeout':
    rr=minimum_budget_v2(s,y,row['d'],max_budget=2,time_limit=30)
    assert rr['status']==status,(run,status,rr)
    key='minimum_budget' if status=='exact' else 'certified_lower_bound'
    assert rr[key]==row[key]
 result=dict(status='passed',complete_tasks=len(list((R/'results').glob('*/completed.json'))),analyses=analyses,vectors=vectors,witnesses=witnesses,outcomes=counts)
 print(json.dumps(result,indent=2));(R/'verification.json').write_text(json.dumps(result,indent=2))
if __name__=='__main__':main()
