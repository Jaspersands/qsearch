"""Independent arithmetic, projective counting and source-access falsifiers."""

from collections import Counter
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path

import pytest

from theorems.jacobi_surface_reconstruction import (
    ARTIFACT, Cyclotomic, ReferenceCharacters, classical_lll_attempt,
    identify_root_turns, large_public_ideal_control, lift_surface_residue,
    native_surface_count, primary_normalize, public_ideal_basis,
    public_surface_attempt, run_controls, surface_bound, valuation_profile,
)


def brute_projective(p, d):
    # Unique representative: first nonzero homogeneous coordinate is one.
    count = 0
    for first in range(4):
        for suffix in itertools.product(range(p), repeat=3 - first):
            point = (0,) * first + (1,) + suffix
            count += (sum(pow(x, d, p) for x in point[:3]) - pow(point[3], d, p)) % p == 0
    return count


@pytest.mark.parametrize("p,d", [(7, 3), (13, 4), (11, 5)])
def test_polynomial_convolution_matches_direct_projective_charts(p, d):
    assert native_surface_count(p, d)["point_count"] == brute_projective(p, d)


@pytest.mark.parametrize("p,d,abc", [(11, 5, (1, 1, 1)), (13, 4, (1, 3, 3)), (7, 3, (1, 2, 2))])
def test_jacobi_recursion_against_full_three_variable_definition(p, d, abc):
    source = ReferenceCharacters(p, d)
    hist = [0] * d
    for x, y in itertools.product(range(1, p), repeat=2):
        z = (1 - x - y) % p
        if z:
            hist[sum(a * source.indices[v] for a, v in zip(abc, (x, y, z))) % d] += 1
    assert source.triple(abc) == source.field.reduce(hist)
    assert source.field.multiply(source.triple(abc), source.field.conjugate(source.triple(abc))) == source.field.constant(p * p)


def test_trivial_partial_product_keeps_the_zero_convolution_mass():
    source = ReferenceCharacters(13, 4)
    assert source.triple((1, 3, 3)) == source.field.constant(-13)


def test_positive_and_inverse_embeddings_are_not_interchanged():
    source = ReferenceCharacters(11, 5)
    profile = dict(valuation_profile((1, 1, 1), 5))
    assert profile[1] == 2 and profile[4] == 0
    value = source.triple((1, 1, 1))
    raw = source.field.evaluate_mod(value, source.teichmuller_root(1, 3), 11 ** 3)
    assert raw % 11 ** 2 == 0 and raw % 11 ** 3 != 0
    assert source.field.evaluate_mod(value, source.teichmuller_root(4, 1), 11) != 0


def test_local_unit_division_requires_the_lost_digits():
    source = ReferenceCharacters(11, 5)
    result = source.reference_local_unit((1, 1, 1), 1, 2)
    assert result["valuation"] == 2
    assert result["required_input_precision"] == 4
    assert result["unit_residue"] % 11 != 0
    assert not result["compact_division_implemented"]
    with pytest.raises(ValueError):
        pow(11, -1, 11 ** 2)
    # Reducing mod p^2 first loses every unit-part digit when v=2.
    value = source.triple((1, 1, 1))
    assert source.field.evaluate_mod(value, source.teichmuller_root(1, 2), 11 ** 2) == 0


@pytest.mark.parametrize("d", [3, 5, 7, 8, 9, 12])
def test_complete_admissible_triple_count_and_galois_norm_profiles(d):
    tuples = [a for a in itertools.product(range(1, d), repeat=3) if sum(a) % d]
    assert len(tuples) == surface_bound(d)
    for abc in tuples:
        profile = dict(valuation_profile(abc, d))
        assert sum(profile.values()) == len(profile)
        assert all(0 <= v <= 2 and v + profile[d - t] == 2 for t, v in profile.items())


@pytest.mark.parametrize("p,d", [(13, 3), (61, 4), (131, 5)])
def test_unique_prime_square_reconstruction_uses_a_proved_interval(p, d):
    count = native_surface_count(p, d)["point_count"]
    correction = count - (p * p + p + 1)
    assert p > 2 * surface_bound(d)
    record = lift_surface_residue(p, d, correction % (p * p))
    assert record["point_count"] == count
    assert record["correction"] == correction


