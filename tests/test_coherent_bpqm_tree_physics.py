"""BPQM projectors checked against independent density matrices and whole laws."""
from fractions import Fraction
import json

import numpy as np
import pytest
from qiskit import transpile
from qiskit.quantum_info import Operator

from theorems.bpqm_gibbs_frontier import exact_gibbs
from theorems.coherent_bpqm_tree import REPORT, TreeCompilationLimit, root_program, run_controls
from theorems.coherent_local_gibbs import (
    CodeProblem, decoder_word_errors, finite_readout, readout_circuit,
)


def actual_code_states(problem, c):
    gamma = (1-np.sqrt(1-float(c)**2))/2
    columns = []
    for word in range(1 << len(problem.structure[0])):
        encoded = problem.encode(word)
        columns.append([np.sqrt(gamma**((x ^ encoded).bit_count())*(1-gamma)**(problem.length-(x ^ encoded).bit_count()))
                        for x in range(1 << problem.length)])
    return np.array(columns).T


def observable(problem, c, root, *, depth=None):
    U = Operator(root_program(problem, c, root, depth=depth)[0]).data
    signs = 1-2*((np.arange(1 << problem.length) >> root) & 1)
    return U.conj().T@(signs[:, None]*U)


@pytest.mark.parametrize("problem", [CodeProblem(3, (7,)), CodeProblem(5, (7, 28)),
                                      CodeProblem(4, (3, 6, 12)), CodeProblem(5, (7, 24))])
@pytest.mark.parametrize("c", ["0", "13/20", "4/5"])
def test_full_tree_root_measurement_reaches_independent_helstrom_optimum(problem, c):
    c = Fraction(c)
    states = actual_code_states(problem, c)
    K = states.shape[1]
    for i, root in enumerate(problem.structure[1]):
        bit_signs = 1-2*((np.arange(K) >> i) & 1)
        delta = (states*bit_signs)@states.T*2/K
        O = observable(problem, c, root)
        actual_error = .5-np.trace(O@delta).real/4
        optimum = .5-sum(abs(np.linalg.eigvalsh(delta)))/4
        assert actual_error == pytest.approx(optimum, abs=3e-12)
        assert np.max(abs(O@O-np.eye(1 << problem.length))) < 4e-12


def test_full_tree_information_projectors_preserve_and_commute_on_actual_orbit_span():
    problem = CodeProblem(5, (7, 28))
    c = Fraction(13, 20)
    basis, _ = np.linalg.qr(actual_code_states(problem, c))
    span_projector = basis@basis.T
    observables = [observable(problem, c, root) for root in problem.structure[1]]
    for left in observables:
        assert np.linalg.norm((np.eye(32)-span_projector)@left@basis) < 5e-12
        for right in observables:
            assert np.linalg.norm((left@right-right@left)@basis) < 5e-12


def test_depth_truncation_does_not_inherit_exact_global_projectors():
    problem = CodeProblem(5, (7, 28))
    basis, _ = np.linalg.qr(actual_code_states(problem, Fraction(13, 20)))
    O = observable(problem, "13/20", problem.structure[1][0], depth=1)
    assert np.linalg.norm((np.eye(32)-basis@basis.T)@O@basis) > .1
    shallow = finite_readout(problem, "13/20", 13, mode="tree_bpqm", tree_depth=1)
    complete = finite_readout(problem, "13/20", 13, mode="tree_bpqm")
    assert shallow["unconditional_TV_including_abort"] > .1
    assert complete["unconditional_TV_including_abort"] < 1e-11


@pytest.mark.parametrize("reverse", [False, True])
def test_sequential_full_tree_decoder_gives_correct_unconditional_joint_gibbs_law(reverse):
    problem = CodeProblem(5, (7, 28))
    for signs in range(32):
        result = finite_readout(problem, "13/20", signs, mode="tree_bpqm", reverse=reverse)
        expected = exact_gibbs(problem.ising(signs), "13/20")
        assert np.max(abs(np.array(result["spin_probabilities"])-np.array(list(map(float, expected))))) < 2e-11
        assert result["unconditional_TV_including_abort"] < 2e-11
        assert result["data_purity"] == pytest.approx(1, abs=6e-11)
        assert result["postselection_used_for_primary_readout"] is False


