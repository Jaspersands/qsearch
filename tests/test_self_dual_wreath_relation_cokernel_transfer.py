import numpy as np

from self_dual_wreath_relation_cokernel_transfer import (
    _abstract_controls,
    _physical_controls,
    audit_leaf_subspaces,
    run_relation_cokernel_transfer,
)


def test_pair_generated_relations_equal_the_full_cokernel() -> None:
    control = _abstract_controls()[0]

    assert control.synthesis_kernel_dimension == 2
    assert control.pair_relation_rank == 2
    assert control.emergent_h0_dimension == 0
    assert control.pair_relations_exhaust_synthesis_kernel
    assert control.pair_complement_polar_support_residual < 1e-10
    assert control.trimmed_relation_pgm_trace_loss < 1e-10
    assert control.exact_relation_cokernel_audit


def test_three_lines_in_a_plane_falsify_universal_pair_generation() -> None:
    control = _abstract_controls()[1]

    assert control.synthesis_rank == 2
    assert control.synthesis_kernel_dimension == 1
    assert control.pair_relation_coefficient_dimension == 0
    assert control.pair_relation_rank == 0
    assert control.emergent_h0_dimension == 1
    assert not control.pair_relations_exhaust_synthesis_kernel
    assert control.pair_complement_polar_support_residual > 0.99
    assert control.exact_relation_cokernel_audit


def test_partial_pair_trim_is_signal_free_even_when_h0_remains() -> None:
    control = _abstract_controls()[2]

    assert control.pair_relation_rank == 1
    assert control.emergent_h0_dimension == 1
    assert control.trimmed_relation_rank == 1
    assert control.trimmed_relation_polar_overlap_residual < 1e-10
    assert control.trimmed_relation_pgm_trace_loss < 1e-10
    assert control.relation_trim_has_zero_ideal_pgm_state_loss
    assert not control.pair_relations_exhaust_synthesis_kernel


def test_zero_state_loss_holds_for_a_dense_arbitrary_relation_trim() -> None:
    e0 = np.asarray([[1.0], [0.0]], dtype=complex)
    control = audit_leaf_subspaces(
        "DENSE-TRIM",
        "test",
        (e0, e0, e0, e0, e0),
    )

    assert control.pair_relation_rank == 4
    assert control.trimmed_relation_rank == 2
    assert control.trimmed_relation_pgm_trace_loss < 1e-10
    assert control.full_kernel_polar_overlap_residual < 1e-10
    assert control.polar_support_cokernel_identity_residual < 1e-10


def test_physical_controls_reproduce_augmented_h0_boundary() -> None:
    w3, w5 = _physical_controls()

    assert w3.synthesis_kernel_dimension == 2
    assert w3.pair_relation_rank == 0
    assert w3.emergent_h0_dimension == 2
    assert not w3.pair_relations_exhaust_synthesis_kernel
    assert w3.exact_relation_cokernel_audit

    assert w5.synthesis_kernel_dimension == 5
    assert w5.pair_relation_rank == 5
    assert w5.emergent_h0_dimension == 0
    assert w5.pair_relations_exhaust_synthesis_kernel
    assert w5.exact_relation_cokernel_audit


def test_report_resolves_state_transfer_but_blocks_sampler_claim() -> None:
    report = run_relation_cokernel_transfer()

    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.headline_metrics["zero_state_loss_control_count"] == 5
    assert report.claim_gate["exact_relation_cokernel_identity_proved"]
    assert report.claim_gate["relation_trim_zero_pgm_state_loss_proved"]
    assert not report.claim_gate[
        "coefficient_to_pgm_trace_comparison_still_needed"
    ]
    assert not report.claim_gate[
        "pair_relations_exhaust_full_cokernel_for_all_n"
    ]
    assert not report.claim_gate["coherent_full_cokernel_projector_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
