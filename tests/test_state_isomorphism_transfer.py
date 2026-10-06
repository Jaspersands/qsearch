from fractions import Fraction
from itertools import product
import json
import math
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pytest

from literature_pipeline import extract_literature_records
from state_hsp_dhsp_scope import geometry
from state_isomorphism_transfer import (
    graph_lift_control, lifted_graph_action, no_programming_control,
    orbit_gap_ledger, packet_control, run_controls,
)


def exact(r):
    return Fraction(int(r["numerator"]), int(r["denominator"]))


@pytest.fixture(scope="module")
def report():
    return run_controls()


def test_actual_graph_lift_recovers_original_reflection_not_a_new_easy_group(report):
    assert len(report["graph_lift_controls"]) == 36
    for r in report["graph_lift_controls"]:
        N, s = r["rotation_order"], r["hidden_element_calibration"]
        assert r["reflection_stabilizer_indices"] == [0, N+s]
        assert r["standard_right_coset_DHSP_hidden_reflection_shift"] == (-s) % N
        assert r["known_sign_map_preserves_full_target"]
        assert r["normal_core_indices"] == [0]
        assert r["minimum_asymmetry_gap"] == 1
        assert r["lifted_state_norm"] == pytest.approx(1)
        assert r["executed_inverse_return_probability"] == pytest.approx(1)
        assert r["selector_function_queries_per_lifted_superposition_preparation"] == 2
        assert r["selector_function_queries_per_preparation_inverse"] == 2
        assert not r["generalized_dihedral_group_is_abelian"]
        assert not r["full_hidden_shift_problem_removed"]
        assert not r["polynomial_overhead_solves_resulting_StateHSP"]
        expected = [2*N*N if j in (0, N+s) else 0 for j in range(2*N)]
        assert r["exact_support_intersection_counts"] == expected


