"""Independent algebra, exact coins, sharp scope and original-equation witnesses."""

from fractions import Fraction
import hashlib
from itertools import product
import json
import math
import random

from flint import fmpz_mat
import pytest

import theorems.interval_character_rounding as module
from theorems.interval_character_rounding import (
    MATCHED_REPORT, REPORT, bounded_basis_audit, certified_radius, character,
    coefficient_numerators, deterministic_certificate, deterministic_radius,
    failure_certificate, multiply_basis, native_moments, particular_for_syndrome,
    round_numerator, run_controls, solve, solve_deterministic,
)


def independent_rows(p):
    squares = {x * x % p for x in range(1, p)}
    chi = [0 if x == 0 else (1 if x in squares else -1) for x in range(p)]
    return [[1] * p] + [[chi[(x - t) % p] for x in range(p)] for t in range(p - 1)]


def moments(p, d, word):
    return [sum(pow(x, j, p) * a for x, a in enumerate(word)) % p for j in range(d)]


def horner(coefficients, x, p):
    result = 0
    for a in reversed(coefficients):
        result = (result * x + a) % p
    return result


@pytest.mark.parametrize("p", [3, 5, 7, 11, 13, 31])
def test_independent_character_Gram_determinant_kernel_and_sharp_boundary(p):
    rows, h = independent_rows(p), (p - 1) // 2
    assert character(p) == tuple(rows[1])
    B = fmpz_mat(rows)
    assert abs(int(B.det())) == p ** h
    for i, row in enumerate(rows):
        assert moments(p, h, row) == [0] * h
        if i:
            assert moments(p, h + 1, row)[-1] == p - 1
        for j, other in enumerate(rows):
            expected = p if i == j == 0 else (0 if not i or not j else (p - 1 if i == j else -1))
            assert sum(a * b for a, b in zip(row, other)) == expected
    assert bounded_basis_audit(p)["first_forbidden_moment_of_every_character_row"] == p - 1


def test_exact_coordinates_are_inverse_rows_not_hidden_nearest_point_advice():
    for p in (3, 5, 7, 13):
        B = fmpz_mat(independent_rows(p))
        rng = random.Random(4493 + p)
        for word in ([0] * p, list(range(p)), [p - 1] + [0] * (p - 1), [rng.randrange(p) for _ in range(p)]):
            numerators = coefficient_numerators(p, word)
            assert list((fmpz_mat([numerators]) * B).tolist()[0]) == [p * a for a in word]
            assert multiply_basis(p, numerators) == [p * a for a in word]
            # Independent Gaussian inverse rather than the producer's Gram formula.
            inverse = B.inv()
            expected = fmpz_mat([[p * a for a in word]]) * inverse
            assert [int(expected[0, i]) for i in range(p)] == numerators


class FixedCoin:
    def __init__(self, value):
        self.value = value

    def randrange(self, p):
        assert 0 <= self.value < p
        return self.value


def test_exact_unbiased_coins_include_negative_numerators_and_ties():
    for p in (3, 5, 7):
        for a in range(-3 * p, 3 * p + 1):
            outputs = [round_numerator(a, p, FixedCoin(k)) for k in range(p)]
            assert sum(outputs) == a
            q, r = divmod(a, p)
            assert outputs.count(q + 1) == r
            assert all(z in (q, q + 1) for z in outputs)
    with pytest.raises(ValueError):
        round_numerator(.5, 5, FixedCoin(0))


