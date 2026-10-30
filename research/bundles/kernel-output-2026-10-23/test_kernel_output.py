import pytest
from sympy import Matrix, Rational, eye, zeros
from sympy.matrices.normalforms import hermite_normal_form

from kernel_output import (
    action, adapted_basis, check_split, column_actions, coordinate_map,
    flat, hurwitz_order, hurwitz_split, inverse_mod, is_lagrangian,
    integer_matrix, lift_split, matrix_multiply, matrix_on_column, matrix_star, mod,
    module_pairing, odd_maximal_order, odd_maximal_split, order_from_module,
    product_actions, reconstruct, weak_endomorphism_action,
)


def kernel(s=0, t=0, u=0):
    return Matrix([[1, 0], [s, t], [0, 1], [t, u]])


@pytest.fixture(scope="module")
def order():
    return hurwitz_order()


def integral(a):
    return all(x.q == 1 for x in a)


@pytest.mark.parametrize("ell", [3, 5, 7, 13, 17, 31])
def test_split_lift_preserves_all_products_and_star(order, ell):
    split = hurwitz_split(ell)
    lifted = lift_split(order, split, ell)
    check_split(order, lifted, ell*ell)
    assert all(mod(a-b, ell) == zeros(2) for a, b in zip(split, lifted))


@pytest.mark.parametrize("ell,s,t,u", [(3, 0, 0, 0), (3, 1, 2, 1), (5, 2, 4, 3), (7, 4, 2, 5)])
def test_full_order_and_module_structure(order, ell, s, t, u):
    out = reconstruct(order, hurwitz_split(ell), kernel(s, t, u), ell)
    assert abs(out.module_numerator.det()) == ell**4
    assert abs(out.order_numerator.det()) == ell**16
    assert abs(out.order_basis.det()) == 1
    assert out.contains_order(Matrix.vstack(order.unit, zeros(4, 1), zeros(4, 1), order.unit))
    m, r = out.module_basis, out.order_basis
    mi, ri = m.inv(), r.inv()
    gram = zeros(8)
    for i in range(8):
        for j in range(8):
            h = module_pairing(order, m[:, i], m[:, j], ell)
            assert integral(h)
            gram[i, j] = (order.traces*h)[0]
        for b in range(4):
            right = Matrix.vstack(*(order.multiply(m[4*k:4*k+4, i], eye(4)[:, b]) for k in range(2)))
            assert integral(mi*right)
    assert gram == gram.T
    assert gram.det() == 16  # Quaternion Hermitian unimodularity is not trace-lattice determinant 1.
    assert all(gram[:i, :i].det() > 0 for i in range(1, 9))
    for i in range(16):
        assert integral(ri*matrix_star(order, r[:, i]))
        for j in range(8):
            assert integral(mi*matrix_on_column(order, r[:, i], m[:, j]))
        for j in range(16):
            assert integral(ri*matrix_multiply(order, r[:, i], r[:, j]))


@pytest.mark.parametrize("ell", [3, 5, 13])
def test_lift_complement_and_kernel_basis_do_not_change_lattice(order, ell):
    split, k = hurwitz_split(ell), kernel(2, 1, 3)
    reference = reconstruct(order, split, k, ell)
    p = adapted_basis(k, ell)
    changed_split = lift_split(order, split, ell, Matrix([2, -1, 5, 3]))
    lifts = [
        reconstruct(order, split, k*Matrix([[1, 3], [0, 1]]), ell),
        reconstruct(order, split, k+ell*Matrix([[4, -1], [0, 3], [1, 2], [5, 7]]), ell),
        reconstruct(order, split, k, ell, complement=p[:, 2:]+k*Matrix([[1, 4], [3, 2]])),
        reconstruct(order, split, k, ell, split_squared=changed_split),
    ]
    # An arbitrary inner change congruent to I modulo ell is another compatible lift.
    v = eye(2)+ell*Matrix([[0, 3], [1, 0]])
    conjugated = tuple(mod(v*a*inverse_mod(v, ell*ell), ell*ell) for a in reference.split_squared)
    lifts.append(reconstruct(order, split, k, ell, split_squared=conjugated))
    for out in lifts:
        assert out.module_numerator == reference.module_numerator
        assert out.order_numerator == reference.order_numerator


