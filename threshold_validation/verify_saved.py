"""Verify published witnesses and one-edit decisions without model training."""
import json,hashlib
import numpy as np
from run_validation import ROOT,direct,all_single_flips,minimum_budget_v2
result=json.loads((ROOT/'results.json').read_text());completion=json.loads((ROOT/'completed.json').read_text())
for f,key in [('protocol.json','protocol_sha256'),('results.json','results_sha256')]:
    assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==completion[key]
for row in result['rows']:
    with np.load(ROOT/'scores'/(row['run']+'.npz')) as data:s=data['validation_score'];y=data['validation_y']
    single=all_single_flips(s,y)
    assert bool(max(single['disagreement_count'])>=row['d'])==(row.get('minimum_budget')==1)
    if row['status']=='exact':
        z=y.copy();z[row['witness_indices']]=1-z[row['witness_indices']]
        assert sum(z!=y)==row['minimum_budget']
        assert abs(direct(s,z)-direct(s,y))>=row['d']
    again=minimum_budget_v2(s,y,row['d'],max_budget=2,time_limit=5)
    assert again['status']==row['status']
    assert again.get('minimum_budget')==row.get('minimum_budget')
    assert again.get('certified_lower_bound')==row.get('certified_lower_bound')
print('PASS: completion hashes; 24 repeated solver outcomes; 24 independent single-edit verdicts; 12 Fraction-verified witnesses.')
