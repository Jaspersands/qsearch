from fractions import Fraction
import hashlib
from itertools import product
import json
import math
import random

import numpy as np
import pytest
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

from theorems import ternary_coherent_reliability as audit
from theorems import ternary_coloring_bpqm as local


def test_exact_integer_updates_match_normalized_physical_channel_formulas():
    for a, b in (((0, 1, 1), (0, 1, 1)), ((1, 2, 4), (2, 0, 5)), ((1, 0, 0), (0, 1, 0))):
        left, right = audit.Header(a, sum(a)), audit.Header(b, sum(b))
        for signs in product((1, -1), repeat=2):
            mu = tuple(left.spectrum[signs[0]*j % 3] for j in range(3))
            nu = tuple(right.spectrum[signs[1]*j % 3] for j in range(3))
            assert audit.combine(left, right, "bit", signs=signs).spectrum == local.bit_spectrum(mu, nu)
            branches = {h: (p, spectrum) for h, p, spectrum in local.check_branches(mu, nu)}
            for h in range(3):
                header = audit.combine(left, right, "check", h, signs=signs)
                if h in branches:
                    assert header.spectrum == branches[h][1]
                    assert Fraction(sum(header.weights), sum(a)*sum(b)) == branches[h][0]
                else:
                    assert header.spectrum is None
            assert audit.combine(left, right, "check", 3, signs=signs).weights == (0, 0, 0)


def test_physical_integer_width_is_linear_in_distinct_leaf_count_not_header_histories():
    header = audit.Header((0, 1, 1), 2)
    leaves = 1
    rng = random.Random(773)
    for _ in range(35):
        # Independent copies are a mathematical tree control, not channel cloning.
        header = audit.combine(header, audit.Header((0, 1, 1), 2),
                               rng.choice(("bit", "check")), rng.randrange(3))
        leaves += 1
        assert header.capacity == 1 << leaves
        assert header.width == leaves+1
        assert sum(header.weights) <= 1 << leaves


@pytest.mark.parametrize("kind", ("bit", "check", "fiber"))
def test_actual_one_bit_circuit_exhaustive_clean_input_domain_and_dark_selector(kind):
    program = audit.message_program(1, kind)
    operations = audit.permutation_ops(program.circuit)
    output_mask = sum(1 << q for q in program.output)
    for values in product(range(2), repeat=6):
        left, right = audit.Header(values[:3], 3), audit.Header(values[3:], 3)
        for h in range(4):
            original = program.encode(left.weights, right.weights, h)
            actual = audit.apply_basis(operations, original)
            assert program.read_output(actual) == audit.combine(left, right, kind, h).weights
            assert actual & ~output_mask == original
            assert audit.apply_basis(operations, actual, inverse=True) == original


@pytest.mark.parametrize("signs", tuple(product((1, -1), repeat=2)))
@pytest.mark.parametrize("kind", ("bit", "check", "fiber"))
def test_actual_larger_weight_circuit_signs_maximum_values_and_complex_superpositions(signs, kind):
    program = audit.message_program(3, kind, signs=signs)
    operations = audit.permutation_ops(program.circuit)
    sources = (((7, 7, 7), (7, 7, 7), 0), ((1, 2, 5), (7, 3, 0), 1),
               ((0, 0, 0), (1, 0, 0), 2), ((0, 1, 1), (0, 1, 1), 3))
    state = {program.encode(a, b, h): amplitude for (a, b, h), amplitude in
             zip(sources, (1/2, 1j/2, -1/2, -1j/2))}
    actual = audit.apply_sparse(operations, state)
    for (a, b, h), amplitude in zip(sources, state.values()):
        original = program.encode(a, b, h)
        target = audit.apply_basis(operations, original)
        assert actual[target] == amplitude
        expected = audit.combine(audit.Header(a, max(1, sum(a))), audit.Header(b, max(1, sum(b))), kind, h, signs=signs)
        assert program.read_output(target) == expected.weights
        assert not any(target >> q & 1 for q in program.scratch)
    assert audit.apply_sparse(operations, actual, inverse=True) == state


