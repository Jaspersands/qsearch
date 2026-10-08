from copy import deepcopy
from fractions import Fraction
import hashlib
from itertools import combinations, product
import json
import math
import subprocess

import numpy as np
import pytest

from ternary_batch_fiber_compiler import pointed_minor
from ternary_cyclic_extractor import random_even_source
from ternary_native_block_walk import SIGNATURES, signature_count
from ternary_residual_fiber_cooling import (
    DERIVATION, REPORT, ResidualFiberParent, cold_population_certificate,
    complete_warm_moment_census, energy_barrier_population, warm_population_moments,
)


@pytest.fixture(scope="module")
def artifact():
    return json.loads(REPORT.read_text())


@pytest.fixture(scope="module")
def parent():
    source = random_even_source(2, 4, 5, 89881)
    return ResidualFiberParent(source, source.value((0,)*5))


def test_native_pointed_three_word_minor_covers_all_control_triples():
    words = tuple(product(range(3), repeat=2))
    for triple in combinations(words, 3):
        assert abs(pointed_minor(triple)["determinant"]) == 1


def test_full_population_normalizer_moments_for_every_fixed_original_word():
    census = complete_warm_moment_census()
    assert census["entire_native_label_matrices"] == 81
    assert census["original_word_targets_per_matrix"] == 9
    assert census["mean_normalizer_by_fixed_original_word"] == ["5/9"]*9
    assert census["variance_normalizer_by_fixed_original_word"] == ["1/81"]*9
    formula = warm_population_moments(1, 3, 2)
    assert Fraction(formula["source_weighted_warm_fiber_success_upper"]) >= Fraction(census["source_weighted_mean_warm_fiber_probability_exact"])


@pytest.mark.parametrize("n,q,M", [(1, 3, 2), (8, 9, 24), (128, 243, 648), (512, 729, 3080)])
def test_warm_moments_keep_the_self_word_and_only_pairwise_independence(n, q, M):
    a = warm_population_moments(n, q, M)
    mu, mu2 = Fraction(a["mean_nonself_weight_exact"]), Fraction(a["second_nonself_weight_exact"])
    D = 3**M
    assert Fraction(a["mean_normalizer_exact"]) == Fraction(1, D)+Fraction(D-1, D)*mu
    assert Fraction(a["normalizer_variance_exact"]) == Fraction(D-1, D*D)*(mu2-mu*mu)
    assert a["warm_state_preparation_granted_not_implemented"]
    assert a["distinct_nonself_weights_pairwise_independent_by_pointed_unit_minor"]


@pytest.mark.parametrize("z", [0, "0", -1, 2, True, 0.25])
def test_warm_moments_reject_undefined_or_float_temperature(z):
    with pytest.raises(ValueError):
        warm_population_moments(1, 3, 2, z)


@pytest.mark.parametrize("t", ["1", "1/2", "1/4"])
def test_actual_local_residual_parent_changes_all_unmarked_classes(parent, t):
    table = parent.conditional((1, 0, 2, 1, 0), (0, 2), t)
    assert table["local_evaluations_charged"] == 9
    for entry in table["entries"]:
        w = [1, 0, 2, 1, 0]
        w[0], w[2] = entry["digits"]
        f = parent.source.value(w)
        e = sum(a != b for a, b in zip(f, parent.target))
        assert tuple(entry["full_frequency"]) == f
        assert entry["residual_energy"] == e
        assert Fraction(entry["relative_amplitude"]) == Fraction(t)**e
    assert not table["full_fiber_count_oracle_used"]


@pytest.mark.parametrize("t", ["0", "-1", "2", True, 0.5])
def test_residual_conditionals_reject_invalid_temperature(parent, t):
    with pytest.raises(ValueError):
        parent.conditional((0,)*5, (0,), t)


@pytest.mark.parametrize("kind", ["word", "work", "local"])
def test_no_partial_residual_parent_certificate(parent, kind):
    with pytest.raises(ValueError):
        if kind == "word":
            parent.reference(1, "1/2", max_words=242)
        elif kind == "work":
            parent.reference(1, "1/2", max_work=1)
        else:
            parent.conditional((0,)*5, (0, 1), "1/2", max_local_words=8)


