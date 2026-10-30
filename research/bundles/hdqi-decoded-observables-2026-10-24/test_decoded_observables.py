from fractions import Fraction as F
from itertools import product
import math
import random

import numpy as np
import pytest

import decoded_observables as d


def matrix(pauli, n):
    x, z, phase = pauli
    out = np.zeros((1 << n, 1 << n), dtype=complex)
    for i in range(1 << n):
        out[i ^ x, i] = (1j)**phase * (-1)**(i & z).bit_count()
    return out


def actual_output(estimator):
    model = estimator.model
    a = d.c.finite_exact_branch(model.pilot, estimator.plan["site_tail"])
    a /= np.linalg.norm(a)
    sectors = {}
    for y, value in enumerate(a):
        residue = y ^ estimator.decoder(model.label(y))
        physical = np.eye(1 << model.n, dtype=complex)
        for i, p in enumerate(model.paulis):
            if y >> i & 1:
                physical = physical @ matrix(p, model.n)
        vector = value * physical.reshape(-1)/math.sqrt(1 << model.n)
        sectors[residue] = sectors.get(residue, np.zeros_like(vector))+vector
    rho = sum(np.outer(v, v.conj()) for v in sectors.values())
    return rho


@pytest.mark.parametrize("value", (F(0), F(1), F(2), F(1, 3), F(10**200, 3), F(1, 10**200)))
@pytest.mark.parametrize("bits", (1, 8, 64))
def test_integer_square_root_has_relative_error_even_at_extreme_scales(value, bits):
    low = d.sqrt_lower(value, bits)
    assert low*low <= value
    assert low*low >= value*(1-F(1, 2**bits))**2


@pytest.mark.parametrize("pauli", ((1, 0, 0), (0, 1, 0), (1, 1, 1), (1, 1, 3)))
def test_exact_pauli_multiplication_and_dagger_include_y_phases(pauli):
    for other in ((1, 0, 0), (0, 1, 0), (1, 1, 1)):
        assert np.max(np.abs(matrix(d.multiply(pauli, other), 1)-matrix(pauli, 1)@matrix(other, 1))) < 1e-14
    assert np.max(np.abs(matrix(d.dagger(pauli), 1)-matrix(pauli, 1).conj().T)) < 1e-14


@pytest.mark.parametrize("paulis", (((1, 0, 0), (1, 0, 0), (0, 1, 0)),
                                    ((1, 0, 0), (0, 1, 0), (1, 1, 1))))
@pytest.mark.parametrize("bad_decoder", (False, True))
@pytest.mark.parametrize("observable", ((1, 0, 0), (0, 1, 0), (1, 1, 1), (0, 0, 0)))
def test_actual_decoded_physical_observable_matches_exact_signed_moments(paulis, bad_decoder, observable):
    model = d.Physical.create(1, paulis, [1, F(-1, 2), F(3, 4)], F(1, 4))
    representatives = {model.label(y): y for y in reversed(range(8))}
    decoder = (lambda syndrome: 0) if bad_decoder else (lambda syndrome: representatives.get(syndrome, 0))
    estimator = d.Estimator(model, decoder, observable)
    rho = actual_output(estimator)
    assert np.trace(rho) == pytest.approx(1)
    expected = np.trace(rho @ np.kron(matrix(observable, 1), np.eye(2)))
    moments = d.finite_moments(estimator)
    assert abs(expected.imag) < 1e-12
    assert abs(float(moments["numerator"]/moments["denominator"])-expected.real) <= float(estimator.plan["weight_relative_error"]/moments["denominator"])+1e-12
    assert moments["numerator_second_moment"] <= 1
    assert moments["denominator"] >= F(1, 2*estimator.plan["ratio_upper"])
    for y in range(8):
        match = d.partner(model, decoder, observable, y)
        if match is not None:
            reverse = d.partner(model, decoder, observable, match[0])
            assert reverse[0] == y
            assert y ^ decoder(model.label(y)) == match[0] ^ decoder(model.label(match[0]))


def test_incorrect_syndrome_and_out_of_image_observable_rows_are_zero():
    model = d.Physical.create(1, [(1, 0, 0)], [1], F(1, 4))
    assert d.partner(model, lambda syndrome: 0, (1, 0, 0), 0) is None
    assert d.partner(model, lambda syndrome: syndrome & 1, (0, 1, 0), 0) is None
    with pytest.raises(ValueError):
        d.partner(model, lambda syndrome: 2, (1, 0, 0), 0)


