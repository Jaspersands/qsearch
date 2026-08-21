import math

import numpy as np

from self_dual_wreath_point_critical_identity_atom import (
    audit_critical_identity_atom,
    build_critical_identity_atom_report,
    critical_identity_atom_scaling_record,
    identity_atom_channel,
    measured_point_channel,
)
from self_dual_wreath_point_stabilizer_quotient import point_quotient_states


THRESHOLD_LABELS = (
    ((3,), (2, 1)),
    ((3,), (1, 1, 1)),
    ((2, 1), (1, 1, 1)),
)


def test_measured_channel_matches_exact_point_state_diagonal():
    measured = measured_point_channel(THRESHOLD_LABELS)
    states = point_quotient_states(THRESHOLD_LABELS, point=2)
    diagonal = np.stack(tuple(np.diag(state).real for state in states))
    assert np.max(np.abs(measured - diagonal)) < 1e-10


def test_identity_atom_is_a_nonnegative_factorial_mass_subchannel():
    measured = measured_point_channel(THRESHOLD_LABELS)
    atom = identity_atom_channel(3, len(THRESHOLD_LABELS))
    assert np.min(measured - atom) > -1e-12
    assert np.allclose(np.sum(atom, axis=1), 1 / math.factorial(3))


def test_atom_energy_relative_collision_and_operational_success_are_exact():
    control = audit_critical_identity_atom(
        3,
        THRESHOLD_LABELS,
        control_id="TEST-W3",
    )
    assert control.exact_identity_atom_channel_verified
    assert math.isclose(
        control.atom_minus_identity_witness_energy,
        (control.n - 1) / control.group_order**2,
    )
    assert math.isclose(
        control.atom_relative_collision,
        (control.n - 1) / control.group_order,
    )
    assert math.isclose(
        control.atom_completed_optimal_success,
        1 / control.n + (control.n - 1) / (control.n * control.group_order),
    )


def test_critical_annealed_energy_is_atom_dominated_but_residual_stays_open():
    records = [critical_identity_atom_scaling_record(n) for n in (16, 32, 64, 128)]
    assert all(row.annealed_critical_ambient_energy_atom_dominated for row in records)
    assert all(row.atom_operational_excess_superpolynomially_small for row in records)
    assert all(
        right.total_energy_distance_from_atom_log2_upper_bound
        < left.total_energy_distance_from_atom_log2_upper_bound
        for left, right in zip(records, records[1:])
    )
    assert all(not row.residual_relative_collision_controlled for row in records)


def test_report_rejects_identity_witness_without_overclaiming_full_no_go():
    report = build_critical_identity_atom_report()
    assert report.theorem.theorem_verified
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["critical_identity_witness_physical_atom_identified"]
    assert report.claim_gate["annealed_critical_ambient_energy_atom_dominated"]
    assert not report.claim_gate["critical_identity_energy_is_algorithmic_evidence"]
    assert not report.claim_gate["residual_relative_collision_controlled"]
    assert not report.claim_gate["critical_harmonic_point_measurement_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]
