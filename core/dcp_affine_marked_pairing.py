"""Executable bounded-width DCP pairing with charged exponential enumeration.

Random affine vertex marking has a polynomial description. Its coverage bound
uses three-wise independence, not an ideal random oracle or a free neighbor list.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, product
from math import comb, log2


def support_count(width: int, radius: int) -> int:
    if any(type(x) is not int for x in (width, radius)) or not 1 <= radius <= width:
        raise ValueError("require integer 1<=radius<=width")
    return sum(comb(width, weight) for weight in range(1, radius+1))


def support_masks(width: int, radius: int):
    support_count(width, radius)
    for weight in range(1, radius+1):
        for indices in combinations(range(width), weight):
            yield sum(1 << i for i in indices)


def affine_hash(value: int, rows: tuple[int, ...], offset: int) -> int:
    result = offset
    for i, row in enumerate(rows):
        result ^= ((row & value).bit_count() & 1) << i
    return result


def coverage_certificate(n: int, width: int, radius: int | None = None) -> dict:
    if type(n) is not int or n < 1 or type(width) is not int or width < 1:
        raise ValueError("positive integer modulus bits and width required")
    modulus = 1 << n
    if radius is None:
        count = 0
        for radius in range(1, width+1):
            count += comb(width, radius)
            if count >= modulus:
                break
    count = support_count(width, radius)
    return support_family_certificate(n, width, radius, count)


def support_family_certificate(n: int, width: int, radius: int, count: int) -> dict:
    """Coverage for a fixed family of DISTINCT nonempty flip supports.

    The caller must supply the family's exact size and maximum Hamming width.
    The signed-sum moment proof does not require all radius-r supports.
    """
    if (any(type(x) is not int for x in (n, width, radius, count))
            or n < 1 or not 1 <= radius <= width or not 1 <= count < 1 << width):
        raise ValueError("invalid nonempty distinct support family dimensions")
    modulus = 1 << n
    mean = Fraction(count, modulus)
    bits = 0
    while (1 << bits)*modulus < 4*count:
        bits += 1
    theta = Fraction(1, 1 << bits)
    second = mean*mean + mean*(1-Fraction(1, modulus))
    lower = theta**2*mean - theta**3*(2*second-2*mean)
    if lower < 0 or lower < theta**2*mean/2:
        raise ArithmeticError("marking choice violates the coverage bound")
    return {"n": n, "width": width, "radius": radius, "supports": count,
            "mean_degree": mean, "degree_second_moment": second,
            "hash_bits": bits, "mark_probability": theta, "source_mass_lower": lower,
            "post_mark_expected_degree": mean*theta,
            "syndrome_target_domain_size": modulus*(1 << bits),
            "syndrome_domain_over_supports": Fraction(modulus*(1 << bits), count),
            "joint_fault_signal_lower": max(Fraction(0), 1-Fraction(radius, n))*lower,
            "independent_fault_signal_lower": Fraction(n-1, n)**radius*lower,
            "public_seed_bits": bits*(width+1), "one_xor_support_predicate_calls": 2*count,
            "six_xor_support_predicate_calls": 12*count,
            "counter_bits": count.bit_length(),
            "unit_mean_degree_reached": count >= modulus,
            "full_assignment_table_required": False,
            "polynomial_time_claimed": False}


@dataclass(frozen=True)
class MarkedPairingProgram:
    labels: tuple[int, ...]
    n: int
    radius: int
    hash_rows: tuple[int, ...]
    hash_offset: int

    def __post_init__(self):
        object.__setattr__(self, "labels", tuple(self.labels))
        object.__setattr__(self, "hash_rows", tuple(self.hash_rows))
        if type(self.n) is not int or self.n < 1:
            raise ValueError("positive integer modulus bits required")
        support_count(len(self.labels), self.radius)
        if any(type(a) is not int or not 0 <= a < 1 << self.n for a in self.labels):
            raise ValueError("labels must lie in Z_(2^n)")
        if (any(type(row) is not int or not 0 <= row < 1 << len(self.labels) for row in self.hash_rows)
                or type(self.hash_offset) is not int or not 0 <= self.hash_offset < 1 << len(self.hash_rows)):
            raise ValueError("invalid affine hash seed")

    def marked(self, assignment: int) -> bool:
        return affine_hash(assignment, self.hash_rows, self.hash_offset) == 0

    def neighbor_predicate(self, assignment: int, mask: int) -> bool:
        if not self.marked(assignment) or not self.marked(assignment ^ mask):
            return False
        difference = 0
        support = mask
        while support:
            bit = support & -support
            i = bit.bit_length()-1
            difference += (-1 if assignment & bit else 1)*self.labels[i]
            support ^= bit
        return difference % (1 << self.n) == 1 << (self.n-1)

    def evaluate_xor(self, assignment: int, output: int = 0,
                     work_count: int = 0, work_image: int = 0) -> dict:
        """Two streamed passes implement a clean XOR oracle on basis wires.

        Keep the entire neighbor count, not an irreversible saturated flag.
        Hit-count increments and image XORs commute, so a second forward
        enumeration with decrements cleans both accumulators without history.
        """
        size = 1 << len(self.labels)
        count = support_count(len(self.labels), self.radius)
        count_modulus = 1 << count.bit_length()
        if (any(type(x) is not int for x in (assignment, output, work_count, work_image))
                or not 0 <= assignment < size or not 0 <= output < 2*size
                or not 0 <= work_count < count_modulus or not 0 <= work_image < size):
            raise ValueError("basis wire out of range")
        predicate_calls = 0
        for mask in support_masks(len(self.labels), self.radius):
            predicate_calls += 1
            if self.neighbor_predicate(assignment, mask):
                work_count = (work_count+1) % count_modulus
                work_image ^= assignment ^ mask
        if self.marked(assignment) and work_count == 1:
            output ^= size | work_image
        for mask in support_masks(len(self.labels), self.radius):
            predicate_calls += 1
            if self.neighbor_predicate(assignment, mask):
                work_count = (work_count-1) % count_modulus
                work_image ^= assignment ^ mask
        return {"output": output, "work_count": work_count, "work_image": work_image,
                "support_predicate_calls": predicate_calls,
                "counter_bits": count.bit_length(), "image_bits": len(self.labels)}

    def propose(self, assignment: int) -> int | None:
        result = self.evaluate_xor(assignment)
        size = 1 << len(self.labels)
        if result["work_count"] or result["work_image"]:
            raise ArithmeticError("unclean proposal workspace")
        return result["output"]-size if result["output"] & size else None


def program_from_seed(labels: tuple[int, ...], n: int, seed: int,
                      radius: int | None = None) -> MarkedPairingProgram:
    """Uniform seed bits biject to ALL matrices/offsets, with no rank rejection."""
    certificate = coverage_certificate(n, len(labels), radius)
    if type(seed) is not int or not 0 <= seed < 1 << certificate["public_seed_bits"]:
        raise ValueError("seed must fit the complete uniform affine seed space")
    width, bits = len(labels), certificate["hash_bits"]
    rows = tuple((seed >> (i*width)) & ((1 << width)-1) for i in range(bits))
    return MarkedPairingProgram(labels, n, certificate["radius"], rows, seed >> (bits*width))


def exact_source_control(n: int, width: int, radius: int) -> dict:
    """Exhaust all labels/hash seeds/assignments; diagnostic only."""
    certificate = coverage_certificate(n, width, radius)
    bits, modulus, size = certificate["hash_bits"], 1 << n, 1 << width
    evaluations = modulus**width * (1 << (bits*(width+1))) * size
    if evaluations > 3_000_000:
        raise ValueError("exact control exceeds the explicit diagnostic budget")
    marks = []
    for rows in product(range(size), repeat=bits):
        for offset in range(1 << bits):
            marks.append(sum(1 << b for b in range(size) if affine_hash(b, rows, offset) == 0))
    degree_sum, degree_square_sum, matched, assignments = 0, 0, 0, 0
    for labels in product(range(modulus), repeat=width):
        residues = [sum(a for i, a in enumerate(labels) if b & (1 << i)) % modulus for b in range(size)]
        neighbors = [sum(1 << (b ^ mask) for mask in support_masks(width, radius)
                         if (residues[b ^ mask]-residues[b]) % modulus == modulus//2) for b in range(size)]
        degree_sum += sum(mask.bit_count() for mask in neighbors)
        degree_square_sum += sum(mask.bit_count()**2 for mask in neighbors)
        assignments += size
        for selected in marks:
            selected_neighbors = [mask & selected for mask in neighbors]
            for b, adjacent in enumerate(selected_neighbors):
                if selected & (1 << b) and adjacent.bit_count() == 1:
                    c = adjacent.bit_length()-1
                    matched += selected_neighbors[c] == 1 << b
    observed = Fraction(matched, assignments*len(marks))
    mean, second = Fraction(degree_sum, assignments), Fraction(degree_square_sum, assignments)
    return {"n": n, "width": width, "radius": radius, "hash_seed_count": len(marks),
            "source_assignments": assignments, "observed_mass": observed,
            "mass_lower": certificate["source_mass_lower"],
            "mean_degree": mean, "degree_second_moment": second,
            "checks": {"first_moment": mean == certificate["mean_degree"],
                       "second_moment": second == certificate["degree_second_moment"],
                       "coverage_bound": observed >= certificate["source_mass_lower"]}}


def _jsonable(value):
    if isinstance(value, Fraction):
        return {"numerator": value.numerator, "denominator": value.denominator}
    if isinstance(value, dict):
        return {key: _jsonable(child) for key, child in value.items()}
    if isinstance(value, (tuple, list)):
        return [_jsonable(child) for child in value]
    return value


def finite_program_control(program: MarkedPairingProgram) -> dict:
    width = len(program.labels)
    if width > 8:
        raise ValueError("full-source program replay is only a finite diagnostic")
    size, modulus = 1 << width, 1 << program.n
    table, failures, evaluations = [], 0, 0
    residues = [sum(a for i, a in enumerate(program.labels) if b & (1 << i)) % modulus for b in range(size)]
    for b in range(size):
        output = program.evaluate_xor(b)
        expected = [c for c in range(size) if program.marked(b) and program.marked(c)
                    and 1 <= (b ^ c).bit_count() <= program.radius
                    and (residues[c]-residues[b]) % modulus == modulus//2]
        value = (size | expected[0]) if len(expected) == 1 else 0
        failures += output["output"] != value or output["work_count"] != 0 or output["work_image"] != 0
        failures += output["support_predicate_calls"] != 2*support_count(width, program.radius)
        evaluations += output["support_predicate_calls"]
        table.append(output["output"]-size if output["output"] & size else None)
    accepted = sum(c is not None and table[c] == b for b, c in enumerate(table))
    return {"labels": program.labels, "n": program.n, "radius": program.radius,
            "hash_rows": program.hash_rows, "hash_offset": program.hash_offset,
            "proposal_table": table, "accepted_source_mass": Fraction(accepted, size),
            "support_predicate_evaluations": evaluations, "failures": failures,
            "selected_calibration_not_natural_coverage_estimate": True}


def build_marked_pairing_audit() -> dict:
    controls = [exact_source_control(n, m, r) for n, m, r in ((2, 2, 1), (2, 2, 2), (3, 3, 1))]
    program_controls = [finite_program_control(program) for program in (
        program_from_seed((1, 3, 0), 2, 0, 2),
        program_from_seed((4, 1, 2), 3, 2, 1),
        program_from_seed((1, 2, 5), 3, 17, 2))]
    scaling = []
    for n in (8, 16, 32, 64, 128, 256, 512):
        row = coverage_certificate(n, n*n)
        row["log2_source_mass_lower"] = log2(row["source_mass_lower"].numerator)-log2(row["source_mass_lower"].denominator)
        row["log2_six_xor_predicate_calls"] = log2(row["six_xor_support_predicate_calls"])
        row["generic_quantum_search_log2_domain_sqrt"] = log2(row["supports"])/2
        row["quantum_search_implemented"] = False
        scaling.append(row)
    return _jsonable({"controls": controls, "program_controls": program_controls, "scaling": scaling,
                      "control_failures": (sum(not all(row["checks"].values()) for row in controls)
                                           + sum(row["failures"] for row in program_controls)),
                      "status": "derived-polynomial-coverage-exponential-finder-review-pending",
                      "contract": {
                          "input_law": "Independent uniform labels and shared uniform affine seed, including singular matrices and empty marked sets; no conditioning on success.",
                          "mass_lower": "theta^2*lambda*(1-2*theta*(lambda-1/N)), lambda=sum_{1<=w<=r} C(m,w)/N, theta=2^-ceil(log2(max(1,4lambda)))",
                          "witness": "Marked vertices with a unique marked half-period neighbor; reciprocal filtering selects isolated edges.",
                          "hash_independence": "Three-wise independent affine maps over F_2; NOT four-wise independent and NOT conditioned full rank.",
                          "resource": "Stream every support twice per XOR evaluator. Six calls cost 12*sum C(m,w) predicate evaluations; polynomial workspace does not remove exponential time.",
                          "unresolved_task": "Replace enumeration by a uniform reversible unique-neighbor algorithm on signed modular subset sums with a binary syndrome and radius constraint.",
                          "finite_program_executed": True, "polynomial_time_finder_constructed": False,
                          "full_decoder_implemented": False, "novelty_established": False,
                          "independently_reviewed": False, "speedup_claim_allowed": False}})
