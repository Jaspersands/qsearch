import pytest

from coset_hidden_involution_standard_block_recoupling import (
    analytic_squared_principal_cosines,
    audit_standard_block_tensors,
    build_standard_block_recoupling_report,
    cross_gram_matrix,
    invariant_gram_matrix,
    repeated_pair_squared_cosine,
    standard_block_scaling_record,
    symmetric_sector_trace_and_determinant,
)


def test_invariant_gram_formulas_have_the_required_asymmetry() -> None:
    physical = invariant_gram_matrix(8)
    source = invariant_gram_matrix(4)
    cross = cross_gram_matrix(4)
    assert physical[1][1] == 49
    assert source[1][1] == 9
    assert cross[1][1] == 9
    assert cross[0][1] * 2 == cross[1][0]


@pytest.mark.parametrize("half_degree", (4, 5, 6))
def test_dense_invariant_tensors_match_the_exact_spectrum(half_degree: int) -> None:
    row = audit_standard_block_tensors(half_degree)
    assert row.physical_fixed_multiplicity == 4
    assert row.source_fixed_multiplicity == 4
    assert row.maximum_spectrum_residual < 1e-10
    assert row.full_rank_verified
    assert row.nonuniform_spectrum_verified
    assert row.invariant_tensor_formula_verified


def test_exact_spectrum_is_scalable_full_rank_and_nonuniform() -> None:
    for half_degree in (4, 5, 8, 16, 32, 64):
        spectrum = analytic_squared_principal_cosines(half_degree)
        pair = float(repeated_pair_squared_cosine(half_degree))
        trace, determinant = symmetric_sector_trace_and_determinant(half_degree)
        assert len(spectrum) == 4
        assert min(spectrum) > 0
        assert max(spectrum) - min(spectrum) > 0.1
        assert spectrum.count(pair) == 2
        assert spectrum[0] + spectrum[-1] == pytest.approx(float(trace))
        assert spectrum[0] * spectrum[-1] == pytest.approx(float(determinant))


def test_spectrum_converges_to_one_eighth_and_three_quarters() -> None:
    spectrum = analytic_squared_principal_cosines(100_000)
    assert spectrum[0] == pytest.approx(1 / 8, abs=1e-5)
    assert spectrum[1] == pytest.approx(1 / 4, abs=1e-5)
    assert spectrum[2] == pytest.approx(1 / 4, abs=1e-5)
    assert spectrum[3] == pytest.approx(1 / 4, abs=1e-5)


def test_standard_block_mass_is_negligible_despite_succinct_recoupling() -> None:
    rows = [standard_block_scaling_record(value) for value in (4, 8, 16, 32)]
    assert all(row.full_rank_nonuniform_matrix_block for row in rows)
    assert all(row.succinct_multiplicity_diagonalization_proved for row in rows)
    assert not any(row.natural_mass_block for row in rows)
    assert rows[-1].log2_source_isotypic_fraction < rows[0].log2_source_isotypic_fraction
    assert rows[-1].log2_alternative_isotypic_mass < rows[0].log2_alternative_isotypic_mass
    assert not any(row.coherent_fourier_block_transform_compiled for row in rows)


def test_report_falsifies_scalarization_without_claiming_a_detector() -> None:
    report = build_standard_block_recoupling_report()
    assert report.headline_metrics["finite_tensor_control_failure_count"] == 0
    assert report.claim_gate["scalable_full_rank_nonuniform_matrix_block_proved"] is True
    assert report.claim_gate["universal_scalarization_falsified"] is True
    assert report.claim_gate[
        "succinct_standard_block_multiplicity_diagonalization_proved"
    ] is True
    assert report.claim_gate["natural_huge_block_transform_resolved"] is False
    assert report.claim_gate["natural_mass_detector_constructed"] is False
    assert report.claim_gate["coherent_fourier_block_transform_compiled"] is False
    assert report.claim_gate["binary_hidden_involution_detector_constructed"] is False
    assert report.claim_gate["speedup_claim_allowed"] is False
