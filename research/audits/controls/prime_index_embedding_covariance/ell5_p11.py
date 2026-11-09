"""One finite covariance/mismatched-embedding falsifier, not a full algorithm.

Sage supplies exact number-field and residue arithmetic. Complex evaluations
are 256-bit numerical controls. The known circular unit is validation truth;
no class/unit source, L1 estimator or quantum primitive is executed.
"""
from pathlib import Path
import json
from sage.all import (
    QQ, ZZ, GF, PolynomialRing, NumberField, CyclotomicField, ComplexField,
    factorial, RealField,
)

ell, p, g, k, r, shift = 5, 11, 2, 2, 4, 2
Q = PolynomialRing(QQ, "x")
x = Q.gen()
K = NumberField(x**5 + x**4 - 4*x**3 - 3*x**2 + 3*x + 1, "t")
t = K.gen()
sigma = K.hom([t*t-2], K)
alpha = K(2)-t
delta = sigma(alpha)/alpha
c = delta.sqrt()
R = CyclotomicField(ell, "zeta")
zeta = R.gen()
lam = zeta-1
eta2 = zeta**2 + zeta**3
v = eta2**4
assert v.conjugate() == v and v.is_unit()
assert ((v-1)/lam**2).denominator() == 1


def sigpow(a, n):
    for _ in range(n % ell):
        a = sigma(a)
    return a


def act(a, exponent):
    ans = K.one()
    for i, coeff in enumerate(exponent.list()):
        assert coeff in ZZ
        ans *= sigpow(a, i)**ZZ(coeff)
    return ans


c0 = act(sigpow(c, shift), v)
CC = ComplexField(256)
RR = RealField(256)
embeddings = K.embeddings(CC)
iota0 = max(embeddings, key=lambda emb: emb(t).real())
rho = (CC(0, 2)*CC.pi()/ell).exp()


def mode(a, j, b):
    return sum(rho**(j*i)*abs(iota0(sigpow(a, i+b))).log()
               for i in range(ell))


def tau(j, b):
    return sum(rho**(j*i)*iota0(sigpow(t, i+b))
               for i in range(ell))


# This known-c target substitutes only for the analytic scalar in this
# finite control. Its branch law is tested against independently evaluated
# algebraic tau_j; it is not an implementation of the native L1 estimator.
scalars = {j: mode(c, j, 0)/tau(j, 0) for j in range(1, ell)}
fp = GF(p)
P = PolynomialRing(fp, "s")


def poly(a):
    return P([fp(coeff) for coeff in K(a).list()])


pi_poly = sum(fp(r)**(-i)*poly(sigpow(t, i)) for i in range(ell))
den = pi_poly.derivative()(fp(2))
assert pi_poly(fp(2)) == 0 and den != 0


def output_for(a):
    w = zeta**((shift+a) % ell)*v
    exponent = (w-1)/lam
    assert exponent.denominator() == 1
    out = alpha*act(delta, exponent)
    assert out.norm() == p
    assert sigma(out)/out == act(delta, w)
    assert poly(act(delta, w))(fp(2)) == fp(r)
    return int(poly(out).derivative()(fp(2))/den)


rows = []
max_relative_error = RR(0)
for b in range(ell):
    j = max(range(1, ell), key=lambda j: abs(mode(c0, j, b)))
    mb = mode(c0, j, b)
    relative = abs(mb-rho**(-b*j)*mode(c0, j, 0))/abs(mb)
    max_relative_error = max(max_relative_error, relative)
    for target_branch in [b, (b+1) % ell]:
        target = scalars[j]*tau(j, target_branch)
        ratio = target/mb
        scores = [abs((ratio*rho**(a*j)).imag())/abs(ratio)
                  for a in range(ell)]
        a = min(range(ell), key=lambda a: scores[a])
        assert scores[a] < RR("1e-60")
        assert all(scores[q] > RR("0.1")
                   for q in range(ell) if q != a)
        expected_a = (-shift+target_branch-b) % ell
        value = output_for(a)
        expected = int(fp(factorial(k))*fp(r)**(target_branch-b))
        assert a == expected_a and value == expected
        rows.append({"unit_embedding": b, "target_embedding": target_branch,
                     "mode": j, "selected_exponent": a,
                     "factorial_residue": value,
                     "matched_embeddings": b == target_branch})
assert max_relative_error < RR("1e-60")
assert {row["factorial_residue"] for row in rows if row["matched_embeddings"]} == {2}
assert {row["factorial_residue"] for row in rows if not row["matched_embeddings"]} == {8}
report = {"ell": ell, "p": p, "g": g, "k": k, "r": r,
          "c0_shift": shift, "real_multiplier": str(v),
          "max_relative_mode_covariance_error": str(max_relative_error),
          "complex_precision_bits": 256, "rows": rows,
          "scope": "One finite Sage algebra control and numerical phase check. Known c supplies validation truth; no L1 sampling, PIP, class-group or quantum algorithm is executed. No asymptotic conclusion from this control."}
Path(__file__).with_suffix(".json").write_text(json.dumps(report, indent=2)+"\n")
print(json.dumps({"matched_outputs": [2]*ell, "mismatched_outputs": [8]*ell,
                  "max_relative_error": str(max_relative_error),
                  "scope": report["scope"]}))
