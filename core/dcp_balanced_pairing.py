"""Balanced-support DCP partner search by a reversible sorting-network join.

This is a classical meet-in-the-middle baseline with a coherent-compatible,
fixed-address compute/copy/uncompute schedule. Both time and storage remain
exponential. No QRAM, novel speedup, or exported gate circuit is claimed.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, islice, product
from math import comb, isqrt, log2

from dcp_affine_marked_pairing import (
    MarkedPairingProgram, _jsonable, affine_hash, support_family_certificate,
)


def block_masks(start: int, width: int, weight: int):
    for indices in combinations(range(start, start+width), weight):
        yield sum(1 << i for i in indices)


def balanced_certificate(n: int, width: int, weight: int | None = None,
                         list_length: int | None = None) -> dict:
    if (type(n) is not int or n < 1 or type(width) is not int
            or width < 2 or width % 2):
        raise ValueError("require positive n and positive even width")
    half = width//2
    if weight is None:
        for weight in range(1, (half+1)//2+1):
            if comb(half, weight)**2 >= 1 << n:
                break
        else:
            raise ValueError("no balanced support family reaches unit mean degree")
    if type(weight) is not int or not 1 <= weight <= half:
        raise ValueError("invalid per-block weight")
    available = comb(half, weight)
    length = min(available, isqrt((1 << n)-1)+1) if list_length is None else list_length
    if type(length) is not int or not 1 <= length <= available:
        raise ValueError("list length must fit the distinct block supports")
    row = support_family_certificate(n, width, 2*weight, length*length)
    padded = 1 << (2*length-1).bit_length()
    levels = padded.bit_length()-1
    comparators = padded*levels*(levels+1)//4
    key_bits = n+row["hash_bits"]+1  # Includes a key beyond the real domain for padding.
    record_bits = key_bits+2+width
    state_bits = key_bits+3*row["counter_bits"]+3*width
    # Replace streamed-enumeration accounting inherited from the coverage helper.
    del row["one_xor_support_predicate_calls"], row["six_xor_support_predicate_calls"]
    row.update({"half_width": half, "per_block_weight": weight,
                "available_block_supports": available, "full_block_lists_used": length == available,
                "each_list_length": length, "padded_records": padded,
                "one_xor_record_evaluations": 4*length,
                "one_xor_comparators": 2*comparators,
                "one_xor_scan_steps": 2*padded,
                "six_xor_comparators": 12*comparators,
                "record_bits": record_bits, "scan_state_bits": state_bits,
                "persistent_workspace_bits": padded*record_bits+(padded+1)*state_bits+comparators,
                "workspace_excludes_reusable_polynomial_arithmetic_scratch": True,
                "coherent_ram_assumed": False, "gate_export_implemented": False,
                "time_form": "O(L*log(L)^2*poly(n,m)), L<=C(m/2,k); default L=ceil(sqrt(2^n)) when available",
                "space_form": "O(L*poly(n,m)) basis-wire bits; coherent when input is a superposition"})
    return row


def comparator_schedule(size: int, reverse: bool = False):
    """Fixed bitonic-network wire addresses, independent of all input values."""
    if type(size) is not int or size < 2 or size & (size-1):
        raise ValueError("network size must be a power of two >=2")
    levels = size.bit_length()-1
    for level in (range(levels, 0, -1) if reverse else range(1, levels+1)):
        for exponent in (range(level) if reverse else range(level-1, -1, -1)):
            for i in (range(size-1, -1, -1) if reverse else range(size)):
                j = i ^ (1 << exponent)
                if j > i:
                    yield i, j, not bool(i & (1 << level))


def _swap_test(left, right, ascending):
    return left > right if ascending else left < right


def sort_records(records: list[tuple[int, int, int]]) -> list[int]:
    flags = []
    for i, j, ascending in comparator_schedule(len(records)):
        swap = int(_swap_test(records[i], records[j], ascending))
        flags.append(swap)
        if swap:
            records[i], records[j] = records[j], records[i]
    return flags


def unsort_records(records: list[tuple[int, int, int]], flags: list[int]) -> int:
    executed = 0
    for i, j, ascending in comparator_schedule(len(records), reverse=True):
        executed += 1
        swap = flags[-1]
        if swap:
            records[i], records[j] = records[j], records[i]
        flags[-1] ^= int(_swap_test(records[i], records[j], ascending))
        if flags[-1]:
            raise ArithmeticError("sorting history did not uncompute")
        flags.pop()  # Only a restored zero wire is released.
    return executed


def _join_step(state: tuple[int, ...], record: tuple[int, int, int]) -> tuple[int, ...]:
    previous, left_count, right_count, left_xor, right_xor, count, image = state
    key, side, mask = record
    if key != previous:
        left_count = right_count = left_xor = right_xor = 0
    if side == 0:
        count += right_count
        image ^= right_xor ^ (mask if right_count & 1 else 0)
        left_count += 1
        left_xor ^= mask
    elif side == 1:
        count += left_count
        image ^= left_xor ^ (mask if left_count & 1 else 0)
        right_count += 1
        right_xor ^= mask
    return key, left_count, right_count, left_xor, right_xor, count, image


@dataclass(frozen=True)
class BalancedPairingProgram:
    labels: tuple[int, ...]
    n: int
    weight: int
    hash_rows: tuple[int, ...]
    hash_offset: int
    list_length: int | None = None

    def __post_init__(self):
        checked = MarkedPairingProgram(self.labels, self.n, 2*self.weight,
                                       self.hash_rows, self.hash_offset)
        certificate = balanced_certificate(self.n, len(checked.labels), self.weight, self.list_length)
        object.__setattr__(self, "labels", checked.labels)
        object.__setattr__(self, "hash_rows", checked.hash_rows)
        object.__setattr__(self, "list_length", certificate["each_list_length"])

    def marked(self, assignment: int) -> bool:
        return affine_hash(assignment, self.hash_rows, self.hash_offset) == 0

    def _records(self, assignment: int):
        half, bits, modulus = len(self.labels)//2, len(self.hash_rows), 1 << self.n
        for side in (0, 1):
            for mask in islice(block_masks(side*half, half, self.weight), self.list_length):
                value = sum((-a if assignment & (1 << i) else a)
                            for i, a in enumerate(self.labels) if mask & (1 << i)) % modulus
                if side:
                    value = (modulus//2-value) % modulus
                # Offsets cancel between endpoints: H(s_left)=H(s_right).
                key = (value << bits) | affine_hash(mask, self.hash_rows, 0)
                yield key, side, mask

    def evaluate_xor(self, assignment: int, output: int = 0) -> dict:
        size = 1 << len(self.labels)
        if (type(assignment) is not int or type(output) is not int
                or not 0 <= assignment < size or not 0 <= output < 2*size):
            raise ValueError("basis wire out of range")
        resource = balanced_certificate(self.n, len(self.labels), self.weight, self.list_length)
        # Explicit controls may use any hash width, not just the theorem's choice.
        extra_bits = len(self.hash_rows)-resource["hash_bits"]
        resource["persistent_workspace_bits"] += (2*resource["padded_records"]+1)*extra_bits
        records = list(self._records(assignment))
        real_records = len(records)
        padding = (1 << (self.n+len(self.hash_rows)), 2, 0)
        records.extend([padding]*(resource["padded_records"]-real_records))
        flags = sort_records(records)
        comparisons, scan_steps = len(flags), 0
        states = [(0,)*7]
        for record in records:
            states.append(_join_step(states[-1], record))
            scan_steps += 1
        count, mask_xor = states[-1][-2:]
        if self.marked(assignment) and count == 1:
            output ^= size | (assignment ^ mask_xor)
        # Each prefix is a separate clean register, not an irreversible reset.
        for i in range(len(records)-1, -1, -1):
            scan_steps += 1
            states[-1] = tuple(a ^ b for a, b in zip(states[-1], _join_step(states[-2], records[i])))
            if any(states[-1]):
                raise ArithmeticError("join prefix did not uncompute")
            states.pop()
        comparisons += unsort_records(records, flags)
        # Reverse the public, fixed-index record-generation circuit.
        for i, expected in enumerate(self._records(assignment)):
            records[i] = tuple(a ^ b for a, b in zip(records[i], expected))
        for i in range(real_records, len(records)):
            records[i] = tuple(a ^ b for a, b in zip(records[i], padding))
        clean = (not flags and states == [(0,)*7] and not any(any(row) for row in records))
        return {"output": output, "workspace_clean": clean,
                # Diagnostic classical replay values, NOT retained quantum outputs.
                "neighbor_count_before_source_mark": count,
                "support_xor_before_source_mark": mask_xor,
                "record_evaluations": 2*real_records,
                "comparators": comparisons, "scan_steps": scan_steps,
                "persistent_workspace_bits": resource["persistent_workspace_bits"]}

    def propose(self, assignment: int) -> int | None:
        row = self.evaluate_xor(assignment)
        if not row["workspace_clean"]:
            raise ArithmeticError("unclean balanced proposal workspace")
        size = 1 << len(self.labels)
        return row["output"]-size if row["output"] & size else None


def balanced_program_from_seed(labels, n: int, seed: int, weight: int | None = None,
                               list_length: int | None = None):
    row = balanced_certificate(n, len(labels), weight, list_length)
    if type(seed) is not int or not 0 <= seed < 1 << row["public_seed_bits"]:
        raise ValueError("seed must fit the complete uniform affine seed space")
    width, bits = len(labels), row["hash_bits"]
    rows = tuple((seed >> (i*width)) & ((1 << width)-1) for i in range(bits))
    return BalancedPairingProgram(labels, n, row["per_block_weight"], rows, seed >> (width*bits), row["each_list_length"])


def _reference_block_supports(half: int, weight: int, length: int) -> set[int]:
    """Small full-domain reference, independent of the streamed combinations."""
    masks = [s for s in range(1 << half) if s.bit_count() == weight]
    return set(sorted(masks, key=lambda s: tuple(i for i in range(half) if s & (1 << i)))[:length])


def exact_balanced_source_control(n: int, width: int, weight: int,
                                  list_length: int | None = None) -> dict:
    certificate = balanced_certificate(n, width, weight, list_length)
    modulus, size, bits = 1 << n, 1 << width, certificate["hash_bits"]
    total = modulus**width * size * (1 << certificate["public_seed_bits"])
    if total > 5_000_000:
        raise ValueError("exact source control exceeds the explicit diagnostic budget")
    marks = [sum(1 << b for b in range(size) if affine_hash(b, rows, offset) == 0)
             for rows in product(range(size), repeat=bits) for offset in range(1 << bits)]
    half, matches, degrees, squares, marked_degrees, marked_vertices = width//2, 0, 0, 0, 0, 0
    # Independent full-assignment graph, not the sorted join's record generator.
    block = _reference_block_supports(half, weight, certificate["each_list_length"])
    supports = [s for s in range(1, size) if (s & ((1 << half)-1)) in block and (s >> half) in block]
    for labels in product(range(modulus), repeat=width):
        sums = [sum(a for i, a in enumerate(labels) if b & (1 << i)) % modulus for b in range(size)]
        neighbors = [sum(1 << (b ^ s) for s in supports if (sums[b ^ s]-sums[b]) % modulus == modulus//2)
                     for b in range(size)]
        degrees += sum(adj.bit_count() for adj in neighbors)
        squares += sum(adj.bit_count()**2 for adj in neighbors)
        for selected in marks:
            induced = [adj & selected for adj in neighbors]
            marked_vertices += selected.bit_count()
            for b, adj in enumerate(induced):
                if selected & (1 << b):
                    marked_degrees += adj.bit_count()
                if selected & (1 << b) and adj.bit_count() == 1:
                    matches += induced[adj.bit_length()-1] == 1 << b
    denominator = modulus**width*size
    mass = Fraction(matches, total)
    return {"n": n, "width": width, "weight": weight,
            "list_length": certificate["each_list_length"],
            "source_label_seed_assignments": total, "observed_mass": mass,
            "source_mass_lower": certificate["source_mass_lower"],
            "conditional_marked_degree": Fraction(marked_degrees, marked_vertices),
            "checks": {"first_moment": Fraction(degrees, denominator) == certificate["mean_degree"],
                       "second_moment": Fraction(squares, denominator) == certificate["degree_second_moment"],
                       "coverage": mass >= certificate["source_mass_lower"],
                       "post_mark_density": Fraction(marked_degrees, marked_vertices) == certificate["post_mark_expected_degree"]}}


def balanced_program_control(program: BalancedPairingProgram) -> dict:
    width, modulus = len(program.labels), 1 << program.n
    if width > 8:
        raise ValueError("program replay is a finite diagnostic")
    size, half, table, failures = 1 << width, width//2, [], 0
    block = _reference_block_supports(half, program.weight, program.list_length)
    sums = [sum(a for i, a in enumerate(program.labels) if b & (1 << i)) % modulus for b in range(size)]
    for b in range(size):
        expected = [c for c in range(size) if program.marked(b) and program.marked(c)
                    and ((b ^ c) & ((1 << half)-1)) in block
                    and ((b ^ c) >> half) in block
                    and (sums[c]-sums[b]) % modulus == modulus//2]
        row = program.evaluate_xor(b)
        failures += row["output"] != (size | expected[0] if len(expected) == 1 else 0)
        failures += not row["workspace_clean"]
        table.append(row["output"]-size if row["output"] & size else None)
    accepted = sum(c is not None and table[c] == b for b, c in enumerate(table))
    return {"labels": program.labels, "n": program.n, "weight": program.weight,
            "list_length": program.list_length,
            "proposal_table": table, "failures": failures,
            "accepted_source_mass": Fraction(accepted, size),
            "selected_calibration_not_natural_coverage_estimate": True}


def build_balanced_pairing_audit() -> dict:
    controls = [exact_balanced_source_control(*args) for args in ((2, 2, 1), (3, 4, 1), (2, 4, 1, 1))]
    programs = [balanced_program_control(p) for p in (
        BalancedPairingProgram((1, 0, 1, 0), 2, 1, (), 0),
        BalancedPairingProgram((1, 1, 1, 1), 2, 1, (), 0),
        balanced_program_from_seed((1, 2, 3, 4), 3, 3, 1))]
    scaling = []
    for n in (8, 16, 32, 64, 128, 256, 512):
        for regime, width in (("linear-samples", 2*n), ("quadratic-samples", 2*((n*n+1)//2))):
            row = balanced_certificate(n, width)
            row["sample_regime"] = regime
            row["analytical_counts_not_large_instance_execution"] = True
            row["log2_list_length"] = log2(row["each_list_length"])
            row["log2_six_xor_comparators"] = log2(row["six_xor_comparators"])
            row["log2_persistent_workspace_bits"] = log2(row["persistent_workspace_bits"])
            mass = row["source_mass_lower"]
            row["log2_source_mass_lower"] = log2(mass.numerator)-log2(mass.denominator)
            scaling.append(row)
    return _jsonable({"controls": controls, "program_controls": programs, "scaling": scaling,
                      "literature": [
                          {"url": "https://arxiv.org/abs/1207.2307", "role": "Prior reversible sorting networks; comparison history is retained and uncomputed, not free erasure."},
                          {"url": "https://arxiv.org/abs/2206.14408", "role": "Prior DCP time/query/memory tradeoffs; linear samples and exponential time are not a new efficiency result."}],
                      "control_failures": (sum(not all(r["checks"].values()) for r in controls)
                                           + sum(r["failures"] for r in programs)),
                      "status": "derived-balanced-mitm-exponential-time-space-review-pending",
                      "contract": {
                          "support_family": "Cartesian product of first L lexicographic weight-k supports in each equal block; neither the whole radius ball nor necessarily full block lists.",
                          "source_law": "Independent uniform labels and unrestricted independent uniform affine seed.",
                          "coverage": "Same three-wise thinning/moment bound with D=L^2. Default L=ceil(sqrt(2^n)) once available gives source mass >=1/128 for n>=2, with no input/seed conditioning.",
                          "charged_resources": "L=ceil(sqrt(2^n)) list entries per block by default; time and coherent storage remain exponential.",
                          "density_after_isolation": "Conditioned on a source being marked, H is still uniform. Expected neighbor count is D/(N*2^ell)=lambda*theta in (1/8,1/4] for lambda>=1. Increasing raw support multiplicity also increases syndrome constraints; no dense-instance shortcut is supplied.",
                          "linear_sample_noise_bound": "For m=2n,n>=6, minimal k<=ceil(n/4)<=n/3. Under the stated prelabel classical-fault marginal <=1/n, source-averaged signed signal >=1/384. No arbitrary quantum noise, independent-batch promise, or full-secret decoder is supplied.",
                          "reversibility": "Fixed sorting addresses, saved comparison bits, full prefix histories, output XOR, inverse scan/sort/record generation.",
                          "classical_baseline_only_for_partner_subproblem": True,
                          "classical_dcp_solver_constructed": False,
                          "finite_program_executed": True,
                          "coherent_ram_assumed": False, "gate_export_implemented": False,
                          "independently_reviewed": False, "novelty_established": False,
                          "speedup_claim_allowed": False}})
