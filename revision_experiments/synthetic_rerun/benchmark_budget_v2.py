import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'threshold_theory'))
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'threshold_influence'))
from pathlib import Path
import json,time,signal,tracemalloc,statistics
import numpy as np
from minimum_budget import within_budget
from budget_v2 import BudgetSolver
root=Path(__file__).parent
protocol={'seed':42081,'n':[64,128,256],'patterns':['distinct','16groups'],'budgets':[2],'distance_fraction':0.05,'repeats':3,'timeout_per_call':10,'includes_preparation':True,'memory':'separate tracemalloc peak run; not RSS','baseline':'previous exact unpruned DP, same feasibility task','no_data_selection':'all six predefined configurations'}
(root/'budget_scaling_protocol.json').write_text(json.dumps(protocol,indent=2))
rng=np.random.default_rng(42081);rows=[]
def alarm(*args):raise TimeoutError()
signal.signal(signal.SIGALRM,alarm)
for pattern in protocol['patterns']:
    for n in protocol['n']:
        s=rng.permutation(n).astype(float)
        if pattern=='16groups':s=np.floor(s*16/n)
        y=(rng.random(n)<.1).astype(int);d=int(np.ceil(.05*n));B=2
        funcs={'old':lambda:within_budget(s,y,d,B),'new':lambda:BudgetSolver(s,y).within(d,B)}
        timing={'old':[],'new':[]};answer={};memory={}
        for rep in range(3):
            for name in (['old','new'] if rep%2==0 else ['new','old']):
                signal.alarm(10);start=time.perf_counter()
                try:out=funcs[name]();timing[name].append(time.perf_counter()-start);answer[name]=out['feasible']
                except TimeoutError:timing[name].append(None)
                finally:signal.alarm(0)
        if len(answer)==2:assert answer['old']==answer['new']
        for name,fn in funcs.items():
            tracemalloc.start();signal.alarm(10)
            try:fn();memory[name]=tracemalloc.get_traced_memory()[1]
            except TimeoutError:memory[name]=None
            finally:signal.alarm(0);tracemalloc.stop()
        med={k:statistics.median(v) if None not in v else None for k,v in timing.items()}
        row={'n':n,'g':len(set(s)),'pattern':pattern,'B':B,'d':d,'feasible':answer,'seconds':timing,'median':med,'speedup':med['old']/med['new'] if all(v is not None for v in med.values()) else None,'peak_bytes':memory}
        rows.append(row);(root/'budget_scaling_results.json').write_text(json.dumps(rows,indent=2));print(row,flush=True)
