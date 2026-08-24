import json
import math
from fractions import Fraction

import numpy as np

from self_dual_wreath_branch_character_equivariant_multiplier_normal_form import (
    _multiplier_representations,
    audit_equivariant_multiplier,
    audit_multiplicity_freedom,
    branch_fourier_multiplier,
    regular_master_freedom_scaling,
    run_equivariant_multiplier_normal_form,
    tensor_field_covariance_residual,
    tensor_product_multiplicities,
    write_equivariant_multiplier_normal_form_report,
)
from self_dual_wreath_orientation_fourier_reduction import (
    _source_representation_rows,
)


S3_LABELS = (((3,), (2, 1)),)
S4_LABELS = (((4,), (3, 1)),)


def test_branch_polar_field_is_exactly_conjugation_covariant() -> None:
    group = tuple(_source_representation_rows((3,)))
    maximum = max(
        tensor_field_covariance_residual(S3_LABELS, conjugator, element)
        for conjugator in group
        for element in group
    )
    assert maximum < 1e-10


def test_fourier_multiplier_is_an_exact_intertwiner() -> None:
    target = (2, 1)
    multiplier = branch_fourier_multiplier(target, S3_LABELS)
    for permutation in _source_representation_rows((3,)):
        input_representation, output_representation = _multiplier_representations(
            target,
            S3_LABELS,
            permutation,
        )
        assert np.linalg.norm(
            output_representation @ multiplier
            - multiplier @ input_representation,
            ord=2,
        ) < 1e-10


def test_class_twirl_reconstructs_the_multiplier() -> None:
    for target, labels, name in (
        ((2, 1), S3_LABELS, "s3"),
        ((3, 1), S4_LABELS, "s4"),
    ):
        control = audit_equivariant_multiplier(name, target, labels)
        assert control.exact_equivariant_normal_form_verified
        assert control.maximum_class_twirl_residual < 1e-10
        assert control.class_reconstruction_residual < 1e-10


def test_character_multiplicities_have_the_correct_total_dimension() -> None:
    cases = (
        ((2, 1), S3_LABELS),
        ((3, 1), S4_LABELS),
        (
            (2, 2),
            (((4,), (3, 1)), ((2, 2), (2, 1, 1))),
        ),
    )
    for target, labels in cases:
        multiplicities = tensor_product_multiplicities(target, labels)
        assert all(value >= 0 for value in multiplicities.values())
        control = audit_multiplicity_freedom("control", target, labels)
        assert control.exact_multiplicity_decomposition_verified
        assert control.decomposition_dimension_sum == control.representation_dimension


def test_reduced_multiplicity_algebra_obeys_cauchy_pressure() -> None:
    control = audit_multiplicity_freedom(
        "two-pair",
        (2, 2),
        (((4,), (3, 1)), ((2, 2), (2, 1, 1))),
    )
    lower_bound = Fraction(control.cauchy_lower_bound)
    assert control.reduced_square_multiplicity_sum >= lower_bound
    assert control.reduced_rectangular_parameter_count == (
        control.branch_dimension * control.reduced_square_multiplicity_sum
    )
    assert math.isclose(
        control.class_lcu_coefficient_one_norm,
        math.sqrt(control.group_order),
    )
    assert not control.covariance_alone_determines_reduced_maps


def test_regular_master_multiplicity_pressure_is_exact_and_grows() -> None:
    rows = [regular_master_freedom_scaling(n) for n in (8, 16, 32, 64)]
    assert all(row.regular_master_cauchy_bound_is_exact for row in rows)
    assert all(not row.covariance_and_gap_imply_polynomial_compiler for row in rows)
    assert all(row.explicit_reduced_map_factorization_open for row in rows)
    assert all(
        right.reduced_rectangular_parameter_count_log2
        > left.reduced_rectangular_parameter_count_log2
        for left, right in zip(rows, rows[1:])
    )


def test_report_closes_normal_form_but_not_explicit_compiler() -> None:
    report = run_equivariant_multiplier_normal_form()
    assert report.theorem.theorem_verified
    assert report.claim_gate["branch_field_conjugation_covariance_proved"]
    assert report.claim_gate["equivariant_multiplier_intertwiner_form_proved"]
    assert report.claim_gate["class_twirl_reconstruction_proved"]
    assert report.claim_gate[
        "direct_class_lcu_normalization_bypass_rejected"
    ]
    assert not report.claim_gate[
        "covariance_and_near_isometry_sufficient_for_compilation"
    ]
    assert not report.claim_gate["specific_quadrant_reduced_maps_factorized"]
    assert not report.claim_gate["direct_equivariant_multiplier_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_writer_emits_live_artifact(tmp_path) -> None:
    path = tmp_path / "equivariant-multiplier.json"
    payload = write_equivariant_multiplier_normal_form_report(path)
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert loaded["status"] == payload["status"]
    assert loaded["headline_metrics"][
        "equivariant_multiplier_normal_form_theorem_count"
    ] == 1
