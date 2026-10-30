"""Independent formal iteration, exhaustive finite groups, and scope controls."""
from dataclasses import replace
from itertools import product
import json
import random

import pytest
import sympy as sp

from theorems.iterated_quadratic_jet import (
    QuadraticIteration,
    analyze,
    block_exp,
    block_log,
    iterate_jet,
    iterate_two_jet,
    report,
    scalar_two_jet,
    verify_propagation,
)


def _identity(D):
    return tuple(tuple(int(i == j) for j in range(D)) for i in range(D))


def _instance(*, D=3, block_size=3, p=7, T=2, seed=31):
    rng = random.Random(seed)
    forms = []
    for _ in range(D):
        B = [[0] * D for _ in range(D)]
        for i in range(D):
            for j in range(i, D):
                B[i][j] = B[j][i] = rng.randrange(p)
        forms.append(B)
    return QuadraticIteration(p, block_size, T, [rng.randrange(1, p) for _ in range(D)],
                              [[rng.randrange(p) for _ in range(D)] for _ in range(D)],
                              forms, [rng.randrange(1, p) for _ in range(D)])


def _full_iterate(problem):
    """Expand entire formal iterates, never truncate or use a jet recurrence."""
    x = sp.symbols(f"x0:{problem.D}")
    values = [sp.Poly(y, *x, modulus=problem.p) for y in x]
    for _ in range(problem.T):
        values = [problem.c[i]
                  + sum(problem.A[i][j] * values[j] for j in range(problem.D))
                  + sum(problem.B[i][j][k] * values[j] * values[k]
                        for j in range(problem.D) for k in range(problem.D))
                  for i in range(problem.D)]
    return values


def _extract(poly, p):
    D = len(poly.gens)
    zero = (0,) * D
    linear = []
    quadratic = [[0] * D for _ in range(D)]
    for i in range(D):
        exponent = list(zero)
        exponent[i] = 1
        linear.append(int(poly.coeff_monomial(tuple(exponent))) % p)
        for j in range(D):
            pair = list(exponent)
            pair[j] += 1
            coefficient = int(poly.coeff_monomial(tuple(pair)))
            quadratic[i][j] = coefficient * (1 if i == j else pow(2, -1, p)) % p
    return (int(poly.coeff_monomial(zero)) % p, tuple(linear),
            tuple(tuple(row) for row in quadratic))


@pytest.mark.parametrize("p", [7, 101])
@pytest.mark.parametrize("seed", [12, 31])
@pytest.mark.parametrize("T", range(4))
def test_jet_matches_independent_sympy_full_iterate(p, seed, T):
    problem = _instance(p=p, seed=seed, T=T)
    full = _full_iterate(problem)
    expected = [_extract(poly, p) for poly in full]
    actual = iterate_two_jet(problem)
    assert actual.v == tuple(row[0] for row in expected)
    assert actual.J == tuple(row[1] for row in expected)
    assert actual.C == tuple(row[2] for row in expected)
    scalar = scalar_two_jet(problem)
    scalar_expected = _extract(sum(a * poly for a, poly in zip(problem.ell, full)), p)
    assert (scalar.constant, scalar.linear, scalar.quadratic) == scalar_expected
    if T == 1:
        assert any(actual.v)


def test_nonzero_orbit_drives_both_jacobian_and_quadratic_update():
    B = [[[0] * 3 for _ in range(3)] for _ in range(3)]
    B[0][0][0] = 1
    problem = QuadraticIteration(7, 3, 2, [1, 2, 3], _identity(3), B, [1, 0, 0])
    jet = iterate_two_jet(problem)
    assert jet.v == (3, 4, 6)
    assert jet.J == ((3, 0, 0), (0, 1, 0), (0, 0, 1))
    assert jet.C[0] == ((4, 0, 0), (0, 0, 0), (0, 0, 0))


@pytest.mark.parametrize("anchor", [(1, 0, 0), (6, 0, 0)])
@pytest.mark.parametrize("T", range(4))
def test_anchored_jet_matches_independent_shift_of_full_sympy_iterate(anchor, T):
    problem = _instance(T=T)
    full = _full_iterate(problem)
    x = full[0].gens
    shifted = [sp.Poly(poly.as_expr().subs({v: v + a for v, a in zip(x, anchor)}, simultaneous=True),
                       *x, modulus=problem.p) for poly in full]
    expected = [_extract(poly, problem.p) for poly in shifted]
    actual = iterate_jet(problem, anchor)
    assert (actual.v, actual.J, actual.C) == tuple(tuple(row[i] for row in expected) for i in range(3))
    scalar = scalar_two_jet(problem, anchor)
    scalar_expected = _extract(sum(a * poly for a, poly in zip(problem.ell, shifted)), problem.p)
    assert (scalar.constant, scalar.linear, scalar.quadratic) == scalar_expected


