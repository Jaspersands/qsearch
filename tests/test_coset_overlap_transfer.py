import copy
import json
from fractions import Fraction

import numpy as np
import pytest

from coherent_overlap_programs import OverlapEchoProgram
from coset_hidden_involution_binary_decision_reduction import involution_conjugacy_class
from coset_overlap_echo import _group_data, exact_three_copy_echo, reflection_coefficients, source_block_control
from coset_overlap_transfer import (
    _fraction, _integer_count_product, _safe_prime_ceiling, build_orbit_transfer,
    build_transfer_report, certified_moment_cap, exact_path_moments, find_decay_witness,
    modular_moments, pair_event_baseline, replay_decay_certificate, verify_decay_witness,
    write_transfer_report,
    replay_transfer_report,
    prefix_tail_envelope,
)


def unquotiented_integer_moment(n, t, k, hidden):
    coefficients, _ = reflection_coefficients(n, t)
    group, index, multiply, _, _ = _group_data(n)
    pairs = [(a, c) for a in range(len(group)) for c in range(len(group))]
    choices = {index[tuple(range(n))]} if hidden is None else {index[tuple(range(n))], index[hidden]}
    weights = [int(coefficients[a])*int(coefficients[c]) for a, c in pairs]
    endpoint = [int(multiply[c, a] in choices) for a, c in pairs]
    f = [[int(multiply[multiply[multiply[d, c], b], a] in choices) for b, d in pairs] for a, c in pairs]
    state = [w*end for w, end in zip(weights, endpoint)]
    for edge in range(1, k-1):
        state = [weights[out] * sum(value*(f[incoming][out] if edge % 2 else f[out][incoming])
                 for incoming, value in enumerate(state)) for out in range(len(pairs))]
    return Fraction(sum(v*end for v, end in zip(state, endpoint)), len(group)**(2*(k-1)))


@pytest.mark.parametrize("hidden", (None, *involution_conjugacy_class(3, 1)))
def test_crt_orbit_transfer_matches_unquotiented_python_integers(hidden):
    record = exact_path_moments(OverlapEchoProgram(3, 1, 8), (3, 4, 5, 8), hidden=hidden)
    assert record["verified"]
    for row in record["rows"]:
        assert _fraction(row) == unquotiented_integer_moment(3, 1, row["copies"], hidden)
    assert record["arithmetic_certificate"]["modulus_exceeds_twice_absolute_bound"]
    assert not record["arithmetic_certificate"]["floating_cancellation_used_for_result"]


def test_nonmissing_four_copy_case_matches_physical_matrices():
    p = OverlapEchoProgram(4, 1, 4)
    physical = source_block_control(p)
    h = involution_conjugacy_class(4, 1)[0]
    m0 = _fraction(exact_path_moments(p, (3, 4))["rows"][-1])
    mh = _fraction(exact_path_moments(p, (3, 4), hidden=h)["rows"][-1])
    assert physical["verified"]
    assert physical["output_total_variation"] == pytest.approx(float(abs(mh-m0)/2), abs=1e-10)


def test_fixed_hidden_quotient_uses_centralizer_and_keeps_orbit_sizes():
    h = involution_conjugacy_class(4, 1)[0]
    kernel = build_orbit_transfer(4, 1, h)
    assert kernel.acting_group_order == 4
    assert len(kernel.representatives) < kernel.order**2
    assert kernel.orbit_sizes.sum() == 24**2
    balance = kernel.a_to_b.multiply(kernel.orbit_sizes[:, None]) - kernel.b_to_a.T.multiply(kernel.orbit_sizes[None, :])
    assert not balance.nnz or np.max(np.abs(balance.data)) == 0
    assert not kernel.a_to_b.data.flags.writeable
    moments = [exact_path_moments(OverlapEchoProgram(4, 1, 5), (5,), hidden=member)["rows"][0]
               for member in involution_conjugacy_class(4, 1)]
    assert len({_fraction(row) for row in moments}) == 1


@pytest.mark.parametrize("n,t", ((True, 1), (6.0, 3), (8, 4)))
def test_kernel_rejects_invalid_or_factorial_inputs(n, t):
    with pytest.raises(ValueError):
        build_orbit_transfer(n, t)


def test_modular_arithmetic_budget_and_large_radix_product():
    kernel = build_orbit_transfer(3, 1)
    with pytest.raises(ValueError):
        modular_moments(kernel, (3,), _safe_prime_ceiling(kernel))
    values = [((i+1) << 170) + 3 for i in range(len(kernel.weights))]
    actual = _integer_count_product(kernel.a_to_b, values)
    dense = kernel.a_to_b.toarray().astype(int)
    assert actual == [sum(int(c)*v for c, v in zip(row, values)) for row in dense]


