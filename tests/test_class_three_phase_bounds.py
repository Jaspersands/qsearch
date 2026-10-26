"""Independent symbolic controls for the universal source-phase bounds.

These are compiler/counterexample tests, not oracle problems or algorithms.
SymPy expands without the production compiler's quadratic-lift cutoff.
"""

import pytest
import sympy as sp

from theorems.class_three_monomial_jet import (
    ClassThreeStructure, FullTaylorJetChart, align_full_jet, compile_full_jet_phase,
    verify_full_jet_phase_support,
)
from theorems.nonlinear_jet_erasure import pullback_phase, weighted_degree, weighted_merge
from theorems.ut5_scalar_phase_compiler import SymbolicScalarPacket


def _phase(st, label, a, b, c, x, mu):
    # Rational form of the BCH phase, with no parameter-degree truncation.
    def bilinear(forms, left, right):
        return [sum(coef*u*v for row, u in zip(form, left)
                    for coef, v in zip(row, right)) for form in forms]
    beta = bilinear(st.beta, a, x)
    gamma = bilinear(st.gamma, a, x)
    xb = bilinear(st.delta, x, b)
    abeta = bilinear(st.delta, a, beta)
    xbeta = bilinear(st.delta, x, beta)
    raw = sum(lam*(cc+(gg-xx)/2+(aa-bb)/12)
              for lam, cc, gg, xx, aa, bb in zip(label, c, gamma, xb, abeta, xbeta))
    ell = [sum(lam*sum(coef*u for coef, u in zip((row[j] for row in form), a))
               for lam, form in zip(label, st.delta))/2 for j in range(st.b_width)]
    return raw-sum((frequency+shift)*(bb+bt/2)
                   for frequency, shift, bb, bt in zip(mu, ell, b, beta))


@pytest.mark.parametrize("p,cdeg,zero_labels", [(17, 4, False), (17, 7, False),
                                               (2**127-1, 7, False), (17, 7, True)])
def test_entire_compiled_phase_equals_untruncated_symbolic_expansion(p, cdeg, zero_labels, monkeypatch):
    st = ClassThreeStructure(p, (((0, 1), (p-1, 0)),),
                            (((0, 7), (p-7, 0)), ((0, 3), (p-3, 0))),
                            (((1,), (0,)), ((0,), (1,))))
    chart = FullTaylorJetChart(p, 1, 2, 2)
    labels = [(0, 0)]*3 if zero_labels else [(0, 0), (2, 3), (4, 1)]
    scales, outcomes = [1, 1, 2], [(2,), (3,), (2,)]
    alignment = align_full_jet(chart, st, labels, scales, outcomes)
    spectator = (3, 5, 7)
    assert alignment.carrier_width-chart.jet_width == len(spectator)
    def forbidden(*_args, **_kwargs):
        raise AssertionError("hidden fixture evaluation is not a compilation primitive")
    monkeypatch.setattr(SymbolicScalarPacket, "evaluate_fixture", forbidden)
    packet = compile_full_jet_phase(alignment, spectator, cdeg)
    q = sp.Symbol("q")
    t = sp.symbols(f"t0:{chart.jet_width}")
    theta = sp.symbols(f"h0:{len(packet.parameter_basis)}")
    point = t+tuple(map(sp.Integer, spectator))
    carrier = [sum(coef*v for coef, v in zip(row, point)) for row in alignment.inverse]
    expression = 0
    for n, (label, s, y) in enumerate(zip(labels, scales, outcomes)):
        components = [sum(value*(y[0]+s*q)**nu[0]
                          for (component, nu), value in zip(packet.parameter_basis, theta)
                          if component == i) for i in range(5)]
        expression -= _phase(st, label, components[:2], components[2:3], components[3:],
                             carrier[3*n:3*n+2], carrier[3*n+2:3*n+3])
    # Reduce rational coefficients only AFTER unrestricted exact expansion.
    symbolic = sp.Poly(expression, q, *t, *theta)
    expected = {}
    for powers, coefficient in symbolic.terms():
        assert coefficient.is_Rational is True
        numerator, denominator = coefficient.as_numer_denom()
        value = int(numerator)*pow(int(denominator), -1, p) % p
        if value:
            alpha, lifted = powers[:chart.width], powers[chart.width:]
            params = tuple(i for i, exponent in enumerate(lifted) for _ in range(exponent))
            expected[(alpha, params)] = value
    assert packet.terms == expected
    assert max(map(lambda key: len(key[1]), expected)) == (1 if zero_labels else 2)
    assert weighted_degree(chart, packet) <= max(cdeg, 3*chart.degree)
    if not zero_labels:
        assert weighted_degree(chart, packet) == max(cdeg, 3*chart.degree)
        assert any(len(params) == 2 and len(set(params)) == 2 for _, params in expected)
    # Spectator effects must be present; they are not discarded as global phase.
    zero = compile_full_jet_phase(alignment, (0, 0, 0), cdeg)
    assert any(value != zero.terms.get(key, 0) and any(key[0])
               for key, value in packet.terms.items())
    # The tighter envelope needs the ACTUAL block-separated Taylor map.
    transported = packet
    for scale, y in ((2, (3,)), (3, (1,))):
        z = tuple((i+1) % p for i in range(chart.jet_width))
        _, matrix = chart.affine_map(y, z, scale)
        assert all(not x for row in matrix[:1] for x in row[1:])
        assert all(not row[0] for row in matrix[1:])
        transported = pullback_phase(chart, transported, y, z, scale)
        verify_full_jet_phase_support(chart, transported, st.a_width, st.b_width, st.c_width, cdeg)
    opposite = SymbolicScalarPacket(p, 1, chart.jet_width, packet.parameter_basis,
                                    {key: -value % p for key, value in packet.terms.items()})
    degree = weighted_degree(chart, packet)
    merged = weighted_merge(chart, (packet, opposite), (1, 1),
                            (((1,), (0,)*chart.jet_width),
                             ((2,), (1,)*chart.jet_width)), degree)
    verify_full_jet_phase_support(chart, merged, st.a_width, st.b_width, st.c_width, cdeg)
    assert weighted_degree(chart, merged) < degree


