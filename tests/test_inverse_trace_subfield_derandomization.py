"""Tests for deterministic subfield derandomization of inverse-trace problems."""
import os
from pathlib import Path
import subprocess

import pytest

from theorems import inverse_trace_subfield_derandomization as subfield
from theorems.inverse_trace_subfield_derandomization import (
    full_degree_zero_directions,
    greedy_vs_matroid_exchange_control,
    solve_subfield_derandomized,
    subfield_kernel_basis,
)


def _reference_mul(a, b, n, modulus):
    value = 0
    for _ in range(n):
        if b & 1:
            value ^= a
        b >>= 1
        a <<= 1
        if a & (1 << n):
            a ^= modulus
    return value


def _reference_power(a, exponent, n, modulus):
    value = 1
    while exponent:
        if exponent & 1:
            value = _reference_mul(value, a, n, modulus)
        a = _reference_mul(a, a, n, modulus)
        exponent >>= 1
    return value


def _assert_original_equations(n, modulus, points, targets, syndrome, result):
    """Check the actual witness with arithmetic independent of the solver."""
    witness = result["witness"]
    assert len(witness) == len(points)
    assert all(type(x) is int and 0 <= x < (1 << n) for x in witness)
    actual_syndrome = [0] * len(syndrome)
    for point, target, value in zip(points, targets, witness):
        power = 1
        for j in range(len(syndrome)):
            actual_syndrome[j] ^= _reference_mul(power, value, n, modulus)
            power = _reference_mul(power, point, n, modulus)
        cur = _reference_power(value, (1 << n) - 2, n, modulus) if value else 0
        actual_trace = 0
        for _ in range(n):
            actual_trace ^= cur
            cur = _reference_mul(cur, cur, n, modulus)
        assert actual_trace == target
    assert actual_syndrome == syndrome


def test_einstein_exact_n8_e4_m2_control():
    """Reproduce Einstein's exact control on F_256 / F_4."""
    n, e, m, modulus = 8, 4, 2, 0x11b
    theta = 2
    beta = 6

    dir_info = full_degree_zero_directions(n, e, modulus, theta=theta, beta=beta)
    assert dir_info["k_basis"] == [1, 188]
    assert dir_info["directions"] == [176, 41, 200, 98]
    assert dir_info["expanded_binary_rank"] == 8
    assert dir_info["kernel_dimension"] == 4
    assert dir_info["verified"] is True

    N, K = 64, 8
    points = list(range(1, N + 1))
    targets = [i % 2 for i in range(N)]  # 32 zero targets, exactly e * K
    syndrome = [1, 2, 3, 4, 5, 6, 7, 8]

    res = solve_subfield_derandomized(
        n, e, modulus, points, targets, syndrome=syndrome, theta=theta, beta=beta
    )

    assert res["restricted_binary_rank"] == 64
    assert res["verified"] is True
    assert res["verified_parity"] is True
    assert res["verified_trace"] is True
    assert res["uniform_sampler"] is False
    assert res["hardness_evidence"] is False
    assert res["selected_zero_indices"] == [i for i, b in enumerate(targets) if b == 0]
    assert len(res["selected_direction_slots"]) == 32
    assert len(res["witness"]) == N
    _assert_original_equations(n, modulus, points, targets, syndrome, res)