def test_exhaustive_independent_rounding_distribution_is_normalized_and_centered():
    for p, word in ((3, [1, 0, 0]), (5, [4, 1, 0, 3, 2]), (7, [1, 5, 2, 6, 0, 4, 1])):
        rows, d = independent_rows(p), (p - 1) // 2
        numerators = coefficient_numerators(p, word)
        choices = []
        for a in numerators:
            q, r = divmod(a, p)
            choices.append([(q, Fraction(p - r, p))] + ([(q + 1, Fraction(r, p))] if r else []))
        mass, means = Fraction(0), [Fraction(0)] * p
        failed = [Fraction(0)] * (p // 2 + 1)
        for outcome in product(*choices):
            z = [o[0] for o in outcome]
            prob = math.prod(o[1] for o in outcome)
            raw = [word[x] - sum(a * row[x] for a, row in zip(z, rows)) for x in range(p)]
            centered = [(a + p // 2) % p - p // 2 for a in raw]
            assert moments(p, d, raw) == moments(p, d, word)
            mass += prob
            for x, a in enumerate(raw):
                means[x] += prob * a
            for u in range(p // 2 + 1):
                if max(map(abs, centered)) > u:
                    failed[u] += prob
        assert mass == 1 and means == [0] * p
        for u, failure in enumerate(failed):
            assert failure <= Fraction(failure_certificate(p, d, u)["per_attempt_failure_upper_exact"])
        assert failed[-1] == 0


def test_every_small_native_syndrome_is_solved_without_planting_or_reroll():
    for p in (3, 5, 7):
        d = (p - 1) // 2
        for target in product(range(p), repeat=d):
            word = particular_for_syndrome(p, d, target)
            assert moments(p, d, word) == list(target)
            row = solve(p, d, p // 2, word, attempts=1)
            e = row["solution"]["centered_affine_witness"]
            assert moments(p, d, e) == list(target)
            poly = row["solution"]["polynomial_coefficients"]
            assert all((word[x] - e[x] - horner(poly, x, p)) % p == 0 for x in range(p))
            assert row["failure_certificate"]["per_attempt_failure_upper_exact"] == "0"


def test_integer_tail_threshold_and_exact_dyadic_repetition_bound():
    row = failure_certificate(61, 30, 15, attempts=2)
    assert row["integer_tail_threshold"] == 16
    assert row["dyadic_exponent_floor"] == 8
    assert Fraction(row["per_attempt_failure_upper_exact"]) == Fraction(61, 128)
    assert Fraction(row["all_attempts_fail_upper_exact"]) == Fraction(61, 128) ** 2
    assert Fraction(row["expected_attempts_upper_exact"]) == Fraction(128, 67)
    assert Fraction(failure_certificate(127, 63, 31)["per_attempt_failure_upper_exact"]) == Fraction(127, 32768)
    for p in (3, 5, 31, 61, 127, 257, 509, 1021, 4093):
        u = certified_radius(p)
        assert Fraction(failure_certificate(p, p // 2, u)["per_attempt_failure_upper_exact"]) <= Fraction(1, 2)
        if u < p // 2:
            assert 2 * (u + 1) ** 2 >= p * (4 * p - 1).bit_length()
    # Tiny positive tails are rounded UP, never silently replaced by probability0.
    row = failure_certificate(4093, 2046, 2045, attempts=64)
    assert 0 < Fraction(row["per_attempt_failure_upper_exact"]) <= Fraction(1, 2) ** 128
    assert 0 < Fraction(row["all_attempts_fail_upper_exact"]) <= Fraction(1, 2) ** 128


@pytest.mark.parametrize("p,d,u", [(9, 2, 1), (2, 1, 1), (True, 1, 1), (7, 4, 2), (7, 0, 1), (7, 3, 4), (7, 3, -1)])
def test_no_extension_composite_punctured_or_beyond_half_rate_scope(p, d, u):
    with pytest.raises(ValueError):
        solve(p, d, u, [0] * int(p))


def test_failure_is_retained_and_not_interpreted_as_hardness():
    word = particular_for_syndrome(7, 3, [1, 0, 0])
    row = solve(7, 3, 0, word, attempts=3)
    assert row["solution"] is None
    assert row["status"] == "ROUNDING_BUDGET_EXHAUSTED_NOT_HARDNESS"
    assert len(row["attempts"]) == 3 and row["target_rerolls"] == 0
    assert not row["failure_certificate"]["uniform_all_target_success_bound_nontrivial"]
    rows = independent_rows(7)
    for attempt in row["attempts"]:
        z = attempt["rounded_coefficients"]
        e = [(word[x] - sum(a * b[x] for a, b in zip(z, rows)) + 3) % 7 - 3 for x in range(7)]
        assert moments(7, 3, e) == [1, 0, 0]
        assert max(map(abs, e)) == attempt["centered_infinity_norm"] > 0


def test_search_witness_is_not_an_ideal_uniform_or_weighted_sampler():
    # Zero particular word has integral coordinates, hence rounding always
    # returns0. The full-interval zero coset has p**(p-d) possible words.
    row = solve(7, 3, 3, [0] * 7)
    assert row["solution"]["centered_affine_witness"] == [0] * 7
    assert 7 ** (7 - 3) > 1


def test_malformed_words_and_targets_rejected_before_rounding():
    for word in ([1, 2], [0] * 6 + [7], [0] * 6 + [False]):
        with pytest.raises(ValueError):
            coefficient_numerators(7, word)
    for target in ([0], [0, 0, 7], [0, False, 0]):
        with pytest.raises(ValueError):
            particular_for_syndrome(7, 3, target)


def test_exact_conditional_expectations_match_independent_exhaustive_distributions():
    for p, word in ((3, [1, 0, 0]), (5, [4, 0, 3, 1, 2]), (7, [1, 5, 2, 6, 0, 4, 1])):
        u = 1
        row = solve_deterministic(p, p // 2, u, word)
        c = Fraction(row["certificate"]["rational_potential_base"])
        B, numerators = independent_rows(p), coefficient_numerators(p, word)
        q, r = [a // p for a in numerators], [a % p for a in numerators]

        def conditional_potential(prefix):
            total = Fraction(0)
            choices = [[(bit, Fraction(1))] for bit in prefix]
            for ri in r[len(prefix):]:
                choices.append([(0, Fraction(p - ri, p))] + ([(1, Fraction(ri, p))] if ri else []))
            for outcome in product(*choices):
                z = [a + b[0] for a, b in zip(q, outcome)]
                prob = math.prod(b[1] for b in outcome)
                raw = [word[x] - sum(a * b[x] for a, b in zip(z, B)) for x in range(p)]
                total += prob * sum(c ** a + c ** -a for a in raw)
            return total

        prefix = []
        previous = initial = conditional_potential(prefix)
        for i, bit in enumerate(row["chosen_ceil_bits"]):
            zero = conditional_potential(prefix + [0])
            one = conditional_potential(prefix + [1]) if r[i] else zero
            assert previous == Fraction(p - r[i], p) * zero + Fraction(r[i], p) * one
            assert bit == int(r[i] != 0 and one < zero)
            prefix.append(bit)
            previous = one if bit else zero
        assert row["initial_exact_potential_certifies_this_target"] == (initial < c ** (u + 1))
        assert Fraction(row["initial_potential_ratio_upper_exact"]) >= initial / c ** (u + 1)
        assert Fraction(row["final_potential_ratio_upper_exact"]) >= previous / c ** (u + 1)
        assert previous <= initial
        assert not row["random_coins_or_seed_used"] and row["target_rerolls"] == 0


def test_rational_log_enclosures_and_uniform_deterministic_width_certificates():
    for p in (3, 5, 7, 11, 17, 19, 23, 31, 61, 127, 257, 509, 1021, 4093):
        u = deterministic_radius(p)
        row = deterministic_certificate(p, p // 2, u)
        lo, hi = Fraction(row["log_base_lower_exact"]), Fraction(row["log_base_upper_exact"])
        assert float(lo) <= math.log(float(Fraction(row["rational_potential_base"]))) + 1e-15
        assert float(hi) >= math.log(float(Fraction(row["rational_potential_base"]))) - 1e-15
        assert lo <= hi and hi - lo < Fraction(1, 1000)
        margin = (u + 1) * lo - Fraction(p, 8) * hi * hi
        assert Fraction(row["Hoeffding_exponent_margin_lower_exact"]) == margin
        assert row["uniform_all_target_potential_certificate"] or row["full_interval_trivially_solved"]
    # Rounded-base Chernoff potential is not identical to the optimized random tail.
    assert certified_radius(23) == 8 and deterministic_radius(23) == 9
    assert not deterministic_certificate(23, 11, 8)["uniform_all_target_potential_certificate"]


def test_naive_nearest_coordinates_have_linear_error_but_conditional_rounding_does_not():
    p = 127
    word, u = [p // 4] + [0] * (p - 1), deterministic_radius(p)
    numerators = coefficient_numerators(p, word)
    nearest = [(2 * a + p) // (2 * p) for a in numerators]
    assert nearest == [0] * p
    assert max(word) == p // 4 > u
    row = solve_deterministic(p, p // 2, u, word)
    assert row["solution"] is not None and row["centered_infinity_norm"] <= u
    assert row["initial_exact_potential_certifies_this_target"]


def test_deterministic_potential_does_not_promote_impossible_target():
    y = particular_for_syndrome(7, 3, [1, 0, 0])
    row = solve_deterministic(7, 3, 0, y)
    assert row["solution"] is None
    assert row["status"] == "POTENTIAL_BOUND_INCONCLUSIVE_NO_WITNESS"
    assert not row["initial_exact_potential_certifies_this_target"]
    assert not row["certificate"]["uniform_all_target_potential_certificate"]


def test_saved_report_replays_and_independent_Horner_moments_check_every_witness():
    saved = json.loads(REPORT.read_text())
    assert saved == run_controls()
    assert saved["source_sha256"] == hashlib.sha256(module.Path(module.__file__).read_bytes()).hexdigest()
    assert saved["matched_input_report_sha256"] == hashlib.sha256(MATCHED_REPORT.read_bytes()).hexdigest()
    prior = json.loads(MATCHED_REPORT.read_text())
    pairs = [(f["profile"]["p"], f["decoder_dimension"], t["particular_word"], t["uniform_target_syndrome"])
             for f in prior["uniform_target_lattice_controls"] for t in f["trials"]]
    matched = [r for r in saved["controls"] if r["input_source"].startswith("EXACT_SAVED")]
    assert [(r["p"], r["d"], r["public_particular_word"], r["original_target_syndrome"]) for r in matched] == pairs
    assert len(saved["controls"]) == 33 and saved["all_saved_targets_have_verified_witnesses"]
    for r in saved["controls"]:
        p, d, u, y = r["p"], r["d"], r["u"], r["public_particular_word"]
        e, poly = r["solution"]["centered_affine_witness"], r["solution"]["polynomial_coefficients"]
        assert len(e) == p and len(poly) == (p + 1) // 2
        assert max(map(abs, e)) <= u
        assert moments(p, d, e) == moments(p, d, y) == r["original_target_syndrome"]
        assert all((y[x] - e[x] - horner(poly, x, p)) % p == 0 for x in range(p))
        assert r["basis_search_or_LLL_calls"] == r["target_rerolls"] == 0
        if p > 127:
            assert d == p // 2
            assert Fraction(r["failure_certificate"]["per_attempt_failure_upper_exact"]) <= Fraction(1, 2)
    assert not saved["novelty_or_quantum_speedup_claimed"]
    assert not saved["arbitrary_sets_or_weighted_sampling_dequantized"]
    assert not saved["punctured_exponential_field_input_dequantized"]
    assert len(saved["deterministic_controls"]) == 8
    for r in saved["deterministic_controls"]:
        p, d, y = r["p"], r["d"], r["public_particular_word"]
        assert r["certificate"]["uniform_all_target_potential_certificate"]
        assert Fraction(r["initial_potential_ratio_upper_exact"]) < 1
        assert Fraction(r["final_potential_ratio_upper_exact"]) < 1
        e = r["solution"]["centered_affine_witness"]
        poly = r["solution"]["polynomial_coefficients"]
        assert moments(p, d, e) == moments(p, d, y) == r["original_target_syndrome"]
        assert max(map(abs, e)) <= r["u"]
        assert all((y[x] - e[x] - horner(poly, x, p)) % p == 0 for x in range(p))
