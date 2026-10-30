from fractions import Fraction
from itertools import product
import random

import pytest

from norm_completion import NormCompletion, affine_solution, rank
from scope_bounds import all_input_bounds, bounds, fixed_prime_cutoff


def rs_fixture():
    p, m = 11, 11
    B = [[pow(x, degree, p) for x in range(m)] for degree in range(4)]
    A = [[pow(x, degree, p) for x in range(m)] for degree in range(3)]
    return NormCompletion(p, B, A, [1]*m, 2)


@pytest.mark.parametrize("p,nu", [(3, 2), (5, 2), (7, 3), (11, 2)])
def test_norm_zero_is_exactly_pair_zero(p, nu):
    for u, v in product(range(p), repeat=2):
        assert ((u*u-nu*v*v) % p == 0) == (u == v == 0)


def test_affine_solution_and_kernel():
    M, s, p = [[1, 2, 3], [0, 1, 1]], [4, 2], 5
    point, kernel = affine_solution(M, s, p)
    assert all(sum(x*y for x, y in zip(row, point)) % p == t for row, t in zip(M, s))
    for row in M:
        assert sum(row[i]*kernel[i][0] for i in range(3)) % p == 0
    with pytest.raises(ValueError, match="inconsistent"):
        affine_solution([[1], [1]], [0, 1], 5)


def test_annihilator_and_square_guards():
    case = rs_fixture()
    h = [1]*case.m
    h[0] = 2
    with pytest.raises(ValueError, match="annihilator"):
        NormCompletion(case.p, case.B, case.A, h, 2)
    with pytest.raises(ValueError, match="nonsquare"):
        NormCompletion(case.p, case.B, case.A, [1]*case.m, 1)
    with pytest.raises(ValueError, match="nonzero annihilator"):
        NormCompletion(case.p, case.B, case.A, [0]*case.m, 2)
    with pytest.raises(ValueError, match="odd prime"):
        NormCompletion(2, [[1, 1]], [[1, 1]], [1, 1], 1)


def test_rank_failure_is_not_infeasibility():
    case = rs_fixture()
    result = case.prepare([1]*case.k, [0]*case.m, [0]*case.m)
    assert result["status"] == "UNKNOWN_SYNDROME_RANK"
    # B has a full-support word even though these particular offsets fail.
    word = [1]*case.m
    syndrome = [sum(row) % case.p for row in case.B]
    assert case.verifies(word, syndrome)


def test_review_counterexample_rank_and_field_size_are_insufficient():
    case = NormCompletion(5, [[1, 4, 0], [0, 1, 4]], [[1, 1, 1]], [1, 1, 1], 2)
    prepared = case.prepare([4, 3], [0, 1, 0], [0, 0, 1])
    assert prepared["matrix"] == [[3, 0], [2, 4]]
    assert rank(prepared["matrix"], 5) == 2
    assert 5**2 >= 2*case.m
    assert prepared["point"] == [0, 0]
    assert case.evaluate(prepared["point"], prepared["a"], prepared["b"]) == [0, 1, 3]
    assert prepared["zero_union_bound"] == 1
    assert case.verifies([1, 2, 4], [4, 3])


def test_zero_annihilator_coordinates_are_paid_in_original_syndrome():
    original = rs_fixture()
    B = [row+[1 if j == 0 else 0] for j, row in enumerate(original.B)]
    A = [row+[1 if j == 0 else 0] for j, row in enumerate(original.A)]
    h = iter([1]*11+[0])
    case = NormCompletion(11, B, A, h, 2)
    syndrome = [1, 2, 3, 4]
    result = case.solve(syndrome, seed=27103)
    assert result["status"] == "VERIFIED_NATIVE_WITNESS"
    assert result["word"][-1] == 1
    assert case.verifies(result["word"], syndrome)


def test_linearization_for_arbitrary_coefficients():
    case = rs_fixture()
    rng = random.Random(27101)
    a, b = ([rng.randrange(case.p) for _ in range(case.m)] for _ in range(2))
    prepared = case.prepare([3, 1, 4, 1], a, b)
    assert prepared["status"] == "CERTIFIED_AFFINE_FIBER"
    origin = case.evaluate([0]*(2*case.r), a, b)
    for _ in range(60):
        t = [rng.randrange(case.p) for _ in range(2*case.r)]
        word = case.evaluate(t, a, b)
        for row, linear in zip(case.B, prepared["matrix"]):
            lhs = sum(x*(y-z) for x, y, z in zip(row, word, origin)) % case.p
            assert lhs == sum(x*y for x, y in zip(linear, t)) % case.p


def test_exhaustive_fiber_matches_every_marginal():
    case = rs_fixture()
    rng = random.Random(27102)
    a, b = ([rng.randrange(case.p) for _ in range(case.m)] for _ in range(2))
    syndrome = [1, 2, 3, 4]
    prepared = case.prepare(syndrome, a, b)
    assert prepared["dimension"] == 2
    counts, successes = [0]*case.m, 0
    for free in product(range(case.p), repeat=prepared["dimension"]):
        t = [(x+sum(a*b for a, b in zip(row, free))) % case.p
             for x, row in zip(prepared["point"], prepared["kernel"])]
        word = case.evaluate(t, a, b)
        assert all(sum(x*y for x, y in zip(row, word)) % case.p == s
                   for row, s in zip(case.B, syndrome))
        for i, value in enumerate(word):
            counts[i] += value == 0
        successes += all(word)
    size = case.p**prepared["dimension"]
    for event in prepared["events"]:
        assert Fraction(counts[event["coordinate"]], size) == event["probability"]
    assert Fraction(successes, size) >= 1-prepared["zero_union_bound"]
    assert case.r < case.k  # The same A cannot support a surjective one-block map.


