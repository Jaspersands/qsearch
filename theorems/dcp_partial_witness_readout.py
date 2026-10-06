"""Seeded partial-witness filtering and direct native vector phase readout.

LOCAL DERIVATION / REVIEW PENDING. A conditional reduction, not a fast solver.
No complete fiber permutation, inverse finder or uniform fiber sampler required.
"""

from __future__ import annotations

import argparse
import cmath
import hashlib
import itertools
import json
import math
from dataclasses import dataclass, replace
from fractions import Fraction
from pathlib import Path

from dcp_bell_inference_kernel import exact
from dcp_carry_packets import compile_packet
from dcp_conditional_carry_features import _solve
from dcp_dense_phase_transport import group_index, group_vector
from dcp_terminal_affine_fibers import _positive_integer

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/reductions/dcp_partial_witness_readout.json"


def orient_measured_packet(packet):
    """Keep any measured syndrome; rewrite its residual with signed labels."""
    if len(packet.pivots) != packet.dimension:
        raise ValueError("full binary rank required; rank abort must be charged")
    signed = tuple(tuple((-a if o else a) % packet.modulus for a, o in zip(row, packet.origin))
                   for row in packet.labels)
    return compile_packet(signed, packet.modulus)


def _origin(packet, raw_syndrome):
    n = packet.dimension
    if type(raw_syndrome) is not int or not 0 <= raw_syndrome < 1 << n or len(packet.pivots) != n:
        raise ValueError("full binary rank and valid ORIGINAL-row syndrome required")
    equations = [(sum((row[p] & 1) << j for j, p in enumerate(packet.pivots)), raw_syndrome >> l & 1)
                 for l, row in enumerate(packet.labels)]
    rank, bits = _solve(equations, n)
    assert rank == n and bits is not None
    return sum((bits >> j & 1) << p for j, p in enumerate(packet.pivots))


def target_source_transform(packet, raw_syndrome, target):
    q, n = packet.modulus, packet.dimension
    Q = q // 2
    target = tuple(target)
    if len(target) != n or any(type(t) is not int or not 0 <= t < Q for t in target):
        raise ValueError("canonical effective target vector required")
    origin = _origin(packet, raw_syndrome)
    signed = tuple(tuple((-a if origin >> i & 1 else a) % q for i, a in enumerate(row)) for row in packet.labels)
    shifted = tuple((2 * t - sum(a for i, a in enumerate(row) if origin >> i & 1)) % q
                    for t, row in zip(target, packet.labels))
    return signed, shifted, origin


def physical_finder_wrapper(packet, finder, *, raw_syndrome, shared_seed):
    """Finder(A,q,r,seed) returns ONE physical Boolean word or None."""
    if packet.syndrome or len(packet.pivots) != packet.dimension:
        raise ValueError("full-rank zero-origin source chart required")
    _origin(packet, raw_syndrome)

    def logical_finder(target):
        signed, shifted, origin = target_source_transform(packet, raw_syndrome, target)
        word = finder(signed, packet.modulus, shifted, shared_seed)
        if type(word) is not int or not 0 <= word < 1 << packet.input_qubits:
            return None
        if tuple(sum(a for i, a in enumerate(row) if word >> i & 1) % packet.modulus for row in signed) != shifted:
            return None
        physical = word ^ origin
        logical = sum((physical >> f & 1) << j for j, f in enumerate(packet.free))
        assert packet.assignment(logical) == tuple(physical >> i & 1 for i in range(packet.input_qubits))
        assert packet.residual(logical) == tuple(target)
        return logical

    return logical_finder


