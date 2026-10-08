from fractions import Fraction
import json
import random
import subprocess

from flint import fmpq
import mpmath as mp
import pytest

from ternary_certified_noise_sampler import (
    acceptance_box, certified_sample_noise, cosine_box, pi_box, sampler_failure_bound,
)
from ternary_covariant_noise import CovariantRecord
from ternary_noise_degradation import (
    REPORT, NoisyLinearRecord, convert_pairs, degradation_bound, gaussian_rounding_loss,
    round_observation_interval, round_source_intervals, rounded_gaussian_profile, sampling_budget, unmask,
)


@pytest.mark.parametrize("bits", (1, 8, 32, 64))
def test_rational_machin_pi_interval_contains_high_precision_reference(bits):
    lower, upper, terms = pi_box(bits)
    with mp.workdps(150):
        assert mp.mpf(str(lower.numerator))/int(lower.denominator) < mp.pi
        assert mp.pi < mp.mpf(str(upper.numerator))/int(upper.denominator)
    assert upper-lower <= fmpq(20, 2**(bits+10))
    assert all(type(x) is int and x >= 1 for x in terms)


@pytest.mark.parametrize("q", (3, 9, 3**80))
def test_exact_cosine_enclosures_include_all_phase_regimes_without_float(q):
    for residue in (0, 1, q//3, 2*q//3, q//2, q-1, -q//2):
        lower, upper = cosine_box(q, residue, 64)
        with mp.workdps(200):
            actual = mp.cos(2*mp.pi*mp.mpf(residue)/q)
            lo, hi = (mp.mpf(int(x.numerator))/int(x.denominator) for x in (lower, upper))
            assert lo-mp.mpf("1e-180") <= actual <= hi+mp.mpf("1e-180")
        assert upper-lower <= fmpq(1, 2**64)
    assert cosine_box(q, q//3, 64) == (fmpq(-1, 2), fmpq(-1, 2))


def test_native_zero_and_one_acceptances_are_exact_not_float_near_ties():
    assert acceptance_box(9, (0, 0), 8) == (1, 1)
    assert acceptance_box(9, (3, 6), 8) == (0, 0)


class Scripted:
    def __init__(self, proposals, coins):
        self.proposals, self.coins = iter(proposals), iter(coins)

    def randrange(self, q):
        return next(self.proposals)

    def getrandbits(self, bits):
        return next(self.coins)


def test_sampler_aborts_instead_of_erasing_a_proposal_cap():
    result = certified_sample_noise(9, Scripted((3, 6), (0,)), max_proposals=1)
    assert result["status"] == "UNKNOWN_PROPOSAL_CAP" and result["noise"] is None
    assert not result["successful_channel_conditioned_on_no_abort_is_exact"]


def test_sampler_precision_cap_is_unknown_not_a_midpoint_guess():
    # At q9,(1,0), acceptance lies between1/2 and1; a one-bit prefix1
    # overlaps it. A numeric midpoint would silently accept or reject.
    result = certified_sample_noise(9, Scripted((1, 0), (1,)), max_bits=1, max_proposals=1)
    assert result["status"] == "UNKNOWN_COIN_PRECISION_CAP"
    assert result["trace"][0]["decisions"][-1]["decision"] == "REFINE"


def test_every_successful_lazy_coin_decision_uses_disjoint_exact_intervals():
    rng = random.Random(129000)
    for _ in range(40):
        result = certified_sample_noise(3**24, rng)
        assert result["noise"] is not None
        for proposal in result["trace"]:
            for step in proposal["decisions"]:
                lo, hi = acceptance_box(3**24, proposal["proposal"], step["bits"])
                assert str(lo) == step["acceptance_lower"] and str(hi) == step["acceptance_upper"]
                coin_lo, coin_hi = fmpq(step["coin_prefix"], 2**step["bits"]), fmpq(step["coin_prefix"]+1, 2**step["bits"])
                if step["decision"] == "ACCEPT":
                    assert coin_hi <= lo
                elif step["decision"] == "REJECT":
                    assert coin_lo >= hi
                else:
                    assert coin_hi > lo and coin_lo < hi


def test_public_noise_conversion_preserves_labels_and_original_pair_ancestry():
    q, secret, rng = 81, (17, 28), random.Random(129100)
    labels = ((1, 0), (0, 1), (2, 3), (4, 5))
    errors = (-1, 0, 1, 0)
    samples = tuple(NoisyLinearRecord(label, (sum(a*s for a, s in zip(label, secret))+e) % q, q, str(i))
                    for i, (label, e) in enumerate(zip(labels, errors)))
    result = convert_pairs(samples, rng, Fraction(1, 2))
    assert result["complete_transcript"] and len(result["records"]) == 2
    assert result["source_ancestry"] == [("0", "1"), ("2", "3")]
    masked = tuple((a+b) % q for a, b in zip(secret, result["reduction_side_secret_mask"]))
    for j, raw in enumerate(result["records"]):
        record = CovariantRecord(**raw)
        assert record.first == labels[2*j] and record.second == labels[2*j+1]
        assert record.residual(masked) == tuple((errors[2*j+k]+result["sampler_runs"][j]["noise"][k]) % q for k in range(2))
    assert unmask(masked, result["reduction_side_secret_mask"], q) == secret
    assert not result["hardness_transfer_admitted"] and not result["accepted_speedup_candidate"]
    assert result["native_unknown_quantum_states_prepared"] == 0


def test_reused_originals_and_mixed_root_samples_are_rejected():
    a = NoisyLinearRecord((1,), 2, 9, "a")
    with pytest.raises(ValueError):
        convert_pairs((a, a), random.Random(1), 1)
    with pytest.raises(ValueError):
        convert_pairs((a, NoisyLinearRecord((1,), 2, 27, "b")), random.Random(1), 1)


def test_complete_transcript_losses_charge_all_sources_and_abort_channels():
    gate = degradation_bound(3**16, 512, "1/2")
    assert fmpq(gate["per_record_ideal_noise_TV_upper"]) == fmpq(40, 3*3**32)
    assert fmpq(gate["per_record_sampler_abort_probability_upper"]) == sampler_failure_bound()
    assert gate["input_classical_samples_required"] == 1024
    assert fmpq(gate["complete_transcript_success_loss_upper"]) > 512*fmpq(gate["per_record_ideal_noise_TV_upper"])
    assert not degradation_bound(9, 16, "1/2")["bound_is_nonvacuous"]
    assert not degradation_bound(9, 16, 0)["unconditional_hardness_or_speedup"]


def test_source_theorem_guards_and_gaussian_width_convention_are_explicit():
    quantum = rounded_gaussian_profile(64, 3**16, "1/1048576", 512)
    classical = rounded_gaussian_profile(64, 3**64, "1/1048576", 512)
    invalid = rounded_gaussian_profile(64, 9, "1/1048576", 512)
    assert quantum["published_quantum_worst_case_source_parameter_guard"]
    assert not quantum["published_classical_worst_case_source_parameter_guard"]
    assert classical["published_classical_worst_case_source_parameter_guard"]
    assert not invalid["published_quantum_worst_case_source_parameter_guard"]
    assert not classical["hardness_transfer_admitted"]
    assert not classical["Gaussian_width_is_standard_deviation"]
    assert classical["source_precision_adapter_implemented"]
    assert fmpq(classical["composed_success_loss_upper"]) >= fmpq(classical["conditional_transcript_bound"]["complete_transcript_success_loss_upper"])
    large_noise = rounded_gaussian_profile(64, 3**16, "1/2", 512)
    assert large_noise["composed_success_loss_upper"] == "1"


def test_source_rounding_guard_handles_negative_and_wrapped_representatives():
    assert round_observation_interval(9, "-1/9", "-1/9")["value"] == 8
    assert round_observation_interval(9, "99/100", "101/100")["value"] == 0
    ambiguous = round_observation_interval(9, "5/36", "7/36")
    assert ambiguous["value"] is None and ambiguous["status"] == "UNKNOWN_ROUNDING_BOUNDARY"
    assert not ambiguous["midpoint_guess_on_ambiguous_interval"]
    with pytest.raises(ValueError):
        round_observation_interval(9, 1, 0)


def test_source_adapter_does_not_select_successful_prefix_samples_as_complete():
    valid = {"label": (1,), "modulus": 9, "lower": "1/10", "upper": "1/9", "source_id": "a"}
    invalid = {"label": (2,), "modulus": 9, "lower": "5/36", "upper": "7/36", "source_id": "b"}
    result = round_source_intervals((valid, invalid))
    assert result["status"] == "UNKNOWN_SOURCE_ROUNDING" and not result["records"]
    assert not result["partial_samples_reused_as_full_transcript"]
    result = round_source_intervals((valid, valid | {"source_id": "b"}))
    assert len(result["records"]) == 2 and result["records"][0].value == 1


def test_source_rounding_loss_covers_both_original_inputs_per_output_pair():
    gate = gaussian_rounding_loss(81, "1/9", 16, "1/1000000")
    assert gate["per_input_rounding_abort_probability_upper"] == "9/50000"
    assert gate["two_M_input_rounding_abort_union_upper"] == "18/3125"


@pytest.mark.parametrize("M,kappa", ((1, 1), (512, 64), (2**80, 160)))
def test_sampling_precision_scales_with_total_records_not_a_fixed_float_budget(M, kappa):
    budget = sampling_budget(M, kappa)
    assert fmpq(budget["M_record_sampler_abort_union_upper"]) <= fmpq(1, 2**kappa)
    assert not budget["fixed_precision_is_asymptotically_sufficient"]
    assert budget["max_proposals"] == 2*(kappa+(2*M-1).bit_length())
    assert budget["max_bits"] == kappa+(6*M*budget["max_proposals"]-1).bit_length()


def test_rounding_confidence_is_charged_and_not_inferred_on_invalid_source_guards():
    valid = rounded_gaussian_profile(64, 3**64, "1/1048576", 512, failure_bits=120)
    assert fmpq(valid["source_rounding_loss"]["two_M_input_rounding_abort_union_upper"]) <= fmpq(1, 2**120)
    assert fmpq(valid["sampler_budget"]["M_record_sampler_abort_union_upper"]) <= fmpq(1, 2**120)
    assert valid["source_rounding_loss"]["source_interval_contains_true_observation_is_assumed_not_inferred"]


def test_independent_exact_replay_covers_large_roots_source_theorems_and_abort_controls():
    checker = REPORT.parents[1]/"certificates/ternary_noise_degradation_crosscheck.js"
    result = subprocess.run(["node", str(checker)], capture_output=True, text=True, check=True)
    report = json.loads(result.stdout)
    assert report["status"] == "PASS"
    assert report["classical_input_originals"] == 128 and report["complete_paired_outputs"] == 64
    assert report["verified_proposals"] == 205 and report["exact_lazy_coin_decisions"] == 206
    assert report["finite_exact_convolution_entries"] == 90
    assert report["explicit_abort_controls"] == 2
    assert not report["hardness_transfer_admitted"] and not report["quantum_input_bridge"]


@pytest.mark.parametrize("mutation", ("wrong_interval", "erased_TV", "false_hardness", "rounding_guess"))
def test_independent_checker_rejects_false_arithmetic_or_admission(tmp_path, mutation):
    report = json.loads(REPORT.read_text())
    if mutation == "wrong_interval":
        report["controls"][0]["converted"]["sampler_runs"][0]["trace"][0]["decisions"][0]["acceptance_lower"] = "-1"
    elif mutation == "erased_TV":
        report["rounded_Gaussian_source_profiles"][0]["composed_success_loss_upper"] = "0"
    elif mutation == "false_hardness":
        report["rounded_Gaussian_source_profiles"][0]["hardness_transfer_admitted"] = True
    else:
        report["rounding_controls"][0]["status"] = "CERTIFIED_UNIQUE_ROUNDING"
        report["rounding_controls"][0]["value"] = 2
    file = tmp_path/"false.json"
    file.write_text(json.dumps(report))
    checker = REPORT.parents[1]/"certificates/ternary_noise_degradation_crosscheck.js"
    assert subprocess.run(["node", str(checker), str(file)], capture_output=True).returncode != 0


@pytest.mark.parametrize("q,V", ((9, -1), (9, .5), (10, 1), (True, 1)))
def test_invalid_or_floating_noise_promises_rejected(q, V):
    with pytest.raises(ValueError):
        degradation_bound(q, 16, V)