def test_zero_dimensional_kernel_and_unreachable_zero_events():
    case = NormCompletion(5, [[1, 0, 4, 0], [0, 1, 0, 4]], [[1, 1, 1, 1]], [1]*4, 2)
    statuses = set()
    for syndrome in product(range(5), repeat=2):
        prepared = case.prepare(syndrome, [1, 0, 0, 0], [0, 1, 0, 0])
        assert prepared["dimension"] == 0
        word = case.evaluate(prepared["point"], prepared["a"], prepared["b"])
        for event in prepared["events"]:
            assert event["rank"] == 0
            assert event["probability"] == int(word[event["coordinate"]] == 0)
            statuses.add(event["zero_attainable"])
    assert statuses == {False, True}


@pytest.mark.parametrize("syndrome", [[0, 0, 0, 0], [1, 2, 3, 4], [10, 10, 10, 10]])
def test_solver_verifies_original_input(syndrome):
    case = rs_fixture()
    result = case.solve(syndrome, seed=27103)
    assert result["status"] == "VERIFIED_NATIVE_WITNESS"
    assert case.verifies(result["word"], syndrome)
    assert result["uniform_native_sampling"] is False
    assert result["history"][-1]["zero_union_bound"] <= Fraction(1, 2)


def test_invalid_inputs_and_caps():
    case = rs_fixture()
    with pytest.raises(ValueError):
        case.solve([0]*case.k, seed=0, kernel_attempts=0)
    with pytest.raises(ValueError):
        case.prepare([case.p]*case.k, [0]*case.m, [0]*case.m)
    with pytest.raises(ValueError):
        NormCompletion(case.p, case.B, case.A+[case.A[0]], [1]*case.m, 2)
    assert rank([[], []], 5) == 0


def test_offset_bound_against_exhaustive_linear_images():
    # k=1,r=2,m=4 with RS A: each of the two random offset maps is onto F_5^2.
    # Thus M is exactly uniform in F_5^4; exhaust that law, not selected offsets.
    p, points, bad = 5, range(4), 0
    for coefficients in product(range(p), repeat=4):
        M = [list(coefficients)]
        if rank(M, p) == 0:
            bad += 1
            continue
        _, kernel = affine_solution(M, [0], p)
        for x in points:
            image = [[(kernel[start][j]+x*kernel[start+1][j]) % p
                      for j in range(3)] for start in (0, 2)]
            if rank(image, p) < 2:
                bad += 1
                break
    assert bad == 97
    assert Fraction(bad, p**4) <= 4*(p-1)*Fraction(p)**(2-4)


@pytest.mark.parametrize("e", [8, 16, 32, 64, 128, 256])
def test_geometric_sufficient_bounds(e):
    report = bounds(1019, e)
    assert report["basepoint_failure_upper_raw_prime_source"] < Fraction(1, 10**8)
    assert report["annihilator_zero_budget_failure_upper"] < Fraction(1, 100)
    assert report["offset_failure_upper"] < Fraction(1, 1000000)
    assert report["pair_stage_constant_success_certified"]
    assert report["source_prime_count_condition_numeric"]
    assert report["public_geometry_required"]
    assert not report["full_cube_conditioning_applied"]


def test_cutoff_does_not_claim_all_fixed_prime_degrees():
    report = fixed_prime_cutoff(1019)
    assert report["integer_e_cutoff"] == 23599
    assert report["dyadic_e_cutoff"] == 16384
    assert 44*16384 <= 1019**2 < 44*32768
    assert Fraction(22*32768, 1019**2) > Fraction(1, 2)
    assert report["beyond_cutoff_status"] == "NO_FIXED_PRIME_ASYMPTOTIC_CERTIFICATE"


def test_exact_bound_diagnostic_cap_not_silent_forecast():
    with pytest.raises(ValueError, match="diagnostic"):
        bounds(1019, 16384)
    with pytest.raises(ValueError, match="prime"):
        fixed_prime_cutoff(1020)


def test_large_exact_bounds_have_lossless_json_encoding():
    from scope_bounds import encode_fraction
    import json
    value = bounds(1019, 256)["basepoint_failure_upper_raw_prime_source"]
    encoded = json.loads(json.dumps(encode_fraction(value)))
    recovered = Fraction(int(encoded["numerator_hex"], 16), int(encoded["denominator_hex"], 16))
    assert recovered == value


@pytest.mark.parametrize("e", [64, 65, 67, 68, 128, 256, 16384, 23599])
def test_all_input_bounds_with_rank_loss(e):
    result = all_input_bounds(1019, e)
    assert result["h_failure_upper"] < Fraction(88, 1019)
    assert result["offset_failure_upper"] < Fraction(1, 2)
    assert result["kernel_zero_union_upper"] <= Fraction(1, 2)
    assert result["pair_stage_constant_success_certified"]
    assert not result["uniform_divisor_source_required"]
    assert not result["matrix_adapter_implemented"]


def test_old_greedy_closes_the_small_degree_boundary():
    for e in range(8, 64):
        assert all_input_bounds(1019, e)["field_condition"]
    assert not all_input_bounds(1019, 32768)["pair_stage_constant_success_certified"]


def test_review_integer_bound_is_not_two_step_monotone():
    first = all_input_bounds(1019, 67)["offset_failure_upper"]
    later = all_input_bounds(1019, 69)["offset_failure_upper"]
    assert first < later < Fraction(1, 2)
    for e in range(64, 80):
        integer = all_input_bounds(1019, e)["offset_failure_upper"]
        envelope_squared = Fraction((22*e-1)**2, 1019**(e-54))
        next_squared = Fraction((22*e+21)**2, 1019**(e-53))
        assert integer*integer <= envelope_squared < Fraction(1, 4)
        assert next_squared < envelope_squared
