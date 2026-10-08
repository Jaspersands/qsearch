from copy import deepcopy
from fractions import Fraction
from itertools import product
import json
import subprocess

import numpy as np
import pytest

from vector_centre_state_hsp_receiver import (
    ROOT, CalibrationBackend, SpanAccumulator, VectorExtension, ZeroSumBuffer,
    affine_solution, calibration_amplitude, combine, conditional_action,
    exact_vector_control, label_stream, mixed_sector_instrument, nullspace,
    rank, rank_one_extension, receive, resource_ledger, run_controls,
    span_contains, vector_sector_instrument, word, words,
)


@pytest.fixture(scope="module")
def report():
    return run_controls()


@pytest.mark.parametrize("forms", [
    (((0, 0), (1, 0)), ((1, 2), (0, 1))),
    (((1, 2), (2, 1)), ((0, 0), (0, 0))),
    (((0, 1), (0, 0)), ((0, 0), (1, 0))),
])
def test_actual_vector_bilinear_group_is_associative_exponent_three(forms):
    G = VectorExtension(forms)
    gs = [((0, 0), (0, 0)), ((1, 0), (0, 1)), ((0, 1), (1, 2)), ((2, 1), (1, 1))]
    identity = ((0, 0), (0, 0))
    for g, h, u in product(gs, repeat=3):
        assert G.multiply(G.multiply(g, h), u) == G.multiply(g, G.multiply(h, u))
    for g in gs:
        assert G.multiply(G.multiply(g, g), g) == identity
    for g, h in product(gs, repeat=2):
        gh, hg = G.multiply(g, h), G.multiply(h, g)
        assert gh[0] == hg[0]
        assert tuple((a-b) % 3 for a, b in zip(gh[1], hg[1])) == G.commutator(g[0], h[0])


@pytest.mark.parametrize("k", [1, 2, 3])
def test_known_two_qutrit_action_is_a_full_linear_representation_in_every_sector(k):
    G = rank_one_extension(k)
    gs = [((0, 0), (0,)*k), ((1, 0), (1,)*k), ((0, 1), (2,)*k), ((2, 1), (0,)*k)]
    for lam in words(k, 3):
        for g, h in product(gs, repeat=2):
            assert np.allclose(conditional_action(lam, g) @ conditional_action(lam, h), conditional_action(lam, G.multiply(g, h)))


def test_quotient_section_is_homomorphic_only_mod_the_fixed_centre():
    G = rank_one_extension(2)
    chart = G.quotient_chart(((1, 0), (0, 1)), ((1, 0),))
    assert not chart.record()["full_preimage_group_is_abelian"]
    assert chart.record()["section_homomorphism_only_mod_fixed_centre"]
    errors = []
    for t, u in product(words(chart.dimension, 3), repeat=2):
        g = G.multiply(chart.section(t), chart.section(u))
        h = chart.section(tuple((a+b) % 3 for a, b in zip(t, u)))
        assert g[0] == h[0]
        z = tuple((a-b) % 3 for a, b in zip(g[1], h[1]))
        assert span_contains(chart.central_fixed_frame, z)
        errors.append(z)
    assert any(any(z) for z in errors)
    with pytest.raises(ValueError, match="commutator escapes"):
        G.quotient_chart(((1, 0), (0, 1)), ())
    with pytest.raises(ValueError, match="independent"):
        G.quotient_chart(((1, 0), (1, 0)), ((1, 0),))


def test_symmetric_full_group_needs_half_quadratic_gauge():
    G = VectorExtension((((1, 2), (2, 1)),))
    chart = G.quotient_chart(((1, 0), (0, 1)), ())
    assert chart.record()["full_preimage_group_is_abelian"]
    assert chart.section((1, 0, 0))[1] == (2,)
    for t, u in product(words(chart.dimension, 3), repeat=2):
        assert G.multiply(chart.section(t), chart.section(u)) == chart.section(tuple((a+b) % 3 for a, b in zip(t, u)))


