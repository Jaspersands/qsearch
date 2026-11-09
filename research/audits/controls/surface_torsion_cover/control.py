"""Exact classical falsifiers/normalizations, not a torsion-cover algorithm.

Algebra interpreter: /opt/anaconda3/envs/qsearch-cas/bin/python
"""
import json
from itertools import product
from pathlib import Path
from sage.all import (CyclotomicField, GF, PolynomialRing, QQ, ZZ, binomial,
                      identity_matrix, matrix, prod)


# A rational linear combination of permutation characters is rational-valued.
k = GF(7)
g = matrix(k, [[0, -1], [1, 3]])
assert g.det() == 1 and g.multiplicative_order() == 8
K = GF(49, 'a')
SK = PolynomialRing(K, 'u')
u = SK.gen()
lam = (u**2 - 3*u + 1).roots(multiplicities=False)[0]
assert lam.multiplicative_order() == 8 and lam + lam**(-1) == 3
C = CyclotomicField(8)
z = C.gen()
lifted_trace = z + z**(-1)
minimal_polynomial = lifted_trace.minpoly()
assert minimal_polynomial == PolynomialRing(QQ, 'x')([-2, 0, 1])
assert lifted_trace not in QQ
obstruction = {
    'g': [[0, -1], [1, 3]], 'field': 'F7', 'determinant': 1, 'order': 8,
    'eigenvalue_field': 'F49', 'eigenvalue_order': 8, 'eigenvalue_trace': '3',
    'Brauer_trace_minimal_polynomial': str(minimal_polynomial),
    'Brauer_trace_is_rational': False,
    'conclusion': 'Natural SL2(F7) module is not in the rational span of permutation modules: their Brauer characters are rational-valued at this 7-regular element.',
}
print('DECISIVE: order-8 natural Brauer trace has minimal polynomial x^2-2; untwisted rational permutation identity fails.', flush=True)

# A formal 64-dimensional rational representation; no curve realization claimed.
def twisted_trace(h, r):
    return sum(binomial(r, s)*j**(r-s)*sum(
        binomial(s, b)*8 for b in range(s+1) if (h+s-2*b) % 8 == 0)
        for j in range(2, 10) for s in range(r+1))


power_sums = [C(0)] + [sum(z**(-h)*twisted_trace(h, r) for h in range(8))/8
                        for r in range(1, 9)]
sector_eigenvalues = [C(j) + lifted_trace for j in range(2, 10)]
assert all(power_sums[r] == sum(a**r for a in sector_eigenvalues) for r in range(1, 9))
elementary = [C(1)]
for r in range(1, 9):
    numerator = sum((-1)**(i-1)*elementary[r-i]*power_sums[i] for i in range(1, r+1))
    elementary.append(numerator/r)  # In characteristic zero, including r=7.
assert all(a.denominator() == 1 for e in elementary for a in e.list())
SC = PolynomialRing(C, 'T')
T = SC.gen()
recovered = sum((-1)**j*elementary[j]*T**(8-j) for j in range(9))
assert recovered == prod(T-a for a in sector_eigenvalues)


def reduce_integral(e):
    return sum(K(ZZ(a))*lam**j for j, a in enumerate(e.list()))


TK = PolynomialRing(K, 'T')
t = TK.gen()
reduced = TK([reduce_integral(a) for a in recovered.list()])
assert reduced == prod(t - (K(j)+lam+lam**(-1)) for j in range(2, 10))
fourier = {
    'formal_rational_representation_dimension': 64, 'character_sector_dimension': 8,
    'twisted_traces_checked': 64, 'power_sum_orders': list(range(1, 9)),
    'fourier_projection_exact': True, 'Newton_over_characteristic_zero_then_reduce': True,
    'order_7_division_performed_before_reduction': True,
    'e7_integral': str(elementary[7]), 'characteristic_polynomial_mod_7': str(reduced),
    'reduced_characteristic_polynomial_matches_eigenvalues': True,
    'toy_F_curve_zeta_realization_claimed': False,
}

# A smooth non-diagonal quartic surface and its actual finite pencil counts.
S = PolynomialRing(k, names=('x0', 'x1', 'x2', 'x3'))
x0, x1, x2, x3 = S.gens()
f = x0**4 + x1**4 + x2**4 - x3**4 + x0*x1*x2*x3
partials = [f.derivative(v) for v in S.gens()]
for v in S.gens():
    assert S.ideal(partials + [v-1]).groebner_basis() == [S(1)]


def projective_points(dimension):
    for leading in range(dimension+1):
        for tail in product(k, repeat=dimension-leading):
            yield (k(0),)*leading + (k(1),) + tail


surface_count = sum(f(*point) == 0 for point in projective_points(3))
base_count = sum(f(0, 0, *point) == 0 for point in projective_points(1))
SU = PolynomialRing(k, 'b')
b = SU.gen()
base_polynomial = b**4 - 1
assert base_polynomial.gcd(base_polynomial.derivative()) == 1
fiber_counts = {}
for parameter in k:
    fiber_counts[str(parameter)] = int(sum(f(parameter*a, a, b, c) == 0
                                         for a, b, c in projective_points(2)))
fiber_counts['infinity'] = int(sum(f(a, 0, b, c) == 0 for a, b, c in projective_points(2)))
assert sum(fiber_counts.values()) == surface_count + 7*base_count
pencil = {
    'surface': str(f), 'smooth_over_algebraic_closure': True,
    'smoothness_certificate': 'All four affine gradient chart ideals have Groebner basis [1].',
    'base_locus_geometric_degree': 4, 'base_locus_transverse': True,
    'surface_F7_points': int(surface_count), 'base_F7_points': int(base_count),
    'fiber_F7_points': fiber_counts, 'sum_fiber_points': sum(fiber_counts.values()),
    'normalization_identity': 'sum_t #fiber_t = #X + 7 #B',
    'scope': 'Finite classical point-count/Leray normalization only.',
}
result = {
    'status': 'PASS', 'untwisted_Artin_obstruction': obstruction,
    'formal_twisted_Fourier_control': fourier, 'quartic_pencil_control': pencil,
    'claim_gates': {'native_algorithm': False, 'quantum_execution': False,
                    'novelty': False, 'speedup': False},
}
Path(__file__).with_suffix('.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
