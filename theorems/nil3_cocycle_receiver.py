"""Explicit class-three BCH groups and a finite cyclic-HSP receiver control.

LOCAL DERIVATION / REVIEW PENDING. Sparse quantum-state simulation is not
polynomial-time classical HSP solving. Public controllers use only known
structure constants, measured labels/outcomes, and supplied coset copies.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from itertools import combinations, product
import json
from math import sqrt
from pathlib import Path
import random

import numpy as np

from theorems.affine_phase_erasure import (
    PhasePacket, cancellation_weights, copy_budget, independent_columns,
    initial_packet, sample_merge,
)
from theorems.folded_rs_decoder import affine_solution
from theorems.graded_hsp_phase_descent import _canonical
from theorems.prime_character_opi import ring

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/reductions/nil3_cocycle_receiver.json"


@dataclass
class ClassThreeBCH:
    """Public Lie algebra in a basis with its derived ideal in the last n slots."""

    p: int
    m: int
    n: int
    brackets: dict[tuple[int, int], tuple[int, ...]]

    def __post_init__(self):
        ring(self.p)
        if self.p <= 3 or type(self.m) is not int or type(self.n) is not int or min(self.m, self.n) < 1:
            raise ValueError("p>3 and positive quotient/derived dimensions required")
        self.dimension = self.m + self.n
        self.zero = (0,) * self.dimension
        for (i, j), vector in self.brackets.items():
            if not 0 <= i < j < self.dimension:
                raise ValueError("strictly ordered basis bracket indices required")
            _canonical(vector, self.dimension, self.p)
            if any(vector[:self.m]):
                raise ValueError("basis must be adapted to the derived ideal")
        basis = [tuple(int(i == j) for j in range(self.dimension))
                 for i in range(self.dimension)]
        values = list(self.brackets.values())
        if not values or independent_columns(values, self.p)[1] != self.n:
            raise ValueError("last n basis vectors must span exactly the derived ideal")
        for i, j, k in combinations(range(self.dimension), 3):
            jacobi = self.add(self.bracket(basis[i], self.bracket(basis[j], basis[k])),
                              self.bracket(basis[j], self.bracket(basis[k], basis[i])),
                              self.bracket(basis[k], self.bracket(basis[i], basis[j])))
            if any(jacobi):
                raise ValueError("Jacobi identity fails")
        if any(self.bracket(x, y) != self.zero
               for x in basis[self.m:] for y in basis[self.m:]):
            raise ValueError("derived ideal must be abelian")
        third = [self.bracket(x, z) for x in basis for z in values]
        if any(self.bracket(x, z) != self.zero for x in basis for z in third):
            raise ValueError("nilpotency class exceeds three")

    def add(self, *vectors):
        return tuple(sum(xs) % self.p for xs in zip(*vectors))

    def scale(self, c, vector):
        return tuple(c * x % self.p for x in vector)

    def bracket(self, x, y):
        result = [0] * self.dimension
        for (i, j), vector in self.brackets.items():
            coefficient = (x[i] * y[j] - x[j] * y[i]) % self.p
            if coefficient:
                for k, value in enumerate(vector):
                    result[k] += coefficient * value
        return tuple(x % self.p for x in result)

    def bch(self, x, y):
        xy = self.bracket(x, y)
        return self.add(x, y, self.scale(pow(2, -1, self.p), xy),
                        self.scale(pow(12, -1, self.p),
                                   self.add(self.bracket(x, xy), self.scale(-1, self.bracket(y, xy)))))

    def lift(self, q):
        _canonical(q, self.m, self.p)
        return tuple(q) + (0,) * self.n

    def ideal(self, normal):
        _canonical(normal, self.n, self.p)
        return (0,) * self.m + tuple(normal)

    def to_chart(self, logarithm):
        q = tuple(logarithm[:self.m])
        residual = (0,) * self.m + tuple(logarithm[self.m:])
        normal = self.add(residual, self.scale(pow(2, -1, self.p),
                                               self.bracket(self.lift(q), residual)))[self.m:]
        return q, normal

    def from_chart(self, q, normal):
        return self.bch(self.ideal(normal), self.lift(q))

    def action(self, q, normal):
        value = self.ideal(normal)
        return self.add(value, self.bracket(self.lift(q), value))[self.m:]

    def cocycle(self, q, r):
        a, b = self.lift(q), self.lift(r)
        ab = self.bracket(a, b)
        return self.add(self.scale(pow(2, -1, self.p), ab),
                        self.scale(pow(3, -1, self.p), self.bracket(a, ab)),
                        self.scale(pow(6, -1, self.p), self.bracket(b, ab)))[self.m:]

    def chart_product(self, q, normal, r, other):
        return (self.add(q, r),
                self.add(normal, self.action(q, other), self.cocycle(q, r)))


def free_two_step_three(p=47, rank=1):
    """Direct products of the free class-three Lie algebra on two generators."""
    if type(rank) is not int or rank < 1:
        raise ValueError("positive product rank required")
    m, dimension, brackets = 2 * rank, 5 * rank, {}
    for i in range(rank):
        x, y, z, u, v = 2*i, 2*i+1, m+3*i, m+3*i+1, m+3*i+2
        for a, b, c in ((x, y, z), (x, z, u), (y, z, v)):
            brackets[a, b] = tuple(int(j == c) for j in range(dimension))
    return ClassThreeBCH(p, m, 3 * rank, brackets)


def free_step_three(p=5, generators=3):
    """Public free class-three Hall-basis fixture, including three-way Jacobi."""
    if type(generators) is not int or generators < 2:
        raise ValueError("at least two generators required")
    m = generators
    second = list(combinations(range(m), 2))
    third = [(k, i, j) for i, j in second for k in range(i, m)]
    degree_two = {pair: m+i for i, pair in enumerate(second)}
    degree_three = {word: m+len(second)+i for i, word in enumerate(third)}
    d, brackets = m+len(second)+len(third), {}
    for i, j in second:
        vector = [0] * d
        vector[degree_two[i, j]] = 1
        brackets[i, j] = tuple(vector)
        for k in range(m):
            vector = [0] * d
            if k >= i:
                vector[degree_three[k, i, j]] = 1
            else:
                vector[degree_three[i, k, j]] = 1
                vector[degree_three[j, k, i]] = p-1
            brackets[k, degree_two[i, j]] = tuple(vector)
    return ClassThreeBCH(p, m, d-m, brackets)


def coset_fixture(group, generator, representative):
    """Secret-bearing fixture ONLY; generator is a logarithmic group coordinate."""
    if not any(generator):
        raise ValueError("nontrivial order-p generator required")
    return {group.bch(representative, group.scale(t, generator)): complex(1/sqrt(group.p))
            for t in range(group.p)}


def potential_fixture(group, generator, q):
    """Unknown proof witness, never passed to either public controller."""
    v, _ = group.to_chart(generator)
    if not any(v):
        raise ValueError("nonzero quotient image required")
    pivot = next(i for i, value in enumerate(v) if value)
    t = q[pivot] * pow(v[pivot], -1, group.p) % group.p
    perpendicular = group.add(q, group.scale(-t, v))
    _, orbit = group.to_chart(group.scale(t, generator))
    return group.add(group.action(perpendicular, orbit),
                     group.cocycle(perpendicular, group.scale(t, v)))


def partial_fourier_branch(group, source, label):
    """Actual partial QFT on the public derived-ideal chart."""
    _canonical(label, group.n, group.p)
    result = {}
    for logarithm, amplitude in source.items():
        q, normal = group.to_chart(logarithm)
        phase = sum(a*b for a, b in zip(label, normal)) % group.p
        result[q] = result.get(q, 0j) + amplitude * np.exp(2j*np.pi*phase/group.p)
    norm = sum(abs(a)**2 for a in result.values())
    if norm < 1e-20:
        return {}, 0.0
    return {q: a/sqrt(norm) for q, a in result.items()}, norm / group.p**group.n


def graph_branches(group, source, learned_direction, *, omit_cocycle=False):
    """Public corrected relabeling, using ONLY an already-learned direction."""
    v, p = tuple(learned_direction), group.p
    _canonical(v, group.m, p)
    if not any(v):
        raise ValueError("nonzero learned direction required")
    pivot = next(i for i, value in enumerate(v) if value)
    inverse = pow(v[pivot], -1, p)
    branches = {}
    for logarithm, amplitude in source.items():
        q, normal = group.to_chart(logarithm)
        t = q[pivot] * inverse % p
        perpendicular = group.add(q, group.scale(-t, v))
        correction = ((0,) * group.n if omit_cocycle else
                      group.cocycle(perpendicular, group.scale(t, v)))
        transformed = group.action(group.scale(-1, perpendicular),
                                   group.add(normal, group.scale(-1, correction)))
        branch = branches.setdefault(perpendicular, {})
        key = (t,) + transformed
        branch[key] = branch.get(key, 0j) + amplitude
    return branches


def sample_fourier(p, state, rng):
    """Finite Born simulation, exponential in width*log(p), not a gate routine."""
    width = len(next(iter(state)))
    if p**width > 100000:
        raise ValueError("finite Fourier diagnostic cap")
    frequencies, probabilities = [], []
    for f in product(range(p), repeat=width):
        amplitude = sum(a * np.exp(-2j*np.pi*(sum(x*y for x, y in zip(f, q)) % p)/p)
                        for q, a in state.items()) / sqrt(p**width)
        frequencies.append(f)
        probabilities.append(abs(amplitude)**2)
    return rng.choices(frequencies, weights=probabilities, k=1)[0]


def learn_quotient_line(group, source, rng):
    """Controller interface has no hidden generator, representative or potential."""
    p = group.p
    if p % 12 != 11:
        raise ValueError("implemented phase controller requires p=11 mod12")
    budget = copy_budget(group.m, group.n)
    ledger = {"source_copies": 0, "zero_fourier_labels": 0,
              "merges": {"3": 0, "2": 0, "1": 0},
              "single_active_merges": {"3": 0, "2": 0, "1": 0},
              "max_equation_rank": {"3": 0, "2": 0, "1": 0},
              "fourier_samples": [], "max_final_phase_error": 0.0}

    def produce(degree):
        if degree == 4:
            original = source()
            label = tuple(rng.randrange(p) for _ in range(group.n))
            state, probability = partial_fourier_branch(group, original, label)
            if len(state) != p or abs(probability*p**group.n - 1) > 1e-9:
                raise ValueError("nonzero quotient-line source promise failed")
            ledger["source_copies"] += 1
            ledger["zero_fourier_labels"] += int(not any(label))
            return state, initial_packet(p, group.m, label)
        inputs = [produce(degree + 1) for _ in range(budget[str(degree)])]
        states, packets = map(list, zip(*inputs))
        weights, rank = cancellation_weights(packets, degree, rng)
        result, packet, _, _ = sample_merge(p, states, packets, weights, rng)
        if packet.degree >= degree or len(result) != p:
            raise ArithmeticError("phase-erasure degree/support invariant failed")
        key = str(degree)
        ledger["merges"][key] += 1
        ledger["single_active_merges"][key] += int(sum(bool(c) for c in weights) == 1)
        ledger["max_equation_rank"][key] = max(ledger["max_equation_rank"][key], rank)
        return result, packet

    for _ in range(group.m + 16):
        state, _ = produce(1)
        anchor = next(iter(state.values()))
        ledger["max_final_phase_error"] = max(ledger["max_final_phase_error"],
                                              max(abs(a/anchor - 1) for a in state.values()))
        frequency = sample_fourier(p, state, rng)
        ledger["fourier_samples"].append(frequency)
        solution = affine_solution(p, ledger["fourier_samples"],
                                   [0] * len(ledger["fourier_samples"]), group.m)
        if len(solution["basis"]) == 1:
            return tuple(solution["basis"][0]), ledger
        if not solution["basis"]:
            raise ArithmeticError("Fourier samples contradicted the nontrivial line promise")
    raise ArithmeticError("charged finite Fourier-learning attempt cap reached")


def learn_normal_generator(group, source, direction, rng):
    """Known quadratic HPGP phase learning after the quotient direction is known.

    If h=(w,v), g_h(t)=t*w+(t^2-t)/2 * D_v*w. Maintain an affine space of
    possible w, cancel its known offset physically, and extract one equation
    per successful quadratic merge. Uninformative outcomes are charged.
    """
    p, n = group.p, group.n
    offset = [0] * n
    basis = [[int(i == j) for i in range(n)] for j in range(n)]
    columns = [group.bracket(group.lift(direction),
                            group.ideal(tuple(int(i == j) for i in range(n))))[group.m:]
               for j in range(n)]
    ledger = {"source_copies": 0, "zero_coefficient_packets": 0,
              "zero_equation_outputs": 0, "equations": [], "quadratic_merges": 0,
              "direct_linear_packets": 0}

    def packet_source():
        branches = graph_branches(group, source(), direction)
        ledger["source_copies"] += 1
        probabilities = [sum(abs(a)**2 for a in state.values()) for state in branches.values()]
        graph = rng.choices(list(branches.values()), weights=probabilities, k=1)[0]
        if len(graph) != p or len({key[0] for key in graph}) != p:
            raise ValueError("learned direction did not yield a full graph state")
        norm = sum(abs(a)**2 for a in graph.values())
        label = [rng.randrange(p) for _ in range(n)]
        quadratic = [sum(a*b for a, b in zip(label, col)) * pow(2, -1, p) % p for col in columns]
        linear = [(a-b) % p for a, b in zip(label, quadratic)]
        rows = [tuple(sum(a*b for a, b in zip(row, vector)) % p for vector in basis)
                for row in (linear, quadratic)]
        packet = PhasePacket(p, 1, len(basis), {(1,): rows[0], (2,): rows[1]})
        state = {}
        for key, amplitude in graph.items():
            t, normal = key[0], key[1:]
            known = sum(a*b for a, b in zip(offset, linear))*t
            known += sum(a*b for a, b in zip(offset, quadratic))*t*t
            phase = (sum(a*b for a, b in zip(label, normal)) - known) % p
            state[(t,)] = amplitude/sqrt(norm) * np.exp(2j*np.pi*phase/p)
        return state, packet

    while basis:
        dimension, success = len(basis), False
        for _ in range(32):
            states, packets = [], []
            for _ in range(2 * (dimension + 1)**2):
                state, packet = packet_source()
                if not packet.degree:
                    ledger["zero_coefficient_packets"] += 1
                    continue
                if packet.degree == 1:
                    states, packets = [state], [packet]
                    ledger["direct_linear_packets"] += 1
                    break
                states.append(state)
                packets.append(packet)
                if len(packets) == (dimension + 1)**2:
                    break
            if not packets or (packets[0].degree == 2 and len(packets) < (dimension+1)**2):
                continue
            if len(packets) == 1:
                state, packet = states[0], packets[0]
            else:
                weights, _ = cancellation_weights(packets, 2, rng)
                state, packet, _, _ = sample_merge(p, states, packets, weights, rng)
                ledger["quadratic_merges"] += 1
            if packet.degree > 1:
                raise ArithmeticError("known HPGP quadratic cancellation failed")
            equation = packet.coefficients.get((1,), (0,) * dimension)
            if not any(equation):
                ledger["zero_equation_outputs"] += 1
                continue
            value = sample_fourier(p, state, rng)[0]
            restriction = affine_solution(p, [equation], [value], dimension)
            new_offset = [sum(row[i]*c for row, c in zip(basis, restriction["offset"])) % p for i in range(n)]
            offset = [(a+b) % p for a, b in zip(offset, new_offset)]
            basis = [[sum(row[i]*c for row, c in zip(basis, vector)) % p for i in range(n)]
                     for vector in restriction["basis"]]
            ledger["equations"].append({"remaining_dimension_before": dimension,
                                         "coefficients": list(equation), "value": value})
            success = True
            break
        if not success:
            raise ArithmeticError("charged finite HPGP attempt cap reached")
    return tuple(offset), ledger


def controls(seed=20261022):
    group = free_two_step_three()
    generator = (1, 2, 3, 4, 5)
    source_rng, receiver_rng = random.Random(seed), random.Random(seed + 1)
    used = 0

    def source():
        nonlocal used
        used += 1
        representative = tuple(source_rng.randrange(group.p) for _ in group.zero)
        return coset_fixture(group, generator, representative)

    direction, erasure = learn_quotient_line(group, source, receiver_rng)
    normal, learning = learn_normal_generator(group, source, direction, receiver_rng)
    recovered = group.from_chart(direction, normal)
    correct = recovered in {group.scale(t, generator) for t in range(1, group.p)}
    if used != erasure["source_copies"] + learning["source_copies"]:
        raise ArithmeticError("unaccounted original source copies")
    return {
        "status": "NONSPLIT_CLASS_THREE_CONSTRUCTIVE_DERIVATION_REVIEW_PENDING",
        "prime": group.p, "quotient_dimension": group.m, "derived_dimension": group.n,
        "source_seed": seed, "receiver_seed": seed + 1,
        "group": "free class-three Lie algebra on two generators, BCH group",
        "split_over_derived_ideal": False,
        "generator_fixture": list(generator), "learned_direction": list(direction),
        "learned_normal_coordinate": list(normal), "recovered_log_generator": list(recovered),
        "recovered_same_hidden_subgroup": correct, "original_coset_copies": used,
        "quotient_erasure": erasure, "known_quadratic_hpgp": learning,
        "new_phase_erasure_controller_changed": False,
        "hidden_data_supplied_to_controllers": False,
        "full_finite_generator_recovery_executed": True,
        "compiled_quantum_algorithm_executed": False,
        "novelty_established": False, "external_problem_reduction_established": False,
        "scope": "explicit adapted class-three Lie presentation, cyclic H outside derived ideal, p=11mod12 controller",
        "not_claimed": [
            "black-box group to Lie-presentation algorithm",
            "arbitrary hidden subgroup reduction implemented",
            "general nilpotent or DCP algorithm",
            "classical runtime advantage from finite sparse simulation",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = controls()
    if args.write:
        REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
