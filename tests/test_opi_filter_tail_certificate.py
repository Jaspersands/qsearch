"""Native moment controls, exact LP dual verification and cutoff countercontrols."""
from copy import deepcopy
from fractions import Fraction
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

import theorems.opi_filter_tail_certificate as tails
from theorems.explicit_cubic_opi import (
    BooleanCubic, CubicOPI, REPORT as CUBIC_REPORT, instance,
)


def native_law(problem, moment_record):
    b = list(map(Fraction, moment_record["rational_Krawtchouk_coefficients"]))
    hist = [0]*(problem.length+1)
    for word in range(1 << problem.message_bits):
        hist[problem.score_count(word)] += 1
    norm = Fraction(moment_record["filter_normalization"])
    law = [Fraction(count, 1 << problem.message_bits)*
           sum(c*tails.krawtchouk(problem.length, j, s) for j, c in enumerate(b))**2/norm
           for s, count in enumerate(hist)]
    return law


@pytest.mark.parametrize("seed", [29, 71])
def test_all_allowed_moments_match_native_not_weighted_binomial_assumption(seed):
    p = instance(3, 5, 4, seed)
    record = tails.filter_moments(p, 1, order=2)
    law = native_law(p, record)
    assert sum(law) == 1
    for r, claimed in enumerate(record["normalized_score_moments"]):
        assert sum(prob*Fraction(s, p.length)**r for s, prob in enumerate(law)) == Fraction(claimed)
    for threshold in range(p.length+2):
        c = tails.tail_certificate(record, threshold)
        actual = sum(law[threshold:])
        assert Fraction(c["tail_probability_lower"]) <= actual <= Fraction(c["tail_probability_upper"])
        assert tails.verify_tail_certificate(record, c)


def test_native_distribution_can_be_radically_nonbinomial_at_unproved_orders():
    # Constant RS polynomials and identical predicates: score is either zero or N.
    N = 7
    T = tuple(1 << j for j in range(4))
    p = CubicOPI(4, N, 1, (T,)*N, (BooleanCubic(3, 0),)*N)
    record = tails.filter_moments(p, 0)
    law = native_law(p, record)
    assert law == [Fraction(1, 2)]+[Fraction(0)]*(N-1)+[Fraction(1, 2)]
    c = tails.tail_certificate(record, N)
    assert Fraction(c["tail_probability_upper"]) >= Fraction(1, 2)
    assert not record["weighted_binomial_law_is_the_native_full_score_distribution"]
    with pytest.raises(ValueError, match="dual-distance"):
        tails.filter_moments(p, 0, order=2)


def test_strict_second_moment_cutoff_cannot_be_bypassed():
    p = instance(4, 7, 3, 29)
    tails.filter_moments(p, 1, order=1)
    with pytest.raises(ValueError, match="dual-distance"):
        tails.filter_moments(p, 1, order=2)
    record = tails.filter_moments(p, 0, order=3)
    c = tails.tail_certificate(record, 5)
    broken = dict(record, filter_degree=1)
    with pytest.raises(ValueError, match="cutoff"):
        tails.verify_tail_certificate(broken, c)


def test_corrupted_pointwise_certificate_and_repetition_are_rejected():
    record = tails.filter_moments(instance(4, 7, 3, 29), 0)
    c = tails.tail_certificate(record, 5)
    broken = deepcopy(c)
    broken["minorant_coefficients"][0] = "100"
    with pytest.raises(ArithmeticError, match="pointwise"):
        tails.verify_tail_certificate(record, broken)
    broken = deepcopy(c)
    broken["independent_repetitions"][0]["success_lower"] = "-1"
    with pytest.raises(ArithmeticError, match="repetition"):
        tails.verify_tail_certificate(record, broken)


def test_failed_numerical_optimizer_returns_trivial_valid_bounds_not_hardness(monkeypatch):
    monkeypatch.setattr(tails, "linprog", lambda *a, **kw: SimpleNamespace(success=False, message="synthetic failure"))
    record = tails.filter_moments(instance(4, 7, 3, 29), 0)
    c = tails.tail_certificate(record, 5)
    assert c["tail_probability_lower"] == "0"
    assert c["tail_probability_upper"] == "1"
    assert c["lower_solver"]["status"] == "UNKNOWN_LP_ZERO_CERTIFICATE"
    assert tails.verify_tail_certificate(record, c)


def test_numerically_infeasible_dual_is_repaired_with_exact_support_checks(monkeypatch):
    record = tails.filter_moments(instance(4, 7, 3, 29), 0)
    monkeypatch.setattr(tails, "linprog", lambda *a, **kw: SimpleNamespace(
        success=True, eqlin=SimpleNamespace(marginals=[0.1, 0.7, 0.4, 0.2])))
    c = tails.tail_certificate(record, 5)
    assert Fraction(c["lower_solver"]["constant_repair"]) > 0
    assert tails.verify_tail_certificate(record, c)


def test_saved_artifact_hashes_moments_and_every_pointwise_certificate():
    if not tails.REPORT.exists():
        pytest.skip("live report not generated yet")
    report = json.loads(tails.REPORT.read_text())
    assert report["source_sha256"] == hashlib.sha256(Path(tails.__file__).read_bytes()).hexdigest()
    assert report["input_artifact_sha256"] == hashlib.sha256(CUBIC_REPORT.read_bytes()).hexdigest()
    for name, digest in report["dependency_sha256"].items():
        assert digest == hashlib.sha256((Path("theorems")/name).read_bytes()).hexdigest()
    assert not report["accepted_speedup_candidate"]
    for row in report["instances"]:
        for f in row["filters"]:
            record = f["moments"]
            replay = tails.filter_moments(SimpleNamespace(length=row["positions"], dimension=row["RS_dimension"]),
                                           record["filter_degree"], order=record["certified_moment_order"])
            assert replay == record
            for certificate in f["tail_certificates"]:
                assert tails.verify_tail_certificate(record, certificate)
