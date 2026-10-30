from copy import deepcopy
import json
from functools import reduce
from operator import xor

import pytest

from theorems import mersenne_partial_norm_filter as partial
from theorems import mersenne_reciprocal_curve as native
from theorems.explicit_quadratic_opi import element, encoded, field


@pytest.fixture(scope="module")
def result():
    return partial.analyze_balanced_factors(partial.fixture_instance())


def test_fixture_is_the_unchanged_native_input():
    instance = partial.fixture_instance()
    assert instance == native.native_instance(17)
    assert instance["points"] == list(range(289))
    assert instance["targets"] == [1]*289
    assert instance["checks"] == 36 and instance["s"] == 3
    assert sum(value << j for j, value in enumerate(instance["field_modulus_coefficients"])) == 0x20009


def test_exact_computed_rank_minor_and_odd_trace_certificate(result):
    assert result["status"] == "BALANCED_FAMILY_EXCLUDED"
    assert result["degree_bound"] == 63
    assert result["product_degree_bound"] == result["native_numerator_degree_max"] == 252
    assert result["rank_by_conjugate"] == [56, 63, 63]
    assert result["coefficient_dimension"] == 1
    cert = result["exclusion_certificate"]
    minor = cert["rank_minor"]
    expected = [[1, ell] for ell in list(range(64, 95))+list(range(96, 289, 8))]
    expected += [[2, ell] for ell in [64, 65, 66, 67, 128, 192, 256]]
    assert minor["rows"] == expected
    assert minor["columns"] == list(range(1, 64))
    assert minor["determinant"] == 44208 == 0xacb0
    dependency = cert["trace_dependency"]
    assert dependency["indices"] == [0, 1, 3, 5, 6, 7, 8, 9, 12, 14, 18]
    assert dependency["derivative_powers"] == [
        73587, 19714, 22427, 29421, 23183, 82085,
        36680, 121879, 23810, 88157, 15149,
    ]
    assert reduce(xor, dependency["derivative_powers"]) == 0
    assert dependency["size"] == 11 and dependency["target_sum"] == 1
    assert partial.verify_exclusion_certificate(result["instance"], cert)
    assert result["certificate_verified"]
    for key in ("native_unsatisfiability_claimed", "unrestricted_solver",
                "uniform_sampler", "universal_collapse_claimed"):
        assert result[key] is False


