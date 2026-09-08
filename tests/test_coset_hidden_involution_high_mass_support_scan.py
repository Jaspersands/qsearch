import json
from pathlib import Path

import numpy as np
import pytest
import proof_tracker

from coset_hidden_involution_high_mass_support_scan import (
    SUPPORT_FOUR_PRIORITY,
    TARGET_ALPHA,
    TARGET_BETA,
    TARGET_HALF_DEGREE,
    TARGET_SYMMETRIC_PARTITION,
    _target_source_mass,
    _load_checkpoint,
    _write_checkpoint,
    separator_commutant_certificate,
)
from coset_hidden_involution_multiplicity_fiber_trace import (
    isolate_root_multiplicity_fiber,
)


def test_simple_separator_connected_graph_certifies_full_star_algebra() -> None:
    diagonal = np.diag([-1.0, 0.0, 2.0])
    path = np.array(
        [
            [0.0, 1.0, 0.0],
            [1.0, 0.0, 1.0],
            [0.0, 1.0, 0.0],
        ]
    )
    certificate = separator_commutant_certificate(
        [diagonal, path],
        search_trials=32,
    )
    assert certificate.scalar_common_commutant_numerically_certified is True
    assert certificate.inferred_full_star_algebra_dimension == 9
    assert certificate.minimum_separator_eigenvalue_gap > 0.1
    assert certificate.maximum_spanning_tree_bottleneck > 0.1
    assert certificate.direct_commutant_nullity_at_1e8 == 1
    assert certificate.direct_commutant_smallest_nonzero_singular_value > 0.1


def test_disconnected_diagonal_generators_do_not_pass_commutant_gate() -> None:
    diagonal = np.diag([-1.0, 0.0, 2.0])
    certificate = separator_commutant_certificate(
        [diagonal, np.eye(3)],
        search_trials=32,
    )
    assert certificate.scalar_common_commutant_numerically_certified is False
    assert certificate.joint_generator_graph_component_count_at_1e8 == 3
    assert certificate.direct_commutant_nullity_at_1e8 == 3
    assert certificate.inferred_full_star_algebra_dimension == 0


def test_target_is_high_multiplicity_and_has_nontrivial_source_mass() -> None:
    numerator, denominator, probability, repeated_fraction = _target_source_mass()
    assert numerator == 758918160
    assert denominator == 87178291200
    assert abs(probability - 0.008705357142857143) <= 1e-16
    assert repeated_fraction > 0.0088
    fiber = isolate_root_multiplicity_fiber(
        TARGET_HALF_DEGREE,
        TARGET_SYMMETRIC_PARTITION,
        TARGET_ALPHA,
        TARGET_BETA,
    )
    assert fiber.symmetric_irrep_dimension == 69498
    assert fiber.branching_multiplicity == 26
    assert fiber.carrier_weight_dimension == 6
    assert fiber.maximum_signed_weight_residual <= 1e-11
    assert fiber.maximum_yjm_content_residual <= 1e-11


def test_support_four_witness_schedule_is_deterministic_and_complete() -> None:
    assert SUPPORT_FOUR_PRIORITY == (6, 10, 11, 12, 5, 7, 8, 9, 13, 14)
    assert len(set(SUPPORT_FOUR_PRIORITY)) == 10


def test_proof_tracker_keeps_finite_closure_separate_from_typical_theorem(
    tmp_path: Path,
    monkeypatch,
) -> None:
    artifact = tmp_path / "high-mass-support-scan.json"
    artifact.write_text(
        json.dumps(
            {
                "claim_gate": {
                    "highest_mass_untested_s14_block_scanned": True,
                    "support_four_full_copy_algebra_numerically_certified": True,
                    "one_minus_o_one_natural_mass_coverage_proved": False,
                    "inverse_polynomial_normalized_gap_proved": False,
                },
                "headline_metrics": {
                    "support_four_direct_commutant_nullity": 1,
                    "support_four_direct_commutant_smallest_nonzero_singular_value": 0.22,
                },
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(proof_tracker, "HIGH_MASS_SUPPORT_SCAN_PATH", artifact)
    lemmas = {
        lemma.id: lemma
        for lemma in proof_tracker._high_mass_support_scan_lemmas(
            "CODE-COSET-COLLECTIVE"
        )
    }
    assert lemmas[
        "LEMMA-CODE-COSET-COLLECTIVE-HIGH-MASS-S14-SUPPORT-FOUR-CLOSURE"
    ].status.startswith("numerically-supported-")
    assert lemmas[
        "LEMMA-CODE-COSET-COLLECTIVE-TYPICAL-LOW-SUPPORT-GAPPED-COMMUTANT"
    ].status == "blocked-one-finite-block-no-mass-or-gap-scaling-theorem"


def test_complex_hermitian_certificate_replays_coefficients_and_cost():
    x = np.array([[0, 1], [1, 0]], dtype=complex)
    y = np.array([[0, -1j], [1j, 0]])
    cert = separator_commutant_certificate([x, y], search_trials=4)
    separator = sum(c * a for c, a in zip(cert.separator_coefficients, [x, y]))
    assert cert.scalar_common_commutant_numerically_certified
    assert np.isclose(np.diff(np.linalg.eigvalsh(separator))[0], cert.minimum_separator_eigenvalue_gap)
    assert cert.lcu_normalized_minimum_gap <= 2 + 1e-12
    # Tiny compressed norms cannot be treated as free coherent amplification.
    tiny = separator_commutant_certificate([x * 0.001, y * 0.001], search_trials=4)
    assert tiny.lcu_normalized_minimum_gap < 0.002


@pytest.mark.parametrize("matrices", [[np.eye(1)], [np.array([[0, 1], [0, 0]])],
                                      [np.diag([float("nan"), 1])], [np.ones(2)]])
def test_invalid_certificate_inputs_fail_closed(matrices):
    with pytest.raises(ValueError):
        separator_commutant_certificate(matrices)


def test_checkpoint_requires_provenance_and_rejects_bad_payload(tmp_path):
    path = tmp_path / "matrices.npz"
    provenance = {"branch": [2, 1], "gauge": "original", "schema": 2}
    matrices = {"p_0_1": np.eye(2)}
    _write_checkpoint(path, matrices, provenance)
    np.testing.assert_array_equal(_load_checkpoint(path, 2, provenance)["p_0_1"], np.eye(2))
    assert not _load_checkpoint(path, 2, {**provenance, "gauge": "changed"})
    assert not _load_checkpoint(path, 3, provenance)
    np.savez_compressed(path, **matrices)
    assert not _load_checkpoint(path, 2, provenance)
    _write_checkpoint(path, {"p_0_1": np.diag([float("nan"), 1])}, provenance)
    assert not _load_checkpoint(path, 2, provenance)
