from dataclasses import replace

import pytest
from sympy import Matrix, eye, symbols, zeros

from bielliptic import (
    SplitSextic, action, adjoint, alternating_form, analyze_pullback,
    apply_curve_lift, assemble_kernel, classify_involution, curve_point_key,
    discover_involutions, eigenspace_frame, embed_factors, matrix_key,
    even_elliptic_quotients, map_even_quotient, matrix_multiply, matrix_star,
    mod, point_key, product_actions, source_involution_geometry,
)
from audit_controls import (
    arithmetic_source, curve_control, order_four_control, rank_census,
    run_arithmetic, sl2_elements,
)
from residual import compatible_neighbor, nullspace, same_space
from residual_controls import OpaqueLabels, lagrangians, space_key


@pytest.mark.parametrize("prime", [7, 11, 13, 17, 2**127-1])
def test_discovery_includes_actual_even_involution_without_field_search(prime):
    curve, points, lifts = curve_control(prime)
    key = matrix_key(Matrix.diag(-1, 1), prime)
    found = next(x for x in lifts if x.matrix == key)
    assert found.status == "ELLIPTIC_INVOLUTION"
    assert found.lift_field_degree == 1
    assert len(lifts) <= 120
    assert all(curve.value(*p) == 0 for p in points)


def test_projective_order_two_is_not_curve_order_two():
    curve, lift = order_four_control()
    assert lift.status == "ORDER_FOUR_LIFT_NOT_SELF_ADJOINT"
    assert lift.kappa == 12 and lift.square_scalar == 1
    point = (1, 0, 1)
    once = apply_curve_lift(curve, lift, point, 5)
    twice = apply_curve_lift(curve, lift, once, 5)
    assert twice == (1, 0, 12)
    assert apply_curve_lift(curve, lift, apply_curve_lift(curve, lift, twice, 5), 5) == point


@pytest.mark.parametrize("p", [7, 13, 17])
def test_lift_on_every_small_rational_curve_point(p):
    curve, _, lifts = curve_control(p)
    lift = next(x for x in lifts if x.matrix == matrix_key(Matrix.diag(-1, 1), p))
    tested = 0
    for x, z in [(1, 0)] + [(x, 1) for x in range(p)]:
        for y in range(p):
            if y*y % p != curve.value(x, z):
                continue
            point = (x, z, y)
            mapped = apply_curve_lift(curve, lift, point, 1)
            assert mapped[2]**2 % p == curve.value(*mapped[:2])
            assert apply_curve_lift(curve, lift, mapped, 1) == point
            tested += 1
    assert tested >= 8


def test_branchpoint_at_infinity_and_changed_coordinate_frame():
    curve, points, lifts = curve_control(13)
    c = Matrix([[1, 1], [1, -1]])
    changed = tuple(point_key(c*Matrix(p), 13) for p in points)
    assert (1, 0) in changed
    moved = SplitSextic.from_branches(13, changed)
    found = discover_involutions(moved, changed)
    for lift in lifts:
        conjugate = c*Matrix(2, 2, lift.matrix)*c.inv_mod(13)
        transformed = next(x for x in found if x.matrix == matrix_key(conjugate, 13))
        assert transformed.status == lift.status


def test_rescaling_a_pgl_representative_does_not_change_lift_classification():
    curve, lift = order_four_control()
    for scale in range(1, 13):
        assert classify_involution(curve, scale*Matrix(2, 2, lift.matrix)) == lift


def test_quadratic_lift_field_is_reported_not_assumed():
    # x -> 2/x has two fixed points only in F_11^2. Three other
    # length-two orbits supply a branch-free fixed-point involution.
    points = tuple((x, 1) for x in (0, 1, 2, 3, 8)) + ((1, 0),)
    curve = SplitSextic.from_branches(11, points)
    lift = classify_involution(curve, Matrix([[0, 2], [1, 0]]))
    assert lift.status == "ELLIPTIC_INVOLUTION"
    assert lift.lift_field_degree == 2
    with pytest.raises(ValueError, match="square root"):
        apply_curve_lift(curve, lift, (0, 1, 0), 1)


