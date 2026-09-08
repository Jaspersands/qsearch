import json
import math
from fractions import Fraction

import pytest

from coset_hidden_involution_signed_tensor_access import (
    minimum_signed_tensor_degree, signed_tensor_degree_control, signed_tensor_source_mass_bound,
    write_signed_tensor_access_report, DEFAULT_EXPERIMENT_ID,
)
from coset_hidden_involution_paired_tower_missing_label_boundary import bipartitions
from coset_hidden_involution_natural_recoupling_boundary import hyperoctahedral_irrep_dimension


@pytest.mark.parametrize("rank", range(2, 9))
def test_exact_degree_formula_and_dimensions_cover_entire_bratteli_graph(rank):
    row = signed_tensor_degree_control(rank)
    assert row["minimum_degree_formula_matches_all_types"]
    assert row["tensor_dimension_identities_exact"]
    assert row["central_parity_identities_exact"]
    assert row["source_bound_respected"]


def test_alpha_tail_costs_two_moves_not_one():
    assert minimum_signed_tensor_degree((2, 1), (2, 1, 1)) == 6
    assert minimum_signed_tensor_degree((1, 1, 1, 1), ()) == 6
    assert minimum_signed_tensor_degree((), (2, 2)) == 4
    assert minimum_signed_tensor_degree((4,), ()) == 0
    with pytest.raises(ValueError):
        minimum_signed_tensor_degree((1, 2), ())


@pytest.mark.parametrize("rank", range(2, 9))
def test_source_bound_respects_exact_even_parity_and_every_budget(rank):
    pairs = [pair for pair in bipartitions(rank) if sum(pair[1]) % 2 == 0]
    denominator = 2**(rank - 1) * math.factorial(rank)
    for budget in range(2 * rank + 1):
        mass = Fraction(sum(hyperoctahedral_irrep_dimension(*pair)**2 for pair in pairs
                            if minimum_signed_tensor_degree(*pair) <= budget), denominator)
        assert mass <= signed_tensor_source_mass_bound(rank, budget)
    assert signed_tensor_source_mass_bound(rank, 0) == Fraction(1, denominator)
    assert signed_tensor_source_mass_bound(rank, 2 * rank) == 1


def test_faithful_range_fails_asymptotically_not_in_small_controls():
    assert Fraction(signed_tensor_degree_control(6)["degree_at_most_rank_exact_source_mass"]) > Fraction(97, 100)
    assert signed_tensor_source_mass_bound(128, 128) < Fraction(1, 2**37)
    assert signed_tensor_source_mass_bound(256, 256) < Fraction(1, 2**105)
    with pytest.raises(ValueError):
        signed_tensor_source_mass_bound(1, 1)


def test_report_retains_quotient_and_alternative_embedding_escape(tmp_path):
    path = tmp_path / "access.json"
    payload = write_signed_tensor_access_report(path, write_registry=False)
    assert json.loads(path.read_text()) == payload
    assert payload["claim_gate"]["exact_finite_controls_passed"]
    assert not payload["claim_gate"]["all_signed_tensor_algorithms_ruled_out"]
    assert not payload["claim_gate"]["speedup_claim_allowed"]


def test_clean_registry_runner_records_scoped_negative(tmp_path, monkeypatch):
    from experiment_runner import run_experiment, supported_experiment_ids
    from research_registry import initialize_seed_registry, load_negative_results, validate_registry
    monkeypatch.chdir(tmp_path)
    initialize_seed_registry(overwrite=True)
    assert DEFAULT_EXPERIMENT_ID in supported_experiment_ids()
    result = run_experiment(DEFAULT_EXPERIMENT_ID)
    assert result.status == "completed"
    negative = next(item for item in load_negative_results()
                    if item["id"] == "FAITHFUL-SIGNED-TENSOR-DIAGRAM-RANGE-MISSES-TYPICAL-SOURCE")
    assert "nonfaithful quotient" in negative["lesson"]
    assert validate_registry()["valid"]
