"""Classical common-norm-flat attack on the existing cubic orbit relation.

The all-input probability proof is local and unreviewed. No claim is made
below the exact rank gate, for uniform sampling, or for a new algorithm.
"""

from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
import random
import sys

from flint import nmod_mat, nmod_poly

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"orbit-residual-decoder-2026-10-24"))
from orbit_decoder import Geometry, field, geometry, integer  # noqa: E402


def parameters(g):
    if not isinstance(g, Geometry) or g.width != 3:
        raise ValueError("the original three-point orbit geometry is required")
    M = len(g.representatives)
    r = 3*M-g.dimension
    d = M-r
    k = max(0, (d+1)//2)
    D = 2*k
    applicable = r == 0 or (d > 0 and D >= r)
    bound = Fraction(0) if r == 0 else (
        Fraction(1, (g.p-1)*g.p**(D-r)) if applicable else None)
    return {"M": M, "dimension": g.dimension, "parity_rank": r,
            "kernel_dimension": d, "extension_polynomial_dimension": k,
            "flat_dimension": D, "applicable": applicable,
            "one_attempt_failure_bound": bound}


def weights_and_product(nodes, p):
    if len(set(nodes)) != len(nodes):
        raise ValueError("interpolation nodes must be distinct")
    product = nmod_poly([1], p)
    for node in nodes:
        product *= nmod_poly([-node, 1], p)
    derivative = product.derivative()
    weights = [pow(int(derivative(node)), -1, p) for node in nodes]
    return weights, product


def norm_representative(p, nu, target, squares):
    """Deterministic O(p) norm search, charged against the explicit tables."""
    for y in range(p):
        value = (target+nu*y*y) % p
        if value in squares:
            return (squares[value], y), y+1
    raise ArithmeticError("nonzero quadratic-extension norm has no preimage")


@dataclass
class Setup:
    g: Geometry
    nu: int
    b: tuple
    ledger: dict
    weights: list
    product: object
    hx: object
    hy: object
    hz: object
    wx: object
    wy: object
    linear: object
    norm_factors: list
    norm_checks: int


def build(g, multipliers, nu):
    ledger = parameters(g)
    p, M, r, k = g.p, ledger["M"], ledger["parity_rank"], ledger["extension_polynomial_dimension"]
    if not ledger["applicable"] or r == 0:
        raise ValueError("nontrivial certified flat threshold is required")
    integer(nu, "nonsquare", 1, p-1)
    if pow(nu, (p-1)//2, p) != p-1:
        raise ValueError("anisotropic nonsquare required")
    if len(multipliers) != M:
        raise ValueError("one public multiplier per original orbit required")
    b = tuple(integer(x, "nonzero multiplier", 1, p-1) for x in multipliers)
    nodes = [x for orbit in g.points for x in orbit]
    weights, product = weights_and_product(nodes, p)
    last = [orbit[2] for orbit in g.points]
    delta, _ = weights_and_product(last, p)
    matrices = [nmod_mat([[weights[3*i+part]*pow(g.points[i][part], j, p) % p
                           for i in range(M)] for j in range(r)], p) for part in range(3)]
    squares = {}
    for x in range(p):
        squares.setdefault(x*x % p, x)
    wx, wy, factors, checks = [], [], [], 0
    for i, c in enumerate(last):
        target = delta[i]*pow(weights[3*i+2]*b[i] % p, -1, p) % p
        (a, beta), used = norm_representative(p, nu, target, squares)
        if (a*a-nu*beta*beta) % p != target:
            raise ArithmeticError("invalid norm scaling")
        factors.append([a, beta])
        checks += used
        powers = [pow(c, j, p) for j in range(k)]
        wx.append([z for v in powers for z in (a*v % p, nu*beta*v % p)])
        wy.append([z for v in powers for z in (beta*v % p, a*v % p)])
    wx, wy = nmod_mat(wx, p), nmod_mat(wy, p)
    hx, hy, hz = matrices
    return Setup(g, nu, b, ledger, weights, product, hx, hy, hz, wx, wy,
                 hx*wx+hy*wy, factors, checks)


def vector(values, p):
    return nmod_mat([[v % p] for v in values], p)


def values(column):
    return [int(column[i, 0]) for i in range(column.nrows())]


def quadratic_syndrome(s, x, y):
    return s.hz*vector([b*(a*a-s.nu*c*c) for b, a, c in zip(s.b, x, y)], s.g.p)


def linear_system(s, center, targets):
    p, M, D = s.g.p, s.ledger["M"], s.ledger["flat_dimension"]
    if len(center) != 2*M or len(targets) != M:
        raise ValueError("full original-field center and target vectors required")
    for value in (*center, *targets):
        integer(value, "field entry", 0, p-1)
    x, y = center[:M], center[M:]
    cross = nmod_mat([[2*s.b[i]*(x[i]*int(s.wx[i,j])-s.nu*y[i]*int(s.wy[i,j])) % p
                       for j in range(D)] for i in range(M)], p)
    matrix = s.linear-s.hz*cross
    rhs = quadratic_syndrome(s, x, y)-s.hx*vector(x, p)-s.hy*vector(y, p)-s.hz*vector(targets, p)
    return matrix, rhs


def full_row_solve(matrix, rhs):
    """Only accept full row rank; failed affine slices are paid retries."""
    r, D, p = matrix.nrows(), matrix.ncols(), matrix.modulus()
    rank = matrix.rank()
    if rank != r:
        return None, rank
    reduced, augmented_rank = nmod_mat(
        [[int(matrix[i,j]) for j in range(D)]+[int(rhs[i,0])] for i in range(r)], p).rref()
    if augmented_rank != r:
        raise ArithmeticError("full-row-rank system became inconsistent")
    result = [0]*D
    for i in range(r):
        pivot = next(j for j in range(D) if reduced[i,j])
        result[pivot] = int(reduced[i,D])
    if matrix*vector(result, p) != rhs:
        raise ArithmeticError("linear completion failed exact replay")
    return result, rank


def interpolate(s, word):
    p = s.g.p
    result = nmod_poly([], p)
    for node, weight, value in zip((a for orbit in s.g.points for a in orbit), s.weights, word):
        quotient, remainder = divmod(s.product, nmod_poly([-node,1], p))
        if remainder:
            raise ArithmeticError("public node did not divide the vanishing polynomial")
        result += quotient*(weight*value % p)
    if result.degree() >= s.g.dimension:
        raise ArithmeticError("parity completion did not yield the ORIGINAL degree bound")
    return [int(c) for c in result] or [0]


def verify(g, b, nu, allowed, coefficients):
    parameters(g)
    validate_allowed(g, allowed)
    if len(b) != len(g.points) or pow(nu, (g.p-1)//2, g.p) != g.p-1:
        raise ValueError("original multiplier vector and nonsquare required")
    integer(nu, "nonsquare", 1, g.p-1)
    for value in b:
        integer(value, "nonzero multiplier", 1, g.p-1)
    if not coefficients or len(coefficients) > g.dimension:
        raise ValueError("one original degree-bounded polynomial required")
    for c in coefficients:
        integer(c, "coefficient", 0, g.p-1)
    residuals = []
    for orbit, scale in zip(g.points, b):
        evaluated = []
        for node in orbit:
            value = 0
            for c in reversed(coefficients):
                value = (value*node+c) % g.p
            evaluated.append(value)
        x, y, z = evaluated
        residuals.append((z+scale*(x*x-nu*y*y)) % g.p)
    score = sum(value in row for value, row in zip(residuals, allowed))
    return {"score": score, "M": len(g.points), "residuals": residuals,
            "degree": max((j for j,c in enumerate(coefficients) if c), default=-1),
            "all_predicates_pass": score == len(g.points),
            "verification": "independent_Horner_at_all_original_points_and_halfsets"}


def validate_allowed(g, allowed):
    if len(allowed) != len(g.points):
        raise ValueError("one original halfset per orbit required")
    for row in allowed:
        if len(row) != (g.p-1)//2 or len(set(row)) != len(row):
            raise ValueError("explicit distinct halfset required")
        for x in row:
            integer(x, "allowed value", 0, g.p-1)


def attempt(s, allowed, center):
    validate_allowed(s.g, allowed)
    targets = [min(row) for row in allowed]
    matrix, rhs = linear_system(s, center, targets)
    solution, rank = full_row_solve(matrix, rhs)
    if solution is None:
        return {"status": "RETRY_RANK", "rank": rank}
    M, p = s.ledger["M"], s.g.p
    dx, dy = values(s.wx*vector(solution, p)), values(s.wy*vector(solution, p))
    x = [(a+d) % p for a,d in zip(center[:M], dx)]
    y = [(a+d) % p for a,d in zip(center[M:], dy)]
    z = [(t-b*(a*a-s.nu*c*c)) % p for t,b,a,c in zip(targets,s.b,x,y)]
    if s.hx*vector(x,p)+s.hy*vector(y,p)+s.hz*vector(z,p) != vector([0]*rank,p):
        raise ArithmeticError("nonlinear native parity check failed")
    coefficients = interpolate(s, [v for triple in zip(x,y,z) for v in triple])
    checked = verify(s.g, s.b, s.nu, allowed, coefficients)
    if not checked["all_predicates_pass"] or checked["residuals"] != targets:
        raise ArithmeticError("native polynomial failed original residual replay")
    return {"status": "VERIFIED_NATIVE_PERFECT", "rank": rank,
            "coefficients": coefficients, "verification": checked}


def solve(g, multipliers, nu, allowed, *, seed=None, attempts=3):
    validate_allowed(g, allowed)
    integer(attempts, "attempt budget", 1, 100)
    ledger = parameters(g)
    if not ledger["applicable"]:
        return {"status": "OUTSIDE_CERTIFIED_RANK_GATE", "ledger": ledger,
                "hardness_or_infeasibility_claim": False}
    if ledger["parity_rank"] == 0:
        raise ValueError("full interpolation is already trivial; this attack requires parity constraints")
    s = build(g, multipliers, nu)
    rng = random.SystemRandom() if seed is None else random.Random(seed)
    history = []
    for _ in range(attempts):
        center = [rng.randrange(g.p) for _ in range(2*ledger["M"])]
        result = attempt(s, allowed, center)
        history.append({"status": result["status"], "rank": result["rank"], "center": center})
        if result["status"] == "VERIFIED_NATIVE_PERFECT":
            break
    delta = ledger["one_attempt_failure_bound"]
    return {**result, "parameters": {k: str(v) if isinstance(v,Fraction) else v for k,v in ledger.items()},
            "attempt_history": history, "attempts_executed": len(history),
            "budget_failure_bound": str(delta**attempts),
            "uniform_independent_algorithm_coins_required": True,
            "seeded_control_not_empirical_probability_certificate": seed is not None,
            "norm_factors": s.norm_factors,
            "work": {"norm_candidate_checks": s.norm_checks, "square_table_entries": g.p,
                     "random_field_draws": len(history)*2*ledger["M"],
                     "linear_systems": len(history), "native_point_replays": 3*ledger["M"]
                     if result["status"] == "VERIFIED_NATIVE_PERFECT" else 0,
                     "scope": "named_work_counts_not_complete_bit_operation_or_memory_measurement"}}


def dual_derivative(s, coefficients):
    """Map a random center to one dual row-combination of the derivative."""
    p, r, M, D = s.g.p, s.ledger["parity_rank"], s.ledger["M"], s.ledger["flat_dimension"]
    if len(coefficients) != r or not any(coefficients):
        raise ValueError("nonzero parity dual vector required")
    for x in coefficients:
        integer(x, "dual entry", 0, p-1)
    weighted = [sum(coefficients[j]*int(s.hz[j,i]) for j in range(r))*s.b[i] % p for i in range(M)]
    return nmod_mat([[(-2*weighted[i]*int(s.wx[i,j])) % p for i in range(M)]
                     +[(2*s.nu*weighted[i]*int(s.wy[i,j])) % p for i in range(M)]
                    for j in range(D)], p)


def fixture(p, K, seed):
    """Reproducible native inputs, not planted solutions or oracle instances."""
    g = geometry(p, 3, K)
    rng = random.Random(seed)
    nu = next(x for x in range(2,p) if pow(x,(p-1)//2,p)==p-1)
    b = tuple(rng.randrange(1,p) for _ in g.points)
    allowed = tuple(tuple(sorted(rng.sample(range(p),(p-1)//2))) for _ in g.points)
    return g,b,nu,allowed
