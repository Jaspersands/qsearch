import json
from pathlib import Path

import pytest
from sympy import Matrix, Rational, eye

import research_registry as registry
from campaign_negative_claim_audit import (
    ACTIVE, ARCHIVE, IDS, build_report, fidelity_counter, graph_input_counter,
    periodic_trotter_counter, positive_slow_chain, stationary_small_gap,
)


@pytest.mark.parametrize("n", (1, 8, 64, 256))
def test_arbitrarily_small_gap_does_not_force_slow_evolution_for_fixed_ground_projector(n):
    r = stationary_small_gap(n)
    H0, Hprime, P = (Matrix(r[key]) for key in ("H0", "Hprime", "ground_projector"))
    assert H0*P-P*H0 == Hprime*P-P*Hprime == Matrix.zeros(2)
    assert P*P == P and P.trace() == 1
    assert Rational(r["minimum_gap"]) == 2*Rational(1, 3**n)
    assert r["ground_state_leakage_for_every_positive_runtime"] == "0"
    assert not r["sufficient_error_bound_is_a_necessary_runtime_bound"]


@pytest.mark.parametrize("n", (1, 100, 1048576))
def test_nonzero_extensive_commutator_does_not_make_a_trotter_upper_bound_necessary(n):
    r = periodic_trotter_counter(n)
    A, B, C, comm = (Matrix(r[key]) for key in ("A", "B", "AplusB", "commutator"))
    assert A+B == C and A*B-B*A == comm and comm != Matrix.zeros(2)
    assert A*A == 9*eye(2) and B*B == 16*eye(2) and C*C == 25*eye(2)
    assert set(A.eigenvals()) == {-3, 3} and set(B.eigenvals()) == {-4, 4} and set(C.eigenvals()) == {-5, 5}
    assert comm.T*comm == 576*eye(2)
    assert r["total_commutator_norm"] == 24*n
    assert r["Trotter_steps"] == 1 and r["exact_complete_Trotter_error"] == "0"
    assert not r["generic_simulation_is_always_easy"]


def test_zero_target_fidelity_can_still_be_a_pure_output_not_white_noise():
    r = fidelity_counter()
    target, error, output = (Matrix(r[key]) for key in ("target", "unitary_error", "output"))
    assert error.T*error == eye(2) and error*target*error.T == output
    assert output*output == output and output.trace() == 1
    assert (target*output).trace() == 0
    assert r["output_purity"] == "1" and r["maximally_mixed_purity"] == "1/2"
    assert r["squared_Hilbert_Schmidt_distance_to_white"] == "1/2"


@pytest.mark.parametrize("n", (8, 64, 256))
def test_positive_reversible_weights_do_not_guarantee_fast_mixing_of_a_chosen_update(n):
    r = positive_slow_chain(n)
    P = Matrix(r["transition_matrix"])
    eps = Rational(1, 2**n)
    assert all(v > 0 for v in P)
    assert P == P.T and P*Matrix([1, 1]) == Matrix([1, 1])
    assert set(P.eigenvals()) == {1, 1-2*eps}
    assert (1-2*eps*r["steps"])/2 == Rational(3, 8)
    assert r["TV_from_point_start_lower_at_steps"] == "3/8"
    assert r["direct_uniform_sampler_is_easy"]
    assert not r["this_example_excludes_every_classical_sampler"]


@pytest.mark.parametrize("n", (8, 32, 64, 256))
def test_linear_explicit_graph_work_is_not_polynomial_depth_work(n):
    r = graph_input_counter(n)
    assert r["explicit_graph_vertices"] == 2**(n+2)-2
    assert not r["linear_vertex_cost_is_polynomial_tree_depth_cost"]
    assert not r["oracle_algorithm_dequantized_by_expanding_exponential_graph"]


def test_originals_are_preserved_but_not_consumed_as_active_negatives():
    archive = json.loads(ARCHIVE.read_text())
    active = json.loads(ACTIVE.read_text())
    assert set(IDS).issubset({row["id"] for row in archive})
    assert not {row["id"] for row in active}.intersection(IDS)
    for row in archive:
        assert row["original_record"]["id"] == row["id"]
        assert row["original_record"]["claim"] and row["original_record"]["lesson"]
        assert row["status"] == "QUARANTINED_OVERBROAD_NO_GO"
        assert not row["original_checks_are_general_proofs"]
        assert row["reinstatement_requires_scoped_mathematical_review"]


@pytest.fixture
def isolated_registry(monkeypatch, tmp_path):
    active, archive = tmp_path/"negative_results.json", tmp_path/"quarantined.json"
    records = json.loads(ARCHIVE.read_text())
    active.write_text(json.dumps([{"id": "SAFE-SCOPED-CONTROL"}]))
    archive.write_text(json.dumps(records))
    monkeypatch.setattr(registry, "NEGATIVE_RESULTS_PATH", active)
    monkeypatch.setattr(registry, "QUARANTINED_NEGATIVES_PATH", archive)
    return active, records


def test_quarantine_rejects_upsert_before_mutating_registry(isolated_registry):
    active, archived = isolated_registry
    original = active.read_text()
    for row in archived:
        record = registry.NegativeResultRecord(**row["original_record"])
        with pytest.raises(ValueError, match="quarantined"):
            registry.upsert_negative_result(record)
        assert active.read_text() == original


def test_raw_file_reintroduction_is_filtered_and_detected_by_validation(isolated_registry):
    active, archived = isolated_registry
    active.write_text(json.dumps([{"id": "SAFE-SCOPED-CONTROL"}, archived[0]["original_record"]]))
    assert registry.load_negative_results() == [{"id": "SAFE-SCOPED-CONTROL"}]
    result = registry.validate_registry()
    assert not result["valid"]
    assert any(row["obligation_id"] == "NEGATIVE-CLAIM-REVIEW" and row["hard_reject"] for row in result["issues"])
    assert result["quarantined_negative_result_count"] == len(archived)


def test_live_report_is_scoped_and_never_certifies_the_remaining_campaign():
    r = build_report()
    assert len(r["quarantined_ids"]) == 3
    assert len(r["stationary_small_gap_controls"]) == len(r["periodic_Trotter_controls"]) == 3
    assert len(r["positive_slow_chain_controls"]) == 3 and len(r["graph_input_controls"]) == 4
    assert not r["remaining_campaign_claims_verified"]
    assert not r["countercontrols_are_quantum_algorithm_candidates"]
    assert not r["new_quantum_speedup_established"]


@pytest.mark.parametrize("call", (lambda: stationary_small_gap(0), lambda: periodic_trotter_counter(True),
                                 lambda: positive_slow_chain(2), lambda: graph_input_counter(-1)))
def test_invalid_countercontrol_parameters_are_rejected(call):
    with pytest.raises(ValueError):
        call()
