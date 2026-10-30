"""Independent exhaustive controls for bounded exact Boolean field search."""
from collections import Counter
from fractions import Fraction
from itertools import combinations, product

import pytest

from theorems import regular_subset_sum as module


def _sum(columns, word, prime, rank):
    return tuple(sum(x * column[j] for x, column in zip(word, columns)) % prime
                 for j in range(rank))


def _span_size(columns, prime, rank):
    return len({_sum(columns, word, prime, rank)
                for word in product(range(prime), repeat=len(columns))})


def _verify(result, columns, prime, degree, prefix_count):
    assert result["status"] == "VERIFIED_REGULAR_SUBSET_WITNESS"
    scales = result["scales"]
    rank = len(columns[0])
    assert len(scales) == len(columns) and any(scales)
    assert all(type(s) is int and s in (0, 1) for s in scales)
    assert _sum(columns, [pow(s, degree, prime) for s in scales], prime, rank) == (0,) * rank
    jacobian = [tuple(degree * pow(s, degree - 1, prime) * x % prime for x in column)
                for s, column in zip(scales, columns) if s]
    assert _span_size(jacobian, prime, rank) == prime**rank
    assert result["jacobian_rank"] == rank and result["exact_verified"]
    assert not result["abort_is_unsatisfiability"]
    if rank:
        assert len(result["basis_indices"]) == rank
        assert all(i < prefix_count for i in result["basis_indices"])
        assert scales[:prefix_count] == [int(i in result["basis_indices"])
                                        for i in range(prefix_count)]


@pytest.mark.parametrize("prime,rank,width", [
    (3, 0, 3), (3, 1, 0), (3, 1, 1), (3, 1, 2), (3, 1, 3),
    (3, 2, 0), (3, 2, 1), (3, 2, 2), (3, 2, 3), (5, 1, 3), (5, 2, 2),
])
def test_every_small_suffix_and_target_matches_bruteforce(prime, rank, width):
    vectors = tuple(product(range(prime), repeat=rank))
    words = tuple(product((0, 1), repeat=width))
    for columns in product(vectors, repeat=width):
        reachable = {_sum(columns, word, prime, rank) for word in words}
        for target in vectors:
            result = module._subset_sum(columns, target, prime=prime, max_states=prime**rank)
            assert (result["mask"] is not None) == (target in reachable)
            assert result["states_visited"] == result["peak_states"] <= prime**rank
            assert result["transitions"] <= width * prime**rank
            assert result["columns_processed"] <= width
            assert not result["cap_truncated"]
            if result["mask"] is not None:
                assert 0 <= result["mask"] < 2**width
                word = [(result["mask"] >> i) & 1 for i in range(width)]
                assert _sum(columns, word, prime, rank) == target
            else:
                assert result["reason"] == "TARGET_NOT_FOUND"
                assert result["states_visited"] == len(reachable)
                assert result["columns_processed"] == width


@pytest.mark.parametrize("prime,rank,width", [
    (3, 0, 0), (3, 0, 3), (3, 1, 0), (3, 1, 1), (3, 1, 2), (3, 1, 3),
    (3, 2, 0), (3, 2, 1), (3, 2, 2), (3, 2, 3), (5, 1, 3), (5, 2, 2),
])
def test_exact_moments_over_all_small_random_matrices(prime, rank, width):
    # Enumerate the full uniform matrix ensemble, without using the DP.
    vectors = tuple(product(range(prime), repeat=rank))
    words = tuple(word for word in product((0, 1), repeat=width) if any(word))
    totals, squares, misses = Counter(), Counter(), Counter()
    matrix_count = 0
    for columns in product(vectors, repeat=width):
        counts = Counter(_sum(columns, word, prime, rank) for word in words)
        matrix_count += 1
        for target in vectors:
            hits = counts[target]
            totals[target] += hits
            squares[target] += hits * hits
            misses[target] += int(hits == 0)
    moments = module.subset_sum_moments(prime, rank, width)
    assert matrix_count == prime**(rank * width)
    assert moments["state_bound"] == prime**rank
    assert moments["nonzero_boolean_words"] == 2**width - 1
    assert moments["mu"] == Fraction(2**width - 1, prime**rank)
    assert moments["variance"] == moments["mu"] * (1 - Fraction(1, prime**rank))
    expected_bound = min(Fraction(1), 1 / moments["mu"]) if width else Fraction(1)
    assert moments["no_hit_upper"] == expected_bound
    for target in vectors:
        mean = Fraction(totals[target], matrix_count)
        variance = Fraction(squares[target], matrix_count) - mean * mean
        assert mean == moments["mu"]
        assert variance == moments["variance"]
        assert Fraction(misses[target], matrix_count) <= moments["no_hit_upper"]
    assert moments["iid_uniform_columns_required"]
    assert moments["target_independent_of_suffix_required"]
    assert not moments["iid_uniform_columns_verified"]
    assert not moments["state_cap_exhaustion_included"]


