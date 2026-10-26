import hashlib
from itertools import product
import json
from random import Random

import pytest

from theorems.balanced_codeword_filter import reciprocal_trace
from theorems.cubic_rs_affine_flats import solve_binary
from theorems.explicit_quadratic_opi import element, encoded
from theorems.inverse_trace_algebraic_audit import (
    REPORT, ROOT, affine_lift_countercontrol, compiled_relations, compiled_residuals,
    inverse_graph_residuals, linearized_rows, monomial_masks, multiplier_certificate,
    multiplier_value, native_model_budget, quadratic_lift,
)


@pytest.mark.parametrize("bits", [2, 3, 4, 5])
def test_quadratic_graph_is_exact_including_zero_and_compiler_matches(bits):
    for x, y in product(range(1 << bits), repeat=2):
        residuals = inverse_graph_residuals(bits, x, y)
        expected = encoded(element(bits, x)**-1) if x else 0
        assert (not any(residuals[:2])) == (y == expected)
        assert compiled_residuals(bits, x, y) == residuals
    assert all(mask.bit_count() <= 2 for p in compiled_relations(bits) for mask in p)


def test_both_directions_of_the_inverse_graph_are_necessary_at_zero():
    assert inverse_graph_residuals(5, 0, 1)[0] == 0
    assert inverse_graph_residuals(5, 0, 1)[1] != 0
    assert inverse_graph_residuals(5, 1, 0)[0] != 0
    assert inverse_graph_residuals(5, 1, 0)[1] == 0


@pytest.mark.parametrize("bits", [3, 4, 5, 6, 7])
def test_multiplier_equivalence_is_exact_only_after_zero_handling(bits):
    for x in range(1 << bits):
        for b in (0, 1):
            value = multiplier_value(bits, x, b)
            assert (value == 0) == (x == 0 or reciprocal_trace(bits, x) == b)
    assert multiplier_value(bits, 0, 1) == 0
    assert reciprocal_trace(bits, 0) != 1


@pytest.mark.parametrize("bits,degree", [(17, 7), (31, 10), (61, 14)])
def test_large_sparse_multiplier_certificate_needs_no_field_enumeration(bits, degree):
    row = multiplier_certificate(bits)
    assert row["equation_degree"] == degree
    assert len(row["product_exponents"]) == bits
    assert row["product_degree"] <= row["multiplier_degree"]+row["maximum_cyclic_gap"]-2


def test_inverse_graph_has_full_affine_hull_except_the_excluded_linear_case():
    for n in (2, 3, 4, 5):
        rows = []
        for x in range(1 << n):
            y = encoded(element(n, x)**-1) if x else 0
            rows.append((1 | (x << 1) | (y << (n+1)), 0))
        rank = solve_binary(rows, 2*n+1)["rank"]
        assert rank == (n+1 if n == 2 else 2*n+1)


@pytest.mark.parametrize("bits", [3, 5, 17, 31, 61])
def test_false_relaxed_pair_survives_all_compiled_local_relations(bits):
    result = affine_lift_countercontrol(bits)
    assert result["status"] == "VERIFIED_SPURIOUS_LOCAL_LINEARIZATION_POINT"
    assert result["graph_affine_rank"] == 2*bits+1
    assert not any(result["linearized_residuals"])
    assert any(result["direct_graph_residuals"])
    assert result["genuine_lift_disagreement_count"] > 0
    assert not result["native_witness"]
    assert not result["general_classical_attack_excluded"]


def test_full_span_failure_remains_unknown():
    class ZeroRng:
        def getrandbits(self, bits):
            return 0

    row = affine_lift_countercontrol(17, samples=12, rng=ZeroRng())
    assert row["status"] == "UNKNOWN_AFFINE_SPAN_BUDGET"
    assert row["graph_affine_rank"] == 1


def test_compiled_residuals_match_field_arithmetic_at_large_bits():
    rng = Random(1022)
    for n in (17, 31, 61):
        for _ in range(8):
            x, y = rng.getrandbits(n), rng.getrandbits(n)
            assert compiled_residuals(n, x, y) == inverse_graph_residuals(n, x, y)


def test_native_counts_do_not_invent_independence_or_a_solver():
    row = native_model_budget(17, 289, 36)
    assert row["remaining_binary_variables"] == 8925
    assert row["minimal_quadratic_equations_raw_count"] == 9826
    assert not row["equations_claimed_independent_or_semiregular"]
    assert not row["polynomial_time_solver_established"]


def test_live_affine_combinations_replay_without_trusting_claimed_residuals():
    data = json.loads(REPORT.read_text())
    assert data["source_sha256"] == hashlib.sha256(
        (ROOT / "theorems/inverse_trace_algebraic_audit.py").read_bytes()).hexdigest()
    assert data["proof_sha256"] == hashlib.sha256(
        (ROOT / "research/INVERSE_TRACE_ALGEBRAIC_AUDIT.md").read_bytes()).hexdigest()
    for row in data["false_local_relaxation_certificates"]:
        bits, lifted, xsum, ysum = row["bits"], 0, 0, 0
        assert len(row["selected_graph_points"]) % 2 == 1
        for x, y in row["selected_graph_points"]:
            assert not any(inverse_graph_residuals(bits, x, y))
            lifted ^= quadratic_lift(bits, x, y)
            xsum ^= x
            ysum ^= y
        assert [xsum, ysum] == row["projected_pair"]
        assert lifted == int(row["quadratic_lift_hex"], 16)
        assert not any((r & lifted).bit_count() % 2 for r in linearized_rows(bits))
        assert compiled_residuals(bits, xsum, ysum)[1] != 0


@pytest.mark.parametrize("bits", [2, True, 257])
def test_invalid_multiplier_widths_are_rejected(bits):
    with pytest.raises(ValueError):
        multiplier_certificate(bits)
