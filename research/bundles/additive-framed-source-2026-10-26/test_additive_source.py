"""Exact algebra and deliberate false-positive controls, not native HSP runs."""

from itertools import product
from pathlib import Path
import sys

import pytest
from sympy import Matrix, Rational, eye, kronecker_product, zeros

from additive_source import (
    adjoint, block_isometry, construct, fixes_inclusions, four_square_matrix,
    frame_operators, input_index, candidate_lattice, multiply, norm,
    quaternion_matrix, scalar_matrix, shear, uniform_plan,
)
from kernel_output import QuaternionOrder, odd_maximal_order

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "smooth-repolarization-2026-10-23"))
from smooth_repolarization import certificate, verify_certificate


def congruence(order, w, z):
    return multiply(order, multiply(order, adjoint(order, w), z), w)


def scaled_suborder(order, ell):
    change = Matrix.diag(1, ell, ell, ell)
    inverse = change.inv()
    products = tuple(tuple(inverse*order.multiply(change[:, i], change[:, j])
                           for j in range(4)) for i in range(4))
    return QuaternionOrder(products, inverse*order.unit,
                           inverse*order.involution*change, order.traces*change), change


@pytest.mark.parametrize("p,n,roots,beta", [
    (7, 2, (3, 2, 1, 1), (0, 0, 0, 0)),
    (11, 3, (8, 4, 0, 0), (0, 1, 1, 0)),
    (19, 5, (24, 4, 4, 4), (2, -1, 3, -2)),
    (31, 7, (48, 8, 4, 4), (1, 2, -1, 1)),
])
def test_quadratic_principal_certificate(p, n, roots, beta):
    order = odd_maximal_order(p)
    record = construct(order, beta, n, roots)
    z, t = record["polarization"], record["trace"]
    identity = scalar_matrix(order, eye(16))
    assert z.integral and adjoint(order, z) == z
    assert multiply(order, z, z)-z.scale(t)+identity == scalar_matrix(order, zeros(16))
    assert multiply(order, z, identity.scale(t)-z) == identity
    small, adj = record["small"], record["small_adjugate"]
    assert multiply(order, small, adj) == scalar_matrix(order, n**4*eye(2))
    zero, one = zeros(4, 1), order.unit
    u = quaternion_matrix([[one, Matrix(beta)/n], [zero, one]])
    assert multiply(order, adjoint(order, u), u).scale(n*n) == small
    inverse = adj.scale(Rational(1, n**4)).repeat(4)
    schur = adj.repeat(4)-multiply(order, multiply(order, adjoint(order, record["cross"]), inverse), record["cross"])
    assert schur == inverse


@pytest.mark.parametrize("delta", [(0, 0, 1, 0), (1, -1, 0, 2)])
def test_translation_is_noncommutative_integral_congruence(delta):
    order = odd_maximal_order(11)
    beta, delta = Matrix([0, 1, 0, 0]), Matrix(delta)
    assert order.multiply(beta, delta) != order.multiply(delta, beta)
    left = construct(order, beta, 3, (8, 4, 0, 0))["polarization"]
    right = construct(order, beta+3*delta, 3, (8, 4, 0, 0))["polarization"]
    w = shear(order, delta)
    assert w.integral and fixes_inclusions(order, w)
    assert congruence(order, w, left) == right
    for e in frame_operators(4):
        e = scalar_matrix(order, e)
        assert multiply(order, w, e) == multiply(order, e, w)


def test_rational_translation_is_not_an_integral_automorphism():
    order = odd_maximal_order(11)
    beta = Matrix([0, 1, 0, 0])
    delta = Matrix([Rational(1, 3), 0, 0, 0])
    w = shear(order, delta)
    left = construct(order, beta, 3, (8, 4, 0, 0))["polarization"]
    right = construct(order, beta+3*delta, 3, (8, 4, 0, 0))["polarization"]
    assert congruence(order, w, left) == right
    assert fixes_inclusions(order, w)
    assert not w.integral


@pytest.mark.parametrize("signs,fixed_column", [((-1, 1), 9), ((1, -1), 0)])
def test_each_omitted_inclusion_allows_false_coset_collision(signs, fixed_column):
    order = odd_maximal_order(11)
    plus = construct(order, order.unit, 3, (8, 4, 0, 0))["polarization"]
    minus = construct(order, -order.unit, 3, (8, 4, 0, 0))["polarization"]
    small = scalar_matrix(order, Matrix.diag(*signs))
    w = block_isometry(order, small, small)
    assert congruence(order, w, plus) == minus
    assert w.integral and not fixes_inclusions(order, w)
    assert all(multiply(order, w, scalar_matrix(order, e)) ==
               multiply(order, scalar_matrix(order, e), w) for e in frame_operators(4))
    vector = scalar_matrix(order, eye(16)[:, fixed_column])
    assert multiply(order, w, vector) == vector
    assert (Rational(-2, 3)*order.unit)[0].q == 3
    # Sign changes are invisible at level two: a single small level is not rigidity.
    assert all(all(x % 2 == 0 for x in coefficient)
               for coefficient in (w-scalar_matrix(order, eye(16))).coefficients)


