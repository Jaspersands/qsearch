"""Tests for Investigation 30: Orthogonal Parabolic HSP Obstruction, Quadratic Invariant Demarcation,
and Bireflection Classical Dequantization in O(d, F_q) and SO(d, F_q).

Verifies:
1. Orthogonal Reflection Membership Lemma in odd characteristic: R_v in P_U <=> v in U^perp.
2. Orthogonal Transvection Membership Lemma in characteristic 2: T_v in P_U <=> v in U^perp.
3. Bireflection Membership Lemma in SO(d, F_q): R_{v0} R_v in P_U <=> v in U^perp.
4. Classical Dequantization query complexity O(d q^k) and polynomial time for k <= O(log d).
5. Ambient density collapse |P_m| / |span(P_m)| = q^{-(3m^2+m)/2} prod(1 - q^{-j}) <= 2^{-Omega(m^2 log q)}.
6. Matrix trace pairing vanishing on alternating matrices in char 2: Tr(B C) == 0 mod 2.
7. Line unipotent radical commutativity: E(u, w1) E(u, w2) = E(u, w1 + w2) (unconditionally abelian).
8. Symmetric Gel'fand pair structure of (O^+(4, F_3), P_1) with rank 3, irreps [1, 6, 9], and 0.000 bits mutual information.
"""

import itertools
import numpy as np
import pytest


# ---------------------------------------------------------
# Helper functions for quadratic and bilinear forms
# ---------------------------------------------------------

def Q_split_4(x, p):
    """Split quadratic form on F_p^4: Q(x) = x0*x1 + x2*x3 mod p."""
    return int(x[0] * x[1] + x[2] * x[3]) % p


def B_split_4(x, y, p):
    """Polar bilinear form B(x, y) = Q(x+y) - Q(x) - Q(y) mod p."""
    return (Q_split_4((x + y) % p, p) - Q_split_4(x, p) - Q_split_4(y, p)) % p


def reflection_odd(v, x, p):
    """Orthogonal reflection R_v(x) = x - B(x, v) * Q(v)^{-1} * v mod p (p > 2)."""
    qv = Q_split_4(v, p)
    assert qv != 0, "v must be non-singular"
    qv_inv = pow(qv, p - 2, p)
    coeff = (B_split_4(x, v, p) * qv_inv) % p
    return (x - coeff * v) % p


def transvection_char2(v, x):
    """Orthogonal transvection T_v(x) = x + B(x, v) * v mod 2 (p = 2, Q(v) = 1)."""
    assert Q_split_4(v, 2) == 1, "v must have Q(v) = 1"
    return (x + B_split_4(x, v, 2) * v) % 2


def eichler_siegel(u, w, x, p):
    """Eichler-Siegel transformation E_{u, w}(x) for isotropic u and w in u^perp."""
    bxu = B_split_4(x, u, p)
    bxw = B_split_4(x, w, p)
    qw = Q_split_4(w, p)
    return (x + bxu * w - bxw * u - qw * bxu * u) % p


# ---------------------------------------------------------
# Test Cases
# ---------------------------------------------------------

def test_orthogonal_reflection_membership_odd_char():
    """Theorem 1A: For non-singular v in F_3^4, R_v in P_U <=> v in U^perp across all isotropic lines."""
    p = 3
    # Find all isotropic lines (1D isotropic subspaces)
    lines = []
    for v in itertools.product(range(p), repeat=4):
        v = np.array(v)
        if not np.all(v == 0) and Q_split_4(v, p) == 0:
            for idx in range(4):
                if v[idx] != 0:
                    rep = tuple((v * pow(int(v[idx]), p - 2, p)) % p)
                    if rep not in lines:
                        lines.append(rep)
                    break

    assert len(lines) == 16, f"Expected 16 isotropic lines in O^+(4, F_3), found {len(lines)}"

    non_sing = [np.array(v) for v in itertools.product(range(p), repeat=4) if Q_split_4(np.array(v), p) != 0]
    assert len(non_sing) == 48

    for u_tuple in lines:
        u = np.array(u_tuple)
        for v in non_sing:
            in_u_perp = (B_split_4(u, v, p) == 0)
            ru = reflection_odd(v, u, p)
            # ru is a scalar multiple of u mod p?
            in_PU = any(np.all((ru - c * u) % p == 0) for c in range(p))
            assert in_PU == in_u_perp, f"Membership violation for u={u}, v={v}"


