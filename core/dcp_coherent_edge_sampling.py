"""List-free DCP edge readout with a shared geometric Grover schedule.

The support register stays coherent: no unique partner, counting oracle, or
exponential list is required. Explicit small-state controls accompany a
review-pending positive interference kernel. Search time remains exponential.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product
from math import asin, comb, log2, sin, sqrt

import numpy as np

from dcp_affine_marked_pairing import _jsonable
from dcp_balanced_pairing import BalancedPairingProgram, balanced_certificate


def unrank_support(width: int, weight: int, rank: int) -> int:
    """Lexicographic combination unranking in at most width candidate steps."""
    if (any(type(x) is not int for x in (width, weight, rank))
            or not 0 <= weight <= width or not 0 <= rank < comb(width, weight)):
        raise ValueError("invalid combination rank")
    mask, start = 0, 0
    for remaining in range(weight, 0, -1):
        for i in range(start, width-remaining+1):
            block = comb(width-i-1, remaining-1)
            if rank < block:
                mask |= 1 << i
                start = i+1
                break
            rank -= block
    return mask


def support_from_index(program: BalancedPairingProgram, index: int) -> int | None:
    count = program.list_length**2
    padded = 1 << (count-1).bit_length()
    if type(index) is not int or not 0 <= index < padded:
        raise ValueError("support index outside padded domain")
    if index >= count:
        return None
    left, right = divmod(index, program.list_length)
    half = len(program.labels)//2
    return (unrank_support(half, program.weight, left)
            | unrank_support(half, program.weight, right) << half)


def edge_predicate(program: BalancedPairingProgram, assignment: int, index: int) -> bool:
    if type(assignment) is not int or not 0 <= assignment < 1 << len(program.labels):
        raise ValueError("assignment outside domain")
    support = support_from_index(program, index)
    if support is None or not program.marked(assignment) or not program.marked(assignment ^ support):
        return False
    delta = sum((-a if assignment & (1 << i) else a)
                for i, a in enumerate(program.labels) if support & (1 << i))
    return delta % (1 << program.n) == 1 << (program.n-1)


def schedule_certificate(padded: int, tail_bits: int = 16) -> dict:
    if (type(padded) is not int or padded < 2 or padded & (padded-1)
            or type(tail_bits) is not int or tail_bits < 1):
        raise ValueError("power-of-two domain >=2 and positive tail bits required")
    index_bits = padded.bit_length()-1
    coin_bits = (index_bits+1)//2
    stop = Fraction(1, 1 << coin_bits)
    rho = 1-stop
    # cos(2 theta_1)=1-2/P; sin^2(2 theta_1)=4(P-1)/P^2.
    f_two_theta = stop**2*(1-Fraction(2, padded)) / (
        stop**2+16*rho*Fraction(padded-1, padded*padded))
    singleton_kernel = (1-f_two_theta)/2
    cutoff = tail_bits*(1 << coin_bits)
    return {"padded_supports": padded, "index_bits": index_bits,
            "coin_bits": coin_bits, "stop_probability": stop, "rho": rho,
            "cutoff": cutoff, "tail_probability_upper": Fraction(1, 1 << tail_bits),
            "singleton_kernel": singleton_kernel,
            "mean_iterations_untruncated": rho/stop,
            "mean_reversible_predicate_calls_upper": 2*(1 << coin_bits)-1,
            "maximum_reversible_predicate_calls": 2*cutoff-1,
            "randomization_shared_across_entire_source": True}


def sample_iterations(padded: int, rng, tail_bits: int = 16) -> int | None:
    """Exact public coins. None means a CHARGED abort, not resampling."""
    row = schedule_certificate(padded, tail_bits)
    for t in range(row["cutoff"]):
        if rng.getrandbits(row["coin_bits"]) == 0:
            return t
    return None


def _angle(degree: int, padded: int) -> float:
    if type(degree) is not int or not 0 <= degree <= padded:
        raise ValueError("degree outside support domain")
    return asin(sqrt(degree/padded))


def marked_amplitude(degree: int, padded: int, iterations: int) -> float:
    if type(iterations) is not int or iterations < 0:
        raise ValueError("nonnegative integer iterations required")
    angle = _angle(degree, padded)
    return sin((2*iterations+1)*angle)/sqrt(degree) if degree else 0.0


def geometric_kernel(left_degree: int, right_degree: int, padded: int) -> Fraction:
    """Exact rational infinite-time kernel; no trigonometric rounding."""
    for degree in (left_degree, right_degree):
        if type(degree) is not int or not 0 <= degree <= padded:
            raise ValueError("degree outside support domain")
    schedule = schedule_certificate(padded)
    if not left_degree or not right_degree:
        return Fraction(0)
    x, y = Fraction(left_degree, padded), Fraction(right_degree, padded)
    a, rho = schedule["stop_probability"]**2, schedule["rho"]
    common = a+4*rho*(x+y-2*x*y)
    denominator = common**2-64*rho*rho*x*y*(1-x)*(1-y)
    return a/Fraction(padded)*(a+8*rho-4*rho*(x+y))/denominator


def sampler_certificate(n: int, width: int, tail_bits: int = 16) -> dict:
    family = balanced_certificate(n, width)
    padded = 1 << (family["supports"]-1).bit_length()
    row = schedule_certificate(padded, tail_bits)
    cap = min(8, padded//2)
    # Remove oriented edges incident to high-degree vertices, without an oracle
    # that identifies these vertices. Positivity lets us ignore them in the bound.
    good_edges = max(Fraction(0), family["mean_degree"]-2*family["degree_second_moment"]/cap)
    kernel_lower = Fraction(1, (1+8*cap)**2)
    survival = max(Fraction(0), 1-Fraction(family["radius"], n))
    row.update({"n": n, "width": width, "weight": family["per_block_weight"],
                "supports": family["supports"], "list_length": family["each_list_length"],
                "vertex_marking_used": False, "degree_cap_for_analysis_only": cap,
                "mean_degree": family["mean_degree"], "second_degree_moment": family["degree_second_moment"],
                "bounded_degree_oriented_mass_lower": good_edges,
                "bounded_degree_kernel_lower": kernel_lower,
                "support_survival_lower": survival,
                "clean_signal_lower": good_edges*kernel_lower-row["tail_probability_upper"],
                "prelabel_fault_signal_lower": good_edges*kernel_lower*survival-row["tail_probability_upper"],
                "log2_mean_predicate_calls_upper": log2(row["mean_reversible_predicate_calls_upper"]),
                "workspace_bound": "poly(m,n,log(1/tail)); index, mask, modular arithmetic, unranking and orientation registers; no list/history over Grover iterations",
                "uniform_support_reflection_not_unknown_state_reflection": True,
                "quantum_counting_required": False, "unique_neighbor_oracle_required": False,
                "explicit_list_required": False, "coherent_ram_assumed": False,
                "polynomial_time_claimed": False, "gate_export_implemented": False,
                "analytical_count_not_large_instance_execution": True})
    return row


def explicit_grover_rows(program: BalancedPairingProgram, iterations: int):
    """Dense finite diagnostic, NOT the scalable storage implementation."""
    size = 1 << len(program.labels)
    padded = 1 << (program.list_length**2-1).bit_length()
    if size*padded > 4096 or type(iterations) is not int or not 0 <= iterations <= 1024:
        raise ValueError("finite diagnostic budget exceeded")
    marked = np.array([[edge_predicate(program, b, j) for j in range(padded)] for b in range(size)])
    state = np.full((size, padded), 1/sqrt(padded))
    for _ in range(iterations):
        state *= np.where(marked, -1, 1)
        state = 2*state.mean(axis=1, keepdims=True)-state
    return state, marked


def physical_edge_readout(program: BalancedPairingProgram, iterations: int,
                          secret: int, eta: float = 1.0,
                          fault_law: dict[int, Fraction] | None = None) -> dict:
    state, marked = explicit_grover_rows(program, iterations)
    size, padded = state.shape
    if size*padded > 128 or not 0 <= eta <= 1:
        raise ValueError("full density-matrix control budget or noise range exceeded")
    if fault_law is not None and (sum(fault_law.values()) != 1
            or any(type(mask) is not int or not 0 <= mask < size or p < 0 for mask, p in fault_law.items())):
        raise ValueError("invalid classical fault-mask distribution")
    def survival(support):
        marginal = sum(p for mask, p in fault_law.items() if not mask & support) if fault_law is not None else 1
        return eta**support.bit_count()*float(marginal)
    residues = np.array([sum(a for i, a in enumerate(program.labels) if b & (1 << i))
                         % (1 << program.n) for b in range(size)])
    psi = np.exp(2j*np.pi*secret*residues/(1 << program.n))/sqrt(size)
    rho = np.outer(psi, psi.conj())
    for b in range(size):
        for c in range(size):
            rho[b, c] *= survival(b ^ c)
    heralded = np.zeros((2*size*padded, size))
    degrees = marked.sum(axis=1).tolist()
    predicted = 0.0
    for b in range(size):
        for j in range(padded):
            if not marked[b, j]:
                continue
            support = support_from_index(program, j)
            orientation = int(bool(b & (support & -support)))
            representative = b ^ (support if orientation else 0)
            heralded[2*(representative*padded+j)+orientation, b] = state[b, j]
            predicted += (marked_amplitude(degrees[b], padded, iterations)
                          * marked_amplitude(degrees[b ^ support], padded, iterations)
                          * survival(support)/size)
    output = heralded@rho@heralded.T
    observed = float(sum(output[i, i ^ 1] for i in range(len(output))).real)
    source_success = float(np.sum(state*state*marked)/size)
    return {"iterations": iterations, "secret": secret, "eta": eta,
            "observed_signal": observed, "predicted_signal": (-1)**secret*predicted,
            "signal_residual": abs(observed-(-1)**secret*predicted),
            "success_residual": abs(float(np.trace(output).real)-source_success),
            "grover_row_norm_residual": float(np.max(abs(np.sum(state*state, axis=1)-1))),
            "heralded_probability": source_success,
            "conditional_normalization_used": False}


def finite_geometric_readout(program: BalancedPairingProgram, tail_bits: int = 16) -> dict:
    _, marked = explicit_grover_rows(program, 0)
    size, padded = marked.shape
    schedule = schedule_certificate(padded, tail_bits)
    degrees = marked.sum(axis=1).tolist()
    infinite = Fraction(0)
    for b in range(size):
        for j in range(padded):
            if marked[b, j]:
                c = b ^ support_from_index(program, j)
                infinite += geometric_kernel(degrees[b], degrees[c], padded)/size
    # Repeated oracle/reflection dynamics, not the closed-form amplitude formula.
    state = np.full((size, padded), 1/sqrt(padded))
    probability, finite = float(schedule["stop_probability"]), 0.0
    rho = float(schedule["rho"])
    for _ in range(schedule["cutoff"]):
        signal = sum(state[b, j]*state[b ^ support_from_index(program, j), j]/size
                     for b in range(size) for j in range(padded) if marked[b, j])
        finite += probability*signal
        state *= np.where(marked, -1, 1)
        state = 2*state.mean(axis=1, keepdims=True)-state
        probability *= rho
    tail = rho**schedule["cutoff"]
    finite = float(finite)
    return {"infinite_geometric_signal": infinite, "truncated_signal": finite,
            "actual_abort_probability": tail, "tail_error": abs(finite-float(infinite)),
            "checks": {"kernel_signal_nonnegative": infinite >= -1e-12,
                       "tail_error_bounded": abs(finite-float(infinite)) <= tail+1e-12,
                       "abort_bound": tail <= float(schedule["tail_probability_upper"])+1e-12},
            "selected_calibration_not_natural_source_estimate": True}


def natural_degree_control() -> dict:
    """Exhaust an entire small unmarked source, not selected successful labels."""
    first = second = good = 0
    count, cap = 4**4*16, 2
    for labels in product(range(4), repeat=4):
        program = BalancedPairingProgram(labels, 2, 1, (), 0)
        _, marked = explicit_grover_rows(program, 0)
        degrees = marked.sum(axis=1).tolist()
        first += sum(degrees)
        second += sum(d*d for d in degrees)
        good += sum(degrees[b] <= cap and degrees[b ^ support_from_index(program, j)] <= cap
                    for b in range(16) for j in range(4) if marked[b, j])
    family = balanced_certificate(2, 4)
    return {"n": 2, "width": 4, "source_assignments": count,
            "mean_degree": Fraction(first, count), "second_moment": Fraction(second, count),
            "degree_cap": cap, "bounded_degree_edge_mass": Fraction(good, count),
            "checks": {"first_moment": Fraction(first, count) == family["mean_degree"],
                       "second_moment": Fraction(second, count) == family["degree_second_moment"],
                       "edge_mass_bound": Fraction(good, count) >= family["mean_degree"]-2*family["degree_second_moment"]/cap}}


def build_coherent_edge_audit() -> dict:
    programs = [BalancedPairingProgram((0, 1, 1, 1), 2, 1, (), 0),
                BalancedPairingProgram((1, 1, 1, 1), 2, 1, (), 0),
                BalancedPairingProgram((1, 0, 1, 0), 2, 1, (0,), 1)]
    physical = [physical_edge_readout(p, t, secret, eta)
                for p in programs for t in (0, 1, 2, 3) for secret in range(4) for eta in (1., .75)]
    geometric = [finite_geometric_readout(p) for p in programs]
    correlated = [physical_edge_readout(programs[0], t, secret, fault_law=law)
                  for law in ({0: Fraction(3, 4), 15: Fraction(1, 4)},
                              {1 << i: Fraction(1, 4) for i in range(4)})
                  for t in (0, 2, 3) for secret in range(4)]
    kernels = [{"padded_supports": size,
                "minimum_entry": min(geometric_kernel(d, e, size) for d in range(1, size+1) for e in range(1, size+1)),
                "singleton_kernel": schedule_certificate(size)["singleton_kernel"]}
               for size in (2, 4, 8, 16, 32)]
    negative = physical_edge_readout(programs[0], 2, 0)
    scaling = [sampler_certificate(n, 2*n) for n in (8, 16, 32, 64, 128, 256, 512)]
    natural = natural_degree_control()
    failures = sum(max(r["signal_residual"], r["success_residual"], r["grover_row_norm_residual"]) > 1e-10 for r in physical)
    failures += sum(max(r["signal_residual"], r["success_residual"]) > 1e-10 for r in correlated)
    failures += sum(not all(r["checks"].values()) for r in geometric)
    failures += sum(r["minimum_entry"] < -1e-12 for r in kernels)
    failures += not abs(negative["observed_signal"]+Fraction(1, 4)) < 1e-12
    failures += not all(natural["checks"].values())
    return _jsonable({"physical_controls": physical, "geometric_controls": geometric,
                      "correlated_noise_controls": correlated,
                      "natural_degree_control": natural,
                      "kernel_controls": kernels, "fixed_time_sign_counterexample": negative,
                      "scaling": scaling, "control_failures": failures,
                      "status": "derived-list-free-edge-readout-exponential-time-review-pending",
                      "contract": {
                          "algorithm": "Prepare uniform padded support index, shared public geometric Grover time, herald valid edge, canonicalize with the retained coherent support index, and measure orientation X. Abort tails count as zero.",
                          "kernel": "K(d,e)=[f(theta_d-theta_e)-f(theta_d+theta_e)]/(2sqrt(de)), f(x)=(1-rho)^2 cos(x)/((1-rho)^2+4rho sin(x)^2); f decreases on [0,pi], so K>=0.",
                          "source_law": "Independent uniform labels, capped balanced support family, NO affine vertex filter; common independent public iteration count.",
                          "signal": "Source-averaged signed signal >=1/25350-2^-tail_bits for m=2n,n>=6 under the declared prelabel classical-fault marginals <=1/n. Constant positive for tail_bits>=16. Uses degree moments and kernel positivity, not a low-degree classifier or isolated-edge oracle.",
                          "noise_scope": "Nonnegative support-survival coherences from the existing prelabel classical-mask gauge, not arbitrary quantum noise or independent-batch guarantees.",
                          "resources": "Per parity-readout attempt: O(2^(n/2)*poly(n,log(1/tail))) time and polynomial coherent workspace. Dense small-state arrays are diagnostics, not required quantum storage. Fresh-batch repetition and full-secret recovery need separate accounting.",
                          "no_quantum_counting_or_unique_partner_needed": True,
                          "unknown_input_state_reflection_used": False,
                          "quantum_gate_export_implemented": False, "polynomial_time_claimed": False,
                          "speedup_claim_allowed": False, "novelty_established": False,
                          "independently_reviewed": False},
                      "literature": [{"url": "https://arxiv.org/abs/quant-ph/9605034",
                                      "role": "Prior Grover multi-solution amplitudes and randomized search. The shared-geometric interference argument is locally derived, not attributed novelty."}]})
