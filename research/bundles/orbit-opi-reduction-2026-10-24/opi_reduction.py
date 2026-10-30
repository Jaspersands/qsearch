"""Paid random restriction of the native cubic relation to scalar OPI.

This is a classical reduction, NOT a scalar OPI solver or a quantum circuit.
The fixed-input probability argument in REDUCTION.md is locally unreviewed.
"""

from fractions import Fraction as F
from math import comb
from pathlib import Path
import random
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"orbit-residual-decoder-2026-10-24"))
from orbit_decoder import Geometry, field, geometry, integer, upward  # noqa: E402


def horner(coefficients, x, p):
    value = 0
    for c in reversed(coefficients):
        value = (value*x+c) % p
    return value


def polynomial(coefficients, p, K):
    if not isinstance(coefficients, (tuple, list)) or len(coefficients) > K:
        raise ValueError("explicit polynomial coefficients of degree below K required")
    return tuple(integer(c, "coefficient", 0, p-1) for c in coefficients)


def validate(g, multipliers, nu, halfsets):
    if not isinstance(g, Geometry) or g.width != 3:
        raise ValueError("the original ordered cubic orbit geometry is required")
    p, M = g.p, len(g.nodes)
    integer(nu, "nonsquare", 1, p-1)
    if pow(nu, (p-1)//2, p) != p-1:
        raise ValueError("the original anisotropic nonsquare is required")
    if len(multipliers) != M or len(halfsets) != M:
        raise ValueError("one multiplier and explicit halfset per native orbit required")
    b = tuple(integer(x, "nonzero multiplier", 1, p-1) for x in multipliers)
    for row in halfsets:
        if not isinstance(row, (tuple, list)) or len(row) != (p-1)//2:
            raise ValueError("every explicit halfset must have exactly (p-1)/2 entries")
        for x in row:
            integer(x, "halfset entry", 0, p-1)
        if tuple(sorted(set(row))) != tuple(row):
            raise ValueError("canonical sorted distinct halfset entries required")
    return b


def local_quadratic(p, zeta, a, b, nu, u, v):
    """Internal field arithmetic; public contracts are checked by restrict()."""
    x0 = (a*u+a*a*v) % p
    y0 = (zeta*a*u+zeta*zeta*a*a*v) % p
    z0 = (zeta*zeta*a*u+zeta*a*a*v) % p
    A = b*(1-nu) % p
    B = (1+2*b*(x0-nu*y0)) % p
    C = (z0+b*(x0*x0-nu*y0*y0)) % p
    beta = (C-B*B*pow(4*A, -1, p)) % p
    return A, B, C, beta


def restrict(g, multipliers, nu, halfsets, q1, q2, ell):
    b = validate(g, multipliers, nu, halfsets)
    integer(ell, "retained list size", 1, (g.p-1)//2)
    q1 = polynomial(q1, g.p, g.row_length)
    q2 = polynomial(q2, g.p, g.row_length)
    quadratics, counts, lists = [], [], []
    for i, (a, node) in enumerate(zip(g.representatives, g.nodes)):
        A, B, C, beta = local_quadratic(
            g.p, g.root, a, b[i], nu, horner(q1, node, g.p), horner(q2, node, g.p))
        accepted = set(halfsets[i])
        preimage = tuple(t for t in range(g.p) if (A*t*t+B*t+C) % g.p in accepted)
        quadratics.append((A, B, C, beta))
        counts.append(len(preimage))
        lists.append(preimage[:ell])
    bad = tuple(i for i, count in enumerate(counts) if count < ell)
    return {"status": "RETRY_SPARSE_LIST" if bad else "REDUCED_TO_SCALAR_OPI",
            "q1": q1, "q2": q2, "ell": ell, "quadratics": tuple(quadratics),
            "counts": tuple(counts), "failed_indices": bad,
            "lists": tuple(lists) if not bad else None,
            "all_native_halfsets_kept": True, "native_witness_produced": False}


def bonferroni_lower(M, independence, q, order=None):
    """No-bad-event bound using only order-wise independence, order odd.

    The order+1 remainder belongs to an independent comparison model. It
    does NOT assume that the actual events are (order+1)-wise independent.
    """
    integer(M, "event count", 1, 21845)
    integer(independence, "independence order", 1, M)
    if not isinstance(q, F) or not 0 <= q <= 1:
        raise ValueError("an exact marginal probability upper bound is required")
    if order is None:
        order = independence if independence % 2 else independence-1
    integer(order, "Bonferroni order", 1, independence)
    if order % 2 != 1:
        raise ValueError("a lower Bonferroni truncation must have odd order")
    remainder = comb(M, order+1)*q**(order+1) if order < M else F(0)
    return max(F(0), (1-q)**M-remainder)


def success_lower(p, M, K, ell, order=None):
    field(p)
    integer(M, "native orbit count", 2, (p-1)//3)
    integer(K, "polynomial dimension", 2, M)
    integer(ell, "retained list size", 1, (p-1)//2)
    if (p-1) % 3:
        raise ValueError("cubic orbits require p=1 mod3")
    h = (p-1)//2
    bad_beta_count = min(p, h*(p-h)//(h-ell+1)**2)
    q = F(bad_beta_count, p)
    return bonferroni_lower(M, K, q, order), bad_beta_count


def downward(value, bits=128):
    return F((value.numerator << bits)//value.denominator, 1 << bits)


def certificate(g, ell, order=None):
    if not isinstance(g, Geometry) or g.width != 3:
        raise ValueError("cubic geometry required")
    M, K = len(g.nodes), g.row_length
    lower, B = success_lower(g.p, M, K, ell, order)
    order = order if order is not None else (K if K % 2 else K-1)
    low = downward(lower)
    return {"p": g.p, "M": M, "K": K, "ell": ell, "rate": str(F(K, M)),
            "density": str(F(ell, g.p)), "bad_beta_count_upper": B,
            "bad_marginal_upper": str(F(B, g.p)), "independence_order": K,
            "Bonferroni_order": order, "success_lower_dyadic": str(low),
            "expected_trials_upper": str(1/low) if low else None,
            "rate_plus_density_minus_one": str(F(K, M)+F(ell, g.p)-1),
            "fixed_input_uniform_coin_theorem": "LOCAL_UNREVIEWED",
            "external_OPI_finite_length_threshold_instantiated": False,
            "zero_bound_is_not_an_impossibility_result": True}


def random_reduction(g, multipliers, nu, halfsets, ell, *, seed=None, attempts=4):
    validate(g, multipliers, nu, halfsets)
    cert = certificate(g, ell)
    integer(attempts, "attempt budget", 1, 100)
    if seed is not None and type(seed) is not int:
        raise ValueError("seed must be an integer or None")
    rng = random.SystemRandom() if seed is None else random.Random(seed)
    history, accepted = [], None
    for _ in range(attempts):
        q1, q2 = [tuple(rng.randrange(g.p) for _ in range(g.row_length)) for _ in range(2)]
        result = restrict(g, multipliers, nu, halfsets, q1, q2, ell)
        history.append({key: result[key] for key in
                        ("status", "q1", "q2", "counts", "failed_indices")})
        if result["status"] == "REDUCED_TO_SCALAR_OPI":
            accepted = result
            break
    low = F(cert["success_lower_dyadic"])
    trial_count, M, K = len(history), len(g.nodes), g.row_length
    return {"status": "REDUCED_TO_SCALAR_OPI" if accepted else "BUDGET_EXHAUSTED",
            "restriction": accepted, "history": history, "certificate": cert,
            "budget_failure_upper_dyadic_under_ideal_coins": str(upward((1-low)**attempts)),
            "seed": seed, "seeded_replay_is_not_probability_evidence": seed is not None,
            "uniform_independent_coefficient_draws_required": True,
            "native_witness_produced": False, "scalar_OPI_solver_executed": False,
            "work": {"attempts_executed": trial_count,
                     "random_field_draws": 2*K*trial_count,
                     "polynomial_evaluations": 2*M*trial_count,
                     "horner_multiply_add_steps": 2*M*K*trial_count,
                     "native_table_membership_lookups": M*g.p*trial_count,
                     "explicit_native_table_entries": M*(g.p-1)//2,
                     "scope": "named_work_counts_not_total_bit_operations_or_peak_memory"}}


def lift_and_verify(g, multipliers, nu, halfsets, restriction, q0):
    """Recompute the restriction, then check one lifted ORIGINAL polynomial."""
    fresh = restrict(g, multipliers, nu, halfsets, restriction["q1"], restriction["q2"], restriction["ell"])
    if fresh != restriction or fresh["status"] != "REDUCED_TO_SCALAR_OPI":
        raise ValueError("a complete unmodified accepted restriction is required")
    q0 = polynomial(q0, g.p, g.row_length)
    coefficients = [0]*g.dimension
    for residue, q in enumerate((q0, fresh["q1"], fresh["q2"])):
        for j, value in enumerate(q):
            coefficients[3*j+residue] = value
    scalar_pass = tuple(horner(q0, node, g.p) in row for node, row in zip(g.nodes, fresh["lists"]))
    residuals, native_pass = [], []
    for points, b, allowed in zip(g.points, multipliers, halfsets):
        x, y, z = (horner(coefficients, t, g.p) for t in points)
        residual = (z+b*(x*x-nu*y*y)) % g.p
        residuals.append(residual)
        native_pass.append(residual in allowed)
    if any(a and not b for a, b in zip(scalar_pass, native_pass)):
        raise ArithmeticError("scalar satisfaction failed to lift to the native predicate")
    return {"status": "VERIFIED_NATIVE_PERFECT" if all(native_pass) else "PARTIAL_NATIVE_WITNESS",
            "coefficients": coefficients, "degree": max((j for j, c in enumerate(coefficients) if c), default=-1),
            "scalar_score": sum(scalar_pass), "native_score": sum(native_pass),
            "native_residuals": residuals, "native_predicates": len(g.nodes),
            "native_point_evaluations": 3*len(g.nodes),
            "reduced_score_preserved_coordinatewise": True,
            "uniform_sampler_or_speedup_claimed": False}
