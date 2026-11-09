from pathlib import Path
import re,json,hashlib
import pandas as pd,numpy as np
R=Path(__file__).resolve().parent;D=R.parent/'data'
rows=[]
# Candidate selection is based on filenames/source notes, never solver results.
for p in sorted(D.rglob('*.csv')):
 if not p.is_file():continue
 rel=p.relative_to(D);deleted=any(x.lower()=='deleted' for x in rel.parts)
 prepared=bool(re.search(r'pre|ready|imb|reduced|smaller|hcv_data|helicopter',p.name,re.I))
 if not prepared or deleted:continue
 df=pd.read_csv(p,low_memory=False);df.columns=df.columns.str.strip()
 q=p.parent;notes=[]
 while q!=D and D in q.parents:
  notes.extend(x for x in q.glob('*.txt') if re.search('source|note',x.name,re.I));q=q.parent
 txt='\n'.join(x.read_text(errors='replace') for x in notes)
 candidates=[]
 for line in txt.splitlines():
  if re.search(r'target\s*vari[ab]*[al]*[be]*le|target\s*class|target\s*column',line,re.I):
   for col in df.columns:
    if re.search(r'(?<!\w)'+re.escape(col)+r'(?!\w)',line,re.I):candidates.append(col)
 targets=['RiskLabel_Binary','RiskLabel','long_stay','Stunting_binary','NSP','target','Status','At_Risk','Label','status','Target_High_Admission','Diabetes_binary','Diagnosis','Target','Fraudulent','is_fraud','fraud','police_report_available_YES','IsFraud','Response','PotentialFraud','Class','label','class','Result','data_stolen','Lavel','condition','Machine failure','outcome','ApprovalStatus','Category','Is high risk','Loan_Status','loan_status','good_bad_flag','Defaulted','Distress','HasBudget','HighIncome','HighMarketValue','High_Investment','HighValueCustomer','Risk','CARAVAN','insuranceclaim','fraud_reported','Churn','Revenue','y','A16']
 hits=list(dict.fromkeys(candidates))
 if len(hits)!=1:hits=[x for x in targets if x in df.columns]
 # Explicit disambiguation from source notes.
 overrides={'pre_train_fault.csv':'condition','pre_ovarian_cancer_binary.csv':'RiskLabel_Binary','ovarian_dataset_smaller.csv':'RiskLabel','Preprocessed_Fraud_Insurance.csv':'police_report_available_YES','TurkishCF_Preprocessed.csv':'Label'}
 if p.name in overrides:hits=[overrides[p.name]]
 t=hits[0] if len(hits)==1 else None
 counts={} if t is None else {str(k):int(v) for k,v in df[t].value_counts(dropna=False).items()}
 row=dict(path=str(rel),filename=p.name,category=rel.parts[0],rows=len(df),columns=len(df.columns),target=t,candidates=hits,counts=counts,source_notes=[str(x.relative_to(D)) for x in notes],source_urls=list(dict.fromkeys(re.findall(r'https?://\S+',txt))),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),status='binary_candidate' if t and df[t].dropna().nunique()==2 and not df[t].isna().any() else 'needs_resolution',all_columns=list(df.columns),flags=[])
 if re.search(r'synthetic|synthetically|simulat',txt,re.I):row['flags'].append('notes_mention_synthetic_or_simulation')
 if re.search(r'altered|make.it.imb|make.it.more.imb|sampled|reduced',str(p),re.I):row['flags'].append('prepared_or_resampled_variant')
 if not row['source_urls']:row['flags'].append('no_source_URL_in_notes')
 rows.append(row)
(R/'inventory.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False))
print('CANDIDATES',len(rows))
for i,r in enumerate(rows):print(i,r['filename'],r['rows'],r['target'],r['counts'],r['status'])
