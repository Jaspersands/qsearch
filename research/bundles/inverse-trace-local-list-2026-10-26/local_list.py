"""Single-copy local list bounds, not a native solver or quantum hardness test.

The scalable certificate uses the binary Kloosterman Weil bound. Exact
finite controls enumerate the entire alphabet and are explicitly capped.
"""

from dataclasses import dataclass
from fractions import Fraction
import importlib.util
from math import isqrt
from pathlib import Path
import sys

from flint import fmpq_mat


ROOT = Path(__file__).resolve().parent
DEPENDENCY = ROOT.parent / "inverse-trace-residual-2026-10-23/residual_sat.py"
SPEC = importlib.util.spec_from_file_location("local_list_native_field", DEPENDENCY)
NATIVE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = NATIVE
SPEC.loader.exec_module(NATIVE)


def exact_rational(value):
    if type(value) not in (int, Fraction):
        raise ValueError("an exact integer or Fraction is required")
    return Fraction(value)


def parameters(bits):
    if type(bits) is not int or bits < 2:
        raise ValueError("binary field degree >= 2 required")
    q = 1 << bits
    return q, min(q, 1 + isqrt(4*q))


def posterior_bound(bits, list_size, *, prior="uniform_local"):
    """Bound per positive-mass outcome, under a uniform one-symbol prior."""
    if prior != "uniform_local":
        raise ValueError("no claim for a changed prior or global side information")
    q, envelope = parameters(bits)
    if type(list_size) is not int or not 0 <= list_size <= q:
        raise ValueError("list cardinality must be an integer between 0 and q")
    if list_size == 0:
        return Fraction(0)
    return min(Fraction(1), Fraction(1, 2) + Fraction((list_size-1)*envelope, 2*q))


def minimum_list_size(bits, confidence=Fraction(1)):
    """Necessary cardinality only; never a sufficiency or construction claim."""
    q, envelope = parameters(bits)
    confidence = exact_rational(confidence)
    if not 0 < confidence <= 1:
        raise ValueError("confidence must lie in (0,1]")
    if confidence <= Fraction(1, 2):
        return 1
    excess = (2*confidence-1)*q/envelope
    return 1 + (excess.numerator + excess.denominator - 1)//excess.denominator


@dataclass(frozen=True)
class FiniteAlphabet:
    field: object
    alphabet: tuple
    characters: tuple
    inverse_walsh: tuple
    native_inverse_trace_alphabet: bool

    @property
    def q(self):
        return self.field.order

    def labels(self, labels):
        labels = tuple(labels)
        for label in labels:
            self.field.element(label)
        if len(set(labels)) != len(labels):
            raise ValueError("a list is a set of distinct field labels")
        return labels

    def spectrum(self):
        return tuple(sum(self.characters[c][a] for a in self.alphabet)
                     for c in range(self.q))


def finite_alphabet(bits, modulus, *, control_alphabet=None):
    """Enumerates q^2 characters; <=128 symbols, never scalable evidence."""
    q, _ = parameters(bits)
    if q > 128:
        raise ValueError("finite control cap: q <= 128; use the analytic bound")
    field = NATIVE.BinaryField(bits, modulus)
    predicate = tuple(field.trace(field.inverse(a)) for a in range(q))
    native = tuple(a for a in range(q) if predicate[a])
    alphabet = native if control_alphabet is None else tuple(control_alphabet)
    if not alphabet:
        raise ValueError("nonempty finite control alphabet required")
    for a in alphabet:
        field.element(a)
    if len(set(alphabet)) != len(alphabet):
        raise ValueError("distinct alphabet elements required")
    characters = tuple(tuple(1-2*field.trace(field.multiply(a, b))
                             for a in range(q)) for b in range(q))
    walsh = tuple(sum((1-2*predicate[a])*characters[b][a] for a in range(q))
                  for b in range(q))
    return FiniteAlphabet(field, alphabet, characters, walsh, alphabet == native)


def unambiguous_subspace_dimension(control, labels):
    """Exact rank test for one possible effect, not a complete POVM search."""
    labels = frozenset(control.labels(labels))
    rows = [[control.characters[c][a] for a in control.alphabet]
            for c in range(control.q) if c not in labels]
    rank = fmpq_mat(rows).rank() if rows else 0
    return len(control.alphabet) - rank


def positive_effect_posterior(control, vectors, labels, *, prior="uniform_local"):
    """Exact real-rational controls for M=sum_v |v><v|, up to scaling.

    Each vector is indexed by control.alphabet. Any nonzero positive M
    can be rescaled to be a POVM effect without changing its posterior.
    The theorem also covers complex effects; these controls do not enumerate them.
    """
    if prior != "uniform_local":
        raise ValueError("uniform local prior required")
    labels = control.labels(labels)
    mass, listed = Fraction(0), Fraction(0)
    for vector in vectors:
        vector = tuple(exact_rational(value) for value in vector)
        if len(vector) != len(control.alphabet):
            raise ValueError("effect vector must be indexed by the alphabet")
        mass += sum(value*value for value in vector)
        for c in labels:
            amplitude = sum(control.characters[c][a]*v
                            for a, v in zip(control.alphabet, vector))
            listed += amplitude*amplitude
    if not mass:
        raise ValueError("outcome has zero probability; posterior is undefined")
    return listed/(control.q*mass)


def pair_optimum_witness(control, left, right):
    """The larger eigenvector of the exact two-label Gram matrix."""
    left, right = control.labels((left, right))
    cross = sum(control.characters[left ^ right][a] for a in control.alphabet)
    sign = 1 if cross >= 0 else -1
    return tuple(control.characters[left][a] + sign*control.characters[right][a]
                 for a in control.alphabet)


def fourier_readout_probabilities(control):
    """Shift-error law for a native halfset; still full-table finite work."""
    size = len(control.alphabet)
    return tuple(Fraction(value*value, control.q*size) for value in control.spectrum())
