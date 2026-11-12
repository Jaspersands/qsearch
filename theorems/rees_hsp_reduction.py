"""Positive Rees cover for ordinary-oracle Lazard HSP.

Public algebra/compiler and exact resource accounting, NOT a quantum
receiver. No hidden subgroup, potential, or reference decoder is an input.
The construction uses gamma_r(L), not gamma_r(L)/gamma_(r+1)(L).
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from itertools import combinations
import json
from math import gcd
from pathlib import Path

from flint import fmpz

from theorems.central_character_descent import tree_budget
from theorems.full_jet_resource_certificate import sde_arity
from theorems.uniform_bch_rees import bch_via_ode
from theorems.nil3_complete_budget import ceil_log
from theorems.symbolic_scalar_phase_erasure import PublicLieAlgebra, _fmpz_solve_coordinates


def _units(n):
    return tuple(tuple(int(i == j) for j in range(n)) for i in range(n))


def _canonical(vector, width, p):
    if len(vector) != width or any(type(x) is not int or not 0 <= x < p for x in vector):
        raise ValueError("canonical field coordinates required")


def _linear(vector, basis, width, p):
    return tuple(sum(a*b[j] for a, b in zip(vector, basis)) % p for j in range(width))


def _tensor_algebra(p, dimension, tensor):
    sparse = tuple((i, j, tuple((k, x) for k, x in enumerate(row) if x))
                   for (i, j), row in tensor.items() if any(row))
    def bracket(left, right):
        result = [0]*dimension
        for i, j, row in sparse:
            scale = left[i]*right[j] % p
            if scale:
                for k, value in row:
                    result[k] += scale*value
        return tuple(x % p for x in result)
    return PublicLieAlgebra(p, dimension, bracket)


@dataclass(frozen=True)
class ReesCover:
    """A = sum_(r=1..c) gamma_r(L)t^r with public evaluation maps.

All operational brackets use frozen, validated structure constants.
ambient_basis maps local L coordinates to original oracle logarithms.
"""
    source: PublicLieAlgebra
    algebra: PublicLieAlgebra
    ambient_basis: tuple
    ambient_width: int
    levels: tuple
    indices: tuple
    inverse_evaluation: tuple

    @property
    def p(self):
        return self.source.p

    @property
    def class_bound(self):
        return len(self.levels)

    @property
    def dimensions(self):
        return tuple(map(len, self.levels))

    @property
    def dimension(self):
        return self.algebra.dimension

    @property
    def points(self):
        return tuple(range(1, self.class_bound+1))

    def coefficients(self, vector):
        _canonical(vector, self.dimension, self.p)
        rows = [[0]*self.source.dimension for _ in self.levels]
        for a, (r, j) in zip(vector, self.indices):
            if a:
                rows[r-1] = [(x+a*y) % self.p for x, y in zip(rows[r-1], self.levels[r-1][j])]
        return tuple(map(tuple, rows))

    def evaluate(self, vector, point):
        if type(point) is not int or not 0 <= point < self.p:
            raise ValueError("canonical evaluation point required")
        coefficients = self.coefficients(vector)
        value = _linear(tuple(pow(point, r, self.p) for r in self.points),
                        coefficients, self.source.dimension, self.p)
        return _linear(value, self.ambient_basis, self.ambient_width, self.p)

    def inputs(self, vector):
        return tuple(self.evaluate(vector, point) for point in self.points)

    def evaluate_fixture(self, original_oracle, vector):
        """Exactly c calls to the original oracle; classical control only."""
        return tuple(original_oracle(x) for x in self.inputs(vector))

    def recover_coefficients(self, evaluations):
        """Public interpolation in ORIGINAL ambient coordinates, no H input."""
        if len(evaluations) != self.class_bound:
            raise ValueError("exactly c evaluation vectors required")
        for v in evaluations:
            _canonical(v, self.ambient_width, self.p)
        return tuple(_linear(row, evaluations, self.ambient_width, self.p) for row in self.inverse_evaluation)

    def dilate(self, vector, scale):
        _canonical(vector, self.dimension, self.p)
        if type(scale) is not int or not 0 < scale < self.p:
            raise ValueError("nonzero canonical scale required")
        return tuple(a*pow(scale, r, self.p) % self.p for a, (r, _) in zip(vector, self.indices))

    def multiply(self, left, right):
        _canonical(left, self.dimension, self.p)
        _canonical(right, self.dimension, self.p)
        return bch_via_ode(left, right, prime=self.p,
                          nilpotency_class=self.class_bound, bracket=self.algebra.bracket)


def make_rees_cover(algebra, ambient_basis):
    """Freeze public basis brackets, verify Lie identities, then form the cover.

