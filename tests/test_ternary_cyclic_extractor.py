from collections import Counter
from fractions import Fraction
from itertools import product
import random

import numpy as np
import pytest

from ternary_cyclic_extractor import (
    apply_cycle_basis, conditional_source_census, curvatures, cycle_forward,
    cycle_inverse, cyclic_output, cyclic_recipe, dense_source_control,
    kernel_relation, random_even_source, recycle_supports, throughput_ledger,
    zero_sum_support,
)


@pytest.mark.parametrize("n", [1, 2, 4, 8, 16, 32])
def test_known_SDE_primitive_is_guaranteed_zero_sum_at_scaling_dimensions(n):
    rng, m = random.Random(92300+n), (n+1)**2
    vectors = [tuple(rng.randrange(3) for _ in range(n)) for _ in range(m)]
    certificate = zero_sum_support(vectors)
    support = certificate["support"]
    assert support and len(set(support)) == len(support)
    assert all(sum(vectors[i][j] for i in support) % 3 == 0 for j in range(n))
    assert certificate["Gaussian_kernel_calls"] <= n+2
    for record in certificate["inner_relations"]:
        first, second = record["first_support"], record["second_support"]
        assert not set(first).intersection(second)
        assert all(sum(vectors[i][j] for i in first) % 3 == sum(vectors[i][j] for i in second) % 3 for j in range(n))


def test_entire_one_dimensional_curvature_space_and_all_three_collision_cases():
    cases = set()
    for vectors in product(range(3), repeat=4):
        result = zero_sum_support([(x,) for x in vectors])
        cases.add(result["case"])
        assert sum(vectors[i] for i in result["support"]) % 3 == 0
    assert cases == {"inner_zero", "outer_zero", "three_equal_disjoint_sums"}


def test_four_disjoint_equal_sum_sets_give_three_cycle_without_solving_a_pointed_inverse():
    record = zero_sum_support([(1,)]*4)
    assert record["case"] == "three_equal_disjoint_sums"
    assert len(record["support"]) == 3
    assert len({i for support in record["four_disjoint_equal_sum_supports"] for i in support}) == 4


@pytest.mark.parametrize("mask", [(1,), (0, 1, 0), (0, 1, 1, 1), (1, 0, 1, 0, 1)])
def test_cyclic_coordinate_change_is_a_bijection_on_every_word_with_untouched_inactive_wires(mask):
    outputs = set()
    for word in product(range(3), repeat=len(mask)):
        transformed = cycle_forward(mask, word)
        assert cycle_inverse(mask, transformed) == word
        assert all(transformed[i] == word[i] for i, x in enumerate(mask) if not x)
        outputs.add(transformed)
    assert len(outputs) == 3**len(mask)
    assert len(cyclic_recipe(mask)["gates"]) == sum(mask)-1
    assert cyclic_recipe(mask)["acceptance_probability"] == "1"


def test_gate_recipe_replays_arbitrary_inputs_not_only_the_known_native_family():
    mask, rng = (0, 1, 1, 1), np.random.default_rng(92291)
    state = rng.normal(size=81)+1j*rng.normal(size=81)
    state /= np.linalg.norm(state)
    actual = apply_cycle_basis(state, mask)
    expected = np.zeros_like(state)
    words = list(product(range(3), repeat=4)); index = {w: i for i, w in enumerate(words)}
    for word in words:
        expected[index[cycle_forward(mask, word)]] = state[index[word]]
    assert np.max(abs(actual-expected)) < 1e-12 and abs(np.linalg.norm(actual)-1) < 1e-12


