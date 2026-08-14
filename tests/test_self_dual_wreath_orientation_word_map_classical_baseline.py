import itertools
import math

import pytest

from self_dual_wreath_compressed_orientation_racah_cumulant_probe import (
    compile_orientation_racah_channel,
)
from self_dual_wreath_orientation_word_map_classical_baseline import (
    audit_exact_s5_walsh_identity,
    classical_cost_record,
    conditional_mutual_information_continuity_bound_bits,
    exact_normalized_word_map_walsh_means,
    normalized_tv_error_bound,
    normalized_word_map_walsh_observables,
    run_orientation_word_map_classical_baseline,
    simultaneous_hoeffding_sample_count,
)


def test_shared_walsh_observables_are_bounded_and_exact_on_s3() -> None:
    base = ((2, 1),) * 6
    exact = exact_normalized_word_map_walsh_means(3, base)
    group = tuple(itertools.permutations(range(3)))
    sums = [0.0] * 8
    for g, h, k in itertools.product(group, repeat=3):
        values = normalized_word_map_walsh_observables(base, g, h, k)
        assert max(abs(value) for value in values) <= 1.0
        for index, value in enumerate(values):
            sums[index] += value
    empirical = tuple(value / len(group) ** 3 for value in sums)
    assert empirical == pytest.approx(tuple(map(float, exact)), abs=1e-15)


def test_exact_s5_character_walsh_means_match_compiled_racah_amplitudes() -> None:
    control = audit_exact_s5_walsh_identity()
    assert control.all_exact_means_nonnegative
    assert control.maximum_exact_to_compiled_residual < 1e-12
    assert control.exact_walsh_identity_verified


def test_concentration_and_normalization_bounds_have_declared_constants() -> None:
    count = simultaneous_hoeffding_sample_count(0.02, 0.05)
    assert count == math.ceil(2.0 * math.log(16.0 / 0.05) / 0.02**2)
    assert normalized_tv_error_bound(0.4, 0.0025) == pytest.approx(0.05)
    with pytest.raises(ValueError):
        normalized_tv_error_bound(0.4, 0.05)
    assert conditional_mutual_information_continuity_bound_bits(0.0) == 0.0
    assert conditional_mutual_information_continuity_bound_bits(0.01) > 0.0


def test_finite_cost_record_counts_sign_problem_without_claiming_separation() -> None:
    control = compile_orientation_racah_channel(
        "S6-WORD-MAP-TEST", ((3, 1, 1, 1),) * 6
    )
    record = classical_cost_record(control)
    assert record.physical_mass_formula_residual < 1e-12
    assert record.random_word_sample_updates_all_syndromes
    assert record.log10_word_samples_sufficient_for_fixed_tv > 20
    assert record.log10_word_samples_sufficient_to_resolve_cmi > 20
    assert record.polynomial_classical_runtime_proved is False
    assert record.classical_lower_bound_proved is False
    assert record.quantum_advantage_proved is False


def test_report_keeps_dequantization_and_speedup_gates_closed() -> None:
    report = run_orientation_word_map_classical_baseline()
    assert report.exact_control.exact_walsh_identity_verified
    assert report.claim_gate["direct_classical_estimator_available"] is True
    assert report.claim_gate["exact_character_average_case_efficiency_proved"] is False
    assert report.claim_gate["importance_sampling_ruled_out"] is False
    assert report.claim_gate["classical_lower_bound_proved"] is False
    assert report.claim_gate["speedup_claim_allowed"] is False
