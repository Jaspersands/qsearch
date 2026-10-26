"""Capped classical orbit-span discovery from a public polynomial evaluator.

The caller supplies a genuine formal degree bound and an evaluator for an
explicit polynomial circuit, usable over extensions of F_p. This is NOT
an arbitrary hiding oracle. Polynomial identities are Monte Carlo checked
at fresh extension-field points. No monomials or group elements are
enumerated. Stabilizer solving after this representation is a separate
published matrix-group dependency, not implemented here.
"""
from collections import deque
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations
from math import factorial
import random

from flint import fmpz, fq_default_ctx

from theorems.symbolic_scalar_phase_erasure import _fmpz_solve_coordinates
from theorems.ut5_matrix_phase_alignment import (
    _canonical, _identity, _lists, _matrix, _product, _rank,
)


@dataclass(frozen=True)
class OrbitModule:
    status: str
    prime: int
    dimension: int
    degree_bound: int
    rank_cap: int
    basis_transforms: tuple
    generator_actions: tuple
    original_generators: tuple
    extension_degree: int
    modulus: tuple
    processed_candidates: int
    relation_tests: int
    evaluation_count: int
    error_bound: Fraction
    randomness: str
    evaluation_points: tuple
    basis_sketches: tuple

    @property
    def rank(self):
        return len(self.basis_transforms)

    @property
    def closed(self):
        return self.status == "CLOSED_MONTE_CARLO"

    @property
    def target(self):
        if not self.closed:
            raise ValueError("rank-capped output is not a representation")
        return (0,)*self.dimension+tuple(int(i == 0) for i in range(self.rank))

    @property
    def faithful_generators(self):
        """Retain the original group block: the orbit action may have kernel."""
        if not self.closed:
            raise ValueError("rank-capped output is not a representation")
        result = []
        for g, action in zip(self.original_generators, self.generator_actions):
            rows = [tuple(row)+(0,)*self.rank for row in g]
            rows += [(0,)*self.dimension+tuple(row) for row in action]
            result.append(tuple(rows))
        return tuple(result)


def orbit_module_budget(prime, degree_bound, generator_count, rank_cap,
                        error_budget=Fraction(1, 100)):
    if type(prime) is not int or prime < 2 or not fmpz(prime).is_prime():
        raise ValueError("prime required")
    if type(degree_bound) is not int or degree_bound < 0:
        raise ValueError("nonnegative formal degree bound required")
    if type(generator_count) is not int or generator_count < 0:
        raise ValueError("nonnegative generator count required")
    if type(rank_cap) is not int or rank_cap < 1:
        raise ValueError("positive integer rank cap required")
    if not isinstance(error_budget, Fraction) or not 0 < error_budget < 1:
        raise ValueError("exact error budget in (0,1) required")
    candidates = 1+generator_count*rank_cap
    k, q = 1, prime
    while degree_bound*candidates*error_budget.denominator > q*error_budget.numerator:
        k, q = k+1, q*prime
    return candidates, k, Fraction(degree_bound*candidates, q)


