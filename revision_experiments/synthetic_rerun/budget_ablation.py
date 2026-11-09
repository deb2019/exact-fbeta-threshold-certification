import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'threshold_theory'))
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'threshold_influence'))
"""2x2 ablation for exact minimum-budget feasibility.

Factors: safe envelope/target/suffix pruning and linear deque transitions.
All variants retain the same integer optimality constraints and return exact
feasibility. This benchmark is exploratory and uses fixed synthetic cases.
"""
from collections import deque
from pathlib import Path
import json, statistics, time
import numpy as np
from minimum_budget import prepare, winner


def solve(scores, labels, distance, budget, *, pruning, deque_dp, u=4, v=1):
    order, ys, K, A, groups, thresholds = prepare(scores, labels)
    n = len(ys); P = int(A[-1]); g = len(K)-1
    base = winner(A, K, P, u, v)
    targets = np.flatnonzero(abs(K-K[base]) >= distance)
    if P <= budget and 0 in targets:
        return True

    for total in range(max(1, P-budget), min(n, P+budget)+1):
        delta = total-P
        if pruning:
            down=(budget-delta)//2; up=(budget+delta)//2
        den=[u*total+v*int(k) for k in K]
        L=[]; U=[]
        for j,(a,k) in enumerate(zip(A,K)):
            if pruning:
                lo=max(0,int(a)-down,total-(n-int(k)))
                hi=min(int(k),int(a)+up,total)
            else:
                lo=max(0,int(a)-budget,total-(n-int(k)))
                hi=min(int(k),int(a)+budget,total)
            L.append(lo); U.append(hi)
        best=0
        if pruning:
            for j in range(1,g+1):
                if L[j]*den[best] > L[best]*den[j]: best=j

        for target0 in targets:
            target=int(target0); D=den[target]
            for a in range(L[target],U[target]+1):
                if pruning:
                    if abs(a-int(A[target])) + abs(total-a-(P-int(A[target]))) > budget:
                        continue
                    cross=a*den[best]-L[best]*D
                    if cross<0 or (cross==0 and best<target) or (target>0 and a==0):
                        continue
                states={0:0}
                for j in range(1,g+1):
                    cap=(a*den[j]-(1 if j<target else 0))//D
                    lo=L[j]; hi=min(U[j],cap)
                    if j==target: lo=max(lo,a); hi=min(hi,a)
                    if j==g: lo=max(lo,total); hi=min(hi,total)
                    size=int(K[j]-K[j-1]); orig=int(A[j]-A[j-1])
                    if deque_dp:
                        nxt={}; keys=list(states); q1=deque();q2=deque();p1=p2=0
                        for c in range(lo,hi+1):
                            for qi,(q,which,qlo,qhi,sign) in enumerate([
                                (q1,0,c-size,c-orig,-1), (q2,1,c-orig,c,1)]):
                                ptr=p1 if qi==0 else p2
                                while ptr<len(keys) and keys[ptr]<=qhi:
                                    b=keys[ptr]; value=states[b]+sign*b
                                    while q and q[-1][1]>value:q.pop()
                                    q.append((b,value));ptr+=1
                                if qi==0:p1=ptr
                                else:p2=ptr
                                while q and q[0][0]<qlo:q.popleft()
                            opts=[]
                            if q1:
                                b,val=q1[0];opts.append((val+c-orig,b))
                            if q2:
                                b,val=q2[0];opts.append((val+orig-c,b))
                            if opts:
                                cost,_=min(opts)
                                if cost<=budget and (not pruning or cost+abs(total-c-(P-int(A[j])))<=budget):
                                    nxt[c]=cost
                    else:
                        nxt={}
                        for b,cost0 in states.items():
                            for c in range(max(lo,b),min(hi,b+size)+1):
                                cost=cost0+abs((c-b)-orig)
                                if cost<=budget and (not pruning or cost+abs(total-c-(P-int(A[j])))<=budget):
                                    if cost<nxt.get(c,budget+1):nxt[c]=cost
                    states=nxt
                    if not states:break
                if total in states and (target==0 or a>0):return True
    return False


def main():
    protocol={"seed":7122026,"n":[64,128,256],"patterns":["distinct","16groups"],
              "budget":2,"distance_fraction":0.05,"repeats":5,
              "variants":["pairwise_no_pruning","pairwise_pruning","deque_pruning"]}
    rng=np.random.default_rng(protocol['seed']); rows=[]
    for pattern in protocol['patterns']:
        for n in protocol['n']:
            s=rng.permutation(n).astype(float)
            if pattern=="16groups":s=np.floor(s*16/n)
            y=(rng.random(n)<.1).astype(int); d=int(np.ceil(.05*n)); B=protocol['budget']
            variants=[("pairwise_no_pruning",False,False),
                      ("pairwise_pruning",True,False),("deque_pruning",True,True)]
            times={};answers={}
            for rep in range(protocol['repeats']):
                run=variants if rep%2==0 else list(reversed(variants))
                for name,prune,dq in run:
                    t0=time.perf_counter()
                    answers[name]=solve(s,y,d,B,pruning=prune,deque_dp=dq)
                    times.setdefault(name,[]).append(time.perf_counter()-t0)
            assert len(set(answers.values()))==1,(pattern,n,answers)
            med={k:statistics.median(v) for k,v in times.items()}
            rows.append({"n":n,"g":len(set(s)),"pattern":pattern,"d":d,"B":B,
                         "feasible":next(iter(answers.values())),"median_seconds":med,
                         "speedup_vs_pairwise_no_pruning":{k:med['pairwise_no_pruning']/v for k,v in med.items()}})
            print(rows[-1],flush=True)
    out={"protocol":protocol,"rows":rows,"all_variant_feasibility_agrees":True}
    Path(__file__).with_name('budget_ablation_results.json').write_text(json.dumps(out,indent=2))
    print("Saved budget_ablation_results.json")

if __name__=="__main__":main()
