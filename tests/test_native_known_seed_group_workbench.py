"""Actual group/source coupling, original promise, Fourier fibres and paid readout."""
from copy import deepcopy
from itertools import product
import json
import random
import subprocess
from fractions import Fraction

from flint import fmpq, fmpq_poly
import numpy as np
import pytest

from theorems.native_known_seed_group_workbench import (
    FULL, SLICE, REPORT, ROOT, amplification_control, character_exponent,
    collision_and_noise_ledger, computational_readout_shadow, decoded_candidate,
    domain_recipe, finite_control, finite_elements, finite_uniform_integer,
    integer_kernel_exact, literal_readout, scalar_overlap_exact, source_fixture,
)
from known_preparation_coherent_reflection import finite_field, reflection_recipe
from known_reflection_tensor_simulation import TensorState
from native_state_hsp_bridge import NativeGroup
from native_noncentral_filter_tradeoff import spectral_probability
from ternary_noise_degradation import NoisyLinearRecord


def field_decode(encoded): return fmpq_poly(list(reversed([fmpq(x) for x in encoded])))
def field_value(encoded, q): return sum(float(fmpq(x))*np.exp(2j*np.pi*k/q) for k, x in enumerate(reversed(encoded)))


@pytest.mark.parametrize("r", (1, 2, 16, 64))
def test_integer_character_frequencies_are_actual_carried_ring_characters(r):
    q = 3**r
    recipe, _, _ = source_fixture(3, r, 1, 2, True, 86000+r)
    G = NativeGroup(2*r, 3)
    b = tuple((x % q, 0) for x in (7, 13, 29))
    raw = recipe["source_receipts"]["original_classical_records"]
    for j, label in enumerate(recipe["public_native_labels"][0]):
        a, c = raw[2*j]["label"], raw[2*j+1]["label"]
        expected = (sum(x*y[0] for x, y in zip(a, b)), sum((y-x)*z[0] for x, y, z in zip(a, c, b)), -sum(x*y[0] for x, y in zip(c, b)))
        assert tuple(character_exponent(G, label, G.rotate(b, out), q) for out in range(3)) == tuple(x % q for x in expected)


@pytest.mark.parametrize("q_r,n", ((1, 1), (1, 3), (2, 1)))
def test_every_nonidentity_hidden_element_decodes_masked_secret_but_identity_does_not(q_r, n):
    q, G = 3**q_r, NativeGroup(2*q_r, n)
    secret = tuple(((i+1) % q, 0) for i in range(n))
    hidden = G.hidden_elements(secret)
    assert decoded_candidate(G, hidden[0]) is None
    for h in hidden[1:]: assert decoded_candidate(G, h) == secret


@pytest.mark.parametrize("domain", (FULL, SLICE))
def test_public_work_recipe_counts_real_controls_and_never_grants_an_opaque_inverse(domain):
    recipe, _, _ = source_fixture(4, 32, 2, 8, True, 86100)
    d = domain_recipe(recipe, domain)
    assert d["work_coordinate_trits"] == (128 if domain == SLICE else 257)
    assert int(d["uniform_work_size"]) == (3**128 if domain == SLICE else 3**257)
    assert d["controlled_character_branches_upper"] == 48
    assert d["controlled_qutrit_cyclic_permutations"] == 8
    assert d["source_preparation_calls"] == d["actual_source_inverse_calls"] == 1
    assert d["point_inverse_uses_original_values_not_secret"]
    assert not d["QRAM_supplied"] and not d["postselection_is_free"]


@pytest.mark.parametrize("domain", (FULL, SLICE))
def test_exact_zero_branch_matches_actual_whole_inverse_for_every_group_coordinate(domain):
    recipe, _, _ = source_fixture(1, 2, 2, 2, True, 86200)
    elements = finite_elements(recipe, domain)
    rows, error, joint = literal_readout(recipe, elements)
    assert error < 1e-11 and abs(np.vdot(joint, joint).real-1) < 1e-11
    for g, (actual, other) in zip(elements, rows):
        exact = scalar_overlap_exact(recipe, g)
        expected = sum(float(exact[k])*np.exp(2j*np.pi*k/9) for k in range(len(exact)))
        assert abs(expected-actual) < 1e-11
        assert abs(abs(actual)**2+other-1) < 1e-11


