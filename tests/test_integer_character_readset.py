from fractions import Fraction as Q
import hashlib
import itertools
import json
from pathlib import Path

import pytest

from theorems import integer_character_babai as babai
from theorems import integer_character_near_vector as near
from theorems import integer_character_readset as readset


@pytest.mark.parametrize("order", [2, 4, 6, 10, 18, 100])
def test_exact_even_grid_moment(order):
    empirical = sum((Q(k, order)**2 for k in range(-order//2, order//2)), Q(0))/order
    assert readset.uniform_residue_mean(order) == empirical
    assert empirical >= Q(1, 12)


@pytest.mark.parametrize("order", [1, 3, 19, 2.0, True])
def test_unsupported_moduli_fail_closed(order):
    with pytest.raises(ValueError, match="even integer"):
        readset.uniform_residue_mean(order)


def test_actual_blind_factory_probability_is_bounded_with_nonunit_labels():
    labels = [1, 0, 1, 0, 1]
    actual = readset.exact_control_probability(2, labels, [0], lambda c: [c[0]], Q(0))
    bound = readset.readset_bound(5, 4, 2, 1, Q(0))
    assert actual == Q(1, 16)
    assert actual <= Q(bound["success_probability_upper"]) < 1
    assert not bound["information_flow_automatically_verified"]
    assert bound["bound_depends_on_input_dependence_not_computation_model"]
    assert not bound["unrestricted_classical_lower_bound"]


def test_adaptation_and_correlated_centers_defeat_misapplied_bound():
    controls = readset.scope_counterexamples()
    adaptive = controls["adaptive_one_visited_candidate"]
    assert Q(adaptive["actual_success"]) == 1
    assert Q(adaptive["incorrect_blind_list_bound"]) == Q(2, 3)
    assert Q(adaptive["bound_charging_that_pool"]) == 1
    correlated = controls["uniform_marginals_but_correlated_centers"]
    assert Q(correlated["actual_success"]) == Q(1, 2)
    assert Q(correlated["incorrect_independence_bound"]) == Q(1, 32)


def test_uniform_constant_certificate_and_dyadic_block_argument():
    certificate = readset.uniform_certificate()
    assert Q(certificate["exponent_rate_lower"]) == Q(289, 42750) > Q(1, 150)
    assert Q(certificate["asymptotic_read_fraction_necessary_for_polynomial_pools"]) == Q(11, 50)
    for h in range(201):
        assert 64+4*h <= Q(200, 3)*(h+1) <= Q(200, 3)*2**h
    for m in [20000, 39999, 40000, 80000]:
        r = (19*m+19)//20
        bound = readset.readset_bound(m, r, 2*3**100, m**4)
        assert Q(bound["hoeffding_exponent"]) > Q(m, 150)
        assert Q(bound["success_probability_upper"]) <= Q(1, 2**(m//300))
    assert not certificate["native_lll_profile_scales_as_assumed"]
    assert not certificate["kernel_checked"]


def test_vacuous_cases_caps_and_invalid_dimensions():
    assert readset.readset_bound(100, 0, 18, 65)["success_probability_upper"] == "1"
    assert readset.readset_bound(100, 100, 18, 65, Q(1, 4))["success_probability_upper"] == "1"
    capped = readset.readset_bound(100000, 100000, 2, 1, Q(0))
    assert capped["dyadic_exponent_used"] == 4096
    assert Q(capped["success_probability_upper"]) == Q(1, 2**4096) > 0
    for args in [(0, 0, 18, 1), (3, 4, 18, 1), (3, -1, 18, 1), (3, 1, 18, 0)]:
        with pytest.raises(ValueError):
            readset.readset_bound(*args)
    with pytest.raises(ValueError):
        readset.readset_bound(3, 1, 18, 1, .065)
    with pytest.raises(ValueError, match="state cap"):
        readset.exact_control_probability(2, [1]*20, [], lambda _: [0], Q(0))


@pytest.mark.parametrize("eliminate_first_coordinate", [False, True])
def test_actual_branch_factory_ignores_prefix_centers_but_scores_do_not(eliminate_first_coordinate):
    labels, order = [1, 5, 3, 7], 21
    _, base = near.lattice_bases(labels, order)
    if eliminate_first_coordinate:
        rows = [[21, 0, 0, 0], base[3],
                [(pow(5, -1, order)*a) % order for a in labels], base[2]]
        blind = [0, 3]
    else:
        rows = [base[3], base[1], base[0], base[2]]
        blind = [3, 1]
    assignments, scores = [], []
    for values in itertools.product([0, 7, 20], repeat=2):
        target = [4, 5, 6, 7]
        for i, value in zip(blind, values):
            target[i] = value
        exact = babai.exact_normalized_babai(rows, labels, order, target)
        search = babai.bounded_last_plane_search(rows, labels, order, target, exact, radius=3)
        assignments.append(tuple(t["assignment_decimal"] for t in search["trials"]))
        scores.append(tuple(t["mean_square"] for t in search["trials"]))
    assert len(set(assignments)) == 1
    assert len(set(scores)) > 1


def test_native_report_retains_falsifier_without_an_asymptotic_claim():
    saved = json.loads(readset.REPORT.read_text())
    assert saved["producer_sha256"] == hashlib.sha256(Path(readset.__file__).read_bytes()).hexdigest()
    replay = readset.native_report()
    assert replay == saved
    native = saved["native"]
    assert len(native["blind_coordinate_indices"]) == 834
    assert len(native["read_coordinate_indices"]) == 190
    assert set(native["blind_coordinate_indices"]).isdisjoint(native["read_coordinate_indices"])
    assert set(native["blind_coordinate_indices"]+native["read_coordinate_indices"]) == set(range(1024))
    assert native["conditional_random_center_bound"]["success_probability_upper"] == "1"
    assert not native["bound_informative_at_native_parameters"]
    assert not native["bound_is_a_probability_for_this_fixed_seed"]
    assert native["frozen_witness_threshold_met"]
    assert Q(native["verified_frozen_witness_mean_square"]) < Q(13, 200)
