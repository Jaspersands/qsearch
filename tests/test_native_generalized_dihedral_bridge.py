"""Actual native phase extraction and generalized-abelian sign gates."""
from fractions import Fraction
from itertools import product
import json
import math
import random
import subprocess

from flint import fmpq
import numpy as np
import pytest

from theorems.native_generalized_dihedral_bridge import (
    REPORT, AdditiveChart, BinaryPhaseSample, baseline_contract, binary_merge,
    extract_binary_source, extraction_budget, finite_control, project_native_density,
)
from cyclotomic_rescaling_gate import pairing, plus
from native_state_hsp_bridge import NativeGroup, ring_words
from native_uniform_descent_receiver import OriginalSource, forward_fixture
from native_descent_noise_composition import symmetric_error_kernel


@pytest.mark.parametrize("level", (1, 2, 3, 4))
def test_complete_native_additive_dual_chart_is_bijective_and_carries_pairing(level):
    chart, values = AdditiveChart(level), ring_words(level)
    assert len(set(chart.dual((v,)) for v in values)) == 3**level
    for a in values:
        assert chart.value(chart.coordinates((a,))) == (a,)
        assert chart.label(chart.dual((a,))) == (a,)
        for s in values:
            assert chart.character(chart.dual((a,)), chart.coordinates((s,))) == pairing(a, s, level)
            summed = chart.coordinates((plus(a, s, level),))
            assert summed == tuple((x+y) % m for x, y, m in zip(chart.coordinates((a,)), chart.coordinates((s,)), chart.orders))


@pytest.mark.parametrize("level", (1, 2, 3, 4, 16, 64, 128, 256))
@pytest.mark.parametrize("n", (1, 4))
def test_scalable_chart_has_actual_integer_inverse_without_domain_enumeration(level, n):
    chart, rng = AdditiveChart(level, n), random.Random(level+n)
    x = tuple(rng.randrange(m) for m in chart.orders)
    assert chart.coordinates(chart.value(x)) == x
    assert chart.label(chart.dual(chart.value(x))) == chart.value(x)
    T = chart.dual_matrix
    assert T[0][0]*T[1][1]-T[0][1]*T[1][0] == -1
    assert math.prod(chart.orders) == 3**(level*n)
    assert not chart.record()["basis_chart_is_a_field_shadow"]
    if level % 2:
        assert T[0][1] % 3 == 0


def test_characteristic_nine_ring_is_not_replaced_with_F3_cubed():
    chart = AdditiveChart(3)
    assert chart.orders == (9, 3)
    assert chart.coordinates(((3, 0),)) == (3, 0)
    assert chart.coordinates(((3, 0),)) != chart.coordinates(((0, 0),))
    assert chart.value((0, 1)) == ((8, 1),)


