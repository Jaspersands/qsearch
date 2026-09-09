from dataclasses import asdict, replace
import numpy as np
import pytest

from dequantization_checks import _budget_class
from phase_state_workbench import (
    ExactPhaseEvaluator,
    PhaseFamilySpec,
    ShiftAttackResult,
    apply_hidden_shift,
    build_query_lower_bound_probes,
    build_query_model_assessments,
    chosen_query_exhaustive_correlation_attack,
    f2_quadratic_algebraic_reconstruction_attack,
    fp2_quadratic_algebraic_reconstruction_attack,
    full_table_group_correlation_attack,
    generate_cyclic_phase_family,
    polynomial_value_recovery,
    quadratic_value_query_controls,
    sample_limited_correlation_attack,
)


class PointOnlyValues:
    """Forbid array conversion, slices, iteration and unbudgeted value reads."""

    def __init__(self, values, budget, allowed=None):
        self.values = values
        self.budget = budget
        self.allowed = allowed
        self.calls = []

    def __array__(self, *args, **kwargs):
        raise AssertionError("hidden full-table conversion")

    def __iter__(self):
        raise AssertionError("hidden full-table iteration")

    def __getitem__(self, index):
        assert isinstance(index, int)
        assert len(self.calls) < self.budget
        assert self.allowed is None or index in self.allowed
        self.calls.append(index)
        return self.values[index]


@pytest.mark.parametrize("n_bits", [3, 4, 5, 6])
def test_boolean_reconstruction_all_shifts_uses_only_origin_and_basis(n_bits):
    spec, values = generate_cyclic_phase_family("bent_quadratic_f2", n_bits)
    positions = [0] + [1 << j for j in range(n_bits)]
    for shift in range(spec.domain_size):
        f = PointOnlyValues(values, n_bits + 1, positions)
        g = PointOnlyValues(apply_hidden_shift(spec, values, shift), n_bits + 1, positions)
        result = f2_quadratic_algebraic_reconstruction_attack(spec, f, g, shift)
        assert result.success
        assert result.recovered_shift == shift
        assert f.calls == positions == g.calls
        assert result.sample_count == result.resources.total_value_queries == 2 * (n_bits + 1)
        assert polynomial_value_recovery(result)


@pytest.mark.parametrize("n_bits", [3, 4, 5, 6])
def test_fp2_reconstruction_all_shifts_uses_six_values(n_bits):
    spec, values = generate_cyclic_phase_family("fp2_quadratic_form", n_bits)
    positions = [0, spec.modulus, 1]
    for shift in range(spec.domain_size):
        f = PointOnlyValues(values, 3, positions)
        g = PointOnlyValues(apply_hidden_shift(spec, values, shift), 3, positions)
        result = fp2_quadratic_algebraic_reconstruction_attack(spec, f, g, shift)
        assert result.success
        assert result.recovered_shift == shift
        assert f.calls == positions == g.calls
        assert result.sample_count == result.resources.total_value_queries == 6


@pytest.mark.parametrize("family,attack", [
    ("bent_quadratic_f2", f2_quadratic_algebraic_reconstruction_attack),
    ("fp2_quadratic_form", fp2_quadratic_algebraic_reconstruction_attack),
])
def test_ground_truth_only_scores_prediction(family, attack):
    spec, base = generate_cyclic_phase_family(family, 5)
    shifted = apply_hidden_shift(spec, base, 23)
    correct = attack(spec, base, shifted, 23)
    wrong_truth = attack(spec, base, shifted, 3)
    assert correct.success and not wrong_truth.success
    assert correct.recovered_shift == wrong_truth.recovered_shift == 23
    assert correct.resources == wrong_truth.resources


def test_odd_boolean_bit_requires_value_sign_not_uncontrolled_global_phase():
    spec, base = generate_cyclic_phase_family("bent_quadratic_f2", 5)
    first = apply_hidden_shift(spec, base, 3)
    second = apply_hidden_shift(spec, base, 19)
    assert np.array_equal(first, -second)
    # These are the same unobserved-global-phase state, but different VALUES.
    assert f2_quadratic_algebraic_reconstruction_attack(spec, base, first, 3).recovered_shift == 3
    assert f2_quadratic_algebraic_reconstruction_attack(spec, base, second, 19).recovered_shift == 19
    assert full_table_group_correlation_attack(spec, base, second, 19).success


def test_singular_fp2_form_does_not_claim_recovery_or_query_input():
    spec = PhaseFamilySpec("fp2_quadratic_form", "F_p^2", 9, 19**2, 19, {}, "singular control")
    forbidden = PointOnlyValues([], 0)
    result = fp2_quadratic_algebraic_reconstruction_attack(spec, forbidden, forbidden, 5)
    assert result.recovered_shift is None and not polynomial_value_recovery(result)


def test_named_quadratic_is_not_an_arbitrary_quadratic_or_masked_family():
    spec, base = generate_cyclic_phase_family("bent_quadratic_f2", 4)
    for family in ("masked_quadratic_f2", "unknown_quadratic", "mm_majority_bent_f2"):
        result = f2_quadratic_algebraic_reconstruction_attack(replace(spec, id=family), base, base, 0)
        assert result.recovered_shift is None


@pytest.mark.parametrize("bad_value", [complex("nan"), complex("inf"), 0j, 0.2j, 1.01])
def test_bad_numeric_phase_values_fail_closed(bad_value):
    spec, base = generate_cyclic_phase_family("fp2_quadratic_form", 4)
    base[0] = bad_value
    with pytest.raises(ValueError, match="phase value"):
        fp2_quadratic_algebraic_reconstruction_attack(spec, base, base, 0)


