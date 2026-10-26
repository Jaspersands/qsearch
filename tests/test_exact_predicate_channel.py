"""Exact amplitude/spectrum checks and countercontrols for the review deduction."""
from fractions import Fraction as Q
from itertools import product
from math import prod

import pytest

from theorems.balanced_filter_channel_audit import (
    _fixture, _fwht, audit_instance, exact_pattern_law,
)


def counts(data, length):
    out = [0]*(1 << length)
    for valid, pattern in zip(data["native_code"], data["target_masks"]):
        if valid:
            out[pattern] += 1
    return out


def direct_source(data, targets):
    return [prod(data["spectra"][b][x] for b, x in zip(targets, word)) for word in data["words"]]


def test_every_signed_legal_support_mask_matches_all_signed_output_amplitudes():
    data = _fixture(2, 3, 2, 1)
    active = [s for s in range(8) if s.bit_count() <= 1]
    saw_zero_native_with_nonzero_herald = False
    checked = 0
    for targets in product((0, 1), repeat=3):
        b = sum(x << i for i, x in enumerate(targets))
        source = direct_source(data, targets)
        for values in product((-1, 0, 1), repeat=len(active)):
            mask = [0]*8
            for i, value in zip(active, values):
                mask[i] = value
            law = exact_pattern_law(targets, counts(data, 3), data["messages"], data["size"], mask, 4)
            masked = [v*mask[s] for v, s in zip(source, data["supports"])]
            summed = [sum(masked[z ^ d] for d in data["code"]) for z in range(data["size"])]
            transformed = _fwht(summed)
            for index, valid, label in zip(data["dual"], data["native_code"], data["target_masks"]):
                expected = data["messages"]*data["size"]*law["kernel"][b ^ label] if valid else 0
                assert transformed[index] == expected
            assert 0 <= law["herald_probability"] <= law["source_filter_mass"] <= 1
            if sum(mask) == 0 and law["herald_probability"] > 0:
                assert law["native_success"] == 0
                assert law["conditional_native_point_probability"] is None
                saw_zero_native_with_nonzero_herald = True
            checked += 1
    assert checked == 648 and saw_zero_native_with_nonzero_herald


def test_direct_compressed_gram_equals_hadamard_diagonal_fiber_count_matrix():
    data = _fixture(3, 3, 1, 1)
    q, size, messages = data["q"], data["size"], data["messages"]
    fibers = counts(data, 3)
    lambdas = [Q(messages*8*c, size) for c in fibers]
    walsh = [2*data["spectra"][0][u]-q*(u == 0) for u in range(q)]
    assert walsh == [a-b for a, b in zip(data["spectra"][0], data["spectra"][1])]
    basis, images = [], []
    for sigma in range(8):
        phi = [prod(Q(walsh[u], q) if sigma >> i & 1 else Q(int(u == 0)) for i, u in enumerate(word))
               for word in data["words"]]
        basis.append(phi)
        images.append([sum(phi[z ^ d] for d in data["code"]) for z in range(size)])
    for sigma in range(8):
        for tau in range(8):
            assert sum(a*b for a, b in zip(basis[sigma], basis[tau])) == int(sigma == tau)
            actual = sum(a*b for a, b in zip(images[sigma], images[tau]))/messages
            expected = sum(lam*(1-2*(((sigma ^ tau) & c).bit_count() % 2)) for c, lam in enumerate(lambdas))/8
            assert actual == expected


def test_physical_example_matches_exact_fiber_count_and_uniformity():
    row = audit_instance(3, 4, 1, 2, (0, 1, 0, 1))
    channel = row["channels"]["padded_list_projection"]
    assert row["native_witness_count"] == 40
    assert Q(*channel["native_valid_probability_per_attempt"]) == Q(5, 4)*Q(11, 16)**2/2 == Q(605, 2048)
    assert channel["conditional_probability_per_native_witness"] == [1, 40]
    assert channel["exact_pattern_amplitudes_checked"]
    assert sum(Q(*p) for p in channel["predicate_pattern_probabilities_per_attempt"]) == Q(*channel["herald_probability"])


def test_branch_dependent_padding_is_physical_but_breaks_pattern_uniformity():
    data = _fixture(3, 4, 1, 2)
    targets = (0, 1, 0, 1)
    source = direct_source(data, targets)
    ball = [v if weight <= 2 else 0 for v, weight in zip(source, data["weights"])]
    summed = [sum(ball[z ^ d] for d in data["code"]) for z in range(data["size"])]
    # P2 for singleton cosets, P8 otherwise; both <= the eight messages.
    assert max(map(len, data["lists"])) == 2
    variable = [v*(2 if len(candidates) == 1 else 1) for v, candidates in zip(summed, data["lists"])]
    readout = _fwht(variable)
    source_scale = Q(16, 8**8)
    physical_scale = source_scale/(data["messages"]*8*data["size"])
    herald = physical_scale*sum(v*v for v in readout)
    ball_mass = source_scale*sum(v*v for v in ball)
    assert 0 <= herald <= ball_mass <= 1
    assert all(readout[j] == 0 for j, valid in zip(data["dual"], data["native_code"]) if not valid)
    native_squares = {readout[j]**2 for j, valid, pattern in zip(data["dual"], data["native_code"], data["target_masks"])
                      if valid and pattern == 10}
    assert len(native_squares) > 1  # Not just a harmless common/global phase.


