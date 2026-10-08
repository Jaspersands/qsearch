from fractions import Fraction
from itertools import product
import json
from pathlib import Path
import subprocess

import numpy as np
import pytest

from cyclic_centre_state_hsp_receiver import (
    BilinearExtension, ROOT, calibration_source, character_matrix,
    final_fourier_control, kernel, qutrit_sector_actions, reference_receiver,
    resource_ledger, run_controls, sector_fourier_control, two_qudit_purified_control, words,
)


@pytest.fixture(scope="module")
def report():
    return run_controls()


@pytest.mark.parametrize("p", [3, 5, 7, 17])
@pytest.mark.parametrize("form", [((0, 0), (1, 0)), ((1, 2), (0, 1)), ((0, 1), (1, 0))])
def test_group_law_order_and_exact_commutator_match_bilinear_form(p, form):
    G = BilinearExtension(p, form)
    gs = [((0, 0), 0), ((1, 0), 0), ((0, 1), 1), ((2, 1), 2)]
    identity = ((0, 0), 0)
    for g, h, k in product(gs, repeat=3):
        assert G.multiply(G.multiply(g, h), k) == G.multiply(g, G.multiply(h, k))
    for g in gs:
        x = identity
        for _ in range(p):
            x = G.multiply(x, g)
        assert x == identity
    for x, z in gs:
        for y, w in gs:
            left = G.multiply((x, z), (y, w))
            right = G.multiply((y, w), (x, z))
            assert left[0] == right[0]
            assert (left[1]-right[1]) % p == G.commutator(x, y)


@pytest.mark.parametrize("p", [3, 5, 7])
def test_half_quadratic_chart_is_actual_homomorphism_not_a_linear_section(p):
    G = BilinearExtension(p, ((0, 0), (1, 0)))
    for v in ((1, 0), (0, 1), (1, 1), (1, 2)):
        frame = (v,)
        for x, y in product(words(2, p), repeat=2):
            xy = tuple((a+b) % p for a, b in zip(x, y))
            assert G.chart(frame, xy) == G.multiply(G.chart(frame, x), G.chart(frame, y))
    assert G.chart(((1, 1),), (1, 0))[1] == pow(2, -1, p)


def test_noncommuting_overgroup_returns_failure_not_an_assumed_repair():
    G = BilinearExtension(3, ((0, 0), (1, 0)))
    with pytest.raises(ValueError, match="does not commute"):
        G.chart(((1, 0), (0, 1)), (1, 0, 0))
    with pytest.raises(ValueError, match="independent"):
        G.chart(((1, 0), (1, 0)), (1, 0, 0))


@pytest.mark.parametrize("p", [3, 5, 7, 17])
@pytest.mark.parametrize("d", [1, 8, 128, 512])
def test_ledger_proves_strict_phase_rigidity_quota_and_selected_sector_union(p, d):
    r = resource_ledger(p, d, Fraction(1, 7), 32)
    delta = Fraction(r["conditional_modulus_defect_threshold"])
    assert 32*delta < Fraction(16, p*p)
    m = r["sector_Fourier_experiments"]
    u = r["data_selected_sector_union_bits"]
    assert 2**u >= p-1
    assert m*delta/2 >= d*r["ceil_log2_p"]+32+2+u
    w = Fraction(r["one_nonzero_sector_weight_lower_if_centre_not_fixed"])
    C = r["selected_sector_copy_quota"]
    N = r["original_centre_acquisition_cap"]
    assert N*w >= 2*C+8*(32+2)
    assert r["fresh_original_final_copy_cap"]*Fraction(1, 7)/2 >= (d+1)*r["ceil_log2_p"]+32+2
    assert r["known_controlled_R_call_cap"] == N+C+r["fresh_original_final_copy_cap"]
    assert Fraction(r["total_ideal_failure_upper"]) == Fraction(3, 2**34)
    assert not r["minimum_conditional_gap_required"]
    assert not r["polylog_group_order_at_arbitrary_binary_encoded_prime"]


