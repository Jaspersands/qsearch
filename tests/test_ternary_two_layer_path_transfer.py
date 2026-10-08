from copy import deepcopy
from fractions import Fraction
import hashlib
from itertools import product
import json
import subprocess

import pytest
from sympy import Matrix
from sympy.matrices.normalforms import hermite_normal_form

from ternary_two_layer_path_transfer import (
    DERIVATION, REPORT, PATTERNS, complete_graph, evaluate, exact_circuit_census,
    exact_zero_pattern_counts, extend, family_envelopes, lattice_matrix,
    moment_numerator, pattern_columns, pattern_weight_numerator,
    structural_certificate, terminal_weights, zero_subset_invariants,
)


@pytest.fixture(scope="module")
def artifact():
    return json.loads(REPORT.read_text())


def test_complete_coordinate_alphabet_is_actual_one_hot_not_independent_phase_edges():
    assert len(PATTERNS) == 81
    for p in PATTERNS:
        C = pattern_columns(p)
        assert all(len(c) == 4 and any(c) for c in C)
        if len(C) == 2:
            assert all(a*b == 0 for a, b in zip(*C))


def test_all_integer_graph_transitions_are_full_column_hnf_closure():
    states, graph = complete_graph()
    assert len(states) == 137 and len(graph) == 137
    assert states[0] == ()
    assert len(set(states)) == len(states)
    for basis, row in zip(states, graph):
        assert len(row) == 81
        for p, j in zip(PATTERNS, row):
            columns = pattern_columns(p)
            joined = lattice_matrix(basis).row_join(lattice_matrix(columns))
            H = hermite_normal_form(joined)
            assert states[j] == tuple(tuple(int(H[i,k]) for i in range(4)) for k in range(H.cols))


@pytest.mark.parametrize("q", [3, 9])
def test_torsion_state_zero_patterns_match_entire_full_root_annihilator(q):
    words = tuple(tuple(int(i != j) for j in range(4)) for i in range(4))
    basis = ()
    for c in words:
        # Binary coordinate column represents trit1 rows and no trit2 rows.
        basis = extend(basis, c)
    B = lattice_matrix(basis)
    counts = [0]*16
    for nu in product(range(q), repeat=4):
        if all(sum(nu[i]*int(B[i,j]) for i in range(4)) % q == 0 for j in range(B.cols)):
            mask = sum(1 << i for i,v in enumerate(nu) if v == 0)
            counts[mask] += 1
    assert tuple(counts) == exact_zero_pattern_counts(basis,q)
    assert counts[0] == 2 and counts[15] == 1 and sum(counts) == 3
    eta, b = Fraction(2-q,q),Fraction(2,q)
    assert moment_numerator(basis,q,2,2) == ((eta**4+2*b**4)*q**4,0)


@pytest.mark.parametrize("angles", [(2,2,2,2),(1,1,3,1),(1,3,2,2)])
@pytest.mark.parametrize("q,M", [(3,2),(9,1)])
def test_direct_actual_quantum_circuit_census_agrees_with_signed_transfer(q,M,angles):
    c = exact_circuit_census(q,M,angles)
    predicted = evaluate(1,q,M,angles)
    assert c["actual_direct_circuit_uniform_mean_exact"] == predicted["uniform_full_target_population_success_exact"]
    assert Fraction(c["actual_direct_circuit_Born_mean_exact"]) <= Fraction(predicted["Born_weighted_population_success_upper"])


@pytest.mark.parametrize("angles", [(0,0,0,0),(0,1,0,3),(1,0,3,0)])
def test_zero_cost_or_zero_mixing_keeps_uniform_rejection_probabilities(angles):
    assert evaluate(3,9,6,angles)["uniform_full_target_population_success_exact"] == "1/729"


@pytest.mark.parametrize("n,q,M", [(1,3,2),(2,9,5),(8,9,24)])
def test_one_layer_limit_retains_exact_self_word_law(n,q,M):
    from ternary_hot_phase_mixer import one_layer_pi_population
    assert evaluate(n,q,M,(0,0,2,2))["uniform_full_target_population_success_exact"] == one_layer_pi_population(n,q,M)["uniform_target_population_success_exact"]


def test_signed_terminal_weights_are_not_probabilities_and_normalize_exactly():
    weights = terminal_weights(5,2,2)
    assert any(a[0] < 0 for i,a in weights)
    assert (sum(a[0] for i,a in weights),sum(a[1] for i,a in weights)) == (81**5,0)


