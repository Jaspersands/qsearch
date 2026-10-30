"""Finite callable-input controls; no source promises inferred from samples."""
from fractions import Fraction
from itertools import product
import random
from types import SimpleNamespace

import pytest

from theorems import partition_source_attack as attack
from theorems.ut5_matrix_phase_alignment import _basis


def learn(f, *, p=3, n=2, R=3, delta=Fraction(1, 3), seed=7, **kwargs):
    plan = attack.PartitionSourcePlan(p, n, R, delta, kwargs.pop("error", Fraction(1, 3)))
    return attack.recover_partition_symmetry(plan, f, rng=random.Random(seed), **kwargs)


@pytest.mark.parametrize("p", [2, 3, 5])
def test_projection_cosets_and_scrambled_unhashable_labels(p):
    def projection(x):
        return (x[0] + 2 * x[1] + x[2]) % p

    labels = [["scrambled", (7 * j + 3) % (p + 7), {"j": j}] for j in range(p)]
    original = [repr(label) for label in labels]
    plain = learn(projection, p=p, n=3, R=p, delta=Fraction(1, p))
    scrambled = learn(lambda x: labels[projection(x)], p=p, n=3, R=p,
                      delta=Fraction(1, p))
    assert plain == scrambled
    assert plain["status"] == "SUCCESS"
    assert plain["quotient_size"] == p
    assert len(plain["collision_basis"]) == 2
    assert all(projection(row) == 0 for row in plain["collision_basis"])
    assert plain["translation_basis"] == tuple(map(tuple, _basis(
        [[1, 0, 0], [0, 1, 0], [0, 0, 1]], p)))
    assert plain["phase_basis"] == ((1, 2 % p, 1),)
    assert plain["pauli_generators"][-1] == (0, 0, 0, 1, 2 % p, 1)
    assert not plain["source_promises_certified"]
    assert not plain["caps"]["source_promises_certified"]
    assert [repr(label) for label in labels] == original


@pytest.mark.parametrize("p", [2, 3, 2**127 - 1])
def test_constant_uses_only_one_quotient_representative(p):
    row = learn(lambda x: None, p=p, n=4, R=1, delta=Fraction(1))
    assert row["status"] == "SUCCESS"
    assert row["quotient_size"] == 1
    assert row["phase_basis"] == ()
    assert len(row["translation_basis"]) == 4
    assert row["counts"]["representatives_tested"] == 1
    assert row["counts"]["peak_collision_rows"] == 4


def test_small_injective_source_returns_full_noncommuting_pauli_group():
    row = learn(tuple, R=9, delta=Fraction(1))
    assert row["status"] == "SUCCESS"
    assert row["collision_basis"] == ()
    assert row["quotient_size"] == 9
    assert len(row["pauli_generators"]) == 4
    assert row["counts"]["representatives_accepted"] == 9


