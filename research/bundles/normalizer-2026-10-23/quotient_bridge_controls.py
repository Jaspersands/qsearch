"""Bounded falsification controls, not scalable black-box HSP software."""

from fractions import Fraction
from itertools import product
from math import sqrt

import numpy as np
from flint import fmpz_mod_ctx, fmpz_mod_mat

from abelian_action_normalizer import AbelianAction


def null_rows(rows, width, p):
    if not rows:
        return tuple(tuple(int(i == j) for j in range(width)) for i in range(width))
    matrix = fmpz_mod_mat(rows, fmpz_mod_ctx(p))
    reduced, rank = matrix.rref()
    values = [[int(reduced[i, j]) for j in range(width)] for i in range(rank)]
    pivots = [next(j for j, value in enumerate(row) if value) for row in values]
    out = []
    for free in set(range(width)) - set(pivots):
        vector = [0] * width
        vector[free] = 1
        for row, pivot in zip(values, pivots):
            vector[pivot] = -row[free] % p
        out.append(tuple(vector))
    return tuple(out)


def span_rows(rows, width, p):
    return null_rows(null_rows(rows, width, p), width, p)


def ideal_abelian_control(p, dimension, oracle, seed=23, samples=16):
    """Numerical finite-register Fourier simulation from actual oracle labels.

    This enumerates p**dimension addresses and is not the claimed efficient
    implementation. No hidden intersection is accepted as an argument.
    """
    if p**dimension > 2048:
        raise ValueError("bounded control only; no field-size campaign")
    addresses = tuple(product(range(p), repeat=dimension))
    labels = tuple(oracle(x) for x in addresses)
    shape = (p,) * dimension
    probability = np.zeros(shape)
    for label in set(labels):
        mask = np.array([int(x == label) for x in labels]).reshape(shape)
        probability += abs(np.fft.fftn(mask))**2 / len(addresses)**2
    total = float(probability.sum())
    if abs(total - 1) > 1e-10:
        raise ArithmeticError("Fourier distribution lost normalization")
    # Roundoff below this threshold is removed only in this numerical control.
    clipped = np.where(probability < 1e-12, 0.0, probability).ravel()
    clipped /= clipped.sum()
    rng = np.random.default_rng(seed)
    selected = rng.choice(len(addresses), size=samples, p=clipped)
    outcomes = tuple(addresses[int(i)] for i in selected)
    inferred = null_rows(outcomes, dimension, p)
    return inferred, probability, outcomes


class FreeClassThreeControl:
    """Free class-three BCH group on X,Y over F_7, only as a finite control.

    Coordinates are X,Y,Z=[X,Y],U=[X,Z],V=[Y,Z]. The fixed control secret
    is <X,Z,U>, conjugated by exp(tY). It is not a research problem family.
    """

    p = 7
    zero = (0, 0, 0, 0, 0)

    def multiply(self, x, y):
        p = self.p
        a, b, c, d, e = x
        A, B, C, D, E = y
        z = a*B - b*A
        half, twelfth = pow(2, -1, p), pow(12, -1, p)
        return ( (a+A) % p, (b+B) % p, (c+C+half*z) % p,
                 (d+D+half*(a*C-c*A)+twelfth*z*(a-A)) % p,
                 (e+E+half*(b*C-c*B)+twelfth*z*(b-B)) % p )

    def inverse(self, g):
        return tuple(-x % self.p for x in g)

    def conjugate(self, g, x):
        return self.multiply(self.multiply(g, x), self.inverse(g))

    def oracle(self, conjugation=0):
        q = (0, conjugation % self.p, 0, 0, 0)

        def evaluate(g):
            a, b, c, _, e = self.conjugate(self.inverse(q), g)
            return b, (e - b*c*pow(2, -1, self.p)
                       - a*b*b*pow(6, -1, self.p)) % self.p
        return evaluate

    def action(self, g):
        out = []
        for j in range(3):
            vector = (0, 0) + tuple(int(i == j) for i in range(3))
            value = self.conjugate(g, vector)
            if value[:2] != (0, 0):
                raise ArithmeticError("control A ceased to be normal")
            out.append(value[2:])
        return tuple(tuple(out[j][i] for j in range(3)) for i in range(3))

    def lift_action(self, matrix):
        # Public, fixture-specific word lift. The general proof instead pays
        # for constructive membership returning a straight-line program.
        g = (matrix[1][0], matrix[2][0], 0, 0, 0)
        if self.action(g) != matrix:
            raise ValueError("matrix not in the public control action image")
        return g


