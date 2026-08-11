import itertools
from functools import lru_cache

import pytest

from self_dual_wreath_nonsystematic_mod_four_no_go import (
    audit_mod_four_marked_presentation,
    audit_mod_four_structure,
    mod_four_all_depth_certificate,
    mod_four_code,
    run_nonsystematic_mod_four_no_go,
)


@lru_cache(maxsize=1)
def _report():
    return run_nonsystematic_mod_four_no_go()


@pytest.mark.parametrize("width", (6, 10, 14))
def test_mod_four_family_has_exact_quarter_cube_density(width):
    code = mod_four_code(width)
    assert len(code) == 2 ** (width - 2)
    assert all(sum(row) % 4 == 0 for row in code)
    assert not any(sum(row) == 2 for row in code)


@pytest.mark.parametrize("width", (6, 10, 14))
def test_mod_four_family_is_nonsystematic_and_star_free(width):
    control = audit_mod_four_structure(width)
    assert control.minimum_distance == 2
    assert control.all_coordinate_pairs_have_explicit_distance_two_witnesses
    assert control.minimum_separating_coordinate_count == width - 1
    assert not control.has_dimension_sized_information_set
    assert not control.contains_weight_two_row
    assert not control.spanning_distance_two_star_exists
    assert control.exact_control_verified


@pytest.mark.parametrize("width", (6, 10, 14))
def test_ordered_codeword_presentation_is_exactly_cyclic_order_four(width):
    control = audit_mod_four_structure(width)
    assert control.incidence_lattice_index == 4
    assert control.smith_invariants == (1,) * (width - 1) + (4,)
    assert control.codeword_presentation_remaining_generator_count == 1
    assert any(
        len(relation) == 4
        for relation in control.codeword_presentation_residual_relations
    )
    assert all(
        len(relation) % 4 == 0
        for relation in control.codeword_presentation_residual_relations
    )
    assert control.exact_cyclic_order_four_presentation_verified


def test_every_coordinate_pair_has_a_weight_four_collision_at_base_width():
    width = 6
    code = set(mod_four_code(width))
    for first, second in itertools.combinations(range(width), 2):
        common = sorted(set(range(width)) - {first, second})[:3]
        left = tuple(int(i in {*common, first}) for i in range(width))
        right = tuple(int(i in {*common, second}) for i in range(width))
        assert left in code
        assert right in code
        assert [i for i, pair in enumerate(zip(left, right)) if pair[0] != pair[1]] == [
            first,
            second,
        ]


def test_full_marked_control_retains_four_torsion_but_loses_surface_exponent():
    control = audit_mod_four_marked_presentation(6)
    assert control.support_difference_peeling_stalls_on_full_core
    assert control.remaining_generator_count == 6
    assert control.fourth_power_relation_present
    assert control.solution_exponent_upper_bound == 5.0
    assert "surface-genus-2" in control.solution_exponent_certificate_source
    assert control.true_pressure_margin_lower_bound > 2.0
    assert control.residual_target_word
    assert control.exact_control_verified


def test_all_depth_surface_certificate_closes_only_bounded_index_family():
    theorem = mod_four_all_depth_certificate()
    assert theorem.arbitrary_admissible_width
    assert theorem.universal_mod_four_family_no_go_verified
    assert theorem.symmetric_group_solution_exponent_upper_bound == 5.0
    report = _report()
    assert report.headline_metrics["all_depth_mod_four_family_construction_count"] == 1
    assert report.headline_metrics["all_depth_mod_four_no_go_theorem_count"] == 1
    assert report.headline_metrics["structural_control_failure_count"] == 0
    assert report.headline_metrics["marked_control_failure_count"] == 0
    assert report.claim_gate["explicit_star_free_nonsystematic_family_constructed"]
    assert not report.claim_gate["bounded_smith_torsion_escape_survives"]
    assert not report.claim_gate["mod_four_actual_pressure_survives"]
    assert not report.claim_gate["growing_smith_invariant_family_constructed"]
    assert not report.claim_gate["all_nonsystematic_stopping_codes_controlled"]
    assert not report.claim_gate["speedup_claim_allowed"]
