"""Exact classical weight/finite-point-count control, not a P2 algorithm.

Algebra interpreter: /opt/anaconda3/envs/qsearch-cas/bin/python.
"""
import json
from itertools import combinations
from pathlib import Path
from sage.all import GF, ProjectiveSpace, QQ, binomial


def wedge_square(weights):
    answer = {}
    for weight, multiplicity in weights.items():
        answer[2*weight] = answer.get(2*weight, 0) + multiplicity*(multiplicity-1)//2
    for (a, ma), (b, mb) in combinations(weights.items(), 2):
        answer[a+b] = answer.get(a+b, 0) + ma*mb
    return {weight: count for weight, count in sorted(answer.items()) if count}


wedge = wedge_square({-1: 4, 0: 44, 1: 4})
assert wedge == {-2: 6, -1: 176, 0: 962, 1: 176, 2: 6}
assert sum(wedge.values()) == 1326
k3_wedge = wedge_square({-1: 1, 0: 19, 1: 1})
assert -2 not in k3_wedge and 2 not in k3_wedge
inactive = [sum(int(binomial(22, j)) for j in range(parity, 23, 2)) for parity in (0, 1)]
assert inactive == [2**21, 2**21]
half_spins = {}
for parity in (0, 1):
    multiplicities = {j-2: int(binomial(4, j))*inactive[(parity-j) % 2] for j in range(5)}
    assert sum(multiplicities.values()) == 2**25
    assert max(multiplicities)-min(multiplicities) == 4
    half_spins[str(parity)] = multiplicities
slopes = [QQ(j-2) + QQ(1)/2 for j in range(5)]
assert slopes[0] == -QQ(3)/2 and slopes[-1] == QQ(5)/2

field = GF(7)
ambient = ProjectiveSpace(3, field, names='x')
S = ambient.coordinate_ring()
x0, x1, x2, x3 = S.gens()
fermat = x0**5 + x1**5 + x2**5 + x3**5
original = fermat + x0*x1*x2*x3*(x0+x1)


def gradient_charts(polynomial):
    derivatives = [polynomial.derivative(v) for v in S.gens()]
    certificates = []
    for v in S.gens():
        gb = S.ideal(derivatives + [v-1]).groebner_basis()
        certificates.append(S(1) in gb)
    return certificates


original_charts = gradient_charts(original)
selected = original
change = None
if not all(original_charts):
    # One bounded fallback: change only the x0*x1^2*x2*x3 coefficient 1 -> 2.
    selected = original + x0*x1**2*x2*x3
    change = 'x0*x1^2*x2*x3 coefficient changed from 1 to 2 after original singularity.'
    selected_charts = gradient_charts(selected)
else:
    selected_charts = original_charts
smooth = all(selected_charts)
scheme = ambient.subscheme([selected])
points = scheme.rational_points()
count = len(points)
# Lefschetz: #X = 1 + q^2 + Tr(F|H2), while [T]det(1-TF) = -Tr(F|H2).
# Correction: the earlier artifact incorrectly called the negative trace a trace.
c1_coefficient = 1 + 7**2 - count
frobenius_trace = count - 1 - 7**2
assert c1_coefficient == -frobenius_trace

# Exact numerical formula normalizations only; not geometric execution evidence.
degree = 5
euler = degree*(degree**2 - 4*degree + 6)
genus = 1 + (9*degree + 3*degree)//2
base_degree = 9*degree
nodes = euler + base_degree - 2*(2-2*genus)
assert (genus, base_degree, nodes, euler-2) == (31, 45, 220, 53)

result = {
    'status': 'PASS' if smooth else 'FAIL_SECOND_QUINTIC_SINGULAR',
    'scope': 'Classical exact weight multiplicities and one finite native point count only.',
    'wedge_square': {'quintic_multiplicities': wedge, 'dimension': sum(wedge.values()),
                     'K3_control_multiplicities': k3_wedge, 'K3_has_weight_plus_or_minus_2': False},
    'D26_half_spin': {
        'active_coordinates': 4, 'inactive_coordinates': 22,
        'inactive_parity_counts': inactive, 'multiplicities_by_half_parity': half_spins,
        'dimension_each': 2**25, 'weight_width': 4,
        'central_shift_can_make_width_1': False, 'exponential_state_enumeration': False,
        'normalized_formal_slopes': [str(a) for a in slopes],
        'formal_slope_scope': 'Conditional ordinary formal shape only; no generic Newton or actual quintic slope claim.',
        'known_Deligne_Schnell_Hodge_obstruction_claimed_new': False,
    },
    'native_F7_baseline': {
        'original_polynomial': str(original), 'original_gradient_charts_unit_ideal': original_charts,
        'original_smooth': all(original_charts), 'fallback_change': change,
        'selected_polynomial': str(selected), 'selected_gradient_charts_unit_ideal': selected_charts,
        'selected_smooth_over_algebraic_closure': smooth,
        'point_count_method': 'Sage projective subscheme rational_points over F7',
        'F7_points': count, 'H2_Frobenius_trace': frobenius_trace,
        'P2_coefficient_c1_of_T': c1_coefficient,
        'trace_formula': '#X = 1 + q^2 + Tr(F|H2)',
        'coefficient_formula': '[T]det(1-T F|H2) = 1 + q^2 - #X = -Tr(F|H2)',
        'correction_record': 'Earlier labels reversed the trace/coefficient signs; corrected to trace +8 and P2 coefficient -8 for #X(F7)=58.',
        'full_P2_computed': False,
    },
    'formula_normalizations_only': {'genus': genus, 'base_degree': base_degree,
                                  'nodes': nodes, 'b2': euler-2},
    'claim_gates': {'algorithm_implementation': False, 'novelty': False,
                    'speedup': False, 'quantum_execution': False},
}
Path(__file__).with_name('result.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