def test_explicit_full_degree_directions_and_solve_across_degrees():
    """Verify directions and arbitrary-syndrome solves across multiple degrees."""
    cases = [
        (6, 3, 67, 12, 2, [3, 5]),
        (8, 4, 0x11b, 16, 2, [7, 11]),
        (12, 4, 0x1053, 16, 2, [13, 17]),
        (15, 5, 0x8003, 20, 2, [19, 23]),
        (18, 6, 0x40081, 24, 2, [29, 31]),
    ]

    for n, e, modulus, N, K, syndrome in cases:
        m = n // e
        dir_info = full_degree_zero_directions(n, e, modulus)
        assert dir_info["n"] == n
        assert dir_info["e"] == e
        assert dir_info["m"] == m
        assert len(dir_info["directions"]) == e
        assert dir_info["kernel_dimension"] == m * (e - 2)
        assert dir_info["expanded_binary_rank"] == n
        assert dir_info["verified"] is True

        points = list(range(1, N + 1))
        targets = [0] * (e * K) + [1] * (N - e * K)
        res = solve_subfield_derandomized(
            n, e, modulus, points, targets, syndrome=syndrome
        )

        assert res["restricted_binary_rank"] == n * K
        assert res["verified"] is True
        assert res["verified_parity"] is True
        assert res["verified_trace"] is True
        assert res["uniform_sampler"] is False
        assert res["hardness_evidence"] is False
        assert len(res["witness"]) == N
        _assert_original_equations(n, modulus, points, targets, syndrome, res)


@pytest.mark.parametrize("n,e,modulus,N", [(6, 3, 67, 36), (9, 3, 0x211, 81), (8, 4, 0x11b, 64)])
def test_native_default_uses_floor_eighth_for_even_and_odd_lengths(n, e, modulus, N):
    K = N // 8
    points = list(range(N))
    targets = [0] * (e * K) + [1] * (N - e * K)
    result = solve_subfield_derandomized(n, e, modulus, points, targets)
    explicit = solve_subfield_derandomized(n, e, modulus, points, targets, syndrome=[0] * K)

    assert result == explicit
    assert result["K"] == K
    assert result["syndrome"] == [0] * K
    assert result["restricted_binary_rank"] == n * K
    assert result["verified"] is True
    _assert_original_equations(n, modulus, points, targets, [0] * K, result)


def test_explicit_syndrome_keeps_arbitrary_positive_check_count():
    points = [0, 1, 63]
    targets = [0] * 3
    result = solve_subfield_derandomized(6, 3, 67, points, targets, syndrome=[63])
    assert result["K"] == 1  # N // 8 is zero, but this explicit K is valid.
    assert result["verified"] is True
    _assert_original_equations(6, 67, points, targets, [63], result)


def test_valid_explicit_zero_selector_preserves_order_and_original_equations():
    points = [2, 5, 0, 63, 1, 7]
    targets = [0, 1, 0, 0, 1, 0]
    indices = [5, 0, 3]
    result = solve_subfield_derandomized(
        6, 3, 67, points, targets, syndrome=[17], zero_indices=indices
    )
    assert result["selected_zero_indices"] == indices
    assert {i for i, _ in result["selected_direction_slots"]} == set(indices)
    assert result["verified"] is True
    _assert_original_equations(6, 67, points, targets, [17], result)


def _unexpected_arithmetic(*args, **kwargs):
    pytest.fail("invalid input reached field arithmetic or direction construction")


@pytest.mark.parametrize("name", ["theta", "beta"])
@pytest.mark.parametrize("value", [-1, 256, 0x11b, True, False, 2.0, "2", []])
def test_direction_elements_rejected_before_any_field_arithmetic(monkeypatch, name, value):
    monkeypatch.setattr(subfield, "mul", _unexpected_arithmetic)
    with pytest.raises(ValueError, match=name):
        full_degree_zero_directions(8, 4, 0x11b, **{name: value})


def test_zero_beta_rejected_before_any_field_arithmetic(monkeypatch):
    monkeypatch.setattr(subfield, "mul", _unexpected_arithmetic)
    with pytest.raises(ValueError, match="beta must be nonzero"):
        full_degree_zero_directions(8, 4, 0x11b, beta=0)


