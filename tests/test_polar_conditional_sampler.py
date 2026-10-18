"""SC recursion against native enumeration, plus average/worst syndrome controls."""
from fractions import Fraction
import hashlib
import json
from pathlib import Path

import pytest

from theorems.polar_conditional_sampler import (
    REPORT, _source_law, calibration, check_masks, native_channel_duality, prefix_one, sample, sample_gibbs, source_biases, syndrome, transform,
)


@pytest.mark.parametrize("N", [1, 2, 4, 8])
def test_transform_is_involutory_and_native_parity_masks_are_exact(N):
    frozen = tuple(range(0, N, 2))
    checks = check_masks(N, frozen)
    for word in range(1 << N):
        u = transform(word, N)
        assert transform(u, N) == word
        assert syndrome(u, frozen) == sum(((word & h).bit_count() % 2) << j for j, h in enumerate(checks))


@pytest.mark.parametrize("N", [2, 4, 8])
def test_every_SC_prefix_probability_equals_independent_native_marginal(N):
    p = Fraction(7, 40)
    law = _source_law(N, p)
    for i in range(N):
        for v in range(1 << i):
            prefix = tuple((v >> j) & 1 for j in range(i))
            mass = sum(prob for word, prob in enumerate(law) if word & ((1 << i)-1) == v)
            one = sum(prob for word, prob in enumerate(law) if word & ((1 << i)-1) == v and (word >> i) & 1)
            work = {"recursive_calls": 0, "maximum_fraction_bits": 0}
            assert prefix_one(N, p, prefix, work=work) == one/mass
            assert work["recursive_calls"] == 2*N-1


def test_future_frozen_bits_cannot_be_silently_treated_as_exact_conditioning():
    r = calibration(2, Fraction(1, 10), (1,))
    assert Fraction(r["worst_syndrome_TV"]) == Fraction(18, 25)
    assert Fraction(r["uniform_syndrome_average_TV"]) == Fraction(2, 5)
    assert Fraction(r["frozen_prefix_bias_sum"]) == Fraction(2, 5)
    assert not r["shaping_is_exact_native_conditional_sampler"]
    assert not r["worst_case_sign_dequantization_proved"]