@pytest.mark.parametrize("copies", ((), (2,), (129,), (3, 3), (True,), (3.0,)))
def test_invalid_sweeps(copies):
    with pytest.raises(ValueError):
        exact_path_moments(OverlapEchoProgram(3, 1, 3), copies)


def test_no_temporal_round_extension():
    with pytest.raises(ValueError, match="ONE echo round"):
        exact_path_moments(OverlapEchoProgram(3, 1, 3, 2), (3,))


def test_protected_alternative_does_not_receive_a_decay_certificate():
    kernel = build_orbit_transfer(3, 1, involution_conjugacy_class(3, 1)[0])
    assert not find_decay_witness(kernel)["certified"]
    assert not verify_decay_witness(kernel, [1]*len(kernel.weights), Fraction(1, 100))["certified"]


@pytest.fixture(scope="module")
def report():
    return build_transfer_report()


def test_s6_long_paths_and_exact_all_copy_bound(report):
    assert report["claim_gate"]["exact_transfer_controls_verified"]
    assert report["claim_gate"]["s6_simple_tv_bound_three_times_three_quarters_power"]
    assert report["claim_gate"]["s6_all_copy_one_pair_dominance_certified"]
    row = next(r for r in report["transfer_audit"]["records"] if r["degree"] == 6)
    assert row["null"]["kernel"]["orbit_boundary_size"] == 585
    assert row["alternative"]["kernel"]["orbit_boundary_size"] == 7438
    laws = {r["copies"]: r for r in row["output_laws"]}
    assert laws[36]["output_total_variation"] == pytest.approx(8.038335919111392e-8)
    assert laws[64]["output_total_variation"] < 3e-13
    assert laws[36]["pair_event_baseline"]["total_variation"] > .55
    assert not any(r["echo_beats_pair_event"] for r in row["output_laws"])
    for certificate in row["decay_certificates"]:
        assert certified_moment_cap(certificate, OverlapEchoProgram(6, 3, 1024)) < Fraction(1, 10**60)
        with pytest.raises(ValueError, match="does not cover"):
            certified_moment_cap(certificate, OverlapEchoProgram(6, 3, 36, 6))
        with pytest.raises(ValueError, match="does not cover"):
            certified_moment_cap(certificate, OverlapEchoProgram(8, 4, 36))
    assert report["claim_gate"]["speedup_claim_allowed"] is False
    json.dumps(report)


def test_exact_prefix_plus_tail_rules_out_every_copy_count(report):
    row = next(r for r in report["transfer_audit"]["records"] if r["degree"] == 6)
    envelope = row["prefix_tail_envelope"]
    assert envelope["certified"] and envelope["one_pair_dominates_every_copy_count"]
    cap = envelope["all_copy_tv_cap"]
    assert Fraction(int(cap["numerator_hex"], 16), int(cap["denominator_hex"], 16)) == Fraction(16843, 303750)
    assert envelope["exact_maximizing_copy_counts"] == [3]
    assert envelope["prefix_count"] == 29
    assert envelope["tail_first_copy_count"] == 32
    broken = copy.deepcopy(row)
    broken["null"]["rows"] = [r for r in broken["null"]["rows"] if r["copies"] != 17]
    assert not prefix_tail_envelope(broken)["certified"]


def test_certificate_replay_detects_mutated_prefactors_and_witness(report):
    row = next(r for r in report["transfer_audit"]["records"] if r["degree"] == 6)
    record = row["decay_certificates"][0]
    kernel = build_orbit_transfer(6, 3)
    assert replay_decay_certificate(kernel, record)
    altered = copy.deepcopy(record)
    altered["even_copies_prefactor"]["numerator_hex"] = "0x0"
    assert not replay_decay_certificate(kernel, altered)
    altered = copy.deepcopy(record)
    altered["positive_witness_hex"][0] = "0x0"
    assert not replay_decay_certificate(kernel, altered)