@pytest.mark.parametrize("n,level", [(1, 8), (2, 8)])
def test_all_native_full_root_gate_branches_are_exact_odd_qutrits_with_unit_acceptance(n, level):
    record = dense_source_control(n, level, 88700+n)
    expected = Fraction(1, 3**(record["active_inputs"]-1))
    assert sum(c["probability"] for c in record["all_active_complement_branches"]) == pytest.approx(1)
    for branch in record["all_active_complement_branches"]:
        output = branch["output"]
        assert branch["probability"] == pytest.approx(float(expected))
        assert output["original_modulus"] == output["output_modulus"] == str(3**(level//2))
        assert output["output_odd_level"] == level-1
        assert not output["field_shadow_replacement"]
        assert output["pivot_phase_can_be_dropped_in_coherent_pointer_mode"] is False
    assert record["maximum_gate_amplitude_error"] < 1e-12


def test_conditional_all_curvatures_all_pointers_and_full_q9_high_lifts_have_uniform_odd_law():
    census = conditional_source_census()
    assert census["curvature_strata"] == 81
    assert census["all_active_pointer_strata"] > 81
    assert census["frequency_pairs_evaluated"] == 27*census["all_active_pointer_strata"]
    assert census["multiplicity_per_pair"] == 1
    assert census["output_low_first_frequency_uniform_including_zero"]


def test_recycling_uses_disjoint_supports_and_charges_retained_inputs_without_false_IID_claims():
    source = random_even_source(4, 16, 100, 88794)
    result = recycle_supports(curvatures(source))
    used = set()
    for child in result["outputs"]:
        support = set(child["support"])
        assert not used.intersection(support)
        used.update(support)
        assert all(sum(curvatures(source)[i][j] for i in support) % 3 == 0 for j in range(4))
    assert not used.intersection(result["retained_original_registers"])
    assert len(used)+len(result["retained_original_registers"]) == 100
    assert result["output_count"] >= 100//25
    assert not result["retained_curvature_labels_claimed_IID"]


def test_joint_child_law_from_two_recycled_disjoint_supports_is_exactly_IID_conditional_on_curvatures():
    vectors = [(1,)]*8
    recycled = recycle_supports(vectors)
    supports = [child["support"] for child in recycled["outputs"]]
    assert len(supports) == 2
    counts = Counter()
    # Vary two disjoint pivot sites' tangent+high values; other parent values fixed.
    for values in product(range(3), repeat=6):
        parents = [(0, 1)]*8
        for k, support in enumerate(supports):
            a, ha, hc = values[3*k:3*k+3]
            parents[support[0]] = (a+3*ha, (1-a) % 3+3*hc)
        output_pairs = []
        for support in supports:
            F = [sum(0 if j == 0 else parents[i][j-1] for i in support) % 9 for j in range(3)]
            output_pairs.append(((F[1]-F[0]) % 9, (F[2]-F[0]) % 9))
        counts[tuple(output_pairs)] += 1
    allowed = [(a, c) for a, c in product(range(9), repeat=2) if (c-2*a) % 3 == 0]
    assert set(counts) == set(product(allowed, repeat=2)) and set(counts.values()) == {1}


def test_wrong_curvature_support_is_not_assigned_a_native_odd_promise():
    source = random_even_source(1, 8, 4, 88701)
    invalid = next(i for i, v in enumerate(curvatures(source)) if any(v))
    with pytest.raises(ValueError, match="do not sum to zero"):
        cyclic_output(source, tuple(int(i == invalid) for i in range(4)), (0,)*4)


def test_single_output_root_recursion_is_still_exponential_even_with_recycling_and_no_failures():
    for n, r in ((1, 8), (2, 8), (8, 32), (32, 128)):
        ledger = throughput_ledger(n, r)
        assert ledger["minimum_one_output_protocol_original_copies"] == str((n+1)**(r-1))
        assert ledger["fresh_batch_protocol_copies_for_one_final_field_qutrit"] == str((n+1)**(3*(r-1)))
        assert ledger["inactive_register_recycling_is_included_in_lower_bound"]
        assert ledger["coherent_pointer_or_multi_output_phase_transducers_excluded_from_lower_bound"]
        assert not ledger["polynomial_in_r_complete_speedup_claim_allowed"]


@pytest.mark.parametrize("vectors", [[], [(0,), (0,)], [(True,)]*4, [(0, 1), (0,)]] )
def test_bad_support_inputs_fail_closed(vectors):
    with pytest.raises(ValueError): zero_sum_support(vectors)


def test_kernel_witness_does_not_use_a_zero_trivial_assignment():
    result = kernel_relation([(1, 0), (0, 1), (1, 1)])
    assert result == (2, 2, 1)
    assert all(sum(c*v[j] for c, v in zip(result, [(1, 0), (0, 1), (1, 1)])) % 3 == 0 for j in range(2))