@pytest.mark.parametrize("entrypoint", ["basis", "directions", "solver"])
@pytest.mark.parametrize(
    "name,value",
    [("n", v) for v in (0, -8, True, False, 8.0, "8", None)]
    + [("e", v) for v in (0, -4, True, False, 4.0, "4", None)]
    + [("modulus", v) for v in (0, -0x11b, True, False, 283.0, "283", None, 67, 0x211)],
)
def test_extension_parameters_are_strict_before_field_arithmetic(monkeypatch, entrypoint, name, value):
    monkeypatch.setattr(subfield, "mul", _unexpected_arithmetic)
    kwargs = dict(n=8, e=4, modulus=0x11b)
    kwargs[name] = value
    with pytest.raises(ValueError):
        if entrypoint == "basis":
            subfield_kernel_basis(**kwargs)
        elif entrypoint == "directions":
            full_degree_zero_directions(**kwargs)
        else:
            solve_subfield_derandomized(**kwargs, points=list(range(8)), targets=[0] * 8)


@pytest.mark.parametrize("entrypoint", ["directions", "solver"])
def test_reducible_modulus_rejected(entrypoint):
    with pytest.raises(ValueError, match="not irreducible"):
        if entrypoint == "directions":
            full_degree_zero_directions(8, 4, 0x100)
        else:
            solve_subfield_derandomized(8, 4, 0x100, list(range(8)), [0] * 8)


@pytest.mark.parametrize("name", ["points", "targets", "syndrome"])
@pytest.mark.parametrize("value", [-1, 64, True, False, 0.0, "0", None, []])
def test_solver_elements_are_canonical_without_coercion(monkeypatch, name, value):
    monkeypatch.setattr(subfield, "full_degree_zero_directions", _unexpected_arithmetic)
    kwargs = dict(points=[0, 1, 2], targets=[0, 0, 0], syndrome=[1])
    kwargs[name][0] = value
    with pytest.raises(ValueError, match=name):
        solve_subfield_derandomized(6, 3, 67, **kwargs)


@pytest.mark.parametrize("N,syndrome", [(0, None), (1, None), (7, None), (8, [])])
def test_zero_check_count_rejected(monkeypatch, N, syndrome):
    monkeypatch.setattr(subfield, "full_degree_zero_directions", _unexpected_arithmetic)
    with pytest.raises(ValueError, match="K must be positive"):
        solve_subfield_derandomized(6, 3, 67, list(range(N)), [0] * N, syndrome=syndrome)


@pytest.mark.parametrize(
    "indices",
    [[-1, 0, 2], [3, 0, 2], [0, 0, 2], [True, 0, 2], [False, 1, 2],
     [0.0, 1, 2], ["0", 1, 2], [None, 1, 2], [[], 1, 2], [0, 1], [0, 1, 2, 0]],
)
def test_invalid_zero_selectors_rejected_before_construction(monkeypatch, indices):
    monkeypatch.setattr(subfield, "full_degree_zero_directions", _unexpected_arithmetic)
    with pytest.raises(ValueError, match="zero_indices"):
        solve_subfield_derandomized(6, 3, 67, [0, 1, 2], [0] * 3, syndrome=[1], zero_indices=indices)


def test_zero_selector_must_select_zero_targets(monkeypatch):
    monkeypatch.setattr(subfield, "full_degree_zero_directions", _unexpected_arithmetic)
    with pytest.raises(ValueError, match="target bit 0"):
        solve_subfield_derandomized(
            6, 3, 67, [0, 1, 2, 3], [0, 0, 0, 1], syndrome=[1], zero_indices=[0, 1, 3]
        )


def test_duplicate_points_and_nonbinary_targets_rejected():
    with pytest.raises(ValueError, match="points must be distinct"):
        solve_subfield_derandomized(6, 3, 67, [0, 0, 2], [0] * 3, syndrome=[1])
    with pytest.raises(ValueError, match="binary bits"):
        solve_subfield_derandomized(6, 3, 67, [0, 1, 2], [0, 2, 0], syndrome=[1])


