#!/opt/anaconda3/envs/qsearch-cas/bin/python
"""Exact fixed-input control of native phase access to relative output bits.

Run with Sage's Python. Secret coefficients belong only to the test harness.
The compiler receives a phase-oracle callback, p, public reference x0, and
computational-basis input X,B. Full-basis equality establishes the linear
operator identity, hence also its action on arbitrary coherent inputs.
This is neither an end-to-end recovery algorithm nor a speedup experiment.
"""
from collections import Counter
from fractions import Fraction
import hashlib
import json
from pathlib import Path

from sage.all import GF, PolynomialRing
from sage.version import version as sage_version


SOURCE = Path(__file__).resolve()
OUTPUT = SOURCE.with_suffix('.json')
# Fixed before any outcomes: all monic irreducible quadratics, references,
# and computational-basis X,B at both primes. No random/selected examples.
PRIMES = (5, 7)


def _hadamard_integer(state):
    """One unnormalized H; the pair of H gates is normalized at the end."""
    result = Counter()
    for (x, bit, reference), amplitude in state.items():
        for out_bit in (0, 1):
            result[x, out_bit, reference] += amplitude * (-1)**(bit*out_bit)
    return {key: value for key, value in result.items() if value}


def _controlled_swap(state):
    return {
        ((reference, bit, x) if bit else (x, bit, reference)): amplitude
        for (x, bit, reference), amplitude in state.items()
    }


def _unconditional_phase_query(state, phase_oracle):
    """One coherent oracle layer; dense simulation evaluates each branch."""
    result = {}
    for (x, bit, reference), amplitude in state.items():
        phase = phase_oracle(reference)
        if phase not in (-1, 1):
            raise ValueError('Native phase promise requires g(x) in {-1,+1}; zero rejected')
        result[x, bit, reference] = amplitude * int(phase)
    return result


def compile_relative_bit(phase_oracle, p, x0, basis_x, basis_bit):
    """H_B, CSWAP, unconditional U_g(R), CSWAP, H_B; R starts at x0."""
    if not (0 <= x0 < p and 0 <= basis_x < p and basis_bit in (0, 1)):
        raise ValueError('Input basis label outside its register')
    state = _hadamard_integer({(basis_x, basis_bit, x0): 1})
    state = _controlled_swap(state)
    state = _unconditional_phase_query(state, phase_oracle)
    state = _controlled_swap(state)
    state = _hadamard_integer(state)
    return {key: Fraction(value, 2) for key, value in state.items()}


def omitted_cswap_control(phase_oracle, p, x0, basis_x, basis_bit):
    """Negative control: delete both controlled swaps from the circuit."""
    state = _hadamard_integer({(basis_x, basis_bit, x0): 1})
    state = _unconditional_phase_query(state, phase_oracle)
    state = _hadamard_integer(state)
    return {key: Fraction(value, 2) for key, value in state.items()}