def test_unordered_graph_preserves_a_legal_shear_but_ordered_domain_does_not():
    modulus = 3
    u = Matrix([[1, 1], [0, 1]])
    w = Matrix.diag(u, u.inv().T)
    e = Matrix.diag(1, 1, 0, 0)
    vectors = [Matrix(x) for x in product(range(modulus), repeat=4)]
    reduce = lambda v: tuple(int(x) % modulus for x in v)
    graph = [(reduce(v), reduce(e*v)) for v in vectors]
    transported = [(reduce(w*v), reduce(w*e*v)) for v in vectors]
    assert set(graph) == set(transported)
    assert graph != transported
    bad = Matrix.eye(4)
    bad[0, 2] = 1
    assert set(graph) != {(reduce(bad*v), reduce(bad*e*v)) for v in vectors}


def test_scalar_frame_centralizer_has_only_two_repeated_blocks():
    size = 8
    equations = []
    for e in frame_operators(2):
        # Column-major vectorization of X*e-e*X.
        equations.append(kronecker_product(e.T, eye(size))-kronecker_product(eye(size), e))
    system = Matrix.vstack(*equations)
    assert size*size-system.rank() == 8
    basis = []
    for block, i, j in product(range(2), range(2), range(2)):
        small = zeros(2)
        small[i, j] = 1
        repeated = kronecker_product(eye(2), small)
        full = zeros(size)
        full[block*4:(block+1)*4, block*4:(block+1)*4] = repeated
        basis.append(Matrix(list(full.T)))
    expected = Matrix.hstack(*basis)
    assert expected.rank() == 8 and system*expected == zeros(system.rows, 8)


@pytest.mark.parametrize("ell", [2, 3, 5, 11])
def test_full_suborder_index_and_lattice_recovery(ell):
    order = odd_maximal_order(11)
    suborder, change = scaled_suborder(order, ell)
    d = ell**3
    assert input_index(order, 11) == 1
    assert input_index(suborder, 11) == d
    generators = [ell**2*eye(4)[:, i] for i in range(1, 4)]
    recovered = candidate_lattice(generators, d)
    assert change*recovered == eye(4)


def test_correct_index_does_not_certify_integrality():
    order = odd_maximal_order(11)
    _, change = scaled_suborder(order, 3)
    wrong = candidate_lattice([eye(4)[:, 0]], 27)
    native_coordinates = change*wrong
    assert native_coordinates[0, 0] == Rational(1, 27)
    assert norm(order, native_coordinates[:, 0]) == Rational(1, 27**2)


@pytest.mark.parametrize("generators", [[], [eye(4)[:, 0], eye(4)[:, 1]]])
def test_wrong_subgroup_size_is_rejected(generators):
    with pytest.raises(ValueError, match="wrong order"):
        candidate_lattice(generators, 27)


@pytest.mark.parametrize("beta", [(0, 0, 0, 0), (0, 1, 1, 0), (2, -1, 3, -2)])
def test_existing_smooth_norm_certificate_accepts_new_trace(beta):
    order = odd_maximal_order(11)
    trace = construct(order, beta, 3, (8, 4, 0, 0))["trace"]
    assert all(verify_certificate(certificate(trace, 2*(trace+3))).values())


def test_cost_report_does_not_claim_executed_geometry():
    plan = uniform_plan(27, 25)
    assert plan["query_count_domain"] == 27**4
    assert plan["stabilized_dimension"] == 128
    assert plan["frame_operator_count"] == 2048
    assert plan["theta_coordinates_per_point"] == 2**256
    assert plan["graph_points_per_prime_exponent"] == 256
    assert plan["refined_prime_kernel_points_exponent"] == 128
    assert plan["marking_product_squared_must_exceed"] > 4*128*plan["trace_bound"]**2
    assert plan["native_geometric_label_executed"] is False


@pytest.mark.parametrize("denominator,roots,beta", [
    (1, (0, 0, 0, 0), (0, 0, 0, 0)),
    (3, (1, 1, 1, 1), (0, 0, 0, 0)),
    (3, (8, 4, 0, 0), (Rational(1, 2), 0, 0, 0)),
])
def test_malformed_polarization_input_rejected(denominator, roots, beta):
    with pytest.raises(ValueError):
        construct(odd_maximal_order(11), beta, denominator, roots)


def test_fixed_four_square_matrix():
    t = four_square_matrix((8, 4, 0, 0))
    assert t.T*t == t*t.T == 80*eye(4)


def test_changing_four_square_frame_per_query_can_destroy_equal_labels():
    first = four_square_matrix((3, 2, 1, 1))
    second = four_square_matrix((2, 3, 1, 1))
    assert first.T*first == second.T*second == 15*eye(4)
    # A frame-preserving isometry would require T_ij*W^dagger*V=T'_ij*I.
    # Nonproportional scalar T matrices cannot satisfy that equation.
    assert Matrix.hstack(Matrix(list(first)), Matrix(list(second))).rank() == 2


def test_receipt_keeps_geometry_review_and_advantage_unexecuted():
    from replay_additive_source import receipt
    scope = receipt()["execution_scope"]
    assert scope["exact_quaternion_matrix_controls_executed"] is True
    assert all(scope[name] is False for name in (
        "native_geometric_label_executed", "native_output_integrality_verifier_executed",
        "coherent_source_executed", "quantum_receiver_executed",
        "independent_review_of_additive_proposal", "native_classical_hardness_established",
        "novelty_established", "speedup_established",
    ))
