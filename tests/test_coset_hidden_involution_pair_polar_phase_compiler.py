import math

import numpy as np
import pytest

from coset_hidden_involution_pair_polar_phase_compiler import (
    audit_pair_polar_control,
    build_pair_polar_phase_report,
    dihedral_reflection_pair,
    pair_polar_scaling_record,
    phase_compiled_pair_polar,
    predicted_principal_cosines,
    smallest_positive_principal_cosine,
    svd_partial_polar,
    write_pair_polar_phase_report,
)


@pytest.mark.parametrize("rotation_order", (3, 4, 5, 8, 11))
def test_exact_dihedral_spectrum_and_half_phase_polar(rotation_order):
    row = audit_pair_polar_control(rotation_order)
    assert row.exact_phase_polar_verified
    assert row.observed_partial_polar_rank == row.predicted_partial_polar_rank
    assert row.phase_pi_kernel_dimension == (
        1 if rotation_order % 2 == 0 else 0
    )
    assert row.maximum_principal_spectrum_residual < 1e-10
    assert row.phase_half_rotation_polar_residual < 1e-10
    assert row.initial_support_residual < 1e-10
    assert row.final_support_residual < 1e-10


def test_smallest_principal_cosine_can_be_inverse_order():
    assert smallest_positive_principal_cosine(4) == pytest.approx(
        math.sin(math.pi / 4)
    )
    assert smallest_positive_principal_cosine(8) == pytest.approx(
        math.sin(math.pi / 8)
    )
    assert smallest_positive_principal_cosine(9) == pytest.approx(
        math.sin(math.pi / 18)
    )
    assert len(predicted_principal_cosines(11)) == 11
    with pytest.raises(ValueError, match="at least two"):
        predicted_principal_cosines(1)


def test_pair_partial_polar_tensorizes_exactly():
    first, second = dihedral_reflection_pair(3)
    pair_polar, first_plus, second_plus = phase_compiled_pair_polar(
        first, second
    )
    direct_tensor = svd_partial_polar(
        np.kron(second_plus @ first_plus, second_plus @ first_plus)
    )
    assert np.linalg.norm(
        direct_tensor - np.kron(pair_polar, pair_polar), ord=2
    ) < 1e-9


def test_phase_resolution_is_logarithmic_while_inverse_gap_grows():
    rows = [
        pair_polar_scaling_record(order)
        for order in (16, 64, 256, 1024, 4096)
    ]
    assert all(row.phase_compiler_polynomial_in_log_order for row in rows)
    assert all(
        row.tensor_pair_polar_polynomial_in_copy_count_and_log_order
        for row in rows
    )
    assert all(
        row.generic_polynomial_cost_superpolynomial_in_log_order
        for row in rows[-2:]
    )
    assert all(
        later.generic_inverse_gap_scale > earlier.generic_inverse_gap_scale
        for earlier, later in zip(rows, rows[1:])
    )
    assert rows[-1].generic_inverse_gap_scale > 1000
    assert rows[-1].phase_resolution_bits < 40
    assert all(not row.global_orbit_synthesis_polar_compiled for row in rows)

    with pytest.raises(ValueError, match="target_error"):
        pair_polar_scaling_record(8, target_error=1.0)
    with pytest.raises(ValueError, match="positive"):
        pair_polar_scaling_record(8, tensor_copy_count=0)


def test_report_compiles_pairs_but_not_global_orbit_polar(tmp_path):
    report = build_pair_polar_phase_report(
        finite_orders=(3, 4, 5, 8),
        scaling_orders=(16, 64, 256, 1024),
    )
    assert report.theorem.theorem_verified
    assert report.theorem.exact_pair_polar_formula_proved
    assert report.theorem.exact_dihedral_spectrum_proved
    assert report.theorem.logarithmic_phase_compiler_constructed
    assert report.theorem.tensor_pair_polar_compiler_constructed
    assert not report.theorem.full_orbit_polar_compiler_constructed
    assert not report.theorem.arbitrary_circuit_lower_bound_proved
    assert report.claim_gate["pair_polar_polynomial_phase_compiler_constructed"]
    assert not report.claim_gate["global_pair_consistency_proved"]
    assert not report.claim_gate["full_orbit_synthesis_polar_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_pair_polar_phase_report(
        tmp_path / "pair-polar.json",
        finite_orders=(3, 4, 5),
        scaling_orders=(16, 64),
    )
    assert payload["status"] == (
        "pair-polar-phase-compiler-proved-global-orbit-polar-open"
    )
    assert payload["headline_metrics"][
        "logarithmic_phase_compiler_count"
    ] == 1
