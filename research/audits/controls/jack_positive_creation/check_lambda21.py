"""One exact Sage control of Ben Dali--Dolega row creation at alpha=3.

No shape sweep. Polynomial arithmetic and Jack polynomials are Sage objects.
"""

import hashlib
import json
from pathlib import Path

from sage.all import QQ, PolynomialRing, SymmetricFunctions, prod


R = PolynomialRing(QQ, names=("p1", "p2", "p3", "y0", "y1", "y2", "y3", "u"))
p1, p2, p3, y0, y1, y2, y3, u = R.gens()
p = [R.zero(), p1, p2, p3]
y = [y0, y1, y2, y3]
alpha = QQ(3)
b = QQ(2)


def y_plus(f):
    return sum((y[i + 1] * f.derivative(y[i]) for i in range(3)), R.zero())


def gamma_y(f):
    # Source (24), with all terms capable of contributing through weight 3.
    join = sum(
        (
            alpha * i * y[i + j] * f.derivative(p[i]).derivative(y[j - 1])
            for i in range(1, 4)
            for j in range(1, 4)
            if i + j <= 3
        ),
        R.zero(),
    )
    split = sum(
        (
            y[i] * p[j] * f.derivative(y[i + j - 1])
            for i in range(1, 4)
            for j in range(1, 4)
            if i + j - 1 <= 3
        ),
        R.zero(),
    )
    twist = sum(
        (b * i * y[i + 1] * f.derivative(y[i]) for i in range(1, 3)),
        R.zero(),
    )
    return join + split + twist


def theta_y(f):
    return sum((p[i] * f.derivative(y[i]) for i in range(1, 4)), R.zero())


def B(n, parameter, f):
    g = y0 * f / alpha
    for _ in range(n):
        g = gamma_y(g) + parameter * y_plus(g)
    return theta_y(g)


def exp_degree2(parameter, f):
    # [t^2] exp(sum_(n>=1) t^n B_n/n).
    return (B(2, parameter, f) + B(1, parameter, B(1, parameter, f))) / 2


signed_first_row = -B(1, -3, R.one())
positive_first_row = B(1, 3, R.one())
assert signed_first_row == positive_first_row == p1

signed = exp_degree2(-6, signed_first_row)
positive = exp_degree2(6, positive_first_row)
assert signed == p1**3 + 2*p1*p2 - 3*p3
assert positive == 3*p1**3 + 12*p1*p2 + 9*p3

# Independent Sage integral-Jack basis, converted into this polynomial ring.
SF = SymmetricFunctions(QQ)
jack_p = SF.power()(SF.jack(t=alpha).J()[2, 1])
sage_jack = sum(
    (coefficient * prod(p[int(k)] for k in partition)
     for partition, coefficient in jack_p),
    R.zero(),
)
assert signed == sage_jack

monomials = (p1**3, p1*p2, p3)
labels = ("1,1,1", "2,1", "3")
signed_coefficients = tuple(QQ(signed.monomial_coefficient(m)) for m in monomials)
positive_coefficients = tuple(QQ(positive.monomial_coefficient(m)) for m in monomials)
ratios = tuple(a / abs(c) for a, c in zip(positive_coefficients, signed_coefficients))
assert ratios == (3, 6, 3)

# Hall norms of the three power sums: z_mu * 3^length(mu).
hall_weights = (QQ(162), QQ(18), QQ(9))
signed_weights = tuple(c*c*h for c, h in zip(signed_coefficients, hall_weights))
positive_weights = tuple(c*c*h for c, h in zip(positive_coefficients, hall_weights))
signed_norm = sum(signed_weights)
positive_norm = sum(positive_weights)
target_law = tuple(w / signed_norm for w in signed_weights)
positive_law = tuple(w / positive_norm for w in positive_weights)
tv = sum(abs(a-c) for a, c in zip(target_law, positive_law)) / 2
assert target_law == (QQ(18)/35, QQ(8)/35, QQ(9)/35)
assert positive_law == (QQ(18)/59, QQ(32)/59, QQ(9)/59)
assert tv == QQ(648)/2065

# A scoped repair on this ONE example exists; the mismatch is not a no-go.
acceptance = (QQ(1), QQ(1)/4, QQ(1))
accepted_mass = tuple(q*a for q, a in zip(positive_law, acceptance))
acceptance_probability = sum(accepted_mass)
assert acceptance_probability == QQ(35)/59
assert tuple(m/acceptance_probability for m in accepted_mass) == target_law

source = Path("research/audits/sources/jack_transform/bendali_dolega_positive.txt")
receipt = {
    "status": "EXACT_SCOPED_FALSIFIER",
    "scope": "lambda=(2,1), alpha=3; one control, no sweep",
    "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
    "operator_source": "equations (23)-(26), Theorem 8.2 first equality",
    "row_order": [1, 2],
    "signed_first_row": str(signed_first_row),
    "positive_first_row": str(positive_first_row),
    "exp_degree2_applied_to_p1_symbolic_u": str(exp_degree2(u, p1)),
    "signed_result": str(signed),
    "positive_result": str(positive),
    "independent_sage_jack": str(sage_jack),
    "partitions": list(labels),
    "positive_over_absolute_signed_coefficients": [str(x) for x in ratios],
    "target_squared_hall_norm": str(signed_norm),
    "positive_squared_hall_norm": str(positive_norm),
    "target_born_law": [str(x) for x in target_law],
    "positive_born_law": [str(x) for x in positive_law],
    "total_variation": str(tv),
    "one_example_rejection_acceptance": [str(x) for x in acceptance],
    "one_example_rejection_success": str(acceptance_probability),
    "general_positive_sampler": "OPEN",
    "hardness_claim": False,
}
# Sage's CLI retains sage/all.py as __file__; use the declared repo-relative path.
out = Path("research/audits/controls/jack_positive_creation/result.json")
out.write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
