"""Exact finite Stoll-kernel and precision falsifiers; no local algorithm.

Sage algebra: /opt/anaconda3/envs/qsearch-cas/bin/python.
"""
import json
from pathlib import Path
from sage.all import PolynomialRing, QQ, ZZ, diagonal_matrix, matrix, vector

R = PolynomialRing(QQ, 'x')
x = R.gen()
kernel_cases = []
for genus in (2, 3, 4):
    f = x**(2*genus+1)+x+1
    a, b = x**(2*genus-1)-QQ(1)/4, -1-x/2
    u0, v0, w0 = R(1), b, x
    s = (v0*x.inverse_mod(f)) % f
    assert f.gcd(f.derivative()) == 1 and a.gcd(a.derivative()) == 1
    assert (s*s+a) % f == 0 and (f-b*b) % a == 0
    assert f-b*b == a*x*x

    def unpack(coefficients, w_bound):
        u = R(list(coefficients[:genus]))
        v = R(list(coefficients[genus:3*genus]))
        w = R(list(coefficients[3*genus:3*genus+w_bound+1]))
        return u, v, w

    def constraints(coefficients, w_bound):
        u, v, w = unpack(coefficients, w_bound)
        first, second = (v-w*s) % f, (v-u*b) % a
        return vector(QQ, [first[j] for j in range(2*genus+1)]
                      + [second[j] for j in range(2*genus-1)])

    dimensions = []
    for bound in range(genus+1):
        variables = 3*genus+bound+1
        columns = []
        for j in range(variables):
            basis = vector(QQ, variables)
            basis[j] = 1
            columns.append(constraints(basis, bound))
        system = matrix(QQ, columns).transpose()
        kernel = system.right_kernel()
        assert kernel.dimension() == bound
        multiples = []
        for exponent in range(bound):
            u, v, w = [x**exponent*entry for entry in (u0, v0, w0)]
            coefficients = vector(QQ, [u[j] for j in range(genus)]
                                  + [v[j] for j in range(2*genus)]
                                  + [w[j] for j in range(bound+1)])
            assert system*coefficients == 0
            multiples.append(coefficients)
        explicit_span = matrix(QQ, bound, variables, [c for row in multiples for c in row]).row_space()
        assert explicit_span == kernel
        dimensions.append(int(kernel.dimension()))
    assert dimensions[-1] == genus
    kernel_cases.append({'g': genus, 'f': str(f), 'a': str(a), 'b': str(b), 's': str(s),
        'degree_bounds': {'u_max': genus-1, 'v_max': 2*genus-1, 'w_max': genus},
        'full_kernel_dimension': dimensions[-1],
        'w_truncation_bounds': list(range(genus+1)), 'truncated_kernel_dimensions': dimensions,
        'all_kernels_equal_explicit_polynomial_multiple_span': True,
        'divisor_norm_identity_f_minus_b_squared_equals_a_x_squared': True,
        'independent_group_algorithm_executed': False})

lam, input_precision = 3, 9
A = matrix(QQ, [[2**lam, 0]])
Aprime = matrix(QQ, [[2**lam, 2**input_precision]])
kernel_vector = vector(QQ, [0, 1])
kernel_vector_prime = vector(QQ, [-2**(input_precision-lam), 1])
assert A*kernel_vector == 0 and Aprime*kernel_vector_prime == 0
kernel_change_valuation = int((kernel_vector_prime[0]-kernel_vector[0]).valuation(2))
assert kernel_change_valuation == 6 and kernel_change_valuation < 7

v = vector(QQ, [1, 2**lam])
vprime = vector(QQ, [1, 2**lam+2**input_precision])
normalized, normalized_prime = v/v[1], vprime/vprime[1]
normalization_change_valuation = int((normalized[0]-normalized_prime[0]).valuation(2))
assert (vprime[1]-v[1]).valuation(2) == input_precision
assert normalization_change_valuation == input_precision-2*lam == 3

B = diagonal_matrix(ZZ, [0, 1])
primitive = vector(ZZ, [1, 2**lam])
image = B*primitive
smith = [int(d) for d in B.elementary_divisors() if d]
assert smith == [1] and primitive[0] == 1
assert image == vector(ZZ, [0, 8]) and image[1].valuation(2) == 3
result = {
    'status': 'PASS', 'scope': 'Finite exact classical kernel-shape checks and precision counterexamples only.',
    'Stoll_nonminimal_kernel_cases': kernel_cases,
    'precision_falsifiers': {
        'row_kernel': {'A': [[8, 0]], 'Aprime': [[8, 512]], 'input_difference_v2': 9,
            'nonzero_Smith_v2': 3, 'primitive_kernel_vectors': [[0, 1], [-64, 1]],
            'kernel_vector_difference_v2': kernel_change_valuation,
            'claimed_output_precision_7_refuted': True},
        'normalization': {'vectors': [[1, 8], [1, 520]], 'chosen_pivot_v2': 3,
            'input_difference_v2': 9, 'first_normalized_coordinates': ['1/8', '1/520'],
            'normalized_coordinate_difference_v2': normalization_change_valuation,
            'two_lambda_absolute_loss': 6, 'one_lambda_absolute_loss_refuted': True},
        'rank_deficient_primitive_vector': {'B': [[0, 0], [0, 1]], 'nonzero_Smith_divisors': smith,
            'primitive_input': [1, 8], 'output': [0, 8], 'output_common_v2': 3,
            'unguarded_unit_Smith_implies_primitive_output_refuted': True}},
    'claim_gates': {'all_g_theorem_from_finite_control': False, 'full_BIT_algorithm': False,
                    'full_local_algorithm': False, 'quantum_execution': False},
}
Path(__file__).with_name('result.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'status': result['status'],
    'kernel_dimensions': [{'g': a['g'], 'truncated': a['truncated_kernel_dimensions']} for a in kernel_cases],
    'precision_falsifiers': result['precision_falsifiers']}, indent=2))