@pytest.mark.parametrize("lam", [1, 2])
def test_known_projective_action_linearises_only_on_the_prepared_sector(lam):
    points = words(2, 3)
    Us = qutrit_sector_actions(lam)
    for i, (a, b) in enumerate(points):
        for j, (c, d) in enumerate(points):
            k = points.index(((a+c) % 3, (b+d) % 3))
            assert np.allclose(Us[i] @ Us[j], np.exp(2j*np.pi*(lam*b*c % 3)/3)*Us[k])
            left = Us[i] @ Us[j]
            assert np.allclose(np.kron(np.kron(left, left), left), np.kron(np.kron(Us[k], Us[k]), Us[k]))
    # Two instead of three SAME-sector copies leave a nontrivial cocycle.
    a, b, k = Us[points.index((0, 1))], Us[points.index((1, 0))], Us[points.index((1, 1))]
    assert not np.allclose(np.kron(a @ b, a @ b), np.kron(k, k))
    # Three DIFFERENT sectors need not have cocycle sum zero.
    others = qutrit_sector_actions(3-lam)
    assert not np.allclose(np.kron(np.kron(a @ b, a @ b), others[1] @ others[3]),
                           np.kron(np.kron(k, k), others[4]))


@pytest.mark.parametrize("lam", [1, 2])
def test_literal_tensor_measurement_on_arbitrary_non_diagonal_mixed_density(lam):
    rng = np.random.default_rng(61321+lam)
    for _ in range(6):
        A = rng.normal(size=(3, 3))+1j*rng.normal(size=(3, 3))
        rho = A @ A.conj().T
        rho /= np.trace(rho)
        r = sector_fourier_control(rho, lam)
        assert r["literal_Kraus_probabilities"] == pytest.approx(r["tensor_moment_Fourier_probabilities"], abs=2e-12)
        for x, z in zip(words(2, 3), r["conditional_action_moments_real_imag"]):
            delta = 1-abs(complex(*z))
            detection = sum(prob for y, prob in zip(words(2, 3), r["literal_Kraus_probabilities"]) if sum(a*b for a, b in zip(x, y)) % 3)
            assert detection >= delta/2-2e-12


def test_supplied_full_known_action_is_an_actual_nonabelian_representation():
    s = calibration_source("coset-coherent", 2)
    G = s["extension"]
    elements = [(x, z) for x in words(2, 3) for z in range(3)]
    matrices = {g: s["action"](g) for g in elements}
    for g, h in product(elements, repeat=2):
        assert np.allclose(matrices[g] @ matrices[h], matrices[G.multiply(g, h)])


def test_every_literal_tensor_outcome_agrees_with_its_entire_character_law(report):
    assert len(report["complete_literal_sector_instruments"]) == 18
    for c in report["complete_literal_sector_instruments"]:
        assert len(c["literal_Kraus_probabilities"]) == 9
        assert c["literal_Kraus_probabilities"] == pytest.approx(c["tensor_moment_Fourier_probabilities"], abs=2e-12)
        assert sum(c["literal_Kraus_probabilities"]) == pytest.approx(1)
        assert c["input_qutrit_copies_consumed"] == 3
        assert not c["selected_sector_supplied_for_free"]
        assert not c["full_unconditioned_tensor_action_claimed_linear"]


def test_all_caps_and_final_original_state_instruments_are_executed(report):
    assert len(report["capped_complete_reference_receivers"]) == 10
    for r in report["capped_complete_reference_receivers"]:
        assert r["status"] == "RECOVERED"
        assert r["recovered_Bose_subgroup_elements"] == r["actual_Bose_subgroup_elements"]
        assert r["actual_total_original_copies"] <= r["ledger"]["total_original_copy_cap"]
        assert r["actual_known_controlled_R_calls"] <= r["ledger"]["known_controlled_R_call_cap"]
        assert sum(r["centre_bucket_counts"]) == r["actual_original_centre_draws"]
        assert sum(r["final_sample_histogram"]) == r["ledger"]["fresh_original_final_copy_cap"]
        if r["selected_nonzero_sector"] is not None:
            assert r["centre_bucket_counts"][r["selected_nonzero_sector"]] == r["ledger"]["selected_sector_copy_quota"]
            assert sum(r["tensor_sample_histogram"]) == r["ledger"]["sector_Fourier_experiments"]
        assert r["final_instrument"]["literal_Kraus_probabilities"] == pytest.approx(r["final_instrument"]["probabilities"], abs=2e-12)
        assert not r["one_original_source_state_copied_or_reused"]


def test_phaseless_quotient_target_is_insufficient_but_final_decoder_recovers_every_lift(report):
    rs = [r for r in report["capped_complete_reference_receivers"] if r["source_kind"] == "coset-mixed"]
    assert {r["calibration_central_lift"] for r in rs} == set(range(3))
    assert len({json.dumps(r["recovered_quotient_overgroup_frame"]) for r in rs}) == 1
    assert len({json.dumps(r["recovered_Bose_subgroup_elements"]) for r in rs}) == 3
    G = BilinearExtension(3, ((0, 0), (1, 0)))
    h = ((0, 1), 0)
    g = ((1, 0), 0)
    assert G.multiply(g, h) != G.multiply(h, g)


