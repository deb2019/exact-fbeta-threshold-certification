from pathlib import Path
import json,numpy as np,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parent;root=R.parent;out=R/'figures';out.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42,'svg.fonttype':'none'})
colors=['#0072B2','#E69F00','#7A7A7A']
def save(fig,name):
 fig.savefig(out/(name+'.png'),dpi=300,bbox_inches='tight');fig.savefig(out/(name+'.pdf'),bbox_inches='tight');fig.savefig(out/(name+'.svg'),bbox_inches='tight');plt.close(fig)
# Real, already verified two-edit witness.
r=json.loads((root/'source_benchmarks/combined_results.json').read_text())['rows'];x=next(x for x in r if x['dataset']=='ctg' and x.get('minimum_budget')==2 and x['distance_fraction']==.05)
a=np.load(root/'threshold_validation/scores'/(x['run']+'.npz'));s=a['validation_score'];y=a['validation_y'];z=y.copy();z[x['witness_indices']]=1-z[x['witness_indices']];order=np.argsort(-s,kind='stable');ends=np.r_[np.flatnonzero(s[order][:-1]!=s[order][1:]),len(s)-1];K=np.r_[0,ends+1]
def f(label):
 A=np.r_[0,np.cumsum(label[order])[ends]];return 5*A/np.maximum(4*sum(label)+K,1)
fig,ax=plt.subplots(2,1,figsize=(7,4.8),gridspec_kw={'height_ratios':[3,1.4]},layout='constrained')
ax[0].plot(K,f(y),color=colors[0],label='Original labels');ax[0].plot(K,f(z),color=colors[1],ls='--',label='Two edited labels')
for k,c,tag in [(x['old_k'],colors[0],'Original cutoff'),(x['new_k'],colors[1],'Edited cutoff')]:ax[0].axvline(k,color=c,ls=':',lw=1);ax[0].scatter([k],[f(y if c==colors[0] else z)[np.flatnonzero(K==k)[0]]],color=c,s=35,zorder=5)
ax[0].set(xlabel='Predicted-positive count K (scores held fixed)',ylabel='$F_2$',title='A  Cutoff reselection after a verified two-label edit');ax[0].legend(loc='lower right',frameon=False)
for j,(lab,k,c) in enumerate([('Original',x['old_k'],colors[0]),('Edited',x['new_k'],colors[1])]):
 ax[1].barh(j,k,color=c,height=.45);ax[1].barh(j,len(y)-k,left=k,color='#eeeeee',height=.45)
lo,hi=sorted([x['old_k'],x['new_k']]);ax[1].axvspan(lo,hi,color='#CC79A7',alpha=.25)
ax[1].set(yticks=[0,1],yticklabels=['Original','Edited'],xlabel='Records ordered by decreasing score',title=f"B  {abs(x['new_k']-x['old_k'])} changed decisions; required d = {x['d']}",xlim=(0,len(y)));ax[1].invert_yaxis()
save(fig,'Figure_1_Certificate_Witness');(out/'figure1_source.json').write_text(json.dumps(x,indent=2))
# Certificate composition.
fig,ax=plt.subplots(1,2,figsize=(9,4),layout='constrained',gridspec_kw={'width_ratios':[1.1,1]})
names=['ctg','wdbc','climate','seismic','blood','mammographic','spambase'];disp={'ctg':'CTG','wdbc':'WDBC','climate':'Climate','seismic':'Seismic','blood':'Blood','mammographic':'Mammographic','spambase':'Spambase'};start=np.zeros(7)
for cat,c,label in [(1,colors[0],'Exactly 1'),(2,colors[1],'Exactly 2'),(3,colors[2],'At least 3')]:
 vals=[sum((x.get('minimum_budget')==cat if cat<3 else x['status']=='lower_bound') for x in r if x['dataset']==name and x['distance_fraction']==.05) for name in names]
 ax[0].barh([disp[q] for q in names],vals,left=start,color=c,label=label);start+=vals
ax[0].invert_yaxis();ax[0].set(xlabel='Model–split runs (six per dataset)',title='A  Main benchmarks, 5% distance',xlim=(0,6),xticks=range(7))
cdata=json.loads((root/'cleaning_sensitivity/summary.json').read_text());labels=[];counts=[]
for name in ['blood','mammographic']:
 for arm,short in [('all_rows','All rows'),('deduplicate_same_label','Deduplicate'),('exclude_conflicts','Exclude conflicts')]:
  q=next(q for q in cdata if q['dataset']==name and q['fraction']==.05 and q['arm']==arm);labels.append(('Blood' if name=='blood' else 'Mammo.')+' / '+short);counts.append([q['exact_one'],q['exact_two'],q['lower_bound']])
