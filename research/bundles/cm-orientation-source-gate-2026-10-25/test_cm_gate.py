from itertools import permutations

import pytest

import cm_gate as c


@pytest.mark.parametrize("prime,order,planes", [(3, 8, 2), (5, 24, 2), (7, 64, 0), (17, 256, 4)])
def test_independent_quotient_algebra_enumeration(prime, order, planes):
    result = c.exhaustive_cm8(prime)
    assert result["norm_one_order"] == order
    assert result["projective_weak_classes"] == order // 2
    assert len(c.etale_counts(prime, c.cm8_permutation(prime))["horizontal_planes"]) == planes
    assert result["geometric_input_verified"] is False


def test_all_rational_cm_torus_types():
    valid = []
    for permutation in permutations(range(4)):
        try:
            valid.append(c.etale_counts(101, permutation))
        except ValueError:
            pass
    assert len(valid) == 8
    assert {x["norm_one_order"] for x in valid} == {100**2, 100*102, 102**2, 101**2-1, 101**2+1}
    assert sorted(len(x["horizontal_planes"]) for x in valid) == [0, 0, 0, 0, 0, 2, 2, 4]


def test_nonscalar_ambiguity_preserves_complete_local_orientation_and_pairing():
    for prime in (3, 5, 7, 17, 2**127-1):
        x = (0, 1, 0, 0)
        one = (1, 0, 0, 0)
        assert c.mul8(x, c.bar8(x, prime), prime) == one
        for basis in ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)):
            assert c.mul8(x, basis, prime) == c.mul8(basis, x, prime)
        assert any(x[i] for i in range(1, 4))  # Not a scalar weak mask.


def test_large_prime_count_is_symbolic_not_enumerated():
    prime = 2**127-1
    assert c.etale_counts(prime, c.cm8_permutation(prime))["norm_one_order"] == (prime+1)**2
    assert c.exhaustive_cm8(prime)["status"] == "NOT_RUN_CAP"
    assert c.exhaustive_cm8(prime)["elements_checked"] == 0


def test_independent_random_completion_bound():
    levels = [(r, c.cm8_permutation(r)) for r in (17, 41, 73)]
    result = c.independent_completion_bound(5, levels)
    assert result["local_tuple_count"] == 128*800*2592
    assert result["conditional_probability_upper"] == "1/11059200"
    assert result["applies_to_honest_evaluations"] is False
    assert result["classical_hardness_established"] is False


@pytest.mark.parametrize("value", [2, 9, -3, 5.0, True])
def test_bad_primes_rejected(value):
    with pytest.raises(ValueError):
        c.etale_counts(value, (0, 1, 2, 3))


@pytest.mark.parametrize("permutation", [(0, 0, 2, 3), (1, 0, 2, 3), (0, 1, 2), (False, 1, 2, 3)])
def test_incompatible_frobenius_rejected(permutation):
    with pytest.raises(ValueError):
        c.etale_counts(5, permutation)


@pytest.mark.parametrize("primes", [(5,), (17, 17)])
def test_nonindependent_levels_rejected(primes):
    with pytest.raises(ValueError):
        c.independent_completion_bound(5, [(r, c.cm8_permutation(r)) for r in primes])


def test_empty_levels_do_not_claim_exclusion():
    assert c.independent_completion_bound(5, [])["conditional_probability_upper"] == "1"