def test_label_dependent_mask_really_leaves_the_proved_pattern_subspace():
    data = _fixture(3, 3, 1, 1)
    source = direct_source(data, (0, 0, 0))
    found = False
    for e, amplitude in enumerate(source):
        if amplitude == 0 or e == 0:
            continue
        # Retain one field label, not its entire zero/nonzero support pattern.
        values = [amplitude if z ^ e in data["code"] else 0 for z in range(data["size"])]
        readout = _fwht(values)
        native_amplitudes = {readout[j] for j, valid, pattern in zip(data["dual"], data["native_code"], data["target_masks"])
                             if valid and pattern == 0}
        if len(native_amplitudes) > 1:
            found = True
            break
    assert found


def test_empty_fiber_and_unpaid_operator_cannot_be_called_successful_sampling():
    data = _fixture(2, 3, 2, 1)
    fibers = counts(data, 3)
    empty = next(i for i, c in enumerate(fibers) if not c)
    targets = tuple(empty >> i & 1 for i in range(3))
    law = exact_pattern_law(targets, fibers, data["messages"], data["size"], [1]*8, 1)
    assert law["native_success"] == 0 and law["conditional_native_point_probability"] is None
    occupied = max(range(8), key=lambda i: fibers[i])
    targets = tuple(occupied >> i & 1 for i in range(3))
    unpaid = exact_pattern_law(targets, fibers, data["messages"], data["size"], [1]*8, 1)
    assert unpaid["herald_probability"] > 1  # No legal list-cap premise was supplied.


def test_all_fixed_syndromes_and_targets_use_charged_translation_not_syndrome_averaging():
    data = _fixture(2, 3, 2, 1)
    native = {x for x, valid in enumerate(data["native_code"]) if valid}
    cosets = set()
    nonempty, empty = 0, 0
    for a, b in product(range(4), repeat=2):
        offset = a | (b << 2)
        coset = frozenset(x ^ offset for x in native)
        cosets.add(coset)
        for targets in product((0, 1), repeat=3):
            pattern = sum(bit << i for i, bit in enumerate(targets))
            count = sum(data["target_masks"][x] == pattern for x in coset)
            row = audit_instance(2, 3, 2, 1, targets, (a, b, 0))
            channel = row["channels"]["padded_list_projection"]
            assert row["native_witness_count"] == count
            assert Q(*channel["native_valid_probability_per_attempt"]) == Q(16*8*count, 64)*Q(1, 2)**2/4
            assert channel["conditional_probability_per_native_witness"] == ([1, count] if count else None)
            assert channel["exact_pattern_amplitudes_checked"]
            if count:
                nonempty += 1
            else:
                empty += 1
    assert len(cosets) == 16 and len(set.union(*(set(c) for c in cosets))) == 64
    assert nonempty and empty and nonempty+empty == 128


def test_equivalent_public_offsets_give_the_same_paid_pattern_distribution():
    data = _fixture(3, 3, 1, 1)
    nonzero_native = next(x for x, valid in enumerate(data["native_code"]) if valid and x)
    offset = 3
    first = data["words"][offset]
    second = data["words"][offset ^ nonzero_native]
    assert first != second
    for targets in product((0, 1), repeat=3):
        a = audit_instance(3, 3, 1, 1, targets, first)
        b = audit_instance(3, 3, 1, 1, targets, second)
        assert a["channels"]["padded_list_projection"] == b["channels"]["padded_list_projection"]


@pytest.mark.parametrize("offset", [(True, 0, 0), (4, 0, 0), (-1, 0, 0), (0, 0)])
def test_public_offsets_are_validated(offset):
    with pytest.raises(ValueError, match="offset"):
        audit_instance(2, 3, 2, 1, (0, 0, 0), offset)


@pytest.mark.parametrize("change", [
    {"fiber_counts": [1]*8}, {"targets": (True, 0, 0)},
    {"mask": [2]*8}, {"mask": [1]*7}, {"padding": 3}, {"padding": 32},
])
def test_pattern_identity_rejects_inconsistent_counts_masks_and_dimensions(change):
    data = _fixture(2, 3, 2, 1)
    args = {"targets": (0, 0, 0), "fiber_counts": counts(data, 3), "message_count": data["messages"],
            "ambient_size": data["size"], "mask": [1]*8, "padding": 4}
    with pytest.raises(ValueError):
        exact_pattern_law(**(args | change))
