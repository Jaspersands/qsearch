"""Three prescribed classical algebra controls; run with qsearch-cas Python.

No quantum simulation or asymptotic inference from finite examples.
"""
import hashlib
import json
from pathlib import Path

from sage.all import (GF, QQ, CyclotomicField, Polyhedron, PolynomialRing,
                      cartesian_product, factorial, matrix)


ROOT = Path(__file__).resolve().parents[1]
SUPPORT = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1), (-1, -1, -1)]
polytope = Polyhedron(vertices=SUPPORT, base_ring=QQ)
volume = int(factorial(3) * polytope.volume())
rank = int(matrix(QQ, [[1, *u] for u in SUPPORT]).rank())
cases = []
for p in (41, 43):
    F = GF(p)
    ring = PolynomialRing(F, names=("x", "y", "z", "t"))
    x, y, z, t = ring.gens()
    xyz = x * y * z
    face_certificates = []
    for dim in range(4):
        for face in polytope.faces(dim):
            geometry = face.as_polyhedron()
            terms = [u for u in SUPPORT if geometry.contains(u)]
            # Multiply the Laurent face by the torus unit xyz.
            h = sum(x ** (u[0] + 1) * y ** (u[1] + 1) * z ** (u[2] + 1)
                    for u in terms)
            ideal = ring.ideal([h, x * h.derivative(x), y * h.derivative(y),
                                z * h.derivative(z), t * xyz - 1])
            empty = ideal.groebner_basis() == [ring.one()]
            assert empty
            face_certificates.append({"dimension": dim, "terms": len(terms),
                                      "unit_ideal": bool(empty)})
    # For each nonzero x,y, z obeys z^2+(1+x+y)z+1/(xy)=0.
    # Its nonzero constant term means every root is in the torus.
    count = 0
    for a in F:
        if not a:
            continue
        for b in F:
            if not b:
                continue
            disc = (1 + a + b) ** 2 - 4 / (a * b)
            count += 1 if disc == 0 else 2 if disc.is_square() else 0
    ambient = ((p - 1) ** 3 + 1) // p
    error = abs(count - ambient)
    bound = (volume - 1) * p
    # epsilon=1/2; square the fractional-power target for exact comparison.
    target_squared = QQ(p ** 3) / 4
    assert p >= (2 * (volume - 1)) ** 2
    assert error <= bound and error ** 2 <= target_squared
    cases.append({"p": p, "s": len(SUPPORT), "rho": rank, "volume": volume,
                  "all_faces": face_certificates, "count": count,
                  "ambient_count": ambient, "absolute_error": error,
                  "weight_bound": bound, "target_error_squared": str(target_squared),
                  "large_field_branch": True, "meets_target": True})

p = 41
degenerate_count = (p - 1) ** 2 + (p - 2) ** 2
ambient = p ** 2 - 3 * p + 3
gap = degenerate_count - ambient
assert gap == (p - 1) * (p - 2) and 2 * gap > p ** 2
guard = {"polynomial": "(1+x)(1+y+z)", "p": p, "s": 6, "rho": 4,
         "count": degenerate_count, "ambient_count": ambient, "error": gap,
         "target_error": str(QQ(p ** 2) / 2), "ambient_estimator_fails": True,
         "classically_exact_by_factorization": True}

# Prescribed fixed-order identity control. Brute counts check the formulas;
# this does not execute Pila's polylogarithmic algorithm.
p, g = 13, 4
F = GF(p)
a = next(a for a in F if a and (a ** ((p - 1) // g)).multiplicative_order() == g)
xi = a ** ((p - 1) // g)
K = CyclotomicField(g)
w = K.gen()
def character(value, exponent):
    value = F(value)
    if not value:
        return K.zero()
    label = next(k for k in range(g) if value ** ((p - 1) // g) == xi ** k)
    return w ** (label * exponent)

twists = {}
for i in range(g):
    for j in range(g):
        A, B = a ** i, a ** j
        # Z=1 affine chart, then all points at Z=0 represented by [u:1:0].
        projective = sum(A * u ** g + B * v ** g == 1 for u in F for v in F)
        projective += sum(A * u ** g + B == 0 for u in F)
        boundary = g * sum(c ** ((p - 1) // g) == 1 for c in (B, A, -B / A))
        torus = sum(A * u ** g + B * v ** g == 1
                    for u in F if u for v in F if v)
        assert projective - boundary == torus
        twists[i, j] = torus
J = {}
for e in range(g):
    for h in range(g):
        inverted = sum(w ** (i * e + j * h) * twists[i, j]
                       for i in range(g) for j in range(g)) / g ** 2
        direct = sum(character(x, e) * character(1 - x, h) for x in F)
        assert inverted == direct
        J[e, h] = inverted

def gauss_product(exponents):
    result, active = K.one(), 0
    for b in exponents:
        b %= g
        if b == 0:
            result *= -1
        elif active == 0:
            active = b
        elif (active + b) % g == 0:
            result *= character(-1, active) * p
            active = 0
        else:
            result *= J[active, b]
            active = (active + b) % g
    assert active == 0
    return result

simplex_support = [(0, 0, 0), (4, 0, 0), (0, 4, 0), (0, 0, 4)]
U = matrix(QQ, [[1, *u] for u in simplex_support]).transpose()
tuples = [e for e in cartesian_product([range(g)] * 4)
          if all(sum(U[i, j] * e[j] for j in range(4)) % g == 0 for i in range(4))]
gauss_sum = sum(gauss_product([-int(b) for b in e]) for e in tuples)
formula_count = ((p - 1) ** 3 + gauss_sum) / p
native_count = sum(1 + u ** 4 + v ** 4 + z ** 4 == 0
                   for u in F if u for v in F if v for z in F if z)
assert formula_count == native_count
simplex = {"p": p, "g": g, "s": 4, "rho": int(U.rank()),
           "polynomial": "1+x^4+y^4+z^4", "twists_checked": len(twists),
           "jacobi_identities_checked": len(J), "kernel_tuples": len(tuples),
           "character_formula_count": int(formula_count), "native_count": native_count,
           "pila_algorithm_executed": False, "all_exact": True}
source_names = ["maeda_pointcount_2608_23929", "sperber_voight_sparse_dwork",
                "pila_curve_families_0504570"]
hashes = {name: hashlib.sha256((ROOT / "audits/sources/legendre_prf" /
                              (name + ".pdf")).read_bytes()).hexdigest()
          for name in source_names}
report = {"contract": "finite classical controls only; no quantum execution or novelty",
          "nondegenerate_cases": cases, "degenerate_guard": guard,
          "fixed_order_identity_control": simplex, "source_pdf_sha256": hashes}
output = Path(__file__).with_suffix(".json")
output.write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps({"counts": [c["count"] for c in cases],
                  "errors": [c["absolute_error"] for c in cases],
                  "faces_per_case": [len(c["all_faces"]) for c in cases],
                  "degenerate_gap": gap, "simplex_count": native_count,
                  "jacobi_checks": len(J), "artifact": str(output)}))
