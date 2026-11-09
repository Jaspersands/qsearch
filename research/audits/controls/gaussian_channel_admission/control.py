"""Exact supplied-component classical control; no learner/circuit execution.

Algebra interpreter: /opt/anaconda3/envs/qsearch-cas/bin/python
"""
import json
from itertools import combinations
from pathlib import Path
from sage.all import CyclotomicField, QQ, diagonal_matrix, identity_matrix, matrix, vector

F = CyclotomicField(4)
ii = F.gen()
I2, I4 = identity_matrix(F, 2), identity_matrix(F, 4)
X = matrix(F, [[0, 1], [1, 0]])
Y = matrix(F, [[0, -ii], [ii, 0]])
Z = diagonal_matrix(F, [1, -1])


def kron(*args):
    result = matrix(F, [[1]])
    for a in args:
        result = result.tensor_product(a.dense_matrix())
    return result


def trace_left(a, left, right):
    return matrix(F, right, right, lambda i, j: sum(a[k*right+i, k*right+j] for k in range(left)))


def trace_right(a, left, right):
    return matrix(F, left, left, lambda i, j: sum(a[i*right+k, j*right+k] for k in range(right)))


def expectation(state, a):
    return sum(x.conjugate()*y for x, y in zip(state, a*state))


majoranas = []
for mode in range(4):
    majoranas.extend(kron(*([Z]*mode + [p] + [I2]*(3-mode))) for p in (X, -Y))
omega, bell = vector(F, 16), vector(F, 16)
for x in range(4):
    bell[4*x+x] = QQ(1)/2
    omega[4*x+x] = (-1)**(int(x).bit_count()//2) * QQ(1)/2
gauge = kron(diagonal_matrix(F, [1, 1, 1, -1]), I4)
assert omega == gauge*bell
omega_density = omega.column()*omega.conjugate().row()
assert trace_right(omega_density, 4, 4) == I4/4


def wick_check(state):
    pair = matrix(F, 8, 8, lambda i, j: expectation(state, majoranas[i]*majoranas[j]) if i < j else 0)
    pair -= pair.transpose()
    checked, mismatches = {}, []
    for degree in (2, 4, 6, 8):
        checked[str(degree)] = 0
        for subset in combinations(range(8), degree):
            word = identity_matrix(F, 16)
            for k in subset:
                word *= majoranas[k]
            actual = expectation(state, word)
            predicted = pair.matrix_from_rows_and_columns(subset, subset).pfaffian()
            checked[str(degree)] += 1
            if actual != predicted:
                mismatches.append({'indices_zero_based': list(subset), 'actual': str(actual), 'wick': str(predicted)})
    return checked, mismatches


moment_counts, omega_mismatches = wick_check(omega)
_, bell_mismatches = wick_check(bell)
assert not omega_mismatches

# Psi is the identity from a dimension-4 core to R_2 tensor O_2.
r, D, h = 4, 2, 2
maxent = vector(F, [1 if a == b else 0 for a in range(4) for b in range(4)])
Jpsi = maxent.column()*maxent.row()/4
assert trace_right(Jpsi, 4, 4) == I4/4
C = r*D*Jpsi  # P,R are the joint ordinary input; O is output.
JT = trace_right(Jpsi, 8, 2)
effect = trace_right(C, 8, 2).transpose()
assert effect == (r*h*JT).transpose()
eigenvalues = effect.eigenvalues()
assert all(QQ(value) >= 0 for value in eigenvalues)
effect_norm = max(QQ(value) for value in eigenvalues)
assert effect_norm <= r*h


def processor(a):
    return matrix(F, 2, 2, lambda o, p: sum(a[i, j]*C[2*i+o, 2*j+p] for i in range(8) for j in range(8)))


vI, vS = vector(F, [1, 0, 0, 1]), vector(F, [1, 0, 0, ii])
tau = (vI.column()*vI.conjugate().row()/3 + 2*vS.column()*vS.conjugate().row()/3)/2
S = diagonal_matrix(F, [1, ii])
assert tau.trace() == 1 and trace_right(tau, 2, 2) == I2/2
assert kron(Z, Z)*tau == tau*kron(Z, Z)
assert all(QQ(tau.matrix_from_rows_and_columns(s, s).det()) >= 0
           for k in range(1, 5) for s in combinations(range(4), k))
linked = r*trace_left(kron(tau.transpose(), I4)*Jpsi, 4, 4)
wrong_linked = r*trace_left(kron(tau, I4)*Jpsi, 4, 4)
assert linked == tau and wrong_linked == tau.transpose() and wrong_linked != tau
unit_checks = 0
for i in range(2):
    for j in range(2):
        unit = matrix(F, 2, 2)
        unit[i, j] = 1
        out = processor(kron(tau, unit))
        assert out == unit/3 + 2*S*unit*S.conjugate_transpose()/3
        assert out.trace() == (1 if i == j else 0)
        unit_checks += 1
bad_tau = diagonal_matrix(F, [1, 0, 0, 0])
assert kron(Z, Z)*bad_tau == bad_tau*kron(Z, Z)
bad_input = diagonal_matrix(F, [1, 0])
bad_output = processor(kron(bad_tau, bad_input))
assert bad_output.trace() == 2
result = {
    'status': 'PASS', 'scope': 'Exact supplied-component classical Wick/CP-link control only.',
    'omega': {'moment_counts': moment_counts, 'wick_mismatches': omega_mismatches,
              'reference_marginal': 'I4/4', 'reference_only_CZ_relation': True},
    'ordinary_bell': {'wick_mismatch_count': len(bell_mismatches),
                      'first_wick_mismatch': bell_mismatches[0] if bell_mismatches else None},
    'cp_link': {'r': r, 'D': D, 'h': h, 'unnormalized_C_factor': r*D,
                'effect_full_transpose_identity': True, 'effect_PSD': True,
                'effect_eigenvalues': [str(v) for v in eigenvalues], 'effect_norm': str(effect_norm),
                'norm_bound_rh': r*h, 'program_transpose_link': True,
                'omitted_program_transpose_fails': True, 'feasible_even_program': True,
                'matrix_units_matching_TP_target': unit_checks,
                'nonTP_even_program_output_trace_on_E00': str(bad_output.trace())},
    'claim_gates': {'full_algorithm_execution': False, 'quantum_execution': False,
                    'novelty': False, 'speedup': False},
}
Path(__file__).with_name('result.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
