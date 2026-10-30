"""Bounded semantic controls, not emitted circuits or a uniform source proof."""
from dataclasses import replace
import random

import pytest

import theorems.guarded_bch_permutation as guarded
import theorems.uniform_bch_rees as bch
from theorems.guarded_bch_permutation import GuardedBCHPermutation


def _model(p=3, scale=1):
    return GuardedBCHPermutation(
        prime=p, nilpotency_class=2, group_dimension=3, control_dimension=2,
        section=lambda u: (u[0], u[1], u[0] * u[1] % p),
        weights=(1, 1, 2), scale=scale,
        bracket=lambda x, y: (0, 0, (x[0] * y[1] - x[1] * y[0]) % p),
    )


def _decode(word, n, p):
    base = 2 ** (p - 1).bit_length()
    return tuple(word // base**i % base for i in range(n))


def _encode(vector, p):
    base = 2 ** (p - 1).bit_length()
    return sum(v * base**i for i, v in enumerate(vector))


def _product(x, y, p):
    # Independent class-two Heisenberg product in logarithmic coordinates.
    a, b, z = x
    c, d, t = y
    return ((a + c) % p, (b + d) % p,
            (z + t + pow(2, -1, p) * (a * d - b * c)) % p)


def _expected(control, target, p, scale, inverse=False):
    u, v = _decode(control, 2, p)
    x = _decode(target, 3, p)
    if scale == 0 or max((u, v) + x) >= p:
        return target
    sign = 1 if inverse else -1
    y = tuple(sign * t % p for t in (scale * u, scale * v, scale**2 * u * v))
    return _encode(_product(x, y, p), p)


@pytest.mark.parametrize("scale", [0, 1, 2])
def test_exhaustive_padded_controls_targets_inverse_and_cleanup(scale):
    model = _model(scale=scale)
    for control in range(16):
        outputs = set()
        for target in range(64):
            expected = _expected(control, target, 3, scale)
            actual = model.permutation(control, target)
            assert actual == expected
            outputs.add(actual)
            assert model.permutation(control, target, inverse=True) == _expected(
                control, target, 3, scale, inverse=True)
            assert model.permutation(control, actual, inverse=True) == target
            backward = model.permutation(control, target, inverse=True)
            assert model.permutation(control, backward) == target
            assert model.lift(control, target) == (control, expected, 0)
            assert model.lift(control, expected, 0, inverse=True) == (control, target, 0)
            assert model.pack(model.unpack(target)) == target
            assert model.unpack(target) == _decode(target, 3, 3)
            assert model.pack(model.unpack(control, control=True), control=True) == control
        assert outputs == set(range(64))


@pytest.mark.parametrize("scale", [0, 1, 2])
def test_arbitrary_nonzero_auxiliary_reverse_gate_sequence(scale):
    model = _model(scale=scale)
    for control in range(16):
        for target in range(64):
            for auxiliary in (1, 3, 21, 63):
                start = (control, target, auxiliary)
                forward = model.lift(*start)
                new_target = auxiliary ^ _expected(control, target, 3, scale)
                new_auxiliary = target ^ _expected(control, new_target, 3, scale, True)
                assert forward == (control, new_target, new_auxiliary)
                assert model.lift(*forward, inverse=True) == start
                backward = model.lift(*start, inverse=True)
                assert model.lift(*backward) == start


def test_padding_and_zero_scale_never_evaluate_callbacks():
    def forbidden(*args):
        raise AssertionError("guarded branch evaluated a callback")

    model = replace(_model(), section=forbidden, bracket=forbidden)
    for control in range(16):
        for target in range(64):
            invalid = max(_decode(control, 2, 3) + _decode(target, 3, 3)) >= 3
            for candidate in (replace(model, scale=0),) + ((model,) if invalid else ()):
                assert candidate.permutation(control, target) == target
                assert candidate.permutation(control, target, inverse=True) == target
                assert candidate.lift(control, target) == (control, target, 0)


def test_nonhomomorphic_section_and_right_action_orientation():
    model = _model()
    u, v = (1, 0), (0, 1)
    assert model.section((1, 1)) != _product(model.section(u), model.section(v), 3)
    control, target = model.pack(u, control=True), model.pack((0, 1, 0))
    right = model.unpack(model.permutation(control, target))
    assert right == _product((0, 1, 0), (2, 0, 0), 3)
    assert right != _product((2, 0, 0), (0, 1, 0), 3)


def test_naive_modular_reduction_is_not_a_binary_permutation():
    model = _model()
    control = model.pack((1, 1), control=True)

    def naive(target):
        reduced = _encode(tuple(v % 3 for v in _decode(target, 3, 3)), 3)
        return _expected(control, reduced, 3, 1)

    assert naive(0) == naive(3)  # Distinct binary inputs, same reduced vector.
    assert len({naive(x) for x in range(64)}) == 27
    assert len({model.permutation(control, x) for x in range(64)}) == 64
    assert model.permutation(control, 3) == 3


@pytest.mark.parametrize("changes", [
    {"prime": 1}, {"prime": True}, {"prime": 3.0},
    {"nilpotency_class": 0}, {"nilpotency_class": 3}, {"nilpotency_class": True},
    {"group_dimension": 0}, {"group_dimension": 3.0},
    {"control_dimension": -1}, {"control_dimension": 4}, {"control_dimension": True},
    {"weights": (1, 1)}, {"weights": (1, 1, 0)}, {"weights": (1, -1, 2)},
    {"weights": (1, True, 2)}, {"weights": None},
    {"scale": -1}, {"scale": 3}, {"scale": True}, {"scale": 1.0},
    {"section": None}, {"bracket": None},
])
def test_reject_malformed_public_parameters(changes):
    with pytest.raises(ValueError):
        replace(_model(), **changes)


@pytest.mark.parametrize("bad", [-1, 64, True, 1.5])
def test_reject_out_of_width_target_and_auxiliary(bad):
    model = _model()
    with pytest.raises(ValueError):
        model.permutation(0, bad)
    for inverse in (False, True):
        with pytest.raises(ValueError):
            model.lift(0, 0, bad, inverse=inverse)


@pytest.mark.parametrize("bad", [-1, 16, True, 1.5])
def test_reject_out_of_width_control_even_at_zero_scale(bad):
    with pytest.raises(ValueError):
        _model(scale=0).permutation(bad, 0)


@pytest.mark.parametrize("bad", [(0,), (0, 0, 3), (0, -1, 0), (True, 0, 0), None])
def test_reject_malformed_section_values(bad):
    with pytest.raises(ValueError):
        replace(_model(), section=lambda u: bad).permutation(0, 0)


def test_raw_packing_and_bracket_validation():
    model = _model()
    assert model.limb_bits == 2
    assert model.pack((3, 2, 1)) == 27
    for bad in ((0,), (4, 0, 0), (-1, 0, 0), (True, 0, 0)):
        with pytest.raises(ValueError):
            model.pack(bad)
    for bad in ((0,), (0, 0, 3), (0, 0, True)):
        with pytest.raises(ValueError):
            replace(model, bracket=lambda x, y: bad).permutation(0, 0)


def test_trivial_quotient_and_characteristic_two_abelian_case():
    model = GuardedBCHPermutation(
        prime=2, nilpotency_class=1, group_dimension=1, control_dimension=0,
        section=lambda u: (0,), weights=(1,), scale=1, bracket=lambda x, y: (0,),
    )
    assert model.pack((), control=True) == 0
    for target in (0, 1):
        assert model.lift(0, target) == (0, target, 0)
    with pytest.raises(ValueError):
        model.permutation(1, 0)


def test_large_prime_samples_without_field_sized_ranges(monkeypatch):
    def bounded_range(*args):
        result = range(*args)
        assert result.stop <= 32 and result.start >= 0, "field-sized enumeration"
        return result

    monkeypatch.setattr(guarded, "range", bounded_range, raising=False)
    monkeypatch.setattr(bch, "range", bounded_range, raising=False)
    p = 2**127 - 1
    rng = random.Random(709)
    for scale in (0, 1, 2, p - 1):
        calls = 0
        model = _model(p, scale)
        bracket = model.bracket

        def counted(x, y):
            nonlocal calls
            calls += 1
            return bracket(x, y)

        model = replace(model, bracket=counted)
        samples = [((p - 1, p - 1), (p - 1, p - 1, p - 1)),
                   ((p, 0), (1, 2, 3)), ((1, 2), (0, p, 0))]
        samples += [(tuple(rng.randrange(p) for _ in range(2)),
                     tuple(rng.randrange(p) for _ in range(3))) for _ in range(8)]
        for u, x in samples:
            control, target = _encode(u, p), _encode(x, p)
            expected = _expected(control, target, p, scale)
            assert model.permutation(control, target) == expected
            assert model.permutation(control, expected, inverse=True) == target
            assert model.lift(control, target) == (control, expected, 0)
            auxiliary = rng.getrandbits(3 * 127)
            start = (control, target, auxiliary)
            assert model.lift(*model.lift(*start), inverse=True) == start
            assert model.lift(*model.lift(*start, inverse=True)) == start
        # Class two uses four bracket calls per active BCH evaluation;
        # each sample above makes at most twelve evaluations, regardless of p.
        assert calls <= len(samples) * 12 * 4
        assert (calls == 0) == (scale == 0)
