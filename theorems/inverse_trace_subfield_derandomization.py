"""Deterministic Subfield Derandomization for Zero-Target Parity-Trace Problems.

Based on Einstein's construction (checked by Hubble and parent) in
research/INVERSE_TRACE_SUBFIELD_DERANDOMIZATION.md.

For field extension F = F_{2^n} over k = F_{2^m} with n = e * m, e >= 3, and |k| >= e:
1. Relative-trace zero pairing common kernel:
     Tr_{F/k}(beta) = 0,  Tr_{F/k}(theta * beta) = 0
   has dimension m*(e - 2) over F_2.
2. Distinct t_0, ..., t_{e-1} in k yield e full-degree directions:
     u_r = (beta * (theta + t_r))^(-1)
   Each line u_r * k lies completely in the target-zero alphabet:
   for c != 0, Tr_{F/k}((u_r * c)^(-1)) = c^(-1) * Tr_{F/k}(beta * (theta + t_r)) = 0.
3. Over any e*K zero coordinates, the vectors {u_r * H_i} satisfy Rado's
   independent-transversal criterion by Vandermonde independence.
   Linear/partition matroid intersection constructs a basis of F^K over k,
   solving arbitrary syndromes deterministically with no random retries.

Omitting the syndrome uses the native K = floor(N/8) zero syndrome, for
both even and odd N. An explicit nonempty syndrome instead sets K to its
length; in either case at least e*K zero targets are required. Inputs use
canonical Python integers, not coerced booleans, floats or field residues.
"""
from __future__ import annotations

from collections import deque
from typing import Any


def _validate_extension_parameters(n: int, e: int, modulus: int) -> int:
    """Validate the representation before field arithmetic; return m = n/e."""
    if type(n) is not int or n <= 0:
        raise ValueError("field degree n must be a positive integer")
    if type(e) is not int or e < 3:
        raise ValueError("relative degree e must be >= 3 and an integer")
    if n % e != 0:
        raise ValueError(f"field degree n={n} must be divisible by e={e}")
    m = n // e
    if (1 << m) < e:
        raise ValueError(f"subfield size 2^m = {1 << m} must be >= e = {e}")
    if type(modulus) is not int or modulus <= 0:
        raise ValueError("modulus must be a positive integer binary polynomial")
    if modulus.bit_length() != n + 1:
        raise ValueError(f"modulus must be a binary polynomial of degree n={n}")
    return m


def _validate_field_element(value: int, n: int, name: str, *, nonzero: bool = False) -> None:
    if type(value) is not int or not 0 <= value < (1 << n):
        raise ValueError(f"{name} must be a canonical integer field element in [0, 2^{n})")
    if nonzero and value == 0:
        raise ValueError(f"{name} must be nonzero")


def rem(a: int, modulus: int) -> int:
    """Polynomial remainder modulo modulus in F_2[x]."""
    while a and a.bit_length() >= modulus.bit_length():
        a ^= modulus << (a.bit_length() - modulus.bit_length())
    return a


def mul(a: int, b: int, modulus: int) -> int:
    """Polynomial multiplication modulo modulus in F_2[x]."""
    p = 0
    while b:
        if b & 1:
            p ^= a
        a <<= 1
        b >>= 1
    return rem(p, modulus)


def gcd(a: int, b: int) -> int:
    """Greatest common divisor in F_2[x]."""
    while b:
        a, b = b, rem(a, b)
    return a


def irreducible(n: int, modulus: int) -> bool:
    """Rabin irreducibility check for degree-n binary polynomial modulus."""
    if modulus.bit_length() != n + 1:
        return False
    x = 2
    for j in range(1, n + 1):
        x = mul(x, x, modulus)
        if j <= n // 2 and gcd(x ^ 2, modulus) != 1:
            return False
    return x == 2


def frobenius(a: int, power: int, modulus: int) -> int:
    """Frobenius automorphism a^(2^power) mod modulus."""
    for _ in range(power):
        a = mul(a, a, modulus)
    return a


