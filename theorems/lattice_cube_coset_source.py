"""Public lattice cube evaluator and exhaustive coherent-source reference audit.

This implements the source FUNCTION and its bounded Born-law reference, not
a scalable physical state-preparation circuit or a DCP decoder. No shortest
vector, hidden shift, or clean flag is an input to CubeCosetSource.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
import hashlib
from itertools import product
import json
from math import prod
from pathlib import Path

from sympy import Matrix, isprime

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/reductions/lattice_cube_coset_source.json"
DERIVATION = ROOT / "research/LATTICE_CUBE_COSET_SOURCE.md"
CONTRACT = ROOT / "research/hypotheses/lattice_cube_coset_source_contract.json"
PRIMARY = ROOT / "research/literature_cache/cs_0304005_source/quantum_average.tex"


def exact_int(value, name, minimum=None):
    if type(value) is not int or (minimum is not None and value < minimum):
        raise ValueError("exact " + name + " required")
    return value


def encode_position(a, box):
    return sum(x * (2 * box) ** i for i, x in enumerate(a))


def decode_difference(shift, n, box):
    """Recover signed box differences, checking the base-2M carry margin."""
    exact_int(n, "positive dimension", 1)
    exact_int(box, "box size", 2)
    N = (2 * box) ** n
    exact_int(shift, "canonical shift", 0)
    if shift >= N:
        raise ValueError("canonical scalar shift required")
    correction = sum(box * (2 * box) ** i for i in range(n))
    x = (shift + correction) % N
    out = []
    for _ in range(n):
        digit = x % (2 * box)
        if not 1 <= digit <= 2 * box - 1:
            raise ValueError("shift outside the strictly signed box-difference contract")
        out.append(digit - box)
        x //= 2 * box
    result = tuple(out)
    if encode_position(result, box) % N != shift:
        raise ArithmeticError("signed base decoding changed the scalar difference")
    return result


@dataclass(frozen=True)
class CubeCosetSource:
    """Public integer parameters only; basis vectors are ROWS."""
    basis: tuple
    prime: int
    residue_guess: int
    coordinate: int
    box: int
    width: int
    offsets: tuple

    def __post_init__(self):
        B = tuple(tuple(row) for row in self.basis)
        offsets = tuple(self.offsets)
        n = len(B)
        if not n or any(len(row) != n for row in B):
            raise ValueError("square nonempty integer lattice basis required")
        for row in B:
            for x in row:
                exact_int(x, "basis entry")
        if Matrix(B).det() == 0:
            raise ValueError("full rank lattice basis required")
        exact_int(self.prime, "positive prime", 2)
        if not isprime(self.prime):
            raise ValueError("prime residue modulus required")
        exact_int(self.residue_guess, "nonzero residue guess", 1)
        exact_int(self.coordinate, "basis coordinate", 0)
        if self.residue_guess >= self.prime or self.coordinate >= n:
            raise ValueError("residue/coordinate guess out of range")
        for x, name in ((self.box, "box"), (self.width, "cube width")):
            exact_int(x, "positive dyadic " + name, 2)
            if x & (x - 1):
                raise ValueError("power-of-two " + name + " required")
        if len(offsets) != n:
            raise ValueError("full public cube offset required")
        if any(type(x) is not int or not 1 <= x <= self.width for x in offsets):
            raise ValueError("integer offsets uniform on1..width required")
        object.__setattr__(self, "basis", B)
        object.__setattr__(self, "offsets", offsets)

    @property
    def dimension(self):
        return len(self.basis)

    @property
    def input_population(self):
        return 2 * self.box ** self.dimension

    @property
    def phase_modulus(self):
        return (2 * self.box) ** self.dimension

    def lattice_point(self, t, a):
        exact_int(t, "colour bit", 0)
        a = tuple(a)
        if t > 1 or len(a) != self.dimension or any(type(x) is not int or not 0 <= x < self.box for x in a):
            raise ValueError("canonical colour and box position required")
        coefficients = list(a)
        coefficients[self.coordinate] = self.prime * a[self.coordinate] + t * self.residue_guess
        return tuple(sum(c * row[i] for c, row in zip(coefficients, self.basis)) for i in range(self.dimension))

    def cell(self, t, a):
        return tuple((x - j) // self.width for x, j in zip(self.lattice_point(t, a), self.offsets))

    def public_access(self):
        return {"basis_rows": self.basis, "prime": self.prime, "residue_guess": self.residue_guess,
                "coordinate": self.coordinate, "box": self.box, "cube_width": self.width,
                "offsets": self.offsets, "input_population": self.input_population,
                "phase_modulus": self.phase_modulus,
                "explicit_cell_evaluator_available": True,
                "uniform_hidden_shift_prior_assumed": False,
                "uniform_secret_twirl_bounds_transferred_to_source": False,
                "shortest_vector_or_shift_given_to_constructor": False,
                "normalized_conditional_state_inverse_available": False,
                "scalable_coherent_evaluator_circuit_compiled": False}

    def clean_arithmetic_plan(self):
        """Exact signed-width certificate for public compute-copy-uncompute.

        Copying the high two's-complement bits implements floor, even for
        negative points. All point/carry/remainder workspace must then be
        uncomputed. This is a compilation contract, NOT a compiled circuit.
        """
        maxima = [self.box - 1] * self.dimension
        maxima[self.coordinate] = self.prime * (self.box - 1) + self.residue_guess
        shift = self.width.bit_length() - 1
        coordinates = []
        for i in range(self.dimension):
            bound = sum(abs(row[i]) * c for row, c in zip(self.basis, maxima)) + self.width
            bits = max(bound.bit_length() + 1, shift + 1)
            coordinates.append({"absolute_point_minus_offset_bound": bound,
                                "signed_point_workspace_bits": bits,
                                "low_remainder_bits_to_uncompute": shift,
                                "signed_cell_output_bits": bits - shift,
                                "strict_signed_range_certified": bound < 2 ** (bits - 1)})
        return {"initial_uniform_source_qubits": 1 + self.dimension * (self.box.bit_length() - 1),
                "position_embedding_padding_qubits": self.dimension,
                "position_phase_register_qubits": self.dimension * self.box.bit_length(),
                "public_coefficient_maxima": tuple(maxima), "coordinate_width_certificates": tuple(coordinates),
                "classical_constant_multiply_accumulate_terms": self.dimension ** 2,
                "signed_floor_implemented_by_high_bit_copy": True,
                "physical_point_carry_remainder_workspace_must_return_zero": True,
                "clean_reversible_arithmetic_gates_compiled": False}

    def fibres_for_audit(self, cap=200_000):
        """Exhaustive private reference, NEVER a polynomial-time preimage oracle."""
        exact_int(cap, "complete domain cap", 1)
        if self.input_population > cap:
            raise ValueError("UNKNOWN_REFERENCE_CAP; no source-failure conclusion")
        fibres = {}
        for t in range(2):
            for a in product(range(self.box), repeat=self.dimension):
                fibres.setdefault(self.cell(t, a), []).append((t, a))
        return fibres

    def audit(self, cap=200_000):
        fibres = self.fibres_for_audit(cap)
        sizes = Counter(len(f) for f in fibres.values())
        valid = all(len(f) <= 2 and len({t for t, _ in f}) == len(f) for f in fibres.values())
        shifts = Counter()
        bad_colours = [0, 0]
        good = 0
        for fibre in fibres.values():
            if len(fibre) == 2 and {t for t, _ in fibre} == {0, 1}:
                by_colour = dict(fibre)
                delta = tuple(b - a for a, b in zip(by_colour[0], by_colour[1]))
                shifts[delta] += 1
                good += 1
            elif len(fibre) == 1:
                bad_colours[fibre[0][0]] += 1
        valid = valid and len(shifts) <= 1
        total = self.input_population
        shifted = tuple({"difference": delta, "cells": count,
                         "scalar_shift": encode_position(delta, self.box) % self.phase_modulus}
                        for delta, count in sorted(shifts.items()))
        return {"public_source": self.public_access(), "clean_arithmetic_plan": self.clean_arithmetic_plan(),
                "complete_original_domain_censused": total,
                "measured_cell_count": len(fibres),
                "fibre_size_histogram": tuple({"size": k, "cells": v,
                                               "Born_mass": str(Fraction(k * v, total))}
                                              for k, v in sorted(sizes.items())),
                "PRIVATE_AUDIT_ONLY_common_differences": shifted,
                "PRIVATE_AUDIT_ONLY_singleton_colour_counts": tuple(bad_colours),
                "good_two_point_cell_count": good,
                "good_two_point_Born_mass": str(Fraction(2 * good, total)),
                "valid_two_point_source_on_full_domain": valid,
                "bad_register_rate": str(Fraction(sum(bad_colours), total)) if valid else None,
                "position_Fourier_label_uniformity_proved": valid,
                "balanced_bad_basis_mixture_proved": valid and bad_colours[0] == bad_colours[1],
                "full_growing_family_reduction_promise_proved": False,
                "reference_enumeration_is_scalable_quantum_source_circuit": False,
                "multipoint_fibres_are_valid_bad_basis_registers": False}


def offset_average_pair_mass(box, width, delta, displacement):
    """Exact partner event averaged over independent fresh offsets and box input.

    Equals full source good mass ONLY when the at-most-two/common-partner
    geometry promise holds. It is otherwise just this proposed pair event.
    """
    if len(delta) != len(displacement):
        raise ValueError("matching coordinate dimensions required")
    exact_int(box, "box", 2)
    exact_int(width, "width", 2)
    if any(type(x) is not int for x in tuple(delta) + tuple(displacement)):
        raise ValueError("exact integer partner differences required")
    return prod(Fraction(max(0, box - abs(x)), box) for x in delta) * prod(
        Fraction(max(0, width - abs(x)), width) for x in displacement)


def classical_LLL_baseline(basis):
    """Public-data reduction and shortest reduced-row control, without truth."""
    B = Matrix(basis)
    reduced, transform = B.lll_transform()
    candidates = [tuple(int(x) for x in reduced.row(i)) for i in range(reduced.rows)]
    vector = min(candidates, key=lambda row: sum(x * x for x in row))
    return {"reduced_basis_rows": tuple(candidates),
            "unimodular_row_transform": tuple(tuple(int(x) for x in transform.row(i)) for i in range(transform.rows)),
            "shortest_reduced_row": vector, "squared_norm": sum(x * x for x in vector),
            "shortest_vector_truth_given_to_baseline": False,
            "norm1_in_integer_lattice_proves_global_shortest": sum(x * x for x in vector) == 1,
            "LLL_solves_general_unique_SVP_claimed": False}


def build_report():
    B = ((10000, 1000), (9999, 1000))
    controls = tuple(CubeCosetSource(B, 389, 1, 0, 256, 128, offsets).audit()
                     for offsets in ((1, 1), (64, 127), (128, 64)))
    invalid = CubeCosetSource(B, 3, 1, 0, 16, 64, (1, 1)).audit()
    averaged = offset_average_pair_mass(256, 128, (0, -1), (1, 0))
    return {"status": "PUBLIC_LATTICE_CUBE_COSET_SOURCE_REFERENCE_REVIEW_PENDING",
            "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "contract_sha256": hashlib.sha256(CONTRACT.read_bytes()).hexdigest(),
            "cached_primary_sha256": hashlib.sha256(PRIMARY.read_bytes()).hexdigest(),
            "complete_source_controls": controls,
            "invalid_geometry_countercontrol": invalid,
            "public_classical_LLL_control": classical_LLL_baseline(B),
            "fixture_geometry_certificate": {"integer_lattice_vertical_spacing": 1000,
                "shortest_squared_norm": 1, "nonparallel_squared_norm_lower": 1_000_000,
                "cube_squared_diameter_upper": 2 * 128 ** 2,
                "other_congruent_multiple_squared_norm_lower": 388 ** 2,
                "LLL_preprocessed_basis_promise_inferred": False},
            "fresh_offset_average": {"private_calibration_difference": (0, -1),
                "private_calibration_displacement": (1, 0),
                "exact_good_Born_mass": str(averaged), "exact_bad_Born_mass": str(1 - averaged),
                "failure_parameter_f1_budget": "1/18",
                "bad_mass_within_declared_f1_budget": 1 - averaged <= Fraction(1, 18),
                "average_is_per_offset_guarantee": False},
            "known_parent_inverse_prices": {
                "good_specified_cell_inverse_zero_probability": "1/65536",
                "good_specified_cell_and_Fourier_label_inverse_zero_probability": "1/17179869184",
                "conditional_normalized_coset_inverse_is_free": False,
                "prices_apply_to_sampling_any_good_cell": False},
            "coherent_workspace_obligation": "COMPUTE_CELL_COPY_UNCOMPUTE_POINT_CARRY_AND_REMAINDER_GARBAGE",
            "source_public_geometry_can_enable_more_than_copy_only_DCP": True,
            "scalable_quantum_source_circuit_compiled": False,
            "efficient_noisy_DCP_decoder_supplied": False,
            "accepted_speedup_candidate": False, "new_active_negative_result_created": False,
            "novelty_claim": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"status": report["status"], "valid_source_controls":
                      [c["valid_two_point_source_on_full_domain"] for c in report["complete_source_controls"]],
                      "invalid_geometry_rejected": not report["invalid_geometry_countercontrol"]["valid_two_point_source_on_full_domain"],
                      "classical_baseline_solved_control": report["public_classical_LLL_control"]["norm1_in_integer_lattice_proves_global_shortest"],
                      "accepted_speedup_candidate": False}, indent=2))


if __name__ == "__main__":
    main()
