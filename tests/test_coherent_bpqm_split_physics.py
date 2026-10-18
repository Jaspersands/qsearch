"""Actual ENU isometry, native correlations and retained-workspace checks."""
from fractions import Fraction
import json
import math

import numpy as np
import pytest
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Operator, Statevector

from theorems.bpqm_gibbs_frontier import exact_gibbs
from theorems.coherent_bpqm_split import (
    REPORT, run_controls, split_decoder, split_root, splitter, unroll, weakened_overlaps,
)
from theorems.coherent_bpqm_tree import TreeCompilationLimit, root_program
from theorems.coherent_local_gibbs import (
    CodeProblem, finite_readout, readout_circuit,
)


def channel(c, bit):
    return np.array([math.sqrt(float((1+c)/2)), (-1)**bit*math.sqrt(float((1-c)/2))])


@pytest.mark.parametrize("a,b", [("0", "0"), ("0", "3/4"), ("1", "3/4"),
                                 ("3/4", "3/4"), ("7/8", "15/16")])
def test_splitter_is_a_coherent_gram_preserving_isometry_not_same_quality_cloning(a, b):
    a, b = Fraction(a), Fraction(b)
    S = Operator(splitter(a, b)).data
    inputs, targets = [], []
    for bit in (0, 1):
        before = np.kron(np.array([1., 0.]), channel(a*b, bit))
        after = np.kron(channel(b, bit), channel(a, bit))
        assert np.max(abs(S@before-after)) < 3e-14
        inputs.append(before)
        targets.append(after)
    assert np.vdot(targets[0], targets[1]) == pytest.approx(float(a*b))
    # A coherent relative phase cannot be changed independently for each bit.
    superposition = inputs[0]+1j*inputs[1]
    expected = targets[0]+1j*targets[1]
    assert np.max(abs(S@superposition-expected)) < 4e-14
    Z0 = np.diag([1., -1., 1., -1.])
    Z0Z1 = np.diag([1., -1., -1., 1.])
    assert np.max(abs(S@Z0-Z0Z1@S)) < 4e-14


@pytest.mark.parametrize("c", ["0", "1/1000", "1/5", "13/20", "9999999999999999/10000000000000000"])
def test_rational_split_conserves_original_overlap_for_every_multiplicity(c):
    for count in range(1, 11):
        children = weakened_overlaps(c, count)
        assert math.prod(children) == Fraction(c)
        assert len(children) == count
        assert all(Fraction(c) <= x <= 1 for x in children)
    if c == "13/20":
        children = weakened_overlaps(c, 3)
        assert all(x > Fraction(c) for x in children)


@pytest.mark.parametrize("depth", [0, 1, 2])
def test_native_codeword_lifts_satisfy_all_unrolled_tree_checks(depth):
    problem = CodeProblem(4, (7, 13))
    for root in problem.structure[1]:
        origins, checks = unroll(problem, root, depth)
        for information in range(4):
            encoded = problem.encode(information)
            lifted = sum(((encoded >> v) & 1) << i for i, v in enumerate(origins))
            assert all((lifted & h).bit_count() % 2 == 0 for h in checks)


def test_depth_one_unrolling_uses_one_paid_weaker_pair_and_native_correlations():
    problem = CodeProblem(4, (7, 13))
    circuit, ledger = split_root(problem, "13/20", 2, depth=1)
    assert circuit.num_qubits == 5
    assert ledger["additional_split_qubits"] == 1
    assert ledger["unrolled_variable_origins"].count(0) == 2
    assert ledger["arbitrary_unknown_state_cloning_used"] is False
    assert ledger["new_native_source_calls"] == 0
    assert ledger["unrolled_independence_is_not_the_native_joint_law"] is True
    assert set(circuit.count_ops()) <= {"u", "cx"}


@pytest.mark.parametrize("depth", [1, 2])
def test_actual_split_native_codewords_match_correlated_lifted_tree_states(depth):
    problem, c = CodeProblem(4, (7, 13)), Fraction(13, 20)
    gamma = (1-math.sqrt(1-float(c)**2))/2
    for root in problem.structure[1]:
        native_U, ledger = split_root(problem, c, root, depth=depth)
        origins = ledger["unrolled_variable_origins"]
        overlaps = [None]*len(origins)
        for allocation in ledger["split_allocations"]:
            for i, value in zip(allocation["occurrences"], allocation["weaker_overlaps"]):
                overlaps[i] = Fraction(value)
        tree = CodeProblem(len(origins), tuple(ledger["unrolled_check_masks"]))
        tree_U, _ = root_program(tree, c, 0, overlaps=tuple(overlaps), fourier_input=True)
        for word in range(4):
            encoded = problem.encode(word)
            actual = QuantumCircuit(native_U.num_qubits)
            for i in range(4):
                actual.ry(2*math.asin(math.sqrt(gamma)), i)
                if (encoded >> i) & 1:
                    actual.x(i)
            actual.compose(native_U, inplace=True)
            native_law = Statevector.from_instruction(actual).probabilities([root])
            lifted = np.array([1.])
            for i in reversed(range(len(origins))):
                lifted = np.kron(lifted, channel(overlaps[i], (encoded >> origins[i]) & 1))
            tree_law = Statevector(lifted).evolve(tree_U).probabilities([0])
            assert np.max(abs(native_law-tree_law)) < 4e-12


