from fractions import Fraction
import itertools

import pytest

from dcp_physical_phase_noise import read
from dcp_systematic_source_transport import (
    _complete_source_controls, _multiply, compile_transport, native_systematic_source_certificate,
)


def test_all_small_native_source_tables_are_exact_systematic_bijections():
    records = _complete_source_controls()
    assert [r["all_invertible_binary_prefixes"] for r in records] == [1, 6]
    assert [r["complete_tail_label_vectors"] for r in records] == [8, 64]
    assert read(records[1]["exact_acceptance_probability"]) == Fraction(3, 8)
    assert records[1]["fixed_secret_phase_covariance_checks"] == 1152


def test_transport_cannot_depend_on_hidden_higher_prefix_bits():
    P = ((1, 1), (0, 1))
    transport = compile_transport(P, 16)
    left = ((1, 1, 5), (0, 1, 7))
    right = ((9, 3, 5), (6, 13, 7))
    A, B = transport.transform_labels(left), transport.transform_labels(right)
    assert A[0][-1] == B[0][-1] and A[1][-1] == B[1][-1]
    assert A != B
    assert transport.record()["selection_uses_binary_prefix_only"]
    assert not transport.record()["row_transform_uses_actual_full_label_prefix_inverse"]


def test_full_label_prefix_inverse_is_a_source_countercontrol_not_same_transport():
    q = 8
    original_odd_prefix = tuple(range(1, q, 2))
    full_inverse_outputs = {a * pow(a, -1, q) % q for a in original_odd_prefix}
    low_only_outputs = {compile_transport(((1,),), q).transform_labels(((a,),))[0][0] for a in original_odd_prefix}
    assert full_inverse_outputs == {1}
    assert low_only_outputs == set(original_odd_prefix)
    ledger = native_systematic_source_certificate(1, 8)
    assert not ledger["transformed_prefix_full_labels_are_exact_identity"]


def test_secret_transform_is_covariant_at_large_composite_modulus_without_field_assumptions():
    q = 1 << 65
    P = ((1, 1, 0), (0, 1, 1), (1, 1, 1))
    transport = compile_transport(P, q)
    identity = tuple(tuple(int(i == j) for j in range(3)) for i in range(3))
    assert _multiply(transport.row_transform, transport.row_transform_inverse, q) == identity
    labels = ((q - 1, 1, q - 2, q - 5), (2, q - 3, 1, q - 7), (1, 3, q - 9, q - 11))
    transformed = transport.transform_labels(labels)
    secret = (q - 1, q - 13, 1 << 60)
    sp = transport.transport_secret(secret)
    assert transport.recover_secret_coordinates(sp) == secret
    for i in range(4):
        assert sum(labels[l][i] * secret[l] for l in range(3)) % q == sum(transformed[l][i] * sp[l] for l in range(3)) % q
    assert transport.record()["modulus_hex"] == hex(q)


def test_q_over_two_coordinates_transform_back_without_recovering_original_top_bits():
    q = 16
    transport = compile_transport(((1, 1), (0, 1)), q)
    for s in itertools.product(range(q), repeat=2):
        sp = transport.transport_secret(s)
        recovered = transport.recover_secret_coordinates(tuple(x % (q // 2) for x in sp))
        assert tuple(x % (q // 2) for x in recovered) == tuple(x % (q // 2) for x in s)
    assert native_systematic_source_certificate(2, 32)["lost_original_top_bits_still_require_fresh_completion"]


def test_packet_coordinate_changes_cannot_be_ignored_when_combining_candidates():
    original = (1, 2)
    left = compile_transport(((1, 0), (0, 1)), 8)
    right = compile_transport(((0, 1), (1, 0)), 8)
    assert left.transport_secret(original) != right.transport_secret(original)
    assert right.recover_secret_coordinates(right.transport_secret(original)) == original


def test_prefix_acceptance_and_every_failed_attempt_are_charged():
    row = native_systematic_source_certificate(2, 20, attempts=8)
    assert read(row["exact_binary_prefix_acceptance_probability"]) == Fraction(3, 8)
    assert read(row["all_allocated_attempts_reject_probability"]) == Fraction(5, 8) ** 8
    assert row["original_states_charged"] == 160
    for n in (1, 2, 4, 8, 32, 64):
        assert read(native_systematic_source_certificate(n, 4 * n * n)["expected_attempts_until_acceptance"]) < 4
    assert not row["uniform_secret_average_is_automatically_a_fixed_secret_decoder_guarantee"]


def test_invalid_prefix_rank_modulus_and_label_domains_are_rejected():
    for P, q in ((((1, 1), (1, 1)), 8), (((1, 0),), 8), (((True,),), 8), (((1,),), 12), (((1,),), 4)):
        with pytest.raises(ValueError):
            compile_transport(P, q)
    transport = compile_transport(((1, 0), (0, 1)), 8)
    for labels in (((1,), (0,)), ((0, 0), (0, 1)), ((1, 0), (0, 1, 1))):
        with pytest.raises(ValueError):
            transport.transform_labels(labels)
    for args in ((0, 4), (2, 1), (True, 4)):
        with pytest.raises(ValueError):
            native_systematic_source_certificate(*args)
    with pytest.raises(ValueError):
        native_systematic_source_certificate(2, 4, attempts=0)
