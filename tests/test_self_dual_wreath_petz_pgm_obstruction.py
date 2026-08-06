import math

import pytest

from self_dual_wreath_petz_pgm_obstruction import (
    petz_pgm_obstruction_record,
    run_petz_pgm_obstruction,
)


def test_generic_environment_is_hypothesis_dimension_not_qubit_count() -> None:
    record = petz_pgm_obstruction_record(32)
    hypotheses = math.factorial(32)

    assert record.generic_environment_dimension_decimal == str(hypotheses)
    assert record.complementary_state_rank_decimal == str(hypotheses)
    assert record.hidden_label_qubit_count == math.ceil(math.log2(hypotheses))
    assert record.log2_generic_environment_sqrt_charge == pytest.approx(
        math.log2(hypotheses) / 2
    )
    assert record.generic_environment_charge_superpolynomial


def test_generic_obstruction_does_not_claim_covariant_lower_bound() -> None:
    report = run_petz_pgm_obstruction()

    assert report.headline_metrics["generic_pgm_to_petz_reduction_count"] == 1
    assert report.headline_metrics["complementary_rank_bypass_failure_count"] == 1
    assert report.claim_gate["generic_petz_pgm_baseline_mapped"]
    assert not report.claim_gate["specific_covariant_pgm_lower_bound_proved"]
    assert report.claim_gate[
        "algebraic_covariance_compressed_factorization_proved"
    ]
    assert not report.claim_gate[
        "polynomial_covariance_compressed_stinespring_circuit_proved"
    ]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_invalid_degree_is_rejected() -> None:
    with pytest.raises(ValueError, match="at least two"):
        petz_pgm_obstruction_record(1)
