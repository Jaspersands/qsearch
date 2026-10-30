"""Supplied quaternion-map controls; no unknown curve maps are computed."""

from functools import reduce
from math import gcd, lcm
import sys

from sympy import Matrix, eye, zeros

from suborder_transcript import ROOT, degree_envelope, transcript_from_points

sys.path.insert(0, str(ROOT / "native-membership-baseline-2026-10-25"))
sys.path.insert(0, str(ROOT / "double-level-source-2026-10-25"))
from calibration_controls import vector_operations
from controls_membership import conjugate, rational_mod
from controls_double import full_split_fixture
from double_level_source import congruence_lift
from kernel_output import action, inverse_mod, matrix_multiply, matrix_star, mod, odd_maximal_order, odd_maximal_split
from local_baseline import local_frame


def map_data(phi, characteristic=11):
    order = odd_maximal_order(characteristic)
    phi = Matrix(phi)
    norm = (order.traces*order.multiply(order.star(phi), phi))[0]/2
    if norm <= 0 or any(x.q != 1 for x in phi):
        raise ValueError("nonzero integral supplied map required")
    dictionary = Matrix.hstack(*(conjugate(order, phi, eye(4)[:, i]) for i in range(4)))
    scale = lcm(*(int(x.q) for x in dictionary))
    return order, phi, int(norm), dictionary, scale


def supplied_transcript_control(phi, prime, scale_multiple=1):
    order, phi, degree, dictionary, minimal_scale = map_data(phi)
    scale = scale_multiple*minimal_scale
    if gcd(prime, 11*scale*degree) != 1:
        raise ValueError("auxiliary prime must avoid the characteristic, scale and supplied degree")
    split = odd_maximal_split(11, prime)
    source = [mod(scale*x, prime) for x in split]
    target = [rational_mod(action(scale*dictionary[:, i], split), prime) for i in range(4)]
    basis, operations = ((1, 0), (0, 1)), vector_operations(prime, 2)
    counts = [0, 0]

    def evaluator(matrix, endpoint):
        def evaluate(point):
            counts[endpoint] += 1
            return tuple(int(x) for x in mod(matrix*Matrix(point), prime))
        return evaluate

    result = transcript_from_points(order, prime, scale, basis, basis,
        [evaluator(x, 0) for x in source], [evaluator(x, 1) for x in target], operations, operations)
    actual = mod(action(phi, split), prime)
    index = next(i for i, x in enumerate(actual) if x)
    normalized = mod(pow(int(actual[index]), -1, prime)*actual, prime)
    assert result["matrix"] == normalized
    assert counts == [8, 8]
    primitive = reduce(gcd, [abs(int(x)) for x in phi]) == 1
    envelope = degree_envelope(scale, 11)
    if primitive:
        assert envelope["degree_multiple"] % degree == 0
    return {"prime": prime, "supplied_degree": degree, "scale": scale,
            "primitive_map": primitive, "degree_envelope": envelope,
            "projective_action_correct": True, "known_source_calls": counts[0],
            "known_suborder_calls": counts[1], "unknown_isogeny_calls": 0,
            "coordinate_table_entries": result["coordinate_table_entries"],
            "intertwiner": [[int(x) for x in row] for row in result["matrix"].tolist()],
            "supplied_map_control": True,
            "actual_curve_points_generated": False, "unknown_native_kernel_recovered": False}


def primitive_degree_countercontrol():
    first = supplied_transcript_control([1, 1, 0, 0], 5)
    second = supplied_transcript_control([2, 2, 0, 0], 5)
    assert first["intertwiner"] == second["intertwiner"]
    assert first["scale"] == second["scale"] == 2
    assert second["degree_envelope"]["degree_multiple"] % second["supplied_degree"] != 0
    return {"same_projective_transcript": True, "same_dictionary": True,
            "degrees": [2, 8], "scale": 2, "claimed_envelope": 22,
            "second_map_violates_envelope_without_primitivity": True,
            "scope": "the primitive global map, not every scalar multiple, satisfies the bound"}


