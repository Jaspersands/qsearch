import pytest

from dcp_carry_packets import compile_packet
from dcp_boolean_phase_pullback import (
    BooleanANFMap, _complete_pullback_control, _physical_instrument_controls,
    canonical_label_sign_orbits, consumed_program_plan, packet_pullback_functions,
    pullback_source_gate, sign_orbit_selector_certificate, signed_label_update,
    _selector_source_controls, source_universal_product_gate,
)


def test_actual_program_instrument_is_proportional_to_unitary_for_all_phases():
    rows = _physical_instrument_controls()
    assert [row["exact_density_phase_identities"] for row in rows] == [64, 128, 1024]
    assert all(row["target_can_be_entangled_with_an_untouched_reference"] for row in rows)


def test_nonlinear_many_to_one_pullback_keeps_every_program_outcome():
    row = _complete_pullback_control()
    assert row["exact_branch_and_packet_pullback_checks"] == 16384
    assert not row["map_is_injective"]
    assert not row["public_map_inverse_required"]
    plan = row["resource_plan"]
    assert plan["program_phase_states_consumed"] == 3
    assert plan["all_outcomes_kept"]
    assert not plan["same_program_or_phase_function_reusable"]
    assert not plan["unknown_residue_decoder"]


def test_public_anf_composition_and_resources_scale_without_truth_tables():
    public_map = BooleanANFMap(64, ((1,), (1 << 63,), (1 | (1 << 63),)))
    assert public_map.evaluate(1 | (1 << 63)) == (1, 1, 1)
    assert public_map.evaluate(1) == (1, 0, 0)
    resources = public_map.resource_upper_bound()
    assert resources["description_size_monomials"] == 3
    assert resources["maximum_anf_degree"] == 2
    assert resources["compute_uncompute_toffoli_upper_bound"] == 4
    assert resources["reusable_clean_work_qubits_upper_bound"] == 2
    assert not resources["physical_gate_backend_exported"]


def test_program_measurement_sign_is_a_label_update_not_an_unknown_rotation():
    labels = ((1, 2, 3), (4, 5, 6))
    assert signed_label_update(labels, 8, 5) == ((7, 2, 5), (4, 5, 2))
    packet = compile_packet(labels, 8)
    updated = compile_packet(signed_label_update(labels, 8, 5), 8)
    assert packet.kernel_rows == updated.kernel_rows


def test_boolean_kernel_compiler_cancels_duplicate_monomials():
    packet = compile_packet([[1, 1, 1]], 8)
    functions = packet_pullback_functions(packet, BooleanANFMap(2, ((1, 3), (3,))))
    assert functions.outputs == ((1,), (1, 3), (3,))
    for z in range(4):
        assert sum(functions.evaluate(z)) % 2 == 0


def test_source_gate_rejects_high_bit_selection_and_free_oracle_reuse():
    kwargs = {"functions_selected_from_low_labels_or_prior_only": True,
              "current_higher_labels_native_iid": True,
              "independent_phase_only_programs": True, "each_program_consumed_once": True}
    row = pullback_source_gate(**kwargs)
    assert row["native_updated_source_certified_as_declared"]
    assert not row["declarations_programmatically_proven"]
    assert not row["repeated_same_function_queries_available"]
    for key in kwargs:
        assert not pullback_source_gate(**{**kwargs, key: False})["native_updated_source_certified_as_declared"]
    assert not pullback_source_gate(**kwargs, outcome_conditioning_or_rejection=True)["native_updated_source_certified_as_declared"]


def test_invalid_public_maps_and_program_resource_mismatches_are_rejected():
    for outputs in (((1, 1),), ((4,),), ((-1,),)):
        with pytest.raises(ValueError):
            BooleanANFMap(2, outputs)
    functions = BooleanANFMap(2, ((1,), (3,)))
    with pytest.raises(ValueError):
        consumed_program_plan([[1]], 8, functions)
    with pytest.raises(ValueError):
        consumed_program_plan([[1, 2]], 7, functions)
    with pytest.raises(ValueError):
        packet_pullback_functions(compile_packet([[1, 1]], 8), functions)
    with pytest.raises(ValueError):
        signed_label_update([[1]], 8, 2)


def test_high_label_sign_covariance_is_a_legal_escape_not_uniform_conditional_high_bits():
    labels = [[1, 3, 4], [2, 5, 0]]
    canonical = canonical_label_sign_orbits(labels, 8)
    for b in range(8):
        assert canonical_label_sign_orbits(signed_label_update(labels, 8, b), 8) == canonical
    row = sign_orbit_selector_certificate(labels, 8)
    assert row["conditional_column_orbit_sizes"] == [2, 2, 1]
    assert row["native_unconditional_updated_label_law_preserved"]
    assert not row["conditional_higher_labels_are_iid_uniform"]
    assert not row["old_fixed_low_chart_high_label_moment_theorem_automatically_usable"]
    controls = _selector_source_controls()
    assert controls["safe_sign_orbit_selected_3_counts"] == [0, 0, 0, 2, 0, 2, 0, 0]
    assert controls["unsafe_original_label_less_than_4_counts"] != [1] * 8


def test_every_two_bit_boolean_function_matches_the_exact_product_criterion():
    admitted = 0
    for mask in range(16):
        terms = tuple(i for i in range(4) if mask >> i & 1)
        functions = BooleanANFMap(2, (terms,))
        values = [functions.evaluate(z)[0] for z in range(4)]
        mixed = values[3] - values[1] - values[2] + values[0]
        row = source_universal_product_gate(functions, 8)
        # An original higher-label increment by2 gives phase exp(i*pi*f/2).
        assert row["source_universal_phase_product"] == (mixed % 4 == 0)
        admitted += row["source_universal_phase_product"]
    assert admitted == 6
    parity = BooleanANFMap(64, ((1, 1 << 63),))
    assert not source_universal_product_gate(parity, 128)["source_universal_phase_product"]
    assert parity.resource_upper_bound()["maximum_anf_degree"] == 1
    with pytest.raises(ValueError):
        source_universal_product_gate(BooleanANFMap(2, ((3,),)), 4)


def test_affine_chart_origin_can_be_absorbed_by_public_label_signs_only():
    for q in (8, 16, 128):
        labels = [[1, 2, 3, 1], [2, 1, 3, 0]]
        for syndrome in range(4):
            packet = compile_packet(labels, q, syndrome)
            origin_mask = sum(bit << i for i, bit in enumerate(packet.origin))
            normalized = compile_packet(signed_label_update(labels, q, origin_mask), q)
            assert packet.kernel_rows == normalized.kernel_rows
            assert all(packet.residual(z) == normalized.residual(z) for z in range(4))