def test_symmetric_off_diagonal_entries_are_half_the_monomial_coefficient():
    problem = _instance(T=1)
    data = problem.specification()
    data["ell"] = [1, 0, 0]
    data["B"][0] = [[0, 3, 0], [3, 0, 0], [0, 0, 0]]
    problem = QuadraticIteration(**data)
    poly = _full_iterate(problem)[0]
    assert int(poly.coeff_monomial((1, 1, 0))) % 7 == 6
    assert scalar_two_jet(problem).quadratic[0][1] == 3


def _scalar_fixture(linear, quadratic, block_size):
    D = len(linear)
    return QuadraticIteration(7, block_size, 1, [2] + [0] * (D - 1),
                              [linear] + [[0] * D for _ in range(D - 1)],
                              [quadratic] + [[[0] * D for _ in range(D)] for _ in range(D - 1)],
                              [1] + [0] * (D - 1))


def _matrix_from_coordinates(problem, values, diagonal=0):
    matrix = [[diagonal * int(i == j) for j in range(problem.D)] for i in range(problem.D)]
    for (i, j), value in zip(problem.lie_coordinates, values):
        matrix[i][j] = value
    return tuple(tuple(row) for row in matrix)


def _finite_invariant(g, linear, quadratic, p):
    # Direct finite coefficient equalities, independent of infinitesimal equations.
    G, B, b = sp.Matrix(g), sp.Matrix(quadratic), sp.Matrix([linear])
    return all(int(x) % p == 0 for x in G.T * B * G - B) and all(
        int(x) % p == 0 for x in b * G - b)


@pytest.mark.parametrize("linear,quadratic", [
    ([0, 0, 0], [[0, 0, 0], [0, 0, 0], [0, 0, 0]]),
    ([1, 0, 0], [[0, 0, 0], [0, 0, 0], [0, 0, 0]]),
    ([0, 0, 0], [[1, 0, 0], [0, 2, 0], [0, 0, 3]]),
    ([0, 0, 1], [[0, 0, 1], [0, 6, 0], [1, 0, 0]]),
    ([0, 0, 0], [[0, 0, 0], [0, 0, 0], [0, 0, 1]]),
    ([0, 1, 3], [[0, 2, 1], [2, 3, 4], [1, 4, 5]]),
])
def test_exhaustive_finite_ut3_invariance_equals_exponential_of_log_kernel(linear, quadratic):
    problem = _scalar_fixture(linear, quadratic, 3)
    result = analyze(problem)
    basis = result["kernel_basis"]
    span = {tuple(sum(a * v[j] for a, v in zip(weights, basis)) % 7 for j in range(3))
            for weights in product(range(7), repeat=len(basis))}
    exponentials = {block_exp(problem, _matrix_from_coordinates(problem, v)) for v in span}
    finite_stabilizer = set()
    for values in product(range(7), repeat=3):
        g = _matrix_from_coordinates(problem, values, diagonal=1)
        log = block_log(problem, g)
        assert block_exp(problem, log) == g
        log_coordinates = tuple(log[i][j] for i, j in problem.lie_coordinates)
        preserves = _finite_invariant(g, linear, quadratic, 7)
        assert preserves == (log_coordinates in span)
        if preserves:
            finite_stabilizer.add(g)
    assert finite_stabilizer == exponentials
    assert len(finite_stabilizer) == 7 ** len(basis)
    assert result["finite_jet_stabilizer_order"] == {"base": 7, "exponent": len(basis)}
    generated, pending = {_identity(3)}, [_identity(3)]
    while pending:
        h = pending.pop()
        for g in result["jet_upper_generators"]:
            hg = tuple(tuple(sum(h[i][k] * g[k][j] for k in range(3)) % 7 for j in range(3))
                       for i in range(3))
            if hg not in generated:
                generated.add(hg)
                pending.append(hg)
    assert generated == finite_stabilizer