def test_exponentially_tiny_conditional_gap_does_not_need_exact_sector_symmetry_learning(report):
    c = report["tiny_conditional_gap_countercontrol"]
    assert Fraction(c["conditional_exact_gap_of_Z_direction"]) == Fraction(1, 2**40)
    r = next(r for r in report["capped_complete_reference_receivers"] if r["source_kind"] == "tiny-conditional-gap" and Fraction(r["contamination_eta"]) == Fraction(1, 2**40))
    assert r["selected_nonzero_sector"] == 1
    assert r["recovered_quotient_overgroup_frame"] == ((0, 1),)
    assert r["recovered_Bose_subgroup_elements"] == (((0, 0), 0),)
    rho = calibration_source("tiny-conditional-gap", eta=Fraction(1, 2**40))["conditional_states"][1]
    value = np.trace(qutrit_sector_actions(1)[1] @ rho)
    assert abs(value) < 1
    assert abs(value) > 1-float(Fraction(1, 2**39))
    assert Fraction(c["original_Bose_gap_lower"]) == Fraction(2, 3)


def test_conditional_gap_probability_formulas_are_exact_rationals(report):
    c = report["tiny_conditional_gap_countercontrol"]
    e = Fraction(c["conditional_exact_gap_of_Z_direction"])
    a = (1-e)**3
    assert Fraction(c["exact_tensor_probability_if_second_character_zero"]) == (1+2*a)/9
    assert Fraction(c["exact_tensor_probability_if_second_character_nonzero"]) == (1-a)/9
    assert Fraction(c["final_original_probability_yb_nonzero_yz1"]) == e/9
    assert 3*Fraction(c["exact_tensor_probability_if_second_character_zero"])+6*Fraction(c["exact_tensor_probability_if_second_character_nonzero"]) == 1


def test_pure_cross_sector_coherence_does_not_change_the_legal_readout_or_bose_target():
    source = calibration_source("coset-coherent", 1)
    assert np.trace(source["original"] @ source["original"]) == pytest.approx(1)
    assert np.linalg.norm(source["original"][:9, 9:]) > .1
    other = calibration_source("coset-mixed", 1)
    for x in source["points"]:
        for z in range(3):
            assert np.trace(source["action"]((x, z)) @ source["original"]) == pytest.approx(np.trace(other["action"]((x, z)) @ other["original"]))


def test_nonstabilizer_full_six_qutrit_controls_do_not_rely_on_diagonal_density_fixtures(report):
    for c in report["nonstabilizer_two_qudit_instruments"]:
        assert c["maximum_nonidentity_one_component_overlap"] < .99
        assert len(c["full_character_words"]) == 81
        assert c["physical_qutrits_in_three_copies"] == 6
        assert c["complete_literal_probabilities"] == pytest.approx(c["tensor_moment_Fourier_probabilities"], abs=2e-12)
        one = c["one_component_instrument"]["literal_Kraus_probabilities"]
        for y, p in zip(c["full_character_words"], c["complete_literal_probabilities"]):
            assert p == pytest.approx(one[3*y[1]+y[3]]/3 if y[2] == 0 else 0, abs=2e-12)
        assert not c["density_table_is_an_algorithm_input"]
    with pytest.raises(ValueError, match="nonstabilizer"):
        two_qudit_purified_control(1, (1, 0, 0))


def test_centre_trivial_case_and_rare_paid_sector_both_survive(report):
    fixed = next(r for r in report["capped_complete_reference_receivers"] if r["successful_centre_fixed_branch"])
    assert fixed["selected_nonzero_sector"] is None
    assert fixed["quotient_overgroup_commutator_zero"] is None
    assert not fixed["actual_abelian_overgroup_used"]
    assert fixed["centre_fixed_quotient_action_linear_on_support"]
    assert not fixed["centre_fixed_section_claimed_linear_on_full_workspace"]
    assert fixed["actual_original_centre_draws"] == fixed["ledger"]["original_centre_acquisition_cap"]
    assert len(fixed["recovered_Bose_subgroup_elements"]) == 9
    rare = next(r for r in report["capped_complete_reference_receivers"] if r["source_kind"] == "rare-central-sector")
    normal = report["capped_complete_reference_receivers"][0]
    assert rare["ledger"]["original_centre_acquisition_cap"] > normal["ledger"]["original_centre_acquisition_cap"]
    assert rare["actual_original_centre_draws"] > normal["actual_original_centre_draws"]


