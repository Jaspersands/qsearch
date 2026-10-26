"""Variable-radical public algebra for a proposed class-four HSP source.

No HSP solver or hidden coefficients are supplied. Alternating forms encode
the public bracket on N/Z(N), where N is a class-two normal group. See the
accompanying research note for the probabilistic and source obligations.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from theorems.prime_character_opi import ring
from theorems.ut5_matrix_phase_alignment import (
    _basis, _canonical, _identity, _lists, _matrix, _rank, _transpose,
    align_jet_maps,
)


def _pair(form, a, b, p):
    return sum(x*form[i][j]*y for i, x in enumerate(a) for j, y in enumerate(b)) % p


@dataclass(frozen=True)
class AlternatingCoordinates:
    weyl: tuple[tuple[int, ...], ...]
    radical: tuple[tuple[int, ...], ...]

    @property
    def qudits(self):
        return len(self.weyl)//2


def factor_alternating(p, form):
    """Public congruence factorization F=D^T Omega D, with radical coordinates."""
    ring(p)
    if not form:
        raise ValueError("positive alternating-form width required")
    w = len(form)
    for row in form:
        _canonical(row, w, p)
    if any(form[i][i] or any((form[i][j]+form[j][i]) % p for j in range(w)) for i in range(w)):
        raise ValueError("alternating form required")
    remaining, first, second = _identity(w), [], []
    while True:
        pair = next(((a, b) for a in remaining for b in remaining if _pair(form, a, b, p)), None)
        if pair is None:
            break
        a, b = pair
        inverse = pow(_pair(form, a, b, p), -1, p)
        b = [x*inverse % p for x in b]
        first.append(a)
        second.append(b)
        projected = []
        for v in remaining:
            ab, aa = _pair(form, v, b, p), _pair(form, v, a, p)
            projected.append([(t-ab*x+aa*y) % p for t, x, y in zip(v, a, b)])
        remaining = _basis(projected, p)
    inverse = _lists(_matrix(_transpose(second+first+remaining), p).inv())
    split = 2*len(first)
    return AlternatingCoordinates(tuple(map(tuple, inverse[:split])), tuple(map(tuple, inverse[split:])))


def label_coordinates(p, forms, label):
    _canonical(label, len(forms), p)
    w = len(forms[0])
    form = [[sum(c*F[i][j] for c, F in zip(label, forms)) % p for j in range(w)] for i in range(w)]
    return factor_alternating(p, form)


def rank_failure_bound(p, noncentral_width, quotient_width, blocks):
    """Union bound for the documented equivariant independent-block schedule."""
    ring(p)
    if p <= 4 or any(type(x) is not int or x < 1 for x in (noncentral_width, quotient_width, blocks)):
        raise ValueError("p>4 and positive dimensions/block count required")
    L = noncentral_width*(quotient_width+2)
    return min(Fraction(1), (p**L-1)*Fraction(2, p)**blocks)


@dataclass(frozen=True)
class VariableJetMaps:
    p: int
    noncentral_width: int
    quotient_width: int
    active_indices: tuple[int, ...]
    representations: tuple[AlternatingCoordinates, ...]
    source_carrier_width: int
    carrier_width: int
    quadratic: tuple[tuple[int, ...], ...]
    linear: tuple[tuple[int, ...], ...]

    @property
    def jet_width(self):
        return self.noncentral_width*(self.quotient_width+1)

    @property
    def mixed_padding_qudits(self):
        return self.carrier_width-self.source_carrier_width


def variable_jet_maps(p, forms, labels, scales, outcomes):
    """Build verified K/J for varying-rank irreps; padding denotes I/p, not |0>."""
    ring(p)
    if p <= 4 or not forms or not forms[0] or not labels or not outcomes or not outcomes[0]:
        raise ValueError("p>4 and positive dimensions required")
    w, z, m = len(forms[0]), len(forms), len(outcomes[0])
    for F in forms:
        if len(F) != w:
            raise ValueError("matching public bracket dimensions required")
        factor_alternating(p, F)
    if _rank([row for F in forms for row in F], p) != w:
        raise ValueError("common radical must be removed into Z(N) first")
    if len(labels) != len(scales) or len(labels) != len(outcomes):
        raise ValueError("matching labels/scales/outcomes required")
    _canonical(scales, len(labels), p)
    for label, y in zip(labels, outcomes):
        _canonical(label, z, p)
        _canonical(y, m, p)
        if not any(label):
            raise ValueError("zero central vectors are rejected before relation selection")
    active = tuple(i for i, s in enumerate(scales) if s)
    if not active or any(sum(pow(s, 4, p)*label[j] for s, label in zip(scales, labels)) % p for j in range(z)):
        raise ValueError("nonzero verified quartic label relation required")
    coordinates = tuple(label_coordinates(p, forms, labels[i]) for i in active)
    physical = sum(c.qudits for c in coordinates)
    D, R = w*(m+1), max(physical, w*(m+2))
    K, J = [[0]*w for _ in range(2*R)], [[0]*D for _ in range(2*R)]
    start = 0
    for source, coordinate in zip(active, coordinates):
        s, y, t = scales[source], outcomes[source], coordinate.qudits
        for j, row in enumerate(coordinate.weyl):
            output = start+j if j < t else R+start+j-t
            K[output] = [s*s*x % p for x in row]
            J[output] = [s*coefficient*x % p for coefficient in [1]+list(y) for x in row]
        start += t
    if _rank([a+b for a, b in zip(K, J)], p) != w+D:
        raise ValueError("public variable-radical jet design is rank deficient")
    return VariableJetMaps(p, w, m, active, coordinates, physical, R,
                           tuple(map(tuple, K)), tuple(map(tuple, J)))


def align_variable_jets(p, forms, labels, scales, outcomes):
    maps = variable_jet_maps(p, forms, labels, scales, outcomes)
    return align_jet_maps(maps)