@pytest.mark.parametrize("noisy", (False, True))
def test_frequency_fibres_have_the_actual_Fourier_law_and_noise_cannot_increase_collision_mass(noisy):
    recipe, secret, _ = source_fixture(1, 2, 2, 2, noisy, 86300)
    kernel, coefficients, counts = integer_kernel_exact(recipe)
    Phi, powers, conjugate = finite_field(9)
    zero = field_decode(kernel["actual_source_zero_mass_exact"])
    p2 = fmpq(kernel["ideal_collision_mass"])
    assert field_value(kernel["actual_source_zero_mass_exact"], 9).real <= float(p2)+1e-12
    for sigma in kernel["frequencies"]:
        computed = fmpq_poly()
        for b in range(9):
            computed += scalar_overlap_exact(recipe, (((b, 0),), 1))*powers[-sigma[0]*b % 9]/9
        assert computed % Phi == coefficients.get(sigma, fmpq_poly())
        z = coefficients.get(sigma, fmpq_poly())
        magnitude = sum(float(z[k])*np.exp(2j*np.pi*k/9) for k in range(len(z)))
        assert abs(magnitude) <= counts[sigma]/kernel["domain_words"]+1e-12
        if not noisy:
            assert z == (fmpq(counts[sigma], kernel["domain_words"])*powers[(sigma[0]*secret[0]) % 9]) % Phi
    if not noisy: assert zero == fmpq_poly([p2])


def test_exact_random_label_collision_identity_is_exhaustively_verified_not_fitted():
    total = fmpq(0)
    for a, c in product(range(3), repeat=2):
        raw = (NoisyLinearRecord((a,), a, 3, "collision-a"), NoisyLinearRecord((c,), c, 3, "collision-c"))
        recipe = reflection_recipe(raw, (0,), 1, 1)
        kernel, _, _ = integer_kernel_exact(recipe)
        total += fmpq(kernel["ideal_collision_mass"])/9
    assert total == fmpq(1, 3)+fmpq(2, 9)


def test_integer_slice_falsifies_reusing_full_group_central_ceiling():
    c = finite_control(1, 1, 1, 2, False, 85001)
    full, sliced = c["domain_controls"]
    full_correct = fmpq(full["correct_decoding_and_zero_mass_exact"][0])
    full_accepted = fmpq(full["nonidentity_candidate_and_zero_mass_exact"][0])
    assert full_correct/full_accepted == fmpq(1, 3)
    slice_correct = fmpq(sliced["correct_decoding_and_zero_mass_exact"][0])
    slice_accepted = fmpq(sliced["source_zero_mass_exact"][0])
    assert slice_correct/slice_accepted == 1
    assert slice_accepted == fmpq(1, 3)
    assert not sliced["full_group_ceiling_applied_to_integer_slice"]


def test_true_target_noise_bound_is_quadratic_pure_error_and_preserves_raw_probability():
    c = finite_control(1, 2, 2, 2, True, 85004)
    error = field_value(c["actual_vs_ideal_pure_trace_distance_squared_exact"], 9).real
    sliced = c["domain_controls"][1]
    correct = field_value(sliced["correct_decoding_and_zero_mass_exact"], 9).real
    assert 9*correct >= max(0, 1-4*error)-1e-12
    assert field_value(sliced["source_zero_mass_exact"], 9).real <= float(fmpq(c["integer_kernel"]["ideal_collision_mass"]))+1e-12


@pytest.mark.parametrize("n", (8, 32, 64, 128))
def test_scalable_conditional_correctness_is_not_free_state_preparation(n):
    q, M = 3**n, n*n+24
    V = fmpq(q*q, 3*n**6)+fmpq(1, 2)
    raw = collision_and_noise_ledger(n, n, 1, M, V)
    amplified = collision_and_noise_ledger(n, n, 1, M, V, n*n)
    N, D = 3**(n*n), 3**M
    expected = fmpq(1, N)+fmpq(N-1, N*D)
    assert fmpq(raw["mean_actual_source_zero_upper"]) == expected
    assert fmpq(raw["ensemble_conditional_correct_lower"]) > fmpq(9, 10)
    assert fmpq(amplified["mean_amplified_zero_success_upper"]) == min(fmpq(1), (2*n*n+1)**2*expected)
    assert amplified["conditional_event_positive_certified_by_source_bound"]
    assert not amplified["two_reflection_bound_is_general_quantum_query_lower_bound"]
    assert not amplified["conditional_pure_phase_bound_covers_generic_gate_errors"]
    necessary = int(fmpq(amplified["necessary_iterations_for_half_mean_zero_success"]))
    assert (2*necessary+1)**2*expected >= fmpq(1, 2)
    assert not necessary or (2*necessary-1)**2*expected < fmpq(1, 2)
    assert amplified["amplified_ensemble_conditional_correct_lower"] is None


