"""Bell-label pushforward and exact sparse-Pauli proof controls.

No Gibbs constructor, quantum oracle, decoder, or research candidate search.
Sparse polynomial expansion below is strictly a bounded proof diagnostic.
"""

from collections import defaultdict
from fractions import Fraction
import math
from operator import index

import numpy as np


def map_sample(label, columns):
    """Binary forward map on one observed label; no inverse or decoder."""
    try:
        label = index(label)
        columns = tuple(index(c) for c in columns)
    except TypeError as exc:
        raise ValueError("Integer label and map columns required") from exc
    if not 0 <= label < (1 << len(columns)):
        raise ValueError("Label outside supplied binary map")
    if any(c < 0 for c in columns):
        raise ValueError("Invalid map column")
    result = 0
    while label:
        bit = label & -label
        result ^= columns[bit.bit_length()-1]
        label ^= bit
    return result


def born_law(coefficients):
    """Exact finite Born distribution for real integer Pauli coefficients."""
    norm = sum(v*v for v in coefficients.values())
    if norm <= 0:
        raise ValueError("Zero filter")
    return {u: Fraction(v*v, norm) for u, v in coefficients.items() if v}


def push_law(law, mapping):
    result = defaultdict(Fraction)
    for label, probability in law.items():
        if probability < 0:
            raise ValueError("Negative probability")
        result[mapping(label)] += probability
    if sum(result.values()) != 1:
        raise ValueError("Input is not an exact probability law")
    return dict(result)


def tv(left, right):
    return sum(abs(left.get(k, 0)-right.get(k, 0)) for k in left.keys() | right.keys()) / 2


def circuit_target_density(amplitudes, images, decoder, phases):
    """Bounded full pure-state circuit, then actual partial trace of source.

    |u,0> -> phase(u)|u xor decoder(image(u)), image(u)>.
    Decoder need not be correct for this population identity.
    """
    size, target_size = len(amplitudes), len(decoder)
    if (size < 1 or size > 256 or size & (size-1) or
            target_size < 1 or target_size > 256 or target_size & (target_size-1)):
        raise ValueError("Invalid or oversized circuit control")
    if len(images) != size or len(phases) != size:
        raise ValueError("Incomplete map or phase table")
    if any(not 0 <= d < size for d in decoder) or any(not 0 <= t < target_size for t in images):
        raise ValueError("Invalid labels")
    a = np.asarray(amplitudes, dtype=complex)
    p = np.asarray(phases, dtype=complex)
    if not np.all(np.isfinite(a)) or not np.all(np.isfinite(p)):
        raise ValueError("Nonfinite input")
    if abs(np.vdot(a, a)-1) > 1e-10 or np.max(abs(abs(p)-1)) > 1e-10:
        raise ValueError("Normalized source and unit phases required")
    state = np.zeros((size, target_size), dtype=complex)
    for u, target in enumerate(images):
        state[u ^ decoder[target], target] += p[u] * a[u]
    return state.T @ state.conj()


def paired_readout_value(u, amplitude, columns, decoder, phase, flip, observable_phase):
    """Bounded CT-state estimator; amplitude/decoder access are PAID inputs.

    The observable maps |t> to observable_phase(t)|t xor flip> and must be
    Hermitian. Callbacks are diagnostic inputs, not certificates of that
    promise, efficient access, source sampling, or arithmetic accuracy.
    """
    flip = index(flip)
    if flip < 0:
        raise ValueError("Negative observable flip mask")
    target = map_sample(u, columns)
    partner_target = target ^ flip
    d, dp = decoder(target), decoder(partner_target)
    if not 0 <= d < 1 << len(columns) or not 0 <= dp < 1 << len(columns):
        raise ValueError("Decoder output outside source register")
    partner = u ^ d ^ dp
    if map_sample(partner, columns) != partner_target:
        return 0.0
    chi, chip, nu = phase(u), phase(partner), observable_phase(target)
    for value in (chi, chip, nu):
        if not math.isfinite(abs(value)) or abs(abs(value)-1) > 1e-10:
            raise ValueError("Finite unit phases required")
    a, b = complex(chi*amplitude(u)), complex(chip*amplitude(partner))
    scale = max(abs(a), abs(b))
    if not math.isfinite(scale):
        raise ArithmeticError("Nonfinite amplitude")
    if scale == 0:
        return 0.0
    a, b = a/scale, b/scale
    return 2*(b.conjugate()*nu*a).real / (abs(a)**2+abs(b)**2)


def multiply_commuting_hermitian(left, right):
    """Exact integer Pauli arithmetic; fail if the product is not Hermitian."""
    accum = defaultdict(lambda: [0, 0])
    for (x, z), a in left.items():
        for (xp, zp), b in right.items():
            key = x ^ xp, z ^ zp
            phase = ((x & z).bit_count() + (xp & zp).bit_count()
                     - (key[0] & key[1]).bit_count() + 2*(z & xp).bit_count()) % 4
            accum[key][phase % 2] += a*b*(1 if phase < 2 else -1)
    if any(imag for real, imag in accum.values()):
        raise ValueError("Product is not Hermitian")
    return {k: real for k, (real, imag) in accum.items() if real}


def polynomial(hamiltonian, coefficients):
    if len(coefficients) > 4 or len(hamiltonian) > 30:
        raise ValueError("Sparse expansion is a bounded diagnostic only")
    result, power = defaultdict(int), {(0, 0): 1}
    for degree, coefficient in enumerate(coefficients):
        for label, value in power.items():
            result[label] += coefficient * value
        if degree+1 < len(coefficients):
            power = multiply_commuting_hermitian(power, hamiltonian)
    return {u: c for u, c in result.items() if c}


def chain_control(n):
    """Native relative-chain form with repetition kernel; not a hard instance."""
    if not 3 <= n <= 6:
        raise ValueError("Control size is bounded")
    columns = tuple(1 << i for i in range(n-1)) + ((1 << (n-1))-1,)
    source, target = {}, {}
    for i in range(n):
        local, center = 1 << i, 1 << (n+i)
        mapped = columns[i] << n
        for src, dst, coefficient in (
            ((local, 0), (local, 0), 1),
            ((0, local), (0, local), -1),
            ((0, center), (0, mapped), 1),
            ((0, local | center), (0, local | mapped), -1),
        ):
            source[src], target[dst] = coefficient, coefficient
        if i+1 < n:
            edge = (0, local | (local << 1))
            source[edge] = target[edge] = 1

    def label_map(label):
        x, z = label
        if x >> n or z >> (2*n):
            raise ValueError("Label outside the source Hamiltonian algebra")
        return x, (z & ((1 << n)-1)) | (map_sample(z >> n, columns) << n)

    return source, target, label_map


def exact_chain_evidence(n=5, degree=2):
    source, target, mapping = chain_control(n)
    a, b = polynomial(source, [1]*(degree+1)), polynomial(target, [1]*(degree+1))
    pushed = push_law(born_law(a), mapping)
    target_law = born_law(b)
    images = [mapping(u) for u in a]
    coherent = defaultdict(int)
    for u, value in a.items():
        coherent[mapping(u)] += value
    return {
        "cells": n, "relative_distance": n, "degree": degree,
        "strict_distance_condition": 2*degree < n,
        "source_terms": len(source), "source_coefficient_support": len(a),
        "target_coefficient_support": len(b),
        "support_map_injective": len(images) == len(set(images)),
        "coherent_coefficients_match": {u: v for u, v in coherent.items() if v} == b,
        "bell_pushforward_tv": str(tv(pushed, target_law)),
        "coefficient_expansion_cost_charged": True,
        "hard_instance": False,
    }