def test_rare_importance_weight_is_not_clipped_and_second_moment_stays_bounded():
    tiny = F(1, 10**120)
    qs = (1-tiny, tiny)
    weights = [d.sqrt_lower(qs[1-y]/qs[y], 40) for y in range(2)]
    assert weights[1] > 10**50
    assert sum(q*w*w for q, w in zip(qs, weights)) <= 1
    correct = sum(q*w for q, w in zip(qs, weights))
    clipped = sum(q*min(w, 1) for q, w in zip(qs, weights))
    assert clipped < correct*F(3, 4)


def test_precision_budget_refuses_uncertified_short_runs():
    model = d.Physical.create(1, [(1, 0, 0), (0, 1, 0)], [1, 1], F(1, 4))
    estimator = d.Estimator(model, lambda syndrome: syndrome, (1, 0, 0))
    plan = estimator.plan
    assert plan["blocks"] % 2 == 1
    assert plan["weight_relative_error"] <= plan["moment_error"]/2
    assert plan["block_draws"]*plan["moment_error"]**2 >= 16
    with pytest.raises(d.s.BudgetExceeded, match="no certified estimate"):
        estimator.estimate(random.Random(1), max_draws=100)


def test_actual_draws_are_rational_reproducible_and_resource_counted():
    model = d.Physical.create(1, [(1, 0, 0), (0, 1, 0)], [1, -1], F(1, 4))
    estimator = d.Estimator(model, lambda syndrome: syndrome, (1, 0, 0))
    left, right = random.Random(42), random.Random(42)
    for _ in range(50):
        a, b = estimator.draw(left), estimator.draw(right)
        assert a == b
        assert isinstance(a[0], F) and a[1] in (-1, 1)
        assert a[2] in (2, 3)
        assert a[3] <= a[2]*estimator.plan["max_word_letters"]


def test_invalid_nonhermitian_physical_input_is_rejected():
    with pytest.raises(ValueError):
        d.Physical.create(1, [(1, 1, 0)], [1], F(1, 4))


def test_every_small_decoder_table_still_gives_a_partial_involution():
    model = d.Physical.create(1, [(1, 0, 0), (0, 1, 0)], [1, 1], F(1, 4))
    for table in product(range(4), repeat=4):
        decoder = table.__getitem__
        for observable in ((1, 0, 0), (0, 1, 0), (1, 1, 1)):
            targets = []
            for y in range(4):
                row = d.partner(model, decoder, observable, y)
                if row is not None:
                    targets.append(row[0])
                    reverse = d.partner(model, decoder, observable, row[0])
                    assert reverse == (y, row[1])
            assert len(targets) == len(set(targets))


@pytest.mark.parametrize("observable", ((0, 2, 0), (1, 1, 1), (3, 0, 0)))
def test_two_physical_qubits_with_out_of_image_syndromes(observable):
    model = d.Physical.create(2, [(1, 0, 0), (0, 3, 0), (3, 1, 1)], [1, -1, 1], F(1, 4))
    table = {model.label(y): y for y in range(8)}
    estimator = d.Estimator(model, lambda syndrome: table.get(syndrome, 0), observable)
    rho = actual_output(estimator)
    expected = np.trace(rho @ np.kron(matrix(observable, 2), np.eye(4)))
    moments = d.finite_moments(estimator)
    assert np.trace(rho) == pytest.approx(1)
    assert abs(expected.imag) < 1e-12
    assert abs(float(moments["numerator"]/moments["denominator"])-expected.real) <= float(estimator.plan["weight_relative_error"]/moments["denominator"])+1e-12


@pytest.mark.parametrize("denominator,expected", ((F(1), F(1, 3)), (F(-1), None)))
def test_median_aggregation_success_and_denominator_refusal(monkeypatch, denominator, expected):
    model = d.Physical.create(1, [(1, 0, 0)], [1], F(1, 4))
    estimator = d.Estimator(model, lambda syndrome: syndrome & 1, (1, 0, 0))
    # Synthetic aggregation fixture, not a certified short physical run.
    estimator.plan.update(block_draws=3, blocks=3, total_draws=9)
    monkeypatch.setattr(estimator, "draw", lambda rng: (F(1, 3), denominator, 3, 6))
    out = estimator.estimate(random.Random(1), max_draws=9)
    assert out["estimate"] == expected
    assert out["status"] == ("estimate" if expected is not None else "refused")
    assert out["words"] == 27 and out["letters"] == 54

