"""Small actual curve controls for the necessary quadratic field extension.

Uses SymPy finite-extension arithmetic; no custom field or isogeny engine.
The curves test descent, not quantum advantage or target-order reconstruction.
"""

from collections import defaultdict

from sympy import Poly, isprime, symbols
from sympy.polys.agca.extensions import MonogenicFiniteExtension


def twist_control(p):
    if not isprime(p) or p <= 3 or p % 4 != 3:
        raise ValueError("control requires prime p>3 with p=3 mod 4")
    t, u = symbols("t u")
    field = MonogenicFiniteExtension(Poly(t*t+1, t, modulus=p))
    values = [field.convert(a)+b*field.generator for a in range(p) for b in range(p)]
    squares = defaultdict(list)
    for y in values:
        squares[y*y].append(y)
    q = p*p
    nonsquare = next(d for d in values if d and d**((q-1)//2) == -field.one)
    reference = [(x, y) for x in values for y in squares[x**3+x]]
    twist = [(x, y) for x in values for y in squares[x**3+nonsquare**2*x]]
    extension = MonogenicFiniteExtension(Poly.from_list([field.one, field.zero, -nonsquare], u, domain=field))
    root = extension.generator
    def embed(a):
        return extension.convert(field.to_sympy(a))
    d = embed(nonsquare)
    mapped = [(d*embed(x), d*root*embed(y)) for x, y in reference]
    checks = {
        "maximal_reference_count": len(reference)+1 == (p+1)**2,
        "minimal_twist_count": len(twist)+1 == (p-1)**2,
        "different_base_point_counts": len(reference) != len(twist),
        "square_root_not_base_rational": root**q == -root and root**q != root,
        "square_root_rational_over_quadratic_extension": root**(q*q) == root,
        "mapped_points_on_twist": all(y*y == x**3+d*d*x for x, y in mapped),
        "map_conjugates_to_its_negative": all(x**q == x and y**q == -y for x, y in mapped),
        "map_not_base_rational_witness": any(y**q != y for _, y in mapped),
        "mapped_points_quadratic_rational": all(x**(q*q) == x and y**(q*q) == y for x, y in mapped),
    }
    if not all(checks.values()):
        raise AssertionError(checks)
    return {"p": p, "base_field_size": q,
            "reference_points": len(reference)+1, "twist_points": len(twist)+1,
            "nonsquare": str(field.to_sympy(nonsquare)), "checks": checks,
            "higher_dimensional_geometric_conversion_executed": False}
