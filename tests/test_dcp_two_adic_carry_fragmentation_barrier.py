"""Test suite for 2-Adic Carry Recurrence & Dictionary Walk Fragmentation Barrier."""
from __future__ import annotations

import math
import random
import pytest

from theorems.dcp_two_adic_carry_fragmentation_barrier import (
    binomial_vector_count,
    exact_relation_weight_bound,
    critical_relation_weight_formula,
    carry_bit_recurrence,
    carry_integer_formula,
    audit_exact_fiber_graphs,
    audit_carry_entropy,
    audit_asymptotic_scaling,
    generate_report,
)


def test_binomial_vector_count():
    """Verify exact binomial vector count against hand-calculated values."""
    # For m=3, w_max=1: comb(3, 1)*2^1 = 3*2 = 6
    assert binomial_vector_count(3, 1) == 6
    # For m=3, w_max=2: 6 + comb(3, 2)*2^2 = 6 + 3*4 = 18
    assert binomial_vector_count(3, 2) == 18
    # For m=3, w_max=3: 18 + comb(3, 3)*2^3 = 18 + 1*8 = 26 (which is 3^3 - 1)
    assert binomial_vector_count(3, 3) == 26
    # Edge case: w_max <= 0
    assert binomial_vector_count(5, 0) == 0


def test_exact_carry_identity():
    """Verify bit-by-bit column carry recurrence matches integer division formula."""
    rng = random.Random(42)
    m = 8
    k = 4
    modulus = 1 << k
    labels = [rng.randrange(modulus) for _ in range(m)]
    target = rng.randrange(modulus)

    fiber_count = 0
    for x in range(1 << m):
        int_sum = sum(((x >> i) & 1) * labels[i] for i in range(m))
        if (int_sum % modulus) == target:
            fiber_count += 1
            c_bit = carry_bit_recurrence(labels, target, x, k)
            c_int = carry_integer_formula(labels, target, x, k)
            assert c_bit == c_int, f"Mismatch at x={x}: c_bit={c_bit}, c_int={c_int}"
            assert 0 <= c_bit < m, f"Carry out of bounds: {c_bit}"

    assert fiber_count > 0, "Fiber should be non-empty"


def test_critical_weight_threshold():
    """Verify critical weight threshold properties and monotonicity."""
    m = 34
    k1 = 8
    k2 = 16
    k3 = 24

    w1 = exact_relation_weight_bound(m, k1, epsilon=0.05)
    w2 = exact_relation_weight_bound(m, k2, epsilon=0.05)
    w3 = exact_relation_weight_bound(m, k3, epsilon=0.05)

    assert w1 <= w2 <= w3, "Weight threshold should be monotonically non-decreasing in k"
    assert w2 == 2, f"Expected W*(16, 34)=2, got {w2}"

    # Verify formula approximation
    w_formula = critical_relation_weight_formula(k2, m, lambda_bits=2.0)
    assert w_formula >= 1


def test_audit_exact_fiber_graphs():
    """Verify exact fiber graph audit produces valid records."""
    records = audit_exact_fiber_graphs(configs=((8, 4),), num_trials=2, seed=99)
    assert len(records) == 2
    for r in records:
        assert r.status == "PASS"
        assert r.exact_identity_verified is True
        assert 0.0 <= r.isolated_fraction <= 1.0
        assert 0.0 <= r.max_component_fraction <= 1.0
        assert r.spectral_gap >= 0.0
        assert r.distinct_carry_count <= r.register_count


def test_audit_carry_entropy():
    """Verify carry entropy audit verifies entropy bounds."""
    records = audit_carry_entropy(configs=((10, 5),), seed=88)
    assert len(records) == 1
    r = records[0]
    assert r.status == "PASS"
    assert r.carry_shannon_entropy <= math.log2(r.register_count) + 1e-9
    assert r.conditional_fiber_entropy > 0.0
    assert r.entropy_ratio_retained >= 0.50
    assert r.max_carry_value < r.register_count


def test_audit_asymptotic_scaling():
    """Verify asymptotic scaling ledger reproduces degree collapse and isolated vertex domination."""
    records = audit_asymptotic_scaling(n_values=(64, 128, 512, 1024), alpha=0.5, dict_exponent=3.0)
    assert len(records) == 4

    # At n=64
    r64 = records[0]
    assert r64.critical_weight_threshold == 4

    # At n=512
    r512 = records[2]
    assert r512.security_parameter_n == 512
    assert r512.critical_weight_threshold == 42
    assert r512.degree_collapses_to_zero is True
    assert r512.isolated_dominates is True
    assert r512.isolated_fraction_lower_bound > 0.9999

    # At n=1024
    r1024 = records[3]
    assert r1024.security_parameter_n == 1024
    assert r1024.critical_weight_threshold == 85
    assert r1024.average_degree_bound < 1e-15
    assert r1024.isolated_fraction_lower_bound >= 0.999999


def test_generate_report():
    """Verify full report generation dictionary and headline metrics."""
    report = generate_report(write_to_file=False)
    assert report["status"] == "PASS"
    metrics = report["headline_metrics"]
    assert metrics["all_exact_identity_verified"] is True
    assert metrics["speedup_claim_allowed"] is False
    assert metrics["accepted_speedup_candidate"] is False
    assert metrics["tail_security_n"] == 1024
    assert metrics["tail_average_degree_bound"] < 1e-15
    assert metrics["tail_isolated_vertex_fraction_lower_bound"] >= 0.999999
