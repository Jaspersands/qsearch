#!/opt/anaconda3/envs/qsearch-cas/bin/python
"""Two predeclared exact algebra controls, not a Kuperberg implementation.

Run with Sage's Python.  The source polynomial is harness data only; the
fingerprint circuit accesses it through the counted bit-output oracle.
The width test is explicitly conditional on its correct harness center.
"""
from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import random
import time

from sage.all import (
    CyclotomicField, GF, PolynomialRing, QQ, QQbar, ZZ,
    identity_matrix, matrix, ones_matrix, vector,
)
from sage.version import version as sage_version


HERE = Path(__file__).resolve()
OUTPUT = HERE.with_suffix('.json')
PRIMES = (37, 43)
PUBLIC_SEED = 7301
GLOBAL_FINGERPRINT_DELTA = Fraction(1, 64)


def contract(p):
    length, bound = 0, Fraction(p*p)
    while bound > GLOBAL_FINGERPRINT_DELTA:
        length += 1
        bound *= Fraction(3, 4)
    # Draw once, with replacement.  Neither outcome nor secret selects offsets.
    rng = random.Random(PUBLIC_SEED)
    offsets = [rng.randrange(p) for _ in range(length)]
    return {
        'p': p, 'harness_center_a': 7,
        'width_rule': 'first positive public quadratic nonresidue',
        'public_seed': PUBLIC_SEED, 'public_offsets': offsets,
        'fingerprint_length': length,
        'global_union_bound': str(bound), 'global_delta_target': '1/64',
    }


