"""Exact finite public-basis audit, not an asymptotic or quantum solver."""

from fractions import Fraction
from math import isqrt


def negacyclic(a):
    d = len(a)
    if not d or d & (d - 1):
        raise ValueError("power-of-two dimension required")
    return [[a[(i-j) % d] * (-1 if i < j else 1)
             for j in range(d)] for i in range(d)]


def primal_rows(a, q):
    if q < 3 or q % 2 == 0:
        raise ValueError("odd modulus at least three required")
    d = len(a)
    centered = [(x + q//2) % q - q//2 for x in a]
    c = negacyclic(centered)
    return [[int(i == j) for j in range(d)] + [c[j][i] for j in range(d)]
            for i in range(d)] + [
                [0]*d + [q*int(i == j) for j in range(d)] for i in range(d)]


def exact_profile(rows):
    """Square-basis wrapper retained for the primal source certificate."""
    n = len(rows)
    if not n or any(len(row) != n for row in rows):
        raise ValueError("square full-rank basis required")
    return exact_row_profile(rows)


def exact_row_profile(rows):
    """Bareiss GS profile, including full-row-rank rectangular embeddings."""
    n = len(rows)
    if not n or len(rows[0]) < n or any(len(row) != len(rows[0]) for row in rows):
        raise ValueError("nonempty full-row-rank rectangular basis required")
    a = [[sum(x*y for x, y in zip(left, right))
          for right in rows] for left in rows]
    previous = 1
    pivots, squared, mu = [], [], [[Fraction(0) for _ in rows] for _ in rows]
    for k in range(n):
        pivot = a[k][k]
        if pivot <= 0:
            raise ValueError("singular basis")
        pivots.append(pivot)
        squared.append(Fraction(pivot, previous))
        for j in range(k+1, n):
            mu[j][k] = Fraction(a[k][j], pivot)
        for i in range(k+1, n):
            for j in range(i, n):
                quotient, remainder = divmod(
                    pivot*a[i][j] - a[i][k]*a[k][j], previous)
                if remainder:
                    raise ArithmeticError("nonintegral Bareiss step")
                a[i][j] = a[j][i] = quotient
        previous = pivot
    return {"leading_gram_determinants": pivots, "gs_squared": squared, "mu": mu}


def nearest_plane(rows, target, profile=None):
    """Exact rational Babai; no floating projection or rounded inverse."""
    n = len(rows)
    if not n or len(target) != len(rows[0]):
        raise ValueError("target dimension mismatch")
    profile = exact_row_profile(rows) if profile is None else profile
    mu, gs = profile["mu"], profile["gs_squared"]
    inner = []
    for i, row in enumerate(rows):
        inner.append(sum(x*y for x, y in zip(row, target)) -
                     sum(mu[i][j]*inner[j] for j in range(i)))
    coordinates = [inner[i]/gs[i] for i in range(n)]
    integers = [0]*n
    for i in range(n-1, -1, -1):
        value = coordinates[i]
        integers[i] = (2*value.numerator + value.denominator)//(2*value.denominator)
        for j in range(i):
            coordinates[j] -= integers[i]*mu[i][j]
    point = [sum(integers[i]*rows[i][j] for i in range(n)) for j in range(len(target))]
    return {"point": point, "residual": [x-y for x, y in zip(target, point)],
            "basis_coefficients": integers}


def dyadic_tail_bound(gs_squared, width_squared):
    """pi>3 and e>2^(36/25) give exponent floor(27*l^2/(25h))."""
    width_squared = Fraction(width_squared)
    if width_squared <= 0 or any(x <= 0 for x in gs_squared):
        raise ValueError("positive GS and width bounds required")
    exponents = [int(27*Fraction(x)/(25*width_squared)) for x in gs_squared]
    # Raise tiny terms to a positive dyadic floor, never underflow them to zero.
    cap = 4096
    uncapped = sum((Fraction(2, 2**min(k, cap)) for k in exponents), Fraction(0))
    return {"failure_upper": min(Fraction(1), uncapped),
            "uncapped_union_upper": uncapped, "dyadic_exponents": exponents,
            "union_exponent_cap": cap}


def mixture_tail_bound(d, gs_squared, log_dimension_upper):
    """Unconditional shared-shape Chernoff bound, without revealing H."""
    l = Fraction(log_dimension_upper)
    base = l*l + Fraction(d, 2)*l**4
    records, total = [], Fraction(0)
    for squared in gs_squared:
        squared = Fraction(squared)
        if squared <= 0:
            raise ValueError("positive GS norms required")
        root = isqrt(squared.numerator//squared.denominator)
        radius = Fraction(root, 2)
        if not radius:
            records.append({"radius_lower": radius, "chernoff_parameter": Fraction(0),
                            "mixture_denominator_loss": Fraction(0),
                            "dyadic_exponent": 0, "tail_upper": Fraction(1)})
            total += 1
            continue
        v = 6*radius/base
        alpha = d*l*l*v*v/144
        while alpha > Fraction(1, 2):
            v /= 2
            alpha /= 4
        exponent = int(Fraction(36, 25)*(v*radius-base*v*v/12))
        assert exponent >= 0
        tail = min(Fraction(1), Fraction(2, 2**min(exponent, 4096))/(1-alpha))
        records.append({"radius_lower": radius, "chernoff_parameter": v,
                        "mixture_denominator_loss": alpha,
                        "dyadic_exponent": exponent, "tail_upper": tail})
        total += tail
    return {"base_width_squared_upper": base, "directions": records,
            "failure_upper": min(Fraction(1), total),
            "uncapped_union_upper": total, "union_exponent_cap": 4096,
            "secret_error_independent_only_conditionally_on_shape": True,
            "hidden_shape_given_to_decoder": False}


def source_certificate(d, gs_squared, log_dimension_upper):
    """Certify log(d)<L using e>163/60; no experimental fit is allowed."""
    if d < 4 or d & (d-1) or len(gs_squared) != 2*d:
        raise ValueError("native power-of-two dimension and 2d profile required")
    l = Fraction(log_dimension_upper)
    if l <= 0 or Fraction(163, 60)**l.numerator <= d**l.denominator:
        raise ValueError("rational log upper bound must pass (163/60)^p>d^r")
    # d^(3/2) <= d*ceil(sqrt(d)), including nonsquare powers of two.
    root = isqrt(d)
    root += root*root != d
    rho_squared = (d*root + 1)*l*l
    spherical = dyadic_tail_bound(gs_squared, rho_squared)
    # Each latent Z=x^2+y^2 has tail exp(-2*pi*z). Union over d/2 pairs.
    z = 2
    shape_exponent = int(Fraction(216*z, 25))
    shape_loss = min(Fraction(1), Fraction(d, 2*2**shape_exponent))
    h_cap = l*l + Fraction(d, 2)*l*l*(l*l+z)
    elliptical = dyadic_tail_bound(gs_squared, h_cap)
    mixture = mixture_tail_bound(d, gs_squared, l)
    conditioned_total = min(Fraction(1), shape_loss+elliptical["failure_upper"])
    return {"spherical": {**spherical, "width_squared_upper": rho_squared},
            "elliptical": {**elliptical, "width_squared_upper": h_cap,
                           "latent_radius_squared": z, "shape_failure_upper": shape_loss,
                           "shape_dyadic_exponent": shape_exponent,
                           "shape_conditioned_total_upper": conditioned_total,
                           "unconditional_mixture": mixture,
                           "total_failure_upper": min(conditioned_total, mixture["failure_upper"])}}
