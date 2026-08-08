import numpy as np
import pytest

from self_dual_wreath_component_povm_spectral_trim import (
    NATURAL_FINAL_FIBER_ASPECT_LOWER,
    audit_component_povm_spectral_trim,
    natural_component_trim_scaling_record,
    run_component_povm_spectral_trim,
)


def _jointly_low_sector_povm() -> tuple[np.ndarray, ...]:
    effects = []
    for index in range(8):
        diagonal = np.zeros(4)
        diagonal[0] = 1 / 8
        if index < 3:
            diagonal[index + 1] = 1.0
        effects.append(np.diag(diagonal).astype(complex))
    return tuple(effects)


def test_spectral_trim_creates_subpovm_with_retained_edge() -> None:
    epsilon = 1e-5
    first = np.diag([epsilon, 0.5, 0.0]).astype(complex)
    second = np.diag([0.0, 0.5, epsilon]).astype(complex)
    third = np.eye(3, dtype=complex) - first - second
    row = audit_component_povm_spectral_trim(
        "TINY-EDGE",
        (first, second, third),
        np.eye(3, dtype=complex) / 3,
        truncation_threshold=0.1,
        coordinate_block_dimensions=(2, 2, 3),
    )

    assert row.minimum_retained_positive_eigenvalue >= 0.1
    assert row.exact_failure_probability == pytest.approx(2 * epsilon / 3)
    assert row.ideal_to_trimmed_mean_square_error == pytest.approx(
        row.exact_failure_probability
    )
    assert row.subpovm_completeness_violation == 0
    assert row.exact_trim_theorem_verified is True


def test_flat_and_concentrated_inputs_have_different_trim_loss() -> None:
    effects = _jointly_low_sector_povm()
    uniform = audit_component_povm_spectral_trim(
        "UNIFORM",
        effects,
        np.eye(4, dtype=complex) / 4,
        truncation_threshold=0.2,
    )
    concentrated = audit_component_povm_spectral_trim(
        "CONCENTRATED",
        effects,
        np.diag([1.0, 0.0, 0.0, 0.0]).astype(complex),
        truncation_threshold=0.2,
    )

    assert uniform.incoming_state_flatness == pytest.approx(1.0)
    assert uniform.exact_failure_probability == pytest.approx(0.25)
    assert concentrated.incoming_state_flatness == pytest.approx(4.0)
    assert concentrated.exact_failure_probability == pytest.approx(1.0)
    assert uniform.exact_trim_theorem_verified is True
    assert concentrated.exact_trim_theorem_verified is True


def test_natural_constant_aspect_turns_polynomial_flatness_into_polynomial_cutoff() -> None:
    row = natural_component_trim_scaling_record(
        48,
        flatness_polynomial_degree=2,
        target_failure_probability=0.1,
    )

    expected = 0.1 * float(NATURAL_FINAL_FIBER_ASPECT_LOWER) / 48**2
    assert row.retained_component_eigenvalue_threshold == pytest.approx(expected)
    assert row.failure_upper_bound == pytest.approx(0.1)
    assert row.inverse_polynomial_threshold_certified_conditionally is True
    assert row.natural_incoming_flatness_proved is False
    assert row.coherent_component_threshold_filter_compiled is False


def test_report_rejects_hard_edge_necessity_without_claiming_compiler() -> None:
    report = run_component_povm_spectral_trim()

    assert report.status == (
        "component-hard-edge-bypassed-conditionally-state-flatness-open"
    )
    assert report.claim_gate[
        "component_positive_edge_required_for_average_state_dilation"
    ] is False
    assert report.claim_gate["state_weighted_component_spectral_trim_proved"] is True
    assert report.claim_gate[
        "polynomial_natural_incoming_common_fiber_flatness_proved"
    ] is False
    assert report.claim_gate["coherent_component_support_select_compiled"] is False
    assert report.claim_gate["speedup_claim_allowed"] is False
    assert report.headline_metrics[
        "concentrated_state_unit_failure_countercontrol_count"
    ] == 1


def test_non_povm_is_rejected() -> None:
    with pytest.raises(ValueError, match="do not form"):
        audit_component_povm_spectral_trim(
            "NOT-POVM",
            (np.eye(2, dtype=complex) / 2,),
            np.eye(2, dtype=complex) / 2,
            truncation_threshold=0.1,
        )
