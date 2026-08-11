import math

import pytest

from coset_hidden_involution_threshold_compiler_boundary import (
    audit_central_dilation_control,
    build_hidden_involution_threshold_compiler_report,
    generic_markov_degree_lower_bound,
    generic_polynomial_compiler_scaling_record,
    write_hidden_involution_threshold_compiler_report,
)


def test_markov_degree_boundary_is_exponential_in_copy_count():
    assert generic_markov_degree_lower_bound(2) == 2
    assert generic_markov_degree_lower_bound(20) >= math.ceil(
        math.sqrt(2**20 / 3)
    )
    assert generic_markov_degree_lower_bound(40) > 500_000
    with pytest.raises(ValueError, match="positive"):
        generic_markov_degree_lower_bound(0)


@pytest.mark.parametrize(("copies", "helstrom", "central_tv"), ((1, 1 / 6, 1 / 12), (2, 5 / 12, 1 / 8)))
def test_central_dilation_compresses_exactly_but_label_measurement_loses_signal(
    copies, helstrom, central_tv
):
    row = audit_central_dilation_control(3, 1, copies)
    assert row.finite_control_verified
    assert row.compression_identity_residual < 1e-9
    assert row.branch_plus_invariance_commutator_norm > 1e-8
    assert row.helstrom_trace_distance == pytest.approx(helstrom)
    assert row.central_class_sum_measurement_total_variation == pytest.approx(
        central_tv
    )
    assert row.central_measurement_strictly_suboptimal
    assert row.compression_not_reducing_for_class_sum


def test_threshold_scaling_blocks_only_generic_polynomial_compiler():
    row = generic_polynomial_compiler_scaling_record(64)
    assert row.threshold_copy_count == math.ceil(
        math.log2(row.conjugacy_class_size)
    )
    assert row.markov_degree_lower_bound > row.threshold_copy_count
    assert row.degree_lower_bound_over_sqrt_class_size > 0.5
    assert not row.generic_polynomial_compiler_is_polynomial
    assert not row.structured_direct_compiler_known
    assert not row.actual_family_circuit_lower_bound_proved


def test_report_keeps_structured_dilation_escape_open(tmp_path):
    report = build_hidden_involution_threshold_compiler_report(
        finite_specs=((3, 1, 1), (3, 1, 2)),
        scaling_n_values=(16, 32, 64),
    )
    assert report.theorem.theorem_verified
    assert report.theorem.efficient_average_projector_block_encoding_formalized
    assert report.theorem.generic_polynomial_degree_exponential_at_threshold
    assert report.theorem.central_dilation_compression_proved
    assert not report.theorem.central_class_sum_measurement_is_helstrom
    assert not report.theorem.structured_threshold_sign_compiler_constructed
    assert not report.theorem.actual_family_circuit_lower_bound_proved
    assert not report.claim_gate["information_theoretic_sample_threshold_new_to_literature"]
    assert not report.claim_gate["coherent_central_dilation_compiler_ruled_out"]
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_hidden_involution_threshold_compiler_report(
        tmp_path / "compiler.json",
        finite_specs=((3, 1, 1), (3, 1, 2)),
        scaling_n_values=(16, 32),
    )
    assert payload["status"] == (
        "generic-threshold-compilers-blocked-structured-sign-route-open"
    )
