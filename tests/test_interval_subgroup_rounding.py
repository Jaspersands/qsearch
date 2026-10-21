"""Sparse frame rank/inverse, exact denominator coins and native witnesses."""

from fractions import Fraction
import hashlib
from itertools import product
import json
import math
import random

from flint import fmpq_mat, fmpz, fmpz_mat
import pytest

import theorems.interval_subgroup_rounding as module
from theorems.interval_character_rounding import particular_for_syndrome
from theorems.interval_subgroup_rounding import (
    REPORT, coordinates, failure_certificate, frame, multiply, norm_one_generator, radius, run_controls, solve,
)


def moments(p, d, word):
    return [sum(pow(x, j, p) * v for x, v in enumerate(word)) % p for j in range(d)]


def rows(model):
    p, w = model["p"], model["waveform"]
    return [[1] * p] + [[w[(x - t) % p] for x in range(p)] for t in range(p - 1)]


@pytest.mark.parametrize("p,ell", [(5, 1), (7, 2), (7, 3), (13, 3), (31, 5), (31, 15)])
def test_native_moments_rank_column_range_and_exact_inverse_independently(p, ell):
    model = frame(p, ell)
    B = rows(model)
    assert sum(bool(x) for x in model["waveform"]) == 2 * ell
    assert set(model["waveform"]) <= {-1, 0, 1}
    det = abs(int(fmpz_mat(B).det()))
    assert det != 0 and det % (p ** ell) == 0
    for b in B:
        assert moments(p, ell, b) == [0] * ell
    first = moments(p, ell + 1, B[1])[-1]
    assert first == model["first_forbidden_moment"] != 0
    assert all(moments(p, ell + 1, b)[-1] == first for b in B[1:])
    assert max(sum(b[x] ** 2 for b in B) for x in range(p)) == 2 * ell + 1
    # Separate rational matrix inverse, not producer's polynomial xgcd.
    rng = random.Random(4547 + p + ell)
    y = [rng.randrange(p) for _ in range(p)]
    nums, D = coordinates(model, y)
    exact = fmpq_mat([y]) * fmpq_mat(B).inv()
    assert [Fraction(int(exact[0, i].numerator), int(exact[0, i].denominator)) for i in range(p)] == [Fraction(a, D) for a in nums]
    assert multiply(model, nums) == [D * a for a in y]


def test_exact_small_rounding_law_normalizes_and_has_zero_mean_on_every_column():
    p, ell, y = 7, 2, [1, 5, 2, 6, 0, 4, 1]
    model = frame(p, ell)
    nums, D = coordinates(model, y)
    options = []
    for a in nums:
        q, r = divmod(a, D)
        options.append([(q, Fraction(D - r, D))] + ([(q + 1, Fraction(r, D))] if r else []))
    mean, mass = [Fraction(0)] * p, Fraction(0)
    B = rows(model)
    for outcome in product(*options):
        probability = math.prod(t[1] for t in outcome)
        z = [t[0] for t in outcome]
        e = [y[x] - sum(a * b[x] for a, b in zip(z, B)) for x in range(p)]
        assert moments(p, ell, e) == moments(p, ell, y)
        mass += probability
        for x in range(p):
            mean[x] += probability * e[x]
    assert mass == 1 and mean == [0] * p


def test_actual_large_common_denominator_is_used_for_all_exact_coins(monkeypatch):
    bounds = []

    class Coin:
        def __init__(self, seed):
            pass

        def randrange(self, upper):
            bounds.append(upper)
            return 0

    monkeypatch.setattr(module.random, "Random", Coin)
    row = solve(61, 5, 5, 0, [15] + [0] * 60, attempts=2)
    D = int(fmpz(row["coordinate_common_denominator_decimal"]))
    assert D > 61 and set(bounds) == {D} and len(bounds) == 122
    assert row["solution"] is None and row["target_rerolls"] == 0
    assert len(row["attempts"]) == 2
    assert row["status"] == "ROUNDING_BUDGET_EXHAUSTED_NOT_HARDNESS"