def test_product_blocks_keep_cross_block_quadratic_constraints():
    linear = [0] * 4
    quadratic = [[0, 0, 1, 0], [0, 0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0]]
    problem = _scalar_fixture(linear, quadratic, 2)
    result = analyze(problem)
    assert result["kernel_coordinates"] == [[0, 1], [2, 3]]
    finite = [g for v in product(range(7), repeat=2)
              if _finite_invariant(g := _matrix_from_coordinates(problem, v, 1), linear, quadratic, 7)]
    assert finite == [_identity(4)]
    assert result["kernel_dimension"] == 0
    assert result["full_stabilizer_identity_certified"]


@pytest.mark.parametrize("block_size", [2, 3, 4, 5])
@pytest.mark.parametrize("p", [7, (1 << 61) - 1])
def test_exp_log_round_trip_all_block_sizes_and_large_prime(block_size, p):
    problem = _instance(D=2 * block_size, block_size=block_size, p=p)
    rng = random.Random(19)
    values = [rng.randrange(p) for _ in problem.lie_coordinates]
    A = _matrix_from_coordinates(problem, values)
    g = _matrix_from_coordinates(problem, values, 1)
    assert block_log(problem, block_exp(problem, A)) == A
    assert block_exp(problem, block_log(problem, g)) == g


def test_p7_ut5_exactness_does_not_require_symmetric_square_degree_guard():
    B = [[(1 if i % 2 == 0 else 6) if i + j == 4 else 0 for j in range(5)] for i in range(5)]
    linear = [0, 0, 0, 0, 1]
    problem = _scalar_fixture(linear, B, 5)
    A = tuple(tuple(int(j == i + 1) for j in range(5)) for i in range(5))
    assert (sp.Matrix(A) ** 4)[0, 4] == 1
    assert all(int(x) % 7 == 0 for x in sp.Matrix(A).T * sp.Matrix(B) + sp.Matrix(B) * sp.Matrix(A))
    assert _finite_invariant(block_exp(problem, A), linear, B, 7)
    assert block_log(problem, block_exp(problem, A)) == A
    result = analyze(problem)
    assert result["kernel_dimension"] > 0
    for v in result["kernel_basis"]:
        assert _finite_invariant(block_exp(problem, _matrix_from_coordinates(problem, v)), linear, B, 7)
    # T=1 is already exact even when the sufficient propagation test fails.
    assert any(not check["ell_fixed"] for check in result["propagation_checks"])
    assert not result["all_upper_generators_propagate"]
    assert result["status"] == "CERTIFIED_FULL_STABILIZER"
    assert result["completion_reason"] == "EXACT_DEGREE_AT_MOST_TWO"
    assert result["full_stabilizer_generators"] == result["jet_upper_generators"]
    assert result["full_stabilizer_certified"]
    assert result["full_stabilizer_order"] == result["finite_jet_stabilizer_order"]


@pytest.mark.parametrize("field,value", [
    ("p", p) for p in [-7, 0, 2, 3, 5, 9, 25, True, 7.0, "7"]
] + [("block_size", b) for b in [0, 1, 2, 4, 5, 6, True, 3.0, "3"]]
  + [("T", T) for T in [-1, True, 1.0, "1", None]])
def test_rejects_malformed_prime_block_size_and_unary_T(field, value):
    data = _instance().specification()
    data[field] = value
    with pytest.raises(ValueError):
        QuadraticIteration(**data)


@pytest.mark.parametrize("field,value", [
    ("c", []), ("c", [0, 0]), ("c", None), ("c", "000"),
    ("A", []), ("A", [[0] * 3] * 2), ("A", [[0] * 2] * 3),
    ("B", []), ("B", [[[0] * 3] * 3] * 2), ("B", [[[0] * 2] * 3] * 3),
    ("ell", [0, 0]), ("ell", None), ("ell", "000"),
])
def test_rejects_malformed_coefficient_shapes(field, value):
    data = _instance().specification()
    data[field] = value
    with pytest.raises(ValueError):
        QuadraticIteration(**data)


@pytest.mark.parametrize("field", ["c", "A", "B", "ell"])
@pytest.mark.parametrize("value", [-1, 7, True, 1.5, "1", None])
def test_rejects_noncanonical_coefficients_without_coercion(field, value):
    data = _instance().specification()
    target = data[field]
    for _ in range({"c": 0, "ell": 0, "A": 1, "B": 2}[field]):
        target = target[0]
    target[0] = value
    with pytest.raises(ValueError, match="canonical"):
        QuadraticIteration(**data)


