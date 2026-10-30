"""Exact ideal-lattice falsifiers; no native curve or hidden-label oracle."""

from sympy import Matrix, Rational, diag


# O = Z[w], w^2-w+6=0; I=(2,w); J=(2,w-1)=conjugate(I).
OMEGA_O = Matrix([[0, -6], [1, 1]])
OMEGA_I = Matrix([[0, -3], [2, 1]])
OMEGA_J = Matrix([[1, -3], [2, 0]])
PAIRING = Matrix([[0, 1], [-1, 0]])
GRAM_O = Matrix([[2, 1], [1, 12]])
GRAM_I = Matrix([[4, 1], [1, 6]])
GRAM_J = Matrix([[4, -1], [-1, 6]])


def intertwiner(x, y):
    """All O-linear maps O -> I in the displayed integral bases."""
    return Matrix([[x, -3*y], [y, 2*x+y]])


def index_form(x, y):
    return 2*x*x+x*y+3*y*y


def rational_charts():
    """Norm-one maps integral at odd primes, respectively at 2."""
    return (intertwiner(Rational(1, 2), -Rational(1, 2)),
            intertwiner(-Rational(2, 3), Rational(1, 3)))


def paired_local_isomorphism(modulus):
    """A compatible SL2(Z/m) intertwiner, polynomial in log(m).

    Glue the denominator-three chart at 2 to the denominator-two chart
    at odd primes. Only the 2-adic part is separated; no factoring oracle.
    """
    if type(modulus) is not int or modulus < 2:
        raise ValueError("modulus must be an integer >= 2")
    even = modulus & -modulus
    odd = modulus // even
    if even == 1:
        x = pow(2, -1, odd)
        y = -x
    elif odd == 1:
        y = pow(3, -1, even)
        x = -2*y
    else:
        inv3 = pow(3, -1, even)
        inv2 = pow(2, -1, odd)

        def glue(at_two, at_odd):
            return (at_two + even*((at_odd-at_two)*pow(even, -1, odd) % odd)) % modulus

        x = glue(-2*inv3, inv2)
        y = glue(inv3, -inv2)
    return intertwiner(x, y).applyfunc(lambda value: int(value) % modulus)


def stable_isomorphism():
    """Supplied O-linear unimodular map I+J -> O+O, NOT an isometry."""
    return Matrix([[2, 0, 2, -1], [0, 1, 0, 1],
                   [-1, -3, 0, -3], [1, 0, 1, 0]])


def vanishes_mod(matrix, modulus):
    if type(modulus) is not int or modulus < 2:
        raise ValueError("modulus must be an integer >= 2")
    if any(entry.is_Integer is not True for entry in matrix):
        raise ValueError("modular certificates require integral entries")
    return all(int(entry) % modulus == 0 for entry in matrix)


def check_local(modulus):
    transform = paired_local_isomorphism(modulus)
    checks = {
        "orientation": vanishes_mod(OMEGA_I*transform-transform*OMEGA_O, modulus),
        "unit_determinant": int(transform.det()) % modulus == 1,
        "pairing": vanishes_mod(transform.T*PAIRING*transform-PAIRING, modulus),
        "doubled_metric": vanishes_mod(transform.T*GRAM_I*transform-GRAM_O, modulus),
    }
    if not all(checks.values()):
        raise AssertionError(checks)
    return {"modulus": modulus, "checks": checks}


def stable_certificate():
    transform = stable_isomorphism()
    unpolarized = diag(OMEGA_O, OMEGA_O)*transform == transform*diag(OMEGA_I, OMEGA_J)
    polarized = transform.T*diag(GRAM_O, GRAM_O)*transform == diag(GRAM_I, GRAM_J)
    if transform.det() != 1 or not unpolarized or polarized:
        raise AssertionError("stable product control failed")
    return {"integral_determinant": 1, "orientation_preserved": unpolarized,
            "product_metric_preserved": polarized,
            "all_product_isometries_excluded_by_written_minimum_proof": True}
