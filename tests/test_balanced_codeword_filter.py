from fractions import Fraction
from itertools import combinations, product

import pytest

from theorems.balanced_codeword_filter import (
    ceil_log2_fraction, filter_budget, nonzero_pair_residual, projective_line_attack,
    reciprocal_trace, reference_control, root_spectrum,
)
from theorems.explicit_quadratic_opi import element, encoded


@pytest.mark.parametrize("bits", [2, 3, 4, 5, 6])
def test_balanced_spectra_and_exact_nonzero_pair_cancellation(bits):
    q = 1 << bits
    roots0, b0 = root_spectrum(bits, 0)
    roots1, b1 = root_spectrum(bits, 1)
    assert len(roots0) == len(roots1) == q//2
    assert set(roots0).isdisjoint(roots1)
    assert b0[0] == b1[0] == q//2
    assert sum(x*x for x in b0) == q*q//2
    assert all(b0[x] == -b1[x] for x in range(1, q))
    assert all(nonzero_pair_residual(b0, x) == 0 for x in range(1, q))
    assert all(nonzero_pair_residual(b1, x) == 0 for x in range(1, q))
    # W=2*b, and the conservative nonzero probability bound is 4/q.
    assert max(4*x*x for x in b0[1:]) <= 8*q


def test_omitting_the_zero_extension_correction_is_not_safe():
    _, spectrum = root_spectrum(5, 0)
    assert max(4*x*x for x in spectrum[1:]) > 4*32


def test_balance_and_phase_are_real_hypotheses():
    q = 8
    # Unbalanced indicator: integer convolution leaves (q-2*|S|)*b(d).
    roots = {0, 1, 2, 3, 4}
    spectrum = tuple(sum((-1)**((u & x).bit_count() % 2) for x in roots) for u in range(q))
    assert any(nonzero_pair_residual(spectrum, d) for d in range(1, q))
    _, balanced = root_spectrum(3, 0)
    assert any(nonzero_pair_residual(tuple(abs(x) for x in balanced), d) for d in range(1, q))


def test_local_identity_for_every_balanced_boolean_function_on_three_bits():
    for roots in combinations(range(8), 4):
        spectrum = tuple(sum((-1)**((u & x).bit_count() % 2) for x in roots) for u in range(8))
        assert all(nonzero_pair_residual(spectrum, d) == 0 for d in range(1, 8))


@pytest.mark.parametrize("radius", [1, 2, 3])
def test_full_physical_reference_has_paid_heralds_and_native_readout(radius):
    result = reference_control(radius=radius)
    assert result["enumerated_error_words"] == 4096
    assert result["valid_native_witness_count"] > 0
    assert 0 < result["herald_probability"] <= 1
    assert 0 <= result["valid_output_probability_per_attempt"] <= result["herald_probability"]
    assert 0 <= result["conditional_valid_probability"] <= 1
    for row in result["support_mask_controls"]:
        assert abs(row["coalesced_norm_squared"]-row["source_mass"]) <= result["support_mask_excess_bound"]
    assert result["herald_probability"]+result["tail_probability"]+result["ambiguous_source_mass"] == 1
    if radius >= 2:
        assert result["ambiguous_source_mass"] > 0
        assert result["retained_ball_coalesced_norm_squared"] != result["retained_ball_mass"]


def test_label_dependent_phase_mask_violates_the_support_only_bound():
    result = reference_control(bits=4, length=3, dimension=1, radius=1)
    assert result["phase_stripped_norm_squared"] > 1+result["support_mask_excess_bound"]


def test_distinct_nonconstant_codewords_and_repeated_targets():
    result = reference_control(bits=2, length=4, dimension=2, radius=1, targets=(1, 1, 0, 0))
    assert result["enumerated_codewords"] == 16
    assert result["valid_native_witness_count"] > 0


def test_large_budget_needs_no_field_tables(monkeypatch):
    import theorems.balanced_codeword_filter as module

    def forbidden(*args, **kwargs):
        raise AssertionError("scalable certificate must not enumerate field elements")

    monkeypatch.setattr(module, "element", forbidden)
    monkeypatch.setattr(module, "root_spectrum", forbidden)
    row = filter_budget(61, 61*61, (61*61)//8, (3*61*61)//5)
    assert row["ideal_arithmetic_failure_upper"] < Fraction(1, 2**100)
    assert row["coherent_tail_excess"] > 0
    assert row["tail_mass"] > row["ambiguous_mass_upper"]
    assert row["list_cap"] >= 1
    assert row["gs_interpolation_monomials"] > row["gs_interpolation_constraints"]
    assert row["gs_multiplicity"] <= 5
    assert not row["classical_hardness_established"]
    assert not row["full_quantum_receiver_implemented"]


@pytest.mark.parametrize("args", [(True, 8, 1, 4), (3, 9, 1, 4), (4, 8, 5, 4), (3, 4, 0, 2)])
def test_bad_or_non_johnson_parameters_rejected(args):
    with pytest.raises(ValueError):
        filter_budget(*args)


def test_reference_caps_and_native_bit_validation():
    with pytest.raises(ValueError, match="cap"):
        reference_control(bits=4, length=6)
    with pytest.raises(ValueError, match="target"):
        reference_control(targets=(True, 0, 1, 0))


@pytest.mark.parametrize("value", [Fraction(1), Fraction(1, 8), Fraction(3, 8), Fraction(7), Fraction(1, 3**100)])
def test_report_dyadic_certificate_is_exact(value):
    exponent = ceil_log2_fraction(value)
    power = Fraction(2)**exponent
    assert power/2 < value <= power


def test_classical_line_attack_matches_all_small_native_targets():
    bits, points, vector = 3, (0, 1, 2, 3), (1, 2, 4, 7)
    attainable = {}
    for u in range(1, 1 << bits):
        word = tuple(encoded(element(bits, v)/element(bits, u)) for v in vector)
        attainable[tuple(reciprocal_trace(bits, x) for x in word)] = word
    assert len(attainable) > 1
    for target in product((0, 1), repeat=4):
        result = projective_line_attack(bits, points, 1, vector, target)
        assert (result["status"] == "VERIFIED_CLASSICAL_WITNESS") == (target in attainable)
        if target in attainable:
            assert tuple(reciprocal_trace(bits, x) for x in result["witness"]) == target


def test_line_attack_rejects_wrong_native_code_and_zero_reciprocal():
    with pytest.raises(ValueError, match="native code"):
        projective_line_attack(3, (0, 1, 2, 3), 1, (1, 2, 4, 6), (0, 1, 0, 1))
    # All b=0 is globally trivial (x=0), but may have no nonzero point on a line.
    result = projective_line_attack(3, (0, 1, 2, 3), 1, (1, 2, 4, 7), (0, 0, 0, 0))
    assert result["status"] == "NO_NONZERO_RECIPROCAL_ON_THIS_LINE"
