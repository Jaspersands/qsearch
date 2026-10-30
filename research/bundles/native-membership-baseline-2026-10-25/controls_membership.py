"""Supplied endomorphism controls, NOT a native interpolation implementation."""

from itertools import product
from math import gcd, prod

from sympy import Matrix, eye, kronecker_product, zeros
from sympy.solvers.diophantine.diophantine import sum_of_four_squares

from native_membership import MembershipPlan, recover_local_data, reduced_norm
from controls_double import full_split_fixture
from kernel_output import (
    action, alternating_form, inverse_mod, mod, odd_maximal_order, odd_maximal_split,
)
from local_baseline import kernel_ideal_from_local_data, local_frame


def rational_mod(matrix, prime):
    return Matrix(matrix).applyfunc(lambda x: int(x.p)*pow(int(x.q), -1, prime) % prime)


def conjugate(order, phi, alpha):
    n = reduced_norm(order, phi)
    if not n:
        raise ValueError("nonzero supplied map required")
    return order.multiply(order.multiply(phi, alpha), order.star(phi))/n


def smith_contains(query, q, e, a, vector):
    """Independent finite-ring control using generators of a supplied kernel."""
    frame = local_frame(vector, q, e)
    divisors = (q**a, q**(e-a))
    moved = mod(inverse_mod(frame, q**e)*query*frame*Matrix.diag(*divisors), q**e)
    return all(int(moved[i, j]) % divisors[i] == 0 for i in range(2) for j in range(2))


def supplied_map_control(coefficients, factors):
    order = odd_maximal_order(11)
    phi = Matrix(coefficients)
    n = reduced_norm(order, phi)
    split = full_split_fixture(11, n, factors)
    plan = MembershipPlan.create(order, split, n, factors, 11)
    phi_matrix = action(phi, split)
    records = []

    def reference_membership(query):
        probe = plan.probe(query)
        gamma = conjugate(order, phi, probe["alpha"])
        integral = all(x.q == 1 for x in gamma)
        # det(phi) has local valuation e, hence image(adj(phi)) is its kernel
        # modulo q^e. This checks containment without using recovered directions.
        local_checks = [mod(phi_matrix*query*phi_matrix.adjugate(), q**e) == zeros(2)
                        for q, e in factors]
        assert integral == all(local_checks)
        records.append({"norm": probe["norm"], "integral": integral,
                        "omitted_primes": [r for r in plan.primes if r not in probe["primes"]],
                        "norm_shares_native_degree": gcd(probe["norm"], n) > 1,
                        "level": probe["torsion_level"]})
        return integral

    result = recover_local_data(n, factors, reference_membership)
    ideal = kernel_ideal_from_local_data(order, split, n, factors,
                                        result["contents"], result["directions"])
    principal = Matrix.hstack(*(order.multiply(eye(4)[:, j], phi) for j in range(4)))
    assert abs(ideal.det()) == abs(principal.det()) == n*n
    assert all(x.q == 1 for x in ideal.inv()*principal)
    assert all(x.q == 1 for x in principal.inv()*ideal)
    assert len(records) == result["membership_calls"]
    return {
        "degree": n, "supplied_map": list(map(int, phi)), "recovery": result,
        "query_count": len(records), "positive_probes": sum(r["integral"] for r in records),
        "negative_probes": sum(not r["integral"] for r in records),
        "noncoprime_norm_probes": sum(r["norm_shares_native_degree"] for r in records),
        "norm_factor_omissions": sum(len(r["omitted_primes"]) for r in records),
        "maximum_observed_norm": max(r["norm"] for r in records),
        "uniform_norm_bound": plan.norm_bound, "fixed_weak_primes": list(plan.primes),
        "transcript_bits": prod(plan.primes).bit_length(),
        "minimum_filtered_level": min(r["level"] for r in records),
        "original_principal_ideal_verified": True,
        "backend": "EXACT_SUPPLIED_MAP_AND_KNOWN_TARGET_ORDER_CONTROL",
        "native_interpolation_executed": False, "unknown_native_kernel_recovered": False,
    }


def masked_action_control(phi, alpha, prime=7, mask=2):
    order = odd_maximal_order(11)
    phi, alpha = Matrix(phi), Matrix(alpha)
    n, norm = reduced_norm(order, phi), reduced_norm(order, alpha)
    if gcd(prime, n*norm*11*mask) != 1:
        raise ValueError("invertible common mask and allowable torsion prime required")
    split = odd_maximal_split(11, prime)
    phi_r, alpha_r = (mod(action(x, split), prime) for x in (phi, alpha))
    gamma = conjugate(order, phi, alpha)
    gamma_r = rational_mod(action(gamma, split), prime)
    basis = mod(mask*phi_r, prime)
    images = mod(basis*alpha_r, prime)
    form = alternating_form(1)
    assert images == mod(gamma_r*basis, prime)
    assert mod(gamma_r.T*form*gamma_r-norm*form, prime) == zeros(2)
    assert mod(images.T*form*images-norm*basis.T*form*basis, prime) == zeros(2)
    return {"gamma": gamma, "gamma_r": gamma_r, "basis": basis,
            "images": images, "norm": norm, "integral": all(x.q == 1 for x in gamma)}


