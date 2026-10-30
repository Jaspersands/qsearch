"""Public Gram-controller controls, not quantum execution or an advantage claim."""

from fractions import Fraction
from itertools import product
import random

import pytest

from theorems.invariant_gram_selector import FiliformGramController
from theorems.power_sde_budget import RandomnessExhausted


def _gram(frame, alpha, p):
    return tuple(tuple(sum(a * x * y for a, x, y in zip(alpha, u, v)) % p
                       for v in frame) for u in frame)


def _scales(frame, coordinates, p):
    return tuple(sum(t * row[i] for t, row in zip(coordinates, frame)) % p
                 for i in range(len(frame[0])))


def _controller(p, seed, *, zero_top=False, zero_beta=False):
    rng = random.Random(seed)
    size = 14 if p % 3 == 2 else 16
    ell = (0,) * size if zero_top else tuple(rng.randrange(p) for _ in range(size))
    beta = (0,) * size if zero_beta else tuple(rng.randrange(p) for _ in range(size))
    return FiliformGramController(p, ell, beta, bit_source=rng)


@pytest.mark.parametrize("p", (5, 7, 11, 13, 19, 101, 1009, (1 << 64)-59, (1 << 127)-1))
@pytest.mark.parametrize("zero_top,zero_beta", ((False, False), (True, False), (False, True)))
def test_all_moments_and_covariance_with_large_integer_fields(p, zero_top, zero_beta):
    controller = _controller(p, 123, zero_top=zero_top, zero_beta=zero_beta)
    rng = random.Random(120)
    alpha = tuple(rng.randrange(p) for _ in range(controller.arity))
    gram = _gram(controller.frame, alpha, p)
    assert len(controller.measurement_rows) == 6
    assert tuple(sum(a * x for a, x in zip(alpha, row)) % p
                 for row in controller.measurement_rows) == tuple(
                     gram[j][k] for j, k in controller.gram_entries)

    for t in ((1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 2, 3)):
        s = _scales(controller.frame, t, p)
        for a in (1, 2, p-1):
            moved = tuple((x + a * e * w) % p
                          for x, e, w in zip(alpha, controller.ell, s))
            assert _gram(controller.frame, moved, p) == gram

    witness = controller.select(gram)
    assert any(witness.scales)
    assert sum(e * s ** 3 for e, s in zip(controller.ell, witness.scales)) % p == 0
    assert sum(b * s * s for b, s in zip(controller.beta, witness.scales)) % p == 0
    assert sum(a * s * s for a, s in zip(alpha, witness.scales)) % p == 0
    assert controller.abort_bound <= Fraction(1, 2 ** controller.failure_bits)
    assert witness.uniform_calls <= controller.rng.call_cap
    assert witness.random_bits <= (controller.rng.call_cap * controller.rng.rejection_cap
                                   * (p-1).bit_length())


def test_three_odd_cubic_classes_and_zero_labels_do_not_exhaust_packing():
    for zeros in (0, 1, 2, 3, 7, 15, 16):
        labels = (0,) * zeros + (1, 2, 3) * 6
        ell = labels[:16]
        controller = FiliformGramController(7, ell, (1,) * 16,
                                            bit_source=random.Random(34))
        controller.verify_frame()
        assert len(controller.frame) == 3


def test_radical_is_retained_in_beta_restriction():
    controller = FiliformGramController(5, (0,) * 14, (0,) * 14,
                                        bit_source=random.Random(55))
    witness = controller.select(((0, 0, 0), (0, 0, 0), (0, 0, 0)))
    assert any(witness.scales)
    assert witness.uniform_calls == 0
    assert controller.root_calls == controller.conic_calls == 0


def test_all_ternary_diagonal_gram_outcomes_have_verified_witnesses():
    for diagonal in product(range(5), repeat=3):
        controller = FiliformGramController(5, (0,) * 14, (0,) * 14,
                                            bit_source=random.Random(71))
        gram = tuple(tuple(diagonal[i] if i == j else 0 for j in range(3))
                     for i in range(3))
        witness = controller.select(gram)
        assert sum(a * t * t for a, t in zip(diagonal, witness.coordinates)) % 5 == 0


