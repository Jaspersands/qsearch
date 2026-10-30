"""Classical baseline controls, not hard instances or a quantum advantage."""
from itertools import product

from flint import fq_default_ctx
import pytest
import sympy as sp

from theorems.frobenius_circuit_lift import (
    lift_frobenius_circuit, mixed_frobenius_derivative_guard,
)
from theorems.succinct_polynomial_stabilizer import white_box_derivative_guard


def evaluate_source(nodes, point, p, coerce):
    values = []
    for node in nodes:
        kind = node[0]
        if kind == "var":
            value = point[node[1]]
        elif kind == "const":
            value = coerce(node[1])
        elif kind == "frob":
            value = values[node[1]]**p
        elif kind == "add":
            value = values[node[1]]+values[node[2]]
        else:
            value = values[node[1]]*values[node[2]]
        values.append(value)
    return values[-1]


def mixed_polarization(p):
    # x^p*z + x*z^p - 2*y*y^p: levels occur together, not one outer Frob.
    return (('var', 0), ('var', 1), ('var', 2), ('frob', 0), ('frob', 1),
            ('frob', 2), ('mul', 3, 2), ('mul', 0, 5), ('add', 6, 7),
            ('mul', 1, 4), ('const', p-2), ('mul', 10, 9), ('add', 8, 11))


def test_mixed_levels_preserve_specialization_and_gradient_of_lift():
    p, D = 7, 3
    nodes = mixed_polarization(p)
    lifted = lift_frobenius_circuit(p, D, nodes)
    assert lifted.degree_bound == 2 and lifted.original_degree_bound == p+1
    variables = sp.symbols('u:6')
    value, gradient = lifted.value_and_gradient(variables, sp.Integer)
    assert sp.expand(value-(variables[3]*variables[2]+variables[0]*variables[5]
                            +(p-2)*variables[1]*variables[4])) == 0
    assert gradient == tuple(sp.diff(value, x) for x in variables)
    field = fq_default_ctx(p, 3)
    point = [field.gen(), field.gen()**2+1, field(2)]
    features = point+[x**p for x in point]
    actual, _ = lifted.value_and_gradient(features, field)
    assert actual == evaluate_source(nodes, point, p, field)


def test_lifted_gradient_recovers_finite_symmetries_missed_by_raw_derivative():
    p = 7
    lifted = lift_frobenius_circuit(p, 3, mixed_polarization(p))
    mixed_frobenius_derivative_guard(lifted)
    with pytest.raises(ValueError):
        white_box_derivative_guard(p, 3, lifted.original_degree_bound)
    field = fq_default_ctx(p, 1)
    constraints = []
    for point in [(0, 1, 1, 0, 0, 1), (0, 0, 1, 0, 0, 1)]:
        point = list(map(field, point))
        _, gradient = lifted.value_and_gradient(point, field)
        # A=a E12+b E23+c E13, acting on EVERY Frobenius level.
        constraints.append([int(sum((gradient[e*3+i]*point[e*3+j]
                                     for e in range(2)), field(0)))
                            for i, j in ((0, 1), (1, 2), (0, 2))])
    x, y, z = sp.symbols('x y z')
    polynomial = x**p*z+x*z**p-2*y*y**p
    count = 0
    for a, b, c in product(range(p), repeat=3):
        learned = all((row[0]*a+row[1]*b+row[2]*c) % p == 0 for row in constraints)
        assert learned == ((a-2*b) % p == 0 and c == 0)
        matrix_c = (c+pow(2, -1, p)*a*b) % p
        image = polynomial.subs({x: x+a*y+matrix_c*z, y: y+b*z}, simultaneous=True)
        assert learned == sp.Poly(image-polynomial, x, y, z, modulus=p).is_zero
        count += learned
    assert count == p
    # log symmetry A=2E12+E23 is NOT found by differentiating F itself.
    raw = 2*y*sp.diff(polynomial, x)+z*sp.diff(polynomial, y)
    assert not sp.Poly(raw, x, y, z, modulus=p).is_zero


def test_large_prime_high_degree_and_shared_dag_do_not_expand_monomials():
    p, depth = 2**127-1, 40
    nodes = [('var', 0)]
    for _ in range(depth):
        previous = len(nodes)-1
        nodes.extend([('frob', previous), ('add', previous, previous+1)])
    for _ in range(50):
        previous = len(nodes)-1
        nodes.append(('mul', previous, previous))
    lifted = lift_frobenius_circuit(p, 2, nodes)
    assert lifted.original_degree_bound == p**depth*2**50
    assert lifted.degree_bound == 2**50 and lifted.frobenius_depth == depth
    assert len(nodes) < len(lifted.nodes) <= lifted.node_bound
    assert lifted.variable_count == 2*(depth+1)
    report = mixed_frobenius_derivative_guard(lifted)
    assert report['unknown_dimension_upper_bound'] == 4  # Not feature width squared.
    assert not report['stabilizer_solver_executed']
    field = fq_default_ctx(p, 3)
    point = [field.gen(), field(2)]
    features, current = [], point
    for _ in range(depth+1):
        features.extend(current)
        current = [x**p for x in current]
    value, _ = lifted.value_and_gradient(features, field)
    assert value == evaluate_source(nodes, point, p, field)


