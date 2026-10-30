"""Fixed-sign HDQI transfer checks, not a Gibbs-preparation algorithm.

Dense audits are capped. Large repeated-term rows use closed formulas and
an independent rational certificate; they do not construct large pilots.
"""

from fractions import Fraction as F
from itertools import combinations
import math
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import eigvalsh, expm

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "hdqi-interference-distance-2026-10-24"))
import interference_distance as i  # noqa: E402


def label_elimination(model):
    """Binary column elimination retaining preimages and a kernel basis."""
    pivots, kernel = {}, []
    for j in range(model.pilot.m):
        value, preimage = model.label(1 << j), 1 << j
        while value:
            pivot = value.bit_length()-1
            if pivot not in pivots:
                pivots[pivot] = (value, preimage)
                break
            old, witness = pivots[pivot]
            value, preimage = value ^ old, preimage ^ witness
        if not value:
            kernel.append(preimage)
    return pivots, tuple(kernel)


def weighted_kernel(model, max_words=1000000):
    """Exact nonzero-kernel enumerator; exponential cost is explicit."""
    if type(max_words) is not int or max_words < 0:
        raise ValueError("nonnegative integer kernel budget required")
    pivots, kernel = label_elimination(model)
    required = (1 << len(kernel))-1
    report = {"rank_B": len(pivots), "kernel_dimension": len(kernel),
              "required_words": required, "checked_words": 0,
              "weighted_sum": None, "weight_counts": None}
    if required > max_words:
        return {**report, "status": "UNKNOWN_BUDGET"}
    weights = [min(F(1), model.pilot.beta*abs(j)) for j in model.pilot.couplings]
    counts, total, word = {}, F(0), 0
    for mask in range(1, required+1):
        word ^= kernel[(mask & -mask).bit_length()-1]
        size = word.bit_count()
        counts[size] = counts.get(size, 0)+1
        total += math.prod((b for j, b in enumerate(weights) if word >> j & 1), start=F(1))
    return {**report, "status": "EXACT", "checked_words": required,
            "weighted_sum": str(total), "weight_counts": {str(k): v for k, v in sorted(counts.items())}}


def low_weight_section(model, t, max_words=1000000):
    """Certify a decoder on every word of weight <=t, not on samples."""
    m = model.pilot.m
    if type(t) is not int or not 0 <= t <= m:
        raise ValueError("integer 0<=t<=m required")
    if type(max_words) is not int or max_words < 0:
        raise ValueError("nonnegative integer decoder budget required")
    pivots, kernel = label_elimination(model)

    def linear_section(syndrome):
        if type(syndrome) is not int or not 0 <= syndrome < 1 << (2*model.n):
            raise ValueError("invalid physical syndrome")
        word, value = 0, syndrome
        while value:
            pivot = value.bit_length()-1
            if pivot not in pivots:
                return 0  # Outside im B: never encountered on a physical input.
            label, witness = pivots[pivot]
            value, word = value ^ label, word ^ witness
        return word

    required = sum(math.comb(m, j) for j in range(t+1)) if kernel else 0
    report = {"t": t, "required_words": required, "checked_words": 0,
              "failure_upper": None, "collision": None}
    if not kernel:
        return linear_section, {**report, "status": "EXACT_INJECTIVE", "failure_upper": "0"}
    if required > max_words:
        return None, {**report, "status": "UNKNOWN_BUDGET"}
    table, checked = {}, 0
    for size in range(t+1):
        for indices in combinations(range(m), size):
            word = sum(1 << j for j in indices)
            syndrome = model.label(word)
            checked += 1
            if syndrome in table:
                return None, {**report, "status": "LOW_WEIGHT_COLLISION", "checked_words": checked,
                              "collision": {"syndrome": syndrome, "first": table[syndrome], "second": word}}
            table[syndrome] = word

    def decoder(syndrome):
        fallback = linear_section(syndrome)
        return table.get(syndrome, fallback)

    tail = i.factorial_tail(model, t)
    return decoder, {**report, "status": "CERTIFIED_LOW_WEIGHT", "checked_words": checked,
                     "failure_upper": str(tail["tail_upper"]), "tail_moment_order": tail["moment_order"]}


