"""Exact classical Bethe-prefix falsifier; no preparation/quantum algorithm.

Sage algebra: /opt/anaconda3/envs/qsearch-cas/bin/python.
"""
import json
from itertools import combinations
from pathlib import Path
from sage.all import PolynomialRing, QQ, matrix, vector

eps = [QQ(1)/2, QQ(2), QQ(1)/5, QQ(7)/5]
roots = [QQ(-1), QQ(1)]
gamma, coupling = -QQ(5)/4, QQ(4)/5
subsets = list(combinations(range(4), 2))


def cauchy(subset):
    return matrix(QQ, [[1/(root-eps[i]) for i in subset] for root in roots])


def permanent_two(C):
    return C[0, 0]*C[1, 1]+C[0, 1]*C[1, 0]


amplitudes = []
for subset in subsets:
    C = cauchy(subset)
    amplitude = permanent_two(C)
    entrywise_squared = matrix(QQ, [[a*a for a in row] for row in C.rows()])
    assert C.det() != 0
    assert amplitude == entrywise_squared.det()/C.det()
    amplitudes.append(amplitude)
assert amplitudes[0] == 0
psi = vector(QQ, amplitudes)


def bethe_residuals(levels):
    return [sum(1/(root-eps[i]) for i in levels)
            - 2*sum(1/(root-other) for j, other in enumerate(roots) if j != a)-gamma
            for a, root in enumerate(roots)]


assert bethe_residuals(range(4)) == [0, 0]
# Independent hard-core pairing Hamiltonian, including i=j diagonal terms.
H = matrix(QQ, 6, 6)
positions = {subset: j for j, subset in enumerate(subsets)}
for column, occupied in enumerate(subsets):
    H[column, column] += sum(eps[j] for j in occupied)
    for lowered in occupied:
        after_lowering = set(occupied)-{lowered}
        for raised in range(4):
            if raised not in after_lowering:
                target = tuple(sorted(after_lowering | {raised}))
                H[positions[target], column] -= coupling
assert H == H.transpose() and H*psi == sum(roots)*psi


def gaudin(levels):
    return matrix(QQ, 2, 2, lambda a, b:
        sum(1/(roots[a]-eps[i])**2 for i in levels)
        - 2*sum(1/(roots[a]-roots[j])**2 for j in range(2) if j != a)
        if a == b else 2/(roots[a]-roots[b])**2)


full_norm = psi.dot_product(psi)
true_prefix_norm = sum(amplitude**2 for subset, amplitude in zip(subsets, amplitudes) if 0 not in subset)
full_gaudin = gaudin(range(4)).det()
deleted_gaudin = gaudin(range(1, 4)).det()
assert full_norm == full_gaudin == QQ(25625)/2304
assert true_prefix_norm == QQ(9625)/2304
assert true_prefix_norm/full_norm == QQ(77)/205
assert deleted_gaudin == QQ(8601)/2304
assert true_prefix_norm-deleted_gaudin == QQ(4)/9
deleted_residuals = bethe_residuals(range(1, 4))
assert deleted_residuals == [QQ(2)/3, QQ(-2)]

# Universal one-level Cauchy relation underlying the general M=2 discrepancy.
S = PolynomialRing(QQ, names=('v1', 'v2', 'e'))
fraction = S.fraction_field()
v1, v2, e = map(fraction, S.gens())
p, q = 1/(v1-e), 1/(v2-e)
assert (p-q)**2 == (v2-v1)**2*p*p*q*q
identity_checks = []
for levels, actual_norm, determinant in [
    (range(4), full_norm, full_gaudin),
    (range(1, 4), true_prefix_norm, deleted_gaudin),
]:
    d = roots[1]-roots[0]
    products = [1/((roots[0]-eps[i])*(roots[1]-eps[i])) for i in levels]
    K = sum(products)
    A = sum(1/(roots[0]-eps[i])**2 for i in levels)
    B = sum(1/(roots[1]-eps[i])**2 for i in levels)
    D = sum(a*a for a in products)
    assert A+B == 2*K+d*d*D
    assert actual_norm == A*B+K*K-2*D
    assert actual_norm-determinant == K*(K+4/(d*d))
    identity_checks.append({'levels': list(levels), 'K': str(K),
                            'norm_minus_Gaudin': str(actual_norm-determinant)})

result = {
    'status': 'PASS', 'scope': 'Falsifies only deleting a site from the on-shell Gaudin norm formula while keeping roots fixed.',
    'epsilon': [str(a) for a in eps], 'roots': [str(a) for a in roots],
    'gamma': str(gamma), 'coupling_G': str(coupling),
    'subsets': [list(a) for a in subsets], 'amplitudes': [str(a) for a in amplitudes],
    'Borchardt_checks': 6, 'zero_amplitude_included': True,
    'Bethe_residuals_full': ['0', '0'], 'pairing_H_eigenvalue': str(sum(roots)),
    'pairing_H_eigenvector_check': True, 'full_norm_and_Gaudin': str(full_norm),
    'site_0_empty': {'true_unnormalized_norm': str(true_prefix_norm),
        'probability': str(true_prefix_norm/full_norm), 'deleted_site_Gaudin': str(deleted_gaudin),
        'exact_discrepancy': str(true_prefix_norm-deleted_gaudin),
        'deleted_site_Bethe_residuals': [str(a) for a in deleted_residuals]},
    'M2_identity': {'formula': 'true_norm - Gaudin_det = K*(K+4/d^2)',
        'universal_one_level_Cauchy_relation_verified_symbolically': True,
        'derivation': 'true_norm=A*B+K^2-2D; Gaudin_det=A*B-2(A+B)/d^2; A+B=2K+d^2*D.',
        'exact_full_and_prefix_checks': identity_checks},
    'claim_gates': {'general_Bethe_algorithm_no_go': False, 'hardness': False,
        'poly_N_algorithm_inference': False, 'full_state_preparation': False,
        'quantum_execution': False, 'novelty': False, 'speedup': False},
}
Path(__file__).with_name('result.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'status': 'PASS', 'full_norm': str(full_norm),
    'site_0_empty': result['site_0_empty'], 'M2_identity_checks': identity_checks}, indent=2))