def test_large_or_bad_source_error_never_becomes_a_conditional_recovery_certificate():
    ledger = collision_and_noise_ledger(4, 4, 1, 32, 3**100)
    assert ledger["ensemble_conditional_correct_lower"] == "0"
    assert not ledger["conditional_event_positive_certified_by_source_bound"]


def test_per_bank_good_distribution_invariance_does_not_prove_ensemble_conditional_invariance():
    # Two legitimate normalized instrument models, not a native-source claim:
    # the first bank is always correct on acceptance, the second always wrong.
    p_good, p_bad = Fraction(3, 4), Fraction(1, 4)
    raw_conditional = p_good/(p_good+p_bad)
    after_good, after_bad = spectral_probability(p_good, 1), spectral_probability(p_bad, 1)
    assert raw_conditional == Fraction(3, 4)
    assert after_good == 0 and after_bad == 1
    assert after_good/(after_good+after_bad) == 0


@pytest.mark.parametrize("domain", (FULL, SLICE))
def test_whole_orbit_amplification_has_actual_sine_cost_and_unchanged_good_distribution(domain):
    recipe, _, _ = source_fixture(1, 1, 1, 2, False, 85001)
    elements = finite_elements(recipe, domain)
    _, _, joint = literal_readout(recipe, elements)
    c = finite_control(1, 1, 1, 2, False, 85001)["domain_controls"][0 if domain == FULL else 1]
    Phi, _, _ = finite_field(3)
    p, correct, accepted = map(field_decode, (c["source_zero_mass_exact"], c["correct_decoding_and_zero_mass_exact"], c["nonidentity_candidate_and_zero_mass_exact"]))
    amp = amplification_control(joint, p, correct, accepted, Phi)
    for row in amp["iteration_history"]:
        pj, cj = field_decode(row["source_zero_mass_exact"]), field_decode(row["correct_and_zero_mass_exact"])
        assert (cj*p-correct*pj) % Phi == 0
        assert row["actual_zero_probability"] <= (2*row["iterations"]+1)**2*float(p[0])+1e-12
        assert row["pure_joint_preparation_or_inverse_calls"] == 2*row["iterations"]+1


@pytest.mark.parametrize("domain", (FULL, SLICE))
def test_early_group_readout_rational_shadow_matches_unconditional_source_prefixes(domain):
    recipe, _, _ = source_fixture(1, 2, 2, 2, True, 86400)
    shadow = computational_readout_shadow(recipe, domain, random.Random(86401))
    assert shadow["source_sample"]["status"] == "CERTIFIED_RATIONAL_POINT_SAMPLE"
    _, _, joint = literal_readout(recipe, (shadow["group_element"],))
    shape = (2, 3, 3)
    exact = abs(joint[0].reshape(shape))**2
    decisions = shadow["source_sample"]["decisions"]
    original_norm = sum((fmpq(x) for x in decisions[0]["exact_branch_weights"]), fmpq(0))
    error = fmpq(shadow["whole_joint_readout_TV_or_abort_upper"])
    prefix = ()
    for d in decisions:
        for k, weight in enumerate(d["exact_branch_weights"]):
            expected = float(np.sum(exact[prefix+(k,)]))
            observed = float(fmpq(weight)/original_norm)
            assert abs(expected-observed) <= float(error)+1e-12
        prefix += (d["selected_outcome"],)
    assert shadow["source_tensor_terms"] == 2
    assert not shadow["group_Fourier_or_whole_orbit_amplification_covered"]


def test_high_root_shadow_does_not_allocate_either_hilbert_space_or_frequency_table(monkeypatch):
    def forbidden(*args, **kwargs): raise AssertionError("dense replay requested")
    monkeypatch.setattr(TensorState, "diagnostic_vector", forbidden)
    recipe, _, _ = source_fixture(4, 64, 2, 8, True, 85006)
    shadow = computational_readout_shadow(recipe, SLICE, random.Random(85007))
    assert shadow["source_tensor_terms"] == 2
    assert not shadow["full_group_or_source_table_allocated"]
    assert not shadow["secret_or_errors_read"]
    assert fmpq(shadow["whole_joint_readout_TV_or_abort_upper"]) < fmpq(1, 10000)