def test_small_p_cannot_be_silently_rounded_from_a_prime_square():
    record = lift_surface_residue(13, 12, 0)
    assert record["status"] == "AMBIGUOUS_USE_SMALL_PRIME_CLASSICAL_BRANCH"
    assert record["lift_count"] > 1
    with pytest.raises(ValueError, match="no lift"):
        lift_surface_residue(101, 3, 101 ** 2 // 2)


def test_same_ideal_is_not_the_relative_norm_condition():
    source = ReferenceCharacters(11, 5)
    f = source.field
    jacobi = source.triple((1, 1, 1))
    unit = f.add(f.constant(1), f.root(1))
    inverse = f.scale(f.add(f.root(1), f.root(3)), -1)
    assert f.multiply(unit, inverse) == f.constant(1)
    wrong = f.multiply(jacobi, unit)
    # Same principal ideal, but not the required all-embedding normalization.
    for t, v in valuation_profile((1, 1, 1), 5):
        if v:
            assert f.evaluate_mod(wrong, source.teichmuller_root(t, v), 11 ** v) == 0
    assert f.multiply(wrong, f.conjugate(wrong)) != f.constant(121)
    with pytest.raises(ValueError, match="norm-normalized"):
        primary_normalize(f, wrong, 11)


def test_primary_congruence_fixes_every_root_without_truth_or_phase():
    for p, d in ((13, 3), (11, 5), (29, 7)):
        source = ReferenceCharacters(p, d)
        f = source.field
        value = source.triple((1, 1, 2) if d == 3 else (1, 1, 1))
        assert sum(value) % d == 1 and sum(j * c for j, c in enumerate(value)) % d == 0
        for k in range(f.roots_of_unity_order):
            rotated = f.multiply(f.unit_root(k), value)
            assert primary_normalize(f, rotated, p) == value
    with pytest.raises(ValueError, match="prime conductors"):
        primary_normalize(Cyclotomic(4), (1, 0), 13)


def test_full_root_group_is_twice_an_odd_conductor_and_all_entries_are_exact():
    f = Cyclotomic(5)
    assert f.roots_of_unity_order == 10
    assert f.unit_root(5) == f.constant(-1)
    assert f.multiply(f.unit_root(-3), f.unit_root(3)) == f.constant(1)
    assert all(type(c) is int for c in f.unit_root(-3))


def test_circular_phase_interval_rejects_ambiguous_rounding():
    for w in (6, 8, 10, 14):
        for k in range(w):
            assert identify_root_turns(Fraction(k, w) - Fraction(1, 16 * w) + 2,
                                       Fraction(1, 8 * w), w) == k
    with pytest.raises(ValueError):
        identify_root_turns(Fraction(1, 20), Fraction(1, 100), 10)
    with pytest.raises(ValueError):
        identify_root_turns(Fraction(0), Fraction(1, 20), 10)


def replay_public_certificate(source, record):
    """Independent verifier: no LLL and no reference Jacobi sums are called."""
    p, d, f = source.p, source.d, source.field
    assert record["status"] == "CLASSICAL_PUBLIC_IDEAL_RECONSTRUCTION_COMPLETED"
    expected = Counter(tuple(sorted(a)) for a in itertools.product(range(1, d), repeat=3) if sum(a) % d)
    actual = {tuple(t["characters"]): t["multiplicity"] for t in record["triples"]}
    assert actual == expected and len(actual) == len(record["triples"])
    for profile in record["profiles"]:
        value = profile["primary_normalized_coefficients"]
        assert [v for _, v in valuation_profile(profile["representative_triple"], d)] == profile["valuation_profile"]
        matrix, index = public_ideal_basis(source, profile["representative_triple"])
        assert abs(int(matrix.det())) == index == p ** f.degree
        assert f.multiply(value, f.conjugate(value)) == f.constant(p * p)
        assert sum(value) % d == 1 and sum(j * c for j, c in enumerate(value)) % d == 0
        for t, exponent in valuation_profile(profile["representative_triple"], d):
            if exponent:
                assert f.evaluate_mod(value, source.teichmuller_root(t, exponent), p ** exponent) == 0
        assert profile["lll_attempt"]["lattice_index"] == str(index)
    total = f.constant(0)
    for triple in record["triples"]:
        profile = record["profiles"][triple["profile_index"]]
        assert [v for _, v in valuation_profile(triple["characters"], d)] == profile["valuation_profile"]
        total = f.add(total, f.scale(profile["primary_normalized_coefficients"], triple["multiplicity"]))
    assert total[1:] == (0,) * (f.degree - 1)
    assert abs(total[0]) <= p * surface_bound(d)
    assert record["point_count"] == p * p + p + 1 + total[0]


def test_large_public_reconstruction_has_no_hidden_exhaustive_or_phase_source(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("true sum or character table accessed by public reconstruction")

    monkeypatch.setattr(ReferenceCharacters, "pair", forbidden)
    monkeypatch.setattr(ReferenceCharacters, "triple", forbidden)
    monkeypatch.setattr(ReferenceCharacters, "indices", property(forbidden))
    record = large_public_ideal_control()
    assert not record["character_table_materialized"]
    source = ReferenceCharacters(record["prime"], record["conductor"], residue_root=record["residue_root"])
    replay_public_certificate(source, record["classical_phase_free_surface_attempt"])
    assert record["classical_phase_free_surface_attempt"]["point_count"] == 5316911983139663865501362488876572959


def test_failed_lll_rows_are_unknown_not_a_quantum_advantage(monkeypatch):
    import theorems.jacobi_surface_reconstruction as module

    monkeypatch.setattr(module, "classical_lll_attempt", lambda source, abc: {"row_attempts": []})
    result = public_surface_attempt(ReferenceCharacters(11, 5))
    assert result["status"] == "NO_BALANCED_LLL_ROW_UNKNOWN"
    assert result["point_count"] is None and result["failure_is_not_hardness"]


@pytest.mark.parametrize("p,d", [(13, 3), (131, 5), (379, 7)])
def test_classical_full_reconstruction_matches_an_independent_count(p, d):
    source = ReferenceCharacters(p, d)
    result = public_surface_attempt(source)
    assert source._indices is None
    replay_public_certificate(source, result)
    assert result["point_count"] == native_surface_count(p, d)["point_count"]
    if d == 3:
        assert result["point_count"] == p * p + 7 * p + 1


@pytest.mark.parametrize("p,d", [(15, 7), (13, 5), (7, 0), (7, 1), (True, 3)])
def test_invalid_input_is_not_a_scientific_candidate(p, d):
    with pytest.raises(ValueError):
        ReferenceCharacters(p, d)


def test_live_artifact_replay_and_explicit_unimplemented_quantum_dependencies():
    report = json.loads(ARTIFACT.read_text())
    assert report == run_controls()
    source = Path(__file__).resolve().parents[1] / "theorems/jacobi_surface_reconstruction.py"
    assert report["source_sha256"] == hashlib.sha256(source.read_bytes()).hexdigest()
    assert not report["new_quantum_algorithm_claimed"]
    assert len(report["controls"]) == 14
    assert sum(len(c["triple_records"]) for c in report["controls"]) == 1032
    assert all(not c["quantum_PIP_unit_or_phase_subroutine_executed"] for c in report["controls"])
