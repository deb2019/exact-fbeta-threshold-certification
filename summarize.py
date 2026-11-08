from pathlib import Path
import json,csv
from collections import Counter
import numpy as np,pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parent
sel=json.loads((R/'selection.json').read_text());records=[];audits=[]
assert len(list((R/'results').glob('*/completed.json')))==71,'Wait for all experiments'
for p in sorted((R/'results').glob('*/completed.json')):
 records+=json.loads((p.parent/'results.json').read_text());audits.append(json.loads((p.parent/'audit.json').read_text()))
lookup={r['id']:r for r in sel}
cat=lambda s:s.split('(')[0].strip().replace('Fraud Dectection','Fraud / insurance').replace('Medical Data','Medical').replace('Predictive Maintenance','Maintenance / other')
def label(r):return 'Unknown' if r['status']=='timeout' else str(r['minimum_budget']) if r['status']=='exact' else '≥3'
for r in records:r['category']=cat(lookup[r['dataset']]['category']);r['budget_label']=label(r)
rows=[]
for category in sorted({r['category'] for r in records}):
 rr=[r for r in records if r['category']==category]
 for f in [.05,.1]:
  x=[r for r in rr if r['fraction']==f];c=Counter(label(r) for r in x)
  rows.append(dict(category=category,tasks=len({r['dataset'] for r in rr}),fraction=f,analyses=len(x),one=c['1'],two=c['2'],at_least_three=c['≥3'],unknown=c['Unknown']))
for f in [.05,.1]:
 x=[r for r in records if r['fraction']==f];c=Counter(label(r) for r in x);rows.append(dict(category='All',tasks=len(audits),fraction=f,analyses=len(x),one=c['1'],two=c['2'],at_least_three=c['≥3'],unknown=c['Unknown']))
assert len(records)==12*len(audits)
summary=dict(tasks=len(audits),vectors=len({r['run'] for r in records}),analyses=len(records),witnesses=sum(r['status']=='exact' for r in records),timeouts=sum(r['status']=='timeout' for r in records),minimum_validation_size=min(r['n'] for r in records),maximum_validation_size=max(r['n'] for r in records),category_rows=rows,prepared_positive_rate_range=[min(a['positive_rate'] for a in audits),max(a['positive_rate'] for a in audits)])
(R/'summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False));(R/'all_results.json').write_text(json.dumps(records,indent=2,ensure_ascii=False));pd.DataFrame(rows).to_csv(R/'category_summary.csv',index=False)
flat=[]
for r in sel:
 a=next((a for a in audits if a['dataset']==r['id']),None)
 flat.append(dict(id=r['id'],file=r['filename'],category=cat(r['category']),target=r['target'],encoded_positive=r['positive_value'],raw_rows=r['rows'],raw_counts=json.dumps(r['counts']),status='completed' if a else 'not_splittable_after_cleaning' if r['id']=='D016' else 'excluded',reason='No rows remain after conflicting-feature-group removal' if r['id']=='D016' else r['reason'],retained_rows=a['n'] if a else '',removed_conflicts=a['removed_conflicts'] if a else '',removed_duplicates=a['removed_duplicates'] if a else '',dropped_columns='; '.join(r['drop_columns']),input_sha256=r['sha256'],input_relative_path=r['path']))
pd.DataFrame(flat).to_csv(R/'dataset_catalog.csv',index=False)
plt.rcParams.update({'font.size':10})
fig,axs=plt.subplots(2,1,figsize=(7.2,6.8),constrained_layout=True)
rr=[r for r in rows if r['fraction']==.05 and r['category']!='All'];y=np.arange(len(rr));left=np.zeros(len(rr))
for key,name,color in [('one','1 edit','#367da2'),('two','2 edits','#df9b40'),('at_least_three','At least 3','#83959b'),('unknown','Unknown','#c85862')]:
 vals=np.array([r[key] for r in rr]);axs[0].barh(y,vals,left=left,label=name,color=color)
 for j,v in enumerate(vals):
  if v:axs[0].text(left[j]+v/2,j,str(v),ha='center',va='center',fontsize=8)
 left+=vals
axs[0].set_yticks(y,[r['category'] for r in rr]);axs[0].set_xlabel('Model–split vectors (5% distance)');axs[0].set_title('A  Prepared-task certificate counts');axs[0].legend(fontsize=8,loc='lower center',bbox_to_anchor=(.5,-.42),ncol=4)
for model,color,marker in [('LR','#367da2','o'),('RF','#df9b40','^')]:
 rr=[r for r in records if r['model']==model and r['fraction']==.05];axs[1].scatter([r['n'] for r in rr],[r['g']/r['n'] for r in rr],s=16,alpha=.55,label=model,c=color,marker=marker)
axs[1].set_xscale('log');axs[1].set_xlabel('Validation records');axs[1].set_ylabel('Distinct-score fraction g/n');axs[1].set_title('B  Observed score ties');axs[1].legend()
for ax in axs:ax.spines[['top','right']].set_visible(False)
for ext in ['png','pdf','svg']:fig.savefig(R/('Figure_4_Prepared_Data_Extension.'+ext),dpi=300,bbox_inches='tight')
print(json.dumps(summary,indent=2))
