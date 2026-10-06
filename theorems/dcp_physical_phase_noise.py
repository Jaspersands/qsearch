"""Physical Z-mask transport and source-aware Bell dephasing certificates.

LOCAL DERIVATION / REVIEW PENDING. IID phase flips are a declared stress model,
not Regev's arbitrary basis-contamination promise or a general no-go theorem.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

from dcp_carry_packets import binary_rank, compile_packet
from dcp_bell_inference_kernel import exact
from dcp_full_bell_source_moments import _physical_full_probabilities, systematic_source_mean

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/dcp_physical_phase_noise.json"


def read(value):
    return Fraction(value["sign"] * int(value["numerator_hex"], 16), int(value["denominator_hex"], 16))


def _rate(value):
    value = Fraction(value)
    if not 0 <= value <= Fraction(1, 2):
        raise ValueError("dephasing flip rate must lie in [0,1/2]")
    return value


@dataclass(frozen=True)
class IndependentPhysicalZ:
    left_rates: tuple[Fraction, ...]
    right_rates: tuple[Fraction, ...]

    def __post_init__(self):
        if not self.left_rates or not self.right_rates:
            raise ValueError("nonempty physical error-rate vectors required")
        object.__setattr__(self, "left_rates", tuple(_rate(x) for x in self.left_rates))
        object.__setattr__(self, "right_rates", tuple(_rate(x) for x in self.right_rates))

    @classmethod
    def iid(cls, left, right, rate):
        return cls((_rate(rate),) * left.input_qubits, (_rate(rate),) * right.input_qubits)

    def validate(self, left, right):
        if len(self.left_rates) != left.input_qubits or len(self.right_rates) != right.input_qubits:
            raise ValueError("physical rate-vector width mismatch")
        if left.modulus != right.modulus or left.retained_qubits != right.retained_qubits or left.dimension != right.dimension:
            raise ValueError("equal packet modulus, dimension and logical width required")

    def fourier(self, left, right, logical_mask):
        self.validate(left, right)
        if not 0 <= logical_mask < 1 << left.retained_qubits:
            raise ValueError("logical Fourier mask out of range")
        value = Fraction(1)
        for packet, rates in ((left, self.left_rates), (right, self.right_rates)):
            for row, p in zip(packet.kernel_rows, rates):
                if (row & logical_mask).bit_count() & 1:
                    value *= 1 - 2 * p
        return value


@dataclass(frozen=True)
class SparsePhysicalZ:
    """Explicit classical JOINT mask law, possibly correlated across packets."""
    entries: tuple[tuple[int, int, Fraction], ...]

    def __post_init__(self):
        entries = tuple((int(a), int(b), Fraction(p)) for a, b, p in self.entries)
        if not entries or any(a < 0 or b < 0 or p < 0 for a, b, p in entries) or sum(p for _, _, p in entries) != 1:
            raise ValueError("normalized nonnegative finite physical mask law required")
        object.__setattr__(self, "entries", entries)

    def validate(self, left, right):
        if left.modulus != right.modulus or left.retained_qubits != right.retained_qubits or left.dimension != right.dimension:
            raise ValueError("equal packet modulus, dimension and logical width required")
        if any(a >= 1 << left.input_qubits or b >= 1 << right.input_qubits for a, b, _ in self.entries):
            raise ValueError("physical mask out of range")

    def logical_distribution(self, left, right):
        self.validate(left, right)
        out = {}
        for a, b, p in self.entries:
            eta = left.logical_z_mask(a) ^ right.logical_z_mask(b)
            out[eta] = out.get(eta, Fraction(0)) + p
        return out

    def fourier(self, left, right, h):
        if not 0 <= h < 1 << left.retained_qubits:
            raise ValueError("logical Fourier mask out of range")
        return sum(p * (-1 if (eta & h).bit_count() & 1 else 1)
                   for eta, p in self.logical_distribution(left, right).items())


def _physical_mask_probability(mask, rates):
    value = Fraction(1)
    for i, p in enumerate(rates):
        value *= p if mask >> i & 1 else 1 - p
    return value


def physical_error_pushforward(left, right, noise, *, physical_enumeration_cap=16):
    """Bounded exact calibration of eta=K1^T e1+K2^T e2, not IID logical bits."""
    noise.validate(left, right)
    m = left.input_qubits + right.input_qubits
    if m > physical_enumeration_cap:
        raise ValueError("physical mask enumeration is exponential; cap exceeded")
    k, distribution = left.retained_qubits, [Fraction(0)] * (1 << left.retained_qubits)
    for a, b in itertools.product(range(1 << left.input_qubits), range(1 << right.input_qubits)):
        eta = left.logical_z_mask(a) ^ right.logical_z_mask(b)
        distribution[eta] += _physical_mask_probability(a, noise.left_rates) * _physical_mask_probability(b, noise.right_rates)
    assert sum(distribution) == 1
    for h in range(1 << k):
        direct = sum(p * (-1 if (eta & h).bit_count() & 1 else 1) for eta, p in enumerate(distribution))
        assert direct == noise.fourier(left, right, h)
    return tuple(distribution)


def fixed_chart_physical_collision(left, right, noise, *, mask_enumeration_cap=14):
    noise.validate(left, right)
    if left.modulus < 8:
        raise ValueError("effective-order>=4 source identity requires modulus>=8")
    k = left.retained_qubits
    if k > mask_enumeration_cap:
        raise ValueError("weighted rank-sum enumeration is exponential; cap exceeded")
    value = Fraction(0)
    for h in range(1 << k):
        rows = [r for r in left.kernel_rows + right.kernel_rows if (r & h).bit_count() & 1]
        value += noise.fourier(left, right, h)**2 * Fraction(1, 1 << binary_rank(rows, k))
    return {"status": "LOCAL_DERIVATION_REVIEW_PENDING", "modulus": left.modulus, "logical_width": k,
            "high_source_mean_relative_full_collision": exact(value),
            "source_centered_likelihood_squared_norm": exact(value - 1),
            "physical_error_law_secret_and_higher_label_independence_assumed": True,
            "physical_mask_bits_independent": isinstance(noise, IndependentPhysicalZ),
            "error_lineage_independence_programmatically_verified": False,
            "effective_secret_character_order_at_least_four_required": True,
            "conditions_on_public_low_charts_and_syndromes": True,
            "noise_source_model": "independent_physical_Z" if isinstance(noise, IndependentPhysicalZ) else "explicit_correlated_physical_Z_law",
            "logical_errors_assumed_independent": False,
            "public_masks_enumerated": 1 << k, "mask_enumeration_is_polynomial": False,
            "general_noise_or_all_measurements_covered": False, "speedup_claim_allowed": False}


def native_physical_source_mean(n, phase_flip_probability):
    if n < 1:
        raise ValueError("positive vector dimension required")
    epsilon = _rate(phase_flip_probability)
    a, k, N = (1 - 2 * epsilon)**2, 2 * n, 1 << (2 * n)
    pivot_single = Fraction(1 + a, 2)
    pivot_pair = Fraction(2 + a, 4)
    free_single = (1 + a * a)**k
    free_pair = (2 + a * a)**k
    value = (N + (free_single - 1) * pivot_single**k
             + (free_pair - N - free_single + 1) * pivot_pair**k) / N
    assert value >= 1
    prefix = systematic_source_mean(n)["two_public_prefix_invertibility_probability"]
    prefix = Fraction(prefix["sign"] * int(prefix["numerator_hex"], 16), 1 << prefix["denominator_binary_exponent"])
    # The native single-packet all-zero verifier is complete only if eta=0.
    zero_accept = (1 - epsilon)**(3 * n) + Fraction(1, N) * (1 - (1 - epsilon)**n)
    leading = (2 + a * a) * (2 + a) / 8
    return {"status": "LOCAL_DERIVATION_REVIEW_PENDING", "dimension": n, "logical_width": k,
            "physical_phase_flip_probability": exact(epsilon), "physical_squared_contrast": exact(a),
            "conditional_mean_relative_full_collision": exact(value),
            "joint_source_chi_squared_to_uniform_output": exact(value - 1),
            "two_public_prefix_invertibility_probability": exact(prefix),
            "nonzero_pair_leading_base_per_logical_qubit": exact(leading),
            "single_member_leading_base_per_logical_qubit": exact((1 + a * a) * (1 + a) / 4),
            "exponential_uniformization_regime": leading < 1,
            "single_packet_known_correct_residue_all_zero_mean_acceptance": exact(zero_accept),
            "single_packet_wrong_committed_residue_high_source_mean_acceptance": exact(Fraction(1, N)),
            "correct_residue_all_zero_verifier_noiseless_completeness_no_longer_valid": epsilon > 0,
            "source": "native_n_by_3n_conditioned_on_first_n_columns_invertible",
            "phase_error_source_model_independence_is_an_assumption": True,
            "regev_basis_contamination_promise_covered": False,
            "all_other_quantum_decoders_closed": False, "speedup_claim_allowed": False}


def physical_transcript_information_bound(n, q, rate, supplied_pair_attempts):
    if q < 8 or q & (q - 1) or supplied_pair_attempts < 1:
        raise ValueError("power-of-two modulus>=8 and positive supplied-pair budget required")
    source = native_physical_source_mean(n, rate)
    Q, k = q // 2, 2 * n
    d = read(source["joint_source_chi_squared_to_uniform_output"])
    prefix = read(source["two_public_prefix_invertibility_probability"])
    rho = Fraction(2, Q)**n
    kl = supplied_pair_attempts * prefix * ((1 - rho) * 2 * d + rho * k)
    gap = Fraction(1, 100) - Fraction(2, Q**n)
    return {"status": "LOCAL_DERIVATION_REVIEW_PENDING", "modulus": q,
            "source": source, "supplied_pair_attempts": supplied_pair_attempts,
            "original_phase_states_consumed": 6 * n * supplied_pair_attempts,
            "full_prior_order_at_most_two_exception_mass": exact(rho),
            "transcript_kl_to_secret_independent_reference_bits_upper_bound": exact(kl),
            "negation_orbit_success_expression": "min(1,2/(q/2)^n+sqrt(KL_bits/2))",
            "orbit_success_below_one_over_100": gap > 0 and kl / 2 < gap * gap,
            "all_noisy_full_output_bits_retained": True,
            "fixed_independent_pairing_before_higher_labels_required": True,
            "discarded_prefix_failures_charged": True,
            "independent_input_Z_errors_not_a_verified_reduction_promise": True,
            "secret_dependent_or_label_dependent_error_laws_covered": False,
            "quantum_memory_encoding_or_other_measurements_covered": False,
            "independent_theorem_review": False, "speedup_claim_allowed": False}


def _correlation_control():
    left = compile_packet([[1, 1, 1]], 8)
    right = compile_packet([[1, 1, 0]], 8)
    noise = IndependentPhysicalZ.iid(left, right, Fraction(1, 16))
    distribution = physical_error_pushforward(left, right, noise)
    p0 = sum(p for eta, p in enumerate(distribution) if eta & 1)
    p1 = sum(p for eta, p in enumerate(distribution) if eta >> 1 & 1)
    joint = distribution[3]
    assert joint != p0 * p1
    return {"left_low": left.labels, "right_low": right.labels,
            "rate": exact(Fraction(1, 16)), "logical_error_distribution": [exact(p) for p in distribution],
            "logical_bit_error_marginals": [exact(p0), exact(p1)],
            "joint_two_bit_error": exact(joint), "product_of_bit_error_marginals": exact(p0 * p1),
            "iid_logical_noise_assumption_falsified": True,
            "physical_error_masks_enumerated": 64}


def _full_physical_source_control():
    low = ([[1, 1]], [[1, 1]])
    base = [compile_packet(A, 8, side) for side, A in enumerate(low)]
    noise = IndependentPhysicalZ.iid(*base, Fraction(1, 16))
    law = physical_error_pushforward(*base, noise)
    total = Fraction(0)
    for high in itertools.product(range(4), repeat=4):
        packets = [compile_packet([[1 + 2 * high[side * 2 + i] for i in range(2)]], 8, side) for side in range(2)]
        p = _physical_full_probabilities(*packets, [1], 1)
        observed = [sum(law[e] * p[v ^ e] for e in range(2)) for v in range(2)]
        total += 2 * sum(x * x for x in observed)
    cert = fixed_chart_physical_collision(*base, noise)
    assert total / 256 == read(cert["high_source_mean_relative_full_collision"])
    return {"complete_higher_label_tables": 256, "left_low": low[0], "right_low": low[1],
            "physical_rate": exact(Fraction(1, 16)), "source_mean_relative_collision": exact(total / 256),
            "certificate": cert}


def _systematic_low_controls():
    records = []
    for epsilon in (Fraction(0), Fraction(1, 32), Fraction(1, 16), Fraction(1, 2)):
        a, total, packet_zero = (1 - 2 * epsilon)**2, Fraction(0), Fraction(0)
        for x, y in itertools.product(range(4), repeat=2):
            rows = ([x, 1, 2], [y, 1, 2])
            weighted = Fraction(0)
            for h, j in itertools.product(range(4), repeat=2):
                physical = [sum(((r & h).bit_count() & 1) << i for i, r in enumerate(rs)) for rs in rows]
                directions = [sum(((r & j).bit_count() & 1) << i for i, r in enumerate(rs)) for rs in rows]
                if all(not (p & d) for p, d in zip(physical, directions)):
                    weighted += a**sum(p.bit_count() for p in physical)
            total += weighted / 4
        for x in range(4):
            packet = compile_packet([[1, x & 1, x >> 1]], 8)
            for e in range(8):
                if packet.logical_z_mask(e) == 0:
                    packet_zero += _physical_mask_probability(e, (epsilon,) * 3)
        cert = native_physical_source_mean(1, epsilon)
        assert total / 16 == read(cert["conditional_mean_relative_full_collision"])
        assert packet_zero / 4 == read(cert["single_packet_known_correct_residue_all_zero_mean_acceptance"])
        records.append({"physical_rate": exact(epsilon), "complete_systematic_pair_tables": 16,
                        "source_mean_relative_collision": exact(total / 16),
                        "complete_single_packet_source_masks": 32,
                        "known_residue_all_zero_acceptance": exact(packet_zero / 4)})
    return records


def _correlated_cancellation_control():
    packet = compile_packet([[1, 1, 1]], 8)
    law = SparsePhysicalZ(((0, 0, Fraction(1, 2)), (1, 1, Fraction(1, 2))))
    assert law.logical_distribution(packet, packet) == {0: Fraction(1)}
    assert all(law.fourier(packet, packet, h) == 1 for h in range(4))
    clean = fixed_chart_physical_collision(packet, packet, IndependentPhysicalZ.iid(packet, packet, 0))
    correlated = fixed_chart_physical_collision(packet, packet, law)
    assert clean["high_source_mean_relative_full_collision"] == correlated["high_source_mean_relative_full_collision"]
    return {"low_labels": packet.labels,
            "explicit_joint_physical_mask_law": [{"left_mask_hex": hex(a), "right_mask_hex": hex(b), "probability": exact(p)}
                                                 for a, b, p in law.entries],
            "each_packet_first_physical_bit_flip_marginal": exact(Fraction(1, 2)),
            "logical_error_distribution": {"0x0": exact(1)},
            "shared_correlated_Z_errors_cancel_in_bell_readout": True,
            "native_iid_source_uniformization_formula_does_not_apply": True,
            "correlated_certificate": correlated}


def run_controls():
    return {"status": "LOCAL_DERIVATION_REVIEW_PENDING", "correlation_control": _correlation_control(),
            "complete_noisy_full_source": _full_physical_source_control(),
            "systematic_low_controls": _systematic_low_controls(),
            "correlated_cancellation_countercontrol": _correlated_cancellation_control(),
            "physical_noise_scaling": [physical_transcript_information_bound(n, max(8, 1 << (n - 1).bit_length()),
                                                                           Fraction(1, 16), n * n)
                                       for n in (16, 32, 64, 128, 256)],
            "vanishing_noise_controls": [native_physical_source_mean(n, Fraction(1, n * n)) for n in (8, 16, 32, 64)],
            "claim_gate": {"physical_to_logical_correlation_accounted": True,
                           "native_reduction_error_law_identified": False,
                           "regev_basis_contamination_is_iid_dephasing": False,
                           "constant_noise_gate_closes_vanishing_noise": False,
                           "noisy_candidate_verifier_noiseless_completeness_preserved": False,
                           "other_collective_or_encoded_measurements_closed": False,
                           "independent_theorem_review": False, "speedup_claim_allowed": False},
            "dependency_sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                                  for p in (Path(__file__), ROOT / "theorems/dcp_carry_packets.py",
                                            ROOT / "theorems/dcp_bell_inference_kernel.py",
                                            ROOT / "theorems/dcp_full_bell_source_moments.py")}}


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