def certify_transfer(model, t, epsilon=F(1, 1000), *, max_kernel_words=1000000,
                     max_decoder_words=1000000):
    epsilon = i.o.s.rational(epsilon)
    if not 0 < epsilon < 1:
        raise ValueError("epsilon must be in (0,1)")
    decoder, section = low_weight_section(model, t, max_decoder_words)
    kernel = weighted_kernel(model, max_kernel_words)
    bound = None
    if decoder is not None and kernel["status"] == "EXACT":
        r, weight = F(section["failure_upper"]), F(kernel["weighted_sum"])
        bound = min(F(1), 2*r+weight, (1+(1 << kernel["kernel_dimension"]))*r)
    accepted = bound is not None and bound <= epsilon*epsilon
    report = {"status": "CERTIFIED_IDEAL_PILOT_TRANSFER" if accepted else "NO_CERTIFICATE",
              "epsilon": str(epsilon), "trace_distance_squared_upper": str(bound) if bound is not None else None,
              "decoder": section, "kernel": kernel, "ideal_canonical_pilot_assumed": True,
              "pilot_preparation_implemented": False, "quantum_advantage_claimed": False,
              "hardness_from_refusal": False, "independent_review": False}
    return decoder, report


def trace_distance(a, b):
    return float(np.sum(abs(eigvalsh(a-b)))/2)


def dense_audit(model, decoder, sign_mask=0):
    if model.pilot.m > 8 or model.n > 3:
        raise ValueError("dense audit requires m<=8,n<=3")
    m, dim = model.pilot.m, 1 << model.n
    if type(sign_mask) is not int or not 0 <= sign_mask < 1 << m:
        raise ValueError("invalid sign mask")
    psi = i.dense_pilot(model)
    psi *= np.array([(-1)**((y & sign_mask).bit_count()) for y in range(1 << m)])
    blocks, bad_by_syndrome = {}, {}
    r = 0.0
    for y, amplitude in enumerate(psi):
        residue = y ^ i.o.decoder_value(model, decoder, model.label(y))
        p = np.eye(dim, dtype=complex)
        for j, generator in enumerate(model.paulis):
            if y >> j & 1:
                p = p@i.matrix(generator, model.n)
        blocks[residue] = blocks.get(residue, np.zeros((dim, dim), complex))+amplitude*p/math.sqrt(dim)
        if residue:
            r += float(abs(amplitude)**2)
            syndrome = model.label(y)
            bad_by_syndrome[syndrome] = bad_by_syndrome.get(syndrome, 0)+1
    zero = np.zeros((dim, dim), complex)
    g = blocks.get(0, zero)
    b = sum((p for residue, p in blocks.items() if residue), start=zero.copy())
    w = float(np.linalg.norm(b)**2)
    target_unnormalized = g+b
    target_norm_squared = float(np.linalg.norm(target_unnormalized)**2)
    target = target_unnormalized/math.sqrt(target_norm_squared)
    physical_h = sum(float(c)*(-1)**((sign_mask >> j) & 1)*i.matrix(p, model.n)
                     for j, (p, c) in enumerate(zip(model.paulis, model.pilot.couplings)))
    physical_s = expm(-float(model.pilot.beta)*physical_h/2)
    thermal = physical_s@physical_s
    thermal /= np.trace(thermal)
    exact_tfd = physical_s/np.linalg.norm(physical_s)
    left = sum((p@p.conj().T for p in blocks.values()), start=zero.copy())
    vectors = [p.reshape(-1) for p in blocks.values()]
    pair = sum((np.outer(v, v.conj()) for v in vectors), start=np.zeros((dim*dim, dim*dim), complex))
    tvect = target.reshape(-1)
    infidelity = 1-float(np.vdot(tvect, pair@tvect).real)
    max_fiber = max(bad_by_syndrome.values(), default=0)
    errors = {"isometry_normalization": abs(float(np.trace(left).real)-1),
              "good_norm": abs(float(np.linalg.norm(g)**2)-(1-r)),
              "physical_target_identity": float(np.linalg.norm(target-exact_tfd)),
              "unnormalized_error_identity": abs(
                  float(np.linalg.norm(b)**2+sum(np.linalg.norm(p)**2 for residue, p in blocks.items() if residue))-(r+w))}
    left_distance = trace_distance(left, thermal)
    pair_distance = trace_distance(pair, np.outer(tvect, tvect.conj()))
    if max(errors.values()) > 1e-9 or infidelity > r+w+1e-9 or w > max_fiber*r+1e-9:
        raise ArithmeticError("fixed-sign identity or bound failed")
    if pair_distance**2 > r+w+1e-9 or left_distance > pair_distance+1e-9:
        raise ArithmeticError("state-distance bound failed")
    return {"n": model.n, "m": m, "sign_mask": sign_mask,
            "pilot_decoding_failure": r, "coherent_bad_mass": w,
            "fixed_sign_infidelity_upper": min(1, r+w),
            "target_norm_ratio": target_norm_squared,
            "max_bad_syndrome_fiber": max_fiber,
            "actual_TFD_infidelity": max(0, infidelity),
            "actual_pair_trace_distance": pair_distance,
            "actual_physical_trace_distance": left_distance,
            "actual_physical_distance_to_maximally_mixed": trace_distance(left, np.eye(dim)/dim),
            "identity_errors": errors, "quantum_algorithm_executed": False}


