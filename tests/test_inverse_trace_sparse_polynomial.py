from copy import deepcopy
from itertools import product

import pytest

from theorems.explicit_quadratic_opi import element, encoded, field
from theorems.inverse_trace_smt import verify_word
from theorems import inverse_trace_sparse_polynomial as sparse


def singleton(bits=7, points=None, checks=6, one=0):
    points = [0]+list(range(16, 64)) if points is None else list(points)
    targets = [0]*len(points)
    targets[one] = 1
    return {"bits": bits, "points": points, "targets": targets, "checks": checks,
            "field_modulus_coefficients": list(map(int, field(bits).modulus().coeffs()))}


def assert_scope(result):
    for key in ("native_unsatisfiability_claimed", "hardness_evidence",
                "unrestricted_target_solver_established", "uniform_sampler"):
        assert result[key] is False
    assert result["certificate_verified"] is True


def test_positive_native_n7_replays_c47_and_original_input_without_aliases():
    problem = singleton()
    problem["public_metadata"] = {"labels": ["original", "not resampled"]}
    original = deepcopy(problem)
    result = sparse.classify_affine_singleton(problem)
    assert problem == original == result["instance"]
    assert result == sparse.classify_affine_singleton(problem)
    assert result["status"] == "VERIFIED_NATIVE_WITNESS"
    assert result["affine_coefficients"] == [0, 47]
    assert result["certificate"]["positive_moments"] == [0]*6
    assert result["certificate"]["inverse_moment"] == 47
    assert result["certificate"]["obstruction"] is None
    assert result["witness"][0] == 1
    assert sum(bool(x) for x in result["witness"][1:]) == 47
    assert result["full_original_word_verified"]
    assert verify_word(problem, result["witness"])
    assert sparse.verify_moment_certificate(problem, result["certificate"])
    assert_scope(result)
    result["instance"]["points"][0] = 1
    result["instance"]["public_metadata"]["labels"].append("changed report")
    assert problem == original


