from pathlib import Path
from dataclasses import replace

import numpy as np
import pytest

from coset_hidden_involution_high_mass_support_scan import separator_commutant_certificate

from coset_hidden_involution_source_weighted_support_portfolio import (
    BASELINE_HIGH_MASS_KEY,
    _branch_cache_path,
    source_ranked_targets,
    classify_scan,
)


def test_source_ranked_targets_exclude_baseline_and_follow_exact_mass() -> None:
    targets = source_ranked_targets(5)
    assert [rank for rank, _ in targets] == [2, 3, 4, 5, 6]
    assert all(
        (
            row.symmetric_partition,
            row.hyperoctahedral_partition,
            row.negative_hyperoctahedral_partition,
        )
        != BASELINE_HIGH_MASS_KEY
        for _, row in targets
    )
    masses = [row.natural_mass_probability for _, row in targets]
    assert masses == sorted(masses, reverse=True)
    assert abs(masses[0] - 0.008370535714285714) <= 1e-16
    assert abs(sum(masses) - 0.03764880952380952) <= 1e-16


def test_branch_checkpoints_are_partition_specific(tmp_path: Path) -> None:
    targets = source_ranked_targets(2)
    first = _branch_cache_path(targets[0][1], tmp_path)
    second = _branch_cache_path(targets[1][1], tmp_path)
    assert first != second
    assert first.parent == tmp_path
    assert second.parent == tmp_path
    assert first.suffix == ".npz"


def test_source_ranked_inputs_are_high_multiplicity_visible_mass_blocks() -> None:
    targets = source_ranked_targets(5)
    assert min(row.branching_multiplicity for _, row in targets) >= 21
    assert min(row.symmetric_irrep_dimension for _, row in targets) >= 68000
    assert sum(row.natural_mass_probability for _, row in targets) > 0.037


def test_failed_separator_search_is_not_a_counterexample():
    cert = separator_commutant_certificate([np.diag([0., 1.]), np.ones((2, 2))], search_trials=2)
    failed_search = replace(cert, scalar_common_commutant_numerically_certified=False)
    assert classify_scan(failed_search, exhaustive=True) == "inconclusive-not-a-counterexample"
    assert classify_scan(failed_search, exhaustive=False) == "inconclusive-not-a-counterexample"
    diagonal = separator_commutant_certificate([np.diag([0., 1.])], search_trials=0)
    assert classify_scan(diagonal, exhaustive=False) == "inconclusive-not-a-counterexample"
    assert classify_scan(diagonal, exhaustive=True) == "numerical-nonscalar-commutant-needs-exact-witness"


def test_impossible_target_counts_are_rejected():
    for count in (0, -1, 100000):
        with pytest.raises(ValueError):
            source_ranked_targets(count)


def test_source_portfolio_has_clean_registry_runner_dispatch(tmp_path, monkeypatch):
    import experiment_runner
    from research_registry import initialize_seed_registry, load_experiment_results, validate_registry
    from coset_hidden_involution_source_weighted_support_portfolio import DEFAULT_EXPERIMENT_ID

    monkeypatch.chdir(tmp_path)
    initialize_seed_registry(overwrite=True)
    calls = []

    def fake_writer(**kwargs):
        calls.append(kwargs)
        return {"summary": "dispatch-only fixture", "status": "inconclusive",
                "headline_metrics": {"source_ranked_unresolved_branch_count": 1}}

    monkeypatch.setattr(experiment_runner, "write_source_weighted_support_portfolio_report", fake_writer)
    assert DEFAULT_EXPERIMENT_ID in experiment_runner.supported_experiment_ids()
    result = experiment_runner.run_experiment(DEFAULT_EXPERIMENT_ID)
    assert len(calls) == 1
    assert calls[0]["registry_experiment_id"] == DEFAULT_EXPERIMENT_ID
    assert any(row["id"] == result.result_id for row in load_experiment_results())
    assert validate_registry()["valid"]