def test_rejects_asymmetric_B_and_freezes_mutable_inputs():
    data = _instance().specification()
    problem = QuadraticIteration(**data)
    data["c"][0] = (data["c"][0] + 1) % 7
    data["B"][0][0][1] = (data["B"][0][1][0] + 1) % 7
    assert problem.c != tuple(data["c"])
    assert problem.B[0][0][1] == problem.B[0][1][0]
    with pytest.raises(ValueError, match="symmetric"):
        QuadraticIteration(**data)


@pytest.mark.parametrize("function,diagonal", [(block_exp, 0), (block_log, 1)])
@pytest.mark.parametrize("location,value", [((0, 0), 2), ((1, 0), 1), ((0, 2), 1),
                                           ((0, 1), 7), ((0, 1), True)])
def test_exp_log_rejects_noncanonical_or_out_of_group_matrices(function, diagonal, location, value):
    problem = _instance(D=4, block_size=2)
    matrix = [[diagonal * int(i == j) for j in range(4)] for i in range(4)]
    matrix[location[0]][location[1]] = value
    with pytest.raises(ValueError):
        function(problem, matrix)


def test_zero_ell_is_rejected_by_native_input_contract():
    with pytest.raises(ValueError, match="nonzero ell"):
        replace(_instance(T=0), ell=(0, 0, 0))


@pytest.mark.parametrize("anchor", [(0, 0, 0), (4, 0, 0)])
def test_T0_exact_full_answer_does_not_require_propagation(anchor):
    problem = replace(_instance(T=0), ell=(1, 0, 0))
    result = analyze(problem, anchors=[anchor])
    assert result["kernel_dimension"] == 1
    assert result["full_stabilizer_order"] == result["finite_jet_stabilizer_order"] == {"base": 7, "exponent": 1}
    assert result["status"] == "CERTIFIED_FULL_STABILIZER"
    assert result["completion_reason"] == "EXACT_DEGREE_AT_MOST_TWO"
    assert result["full_stabilizer_certified"]
    assert not result["all_upper_generators_propagate"]
    assert not result["full_stabilizer_upper_bound_only"]
    assert result["full_stabilizer_generators"] == result["jet_upper_generators"]
    assert result["resources"]["jet_steps_executed"] == 0
    assert result["formal_degree_upper_bound"] == {"base": 2, "exponent": 0}


@pytest.mark.parametrize("anchor", [[], [0, 0], [0, 1, 0], [0, 0, 1], [-1, 0, 0],
                                   [7, 0, 0], [True, 0, 0], [1.0, 0, 0], "000"])
def test_rejects_noncanonical_or_not_whole_group_fixed_anchors(anchor):
    problem = _instance()
    with pytest.raises(ValueError):
        iterate_jet(problem, anchor)
    with pytest.raises(ValueError):
        analyze(problem, anchors=[anchor])


@pytest.mark.parametrize("anchors", [[], (), {}, "zero", [None]])
def test_rejects_empty_or_malformed_anchor_batches(anchors):
    with pytest.raises(ValueError):
        analyze(_instance(), anchors=anchors)


def test_fixed_anchor_uses_first_coordinate_of_each_block_only():
    problem = _instance(D=4, block_size=2, T=0)
    assert iterate_jet(problem, [2, 0, 3, 0]).v == (2, 0, 3, 0)
    with pytest.raises(ValueError, match="whole Gamma"):
        iterate_jet(problem, [2, 0, 0, 3])


@pytest.mark.parametrize("failed_check", [None, "constant_fixed", "linear_commutes", "quadratic_equivariant", "ell_fixed"])
def test_propagation_checks_each_public_coefficient_identity(failed_check):
    data = _instance().specification()
    data.update(c=[0, 0, 0], A=[list(row) for row in _identity(3)],
                B=[[[0] * 3 for _ in range(3)] for _ in range(3)], ell=[0, 0, 1])
    if failed_check == "constant_fixed":
        data["c"][1] = 1
    elif failed_check == "linear_commutes":
        data["A"][1][1] = 2
    elif failed_check == "quadratic_equivariant":
        data["B"][0][0][0] = 1
    elif failed_check == "ell_fixed":
        data["ell"] = [1, 0, 0]
    problem = QuadraticIteration(**data)
    g = ((1, 1, 0), (0, 1, 0), (0, 0, 1))
    checks = verify_propagation(problem, g)
    assert checks["passed"] == (failed_check is None)
    for key in ("constant_fixed", "linear_commutes", "quadratic_equivariant", "ell_fixed"):
        assert checks[key] == (key != failed_check)


