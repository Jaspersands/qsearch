"""Bounded full-matrix controls for mixed central-character descent.

This is a falsifier harness, NOT an HSP implementation or a general SDE
solver. The channel takes public group operations and observed labels;
hidden subgroups occur only in source/expected-output fixtures.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
from functools import cached_property
from itertools import product
import json
from math import prod
from pathlib import Path

import numpy as np

from theorems.prime_character_opi import ring


def check_moment(labels, scales, p, degree):
    """Validate a supplied public SDE witness, including its active support."""
    ring(p)
    if not isinstance(degree, int) or degree < 1:
        raise ValueError("positive degree required")
    if not labels or len(labels) != len(scales) or not labels[0]:
        raise ValueError("nonempty equal-length label/scale lists required")
    width = len(labels[0])
    if any(len(row) != width for row in labels):
        raise ValueError("inconsistent central rank")
    if any(type(x) is not int or not 0 <= x < p for row in labels for x in row):
        raise ValueError("canonical field labels required")
    if any(type(s) is not int or not 0 <= s < p for s in scales):
        raise ValueError("canonical field scales required")
    active = tuple(i for i, s in enumerate(scales) if s)
    if not active:
        raise ValueError("all-zero witness destroys the support test")
    if any(sum(row[j]*pow(s, degree, p) for row, s in zip(labels, scales)) % p for j in range(width)):
        raise ValueError("nonzero character moment")
    return active


def controlled_discard(rho, permutations):
    """Literal uniform-control/target-trace channel, not a predicted kernel.

permutations[q,x] is the output target basis index U_q|x>. Inverting
these permutations performs both target sums in the Kraus contraction.
"""
    rho = np.asarray(rho, dtype=complex)
    permutations = np.asarray(permutations)
    if rho.ndim != 2 or rho.shape[0] != rho.shape[1] or not 0 < len(rho) <= 1024:
        raise ValueError("bounded square density fixture required")
    if permutations.ndim != 2 or not len(permutations) or permutations.shape[1] != len(rho):
        raise ValueError("invalid controlled action shape")
    if not np.issubdtype(permutations.dtype, np.integer):
        raise ValueError("integer permutations required")
    if not np.all(np.sort(permutations, axis=1) == np.arange(len(rho))):
        raise ValueError("controlled action must be a permutation")
    pullbacks = np.argsort(permutations, axis=1)
    size = len(pullbacks)
    return np.array([[sum(rho[a, b])/size for b in pullbacks] for a in pullbacks])


@dataclass(frozen=True)
class HeisenbergFixture:
    """Actual UT3 group, coordinates (x,y,z), with an explicit size cap."""
    p: int

    def __post_init__(self):
        ring(self.p)
        if self.p < 3 or self.p**3 > 256:
            raise ValueError("odd-prime bounded matrix fixture only")

    @cached_property
    def elements(self):
        return tuple(product(range(self.p), repeat=3))

    @cached_property
    def index(self):
        return {g: i for i, g in enumerate(self.elements)}

    @cached_property
    def representatives(self):
        return tuple((x, y, 0) for x, y in product(range(self.p), repeat=2))

    def multiply(self, a, b):
        x, y, z = a
        X, Y, Z = b
        return ((x+X) % self.p, (y+Y) % self.p, (z+Z+x*Y) % self.p)

    def inverse(self, a):
        x, y, z = a
        return (-x % self.p, -y % self.p, (x*y-z) % self.p)

    def dilate(self, a, s):
        if not 0 < s < self.p:
            raise ValueError("only nonzero scales define automorphisms")
        x, y, z = a
        return (s*x % self.p, s*y % self.p, s*s*z % self.p)

    def right_permutation(self, g):
        return np.array([self.index[self.multiply(x, self.inverse(g))] for x in self.elements])

    def controls(self, s):
        return np.array([self.right_permutation(self.dilate(g, s)) for g in self.representatives])

    def line_fixture(self, central_slope=0):
        return tuple((t, t, (t*t*pow(2, -1, self.p)+central_slope*t) % self.p) for t in range(self.p))

    def coset_density_fixture(self, hidden):
        hidden = set(hidden)
        return np.array([[int(self.multiply(self.inverse(x), y) in hidden)/len(self.elements)
                          for y in self.elements] for x in self.elements], dtype=complex)

    def projector(self, label):
        if not 0 <= label < self.p:
            raise ValueError("canonical character required")
        matrix = np.zeros((len(self.elements),)*2, dtype=complex)
        columns = np.arange(len(self.elements))
        for z in range(self.p):
            matrix[self.right_permutation((0, 0, z)), columns] += np.exp(-2j*np.pi*label*z/self.p)/self.p
        return matrix

    def restored_fourier_projector(self, label):
        # Negative central Fourier, copy/measure its label, inverse QFT.
        columns = np.arange(self.p)
        fourier = np.exp(-2j*np.pi*np.outer(columns, columns)/self.p)/np.sqrt(self.p)
        row = fourier[label]
        return np.kron(np.eye(self.p**2), np.outer(row.conj(), row))

    def branches(self, rho):
        result = []
        for label in range(self.p):
            P = self.projector(label)
            branch = P @ rho @ P.conj().T
            mass = float(np.trace(branch).real)
            result.append((mass, branch/mass if mass > 1e-12 else None))
        return result

    def expected_quotient_fixture(self, hidden):
        support = {(g[0], g[1]) for g in hidden}
        return np.array([[int(((g[0]-h[0]) % self.p, (g[1]-h[1]) % self.p) in support)/self.p**2
                          for h in self.representatives] for g in self.representatives])


def exhaustive_scale_fixture(labels, p, degree):
    """Deliberately bounded exponential witness search; never a solver backend."""
    if p**len(labels) > 10000:
        raise ValueError("exhaustive falsifier fixture cap exceeded")
    for scales in product(range(p), repeat=len(labels)):
        if any(scales) and all(sum(row[j]*pow(s, degree, p) for row, s in zip(labels, scales)) % p == 0
                              for j in range(len(labels[0]))):
            check_moment(labels, scales, p, degree)
            return scales
    raise ValueError("no witness at this fixture arity")


def all_branch_control(p=5, central_slope=0):
    group = HeisenbergFixture(p)
    hidden = group.line_fixture(central_slope)
    branches = group.branches(group.coset_density_fixture(hidden))
    factors = {(label, s): controlled_discard(rho, group.controls(s))*p**2
               for label, (_, rho) in enumerate(branches) for s in range(1, p)}
    expected = group.expected_quotient_fixture(hidden)
    max_error = 0.0
    zero_scale_branches = 0
    for labels in product(range(p), repeat=3):
        vectors = tuple((label,) for label in labels)
        scales = exhaustive_scale_fixture(vectors, p, 2)
        active = check_moment(vectors, scales, p, 2)
        output = prod((factors[labels[i], scales[i]] for i in active))/p**2
        max_error = max(max_error, float(np.max(np.abs(output-expected))))
        zero_scale_branches += int(len(active) < 3)
    return {"prime": p, "complete_label_tuples": p**3,
            "zero_scale_branches": zero_scale_branches,
            "maximum_entry_error": max_error,
            "maximum_label_mass_error": max(abs(mass-1/p) for mass, _ in branches)}


def tree_budget(arities, leaf_error=Fraction(0), stage_errors=None):
    """Worst-case fresh-copy tree and unconditional trace-distance bound.

