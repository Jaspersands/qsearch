"""Exact single G_m control for the two-filter classical relation candidate."""
import json
from pathlib import Path
from sage.all import QQ, ZZ, PolynomialRing, matrix, vector

P = PolynomialRing(QQ, names=('x','y'))
x, y = P.gens()
A = P.quotient(P.ideal(x*y-1), names=('xb','yb'))
xb, yb = A.gens()
polys = [2*x, 3*x**2, 12*x**4, x]
inverses = [y/2, y**2/3, y**4/12, y]
units = [A(f) for f in polys]
inv = [A(f) for f in inverses]
assert all(u*v == 1 for u,v in zip(units,inv))
# Omega_(A/Q) is free of rank1 with dx basis, since x is a unit and
# y dx+x dy=0. These inputs depend only on x, so no dy term is omitted.
dlogs = [A(g*f.derivative(x)) for f,g in zip(polys,inverses)]
assert dlogs == [yb,2*yb,4*yb,yb]
log_row = matrix(ZZ, [[1,2,4,1]])
images = [QQ(f(1,1)) for f in polys]
finite_rows = matrix(ZZ, [[u.valuation(2) for u in images],
                          [u.valuation(3) for u in images]])
combined = log_row.stack(finite_rows)
relations = combined.right_kernel()
expected = vector(ZZ, [-2,-1,1,0])
assert relations.rank() == 1 and expected in relations
assert matrix(ZZ,[expected]).row_module() == relations
only_dlog = vector(ZZ,[1,0,0,-1])
only_specialization = vector(ZZ,[0,0,0,1])
assert log_row*only_dlog == 0 and finite_rows*only_dlog != 0
assert finite_rows*only_specialization == 0 and log_row*only_specialization != 0
assert units[0]*inv[3] == 2
assert units[3] != 1 and images[3] == 1
assert inv[0]**2 * inv[1] * units[2] == 1
result = {'scope':'One exact classical algebra control, no general relation algorithm or complexity evidence.',
          'input':'Q[x,y]/(xy-1), units (2x,3x^2,12x^4,x)',
          'dlog_row':[1,2,4,1],
          'specialized_values':[str(u) for u in images],
          'finite_prime_valuation_rows':[[int(v) for v in row] for row in finite_rows.rows()],
          'relation_basis':[list(map(int,expected))],
          'dlog_only_false_relation':list(map(int,only_dlog)),
          'dlog_only_product':'2',
          'specialization_only_false_relation':list(map(int,only_specialization)),
          'specialization_only_original_product':'x',
          'exact_products_checked':True}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,separators=(',',':')))