def test_empty_or_complete_constraints_and_fair_source_have_exact_shaping_laws():
    for N, p, frozen in ((4, Fraction(7, 40), ()), (4, Fraction(7, 40), tuple(range(4))),
                         (4, Fraction(1, 2), (1, 3))):
        r = calibration(N, p, frozen)
        assert r["worst_syndrome_TV"] == "0"
    for N in (8, 32):
        out = sample(N, Fraction(7, 40), tuple(range(N//2)), 0, 29)
        assert out["native_conditional_distribution_certified"]


def test_nonprefix_high_entropy_control_does_not_hide_bad_syndromes_in_the_average():
    p = Fraction(7, 40)
    biases = source_biases(8, p)
    frozen = tuple(sorted(sorted(range(8), key=lambda i: (biases[i], i))[:4]))
    assert frozen == (0, 1, 2, 4)
    r = calibration(8, p, frozen)
    average, worst = Fraction(r["uniform_syndrome_average_TV"]), Fraction(r["worst_syndrome_TV"])
    assert 0 < average < Fraction(1, 200)
    assert worst > 10*average
    assert len(r["all_syndromes"]) == 16


def test_conditional_polar_target_really_is_the_native_signed_code_Gibbs_law():
    N, p, frozen = 4, Fraction(7, 40), (0, 1)
    checks = check_masks(N, frozen)
    law = _source_law(N, p)
    for signs in range(1 << N):
        s = syndrome(transform(signs, N), frozen)
        mass = sum(prob for u, prob in enumerate(law) if syndrome(u, frozen) == s)
        # Native Ising parity variables range over this binary linear kernel.
        kernel = [y for y in range(1 << N) if all((h & y).bit_count() % 2 == 0 for h in checks)]
        weights = [p**(y ^ signs).bit_count()*(1-p)**(N-(y ^ signs).bit_count()) for y in kernel]
        assert sum(weights) == mass
        for y, weight in zip(kernel, weights):
            assert law[transform(y ^ signs, N)]/mass == weight/sum(weights)


@pytest.mark.parametrize("N", [2, 4])
def test_independent_native_CQ_density_matrices_confirm_reversed_source_entropy_duality(N):
    r = native_channel_duality(N, Fraction(7, 40))
    assert r["reverse_index_identity_max_error"] < 2e-12
    assert r["reverse_index_fidelity_max_error"] < 2e-12
    assert all(-2e-12 <= e <= f/2+2e-12 for e, f in zip(
        r["native_bit_Helstrom_errors"], r["native_synthesized_root_fidelities"]))
    assert r["pure_state_overlap"] == "13/20"
    assert not r["asymptotic_capacity_or_Gibbs_separation_proved_by_numerics"]
    for i in range(N):
        # G^T=R G R, with R reversing coordinate order, fixes code conventions.
        column = check_masks(N, (i,))[0]
        row = transform(1 << (N-1-i), N)
        reversed_row = sum(((row >> j) & 1) << (N-1-j) for j in range(N))
        assert column == reversed_row


def test_scalable_samples_pay_quadratic_recursion_and_never_claim_TV_from_feasibility():
    for N in (16, 32):
        frozen = tuple(range(0, N, 2))
        for target in (0, (1 << len(frozen))-1):
            out = sample(N, Fraction(7, 40), frozen, target, 29)
            assert out["recursive_work"]["recursive_calls"] == (N-len(frozen))*(2*N-1)
            assert syndrome(transform(int(out["noise_word_hex"], 16), N), frozen) == target
            assert not out["native_conditional_distribution_certified"]
            assert not out["unconditional_source_table_materialized"]
    with pytest.raises(ValueError, match="capped"):
        calibration(16, Fraction(7, 40), ())
    with pytest.raises(ValueError):
        sample(4, 0.175, (0,), 0, 29)


def test_signed_Gibbs_workflow_outputs_the_actual_kernel_and_labels_exactness_honestly():
    for frozen in ((0, 1), (0, 2)):
        for signs in range(16):
            out = sample_gibbs(4, Fraction(13, 20), frozen, signs, 29)
            y = int(out["Gibbs_kernel_word_hex"], 16)
            assert all((h & y).bit_count() % 2 == 0 for h in check_masks(4, frozen))
            assert y ^ signs == int(out["noise_word_hex"], 16)
            assert out["native_conditional_distribution_certified"] == (frozen == (0, 1))
            assert out["top_level_polar_transforms_including_native_checks"] == 7
            assert out["binary_check_description_bits"] == 4*len(frozen)


def test_saved_all_syndrome_results_and_every_large_native_sample_replay():
    if not REPORT.exists():
        pytest.skip("producer not yet run")
    report = json.loads(REPORT.read_text())
    assert report["source_sha256"] == hashlib.sha256(Path("theorems/polar_conditional_sampler.py").read_bytes()).hexdigest()
    for name, digest in report["dependency_sha256"].items():
        assert digest == hashlib.sha256((Path("theorems")/name).read_bytes()).hexdigest()
    assert not report["all_polar_code_Gibbs_tasks_dequantized"]
    for r in report["calibrations"]:
        assert calibration(r["positions"], r["noise_probability"], tuple(r["frozen_coordinates"])) == r
        assert r["shaping_recursive_calls_charged"] == r["shaping_prefix_queries_charged"]*(2*r["positions"]-1)
    for r in report["native_channel_source_duality"]:
        assert native_channel_duality(r["positions"], r["source_probability"]) == r
    for r in report["scalable_native_samples"]:
        for out in r["samples"]:
            assert sample(r["positions"], r["noise_probability"], tuple(r["frozen_coordinates"]),
                          out["target"], out["seed"]) == out
        for out in r["signed_Gibbs_samples"]:
            assert sample_gibbs(r["positions"], out["channel_overlap"], tuple(r["frozen_coordinates"]),
                                int(out["public_clause_signs_hex"], 16), out["seed"]) == out
