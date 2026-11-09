"""Exact local control; not the asymptotic algorithm or evidence for its theorem."""
from itertools import product, combinations
import json
from pathlib import Path
from sage.all import CyclotomicField, PolynomialRing, matrix, vector, binomial

K = CyclotomicField(8)
a = K.gen()
R = PolynomialRing(K, 'T')
T = R.gen()
S = PolynomialRing(K, 'z')
z = S.gen()
n, Q, J = 4, 3, 3
bits = list(product((0, 1), repeat=n))
groups = ((0, 1), (2, 3))
local = list(product((0, 1), repeat=2))
b = (1-T)*(1-T/2)
# Rows restore x0,x2,x1,x3 at T=0. Each measurement is a group sum.
rows = ((1-T/3, 0, T/3, T/3),
        (T, T, b, 0), (0, b, T, T),
        (T/3, T/3, 0, 1-T/3))
rows = tuple(tuple(R(c) for c in row) for row in rows)

def factor(f, u, v):
    return 1+2*u-3*v+a*u*v if f == 0 else 2-u+v+(1-a)*u*v

def dot(row, x):
    return sum(c*d for c, d in zip(row, x))

H = sum(factor(0, dot(rows[0], x), dot(rows[1], x)) *
        factor(1, dot(rows[2], x), dot(rows[3], x)) for x in bits)
assert H.degree() <= 8
for i, v in enumerate((0, 2, 1, 3)):
    assert [c(0) for c in rows[i]] == [int(j == v) for j in range(n)]

def assignment(t):
    return (0, 1) if t < 3 else (1, 0)

# Verify the supplied design's kernel implication, exactly over Q subset K.
for t in range(1, Q+1):
    for f in (0, 1):
        other = groups[1-assignment(t)[f]]
        for row in rows[2*f:2*f+2]:
            assert row[other[0]](t) == row[other[1]](t)

def jet(t, f, x, U, wrong_correction=False):
    correction_bits = x if wrong_correction else [int(i in U) for i in range(n)]
    vals = []
    for row in rows[2*f:2*f+2]:
        vals.append(S(dot([c(t) for c in row], x)) +
                    sum((S(c(t+z))-c(t))*correction_bits[i]
                        for i, c in enumerate(row)))
    return S(factor(f, *vals)).truncate(J)

def separated(t, E, U, *, wrong_correction=False, drop_restriction=False):
    total = S.zero()
    for sums in product(range(3), repeat=2):
        fibers = [[v for v in local if sum(v) == y] for y in sums]
        reps = [v[0] for v in fibers]
        acc = S.one()
        for g in (0, 1):
            f = assignment(t).index(g)
            subtotal = S.zero()
            for v in fibers[g]:
                if not drop_restriction and any(v[j] != 1 for j, i in enumerate(groups[g]) if i in E):
                    continue
                x = list(reps[0] + reps[1])
                for j, i in enumerate(groups[g]):
                    x[i] = v[j]
                subtotal += jet(t, f, x, U, wrong_correction)
            acc = (acc*subtotal).truncate(J)
        total += acc
    return total

def recovered_jet(t, **kwargs):
    total = S.zero()
    for size in range(J):
        for E in combinations(range(n), size):
            for u_size in range(size+1):
                for U in combinations(E, u_size):
                    total += (-1)**(size-u_size)*separated(t, E, U, **kwargs)
    return total.truncate(J)

jets = [recovered_jet(t) for t in range(1, Q+1)]
assert jets == [S(H(t+z)).truncate(J) for t in range(1, Q+1)]
A = matrix(K, [[binomial(k, j)*t**(k-j) if k >= j else 0
                for k in range(Q*J)] for t in range(1, Q+1) for j in range(J)])
coeffs = A.solve_right(vector(K, [p[j] for p in jets for j in range(J)]))
assert R(list(coeffs)) == H
wrong_correction = [recovered_jet(t, wrong_correction=True) for t in range(1, Q+1)]
wrong_restriction = [recovered_jet(t, drop_restriction=True) for t in range(1, Q+1)]
assert wrong_correction != jets
assert wrong_restriction != jets

out = {'scope': 'one exact supplied-design control, not asymptotic execution',
       'field': 'Q(zeta_8)', 'n': n, 'Q': Q, 'R': 2, 'J': J,
       'measurements': ['x0+x1', 'x2+x3'], 'direct_H': str(H),
       'H0': str(H(0)), 'jets': [str(p) for p in jets],
       'design_kernel_verified': True, 'all_jets_match': True,
       'hermite_full_polynomial_matches': True,
       'wrong_x_dependent_correction_rejected': True,
       'dropped_fixed_bits_rejected': True,
       'wrong_correction_jets': [str(p) for p in wrong_correction],
       'wrong_restriction_jets': [str(p) for p in wrong_restriction]}
Path(__file__).with_suffix('.json').write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps({k: v for k, v in out.items() if not k.endswith('jets') and k != 'direct_H'}))
