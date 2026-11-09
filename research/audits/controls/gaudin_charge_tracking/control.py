"""Exact algebraic finite counterexample to same-excitation charge gap >=2.

Sage algebra: /opt/anaconda3/envs/qsearch-cas/bin/python.
This freezes the first rational fixture found; no parameter sweep is run here.
"""
import json
from itertools import combinations
from pathlib import Path
from sage.all import AA, QQ, RealField, RealIntervalField, identity_matrix, matrix, vector

N = 3
sites = [QQ(0), QQ(1), QQ(2)]
coupling = QQ(1)/10
weights = [1, 3, 9]
RR, RI = RealField(256), RealIntervalField(256)


def charges(excitation):
    states = list(combinations(range(N), excitation))
    positions = {state: j for j, state in enumerate(states)}
    size = len(states)
    answer = []
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
                Q[positions[target], column] += coefficient
                Q[column, column] -= coefficient
        answer.append(Q)
    I = identity_matrix(QQ, size)
    assert sum(answer, matrix(QQ, size, size)) == excitation*I
    for i, Q in enumerate(answer):
        for j in range(N):
            assert Q*answer[j] == answer[j]*Q
        assert Q*Q == Q-coupling/2*sum(
            ((Q-answer[j])/(sites[i]-sites[j]) for j in range(N) if j != i), matrix(QQ, size, size))
    return states, answer


def enclosure(a):
    interval = a.interval(RI)
    lower, upper = interval.lower().exact_rational(), interval.upper().exact_rational()
    assert AA(lower) <= a <= AA(upper)
    return {'decimal_256_bits': str(interval),
            'rational_lower': str(lower),
            'rational_upper': str(upper)}


sectors = {}
for excitation in range(N+1):
    states, Q = charges(excitation)
    size = len(states)
    H = sum((weight*charge for weight, charge in zip(weights, Q)), matrix(QQ, size, size))
    roots = sorted(H.charpoly().roots(AA, multiplicities=False))
    assert len(roots) == size
    eigenpairs = []
    for root in roots:
        kernel = (H.change_ring(AA)-root*identity_matrix(AA, size)).right_kernel()
        assert kernel.dimension() == 1
        v = kernel.basis()[0]
        norm_squared = v.dot_product(v)
        tuple_q = [(v.dot_product(charge.change_ring(AA)*v))/norm_squared for charge in Q]
        assert all(charge.change_ring(AA)*v == q*v for charge, q in zip(Q, tuple_q))
        assert sum(tuple_q) == excitation
        normalized = v/norm_squared.sqrt()
        numerical_vector = vector(RR, list(normalized))
        numerical_residual = max(abs(a) for charge, q in zip(Q, tuple_q)
                                 for a in charge.change_ring(RR)*numerical_vector-RR(q)*numerical_vector)
        assert numerical_residual < RR(2)**(-230)
        eigenpairs.append({'q': tuple_q, 'vector': normalized, 'combo_root': root,
                           'numerical_residual': numerical_residual})
    sectors[excitation] = {'states': states, 'charges': Q, 'combo': H, 'pairs': eigenpairs}

witness = sectors[1]
left, right = witness['pairs'][1], witness['pairs'][2]
squared_gap = sum((a-b)**2 for a, b in zip(left['q'], right['q']))
assert AA(QQ(1879)/1000) < squared_gap < AA(QQ(1880)/1000) < 2
assert squared_gap > QQ(1)/N
all_same_sector_gaps = [sum((a-b)**2 for a, b in zip(left['q'], right['q']))
    for sector in sectors.values() for left, right in combinations(sector['pairs'], 2)]
minimum_same_sector = min(all_same_sector_gaps)
assert minimum_same_sector >= QQ(1)/N

result = {
    'status': 'EXACT_COUNTEREXAMPLE_SAME_EXCITATION_BOUND_2',
    'scope': 'One finite rational Gaudin charge fixture, certified with exact real algebraic arithmetic.',
    'parameters': {'N': N, 'sites': [str(e) for e in sites], 'g': str(coupling),
                   'excitation': 1, 'generic_combination_weights': weights,
                   'witness_sector_basis': [list(state) for state in witness['states']]},
    'exact_checks': {'all_sector_pairwise_commutators_zero': True,
        'all_sector_quadratic_charge_relations': True, 'sum_charges_equals_excitation': True,
        'joint_eigenvector_residuals_exactly_zero': True,
        'all_8_joint_eigenvectors_covered': True},
    'witness': {'combination_characteristic_polynomial': str(witness['combo'].charpoly()),
        'combination_root_indices_in_increasing_order': [1, 2],
        'left_combo_root': enclosure(left['combo_root']), 'right_combo_root': enclosure(right['combo_root']),
        'left_charge_tuple': [enclosure(q) for q in left['q']],
        'right_charge_tuple': [enclosure(q) for q in right['q']],
        'left_normalized_eigenvector': [enclosure(a) for a in left['vector']],
        'right_normalized_eigenvector': [enclosure(a) for a in right['vector']],
        'squared_joint_gap': enclosure(squared_gap),
        'squared_gap_minimal_polynomial': str(squared_gap.minpoly()),
        'exact_rational_gap_bracket': ['1879/1000', '47/25'],
        'same_excitation_bound_2_refuted': True,
        'rounded_256_bit_eigenvector_max_residual': str(max(left['numerical_residual'], right['numerical_residual']))},
    'weaker_bound': {'one_over_N': str(QQ(1)/N), 'counterexample_found': False,
        'fixture_minimum_same_sector_squared_gap': enclosure(minimum_same_sector),
        'cross_excitation_deduction': 'sum_i q_i=m implies squared gap >=(m-mprime)^2/N >=1/N for distinct excitations by Cauchy-Schwarz.',
        'all_N_same_sector_1_over_N_bound_proved': False},
    'exploratory_scope': 'NumPy exploration stopped at the first violation, N3 equally-spaced g=1/10; no N4/N6 or irregular/clustered sweep after this counterexample.',
    'claim_gates': {'general_complexity_conclusion': False, 'all_N_gap_lower_bound': False,
        'general_Gaudin_algorithm_no_go': False, 'quantum_execution': False,
        'novelty': False, 'speedup': False},
}
Path(__file__).with_name('result.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'status': result['status'], 'parameters': result['parameters'],
    'squared_gap': enclosure(squared_gap), 'minimal_polynomial': str(squared_gap.minpoly()),
    'rounded_256_bit_residual': result['witness']['rounded_256_bit_eigenvector_max_residual'],
    'weaker_1_over_N_bound_refuted': False}, indent=2))
