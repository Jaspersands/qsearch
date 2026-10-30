from itertools import product

import pytest
import z3

from residual_sat import (
    BinaryField, affine_chart, conic_constraint, inverse_trace_constraint, solve_residual,
    symbolic_multiply, syndrome, verify,
)


@pytest.mark.parametrize("bits,modulus", [(3, 11), (4, 19), (5, 37), (7, 131), (11, 2053), (17, 131081), (31, 2147483657)])
def test_field_presentation_and_basis_trace(bits, modulus):
    field = BinaryField(bits, modulus)
    for a in range(1, min(field.order, 100)):
        assert field.multiply(a, field.inverse(a)) == 1
        assert field.trace(a) == field.trace(field.multiply(a, a))


@pytest.mark.parametrize("modulus", [9, 15, 17])
def test_reducible_or_wrong_degree_modulus_rejected(modulus):
    with pytest.raises(ValueError):
        BinaryField(3, modulus)


def test_symbolic_field_product_exhaustively_matches_independent_polynomial_product():
    field = BinaryField(3, 11)
    a, b = z3.BitVecs("a b", 3)
    expression = symbolic_multiply(field, a, b)
    for x, y in product(range(8), repeat=2):
        result = z3.simplify(z3.substitute(expression, (a, z3.BitVecVal(x, 3)), (b, z3.BitVecVal(y, 3))))
        assert result.as_long() == field.multiply(x, y)


def test_totalized_inverse_and_bit_predicate_exhaustively():
    field = BinaryField(3, 11)
    x, y = z3.BitVecs("x y", 3)
    for bit in (0, 1):
        expression = inverse_trace_constraint(field, x, y, bit)
        for a, b in product(range(8), repeat=2):
            actual = z3.is_true(z3.simplify(z3.substitute(expression,
                (x, z3.BitVecVal(a, 3)), (y, z3.BitVecVal(b, 3)))))
            assert actual == (b == field.inverse(a) and field.trace(b) == bit)


@pytest.mark.parametrize("points,checks", [((0, 1, 2), 1), ((1, 2, 4, 6), 2), ((0, 2, 5), 3)])
def test_lagrange_chart_every_syndrome_and_free_assignment(points, checks):
    field = BinaryField(3, 11)
    for rhs in product(range(8), repeat=checks):
        constants, matrix = affine_chart(field, points, checks, rhs)
        for free in product(range(8), repeat=len(points)-checks):
            word = []
            for c, row in zip(constants, matrix):
                for a, b in zip(row, free):
                    c ^= field.multiply(a, b)
                word.append(c)
            word.extend(free)
            assert syndrome(field, points, word, checks) == rhs


@pytest.mark.parametrize("encoding", ["inverse", "conic"])
@pytest.mark.parametrize("target", [(0, 0), (0, 1), (1, 0), (1, 1)])
def test_every_small_syndrome_matches_exhaustive_fibers(target, encoding):
    field, points = BinaryField(3, 11), (1, 2)
    for h in range(8):
        possible = [word for word in product(range(8), repeat=2)
                    if verify(field, points, word, 1, target, (h,))]
        result = solve_residual(field, points, 1, target, (h,), seconds=5, encoding=encoding)
        assert result["status"] == ("VERIFIED_RESIDUAL_WITNESS" if possible else "UNSAT_REPORTED_BY_Z3")
        if possible:
            assert tuple(result["witness"]) in possible


def test_zero_one_syndrome_contradiction_cannot_pass_by_false_zero_inverse():
    field = BinaryField(3, 11)
    result = solve_residual(field, (0, 1), 1, (0, 1), (0,), seconds=5)
    assert result["status"] == "UNSAT_REPORTED_BY_Z3"
    assert not verify(field, (0, 1), (0, 0), 1, (0, 1), (0,))


@pytest.mark.parametrize("bits,modulus", [(3, 11), (4, 19)])
def test_conic_projection_exact_including_zero_and_even_degree(bits, modulus):
    field = BinaryField(bits, modulus)
    for x, bit in product(range(field.order), (0, 1)):
        u = z3.BitVec("u", bits)
        solver = z3.Solver()
        solver.add(conic_constraint(field, z3.BitVecVal(x, bits), u, bit))
        assert (solver.check() == z3.sat) == (field.trace(field.inverse(x)) == bit)


def test_native_prefix_is_not_a_planted_full_witness():
    from run_attack import make_instance, worker
    field, instance = make_instance(7, 2301, "induced", "random")
    assert len(instance["accepted_prefix"]) < len(instance["points"])
    assert not instance["full_witness_used_to_generate_input"]
    result = worker({"bits": 7, "seed": 2301, "mode": "induced", "pattern": "random",
                     "seconds": 5, "resource_limit": 5_000_000, "encoding": "conic", "algebraic": True})
    assert result["original_native_relation_verified"]
    assert verify(field, instance["points"], result["full_native_witness"],
                  instance["checks"], instance["targets"], [0]*instance["checks"])


def test_solver_exhaustion_is_unknown_not_hardness_or_unsat():
    field = BinaryField(5, 37)
    result = solve_residual(field, tuple(range(8)), 4, (1,)*8, (0, 1, 2, 3),
                            seconds=5, resource_limit=1)
    assert result["status"] == "UNKNOWN"
    assert not result["polynomial_time_proved"]
    assert not result["uniform_sampling_claim"]


def test_duplicate_points_and_bad_targets_are_rejected():
    field = BinaryField(3, 11)
    with pytest.raises(ValueError):
        solve_residual(field, (1, 1), 1, (0, 1), (0,))
    with pytest.raises(ValueError):
        solve_residual(field, (1, 2), 1, (0, 2), (0,))


def test_whole_worker_cap_covers_startup_build_and_verification():
    from run_attack import bounded_run
    result = bounded_run({"bits": 17, "seed": 2301, "mode": "induced", "pattern": "random",
                          "seconds": .001, "resource_limit": 5_000_000,
                          "encoding": "inverse", "algebraic": False})
    assert result["result"]["status"] == "UNKNOWN"
    assert result["result"]["reason"] == "whole_worker_wall_cap"
