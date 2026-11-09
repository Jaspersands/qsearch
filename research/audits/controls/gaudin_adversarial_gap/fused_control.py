"""One EXACT rational compressed n=64 control; no physical fusion claim.

Entry interpreter: /opt/anaconda3/bin/python.
Sage QQ/Sturm subprocess: /opt/anaconda3/envs/qsearch-cas/bin/python.
No optimizer rerun, size sweep, network, or full physical spin matrix.
"""
import json
import subprocess
from pathlib import Path

import numpy as np
from scipy.linalg import eigh_tridiagonal


N_CLUSTER = 64
S = N_CLUSTER / 2
G = 1 / (2 * N_CLUSTER)
m = np.arange(-S, S + 1)
diagonal = m + G * m**2
offdiagonal = -G / 2 * (S * (S + 1) - m[:-1] * (m[:-1] + 1))
numerical = eigh_tridiagonal(diagonal, offdiagonal, select='i',
                             select_range=(0, 2), eigvals_only=True)
if numerical[1] - numerical[0] >= 0.5:
    raise RuntimeError('Fixed n64 numerical trigger absent; stop, do not expand.')

SAGE_CERTIFICATE = r'''
import json
from sage.all import QQ, ZZ
n = ZZ(64)
S = QQ(n)/2
g = QQ(1)/(2*n)
ms = [QQ(-S+i) for i in range(n+1)]
ds = [a+g*a*a for a in ms]
es = [-g/2*(S*(S+1)-a*(a+1)) for a in ms[:-1]]
assert len(ds)==65 and len(es)==64 and all(e!=0 for e in es)

def count_below(x):
    # p_k=det(H_k-xI); Sylvester/Jacobi Sturm inertia counts signs of
    # [p_0,...,p_D]. Ignore internal zeros; consecutive zeros are excluded
    # by nonzero offdiagonals. Endpoints must not be eigenvalues.
    p0, p1 = QQ(1), ds[0]-x
    signs = [int(p0.sign()), int(p1.sign())]
    for k in range(1,len(ds)):
        p2 = (ds[k]-x)*p1-es[k-1]**2*p0
        signs.append(int(p2.sign()))
        p0,p1 = p1,p2
    assert signs[-1]!=0
    nonzero = [s for s in signs if s]
    variations = sum(a!=b for a,b in zip(nonzero,nonzero[1:]))
    return {'endpoint':str(x),'signs_leading_principal_determinants':signs,
            'internal_zero_count':signs[:-1].count(0),
            'full_determinant_nonzero':True,
            'number_of_eigenvalues_strictly_below':int(variations)}

intervals=[(QQ(-24173)/1000,QQ(-24172)/1000),
           (QQ(-23904)/1000,QQ(-23903)/1000)]
certificates=[]
for k,(lo,hi) in enumerate(intervals):
    left,right=count_below(lo),count_below(hi)
    assert left['number_of_eigenvalues_strictly_below']==k
    assert right['number_of_eigenvalues_strictly_below']==k+1
    assert 0<hi-lo<=QQ(1)/1000
    certificates.append({'eigenvalue_index_from_zero':k,
       'open_interval':[str(lo),str(hi)],'width':str(hi-lo),
       'left_inertia':left,'right_inertia':right})
lower=intervals[1][0]-intervals[0][1]
upper=intervals[1][1]-intervals[0][0]
assert 0<lower<upper<QQ(1)/2
print(json.dumps({'arithmetic':'Sage exact QQ',
  'matrix_is_irreducible_real_symmetric_tridiagonal':True,
  'certificate_method':'Jacobi Sturm sign variations of det(H_k-xI)',
  'eigenvalue_certificates':certificates,
  'strict_lowest_gap_interval':[str(lower),str(upper)],
  'strict_lowest_gap_upper_bound':str(upper),
  'strict_upper_bound_less_than_half':True,
  'conditional_fused_squared_charge_gap_upper_bound':str(2*upper**2/n),
  'conditional_physical_threshold':str(QQ(1)/(2*n))}))
'''
completed = subprocess.run(
    ['/opt/anaconda3/envs/qsearch-cas/bin/python', '-c', SAGE_CERTIFICATE],
    check=True, capture_output=True, text=True)
exact = json.loads(completed.stdout)
result = {
    'status': 'EXACT_COMPRESSED_LOWEST_GAP_LT_HALF',
    'scope': 'One n64 two-spin compressed matrix only; no n sweep or optimizer rerun.',
    'fixed_parameters': {'cluster_size_n': N_CLUSTER, 'conditional_physical_N': 128,
                         'S': '32', 'g': '1/128', 'total_Sz': 0,
                         'matrix_dimension': 65, 'm_range': [-32, 32]},
    'matrix_formula': {'diagonal': 'd_m=m+g*m^2',
                       'offdiagonal_m_to_m_plus_1': '-g/2*(S*(S+1)-m*(m+1))',
                       'operator': 'H=S_Az-g*S_A dot S_B on total Sz=0'},
    'characteristic_recurrence':
        'p_0=1; p_1=d_0-x; p_(k+1)=(d_k-x)*p_k-e_(k-1)^2*p_(k-1)',
    'numerical_first_three_eigenvalues': numerical.tolist(),
    'numerical_lowest_gap': float(numerical[1]-numerical[0]),
    'exact': exact,
    'fusion_obligation': 'Parent must prove embedding into native charges and finite distinct-site continuation.',
    'conditional_charge_gap_formula': 'squared_joint_gap=2*(Delta h)^2/n',
    'claim_gates': {'full_physical_native_gap_counterexample': False,
                    'finite_distinct_native_site_realization': False,
                    'asymptotic_gap_claim': False, 'algorithm': False,
                    'hardness': False, 'novelty': False, 'quantum_execution': False},
}
Path(__file__).with_name('fused_result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status': result['status'],
                  'numerical_first_three_eigenvalues': numerical.tolist(),
                  'numerical_lowest_gap': result['numerical_lowest_gap'],
                  'strict_exact_lowest_gap_interval': exact['strict_lowest_gap_interval'],
                  'endpoint_eigenvalue_counts': [
                      [c['left_inertia']['number_of_eigenvalues_strictly_below'],
                       c['right_inertia']['number_of_eigenvalues_strictly_below']]
                      for c in exact['eigenvalue_certificates']],
                  'conditional_fused_squared_charge_gap_upper_bound':
                      exact['conditional_fused_squared_charge_gap_upper_bound']},indent=2))
