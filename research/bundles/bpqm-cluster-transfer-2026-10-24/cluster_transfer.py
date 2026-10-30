"""Exact finite controls for decoding duality and planted cluster mobility.

This is not a fixed-disorder Gibbs sampler or a mixing-time certificate.
Enumeration is explicitly capped; scalable routines use only binary matrices.
"""

from collections import defaultdict
from fractions import Fraction as F
from math import comb, isfinite, isqrt


def integer(value, name, low, high):
    if type(value) is not int or not low <= value <= high:
        raise ValueError(f"{name} must be an integer in [{low}, {high}]")
    return value


def overlap(value):
    if not isinstance(value, (int, F)) or isinstance(value, bool):
        raise ValueError("use an exact integer or Fraction overlap")
    value = F(value)
    if not 0 <= value < 1:
        raise ValueError("finite nonnegative inverse temperature required")
    return value


def rows_checked(rows, n):
    integer(n, "spin count", 1, 100000)
    rows = tuple(rows)
    if any(type(row) is not int or not 0 <= row < 1 << n for row in rows):
        raise ValueError("each row must be an n-bit integer")
    return rows


def image(rows, x):
    return sum(((row & x).bit_count() % 2) << i for i, row in enumerate(rows))


def kernel_basis(rows, n):
    """Bit-packed echelon solve; no codeword/state enumeration."""
    rows = rows_checked(rows, n)
    pivots = {}
    for row in rows:
        while row:
            pivot = row.bit_length()-1
            if pivot in pivots:
                row ^= pivots[pivot]
            else:
                pivots[pivot] = row
                break
    basis = []
    for free in range(n):
        if free in pivots:
            continue
        word = 1 << free
        for pivot, row in sorted(pivots.items()):
            if (row & word).bit_count() % 2:
                word ^= 1 << pivot
        basis.append(word)
    return tuple(basis)


def span(basis, *, cap=65536):
    if 1 << len(basis) > cap:
        raise ValueError("finite enumeration cap exceeded; UNKNOWN, not hardness")
    words = [0]
    for vector in basis:
        words += [word ^ vector for word in words]
    return tuple(words)


def kernel_geometry(rows, n):
    basis = kernel_basis(rows, n)
    active = 0
    for word in basis:
        active |= word
    return {"basis": basis, "rank": n-len(basis), "nullity": len(basis),
            "active_coordinates": active.bit_count(),
            "mean_jump": F(active.bit_count(), 2),
            "holding_probability": F(1, 1 << len(basis))}


def draw_kernel(basis, rng):
    word = 0
    for vector in basis:
        if rng.getrandbits(1):
            word ^= vector
    return word


def coin(probability, rng):
    return rng.randrange(probability.denominator) < probability.numerator


def socket_rows(n, rng):
    """The unchanged (clause degree 3, spin degree 6) socket ensemble."""
    integer(n, "spin count", 1, 100000)
    sockets = [i for i in range(n) for _ in range(6)]
    rng.shuffle(sockets)
    rows = []
    for start in range(0, len(sockets), 3):
        row = 0
        for i in sockets[start:start+3]:
            row ^= 1 << i
        rows.append(row)
    return tuple(rows)


def planted_start(rows, n, c, rng):
    """Generate NEW disorder J and its conditional equilibrium spin x.

    J is partition-weighted, NOT a supplied uniformly random instance.
    The returned J must stay fixed during a trajectory.
    """
    rows, c = rows_checked(rows, n), overlap(c)
    x = rng.getrandbits(n)
    noise = sum(coin((1-c)/2, rng) << i for i in range(len(rows)))
    return image(rows, x) ^ noise, x


def cluster_step(rows, n, c, signs, x, rng):
    rows, c = rows_checked(rows, n), overlap(c)
    integer(signs, "sign word", 0, (1 << len(rows))-1)
    integer(x, "spin word", 0, (1 << n)-1)
    p = 2*c/(1+c)
    satisfied = image(rows, x) ^ signs
    selected = tuple(row for i, row in enumerate(rows)
                     if not (satisfied >> i & 1) and coin(p, rng))
    geometry = kernel_geometry(selected, n)
    delta = draw_kernel(geometry["basis"], rng)
    return x ^ delta, geometry


