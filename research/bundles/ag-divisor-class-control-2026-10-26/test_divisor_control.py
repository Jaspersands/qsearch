from fractions import Fraction

import pytest

from divisor_control import DEFAULT_INDICES, EXTRA_X, build_control, cover, split_fiber


@pytest.fixture(scope="module")
def actual():
    return build_control()


def test_extra_points_are_actual_distinct_cover_points_outside_D():
    points = split_fiber(EXTRA_X)
    p = cover.PRIME
    assert len({(P["x"], P["y"], *P["w"]) for P in points}) == 16
    for P in points:
        product = 1
        for a in range(13):
            product = product*(P["x"]-a) % p
        assert P["y"]**2 % p == product
        assert all(w*w % p == P["x"]*(P["x"]-j) % p for j, w in enumerate(P["w"], 1))
    assert EXTRA_X not in cover.default_seed().splitting_x


def test_complete_new_class_escapes_same_code_cube(actual):
    problem, _, data = actual
    assert data["divisor_degree"] == 83
    assert (problem.k, problem.m, len(problem.W), len(problem.U)) == (43, 176, 126, 176)
    assert not problem.annihilator
    assert data["dimension_L_G_minus_K"] == 0
    for coefficients in data["rr_basis_coefficients"]:
        assert all(sum(a*b for a, b in zip(row, coefficients)) % cover.PRIME == 0
                   for row in data["vanishing_constraints"])


def test_no_annihilator_is_not_hardness(actual):
    problem, fiber, data = actual
    target = tuple(range(problem.k))
    failed = problem.deterministic_attempt(target, 2)
    assert failed["witness"] is None and not failed["hardness_evidence"]
    sample = fiber.sample(target, seed=20261026, attempts=8)
    assert problem.verifies(sample["witness"], target)
    assert data["classical_uniform_fiber_success_lower"] == Fraction(99827, 100003)
    assert data["classical_expected_trials_upper"] == Fraction(100003, 99827)
    assert data["all_affine_coordinate_marginals_verified_uniform"]


@pytest.mark.parametrize("x", [0, 18501, -1, 100003, True])
def test_wrong_or_overlapping_extra_fibers_rejected(x):
    with pytest.raises(ValueError):
        split_fiber(x)


@pytest.mark.parametrize("indices", [(0, 0, 1, 2, 3), (0, 1, 2, 3), (0, 1, 2, 3, 16)])
def test_invalid_zero_divisors_rejected(indices):
    with pytest.raises(ValueError):
        build_control(indices)


def test_no_distribution_scaling_or_advantage_promotion(actual):
    _, _, data = actual
    assert data["chosen_fiber_indices"] == DEFAULT_INDICES
    assert data["divisor_class_constructed"]
    for key in ("uniform_Picard_class_sample", "higher_level_cube_rank_known",
                "quantum_execution", "classical_hardness_established",
                "quantum_advantage_established", "registry_admission"):
        assert not data[key]
