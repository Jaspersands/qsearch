"""Full Bell source moments across growing moduli, not an unknown-secret decoder.

LOCAL DERIVATION / REVIEW PENDING. Collision fluctuations are not mutual
information, sample complexity, efficient inference, or a speedup certificate.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path

from dcp_carry_packets import binary_rank, compile_packet
from dcp_correlated_bell import dyadic

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/dcp_full_bell_source_moments.json"


def full_collision_source_certificate(left, right, *, enumeration_cap=14):
    """Exact HIGH-LABEL averaged N sum_v P(v|u,s)^2, for fixed low charts."""
    q, k = left.modulus, left.retained_qubits
    if q != right.modulus or q < 8 or q & (q - 1):
        raise ValueError("equal power-of-two moduli at least eight required")
    if left.dimension != right.dimension or k != right.retained_qubits:
        raise ValueError("equal packet dimensions and logical widths required")
    if k > enumeration_cap:
        raise ValueError("full mask enumeration is exponential; cap exceeded")
    physical_rows = left.kernel_rows + right.kernel_rows
    counts = {}
    count = 0
    for h in range(1 << k):
        rank = binary_rank([row for row in physical_rows if (row & h).bit_count() & 1], k)
        counts[rank] = counts.get(rank, 0) + 1
        count += 1 << (k - rank)
    return {"status": "LOCAL_DERIVATION_REVIEW_PENDING", "modulus": q,
            "logical_width": k, "input_phase_qubits": left.input_qubits + right.input_qubits,
            "selected_row_rank_histogram": {str(r): c for r, c in sorted(counts.items())},
            "ordered_disjoint_physical_direction_pairs": count,
            "high_label_mean_relative_full_collision": dyadic(Fraction(count, 1 << k)),
            "universal_mean_relative_collision_lower_bound": dyadic(Fraction(2) - Fraction(1, 1 << k)),
            "requires_nonzero_secret_parity": True,
            "conditions_on_low_labels_and_public_charts": True,
            "uniform_average_over_all_remaining_label_bits": True,
            "independent_of_xor_and_initial_syndrome": True,
            "mask_enumeration_count": 1 << k, "mask_enumeration_is_polynomial": False,
            "full_secret_likelihood_evaluator_implemented": False,
            "statistic_is_mutual_information": False,
            "source_tail_concentration_proved": False,
            "unknown_secret_decoder": False, "speedup_claim_allowed": False}


def systematic_source_mean(n):
    """Native n x 3n source conditional on each first n columns invertible."""
    if n < 1:
        raise ValueError("positive vector dimension required")
    k = 2 * n
    prefix = Fraction(1)
    for j in range(1, n + 1):
        prefix *= 1 - Fraction(1, 1 << j)
    mean = Fraction(2) - Fraction(1, 1 << k)
    mean += Fraction(3**k - (1 << (k + 1)) + 1, 1 << k) * Fraction(3, 4)**(2 * n)
    return {"status": "LOCAL_DERIVATION_REVIEW_PENDING", "dimension": n,
            "logical_width": k, "input_qubits_per_packet": 3 * n,
            "two_public_prefix_invertibility_probability": dyadic(prefix * prefix),
            "conditional_mean_relative_full_collision": dyadic(mean),
            "public_source_rejection_charged": True,
            "prefix_selection_is_secret_independent": True,
            "conditions_on_prefix_success_not_unconditional_claim": True,
            "valid_for_all_power_of_two_moduli_at_least_eight": True,
            "requires_nonzero_secret_parity": True,
            "mean_does_not_prove_typical_instance_signal": True,
            "mean_does_not_prove_information_or_efficiency": True,
            "speedup_claim_allowed": False}


def fresh_native_verification_certificate(modulus, secret_minus_candidate, tests=1):
    """Source-averaged soundness of public candidate phase correction + H."""
    if modulus < 2 or modulus & (modulus - 1) or tests < 1 or not secret_minus_candidate:
        raise ValueError("power-of-two modulus, nonempty difference and positive test count required")
    delta = tuple(int(x) % modulus for x in secret_minus_candidate)
    divisor = math.gcd(modulus, *delta)
    equal = divisor == modulus
    return {"status": "LOCAL_DERIVATION_REVIEW_PENDING", "modulus": modulus,
            "dimension": len(delta), "verification_states_consumed": tests,
            "difference_character_image_order": modulus // divisor,
            "candidate_equals_secret": equal,
            "one_test_high_source_average_acceptance": dyadic(Fraction(1) if equal else Fraction(1, 2)),
            "all_tests_high_source_average_acceptance": dyadic(Fraction(1) if equal else Fraction(1, 1 << tests)),
            "requires_fresh_original_native_phase_states": True,
            "does_not_grant_phase_state_from_carry_packet": True,
            "candidate_committed_before_verification_labels": True,
            "all_native_labels_retained_no_postselection": True,
            "public_known_candidate_phase_correction_not_unknown_inverse": True,
            "ideal_noiseless_and_exact_measurement_model": True,
            "unknown_secret_used_only_for_calibration_certificate": True,
            "decoder_implemented": False, "speedup_claim_allowed": False}


def fresh_packet_verification_certificate(packet, secret_minus_residue, tests=1):
    """Native higher-label mean for known-residue phase correction + H^k."""
    if packet.modulus < 4 or tests < 1 or len(secret_minus_residue) != packet.dimension:
        raise ValueError("modulus at least four, matching difference and positive test count required")
    Q = packet.modulus // 2
    equal = all(int(x) % Q == 0 for x in secret_minus_residue)
    k = packet.retained_qubits
    return {"status": "LOCAL_DERIVATION_REVIEW_PENDING", "modulus": packet.modulus,
            "packet_secret_modulus": Q, "logical_width": k,
            "candidate_equals_packet_residue": equal,
            "fresh_packets_consumed": tests,
            "fresh_original_phase_states_consumed": tests * packet.input_qubits,
            "one_test_conditional_high_source_mean_acceptance": dyadic(Fraction(1) if equal else Fraction(1, 1 << k)),
            "all_tests_conditional_high_source_mean_acceptance": dyadic(Fraction(1) if equal else Fraction(1, 1 << (k * tests))),
            "conditions_on_low_labels_chart_and_syndrome": True,
            "candidate_committed_before_fresh_higher_labels": True,
            "uniform_native_higher_labels_required": True,
            "no_secret_parity_precondition": True,
            "does_not_recover_lost_original_high_bit": True,
            "known_public_residue_phase_correction_not_hidden_inverse": True,
            "ideal_noiseless_exact_model": True,
            "residue_decoder_implemented": False, "speedup_claim_allowed": False}


def known_residue_phase_correction_plan(packet, candidate):
    """One reusable clean ancilla; affine parity compute/phase/uncompute."""
    if len(candidate) != packet.dimension:
        raise ValueError("known residue candidate dimension mismatch")
    candidate = tuple(int(x) % (packet.modulus // 2) for x in candidate)
    steps = []
    for i, (origin, row) in enumerate(zip(packet.origin, packet.kernel_rows)):
        exponent = -sum(c * A[i] for c, A in zip(candidate, packet.labels)) % packet.modulus
        if exponent:
            steps.append({"physical_coordinate": i, "affine_origin": origin,
                          "logical_parity_mask_hex": hex(row),
                          "known_phase_exponent_mod_q_hex": hex(exponent)})
    return {"status": "PUBLIC_KNOWN_CANDIDATE_PLAN_NOT_UNKNOWN_PREPARATION_INVERSE",
            "modulus": packet.modulus, "logical_width": packet.retained_qubits,
            "steps_compute_phase_uncompute": steps, "reusable_clean_ancillas": 1,
            "known_diagonal_phase_gates": len(steps),
            "cnot_gates": 2 * sum(int(s["logical_parity_mask_hex"], 16).bit_count() for s in steps),
            "x_gates": 2 * sum(s["affine_origin"] for s in steps),
            "candidate_dependent_global_phase_ignored": True,
            "unknown_secret_or_phase_evaluator_required": False,
            "angle_precision_cost_must_be_charged": True,
            "physical_backend_execution_verified": False}


def known_residue_high_bit_completion_bound(n, failure_exponent=40):
    if n < 1 or failure_exponent < 1:
        raise ValueError("positive dimension and failure exponent required")
    samples = n + failure_exponent
    failure = Fraction((1 << n) - 1, 1 << samples)
    return {"status": "LOCAL_DERIVATION_REVIEW_PENDING", "dimension": n,
            "requires_correct_known_s_mod_q_over_two": True,
            "fresh_original_phase_states_consumed": samples,
            "highest_bit_vector_binary_rank_failure_upper_bound": dyadic(failure),
            "public_candidate_correction_followed_by_hadamard": True,
            "classical_binary_equation_solver_required": True,
            "all_labels_retained_no_source_postselection": True,
            "incorrect_residue_not_covered": True, "noise_or_rotation_error_not_covered": True,
            "residue_decoder_implemented": False, "speedup_claim_allowed": False}


def _independent_disjoint_count(left, right):
    def physical(packet, mask):
        return sum(((row & mask).bit_count() & 1) << i for i, row in enumerate(packet.kernel_rows))
    images = [[physical(packet, z) for z in range(1 << packet.retained_qubits)] for packet in (left, right)]
    return sum(not (x[h] & x[j]) and not (y[h] & y[j])
               for h in range(len(images[0])) for j in range(len(images[0]))
               for x, y in [images])


def _physical_full_probabilities(left, right, secret, u):
    """Bounded q=8 fourth-root identity control, not a production sampler."""
    if left.modulus != 8 or left.retained_qubits > 8:
        raise ValueError("bounded modulus-eight control required")
    k = left.retained_qubits
    phases = [(sum(s * (a + b) for s, a, b in zip(secret, left.residual(z), right.residual(z ^ u)))) % 4
              for z in range(1 << k)]
    output = []
    for v in range(1 << k):
        roots = [0] * 4
        for z, phase in enumerate(phases):
            roots[(phase + 2 * ((z & v).bit_count() & 1)) % 4] += 1
        output.append(Fraction((roots[0] - roots[2])**2 + (roots[1] - roots[3])**2, 1 << (2 * k)))
    assert sum(output) == 1
    return output


def _complete_q8_source_control():
    low = ([[1, 1, 1]], [[1, 1, 0]])
    base = [compile_packet(A, 8) for A in low]
    cert = full_collision_source_certificate(*base)
    averages = {u: Fraction(0) for u in (0, 3)}
    for high in itertools.product(range(4), repeat=6):
        packets = [compile_packet([[b + 2 * high[side * 3 + i] for i, b in enumerate(A[0])]], 8)
                   for side, A in enumerate(low)]
        for u in averages:
            p = _physical_full_probabilities(*packets, [1], u)
            conjugate = _physical_full_probabilities(*packets, [3], u)
            assert p == conjugate
            averages[u] += (1 << packets[0].retained_qubits) * sum(x * x for x in p)
    count = 4**6
    expected = Fraction(cert["ordered_disjoint_physical_direction_pairs"], 4)
    assert all(value / count == expected for value in averages.values())
    return {"left_low": low[0], "right_low": low[1], "complete_higher_label_tables": count,
            "xor_outcomes_checked": list(averages),
            "source_mean_relative_collisions": {str(u): dyadic(a / count) for u, a in averages.items()},
            "all_tables_obey_secret_negation_invariance": True,
            "certificate": cert, "bounded_identity_control_not_candidate": True}


def _quartet_controls():
    records = []
    for q in (8, 16, 32, 128):
        left, right = compile_packet([[1, 1, 1]], q), compile_packet([[1, 1, 0]], q)
        k = left.retained_qubits
        count = 0
        for a, b, c, d in itertools.product(range(1 << k), repeat=4):
            valid = True
            for packet in (left, right):
                for row in packet.kernel_rows:
                    delta = sum(sign * ((row & z).bit_count() & 1) for sign, z in zip((1, -1, 1, -1), (a, b, c, d)))
                    valid &= delta % (q // 2) == 0
            count += valid
        cert = full_collision_source_certificate(left, right)
        assert count == (1 << k) * cert["ordered_disjoint_physical_direction_pairs"]
        records.append({"modulus": q, "physical_source_surviving_quartets": count,
                        "quartets_checked": 1 << (4 * k), "certificate": cert})
    return records


def _systematic_control():
    total = Fraction(0)
    for a, b in itertools.product(range(4), repeat=2):
        packets = [compile_packet([[1, code & 1, code >> 1]], 8) for code in (a, b)]
        count = _independent_disjoint_count(*packets)
        cert = full_collision_source_certificate(*packets)
        assert cert["ordered_disjoint_physical_direction_pairs"] == count
        total += Fraction(count, 4)
    assert total / 16 == Fraction(65, 32)
    return {"dimension": 1, "complete_systematic_pair_tables": 16,
            "mean_relative_collision": dyadic(total / 16),
            "full_source_formula": systematic_source_mean(1)}


def run_controls():
    return {"status": "LOCAL_DERIVATION_REVIEW_PENDING",
            "complete_q8_source": _complete_q8_source_control(),
            "growing_modulus_quartets": _quartet_controls(),
            "systematic_source_control": _systematic_control(),
            "systematic_source_scaling": [systematic_source_mean(n) for n in (1, 2, 4, 8, 16, 32, 64, 128)],
            "fresh_native_candidate_verification": [fresh_native_verification_certificate(q, delta, 40)
                                                    for q, delta in ((8, [2]), (128, [64, 0]),
                                                                     (1 << 64, [2, 0]), (8, [0]))],
            "fresh_packet_residue_verification": [fresh_packet_verification_certificate(
                compile_packet([[1, 1, 1]], 8), [delta], 3) for delta in (0, 1, 2, 3)],
            "known_residue_high_bit_completion": [known_residue_high_bit_completion_bound(n)
                                                   for n in (8, 32, 128)],
            "known_residue_correction_plan": known_residue_phase_correction_plan(
                compile_packet([[1, 3, 5, 7]], 8, 1), [1]),
            "claim_gate": {"one_bit_gate_cannot_close_full_output": True,
                           "collision_mean_is_secret_mutual_information": False,
                           "typical_source_concentration_proved": False,
                           "full_bell_real_measurement_is_invariant_under_secret_negation": True,
                           "negation_ambiguity_closes_general_complex_measurements": False,
                           "unknown_secret_decoder": False, "independent_theorem_review": False,
                           "speedup_claim_allowed": False},
            "dependency_sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                                  for p in (Path(__file__), ROOT / "theorems/dcp_carry_packets.py",
                                            ROOT / "theorems/dcp_correlated_bell.py")}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--save", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.save:
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"status": report["status"], "complete_q8_tables": 4**6,
                      "claim_gate": report["claim_gate"]}, indent=2))


if __name__ == "__main__":
    main()
