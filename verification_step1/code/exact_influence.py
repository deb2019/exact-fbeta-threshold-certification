"""Exact single-label counterfactual influence on empirical F2 threshold selection.

Fixed finite scores, binary labels; no retraining. Tied scores move together.
The highest threshold (fewest predicted positives) wins exact metric ties.
Complexity O(n log n) including sorting, O(n) after sorting, O(n) memory.
No generalization, noise probability, or clean-performance guarantee is implied.
"""
import numpy as np

def _better(i,j,num,den):
    z=int(num[i])*int(den[j])-int(num[j])*int(den[i])
    return i if z>0 or (z==0 and i<j) else j

def _prefix(num,den):
    out=np.empty(len(num),dtype=int);best=0
    for i in range(len(num)):
        best=_better(i,best,num,den);out[i]=best
    return out

def _suffix(num,den):
    out=np.empty(len(num),dtype=int);best=len(num)-1
    for i in range(len(num)-1,-1,-1):
        best=_better(i,best,num,den);out[i]=best
    return out

def prepare(scores,labels):
    s=np.asarray(scores,dtype=float);y=np.asarray(labels)
    if len(s)==0 or s.ndim!=1 or y.shape!=s.shape or not np.isfinite(s).all() or not np.isin(y,[0,1]).all():
        raise ValueError('nonempty finite 1D scores and matching binary labels required')
    order=np.argsort(-s,kind='stable');ss=s[order];ys=y[order].astype(int)
    ends=np.r_[np.flatnonzero(ss[:-1]!=ss[1:]),len(s)-1]
    k=np.r_[0,ends+1];tp=np.r_[0,np.cumsum(ys)[ends]]
    groups=np.repeat(np.arange(1,len(k)),np.diff(k))
    return order,ys,k,tp,groups,np.r_[np.inf,ss[ends]]

def select(scores,labels):
    _,ys,k,tp,_,t=prepare(scores,labels)
    den=4*ys.sum()+k;den=np.maximum(den,1)
    best=int(_prefix(tp,den)[-1])
    return dict(index=best,k=int(k[best]),threshold=float(t[best]))

def all_single_flips(scores,labels):
    order,ys,k,tp,groups,t=prepare(scores,labels);P=int(ys.sum());n=len(ys)
    base=int(_prefix(tp,np.maximum(4*P+k,1))[-1]);changed=np.empty(n,dtype=int)
    for delta in [-1,1]:
        eligible=np.flatnonzero((1-2*ys)==delta)
        if not len(eligible):continue
        den=np.maximum(4*(P+delta)+k,1)
        left=_prefix(tp,den);right=_suffix(tp+delta,den)
        for pos in eligible:
            g=groups[pos];i=int(left[g-1]);j=int(right[g])
            # Left candidates exclude flipped item, right candidates include it.
            comparison=int(tp[i])*int(den[j])-int(tp[j]+delta)*int(den[i])
            changed[pos]=i if comparison>=0 else j
    indices=np.empty(n,dtype=int);indices[order]=changed
    return dict(base_index=base,base_k=int(k[base]),base_threshold=float(t[base]),
                changed_index=indices,changed_k=k[indices],changed_threshold=t[indices],
                disagreement_count=np.abs(k[indices]-k[base]),candidate_k=k,candidate_threshold=t)