@pytest.mark.parametrize("width", (1, 2))
def test_lowered_standard_multiplier_matches_independent_full_statevector_including_phases(width):
    circuit = audit.multiplier(width)
    operations = audit.permutation_ops(circuit)
    rng = np.random.default_rng(901+width)
    vector = rng.normal(size=1 << circuit.num_qubits)+1j*rng.normal(size=1 << circuit.num_qubits)
    vector /= np.linalg.norm(vector)
    direct = Statevector(vector).evolve(circuit).data
    expected = np.zeros_like(vector)
    for basis, amplitude in enumerate(vector):
        expected[audit.apply_basis(operations, basis)] = amplitude
    assert np.allclose(direct, expected, atol=1e-12)
    # Independently verify its clean-ancilla arithmetic contract.
    for a, b in product(range(1 << width), repeat=2):
        source = a+(b << width)
        assert audit.apply_basis(operations, source) == source+((a*b) << (2*width))


def test_sparse_auditor_refuses_to_hide_phases_or_nonpermutation_operations():
    circuit = QuantumCircuit(2)
    circuit.z(0)
    with pytest.raises(ValueError):
        audit.permutation_ops(circuit)
    circuit = QuantumCircuit(2, global_phase=.2)
    with pytest.raises(ValueError):
        audit.permutation_ops(circuit)


def test_digit_comparison_all_signs_exact_zero_terms_and_equalities():
    for p, q, a, b in product(range(-3, 4), range(-3, 4), range(5), range(5)):
        value = p*math.sqrt(b)-q*math.sqrt(a)
        expected = 0 if abs(value) < 1e-12 else (1 if value > 0 else -1)
        assert audit.root_difference_sign(p, q, a, b) == expected
    huge = 1 << 4096
    assert audit.root_difference_sign(huge, huge-1, 1, 1) == 1
    assert audit.root_difference_sign(-huge, -huge+1, 1, 1) == -1


@pytest.mark.parametrize("steps", (1, 2, 4, 8, 16, 32))
def test_integer_cordic_uniform_angle_bound_including_endpoints_and_tiny_ratios(steps):
    for a, b in [(a, b) for a, b in product(range(9), repeat=2) if a+b]+[(1, 1 << 2048), (1 << 2048, 1)]:
        record = audit.cordic_digits(a, b, steps)
        angle = sum((-1 if digit else 1)*math.atan(math.ldexp(1., -i)) for i, digit in enumerate(record["digits"]))
        expected = math.atan2(math.sqrt(Fraction(b, a+b)), math.sqrt(Fraction(a, a+b)))
        assert abs(angle-expected) <= float(Fraction(record["ideal_real_angle_error_upper"]))+2e-15
        p, q, norm_squared = 1, 0, 1
        for i, row in enumerate(record["trace"]):
            sigma = -1 if row["digit"] else 1
            p, q = (p << i)-sigma*q, (q << i)+sigma*p
            norm_squared *= (1 << (2*i))+1
            assert (p, q) == (int(row["p"]), int(row["q"]))
            assert p*p+q*q == norm_squared
            assert max(abs(p).bit_length(), abs(q).bit_length()) < record["signed_coefficient_width_sufficient"]
        assert not record["digit_generation_reversible_circuit_compiled"]


@pytest.mark.parametrize("pair", ((0, 1), (0, 2)))
def test_actual_digit_controlled_rotations_match_all_blocks_in_complex_superposition(pair):
    steps = 3
    circuit = audit.rotation_program(steps, pair)
    rng = np.random.default_rng(218)
    source = rng.normal(size=1 << circuit.num_qubits)+1j*rng.normal(size=1 << circuit.num_qubits)
    source /= np.linalg.norm(source)
    expected = source.copy()
    for digits in range(1 << steps):
        for enabled in range(2):
            record = {"enabled": enabled, "digits": [digits >> i & 1 for i in range(steps)]}
            indices = [digits+(enabled << steps)+(data << (steps+1)) for data in range(4)]
            matrix = np.eye(4)
            matrix[:3, :3] = audit.rotation_matrix(record, pair)
            expected[indices] = matrix @ source[indices]
    actual = Statevector(source).evolve(circuit)
    assert np.allclose(actual.data, expected, atol=1e-12)
    assert np.allclose(actual.evolve(circuit.inverse()).data, source, atol=1e-12)


