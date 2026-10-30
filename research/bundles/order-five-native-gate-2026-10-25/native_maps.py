"""Public maps of y^2=x^5+c over F_p, p=4 mod 5.

This frontend evaluates on F_(p^2) Mumford divisors. It does not construct
an incoming isogeny, auxiliary torsion bases, or a geometric hiding source.
"""

from flint import fq_default_ctx, fq_default_poly_ctx
from sympy import isprime


class OrderFiveModel:
    def __init__(self, p, constant=-1):
        if type(p) is not int or p <= 5 or p % 5 != 4 or not isprime(p):
            raise ValueError("prime characteristic p>5 with p=4 mod 5 required")
        if type(constant) is not int or not constant % p:
            raise ValueError("nonzero prime-field constant required")
        self.p, self.constant = p, constant % p
        self.field = fq_default_ctx(p, 2, "u")
        self.polys = fq_default_poly_ctx(self.field)
        self.curve = self.polys([self.constant, 0, 0, 0, 0, 1])
        _, factors = self.polys([1, 1, 1, 1, 1]).factor()
        if len(factors) != 4 or any(f.degree() != 1 or e != 1 for f, e in factors):
            raise ArithmeticError("degree-two field did not split the fifth roots")
        roots = [-f[0]/f[1] for f, _ in factors]
        self.zeta = min(roots, key=lambda z: tuple(int(a) for a in z.to_list()))
        if self.zeta == 1 or self.zeta**5 != 1 or self.zeta**p != self.zeta**4:
            raise ArithmeticError("order-five/Frobenius certificate failed")

    def validate(self, divisor):
        u, v = divisor
        if (not 0 <= u.degree() <= 2 or u.leading_coefficient() != 1
                or v.degree() >= u.degree() or (self.curve-v*v) % u != 0):
            raise ValueError("reduced Mumford divisor on the supplied curve required")
        return divisor

    def gamma(self, divisor, power=1):
        u, v = self.validate(divisor)
        z = self.zeta**(power % 5)
        degree = u.degree()
        moved = (self.polys([u[i]*z**(degree-i) for i in range(degree+1)]),
                 self.polys([v[i]*z**(-i) for i in range(v.degree()+1)]))
        return self.validate(moved)

    def frobenius(self, divisor):
        u, v = self.validate(divisor)
        moved = (self.polys([u[i]**self.p for i in range(u.degree()+1)]),
                 self.polys([v[i]**self.p for i in range(v.degree()+1)]))
        return self.validate(moved)

    def from_points(self, points):
        if len(points) > 2:
            raise ValueError("at most two affine points in this control adapter")
        for x, y in points:
            if y*y != self.curve(x):
                raise ValueError("point is not on the supplied curve")
        if not points:
            return self.polys([1]), self.polys([])
        x, y = points[0]
        if len(points) == 1:
            return self.validate((self.polys([-x, 1]), self.polys([y])))
        a, b = points[1]
        if a == x:
            raise ValueError("distinct x coordinates required by the interpolation adapter")
        slope = (b-y)/(a-x)
        return self.validate((self.polys([x*a, -x-a, 1]), self.polys([y-slope*x, slope])))

    def certificate(self, ell):
        if type(ell) is not int or ell in (2, 5, self.p) or not isprime(ell):
            raise ValueError("odd prime ell distinct from 5 and the characteristic required")
        indices = [self.p-1, self.p-2, 2*self.p-1, 2*self.p-2]
        if any(index % 5 == 0 for index in indices):
            raise ArithmeticError("Cartier support certificate failed")
        return {
            "status": "PUBLIC_MAPS_SUPPLIED_CONDITIONAL_WORD_ATTACK",
            "characteristic": self.p, "constant": self.constant, "ell": ell,
            "map_field_degree_over_prime_field": 2,
            "gamma_characteristic_polynomial": [1, 1, 1, 1, 1],
            "squared_rosati_norm_bounds": [4, 4*self.p],
            "cartier_coefficient_indices_mod_five": [i % 5 for i in indices],
            "cartier_matrix_zero_by_support": True,
            "target_word_depth_bound": 2,
            "hiding_function_queries_required": 0,
            "incoming_isogeny_constructed": False,
            "auxiliary_torsion_basis_backend_implemented": False,
            "native_kernel_recovered": False,
            "independent_review_completed": False,
        }


def finite_points(model, cap=1000):
    """Exhaustive, explicitly capped geometry reference; not the algorithm."""
    if model.p**2 > cap:
        raise ValueError("finite point-control field cap exceeded")
    points = []
    for a in range(model.p):
        for b in range(model.p):
            x = model.field([a, b])
            value = model.curve(x)
            if value.is_square():
                y = value.sqrt()
                points.append((x, y))
                if y != 0:
                    points.append((x, -y))
    return tuple(points)