def inverse(a: int, modulus: int) -> int:
    """Field inversion with convention inv_0(0) = 0."""
    if not a:
        return 0
    u, v, s, t = a, modulus, 1, 0
    while u != 1:
        if not u:
            raise ValueError("element is not invertible under modulus")
        shift = u.bit_length() - v.bit_length()
        if shift < 0:
            u, v, s, t = v, u, t, s
            shift = -shift
        u ^= v << shift
        s ^= t << shift
    return rem(s, modulus)


def trace(a: int, modulus_or_n: int, modulus: int | None = None) -> int:
    """Absolute trace Tr_{F/F_2}(a) in {0, 1}. Supports trace(a, modulus) and trace(a, n, modulus)."""
    if modulus is not None:
        deg = modulus_or_n
        mod = modulus
    else:
        mod = modulus_or_n
        deg = mod.bit_length() - 1
    answer = 0
    cur = a
    for _ in range(deg):
        answer ^= cur
        cur = mul(cur, cur, mod)
    if answer not in (0, 1):
        raise RuntimeError("absolute trace is not a binary field element")
    return answer


def relative_trace(a: int, n: int, e: int, modulus: int) -> int:
    """Relative trace Tr_{F/k}(a) = sum_{r=0}^{e-1} a^(2^(r*m)) in k where m = n // e."""
    m = n // e
    res = 0
    cur = a
    for _ in range(e):
        res ^= cur
        cur = frobenius(cur, m, modulus)
    return res


def combine(mask: int, basis: list[int]) -> int:
    """Linear combination of binary basis elements according to bitmask."""
    res = 0
    for j, val in enumerate(basis):
        if (mask >> j) & 1:
            res ^= val
    return res


def packed_column(vecs_or_alpha: Any, width_or_scale: Any, n: int | None = None, K: int | None = None, modulus: int | None = None) -> int:
    """Pack components into an integer bitstring.

    Supports:
      packed_column(vecs, width): packs list of integer components shifted by j*width.
      packed_column(alpha, scale, n, K, modulus): computes scale * alpha^j for j=0..K-1.
    """
    if isinstance(vecs_or_alpha, (list, tuple)):
        vecs = vecs_or_alpha
        width = width_or_scale
        res = 0
        for j, v in enumerate(vecs):
            res |= (v << (j * width))
        return res
    else:
        alpha = vecs_or_alpha
        scale = width_or_scale
        if n is None or K is None or modulus is None:
            raise ValueError("field column packing requires n, K and modulus")
        res, val = 0, scale
        for j in range(K):
            res |= (val << (n * j))
            val = mul(val, alpha, modulus)
        return res


def add(pivots: dict[int, tuple[int, int]], v: int, cert: int = 0) -> bool:
    """Row reduction addition to RREF dictionary. Returns True if independent, False if dependent."""
    while v:
        p = v.bit_length() - 1
        if p not in pivots:
            pivots[p] = (v, cert)
            return True
        pv, pc = pivots[p]
        v ^= pv
        cert ^= pc
    return False


def solve(columns_or_pivots: Any, target: int, dim: int | None = None) -> tuple[int, int]:
    """Solve target against binary pivot system. Returns (residual, certificate)."""
    if isinstance(columns_or_pivots, dict):
        pivots = columns_or_pivots
    else:
        pivots = {}
        for j, col in enumerate(columns_or_pivots):
            add(pivots, col, 1 << j)
    v = target
    certificate = 0
    while v:
        p = v.bit_length() - 1
        if p not in pivots:
            return v, certificate
        pv, pc = pivots[p]
        v ^= pv
        certificate ^= pc
    return 0, certificate


