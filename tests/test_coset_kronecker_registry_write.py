"""Registry writes from the Kronecker marginal writer are recorded, not dropped."""
import json

import pytest

import research_registry as registry
from coset_kronecker_marginal_conservation import write_kronecker_marginal_conservation_report


def test_registry_write_is_recorded(tmp_path, monkeypatch):
    results = tmp_path / "experiment_results.json"
    results.write_text("[]")
    monkeypatch.setattr(registry, "EXPERIMENT_RESULTS_PATH", results)
    payload = write_kronecker_marginal_conservation_report(
        tmp_path / "report.json",
        registry_result_id="RESULT-TEST-KRONECKER",
    )
    records = json.loads(results.read_text())
    assert [record["id"] for record in records] == ["RESULT-TEST-KRONECKER"]
    assert records[0]["experiment_id"] == "EXP-COSET-KRONECKER-MARGINAL-CONSERVATION"
    assert records[0]["metrics"] == payload["headline_metrics"]


def test_registry_write_can_be_disabled(tmp_path, monkeypatch):
    results = tmp_path / "experiment_results.json"
    results.write_text("[]")
    monkeypatch.setattr(registry, "EXPERIMENT_RESULTS_PATH", results)
    write_kronecker_marginal_conservation_report(tmp_path / "report.json", write_registry=False)
    assert json.loads(results.read_text()) == []


def test_misspelled_registry_argument_is_rejected(tmp_path):
    with pytest.raises(TypeError):
        write_kronecker_marginal_conservation_report(tmp_path / "report.json", write_regsitry=True)