def test_all_small_syndromes_preserve_original_model_including_d_below_ell():
    for p, d, ell in ((5, 1, 1), (7, 2, 3), (7, 3, 3)):
        for target in product(range(p), repeat=d):
            y = particular_for_syndrome(p, d, target)
            row = solve(p, d, ell, p // 2, y, attempts=1)
            assert moments(p, d, row["solution"]["centered_affine_witness"]) == list(target)
            assert row["failure_certificate"]["per_attempt_all_target_failure_upper_exact"] == "0"


def test_width_really_uses_sparse_column_parameter_not_dense_p():
    expected = [(31, 5, 6), (61, 5, 6), (127, 7, 8), (257, 16, 13), (1021, 17, 14)]
    for p, ell, u in expected:
        assert radius(p, ell) == u
        certificate = failure_certificate(p, ell, ell, u, attempts=2)
        assert certificate["column_squared_range_sum_upper"] == 2 * ell + 1
        delta = Fraction(certificate["per_attempt_all_target_failure_upper_exact"])
        assert delta <= Fraction(1, 2)
        assert Fraction(certificate["all_attempts_fail_upper_exact"]) == delta ** 2


def pair_multiply(a, b, p, nu):
    return ((a[0] * b[0] + nu * a[1] * b[1]) % p,
            (a[0] * b[1] + a[1] * b[0]) % p)


def pair_power(a, k, p, nu):
    answer = (1, 0)
    while k:
        if k % 2:
            answer = pair_multiply(answer, a, p, nu)
        a = pair_multiply(a, a, p, nu)
        k //= 2
    return answer


@pytest.mark.parametrize("p,ell", [(11, 3), (17, 3), (47, 6), (47, 12), (47, 16), (107, 9)])
def test_independent_pair_field_generator_trace_fibers_moments_and_inverse(p, ell):
    model = frame(p, ell, "nonsplit")
    nu = model["quadratic_nonresidue"]
    g = tuple(model["primitive_generator"])
    assert nu not in {a * a % p for a in range(p)}
    assert (g[0] * g[0] - nu * g[1] * g[1]) % p == 1
    group, z = set(), (1, 0)
    for _ in range(p + 1):
        group.add(z)
        z = pair_multiply(z, g, p, nu)
    assert len(group) == p + 1 and z == (1, 0)
    step = pair_power(g, (p + 1) // ell, p, nu)
    H = [pair_power(step, i, p, nu) for i in range(ell)]
    assert len(set(H)) == ell
    counts = []
    for a in model["trace_coset_exponents"]:
        ga = pair_power(g, a, p, nu)
        trace = [2 * pair_multiply(ga, z, p, nu)[0] % p for z in H]
        counts.append([trace.count(x) for x in range(p)])
    assert tuple(a - b for a, b in zip(*counts)) == model["waveform"]
    B = rows(model)
    assert all(moments(p, ell, b) == [0] * ell for b in B)
    assert moments(p, ell + 1, B[1])[-1] == model["first_forbidden_moment"] != 0
    squared_norm = sum(x * x for x in model["waveform"])
    assert squared_norm == model["squared_waveform_norm"]
    assert max(sum(b[x] ** 2 for b in B) for x in range(p)) == squared_norm + 1
    if model["torus_quotient_index"] >= 5:
        assert max(map(abs, model["waveform"])) == 1 and squared_norm == 2 * ell
        assert max(counts[0]) == max(counts[1]) == 1
    else:
        assert max(map(abs, model["waveform"])) == 2
        assert squared_norm == 3 * ell - math.gcd(ell, 2) > 2 * ell
    y = [int(i * i + 5 * i + 7) % p for i in range(p)]
    # A nonpolynomial spike avoids relying on an integral kernel coordinate.
    y[0] = (y[0] + 1) % p
    nums, D = coordinates(model, y)
    alpha = fmpq_mat([y]) * fmpq_mat(B).inv()
    assert [Fraction(int(alpha[0, i].numerator), int(alpha[0, i].denominator)) for i in range(p)] == [Fraction(a, D) for a in nums]
    assert abs(int(fmpz_mat(B).det())) % p ** ell == 0


def test_inverse_trace_classes_can_annihilate_a_naive_waveform_completely():
    # At quotient index3, g^2 H=(gH)^-1, hence their trace multisets coincide.
    p, ell = 47, 16
    _, g, _, _ = norm_one_generator(p)
    step = g ** ((p + 1) // ell)
    one = sorted(int((g * step ** i).trace()) for i in range(ell))
    two = sorted(int((g * g * step ** i).trace()) for i in range(ell))
    assert one == two
    model = frame(p, ell, "nonsplit")
    assert model["trace_coset_exponents"] == [0, 1]
    assert model["squared_waveform_norm"] == 46  # NOT the incorrect unit-fiber32.
    assert failure_certificate(p, ell, ell, 12, torus="nonsplit")["column_squared_range_sum_upper"] == 47


def test_nonsplit_model_keeps_prime_input_and_correct_divisor_scope():
    for p, ell, u, split_u in ((47, 6, 7, 13), (107, 9, 9, 21), (509, 15, 13, 37), (1019, 17, 14, 78)):
        assert radius(p, ell, torus="nonsplit") == u < split_u
        cert = failure_certificate(p, ell, ell, u, torus="nonsplit")
        assert cert["column_squared_range_sum_upper"] == 2 * ell + 1
        assert Fraction(cert["per_attempt_all_target_failure_upper_exact"]) <= Fraction(1, 2)
    with pytest.raises(ValueError):
        frame(47, 6, "split")
    with pytest.raises(ValueError):
        frame(61, 5, "nonsplit")
    with pytest.raises(ValueError):
        frame(47, 6, "unknown")
    with pytest.raises(ValueError):
        solve(47, 7, 6, 7, [0] * 47, torus="nonsplit")
    with pytest.raises(ValueError):
        frame(47 * 47, 6, "nonsplit")


def test_all_small_nonsplit_syndromes_and_impossible_targets_are_retained():
    p, ell, d = 7, 2, 2
    for target in product(range(p), repeat=d):
        y = particular_for_syndrome(p, d, target)
        r = solve(p, d, ell, p // 2, y, torus="nonsplit", attempts=1)
        assert len(r["solution"]["centered_affine_witness"]) == p
        assert moments(p, d, r["solution"]["centered_affine_witness"]) == list(target)
    r = solve(p, d, ell, 0, particular_for_syndrome(p, d, [1, 0]), torus="nonsplit", attempts=3)
    assert r["solution"] is None and len(r["attempts"]) == 3 and r["target_rerolls"] == 0


@pytest.mark.parametrize("p,d,ell,u", [(9, 1, 2, 1), (31, 6, 5, 4), (31, 5, 7, 4), (31, 5, 30, 4), (31, 5, True, 4), (31, 5, 5, 16)])
def test_no_nonprime_missing_divisor_extra_moment_or_unbounded_interval_scope(p, d, ell, u):
    with pytest.raises(ValueError):
        solve(p, d, ell, u, [0] * p)


def test_saved_native_witnesses_and_source_provenance_replay():
    report = json.loads(REPORT.read_text())
    assert report == run_controls()
    assert report["source_sha256"] == hashlib.sha256(module.Path(module.__file__).read_bytes()).hexdigest()
    assert len(report["controls"]) == 10 and report["all_declared_targets_verified"]
    assert len(report["nonsplit_controls"]) == 8
    for r in report["controls"] + report["nonsplit_controls"]:
        p, d, ell, y = r["p"], r["d"], r["ell"], r["public_particular_word"]
        e, poly = r["solution"]["centered_affine_witness"], r["solution"]["polynomial_coefficients"]
        assert len(e) == p and len(poly) == p - ell
        assert max(map(abs, e)) <= r["u"]
        assert r["u"] < r.get("dense_character_certified_radius", r.get("best_split_certified_radius"))
        assert moments(p, d, e) == moments(p, d, y) == r["target_syndrome"]
        for x in range(p):
            value = 0
            for a in reversed(poly):
                value = (value * x + a) % p
            assert (y[x] - e[x] - value) % p == 0
        assert r["coordinate_denominator_bits"] == int(fmpz(r["coordinate_common_denominator_decimal"])).bit_length()
        assert r["quantum_uniform_interval_sufficient_condition_met"]
        assert Fraction(r["failure_certificate"]["per_attempt_all_target_failure_upper_exact"]) <= Fraction(1, 2)
    assert not report["novelty_quantum_speedup_or_weighted_sampling_claimed"]
    assert not report["arbitrary_sets_punctured_inputs_or_all_prime_smoothness_claimed"]
    assert len(report["nearest_controls"]) == 2
    for r in report["nearest_controls"]:
        assert r["rounding_mode"] == "nearest" and r["rounding_seed_for_replay_only"] is None
        assert r["nearest_rounding_certificate"]["requested_interval_uniformly_solved"]
        assert r["nearest_rounding_certificate"]["all_target_centered_integer_radius"] == r["ell"]
        assert r["failure_certificate"]["comparison_only_not_active_rounding_model"]
        assert moments(r["p"], r["d"], r["solution"]["centered_affine_witness"]) == r["target_syndrome"]
        assert max(map(abs, r["solution"]["centered_affine_witness"])) <= r["u"]
