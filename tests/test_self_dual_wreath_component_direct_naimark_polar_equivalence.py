from functools import lru_cache

import numpy as np
import pytest

from self_dual_wreath_component_direct_naimark_polar_equivalence import (
    _random_leaf_system,
    audit_direct_naimark_polar_equivalence,
    coherent_gauge_countercontrol,
    direct_component_naimark_normal_form,
    run_component_direct_naimark_polar_equivalence,
    state_weighted_approximation_boundary,
)


@lru_cache(maxsize=1)
def _report():
    return run_component_direct_naimark_polar_equivalence()


@pytest.mark.parametrize(
    ("seed", "physical", "blocks", "fiber"),
    [
        (4301, 9, (2, 3, 4, 5), 4),
        (4313, 10, (2, 2, 3), 5),
        (4327, 8, (1,) * 12, 3),
    ],
)
def test_direct_component_naimark_is_restricted_orientation_polar(
    seed: int,
    physical: int,
    blocks: tuple[int, ...],
    fiber: int,
) -> None:
    leaves, common = _random_leaf_system(
        seed,
        physical_dimension=physical,
        block_dimensions=blocks,
        common_dimension=fiber,
    )
    row = audit_direct_naimark_polar_equivalence(
        f"CONTROL-{seed}",
        leaves,
        common,
    )

    assert row.exact_direct_naimark_polar_equivalence_verified
    assert row.direct_restricted_polar_factorization_residual <= 1e-8
    assert row.restricted_polar_recovery_residual <= 1e-8
    assert row.component_effect_sum_identity_residual <= 1e-8
    assert row.coefficient_projection_normal_form_residual <= 1e-8


def test_coordinate_measurement_realizes_all_component_effects_at_once() -> None:
    leaves, common = _random_leaf_system(
        4337,
        physical_dimension=7,
        block_dimensions=(2, 2, 3, 4),
        common_dimension=3,
    )
    _, _, direct, components, effects = direct_component_naimark_normal_form(
        leaves,
        common,
    )
    np.testing.assert_allclose(
        direct.conj().T @ direct,
        np.eye(common.shape[1]),
        atol=1e-9,
    )
    np.testing.assert_allclose(
        sum(effects, np.zeros_like(effects[0])),
        np.eye(common.shape[1]),
        atol=1e-9,
    )
    for component, effect in zip(components, effects):
        np.testing.assert_allclose(
            component.conj().T @ component,
            effect,
            atol=1e-9,
        )


def test_identical_component_effects_do_not_fix_coherent_output_gauge() -> None:
    control = coherent_gauge_countercontrol()

    assert control.identical_povm_effects
    assert control.maximum_coordinate_probability_residual == pytest.approx(0)
    assert control.coherent_output_overlap == pytest.approx(0, abs=1e-12)
    assert control.coherent_output_trace_distance == pytest.approx(1)
    assert control.coherent_map_operator_distance == pytest.approx(np.sqrt(2))
    assert not control.coherent_dilation_determined_by_effects_alone


def test_frobenius_scalarization_requires_actual_input_flatness() -> None:
    boundary = state_weighted_approximation_boundary(128)

    assert boundary.flatness_weighted_bound_verified
    assert boundary.normalized_frobenius_error == pytest.approx(1 / 128)
    assert boundary.uniform_input_flatness == pytest.approx(1)
    assert boundary.uniform_input_exact_error == pytest.approx(1 / 128)
    assert boundary.concentrated_input_flatness == pytest.approx(128)
    assert boundary.concentrated_input_exact_error == pytest.approx(1)
    assert not boundary.uniform_error_controls_concentrated_input_without_flatness


def test_report_relocates_the_gate_without_promoting_an_algorithm() -> None:
    report = _report()

    assert report.headline_metrics[
        "direct_naimark_restricted_polar_equivalence_theorem_count"
    ] == 1
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate[
        "direct_component_naimark_equals_restricted_orientation_polar"
    ]
    assert report.claim_gate["coordinate_measurement_realizes_component_povm"]
    assert not report.claim_gate[
        "independent_effect_square_root_synthesis_is_fundamental_gate"
    ]
    assert not report.claim_gate["component_effects_determine_coherent_output_gauge"]
    assert not report.claim_gate[
        "uniform_frobenius_scalarization_controls_arbitrary_inputs"
    ]
    assert report.claim_gate[
        "natural_all_level_state_weighted_component_trim_proved"
    ]
    assert not report.claim_gate[
        "coherent_component_threshold_support_select_compiled"
    ]
    assert not report.claim_gate["natural_restricted_orientation_polar_compiled"]
    assert not report.claim_gate["label_sensitive_information_gain_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
