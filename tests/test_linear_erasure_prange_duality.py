from itertools import product
import json
import math
import random
import subprocess

from flint import fmpq
import numpy as np
import pytest

from linear_erasure_prange_duality import (
    REPORT, AffineFactorInstance, AffineBranch, all_local_spaces, all_affine_spaces, branch_isometry,
    complete_factor_control, four_message_control, four_message_mixture,
    four_message_optimality, frequency_probability, mixture_record, null_basis,
    outside_linear_cone_control, sample_affine_mixture, scaling_bound, span, rank_duality_control,
    validate_mixture,
)


@pytest.mark.parametrize("c", ("1/10", "1/3", "1/2", "2/3", "9/10"))
def test_actual_partial_decoder_cleans_scratch_and_preserves_every_input(c):
    r, p = four_message_control(c), fmpq(c)
    assert r["isometry_error_diagnostic"] < 1e-12
    assert max(r["eight_codeword_output_errors_diagnostic"]) < 1e-12
    assert r["constant_local_input_dimension"] == 16
    assert r["constant_local_output_dimension"] == 96
    joint = fmpq(r["mean_unknown_bits"])
    assert joint == 4*p*p-p**4
    assert joint < fmpq(r["product_USD_parity_mean_unknown_bits"])
    assert joint < fmpq(r["full_block_USD_only_mean_unknown_bits"])
    assert not r["global_coherent_Gibbs_sampler_implemented"]
    assert not r["hardware_synthesis_implemented"]


@pytest.mark.parametrize("c", ("1/3", "1/2", "2/3"))
def test_entire_coherent_prior_is_not_a_bernoulli_codeword_channel(c):
    r = four_message_control(c)
    prior = list(map(fmpq, r["normalized_equal_superposition_branch_probabilities"]))
    weights = [fmpq(b["weight"]) for b in r["mixture"]["branches"]]
    assert sum(prior) == sum(weights) == 1 and prior != weights
    assert np.allclose(list(map(float, prior)), r["coherent_prior_branch_probabilities_diagnostic"], rtol=0, atol=1e-12)
    assert not r["mixture"]["codeword_branch_law_is_universal_coherent_prior_law"]


@pytest.mark.parametrize("c", ("1/3", "1/2"))
@pytest.mark.parametrize("bits", tuple(product(range(2), repeat=4)))
def test_four_spin_elimination_is_the_actual_positive_affine_factor(bits, c):
    p = fmpq(c)
    g = [(-1)**b for b in bits]
    eliminated = sum(math.prod(1+p*z*x for x in g) for z in (-1, 1))/2
    relative = sum((bits[j]^bits[3]) << j for j in range(3))
    factor = 8*frequency_probability(four_message_mixture(c), relative)
    assert factor == eliminated


@pytest.mark.parametrize("c", ("1/10", "1/3", "2/5", "1/2", "2/3", "9/10"))
def test_exact_dual_certifies_optimality_for_all_affine_subspaces_not_all_measurements(c):
    r = four_message_optimality(c)
    assert len(r["all_affine_subspaces"]) == 51
    assert [sum(len(S) == 2**d for S in all_local_spaces(3)) for d in range(4)] == [1, 7, 7, 1]
    assert [sum(len(S) == 2**d for S in all_affine_spaces(3)) for d in range(4)] == [8, 28, 14, 1]
    assert all(fmpq(s["dual_average"]) <= s["unknown_bits"] for s in r["all_affine_subspaces"])
    p = fmpq(c)
    assert r["primal_mean_unknown_bits"] == r["dual_lower_bound"] == str(4*p*p-p**4)
    assert r["optimal_within_positive_affine_subspace_instruments"]
    assert not r["optimal_among_all_quantum_measurements"]


