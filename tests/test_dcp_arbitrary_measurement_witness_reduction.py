import numpy as np
import pytest
from fractions import Fraction

from dcp_arbitrary_measurement_witness_reduction import (
    arbitrary_measurement_scaling_record,
    arbitrary_measurement_witness_theorem,
    audit_arbitrary_measurement_reduction,
    audit_physical_measurement_reduction,
    covariant_correlation_seed,
    random_exact_povm,
    run_arbitrary_measurement_witness_reduction,
    physical_uniform_fiber_counterexample,
    write_arbitrary_measurement_witness_reduction_report,
    label_average_success_bound,
    unamplified_reduction_contract,
)


COUNTS = (2, 0, 1, 3, 0, 2, 1, 1)
SUPPORT = tuple(index for index, count in enumerate(COUNTS) if count)


def test_higher_rank_covariant_measurement_yields_average_fiber_filter() -> None:
    phases = np.exp(0.17j * (np.arange(len(SUPPORT)) + 1) ** 2)
    seed = covariant_correlation_seed(
        len(COUNTS),
        len(SUPPORT),
        mixing=0.65,
        phases=phases,
    )
    control = audit_arbitrary_measurement_reduction(
        "HIGHER-RANK",
        COUNTS,
        source_measurement_kind="higher-rank-covariant",
        covariant_seed=seed,
    )
    assert control.higher_rank_effect_verified
    assert not control.initially_noncovariant_measurement
    assert control.qft_diagonal_filter_residual <= 1e-10
    assert control.inverse_filter_residual <= 1e-10
    assert (
        control.uniform_legal_average_target_preparation_probability
        + 1e-10
        >= control.source_measurement_average_success
    )
    assert (
        control.planted_average_target_preparation_probability
        + 1e-10
        >= control.legal_support_to_assignment_ratio
        * control.uniform_legal_average_target_preparation_probability
    )
    assert control.exact_arbitrary_measurement_reduction_verified


def test_random_noncovariant_povm_symmetrizes_without_average_loss() -> None:
    original = random_exact_povm(
        len(COUNTS),
        len(SUPPORT),
        seed=313,
    )
    control = audit_arbitrary_measurement_reduction(
        "NONCOVARIANT",
        COUNTS,
        source_measurement_kind="random-noncovariant",
        original_effects=original,
    )
    assert control.initially_noncovariant_measurement
    assert control.higher_rank_effect_verified
    assert control.source_to_symmetrized_success_residual <= 1e-10
    assert control.symmetrized_success_spread <= 1e-10
    assert control.symmetrized_covariance_residual <= 1e-10
    assert control.exact_arbitrary_measurement_reduction_verified


def test_target_filter_is_a_valid_contraction_even_when_nonuniform() -> None:
    phases = np.exp(0.31j * np.arange(len(SUPPORT)))
    seed = covariant_correlation_seed(
        len(COUNTS),
        len(SUPPORT),
        mixing=0.41,
        phases=phases,
    )
    control = audit_arbitrary_measurement_reduction(
        "NONUNIFORM-FILTER",
        COUNTS,
        source_measurement_kind="nonuniform-higher-rank",
        covariant_seed=seed,
    )
    assert 0 <= control.minimum_target_preparation_probability <= 1
    assert 0 <= control.maximum_target_preparation_probability <= 1 + 1e-10
    assert control.cleaned_subanalysis_contraction_residual <= 1e-10
    assert control.decoding_success_to_filter_mass_residual <= 1e-10
    assert control.planted_average_dominates_scaled_legal_residual <= 1e-10


def test_invalid_covariant_seed_diagonal_fails_completeness() -> None:
    invalid = np.eye(len(SUPPORT)) / (len(COUNTS) + 1)
    control = audit_arbitrary_measurement_reduction(
        "INVALID",
        COUNTS,
        source_measurement_kind="invalid-seed",
        covariant_seed=invalid,
    )
    assert not control.exact_arbitrary_measurement_reduction_verified
    assert control.symmetrized_effect_completeness_residual > 1e-3


def test_inverse_polynomial_measurement_bootstrap_is_polynomial() -> None:
    for power in (0, 2, 4, 8):
        row = arbitrary_measurement_scaling_record(256, power, 8)
        assert row.polynomial_bootstrap
        assert row.one_shot_uniform_legal_witness_success_lower_bound == pytest.approx(
            256.0 ** (-power)
        )
        assert row.actual_circuit_povm_semantics_exact
        assert row.inverse_polynomial_wrapper_precision_sufficient
        assert row.robust_average_witness_success_lower_bound == pytest.approx(
            0.75 * row.decoding_success_lower_bound
        )
        assert row.one_shot_planted_inversion_success_lower_bound == row.decoding_success_lower_bound
        assert row.robust_planted_inversion_success_lower_bound == row.robust_average_witness_success_lower_bound
        assert row.target_precision <= row.decoding_success_lower_bound/128
        assert not row.occupancy_assumption_used
        assert not row.per_target_bounded_error_proved


