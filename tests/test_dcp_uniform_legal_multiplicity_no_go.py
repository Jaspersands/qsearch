import math

import numpy as np
import pytest

from dcp_uniform_legal_multiplicity_no_go import (
    falling_factorial,
    limiting_multiplicity_law,
    multiplicity_tail_certificate,
    run_uniform_legal_multiplicity_no_go,
    uniform_legal_multiplicity_no_go_theorem,
    uniform_legal_tail_bound,
)


def test_falling_factorial_and_tail_bound_are_exact() -> None:
    counts = np.asarray([0, 1, 1, 2, 3, 5, 0, 4], dtype=np.int64)
    tail, bound, residual = uniform_legal_tail_bound(counts, 4, 3)
    assert falling_factorial(4, 3) == 24
    assert tail == pytest.approx(2 / 6)
    assert bound >= tail
    assert residual == 0


def test_requested_polynomial_tail_uses_one_fixed_moment() -> None:
    certificate = multiplicity_tail_certificate(0.5, 7.0)
    assert certificate.selected_fixed_factorial_order == 16
    assert certificate.exponent_margin > 0
    assert certificate.superpolynomial_tail_certificate_valid


def test_uniform_legal_and_planted_limits_are_distinct() -> None:
    rows = limiting_multiplicity_law(30)
    legal_mass = sum(row.uniform_legal_probability for row in rows)
    planted_mass = sum(row.planted_probability for row in rows)
    assert legal_mass == pytest.approx(1.0, abs=1e-12)
    assert planted_mass == pytest.approx(1.0, abs=1e-12)
    assert rows[0].uniform_legal_probability == pytest.approx(
        math.exp(-1) / (1 - math.exp(-1))
    )
    assert rows[0].planted_probability == pytest.approx(math.exp(-1))
    assert rows[2].planted_to_uniform_legal_ratio == pytest.approx(
        3 * (1 - math.exp(-1))
    )


def test_invalid_tail_contract_is_rejected() -> None:
    with pytest.raises(ValueError, match="nonempty"):
        uniform_legal_tail_bound([], 2, 1)
    with pytest.raises(ValueError, match="threshold"):
        uniform_legal_tail_bound([1, 2], 1, 2)
    with pytest.raises(ValueError, match="legal"):
        uniform_legal_tail_bound([0, 0], 2, 1)
    with pytest.raises(ValueError, match="positive"):
        multiplicity_tail_certificate(0.0, 2.0)


def test_theorem_keeps_general_algorithms_out_of_scope() -> None:
    theorem = uniform_legal_multiplicity_no_go_theorem()
    assert theorem.theorem_verified
    assert theorem.high_multiplicity_uniform_legal_subfamily_eliminated
    assert not theorem.general_representation_dissection_eliminated
    assert not theorem.polynomial_subset_sum_solver_eliminated
    assert "internal" in theorem.scope_limit


def test_report_falsifies_only_multiplicity_shortcut() -> None:
    report = run_uniform_legal_multiplicity_no_go()
    assert report.headline_metrics["uniform_legal_multiplicity_no_go_theorem_count"] == 1
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert not report.claim_gate[
        "polynomial_fiber_multiplicity_representation_collapse_survives"
    ]
    assert report.claim_gate["internal_representation_dissection_survives"]
    assert report.claim_gate["joint_low_high_preconditioner_survives"]
    assert not report.claim_gate["speedup_claim_allowed"]
