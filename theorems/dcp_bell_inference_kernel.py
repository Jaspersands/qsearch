"""Source-aware Bell inference geometry, SQ scope and independent readout noise.

LOCAL DERIVATION / REVIEW PENDING. No decoder, generic hardness theorem,
independent review, natural noise reduction or speedup claim.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path

from dcp_carry_packets import binary_rank, compile_packet, quadratic_data
from dcp_full_bell_source_moments import _physical_full_probabilities, systematic_source_mean

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/dcp_bell_inference_kernel.json"


def exact(value):
    value = Fraction(value)
    return {"sign": (value > 0) - (value < 0), "numerator_hex": hex(abs(value.numerator)),
            "denominator_hex": hex(value.denominator)}


def _read_dyadic(value):
    return Fraction(value["sign"] * int(value["numerator_hex"], 16),
                    1 << value["denominator_binary_exponent"])


def _noise(value):
    value = Fraction(value)
    if not 0 <= value <= Fraction(1, 2):
        raise ValueError("independent output-bit flip rate must be in [0,1/2]")
    return value


def _packet_pair(left, right):
    if (left.modulus != right.modulus or left.modulus < 8 or
            left.dimension != right.dimension or left.retained_qubits != right.retained_qubits):
        raise ValueError("equal packet modulus>=8, dimension and width required")


def _scalar_quadratic_rows(left, right, secret):
    Q, k = left.modulus // 2, left.retained_qubits
    e = [x // (Q // 2) for x in secret]
    forms = []
    for packet in (left, right):
        binary = compile_packet([[a % 4 for a in row] for row in packet.labels], 4, packet.syndrome)
        _, quadratic = quadratic_data(binary)
        forms.append(quadratic)
    return [sum((sum(e[l] * (forms[0][l][i][j] ^ forms[1][l][i][j])
                     for l in range(left.dimension)) & 1) << j for j in range(k)) for i in range(k)]


def cross_secret_kernel(left, right, s, t, *, bit_flip_probability=0, enumeration_cap=14):
    """E_high [N sum_v p_s(v|u,A) p_t(v|u,A)], including exact noisy law."""
    _packet_pair(left, right)
    Q, k = left.modulus // 2, left.retained_qubits
    if len(s) != left.dimension or len(t) != left.dimension:
        raise ValueError("secret dimension mismatch")
    s, t = tuple(int(x) % Q for x in s), tuple(int(x) % Q for x in t)
    same_orbit = t == s or t == tuple(-x % Q for x in s)
    flip = _noise(bit_flip_probability)
    weight = (1 - 2 * flip)**2
    order = Q // math.gcd(Q, *s)
    count, rank = 0, None
    if not same_orbit:
        value = Fraction(1)
        cost = "constant_after_vector_comparison"
    elif order <= 2 and flip == 0:
        rank = binary_rank(_scalar_quadratic_rows(left, right, s), k)
        value = Fraction(1 << k, 1 << rank)
        cost = "polynomial_binary_rank"
    else:
        if k > enumeration_cap:
            raise ValueError("diagonal weighted mask enumeration is exponential; cap exceeded")
        rows = left.kernel_rows + right.kernel_rows
        quadratic = _scalar_quadratic_rows(left, right, s) if order <= 2 else None
        value = Fraction(0)
        for h in range(1 << k):
            if quadratic is None:
                R = binary_rank([row for row in rows if (row & h).bit_count() & 1], k)
                contribution = Fraction(1, 1 << R)
            else:
                contribution = int(all((row & h).bit_count() % 2 == 0 for row in quadratic))
            value += weight**h.bit_count() * contribution
            count += 1
        cost = "exponential_public_mask_sum"
    return {"status": "LOCAL_DERIVATION_REVIEW_PENDING", "modulus": left.modulus,
            "packet_secret_modulus": Q, "logical_width": k,
            "secret_s": list(s), "secret_t": list(t), "same_negation_orbit": same_orbit,
            "secret_s_character_order": order, "output_bit_flip_probability": exact(flip),
            "source_mean_relative_cross_collision": exact(value),
            "centered_likelihood_inner_product": exact(value - 1),
            "order_two_combined_quadratic_rank": rank, "evaluation_cost_class": cost,
            "public_masks_enumerated": count,
            "conditions_on_low_charts_not_fixed_high_labels": True,
            "higher_labels_uniform_and_independent_required": True,
            "independent_of_xor_and_initial_syndrome": True,
            "is_mutual_information_or_sample_complexity": False,
            "unknown_secret_decoder": False, "speedup_claim_allowed": False}


def systematic_noisy_source_mean(n, bit_flip_probability=0):
    if n < 1:
        raise ValueError("positive vector dimension required")
    epsilon = _noise(bit_flip_probability)
    t, k, N = (1 - 2 * epsilon)**2, 2 * n, 1 << (2 * n)
    zero_members = N + (1 + t)**k - 1
    nonzero_pairs = (2 + t)**k - zero_members
    value = (zero_members + nonzero_pairs * Fraction(3, 4)**(2 * n)) / N
    assert value >= 1
    prefix = _read_dyadic(systematic_source_mean(n)["two_public_prefix_invertibility_probability"])
    return {"status": "LOCAL_DERIVATION_REVIEW_PENDING", "dimension": n,
            "logical_width": k, "output_bit_flip_probability": exact(epsilon),
            "squared_fourier_attenuation_per_bit": exact(t),
            "conditional_mean_relative_full_collision": exact(value),
            "joint_source_likelihood_chi_squared_to_uniform_reference": exact(value - 1),
            "two_public_prefix_invertibility_probability": exact(prefix),
            "leading_moment_base_per_logical_qubit": exact(3 * (2 + t) / 8),
            "exponential_uniformization_regime": t < Fraction(2, 3),
            "uniformization_not_claimed_at_threshold": t == Fraction(2, 3),
            "secret_character_order_at_least_four_required": True,
            "conditions_on_public_prefix_event": True,
            "requires_independent_logical_output_bit_flips": True,
            "correlated_native_phase_errors_covered": False,
            "all_measurements_or_quantum_memory_covered": False, "speedup_claim_allowed": False}


def detector_repetition_countercontrol(bit_flip_probability, repetitions, logical_width):
    if repetitions < 1 or repetitions % 2 != 1 or logical_width < 1:
        raise ValueError("odd positive repetitions and positive logical width required")
    epsilon = _noise(bit_flip_probability)
    effective = sum(Fraction(math.comb(repetitions, j)) * epsilon**j * (1 - epsilon)**(repetitions - j)
                    for j in range(repetitions // 2 + 1, repetitions + 1))
    return {"status": "READOUT_ONLY_COUNTERCONTROL_NOT_NATIVE_PHASE_ERROR_REPAIR",
            "detector_flip_probability": exact(epsilon), "repetitions_per_logical_bit": repetitions,
            "majority_vote_effective_flip_probability": exact(effective),
            "logical_width": logical_width, "additional_clean_ancillas": logical_width * (repetitions - 1),
            "additional_cnot_gates": logical_width * (repetitions - 1),
            "measured_bits": logical_width * repetitions,
            "copies_only_computational_basis_value_not_unknown_state": True,
            "assumes_ideal_post_hadamard_copy_gates_and_independent_detector_errors": True,
            "repairs_pre_hadamard_phase_errors": False,
            "remains_in_uniformization_regime": (1 - 2 * effective)**2 < Fraction(2, 3),
            "physical_backend_execution_verified": False, "speedup_claim_allowed": False}


def _rational_read(value):
    return Fraction(value["sign"] * int(value["numerator_hex"], 16), int(value["denominator_hex"], 16))


def statistical_query_certificate(n, modulus, queries, tolerance):
    if n < 1 or modulus < 8 or modulus & (modulus - 1) or queries < 1:
        raise ValueError("positive dimension/budget and power-of-two modulus>=8 required")
    tau = Fraction(tolerance)
    if not 0 < tau <= 1:
        raise ValueError("SQ tolerance must be in (0,1]")
    Q = modulus // 2
    M = (Q**n - (Q // 2)**n) // 2
    source = systematic_source_mean(n)
    d = _read_dyadic(source["conditional_mean_relative_full_collision"]) - 1
    distinguishable = min(M, d // (tau * tau))
    success = min(Fraction(1), Fraction(queries * distinguishable + 1, M))
    return {"status": "LOCAL_DERIVATION_REVIEW_PENDING", "dimension": n, "modulus": modulus,
            "odd_secret_negation_orbits_hex": hex(M), "statistical_queries": queries,
            "absolute_expectation_tolerance": exact(tau),
            "common_centered_likelihood_squared_norm": exact(d),
            "two_public_prefix_invertibility_probability": exact(_read_dyadic(source["two_public_prefix_invertibility_probability"])),
            "source_rejection_not_free_and_sq_oracle_not_a_sample_factory": True,
            "max_orbits_distinguished_from_reference_per_query_hex": hex(distinguishable),
            "adversarial_valid_sq_oracle_uniform_orbit_success_upper_bound": exact(success),
            "public_source": "native_n_by_3n_pairs_conditioned_on_both_first_n_blocks_invertible",
            "secret_prior": "uniform_nonzero_parity_packet_residues_modulo_negation",
            "sq_queries_bounded_in_minus_one_to_one": True,
            "query_evaluation_time_unrestricted": True,
            "raw_sample_algorithms_covered": False,
            "joint_multisample_queries_covered": False,
            "chosen_source_labels_covered": False,
            "different_quantum_measurements_covered": False,
            "classical_hardness_or_quantum_speedup_claim": False}


def noisy_transcript_certificate(n, modulus, bit_flip_probability, supplied_pair_attempts):
    if modulus < 8 or modulus & (modulus - 1) or supplied_pair_attempts < 1:
        raise ValueError("power-of-two modulus>=8 and positive supplied-pair budget required")
    source = systematic_noisy_source_mean(n, bit_flip_probability)
    Q = modulus // 2
    d = _rational_read(source["joint_source_likelihood_chi_squared_to_uniform_reference"])
    prefix = _rational_read(source["two_public_prefix_invertibility_probability"])
    exception = Fraction(2, Q)**n
    kl = supplied_pair_attempts * prefix * ((1 - exception) * 2 * d + exception * 2 * n)
    gap = Fraction(1, 100) - Fraction(2, Q**n)
    return {"status": "LOCAL_DERIVATION_REVIEW_PENDING", "dimension": n, "modulus": modulus,
            "supplied_pair_attempts": supplied_pair_attempts,
            "original_phase_states_consumed": 6 * n * supplied_pair_attempts,
            "source": source,
            "uniform_prior_order_at_most_two_exception_mass": exact(exception),
            "transcript_kl_to_secret_independent_reference_bits_upper_bound": exact(kl),
            "uniform_packet_residue_mutual_information_bits_upper_bound": exact(min(Fraction(n * (Q.bit_length() - 1)), kl)),
            "negation_orbit_identification_success_expression": "min(1,2/Q^n+sqrt(KL_bits/2))",
            "orbit_success_below_one_over_100": gap > 0 and kl / 2 < gap * gap,
            "rejected_prefix_attempts_discard_all_quantum_data_and_are_charged": True,
            "all_accepted_noisy_full_v_retained": True,
            "fresh_independent_pairs_and_fixed_declared_measurement_required": True,
            "pairing_chosen_before_higher_labels_required": True,
            "adaptive_label_matching_covered": False,
            "independent_logical_output_noise_not_a_native_reduction_promise": True,
            "detector_only_repetition_or_general_fault_tolerance_covered": False,
            "secret_independent_uniform_noisy_output_reference_available": True,
            "additional_quantum_verification_or_memory_covered": False,
            "arbitrary_decoders_or_other_measurements_closed": False,
            "independent_theorem_review": False, "speedup_claim_allowed": False}


def _character_cross_control(left, right, s, t, u):
    """Exact four-index higher-label character contraction, no rank formula."""
    k, Q = left.retained_qubits, left.modulus // 2
    total, surviving = 0, 0
    for a, b, c in itertools.product(range(1 << k), repeat=3):
        d = a ^ b ^ c
        valid = True
        phase = 0
        for packet, offset in ((left, 0), (right, u)):
            assignments = [packet.assignment(z ^ offset) for z in (a, b, c, d)]
            for i in range(packet.input_qubits):
                dx, dy = assignments[0][i] - assignments[1][i], assignments[2][i] - assignments[3][i]
                if any((x * dx + y * dy) % Q for x, y in zip(s, t)):
                    valid = False
                    break
            residual = [packet.residual(z ^ offset) for z in (a, b, c, d)]
            phase += sum(x * (ra - rb) + y * (rc - rd) for x, y, ra, rb, rc, rd in zip(s, t, *residual))
        if valid:
            # All surviving terms here are real roots, including order-two signs.
            assert phase % Q in (0, Q // 2)
            total += 1 if phase % Q == 0 else -1
            surviving += 1
    return Fraction(total, 1 << (2 * k)), surviving


def character_kernel_controls():
    records = []
    low = ([[1, 1, 0], [0, 1, 1]], [[1, 1, 0], [0, 0, 1]])
    for q in (8, 16, 128):
        Q = q // 2
        packets = [compile_packet(A, q, 1) for A in low]
        secrets = list(itertools.product(range(Q), repeat=2)) if q == 8 else [
            (0, 0), (1, 0), (3, 0), (Q - 1, 0), (2, 0), (Q - 2, 0),
            (Q // 2, 0), (0, Q // 2), (1, 1), (1, 3)]
        for s, t, u in itertools.product(secrets, secrets, range(2)):
            direct, surviving = _character_cross_control(*packets, s, t, u)
            predicted = cross_secret_kernel(*packets, s, t)
            assert direct == _rational_read(predicted["source_mean_relative_cross_collision"])
            records.append({"modulus": q, "secret_s": s, "secret_t": t, "xor_outcome": u,
                            "mean_relative_cross_collision": exact(direct),
                            "surviving_source_character_terms": surviving,
                            "character_terms_tested": 8})
    return {"low_left": low[0], "low_right": low[1], "initial_syndrome": 1,
            "records": records, "finite_controls_not_a_source_success_sweep": True}


def _noisy_physical_source_control():
    epsilon, totals = Fraction(1, 8), {}
    k, q = 1, 8
    secrets = [(s,) for s in range(4)]
    for s, t in itertools.product(secrets, repeat=2):
        totals[s, t] = Fraction(0)
    for high in itertools.product(range(4), repeat=4):
        packets = [compile_packet([[1 + 2 * high[2 * side + i] for i in range(2)]], q, side)
                   for side in range(2)]
        observed = {}
        for s in secrets:
            p = _physical_full_probabilities(*packets, s, 1)
            observed[s] = [(1 - epsilon) * p[v] + epsilon * p[v ^ 1] for v in range(2)]
        for s, t in totals:
            totals[s, t] += 2 * sum(a * b for a, b in zip(observed[s], observed[t]))
    base = [compile_packet([[1, 1]], q, side) for side in range(2)]
    rows = []
    for (s, t), total in totals.items():
        expected = cross_secret_kernel(*base, s, t, bit_flip_probability=epsilon)
        assert total / 256 == _rational_read(expected["source_mean_relative_cross_collision"])
        rows.append({"secret_s": s, "secret_t": t, "mean_relative_cross_collision": exact(total / 256)})
    return {"complete_higher_label_tables": 256, "logical_width": k,
            "independent_output_flip_probability": exact(epsilon), "records": rows,
            "all_source_tables_included": True}


def _weighted_systematic_control():
    epsilon, t = Fraction(1, 8), Fraction(9, 16)
    total = Fraction(0)
    for a, b in itertools.product(range(4), repeat=2):
        rows = ([a, 1, 2], [b, 1, 2])
        D = Fraction(0)
        for h, j in itertools.product(range(4), repeat=2):
            physical = [[sum(((r & z).bit_count() & 1) << i for i, r in enumerate(rs)) for z in (h, j)] for rs in rows]
            if all(not (x & y) for x, y in physical):
                D += t**h.bit_count()
        total += D / 4
    expected = systematic_noisy_source_mean(1, epsilon)
    assert total / 16 == _rational_read(expected["conditional_mean_relative_full_collision"])
    return {"complete_systematic_pair_tables": 16, "weighted_mean_relative_collision": exact(total / 16)}


def fixed_chart_order_two_alias_control():
    low = ([[1, 0, 1, 1], [0, 1, 1, 1]], [[1, 0, 0, 0], [0, 1, 0, 0]])
    packets = [compile_packet(A, 8) for A in low]
    s, t = [2, 0], [0, 2]
    for a, b in ((s, s), (s, t), (t, t)):
        assert _rational_read(cross_secret_kernel(*packets, a, b)["centered_likelihood_inner_product"]) == 0
    checks = 0
    for seed in range(4):
        changed = [compile_packet([[b + 2 * ((seed + 3 * side + l + i) % 4) for i, b in enumerate(row)]
                                   for l, row in enumerate(A)], 8, side) for side, A in enumerate(low)]
        for u in range(4):
            assert _physical_full_probabilities(*changed, s, u) == [Fraction(1, 4)] * 4
            assert _physical_full_probabilities(*changed, t, u) == [Fraction(1, 4)] * 4
            checks += 2
    return {"low_left": low[0], "low_right": low[1], "secret_s": s, "secret_t": t,
            "not_same_negation_orbit": True, "both_combined_binary_quadratic_ranks": [2, 2],
            "both_centered_likelihood_squared_norms": exact(0),
            "full_laws_uniform_for_every_higher_label_table": True,
            "full_rank_quadratic_derivation_not_exhaustive_high_source": True,
            "bounded_physical_full_law_checks": checks,
            "order_at_least_four_identifiability_statement_not_affected": True}


def run_controls():
    return {"status": "LOCAL_DERIVATION_REVIEW_PENDING", "character_kernels": character_kernel_controls(),
            "complete_noisy_physical_source": _noisy_physical_source_control(),
            "weighted_systematic_source": _weighted_systematic_control(),
            "fixed_chart_order_two_alias": fixed_chart_order_two_alias_control(),
            "detector_repetition_countercontrol": detector_repetition_countercontrol(Fraction(1, 8), 7, 256),
            "sq_scaling": [statistical_query_certificate(n, max(8, 1 << (n - 1).bit_length()), n * n, Fraction(1, n * n))
                           for n in (4, 8, 16, 32, 64, 128)],
            "readout_noise_scaling": [noisy_transcript_certificate(n, max(8, 1 << (n - 1).bit_length()), Fraction(1, 8), n * n)
                                      for n in (16, 32, 64, 128, 256, 512)],
            "claim_gate": {"different_negation_orbits_are_centered_l2_orthogonal": True,
                           "l2_geometry_proves_polynomial_sample_learning": False,
                           "sq_obstruction_closes_raw_sample_learning": False,
                           "noise_model_is_native_phase_error_model": False,
                           "noisy_transcript_uniformization_closes_clean_collective_readout": False,
                           "unknown_secret_decoder": False, "independent_theorem_review": False,
                           "speedup_claim_allowed": False},
            "dependency_sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                                  for p in (Path(__file__), ROOT / "theorems/dcp_carry_packets.py",
                                            ROOT / "theorems/dcp_full_bell_source_moments.py")}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--save", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.save:
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"status": report["status"], "character_kernels": len(report["character_kernels"]["records"]),
                      "claim_gate": report["claim_gate"]}, indent=2))


if __name__ == "__main__":
    main()
