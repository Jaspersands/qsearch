from itertools import product
import json
import math
import random
import subprocess

from flint import fmpq
import numpy as np
import pytest

from parity_block_usd_prange import (
    REPORT, BlockXOR, affine_system, conditional_inner_probability, exact_control,
    local_control, local_recipe, local_unitary, random_matrix_failure_bound,
    sample_block_prange, sample_planted_zero, uniform_affine_solution,
)


@pytest.mark.parametrize("c", ("1/10", "1/3", "1/2", "2/3", "9/10"))
def test_literal_public_decoder_is_unitary_and_cleans_parity_scratch_for_all_codewords(c):
    r = local_control(c)
    assert r["unitarity_error_diagnostic"] < 1e-12
    assert max(r["coherent_four_codeword_errors_diagnostic"]) < 1e-12
    p = fmpq(c)
    assert fmpq(r["recipe"]["joint_success"]) > fmpq(r["recipe"]["product_USD_with_parity_success"])
    assert r["input_and_output_Gram_entries"] == [str(fmpq(1) if i == j else p*p) for i, j in product(range(4), repeat=2)]
    U = local_unitary(c)
    assert np.linalg.norm(U.T@U-np.eye(16)) < 1e-12


def test_the_parity_promise_cannot_be_silently_removed():
    c, U = .5, local_unitary("1/2")
    a, b = math.sqrt((1+c)/2), math.sqrt((1-c)/2)
    message = np.kron(np.kron((a, b), (a, b)), (a, -b))
    out = U@np.kron(message, (1., 0.))
    dirty_mass = sum(abs(out[i])**2 for i in range(16) if (i >> 1)&1)
    assert dirty_mass > .1


@pytest.mark.parametrize("c", ("1/3", "1/2", "2/3"))
def test_coherent_prior_changes_the_erasure_law(c):
    r, p = local_control(c), fmpq(c)
    expected = 4*p*p/(1+3*p*p)
    assert fmpq(r["normalized_equal_superposition_erasure_probability"]) == expected
    assert abs(r["equal_superposition_erasure_diagnostic"]-float(expected)) < 1e-12
    assert expected != p*p
    assert not r["classical_codeword_erasure_law_applies_to_every_coherent_prior"]


@pytest.mark.parametrize("bits", tuple(product(range(2), repeat=3)))
@pytest.mark.parametrize("c", ("1/3", "1/2"))
def test_spin_elimination_has_positive_correlated_block_constraint_mixture(bits, c):
    c = fmpq(c)
    g = tuple((-1)**b for b in bits)
    eliminated = sum(math.prod(1+c*z*s for s in g) for z in (-1, 1))
    matching = int(g[0] == g[1] == g[2])
    reconstructed = 2*(1-c*c)+8*c*c*matching
    assert eliminated == reconstructed
    lam = 4*c*c/(1-c*c)
    assert lam/(4+lam) == c*c


def test_exact_sampler_matches_gibbs_when_all_selected_systems_are_full_rank():
    instance = BlockXOR(4, ((1, 2, 0), (4, 8, 0)), ((0, 1, 0), (1, 0, 1)))
    c = exact_control(instance, "1/2")
    assert c["bad_subset_mass"] == "0" and c["complete_output_TV"] == "0"
    assert c["Gibbs_probabilities"] == c["sampler_probabilities"]
    assert sum(map(fmpq, c["sampler_probabilities"])) == 1


def test_rank_defects_and_frustration_are_not_conditioned_away():
    instance = BlockXOR(1, ((1, 1, 1), (0, 1, 1)), ((0, 1, 0), (1, 0, 0)))
    c = exact_control(instance, "1/2")
    assert fmpq(c["bad_subset_mass"]) > 0
    assert c["subsets"][1]["solution_count"] == 0
    assert c["subsets"][1]["tilt"] == "0"
    assert not c["failures_conditioned_away"]
    assert fmpq(c["complete_output_TV"]) <= fmpq(c["subset_TV"])+fmpq(c["bad_subset_mass"])


def test_complete_random_sign_average_obeys_finite_dequantization_bound():
    labels = ((1, 2, 3), (1, 3, 2))
    controls = [exact_control(BlockXOR(2, labels, (bits[:3], bits[3:])), "1/2") for bits in product(range(2), repeat=6)]
    mean = sum(fmpq(c["complete_output_TV"]) for c in controls)/64
    assert len({c["bad_subset_mass"] for c in controls}) == 1
    assert mean <= 3*fmpq(controls[0]["bad_subset_mass"])


def test_uniform_affine_sampler_enumerates_each_solution_once_not_only_a_pivot_assignment():
    class Bits:
        def __init__(self, bits):
            self.bits = iter(bits)
        def randrange(self, limit):
            assert limit == 2
            return next(self.bits)
    equations = ((0b1011, 1), (0b0110, 0))
    system = affine_system(equations, 4)
    samples = [uniform_affine_solution(system, 4, Bits(bits)) for bits in product(range(2), repeat=len(system["free"]))]
    expected = [x for x in range(16) if all((x&a).bit_count() % 2 == b for a, b in equations)]
    assert sorted(samples) == expected


def test_inconsistent_affine_system_is_detected_exactly():
    system = affine_system(((1, 0), (1, 1)), 3)
    assert not system["consistent"]
    with pytest.raises(ValueError):
        uniform_affine_solution(system, 3, random.Random(0))


