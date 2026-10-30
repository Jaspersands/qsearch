from itertools import product
from math import gcd, prod
from pathlib import Path
import sys

import pytest
from sympy import Matrix, eye, zeros

sys.path.insert(0, str(Path(__file__).resolve().parent))
from native_membership import (
    MembershipPlan, content_depth, embed_local, filter_transcript, local_direction,
    prefix_queries, recover_local_data,
)
from controls_membership import (
    different_column_masks_counterexample, false_interpolant_control,
    masked_action_control, membership_incidence_control, negative_graph_control,
    smith_contains, supplied_map_control,
)
from controls_double import full_split_fixture
from kernel_output import action, mod, odd_maximal_order


@pytest.mark.parametrize("q,e,a", [(2, 1, 0), (2, 3, 0), (2, 4, 1), (3, 2, 0),
                                    (3, 3, 1), (5, 1, 0)])
def test_exhaustive_projective_prefix_equivalence(q, e, a):
    depth, modulus = e-2*a, q**(e-2*a)
    lines = [(x, 1) for x in range(modulus)]+[(1, y) for y in range(0, modulus, q)]
    for true, proposed in product(lines, repeat=2):
        for digits in range(1, depth+1):
            answers = [smith_contains(query, q, e, a, true)
                       for query in prefix_queries(proposed, q, e, depth, digits)]
            correct = (true[0]*proposed[1]-true[1]*proposed[0]) % q**digits == 0
            assert all(answers) == correct


def test_upper_unipotent_alone_has_false_prefix_positive():
    upper, projector = prefix_queries((1, 0), 3, 2, 2, 2)
    assert smith_contains(upper, 3, 2, 0, (1, 3))
    assert not smith_contains(projector, 3, 2, 0, (1, 3))
    assert projector.det() == 0


@pytest.mark.parametrize("q,e,a,v", [(2, 8, 1, (1, 6)), (3, 5, 1, (4, 1)),
                                      (5, 4, 2, (1, 5)), (7, 2, 0, (1, 7))])
def test_content_and_two_chart_direction(q, e, a, v):
    membership = lambda query: smith_contains(query, q, e, a, v)
    content = content_depth(q, e, membership)
    assert content["content_exponent"] == a
    assert content["membership_calls"] == 2*(e+1)
    if content["depth"]:
        result = local_direction(q, e, content["depth"], membership)
        x, y = result["vector"]
        assert (x*v[1]-y*v[0]) % q**content["depth"] == 0
        assert result["membership_calls"] == 2*(q*content["depth"]+1)


@pytest.mark.parametrize("phi,factors", [([1, 1, 0, 0], ((2, 1),)),
    ([1, 2, 0, 0], ((5, 1),)), ([3, 4, 0, 0], ((5, 2),)),
    ([-2, 14, 0, 0], ((2, 3), (5, 2))), ([6, 0, 0, 0], ((2, 2), (3, 2))),
    ([3, 2, 0, 0], ((13, 1),))])
def test_supplied_map_integrality_matches_containment_and_original_ideal(phi, factors):
    result = supplied_map_control(phi, factors)
    assert result["original_principal_ideal_verified"]
    assert result["maximum_observed_norm"] <= result["uniform_norm_bound"]
    assert not result["native_interpolation_executed"]
    assert not result["unknown_native_kernel_recovered"]
    if phi != [6, 0, 0, 0]:
        assert result["negative_probes"] > 0
        assert result["noncoprime_norm_probes"] > 0
    else:
        assert result["recovery"]["directions"] == {}


@pytest.mark.parametrize("n,factors", [(2, ((2, 1),)), (9, ((3, 2),)),
                                      (200, ((2, 3), (5, 2)))])
def test_public_lifts_and_one_uniform_transcript(n, factors):
    order = odd_maximal_order(11)
    split = full_split_fixture(11, n, factors)
    plan = MembershipPlan.create(order, split, n, factors, 11)
    original = plan.primes
    for query in (eye(2), zeros(2), Matrix([[0, 1], [0, 0]]), Matrix([[1, 2], [3, 4]])):
        record = plan.probe(query)
        alpha, norm, m = record["alpha"], record["norm"], record["torsion_level"]
        assert mod(action(alpha, split)-query, n) == zeros(2)
        assert mod(alpha-order.unit, 11) == zeros(4, 1)
        assert norm % 11 == 1 and 0 < norm <= plan.norm_bound
        assert max(abs(int(x)) for x in alpha) <= n*11
        assert plan.primes == original
        assert set(record["primes"]) <= set(original)
        assert gcd(m, norm*n*11) == 1 and m > norm and m*m > 8*n*n*norm
        assert prod(r for r in original if norm % r == 0) <= norm
    assert gcd(plan.probe(zeros(2))["norm"], n) > 1