def test_general_two_bit_instrument_and_classical_factor_share_the_same_dimensions():
    branches = (AffineBranch(2, (1, 2), "1/2"), AffineBranch(2, (3,), "1/3"), AffineBranch(2, (), "1/6"))
    T = branch_isometry(branches)
    assert np.linalg.norm(T.T@T-np.eye(4)) < 1e-12
    for d in range(4):
        message = np.array([math.sqrt(float(frequency_probability(branches, y)))*(-1)**((d&y).bit_count()) for y in range(4)])
        expected = np.zeros(12)
        for i, b in enumerate(branches):
            out = sum(((d&v).bit_count() % 2) << j for j, v in enumerate(b.basis))
            expected[4*i+out] = math.sqrt(float(b.weight))
        assert np.linalg.norm(T@message-expected) < 1e-12
    record = mixture_record(branches)
    assert record["mean_unknown_bits"] == "2/3"
    assert all(b["unknown_quantum_bits"] == b["classical_affine_constraints"] for b in record["branches"])


def test_any_positive_channel_has_a_point_mixture_but_it_may_erase_every_logical_bit():
    q = tuple(map(fmpq, ("1/10", "3/10", "3/10", "3/10")))
    branches = validate_mixture(tuple(AffineBranch(2, (), w, y) for y, w in enumerate(q)))
    assert tuple(frequency_probability(branches, y) for y in range(4)) == q
    assert mixture_record(branches)["mean_unknown_bits"] == "2"
    assert np.linalg.norm(branch_isometry(branches).T@branch_isometry(branches)-np.eye(4)) < 1e-12


def test_gf2_annihilator_is_independent_complete_and_not_just_a_coordinate_mask():
    for basis in ((1, 2, 4), (7,), (3, 5), (), (3, 6)):
        annihilator = null_basis(basis, 3)
        assert len(annihilator) == 3-len(basis)
        assert len(span(annihilator)) == 2**len(annihilator)
        assert span(basis) == tuple(x for x in range(8) if all((x&b).bit_count() % 2 == 0 for b in annihilator))


def test_all_full_rank_branches_give_exact_gibbs_law_not_only_a_success_conditioned_law():
    branches = (AffineBranch(2, (1, 2), "1/2"), AffineBranch(2, (3,), "1/3"), AffineBranch(2, (), "1/6"))
    instance = AffineFactorInstance(4, ((1, 2), (4, 8)), (1, 2))
    r = complete_factor_control(instance, branches)
    assert r["bad_mass"] == r["complete_output_TV"] == "0"
    assert r["Gibbs_probabilities"] == r["sampler_probabilities"]
    assert r["tilted_normalization"] == "1"


def test_frustrated_affine_factors_keep_tilts_and_every_fallback():
    instance = AffineFactorInstance(1, ((1, 1, 1), (0, 1, 1)), (1, 3))
    r = complete_factor_control(instance, four_message_mixture("1/2"))
    assert any(not b["solutions"] and b["tilt"] == "0" for b in r["branches"])
    assert any(fmpq(b["tilt"]) > 1 for b in r["branches"])
    assert fmpq(r["bad_mass"]) > 0
    assert sum(map(fmpq, r["sampler_probabilities"])) == 1
    assert fmpq(r["complete_output_TV"]) <= fmpq(r["subset_TV"])+fmpq(r["bad_mass"])
    assert not r["fixed_sign_bound_inferred_from_sign_average"]


@pytest.mark.parametrize("c", ("1/3", "1/2"))
def test_quantum_reconstruction_and_classical_affine_matrices_are_exact_transposes(c):
    instance = AffineFactorInstance(4, ((1, 2, 4), (2, 4, 8)), (1, 6))
    branches = four_message_mixture(c)
    for selected in product(range(6), repeat=2):
        r = rank_duality_control(instance, branches, selected)
        assert r["quantum_reconstruction_columns"] == tuple(a for a, b in r["classical_equation_rows"])
        assert r["unknown_bits"] == sum(3-branches[i].dimension for i in selected)
        assert r["quantum_unique_reconstruction_iff_classical_full_row_rank"]
        assert not r["arbitrary_coherent_prior_success_from_rank_alone"]