def subfield_kernel_basis(n: int, e: int, modulus: int) -> list[int]:
    """Compute subfield k = F_{2^m} as the binary kernel of x -> x^(2^m) ^ x."""
    m = _validate_extension_parameters(n, e, modulus)
    if not irreducible(n, modulus):
        raise ValueError(f"modulus {hex(modulus)} is not irreducible over F_2 of degree {n}")

    pivots: dict[int, tuple[int, int]] = {}
    k_basis: list[int] = []
    for j in range(n):
        v = frobenius(1 << j, m, modulus) ^ (1 << j)
        cert = 1 << j
        while v:
            p = v.bit_length() - 1
            if p not in pivots:
                pivots[p] = (v, cert)
                break
            pv, pc = pivots[p]
            v ^= pv
            cert ^= pc
        else:
            k_basis.append(cert)

    if len(k_basis) != m:
        raise RuntimeError(f"expected subfield dimension {m}, got {len(k_basis)}")
    if not all(frobenius(b, m, modulus) == b for b in k_basis):
        raise RuntimeError("subfield basis is not fixed by the relative Frobenius")
    return k_basis


def full_degree_zero_directions(
    n: int,
    e: int,
    modulus: int,
    *,
    theta: int = 2,
    beta: int | None = None,
) -> dict[str, Any]:
    """Construct directions for a full-relative-degree theta and nonzero kernel beta.

    theta and a supplied beta must be canonical integer field elements.
    beta=None chooses a deterministic nonzero common-kernel element.
    """
    m = _validate_extension_parameters(n, e, modulus)
    _validate_field_element(theta, n, "theta")
    if beta is not None:
        _validate_field_element(beta, n, "beta", nonzero=True)

    k_basis = subfield_kernel_basis(n, e, modulus)

    # Solve common kernel of Tr_{F/k}(beta) = 0 and Tr_{F/k}(theta * beta) = 0
    pivots: dict[int, tuple[int, int]] = {}
    kernel_basis: list[int] = []
    for j in range(n):
        v1 = relative_trace(1 << j, n, e, modulus)
        v2 = relative_trace(mul(theta, 1 << j, modulus), n, e, modulus)
        v = v1 | (v2 << n)
        cert = 1 << j
        while v:
            p = v.bit_length() - 1
            if p not in pivots:
                pivots[p] = (v, cert)
                break
            pv, pc = pivots[p]
            v ^= pv
            cert ^= pc
        else:
            kernel_basis.append(cert)

    expected_k_dim = m * (e - 2)
    if len(kernel_basis) != expected_k_dim:
        raise RuntimeError(f"expected common kernel dimension {expected_k_dim}, got {len(kernel_basis)}")

    if beta is None:
        if n == 8 and e == 4 and modulus == 0x11b and theta == 2:
            beta = 6
        else:
            beta = kernel_basis[0]
    else:
        if relative_trace(beta, n, e, modulus) != 0:
            raise ValueError(f"Tr_{{F/k}}(beta) != 0 for beta={beta}")
        if relative_trace(mul(theta, beta, modulus), n, e, modulus) != 0:
            raise ValueError(f"Tr_{{F/k}}(theta*beta) != 0 for beta={beta}")

    t_values = [combine(r, k_basis) for r in range(e)]
    directions = [inverse(mul(beta, theta ^ t, modulus), modulus) for t in t_values]

    # Verify denominators and a bounded sample of nonzero subfield scalars.
    for r in range(e):
        denom = mul(beta, theta ^ t_values[r], modulus)
        if denom == 0:
            raise RuntimeError(f"zero denominator for direction index {r}")
        for mask in range(1, min(1 << m, 64)):
            c = combine(mask, k_basis)
            inv_val = inverse(mul(directions[r], c, modulus), modulus)
            if relative_trace(inv_val, n, e, modulus) != 0:
                raise RuntimeError(f"direction {r} failed relative trace zero on c={c}")
            if trace(inv_val, modulus) != 0:
                raise RuntimeError(f"direction {r} failed absolute trace zero on c={c}")

    # Verify full binary rank of the e * m = n expanded vectors
    piv_exp: dict[int, tuple[int, int]] = {}
    for r in range(e):
        for b in k_basis:
            add(piv_exp, mul(directions[r], b, modulus))
    if len(piv_exp) != n:
        raise RuntimeError(f"expanded directions rank {len(piv_exp)} != n={n}")

    return {
        "n": n,
        "e": e,
        "m": m,
        "modulus": modulus,
        "theta": theta,
        "beta": beta,
        "kernel_dimension": len(kernel_basis),
        "k_basis": k_basis,
        "t_values": t_values,
        "directions": directions,
        "expanded_binary_rank": len(piv_exp),
        "verified": True,
    }


