"""Arithmetic controls for weak PPAV marks, NOT an isogeny implementation.

Inputs to normalize_pairings are already computed Weil-pairing exponents.
Obtaining points, pairings, discrete logarithms, theta models and an actual
Theorem 7.1 interpolator remains outside this module.
"""

from itertools import product
from math import gcd, isqrt


def _positive(value, name):
    if type(value) is not int or value < 1:
        raise ValueError(f"{name} must be a positive integer")


def is_prime(value):
    if type(value) is not int or value < 2:
        return False
    return all(value % d for d in range(2, isqrt(value) + 1))


def rank_mod(matrix, prime):
    rows = [list(row) for row in matrix]
    rank = 0
    for col in range(len(rows[0])):
        pivot = next((j for j in range(rank, len(rows)) if rows[j][col] % prime), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        scale = pow(rows[rank][col] % prime, -1, prime)
        rows[rank] = [(x * scale) % prime for x in rows[rank]]
        for j in range(len(rows)):
            if j != rank:
                coefficient = rows[j][col]
                rows[j] = [(a - coefficient * b) % prime
                           for a, b in zip(rows[j], rows[rank])]
        rank += 1
    return rank


def _pairing_matrix(matrix, prime):
    dimension = len(matrix)
    if not dimension or dimension % 2 or any(len(row) != dimension for row in matrix):
        raise ValueError("pairing matrix must be nonempty, square and even-dimensional")
    if any(type(x) is not int or not 0 <= x < prime for row in matrix for x in row):
        raise ValueError("pairing exponents must be canonical residues")
    if any(matrix[i][i] or any((matrix[i][j] + matrix[j][i]) % prime
                              for j in range(dimension)) for i in range(dimension)):
        raise ValueError("pairing matrix must be alternating")
    if rank_mod(matrix, prime) != dimension:
        raise ValueError("pairing matrix must be nondegenerate")
    return dimension


def normalize_pairings(prime, multiplier, source, weak_image):
    """Recover a common weak scalar up to sign from all pairing exponents.

    For Q_i=[a]phi(P_i), image = multiplier*a^2*source modulo prime.
    Pairing compatibility alone does NOT certify a global geometric phi.
    """
    if not is_prime(prime) or prime == 2:
        raise ValueError("an odd prime auxiliary level is required")
    _positive(multiplier, "multiplier")
    if multiplier % prime == 0:
        raise ValueError("auxiliary level must be coprime to multiplier")
    dimension = _pairing_matrix(source, prime)
    if _pairing_matrix(weak_image, prime) != dimension:
        raise ValueError("source/image dimension mismatch")
    i, j = next((i, j) for i in range(dimension) for j in range(dimension) if source[i][j])
    ratio = weak_image[i][j] * pow(source[i][j], -1, prime) % prime
    if any((weak_image[i][j] - ratio * source[i][j]) % prime
           for i in range(dimension) for j in range(dimension)):
        raise ValueError("weak images fail common-scalar pairing compatibility")
    square = ratio * pow(multiplier % prime, -1, prime) % prime
    roots = tuple(a for a in range(1, prime) if a*a % prime == square)
    if len(roots) != 2:
        raise ValueError("weak scale is not a nonzero square")
    return {
        "prime": prime,
        "scale_square": square,
        "root_pair": roots,
        "normalizer": pow(roots[0], -1, prime),
        "remaining_ambiguity": "one_common_sign_at_this_level",
        "pairing_entries_checked": dimension*dimension,
        "square_root_candidates_tested": prime-1,
        "global_isogeny_certified": False,
    }


def sign_patterns(level_count, *, cap):
    """Enumerate signs modulo one GLOBAL sign, with an explicit hard cap."""
    _positive(level_count, "level_count")
    _positive(cap, "cap")
    count = 1 << (level_count - 1)
    if count > cap:
        raise ValueError(f"requires {count} branches, exceeding cap {cap}")
    for remaining in product((1, -1), repeat=level_count-1):
        yield (1,) + remaining


def auxiliary_plan(multiplier, dimension, characteristic):
    """Small odd prime levels satisfying interpolation AND projective rigidity.

    This is only resource arithmetic. No torsion points are constructed.
    """
    _positive(multiplier, "multiplier")
    _positive(dimension, "dimension")
    if not is_prime(characteristic) or characteristic == 2:
        raise ValueError("this theta-model audit requires odd prime characteristic")
    bound_squared = 8 * dimension**3 * multiplier**2
    levels, total, candidate = [], 1, 3
    while total <= multiplier or total*total <= bound_squared:
        if is_prime(candidate) and gcd(candidate, characteristic*multiplier) == 1:
            levels.append(candidate)
            total *= candidate
        candidate += 2
    return {
        "multiplier": multiplier,
        "dimension": dimension,
        "characteristic": characteristic,
        "levels": levels,
        "level_product": total,
        "projective_rigidity_bound_squared": bound_squared,
        "interpolation_arity_condition": total > multiplier,
        "projective_rigidity_condition": total*total > bound_squared,
        "max_prime": max(levels),
        "sign_branches_mod_global_sign": 1 << (len(levels)-1),
        "torsion_points_constructed": False,
        "interpolator_executed": False,
        "kernel_recovered": False,
    }


def transpose(matrix):
    return tuple(zip(*matrix))


def multiply(left, right):
    return tuple(tuple(sum(a*b for a, b in zip(row, col)) for col in zip(*right))
                 for row in left)


def repolarization_countercontrol():
    # On E^2, this integer matrix acts identically on each elliptic factor.
    shear = ((1, 1), (0, 1))
    polarization = multiply(transpose(shear), shear)
    squared = multiply(transpose(polarization), polarization)
    determinant = polarization[0][0]*polarization[1][1]-polarization[0][1]*polarization[1][0]
    return {
        "shear": shear,
        "positive_symmetric_endomorphism": polarization,
        "geometric_degree_on_E_squared": determinant**2,
        "adjoint_product_for_original_polarization": squared,
        "is_polarized_isogeny_for_original_models": False,
        "changed_polarization_is_principal": True,
        "general_repolarization_impossibility_claim": False,
    }


def descent_countercontrol():
    """A genuine Gaussian-isogeny identity defeating too-short descent tests.

    On E^2, Phi=diag(6+5i,6-5i), ell=61, and a swaps the factors.
    Gamma=Phi*a*Phi^-1 is nonintegral, but equals a on 5-torsion.
    """
    phi = ((6, -5, 0, 0), (5, 6, 0, 0), (0, 0, 6, 5), (0, 0, -5, 6))
    swap = ((0, 0, 1, 0), (0, 0, 0, 1), (1, 0, 0, 0), (0, 1, 0, 0))
    numerator = multiply(multiply(phi, swap), transpose(phi))
    local = tuple(tuple(x * pow(61, -1, 5) % 5 for x in row) for row in numerator)
    return {
        "ell": 61, "endomorphism_multiplier": 1, "dimension": 2,
        "auxiliary_order": 5, "conjugate_numerator": numerator,
        "conjugate_denominator": 61, "candidate_integral_endomorphism": swap,
        "torsion_action_matches_candidate": local == swap,
        "off_diagonal_gaussian_component_trace": "22/61",
        "true_conjugate_integral": False,
        "published_interpolation_input_and_uniqueness_bounds_hold": 5 > 1 and 5*5 > 8*2,
        "descent_rigidity_bound_holds": 5*5 > 8*2*61*61,
        "geometric_interpolator_executed": False,
    }
