from pathlib import Path
import sys

import pytest
from sympy import Matrix, eye

sys.path.insert(0, str(Path(__file__).resolve().parent))
from elliptic_fields import (
    frobenius_power, normalization_plan, supersingular_trace_classes, twist_countercontrol,
)


@pytest.mark.parametrize("p", [5, 7, 11, 13, 37])
@pytest.mark.parametrize("degree", [1, 2, 3, 4])
def test_all_possible_trace_classes_have_same_positive_scalar(p, degree):
    for trace in supersingular_trace_classes(p, degree):
        assert frobenius_power(p, degree, trace, 12) == (p**(6*degree), 0)
    assert normalization_plan(p, degree, []) ["fixed_scalar_mod_8"] == 1


def test_actual_twists_rule_out_separate_scalar_field_shortcut():
    result = twist_countercontrol()
    assert [r["points_over_F121"] for r in result["curves"]] == [122, 111]
    assert all(r["hasse_invariant_zero"] for r in result["curves"])
    assert not result["relative_degree_6_defines_maps_between_fixed_endpoints"]
    assert result["relative_degree_12_matches_endpoint_frobenius"]
    assert not result["isogeny_computed"]


def test_repeated_characteristic_polynomial_is_not_actual_minimal_polynomial():
    q, trace = 121, 22
    companion = Matrix([[0, -q], [1, trace]])
    assert companion**12 != q**6*eye(2)
    assert frobenius_power(11, 2, trace, 12) == (q**6, 0)


def test_auxiliary_fields_are_separate_and_match_the_paid_base():
    result = normalization_plan(11, 2, [(3, 1), (5, 1), (7, 2)])
    assert result["fixed_base_degree"] == 24
    assert [r["absolute_auxiliary_degree"] for r in result["auxiliary_fields"]] == [48, 96, 1008]
    assert result["sum_separate_auxiliary_degrees"] == 1152
    assert not result["field_embeddings_constructed"]
    assert not result["unknown_isogeny_constructed"]
    assert not result["common_field_for_unknown_phi_given_as_input"]


@pytest.mark.parametrize("args", [(2, 2, []), (3, 2, []), (9, 2, []), (11, 0, []),
    (11, 2, [(11, 1)]), (11, 2, [(3, 3)]), (11, 2, [(3, 1), (3, 1)])])
def test_invalid_field_plans_rejected(args):
    with pytest.raises(ValueError):
        normalization_plan(*args)


def test_ordinary_trace_not_promoted_to_supersingular_field_promise():
    with pytest.raises(ValueError, match="supersingular"):
        frobenius_power(11, 1, 2, 12)
