"""Classical-query / quantum-processing simulation of a codomain instrument.

LOCAL DERIVATION / REVIEW PENDING. Not a classical simulator for arbitrary
quantum computation, and not a general DHSP oracle lower bound.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path

import numpy as np

from dhsp_codomain_instrument import _integer, _source, probability, rational

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/classical_baselines/dhsp_codomain_sample_simulation.json"


def _matrix(n):
    return [[Fraction(0) for _ in range(n)] for _ in range(n)]


def _operators(operators):
    if not isinstance(operators, (list, tuple)) or not operators or len(operators) > 4:
        raise ValueError("bounded nonempty exact real operator family required")
    d = len(operators[0])
    if not 1 <= d <= 4:
        raise ValueError("bounded memory dimension required")
    result = []
    for W in operators:
        if len(W) != d or any(len(row) != d for row in W) or any(type(x) not in (int, Fraction) for row in W for x in row):
            raise ValueError("equal-sized exact real square operators required")
        W = tuple(tuple(map(Fraction, row)) for row in W)
        for i in range(d):
            for j in range(d):
                if sum(W[k][i]*W[k][j] for k in range(d)) != int(i == j):
                    raise ValueError("operators must be unitary, not silently normalized")
        result.append(W)
    return result


def channel_choi(p, operators):
    """Unnormalized Choi blocks; trace=d. OUT then IN basis for each tag."""
    p, Ws = probability(p), _operators(operators)
    if len(p) != len(Ws):
        raise ValueError("operator and probability families must match")
    d = len(Ws[0])
    vectors = [tuple(x for row in W for x in row) for W in Ws]
    mean = [sum(p[y]*vectors[y][i] for y in range(len(p))) for i in range(d*d)]
    H, F = _matrix(d*d), _matrix(d*d)
    for i in range(d*d):
        for j in range(d*d):
            H[i][j] = mean[i]*mean[j]
            F[i][j] = sum(p[y]*vectors[y][i]*vectors[y][j] for y in range(len(p)))-H[i][j]
    return H, F


def empirical_choi(indices, operators):
    """Uniform SAMPLE POSITIONS, including repeated labels; no deduplication."""
    Ws = _operators(operators)
    if not isinstance(indices, (list, tuple)) or not indices or len(indices) > 16 or any(type(y) is not int or not 0 <= y < len(Ws) for y in indices):
        raise ValueError("bounded nonempty sample-index list required")
    counts = [Fraction(indices.count(y), len(indices)) for y in range(len(Ws))]
    return channel_choi(counts, Ws)


def empirical_control(p, operators, samples, name):
    p, Ws = probability(p), _operators(operators)
    _integer(samples, "sample-list size")
    if samples > 4 or len(p) != len(Ws):
        raise ValueError("exact enumeration is bounded calibration only")
    H, F = channel_choi(p, Ws)
    d, size = len(Ws[0]), len(H)
    mean_H, mean_F = _matrix(size), _matrix(size)
    tuples = 0
    for indices in product(range(len(p)), repeat=samples):
        weight = Fraction(1)
        for y in indices:
            weight *= p[y]
        sample_H, sample_F = empirical_choi(indices, Ws)
        for i in range(size):
            for j in range(size):
                mean_H[i][j] += weight*sample_H[i][j]
                mean_F[i][j] += weight*sample_F[i][j]
        tuples += 1
    for i in range(size):
        for j in range(size):
            assert mean_H[i][j]-H[i][j] == F[i][j]/samples
            assert mean_F[i][j]-F[i][j] == -F[i][j]/samples
    mean_operator = np.array([[sum(p[y]*Ws[y][i][j] for y in range(len(p))) for j in range(d)] for i in range(d)], dtype=float)
    effect = np.eye(d)-mean_operator.T @ mean_operator
    maximum_error = float(np.linalg.eigvalsh(effect).max()/samples)
    choi_error = sum(F[i][i] for i in range(size))/Fraction(d*samples)
    return {
        "name": name, "memory_dimension": d, "samples_per_probe": samples,
        "source_probabilities": [rational(x) for x in p],
        "operators": [[[rational(x) for x in row] for row in W] for W in Ws],
        "source_choi_H": [[rational(x) for x in row] for row in H],
        "source_choi_F": [[rational(x) for x in row] for row in F],
        "empirical_average_choi_H": [[rational(x) for x in row] for row in mean_H],
        "empirical_average_choi_F": [[rational(x) for x in row] for row in mean_F],
        "enumerated_sample_tuples": tuples,
        "normalized_choi_input_trace_distance": rational(choi_error),
        "maximum_input_trace_distance_numeric_only": maximum_error,
        "dimension_independent_half_diamond_upper": rational(Fraction(1, samples)),
        "entangled_reference_allowed": True,
        "source_mean_operator_given_to_simulator": False,
    }


def physical_empirical_control(operators, indices):
    """Build the empirical uniform-index isometry and measure only its H/F tag."""
    W = np.asarray(operators, dtype=complex)
    if W.ndim != 3 or not 1 <= W.shape[0] <= 4 or W.shape[1] != W.shape[2] or not 1 <= W.shape[1] <= 4 or not np.isfinite(W).all():
        raise ValueError("bounded operator family required")
    d = W.shape[1]
    if any(not np.allclose(U.conj().T @ U, np.eye(d), atol=1e-12, rtol=0) for U in W):
        raise ValueError("unitary family required")
    if not isinstance(indices, (list, tuple)) or not indices or len(indices) > 8 or any(type(y) is not int or not 0 <= y < len(W) for y in indices):
        raise ValueError("bounded empirical sample positions required")
    m = len(indices)
    # IN is an entangled reference, not a known or reset memory assumption.
    amplitude = np.stack([W[y]/np.sqrt(m*d) for y in indices])
    accepted = np.sum(amplitude, axis=0)/np.sqrt(m)
    failed = amplitude-accepted[None, :, :]/np.sqrt(m)
    accepted = accepted.reshape(d*d)
    H = np.outer(accepted, accepted.conj())
    F = sum(np.outer(row.reshape(d*d), row.reshape(d*d).conj()) for row in failed)
    mean_operator = W[list(indices)].mean(axis=0)
    vec = mean_operator.reshape(d*d)
    expected_H = np.outer(vec, vec.conj())/d
    expected_F = sum(np.outer(W[y].reshape(d*d), W[y].reshape(d*d).conj()) for y in indices)/(m*d)-expected_H
    return {"sample_indices": list(indices), "memory_dimension": d,
            "operators_real": W.real.tolist(), "operators_imag": W.imag.tolist(),
            "H_real": H.real.tolist(), "H_imag": H.imag.tolist(),
            "F_real": F.real.tolist(), "F_imag": F.imag.tolist(),
            "physical_formula_residual": float(max(np.max(np.abs(H-expected_H)), np.max(np.abs(F-expected_F)))),
            "trace": float(np.trace(H+F).real),
            "minimum_failure_eigenvalue": float(np.linalg.eigvalsh(F).min()),
            "sample_positions_not_unique_labels": True}


def predictive_distribution(N, forced):
    """Posterior uniform half subset, conditioned on prior correct-label draws."""
    _source(N, 1)
    if N > 64 or not isinstance(forced, (tuple, list)) or len(set(forced)) != len(forced) or len(forced) > N//2 or any(type(y) is not int or not 0 <= y < N for y in forced):
        raise ValueError("bounded distinct forced half-subset members required")
    c, M = len(forced), N//2
    return tuple(Fraction(1, M) if y in forced else Fraction(M-c, M*(N-c)) for y in range(N))


def _policy(policy, prefix):
    if policy == "zero":
        return 0
    if policy == "alternating":
        return len(prefix) % 2
    if policy == "last_label_parity":
        return prefix[-1] % 2 if prefix else 0
    if policy == "collision_feedback":
        return int(len(set(prefix)) != len(prefix))
    raise ValueError("declared bounded adaptive source policy required")


def transcript_probability(N, hypothesis, labels, policy):
    """Exact posterior law with one shared subset, never a resampled nuisance."""
    _source(N, 1)
    if N > 8 or not isinstance(labels, (tuple, list)) or len(labels) > 4 or any(type(y) is not int or not 0 <= y < N for y in labels):
        raise ValueError("bounded label history required")
    if type(hypothesis) is not int or hypothesis not in (0, 1):
        raise ValueError("canonical hidden parity required")
    _policy(policy, ())
    forced, weight = set(), Fraction(1)
    for t, y in enumerate(labels):
        if _policy(policy, labels[:t]) == hypothesis:
            dist = predictive_distribution(N, sorted(forced))
            weight *= dist[y]
            if weight == 0:
                return weight
            forced.add(y)
        else:
            weight /= N
    return weight


def transcript_control(N, queries, policy):
    _source(N, 1)
    _integer(queries, "label-only samples", 0)
    if N > 8 or queries > 4:
        raise ValueError("full transcripts are bounded calibration only")
    totals, TV = [Fraction(0), Fraction(0)], Fraction(0)
    rows = []
    for labels in product(range(N), repeat=queries):
        weights = [transcript_probability(N, h, labels, policy) for h in (0, 1)]
        totals = [totals[h]+weights[h] for h in (0, 1)]
        TV += abs(weights[0]-weights[1])/2
        rows.append({"labels": list(labels), "probabilities": [rational(x) for x in weights]})
    bound = min(Fraction(1), Fraction(queries*(queries-1), 2*N))
    assert totals == [1, 1] and TV <= bound
    return {"rotation_order": N, "label_only_queries": queries, "policy": policy,
            "shared_subset": True, "records": rows, "exact_total_variation": rational(TV),
            "coupling_upper": rational(bound), "domain_indices_available_to_decoder": False}


def _cuberoot(n):
    lo, hi = 0, 1 << ((n.bit_length()+2)//3)
    while lo+1 < hi:
        mid = (lo+hi)//2
        if mid**3 <= n:
            lo = mid
        else:
            hi = mid
    return hi if hi**3 <= n else lo


def simulation_certificate(n, probes, samples=None, implementation_error=Fraction(0)):
    _integer(n, "modulus bits")
    _integer(probes, "instrument calls", 0)
    if type(implementation_error) not in (int, Fraction) or not 0 <= implementation_error <= 1:
        raise ValueError("exact total composed parity-comparison trace-error budget required")
    N = 1 << n
    if samples is None:
        root = max(1, _cuberoot(2*N//max(1, probes)))
        m0 = 1 << (root.bit_length()-1)
        choices = (m0, 2*m0)
        samples = min(choices, key=lambda m: Fraction(2*probes, m)+Fraction(probes*m*(probes*m-1), 2*N))
    _integer(samples, "samples per empirical call")
    Q = probes*samples
    one_hypothesis_error = Fraction(probes, samples)
    sample_distance = min(Fraction(1), Fraction(Q*(Q-1), 2*N))
    ideal = min(Fraction(1), 2*one_hypothesis_error+sample_distance)
    bound = min(Fraction(1), ideal+implementation_error)
    return {"modulus_bits": n, "rotation_order": str(N), "instrument_calls": probes,
            "samples_per_empirical_call": str(samples), "total_classical_label_samples": str(Q),
            "empirical_list_size_is_power_of_two": samples & (samples-1) == 0,
            "simulation_error_per_hypothesis": rational(one_hypothesis_error),
            "simulated_label_transcript_distance_upper": rational(sample_distance),
            "ideal_original_instrument_parity_distance_upper": rational(ideal),
            "total_composed_parity_comparison_trace_error_budget": rational(implementation_error),
            "original_instrument_distance_upper_with_error": rational(bound),
            "binary_parity_success_upper_with_error": rational((1+bound)/2),
            "arbitrary_memory_dimension_and_entangled_reference_allowed": True,
            "known_codomain_controls_on_incoming_quantum_memory_allowed": True,
            "initial_memory_secret_independent_required_for_parity_gate": True,
            "same_fixed_nuisance_for_every_call": True,
            "classical_query_quantum_processing_not_classical_computation": True,
            "other_oracle_queries_retained_domain_or_coherent_subgroup_choices_covered": False,
            "simulator_samples_not_free_algorithm_resources": True,
            "conditional_herald_accuracy_certified": False,
            "candidate_record_accepted": False, "speedup_claim_allowed": False}


def adaptive_memory_control(samples):
    """Two calls, entangled reference, tag-adaptive subgroup, fixed hidden subset."""
    _integer(samples, "empirical list size")
    if samples > 16:
        raise ValueError("bounded adaptive memory calibration required")
    rotation = np.array([[3/5, -4/5], [4/5, 3/5]])
    Ws = [np.eye(2), np.diag([1, -1]), np.array([[0, 1], [1, 0]]), rotation]
    gates = [np.kron(W, np.eye(2)) for W in Ws]
    interleave = np.kron(rotation, np.eye(2))
    bell = np.array([1, 0, 0, 1])/np.sqrt(2)
    initial = np.outer(bell, bell)
    subsets = list(combinations(range(4), 2))

    def call(rho, S, epsilon, h, m):
        p = [Fraction(1, 2) if y in S else 0 for y in range(4)] if epsilon == h else [Fraction(1, 4)]*4
        mean = sum(float(p[y])*gates[y] for y in range(4))
        H = mean @ rho @ mean.T
        F = sum(float(p[y])*gates[y] @ rho @ gates[y].T for y in range(4))-H
        return (H, F) if m is None else (H+F/m, F*(1-1/m))

    def execute(h, m, resample):
        out = np.zeros((16, 16))
        for S in subsets:
            first = call(initial, S, 0, h, m)
            for a in range(2):
                rho = interleave @ first[a] @ interleave.T
                second_subsets = subsets if resample else [S]
                for next_S in second_subsets:
                    second = call(rho, next_S, a, h, m)
                    for b in range(2):
                        offset = 4*(2*a+b)
                        out[offset:offset+4, offset:offset+4] += second[b]/(len(subsets)*len(second_subsets))
        return out

    source = [execute(h, None, False) for h in (0, 1)]
    simulated = [execute(h, samples, False) for h in (0, 1)]
    fresh = [execute(h, None, True) for h in (0, 1)]
    distances = [float(np.sum(np.abs(np.linalg.eigvalsh(source[h]-simulated[h])))/2) for h in (0, 1)]
    assert all(x <= 2/samples+1e-10 for x in distances)
    return {"samples_per_call": samples, "instrument_calls": 2,
            "source_states_by_parity": [r.tolist() for r in source],
            "simulated_states_by_parity": [r.tolist() for r in simulated],
            "fresh_resampled_states_by_parity": [r.tolist() for r in fresh],
            "simulation_distances_by_parity": distances,
            "source_parity_trace_distance": float(np.sum(np.abs(np.linalg.eigvalsh(source[0]-source[1])))/2),
            "simulated_parity_trace_distance": float(np.sum(np.abs(np.linalg.eigvalsh(simulated[0]-simulated[1])))/2),
            "shared_resampled_maximum_frobenius_difference": float(max(np.linalg.norm(source[h]-fresh[h]) for h in (0, 1))),
            "entangled_reference_retained": True, "all_flags_and_memory_retained": True,
            "source_is_not_resampled": True, "unknown_mean_operator_used_by_physical_simulator": False,
            "bounded_calibration_not_scaling_evidence": True}


def postselection_counterledger(n, samples):
    _integer(n, "modulus bits", 2)
    _integer(samples, "empirical samples")
    M = 1 << (n-1)
    true_herald = Fraction(1, M)
    empirical_herald = true_herald+(1-true_herald)/samples
    return {"modulus_bits": n, "hidden_half_image_size": str(M), "empirical_samples": str(samples),
            "true_full_label_herald": rational(true_herald),
            "empirical_average_full_label_herald": rational(empirical_herald),
            "unconditional_complete_output_trace_distance": rational((1-true_herald)/samples),
            "empirical_heralded_pure_target_overlap": rational(Fraction(samples, samples+M-1)),
            "fidelity_convention": "Pure-target expectation in normalized H block, not its square root",
            "efficient_conditional_pure_image_preparation_claim_allowed": False}


def run_controls():
    I, X, Z = [[1, 0], [0, 1]], [[0, 1], [1, 0]], [[1, 0], [0, -1]]
    rotation = [[Fraction(3, 5), Fraction(-4, 5)], [Fraction(4, 5), Fraction(3, 5)]]
    families = [("identity_Z_diamond_not_choi", (Fraction(1, 2),)*2, [I, Z]),
                ("noncommuting_identity_X_Z", (Fraction(1, 2), Fraction(1, 3), Fraction(1, 6)), [I, X, Z]),
                ("rational_nonorthogonal_controls", (Fraction(3, 4), Fraction(1, 4)), [I, rotation]),
                ("global_phase_cancellation", (Fraction(1, 2),)*2, [I, [[-1, 0], [0, -1]]])]
    empirical = [empirical_control(p, Ws, m, name) for name, p, Ws in families for m in (1, 2, 4)]
    S = np.diag([1, 1j])
    physical = [physical_empirical_control(Ws, indices) for Ws in ([I, Z], [I, S], [X, rotation]) for indices in ([0], [0, 1], [0, 0, 1], [1, 0, 1, 1])]
    posterior = []
    for N in (4, 8):
        for c in range(N//2+1):
            forced = list(range(c))
            law = predictive_distribution(N, forced)
            TV = sum(abs(x-Fraction(1, N)) for x in law)/2
            assert TV == Fraction(c, N)
            posterior.append({"rotation_order": N, "forced": forced,
                              "predictive_law": [rational(x) for x in law], "distance_to_uniform": rational(TV)})
    transcripts = [transcript_control(N, Q, policy) for N, Q in ((4, 3), (4, 4), (8, 3)) for policy in ("zero", "alternating", "last_label_parity", "collision_feedback")]
    return {
        "status": "LOCAL_DERIVATION_REVIEW_PENDING",
        "empirical_channel_controls": empirical, "physical_empirical_controls": physical,
        "exact_posterior_controls": posterior, "adaptive_shared_subset_controls": transcripts,
        "adaptive_entangled_memory_controls": [adaptive_memory_control(m) for m in (1, 2, 4, 8)],
        "dimension_free_scaling_ledgers": [simulation_certificate(n, n*n) for n in (32, 64, 128, 256)],
        "precision_floor_counterledger": simulation_certificate(256, 256**2, implementation_error=Fraction(1, 10**6)),
        "polynomial_accuracy_simulator_ledger": simulation_certificate(128, 128**2, 1 << 34),
        "postselection_counterledger": postselection_counterledger(128, 1 << 34),
        "chosen_query_scope_countercontrol": {"queries": [[0, 0], [1, 0]], "hidden_shifts": [0, 1],
            "same_output_iff_shift_zero": True, "classical_success": rational(Fraction(1)),
            "why_outside": "Chosen DOMAIN queries with equality comparison, not the label-only subgroup sampler."},
        "claim_gate": {"independent_review": False, "novelty_claim": False, "candidate_accepted": False,
            "speedup_claim_allowed": False, "general_dhsp_oracle_lower_bound": False,
            "arbitrary_quantum_postprocessing_classically_simulated": False},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPORT)
    args = parser.parse_args()
    report = run_controls()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n")
    print(json.dumps({"report": str(args.output), "exact_empirical_controls": len(report["empirical_channel_controls"]),
                      "adaptive_source_controls": len(report["adaptive_shared_subset_controls"]), "candidate_accepted": False}))


if __name__ == "__main__":
    main()