def check_case(case):
    p, a = case['p'], case['harness_center_a']
    Fp = GF(p)
    R = PolynomialRing(Fp, 'X')
    X = R.gen()

    def chi(value):
        value = Fp(value)
        return 0 if not value else (1 if value.is_square() else -1)

    chars = [chi(x) for x in range(p)]
    d = next(x for x in range(1, p) if chars[x] == -1)
    b, c = int(Fp(-2*a)), int(Fp(a*a-d))
    hidden_polynomial = X*X + b*X + c
    assert hidden_polynomial.is_irreducible()
    case['harness_width_d'] = d
    case['harness_coefficients_b_c'] = [b, c]
    case['harness_only_not_recovered_by_a_sieve'] = True
    query_counts = Counter()
    queried_points = set()

    def oracle(value, purpose):
        value = int(Fp(value))
        query_counts[purpose] += 1
        queried_points.add(value)
        result = chi(hidden_polynomial(Fp(value)))
        assert result in (-1, 1)
        return int(result == -1)  # Native reversible oracle's output bit.

    # F'=F o inversion.  Its argument computation does NOT use the secret a.
    fingerprints, fibers = {}, defaultdict(list)
    for t in range(p):
        for branch in (0, 1):
            arguments = [(offset-t) if branch == 0 else (t-offset)
                         for offset in case['public_offsets']]
            label = tuple(oracle(x, 'fingerprint_full_enumeration')
                          for x in arguments)
            fingerprints[t, branch] = label
            fibers[label].append((t, branch))
    shift = int(Fp(2*a))
    assert len(fibers) == p
    for t in range(p):
        expected = {(t, 0), ((t+shift) % p, 1)}
        assert set(fibers[fingerprints[t, 0]]) == expected
    assert query_counts['fingerprint_full_enumeration'] == 2*p*case['fingerprint_length']

    # An exact cyclotomic field contains both the p-th root and i.  The
    # canonical QQbar embedding fixes the sign of the real square root.
    K = CyclotomicField(4*p, names='zeta4p')
    zeta4p = K.gen()
    zeta, imaginary = zeta4p**4, zeta4p**p
    powers = [zeta**j for j in range(p)]
    tau = sum((chars[j]*powers[j] for j in range(p)), K.zero())
    expected_gauss_phase = K.one() if p % 4 == 1 else imaginary
    sqrt_p = tau / expected_gauss_phase
    embedding = K.hom([QQbar.zeta(4*p)], QQbar)
    assert sqrt_p*sqrt_p == p
    assert embedding(sqrt_p).imag() == 0 and embedding(sqrt_p).real() > 0
    assert tau*tau.conjugate() == p
    assert tau/sqrt_p == expected_gauss_phase

    # Exact positive-QFT amplitudes from each ACTUAL fiber, retaining k=0.
    # Common input sqrt(2) normalization is accounted for in probabilities.
    phase_checks = 0
    for t in range(p):
        actual = fibers[fingerprints[t, 0]]
        x0 = next(x for x, branch in actual if branch == 0)
        x1 = next(x for x, branch in actual if branch == 1)
        for k in range(p):
            amplitude0 = powers[(k*x0) % p]
            amplitude1 = powers[(k*x1) % p]
            assert amplitude1 == powers[(k*shift) % p]*amplitude0
            probability_k = (amplitude0*amplitude0.conjugate()
                             + amplitude1*amplitude1.conjugate()) / (2*p)
            assert probability_k == QQ(1)/p
            phase_checks += 1
    # Omitting inversion leaves a coset-dependent relative phase.
    raw_relative_shifts = set()
    for t in range(p):
        raw_label = fingerprints[(-t) % p, 0]
        other = next(u for u in range(p) if fingerprints[u, 1] == raw_label)
        raw_relative_shifts.add((other-t) % p)
    assert len(raw_relative_shifts) == p

    C = matrix(ZZ, p, p, lambda y, z: chars[(y-z) % p])
    J = ones_matrix(ZZ, p)
    assert C.transpose()*C == p*identity_matrix(ZZ, p)-J
    assert C*J == matrix(ZZ, p, p, 0) and J*C == matrix(ZZ, p, p, 0)
    assert C.transpose() == chars[-1]*C

    # F U F^dagger is diagonal.  Verify every circulant coefficient of
    # F^dagger D F instead of cubic cyclotomic matrix multiplication.
    diagonal = [K.one()] + [tau*chars[k]/sqrt_p for k in range(1, p)]
    assert all(value*value.conjugate() == 1 for value in diagonal)
    for difference in range(p):
        reconstructed = sum((diagonal[k]*powers[(-k*difference) % p]
                             for k in range(p)), K.zero()) / p
        assert reconstructed == K(chars[difference])/sqrt_p + QQ(1)/p
    wrong_real_gauss_rejected = None
    if p % 4 == 3:
        wrong_diagonal = [K.one()] + [K(chars[k]) for k in range(1, p)]
        assert wrong_diagonal != diagonal
        wrong_coefficient = sum((wrong_diagonal[k]*powers[(-k) % p]
                                 for k in range(p)), K.zero()) / p
        assert wrong_coefficient != K(chars[1])/sqrt_p + QQ(1)/p
        wrong_real_gauss_rejected = True
    # Dropping the zero-frequency correction has a zero eigenvalue.
    assert C.transpose()*C/p != identity_matrix(QQ, p)

    squares = [z for z in range(p) if chars[z] >= 0]
    count = len(squares)
    assert count == (p+1)//2 and d not in squares
    assert {int(Fp(r*r)) for r in range(count)} == set(squares)
    phase_vector = [0]*p
    root_checks = []
    for z in squares:
        root = int(Fp(z).sqrt())
        root = min(root, p-root)
        assert int(Fp(root*root)) == z and 0 <= root < count
        sign = (-1)**oracle(a+root, 'width_canonical_root')
        other_sign = (-1)**oracle(a-root, 'width_alternative_root_control')
        assert sign == other_sign == chi(z-d)
        phase_vector[z] = sign
        root_checks.append([z, root])
    v = vector(ZZ, phase_vector)
    convolution = C*v
    T = int(sum(v))
    assert T == -(1+chars[-1])//2
    assert convolution[d] == chars[-1]*count
    probabilities = []
    exact_probabilities = []
    for y in range(p):
        numerator = int(convolution[y])
        unnormalized_amplitude = K(numerator)/sqrt_p + QQ(T)/p
        probability = unnormalized_amplitude*unnormalized_amplitude.conjugate()/count
        rational = QQ(numerator*numerator*p+T*T)/(count*p*p)
        sqrt_coefficient = QQ(2*numerator*T)/(count*p*p)
        assert probability == rational+sqrt_coefficient*sqrt_p
        exact_probabilities.append(probability)
        probabilities.append({'output': y, 'rational': str(rational),
                              'sqrt_p_coefficient': str(sqrt_coefficient)})
    assert sum(exact_probabilities, K.zero()) == 1
    assert sum(QQ(item['rational']) for item in probabilities) == 1
    assert sum(QQ(item['sqrt_p_coefficient']) for item in probabilities) == 0
    if p % 4 == 3:
        expected_target = K(count)/p
        formula = '|S|/p'
    else:
        expected_target = (K(count)/sqrt_p-QQ(1)/p)**2/count
        formula = '(sqrt(|S|/p)-1/(p*sqrt(|S|)))^2'
    assert exact_probabilities[d] == expected_target
    assert query_counts['width_canonical_root'] == count
    assert query_counts['width_alternative_root_control'] == count

    return dict(case, passed=True,
                exact_field=f'CyclotomicField({4*p}) with canonical QQbar embedding',
                gauss_phase='1' if p % 4 == 1 else 'i',
                all_fibers_checked=len(fibers), all_fiber_sizes_two=True,
                exact_coset_phase_and_uniform_label_checks=phase_checks,
                zero_fourier_label_retained=True,
                omitted_inversion_relative_shifts=len(raw_relative_shifts),
                exact_C_adjoint_C_and_zero_frequency_identities=True,
                exact_QFT_unitary_circulant_coefficients=p,
                exact_diagonal_unit_modulus_checks=p,
                wrong_real_gauss_phase_rejected=wrong_real_gauss_rejected,
                omitted_zero_frequency_rejected=True,
                native_square_root_pairs=root_checks,
                square_domain_size=count, restricted_character_sum=T,
                exact_width_target_formula=formula,
                exact_width_target_probability=probabilities[d],
                exact_output_probabilities=probabilities,
                exact_probability_sum='1',
                oracle_counts=dict(query_counts),
                control_native_oracle_calls=sum(query_counts.values()),
                distinct_control_native_points=len(queried_points),
                native_queries_per_fresh_DCP_sample=case['fingerprint_length'],
                width_state_native_queries_per_coherent_preparation=1,
                classical_public_character_table_entries=p)