@pytest.mark.parametrize("p", [2, 11])
def test_actual_quaternion_isogeny_gives_exact_transported_lattices(p):
    ell = 13
    order = hurwitz_order() if p == 2 else odd_maximal_order(p)
    split = hurwitz_split(ell) if p == 2 else odd_maximal_split(p, ell)
    alpha, conjugate = Matrix([3, 2, 0, 0]), Matrix([3, -2, 0, 0])
    phi = Matrix.vstack(alpha, zeros(4, 1), zeros(4, 1), conjugate)
    dual = matrix_star(order, phi)
    identity = Matrix.vstack(order.unit, zeros(4, 1), zeros(4, 1), order.unit)
    assert matrix_multiply(order, dual, phi) == ell*identity
    image = mod(action(phi, product_actions(split)), ell)
    columns = []
    for block in [0, 2]:
        vector = next(Matrix([1, z]) for z in range(ell)
                      if mod(image[block:block+2, block:block+2]*Matrix([1, z]), ell) == zeros(2, 1))
        v = zeros(4, 1)
        v[block:block+2, :] = vector
        columns.append(v)
    out = reconstruct(order, split, Matrix.hstack(*columns), ell)
    expected_module = Matrix.hstack(*(matrix_on_column(order, dual, eye(8)[:, i]) for i in range(8)))
    expected_order = Matrix.hstack(*(matrix_multiply(order, matrix_multiply(order, dual, eye(16)[:, i]), phi)
                                    for i in range(16)))
    assert out.module_numerator == hermite_normal_form(integer_matrix(expected_module))
    assert out.order_numerator == hermite_normal_form(integer_matrix(expected_order))
    for i in range(8):
        y = out.module_basis[:, i]
        represented = matrix_on_column(order, phi, y)
        assert integral(represented)
        assert module_pairing(order, y, y, ell) == module_pairing(order, represented, represented, 1)


def test_mod_ell_only_order_shortcuts_are_wrong(order):
    ell = 5
    k = kernel()
    out = reconstruct(order, hurwitz_split(ell), k, ell)
    p = adapted_basis(k, ell)
    wrong = zeros(4)
    wrong[2, 0] = ell
    wrong = mod(p*wrong*inverse_mod(p, ell*ell), ell*ell)
    coefficients = mod(inverse_mod(coordinate_map(product_actions(out.split_squared)), ell*ell)*flat(wrong), ell*ell)
    assert mod(wrong, ell) == zeros(4)
    assert not out.contains_order(coefficients/ell)
    identity = Matrix.vstack(order.unit, zeros(4, 1), zeros(4, 1), order.unit)
    assert not out.contains_order(identity/ell)


def test_non_lagrangian_breaks_polarized_output(order):
    ell, bad = 5, eye(4)[:, :2]
    assert not is_lagrangian(bad, ell)
    with pytest.raises(ValueError, match="Lagrangian"):
        reconstruct(order, hurwitz_split(ell), bad, ell)
    out = reconstruct(order, hurwitz_split(ell), bad, ell, require_lagrangian=False)
    m, r = out.module_basis, out.order_basis
    assert any(not integral(module_pairing(order, m[:, i], m[:, j], ell))
               for i in range(8) for j in range(8))
    assert any(not out.contains_order(matrix_star(order, r[:, i])) for i in range(16))


@pytest.mark.parametrize("level", [3, 9, 7, 49])
def test_common_weak_units_cancel_but_independent_masks_do_not(level):
    ell = 5
    a = Matrix([[1, 1, 0, 0], [0, 0, 2, 0], [1, 0, 1, 1], [0, 1, 0, 2]])
    phi = Matrix([[1, 2, 0, 0], [0, 1, 0, 0], [0, 0, 1, 3], [0, 0, 0, 1]])
    exact = mod(pow(ell, -1, level)*phi*a*inverse_mod(phi, level), level)
    for unit in range(1, level):
        if unit % (3 if level in (3, 9) else 7):
            assert weak_endomorphism_action(a, unit*phi, ell, level) == exact
    assert weak_endomorphism_action(a, phi*Matrix.diag(-1, 1, 1, 1), ell, level) != exact


