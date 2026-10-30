"""Classical 2-jet falsifier for public formal F = ell composed with P^T.

P_i(x) = c_i + A_i x + x^T B_i x, with symmetric B_i over a prime field.
Gamma is the block-diagonal product UT_b(F_p), acting by x -> g x. Equality
means formal polynomial equality, not equality of functions on F_p^D.

For g in Gamma, N = g-I has N^b = 0 and b < p. Truncated exp/log are inverse
bijections. If g^T B g = B, then N^T B = B(g^{-1}-I), hence
log(g)^T B = B log(g^{-1}) = -B log(g). Conversely A^T B = -BA implies
exp(A)^T B = B exp(-A). These identities do not require B to be invertible.
The linear condition is likewise equivalent to b^T log(g) = 0. Thus exp of
the linear kernel is EXACTLY the finite 2-jet stabilizer, even at p=7,b=5.
No bound involving the degree of the full iterate is needed.

Jets at anchors fixed by all of Gamma may be stacked. The full formal
stabilizer is contained in the resulting jet upper group. A zero kernel
certifies the full stabilizer as the identity. For T <= 1 the full polynomial
has degree at most two, so the jet upper group is already the full answer.
Otherwise, exponentials of a
kernel basis generate the upper group (BCH in nilpotency class < p, or the
Frattini quotient of this exponent-p group). If every such generator commutes
with the public quadratic map P and fixes ell, it preserves every iterate;
the upper group is then the FULL stabilizer. Failed propagation is UNKNOWN,
not a smaller generator answer and not a hardness result.
T is charged in UNARY; this is not an algorithm polynomial in log(T).
No quantum execution, advantage, or new quantum candidate is claimed.
"""
from __future__ import annotations

from dataclasses import dataclass
import random

from flint import fmpz

from theorems.symbolic_scalar_phase_erasure import _fmpz_nullspace_basis


Vector = tuple[int, ...]
Matrix = tuple[Vector, ...]
Tensor = tuple[Matrix, ...]
SCHEMA_VERSION = "1.1"


def _canonical(value, shape: tuple[int, ...], p: int, name: str):
    if not shape:
        if type(value) is not int or not 0 <= value < p:
            raise ValueError(f"{name} requires canonical integer coefficients in [0, p)")
        return value
    if not isinstance(value, (list, tuple)) or len(value) != shape[0]:
        raise ValueError(f"{name} requires shape {shape}")
    return tuple(_canonical(item, shape[1:], p, name) for item in value)