def test_large_scaling_transfer_uses_no_word_group_or_path_enumeration(monkeypatch):
    complete_graph()
    monkeypatch.setattr("ternary_two_layer_path_transfer.product",lambda *a,**k:pytest.fail("large native grid enumerated"))
    r=evaluate(32,81,136,(1,1,1,1))
    assert 0 <= Fraction(r["uniform_full_target_population_success_exact"]) <= 1
    assert not r["enumerates_original_word_cube_or_secret_group"]
    assert r["keeps_integer_lattice_and_full_root_torsion"]


def test_finite_dag_depth_and_all_quarter_loops_are_exact_certificates():
    c=structural_certificate()
    assert c["maximum_strict_lattice_path_length"] == 5
    assert c["all_quarter_self_loop_moduli_at_most_one"]
    assert c["continuous_self_loop_modulus_upper"] == "43/27"
    assert c["continuous_self_loop_modulus_one_not_certified_by_this_report"]
    assert any(int(a["coefficient_numerator_over81"]) < 0
               for r in c["all_self_loop_Laurent_coefficients"] for a in r["Laurent_coefficients"])


def test_public_continuous_angles_fail_in_stated_near_entropy_regime():
    c=family_envelopes(128,243,648)
    assert Fraction(c["label_and_target_adaptive_continuous_angles_uniform_success_upper"]) < Fraction(1,2**90)
    assert Fraction(c["label_and_target_adaptive_continuous_angles_Born_success_upper"]) < Fraction(1,2**45)
    assert c["arbitrary_mixer_shapes_more_layers_or_other_receivers_not_covered"]


def test_continuous_coarse_bound_is_not_extrapolated_to_arbitrary_larger_batches():
    c=family_envelopes(8,9,1000)
    assert c["all_fixed_continuous_angles_uniform_success_upper"] == "1"
    assert c["continuous_bound_can_be_vacuous_for_much_larger_polynomial_batches"]


@pytest.mark.parametrize("angles", [(True,0,0,0),(4,0,0,0),(0.5,0,0,0),(0,0,0)])
def test_angle_schema_is_exact_and_scoped(angles):
    with pytest.raises(ValueError):
        evaluate(1,3,2,angles)


def test_complete_census_cap_never_returns_partial_mean():
    with pytest.raises(ValueError):
        exact_circuit_census(9,3,(1,1,1,1))


def test_artifact_pinned_math_and_no_claim_promotions(artifact):
    assert artifact["derivation_sha256"] == hashlib.sha256(DERIVATION.read_bytes()).hexdigest()
    for flag in ("general_mixer_shape_or_deeper_circuit_lower_bound","coherent_fiber_eraser_supplied","quantum_speedup_proved","candidate_record_accepted","novelty_claim"):
        assert artifact[flag] is False


def test_independent_checker():
    r=subprocess.run(["node","research/certificates/ternary_two_layer_path_transfer_crosscheck.js"],capture_output=True,text=True)
    assert r.returncode == 0,r.stderr
    assert json.loads(r.stdout)["status"] == "PASS"


@pytest.mark.parametrize("case",["lattice","Smith","loop","mean","scope"])
def test_independent_checker_rejects_tampered_mathematical_evidence(artifact,tmp_path,case):
    bad=deepcopy(artifact)
    if case == "lattice":
        bad["complete_integer_lattice_graph"][0]["coordinate_pattern_next_states"][1]=0
    elif case == "Smith":
        bad["complete_integer_lattice_graph"][1]["zero_subset_Smith_invariants"][0]["invariants"]=[3]
    elif case == "loop":
        bad["signed_transfer_structure_certificate"]["all_self_loop_Laurent_coefficients"][0]["Laurent_coefficients"][0]["coefficient_numerator_over81"]="100"
    elif case == "mean":
        bad["growing_population_menus"][0]["fixed_angle_population_menu"][0]["uniform_full_target_population_success_exact"]="0"
    else:
        bad["global_two_layer_family_envelopes"][-1]["continuous_bound_can_be_vacuous_for_much_larger_polynomial_batches"]=False
    p=tmp_path/"bad.json"; p.write_text(json.dumps(bad))
    r=subprocess.run(["node","research/certificates/ternary_two_layer_path_transfer_crosscheck.js",str(p)],capture_output=True,text=True)
    assert r.returncode != 0