def _symbolic_propagates(problem, g):
    x = sp.symbols(f"x0:{problem.D}")
    P = sp.Matrix([problem.c[i] + sum(problem.A[i][j] * x[j] for j in range(problem.D))
                   + sum(problem.B[i][j][k] * x[j] * x[k]
                         for j in range(problem.D) for k in range(problem.D))
                   for i in range(problem.D)])
    g = sp.Matrix(g)
    gx = g * sp.Matrix(x)
    composed = P.subs(dict(zip(x, gx)), simultaneous=True)
    return all(sp.Poly(value, *x, modulus=problem.p).is_zero for value in composed - g * P) and all(
        int(value) % problem.p == 0 for value in sp.Matrix([problem.ell]) * g - sp.Matrix([problem.ell]))


def test_quadratic_propagation_includes_output_mixing_not_individual_invariance():
    # P(x) = x_2*x is equivariant, but its first quadratic is not invariant.
    B = [[[0] * 3 for _ in range(3)] for _ in range(3)]
    B[0][0][2] = B[0][2][0] = B[1][1][2] = B[1][2][1] = 4
    B[2][2][2] = 1
    problem = QuadraticIteration(7, 3, 2, [0] * 3, _identity(3), B, [0, 0, 1])
    g = ((1, 1, 0), (0, 1, 0), (0, 0, 1))
    assert not _finite_invariant(g, [0] * 3, B[0], 7)
    assert verify_propagation(problem, g)["passed"]
    assert _symbolic_propagates(problem, g)


@pytest.mark.parametrize("block_size", [2, 3, 4, 5])
def test_exact_quadratic_propagation_with_cross_block_terms(block_size):
    D = 2 * block_size
    B = [[[0] * D for _ in range(D)] for _ in range(D)]
    for i in range(D - 1):
        B[i][i][D - 1] = B[i][D - 1][i] = 4
    B[-1][-1][-1] = 1
    # P(x) = (1+x_last)*x, with a Gamma-invariant scalar multiplier.
    problem = QuadraticIteration(7, block_size, 2, [0] * D, _identity(D), B, [0] * (D - 1) + [1])
    rng = random.Random(17)
    g = _matrix_from_coordinates(problem, [rng.randrange(7) for _ in problem.lie_coordinates], 1)
    assert verify_propagation(problem, g)["passed"]
    assert _symbolic_propagates(problem, g)


@pytest.fixture(scope="module")
def public_report():
    return report()


def test_report_is_deterministic_json_serializable_and_replayable(public_report):
    assert json.loads(json.dumps(public_report)) == public_report == report()
    assert public_report["proof_note"] == "research/ITERATED_QUADRATIC_JET_FILTER.md"
    assert len(public_report["cases"]) == 4
    for case in public_report["cases"]:
        assert set(case["input"]) == {"p", "block_size", "T", "c", "A", "B", "ell"}
        assert analyze(QuadraticIteration(**case["input"]), case["anchors"]) == {
            key: value for key, value in case.items() if key not in ("name", "seed")}
        resources = case["resources"]
        assert resources["T_encoding"] == "UNARY"
        assert resources["unary_iteration_units_charged"] == case["input"]["T"]
        assert resources["jet_steps_executed"] == len(case["anchors"]) * case["input"]["T"]
        assert resources["total_field_operations"] == "O(k (T+1) D^4) for block_size <= 5"
        assert resources["matrix_products"] == "Dense D-by-D loops, O(D^3) per product; no sparse multiplication"
        assert not resources["full_iterate_expanded"]
        assert not resources["finite_group_enumerated"]


def test_large_unary_iteration_bound_serializes_without_global_limit_changes():
    import sys
    limit_before = sys.get_int_max_str_digits()
    zero = ((0, 0), (0, 0))
    problem = QuadraticIteration(7, 2, 15000, (0, 0), _identity(2), (zero, zero), (1, 0))
    result = analyze(problem)
    assert result["formal_degree_upper_bound"] == {"base": 2, "exponent": 15000}
    assert json.loads(json.dumps(result)) == result
    assert sys.get_int_max_str_digits() == limit_before
    assert result["resources"]["jet_steps_executed"] == 15000
    assert result["full_stabilizer_order"] == {"base": 7, "exponent": 0}


