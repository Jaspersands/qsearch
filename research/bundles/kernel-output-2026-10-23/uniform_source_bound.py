"""Public source bounds and elementary lifts; no geometric source backend."""

from sympy import Matrix, eye, isprime, nextprime, zeros

from kernel_output import (
    action, alternating_form, check_split, coordinate_map, flat,
    integer_matrix, inverse_mod, matrix_multiply, mod,
)


def elementary(size, i, j, c):
    out = eye(size)
    out[i, j] = c
    return out


def sl_word(matrix, ell):
    """Return a product word with at most (d-1)(d+9) transvections."""
    matrix = integer_matrix(matrix)
    d = matrix.rows
    if not isprime(ell) or ell == 2 or d < 2 or matrix.cols != d or int(matrix.det()) % ell != 1:
        raise ValueError("SL_d at an odd prime required")
    work, operations = mod(matrix, ell), []

    def left(i, j, c):
        nonlocal work
        c %= ell
        if c:
            work = mod(elementary(d, i, j, c)*work, ell)
            operations.append((i, j, c))

    for col in range(d):
        pivot = next(r for r in range(col, d) if work[r, col])
        if pivot != col:
            left(col, pivot, 1)
            left(pivot, col, -1)
            left(col, pivot, 1)
        for row in range(d):
            if row != col:
                left(row, col, -int(work[row, col])*pow(int(work[col, col]), -1, ell))
    word = [(i, j, (-c) % ell) for i, j, c in operations]
    for i in range(d-1):
        a = int(work[i, i])
        word.extend([(i, d-1, a), (d-1, i, -pow(a, -1, ell)), (i, d-1, a),
                     (i, d-1, -1), (d-1, i, 1), (i, d-1, -1)])
    result = tuple((i, j, c % ell) for i, j, c in word if c % ell)
    if len(result) > (d-1)*(d+9):
        raise AssertionError("public word bound violated")
    return result


def lift_symplectic(order, split, matrix, ell):
    """Exact degree-one quaternion word, using centered lifts of coefficients."""
    matrix = integer_matrix(matrix)
    g = matrix.rows//2
    if matrix.shape != (2*g, 2*g) or g < 2:
        raise ValueError("at least two elliptic factors required")
    form = alternating_form(g)
    if mod(matrix.T*form*matrix-form, ell) != zeros(2*g):
        raise ValueError("symplectic matrix required")
    check_split(order, split, ell)
    inverse = inverse_mod(coordinate_map(split), ell)
    physical = sl_word(matrix, ell)
    cross = []
    for i, j, c in physical:
        if i//2 != j//2:
            cross.append((i, j, c))
        else:
            k = next(k for k in range(2*g) if k//2 != i//2)
            cross.extend([(i, k, c), (k, j, 1), (i, k, -c), (k, j, -1)])
    factors = []
    for i, j, c in cross:
        image = zeros(2)
        image[i % 2, j % 2] = c
        coordinates = mod(inverse*flat(image), ell)
        coordinates = coordinates.applyfunc(lambda x: int(x)-ell if x > ell//2 else int(x))
        factors.append((i//2, j//2, coordinates))
    identity = Matrix.vstack(*(order.unit if i == j else zeros(4, 1)
                               for i in range(g) for j in range(g)))
    sigma, sigma_inverse = identity.copy(), identity.copy()
    for a, b, q in factors:
        forward, backward = identity.copy(), identity.copy()
        forward[4*(a*g+b):4*(a*g+b+1), :] += q
        backward[4*(a*g+b):4*(a*g+b+1), :] -= q
        sigma = matrix_multiply(order, sigma, forward, g)
        sigma_inverse = matrix_multiply(order, backward, sigma_inverse, g)
    return {"sigma": sigma, "inverse": sigma_inverse,
            "physical_length": len(physical), "quaternion_length": len(factors),
            "factors": tuple(factors)}


def uniform_surface_bound(order, ell):
    if not isprime(ell) or ell == 2:
        raise ValueError("odd prime required")
    basis_norms = [(order.traces*order.multiply(order.star(eye(4)[:, i]), eye(4)[:, i]))[0]/2
                   for i in range(4)]
    if any(n.q != 1 or n <= 0 for n in basis_norms):
        raise ValueError("positive integral quaternion basis norms required")
    norm_sum = int(sum(basis_norms))
    factor_bound = 2+(ell-1)**2*norm_sum
    return {"physical_length_bound": 39, "quaternion_length_bound": 156,
            "basis_norm_sum": norm_sum, "factor_squared_frobenius_bound": factor_bound,
            "trace_bound": factor_bound**156}


def smooth_denominator(order, ell, characteristic):
    if not isprime(characteristic) or characteristic in (2, ell):
        raise ValueError("distinct odd characteristic required")
    bounds = uniform_surface_bound(order, ell)
    denominator, prime, primes = 1, 2, []
    while denominator <= bounds["trace_bound"]+2:
        if prime not in (ell, characteristic):
            denominator *= prime
            primes.append(prime)
        prime = int(nextprime(prime))
    return {**bounds, "denominator": denominator, "primes": tuple(primes)}