@pytest.mark.parametrize("prime,rank,width", [(3, 1, 3), (3, 2, 3), (5, 1, 3)])
def test_distinct_boolean_word_images_are_pairwise_uniform(prime, rank, width):
    vectors = tuple(product(range(prime), repeat=rank))
    words = tuple(word for word in product((0, 1), repeat=width) if any(word))
    pairs = tuple(combinations(range(len(words)), 2))
    joint = {pair: Counter() for pair in pairs}
    for columns in product(vectors, repeat=width):
        images = [_sum(columns, word, prime, rank) for word in words]
        for i, j in pairs:
            joint[i, j][images[i], images[j]] += 1
    expected = prime**(rank * (width - 2))
    for counts in joint.values():
        assert len(counts) == prime**(2 * rank)
        assert set(counts.values()) == {expected}


@pytest.mark.parametrize("prime", [3, 5, 7])
def test_witness_uses_the_original_degree_without_reduction(prime):
    columns = [(0, 0), (1, 1), (2, 2), (0, 1), (0, 0), (prime - 1, prime - 2)]
    for degree in range(1, prime):
        result = module.regular_subset_witness(columns, prime=prime, degree=degree, prefix_count=4)
        _verify(result, columns, prime, degree, 4)
        assert result["basis_indices"] == (1, 3)
        assert result["scales"] == [0, 1, 0, 1, 0, 1]
        assert result["degree"] == degree
        assert result["state_cap_met"] and result["max_states"] == prime**2


def test_all_small_prefixes_and_suffixes_have_exact_public_results():
    prime, rank = 3, 2
    vectors = tuple(product(range(prime), repeat=rank))
    for prefix in product(vectors, repeat=2):
        independent = _span_size(prefix, prime, rank) == prime**rank
        target = tuple(-x % prime for x in _sum(prefix, (1, 1), prime, rank))
        for suffix in product(vectors, repeat=2):
            columns = prefix + suffix
            result = module.regular_subset_witness(columns, prime=prime, degree=2, prefix_count=2)
            reachable = {_sum(suffix, word, prime, rank) for word in product((0, 1), repeat=2)}
            if independent and target in reachable:
                _verify(result, columns, prime, 2, 2)
            else:
                assert result["status"] == "ABORT" and result["scales"] is None
                expected = "TARGET_NOT_FOUND" if independent else "PREFIX_RANK_DEFICIENT"
                assert result["reason"] == expected


@pytest.mark.parametrize("columns,prefix_count", [
    ([(1, 0), (2, 0), (0, 1), (2, 2)], 2),
    ([(1,), (2,)], 0), ([(0,)] * 4, 3), ([(0, 0)] * 4, 4),
])
def test_deficient_prefix_is_not_repaired_from_the_suffix(columns, prefix_count):
    result = module.regular_subset_witness(columns, prime=3, degree=2, prefix_count=prefix_count)
    assert result["status"] == "ABORT" and result["scales"] is None
    assert result["reason"] == "PREFIX_RANK_DEFICIENT"
    assert result["states_visited"] == result["transitions"] == result["columns_processed"] == 0
    assert not result["zero_rank_branch"] and not result["abort_is_unsatisfiability"]


