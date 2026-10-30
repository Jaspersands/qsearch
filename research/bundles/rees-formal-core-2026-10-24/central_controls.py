"""Finite falsification controls for the central-instrument proof, not HSP search."""

import argparse
from functools import lru_cache
import hashlib
from itertools import product
import json
from pathlib import Path

import numpy as np


GROUP = tuple(product(range(3), repeat=4))
INDEX = {g: i for i, g in enumerate(GROUP)}
CENTER = tuple(product(range(3), repeat=2))
ADDRESSES = tuple(product(range(3), repeat=2))


def mul(g, h):
    x, y, z, w = g
    a, b, c, d = h
    return ((x+a) % 3, (y+b) % 3, (z+c+x*b) % 3, (w+d) % 3)


def inv(g):
    x, y, z, w = g
    return ((-x) % 3, (-y) % 3, (x*y-z) % 3, (-w) % 3)


def embed(z):
    return (0, 0, *z)


def character(label, z):
    return np.exp(2j*np.pi*sum(a*b for a, b in zip(label, z))/3)


@lru_cache(None)
def right_regular(g):
    matrix = np.zeros((81, 81), dtype=complex)
    for i, x in enumerate(GROUP):
        matrix[INDEX[mul(x, inv(g))], i] = 1
    matrix.flags.writeable = False
    return matrix


@lru_cache(None)
def projector(label):
    # Matches spectralAction exactly; a sign reversal merely relabels sectors.
    matrix = sum(character(label, z)*right_regular(inv(embed(z))) for z in CENTER)/9
    matrix.flags.writeable = False
    return matrix


def oracle_source(family):
    labels = {
        "trivial": lambda g: g,
        "proper_intersection": lambda g: (g[1], g[3]),
        "full_center": lambda g: g[:2],
    }
    label = labels[family]
    values = [label(g) for g in GROUP]
    # Trace the output of the ordinary uniform hiding-function query.
    return np.array([[a == b for b in values] for a in values], dtype=complex)/81


def hidden_elements(family):
    return {
        "trivial": {(0, 0, 0, 0)},
        "proper_intersection": {(x, 0, z, 0) for x in range(3) for z in range(3)},
        "full_center": {embed(z) for z in CENTER},
    }[family]


def coefficient(family, label, g):
    hidden = hidden_elements(family)
    return sum(character(label, z) for z in CENTER if mul(g, inv(embed(z))) in hidden)


def measured_branches(family):
    source = oracle_source(family)
    return {label: projector(label)@source@projector(label).conj().T for label in CENTER}


def scales(labels):
    for candidate in product(range(3), repeat=3):
        if any(candidate) and all(sum(s*s*label[j] for s, label in zip(candidate, labels)) % 3 == 0
                                  for j in range(2)):
            return candidate
    raise ValueError("no nonzero moment solution for this record")


def action(q, s, twisted):
    x, y = q
    z, w = ((x*y) % 3, (x+y*y) % 3) if twisted else (0, 0)
    return (s*x % 3, s*y % 3, s*s*z % 3, s*s*w % 3)


def discard_gram(tau, s, twisted):
    # Direct target partial trace after the controlled permutations.
    permutations = [[INDEX[mul(t, action(q, s, twisted))] for t in GROUP] for q in ADDRESSES]
    return np.array([[sum(tau[x, y] for x, y in zip(left, right))
                      for right in permutations] for left in permutations])


def apply_reference(gram, rho, reference):
    return (rho.reshape(9, reference, 9, reference)*gram[:, None, :, None]).reshape(rho.shape)


def audit():
    branches = measured_branches("proper_intersection")
    masses = {label: float(np.trace(tau).real) for label, tau in branches.items()}
    allowed = {label for label in CENTER if label[0] == 0}
    target = np.array([[q[1] == r[1] for r in ADDRESSES] for q in ADDRESSES], dtype=float)
    worst = 0.
    positive = forbidden = 0
    total = np.zeros((9, 9), dtype=complex)
    complete_mass = 0.
    grams = {(label, s, twist): discard_gram(tau, s, twist)
             for label, tau in branches.items() for s in range(3) for twist in (False, True)}
    for labels in product(CENTER, repeat=3):
        valid = all(label in allowed for label in labels)
        if valid:
            positive += 1
            selected = scales(labels)
        else:
            forbidden += 1
            selected = (0, 0, 0)  # Impossible outcomes need no conditional solver.
        mass = np.prod([masses[label] for label in labels]) if valid else 0.
        for twist in (False, True):
            actual = np.prod([grams[label, s, twist] for label, s in zip(labels, selected)], axis=0)
            worst = max(worst, float(np.max(np.abs(actual-mass*target))))
            if twist:
                total += actual
        complete_mass += mass
    projectors = [projector(label) for label in CENTER]
    return {
        "scope": "UT3(F3) x C3; exact finite model evaluated in floating point",
        "group_order": 81, "central_order": 9, "intersection_order": 3,
        "central_outcomes": 9, "positive_records": positive, "zero_mass_records": forbidden,
        "complete_record_mass": float(complete_mass),
        "maximum_record_entry_error": worst,
        "complete_channel_entry_error": float(np.max(np.abs(total-target))),
        "kraus_completeness_error": float(np.max(np.abs(sum(p.conj().T@p for p in projectors)-np.eye(81)))),
        "forbidden_branch_norm": max(float(np.linalg.norm(branches[label])) for label in CENTER if label not in allowed),
        "allowed_mass_error": max(abs(masses[label]-1/3) for label in allowed),
        "joint_source_assumption": "independent copies; marginal guarantees do not suffice",
        "new_algorithm_or_speedup_claim": False, "quantum_execution": False,
        "formal_proof_receipt": "receipt.json",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = audit()
    root = Path(__file__).resolve().parent
    result["source_sha256"] = {name: hashlib.sha256((root/name).read_bytes()).hexdigest()
                               for name in ("central_controls.py", "test_central_controls.py")}
    payload = json.dumps(result, indent=2, sort_keys=True)+"\n"
    if args.output:
        args.output.write_text(payload)
    print(payload, end="")