def test_off_diagonal_gram_entries_cannot_be_discarded():
    controller = _controller(5, 123, zero_top=True, zero_beta=True)
    first, second, third = controller.frame
    frame = (tuple((x+y) % 5 for x, y in zip(first, second)), second, third)
    alpha = (1,) * controller.arity
    gram = _gram(frame, alpha, 5)
    assert any(gram[i][j] for i in range(3) for j in range(i+1, 3))
    bad = next(t for t in product(range(5), repeat=3)
               if any(t) and sum(gram[i][i] * t[i] ** 2 for i in range(3)) % 5 == 0
               and sum(gram[i][j] * t[i] * t[j]
                       for i in range(3) for j in range(3)) % 5 != 0)
    scales = _scales(frame, bad, 5)
    assert sum(a * s * s for a, s in zip(alpha, scales)) % 5 != 0


def test_invariant_weights_do_not_certify_invariant_complex_amplitudes():
    # ell=(1,-1), s=(1,1), beta=0; phase a(alpha)=omega**alpha[0].
    # On the moment hyperplane the weights stay one but the amplitude shifts.
    for x, shift in product(range(5), range(1, 5)):
        alpha = (x, -x % 5)
        moved = ((x+shift) % 5, (-x-shift) % 5)
        assert sum(alpha) % 5 == sum(moved) % 5 == 0
        assert (moved[0]-alpha[0]) % 5 == shift


@pytest.mark.parametrize("p", (True, 3, 9, 15))
def test_invalid_fields_are_rejected(p):
    with pytest.raises(ValueError):
        FiliformGramController(p, (0,) * 14, (0,) * 14)


@pytest.mark.parametrize("ell,beta", (((0,) * 13, (0,) * 14),
                                      ((0,) * 14, (0,) * 15),
                                      ((True,) + (0,) * 13, (0,) * 14),
                                      ((5,) + (0,) * 13, (0,) * 14)))
def test_malformed_central_records_rejected(ell, beta):
    with pytest.raises(ValueError):
        FiliformGramController(5, ell, beta)


def test_only_one_symmetric_gram_outcome_not_an_alpha_vector_is_consumed():
    controller = _controller(5, 7)
    with pytest.raises(ValueError):
        controller.select((0,) * 14)
    with pytest.raises(ValueError):
        controller.select(((1, 1, 0), (0, 1, 0), (0, 0, 1)))
    with pytest.raises(ValueError):
        controller.select(((True, 0, 0), (0, 1, 0), (0, 0, 1)))
    controller.select(((0, 0, 0), (0, 0, 0), (0, 0, 0)))
    with pytest.raises(ValueError):
        controller.select(((0, 0, 0), (0, 0, 0), (0, 0, 0)))


class _BadBits:
    def getrandbits(self, width):
        return (1 << width)-1


class _ZeroBits:
    def getrandbits(self, width):
        return 0


def test_fair_bit_rejection_is_bounded_and_aborts_not_a_witness():
    controller = FiliformGramController(5, (0,) * 14, (0,) * 14,
                                        failure_bits=1, bit_source=_BadBits())
    with pytest.raises(RandomnessExhausted, match="integer rejection"):
        controller.select(((1, 0, 0), (0, 1, 0), (0, 0, 1)))


def test_bounded_cube_root_failure_is_preserved():
    with pytest.raises(RandomnessExhausted, match="root splitting"):
        FiliformGramController(7, (1,) * 16, (0,) * 16,
                              failure_bits=1, bit_source=_ZeroBits())


@pytest.mark.parametrize("p", (7, 13, (1 << 127)-1))
def test_stronger_scalar_cubic_comparator_uses_only_three_inputs(p):
    from theorems.cubic_diagonal_solver import ternary_cubic_scales
    from theorems.scalar_fermat_solver import _field_root

    rng = random.Random(20261030)
    fixtures = (product(range(p), repeat=3) if p < 20 else
                (tuple(rng.randrange(p) for _ in range(3)) for _ in range(100)))
    for coefficients in fixtures:
        zero = next((i for i, a in enumerate(coefficients) if a == 0), None)
        witness = [0, 0, 0]
        if zero is not None:
            witness[zero] = 1
        else:
            pair = next(((i, j) for i in range(3) for j in range(i+1, 3)
                         if pow(coefficients[i], (p-1)//3, p)
                         == pow(coefficients[j], (p-1)//3, p)), None)
            if pair is not None:
                i, j = pair
                witness[i] = 1
                witness[j] = _field_root(
                    p, 3, -coefficients[i]*pow(coefficients[j], -1, p) % p)
            else:
                a, b, c = coefficients
                result = ternary_cubic_scales(p, (a, -b % p, c), rng=rng)
                one, y, z = result.scales
                assert one == 1
                witness = (z, y, 1)
        assert any(witness)
        assert sum(a*pow(s, 3, p) for a, s in zip(coefficients, witness)) % p == 0
