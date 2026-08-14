import math

import pytest

from self_dual_wreath_alternating_entropy_transfer_reduction import (
    audit_alternating_entropy_reduction,
    run_alternating_entropy_transfer_reduction,
    sublog_equivalence_control,
    write_alternating_entropy_transfer_reduction_report,
)


def test_exact_finite_chain_reduces_to_coarse_alternating_base() -> None:
    for n in range(2, 6):
        row = audit_alternating_entropy_reduction(n)
        assert row.full_minus_base_residual < 1e-8
        assert row.base_minus_alternating_residual < 1e-8
        assert row.conditional_information_bound_verified
        assert row.exact_entropy_reduction_verified


def test_three_bit_term_is_asymptotically_negligible_on_log_scale() -> None:
    differences = []
    for n in (10**6, 10**12, 10**24):
        difference, verified = sublog_equivalence_control(
            n,
            math.sqrt(math.log2(n)),
            3.0,
        )
        assert verified
        differences.append(difference)

    assert differences == sorted(differences, reverse=True)
    assert differences[-1] < differences[0]


def test_sublog_control_rejects_invalid_three_bit_entropy() -> None:
    with pytest.raises(ValueError):
        sublog_equivalence_control(100, 1.0, 3.1)


def test_report_moves_rank_gate_without_claiming_alternating_entropy_bound(tmp_path) -> None:
    report = run_alternating_entropy_transfer_reduction()

    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate[
        "full_sublog_entropy_equivalent_to_base_sublog_entropy_proved"
    ]
    assert report.claim_gate[
        "base_law_is_coarse_alternating_tetrahedral_law_proved"
    ]
    assert not report.claim_gate[
        "orientation_entropy_asymptotic_control_required_for_rank"
    ]
    assert not report.claim_gate[
        "coarse_alternating_total_correlation_sublogarithmic_proved"
    ]
    assert not report.claim_gate["physical_rank_profile_mixes_proved"]
    assert not report.claim_gate["algorithm_claim_allowed"]
    assert not report.claim_gate["speedup_claim_allowed"]

    path = tmp_path / "alternating-entropy.json"
    payload = write_alternating_entropy_transfer_reduction_report(path)
    assert path.exists()
    assert payload["headline_metrics"]["new_quantum_algorithm_count"] == 0