Stages are in execution order (highest grade first). Stage error includes
its complete adaptive instrument and explicit abort flag, not normalized
rare branches. All arities count consumed zero-weight inputs as well.
"""
    arities = tuple(arities)
    if any(type(a) is not int or a < 1 for a in arities):
        raise ValueError("positive integral arities required")
    errors = tuple(stage_errors) if stage_errors is not None else (Fraction(0),)*len(arities)
    if len(errors) != len(arities) or leaf_error < 0 or any(e < 0 for e in errors):
        raise ValueError("one nonnegative error per complete stage required")
    counts = []
    leaves = 1
    for a in reversed(arities):
        counts.append(leaves)
        leaves *= a
    counts.reverse()
    bound = leaves*leaf_error+sum(count*error for count, error in zip(counts, errors))
    return {"source_leaves": leaves, "stage_calls": tuple(counts),
            "total_instrument_calls": leaves+sum(counts),
            "trace_distance_bound": min(Fraction(1), bound)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    controls = [all_branch_control(p) for p in (3, 5)]
    wrong = all_branch_control(5, central_slope=1)
    if any(row["maximum_entry_error"] > 1e-10 for row in controls) or wrong["maximum_entry_error"] < 1e-3:
        raise RuntimeError("central descent control or preservation falsifier failed")
    report = {"status": "mixed_channel_identity_with_explicit_contracts_not_discovery",
              "controls": controls, "nonpreserved_hidden_subgroup_falsifier": wrong,
              "formal_module": "formal/Formal/CentralCharacterDescent.lean",
              "research_note": "research/CENTRAL_CHARACTER_DESCENT.md",
              "no_general_sde_implementation": True, "no_speedup_claim": True,
              "remaining": ["arbitrary-H recursion refinement", "independent whole-proof and novelty review",
                            "hard application and classical comparison", "quantum synthesis and SDE implementation"]}
    if args.write:
        path = Path(__file__).resolve().parents[1]/"research/reductions/central_character_descent.json"
        path.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