def test_rational_scaling_rejects_the_apparent_joint_decoder_advantage():
    r = scaling_bound(4096, 4301, "1/2")
    assert r["matched_quantum_unknown_and_classical_constraint_load"] == "15/16"
    assert r["product_USD_parity_load"] == "17/16"
    assert r["threshold_above_joint_below_product"]
    assert fmpq(r["mean_classical_Gibbs_TV_upper"]) < fmpq(1, 100000)
    assert not r["quantum_full_coherent_prior_success_proved"]
    assert r["random_sign_average_not_arbitrary_sign_guarantee"]


def test_actual_public_matrix_sampler_scales_beyond_exact_control_caps():
    branches = four_message_mixture("1/2")
    rng = random.Random(133410)
    instance = AffineFactorInstance(72, tuple(tuple(rng.randrange(2**72) for _ in range(3)) for _ in range(64)), tuple(rng.randrange(8) for _ in range(64)))
    samples = [sample_affine_mixture(instance, branches, rng) for _ in range(16)]
    assert sum(s["success"] for s in samples) == 15
    for s in samples:
        equations = instance.equations(branches, s["branches"])
        assert s["constraints"] == sum(3-branches[b].dimension for b in s["branches"])
        if s["success"]:
            assert all((a&s["outer"]).bit_count() % 2 == b for a, b in equations)
        else:
            assert s["outer"] == 0 and s["fallback_mass_is_charged"]
    assert complete_factor_control(instance, branches) == {"status": "UNKNOWN_FULL_LAW_CAP", "partial_law_promoted": False}


def test_outside_origin_linear_cone_is_not_promoted_to_hardness_or_advantage():
    r = outside_linear_cone_control()
    assert r["negative_nonzero_Walsh_coefficients"] == ("-1/5",)*3
    assert r["linear_origin_subspace_mixture_excluded"]
    assert not r["affine_coset_mixture_excluded"]
    assert not r["classical_hardness_established"] and not r["efficient_quantum_sampler_established"]
    assert r["optimal_affine_mean_unknown_bits"] == "3/5"
    assert max(r["codeword_output_errors_diagnostic"]) < 1e-12
    assert r["isometry_error_diagnostic"] < 1e-12
    assert len(r["all_affine_subspaces"]) == 11
    assert r["complete_matched_classical_control"]["complete_output_TV"] == "0"
    census = r["complete_sign_census"]
    assert len(census["cases"]) == 16
    assert any(any(b["tilt"] == "0" for b in c["branches"]) for c in census["cases"])
    assert fmpq(census["mean_output_TV"]) <= fmpq(census["mean_output_TV_upper"])
    assert not r["affine_branch_phases_discarded"]


def test_independent_exact_replay_covers_every_committed_population():
    result = subprocess.run(["node", str(REPORT.parents[1]/"certificates/linear_erasure_prange_duality_crosscheck.js")], capture_output=True, text=True, check=True)
    r = json.loads(result.stdout)
    assert r["status"] == "PASS" and r["complete_signed_instances"] == 145
    assert r["exact_Gram_entries"] == 208 and r["exact_dual_subspaces"] == 164
    assert r["live_samples"] == 16 and r["live_successes"] == 15