def test_lift_representation_law_on_all_basis_states_with_independent_sympy_group():
    N = 4
    G = geometry(N)
    indices = np.arange(2*N**4)
    for i, g in enumerate(G["elements"]):
        for j, h in enumerate(G["elements"]):
            k = G["index"][g*h]
            twice = lifted_graph_action(lifted_graph_action(indices, N, j % N, j//N), N, i % N, i//N)
            once = lifted_graph_action(indices, N, k % N, k//N)
            assert np.array_equal(twice, once)
    rotate_then_reflect = lifted_graph_action(lifted_graph_action(indices, N, 0, 1), N, 1, 0)
    reflect_then_rotate = lifted_graph_action(lifted_graph_action(indices, N, 1, 0), N, 0, 1)
    assert not np.array_equal(rotate_then_reflect, reflect_then_rotate)


def test_native_packet_good_gap_does_not_supply_circuit_or_decision_to_search(report):
    packets = report["native_packet_controls"][:8]
    assert {r["unfiltered_label_seed"] for r in packets} == set(range(44011, 44019))
    assert any(r["observed_gap_off_stabilizer"] > .2 for r in packets)
    for r in packets:
        assert r["all_hidden_secrets_are_YES_for_unrestricted_isomorphism_decision"]
        assert not r["decision_YES_alone_recovers_hidden_element"]
        assert not r["exact_packet_preparation_and_inverse_supplied_by_native_samples"]
        assert not r["well_separated_orbit_is_a_polynomial_decoder"]
        assert not r["Pauli_exponent_two_group_condition_met"]


def test_easy_order_two_and_aliased_native_sources_are_explicit_countercontrols(report):
    zero, half, even = report["native_packet_controls"][-3:]
    assert zero["cyclic_lift_image_order"] == 1 and len(zero["rotation_stabilizer"]) == 32
    assert half["cyclic_lift_image_order"] == 2 and len(half["rotation_stabilizer"]) == 16
    assert even["cyclic_lift_image_order"] == 16 and even["rotation_stabilizer"] == [0, 16]
    assert half["Pauli_exponent_two_group_condition_met"]
    assert not even["Pauli_exponent_two_group_condition_met"]


def test_orbit_gap_source_moment_is_exact_for_all_nonzero_differences():
    N, r = 8, 3
    for delta in range(1, N):
        mean = sum(math.prod(math.cos(math.pi*k*delta/N)**2 for k in labels)
                   for labels in product(range(N), repeat=r))/N**r
        assert mean == pytest.approx(2**(-r))


def test_scaled_packet_gap_and_literal_resampling_cost_have_separate_scopes(report):
    for r in report["orbit_gap_scaling_ledgers"]:
        N, bits, packet = int(r["modulus"]), r["modulus_bits"], r["IID_native_packet_size"]
        alpha = exact(r["maximum_nonidentity_orbit_overlap_threshold"])
        assert packet == bits+12
        assert exact(r["source_probability_of_any_overlap_above_threshold_upper"]) == Fraction(N-1, 2**packet*alpha**2)
        assert exact(r["source_probability_of_any_overlap_above_threshold_upper"]) <= Fraction(1, 1024)
        p = r["literal_ordered_packet_rejection_resampling_probability"]
        assert p == {"base": 2, "exponent": str(-bits*packet)}
        assert not r["good_gap_solves_preparation_or_decoding"]
        assert not r["Markov_union_bound_is_computational_lower_bound"]


def test_finite_copy_programs_cannot_exactly_supply_distinct_reflections(report):
    for r in report["exact_programming_countercontrols"]:
        N, t = r["modulus"], r["identical_program_copy_count"]
        assert r["exact_finite_program_overlap_is_nonzero"]
        assert r["program_overlap_log_abs"] == pytest.approx(t*math.log(math.cos(math.pi/N)))
        assert r["reflection_unitary_product_distance_from_scalar"] == pytest.approx(math.sqrt(2)*math.sin(2*math.pi/N))
        assert not r["deterministic_exact_universal_programming_of_both_reflections_possible"]
        assert not r["approximate_or_heralded_programs_excluded"]
        assert not r["generic_DCP_sample_runtime_lower_bound"]


def test_audited_paper_is_not_attributed_a_gowers_or_phase_sieve_algorithm():
    r = next(r for r in extract_literature_records() if r.id == "state-isomorphism-2026")
    assert r.source == "primary_audit_2605.12615v2"
    assert "decision" in r.mechanism
    assert "exponent-two" in r.problem_family
    assert "not automatically" in r.reduction
    assert "not Gowers" in r.proof_technique
    assert "native copies versus circuit descriptions" in r.no_go_barrier


def test_live_literature_artifact_matches_regenerated_primary_audit():
    path = Path(__file__).resolve().parents[1]/"research/literature_records.json"
    persisted = next(r for r in json.loads(path.read_text()) if r["id"] == "state-isomorphism-2026")
    fresh = next(r for r in extract_literature_records() if r.id == persisted["id"])
    for key in ("mechanism", "problem_family", "reduction", "no_go_barrier", "proof_technique", "open_question", "reusable_abstraction", "source"):
        assert persisted[key] == getattr(fresh, key)


def test_primary_override_also_matches_real_arxiv_version_urls_not_spoofed_hosts():
    for url in ("https://arxiv.org/abs/2605.12615v2", "https://arxiv.org/pdf/2605.12615v2.pdf"):
        with patch("literature_pipeline.fetch_recent_arxiv_quantum_algorithms", return_value=[{
            "id": "new-arxiv-record", "url": url, "tags": ["hidden-shift"], "title": "Incoming paper",
        }]):
            r = next(r for r in extract_literature_records(refresh_arxiv=True) if r.id == "new-arxiv-record")
            assert "decision" in r.mechanism and r.source == "primary_audit_2605.12615v2"
    with patch("literature_pipeline.fetch_recent_arxiv_quantum_algorithms", return_value=[{
        "id": "spoof-record", "url": "https://notarxiv.org/pdf/2605.12615v2.pdf", "tags": [], "title": "Unknown",
    }]):
        r = next(r for r in extract_literature_records(refresh_arxiv=True) if r.id == "spoof-record")
        assert r.source != "primary_audit_2605.12615v2"


def test_no_access_mismatch_is_promoted_to_paper_refutation(report):
    assert not any(report["claim_gate"].values())
    json.loads(json.dumps(report, allow_nan=False))


@pytest.mark.parametrize("call", [lambda: graph_lift_control(4, 4),
    lambda: lifted_graph_action([0], 4, True, 0), lambda: lifted_graph_action([-1], 4, 0, 0),
    lambda: packet_control(8, [0]*13), lambda: orbit_gap_ledger(2),
    lambda: orbit_gap_ledger(8, .1), lambda: no_programming_control(8, 0)])
def test_invalid_or_unbounded_contracts_are_rejected(call):
    with pytest.raises(ValueError):
        call()
