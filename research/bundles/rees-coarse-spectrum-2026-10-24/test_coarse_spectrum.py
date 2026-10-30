from fractions import Fraction as F
from itertools import permutations
import inspect

import numpy as np
import pytest

from coarse_spectrum import (ceil_log2, coarsen_reference, coordinate_wedge_overlap_modulus,
    diagonal_distance, grid_plan, near_degenerate_control, nonflat_growth_control,
    nonnormal_control, rotated_gap_control, source_plan, support_module)


@pytest.mark.parametrize("rank,gap,eps", [(1, F(1), F(1, 8)), (7, F(1, 7), F(1, 16)),
                                            (31, F(1, 100), F(1, 1024))])
def test_exact_grid_and_coarsening_ledgers(rank, gap, eps):
    p = grid_plan(rank, gap, eps)
    assert p["grid_choices"] & (p["grid_choices"]-1) == 0
    assert p["bad_grid_probability_upper"] <= eps/32
    assert p["coarsening_trace_norm_upper"] == gap/16
    assert p["off_group_projector_operator_gap_lower"] >= gap/2
    assert p["ray_gap_lower"] == gap*gap/8


@pytest.mark.parametrize("values", [(F(1), 0), (F(1, 2), F(1, 4), F(1, 4), 0),
                                      (F(1, 3), F(1, 3), F(1, 3)),
                                      (1-F(1, 2**300), F(1, 2**300))])
