"""Exact supplied-Smith-kernel controls, not a simulated opaque-label search."""

from sympy import Matrix, eye, zeros

from content_reduction import probe_schedule, recover_content
from cyclic_source import certificate_queries, cyclic_annihilator, primitive_frame
from controls_cyclic import split_fixture
from kernel_output import action, inverse_mod, mod, odd_maximal_order


def preserves_smith_doubled(query, p, e, content_exponent, vector):
    """Check actual generator membership in a nonfree doubled subgroup."""
    a, b, m = content_exponent, e-content_exponent, p**e
    if not 0 <= a <= b:
        raise ValueError("Smith exponents must be ordered and total e")
    frame = primitive_frame(vector, m, ((p, e),))
    change = Matrix.diag(frame, frame)
    divisors = (p**a, p**b, p**a, p**b)
    generators = change*Matrix.diag(*divisors)
    moved = mod(inverse_mod(change, m)*Matrix(query)*generators, m)
    return all(int(moved[i, j]) % divisors[i] == 0 for i in range(4) for j in range(4))


def content_control(n, factors, smith_data):
    """smith_data is supplied evidence and is NOT an input to the public protocol."""
    records = probe_schedule(n, factors)
    matches = {}
    for record in records:
        p = record["key"][0]
        e, a, vector = smith_data[p]
        matches[record["key"]] = preserves_smith_doubled(record["query"], p, e, a, vector)
    result = recover_content(n, factors, matches)
    result["supplied_smith_data_not_recovered"] = True
    result["classical_source_query_bound"] = len(records)+1
    return result


def ideal_scaling_control():
    """The degree243 kernel with content3 is supplied, not recovered."""
    order, p, e, a, vector = odd_maximal_order(11), 3, 5, 1, Matrix([3, 1])
    n, residual, content = p**e, p**(e-2*a), p**a
    residual_split = split_fixture(11, residual, ((p, e-2*a),))
    smaller = cyclic_annihilator(order, residual_split, vector, residual, ((p, e-2*a),))
    original = content*smaller
    frame = primitive_frame(vector, n, ((p, e),))
    generators = frame*Matrix.diag(p**a, p**(e-a))
    original_split = split_fixture(11, n, ((p, e),))
    assert abs(original.det()) == n*n
    for j in range(4):
        assert mod(action(original[:, j], original_split)*generators, n) == zeros(2)
    candidate_checks = certificate_queries(vector, n, ((p, e),))
    assert all(preserves_smith_doubled(q, p, e, a, vector) for q in candidate_checks)
    return {"degree": n, "content": content, "residual_degree": residual,
            "ideal_index": int(abs(original.det())), "ideal_norm": n,
            "ideal_hnf": [list(map(int, original.row(i))) for i in range(4)],
            "annihilates_original_supplied_kernel": True,
            "unknown_kernel_recovered": False, "geometric_execution": False}


def noncyclic_endomorphism_control():
    """phi=3(3+4i), degree225: a genuine supplied noncyclic endomorphism."""
    order = odd_maximal_order(11)
    residual, n, content, vector = 25, 225, 3, Matrix([4, 3])
    psi = 3*order.unit+4*eye(4)[:, 1]
    phi = content*psi
    assert order.multiply(order.star(phi), phi) == n*order.unit
    result = content_control(n, ((3, 2), (5, 2)),
                             {3: (2, 1, (1, 0)), 5: (2, 0, tuple(vector))})
    assert result["content"] == content and result["cyclic_residual_degree"] == residual
    split = split_fixture(11, residual, ((5, 2),))
    assert mod(action(psi, split)*vector, residual) == zeros(2, 1)
    ideal = content*cyclic_annihilator(order, split, vector, residual, ((5, 2),))
    principal = Matrix.hstack(*[order.multiply(eye(4)[:, i], phi) for i in range(4)])
    assert abs(ideal.det()) == abs(principal.det()) == n*n
    assert all(x.q == 1 for x in ideal.inv()*principal)
    assert all(x.q == 1 for x in principal.inv()*ideal)
    return {"degree": n, "content": content, "residual_degree": residual,
            "supplied_phi_coordinates": list(map(int, phi)),
            "reconstructed_ideal_equals_principal_left_ideal": True,
            "ideal_index": int(abs(ideal.det())),
            "protocol": result, "unknown_kernel_recovered": False,
            "curve_points_generated": False, "geometric_quotients_executed": False}
