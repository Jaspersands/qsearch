from fractions import Fraction as F
from itertools import product

import numpy as np
import pytest

import bent_classical as b
from orbit_decoder import Geometry


@pytest.mark.parametrize("p,k", [(7, 1), (3, 2)])
def test_all_scale_flat_spectrum_and_forward_permutation(p, k):
    form = b.Form(p, tuple(range(k)), 2, 1)
    images = {form.permutation(y) for y in product(range(p), repeat=k)}
    assert len(images) == p**k
    values = np.empty((p,)*(2*k), complex)
    for v in range(1, p):
        for row in product(range(p), repeat=2*k):
            values[row] = np.exp(2j*np.pi*v*form.residual((*row, 0))/p)
        spectrum = np.fft.fftn(values)/p**(2*k)
        assert np.allclose(abs(spectrum), p**(-k), atol=1e-13)


def test_nonpermutation_source_does_not_get_flatness():
    x, y = np.indices((5, 5))
    spectrum = np.fft.fftn(np.exp(2j*np.pi*y**3/5))/25
    assert not np.allclose(abs(spectrum), 1/5)


@pytest.mark.parametrize("p,width", [(13, 3), (31, 5), (43, 7), (941, 5)])
def test_native_classical_perfect_witness(p, width):
    g, forms, allowed = b.instance(p, width, 271024)
    result = b.solve(g, forms, allowed, 271025)
    assert result["status"] == "VERIFIED_NATIVE_PERFECT"
    assert result["verification"]["score"] == len(forms)
    assert result["permutation_inverse_or_root_used"] is False
    assert result["quantum_resources"] == 0
    assert F(result["one_attempt_failure_bound"]) < F(1, width)
    assert b.verify(g, forms, allowed, result["coefficients"])["all_predicates_pass"]


def test_exact_singular_census_and_failed_attempts_are_real():
    g, forms, allowed = b.instance(7, 3, 1)
    singular = 0
    for a, c in product(range(7), repeat=2):
        result = b.linear_attempt(g, forms, allowed, ((a,), (c,)))
        singular += result["status"] == "RETRY_SINGULAR"
    assert 0 < F(singular, 49) <= F(2, 7)
    observed_retry = False
    for seed in range(100):
        result = b.solve(g, forms, allowed, seed, attempts=1)
        if result["status"] == "RETRY_SINGULAR":
            assert "coefficients" not in result
            assert result["attempts_executed"] == 1
            assert result["field_random_draws"] == 2
            observed_retry = True
            break
    assert observed_retry


def test_fixed_zero_image_gives_vandermonde_special_case():
    g, forms, allowed = b.instance(31, 5, 21)
    result = b.linear_attempt(g, forms, allowed, [f.shift for f in forms])
    assert result["rank"] == result["constraints"]
    assert result["verification"]["all_predicates_pass"]


@pytest.mark.parametrize("bad", ["dimension", "halfset", "field", "width"])
def test_contracts_fail_closed(bad):
    g, forms, allowed = b.instance(31, 5, 21)
    if bad == "dimension":
        g = Geometry(g.p, g.width, g.root, g.representatives, 3)
    elif bad == "halfset":
        allowed[0] = (0,)*15
    elif bad == "field":
        forms[0] = b.Form(7, (0, 0), 1, 0)
    else:
        forms[0] = b.Form(31, (0,), 1, 0)
    with pytest.raises(ValueError):
        b.solve(g, forms, allowed, 0)


def test_replay_rejects_noncanonical_or_oversized_polynomial():
    g, forms, allowed = b.instance(31, 5, 21)
    for coefficients in ([0.] * 18, [31], [0]*(g.dimension+1)):
        with pytest.raises(ValueError):
            b.verify(g, forms, allowed, coefficients)
