import itertools,json,time
import numpy as np
from fractions import Fraction
from minimum_budget import minimum_budget
from pathlib import Path

def direct(s,y,u,v):
    cuts=[np.inf]+sorted(set(s),reverse=True);best=Fraction(-1);out=None
    for t in cuts:
        pred=s>=t;k=int(pred.sum());p=int(sum(y));tp=int(np.asarray(y)[pred].sum())
        f=Fraction(tp,u*p+v*k) if u*p+v*k else Fraction(0)
        if f>best:best=f;out=pred
    return out
start=time.time();checks=0;witnesses=0
for n in range(1,6):
    ys=list(itertools.product([0,1],repeat=n))
    for s in [np.arange(n,dtype=float),np.arange(n)//2,np.zeros(n)]:
        for u,v in [(1,4),(1,1),(4,1)]:
            preds=[direct(s,y,u,v) for y in ys]
            for a,y in enumerate(ys):
                for d in sorted(set([1,max(1,n//2),n])):
                    candidates=[sum(x!=z for x,z in zip(y,yy)) for yy,pp in zip(ys,preds) if sum(preds[a]!=pp)>=d]
                    expected=min(candidates) if candidates else None
                    result=minimum_budget(s,y,d,u=u,v=v);assert result['minimum_budget']==expected,(n,s,y,d,u,v,result,expected)
                    if result['feasible']:
                        yy=result['labels'];assert sum(x!=z for x,z in zip(y,yy))==expected
                        assert sum(direct(s,yy,u,v)!=preds[a])>=d;witnesses+=1
                    checks+=1
out={'configurations_distance_beta_checks':checks,'independent_witness_checks':witnesses,'exhaustive_n':'1..5','beta_squared':['1/4','1','4'],'patterns':['distinct','paired ties','all tied'],'seconds':time.time()-start,'all_passed':True}
Path(__file__).with_name('budget_verification.json').write_text(json.dumps(out,indent=2));print(out)
