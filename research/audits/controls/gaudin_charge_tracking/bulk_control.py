"""Fixed finite bulk-sector attack; numerical nonfalsification is not proof.

Sage algebra: /opt/anaconda3/envs/qsearch-cas/bin/python.
The previously frozen M=1 control is neither imported nor rerun.
"""
import json
from itertools import combinations
from pathlib import Path
import numpy as np
from sage.all import QQ, identity_matrix, matrix


def exact_charges(sites, coupling, excitation):
    N = len(sites)
    states = list(combinations(range(N), excitation))
    locations = {state: j for j, state in enumerate(states)}
    size, charges = len(states), []
    for i in range(N):
        Q = matrix(QQ, size, size)
        for column, state in enumerate(states):
            occupied = set(state)
            Q[column, column] += int(i in occupied)
            for j in range(N):
                if j == i or ((i in occupied) == (j in occupied)):
                    continue
                coefficient = coupling/(2*(sites[i]-sites[j]))
                target = tuple(sorted(occupied.symmetric_difference({i, j})))
                Q[locations[target], column] += coefficient
                Q[column, column] -= coefficient
        assert Q == Q.transpose()
        charges.append(Q)
    I = identity_matrix(QQ, size)
    assert sum(charges, matrix(QQ, size, size)) == excitation*I
    for i, Q in enumerate(charges):
        assert all(Q*R == R*Q for R in charges)
        assert Q*Q == Q-coupling/2*sum(
            ((Q-charges[j])/(sites[i]-sites[j]) for j in range(N) if j != i), matrix(QQ, size, size))
    return states, charges


cases = []
for N, excitation, irregular in [
    (4, 2, [QQ(0), QQ(1)/10, QQ(3)/2, QQ(4)]),
    (6, 3, [QQ(0), QQ(1)/10, QQ(3)/2, QQ(7)/3, QQ(4), QQ(13)/2]),
]:
    patterns = [('equally_spaced', list(map(QQ, range(N)))),
                ('fixed_irregular_cluster', irregular)]
    for pattern, sites in patterns:
        for coupling in [QQ(1)/10, QQ(1), QQ(10)]:
            states, exact = exact_charges(sites, coupling, excitation)
            floating = [np.array([[float(a) for a in row] for row in Q.rows()]) for Q in exact]
            for combination_weights in [
                [3**i for i in range(N)], [1, 7, 23, 61, 127, 251][:N],
                [2, 11, 37, 83, 173, 359][:N],
            ]:
                combination = sum(weight*Q for weight, Q in zip(combination_weights, floating))
                eigenvalues, eigenvectors = np.linalg.eigh(combination)
                tuples = np.array([np.diag(eigenvectors.T@Q@eigenvectors) for Q in floating]).T
                residual = max(float(np.max(np.linalg.norm(Q@eigenvectors-eigenvectors*tuples[:, i], axis=0)))
                               for i, Q in enumerate(floating))
                if residual < 1e-9:
                    break
            assert residual < 1e-9, (N, pattern, str(coupling), residual)
            differences = tuples[:, None, :]-tuples[None, :, :]
            squared_gaps = np.einsum('ijk,ijk->ij', differences, differences)
            np.fill_diagonal(squared_gaps, np.inf)
            row, column = map(int, np.unravel_index(np.argmin(squared_gaps), squared_gaps.shape))
            minimum = float(squared_gaps[row, column])
            cases.append({'N': N, 'M': excitation, 'sector_dimension': len(states),
                'site_pattern': pattern, 'sites': list(map(str, sites)), 'g': str(coupling),
                'exact_commutator_quadratic_sum_checks': True,
                'diagonalization_combination_weights': combination_weights,
                'numeric_max_joint_eigenvector_residual': residual,
                'numeric_min_combination_eigenvalue_spacing': float(np.min(np.diff(eigenvalues))),
                'numeric_min_same_sector_squared_gap': minimum, 'primary_threshold_1_over_N': str(QQ(1)/N),
                'minimum_pair_indices': [row, column],
                'minimum_pair_charge_tuples': [tuples[row].tolist(), tuples[column].tolist()],
                'numerical_primary_violation_candidate': minimum < 1.0/N-1e-7})

violations = [case for case in cases if case['numerical_primary_violation_candidate']]
minimum_case = min(cases, key=lambda case: case['numeric_min_same_sector_squared_gap'])
result = {
    'status': 'NUMERICAL_CANDIDATE_REQUIRES_EXACT_CERTIFICATION' if violations else 'FINITE_NONFALSIFICATION_ONLY',
    'scope': 'Exactly 12 fixed bulk cases, exact matrix identities and numerical joint spectra only.',
    'cases': cases, 'numerical_primary_violation_count': len(violations),
    'minimum_observed_squared_gap': minimum_case['numeric_min_same_sector_squared_gap'],
    'maximum_numeric_joint_residual': max(case['numeric_max_joint_eigenvector_residual'] for case in cases),
    'no_numerical_gap_is_an_all_parameter_lower_bound': True,
    'claim_gates': {'primary_conjecture_proved': False, 'primary_conjecture_exactly_refuted': False,
        'scaling_claim': False, 'general_complexity_conclusion': False,
        'quantum_execution': False, 'novelty': False, 'speedup': False},
}
Path(__file__).with_name('bulk_result.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'status': result['status'], 'case_count': len(cases),
    'minimum_observed_case': minimum_case,
    'maximum_numeric_joint_residual': result['maximum_numeric_joint_residual'],
    'numerical_primary_violation_count': len(violations)}, indent=2))
