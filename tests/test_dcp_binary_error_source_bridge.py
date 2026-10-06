import itertools
from fractions import Fraction

import pytest

from dcp_binary_error_source_bridge import (
    _marker_controls,_translation_family_controls, hidden_marker_source_certificate,
    hidden_marker_target_wrapper, single_translation_conversion_certificate,
    ternary_import_certificate,two_point_fourier_certificate,
)
from dcp_physical_phase_noise import read


def test_hidden_marker_exact_joint_law_has_polynomial_zero_to_target_transfer():
    rows=_marker_controls()
    assert [r["complete_source_and_marker_trials"] for r in rows] == [81,1024]
    for row in rows:
        assert row["accepted_target_trials"] == row["successful_zero_output_weight_sum"]
        assert row["accepted_target_trials"] >= row["nonempty_zero_successes"]
    certificate=hidden_marker_source_certificate(31,Fraction(1,16))
    assert read(certificate["uniform_full_target_coverage_lower_bound"]) == Fraction(1,512)
    assert certificate["one_extra_public_classical_column_not_an_extra_unknown_phase_state"]


def test_original_target_and_marker_are_not_passed_to_zero_solver():
    seen=[]
    def solver(A,q,seed):
        seen.append((A,q,seed))
        return next((word for word in range(1,8) if sum(a*(word>>i&1) for i,a in enumerate(A[0]))%q==0),None)
    for j in range(3):
        word=hidden_marker_target_wrapper(((1,2),),3,(1,),solver,marker_index=j,solver_seed=19)
        if word is not None:
            assert sum(a*(word>>i&1) for i,a in enumerate((1,2)))%3 == 1
    assert all(len(args)==3 and args[2]==19 for args in seen)


def test_leaking_the_marker_can_destroy_coverage_even_with_perfect_zero_success():
    for entries in itertools.product(range(3),repeat=4):
        A=(entries[:3],);target=(entries[3],)
        for marker in range(4):
            def leaked_solver(H,q,seed,marker=marker):
                # Every3 vectors in Z3 have a nonempty zero sum; deliberately avoid marker.
                return next(word for word in range(1,16) if not(word>>marker&1) and
                            sum(a*(word>>i&1) for i,a in enumerate(H[0]))%q==0)
            assert hidden_marker_target_wrapper(A,3,target,leaked_solver,marker_index=marker) is None


@pytest.mark.parametrize("bad",[None,0,-1,8,True,1])
def test_empty_invalid_or_unmarked_zero_words_fail_closed(bad):
    assert hidden_marker_target_wrapper(((1,2),),3,(1,),lambda *args:bad,marker_index=2) is None


def test_actual_translation_families_have_information_not_boolean_error_rank():
    rows=_translation_family_controls()
    assert [row["source_family_rank"] for row in rows] == [2,2,2,3,4]
    assert [row["target_family_rank"] for row in rows] == [2,3,7,7,15]
    assert rows[0]["ternary_exact_isometry_residual"] < 1e-10
    assert all(row["target_projector_sum_operator_norm"] <= 2+1e-10 for row in rows)


@pytest.mark.parametrize("q,copies,excluded",[(3,1,False),(4,1,True),(8,2,True),(8,4,False),(16,3,True)])
def test_exact_heralded_branch_bound_does_not_assume_uniform_success(q,copies,excluded):
    row=single_translation_conversion_certificate(q,copies)
    assert row["exact_nonzero_pure_target_branch_ruled_out"] == excluded
    assert row["arbitrary_exact_heralded_branch_necessary_same_translation_copies"] == q//2
    assert not row["native_different_label_collective_algorithm_ruled_out"]


def test_arbitrary_channel_average_success_times_fidelity_bound_charges_heralds():
    row=single_translation_conversion_certificate(1<<65,256)
    assert read(row["arbitrary_heralded_channel_uniform_mean_success_times_target_fidelity_upper_bound"]) == Fraction(514,1<<65)
    assert not row["same_label_copies_granted_by_native_source"]
    assert not row["arbitrary_quantum_subset_sum_algorithm_ruled_out"]


def test_boolean_fourier_alphabet_is_not_binary_at_growing_modulus():
    assert two_point_fourier_certificate(3)["minimum_fourier_support_with_both_nonzero_coefficients"] == 2
    row=two_point_fourier_certificate(1<<65)
    assert row["minimum_fourier_support_with_both_nonzero_coefficients"] == (1<<65)-1
    assert read(row["arbitrary_normalized_two_frequency_retention_mass_upper_bound"]) == Fraction(1,1<<63)
    assert not row["binary_support_compatible_with_minimum_size"]
    nonunit=two_point_fourier_certificate(8,gap=4)
    assert nonunit["minimum_fourier_support_with_both_nonzero_coefficients"] == 4
    assert not nonunit["full_boolean_unit_gap_source"]


def test_high_density_ternary_finder_is_not_a_one_word_DCP_readout():
    row=ternary_import_certificate(128,1024,513)
    assert row["one_selected_witness_full_group_readout_probability_upper_bound_dyadic_exponent"] == 821
    assert not row["additive_homomorphism_between_ternary_and_two_power_groups_is_nontrivial"]
    assert not row["new_paper_is_a_native_DCP_solver"]
    for q in (4,8,16,32):
        assert (q-1)%3+1%3 != 0  # Integer mod3 reduction fails to respect the q-wrap.
        assert q%3 != 0


def test_interface_parameter_validation():
    with pytest.raises(ValueError):
        hidden_marker_source_certificate(1,2)
    with pytest.raises(ValueError):
        hidden_marker_source_certificate(1,1,returned_weight_lower_bound=3)
    with pytest.raises(ValueError):
        hidden_marker_target_wrapper(((1,),),4,(0,),lambda *args:1,marker_index=2)
    with pytest.raises(ValueError):
        single_translation_conversion_certificate(8,0)
    with pytest.raises(ValueError):
        two_point_fourier_certificate(8,gap=8)
    with pytest.raises(ValueError):
        ternary_import_certificate(1,1,1)
