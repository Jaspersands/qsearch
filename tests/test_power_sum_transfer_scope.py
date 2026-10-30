"""Exact transfer countercontrols, not tests of the cited point-finder."""
import random

import pytest
import sympy as sp

from theorems.power_sde import power_arity, power_weights
from theorems.weighted_two_erasure_cascade import verify_general_degree_witness


def _repeated_last_basis_columns(rank, width):
    basis = [tuple(int(i == j) for i in range(rank)) for j in range(rank)]
    return basis + [basis[-1]] * (width - rank)


@pytest.mark.parametrize("prime,degree,rank", [(7, 2, 2), (7, 3, 2),
                                             (13, 3, 3), (17, 4, 3)])
def test_full_row_rank_and_many_nonzero_columns_do_not_imply_radicality(
        prime, degree, rank):
    width = rank * degree + 1
    columns = _repeated_last_basis_columns(rank, width)
    matrix = sp.Matrix.hstack(*(sp.Matrix(column) for column in columns))
    assert matrix[:, :rank] == sp.eye(rank)
    assert all(any(column) for column in columns)
    assert width > rank * degree and prime > degree
    x = sp.symbols(f"x0:{width}")
    equations = [sum(column[row] * x[j]**degree
                     for j, column in enumerate(columns)) for row in range(rank)]
    ideal = sp.groebner(equations, *x, modulus=prime)
    assert ideal.reduce(x[0]**degree)[1] == 0
    assert ideal.reduce(x[0])[1] == x[0]
    # The homogeneous system has only degree >= d terms, but its radical
    # contains x0. A smoothness claim cannot follow from matrix rank alone.
    jacobian = sp.Matrix(equations).jacobian(x)
    assert all(sp.rem(entry, x[0], x[0]) == 0 for entry in jacobian.row(0))


def test_fixing_an_arbitrary_chart_can_erase_every_nonzero_solution():
    prime, degree, rank, width = 7, 3, 2, 7
    columns = _repeated_last_basis_columns(rank, width)
    x = sp.symbols(f"x0:{width}")
    equations = [sum(column[row] * x[j]**degree
                     for j, column in enumerate(columns)) for row in range(rank)]
    # x0^3 = 0 forces x0 = 0 over the field. All witnesses lie elsewhere.
    wrong_chart = sp.groebner(equations + [x[0]-1], *x, modulus=prime)
    assert wrong_chart.contains(sp.Integer(1))
    witness = (0, 1, prime-1, 0, 0, 0, 0)
    verify_general_degree_witness(prime, columns, witness, degree)
    assert all(int(f.subs(dict(zip(x, witness)))) % prime == 0 for f in equations)
    assert witness[1] == 1
    right_chart = sp.groebner(equations + [x[1]-1], *x, modulus=prime)
    assert not right_chart.contains(sp.Integer(1))


@pytest.mark.parametrize("rank", [2, 4])
def test_existing_solver_handles_the_nonradical_transfer_counterexample(rank):
    prime, degree = 65537, 2
    columns = _repeated_last_basis_columns(rank, power_arity(rank, degree))
    result = power_weights(prime, degree, columns, rng=random.Random(20261030))
    verify_general_degree_witness(prime, columns, result.weights, degree)
    assert result.compressed_rank == rank
    assert any(result.weights)
    assert result.weights[:rank-1] == (0,) * (rank-1)


@pytest.mark.parametrize("degree,rank", [(2, 2), (3, 3), (4, 2)])
def test_reduced_disjoint_power_system_still_has_product_geometric_degree(degree, rank):
    # A product of Fermat hypersurfaces on disjoint groups of d+1 variables
    # has a reduced regular defining sequence in characteristic > d. Slice
    # each block to x_j^d = 1: a transverse zero-dimensional section has d^r
    # points over the algebraic closure, all with nonzero Jacobian determinant.
    prime = 97
    x = sp.symbols(f"x0:{rank}")
    equations = [v**degree-1 for v in x]
    basis = sp.groebner(equations, *x, modulus=prime)
    assert [poly.LM().exponents for poly in basis.polys] == [
        tuple(degree if i == j else 0 for i in range(rank)) for j in range(rank)]
    roots = [a for a in range(prime) if pow(a, degree, prime) == 1]
    assert len(roots) == degree
    assert all(degree * pow(a, degree-1, prime) % prime for a in roots)
    assert len(roots)**rank == degree**rank
    for variable in x:
        assert sp.gcd(sp.Poly(variable**degree-1, variable, modulus=prime),
                      sp.Poly(degree*variable**(degree-1), variable, modulus=prime)).degree() == 0


def test_smooth_output_of_a_reduced_homogeneous_system_is_nonzero():
    p = 7
    x, y, z = sp.symbols("x y z")
    equation = x**3+y**3+z**3
    gradient = [sp.diff(equation, v) for v in (x, y, z)]
    origin = {x: 0, y: 0, z: 0}
    assert equation.subs(origin) == 0
    assert all(entry.subs(origin) == 0 for entry in gradient)
    point = {x: 1, y: p-1, z: 0}
    assert int(equation.subs(point)) % p == 0
    assert any(int(entry.subs(point)) % p for entry in gradient)
    # This checks the singular-origin distinction. It does not execute the
    # external point-finder, whose smooth-output contract comes from its proof.
