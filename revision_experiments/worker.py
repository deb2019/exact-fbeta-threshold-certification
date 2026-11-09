import sys,json,time,numpy as np
from baselines import dp,scan,integer_program
name,path,d=sys.argv[1:];a=np.load(path);t=time.perf_counter();r={'DP':dp,'pair_scan':scan,'MILP_HiGHS':integer_program}[name](a['s'],a['y'],int(d),seconds=5);print(json.dumps(dict(seconds=time.perf_counter()-t,**r)))
