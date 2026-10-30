"""Uniform elliptic source-field deduction and exact twist countercontrols.

No hidden isogeny, finite-field embedding, or theta-model construction is run.
"""

from functools import lru_cache

from sympy import Poly, isprime, symbols
from sympy.polys.agca.extensions import MonogenicFiniteExtension


def _parameters(p, base_degree):
    if type(p) is not int or p <= 3 or not isprime(p):
        raise ValueError("prime characteristic > 3 required")
    if type(base_degree) is not int or base_degree < 1:
        raise ValueError("positive explicitly represented base-field degree required")
    return p**base_degree


def supersingular_trace_classes(p, base_degree):
    """Necessary classes, not a claim every class occurs for every p."""
    _parameters(p, base_degree)
    if base_degree % 2:
        return (0,)
    root = p**(base_degree//2)
    return tuple(k*root for k in (-2, -1, 0, 1, 2))


def frobenius_power(p, base_degree, trace, exponent):
    """Return a+b*pi using the actual supersingular minimal-polynomial cases."""
    q = _parameters(p, base_degree)
    if type(trace) is not int or trace not in supersingular_trace_classes(p, base_degree):
        raise ValueError("trace violates the supersingular class restriction")
    if type(exponent) is not int or exponent < 0:
        raise ValueError("nonnegative exponent required")
    if trace*trace == 4*q:
        # End^0(E) has no nonzero nilpotents, so pi=trace/2. The repeated
        # characteristic polynomial alone would leave a spurious nilpotent.
        return ((trace//2)**exponent, 0)
    a, b = 1, 0
    for _ in range(exponent):
        a, b = -q*b, a+trace*b
    return a, b


def normalization_plan(p, base_degree, levels):
    q = _parameters(p, base_degree)
    levels = tuple(levels)
    if len(set(levels)) != len(levels):
        raise ValueError("duplicate auxiliary levels")
    rows = []
    for r, exponent in levels:
        if (type(r) is not int or not isprime(r) or r == p
                or type(exponent) is not int or exponent not in (1, 2)):
            raise ValueError("unramified prime or prime-square levels required")
        extension = r**(exponent-1)*(r-1)
        order = r**exponent
        assert pow(q, 6*extension, order) == 1
        rows.append({"prime": r, "exponent": exponent, "torsion_order": order,
                     "relative_auxiliary_degree": extension,
                     "absolute_auxiliary_degree": 12*base_degree*extension})
    scalar = q**6
    for trace in supersingular_trace_classes(p, base_degree):
        assert frobenius_power(p, base_degree, trace, 12) == (scalar, 0)
    assert scalar % 8 == 1
    return {"characteristic": p, "input_base_degree": base_degree,
            "relative_base_extension": 12, "fixed_base_degree": 12*base_degree,
            "fixed_frobenius_scalar": scalar, "fixed_scalar_mod_8": scalar % 8,
            "common_field_for_unknown_phi_given_as_input": False,
            "scope": "SUPERSINGULAR_ELLIPTIC_ENDPOINTS_OVER_ONE_EXPLICIT_FIELD",
            "auxiliary_fields": rows,
            "sum_separate_auxiliary_degrees": sum(x["absolute_auxiliary_degree"] for x in rows),
            "supersingularity_verified_by_plan": False,
            "field_embeddings_constructed": False, "unknown_isogeny_constructed": False,
            "compositum_of_auxiliary_fields_constructed": False}


@lru_cache(maxsize=1)
def twist_countercontrol():
    """Two actual F_121 curves have OPPOSITE scalar Frobenius over F_(11^12)."""
    u, x = symbols("u x")
    field = MonogenicFiniteExtension(Poly(u*u+1, u, modulus=11))
    values = [field(a)+b*field.generator for a in range(11) for b in range(11)]
    squares = {v*v for v in values if v}
    coefficients = ((field.one+field.generator, field.zero),
                    (field.zero, field.one+2*field.generator))
    records = []
    for a, b in coefficients:
        discriminant_part = 4*a**3+27*b**2
        assert discriminant_part
        points = 1
        for xx in values:
            rhs = xx**3+a*xx+b
            points += 1 if not rhs else 2 if rhs in squares else 0
        polynomial = Poly.from_list([field.one, field.zero, a, b], x, domain=field)
        hasse = field.convert((polynomial**5).nth(10))
        assert not hasse
        trace = 122-points
        records.append({"a": str(a), "b": str(b), "points_over_F121": points,
                        "trace": trace, "hasse_invariant_zero": not hasse,
                        "frobenius_power_6": list(frobenius_power(11, 2, trace, 6)),
                        "frobenius_power_12": list(frobenius_power(11, 2, trace, 12))})
    assert [x["trace"] for x in records] == [0, 11]
    assert records[0]["frobenius_power_6"] == [-11**6, 0]
    assert records[1]["frobenius_power_6"] == [11**6, 0]
    assert all(x["frobenius_power_12"] == [11**12, 0] for x in records)
    return {"field": "F_11[u]/(u^2+1)", "curves": records,
            "relative_degree_6_makes_each_endomorphism_ring_defined": True,
            "relative_degree_6_defines_maps_between_fixed_endpoints": False,
            "relative_degree_12_matches_endpoint_frobenius": True,
            "actual_point_counts_computed": True, "isogeny_computed": False,
            "source_promise_repair_independently_reviewed": False}