def test_exact_sampling_does_not_require_high_word_recovery():
    problem = CodeProblem(5, (7, 28))
    errors = decoder_word_errors(problem, "13/20", mode="tree_bpqm")
    assert errors["average_word_error"] > .1
    result = finite_readout(problem, "13/20", 5, mode="tree_bpqm")
    assert result["unconditional_TV_including_abort"] < 2e-11


def test_parity_heralds_and_gate_tables_are_explicit_paid_and_not_measured():
    problem = CodeProblem(5, (7, 28))
    circuit, ledger = root_program(problem, "13/20", 2)
    assert sorted(ledger["distinct_original_channels_used"]) == list(range(5))
    assert len(ledger["retained_parity_herald_qubits"]) == 2
    assert ledger["explicit_herald_table_entries"] == 4
    assert ledger["internal_heralds_measured_or_reset"] is False
    assert ledger["unknown_channel_output_cloning_used"] is False
    assert ledger["explicit_herald_tables_can_be_exponential"] is True
    assert ledger["efficient_approximate_reliability_register_implemented"] is False
    assert set(circuit.count_ops()) <= {"u", "cx"}
    # Cached programs must not be corrupted by a caller's mutable result.
    circuit.x(0)
    ledger["distinct_original_channels_used"].clear()
    fresh, restored = root_program(problem, "13/20", 2)
    assert "x" not in fresh.count_ops()
    assert restored["distinct_original_channels_used"] == list(range(5))


def test_actual_tree_source_measurements_and_adjoints_are_all_charged():
    circuit, ledger = readout_circuit(CodeProblem(5, (7, 28)), "13/20", 13, mode="tree_bpqm")
    compiled = transpile(circuit, basis_gates=["u", "cx"], optimization_level=0)
    assert int(compiled.count_ops().get("u", 0)) == ledger["total_executed_one_qubit_gates"]
    assert int(compiled.count_ops().get("cx", 0)) == ledger["total_executed_CNOTs"]
    assert len(ledger["tree_root_programs"]) == 3
    assert ledger["global_mass_table_entries_materialized"] == 0


def test_cycles_cannot_be_unrolled_by_cloning_and_shallow_actual_trees_are_legal():
    problem = CodeProblem(6, (7, 28, 49))
    with pytest.raises(TreeCompilationLimit, match="UNKNOWN"):
        root_program(problem, "13/20", 0)
    circuit, ledger = root_program(problem, "13/20", 0, depth=1)
    assert circuit.num_qubits == 6
    assert len(ledger["distinct_original_channels_used"]) == 5
    assert ledger["unknown_channel_output_cloning_used"] is False
    for signs in (0, 17):
        result = finite_readout(problem, "13/20", signs, mode="tree_bpqm", tree_depth=1)
        assert result["support_leakage_probability_included_not_discarded"] < 2e-11
        assert result["unconditional_TV_including_abort"] > .01


def test_unsupported_inputs_are_unknown_not_an_algorithmic_no_go():
    with pytest.raises(TreeCompilationLimit, match="UNKNOWN"):
        root_program(CodeProblem(11, (2047,)), "1/2", 0)
    with pytest.raises(TreeCompilationLimit, match="UNKNOWN"):
        root_program(CodeProblem(3, (1, 7)), "1/2", 1)
    for depth in (True, -1, 1.0):
        with pytest.raises(ValueError):
            root_program(CodeProblem(3, (7,)), "1/2", 0, depth=depth)
    root_program(CodeProblem(3, (7,)), "1/2", 1, depth=1)
    with pytest.raises(ValueError):
        root_program(CodeProblem(3, (7,)), "1/2", True, depth=True)


def test_complete_live_replay_does_not_claim_a_random_graph_speedup():
    report = run_controls()
    assert report == json.loads(REPORT.read_text())
    assert report["accepted_speedup_candidate"] is False
    assert report["random_regular_cyclic_ensemble_executed"] is False
    assert report["classical_tree_Gibbs_sampling_is_already_efficient"] is True
    assert report["explicit_herald_tables_can_be_exponential"] is True
    for row in report["results"]:
        if row["check_depth"] is None:
            assert row["maximum_unconditional_TV"] < 3e-11
