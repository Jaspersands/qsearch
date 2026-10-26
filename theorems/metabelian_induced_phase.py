"""Public higher-parameter-degree compiler for right-fiber induced phases.

This is exact coefficient algebra, not a quantum receiver or an SDE solver.
Hidden potential coefficients are formal indeterminates. Only methods named
fixture accept their values. The old quadratic packet contract is unchanged.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from functools import cached_property, lru_cache
from itertools import combinations
from math import comb, prod

from theorems.affine_phase_erasure import monomials
from theorems.ambient_section_potential import section_word_certificate
from theorems.class_three_monomial_jet import FullTaylorJetChart
from theorems.induced_cocycle_formula import operator_coefficients
from theorems.nonlinear_jet_erasure import _jet_terms
from theorems.prime_character_opi import ring
from theorems.symbolic_scalar_phase_erasure import PublicLieAlgebra
from theorems.ut5_matrix_phase_alignment import (
    _canonical, _identity, _lists, _matrix, _product, _transpose,
)
from theorems.ut5_scalar_phase_compiler import _add, _shifted_component


@dataclass(frozen=True)
class MetabelianLieChart:
    """Ordered N=A+I with [N,N]<=I, [I,I]=0; A need not be a subalgebra.

    Public structure constants are checked for alternation, Jacobi and
    nilpotency. This does NOT certify that N is an ambient derived algebra.
    """
    p: int
    a_width: int
    brackets: tuple

    def __post_init__(self):
        ring(self.p)
        n, r = self.width, self.a_width
        if type(r) is not int or not 0 < r < n or self.p <= 2:
            raise ValueError("odd prime and positive A,I dimensions required")
        if not isinstance(self.brackets, tuple) or any(
                not isinstance(rows, tuple) or len(rows) != n for rows in self.brackets):
            raise ValueError("immutable square structure tensor required")
        for rows in self.brackets:
            for row in rows:
                if not isinstance(row, tuple):
                    raise ValueError("immutable structure coordinates required")
                _canonical(row, n, self.p)
                if any(row[:r]):
                    raise ValueError("derived algebra must lie in I")
        for i in range(n):
            for j in range(n):
                if (i == j and any(self.brackets[i][j])) or any(
                        (a+b) % self.p for a, b in zip(self.brackets[i][j], self.brackets[j][i])):
                    raise ValueError("alternating bracket required")
                if i >= r and j >= r and any(self.brackets[i][j]):
                    raise ValueError("I must be abelian")
        for i, j, k in combinations(range(n), 3):
            jacobi = [0]*n
            for a, b, c in ((i, j, k), (j, k, i), (k, i, j)):
                for l, value in self.sparse[b][c]:
                    for t, coefficient in self.sparse[a][l]:
                        jacobi[t] += value*coefficient
            if any(v % self.p for v in jacobi):
                raise ValueError("Jacobi identity failed")
        if self.nilpotency_class >= self.p:
            raise ValueError("Lazard range p>class(N) required")

    @property
    def width(self):
        return len(self.brackets)

    @property
    def ideal_width(self):
        return self.width-self.a_width

    @cached_property
    def sparse(self):
        return tuple(tuple(tuple((k, c) for k, c in enumerate(row) if c)
                           for row in rows) for rows in self.brackets)

    def bracket(self, left, right):
        for value in (left, right):
            _canonical(value, self.width, self.p)
        result = [0]*self.width
        for i, a in enumerate(left):
            if a:
                for j, b in enumerate(right):
                    if b:
                        for t, c in self.sparse[i][j]:
                            result[t] += a*b*c
        return tuple(x % self.p for x in result)

    @cached_property
    def nilpotency_class(self):
        algebra = PublicLieAlgebra(self.p, self.width, self.bracket)
        return algebra.nilpotency_class(_identity(self.width))


def _multiply(left, right, p, parameter_cap):
    result = {}
    for (alpha, parameters), a in left.items():
        for (beta, others), b in right.items():
            if len(alpha) != len(beta):
                raise ValueError("matching polynomial coordinate widths required")
            lifted = tuple(sorted(parameters+others))
            if len(lifted) > parameter_cap:
                raise ArithmeticError("phase exceeded the declared parameter lift")
            key = (tuple(x+y for x, y in zip(alpha, beta)), lifted)
            _add(result, {key: a*b % p}, 1, p)
    return result


def _substitute(terms, coordinates, parameters, p, cap, width):
    """Exact substitution, never degree truncation; None preserves parameters."""
    zero = (0,)*width
    @lru_cache(maxsize=None)
    def power(j, exponent):
        if not exponent:
            return {(zero, ()): 1}
        return _multiply(power(j, exponent-1), coordinates[j], p, cap)
    result = {}
    for (alpha, indices), coefficient in terms.items():
        value = {(zero, indices if parameters is None else ()): coefficient}
        if parameters is not None:
            for index in indices:
                value = _multiply(value, parameters[index], p, cap)
        for j, exponent in enumerate(alpha):
            if exponent:
                value = _multiply(value, power(j, exponent), p, cap)
        _add(result, value, 1, p)
    return result


@lru_cache(maxsize=None)
def lie_word_cocycle_template(structure):
    """All coefficients of kappa(exp(Q),x), formal Q and public carrier x.

    A template key is (carrier exponent, sorted log-coordinate indices).
    The universal free-associative certificate verifies the entire Lie word.
    No polynomial fitting or actual potential coefficients enter this API.
    """
    st = structure
    p, n, r, k = st.p, st.width, st.a_width, st.nilpotency_class
    zero = (0,)*r
    letters = [[{} for _ in range(n)] for _ in range(3)]
    for j in range(r):
        x = (tuple(int(i == j) for i in range(r)), ())
        letters[0][j] = {(zero, (j,)): p-1, x: p-1}
        letters[1][j] = {(zero, (j,)): 1}
    for j in range(r, n):
        letters[2][j] = {(zero, (j,)): 1}
    def bracket(left, right):
        result = [{} for _ in range(n)]
        for i, a in enumerate(left):
            if a:
                for j, b in enumerate(right):
                    if b and st.sparse[i][j]:
                        value = _multiply(a, b, p, k)
                        for t, coefficient in st.sparse[i][j]:
                            _add(result[t], value, coefficient, p)
        return result
    @lru_cache(maxsize=None)
    def nested(word):
        return letters[word[0]] if len(word) == 1 else bracket(letters[word[0]], nested(word[1:]))
    result = [{} for _ in range(n)]
    for word, coefficient in section_word_certificate(k).field_terms(p):
        for target, value in zip(result, nested(word)):
            _add(target, value, coefficient, p)
    return _checked_template(result, st)


def _checked_template(result, st):
    r, k = st.a_width, st.nilpotency_class
    if any(result[:r]):
        raise ArithmeticError("universal cocycle left the abelian ideal")
    if any(sum(alpha)+len(parameters) > k for component in result
           for alpha, parameters in component):
        raise ArithmeticError("cocycle exceeded normal nilpotency class")
    if any(sum(j >= r for j in parameters) > 1 or
           (not any(j >= r for j in parameters) and not any(alpha))
           for component in result for alpha, parameters in component):
        raise ArithmeticError("cocycle violated abelian-fiber support")
    return tuple(tuple(sorted(component.items())) for component in result[r:])


@lru_cache(maxsize=None)
def cocycle_template(structure):
    """Public closed-form compiler; no exp/log expansion or hidden values.

    On I, R=ad(A), S=ad(X) commute. Compile R^i S^j B and
    R^i S^j[A,X] with the universal right-fiber coefficients.
    lie_word_cocycle_template is the independent exponential-word reference.
    """
    st = structure
    p, n, r, k = st.p, st.width, st.a_width, st.nilpotency_class
    zero = (0,)*r
    a, x, b = ([{} for _ in range(n)] for _ in range(3))
    for j in range(r):
        a[j] = {(zero, (j,)): 1}
        x[j] = {(tuple(int(i == j) for i in range(r)), ()): 1}
    for j in range(r, n):
        b[j] = {(zero, (j,)): 1}

    def bracket(left, right):
        result = [{} for _ in range(n)]
        for i, first in enumerate(left):
            if first:
                for j, second in enumerate(right):
                    if second and st.sparse[i][j]:
                        value = _multiply(first, second, p, k)
                        for t, coefficient in st.sparse[i][j]:
                            _add(result[t], value, coefficient, p)
        return result

    curvature = bracket(a, x)
    @lru_cache(maxsize=None)
    def acted(seed, i, j):
        if i:
            return bracket(a, acted(seed, i-1, j))
        if j:
            return bracket(x, acted(seed, 0, j-1))
        return b if seed == "B" else curvature

    result = [{} for _ in range(n)]
    for (seed, i, j), rational in operator_coefficients(k):
        coefficient = rational.numerator*pow(rational.denominator, -1, p) % p
        for target, value in zip(result, acted(seed, i, j)):
            _add(target, value, coefficient, p)
    return _checked_template(result, st)


@dataclass(frozen=True)
class InducedAlignment:
    chart: FullTaylorJetChart
    structure: MetabelianLieChart
    labels: tuple
    scales: tuple
    outcomes: tuple
    displacement_map: tuple
    forward: tuple
    inverse: tuple

    @property
    def carrier_width(self):
        return len(self.labels)*self.structure.a_width


def align_induced_jet(chart, structure, labels, scales, outcomes):
    """Label-independent GL alignment. Zero labels are ordinary outcomes."""
    p, r = structure.p, structure.a_width
    if not isinstance(chart, FullTaylorJetChart) or (chart.p, chart.noncentral_width) != (p, r):
        raise ValueError("compatible full jet chart required")
    if not labels or len(labels) != len(scales) or len(labels) != len(outcomes):
        raise ValueError("matching nonempty transcript required")
    _canonical(scales, len(labels), p)
    if not all(scales):
        raise ValueError("nonzero source scales required")
    rows = []
    for label, s, y in zip(labels, scales, outcomes):
        _canonical(label, structure.ideal_width, p)
        _canonical(y, chart.quotient_width, p)
        features = [pow(s, k, p)*prod(pow(v, e, p) for v, e in zip(y, alpha)) % p
                    for alpha, k, _ in chart.indices]
        rows.extend([value*int(a == b) for value, (_, _, a) in zip(features, chart.indices)]
                    for b in range(r))
    J, R = chart.jet_width, len(rows)
    reduced, rank = _matrix(_transpose(rows), p).rref()
    if rank != J:
        raise ValueError("full feature design is rank deficient")
    pivots = {next(i for i, x in enumerate(row) if x) for row in _lists(reduced)[:rank]}
    inverse = _transpose(_transpose(rows)+[row for i, row in enumerate(_identity(R)) if i not in pivots])
    forward = _lists(_matrix(inverse, p).inv())
    if _product(forward, rows, p) != [row[:J] for row in _identity(R)]:
        raise ArithmeticError("GL alignment certificate failed")
    return InducedAlignment(chart, structure, tuple(map(tuple, labels)), tuple(scales),
                            tuple(map(tuple, outcomes)), tuple(map(tuple, rows)),
                            tuple(map(tuple, forward)), tuple(map(tuple, inverse)))


@dataclass
class InducedPhasePacket:
    """Fixed formal coefficients of every log-Q component through degree D.

    Matching schemas do not certify common hidden-instance provenance,
    physical freshness, or source consumption. This is only public algebra.
    """
    chart: FullTaylorJetChart
    normal_width: int
    parameter_cap: int
    terms: dict

    def __post_init__(self):
        self.validate()

    @property
    def parameter_basis(self):
        return tuple((a, alpha) for a in range(self.normal_width)
                     for alpha in monomials(self.chart.quotient_width, self.chart.degree))

    @property
    def lifted_parameter_count(self):
        return comb(len(self.parameter_basis)+self.parameter_cap, self.parameter_cap)

    @property
    def supported_parameter_count(self):
        """At most one I coefficient; a pure-A term needs a carrier factor."""
        h = comb(self.chart.quotient_width+self.chart.degree, self.chart.quotient_width)
        h_a = h*self.chart.noncentral_width
        h_i = h*(self.normal_width-self.chart.noncentral_width)
        return (1+h_i)*comb(h_a+self.parameter_cap-1, self.parameter_cap-1)

    @property
    def weighted_degree(self):
        return max((self.chart.weighted_degree(alpha) for alpha, _ in self.terms), default=0)

    @property
    def schema(self):
        return type(self), self.chart, self.normal_width, self.parameter_cap, self.parameter_basis

    def validate(self):
        if not isinstance(self.chart, FullTaylorJetChart):
            raise ValueError("full jet chart required")
        if type(self.normal_width) is not int or self.normal_width <= self.chart.noncentral_width:
            raise ValueError("positive normal ideal dimension required")
        if type(self.parameter_cap) is not int or self.parameter_cap < 1:
            raise ValueError("positive parameter cap required")
        if self.chart.p <= self.parameter_cap*self.chart.degree:
            raise ValueError("conservative erasure scope requires p>kD")
        basis = self.parameter_basis
        h = len(basis)
        for (alpha, parameters), c in self.terms.items():
            if self.chart.weighted_degree(alpha) > self.parameter_cap*self.chart.degree:
                raise ValueError("phase exceeded the weighted envelope")
            if len(parameters) > self.parameter_cap or tuple(sorted(parameters)) != parameters or any(
                    type(i) is not int or not 0 <= i < h for i in parameters):
                raise ValueError("canonical bounded parameter monomial required")
            ideal_count = sum(basis[i][0] >= self.chart.noncentral_width for i in parameters)
            if ideal_count > 1 or (not ideal_count and len(parameters) >= self.parameter_cap):
                raise ValueError("phase violated abelian-fiber parameter support")
            parameter_degree = len(parameters)
            if not parameter_degree or sum(alpha[:self.chart.quotient_width]) > parameter_degree*self.chart.degree or sum(
                    alpha[self.chart.quotient_width:]) > self.parameter_cap-parameter_degree:
                raise ValueError("phase violated separated q/jet source support")
            if type(c) is not int or not 0 < c < self.chart.p:
                raise ValueError("nonzero canonical field coefficient required")

    def evaluate_fixture(self, point, parameters):
        """Known-value reference check ONLY, never used by the compiler."""
        self.validate()
        p = self.chart.p
        _canonical(point, self.chart.width, p)
        _canonical(parameters, len(self.parameter_basis), p)
        return sum(c*prod(pow(x, e, p) for x, e in zip(point, alpha))*prod(parameters[j] for j in inds)
                   for (alpha, inds), c in self.terms.items()) % p


def _affine_polynomials(offset, matrix, p, width):
    zero = (0,)*width
    result = []
    for constant, row in zip(offset, matrix):
        value = {(zero, ()): constant} if constant else {}
        for j, c in enumerate(row):
            if c:
                value[(tuple(int(i == j) for i in range(width)), ())] = c % p
        result.append(value)
    return result


def compile_induced_phase(alignment, spectator):
    """Compile -sum lambda*kappa(exp(Q(Y+s*q)), L^-1(t,spectator))."""
    ch, st = alignment.chart, alignment.structure
    return _compile_induced_phase(alignment, spectator,
                                  InducedPhasePacket(ch, st.width, st.nilpotency_class, {}))


def _compile_induced_phase(alignment, spectator, packet):
    """Shared exact substitution for uniform and certified filtered schemas."""
    ch, st = alignment.chart, alignment.structure
    p, r, k, J, R, m = ch.p, st.a_width, st.nilpotency_class, ch.jet_width, alignment.carrier_width, ch.quotient_width
    if align_induced_jet(ch, st, alignment.labels, alignment.scales, alignment.outcomes) != alignment:
        raise ValueError("verified induced alignment required")
    _canonical(spectator, R-J, p)
    offsets = [sum(a*b for a, b in zip(row[J:], spectator)) % p for row in alignment.inverse]
    matrix = [(0,)*m+row[:J] for row in alignment.inverse]
    carriers = _affine_polynomials(offsets, matrix, p, ch.width)
    template, displacement = cocycle_template(st), []
    for i, (label, s, y) in enumerate(zip(alignment.labels, alignment.scales, alignment.outcomes)):
        components = [_shifted_component(p, ch.width, packet.parameter_basis, a, s, y)
                      for a in range(st.width)]
        displacement.extend(components[:r])
        for coefficient, component in zip(label, template):
            if coefficient:
                value = _substitute(dict(component), carriers[i*r:(i+1)*r], components, p, k, ch.width)
                _add(packet.terms, value, -coefficient, p)
    for j, row in enumerate(alignment.forward):
        translated = {}
        for c, component in zip(row, displacement):
            _add(translated, component, c, p)
        nonconstant = {key: c for key, c in translated.items() if any(key[0])}
        expected = _jet_terms(ch, packet.parameter_basis, j, ch.width) if j < J else {}
        if nonconstant != expected:
            raise ArithmeticError("aligned displacement is not the common full jet")
    packet.validate()
    return packet


def pullback_induced_phase(packet, y, z, scale):
    packet.validate()
    ch = packet.chart
    offset, matrix = ch.affine_map(y, z, scale)
    coordinates = _affine_polynomials(offset, matrix, ch.p, ch.width)
    terms = _substitute(packet.terms, coordinates, None, ch.p, packet.parameter_cap, ch.width)
    return replace(packet, terms=terms)


def induced_leading_columns(packets, degree):
    if type(degree) is not int or degree < 1 or not packets:
        raise ValueError("positive degree and nonempty packet batch required")
    first = packets[0]
    for packet in packets:
        packet.validate()
        if packet.schema != first.schema:
            raise ValueError("identical formal coefficient schemas required")
        if packet.weighted_degree > degree:
            raise ValueError("packet exceeds stage degree")
    keys = tuple(sorted({key for packet in packets for key in packet.terms
                         if first.chart.weighted_degree(key[0]) == degree}))
    return [tuple(packet.terms.get(key, 0) for key in keys) or (0,) for packet in packets], keys


def merge_induced_phases(packets, scales, outcomes, degree):
    """Verify a supplied public SDE witness and lower weighted phase degree.

    Not a witness search or instrument execution. Scales precede outcomes;
    all sources, including zero-scale discards, must be fresh and consumed
    by a future physical controller. This algebra does not enforce that.
    """
    columns, _ = induced_leading_columns(packets, degree)
    first, terms = packets[0], {}
    ch, p = first.chart, first.chart.p
    _canonical(scales, len(packets), p)
    if not any(scales) or any(sum(col[j]*pow(s, degree, p) for col, s in zip(columns, scales)) % p
                              for j in range(len(columns[0]))):
        raise ArithmeticError("coefficientwise weighted cancellation failed")
    if len(outcomes) != len(packets):
        raise ValueError("matching outcome count required")
    for packet, scale, (y, z) in zip(packets, scales, outcomes):
        _canonical(y, ch.quotient_width, p)
        _canonical(z, ch.jet_width, p)
        if scale:
            _add(terms, pullback_induced_phase(packet, y, z, scale).terms, 1, p)
    result = replace(first, terms=terms)
    if result.weighted_degree >= degree:
        raise ArithmeticError("weighted degree did not decrease")
    return result


def diagnostic_report():
    """Finite coefficient audit, not an ambient HSP or timing benchmark."""
    import sympy as sp
    from theorems.right_abelian_induced_source import symbolic_filiform_cocycle

    rows = []
    for p in (17, 2**127-1):
        brackets = [[[0]*5 for _ in range(5)] for _ in range(5)]
        for j in range(1, 4):
            brackets[0][j][j+1], brackets[j][0][j+1] = 1, p-1
        for r in (1, 2):
            st = MetabelianLieChart(p, r, tuple(tuple(map(tuple, row)) for row in brackets))
            if r == 2:
                g, x, independent = symbolic_filiform_cocycle(4)
            else:
                a, xx = sp.symbols("a x")
                b = sp.symbols("b0:4")
                g, x = (a,)+b, (xx,)
                independent = [sum((-(a+xx))**u/sp.factorial(u)*a**v/sp.factorial(v+1)*b[j-u-v]
                                   for u in range(j+1) for v in range(j-u+1)) for j in range(4)]
            template = cocycle_template(st)
            for component, expression in zip(template, independent):
                expected = {}
                for powers, c in sp.Poly(sp.expand(expression), *x, *g).terms():
                    numerator, denominator = sp.fraction(c)
                    coefficient = int(numerator)*pow(int(denominator), -1, p) % p
                    indices = tuple(j for j, exponent in enumerate(powers[r:]) for _ in range(exponent))
                    if coefficient:
                        expected[(powers[:r], indices)] = coefficient
                if dict(component) != expected:
                    raise ArithmeticError("independent semidirect coefficient comparison failed")
            ch = FullTaylorJetChart(p, 1, r, 2)
            labels = [(0,)*st.ideal_width]+[tuple(i+j+1 for j in range(st.ideal_width)) for i in range(3)]
            a = align_induced_jet(ch, st, labels, (1, 1, 2, 1), ((0,), (1,), (0,), (1,)))
            packet = compile_induced_phase(a, tuple(range(1, r+1)))
            negative = compile_induced_phase(align_induced_jet(ch, st,
                [tuple(-v % p for v in label) for label in labels], a.scales, a.outcomes), tuple(range(1, r+1)))
            merged = merge_induced_phases([packet, negative], (1, 1),
                [((0,), (0,)*ch.jet_width), ((1,), (1,)*ch.jet_width)], packet.weighted_degree)
            rows.append({
                "p": p, "normal_class": st.nilpotency_class, "quotient_width": r,
                "ideal_width": st.ideal_width, "potential_degree_fixture": 2,
                "independent_cocycle_coefficients_match": True,
                "source_labels_include_zero": True, "spectators_retained": r,
                "template_terms": sum(len(v) for v in template),
                "aligned_phase_terms": len(packet.terms),
                "max_parameter_degree": max(len(params) for _, params in packet.terms),
                "weighted_degree_before_merge": packet.weighted_degree,
                "weighted_degree_after_merge": merged.weighted_degree,
                "generic_parameter_columns": packet.lifted_parameter_count,
                "fiber_supported_parameter_columns": packet.supported_parameter_count,
            })
    return {
        "schema": "metabelian_induced_phase_v1", "diagnostics": rows,
        "status": "public coefficient compiler verified by exact finite falsifiers",
        "cocycle_backend": "commuting_adjoint_closed_form",
        "universal_identity_artifact": "research/reductions/induced_cocycle_formula.json",
        "unknown_coefficients_are_formal": True,
        "legacy_quadratic_guard_preserved": True,
        "speedup_claim_allowed": False, "receiver_executed": False,
        "limitations": [
            "degree-two diagnostic potentials are not the full c9 ambient source",
            "large ambient witness checked separately in tests; full D9 aligned packet not expanded",
            "no general SDE search, physical freshness controller, or synthesis backend",
            "local Lean operator/source theorems do not certify the whole algorithm or novelty",
            "no useful hard application or classical lower bound established",
        ],
    }


if __name__ == "__main__":
    import argparse
    import json
    from pathlib import Path
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = diagnostic_report()
    if args.write:
        path = Path(__file__).resolve().parents[1]/"research/reductions/metabelian_induced_phase.json"
        path.write_text(json.dumps(report, indent=2)+"\n")
        print(path)
    print(json.dumps(report, indent=2))
