from fractions import Fraction as F

import numpy as np
import pytest

from mixed_average import (adjacent_mixed_control, decode_reference, dependency,
                           marginal, packet_reference, source_plan)


def plan(**updates):
    args = dict(p=131, nilpotency_class=3, rank_cap=3, twirl_gap=F(1, 4), error=F(1, 32),
                receiver_leaves=8, design_size=24, cover_order_bits=32)
    args.update(updates)
    return source_plan(**args)


@pytest.mark.parametrize("spectrum", [(F(1), 0), (F(3, 4), F(1, 4)),
    (F(1, 2), F(1, 4), F(1, 4)), (1-F(1, 2**100), F(1, 2**100), 0)])
def test_decoder_recovers_rounded_state_including_degeneracy_and_discarded_tail(spectrum):
    d = len(spectrum)
    rng = np.random.default_rng(25+d)
    frame, _ = np.linalg.qr(rng.normal(size=(d, d))+1j*rng.normal(size=(d, d)))
    ref = packet_reference(spectrum, frame)
    output = decode_reference(ref["packet"], d, ref["ranks"], ref["weights"])
    assert np.linalg.norm(output-ref["rounded_density"]/float(ref["mass"])) < 1e-12
    assert np.trace(ref["packet"]).real == pytest.approx(1)
    assert ref["loss"] <= F(1, 256)


def test_covariance_for_arbitrary_entangled_density_not_just_prepared_packet():
    rng = np.random.default_rng(251025)
    d, registers = 3, 3
    z = rng.normal(size=(d**registers, 7))+1j*rng.normal(size=(d**registers, 7))
    sigma = z@z.conj().T
    sigma /= np.trace(sigma)
    ranks, weights = (1, 2), (F(2, 5), F(3, 5))
    decoded = decode_reference(sigma, d, ranks, weights)
    primitive = dependency("coarse").support_module()
    for _ in range(8):
        U, _ = np.linalg.qr(rng.normal(size=(d, d))+1j*rng.normal(size=(d, d)))
        action = primitive.tensor_power(U, registers)
        out = decode_reference(action@sigma@action.conj().T, d, ranks, weights)
        assert np.linalg.norm(out-U@decoded@U.conj().T) < 1e-12
    assert np.trace(decoded).real == pytest.approx(1)
    assert min(np.linalg.eigvalsh(decoded)) > 0


@pytest.mark.parametrize("p", [131, 257])
def test_mixed_average_promise_is_not_pointwise_promise(p):
    ref = adjacent_mixed_control(p)
    assert ref["old_minimum_pointwise_distance"] < .013
    assert ref["packet_twirl_fidelity"] == pytest.approx(3/8)
    assert ref["packet_twirl_distance"] >= ref["decoded_twirl_distance"]-1e-12
    assert ref["decoded_twirl_distance"] >= float(F(ref["transferred_lower_bound"]))-1e-12
    for name in ["pointwise_formula_error", "mixed_twirl_formula_error", "decode_identity_error", "twirl_covariance_error"]:
        assert ref[name] < 1e-12
    assert ref["classically_easy_calibration_not_algorithm_candidate"]


def test_false_twirl_promise_can_still_enlarge_stabilizer():
    tiny = F(1, 2**100)
    ref = packet_reference((F(1, 2)-tiny, F(1, 2)+tiny), np.eye(2), delta=F(1, 4))
    rounded = ref["rounded_density"]
    H = np.array([[1, 1], [1, -1]])/np.sqrt(2)
    U = H@np.diag([1, np.exp(2j*np.pi/131)])@H
    assert np.linalg.norm(U@rounded@U.conj().T-rounded) < 1e-12
    # Exact spectrum distinguishes the rays, even below floating precision.
    assert 0 < tiny < F(1, 4)
    assert ref["ranks"] == (2,)


def test_whole_support_wedge_cannot_decode_unequal_spectral_weights():
    primitive = dependency("coarse").support_module()
    whole = primitive.wedge_vector(np.eye(2))
    output = decode_reference(np.outer(whole, whole.conj()), 2, (2,), (F(1),))
    assert np.linalg.norm(output-np.eye(2)/2) < 1e-12
    assert primitive.trace_distance(output, np.diag([.75, .25])) == pytest.approx(.25)


def test_changing_grid_between_moment_factors_can_break_exact_symmetry():
    p = 131
    omega = np.exp(2j*np.pi/p)
    # One grid retains only eigenray 1; another also retains eigenray 2.
    # The mixed density is diagonal, hence every group element fixes it.
    matched = omega * omega**(p-1)
    mismatched = omega * (omega**3)**(p-1)
    assert abs(matched-1) < 1e-12
    assert abs(mismatched-1) > .01
    coarse = dependency("coarse")
    grid = coarse.grid_plan(2, F(1, 16), F(1, 32))
    tiny = 3*grid["bin_width"]/2
    a = coarse.coarsen_reference((1-tiny, tiny), grid, 0)
    b = coarse.coarsen_reference((1-tiny, tiny), grid, 3*grid["grid_choices"]//4)
    assert (a["retained_rank"], b["retained_rank"]) == (2, 1)


@pytest.mark.parametrize("rank,gap", [(1, F(1, 2)), (7, F(1, 7)), (31, F(1, 100))])
def test_complete_resource_ledger_recomputed_with_weaker_promise(rank, gap):
    out = plan(rank_cap=rank, twirl_gap=gap)
    eps = out["error"]
    assert out["coarsening_trace_norm_upper"] == gap/64
    assert out["pure_packet_twirl_gap_lower"] == gap/2
    assert out["charged_amplification_gap_lower"] == gap*gap/128
    assert out["curve_overlap_gap_lower"] == gap*gap/64
    assert out["random_scale_count"]*24 == out["independent_packet_cap"]
    assert out["random_scale_count"]*F(1, 2**out["random_scale_trial_cap"]) <= eps/32
    assert out["original_controlled_action_cap"]*out["original_action_error_per_call"] == eps/32
    assert out["growth_measurement_cap"]*out["growth_instrument_error_per_call"] == eps/32
    assert out["raw_copy_cap"] == out["spectral_attempt_cap"]*(1+sum(out["program_copies_per_bit"]))
    assert out["total_allocated_error_upper"] == 29*eps/32 < eps
    assert out["grid_reused_across_all_sources"]
    assert out["fresh_scale_per_moment_packet_required"]
    for key in ["orbit_gap", "off_group_projector_operator_gap_lower", "ray_gap_lower"]:
        assert key not in out
    for key in ["pointwise_orbit_gap_required", "total_gate_cost_certified", "quantum_execution",
                "accepted_speedup_candidate", "independent_review_of_this_composition"]:
        assert out[key] is False


@pytest.mark.parametrize("update", [dict(p=127), dict(p=133), dict(nilpotency_class=4),
    dict(nilpotency_class=True), dict(rank_cap=0), dict(twirl_gap=.25), dict(twirl_gap=0),
    dict(error=1), dict(error=True), dict(receiver_leaves=0)])
def test_invalid_or_unproved_parameters_rejected(update):
    with pytest.raises(ValueError):
        plan(**update)


def test_reference_guards():
    with pytest.raises(ValueError):
        marginal(np.eye(512), 2, 9, 0)
    with pytest.raises(ValueError):
        decode_reference(np.eye(2), 2, (1,), (F(1, 2),))
    with pytest.raises(ValueError):
        decode_reference(np.eye(2), 2, (True,), (F(1),))
    with pytest.raises(ValueError):
        packet_reference((F(1, 2), F(1, 2)), np.zeros((2, 2)))
