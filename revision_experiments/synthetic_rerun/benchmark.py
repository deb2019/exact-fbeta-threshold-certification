import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'threshold_theory'))
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'threshold_influence'))
"""Paired timing; exact integer tournament baseline, one sort per whole task.
Both swap methods enumerate score-group pairs and return record-weighted histograms.
Timing includes preparation and output; memory in separate tracemalloc runs.
"""
import sys,time,json,platform,tracemalloc,statistics
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'threshold_influence'))
from exact_influence import prepare,all_single_flips
from exact_swaps import SwapAnalyzer

def argmax_exact(a,d):
    ix=np.arange(len(a))
    while len(ix)>1:
        left=ix[0:len(ix)//2*2:2];right=ix[1:len(ix)//2*2:2]
        cross=a[left]*d[right]-a[right]*d[left]
        win=np.where(cross>=0,left,right)
        ix=np.r_[win,ix[-1:]] if len(ix)%2 else win
    return int(ix[0])

def flip_baseline(s,y):
    order,ys,k,A,groups,t=prepare(s,y);P=int(sum(ys));out=np.empty(len(y),dtype=int)
    # Same-group/same-label flips are identical; cache them as a stronger baseline.
    for h in range(1,len(k)):
        for label in [0,1]:
            local=np.arange(k[h-1],k[h]);ids=local[ys[local]==label]
            if len(ids):
                delta=1-2*label;new=A.copy();new[h:]+=delta
                out[order[ids]]=k[argmax_exact(new,np.maximum(4*(P+delta)+k,1))]
    return out

def flip_fast(s,y):return all_single_flips(s,y)['changed_k']

def swap_baseline(s,y):
    order,ys,k,A,groups,t=prepare(s,y);P=int(sum(ys));d=np.maximum(4*P+k,1)
    pc=np.bincount(groups,weights=ys,minlength=len(k)).astype(int);nc=np.diff(np.r_[0,k])-pc
    hist=np.zeros(len(k),dtype=np.int64)
    for p in np.flatnonzero(pc):
        for q in np.flatnonzero(nc):
            new=A.copy()
            if q<p:new[q:p]+=1
            if p<q:new[p:q]-=1
            hist[argmax_exact(new,d)]+=pc[p]*nc[q]
    return hist

def swap_fast(s,y):
    obj=SwapAnalyzer(s,y);out=np.zeros(len(obj.k),dtype=np.int64)
    for p in obj.pg:
        selected=obj.query_groups(p,obj.ng);np.add.at(out,selected,obj.pc[p]*obj.nc[obj.ng])
    return out

def batched_argmax(a,d):
    ix=np.broadcast_to(np.arange(a.shape[1]),a.shape).copy();rows=np.arange(a.shape[0])[:,None]
    while ix.shape[1]>1:
        end=ix.shape[1]//2*2;left=ix[:,:end:2];right=ix[:,1:end:2]
        cross=a[rows,left]*d[rows,right]-a[rows,right]*d[rows,left]
        win=np.where(cross>=0,left,right)
        ix=np.concatenate([win,ix[:,-1:]],axis=1) if ix.shape[1]%2 else win
    return ix[:,0]
scalar_flip=flip_baseline
scalar_swap=swap_baseline

def flip_baseline(s,y):
    order,ys,k,A,groups,t=prepare(s,y);P=int(sum(ys));out=np.empty(len(y),dtype=int)
    scenarios=[];record_ids=[]
    for h in range(1,len(k)):
        local=np.arange(k[h-1],k[h])
        for label in [0,1]:
            ids=local[ys[local]==label]
            if len(ids):scenarios.append((h,1-2*label));record_ids.append(ids)
    j=np.arange(len(k))[None,:]
    for start in range(0,len(scenarios),64):
        batch=np.array(scenarios[start:start+64]);h=batch[:,0,None];delta=batch[:,1,None]
        a=A[None,:]+delta*(j>=h);d=np.maximum(4*(P+delta)+k[None,:],1)
        selected=batched_argmax(a,d)
        for r,sel in enumerate(selected):out[order[record_ids[start+r]]]=k[sel]
    return out

def swap_baseline(s,y):
    order,ys,k,A,groups,t=prepare(s,y);P=int(sum(ys));den=np.maximum(4*P+k,1)
    pc=np.bincount(groups,weights=ys,minlength=len(k)).astype(int);nc=np.diff(np.r_[0,k])-pc
    hist=np.zeros(len(k),dtype=np.int64);j=np.arange(len(k))[None,:]
    # Streaming batches, never materialize all pair outputs.
    pairs=[]
    def flush(pairs):
        pq=np.array(pairs);p=pq[:,0,None];q=pq[:,1,None]
        a=A[None,:]+(j>=q).astype(int)-(j>=p).astype(int)
        d=np.broadcast_to(den,a.shape);selected=batched_argmax(a,d)
        np.add.at(hist,selected,pc[pq[:,0]]*nc[pq[:,1]])
    for p in np.flatnonzero(pc):
        for q in np.flatnonzero(nc):
            pairs.append((p,q))
            if len(pairs)==64:flush(pairs);pairs=[]
    if pairs:flush(pairs)
    return hist

root=Path(__file__).parent
protocol={'seed':829031,'repeats':3,'sizes_flip':[128,512,2048,8192],'sizes_swap':[64,128,256,512],'positive_fraction':0.1,'scores':['distinct','16_tied_groups'],'timing':'complete callable including sort/preparation; alternating order; median 3; one warmup','baseline':'batched (64 scenarios) exact int64 tournament cutoff scan, one initial sort, same-group label cache / group-pair compression','memory':'separate tracemalloc peak Python/NumPy traced allocations, not total RSS','threads':'single Python process; no training','warning':'synthetic scaling benchmark, not population or end-to-end ML performance'}
(root/'benchmark_protocol.json').write_text(json.dumps(protocol,indent=2))
rows=[];rng=np.random.default_rng(protocol['seed'])
for task,ns,fast,slow in [('flip',protocol['sizes_flip'],flip_fast,flip_baseline),('swap',protocol['sizes_swap'],swap_fast,swap_baseline)]:
    for pattern in protocol['scores']:
        for n in ns:
            y=np.zeros(n,dtype=int);y[rng.choice(n,max(1,n//10),replace=False)]=1
            s=rng.permutation(n).astype(float)
            if pattern=='16_tied_groups':s=np.floor(s*16/n)
            expected=slow(s,y);assert np.array_equal(fast(s,y),expected)
            if n<=128:assert np.array_equal(expected,(scalar_flip if task=='flip' else scalar_swap)(s,y))
            times={'fast':[],'baseline':[]}
            for rep in range(3):
                order=[('fast',fast),('baseline',slow)]
                if rep%2:order.reverse()
                for name,fn in order:
                    start=time.perf_counter();got=fn(s,y);elapsed=time.perf_counter()-start
                    assert np.array_equal(got,expected);times[name].append(elapsed)
            mem={}
            for name,fn in [('fast',fast),('baseline',slow)]:
                tracemalloc.start();fn(s,y);_,peak=tracemalloc.get_traced_memory();tracemalloc.stop();mem[name]=peak
            f=statistics.median(times['fast']);b=statistics.median(times['baseline'])
            row={'task':task,'pattern':pattern,'n':n,'positives':int(sum(y)),'groups':len(set(s)),'fast_seconds':f,'baseline_seconds':b,'speedup':b/f,'fast_peak_bytes':mem['fast'],'baseline_peak_bytes':mem['baseline'],'raw_seconds':times}
            rows.append(row);print({k:v for k,v in row.items() if k!='raw_seconds'},flush=True)
            (root/'benchmark_results.json').write_text(json.dumps({'environment':{'python':sys.version,'numpy':np.__version__,'platform':platform.platform(),'processor':platform.processor()},'rows':rows},indent=2))
