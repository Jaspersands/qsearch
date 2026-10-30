"""Explicitly exponential small-instance controls, separate from the sampler."""

from __future__ import annotations

from fractions import Fraction as F
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import expm

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "hdqi-parent-gap-2026-10-23"))
from parent_gap import build_model

from fermion_sampler import (amplitudes, boundary, chord_word, coherent_numerator,
                             condition, determinant, minor, probability,
                             proposal_probability, word_phase)


def dense_pilot(model, beta):
    if not 1 <= len(model.edges) <= 8:
        raise ValueError("dense native audit is capped at 8 edge generators")
    h = build_model(len(model.edges), model.line_edges, model.couplings).h
    # Shift the ground energy to avoid an irrelevant overflow in this reference.
    energy = float(np.linalg.eigvalsh(h)[0])
    vector = expm(-beta * (h - energy * np.eye(len(h))) / 2)[:, 0]
    return vector / np.linalg.norm(vector)


def coherent_reference(prepared):
    model = prepared.model
    if len(model.edges) > 8:
        raise ValueError("coherent state table is a capped audit, not a circuit")
    result = []
    denominator = np.sqrt(len(prepared.sectors) * float(prepared.total_norm))
    for y in range(1 << len(model.edges)):
        phase, x = word_phase(model, y)
        numerator = coherent_numerator(amplitudes(prepared, x), chord_word(model, y))
        result.append((1j) ** (-phase) * (-1j) ** (x.bit_count() // 2)
                      * float(numerator) / denominator)
    return np.array(result)


def dpp_branch_law(kernel):
    if len(kernel) > 10:
        raise ValueError("exhaustive DPP branch audit capped at 10 vertices")
    result = {}

    def walk(k, index, word, weight):
        if not k:
            result[word] = weight
            return
        p = k[0][0]
        for take, chance in ((False, 1 - p), (True, p)):
            if chance:
                walk(condition(k, take), index + 1, word | (int(take) << index),
                     weight * chance)

    walk(kernel, 0, 0, F(1))
    return result


def rational_law_control(prepared):
    if len(prepared.model.edges) > 8:
        raise ValueError("full law audit capped at 8 generators")
    count = len(prepared.sectors)
    native_law = [probability(prepared, y)
                  for y in range(1 << len(prepared.model.edges))]
    proposals = [proposal_probability(prepared, y) for y in range(len(native_law))]
    envelope = all(p <= count * q for p, q in zip(native_law, proposals))
    accepted_mass = sum((p / count for p in native_law), F(0))
    branch_checks = []
    for sector in prepared.sectors:
        law = dpp_branch_law(sector.marginal)
        branch_checks.append(all(
            law.get(x, F(0)) == determinant(minor(sector.k, x)) / sector.norm
            for x in range(1 << prepared.model.n)))
    return {
        "target_normalized_exactly": sum(native_law, F(0)) == 1,
        "proposal_normalized_exactly": sum(proposals, F(0)) == 1,
        "envelope_holds_exactly": envelope,
        "accepted_mass": str(accepted_mass),
        "expected_trials": count,
        "all_dpp_branches_exact": all(branch_checks),
        "incoherent_shortcut_tv": float(sum((abs(p - q) for p, q in
                                               zip(native_law, proposals)), F(0)) / 2),
    }