def discover_orbit_module(prime, dimension, evaluator, degree_bound, generators,
                          rank_cap, *, error_budget=Fraction(1, 100), seed=None):
    """Learn span{g.F:g in Gamma}, or exhibit rank_cap+1 independent translates.

    Action convention: (g.F)(x)=F(g^-1*x); returned matrices act on
    coefficient COLUMN vectors. The evaluator accepts (point, field).
    A seeded run is a reproducible diagnostic, not certified random
    sampling. The error bound assumes fresh independent uniform draws.
    FLINT supplies extension-field construction; its construction cost
    is not included in evaluation_count. No group promise is inferred.
    """
    generators = tuple(tuple(tuple(row) for row in g) for g in generators)
    limit, k, error = orbit_module_budget(prime, degree_bound, len(generators),
                                         rank_cap, error_budget)
    if type(dimension) is not int or dimension < 1:
        raise ValueError("positive matrix dimension required")
    if not callable(evaluator):
        raise ValueError("extension-field polynomial evaluator required")
    if seed is not None and type(seed) is not int:
        raise ValueError("integer diagnostic seed or None required")
    inverses = []
    for g in generators:
        if len(g) != dimension:
            raise ValueError("square generator of the stated dimension required")
        for row in g:
            _canonical(row, dimension, prime)
        if _rank(g, prime) != dimension:
            raise ValueError("invertible matrix generators required")
        inverses.append(tuple(map(tuple, _lists(_matrix(g, prime).inv()))))
    field = fq_default_ctx(prime, k)
    if not field.modulus().is_irreducible():
        raise ArithmeticError("extension modulus failed irreducibility verification")
    rng = random.SystemRandom() if seed is None else random.Random(seed)
    points, basis, basis_inverse, sketches, relations = [], [], [], [], {}
    evaluations = processed = tests = 0
    identity = tuple(map(tuple, _identity(dimension)))
    queue = deque([(None, identity, identity)])

    def value(inverse, point):
        nonlocal evaluations
        transformed = tuple(sum((a*x for a, x in zip(row, point)), field(0))
                            for row in inverse)
        evaluations += 1
        result = evaluator(transformed, field)
        # Addition coerces constants and rejects a mismatched FLINT field.
        return field(0)+result

    def digits(value):
        return tuple(int(a) for a in value.to_list())

    def finish(status):
        actions = []
        if status == "CLOSED_MONTE_CARLO":
            for j in range(len(generators)):
                columns = [relations[j, i]+(0,)*(len(basis)-len(relations[j, i]))
                           for i in range(len(basis))]
                action = tuple(tuple(columns[col][row] for col in range(len(basis)))
                               for row in range(len(basis)))
                if basis and _rank(action, prime) != len(basis):
                    raise ArithmeticError("learned generator action is singular; do not promote")
                actions.append(action)
        return OrbitModule(status, prime, dimension, degree_bound, rank_cap,
                           tuple(basis), tuple(actions), generators, k,
                           tuple(int(c) for c in field.modulus()), processed,
                           tests, evaluations, error,
                           "system_random" if seed is None else "seeded_diagnostic",
                           tuple(tuple(digits(x) for x in point) for point in points),
                           tuple(sketches))

    while queue:
        edge, g, inverse = queue.popleft()
        processed += 1
        if processed > limit:
            raise ArithmeticError("candidate clock exceeded")
        target = tuple(a for point in points for a in digits(value(inverse, point)))
        coeff = _fmpz_solve_coordinates(sketches, target, prime)
        if coeff is not None:
            # Coefficients are fixed BEFORE drawing this validation point.
            point = tuple(field([rng.randrange(prime) for _ in range(k)])
                          for _ in range(dimension))
            images = [value(b, point) for b in basis_inverse]
            candidate = value(inverse, point)
            tests += 1
            points.append(point)
            for i, image in enumerate(images):
                sketches[i] += digits(image)
            target += digits(candidate)
            if candidate != sum((c*v for c, v in zip(coeff, images)), field(0)):
                coeff = None
        if coeff is None:
            # Evaluation rank is an exact independence witness even on a
            # history containing a missed PIT error. Never truncate a basis.
            basis.append(g)
            basis_inverse.append(inverse)
            sketches.append(target)
            if len(basis) > rank_cap:
                return finish("RANK_CAP_EXCEEDED")
            coeff = (0,)*(len(basis)-1)+(1,)
            i = len(basis)-1
            for j, a in enumerate(generators):
                child = tuple(map(tuple, _product(a, g, prime)))
                child_inverse = tuple(map(tuple, _product(inverse, inverses[j], prime)))
                queue.append(((j, i), child, child_inverse))
        if edge is not None:
            relations[edge] = coeff
    return finish("CLOSED_MONTE_CARLO")