@dataclass(frozen=True)
class QuadraticIteration:
    """Fully public coefficients; accepted list/tuple containers are frozen.

    The public linear functional ell must be nonzero. Coefficients must already
    be canonical: no reduction modulo p, coercion
    of floats/bools, or symmetrization is performed. D is inferred from c.
    Off-diagonal B_i entries contribute twice to the polynomial coefficient.
    """

    p: int
    block_size: int
    T: int
    c: Vector
    A: Matrix
    B: Tensor
    ell: Vector

    def __post_init__(self) -> None:
        if type(self.p) is not int or self.p <= 5 or not fmpz(self.p).is_prime():
            raise ValueError("p must be a prime integer greater than 5")
        if type(self.block_size) is not int or not 2 <= self.block_size <= 5:
            raise ValueError("block_size must be an integer from 2 through 5")
        if type(self.T) is not int or self.T < 0:
            raise ValueError("T must be a nonnegative integer, charged in unary")
        if not isinstance(self.c, (list, tuple)) or not self.c:
            raise ValueError("c must specify a positive dimension D")
        D = len(self.c)
        if D % self.block_size:
            raise ValueError("block_size must divide D")
        for name, shape in (("c", (D,)), ("A", (D, D)),
                            ("B", (D, D, D)), ("ell", (D,))):
            object.__setattr__(self, name, _canonical(getattr(self, name), shape, self.p, name))
        if not any(self.ell):
            raise ValueError("nonzero ell is required by the native input contract")
        if any(B[i][j] != B[j][i] for B in self.B for i in range(D) for j in range(i)):
            raise ValueError("every B_i must be symmetric")

    @property
    def D(self) -> int:
        return len(self.c)

    @property
    def lie_coordinates(self) -> tuple[tuple[int, int], ...]:
        return tuple((i, j) for i in range(self.D) for j in range(i + 1, self.D)
                     if i // self.block_size == j // self.block_size)

    def specification(self) -> dict:
        return {"p": self.p, "block_size": self.block_size, "T": self.T,
                "c": list(self.c), "A": [list(row) for row in self.A],
                "B": [[list(row) for row in B] for B in self.B], "ell": list(self.ell)}


def _identity(D: int) -> Matrix:
    return tuple(tuple(int(i == j) for j in range(D)) for i in range(D))


def _matmul(left: Matrix, right: Matrix, p: int) -> Matrix:
    columns = tuple(zip(*right))
    return tuple(tuple(sum(a * b for a, b in zip(row, col)) % p for col in columns)
                 for row in left)


@dataclass(frozen=True)
class VectorJet:
    v: Vector
    J: Matrix
    C: Tensor


@dataclass(frozen=True)
class ScalarJet:
    constant: int
    linear: Vector
    quadratic: Matrix


def _fixed_anchor(problem: QuadraticIteration, anchor) -> Vector:
    anchor = _canonical(anchor, (problem.D,), problem.p, "anchor")
    if any(value and i % problem.block_size != 0 for i, value in enumerate(anchor)):
        raise ValueError("anchor must be fixed by the whole Gamma: only block-first coordinates may be nonzero")
    return anchor


def iterate_jet(problem: QuadraticIteration, anchor=None) -> VectorJet:
    """Exact coefficients of P^T(anchor+x), with the full constant orbit.

    v' = P(v), U_ia = A_ia + 2(B_i v)_a, J' = U J,
    C'_i = sum_a U_ia C_a + J^T B_i J. All right sides use the OLD jet.
    The default anchor is zero. Every supplied anchor must be fixed by Gamma.
    Dense arithmetic uses O((T+1) D^4) field operations and O(D^3) storage.
    """
    D, p = problem.D, problem.p
    zero = tuple((0,) * D for _ in range(D))
    v = _fixed_anchor(problem, (0,) * D if anchor is None else anchor)
    J, C = _identity(D), (zero,) * D
    for _ in range(problem.T):
        Bv = tuple(tuple(sum(row[a] * v[a] for a in range(D)) % p for row in B)
                   for B in problem.B)
        U = tuple(tuple((problem.A[i][a] + 2 * Bv[i][a]) % p for a in range(D))
                  for i in range(D))
        next_v = tuple((problem.c[i] + sum(problem.A[i][a] * v[a] + v[a] * Bv[i][a]
                                         for a in range(D))) % p for i in range(D))
        transpose = tuple(zip(*J))
        next_C = []
        for i in range(D):
            pullback = _matmul(transpose, _matmul(problem.B[i], J, p), p)
            next_C.append(tuple(tuple((sum(U[i][a] * C[a][r][s] for a in range(D))
                                       + pullback[r][s]) % p for s in range(D))
                                for r in range(D)))
        v, J, C = next_v, _matmul(U, J, p), tuple(next_C)
    return VectorJet(v, J, C)


iterate_two_jet = iterate_jet


def scalar_two_jet(problem: QuadraticIteration, anchor=None) -> ScalarJet:
    jet = iterate_jet(problem, anchor)
    D, p, ell = problem.D, problem.p, problem.ell
    return ScalarJet(
        sum(ell[i] * jet.v[i] for i in range(D)) % p,
        tuple(sum(ell[i] * jet.J[i][j] for i in range(D)) % p for j in range(D)),
        tuple(tuple(sum(ell[i] * jet.C[i][r][s] for i in range(D)) % p
                    for s in range(D)) for r in range(D)),
    )


def _kernel_rows(jet: ScalarJet, coordinates, p: int) -> list[list[int]]:
    D, b, B = len(jet.linear), jet.linear, jet.quadratic
    rows = [[b[i] if j == s else 0 for i, j in coordinates] for s in range(D)]
    # Only the upper triangle is needed; the matrix equation is symmetric.
    rows.extend([((B[r][i] if j == s else 0) + (B[i][s] if j == r else 0)) % p
                 for i, j in coordinates] for r in range(D) for s in range(r, D))
    return rows


def _block_matrix(problem: QuadraticIteration, matrix, diagonal: int) -> Matrix:
    result = _canonical(matrix, (problem.D, problem.D), problem.p, "matrix")
    allowed = set(problem.lie_coordinates)
    if any(result[i][j] != (diagonal if i == j else 0)
           for i in range(problem.D) for j in range(problem.D) if (i, j) not in allowed):
        raise ValueError("matrix must have the specified block-unitriangular/strict-upper form")
    return result


def block_exp(problem: QuadraticIteration, lie_matrix: Matrix) -> Matrix:
    """Exponentiate a block-strict-upper matrix; this alone claims no symmetry."""
    A = _block_matrix(problem, lie_matrix, 0)
    p, D = problem.p, problem.D
    power = _identity(D)
    result = [list(row) for row in power]
    inverse_factorial = 1
    for k in range(1, problem.block_size):
        power = _matmul(power, A, p)
        inverse_factorial = inverse_factorial * pow(k, -1, p) % p
        for i in range(D):
            for j in range(D):
                result[i][j] = (result[i][j] + inverse_factorial * power[i][j]) % p
    return tuple(tuple(row) for row in result)


def block_log(problem: QuadraticIteration, group_matrix: Matrix) -> Matrix:
    """Logarithm of an element of Gamma, with no full-polynomial degree guard."""
    g = _block_matrix(problem, group_matrix, 1)
    p, D = problem.p, problem.D
    N = tuple(tuple((g[i][j] - int(i == j)) % p for j in range(D)) for i in range(D))
    power = _identity(D)
    result = [[0] * D for _ in range(D)]
    for k in range(1, problem.block_size):
        power = _matmul(power, N, p)
        coefficient = (-1 if k % 2 == 0 else 1) * pow(k, -1, p) % p
        for i in range(D):
            for j in range(D):
                result[i][j] = (result[i][j] + coefficient * power[i][j]) % p
    return tuple(tuple(row) for row in result)


def verify_propagation(problem: QuadraticIteration, group_matrix: Matrix) -> dict:
    """Exact coefficient test for P(gx)=gP(x) and ell*g=ell, not a PIT heuristic.

    Two dense matrix products cost O(D^3) per generator. The quadratic check
    explicitly loops over D output forms, O(D^2) entries, and b-by-b block
    index pairs, costing O(b^2 D^3). For b <= 5 and O(D) generators the total
    is O(D^4); no sparse matrix-multiplication optimization is assumed.
    """
    g = _block_matrix(problem, group_matrix, 1)
    D, p, b = problem.D, problem.p, problem.block_size
    blocks = [range(i // b * b, (i // b + 1) * b) for i in range(D)]
    constant = all(sum(g[i][j] * problem.c[j] for j in blocks[i]) % p == problem.c[i]
                   for i in range(D))
    linear = _matmul(problem.A, g, p) == _matmul(g, problem.A, p)
    quadratic = all(
        (sum(g[a][r] * problem.B[i][a][s0] * g[s0][s]
             for a in blocks[r] for s0 in blocks[s])
         - sum(g[i][j] * problem.B[j][r][s] for j in blocks[i])) % p == 0
        for i in range(D) for r in range(D) for s in range(r, D)
    )
    ell = all(sum(problem.ell[i] * g[i][j] for i in blocks[j]) % p == problem.ell[j]
              for j in range(D))
    return {"constant_fixed": constant, "linear_commutes": linear,
            "quadratic_equivariant": quadratic, "ell_fixed": ell,
            "passed": constant and linear and quadratic and ell}


def _scope_flags() -> dict:
    return {"all_input_coefficients_public": True, "no_quantum_execution": True,
            "no_advantage": True, "quantum_execution_performed": False,
            "quantum_advantage_claimed": False, "new_quantum_candidate": False,
            "hardness_promises": False, "hardness_claimed": False,
            "unchecked_kernel_basis_claimed_as_full_F_symmetries": False,
            "full_degree_guard_used": False, "actual_degree_claimed": False}


def analyze(problem: QuadraticIteration, anchors=None) -> dict:
    """Intersect fixed-anchor jet groups, then certify propagation if possible.

    The intersection is an exact finite jet group and an upper bound for the
    full formal stabilizer. At T <= 1 it is the full answer because F has
    degree at most two. Failed propagation does not show that the failing
    generator fails to preserve F; the propagation test is only sufficient.
    """
    if anchors is None:
        anchors = [(0,) * problem.D]
    if not isinstance(anchors, (list, tuple)) or not anchors:
        raise ValueError("anchors must be a nonempty list or tuple of Gamma-fixed anchors")
    anchors = tuple(_fixed_anchor(problem, anchor) for anchor in anchors)
    jets = [scalar_two_jet(problem, anchor) for anchor in anchors]
    coordinates = problem.lie_coordinates
    rows = [row for jet in jets for row in _kernel_rows(jet, coordinates, problem.p)]
    basis = _fmpz_nullspace_basis(rows, len(coordinates), problem.p)
    nullity = len(basis)
    D, m, R = problem.D, len(coordinates), len(rows)
    generators = []
    propagation = []
    for vector in basis:
        matrix = [[0] * D for _ in range(D)]
        for (i, j), value in zip(coordinates, vector):
            matrix[i][j] = value
        g = block_exp(problem, matrix)
        generators.append([list(row) for row in g])
        propagation.append(verify_propagation(problem, g))
    all_propagate = all(check["passed"] for check in propagation)
    completion_reason = (
        "ZERO_JET_KERNEL" if nullity == 0 else
        "EXACT_DEGREE_AT_MOST_TWO" if problem.T <= 1 else
        "EXACT_QUADRATIC_PROPAGATION" if all_propagate else None
    )
    complete = completion_reason is not None
    # Keep large powers exact without expanding decimal integers in JSON.
    order = {"base": problem.p, "exponent": nullity}
    serialized_jets = [{"constant": jet.constant, "linear": list(jet.linear),
                        "quadratic": [list(row) for row in jet.quadratic]} for jet in jets]
    return {
        "schema_version": SCHEMA_VERSION,
        "status": ("CERTIFIED_TRIVIAL_FULL_STABILIZER" if nullity == 0 else
                   "CERTIFIED_FULL_STABILIZER" if complete else "UNKNOWN_FULL_STABILIZER"),
        "input": problem.specification(),
        "anchors": [list(anchor) for anchor in anchors],
        "D": D, "group": "product UT_b(F_p), consecutive diagonal blocks, x -> g x",
        "equality_semantics": "formal polynomial equality over F_p, not pointwise function equality",
        "jet": serialized_jets[0], "anchor_jets": serialized_jets,
        "kernel_coordinates": [list(pair) for pair in coordinates],
        "kernel_basis": [list(row) for row in basis],
        "kernel_dimension": nullity, "constraint_rank": m - nullity,
        "finite_jet_stabilizer": "{exp(sum_i t_i K_i): t_i in F_p}, K_i from kernel_basis",
        "finite_jet_stabilizer_exact": True,
        "jet_upper_generators": generators,
        "propagation_checks": propagation,
        "all_upper_generators_propagate": all_propagate,
        "completion_reason": completion_reason,
        "full_stabilizer_generators": generators if complete else None,
        "full_stabilizer_certified": complete,
        "finite_jet_stabilizer_order": dict(order),
        "full_stabilizer_order_upper_bound": dict(order),
        "full_stabilizer_order": dict(order) if complete else None,
        "full_stabilizer_identity_certified": nullity == 0,
        "full_stabilizer_upper_bound_only": not complete,
        "formal_degree_upper_bound": {"base": 2, "exponent": problem.T},
        "degree_bound_description": "2^T is an upper bound, not the actual degree",
        "resources": {
            "T_encoding": "UNARY", "unary_iteration_units_charged": problem.T,
            "anchor_count": len(anchors), "jet_steps_executed": len(anchors) * problem.T,
            "field_element_bits": problem.p.bit_length(),
            "public_stored_field_coefficients": D ** 3 + D ** 2 + 2 * D,
            "public_anchor_field_coefficients": len(anchors) * D,
            "lie_variables": m, "linear_constraint_rows": R,
            "matrix_products": "Dense D-by-D loops, O(D^3) per product; no sparse multiplication",
            "jet_field_operations": "O(k (T+1) D^4), k = number of anchors",
            "nullspace_field_operations": "O(R m^2)",
            "propagation_generators_checked": len(generators),
            "generator_exponential_field_operations": "O(s b D^3), s = kernel_dimension; dense truncated matrix powers",
            "propagation_per_generator_field_operations": "O(b^2 D^3); two dense products plus explicit block-index quadratic loops",
            "propagation_field_operations": "O(D^4) for block_size <= 5",
            "total_field_operations": "O(k (T+1) D^4) for block_size <= 5",
            "field_storage": "O(D^3 + R m)",
            "bit_cost_note": "Exact modular arithmetic on O(log p)-bit field elements; prime validation also charged",
            "polynomial_in_log_T_claimed": False,
            "full_iterate_expanded": False, "finite_group_enumerated": False,
        },
        **_scope_flags(),
    }


def _seeded_forms(D: int, p: int, rng: random.Random) -> list[list[list[int]]]:
    forms = []
    for _ in range(D):
        B = [[0] * D for _ in range(D)]
        for i in range(D):
            for j in range(i, D):
                B[i][j] = B[j][i] = rng.randrange(1, p)
        forms.append(B)
    return forms


def report() -> dict:
    """Reproducible public fixtures and certificates; no files or CLI side effects."""
    dense_seed, mixed_seed = 20261029, 257
    rng = random.Random(dense_seed)
    D, p = 10, 101
    dense = QuadraticIteration(
        p, 5, 16, [rng.randrange(1, p) for _ in range(D)],
        [[rng.randrange(1, p) for _ in range(D)] for _ in range(D)],
        _seeded_forms(D, p, rng), [rng.randrange(1, p) for _ in range(D)],
    )
    D, p = 5, (1 << 61) - 1
    forms = _seeded_forms(D, p, random.Random(mixed_seed))
    forms[0] = _identity(D)
    near_identity = QuadraticIteration(p, 5, 257, [0] * D, _identity(D), forms, [1, 0, 0, 0, 0])
    forms = [[[0] * D for _ in range(D)] for _ in range(D)]
    forms[0][1][1] = forms[1][0][0] = 1
    unknown = QuadraticIteration(7, 5, 7, [0] * D, _identity(D), forms, [1, 0, 0, 0, 0])
    cases = []
    for name, seed, problem in (("dense_generic_quadratic", dense_seed, dense),
                                ("near_identity_high_degree_bound", mixed_seed, near_identity),
                                ("characteristic_cancellation_unknown", None, unknown)):
        cases.append({"name": name, "seed": seed, **analyze(problem)})
    cases.append({"name": "characteristic_cancellation_two_anchor_complete", "seed": None,
                  **analyze(unknown, anchors=[[0] * D, [1, 0, 0, 0, 0]])})
    return {"schema_version": SCHEMA_VERSION, "subsystem": "iterated_quadratic_jet",
            "proof_note": "research/ITERATED_QUADRATIC_JET_FILTER.md",
            "claim_scope": "Classical fixed-anchor jet upper group, with full equality certified by zero kernel, T <= 1, or exact propagation; no hardness promise",
            "cases": cases, **_scope_flags()}
