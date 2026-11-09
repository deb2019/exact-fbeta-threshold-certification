from pathlib import Path
from datetime import datetime,timezone
import json,numpy as np
from baselines import dp
from run import direct
R=Path(__file__).resolve().parent
p=dict(created_utc=datetime.now(timezone.utc).isoformat(),cases=['ctg_LR','ctg_RF','wdbc_LR','wdbc_RF','spambase_LR','spambase_RF'],beta_squared=[1,4],distance_fractions=[.01,.025,.05,.1,.2],budget=2,time_limit=5,scope='Descriptive reuse of six fixed score vectors; no independent generalization or new-data confirmation')
assert not (R/'parameter_protocol.json').exists();(R/'parameter_protocol.json').write_text(json.dumps(p,indent=2));rows=[]
for name in p['cases']:
 a=np.load(R/'scores'/f'{name}.npz');s=a['s'];y=a['y']
 for u in p['beta_squared']:
  for f in p['distance_fractions']:
   d=int(np.ceil(f*len(y)));r=dp(s,y,d,u=u)
   if r['status']=='exact':
    z=y.copy();z[r['witness_indices']]=1-z[r['witness_indices']];assert sum(z!=y)==r['minimum_budget'];assert abs(direct(s,z,u=u)-direct(s,y,u=u))>=d
   rows.append(dict(case=name,u=u,v=1,fraction=f,d=d,**r))
(R/'parameter_results.json').write_text(json.dumps(rows,indent=2));print('Parameter analyses:',len(rows))