@pytest.mark.parametrize("k", [1, 2, 8, 32, 128, 512])
@pytest.mark.parametrize("d", [1, 8, 128])
def test_exact_ledger_pays_for_all_witnesses_and_all_ordered_pairs(k, d):
    L = resource_ledger(d, k, Fraction(1, 7), 32)
    W, H = L["zero_sum_window"], L["required_included_witnesses_per_unfixed_central_element"]
    delta = Fraction(L["conditional_modulus_defect_threshold"])
    assert 32*delta < 3
    assert delta*H/(2*W) >= 4*d+32+2
    assert L["original_central_measurement_count"]*Fraction(1, 14) >= 2*(W+H)+8*(2*k+32+2)
    assert L["fresh_original_final_copy_count"]*Fraction(1, 14) >= 2*(d+k)+32+2
    assert Fraction(L["total_ideal_failure_upper"]) == Fraction(3, 2**34)
    assert not L["minimum_conditional_gap_assumed"]
    assert not L["same_central_sector_collision_required"]


@pytest.mark.parametrize("epsilon", [True, 0, -1, "2", .5])
def test_ledger_rejects_invalid_or_inexact_gap(epsilon):
    with pytest.raises(ValueError):
        resource_ledger(2, 2, epsilon, 4)


@pytest.mark.parametrize("k,count,skew", [(1, 101, Fraction(1)), (2, 503, Fraction(1, 7)), (5, 1000, Fraction(1))])
def test_streaming_selector_uses_each_register_once_and_bounds_its_only_tail(k, count, skew):
    selector = ZeroSumBuffer(k, retain_blocks=True)
    labels = list(label_stream(21771, count, k, skew=skew))
    for lam in labels:
        selector.push(lam)
    c = selector.finish()
    included = [i for block in c["blocks"] for i in block["original_indices"]]
    assert len(set(included)) == len(included)
    assert set(included).isdisjoint(c["leftover_original_indices"])
    assert sorted(included+list(c["leftover_original_indices"])) == list(range(count))
    assert len(c["leftover_original_indices"]) < (k+1)**2
    assert c["maximum_live_conditional_registers"] <= (k+1)**2
    for b in c["blocks"]:
        assert all(not sum(labels[i][j] for i in b["original_indices"]) % 3 for j in range(k))
    assert not c["retained_characters_claimed_IID"]
    assert not c["distinct_indices_certify_physical_IID_copies"]


def test_large_vector_centre_control_does_not_require_repeated_sectors(report):
    c = report["large_distinct_sector_coverage_control"]
    assert c["distinct_label_count"] > .99*c["original_inputs"]
    assert c["largest_identical_sector_bucket"] < 3
    assert c["included_original_inputs"] > c["original_inputs"]-(12+1)**2
    assert any(len(set(map(tuple, b["central_characters"]))) > 1 for b in c["blocks"])
    assert not c["full_confidence_copy_ledger_met_by_this_pool"]


def test_cocycle_projection_cancellation_alone_loses_hidden_lift_phase():
    labels = ((1, 1), (2, 1))  # First coordinate sums to zero, whole vector does not.
    data = [calibration_amplitude(lam, (0, 0), (0, 1), "nonnormal-line") for lam in labels]
    vectors = [np.array(c)*np.exp(2j*np.pi*np.array(t)/3) for c, t in data]
    with pytest.raises(ValueError, match="full VECTOR"):
        vector_sector_instrument(labels, vectors)
    x = ((0, 1), (0, 0))
    moment = np.prod([np.vdot(v, conditional_action(lam, x) @ v) for v, lam in zip(vectors, labels)])
    assert abs(moment) == pytest.approx(1)
    assert abs(moment-1) > 1


