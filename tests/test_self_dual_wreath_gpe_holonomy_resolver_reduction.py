import math

import numpy as np

from self_dual_wreath_gpe_holonomy_resolver_reduction import (
    audit_holonomy_fixed_space_reduction,
    fixed_space_hamiltonian,
    near_flat_holonomy_counterexample,
    rotation,
    run_gpe_holonomy_resolver_reduction,
)


def test_flat_triangle_has_full_covariantly_constant_fiber():
    first = rotation(0.2)
    second = rotation(-0.37)
    row = audit_holonomy_fixed_space_reduction(
        "flat",
        3,
        {
            (0, 1): first,
            (1, 2): second,
            (0, 2): second @ first,
        },
        ((0, 1), (1, 2)),
    )
    assert row.exact_holonomy_fixed_space_reduction_verified
    assert row.connection_kernel_dimension == 2
    assert row.holonomy_fixed_space_dimension == 2


def test_nontrivial_holonomy_fixed_space_matches_connection_kernel():
    identity = np.eye(3, dtype=complex)
    chord = np.zeros((3, 3), dtype=complex)
    chord[0, 0] = 1
    chord[1:, 1:] = rotation(0.61)
    row = audit_holonomy_fixed_space_reduction(
        "partial",
        3,
        {(0, 1): identity, (1, 2): identity, (0, 2): chord},
        ((0, 1), (1, 2)),
    )
    assert row.exact_holonomy_fixed_space_reduction_verified
    assert row.connection_kernel_dimension == 1
    assert row.holonomy_fixed_space_dimension == 1


def test_fixed_space_hamiltonian_has_expected_rotation_gap():
    angle = 0.125
    hamiltonian = fixed_space_hamiltonian((rotation(angle),))
    eigenvalues = np.linalg.eigvalsh(hamiltonian)
    expected = math.sin(angle / 2) ** 2
    assert np.max(np.abs(eigenvalues - expected)) < 1e-12


def test_succinct_near_flat_holonomy_can_have_exponentially_small_gap():
    early = near_flat_holonomy_counterexample(6)
    late = near_flat_holonomy_counterexample(18)
    assert early.pair_transport_is_exact_unitary
    assert late.pair_transport_is_exact_unitary
    assert late.fixed_space_hamiltonian_gap < early.fixed_space_hamiltonian_gap
    assert late.inverse_gap_log2 > early.inverse_gap_log2 + 20
    assert not late.inverse_polynomial_gap_guaranteed


def test_report_keeps_natural_gap_and_recursive_coverage_open():
    report = run_gpe_holonomy_resolver_reduction()
    gate = report.claim_gate
    assert gate["pair_racah_holonomies_implicitly_executable"]
    assert gate["flat_connection_kernel_equals_holonomy_fixed_space_proved"]
    assert gate["polynomial_resolver_conditional_on_select_and_gap"]
    assert not gate["natural_coherent_holonomy_generator_select_proved"]
    assert not gate["natural_inverse_polynomial_holonomy_gap_proved"]
    assert not gate["partial_support_and_emergent_dependencies_resolved"]
    assert not gate["complete_higher_order_relative_polar_proved"]
    assert not gate["hidden_permutation_decoder_proved"]
    assert not gate["speedup_claim_allowed"]
