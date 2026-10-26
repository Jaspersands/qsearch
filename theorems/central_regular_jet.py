"""Public central-only regular-source algebra, not an executed HSP receiver.

For a class-two normal group, negative Fourier on the center followed by
negation of the remaining coordinates gives a fixed-width monomial gauge.
Its Weyl map is (I, -B_lambda/2). Zero labels and singular forms are legal;
no irreducible-representation dimension or Plancherel-sector rule is used.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import prod

from theorems.affine_phase_erasure import monomials
from theorems.nonlinear_jet_erasure import TaylorJetChart, _compile_scalar_displacement
from theorems.prime_character_opi import ring
from theorems.ut5_matrix_phase_alignment import _canonical, _rank, verify_alignment
from theorems.ut5_scalar_phase_compiler import _add, _shifted_component


def regular_weyl_map(p, forms, label):
    """Return D_lambda=(I,-B_lambda/2); D^T Omega D=B_lambda."""
    ring(p)
    if p == 2 or not forms or not forms[0]:
        raise ValueError("odd prime and nonempty alternating-form family required")
    w = len(forms[0])
    _canonical(label, len(forms), p)
    for form in forms:
        if len(form) != w:
            raise ValueError("matching square alternating forms required")
        for row in form:
            _canonical(row, w, p)
        if any(form[i][i] or any((form[i][j]+form[j][i]) % p for j in range(w))
               for i in range(w)):
            raise ValueError("alternating forms required")
    half = pow(2, -1, p)
    top = [tuple(int(i == j) for j in range(w)) for i in range(w)]
    bottom = [tuple(-half*sum(a*form[i][j] for a, form in zip(label, forms)) % p
                    for j in range(w)) for i in range(w)]
    return tuple(top+bottom)


def scalar_features(chart, scale, outcome):
    """A nonzero scale times all degree <=D-1 monomials in (scale,Y)."""
    _canonical([scale], 1, chart.p)
    _canonical(outcome, chart.quotient_width, chart.p)
    if not scale:
        raise ValueError("nonzero active scale required")
    return (pow(scale, chart.degree, chart.p),)+tuple(
        pow(scale, k, chart.p)*prod(pow(y, e, chart.p) for y, e in zip(outcome, alpha)) % chart.p
        for alpha, k, a in chart.indices if a == 0)


@dataclass(frozen=True)
class CentralRegularMaps:
    chart: TaylorJetChart
    active_indices: tuple
    weyl_maps: tuple
    feature_matrix: tuple
    quadratic: tuple  # Shared geometry protocol: degree-D K, not quadratic in general.
    linear: tuple  # Shared geometry protocol: retained J, not a linear hidden curve.

    @property
    def p(self):
        return self.chart.p

    @property
    def jet_width(self):
        return self.chart.jet_width

    @property
    def carrier_width(self):
        return len(self.active_indices)*self.chart.noncentral_width


def regular_jet_maps(chart, forms, labels, scales, outcomes):
    """Check public relation and scalar feature rank, then form unpadded K/J.

No hidden potential, radical characters, sector choice, source generation
or SDE solver is supplied. Features must have full rank even if extra Z
rows could rescue a deficient design: this is the proved sufficient route.
"""
    p, w, D = chart.p, chart.noncentral_width, chart.degree
    if not labels or len(labels) != len(scales) or len(labels) != len(outcomes):
        raise ValueError("matching nonempty public source records required")
    _canonical(scales, len(labels), p)
    all_maps = tuple(regular_weyl_map(p, forms, label) for label in labels)
    if len(all_maps[0]) != 2*w:
        raise ValueError("forms must match the chart noncentral width")
    for y in outcomes:
        _canonical(y, chart.quotient_width, p)
    active = tuple(i for i, s in enumerate(scales) if s)
    # Isotropy needs cancellation on [N,N], not on every central coordinate.
    if not active or any(sum(pow(s, 2*D, p)*matrix[w+a][b]
                             for s, matrix in zip(scales, all_maps)) % p
                         for a in range(w) for b in range(w)):
        raise ValueError("nonzero verified degree-2D commutator relation required")
    features = tuple(scalar_features(chart, scales[i], outcomes[i]) for i in active)
    ell = 1+chart.jet_width//w
    if _rank(features, p) != ell:
        raise ValueError("scalar feature design is rank deficient")
    R = len(active)*w
    K, J = [[0]*w for _ in range(2*R)], [[0]*chart.jet_width for _ in range(2*R)]
    for block, i in enumerate(active):
        s, y = scales[i], outcomes[i]
        for j, row in enumerate(all_maps[i]):
            output = block*w+j if j < w else R+block*w+j-w
            K[output] = [pow(s, D, p)*value % p for value in row]
            J[output] = [pow(s, k, p)*prod(pow(x, e, p) for x, e in zip(y, alpha))*row[a] % p
                         for alpha, k, a in chart.indices]
    if R < w+chart.jet_width or _rank([a+b for a, b in zip(K[:R], J[:R])], p) != w+chart.jet_width:
        raise ArithmeticError("scalar rank did not lift to the claimed X rank")
    return CentralRegularMaps(chart, active, tuple(all_maps[i] for i in active), features,
                              tuple(map(tuple, K)), tuple(map(tuple, J)))


def regular_rank_schedule(chart):
    """Conditional rank bound given arbitrary prior labels and valid witnesses.

Requires independent fresh block rescalings and uniform shear outcomes,
with selection before those draws. It does not certify their provenance.
"""
    p, D = chart.p, chart.degree
    if p <= 2*D:
        raise ValueError("this conservative schedule requires p > 2D")
    ell = 1+chart.jet_width//chart.noncentral_width
    blocks = (ell+1)*p.bit_length()+2
    return blocks, min(Fraction(1), (p**ell-1)*Fraction(D-1, p-1)**blocks)


def compile_regular_scalar_packet(alignment, forms, labels, scales, outcomes,
                                  spectator_outcome, central_degree):
    """Public phase table from the central-only gauge, not irrep scalarization."""
    maps = alignment.maps
    if not isinstance(maps, CentralRegularMaps):
        raise ValueError("central-only regular maps required")
    chart = maps.chart
    p, m, w, J, R = chart.p, chart.quotient_width, chart.noncentral_width, chart.jet_width, maps.carrier_width
    if type(central_degree) is not int or not chart.degree <= central_degree < p:
        raise ValueError("central degree must satisfy D <= c < p")
    if regular_jet_maps(chart, forms, labels, scales, outcomes) != maps or not verify_alignment(alignment):
        raise ValueError("verified regular alignment for this transcript required")
    _canonical(spectator_outcome, R-J, p)
    basis = tuple((a, nu) for a in range(w+len(forms))
                  for nu in monomials(m, chart.degree if a < w else central_degree))
    displacement, psi = [{} for _ in range(2*R)], {}
    for block, (i, weyl) in enumerate(zip(maps.active_indices, maps.weyl_maps)):
        s, y = scales[i], outcomes[i]
        components = [_shifted_component(p, chart.width, basis, a, s, y) for a in range(w)]
        for j, row in enumerate(weyl):
            target = block*w+j if j < w else R+block*w+j-w
            for coefficient, component in zip(row, components):
                _add(displacement[target], component, coefficient, p)
        for j, coefficient in enumerate(labels[i]):
            _add(psi, _shifted_component(p, chart.width, basis, w+j, s, y), coefficient, p)
    return _compile_scalar_displacement(alignment, basis, displacement, psi,
                                        spectator_outcome, central_degree)
