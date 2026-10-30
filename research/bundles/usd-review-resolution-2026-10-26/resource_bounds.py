"""Exact resource accounting for the reviewed ideal USD transfer argument.

This is an analytic certificate, not a decoder compiler or a hardness test.
"""

from fractions import Fraction
import json


def rational(value, name):
    if type(value) not in (int, Fraction):
        raise ValueError(f"{name} must be an exact rational")
    return Fraction(value)


def verified_trial_bounds(p0, gram_upper, *, raw_tv_error=0, failure_bits=20):
    """Bound raw trials per verified witness, charging rejected branches too.

    The caller must prove p_bar >= p0, lambda_s <= gram_upper and exact
    unambiguity for the ideal algorithm. raw_tv_error must bound the ENTIRE
    compiled raw-trial output distribution, including its failure outcome.
    """
    p0 = rational(p0, "p0")
    upper = rational(gram_upper, "gram_upper")
    error = rational(raw_tv_error, "raw_tv_error")
    if not 0 < p0 <= 1 or upper < p0:
        raise ValueError("require 0 < p0 <= 1 and gram_upper >= p0")
    if type(failure_bits) is not int or failure_bits < 1:
        raise ValueError("failure_bits must be a positive integer")
    ideal_raw = p0*p0/upper
    if not 0 <= error < ideal_raw:
        raise ValueError("whole-trial TV error must be below the success margin")
    success = ideal_raw-error
    # (1-success)^T <= exp(-T*success) <= 2^(-bits) when T*success >= bits.
    count = Fraction(failure_bits, 1)/success
    cap = (count.numerator+count.denominator-1)//count.denominator
    return {
        "ideal_raw_trials_per_accepted_branch_upper": 1/p0,
        "ideal_validity_given_acceptance_lower": p0/upper,
        "ideal_raw_verified_success_lower": ideal_raw,
        "compiled_raw_verified_success_lower": success,
        "raw_trials_per_verified_witness_upper": 1/success,
        "raw_trial_cap": cap,
        "failure_probability_upper": Fraction(1, 2**failure_bits),
        "requires_independent_fresh_trials": True,
        "premises_verified_by_this_helper": False,
        "compiled_decoder_implemented": False,
        "uniform_valid_output_law_claimed": False,
        "quantum_advantage_established": False,
    }


def unequal_success_workspace_control():
    """Exact two-state feasible USD control, with nonblank inverse workspace.

    G = [[1,1/2],[1/2,1]], D = diag(1/4,1/2). Positivity of G-D
    certifies a USD dilation. A physical dilation was independently tested
    by the reviewer; the formulas here are rational and do not reset work.
    """
    overlap, p, q = Fraction(1, 2), Fraction(1, 4), Fraction(1, 2)
    determinant = (1-p)*(1-q)-overlap**2
    if min(1-p, 1-q, determinant) <= 0:
        raise ArithmeticError("failure Gram must be positive definite")
    mean = (p+q)/2
    cases = []
    for sign in (1, -1):
        lam = 1+sign*overlap
        joint_fidelity = mean/lam
        blank = (p*p+q*q-2*sign*overlap*p*q)/(2*mean*(1-overlap**2))
        if not 0 <= joint_fidelity <= blank <= 1:
            raise ArithmeticError("joint fidelity must be contained in blank sector")
        cases.append({"character": (1, sign), "gram_eigenvalue": lam,
                      "squared_joint_fidelity": joint_fidelity,
                      "blank_workspace_probability": blank,
                      "nonblank_workspace_probability": 1-blank,
                      "resetting_workspace_is_not_permitted": True})
    return {"success_probabilities": (p, q), "average_success": mean,
            "failure_gram_determinant": determinant, "cases": cases}


def jsonable(value):
    if isinstance(value, Fraction):
        return str(value)
    if isinstance(value, dict):
        return {key: jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [jsonable(item) for item in value]
    return value


if __name__ == "__main__":
    print(json.dumps(jsonable({
        "scope": "REVIEW_RESOLUTION_ONLY_NO_GENERAL_DECODER",
        "workspace_control": unequal_success_workspace_control(),
        "ideal_example": verified_trial_bounds(Fraction(1, 4), Fraction(3, 2)),
        "compiled_example": verified_trial_bounds(Fraction(1, 4), Fraction(3, 2),
                                                   raw_tv_error=Fraction(1, 96)),
    }), indent=2))