@pytest.mark.parametrize("coefficients", [
    (1, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 1),
    (0, 0, 1, 0, 0, 0, 1), (1, 2),
])
def test_bad_curves_rejected(coefficients):
    with pytest.raises(ValueError):
        SplitSextic(13, coefficients)


def test_bad_fields_points_maps_and_metadata_rejected():
    for p in (2, 9, 15):
        with pytest.raises(ValueError):
            SplitSextic.from_branches(p, [(x, 1) for x in range(6)])
    curve, points, lifts = curve_control(13)
    for invalid in (points[:5], points[:5]+points[:1], points[:5]+((0, 1),)):
        with pytest.raises(ValueError):
            discover_involutions(curve, invalid)
    for m in (eye(2), zeros(2), Matrix([[1, 1], [0, 1]]), Matrix([[0, 2], [1, 0]])):
        with pytest.raises(ValueError):
            classify_involution(curve, m)
    lift = next(x for x in lifts if x.matrix == matrix_key(Matrix.diag(-1, 1), 13))
    with pytest.raises(ValueError, match="metadata"):
        apply_curve_lift(curve, replace(lift, kappa=2), (1, 0, 1), 1)
    with pytest.raises(ValueError, match="not on"):
        apply_curve_lift(curve, lift, (1, 0, 0), 1)


def test_explicit_even_model_elliptic_quotients_symbolically():
    x, a, b, c = symbols("x a b c", nonzero=True)
    f = x**6+a*x**4+b*x**2+c
    plus_x = x**2
    minus_x = c/x**2
    assert (plus_x**3+a*plus_x**2+b*plus_x+c-f).expand() == 0
    assert (minus_x**3+b*minus_x**2+a*c*minus_x+c*c-c*c*f/x**6).expand() == 0


@pytest.mark.parametrize("p,scale", [(13, 1), (13, 2), (17, 3)])
def test_paid_quotient_maps_on_actual_points_including_infinities(p, scale):
    original, _, _ = curve_control(p)
    curve = SplitSextic(p, tuple(scale*c % p for c in original.coefficients))
    quotients = even_elliptic_quotients(curve)
    for x, z in [(1, 0)] + [(x, 1) for x in range(p)]:
        for y in range(p):
            if y*y % p != curve.value(x, z):
                continue
            for side in (0, 1):
                output = map_even_quotient(curve, (x, z, y), side)
                if output is not None:
                    u, v = output
                    assert v*v % p == sum(a*pow(u, i, p) for i, a in enumerate(quotients[side])) % p
                involution = (-x, z, y if side == 0 else -y)
                assert map_even_quotient(curve, involution, side) == output


def test_rank_zero_source_exchange_yields_two_degree_ell_maps_in_control():
    source, _, result = run_arithmetic("stable_swap")
    split = result.source_split
    assert split.kind == "UNITARY_EXCHANGE"
    assert split.polarization_multiplier == 2
    order, one = source.order, source.order.unit
    # The product-target fixture has quotient rows (1,1) and (1,-1).
    # This is a degree/diagram control, NOT a genus-two native execution.
    quotient = Matrix.vstack(one, one, one, -one)
    restricted = matrix_multiply(order, matrix_multiply(order, quotient, source.phi), split.embeddings)
    assert all(int(c) % 2 == 0 for c in restricted)
    elliptic = restricted/2
    assert elliptic[4:12, :] == zeros(8, 1)
    assert elliptic[:4, :] == Matrix([1, 2, 0, 0])
    assert elliptic[12:, :] == Matrix([1, -2, 0, 0])
    for psi in (elliptic[:4, :], elliptic[12:, :]):
        assert order.multiply(order.star(psi), psi) == 5*one
    identity = Matrix.vstack(one, zeros(4, 1), zeros(4, 1), one)
    assert matrix_multiply(order, matrix_star(order, split.embeddings), split.embeddings) == 2*identity
    assert matrix_multiply(order, source.phi, split.embeddings) == matrix_multiply(
        order, matrix_star(order, quotient), elliptic)


