from pathlib import Path
import json,sys,time,platform,hashlib,itertools
from datetime import datetime,timezone
from fractions import Fraction
import numpy as np,scipy
from baselines import scan,integer_program,dp
R=Path(__file__).resolve().parent

def direct(s,y,u=4,v=1):
 kbest=0;best=Fraction(0);P=int(sum(y))
 for t in sorted(set(s),reverse=True):
  mask=s>=t;k=int(sum(mask));a=int(sum(y[mask]));f=Fraction(a,u*P+v*k)
  if f>best:best=f;kbest=k
 return kbest

def verify():
 count=0
 for n in range(2,6):
  for tied in [False,True]:
   s=np.arange(n,dtype=float);s=np.floor(s/2) if tied else s
   for yy in itertools.product([0,1],repeat=n):
    y=np.array(yy);d=max(1,n//2)
    answers=[fn(s,y,d,seconds=15) for fn in [scan,integer_program,dp]]
    assert len({(r['status'],r.get('minimum_budget'),r.get('certified_lower_bound')) for r in answers})==1,(n,yy,answers)
    for r in answers:
     if r['status']=='exact':
      z=y.copy();z[r['witness_indices']]=1-z[r['witness_indices']];assert sum(z!=y)==r['minimum_budget'];assert abs(direct(s,z)-direct(s,y))>=d
    count+=1
 (R/'small_verification.json').write_text(json.dumps(dict(cases=count,methods=3,status='passed'),indent=2))

def main():
 p={'created_utc':datetime.now(timezone.utc).isoformat(),'seed':20261017,'synthetic_n':[64,128,256],'patterns':['distinct','16groups'],'positive_fraction':.1,'real_arrays':'first existing seed, LR and RF, CTG/WDBC/Spambase; all 6 included','distance_fraction':.05,'budget':2,'repeats':3,'seconds_per_method':5,'methods':['DP','pair_scan','MILP_HiGHS'],'timing':'end-to-end preparation, minimum-budget<=2, rotating order; cooperative timeout; all statuses retained','MILP':'SciPy/HiGHS integer model with cumulative counts, absolute-edit auxiliaries and big-M target selection; enumerate edited totals; exact-check witnesses; numerical optimality/infeasibility certificates','baseline':'exact integer batched cutoff tournaments; group/label type compression includes same-direction and opposite-direction pairs; sort once','environment':{'python':sys.version,'numpy':np.__version__,'scipy':scipy.__version__,'cpu':next(x.split(':',1)[1].strip() for x in Path('/proc/cpuinfo').read_text().splitlines() if x.startswith('model name'))},'code_sha256':hashlib.sha256((R/'baselines.py').read_bytes()).hexdigest()}
 assert not (R/'protocol.json').exists();(R/'protocol.json').write_text(json.dumps(p,indent=2))
 verify();rng=np.random.default_rng(p['seed']);cases=[]
 for pat in p['patterns']:
  for n in p['synthetic_n']:
   s=rng.permutation(n).astype(float)
   if pat=='16groups':s=np.floor(s*16/n)
   y=(rng.random(n)<.1).astype(int);cases.append((f'synthetic_{pat}_{n}',s,y))
 for name,folder,seed in [('ctg','threshold_validation',20261007),('wdbc','threshold_validation',20261007),('spambase','source_benchmarks',20261016)]:
  for m in ['LR','RF']:
   a=np.load(R.parent/folder/'scores'/f'{name}_{seed}_{m}.npz');cases.append((f'{name}_{m}',a['validation_score'],a['validation_y']))
 (R/'scores').mkdir(exist_ok=True);rows=[];methods=[('DP',dp),('pair_scan',scan),('MILP_HiGHS',integer_program)]
 for name,s,y in cases:
  np.savez_compressed(R/'scores'/f'{name}.npz',s=s,y=y);d=int(np.ceil(.05*len(y)));row=dict(case=name,n=len(y),g=len(set(s)),positives=int(sum(y)),d=d,methods={})
  for rep in range(3):
   for meth,fn in methods[rep:]+methods[:rep]:
    start=time.perf_counter();r=fn(s,y,d,seconds=5);sec=time.perf_counter()-start
    if r['status']=='exact':
     z=y.copy();z[r['witness_indices']]=1-z[r['witness_indices']];assert sum(z!=y)==r['minimum_budget'];assert abs(direct(s,z)-direct(s,y))>=d
    row['methods'].setdefault(meth,[]).append(dict(seconds=sec,**r));print(name,rep,meth,r['status'],round(sec,4),flush=True)
  completed=[(r['status'],r.get('minimum_budget'),r.get('certified_lower_bound')) for v in row['methods'].values() for r in v if r['status']!='timeout'];assert len(set(completed))<=1
  rows.append(row);(R/'results.json').write_text(json.dumps(rows,indent=2))
 (R/'completed.json').write_text(json.dumps(dict(cases=len(rows),calls=108,completed_utc=datetime.now(timezone.utc).isoformat()),indent=2))
if __name__=='__main__':main()
