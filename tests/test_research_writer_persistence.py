from pathlib import Path

from character_moment_obstruction import write_character_moment_obstruction_report
from dcp_symmetric_relation_lift import write_symmetric_relation_lift_audit
from research_registry import (initialize_seed_registry, load_experiment_results, load_negative_results,
    load_scaling_runs, validate_registry)


def test_disabled_registry_writes_do_not_create_registry_files(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    write_character_moment_obstruction_report(families=["legendre_symbol"], n_values=[6], write_registry=False)
    write_symmetric_relation_lift_audit(write_registry=False)
    assert not Path("research/registry").exists()


def test_enabled_writes_are_idempotent_and_honor_result_identifiers(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    initialize_seed_registry(overwrite=True)
    path = Path("research/reductions/custom_symmetric_lift.json")
    for _ in range(2):
        moment = write_character_moment_obstruction_report(families=["legendre_symbol"], n_values=[6])
        lift = write_symmetric_relation_lift_audit(path=path, registry_result_id="RESULT-CUSTOM-SYMMETRIC-LIFT")
    rows = [row for row in load_scaling_runs() if row["id"] == moment["id"]]
    assert rows == [moment]
    rows = [row for row in load_experiment_results() if row["id"] == "RESULT-CUSTOM-SYMMETRIC-LIFT"]
    assert len(rows) == 1 and rows[0]["metrics"] == lift["headline_metrics"]
    assert rows[0]["created_at"] == lift["created_at"]
    assert rows[0]["artifacts"] == {"dcp_symmetric_relation_lift": str(path)}
    assert rows[0]["metrics"]["proved_polynomial_relation_solver_count"] == 0
    for identifier in ("NEG-DCP-ARBITRARY-RELATION-INCOMPATIBLE-WITH-MATCHING", "NEG-DCP-RELATION-LIFT-AS-SOLVER-CONSTRUCTION"):
        records = [row for row in load_negative_results() if row["id"] == identifier]
        assert len(records) == 1
        assert records[0]["evidence"] == lift["headline_metrics"]
        assert records[0]["source"] == str(path)
    assert validate_registry()["valid"]
