"""Nonunit-output reduction controls, LOCAL DERIVATION / REVIEW PENDING.

Exact arithmetic for scoped native-input existence bounds. No quantum
solver, source attack, security estimate or independent proof verification.
"""

import itertools
import json
import math
from collections import Counter
from pathlib import Path

import sympy as sp


counts = Counter()


def convolution(a):
    d = len(a)
    S = sp.zeros(d)
    for j in range(d-1):
        S[j+1, j] = 1
    S[0, d-1] = -1
    v = sp.Matrix(a)
    return sp.Matrix.hstack(*(S**j * v for j in range(d)))


def rank_mod(M, q):
    A = [[int(v) % q for v in row] for row in M.tolist()]
    rank = 0
    for col in range(M.cols):
        pivot = next((i for i in range(rank, M.rows) if A[i][col]), None)
        if pivot is None:
            continue
        A[rank], A[pivot] = A[pivot], A[rank]
        inverse = pow(A[rank][col], -1, q)
        A[rank] = [v * inverse % q for v in A[rank]]
        for i in range(M.rows):
            if i != rank and A[i][col]:
                scalar = A[i][col]
                A[i] = [(x - scalar*y) % q for x, y in zip(A[i], A[rank])]
        rank += 1
    return rank


for d in (2, 4):
    for q in (3, 5, 7, 11, 13, 17, 19):
        f = next(i for i in range(1, d+1) if pow(q, i, 2*d) == 1)
        if f < d//2:
            counts['low_residue_degree_family_excluded'] += 1
            continue
        for h in itertools.product(range(-2, 3), repeat=d):
            if not any(h):
                continue
            H = convolution(h)
            determinant = abs(int(H.det()))
            norm2 = sum(v*v for v in h)
            assert determinant > 0 and determinant**2 <= norm2**d
            counts['exact_hadamard_controls'] += 1
            rank = rank_mod(H, q)
            if rank < d:
                assert rank <= d - f
                assert determinant % (q**f) == 0
                assert norm2 >= q
                counts['nonunit_norm_and_divisibility_controls'] += 1

# Outside the high-degree family, the proposed sqrt(q) bound is FALSE.
h = (0, 0, 0, 1, 0, 1, 1, 1)
q = 17
H = convolution(h)
assert int(H.det()) % q == 0 and sum(v*v for v in h) < q
counts['low_degree_counterexample_retained'] += 1

# The zero polynomial is excluded: its rational multiplication matrix is singular.
assert convolution((0, 0)).det() == 0
counts['zero_polynomial_excluded'] += 1

# Distinct points in either CRT ideal really have sqrt(q) separation.
for q in (5, 13, 17):
    roots = [r for r in range(q) if r*r % q == q-1]
    assert len(roots) == 2
    for root in roots:
        for w in (1, 2, 3):
            limit = math.isqrt(q*w*w)
            points = [h for h in itertools.product(range(-limit, limit+1), repeat=2)
                      if sum(v*v for v in h) <= q*w*w and (h[0]+root*h[1]) % q == 0]
            assert len(points) <= (1+2*w)**2
            for i, a in enumerate(points):
                for b in points[i+1:]:
                    assert sum((x-y)**2 for x, y in zip(a, b)) >= q
            counts['exact_ideal_packing_controls'] += 1

artifact = json.loads(Path(__file__).with_name('native_rlwe_single_witness_d12_arithmetic.json').read_text())
rows = []
for row in artifact['parameter_rows']:
    d, q = row['d'], int(row['q'])
    assert row['residue_degree'] == d//2
    assert pow(q, d//2, 2*d) == 1 and pow(q, d//4, 2*d) != 1
    for lane in row['lanes']:
        Rs = lane['prior_radius']
        E = int(lane['total_training_error_norm_bound'])
        denominator = 16 * Rs**2 * E**2
        L = math.isqrt((q-1)//denominator)
        assert denominator * L**2 < q <= denominator * (L+1)**2
        numerator = (q-1) * (2*L+1)**(2*d)
        divisor = q**d
        assert numerator * 10**8 <= divisor
        adaptive_numerator = 2 * (q-1) * 45**d * 2**d
        adaptive_divisor = 16**d * (Rs*E)**(2*d) * (2**d-1)
        assert adaptive_numerator * 10**8 <= adaptive_divisor
        rows.append(dict(d=d, lane=lane['lane'], max_coordinate_magnitude=str(L),
                         exact_fixed_nonunit_existence_bound_le_1e_minus_8=True,
                         exact_ALL_adaptive_nonunit_existence_bound_le_1e_minus_8=True,
                         log10_all_adaptive_reference=math.log10(2*(q-1))+d*math.log10(45/(16*(Rs*E)**2))-math.log10(1-2.0**(-d)),
                         log10_cube_reference=math.log10(q-1)+2*d*math.log10(2*L+1)-d*math.log10(q)))
        counts['exact_large_row_bounds'] += 1

print(json.dumps(dict(scope='nonunit_syndromes_under_worst_case_noise_and_box_certificate',
                     counts=counts, parameter_rows=rows), indent=2))
