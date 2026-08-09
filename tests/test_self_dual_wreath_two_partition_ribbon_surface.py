from self_dual_wreath_two_partition_ribbon_surface import (
    audit_two_partition_ribbon_surface,
    exact_symmetric_group_solution_count,
    predicted_symmetric_group_solution_count,
    ribbon_surface_components,
    run_two_partition_ribbon_surface,
    symmetric_group_leading_solution_exponent,
)


def test_identical_partitions_form_spheres_with_free_vertex_loops():
    components, faces = ribbon_surface_components(
        (0, 0, 1, 1),
        (0, 0, 1, 1),
    )
    assert len(components) == 2
    assert len(faces) == 4
    assert all(row.orientable_genus == 0 for row in components)
    assert sum(row.free_rank_contribution for row in components) == 2
    assert symmetric_group_leading_solution_exponent(
        (0, 0, 1, 1),
        (0, 0, 1, 1),
    ) == 2


def test_EFBEBFB_pair_is_a_torus_with_two_free_generators():
    split = (0, 0, 1, 0, 1, 0, 1)
    differing = (0, 1, 1, 0, 1, 1, 1)
    control = audit_two_partition_ribbon_surface(
        "EFBEBFB",
        split,
        differing,
    )
    assert len(control.components) == 1
    component = control.components[0]
    assert component.orientable_genus == 1
    assert component.surface_vertex_count == 3
    assert control.free_group_rank == 2
    assert control.symmetric_group_leading_solution_exponent == 3
    assert control.exact_solution_count == 648
    assert control.predicted_solution_count == 648
    assert control.exact_finite_solution_formula_verified


def test_ribbon_formula_matches_exact_S3_counts_on_adversarial_pairs():
    pairs = (
        ((0, 1, 0, 1), (0, 0, 1, 1)),
        ((0, 1, 0, 1), (0, 1, 1, 0)),
        ((0, 1, 0, 1, 0), (0, 0, 1, 1, 0)),
    )
    for first, second in pairs:
        assert exact_symmetric_group_solution_count(
            first, second
        ) == predicted_symmetric_group_solution_count(first, second)


def test_report_keeps_the_multi_partition_entropy_problem_open():
    report = run_two_partition_ribbon_surface(maximum_position_count=6)
    assert report.headline_metrics["checked_partition_pair_count"] == 5_460
    assert report.headline_metrics["ribbon_topology_failure_count"] == 0
    assert report.headline_metrics[
        "finite_S3_solution_formula_failure_count"
    ] == 0
    assert report.claim_gate["two_partition_ribbon_surface_theorem_proved"]
    assert not report.claim_gate[
        "full_support_profile_ribbon_complex_theorem_proved"
    ]
    assert not report.claim_gate["growing_degree_pressure_separation_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
