from itertools import product

import pytest
import sympy as sp

from power_product import exp_upper, fixes_atoms, solve_ut_power_product, transformed


def matrices_ut(d, p):
    positions = [(i, j) for i in range(d) for j in range(i+1, d)]
    for entries in product(range(p), repeat=len(positions)):
        matrix = sp.eye(d)
        for position, value in zip(positions, entries):
            matrix[position] = value
        yield matrix


def generated_group(generators, d, p):
    identity = tuple(int(x) for x in sp.eye(d))
    result, queue = {identity}, [identity]
    while queue:
        current = sp.Matrix(d, d, queue.pop())
        for generator in generators:
            new = tuple(int(x) % p for x in current*sp.Matrix(generator))
            if new not in result:
                result.add(new)
                queue.append(new)
    return result


@pytest.mark.parametrize("weights", [(1, 1), (2, 3), (5, 10), (0, 2)])
def test_exhaustive_same_native_product_not_only_membership(weights):
    x = sp.symbols("x:3")
    atoms = (x[0], x[1]+x[2])
    result = solve_ut_power_product(atoms, weights, 5, x)
    target = sp.Poly(sp.prod(a**e for a, e in zip(atoms, weights)), *x, modulus=5)
    actual = generated_group(result.group_generators, 3, 5)
    expected = {tuple(int(v) for v in g) for g in matrices_ut(3, 5) if transformed(target, g) == target}
    assert result.status == "CLASSICALLY_SOLVED"
    assert actual == expected


def test_shared_reducible_atoms_need_no_factorization():
    x, y, z = sp.symbols("x y z")
    atoms = (x*y, x*(y+z))
    result = solve_ut_power_product(atoms, (2, 3), 7, (x, y, z))
    target = sp.Poly(atoms[0]**2*atoms[1]**3, x, y, z, modulus=7)
    actual = generated_group(result.group_generators, 3, 7)
    expected = {tuple(int(v) for v in g) for g in matrices_ut(3, 7) if transformed(target, g) == target}
    assert result.radical_degree_upper_bound == 4
    assert actual == expected


def test_127_bit_prime_and_huge_binary_exponents_are_not_expanded():
    p = 2**127-1
    x = sp.symbols("x:4")
    result = solve_ut_power_product((x[0], x[0]+x[1]**2), (p**8-1, p**9+2), p, x)
    assert result.status == "CLASSICALLY_SOLVED"
    assert result.total_degree.bit_length() > 1100
    assert result.radical_degree_upper_bound == 3
    assert len(result.lie_basis) == 1
    assert result.group_generators[0][2][3] != 0
    assert all(result.group_generators[0][i][j] == int(i == j)
               for i in range(4) for j in range(4) if (i, j) != (2, 3))
    assert not p > 3*result.total_degree


@pytest.mark.parametrize("p", [3, 5, 7])
def test_sharp_p_factor_counterexample(p):
    x, y = sp.symbols("x y")
    atoms = tuple(x+a*y for a in range(p))
    norm = sp.Poly(sp.prod(atoms), x, y, modulus=p)
    assert norm == sp.Poly(x**p-x*y**(p-1), x, y, modulus=p)
    shear = sp.Matrix([[1, 1], [0, 1]])
    assert transformed(norm, shear) == norm
    assert not fixes_atoms(atoms, shear, p, (x, y))
    result = solve_ut_power_product(atoms, (1,)*p, p, (x, y))
    assert result.status == "OUT_OF_SCOPE" and not result.group_generators


def test_p_group_premise_is_essential():
    x, y = sp.symbols("x y")
    swap = sp.Matrix([[0, 1], [1, 0]])
    target = sp.Poly(x*y, x, y, modulus=5)
    assert transformed(target, swap) == target
    assert not fixes_atoms((x, y), swap, 5, (x, y))


def test_scalar_semi_invariants_cannot_be_ignored_for_non_p_groups():
    x, y = sp.symbols("x y")
    sign = sp.diag(-1, 1)
    assert transformed(sp.Poly(x**2, x, y, modulus=5), sign) == sp.Poly(x**2, x, y, modulus=5)
    assert not fixes_atoms((x,), sign, 5, (x, y))


def test_atom_degree_guard_is_separate_from_factor_count():
    x = sp.symbols("x:4")
    result = solve_ut_power_product((x[0]**2+x[1],), (100,), 5, x)
    assert result.radical_degree_upper_bound == 2
    assert result.status == "OUT_OF_SCOPE"
    assert "infinitesimal" in result.reason


@pytest.mark.parametrize("atoms,weights,reason", [((0,), (1,), "zero"), ((0,), (0,), "constant"),
                                                ((2,), (5,), "constant"), ((), (), "constant")])
def test_zero_constant_and_ignored_zero_power(atoms, weights, reason):
    variables = sp.symbols("x:3")
    result = solve_ut_power_product(atoms, weights, 3, variables)
    assert result.status == "FULL_GROUP" and reason in result.reason
    assert len(generated_group(result.group_generators, 3, 3)) == 27


@pytest.mark.parametrize("weights", [(-1,), (1.0,), (True,), (), (1, 2)])
def test_invalid_exponents_rejected(weights):
    x, y = sp.symbols("x y")
    with pytest.raises(ValueError):
        solve_ut_power_product((x,), weights, 5, (x, y))


@pytest.mark.parametrize("prime", [2, 9, 15, 1.5, True])
def test_invalid_fields_rejected(prime):
    x, y = sp.symbols("x y")
    with pytest.raises(ValueError):
        solve_ut_power_product((x,), (1,), prime, (x, y))


def test_exponential_checks_its_matrix_contract():
    with pytest.raises(ValueError):
        exp_upper([[0, 0], [1, 0]], 5)
    with pytest.raises(ValueError):
        exp_upper([[0, 1], [0, 0]], 2)


def test_one_variable_trivial_ambient():
    x = sp.symbols("x")
    result = solve_ut_power_product((x,), (10**10,), 5, (x,))
    assert result.status == "CLASSICALLY_SOLVED"
    assert not result.lie_basis and not result.group_generators


def test_live_replay_keeps_access_and_boundary_flags():
    from power_product_replay import audit
    result = audit()
    assert result["prime_certificate"]["final_residue"] == 0
    assert [len(control["lie_basis"]) for control in result["controls"]] == [1, 6, 28]
    assert all(not control["old_raw_degree_guard"] and not control["old_mixed_no_carry_guard"]
               for control in result["controls"])
    assert all(control["filter_status"] == "OUT_OF_SCOPE" for control in result["sharp_boundary_controls"])
    assert not result["new_quantum_algorithm"] and not result["speedup_claim"]
    assert not result["arbitrary_circuit_factorization_implemented"]
