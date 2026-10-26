"""Exact vector/scalar projection controls for the original-source proof."""

from random import Random

import pytest

from theorems.class_three_monomial_jet import ClassThreeStructure


@pytest.mark.parametrize("p", [5, 17, (1 << 127)-1])
def test_all_character_projections_preserve_product_but_not_physical_group(p):
    beta = (((0, 1, 0), (p-1, 0, 0), (0, 0, 0)),
            ((0, 0, 0), (0, 0, 1), (0, p-1, 0)))
    gamma = (((0, 0, 1), (0, 0, 0), (p-1, 0, 0)),
             ((0, 1, 0), (p-1, 0, 1), (0, p-1, 0)))
    delta = (((0, 1), (0, 0), (p-1, 0)), ((0, 0), (0, 0), (0, 0)))
    vector = ClassThreeStructure(p, beta, gamma, delta)
    rng = Random(20261021)

    def sample():
        return tuple(tuple(rng.randrange(p) for _ in range(d)) for d in (3, 2, 2))

    for label in [(0, 0), (1, 0), (0, 1), (1, 2)]:
        def contract(forms):
            return (tuple(tuple(sum(label[k]*forms[k][i][j] for k in range(2)) % p
                                for j in range(len(forms[0][0])))
                          for i in range(len(forms[0]))),)

        scalar = ClassThreeStructure(p, beta, contract(gamma), contract(delta))

        def project(g):
            return g[:2]+((sum(a*b for a, b in zip(label, g[2])) % p,),)

        for _ in range(12):
            g, h, k = sample(), sample(), sample()
            assert project(vector.multiply_fixture(g, h)) == scalar.multiply_fixture(project(g), project(h))
            assert vector.multiply_fixture(vector.multiply_fixture(g, h), k) == (
                vector.multiply_fixture(g, vector.multiply_fixture(h, k)))

        # Projection is NOT a faithful encoding of the physical group.
        # The full source still has |C|=p^2 even if this scalar image is trivial.
        g = sample()
        kernel = (label[1], -label[0] % p) if any(label) else (1, 0)
        h = g[:2]+(tuple((a+b) % p for a, b in zip(g[2], kernel)),)
        assert g != h
        assert project(g) == project(h)
        assert vector.c_width == 2
        if label == (0, 0):
            assert any(c for form in scalar.beta for row in form for c in row)
            assert not any(c for form in scalar.gamma+scalar.delta for row in form for c in row)


def test_jacobi_is_an_input_obligation_not_an_inferred_source_property():
    # [a0,a1]=b0 and [a2,b0]=c0 without compensating cyclic terms.
    with pytest.raises(ValueError, match="Jacobi"):
        ClassThreeStructure(5,
            (((0, 1, 0), (4, 0, 0), (0, 0, 0)),),
            (((0, 0, 0), (0, 0, 0), (0, 0, 0)),),
            (((0,), (0,), (1,)),))
    # Looking only through the zero character would hide the bad Jacobi
    # tensor. A valid scalar projection cannot certify the physical input.
    collapsed = ClassThreeStructure(5,
        (((0, 1, 0), (4, 0, 0), (0, 0, 0)),),
        (((0, 0, 0), (0, 0, 0), (0, 0, 0)),),
        (((0,), (0,), (0,)),))
    assert collapsed.delta == (((0,), (0,), (0,)),)