@pytest.mark.parametrize("n,R,gap,evaluator,d_basis,t_basis,z_basis,accepted", [
    (2, 6, Fraction(2, 27), lambda x: (x[1], 0 if x[1] == 0 else x[0]),
     ((1, 0),), ((1, 0),), ((0, 1),), 1),
    (3, 17, Fraction(2, 81), lambda x: (x[2], x[1], 0 if x[1] == 0 else x[0]),
     ((1, 0, 0),), ((1, 0, 0), (0, 0, 1)), ((0, 1, 0), (0, 0, 1)), 3),
    (3, 12, Fraction(1, 27),
     lambda x: (0, x[1]) if x[2] == 0 else (1, x[0]) if x[2] == 1 else (2, x[0], x[1]),
     ((1, 0, 0), (0, 1, 0)), ((1, 0, 0), (0, 1, 0)), ((0, 0, 1),), 1),
])
def test_nonuniform_partition_fixtures(n, R, gap, evaluator, d_basis, t_basis, z_basis, accepted):
    row = learn(evaluator, n=n, R=R, delta=gap)
    assert row["status"] == "SUCCESS"
    assert row["collision_basis"] == d_basis
    assert row["translation_basis"] == t_basis
    assert row["phase_basis"] == z_basis
    assert row["pauli_generators"] == (tuple(t + (0,) * n for t in t_basis)
                                        + tuple((0,) * n + z for z in z_basis))
    caps, counts = row["caps"], row["counts"]
    assert counts["representatives_tested"] == row["quotient_size"] <= R
    assert counts["representatives_accepted"] == accepted
    assert counts["verification_pairs"] < row["quotient_size"] * caps["verification_pairs_per_representative"]
    assert counts["queries"] == 2 * counts["collision_pairs"] + 4 * counts["verification_pairs"]
    assert counts["queries"] <= caps["query_bound"]
    assert counts["field_draws"] == 2 * n * (counts["collision_pairs"] + counts["verification_pairs"])
    assert counts["random_bits"] <= caps["random_bit_cap"]
    assert counts["peak_collision_rows"] <= n
    assert not row["source_promises_certified"]


def test_wrong_R_aborts_before_quotient_enumeration(monkeypatch):
    def forbidden(*args):
        pytest.fail("quotient enumeration before cap check")

    monkeypatch.setattr(attack, "_quotient_representatives", forbidden)
    row = learn(tuple, R=1, delta=Fraction(1))
    assert row["status"] == "ABORT_QUOTIENT_CAP"
    assert row["quotient_size"] == 9
    assert row["counts"]["queries"] == 2 * row["caps"]["collision_pair_cap"]
    assert row["counts"]["representatives_tested"] == 0
    assert row["pauli_generators"] == ()


def test_rejection_cap_charges_bits_and_never_queries_source():
    row = attack.recover_partition_symmetry(
        attack.PartitionSourcePlan(3, 2, 1, Fraction(1)),
        lambda x: pytest.fail("unexpected source query"),
        rng=SimpleNamespace(getrandbits=lambda k: (1 << k) - 1))
    assert row["status"] == "ABORT_RANDOMNESS_CAP"
    assert row["counts"]["queries"] == row["counts"]["field_draws"] == 0
    assert row["counts"]["random_bit_calls"] == row["caps"]["field_rejection_attempt_cap"]
    assert row["counts"]["random_bits"] == 2 * row["counts"]["random_bit_calls"]
    assert row["pauli_generators"] == ()


@pytest.mark.parametrize("cap", [0, 1, 11, 194])
def test_optional_query_cap_never_overruns(cap):
    calls = []
    row = learn(lambda x: calls.append(x), R=1, delta=Fraction(1), query_cap=cap)
    assert row["status"] == "ABORT_QUERY_CAP"
    assert row["counts"]["queries"] == len(calls) == cap
    assert row["pauli_generators"] == ()


def test_exact_query_cap_allows_completion():
    caps = attack.PartitionSourcePlan(3, 2, 1, Fraction(1)).caps()
    row = learn(lambda x: 0, R=1, delta=Fraction(1), query_cap=caps["query_bound"])
    assert row["status"] == "SUCCESS"
    assert row["counts"]["queries"] == caps["query_bound"]


def test_randomness_abort_in_verification_discards_partial_generators():
    plan = attack.PartitionSourcePlan(3, 1, 1, Fraction(1))
    caps = plan.caps()
    draws = 0

    def bits(k):
        nonlocal draws
        draws += 1
        return draws % 2 if draws <= 2 * caps["collision_pair_cap"] else 3

    row = attack.recover_partition_symmetry(plan, lambda x: 0,
                                            rng=SimpleNamespace(getrandbits=bits))
    assert row["status"] == "ABORT_RANDOMNESS_CAP"
    assert row["collision_basis"] == ((1,),)
    assert row["quotient_size"] == 1
    assert row["counts"]["representatives_tested"] == 1
    assert row["counts"]["verification_pairs"] == 0
    assert row["counts"]["queries"] == 2 * caps["collision_pair_cap"]
    assert row["translation_basis"] == row["phase_basis"] == row["pauli_generators"] == ()