def test_all_heterogeneous_literal_branches_and_nonstabilizers_are_retained(report):
    assert len(report["exact_two_qutrit_heterogeneous_instruments"]) == 5
    for c in report["exact_two_qutrit_heterogeneous_instruments"]:
        assert c["literal_Kraus_probabilities"] == pytest.approx(c["character_law_probabilities"], abs=2e-12)
        assert sum(c["literal_Kraus_probabilities"]) == pytest.approx(1)
        assert c["all_outcomes_retained"]
        assert not c["identical_conditional_state_promise_used"]
    for c in report["literal_heterogeneous_instruments"]:
        assert c["literal_Kraus_probabilities"] == pytest.approx(c["character_law_probabilities"], abs=2e-12)
        assert len(c["input_density_real_imag"]) == c["actual_conditional_copies_consumed"]


def test_approximate_eigenvector_commutator_rigidity_on_nondiagonal_mixed_inputs():
    rng = np.random.default_rng(78011)
    for lam in (1, 2):
        X = conditional_action((lam, 0), ((1, 0), (0, 0)))
        Z = conditional_action((lam, 0), ((0, 1), (0, 0)))
        for _ in range(32):
            A = rng.normal(size=(9, 9))+1j*rng.normal(size=(9, 9))
            rho = A @ A.conj().T
            rho /= np.trace(rho)
            assert min(abs(np.trace(X @ rho)), abs(np.trace(Z @ rho))) < 15/16


def test_original_skewed_source_law_is_not_silently_replaced_by_uniform_sampling(report):
    r = next(r for r in report["full_budget_reference_receivers"] if r["spectrum_uniform_mixture_weight"] == "1/4")
    f = r["literal_final_original_instrument"]
    probabilities = list(map(Fraction, f["exact_mixture_probabilities"]))
    assert probabilities[0] == Fraction(3, 4)+Fraction(1, 4*3**len(r["final_law_active_uniform_character_frame"]))
    assert max(probabilities) > 3*min(p for p in probabilities if p)
    assert f["literal_Kraus_probabilities"] == pytest.approx(list(map(float, probabilities)), abs=2e-12)


def test_all_full_budget_reference_runs_recover_actual_subgroup_and_pay_for_copies(report):
    for r in report["full_budget_reference_receivers"]:
        L, c = r["ledger"], r["coverage"]
        assert r["status"] == "FULL_BUDGET_REFERENCE_RECOVERED"
        assert c["original_inputs"] == L["original_central_measurement_count"]
        assert r["actual_original_copies_consumed"] == L["total_original_copy_cap"]
        assert r["actual_known_controlled_R_calls"] <= L["known_controlled_R_call_cap"]
        assert sum(b["count"] for b in r["block_character_histogram"]) == c["block_count"]
        assert sum(b["count"] for b in r["final_character_histogram"]) == L["fresh_original_final_copy_count"]
        Z = r["learned_fixed_centre_basis"]
        assert len(r["lifted_subgroup_generators"]) == len(Z)+(1 if r["source_kind"] == "nonnormal-line" else 2)
        for x, z in r["lifted_subgroup_generators"]:
            residual = tuple((a-ta*x[0]-tb*x[1]) % 3 for a, ta, tb in zip(z, r["calibration_tau_a"], r["calibration_tau_b"]))
            assert span_contains(Z, residual)
        assert not r["quantum_advantage_inferred_from_calibration"]
        assert not r["uniform_control_flow_uses_hidden_source_parameters"]
        assert not r["source_IID_and_known_R_contract_verified_from_outcomes_alone"]


def test_baseline_really_reads_basis_outcomes_and_uses_independent_copies(report):
    for r in report["full_budget_reference_receivers"]:
        B = r["basis_readout_baseline"]
        assert B["status"] == "SOURCE_SPECIFIC_BASIS_READOUT_RECOVERED"
        assert len(B["central_label_rows"]) == B["alternative_fresh_copy_count"]
        for row, clock in zip(B["central_label_rows"], B["clock_computational_basis_outcomes"]):
            assert sum(a*b for a, b in zip(row, B["recovered_tau_b_mod_fixed_centre"])) % 3 == -clock % 3
        assert not B["copies_shared_with_collective_receiver"]
        assert not B["baseline_establishes_general_StateHSP_classical_algorithm"]


