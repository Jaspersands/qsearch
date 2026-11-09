"""One exact classical halving/formal-log control; not a local-image solver.

Sage algebra: /opt/anaconda3/envs/qsearch-cas/bin/python.
"""
import json
from pathlib import Path
from sage.all import PolynomialRing, QQ, binomial, matrix, prod, vector

R = PolynomialRing(QQ, 'x')
x = R.gen()
roots = [QQ(0), QQ(-1), QQ(-4), QQ(-9), QQ(-16)]
f = prod(x-root for root in roots)
f1 = f//x
s_values = list(map(QQ, [24, 1, 2, 3, 4]))
s = R.lagrange_polynomial(list(zip(roots, s_values)))
assert (s*s-(f1-x)) % f == 0


def constraints(coefficients, degree):
    u, v = R(coefficients[0]), coefficients[1]+coefficients[2]*x
    w = x**degree + sum(coefficients[3+j]*x**j for j in range(degree))
    first, third = (x*v-w*s) % f1, (u*f1-w*s) % x
    return vector(QQ, [first[j] for j in range(4)] + [third[0]])


inconsistent_degrees = []
for degree in range(3):
    nvars = 3+degree
    zero = vector(QQ, nvars)
    constant = constraints(zero, degree)
    columns = []
    for j in range(nvars):
        basis = vector(QQ, nvars)
        basis[j] = 1
        columns.append(constraints(basis, degree)-constant)
    linear = matrix(QQ, columns).transpose()
    try:
        solution = linear.solve_right(-constant)
    except ValueError:
        inconsistent_degrees.append(degree)
        continue
    assert constraints(solution, degree) == 0
    u, v = R(solution[0]), solution[1]+solution[2]*x
    w = x**degree + sum(solution[3+j]*x**j for j in range(degree))
    break
else:
    raise AssertionError('No Stoll solution within the promised degree bounds')
assert inconsistent_degrees == [0, 1] and degree == 2
assert u*u*f1 == x*v*v+w*w
assert u.degree() == 0 and u != 0
r = (-v*x/u[0]) % w
assert (f-r*r) % w == 0


def cantor_add(left, right):
    a1, b1 = left
    a2, b2 = right
    d0, h1, h2 = a1.xgcd(a2)
    d, h3, h4 = d0.xgcd(b1+b2)
    A, remainder = (a1*a2).quo_rem(d*d)
    assert remainder == 0
    numerator = h3*h1*a1*b2+h3*h2*a2*b1+h4*(b1*b2+f)
    B, remainder = numerator.quo_rem(d)
    assert remainder == 0
    B %= A
    while A.degree() > 2:
        next_A, remainder = (f-B*B).quo_rem(A)
        assert remainder == 0
        A = next_A.monic()
        B = (-B) % A
    return A.monic(), B % A


P, Q = (x, R(0)), (w, r)
twice = cantor_add(Q, Q)
four_times = cantor_add(twice, twice)
assert twice == P and four_times == (R(1), R(0))
assert Q != (R(1), R(0)) and twice != (R(1), R(0))


def dyadic_label(value):
    value = QQ(value)
    assert value != 0
    valuation = int(value.valuation(2))
    unit = value/QQ(2)**valuation
    odd_residue = int((unit.numerator()*unit.denominator().inverse_mod(8)) % 8)
    sign, five = {1: (0, 0), 3: (1, 1), 5: (0, 1), 7: (1, 0)}[odd_residue]
    return {'valuation': valuation, 'odd_unit_mod_8': odd_residue,
            'F2_coordinates_2_minus1_5': [valuation % 2, sign, five]}


P_representatives = [f1(root)-root for root in roots]
Q_representatives = [w(root) for root in roots]
P_labels = [dyadic_label(value) for value in P_representatives]
Q_labels = [dyadic_label(value) for value in Q_representatives]
assert all(label['F2_coordinates_2_minus1_5'] == [0, 0, 0] for label in P_labels)

# F(z)=z^(2g+1)f(1/z), using f=x^(2g+1)+x+1 independently for each genus.
Z = PolynomialRing(QQ, 'z')
z = Z.gen()
N, terms = 2, 64
log_cases = []
for genus in range(1, 6):
    polynomial = x**(2*genus+1)+x+1
    assert polynomial.gcd(polynomial.derivative()) == 1
    correction = z**(2*genus)+z**(2*genus+1)
    truncated = sum((binomial(-QQ(1)/2, j)*correction**j
                     for j in range((terms-1)//(2*genus)+1)), Z(0))
    coefficients = [truncated[m] for m in range(terms)]
    assert all(c == 0 or c.valuation(2) >= -2*m for m, c in enumerate(coefficients))
    logs = matrix(QQ, genus, genus, lambda i, k: -sum(
        coefficients[m]*QQ(2**N*(i+1))**(2*k+2*m+1)/(2*k+2*m+1)
        for m in range(terms)))
    actual = int(logs.det().valuation(2))
    predicted = N*genus**2 + sum(int(QQ(i).valuation(2)) for i in range(1, genus+1)) + sum(
        int(QQ(j*j-i*i).valuation(2)) for i in range(1, genus+1) for j in range(i+1, genus+1))
    tail_bound = N*genus**2+2*terms*(N-1)
    assert actual == predicted and tail_bound > predicted
    log_cases.append({'g': genus, 'f': str(polynomial), 'N': N, 'retained_c_m': terms,
                      'truncated_determinant_v2': actual, 'predicted_full_determinant_v2': predicted,
                      'omitted_determinant_tail_v2_lower_bound': tail_bound,
                      'tail_strictly_above_determinant': True})

result = {
    'status': 'PASS', 'scope': 'Exact finite classical halving and formal-log determinant controls only.',
    'halving': {'f': str(f), 's': str(s), 'square_root_values': [str(a) for a in s_values],
        'inconsistent_monic_w_degrees': inconsistent_degrees,
        'u': str(u), 'v': str(v), 'w': str(w), 'r': str(r),
        'Stoll_identity_exact': True, 'independent_Cantor_2Q_equals_P': True,
        'independent_Cantor_4Q_equals_zero': True, 'Q_exact_order': 4,
        'P_Kummer_values': [str(a) for a in P_representatives], 'P_dyadic_labels': P_labels,
        'Q_Kummer_values': [str(a) for a in Q_representatives], 'Q_dyadic_labels': Q_labels,
        'Q_has_nonzero_dyadic_label': any(any(label['F2_coordinates_2_minus1_5']) for label in Q_labels)},
    'log_determinants': log_cases,
    'tail_bound': {
        'coefficient_bound': 'v2(c_m)>=-2m: binomial(-1/2,j)=(-1)^j binomial(2j,j)/4^j, j<=m, with integral F.',
        'entry_tail': 'For k=0..g-1 and m>=M, v2(c_m*(2^N i)^(2k+2m+1)/(2k+2m+1)) >= N(2k+1)+2M(N-1).',
        'determinant_tail': 'Every determinant difference term has an omitted entry; other column k entries have valuation >=N(2k+1). Hence v2(det(full)-det(truncated))>=N*g^2+2M(N-1).',
        'finite_checks_are_all_g_proof': False},
    'claim_gates': {'full_local_image': False, 'global_Selmer': False,
                    'quantum_execution': False, 'general_saturation_clock': False},
}
Path(__file__).with_name('result.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'status': result['status'], 'halving': result['halving'],
                  'log_determinants': log_cases}, indent=2))
