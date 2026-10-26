"""Class-three regular gauges and FULL Taylor-jet control algebra.

No hidden polynomial is an input to the compiler. The functions explicitly
named fixture evaluate known group elements for falsification only. This
module does not prepare quantum states, solve SDEs, or execute an HSP solver.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import cached_property
from itertools import product
from math import prod

from theorems.affine_phase_erasure import monomials
from theorems.nonlinear_jet_erasure import TaylorJetChart, _jet_terms, weighted_degree
from theorems.prime_character_opi import ring
from theorems.ut5_matrix_phase_alignment import (
    _canonical, _identity, _lists, _matrix, _product, _rank, _transpose,
)
from theorems.ut5_scalar_phase_compiler import (
    SymbolicScalarPacket, _add, _multiply, _shifted_component,
)


def _bilinear(forms, x, y, p):
    return tuple(sum(c*a*b for row, a in zip(form, x) for c, b in zip(row, y)) % p
                 for form in forms)


@dataclass(frozen=True)
class ClassThreeStructure:
    """[A,A]=(beta,gamma), [A,B]=delta in central C; all other brackets zero.

    beta has shape (s,r,r), gamma (z,r,r), delta (z,r,s). The class-two
    normal case is s=0, beta=(), and delta has empty rows; no B-Fourier
    registers or source-level cancellation witness are then required.
    Jacobi is checked. This schema alone does NOT certify C=Z(N), that
    B=(N'+C)/C, or embedding into an ambient lower-central filtration.
    """
    p: int
    beta: tuple
    gamma: tuple
    delta: tuple

    def __post_init__(self):
        ring(self.p)
        if self.p <= 3 or not self.gamma or not self.gamma[0]:
            raise ValueError("p>3 and positive A,C dimensions required")
        r, s, z = self.a_width, self.b_width, self.c_width
        for forms, count, rows, cols in ((self.beta,s,r,r), (self.gamma,z,r,r),
                                         (self.delta,z,r,s)):
            if len(forms) != count:
                raise ValueError("inconsistent structure tensor dimensions")
            for form in forms:
                if len(form) != rows:
                    raise ValueError("inconsistent structure tensor dimensions")
                for row in form:
                    _canonical(row, cols, self.p)
        for form in self.beta+self.gamma:
            if any(form[i][i] or (form[i][j]+form[j][i]) % self.p
                   for i,j in product(range(r),repeat=2)):
                raise ValueError("alternating A brackets required")
        for h,i,j,k in product(range(z),range(r),range(r),range(r)):
            if sum(self.delta[h][i][b]*self.beta[b][j][k]
                   +self.delta[h][j][b]*self.beta[b][k][i]
                   +self.delta[h][k][b]*self.beta[b][i][j] for b in range(s)) % self.p:
                raise ValueError("class-three Jacobi identity failed")

    @property
    def a_width(self):
        return len(self.gamma[0])

    @property
    def b_width(self):
        return len(self.beta)

    @property
    def c_width(self):
        return len(self.gamma)

    @property
    def carrier_width(self):
        return self.a_width+self.b_width

    def _element(self, element):
        if len(element) != 3:
            raise ValueError("three coordinate blocks required")
        for row, size in zip(element,(self.a_width,self.b_width,self.c_width)):
            _canonical(row,size,self.p)

    def multiply_fixture(self, left, right):
        """BCH in known log coordinates, not evaluation of a hidden potential."""
        self._element(left)
        self._element(right)
        p = self.p
        a,b,c = left
        x,y,z = right
        beta = _bilinear(self.beta,a,x,p)
        gamma = _bilinear(self.gamma,a,x,p)
        ay,xb = _bilinear(self.delta,a,y,p),_bilinear(self.delta,x,b,p)
        ab,xbeta = _bilinear(self.delta,a,beta,p),_bilinear(self.delta,x,beta,p)
        return (tuple((u+v) % p for u,v in zip(a,x)),
                tuple((u+v+pow(2,-1,p)*w) % p for u,v,w in zip(b,y,beta)),
                tuple((u+v+pow(2,-1,p)*(g+d-e)+pow(12,-1,p)*(f-h)) % p
                      for u,v,g,d,e,f,h in zip(c,z,gamma,ay,xb,ab,xbeta)))

    def translation_map(self, label):
        """D_lambda a=(a,lambda*delta(a,-)/2), including label zero."""
        _canonical(label,self.c_width,self.p)
        r,s,p = self.a_width,self.b_width,self.p
        return tuple(map(tuple,_identity(r)))+tuple(
            tuple(pow(2,-1,p)*sum(label[h]*self.delta[h][i][j]
                                 for h in range(self.c_width)) % p for i in range(r))
            for j in range(s))

    def fourier_action_fixture(self, label, element, carrier):
        """Known-element action after NEGATIVE B-Fourier; mu stays quantum."""
        self._element(element)
        _canonical(carrier,self.carrier_width,self.p)
        D = self.translation_map(label)
        p,r = self.p,self.a_width
        a,b,_ = element
        x,mu = carrier[:r],carrier[r:]
        shift = tuple(sum(u*v for u,v in zip(row,a)) % p for row in D)
        _,d,cocycle = self.multiply_fixture(element,(tuple(x),(0,)*self.b_width,(0,)*self.c_width))
        phase = (sum(u*v for u,v in zip(label,cocycle))
                 -sum((u+v)*w for u,v,w in zip(mu,shift[r:],d))) % p
        return tuple((u+v) % p for u,v in zip(carrier,shift)),phase


@dataclass(frozen=True)
class FullTaylorJetChart(TaylorJetChart):
    """Retain k=D too: no top-translation cancellation or isotropy premise."""
    @cached_property
    def indices(self):
        return tuple((alpha,k,a) for k in range(1,self.degree+1)
                     for alpha in monomials(self.quotient_width,self.degree-k)
                     for a in range(self.noncentral_width))

    @property
    def feature_count(self):
        return self.jet_width//self.noncentral_width


@dataclass(frozen=True)
class FullJetAlignment:
    chart: FullTaylorJetChart
    structure: ClassThreeStructure
    labels: tuple
    scales: tuple
    outcomes: tuple
    features: tuple
    displacement_map: tuple
    forward: tuple
    inverse: tuple

    @property
    def carrier_width(self):
        return len(self.labels)*self.structure.carrier_width


def align_full_jet(chart, structure, labels, scales, outcomes):
    """Public GL permutation L with L*J=(I,0); no SDE witness is needed.

    Rank acceptance is a physical postselection and consumes the batch.
    This function checks values, not the source/outcome sampling protocol.
    """
    p,r = chart.p,chart.noncentral_width
    if not isinstance(chart,FullTaylorJetChart) or (structure.p,structure.a_width) != (p,r):
        raise ValueError("compatible FULL jet chart and structure required")
    if not labels or len(labels) != len(scales) or len(labels) != len(outcomes):
        raise ValueError("matching nonempty transcript required")
    _canonical(scales,len(labels),p)
    if not all(scales):
        raise ValueError("all source scales must be nonzero")
    features,rows = [],[]
    for label,s,y in zip(labels,scales,outcomes):
        _canonical(y,chart.quotient_width,p)
        values = [pow(s,k,p)*prod(pow(v,e,p) for v,e in zip(y,alpha)) % p
                  for alpha,k,_ in chart.indices]
        features.append(tuple(values[j] for j,(_,_,a) in enumerate(chart.indices) if a == 0))
        for row in structure.translation_map(label):
            rows.append([v*row[a] % p for v,(_,_,a) in zip(values,chart.indices)])
    J,R = chart.jet_width,len(rows)
    if _rank(features,p) != J//r:
        raise ValueError("scalar feature design is rank deficient")
    reduced,rank = _matrix(_transpose(rows),p).rref()
    if rank != J:
        raise ArithmeticError("feature rank did not lift to translation rank")
    pivots = {next(i for i,x in enumerate(row) if x) for row in _lists(reduced)[:rank]}
    # These standard columns complete J because its pivot-row minor is invertible.
    columns = _transpose(rows)+[row for i,row in enumerate(_identity(R)) if i not in pivots]
    inverse = _transpose(columns)
    forward = _lists(_matrix(inverse,p).inv())
    expected = [row[:J] for row in _identity(R)]
    if _product(forward,rows,p) != expected:
        raise ArithmeticError("GL alignment certificate failed")
    return FullJetAlignment(chart,structure,tuple(map(tuple,labels)),tuple(scales),
                            tuple(map(tuple,outcomes)),tuple(features),tuple(map(tuple,rows)),
                            tuple(map(tuple,forward)),tuple(map(tuple,inverse)))


def full_jet_rank_schedule(chart):
    """Conditional bound for independent nonzero scales and uniform Y rows."""
    if not isinstance(chart,FullTaylorJetChart) or chart.p <= 2*chart.degree:
        raise ValueError("FULL chart with p>2D required")
    ell = chart.feature_count
    B = (ell+1)*chart.p.bit_length()+2
    return B,min(Fraction(1),(chart.p**ell-1)*Fraction(chart.degree-1,chart.p-1)**B)


def _poly_bilinear(forms, left, right, p):
    result = []
    for form in forms:
        value = {}
        for row,a in zip(form,left):
            for c,b in zip(row,right):
                if c:
                    _add(value,_multiply(a,b,p),c,p)
        result.append(value)
    return result


def compile_full_jet_phase(alignment, spectator, central_degree):
    """Compile -sum Phi(g(Y+s*q), L^-1(t,spectator)) symbolically.

    Phi=R0-(mu+l_lambda(a)).(b+beta(a,x)/2). The fixed parameter schema
    contains coefficients of Q_A,Q_B (degree D) and Q_C (degree c), with
    their quadratic lift. Hidden coefficients are NOT supplied/evaluated.
    """
    chart,st = alignment.chart,alignment.structure
    p,m,J,R,D = chart.p,chart.quotient_width,chart.jet_width,alignment.carrier_width,chart.degree
    r,s,z = st.a_width,st.b_width,st.c_width
    if type(central_degree) is not int or not D <= central_degree < p:
        raise ValueError("central degree must satisfy D<=c<p")
    if p <= 3*D:
        raise ValueError("conservative phase-erasure scope requires p>3D")
    if align_full_jet(chart,st,alignment.labels,alignment.scales,alignment.outcomes) != alignment:
        raise ValueError("verified full-jet alignment required")
    _canonical(spectator,R-J,p)
    basis = tuple((a,nu) for a in range(r+s+z)
                  for nu in monomials(m,D if a < r+s else central_degree))
    zero,width = (0,)*chart.width,chart.width
    carrier = []
    for row in alignment.inverse:
        value = {}
        constant = sum(u*v for u,v in zip(row[J:],spectator)) % p
        if constant:
            value[(zero,())] = constant
        for j,c in enumerate(row[:J]):
            if c:
                value[(tuple(int(i == m+j) for i in range(width)),())] = c
        carrier.append(value)
    displacement,phase = [],{}
    for block,(label,scale,y) in enumerate(zip(alignment.labels,alignment.scales,alignment.outcomes)):
        components = [_shifted_component(p,width,basis,j,scale,y) for j in range(r+s+z)]
        a,b,c = components[:r],components[r:r+s],components[r+s:]
        point = carrier[block*(r+s):(block+1)*(r+s)]
        x,mu = point[:r],point[r:]
        shift = []
        for row in st.translation_map(label):
            value = {}
            for coefficient,component in zip(row,a):
                _add(value,component,coefficient,p)
            shift.append(value)
        displacement.extend(shift)
        beta = _poly_bilinear(st.beta,a,x,p)
        gamma = _poly_bilinear(st.gamma,a,x,p)
        xb = _poly_bilinear(st.delta,x,b,p)
        abeta = _poly_bilinear(st.delta,a,beta,p)
        xbeta = _poly_bilinear(st.delta,x,beta,p)
        for lam,cc,gg,xx,aa,bb in zip(label,c,gamma,xb,abeta,xbeta):
            for value,factor in ((cc,1),(gg,pow(2,-1,p)),(xx,-pow(2,-1,p)),
                                 (aa,pow(12,-1,p)),(bb,-pow(12,-1,p))):
                _add(phase,value,-lam*factor,p)
        for frequency,l,b0,beta0 in zip(mu,shift[r:],b,beta):
            left,right = dict(frequency),dict(b0)
            _add(left,l,1,p)
            _add(right,beta0,pow(2,-1,p),p)
            _add(phase,_multiply(left,right,p),1,p)
    for j,row in enumerate(alignment.forward):
        actual = {}
        for coefficient,component in zip(row,displacement):
            _add(actual,component,coefficient,p)
        nonconstant = {key:value for key,value in actual.items() if any(key[0])}
        expected = _jet_terms(chart,basis,j,width) if j < J else {}
        if nonconstant != expected:
            raise ArithmeticError("FULL shared Taylor jet identity failed")
    packet = SymbolicScalarPacket(p,m,J,basis,phase)
    if weighted_degree(chart,packet) > max(central_degree,3*D):
        raise ArithmeticError("class-three weighted degree bound failed")
    verify_full_jet_phase_support(chart, packet, r, s, z, central_degree)
    return packet


def verify_full_jet_phase_support(chart, packet, a_width, b_width, c_width, central_degree):
    """Check invariant coefficient blocks used by the sharper SDE envelope.

    This validates a polynomial, not its source provenance. Only separate
    public affine maps on q and t preserve the degree bounds used here.
    """
    if (not isinstance(chart, FullTaylorJetChart)
            or any(type(x) is not int for x in (a_width, b_width, c_width, central_degree))
            or a_width != chart.noncentral_width or b_width < 0 or c_width < 1
            or not chart.degree <= central_degree < chart.p):
        raise ValueError("matching full chart, component dimensions and central degree required")
    weighted_degree(chart, packet)  # validate coefficient/parameter encoding
    m, d = chart.quotient_width, chart.degree
    for component, powers in packet.parameter_basis:
        if (type(component) is not int or not 0 <= component < a_width+b_width+c_width
                or len(powers) != m or any(type(x) is not int or x < 0 for x in powers)
                or sum(powers) > (d if component < a_width+b_width else central_degree)):
            raise ValueError("parameter basis exceeds the declared potential coefficient schema")
    for (alpha, params), coefficient in packet.terms.items():
        if not coefficient:
            continue
        q_degree, jet_degree = sum(alpha[:m]), sum(alpha[m:])
        components = [packet.parameter_basis[i][0] for i in params]
        if not components or (len(components) == 1 and components[0] >= a_width+b_width):
            valid = q_degree <= central_degree and jet_degree == 0
        elif len(components) == 1:
            valid = q_degree <= d and jet_degree <= 2
        else:
            valid = (max(components) < a_width+b_width and min(components) < a_width
                     and q_degree <= 2*d and jet_degree <= 1)
        if not valid:
            raise ArithmeticError("phase exceeds source-structured q/jet/parameter support")