def negative_graph_control():
    """A NONINTEGRAL gamma still gives a full isotropic interpolation kernel."""
    order, phi, alpha = odd_maximal_order(11), Matrix([1, 1, 0, 0]), Matrix([0, 0, 1, 0])
    result = masked_action_control(phi, alpha)
    assert not result["integral"]
    n, norm, prime = reduced_norm(order, phi), result["norm"], 7
    level = 5*7*13
    assert gcd(level, norm*n*11) == 1 and level*level > 8*n*n*norm
    a, b, c, d = map(int, sum_of_four_squares(level-norm))
    scalar = Matrix([[a, -b, -c, -d], [b, a, d, -c],
                     [c, -d, a, b], [d, c, -b, a]])
    assert scalar*scalar.T == (level-norm)*eye(4)
    ranks = []
    for r in (5, 7, 13):
        data = masked_action_control(phi, alpha, r)
        basis, images = data["basis"], data["images"]
        upper = kronecker_product(scalar.T, basis)
        lower = Matrix.diag(*([images]*4))
        graph = Matrix.vstack(upper, lower)
        assert gcd(int(lower.det()), r) == 1
        assert mod(graph.T*alternating_form(8)*graph, r) == zeros(8)
        ranks.append({"prime": r, "rank": 8, "isotropic": True})
    return {"native_degree": n, "norm": norm, "torsion_level": level,
            "gamma_coordinates": [str(x) for x in result["gamma"]],
            "integral": False, "local_graphs": ranks,
            "expected_interpolator_result": "BOTTOM_BY_SEPARATION_PROOF",
            "interpolator_executed": False}


def different_column_masks_counterexample():
    order, prime = odd_maximal_order(11), 7
    phi, alpha = Matrix([1, 1, 0, 0]), Matrix([0, 1, 0, 0])
    split = odd_maximal_split(11, prime)
    phi_r, alpha_r = (mod(action(x, split), prime) for x in (phi, alpha))
    bad_basis = mod(phi_r*Matrix.diag(1, 2), prime)
    inferred = mod(bad_basis*alpha_r*inverse_mod(bad_basis, prime), prime)
    actual = rational_mod(action(conjugate(order, phi, alpha), split), prime)
    assert inferred != actual
    assert inferred.det() % prime == actual.det() % prime == 1
    return {"prime": prime, "actual": list(map(int, actual)),
            "incorrect": list(map(int, inferred)), "determinant_check_still_passes": True,
            "common_scalar_promise_is_essential": True}


def false_interpolant_control():
    """Paper uniqueness for integral maps alone does NOT separate rational maps."""
    order = odd_maximal_order(11)
    # phi=1+3j has norm 100 and reduces to 1 on 3-torsion.
    phi, alpha = Matrix([-2, 0, 6, 0]), Matrix([0, 1, 0, 0])
    n, norm, level = reduced_norm(order, phi), reduced_norm(order, alpha), 3
    gamma = conjugate(order, phi, alpha)
    assert n == 100 and norm == 1 and any(x.q != 1 for x in gamma)
    split = odd_maximal_split(11, level)
    assert rational_mod(action(gamma-alpha, split), level) == zeros(2)
    assert level > norm and level*level > 8*norm
    assert level*level <= 8*n*n*norm
    delta = n*alpha-order.multiply(order.multiply(phi, alpha), order.star(phi))
    assert delta != zeros(4, 1) and all(int(x) % level == 0 for x in delta)
    return {"degree": n, "norm": norm, "torsion_level": level,
            "rational_gamma": [str(x) for x in gamma],
            "different_integral_interpolant": list(map(int, alpha)),
            "paper_uniqueness_bound_passes": True,
            "native_separation_bound_passes": False,
            "membership_would_be_false_positive_without_stronger_bound": True}


def membership_incidence_control(q):
    """Exhaustive SMALL-field check of the native prime-degree Boolean interface.

    This is not a new oracle candidate or a lower bound for the native input.
    The general at-most-two statement is proved in the accompanying note.
    """
    from sympy import isprime
    if type(q) is not int or not isprime(q) or q > 11:
        raise ValueError("small prime control only")
    lines = [(x, 1) for x in range(q)]+[(1, 0)]
    histogram = {0: 0, 1: 0, 2: 0}
    scalar_count = 0
    for a, b, c, d in product(range(q), repeat=4):
        count = sum(((a*x+b*y)*y-(c*x+d*y)*x) % q == 0 for x, y in lines)
        if a == d and b == c == 0:
            assert count == q+1
            scalar_count += 1
        else:
            assert count <= 2
            histogram[count] += 1
    return {"prime": q, "projective_lines": q+1, "scalar_matrices": scalar_count,
            "nonscalar_fixed_line_histogram": histogram,
            "scope": "BOOLEAN_MEMBERSHIP_ONLY_NOT_NATIVE_INPUT_HARDNESS"}
