"""Frozen post-development computational validation; run from this directory."""
from pathlib import Path
import sys, json, hashlib, zipfile, io, math, time, platform
from datetime import datetime, timezone
from fractions import Fraction
import numpy as np
import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'code'))
from budget_v2 import minimum_budget_v2
from exact_influence import all_single_flips

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def direct(s,y):
    order=np.argsort(-s,kind='stable');ss=s[order];ys=y[order]
    total=int(sum(y));a=0;best=Fraction(0);k=0
    for j in range(len(s)):
        a+=int(ys[j])
        if j+1<len(s) and ss[j]==ss[j+1]:continue
        value=Fraction(a,4*total+j+1)
        if value>best:best=value;k=j+1
    return k

def main():
    # Written before parsing data, fitting models, or inspecting solver outcomes.
    protocol={'created_utc':datetime.now(timezone.utc).isoformat(),
      'purpose':'Post-development computational validation, not external clinical validation or preregistration',
      'datasets':{'ctg':{'source':'https://doi.org/10.24432/C51S4N','positive':'NSP=3','negative':'NSP=1 or 2','features':'21 numbered diagnostic features only; no CLASS or morphology indicators'},
                  'wdbc':{'source':'https://doi.org/10.24432/C5DW2B','positive':'M','negative':'B','features':'30 measurements; ID excluded'}},
      'seeds':[20261007,20261008,20261009], 'split':'stratified 50/25/25, seed then seed+1',
      'preprocessing':'Exclude all feature-identical conflicting-label groups; keep first duplicate feature vector. Train-only median imputation; LR train-only standardization.',
      'models':{'LR':{'C':1,'max_iter':2000},'RF':{'n_estimators':120,'min_samples_leaf':5,'max_features':'sqrt','n_jobs':2}},
      'beta':2,'primary_distance_fraction':0.05,'secondary_distance_fraction':0.10,'max_budget':2,'time_limit_seconds':5,
      'tie_rule':'highest threshold / fewest positive predictions','score_rounding':False,
      'test_policy':'test rows reserved; no prediction or evaluation on test data',
      'checks':'Fraction witness enumeration and independent all-single-edit verdict',
      'raw_sha256':{p.name:sha(p) for p in sorted((ROOT/'raw').glob('*.zip'))},
      'code_sha256':{p.name:sha(p) for p in sorted((ROOT/'code').glob('*.py'))},
      'runner_sha256':sha(Path(__file__)),
      'environment':{'python':sys.version,'numpy':np.__version__,'pandas':pd.__version__,'sklearn':sklearn.__version__,'platform':platform.platform(),
                     'cpu':next((s.split(':',1)[1].strip() for s in Path('/proc/cpuinfo').read_text().splitlines() if s.startswith('model name')),'unknown')}}
    if (ROOT/'protocol.json').exists():raise RuntimeError('Use a fresh output directory; do not overwrite frozen protocol/results')
    (ROOT/'protocol.json').write_text(json.dumps(protocol,indent=2))
    z=zipfile.ZipFile(ROOT/'raw/ctg.zip');a=pd.read_excel(io.BytesIO(z.read('CTG.xls')),sheet_name='Data',header=None)
    names=a.iloc[1,10:31].tolist();a=a.iloc[2:];a=a.loc[a.iloc[:,45].isin([1,2,3])]
    ctg=pd.DataFrame(a.iloc[:,10:31].to_numpy(dtype=float),columns=names);ctg['label']=(a.iloc[:,45].to_numpy()==3).astype(int)
    z=zipfile.ZipFile(ROOT/'raw/wdbc.zip');a=pd.read_csv(io.BytesIO(z.read('wdbc.data')),header=None)
    wdbc=a.iloc[:,2:].astype(float).copy();wdbc.columns=['feature_'+str(i+1) for i in range(30)];wdbc['label']=(a.iloc[:,1]=='M').astype(int)
    rows=[];audits=[];(ROOT/'scores').mkdir(exist_ok=True)
    for name,df in [('ctg',ctg),('wdbc',wdbc)]:
        raw_n=len(df);features=list(df.columns[:-1]);conflict=df.groupby(features,dropna=False)['label'].transform('nunique')>1
        bad=int(conflict.sum());df=df.loc[~conflict];before=len(df);df=df.drop_duplicates(features);duplicates=before-len(df)
        ids=df.index.to_numpy();X=df[features].to_numpy();y=df.label.to_numpy(dtype=int)
        audits.append({'dataset':name,'raw_n':raw_n,'n':len(df),'features':features,'positives':int(y.sum()),'conflicting_rows_removed':bad,'duplicate_rows_removed':duplicates})
        for seed in protocol['seeds']:
            train,other=train_test_split(np.arange(len(y)),test_size=.5,stratify=y,random_state=seed)
            val,test=train_test_split(other,test_size=.5,stratify=y[other],random_state=seed+1)
            for modelname in ['LR','RF']:
                estimator=LogisticRegression(C=1,max_iter=2000,random_state=seed) if modelname=='LR' else RandomForestClassifier(n_estimators=120,min_samples_leaf=5,max_features='sqrt',n_jobs=2,random_state=seed)
                steps=[SimpleImputer(strategy='median')]+([StandardScaler()] if modelname=='LR' else [])+[estimator]
                model=make_pipeline(*steps);model.fit(X[train],y[train]);s=model.predict_proba(X[val])[:,1];yv=y[val]
                run=f'{name}_{seed}_{modelname}';np.savez_compressed(ROOT/'scores'/f'{run}.npz',validation_score=s,validation_y=yv,train_id=ids[train],validation_id=ids[val],test_id=ids[test])
                one=all_single_flips(s,yv);base=direct(s,yv)
                for fraction in [0.05,0.10]:
                    d=math.ceil(fraction*len(val));start=time.perf_counter();r=minimum_budget_v2(s,yv,d,max_budget=2,time_limit=5);elapsed=time.perf_counter()-start
                    row={'run':run,'dataset':name,'model':modelname,'seed':seed,'n_validation':len(val),'positives':int(yv.sum()),'g':len(set(s)),'distance_fraction':fraction,'d':d,'seconds':elapsed,**r}
                    exists_one=bool(np.max(one['disagreement_count'])>=d)
                    if r['status']!='timeout':assert exists_one==(r.get('minimum_budget')==1)
                    row['single_edit_check']=('passed' if r['status']!='timeout' else 'not_asserted')
                    if r['status']=='exact':
                        z=np.asarray(r['labels']);new=direct(s,z);assert int(sum(z!=yv))==r['minimum_budget'];assert abs(new-base)>=d
                        row.update(witness_indices=np.flatnonzero(z!=yv).tolist(),old_k=base,new_k=new,witness_verified=True)
                    row.pop('labels',None);rows.append(row)
                    (ROOT/'results.json').write_text(json.dumps({'audit':audits,'rows':rows},indent=2))
                    print(run,fraction,r['status'],r.get('minimum_budget',r.get('certified_lower_bound')),round(elapsed,4),flush=True)
    (ROOT/'completed.json').write_text(json.dumps({'completed_utc':datetime.now(timezone.utc).isoformat(),'protocol_sha256':sha(ROOT/'protocol.json'),'results_sha256':sha(ROOT/'results.json'),'runs':len(rows)},indent=2))
if __name__=='__main__':main()
