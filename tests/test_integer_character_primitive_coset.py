from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path

from flint import fmpz_mat
import pytest

from theorems import integer_character_primitive_coset as coset
from theorems import integer_character_resonance as resonance
from theorems.native_rlwe_primal_babai import exact_row_profile, nearest_plane


def test_prefix_is_minimal_and_rule_is_fixed_before_attack():
    primes = resonance.integer.prime_support(1024)
    d, head, total = coset.weighted_prefix(primes)
    assert d == 42
    assert primes[d-1] == 191
    assert head >= 3*total/4
    assert head-Q(1, primes[d-1]) < 3*total/4


@pytest.mark.parametrize("residue", [1, 2])
@pytest.mark.parametrize("centers", [[0, 0, 0], [13, -41, 3], [10**40, -7, 81]])
@pytest.mark.parametrize("integer_prefix", [True, False])
def test_rational_coset_rounding_matches_independent_fraction_babai(residue, centers, integer_prefix):
    order, labels = 54, [1, 7, 43]
    small = order//3
    _, original = coset.near.lattice_bases([a % small for a in labels], small)
    # A shear, sign change and permutation exercise rational target columns
    # as well as nontrivial Gram--Schmidt coefficients.
    rows = [original[2], [-v for v in original[1]],
            [original[0][j]+3*original[1][j]-2*original[2][j] for j in range(3)]]
    if not integer_prefix:
        rows = [[original[0][j]+3*original[1][j] for j in range(3)],
                [original[2][j]+2*original[0][j] for j in range(3)],
                [-v for v in original[1]]]
    result = coset.primitive_nearest_plane(rows, labels, order, residue=residue, centers=centers)
    target = [Q(c-residue*a, 3) for c, a in zip(centers, labels)]
    independent = nearest_plane(rows, target)
    assert result["point"] == independent["point"]
    assert result["basis_coefficients"] == independent["basis_coefficients"]
    assert result["assignment"] % 3 == residue
    for a, e, c in zip(labels, result["prefix_error_numerators"], centers):
        assert (e-a*result["assignment"]+c) % order == 0
    profile = exact_row_profile(rows)
    trace = sum(profile["gs_squared"], Q())/(small*small)
    assert result["normalized_gs_trace_lower"] <= trace <= result["normalized_gs_trace_upper"]
    assert result["prefix_squared_error"] <= trace/4


def test_wrong_index_basis_is_rejected_not_used_for_a_covering_claim():
    labels, order = [1, 7, 43], 54
    _, rows = coset.near.lattice_bases([a % 18 for a in labels], 18)
    rows[0] = [2*v for v in rows[0]]
    with pytest.raises(ValueError, match="index"):
        coset.primitive_nearest_plane(rows, labels, order)


@pytest.mark.parametrize("residue", [0, 3, True, 1.0])
def test_primitive_class_is_enforced_not_just_nonzero(residue):
    _, rows = coset.near.lattice_bases([1, 7, 7], 18)
    with pytest.raises(ValueError, match="primitive residue"):
        coset.primitive_nearest_plane(rows, [1, 7, 43], 54, residue=residue)


def test_omitted_weights_are_charged_at_minus_one():
    primes = resonance.integer.prime_support(12)
    d, head, total = coset.weighted_prefix(primes)
    result = coset.score_guarantees(primes, [0]*d, 54, Q())
    expected = 2*head/total-1
    assert Q(result["witness_score_lower_with_worst_case_tail"]) == coset.dyadic_lower(expected)
    assert Q(result["all_prefix_targets_score_lower_with_worst_case_tail"]) == coset.dyadic_lower(expected)
    assert not result["omitted_coordinates_assumed_random"]
    assert not result["sampling_law_claimed"]
    # Large prefix error cannot inherit the perfect-prefix guarantee.
    error = [54]*d
    bad = coset.score_guarantees(primes, error, 54, Q(d))
    assert not bad["witness_threshold_certified"]
    assert not bad["all_prefix_targets_threshold_certified"]
    with pytest.raises(ValueError, match="does not cover"):
        coset.score_guarantees(primes, error, 54, Q())


def test_saved_native_witness_and_all_target_bound_replay():
    saved = json.loads(coset.REPORT.read_text())
    problem, _, input_hash = coset.load_native()
    rows = [list(map(int, row)) for row in saved["reduced_basis_decimal"]]
    assert saved["input_artifact_sha256"] == input_hash
    assert saved["producer_sha256"] == hashlib.sha256(Path(coset.__file__).read_bytes()).hexdigest()
    assert coset.certificate(problem, rows) == saved["certificate"]
    cert = saved["certificate"]
    assert cert["full_score"]["primitive"] and cert["full_score"]["accepted"]
    assert Q(cert["full_score"]["score_lower"]) > Q(3, 4)
    assert Q(cert["guarantees"]["all_prefix_targets_score_lower_with_worst_case_tail"]) > Q(1, 2)
    assert saved["predeclared_policy"]["nearest_plane_calls"] == 1
    assert not saved["cost"]["group_table_used"]
    assert not saved["cost"]["prior_1024_dimensional_LLL_basis_used"]
    assert not saved["cost"]["full_CVP_algorithm_executed"]
    assert not saved["asymptotic"]["polynomial_time_classical_theorem"]
    assert not saved["asymptotic"]["LLL_scaling_guarantee"]
    assert not saved["asymptotic"]["quantum_hardness_or_speedup_proved"]


def test_native_all_gram_pivots_checked_by_independent_determinants():
    saved = json.loads(coset.REPORT.read_text())
    cert = saved["certificate"]
    rows = [list(map(int, row)) for row in saved["reduced_basis_decimal"]]
    d = len(rows)
    order = 2*3**(saved["problem"]["modulus_exponent"]-2)
    matrix = fmpz_mat(rows)
    assert abs(int(matrix.det())) == order**(d-1)
    gram = matrix*matrix.transpose()
    previous, lower_units, upper_units = 1, 0, 0
    for k, normalized in enumerate(map(int, cert["normalized_gram_pivots_decimal"]), 1):
        leading = fmpz_mat([[gram[i, j] for j in range(k)] for i in range(k)])
        determinant = int(leading.det())
        assert determinant == normalized*order**(2*k-2)
        floor, remainder = divmod(determinant << 96, previous*order*order)
        lower_units += floor
        upper_units += floor+bool(remainder)
        previous = determinant
    assert Q(lower_units, 2**96) == Q(cert["normalized_gs_trace_lower"])
    assert Q(upper_units, 2**96) == Q(cert["normalized_gs_trace_upper"])
