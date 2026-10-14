from copy import deepcopy
from fractions import Fraction
from itertools import product
import json
import subprocess

import numpy as np
import pytest

from theorems import native_word_spectral_filter_audit as A


def stored():
    return json.loads(A.REPORT.read_text())


def node_check(payload):
    return subprocess.run([
        "node", "-e",
        "const A=require('./research/certificates/native_word_spectral_filter_audit_crosscheck.js');"
        "let s='';process.stdin.on('data',x=>s+=x);process.stdin.on('end',()=>console.log(JSON.stringify(A.verify(JSON.parse(s)))));",
    ], input=json.dumps(payload), text=True, capture_output=True, cwd=A.ROOT)


@pytest.mark.parametrize("family,degree", (
    ("CONSTANT", 0), ("NONZERO_KERNEL_BIAS", 1), ("GEOMETRIC", 8), ("CHEBYSHEV_ENDPOINT", 8),
))
def test_canonical_globally_bounded_filters(family, degree):
    spec = A.certified_filter(family, degree)
    coefficients = spec["ascending_coefficients"]
    assert len(coefficients) == degree + 1
    assert spec["polynomial_selected_independently_of_original_values"]
    for j in range(129):
        assert 0 <= A.polynomial_value(coefficients, Fraction(j, 128)) <= 1


@pytest.mark.parametrize("index", range(4))
def test_finite_effects_against_dense_matrix_polynomial(index):
    control = stored()["actual_native_source_controls"][index]
    rows, D = control["actual_native_word_rows"], control["word_dimension"]
    q = control["original_records"][0]["modulus"]
    frequencies = [tuple(r["frequency"]) for r in rows]
    K = np.asarray([[int(a == b) / D for b in frequencies] for a in frequencies])
    psi = np.exp(2j * np.pi * np.asarray([r["known_phase"] for r in rows]) / q) / np.sqrt(D)
    for f in control["spectral_filter_controls"]:
        coefficients = list(map(Fraction, f["filter"]["ascending_coefficients"]))
        result = np.zeros_like(K)
        for c in reversed(coefficients):
            result = result @ K + float(c) * np.eye(D)
        source = float(np.vdot(psi, result @ psi).real)
        null = float(np.trace(result) / D)
        assert source == pytest.approx(f["diagnostic_source_acceptance_probability"], abs=1e-9)
        assert null == pytest.approx(float(Fraction(f["IID_null_acceptance"])), abs=1e-9)
        assert abs(source - null) <= float(Fraction(f["absolute_source_null_gap_upper"])) + 1e-9


def test_same_original_word_classical_collision_moment_identity():
    control = stored()["actual_native_source_controls"][0]
    rows, D = control["actual_native_word_rows"], control["word_dimension"]
    q = control["original_records"][0]["modulus"]
    frequencies = [tuple(r["frequency"]) for r in rows]
    K = np.asarray([[int(a == b) / D for b in frequencies] for a in frequencies])
    psi = np.exp(2j * np.pi * np.asarray([r["known_phase"] for r in rows]) / q) / np.sqrt(D)
    for k in (1, 2):
        total = sum(np.exp(2j * np.pi * (group[-1]["known_phase"] - group[0]["known_phase"]) / q)
                    for group in product(rows, repeat=k + 1)
                    if all(r["frequency"] == group[0]["frequency"] for r in group))
        expectation = total / D ** (k + 1)
        assert expectation == pytest.approx(np.vdot(psi, np.linalg.matrix_power(K, k) @ psi), abs=1e-10)


def test_response_dependent_fibre_constant_mask_does_not_change_any_filter_probability():
    c = stored()["actual_native_source_controls"][2]
    raw = tuple(A.NoisyLinearRecord(tuple(r["label"]), r["value"], r["modulus"], r["source_id"]) for r in c["original_records"])
    q = raw[0].modulus
    adaptive_mask = (sum(r.value for r in raw) % q,)
    specs = tuple((f["filter"]["family"], f["filter"]["degree"]) for f in c["spectral_filter_controls"])
    out = A.finite_control(raw, adaptive_mask, specs)
    for old, new in zip(c["spectral_filter_controls"], out["spectral_filter_controls"]):
        assert old["exact_source_acceptance_root_polynomial"] == list(new["exact_source_acceptance_root_polynomial"])
        assert old["IID_null_acceptance"] == new["IID_null_acceptance"]


def test_exact_label_censuses_cover_composite_and_multidimensional_roots():
    censuses = stored()["complete_label_source_collision_censuses"]
    assert [(c["dimension"], c["root_digits"]) for c in censuses] == [(1, 1), (1, 2), (2, 1)]
    assert all(c["complete_original_label_banks"] == 81 for c in censuses)
    assert all(c["exact_mean_collision_probability"] == "11/27" for c in censuses)
    assert all(not c["census_is_new_oracle_problem_or_algorithm_candidate"] for c in censuses)


