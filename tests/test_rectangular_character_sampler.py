from collections import Counter
from fractions import Fraction as Q
from itertools import permutations, product
import json
from math import factorial
import random

import numpy as np
import pytest

from core.involution_character_arithmetic import fixed_point_free_character
from theorems import rectangular_character_sampler as r
from theorems.representation_obstruction import hook_length_dimension, integer_partitions
from theorems.symmetric_character import rim_hook_removals, symmetric_character


@pytest.mark.parametrize("m", range(1, 7))
def test_actual_rsk_map_has_exact_plancherel_law(m):
    counts = Counter(r.rsk_shape(word) for word in permutations(range(m)))
    assert counts == {p: hook_length_dimension(p)**2 for p in integer_partitions(m)}


@pytest.mark.parametrize("k,m", [(1, 5), (2, 4), (3, 4), (4, 3), (7, 2)])
def test_exhaustive_actual_random_source_equals_full_qct_output_law(k, m):
    counts = Counter(r.colored_permutation_shape(perm, colors, k)
                     for perm in permutations(range(m))
                     for colors in product(range(k), repeat=m))
    denominator = k**m*factorial(m)
    assert sum(counts.values()) == denominator
    for shape in integer_partitions(k*m):
        expected = symmetric_character(shape, (k,)*m)**2
        assert counts[shape] == expected
        assert Q(counts[shape], denominator) == r.column_probability(shape, k, m)


def test_complete_columns_against_independent_rim_hook_recursion():
    result = r.exact_column_controls(16)
    assert result["complete_columns"] == 50
    assert result["partition_column_pairs"] > 1000


@pytest.mark.parametrize("k", [1, 2, 3, 5, 9])
def test_abacus_roundtrip_and_degree_for_different_runner_populations(k):
    rng = random.Random(811+k)
    for _ in range(25):
        parts = []
        for _ in range(k):
            m = rng.randrange(12)
            permutation = list(range(m))
            rng.shuffle(permutation)
            parts.append(r.rsk_shape(tuple(permutation)))
        quotient = tuple(parts)
        shape = r.assemble_quotient(quotient)
        assert sum(shape) == k*sum(map(sum, quotient))
        assert r.empty_core_quotient(shape, k) == quotient


def test_nonempty_core_has_zero_character_mass():
    assert r.empty_core_quotient((3, 2, 1), 2) is None
    assert r.column_probability((3, 2, 1), 2, 3) == 0
    assert r.assemble_quotient(((), (), ())) == ()
    assert r.empty_core_quotient((), 3) == ((), (), ())


def test_involution_formula_agrees_with_existing_exact_arithmetic():
    for n in range(2, 19, 2):
        for shape in integer_partitions(n):
            assert r.column_probability(shape, 2, n//2) == Q(
                fixed_point_free_character(shape)**2, 2**(n//2)*factorial(n//2))


def test_qct_class_basis_sampling_is_not_hsp_weak_fourier_sampling():
    qct, hsp = [], []
    for shape in integer_partitions(4):
        d = hook_length_dimension(shape)
        chi = symmetric_character(shape, (2, 2))
        qct.append(r.column_probability(shape, 2, 2))
        hsp.append(Q(d*(d+chi), factorial(4)))
    assert sum(qct) == sum(hsp) == 1
    assert sum(abs(a-b) for a, b in zip(qct, hsp))/2 == Q(1, 4)


def test_coherent_class_superposition_is_not_a_mixture_of_column_laws():
    qct = np.array([[1, 1], [1, -1]])/np.sqrt(2)
    plus = np.array([1, 1])/np.sqrt(2)
    coherent = abs(qct@plus)**2
    mixture = np.sum(abs(qct)**2, axis=1)/2
    np.testing.assert_allclose(coherent, [1, 0], atol=1e-15)
    np.testing.assert_allclose(mixture, [0.5, 0.5], atol=1e-15)
    assert np.sum(abs(coherent-mixture))/2 > 0.49


def test_mixed_cycle_types_have_signed_cancellations_not_positive_quotient_counts():
    def unsigned(shape, cycles):
        if not cycles:
            return int(not shape)
        return sum(unsigned(smaller, cycles[1:]) for smaller, _ in rim_hook_removals(shape, cycles[0]))

    assert unsigned((2, 2), (2, 1, 1)) == 2
    assert symmetric_character((2, 2), (2, 1, 1)) == 0


def test_large_sampler_does_not_enumerate_partitions_group_or_characters(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("scalable sampler invoked an enumerative control")

    monkeypatch.setattr(r, "symmetric_character", forbidden)
    monkeypatch.setattr(r, "integer_partitions", forbidden)
    monkeypatch.setattr(r, "column_probability", forbidden)
    for k, m in ((2, 2048), (3, 1365), (17, 241)):
        shape = r.sample(k, m, random.Random(940+k))
        assert sum(shape) == k*m
        assert r.empty_core_quotient(shape, k) is not None


@pytest.mark.parametrize("call", [
    lambda: r.sample(True, 3, random.Random()),
    lambda: r.sample(2, 0, random.Random()),
    lambda: r.rsk_shape((1, 1)),
    lambda: r.rsk_shape([1, 2]),
    lambda: r.assemble_quotient(((1, 2), ())),
    lambda: r.assemble_quotient(()),
    lambda: r.empty_core_quotient((2, 1), 0),
    lambda: r.column_probability((2, 1), 2, 2),
    lambda: r.colored_permutation_shape((0, 0), (0, 1), 2),
    lambda: r.colored_permutation_shape((0, 1), (0, 2), 2),
    lambda: r.exact_column_controls(21),
])
def test_invalid_inputs_fail_closed(call):
    with pytest.raises(ValueError):
        call()


def test_native_artifact_replays_without_enumerative_reference():
    if not r.REPORT.exists():
        pytest.skip("live report not yet generated")
    report = json.loads(r.REPORT.read_text())
    for row in report["native"]:
        k, m = row["cycle_length"], row["cycle_count"]
        rng = random.Random(row["seed"])
        shapes = [r.sample(k, m, rng) for _ in range(row["sample_count"])]
        assert shapes == [tuple(shape) for shape in row["samples"]]
        mass = r.column_probability(shapes[0], k, m)
        assert Q(int(row["first_sample_mass_numerator_hex"], 16),
                 int(row["first_sample_mass_denominator_hex"], 16)) == mass
        assert row["all_sizes_and_empty_cores_verified"]
        assert not row["rejection_postselection_used"]
        assert row["conjugacy_class_size_bits"] > 15000
    assert not report["quantum_algorithm_executed"]
    assert not report["new_algorithm_claimed"]
