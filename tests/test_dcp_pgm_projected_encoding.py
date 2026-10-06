from fractions import Fraction

import pytest

from dcp_pgm_projected_encoding import (
    _ceil_sqrt, bounded_physical_control, normalization_certificate, run_controls,
)


def read(row):
    return Fraction(int(row["numerator_hex"],16),int(row["denominator_hex"],16))


@pytest.fixture(scope="module")
def report():
    return run_controls()


def test_actual_public_unitary_and_reflections_match_every_secret_spectral_formula(report):
    for control in report["physical_controls"]:
        assert not control["unknown_input_preparation_inverse_used"]
        for row in control["physical_controls"]:
            assert row["optimal_classical_label_guess_uniform_secret_unconditional"]>=row["spectral_correct_unconditional"]-1e-9
            for s in row["every_secret_physical_probabilities"]:
                assert s["correct_unconditional"]==pytest.approx(row["spectral_correct_unconditional"])
                assert s["herald"]==pytest.approx(row["spectral_herald"])
                assert s["total_physical_norm"]==pytest.approx(1)
                assert s["herald"]+s["failed_herald"]==pytest.approx(1)


def test_condition_one_does_not_make_tiny_absolute_singular_values_free(report):
    row = report["physical_controls"][0]
    assert read(row["supported_singular_value_condition_number_squared"])==1
    assert read(row["raw_correct_exact"])==Fraction(1,4)
    assert read(row["raw_conditional_correct_exact"])==1
    assert row["physical_controls"][1]["spectral_correct_unconditional"]==pytest.approx(1)


def test_zero_matrix_retains_impossible_secret_discrimination_and_failure_cost(report):
    row = report["physical_controls"][1]
    assert read(row["raw_herald_exact"])==1
    assert row["ideal_PGM_success"]==pytest.approx(0.25)
    assert all(r["spectral_correct_unconditional"]==pytest.approx(0.25) for r in row["physical_controls"])


def test_complete_source_census_verifies_pooled_conditioning_not_unconditional_success(report):
    assert [r["complete_native_matrices"] for r in report["complete_native_sources"]]==[16,512,256]
    for r in report["complete_native_sources"]:
        G,N = r["q"]**r["n"],2**r["m"]
        assert read(r["exact_mean_raw_herald"])==Fraction(N+G-1,N*G)
        assert read(r["exact_pooled_conditional_correct"])==Fraction(N,N+G-1)
        assert read(r["unconditional_correct"])==Fraction(1,G)


def test_native_plus16_can_look_good_conditionally_and_still_fail_exponentially(report):
    for r in report["native_growing_ledgers"]:
        G = 1 << (r["dimension"]*r["modulus_bits"])
        assert read(r["native_pooled_correct_probability_given_raw_herald"])>Fraction(65536,65537)
        assert read(r["odd_bounded_polynomial_correct_probability_upper_bound"])==Fraction(5*r["degree"]**2,2*G)
        minimum = int(r["minimum_degree_necessary_for_target_success"],16)
        assert minimum**2>=Fraction(G,5) and (minimum-1)**2<Fraction(G,5)
        assert r["conservative_correct_probability_dyadic_exponent"]>200
        assert not r["arbitrary_interleaved_algorithms_or_other_encodings_ruled_out"]
    assert not any(report["claim_gate"].values())


def test_easy_family_counterexample_prevents_general_QSVT_or_DHSP_no_go(report):
    row = report["easy_binary_family_countercontrol"]
    assert row["direct_correct_probability"]==row["comparison_singular_condition_number"]==1
    assert not row["general_hidden_subgroup_hardness_inferred"]
    # Actual identity-label binary phases decode by independent Hadamards.
    for s in range(16):
        for i in range(4):
            phase = (-1)**((s>>i)&1)
            bit = (s>>i)&1
            assert abs((1+(-1)**bit*phase)/2)**2==1


def test_jointly_normalized_random_branch_instruments_keep_unconditional_bound(report):
    weights = [Fraction(1,5),Fraction(3,10),Fraction(1,10),Fraction(2,5)]
    assert sum(weights)==1
    for control in report["physical_controls"]:
        G = control["modulus"]**len(control["labels"])
        branches = control["physical_controls"]
        for index in range(G):
            total = sum(float(w)*b["every_secret_physical_probabilities"][index]["total_physical_norm"]
                        for w,b in zip(weights,branches))
            assert total==pytest.approx(1)
        # Branch labels are retained; each branch gets its own optimal re-guess.
        success = sum(float(w)*b["optimal_classical_label_guess_uniform_secret_unconditional"]
                      for w,b in zip(weights,branches))
        assert success<=min(1,5*max(b["degree"] for b in branches)**2/(2*G))+1e-9


@pytest.mark.parametrize("x",[Fraction(1,4),Fraction(1),Fraction(2),Fraction(9),Fraction(10),Fraction(10**100+1,3)])
def test_exact_rational_square_root_rounding(x):
    k = _ceil_sqrt(x)
    assert k*k>=x and (k-1)**2<x


@pytest.mark.parametrize("args",[(0,2,2,3),(1,0,2,3),(1,2,0,3),(1,2,2,0),(True,2,2,3),(1,2,2,3,0),(1,2,2,3,0.5)])
def test_invalid_exact_certificate_parameters_rejected(args):
    with pytest.raises(ValueError):
        normalization_certificate(*args)


@pytest.mark.parametrize("A,q,degrees",[([],4,(1,)),([[1]],3,(1,)),([[True]],4,(1,)),([[1],[1,2]],4,(1,)),([[1]],4,(2,)),([[1]],4,()),([[1]],4,(33,))])
def test_invalid_or_unbounded_physical_controls_rejected(A,q,degrees):
    with pytest.raises(ValueError):
        bounded_physical_control(A,q,degrees)


def test_degree_envelope_clamps_at_one_without_false_superprobabilities():
    row = normalization_certificate(1,2,2,100)
    assert read(row["odd_bounded_polynomial_correct_probability_upper_bound"])==1
    assert row["conservative_correct_probability_dyadic_exponent"]==0
