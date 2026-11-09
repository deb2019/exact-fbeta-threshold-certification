"""Independent exhaustive oracle for the three published ablation variants.

The oracle evaluates explicit prediction vectors with Fraction F-beta values.
It imports no preparation, winner, pruning, or recurrence from the tested code.
"""
from pathlib import Path
from itertools import product
from fractions import Fraction
from datetime import datetime, timezone
from collections import Counter
import hashlib, json, platform, sys, time
import numpy as np

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'code'))
from budget_ablation import solve
VARIANTS=[('pairwise_no_pruning',False,False),('pairwise_pruning',True,False),('deque_pruning',True,True)]

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def oracle_predictions(scores, labels, u, v):
    # Empty set is first; descending score thresholds implement highest-threshold ties.
    candidates=[tuple(False for _ in scores)]
    candidates += [tuple(s>=threshold for s in scores) for threshold in sorted(set(scores),reverse=True)]
    positive=sum(labels);best=Fraction(0);selected=candidates[0]
    for prediction in candidates:
        tp=sum(int(a and b) for a,b in zip(prediction,labels))
        denominator=u*positive+v*sum(prediction)
        f=Fraction((u+v)*tp,denominator) if denominator else Fraction(0)
        if f>best:best=f;selected=prediction
    return selected

def main():
    out=ROOT/'results';out.mkdir(exist_ok=True)
    if (out/'protocol.json').exists():raise RuntimeError('Use a fresh copy without results/; do not overwrite evidence')
    protocol={'started_utc':datetime.now(timezone.utc).isoformat(),
      'purpose':'New saved rerun of the described small-instance design; not recovery of the lost original inline script',
      'n':list(range(1,6)),'score_patterns':['distinct','paired_ties','all_tied'],
      'labels':'all 2^n binary vectors','beta_squared':[[1,4],[1,1],[4,1]],
      'distance':'sorted unique {1,max(1,n//2),n}','budget':'all integers 0..n',
      'oracle':'explicit threshold prediction vectors and exact Fraction F-beta; enumerate all edited labels',
      'tie_rule':'highest threshold; zero denominator objective=0',
      'variants':[x[0] for x in VARIANTS],
      'code_sha256':{p.name:sha(p) for p in sorted((ROOT/'code').glob('*.py'))},
      'verifier_sha256':sha(Path(__file__)),
      'python':sys.version,'numpy':np.__version__,'platform':platform.platform()}
    (out/'protocol.json').write_text(json.dumps(protocol,indent=2))
    scenarios=0;calls=0;mismatches=[];counts=Counter();start=time.perf_counter()
    with (out/'checks.jsonl').open('w') as record:
        for n in protocol['n']:
            vectors=list(product([0,1],repeat=n))
            for pattern in protocol['score_patterns']:
                scores=list(range(n)) if pattern=='distinct' else [i//2 for i in range(n)] if pattern=='paired_ties' else [0]*n
                for u,v in protocol['beta_squared']:
                    winners={y:oracle_predictions(scores,y,u,v) for y in vectors}
                    for y in vectors:
                        base=winners[y]
                        for d in sorted({1,max(1,n//2),n}):
                            costs=[sum(a!=b for a,b in zip(y,z)) for z in vectors if sum(a!=b for a,b in zip(base,winners[z]))>=d]
                            radius=min(costs) if costs else None
                            for budget in range(n+1):
                                expected=radius is not None and radius<=budget
                                answers={}
                                for name,prune,dq in VARIANTS:
                                    actual=bool(solve(scores,np.asarray(y),d,budget,pruning=prune,deque_dp=dq,u=u,v=v))
                                    calls+=1;answers[name]=actual
                                    if actual!=expected:mismatches.append({'scenario':scenarios,'variant':name})
                                row={'id':scenarios,'n':n,'pattern':pattern,'u':u,'v':v,'labels':y,'distance':d,'budget':budget,'oracle_minimum':radius,'expected':expected,'answers':answers}
                                record.write(json.dumps(row)+'\n');scenarios+=1;counts[str(n)]+=1
            print(f'n={n}: cumulative {scenarios} scenarios, {calls} variant checks; mismatches={len(mismatches)}',flush=True)
    result={'status':'passed' if not mismatches else 'failed','scenarios':scenarios,'variant_checks':calls,
      'by_n':dict(counts),'mismatches':mismatches,'elapsed_seconds':time.perf_counter()-start,
      'completed_utc':datetime.now(timezone.utc).isoformat(),'protocol_sha256':sha(out/'protocol.json'),'checks_sha256':sha(out/'checks.jsonl'),
      'limits':'Exhaustive labels within three score patterns for n<=5; not exhaustive over all score partitions or a proof for arbitrary n.'}
    (out/'summary.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
    if mismatches:raise SystemExit(1)

if __name__=='__main__':main()