def test_fixed_seed_dense_case_records_its_result_without_resampling(public_report):
    case = public_report["cases"][0]
    assert case["seed"] == 20261029
    assert (case["D"], case["input"]["block_size"], case["input"]["p"], case["input"]["T"]) == (10, 5, 101, 16)
    assert all(case["input"]["c"])
    assert all(value for row in case["input"]["A"] for value in row)
    assert case["finite_jet_stabilizer_exact"]
    assert case["full_stabilizer_identity_certified"] == (case["kernel_dimension"] == 0)
    assert case["formal_degree_upper_bound"] == {"base": 2, "exponent": 16}
    assert 2 ** 16 > 101


def test_large_degree_bound_near_identity_has_exact_trivial_certificate(public_report):
    case = public_report["cases"][1]
    problem = QuadraticIteration(**case["input"])
    assert (problem.D, problem.block_size, problem.p, problem.T) == (5, 5, 2 ** 61 - 1, 257)
    assert problem.A == problem.B[0] == _identity(5)
    assert problem.c == (0,) * 5 and problem.ell == (1, 0, 0, 0, 0)
    assert case["jet"]["constant"] == 0
    assert case["jet"]["linear"] == [1, 0, 0, 0, 0]
    assert case["jet"]["quadratic"] == [[257 * int(i == j) for j in range(5)] for i in range(5)]
    assert case["formal_degree_upper_bound"] == {"base": 2, "exponent": 257}
    assert 2 ** 257 > problem.p
    assert case["kernel_dimension"] == 0
    assert case["status"] == "CERTIFIED_TRIVIAL_FULL_STABILIZER"
    assert case["full_stabilizer_order"] == case["full_stabilizer_order_upper_bound"] == {"base": problem.p, "exponent": 0}
    assert case["full_stabilizer_generators"] == []
    assert case["completion_reason"] == "ZERO_JET_KERNEL"


def test_characteristic_cancellation_is_unknown_not_full_F_symmetry(public_report):
    case = public_report["cases"][2]
    problem = QuadraticIteration(**case["input"])
    assert problem.p == problem.T == 7
    assert case["jet"] == {"constant": 0, "linear": [1, 0, 0, 0, 0], "quadratic": [[0] * 5 for _ in range(5)]}
    assert case["kernel_dimension"] == 6
    assert case["status"] == "UNKNOWN_FULL_STABILIZER"
    assert case["full_stabilizer_order"] is None
    assert case["full_stabilizer_order_upper_bound"] == {"base": 7, "exponent": 6}
    assert case["full_stabilizer_upper_bound_only"]
    assert case["full_stabilizer_generators"] is None
    assert case["completion_reason"] is None
    assert len(case["jet_upper_generators"]) == 6
    assert not all(check["passed"] for check in case["propagation_checks"])

    # The shear y -> y+z preserves the jet but fails on the full iterate.
    values = [int(pair == (1, 2)) for pair in problem.lie_coordinates]
    g = block_exp(problem, _matrix_from_coordinates(problem, values))
    assert _finite_invariant(g, case["jet"]["linear"], case["jet"]["quadratic"], 7)

    # A formal degree-eight witness is essential: point evaluation can alias it.
    x, y, z = sp.symbols("x y z")
    a, b = sp.Poly(x, x, y, modulus=7), sp.Poly(y, x, y, modulus=7)

    def truncate(poly):
        return sp.Poly.from_dict({powers: c for powers, c in poly.terms() if sum(powers) <= 8},
                                 (x, y), modulus=7)

    for _ in range(7):
        a, b = truncate(a + b * b), truncate(b + a * a)
    assert a == sp.Poly(x - x ** 6 * y ** 2 + 2 * x ** 3 * y ** 5 - y ** 8, x, y, modulus=7)
    assert not sp.Poly(a.as_expr().subs(y, y + z) - a.as_expr(), x, y, z, modulus=7).is_zero