@pytest.mark.parametrize("mutation", ("branch_weight", "annihilator", "mean_load", "coherent_prior", "Gram", "dual", "missing_space", "optimal_general", "tilt", "fallback", "Gibbs", "sign_average", "tail", "classical_rank", "live_large_integer", "affine_exclusion", "affine_phase", "affine_offset", "transpose", "speedup"))
def test_independent_checker_rejects_false_instrument_or_classical_advantage(tmp_path, mutation):
    r = json.loads(REPORT.read_text())
    quantum, optimal = r["four_message_quantum_controls"][0], r["instrument_optimality_controls"][0]
    case = r["complete_sign_censuses"][0]["complete_sign_cases"][0]
    if mutation == "branch_weight":
        quantum["mixture"]["branches"][1]["weight"] = "1"
    elif mutation == "annihilator":
        quantum["mixture"]["branches"][4]["annihilator_basis"] = [1, 2]
    elif mutation == "mean_load":
        quantum["mixture"]["branches"][1]["classical_affine_constraints"] = 0
    elif mutation == "coherent_prior":
        quantum["mixture"]["codeword_branch_law_is_universal_coherent_prior_law"] = True
    elif mutation == "Gram":
        quantum["exact_input_output_Gram_entries"][1] = "1"
    elif mutation == "dual":
        optimal["exact_dual_coefficients"][0] = "0"
    elif mutation == "missing_space":
        optimal["all_affine_subspaces"].pop()
    elif mutation == "optimal_general":
        optimal["optimal_among_all_quantum_measurements"] = True
    elif mutation == "tilt":
        case["branches"][-1]["tilt"] = "1"
    elif mutation == "fallback":
        case["sampler_probabilities"][0] = "0"
    elif mutation == "Gibbs":
        case["Gibbs_probabilities"][0] = "0"
    elif mutation == "sign_average":
        r["complete_sign_censuses"][0]["mean_output_TV"] = "0"
    elif mutation == "tail":
        r["scaling_controls"][-1]["constraint_tail_upper"] = "0"
    elif mutation == "classical_rank":
        r["scaling_controls"][0]["matched_quantum_unknown_and_classical_constraint_load"] = "1/2"
    elif mutation == "live_large_integer":
        s = r["live_classical_samples"][0]
        s["outer"] = str(int(s["outer"]) ^ 1)
    elif mutation == "affine_exclusion":
        r["outside_linear_cone_control"]["affine_coset_mixture_excluded"] = True
    elif mutation == "affine_phase":
        r["outside_linear_cone_control"]["affine_branch_phases_discarded"] = True
    elif mutation == "affine_offset":
        r["outside_linear_cone_control"]["matched_affine_instrument"]["branches"][1]["offset"] = 0
    elif mutation == "transpose":
        r["rank_duality_controls"][-1]["quantum_reconstruction_columns"][0] ^= 1
    else:
        r["accepted_speedup_candidate"] = True
    target = tmp_path/"forged.json"
    target.write_text(json.dumps(r))
    result = subprocess.run(["node", str(REPORT.parents[1]/"certificates/linear_erasure_prange_duality_crosscheck.js"), str(target)], capture_output=True)
    assert result.returncode != 0


@pytest.mark.parametrize("call", (
    lambda: AffineBranch(0, (), "1"), lambda: AffineBranch(2, (1, 1), "1/2"),
    lambda: AffineBranch(2, (4,), "1/2"), lambda: AffineBranch(2, (1,), -.5),
    lambda: AffineBranch(2, (1,), "-1/2"), lambda: AffineBranch(2, (1,), "1/2", 4),
    lambda: validate_mixture((AffineBranch(2, (1,), "1"),)),
    lambda: validate_mixture((AffineBranch(2, (1, 2), "1/2"),)),
    lambda: validate_mixture((AffineBranch(1, (1,), "1/2"), AffineBranch(2, (1, 2), "1/2"))),
    lambda: frequency_probability(four_message_mixture("1/2"), 8),
    lambda: all_local_spaces(4), lambda: mixture_record((AffineBranch(4, (1, 2, 4, 8), "1"),)),
    lambda: AffineFactorInstance(1, ((2,),), (0,)),
    lambda: AffineFactorInstance(1, ((1, 0),), (4,)),
    lambda: AffineFactorInstance(1, ((1,), (0, 1)), (0, 0)),
    lambda: scaling_bound(4, 8, "1/2", "1"),
))
def test_invalid_sources_exact_weights_or_unbounded_certificate_claims_rejected(call):
    with pytest.raises(ValueError):
        call()
