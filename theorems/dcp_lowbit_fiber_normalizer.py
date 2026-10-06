"""Reversible first-residue-bit normalization, not a growing-q decoder.

LOCAL DERIVATION / REVIEW PENDING. Reuses the existing common-isotropic
constructor. Higher-bit carry graphs do not automatically retain its model.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import random
from dataclasses import dataclass, replace
from fractions import Fraction
from pathlib import Path

from dcp_bell_inference_kernel import exact
from dcp_carry_packets import binary_rank, compile_packet, greedy_common_isotropic

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/dcp_lowbit_fiber_normalizer.json"


def _apply_rows(rows, value):
    return sum(((row & value).bit_count() & 1) << i for i, row in enumerate(rows))


def _columns_value(columns, value):
    result = 0
    for i, column in enumerate(columns):
        if value >> i & 1:
            result ^= column
    return result


def _inverse_rows(rows):
    width = len(rows)
    if not width or any(type(r) is not int or not 0 <= r < 1 << width for r in rows):
        raise ValueError("nonempty square binary matrix required")
    augmented = [row | (1 << (width + i)) for i, row in enumerate(rows)]
    for j in range(width):
        pivot = next((i for i in range(j, width) if augmented[i] >> j & 1), None)
        if pivot is None:
            raise ValueError("binary matrix is singular")
        augmented[j], augmented[pivot] = augmented[pivot], augmented[j]
        for i in range(width):
            if i != j and augmented[i] >> j & 1:
                augmented[i] ^= augmented[j]
    assert [row & ((1 << width) - 1) for row in augmented] == [1 << i for i in range(width)]
    return tuple(row >> width for row in augmented)


def _independent_extension(rows, width):
    basis, pivots = [], {}
    for original in [*rows, *(1 << i for i in range(width))]:
        reduced = original
        for p in sorted(pivots, reverse=True):
            if reduced >> p & 1:
                reduced ^= pivots[p]
        if reduced:
            pivots[reduced.bit_length() - 1] = reduced
            basis.append(original)
    if len(basis) != width:
        raise ValueError("binary basis extension failed")
    return tuple(basis)


@dataclass(frozen=True)
class LowBitFiberNormalizer:
    packet: object
    isotropic_directions: tuple[int, ...]
    basis_columns: tuple[int, ...]
    basis_inverse_rows: tuple[int, ...]

    @property
    def isotropic_width(self):
        return len(self.isotropic_directions)

    def background_plan(self, background):
        d, k, n = self.isotropic_width, self.packet.retained_qubits, self.packet.dimension
        if type(background) is not int or not 0 <= background < 1 << (k - d):
            raise ValueError("background outside complementary chart")
        y = _columns_value(self.basis_columns[d:], background)
        origin = tuple(t & 1 for t in self.packet.residual(y))
        rows = [0] * n
        for j, direction in enumerate(self.isotropic_directions):
            difference = tuple((a ^ b) & 1 for a, b in zip(self.packet.residual(y ^ direction), origin))
            for l, coefficient in enumerate(difference):
                rows[l] |= coefficient << j
        full_rank = binary_rank(rows, d) == n
        if full_rank:
            completed = _independent_extension(rows, d)
            offset = sum(x << l for l, x in enumerate(origin))
        else:
            completed, offset = tuple(1 << i for i in range(d)), 0
        return {"rows": completed, "inverse_rows": _inverse_rows(completed), "offset": offset,
                "full_residue_bit_rank": full_rank, "residue_bit_rows": tuple(rows)}

    def normalize(self, logical):
        k, d = self.packet.retained_qubits, self.isotropic_width
        if type(logical) is not int or not 0 <= logical < 1 << k:
            raise ValueError("logical assignment out of range")
        coordinates = _apply_rows(self.basis_inverse_rows, logical)
        u, y = coordinates & ((1 << d) - 1), coordinates >> d
        plan = self.background_plan(y)
        return (_apply_rows(plan["rows"], u) ^ plan["offset"]) | (y << d)

    def denormalize(self, normalized):
        k, d = self.packet.retained_qubits, self.isotropic_width
        if type(normalized) is not int or not 0 <= normalized < 1 << k:
            raise ValueError("normalized assignment out of range")
        u, y = normalized & ((1 << d) - 1), normalized >> d
        plan = self.background_plan(y)
        original_u = _apply_rows(plan["inverse_rows"], u ^ plan["offset"])
        return _columns_value(self.basis_columns, original_u | (y << d))


def compile_normalizer(packet):
    if packet.modulus < 8 or packet.syndrome or len(packet.pivots) != packet.dimension:
        raise ValueError("full-rank zero-origin native packet with q>=8 required")
    base = compile_packet([[a & 1 for a in row] for row in packet.labels], 4)
    U = greedy_common_isotropic(base)
    k, d = packet.retained_qubits, len(U)
    if d < packet.dimension:
        raise ValueError("isotropic chart too small to normalize all n residue bits")
    columns = _independent_extension(U, k)
    rows = tuple(sum(((column >> i) & 1) << j for j, column in enumerate(columns)) for i in range(k))
    return LowBitFiberNormalizer(packet, U, columns, _inverse_rows(rows))


def lowbit_source_certificate(n, k):
    if type(n) is not int or n < 1 or type(k) is not int or k < n * (n + 1):
        raise ValueError("positive dimension and k>=n(n+1) required for uniform isotropic-size guarantee")
    d = math.ceil(Fraction(k, n + 1))
    full_rank = math.prod(1 - Fraction(1, 1 << (d - i)) for i in range(n))
    return {"status": "FIRST_RESIDUE_LAYER_ONLY_NOT_ITERATED_DECODER",
            "dimension": n, "logical_width": k, "guaranteed_isotropic_width": d,
            "native_original_states": n + k,
            "source_mean_good_background_fraction_lower_bound": exact(full_rank),
            "source_mean_bad_background_fraction_upper_bound": exact(Fraction((1 << n) - 1, 1 << d)),
            "middle_label_rank_law": "IID_uniform_n_by_d_binary_matrix_for_each_fixed_background",
            "isotropic_directions_selected_from_binary_labels_only": True,
            "higher_unused_label_bits_independent_before_good_background_conditioning": True,
            "independence_between_background_rank_events_assumed": False,
            "both_directions_uniform_polynomial_classical_evaluators": True,
            "logical_assignments_or_fibers_enumerated_by_compiler": False,
            "reversible_quantum_backend_and_precision_export_implemented": False,
            "postselected_source_automatically_native_for_next_layer": False,
            "higher_residue_layer_closed_under_same_quadratic_model": False,
            "unknown_secret_recovered": False, "candidate_record_accepted": False,
            "independent_theorem_review": False, "speedup_claim_allowed": False}


def _complete_middle_source_controls():
    records = []
    for B in ([[1, 1, 1, 1, 1, 1]], [[1, 0, 1, 1, 0, 1], [0, 1, 0, 1, 1, 1]]):
        base = compile_normalizer(compile_packet(B, 8))
        n, m, k, d = len(B), len(B[0]), base.packet.retained_qubits, base.isotropic_width
        totals, rank_histograms, checks = 0, [dict() for _ in range(1 << (k - d))], 0
        for middle in itertools.product(range(2), repeat=n * m):
            labels = tuple(tuple(B[l][i] + 2 * middle[l * m + i] for i in range(m)) for l in range(n))
            normalizer = replace(base, packet=replace(base.packet, labels=labels))
            for y, histogram in enumerate(rank_histograms):
                plan = normalizer.background_plan(y)
                key = plan["residue_bit_rows"]
                histogram[key] = histogram.get(key, 0) + 1
                totals += plan["full_residue_bit_rank"]
            outputs = [normalizer.normalize(z) for z in range(1 << k)]
            assert sorted(outputs) == list(range(1 << k))
            for z, w in enumerate(outputs):
                assert normalizer.denormalize(w) == z
                if normalizer.background_plan(w >> d)["full_residue_bit_rank"]:
                    assert (w & ((1 << n) - 1)) == sum((t & 1) << l for l, t in enumerate(normalizer.packet.residual(z)))
                checks += 1
        sources = 1 << (n * m)
        for histogram in rank_histograms:
            assert len(histogram) == 1 << (n * d)
            assert set(histogram.values()) == {sources >> (n * d)}
        rank_probability = math.prod(1 - Fraction(1, 1 << (d - i)) for i in range(n))
        assert Fraction(totals, sources * len(rank_histograms)) == rank_probability
        records.append({"low_labels": B, "all_middle_label_tables": sources,
                        "logical_width": k, "isotropic_width": d,
                        "isotropic_directions_hex": [hex(x) for x in base.isotropic_directions],
                        "basis_columns_hex": [hex(x) for x in base.basis_columns],
                        "basis_inverse_rows_hex": [hex(x) for x in base.basis_inverse_rows],
                        "all_backgrounds": len(rank_histograms),
                        "distinct_linear_matrices_per_background": 1 << (n * d),
                        "each_linear_matrix_source_multiplicity": sources >> (n * d),
                        "exact_source_mean_good_background_fraction": exact(rank_probability),
                        "whole_permutation_inverse_and_residue_checks": checks})
    return records


def _anf(values):
    coefficients = list(values)
    width = len(values).bit_length() - 1
    for j in range(width):
        for mask in range(1 << width):
            if mask >> j & 1:
                coefficients[mask] ^= coefficients[mask ^ (1 << j)]
    return tuple(mask for mask, value in enumerate(coefficients) if value)


def _higher_carry_countercontrol():
    rng = random.Random(20261004)
    for trial in range(100):
        labels = [[1 + 2 * rng.randrange(8) for _ in range(6)]]
        normalizer = compile_normalizer(compile_packet(labels, 16))
        k, d = normalizer.packet.retained_qubits, normalizer.isotropic_width
        if not all(normalizer.background_plan(y)["full_residue_bit_rank"] for y in range(1 << (k - d))):
            continue
        for target in range(2):
            quotients = []
            for r in range(1 << (k - 1)):
                z = normalizer.denormalize(target | (r << 1))
                value = normalizer.packet.residual(z)[0]
                assert value % 2 == target
                quotients.append((value - target) // 2 % 4)
            terms = _anf([q & 1 for q in quotients])
            degree = max((mask.bit_count() for mask in terms), default=0)
            if degree > 2:
                return {"labels": labels, "modulus": 16, "logical_width": k,
                        "isotropic_width": d, "bounded_source_trial_index": trial,
                        "isotropic_directions_hex": [hex(x) for x in normalizer.isotropic_directions],
                        "basis_columns_hex": [hex(x) for x in normalizer.basis_columns],
                        "basis_inverse_rows_hex": [hex(x) for x in normalizer.basis_inverse_rows],
                        "bounded_normalized_to_logical_permutation": [normalizer.denormalize(w) for w in range(1 << k)],
                        "all_backgrounds_full_rank": True, "fixed_first_residue_bit": target,
                        "higher_quotient_values": quotients,
                        "higher_quotient_low_bit_ANF_masks_hex": [hex(mask) for mask in terms],
                        "higher_quotient_low_bit_degree": degree,
                        "blind_reuse_of_native_quadratic_first_layer_model_falsified": True,
                        "all_higher_bit_algorithms_or_other_parameterizations_ruled_out": False}
    raise AssertionError("seeded higher-carry countercontrol was not reproduced")


def run_controls():
    return {"status": "LOCAL_DERIVATION_REVIEW_PENDING",
            "complete_middle_source_controls": _complete_middle_source_controls(),
            "higher_carry_countercontrol": _higher_carry_countercontrol(),
            "lattice_regime_first_layer_bounds": [lowbit_source_certificate(n, 4 * n * n + 16) for n in (16, 32, 64, 128)],
            "claim_gate": {"first_residue_layer_has_polynomial_reversible_classical_evaluators": True,
                           "efficient_full_growing_modulus_transport_implemented": False,
                           "source_model_closes_under_repeated_normalization": False,
                           "secret_decoding_by_first_layer_alone": False,
                           "quantum_only_mechanism": False,
                           "candidate_record_accepted": False, "speedup_claim_allowed": False,
                           "independent_theorem_review": False, "novelty_claim": False},
            "dependency_sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                                  for p in (Path(__file__), ROOT / "theorems/dcp_carry_packets.py",
                                            ROOT / "theorems/dcp_bell_inference_kernel.py")}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--save", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.save:
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"status": report["status"], "claim_gate": report["claim_gate"]}, indent=2))


if __name__ == "__main__":
    main()