def verify_evaluation_rank(result, evaluator):
    """Replay an EXACT independence witness; does not verify PIT equalities."""
    from flint import fmpz_mod_poly_ctx

    field = fq_default_ctx(modulus=fmpz_mod_poly_ctx(result.prime)(list(result.modulus)))
    points = [tuple(field(list(x)) for x in point) for point in result.evaluation_points]
    sketches = []
    for g in result.basis_transforms:
        inverse = _lists(_matrix(g, result.prime).inv())
        sketch = []
        for point in points:
            transformed = tuple(sum((a*x for a, x in zip(row, point)), field(0))
                                for row in inverse)
            value = field(0)+evaluator(transformed, field)
            sketch.extend(int(a) for a in value.to_list())
        sketches.append(tuple(sketch))
    return tuple(sketches) == result.basis_sketches and _rank(sketches, result.prime) == result.rank


@dataclass(frozen=True)
class MooreMinor:
    """Explicit formal polynomial det(x_j^(p^i)), not an oracle problem.

    Its distinct coordinate minors are linearly independent formal
    polynomials and transform by exterior powers over the BASE field.
    They give an independent, exact checker for the learned representation.
    """
    prime: int
    dimension: int
    indices: tuple

    def __post_init__(self):
        orbit_module_budget(self.prime, 0, 0, 1)
        if type(self.dimension) is not int or self.dimension < 1:
            raise ValueError("positive dimension required")
        if (not isinstance(self.indices, tuple) or not self.indices or
                any(type(i) is not int or not 0 <= i < self.dimension for i in self.indices) or
                tuple(sorted(set(self.indices))) != self.indices):
            raise ValueError("nonempty increasing coordinate subset required")

    @property
    def degree_bound(self):
        return sum(self.prime**i for i in range(len(self.indices)))

    def __call__(self, point, field):
        if len(point) != self.dimension or int(field.characteristic()) != self.prime:
            raise ValueError("point dimension and characteristic must match")
        row = [point[j] for j in self.indices]
        matrix = []
        for _ in self.indices:
            matrix.append(row)
            row = [x.frobenius() for x in row]
        determinant = field(1)
        for j in range(len(matrix)):
            pivot = next((i for i in range(j, len(matrix)) if not matrix[i][j].is_zero()), None)
            if pivot is None:
                return field(0)
            if pivot != j:
                matrix[j], matrix[pivot] = matrix[pivot], matrix[j]
                determinant = -determinant
            diagonal = matrix[j][j]
            determinant *= diagonal
            for i in range(j+1, len(matrix)):
                ratio = matrix[i][j]/diagonal
                for col in range(j+1, len(matrix)):
                    matrix[i][col] -= ratio*matrix[j][col]
        return determinant

    def exterior_coefficients(self, transform):
        """Exact Cauchy-Binet coefficients; diagnostic cost binomial(D,k)."""
        inverse = _lists(_matrix(transform, self.prime).inv())
        return tuple(int(_matrix([[inverse[i][j] for j in cols] for i in self.indices],
                                 self.prime).det())
                     for cols in combinations(range(self.dimension), len(self.indices)))

    def verify_representation(self, result):
        """All generator identities as FORMAL polynomials, not sampled checks."""
        if (not result.closed or result.prime != self.prime or
                result.dimension != self.dimension or not result.rank or
                len(result.generator_actions) != len(result.original_generators) or
                result.basis_transforms[0] != tuple(map(tuple, _identity(self.dimension)))):
            return False
        if any(len(action) != result.rank or any(len(row) != result.rank for row in action)
               for action in result.generator_actions):
            return False
        vectors = [self.exterior_coefficients(g) for g in result.basis_transforms]
        if _rank(vectors, self.prime) != result.rank:
            return False
        for g, action in zip(result.original_generators, result.generator_actions):
            for j, b in enumerate(result.basis_transforms):
                target = self.exterior_coefficients(_product(g, b, self.prime))
                learned = tuple(sum(action[i][j]*v[t] for i, v in enumerate(vectors)) % self.prime
                                for t in range(len(target)))
                if learned != target:
                    return False
        return True


def _ut3_generators(dimension):
    generators = []
    for i, j in ((0, 1), (1, 2)):
        g = _identity(dimension)
        g[i][j] = 1
        generators.append(g)
    return generators


