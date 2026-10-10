"""Test suite for Non-Abelian Coset Multiplicity-Carrier Decoupling Trilemma."""
from __future__ import annotations

import pytest

from theorems.coset_multiplicity_carrier_trilemma import (
    standard_rep_matrix,
    verify_three_copy_commutator,
    verify_commutant_zero_information,
    compute_commutant_dimension,
    build_scaling_profiles,
    build_report,
)


def test_standard_rep_matrix():
    """Verify standard representation matrix properties."""
    # Transposition (0, 1) in S_3 (dim 2)
    V = standard_rep_matrix((1, 0, 2), 3)
    assert V.shape == (2, 2)
    # V^2 must be identity
    assert (V @ V == [[1, 0], [0, 1]]).all()
    # Trace must be fix((0, 1)) - 1 = 1 - 1 = 0
    assert V.trace() == 0


def test_three_copy_commutator_entry():
    """Verify [K_12, K_23]_{(0,0,0),(0,0,1)} = n for n in {3, 4, 5}."""
    for n in (3, 4, 5):
        audit = verify_three_copy_commutator(n)
        assert audit["observed_witness_entry"] == n
        assert audit["entry_matches_closed_form"] is True
        assert audit["is_strictly_noncommuting"] is True


def test_commutant_zero_information():
    """Verify that commutant observables have identically zero mutual information with hidden conjugacy elements."""
    for n in (3, 4, 5):
        audit = verify_commutant_zero_information(n)
        assert audit["trace_variation"] < 1e-12
        assert audit["is_constant_across_class"] is True
        assert audit["mutual_information_bits"] == 0.0
        assert audit["zero_information_verified"] is True


def test_commutant_dimension():
    """Verify commutant dimension dim(Commutant(V^k)) values."""
    # S_3: dim(V) = 2. dim(Commutant(V^3)) = 11
    assert compute_commutant_dimension(3, 3) == 11
    # S_4: dim(V) = 3. dim(Commutant(V^3)) = 31
    assert compute_commutant_dimension(4, 3) == 31
    # S_5: dim(V) = 4. dim(Commutant(V^3)) = 40
    assert compute_commutant_dimension(5, 3) == 40


def test_scaling_profiles():
    """Verify scaling profiles table and exponential Racah complexity."""
    profiles = build_scaling_profiles(n_values=(3, 4, 5, 6, 8, 16))
    assert len(profiles) == 6
    for p in profiles:
        assert p["commutator_matches_n"] is True
        assert p["commutant_mutual_information_bits"] == 0.0

    # At n=16, Racah complexity is exponential
    p16 = profiles[-1]
    assert p16["n"] == 16
    assert p16["racah_complexity_exponential"] is True
    assert p16["asymptotic_mult_dimension_log2_k_n"] > 80.0


def test_build_report():
    """Verify report generation dictionary and headline metrics."""
    report = build_report()
    assert report["status"] == "PASS"
    metrics = report["headline_metrics"]
    assert metrics["all_commutator_witnesses_verified"] is True
    assert metrics["all_commutant_zero_information_verified"] is True
    assert metrics["speedup_claim_allowed"] is False
    assert metrics["accepted_speedup_candidate"] is False
    assert metrics["tail_n"] == 16
    assert metrics["tail_commutator_witness"] == 16
