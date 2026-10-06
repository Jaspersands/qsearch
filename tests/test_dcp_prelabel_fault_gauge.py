from fractions import Fraction

import pytest

from dcp_carry_packets import compile_packet
from dcp_physical_phase_noise import native_physical_source_mean, read
from dcp_prelabel_fault_gauge import (
    PrelabelBasisFaultLaw, _all_or_none, _fixed_source_calibration, _gauge_algebra_control,
    _iid_fault_law_calibration, _union_fault_moment,
    basis_gauge_transfer_gate, native_gauged_source_mean, two_point_completion_ledger,
)


def test_gauge_requires_prelabel_fault_data_and_discarded_coins():
    kwargs = {"fault_data_precedes_uniform_fourier_labels": True,
              "independent_uniform_fourier_labels": True,
              "old_labels_and_gauge_coins_discarded": True,
              "classical_mixture_of_product_good_or_basis_states": True}
    row = basis_gauge_transfer_gate(**kwargs)
    assert row["transfer_obligations_satisfied_as_declared"]
    assert not row["iid_physical_phase_formula_usable_as_declared"]
    assert not row["declarations_programmatically_proven"]
    assert not basis_gauge_transfer_gate(**{**kwargs, "fault_data_precedes_uniform_fourier_labels": False})["transfer_obligations_satisfied_as_declared"]
    assert not basis_gauge_transfer_gate(**{**kwargs, "old_labels_and_gauge_coins_discarded": False})["transfer_obligations_satisfied_as_declared"]
    iid = basis_gauge_transfer_gate(**kwargs, independent_fault_statuses=True)
    assert iid["iid_physical_phase_formula_usable_as_declared"]
    assert iid["iid_basis_failure_to_phase_flip_rate"] == "epsilon_i=gamma_i/2"


def test_iid_basis_faults_match_physical_phase_flips_at_half_the_rate():
    law = _iid_fault_law_calibration(Fraction(1, 8))
    direct = _fixed_source_calibration(law)
    phase = native_physical_source_mean(1, Fraction(1, 16))
    assert direct == read(phase["conditional_mean_relative_full_collision"])


def test_correlated_fault_laws_match_all_systematic_low_source_charts():
    laws = [PrelabelBasisFaultLaw(((1, 0, Fraction(1, 2)), (0, 2, Fraction(1, 2)))),
            PrelabelBasisFaultLaw(((0, 0, Fraction(7, 8)), (7, 7, Fraction(1, 8))))]
    for law in laws:
        assert _fixed_source_calibration(law) == read(native_gauged_source_mean(1, law)["conditional_mean_relative_full_collision"])


def test_large_correlated_faults_invalidate_the_same_marginal_iid_no_go():
    row = _all_or_none(256, Fraction(1, 8))
    correlated = read(row["conditional_mean_relative_full_collision"])
    iid = read(row["same_marginal_iid_phase_source_mean"])
    assert row["same_marginal_iid_uniformization_regime"]
    assert correlated > 1000
    assert iid < Fraction(101, 100)
    assert not row["logical_mask_enumeration_required"]
    assert row["conceptual_independent_fault_law_pairs_evaluated"] == 4


def test_sparse_fault_fourier_transport_keeps_64_bit_logical_masks():
    packet = compile_packet([[1] * 65], 128)
    law = PrelabelBasisFaultLaw(((0, 0, Fraction(3, 4)), (1, 0, Fraction(1, 4))))
    assert law.fourier(packet, packet, 2**63) == Fraction(3, 4)
    assert law.fourier(packet, packet, (1 << 63) | 1) == 1


def test_union_moment_handles_fully_faulted_free_and_pivot_rows():
    for n in (1, 8, 64):
        mask = (1 << (3 * n)) - 1
        assert _union_fault_moment(n, mask, mask) == 1
        clean = native_physical_source_mean(n, 0)
        assert _union_fault_moment(n, 0, 0) == read(clean["conditional_mean_relative_full_collision"])


def test_constant_fault_law_is_not_a_shared_physical_Z_cancellation_law():
    packet = compile_packet([[1, 1, 1]], 8)
    # A failed basis qubit becomes maximally mixed, not a known/shared Z flip.
    law = PrelabelBasisFaultLaw(((1, 1, Fraction(1)),))
    assert law.fourier(packet, packet, 1) == 0
    assert law.fourier(packet, packet, 3) == 1


def test_fault_law_requires_normalization_integer_masks_and_valid_width():
    with pytest.raises(ValueError):
        PrelabelBasisFaultLaw(((0, 0, Fraction(1, 2)),))
    with pytest.raises(ValueError):
        PrelabelBasisFaultLaw(((0.5, 0, Fraction(1)),))
    with pytest.raises(ValueError):
        native_gauged_source_mean(1, PrelabelBasisFaultLaw(((8, 0, Fraction(1)),)))
    with pytest.raises(ValueError):
        native_gauged_source_mean(0, PrelabelBasisFaultLaw(((0, 0, Fraction(1)),)))


def test_exact_gauge_algebra_keeps_the_postlabel_counterexample():
    row = _gauge_algebra_control()
    assert row["exact_good_density_phase_identities_checked"] == 512
    assert row["fixed_prelabel_bad_bit_conditional_counts"] == [1, 1]
    assert row["counterexample_conditional_counts"] == [2, 0]


def test_each_fixed_union_moment_matches_all_physical_disjoint_directions():
    for left in range(8):
        for right in range(8):
            value = Fraction(0)
            for a in range(4):
                for b in range(4):
                    rows = ([a, 1, 2], [b, 1, 2])
                    for h in range(4):
                        images = [sum(((r & h).bit_count() & 1) << i for i, r in enumerate(rs)) for rs in rows]
                        if images[0] & left or images[1] & right:
                            continue
                        for j in range(4):
                            directions = [sum(((r & j).bit_count() & 1) << i for i, r in enumerate(rs)) for rs in rows]
                            if not (images[0] & directions[0] or images[1] & directions[1]):
                                value += Fraction(1, 64)
            assert value == _union_fault_moment(1, left, right)


def test_actual_two_point_failure_scaling_does_not_create_constant_rate_lpn():
    row = two_point_completion_ledger(128, 256)
    assert read(row["definition_3_1_basis_failure_bound"]) == Fraction(1, 1024)
    assert read(row["gauged_each_original_phase_flip_marginal_bound"]) == Fraction(1, 2048)
    completion = row["known_correct_residue_completion"]
    assert read(completion["marginal_flip_bound_only_correct_completion_success_lower_bound"]) > Fraction(9, 10)
    assert not row["natural_lattice_M_and_total_state_supply_parameter_map_verified"]
    assert not row["fault_independence_or_conditional_history_budget_inferred"]
    with pytest.raises(ValueError):
        two_point_completion_ledger(128, 255)
    with pytest.raises(ValueError):
        two_point_completion_ledger(128, 256, failure_parameter=0)
