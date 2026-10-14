"""Paid, constant-gap syndrome dilation of the actual native word map.

Its label-only Fourier-sector ancillas can give noncommuting word effects,
but do not increase uniform-secret average overlap. All readout mass remains.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
from itertools import product
import json
from math import isqrt
from pathlib import Path

import numpy as np

from native_basis_lottery import BasisBank, original_bank
from native_full_root_slice import source_data
from native_small_multiple_completion import _rational
from native_word_spectral_filter_audit import finite_control
from native_word_span_decision import root_polynomial
from ternary_measured_lattice_decoder import exact_json, integer
from ternary_noise_degradation import NoisyLinearRecord

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT / "research/NATIVE_SYNDROME_DILATION.md"
REPORT = ROOT / "research/reductions/native_syndrome_dilation.json"


class SyndromeDilation:
    """Finite permutation/mixer reference, never a dense joint Hamiltonian."""

    def __init__(self, records, mask, max_joint_cells=8192):
        self.raw = original_bank(records)
        self.q, self.n = self.raw[0].modulus, len(self.raw[0].label)
        integer(max_joint_cells, "positive whole joint-state cap", 1)
        if len(self.raw) % 2:
            raise ValueError("complete actual original pairs required")
        self.M, self.D, self.N = len(self.raw) // 2, 3 ** (len(self.raw) // 2), self.q ** self.n
        if self.D > 256 or self.N > 81 or self.D * self.N > max_joint_cells:
            raise ValueError("whole native word/syndrome reference cap exceeded")
        self.base = finite_control(self.raw, mask, (("GEOMETRIC", 1),))
        self.rows = self.base["actual_native_word_rows"]
        self.frequencies = tuple(product(range(self.q), repeat=self.n))
        index = {v: j for j, v in enumerate(self.frequencies)}
        self.shift = np.asarray([[index[tuple((x + a) % self.q for x, a in zip(z, row["frequency"]))]
                                  for z in self.frequencies] for row in self.rows])
        self.phi = np.exp(2j * np.pi * np.asarray([row["frequency"] for row in self.rows]) @ np.asarray(self.frequencies).T / self.q) / np.sqrt(self.D)
        self.fourier_work = np.exp(2j * np.pi * np.asarray(self.frequencies) @ np.asarray(self.frequencies).T / self.q) / np.sqrt(self.N)
        self.psi = np.exp(2j * np.pi * np.asarray([row["known_phase"] for row in self.rows]) / self.q) / np.sqrt(self.D)

    def _joint(self, state):
        state = np.asarray(state, dtype=complex)
        if state.shape != (self.D, self.N) or not np.isfinite(state).all():
            raise ValueError("complete finite joint amplitude array required")
        return state

    def translate(self, state, inverse=False):
        state = self._joint(state)
        if inverse:
            return np.take_along_axis(state, self.shift, axis=1)
        out = np.empty_like(state)
        np.put_along_axis(out, self.shift, state, axis=1)
        return out

    def ground(self, state):
        shifted = self.translate(state)
        projected = np.broadcast_to(shifted.mean(axis=0), shifted.shape).copy()
        return self.translate(projected, inverse=True)

    def hamiltonian(self, state):
        shifted = self.translate(state).reshape((3,) * self.M + (self.N,))
        result = np.zeros_like(shifted)
        for j in range(self.M):
            result += shifted - shifted.mean(axis=j, keepdims=True)
        return self.translate(result.reshape(self.D, self.N), inverse=True)

    def readout(self, state):
        """Actual T_f, word F3 inverse, and syndrome Fourier readout, all outputs."""
        shifted = self.translate(state).reshape((3,) * self.M + (self.N,))
        F3dag = np.exp(-2j * np.pi * np.outer(np.arange(3), np.arange(3)) / 3) / np.sqrt(3)
        for j in range(self.M):
            shifted = np.moveaxis(np.tensordot(F3dag, shifted, axes=(1, j)), 0, j)
        return shifted.reshape(self.D, self.N) @ self.fourier_work.conj()

    def public_ancillas(self):
        sector = tuple(sum(row.label[j] for row in self.raw) % self.q for j in range(self.n))
        other = ((sector[0] + 1) % self.q,) + sector[1:]
        i, j = self.frequencies.index(sector), self.frequencies.index(other)
        zero = np.zeros(self.N, dtype=complex)
        zero[0] = 1
        uniform_weights = tuple(Fraction(1, self.N) for _ in range(self.N))
        basis_weights = tuple(Fraction(int(t == i)) for t in range(self.N))
        pair_weights = tuple(Fraction(int(t in (i, j)), 2) for t in range(self.N))
        return (
            ("ZERO_COMPUTATIONAL", zero, uniform_weights, ()),
            ("PUBLIC_FOURIER_SECTOR", self.fourier_work[:, i], basis_weights, (sector,)),
            ("PUBLIC_TWO_FOURIER_SECTORS", (self.fourier_work[:, i] + 1j * self.fourier_work[:, j]) / np.sqrt(2), pair_weights, (sector, other)),
        )

    def compressed_effect(self, weights):
        weights = tuple(map(_rational, weights))
        if len(weights) != self.N or any(w < 0 for w in weights) or sum(weights) != 1:
            raise ValueError("complete public syndrome Fourier probability law required")
        return (self.phi * np.asarray(list(map(float, weights)))) @ self.phi.conj().T

    def exact_overlap(self, weights):
        weights = tuple(map(_rational, weights))
        self.compressed_effect(weights)
        if all(w == Fraction(1, self.N) for w in weights):
            return self.base["spectral_filter_controls"][0]["exact_source_acceptance_root_polynomial"]
        coefficients = [Fraction(0)] * self.q
        for sector, weight in zip(self.frequencies, weights):
            if not weight:
                continue
            phases = tuple((row["known_phase"] - sum(a * s for a, s in zip(row["frequency"], sector))) % self.q for row in self.rows)
            counts = Counter(phases)
            for a, count_a in counts.items():
                for b, count_b in counts.items():
                    coefficients[(b - a) % self.q] += weight * count_a * count_b / (self.D * self.D)
        return root_polynomial(coefficients, self.q)

    def classical_readout_law(self, weights):
        """Exact closed-form law evaluated numerically, not a certified coin sampler."""
        phases = self.base["actual_native_word_rows"]
        out = np.zeros((self.D, self.N))
        for t, (sector, weight) in enumerate(zip(self.frequencies, weights)):
            if not weight:
                continue
            local = []
            for j in range(self.M):
                a, c = self.raw[2 * j:2 * j + 2]
                y1 = (a.value + sum(x * z for x, z in zip(a.label, self.base["known_mask"]))) % self.q
                y2 = (c.value + sum(x * z for x, z in zip(c.label, self.base["known_mask"]))) % self.q
                labels = (a.label, tuple((v - u) % self.q for u, v in zip(a.label, c.label)), tuple(-v % self.q for v in c.label))
                eta = (y1, (y2 - y1) % self.q, -y2 % self.q)
                numerators = tuple((y - sum(x * s for x, s in zip(label, sector))) % self.q for label, y in zip(labels, eta))
                local.append(tuple(abs(sum(np.exp(2j * np.pi * (value - self.q // 3 * ell * u) / self.q)
                                               for u, value in enumerate(numerators)) / 3) ** 2 for ell in range(3)))
            for w, row in enumerate(phases):
                p = float(weight)
                for j, ell in enumerate(row["word"]):
                    p *= local[j][ell]
                out[w, t] = p
        return out


def sector_noncommutation_witness(base, sector):
    rows, D = base["actual_native_word_rows"], base["word_dimension"]
    q = base["original_records"][0]["modulus"]
    counts = Counter(tuple(r["frequency"]) for r in rows)
    for i, a in enumerate(rows):
        for j, b in enumerate(rows):
            ca, cb = counts[tuple(a["frequency"])], counts[tuple(b["frequency"])]
            if ca != cb:
                return {"word_indices": (i, j), "commutator_root_of_unity_prefactor": str(Fraction(ca - cb, D * D)),
                        "commutator_phase_exponent": sum(t * (x - y) for t, x, y in zip(sector, a["frequency"], b["frequency"])) % q,
                        "nonzero_entry_certified_from_counts_and_root_of_unity": True}
    return None


def control(args):
    raw, mask, truth, errors = source_data(*args)
    work = SyndromeDilation(raw, mask)
    error_phases = tuple(sum(b * e for j, t in enumerate(row["word"])
                             for b, e in zip(((1, 0), (-1, 1), (0, -1))[t], errors[2 * j:2 * j + 2])) % work.q for row in work.rows)
    noisy_family = np.exp(2j * np.pi * np.asarray(error_phases)[:, None] / work.q) * work.phi
    raw_mean = work.base["spectral_filter_controls"][0]["diagnostic_source_acceptance_probability"]
    records = []
    K = np.asarray([[int(a["frequency"] == b["frequency"]) / work.D for b in work.rows] for a in work.rows])
    for kind, ancilla, weights, sectors in work.public_ancillas():
        state = np.outer(work.psi, ancilla)
        projected = work.ground(state)
        mass = float(np.vdot(projected, projected).real)
        E = work.compressed_effect(weights)
        amplitudes = work.readout(state)
        classical = work.classical_readout_law(weights)
        secret_overlaps = np.sum(np.asarray(list(map(float, weights)))[:, None] * abs(work.phi.conj().T @ noisy_family) ** 2, axis=0)
        residual = float(np.linalg.norm(work.hamiltonian(projected)))
        if abs(float(secret_overlaps.mean()) - raw_mean) > 1e-9 or abs(float(np.vdot(work.psi, E @ work.psi).real) - mass) > 1e-9 or residual > 1e-9 or np.max(abs(abs(amplitudes) ** 2 - classical)) > 1e-9:
            raise ArithmeticError("literal dilation, source average, or full classical readout law disagrees")
        records.append({
            "ancilla_kind": kind, "public_sector_parameters": sectors,
            "exact_syndrome_Fourier_weights": tuple(str(w) for w in weights),
            "exact_original_data_ground_probability_root_polynomial": work.exact_overlap(weights),
            "diagnostic_ground_probability": mass, "diagnostic_entire_readout_mass": float(np.sum(abs(amplitudes) ** 2)),
            "diagnostic_ground_Hamiltonian_residual": residual,
            "diagnostic_complete_measured_law_max_error_against_classical": float(np.max(abs(abs(amplitudes) ** 2 - classical))),
            "diagnostic_compressed_effect_commutator_norm": float(np.linalg.norm(K @ E - E @ K)),
            "exact_noncommutation_witness": sector_noncommutation_witness(work.base, sectors[0]) if kind == "PUBLIC_FOURIER_SECTOR" else None,
            "complete_uniform_secret_sweep_ground_probabilities": tuple(float(p) for p in secret_overlaps),
            "diagnostic_uniform_secret_mean": float(secret_overlaps.mean()),
            "exact_uniform_secret_mean_root_polynomial": work.base["spectral_filter_controls"][0]["exact_source_acceptance_root_polynomial"],
            "known_rank_one_driver_interpolation": {
                "path": "(1-lambda)*(I-|initial><initial|)+lambda*(I-P_ground)",
                "minimum_active_two_dimensional_gap_squared_root_polynomial": work.exact_overlap(weights),
                "diagnostic_minimum_active_gap": float(np.sqrt(max(0, mass))),
                "minimum_active_gap_location": "1/2",
                "other_target_ground_directions": work.N - 1,
                "other_target_ground_directions_energy": "1-lambda",
                "full_lowest_level_gap_is_same_as_active_gap": False,
                "constant_endpoint_band_gap_removes_this_path_bottleneck": False,
                "general_different_driver_or_path_lower_bound_claimed": False,
            },
            "exact_IID_uniform_original_value_null_ground_probability": str(Fraction(1, work.D)),
            "original_responses_enter_ancilla_preparation": False,
            "normalized_fibre_access_supplied": False,
            "all_failure_readout_mass_kept": True,
        })
    return {"native_source_reference": work.base, "truth_ONLY_FOR_SOURCE_SWEEP_CALIBRATION": {"masked_secret": truth, "original_errors": errors},
            "joint_word_syndrome_dimension": work.D * work.N, "expanded_ground_rank": work.N,
            "exact_unnormalized_Hamiltonian_gap": "1", "exact_Hamiltonian_norm": work.M,
            "exact_norm1_Hamiltonian_gap": str(Fraction(1, work.M)),
            "public_ancilla_experiments": tuple(records),
            "dense_joint_Hamiltonian_or_joint_projector_allocated": False,
            "physical_gate_and_precision_certificates_supplied": False}


def decode_noiseless(records):
    """Response-dependent countercontrol uses only public records, not truth."""
    raw = original_bank(records)
    bank = BasisBank(raw)
    q, n = raw[0].modulus, len(raw[0].label)
    for j in range(bank.planned):
        if bank.rank(j) != n:
            continue
        X = bank.inverse(j, q)["inverse"]
        values = tuple(r.value for r in bank.block(j))
        candidate = tuple(sum(a * y for a, y in zip(row, values)) % q for row in X)
        if all((sum(a * s for a, s in zip(r.label, candidate)) - r.value) % q == 0 for r in raw):
            return {"candidate_secret": candidate, "public_label_rank_calls": bank.rank_calls,
                    "public_ring_inverse_calls": bank.inverse_calls, "original_equations_checked": len(raw),
                    "truth_supplied_to_decoder": False}
    return {"candidate_secret": None, "public_label_rank_calls": bank.rank_calls,
            "public_ring_inverse_calls": bank.inverse_calls, "original_equations_checked": 0,
            "truth_supplied_to_decoder": False}


def response_mask_countercontrol():
    raw, _, _, _ = source_data(1, 2, 4, False, 99002)
    decoder = decode_noiseless(raw)
    s = decoder["candidate_secret"]
    if s is None:
        raise ArithmeticError("noiseless same-source public decoder countercontrol failed")
    q = raw[0].modulus
    mask = tuple(-x % q for x in s)
    work = SyndromeDilation(raw, mask)
    ancilla = work.fourier_work[:, 0]
    projected = work.ground(np.outer(work.psi, ancilla))
    return {"original_records": tuple(r.public() for r in raw), "public_noiseless_decoder": decoder,
            "original_response_dependent_known_mask": mask,
            "label_only_work_ancilla_sector": (0,) * work.n,
            "diagnostic_ground_probability_after_paid_classical_mask": float(np.vdot(projected, projected).real),
            "word_phase_preparation_is_uniform_AFTER_paid_classical_mask": bool(np.max(abs(work.psi - np.ones(work.D) / np.sqrt(work.D))) < 1e-10),
            "general_label_only_ancilla_average_bound_with_response_adaptive_mask_applies": False,
            "zero_computational_work_raw_Gram_mask_invariance_is_not_falsified": True,
            "noiseless_control_is_a_hard_source_or_quantum_speedup": False}


def dilation_ledger(n, r, surplus, target="1/2"):
    for x in (n, r, surplus):
        integer(x, "positive dilation scope", 1)
    if n * r > 16384 or surplus > 128:
        raise ValueError("whole exact exponent certificate cap exceeded")
    target = _rational(target)
    if not 0 < target <= 1:
        raise ValueError("valid desired mean ground acceptance required")
    factor = 1 + Fraction(1, 3 ** surplus)
    primitive_factor = factor / (1 - Fraction(1, 3 ** n))
    squared = target * 3 ** (n * r) / factor
    d = isqrt(squared.numerator // squared.denominator)
    if d * d * squared.denominator < squared.numerator:
        d += 1
    M = n * r + surplus
    return {
        "dimension": n, "root_digits": r, "word_sites": M, "word_surplus": surplus,
        "syndrome_ancilla_trits": n * r, "exact_unnormalized_Hamiltonian_gap": "1",
        "exact_Hamiltonian_norm": M, "exact_norm1_Hamiltonian_gap": str(Fraction(1, M)),
        "word_preparation_uniform_qutrits": M, "known_response_phase_gates": M,
        "known_rank_one_initial_reflection_response_phase_gates": 2 * M,
        "coherent_ground_test_word_Fourier_gates": 2 * M,
        "forward_and_inverse_conditioned_label_shift_terms_upper": 6 * M * n,
        "uniform_secret_mean_ground_acceptance_upper": {"coefficient": str(factor), "base": 3, "exponent": -n * r},
        "uniform_primitive_secret_mean_ground_acceptance_upper": {"coefficient": str(primitive_factor), "base": 3, "exponent": -n * r},
        "target_mean_amplified_ground_mass": str(target), "necessary_standard_amplification_iterations_lower_FULL_uniform_secret": d // 2,
        "arbitrary_label_only_pure_or_mixed_syndrome_ancillas_covered": True,
        "fixed_or_label_only_mask_AND_errors_independent_of_secret_required": True,
        "IID_full_root_original_labels_required_only_for_population_collision_bound": True,
        "uniform_original_value_null_IID_required": True,
        "noncommuting_effects_possible_but_not_sufficient_for_advantage": True,
        "response_dependent_masks_or_work_preprocessing_excluded_by_this_bound": True,
        "inverse_for_arbitrary_mixed_ancilla_preparation_is_not_granted": True,
        "per_secret_success_upper_or_universal_quantum_lower_bound_claimed": False,
        "scalable_quantum_speedup_supplied": False,
    }


def build_report():
    deps = ("native_word_spectral_filter_audit.py", "native_word_span_decision.py", "native_basis_lottery.py",
            "native_full_root_slice.py", "native_small_multiple_completion.py", "ternary_measured_lattice_decoder.py", "ternary_noise_degradation.py")
    return {
        "status": "CONSTRUCTIVE_CONSTANT_GAP_SYNDROME_DILATION_NONCOMMUTING_EFFECTS_NO_OVERLAP_GAIN",
        "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
        "dependency_sha256": {f: hashlib.sha256((ROOT / "theorems" / f).read_bytes()).hexdigest() for f in deps},
        "actual_source_controls": tuple(control(p) for p in ((1, 1, 3, False, 99001), (1, 2, 4, False, 99002), (1, 3, 5, True, 99003), (2, 1, 3, False, 99004))),
        "response_adaptive_mask_countercontrol": response_mask_countercontrol(),
        "scaling_dilation_ledgers": tuple(dilation_ledger(n, n, 12) for n in (8, 32, 64, 128)),
        "matched_classical_readout": "measure public work Fourier sector first, then sample independent original-data one-qutrit F3 outputs; all word and sector outcomes retained",
        "certified_finite_precision_classical_sampler_implemented_here": False,
        "coherent_amplification_or_noncommuting_work_interleaving_classically_simulated": False,
        "accepted_speedup_candidate": False, "new_active_negative_result_created": False,
        "research_decision": "GAP_AND_NONCOMMUTATION_ARE_NOT_ENOUGH_CHARGE_SOURCE_OVERLAP_AND_MEASURED_CLASSICAL_SECTOR_CLOSURE",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write:
        REPORT.write_text(json.dumps(exact_json(report), indent=2) + "\n")
    print(json.dumps({"status": report["status"], "actual_source_controls": len(report["actual_source_controls"]),
        "noncommuting_word_effect_witnesses": sum(e["exact_noncommutation_witness"] is not None for c in report["actual_source_controls"] for e in c["public_ancilla_experiments"]),
        "constant_gap_is_an_efficient_receiver": False, "response_mask_countercontrol_accepts": report["response_adaptive_mask_countercontrol"]["diagnostic_ground_probability_after_paid_classical_mask"]}, indent=2))


if __name__ == "__main__":
    main()