def finite_laws(rows, n, c):
    """Exact all-sign, all-spin controls. This is exponential reference work."""
    rows, c = rows_checked(rows, n), overlap(c)
    m = len(rows)
    if m > 8 or n > 5:
        raise ValueError("exact law enumeration capped at 8 clauses and 5 spins")
    weight = {e: ((1-c)/2)**e.bit_count()*((1+c)/2)**(m-e.bit_count())
              for e in range(1 << m)}
    partitions, gibbs, annealed, quenched = {}, {}, {}, {}
    for signs in range(1 << m):
        z = sum(weight[signs ^ image(rows, x)] for x in range(1 << n))
        partitions[signs] = z
        for x in range(1 << n):
            w = weight[signs ^ image(rows, x)]
            gibbs[signs, x] = w/z
            annealed[signs, x] = w/(1 << n)
            quenched[signs, x] = w/z/(1 << m)
    columns = tuple(image(rows, 1 << i) for i in range(n))
    linear_image = tuple(sorted(set(span(columns))))
    seen, cosets = set(), []
    for representative in range(1 << m):
        if representative in seen:
            continue
        coset = tuple(representative ^ v for v in linear_image)
        seen.update(coset)
        cosets.append(sum(weight[e] for e in coset))
    uniform = F(1, len(cosets))
    eta = sum(abs(p-uniform) for p in cosets)/2
    joint_tv = sum(abs(annealed[k]-quenched[k]) for k in quenched)/2
    return {"weights": weight, "partitions": partitions, "gibbs": gibbs,
            "annealed": annealed, "quenched": quenched,
            "coset_probabilities": tuple(cosets), "eta": eta,
            "joint_tv": joint_tv}


def finite_step(rows, n, c, signs, x):
    rows, c = rows_checked(rows, n), overlap(c)
    if n > 5 or len(rows) > 8:
        raise ValueError("exact transition enumeration cap exceeded")
    integer(signs, "sign word", 0, (1 << len(rows))-1)
    integer(x, "spin word", 0, (1 << n)-1)
    satisfied = [row for i, row in enumerate(rows)
                 if ((signs ^ image(rows, x)) >> i & 1) == 0]
    p, law = 2*c/(1+c), defaultdict(F)
    for mask in range(1 << len(satisfied)):
        selected = [row for i, row in enumerate(satisfied) if mask >> i & 1]
        probability = p**mask.bit_count()*(1-p)**(len(satisfied)-mask.bit_count())
        kernel = span(kernel_basis(selected, n))
        for delta in kernel:
            law[x ^ delta] += probability/len(kernel)
    return dict(law)


def bernoulli_kernel_law(rows, n, c):
    rows, c = rows_checked(rows, n), overlap(c)
    if n > 5 or len(rows) > 8:
        raise ValueError("exact Bernoulli/kernel enumeration cap exceeded")
    law = defaultdict(F)
    for mask in range(1 << len(rows)):
        selected = [row for i, row in enumerate(rows) if mask >> i & 1]
        probability = c**mask.bit_count()*(1-c)**(len(rows)-mask.bit_count())
        kernel = span(kernel_basis(selected, n))
        for delta in kernel:
            law[delta] += probability/len(kernel)
    return dict(law)


def expected_weight_count(n, h, c):
    """Exact socket first moment: binom(n,h)[z^(6h)]F_c(z)^(2n)/binom(6n,6h)."""
    integer(n, "finite spin count", 1, 32)
    integer(h, "weight", 0, n)
    c = overlap(c)
    polynomial, base = [F(1)], (F(1), 3*(1-c), F(3), 1-c)
    for _ in range(2*n):
        nxt = [F(0)]*min(len(polynomial)+3, 6*h+1)
        for i, a in enumerate(polynomial):
            for j, b in enumerate(base):
                if i+j < len(nxt):
                    nxt[i+j] += a*b
        polynomial = nxt
    return F(comb(n, h), comb(6*n, 6*h))*polynomial[6*h]


def choose_z(rho, c):
    """Numerical witness search only. Every proposed witness is checked exactly."""
    rho, c = float(rho), float(c)
    lo, hi = 1e-12, 1e8
    for _ in range(100):
        z = (lo*hi)**0.5
        f = 1+3*(1-c)*z+3*z*z+(1-c)*z**3
        mu = (3*(1-c)*z+6*z*z+3*(1-c)*z**3)/f
        if mu < 3*rho:
            lo = z
        else:
            hi = z
    if not isfinite(z):
        raise ArithmeticError("failed numerical proposal")
    return F(z).limit_denominator(100000)


