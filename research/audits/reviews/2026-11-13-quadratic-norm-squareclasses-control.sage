"""One exact real-quadratic stress case; no parameter sweep.

Run with /opt/anaconda3/envs/qsearch-cas/bin/sage and redirect stdout to the
adjacent JSON file.  The script certifies this example only, not a complexity
claim or the universally quantified squareclass theorem.
"""
import json

K = QuadraticField(34, 'r')
r = K.gen()
beta = 3 + r
P = K.ideal(5, r + 3)
cf = continued_fraction(r)
period = [int(x) for x in cf.period()]

assert beta.norm() == -25
assert (beta / 5).norm() == -1
assert K.ideal(beta) == P**2
assert P.norm() == 5
assert (6 + r).norm() == 2
assert r.norm() == -34
assert period == [1, 4, 1, 10]

print(json.dumps({
    "scope": "single exact falsifier to an integral-negative-Pell prerequisite",
    "d": int(34),
    "S_Q": [int(x) for x in [2, 17]],
    "primitive_conic_point_for_a_minus_one": [int(x) for x in [3, 1, 5]],
    "beta": "3 + sqrt(34)",
    "norm_beta": int(beta.norm()),
    "norm_beta_over_5": int((beta / 5).norm()),
    "principal_ideal_beta": "(5, sqrt(34) + 3)^2",
    "ideal_equality_verified": True,
    "sqrt_d_continued_fraction_period": period,
    "period_length_even": len(period) % 2 == 0,
    "norm_6_plus_sqrt_d": int((6 + r).norm()),
    "norm_sqrt_d": int(r.norm()),
    "finite_control_proves_general_algorithm": False,
    "conic_backend_polynomial_clock_verified_here": False
}, indent=int(2), sort_keys=True))
