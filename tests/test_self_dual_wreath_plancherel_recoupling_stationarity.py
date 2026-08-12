import json
from fractions import Fraction

from representation_obstruction import integer_partitions
from self_dual_wreath_plancherel_recoupling_stationarity import (
    audit_plancherel_recoupling_stationarity,
    dimension_weighted_kronecker_transition,
    plancherel_weights,
    recouple_against_plancherel,
    recoupling_stationarity_scaling_record,
    run_plancherel_recoupling_stationarity,
    write_plancherel_recoupling_stationarity_report,
)


def test_every_dimension_weighted_transition_row_normalizes() -> None:
    for n in range(2, 9):
        partitions = tuple(integer_partitions(n))
        for left in partitions:
            for right in partitions:
                assert sum(
                    dimension_weighted_kronecker_transition(left, right).values()
                ) == 1


def test_fixed_input_plus_plancherel_is_exactly_plancherel() -> None:
    for n in range(2, 10):
        expected = plancherel_weights(n)
        for fixed in integer_partitions(n):
            assert recouple_against_plancherel(fixed) == expected


def test_exact_regular_multiplicity_controls_pass() -> None:
    for n in range(2, 11):
        row = audit_plancherel_recoupling_stationarity(n)
        assert row.exact_plancherel_stationarity_verified
        assert row.transition_row_normalization_residual == "0"
        assert row.maximum_stationarity_residual == "0"
        assert row.maximum_regular_multiplicity_identity_residual == 0
        assert row.maximum_output_dependence_on_fixed_input_residual == "0"
        assert row.maximum_two_step_stationarity_residual == "0"


def test_plancherel_weights_are_exact_probabilities() -> None:
    for n in range(2, 12):
        weights = plancherel_weights(n)
        assert sum(weights.values(), Fraction()) == 1
        assert all(weight > 0 for weight in weights.values())


def test_scaling_scope_keeps_shared_coherence_open() -> None:
    row = recoupling_stationarity_scaling_record(1024)
    assert row.disjoint_tree_root_law == "exact Plancherel"
    assert row.disjoint_tree_root_independence
    assert not row.independent_recoupling_focuses_rare_channels
    assert not row.shared_source_coherence_ruled_out
    assert not row.coherent_racah_transform_dequantized


def test_report_preserves_classical_label_scope() -> None:
    report = run_plancherel_recoupling_stationarity()
    assert report.theorem.theorem_verified
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["dimension_weighted_recoupling_preserves_plancherel"]
    assert not report.claim_gate["shared_source_recoupling_dequantized"]
    assert not report.claim_gate["coherent_racah_transform_dequantized"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_report_writer_emits_valid_json(tmp_path) -> None:
    path = tmp_path / "plancherel_recoupling_stationarity.json"
    payload = write_plancherel_recoupling_stationarity_report(path)
    parsed = json.loads(path.read_text())
    assert parsed["status"] == payload["status"]
    assert parsed["headline_metrics"] == payload["headline_metrics"]
