"""Exact controls for the scoped fixed-cell cubic collision obstruction.

These test the mathematics and prescribed legal scaffold choices, not the
choices returned by production `_relation` or any compiled receiver.
"""
from itertools import combinations, product

import pytest


P = 7
Z = (1, 2, 4)
RECTANGLES = tuple(product(tuple(combinations(range(3), 2)), repeat=2))


def _rank(rows, prime=P):
    matrix = [list(row) for row in rows]
    if not matrix:
        return 0
    rank = 0
    for column in range(len(matrix[0])):
        pivot = next((i for i in range(rank, len(matrix))
                      if matrix[i][column] % prime), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = pow(matrix[rank][column], -1, prime)
        matrix[rank] = [value*inverse % prime for value in matrix[rank]]
        for i in range(rank+1, len(matrix)):
            scale = matrix[i][column]
            matrix[i] = [(value-scale*base) % prime
                         for value, base in zip(matrix[i], matrix[rank])]
        rank += 1
    return rank


def _planes_four(prime):
    for pivots in combinations(range(4), 2):
        free = [(i, j) for i, pivot in enumerate(pivots)
                for j in range(pivot+1, 4) if j not in pivots]
        for values in product(range(prime), repeat=len(free)):
            rows = [[0]*4 for _ in range(2)]
            for i, pivot in enumerate(pivots):
                rows[i][pivot] = 1
            for (i, j), value in zip(free, values):
                rows[i][j] = value
            yield tuple(map(tuple, rows))


@pytest.fixture(scope="module")
def planes():
    return tuple(_planes_four(P))


def _rectangle(rows, columns):
    i, k = rows
    j, l = columns
    positions = (3*i+j, 3*i+l, 3*k+j, 3*k+l)
    coefficients = (pow(Z[i]*Z[j], -1, P),
                    -pow(Z[i]*Z[l], -1, P) % P,
                    -pow(Z[k]*Z[j], -1, P) % P,
                    pow(Z[k]*Z[l], -1, P))
    return positions, coefficients


def _moments(coefficients, first, second):
    # Binomial factors 3 are invertible; these are the four trilinear tests.
    return tuple(sum(c*pow(a, 3-j, P)*pow(b, j, P)
                     for c, a, b in zip(coefficients, first, second)) % P
                 for j in range(4))


def _in_annihilator(coefficients):
    for rows, columns in RECTANGLES:
        positions, factors = _rectangle(rows, columns)
        if sum(factor*coefficients[position]
               for position, factor in zip(positions, factors)) % P:
            return False
    return True


def _example():
    q = ((1, 0), (0, 1), (5, 3))
    return tuple(tuple(a*b % P for a in q[i] for b in q[j])
                 for i in range(3) for j in range(3))


def _contract(labels, first, second, third):
    return tuple(sum(label[j]*a*b*c
                     for label, a, b, c in zip(labels, first, second, third)) % P
                 for j in range(len(labels[0])))


def _assert_axes(labels):
    for component in range(len(labels[0])):
        for fixed in range(3):
            assert sum(Z[i]*labels[3*i+fixed][component] for i in range(3)) % P == 0
            assert sum(Z[j]*labels[3*fixed+j][component] for j in range(3)) % P == 0


def test_annihilator_and_actual_tensor_have_complementary_ranks():
    labels = _example()
    _assert_axes(labels)
    assert _rank(labels) == 4
    generators = []
    for index in range(3):
        generators.append(tuple(Z[i]*int(j == index)
                                for i in range(3) for j in range(3)))
        generators.append(tuple(int(i == index)*Z[j]
                                for i in range(3) for j in range(3)))
    assert _rank(generators) == 5
    for coefficients in generators:
        assert _in_annihilator(coefficients)
        assert all(sum(c*label[j] for c, label in zip(coefficients, labels)) % P == 0
                   for j in range(4))
    rectangle_rows = []
    for rows, columns in RECTANGLES:
        positions, factors = _rectangle(rows, columns)
        row = [0]*9
        for position, factor in zip(positions, factors):
            row[position] = factor
        rectangle_rows.append(row)
    assert _rank(rectangle_rows) == 4


@pytest.mark.parametrize("count", (1, 2, 3, 4))
def test_cubes_of_distinct_projective_binary_forms_are_independent(count):
    forms = tuple((1, t) for t in range(P))+((0, 1),)
    for chosen in combinations(forms, count):
        coefficients = [(a**3 % P, 3*a*a*b % P, 3*a*b*b % P, b**3 % P)
                        for a, b in chosen]
        assert _rank(coefficients) == count


def test_cube_classes_exclude_adjacent_and_both_diagonal_pairings():
    cubes = {pow(value, 3, P) for value in range(1, P)}
    assert P-1 in cubes
    assert len({pow(value, (P-1)//3, P) for value in Z}) == 3
    for rows, columns in RECTANGLES:
        i, k = rows
        j, l = columns
        a = Z[i]*pow(Z[k], -1, P) % P
        b = Z[j]*pow(Z[l], -1, P) % P
        assert a not in cubes and b not in cubes
        assert not (a*b % P in cubes and a*pow(b, -1, P) % P in cubes)


def test_rref_plane_inventory_is_complete_and_has_no_duplicates(planes):
    expected = ((P**4-1)*(P**4-P))//((P**2-1)*(P**2-P))
    assert expected == len(planes) == len(set(planes)) == 2850
    assert all(_rank(plane) == 2 for plane in planes)


@pytest.mark.parametrize("rows,columns", RECTANGLES)
def test_no_rectangle_has_a_singular_plane_including_zero_entries(rows, columns, planes):
    _, coefficients = _rectangle(rows, columns)
    assert not any(_moments(coefficients, first, second) == (0, 0, 0, 0)
                   for first, second in planes)


def test_split_cubic_positive_control_has_27_planes(planes):
    assert sum(_moments((1, P-1, 1, P-1), first, second) == (0, 0, 0, 0)
               for first, second in planes) == 27


def test_two_independent_sde_witnesses_fail_the_mixed_conditions():
    labels = _example()
    first = (0, 1, 6, 6, 0, 1, 1, 6, 0)
    second = (0, 2, 6, 6, 0, 1, 1, 6, 0)
    assert _rank((first, second)) == 2
    assert tuple(pow(a, 3, P) for a in first) == tuple(pow(a, 3, P) for a in second)
    assert _contract(labels, first, first, first) == (0, 0, 0, 0)
    assert _contract(labels, second, second, second) == (0, 0, 0, 0)
    assert _contract(labels, first, first, second) == (0, 1, 0, 0)
    assert _contract(labels, first, second, second) == (0, 3, 0, 0)
    assert _in_annihilator(tuple(pow(a, 3, P) for a in first))
    assert not _in_annihilator(tuple(a*a*b % P for a, b in zip(first, second)))


def test_rank_four_condition_cannot_be_dropped():
    q = (1, 0, 5)
    labels = tuple((q[i]*q[j] % P,) for i in range(3) for j in range(3))
    _assert_axes(labels)
    assert _rank(labels) == 1
    first = tuple(int(i == 1) for i in range(9))
    second = tuple(int(i == 3) for i in range(9))
    assert _rank((first, second)) == 2
    for choices in product((first, second), repeat=3):
        assert _contract(labels, *choices) == (0,)
    assert not _in_annihilator(first)


def test_example_is_realized_by_prescribed_legal_scaffold_choices():
    labels = _example()
    zero = (0, 0, 0, 0)
    width, block_count = 5, 9
    blocks = [tuple(labels[3*i+j] for i in range(3))+(zero, zero) for j in range(3)]
    blocks += [(zero,)*width for _ in range(block_count-3)]
    relations = [Z+(0, 0)]*3+[(1, 0, 0, 0, 0)]*(block_count-3)
    original = tuple(label for block in blocks for label in block)
    assert len(original) == 45 and _rank(original) == 4
    children = []
    for block_index, (block, relation) in enumerate(zip(blocks, relations)):
        assert any(relation)
        assert all(sum(c*label[j] for c, label in zip(relation, block)) % P == 0
                   for j in range(4))
        cells = [dict() for _ in Z]
        for offset, coefficient in enumerate(relation):
            if coefficient:
                # These prescribed coefficients are representatives, with root one.
                cells[Z.index(coefficient)][width*block_index+offset] = 1
        assert cells[0]
        values = [tuple(sum(original[index][j]*weight**3
                            for index, weight in cell.items()) % P for j in range(4))
                  for cell in cells]
        children.append((cells, values))
    outer_relation = Z+(0,)*(block_count-3)
    assert all(sum(c*values[i][j] for c, (_, values) in zip(outer_relation, children)) % P == 0
               for i in range(3) for j in range(4))
    final_cells = [dict() for _ in range(9)]
    for coefficient, (cells, _) in zip(outer_relation, children):
        if coefficient:
            j = Z.index(coefficient)
            for i, cell in enumerate(cells):
                final_cells[3*i+j].update(cell)
    supports = [set(cell) for cell in final_cells]
    assert all(len(support) == 1 for support in supports)
    assert len(set().union(*supports)) == sum(map(len, supports)) == 9
    actual = tuple(tuple(sum(original[index][j]*weight**3
                             for index, weight in cell.items()) % P for j in range(4))
                   for cell in final_cells)
    assert actual == labels
    _assert_axes(actual)
    assert _rank(actual) == 4
    assert sum(label == zero for label in original) == 36
