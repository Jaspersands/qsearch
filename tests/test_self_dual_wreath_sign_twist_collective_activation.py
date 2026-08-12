import json
import math
from fractions import Fraction

from self_dual_wreath_sign_twist_collective_activation import (
    audit_sign_twist_activation,
    closed_form_sign_twist_collective_signal,
    exact_sign_twist_collective_signal,
    run_sign_twist_collective_activation,
    sign_twist_source_law_record,
    sign_twist_source_partitions,
    transpose_partition,
    write_sign_twist_collective_activation_report,
)


def test_transpose_partition_is_an_involution() -> None:
    for partition in ((6,), (4, 2), (3, 2, 1), (2, 2, 1, 1), (1,) * 6):
        assert transpose_partition(transpose_partition(partition)) == partition


def test_source_family_is_pairwise_nonadjacent_and_twist_creates_two_edges() -> None:
    for n in range(6, 65):
        control = audit_sign_twist_activation(n)
        assert control.pairwise_nonadjacent_sources_verified
        assert control.source_young_edge_count == 0
        assert control.exactly_two_sign_twisted_edges_verified
        assert control.effective_young_edge_count == 2
        assert control.effective_edge_standard_multiplicities == (1, 1)


def test_exact_signal_has_closed_polynomial_form() -> None:
    for n in (6, 7, 8, 10, 16, 32, 64, 128):
        assert exact_sign_twist_collective_signal(n) == (
            closed_form_sign_twist_collective_signal(n)
        )
        expected = Fraction(
            432,
            n**6 * (n - 1) ** 3 * (n - 3) ** 3 * (n - 5) ** 3,
        )
        assert exact_sign_twist_collective_signal(n) == expected


def test_s6_direct_overlap_agrees_with_all_n_formula() -> None:
    control = audit_sign_twist_activation(6, direct_finite_validation=True)
    assert control.finite_direct_control_verified
    assert control.direct_to_exact_residual is not None
    assert control.direct_to_exact_residual < 1e-12
    assert control.exact_collective_signal == "1/364500"


def test_source_law_obstruction_is_factorial_despite_polynomial_signal() -> None:
    rows = [sign_twist_source_law_record(n) for n in (8, 16, 32, 64)]
    assert all(row.inverse_polynomial_conditional_signal for row in rows)
    assert all(not row.inverse_polynomial_source_admission for row in rows)
    assert all(not row.natural_plancherel_algorithm_obtained for row in rows)
    assert all(
        row.postselection_amplitude_amplification_query_lower_log2 > 0
        for row in rows
    )
    assert rows[-1].postselection_amplitude_amplification_query_lower_log2 > (
        10 * math.log2(rows[-1].n)
    )


def test_family_requires_non_degenerate_degree() -> None:
    try:
        sign_twist_source_partitions(5)
    except ValueError:
        pass
    else:
        raise AssertionError("n<6 must be rejected")


def test_report_keeps_source_admission_and_algorithm_gates_closed() -> None:
    report = run_sign_twist_collective_activation()
    assert report.theorem.theorem_verified
    assert report.headline_metrics["structural_control_failure_count"] == 0
    assert report.headline_metrics["conditional_signal_polynomial_exponent"] == 15
    assert report.claim_gate["inverse_polynomial_conditional_point_energy_proved"]
    assert not report.claim_gate["inverse_polynomial_natural_source_probability_proved"]
    assert not report.claim_gate["high_plancherel_weight_analogue_found"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_report_writer_emits_valid_json(tmp_path) -> None:
    path = tmp_path / "sign_twist_activation.json"
    payload = write_sign_twist_collective_activation_report(path)
    parsed = json.loads(path.read_text())
    assert parsed["status"] == payload["status"]
    assert parsed["headline_metrics"] == payload["headline_metrics"]
