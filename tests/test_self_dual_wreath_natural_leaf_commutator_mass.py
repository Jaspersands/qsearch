import math

import pytest

from self_dual_wreath_natural_leaf_commutator_mass import (
    audit_projection_commutator_formula,
    natural_leaf_commutator_scaling_record,
    projection_commutator_norm_from_cosine,
    run_natural_leaf_commutator_mass,
)


@pytest.mark.parametrize("dimension", [2, 3, 5, 11, 31])
def test_principal_cosine_gives_exact_projection_commutator_norm(
    dimension: int,
) -> None:
    row = audit_projection_commutator_formula("CONTROL", dimension)

    expected = math.sqrt(1 - dimension**-2) / dimension
    assert row.predicted_principal_cosine == pytest.approx(1 / dimension)
    assert row.predicted_commutator_norm == pytest.approx(expected)
    assert row.observed_commutator_norm == pytest.approx(expected)
    assert row.commutator_norm_residual < 1e-12
    assert row.exact_projection_commutator_formula_verified is True


def test_natural_standard_carrier_witness_is_inverse_polynomial() -> None:
    row = natural_leaf_commutator_scaling_record(48)

    assert row.standard_carrier_partition == (47, 1)
    assert row.standard_carrier_dimension == 47
    assert row.commutator_operator_norm_lower_bound > 1 / 48
    assert row.commutator_operator_norm_lower_bound < 1 / 47
    assert row.inverse_commutator_scale < 48
    assert row.density_one_balanced_pair_noncommutativity_proved is True
    assert row.global_distinct_transfer_proved is True
    assert row.canonical_component_commutator_transfer_proved is False


def test_endpoint_cosines_have_zero_commutator() -> None:
    assert projection_commutator_norm_from_cosine(0.0) == 0.0
    assert projection_commutator_norm_from_cosine(1.0) == 0.0


def test_report_keeps_leaf_to_component_transfer_gate_closed() -> None:
    report = run_natural_leaf_commutator_mass()

    assert report.status == (
        "density-one-natural-leaf-noncommutativity-proved-component-transfer-open"
    )
    assert report.claim_gate[
        "natural_orientation_leaf_algebra_noncommutative_on_density_one_pairs"
    ] is True
    assert report.claim_gate[
        "natural_leaf_commutator_has_inverse_polynomial_norm_witness"
    ] is True
    assert report.claim_gate[
        "natural_canonical_component_effect_algebra_noncommutative_on_positive_mass"
    ] is False
    assert report.claim_gate["leaf_to_component_commutator_transfer_proved"] is False
    assert report.claim_gate["speedup_claim_allowed"] is False
    assert report.headline_metrics[
        "natural_density_one_balanced_leaf_pair_noncommutativity_theorem_count"
    ] == 1
