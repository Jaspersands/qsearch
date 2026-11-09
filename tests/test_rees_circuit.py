"""Gate-level Rees circuit on Heis(F_3): exact simulation of the compiled modules.

Finite falsifiers on one instance. A pass shows the compiled Qiskit gate lists
reproduce the paper's sources, instrument, merge and readout exactly on every
subgroup of Heis(F_3); it proves nothing about other groups or about cost.
The exhaustive fixture runs one 24-qubit Aer statevector per subgroup (a few
minutes in all).
"""
import numpy as np
import pytest

from theorems.rees_circuit import (
    CHECK_KEYS, P, TOL, STATUS, bch_reference, channel_output, check_instance, cover, hidden_instances,
    merge_aer_check, merge_circuit, merge_permutation, merge_table, paper_counts,
    run_algorithm, simulate_instrument, simulate_source, terminal_sample_circuit, witnesses,
    coset_density, expected_stage_indices,
)
from theorems.rees_end_to_end_sim import rref

INSTANCES = hidden_instances()
BY_NAME = {inst.name: inst for inst in INSTANCES}


def _find(basis):
    target = rref(list(basis), P)
    return next(inst for inst in INSTANCES if rref(inst.log_h, P) == target)


@pytest.fixture(scope="module")
def checks():
    return {inst.name: check_instance(inst) for inst in INSTANCES}


def test_status_does_not_claim_a_coherent_receiver():
    assert STATUS["coherent_receiver_implemented"] is False


def test_instance_is_heis_f3_with_all_19_subgroups():
    cv = cover()
    assert cv.dims == (3, 1) and cv.c == 2 and cv.points == (1, 2)
    assert len(INSTANCES) == 19
    assert sum(not inst.flags()["normal"] for inst in INSTANCES) == 12


@pytest.mark.parametrize("s", [1, 2])
def test_merge_gates_equal_bch_right_translation_with_clean_scratch(s):
    perm, flags = merge_permutation(s)
    assert flags == {"q_never_targeted": True, "q_unchanged": True,
                     "scratch_clean_all_inputs": True, "x_canonical": True}
    assert (perm == bch_reference(s)).all()          # x -> x * (-delta_s(sigma(q))) on all 27 x 81 inputs


@pytest.mark.parametrize("s", [1, 2])
def test_merge_aer_statevector_matches_bit_level_evaluation(s):
    rng = np.random.default_rng(11+s)
    psi = rng.normal(size=81)+1j*rng.normal(size=81)
    psi /= np.linalg.norm(psi)
    q_density, scratch_zero = merge_aer_check(psi, s)
    assert abs(scratch_zero-1) < TOL
    assert np.abs(q_density-channel_output([np.outer(psi, psi.conj())], (s,))).max() < 1e-8


def test_every_subgroup_exhaustively(checks):
    for name, c in checks.items():
        assert c["passed"], c
        assert all(c[k] is True for k in CHECK_KEYS), name
        assert c["source_padding_weight"] < TOL and c["instrument_padding_weight"] < TOL
        assert c["branch_witness_cases"] > 0
    assert sum(c["branch_witness_cases"] for c in checks.values()) == 3198


def test_non_normal_subgroups_are_covered(checks):
    non_normal = [c for c in checks.values() if not c["normal"]]
    assert len(non_normal) == 12 and all(c["all_merge_outputs_equal_rho_H1"] for c in non_normal)


@pytest.mark.parametrize("seed", [0, 1])
def test_seeded_runs_recover_log_h_for_every_subgroup(checks, seed):
    for inst in INSTANCES:
        got, queries = run_algorithm(inst, seed=seed)
        assert got == rref(inst.log_h, P), inst.name
        assert queries == 7*3*2                     # 7 samples x M_2 = 3 sources x c = 2 calls


def test_primitive_counts_match_compilation_note():
    _, counts = terminal_sample_circuit(None, (1, 2, 1))
    note = paper_counts(1)
    for key, value in note.items():
        if key == "bracket_evaluations_upper_bound":
            assert counts["bracket_evaluations"] == 12 <= value == 48
        else:
            assert counts[key] == value, key


def test_zero_scale_slot_is_consumed_without_gates():
    _, full = terminal_sample_circuit(None, (1, 1, 1))
    _, partial = terminal_sample_circuit(None, (1, 0, 1))
    assert full["controlled_right_actions"] == 3 and partial["controlled_right_actions"] == 2
    assert partial["bch_passes"] == 8


def test_assembled_circuit_width():
    qc, _ = terminal_sample_circuit(None, (1, 1, 1))
    assert qc.num_qubits == 82
    gates = {inst.operation.name for inst in qc.data}
    assert {"qft3", "qft3_dg", "swap", "measure"} <= gates


def test_negative_control_merge_without_bennett_uncompute_leaves_garbage():
    _, flags = merge_permutation(1, bennett=False)
    assert flags["scratch_clean_all_inputs"] is False


def test_negative_control_non_witness_scales_give_wrong_output():
    inst = _find([(1, 0, 0)])                      # non-normal, meets the centre trivially
    rho, _, _ = simulate_source(inst)
    branches, _ = simulate_instrument(rho)
    target = coset_density(expected_stage_indices(cover(), inst.log_h, 1), 27)
    labels = (1, 1, 1)
    bad = [s for s in [(1, 0, 0), (1, 1, 0)] if s not in witnesses(labels)]
    assert bad
    for s in bad:
        sigma = channel_output([branches[l][1] for l in labels], s)
        assert np.abs(sigma-target).max() > 1e-3


@pytest.mark.parametrize("basis", [[(1, 0, 0)], [(0, 1, 0)]])
def test_exact_source_evaluation_matches_aer_statevector(basis):
    inst = _find(basis)
    exact, work_e, _ = simulate_source(inst)
    aer, work_a, leak = simulate_source(inst, method="aer")
    assert np.abs(exact-aer).max() < 1e-12 and abs(work_e-1) < TOL and abs(work_a-1) < TOL and leak < TOL


@pytest.mark.parametrize("inst", INSTANCES, ids=[i.name for i in INSTANCES])
def test_negative_controls_on_sources(inst):
    z_in_h = bool(inst.log_h) and len(rref(inst.log_h+[(0, 0, 1)], P)) == len(inst.log_h)
    one_point_wrong = not z_in_h
    ref, _, _ = simulate_source(inst)              # verified equal to rho of the lift above
    one, _, _ = simulate_source(inst, points=(1,))
    dirty, work_zero, _ = simulate_source(inst, uncompute=False)
    # prop:single-evaluation: one point is wrong exactly when z is not in h
    assert (np.abs(one-ref).max() > 1e-6) == one_point_wrong
    # keeping the E_s workspace is always seen by the workspace check; it changes the
    # address state exactly when h != 0 (for H = 1 the source is already I/81)
    assert abs(work_zero-1) > 1e-6
    assert (np.abs(dirty-ref).max() > 1e-6) == bool(inst.log_h)
