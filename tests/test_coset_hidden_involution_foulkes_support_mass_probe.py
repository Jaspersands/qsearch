from fractions import Fraction

import pytest

from coset_hidden_involution_foulkes_support_mass_probe import (
    build_foulkes_support_mass_report,
    foulkes_cycle_counts,
    foulkes_multiplicities,
    foulkes_power_sum_coefficients,
    foulkes_support_mass_record,
    partition_centralizer_order,
    write_foulkes_support_mass_report,
)


def test_power_sum_compiler_produces_exact_wreath_cycle_counts():
    coefficients = foulkes_power_sum_coefficients(2, 3)
    counts = foulkes_cycle_counts(2, 3)
    assert all(isinstance(value, Fraction) for value in coefficients.values())
    assert sum(counts.values()) == 72
    assert set(coefficients) == set(counts)
    assert partition_centralizer_order((3, 2, 1)) == 6
    with pytest.raises(ValueError, match="block_size"):
        foulkes_power_sum_coefficients(2, 1)


@pytest.mark.parametrize(("block_count", "block_size"), ((2, 3), (4, 3), (3, 4)))
def test_exact_foulkes_multiplicity_dimension_and_hook_controls(
    block_count, block_size
):
    record = foulkes_support_mass_record(block_count, block_size)
    multiplicities = foulkes_multiplicities(block_count, block_size)
    assert record.induced_dimension_identity_verified
    assert record.hook_constituent_violation_count == 0
    assert multiplicities[(block_count * block_size,)] == 1
    assert 0 < record.support_sector_count < record.partition_count
    assert 0.0 < record.exact_trimmed_candidate_support_probability < 1.0
    assert record.exact_all_register_support_mass_log2 < -20
    assert not record.asymptotic_support_deficit_classified
    assert not record.coherent_support_projector_compiled


def test_fixed_block_three_support_mass_rises_but_tensor_event_stays_small():
    rows = [foulkes_support_mass_record(a, 3) for a in (2, 4, 6)]
    assert [row.support_sector_count for row in rows] == [2, 12, 67]
    assert rows[0].exact_trimmed_candidate_support_probability > rows[1].exact_trimmed_candidate_support_probability
    assert rows[1].exact_trimmed_candidate_support_probability < rows[2].exact_trimmed_candidate_support_probability
    assert all(row.all_register_support_mass_below_one_in_a_million for row in rows)
    assert all(row.support_deficit_times_copy_count > 8 for row in rows)


def test_report_keeps_asymptotic_and_coherent_projector_gates_closed(tmp_path):
    report = build_foulkes_support_mass_report(specs=((2, 3), (4, 3), (3, 4)))
    assert report.theorem.theorem_verified
    assert report.theorem.exact_power_sum_compiler_verified
    assert report.theorem.exact_finite_support_mass_verified
    assert not report.theorem.asymptotic_support_deficit_classified
    assert not report.theorem.coherent_foulkes_support_projector_compiled
    assert not report.theorem.post_support_deflation_frame_norm_bounded
    assert report.claim_gate["exact_foulkes_support_mass_compiler_verified"]
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_foulkes_support_mass_report(
        tmp_path / "foulkes-support.json",
        specs=((2, 3), (4, 3)),
    )
    assert payload["status"] == (
        "exact-foulkes-support-mass-probe-asymptotic-deficit-open"
    )
    assert payload["headline_metrics"]["new_quantum_algorithm_count"] == 0
