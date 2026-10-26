"""Public Taylor-jet algebra for a proposed nonlinear HSP receiver.

No hidden polynomial is evaluated, no diagonal witness is searched for, and
no quantum source is prepared here. The existing exactly phased symplectic
alignment is reused; its historical K/J attribute names do not assert that
the new top-degree map is quadratic or that its retained jet is linear.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import cached_property
from math import comb, prod

from theorems.affine_phase_erasure import monomials
from theorems.class_four_matrix_source import factor_alternating, label_coordinates
from theorems.prime_character_opi import ring
from theorems.ut5_matrix_phase_alignment import _canonical, _rank, verify_alignment
from theorems.ut5_scalar_phase_compiler import (
    SymbolicScalarPacket, _add, _multiply, _shifted_component,
)


@dataclass(frozen=True)
class TaylorJetChart:
    p: int
    quotient_width: int
    noncentral_width: int
    degree: int

    def __post_init__(self):
        ring(self.p)
        if any(type(x) is not int or x < 1 for x in
               (self.quotient_width, self.noncentral_width)):
            raise ValueError("positive integer dimensions required")
        if type(self.degree) is not int or not 2 <= self.degree < self.p:
            raise ValueError("jet degree must satisfy 2 <= D < p")

    @cached_property
    def indices(self):
        """Retained order (alpha,k,a): |alpha|+k<=D, 1<=k<D, a in W."""
        return tuple((alpha, k, a) for k in range(1, self.degree)
                     for alpha in monomials(self.quotient_width, self.degree-k)
                     for a in range(self.noncentral_width))

    @property
    def jet_width(self):
        return len(self.indices)

    @property
    def width(self):
        return self.quotient_width+self.jet_width

    @cached_property
    def weights(self):
        return (1,)*self.quotient_width+tuple(k for _, k, _ in self.indices)

    def weighted_degree(self, alpha):
        if len(alpha) != self.width or any(type(a) is not int or a < 0 for a in alpha):
            raise ValueError("canonical monomial of chart width required")
        return sum(a*b for a, b in zip(alpha, self.weights))

    def transport_matrix(self, y, scale):
        """A(y,s) with F(y+s*q)=F(y)+A(y,s)F(q), without coefficients of F."""
        _canonical(y, self.quotient_width, self.p)
        _canonical([scale], 1, self.p)
        if not scale:
            raise ValueError("nonzero scale required for invertible jet transport")
        lookup = {key: i for i, key in enumerate(self.indices)}
        rows = []
        for alpha, k, a in self.indices:
            row = [0]*self.jet_width
            for delta in monomials(self.quotient_width, k-1):
                shifted = tuple(x+d for x, d in zip(alpha, delta))
                value = pow(scale, k-sum(delta), self.p)
                for x, d, origin in zip(alpha, delta, y):
                    value = value*comb(x+d, d)*pow(origin, d, self.p) % self.p
                row[lookup[(shifted, k-sum(delta), a)]] = value
            rows.append(tuple(row))
        return tuple(rows)

    def affine_map(self, y, z, scale):
        """Return offset and matrix for (q,t)->(y+s*q,z+A(y,s)t)."""
        _canonical(z, self.jet_width, self.p)
        transport = self.transport_matrix(y, scale)
        m = self.quotient_width
        rows = [tuple(scale*int(i == j) for j in range(m))+(0,)*self.jet_width
                for i in range(m)]
        rows += [(0,)*m+row for row in transport]
        return tuple(y)+tuple(z), tuple(rows)


@dataclass(frozen=True)
class HigherJetMaps:
    chart: TaylorJetChart
    active_indices: tuple
    representations: tuple
    source_carrier_width: int
    carrier_width: int
    quadratic: tuple  # Protocol name for K, here the degree-D coefficient map.
    linear: tuple  # Protocol name for J, here the retained nonlinear-jet map.

    @property
    def p(self):
        return self.chart.p

    @property
    def jet_width(self):
        return self.chart.jet_width

    @property
    def mixed_padding_qudits(self):
        return self.carrier_width-self.source_carrier_width


def higher_jet_maps(chart, forms, labels, scales, outcomes):
    """Verify a supplied degree-2D label relation and build public K/J maps.

    Rank is checked, not assumed from this fixture's frequency. The separate
    probability theorem needs equivariant relation selection, fresh rescaling
    and independent blocks. Padding means physical maximally mixed qudits.
    """
    p, w, D = chart.p, chart.noncentral_width, chart.degree
    if not forms or not labels or len(labels) != len(scales) or len(labels) != len(outcomes):
        raise ValueError("nonempty forms and matching batch inputs required")
    for form in forms:
        if len(form) != w:
            raise ValueError("bracket form must match noncentral width")
        factor_alternating(p, form)
    if _rank([row for form in forms for row in form], p) != w:
        raise ValueError("common radical must be removed first")
    _canonical(scales, len(labels), p)
    for label, y in zip(labels, outcomes):
        _canonical(label, len(forms), p)
        _canonical(y, chart.quotient_width, p)
        if not any(label):
            raise ValueError("nonzero central labels required")
    active = tuple(i for i, s in enumerate(scales) if s)
    if not active or any(sum(pow(s, 2*D, p)*label[j] for s, label in zip(scales, labels)) % p
                         for j in range(len(forms))):
        raise ValueError("nonzero verified degree-2D label relation required")
    coordinates = tuple(label_coordinates(p, forms, labels[i]) for i in active)
    physical = sum(c.qudits for c in coordinates)
    R = max(physical, w+chart.jet_width)
    K = [[0]*w for _ in range(2*R)]
    J = [[0]*chart.jet_width for _ in range(2*R)]
    start = 0
    for i, rep in zip(active, coordinates):
        s, y, r = scales[i], outcomes[i], rep.qudits
        for j, row in enumerate(rep.weyl):
            output = start+j if j < r else R+start+j-r
            K[output] = [pow(s, D, p)*x % p for x in row]
            J[output] = [pow(s, k, p)*prod(pow(x, e, p) for x, e in zip(y, alpha))*row[a] % p
                         for alpha, k, a in chart.indices]
        start += r
    if _rank([a+b for a, b in zip(K, J)], p) != w+chart.jet_width:
        raise ValueError("higher-jet design is rank deficient")
    return HigherJetMaps(chart, active, coordinates, physical, R,
                         tuple(map(tuple, K)), tuple(map(tuple, J)))


def rank_schedule(chart):
    """Conservative independent-block count and conditional rank-failure bound."""
    p, D = chart.p, chart.degree
    if p <= 2*D:
        raise ValueError("rank schedule requires p > 2D")
    L = chart.noncentral_width+chart.jet_width
    blocks = (L+1)*p.bit_length()+2
    bound = min(Fraction(1), (p**L-1)*Fraction(D, p-1)**blocks)
    return blocks, bound


def _jet_terms(chart, basis, index, width):
    alpha, k, a = chart.indices[index]
    lookup = {key: i for i, key in enumerate(basis)}
    terms = {}
    for beta in monomials(chart.quotient_width, k):
        if sum(beta) != k:
            continue
        nu = tuple(x+y for x, y in zip(alpha, beta))
        parameter = lookup[(a, nu)]
        coefficient = prod(comb(n, b) for n, b in zip(nu, beta)) % chart.p
        terms[(beta+(0,)*(width-len(beta)), (parameter,))] = coefficient
    return terms


def compile_higher_scalar_packet(alignment, forms, labels, scales, outcomes,
                                radical_characters, spectator_outcome, central_degree):
    """Compile the aligned Weyl phase; check the FULL shared nonlinear jet.

    The fixed parameters are coefficients of Q_W (degree D), Q_Z (degree
    central_degree), and their quadratic lift. This is public algebra, not
    a source-access or provenance certificate for the supplied transcript.
    """
    maps = alignment.maps
    chart = maps.chart
    p, w, m, J, R = chart.p, chart.noncentral_width, chart.quotient_width, chart.jet_width, maps.carrier_width
    if type(central_degree) is not int or not chart.degree <= central_degree < p:
        raise ValueError("central degree must satisfy D <= c < p")
    if higher_jet_maps(chart, forms, labels, scales, outcomes) != maps or not verify_alignment(alignment):
        raise ValueError("verified alignment for this public transcript required")
    if len(radical_characters) != len(labels):
        raise ValueError("one radical character per input required")
    for label, character in zip(labels, radical_characters):
        _canonical(character, len(label_coordinates(p, forms, label).radical), p)
    _canonical(spectator_outcome, R-J, p)
    basis = tuple((a, nu) for a in range(w+len(forms))
                  for nu in monomials(m, chart.degree if a < w else central_degree))
    displacement, psi, start = [{} for _ in range(2*R)], {}, 0
    for i, rep in zip(maps.active_indices, maps.representations):
        s, y, r = scales[i], outcomes[i], rep.qudits
        components = [_shifted_component(p, chart.width, basis, j, s, y) for j in range(w)]
        for j, row in enumerate(rep.weyl):
            target = start+j if j < r else R+start+j-r
            for coefficient, component in zip(row, components):
                _add(displacement[target], component, coefficient, p)
        for j, coefficient in enumerate(labels[i]):
            _add(psi, _shifted_component(p, chart.width, basis, w+j, s, y), coefficient, p)
        for coefficient, row in zip(radical_characters[i], rep.radical):
            for a, component in zip(row, components):
                _add(psi, component, coefficient*a, p)
        start += r
    return _compile_scalar_displacement(alignment, basis, displacement, psi,
                                        spectator_outcome, central_degree)


def _compile_scalar_displacement(alignment, basis, displacement, psi,
                                 spectator_outcome, central_degree):
    """Shared monomial-gauge contraction after each source wrapper validates maps."""
    chart = alignment.maps.chart
    p, m, J, R = chart.p, chart.quotient_width, chart.jet_width, alignment.maps.carrier_width
    transformed = []
    for row in alignment.symplectic:
        value = {}
        for coefficient, component in zip(row, displacement):
            _add(value, component, coefficient, p)
        transformed.append(value)
    for j, component in enumerate(transformed[:R]):
        nonconstant = {key: value for key, value in component.items() if any(key[0])}
        expected = _jet_terms(chart, basis, j, chart.width) if j < J else {}
        if nonconstant != expected:
            raise ArithmeticError("aligned X displacement is not the common Taylor jet")
    phase = {}
    _add(phase, psi, -1, p)
    for j, (A, B) in enumerate(zip(transformed[:R], transformed[R:])):
        _add(phase, _multiply(A, B, p), -pow(2, -1, p), p)
        if j < J:
            exponent = tuple(int(i == m+j) for i in range(chart.width))
            _add(phase, _multiply(B, {(exponent, ()): 1}, p), -1, p)
        else:
            _add(phase, B, -spectator_outcome[j-J], p)
    result = SymbolicScalarPacket(p, m, J, basis, phase)
    if weighted_degree(chart, result) > max(central_degree, 2*chart.degree-1):
        raise ArithmeticError("scalar phase exceeds the weighted source bound")
    return result


def fourier_curve_packet(chart, parameter_basis, eta):
    """Public phase eta.F(q) AFTER weighted erasure and negative t-Fourier.

    Every eta is retained. Calling this before physical phase erasure does
    not make the formula correct; this helper cannot certify a source state.
    """
    _canonical(eta, chart.jet_width, chart.p)
    if len(set(parameter_basis)) != len(parameter_basis):
        raise ValueError("distinct ordered parameter basis required")
    terms = {}
    for j, coefficient in enumerate(eta):
        _add(terms, _jet_terms(chart, parameter_basis, j, chart.quotient_width), coefficient, chart.p)
    return SymbolicScalarPacket(chart.p, chart.quotient_width, 0, parameter_basis, terms)


def _validate_packet(chart, packet):
    if (packet.p, packet.quotient_width, packet.jet_width) != (
            chart.p, chart.quotient_width, chart.jet_width):
        raise ValueError("packet dimensions must match Taylor chart")
    h = len(packet.parameter_basis)
    if not h or len(set(packet.parameter_basis)) != h:
        raise ValueError("nonempty distinct ordered parameter basis required")
    for (alpha, parameters), coefficient in packet.terms.items():
        chart.weighted_degree(alpha)
        if len(parameters) > 2 or tuple(sorted(parameters)) != parameters or any(
                type(i) is not int or not 0 <= i < h for i in parameters):
            raise ValueError("canonical lifted parameter indices required")
        if type(coefficient) is not int or not 0 <= coefficient < chart.p:
            raise ValueError("canonical field coefficient required")


def weighted_degree(chart, packet):
    _validate_packet(chart, packet)
    return max((chart.weighted_degree(alpha) for (alpha, _), c in packet.terms.items() if c), default=0)


def weighted_leading_columns(chart, packets, degree):
    """Public coefficient identities, not cancellation at hidden truth values."""
    if type(degree) is not int or degree < 1 or not packets:
        raise ValueError("positive stage degree and nonempty batch required")
    for packet in packets:
        if packet.parameter_basis != packets[0].parameter_basis:
            raise ValueError("same ordered parameter basis required")
        if weighted_degree(chart, packet) > degree:
            raise ValueError("packet exceeds weighted stage degree")
    keys = tuple(sorted({key for packet in packets for key, c in packet.terms.items()
                         if c and chart.weighted_degree(key[0]) == degree}))
    return [tuple(packet.terms.get(key, 0) for key in keys) or (0,)
            for packet in packets], keys


def verify_weighted_witness(chart, packets, scales, degree):
    columns, _ = weighted_leading_columns(chart, packets, degree)
    _canonical(scales, len(packets), chart.p)
    if not any(scales) or any(sum(col[j]*pow(s, degree, chart.p)
                                 for col, s in zip(columns, scales)) % chart.p
                              for j in range(len(columns[0]))):
        raise ArithmeticError("public weighted cancellation failed")


def pullback_phase(chart, packet, y, z, scale):
    """Symbolic pullback through the PUBLIC triangular affine address map."""
    _validate_packet(chart, packet)
    offset, matrix = chart.affine_map(y, z, scale)
    p, width = chart.p, chart.width
    zero = (0,)*width
    substitutions = []
    for constant, row in zip(offset, matrix):
        terms = {(zero, ()): constant} if constant else {}
        for j, value in enumerate(row):
            if value:
                terms[(tuple(int(i == j) for i in range(width)), ())] = value
        substitutions.append(terms)
    result = {}
    for (alpha, params), coefficient in packet.terms.items():
        value = {(zero, params): coefficient}
        for exponent, substitution in zip(alpha, substitutions):
            for _ in range(exponent):
                value = _multiply(value, substitution, p)
        _add(result, value, 1, p)
    return SymbolicScalarPacket(p, chart.quotient_width, chart.jet_width,
                                packet.parameter_basis, result)


def weighted_merge(chart, packets, scales, outcomes, degree):
    """Verify scales and update maps; this does NOT consume physical sources.

    Caller must choose scales before measuring outcomes, use disjoint sources
    from one hidden instance/chart, and discard zero-scale inputs. Matching
    parameter schemas alone cannot certify these physical premises.
    """
    verify_weighted_witness(chart, packets, scales, degree)
    if len(outcomes) != len(packets):
        raise ValueError("matching outcome count required")
    terms = {}
    for packet, s, (y, z) in zip(packets, scales, outcomes):
        if not s:
            continue
        _add(terms, pullback_phase(chart, packet, y, z, s).terms, 1, chart.p)
    result = SymbolicScalarPacket(chart.p, chart.quotient_width, chart.jet_width,
                                  packets[0].parameter_basis, terms)
    if weighted_degree(chart, result) >= degree:
        raise ArithmeticError("weighted degree did not decrease")
    return result