def test_numeric_precision_limit_cannot_be_bypassed_with_a_large_modulus():
    p = 2**61 - 1
    spec = PhaseFamilySpec("fp2_quadratic_form", "F_p^2", 122, p*p, p, {}, "exact access required")
    with pytest.raises(ValueError, match="ExactPhaseEvaluator"):
        fp2_quadratic_algebraic_reconstruction_attack(spec, PointOnlyValues([], 0), PointOnlyValues([], 0), 0)


def test_exact_phase_oracle_metadata_and_output_are_checked():
    spec, _ = generate_cyclic_phase_family("bent_quadratic_f2", 4)
    with pytest.raises(ValueError, match="mismatch"):
        wrong = ExactPhaseEvaluator(spec.domain_size, 3, lambda x: 0)
        f2_quadratic_algebraic_reconstruction_attack(spec, wrong, wrong, 0)
    with pytest.raises(ValueError, match="canonical residue"):
        wrong = ExactPhaseEvaluator(spec.domain_size, 2, lambda x: 2)
        f2_quadratic_algebraic_reconstruction_attack(spec, wrong, wrong, 0)


def test_large_domain_controls_do_not_allocate_tables():
    rows = quadratic_value_query_controls()
    assert len(rows) == 9
    assert max(row["domain_size"] for row in rows) >= 2**254
    for row in rows:
        assert row["attack"]["success"]
        assert row["attack"]["sample_count"] == row["expected_total_value_calls"]
        assert not row["attack"]["resources"]["full_table_materialized"]
        assert "exact integer residues" in row["attack"]["resources"]["precision_requirement"]


def test_random_baseline_reads_only_charged_samples_but_scans_the_shift_domain():
    spec, base = generate_cyclic_phase_family("bent_quadratic_f2", 5)
    g = apply_hidden_shift(spec, base, 19)
    f_access, g_access = PointOnlyValues(base, 8), PointOnlyValues(g, 8)
    result = sample_limited_correlation_attack(spec, f_access, g_access, 19, 8, 5)
    assert result.sample_count == len(f_access.calls) + len(g_access.calls) == 16
    assert result.resources.classical_time_class == "domain_exhaustive"
    assert not polynomial_value_recovery(result)


def test_exhaustive_queries_are_cached_and_separately_charged():
    spec, base = generate_cyclic_phase_family("bent_quadratic_f2", 5)
    f_access = PointOnlyValues(base, spec.domain_size)
    g_access = PointOnlyValues(apply_hidden_shift(spec, base, 19), 5)
    result = chosen_query_exhaustive_correlation_attack(spec, f_access, g_access, 19, 5, 5)
    assert len(set(f_access.calls)) == len(f_access.calls) == spec.domain_size
    assert len(g_access.calls) == 5
    assert result.sample_count == spec.domain_size + 5
    assert result.resources.full_table_materialized
    assert not polynomial_value_recovery(result)


@pytest.mark.parametrize("sample_count", [None, 1, 4])
def test_small_or_missing_query_count_is_not_polynomial_time_evidence(sample_count):
    spec, _ = generate_cyclic_phase_family("bent_quadratic_f2", 4)
    attack = ShiftAttackResult("unaccounted", 0, True, 1.0, "O(n)", "asserted", ["explicit_evaluator"], sample_count)
    assert not polynomial_value_recovery(attack)
    assert _budget_class(asdict(spec), asdict(attack)) == "unverified-resource-accounting"
    probe = next(p for p in build_query_lower_bound_probes(spec, [attack], 4) if p.model == "explicit_evaluator")
    assert probe.verdict == "unresolved-evaluator-model"
    assert probe.observed_query_budget is None


def test_probe_reports_the_winning_attack_budget_not_exhaustive_budget():
    spec, base = generate_cyclic_phase_family("fp2_quadratic_form", 5)
    g = apply_hidden_shift(spec, base, 13)
    algebraic = fp2_quadratic_algebraic_reconstruction_attack(spec, base, g, 13)
    exhaustive = chosen_query_exhaustive_correlation_attack(spec, base, g, 13, 8, 2)
    probe = next(p for p in build_query_lower_bound_probes(spec, [algebraic, exhaustive], 8) if p.model == "explicit_evaluator")
    assert probe.observed_query_budget == 6 != exhaustive.sample_count
    assert probe.baseline == algebraic.name
    assert "total" in probe.query_count_unit
    assert _budget_class(asdict(spec), asdict(algebraic)) == "polynomial-time-value-reconstruction-under-promise"
    damaged = replace(algebraic, sample_count=None)
    assert not polynomial_value_recovery(damaged)
    assert _budget_class(asdict(spec), asdict(damaged)) == "unverified-resource-accounting"


def test_finite_sample_recovery_is_not_promoted_to_efficient_dequantization():
    spec, base = generate_cyclic_phase_family("bent_quadratic_f2", 4)
    result = sample_limited_correlation_attack(spec, base, apply_hidden_shift(spec, base, 13), 13, 16, 3)
    assert result.success
    probe = next(p for p in build_query_lower_bound_probes(spec, [result], 16) if p.model == "random_sample")
    assert probe.verdict == "finite-random-sample-recovery-only"
    assert "exhaustive" in probe.notes


def test_missing_baseline_or_ambiguous_coherent_interface_is_not_survival():
    assert all(not item.survives_current_baselines for item in build_query_model_assessments([]))
    coherent = next(item for item in build_query_model_assessments([]) if item.model == "coherent_oracle")
    assert "VALUE" in coherent.notes