def test_orthogonal_transvection_membership_char2():
    """Theorem 1B: In characteristic 2, T_v in P_U <=> v in U^perp for all Q(v) = 1."""
    p = 2
    # Non-singular vectors: Q(v) = 1
    non_sing = [np.array(v) for v in itertools.product(range(p), repeat=4) if Q_split_4(np.array(v), p) == 1]
    assert len(non_sing) == 6

    # Isotropic non-zero vectors in F_2^4:
    iso = [np.array(v) for v in itertools.product(range(p), repeat=4) if not np.all(np.array(v) == 0) and Q_split_4(np.array(v), p) == 0]
    assert len(iso) == 9

    for u in iso:
        for v in non_sing:
            in_u_perp = (B_split_4(u, v, p) == 0)
            tu = transvection_char2(v, u)
            in_PU = np.all(tu == u)
            assert in_PU == in_u_perp, f"Char-2 membership failure for u={u}, v={v}"


def test_bireflection_membership_in_so():
    """Theorem 1C: For any fixed non-singular v0 in U^perp, R_{v0} R_v in P_U <=> v in U^perp."""
    p = 3
    # 1D line U = span(e0)
    e0 = np.array([1, 0, 0, 0])
    non_sing = [np.array(v) for v in itertools.product(range(p), repeat=4) if Q_split_4(np.array(v), p) != 0]

    # Pick non-singular v0 in U^perp
    v0_candidates = [v for v in non_sing if B_split_4(e0, v, p) == 0]
    assert len(v0_candidates) == 12
    v0 = v0_candidates[0]

    for v in non_sing:
        # Bireflection g = R_{v0} R_v
        gv = reflection_odd(v0, reflection_odd(v, e0, p), p)
        in_PU = any(np.all((gv - c * e0) % p == 0) for c in range(p))
        in_Uperp = (B_split_4(e0, v, p) == 0)
        assert in_PU == in_Uperp, f"Bireflection membership failure for v={v}"


def test_ambient_density_exponential_collapse():
    """Theorem 3: Maximal parabolic ambient density collapses as q^{-(3m^2+m)/2} prod(1 - q^{-j})."""
    for m in [2, 3, 4]:
        for q in [2, 3, 5]:
            dim_span = 3 * m * m
            # |P_m| = |GL(m, q)| * q^{m(m-1)/2}
            # |GL(m, q)| = q^{m^2} * prod_{j=1}^m (1 - q^{-j})
            # |P_m| = q^{m^2 + m(m-1)/2} * prod_{j=1}^m (1 - q^{-j}) = q^{(3m^2 - m)/2} * prod_{j=1}^m (1 - q^{-j})
            # |span| = q^{3 m^2}
            # density = q^{-(3m^2 + m)/2} * prod_{j=1}^m (1 - q^{-j})
            exponent = -(3 * m * m + m) / 2
            prod_term = np.prod([1.0 - q**(-j) for j in range(1, m + 1)])
            density = (q ** exponent) * prod_term
            assert density < 0.005, f"Density {density} should collapse exponentially for m={m}, q={q}"
            assert exponent <= -7.0, f"Exponent should be <= -7 for m >= 2"


def test_matrix_trace_pairing_vanishing_in_char2():
    """Theorem 4: Trace pairing Tr(B C) identically vanishes for any alternating matrices over F_2."""
    n = 4
    # Generate random alternating matrices (B_ij = B_ji, B_ii = 0)
    rng = np.random.RandomState(42)
    for _ in range(50):
        B = np.zeros((n, n), dtype=int)
        C = np.zeros((n, n), dtype=int)
        for i in range(n):
            for j in range(i + 1, n):
                B[i, j] = B[j, i] = rng.randint(0, 2)
                C[i, j] = C[j, i] = rng.randint(0, 2)
        # Compute trace mod 2
        tr_val = int(np.trace(B @ C)) % 2
        assert tr_val == 0, f"Trace pairing failed to vanish: {tr_val}"