def test_conditional_inputs_cannot_be_reused_or_mislabeled():
    backend = CalibrationBackend(2, "nonnormal-line", 12, (), Fraction(1), 4)
    lam = backend.measure_centre(0)
    record = {"original_indices": (0,), "central_characters": (lam,)}
    backend.measure_block(record)
    with pytest.raises(ValueError, match="reused"):
        backend.measure_block(record)
    with pytest.raises(ValueError, match="fresh"):
        backend.measure_centre(0)


def test_zero_dimensional_quotient_and_affine_field_solver_are_well_defined():
    assert nullspace(((),), 0) == ()
    assert combine((), (), 0) == ()
    assert SpanAccumulator(0).kernel() == ()
    assert affine_solution(((1, 1),), (2,), 2) == (2, 0)
    with pytest.raises(ValueError, match="inconsistent"):
        affine_solution(((0, 0),), (1,), 2)


def test_uniform_control_flow_can_use_general_vector_B_without_state_tables():
    G = VectorExtension((((0, 1, 2), (2, 0, 1), (1, 2, 0)), ((1, 0, 0), (0, 1, 0), (0, 0, 1))))
    class TrivialRepresentationControl:
        # Known R(g)=I and an arbitrary state: the actual subgroup is G.
        def measure_centre(self, index):
            return (0, 0)
        def measure_block(self, block):
            return (0, 0, 0)
        def measure_original(self, chart, index):
            return (0,)*chart.dimension
    r = receive(G, Fraction(1), 1, TrivialRepresentationControl())
    assert len(r["lifted_subgroup_generators"]) == G.d+G.k
    assert not r["quotient_chart"]["full_preimage_group_is_abelian"]
    assert r["quotient_chart"]["dimension"] == G.d


def test_independent_exact_checker(report, tmp_path):
    target = tmp_path/"report.json"
    target.write_text(json.dumps(report))
    result = subprocess.run(["node", str(ROOT/"research/certificates/vector_centre_state_hsp_receiver_crosscheck.js"), str(target)], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["exact_heterogeneous_two_qutrit_branches"] == 45


@pytest.mark.parametrize("mutation", ["phase", "reuse", "tail", "cost", "quotient", "lift", "probability", "baseline", "scope", "digest"])
def test_independent_checker_rejects_false_artifacts(report, tmp_path, mutation):
    bad = deepcopy(report)
    pool = bad["large_distinct_sector_coverage_control"]
    r = bad["full_budget_reference_receivers"][0]
    if mutation == "phase":
        bad["exact_two_qutrit_heterogeneous_instruments"][0]["central_characters"] = ((1, 1), (2, 0))
    elif mutation == "reuse":
        pool["blocks"][1]["original_indices"] = pool["blocks"][0]["original_indices"]
    elif mutation == "tail":
        pool["leftover_original_indices"] = list(range(pool["zero_sum_window"]))
    elif mutation == "cost":
        r["ledger"]["original_central_measurement_count"] -= 1
    elif mutation == "quotient":
        bad["full_budget_reference_receivers"][2]["quotient_chart"]["full_preimage_group_is_abelian"] = True
    elif mutation == "lift":
        bad["full_budget_reference_receivers"][1]["lifted_subgroup_generators"] = []
    elif mutation == "probability":
        r["literal_final_original_instrument"]["exact_mixture_probabilities"][0] = "1"
    elif mutation == "baseline":
        r["basis_readout_baseline"]["copies_shared_with_collective_receiver"] = True
    elif mutation == "scope":
        bad["new_classical_HSP_speedup_claimed"] = True
    else:
        bad["producer_sha256"] = "0"*64
    target = tmp_path/"bad.json"
    target.write_text(json.dumps(bad))
    result = subprocess.run(["node", str(ROOT/"research/certificates/vector_centre_state_hsp_receiver_crosscheck.js"), str(target)], capture_output=True, text=True)
    assert result.returncode != 0
