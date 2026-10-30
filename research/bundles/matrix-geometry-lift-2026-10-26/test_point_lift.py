from pathlib import Path
import sys

from flint import nmod_mat
import pytest

from point_lift import lift_point, orthogonal, rows, schur

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "ag-divisor-class-control-2026-10-26"))
try:
    from divisor_control import build_control, cover
finally:
    sys.path.pop(0)


@pytest.fixture(scope="module")
def source():
    return build_control()[2]["original_parity"]


@pytest.mark.parametrize("point", [0, 17, 175])
def test_matrix_only_lift_on_actual_new_class(source, point):
    result = lift_point(source, cover.PRIME, point)
    assert result["original_matrix"] == source
    assert (result["inferred_genus_under_AG_promise"], result["inferred_degree_under_AG_promise"]) == (41, 83)
    assert (result["lifted_dimension"], result["lifted_degree_under_AG_promise"],
            result["lifted_square_dimension"], result["lifted_quadratic_relation_dimension"]) == (44, 84, 128, 862)
    column = [row[point] for row in result["lifted_projective_points_as_columns"]]
    assert column == [0]*43+[1]
    minus = nmod_mat(result["shortened_original"], cover.PRIME)
    lifted = nmod_mat(result["lifted_punctured"], cover.PRIME)
    W = nmod_mat(result["punctured_square"], cover.PRIME)
    products = schur(minus, lifted)
    assert nmod_mat(rows(W)+rows(products), cover.PRIME).rank() == W.rank()
    assert not result["AG_promise_verified_by_dimension_checks"]
    assert not result["native_search_solved_by_lift"]


def test_known_near_canonical_curve_has_same_lift_dimensions():
    source = cover.control()[2]["original_parity"]
    result = lift_point(source, cover.PRIME)
    assert result["lifted_dimension"] == 44
    assert result["lifted_square_dimension"] == 128


def test_column_scaling_does_not_change_geometric_dimensions(source):
    scaled = [[value*(i+1) % cover.PRIME for i, value in enumerate(row)] for row in source]
    result = lift_point(scaled, cover.PRIME, 5)
    assert result["original_matrix"] == scaled
    assert result["lifted_square_dimension"] == 128


@pytest.mark.parametrize("point", [-1, 176, True])
def test_invalid_point_rejected(source, point):
    with pytest.raises(ValueError):
        lift_point(source, cover.PRIME, point)


def test_no_implicit_AG_claim_from_arbitrary_matrix():
    with pytest.raises(ValueError):
        lift_point([[1, 0, 1, 1], [0, 1, 1, 2]], 3)


def test_orthogonal_computation_is_exact():
    matrix = nmod_mat([[1, 2, 3], [2, 1, 4]], 7)
    complement = orthogonal(matrix)
    assert complement.rank() == 1
    assert all(value == 0 for row in rows(matrix*complement.transpose()) for value in row)
