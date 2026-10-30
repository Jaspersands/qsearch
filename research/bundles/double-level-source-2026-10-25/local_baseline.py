"""Classical local direction recovery from the SAME proposed marked source."""

from sympy import Matrix, eye, isprime
from sympy.ntheory.modular import crt

from double_level_source import checked_factors
from kernel_output import _preimage_lattice, check_split, coordinate_map, integer_matrix, inverse_mod, mod


def local_frame(vector, p, e):
    if type(p) is not int or not isprime(p) or type(e) is not int or e < 1:
        raise ValueError("prime and positive exponent required")
    n = p**e
    vector = mod(integer_matrix(vector), n)
    if vector.shape != (2, 1):
        raise ValueError("two-coordinate vector required")
    x, y = map(int, vector)
    if x % p:
        complement = (0, pow(x, -1, n))
    elif y % p:
        complement = (-pow(y, -1, n), 0)
    else:
        raise ValueError("primitive vector required")
    return mod(vector.row_join(Matrix(complement)), n)


def prefix_queries(vector, p, e, depth, digits):
    """Accept exactly the proposed direction mod p^digits of a depth-d kernel."""
    if (type(depth) is not int or type(digits) is not int
            or not 1 <= digits <= depth <= e):
        raise ValueError("1 <= prefix digits <= direction depth <= input exponent required")
    frame = local_frame(vector, p, e)
    change = Matrix.diag(frame, frame)
    s, n = p**(depth-digits), p**e
    upper, mix = eye(4), eye(4)
    upper[0, 1] = s
    mix[0, 2], mix[3, 1] = s, -s
    inverse = inverse_mod(change, n)
    return tuple(mod(change*g*inverse, n) for g in (upper, mix))


def content_depth(p, e, equal_identity):
    """Classical period probes; callback must use original geometric labels."""
    local_frame((1, 0), p, e)
    thresholds, count = [], 0
    for row, col in ((0, 1), (1, 0)):
        outcomes = []
        for k in range(e+1):
            query = eye(4)
            query[row, col] = p**k
            value = equal_identity(mod(query, p**e))
            if type(value) is not bool:
                raise ValueError("exact boolean comparison required")
            outcomes.append(value)
            count += 1
        if not outcomes[-1] or outcomes != sorted(outcomes):
            raise ValueError("nonmonotone or nonidentity source response")
        thresholds.append(outcomes.index(True))
    depth = max(thresholds)
    if (e-depth) % 2 or any(k and (depth-k) % 2 for k in thresholds):
        raise ValueError("invalid Smith-kernel threshold parities")
    return {"depth": depth, "content_exponent": (e-depth)//2,
            "thresholds": thresholds, "source_comparisons": count}


def classical_local_direction(p, e, depth, equal_identity, max_queries=4096):
    """O(p*depth) matched baseline, NOT polynomial in log(p) for large p."""
    local_frame((1, 0), p, e)
    if (type(depth) is not int or not 1 <= depth <= e
            or type(max_queries) is not int or max_queries < 0):
        raise ValueError("positive direction depth and nonnegative query budget required")
    bound = 2*(p*depth+1)
    if bound > max_queries:
        raise ValueError("classical digit search exceeds declared query budget")
    count = 0

    def accepted(vector, digits):
        nonlocal count
        values = [equal_identity(q) for q in prefix_queries(vector, p, e, depth, digits)]
        count += 2
        if any(type(value) is not bool for value in values):
            raise ValueError("exact boolean comparison required")
        return all(values)

    first = [(z, 1) for z in range(p)]+[(1, 0)]
    winners = [v for v in first if accepted(v, 1)]
    if len(winners) != 1:
        raise ValueError("source violates unique local-direction promise")
    x, y = winners[0]
    affine = y == 1
    z = x if affine else y
    for digits in range(2, depth+1):
        candidates = [z+t*p**(digits-1) for t in range(p)]
        winners = [v for v in candidates if accepted((v, 1) if affine else (1, v), digits)]
        if len(winners) != 1:
            raise ValueError("source violates unique local-direction promise")
        z = winners[0]
    return {"vector": [z, 1] if affine else [1, z], "modulus": p**depth,
            "source_comparisons": count, "source_comparison_bound": bound,
            "source_promise_verified": False, "quantum_execution": False}


def kernel_ideal_from_local_data(order, actions, n, factors, contents, directions):
    """Original LEFT ideal from supplied/recovered local data; not a solver."""
    factors = checked_factors(n, factors)
    check_split(order, actions, n)
    if set(contents) != {p for p, _ in factors}:
        raise ValueError("one content exponent per input prime required")
    scalar, moduli, frames, active = 1, [], [], set()
    for p, e in factors:
        a = contents[p]
        if type(a) is not int or not 0 <= 2*a <= e:
            raise ValueError("invalid content exponent")
        scalar *= p**a
        depth = e-2*a
        if depth:
            active.add(p)
            if p not in directions:
                raise ValueError("missing residual direction")
            moduli.append(p**depth)
            frames.append(local_frame(directions[p], p, depth))
    if set(directions) != active:
        raise ValueError("directions must exactly match positive-depth components")
    residual = n//(scalar*scalar)
    if residual == 1:
        return scalar*eye(4)
    frame = Matrix(2, 2, [int(crt(moduli, [f[i] for f in frames])[0]) for i in range(4)])
    inverse = inverse_mod(frame, residual)
    allowed = []
    for row in range(2):
        a = Matrix.zeros(2)
        a[row, 1] = 1
        allowed.append(mod(a*inverse, residual))
    smaller = _preimage_lattice(coordinate_map(tuple(mod(a, residual) for a in actions)), allowed, residual)
    ideal = scalar*smaller
    if abs(ideal.det()) != n*n:
        raise ArithmeticError("original ideal index mismatch")
    return ideal
