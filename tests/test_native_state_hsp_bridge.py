from collections import Counter
from itertools import product

import numpy as np
import pytest

from cyclotomic_rescaling_gate import multiply, plus, reduce_element
from native_state_hsp_bridge import NativeGroup, class_ceiling, ring_words, run_controls
from vector_centre_state_hsp_receiver import VectorExtension


@pytest.fixture(scope="module")
def report():
    return run_controls()


@pytest.mark.parametrize("level", [1, 2, 3, 4])
@pytest.mark.parametrize("dimension", [1, 2])
def test_known_induced_actions_are_linear_and_native_states_have_the_claimed_hidden_group(level, dimension):
    G = NativeGroup(level, dimension)
    labels = [((1, 0),)*dimension, ((0, 1),)*dimension, ((2, 1),)*dimension]
    gs = [(((0, 0),)*dimension, 0), (((1, 0),)*dimension, 1), (((0, 1),)*dimension, 2)]
    secret = ((2, 1),)*dimension
    for label in labels:
        psi = G.supplied_phase_state(label, secret)
        for h in G.hidden_elements(secret):
            assert np.allclose(G.induced_action(label, h) @ psi, psi)
        for g, h in product(gs, repeat=2):
            assert np.allclose(G.induced_action(label, g) @ G.induced_action(label, h), G.induced_action(label, G.compose(g, h)))
    H = G.hidden_elements(secret)
    assert set(G.compose(g, h) for g, h in product(H, repeat=2)) == set(H)


@pytest.mark.parametrize("n", [1, 2, 8])
def test_level_two_has_the_exact_public_vector_bilinear_chart(n):
    G = NativeGroup(2, n)
    matrices = []
    for j in range(n):
        B = [[0]*(n+1) for _ in range(n+1)]
        B[-1][j] = 1
        matrices.append(B)
    V = VectorExtension(matrices)
    gs = [(((1, 0),)*n, 1), (((2, 1),)*n, 2), (((0, 1),)*n, 0)]
    for g, h in product(gs, repeat=2):
        assert G.class_two_coordinates(G.compose(g, h)) == V.multiply(G.class_two_coordinates(g), G.class_two_coordinates(h))
    with pytest.raises(ValueError, match="only at native level2"):
        NativeGroup(4).class_two_coordinates((((1, 0),), 1))


def test_every_original_source_overlap_is_exactly_the_hidden_subgroup_indicator(report):
    assert len(report["exact_original_source_controls"]) == 12
    for c in report["exact_original_source_controls"]:
        assert c["every_group_element_checked"] == 3**(c["level"]+1)
        assert len(c["exact_original_Bose_subgroup"]) == 3
        assert c["original_absolute_overlap_gap"] == "1"
        assert c["maximum_literal_matrix_error"] < 2e-11
        assert not c["full_coherent_graph_state_or_unknown_inverse_used"]
        assert not c["known_representation_depends_on_hidden_secret"]
        assert not c["bounded_matrix_replay_is_scalable_receiver"]


@pytest.mark.parametrize("r", [2, 3, 4, 5, 6])
@pytest.mark.parametrize("c", [1, 2, 3])
def test_integer_secret_fibre_ceiling_matches_the_actual_ramified_embedding(r, c):
    q = 3**((r+1)//2)
    projected = Counter(reduce_element((s, 0), min(r, c)) for s in range(q))
    L = class_ceiling(r, 1, c)
    size = L["integer_embedded_secret_fibre_count"]
    assert set(projected.values()) == {size["base"]**size["exponent"]}
    assert len(projected) == 3**L["maximum_integer_secret_trits_retained_per_coordinate"]
    assert not L["bound_applies_to_arbitrary_quantum_state_conversions"]


@pytest.mark.parametrize("r", [2, 3, 4])
def test_successive_rotation_commutators_reach_every_lower_central_ideal_layer(r):
    # [(0,1),(a,0)] = ((zeta-1)*a,0), checked against explicit multiplication.
    G = NativeGroup(r)
    identity = (((0, 0),), 0)
    rotation, rotation_inverse = (((0, 0),), 1), (((0, 0),), 2)
    values = ring_words(r)
    layer = set(values)
    for depth in range(1, r+1):
        derived = set()
        for a in layer:
            translation, inverse = ((a,), 0), ((reduce_element((-a[0], -a[1]), r),), 0)
            comm = G.compose(G.compose(G.compose(rotation, translation), rotation_inverse), inverse)
            assert comm == ((multiply((-1, 1), a, r),), 0)
            derived.add(comm[0][0])
        assert len(derived) == 3**max(r-depth, 0)
        layer = derived
    assert layer == {(0, 0)}
    assert identity == G.hidden_elements(((0, 0),))[0]


def test_group_projection_loses_precision_but_native_quantum_states_do_not_all_lose_it(report):
    c = report["homomorphic_projection_loss_countercontrol"]
    assert c["integer_secrets"] == [0, 3]
    assert c["same_projected_secret"]
    assert c["conditional_phase_state_fidelity"] == pytest.approx(1/3)
    assert not c["quantum_sample_information_destroyed_by_ALL_transformations"]
    assert not report["growing_native_nilpotency_class_handled"]
    assert not report["new_native_receiver_or_classical_speedup_supplied"]


def test_large_transfer_ledgers_keep_exponential_counts_symbolic_and_exact(report):
    for L in report["growing_class_transfer_ledgers"]:
        bound = L["integer_embedded_secret_fibre_count"]
        assert bound == {"base": 3, "exponent": L["native_dimension"]*(L["integer_secret_trits_per_coordinate"]-L["maximum_integer_secret_trits_retained_per_coordinate"])}
    assert report["growing_class_transfer_ledgers"][-1]["integer_embedded_secret_fibre_count"]["exponent"] == 128*63


def test_central_descent_preserves_the_exact_native_gap_but_not_polynomial_depth_cost(report):
    for c in report["exact_central_descent_controls"]:
        assert c["central_character_bucket_sizes"] == [3**(c["level"]-1)]*3
        assert c["every_group_element_checked"] == 3**(c["level"]+1)
        assert c["group_elements_in_hidden_subgroup_times_designated_centre"] == 9
        assert c["exact_quotient_Bose_gap_after_fresh_window_zero_sum"] == "1"
        assert c["maximum_literal_conditional_error"] < 2e-11
        assert c["quotient_group_is_abelian"] == (c["level"] == 2)
        assert not c["adaptive_recycled_outputs_claimed_IID"]
        assert not c["polynomial_growing_depth_copy_recurrence_proved"]
