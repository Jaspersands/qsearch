"""Physical interfaces for DCP half-period pairings and permutation readouts.

These are conditional circuit constructions, not efficient relation finders.
Finite truth tables are controls and must never be charged as free oracles.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from math import comb, log2
import random
from typing import Sequence

import numpy as np
from scipy.optimize import linear_sum_assignment


def _instance(labels: Sequence[int], modulus: int, max_width: int = 16) -> tuple[int, ...]:
    if type(modulus) is not int or not 2 <= modulus <= 1 << 30 or modulus & (modulus-1):
        raise ValueError("finite controls require a power-of-two modulus in [2,2^30]")
    if not 1 <= len(labels) <= max_width or any(type(a) is not int for a in labels):
        raise ValueError(f"integer labels required, with width 1..{max_width}")
    return tuple(a % modulus for a in labels)


def subset_residues(labels: Sequence[int], modulus: int) -> np.ndarray:
    labels = _instance(labels, modulus)
    result = [0]
    for a in labels:
        result += [(value+a) % modulus for value in result]
    return np.asarray(result, dtype=np.int64)


def _proposal(table: Sequence[int | None], width: int) -> tuple[int | None, ...]:
    size = 1 << width
    if len(table) != size or any(value is not None and
                                 (type(value) is not int or not 0 <= value < size) for value in table):
        raise ValueError("proposal needs one in-range integer or None per assignment")
    return tuple(table)


def matching_profile(labels: Sequence[int], modulus: int, table: Sequence[int | None]) -> dict:
    labels = _instance(labels, modulus)
    table = _proposal(table, len(labels))
    residues = subset_residues(labels, modulus)
    valid = [b for b, c in enumerate(table) if c is not None
             and (int(residues[c])-int(residues[b])) % modulus == modulus//2]
    mutual = [b for b in valid if table[table[b]] == b]
    distances = Counter((b ^ table[b]).bit_count() for b in mutual)
    return {"valid_proposal_count": len(valid), "mutual_assignment_count": len(mutual),
            "assignment_count": len(table), "valid_proposal_fraction": len(valid)/len(table),
            "heralded_success_fraction": len(mutual)/len(table),
            "accepted_assignments": mutual,
            "accepted_hamming_histogram": dict(sorted(distances.items())),
            "pairs": [(b, table[b]) for b in mutual if b < table[b]]}


def canonical_proposal(labels: Sequence[int], modulus: int) -> tuple[int | None, ...]:
    """Exponential reference oracle, explicitly NOT a candidate implementation."""
    residues = subset_residues(labels, modulus)
    first = {}
    for b, residue in enumerate(residues):
        first.setdefault(int(residue), b)
    return tuple(first.get((int(residue)+modulus//2) % modulus) for residue in residues)


def reference_matching_proposal(labels: Sequence[int], modulus: int, eta: float = 1.0,
                                optimize_noise: bool = False) -> tuple[int | None, ...]:
    """Exponential fiber-table reference. Assignment costs/lookup are NOT free."""
    labels = _instance(labels, modulus, max_width=10)
    if not 0 <= eta <= 1:
        raise ValueError("invalid coherence parameter")
    fibers = {}
    for b, residue in enumerate(subset_residues(labels, modulus)):
        fibers.setdefault(int(residue), []).append(b)
    table = [None]*(1 << len(labels))
    for residue, left in fibers.items():
        if residue >= modulus//2:
            continue
        right = fibers.get(residue+modulus//2, [])
        if not right:
            continue
        if optimize_noise:
            costs = np.array([[-eta**((b ^ c).bit_count()) for c in right] for b in left])
            rows, cols = linear_sum_assignment(costs)
            pairs = ((left[i], right[j]) for i, j in zip(rows, cols))
        else:
            pairs = zip(left, right)
        for b, c in pairs:
            table[b], table[c] = c, b
    return tuple(table)


def mutual_circuit_maps(labels: Sequence[int], modulus: int, table: Sequence[int | None]) -> dict:
    """Six XOR-oracle calls; every listed operation is a full-space permutation.

    Registers (low to high): x[m], u[m+1], v[m+1], accept, orientation.
    A valid image is encoded as 2^m+image; None is encoded as zero.
    """
    labels = _instance(labels, modulus, max_width=4)
    m = len(labels)
    table = _proposal(table, m)
    size, mask = 1 << m, (1 << m)-1
    u_shift, v_shift, a_shift, e_shift = m, 2*m+1, 3*m+2, 3*m+3
    encoded = np.array([0 if c is None else size+c for c in table], dtype=np.int64)
    residues = subset_residues(labels, modulus)
    identity = np.arange(1 << (3*m+4), dtype=np.int64)
    oracle_calls = 0

    def oracle(indices: np.ndarray, input_shift: int, output_shift: int) -> np.ndarray:
        nonlocal oracle_calls
        oracle_calls += 1
        return indices ^ (encoded[(indices >> input_shift) & mask] << output_shift)

    accept = oracle(oracle(identity, 0, u_shift), u_shift, v_shift)
    x, u, v = accept & mask, (accept >> u_shift) & (2*size-1), (accept >> v_shift) & (2*size-1)
    condition = ((u >= size) & (v >= size) & ((v & mask) == x)
                 & ((residues[u & mask]-residues[x]) % modulus == modulus//2))
    accept ^= condition.astype(np.int64) << a_shift
    accept = oracle(oracle(accept, u_shift, v_shift), 0, u_shift)

    ordered = oracle(identity, 0, u_shift)
    x, c = ordered & mask, (ordered >> u_shift) & mask
    ordered ^= (x > c).astype(np.int64) << e_shift
    swap = ((ordered >> e_shift) & 1) * (x ^ c)
    ordered ^= swap ^ (swap << u_shift)
    ordered = oracle(ordered, 0, u_shift)
    return {"accept": accept, "ordered": ordered, "accept_shift": a_shift,
            "orientation_shift": e_shift, "oracle_calls": oracle_calls, "width": m}


def physical_pair_isometry(labels: Sequence[int], modulus: int, table: Sequence[int | None]) -> tuple[np.ndarray, dict]:
    maps = mutual_circuit_maps(labels, modulus, table)
    m, size = maps["width"], 1 << maps["width"]
    profile = matching_profile(labels, modulus, table)
    matrix = np.zeros((2*size, size), dtype=np.int64)
    clean = True
    for b in range(size):
        accepted = int(maps["accept"][b])
        if not (accepted >> maps["accept_shift"]) & 1:
            continue
        output = int(maps["ordered"][accepted])
        r, e = output & (size-1), (output >> maps["orientation_shift"]) & 1
        clean &= output == r + (1 << maps["accept_shift"]) + (e << maps["orientation_shift"])
        matrix[2*r+e, b] = 1
    projector = np.zeros(size, dtype=np.int64)
    projector[profile["accepted_assignments"]] = 1
    checks = {
        "accept_full_space_permutation": np.array_equal(np.sort(maps["accept"]), np.arange(len(maps["accept"]))),
        "ordering_full_space_permutation": np.array_equal(np.sort(maps["ordered"]), np.arange(len(maps["ordered"]))),
        "accepted_workspace_exactly_clean": bool(clean),
        "accepted_isometry_exact": np.array_equal(matrix.T@matrix, np.diag(projector)),
    }
    return matrix, checks


def dephased_source(labels: Sequence[int], modulus: int, secret: int, eta: float = 1.0,
                    measure_low_sum: bool = False) -> np.ndarray:
    labels = _instance(labels, modulus, max_width=8)
    if not 0 <= eta <= 1:
        raise ValueError("dephasing coherence eta must lie in [0,1]")
    residues = subset_residues(labels, modulus)
    phase = np.exp(2j*np.pi*(((secret % modulus)*residues) % modulus)/modulus)
    size = len(residues)
    attenuation = np.array([[eta**((b ^ c).bit_count()) for c in range(size)] for b in range(size)])
    result = np.outer(phase, phase.conj())*attenuation/size
    if measure_low_sum:
        low = residues % (modulus//2)
        result *= low[:, None] == low[None, :]
    return result


def hamming_visibility(histogram: dict[int, int], size: int, eta: float) -> float:
    if not 0 <= eta <= 1 or size <= 0:
        raise ValueError("invalid visibility parameters")
    return sum(count*eta**weight for weight, count in histogram.items())/size


def correlated_fault_source(labels: Sequence[int], modulus: int, secret: int,
                            fault_law: dict[int, Fraction]) -> np.ndarray:
    """Gauged prelabel classical mask mixtures, not arbitrary quantum noise.

    Matrix element (b,c) survives precisely if no fault hits b xor c. The
    entire mask law is charged input for these finite controls, not an oracle.
    """
    labels = _instance(labels, modulus, max_width=8)
    size = 1 << len(labels)
    if (not fault_law or any(type(mask) is not int or not 0 <= mask < size
                            or not isinstance(probability, Fraction) or probability < 0
                            for mask, probability in fault_law.items())
            or sum(fault_law.values()) != 1):
        raise ValueError("fault law must be an exact probability distribution on masks")
    survival = [sum(probability for faults, probability in fault_law.items() if not faults & support)
                for support in range(size)]
    attenuation = np.array([[float(survival[b ^ c]) for c in range(size)] for b in range(size)])
    return dephased_source(labels, modulus, secret)*attenuation


def correlated_noise_controls() -> list[dict]:
    labels, modulus, table = (1, 3), 4, (3, 2, 1, 0)
    matrix, _ = physical_pair_isometry(labels, modulus, table)
    profile = matching_profile(labels, modulus, table)
    observable = np.kron(np.eye(4), [[0, 1], [1, 0]])
    rows = []
    for name, law in (
        ("all-or-none-faults", {0: Fraction(3, 4), 3: Fraction(1, 4)}),
        ("exactly-one-fault", {1: Fraction(1, 2), 2: Fraction(1, 2)}),
        ("rare-disjoint-faults", {0: Fraction(7, 8), 1: Fraction(1, 16), 2: Fraction(1, 16)}),
    ):
        marginals = [sum(probability for mask, probability in law.items() if mask & (1 << i))
                     for i in range(2)]
        target, lower = Fraction(0), Fraction(0)
        for b in profile["accepted_assignments"]:
            support = b ^ table[b]
            target += sum(probability for mask, probability in law.items() if not mask & support)/4
            lower += max(Fraction(0), 1-sum(marginals[i] for i in range(2) if support & (1 << i)))/4
        residual = 0.0
        for secret in range(modulus):
            source = correlated_fault_source(labels, modulus, secret, law)
            output = matrix@source@matrix.T
            residual = max(residual, abs(float(np.trace(observable@output).real)-(-1)**secret*float(target)),
                           abs(float(np.trace(output).real)-profile["heralded_success_fraction"]))
        rows.append({"name": name, "weighted_signal": float(target),
                     "marginal_union_lower": float(lower), "maximum_residual": residual,
                     "incorrect_independent_model_signal": hamming_visibility(profile["accepted_hamming_histogram"], 4, float(1-marginals[0])),
                     "fault_law": {str(mask): {"numerator": p.numerator, "denominator": p.denominator}
                                   for mask, p in law.items()}})
    return rows


def evaluate_mutual_program(labels: Sequence[int], modulus: int, table: Sequence[int | None]) -> dict:
    profile = matching_profile(labels, modulus, table)
    matrix, checks = physical_pair_isometry(labels, modulus, table)
    x_readout = np.kron(np.eye(len(table)), np.array([[0, 1], [1, 0]]))
    rows = []
    for eta in (1.0, .75, 0.0):
        target = hamming_visibility(profile["accepted_hamming_histogram"], len(table), eta)
        for secret in range(modulus):
            output = matrix@dephased_source(labels, modulus, secret, eta)@matrix.T
            mass = float(np.trace(output).real)
            signal = float(np.trace(x_readout@output).real)
            rows.append({"eta": eta, "secret": secret, "accepted_mass": mass,
                         "signed_output_bias": signal,
                         "success_residual": abs(mass-profile["heralded_success_fraction"]),
                         "signal_residual": abs(signal-(-1)**secret*target)})
    return {"profile": profile, "physical_checks": checks, "rows": rows,
            "maximum_residual": max(max(row["success_residual"], row["signal_residual"]) for row in rows),
            "clean_xor_oracle_calls": 6,
            "lookup_table_is_efficient_implementation": False}


def evaluate_flagged_permutation(labels: Sequence[int], modulus: int, permutation: Sequence[int]) -> dict:
    labels = _instance(labels, modulus, max_width=8)
    table = _proposal(permutation, len(labels))
    size = len(table)
    if any(c is None for c in table) or sorted(table) != list(range(size)):
        raise ValueError("a clean permutation, not a many-to-one function, is required")
    residues = subset_residues(labels, modulus)
    valid = [(int(residues[c])-int(residues[b])) % modulus == modulus//2 for b, c in enumerate(table)]
    histogram = dict(sorted(Counter((b ^ table[b]).bit_count() for b in range(size) if valid[b]).items()))
    # Branch 0 has flag 1; branch 1 has flag q(b) and data P(b).
    isometry = np.zeros((4*size, size), complex)
    for b, c in enumerate(table):
        isometry[size+b, b] = 1/np.sqrt(2)
        isometry[2*size+int(valid[b])*size+c, b] = 1/np.sqrt(2)
    x_readout = np.kron(np.array([[0, 1], [1, 0]]), np.eye(2*size))
    rows = []
    for eta in (1.0, .75, 0.0):
        target = hamming_visibility(histogram, size, eta)
        for secret in range(modulus):
            output = isometry@dephased_source(labels, modulus, secret, eta)@isometry.conj().T
            signal = float(np.trace(x_readout@output).real)
            rows.append({"eta": eta, "secret": secret, "signal": signal,
                         "residual": abs(signal-(-1)**secret*target)})
    return {"valid_edge_fraction": sum(valid)/size, "valid_hamming_histogram": histogram,
            "isometry_residual": float(np.max(np.abs(isometry.conj().T@isometry-np.eye(size)))),
            "rows": rows, "maximum_residual": max(row["residual"] for row in rows),
            "requires_efficient_clean_permutation_and_inverse": True,
            "mutuality_required": False, "full_decoder_constructed": False}


def gauge_control(modulus: int = 8) -> dict:
    """Average every (old label, random X flip), retaining the updated label."""
    _instance((0,), modulus)
    x = np.array([[0, 1], [1, 0]], complex)
    worst_good, worst_bad, adaptive_gap = 0.0, 0.0, 0.0
    for secret in range(modulus):
        for bit in (0, 1):
            good = [np.zeros((2, 2), complex) for _ in range(modulus)]
            bad = [np.zeros((2, 2), complex) for _ in range(modulus)]
            adaptive = [np.zeros((2, 2), complex) for _ in range(modulus)]
            for label in range(modulus):
                vector = np.array([1, np.exp(2j*np.pi*secret*label/modulus)])/np.sqrt(2)
                for flip in (0, 1):
                    updated = (-label if flip else label) % modulus
                    unitary = x if flip else np.eye(2)
                    state = unitary@vector
                    good[updated] += np.outer(state, state.conj())/2
                    bad[updated][bit ^ flip, bit ^ flip] += .5
                    chosen = int(label >= modulus//2) ^ flip
                    adaptive[updated][chosen, chosen] += .5
            for label in range(modulus):
                expected = dephased_source((label,), modulus, secret)
                worst_good = max(worst_good, float(np.max(np.abs(good[label]-expected))))
                worst_bad = max(worst_bad, float(np.max(np.abs(bad[label]-np.eye(2)/2))))
                adaptive_gap = max(adaptive_gap, float(np.max(np.abs(adaptive[label]-np.eye(2)/2))))
    return {"modulus": modulus, "maximum_good_state_residual": worst_good,
            "maximum_prelabel_bad_bit_residual": worst_bad,
            "postlabel_adversarial_bit_counterexample_gap": adaptive_gap,
            "scope": "Bad basis bits and fault status fixed before uniform Fourier labels; independent faults give product dephasing. Correlated faults require their joint law."}


def local_mass_bound(n: int, m: int, radius: int) -> Fraction:
    if any(type(value) is not int for value in (n, m, radius)) or n < 1 or m < 1 or not 0 <= radius <= m:
        raise ValueError("invalid local matching dimensions")
    return min(Fraction(1), Fraction(sum(comb(m, k) for k in range(1, radius+1)), 1 << n))


def noise_mass_envelope(n: int, m: int, eta: Fraction) -> dict:
    """Exact relaxation for natural-label-averaged half-period edge mass.

    At distance w, expected accepted mass is at most C(m,w)/2^n. Its total
    is at most one. Fill shortest distances first since eta^w is decreasing.
    The relaxation grants an unlimited adaptive matcher, not a realizable one.
    """
    local_mass_bound(n, m, 0)
    if not isinstance(eta, Fraction) or not 0 <= eta <= 1:
        raise ValueError("eta must be an exact Fraction in [0,1]")
    remaining, upper = Fraction(1), Fraction(0)
    allocations = []
    for weight in range(1, m+1):
        mass = min(remaining, Fraction(comb(m, weight), 1 << n))
        upper += mass*eta**weight
        allocations.append((weight, mass))
        remaining -= mass
        if not remaining:
            break
    return {"upper": upper, "allocations": allocations, "unallocated_mass": remaining,
            "capacity_saturating_weight": None if remaining else allocations[-1][0]}


def build_pairing_controls() -> dict:
    controls = []
    for labels, modulus in (((1, 3), 4), ((2, 0), 4), ((1, 2, 5), 8)):
        size = 1 << len(labels)
        proposals = {"complement": tuple(b ^ (size-1) for b in range(size)),
                     "canonical-oracle-control": canonical_proposal(labels, modulus),
                     "cyclic-increment": tuple((b+1) % size for b in range(size))}
        for name, table in proposals.items():
            controls.append({"name": name, "labels": labels, "modulus": modulus,
                             **evaluate_mutual_program(labels, modulus, table)})
    permutation_controls = [evaluate_flagged_permutation((2, 0), 4, (1, 2, 3, 0)),
                            evaluate_flagged_permutation((1, 2, 5), 8, tuple((b+1) % 8 for b in range(8)))]
    rng = random.Random(20260922)
    canonical_rows = []
    for width in (4, 6, 8, 10, 12):
        profiles = []
        for _ in range(8):
            labels = tuple(rng.randrange(16) for _ in range(width))
            profiles.append(matching_profile(labels, 16, canonical_proposal(labels, 16)))
        canonical_rows.append({"n": 4, "samples": width, "trials": len(profiles),
                               "mean_valid_proposal_fraction": sum(p["valid_proposal_fraction"] for p in profiles)/len(profiles),
                               "mean_heralded_mass": sum(p["heralded_success_fraction"] for p in profiles)/len(profiles),
                               "canonical_mass_upper_bound": min(1, 16/(1 << width)),
                               "reference_preprocessing_assignments": 1 << width,
                               "efficient_candidate": False})
    references = []
    for width in (6, 8, 10):
        labels = tuple(rng.randrange(16) for _ in range(width))
        row = {"labels": labels, "modulus": 16, "eta": .75,
               "reference_preprocessing_assignments": 1 << width, "efficient_candidate": False}
        for name, table in (
            ("canonical", canonical_proposal(labels, 16)),
            ("rank-paired", reference_matching_proposal(labels, 16)),
            ("noise-weighted-assignment", reference_matching_proposal(labels, 16, .75, True)),
        ):
            profile = matching_profile(labels, 16, table)
            row[name] = {"mass": profile["heralded_success_fraction"],
                         "noise_weighted_mass": hamming_visibility(profile["accepted_hamming_histogram"], len(table), .75),
                         "hamming_histogram": profile["accepted_hamming_histogram"]}
        counts = Counter(subset_residues(labels, 16))
        row["noise_assignment_cost_matrix_entries"] = sum(counts[s]*counts[s+8] for s in range(8))
        references.append(row)
    scaling = []
    for n in (64, 128, 256, 512):
        m, radius = n*n, n.bit_length()-1
        cap = local_mass_bound(n, m, radius)
        scaling.append({"n": n, "samples": m, "radius": radius,
                        "mean_local_mass_upper": {"numerator": cap.numerator, "denominator": cap.denominator},
                        "log2_mean_local_mass_upper": log2(cap.numerator)-log2(cap.denominator),
                        "all_good_batch_log2_probability": m*log2(1-1/n),
                        "radius_noise_visibility": (1-1/n)**radius,
                        "conditional_visibility_is_not_source_coverage": True})
    envelopes = []
    for n in (64, 128, 256, 512, 1024, 2048, 4096):
        for name, eta in (("constant-quarter-fault", Fraction(3, 4)),
                          ("inverse-n-fault", Fraction(n-1, n))):
            bound = noise_mass_envelope(n, n*n, eta)
            upper = bound["upper"]
            envelopes.append({"n": n, "samples": n*n, "noise_model": name,
                              "eta": {"numerator": eta.numerator, "denominator": eta.denominator},
                              "weighted_mass_upper": {"numerator": upper.numerator, "denominator": upper.denominator},
                              "log2_weighted_mass_upper": log2(upper.numerator)-log2(upper.denominator),
                              "capacity_saturating_weight": bound["capacity_saturating_weight"],
                              "achievability_claimed": False})
    gauge = gauge_control()
    correlated = correlated_noise_controls()
    failures = sum(not all(row["physical_checks"].values()) or row["maximum_residual"] > 1e-10 for row in controls)
    failures += sum(row["maximum_residual"] > 1e-10 or row["isometry_residual"] > 1e-10 for row in permutation_controls)
    failures += int(gauge["maximum_good_state_residual"] > 1e-10 or gauge["maximum_prelabel_bad_bit_residual"] > 1e-10)
    failures += sum(row["maximum_residual"] > 1e-10 or row["marginal_union_lower"] > row["weighted_signal"]+1e-12 for row in correlated)
    return {"mutual_controls": controls, "permutation_controls": permutation_controls,
            "gauge_control": gauge, "canonical_density_controls": canonical_rows,
            "correlated_noise_controls": correlated,
            "exponential_reference_matchings": references,
            "scaling": scaling, "noise_mass_envelopes": envelopes, "control_failures": failures,
            "contract": {
                "mutual_success": "|{b:F(F(b))=b and f(F(b))-f(b)=N/2}|/2^m",
                "mutual_clean_xor_oracle_calls": 6,
                "permutation_signal": "2^-m sum_{b:delta f=N/2} eta^Hamming(b,P(b))",
                "permutation_access": "Supplied efficient clean controlled P and P inverse, not just forward classical evaluation.",
                "gauge": "Apply independent random X flips and negate corresponding labels; discard old labels and flip coins before choosing a program from updated labels and fresh independent randomness only.",
                "noise_scope": "Pre-Fourier classical mask mixtures give survival Pr(fault mask misses b xor c); independent faults give eta^weight. Postlabel corruption or general quantum channels are not covered.",
                "correlated_noise_lower_bound": "With per-coordinate fault marginal <=epsilon, moves of width <=r have signal >=max(0,1-r*epsilon) times source coverage. Fresh batches for estimation must have the required independence or conditional guarantees.",
                "scaling_requirement": "An efficient program must achieve inverse-polynomial NATURAL LABEL-AVERAGED weighted edge mass.",
                "local_mass_bound": "E_y accepted mass at Hamming distance <=r is <=sum_{j=1}^r C(m,j)/2^n, even for label/input-adaptive proposals.",
                "noise_mass_envelope": "Maximize sum_w eta^w p_w subject to 0<=p_w<=C(m,w)/2^n and sum_w p_w<=1. This bounds only the declared pair/permutation readouts, not arbitrary DCP algorithms.",
                "constant_noise_limit": "For m=poly(n) and fixed eta<1 the envelope is superpolynomially small; eta=1-1/n is not excluded. A vacuous upper bound is not constructive evidence.",
                "novelty_established": False, "independently_reviewed": False,
                "gate_export_implemented": False, "polynomial_decoder_constructed": False}}