@pytest.mark.parametrize("steps", (4, 12, 24))
def test_two_givens_uniform_operator_error_and_physical_phase_covariance(steps):
    for weights in ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), (0, 1, 1), (1, 2, 8), (1, 1 << 1024, 1)):
        matrix, records = audit.compression_reference(weights, steps)
        assert np.allclose(matrix.conj().T @ matrix, np.eye(3), atol=1e-12)
        if not sum(weights):
            assert np.array_equal(matrix, np.eye(3))
            assert not any(r["enabled"] for r in records)
            continue
        vector = np.array([math.sqrt(Fraction(w, sum(weights))) for w in weights])
        first_angle = math.atan2(vector[1], vector[0])
        second_angle = math.atan2(vector[2], math.hypot(vector[0], vector[1]))
        first, second = np.eye(3), np.eye(3)
        for target, angle, endpoint in ((first, first_angle, 1), (second, second_angle, 2)):
            target[0, 0] = target[endpoint, endpoint] = math.cos(angle)
            target[0, endpoint], target[endpoint, 0] = math.sin(angle), -math.sin(angle)
        assert np.linalg.norm(matrix-second @ first, ord=2) <= 4/(1 << steps)+2e-14
        for phase in (1, local.OMEGA, local.OMEGA**2):
            assert np.linalg.norm(matrix @ (phase*vector)-np.array([phase, 0, 0])) <= 4/(1 << steps)+2e-14


def test_precision_budget_counts_full_program_not_number_of_herald_branches():
    record = audit.precision_budget(10**12, "1/1000", source_error="1/10000", gate_synthesis_error="1/10000")
    assert Fraction(record["total_output_TV_perturbation_upper"]) <= Fraction(1, 1000)
    assert record["CORDIC_steps_sufficient"] == 53
    assert record["herald_branches_are_not_summed"]
    assert not record["gate_synthesis_budget_has_been_implemented"]
    with pytest.raises(ValueError):
        audit.precision_budget(1, "1/100", source_error="1/100")


def test_invalid_headers_overflow_and_unsupported_encodings_are_rejected():
    for weights in ((1, 2), (1, -1, 1), (1, .5, 1), (True, 1, 0)):
        with pytest.raises(ValueError):
            audit.Header(weights, 10)
    with pytest.raises(ValueError):
        audit.Header((1, 2, 3), 5)
    program = audit.message_program(1, "check")
    with pytest.raises(ValueError):
        program.encode((0, 2, 0), (0, 1, 1))
    with pytest.raises(ValueError):
        program.encode((0, 1, 1), (0, 1, 1), 4)
    with pytest.raises(ValueError):
        audit.rotation_program(4, (1, 2))


def test_live_report_binds_actual_sources_and_does_not_claim_a_full_receiver():
    report = json.loads(audit.REPORT.read_text())
    for path, digest in report["source_sha256"].items():
        assert hashlib.sha256((audit.ROOT/path).read_bytes()).hexdigest() == digest
    assert sum(row["exhaustive_one_bit_inputs_including_unused_selector"] for row in report["exhaustive_gate_checks"]) == 768
    assert report["exact_message_header_circuits_implemented"]
    assert not report["coherent_CORDIC_digit_generation_compiled"]
    assert not report["full_LDPC_receiver_compiled"]
    assert not report["quantum_speedup_or_classical_hardness_established"]
    for row in report["actual_circuit_scaling"]:
        assert row["qubits_including_all_inputs_outputs_and_scratch"] == 14*row["input_weight_width"]+11
        assert row["actual_maximum_X_controls"] <= 4
        assert not row["upstream_herald_history_enumeration_used"]
