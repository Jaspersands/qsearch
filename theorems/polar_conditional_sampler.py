"""Exact-arithmetic polar SC shaping as a classical Gibbs competitor.

The sampler ignores future frozen constraints. Small native TV diagnostics
separate average-syndrome guarantees from worst-case signs. No quantum no-go.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from math import log2
from pathlib import Path
import random
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.bpqm_gibbs_frontier import integer

REPORT = ROOT/"research/classical_baselines/polar_conditional_sampler.json"


def _length(N):
    integer(N, "polar block length", 1, 32768)
    if N & (N-1):
        raise ValueError("power-of-two polar length required")


def _probability(p):
    if type(p) not in (int, Fraction, str):
        raise ValueError("exact rational source probability required")
    p = Fraction(p)
    if not 0 < p < 1:
        raise ValueError("strictly positive source probabilities required")
    return p


def transform(word, N):
    """Arikan transform with explicit interleaved inputs; this convention is involutory."""
    _length(N)
    integer(word, "binary polar word", 0, (1 << N)-1)
    if N == 1:
        return word
    even = sum(((word >> (2*j)) & 1) << j for j in range(N//2))
    odd = sum(((word >> (2*j+1)) & 1) << j for j in range(N//2))
    return transform(even ^ odd, N//2) | (transform(odd, N//2) << (N//2))


def syndrome(word, frozen):
    return sum(((word >> i) & 1) << j for j, i in enumerate(frozen))


def _frozen(N, frozen):
    if (type(frozen) is not tuple or tuple(sorted(set(frozen))) != frozen
            or any(type(i) is not int or not 0 <= i < N for i in frozen)):
        raise ValueError("canonical increasing frozen coordinates required")


def check_masks(N, frozen):
    _length(N)
    _frozen(N, frozen)
    images = [transform(1 << j, N) for j in range(N)]
    return tuple(sum(((image >> i) & 1) << j for j, image in enumerate(images)) for i in frozen)


def _prefix_one(priors, prefix, work):
    work["recursive_calls"] += 1
    if len(priors) == 1:
        out = priors[0]
    else:
        half, paired = len(priors)//2, len(prefix)//2
        a = _prefix_one(priors[:half], tuple(prefix[2*j] ^ prefix[2*j+1] for j in range(paired)), work)
        b = _prefix_one(priors[half:], tuple(prefix[2*j+1] for j in range(paired)), work)
        if len(prefix) % 2 == 0:
            out = a*(1-b)+(1-a)*b
        else:
            zero, one = ((1-a)*(1-b), a*b) if prefix[-1] == 0 else (a*(1-b), (1-a)*b)
            out = one/(zero+one)
    work["maximum_fraction_bits"] = max(work["maximum_fraction_bits"], out.numerator.bit_length(), out.denominator.bit_length())
    return out


def prefix_one(N, p, prefix, *, work=None):
    """P(U_i=1 | U_<i), WITHOUT future constraints, in O(N) rational operations."""
    _length(N)
    p = _probability(p)
    if (type(prefix) is not tuple or len(prefix) >= N
            or any(type(b) is not int or b not in (0, 1) for b in prefix)):
        raise ValueError("canonical proper binary prefix required")
    if work is None:
        work = {"recursive_calls": 0, "maximum_fraction_bits": 0}
    return _prefix_one((p,)*N, prefix, work)


def sample(N, p, frozen, target, seed):
    _length(N)
    p = _probability(p)
    _frozen(N, frozen)
    integer(target, "frozen-bit syndrome", 0, (1 << len(frozen))-1)
    integer(seed, "sampler replay seed", 0, (1 << 64)-1)
    rng, prefix, work = random.Random(seed), [], {"recursive_calls": 0, "maximum_fraction_bits": 0}
    fixed = {i: (target >> j) & 1 for j, i in enumerate(frozen)}
    for i in range(N):
        if i in fixed:
            prefix.append(fixed[i])
        else:
            q = prefix_one(N, p, tuple(prefix), work=work)
            prefix.append(int(rng.randrange(q.denominator) < q.numerator))
    u = sum(b << i for i, b in enumerate(prefix))
    e = transform(u, N)
    if syndrome(transform(e, N), frozen) != target:
        raise ArithmeticError("sample fails native polar syndrome")
    exact = frozen == tuple(range(len(frozen))) or p == Fraction(1, 2)
    return {"noise_word_hex": hex(e), "polar_word_hex": hex(u), "seed": seed, "target": target,
            "recursive_work": work, "exact_rational_Bernoulli_draws": N-len(frozen),
            "future_frozen_constraints_in_prefix_conditionals": False,
            "native_conditional_distribution_certified": exact,
            "exactness_reason": "PREFIX_CONSTRAINTS_OR_FAIR_INDEPENDENT_SOURCE" if exact else None,
            "unconditional_source_table_materialized": False}


def sample_gibbs(N, overlap, frozen, signs, seed):
    """Sample a kernel word with weight proportional to product(1+c*(-1)^(y+J))."""
    _length(N)
    if type(overlap) not in (int, Fraction, str):
        raise ValueError("exact rational overlap required")
    c = Fraction(overlap)
    if not 0 <= c < 1:
        raise ValueError("overlap in [0,1) required")
    integer(signs, "public clause signs", 0, (1 << N)-1)
    target = syndrome(transform(signs, N), frozen)
    out = sample(N, (1-c)/2, frozen, target, seed)
    y = int(out["noise_word_hex"], 16) ^ signs
    checks = check_masks(N, frozen)
    if any((h & y).bit_count() % 2 for h in checks):
        raise ArithmeticError("classical Gibbs word outside the native code kernel")
    return {**out, "Gibbs_kernel_word_hex": hex(y), "public_clause_signs_hex": hex(signs),
            "channel_overlap": str(c), "code_check_masks_hex": list(map(hex, checks)),
            "top_level_polar_transforms_including_native_checks": N+3,
            "native_constraint_dot_products": len(frozen),
            "binary_check_description_bits": N*len(frozen),
            "binary_transform_work_is_additional_to_rational_recursion_counter": True,
            "native_Gibbs_weight": "product_j(1+c*(-1)^(y_j+J_j)); H_F*y=0"}


def _source_law(N, p):
    if N > 10:
        raise ValueError("UNKNOWN: full-law diagnostic capped; scalable sampler is separate")
    out = [Fraction(0)]*(1 << N)
    for e in range(1 << N):
        out[transform(e, N)] = p**e.bit_count()*(1-p)**(N-e.bit_count())
    return out


def source_biases(N, p):
    _length(N)
    p = _probability(p)
    law = _source_law(N, p)
    biases = []
    for i in range(N):
        masses = [[Fraction(0), Fraction(0)] for _ in range(1 << i)]
        for word, probability in enumerate(law):
            masses[word & ((1 << i)-1)][(word >> i) & 1] += probability
        biases.append(sum(abs(a-b)/2 for a, b in masses))
    return tuple(biases)


def native_channel_duality(N, p):
    """Independent small density matrices, NOT a scalable decoder implementation."""
    _length(N)
    p = _probability(p)
    if N > 4:
        raise ValueError("UNKNOWN: native density-matrix calibration cap")
    source = _source_law(N, p)
    source_entropies = []
    for i in range(N):
        masses = [[Fraction(0), Fraction(0)] for _ in range(1 << i)]
        for u, probability in enumerate(source):
            masses[u & ((1 << i)-1)][(u >> i) & 1] += probability
        source_entropies.append(sum(float(a+b)*sum(-float(x/(a+b))*log2(float(x/(a+b)))
                                                  for x in (a, b) if x) for a, b in masses))
    amplitudes = np.array([float(p**e.bit_count()*(1-p)**(N-e.bit_count()))**0.5 for e in range(1 << N)])
    states = np.array([[amplitudes[e]*(-1)**((e & transform(u, N)).bit_count() % 2)
                        for u in range(1 << N)] for e in range(1 << N)])
    entropies, minimum_eigenvalue = [], 0.
    for i in range(N+1):
        selected = states[:, list(range(0, 1 << N, 1 << i))]
        density = selected @ selected.T/selected.shape[1]
        eigenvalues = np.linalg.eigvalsh(density)
        minimum_eigenvalue = min(minimum_eigenvalue, float(min(eigenvalues)))
        if min(eigenvalues) < -1e-12 or abs(sum(eigenvalues)-1) > 1e-12:
            raise ArithmeticError("native CQ calibration density matrix invalid")
        entropies.append(-sum(float(x)*log2(float(x)) for x in eigenvalues if x > 1e-14))
    capacities = [entropies[i]-entropies[i+1] for i in range(N)]
    fidelities, bit_errors = [], []
    for i in range(N):
        zero = list(range(0, 1 << N, 1 << (i+1)))
        one = [u+(1 << i) for u in zero]
        A, B = states[:, zero]/len(zero)**0.5, states[:, one]/len(one)**0.5
        # Purification Gram SVD avoids taking square roots of spurious tiny
        # positive eigenvalues in rank-deficient density matrices.
        fidelities.append(float(sum(np.linalg.svd(A.T @ B, compute_uv=False))))
        difference = A @ A.T-B @ B.T
        bit_errors.append(float((1-sum(abs(np.linalg.eigvalsh(difference)))/2)/2))
    source_magnitudes = [float(2*b) for b in source_biases(N, p)]
    discrepancy = max(abs(a-b) for a, b in zip(capacities, reversed(source_entropies)))
    fidelity_discrepancy = max(abs(a-b) for a, b in zip(fidelities, reversed(source_magnitudes)))
    if discrepancy > 2e-12 or fidelity_discrepancy > 2e-12:
        raise ArithmeticError("native reversed-index PSC/source entropy duality failed")
    return {"positions": N, "source_probability": str(p), "pure_state_overlap": str(1-2*p),
            "native_synthesized_Holevo_information": capacities,
            "source_conditional_entropies": source_entropies,
            "native_synthesized_root_fidelities": fidelities,
            "native_bit_Helstrom_errors": bit_errors,
            "source_mean_absolute_posterior_biases": source_magnitudes,
            "reverse_index_fidelity_max_error": fidelity_discrepancy,
            "reverse_index_identity_max_error": discrepancy,
            "minimum_numerical_density_eigenvalue": minimum_eigenvalue,
            "state_vectors_materialized": 1 << N, "density_matrix_entries": 1 << (2*N),
            "native_density_calibration_is_not_a_quantum_decoder": True,
            "asymptotic_capacity_or_Gibbs_separation_proved_by_numerics": False}


def calibration(N, p, frozen):
    """Enumerate all sources/syndromes; prove the hybrid bound on actual laws."""
    _length(N)
    p = _probability(p)
    _frozen(N, frozen)
    native = _source_law(N, p)
    qjoint, count = [], 1 << len(frozen)
    for word in range(1 << N):
        probability, prefix = Fraction(1, count), []
        for i in range(N):
            bit = (word >> i) & 1
            if i not in frozen:
                one = prefix_one(N, p, tuple(prefix))
                probability *= one if bit else 1-one
            prefix.append(bit)
        qjoint.append(probability)
    if sum(qjoint) != 1 or sum(native) != 1:
        raise ArithmeticError("polar source or shaping law not normalized")
    source_mass = [Fraction(0)]*count
    qmass = [Fraction(0)]*count
    for u, probability in enumerate(native):
        s = syndrome(u, frozen)
        source_mass[s] += probability
        qmass[s] += qjoint[u]
    if qmass != [Fraction(1, count)]*count:
        raise ArithmeticError("shaping syndromes are not exactly uniform")
    tvs = []
    for s in range(count):
        tvs.append(sum(abs(qjoint[u]*count-native[u]/source_mass[s]) for u in range(1 << N)
                       if syndrome(u, frozen) == s)/2)
    joint = sum(abs(a-b) for a, b in zip(native, qjoint))/2
    marginal = sum(abs(x-Fraction(1, count)) for x in source_mass)/2
    average, weighted = sum(tvs)/count, sum(p*t for p, t in zip(source_mass, tvs))
    biases = source_biases(N, p)
    epsilon = sum(biases[i] for i in frozen)
    if not (joint <= epsilon and average <= joint+marginal and weighted <= joint+marginal
            and marginal <= joint and max(tvs) <= min(1, count*(joint+marginal))):
        raise ArithmeticError("native hybrid/conditional total-variation bound failed")
    return {"positions": N, "noise_probability": str(p), "frozen_coordinates": list(frozen),
            "source_law_entries_charged": 1 << N, "source_construction_is_exponential_calibration": True,
            "shaping_prefix_queries_charged": (1 << N)*(N-len(frozen)),
            "shaping_recursive_calls_charged": (1 << N)*(N-len(frozen))*(2*N-1),
            "frozen_prefix_bias_sum": str(epsilon), "source_shaping_joint_TV": str(joint),
            "syndrome_uniformity_TV": str(marginal), "uniform_syndrome_average_TV": str(average),
            "native_syndrome_weighted_average_TV": str(weighted), "worst_syndrome_TV": str(max(tvs)),
            "average_conditional_TV_upper": str(min(1, 2*epsilon)),
            "worst_conditional_TV_upper": str(min(1, 2*count*epsilon)),
            "all_syndromes": [{"syndrome": s, "native_mass": str(source_mass[s]), "sampler_TV": str(tvs[s])}
                              for s in range(count)],
            "worst_case_sign_dequantization_proved": False,
            "shaping_is_exact_native_conditional_sampler": max(tvs) == 0,
            "native_full_law_calibration_not_quantum_advantage": True}


def run_controls():
    p = Fraction(7, 40)
    calibrations = [calibration(2, Fraction(1, 10), (1,)), calibration(4, p, (0, 1))]
    # Exhaustive design cost is explicit; this is not an efficient asymptotic constructor.
    biases = source_biases(8, p)
    frozen = tuple(sorted(sorted(range(8), key=lambda i: (biases[i], i))[:3]))
    calibrations.append(calibration(8, p, frozen))
    nonprefix = tuple(sorted(sorted(range(8), key=lambda i: (biases[i], i))[:4]))
    calibrations.append(calibration(8, p, nonprefix))
    rows = []
    for N in (16, 32, 64):
        for F in (tuple(range(N//2)), tuple(range(0, N, 2))):
            rows.append({"positions": N, "noise_probability": str(p), "frozen_coordinates": list(F),
                         "frozen_set_is_a_supplied_public_control_not_certified_polar_design": True,
                         "samples": [sample(N, p, F, (1 << len(F))-1 if j % 2 else 0, 29+j) for j in range(4)],
                         "signed_Gibbs_samples": [sample_gibbs(N, 1-2*p, F,
                             random.Random(71+j).getrandbits(N), 171+j) for j in range(2)],
                         "distributional_TV_not_certified_by_sample_feasibility": True})
    return {"schema_version": "1.0", "subsystem": "polar_conditional_sampler",
            "calibrations": calibrations, "scalable_native_samples": rows,
            "native_channel_source_duality": [native_channel_duality(N, p) for N in (2, 4)],
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "numpy_version": np.__version__,
            "dependency_sha256": {"bpqm_gibbs_frontier.py": hashlib.sha256(
                (ROOT/"theorems/bpqm_gibbs_frontier.py").read_bytes()).hexdigest()},
            "accepted_speedup_candidate": False, "quantum_decoder_implemented": False,
            "all_polar_code_Gibbs_tasks_dequantized": False,
            "local_hybrid_derivation_review_pending": True,
            "literature": ["https://arxiv.org/pdf/2109.08170", "https://arxiv.org/pdf/2401.07167",
                           "https://arxiv.org/abs/0807.3917", "https://arxiv.org/html/2506.09239v2",
                           "https://arxiv.org/abs/1701.05583", "https://arxiv.org/abs/2103.09225"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    print(json.dumps([{"N": r["positions"], "frozen": r["frozen_coordinates"],
                       "average_TV": float(Fraction(r["uniform_syndrome_average_TV"])),
                       "worst_TV": float(Fraction(r["worst_syndrome_TV"])),
                       "hybrid_epsilon": float(Fraction(r["frozen_prefix_bias_sum"]))}
                      for r in report["calibrations"]], indent=2))


if __name__ == "__main__":
    main()
