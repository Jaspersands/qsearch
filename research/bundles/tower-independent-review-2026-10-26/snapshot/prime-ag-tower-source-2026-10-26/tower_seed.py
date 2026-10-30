"""Check a concrete prime-field tower seed, not a generated tower or speedup.

The bridge from the checked Kummer data to an infinite tower uses the written
proof and Schoof's class-field-tower theorem in TOWER_SOURCE.md.
"""

from dataclasses import dataclass
from fractions import Fraction
from math import prod

from flint import fmpz


PRIME = 100003
BRANCHES = tuple(range(13))
SPLITTING_X = (18501, 29631, 37154, 37155, 40763, 48611,
               48612, 48613, 48614, 48615, 51887)


def checked_prime(prime):
    if (type(prime) is not int or not 3 <= prime < 2**63
            or not fmpz(prime).is_prime()):
        raise ValueError("verified odd prime below 2^63 required")


def canonical_distinct(values, prime, label):
    values = tuple(values)
    if (not values or any(type(x) is not int or not 0 <= x < prime for x in values)
            or len(set(values)) != len(values)):
        raise ValueError(f"{label}: distinct canonical field entries required")
    return values


@dataclass(frozen=True)
class TowerSeed:
    prime: int
    branches: tuple
    splitting_x: tuple

    def __post_init__(self):
        checked_prime(self.prime)
        branches = canonical_distinct(self.branches, self.prime, "branches")
        xs = canonical_distinct(self.splitting_x, self.prime, "splitting x")
        if len(branches) < 5 or len(branches) % 2 != 1:
            raise ValueError("odd squarefree split polynomial of degree >=5 required")
        if self.prime % 4 != 3:
            raise ValueError("this seed verifier uses square roots only for p=3 mod 4")
        if any(pow((x-a) % self.prime, (self.prime-1)//2, self.prime) != 1
               for x in xs for a in branches):
            raise ValueError("every x-a must be a NONZERO square")
        object.__setattr__(self, "branches", branches)
        object.__setattr__(self, "splitting_x", xs)

    @property
    def genus(self):
        return (len(self.branches)-1)//2

    def certificate(self):
        points = []
        for x in self.splitting_x:
            roots = [pow((x-a) % self.prime, (self.prime+1)//4, self.prime)
                     for a in self.branches]
            y = prod(roots) % self.prime
            points.append({"x": x, "square_roots": roots, "y_pair": [y, (-y) % self.prime]})
        rank = len(self.branches)-1
        split_count = 2*len(points)+1
        margin = (rank-2)**2-4*(split_count+1)
        return {
            "prime": self.prime, "branches": list(self.branches), "genus": self.genus,
            "affine_splitting_pairs": points, "infinity_in_splitting_set": True,
            "splitting_places": split_count, "kummer_rank_over_base": rank,
            "explicit_elementary_cover_degree": 2**rank,
            "schoof_squared_margin": margin,
            "schoof_sufficient_criterion": rank >= 2 and margin >= 0,
            "external_theorem_required": "Schoof 1992 Theorem 2.3",
            "proof_status": "WRITTEN_DEDUCTION_NOT_INDEPENDENTLY_REVIEWED",
            "infinite_tower_implemented": False, "native_parity_matrix_constructed": False,
            "quantum_advantage_established": False, "registry_admission": False,
        }


def default_seed():
    return TowerSeed(PRIME, BRANCHES, SPLITTING_X)


def verify_certificate(certificate):
    """Recompute all fields, including roots; never trust serialized booleans."""
    try:
        xs = tuple(item["x"] for item in certificate["affine_splitting_pairs"])
        seed = TowerSeed(certificate["prime"], tuple(certificate["branches"]), xs)
        return seed.certificate() == certificate
    except (KeyError, TypeError, ValueError):
        return False


def scan_consecutive_square_runs(prime=PRIME, degree=13, count=11):
    """Deterministic discovery replay, with every Legendre test counted."""
    checked_prime(prime)
    if (type(degree) is not int or not 1 <= degree < prime
            or type(count) is not int or count < 1):
        raise ValueError("positive degree < prime and positive count required")
    run, found = 0, []
    for x in range(1, prime):
        run = run+1 if pow(x, (prime-1)//2, prime) == 1 else 0
        if run >= degree:
            found.append(x)
            if len(found) == count:
                return {"x_values": found, "legendre_tests": x, "status": "FOUND"}
    return {"x_values": found, "legendre_tests": prime-1, "status": "CAP_EXHAUSTED_UNKNOWN"}


def kummer_quotient_rank(degree):
    """F2 valuation classes of x-a_i modulo the single product relation."""
    if type(degree) is not int or degree < 1:
        raise ValueError("positive integer degree required")
    relation = (1 << degree)-1
    pivots = {}
    for i in range(degree):
        vector = 1 << i
        if vector & (1 << (degree-1)):
            vector ^= relation
        while vector:
            pivot = vector.bit_length()-1
            if pivot not in pivots:
                pivots[pivot] = vector
                break
            vector ^= pivots[pivot]
    return len(pivots)


def specialization(cover_degree):
    """Theorem-implied AG dimensions, not a matrix or a constructed level.

Use G=10*pi^*(infinity)+3R and all lifts of the 22 finite seed points.
Intermediate degrees 2^j exist in the infinite pro-2 extension, but their
selection and Riemann-Roch computations are not implemented here.
"""
    if (type(cover_degree) is not int or cover_degree < 1
            or cover_degree & (cover_degree-1)):
        raise ValueError("positive power-of-two cover degree required")
    e = cover_degree
    g, d, m = 5*e+1, 10*e+3, 22*e
    k, w = d-g+1, 2*d-g+1
    valid = m > 2*d
    return {
        "cover_degree": e, "genus": g, "divisor_degree": d, "length": m,
        "dimension": k, "square_dimension_if_valid": w if valid else None,
        "standard_ag_range": valid, "designed_dual_distance": m-d,
        "cubic_completion_sufficient": m > 3*d-g+1,
        "rational_gonality_lower": (23*e+PRIME)//(PRIME+1),
        "full_parity_matrix_entries": k*m,
        "matrix_entry_bits": PRIME.bit_length(),
        "status": "THEOREM_IMPLIED_PARAMETERS_NOT_A_GENERATED_MATRIX",
        "requires_verified_seed_and_written_geometric_argument": True,
        "efficient_uniform_generator_proved": False,
        "quantum_advantage_established": False,
    }


def exact_small_quantum_bounds(cover_degree):
    """Exact sufficient bounds only for bounded controls, no code enumeration."""
    info = specialization(cover_degree)
    if not info["standard_ag_range"] or cover_degree > 32:
        raise ValueError("requires standard AG range and cover degree <=32")
    k, w = info["dimension"], info["square_dimension_if_valid"]
    m, d = info["length"], info["divisor_degree"]
    error = Fraction((PRIME**k-1)*PRIME**w, (PRIME-1)**m)
    tail = Fraction(PRIME**k-1, (PRIME-1)**(m-d))
    success = max(Fraction(0), (1-error)/(1+tail))
    return {"E_upper": error, "A_tail_upper": tail, "ideal_success_lower": success,
            "requires_unreviewed_usd_reduction": True,
            "native_parity_matrix_constructed": False, "quantum_execution": False}


def asymptotic_quantum_certificate():
    """Integer checks for E < p^9 (2/p^2)^e, all dyadic e>=8."""
    bernoulli_margin = PRIME-44
    start_bound = Fraction(2**8, PRIME**7)
    ratio = Fraction(2, PRIME**2)
    if bernoulli_margin <= 0 or not 0 < ratio < 1 or not start_bound < 1:
        raise ArithmeticError("coarse bound failed")
    return {"coarse_E_formula": "p^9 * (2/p^2)^e", "minimum_cover_degree": 8,
            "bernoulli_margin_p_minus_44": bernoulli_margin,
            "E_upper_at_e8": start_bound, "per_degree_ratio": ratio,
            "status": "CONDITIONAL_ON_WRITTEN_AG_AND_USD_ARGUMENTS",
            "all_dyadic_e_ge_8_bound_nonvacuous": True,
            "quantum_advantage_established": False}


def persistent_section_bound(extra_degree, punctures, *, full_kummer_inclusion_asserted):
    """Conditional section count, not a verifier for an arbitrary cover."""
    if (type(extra_degree) is not int or extra_degree < 3
            or type(punctures) is not int or punctures < 0
            or type(full_kummer_inclusion_asserted) is not bool):
        raise ValueError("effective extra degree >=3, nonnegative punctures, boolean premise")
    bound = max(0, 93-3*extra_degree-punctures) if full_kummer_inclusion_asserted else None
    return {"annihilator_dimension_lower": bound,
            "inclusion_premise_verified_by_this_helper": False,
            "requires_effective_E_and_effective_punctures": True,
            "requires_G_equals_canonical_plus_E": True,
            "quantum_advantage_established": False,
            "status": "CONDITIONAL_SECTION_COUNT" if bound else "NO_CERTIFICATE_NOT_HARDNESS"}
