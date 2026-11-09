"""One exact paired falsifier; run with the qsearch-cas Python (Sage).

This is not a Kloosterman approximation algorithm or a full-zeta execution.
The all-prime claims are sourced/proved in KLOOSTERMAN_SPECTRAL_ADMISSION.md.
"""
from hashlib import sha256
import json
from pathlib import Path

from sage.all import CyclotomicField, FunctionField, GF, PolynomialRing


def main():
    p, r = 5, 2
    cyclo = CyclotomicField(p)
    zeta = cyclo.gen()
    base = FunctionField(GF(p), "x")
    x = base.gen()
    ring = PolynomialRing(base, "y")
    y = ring.gen()
    values, cases = {}, []
    for a in (1, 4):
        value = sum(zeta ** ((j + a * pow(j, -1, p)) % p)
                    for j in range(1, p))
        curve_field = base.extension(y**p - y - x - a/x, "y")
        points = {(j, k) for j in range(1, p) for k in range(p)
                  if (k**p - k - j - a * pow(j, -1, p)) % p == 0}
        poly = value.minpoly()
        genus = int(curve_field.genus())
        assert list(poly) == [1, -3, 1]
        assert genus == 4 and len(points) == 10
        values[a] = (value, points)
        cases.append({
            "a": a, "cyclotomic_value": str(value),
            "minpoly_coefficients_low_to_high": [int(c) for c in poly],
            "algebraic_degree": int(poly.degree()), "sage_genus": genus,
            "affine_point_count": len(points),
            "projective_point_count": len(points) + 2,
            "boundary_justification": "One totally ramified rational point at each simple pole",
        })
    first, second = values[1][0], values[4][0]
    assert first != second
    assert first + second == 3 and first * second == 1
    sigma = cyclo.hom([zeta**r], cyclo)
    assert sigma(first) == second
    assert {(r*j % p, r*k % p) for j, k in values[1][1]} == values[4][1]
    assert (r*x + (r*r)/(r*x)) == r*(x + 1/x)
    source_dir = Path(__file__).resolve().parents[1] / "audits/sources/legendre_prf"
    sources = ["bruin_kloosterman_1807_03600.pdf", "childs_walk_0810_0312.pdf",
               "kloosterman_degree_1107_0188.pdf", "kedlaya_zeta_0411623.pdf"]
    result = {
        "scope": "One paired exact p5 falsifier of elliptic-trace and unmarked-zeta shortcuts",
        "p": p, "r": r, "cases": cases,
        "distinct_conjugates": True, "isomorphism_equation_exact": True,
        "affine_point_bijection_exact": True,
        "same_full_zeta": "Follows from the proved Fp isomorphism; full zeta not computed",
        "source_sha256": {name: sha256((source_dir/name).read_bytes()).hexdigest()
                          for name in sources},
        "guards": {
            "full_zeta_executed": False, "quantum_algorithm_executed": False,
            "runtime_lower_bound": False, "general_classical_solution": False,
            "novelty": False, "separation": False,
            "marked_curve_algorithms_ruled_out": False,
        },
    }
    output = Path(__file__).with_suffix(".json")
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"p": p, "distinct_conjugates": True,
                      "genera": [c["sage_genus"] for c in cases],
                      "projective_counts": [c["projective_point_count"] for c in cases],
                      "output": str(output)}))


if __name__ == "__main__":
    main()
