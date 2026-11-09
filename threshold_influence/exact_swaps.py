"""Exact F2 threshold sensitivity to every positive/negative label swap.
Requires exact_influence.py beside this file. Fixed scores; highest threshold wins ties.
O(n log n + gp*gn) time, O(n log n) memory; gp/gn are score groups containing
positive/negative labels. Individual pairs in identical groups are counted with multiplicity.
"""
import numpy as np
from exact_influence import prepare,_prefix,_suffix

def better(a,b,num,den):
    cross=num[a]*den[b]-num[b]*den[a]
    return np.where((cross>0)|((cross==0)&(a<b)),a,b)

class RMQ:
    def __init__(self,num,den):
        self.num=num;self.den=den;self.tables=[np.arange(len(num))]
        self.logs=np.zeros(len(num)+1,dtype=int)
        for i in range(2,len(self.logs)):self.logs[i]=self.logs[i//2]+1
        half=1
        while 2*half<=len(num):
            old=self.tables[-1];length=len(num)-2*half+1
            self.tables.append(better(old[:length],old[half:half+length],num,den));half*=2
        self.matrix=np.full((len(self.tables),len(num)),-1,dtype=int)
        for level,tab in enumerate(self.tables):self.matrix[level,:len(tab)]=tab
        del self.tables
    def query(self,lo,hi):
        levels=self.logs[hi-lo+1]
        return better(self.matrix[levels,lo],self.matrix[levels,hi-(1<<levels)+1],self.num,self.den)

class SwapAnalyzer:
    def __init__(self,s,y):
        self.s=np.asarray(s);self.y=np.asarray(y)
        order,ys,k,A,groups,t=prepare(s,y)
        self.k=k;self.A=A;self.t=t;self.P=int(ys.sum());self.n=len(ys)
        # Integer cross-products are exact within this explicit int64 bound.
        if self.n>100_000_000:raise ValueError('integer cross-product range exceeded')
        self.den=np.maximum(4*self.P+k,1)
        self.prefix=_prefix(A,self.den);self.suffix=_suffix(A,self.den)
        self.base=int(self.prefix[-1]);self.group=np.empty(self.n,dtype=int);self.group[order]=groups
        self.rmq={d:RMQ(A+d,self.den) for d in [-1,1]}
        self.pc=np.bincount(groups,weights=ys,minlength=len(k)).astype(np.int64)
        self.nc=np.diff(np.r_[0,k])-self.pc
        self.pg=np.flatnonzero(self.pc);self.ng=np.flatnonzero(self.nc)
    def query_groups(self,positive_group,negative_groups):
        q=np.asarray(negative_groups,dtype=int);p=positive_group
        result=np.full(len(q),self.base,dtype=int)
        for delta,mask in [(1,q<p),(-1,q>p)]:
            if not mask.any():continue
            lo=np.minimum(p,q[mask]);hi=np.maximum(p,q[mask])-1
            outside=better(self.prefix[lo-1],self.suffix[hi+1],self.A,self.den)
            inside=self.rmq[delta].query(lo,hi)
            cross=(self.A[inside]+delta)*self.den[outside]-self.A[outside]*self.den[inside]
            result[mask]=np.where((cross>0)|((cross==0)&(inside<outside)),inside,outside)
        return result
    def summarize(self):
        total=self.P*(self.n-self.P)
        if not total:return {'pairs':0,'base_k':int(self.k[self.base]),'max_changed':0,'histogram':[]}
        hist=np.zeros(len(self.k),dtype=np.int64);worst=-1;wp=wn=None
        for p in self.pg:
            selected=self.query_groups(p,self.ng);weights=self.pc[p]*self.nc[self.ng]
            np.add.at(hist,selected,weights)
            dif=np.abs(self.k[selected]-self.k[self.base]);j=int(np.argmax(dif))
            if dif[j]>worst:worst=int(dif[j]);wp=int(p);wn=int(self.ng[j]);wi=int(selected[j])
        assert hist.sum()==total
        pos=int(np.flatnonzero((self.group==wp)&(self.y==1))[0]);neg=int(np.flatnonzero((self.group==wn)&(self.y==0))[0])
        return dict(pairs=total,group_pairs=len(self.pg)*len(self.ng),base_k=int(self.k[self.base]),
                    max_changed=worst,max_fraction=worst/self.n,
                    fraction_swaps_changing=float((total-hist[self.base])/total),
                    witness_positive=pos,witness_negative=neg,witness_new_k=int(self.k[wi]),
                    old_threshold=float(self.t[self.base]),new_threshold=float(self.t[wi]),
                    histogram=[(int(self.k[i]),int(hist[i])) for i in np.flatnonzero(hist)])
