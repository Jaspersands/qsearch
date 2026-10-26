import hashlib
from itertools import product
import json

import numpy as np
import pytest
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.quantum_info import Statevector

from theorems import ternary_cordic_step as audit
from theorems.ternary_coherent_reliability import (
    apply_basis, apply_sparse, permutation_ops, root_difference_sign,
)


@pytest.mark.parametrize("width", (1, 2, 3))
def test_comparator_matches_exhaustive_unsigned_truth_and_cleans_all_scratch(width):
    a, b, out, diff, carry, cin = (QuantumRegister(n, label) for n, label in
                                 ((width, "a"), (width, "b"), (1, "out"), (width, "diff"), (1, "carry"), (1, "cin")))
    circuit = QuantumCircuit(a, b, out, diff, carry, cin)
    audit.greater_equal(circuit, a, b, out[0], diff, carry[0], cin[0])
    operations = permutation_ops(circuit)
    for x, y, output in product(range(1 << width), range(1 << width), range(2)):
        source = x+(y << width)+(output << (2*width))
        assert apply_basis(operations, source) == (x+(y << width)+((output ^ int(x >= y)) << (2*width)))


@pytest.mark.parametrize("m,w,i", ((2, 1, 0), (2, 2, 1), (3, 2, 2)))
def test_real_signed_decision_update_random_coherent_inputs_zero_terms_and_minimum_integer(m, w, i):
    program = audit.step_program(m, w, i)
    operations = permutation_ops(program.circuit)
    inputs = list(product(range(-(1 << (m-1)), 1 << (m-1)), repeat=2))
    weights = [(0, 0), (0, (1 << w)-1), ((1 << w)-1, 0), (1, (1 << w)-1)]
    source, expected = {}, {}
    for j, ((p, q), (a, b)) in enumerate(product(inputs, weights)):
        original = program.encode(p, q, a, b)
        actual = apply_basis(operations, original)
        sigma = -1 if root_difference_sign(p, q, a, b) < 0 else 1
        assert program.read(actual) == (int(sigma < 0), (p << i)-sigma*q, (q << i)+sigma*p)
        assert not any(actual >> bit & 1 for bit in program.scratch)
        assert apply_basis(operations, actual, inverse=True) == original
        amplitude = complex((-1)**j, (-1)**(j//2))
        source[original], expected[actual] = amplitude, amplitude
    assert apply_sparse(operations, source) == expected
    assert apply_sparse(operations, expected, inverse=True) == source
    predicted = audit.step_size(m, w, i)
    assert len(operations) == predicted["gates"]
    assert program.circuit.num_qubits == predicted["qubits"]
    assert len(program.scratch) == predicted["scratch"]
    assert max(mask.bit_count() for mask, _ in operations) <= 3


def test_sparse_x_rotation_evaluator_matches_independent_dense_arbitrary_control_states_and_inverse():
    from qiskit.circuit.library import RYGate
    circuit = QuantumCircuit(5)
    circuit.x(0)
    circuit.cx(1, 4)
    circuit.ccx(0, 1, 3)
    circuit.append(RYGate(.319).control(2, ctrl_state=1, annotated=False), [1, 3, 2])
    circuit.append(RYGate(-.738).control(1, ctrl_state=0, annotated=False), [4, 0])
    rng = np.random.default_rng(721)
    source = rng.normal(size=32)+1j*rng.normal(size=32)
    source /= np.linalg.norm(source)
    operations = audit.sparse_gate_program(circuit)
    sparse = audit.apply_sparse_gates(operations, dict(enumerate(source)))
    actual = np.array([sparse.get(i, 0) for i in range(32)])
    assert np.allclose(actual, Statevector(source).evolve(circuit).data, atol=1e-12)
    inverse = audit.apply_sparse_gates(operations, sparse, inverse=True)
    assert np.allclose([inverse.get(i, 0) for i in range(32)], source, atol=1e-12)
    circuit.z(0)
    with pytest.raises(ValueError):
        audit.sparse_gate_program(circuit)


@pytest.mark.parametrize("steps,pair", ((1, (0, 1)), (2, (0, 2)), (3, (0, 1)), (4, (0, 2))))
def test_complete_variable_weight_rotation_coherent_control_cleanup_and_total_inverse(steps, pair):
    program = audit.variable_rotation(2, steps, pair)
    record = audit.coherent_control(program)
    assert record["full_state_reference_residual_numeric"] < 1e-12
    assert record["inverse_recovery_residual_numeric"] < 1e-12
    assert record["arithmetic_garbage_probability_numeric"] == 0
    assert len(program.circuit.data) == program.predicted_logical_gates
    assert program.circuit.num_qubits == audit.rotation_size(2, steps)["qubits"]
    assert not record["dense_many_qubit_statevector_or_ideal_arithmetic_oracle_used"]


def test_reference_cap_and_exact_integer_overflow_refuse_before_silent_truncation():
    program = audit.step_program(2, 1, 0)
    for args in ((2, 0, 0, 1), (-3, 0, 0, 1), (1, 0, 2, 1), (1, 0, -1, 1), (True, 0, 0, 1)):
        with pytest.raises(ValueError):
            program.encode(*args)
    with pytest.raises(ValueError, match="reference cap"):
        audit.variable_rotation(10, 64, max_gates=1000)
    with pytest.raises(ValueError):
        audit.variable_rotation(1, 2, (1, 2))


def test_live_source_bound_artifact_contains_real_variable_weight_gates_without_block_claim():
    report = json.loads(audit.REPORT.read_text())
    for path, digest in report["source_sha256"].items():
        assert hashlib.sha256((audit.ROOT/path).read_bytes()).hexdigest() == digest
    assert report["exhaustive_clean_small_input_cases"] == 64
    assert report["whole_CORDIC_history_and_rotation_composition_compiled"]
    assert not report["whole_LDPC_receiver_compiled"]
    assert not report["speedup_claim_allowed"]
    assert report["large_rotation_cost_prediction"]["predicted_logical_gates"] == 5_048_480_990
    assert not report["large_rotation_cost_prediction"]["large_circuit_allocated_or_executed"]
    for row in report["resources"]:
        expected = audit.step_size(row["signed_coefficient_width"], row["weight_width"], row["iteration"])
        assert expected["gates"] == row["actual_controlled_X_gates"]
        assert expected["qubits"] == row["actual_qubits_including_retained_inputs_outputs_and_scratch"]
        assert row["actual_maximum_X_controls"] <= 3