class RejectCoin:
    def getrandbits(self, bits): return 2**bits-1


def test_group_coin_abort_is_explicit_and_still_has_complete_unconditional_budget():
    d = finite_uniform_integer(3, RejectCoin(), 3)
    assert d["value"] is None and len(d["draws"]) == 3
    recipe, _, _ = source_fixture(1, 1, 1, 1, True, 86500)
    shadow = computational_readout_shadow(recipe, SLICE, RejectCoin())
    assert shadow["status"] == "EXPLICIT_GROUP_COIN_ABORT"
    assert fmpq(shadow["unconditional_coin_abort_upper"]) <= fmpq(1, 2**24)
    assert not shadow["whole_completion_conditioning_allowed"]
    bad = deepcopy(recipe)
    bad["ideal_unknown_state_inverse_supplied"] = True
    with pytest.raises(ValueError, match="same-original-data"):
        computational_readout_shadow(bad, SLICE, RejectCoin())


def test_word_and_group_table_limits_do_not_turn_into_unknown_oracle_access():
    recipe, _, _ = source_fixture(3, 16, 1, 16, False, 86600)
    with pytest.raises(ValueError, match="bounded"): finite_elements(recipe, FULL)
    with pytest.raises(ValueError, match="bounded"): integer_kernel_exact(recipe)
    with pytest.raises(ValueError, match="declared"): domain_recipe(recipe, "CHOSEN_LABEL_ORACLE")


def test_live_artifact_has_full_unconditional_laws_not_accepted_only_scores():
    report = json.loads(REPORT.read_text())
    assert len(report["finite_actual_group_controls"]) == 4
    assert len(report["scalable_collision_noise_price_ledgers"]) == 8
    assert len(report["computational_readout_classical_shadows"]) == 4
    for c in report["finite_actual_group_controls"]:
        for d in c["domain_controls"]:
            assert d["literal_group_source_Schmidt_rank"] > 1
            q = int(c["source_recipe"]["modulus"])
            total = 0.
            for row in d["group_rows"]:
                p = field_value(row["source_zero_probability_exact"], q).real
                other = field_value(row["source_nonzero_probability_exact"], q).real
                assert min(p, other) > -1e-12 and abs(p+other-1) < 1e-12
                total += p/len(d["group_rows"])
                if row["group_element"][1] == 0: assert row["decoded_candidate"] is None
            assert abs(total-field_value(d["source_zero_mass_exact"], q).real) < 1e-11
    assert not report["efficient_full_decoder_supplied"]
    assert not report["integer_slice_excluded_by_full_group_central_ceiling"]
    assert not report["accepted_speedup_candidate"]


def test_independent_native_group_checker_replays_every_branch_kernel_and_cost():
    checker = ROOT/"research/certificates/native_known_seed_group_crosscheck.js"
    result = subprocess.run(["node", str(checker)], capture_output=True, text=True, timeout=120)
    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert report["status"] == "PASS" and report["exact_group_rows"] == 2748
    assert report["exact_integer_Fourier_kernels"] == 4 and report["paid_amplification_controls"] == 8
    assert not report["complete_scalable_shadow_tensor_reconstruction"]


@pytest.mark.parametrize("forgery", ("scope", "identity_amplitude", "amplification_price"))
def test_independent_checker_rejects_scope_gate_and_free_amplification_forgeries(forgery, tmp_path):
    report = json.loads(REPORT.read_text())
    exported = "run"
    if forgery == "scope": report["integer_slice_excluded_by_full_group_central_ceiling"] = True
    if forgery == "identity_amplitude": report["finite_actual_group_controls"][0]["domain_controls"][0]["group_rows"][0]["source_zero_amplitude_exact"] = ["-1"]
    if forgery == "amplification_price":
        report = deepcopy(report["scalable_collision_noise_price_ledgers"][1])
        report["two_reflection_iteration_count"] = 0
        exported = "ledger"
    file = tmp_path/"forged.json"
    file.write_text(json.dumps(report))
    script = "const fs=require('fs'); const C=require(process.argv[1]); C[process.argv[3]](JSON.parse(fs.readFileSync(process.argv[2],'utf8')));"
    result = subprocess.run(["node", "-e", script, str(ROOT/"research/certificates/native_known_seed_group_crosscheck.js"), str(file), exported], capture_output=True, text=True, timeout=120)
    assert result.returncode != 0
