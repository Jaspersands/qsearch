"""Exact finite falsifiers for local seed/offset formulas, not a seed solver."""
from sage.all import QQ, matrix, vector, diagonal_matrix, identity_matrix
from pathlib import Path
import json

I = identity_matrix(QQ, 3)
checks = []
for m in (2, 3, 7, 20):
    A = diagonal_matrix(QQ, [1, 4, -25*2**(2*m)])
    B = diagonal_matrix(QQ, [5, 20, -2**(2*m)])
    U = matrix(QQ, [[1,-4,0],[1,1,0],[0,0,QQ(1)/5]])
    assert U.transpose()*A*U == B and U.det() == 1
    assert min(x.valuation(2) for x in U.list() if x) >= 0
    assert all((x.valuation(2) >= 2) for x in (A-B).list() if x)
    # Every first column congruent to e1 mod2 fails its norm equation mod8.
    for x in range(1,8,2):
        for y in range(0,8,2):
            for z in range(0,8,2):
                assert (x*x+4*y*y-25*2**(2*m)*z*z) % 8 == 1
    err = B.inverse()*(A-B)
    assert min(x.valuation(2) for x in err.list() if x) == 2
    a = 5*2**m
    R = matrix(QQ, [[QQ(5)/4,0,QQ(3)*a/4],[0,1,0],[QQ(3)/(4*a),0,QQ(5)/4]])
    F = R*U
    assert R.transpose()*A*R == A and R.det() == 1
    assert F.transpose()*A*F == B and F.det() == 1
    assert min(x.valuation(2) for x in F.list() if x) < 0
    checks.append({'m':m, 'exact_isometry':True, 'identity_residue_unliftable':True})

p = 17; s = p**4
A = diagonal_matrix(QQ, [1,p*p,-s])
P = matrix(QQ, [[3,0,QQ(1)/3],[0,1,0],[0,0,QQ(1)/3]])
B = P.transpose()*A*P
def reflection(v):
    v = vector(QQ,v)
    return I-2*v.column()*(v.row()*A)/(v*A*v)
v = vector(QQ,[1,0,4]); d = v*A*v
g = reflection(v)*reflection([0,1,0]); X = g*P
assert g.transpose()*A*g == A and g.det() == 1
assert X.transpose()*A*X == B and X.det() == 1
assert min(x.valuation(3) for x in X.list() if x) >= 0
assert d.valuation(3) == 1 and (d/3) % 3 == 1
assert 1+g.trace() == 0
signs = [I,diagonal_matrix(QQ,[1,-1,-1]),diagonal_matrix(QQ,[-1,1,-1]),diagonal_matrix(QQ,[-1,-1,1])]
ts = [1+(D*g).trace() for D in signs]
assert sum(ts) == 4 and ts[3] == 4/d
theta = d*p*p
theta_signs = [1,-p*p*s,-s,p*p]
for t, th in zip(ts, theta_signs):
    if t:
        assert QQ(th*t/theta).is_square()
assert min(x.valuation(17) for x in P.list() if x) >= 0
assert min(x.valuation(17) for x in P.inverse().list() if x) >= 0
report = {'scope':'Finite exact falsifiers only; no uniform seed construction or complexity theorem.',
          'dyadic_cases':checks,'p17_neighbor_place':3,'p17_offset_trivial':True,
          'single_trace_degenerate':True,'four_chart_formula':True}
Path(__file__).with_name('local_offset_result.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'dyadic_cases':len(checks),'neighbor':True,'four_charts':True}))