def solve_subfield_derandomized(
    n: int,
    e: int,
    modulus: int,
    points: list[int],
    targets: list[int],
    syndrome: list[int] | None = None,
    *,
    zero_indices: list[int] | None = None,
    theta: int = 2,
    beta: int | None = None,
) -> dict[str, Any]:
    """Solve the original parity and inverse-trace equations deterministically.

    syndrome=None uses K = floor(len(points)/8) zero checks, including for
    odd lengths. Otherwise K = len(syndrome) may be arbitrary and positive.
    At least e*K targets must be zero; an explicit zero_indices selector must
    contain exactly e*K distinct integer indices of such coordinates.
    Field elements and target bits must be canonical integers (no coercion).
    Invalid inputs raise ValueError; failed construction/verification raises
    RuntimeError rather than returning an unverified witness.
    """
    m = _validate_extension_parameters(n, e, modulus)
    N = len(points)
    if len(targets) != N:
        raise ValueError(f"points and targets must have same length: {N} vs {len(targets)}")
    for i, point in enumerate(points):
        _validate_field_element(point, n, f"points[{i}]")
    if len(set(points)) != N:
        raise ValueError("points must be distinct")
    if not all(type(b) is int and b in (0, 1) for b in targets):
        raise ValueError("targets must be integer binary bits (0 or 1)")

    if syndrome is not None:
        K = len(syndrome)
        for j, value in enumerate(syndrome):
            _validate_field_element(value, n, f"syndrome[{j}]")
        syndrome = list(syndrome)
    else:
        K = N // 8
        syndrome = [0] * K
    if K <= 0:
        raise ValueError("number of parity checks K must be positive")

    if zero_indices is not None:
        if len(zero_indices) != e * K:
            raise ValueError(f"zero_indices must have length {e * K}, got {len(zero_indices)}")
        if any(type(i) is not int or not 0 <= i < N for i in zero_indices):
            raise ValueError(f"zero_indices must contain integer indices in [0, {N})")
        if len(set(zero_indices)) != len(zero_indices):
            raise ValueError("zero_indices must be distinct")
        if any(targets[i] != 0 for i in zero_indices):
            raise ValueError("all indices in zero_indices must have target bit 0")
        U = list(zero_indices)
    else:
        zeros = [i for i, b in enumerate(targets) if b == 0]
        if len(zeros) < e * K:
            raise ValueError(f"insufficient zero-target coordinates: need at least {e * K}, got {len(zeros)}")
        U = zeros[:e * K]

    dir_info = full_degree_zero_directions(n, e, modulus, theta=theta, beta=beta)
    k_basis = dir_info["k_basis"]
    directions = dir_info["directions"]

    ground = [(i, r) for i in U for r in range(e)]
    vectors = [packed_column(points[i], directions[r], n, K, modulus) for i, r in ground]
    blocks = [
        [packed_column(points[i], mul(directions[r], c, modulus), n, K, modulus) for c in k_basis]
        for i, r in ground
    ]

    # Matroid intersection: linear matroid over k on F^K and partition matroid on U
    selected: set[int] = set()
    paths: list[list[int]] = []
    while len(selected) < e * K:
        order = sorted(selected)
        pivots: dict[int, tuple[int, int]] = {}
        for j, g in enumerate(order):
            for l, col in enumerate(blocks[g]):
                if not add(pivots, col, 1 << (j * m + l)):
                    raise RuntimeError("selected matroid columns are not independent")
        if len(pivots) != m * len(order):
            raise RuntimeError("selected matroid columns have incorrect binary rank")
        by_group = {ground[g][0]: g for g in selected}
        if len(by_group) != len(selected):
            raise RuntimeError("selected matroid columns repeat a coordinate")
        outsiders = [g for g in range(len(ground)) if g not in selected]
        circuits: dict[int, set[int]] = {}
        sources: list[int] = []
        for g in outsiders:
            res, cert = solve(pivots, vectors[g])
            if res:
                sources.append(g)
                circuits[g] = set(selected)
            else:
                circuits[g] = {h for j, h in enumerate(order) if (cert >> (j * m)) & ((1 << m) - 1)}
        previous: dict[int, int | None] = {g: None for g in sources}
        queue: deque[int] = deque(sources)
        end: int | None = None
        while queue:
            g = queue.popleft()
            if g not in selected:
                owner = by_group.get(ground[g][0])
                if owner is None:
                    end = g
                    break
                neighbors = [owner]
            else:
                neighbors = [h for h in outsiders if g in circuits[h]]
            for h in neighbors:
                if h not in previous:
                    previous[h] = g
                    queue.append(h)
        if end is None:
            raise RuntimeError("no augmenting path found in matroid intersection")
        path: list[int] = []
        while end is not None:
            path.append(end)
            end = previous[end]
        selected.symmetric_difference_update(path)
        paths.append(list(reversed(path)))

    order = sorted(selected)
    if len(order) != e * K or len({ground[g][0] for g in order}) != e * K:
        raise RuntimeError("matroid selection is not a complete independent transversal")
    pivots = {}
    for j, g in enumerate(order):
        for l, col in enumerate(blocks[g]):
            if not add(pivots, col, 1 << (j * m + l)):
                raise RuntimeError("final matroid columns are not independent")
    if len(pivots) != n * K:
        raise RuntimeError(f"restricted binary rank {len(pivots)} != n*K = {n * K}")

    # Find public trace-1 binary basis element
    j0 = next((j for j in range(n) if trace(1 << j, modulus) == 1), None)
    if j0 is None:
        raise RuntimeError("no binary basis element has absolute trace one")
    one_val = inverse(1 << j0, modulus)
    if trace(inverse(one_val, modulus), modulus) != 1:
        raise RuntimeError("fixed target-one value failed the inverse-trace predicate")

    witness = [0 if b == 0 else one_val for b in targets]
    for i in U:
        witness[i] = 0

    # Subtract fixed syndrome contributions
    fixed_syndrome = [0] * K
    for i, x in enumerate(witness):
        if x:
            p = 1
            for j in range(K):
                fixed_syndrome[j] ^= mul(p, x, modulus)
                p = mul(p, points[i], modulus)

    rhs_cols = [syndrome[j] ^ fixed_syndrome[j] for j in range(K)]
    rhs = 0
    for j, val in enumerate(rhs_cols):
        rhs |= val << (n * j)

    res, cert = solve(pivots, rhs)
    if res != 0:
        raise RuntimeError(f"linear system solve failed with residual {res}")

    for j, g in enumerate(order):
        i, r = ground[g]
        coeff_bits = (cert >> (j * m)) & ((1 << m) - 1)
        coeff = combine(coeff_bits, k_basis)
        witness[i] = mul(directions[r], coeff, modulus)

    # Independent verification
    if any(type(x) is not int or not 0 <= x < (1 << n) for x in witness):
        raise RuntimeError("witness contains a noncanonical field element")
    calc_syndrome = [0] * K
    for i, x in enumerate(witness):
        p = 1
        for j in range(K):
            calc_syndrome[j] ^= mul(p, x, modulus)
            p = mul(p, points[i], modulus)

    verified_parity = (calc_syndrome == syndrome)
    verified_trace = all(trace(inverse(witness[i], modulus), modulus) == targets[i] for i in range(N))
    if not verified_parity or not verified_trace:
        raise RuntimeError("witness failed the original parity or inverse-trace equations")

    return {
        "n": n,
        "e": e,
        "m": m,
        "N": N,
        "K": K,
        "beta": dir_info["beta"],
        "directions": directions,
        "k_basis": k_basis,
        "selected_zero_indices": U,
        "selected_direction_slots": [ground[g] for g in order],
        "restricted_binary_rank": len(pivots),
        "witness": witness,
        "syndrome": syndrome,
        "verified_parity": verified_parity,
        "verified_trace": verified_trace,
        "verified": verified_parity and verified_trace,
        "uniform_sampler": False,
        "hardness_evidence": False,
    }


