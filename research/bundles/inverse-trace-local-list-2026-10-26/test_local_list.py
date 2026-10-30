from fractions import Fraction
from itertools import combinations

import pytest

import local_list as m


@pytest.fixture(scope="module", params=[(2, 7), (3, 11), (5, 37), (7, 131)])
def control(request):
    return m.finite_alphabet(*request.param)


def test_native_halfset_fourier_and_kloosterman_identity(control):
    c, f = control, control.field
    assert c.native_inverse_trace_alphabet
    assert len(c.alphabet) == c.q//2 and 0 not in c.alphabet
    assert c.inverse_walsh[0] == 0
    assert c.spectrum()[0] == c.q//2
    envelope = m.parameters(f.bits)[1]
    for b in range(1, c.q):
        k = sum(1-2*f.trace(f.inverse(a) ^ f.multiply(b, a))
                for a in range(1, c.q))
        assert c.inverse_walsh[b] == 1+k
        assert k*k <= 4*c.q
        assert abs(c.inverse_walsh[b]) <= envelope
        assert 2*c.spectrum()[b] == -c.inverse_walsh[b]


def test_exact_posterior_normalization_and_readout_countercontrol(control):
    c = control
    unit = tuple(int(i == 0) for i in range(len(c.alphabet)))
    assert m.positive_effect_posterior(c, (unit,), range(c.q)) == 1
    assert m.positive_effect_posterior(c, (unit,), (0,)) == Fraction(1, c.q)
    assert m.positive_effect_posterior(c, (unit,), ()) == 0
    # Fourier readout still guesses one symbol correctly with probability 1/2.
    row = tuple(c.characters[3][a] for a in c.alphabet)
    assert m.positive_effect_posterior(c, (row,), (3,)) == Fraction(1, 2)
    noise = m.fourier_readout_probabilities(c)
    assert noise[0] == Fraction(1, 2) and sum(noise) == 1
    for b in range(1, c.q):
        assert noise[b] == Fraction(c.inverse_walsh[b]**2, 2*c.q**2)


def test_exact_pair_optimum_and_mixed_effect_bound(control):
    c = control
    for right in range(1, c.q):
        witness = m.pair_optimum_witness(c, 0, right)
        actual = m.positive_effect_posterior(c, (witness,), (0, right))
        assert actual == Fraction(len(c.alphabet)+abs(c.spectrum()[right]), c.q)
        assert actual <= m.posterior_bound(c.field.bits, 2)
        # A sum of positive rank-one terms is not incorrectly treated as pure.
        second = tuple((-1)**i * Fraction(i+1, i+2) for i in range(len(witness)))
        mixed = m.positive_effect_posterior(c, (witness, second), (0, right))
        assert mixed <= m.posterior_bound(c.field.bits, 2)
        assert m.positive_effect_posterior(c, (second,), range(c.q)) == 1


@pytest.mark.parametrize("bits,modulus", [(3, 11), (5, 37)])
def test_all_native_pairs_have_no_unambiguous_effect(bits, modulus):
    c = m.finite_alphabet(bits, modulus)
    for pair in combinations(range(c.q), 2):
        assert m.unambiguous_subspace_dimension(c, pair) == 0


def test_affine_halfset_and_degree_two_are_real_exceptions():
    native = m.finite_alphabet(3, 11)
    f = native.field
    affine = tuple(a for a in range(f.order) if f.trace(a))
    c = m.finite_alphabet(3, 11, control_alphabet=affine)
    assert not c.native_inverse_trace_alphabet
    assert m.unambiguous_subspace_dimension(c, (0, 1)) == 1
    witness = m.pair_optimum_witness(c, 0, 1)
    assert m.positive_effect_posterior(c, (witness,), (0, 1)) == 1
    # General halfset uncertainty alone cannot prove our native bound.
    assert m.positive_effect_posterior(c, (witness,), (0, 1)) > m.posterior_bound(3, 2)
    small = m.finite_alphabet(2, 7)
    assert m.unambiguous_subspace_dimension(small, (0, 1)) == 1
    assert m.minimum_list_size(2) == 2


def test_large_lists_not_all_measurements_are_rejected():
    c = m.finite_alphabet(5, 37)
    labels = tuple(i for i, value in enumerate(c.spectrum()) if value)
    assert len(labels) >= m.minimum_list_size(5)
    assert m.unambiguous_subspace_dimension(c, labels) >= 1
    assert m.positive_effect_posterior(c, ((1,)*len(c.alphabet),), labels) == 1
    assert m.unambiguous_subspace_dimension(c, range(c.q)) == len(c.alphabet)
    assert m.unambiguous_subspace_dimension(c, ()) == 0


@pytest.mark.parametrize("bits", [2, 3, 5, 7, 17, 31, 127, 1024])
@pytest.mark.parametrize("confidence", [Fraction(1, 2), Fraction(2, 3), Fraction(99, 100), Fraction(1)])
def test_exact_scaling_bound_and_rounding(bits, confidence):
    size = m.minimum_list_size(bits, confidence)
    assert m.posterior_bound(bits, size) >= confidence
    assert m.posterior_bound(bits, size-1) < confidence
    assert m.posterior_bound(bits, 1) == Fraction(1, 2)
    assert m.posterior_bound(bits, 1 << bits) == 1


@pytest.mark.parametrize("bits", [0, 1, -2, True, 5.0])
def test_invalid_field_degree(bits):
    with pytest.raises(ValueError):
        m.parameters(bits)


@pytest.mark.parametrize("size", [-1, 33, True, 2.0])
def test_invalid_list_cardinality(size):
    with pytest.raises(ValueError):
        m.posterior_bound(5, size)


@pytest.mark.parametrize("confidence", [0, 2, -1, 0.5, True])
def test_invalid_confidence(confidence):
    with pytest.raises(ValueError):
        m.minimum_list_size(5, confidence)


def test_scope_and_input_guards():
    c = m.finite_alphabet(3, 11)
    for labels in ((0, 0), (-1,), (8,), (True,)):
        with pytest.raises(ValueError):
            m.unambiguous_subspace_dimension(c, labels)
    for vectors in ((), ((0,)*4,), ((1, 2),), ((1.0, 0, 0, 0),)):
        with pytest.raises(ValueError):
            m.positive_effect_posterior(c, vectors, (0,))
    with pytest.raises(ValueError):
        m.posterior_bound(3, 2, prior="known_symbol")
    with pytest.raises(ValueError):
        m.positive_effect_posterior(c, ((1,)*4,), (0,), prior="conditioned_on_other_symbols")
    with pytest.raises(ValueError, match="finite control cap"):
        m.finite_alphabet(17, 131075)
    with pytest.raises(ValueError, match="reducible"):
        m.finite_alphabet(3, 9)
    for alphabet in ((), (1, 1), (8,), (True,)):
        with pytest.raises(ValueError):
            m.finite_alphabet(3, 11, control_alphabet=alphabet)