The callable input is interpreted only through its basis structure
constants. Bilinearity is imposed by reconstruction, not inferred from
finite tests of an arbitrary callable. No field-sized table is built.
"""
    basis = tuple(algebra.span(ambient_basis))
    n, p = len(basis), algebra.p
    if not n:
        raise ValueError("nonzero public ambient required")
    tensor = {}
    for i, a in enumerate(basis):
        for j, b in enumerate(basis):
            row = _fmpz_solve_coordinates(basis, algebra.bracket(a, b), p)
            if row is None:
                raise ValueError("public ambient not bracket closed")
            tensor[i, j] = tuple(row)
    for i in range(n):
        if any(tensor[i, i]):
            raise ValueError("nonalternating structure constants")
        for j in range(n):
            if any((x+y) % p for x, y in zip(tensor[i, j], tensor[j, i])):
                raise ValueError("nonantisymmetric structure constants")
    source = _tensor_algebra(p, n, tensor)
    units = _units(n)
    for i, j, k in combinations(range(n), 3):
        terms = [source.bracket(units[a], tensor[b, c]) for a, b, c in ((i, j, k), (j, k, i), (k, i, j))]
        if any(sum(row[t] for row in terms) % p for t in range(n)):
            raise ValueError("Jacobi identity failed")
    levels = tuple(tuple(row) for row in source.lower_central_series(units)[:-1])
    c = len(levels)
    if c >= p:
        raise ValueError("Lazard input requires class<p")
    indices = tuple((r, j) for r, level in enumerate(levels, 1) for j in range(len(level)))
    positions = {key: i for i, key in enumerate(indices)}
    cover_tensor = {}
    for i, (r, a) in enumerate(indices):
        for j, (s, b) in enumerate(indices):
            value = source.bracket(levels[r-1][a], levels[s-1][b])
            if r+s > c:
                if any(value):
                    raise ArithmeticError("discarded bracket is nonzero: not a Rees cover")
                continue
            coordinates = _fmpz_solve_coordinates(levels[r+s-1], value, p)
            if coordinates is None:
                raise ArithmeticError("lower central filtration is not multiplicative")
            row = [0]*len(indices)
            for k, x in enumerate(coordinates):
                row[positions[r+s, k]] = x
            if any(row):
                cover_tensor[i, j] = tuple(row)
    cover = _tensor_algebra(p, len(indices), cover_tensor)
    evaluation = [tuple(pow(s, r, p) for r in range(1, c+1)) for s in range(1, c+1)]
    inverse = tuple(_fmpz_solve_coordinates(evaluation, row, p) for row in _units(c))
    if any(row is None for row in inverse):
        raise ArithmeticError("singular nonzero-point Vandermonde matrix")
    return ReesCover(source, cover, basis, algebra.dimension, levels, indices, tuple(map(tuple, inverse)))


def zero_sum_length(p, kappa):
    """Least t >= 2 with z_1^kappa+...+z_t^kappa = 0 for NONZERO z_i in F_p (kappa | p-1).

    Equivalently the least number of elements of the subgroup P of nonzero
    kappa-th powers (order h = (p-1)/kappa) with sum 0.  Exact:
    t = 2 iff -1 in P iff h is even (kappa = 1 gives h = p-1 even);
    t <= 3 once p+1-(kappa-1)(kappa-2)sqrt(p) > 3 kappa (Hasse-Weil on the
    smooth Fermat curve, minus at most 3 kappa points with xyz = 0);
    otherwise breadth-first search on the Cayley graph Cay(F_p, P), where
    t = 1 + dist(0, -1).  Chevalley-Warning gives t <= kappa+1.
    """
    if type(p) is not int or p < 2 or not fmpz(p).is_prime():
        raise ValueError("prime p required")
    if type(kappa) is not int or kappa < 1 or (p-1) % kappa:
        raise ValueError("positive kappa dividing p-1 required")
    h = (p-1)//kappa
    if h % 2 == 0:
        return 2
    if kappa > 1:
        slack = p+1-3*kappa
        genus2 = (kappa-1)*(kappa-2)
        if slack > 0 and slack*slack > genus2*genus2*p:
            return 3
    powers = {pow(x, kappa, p) for x in range(1, p)}
    if len(powers) != h:
        raise ArithmeticError("kappa-th power subgroup has the wrong order")
    if any((-1-x) % p in powers for x in powers):
        return 3
    dist = {0: 0}
    frontier = [0]
    while (p-1) not in dist:
        nxt = []
        for x in frontier:
            for y in powers:
                z = (x+y) % p
                if z not in dist:
                    dist[z] = dist[x]+1
                    nxt.append(z)
        frontier = nxt
    t = dist[p-1]+1
    if t > kappa+1:
        raise ArithmeticError("Chevalley-Warning bound t <= kappa+1 violated")
    return t


def schedule1_zero_sum_depth(p, degree):
    """L_d = ceil(log2 t(p, kappa_d)), kappa_d = gcd(d, p-1): the Schedule 1 rounds charged."""
    if type(degree) is not int or degree < 1:
        raise ValueError("positive integer degree required")
    kappa = gcd(degree, p-1)
    return kappa, (zero_sum_length(p, kappa)-1).bit_length()


def zero_sum_sde_arity(p, degree, equations):
    """Public Schedule 1 arity G(kappa_d, a)^{L_d} (a+1 when kappa_d = 1).

    Never exceeds the published sde_arity(degree, equations) = B_d(a), since
    kappa_d <= d and L_d <= ceil(log2(kappa_d+1)) <= ceil(log2(d+1)).
    """
    if type(equations) is not int or equations < 0:
        raise ValueError("nonnegative integer equation count required")
    kappa, depth = schedule1_zero_sum_depth(p, degree)
    if kappa == 1:
        return equations+1
    return (kappa**(kappa*(kappa-1)//2)*(equations+1)**kappa)**depth


def _zero_sum_pattern(p, class_bound):
    return tuple(schedule1_zero_sum_depth(p, d) for d in range(2, class_bound+1))


@lru_cache(maxsize=None)
def zero_sum_depth_patterns(class_bound):
    """Every (kappa_d, L_d)_{d=2..c} pattern over ALL primes p > c, with one prime realizing it.

    Primes c < p < 4c^4 are enumerated.  For p >= 4c^4 >= 4 kappa^4 the Weil
    bound gives t <= 3, so L_d = 1 if (p-1)/kappa_d is even and 2 otherwise;
    the pattern then depends only on p mod N = 2^(J+1) * odd part of
    lcm(1..c), J = floor(log2 c), and by Dirichlet every unit class mod N
    contains primes >= 4c^4 (one is found and recorded for each class).
    """
    if type(class_bound) is not int or class_bound < 1:
        raise ValueError("positive integer class bound required")
    c = class_bound
    patterns = {}
    if c == 1:
        return {(): 2}
    bound = 4*c**4
    for p in range(c+1, bound):
        if fmpz(p).is_prime():
            patterns.setdefault(_zero_sum_pattern(p, c), p)
    modulus = 1
    for d in range(2, c+1):
        modulus = modulus*d//gcd(modulus, d)
    modulus = modulus*2**(c.bit_length())//gcd(modulus, 2**(c.bit_length()))
    for r in range(1, modulus):
        if gcd(r, modulus) != 1:
            continue
        p = r+modulus*((bound-r)//modulus+1)
        while not fmpz(p).is_prime():
            p += modulus
        pattern = _zero_sum_pattern(p, c)
        expected = tuple((gcd(d, r-1) if r > 1 else d,) for d in range(2, c+1))
        if tuple((k,) for k, _ in pattern) != expected:
            raise ArithmeticError("residue-class pattern does not match gcd(d, r-1)")
        patterns.setdefault(pattern, p)
    return patterns


def zero_sum_depth_exponent(class_bound):
    """max over primes p > c of 1 + sum_d kappa_d L_d, with a maximizing prime (smallest found)."""
    best = None
    for pattern, p in zero_sum_depth_patterns(class_bound).items():
        value = 1+sum(k*depth for k, depth in pattern)
        if best is None or value > best[0] or (value == best[0] and p < best[1]):
            best = (value, p)
    return best


def _pattern_arities(pattern, equations_top_down):
    """Arities top-down (d = c..2) for a pattern listed bottom-up (d = 2..c)."""
    out = []
    for (kappa, depth), a in zip(reversed(pattern), equations_top_down):
        out.append(a+1 if kappa == 1 else (kappa**(kappa*(kappa-1)//2)*(a+1)**kappa)**depth)
    return tuple(out)


def _worst_zero_sum_arities(class_bound, equations_top_down):
    """Pattern maximizing the tree size prod M_d over all primes p > c (ties: smallest prime)."""
    best = None
    for pattern, p in zero_sum_depth_patterns(class_bound).items():
        arities = _pattern_arities(pattern, equations_top_down)
        leaves = tree_budget(arities)["source_leaves"] if arities else 1
        if best is None or leaves > best[0] or (leaves == best[0] and p < best[2]):
            best = (leaves, arities, p, pattern)
    return best[1], best[2], best[3]


def recovery_budget(cover, error=Fraction(1, 3), depth="published"):
    """Fresh-copy trees AND final readout; excludes unimplemented gate synthesis.

    depth="published" (default): Schedule 1 at degree d with B_d (published theorem).
    depth="zero_sum_instance": arity G(kappa_d, g_d)^{L_d} at the cover's own prime.
    depth="zero_sum_worst": the same arity maximized (as a whole tree) over all primes p > c,
    a p-uniform count like B_d; rank error and slack stay at the cover's prime.
    In both zero-sum modes query_dimension_exponent is the max over p > c of 1+sum kappa_d L_d.

    Classical SDE attempts run on saved measured labels before any dilation.
    Given a uniform expected-time bound T (including witness verification),
    fresh-seed attempts capped at 2T fail with probability at most 1/2 each.
    They neither remeasure nor replace the already conditioned source bank.
    This is a conditional clock certificate, not an implemented solver.
    """
    if not isinstance(error, Fraction) or not 0 < error < 1:
        raise ValueError("exact error Fraction in (0,1) required")
    c, n, p = cover.class_bound, cover.source.dimension, cover.p
    equations = tuple(cover.dimensions[d-1] for d in range(c, 1, -1))
    if depth == "published":
        arities = tuple(sde_arity(d, a) for d, a in zip(range(c, 1, -1), equations))
        exponent = 1+sum(d*d.bit_length() for d in range(2, c+1))
        arity_prime = None
    elif depth == "zero_sum_instance":
        arities = tuple(zero_sum_sde_arity(p, d, a) for d, a in zip(range(c, 1, -1), equations))
        exponent = zero_sum_depth_exponent(c)[0]
        arity_prime = p
    elif depth == "zero_sum_worst":
        arities, arity_prime, _ = _worst_zero_sum_arities(c, equations)
        exponent = zero_sum_depth_exponent(c)[0]
    else:
        raise ValueError("depth must be 'published', 'zero_sum_instance' or 'zero_sum_worst'")
    tree = tree_budget(arities)
    slack = ceil_log(p, 3/error)
    samples = n+slack
    leaves = samples*tree["source_leaves"]
    solvers = samples*sum(tree["stage_calls"])
    instruments = leaves+solvers+samples
    solver_error = error/(3*solvers) if solvers else Fraction(0)
    restarts = ceil_log(2, 1/solver_error) if solvers else 0
    rank_error = Fraction(1, (p-1)*p**slack)
    return {"original_dimension": n, "cover_dimension": cover.dimension, "class": c,
            "grade_dimensions": cover.dimensions, "queries_per_leaf": c,
            "stage_arities_top_down": arities, "final_fourier_samples": samples,
            "source_preparations": leaves, "sde_calls": solvers,
            "final_fourier_readout_calls": samples,
            "complete_instrument_calls": instruments, "original_queries": c*leaves,
            "rank_failure_bound": rank_error,
            "solver_abort_per_call": solver_error,
            "classical_sde_attempts_per_call": restarts,
            "classical_sde_abort_bound_per_call": Fraction(1, 2**restarts) if solvers else Fraction(0),
            "classical_sde_attempt_cap": solvers*restarts,
            "classical_restart_extra_source_copies": 0,
            "instrument_error_per_call": error/(3*instruments),
            "total_error_bound": rank_error+(error/3 if solvers else 0)+error/3,
            "query_dimension_exponent": exponent,
            "schedule1_depth": depth, "arity_prime": arity_prime}


def black_box_large_prime_budget(encoding_bits, class_bound, error=Fraction(1, 3), depth="published"):
    """Conditional envelope for large-prime CORE calls, not a total gate bound.

    The imported outer reduction and input conversion are NOT implemented.
    Fixed class, unique encodings, and ordinary coherent f are premises.
    Small-prime algorithms and group/coordinate preprocessing are excluded
    from the numerical query bound, but receive explicit error allocations.
    depth="published" charges B_d; depth="zero_sum_worst" charges the
    zero-sum-depth Schedule 1 arity maximized over all primes p > c.
    """
    if any(type(x) is not int or x < 1 for x in (encoding_bits, class_bound)):
        raise ValueError("positive integer encoding width and fixed class required")
    if not isinstance(error, Fraction) or not 0 < error < 1:
        raise ValueError("exact error Fraction in (0,1) required")
    b, c = encoding_bits, class_bound
    cap = b*(b+1)
    local_error = error/(4*cap)
    slack = ceil_log(2, 12*cap/error)
    if depth == "published":
        arities = tuple(sde_arity(d, b) for d in range(c, 1, -1))
        exponent = 3+sum(d*d.bit_length() for d in range(2, c+1))
        arity_prime = None
    elif depth == "zero_sum_worst":
        arities, arity_prime, _ = _worst_zero_sum_arities(c, (b,)*(c-1))
        exponent = 2+zero_sum_depth_exponent(c)[0]
    else:
        raise ValueError("depth must be 'published' or 'zero_sum_worst'")
    tree = tree_budget(arities)
    queries = cap*c*(b+slack)*tree["source_leaves"]
    return {
        "encoding_bits": b, "fixed_class_bound": c,
        "large_prime_call_cap": cap, "small_prime_call_cap": c,
        "chart_error_per_call": local_error, "core_error_per_call": local_error,
        "small_prime_error_per_call": error/(4*c),
        "preprocessing_error_allocation": error/4,
        "total_allocated_error": error,
        "uniform_fourier_slack": slack,
        "local_rank_failure_bound": Fraction(1, 2**slack),
        "large_prime_original_query_bound": queries,
        "large_prime_query_dimension_exponent": exponent,
        "schedule1_depth": depth, "arity_prime": arity_prime,
        "conditional_on_rees_core": True,
        "outer_normalizer_recursion_required": True,
        "outer_reduction_implemented": False,
        "covers_small_prime_queries": False,
        "covers_group_preprocessing_cost": False,
        "is_total_gate_bound": False,
    }


def binary_zero_sum_support(prime, labels, power_witness):
    """Check a degree-(p-1) witness and extract a NONEMPTY zero-sum subset.

    Fermat turns each nonzero weight into 1. This validates a supplied
    witness; it does not implement the fixed-degree diagonal solver.
    Unlike the Lazard core, this check includes p=2.
    """
    if type(prime) is not int or prime < 2 or not fmpz(prime).is_prime():
        raise ValueError("prime field required")
    labels = tuple(tuple(row) for row in labels)
    weights = tuple(power_witness)
    if not labels or not labels[0] or len(labels) != len(weights):
        raise ValueError("nonempty equally sized label and witness lists required")
    width = len(labels[0])
    if any(len(row) != width for row in labels):
        raise ValueError("consistent label width required")
    if any(type(x) is not int or not 0 <= x < prime
           for row in labels for x in row):
        raise ValueError("canonical prime-field labels required")
    if any(type(x) is not int or not 0 <= x < prime for x in weights):
        raise ValueError("canonical prime-field witness required")
    active = tuple(i for i, x in enumerate(weights) if x)
    if not active or any(sum(labels[i][j] for i in active) % prime for j in range(width)):
        raise ValueError("witness must give a nonempty zero-sum subset")
    return active


def black_box_copy_budget(encoding_bits, class_bound, error=Fraction(1, 3), depth="published"):
    """Conditional original-coset-copy envelope for ALL fixed-class nilpotent G.

    Fresh mixed coset copies replace f queries. Public group inverses are
    still required; no inverse of an UNKNOWN source is supplied. The
    small-prime branch uses forward-only zero-sum descent and bounded-error
    Fourier sampling. Neither branch nor public preprocessing is executed.
    """
    large = black_box_large_prime_budget(encoding_bits, class_bound, error, depth)
    b, c = encoding_bits, class_bound
    small_primes = tuple(p for p in range(2, c+1) if fmpz(p).is_prime())
    arities = tuple((p, sde_arity(p-1, b)) for p in small_primes)
    # At kappa = p-1 the least zero sum has t = p terms, so ceil(log2 t) = ceil(log2(kappa+1)):
    # the zero-sum depth leaves the small-prime arities unchanged.
    if depth != "published" and any(zero_sum_sde_arity(p, p-1, b) != s for p, s in arities):
        raise ArithmeticError("zero-sum depth changed a small-prime arity")
    worst_arity = max((s for _, s in arities), default=1)
    cap = b*(b+1)
    samples = b+large["uniform_fourier_slack"]
    # Across small-prime Sylows, sum of squared composition lengths <= b^2.
    small_calls = cap if small_primes else 0
    small_copies = small_calls*samples*worst_arity**(c-1)
    large_copies = large["large_prime_original_query_bound"]
    small_exponent = (3+(c-1)*max((p-1)*(p-1).bit_length() for p in small_primes)
                      if small_primes else None)
    return {
        "encoding_bits": b, "fixed_class_bound": c,
        "large_prime_local_call_cap": cap, "small_prime_hsmc_call_cap": small_calls,
        "small_primes": small_primes, "small_prime_zero_sum_arities": arities,
        "small_prime_descent_depth_bound": c-1,
        "final_fourier_samples_per_call": samples,
        "large_prime_original_copy_bound": large_copies,
        "small_prime_original_copy_bound": small_copies,
        "total_original_copy_bound": large_copies+small_copies,
        "large_prime_copy_dimension_exponent": large["large_prime_query_dimension_exponent"],
        "small_prime_copy_dimension_exponent": small_exponent,
        "preprocessing_error_allocation": error/4,
        "chart_error_per_large_prime_call": error/(4*cap),
        "large_prime_error_per_call": error/(4*cap),
        "small_prime_error_per_hsmc_call": error/(4*cap) if small_primes else Fraction(0),
        "unused_small_prime_error_allocation": Fraction(0) if small_primes else error/4,
        "local_rank_failure_bound": large["local_rank_failure_bound"],
        "total_error_allocation": error,
        "source_contract": "fresh_IID_exact_mixed_coset_states_in_original_unique_group_encoding",
        "ordinary_hiding_function_required": False,
        "unknown_source_preparation_inverse_required": False,
        "coherent_public_group_operations_required": True,
        "public_presentation_and_coordinate_acquisition_charged": True,
        "normalizer_recursion_required": True,
        "conditional_on_rees_core": True,
        "all_hidden_source_copy_calls_covered": True,
        "public_group_operation_count_included": False,
        "general_diagonal_solver_implemented": False,
        "quantum_receiver_implemented": False,
        "outer_reduction_implemented": False,
        "is_total_gate_bound": False,
        "speedup_claim_allowed": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    from theorems.right_abelian_induced_source import derived_length_three_witness
    algebra, ambient, *_ = derived_length_three_witness(43)
    cover = make_rees_cover(algebra, ambient)

    def profile_of(budget):
        profile = {key: budget[key] for key in ("original_dimension", "cover_dimension", "class",
                   "grade_dimensions", "queries_per_leaf", "final_fourier_samples", "query_dimension_exponent",
                   "final_fourier_readout_calls", "classical_sde_attempts_per_call",
                   "classical_restart_extra_source_copies")}
        profile["original_queries_ceil_log2"] = (budget["original_queries"]-1).bit_length()
        profile["complete_instrument_calls_ceil_log2"] = (budget["complete_instrument_calls"]-1).bit_length()
        profile["instrument_error_per_call"] = str(budget["instrument_error_per_call"])
        profile["classical_sde_abort_bound_per_call"] = str(budget["classical_sde_abort_bound_per_call"])
        profile["readout_included_in_instrument_budget"] = True
        profile["total_error_bound"] = str(budget["total_error_bound"])
        return profile

    def outer_of(outer):
        outer_profile = {key: value for key, value in outer.items()
                         if not isinstance(value, Fraction) and key != "large_prime_original_query_bound"}
        outer_profile["large_prime_original_queries_ceil_log2"] = (outer["large_prime_original_query_bound"]-1).bit_length()
        outer_profile["status"] = "conditional_worst_case_envelope_not_executed_group_algorithm"
        outer_profile["scope_audit"] = "research/REES_WHOLE_PROOF_SCOPE_AUDIT.md"
        return outer_profile

    def copy_of(copies):
        copy_profile = {key: str(value) if isinstance(value, Fraction) else value
                        for key, value in copies.items() if not key.endswith("_copy_bound")}
        for key in ("large_prime_original", "small_prime_original", "total_original"):
            count = copies[key+"_copy_bound"]
            copy_profile[key+"_copies_ceil_log2"] = (count-1).bit_length() if count else None
        copy_profile["status"] = "conditional_copy_only_scope_correction_not_executed_receiver"
        copy_profile["scope_audit"] = "research/REES_COPY_ONLY_OUTER_REDUCTION.md"
        return copy_profile

    bits = (cover.p**cover.source.dimension-1).bit_length()
    budget = recovery_budget(cover, depth="zero_sum_worst")
    profile = profile_of(budget)
    exponent, exponent_prime = zero_sum_depth_exponent(cover.class_bound)
    profile["schedule1_depth_rule"] = "L_d = ceil(log2 t_d), t_d least nonzero zero sum of kappa_d-th powers, kappa_d = gcd(d,p-1)"
    profile["arity_maximizing_prime"] = budget["arity_prime"]
    profile["query_dimension_exponent_maximizing_prime"] = exponent_prime
    instance = recovery_budget(cover, depth="zero_sum_instance")
    instance_profile = profile_of(instance)
    instance_profile["prime"] = cover.p
    instance_profile["stage_depths_bottom_up"] = [list(x) for x in _zero_sum_pattern(cover.p, cover.class_bound)]
    outer_profile = outer_of(black_box_large_prime_budget(bits, cover.class_bound, depth="zero_sum_worst"))
    copy_profile = copy_of(black_box_copy_budget(bits, cover.class_bound, depth="zero_sum_worst"))
    published = {"schedule1_depth_rule": "ceil(log2(d+1)) at degree d: B_d of eq:Bd (published thm:main)",
                 "profile": profile_of(recovery_budget(cover))}
    published_outer = outer_of(black_box_large_prime_budget(bits, cover.class_bound))
    published_copy = copy_of(black_box_copy_budget(bits, cover.class_bound))
    published["large_prime_outer_envelope"] = {key: published_outer[key] for key in (
        "large_prime_query_dimension_exponent", "large_prime_original_queries_ceil_log2")}
    published["copy_only_outer_envelope"] = {key: published_copy[key] for key in (
        "large_prime_copy_dimension_exponent", "small_prime_copy_dimension_exponent",
        "large_prime_original_copies_ceil_log2", "small_prime_original_copies_ceil_log2",
        "total_original_copies_ceil_log2")}
    report = {"status": "provisional_Rees_homogenization_and_general_central_descent_not_discovery",
              "input_model": "explicit odd-prime F_p Lie constants, fixed class c<p, coherent ordinary hiding function",
              "profile": profile, "hidden_advice_inputs": [],
              "normalizer_recursion_required": False, "transversality_required": False,
              "coherent_receiver_implemented": False, "general_sde_implemented": False,
              "formal_draft": "formal/drafts/ReesHomogenization.lean", "formal_compiler_checked": False,
              "independent_review": False, "novelty_established": False, "speedup_claim_allowed": False,
              "conditional_black_box_scope": "fixed-class finite nilpotent groups via paid published reductions; proof under review",
              "large_prime_outer_envelope": outer_profile,
              "copy_only_outer_envelope": copy_profile,
              "zero_sum_depth_instance_profile": instance_profile,
              "published_depth_profile": published,
              "review_manuscript": "research/manuscripts/rees_hsp_review.tex",
              "research_note": "research/REES_HSP_REDUCTION.md"}
    if args.write:
        path = Path(__file__).resolve().parents[1]/"research/reductions/rees_hsp_reduction.json"
        path.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
