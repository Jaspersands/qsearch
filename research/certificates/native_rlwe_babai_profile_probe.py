"""Targeted native-kernel classical certificate, LOCAL REVIEW PENDING.

This is one finite input, not an asymptotic attack or a quantum solver.
The ratio polynomial has its actual conditional uniform native law. The
profile certificate applies to every affine coset of this same kernel.
"""

import argparse
import json
import random
import time
from pathlib import Path

import sympy as sp


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--backend', choices=('sympy', 'flint'), default='sympy')
parser.add_argument('--save', action='store_true', help='Save the generated mathematical certificate beside this probe.')
args = parser.parse_args()

seed = 290952
rng = random.Random(seed)
source = json.loads(Path(__file__).with_name('native_rlwe_single_witness_d12_arithmetic.json').read_text())
parameter = next(row for row in source['parameter_rows'] if row['d'] == 64)
d, q = parameter['d'], int(parameter['q'])
m = [rng.randrange(q) for _ in range(d)]
centered = [(v + q//2) % q - q//2 for v in m]
S = sp.zeros(d)
for j in range(d-1):
    S[j+1, j] = 1
S[0, d-1] = -1
v = sp.Matrix(centered)
M = sp.Matrix.hstack(*(S**j * v for j in range(d))).T
B = (q*sp.eye(d)).row_join(-M).col_join(sp.zeros(d).row_join(sp.eye(d)))
native_rows = B.T
print(json.dumps(dict(stage='native_basis_ready', seed=seed, d=d, q=str(q))), flush=True)
started = time.perf_counter()
if args.backend == 'flint':
    from flint import fmpz_mat
    integer_rows = fmpz_mat([[int(v) for v in native_rows.row(i)] for i in range(2*d)])
    flint_reduced, flint_transform = integer_rows.lll(transform=True)
    assert abs(int(flint_transform.det())) == 1
    assert flint_transform * integer_rows == flint_reduced
    reduced = sp.Matrix([[int(flint_reduced[i,j]) for j in range(2*d)] for i in range(2*d)])
    transform = sp.Matrix([[int(flint_transform[i,j]) for j in range(2*d)] for i in range(2*d)])
else:
    reduced, transform = native_rows.lll_transform()
elapsed = time.perf_counter() - started
print(json.dumps(dict(stage='lll_complete', elapsed_seconds=elapsed)), flush=True)
assert reduced == transform * native_rows
if args.backend == 'sympy':
    assert abs(int(transform.det())) == 1
F = sp.eye(d).row_join(M)
assert F * reduced.T % q == sp.zeros(d, 2*d)

# Bareiss pivots are exact leading Gram determinants. Their ratios are
# the squared GS lengths; ceiling each ratio avoids huge rational sums.
G = reduced * reduced.T
A = [[int(G[i, j]) for j in range(2*d)] for i in range(2*d)]
previous = 1
pivots = []
gs_ceiling = []
for k in range(2*d):
    pivot = A[k][k]
    assert pivot > 0
    pivots.append(pivot)
    gs_ceiling.append((pivot + previous - 1)//previous)
    for i in range(k+1, 2*d):
        for j in range(i, 2*d):
            numerator = pivot * A[i][j] - A[i][k] * A[k][j]
            quotient, remainder = divmod(numerator, previous)
            assert remainder == 0
            A[i][j] = quotient
            A[j][i] = quotient
    previous = pivot
assert pivots[-1] == q**(2*d)
Q = sum(gs_ceiling)
lane_checks = []
for lane in parameter['lanes']:
    Rs = lane['prior_radius']
    E = int(lane['total_training_error_norm_bound'])
    t = q//(2*Rs+1)
    accepted = E*E*Q < t*t
    lane_checks.append(dict(lane=lane['lane'], prior_radius=Rs, error_norm=str(E),
                            chosen_label=str(t), babai_all_cosets_certificate=accepted,
                            squared_margin_numerator=str(t*t),
                            squared_margin_denominator=str(E*E*Q)))

payload = dict(status='LOCAL_DERIVATION_REVIEW_PENDING', scope='one_finite_native_kernel_all_cosets',
               asymptotic_attack_proved=False, quantum_algorithm=False,
               seed=seed, d=d, q=str(q), construction_backend=args.backend,
               basis_lift='centered', native_ratio=[str(v) for v in m],
               reduced_row_basis=[[str(int(v)) for v in reduced.row(i)] for i in range(2*d)],
               unimodular_transform=[[str(int(v)) for v in transform.row(i)] for i in range(2*d)],
               gs_squared_integer_upper=[str(v) for v in gs_ceiling],
               gs_squared_sum_upper=str(Q), elapsed_lll_seconds=elapsed,
               lanes=lane_checks)
print(json.dumps(dict(stage='certificate_complete', gs_squared_sum_upper=str(Q), lanes=lane_checks)), flush=True)
if args.save:
    destination = Path(__file__).with_name('native_rlwe_babai_profile_d64.json')
    destination.write_text(json.dumps(payload, indent=2)+'\n')
    print(json.dumps(dict(saved_certificate=str(destination))), flush=True)
