"""Tests for modulo-scale original-prefix pruning and canonical DAG collapse."""
from copy import deepcopy
from fractions import Fraction
import json
import subprocess

import pytest

from theorems import native_prefix_ambiguity_pruning as P
from native_basis_lottery import _certificate_int


def stored():
    return json.loads(P.REPORT.read_text())


def records(rows):
    return tuple(
        P.NoisyLinearRecord(
            tuple(_certificate_int(a) for a in r["label"]),
            _certificate_int(r["value"]),
            _certificate_int(r["modulus"]),
            r["source_id"],
        )
        for r in rows
    )


def node_check(payload):
    return subprocess.run(
        [
            "node",
            "-e",
            "const C=require('./research/certificates/native_prefix_ambiguity_pruning_crosscheck.js');"
            "let s='';process.stdin.on('data',x=>s+=x);"
            "process.stdin.on('end',()=>console.log(JSON.stringify(C.verify(JSON.parse(s)))));",
        ],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        cwd=P.ROOT,
    )


def test_modulo_scale_projection_is_completely_invariant_to_unknown_upper_quotient():
    q0, L, g = 243, 27, 9
    prefix = (14, 23)
    errors = (-2, 3, 0, -1, 2)
    labels = ((7, 19), (41, 103), (200, 11), (5, 88), (123, 67))
    baseline = None
    for h0 in (0, 1, 4, 8):
        for h1 in (0, 2, 5, 7):
            s = (prefix[0] + L * h0, prefix[1] + L * h1)
            raw = tuple(
                P.NoisyLinearRecord(a, (a[0] * s[0] + a[1] * s[1] + e) % q0, q0, f"inv:{j}")
                for j, (a, e) in enumerate(zip(labels, errors))
            )
            fit = P.modulo_scale_prefix_fit(raw, L, prefix, 3)
            assert fit["fits_modulo_scale_radius"]
            assert fit["non_wrapping_unique_decoding_regime_4R_lt_L"]
            assert fit["modulo_scale_circular_distances"] == tuple(abs(e) for e in errors)
            if baseline is None:
                baseline = fit["modulo_scale_circular_distances"]
            else:
                assert fit["modulo_scale_circular_distances"] == baseline


@pytest.mark.parametrize("index", (0, 1))
def test_actual_dag_pruning_controls_prune_false_branches_and_merge_canonical_nodes(index):
    c = stored()["actual_dag_pruning_controls"][index]
    raw = records(c["original_records"])
    secret = tuple(_certificate_int(x) for x in c["original_secret_FOR_CALIBRATION_ONLY"])
    dag = c["dag_traversal"]
    assert tuple(_certificate_int(x) for x in dag["candidate_secret"]) == secret
    assert dag["max_active_canonical_nodes_per_level"] == 2
    lv0 = dag["level_reports"][0]["node_pruning_reports"][0]["candidate_evaluations"]
    statuses = [e["status"] for e in lv0]
    assert statuses.count("PRUNED_BY_MODULO_SCALE_ORIGINAL_RESIDUAL") == 2
    assert statuses.count("REJECTED_INCOMPATIBLE_RING_IMAGE") == 1
    assert statuses.count("SURVIVING_NEW_CANONICAL_NODE") == 2
    assert statuses.count("MERGED_INTO_EXISTING_CANONICAL_NODE") == 1
    assert not dag["multiple_producer_or_source_law_certified"]
    assert dag["total_canonical_node_original_rounding_evaluations"] == len(raw)+sum(
        r["canonical_node_original_rounding_evaluations"] for lv in dag["level_reports"] for r in lv["node_pruning_reports"])


def test_wrap_around_and_half_modulus_collision_falsifiers():
    f = P.falsifiers()
    w1 = f["complete_wrap_L_le_2R_falsifier"]
    assert w1["all_tested_prefixes_fit_trivially"]
    assert w1["pruner_refuses_wrapping_scale"]
    assert w1["surviving_canonical_child_count"] == 0
    w2 = f["half_modulus_collision_2R_lt_L_le_4R_falsifier"]
    assert not w2["non_wrapping_4R_lt_L"]
    assert w2["true_prefix_fits"] and w2["colliding_wrong_prefix_also_fits"]
    assert w2["four_R_lt_L_is_sufficient_scope_not_instance_necessity"]


