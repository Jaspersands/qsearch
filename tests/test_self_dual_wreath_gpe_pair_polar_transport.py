import numpy as np

from self_dual_wreath_gpe_pair_polar_transport import (
    audit_gpe_carrier_reassociation,
    gpe_decode_three_carriers,
    gpe_encode_three_carriers,
    gpe_pair_transport_scaling_record,
    gpe_row_swap_reassociation,
    pair_invariant_bases,
    run_gpe_pair_polar_transport,
)


def test_pair_cross_overlap_is_inverse_dimension_times_reassociation():
    for dimension in range(1, 6):
        row = audit_gpe_carrier_reassociation(dimension)
        assert row.exact_pair_polar_reassociation_verified
        assert row.cross_overlap_factorization_residual < 1e-8
        assert row.polar_reassociation_residual < 1e-8


def test_gpe_normal_form_is_an_isometry_on_three_carriers():
    dimension = 3
    rng = np.random.default_rng(901)
    state = rng.normal(size=(dimension,) * 3) + 1j * rng.normal(
        size=(dimension,) * 3
    )
    state /= np.linalg.norm(state)
    encoded = gpe_encode_three_carriers(state)
    decoded = gpe_decode_three_carriers(encoded)
    assert abs(np.linalg.norm(encoded) - 1.0) < 1e-10
    assert np.linalg.norm(decoded - state) < 1e-10


def test_coherent_gpe_row_swap_reassociates_entanglement():
    for dimension in (2, 3):
        target, source = pair_invariant_bases(dimension)
        for free_index in range(dimension):
            source_state = source[:, free_index].reshape((dimension,) * 3)
            expected_target = target[:, free_index].reshape((dimension,) * 3)
            actual = gpe_row_swap_reassociation(source_state)
            assert np.linalg.norm(actual - expected_target) < 1e-10


def test_pair_transport_scaling_has_no_inverse_dimension_dependency():
    row = gpe_pair_transport_scaling_record(128)
    assert row.generalized_phase_estimation_call_count == 3
    assert row.generalized_phase_estimation_inverse_call_count == 3
    assert row.equality_controlled_carrier_swap_count == 1
    assert not row.normalized_cross_overlap_qsvt_required
    assert not row.full_kronecker_transform_required
    assert row.direct_pair_polar_polynomial
    assert not row.complete_orientation_polar_polynomial


def test_report_moves_bottleneck_to_higher_order_frame_composition():
    report = run_gpe_pair_polar_transport()
    gate = report.claim_gate
    assert gate["exact_pair_cross_overlap_polar_factorization_proved"]
    assert gate["coherent_gpe_carrier_export_proved"]
    assert gate["pair_polar_avoids_inverse_carrier_dimension"]
    assert gate["uniform_polynomial_pair_polar_circuit_proved"]
    assert not gate["full_kronecker_transform_required"]
    assert not gate["higher_level_relative_polar_circuit_proved"]
    assert not gate["complete_many_orientation_pgm_polar_proved"]
    assert not gate["hidden_permutation_decoder_proved"]
    assert not gate["speedup_claim_allowed"]
