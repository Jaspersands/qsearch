"""Exact rational, uniform tanh approximation certificates for transfer products.

Dyadic multipoles are classical prior art. This variant exposes every error
term using rational arithmetic; it does not compile complex transfer roots.
"""

from fractions import Fraction as Q
from math import comb


def exact(value):
    if isinstance(value, bool) or not isinstance(value, (int, Q)):
        raise TypeError("int/Fraction input required")
    return Q(value)


def atan_interval(denominator, terms):
    total = sum((Q((-1)**j, (2*j+1)*denominator**(2*j+1)) for j in range(terms)), Q(0))
    other = total+Q((-1)**terms, (2*terms+1)*denominator**(2*terms+1))
    return min(total, other), max(total, other)


def pi_squared_quarter(tolerance):
    tolerance = exact(tolerance)
    if not 0 < tolerance < 1:
        raise ValueError("relative tolerance must be between zero and one")
    terms = 1
    while True:
        a, b = atan_interval(5, terms), atan_interval(239, terms)
        lo, hi = 16*a[0]-4*b[1], 16*a[1]-4*b[0]
        lo, hi = lo*lo/4, hi*hi/4
        relative = (hi-lo)/(2*lo)
        if lo >= 2 and relative <= tolerance:
            return {"lo": lo, "hi": hi, "midpoint": (lo+hi)/2,
                    "relative_error_upper": relative, "machin_terms": terms}
        terms += 1


def power_sums(stop, degree):
    """Sum n^k for 0<=n<stop without iterating to stop."""
    answer = []
    for k in range(degree+1):
        numerator = stop**(k+1)-sum(comb(k+1, j)*answer[j] for j in range(k))
        value, remainder = divmod(numerator, k+1)
        if remainder:
            raise ArithmeticError("power-sum divisibility failed")
        answer.append(value)
    return answer


def block_moments(low, high, order):
    left, right = power_sums(low, 2*(order-1)), power_sums(high+1, 2*(order-1))
    sums = [b-a for a, b in zip(left, right)]
    center = Q((2*low+1)**2+(2*high+1)**2, 2)
    base, coefficients, moments = [1-center, Q(4), Q(4)], [Q(1)], []
    for _ in range(order):
        moments.append(sum((a*sums[j] for j, a in enumerate(coefficients)), Q(0)))
        updated = [Q(0)]*(len(coefficients)+2)
        for j, value in enumerate(coefficients):
            for k, coefficient in enumerate(base):
                updated[j+k] += value*coefficient
        coefficients = updated
    return center, moments


def construct(max_x, error):
    max_x, error = exact(max_x), exact(error)
    if max_x <= 0 or not 0 < error <= Q(1, 4):
        raise ValueError("need max_x>0 and 0<error<=1/4")
    constant = pi_squared_quarter(error/16)
    c = constant["midpoint"]
    order = 1
    while 2*Q(3, 5)**order > error/4:
        order += 1
    groups = 1
    while (1 << groups)-1 < 2*max_x/error:
        groups += 1
    cutoff = (1 << groups)-1
    blocks = []
    for b in range(groups):
        low, high = (1 << b)-1, (1 << (b+1))-2
        center, moments = block_moments(low, high, order)
        spread = Q((2*high+1)**2-(2*low+1)**2, 2)
        if spread > Q(3, 5)*center:
            raise ArithmeticError("dyadic geometric ratio exceeds 3/5")
        blocks.append({"low": low, "high": high, "center": c*center,
                       "numerators": [2*(-c)**k*moment for k, moment in enumerate(moments)]})
    relative = constant["relative_error_upper"]
    budgets = {"constant_error_upper": relative/(1-relative),
               "geometric_error_upper": 2*Q(3, 5)**order,
               "tail_error_upper": max_x/(c*(2*cutoff-1))}
    total = sum(budgets.values(), Q(0))
    if total > error:
        raise ArithmeticError("uniform approximation budget not met")
    return {"max_x": max_x, "requested_error": error, "pi_squared_quarter": constant,
            "order": order, "groups": groups, "effective_pole_count": cutoff,
            "transfer_degree_upper": 2*groups*order, "blocks": blocks, **budgets,
            "uniform_error_upper": total, "denominator_positive_on_real_axis": True,
            "factor_roots_compiled": False, "full_sampler_executed": False}


