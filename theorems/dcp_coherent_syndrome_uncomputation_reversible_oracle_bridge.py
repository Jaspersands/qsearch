"""Separate coherent, dephased and discarded CNOT syndromes.

For B equiprobable branches, retain relative phases alpha_d:
  |Psi> = B^-1/2 sum_d exp(i alpha_d)|d>(|0>+exp(i theta_d)|1>)/sqrt(2).
The coherent trace distance is sqrt(1-|<Psi|Psi'>|^2). The average of
|sin((theta_d-theta'_d)/2)| is instead the DEPHASED-syndrome distance.
Unitary processing preserves the former, not a bound by the latter.
Native CNOT collimation generates secret-dependent alpha_d; dropping those
phases is not a gauge choice. All dense computations here are finite controls,
not efficient DCP decoders or impossibility results.
"""
from __future__ import annotations

import cmath
import hashlib
import itertools
import json
import math

THEOREM_ID = "dcp_coherent_syndrome_uncomputation_reversible_oracle_bridge"
SCHEMA_VERSION = "dcp-coherent-syndrome-uncomputation-reversible-oracle-bridge-v2"


def _phases(values, name):
    out = tuple(float(x) for x in values)
    if not out or any(not math.isfinite(x) for x in out):
        raise ValueError(f"nonempty finite {name} required")
    return out


def branch_state(theta, branch_phases=None):
    """Explicit coherent state in (syndrome, target) order; relative phases retained."""
    theta = _phases(theta, "branch phases")
    B = len(theta)
    if B & (B-1):
        raise ValueError("power-of-two syndrome dimension required")
    alpha = (0.0,)*B if branch_phases is None else _phases(branch_phases, "syndrome amplitudes")
    if len(alpha) != B:
        raise ValueError("matching syndrome phase count required")
    norm = math.sqrt(2*B)
    return tuple(cmath.exp(1j*(a+bit*t))/norm for a, t in zip(alpha, theta) for bit in (0, 1))


def verify_branch_helstrom_and_unitary_invariance(
    theta_s, theta_s_prime, *, branch_phases_s=None, branch_phases_s_prime=None,
):
    """Trace distance means half the trace norm, twice equal-prior success bias."""
    theta_s, theta_s_prime = _phases(theta_s, "theta"), _phases(theta_s_prime, "theta prime")
    if len(theta_s) != len(theta_s_prime):
        raise ValueError("matching branch count required")
    state = branch_state(theta_s, branch_phases_s)
    other = branch_state(theta_s_prime, branch_phases_s_prime)
    B = len(theta_s)
    inner = sum(a.conjugate()*b for a, b in zip(state, other))
    coherent = math.sqrt(max(0.0, 1.0-abs(inner)**2))
    dephased = sum(abs(math.sin((a-b)/2)) for a, b in zip(theta_s, theta_s_prime))/B
    mean_diff = sum(cmath.exp(1j*a)-cmath.exp(1j*b) for a, b in zip(theta_s, theta_s_prime))/B
    discarded = abs(mean_diff)/2
    return {
        "num_branches": B,
        "inner_product_real": inner.real, "inner_product_imag": inner.imag,
        "coherent_joint_trace_distance": coherent,
        "dephased_syndrome_trace_distance": dephased,
        "traceout_trace_distance": discarded,
        "data_processing_hierarchy_holds": coherent+1e-12 >= dephased >= discarded-1e-12,
        "postselected_d0_survival": 1/B,
        "postselected_d0_conditional_distance": abs(math.sin((theta_s[0]-theta_s_prime[0])/2)),
        "v1_branch_average_is_not_a_coherent_upper_bound": coherent > dephased+1e-12,
        "dense_reference_dimension": 2*B,
    }


