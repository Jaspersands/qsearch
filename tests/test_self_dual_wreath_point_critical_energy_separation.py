import math

import numpy as np

from self_dual_wreath_point_critical_energy_separation import (
    audit_critical_energy_separation,
    build_critical_energy_separation_report,
    classical_point_ensemble_metrics,
    critical_energy_scaling_record,
    critical_register_parameters,
    flat_partition_probabilities,
    spiky_simplex_probabilities,
)


def test_two_covariant_commuting_families_have_identical_critical_energy():
    n = 4
    dimension = critical_register_parameters(n)[2]
    control = audit_critical_energy_separation(n, dimension)
    assert control.same_energy_opposite_operational_behavior_verified
    assert math.isclose(control.common_normalized_energy, n - 1)
    assert control.normalized_energy_residual < 1e-10


def test_flat_family_is_perfect_while_spiky_family_has_exact_small_success():
    n = 3
    dimension = critical_register_parameters(n)[2]
    flat = classical_point_ensemble_metrics(
        flat_partition_probabilities(n, dimension),
        family="flat",
    )
    spiky = classical_point_ensemble_metrics(
        spiky_simplex_probabilities(n, dimension),
        family="spiky",
    )
    assert math.isclose(flat.optimal_success_probability, 1.0)
    assert math.isclose(flat.average_relative_collision, n - 1)
    assert math.isclose(
        spiky.optimal_success_probability,
        1 / n + (n - 1) / math.sqrt(n * dimension),
    )
    assert math.isclose(
        spiky.average_relative_collision,
        n * (n - 1) / dimension,
    )
    assert flat.optimal_success_probability > spiky.optimal_success_probability


def test_general_uniform_ensemble_pgm_relative_collision_identity():
    probabilities = np.asarray(
        [
            [0.55, 0.25, 0.20],
            [0.10, 0.65, 0.25],
            [0.30, 0.20, 0.50],
        ]
    )
    metrics = classical_point_ensemble_metrics(probabilities, family="generic")
    average = np.mean(probabilities, axis=0)
    direct_pgm = np.sum(probabilities * probabilities / average) / 9
    assert math.isclose(metrics.pgm_success_probability, direct_pgm)


def test_spiky_critical_excess_is_superpolynomial_at_scaling_ranks():
    records = [critical_energy_scaling_record(n) for n in (16, 32, 64, 128)]
    assert all(row.spiky_excess_superpolynomially_small for row in records)
    assert all(
        right.spiky_optimal_excess_log2 < left.spiky_optimal_excess_log2
        for left, right in zip(records, records[1:])
    )


def test_report_preserves_natural_relative_spectrum_claim_gates():
    report = build_critical_energy_separation_report()
    assert report.theorem.theorem_verified
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["relative_collision_is_correct_pgm_scalar"]
    assert not report.claim_gate["critical_ambient_energy_determines_point_advantage"]
    assert not report.claim_gate["natural_critical_relative_collision_proved"]
    assert not report.claim_gate["critical_harmonic_naimark_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]