def test_every_root_receives_private_workspace_not_an_assumed_clean_reused_pool():
    decoder, ledger = split_decoder(CodeProblem(4, (7, 13)), "13/20", depth=2)
    roots = ledger["tree_root_programs"]
    spaces = [set(row["private_split_workspace_in_decoder"]) for row in roots]
    assert [len(s) for s in spaces] == [5, 3]
    assert spaces[0].isdisjoint(spaces[1])
    assert ledger["additional_split_qubits"] == 8
    assert decoder.num_qubits == 14


def test_retained_clone_workspace_is_not_zero_after_the_complete_readout():
    result = finite_readout(CodeProblem(4, (7, 13)), "13/20", 0,
                            mode="split_tree_bpqm", tree_depth=1)
    assert .99 < result["split_workspace_zero_probability"] < .999
    assert result["unconditional_TV_including_abort"] > .1
    assert result["work_register_reset_assumed"] is False
    assert result["postselection_used_for_primary_readout"] is False
    assert result["support_leakage_probability_included_not_discarded"] < 1e-11


def test_actual_gate_and_all_original_label_record_and_split_wire_counts_are_paid():
    circuit, ledger = readout_circuit(CodeProblem(4, (7, 13)), "13/20", 5,
                                      mode="split_tree_bpqm", tree_depth=1)
    compiled = transpile(circuit, basis_gates=["u", "cx"], optimization_level=0)
    assert circuit.num_qubits == ledger["qubits_with_source_label_and_work"] == 9
    assert int(compiled.count_ops().get("u", 0)) == ledger["total_executed_one_qubit_gates"]
    assert int(compiled.count_ops().get("cx", 0)) == ledger["total_executed_CNOTs"]
    assert ledger["additional_split_qubits"] == 1
    assert ledger["each_root_has_private_unreset_split_workspace"] is True


def test_depth_zero_is_the_original_linear_baseline_not_a_new_source():
    problem = CodeProblem(4, (7, 13))
    for signs in range(16):
        linear = finite_readout(problem, "13/20", signs, mode="linear")
        split = finite_readout(problem, "13/20", signs, mode="split_tree_bpqm", tree_depth=0)
        assert np.max(abs(np.array(linear["spin_probabilities"])-np.array(split["spin_probabilities"]))) < 2e-12
        assert split["resource_ledger"]["additional_split_qubits"] == 0


def test_caps_and_bad_inputs_are_not_promoted_to_native_hardness():
    for bad in (True, 1., -1, 1):
        with pytest.raises(ValueError):
            weakened_overlaps(bad, 2)
    for bad in (True, -1, 4):
        with pytest.raises(ValueError):
            split_decoder(CodeProblem(4, (7, 13)), "13/20", depth=bad)
    with pytest.raises(TreeCompilationLimit, match="UNKNOWN"):
        split_root(CodeProblem(6, (7, 25, 42, 52)), "13/20", 0, depth=2)


def test_live_native_artifact_keeps_all_signs_and_exact_classical_targets():
    artifact = json.loads(REPORT.read_text())
    assert artifact == run_controls()
    assert artifact["native_sampling_family_classically_difficult"] is False
    assert artifact["accepted_speedup_candidate"] is False
    assert len(artifact["results"]) == 6
    assert len(artifact["classical_native_targets"]) == 32
    problem = CodeProblem(4, (7, 13))
    for row in artifact["classical_native_targets"]:
        expected = exact_gibbs(problem.ising(int(row["sign_mask_hex"], 16)), row["overlap_c_exact"])
        assert list(map(Fraction, row["exact_native_spin_probabilities"])) == list(expected)
    for row in artifact["results"]:
        assert row["native_Tanner_graph_is_cyclic"] is True
        assert row["all_signs_enumerated_no_favorable_selection"] is True
        assert len(row["all_sign_cases"]) == 16
        word_success = row["word_recovery"]["success_by_actual_codeword"]
        assert max(word_success)-min(word_success) < 1e-10