def test_snapshot_prevents_column_reuse_and_charges_collisions():
    columns = [(1,), (0,), (1,)]
    result = module.regular_subset_witness(columns, prime=5, degree=4, prefix_count=1)
    assert result["status"] == "ABORT" and result["reason"] == "TARGET_NOT_FOUND"
    assert result["states_visited"] == result["peak_states"] == 2
    assert result["transitions"] == result["columns_processed"] == 2
    assert result["scales"] is None
    repeated = [(1,)] * 5
    success = module.regular_subset_witness(repeated, prime=5, degree=4, prefix_count=1)
    _verify(success, repeated, 5, 4, 1)
    assert success["scales"] == [1] * 5
    assert success["suffix_mask"] == 15
    assert success["states_visited"] == 5 and success["transitions"] == 10


def test_exhausted_search_does_not_claim_arbitrary_sde_unsatisfiability():
    # The degree-one solution (1,4) exists, but no Boolean solution does.
    result = module.regular_subset_witness([(1,), (1,)], prime=5, degree=1, prefix_count=1)
    assert (1 + 4) % 5 == 0
    assert result["status"] == "ABORT" and result["scales"] is None
    assert result["reason"] == "TARGET_NOT_FOUND" and result["state_cap_met"]
    assert not result["abort_is_unsatisfiability"]
    # A discarded dependent prefix column cannot be reused as suffix.
    result = module.regular_subset_witness([(1,), (4,)], prime=5, degree=4, prefix_count=2)
    assert result["status"] == "ABORT" and result["basis_indices"] == (0,)
    assert result["columns_processed"] == 0 and result["states_visited"] == 1


def test_state_cap_aborts_without_a_partial_witness_or_extra_confidence():
    columns = [(1,), (1,), (3,)]
    capped = module.regular_subset_witness(columns, prime=5, degree=4, prefix_count=1, max_states=2)
    assert capped["status"] == "ABORT" and capped["reason"] == "STATE_CAP"
    assert capped["scales"] is None and capped["suffix_mask"] is None
    assert capped["cap_truncated"] and not capped["state_cap_met"]
    assert capped["states_visited"] == capped["peak_states"] == 2
    assert capped["transitions"] == capped["columns_processed"] == 2
    assert not capped["exact_verified"] and not capped["iid_uniform_columns_verified"]
    assert capped["arbitrary_fixed_bank_success_bound"] is None
    full = module.regular_subset_witness(columns, prime=5, degree=4, prefix_count=1)
    _verify(full, columns, 5, 4, 1)


@pytest.mark.parametrize("cap", [2, 5, 6])
def test_cap_coverage_is_separate_from_verified_early_success(cap):
    columns = [(1,), (4,), (3,)]
    result = module.regular_subset_witness(columns, prime=5, degree=4, prefix_count=1, max_states=cap)
    _verify(result, columns, 5, 4, 1)
    assert result["state_cap_met"] is (cap >= 5)
    assert not result["cap_truncated"]
    assert result["max_states"] == cap and result["peak_states"] == 2
    assert result["columns_processed"] == result["transitions"] == 1


def test_tiny_cap_counts_collisions_and_stops_before_inserting_target():
    result = module.regular_subset_witness([(1,), (0,), (4,)], prime=5, degree=4,
                                           prefix_count=1, max_states=1)
    assert result["reason"] == "STATE_CAP" and result["scales"] is None
    assert result["peak_states"] == 1 and result["transitions"] == 2
    assert result["columns_processed"] == 2
    no_growth = module.regular_subset_witness([(1,), (0,), (0,)], prime=5, degree=4,
                                              prefix_count=1, max_states=1)
    assert no_growth["reason"] == "TARGET_NOT_FOUND" and not no_growth["cap_truncated"]
    assert not no_growth["state_cap_met"] and no_growth["states_visited"] == 1


