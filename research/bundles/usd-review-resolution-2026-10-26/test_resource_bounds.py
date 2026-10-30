from fractions import Fraction as F

import pytest

from resource_bounds import unequal_success_workspace_control, verified_trial_bounds


def test_acceptance_is_not_verified_witness_cost():
    bound = verified_trial_bounds(F(1, 4), F(3, 2))
    assert bound["ideal_raw_trials_per_accepted_branch_upper"] == 4
    assert bound["ideal_validity_given_acceptance_lower"] == F(1, 6)
    assert bound["ideal_raw_verified_success_lower"] == F(1, 24)
    assert bound["raw_trials_per_verified_witness_upper"] == 24
    assert bound["raw_trial_cap"] == 480


def test_whole_trial_error_is_charged_before_repetition():
    bound = verified_trial_bounds(F(1, 4), F(3, 2), raw_tv_error=F(1, 96))
    assert bound["compiled_raw_verified_success_lower"] == F(1, 32)
    assert bound["raw_trials_per_verified_witness_upper"] == 32
    assert bound["raw_trial_cap"] == 640


@pytest.mark.parametrize("p0,upper", [(F(1, 7), F(8, 7)), (F(3, 5), 2), (1, 1)])
def test_exact_conservative_cap(p0, upper):
    bound = verified_trial_bounds(p0, upper, failure_bits=8)
    failure = (1-bound["compiled_raw_verified_success_lower"])**bound["raw_trial_cap"]
    assert failure <= bound["failure_probability_upper"] == F(1, 256)


def test_nonblank_workspace_after_inverse_is_expected():
    control = unequal_success_workspace_control()
    assert control["failure_gram_determinant"] == F(1, 8)
    assert control["average_success"] == F(3, 8)
    plus, minus = control["cases"]
    assert [plus["squared_joint_fidelity"], minus["squared_joint_fidelity"]] == [F(1, 4), F(3, 4)]
    assert [plus["nonblank_workspace_probability"], minus["nonblank_workspace_probability"]] == [F(2, 3), F(2, 9)]


@pytest.mark.parametrize("p0,upper,error", [(0, 1, 0), (2, 2, 0), (1, F(1, 2), 0),
                                          (F(1, 4), F(3, 2), F(1, 24)),
                                          (F(1, 4), F(3, 2), -1), (0.25, 1, 0)])
def test_invalid_or_exhausted_margins_are_rejected(p0, upper, error):
    with pytest.raises(ValueError):
        verified_trial_bounds(p0, upper, raw_tv_error=error)


def test_exponential_margin_is_not_polynomial_certificate():
    n = 20
    bound = verified_trial_bounds(F(1, 2**n), 2)
    assert bound["raw_trials_per_verified_witness_upper"] == 2**(2*n+1)
    assert not bound["premises_verified_by_this_helper"]
    assert not bound["compiled_decoder_implemented"]
    assert not bound["uniform_valid_output_law_claimed"]
    assert not bound["quantum_advantage_established"]
