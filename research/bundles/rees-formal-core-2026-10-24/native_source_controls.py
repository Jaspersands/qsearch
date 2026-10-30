"""Finite controls of the native-source interface, not a search algorithm."""

from fractions import Fraction
from itertools import product

import numpy as np


P = 3
GROUP = tuple(product(range(P), repeat=3))
COVER = tuple(product(range(P), repeat=4))
INDEX = {g: i for i, g in enumerate(GROUP)}


def mul(x, y):
    a, b, c = x
    u, v, w = y
    return ((a+u) % P, (b+v) % P, (c+w+2*(a*v-b*u)) % P)


def cover_mul(x, y):
    a, b, c, d = x
    u, v, w, t = y
    return ((a+u) % P, (b+v) % P, (c+w) % P, (d+t+2*(a*v-b*u)) % P)


def inv(x):
    return tuple(-a % P for a in x)


def evaluate(x, a):
    u, v, w, t = x
    return (a*u % P, a*v % P, (a*w+a*a*t) % P)


def hidden(family, g):
    if family == "trivial":
        return g == (0, 0, 0)
    if family == "nonhomogeneous_line":
        return g[1] == 0 and g[0] == g[2]
    if family == "full":
        return True
    raise ValueError("unknown control family")


def native_source(family):
    return np.array([[hidden(family, mul(inv(y), x)) for y in GROUP] for x in GROUP], dtype=float)/len(GROUP)


def literal_pullback(states, *, points=(1, 2), wrong_left=False):
    """Actual controlled permutations followed by target partial traces.

    No hidden subgroup is an argument to this operation. Its independent
    target contract is exactly the tensor product of the supplied states.
    """
    if len(states) != len(points) or any(np.shape(state) != (len(GROUP), len(GROUP)) for state in states):
        raise ValueError("one independent 27-dimensional target state per evaluation required")
    out = np.ones((len(COVER), len(COVER)))/len(COVER)
    for a, state in zip(points, states):
        indices = np.array([[INDEX[mul(evaluate(q, a), t) if wrong_left else mul(t, evaluate(q, a))]
                             for t in GROUP] for q in COVER])
        out *= np.asarray(state)[indices[:, None, :], indices[None, :, :]].sum(axis=-1)
    return out


def expected_source(family, points=(1, 2)):
    return np.array([[all(hidden(family, evaluate(cover_mul(inv(y), x), a)) for a in points)
                      for y in COVER] for x in COVER], dtype=float)/len(COVER)


def trace_distance(a, b):
    return float(np.abs(np.linalg.eigvalsh(a-b)).sum()/2)


def postselection_probability(prime, heisenberg_factors):
    if prime < 3 or prime % 2 == 0 or heisenberg_factors < 1:
        raise ValueError("positive factor count and an odd prime parameter are required")
    # Formula for a promised odd prime. No primality or group recognition
    # is inferred from this numerical resource calculation.
    return Fraction(1, prime**(2*heisenberg_factors))


def audit():
    errors = {}
    for family in ("trivial", "nonhomogeneous_line", "full"):
        source = native_source(family)
        actual = literal_pullback((source, source))
        expected = expected_source(family)
        error = float(np.max(np.abs(actual-expected)))
        if error > 1e-12 or abs(np.trace(actual)-1) > 1e-12:
            raise ArithmeticError("native acquisition control failed")
        errors[family] = error
    source = native_source("nonhomogeneous_line")
    correct = expected_source("nonhomogeneous_line")
    wrong_left = trace_distance(literal_pullback((source, source), wrong_left=True), correct)
    # The paired evaluation is injective, so retaining this public work
    # register before discarding it dephases the entire address.
    dirty = trace_distance(np.diag(np.diag(correct)), correct)
    if wrong_left < .1 or dirty < .1:
        raise ArithmeticError("adversarial interface control stopped falsifying its shortcut")
    return {
        "source_entry_errors": errors,
        "source_copies_per_top_preparation": 2,
        "enumerated_native_group_order": len(GROUP),
        "enumerated_cover_order": len(COVER),
        "wrong_left_translation_trace_distance": wrong_left,
        "retained_evaluation_work_trace_distance": dirty,
        "naive_projection_success_one_factor": str(postselection_probability(3, 1)),
        "naive_projection_success_ten_factors": str(postselection_probability(3, 10)),
        "finite_interface_controls_only": True,
        "quantum_execution": False,
        "new_algorithm_or_speedup_claim": False,
    }
