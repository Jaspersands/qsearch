import json
from fractions import Fraction

import pytest

from coset_hidden_involution_natural_support_six_mass_audit import repeated_branch_census
from coset_hidden_involution_spectral_label_budget import (
    build_spectral_label_budget, necessary_label_rounds, source_label_mass_bound,
    spectral_label_capacity, write_spectral_label_budget_report,
    tensor_source_label_mass_bound,
    maximum_dimension_tensor_label_mass_bound,
)


def test_packing_includes_endpoints_and_tensor_labels():
    assert spectral_label_capacity(Fraction(1)) == 3
    assert spectral_label_capacity(Fraction(1), observables=2) == 9
    assert spectral_label_capacity(Fraction(3, 2)) == 2
    assert spectral_label_capacity(Fraction(3)) == 1
    for b in range(2, 80):
        assert spectral_label_capacity(Fraction(2, b - 1)) == b


@pytest.mark.parametrize("m", [2, 3, 4, 5])
def test_exact_mass_and_average_decoding_bounds_against_full_branch_census(m):
    denominator, _, _, repeated = repeated_branch_census(m)
    singleton_mass = Fraction(denominator - sum(r.natural_mass_numerator for r in repeated), denominator)
    for capacity in (0, 1, 2, 3, 8):
        small_mass = (singleton_mass if capacity else 0) + sum(
            (Fraction(r.natural_mass_numerator, denominator) for r in repeated
             if r.branching_multiplicity <= capacity), Fraction(0)
        )
        average_decoding = (singleton_mass if capacity else 0) + sum(
            (Fraction(r.natural_mass_numerator, denominator)
             * min(Fraction(1), Fraction(capacity, r.branching_multiplicity))
             for r in repeated), Fraction(0)
        )
        assert small_mass <= source_label_mass_bound(m, capacity)
        assert average_decoding <= source_label_mass_bound(m, capacity)


def test_fixed_count_polynomial_gap_mass_drops_but_adaptive_labels_not_excluded():
    bound = source_label_mass_bound(128, spectral_label_capacity(Fraction(1, 128**4), observables=4))
    assert bound < Fraction(1, 10**20)
    rounds = necessary_label_rounds(128, 2)
    assert rounds > 20
    assert source_label_mass_bound(128, 2**(rounds - 1)) < Fraction(1, 2)
    assert source_label_mass_bound(128, 2**rounds) >= Fraction(1, 2)
    assert source_label_mass_bound(128, 2**(128 * 128)) == 1


def test_report_uses_exact_bounds_and_does_not_claim_hsp_or_formal_lower_bound(tmp_path):
    path = tmp_path / "budget.json"
    report = write_spectral_label_budget_report(path, write_registry=False)
    assert json.loads(path.read_text()) == report
    assert len(report["scaling_records"]) == 54
    for row in report["scaling_records"]:
        bound = row["resolvable_branch_mass_upper_bound"]
        exact = Fraction(int(bound["numerator"]), int(bound["denominator"]))
        assert 0 < exact <= 1
        assert (exact < Fraction(1, 100)) == row["upper_bound_below_one_percent"]
    assert not report["claim_gate"]["all_quantum_measurements_ruled_out"]
    assert not report["claim_gate"]["speedup_claim_allowed"]
    assert not report["derivation"]["machine_checked_formal_proof"]


@pytest.mark.parametrize("gap", [0, 0.1, Fraction(-1)])
def test_invalid_gap_rejected(gap):
    with pytest.raises(ValueError):
        spectral_label_capacity(gap)


def test_invalid_grids_and_depth_inputs_rejected():
    with pytest.raises(ValueError):
        build_spectral_label_budget(half_degrees=())
    with pytest.raises(ValueError):
        build_spectral_label_budget(gap_powers=(-1,))
    with pytest.raises(ValueError):
        source_label_mass_bound(1, 4)
    with pytest.raises(ValueError):
        necessary_label_rounds(7, 1)


