import math

import numpy as np
import pytest

from dcp_per_target_stratum_obstruction import (
    audit_multiplicity_orbit,
    audit_stratum_filter,
    multiplicity_stratum_correlation,
    poisson_stratum_limit,
    run_per_target_stratum_obstruction,
)


COUNTS = np.asarray((1, 2, 1, 3, 2, 1, 3, 1), dtype=np.int64)


def test_root_of_unity_gram_seed_is_psd_with_unit_diagonal() -> None:
    support, _, correlation = multiplicity_stratum_correlation(COUNTS, 2)
    assert len(support) == len(COUNTS)
    assert np.min(np.linalg.eigvalsh(correlation)) >= -1e-10
    assert np.max(np.abs(np.diag(correlation) - 1)) <= 1e-12


def test_cleaned_filter_is_exactly_zero_on_rejected_stratum() -> None:
    control = audit_stratum_filter("EXACT-J2", COUNTS, 2)
    assert control.stratum_filter_verified
    assert control.maximum_rejected_target_success <= 1e-10
    assert control.minimum_accepted_target_success == pytest.approx(1.0)
    assert control.maximum_accepted_target_success == pytest.approx(1.0)
    assert not control.per_target_success_proved


def test_signed_unit_orbit_preserves_target_multiplicity() -> None:
    labels = [3, 7, 12, 21, 34, 55, 61, 9]
    n_bits = 6
    modulus = 1 << n_bits
    from dcp_subset_sum_qtt_contraction_search import exact_cyclic_subset_sum_counts

    counts = exact_cyclic_subset_sum_counts(labels, modulus)
    target = int(np.flatnonzero(counts > 0)[0])
    control = audit_multiplicity_orbit(
        n_bits,
        labels,
        target,
        transformation_count=20,
        seed=71,
    )
    assert control.signed_unit_orbit_preserves_multiplicity
    assert not control.orbit_crosses_multiplicity_strata
    assert control.transformed_multiplicity_minimum == control.target_multiplicity
    assert control.transformed_multiplicity_maximum == control.target_multiplicity


@pytest.mark.parametrize("multiplicity", [1, 2, 3, 4])
def test_poisson_stratum_has_positive_mass_and_constant_decoder_limit(
    multiplicity: int,
) -> None:
    row = poisson_stratum_limit(multiplicity)
    assert row.limiting_uniform_legal_target_mass == pytest.approx(
        1 / (math.factorial(multiplicity) * (math.e - 1))
    )
    assert row.limiting_decoder_success_probability > 0
    assert row.per_target_gap_persists_asymptotically


def test_report_blocks_only_the_per_target_proof_strategy() -> None:
    report = run_per_target_stratum_obstruction()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.theorem.information_theoretic_counterexample_proved
    assert not report.theorem.efficient_stratum_filter_measurement_constructed
    assert not report.claim_gate["average_measurement_to_witness_reduction_invalidated"]
    assert not report.claim_gate["average_to_per_target_upgrade_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