def test_theorem_scope_keeps_approximation_and_per_target_guarantees_open() -> None:
    theorem = arbitrary_measurement_witness_theorem()
    assert theorem.arbitrary_effect_rank
    assert theorem.initially_noncovariant_measurements
    assert not theorem.pgm_structure_used
    assert theorem.accessible_exact_measurement_route_reduced
    assert theorem.average_planted_inversion_route_reduced
    assert not theorem.approximation_to_ideal_povm_is_loophole
    assert theorem.standard_wrapper_gate_synthesis_robust
    assert not theorem.per_target_bounded_error_proved
    assert not theorem.inaccessible_noisy_channel_reduced


def test_report_closes_exact_measurement_architecture_shortcuts() -> None:
    report = run_arbitrary_measurement_witness_reduction()
    assert report.headline_metrics[
        "arbitrary_exact_measurement_to_witness_theorem_count"
    ] == 1
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.headline_metrics["higher_rank_control_count"] == 4
    assert report.headline_metrics["initially_noncovariant_control_count"] == 2
    assert not report.claim_gate[
        "accessible_exact_higher_rank_measurement_shortcut_open"
    ]
    assert not report.claim_gate[
        "accessible_exact_noncovariant_measurement_shortcut_open"
    ]
    assert not report.claim_gate[
        "approximation_to_ideal_standard_circuit_measurement_is_loophole"
    ]
    assert report.claim_gate["standard_wrapper_gate_synthesis_robust"]
    assert not report.claim_gate["inaccessible_noisy_channel_route_closed"]
    assert not report.claim_gate["speedup_claim_allowed"]
    assert not report.claim_gate["arbitrary_measurement_implies_uniform_fiber_preparation"]
    assert not report.claim_gate["label_average_only_bootstrap_proved"]
    assert not report.claim_gate["novelty_established"]
    assert report.headline_metrics["full_physical_space_control_count"] == 5
    assert report.headline_metrics["uniform_fiber_inference_counterexample_count"] == 1


def test_rational_full_space_counterexample_exactly_refutes_uniform_fibers():
    import sympy as s
    record = physical_uniform_fiber_counterexample()
    exact = record["exact_rational_construction"]
    e0 = s.Matrix(exact["seed_numerators"])/exact["seed_denominator"]
    u = s.diag(1, -1, -1, 1)
    assert e0+u*e0*u == s.eye(4)
    assert set(e0.eigenvals()) == {s.S(0), s.Rational(1, 2), s.S(1)}
    psi = s.ones(4, 1)/2
    success = (psi.T*e0*psi)[0]
    assert success == s.Rational(1, 2)
    eta_density = e0*psi*psi.T*e0
    assert 2*(eta_density[0, 0]+eta_density[3, 3]) == s.Rational(1, 2)
    assert 2*(eta_density[1, 1]+eta_density[2, 2]) == s.Rational(1, 4)
    assert eta_density[3, 3] == 0 and eta_density[0, 0] > 0
    assert record["uniform_fiber_inference_refuted"]
    assert record["planted_witness_success"] == pytest.approx(.375)


@pytest.mark.parametrize("modulus,labels", ((3, (1, 1, 2)), (8, (1,)), (5, (0, 1, 4, 2)), (8, (0,)*6)))
def test_full_physical_povms_preserve_witness_support_not_uniformity(modulus, labels):
    result = audit_physical_measurement_reduction(labels, modulus,
        original_effects=random_exact_povm(modulus, 1 << len(labels), seed=818))
    assert result["verified"]
    assert result["assignment_dimension"] == 1 << len(labels)
    assert result["planted_witness_success"]+1e-9 >= result["both_target_laws_lower_bound"]
    assert result["uniform_all_residues_witness_success"]+1e-9 >= result["source_decoding_success"]**2
    for target, probabilities in result["postselected_basis_probabilities"].items():
        assert sum(probabilities) == pytest.approx(1)
        for bitstring, probability in enumerate(probabilities):
            residue = sum(a*((bitstring >> j) & 1) for j, a in enumerate(labels)) % modulus
            if residue != int(target):
                assert probability < 1e-16


def test_high_multiplicity_needs_no_occupancy_loss():
    result = audit_physical_measurement_reduction((0,)*6, 8,
        covariant_seed=np.eye(64)/8)
    assert result["support_size"] == 1
    assert result["source_decoding_success"] == pytest.approx(1/8)
    assert result["both_target_laws_lower_bound"] == pytest.approx(1/8)
    assert result["planted_witness_success"] == pytest.approx(1/8)
    assert not result["occupancy_assumption_used"]


