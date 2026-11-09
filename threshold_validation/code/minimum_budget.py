"""Exact bounded-budget threshold robustness, rational beta^2=u/v.
Fixed finite scores; smallest cutoff index wins ties. Research reference implementation.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'threshold_influence'))
import numpy as np
from exact_influence import prepare

def winner(A,K,P,u=4,v=1):
    if P==0:return 0
    best=0
    for j in range(1,len(K)):
        if int(A[j])*(u*P+v*int(K[best]))>int(A[best])*(u*P+v*int(K[j])):best=j
    return best

def within_budget(scores,labels,distance,budget,u=4,v=1):
    if not isinstance(u,int) or not isinstance(v,int) or min(u,v)<=0:raise ValueError('positive integer u,v required')
    order,ys,K,A,groups,thresholds=prepare(scores,labels)
    n=len(ys);P=int(A[-1]);g=len(K)-1
    if not 1<=distance<=n or not 0<=budget<=n:raise ValueError('invalid distance/budget')
    base=winner(A,K,P,u,v);targets=np.flatnonzero(abs(K-K[base])>=distance)
    # P'=0: all scores zero and tie policy selects cutoff 0.
    if P<=budget and 0 in targets:
        return {'feasible':True,'cost':P,'target':0,'labels':np.zeros(n,dtype=int).tolist(),'base':base}
    for total in range(max(1,P-budget),min(n,P+budget)+1):
        for target in targets:
            target=int(target);kt=int(K[target]);den=u*total+v*kt
            low=max(0,int(A[target])-budget,total-(n-kt))
            high=min(kt,total,int(A[target])+budget)
            for a in range(low,high+1):
                if target==0 and a!=0:continue
                states={0:0};parents=[]
                for j in range(1,g+1):
                    size=int(K[j]-K[j-1]);orig=int(A[j]-A[j-1])
                    # Strictly beat all earlier cutoffs; allow equality later.
                    cap=(a*(u*total+v*int(K[j]))-(1 if j<target else 0))//den
                    lower=max(0,int(A[j])-budget,total-(n-int(K[j])))
                    upper=min(int(K[j]),int(A[j])+budget,total,cap)
                    if j==target:lower=max(lower,a);upper=min(upper,a)
                    if j==g:lower=max(lower,total);upper=min(upper,total)
                    nxt={};parent={}
                    for c,cost in states.items():
                        for z in range(max(lower,c),min(upper,c+size)+1):
                            value=cost+abs((z-c)-orig)
                            if value<=budget and value<nxt.get(z,budget+1):nxt[z]=value;parent[z]=c
                    states=nxt;parents.append(parent)
                    if not states:break
                # Cutoff 0 is an earlier competitor whenever target>0;
                # if a=0 it wins the tie, so reject such candidates.
                if total in states and len(parents)==g and (target==0 or a>0):
                    counts=[];z=total
                    for j in range(g-1,-1,-1):
                        c=parents[j][z];counts.append(z-c);z=c
                    new=ys.copy()
                    for j,x in enumerate(reversed(counts),1):
                        ids=np.arange(K[j-1],K[j]);pos=ids[ys[ids]==1];neg=ids[ys[ids]==0]
                        if x<len(pos):new[pos[:len(pos)-x]]=0
                        else:new[neg[:x-len(pos)]]=1
                    out=np.empty(n,dtype=int);out[order]=new
                    return {'feasible':True,'cost':states[total],'target':target,'labels':out.tolist(),'base':base}
    return {'feasible':False,'base':base}

def minimum_budget(scores,labels,distance,max_budget=None,u=4,v=1):
    n=len(labels);limit=n if max_budget is None else max_budget
    for b in range(limit+1):
        out=within_budget(scores,labels,distance,b,u,v)
        if out['feasible']:return {**out,'minimum_budget':b}
    return {'feasible':False,'minimum_budget':None,'certified_lower_bound':limit+1}
