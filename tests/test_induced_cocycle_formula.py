"""Universal coefficient identities and nonsplit/source-assumption falsifiers."""
from dataclasses import replace
from fractions import Fraction
from itertools import product
from math import factorial

import numpy as np
import pytest

from theorems.induced_cocycle_formula import (
    _basis_bracket, cocycle_certificate, operator_coefficients,
    verify_differential_coefficients, word_normal_form,
)
from theorems.metabelian_induced_phase import (
    MetabelianLieChart, cocycle_template, lie_word_cocycle_template,
)
from theorems.symbolic_scalar_phase_erasure import _fmpz_solve_coordinates
from tests.test_metabelian_induced_phase import filiform_chart
from tests.test_metabelian_phase_extension import finite_matrix_exp_log


@pytest.mark.parametrize("k", range(1, 8))
def test_universal_identity_not_sampled_input_values(k):
    cert = cocycle_certificate(k)
    cert.verify()
    assert len(cert.terms) == k*k
    assert cert.terms == word_normal_form(k)
    assert all(factorial(k) % c.denominator == 0 for _, c in cert.terms)
    for p in (17, 2**127-1):
        values = cert.field_terms(p)
        assert len(values) == k*k and all(0 < v < p for _, v in values)


def test_differential_identity_at_higher_class_without_word_expansion():
    # This tests the ODE's complete coefficient identity, not an exponential
    # word certificate or a quantum receiver at class 64.
    for k in (8, 16, 32, 64):
        verify_differential_coefficients(k)
        assert len(operator_coefficients(k)) == k*k
    with pytest.raises(ValueError, match="Lazard"):
        cocycle_certificate(5).field_terms(5)
    for bad in (0, -1, 1.5, True):
        with pytest.raises(ValueError):
            operator_coefficients(bad)


@pytest.mark.parametrize("key", [("B", 0, 0), ("B", 1, 1), ("C", 0, 0), ("C", 1, 1)])
def test_single_wrong_coefficient_is_rejected(key):
    cert = cocycle_certificate(4)
    broken = dict(cert.terms)
    broken[key] += 1
    with pytest.raises(ValueError, match="differential"):
        replace(cert, terms=tuple(sorted(broken.items()))).verify()
    with pytest.raises(ValueError, match="support"):
        replace(cert, terms=cert.terms[:-1]).verify()
    with pytest.raises(ValueError, match="canonical"):
        replace(cert, terms=cert.terms+cert.terms[:1]).verify()


def universal_chart(p, k):
    """A genuine nonsplit abelian extension, with the full universal module."""
    keys = (("A", 0, 0), ("X", 0, 0))+tuple(key for key, _ in operator_coefficients(k))
    position = {key: i for i, key in enumerate(keys)}
    table = []
    for a in keys:
        rows = []
        for b in keys:
            values = [0]*len(keys)
            for key, c in _basis_bracket(a, b, k).items():
                values[position[key]] = int(c) % p
            rows.append(tuple(values))
        table.append(tuple(rows))
    return MetabelianLieChart(p, 2, tuple(table)), keys


@pytest.mark.parametrize("p,k", [(17, 2), (17, 3), (17, 4), (2**127-1, 3)])
def test_entire_public_compiler_on_nonsplit_universal_extension(p, k):
    st, keys = universal_chart(p, k)
    assert st.nilpotency_class == k
    assert st.width == k*k+2
    curvature = keys.index(("C", 0, 0))
    # No change A->A+u, X->X+v can eliminate this coordinate of [A,X]:
    # [A,v] and [X,u] have zero C_00 coefficient, and [I,I]=0.
    assert st.brackets[0][1][curvature] == 1
    assert all(st.brackets[a][i][curvature] == 0 for a in (0, 1) for i in range(2, st.width))
    assert cocycle_template(st) == lie_word_cocycle_template(st)


def test_compiler_after_nontrivial_public_section_and_ideal_basis_change():
    st, _ = universal_chart(17, 3)
    basis = [tuple(int(i == j) for i in range(st.width)) for j in range(st.width)]
    # New section has ideal offsets; I itself is unchanged.
    basis[0] = tuple((a+b) % 17 for a, b in zip(basis[0], basis[2]))
    basis[1] = tuple((a+3*b) % 17 for a, b in zip(basis[1], basis[4]))
    basis[3] = tuple((a+2*b) % 17 for a, b in zip(basis[3], basis[5]))
    tensor = tuple(tuple(_fmpz_solve_coordinates(basis, st.bracket(a, b), 17) for b in basis) for a in basis)
    changed = MetabelianLieChart(17, 2, tensor)
    assert changed.brackets != st.brackets
    assert cocycle_template(changed) == lie_word_cocycle_template(changed)


def test_closed_compiler_does_not_call_the_exponential_word_or_hidden_values(monkeypatch):
    import theorems.metabelian_induced_phase as compiler
    st = replace(filiform_chart(19, 5), a_width=1)
    expected = lie_word_cocycle_template(st)
    cocycle_template.cache_clear()
    def forbidden(*args, **kwargs):
        raise AssertionError("exponential-word fallback is not the closed compiler")
    monkeypatch.setattr(compiler, "section_word_certificate", forbidden)
    assert cocycle_template(st) == expected


def test_two_ideal_inputs_and_noncommuting_actions_are_real_counterexamples():
    # ut_5 with I=N' has nonabelian I. The tempting formula is false here.
    p, n = 101, 5
    def e(i, j):
        value = np.zeros((n, n), dtype=object)
        value[i, j] = 1
        return value
    a, x, b = e(0, 1)+e(2, 3), e(1, 2)+e(3, 4), e(0, 2)
    bracket = lambda u, v: (u @ v-v @ u) % p
    curvature = bracket(a, x)
    assert np.any(bracket(curvature, b))
    assert not np.array_equal(bracket(a, bracket(x, b)), bracket(x, bracket(a, b)))
    predicted = np.zeros((n, n), dtype=object)
    for (seed, i, j), c in operator_coefficients(4):
        value = b if seed == "B" else curvature
        for _ in range(j):
            value = bracket(x, value)
        for _ in range(i):
            value = bracket(a, value)
        predicted = (predicted+c.numerator*pow(c.denominator, -1, p)*value) % p
    word = finite_matrix_exp_log((-a-x) % p, p) @ finite_matrix_exp_log(a+b, p) % p
    word = word @ finite_matrix_exp_log(x, p) % p
    actual = finite_matrix_exp_log(word, p, logarithm=True)
    assert not np.array_equal(predicted, actual)


def test_universal_bracket_jacobi_and_boundary_truncation():
    # The module is a Lie algebra before specialization, not a convenient
    # table that merely happens to match the desired cocycle coefficients.
    from theorems.induced_cocycle_formula import _bracket, _add
    k = 4
    _, keys = universal_chart(17, k)
    for a, b, c in product(keys, repeat=3):
        result = {}
        for x, y, z in ((a, b, c), (b, c, a), (c, a, b)):
            _add(result, _bracket({x: Fraction(1)}, _basis_bracket(y, z, k), k))
        assert not result
    assert not _basis_bracket(("A", 0, 0), ("B", 3, 0), k)
    assert _basis_bracket(("A", 0, 0), ("B", 2, 0), k) == {("B", 3, 0): 1}