def test_syntactic_degree_can_be_inflated_without_changing_the_polynomial():
    p = 2**127-1
    nodes = [('var', 0)]
    for _ in range(130):
        previous = len(nodes)-1
        nodes.append(('mul', previous, previous))
    power = len(nodes)-1
    nodes.append(('const', p-1))
    nodes.append(('mul', power, len(nodes)-1))
    nodes.append(('add', power, len(nodes)-1))
    nodes.append(('add', 0, len(nodes)-1))
    # This DAG is formally x+(P-P), not just an equality on base-field points.
    lifted = lift_frobenius_circuit(p, 2, nodes)
    plain = lift_frobenius_circuit(p, 2, [('var', 0)])
    assert lifted.degree_bound == 2**130 >= p
    assert plain.degree_bound == 1 < p
    assert lifted.frobenius_depth == plain.frobenius_depth == 0
    assert len(nodes) == 135
    with pytest.raises(ValueError):
        mixed_frobenius_derivative_guard(lifted)
    mixed_frobenius_derivative_guard(plain)
    field = fq_default_ctx(p, 2)
    for point in ((field(0), field(1)), (field.gen(), field(2)),
                  (field.gen()+1, field.gen()**2)):
        value, gradient = lifted.value_and_gradient(point, field)
        assert value == point[0]
        assert gradient == (field(1), field(0))
        assert (value, gradient) == plain.value_and_gradient(point, field)
    # A sufficient guard may reject an unhelpful presentation. That rejection
    # cannot make syntactic degree an intrinsic hardness or admission criterion.


def test_identical_block_action_is_not_equivariant_for_non_base_field_matrices():
    field = fq_default_ctx(7, 2)
    coefficient = field.gen()
    assert coefficient**7 != coefficient
    # Under x -> x+a*y, the level-one block uses a^p, not a, unless a is in Fp.
    assert (field(0)+coefficient*field(1))**7 != field(0)+coefficient*field(1)


def test_long_frobenius_chain_is_iterative_and_keeps_complete_variable_blocks():
    nodes = [('var', 0)]+[('frob', i) for i in range(1500)]
    lifted = lift_frobenius_circuit(7, 2, nodes)
    assert lifted.nodes == (('var', 3000),)
    assert lifted.variable_count == 3002  # The unmentioned second coordinate is still needed.
    assert mixed_frobenius_derivative_guard(lifted)['parameter_degree_bound'] == 1


def test_degree_p_carry_destroys_injectivity_and_guard_rejects_it():
    p = 5
    nodes = [('var', 0)]
    for _ in range(p-1):
        nodes.append(('mul', len(nodes)-1, 0))
    nodes += [('frob', 0), ('const', p-1), ('mul', p, p+1), ('add', p-1, p+2)]
    lifted = lift_frobenius_circuit(p, 2, nodes)
    with pytest.raises(ValueError, match='no-carry'):
        mixed_frobenius_derivative_guard(lifted)
    u0, v0, u1, v1 = sp.symbols('u0 v0 u1 v1')
    Q, _ = lifted.value_and_gradient((u0, v0, u1, v1), sp.Integer)
    assert not sp.Poly(Q, u0, v0, u1, v1, modulus=p).is_zero
    specialized = Q.subs({u1: u0**p, v1: v0**p}, simultaneous=True)
    assert sp.Poly(specialized, u0, v0, modulus=p).is_zero
    changed = Q.subs({u0: u0+v0, u1: u1+v1}, simultaneous=True)-Q
    assert not sp.Poly(changed, u0, v0, u1, v1, modulus=p).is_zero


@pytest.mark.parametrize('nodes', [(), (('pow', 0),), (('var', 2),),
    (('const', 7),), (('const', True),), (('add', 0, 0),),
    (('var', 0), ('frob', 1)), (('var', 0), ('mul', True, 0)),
    (('var', 0, 1),), (('var', 0), ('frob', -1))])
def test_malformed_or_unverified_gate_descriptions_are_rejected(nodes):
    with pytest.raises(ValueError):
        lift_frobenius_circuit(7, 2, nodes)


def test_constant_output_and_output_selection_are_explicit():
    lifted = lift_frobenius_circuit(7, 2, [('const', 3), ('var', 0)], output=0)
    field = fq_default_ctx(7, 1)
    value, gradient = lifted.value_and_gradient([field(1), field(2)], field)
    assert value == field(3) and gradient == (field(0), field(0))
    assert lifted.degree_bound == 0
    with pytest.raises(ValueError):
        lifted.value_and_gradient([field(1)], field)
    for p, D, output in [(3, 2, 0), (9, 2, 0), (7, True, 0), (7, 2, True), (7, 2, 3)]:
        with pytest.raises(ValueError):
            lift_frobenius_circuit(p, D, [('var', 0)], output=output)