@pytest.mark.parametrize("level", (2, 3, 4, 16, 64, 128))
def test_integer_embedding_restriction_uses_only_actual_promised_phase_axes(level):
    n, rng, chart = 4, random.Random(level), AdditiveChart(level, 4)
    label_coordinates = tuple(rng.randrange(m) for m in chart.orders)
    label = chart.value(label_coordinates)
    secret = tuple((rng.randrange(chart.orders[2*i]), 0) for i in range(n))
    full = chart.character(chart.dual(label), chart.coordinates(secret))
    dual = chart.dual(label)
    restricted = sum((Fraction(dual[2*i]*secret[i][0], chart.orders[2*i]) for i in range(n)), Fraction()) % 1
    assert full == restricted
    assert chart.coordinates(secret)[1::2] == (0,)*n
    assert math.prod(chart.orders[::2]) == 3**(n*((level+1)//2))


@pytest.mark.parametrize("level", (1, 2, 3, 4))
def test_integer_secret_dual_label_marginal_is_uniform_without_favorable_filtering(level):
    chart, counts = AdditiveChart(level), {}
    for label in ring_words(level):
        k = chart.dual((label,))[0]
        counts[k] = counts.get(k, 0)+1
    assert len(counts) == chart.orders[0]
    assert set(counts.values()) == {chart.orders[1]}


@pytest.mark.parametrize("level", (1, 2, 3, 4))
def test_every_scalar_projection_has_constant_probability_and_true_unknown_phase(level):
    chart, G, values = AdditiveChart(level), NativeGroup(level), ring_words(level)
    for a, s in product(values, repeat=2):
        psi = G.supplied_phase_state((a,), (s,))
        sample, record = project_native_density((a,), np.outer(psi, psi.conj()), level, (0,))
        assert abs(record["success_probability"]-2/3) < 1e-12
        expected = psi[:2]/np.sqrt(2/3)
        assert np.max(abs(sample.state-np.outer(expected, expected.conj()))) < 1e-12
        theta = chart.character(sample.dual_label, chart.coordinates((s,)))
        assert abs(sample.state[1, 0]-np.exp(2j*np.pi*float(theta))/2) < 1e-12
        assert sample.original_indices == (0,)
        assert not record["state_prepared_from_secret"] and not record["success_filters_higher_label_digits"]


@pytest.mark.parametrize("level", (2, 3, 4))
@pytest.mark.parametrize("g_left,g_right", (("1", "1"), ("9/10", "3/5"), ("0", "1")))
def test_both_sign_merges_match_literal_CNOT_including_anisotropic_native_noise(level, g_left, g_right):
    G, chart, secret = NativeGroup(level, 2), AdditiveChart(level, 2), ((2, 1), (4, 2))
    left_label, right_label = G.vector(((1, 2), (3, 1))), G.vector(((3, 1), (2, 2)))
    samples = []
    for label, g, index in ((left_label, g_left, 0), (right_label, g_right, 1)):
        psi = G.supplied_phase_state(label, secret)
        rho = np.outer(psi, psi.conj())*symmetric_error_kernel(g)
        sample, _ = project_native_density(label, rho, level, (index,))
        theta = chart.character(sample.dual_label, chart.coordinates(secret))
        assert abs(sample.state[1, 0]-float(fmpq(g))*np.exp(2j*np.pi*float(theta))/2) < 1e-12
        samples.append(sample)
    U = np.eye(4)[[0, 1, 3, 2]]
    literal = (U@np.kron(samples[0].state, samples[1].state)@U.T).reshape(2, 2, 2, 2)
    for b in (0, 1):
        child, record = binary_merge(*samples, b)
        projected = literal[:, b, :, b]
        assert np.max(abs(child.state-2*projected)) < 1e-12
        assert abs(record["branch_probability"]-.5) < 1e-12
        theta = chart.character(child.dual_label, chart.coordinates(secret))
        assert abs(child.state[1, 0]-float(fmpq(g_left)*fmpq(g_right))*np.exp(2j*np.pi*float(theta))/2) < 1e-12
        assert child.original_indices == (0, 1)
        assert not record["either_sign_can_be_chosen_deterministically"]
        assert not record["unknown_secret_used"]


@pytest.mark.parametrize("M", (1, 4, 16))
@pytest.mark.parametrize("bits", (1, 4, 16))
def test_exact_paid_binomial_extraction_tail_bound(M, bits):
    r = extraction_budget(M, bits)
    C = r["original_copy_cap"]
    actual = sum(Fraction(math.comb(C, k)*2**k, 3**C) for k in range(M))
    assert actual <= Fraction(r["ideal_IID_extraction_failure_upper_exact"]) <= Fraction(1, 2**(bits+1))
    assert C == 3*(M+bits)
    assert not r["finite_source_or_preparation_promises_established_here"]


@pytest.mark.parametrize("n,L", ((1, 2), (1, 3), (2, 3), (4, 4)))
def test_finite_original_source_projection_counts_all_successes_and_rejects(n, L):
    control = finite_control(n, L, 12+n+L)
    r = control["extraction"]
    assert r["outputs_accepted"] == r["budget"]["required_binary_outputs"] == 16
    accepted = [i for p in r["projection_records"] if p["accepted"] for i in p["original_indices"]]
    assert sorted(accepted+r["rejected_original_indices"]) == list(range(r["original_inputs_supplied"]))
    assert len(r["original_source_records"]) == r["original_inputs_supplied"] <= r["budget"]["original_copy_cap"]
    assert not r["receiver_takes_hidden_secret"] and not r["hidden_shift_solved"]
    for merge in control["binary_merge_controls"]:
        assert merge["branches_are_alternative_counterfactual_replays_not_two_physical_outputs"]


def test_finite_input_exhaustion_does_not_generate_free_states():
    sample = next(forward_fixture(3, ((2, 1),), 13))
    budget = extraction_budget(4)
    source = OriginalSource([sample], 3, 1, budget["original_copy_cap"])
    outputs, r = extract_binary_source(source, 4, np.random.default_rng(1))
    assert len(outputs) <= 1 and source.count == 1
    assert r["status"] == "NO_COMPLETE_BATCH_FROM_PAID_FINITE_SOURCE" and r["source_exhaustion"]


def test_unlucky_extraction_stops_at_cap_instead_of_unbounded_retry():
    class RejectRNG:
        def random(self):
            return .999999
    budget = extraction_budget(4)
    source = OriginalSource(forward_fixture(3, ((2, 1),), 13), 3, 1, budget["original_copy_cap"])
    outputs, r = extract_binary_source(source, 4, RejectRNG())
    assert not outputs and source.count == budget["original_copy_cap"]
    assert len(r["rejected_original_indices"]) == source.count
    assert r["status"] == "NO_COMPLETE_BATCH_FROM_PAID_FINITE_SOURCE"


@pytest.mark.parametrize("kind", ("small_cap", "used_source", "reuse", "nonuniform", "coordinates", "wrong_group"))
def test_invalid_access_and_classical_coordinate_promises_rejected(kind):
    chart = AdditiveChart(3)
    source = OriginalSource(forward_fixture(3, ((2, 1),), 13), 3, 1, 100)
    s = BinaryPhaseSample((1, 0), chart.orders, np.ones((2, 2))/2, (0,))
    with pytest.raises(ValueError):
        if kind == "small_cap":
            extract_binary_source(OriginalSource([], 3, 1, 1), 4, np.random.default_rng(1))
        elif kind == "used_source":
            source.take()
            extract_binary_source(source, 4, np.random.default_rng(1))
        elif kind == "reuse":
            binary_merge(s, s, 0)
        elif kind == "nonuniform":
            project_native_density(((1, 0),), np.diag([1, 0, 0]), 3, (0,))
        elif kind == "coordinates":
            chart.value((9, 0))
        else:
            binary_merge(s, BinaryPhaseSample((1,), (9,), s.state, (1,)), 0)


@pytest.mark.parametrize("n,L", ((8, 2), (32, 64), (128, 256)))
def test_known_baseline_scope_does_not_become_an_implemented_new_solver(n, L):
    r = baseline_contract(n, L)
    assert r["entropy_log3_exact"] == n*L
    assert not r["complete_Kuperberg_sieve_implemented"] and not r["known_bound_is_a_new_quantum_algorithm"]
    assert not r["noise_robustness_inherited_from_ideal_theorem"] and not r["classical_original_data_separation_established"]
    assert r["conditional_integer_secret_entropy_log3_exact"] == n*((L+1)//2)
    assert not r["integer_embedding_verified_from_data"]


def test_independent_complete_bridge_replay():
    checker = REPORT.parents[1]/"certificates/native_generalized_dihedral_crosscheck.js"
    out = subprocess.run(["node", str(checker)], capture_output=True, text=True, check=True)
    r = json.loads(out.stdout)
    assert r["status"] == "PASS" and r["native_projection_records"] > 60
    assert r["actual_merge_branches"] == 64
    assert not r["complete_known_solver_implemented"]


@pytest.mark.parametrize("mutation", ("dual", "chart", "phase", "sign", "copies", "source", "tail", "claim", "clone"))
def test_independent_checker_rejects_free_source_wrong_characters_and_false_solver_claims(tmp_path, mutation):
    r = json.loads(REPORT.read_text())
    c = r["finite_original_source_controls"][0]
    p = c["extraction"]["projection_records"][0]
    if mutation == "dual":
        p["public_dual_label"][0] ^= 1
    elif mutation == "chart":
        r["scalable_chart_controls"][2]["dual_matrix_per_coordinate"][0][0] += 1
    elif mutation == "phase":
        p["normalized_retained_density"][0][1][0] += .1
    elif mutation == "sign":
        c["binary_merge_controls"][0]["both_actual_instrument_branches"][1]["label_sign"] = 1
    elif mutation == "copies":
        c["extraction"]["original_inputs_supplied"] -= 1
    elif mutation == "source":
        c["extraction"]["original_source_records"][0]["supplied_amplitudes"][1][0] += .1
    elif mutation == "tail":
        c["extraction"]["budget"]["ideal_IID_extraction_failure_upper_exact"] = "0"
    elif mutation == "claim":
        r["known_ideal_solver_is_implemented_here"] = True
    else:
        c["binary_merge_controls"][0]["branches_are_alternative_counterfactual_replays_not_two_physical_outputs"] = False
    target = tmp_path/"forged.json"
    target.write_text(json.dumps(r))
    out = subprocess.run(["node", str(REPORT.parents[1]/"certificates/native_generalized_dihedral_crosscheck.js"), str(target)], capture_output=True)
    assert out.returncode != 0