def evaluate(certificate, x):
    x = exact(x)
    if abs(x) > certificate["max_x"]:
        raise ValueError("outside certified interval")
    value = Q(0)
    for block in certificate["blocks"]:
        denominator = x*x+block["center"]
        power = denominator
        for numerator in block["numerators"]:
            value += x*numerator/power
            power *= denominator
    return value


def native_certificate(couplings, radius, beta, error):
    couplings = tuple(exact(j) for j in couplings)
    beta, error = exact(beta), exact(error)
    if len(couplings) < 2 or any(not j or abs(j) > 1 for j in couplings):
        raise ValueError("invalid native couplings")
    if type(radius) is not int or not 1 <= radius < len(couplings):
        raise ValueError("invalid radius")
    if beta <= 0 or not 0 < error <= Q(1, 4):
        raise ValueError("positive beta required; beta zero needs only the native vacuum")
    alpha = (len(couplings)+radius)//(radius+1)
    approximation = construct(beta*sum(map(abs, couplings))/2, error/(4*alpha))
    return {"couplings": couplings, "radius": radius, "beta": beta, "target_error": error,
            "mode_count": alpha, "approximation": approximation,
            "thermal_squared_state_error_upper": alpha*approximation["uniform_error_upper"]**2,
            "complex_factor_sampler_implemented": False,
            "quantum_advantage_claim": False,
            "uniform_polynomial_sampler_claim": False}


def integer_transfer_polynomial(certificate, beta=Q(1)):
    """Expand p(z)=E((beta*z/2)^2)-(beta*z/2)B((beta*z/2)^2)."""
    import sympy as sp

    beta = exact(beta)
    if beta <= 0:
        raise ValueError("positive beta required")
    y, z = sp.symbols("y z")
    denominator = sp.Poly(1, y, domain=sp.QQ)
    factors = []
    for block in certificate["blocks"]:
        center = block["center"]
        factor = sp.Poly(y+sp.Rational(center.numerator, center.denominator), y, domain=sp.QQ)
        factors.append(factor)
        denominator *= factor**certificate["order"]
    numerator = sp.Poly(0, y, domain=sp.QQ)
    for block, factor in zip(certificate["blocks"], factors):
        power = factor
        for value in block["numerators"]:
            if value:
                numerator += sp.Rational(value.numerator, value.denominator)*denominator.exquo(power)
            power *= factor
    scale = sp.Rational(beta.numerator, 2*beta.denominator)
    expression = denominator.as_expr().subs(y, scale**2*z**2)-scale*z*numerator.as_expr().subs(y, scale**2*z**2)
    _, integer = sp.Poly(expression, z, domain=sp.QQ).clear_denoms(convert=True)
    _, integer = integer.primitive()
    coefficients = list(reversed([int(a) for a in integer.all_coeffs()]))
    if coefficients[0] <= 0:
        raise ArithmeticError("positive even denominator lost")
    return coefficients


def ceil_log2(value):
    value = exact(value)
    if value <= 0:
        raise ValueError("positive value required")
    exponent = value.numerator.bit_length()-value.denominator.bit_length()
    power = Q(2)**exponent
    return exponent+int(power < value)


def root_rounding_plan(native):
    """Resource specification, NOT a root certificate or completed sampler."""
    expected = native_certificate(native["couplings"], native["radius"], native["beta"], native["target_error"])
    if native != expected:
        raise ValueError("native approximation record does not reproduce")
    coefficients = integer_transfer_polynomial(native["approximation"], native["beta"])
    m, factors, error = len(native["couplings"]), len(coefficients)-1, native["target_error"]
    if factors <= 0 or coefficients[0] <= 0:
        raise ValueError("nonconstant positive-normalized transfer polynomial required")
    root_bound = 1+max(Q(abs(a), coefficients[0]) for a in coefficients[1:])
    growth_bits = ceil_log2(root_bound+2)
    bits = ceil_log2(8*factors*m/error)+m*factors*growth_bits
    return {"transfer_factors": factors, "root_modulus_upper": root_bound,
            "root_disk_radius_target_bits": bits,
            "reference_pilot_norm_lower_from_positive_even_part": Q(1),
            "normalized_root_rounding_error_upper": error/4,
            "requires_all_root_disks_and_multiplicities": True,
            "root_disks_produced": False, "complex_sampler_executed": False}