def test_physical_effects_cannot_be_replaced_by_compressed_effects():
    with pytest.raises(ValueError, match="dimension"):
        audit_physical_measurement_reduction((1, 1), 2, covariant_seed=np.eye(2)/2)
    with pytest.raises(ValueError, match="positive and complete"):
        audit_physical_measurement_reduction((1, 1), 2, covariant_seed=np.eye(4)/3)
    bad = [np.diag([-1., 1, 1, 1]), np.diag([2., 0, 0, 0])]
    with pytest.raises(ValueError, match="positive and complete"):
        audit_physical_measurement_reduction((1, 1), 2, original_effects=bad)


def test_writer_preserves_no_registry_and_custom_identity(tmp_path, monkeypatch):
    import dcp_arbitrary_measurement_witness_reduction as module
    results, negatives = [], []
    monkeypatch.setattr(module, "upsert_experiment_result", results.append)
    monkeypatch.setattr(module, "upsert_negative_result", negatives.append)
    write_arbitrary_measurement_witness_reduction_report(tmp_path/"control.json", write_registry=False)
    assert not results and not negatives
    write_arbitrary_measurement_witness_reduction_report(tmp_path/"live.json",
        registry_experiment_id="EXP-CUSTOM", registry_candidate_id="CAND-CUSTOM", registry_result_id="RESULT-CUSTOM")
    assert results[0].id == "RESULT-CUSTOM" and results[0].experiment_id == "EXP-CUSTOM"
    assert negatives[0].applies_to == ["CAND-CUSTOM"]
    assert "not a DCP no-go" in negatives[0].evidence["scope"]


def test_zero_success_needs_no_branch_normalization():
    seed = np.array([[1., -1.], [-1., 1.]])/2
    result = audit_physical_measurement_reduction((1,), 2, covariant_seed=seed)
    assert result["verified"]
    assert result["source_decoding_success"] == pytest.approx(0)
    assert result["planted_witness_success"] == pytest.approx(0)
    assert result["normalized_uniform_span_leakage_squared"] is None
    assert not result["success_probability_estimation_required"]


def test_unamplified_block_matches_complete_physical_unitary_compute_copy_uncompute():
    from scipy.linalg import null_space
    from dcp_arbitrary_measurement_witness_reduction import _psd_square_root, qft_matrix
    record = physical_uniform_fiber_counterexample()
    exact = record["exact_rational_construction"]
    e0 = np.array(exact["seed_numerators"], dtype=complex)/4
    u = np.diag([1, -1, -1, 1])
    effects = (e0, u@e0@u)
    v = np.vstack([_psd_square_root(e) for e in effects])
    decoder = np.column_stack((v, null_space(v.conj().T)))
    assert np.linalg.norm(decoder.conj().T@decoder-np.eye(8)) < 1e-12
    hadamard = np.array([[1, 1], [1, -1]])/np.sqrt(2)
    prep = np.kron(hadamard, hadamard)
    known_preps = (prep, u@prep)
    block = np.zeros((2, 4), dtype=complex)
    for basis in range(4):
        initial = np.eye(8)[:, basis]
        computed = decoder@initial
        copied = np.zeros((2, 8), dtype=complex)
        for outcome in range(2):
            copied[outcome, outcome*4:(outcome+1)*4] = computed[outcome*4:(outcome+1)*4]
        for outcome in range(2):
            uncomputed = decoder.conj().T@copied[outcome]
            unprepared = np.kron(np.eye(2), known_preps[outcome].conj().T)@uncomputed
            block[outcome, basis] = unprepared[0]
    inverse = block.conj().T@qft_matrix(2).conj().T
    assert np.sum(abs(inverse)**2, axis=0) == pytest.approx([.5, .25])
    assert abs(inverse[3, 0]) < 1e-12
    assert abs(inverse[0, 0])**2 == pytest.approx(.5)


def test_label_average_bound_includes_zero_and_rare_successful_sources():
    result = label_average_success_bound((Fraction(0), Fraction(1)), (Fraction(99, 100), Fraction(1, 100)))
    assert result["jensen_verified"]
    assert result["mean_squared_success"] == "1/100"
    assert result["label_averaged_witness_lower_bound"] == "1/10000"
    contract = unamplified_reduction_contract()
    assert contract["decoder_or_inverse_calls_per_attempt"] == 2
    assert not contract["amplitude_amplification_required"]
    assert not contract["success_estimation_required"]
    assert not contract["free_postselection"]
    with pytest.raises(ValueError):
        label_average_success_bound((.5,), (Fraction(1),))
    with pytest.raises(ValueError):
        label_average_success_bound((Fraction(1),), (Fraction(1, 2),))