def inseparable_half_control():
    """phi=(1+i)j, degree22, using query modulus2 WITHOUT a split at p=11."""
    order = odd_maximal_order(11)
    unit, i, j = order.unit, eye(4)[:, 1], 2*eye(4)[:, 2]-order.unit
    phi = order.multiply(unit+i, j)
    _, _, degree, _, scale = map_data(phi)
    assert degree == 22 and scale == 2
    query = eye(4)
    query[0, 1] = 1
    split = full_split_fixture(11, 2, ((2, 1),))
    lifted = congruence_lift(order, split, query, 2, ((2, 1),))
    zero = zeros(4, 1)
    identity = Matrix.vstack(unit, zero, zero, unit)
    doubled = Matrix.vstack(phi, zero, zero, phi)
    h = matrix_multiply(order, matrix_multiply(order, doubled, lifted["S"]),
                        matrix_star(order, doubled))/degree
    half = (h-identity)/2
    assert all(x.q == 1 for x in h) and all(x.q == 1 for x in half)
    assert lifted["trace"] % 4 == 2
    assert matrix_multiply(order, half, half) == ((lifted["trace"]-2)//4)*h
    return {"degree": degree, "query_modulus": 2, "trace": lifted["trace"],
            "ramified_order_split_used": False, "characteristic_padding_used": False,
            "half_polarization_integral": True, "half_identity_verified": True,
            "supplied_map_only": True, "geometric_source_executed": False}


def unknown_depth_control(prime, exponent, depth, vector):
    """Native cyclic-kernel arithmetic control, not an opaque search candidate."""
    if not 0 <= depth <= exponent:
        raise ValueError("kernel depth must lie in the ambient modulus")
    modulus = prime**exponent
    frame = local_frame(vector, prime, exponent)
    inverse = inverse_mod(frame, modulus)
    generators = frame*Matrix.diag(prime**(exponent-depth), modulus)

    def preserves(query):
        moved = mod(inverse*query*generators, modulus)
        return all(int(moved[0, j]) % prime**(exponent-depth) == 0
                   and int(moved[1, j]) % modulus == 0 for j in range(2))

    thresholds = []
    for upper in (True, False):
        outcomes = []
        for j in range(exponent+1):
            query = eye(2)
            query[0 if upper else 1, 1 if upper else 0] = prime**j
            outcomes.append(preserves(query))
        threshold = outcomes.index(True)
        assert outcomes == [False]*threshold+[True]*(exponent+1-threshold)
        thresholds.append(threshold)
    assert max(thresholds) == depth
    return {"prime": prime, "ambient_exponent": exponent, "kernel_depth": depth,
            "axis_thresholds": thresholds, "containment_calls": 2*(exponent+1),
            "recovered_depth": max(thresholds), "supplied_kernel_only": True}


def right_order_inseparability_control():
    """Known principal ideals: a target Frobenius factor leaves the right order."""
    order = odd_maximal_order(11)
    j = 2*eye(4)[:, 2]-order.unit
    psi = Matrix([3, 4, 0, 0])
    phi = order.multiply(j, psi)

    def right_order(gamma):
        norm = (order.traces*order.multiply(order.star(gamma), gamma))[0]/2
        return Matrix.hstack(*(order.multiply(order.multiply(order.star(gamma), eye(4)[:, i]),
                                              gamma)/norm for i in range(4)))

    first, second = right_order(psi), right_order(phi)
    assert all(x.q == 1 for x in first.inv()*second)
    assert all(x.q == 1 for x in second.inv()*first)
    return {"separable_degree": 25, "inseparable_composite_degree": 275,
            "right_orders_equal_as_rational_lattices": True,
            "supplied_principal_maps_only": True, "target_ring_computed_from_unknown_input": False}
