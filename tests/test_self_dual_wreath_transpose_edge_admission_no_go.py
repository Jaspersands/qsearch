import json

from self_dual_wreath_transpose_edge_admission_no_go import (
    audit_transpose_edge_admission,
    run_transpose_edge_admission_no_go,
    transpose_edge_admission_scaling_record,
    transpose_young_neighbors,
    write_transpose_edge_admission_no_go_report,
)
from representation_obstruction import integer_partitions


def test_transpose_edge_probability_obeys_degree_atom_bound() -> None:
    for n in range(4, 17):
        row = audit_transpose_edge_admission(n)
        assert row.exact_finite_admission_bound_verified
        assert row.probability_bound_violation == 0
        assert row.maximum_degree_bound_violation == 0
        assert row.distinct_transpose_edge_probability <= (
            row.degree_times_max_atom_upper_bound
        )


def test_transpose_edge_relation_is_symmetric() -> None:
    for n in range(4, 11):
        partitions = tuple(integer_partitions(n))
        neighbors = {
            partition: set(transpose_young_neighbors(partition, partitions))
            for partition in partitions
        }
        for left in partitions:
            for right in partitions:
                assert (right in neighbors[left]) == (left in neighbors[right])


def test_finite_probability_is_nonzero_but_not_promoted_as_scaling() -> None:
    rows = [audit_transpose_edge_admission(n) for n in range(6, 13)]
    assert all(row.distinct_transpose_edge_probability > 0 for row in rows)
    assert all(row.ordered_active_pair_count > 0 for row in rows)


def test_scaling_scope_leaves_collective_recoupling_open() -> None:
    row = transpose_edge_admission_scaling_record(1024)
    assert not row.inverse_polynomial_source_local_transpose_edge_admission
    assert not row.collective_intermediate_recoupling_ruled_out
    assert row.polynomial_pool_probability_upper_asymptotic.endswith(
        "exp(-Theta(sqrt(n)))"
    )


def test_report_preserves_source_local_scope() -> None:
    report = run_transpose_edge_admission_no_go()
    assert report.theorem.theorem_verified
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["source_local_transpose_edge_probability_bound_proved"]
    assert not report.claim_gate["collective_intermediate_recoupling_ruled_out"]
    assert not report.claim_gate["typical_collective_energy_bound_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_report_writer_emits_valid_json(tmp_path) -> None:
    path = tmp_path / "transpose_edge_admission_no_go.json"
    payload = write_transpose_edge_admission_no_go_report(path)
    parsed = json.loads(path.read_text())
    assert parsed["status"] == payload["status"]
    assert parsed["headline_metrics"] == payload["headline_metrics"]