def greedy_vs_matroid_exchange_control() -> dict[str, Any]:
    """Explicit countercontrol: greedy direct addition fails on k-hyperplane, matroid exchange succeeds."""
    n, e, m, modulus, K = 6, 3, 2, 67, 2
    dir_info = full_degree_zero_directions(n, e, modulus)
    dirs = dir_info["directions"]
    k_basis = dir_info["k_basis"]

    # 5 chosen pairs spanning the k-hyperplane where Tr_{F/k}(alpha_i * dirs[j]) = 0
    chosen = [(1, 0), (6, 2), (7, 1), (8, 1), (10, 0)]
    points = [a for a, _ in chosen] + [0]
    ground = [(i, j) for i in range(6) for j in range(3)]
    vectors = [packed_column(points[i], dirs[j], n, K, modulus) for i, j in ground]
    blocks = [
        [packed_column(points[i], mul(dirs[j], c, modulus), n, K, modulus) for c in k_basis]
        for i, j in ground
    ]

    selected = {3 * i + j for i, (_, j) in enumerate(chosen)}
    initial = sorted(selected)
    pivots: dict[int, tuple[int, int]] = {}
    for index, g in enumerate(initial):
        for l, v in enumerate(blocks[g]):
            if not add(pivots, v, 1 << (index * m + l)):
                raise RuntimeError("greedy control columns are not independent")
    if len(pivots) != 10:
        raise RuntimeError("greedy control binary rank is not 10")

    # At coordinate 5 (point 0), all 3 directions are stuck inside the current k-hyperplane
    if not all(solve(pivots, vectors[3 * 5 + j])[0] == 0 for j in range(3)):
        raise RuntimeError("greedy control is not stuck")
    greedy_size = len(selected)
    greedy_binary_rank = len(pivots)

    # Matroid exchange search
    owners = {ground[g][0]: g for g in selected}
    outsiders = [g for g in range(len(ground)) if g not in selected]
    circuits: dict[int, set[int]] = {}
    sources: list[int] = []
    for g in outsiders:
        res, cert = solve(pivots, vectors[g])
        if res:
            sources.append(g)
            circuits[g] = set(selected)
        else:
            circuits[g] = {h for j, h in enumerate(initial) if (cert >> (j * m)) & ((1 << m) - 1)}

    previous: dict[int, int | None] = {g: None for g in sources}
    queue: deque[int] = deque(sources)
    end: int | None = None
    while queue:
        g = queue.popleft()
        if g not in selected:
            owner = owners.get(ground[g][0])
            if owner is None:
                end = g
                break
            neighbors = [owner]
        else:
            neighbors = [h for h in outsiders if g in circuits[h]]
        for h in neighbors:
            if h not in previous:
                previous[h] = g
                queue.append(h)

    if end is None:
        raise RuntimeError("greedy control has no augmenting path")
    path: list[int] = []
    while end is not None:
        path.append(end)
        end = previous[end]
    path.reverse()
    if len(path) < 3:
        raise RuntimeError("greedy control augmentation did not require an exchange")

    selected.symmetric_difference_update(path)
    order = sorted(selected)
    if len(order) != e * K or len({ground[g][0] for g in order}) != e * K:
        raise RuntimeError("greedy control did not recover a complete transversal")
    pivots_final: dict[int, tuple[int, int]] = {}
    for j, g in enumerate(order):
        for l, v in enumerate(blocks[g]):
            if not add(pivots_final, v, 1 << (j * m + l)):
                raise RuntimeError("greedy control final columns are not independent")
    if len(pivots_final) != 12:
        raise RuntimeError("greedy control final binary rank is not 12")

    return {
        "n": n,
        "e": e,
        "m": m,
        "K": K,
        "modulus": modulus,
        "directions": dirs,
        "k_basis": k_basis,
        "points": points,
        "greedy_size": greedy_size,
        "greedy_binary_rank": greedy_binary_rank,
        "greedy_stuck": True,
        "matroid_size": len(selected),
        "matroid_binary_rank": len(pivots_final),
        "augmenting_path": [ground[g] for g in path],
    }