def test_exact_public_clocks_and_actual_counters():
    calls, widths = [], []
    rng = random.Random(21)

    def bits(k):
        widths.append(k)
        return rng.getrandbits(k)

    row = attack.recover_partition_symmetry(
        attack.PartitionSourcePlan(3, 2, 1, Fraction(2, 3), Fraction(1, 7)),
        lambda x: calls.append(x), rng=SimpleNamespace(getrandbits=bits))
    caps, counts = row["caps"], row["counts"]
    assert row["status"] == "SUCCESS"
    assert caps["beta"] == Fraction(1, 21)
    assert caps["collision_pair_cap"] == 168
    assert caps["verification_pairs_per_representative"] == 4
    assert caps["field_draw_cap"] == 688
    assert caps["field_rejection_attempt_cap"] == 14
    assert counts["queries"] == len(calls) == caps["query_bound"] == 352
    assert counts["random_bits"] == sum(widths) <= caps["random_bit_cap"]
    assert counts["random_bit_calls"] == len(widths)
    assert counts["field_draws"] == caps["field_draw_cap"]
    assert counts["verification_pairs"] == 4
    assert counts["peak_collision_rows"] <= 2
    assert caps["randomness_abort_bound"] <= caps["beta"]
    assert all(type(x) is tuple and len(x) == 2 and all(0 <= a < 3 for a in x)
               for x in calls)


def test_nonpivot_complement_representatives_are_distinct_modulo_span():
    rows = _basis([[1, 1, 0], [0, 0, 1]], 3)
    reps = tuple(attack._quotient_representatives(3, 3, [1], 3))
    assert reps == ((0, 0, 0), (0, 1, 0), (0, 2, 0))
    for a, b in product(reps, repeat=2):
        if a != b:
            assert len(_basis(rows + [[(x-y) % 3 for x, y in zip(a, b)]], 3)) == 3


def test_default_rng_does_not_change_global_random_state(monkeypatch):
    state = random.getstate()
    created = []

    def system_random():
        created.append(True)
        return random.Random(12)

    monkeypatch.setattr(attack, "SystemRandom", system_random)
    row = attack.recover_partition_symmetry(
        attack.PartitionSourcePlan(3, 2, 1, Fraction(1)), lambda x: 0)
    assert row["status"] == "SUCCESS"
    assert created == [True]
    assert random.getstate() == state


@pytest.mark.parametrize("change", [
    {"prime": True}, {"prime": 9}, {"width": 0},
    {"inverse_purity": True}, {"inverse_purity": 0},
    {"gap": 0.5}, {"gap": Fraction(0)}, {"gap": Fraction(2)},
    {"error": 0.1}, {"error": Fraction(1)}, {"query_cap": -1},
    {"rng": 7},
])
def test_invalid_contract_rejected_before_queries(change):
    args = dict(prime=3, width=2, inverse_purity=1, gap=Fraction(1))
    options = {key: value for key, value in change.items() if key in ("query_cap", "rng")}
    args.update({key: value for key, value in change.items() if key not in options})
    with pytest.raises(ValueError):
        attack.recover_partition_symmetry(attack.PartitionSourcePlan(**args),
                                          lambda x: pytest.fail("unexpected query"), **options)


@pytest.mark.parametrize("value", [-1, 4, True, 1.5])
def test_malformed_bit_source_is_not_silently_reduced(value):
    with pytest.raises(ValueError, match="invalid bit string"):
        attack.recover_partition_symmetry(
            attack.PartitionSourcePlan(3, 1, 1, Fraction(1)), lambda x: 0,
            rng=SimpleNamespace(getrandbits=lambda k: value))