def test_hidden_dependent_carrier_breaks_quadratic_parameter_bound():
    # Filiform algebra: beta(a,x)=a0*x1-a1*x0, delta(a,b)=a0*b.
    # Valid public carrier x=(0,t): Phi=-a0^2*t/6. Illegally setting
    # t=h makes the same formula cubic in h. No finite fitting can fix this.
    st = ClassThreeStructure(17, (((0, 1), (16, 0)),),
                            (((0, 0), (0, 0)),), (((1,), (0,)),))
    h, t = sp.symbols("h t")
    public = sp.expand(_phase(st, [1], [h, 0], [0], [0], [0, t], [0]))
    assert public == -h*h*t/6
    assert sp.Poly(public, h).degree() == 2
    hidden = sp.Poly(public.subs(t, h), h)
    assert hidden.degree() == 3
    assert all((int(6*hidden.eval(v)) + v**3) % 17 == 0 for v in range(17))


@pytest.mark.parametrize("D", [1, 2, 4])
def test_weight_three_D_is_necessary_without_extra_source_structure(D):
    q, t, h = sp.symbols("q t h")
    polynomial = sp.Poly(-h*h*q**(2*D)*t/6, q, t, h)
    assert max(a + D*b for (a, b, _), _coef in polynomial.terms()) == 3*D
    assert max(c for (_a, _b, c), _coef in polynomial.terms()) == 2
    # This is the exact filiform phase, not a postulated cubic term.
    st = ClassThreeStructure(17, (((0, 1), (16, 0)),),
                            (((0, 0), (0, 0)),), (((1,), (0,)),))
    assert sp.expand(_phase(st, [1], [h*q**D, 0], [0], [0], [0, t], [0])) == polynomial.as_expr()


@pytest.mark.parametrize("alpha,params", [
    ((0, 2, 0, 0), (0, 0)),  # quadratic hidden coefficients cannot have t-degree two
    ((0, 1, 0, 0), (2,)),  # central coefficients have no carrier dependence
    ((3, 0, 0, 0), (0,)),  # linear A/B coefficients have q-degree at most D
    ((1, 0, 0, 0), (1, 1)),  # B*B terms are absent
    ((1, 0, 0, 0), (0, 2)),  # central cross-products are absent
])
def test_generic_weight_bound_does_not_imply_source_structure(alpha, params):
    chart = FullTaylorJetChart(17, 1, 1, 2)
    basis = ((0, (0,)), (1, (0,)), (2, (0,)))
    packet = SymbolicScalarPacket(17, 1, chart.jet_width, basis, {(alpha, params): 1})
    assert weighted_degree(chart, packet) <= 6
    with pytest.raises(ArithmeticError, match="source-structured"):
        verify_full_jet_phase_support(chart, packet, 1, 1, 1, 4)


def test_weight_triangular_but_cross_block_transport_breaks_sharper_bound():
    chart = FullTaylorJetChart(17, 1, 1, 2)
    basis = ((0, (0,)),)
    source = SymbolicScalarPacket(17, 1, chart.jet_width, basis,
                                  {((4, 0, 0, 1), (0, 0)): 1})
    verify_full_jet_phase_support(chart, source, 1, 0, 1, 4)
    # t_(weight 2) <- t_(weight 2)+q is lower-weight affine, but NOT Taylor transport.
    terms = dict(source.terms)
    terms[((5, 0, 0, 0), (0, 0))] = 1
    invalid = SymbolicScalarPacket(17, 1, chart.jet_width, basis, terms)
    assert weighted_degree(chart, invalid) == weighted_degree(chart, source) == 6
    with pytest.raises(ArithmeticError, match="source-structured"):
        verify_full_jet_phase_support(chart, invalid, 1, 0, 1, 4)


@pytest.mark.parametrize("basis", [((2, (0,)),), ((0, (3,)),), ((1, (5,)),), ((0, (0, 0)),)])
def test_support_certificate_cannot_hide_extra_unknown_coefficients(basis):
    chart = FullTaylorJetChart(17, 1, 1, 2)
    packet = SymbolicScalarPacket(17, 1, chart.jet_width, basis, {((1, 0, 0, 0), (0,)): 1})
    with pytest.raises(ValueError, match="potential coefficient schema"):
        verify_full_jet_phase_support(chart, packet, 1, 0, 1, 4)
