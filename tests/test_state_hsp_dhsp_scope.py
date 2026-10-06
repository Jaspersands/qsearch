from fractions import Fraction
import json

import numpy as np
import pytest

from state_hsp_dhsp_scope import geometry, graph_control, run_controls, weak_distribution


def exact(row):
    return Fraction(int(row["numerator"]), int(row["denominator"]))


@pytest.fixture(scope="module")
def report():
    return run_controls()


def test_every_declared_shift_has_graph_symmetry_exactly_the_reflection_subgroup(report):
    assert len(report["graph_controls"]) == 54
    for r in report["graph_controls"]:
        H = r["hidden_reflection_subgroup_indices"]
        for g, overlap in enumerate(r["graph_representation_overlaps"]):
            assert overlap == pytest.approx(int(g in H))
        assert r["minimum_asymmetry_gap"] == 1
        assert r["graph_state_norm"] == pytest.approx(1)


def test_coherent_preparation_and_inverse_are_available_not_a_missing_resource(report):
    for r in report["graph_controls"]:
        assert r["executed_A_inverse_return_probability"] == pytest.approx(1)
        assert r["unknown_oracle_calls_for_A"] == r["unknown_oracle_calls_for_A_inverse"] == 1
        assert not r["coherent_access_lacking_is_the_blocker"]
        assert not r["abelian_theorem_applies_to_full_group"]


def test_normal_core_and_rotation_restriction_cannot_identify_any_reflection_shift(report):
    for r in report["graph_controls"]:
        assert r["normal_core_indices"] == [0]
        assert r["rotation_restriction_stabilizer"] == [0]
        assert not r["normal_core_output_recovers_shift"]
    for N in (3, 4, 5, 6, 8, 12, 16):
        rows = [r for r in report["graph_controls"] if r["rotation_order"] == N]
        assert {r["hidden_shift_calibration"] for r in rows} == set(range(N))


def test_full_subgroup_enumeration_gives_baer_center_not_rotation_subgroup(report):
    from sympy import divisor_count, divisors
    for r in report["graph_controls"]:
        N = r["rotation_order"]
        assert r["all_subgroup_count"] == int(divisor_count(N)+sum(divisors(N)))
        assert r["baer_norm_indices"] == r["center_indices"]
        assert len(r["center_indices"]) == (1 if N % 2 else 2)
        assert r["baer_and_center_index"] == (2*N if N % 2 else N)
        assert r["rotation_subgroup_index"] == 2


def test_exponential_index_premises_cannot_be_replaced_by_index_two_abelian_subgroup(report):
    for r in report["exponential_order_ledgers"]:
        assert int(r["center_and_baer_index"]) == 2**r["rotation_order_bits"]
        assert r["rotation_subgroup_index"] == 2
        assert not r["poly_near_hamiltonian_family"]
        assert not r["poly_near_abelian_family"]


def test_weak_fourier_character_probabilities_are_physical_and_normalized(report):
    for r in report["graph_controls"]:
        probabilities = r["weak_irrep_probabilities"]
        assert sum(exact(p) for p in probabilities.values()) == 1
        for key, value in probabilities.items():
            assert float(exact(value)) == pytest.approx(r["executed_character_probabilities"][key])


@pytest.mark.parametrize("N", [3, 5, 7, 9])
def test_odd_rotation_orders_have_zero_shift_information_in_irrep_labels(N):
    assert all(weak_distribution(N, s) == weak_distribution(N, 0) for s in range(N))


@pytest.mark.parametrize("N", [4, 6, 8, 12, 16])
def test_even_rotation_orders_have_only_rare_parity_information_in_irrep_labels(N):
    from math import log2
    distributions = [weak_distribution(N, s) for s in range(N)]
    mean = {k: sum(d[k] for d in distributions)/N for k in distributions[0]}
    information = sum(float(p)/N*log2(float(p/mean[k]))
                      for d in distributions for k, p in d.items() if p)
    assert information == pytest.approx(1/N)
    total_variation = sum(abs(distributions[0][k]-distributions[1][k]) for k in mean)/2
    assert total_variation == Fraction(1, N)
    assert all(distributions[s] == distributions[s % 2] for s in range(N))


def test_graph_and_reduced_coset_state_have_same_overlap_with_right_representation():
    r, N = graph_control(8, 3), 8
    g = geometry(N)
    labels = r["source_labels"]
    rho = np.array([[int(labels[i] == labels[j])/(2*N) for j in range(2*N)] for i in range(2*N)])
    assert np.trace(rho) == pytest.approx(1)
    assert np.linalg.eigvalsh(rho).min() > -1e-14
    for h, element in enumerate(g["elements"]):
        perm = [g["index"][a*element**-1] for a in g["elements"]]
        R = np.zeros_like(rho)
        R[perm, np.arange(2*N)] = 1
        assert np.trace(R @ rho) == pytest.approx(r["graph_representation_overlaps"][h])


def test_irrep_probabilities_do_not_exclude_hidden_information_in_quantum_blocks(report):
    assert not any(report["claim_gate"].values())
    json.loads(json.dumps(report, allow_nan=False))
    for r in report["graph_controls"]:
        assert not r["irreducible_quantum_blocks_declared_uninformative"]


@pytest.mark.parametrize("callback", [lambda: geometry(2), lambda: geometry(33),
    lambda: graph_control(4, 4), lambda: graph_control(4, -1),
    lambda: weak_distribution(True, 0), lambda: weak_distribution(4, 4)])
def test_out_of_scope_or_invalid_instances_are_rejected(callback):
    with pytest.raises(ValueError):
        callback()
