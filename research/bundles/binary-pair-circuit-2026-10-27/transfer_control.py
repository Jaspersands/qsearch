"""Fixed F3 repetition control of the *actual* binary map and its inverse.

The success projector is enumerated only on 3^length pair transcripts. This
is not a compiled general decoder. It checks the accepted retained-label
state Pa/sqrt(p_bar), keeping every work register through the real inverse.
"""

from dataclasses import replace
from itertools import combinations, product
import math

import numpy as np

from pair_circuit import inverse, pair_circuit, simulate


def repetition_transfer(length, syndrome):
    if length not in (2, 3, 4) or syndrome not in range(3):
        raise ValueError("fixed F3 repetition controls only")
    local = pair_circuit(3)
    qubits = 4 * length + 3
    shared = (4 * length, 4 * length + 1, 4 * length + 2)
    gates = ()
    for coordinate in range(length):
        wires = tuple(range(4 * coordinate, 4 * coordinate + 4)) + shared
        gates += tuple(replace(g, targets=tuple(wires[b] for b in g.targets),
                               controls=tuple((wires[b], v) for b, v in g.controls))
                       for g in local.gates)
    labels = np.zeros((1 << qubits, 3), dtype=complex)
    for c in range(3):
        phi = np.full(3, -1 / math.sqrt(6))
        phi[c] += math.sqrt(3 / 2)
        for word in product(range(3), repeat=length):
            idx = sum(value << (4 * i) for i, value in enumerate(word))
            labels[idx, c] = math.prod(phi[value] for value in word)
    character = np.exp(-2j * np.pi * syndrome * np.arange(3) / 3)
    target = labels @ character / math.sqrt(3)
    lam = float(np.vdot(target, target).real)
    transformed = np.column_stack([simulate(gates, labels[:, c]) for c in range(3)])
    good = np.zeros(1 << qubits, dtype=bool)
    for transcript in product(tuple(combinations(range(3), 2)), repeat=length):
        solutions = [(v, w) for v, w in product(range(3), repeat=2)
                     if all((w - (a + b) * v + a*b) % 3 == 0 for a, b in transcript)]
        if len(solutions) == 1:
            idx = sum((a | (b << 2)) << (4*i) for i, (a, b) in enumerate(transcript))
            good[idx] = True
    successful = transformed.copy()
    successful[~good] = 0
    gram = successful.conj().T @ successful
    pbar = float(np.trace(gram).real / 3)
    if not np.allclose(gram, pbar*np.eye(3), atol=1e-14, rtol=0):
        raise ArithmeticError("accepted decoder is not unambiguous")
    accepted = successful @ character / math.sqrt(3 * pbar)
    output = simulate(inverse(gates), accepted)
    fidelity = float(abs(np.vdot(target / math.sqrt(lam), output)) ** 2)
    index = np.arange(len(output))
    data_mask = sum(3 << (4*i) for i in range(length))
    dirty = float(np.sum(abs(output[(index & ~data_mask) != 0]) ** 2))
    fourier = np.exp(2j*np.pi*np.outer(np.arange(3), np.arange(3))/3)/math.sqrt(3)
    for i in range(length):
        base = index[(index & (3 << (4*i))) == 0]
        rows = base[None, :] | (np.arange(3)[:, None] << (4*i))
        output[rows] = fourier @ output[rows]
    valid = np.ones(len(output), dtype=bool)
    total = np.zeros(len(output), dtype=int)
    codes = np.zeros(len(output), dtype=int)
    for i in range(length):
        value = (index >> (4*i)) & 3
        valid &= (value == 1) | (value == 2)
        total += value
        codes += value * 3**i
    valid &= total % 3 == syndrome
    probability = float(np.sum(abs(output[valid]) ** 2))
    law = np.bincount(codes[valid], weights=abs(output[valid])**2,
                      minlength=3**length) / probability
    ideal_law = np.zeros(3**length)
    fiber = [sum(value*3**i for i, value in enumerate(word))
             for word in product((1, 2), repeat=length) if sum(word) % 3 == syndrome]
    ideal_law[fiber] = 1 / len(fiber)
    tv = float(np.sum(abs(law - ideal_law)) / 2)
    tv_bound = math.sqrt(max(0, 1 - fidelity / probability))
    if abs(fidelity - pbar/lam) > 1e-12 or probability + 1e-12 < fidelity:
        raise ArithmeticError("binary inverse violates the transfer identity")
    if tv > tv_bound + 1e-12:
        raise ArithmeticError("verified conditional law violates fidelity-TV bound")
    return {"prime": 3, "length": length, "syndrome": syndrome,
            "qubits": qubits, "decoder_success": pbar, "gram_eigenvalue": lam,
            "joint_fidelity": fidelity, "predicted_joint_fidelity": pbar/lam,
            "data_valid_probability": probability,
            "raw_verified_probability": pbar * probability,
            "dirty_work_probability": dirty,
            "verified_conditional_tv_from_uniform": tv,
            "conditional_fidelity_tv_upper": tv_bound,
            "decoder_projector": "bounded enumeration, not gate compiled",
            "quantum_execution": False, "advantage_evidence": False}
