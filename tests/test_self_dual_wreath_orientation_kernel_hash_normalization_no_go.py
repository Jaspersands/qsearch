from __future__ import annotations

import json

from self_dual_wreath_orientation_kernel_hash_normalization_no_go import (
    audit_hash_conditioned_analysis,
    generic_polar_degree_lower_bound,
    natural_hash_normalization_scaling,
    run_hash_normalization_no_go,
    write_hash_normalization_no_go_report,
)


THRESHOLD = (
    ((3,), (2, 1)),
    ((3,), (1, 1, 1)),
    ((2, 1), (1, 1, 1)),
)


def test_kernel_mean_is_exactly_physical_sector_mass_scale() -> None:
    for target in ((3,), (2, 1), (1, 1, 1)):
        control = audit_hash_conditioned_analysis(
            3,
            target,
            THRESHOLD,
            hash_output_bits=1,
            control_id=str(target),
        )
        assert control.sector_mass_mean_identity_residual < 1e-9


def test_hash_conditioned_canonical_gram_has_retained_size_normalization() -> None:
    control = audit_hash_conditioned_analysis(
        3,
        (2, 1),
        THRESHOLD,
        hash_output_bits=1,
        control_id="standard",
    )
    assert control.orientation_count == 8
    assert control.retained_orientation_count == 4
    assert control.hash_density == 0.5
    assert control.conditional_analysis_gram_residual < 1e-9
    assert control.exact_hash_conditioned_normalization_verified


def test_hash_conditioning_does_not_change_the_mathematical_polar() -> None:
    control = audit_hash_conditioned_analysis(
        3,
        (3,),
        THRESHOLD,
        hash_output_bits=1,
        control_id="trivial",
    )
    assert control.conditional_polar_scale_invariance_residual < 1e-9


def test_uniform_full_rank_hash_family_preserves_target_mass() -> None:
    control = audit_hash_conditioned_analysis(
        3,
        (2, 1),
        THRESHOLD,
        hash_output_bits=1,
        control_id="mass-transfer",
    )
    assert control.enumerated_full_rank_hash_fiber_count > 0
    assert control.maximum_orientation_inclusion_probability_residual < 1e-12
    assert control.conditioned_target_mass_transfer_residual < 1e-12


def test_generic_polar_degree_grows_as_inverse_singular_scale() -> None:
    assert generic_polar_degree_lower_bound(0.5) >= 1
    assert generic_polar_degree_lower_bound(0.01) > 90
    assert generic_polar_degree_lower_bound(0.001) > 900


def test_inverse_polynomial_hash_still_has_factorial_natural_normalization() -> None:
    row = natural_hash_normalization_scaling(512)
    assert row.inverse_polynomial_hash_acceptance
    assert row.ideal_almost_scalar_kernel_granted
    assert row.log2_high_row_canonical_singular_value_upper_bound < -3000
    assert row.log2_generic_scalar_whitening_degree_lower_bound > 3000
    assert not row.generic_scalar_whitening_polynomial


def test_report_rejects_scalar_hash_whitening_but_not_structured_polar() -> None:
    report = run_hash_normalization_no_go()
    assert report.theorem.theorem_verified
    assert report.claim_gate["hash_conditioned_canonical_gram_identified"]
    assert report.claim_gate["kernel_mean_linked_to_physical_sector_mass"]
    assert report.claim_gate["canonical_hash_scalar_whitening_rejected"]
    assert not report.claim_gate[
        "ideal_almost_scalar_hash_kernel_would_enable_scalar_whitening"
    ]
    assert not report.claim_gate["direct_structured_orientation_polar_ruled_out"]
    assert not report.claim_gate["actual_physical_pgm_rejected"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_writer_emits_live_hash_normalization_artifact(tmp_path) -> None:
    path = tmp_path / "hash-normalization-no-go.json"
    payload = write_hash_normalization_no_go_report(path)
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert loaded["status"] == payload["status"]
    assert loaded["headline_metrics"][
        "hash_scalar_whitening_normalization_no_go_count"
    ] == 1
