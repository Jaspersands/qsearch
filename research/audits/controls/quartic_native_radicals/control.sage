# Two fixed exact formula controls only; no asymptotic inference.
# CAS: /opt/anaconda3/envs/qsearch-cas/bin/sage
from sage.all import QQ, PolynomialRing, NumberField
from pathlib import Path
import json

out = Path("research/audits/controls/quartic_native_radicals/result.json").resolve()
Qx = PolynomialRing(QQ, "x")
x = Qx.gen()
QT = PolynomialRing(QQ, "T")
T = QT.gen()
cases = [("Phi5", x**4+x**3+x**2+x+1, QQ(2), 125),
         ("cyclic_quartic_17", x**4-34*x**2+17, QQ(-34), 4913)]
rows = []
for name, h, expected_u, expected_field_discriminant in cases:
    assert h.degree() == 4 and h.is_monic() and h.is_irreducible()
    a, b, c, d = [QQ(h[i]) for i in [3, 2, 1, 0]]
    R = T**3-b*T**2+(a*c-4*d)*T+4*b*d-a*a*d-c*c
    rational_roots = R.roots(ring=QQ, multiplicities=False)
    assert rational_roots == [expected_u], (name, rational_roots)
    u = rational_roots[0]
    K = NumberField(h, "theta")
    theta = K.gen()
    Ds = a*a-4*b+4*u
    checks = {"monic_irreducible_degree_four": True,
              "unique_rational_resolvent_root": len(rational_roots) == 1,
              "expected_resolvent_root": u == expected_u}
    denominators = {}
    if Ds != 0:
        branch = "Ds_nonzero"
        denominator_s = 2*theta**2+a*theta+u
        assert denominator_s != 0
        s = -(a*theta**2+2*(b-u)*theta+c)/denominator_s
        denominator_t = 2*s+a
        assert denominator_t != 0
        t = (c+s*u)/denominator_t
        denominators = {"s_denominator_nonzero": denominator_s != 0,
                        "t_denominator_nonzero": denominator_t != 0}
        checks["s_quadratic_equation"] = s*s+a*s+b-u == 0
        checks["t_quadratic_equation"] = t*t-u*t+d == 0
        checks["theta_quadratic_equation"] = theta*theta-s*theta+t == 0
        checks["s_discriminant_identity"] = (2*s+a)**2 == Ds
        quadratic_generator = s
        generator_name = "s"
    else:
        branch = "Ds_zero"
        s = K(-a/2)
        t = s*theta-theta**2
        checks["s_equals_minus_a_over_two"] = s == -a/2
        checks["s_quadratic_equation"] = s*s+a*s+b-u == 0
        checks["t_quadratic_equation"] = t*t-u*t+d == 0
        checks["t_discriminant_identity"] = (2*t-u)**2 == u*u-4*d
        checks["theta_quadratic_equation"] = theta*theta-s*theta+t == 0
        quadratic_generator = t
        generator_name = "t"
    drel = s*s-4*t
    checks["relative_radical_identity"] = (2*theta-s)**2 == drel
    checks["relative_discriminant_nonzero"] = drel != 0
    generator_minpoly = quadratic_generator.minpoly()
    checks["quadratic_generator_degree_two"] = generator_minpoly.degree() == 2
    assert all(checks.values()) and all(denominators.values()), (name, checks, denominators)
    field_discriminant = K.discriminant()
    rows.append({"case": name, "h": str(h),
        "coefficients": {k: str(v) for k, v in zip(["a","b","c","d"],[a,b,c,d])},
        "resolvent": str(R), "rational_roots": [str(v) for v in rational_roots],
        "u": str(u), "Ds": str(Ds), "branch": branch,
        "s": str(s), "t": str(t), "drel": str(drel),
        "quadratic_generator": generator_name,
        "quadratic_generator_minpoly": str(generator_minpoly),
        "quadratic_generator_degree": int(generator_minpoly.degree()),
        "denominator_checks": denominators, "assertions": checks,
        "field_discriminant": int(field_discriminant),
        "expected_field_discriminant": int(expected_field_discriminant),
        "field_discriminant_matches_expected": field_discriminant == expected_field_discriminant})
result = {"status": "PASS", "scope": "Two fixed native quartics; exact identities and both Ds branches only. No classgroup/unit call, sweep, or asymptotic theorem.",
          "cas": "/opt/anaconda3/envs/qsearch-cas/bin/sage", "cases": rows,
          "discriminant_mismatches": [r["case"] for r in rows if not r["field_discriminant_matches_expected"]]}
out.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
print(json.dumps({"status": result["status"], "cases": [{"case": r["case"], "branch": r["branch"], "assertions_passed": len(r["assertions"]), "quadratic_generator_degree": r["quadratic_generator_degree"], "field_discriminant": r["field_discriminant"]} for r in rows], "discriminant_mismatches": result["discriminant_mismatches"]}, indent=2))