def test_exact_coarsening_loss_and_good_grid_classification(values):
    plan = grid_plan(len(values), F(1, 5), F(1, 4))
    for offset in (0, 1, plan["grid_choices"]//4, plan["grid_choices"]-1):
        result = coarsen_reference(values, plan, offset)
        assert all(0 <= rounded <= value for value, rounded in zip(values, result["rounded"]))
        assert result["trace_norm_loss"] <= plan["coarsening_trace_norm_upper"]
        assert 1 <= result["retained_rank"] <= plan["rank_cap"]
        if not result["bad_grid"]:
            for value, label in zip(values, result["labels"]):
                for error in (-plan["boundary_margin"]/2, plan["boundary_margin"]/2):
                    estimate = value+error
                    estimated_label = None if estimate < result["cutoff"] else int((estimate-result["cutoff"])//plan["bin_width"])
                    assert estimated_label == label


def test_discrete_random_grid_bad_mass_exhaustively():
    values = (F(1, 2), F(1, 3), F(1, 6))
    plan = grid_plan(3, F(1, 2), F(1))
    bad = sum(coarsen_reference(values, plan, j)["bad_grid"] for j in range(plan["grid_choices"]))
    assert F(bad, plan["grid_choices"]) <= plan["bad_grid_probability_upper"]
    assert bad > 0  # Boundary coincidences are charged, not assumed away.


def test_full_stabilizers_preserved_for_all_reference_permutations():
    values = (F(1, 2), F(1, 4), F(1, 4), F(0))
    group = tuple(permutations(range(4)))
    delta = min(diagonal_distance(values, g) for g in group if diagonal_distance(values, g))
    plan = grid_plan(3, delta, F(1, 4))
    for offset in (0, 11, plan["grid_choices"]//3):
        coarse = coarsen_reference(values, plan, offset)
        for g in group:
            inside = diagonal_distance(values, g) == 0
            assert (diagonal_distance(coarse["rounded"], g) == 0) == inside
            assert bool(coordinate_wedge_overlap_modulus(coarse["bins"], g)) == inside
            if not inside:
                assert diagonal_distance(coarse["rounded"], g) >= delta-plan["coarsening_trace_norm_upper"]


def test_tiny_original_weights_and_splittings_do_not_set_cost():
    result = near_degenerate_control()
    assert result["minimum_positive_weight"] == F(1, 2**300)
    assert result["explicit_tiny_splitting"] < F(1, 2**200)
    assert min(result["actual_nonidentity_distances"]) >= result["promised_global_gap"]
    assert result["retained_rank"] == 6
    assert sorted(result["retained_bin_ranks"]) == [1, 1, 4]
    assert result["trace_norm_loss"] <= result["coarsening_bound"]
    assert result["good_grid"] and result["original_and_coarse_stabilizers_equal"]
    assert result["packet_outside_overlap_moduli"] == (0, 0)
    assert result["whole_support_wedge_outside_overlap_modulus"] == 1
    assert result["classically_easy_reference_not_application"]


def test_nonnormal_hidden_group_not_only_core():
    result = nonnormal_control()
    assert result["hidden_order"] == 3 and result["normal_core_order"] == 1
    assert result["minimum_outside_trace_distance"] >= F(1, 5)
    assert result["matches_expected_subgroup"]
    assert result["original_coarse_and_packet_subgroups_equal"]


def test_false_global_gap_really_can_add_spurious_symmetry():
    tiny = F(1, 2**100)
    values = (F(1, 2)-tiny, F(1, 2)+tiny)
    plan = grid_plan(2, F(1, 2), F(1, 16))  # Deliberately false promise.
    coarse = coarsen_reference(values, plan, plan["grid_choices"]//4)
    assert diagonal_distance(values, (1, 0)) == 2*tiny < plan["orbit_gap"]
    assert diagonal_distance(coarse["rounded"], (1, 0)) == 0
    assert plan["global_gap_and_rank_are_promises_not_certified"]


def test_degenerate_internal_rotations_preserved_without_choosing_eigenrays():
    primitive = support_module()
    angle = 2*np.pi/3
    U = np.eye(4, dtype=complex)
    U[1:3, 1:3] = [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]]
    rho = np.diag([.5, .25, .25, 0])
    assert np.linalg.norm(U@rho@U.conj().T-rho) < 1e-12
    frame = np.eye(4)[:, 1:3]
    omega = primitive.wedge_vector(frame)
    assert abs(np.vdot(omega, np.kron(U, U)@omega)) == pytest.approx(1)
    assert abs(U[1, 1]) < .6  # A chosen-eigenray method would reject it.


def test_wedge_phase_is_not_silently_called_an_exact_stabilizer():
    omega = np.exp(2j*np.pi/3)
    U = np.diag([omega, 1, 1])
    frame = np.eye(3)[:, :2]
    determinant = np.linalg.det(frame.conj().T@U@frame)
    assert abs(determinant) == pytest.approx(1)
    assert abs(determinant-1) > 1
    assert determinant**3 == pytest.approx(1)  # Finite character cancellation control.


def test_fine_spectral_measurement_is_not_a_coarse_projector_channel():
    coherent = np.ones((2, 2))/2
    fine = np.diag(np.diag(coherent))
    coarse = coherent  # Both eigenvectors belong to one retained bin.
    distance = np.abs(np.linalg.eigvalsh(fine-coarse)).sum()/2
    assert distance == pytest.approx(.5)
    rho_target = np.diag([.5001, .4999])
    assert np.array_equal(rho_target, np.diag(np.diag(rho_target)))


def test_nonflat_history_growth_and_rank_saturation():
    result = nonflat_growth_control()
    for row in result["rows"]:
        assert row["success_probability"] >= float(row["proven_lower"])-1e-12
    assert result["failure_sector_leakage"] < 1e-12
    assert result["full_wedge_trace_error"] < 1e-12
    assert abs(result["beyond_true_rank_success"]) < 1e-12


def test_nonflat_growth_lower_bound_can_be_tight():
    primitive = support_module()
    rho = np.diag([.5, 1/3, 1/6])
    vector = primitive.wedge_vector(np.eye(3)[:, :2])
    retained = np.outer(vector, vector.conj())
    success, _, _, _ = primitive.growth_instrument(3, 2)
    probability = np.trace(success@np.kron(retained, rho)@success.conj().T).real
    assert probability == pytest.approx(1/18)


def test_nondiagonal_projector_and_determinant_gap_transfer():
    result = rotated_gap_control()
    delta = float(result["promised_gap_in_this_fixture"])
    for row in result["rows"]:
        assert row["original_trace_distance"] >= delta
        assert row["coarse_trace_distance"] >= delta-float(result["coarsening_bound"])
        assert row["coarse_trace_distance"] <= row["maximum_projector_gap"]+1e-12
        assert 0 < row["packet_overlap_modulus"] < np.sqrt(1-delta**2/4)


@pytest.mark.parametrize("R,delta,eps", [(1, F(1, 2), F(1, 8)), (7, F(1, 7), F(1, 32)), (32, F(1, 100), F(1, 64))])
def test_complete_resource_schedule(R, delta, eps):
    p = source_plan(rank_cap=R, orbit_gap=delta, error=eps, receiver_leaves=8, design_size=6, cover_order_bits=16)
    assert p["growth_attempts_per_stage"]*p["bin_width"]/(R+1) >= ceil_log2(32*p["growth_stage_cap"]/eps)
    assert p["spectral_attempts_per_fetch"]*p["bin_width"] >= ceil_log2(32*p["filtered_target_requests"]/eps)
    assert p["qpe_grid"] >= 256/(p["boundary_margin"]*p["spectral_bad_estimate_budget_per_attempt"])
    t = p["qpe_bits"]
    assert sum(F(8*4**b, N) for b, N in enumerate(p["program_copies_per_bit"])) <= p["dme_half_diamond_budget_per_attempt"]
    assert p["raw_copy_cap"] == p["spectral_attempt_cap"]*(1+sum(p["program_copies_per_bit"]))
    assert p["growth_measurement_cap"]*p["growth_instrument_error_per_call"] == eps/32
    assert p["original_controlled_action_cap"]*p["original_action_error_per_call"] == eps/32
    assert p["total_allocated_error_upper"] == eps*F(7, 8)
    assert t > 0 and not p["quantum_execution"] and not p["accepted_speedup_candidate"]


def test_planner_has_no_spectrum_or_exact_rank_parameter():
    parameters = inspect.signature(source_plan).parameters
    assert not any(key in parameters for key in ["spectrum", "eigenbasis", "rank", "minimum_weight", "spectral_gap"])


@pytest.mark.parametrize("rank,gap,eps", [(0, F(1), F(1)), (True, F(1), F(1)),
    (2, 0, F(1)), (2, F(3, 2), F(1)), (2, .5, F(1)), (2, F(1), 0)])
def test_bad_promises_rejected(rank, gap, eps):
    with pytest.raises(ValueError):
        grid_plan(rank, gap, eps)


def test_reference_rejects_rank_and_grid_violations():
    p = grid_plan(1, F(1), F(1, 8))
    for values, index in [((F(1, 2), F(1, 2)), 0), ((F(-1), F(2)), 0),
                          ((F(1, 2),), 0), ((1.,), 0), ((F(1),), -1), ((F(1),), p["grid_choices"])]:
        with pytest.raises(ValueError):
            coarsen_reference(values, p, index)


def test_live_receipt_hashes_and_non_admission_guards():
    import hashlib
    import importlib.util
    import json
    from pathlib import Path

    root = Path(__file__).resolve().parent
    spec = importlib.util.spec_from_file_location("coarse_audit_receipt", root/"run_audit.py")
    audit = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(audit)
    result = audit.receipt()
    json.dumps(result, default=audit.encode)
    assert all(hashlib.sha256((root/name).read_bytes()).hexdigest() == digest for name, digest in result["sha256"].items())
    assert all(hashlib.sha256((root.parent/name).read_bytes()).hexdigest() == digest for name, digest in result["dependency_sha256"].items())
    assert not result["quantum_algorithm_executed"]
    assert not result["novelty_established"]
    assert not result["accepted_speedup_candidate"]
