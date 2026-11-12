# One fixed exact arithmetic counterexample only. No classgroup/unit calls or sweep.
from sage.all import QQ, PolynomialRing, NumberField
from pathlib import Path
import json

out = Path("research/audits/controls/quartic_content_counterexample/result.json").resolve()
Qx = PolynomialRing(QQ, "x"); x = Qx.gen()
F = NumberField(x*x-x-57, "t"); t = F.gen()
d = -107-15*t
rho = 6-t
epsilon = t+7
X = 198+29*t
Y = F(18)
Z = -228-35*t
q = F.ideal(3,t)
qprime = F.ideal(3,t-1)
Icontent = F.ideal([X,Y,Z])
checks = {
    "quadratic_equation": t*t-t-57 == 0,
    "field_discriminant_229": F.discriminant() == 229,
    "norm_d_229": d.norm() == 229,
    "norm_rho_minus_27": rho.norm() == -27,
    "norm_epsilon_minus_one": epsilon.norm() == -1,
    "quarter_identity": (t*t-d)/4 == 41+4*t,
    "norm_form_square_identity": X*X-d*Y*Y == Z*Z,
    "q_prime_norm_three": q.is_prime() and q.norm() == 3,
    "qprime_prime_norm_three": qprime.is_prime() and qprime.norm() == 3,
    "q_and_qprime_distinct": q != qprime,
    "rational_three_factorization": F.ideal(3) == q*qprime,
    "rho_ideal_equals_q_cubed": F.ideal(rho) == q**3,
    "content_ideal_equals_q": Icontent == q,
    "valuation_X_at_q_one": F.ideal(X).valuation(q) == 1,
    "valuation_Z_at_q_one": F.ideal(Z).valuation(q) == 1,
    "valuation_Y_at_q_two": F.ideal(Y).valuation(q) == 2,
    "valuation_X_at_qprime_zero": F.ideal(X).valuation(qprime) == 0,
    "d_is_q_unit": F.ideal(d).valuation(q) == 0,
    "d_congruent_one_mod_q": d-1 in q,
    "q_residue_characteristic_odd": q.smallest_integer() == 3,
    "rational_sqrt_bound": 15**2 < 229 and 229 < 16**2,
    "positive_unit_bound": 90+6*16 == 186 and 186 < 229,
}
assert all(checks.values()), checks
# The exact residue certificate d=1 mod q gives two distinct roots +/-1 in F_3.
residue_roots = [a for a in range(3) if (a*a-1) % 3 == 0]
assert residue_roots == [1,2]
Pz = PolynomialRing(F, "z"); z = Pz.gen()
L = F.extension(z*z-d, "delta"); delta = L.gen()
beta = (9+L(rho)*delta)**2/L(rho)
relative_checks = {
    "delta_square_d": delta*delta == L(d),
    "beta_equals_X_plus_Y_delta": beta == L(X)+L(Y)*delta,
    "beta_over_rho_square": beta/L(rho) == (9/L(rho)+delta)**2,
    "relative_norm_by_explicit_conjugation_Z_squared": beta*(L(X)-L(Y)*delta) == L(Z*Z),
}
assert all(relative_checks.values()), relative_checks
# Fixed degree-four relative field only; factor the extension of the single ideal q.
q_extension = L.ideal([L(a) for a in q.gens()])
q_factors = list(q_extension.factor())
assert len(q_factors) == 2 and all(e == 1 for P,e in q_factors)
beta_ideal = L.ideal(beta)
relative_prime_rows = []
for P,e in q_factors:
    v = beta_ideal.valuation(P)
    assert v == 1
    relative_prime_rows.append({"prime_generators": [str(a) for a in P.gens()], "ramification_exponent_in_q_extension": int(e), "beta_valuation": int(v)})
relative_checks["q_splits_into_two_distinct_unramified_primes"] = True
relative_checks["beta_valuation_one_at_both_q_primes"] = True
# This elementary certificate does not assume that epsilon is a fundamental unit.
nonprincipality_certificate = {
    "unit": "epsilon=(15+sqrt(229))/2, Norm(epsilon)=-1",
    "rational_bound": "15<sqrt(229)<16, hence 12*epsilon=90+6*sqrt(229)<186<229",
    "ring_of_integers": "O_F=Z[t], since the defining polynomial discriminant equals the field discriminant229",
    "proof": "If q=(alpha), then |Norm(alpha)|=3. Multiplying by an integral power of the unit epsilon makes each real conjugate have absolute value at most sqrt(3*epsilon): choose |alpha_1| in [sqrt(3/epsilon),sqrt(3*epsilon)]. Writing alpha=a+b*t with integral a,b gives |b|=|alpha_1-alpha_2|/sqrt(229)<=2*sqrt(3*epsilon)/sqrt(229)<1. Thus b=0 and |Norm(alpha)|=a^2 cannot equal3. Therefore q is not principal. No fundamental-unit or class-group computation is used.",
    "conclusion": "q is nonprincipal; therefore the content ideal q has no element generator",
}
result = {
    "status": "PASS",
    "scope": "One fixed exact content counterexample to an element-gcd primitive-lift step; not a falsifier of a corrected ideal-saturation algorithm and not an asymptotic control.",
    "cas": "/opt/anaconda3/envs/qsearch-cas/bin/sage",
    "field": "Q(t), t^2-t-57=0", "field_discriminant": int(F.discriminant()),
    "d": str(d), "rho": str(rho), "epsilon": str(epsilon),
    "X": str(X), "Y": str(Y), "Z": str(Z),
    "norms": {"d": int(d.norm()), "rho": int(rho.norm()), "epsilon": int(epsilon.norm())},
    "q_generators": [str(a) for a in q.gens()],
    "qprime_generators": [str(a) for a in qprime.gens()],
    "valuations": {"X_at_q": int(F.ideal(X).valuation(q)), "Z_at_q": int(F.ideal(Z).valuation(q)), "Y_at_q": int(F.ideal(Y).valuation(q)), "X_at_qprime": int(F.ideal(X).valuation(qprime))},
    "assertions": checks, "residue_square_roots_of_d_mod_q": [int(a) for a in residue_roots],
    "relative_assertions": relative_checks, "beta": str(beta),
    "relative_primes_above_q": relative_prime_rows,
    "nonprincipality_certificate": nonprincipality_certificate,
}
out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
print(json.dumps({"status": result["status"], "base_assertions_passed": len(checks), "relative_assertions_passed": len(relative_checks), "norms": result["norms"], "valuations": result["valuations"], "beta_valuations_at_two_split_primes": [r["beta_valuation"] for r in relative_prime_rows], "nonprincipal_content_ideal": "q=(3,t)"},indent=2))