def test_gaussian_dag_pruning_profiles_and_arb_probability_replay():
    rep = stored()
    profiles = rep["Gaussian_DAG_pruning_profiles"]
    assert [p["dimension"] for p in profiles] == [8, 32, 128]
    assert [p["tight_radius_covers_all_declared_nonunit_children"] for p in profiles] == [False, True, True]
    assert [p["pruned_canonical_DAG_internal_nodes_upper_IF_covered"] for p in profiles] == [None, 5, 8]
    assert P.verify_probability_boxes(rep)["verified"] is True
    for p in profiles[1:]:
        assert Fraction(p["total_local_pruning_and_radius_failure_upper"]) < Fraction(1, 10 ** 18)
        d = p["first_step_max_child_root_digits"]
        expansions = 1 + d * (d + 1) // 2
        assert p["pruned_canonical_DAG_expansion_calls_upper_IF_covered"] == expansions
        assert p["pruned_canonical_DAG_candidate_checks_upper_IF_covered"] == expansions * p["candidates_per_expanded_node"]
        assert not p["coefficient_bound_derived_from_actual_or_published_producer"]
        assert int(p["unpruned_complete_tree_leaves_at_depth_d_max"]) >= 64 ** 5


def test_validation_rejects_invalid_scales_radii_and_empty_candidates():
    raw = (P.NoisyLinearRecord((1, 2), 5, 81, "r0"),)
    with pytest.raises(ValueError):
        P.modulo_scale_prefix_fit(raw, 1, (0, 0), 0)
    with pytest.raises(ValueError):
        P.modulo_scale_prefix_fit(raw, 2, (0, 0), 0)
    with pytest.raises(ValueError):
        P.modulo_scale_prefix_fit(raw, 9, (0, 0), 21)
    with pytest.raises(ValueError):
        P.prune_candidate_list_at_node(raw, 1, (0, 0), (), 0)


def test_independent_js_checker_verifies_stored_report():
    r = node_check(stored())
    assert r.returncode == 0, r.stderr
    out = json.loads(r.stdout)
    assert out["verified"] is True
    assert out["replayed_candidate_checks"] == 22
    assert out["replayed_distance_checks"] == 180
    assert out["multiple_producer_supplied"] is False


def test_depth_dependent_lists_revisit_the_same_node_and_falsify_old_linear_work_bound():
    c = P.scope_and_revisit_countercontrols()["canonical_node_revisited_at_different_depths"]
    r = c["dag_traversal"]
    assert r["candidate_secret"] == (5,)
    assert r["total_candidates_evaluated"] == 8 > c["claimed_old_linear_candidate_bound"]
    assert r["actual_canonical_node_expansion_calls"] == 4
    assert r["actual_distinct_canonical_nodes_expanded"] == 3
    assert r["actual_repeated_canonical_node_expansions"] == 1
    assert not r["global_candidate_list_per_node_cache_used"]
    assert not r["unpruned_exponential_tree_elimination_certified_on_observed_bank"]


def test_nonwrapping_is_a_sufficient_source_scope_not_instance_necessity():
    c = P.scope_and_revisit_countercontrols()["unique_instance_outside_nonwrapping_proof_scope"]
    assert 4*c["radius"] >= c["scale"] > 2*c["radius"]
    assert c["compatible_prefixes"] == (5,) and c["complete_prefixes_checked"] == 27
    assert c["proof_gate_is_not_a_general_instance_impossibility_claim"]


@pytest.mark.parametrize("index", (0,1))
def test_safe_prefix_recursion_is_matched_by_one_pass_classical_root_completion(index):
    c=stored()["actual_dag_pruning_controls"][index];b=c["one_pass_classical_root_comparison"]
    assert b["fitting_secrets"] == [c["original_secret_FOR_CALIBRATION_ONLY"]]
    assert len(b["root_trials"]) == 6 and b["public_label_rref_calls"] == 1
    assert b["cached_ring_inversions"] == 2
    assert b["additional_multiple_or_decision_producer_calls"] == b["Gaussian_flooded_samples_requested"] == 0
    assert not b["planted_truth_or_source_law_certified"]