def reduction_control(conjugation=1, seed=23):
    group = FreeClassThreeControl()
    p = group.p
    oracle = group.oracle(conjugation)
    action = AbelianAction(p, (1, 1, 1))
    x, y = (1, 0, 0, 0, 0), (0, 1, 0, 0, 0)
    intersection, first_probability, first_samples = ideal_abelian_control(
        p, 3, lambda v: oracle((0, 0) + v), seed=seed)
    if len(intersection) != 2:
        raise ArithmeticError("finite Fourier sample failed to learn the full intersection")
    if not all(oracle((0, 0)+v) == oracle(group.zero) for v in intersection):
        raise ArithmeticError("inferred intersection failed native membership")
    normalizer = action.stabilizer((group.action(x), group.action(y)), intersection)
    lifts = tuple(group.lift_action(m) for m in normalizer.stabilizer_group_generators)
    if normalizer.stabilizer_order != p or any(g[1] for g in lifts):
        raise ArithmeticError("unexpected normalizer in this fixed control")

    annihilator = null_rows(intersection, 3, p)
    if len(annihilator) != 1 or annihilator[0][2] == 0:
        raise ArithmeticError("unexpected quotient chart")
    ell = tuple(z * pow(annihilator[0][2], -1, p) % p for z in annihilator[0])

    def project(g):
        if g[1] != 0:
            raise ValueError("element lies outside the normalizer")
        return g[0], sum(a*b for a, b in zip(ell, g[2:])) % p

    def section(v):
        a, value = v
        # Intentionally nonhomomorphic: the Z coordinate depends on value.
        return a, 0, value, 0, (value - ell[0]*value) % p

    terminal, second_probability, second_samples = ideal_abelian_control(
        p, 2, lambda v: oracle(section(v)), seed=seed+1)
    answer = tuple((0, 0)+v for v in intersection) + tuple(section(v) for v in terminal)
    if not all(oracle(g) == oracle(group.zero) for g in answer):
        raise ArithmeticError("pulled-back answer failed native membership")
    return {
        "group": group, "oracle": oracle, "intersection": intersection,
        "action_result": normalizer, "lifts": lifts,
        "project": project, "section": section, "terminal": terminal,
        "answer": answer, "first_probability": first_probability,
        "second_probability": second_probability,
        "first_samples": first_samples, "second_samples": second_samples,
    }


def clean_compiler_error(unitaries, answers, output_bits=1, arbitrary_target=False):
    """Retained-input compiler norm, with initialized workspace.

    The default also initializes the target to zero. With arbitrary_target,
    take the operator norm over its entire input space, not just basis states.
    """
    if len(unitaries) != len(answers) or output_bits < 1:
        raise ValueError("invalid compiler input/answer specification")
    errors, failures = [], []
    outputs = 1 << output_bits
    for unitary, answer in zip(unitaries, answers):
        unitary = np.asarray(unitary, dtype=complex)
        dimension = len(unitary)
        if not 0 <= answer < outputs:
            raise ValueError("answer outside output register")
        if (unitary.shape != (dimension, dimension) or dimension % outputs
                or not np.allclose(unitary.conj().T @ unitary, np.eye(dimension))):
            raise ValueError("invalid workspace unitary")
        initial = unitary[:, 0]
        copied = np.zeros((dimension, outputs, outputs), dtype=complex)
        for w, amplitude in enumerate(initial):
            for target in range(outputs):
                copied[w, (w % outputs) ^ target, target] = amplitude
        cleaned = np.einsum("vw,wyz->vyz", unitary.conj().T, copied)
        ideal = np.zeros_like(cleaned)
        for target in range(outputs):
            ideal[0, target ^ answer, target] = 1
        difference = cleaned - ideal
        error = (np.linalg.norm(difference.reshape(dimension*outputs, outputs), 2)
                 if arbitrary_target else np.linalg.norm(difference[:, :, 0]))
        errors.append(float(error))
        failures.append(float(sum(abs(z)**2 for w, z in enumerate(initial)
                                  if w % outputs != answer)))
    # Orthogonal retained-input blocks make the full operator norm their max.
    return max(errors, default=0.0), max(failures, default=0.0)


def in_place_householder_falsifier(dimension):
    """Exact discrepancy for compute/copy/uncompute WITHOUT retained input."""
    if dimension < 2:
        raise ValueError("dimension must be at least two")
    delta = Fraction(4*(dimension-1), dimension**2)
    superposition_error_squared = Fraction(4*(dimension-1), dimension)
    return {
        "basis_failure_probability": delta,
        "basis_column_error": sqrt(2*float(delta)),
        "uniform_input_error": sqrt(float(superposition_error_squared)),
        "uniform_input_error_squared": superposition_error_squared,
        "uniform_input_trace_distance": 2*sqrt(float(delta)),
        "balanced_witness_overlap": Fraction(0),
        "balanced_witness_trace_distance": 2,
    }
