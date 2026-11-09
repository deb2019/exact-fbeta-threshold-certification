from pathlib import Path
import os
for v in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']:os.environ[v]='1'
import sys,json,time,math,hashlib,warnings,traceback,concurrent.futures
import numpy as np,pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
R=Path(__file__).resolve().parent
BASE=R.parent/'base' if (R.parent/'base').exists() else R.parent
sys.path.insert(0,str(BASE/'threshold_validation'))
DATA_ROOT=Path(os.environ.get('PREPARED_DATA_ROOT',str(R.parent/'data')))
from run_validation import direct,all_single_flips,minimum_budget_v2
P=json.loads((R/'protocol.json').read_text())
def write(p,x):
 text=json.dumps(x,indent=2,ensure_ascii=False)
 with p.open('w') as f:
  f.write(text);f.flush();os.fsync(f.fileno())
 assert p.read_text()==text
def run(r):
 out=R/'results'/r['id'];out.mkdir(parents=True,exist_ok=True)
 if (out/'completed.json').exists():return r['id'],'cached'
 try:
  p=DATA_ROOT/r['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256']
  df=pd.read_csv(p,low_memory=False);df.columns=df.columns.str.strip();yv=pd.to_numeric(df[r['target']],errors='raise');assert set(yv.unique())=={0,1}
  y=(yv.to_numpy()==r['positive_value']).astype(int)
  X=df.drop(columns=[r['target']]+r['drop_columns']).replace([np.inf,-np.inf],np.nan)
  ids=np.arange(len(y));h=pd.util.hash_pandas_object(X,index=False)
  conflict=pd.DataFrame({'h':h,'y':y}).groupby('h').y.transform('nunique').to_numpy()>1
  keep=~conflict;duplicates=X.loc[keep].duplicated().to_numpy();idx=np.flatnonzero(keep)[~duplicates];X=X.iloc[idx].reset_index(drop=True);y=y[idx];ids=ids[idx]
  cols=X.select_dtypes(include=np.number).columns.tolist();cats=[c for c in X.columns if c not in cols]
  for c in cats:X[c]=X[c].map(lambda x:str(x) if pd.notna(x) else np.nan)
  audit=dict(dataset=r['id'],raw_n=len(df),n=len(y),positive_n=int(y.sum()),positive_rate=float(y.mean()),features=list(X.columns),removed_conflicts=int(conflict.sum()),removed_duplicates=int(duplicates.sum()),drop_columns=r['drop_columns'],categorical_columns=cats)
  write(out/'audit.json',audit);rows=[]
  for seed in P['seeds']:
   tr,other=train_test_split(np.arange(len(y)),test_size=.5,stratify=y,random_state=seed)
   va,te=train_test_split(other,test_size=.5,stratify=y[other],random_state=seed+1)
   for name in P['models']:
    npip=make_pipeline(SimpleImputer(strategy='median'),*([StandardScaler()] if name=='LR' else []))
    cpip=make_pipeline(SimpleImputer(strategy='most_frequent'),OneHotEncoder(handle_unknown='ignore'))
    pre=ColumnTransformer([('num',npip,cols),('cat',cpip,cats)])
    est=LogisticRegression(C=1,max_iter=2000,random_state=seed) if name=='LR' else RandomForestClassifier(n_estimators=120,min_samples_leaf=5,max_features='sqrt',n_jobs=1,random_state=seed)
    model=make_pipeline(pre,est);t=time.perf_counter()
    with warnings.catch_warnings(record=True) as ws:
     warnings.simplefilter('always');model.fit(X.iloc[tr],y[tr]);s=model.predict_proba(X.iloc[va])[:,1]
    fit_seconds=time.perf_counter()-t;assert np.isfinite(s).all();v=y[va];runid=f'{r["id"]}_{seed}_{name}'
    with (out/f'{runid}.npz').open('wb') as sf:
     np.savez_compressed(sf,validation_score=s,validation_y=v,train_id=ids[tr],validation_id=ids[va],test_id=ids[te]);sf.flush();os.fsync(sf.fileno())
    with np.load(out/f'{runid}.npz') as zz:assert np.array_equal(zz['validation_score'],s)
    base=direct(s,v);one=all_single_flips(s,v);max_one=int(np.max(one['disagreement_count']))
    for f in P['distances']:
     d=math.ceil(f*len(v));t=time.perf_counter();res=minimum_budget_v2(s,v,d,max_budget=2,time_limit=5);elapsed=time.perf_counter()-t
     row=dict(dataset=r['id'],run=runid,seed=seed,model=name,n=len(v),positives=int(v.sum()),g=len(np.unique(s)),fraction=f,d=d,fit_seconds=fit_seconds,solver_seconds=elapsed,max_single_edit_disagreement=max_one,warnings=list(dict.fromkeys(str(w.message) for w in ws)),**res)
     if res['status']!='timeout':assert (max_one>=d)==(res.get('minimum_budget')==1)
     if res['status']=='exact':
      z=np.asarray(res['labels']);new=direct(s,z);assert int(np.sum(z!=v))==res['minimum_budget'];assert abs(new-base)>=d
      row.update(witness_indices=np.flatnonzero(z!=v).tolist(),old_k=base,new_k=new,witness_verified=True)
     row.pop('labels',None);rows.append(row);write(out/'results.json',rows)
    print(runid,'done',flush=True)
  write(out/'results.json',rows)
  assert len(json.loads((out/'results.json').read_text()))==12
  write(out/'completed.json',dict(analyses=len(rows),vectors=len(P['seeds'])*len(P['models'])));return r['id'],'complete'
 except Exception:
  err=traceback.format_exc();write(out/'error.json',{'error':err});return r['id'],err
if __name__=='__main__':
 (R/'results').mkdir(exist_ok=True)
 selected=[r for r in json.loads((R/'selection.json').read_text()) if r['decision']=='include']
 with concurrent.futures.ProcessPoolExecutor(max_workers=4) as ex:
  for result in ex.map(run,selected):print('DATASET',*result,flush=True)
