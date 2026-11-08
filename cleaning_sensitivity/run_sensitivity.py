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
sys.path.insert(0,str(ROOT.parent/'threshold_validation'/'code'))
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
    protocol=json.loads((ROOT/'protocol.json').read_text())
    datasets=[]
    for name in protocol['datasets']:
        z=zipfile.ZipFile(ROOT.parent/'source_benchmarks'/'raw'/f'{name}.zip')
        cat=[]
        if name=='climate':
            a=pd.read_csv(io.BytesIO(z.read('pop_failures.dat')),sep=r'\s+')
            df=a.iloc[:,2:20].astype(float).copy();df['label']=(a.iloc[:,20]==0).astype(int)
        elif name=='seismic':
            from scipy.io import arff
            a=pd.DataFrame(arff.loadarff(io.StringIO(z.read('seismic-bumps.arff').decode()))[0])
            df=a.iloc[:,:-1].copy();cat=['seismic','seismoacoustic','shift','ghazard']
            for c in df:
                if c in cat:df[c]=df[c].str.decode('ascii')
                else:df[c]=df[c].astype(float)
            df['label']=(a.iloc[:,-1].astype(str)=='1').astype(int)
        else:
            member={'blood':'transfusion.data','mammographic':'mammographic_masses.data','spambase':'spambase.data'}[name]
            a=pd.read_csv(io.BytesIO(z.read(member)),header=0 if name=='blood' else None,na_values='?')
            df=a.iloc[:,1:-1].copy() if name=='mammographic' else a.iloc[:,:-1].copy()
            df.columns=['feature_'+str(i) for i in range(df.shape[1])]
            if name=='mammographic':cat=['feature_1','feature_2']
            df['label']=a.iloc[:,-1].astype(int)
        df.columns=df.columns.astype(str)
        datasets.append((name,df,cat))
    if (ROOT/'completed.json').exists():raise RuntimeError('Completed results already exist')
    rows=[];audits=[];(ROOT/'scores').mkdir(exist_ok=True)
    from sklearn.model_selection import GroupShuffleSplit
    for name,raw,cat in datasets:
        features=list(raw.columns[:-1]);groups=raw.groupby(features,dropna=False,sort=False).ngroup().to_numpy()
        conflict=raw.groupby(features,dropna=False)['label'].transform('nunique')>1
        for seed in protocol['seeds']:
            tr,other=next(GroupShuffleSplit(n_splits=1,test_size=.5,random_state=seed).split(raw,groups=groups))
            va,te=next(GroupShuffleSplit(n_splits=1,test_size=.5,random_state=seed+1).split(raw.iloc[other],groups=groups[other]))
            raw_parts=[tr,other[va],other[te]]
            for arm in protocol['arms']:
                if arm=='all_rows':df=raw
                elif arm=='deduplicate_same_label':df=raw.drop_duplicates(features+['label'])
                else:df=raw.loc[~conflict].drop_duplicates(features)
                ids=df.index.to_numpy();X=df[features];y=df.label.to_numpy(dtype=int)
                train,val,test=[np.flatnonzero(np.isin(ids,v)) for v in raw_parts]
                assert len(set(y[train]))==2 and len(val)>0
                group_parts=[set(groups[ids[v]]) for v in [train,val,test]]
                assert not(group_parts[0]&group_parts[1] or group_parts[0]&group_parts[2] or group_parts[1]&group_parts[2])
                audits.append(dict(dataset=name,seed=seed,arm=arm,n=len(df),positives=int(y.sum()),n_train=len(train),n_validation=len(val),n_test=len(test),group_overlap=False))
                for modelname in ['LR','RF']:
                    estimator=LogisticRegression(C=1,max_iter=2000,random_state=seed) if modelname=='LR' else RandomForestClassifier(n_estimators=120,min_samples_leaf=5,max_features='sqrt',n_jobs=2,random_state=seed)
                    from sklearn.compose import ColumnTransformer
                    from sklearn.preprocessing import OneHotEncoder
                    numeric=[c for c in features if c not in cat]
                    num=make_pipeline(SimpleImputer(strategy='median'),*([StandardScaler()] if modelname=='LR' else []))
                    transforms=[('numeric',num,numeric)]
                    if cat:transforms.append(('categorical',make_pipeline(SimpleImputer(strategy='most_frequent'),OneHotEncoder(handle_unknown='ignore')),cat))
                    model=make_pipeline(ColumnTransformer(transforms),estimator);model.fit(X.iloc[train],y[train]);s=model.predict_proba(X.iloc[val])[:,1];yv=y[val]
                    run=f'{name}_{seed}_{modelname}_{arm}';np.savez_compressed(ROOT/'scores'/f'{run}.npz',validation_score=s,validation_y=yv,train_id=ids[train],validation_id=ids[val],test_id=ids[test],train_group=groups[ids[train]],validation_group=groups[ids[val]],test_group=groups[ids[test]])
                    one=all_single_flips(s,yv);base=direct(s,yv)
                    for fraction in [0.05,0.10]:
                        d=math.ceil(fraction*len(val));start=time.perf_counter();r=minimum_budget_v2(s,yv,d,max_budget=2,time_limit=5);elapsed=time.perf_counter()-start
                        row={'run':run,'dataset':name,'arm':arm,'model':modelname,'seed':seed,'n_validation':len(val),'positives':int(yv.sum()),'g':len(set(s)),'distance_fraction':fraction,'d':d,'seconds':elapsed,**r}
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
if __name__=="__main__":main()
