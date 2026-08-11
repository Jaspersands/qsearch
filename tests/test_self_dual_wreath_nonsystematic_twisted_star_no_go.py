import itertools
from functools import lru_cache

from self_dual_wreath_nonsystematic_twisted_star_no_go import (
    audit_twisted_star,
    distance_two_difference_supports,
    minimum_separating_coordinate_count,
    run_nonsystematic_twisted_star_no_go,
    twisted_star_code,
    twisted_star_recursive_extension,
)


@lru_cache(maxsize=1)
def _report():
    return run_nonsystematic_twisted_star_no_go()


def _minimum_distance(code):
    return min(
        sum(a != b for a, b in zip(left, right))
        for left, right in itertools.combinations(code, 2)
    )


def test_twisted_star_is_an_all_depth_codimension_two_code_family():
    for width in range(4, 11):
        code = twisted_star_code(width)
        assert len(code) == 2 ** (width - 2)
        assert len(set(code)) == len(code)
        assert all(len(row) == width for row in code)
        assert all(sum(row) % 2 == 0 for row in code)
        assert _minimum_distance(code) == 2
        if width > 4:
            assert twisted_star_recursive_extension(
                twisted_star_code(width - 1)
            ) == code


def test_every_dimension_sized_projection_has_a_distance_two_collision():
    for width in range(4, 11):
        code = twisted_star_code(width)
        expected_pairs = tuple(itertools.combinations(range(width), 2))
        assert distance_two_difference_supports(code) == expected_pairs
        assert minimum_separating_coordinate_count(code) == width - 1


def test_full_marked_presentations_collapse_to_fixed_rank_surface_systems():
    for width in range(4, 8):
        control = audit_twisted_star(width)
        assert not control.has_dimension_sized_information_set
        assert control.zero_and_all_star_rows_present
        assert control.support_difference_peeling_stalls_on_full_core
        assert control.remaining_generator_count == 6
        if width >= 5:
            assert control.residual_involution_relation_present
        assert control.solution_exponent_upper_bound == 5.0
        assert "surface-genus-2" in control.solution_exponent_certificate_source
        assert control.true_pressure_margin_lower_bound > 2.0
        assert control.residual_target_word
        assert control.exact_control_verified


def test_report_kills_only_the_explicit_nonsystematic_family():
    report = _report()
    theorem = report.all_depth_certificate
    assert theorem.arbitrary_width
    assert theorem.universal_twisted_star_family_no_go_verified
    assert theorem.symmetric_group_solution_exponent_upper_bound == 5.0
    assert theorem.uniform_pressure_margin_lower_bound == 2.0
    assert report.headline_metrics[
        "all_depth_nonsystematic_family_construction_count"
    ] == 1
    assert report.headline_metrics[
        "all_depth_twisted_star_no_go_theorem_count"
    ] == 1
    assert report.headline_metrics["control_failure_count"] == 0
    assert report.claim_gate[
        "explicit_nonsystematic_constant_codimension_family_constructed"
    ]
    assert not report.claim_gate["twisted_star_information_set_escape_survives"]
    assert not report.claim_gate["twisted_star_actual_pressure_survives"]
    assert report.claim_gate["all_twisted_star_widths_controlled"]
    assert not report.claim_gate["all_nonsystematic_stopping_codes_controlled"]
    assert not report.claim_gate["speedup_claim_allowed"]
