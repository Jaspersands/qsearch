"""Exact correlated Bell readout likelihoods and a restricted parity audit.

LOCAL DERIVATION / REVIEW PENDING. Trial-secret likelihood evaluation is not
an unknown-secret decoder or a replacement of its quantum input front end.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import random
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

from dcp_carry_packets import (
    binary_rank, calibration_bell_probabilities, calibration_packet_state,
    compile_packet, quadratic_data,
)


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/dcp_correlated_bell.json"


@dataclass(frozen=True)
class Z4Quadratic:
    constant: int
    linear: tuple[int, ...]
    upper_rows: tuple[int, ...]

    def __post_init__(self):
        k = len(self.linear)
        if self.constant not in range(4) or any(b not in range(4) for b in self.linear):
            raise ValueError("Z4 coefficients must be reduced modulo four")
        if len(self.upper_rows) != k or any(row < 0 or row >= 1 << k or row & ((1 << (i + 1)) - 1)
                                           for i, row in enumerate(self.upper_rows)):
            raise ValueError("strictly upper-triangular binary quadratic rows required")

    def evaluate(self, z):
        if not 0 <= z < 1 << len(self.linear):
            raise ValueError("quadratic assignment out of range")
        return (self.constant + sum(b for i, b in enumerate(self.linear) if z >> i & 1)
                + 2 * sum((row & z).bit_count() for i, row in enumerate(self.upper_rows)
                          if z >> i & 1)) % 4


def _binary_gauss(constant, linear_mask, upper_rows):
    """Normalized binary quadratic sum via its symplectic/Arf decomposition."""
    k = len(upper_rows)
    rows = [upper_rows[i] | sum((1 << j) for j in range(i) if upper_rows[j] >> i & 1)
            for i in range(k)]
    rank = binary_rank(rows, k) if k else 0
    def bilinear(u, v):
        return sum((row & v).bit_count() for i, row in enumerate(rows) if u >> i & 1) & 1
    def quadratic(u):
        return ((linear_mask & u).bit_count()
                + sum((row & u).bit_count() for i, row in enumerate(upper_rows) if u >> i & 1)) & 1
    basis = [1 << i for i in range(k)]
    sign, pairs = constant & 1, 0
    while True:
        pair = next(((i, j) for i in range(len(basis)) for j in range(i + 1, len(basis))
                     if bilinear(basis[i], basis[j])), None)
        if pair is None:
            break
        i, j = pair
        u, v = basis[i], basis[j]
        sign ^= quadratic(u) & quadratic(v)
        basis = [w ^ (u if bilinear(w, v) else 0) ^ (v if bilinear(w, u) else 0)
                 for t, w in enumerate(basis) if t not in (i, j)]
        pairs += 1
    assert 2 * pairs == rank
    if any(quadratic(w) for w in basis):
        return Fraction(0)
    return Fraction(-1 if sign else 1, 1 << pairs)


def quadratic_gauss(phase):
    """Exact normalized sum i^phase, including its imaginary part."""
    k = len(phase.linear)
    odd = sum((b & 1) << i for i, b in enumerate(phase.linear))
    if not odd:
        value = _binary_gauss(phase.constant // 2, sum((b // 2) << i for i, b in enumerate(phase.linear)), phase.upper_rows)
        return (Fraction(0), value) if phase.constant & 1 else (value, Fraction(0))
    pivot = (odd & -odd).bit_length() - 1
    free = [i for i in range(k) if i != pivot]
    basis = [(1 << i) | ((1 << pivot) if odd >> i & 1 else 0) for i in free]
    answers = []
    for parity in (0, 1):
        origin = (parity ^ (phase.constant & 1)) << pivot
        def restricted(z):
            x = origin
            for i, v in enumerate(basis):
                if z >> i & 1:
                    x ^= v
            value = phase.evaluate(x)
            assert value & 1 == parity
            return (value - parity) // 2 & 1
        c = restricted(0)
        b = [restricted(1 << j) ^ c for j in range(len(free))]
        upper = tuple(sum((restricted((1 << i) | (1 << j)) ^ b[i] ^ b[j] ^ c) << j
                          for j in range(i + 1, len(free))) for i in range(len(free)))
        answers.append(_binary_gauss(c, sum(value << i for i, value in enumerate(b)), upper) / 2)
    return tuple(answers)


@dataclass(frozen=True)
class BellParityTensor:
    modulus: int
    xor_outcome: int
    parity_mask: int
    constants: tuple[int, ...]
    linear: tuple[tuple[int, ...], ...]
    upper_rows: tuple[tuple[int, ...], ...]
    middle_linear_rank: int
    input_phase_qubits: int

    @property
    def width(self):
        return len(self.linear[0])

    def instantiate(self, secret):
        if len(secret) != len(self.constants):
            raise ValueError("trial secret dimension mismatch")
        reduced = tuple(int(s) % (self.modulus // 2) for s in secret)
        c = sum(s * a for s, a in zip(reduced, self.constants)) % 4
        b = tuple(sum(s * row[j] for s, row in zip(reduced, self.linear)) % 4 for j in range(self.width))
        upper = []
        for j in range(self.width):
            row = 0
            for s, component in zip(reduced, self.upper_rows):
                if s & 1:
                    row ^= component[j]
            upper.append(row)
        return Z4Quadratic(c, b, tuple(upper))

    def bias(self, secret):
        real, imaginary = quadratic_gauss(self.instantiate(secret))
        assert imaginary == 0, "X-parity expectation must be real"
        return real

    def likelihood(self, secret, parity_bit, *, include_xor=True):
        if parity_bit not in (0, 1):
            raise ValueError("binary outcome required")
        value = (1 + (-1 if parity_bit else 1) * self.bias(secret)) / 2
        return value / (1 << self.width) if include_xor else value


def _derivative_tensor(packet, h, offset):
    k, m = packet.retained_qubits, packet.input_qubits
    flip = sum(((row & h).bit_count() & 1) << i for i, row in enumerate(packet.kernel_rows))
    columns = [sum((row >> j & 1) << i for i, row in enumerate(packet.kernel_rows)) for j in range(k)]
    scale = 2 if packet.modulus == 4 else 1
    constants, linear, upper = [], [], []
    for component in packet.labels:
        weights = [a * (1 - 2 * (origin ^ ((row & offset).bit_count() & 1))) if flip >> i & 1 else 0
                   for i, (a, origin, row) in enumerate(zip(component, packet.origin, packet.kernel_rows))]
        assert sum(weights) % 2 == 0
        constants.append(scale * (sum(weights) // 2) % 4)
        linear.append(tuple(-scale * sum(w for i, w in enumerate(weights) if column >> i & 1) % 4
                            for column in columns))
        parity = sum((a & 1) << i for i, a in enumerate(component))
        upper.append(tuple(sum(((parity & flip & columns[i] & columns[j]).bit_count() & 1) << j
                               for j in range(i + 1, k)) for i in range(k)) if scale == 1 else (0,) * k)
    return tuple(constants), tuple(linear), tuple(upper), [row for i, row in enumerate(packet.kernel_rows) if flip >> i & 1]


def compile_bell_parity(left, right, xor_outcome, parity_mask):
    if left.modulus != right.modulus or left.modulus not in (4, 8):
        raise ValueError("exact quadratic marginal compiler requires equal modulus four or eight")
    k = left.retained_qubits
    if left.dimension != right.dimension or k != right.retained_qubits or k == 0:
        raise ValueError("equal nonempty packet widths and dimensions required")
    if not 0 <= xor_outcome < 1 << k or not 0 < parity_mask < 1 << k:
        raise ValueError("nonzero parity mask and valid XOR outcome required")
    c1, b1, q1, rows1 = _derivative_tensor(left, parity_mask, 0)
    c2, b2, q2, rows2 = _derivative_tensor(right, parity_mask, xor_outcome)
    return BellParityTensor(left.modulus, xor_outcome, parity_mask,
        tuple((a + b) % 4 for a, b in zip(c1, c2)),
        tuple(tuple((a + b) % 4 for a, b in zip(x, y)) for x, y in zip(b1, b2)),
        tuple(tuple(a ^ b for a, b in zip(x, y)) for x, y in zip(q1, q2)),
        binary_rank(rows1 + rows2, k), left.input_qubits + right.input_qubits)


def q4_full_bell_likelihood(left, right, secret, xor_outcome, hadamard_outcome):
    """Full correlated outcome law, not a product of its parity marginals."""
    if left.modulus != 4 or right.modulus != 4:
        raise ValueError("full likelihood implemented only at modulus four; q=8 may have cubic phases")
    k = left.retained_qubits
    if left.dimension != right.dimension or k != right.retained_qubits or len(secret) != left.dimension:
        raise ValueError("packet/trial secret mismatch")
    if not 0 <= xor_outcome < 1 << k or not 0 <= hadamard_outcome < 1 << k:
        raise ValueError("Bell outcome out of range")
    l1, q1 = quadratic_data(left)
    l2, q2 = quadratic_data(right)
    def qvalue(form, z):
        return sum(form[i][j] for i in range(k) for j in range(i + 1, k)
                   if z >> i & 1 and z >> j & 1) & 1
    c = sum((s & 1) * (sum(l2[l][i] for i in range(k) if xor_outcome >> i & 1)
                           + qvalue(q2[l], xor_outcome)) for l, s in enumerate(secret)) & 1
    b = tuple(2 * ((hadamard_outcome >> i & 1) ^
                   (sum((s & 1) * (l1[l][i] ^ l2[l][i] ^
                                    (sum(q2[l][i][j] for j in range(k) if xor_outcome >> j & 1) & 1))
                        for l, s in enumerate(secret)) & 1)) for i in range(k))
    upper = tuple(sum((sum((s & 1) * (q1[l][i][j] ^ q2[l][i][j])
                          for l, s in enumerate(secret)) & 1) << j for j in range(i + 1, k)) for i in range(k))
    amplitude, imaginary = quadratic_gauss(Z4Quadratic(2 * c, b, upper))
    assert imaginary == 0
    return amplitude * amplitude / (1 << k)


def dyadic(value):
    value = Fraction(value)
    assert value.denominator & (value.denominator - 1) == 0
    return {"sign": (value.numerator > 0) - (value.numerator < 0),
            "numerator_hex": hex(abs(value.numerator)),
            "denominator_binary_exponent": value.denominator.bit_length() - 1}


def tail_unit_information_certificate(n, fresh_pair_attempts=1):
    """Uniform-secret classical transcript; one chosen tail-unit parity/pair."""
    if n < 4 or fresh_pair_attempts < 1:
        raise ValueError("n>=4 and positive fresh-pair budget required")
    r = n // 2
    count_tail = Fraction(sum(math.comb(2 * n, c) for c in range(r)), 1 << (2 * n))
    row_rank_fail = Fraction(1, 1 << (n - 1 - r))
    prefix_fail = Fraction(2, 1 << n)
    bad_rank = min(Fraction(1), prefix_fail + n * (count_tail + row_rank_fail))
    alpha = min(Fraction(1), bad_rank + Fraction(1, 1 << n) + Fraction(n, 1 << (r + 1)))
    kl = fresh_pair_attempts * alpha
    information = min(Fraction(2 * n), kl)
    success_certificates = {}
    for denominator in (10, 100):
        gap = Fraction(1, denominator) - Fraction(1, 1 << (2 * n))
        success_certificates[f"success_below_one_over_{denominator}"] = gap > 0 and kl / 2 < gap * gap
    return {"status": "LOCAL_DERIVATION_REVIEW_PENDING", "dimension": n,
            "modulus": 8, "secret_parameter_modulus_after_parity_chart": 4,
            "input_qubits_per_packet": 3 * n, "fresh_pair_attempts": fresh_pair_attempts,
            "tail_unit_dictionary_size": n, "middle_rank_floor_outside_bad_event": r + 1,
            "selected_pivot_count_tail_bound": dyadic(count_tail),
            "rank_failure_bound_given_enough_selected_pivots": dyadic(row_rank_fail),
            "two_prefix_rank_failure_bound": dyadic(prefix_fail),
            "public_low_rank_event_probability_upper_bound": dyadic(bad_rank),
            "one_bit_average_squared_bias_upper_bound": dyadic(alpha),
            "transcript_kl_to_matched_fair_reference_bits_upper_bound": dyadic(kl),
            "uniform_secret_mutual_information_bits_upper_bound": dyadic(information),
            "identification_success_expression": "min(1,4^-n+sqrt(KL_bits/2))",
            **success_certificates,
            "high_bits_and_classical_history_can_choose_dictionary_member": True,
            "selector_cannot_inspect_v_before_selecting_parity": True,
            "all_other_v_information_discarded": True,
            "coherent_memory_or_reused_packets_covered": False,
            "external_secret_correlated_side_information_covered": False,
            "full_bell_transcript_covered": False,
            "general_high_level_or_adaptive_quantum_decoder_closed": False,
            "independent_theorem_review": False}


def _gauss_controls():
    digest = hashlib.sha256()
    checks = 0
    for k in range(4):
        pairs = list(itertools.combinations(range(k), 2))
        for c in range(4):
            for linear in itertools.product(range(4), repeat=k):
                for mask in range(1 << len(pairs)):
                    upper = [0] * k
                    for t, (i, j) in enumerate(pairs):
                        if mask >> t & 1:
                            upper[i] |= 1 << j
                    phase = Z4Quadratic(c, linear, tuple(upper))
                    real, imag = quadratic_gauss(phase)
                    roots = [phase.evaluate(z) for z in range(1 << k)]
                    assert real == Fraction(roots.count(0) - roots.count(2), 1 << k)
                    assert imag == Fraction(roots.count(1) - roots.count(3), 1 << k)
                    row = [k, c, list(linear), mask, str(real.numerator), str(real.denominator),
                           str(imag.numerator), str(imag.denominator)]
                    digest.update((json.dumps(row, separators=(",", ":")) + "\n").encode())
                    checks += 1
    return {"complete_quadratic_phase_tables": checks, "exact_value_checksum": digest.hexdigest()}


def _packet_record(packet):
    return {"labels": packet.labels, "modulus": packet.modulus,
            "origin": packet.origin, "kernel_rows_hex": [hex(row) for row in packet.kernel_rows],
            "retained_qubits": packet.retained_qubits}


def _bell_controls():
    rng = random.Random(260910974)
    rows, polynomial_checks, width_mismatch = [], 0, 0
    for q in (4, 8):
        for n, m in ((1, 4), (2, 6)):
            for _ in range(4):
                left = compile_packet([[rng.randrange(q) for _ in range(m)] for _ in range(n)], q)
                right = compile_packet([[rng.randrange(q) for _ in range(m)] for _ in range(n)], q)
                if left.retained_qubits != right.retained_qubits:
                    width_mismatch += 1
                    continue
                left = compile_packet(left.labels, q, rng.randrange(1 << len(left.pivots)))
                right = compile_packet(right.labels, q, rng.randrange(1 << len(right.pivots)))
                k = left.retained_qubits
                u, h = rng.randrange(1 << k), rng.randrange(1, 1 << k)
                tensor = compile_bell_parity(left, right, u, h)
                secret = tuple(rng.randrange(q // 2) for _ in range(n))
                phase = tensor.instantiate(secret)
                for z in range(1 << k):
                    values = [left.residual(z ^ h), right.residual(z ^ h ^ u),
                              left.residual(z), right.residual(z ^ u)]
                    direct = (4 // (q // 2)) * sum(s * (a + b - c - d)
                              for s, a, b, c, d in zip(secret, *values)) % 4
                    assert direct == phase.evaluate(z)
                    polynomial_checks += 1
                probabilities = calibration_bell_probabilities(calibration_packet_state(left, secret),
                                                                calibration_packet_state(right, secret))
                p0 = sum(probabilities[u, v] for v in range(1 << k) if (v & h).bit_count() % 2 == 0)
                exact = tensor.likelihood(secret, 0)
                assert abs(p0 - float(exact)) < 1e-12
                v = rng.randrange(1 << k)
                full = q4_full_bell_likelihood(left, right, secret, u, v) if q == 4 else None
                if full is not None:
                    assert abs(probabilities[u, v] - float(full)) < 1e-12
                rows.append({"left": _packet_record(left), "right": _packet_record(right),
                             "secret_for_calibration_only": secret, "xor_outcome": u, "parity_mask": h,
                             "joint_zero_parity_probability": dyadic(exact),
                             "hadamard_outcome": v, "q4_joint_full_probability": dyadic(full) if full is not None else None,
                             "identity_control_not_candidate_or_native_success_sweep": True})
    return {"controls": rows, "complete_derivative_polynomial_assignments": polynomial_checks,
            "width_mismatch_controls_charged": width_mismatch}


def _native_rank_controls():
    rng = random.Random(3014125)
    rows = []
    for n in (4, 8, 16, 32):
        trials, records, mismatches, prefix_failures = 4, [], 0, 0
        for _ in range(trials):
            packets = [compile_packet([[rng.randrange(8) for _ in range(3 * n)] for _ in range(n)], 8) for _ in range(2)]
            left, right = packets
            if left.retained_qubits != 2 * n or right.retained_qubits != 2 * n:
                mismatches += 1
                continue
            if any(any(p >= 2 * n for p in packet.pivots) for packet in packets):
                prefix_failures += 1
                continue
            u = rng.randrange(1 << (2 * n))
            h = 1 << (n + rng.randrange(n))
            tensor = compile_bell_parity(left, right, u, h)
            secret = tuple(rng.randrange(4) for _ in range(n))
            records.append({"middle_linear_rank": tensor.middle_linear_rank,
                            "secret_has_nonzero_parity": any(s & 1 for s in secret),
                            "known_secret_bias_for_calibration_only": dyadic(tensor.bias(secret))})
        rows.append({"dimension": n, "unconditional_label_pairs_drawn": trials,
                     "nonfull_width_pairs_charged": mismatches, "rows": records,
                     "nonfull_prefix_pairs_charged": prefix_failures,
                     "xor_uniformly_drawn_not_postselected": True,
                     "parity_selected_before_v_and_without_secret": True,
                     "finite_rows_are_not_an_asymptotic_theorem": True})
    return rows


def full_output_countercontrol():
    left = compile_packet([[1, 1, 1]], 4)
    right = compile_packet([[1, 1, 0]], 4)
    full_success = Fraction(0)
    parity_success = Fraction(0)
    for u in range(4):
        for v in range(4):
            full_success += max(q4_full_bell_likelihood(left, right, [s], u, v) / 2 for s in (0, 1))
        tensor = compile_bell_parity(left, right, u, 1)
        for b in (0, 1):
            parity_success += max(tensor.likelihood([s], b) / 2 for s in (0, 1))
    assert full_success == Fraction(7, 8)
    assert parity_success == Fraction(3, 4)
    return {"q4_nonmatching_full_readout_bayes_success": dyadic(full_success),
            "one_coordinate_parity_bayes_success": dyadic(parity_success),
            "fixed_dimension_control_not_new_speedup": True,
            "absence_of_public_common_radical_does_not_imply_no_full_information": True}


def middle_parseval_controls():
    records = []
    for low_right in ([[1, 1, 1]], [[1, 1, 0]]):
        left_low = [[1, 1, 1]]
        base_left, base_right = compile_packet(left_low, 8), compile_packet(low_right, 8)
        for u in range(4):
            for h in range(1, 4):
                rank = compile_bell_parity(base_left, base_right, u, h).middle_linear_rank
                sums = {s: Fraction(0) for s in (1, 3)}
                for labels in range(64):
                    left = compile_packet([[b + 2 * (labels >> i & 1) for i, b in enumerate(left_low[0])]], 8)
                    right = compile_packet([[b + 2 * (labels >> (i + 3) & 1) for i, b in enumerate(low_right[0])]], 8)
                    tensor = compile_bell_parity(left, right, u, h)
                    assert tensor.middle_linear_rank == rank
                    for s in sums:
                        sums[s] += tensor.bias([s])**2
                for s, total in sums.items():
                    average = total / 64
                    assert average == Fraction(1, 1 << rank)
                    records.append({"left_low": left_low, "right_low": low_right,
                                    "xor_outcome": u, "parity_mask": h, "secret_for_calibration_only": s,
                                    "middle_tables_exhausted": 64, "middle_linear_rank": rank,
                                    "average_squared_bias": dyadic(average),
                                    "equality_uses_invariance_along_selected_row_kernel": True,
                                    "top_bits_fixed_only_because_their_magnitude_effect_is_a_global_phase": True})
    left = compile_packet([[1, 1, 1]], 8)
    even = compile_bell_parity(left, left, 0, 1).bias([2])**2
    assert even == 1
    return {"rows": records, "nonzero_secret_parity_precondition_required": True,
            "all_even_secret_exception_squared_bias_witness": dyadic(even),
            "bounded_identity_controls_not_scalable_candidate_family": True}


def run_controls():
    return {"status": "LOCAL_DERIVATION_REVIEW_PENDING", "quadratic_gauss": _gauss_controls(),
            "physical_bell": _bell_controls(), "native_rank_controls": _native_rank_controls(),
            "full_output_countercontrol": full_output_countercontrol(),
            "middle_parseval_controls": middle_parseval_controls(),
            "tail_unit_information_certificates": [tail_unit_information_certificate(n, n * n)
                                                   for n in (8, 16, 32, 64, 128)],
            "claim_gate": {"matched_packets_or_copies_required": False,
                           "full_q8_likelihood_implemented": False,
                           "marginals_can_be_multiplied_as_independent": False,
                           "unknown_secret_decoder": False,
                           "known_secret_simulation_is_dequantization": False,
                           "all_full_output_or_quantum_adaptive_measurements_closed": False,
                           "independent_theorem_review": False, "speedup_claim_allowed": False},
            "dependency_sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                                  for p in (Path(__file__), ROOT / "theorems/dcp_carry_packets.py")}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--save", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.save:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"status": report["status"], "gauss": report["quadratic_gauss"],
                      "bell_controls": len(report["physical_bell"]["controls"]),
                      "claim_gate": report["claim_gate"]}, indent=2))


if __name__ == "__main__":
    main()