@pytest.mark.parametrize("bits", [7, 11, 17])
def test_polynomial_basis_negative_native_family(bits):
    problem = singleton(bits, range(bits*bits), bits*bits//8)
    original = deepcopy(problem)
    result = sparse.classify_affine_singleton(problem)
    assert result["status"] == "AFFINE_ANSATZ_EXCLUDED"
    assert result["certificate"]["obstruction"] == {
        "kind": "NONZERO_CENTERED_MOMENT", "degree": 1, "value": bits*bits-1}
    assert result["witness"] is result["affine_coefficients"] is None
    assert not result["full_original_word_verified"]
    assert sparse.verify_moment_certificate(problem, result["certificate"])
    assert original == problem == result["instance"]
    assert_scope(result)


def test_all_positive_moments_zero_but_inverse_moment_zero_is_excluded():
    offsets = [r ^ w for r in (8, 16, 24, 40, 72, 88) for w in range(8)]
    problem = singleton(points=[0]+offsets)
    result = sparse.classify_affine_singleton(problem)
    assert len(problem["points"]) == 49
    assert result["certificate"]["positive_moments"] == [0]*6
    assert result["certificate"]["inverse_moment"] == 0
    assert result["certificate"]["obstruction"] == {
        "kind": "ZERO_CENTERED_INVERSE_MOMENT", "degree": -1, "value": 0}
    assert result["status"] == "AFFINE_ANSATZ_EXCLUDED"
    assert sparse.verify_moment_certificate(problem, result["certificate"])
    assert_scope(result)


def test_shift_scale_and_permutation_keep_actual_singleton_and_point_order():
    base = singleton()
    reference = sparse.classify_affine_singleton(base)
    scale, shift = element(7, 3), element(7, 71)
    transformed = [encoded(scale*element(7, p)+shift) for p in base["points"]]
    problem = singleton(points=transformed[::-1], one=48)
    original = deepcopy(problem)
    result = sparse.classify_affine_singleton(problem)
    slope = element(7, 47)/scale
    assert result["status"] == "VERIFIED_NATIVE_WITNESS"
    assert result["affine_coefficients"] == [encoded(-slope*shift), encoded(slope)]
    assert result["witness"] == reference["witness"][::-1]
    assert result["certificate"]["one_index"] == 48
    assert result["certificate"]["one_point"] == 71
    assert verify_word(problem, result["witness"])
    assert original == problem == result["instance"]


def test_check_boundary_includes_the_kth_moment_not_only_k_minus_one():
    for checks in (4, 14):
        assert sparse.classify_affine_singleton(singleton(checks=checks))["status"] == "VERIFIED_NATIVE_WITNESS"
    result = sparse.classify_affine_singleton(singleton(checks=15))
    assert result["status"] == "AFFINE_ANSATZ_EXCLUDED"
    assert result["certificate"]["positive_moments"][:14] == [0]*14
    assert result["certificate"]["obstruction"]["degree"] == 15


@pytest.mark.parametrize("points", [[0]+list(range(8, 16)), list(range(9))])
def test_complete_classification_matches_all_affine_polynomials_in_gf32(points):
    problem = singleton(5, points, 4)
    result = sparse.classify_affine_singleton(problem)
    values = [element(5, p) for p in points]
    accepted = []
    for constant, slope in product(range(32), repeat=2):
        z = [element(5, constant)+element(5, slope)*a for a in values[1:]]
        if any(v == 0 for v in z):
            continue
        word = [1]+[encoded(v+v**-1) for v in z]
        if verify_word(problem, word):
            accepted.append(([constant, slope], word))
    if accepted:
        assert accepted == [(result["affine_coefficients"], result["witness"])]
        assert result["status"] == "VERIFIED_NATIVE_WITNESS"
    else:
        assert result["status"] == "AFFINE_ANSATZ_EXCLUDED"


@pytest.mark.parametrize("problem,match", [
    (singleton(4, range(9), 4), "odd field degree"),
    (singleton(points=range(8), checks=4), "odd length"),
    (singleton(checks=3), "at least four"),
    (dict(singleton(), targets=[0]*49), "exactly one"),
    (dict(singleton(), targets=[1]*49), "exactly one"),
    (dict(singleton(), targets=[1, 1]+[0]*47), "exactly one"),
])
def test_unsupported_contract_is_an_error_never_ansatz_exclusion(problem, match):
    with pytest.raises(ValueError, match=match):
        sparse.classify_affine_singleton(problem)
    assert not sparse.verify_moment_certificate(problem, {})


@pytest.mark.parametrize("key,value", [
    ("bits", True), ("bits", 1), ("bits", 129),
    ("checks", True), ("checks", 0), ("checks", 49), ("checks", 4.0),
    ("points", [0]*49), ("points", [0, 128]+list(range(17, 64))),
    ("points", [False]+list(range(16, 64))), ("points", [[0]]+list(range(16, 64))),
    ("points", None), ("targets", "1"+"0"*48), ("targets", [1]),
    ("targets", [True]+[0]*48), ("targets", [2]+[0]*48),
    ("field_modulus_coefficients", [1, 0, 0, 0, 0, 0, 0, 1]),
    ("field_modulus_coefficients", [True, 1, 0, 0, 0, 0, 0, 1]),
    ("field_modulus_coefficients", None),
])
def test_malformed_native_contract_rejected_without_coercion(key, value):
    problem = dict(singleton(), **{key: value})
    with pytest.raises(ValueError):
        sparse.classify_affine_singleton(problem)
    assert not sparse.verify_moment_certificate(problem, {})


@pytest.mark.parametrize("problem", [None, [], {}, {"points": []}])
def test_missing_instance_fields_are_value_errors(problem):
    with pytest.raises(ValueError):
        sparse.classify_affine_singleton(problem)


@pytest.mark.parametrize("key", list(singleton()))
def test_every_required_field_is_checked(key):
    problem = singleton()
    del problem[key]
    with pytest.raises(ValueError):
        sparse.classify_affine_singleton(problem)


@pytest.mark.parametrize("key,value", [
    ("one_index", 1), ("one_index", False), ("one_point", 1),
    ("positive_moments", [1]+[0]*5), ("positive_moments", [False]*6),
    ("positive_moments", [0]*5), ("positive_moments", None),
    ("inverse_moment", 0), ("inverse_moment", True),
    ("obstruction", {"kind": "ZERO_CENTERED_INVERSE_MOMENT", "degree": -1, "value": 0}),
])
def test_positive_certificate_tampering_fails(key, value):
    problem = singleton()
    certificate = sparse.classify_affine_singleton(problem)["certificate"]
    certificate[key] = value
    assert not sparse.verify_moment_certificate(problem, certificate)


def test_exclusion_certificate_tampering_and_different_input_fail():
    problem = singleton(points=range(49))
    certificate = sparse.classify_affine_singleton(problem)["certificate"]
    assert not sparse.verify_moment_certificate(singleton(), certificate)
    for obstruction in (None, {}, [], {"kind": "NONZERO_CENTERED_MOMENT", "degree": True, "value": 48},
                        {"kind": "NONZERO_CENTERED_MOMENT", "degree": 1, "value": 49}):
        assert not sparse.verify_moment_certificate(problem, dict(certificate, obstruction=obstruction))
    for key in certificate:
        modified = dict(certificate)
        del modified[key]
        assert not sparse.verify_moment_certificate(problem, modified)
    assert not sparse.verify_moment_certificate(problem, dict(certificate, extra=True))
    assert not sparse.verify_moment_certificate(problem, None)


def test_native_verifier_failure_is_not_promoted_to_success(monkeypatch):
    calls = []

    def reject(instance, word):
        calls.append((deepcopy(instance), list(word)))
        return False

    monkeypatch.setattr(sparse, "verify_word", reject)
    problem = singleton()
    with pytest.raises(ArithmeticError, match="original native verification"):
        sparse.classify_affine_singleton(problem)
    assert len(calls) == 1 and calls[0][0] == problem and calls[0][1][0] == 1


def test_bad_internal_moment_replay_fails_closed(monkeypatch):
    monkeypatch.setattr(sparse, "verify_moment_certificate", lambda *_: False)
    with pytest.raises(ArithmeticError, match="moment certificate"):
        sparse.classify_affine_singleton(singleton(points=range(49)))