start=np.zeros(6)
for j,c in enumerate(colors):v=np.array(counts)[:,j];ax[1].barh(labels,v,left=start,color=c);start+=v
ax[1].invert_yaxis();ax[1].set(xlabel='Model–split runs (six per policy)',title='B  Cleaning sensitivity, 5% distance',xlim=(0,6),xticks=range(7));fig.legend(*ax[0].get_legend_handles_labels(),loc='outside lower center',ncol=3,frameon=False)
save(fig,'Figure_2_Budgets_and_Cleaning')
# Runtime panels; new same-host synthetic runs.
b=json.loads((R/'synthetic_rerun/benchmark_results.json').read_text())['rows'];br=json.loads((R/'results.json').read_text());scale=json.loads((root/'scalability/results.json').read_text())
fig,ax=plt.subplots(2,2,figsize=(9,7.2),layout='constrained')
for axis,task,title in [(ax[0,0],'flip','A  All single-label flips'),(ax[0,1],'swap','B  Positive–negative swap histogram')]:
 for pattern,ls in [('distinct','-'),('16_tied_groups','--')]:
  rr=[x for x in b if x['task']==task and x['pattern']==pattern]
  for key,c,name in [('fast_seconds',colors[0],'Specialized'),('baseline_seconds',colors[1],'Batched scan')]:axis.plot([x['n'] for x in rr],[1000*x[key] for x in rr],marker='o',ls=ls,color=c,label=name+(' / distinct' if ls=='-' else ' / tied'))
 axis.set(xscale='log',yscale='log',xlabel='n',ylabel='Median time (ms)',title=title);axis.grid(alpha=.2)
ax[0,0].legend(fontsize=7,frameon=False)
rr=[x for x in br if not x['case'].startswith('synthetic')];idx=np.arange(len(rr));axis=ax[1,0]
for j,(meth,c) in enumerate([('DP',colors[0]),('pair_scan',colors[1]),('MILP_HiGHS',colors[2])]):
 for i,x in enumerate(rr):
  runs=x['methods'][meth];ts=[v['seconds'] for v in runs];timeout=any(v['status']=='timeout' for v in runs)
  axis.scatter(i+(j-1)*.2,np.median(ts)*1000,c=c,marker='^' if timeout else 'o',s=35,label={'DP':'DP','pair_scan':'Pair scan','MILP_HiGHS':'MILP (HiGHS)'}[meth] if i==0 else None)
axis.set(yscale='log',xticks=idx,xticklabels=[{'ctg':'CTG','wdbc':'WDBC','spambase':'Spambase'}[x['case'].split('_')[0]]+'\n'+x['case'].split('_')[1] for x in rr],ylabel='Time (ms)',title='C  Minimum arbitrary-edit budget ≤ 2');axis.tick_params(axis='x',labelsize=7.5);axis.legend(fontsize=7,frameon=False);axis.text(.02,.97,'▲ includes a timeout (censored)',transform=axis.transAxes,va='top',fontsize=7);axis.grid(axis='y',alpha=.2)
axis=ax[1,1]
for model,c in [('LR',colors[0]),('RF',colors[1])]:
 for f,ls in [(.05,'-'),(.1,'--')]:
  ns=[];means=[];low=[];high=[]
  for size in [1000,5000,10000,'full']:
   q=[x for x in scale if x['model']==model and x['fraction']==f and x['size_requested']==size];ns.append(np.mean([x['n'] for x in q]));ts=np.array([x['median_seconds'] for x in q])*1000;means.append(np.median(ts));low.append(min(ts));high.append(max(ts))
  axis.plot(ns,means,c=c,ls=ls,marker='o',label=f'{model}, {int(f*100)}%');axis.fill_between(ns,low,high,color=c,alpha=.08)
axis.set(xlabel='Certification n',ylabel='Solver time (ms)',title='D  Bank Marketing, B ≤ 2');axis.legend(fontsize=7,frameon=False);axis.grid(alpha=.2)
save(fig,'Figure_3_Computational_Performance')
