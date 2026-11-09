"""Exact local-residue/determinant controls, not an integral similarity solver.

Use /opt/anaconda3/envs/qsearch-cas/bin/python for Sage algebra.
"""
import json
from pathlib import Path
from sage.all import (NumberField, PolynomialRing, QQ, block_diagonal_matrix,
                      identity_matrix, matrix, vector)

S = PolynomialRing(QQ, 'x')
x = S.gen()
K = NumberField(x**2-2, 'a')
a = K.gen()
O = K.ring_of_integers()
P = K.primes_above(2)[0]
E = 2**200 + 1


def modular_power(base, exponent, modulus):
    if exponent < 0:
        base, exponent = base.inverse_mod(modulus), -exponent
    result, base = base.parent()(1), modulus.reduce(base)
    while exponent:
        if exponent & 1:
            result = modulus.reduce(result*base)
        base = modulus.reduce(base*base)
        exponent >>= 1
    return result


def local_product(field, prime, precision, atoms, exponents):
    valuations = [int(field.ideal(atom).valuation(prime)) for atom in atoms]
    total = sum(e*v for e, v in zip(exponents, valuations))
    if total < 0:
        return {'status': 'NEGATIVE_VALUATION', 'valuation': total}, None
    uniformizer = next(b for b in prime.basis() if field.ideal(b).valuation(prime) == 1)
    modulus = prime**precision
    result, denominators = field(1), []
    for atom, exponent, valuation in zip(atoms, exponents, valuations):
        unit = atom*uniformizer**(-valuation)
        denominator_ideal = field.ideal(1).intersection(field.ideal(1/unit))
        denominator = next(b for b in denominator_ideal.basis()
                           if field.ideal(b).valuation(prime) == 0)
        numerator = denominator*unit
        assert numerator in field.ring_of_integers()
        residue = modulus.reduce(numerator*denominator.inverse_mod(modulus))
        result = modulus.reduce(result*modular_power(residue, exponent, modulus))
        denominators.append({'value': str(denominator), 'valuation': 0,
                             'denominator_ideal_norm': str(denominator_ideal.norm())})
    result = field(0) if total >= precision else modulus.reduce(result*uniformizer**total)
    return {'status': 'PASS', 'valuation': total, 'leaf_valuations': valuations,
            'uniformizer': str(uniformizer), 'local_denominators': denominators,
            'residue': str(result)}, result


precision = 17
dyadic, residue = local_product(K, P, precision, [6+4*a, K(2)], [E, -E])
modulus = P**precision
direct = modular_power(3+2*a, E, modulus)
assert residue == direct and dyadic['leaf_valuations'] == [2, 2]
assert dyadic['valuation'] == 0 and P.ramification_index() == 2

# Divide the SUM U^E-1 by 2 only after enlarging the ideal modulus by (2).
larger = P**(precision+2)
large_residue = modular_power(3+2*a, E, larger)
quotient_residue = modulus.reduce((large_residue-1)/2)
assert (large_residue-1)/2 in O
try:
    K(2).inverse_mod(modulus)
except ZeroDivisionError:
    invalid_inverse_rejected = True
else:
    invalid_inverse_rejected = False
assert invalid_inverse_rejected
# Independent binary geometric sum: (U^E-1)/2 = (1+a) sum_(j<E) U^j.
remaining, accumulated_power, accumulated_sum = E, K(1), K(0)
block_power, block_sum = 3+2*a, K(1)
while remaining:
    if remaining & 1:
        accumulated_sum = modulus.reduce(accumulated_sum+accumulated_power*block_sum)
        accumulated_power = modulus.reduce(accumulated_power*block_power)
    block_sum = modulus.reduce(block_sum*(1+block_power))
    block_power = modulus.reduce(block_power**2)
    remaining >>= 1
assert quotient_residue == modulus.reduce((1+a)*accumulated_sum)

L = NumberField(x**2-5, 'b')
b = L.gen()
split_primes = L.primes_above(11)
good = next(Q for Q in split_primes if L.ideal(b-4).valuation(Q) == 1)
bad = next(Q for Q in split_primes if Q != good)
u = (b-4)/11
assert u == -1/(b+4) and u.denominator() == 11
split, split_residue = local_product(L, good, 4, [u], [1])
assert split_residue == (good**4).reduce(-(b+4).inverse_mod(good**4))
opposite, _ = local_product(L, bad, 4, [u], [1])
assert opposite == {'status': 'NEGATIVE_VALUATION', 'valuation': -1}

# K[t]-module lengths: j=1 with multiplicity 2; j=3 with multiplicity 1.
N3 = matrix(K, [[0, 1, 0], [0, 0, 1], [0, 0, 0]])
A2 = matrix(K, [[1+a, 2], [1, 3]])
scalar = 2+a
BK = a*identity_matrix(K, 5) + block_diagonal_matrix(matrix(K, 2), N3)
alpha0 = block_diagonal_matrix(A2, scalar*identity_matrix(K, 3))
radical = block_diagonal_matrix(matrix(K, 2), 7*N3+3*N3**2)
alpha = alpha0+radical
assert radical**3 == 0 and BK*alpha == alpha*BK


def rational_restriction(operator):
    columns = []
    for slot in range(5):
        for power in range(2):
            v = vector(K, [a**power if j == slot else 0 for j in range(5)])
            columns.append(vector(QQ, [c for entry in operator*v for c in entry.vector()]))
    return matrix(QQ, columns).transpose()


BQ, alphaQ, alpha0Q = map(rational_restriction, [BK, alpha, alpha0])
assert BQ*alphaQ == alphaQ*BQ
assert BQ.charpoly() == (x**2-2)**5
predicted = A2.det().norm()*scalar.norm()**3
wrong_multiplicity_exponent = A2.det().norm()**2*scalar.norm()
assert alphaQ.det() == alpha0Q.det() == predicted == -136
assert wrong_multiplicity_exponent == 578 and predicted != wrong_multiplicity_exponent

result = {
    'status': 'PASS', 'scope': 'Exact finite classical local-residue and determinant gates only.',
    'ramified_dyadic': dict(dyadic, precision=precision, exponent_binary_bits=E.bit_length(),
                            exponent='2^200+1', nonunit_leaves=True, direct_small_unit_power_matches=True),
    'denominator_enlarged_division': {'expression': '((3+2sqrt(2))^E-1)/2',
        'target_P_precision': precision, 'enlarged_P_precision': precision+2,
        'residue': str(quotient_residue), 'binary_geometric_sum_matches': True,
        'inverting_2_mod_P_power_rejected': invalid_inverse_rejected},
    'split_11_local_unit': dict(split, original_rational_denominator=11,
                               alternate_unit_denominator_matches=True, opposite_prime=opposite),
    'determinant_character': {'rational_dimension': 10, 'module_j_and_multiplicity': [[1, 2], [3, 1]],
        'B_characteristic_polynomial': str(BQ.charpoly()), 'commutation_exact': True,
        'quotient_determinant_norms': [str(A2.det().norm()), str(scalar.norm())],
        'predicted_and_actual_Q_determinant': str(predicted), 'radical_lift_independence': True,
        'incorrect_multiplicity_exponent_determinant': str(wrong_multiplicity_exponent)},
    'claim_gates': {'full_similarity_solver': False, 'algorithm_execution': False,
                    'quantum_execution': False, 'novelty': False, 'speedup': False},
}
Path(__file__).with_name('result.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
