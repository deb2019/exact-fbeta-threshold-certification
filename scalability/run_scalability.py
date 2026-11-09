from pathlib import Path
import sys,json,zipfile,io,time,math,hashlib,platform
from datetime import datetime,timezone
import numpy as np,pandas as pd,sklearn
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import make_pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R.parent/'threshold_validation'))
from run_validation import direct,all_single_flips,minimum_budget_v2
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 p=json.loads((R/'protocol.json').read_text());assert not (R/'completed.json').exists()
 assert sha(R.parent/'threshold_validation/code/budget_v2.py')==p['solver_sha256']
 z=zipfile.ZipFile(R/'raw/bank_marketing.zip');inner=zipfile.ZipFile(io.BytesIO(z.read('bank.zip')))
 df=pd.read_csv(io.BytesIO(inner.read('bank-full.csv')),sep=';');X=df.drop(columns=['y','duration']);y=(df.y=='yes').to_numpy(dtype=int)
 groups=X.groupby(list(X.columns),dropna=False,sort=False).ngroup().to_numpy();cat=X.select_dtypes(include='object').columns.tolist();num=[c for c in X if c not in cat]
 env=dict(cpu=next(x.split(':',1)[1].strip() for x in Path('/proc/cpuinfo').read_text().splitlines() if x.startswith('model name')),python=sys.version,numpy=np.__version__,pandas=pd.__version__,sklearn=sklearn.__version__,platform=platform.platform(),raw_sha256=sha(R/'raw/bank_marketing.zip'),runner_sha256=sha(Path(__file__)),n=len(y),positives=int(y.sum()),features=list(X.columns),feature_groups=len(set(groups)))
 (R/'environment.json').write_text(json.dumps(env,indent=2));(R/'scores').mkdir(exist_ok=True);rows=[]
 for seed in p['seeds']:
  tr,va=next(GroupShuffleSplit(n_splits=1,test_size=.5,random_state=seed).split(X,groups=groups));assert not set(groups[tr])&set(groups[va])
  order=np.random.default_rng(seed+100).permutation(len(va))
  for modelname in ['LR','RF']:
   est=LogisticRegression(C=1,max_iter=2000,random_state=seed) if modelname=='LR' else RandomForestClassifier(n_estimators=120,min_samples_leaf=5,max_features='sqrt',n_jobs=2,random_state=seed)
   prep=ColumnTransformer([('num',make_pipeline(SimpleImputer(strategy='median'),*([StandardScaler()] if modelname=='LR' else [])),num),('cat',make_pipeline(SimpleImputer(strategy='most_frequent'),OneHotEncoder(handle_unknown='ignore')),cat)])
   model=make_pipeline(prep,est);model.fit(X.iloc[tr],y[tr]);full=model.predict_proba(X.iloc[va])[:,1]
   for size in p['sizes']:
    take=order if size=='full' else order[:size];ids=va[take];s=full[take];yv=y[ids];run=f'bank_{seed}_{modelname}_{size}'
    np.savez_compressed(R/'scores'/f'{run}.npz',validation_score=s,validation_y=yv,validation_id=ids,train_id=tr,train_group=groups[tr],validation_group=groups[ids])
    one=all_single_flips(s,yv);base=direct(s,yv)
    for f in p['distances']:
     d=math.ceil(f*len(s));samples=[];results=[]
     for rep in range(p['repeats']):
      t=time.perf_counter();r=minimum_budget_v2(s,yv,d,max_budget=2,time_limit=p['time_limit_seconds']);samples.append(time.perf_counter()-t);results.append(r)
     r=results[0];row=dict(run=run,seed=seed,model=modelname,size_requested=size,n=len(s),g=len(set(s)),positives=int(yv.sum()),fraction=f,d=d,seconds=samples,median_seconds=float(np.median(samples)),repeat_statuses=[z['status'] for z in results],**r)
     # Never turn a timeout into a certificate. Record cross-repeat variation explicitly.
     row['repeat_agreement']=all((z['status'],z.get('minimum_budget'),z.get('certified_lower_bound'))==(r['status'],r.get('minimum_budget'),r.get('certified_lower_bound')) for z in results)
     if r['status']!='timeout':assert bool(max(one['disagreement_count'])>=d)==(r.get('minimum_budget')==1)
     if r['status']=='exact':
      edited=np.asarray(r['labels']);assert sum(edited!=yv)==r['minimum_budget'];new=direct(s,edited);assert abs(new-base)>=d
      row.update(witness_indices=np.flatnonzero(edited!=yv).tolist(),old_k=base,new_k=new,witness_verified=True)
     row.pop('labels',None);rows.append(row);(R/'results.json').write_text(json.dumps(rows,indent=2));print(run,f,r['status'],r.get('minimum_budget',r.get('certified_lower_bound')),row['median_seconds'],flush=True)
 (R/'completed.json').write_text(json.dumps(dict(completed_utc=datetime.now(timezone.utc).isoformat(),analyses=len(rows),protocol_sha256=sha(R/'protocol.json'),results_sha256=sha(R/'results.json')),indent=2))
if __name__=='__main__':main()