def test_non_characteristic_iteration_can_leave_all_fixed_anchor_jets_inconclusive():
    p, dimension = 11, 4
    linear = [list(row) for row in _identity(dimension)]
    linear[1][1] = 0
    forms = [[[0]*dimension for _ in range(dimension)] for _ in range(dimension)]
    forms[1][1][1] = 1
    problem = QuadraticIteration(p, dimension, 2, [0]*dimension,
                                  linear, forms, [0, 1, 0, 0])
    # P=(x0,x1^2,x2,x3), so ell(P^2)=x1^4; neither p-power iteration
    # nor ramification at T=p causes this incomplete low-order filter.
    full = _full_iterate(problem)[1]
    x = full.gens
    assert full == sp.Poly(x[1]**4, *x, modulus=p)
    anchors = [[a, 0, 0, 0] for a in range(p)]
    result = analyze(problem, anchors=anchors)
    assert result["kernel_dimension"] == 6
    assert result["status"] == "UNKNOWN_FULL_STABILIZER"
    assert result["full_stabilizer_generators"] is None
    assert all(jet["linear"] == [0]*dimension and
               jet["quadratic"] == [[0]*dimension for _ in range(dimension)]
               for jet in result["anchor_jets"])
    # This remains easy by direct algebra: a UT4 element replaces x1 by
    # x1+a*x2+b*x3. Characteristic 11 does not kill either linear coefficient.
    a, b = sp.symbols("a b")
    difference = sp.Poly((x[1]+a*x[2]+b*x[3])**4-x[1]**4, *x)
    assert difference.coeff_monomial(x[1]**3*x[2]) == 4*a
    assert difference.coeff_monomial(x[1]**3*x[3]) == 4*b
    assert difference.as_expr().subs({a: 0, b: 0}) == 0
    # Exact full stabilizer imposes two coordinate constraints, not all six.
    assert p**4 < p**result["kernel_dimension"]


def test_two_anchor_p7_case_is_complete_classical_stabilizer(public_report):
    case = public_report["cases"][3]
    problem = QuadraticIteration(**case["input"])
    assert case["input"] == public_report["cases"][2]["input"]
    assert case["anchors"] == [[0] * 5, [1, 0, 0, 0, 0]]
    assert [jet["linear"] for jet in case["anchor_jets"]] == [[1, 0, 0, 0, 0], [1, 2, 0, 0, 0]]
    assert case["kernel_dimension"] == 3
    assert case["status"] == "CERTIFIED_FULL_STABILIZER"
    assert case["completion_reason"] == "EXACT_QUADRATIC_PROPAGATION"
    assert case["full_stabilizer_order"] == case["full_stabilizer_order_upper_bound"] == {"base": 7, "exponent": 3}
    assert case["all_upper_generators_propagate"] and case["full_stabilizer_certified"]
    assert not case["full_stabilizer_upper_bound_only"]
    assert not case["full_stabilizer_identity_certified"]
    assert case["full_stabilizer_generators"] == case["jet_upper_generators"]
    expected = {_matrix_from_coordinates(problem, [int(pair == target) for pair in problem.lie_coordinates], 1)
                for target in ((2, 3), (2, 4), (3, 4))}
    assert {tuple(tuple(row) for row in g) for g in case["full_stabilizer_generators"]} == expected
    for g, check in zip(case["full_stabilizer_generators"], case["propagation_checks"]):
        assert check == verify_propagation(problem, g)
        assert all(check.values())
        assert _symbolic_propagates(problem, g)


def test_manual_p7_gradient_at_two_anchors_independent_of_tensor_recurrence(public_report):
    for start, expected in [(0, (1, 0)), (1, (1, 2))]:
        x, y, dx, dy = start, 0, (1, 0), (0, 1)
        for _ in range(7):
            dx, dy = (tuple((u + 2 * y * v) % 7 for u, v in zip(dx, dy)),
                      tuple((v + 2 * x * u) % 7 for u, v in zip(dx, dy)))
            x, y = (x + y * y) % 7, (y + x * x) % 7
        assert dx == expected
        assert public_report["cases"][3]["anchor_jets"][start]["linear"] == [*expected, 0, 0, 0]


def test_every_report_scope_flag_disclaims_quantum_and_hardness(public_report):
    for record in [public_report, *public_report["cases"]]:
        assert record["all_input_coefficients_public"]
        assert record["no_quantum_execution"] and record["no_advantage"]
        for flag in ("quantum_execution_performed", "quantum_advantage_claimed", "new_quantum_candidate",
                     "hardness_promises", "hardness_claimed", "unchecked_kernel_basis_claimed_as_full_F_symmetries",
                     "full_degree_guard_used", "actual_degree_claimed"):
            assert record[flag] is False
