"""Exact access-loss controls, not a new oracle-search problem or native solver."""

from itertools import product
from functools import reduce
from math import gcd
from pathlib import Path
import sys

from sympy import GF, Matrix, eye, isprime, zeros
from sympy.polys.matrices import DomainMatrix

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "kernel-output-2026-10-23"))
sys.path.insert(0, str(ROOT / "native-membership-baseline-2026-10-25"))
from kernel_output import action, flat, inverse_mod, mod, odd_maximal_order, odd_maximal_split
from controls_membership import conjugate, rational_mod


def _prime(prime):
    if type(prime) is not int or prime <= 2 or not isprime(prime):
        raise ValueError("odd prime required for these finite controls")


def column_basis(matrix, prime):
    _, pivots = DomainMatrix.from_Matrix(Matrix(matrix)).convert_to(GF(prime)).rref()
    return mod(Matrix(matrix)[:, list(pivots)], prime)


def matrix_algebra(generators, prime):
    """Finite linear closure; explicit dimension is charged, not scalable advice."""
    _prime(prime)
    generators = tuple(Matrix(x) for x in generators)
    if not generators or any(x.shape != generators[0].shape for x in generators):
        raise ValueError("nonempty equal-size matrix generators required")
    size = generators[0].rows
    if size != generators[0].cols:
        raise ValueError("square generators required")
    basis = [eye(size)]
    while True:
        candidates = basis+[mod(a*b, prime) for a in generators for b in basis]
        columns = column_basis(Matrix.hstack(*(flat(x) for x in candidates)), prime)
        if columns.cols == len(basis):
            return tuple(Matrix(size, size, list(columns[:, j])) for j in range(columns.cols))
        basis = [Matrix(size, size, list(columns[:, j])) for j in range(columns.cols)]


def commutant(generators, prime):
    _prime(prime)
    generators = tuple(Matrix(x) for x in generators)
    if not generators or any(x.shape != generators[0].shape for x in generators):
        raise ValueError("nonempty equal-size generators required")
    size = generators[0].rows
    if size != generators[0].cols:
        raise ValueError("square matrices required")
    units = [Matrix(size, size, [int(i == j) for i in range(size*size)])
             for j in range(size*size)]
    constraints = Matrix.vstack(*[Matrix.hstack(*(flat(a*u-u*a) for u in units))
                                 for a in generators])
    kernel = mod(DomainMatrix.from_Matrix(constraints).convert_to(GF(prime))
                 .nullspace().to_Matrix().T, prime)
    return tuple(Matrix(size, size, list(kernel[:, j])) for j in range(kernel.cols))


def projective_centralizer_count(alpha, prime):
    """Enumerative finite falsifier; never an algorithm polynomial in log(r)."""
    if prime > 101:
        raise ValueError("small-prime enumeration cap exceeded")
    central = commutant((alpha,), prime)
    if len(central) != 2:
        raise ValueError("nonscalar two-dimensional cyclic action required")
    representatives = set()
    for coefficients in product(range(prime), repeat=2):
        matrix = mod(sum((c*a for c, a in zip(coefficients, central)), zeros(2)), prime)
        if matrix.det() % prime == 0:
            continue
        first = next(int(x) for x in matrix if x)
        representatives.add(tuple(mod(pow(first, -1, prime)*matrix, prime)))
    return len(representatives)


def stabilized_controls(prime, copies):
    _prime(prime)
    if copies not in (1, 2, 3):
        raise ValueError("bounded exact control supports one to three copies")
    alpha = odd_maximal_split(11, prime)[1]
    generators = []
    for i in range(copies):
        for j in range(copies):
            elementary = zeros(copies)
            elementary[i, j] = 1
            generators.append(Matrix.vstack(*[
                Matrix.hstack(*[int(elementary[r, s])*eye(2) for s in range(copies)])
                for r in range(copies)]))
    generators.append(Matrix.diag(*([alpha]*copies)))
    algebra, central = matrix_algebra(generators, prime), commutant(generators, prime)
    assert len(algebra) == 2*copies*copies
    assert len(central) == 2
    return {"prime": prime, "copies": copies, "generated_algebra_dimension": len(algebra),
            "full_algebra_dimension": 4*copies*copies, "commutant_dimension": len(central),
            "projective_ambiguity_removed": False}


def frobenius_product_control(prime):
    """Natural twisted diagonal and Frobenius/dual arrows on E x E^(p)."""
    split, p = odd_maximal_split(11, prime), 11
    alpha, frobenius = split[1], mod(2*split[2]-eye(2), prime)
    conjugate_alpha = mod(frobenius*alpha*inverse_mod(frobenius, prime), prime)
    assert mod(conjugate_alpha+alpha, prime) == zeros(2)
    first, second = Matrix.diag(eye(2), zeros(2)), Matrix.diag(zeros(2), eye(2))
    forward, dual = zeros(4), zeros(4)
    forward[2:, :2] = frobenius
    dual[:2, 2:] = mod(p*inverse_mod(frobenius, prime), prime)
    generators = (first, second, Matrix.diag(alpha, conjugate_alpha), forward, dual)
    algebra, central = matrix_algebra(generators, prime), commutant(generators, prime)
    assert len(algebra) == 8 and len(central) == 2
    return {"prime": prime, "characteristic": p, "generated_algebra_dimension": 8,
            "full_algebra_dimension": 16, "commutant_dimension": 2,
            "natural_twist_relation_checked": True, "actual_curve_backend_executed": False}