def endpoint_certificate(rho, z, c, decay):
    """Check exp(b f(rho,z)) <= decay^b using rational integer powers only."""
    rho, z, decay = F(rho), F(z), F(decay)
    c = overlap(c)
    if not 0 <= rho <= 1 or z <= 0 or not 0 < decay < 1:
        raise ValueError("invalid entropy certificate input")
    a, b = rho.numerator, rho.denominator
    polynomial = 1+3*(1-c)*z+3*z*z+(1-c)*z**3
    ratio = polynomial**(2*b)*rho**(5*a)*(1-rho)**(5*(b-a))/z**(6*a)
    return ratio <= decay**b


def make_certificate():
    c, cutoff, decay = F(13, 20), F(1, 50), F(99, 100)
    intervals = []
    for k in range(2, 100):
        left, right = F(k, 100), F(k+1, 100)
        z = choose_z((left+right)/2, c)
        intervals.append({"left": str(left), "right": str(right), "z": str(z)})
    certificate = {"c": str(c), "cutoff": str(cutoff), "decay": str(decay),
                   "intervals": intervals}
    verify_certificate(certificate)
    return certificate


def verify_certificate(certificate):
    c, cutoff, decay = (F(certificate[k]) for k in ("c", "cutoff", "decay"))
    if not 0 < cutoff < 1:
        raise ValueError("invalid cutoff")
    previous = cutoff
    for entry in certificate["intervals"]:
        left, right, z = (F(entry[k]) for k in ("left", "right", "z"))
        if left != previous or not left < right <= 1:
            raise ValueError("entropy intervals do not form an exact contiguous cover")
        if not all(endpoint_certificate(rho, z, c, decay) for rho in (left, right)):
            raise ValueError("rational endpoint inequality failed")
        previous = right
    if previous != 1:
        raise ValueError("incomplete entropy cover")
    return True


def mobility_bound(n, certificate):
    integer(n, "spin count", 1, 100000)
    verify_certificate(certificate)
    return min(F(1), (n+1)*(6*n+1)*F(certificate["decay"])**n)


def upward_dyadic(value, bits=128):
    value = F(value)
    scale = 1 << integer(bits, "rounding bits", 1, 4096)
    return F(-(-value.numerator*scale//value.denominator), scale)


def conditional_trajectory_bound(annealed_step_tail, steps, decoder_block_error, bits=128):
    """Union bound plus ONE disorder transfer, conditional on a block-error theorem.

    A finite tree bit-error number is not a block-error bound. None preserves
    UNKNOWN; the routine does not infer an error theorem from measurements.
    """
    integer(steps, "step count", 1, 10**12)
    tail = F(annealed_step_tail)
    if not 0 <= tail <= 1:
        raise ValueError("tail bound must be in [0,1]")
    if decoder_block_error is None:
        return None
    if not isinstance(decoder_block_error, (int, F)) or isinstance(decoder_block_error, bool):
        raise ValueError("block error must be an exact rational bound or None")
    error = F(decoder_block_error)
    if not 0 <= error <= 1:
        raise ValueError("block error must be in [0,1]")
    scale = 1 << integer(bits, "rounding bits", 1, 4096)
    numerator = -(-error.numerator*scale*scale//error.denominator)
    root = isqrt(numerator)
    if root*root < numerator:
        root += 1
    return min(F(1), steps*tail+F(root, scale))


def bounded_cut_flow(crossing_mass, separator_mass, long_jump):
    """A conditional cut bound; callers must establish every input for SAME instance.

    crossing_mass is pi(A), assumed <=1/2. The other quantities bound
    pi(separator) and stationary P[Hamming jump >= separation].
    Returns Phi(A) upper and the integer times ruled out at TV tolerance 1/4.
    """
    a, s, p = map(F, (crossing_mass, separator_mass, long_jump))
    if not 0 < a <= F(1, 2) or not 0 <= s <= 1 or not 0 <= p <= 1:
        raise ValueError("invalid conditional cut inputs")
    flow = min(a, s+p)
    if not flow:
        return {"conductance_upper": F(0), "ruled_out_time_upper_exclusive": None}
    phi = flow/a
    return {"conductance_upper": phi, "ruled_out_time_upper_exclusive": 1/(4*phi)}
