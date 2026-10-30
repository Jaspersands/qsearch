from fractions import Fraction

import pytest

from source_independence_control import (
    audit, convolution, distance_from_uniform, packet_frequencies, scale_average,
)


def test_literal_target_basis_counts_and_uniform_scale_average():
    counts = packet_frequencies()
    assert sum(counts) == 16
    assert counts[0] == 4
    assert all(counts[x] == counts[-x % 257] for x in range(257))
    averaged = scale_average(counts)
    assert sum(averaged) == 16 * 257
    assert averaged[0] == 4 * 257 + 12
    assert set(averaged[1:]) == {12}


def test_complete_source_distinguishes_independent_and_shared_scales():
    report = audit()
    assert report["single_packet_marginals_agree"]
    for row in report["rows"][1:]:
        assert Fraction(row["shared_scale_trace_distance"]) > Fraction(row["independent_scale_trace_distance"])
    final = report["rows"][-1]
    assert Fraction(final["independent_scale_trace_distance"]) < Fraction(1, 50000)
    assert Fraction(final["shared_scale_trace_distance"]) >= Fraction(256, 257**2)
    assert not report["quantum_execution"] and not report["speedup_established"]


def test_distributions_use_tensor_frequencies_not_entrywise_powers():
    assert convolution((1, 2, 0), (0, 1, 3)) == (6, 1, 5)
    assert distance_from_uniform((1, 1, 1)) == 0
    assert distance_from_uniform((1, 0, 0)) == Fraction(2, 3)


@pytest.mark.parametrize("bad", [0, 13, True, 1.5])
def test_reference_control_is_bounded(bad):
    with pytest.raises(ValueError):
        audit(bad)


def test_invalid_distributions_and_other_families_rejected():
    with pytest.raises(ValueError):
        packet_frequencies(131)
    with pytest.raises(ValueError):
        convolution((1,), (1, 0))
    with pytest.raises(ValueError):
        distance_from_uniform((0, 0))