def test_dyadic_primary_embedding_is_at_full_original_precision():
    query = Matrix([[1, 2], [0, 0]])
    result = embed_local(query, 2, 3, 200, ((2, 3), (5, 2)))
    assert mod(result-query, 8) == zeros(2)
    assert mod(result-eye(2), 25) == zeros(2)
    with pytest.raises(ValueError, match="original factorization"):
        embed_local(query, 2, 1, 200, ((2, 3), (5, 2)))


@pytest.mark.parametrize("bad", [(3, 3, 5), (2, 3, 5), (3, 5, 11), (3, 5, 9), (3, 5)])
def test_malformed_or_insufficient_transcripts_rejected(bad):
    with pytest.raises(ValueError):
        filter_transcript(bad, 2, 11, 1, 100)


@pytest.mark.parametrize("norm", [0, -1, 101, 11, True])
def test_bad_norm_rejected(norm):
    with pytest.raises(ValueError):
        filter_transcript((3, 5, 7, 13, 17), 2, 11, norm, 100)


@pytest.mark.parametrize("p", [2, 3, 4, 5])
def test_bad_characteristic_rejected(p):
    with pytest.raises(ValueError):
        MembershipPlan.create(odd_maximal_order(11), (), 5, ((5, 1),), p)


@pytest.mark.parametrize("mask", [1, 2, 3, 6])
def test_shared_mask_cancels_even_on_negative_membership(mask):
    record = masked_action_control([1, 1, 0, 0], [0, 0, 1, 0], mask=mask)
    assert not record["integral"]


def test_negative_case_has_valid_full_isotropic_graph():
    record = negative_graph_control()
    assert not record["integral"] and not record["interpolator_executed"]
    assert all(x["isotropic"] and x["rank"] == 8 for x in record["local_graphs"])


def test_columnwise_masks_do_not_cancel_despite_pairing_check():
    record = different_column_masks_counterexample()
    assert record["actual"] != record["incorrect"]
    assert record["determinant_check_still_passes"]


def test_published_uniqueness_bound_alone_permits_false_membership():
    record = false_interpolant_control()
    assert record["paper_uniqueness_bound_passes"]
    assert record["membership_would_be_false_positive_without_stronger_bound"]


def test_budgets_reject_before_any_oracle_queries():
    def forbidden(query):
        pytest.fail("budget must be checked before the first callback")
    with pytest.raises(ValueError, match="budget"):
        local_direction(65537, 1, 1, forbidden)
    with pytest.raises(ValueError, match="budget"):
        recover_local_data(65537, ((65537, 1),), forbidden)


@pytest.mark.parametrize("answer", [1, None, "yes"])
def test_nonboolean_responses_rejected(answer):
    with pytest.raises(ValueError, match="boolean"):
        content_depth(2, 1, lambda _: answer)


def test_inconsistent_membership_rejected():
    with pytest.raises(ValueError, match="unique"):
        local_direction(2, 1, 1, lambda _: True)
    answers = iter([True, False, True, True, True, True])
    with pytest.raises(ValueError, match="nonmonotone"):
        content_depth(2, 2, lambda _: next(answers))
    answers = iter([False, False, True, True, False, False, True, True])
    with pytest.raises(ValueError, match="parities"):
        content_depth(2, 3, lambda _: next(answers))


@pytest.mark.parametrize("q", [2, 3, 5, 7])
def test_boolean_membership_queries_select_at_most_two_directions(q):
    record = membership_incidence_control(q)
    assert sum(record["nonscalar_fixed_line_histogram"].values())+q == q**4


@pytest.mark.parametrize("q", [2, 3, 5, 7])
def test_each_direction_has_a_unique_unipotent_membership_probe(q):
    lines = [(x, 1) for x in range(q)]+[(1, 0)]
    for proposed in lines:
        upper, _ = prefix_queries(proposed, q, 1, 1, 1)
        assert [v for v in lines if smith_contains(upper, q, 1, 0, v)] == [proposed]
