from fractions import Fraction
from itertools import product
from math import sqrt
import random

import numpy as np
import pytest

from theorems.hermite_streaming_composition import (
    bounded_subset, composition_ledger, failure_account, fourier,
    instrument_control, load_one_pass, loader_control, sampler_failure, source_law,
)


@pytest.mark.parametrize("q,ell", [(3, 1), (3, 2), (5, 2), (7, 1)])
def test_loader_matches_product_law_and_consumes_shuffled_stream_once(q, ell):
    result = loader_control(q, ell, Fraction(21, 50), 20)
    assert result["product_formula_max_residual"] < 1e-12
    assert result["stream_order_max_residual"] < 1e-12
    assert max(result["selector_one_mass"]) < 1e-25
    assert result["observed_good_scores"] == pytest.approx(
        [result["predicted_good_score"]]*(q-1), abs=1e-12)
    assert result["entries_consumed"] == (q-1)*q**ell
    assert result["omitted_rotation_selector_mass"] == pytest.approx(
        [result["predicted_omitted_rotation_mass"]["float"]]*(q-1), abs=1e-12)
    assert result["dirty_state_differs"]


def test_fourier_uses_additive_vector_group_not_cyclic_extension():
    q, ell = 3, 2
    labels = list(product(range(q), repeat=ell))
    values = np.arange(q**ell)+1j*np.arange(q**ell)[::-1]
    expected = np.array([sum(value*np.exp(-2j*np.pi*sum(a*b for a, b in zip(x, y))/q)
                             for x, value in zip(labels, values))/sqrt(q**ell)
                         for y in labels])
    actual = fourier(values, q, ell)
    assert np.max(np.abs(actual-expected)) < 1e-12
    assert np.max(np.abs(actual-np.fft.fft(values, norm="ortho"))) > 1
    assert fourier(actual, q, ell, inverse=True) == pytest.approx(values)


def test_stream_promise_and_exact_parameter_checks():
    entries = [(i, z, int(z == i)) for i in range(2) for z in range(3)]
    class Once:
        used = False

        def __iter__(self):
            assert not self.used
            self.used = True
            return iter(entries)

    load_one_pass(3, 1, Fraction(2, 5), Once())
    for bad in (entries[:-1], entries+[entries[0]], [(i, z, 0) for i, z, _ in entries]):
        with pytest.raises(ValueError):
            load_one_pass(3, 1, Fraction(2, 5), iter(bad))
    with pytest.raises(ValueError):
        source_law(3, 1, 0.42)


@pytest.mark.parametrize("q,ell", [(3, 1), (3, 2), (5, 2), (11, 3)])
def test_score_lower_bound_including_odd_cardinality(q, ell):
    for numerator in range(1, 50):
        lam = Fraction(numerator, 100)
        law = source_law(q, ell, lam)
        assert law["theta"] < lam
        assert law["score"] >= 0.5+sqrt(float(lam*(1-lam)))-1/q


def test_sampler_exact_conditional_uniformity_and_failure_enumeration():
    # n=3, two draws, one trial: first consumes two bits, second one bit.
    masses, failures = {}, Fraction(0)
    for first, second in product(range(4), range(2)):
        words = iter([first, second])
        selected = bounded_subset(3, 2, 1, lambda bits: next(words))
        if selected is None:
            failures += Fraction(1, 8)
        else:
            masses[selected] = masses.get(selected, Fraction(0))+Fraction(1, 8)
    assert failures == sampler_failure(3, 2, 1) == Fraction(1, 4)
    assert masses == {(0, 1): Fraction(1, 4), (0, 2): Fraction(1, 4),
                      (1, 2): Fraction(1, 4)}
    assert bounded_subset(3, 0, 1, lambda bits: pytest.fail("no bits needed")) == ()
    assert bounded_subset(1, 1, 1, lambda bits: pytest.fail("no bits needed")) == (0,)
    assert bounded_subset(3, 1, 4, lambda bits: 3) is None


def test_sampler_bound_and_no_duplicates():
    rng = random.Random(8)
    for n in range(2, 13):
        for count in range(n+1):
            assert sampler_failure(n, count, 4) <= Fraction(count, 2**4)
            selected = bounded_subset(n, count, 32, rng.getrandbits)
            assert len(set(selected)) == count
            assert all(0 <= value < n for value in selected)


def test_unconditional_failure_charges_sampler_herald_and_synthesis():
    base = failure_account(10000, Fraction(1, 5), Fraction(1, 10000),
                           Fraction(0), Fraction(0))
    paid = failure_account(10000, Fraction(1, 5), Fraction(1, 10000),
                           Fraction(1, 1000), Fraction(1, 2000))
    assert paid["unconditional_total_failure_upper"]["float"] == pytest.approx(
        base["unconditional_total_failure_upper"]["float"]+0.0015)
    assert paid["conditioning_on_acceptance_used"] is False
    assert failure_account(100, Fraction(-1, 100), Fraction(0), Fraction(0),
                           Fraction(0))["unconditional_total_failure_upper"]["float"] == 1
    assert failure_account(100, Fraction(1, 10), Fraction(1), Fraction(0),
                           Fraction(0))["unconditional_total_failure_upper"]["float"] == 1


def test_composition_ledger_pays_randomness_without_claiming_runtime_speedup():
    ledger = composition_ledger()
    assert ledger["pins"] == 4301
    assert ledger["pin_sampler_trials_per_draw"] == 53
    assert 0 < ledger["pin_sampler_failure_upper"]["float"] <= 2**-40
    assert ledger["unconditional_total_failure_upper"]["float"] < 0.00004
    assert ledger["new_quantum_algorithm_claim_allowed"] is False
    assert ledger["approximate_gates_per_stream_entry"] == 0
    assert "NOT polylog" in ledger["total_time"]
    assert "log(q*ell)" in ledger["reversible_bits"]
    with pytest.raises(ValueError):
        composition_ledger(lam=Fraction(49, 100), tau=Fraction(43, 100))


def test_actual_decoder_instrument_erases_labels_and_keeps_herald_failure():
    result = instrument_control()
    assert result["accepted"] == [True, True, False]
    assert result["herald_failure_mass"]["float"] == pytest.approx(1/3)
    assert result["accepted_mass"]["float"] == pytest.approx(2/3)
    assert result["erased_error_registers_all_zero"]
    assert result["clean_zero_character_numerator"]["float"] == pytest.approx(4/3)
    assert result["retained_error_register_numerator"]["float"] == pytest.approx(2/3)
    assert result["not_the_full_product_source"]
