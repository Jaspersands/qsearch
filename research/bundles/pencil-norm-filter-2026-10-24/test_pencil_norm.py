from itertools import product

import pytest
import sympy as sp
from sympy.polys.matrices import DomainMatrix

from pencil_norm import pencil_translation, solve_ut_pencil_norm, transformed
from power_product import solve_ut_power_product


def all_ut(d, p):
    positions = [(i, j) for i in range(d) for j in range(i + 1, d)]
    for values in product(range(p), repeat=len(positions)):
        matrix = sp.eye(d)
        for position, value in zip(positions, values):
            matrix[position] = value
        yield matrix


def closure(generators, d, p):
    identity = tuple(int(value) for value in sp.eye(d))
    seen, queue = {identity}, [identity]
    while queue:
        matrix = sp.Matrix(d, d, queue.pop())
        for generator in generators:
            result = tuple(int(value) % p for value in matrix * sp.Matrix(generator))
            if result not in seen:
                seen.add(result)
                queue.append(result)
    return seen


@pytest.mark.parametrize("p,which", [(5, 0), (5, 1), (7, 2), (7, 3)])
def test_exhaustive_original_norm_stabilizer_not_just_returned_members(p, which):
    x, y, z = sp.symbols("x y z")
    P, Q = [(x + y**2, y), (x, y**2), (x + z**2, y*z), (1, y + z)][which]
    answer = solve_ut_pencil_norm(P, Q, p, (x, y, z))
    original = sp.Poly(P**p - P*Q**(p - 1), x, y, z, modulus=p)
    expected = {tuple(int(value) for value in g) for g in all_ut(3, p)
                if transformed(original, g) == original}
    assert answer.status == "CLASSICALLY_SOLVED"
    assert closure(answer.group_generators, 3, p) == expected


def test_factor_permutations_are_retained_not_replaced_by_fixed_atoms():
    x, y, z = sp.symbols("x y z")
    p, P, Q = 5, x + y**2, y
    answer = solve_ut_pencil_norm(P, Q, p, (x, y, z))
    assert len(answer.lie_basis) == 1 and answer.translation_coefficients[0] != 0
    g = sp.Matrix(answer.group_generators[0])
    assert transformed(sp.Poly(P, x, y, z, modulus=p), g) != sp.Poly(P, x, y, z, modulus=p)
    old = solve_ut_power_product([P+t*Q for t in range(p)], [1]*p, p, (x, y, z))
    assert old.status == "OUT_OF_SCOPE"


@pytest.mark.parametrize("multiplicity", [1, 2, 3])
def test_gradient_divisor_recovers_repeated_denominator_multiplicity(multiplicity):
    x, y, z = sp.symbols("x y z")
    p = 11
    P, Q = x, y**multiplicity
    norm = sp.Poly(P**p-P*Q**(p-1), x, y, z, modulus=p)
    divisor = sp.Poly(0, x, y, z, modulus=p)
    for variable in (x, y, z):
        divisor = divisor.gcd(norm.diff(variable))
    assert divisor.monic() == sp.Poly(y**(multiplicity*(p-1)-1), x, y, z, modulus=p)
    assert solve_ut_pencil_norm(P, Q, p, (x, y, z)).status == "CLASSICALLY_SOLVED"


@pytest.mark.parametrize("p", [3, 5])
def test_nested_norm_is_counterexample_to_dropping_separation_guard(p):
    x, z, y = sp.symbols("x z y")
    P, Q = x**p-x*z**(p-1), y**p-y*z**(p-1)
    original = sp.Poly(P**p-P*Q**(p-1), x, z, y, modulus=p)
    g = sp.Matrix([[1, 0, 0], [0, 1, 1], [0, 0, 1]])
    assert transformed(original, g) == original
    assert transformed(sp.Poly(Q, x, z, y, modulus=p), g) != sp.Poly(Q, x, z, y, modulus=p)
    assert sp.Poly(P, x, z, y, modulus=p).gcd(sp.Poly(Q, x, z, y, modulus=p)).total_degree() == 0
    answer = solve_ut_pencil_norm(P, Q, p, (x, z, y))
    assert answer.status == "OUT_OF_SCOPE" and "separation" in answer.reason
    assert not answer.group_generators


def test_non_p_group_scalar_counterexample():
    x, y = sp.symbols("x y")
    p, g = 5, sp.diag(1, 2)
    norm = sp.Poly(x**p-x*y**(p-1), x, y, modulus=p)
    assert transformed(norm, g) == norm
    assert pencil_translation(sp.Poly(x, x, y, modulus=p), sp.Poly(y, x, y, modulus=p), g) is None


