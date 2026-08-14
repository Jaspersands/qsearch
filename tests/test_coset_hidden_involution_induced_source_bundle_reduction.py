import pytest

from coset_hidden_involution_induced_source_bundle_reduction import (
    audit_pair_connection_cocycle_distinction,
    audit_s3_induced_source,
    build_induced_source_bundle_report,
    induced_source_scaling_record,
    s3_induced_source_multiplicities,
    s3_synthesis_multiplicity_ranks,
    write_induced_source_bundle_report,
)


@pytest.mark.parametrize("copy_count", (1, 2, 3))
def test_s3_source_is_induced_and_synthesis_has_predicted_blocks(copy_count):
    control = audit_s3_induced_source(copy_count)
    assert control.induced_source_normal_form_verified
    assert control.maximum_synthesis_equivariance_residual < 1e-9
    assert control.observed_source_character_identity == pytest.approx(
        3 ** (copy_count + 1)
    )
    assert control.observed_source_character_transposition == pytest.approx(1.0)
    assert control.observed_source_character_three_cycle == pytest.approx(0.0)
    assert (
        control.observed_trivial_source_multiplicity,
        control.observed_sign_source_multiplicity,
        control.observed_standard_source_multiplicity,
    ) == s3_induced_source_multiplicities(copy_count)
    assert (
        control.observed_trivial_synthesis_multiplicity_rank,
        control.observed_sign_synthesis_multiplicity_rank,
        control.observed_standard_synthesis_multiplicity_rank,
    ) == s3_synthesis_multiplicity_ranks(copy_count)
    assert control.observed_total_synthesis_rank == (
        3 ** (copy_count + 1) - 2 * (copy_count + 1)
    )


def test_pair_polar_holonomy_is_not_the_induced_stabilizer_cocycle():
    control = audit_pair_connection_cocycle_distinction()
    assert control.control_verified
    assert control.stabilizer_cocycle_spectrum == (-1, 1, 1)
    assert control.canonical_pair_holonomy_spectrum == (-1, -1, 1)
    assert not control.spectra_equal
    assert not control.pair_polar_connection_is_induced_bundle_cocycle


def test_induced_source_scaling_keeps_the_physical_lift_open():
    rows = [induced_source_scaling_record(k) for k in (1, 2, 8, 32, 128)]
    assert all(row.branch_covariance_fourier_transform_available for row in rows)
    assert all(not row.physical_to_source_analysis_compiled for row in rows)
    assert all(not row.multiplicity_polar_compiled for row in rows)
    assert all(
        row.standard_synthesis_kernel_multiplicity == row.copy_count + 1
        for row in rows
    )

    with pytest.raises(ValueError, match="positive"):
        s3_induced_source_multiplicities(0)
    with pytest.raises(ValueError, match="positive"):
        s3_synthesis_multiplicity_ranks(0)


def test_report_resolves_covariance_but_not_multiplicity_polar(tmp_path):
    report = build_induced_source_bundle_report(
        finite_copy_counts=(1, 2),
        scaling_copy_counts=(1, 2, 8, 32),
    )
    assert report.theorem.theorem_verified
    assert report.theorem.induced_source_identity_proved
    assert report.theorem.frobenius_block_reduction_proved
    assert not report.theorem.pair_polar_gluing_required_for_global_covariance
    assert report.theorem.branch_covariance_fourier_transform_constructed
    assert not report.theorem.physical_to_source_analysis_compiled
    assert not report.theorem.multiplicity_support_polar_compiled
    assert not report.theorem.full_orbit_synthesis_polar_compiled
    assert report.claim_gate["orbit_source_is_induced_bundle"]
    assert not report.claim_gate["global_covariance_requires_pair_polar_gluing"]
    assert not report.claim_gate["physical_to_branch_source_lift_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_induced_source_bundle_report(
        tmp_path / "induced-source.json",
        finite_copy_counts=(1, 2),
        scaling_copy_counts=(1, 2, 8),
    )
    assert payload["status"] == (
        "induced-branch-covariance-resolved-multiplicity-polar-open"
    )
    assert payload["headline_metrics"][
        "branch_covariance_fourier_transform_count"
    ] == 1
