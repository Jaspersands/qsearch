from fractions import Fraction
import itertools
import math

import numpy as np
import pytest

from coset_source_orbit_contraction import (
    _permutation_ranks, matching_centralizer_orbits,
    source_orbit_character_data, audit_streamed_source_orbits,
)
from coset_binary_carrier_instruments import (
    _source_parity_group_data, _coarse_source_factors, _source_category_projectors,
    coarse_source_joint_laws, corrected_weight_laws, source_count_weight_controls,
)


def test_lehmer_ranks_match_independent_lexicographic_enumeration():
    for n in (2, 4, 6):
        group = np.array(list(itertools.permutations(range(n))))
        assert np.array_equal(_permutation_ranks(group), np.arange(math.factorial(n)))
        shuffled = group[np.arange(len(group)-1, -1, -1)]
        assert np.array_equal(_permutation_ranks(shuffled), np.arange(len(group)-1, -1, -1))


@pytest.mark.parametrize("n,count", ((4, 8), (6, 34), (8, 182)))
def test_centralizer_orbits_partition_every_group_element_with_exact_mass(n, count):
    group, generators, orbits = matching_centralizer_orbits(n)
    assert len(orbits) == count
    assert sorted(j for orbit in orbits for j in orbit) == list(range(math.factorial(n)))
    assert len(generators) == n-1
    h = tuple(j ^ 1 for j in range(n))
    for s in generators:
        assert tuple(s[h[s[j]]] for j in range(n)) == h
    centralizer_order = 2**(n//2)*math.factorial(n//2)
    assert all(centralizer_order % len(orbit) == 0 for orbit in orbits)
    assert all(group[orbit[0]] == min(group[j] for j in orbit) for orbit in orbits)


@pytest.mark.parametrize("bad", (True, 3, 5, 10, 8.0))
def test_unbounded_or_invalid_orbit_inputs_are_rejected(bad):
    with pytest.raises(ValueError):
        matching_centralizer_orbits(bad)


def test_orbit_contraction_matches_all_exact_full_pair_spectra_not_just_probabilities():
    audit = audit_streamed_source_orbits()
    assert audit["verified"]
    assert [r["streamed_pairs"] for r in audit["controls"]] == [192, 24480]
    assert all(r["all_signed_spectra_and_remainders_identical"] for r in audit["controls"])
    assert not audit["extends_to_growing_degree_algorithm"]


def test_only_simultaneous_hidden_preserving_conjugation_is_a_valid_reduction():
    data = _source_parity_group_data(4, 2)
    _, _, projectors, phases = _source_category_projectors(data, "phase_sign")
    factors = _coarse_source_factors(data, projectors, phases, 0)
    group, generators, _ = matching_centralizer_orbits(4)
    index = {g: j for j, g in enumerate(group)}
    for s in generators:
        perm = np.array([index[tuple(s[g[s[j]]] for j in range(4))] for g in group])
        assert np.array_equal(factors[:, perm[:, None], perm[None, :]], factors)
    h, other_h = (translated[0] for translated in data[8][:2])
    # These first endpoints are conjugate in S4 but not in C(h).
    assert not np.array_equal(factors[:, h, 0], factors[:, other_h, 0])


def test_s8_streamed_certificate_does_not_allocate_a_full_pair_matrix():
    metadata, spectra, mixtures, tails, priors, weight = source_orbit_character_data(8)
    assert metadata["enumerated_group_pairs"] == 7338240
    assert metadata["full_group_pairs_represented"] == 1625702400
    assert metadata["maximum_product_index_block_entries"] == 40320
    assert not metadata["full_pair_matrix_allocated"]
    assert not metadata["is_polynomial_in_degree"]
    assert metadata["int64_accumulation_range_verified"]
    assert metadata["exact_character_row_orthogonality_verified"]
    assert metadata["independent_two_quotient_characters_checked"] == 22
    assert any(w < 0 for spectrum in spectra for _, w in spectrum)
    assert all(sum(p) == 1 for p in priors)
    assert Fraction(weight["exact_amplitude_overlap"]) <= Fraction(1, 105)


def test_s8_joint_laws_preserve_source_and_independent_weight_marginals():
    metadata, _, _, _, priors, _ = source_orbit_character_data(8)
    for k in (2, 7, 12, 16):
        laws, mixtures, errors = coarse_source_joint_laws(8, 4, k)
        expected_weights = corrected_weight_laws(8, 4, k)[0]
        for b in (0, 1):
            assert sum(laws[b].values()) == sum(mixtures[b].values()) == 1
            observed_weights = [Fraction() for _ in range(k+1)]
            for histogram, mass in laws[b].items():
                observed_weights[sum(histogram[1::2])] += mass
            assert tuple(observed_weights) == expected_weights[b]
            assert sum(abs(laws[b][key]-mixtures[b][key]) for key in laws[b])/2 <= errors[b]
    assert metadata["same_hidden_member_in_every_copy"]


@pytest.mark.parametrize("kind", ("irrep", "character_sign", "invented"))
def test_s8_does_not_silently_substitute_sign_categories_for_requested_irreps(kind):
    with pytest.raises(ValueError):
        coarse_source_joint_laws(8, 4, 2, kind)


def test_s8_baseline_coverage_is_explicit_not_an_unimplemented_optimum():
    rows = source_count_weight_controls(8, 4, (2, 4, 7))["copy_sweep"]
    assert rows[0]["full_pair_likelihood_baseline"] is not None
    assert rows[1]["full_pair_likelihood_baseline"] is not None
    assert rows[2]["full_pair_likelihood_baseline"] is None
    assert rows[2]["complete_paired_table_beats_full_pair_likelihood"] is None
    assert all(not r["ideal_table_is_compiled_classifier"] for r in rows)


def test_intermediate_probe_fails_its_baseline_without_claiming_an_all_source_no_go():
    from coset_source_orbit_contraction import intermediate_copy_information_controls
    rows = intermediate_copy_information_controls()
    for row in rows:
        assert row["ideal_paired_table_loses_to_pair_count"]
        assert Fraction(row["exact_information_loss_lower_bound"]) > 0
        assert not row["raw_support_measurement_is_implemented"]
        assert not row["all_source_irrep_information_retained"]
        assert not row["growing_degree_or_all_copy_no_go"]
    last = rows[-1]
    assert Fraction(last["raw_trace_distance_lower_bound"]) == 1-Fraction(105, 65536)
    assert last["paired_category_walsh_distance"] == pytest.approx(.11952000153653906)
    assert last["pair_event_count_distance"] == pytest.approx(.15025463718219184)
