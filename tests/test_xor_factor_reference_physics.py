"""Exact factor-contraction and sampling laws against independent full sums."""
from fractions import Fraction
from math import prod
import random

import pytest

from theorems.affine_cluster_native_probe import socket_instance
from theorems.bpqm_gibbs_frontier import XorIsing, exact_gibbs
from theorems.xor_factor_reference import ExactXorReference, FactorReferenceLimit


@pytest.mark.parametrize("spins", range(1, 7))
def test_backward_sampling_law_equals_every_independent_gibbs_probability(spins):
    model, _ = socket_instance(spins, random.Random(71))
    c = Fraction(13, 20)
    reference = ExactXorReference(model, c)
    expected = exact_gibbs(model, c)
    actual = tuple(reference.probability(x) for x in range(1 << spins))
    assert actual == expected
    assert sum(actual) == 1
    integer_weights = [prod(33 if ((mask & x).bit_count() % 2 == sign) else 7
                            for mask, sign in model.clauses) for x in range(1 << spins)]
    assert reference.partition_integer == sum(integer_weights)
    assert reference.query_parity_mean == sum(p*(-1)**(x & 1) for x, p in enumerate(expected))


def test_free_spins_constant_frustrated_and_duplicate_factors_are_retained():
    model = XorIsing(4, ((0, 0), (0, 1), (2, 1), (2, 1), (10, 0)))
    for query in range(4):
        reference = ExactXorReference(model, "13/20", query_bit=query)
        target = exact_gibbs(model, "13/20")
        assert tuple(reference.probability(x) for x in range(16)) == target
        assert reference.query_parity_mean == sum(p*(-1)**((x >> query) & 1)
                                                  for x, p in enumerate(target))


def test_large_public_integer_coefficients_are_not_rounded_or_overflowed():
    model = XorIsing(2, ((1, 0),)*200 + ((2, 1),))
    reference = ExactXorReference(model, "13/20")
    assert reference.query_parity_mean == Fraction(33**200-7**200, 33**200+7**200)
    assert reference.partition_integer == (33**200+7**200)*(33+7)
    assert reference.ledger()["largest_bucket_variables"] == 1
    assert reference.ledger()["full_word_table_materialized"] is False


def test_operational_entry_caps_return_unknown_not_hardness_or_truncation():
    model = XorIsing(5, ((31, 0),))
    with pytest.raises(FactorReferenceLimit, match="UNKNOWN"):
        ExactXorReference(model, "1/2", max_entries=16)
    model = XorIsing(5, ((1, 0),))
    with pytest.raises(FactorReferenceLimit, match="UNKNOWN"):
        ExactXorReference(model, "1/2", total_entry_budget=4)


def test_sampling_uses_conditionals_for_every_spin_with_no_state_table_oracle():
    model = XorIsing(12, tuple(((1 << i) | (1 << (i+1)), i % 2) for i in range(11)))
    reference = ExactXorReference(model, "13/20", max_entries=32)
    class ExtremeRNG:
        def __init__(self, high):
            self.high = high
            self.calls = []

        def randrange(self, denominator):
            assert type(denominator) is int and denominator >= 2
            self.calls.append(denominator)
            return denominator-1 if self.high else 0

    low, high = ExtremeRNG(False), ExtremeRNG(True)
    assert reference.sample(low) == 0
    assert reference.sample(high) == (1 << 12)-1
    assert len(low.calls) == len(high.calls) == 12
    ledger = reference.ledger()
    assert ledger["peak_single_factor_entries"] <= 32
    assert ledger["full_word_table_materialized"] is False
    assert ledger["cost_exponential_in_elimination_width"] is True
    assert ledger["polynomial_general_algorithm_claimed"] is False


def test_actual_32_spin_reference_matches_saved_ground_truth_not_trace_means():
    import json
    from theorems.affine_cluster_native_probe import REPORT
    report = json.loads(REPORT.read_text())
    model, _ = socket_instance(32, random.Random(29))
    reference = ExactXorReference(model, "13/20")
    stored = report["targeted_stronger_falsifier"]["exact_factor_reference"]
    assert reference.ledger() == stored
    assert Fraction(-3, 5) < reference.query_parity_mean < Fraction(-1, 2)
    assert stored["peak_single_factor_entries"] == 1 << 19
    assert stored["full_word_table_materialized"] is False
    assert stored["query_parity_mask_hex"] == "0x1"


def test_reference_rejects_float_probabilities_and_invalid_observable():
    model = XorIsing(2, ((3, 0),))
    with pytest.raises(ValueError):
        ExactXorReference(model, .65)
    with pytest.raises(ValueError):
        ExactXorReference(model, "1/2", query_bit=2)
