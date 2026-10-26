"""Finite UT4 controls for the affine-support phase-erasure proposal.

All secret-bearing source/potential functions are fixtures. The physical
controller is in affine_phase_erasure and sees only public phase maps.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import product
import json
from math import sqrt
from pathlib import Path
import random

import numpy as np

from theorems.affine_phase_erasure import (
    cancellation_weights, copy_budget, initial_packet, monomials, sample_merge,
)
from theorems.graded_hsp_phase_descent import UT4Product, coset_fixture
from theorems.folded_rs_decoder import affine_solution

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/reductions/ut4_affine_phase_receiver.json"


def opaque_classical_query_bound(p, rank, queries):
    """Distributional collision bound for random opaque coset labels only."""
    UT4Product(p, rank)
    if type(queries) is not int or queries < 0:
        raise ValueError("nonnegative query count required")
    families = (p ** (6 * rank) - p ** (4 * rank)) // (p - 1)
    success = min(Fraction(1), Fraction(queries * (queries - 1) // 2 + 1, families))
    return families, success


def split_coordinates(group, element):
    """Public G=N semidirect A chart, N=((13,23,24,14)), A=((12,34))."""
    q, normal = [], []
    for i in range(group.rank):
        x, b, z, u, v, w = element[6*i:6*i+6]
        q += [x, z]
        normal += [u, b, v - b*z, w - u*z]
    return tuple(q), tuple(x % group.p for x in normal)


def join_coordinates(group, q, normal):
    element = []
    for i in range(group.rank):
        x, z = q[2*i:2*i+2]
        u, b, v, w = normal[4*i:4*i+4]
        element += [x, b, z, u, v + b*z, w + u*z]
    return tuple(x % group.p for x in element)


def action(group, q, normal):
    result = []
    for i in range(group.rank):
        x, z = q[2*i:2*i+2]
        u, b, v, w = normal[4*i:4*i+4]
        result += [u + x*b, b, v - z*b, w + x*v - z*u - x*z*b]
    return tuple(x % group.p for x in result)


def partial_fourier_branch(group, source_state, label):
    """Public partial QFT branch, with its actual probability."""
    p = group.p
    if len(label) != 4 * group.rank or any(type(a) is not int or not 0 <= a < p for a in label):
        raise ValueError("canonical Fourier label required")
    result = {}
    for element, amplitude in source_state.items():
        q, normal = split_coordinates(group, element)
        phase = sum(a * b for a, b in zip(label, normal)) % p
        result[q] = result.get(q, 0j) + amplitude * np.exp(2j * np.pi * phase / p)
    norm = sum(abs(a) ** 2 for a in result.values())
    if norm < 1e-20:
        return {}, 0.0
    return {q: a / sqrt(norm) for q, a in result.items()}, norm / p ** len(label)


def normal_intersection_branches(group, source_state):
    """Measure A, then undo its known action to obtain H-intersect-N cosets."""
    branches = {}
    for element, amplitude in source_state.items():
        q, normal = split_coordinates(group, element)
        transformed = action(group, tuple(-x % group.p for x in q), normal)
        branch = branches.setdefault(q, {})
        branch[transformed] = branch.get(transformed, 0j) + amplitude
    return branches


def potential_fixture(group, generator, q):
    """Secret-bearing proof witness. NEVER needed by the phase controller."""
    v, _ = split_coordinates(group, generator)
    if not any(v):
        raise ValueError("nonzero projection to A required")
    pivot = next(i for i, x in enumerate(v) if x)
    t = q[pivot] * pow(v[pivot], -1, group.p) % group.p
    transverse = tuple((a - t*b) % group.p for a, b in zip(q, v))
    _, orbit = split_coordinates(group, group.power(generator, t))
    return action(group, transverse, orbit)


def graph_relabel_branches(group, source_state, learned_direction):
    """Public conversion to univariate HPGP states AFTER learning the line.

    Measure q_perp=q-ell(q)*v, apply Phi(-q_perp) to the normal coordinates,
    and retain ell(q). This needs fresh original coset copies, not an oracle
    restricted to a hidden preimage or an unknown coset representative.
    """
    p, v = group.p, tuple(learned_direction)
    if len(v) != 2 * group.rank or not any(v) or any(type(a) is not int or not 0 <= a < p for a in v):
        raise ValueError("nonzero canonical learned quotient direction required")
    pivot = next(i for i, x in enumerate(v) if x)
    inverse = pow(v[pivot], -1, p)
    branches = {}
    for element, amplitude in source_state.items():
        q, normal = split_coordinates(group, element)
        t = q[pivot] * inverse % p
        perpendicular = tuple((a - t*b) % p for a, b in zip(q, v))
        transformed = action(group, tuple(-a % p for a in perpendicular), normal)
        branch = branches.setdefault(perpendicular, {})
        key = (t,) + transformed
        branch[key] = branch.get(key, 0j) + amplitude
    return branches


def interpolate_potential_fixture(group, generator):
    """Bounded verification of the global cubic potential, not an algorithm step."""
    width, p = 2 * group.rank, group.p
    if p ** width > 4096:
        raise ValueError("finite interpolation diagnostic cap")
    basis = [a for a in monomials(width, 3) if any(a)]
    points = list(product(range(p), repeat=width))
    rows = [[int(np.prod([pow(x, a, p) for x, a in zip(q, alpha)], dtype=object)) % p
             for alpha in basis] for q in points]
    values = [potential_fixture(group, generator, q) for q in points]
    coefficients = []
    for j in range(4 * group.rank):
        solution = affine_solution(p, rows, [value[j] for value in values], len(basis))
        if solution is None or solution["basis"]:
            raise ArithmeticError("potential is not a unique cubic in the tested chart")
        coefficients.append(solution["offset"])
    return tuple(coefficients[j][i] for i in range(len(basis)) for j in range(4 * group.rank))


def run_diagnostic(seed=20261021, outputs=1):
    """Original random cosets -> random Fourier labels -> all-degree erasure."""
    if type(outputs) is not int or not 1 <= outputs <= 4:
        raise ValueError("diagnostic supports one to four output states")
    p, rank = 23, 1
    group = UT4Product(p, rank)
    # Both grade-two coordinates are nonzero, unlike the preceding promise.
    generator = group.exp((1, 2, 3, 4, 5, 6))
    rng = random.Random(seed)
    budget = copy_budget(2 * rank, 4 * rank)
    counts = {"source_cosets": 0, "merges": {"3": 0, "2": 0, "1": 0},
              "max_equation_rank": {"3": 0, "2": 0, "1": 0},
              "zero_fourier_labels": 0,
              "single_active_input_merges": {"3": 0, "2": 0, "1": 0}}
    max_phase_error, max_fourier_probability_error = 0.0, 0.0

    def produce(degree):
        nonlocal max_fourier_probability_error
        if degree == 4:
            representative = tuple(rng.randrange(p) for _ in group.identity)
            label = tuple(rng.randrange(p) for _ in range(4 * rank))
            counts["zero_fourier_labels"] += int(not any(label))
            state, probability = partial_fourier_branch(
                group, coset_fixture(group, generator, representative), label)
            max_fourier_probability_error = max(max_fourier_probability_error, abs(probability - p ** (-4*rank)))
            counts["source_cosets"] += 1
            return state, initial_packet(p, 2 * rank, label)
        inputs = [produce(degree + 1) for _ in range(budget[str(degree)])]
        states, packets = map(list, zip(*inputs))
        weights, equation_rank = cancellation_weights(packets, degree, rng)
        counts["single_active_input_merges"][str(degree)] += int(sum(bool(c) for c in weights) == 1)
        state, packet, _, _ = sample_merge(p, states, packets, weights, rng)
        if packet.degree >= degree:
            raise ArithmeticError("symbolic degree did not decrease")
        if len(state) != p:
            raise ArithmeticError("collective measurement lost full line support")
        counts["merges"][str(degree)] += 1
        counts["max_equation_rank"][str(degree)] = max(
            counts["max_equation_rank"][str(degree)], equation_rank)
        return state, packet

    output_rows = []
    v, _ = split_coordinates(group, generator)
    for _ in range(outputs):
        state, packet = produce(1)
        anchor = next(iter(state.values()))
        error = max(abs(a / anchor - 1) for a in state.values())
        max_phase_error = max(max_phase_error, error)
        probabilities = {}
        for frequency in product(range(p), repeat=2 * rank):
            amp = sum(a * np.exp(-2j * np.pi * sum(x*y for x, y in zip(frequency, q)) / p)
                      for q, a in state.items()) / sqrt(p ** (2 * rank))
            probabilities[frequency] = abs(amp) ** 2
        forbidden_mass = sum(probability for f, probability in probabilities.items()
                             if sum(x*y for x, y in zip(f, v)) % p)
        output_rows.append({"support_size": len(state), "symbolic_degree": packet.degree,
                            "relative_phase_error": error, "fourier_mass_outside_annihilator": forbidden_mass})
    families, classical_bound = opaque_classical_query_bound(p, rank, 64)
    return {
        "status": "CONSTRUCTIVE_QUOTIENT_LINE_CONVERSION_REVIEW_PENDING",
        "scope": "cyclic H not in N for UT4(Fp)^r; implemented controller p=11 mod12",
        "prime": p, "rank": rank, "seed": seed, "log_generator_fixture": [1, 2, 3, 4, 5, 6],
        "public_input_model": "original coset states and measured Fourier labels; no hidden advice",
        "copy_budget": budget, "counts": counts, "outputs": output_rows,
        "max_partial_fourier_probability_error": max_fourier_probability_error,
        "max_relative_phase_error": max_phase_error,
        "all_outcomes_retained": True, "rare_label_postselection": False,
        "diagnostic_enumeration_is_quantum_runtime": False,
        "classical_query_audit": {
            "model": "uniform cyclic H outside N, independent opaque injective coset names",
            "subgroup_count": families, "queries": 64,
            "success_upper_bound_fraction": str(classical_bound),
            "general_bound": "min(1,(binom(T,2)+1)/((p^(6r)-p^(4r))/(p-1)))",
            "not_a_lower_bound_for_structured_explicit_evaluators": True,
            "finite_example_shows_runtime_advantage": False,
        },
        "full_hsp_receiver_executed": False,
        "novelty_established": False, "external_computational_reduction": None,
        "remaining": [
            "Independent proof and prior-art review of the collective affine-support extension.",
            "Public copies-only reduction to known univariate HPGP is tested; the HPGP solver is not executed.",
            "No cryptographic, lattice, graph or other external problem reduction established.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--outputs", type=int, default=1)
    args = parser.parse_args()
    report = run_diagnostic(outputs=args.outputs)
    if args.write:
        REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
