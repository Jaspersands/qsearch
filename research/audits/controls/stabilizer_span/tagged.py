"""Exact finite coefficient-extraction interface, not an all-n proof.

Run with /opt/anaconda3/envs/qsearch-cas/bin/python tagged.py.
"""

import json
from itertools import combinations, product
from pathlib import Path

from sage.all import AA, CyclotomicField, PolynomialRing, QQ, matrix, vector


B = CyclotomicField(8)
zeta = B.gen()
sqrt2 = zeta + zeta.conjugate()
P = PolynomialRing(B, 'x')
x = P.gen()
f = x**5 - 2
assert f.is_irreducible()
L = B.extension(f, 'theta')
theta = L.gen()
assert L.relative_degree() == 5
assert theta**5 == 2

n, K = 3, 4
epsilon = QQ(1) / 2**6 / (8 * K)
points = list(product(range(2), repeat=n))
E = [v for v in points if sum(v) <= 1]
R = vector(B, [1 if v in E else 0 for v in points])
states = [vector(B, [sqrt2**(-n)] * 2**n)]
for i, j in combinations(range(n), 2):
    cell = [v for v in points if tuple(k for k in range(n) if v[k])[:2] == (i, j)]
    states.append(vector(B, [sqrt2**(-(n - j - 1)) if v in cell else 0 for v in points]))
assert len(states) == K
tagged = vector(L, R) + epsilon * sum(
    (theta**(j + 1) * vector(L, state) for j, state in enumerate(states)), vector(L, 2**n))
coefficients = []
for entry in tagged:
    row = entry.list()
    coefficients.append(row + [B(0)] * (5 - len(row)))
C = matrix(B, coefficients)
expected = matrix(B, [R] + [epsilon * state for state in states]).transpose()
assert C == expected
V = matrix(B, states).transpose()
assert C.rank() == V.rank() == K
assert C.column_space() == V.column_space()
assert C.column(0) == R
assert all(C.column(j + 1) / epsilon == state for j, state in enumerate(states))

# AA comparisons certify the positive real embedding without floating tolerances.
Q = PolynomialRing(QQ, 't')
t = Q.gen()
roots = (t**5 - 2).roots(AA, multiplicities=False)
assert len(roots) == 1
real_theta = roots[0]
assert 1 < real_theta < 2
assert real_theta**K < 2

result = {
    'status': 'PASS',
    'scope': 'Finite exact coefficient-extraction interface; no alternative-decomposition search or all-n theorem evidence.',
    'n': n, 'K': K, 'base_field': 'Q(zeta_8)',
    'relative_polynomial': 'x^5 - 2', 'irreducible_over_base': True,
    'relative_degree': int(L.relative_degree()), 'absolute_degree': int(L.absolute_degree()),
    'epsilon': str(epsilon), 'coefficient_column_count': int(C.ncols()),
    'coefficient_rank': int(C.rank()), 'original_span_rank': int(V.rank()),
    'checks': {
        'coefficient_columns_equal_R_then_epsilon_states': True,
        'coefficient_span_equals_V': True, 'each_original_state_recovered_exactly': True,
        'field_identity_theta_power_5_equals_2': True,
        'exact_real_bounds_1_less_theta_less_2': True,
        'exact_real_bound_theta_power_K_less_2': True,
    },
    'claim_gates': {
        'general_rank_to_extent_bound': False, 'full_learner_execution': False,
        'quantum_execution': False, 'exhaustive_minimal_rank_search': False,
    },
}
Path(__file__).with_suffix('.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