@pytest.mark.parametrize("d", [3, 7, 4, 8, 12])
def test_common_mask_survives_division_by_two_at_odd_and_even_levels(d):
    from math import gcd
    psi = Matrix([[1, -2], [2, 1]])
    point = Matrix([1, 0])
    if d % 2:
        mask = next(x for x in range(2, d+2) if gcd(x, d) == 1)
        response = mod(mask*2*psi*point, d)
        assert mod(pow(2, -1, d)*response, d) == mod(mask*psi*point, d)
    else:
        level = 2*d
        mask = next(x for x in range(2, level+2) if gcd(x, level) == 1)
        # Coordinates in T_d embed as twice those coordinates in T_(2d).
        for first in (0, 1):
            for second in (0, 1):
                preimage = point+d*Matrix([first, second])
                response = mod(mask*2*psi*preimage, level)
                assert all(int(x) % 2 == 0 for x in response)
                assert mod(response/2, d) == mod(mask*psi*point, d)


@pytest.mark.parametrize("sign", [1, -1])
def test_diagonal_involution_forces_product_target(sign):
    source = arithmetic_source("stable_swap")
    one, zero = source.order.unit, zeros(4, 1)
    split = source_involution_geometry(source.order, Matrix.vstack(sign*one, zero, zero, -sign*one))
    assert split.kind == "DIAGONAL_SIGN_PRODUCT_TARGET_ONLY"
    assert not split.smooth_jacobian_target_possible
    assert split.polarization_multiplier == 1


@pytest.mark.parametrize("unit_coordinates", [(1, 0, 0, 0), (-1, 0, 0, 0),
                                              (0, 1, 0, 0), (0, -1, 0, 0)])
def test_exchange_embeddings_keep_the_actual_quaternion_unit(unit_coordinates):
    source = arithmetic_source("stable_swap")
    order, one, zero = source.order, source.order.unit, zeros(4, 1)
    u = Matrix(unit_coordinates)
    beta = Matrix.vstack(zero, u, order.star(u), zero)
    split = source_involution_geometry(order, beta)
    signs = Matrix.vstack(one, zero, zero, -one)
    assert matrix_multiply(order, beta, split.embeddings) == matrix_multiply(order, split.embeddings, signs)
    assert split.kind == "UNITARY_EXCHANGE"


@pytest.mark.parametrize("ell", [3, 5, 7])
def test_exhaustive_rank_dichotomy(ell):
    assert rank_census(ell) == {0: (ell+1)**2, 1: 0, 2: ell*(ell*ell-1)}


@pytest.mark.parametrize("kind,rank", [("mixing", 2), ("stable_swap", 0)])
def test_access_matched_crt_then_classification(kind, rank):
    source, recovered, result = run_arithmetic(kind)
    assert recovered.coordinates == source.reference_pullbacks()
    assert source.calls == list(recovered.primes)
    assert recovered.weak_basis_points_required == 4*len(source.calls)
    assert recovered.target_basis_points_required == 4*len(source.calls)
    assert result.image.cols == rank
    assert not result.geometric_input_verified
    assert not result.quantum_receiver_executed
    actual = nullspace(action(source.phi, product_actions(source.split(source.ell))), source.ell)
    if rank:
        assert same_space(actual, result.image, source.ell)
        assert result.compatible_lagrangian_count == 1
    else:
        beta = recovered.coordinates[0]/source.ell
        assert result.beta_coordinates == beta
        assert result.compatible_lagrangian_count == 36
        assert result.status == "TWO_HIDDEN_LINES_NOT_CLASSICALLY_SOLVED"
        operators = product_actions(source.split(source.ell))
        assert same_space(actual, action(beta, operators)*actual, source.ell)