def test_default_cap_is_lazy_not_a_field_enumeration():
    rank, prime = 20, 5
    columns = [tuple(int(i == j) for j in range(rank)) for i in range(rank)]
    columns.append((4,) * rank)
    result = module.regular_subset_witness(columns, prime=prime, degree=4, prefix_count=rank)
    assert result["status"] == "VERIFIED_REGULAR_SUBSET_WITNESS"
    assert result["max_states"] == 5**20 and result["state_cap_met"]
    assert result["peak_states"] == 2 and result["transitions"] == 1
    assert result["scales"] == [1] * 21 and result["jacobian_rank"] == rank


@pytest.mark.parametrize("width", [1, 3])
def test_zero_dimension_requires_columns_but_no_search(width):
    columns = [()] * width
    for prefix_count in range(width + 1):
        result = module.regular_subset_witness(columns, prime=5, degree=4, prefix_count=prefix_count)
        _verify(result, columns, 5, 4, prefix_count)
        assert result["zero_rank_branch"] and result["scales"] == [1] + [0] * (width - 1)
        assert result["max_states"] == result["state_bound"] == 1
        assert result["state_cap_met"] and result["basis_indices"] == ()
        assert result["states_visited"] == result["peak_states"] == 0
        assert result["transitions"] == result["columns_processed"] == 0


@pytest.mark.parametrize("changes", [
    {"prime": True}, {"prime": 5.0}, {"prime": "5"}, {"prime": 2}, {"prime": 1},
    {"prime": 4}, {"prime": 9}, {"prime": 341}, {"prime": 561},
    {"degree": True}, {"degree": 1.0}, {"degree": 0}, {"degree": -1}, {"degree": 5},
    {"prefix_count": True}, {"prefix_count": 1.0}, {"prefix_count": -1}, {"prefix_count": 3},
    {"max_states": True}, {"max_states": 1.0}, {"max_states": 0}, {"max_states": -1},
    {"columns": []}, {"columns": ()}, {"columns": None}, {"columns": "14"},
    {"columns": {0: (1,), 1: (4,)}}, {"columns": iter([(1,), (4,)])},
    {"columns": [1, 4]}, {"columns": [(1,), ()]}, {"columns": [(), (1,)]},
    {"columns": [(True,), (4,)]}, {"columns": [(False,), (4,)]},
    {"columns": [(1.0,), (4,)]}, {"columns": [("1",), (4,)]},
    {"columns": [(-1,), (4,)]}, {"columns": [(5,), (4,)]},
    {"columns": [(1,), (False,)]}, {"columns": [(1,), (5,)]},
])
def test_strict_invalid_inputs(changes):
    args = dict(columns=[(1,), (4,)], prime=5, degree=4, prefix_count=1)
    args.update(changes)
    with pytest.raises(ValueError):
        module.regular_subset_witness(**args)


@pytest.mark.parametrize("changes", [
    {"prime": True}, {"prime": 5.0}, {"prime": 2}, {"prime": 9},
    {"rank": True}, {"rank": -1}, {"rank": 1.0},
    {"width": True}, {"width": -1}, {"width": 1.0},
])
def test_moments_validate_strictly(changes):
    args = dict(prime=5, rank=1, width=2)
    args.update(changes)
    with pytest.raises(ValueError):
        module.subset_sum_moments(**args)


def test_calls_are_deterministic_and_leave_input_unchanged():
    columns = [[0, 0], [1, 1], [0, 1], [0, 0], [4, 3], [4, 3]]
    original = [column[:] for column in columns]
    first = module.regular_subset_witness(columns, prime=5, degree=4, prefix_count=3)
    for _ in range(3):
        assert module.regular_subset_witness(columns, prime=5, degree=4, prefix_count=3) == first
    assert columns == original


def test_final_verification_rejects_corrupt_search_output(monkeypatch):
    original = module._subset_sum

    def corrupt(*args, **kwargs):
        result = original(*args, **kwargs)
        result["mask"] = 0
        return result

    monkeypatch.setattr(module, "_subset_sum", corrupt)
    with pytest.raises(ArithmeticError, match="verification failed"):
        module.regular_subset_witness([(1,), (4,)], prime=5, degree=4, prefix_count=1)