def test_live_registry_runner_and_proof_gates_preserve_retraction(tmp_path, monkeypatch):
    import json
    from experiment_runner import run_experiment
    from proof_tracker import _dcp_physical_witness_lemmas
    from dequantization_checks import build_dequantization_report
    from research_registry import initialize_seed_registry, load_experiment_results, validate_registry
    monkeypatch.chdir(tmp_path)
    initialize_seed_registry(overwrite=False)
    payload = write_arbitrary_measurement_witness_reduction_report()
    experiment = "EXP-DHS-DCP-ARBITRARY-MEASUREMENT-WITNESS-REDUCTION"
    for _ in range(2):
        assert run_experiment(experiment).status == "completed"
    assert len([r for r in load_experiment_results() if r["experiment_id"] == experiment]) == 1
    assert validate_registry()["valid"]
    assert any(r["id"].endswith("DCP-PHYSICAL-WITNESS-NOT-UNIFORM-FIBER")
               for r in build_dequantization_report()["findings"])
    assert all(r.status.startswith("derived") for r in _dcp_physical_witness_lemmas("CODE-COSET-COLLECTIVE"))
    payload["claim_gate"]["unamplified_label_average_success_transfer_derived"] = 1
    from pathlib import Path
    Path("research/reductions/dcp_arbitrary_measurement_witness_reduction.json").write_text(json.dumps(payload))
    assert _dcp_physical_witness_lemmas("CODE-COSET-COLLECTIVE")[1].status.startswith("blocked")


def test_decoder_can_mix_quantum_label_workspace_without_free_inverse_compression():
    from dcp_arbitrary_measurement_witness_reduction import qft_matrix
    rng = np.random.default_rng(911)
    decoder, _ = np.linalg.qr(rng.normal(size=(16, 16))+1j*rng.normal(size=(16, 16)))
    h = np.array([[1, 1], [1, -1]])/np.sqrt(2)
    x_gate = np.array([[0, 1], [1, 0]])
    prep = np.kron(h, h)
    source_successes, witness_successes = [], []
    for label, coefficients in enumerate(((1, 1), (1, 0))):
        residues = np.array([sum(a*((b >> j) & 1) for j, a in enumerate(coefficients)) % 2 for b in range(4)])
        phase = np.diag((-1.)**residues)
        # Order R,O,L,A: random twirl, outcome, quantum label, two assignment bits.
        initialize_label = np.kron(np.eye(2), np.kron(x_gate if label else np.eye(2), np.eye(4)))
        twirl_phase = np.diag(np.concatenate((np.ones(16), np.tile((-1.)**residues, 4))))
        correction = np.zeros((32, 32))
        for i in range(32):
            r, o, rest = i//16, (i//8) % 2, i % 8
            correction[r*16+(o ^ r)*8+rest, i] = 1
        physical = (correction @ np.kron(np.eye(2), decoder) @ twirl_phase
                    @ np.kron(h, np.eye(16)) @ np.kron(np.eye(2), initialize_label))
        assert np.linalg.norm(physical.conj().T@physical-np.eye(32)) < 1e-12
        outcome = (np.arange(32)//8) % 2
        embedding = physical[:, :4]
        effects = [embedding.conj().T@(embedding*(outcome == d)[:, None]) for d in range(2)]
        known_preps = (prep, phase@prep)
        actual = np.zeros((2, 4), dtype=complex)
        for b in range(4):
            for d in range(2):
                copied_branch = embedding[:, b]*(outcome == d)
                uncomputed = physical.conj().T@copied_branch
                unprepared = np.kron(np.eye(8), known_preps[d].conj().T)@uncomputed
                actual[d, b] = unprepared[0]
        predicted = np.vstack([known_preps[d][:, 0].conj()@effects[d] for d in range(2)])
        assert np.linalg.norm(actual-predicted) < 1e-12
        inverse = actual.conj().T@qft_matrix(2).conj().T
        assert np.linalg.norm(inverse*(residues[:, None] != np.arange(2))) < 1e-12
        success = float(np.vdot(prep[:, 0], effects[0]@prep[:, 0]).real)
        law = np.bincount(residues, minlength=2)/4
        witness = float(law@np.sum(abs(inverse)**2, axis=0))
        assert witness+1e-12 >= success**2
        source_successes.append(success)
        witness_successes.append(witness)
        original_input = initialize_label[:, :4]@prep[:, 0]
        output = decoder@original_input
        assert np.sum(abs(output[((np.arange(16)//4) % 2) != label])**2) > .1
    assert np.mean(witness_successes)+1e-12 >= np.mean(source_successes)**2