def test_modulo_scale_code_separation_forces_mod3_full_rank():
    # A mod3 null vector induces an exactly zero nonzero codeword modulo every3-power L.
    labels=((1,1),(2,2),(0,0));z=(1,2)
    for L in (3,9,27,81):
        h=tuple(L//3*x for x in z)
        assert any(h) and all(sum(a*x for a,x in zip(row,h)) % L == 0 for row in labels)


def test_pruning_radius_event_is_stronger_than_exact_all_row_quotient_rounding():
    for L in (3,9,27,81):
        for R in range((L-1)//4+1):
            assert 4*R < L
            for e in range(-R,R+1):
                assert (e+L//2)//L == 0


@pytest.mark.parametrize(
    "kind",
    (
        "dag-candidate",
        "dag-distance-count",
        "dag-rounding-count",
        "dag-merge-status",
        "dag-node-hash",
        "dag-secret",
        "profile-dmax",
        "profile-rgauss",
        "profile-crude",
        "profile-covered",
        "profile-tail",
        "profile-sep-union",
        "profile-dag-nodes",
        "profile-expansion-work",
        "profile-tree-leaves",
        "producer-coefficient-bound",
        "revisit-count",
        "necessity-claim",
        "wrap1-flag",
        "wrap2-flag",
        "producer-claim",
        "dependency",
        "hash",
    ),
)
def test_independent_js_checker_rejects_pruning_dag_and_source_tampering(kind):
    p = deepcopy(stored())
    c0 = p["actual_dag_pruning_controls"][0]["dag_traversal"]
    prof = p["Gaussian_DAG_pruning_profiles"][1]
    if kind == "dag-candidate":
        c0["total_candidates_evaluated"] += 1
    elif kind == "dag-distance-count":
        c0["total_original_distance_evaluations"] -= 1
    elif kind == "dag-rounding-count":
        c0["total_canonical_node_original_rounding_evaluations"] = 0
    elif kind == "dag-merge-status":
        c0["level_reports"][0]["node_pruning_reports"][0]["candidate_evaluations"][4]["status"] = "SURVIVING_NEW_CANONICAL_NODE"
    elif kind == "dag-node-hash":
        c0["level_reports"][0]["node_pruning_reports"][0]["surviving_canonical_child_nodes"][0]["canonical_node_sha256"] = "0" * 64
    elif kind == "dag-secret":
        c0["candidate_secret"][0] += 1
    elif kind == "profile-dmax":
        prof["first_step_max_child_root_digits"] += 1
    elif kind == "profile-rgauss":
        prof["tight_Gaussian_verification_radius"] = "1"
    elif kind == "profile-crude":
        prof["crude_q_over_n_radius_max_prunable_child_root_digits"] += 1
    elif kind == "profile-covered":
        prof["tight_radius_covers_all_declared_nonunit_children"] = False
    elif kind == "profile-tail":
        prof["whole_bank_Gaussian_radius_failure_upper"] = "0"
    elif kind == "profile-sep-union":
        prof["all_scales_code_separation_failure_union_upper"] = "0"
    elif kind == "profile-dag-nodes":
        prof["pruned_canonical_DAG_internal_nodes_upper_IF_covered"] = 1
    elif kind == "profile-expansion-work":
        prof["pruned_canonical_DAG_candidate_checks_upper_IF_covered"] = (prof["first_step_max_child_root_digits"]+1)*prof["candidates_per_expanded_node"]
    elif kind == "producer-coefficient-bound":
        prof["coefficient_bound_derived_from_actual_or_published_producer"] = True
    elif kind == "revisit-count":
        p["scope_and_revisit_countercontrols"]["canonical_node_revisited_at_different_depths"]["dag_traversal"]["actual_repeated_canonical_node_expansions"] = 0
    elif kind == "necessity-claim":
        p["scope_and_revisit_countercontrols"]["unique_instance_outside_nonwrapping_proof_scope"]["compatible_prefixes"] = []
    elif kind == "profile-tree-leaves":
        prof["unpruned_complete_tree_leaves_at_depth_d_max"] = 1
    elif kind == "wrap1-flag":
        p["wrap_around_falsifiers"]["complete_wrap_L_le_2R_falsifier"]["all_tested_prefixes_fit_trivially"] = False
    elif kind == "wrap2-flag":
        p["wrap_around_falsifiers"]["half_modulus_collision_2R_lt_L_le_4R_falsifier"]["four_R_lt_L_is_sufficient_scope_not_instance_necessity"] = False
    elif kind == "producer-claim":
        p["actual_quantum_decision_or_multiple_producer"] = True
    elif kind == "dependency":
        p["dependency_sha256"]["native_source_refresh.py"] = "0" * 64
    else:
        p["producer_sha256"] = "0" * 64
    assert node_check(p).returncode != 0