def test_replay_is_independent_of_producer_and_not_a_hardcoded_row_order(result, monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("producer must not run during independent certificate replay")
    monkeypatch.setattr(partial, "_field_and_product", forbidden)
    monkeypatch.setattr(partial, "_conjugacy_rank", forbidden)
    monkeypatch.setattr(partial, "_trace_dependency", forbidden)
    cert = deepcopy(result["exclusion_certificate"])
    cert["rank_minor"]["rows"].reverse()
    assert partial.verify_exclusion_certificate(result["instance"], cert)


@pytest.mark.parametrize("raw_lambda", [1, 2, 12345])
def test_constant_family_meets_native_parity_but_not_all_one_targets(result, raw_lambda):
    instance = result["instance"]
    points = [element(17, a) for a in instance["points"]]
    lam = element(17, raw_lambda)
    word = []
    for i, alpha in enumerate(points):
        derivative = field(17).one()
        for j, beta in enumerate(points):
            if i != j:
                derivative *= alpha+beta
        word.append(encoded(lam/derivative))
    targets = [native.reciprocal_trace(17, 3, value) for value in word]
    correct = deepcopy(instance)
    correct["targets"] = targets
    assert native.verify_word(correct, word)
    assert not native.verify_word(instance, word)
    indices = result["exclusion_certificate"]["trace_dependency"]["indices"]
    assert sum(targets[i] for i in indices) % 2 == 0


def test_zero_targets_are_not_excluded():
    instance = partial.fixture_instance()
    instance["targets"] = [0]*289
    row = partial.analyze_balanced_factors(instance)
    assert row["status"] == "NO_TRACE_OBSTRUCTION"
    assert row["rank_by_conjugate"] == [56, 63, 63]
    assert row["constant_family_trace_dependency"] is None
    assert row["exclusion_certificate"] is None
    assert not row["certificate_verified"]
    assert native.verify_word(instance, [0]*289)


def test_n19_is_not_promoted_to_universal_collapse():
    instance = native.native_instance(19)
    before = deepcopy(instance)
    row = partial.analyze_balanced_factors(instance)
    assert instance == before == row["instance"]
    assert row["degree_bound"] == 78
    assert row["rank_by_conjugate"] == [64, 75, 77]
    assert row["coefficient_dimension"] == 2
    assert row["status"] == "NONCONSTANT_FAMILY_REMAINS"
    assert row["rank_minor"] is None and row["exclusion_certificate"] is None
    # A contradiction for constant factors cannot exclude the surviving space.
    assert row["constant_family_trace_dependency"] is not None
    assert not row["certificate_verified"]


@pytest.mark.parametrize("transform", ["reverse", "translate"])
def test_supplied_points_order_and_input_are_preserved(transform):
    instance = partial.fixture_instance()
    if transform == "reverse":
        instance["points"].reverse()
    else:
        instance["points"] = [value ^ 123 for value in instance["points"]]
    before = deepcopy(instance)
    row = partial.analyze_balanced_factors(instance)
    assert row["status"] == "BALANCED_FAMILY_EXCLUDED"
    assert instance == before == row["instance"]
    row["instance"]["targets"][0] = 0
    assert instance == before


@pytest.mark.parametrize("kind", [
    "wrong_tag", "missing_s", "old_s", "wrong_checks", "duplicate_point",
    "wrong_target_length", "boolean_point", "changed_modulus", "unsupported_n",
])
def test_invalid_or_unsupported_inputs_raise_not_exclude(kind):
    instance = partial.fixture_instance()
    if kind == "wrong_tag":
        instance["problem_family"] = "inverse_trace"
    elif kind == "missing_s":
        del instance["s"]
    elif kind == "old_s":
        instance["s"] = 4
    elif kind == "wrong_checks":
        instance["checks"] = 35
    elif kind == "duplicate_point":
        instance["points"][1] = 0
    elif kind == "wrong_target_length":
        instance["targets"].pop()
    elif kind == "boolean_point":
        instance["points"][0] = False
    elif kind == "changed_modulus":
        instance["field_modulus_coefficients"][1] ^= 1
    else:
        instance = native.native_instance(23)
    with pytest.raises(ValueError):
        partial.analyze_balanced_factors(instance)
    assert not partial.verify_exclusion_certificate(instance, {})


@pytest.mark.parametrize("kind", [
    "hash", "degree", "boolean_degree", "schema", "zero_determinant", "wrong_determinant",
    "duplicate_row", "wrong_valid_row", "bad_conjugate", "bad_coefficient", "columns",
    "boolean_column", "empty_dependency", "duplicate_index", "out_of_range_index",
    "wrong_power", "wrong_point", "size", "field_sum", "target_sum", "extra_key",
])
def test_tampered_certificates_are_rejected(result, kind):
    cert = deepcopy(result["exclusion_certificate"])
    minor, dependency = cert["rank_minor"], cert["trace_dependency"]
    if kind == "hash":
        cert["instance_sha256"] = "0"*64
    elif kind == "degree":
        cert["degree_bound"] -= 1
    elif kind == "boolean_degree":
        cert["degree_bound"] = True
    elif kind == "schema":
        cert["schema_version"] = "1"
    elif kind == "zero_determinant":
        minor["determinant"] = 0
    elif kind == "wrong_determinant":
        minor["determinant"] ^= 1
    elif kind == "duplicate_row":
        minor["rows"][0] = minor["rows"][1][:]
    elif kind == "wrong_valid_row":
        minor["rows"][0] = [1, 95]
    elif kind == "bad_conjugate":
        minor["rows"][0][0] = 4
    elif kind == "bad_coefficient":
        minor["rows"][0][1] = 63
    elif kind == "columns":
        minor["columns"].reverse()
    elif kind == "boolean_column":
        minor["columns"][0] = True
    elif kind == "empty_dependency":
        dependency["indices"] = []
    elif kind == "duplicate_index":
        dependency["indices"][0] = dependency["indices"][1]
    elif kind == "out_of_range_index":
        dependency["indices"][-1] = 289
    elif kind == "wrong_power":
        dependency["derivative_powers"][0] ^= 1
    elif kind == "wrong_point":
        dependency["points"][0] ^= 1
    elif kind == "size":
        dependency["size"] += 1
    elif kind == "field_sum":
        dependency["field_sum"] = 1
    elif kind == "target_sum":
        dependency["target_sum"] = 0
    else:
        cert["unsatisfiable"] = True
    assert not partial.verify_exclusion_certificate(result["instance"], cert)


def test_rebound_all_zero_targets_still_fail_the_actual_contradiction(result):
    instance = deepcopy(result["instance"])
    instance["targets"] = [0]*289
    cert = deepcopy(result["exclusion_certificate"])
    assert not partial.verify_exclusion_certificate(instance, cert)
    cert["instance_sha256"] = partial._digest(instance)
    assert not partial.verify_exclusion_certificate(instance, cert)


def test_failed_independent_replay_cannot_be_reported_as_success(monkeypatch):
    monkeypatch.setattr(partial, "verify_exclusion_certificate", lambda *args: False)
    with pytest.raises(ArithmeticError, match="independent replay"):
        partial.analyze_balanced_factors(partial.fixture_instance())


def test_saved_report_replays_and_preserves_both_fixtures():
    report = json.loads(partial.REPORT.read_text(encoding="ascii"))
    assert len(report["results"]) == 2 and report["exclusion_count"] == 1
    assert report["results"][0]["instance"] == partial.fixture_instance()
    assert report["results"][1]["instance"] == native.native_instance(19)
    assert partial.verify_report(report)
    report["results"][0]["coefficient_dimension"] = 2
    assert not partial.verify_report(report)


def test_cli_stdout_and_saved_report_replay(capsys):
    assert partial.main([]) == 0
    report = json.loads(capsys.readouterr().out)
    assert len(report["results"]) == report["exclusion_count"] == 1
    assert partial.main(["--verify"]) == 0
    assert json.loads(capsys.readouterr().out) == {
        "verified": True, "result_count": 2, "exclusion_count": 1,
    }


def test_cli_malformed_report_fails_without_writing(monkeypatch, capsys):
    class BrokenReport:
        def read_text(self, **kwargs):
            return "not JSON"
    monkeypatch.setattr(partial, "REPORT", BrokenReport())
    assert partial.main(["--verify"]) == 1
    assert json.loads(capsys.readouterr().out)["verified"] is False


def test_cli_rejects_generation_option_during_replay():
    with pytest.raises(SystemExit) as error:
        partial.main(["--verify", "--include-n19"])
    assert error.value.code == 2
