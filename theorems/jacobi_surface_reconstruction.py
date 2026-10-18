"""Exact Jacobi/CM experiment for split Fermat SURFACES, not a quantum oracle.

Input p prime, d|(p-1), surface X^d+Y^d+Z^d=W^d. All calibration sums are
computed CLASSICALLY by explicit characters. Quantum PIP/unit-group/phase
routines are published dependencies, NOT implemented or replaced by these
sums. Test the actual arithmetic reduction, a public ideal-lattice attack,
and conditions required before a new algorithm claim could be made.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import itertools
import json
import math
from pathlib import Path
import sys

from flint import fmpz_mat, fmpz_poly
from sympy import Poly, cyclotomic_poly, factorint, isprime, primitive_root

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
ARTIFACT = ROOT / "research/classical_baselines/jacobi_surface_reconstruction.json"


class Cyclotomic:
    """Exact Z[zeta_d] arithmetic using the standard monic cyclotomic basis."""

    def __init__(self, d: int):
        if type(d) is not int or not 3 <= d <= 24:
            raise ValueError("reference conductor must be 3..24; a cap is not hardness evidence")
        self.d = d
        self.modulus = fmpz_poly([int(c) for c in reversed(Poly(cyclotomic_poly(d)).all_coeffs())])
        self.degree = self.modulus.degree()
        self.units = tuple(t for t in range(1, d) if math.gcd(t, d) == 1)

    def reduce(self, values) -> tuple[int, ...]:
        poly = fmpz_poly(list(values)) % self.modulus
        return tuple(int(poly[j]) for j in range(self.degree))

    def constant(self, value: int) -> tuple[int, ...]:
        return self.reduce([value])

    def root(self, exponent: int) -> tuple[int, ...]:
        values = [0] * self.d
        values[exponent % self.d] = 1
        return self.reduce(values)

    def add(self, a, b) -> tuple[int, ...]:
        return tuple(x + y for x, y in zip(a, b))

    def scale(self, a, scalar: int) -> tuple[int, ...]:
        return tuple(scalar * x for x in a)

    def multiply(self, a, b) -> tuple[int, ...]:
        return self.reduce(fmpz_poly(list(a)) * fmpz_poly(list(b)))

    def conjugate(self, a) -> tuple[int, ...]:
        result = self.constant(0)
        for j, c in enumerate(a):
            result = self.add(result, self.scale(self.root(-j), c))
        return result

    def evaluate_mod(self, a, root: int, modulus: int) -> int:
        value = 0
        for coefficient in reversed(a):
            value = (value * root + coefficient) % modulus
        return value

    @property
    def roots_of_unity_order(self) -> int:
        return math.lcm(2, self.d)

    def unit_root(self, index: int) -> tuple[int, ...]:
        index %= self.roots_of_unity_order
        # For odd d, -zeta_d^((d+1)/2)=exp(2*pi*i/(2d)).
        if self.d % 2:
            return self.scale(self.root(index * ((self.d + 1) // 2)), (-1) ** index)
        return self.root(index)


class ReferenceCharacters:
    """EXHAUSTIVE classical sum source; never a polynomial quantum subroutine."""

    def __init__(self, p: int, d: int, *, residue_root: int | None = None):
        self.field = Cyclotomic(d)
        if type(p) is not int or p >= 2 ** 64 or not isprime(p) or (p - 1) % d:
            raise ValueError("public arithmetic requires prime p<2^64 and d|(p-1)")
        if residue_root is None and p > 20000:
            raise ValueError("large public inputs must supply a verified order-d residue root")
        self.p, self.d = p, d
        self.generator = int(primitive_root(p)) if residue_root is None else None
        self.root = pow(self.generator, (p - 1) // d, p) if residue_root is None else residue_root
        if (type(self.root) is not int or not 0 < self.root < p or pow(self.root, d, p) != 1
                or any(pow(self.root, d // ell, p) == 1 for ell in factorint(d))):
            raise ValueError("residue root must have EXACT order d")
        self._indices = None
        self.pairs = {}
        self.triples = {}
        self.reference_summands = 0

    @property
    def indices(self):
        if self.p > 20000:
            raise ValueError("exhaustive reference sum capped at p<=20000; unsupported is not hard")
        if self._indices is None:
            lookup = {pow(self.root, j, self.p): j for j in range(self.d)}
            self._indices = [None] + [lookup[pow(x, (self.p - 1) // self.d, self.p)] for x in range(1, self.p)]
        return self._indices

    def pair(self, a: int, b: int) -> tuple[int, ...]:
        key = tuple(sorted((a % self.d, b % self.d)))
        if key not in self.pairs:
            histogram = [0] * self.d
            for x in range(2, self.p):
                histogram[(key[0] * self.indices[x] + key[1] * self.indices[(1 - x) % self.p]) % self.d] += 1
            self.reference_summands += self.p - 2
            self.pairs[key] = self.field.reduce(histogram)
        return self.pairs[key]

    def triple(self, abc) -> tuple[int, ...]:
        key = tuple(sorted(int(x) % self.d for x in abc))
        if len(key) != 3 or any(x == 0 for x in key) or sum(key) % self.d == 0:
            raise ValueError("three nontrivial characters with nontrivial total product required")
        if key not in self.triples:
            a, b, c = key
            if (a + b) % self.d == 0:
                # The t=0 convolution mass is essential here. Omitting it
                # would incorrectly return a root of unity instead of p times it.
                self.triples[key] = self.field.scale(self.field.root(a * self.indices[-1]), self.p)
            else:
                self.triples[key] = self.field.multiply(self.pair(a, b), self.pair((a + b) % self.d, c))
        return self.triples[key]

    def teichmuller_root(self, t: int, precision: int) -> int:
        if t not in self.field.units or type(precision) is not int or not 1 <= precision <= 4:
            raise ValueError("a Galois unit and precision1..4 required")
        return pow(pow(self.root, t, self.p), self.p ** (precision - 1), self.p ** precision)

    def reference_local_unit(self, abc, t: int, digits: int) -> dict:
        """VALUATION-AWARE native reference, not compact quantum-output division."""
        exponent = dict(valuation_profile(abc, self.d))[t]
        if type(digits) is not int or not 1 <= digits <= 2:
            raise ValueError("request one or two unit-part digits")
        precision = digits + exponent
        value = self.triple(abc)
        residue = self.field.evaluate_mod(value, self.teichmuller_root(t, precision), self.p ** precision)
        if residue % self.p ** exponent:
            raise ArithmeticError("local division used an incorrect valuation")
        unit = (residue // self.p ** exponent) % self.p ** digits
        assert unit % self.p
        return {"valuation": exponent, "unit_residue": unit, "unit_modulus": self.p ** digits,
                "required_input_precision": precision, "compact_division_implemented": False}


def valuation_profile(abc, d: int) -> tuple[tuple[int, int], ...]:
    a = tuple(abc)
    if len(a) != 3 or any(type(x) is not int or not 0 < x < d for x in a) or sum(a) % d == 0:
        raise ValueError("admissible nontrivial triple required")
    # POSITIVE embedding zeta -> g^((p-1)t/d). The inverse embedding has
    # the complementary carry; never silently interchange the conventions.
    profile = tuple((t, 2 - sum((x * t) % d for x in a) // d)
                    for t in range(1, d) if math.gcd(t, d) == 1)
    mapping = dict(profile)
    assert all(mapping[t] + mapping[d - t] == 2 for t in mapping)
    return profile


def surface_bound(d: int) -> int:
    if type(d) is not int or d < 3:
        raise ValueError("surface degree must be >=3")
    return (d - 1) * (d * d - 3 * d + 3)


def lift_surface_residue(p: int, d: int, residue: int) -> dict:
    """Recover the integer correction ONLY when the Weil interval is unique."""
    bound, modulus = surface_bound(d) * p, p * p
    residue %= modulus
    first = -((bound + residue) // modulus)
    last = (bound - residue) // modulus
    count = max(0, last - first + 1)
    if count == 0:
        raise ValueError("residue has no lift inside the supplied Weil interval")
    if count != 1:
        return {"status": "AMBIGUOUS_USE_SMALL_PRIME_CLASSICAL_BRANCH", "lift_count": count,
                "weil_absolute_bound": bound, "modulus": modulus}
    correction = residue + first * modulus
    return {"status": "UNIQUE_INTEGER_LIFT", "correction": correction,
            "point_count": p * p + p + 1 + correction,
            "weil_absolute_bound": bound, "modulus": modulus}


def native_surface_count(p: int, d: int) -> dict:
    """Independent exact classical baseline using a full prime-length product.

    This is polynomial in p, NOT log p. If p<=2B=O(d^3), it is a legitimate
    polynomial-in-degree fallback. Outside that regime it is reference work.
    """
    histogram = [0] * p
    for x in range(p):
        histogram[pow(x, d, p)] += 1
    square = fmpz_poly(histogram) ** 2
    convolution = [int(square[j]) + int(square[j + p]) for j in range(p)]
    affine = sum(convolution[t] * histogram[(1 - t) % p] for t in range(p))
    zero_at_infinity = sum(convolution[t] * histogram[-t % p] for t in range(p))
    assert (zero_at_infinity - 1) % (p - 1) == 0
    return {"point_count": affine + (zero_at_infinity - 1) // (p - 1),
            "affine_chart_count": affine, "projective_boundary_count": (zero_at_infinity - 1) // (p - 1),
            "full_table_entries": p, "integer_polynomial_degree": p - 1,
            "polynomial_in_log_p_algorithm": False}


def public_ideal_basis(source: ReferenceCharacters, abc) -> tuple[fmpz_mat, int]:
    """Build ideal lattice from PUBLIC carry constraints, never the true sum.

    At each new split prime some basis evaluation is a unit, because all
    previously imposed prime ideals are coprime. Kernel elimination gives
    the correct index p**sum(e_t); determinant is checked exactly.
    """
    field, p = source.field, source.p
    n = field.degree
    basis = [[int(i == j) for j in range(n)] for i in range(n)]
    index = 1
    for t, exponent in valuation_profile(abc, source.d):
        if exponent == 0:
            continue
        modulus = p ** exponent
        root = source.teichmuller_root(t, exponent)
        evaluations = [field.evaluate_mod(row, root, modulus) for row in basis]
        pivot = next((j for j, value in enumerate(evaluations) if math.gcd(value, p) == 1), None)
        if pivot is None:
            raise ArithmeticError("public split-prime kernel lost surjectivity")
        row = basis[pivot][:]
        inverse = pow(evaluations[pivot], -1, modulus)
        for j in range(n):
            if j != pivot:
                multiplier = evaluations[j] * inverse % modulus
                basis[j] = [x - multiplier * y for x, y in zip(basis[j], row)]
        basis[pivot] = [modulus * value for value in row]
        index *= modulus
    matrix = fmpz_mat(basis)
    if abs(int(matrix.det())) != index or index != p ** n:
        raise ArithmeticError("public ideal lattice index failed exact norm check")
    return matrix, index


def classical_lll_attempt(source: ReferenceCharacters, abc) -> dict:
    """A deterministic classical attack on the actual public ideal.

    Test every reduced row for alpha*conjugate(alpha)=p^2, not for equality
    with the true Jacobi sum. Success gives a balanced generator UP TO a
    root of unity, not the exact character-dependent Jacobi sum.
    """
    basis, index = public_ideal_basis(source, abc)
    reduced = basis.lll()
    field = source.field
    attempts = []
    for i in range(field.degree):
        row = tuple(int(reduced[i, j]) for j in range(field.degree))
        norm_product = field.multiply(row, field.conjugate(row))
        checks = []
        for t, exponent in valuation_profile(abc, source.d):
            if exponent:
                checks.append(field.evaluate_mod(row, source.teichmuller_root(t, exponent), source.p ** exponent) == 0)
        assert all(checks)
        attempts.append({"coefficients": list(row), "relative_norm": list(norm_product),
                         "balanced_generator_found": norm_product == field.constant(source.p ** 2)})
    return {"triple": list(abc), "lattice_index": str(index), "field_degree": field.degree,
            "row_attempts": attempts, "balanced_generator_found": any(r["balanced_generator_found"] for r in attempts),
            "used_true_jacobi_sum": False, "exact_jacobi_phase_identified": False,
            "no_row_success_is_not_hardness": True}


def identify_root_turns(estimate: Fraction, error_bound: Fraction, root_order: int) -> int:
    """Certified nearest root from a circular phase INTERVAL, in turns.

    Phases must come from charged, controlled-precision routines. This does
    not manufacture a phase estimate from an unknown algebraic number.
    """
    if not isinstance(estimate, Fraction) or not isinstance(error_bound, Fraction):
        raise ValueError("exact rational phase interval required")
    if type(root_order) is not int or root_order < 2 or not 0 <= error_bound < Fraction(1, 2 * root_order):
        raise ValueError("phase uncertainty must be below half the root spacing")
    scaled = estimate * root_order + Fraction(1, 2)
    nearest = scaled.numerator // scaled.denominator
    distance = abs(estimate - Fraction(nearest, root_order))
    if distance + error_bound >= Fraction(1, 2 * root_order):
        raise ValueError("phase interval crosses a root-selection boundary")
    return nearest % root_order


def primary_normalize(field: Cyclotomic, candidate, p: int) -> tuple[int, ...]:
    """For odd PRIME conductor, fix the root WITHOUT phase or a true sum.

    J(chi^a,chi^b,chi^c)=1 mod(1-zeta)^2. In this quotient a polynomial
    has residue1 iff A(1)=1 and A'(1)=0 mod d. All 2d roots have distinct
    residues. Ideal membership must ALSO be checked by the caller.
    """
    if not isprime(field.d):
        raise ValueError("primary normalization here is proved only for odd prime conductors")
    if field.multiply(candidate, field.conjugate(candidate)) != field.constant(p * p):
        raise ValueError("same ideal alone does not give a norm-normalized generator")
    matches = []
    for k in range(field.roots_of_unity_order):
        value = field.multiply(field.unit_root(-k), candidate)
        if sum(value) % field.d == 1 and sum(j * c for j, c in enumerate(value)) % field.d == 0:
            matches.append(value)
    if len(matches) != 1:
        raise ArithmeticError("primary congruence did not select a unique root")
    return matches[0]


def public_surface_attempt(source: ReferenceCharacters) -> dict:
    """Real CLASSICAL LLL+primary attempt; failure is UNKNOWN, not hardness.

    No true character sums or phase estimates are used, even to choose rows.
    Reuse identical ideal profiles. A completed result has exact norm,
    membership, index and primary-congruence certificates, subject to the
    stated local mathematical derivation, not an independent proof audit.
    """
    if not isprime(source.d):
        raise ValueError("public phase-free reconstruction currently requires prime conductor")
    field, p, d = source.field, source.p, source.d
    multiplicities = Counter(tuple(sorted(a)) for a in itertools.product(range(1, d), repeat=3) if sum(a) % d)
    profiles, by_profile, triple_records = [], {}, []
    total = field.constant(0)
    unresolved = []
    for abc, multiplicity in sorted(multiplicities.items()):
        profile = tuple(e for _, e in valuation_profile(abc, d))
        if profile not in by_profile:
            attack = classical_lll_attempt(source, abc)
            normalized = None
            for row in attack["row_attempts"]:
                if row["balanced_generator_found"]:
                    normalized = primary_normalize(field, row["coefficients"], p)
                    break
            by_profile[profile] = len(profiles)
            profiles.append({"valuation_profile": list(profile), "representative_triple": list(abc),
                             "lll_attempt": attack,
                             "primary_normalized_coefficients": list(normalized) if normalized is not None else None})
        record_index = by_profile[profile]
        normalized = profiles[record_index]["primary_normalized_coefficients"]
        triple_records.append({"characters": list(abc), "multiplicity": multiplicity, "profile_index": record_index})
        if normalized is None:
            unresolved.append(list(abc))
        else:
            total = field.add(total, field.scale(normalized, multiplicity))
    if unresolved:
        return {"status": "NO_BALANCED_LLL_ROW_UNKNOWN", "unresolved_triples": unresolved,
                "profiles": profiles, "triples": triple_records, "point_count": None,
                "failure_is_not_hardness": True}
    if total[1:] != (0,) * (field.degree - 1) or abs(total[0]) > surface_bound(d) * p:
        raise ArithmeticError("public reconstructed orbit sum fails rationality or Weil bound")
    return {"status": "CLASSICAL_PUBLIC_IDEAL_RECONSTRUCTION_COMPLETED",
            "point_count": p * p + p + 1 + total[0], "correction": total[0],
            "profiles": profiles, "triples": triple_records,
            "used_true_jacobi_sum_or_phase": False, "worst_case_polynomial_LLL_success_proved": False}


def surface_control(p: int, d: int) -> dict:
    source = ReferenceCharacters(p, d)
    field = source.field
    multiplicities = Counter(tuple(sorted(a)) for a in itertools.product(range(1, d), repeat=3) if sum(a) % d)
    assert sum(multiplicities.values()) == surface_bound(d)
    total = field.constant(0)
    triples = []
    for abc, multiplicity in sorted(multiplicities.items()):
        value = source.triple(abc)
        if field.multiply(value, field.conjugate(value)) != field.constant(p * p):
            raise ArithmeticError("native Jacobi relative norm failed")
        profile = valuation_profile(abc, d)
        actual_valuations = []
        for t, predicted in profile:
            residue = field.evaluate_mod(value, source.teichmuller_root(t, 3), p ** 3)
            observed = 0
            while observed < 3 and residue % p == 0:
                residue //= p
                observed += 1
            if observed != predicted:
                raise ArithmeticError("positive-embedding carry convention failed native valuation")
            actual_valuations.append([t, observed])
        total = field.add(total, field.scale(value, multiplicity))
        triples.append({"characters": list(abc), "ordered_multiplicity": multiplicity,
                        "coefficients": list(value), "positive_embedding_valuations": actual_valuations,
                        "residue_mod_prime_square": field.evaluate_mod(value, source.teichmuller_root(1, 2), p * p)})
    if total[1:] != (0,) * (field.degree - 1):
        raise ArithmeticError("complete Jacobi orbit sum is not a rational integer")
    correction = total[0]
    native = native_surface_count(p, d)
    if native["point_count"] != p * p + p + 1 + correction:
        raise ArithmeticError("native surface count disagrees with exact Jacobi formula")
    residue = field.evaluate_mod(total, source.teichmuller_root(1, 2), p * p)
    lifted = lift_surface_residue(p, d, residue)
    if lifted["status"] == "UNIQUE_INTEGER_LIFT":
        assert lifted["point_count"] == native["point_count"]
    keys = sorted(multiplicities)
    # Fixed public indices, no success-dependent source/ideal selection.
    chosen = [keys[j] for j in sorted({0, len(keys) // 4, len(keys) // 2, 3 * len(keys) // 4, len(keys) - 1})]
    attacks = [classical_lll_attempt(source, abc) for abc in chosen]
    public_reconstruction = public_surface_attempt(source) if isprime(d) else None
    if public_reconstruction and public_reconstruction["point_count"] is not None:
        if public_reconstruction["point_count"] != native["point_count"]:
            raise ArithmeticError("phase-free classical public-ideal reconstruction failed native count")
    phase_controls = []
    for attack in attacks:
        abc = tuple(attack["triple"])
        truth = source.triple(abc)
        for row in attack["row_attempts"]:
            if row["balanced_generator_found"]:
                candidates = [k for k in range(field.roots_of_unity_order)
                              if field.multiply(field.unit_root(k), truth) == tuple(row["coefficients"])]
                assert len(candidates) == 1
                k, w = candidates[0], field.roots_of_unity_order
                recovered = identify_root_turns(Fraction(k, w) + Fraction(1, 16 * w), Fraction(1, 8 * w), w)
                assert recovered == k
                restored = field.multiply(field.unit_root(-recovered), row["coefficients"])
                assert restored == truth
                phase_controls.append({"triple": list(abc), "root_order": w, "true_root_index": k,
                                       "recovered_from_synthetic_phase_interval": recovered,
                                       "true_sum_used_only_for_validation": True,
                                       "exact_adjusted_generator_matches_reference": True,
                                       "quantum_phase_estimation_executed": False})
    return {"prime": p, "surface_degree": d, "cyclotomic_polynomial": [int(x) for x in field.modulus],
            "generator": source.generator, "positive_residue_root": source.root,
            "primitive_betti_count_B": surface_bound(d), "point_count": native["point_count"],
            "correction": correction, "native_classical_baseline": native,
            "reference_character_table_entries": p - 1, "reference_pair_summands": source.reference_summands,
            "triple_records": triples, "integer_reconstruction": lifted,
            "theoretical_branch": "PRIME_SQUARE_FROM_UNIMPLEMENTED_QUANTUM_RESIDUES" if p > 2 * surface_bound(d) else "CHARGED_SMALL_P_CLASSICAL_FALLBACK",
            "classical_ideal_lll_attempts": attacks, "root_phase_validation": phase_controls,
            "classical_phase_free_surface_attempt": public_reconstruction,
            "known_cubic_closed_form": p * p + 7 * p + 1 if d == 3 else None,
            "jacobi_source": "EXHAUSTIVE_CLASSICAL_REFERENCE_NOT_QUANTUM_PIP",
            "quantum_PIP_unit_or_phase_subroutine_executed": False}


def large_public_ideal_control() -> dict:
    """Known 61-bit Mersenne prime: no p-sized table or true sum is accessed."""
    p, d = 2 ** 61 - 1, 11
    attempts = 0
    root = None
    for base in range(2, 100):
        attempts += 1
        candidate = pow(base, (p - 1) // d, p)
        if candidate != 1:
            root = candidate
            break
    if root is None:
        raise ArithmeticError("bounded public root construction found no order11 root")
    source = ReferenceCharacters(p, d, residue_root=root)
    result = classical_lll_attempt(source, (1, 2, 4))
    reconstructed = public_surface_attempt(source)
    if source._indices is not None or source.reference_summands:
        raise ArithmeticError("public ideal attack illegally materialized a reference sum")
    return {"prime": p, "conductor": d, "residue_root": root,
            "public_modular_power_attempts": attempts, "classical_lll_attempt": result,
            "classical_phase_free_surface_attempt": reconstructed,
            "character_table_materialized": False, "quantum_subroutine_executed": False}


def run_controls() -> dict:
    specs = [(7, 3), (13, 3), (13, 4), (61, 4), (11, 5), (131, 5),
             (29, 7), (379, 7), (17, 8), (617, 8), (19, 9), (937, 9), (13, 12), (2473, 12)]
    controls = [surface_control(p, d) for p, d in specs]
    return {"schema_version": "jacobi-split-fermat-surface-v1",
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "literature": ["https://arxiv.org/abs/2607.29453", "https://arxiv.org/abs/quant-ph/0207131",
                           "https://arxiv.org/abs/math/0411623", "https://arxiv.org/abs/quant-ph/0405081"],
            "question": "Can norm-normalized exact Jacobi residues provide a charged exact surface-count reduction?",
            "proof_status": "LOCAL_REDUCTION_REVIEW_PENDING_EXTERNAL_QUANTUM_PRIMITIVES_NOT_IMPLEMENTED",
            "prime_conductor_phase_selection": "CLASSICAL_PRIMARY_CONGRUENCE_NO_QUANTUM_PHASE_NEEDED",
            "controls": controls, "new_quantum_algorithm_claimed": False,
            "large_public_ideal_control": large_public_ideal_control(),
            "central_candidate_or_negative_created": False,
            "unresolved": ["Generic three-character quantum CM reconstruction beyond the cited repeated-character theorem",
                           "Valuation-aware compact local division and residue evaluation with proved bit costs",
                           "Quantum PIP/unit/phase implementations and independent theorem review",
                           "Strong variable-conductor classical comparisons and novelty assessment"],
            "all_exact_controls_pass": True}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.write:
        ARTIFACT.write_text(json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n")
    attempts = [a for c in report["controls"] for a in c["classical_ideal_lll_attempts"]]
    print(json.dumps({"exact_surface_controls": len(report["controls"]),
                      "public_ideal_lll_attempts": len(attempts),
                      "balanced_generators_found": sum(a["balanced_generator_found"] for a in attempts),
                      "quantum_subroutines_executed": False, "new_algorithm_claimed": False}, indent=2))


if __name__ == "__main__":
    main()