def _class_nine_generators(p):
    """The existing exp(J), exp(sum i^2 E_i,i+1) witness in UT(10,p)."""
    if p <= 9:
        raise ValueError("class-nine exponential requires p>9")
    generators = []
    for weights in ([1]*9, [(i+1)**2 for i in range(9)]):
        g = _identity(10)
        for i in range(10):
            product = 1
            for j in range(i+1, 10):
                product = product*weights[j-1] % p
                g[i][j] = product*pow(factorial(j-i), -1, p) % p
        generators.append(g)
    return generators


def baseline_report():
    from theorems.right_abelian_induced_source import derived_length_three_witness

    rows = []
    cases = [
        ("degree_p_frobenius_lift", MooreMinor(5, 6, (0, 1, 3, 4, 5)), _ut3_generators(6), 3),
        ("large_prime_moore_minor", MooreMinor(2**127-1, 3, (0, 1)), _ut3_generators(3), 3),
        ("actual_class_nine_ambient", MooreMinor(43, 10, tuple(range(9))), _class_nine_generators(43), 10),
    ]
    for name, polynomial, generators, cap in cases:
        result = discover_orbit_module(polynomial.prime, polynomial.dimension, polynomial,
                                       polynomial.degree_bound, generators, cap, seed=20261022)
        rank_verified = verify_evaluation_rank(result, polynomial)
        identities_verified = polynomial.verify_representation(result)
        if not result.closed or not rank_verified or not identities_verified:
            raise ArithmeticError("Moore baseline failed independent exact certification")
        rows.append({"name": name, "prime": polynomial.prime, "dimension": polynomial.dimension,
                     "moore_indices": polynomial.indices, "formal_degree": polynomial.degree_bound,
                     "rank": result.rank, "faithful_dimension": polynomial.dimension+result.rank,
                     "processed_candidates": result.processed_candidates, "relation_tests": result.relation_tests,
                     "circuit_evaluations": result.evaluation_count, "extension_degree": result.extension_degree,
                     "pit_error_bound_ideal_randomness": str(result.error_bound), "randomness": result.randomness,
                     "exact_evaluation_rank_verified": rank_verified,
                     "exact_exterior_generator_identities_verified": identities_verified,
                     "classification": "classical reduction to explicit matrix vector stabilizer",
                     "stabilizer_backend_executed": False})
    high = discover_orbit_module(127, 3, lambda x, field: x[0]**126, 126,
                                 _ut3_generators(3), 5, seed=20261022)
    if high.status != "RANK_CAP_EXCEEDED" or not verify_evaluation_rank(high, lambda x, field: x[0]**126):
        raise ArithmeticError("rank-cap negative control failed")
    return {"schema": "polynomial_orbit_module_classical_filter_v1", "seed": 20261022,
            "scope": "explicit public polynomial circuits over extension fields; not arbitrary HSP oracles",
            "controls": rows,
            "class_nine_group": derived_length_three_witness(43)[2],
            "rank_cap_control": {"polynomial": "x0^126 over F127", "group": "UT(3,127)",
                                 "rank_cap": 5, "independent_translates": high.rank, "status": high.status,
                                 "exact_rank_verified": True, "hardness_inferred": False,
                                 "known_formal_stabilizer": "a=c=0 in [[1,a,c],[0,1,b],[0,0,1]]",
                                 "reason": "unique factorization gives an easy stabilizer despite large orbit rank"},
            "published_dependency": "https://ix.cs.uoregon.edu/~luks/solmatgrp.pdf, Theorem 3.2(5)",
            "not_established": ["general matrix stabilizer backend implemented", "new quantum algorithm",
                                "hardness when rank cap is exceeded", "novelty of the classical reduction",
                                "degree/evaluator contract for arbitrary callbacks"]}


def main():
    import argparse
    import json
    from pathlib import Path

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = baseline_report()
    encoded = json.dumps(report, indent=2)+"\n"
    if args.write:
        root = Path(__file__).resolve().parents[1]
        (root/"research/classical_baselines/polynomial_orbit_module.json").write_text(encoded)
    print(encoded, end="")


if __name__ == "__main__":
    main()
