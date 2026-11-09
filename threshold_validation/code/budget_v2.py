"""Exact budget DP with necessary-envelope pruning and linear-time stages.
Rational beta squared u/v; fixed scores; highest threshold wins objective ties.
No rounding of scores and no approximation of feasible label edits.
"""
from collections import deque
import time
import numpy as np
from minimum_budget import prepare,winner

class BudgetTimeout(TimeoutError):pass

def transition(states,lower,upper,size,orig,budget,remaining_original,total):
    keys=list(states);queues=[deque(),deque()];pointers=[0,0];out={};parents={}
    for c in range(lower,upper+1):
        options=[]
        for side,(lo,hi,sign) in enumerate([(c-size,c-orig,-1),(c-orig,c,1)]):
            queue=queues[side];i=pointers[side]
            while i<len(keys) and keys[i]<=hi:
                b=keys[i];value=states[b]+sign*b
                while queue and queue[-1][1]>value:queue.pop()
                queue.append((b,value));i+=1
            pointers[side]=i
            while queue and queue[0][0]<lo:queue.popleft()
            if queue:
                b,value=queue[0];cost=value+(c-orig if side==0 else orig-c)
                options.append((cost,b))
        if options:
            cost,b=min(options)
            if cost+abs(total-c-remaining_original)<=budget:
                out[c]=cost;parents[c]=b
    return out,parents

class BudgetSolver:
    def __init__(self,scores,labels,u=4,v=1):
        if not isinstance(u,int) or not isinstance(v,int) or min(u,v)<=0:raise ValueError('positive integer u,v')
        self.order,self.ys,self.K,self.A,self.groups,self.thresholds=prepare(scores,labels)
        self.n=len(self.ys);self.P=int(self.A[-1]);self.g=len(self.K)-1;self.u=u;self.v=v
        self.base=winner(self.A,self.K,self.P,u,v)
    def within(self,distance,budget,time_limit=None):
        n,P,g,u,v=self.n,self.P,self.g,self.u,self.v;K,A=self.K,self.A
        if not 1<=distance<=n or not 0<=budget<=n:raise ValueError('invalid distance/budget')
        start=time.perf_counter();deadline=float('inf') if time_limit is None else start+time_limit
        stats={'candidate_counts':0,'envelope_pruned':0,'dp_started':0,'dp_stages':0}
        def checktime():
            if time.perf_counter()>deadline:raise BudgetTimeout('Time limit reached; infeasibility NOT established')
        targets=np.flatnonzero(abs(K-K[self.base])>=distance)
        if P<=budget and 0 in targets:return {'feasible':True,'cost':P,'target':0,'labels':np.zeros(n,dtype=int).tolist(),'base':self.base,'stats':stats}
        for total in range(max(1,P-budget),min(n,P+budget)+1):
            delta=total-P;down=(budget-delta)//2;up=(budget+delta)//2
            den=[u*total+v*int(k) for k in K]
            L=[max(0,int(a)-down,total-(n-int(k))) for a,k in zip(A,K)]
            U=[min(int(k),int(a)+up,total) for a,k in zip(A,K)]
            best=0
            for j in range(1,g+1):
                if L[j]*den[best]>L[best]*den[j]:best=j
            for target in targets:
                checktime();target=int(target);D=den[target]
                for a in range(L[target],U[target]+1):
                    stats['candidate_counts']+=1
                    if abs(a-int(A[target]))+abs(total-a-(P-int(A[target])))>budget:continue
                    cross=a*den[best]-L[best]*D
                    if cross<0 or (cross==0 and best<target) or (target>0 and a==0):
                        stats['envelope_pruned']+=1;continue
                    stats['dp_started']+=1;states={0:0};parents=[]
                    for j in range(1,g+1):
                        if j%128==0:checktime()
                        stats['dp_stages']+=1
                        cap=(a*den[j]-(1 if j<target else 0))//D
                        lower=L[j];upper=min(U[j],cap)
                        if j==target:lower=max(lower,a);upper=min(upper,a)
                        if j==g:lower=max(lower,total);upper=min(upper,total)
                        states,parent=transition(states,lower,upper,int(K[j]-K[j-1]),int(A[j]-A[j-1]),budget,P-int(A[j]),total)
                        parents.append(parent)
                        if not states:break
                    if total in states and len(parents)==g:
                        counts=[];z=total
                        for j in range(g-1,-1,-1):c=parents[j][z];counts.append(z-c);z=c
                        new=self.ys.copy()
                        for j,x in enumerate(reversed(counts),1):
                            ids=np.arange(K[j-1],K[j]);pos=ids[self.ys[ids]==1];neg=ids[self.ys[ids]==0]
                            if x<len(pos):new[pos[:len(pos)-x]]=0
                            else:new[neg[:x-len(pos)]]=1
                        out=np.empty(n,dtype=int);out[self.order]=new
                        return {'feasible':True,'cost':states[total],'target':target,'labels':out.tolist(),'base':self.base,'stats':stats}
        return {'feasible':False,'base':self.base,'stats':stats}

def minimum_budget_v2(scores,labels,distance,max_budget=None,u=4,v=1,time_limit=None):
    solver=BudgetSolver(scores,labels,u,v);limit=solver.n if max_budget is None else max_budget
    start=time.perf_counter()
    for b in range(limit+1):
        remaining=None if time_limit is None else time_limit-(time.perf_counter()-start)
        if remaining is not None and remaining<=0:return {'status':'timeout','certified_lower_bound':b}
        try:r=solver.within(distance,b,remaining)
        except BudgetTimeout:return {'status':'timeout','certified_lower_bound':b}
        if r['feasible']:return {**r,'status':'exact','minimum_budget':b}
    return {'status':'lower_bound','certified_lower_bound':limit+1}