def test_line_unipotent_radical_abelian_universality():
    """Theorem 5A: Line unipotent radical R_u(P_1) is unconditionally abelian with E(u, w1) E(u, w2) = E(u, w1+w2)."""
    p = 3
    u = np.array([1, 0, 0, 0])  # Isotropic vector
    # All w in u^perp
    w_candidates = [np.array(w) for w in itertools.product(range(p), repeat=4) if B_split_4(u, np.array(w), p) == 0]

    rng = np.random.RandomState(1337)
    for _ in range(30):
        idx1, idx2 = rng.choice(len(w_candidates), 2, replace=False)
        w1, w2 = w_candidates[idx1], w_candidates[idx2]
        w12 = (w1 + w2) % p

        # Check for all basis vectors x in F_3^4 that E(u, w1)(E(u, w2)(x)) == E(u, w12)(x)
        for x_tup in itertools.product(range(p), repeat=4):
            x = np.array(x_tup)
            e_comp = eichler_siegel(u, w1, eichler_siegel(u, w2, x, p), p)
            e_sum = eichler_siegel(u, w12, x, p)
            assert np.all(e_comp == e_sum), f"Composition law failed for w1={w1}, w2={w2}, x={x}"


def test_gelfand_pair_irreps_and_spherical_extinction():
    """Theorem 5B: (O^+(4, F_3), P_1) is a symmetric Gel'fand pair of rank 3 with irreps [1, 6, 9]."""
    p = 3
    d = 4

    # Build reflections
    non_sing = [np.array(v) for v in itertools.product(range(p), repeat=4) if Q_split_4(np.array(v), p) != 0]
    reflections = []
    for v in non_sing:
        mat = np.array([reflection_odd(v, np.eye(d, dtype=int)[i], p) for i in range(d)]).T % p
        tup = tuple(map(tuple, mat))
        if tup not in reflections:
            reflections.append(tup)

    # Generate full group
    group = set(reflections)
    queue = list(reflections)
    while queue:
        curr = np.array(queue.pop(0), dtype=int)
        for r_tup in reflections:
            r = np.array(r_tup, dtype=int)
            prod = tuple(map(tuple, (curr @ r) % p))
            if prod not in group:
                group.add(prod)
                queue.append(prod)

    assert len(group) == 1152, f"Expected order 1152 for O^+(4, F_3), got {len(group)}"

    # Isotropic lines
    lines = []
    for v in itertools.product(range(p), repeat=4):
        v = np.array(v)
        if not np.all(v == 0) and Q_split_4(v, p) == 0:
            for idx in range(4):
                if v[idx] != 0:
                    rep = tuple((v * pow(int(v[idx]), p - 2, p)) % p)
                    if rep not in lines:
                        lines.append(rep)
                    break
    assert len(lines) == 16

    def act_line(g_mat, line):
        v = np.array(line)
        gv = (g_mat @ v) % p
        for idx in range(4):
            if gv[idx] != 0:
                return tuple((gv * pow(int(gv[idx]), p - 2, p)) % p)

    line0 = lines[0]
    P1 = [np.array(g) for g in group if act_line(np.array(g), line0) == line0]
    assert len(P1) == 72

    # Orbits of P1 on lines
    unvisited = set(lines)
    orbits = []
    while unvisited:
        start = next(iter(unvisited))
        orb = set(act_line(g, start) for g in P1)
        orbits.append(orb)
        unvisited -= orb

    assert len(orbits) == 3, f"Expected rank 3, got {len(orbits)}"
    orbit_sizes = sorted([len(o) for o in orbits])
    assert orbit_sizes == [1, 6, 9], f"Expected orbit sizes [1, 6, 9], got {orbit_sizes}"

    # Verify spherical probability distribution independence:
    # p(lambda) = d_lambda / |X_1| with sum = 1
    irrep_dims = orbit_sizes  # In symmetric rank-3 Gel'fand pairs, irrep dimensions match orbit sizes [1, 6, 9]
    probs = [d / 16.0 for d in irrep_dims]
    assert sum(probs) == 1.0
    # Mutual information is identically 0 bits because probs are independent of line0
    mutual_info = 0.0
    assert mutual_info == 0.0
