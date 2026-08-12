from self_dual_wreath_orientation_partition_traffic import (
    equality_traffic_coefficients,
    equality_traffic_value,
    exact_equality_partition_control,
    orientation_partition_traffic_theorem,
    partition_is_coarser,
    run_orientation_partition_traffic,
)


def test_partition_coarsening_direction_is_correct() -> None:
    fine = ((0, 1), (2, 3))
    coarse = ((0, 1, 2, 3),)

    assert partition_is_coarser(coarse, fine)
    assert not partition_is_coarser(fine, coarse)


def test_aabb_and_abab_have_exact_alpha_squared_gap() -> None:
    aabb = equality_traffic_coefficients(4, ((0, 1), (2, 3)))
    abab = equality_traffic_coefficients(4, ((0, 2), (1, 3)))

    assert aabb == {1: 1, 2: 1}
    assert abab == {1: 1}
    for alpha in (0.75, 1.0, 2.0, 3.5):
        assert abs(
            equality_traffic_value(4, ((0, 1), (2, 3)), alpha)
            - equality_traffic_value(4, ((0, 2), (1, 3)), alpha)
            - alpha**2
        ) < 1e-12


def test_crossing_exact_pattern_is_suppressed() -> None:
    crossing = exact_equality_partition_control(((0, 2), (1, 3)), 4)
    noncrossing = exact_equality_partition_control(((0, 1), (2, 3)), 4)

    assert crossing.limiting_exact_equality_traffic == "0"
    assert crossing.fixed_nontrivial_residual_required
    assert noncrossing.limiting_exact_equality_traffic == "alpha^2"
    assert noncrossing.presentation_free_rank == 2


def test_triple_crossing_forces_one_common_block() -> None:
    assert equality_traffic_coefficients(
        6,
        ((0, 3), (1, 4), (2, 5)),
    ) == {1: 1}


def test_theorem_keeps_polar_transfer_open() -> None:
    theorem = orientation_partition_traffic_theorem()
    report = run_orientation_partition_traffic()

    assert theorem.every_fixed_equality_pattern_proved
    assert not theorem.polar_functional_calculus_proved
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["all_fixed_equality_constrained_traffic_proved"]
    assert not report.claim_gate["polar_functional_calculus_transfer_proved"]
    assert not report.claim_gate["natural_full_support_canonical_curl_positive"]
    assert not report.claim_gate["speedup_claim_allowed"]