def test_degree_price_is_exponential_but_explicitly_scoped():
    ledgers = stored()["scaling_degree_ledgers"]
    assert [p["degree_lower_bound_bit_length"] for p in ledgers] == [50, 811, 3245, 12983]
    for p in ledgers:
        assert p["label_only_globally_bounded_raw_Gram_filter_required"]
        assert not p["degree_bound_is_a_general_quantum_query_lower_bound"]
        assert not p["efficient_different_preconditioner_or_noncommuting_measurement_excluded"]
        assert not p["balanced_fibres_or_per_matrix_uniformity_assumed"]


def test_implementation_error_that_swallows_gap_makes_bound_vacuous():
    p = A.degree_ledger(8, 8, 12, effect_error="1/8")
    assert p["residual_exact_filter_gap_required"] == "0"
    assert p["minimum_acceptance_polynomial_degree_under_scoped_model"] == 0
    assert not p["actual_quantum_decision_algorithm_supplied"]


def test_scope_countercontrols_do_not_become_global_no_go_or_candidates():
    p = stored()
    c = p["concentrated_labels_countercontrol"]
    assert c["collision_probability"] == "1"
    assert c["spectral_filter_controls"][0]["diagnostic_source_acceptance_probability"] == pytest.approx(1)
    assert c["spectral_filter_controls"][0]["IID_null_acceptance"] == "1/9"
    assert not p["unbounded_rescaling_countercontrol"]["valid_globally_bounded_filter"]
    assert not p["data_dependent_coefficients_countercontrol"]["label_only_filter_model_applies"]
    assert not p["all_quantum_measurements_or_preconditioners_excluded"]


@pytest.mark.parametrize("call", (
    lambda: A.certified_filter("CHEBYSHEV_ENDPOINT", 33),
    lambda: A.certified_filter("SPECTRUM_ONLY_RESCALE", 1),
    lambda: A.degree_ledger(0, 8, 12),
    lambda: A.degree_ledger(129, 129, 12),
    lambda: A.degree_ledger(8, 8, 12, preparation_error="-1/10"),
    lambda: A.collision_census(3, 3, 3),
))
def test_whole_work_and_model_scope_validation(call):
    with pytest.raises(ValueError):
        call()


def test_independent_exact_checker_replays_native_effects_and_scaling():
    result = node_check(stored())
    assert result.returncode == 0, result.stderr
    out = json.loads(result.stdout)
    assert out["verified"]
    assert out["exact_spectral_filters"] == 40
    assert out["actual_native_word_rows"] == 378


@pytest.mark.parametrize("kind", (
    "word-phase", "word-frequency", "filter-coefficient", "null", "gap-polynomial",
    "bound", "range-certificate", "data-dependent-filter", "degree", "error-budget",
    "general-query-claim", "classical-norm", "census", "source-law-claim", "speedup", "hash",
))
def test_independent_exact_checker_rejects_probability_and_scope_tampering(kind):
    p = deepcopy(stored())
    c, ledger = p["actual_native_source_controls"][0], p["scaling_degree_ledgers"][0]
    f = c["spectral_filter_controls"][2]
    if kind == "word-phase":
        c["actual_native_word_rows"][0]["known_phase"] ^= 1
    elif kind == "word-frequency":
        c["actual_native_word_rows"][0]["frequency"][0] ^= 1
    elif kind == "filter-coefficient":
        f["filter"]["ascending_coefficients"][1] = "2"
    elif kind == "null":
        f["IID_null_acceptance"] = "0"
    elif kind == "gap-polynomial":
        f["exact_source_minus_IID_null_root_polynomial"] = []
    elif kind == "bound":
        f["absolute_source_null_gap_upper"] = "0"
    elif kind == "range-certificate":
        f["filter"]["global_range_certificate"] = "bounded on actual eigenvalues only"
    elif kind == "data-dependent-filter":
        f["filter"]["polynomial_selected_independently_of_original_values"] = False
    elif kind == "degree":
        ledger["minimum_acceptance_polynomial_degree_under_scoped_model"] = "1"
    elif kind == "error-budget":
        ledger["residual_exact_filter_gap_required"] = "1/4"
    elif kind == "general-query-claim":
        ledger["degree_bound_is_a_general_quantum_query_lower_bound"] = True
    elif kind == "classical-norm":
        f["matched_classical_monomial_estimator"]["coefficient_l1_norm"] = "0"
    elif kind == "census":
        p["complete_label_source_collision_censuses"][0]["exact_mean_collision_probability"] = "1/3"
    elif kind == "source-law-claim":
        c["IID_label_source_law_established_by_this_fixture"] = True
    elif kind == "speedup":
        p["accepted_speedup_candidate"] = True
    else:
        p["producer_sha256"] = "0" * 64
    assert node_check(p).returncode != 0