def check_prime(p):
    field = GF(p)
    ring = PolynomialRing(field, 'X')
    X = ring.gen()
    counts = Counter()
    first_negative_failure = None

    # Every secret and character table is harness-only data. The compiler
    # has no reference to b,c, the polynomial, this table, or an expected bit.
    for b in range(p):
        for c in range(p):
            polynomial = X**2 + b*X + c
            if not polynomial.is_irreducible():
                continue
            counts['irreducible_quadratics'] += 1
            table = []
            for x in range(p):
                value = polynomial(field(x))
                table.append(0 if not value else (1 if value.is_square() else -1))
                counts['harness_character_evaluations'] += 1
            assert all(phase in (-1, 1) for phase in table)

            def oracle(x):
                counts['positive_classical_oracle_callback_evaluations'] += 1
                return table[x]

            def negative_oracle(x):
                counts['negative_classical_oracle_callback_evaluations'] += 1
                return table[x]

            for x0 in range(p):
                counts['secret_reference_pairs'] += 1
                for x in range(p):
                    relative_bit = int(table[x] != table[x0])
                    for bit in (0, 1):
                        expected = {(x, bit ^ relative_bit, x0): Fraction(table[x0])}
                        actual = compile_relative_bit(oracle, p, x0, x, bit)
                        assert actual == expected, (p, b, c, x0, x, bit, actual, expected)
                        counts['basis_cases'] += 1
                        counts['exact_operator_identity_checks_passed'] += 1
                        assert all(key[0] == x and key[2] == x0 for key in actual)
                        counts['clean_reference_checks_passed'] += 1
                        negative = omitted_cswap_control(negative_oracle, p, x0, x, bit)
                        if negative != expected:
                            counts['negative_control_failures'] += 1
                            if first_negative_failure is None:
                                first_negative_failure = {
                                    'harness_b_c': [b, c], 'x0': x0,
                                    'basis_x': x, 'basis_bit': bit,
                                    'g_x0': table[x0], 'g_x': table[x],
                                    'expected_output_bit': bit ^ relative_bit,
                                    'negative_output_bit': bit,
                                }
                        else:
                            counts['negative_control_coincidental_matches'] += 1

    assert counts['irreducible_quadratics'] == p*(p-1)//2
    assert counts['basis_cases'] == p*(p-1)//2 * p * p * 2
    assert counts['negative_control_failures'] == p*(p-1)//2 * (p*p-1)
    assert counts['positive_classical_oracle_callback_evaluations'] == 2*counts['basis_cases']
    assert counts['negative_classical_oracle_callback_evaluations'] == 2*counts['basis_cases']

    # A reducible X^2 oracle gives phase zero at the public reference 0.
    # It must be rejected, rather than treated as a unitary phase operation.
    def invalid_zero_oracle(x):
        value = field(x)**2
        return 0 if not value else (1 if value.is_square() else -1)

    try:
        compile_relative_bit(invalid_zero_oracle, p, 0, 1, 0)
    except ValueError:
        counts['zero_output_promise_rejections'] += 1
    else:
        raise AssertionError('Accepted a zero-output phase oracle')
    assert first_negative_failure is not None
    return {'p': p, 'counts': dict(counts), 'first_negative_failure': first_negative_failure}


def main():
    cases = [check_prime(p) for p in PRIMES]
    totals = Counter()
    for case in cases:
        totals.update(case['counts'])
    report = {
        'status': 'PASS',
        'source_file': SOURCE.name,
        'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        'sage_version': sage_version,
        'predeclared_inputs': {
            'primes': list(PRIMES),
            'secrets': 'ALL monic irreducible X^2+bX+c over F_p',
            'references_x0': 'ALL F_p',
            'basis_inputs_X_B': 'ALL F_p x {0,1}',
            'amplitudes': 'Exact integer unnormalized Hadamards followed by division by 2',
        },
        'native_access': 'Unconditional U_g|x>=g(x)|x>, with g(x) in {-1,+1}',
        'identity': 'C_g|x,B,x0> = g(x0)|x,B XOR (L_g(x) XOR L_g(x0)),x0>',
        'global_phase': 'g(x0) is independent of X,B and retained in exact equality',
        'coherent_superpositions': 'Covered by equality on every basis input and linearity',
        'resources': {
            'coherent_native_phase_queries_per_compiled_call': 1,
            'controlled_swaps_per_compiled_call': 2,
            'hadamards_per_compiled_call': 2,
            'controlled_oracle_queries': 0,
            'reference_register': 'Public |x0>, returned clean; O(log p) qubits',
            'classical_simulation_cost': 'Each basis case evaluates two phase branches per circuit; harness additionally enumerates p character values per secret. These are classical simulation evaluations, not native coherent-query counts.',
        },
        'zero_promise_scope': 'The compiler rejects a zero returned on a simulated branch; native nonzero output at every x remains an input promise, not a globally verified property of a black-box oracle.',
        'claim': 'Unconditional native phase access suffices to coherently compute relative output bits with one phase query per call, up to the fixed global phase g(x0).',
        'limits': 'Finite exact compiler control only. No end-to-end recovery algorithm executed; no polynomial-time algorithm, quantum speedup, novelty, or classical hardness claim.',
        'totals': dict(totals),
        'cases': cases,
    }
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'status': report['status'], 'output': str(OUTPUT), 'source_sha256': report['source_sha256'], 'totals': dict(totals)}, sort_keys=True))


if __name__ == '__main__':
    main()