def native_cnot_collimation_audit(input_phases_s, input_phases_s_prime):
    """Actually permute a native product state, retaining anchor amplitudes.

    Target u=x_0, syndromes d_j=x_j XOR x_0. Branch alpha_d=sum_{j>0}
    theta_j*d_j and theta_d=theta_0+sum_{j>0}(1-2*d_j)*theta_j.
    """
    source = _phases(input_phases_s, "native phases")
    other = _phases(input_phases_s_prime, "native phases prime")
    if len(source) != len(other) or len(source) > 10:
        raise ValueError("matching finite-control input sizes at most ten required")
    W, after, branch_data = len(source), [], []
    for phases in (source, other):
        native = tuple(cmath.exp(1j*sum(x*a for x, a in zip(bits, phases)))/math.sqrt(1 << W)
                       for bits in itertools.product((0, 1), repeat=W))
        permuted, theta, alpha = [0j]*(1 << W), [], []
        for d in itertools.product((0, 1), repeat=W-1):
            theta.append(phases[0]+sum((1-2*b)*a for b, a in zip(d, phases[1:])))
            alpha.append(sum(b*a for b, a in zip(d, phases[1:])))
            syndrome = sum(b << (W-2-j) for j, b in enumerate(d))
            for u in (0, 1):
                bits = (u, *(b ^ u for b in d))
                index = sum(b << (W-1-j) for j, b in enumerate(bits))
                permuted[2*syndrome+u] = native[index]
        reference = branch_state(theta, alpha)
        after.append((tuple(permuted), max(abs(a-b) for a, b in zip(reference, permuted))))
        branch_data.append((theta, alpha))
    theta, alpha = branch_data[0]
    theta_prime, alpha_prime = branch_data[1]
    audit = verify_branch_helstrom_and_unitary_invariance(
        theta, theta_prime, branch_phases_s=alpha, branch_phases_s_prime=alpha_prime)
    native_inner = complex(1)
    for a, b in zip(source, other):
        native_inner *= (1+cmath.exp(1j*(b-a)))/2
    measured_inner = sum(a.conjugate()*b for a, b in zip(after[0][0], after[1][0]))
    omitted = verify_branch_helstrom_and_unitary_invariance(theta, theta_prime)
    return {"wires": W, "max_native_permutation_error": max(a[1] for a in after),
            "native_inner_product_error": abs(native_inner-measured_inner),
            "branch_accounting": audit,
            "dropping_branch_phases_changes_coherent_distance": abs(
                audit["coherent_joint_trace_distance"]-omitted["coherent_joint_trace_distance"]) > 1e-12,
            "exponential_reference_only": True}


def verify_known_offset_controlled_uncomputation_control(theta_0_s, theta_0_s_prime, known_offsets):
    """Explicit controlled phase and H gates for PUBLIC offsets, alpha_d=0 only."""
    offsets = _phases(known_offsets, "known offsets")
    theta, other = [theta_0_s+d for d in offsets], [theta_0_s_prime+d for d in offsets]
    B = len(offsets)
    outputs = []
    for values in (theta, other):
        state = list(branch_state(values))
        for d, delta in enumerate(offsets):
            state[2*d+1] *= cmath.exp(-1j*delta)
        # Syndrome-register Walsh-Hadamard butterflies, target untouched.
        step = 1
        while step < B:
            for start in range(0, B, 2*step):
                for d in range(start, start+step):
                    for bit in (0, 1):
                        a, b = 2*d+bit, 2*(d+step)+bit
                        left, right = state[a], state[b]
                        state[a], state[b] = (left+right)/math.sqrt(2), (left-right)/math.sqrt(2)
            step *= 2
        outputs.append(state)
    before = verify_branch_helstrom_and_unitary_invariance(theta, other)
    inner = sum(a.conjugate()*b for a, b in zip(*outputs))
    distance = math.sqrt(max(0.0, 1-abs(inner)**2))
    zero_prob = sum(abs(x)**2 for x in outputs[0][:2])
    return {"num_branches": B, "uncompute_to_zero_probability": zero_prob,
            "trace_distance_before": before["coherent_joint_trace_distance"],
            "trace_distance_after": distance,
            "unitary_helstrom_preserved": abs(distance-before["coherent_joint_trace_distance"]) < 1e-12,
            "deterministic_uncomputation_exact": abs(zero_prob-1) < 1e-12,
            "public_offset_and_zero_branch_amplitude_phase_assumption": True}


def generate_dcp_coherent_syndrome_uncomputation_reversible_oracle_certificate():
    counterexample = verify_branch_helstrom_and_unitary_invariance([0, 0], [0, math.pi])
    native = native_cnot_collimation_audit([0, 0, 0], [math.pi/3, math.pi/2, -math.pi/5])
    control = verify_known_offset_controlled_uncomputation_control(0, math.pi/2, [0, .4, -.7, 1.1])
    payload = {
        "theorem_id": THEOREM_ID, "schema_version": SCHEMA_VERSION,
        "scope_constraints": {
            "applies_to": "Explicit pure coherent branch states, their dephased and discarded images; finite native CNOT controls",
            "does_not_claim": "Efficient joint measurement synthesis, coherent upper bound by a branch average, or a DCP no-go",
            "native_branch_amplitude_phases_retained": True,
        },
        "v1_coherent_upper_bound_retracted": True,
        "coherent_vs_dephased_counterexample": counterexample,
        "native_cnot_control": native, "known_offset_constructive_control": control,
        "all_checks_passed": (counterexample["data_processing_hierarchy_holds"]
                              and counterexample["v1_branch_average_is_not_a_coherent_upper_bound"]
                              and native["max_native_permutation_error"] < 1e-12
                              and native["native_inner_product_error"] < 1e-12
                              and native["branch_accounting"]["data_processing_hierarchy_holds"]
                              and native["dropping_branch_phases_changes_coherent_distance"]
                              and control["deterministic_uncomputation_exact"]
                              and control["unitary_helstrom_preserved"]),
        "honesty_guardrails": {"accepted_speedup_candidate": False,
                               "new_active_negative_result_created": False, "novelty_claim": False},
    }
    payload["certificate_sha256_16"] = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()[:16]
    return payload