@pytest.mark.parametrize("ell", [3, 5, 7])
def test_residual_candidates_exactly_match_neighbor_integrality(ell):
    beta = Matrix.diag(1, 1, -1, -1)
    count = 0
    for kernel in lagrangians(ell):
        invariant = same_space(kernel, beta*kernel, ell)
        assert compatible_neighbor(ell*beta, kernel, ell) == invariant
        if invariant:
            count += 1
            assert nullspace(Matrix.hstack(kernel, -eye(4)[:, :2]), ell).cols == 1
    assert count == (ell+1)**2


def test_two_actual_factor_restrictions_preserve_label_collisions():
    source, _, result = run_arithmetic("stable_swap")
    actual = nullspace(action(source.phi, product_actions(source.split(5))), 5)
    coordinates = mod(result.frame.inv_mod(5)*actual, 5)
    plus = next(coordinates[:2, j] for j in range(2) if coordinates[:2, j] != zeros(2, 1))
    minus = next(coordinates[2:, j] for j in range(2) if coordinates[2:, j] != zeros(2, 1))
    assert same_space(assemble_kernel(result, plus, minus), actual, 5)
    for side, line in enumerate((plus, minus)):
        oracle = OpaqueLabels(actual, 5)
        forward, backward = {}, {}
        for matrix in sl2_elements(5):
            args = (matrix, eye(2)) if side == 0 else (eye(2), matrix)
            label = oracle(embed_factors(result, *args))
            key = space_key(matrix*line, 5)
            assert label not in forward or forward[label] == key
            assert key not in backward or backward[key] == label
            forward[label], backward[key] = key, label
        assert len(forward) == len(backward) == 6
        assert oracle.calls == 120


def test_frame_is_not_a_hidden_line_answer_and_scalar_involution_rejected():
    source, _, result = run_arithmetic("stable_swap")
    keys = set()
    lines = [Matrix([1, 0])] + [Matrix([x, 1]) for x in range(5)]
    for plus in lines:
        for minus in lines:
            keys.add(space_key(assemble_kernel(result, plus, minus), 5))
    assert len(keys) == 36
    unit = Matrix.vstack(source.order.unit, zeros(4, 1), zeros(4, 1), source.order.unit)
    with pytest.raises(ValueError, match="trace zero"):
        analyze_pullback(source.order, 5, source.split(5), 5*unit)


def test_bad_pullbacks_and_illegal_GL_extension_rejected():
    source, reconstruction, result = run_arithmetic("stable_swap")
    alpha = reconstruction.coordinates[0]
    for invalid in (alpha/2, 2*alpha):
        with pytest.raises(ValueError):
            analyze_pullback(source.order, 5, source.split(5), invalid)
    with pytest.raises(ValueError, match="self-adjoint"):
        analyze_pullback(source.order, 5, source.split(5), eye(16)[:, 1])
    with pytest.raises(ValueError, match="GL2 extension"):
        embed_factors(result, Matrix.diag(2, 1), eye(2))
    with pytest.raises(ValueError, match="nonzero"):
        assemble_kernel(result, zeros(2, 1), Matrix([1, 0]))
    with pytest.raises(ValueError):
        embed_factors(replace(result, frame=2*eye(4)), eye(2), eye(2))


@pytest.mark.parametrize("ell", [3, 5, 2**127-1])
def test_public_symplectic_coordinate_changes_and_large_prime(ell):
    j = alternating_form(2)
    v = Matrix([1, 3, 2, 4])
    t = mod(eye(4)+v*v.T*j, ell)
    beta = mod(t*Matrix.diag(1, 1, -1, -1)*t.inv_mod(ell), ell)
    frame = eigenspace_frame(beta, ell)
    assert mod(frame.T*j*frame, ell) == mod(j, ell)
    assert mod(frame.inv_mod(ell)*beta*frame, ell) == mod(Matrix.diag(1, 1, -1, -1), ell)
    with pytest.raises(ValueError):
        eigenspace_frame(eye(4), ell)
