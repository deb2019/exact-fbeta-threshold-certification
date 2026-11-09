from pathlib import Path
from itertools import product
from fractions import Fraction
import sys,json,time,hashlib
import numpy as np
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R.parent/'threshold_theory'))
from budget_v2 import minimum_budget_v2

def candidates(s):return [tuple(False for _ in s)]+[tuple(x>=t for x in s) for t in sorted(set(s),reverse=True)]
def selected(pred,y,u,v,largest=False):
 values=[]
 for z in pred:
  den=u*sum(y)+v*sum(z);values.append(Fraction(sum(a*b for a,b in zip(z,y)),den) if den else Fraction(0))
 ties=[i for i,x in enumerate(values) if x==max(values)]
 return ties[-1] if largest else ties[0]

def main():
 start=time.perf_counter();checks=0;witnesses=0;ties_checked=0;failures=[]
 ratios=[(1,4),(1,1),(4,1),(10**40+7,10**39+3)]
 for n in range(1,5):
  labels=list(product([0,1],repeat=n))
  for boundaries in product([0,1],repeat=n-1):
   s=[0]
   for b in boundaries:s.append(s[-1]+b)
   pred=candidates(s);K=[sum(z) for z in pred];g=len(K)-1
   for u,v in ratios:
    wins={y:selected(pred,y,u,v) for y in labels}
    for y in labels:
     for d in range(1,n+1):
      possible=[sum(a!=b for a,b in zip(y,z)) for z in labels if abs(K[wins[y]]-K[wins[z]])>=d]
      radius=min(possible) if possible else None
      got=minimum_budget_v2(s,np.array(y),d,max_budget=n,u=u,v=v)
      if radius is None:assert got['status']=='lower_bound' and got['certified_lower_bound']==n+1
      else:
       assert got['status']=='exact' and got['minimum_budget']==radius
       z=tuple(got['labels']);assert sum(a!=b for a,b in zip(y,z))==radius
       assert abs(K[selected(pred,z,u,v)]-K[wins[y]])>=d;witnesses+=1
      checks+=1
    # Check strict-inequality characterization for both deterministic tie policies.
    for y in labels:
     P=sum(y)
     for largest in [False,True]:
      expected=selected(pred,y,u,v,largest)
      if not P:assert expected==(g if largest else 0);ties_checked+=1;continue
      C=[sum(a*b for a,b in zip(z,y)) for z in pred]
      accepted=[]
      for k in range(g+1):
       D=u*P+v*K[k];a=C[k]
       if all(C[j]*D<=a*(u*P+v*K[j])-int(j>k if largest else j<k) for j in range(g+1)):accepted.append(k)
      assert accepted==[expected];ties_checked+=1
  print(n,checks,witnesses,ties_checked,flush=True)
 result={'status':'passed','production_radius_checks':checks,'witness_checks':witnesses,'tie_constraint_checks':ties_checked,'n_max':4,'patterns':'all ordered contiguous tie partitions','beta_squared_pairs':ratios,'elapsed_seconds':time.perf_counter()-start,'limitations':'All partitions through n=4; not arbitrary-n proof. Alternate tie constraints verified; production solver remains smallest-index only.','code_hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),R.parent/'threshold_theory/budget_v2.py',R.parent/'threshold_theory/minimum_budget.py']}}
 (R/'audit_results.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
if __name__=='__main__':main()