def log_cosh(x):
    return math.log1p(2*math.sinh(x/2)**2)


def repeated_formula(k, beta=1.0):
    if type(k) is not int or not 1 <= k <= 2**40:
        raise ValueError("integer 1<=K<=2^40 required")
    if isinstance(beta, bool) or not math.isfinite(beta) or not 0 <= beta <= 1:
        raise ValueError("finite 0<=beta<=1 required")
    x = beta/(2*k)
    q = math.sinh(x)**2/math.cosh(2*x)
    r = -math.expm1((k-1)*math.log1p(-q))
    log_z = k*log_cosh(beta/k)
    g0 = math.exp(k*log_cosh(x)-log_z/2)
    g1 = -math.exp((k-1)*log_cosh(x)-log_z/2)*math.sinh(x)
    v0 = math.cosh(beta/2)*math.exp(-log_z/2)
    v1 = -math.sinh(beta/2)*math.exp(-log_z/2)
    w = (v0-g0)**2+(v1-g1)**2
    return {"K": k, "beta": beta, "canonical_total_squared_mass": 1/k,
            "canonical_sign_ratio": 1, "pilot_decoding_failure": r,
            "coherent_bad_mass": w, "target_norm_ratio": math.cosh(beta)*math.exp(-log_z),
            "actual_physical_trace_distance": (math.tanh(beta)-math.tanh(beta/k))/2,
            "physical_H_unchanged": "Z", "large_pilot_built": False,
            "floating_values_are_not_interval_certificates": True}


def repeated_certificate(k):
    if type(k) is not int or not 2 <= k <= 2**40:
        raise ValueError("integer 2<=K<=2^40 required")
    failure_upper = F(k-1, 4*k*k)
    distance_lower = F(3, 8)-F(1, 2*k)
    return {"K": k, "beta": "1", "pilot_failure_upper": str(failure_upper),
            "physical_trace_distance_strict_lower": str(distance_lower),
            "canonical_beta_squared_mass": str(F(1, k)),
            "canonical_beta_squared_Jmax_squared_d_plus_one": str(F(1, k*k)),
            "canonical_sign_ratio": "1",
            "small_failure_does_not_certify_fixed_sign_Gibbs": distance_lower*distance_lower > 2*failure_upper,
            "random_sign_theorem_falsified": False, "large_pilot_built": False}


def repeated_model(k, beta=F(1)):
    if type(k) is not int or not 1 <= k <= 8:
        raise ValueError("explicit repeated model capped at K<=8")
    return i.o.d.Physical.create(1, [(0, 1, 0)]*k, [F(1, k)]*k, beta)


def exact_commutator(left, right):
    """Sparse Gaussian-rational Pauli product, with canonical X^x Z^z keys."""
    out = {}
    for sign, a, b in ((1, left, right), (-1, right, left)):
        for p, c in a:
            for q, e in b:
                x, z, phase = i.o.d.multiply(p, q)
                real, imag = ((1, 0), (0, 1), (-1, 0), (0, -1))[phase]
                old = out.get((x, z), (F(0), F(0)))
                out[x, z] = (old[0]+sign*c*e*real, old[1]+sign*c*e*imag)
    return {key: value for key, value in out.items() if value != (0, 0)}


def sign_structure_control():
    c, s = F(3, 5), F(4, 5)
    z1, z2, yx, xy = (0, 1, 0), (0, 2, 0), (3, 1, 1), (3, 2, 1)
    a = [(z1, c), (yx, -s)]
    b = [(z2, c), (xy, -s)]
    flipped = [(z2, c), (xy, s)]
    original = exact_commutator(a, b)
    changed = exact_commutator(a, flipped)
    if original or changed != {(3, 3): (F(0), -4*c*s)}:
        raise ArithmeticError("exact correlated-sign control failed")
    return {"cos_2theta": str(c), "sin_2theta": str(s),
            "original_grouped_terms_commute": not original,
            "one_independent_Pauli_sign_flip_breaks_commutation": bool(changed),
            "changed_commutator_coefficient_on_X1X2Z1Z2": ["0", str(-4*c*s)],
            "this_is_an_identity_control_not_a_hardness_instance": True}