def test_actual_sampler_runs_on_large_instance_without_reference_enumeration():
    rng = random.Random(133402)
    instance = BlockXOR(48, tuple(tuple(rng.randrange(2**48) for _ in range(3)) for _ in range(64)),
                        tuple(tuple(rng.randrange(2) for _ in range(3)) for _ in range(64)))
    sample = sample_block_prange(instance, "1/3", rng)
    assert sample["success"]
    assert all((a&sample["outer"]).bit_count() % 2 == b for a, b in instance.selected_equations(sample["selected"]))
    capped = exact_control(instance, "1/3")
    assert capped["status"] == "UNKNOWN_EXACT_DISTRIBUTION_CAP" and not capped["partial_law_promoted"]


def test_matched_correlated_baseline_kills_naive_threshold_advantage_at_scale():
    c = random_matrix_failure_bound(4096, 2253, "1/2")
    assert c["naive_baseline_would_suggest_quantum_threshold_improvement"]
    assert c["joint_quantum_erasure_load_per_block"] == c["matched_classical_block_constraint_load_per_block"] == "1/2"
    assert c["independent_clause_Prange_load_per_block"] == "5/8"
    assert fmpq(c["mean_classical_Gibbs_TV_upper"]) < fmpq(2, 1000)
    assert not c["efficient_quantum_advantage_established"]


def test_planted_signs_kill_fixed_sign_prange_claim_but_another_classical_sampler_succeeds():
    r = random_matrix_failure_bound(4096, 2253, "1/2")
    assert fmpq(r["all_zero_sign_block_Prange_mean_TV_lower"]) > fmpq(99, 100)
    assert fmpq(r["all_zero_sign_zero_outer_sampler_mean_TV_upper"]) < fmpq(1, 10**100)
    assert not r["fixed_sign_claim_inferred_from_random_sign_average"]
    assert not r["failure_of_one_classical_sampler_proves_quantum_advantage"]
    instance = BlockXOR(8, ((1, 2, 4), (5, 6, 7)), ((0, 0, 0), (0, 0, 0)))
    rng = random.Random(481)
    for _ in range(16):
        sample = sample_planted_zero(instance, "1/2", rng)
        assert sample["outer"] == 0 and 0 <= sample["inner"] < 4
    with pytest.raises(ValueError, match="not a general signed"):
        sample_planted_zero(BlockXOR(8, instance.labels, ((0, 1, 0), (0, 0, 0))), "1/2", rng)


def test_independent_exact_checker_replays_the_whole_control_population():
    result = subprocess.run(["node", str(REPORT.parents[1]/"certificates/parity_block_usd_prange_crosscheck.js")], text=True, capture_output=True, check=True)
    c = json.loads(result.stdout)
    assert c["status"] == "PASS" and c["complete_signed_instances"] == 192
    assert c["local_quantum_programs"] == 3 and c["live_classical_samples"] == 32


@pytest.mark.parametrize("mutation", ("filter", "dirty_failure", "Gibbs", "fallback", "tilt", "sign_average", "large_tail", "classical_threshold", "coherent_prior", "planted_sign", "speedup"))
def test_independent_checker_rejects_false_coherence_conditioning_or_advantage(tmp_path, mutation):
    r = json.loads(REPORT.read_text())
    if mutation == "filter":
        r["local_quantum_controls"][0]["recipe"]["rows"][0]["filter_success_squared"] = "1"
    elif mutation == "dirty_failure":
        r["local_quantum_controls"][0]["recipe"]["coherent_failure_state_is_codeword_independent"] = False
    elif mutation == "Gibbs":
        r["complete_sign_censuses"][0]["random_sign_cases"][0]["Gibbs_probabilities"][0] = "0"
    elif mutation == "fallback":
        r["complete_sign_censuses"][0]["random_sign_cases"][0]["sampler_probabilities"][0] = "0"
    elif mutation == "tilt":
        r["complete_sign_censuses"][0]["random_sign_cases"][0]["subsets"][3]["tilt"] = "1"
    elif mutation == "sign_average":
        r["complete_sign_censuses"][0]["mean_complete_output_TV"] = "0"
    elif mutation == "large_tail":
        r["scaling_controls"][0]["exact_binomial_tail"] = "0"
    elif mutation == "classical_threshold":
        r["scaling_controls"][0]["matched_classical_block_constraint_load_per_block"] = "1"
    elif mutation == "coherent_prior":
        r["local_quantum_controls"][0]["classical_codeword_erasure_law_applies_to_every_coherent_prior"] = True
    elif mutation == "planted_sign":
        r["scaling_controls"][-1]["all_zero_sign_zero_outer_sampler_mean_TV_upper"] = "1"
    else:
        r["accepted_speedup_candidate"] = True
    file = tmp_path/"forged.json"
    file.write_text(json.dumps(r))
    assert subprocess.run(["node", str(REPORT.parents[1]/"certificates/parity_block_usd_prange_crosscheck.js"), str(file)], capture_output=True).returncode != 0


@pytest.mark.parametrize("call", (
    lambda: local_recipe(.5), lambda: local_recipe("0"), lambda: local_recipe("1"),
    lambda: BlockXOR(0, ((0, 0, 0),), ((0, 0, 0),)),
    lambda: BlockXOR(2, ((4, 0, 0),), ((0, 0, 0),)),
    lambda: BlockXOR(2, ((1, 0, 0),), ((0, 2, 0),)),
    lambda: affine_system(((8, 1),), 3), lambda: affine_system(((1, True),), 3),
))
def test_invalid_source_and_field_parameters_rejected(call):
    with pytest.raises(ValueError):
        call()