def same_degree_ambiguity_control(prime):
    """h=(1+j)/2 and 1-h: genuine supplied degree-three maps in characteristic11."""
    order, split = odd_maximal_order(11), odd_maximal_split(11, prime)
    h, hbar = eye(4)[:, 2], order.unit-eye(4)[:, 2]
    assert order.multiply(order.star(h), h) == 3*order.unit
    assert order.multiply(order.star(hbar), hbar) == 3*order.unit
    if prime in (3, 11):
        raise ValueError("auxiliary prime must avoid the common degree and characteristic")
    first, second, alpha = (mod(action(x, split), prime) for x in (h, hbar, h))
    assert mod(first*alpha-alpha*first, prime) == zeros(2)
    assert mod(second*alpha-alpha*second, prime) == zeros(2)
    ratio = mod(inverse_mod(first, prime)*second, prime)
    nonscalar = ratio[0, 1] != 0 or ratio[1, 0] != 0 or ratio[0, 0] != ratio[1, 1]
    assert nonscalar
    # The original degree-three kernels are distinct, checked at their degree.
    at_three = odd_maximal_split(11, 3)
    h3, bar3 = (mod(action(x, at_three), 3) for x in (h, hbar))
    assert h3.det() % 3 == bar3.det() % 3 == 0
    assert column_basis(Matrix.vstack(h3, bar3), 3).cols == 2
    transverse = eye(4)[:, 1]
    first_image, second_image = (rational_mod(action(conjugate(order, x, transverse), split), prime)
                                 for x in (h, hbar))
    assert first_image != second_image
    from kernel_output import matrix_multiply, matrix_star
    zero, one = zeros(4, 1), order.unit
    identity = Matrix.vstack(one, zero, zero, one)
    sigma = Matrix.vstack(one, 6*transverse, zero, one)
    gram = matrix_multiply(order, matrix_star(order, sigma), sigma)
    transported = []
    for phi in (h, hbar):
        doubled = Matrix.vstack(phi, zero, zero, phi)
        image = matrix_multiply(order, matrix_multiply(order, doubled, gram),
                                matrix_star(order, doubled))/3
        assert all(x.q == 1 for x in (image-identity)/2)
        transported.append(image)
    assert transported[0] != transported[1]
    return {"prime": prime, "common_degree": 3, "same_known_quadratic_action": True,
            "maps_differ_by_nonscalar_centralizer": True,
            "original_degree_three_kernels_distinct": True,
            "transport_of_transverse_operator_differs": True,
            "transported_integral_gram_operators_differ": True,
            "both_half_polarizations_integral": True,
            "supplied_global_endomorphisms": True, "native_hardness_claim": False}


def unbounded_primitive_family_control():
    """h^k, h=(1+j)/2, all commute with the SAME fixed input h."""
    order, h = odd_maximal_order(11), eye(4)[:, 2]
    assert order.multiply(h, h)-h+3*order.unit == zeros(4, 1)
    at_three = mod(action(h, odd_maximal_split(11, 3)), 3)
    assert at_three != zeros(2) and mod(at_three*at_three-at_three, 3) == zeros(2)
    records, value = [], order.unit
    for exponent in range(1, 65):
        value = order.multiply(value, h)
        if exponent not in (1, 2, 4, 8, 16, 32, 64):
            continue
        degree = 3**exponent
        assert order.multiply(order.star(value), value) == degree*order.unit
        assert reduce(gcd, (abs(int(x)) for x in value)) == 1
        assert order.multiply(value, h) == order.multiply(h, value)
        records.append({"exponent": exponent, "degree": degree,
                        "primitive_integral_map": True, "same_fixed_quadratic_input": True})
    return {"fixed_known_endomorphism": "h=(1+j)/2, j^2=-11", "controls": records,
            "bound_on_every_primitive_intertwiner_from_fixed_input": False,
            "minimal_degree_intertwiner_lower_bound_claim": False,
            "scope": "counterexample to a universal bound, not to choosing a small representative"}


def gram_nonclosure_control():
    """Gram-in-K integral automorphisms do not form a query group."""
    from kernel_output import matrix_multiply, matrix_star
    order = odd_maximal_order(11)
    one, i, j = order.unit, eye(4)[:, 1], 2*eye(4)[:, 2]-order.unit
    zero = zeros(4, 1)
    unitary = Matrix.vstack(i, zero, zero, one)
    shear = Matrix.vstack(one, one, zero, one)
    combined = matrix_multiply(order, shear, unitary)

    def gram(value):
        return matrix_multiply(order, matrix_star(order, value), value)

    def in_quadratic(value):
        return all(order.multiply(value[k:k+4, :], j) == order.multiply(j, value[k:k+4, :])
                   for k in range(0, 16, 4))

    assert in_quadratic(gram(unitary)) and in_quadratic(gram(shear))
    assert not in_quadratic(gram(combined))
    return {"quadratic_field": "Q(j), j^2=-11", "first_gram_in_field": True,
            "second_gram_in_field": True, "product_gram_in_field": False,
            "genuine_integral_automorphisms": True, "hsp_query_group_established": False}