@pytest.mark.parametrize("failure", ["parity", "trace", "noncanonical"])
def test_final_original_equation_checks_fail_closed(monkeypatch, failure):
    original_solve, original_trace, original_mul = subfield.solve, subfield.trace, subfield.mul
    final_solve = False

    def corrupted_solve(pivots, target, dim=None):
        nonlocal final_solve
        if len(pivots) == 6:
            final_solve = True
            if failure == "parity":
                return 0, 0  # Lie about solving the nonzero syndrome.
        return original_solve(pivots, target, dim)

    def corrupted_trace(*args):
        if final_solve and failure == "trace":
            return 1  # Fail only the final inverse-trace checks, not construction.
        return original_trace(*args)

    def corrupted_mul(*args):
        if final_solve and failure == "noncanonical":
            return -1
        return original_mul(*args)

    monkeypatch.setattr(subfield, "solve", corrupted_solve)
    monkeypatch.setattr(subfield, "trace", corrupted_trace)
    monkeypatch.setattr(subfield, "mul", corrupted_mul)
    message = "noncanonical" if failure == "noncanonical" else "original parity or inverse-trace"
    with pytest.raises(RuntimeError, match=message):
        solve_subfield_derandomized(6, 3, 67, [0, 1, 2], [0] * 3, syndrome=[1])


@pytest.mark.parametrize("control", [False, True])
def test_failed_elimination_cannot_claim_verification(monkeypatch, control):
    directions = full_degree_zero_directions(6, 3, 67)
    monkeypatch.setattr(subfield, "full_degree_zero_directions", lambda *args, **kwargs: directions)
    monkeypatch.setattr(subfield, "add", lambda *args, **kwargs: False)
    with pytest.raises(RuntimeError, match="not independent"):
        if control:
            greedy_vs_matroid_exchange_control()
        else:
            solve_subfield_derandomized(6, 3, 67, [0, 1, 2], [0] * 3, syndrome=[1])


def test_optimized_python_preserves_solver_control_and_fail_closed_checks():
    test_file = Path(__file__).resolve()
    result = subprocess.run(
        ["/opt/anaconda3/bin/python", "-B", "-O", "-m", "pytest", "-q", "-p", "no:cacheprovider",
         str(test_file), "-k", "not optimized_python"],
        cwd=test_file.parents[1],
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1"},
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_rejection_on_insufficient_zeros_and_invalid_parameters():
    """Verify rejection when target conditions or parameters are invalid."""
    # Insufficient zeros: need e * K = 4 * 2 = 8 zeros, but only 7 provided
    n, e, modulus = 8, 4, 0x11b
    points = list(range(1, 17))
    targets = [0] * 7 + [1] * 9
    syndrome = [1, 2]
    with pytest.raises(ValueError, match="insufficient zero-target coordinates"):
        solve_subfield_derandomized(n, e, modulus, points, targets, syndrome=syndrome)

    # e < 3
    with pytest.raises(ValueError, match="must be >= 3"):
        subfield_kernel_basis(8, 2, 0x11b)

    with pytest.raises(ValueError, match="must be >= 3"):
        full_degree_zero_directions(8, 2, 0x11b)

    # (1 << m) < e: e.g. n=6, e=6, m=1, where 2^1 = 2 < 6
    with pytest.raises(ValueError, match="must be >= e"):
        subfield_kernel_basis(6, 6, 67)

    with pytest.raises(ValueError, match="must be >= e"):
        full_degree_zero_directions(6, 6, 67)

    # n % e != 0
    with pytest.raises(ValueError, match="must be divisible by e"):
        subfield_kernel_basis(8, 3, 0x11b)

    with pytest.raises(ValueError, match="must be divisible by e"):
        full_degree_zero_directions(8, 3, 0x11b)

    # Non-irreducible modulus
    with pytest.raises(ValueError, match="not irreducible"):
        subfield_kernel_basis(8, 4, 0x100)


def test_failed_greedy_control_and_matroid_exchange_recovery():
    """Verify failed greedy control on k-hyperplane and matroid exchange recovery."""
    res = greedy_vs_matroid_exchange_control()
    assert res["greedy_size"] == 5
    assert res["greedy_binary_rank"] == 10
    assert res["greedy_stuck"] is True
    assert res["matroid_size"] == 6
    assert res["matroid_binary_rank"] == 12
    assert len(res["augmenting_path"]) >= 3
