from pathlib import Path

import proof_tracker

from coset_hidden_involution_multiplicity_fiber_trace import (
    _validate_against_commutant_projection,
    _validate_against_full_k4_twirl,
    isolate_root_multiplicity_fiber,
    propagate_stabilizer_tableau_fibers,
    run_multiplicity_fiber_trace,
    write_multiplicity_fiber_trace_report,
)


def test_direct_signed_yjm_projection_isolates_exact_copy_fiber() -> None:
    fiber = isolate_root_multiplicity_fiber(
        4,
        (4, 2, 2),
        (2,),
        (2,),
    )
    assert fiber.symmetric_irrep_dimension == 56
    assert fiber.branching_multiplicity == 2
    assert fiber.root_fiber_dimension == 2
    assert fiber.carrier_weight_dimension == 1
    assert fiber.maximum_signed_weight_residual <= 1e-12
    assert fiber.maximum_yjm_content_residual <= 1e-12
    assert fiber.orthonormality_residual <= 1e-12


def test_tableau_propagation_preserves_common_copy_gauge() -> None:
    fibers, propagation_residual, orthogonality_residual = (
        propagate_stabilizer_tableau_fibers(
            7,
            (10, 2, 2),
            (4, 1),
            (2,),
        )
    )
    assert len(fibers) == 4
    assert all(fiber.shape == (1365, 2) for fiber in fibers)
    assert propagation_residual <= 1e-12
    assert orthogonality_residual <= 1e-10


def test_fiber_trace_matches_explicit_full_group_twirl() -> None:
    validation = _validate_against_full_k4_twirl()
    assert validation.validation_passed is True
    assert validation.equal_weight_character_count == 6
    assert validation.full_carrier_dimension == 6
    assert validation.exact_reference_residual <= 1e-12


def test_fiber_trace_matches_independent_s14_commutant_projection() -> None:
    validation = _validate_against_commutant_projection()
    assert validation.validation_passed is True
    assert validation.branching_multiplicity == 2
    assert validation.full_carrier_dimension == 84
    assert validation.exact_reference_residual <= 1e-12


def test_report_keeps_typical_compression_and_decoder_claims_blocked() -> None:
    report = run_multiplicity_fiber_trace()
    assert report.theorem.theorem_verified is True
    assert report.theorem.polynomial_ambient_compression_proved is False
    assert report.theorem.coherent_multiplicity_transform_compiled is False
    assert report.claim_gate["normalized_gap_on_natural_mass_proved"] is False
    assert report.claim_gate["hidden_involution_decoder_compiled"] is False
    assert report.claim_gate["speedup_claim_allowed"] is False


def test_writer_emits_validated_artifact_without_registry(tmp_path: Path) -> None:
    output = tmp_path / "multiplicity-fiber-trace.json"
    payload = write_multiplicity_fiber_trace_report(
        output,
        write_registry=False,
    )
    assert output.exists()
    assert payload["status"] == (
        "matrix-free-copy-fiber-trace-validated-typical-ambient-scaling-open"
    )
    assert payload["headline_metrics"][
        "carrier_partial_trace_full_twirl_validation_count"
    ] == 1
    assert payload["headline_metrics"][
        "polynomial_typical_ambient_compression_theorem_count"
    ] == 0


def test_proof_tracker_proves_trace_but_blocks_typical_compression(
    tmp_path: Path,
    monkeypatch,
) -> None:
    output = tmp_path / "multiplicity-fiber-trace.json"
    write_multiplicity_fiber_trace_report(output, write_registry=False)
    monkeypatch.setattr(proof_tracker, "MULTIPLICITY_FIBER_TRACE_PATH", output)
    lemmas = {
        lemma.id: lemma
        for lemma in proof_tracker._multiplicity_fiber_trace_lemmas(
            "CODE-COSET-COLLECTIVE"
        )
    }
    assert lemmas[
        "LEMMA-CODE-COSET-COLLECTIVE-MULTIPLICITY-FIBER-PARTIAL-TRACE"
    ].status.startswith("proved-")
    assert lemmas[
        "LEMMA-CODE-COSET-COLLECTIVE-TYPICAL-MULTIPLICITY-FIBER-COMPRESSION"
    ].status == "blocked-exponential-ambient-specht-rows-remain"
