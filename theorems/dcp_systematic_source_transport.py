"""Low-selected systematic native label transport with fixed-secret covariance.

LOCAL DERIVATION / REVIEW PENDING. This only changes public label coordinates.
It does not supply an algorithm for unknown phase or residue decoding.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

from dcp_bell_inference_kernel import exact
from dcp_lowbit_fiber_normalizer import _inverse_rows

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/dcp_systematic_source_transport.json"


def _multiply(A, B, modulus):
    return tuple(tuple(sum(a * B[j][l] for j, a in enumerate(row)) % modulus
                       for l in range(len(B[0]))) for row in A)


def _transpose(A):
    return tuple(zip(*A))


def _apply(A, vector, modulus):
    return tuple(sum(a * b for a, b in zip(row, vector)) % modulus for row in A)


def _lift_inverse(T, binary_inverse, modulus):
    n, precision, Y = len(T), 2, binary_inverse
    while precision < modulus:
        precision = min(modulus, precision * precision)
        TY = _multiply(T, Y, precision)
        correction = tuple(tuple((2 * int(i == j) - TY[i][j]) % precision for j in range(n)) for i in range(n))
        Y = _multiply(Y, correction, precision)
    identity = tuple(tuple(int(i == j) for j in range(n)) for i in range(n))
    assert _multiply(T, Y, modulus) == _multiply(Y, T, modulus) == identity
    return Y


@dataclass(frozen=True)
class SystematicSourceTransport:
    binary_prefix: tuple[tuple[int, ...], ...]
    modulus: int
    row_transform: tuple[tuple[int, ...], ...]
    row_transform_inverse: tuple[tuple[int, ...], ...]

    def transform_labels(self, labels):
        n = len(self.binary_prefix)
        if len(labels) != n or not labels or len(labels[0]) < n or any(len(row) != len(labels[0]) for row in labels):
            raise ValueError("rectangular labels with declared n-column prefix required")
        if any(type(a) is not int for row in labels for a in row):
            raise ValueError("integer public labels required")
        if any((labels[l][i] & 1) != self.binary_prefix[l][i] for l in range(n) for i in range(n)):
            raise ValueError("transport was compiled for a different binary prefix")
        return _multiply(self.row_transform, tuple(tuple(row) for row in labels), self.modulus)

    def transport_secret(self, secret):
        if len(secret) != len(self.binary_prefix) or any(type(x) is not int for x in secret):
            raise ValueError("matching integer calibration secret required")
        return _apply(_transpose(self.row_transform_inverse), secret, self.modulus)

    def recover_secret_coordinates(self, transformed_secret):
        if len(transformed_secret) != len(self.binary_prefix) or any(type(x) is not int for x in transformed_secret):
            raise ValueError("matching recovered integer coordinates required")
        return _apply(_transpose(self.row_transform), transformed_secret, self.modulus)

    def record(self):
        return {"binary_prefix": self.binary_prefix, "modulus_hex": hex(self.modulus),
                "row_transform": self.row_transform,
                "row_transform_inverse_hex": [[hex(x) for x in row] for row in self.row_transform_inverse],
                "selection_uses_binary_prefix_only": True,
                "row_transform_uses_actual_full_label_prefix_inverse": False,
                "secret_transform": "s_prime=T^(-transpose)*s mod q; calibration only",
                "coordinate_recovery": "s=T^transpose*s_prime mod q; after a real decoder exists",
                "unknown_secret_recovered": False}


def compile_transport(binary_prefix, modulus):
    if type(modulus) is not int or modulus < 8 or modulus & (modulus - 1):
        raise ValueError("power-of-two q>=8 required")
    P = tuple(tuple(row) for row in binary_prefix)
    n = len(P)
    if not n or any(len(row) != n or any(type(a) is not int or a not in (0, 1) for a in row) for row in P):
        raise ValueError("nonempty square binary prefix required")
    rows = tuple(sum(a << j for j, a in enumerate(row)) for row in P)
    inverse = _inverse_rows(rows)
    T = tuple(tuple(row >> j & 1 for j in range(n)) for row in inverse)
    Y = _lift_inverse(T, P, modulus)
    return SystematicSourceTransport(P, modulus, T, Y)


def native_systematic_source_certificate(n, input_states, *, attempts=1):
    if any(type(x) is not int for x in (n, input_states, attempts)) or n < 1 or input_states < n or attempts < 1:
        raise ValueError("positive dimension/attempts and enough original states required")
    success = math.prod(1 - Fraction(1, 1 << j) for j in range(1, n + 1))
    return {"status": "EXACT_LOW_SELECTED_NATIVE_SYSTEMATIC_SOURCE_NOT_DECODER",
            "dimension": n, "original_states_per_attempt": input_states, "allocated_attempts": attempts,
            "original_states_charged": input_states * attempts,
            "exact_binary_prefix_acceptance_probability": exact(success),
            "all_allocated_attempts_reject_probability": exact((1 - success) ** attempts),
            "expected_attempts_until_acceptance": exact(1 / success),
            "expected_attempts_upper_bound": 4,
            "conditioning": "first n binary columns invertible; low-only T is binary-prefix inverse lifted with entries0/1",
            "transformed_binary_prefix_is_identity": True,
            "transformed_higher_bits_on_every_column_are_iid_uniform_conditional_on_entire_transformed_B": True,
            "transformed_tail_full_labels_are_iid_uniform_and_independent_of_original_binary_prefix": True,
            "transformed_prefix_full_labels_are_exact_identity": False,
            "same_source_law_requires_low_only_transform_not_full_prefix_inverse": True,
            "fixed_secret_transport_is_conditioned_on_original_binary_prefix": True,
            "uniform_secret_average_is_automatically_a_fixed_secret_decoder_guarantee": False,
            "labels_changed_requires_extra_unknown_state_preparation": False,
            "q_over_2_residue_coordinates_transform_back_mod_q_over_2_only": True,
            "lost_original_top_bits_still_require_fresh_completion": True,
            "different_transformed_secret_coordinates_across_packets_must_be_reconciled": True,
            "finite_profile_statistics_are_native_scaling_theorems": False,
            "candidate_record_accepted": False, "speedup_claim_allowed": False}


def _complete_source_controls():
    q, records = 8, []
    for n in (1, 2):
        prefixes = []
        totals, phase_checks = Counter(), 0
        for bits in itertools.product((0, 1), repeat=n * n):
            P = tuple(tuple(bits[n * l:n * (l + 1)]) for l in range(n))
            try:
                transport = compile_transport(P, q)
            except ValueError:
                continue
            histograms = []
            for low in itertools.product((0, 1), repeat=n):
                values = Counter()
                for H in itertools.product(range(q // 2), repeat=n):
                    A = tuple(tuple(P[l]) + (low[l] + 2 * H[l],) for l in range(n))
                    transformed = transport.transform_labels(A)
                    col = tuple(transformed[l][-1] for l in range(n))
                    values[col] += 1
                    totals[col] += 1
                assert len(values) == (q // 2) ** n and set(values.values()) == {1}
                histograms.append({"original_tail_low_column": low,
                                   "transformed_tail_low_column": _apply(transport.row_transform, low, 2),
                                   "distinct_higher_lifts": len(values), "each_lift_multiplicity": 1})
            prefix_high_outputs = set()
            for H in itertools.product(range(q // 2), repeat=n * n):
                labels = tuple(tuple(P[l][i] + 2 * H[n * l + i] for i in range(n)) for l in range(n))
                transformed = transport.transform_labels(labels)
                assert all(transformed[l][i] & 1 == int(l == i) for l in range(n) for i in range(n))
                prefix_high_outputs.add(transformed)
            assert len(prefix_high_outputs) == (q // 2) ** (n * n)
            sample = tuple(tuple(P[l][i] + 2 * ((l + i + 1) % 4) for i in range(n)) + (3 + 2 * l,) for l in range(n))
            transformed = transport.transform_labels(sample)
            for s in itertools.product(range(q), repeat=n):
                sp = transport.transport_secret(s)
                assert transport.recover_secret_coordinates(sp) == s
                for i in range(n + 1):
                    assert sum(sample[l][i] * s[l] for l in range(n)) % q == sum(transformed[l][i] * sp[l] for l in range(n)) % q
                    phase_checks += 1
            prefixes.append({"transport": transport.record(), "tail_coset_controls": histograms,
                             "distinct_transformed_higher_prefix_tables": len(prefix_high_outputs)})
        assert len(totals) == q ** n and set(totals.values()) == {len(prefixes)}
        records.append({"dimension": n, "modulus": q, "all_invertible_binary_prefixes": len(prefixes),
                        "exact_acceptance_probability": exact(Fraction(len(prefixes), 1 << (n * n))),
                        "transports": prefixes, "complete_tail_label_vectors": len(totals),
                        "each_tail_label_vector_multiplicity_over_prefixes": len(prefixes),
                        "fixed_secret_phase_covariance_checks": phase_checks})
    return records


def run_controls():
    P = ((1, 1, 0), (0, 1, 1), (1, 1, 1))
    large = compile_transport(P, 1 << 65)
    return {"status": "LOCAL_DERIVATION_REVIEW_PENDING", "complete_native_source_controls": _complete_source_controls(),
            "arbitrary_precision_transport_control": large.record(),
            "scaling_source_ledgers": [native_systematic_source_certificate(n, 4 * n * n + 16 + n, attempts=8)
                                       for n in (2, 4, 8, 16, 32)],
            "claim_gate": {"systematic_identity_binary_prefix_can_be_native_with_constant_acceptance": True,
                           "higher_labels_stay_native_under_low_selected_row_transport": True,
                           "full_label_prefix_inverse_preserves_same_higher_prefix_law": False,
                           "finite_systematic_profiles_establish_a_scalable_decoder": False,
                           "independent_theorem_review": False, "novelty_claim": False,
                           "candidate_record_accepted": False, "speedup_claim_allowed": False},
            "dependency_sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                                  for p in (Path(__file__), ROOT / "theorems/dcp_lowbit_fiber_normalizer.py")}}


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
