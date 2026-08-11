import math

import numpy as np
import pytest

from dcp_source_weighted_inversion_tradeoff import (
    run_dcp_source_weighted_inversion_tradeoff,
    scaling_record,
    source_weighted_inversion_metrics,
    trimmed_inversion_metrics,
    write_dcp_source_weighted_inversion_tradeoff,
)


def test_source_weighted_mean_and_rms_identities_are_exact():
    counts = np.asarray([0, 1, 2, 5, 0, 3, 1], dtype=np.int64)
    row = source_weighted_inversion_metrics("arbitrary", counts)
    assert row.normalizations_verified
    assert row.mean_pgm_duality_residual < 1e-12
    assert row.rms_support_identity_residual < 1e-12
    assert row.mean_reciprocal_amplitude**2 == pytest.approx(
        len(counts) * row.pgm_success_probability
    )
    assert row.rms_reciprocal_amplitude**2 == pytest.approx(5.0)


def test_uniform_collision_fibers_have_perfect_pgm_but_large_inverse_scale():
    row = source_weighted_inversion_metrics("uniform", np.full(8, 2))
    assert row.pgm_success_probability == pytest.approx(1.0)
    assert row.mean_reciprocal_amplitude == pytest.approx(math.sqrt(8))
    assert row.rms_reciprocal_amplitude == pytest.approx(math.sqrt(8))


def test_trimming_identity_and_multiplicity_bound():
    counts = np.asarray([0, 1, 2, 5, 0, 3, 1], dtype=np.int64)
    row = trimmed_inversion_metrics("trim", counts, (1, 2, 5, 6))
    assert row.exact_conditional_rms_squared == pytest.approx(
        row.accepted_residue_count / row.accepted_source_mass
    )
    assert (
        row.conditional_rms_reciprocal_amplitude
        + 1e-12
        >= row.multiplicity_bound_rms_lower_bound
    )
    assert row.lower_bound_residual < 1e-12
    assert not row.branchwise_polytime_inversion_certified


def test_trimming_rejects_illegal_residues():
    with pytest.raises(ValueError, match="legal"):
        trimmed_inversion_metrics("bad", (1, 0, 2), (1,))


def test_asymptotic_tradeoff_is_exponential_despite_inverse_polynomial_information():
    row = scaling_record(512, pgm_success_lower_bound_power=4)
    assert row.mean_inverse_lower_bound_log2 > 200
    assert row.quenched_rms_inverse_log2_asymptotic > 250
    assert row.trimmed_rms_lower_bound_log2 > 200
    assert not row.polynomial_branchwise_cost_possible


def test_report_keeps_global_collective_route_open(tmp_path):
    report = run_dcp_source_weighted_inversion_tradeoff()
    assert report.theorem.theorem_verified
    assert report.theorem.mean_pgm_duality_proved
    assert report.theorem.rms_support_identity_proved
    assert report.theorem.trimmed_multiplicity_bound_proved
    assert not report.theorem.source_weighting_rescues_direct_inversion
    assert not report.theorem.global_source_aware_coisometry_ruled_out
    assert not report.theorem.general_quantum_lower_bound_proved
    assert not report.claim_gate["standard_variable_time_rms_rescues_direct_encoding"]
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_dcp_source_weighted_inversion_tradeoff(tmp_path / "report.json")
    assert payload["status"] == "dcp-source-weighted-inversion-tradeoff-active"