def test_large_prime_has_fixed_lattice_rank(order):
    ell = 2**127-1
    # A bounded explicit fixture search, not an inferred runtime theorem.
    a, b = next((a, pow((-1-a*a) % ell, (ell+1)//4, ell)) for a in range(100)
                if pow((-1-a*a) % ell, (ell-1)//2, ell) == 1)
    i, j = Matrix([[0, -1], [1, 0]]), Matrix([[a, b], [b, -a]])
    split = tuple(mod(x, ell) for x in (eye(2), i, j, (eye(2)+i+j+i*j)*pow(2, -1, ell)))
    out = reconstruct(order, split, kernel(17, ell-7, 45), ell)
    assert out.module_numerator.shape == (8, 8)
    assert out.order_numerator.shape == (16, 16)
    assert out.module_numerator.det() == ell**4
    assert out.order_numerator.det() == ell**16


@pytest.mark.parametrize("ell", [3, 5, 13, 31])
def test_independent_module_left_order_matches_prime_square_congruences(order, ell):
    out = reconstruct(order, hurwitz_split(ell), kernel(2, 1, 4), ell)
    assert order_from_module(order, out.module_numerator, ell) == out.order_numerator


@pytest.mark.parametrize("p,ell", [(3, 5), (7, 13), (11, 3), (19, 7)])
def test_odd_characteristic_full_maximal_order(p, ell):
    order = odd_maximal_order(p)
    split = odd_maximal_split(p, ell)
    for row in order.products:
        assert all(integral(x) for x in row)
    trace_gram = Matrix(4, 4, lambda i, j:
                        (order.traces*order.multiply(order.star(eye(4)[:, i]), eye(4)[:, j]))[0])
    assert trace_gram.det() == p*p
    out = reconstruct(order, split, kernel(1, 2, 3), ell)
    assert order_from_module(order, out.module_numerator, ell) == out.order_numerator
    gram = Matrix(8, 8, lambda i, j:
                  (order.traces*module_pairing(order, out.module_basis[:, i], out.module_basis[:, j], ell))[0])
    assert gram.det() == p**4
    assert all(gram[:i, :i].det() > 0 for i in range(1, 9))
    assert all(out.contains_order(matrix_star(order, out.order_basis[:, i])) for i in range(16))


@pytest.mark.parametrize("bad", [2, 4, 9, 15])
def test_invalid_prime_rejected(order, bad):
    with pytest.raises(ValueError):
        reconstruct(order, hurwitz_split(3), kernel(), bad)


def test_malformed_inputs_rejected(order):
    with pytest.raises(ValueError, match="independent"):
        reconstruct(order, hurwitz_split(5), zeros(4, 2), 5)
    with pytest.raises(ValueError, match="integral"):
        mod(Matrix([[Rational(1, 2)]]), 5)
    with pytest.raises(ValueError, match="coprime"):
        weak_endomorphism_action(eye(4), eye(4), 5, 25)
    with pytest.raises(ValueError):
        lift_split(order, (eye(2),)*4, 5)
    lifted = list(lift_split(order, hurwitz_split(5), 5))
    lifted[1] = mod(lifted[1]+5*eye(2), 25)
    with pytest.raises(ValueError):
        reconstruct(order, hurwitz_split(5), kernel(), 5, split_squared=lifted)


def test_composite_auxiliary_level_with_no_unit_pivot():
    w = Matrix.diag(Matrix([[2, 3], [3, 2]]), eye(2))
    assert mod(w*inverse_mod(w, 6), 6) == eye(4)
    a = eye(4)
    a[1, 2] = 1
    assert weak_endomorphism_action(a, -w, 5, 6) == weak_endomorphism_action(a, w, 5, 6)
