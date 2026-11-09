from pathlib import Path
import sys,time,itertools
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import coo_matrix
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'threshold_theory'))
from budget_v2 import BudgetSolver,minimum_budget_v2
from minimum_budget import prepare,winner

def batch_winners(A,K,P,u=4,v=1):
    den=u*P[:,None]+v*K[None,:];den=np.maximum(den,1)
    ix=np.tile(np.arange(len(K)),(len(P),1));rr=np.arange(len(P))[:,None]
    while ix.shape[1]>1:
        even=ix.shape[1]//2*2;l=ix[:,:even:2];r=ix[:,1:even:2]
        win=np.where(A[rr,l]*den[rr,r]>=A[rr,r]*den[rr,l],l,r)
        ix=np.concatenate([win,ix[:,-1:]],axis=1) if even<ix.shape[1] else win
    return ix[:,0]

def scan(s,y,d,B=2,u=4,v=1,seconds=5):
    start=time.perf_counter();order,ys,K,A,groups,_=prepare(s,y);n=len(y);P=int(sum(y));base=winner(A,K,P,u,v)
    assert (u+v)*n*n*4<2**63
    types=[]
    for h in range(1,len(K)):
        for label in [0,1]:
            ids=np.flatnonzero((groups==h)&(ys==label))
            if len(ids):types.append((h,1-2*label,ids[:2],len(ids)))
    tested=0
    for b in range(1,B+1):
        stream=((i,) for i in range(len(types))) if b==1 else itertools.combinations_with_replacement(range(len(types)),2)
        while True:
            batch=list(itertools.islice(stream,256))
            if not batch:break
            if time.perf_counter()-start>seconds:return dict(status='timeout',certified_lower_bound=b,tested=tested)
            if b==2:batch=[z for z in batch if z[0]!=z[1] or types[z[0]][3]>=2]
            if not batch:continue
            aa=np.tile(A,(len(batch),1));pp=np.full(len(batch),P,dtype=np.int64)
            for col in range(b):
                tt=[types[z[col]] for z in batch];h=np.array([z[0] for z in tt]);delta=np.array([z[1] for z in tt]);aa+=delta[:,None]*(np.arange(len(K))[None,:]>=h[:,None]);pp+=delta
            winners=batch_winners(aa,K,pp,u,v);tested+=len(batch);ok=np.flatnonzero(abs(K[winners]-K[base])>=d)
            if len(ok):
                chosen=batch[int(ok[0])];ed=[]
                for j,t in enumerate(chosen):ed.append(int(order[types[t][2][1 if j and chosen[j-1]==t else 0]]))
                return dict(status='exact',minimum_budget=b,witness_indices=ed,tested=tested)
    return dict(status='lower_bound',certified_lower_bound=B+1,tested=tested)

def integer_program(s,y,d,B=2,u=4,v=1,seconds=5):
    start=time.perf_counter();order,ys,K,A,groups,_=prepare(s,y);n=len(y);P=int(sum(y));g=len(K)-1;base=winner(A,K,P,u,v)
    targets=np.flatnonzero(abs(K-K[base])>=d);best=None;unknown=False;statuses=[]
    if P<=B and 0 in targets:best=(P,np.flatnonzero(np.asarray(y)==1).tolist())
    targets=targets[targets>0];nt=len(targets)
    if not nt:return dict(status='exact',minimum_budget=best[0],witness_indices=best[1]) if best else dict(status='lower_bound',certified_lower_bound=B+1)
    # C_0..C_g integer cumulative counts; e_1..e_g integer edit bounds; q target selectors.
    nc=g+1;offe=nc;offq=nc+g;nv=offq+nt
    for total in range(max(1,P-B),min(n,P+B)+1):
        if time.perf_counter()-start>seconds:unknown=True;break
        rr=[];cc=[];vv=[];lower=[];upper=[]
        def add(cols,vals,lo,hi):
            k=len(lower);rr.extend([k]*len(cols));cc.extend(cols);vv.extend(vals);lower.append(lo);upper.append(hi)
        for j in range(1,g+1):
            m=int(K[j]-K[j-1]);p=int(A[j]-A[j-1]);e=offe+j-1
            add([j,j-1],[1,-1],0,m)
            add([j,j-1,e],[1,-1,-1],-np.inf,p)
            add([j,j-1,e],[-1,1,-1],-np.inf,-p)
        add(list(range(offe,offq)),[1]*g,0,B)
        add(list(range(offq,nv)),[1]*nt,1,1)
        # Indicator constraints linearized with valid, target-specific big-M constants.
        for t,k in enumerate(targets):
            D=u*total+v*int(K[k]);minck=max(0,total-(n-int(K[k])))
            for j in range(g+1):
                if j==k:continue
                qj=u*total+v*int(K[j]);strict=int(j<k)
                M=max(0,D*min(int(K[j]),total)-qj*minck+strict)
                add([j,int(k),offq+t],[D,-qj,M],-np.inf,M-strict)
        remaining=seconds-(time.perf_counter()-start)
        if remaining<=0:unknown=True;break
        matrix=coo_matrix((vv,(rr,cc)),shape=(len(lower),nv)).tocsc()
        lb=np.zeros(nv);ub=np.r_[np.minimum(K,total),np.full(g,B),np.ones(nt)].astype(float);lb[g]=ub[g]=total
        objective=np.r_[np.zeros(nc),np.ones(g),np.zeros(nt)]
        res=milp(objective,integrality=np.ones(nv),bounds=Bounds(lb,ub),constraints=LinearConstraint(matrix,lower,upper),options={'time_limit':remaining,'mip_rel_gap':0})
        statuses.append(int(res.status))
        if res.status not in [0,2]:unknown=True
        if res.x is not None:
            C=np.rint(res.x[:nc]).astype(int);new=ys.copy()
            for j in range(1,g+1):
                ids=np.arange(K[j-1],K[j]);pos=ids[ys[ids]==1];neg=ids[ys[ids]==0];x=int(C[j]-C[j-1])
                if x<len(pos):new[pos[:len(pos)-x]]=0
                else:new[neg[:x-len(pos)]]=1
            edits=np.flatnonzero(new!=ys);out=np.empty(n,dtype=int);out[order]=new
            # Exact objective/tie check, independent of solver floating-point tolerance.
            _,ny,nK,nA,_,_=prepare(s,out);newk=winner(nA,nK,int(sum(out)),u,v)
            valid=len(edits)<=B and abs(int(nK[newk])-int(K[base]))>=d
            if not valid:raise AssertionError('MILP candidate failed exact integer validation')
            if best is None or len(edits)<best[0]:best=(len(edits),np.flatnonzero(out!=y).tolist())
            if best[0]==1:return dict(status='exact',minimum_budget=1,witness_indices=best[1],solver_statuses=statuses)
    if unknown:return dict(status='timeout',certified_lower_bound=1,upper_bound=None if best is None else best[0],solver_statuses=statuses)
    if best:return dict(status='exact',minimum_budget=best[0],witness_indices=best[1],solver_statuses=statuses)
    return dict(status='lower_bound',certified_lower_bound=B+1,solver_statuses=statuses)

def dp(s,y,d,B=2,u=4,v=1,seconds=5):
    r=minimum_budget_v2(s,y,d,max_budget=B,u=u,v=v,time_limit=seconds)
    if 'labels' in r:r['witness_indices']=np.flatnonzero(np.asarray(r.pop('labels'))!=y).tolist()
    return r
