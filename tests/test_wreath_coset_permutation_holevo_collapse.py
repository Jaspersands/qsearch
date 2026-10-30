"""Normalized source controls and fail-closed scope, not a copy barrier."""
from fractions import Fraction
import hashlib
from itertools import permutations
import json
import math

import numpy as np
import pytest

from theorems import wreath_coset_permutation_holevo_collapse as source


def test_old_hidden_set_is_not_a_subgroup():
    control = source.invalid_subgroup_counterexample()
    assert control["both_factors_in_proposed_set"]
    assert not control["product_in_proposed_set"]
    assert source.wreath_multiply(control["x"], control["y"]) == control["product"]


@pytest.mark.parametrize("tau", list(permutations(range(3))))
def test_valid_repair_is_a_conjugate_subgroup(tau):
    e = tuple(range(3))
    base = source.valid_subgroup(e)
    conjugator, inv = (e, tau, 0), (e, source.inverse(tau), 0)
    conjugated = {source.wreath_multiply(source.wreath_multiply(conjugator, h), inv) for h in base}
    actual = source.valid_subgroup(tau)
    assert conjugated == actual
    assert len(actual) == 12
    assert all(source.wreath_multiply(a, b) in actual for a in actual for b in actual)


@pytest.mark.parametrize("bad", [(), (0, 1), (0, 0, 2), (0, 1, 3), (False, 1, 2), tuple(range(5))])
def test_bounded_subgroup_enumeration_rejects_bad_or_large_inputs(bad):
    with pytest.raises(ValueError):
        source.valid_subgroup(bad)


@pytest.mark.parametrize("n,dims", [(3, [1, 1, 2]), (4, [1, 1, 2, 3, 3])])
def test_exact_plancherel_weights_and_holevo_not_collapse(n, dims):
    row = source.information_profile(n)
    weights = [Fraction(d*d, math.factorial(n)) for d in dims]
    assert Fraction(row["compressed_purity"]) == sum(p*p for p in weights)
    assert Fraction(row["raw_regular_coset_purity"]) == Fraction(1, math.factorial(n))
    assert Fraction(row["optimal_one_copy_guessing_probability"]) == sum(p*p for p in weights)
    assert Fraction(row["trace_distance_from_ensemble_average"]) == 1 - Fraction(len(dims), math.factorial(n))
    assert row["optimal_measurement_implemented"] is False
    assert row["one_copy_holevo_bits"] == pytest.approx(2*sum(float(p)*math.log2(d) for p, d in zip(weights, dims)))
    assert row["one_copy_holevo_bits"] == pytest.approx(row["secret_entropy_bits"] - row["plancherel_entropy_bits"])
    assert row["holevo_is_achieved_accessible_information"] is False


@pytest.mark.parametrize("n", [3, 4, 8, 16, 24, 32])
def test_one_copy_capacity_scales_up_not_down(n):
    row = source.information_profile(n)
    assert row["elementary_holevo_lower_bound_bits"] <= row["one_copy_holevo_bits"] <= row["secret_entropy_bits"]
    assert row["one_copy_holevo_bits"] > 1/n


@pytest.mark.parametrize("n", [True, None, 2, 3.0, 33, 10**6])
def test_profile_caps_prevent_unbounded_partition_enumeration(n):
    with pytest.raises(ValueError):
        source.information_profile(n)


def test_actual_native_and_compressed_s3_density_controls():
    row = source.finite_state_control_s3()
    assert row["all_states_normalized_positive"]
    assert row["states_checked"] == 6 and row["pair_overlaps_checked"] == 36
    assert row["raw_purity"] == pytest.approx(1/6)
    assert row["compressed_purity"] == pytest.approx(1/2)
    assert row["raw_holevo_bits"] == pytest.approx(4/3)
    assert row["compressed_holevo_bits"] == pytest.approx(4/3)
    assert row["raw_overlap_identity_max_residual"] < 1e-12


def test_entropy_rejects_unphysical_operators():
    for matrix in (np.diag([1., -1.]), np.eye(2), np.diag([1.1, -0.1]),
                   np.array([[1., 2.], [0., 0.]]), np.array([[float("nan")]])):
        with pytest.raises(ArithmeticError):
            source._entropy(matrix)


def _assert_scope(report):
    assert report["status"] == "WREATH_SOURCE_CORRECTED_AND_REPAIRED_FAMILY_CLASSICALLY_RECOVERED"
    for flag in ("general_copy_lower_bound_proved", "factorial_holevo_collapse_proved",
                 "general_code_equivalence_solved", "quantum_receiver_implemented",
                 "speedup_claim_allowed", "accepted_speedup_candidate"):
        assert report[flag] is False
    assert "theorems_proved" not in report and "scaling_profiles" not in report
    assert report["retracted_negative_ids"] == [source.NEGATIVE_RESULT_ID]
    for row in report["classical_recovery_controls"]:
        assert row["exact_recovery"] and not row["labels_read_as_permutations"]
        assert row["query_count"] == math.comb(row["n"], 2) + row["n"] + 1


def test_report_has_only_supported_claims():
    _assert_scope(source.build_report())
    assert not hasattr(source, "register_negative_result")


def test_live_report_hashes_and_retracted_registry_record():
    report = json.loads(source.REPORT.read_text())
    _assert_scope(report)
    assert report["producer_sha256"] == hashlib.sha256(source.Path(source.__file__).read_bytes()).hexdigest()
    assert report["derivation_sha256"] == hashlib.sha256(source.DERIVATION.read_bytes()).hexdigest()
    assert not any(r["id"] == source.NEGATIVE_RESULT_ID for r in json.loads(source.REGISTRY.read_text()))


def test_writer_applies_review_before_publishing_and_can_skip_it(tmp_path, monkeypatch):
    from theorems import nonabelian_barrier_scope_audit as quarantine

    events = []
    monkeypatch.setattr(source, "REPORT", tmp_path / "report.json")
    monkeypatch.setattr(source, "build_report", lambda: {"speedup_claim_allowed": False})
    monkeypatch.setattr(quarantine, "quarantine_reviewed_negatives", lambda: events.append("quarantine"))
    assert source.write_report() == source.REPORT
    assert events == ["quarantine"]
    source.write_report(write_registry=False)
    assert events == ["quarantine"]
    assert json.loads(source.REPORT.read_text()) == {"speedup_claim_allowed": False}


def test_writer_refuses_changed_evidence(tmp_path, monkeypatch):
    from theorems import nonabelian_barrier_scope_audit as quarantine

    def changed():
        raise ValueError("reviewed evidence changed")

    monkeypatch.setattr(source, "REPORT", tmp_path / "report.json")
    monkeypatch.setattr(source, "build_report", lambda: {})
    monkeypatch.setattr(quarantine, "quarantine_reviewed_negatives", changed)
    with pytest.raises(ValueError, match="evidence changed"):
        source.write_report()
    assert not source.REPORT.exists()