def test_clean_registry_runner_persists_scoped_negative_result(tmp_path, monkeypatch):
    from experiment_runner import run_experiment, supported_experiment_ids
    from research_registry import initialize_seed_registry, load_negative_results, load_experiment_results, validate_registry
    from coset_hidden_involution_spectral_label_budget import DEFAULT_EXPERIMENT_ID

    monkeypatch.chdir(tmp_path)
    initialize_seed_registry(overwrite=True)
    assert DEFAULT_EXPERIMENT_ID in supported_experiment_ids()
    result = run_experiment(DEFAULT_EXPERIMENT_ID)
    assert result.status == "completed"
    records = load_experiment_results()
    assert any(row["id"] == result.result_id for row in records)
    negative = next(row for row in load_negative_results()
                    if row["id"] == "TYPICAL-MULTIPLICITY-SINGLE-GAPPED-SEPARATOR-PACKING-OBSTRUCTION")
    assert "not an HSP lower bound" in negative["lesson"]
    assert validate_registry()["valid"]


def test_proof_tracker_marks_scope_and_keeps_compiler_blocked(tmp_path, monkeypatch):
    import proof_tracker
    path = tmp_path / "budget.json"
    write_spectral_label_budget_report(path, write_registry=False)
    monkeypatch.setattr(proof_tracker, "SPECTRAL_LABEL_BUDGET_PATH", path)
    monkeypatch.setattr(proof_tracker, "SOURCE_WEIGHTED_SUPPORT_PORTFOLIO_PATH", tmp_path / "missing.json")
    records = proof_tracker._spectral_label_budget_lemmas("CODE-COSET-COLLECTIVE")
    assert records[1].status == "derived-scoped-packing-obstruction-review-pending"
    assert records[2].status.startswith("blocked-")
    assert not any(row.status.startswith("proved-") for row in records)


def test_negative_result_audit_applies_only_to_linked_candidate():
    from dequantization_checks import findings_from_negative_results
    negative = {"id": "TYPICAL-MULTIPLICITY-SINGLE-GAPPED-SEPARATOR-PACKING-OBSTRUCTION",
                "applies_to": ["CODE-COSET-COLLECTIVE"], "reason_invalid": "packing under the specified source law"}
    findings = findings_from_negative_results(
        [{"id": "CODE-COSET-COLLECTIVE"}, {"id": "UNRELATED-CANDIDATE"}], [negative])
    assert len(findings) == 1
    assert findings[0].target_id == "CODE-COSET-COLLECTIVE"
    assert "not classical dequantization" in findings[0].required_action
    assert findings[0].blocks_speedup_claim


@pytest.mark.parametrize("n", [3, 4, 5, 6])
def test_tensor_source_bound_against_exact_kronecker_census(n):
    import math
    from itertools import product
    from symmetric_character import kronecker_coefficient
    from representation_obstruction import integer_partitions, hook_length_dimension
    partitions = integer_partitions(n)
    denominator = math.factorial(n)**2
    weights = []
    for left, right, target in product(partitions, repeat=3):
        g = kronecker_coefficient(left, right, target)
        numerator = g * hook_length_dimension(left) * hook_length_dimension(right) * hook_length_dimension(target)
        weights.append((g, Fraction(numerator, denominator)))
    assert sum(weight for _, weight in weights) == 1
    for capacity in (0, 1, 2, 4):
        mass = sum(weight for g, weight in weights if g <= capacity)
        assert mass <= tensor_source_label_mass_bound(n, capacity, source="plancherel")
        assert tensor_source_label_mass_bound(n, capacity, source="involution-coset") >= mass


def test_tensor_source_scope_is_explicit_and_scaling_obstructs_complete_labels():
    assert tensor_source_label_mass_bound(128, 128**8) < Fraction(1, 10**40)
    with pytest.raises(ValueError):
        tensor_source_label_mass_bound(16, 4, source="postselected")
    with pytest.raises(ValueError):
        tensor_source_label_mass_bound(16, 4, copies=1)
    report = build_spectral_label_budget(half_degrees=(16,))
    assert all(not row["conditional_eigenlabel_distribution_assumed_uniform"]
               for row in report["tensor_scaling_records"])


def test_maximum_dimension_source_bound_without_postselection_assumption():
    from symmetric_character import kronecker_coefficient
    from representation_obstruction import integer_partitions, hook_length_dimension
    for n in range(3, 9):
        partitions = integer_partitions(n)
        source = max(partitions, key=hook_length_dimension)
        dimension = hook_length_dimension(source)
        mass = sum(Fraction(hook_length_dimension(target) * g, dimension**2)
                   for target in partitions
                   if (g := kronecker_coefficient(source, source, target)) <= 2)
        assert mass <= maximum_dimension_tensor_label_mass_bound(n, 2)
    assert maximum_dimension_tensor_label_mass_bound(128, 128**8) < Fraction(1, 10**40)
