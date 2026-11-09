from pathlib import Path
import sys,json,hashlib,time,math,zipfile,platform
from datetime import datetime,timezone
import numpy as np,pandas as pd,sklearn
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R.parent/'threshold_validation'))
from run_validation import direct,all_single_flips,minimum_budget_v2
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def load():
 with zipfile.ZipFile(R/'raw/ozone.zip') as z:df=pd.read_csv(z.open('onehr.data'),header=None,na_values='?')
 X=df.iloc[:,1:-1];y=df.iloc[:,-1].to_numpy(dtype=int)
 groups=X.groupby(list(X.columns),dropna=False,sort=False).ngroup().to_numpy()
 return X,y,groups
if __name__=='__main__':
 p=json.loads((R/'protocol.json').read_text());assert not (R/'completed.json').exists();assert sha(R/'raw/ozone.zip')==p['raw_sha256'];assert sha(R.parent/'threshold_validation/code/budget_v2.py')==p['solver_sha256']
 X,y,groups=load();assert set(y)=={0,1};assert y.mean()<.05
 env=dict(cpu=next(x.split(':',1)[1].strip() for x in Path('/proc/cpuinfo').read_text().splitlines() if x.startswith('model name')),python=sys.version,numpy=np.__version__,pandas=pd.__version__,sklearn=sklearn.__version__,platform=platform.platform(),runner_sha256=sha(Path(__file__)),n=len(y),positives=int(y.sum()),positive_rate=float(y.mean()),features=X.shape[1],feature_groups=len(set(groups)),missing_cells=int(X.isna().sum().sum()))
 (R/'environment.json').write_text(json.dumps(env,indent=2));(R/'scores').mkdir(exist_ok=True);rows=[]
 for seed in p['seeds']:
  folds=list(StratifiedGroupKFold(n_splits=4,shuffle=True,random_state=seed).split(X,y,groups));va=folds[0][1];te=folds[1][1];tr=np.concatenate([folds[2][1],folds[3][1]])
  for a,b in [(tr,va),(tr,te),(va,te)]:assert not set(groups[a])&set(groups[b])
  for name in ['LR','RF']:
   est=LogisticRegression(C=1,max_iter=2000,random_state=seed) if name=='LR' else RandomForestClassifier(n_estimators=120,min_samples_leaf=5,max_features='sqrt',n_jobs=2,random_state=seed)
   model=make_pipeline(SimpleImputer(strategy='median'),*([StandardScaler()] if name=='LR' else []),est);model.fit(X.iloc[tr],y[tr]);s=model.predict_proba(X.iloc[va])[:,1];yv=y[va];run=f'ozone_onehr_{seed}_{name}'
   np.savez_compressed(R/'scores'/f'{run}.npz',validation_score=s,validation_y=yv,validation_id=va,train_id=tr,test_id=te,validation_group=groups[va],train_group=groups[tr],test_group=groups[te])
   base=direct(s,yv);one=all_single_flips(s,yv)
   for f in p['distances']:
    d=math.ceil(f*len(s));t=time.perf_counter();r=minimum_budget_v2(s,yv,d,max_budget=p['budget'],time_limit=p['time_limit_seconds']);elapsed=time.perf_counter()-t
    row=dict(run=run,seed=seed,model=name,n=len(s),g=len(np.unique(s)),positives=int(yv.sum()),positive_rate=float(yv.mean()),train_n=len(tr),train_positives=int(y[tr].sum()),test_n=len(te),test_positives=int(y[te].sum()),fraction=f,d=d,seconds=elapsed,**r)
    if r['status']!='timeout':assert bool(max(one['disagreement_count'])>=d)==(r.get('minimum_budget')==1)
    if r['status']=='exact':
     edited=np.asarray(r['labels']);assert sum(edited!=yv)==r['minimum_budget'];new=direct(s,edited);assert abs(new-base)>=d
     row.update(witness_indices=np.flatnonzero(edited!=yv).tolist(),old_k=base,new_k=new,witness_verified=True)
    row.pop('labels',None);rows.append(row);(R/'results.json').write_text(json.dumps(rows,indent=2));print(run,f,r['status'],r.get('minimum_budget',r.get('certified_lower_bound')),elapsed,flush=True)
 (R/'completed.json').write_text(json.dumps(dict(completed_utc=datetime.now(timezone.utc).isoformat(),analyses=len(rows),protocol_sha256=sha(R/'protocol.json'),results_sha256=sha(R/'results.json')),indent=2))