def test_approximate_commutator_inequality_on_arbitrary_mixed_qutrits():
    rng = np.random.default_rng(17051)
    U = qutrit_sector_actions(1)
    for _ in range(12):
        A = rng.normal(size=(3, 3))+1j*rng.normal(size=(3, 3))
        rho = A @ A.conj().T
        rho /= np.trace(rho)
        for x, y in product(range(9), repeat=2):
            defect = max(1-abs(np.trace(U[x] @ rho)), 1-abs(np.trace(U[y] @ rho)))
            dx, dy = words(2, 3)[x], words(2, 3)[y]
            c = (dx[1]*dy[0]-dy[1]*dx[0]) % 3
            exact_commutator_square = abs(np.exp(2j*np.pi*c/3)-1)**2
            assert exact_commutator_square <= 32*defect+1e-12


@pytest.mark.parametrize("callback", [
    lambda: BilinearExtension(True, ((0,),)), lambda: BilinearExtension(9, ((0,),)),
    lambda: BilinearExtension(2, ((0,),)), lambda: BilinearExtension(3, ((True,),)),
    lambda: resource_ledger(3, True, "1/4", 8), lambda: resource_ledger(3, 8, 0, 8),
    lambda: resource_ledger(3, 8, True, 8), lambda: resource_ledger(3, 8, .25, 8),
    lambda: resource_ledger(3, 8, "3/2", 8), lambda: resource_ledger(3, 8, "1/4", True),
    lambda: sector_fourier_control(np.eye(3)/3, 0), lambda: sector_fourier_control(np.eye(3)/3, True),
    lambda: sector_fourier_control(np.eye(3), 1), lambda: sector_fourier_control(np.eye(3)/3, 1, literal="yes"),
    lambda: kernel(((0, 3),), 2, 3),
    lambda: final_fourier_control(calibration_source("coset-mixed"), (), centre_fixed=True),
])
def test_invalid_source_or_access_promises_are_not_silently_granted(callback):
    with pytest.raises(ValueError):
        callback()


def test_independent_checker_replays_live_control_and_rejects_tampering(report, tmp_path):
    p = tmp_path/"control.json"
    p.write_text(json.dumps(report))
    checker = ROOT/"research/certificates/cyclic_centre_state_hsp_receiver_crosscheck.js"
    good = subprocess.run(["node", str(checker), str(p)], capture_output=True, text=True)
    assert good.returncode == 0, good.stderr
    assert json.loads(good.stdout)["status"] == "PASS"
    for category in range(9):
        bad = json.loads(json.dumps(report))
        if category == 0:
            bad["native_DHSP_source_reduction_supplied"] = True
        elif category == 1:
            bad["growing_integer_resource_ledgers"][0]["selected_sector_copy_quota"] -= 1
        elif category == 2:
            bad["complete_literal_sector_instruments"][0]["literal_Kraus_probabilities"][0] += .01
        elif category == 3:
            bad["capped_complete_reference_receivers"][0]["recovered_Bose_subgroup_elements"][1][1] = 1
        elif category == 4:
            bad["tiny_conditional_gap_countercontrol"]["exact_tensor_probability_if_second_character_nonzero"] = "0"
        elif category == 5:
            bad["capped_complete_reference_receivers"][0]["actual_total_original_copies"] -= 1
        elif category == 6:
            bad["derivation_sha256"] = "0"*64
        elif category == 7:
            bad["nonstabilizer_two_qudit_instruments"][0]["complete_literal_probabilities"][0] += .01
        else:
            fixed = next(r for r in bad["capped_complete_reference_receivers"] if r["successful_centre_fixed_branch"])
            fixed["quotient_overgroup_commutator_zero"] = True
        p.write_text(json.dumps(bad))
        result = subprocess.run(["node", str(checker), str(p)], capture_output=True, text=True)
        assert result.returncode != 0, f"tamper category {category} accepted"


def test_no_speedup_or_novelty_is_inferred_from_finite_calibration(report):
    for flag in ("all_central_extensions_solved", "native_DHSP_source_reduction_supplied",
                 "new_classical_HSP_speedup_claimed", "candidate_record_accepted",
                 "novelty_claimed", "Shor_level_result_claimed"):
        assert report[flag] is False
    json.dumps(report, allow_nan=False)
