"""Central-support theorem counts come from their checks, and registry writes are recorded."""
import dataclasses
import json

import research_registry as registry
import self_dual_wreath_central_support_rank_bridge as module


def test_relative_rank_count_follows_its_check(monkeypatch):
    failed = dataclasses.replace(
        module.collision_free_s4_rank_bridge_control(),
        exact_rank_bridge_inequality_verified=False,
    )
    monkeypatch.setattr(module, "collision_free_s4_rank_bridge_control", lambda: failed)
    metrics = module.run_central_support_rank_bridge().headline_metrics
    assert metrics["relative_rank_central_support_bridge_theorem_count"] == 0


def test_registry_write_is_recorded(tmp_path, monkeypatch):
    results = tmp_path / "experiment_results.json"
    results.write_text("[]")
    monkeypatch.setattr(registry, "EXPERIMENT_RESULTS_PATH", results)
    module.write_central_support_rank_bridge_report(
        tmp_path / "report.json",
        registry_result_id="RESULT-TEST-CENTRAL",
    )
    records = json.loads(results.read_text())
    assert [record["id"] for record in records] == ["RESULT-TEST-CENTRAL"]
    assert records[0]["metrics"]["polynomial_rank_degree_reduction_theorem_count"] == 1


def test_registry_write_can_be_disabled(tmp_path, monkeypatch):
    results = tmp_path / "experiment_results.json"
    results.write_text("[]")
    monkeypatch.setattr(registry, "EXPERIMENT_RESULTS_PATH", results)
    module.write_central_support_rank_bridge_report(tmp_path / "report.json", write_registry=False)
    assert json.loads(results.read_text()) == []
