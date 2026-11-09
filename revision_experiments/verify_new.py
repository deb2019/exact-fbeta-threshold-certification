from pathlib import Path
import json,numpy as np
from baselines import dp,scan
from run import direct
R=Path(__file__).resolve().parent;r=json.loads((R/'results.json').read_text());w=0;checked=0;timeouts=0
for x in r:
 a=np.load(R/'scores'/(x['case']+'.npz'));s=a['s'];y=a['y'];truth=dp(s,y,x['d'])
 for name,reps in x['methods'].items():
  for z in reps:
   if z['status']=='timeout':timeouts+=1;continue
   for k in ['status','minimum_budget','certified_lower_bound']:assert z.get(k)==truth.get(k),(x['case'],name,k)
   checked+=1
   if z['status']=='exact':
    yy=y.copy();yy[z['witness_indices']]=1-yy[z['witness_indices']];assert sum(yy!=y)==z['minimum_budget'];assert abs(direct(s,yy)-direct(s,y))>=x['d'];w+=1
  if name=='pair_scan' and all(z['status']!='timeout' for z in reps):
   z=scan(s,y,x['d']);assert z['status']==truth['status'];assert z.get('minimum_budget')==truth.get('minimum_budget')
params=json.loads((R/'parameter_results.json').read_text());pw=0
for x in params:
 a=np.load(R/'scores'/(x['case']+'.npz'));s=a['s'];y=a['y'];z=dp(s,y,x['d'],u=x['u'])
 for k in ['status','minimum_budget','certified_lower_bound']:assert z.get(k)==x.get(k)
 if x['status']=='exact':
  yy=y.copy();yy[x['witness_indices']]=1-yy[x['witness_indices']];assert sum(yy!=y)==x['minimum_budget'];assert abs(direct(s,yy,u=x['u'])-direct(s,y,u=x['u']))>=x['d'];pw+=1
print(json.dumps(dict(status='passed',baseline_cases=len(r),completed_timed_outputs_checked=checked,censored_timed_outputs=timeouts,baseline_witness_checks=w,parameter_analyses=len(params),parameter_witness_checks=pw),indent=2))
