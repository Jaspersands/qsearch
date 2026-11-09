"""Finite falsifiers only; run with qsearch-cas/bin/python, not a Selmer solver."""
import json
from pathlib import Path
from sage.all import GF, ZZ, Zmod, PolynomialRing, matrix, identity_matrix, vector, prod


def dyadic_control():
    A = PolynomialRing(Zmod(8), "t")
    t = A.gen()
    B = A.quotient(t**2 - 2, "pi")
    pi = B.gen()
    gens = [1 + pi**j for j in range(1, 6)]
    units = [B(a) + b * pi for a in (1, 3, 5, 7) for b in range(8)]

    def key(z):
        return tuple(int(z.lift()[i]) for i in range(2))

    inverses = {key(u): next(v for v in units if u*v == 1) for u in units}

    def power(u, e):
        return u**e if e >= 0 else inverses[key(u)]**(-e)

    def phi(row):
        return prod((power(u, int(e)) for u, e in zip(gens, row)), B.one())

    def valuation(z):
        c = key(z)
        return min([6] + [2*ZZ(c[i]).valuation(2)+i for i in range(2) if c[i]])

    def digit(z, j):
        assert valuation(z) >= j
        return (key(z)[j % 2] // (2**(j//2))) % 2

    M = identity_matrix(ZZ, 5)
    indices = []
    for j in range(1, 6):
        bits = [digit(phi(row)-1, j) for row in M.rows()]
        if any(bits):
            pivot = bits.index(1)
            rows = []
            for i in range(5):
                row = vector(ZZ, 5)
                row[i] = 2 if i == pivot else 1
                if i != pivot:
                    row[pivot] = -bits[i]
                rows.append(row)
            M = (matrix(ZZ, rows)*M).hermite_form()
        assert all(valuation(phi(row)-1) >= j+1 for row in M.rows())
        indices.append(int(abs(M.det())))
    assert all(phi(row) == 1 for row in M.rows())
    assert abs(M.det()) == len(units) == 32
    W = M.change_ring(GF(2)).row_space()
    Q = W.ambient_vector_space().quotient(W)

    def coords(u):
        exponents = [0]*5
        for j in range(1, 6):
            bit = digit(u-1, j)
            exponents[j-1] = bit
            if bit:
                u *= inverses[key(gens[j-1])]
        assert u == 1
        return Q(vector(GF(2), exponents))

    squares = {key(u*u) for u in units}
    assert len(squares) == 4
    assert Q.dimension() == 3
    assert len({tuple(coords(u)) for u in units}) == 8
    assert all(coords(u*u).is_zero() for u in units)
    assert all(coords(u*v) == coords(u)+coords(v) for u in units for v in units)
    # Saturating a full-rank lattice returns Z^5 and erases all unit bits.
    assert M.row_module().saturation() == ZZ**5
    return {"field": "Q2(sqrt(2))", "level_indices": indices,
            "relation_matrix": [[int(x) for x in r] for r in M.rows()],
            "unit_count": 32, "unit_square_count": 4,
            "unit_squareclass_dimension": 3, "total_squareclass_dimension": 4,
            "all_products_homomorphism": True, "saturation_wrong_dimension": 0}


def native_family_control():
    R = PolynomialRing(ZZ, "x")
    x = R.gen()
    G = x**3-22*x**2-25*x-1
    H = G(x-4)
    B = R((H-G)/4)
    h = G+2*B
    f = x*G*H-B**2
    assert f.degree() == 7 and f.is_monic() and h.degree() == 3
    assert h**2+4*f == (1+4*x)*G*H
    assert G.discriminant() == 559**2 and G.is_irreducible()
    F = R(4**7*f(x/4)+4**6*h(x/4)**2)
    G4 = R(4**3*G(x/4))
    assert F == (x+1)*G4*G4(x-16)
    checks = {}
    for p in (2, 3, 5, 7):
        gp = G.change_ring(GF(p))
        assert gp.is_irreducible()
        checks[str(p)] = {"G_irreducible": True}
        if p != 2:
            assert gp != gp(gp.parent().gen()-4)
            assert F.discriminant() % p != 0
            checks[str(p)]["F_separable"] = True
    hb, fb = h.change_ring(GF(2)), f.change_ring(GF(2))
    smooth = hb.gcd(hb.derivative()**2*fb+fb.derivative()**2)
    assert smooth == 1

    # Exact tangent columns at the sufficient residue size; no norms,
    # complete local image, Jacobian order or Selmer dimension is computed.
    g, a = 3, 1
    while 2**a < 1024*(g+1)**2:
        a += 2
    k = GF(2**a, "z")
    z = k.gen()
    hk, fk = h.change_ring(k), f.change_ring(k)
    selected = []
    allowed_x = 0
    for v in k:
        hv = hk(v)
        if hv == 0 or (fk(v)/hv**2).trace() != 0:
            continue
        allowed_x += 1
        if len(selected) < g:
            for j in range(a):
                col = vector(GF(2), [(z**j*v**ell/hv).trace() for ell in range(g)])
                if matrix(GF(2), selected+[col]).rank() > len(selected):
                    selected.append(col)
    assert len(selected) == g and allowed_x > g
    return {"G": str(G), "G_discriminant": int(G.discriminant()),
            "global_factor_degrees": [1, 3, 3], "genus": 3,
            "small_prime_checks": checks, "dyadic_affine_smoothness_gcd": str(smooth),
            "infinity_smooth_from_monic_odd_model": True,
            "residue_degree": a, "residue_size": int(k.cardinality()),
            "allowed_distinct_x": allowed_x, "tangent_rank": len(selected)}


result = {"scope": "Exact finite falsifiers, not full local/Selmer or quantum execution",
          "dyadic": dyadic_control(), "native_family": native_family_control(),
          "claims": {"asymptotic_from_control": False, "quantum_execution": False,
                     "selmer_dimension_computed": False, "speedup": False}}
out = Path(__file__).with_suffix(".json")
out.write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps(result, separators=(",", ":")))