@dataclass(frozen=True)
class PartialWitnessSelector:
    packet: object
    finder: object

    def __post_init__(self):
        if self.packet.syndrome or len(self.packet.pivots) != self.packet.dimension or not callable(self.finder):
            raise ValueError("full-rank zero-origin packet and a fixed deterministic finder required")

    @property
    def group_size(self):
        return (self.packet.modulus // 2) ** self.packet.dimension

    def witness(self, target_index):
        if type(target_index) is not int or not 0 <= target_index < self.group_size:
            raise ValueError("target index outside phase group")
        target = group_vector(target_index, self.packet.dimension, self.packet.modulus // 2)
        word = self.finder(target)
        if type(word) is not int or not 0 <= word < 1 << self.packet.retained_qubits or self.packet.residual(word) != target:
            return 0, False
        return word, True

    def forward_basis(self, word, target_workspace=0, flag=0):
        self._check(word, target_workspace, flag)
        target = target_workspace ^ group_index(self.packet.residual(word), self.packet.modulus // 2)
        selected, valid = self.witness(target)
        return word ^ selected, target, flag ^ int(valid and word == selected)

    def inverse_basis(self, word, target_workspace, flag):
        self._check(word, target_workspace, flag)
        selected, valid = self.witness(target_workspace)
        original = word ^ selected
        return (original, target_workspace ^ group_index(self.packet.residual(original), self.packet.modulus // 2),
                flag ^ int(valid and original == selected))

    def _check(self, word, target, flag):
        if type(word) is not int or not 0 <= word < 1 << self.packet.retained_qubits or type(target) is not int or not 0 <= target < self.group_size or flag not in (0, 1):
            raise ValueError("valid complete basis registers required")


def selector_interface_gate(*, deterministic_given_explicit_seed=False,
                            seed_independent_of_target_and_fault_data=False,
                            uniform_bounded_time_algorithm=False,
                            verified_one_word_or_failure=False,
                            reversible_transcript_uncomputation=False,
                            independent_target_coverage_proved=False):
    declarations = {
        "fixed reproducible explicit seed": deterministic_given_explicit_seed,
        "fresh seed independent of target and prelabel fault data": seed_independent_of_target_and_fault_data,
        "uniform bounded runtime rather than a label-specific table": uniform_bounded_time_algorithm,
        "verified single witness or failure": verified_one_word_or_failure,
        "all target-dependent finder history uncomputed": reversible_transcript_uncomputation,
        "independent uniform-target source coverage theorem": independent_target_coverage_proved,
    }
    return {"status": "CONDITIONAL_SELECTOR_INTERFACE_GATE_NOT_PROVEN_SOLVER",
            "issues": [name for name, value in declarations.items() if not value],
            "obligations_satisfied_as_declared": all(declarations.values()),
            "declarations_programmatically_proven": False,
            "arbitrary_measured_quantum_witness_finder_automatically_compatible": False,
            "inverse_witness_function_uniform_fiber_sampler_or_second_witness_required": False,
            "candidate_record_accepted": False, "speedup_claim_allowed": False}


def integer_fault_survival_lower_bound(expected_faults):
    mu = Fraction(expected_faults)
    if mu < 0:
        raise ValueError("nonnegative expected fault count required")
    floor = mu.numerator // mu.denominator
    return Fraction(1, 1 << floor) * (1 - (mu - floor) / 2)


def partial_witness_resource_certificate(n, modulus_bits, overhead_bits, coverage_lower_bound,
                                         *, expected_packet_faults=0):
    for value, name in ((n, "dimension"), (modulus_bits, "full modulus bits")):
        _positive_integer(value, name)
    if modulus_bits < 2 or type(overhead_bits) is not int or overhead_bits < 0:
        raise ValueError("power-of-two modulus at least four and nonnegative overhead required")
    beta = Fraction(coverage_lower_bound)
    if not 0 <= beta <= 1:
        raise ValueError("unconditional independent-target coverage must be a probability")
    k, m = n * (modulus_bits - 1) + overhead_bits, n * modulus_bits + overhead_bits
    rank_bad = Fraction(1, 1 << k)
    # Round to a small rational whenever the exponentially small rank loss permits it.
    retained = beta / 2 if rank_bad <= beta / 2 else max(Fraction(0), beta - rank_bad)
    ideal = retained ** 2 / (1 << overhead_bits)
    survival = integer_fault_survival_lower_bound(expected_packet_faults)
    return {"status": "CONDITIONAL_SINGLE_WITNESS_NATIVE_READOUT_REDUCTION_NOT_SOLVER",
            "dimension": n, "full_modulus_bits": modulus_bits, "logical_width": k,
            "original_phase_states_per_attempt": m, "density_overhead_bits": overhead_bits,
            "assumed_unconditional_uniform_target_coverage_lower_bound": exact(beta),
            "binary_rank_rejection_probability_upper_bound": f"2^-{k}",
            "all_binary_prefixes_are_not_postselected": True,
            "coverage_after_charging_full_rank_rejection_lower_bound": exact(retained),
            "ideal_correct_residue_probability_per_original_attempt_lower_bound": exact(ideal),
            "expected_prelabel_packet_faults_upper_bound": exact(Fraction(expected_packet_faults)),
            "conditional_independent_fair_Z_mixture_ideal_component_weight_lower_bound": exact(survival),
            "gauged_correct_residue_probability_lower_bound": exact(ideal * survival),
            "success_bound_is_for_each_fixed_secret": True,
            "coverage_can_be_label_average_without_identifying_good_packets": True,
            "canonical_selection_overhead_is_exponential_when_overhead_bits_exceeds_log_scale": True,
            "fault_statuses_may_be_correlated_but_must_precede_fresh_labels_and_solver_seed": True,
            "gauge_transfer_is_a_source_obligation_not_an_arbitrary_noise_promise": True,
            "full_secret_completion_or_natural_lattice_composition_implemented": False,
            "uniform_polynomial_witness_finder_constructed": False,
            "independent_theorem_review": False, "candidate_record_accepted": False,
            "novelty_claim": False, "speedup_claim_allowed": False}


def correlated_attempt_failure_bound(ideal_block_success, expected_faults_per_block,
                                     attempts, *, markov_factor=12, verification_states=64):
    p, mu = Fraction(ideal_block_success), Fraction(expected_faults_per_block)
    _positive_integer(attempts, "preallocated attempts")
    _positive_integer(verification_states, "fresh verification states")
    if not 0 < p <= 1 or mu < 0 or type(markov_factor) is not int or markov_factor < 2:
        raise ValueError("positive ideal block success and valid aggregate fault budget required")
    threshold = (2 * markov_factor * mu).numerator // (2 * markov_factor * mu).denominator
    if Fraction(threshold) < 2 * markov_factor * mu:
        threshold += 1
    q = p / (1 << threshold)
    # (1-q)^h <= 1/(1+h*q); exact, conservative, and no huge power strings.
    none_bound = 1 / (1 + (attempts // 2) * q)
    markov = Fraction(0) if mu == 0 else Fraction(1, markov_factor)
    false_accept = min(Fraction(1), Fraction(attempts, 1 << verification_states))
    return {"status": "CONDITIONAL_CORRELATED_PRELABEL_BLOCK_AMPLIFICATION_LEDGER",
            "preallocated_disjoint_attempts": attempts,
            "expected_faults_per_complete_block_upper_bound": exact(mu),
            "maximum_faults_in_good_block": threshold,
            "guaranteed_good_blocks_on_aggregate_budget_event": attempts // 2,
            "source_labels_seeds_and_latent_gauge_coins_independent_conditional_fault_statuses": True,
            "independence_of_fault_statuses_or_unconditional_attempt_success_assumed": False,
            "aggregate_budget_failure_probability_upper_bound": exact(markov),
            "no_correct_verified_candidate_on_budget_event_probability_upper_bound": exact(none_bound),
            "any_wrong_full_candidate_passes_fresh_tests_upper_bound": exact(false_accept),
            "total_algorithm_failure_probability_upper_bound": exact(min(Fraction(1), markov + none_bound + false_accept)),
            "candidate_committed_before_fresh_verification_labels_required": True,
            "ideal_block_success_must_include_all_required_readout_and_true_candidate_verification": True,
            "gate_precision_and_native_gauge_lineage_composition_verified": False,
            "candidate_record_accepted": False, "speedup_claim_allowed": False}


def legal_target_coverage_transfer(legal_coverage_lower_bound, overhead_bits):
    beta = Fraction(legal_coverage_lower_bound)
    if not 0 <= beta <= 1 or type(overhead_bits) is not int or overhead_bits < 0:
        raise ValueError("legal-input probability and nonnegative density overhead required")
    legal_mass = Fraction(1 << overhead_bits, (1 << overhead_bits) + 1)
    return {"legal_input_sampling_law": "IID native label matrix and independent uniform target, globally conditioned on existence",
            "native_legal_pair_probability_lower_bound": exact(legal_mass),
            "unconditional_verified_target_coverage_lower_bound": exact(beta * legal_mass),
            "mean_of_per_label_legal_coverage_ratios_is_this_law": False,
            "planted_target_coverage_automatically_transfers": False}


def complete_block_resource_certificate(n, modulus_bits, overhead_bits, coverage_lower_bound,
                                        attempts, *, completion_slack=16, markov_factor=4):
    _positive_integer(completion_slack, "binary completion slack")
    _positive_integer(attempts, "preallocated attempts")
    selector = partial_witness_resource_certificate(n, modulus_bits, overhead_bits, coverage_lower_bound)
    from dcp_physical_phase_noise import read
    ideal = read(selector["ideal_correct_residue_probability_per_original_attempt_lower_bound"])
    verification = (attempts - 1).bit_length() + 32
    block_states = selector["original_phase_states_per_attempt"] + n + completion_slack + verification
    ideal_block = ideal * (1 - Fraction(1, 1 << completion_slack))
    mu = Fraction(block_states, n * modulus_bits)
    if not ideal_block:
        return {"status": "NO_POSITIVE_ASSUMED_COVERAGE_AFTER_RANK_CHARGE", "candidate_record_accepted": False}
    amplification = correlated_attempt_failure_bound(ideal_block, mu, attempts,
                                                     markov_factor=markov_factor, verification_states=verification)
    return {"status": "CONDITIONAL_FULL_SECRET_RESOURCE_COMPOSITION_NOT_NATIVE_LATTICE_PROOF",
            "dimension": n, "full_modulus_bits": modulus_bits, "density_overhead_bits": overhead_bits,
            "selector": selector, "fresh_binary_completion_states": n + completion_slack,
            "completion_rank_failure_probability_upper_bound": exact(Fraction(1, 1 << completion_slack)),
            "fresh_full_candidate_verification_states": verification,
            "ideal_complete_block_success_lower_bound": exact(ideal_block),
            "original_states_per_complete_attempt": block_states,
            "original_states_preallocated_for_all_attempts": attempts * block_states,
            "basis_fault_marginal_promise_required_for_each_fixed_secret": exact(Fraction(1, n * modulus_bits)),
            "amplification": amplification,
            "full_secret_failure_bound_below_one_third_as_declared": read(amplification[
                "total_algorithm_failure_probability_upper_bound"]) < Fraction(1, 3),
            "correlated_prelabel_faults_not_iid_success_trials": True,
            "native_lattice_state_supply_gauge_lineage_and_gate_precision_composed": False,
            "finder_coverage_is_an_assumption_not_an_experimental_result": True,
            "large_constant_state_budget_is_a_conditional_ledger_not_an_executed_algorithm": True,
            "candidate_record_accepted": False, "speedup_claim_allowed": False}


def bounded_selector_control(selector, *, maximum_logical_width=7):
    packet, G = selector.packet, selector.group_size
    k, n, Q = packet.retained_qubits, packet.dimension, packet.modulus // 2
    if k > maximum_logical_width or G > 1 << k:
        raise ValueError("bounded calibration requires logical_width>=group_bits and width within cap")
    N = 1 << k
    accepted = [(t, w) for t in range(G) if (pair := selector.witness(t))[1] for w in (pair[0],)]
    assert len({w for _, w in accepted}) == len(accepted)
    inverse_checks = 0
    for x, t, flag in itertools.product(range(N), range(G), (0, 1)):
        out = selector.forward_basis(x, t, flag)
        assert selector.inverse_basis(*out) == (x, t, flag)
        inverse_checks += 1
    correct = Fraction(len(accepted) ** 2, N * G)
    for s_index in range(G):
        s = group_vector(s_index, n, Q)
        amplitude = 0j
        for x in range(N):
            out, t, flag = selector.forward_basis(x)
            if flag:
                assert out == 0
                phase = sum(a * b for a, b in zip(s, packet.residual(x)))
                phase -= sum(a * b for a, b in zip(s, group_vector(t, n, Q)))
                amplitude += cmath.exp(2j * math.pi * phase / Q) / math.sqrt(N * G)
        assert abs(abs(amplitude) ** 2 - float(correct)) < 1e-12
    return {"labels": packet.labels, "modulus": packet.modulus, "logical_width": k,
            "accepted_target_witness_pairs": accepted,
            "full_basis_forward_inverse_checks": inverse_checks,
            "fixed_secret_QFT_controls": G,
            "uniform_target_coverage": exact(Fraction(len(accepted), G)),
            "herald_probability": exact(Fraction(len(accepted), N)),
            "correct_readout_probability_for_every_secret": exact(correct),
            "conditional_correct_readout_given_herald": exact(Fraction(len(accepted), G)),
            "which_path_history_not_uncomputed_correct_readout_probability": exact(Fraction(len(accepted), N * G)),
            "reference_finder_uses_bounded_enumeration": True,
            "reference_finder_is_a_uniform_polynomial_algorithm": False,
            "candidate_record_accepted": False, "speedup_claim_allowed": False}


def _full_target_source_control(n, width, q):
    if n * width * (q.bit_length() - 1) > 12:
        raise ValueError("complete source distribution control exceeds budget")
    low_cache, images, good = {}, set(), 0
    for entries in itertools.product(range(q), repeat=n * width):
        A = tuple(tuple(entries[l * width:(l + 1) * width]) for l in range(n))
        B = tuple(tuple(a & 1 for a in row) for row in A)
        if B not in low_cache:
            packet = compile_packet(B, q)
            low_cache[B] = packet if len(packet.pivots) == n else None
        base = low_cache[B]
        if base is None:
            continue
        packet = replace(base, labels=A)
        good += 1
        for sigma in range(1 << n):
            for t in itertools.product(range(q // 2), repeat=n):
                signed, target, origin = target_source_transform(packet, sigma, t)
                assert tuple(sum((row[i] & 1) for i in range(width) if origin >> i & 1) % 2 for row in A) == tuple(sigma >> l & 1 for l in range(n))
                key = signed, target
                assert key not in images
                images.add(key)
    assert len(images) == good * q ** n
    return {"dimension": n, "physical_width": width, "modulus": q,
            "complete_label_tables": q ** (n * width), "full_binary_rank_label_tables": good,
            "parity_wrapper_domain_and_uniform_full_target_image_pairs": len(images),
            "uniform_full_target_joint_law_exact_bijection_verified": True,
            "original_binary_row_syndrome_not_rref_row_bits_used": True}


def run_controls():
    controls = []
    for labels, q, cutoff in ((((1, 1, 2, 4),), 8, 4), (((1, 1, 2, 4),), 8, 2),
                              (((1, 0, 2, 0), (0, 1, 0, 2)), 4, 4)):
        packet = compile_packet(labels, q)
        words = {}
        for x in range(1 << packet.retained_qubits):
            words.setdefault(packet.residual(x), x)
        selector = PartialWitnessSelector(packet, lambda t, words=words, cutoff=cutoff, packet=packet:
                                           words.get(tuple(t)) if group_index(t, packet.modulus // 2) < cutoff else None)
        controls.append(bounded_selector_control(selector))
    assumed = [partial_witness_resource_certificate(n, 4 * n + 1, delta, Fraction(1, n * n),
                                                    expected_packet_faults=Fraction(n * (4 * n + 1) + delta, n * (4 * n + 1)))
               for n, delta in ((8, 0), (8, 4), (16, 0), (16, 16), (32, 0))]
    return {"status": "LOCAL_DERIVATION_REVIEW_PENDING",
            "bounded_full_unitary_and_fixed_secret_controls": controls,
            "complete_independent_full_target_source_controls": [_full_target_source_control(1, 3, 4), _full_target_source_control(2, 3, 4)],
            "conditional_resource_scaling_assuming_missing_finder": assumed,
            "conditional_full_secret_block_ledgers": [complete_block_resource_certificate(
                n, 4 * n + 1, delta, Fraction(1, n * n), (1 << (40 + delta)) * n ** 4)
                for n, delta in ((8, 0), (8, 16), (16, 0), (16, 16), (32, 0))],
            "legal_target_source_transfer_controls": [legal_target_coverage_transfer(Fraction(1, 16), d) for d in (0, 4, 16)],
            "claim_gate": {"single_partial_witness_suffices_for_this_conditional_readout": True,
                           "complete_fiber_rank_unrank_uniform_sampling_or_two_witnesses_required": False,
                           "inverse_witness_function_required": False,
                           "shared_seed_and_clean_target_dependent_history_required": True,
                           "original_states_and_rejections_are_charged": True,
                           "arbitrary_measured_quantum_solver_automatically_lifts": False,
                           "uniform_polynomial_native_finder_supplied": False,
                           "full_native_lattice_fault_and_precision_composition_verified": False,
                           "independent_theorem_review": False, "novelty_claim": False,
                           "candidate_record_accepted": False, "speedup_claim_allowed": False},
            "dependency_sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                                  for p in (Path(__file__), ROOT / "theorems/dcp_carry_packets.py",
                                            ROOT / "theorems/dcp_conditional_carry_features.py",
                                            ROOT / "theorems/dcp_dense_phase_transport.py",
                                            ROOT / "theorems/dcp_prelabel_fault_gauge.py",
                                            ROOT / "theorems/dcp_physical_phase_noise.py",
                                            ROOT / "theorems/dcp_terminal_affine_fibers.py",
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