def test_large_reference_preflight_never_builds_the_block_menu(monkeypatch):
    p = ResidualFiberParent(random_even_source(8, 4, 128, 99317), (0,)*8)
    monkeypatch.setattr("ternary_residual_fiber_cooling.combinations", lambda *a: pytest.fail("huge block menu"))
    with pytest.raises(ValueError):
        p.reference(64, "1/2")
    assert p.conditional((0,)*128, (0, 31, 127), "1/2")["local_evaluations_charged"] == 27


@pytest.mark.parametrize("t", ["1/2", "1/4"])
def test_exact_parent_ground_state_and_cross_operator_schur_bound(parent, t):
    r = parent.reference(1, t)
    D = len(r["complete_words"])
    H = np.zeros((D, D))
    for i, row in enumerate(r["parent_rows"]):
        for j, value in row:
            H[i, j] = float(Fraction(value))
    assert np.max(abs(H-H.T)) < 1e-13
    assert np.linalg.eigvalsh(H)[0] >= -1e-12
    g = np.array([float(Fraction(t)**e) for e in r["complete_residual_energies"]])
    assert np.linalg.norm(H@g) < 1e-12
    marked = r["marked_word_indices"]
    outside = [i for i in range(D) if i not in marked]
    norm = np.linalg.svd(H[np.ix_(marked, outside)], compute_uv=False)[0]
    assert norm*norm <= float(Fraction(r["cross_operator_norm_squared_Schur_upper"]))+1e-13


def test_population_energy_barrier_is_all_signature_not_seeded_sampling():
    n, q, M, k = 512, 729, 3080, 6
    c = energy_barrier_population(n, q, M, k)
    exact = signature_count(M, k)*2**(n//3)*Fraction(q+1, 2*q)**n
    assert Fraction(c["probability_any_small_signature_below_energy_threshold_upper"]) == exact
    assert exact < Fraction(1, 2**240)
    assert c["minimum_boundary_energy_on_good_labels"] == n//3+1
    assert c["hotter_excursions_are_outside_scope"]


def test_cold_warm_start_cannot_be_called_polynomial_eraser():
    c = cold_population_certificate(512, 729, 3080, 6, 512**2)
    assert Fraction(c["source_weighted_cold_raw_fiber_success_upper"]) < Fraction(1, 2**240)
    assert not c["arbitrary_quantum_or_hot_schedule_lower_bound"]
    assert c["arbitrary_diagonal_controls_covered"]


def test_warm_state_grant_and_vacuous_small_controls_are_retained(artifact):
    assert artifact["finite_cold_dynamics"]["complete_warm_state_granted_not_prepared"]
    assert not artifact["finite_cold_dynamics"]["numeric_control_is_rigorous_roundoff_certificate"]
    assert artifact["hot_temperature_excursions_are_not_excluded"]
    assert artifact["population_cold_ledgers"][0]["source_weighted_cold_raw_fiber_success_upper"] == "1"


def test_report_hash_and_no_unsupported_algorithm_claims(artifact):
    assert artifact["derivation_sha256"] == hashlib.sha256(DERIVATION.read_bytes()).hexdigest()
    for flag in ("arbitrary_quantum_or_hot_schedule_lower_bound", "efficient_fiber_eraser_supplied", "quantum_speedup_proved", "candidate_record_accepted", "novelty_claim"):
        assert artifact[flag] is False


def test_independent_checker():
    r = subprocess.run(["node", "research/certificates/ternary_residual_fiber_cooling_crosscheck.js"], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert json.loads(r.stdout)["status"] == "PASS"


@pytest.mark.parametrize("case", ["row", "energy", "moment", "hot", "population"])
def test_independent_checker_rejects_tampered_evidence(artifact, tmp_path, case):
    r = deepcopy(artifact)
    if case == "row":
        r["exact_parent_controls"][0]["parent_rows"][0][0][1] = "0"
    elif case == "energy":
        r["exact_parent_controls"][0]["complete_residual_energies"][0] = 100
    elif case == "moment":
        r["complete_warm_moment_census"]["variance_normalizer_by_fixed_original_word"][0] = "0"
    elif case == "hot":
        r["hot_temperature_excursions_are_not_excluded"] = False
    else:
        r["population_cold_ledgers"][-1]["energy_barrier_population"]["probability_any_small_signature_below_energy_threshold_upper"] = "0"
    p = tmp_path/"bad.json"; p.write_text(json.dumps(r))
    result = subprocess.run(["node", "research/certificates/ternary_residual_fiber_cooling_crosscheck.js", str(p)], capture_output=True, text=True)
    assert result.returncode != 0