def test_zero_translation_uses_canonical_polynomial_zero():
    x, y, z = sp.symbols("x y z")
    P, Q = sp.Poly(1, x, y, z, modulus=7), sp.Poly(y+z, x, y, z, modulus=7)
    assert pencil_translation(P, Q, sp.eye(3)) == 0


def test_base_field_table_would_silently_change_the_problem():
    x, y = sp.symbols("x y")
    p, P, Q = 7, x, y**2+1
    norm = sp.Poly(P**p-P*Q**(p-1), x, y, modulus=p)
    assert all(int(norm.eval({x: a, y: b})) % p == 0 for a, b in product(range(p), repeat=2))
    assert transformed(norm, sp.Matrix([[1, 1], [0, 1]])) != norm
    answer = solve_ut_pencil_norm(P, Q, p, (x, y))
    assert answer.status == "CLASSICALLY_SOLVED" and not answer.group_generators


def test_infinitesimal_guard_is_not_implied_by_pencil_guard():
    variables = sp.symbols("x:5")
    answer = solve_ut_pencil_norm(variables[0]**2+variables[1], variables[1], 7, variables)
    assert 7 > answer.gradient_separation_bound
    assert answer.status == "OUT_OF_SCOPE" and "infinitesimal" in answer.reason


def test_common_factors_are_not_silently_cancelled():
    x, y = sp.symbols("x y")
    answer = solve_ut_pencil_norm(x*y, y**2, 7, (x, y))
    assert answer.status == "OUT_OF_SCOPE" and "coprime" in answer.reason


@pytest.mark.parametrize("p", [5, 7, 11])
def test_orbit_rank_at_least_p_despite_small_pencil_reduction(p):
    y, z = sp.symbols("y z")
    rows = []
    for c in range(p):
        polynomial = sp.Poly((y+c*z)**(p-1), y, z, modulus=p)
        rows.append([int(polynomial.coeff_monomial(y**(p-1-j)*z**j)) % p for j in range(p)])
    assert DomainMatrix.from_list(rows, sp.GF(p)).rank() == p


def test_127_bit_prime_keeps_all_norm_powers_unexpanded():
    p, variables = 2**127-1, sp.symbols("x:6")
    answer = solve_ut_pencil_norm(variables[0]+variables[1]**2, variables[1], p, variables)
    assert answer.status == "CLASSICALLY_SOLVED"
    assert len(answer.lie_basis) == 7
    assert answer.formal_degree_upper_bound == 2*p
    assert len(answer.translation_coefficients) == 7
    assert sum(bool(value) for value in answer.translation_coefficients) == 1


@pytest.mark.parametrize("p", [2, 9, 15, 1.5, True])
def test_invalid_fields(p):
    x, y = sp.symbols("x y")
    with pytest.raises(ValueError):
        solve_ut_pencil_norm(x, y, p, (x, y))


@pytest.mark.parametrize("variables", [(), (sp.Symbol("x"), sp.Symbol("x")), (1, 2)])
def test_invalid_variables(variables):
    with pytest.raises(ValueError):
        solve_ut_pencil_norm(1, 1, 7, variables)


@pytest.mark.parametrize("P,Q", [(0, sp.Symbol("y")), (1, 0), (sp.Symbol("x"), 1)])
def test_outside_specialized_input_contract_is_not_hardness(P, Q):
    x, y = sp.symbols("x y")
    answer = solve_ut_pencil_norm(P, Q, 7, (x, y))
    assert answer.status == "OUT_OF_SCOPE" and not answer.group_generators


def test_trivial_one_variable_ambient():
    x = sp.Symbol("x")
    answer = solve_ut_pencil_norm(1, x, 5, (x,))
    assert answer.status == "CLASSICALLY_SOLVED" and not answer.lie_basis


def test_live_replay_preserves_scope_and_counterexamples():
    from pencil_norm_replay import audit
    result = audit()
    assert result["prime_certificate"]["final_residue"] == 0
    assert [len(row["lie_basis"]) for row in result["controls"]] == [1, 7, 29]
    assert all(not row["large_norm_expanded"] for row in result["controls"])
    assert all(not row["old_small_factor_support_guard"] and not row["old_no_carry_guard"]
               for row in result["controls"])
    assert all(row["norm_preserved"] and not row["denominator_preserved"]
               and row["filter_status"] == "OUT_OF_SCOPE" for row in result["nested_norm_counterexamples"])
    assert not result["speedup_claim"] and not result["quantum_algorithm_executed"]
    assert not result["classical_novelty_claim"]
