import itertools
import json
from fractions import Fraction
from pathlib import Path

import pytest
import sympy as sp

from native_rlwe_primal_babai import (
    dyadic_tail_bound, exact_profile, nearest_plane, negacyclic,
    primal_rows, source_certificate, mixture_tail_bound,
)


def test_negacyclic_graph_uses_original_small_secret_not_normalized_prior():
    a, q = [3, 4, 2, 1], 17
    rows = primal_rows(a, q)
    c = sp.Matrix(negacyclic(a))
    assert c[:, 1] == sp.Matrix([-1, 3, 4, 2])
    assert abs(sp.Matrix(rows).det()) == q**4
    for row in rows:
        assert (sp.Matrix(row[4:])-c*sp.Matrix(row[:4])) % q == sp.zeros(4, 1)


def test_bareiss_profile_matches_direct_rational_orthogonalization():
    rows = primal_rows([2, 1, 3, 4], 11)
    rows = [list(row) for row in sp.Matrix(rows).lll().tolist()]
    result = exact_profile(rows)
    orthogonal = []
    for i, row in enumerate(rows):
        v = sp.Matrix(row)
        for j, u in enumerate(orthogonal):
            mu = (v.dot(u))/u.dot(u)
            assert mu == sp.Rational(result["mu"][i][j].numerator,
                                     result["mu"][i][j].denominator)
            v -= mu*u
        orthogonal.append(v)
        assert v.dot(v) == sp.Rational(result["gs_squared"][i].numerator,
                                      result["gs_squared"][i].denominator)
    assert result["leading_gram_determinants"][-1] == 11**8


def test_exact_nearest_plane_decodes_original_residual_in_its_cell():
    a, q = [5, 3], 101
    rows = sp.Matrix(primal_rows(a, q)).lll().tolist()
    profile = exact_profile(rows)
    c = negacyclic(a)
    count = 0
    for secret in itertools.product(range(-1, 2), repeat=2):
        for error in itertools.product(range(-1, 2), repeat=2):
            b = [(sum(c[i][j]*secret[j] for j in range(2))+error[i]) % q
                 for i in range(2)]
            target = [0, 0] + [(x+q//2) % q-q//2 for x in b]
            answer = nearest_plane(rows, target, profile)
            assert answer["point"][:2] == list(secret)
            assert answer["residual"] == [-x for x in secret]+list(error)
            count += 1
    assert count == 81


def test_tail_certificate_has_positive_floor_not_underflow():
    bound = dyadic_tail_bound([10**20, 10**21], 1)
    assert bound["failure_upper"] == Fraction(4, 2**4096) > 0
    assert bound["union_exponent_cap"] == 4096
    assert dyadic_tail_bound([1, 1], 1)["failure_upper"] == 1


def test_rational_transcendental_bridges_are_exact_integer_checks():
    assert Fraction(163, 60)**25 > 2**36
    assert Fraction(163, 60)**25 > 64**6
    with pytest.raises(ValueError, match="log upper"):
        source_certificate(64, [1]*128, 4)
    cert = source_certificate(64, [10**6]*128, Fraction(25, 6))
    assert cert["spherical"]["width_squared_upper"] == Fraction(513*625, 36)
    assert cert["elliptical"]["shape_failure_upper"] == Fraction(1, 4096)
    assert cert["elliptical"]["shape_dyadic_exponent"] == 17


def test_hidden_shape_loss_is_charged_once_not_given_to_solver():
    cert = source_certificate(64, [10**6]*128, Fraction(25, 6))
    e = cert["elliptical"]
    assert e["shape_conditioned_total_upper"] == e["shape_failure_upper"]+e["failure_upper"]
    assert e["total_failure_upper"] == min(e["shape_conditioned_total_upper"],
                                           e["unconditional_mixture"]["failure_upper"])
    assert not e["unconditional_mixture"]["hidden_shape_given_to_decoder"]


def test_unconditional_mixture_has_no_shape_oracle_or_unconditional_independence():
    result = mixture_tail_bound(64, [1, 10**6, 10**12], Fraction(25, 6))
    assert result["secret_error_independent_only_conditionally_on_shape"]
    for row in result["directions"]:
        assert 0 <= row["mixture_denominator_loss"] <= Fraction(1, 2)
        assert 0 < row["tail_upper"] <= 1
    assert result["failure_upper"] == 1


def test_latent_product_denominator_bound_retains_all_correlations():
    alpha = Fraction(1, 2)
    for composition in itertools.product(range(5), repeat=4):
        if sum(composition) != 4:
            continue
        product = Fraction(1)
        for x in composition:
            product *= 1-alpha*Fraction(x, 4)
        assert product >= 1-alpha
    # Concentrating the joint secret/error direction in ONE latent plane attains equality.
    assert (1-alpha) == (1-alpha)*1*1*1


def test_bad_basis_can_fail_when_the_original_problem_is_easy():
    rows = [[1, 20], [0, 1]]  # Unimodular, but a deliberately bad GS cell.
    target = [Fraction(1, 10), 0]
    point = nearest_plane(rows, target)
    assert point["point"] != [0, 0]
    reduced = [[1, 0], [0, 1]]
    assert nearest_plane(reduced, target)["point"] == [0, 0]
    assert dyadic_tail_bound(exact_profile(rows)["gs_squared"], 1)["failure_upper"] == 1


@pytest.mark.parametrize("rows", ([[1, 0], [2, 0]], [[1, 0, 0], [0, 1, 0]], []))
def test_invalid_basis_rejected(rows):
    with pytest.raises(ValueError):
        exact_profile(rows)


@pytest.mark.parametrize("seed", (290960, 290961))
def test_saved_source_certificate_is_not_asymptotic_or_independently_reviewed(seed):
    path = Path(__file__).resolve().parents[1]/f"research/certificates/native_rlwe_primal_babai_d64_seed{seed}.json"
    saved = json.loads(path.read_text())
    profile = exact_profile(saved["reduced_row_basis"])
    l = saved["log_dimension_upper"]
    cert = source_certificate(saved["d"], profile["gs_squared"],
                              Fraction(int(l["numerator_hex"], 16), int(l["denominator_hex"], 16)))
    for lane, key in (("spherical", "failure_upper"), ("elliptical", "total_failure_upper")):
        old = saved["certificate"][lane][key]
        assert Fraction(int(old["numerator_hex"], 16), int(old["denominator_hex"], 16)) == cert[lane][key]
        assert 0 < cert[lane][key] < Fraction(1, 10)
    assert not saved["asymptotic_attack_proved"]
    assert not saved["quantum_algorithm"]
    assert not saved["independent_review"]
    assert not saved["source_distribution_samples"]
    assert not saved["source_transfer_losses_paid"]
    assert [x["correct"] for x in saved["controls"]] == [True]*4+[False]*2