def main():
    started = time.monotonic()
    cases = [contract(p) for p in PRIMES]
    report = {
        'status': 'PREDECLARED_EXACT_ALGEBRA_CONTROL',
        'predeclaration_revision': 'Before execution, parent authorized replacing p41 '
            'with p43: p37 and p41 were both1 mod4. Exactly p37/p43 now cover both branches.',
        'source_contracts': cases, 'sage_version': sage_version,
        'script_sha256': hashlib.sha256(HERE.read_bytes()).hexdigest(),
        'scope': 'Dense finite exact algebra control using hidden parameters only in '
            'the oracle harness and expected-answer checks. Width test is conditional on '
            'the correct harness center. No sieve or efficient measurement is simulated.',
        'kuperberg_sieve_implemented': False,
        'end_to_end_quantum_decoder_executed': False,
        'asymptotic_or_speedup_evidence_claimed': False,
        'q1_or_phase_only_transfer_claimed': False,
        'rows': [],
    }
    OUTPUT.write_text(json.dumps(report, indent=2)+'\n')
    print('PREDECLARED: p37/p43, a7, first nonsquare, seed7301, delta<=1/64; no rerolls.', flush=True)
    for case in cases:
        try:
            row = check_case(dict(case))
        except Exception as error:
            row = dict(case, passed=False, error_type=type(error).__name__, error=str(error))
        report['rows'].append(row)
        OUTPUT.write_text(json.dumps(report, indent=2)+'\n')
        print('p', case['p'], 'passed', row['passed'],
              'native_calls', row.get('control_native_oracle_calls'),
              'target_probability', row.get('exact_width_target_probability'), flush=True)
    report['status'] = ('EXACT_NATIVE_DCP_AND_PARTIAL_LEGENDRE_IDENTITIES_PASS'
                        if all(row['passed'] for row in report['rows']) else
                        'EXACT_ALGEBRA_CONTROL_HAS_FAILURE')
    report['wall_seconds'] = time.monotonic()-started
    OUTPUT.write_text(json.dumps(report, indent=2)+'\n')
    assert all(row['passed'] for row in report['rows']), report['status']


if __name__ == '__main__':
    main()
