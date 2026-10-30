"""Independent function-space controls of the one-point plane adapter.

The hyperelliptic equations are supplied controls, not recovered native
genus41 geometry. All section relations use exact polynomial arithmetic.
"""

from functools import lru_cache

from flint import nmod_mat, nmod_poly
from sympy import Poly, groebner, symbols


t, eta, X, Y = symbols("t eta X Y")


class CurveControl:
    def __init__(self, genus, prime=17):
        self.genus, self.prime = genus, prime
        self.ell, self.m, self.n = 2*genus+2, 2*genus+1, 2*genus+2
        coefficients = [2, 2]+[0]*(2*genus-1)+[1]
        f = nmod_poly(coefficients, prime)
        assert f.gcd(f.derivative()).degree() == 0
        self.relation = groebner([eta**2-t**(2*genus+1)-2*t-2], eta, t, modulus=prime)

    @lru_cache(None)
    def basis(self, degree):
        bound = degree*self.ell
        return tuple(sorted(((a, b) for b in (0, 1) for a in range(bound//2+1)
                             if 2*a+self.m*b <= bound), key=lambda pair: 2*pair[0]+self.m*pair[1]))

    def coordinates(self, expression, degree):
        reduced = self.relation.reduce(expression.expand())[1]
        polynomial = Poly(reduced, t, eta, modulus=self.prime)
        values = {pair: int(coefficient) % self.prime for pair, coefficient in polynomial.terms()}
        assert all(pair in self.basis(degree) for pair, value in values.items() if value)
        return [values.get(pair, 0) for pair in self.basis(degree)]

    def expression(self, row, degree):
        return sum(value*t**a*eta**b for value, (a, b) in zip(row, self.basis(degree)))

    def span(self, rows):
        matrix, rank = nmod_mat(rows, self.prime).rref()
        return [[int(matrix[i, j]) for j in range(matrix.ncols())] for i in range(rank)]

    def kernel(self, rows):
        matrix = nmod_mat(rows, self.prime)
        null, dimension = matrix.nullspace()
        return [[int(null[i, j]) for i in range(matrix.ncols())] for j in range(dimension)]

    @lru_cache(None)
    def monomial_product(self, i, j):
        a, b = self.basis(2)[i]
        c, d = self.basis(2)[j]
        return tuple(self.coordinates(t**(a+c)*eta**(b+d), 4))

    def multiply(self, left, right):
        out = [0]*len(self.basis(4))
        for i, a in enumerate(left):
            if not a:
                continue
            for j, b in enumerate(right):
                if b:
                    out = [(x+a*b*y) % self.prime for x, y in zip(out, self.monomial_product(i, j))]
        return out

    def product_span(self, left, right):
        return self.span([self.multiply(a, b) for a in left for b in right])

    def colon(self, target, divisor):
        dual = self.kernel(target)
        identity = self.identity()
        constraints = []
        for word in divisor:
            products = [self.multiply(e, word) for e in identity]
            for test in dual:
                constraints.append([sum(x*y for x, y in zip(value, test)) % self.prime for value in products])
        assert constraints
        return self.span(self.kernel(constraints))

    def identity(self):
        size = len(self.basis(2))
        return [[int(i == j) for j in range(size)] for i in range(size)]

    def one_point_spaces(self, denominator=None):
        identity = self.identity()
        spaces = {0: identity, 1: identity[:-1]}
        # At infinity only the top-pole monomial has nonzero evaluation
        # in the2H fiber. Later multiplicities come from product/colon.
        for j in range(1, self.ell):
            spaces[j+1] = self.colon(self.product_span(spaces[j], spaces[1]), identity)
        h = identity[0] if denominator is None else self.coordinates(denominator, 2)
        assert any(h) and nmod_mat(spaces[self.ell]+[h], self.prime).rank() == len(spaces[self.ell])
        hR2 = self.product_span([h], identity)
        numerators = {j: self.colon(hR2, spaces[j]) for j in (self.m-1, self.m, self.n)}
        return spaces, numerators

    def plane_relation(self):
        monomials = [(i, j) for j in range(self.m+1)
                     for i in range(((self.m-j)*self.n)//self.m+1)]
        # Here h=1, z_x=eta, z_y=t^(g+1), all as2H-sections.
        rows = [self.coordinates(eta**i*t**((self.genus+1)*j), 2*self.n) for i, j in monomials]
        kernel = self.kernel(list(map(list, zip(*rows))))
        assert len(kernel) == 1
        leading = monomials.index((0, self.m))
        coefficient = kernel[0][leading]
        assert coefficient
        coefficients = [c*pow(coefficient, -1, self.prime) % self.prime for c in kernel[0]]
        expression = sum(c*X**i*Y**j for c, (i, j) in zip(coefficients, monomials))
        expression = Poly(expression, X, Y, modulus=self.prime).as_expr()
        assert self.relation.reduce(expression.subs({X: eta, Y: t**(self.genus+1)}).expand())[1] == 0
        return expression, {"genus": self.genus, "prime": self.prime,
                            "pole_orders": [self.m, self.n], "monomial_count": len(monomials),
                            "relation_kernel_dimension": len(kernel),
                            "true_section_space_degree": 2*self.n,
                            "true_section_space_dimension": len(self.basis(2*self.n)),
                            "total_plane_degree": Poly(expression, X, Y).total_degree(),
                            "native_genus41_adapter_implemented": False}


def inseparable_control():
    """Replay the independent review's genus4 Artin--Schreier control."""
    w = symbols("w")
    ring = groebner([w**3-w-t**5], w, t, modulus=3)
    monomials = [(i, j) for j in range(10) for i in range((90-10*j)//9+1)]
    reductions = [Poly(ring.reduce((t**(3*i)*w**(2*j)).expand())[1], t, w, modulus=3)
                  for i, j in monomials]
    basis = sorted({power for polynomial in reductions for power, coefficient in polynomial.terms() if coefficient})
    rows = [[int(polynomial.coeff_monomial(t**a*w**b)) % 3 for a, b in basis] for polynomial in reductions]
    matrix = nmod_mat(list(map(list, zip(*rows))), 3)
    null, dimension = matrix.nullspace()
    assert len(monomials) == 56 and matrix.rank() == 55 and dimension == 1
    leading = monomials.index((0, 9))
    scale = pow(int(null[leading, 0]), -1, 3)
    equation = sum(int(null[k, 0])*scale*X**i*Y**j for k, (i, j) in enumerate(monomials))
    expected = Y**9+Y**6+Y**3-X**10
    assert Poly(equation-expected, X, Y, modulus=3).is_zero
    assert Poly(expected.diff(Y), X, Y, modulus=3).is_zero
    assert not Poly(expected.diff(X), X, Y, modulus=3).is_zero
    assert ring.reduce((w**2*(w**2-1)**2-t**10).expand())[1] == 0
    assert ring.reduce((w*(w**2-1)-t**5).expand())[1] == 0
    return {"curve": "w^3-w=t^5 over F3", "genus": 4,
            "x": "t^3", "y": "w^2", "pole_orders": [9, 10],
            "monomial_count": 56, "rank": 55, "relation_kernel_dimension": 1,
            "plane_equation": str(expected), "derivative_in_Y_is_zero": True,
            "symbolic_inverse_verified": True, "native_adapter_implemented": False}


def report():
    from hashlib import sha256
    from pathlib import Path

    root = Path(__file__).resolve().parent
    output = []
    for genus, prime in ((1, 17), (2, 17), (1, 3), (2, 5)):
        control = CurveControl(genus, prime)
        spaces, numerators = control.one_point_spaces()
        relation, data = control.plane_relation()
        data["equation_mod_p"] = str(relation)
        data["one_point_numerator_dimensions"] = {j: len(rows) for j, rows in numerators.items()}
        output.append(data)
    files = [root/name for name in ("plane_control.py", "test_plane_control.py", "PLANE.md", "REVIEW_RESOLUTION.md")]
    files += [root.parent/"matrix-lift-access-review-2026-10-26/PLANE_REVIEW.md",
              root.parent/"auxiliary-four-list-review-2026-10-26/COMPRESSED_REVIEW.md",
              root.parent/"compressed-graded-algebra-2026-10-26/REVIEW_RESOLUTION.md"]
    return {"status": "EXACT_SUPPLIED_CURVE_CONTROLS_NOT_NATIVE_ADAPTER", "controls": output,
            "inseparable_control": inseparable_control(),
            "native_genus41_group_order_computed": False,
            "quantum_advantage_established": False,
            "sha256": {str(path.relative_to(root.parent)): sha256(path.read_bytes()).hexdigest() for path in files}}


if __name__ == "__main__":
    import argparse
    from hashlib import sha256
    import json
    from pathlib import Path

    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--write", action="store_true")
    group.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = json.loads(json.dumps(report()))
    destination = Path(__file__).resolve().parent/"receipt.json"
    if args.write:
        destination.write_text(json.dumps(data, indent=2)+"\n")
    elif args.check:
        if json.loads(destination.read_text()) != data:
            raise SystemExit("FAIL: plane-adapter controls changed")
    else:
        print(json.dumps(data, indent=2))
    if args.write or args.check:
        print(f"PASS:4 supplied-curve and1 inseparable controls;{len(data['sha256'])} hashes;SHA256 {sha256(destination.read_bytes()).hexdigest()}")