def test_finite_pair_event_baseline_is_quantum_and_preserves_mass():
    for k in (3, 12, 64):
        result = pair_event_baseline(6, 3, k)
        assert result["quantum_frontend"]
        assert not result["classical_unknown_input_solver"]
        assert 0 < Fraction(result["exact_total_variation"]) < 1
        assert result["lower_bound_on_full_pair_likelihood_readout"]
        assert result["group_qft_or_inverse_calls"] == 6*(k//2)


def test_event_baseline_is_bounded_by_the_full_quantum_label_readout():
    from coset_binary_carrier_instruments import independent_pair_copy_baseline
    for k in (3, 4, 6):
        event = Fraction(pair_event_baseline(6, 3, k)["exact_total_variation"])
        complete = Fraction(independent_pair_copy_baseline(6, 3, k)["exact_total_variation"])
        assert event <= complete


def test_writer_disabled_and_custom_ids(tmp_path, monkeypatch, report):
    import coset_overlap_transfer as module
    monkeypatch.setattr(module, "build_transfer_report", lambda **kw: copy.deepcopy(report))
    results, negatives = [], []
    monkeypatch.setattr(module, "upsert_experiment_result", results.append)
    monkeypatch.setattr(module, "upsert_negative_result", negatives.append)
    path = tmp_path / "transfer.json"
    write_transfer_report(path, write_registry=False)
    assert results == [] and negatives == []
    write_transfer_report(path, registry_experiment_id="EXP-CUSTOM", registry_candidate_id="CAND-CUSTOM", registry_result_id="RESULT-CUSTOM")
    assert results[0].id == "RESULT-CUSTOM" and results[0].experiment_id == "EXP-CUSTOM"
    assert negatives[0].applies_to == ["CAND-CUSTOM"]
    assert json.loads(path.read_text())["claim_gate"]["growing_degree_bound_proved"] is False


def test_saved_certificate_replay_and_missing_hypothesis(tmp_path, report):
    path = tmp_path / "transfer.json"
    path.write_text(json.dumps(report))
    replay = replay_transfer_report(path)
    assert replay["valid"] and replay["exact_prefix_moments_replayed"] == 58
    broken = copy.deepcopy(report)
    row = next(r for r in broken["transfer_audit"]["records"] if r["degree"] == 6)
    row["decay_certificates"].pop()
    path.write_text(json.dumps(broken))
    assert not replay_transfer_report(path)["valid"]
    assert not replay_transfer_report(tmp_path / "missing.json")["valid"]


def test_saved_moment_tampering_is_not_hidden_by_valid_decay_vectors(tmp_path, report):
    broken = copy.deepcopy(report)
    row = next(r for r in broken["transfer_audit"]["records"] if r["degree"] == 6)
    next(r for r in row["null"]["rows"] if r["copies"] == 17)["moment_numerator_hex"] = "0x0"
    path = tmp_path / "transfer.json"
    path.write_text(json.dumps(broken))
    result = replay_transfer_report(path)
    assert not result["valid"]
    assert "CRT replay" in result["issues"][0]


def test_runner_proof_dequantization_integration(tmp_path, monkeypatch, report):
    import coset_overlap_transfer as module
    import experiment_runner
    from coset_overlap_transfer import DEFAULT_EXPERIMENT_ID
    from dequantization_checks import build_dequantization_report
    from proof_tracker import _overlap_transfer_lemmas
    from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry
    monkeypatch.chdir(tmp_path)
    initialize_seed_registry(overwrite=False)
    monkeypatch.setattr(module, "build_transfer_report", lambda **kw: copy.deepcopy(report))
    write_transfer_report()
    for _ in range(2):
        assert experiment_runner.run_experiment(DEFAULT_EXPERIMENT_ID).status == "completed"
    assert len([r for r in load_experiment_results() if r["experiment_id"] == DEFAULT_EXPERIMENT_ID]) == 1
    assert any(r["id"] == "S6-ONE-ROUND-OVERLAP-ECHO-ALL-COPY-DECAY" for r in load_negative_results())
    assert any(r["id"].endswith("S6-SPATIAL-ECHO-SIGNAL-ERASURE") for r in build_dequantization_report()["findings"])
    assert all(r.status.startswith("derived") for r in _overlap_transfer_lemmas("CODE-COSET-COLLECTIVE"))
    assert validate_registry()["valid"]
    broken = copy.deepcopy(report)
    broken["claim_gate"]["s6_one_round_all_copy_decay_certified"] = 1
    module.REPORT_PATH.write_text(json.dumps(broken))
    assert _overlap_transfer_lemmas("CODE-COSET-COLLECTIVE")[1].status.startswith("blocked")


def test_cli_no_registry_and_replay_are_read_only(monkeypatch, report):
    import qsearch
    from argparse import Namespace
    monkeypatch.setattr(qsearch, "initialize_seed_registry", lambda **kw: pytest.fail("seed touched"))
    monkeypatch.setattr(qsearch, "write_transfer_report", lambda **kw: report if kw["write_registry"] is False else pytest.fail("registry touched"))
    assert qsearch.command_coset_overlap_transfer(Namespace(no_registry=True, replay=False)) == 0
    monkeypatch.setattr(qsearch, "replay_transfer_report", lambda: {"valid": True})
    assert qsearch.command_coset_overlap_transfer(Namespace(no_registry=False, replay=True)) == 0
