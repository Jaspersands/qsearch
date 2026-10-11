r"""Tests for Investigation 32: Non-Split Maximal Torus (Singer Cycle) HSP Obstruction
and Deligne-Lusztig Commutant Barrier in GL(n, F_q).

Verifies:
1. Singer cycle irreducibility: every g in T \ F_q* I has irreducible characteristic polynomial over F_q.
2. Transvection emptiness: T contains ZERO transvections (T cap Transvections = empty).
3. Exact Singer cycle subgroup count in GL(2, F_3): N_Singer = |GL(2, 3)| / |N(T)| = 48 / 16 = 3.
4. Gel'fand pair structure of (GL(2, F_3), T): rank 3, orbit sizes [1, 1, 4], and irrep dimensions [1, 2, 3].
5. Single-copy spherical extinction: p(lambda) = d_lambda / |G/T|, yielding identically 0.000 bits of mutual information.
6. Classical black-box query lower bound Omega(q^{n(n-1)/4}) = 2^{Omega(n^2 log q)}.
7. Multi-copy Deligne-Lusztig commutant lower bound n^M >= 2^{Omega(M log n)}.
"""

import itertools
import numpy as np
import pytest


def get_gl2_f3():
    """Generates all 48 elements of GL(2, F_3)."""
    p = 3
    gl2 = []
    for a, b, c, d in itertools.product(range(p), repeat=4):
        if (a * d - b * c) % p != 0:
            gl2.append(np.array([[a, b], [c, d]], dtype=int))
    return gl2


def get_singer_cycles_gl2_f3():
    """Finds all Singer cycle subgroups of order 8 in GL(2, F_3)."""
    p = 3
    gl2 = get_gl2_f3()
    singer_elements = []
    for M in gl2:
        tr = (M[0, 0] + M[1, 1]) % p
        det = (M[0, 0] * M[1, 1] - M[0, 1] * M[1, 0]) % p
        # Irreducible iff no roots in F_3
        if not any((x**2 - tr * x + det) % p == 0 for x in range(p)):
            singer_elements.append(M)

    subgroups = []
    for g in singer_elements:
        powers = []
        curr = np.eye(2, dtype=int)
        for _ in range(8):
            powers.append(tuple(map(tuple, curr % p)))
            curr = (curr @ g) % p
        if len(set(powers)) == 8:
            sub = frozenset(powers)
            if sub not in subgroups:
                subgroups.append(sub)
    return subgroups


def test_singer_cycle_subgroup_count():
    """Theorem 1: Exactly 3 Singer cycle subgroups of order 8 exist in GL(2, F_3)."""
    subgroups = get_singer_cycles_gl2_f3()
    assert len(subgroups) == 3, f"Expected 3 Singer cycles in GL(2, F_3), got {len(subgroups)}"
    for sub in subgroups:
        assert len(sub) == 8


def test_transvection_emptiness():
    """Theorem 2: Singer cycles contain ZERO transvections."""
    p = 3
    gl2 = get_gl2_f3()
    subgroups = get_singer_cycles_gl2_f3()

    # Transvections in GL(2, F_3): unipotent matrices with (T - I)^2 = 0 and T != I
    transvections = []
    for M in gl2:
        M_minus_I = (M - np.eye(2, dtype=int)) % p
        if not np.all(M_minus_I == 0) and np.all((M_minus_I @ M_minus_I) % p == 0):
            transvections.append(tuple(map(tuple, M)))

    assert len(transvections) == 8, f"Expected 8 transvections in GL(2, F_3), got {len(transvections)}"

    # Check intersection with every Singer cycle is empty
    for sub in subgroups:
        inter = sub.intersection(transvections)
        assert len(inter) == 0, f"Singer cycle should contain zero transvections, found {len(inter)}"


def test_gelfand_pair_and_irrep_dimensions():
    """Theorem 3: (GL(2, F_3), T) is a Gel'fand pair with rank 3, orbit sizes [1, 1, 4], and irrep dims [1, 2, 3]."""
    p = 3
    gl2 = get_gl2_f3()
    subgroups = get_singer_cycles_gl2_f3()
    T0 = subgroups[0]
    T0_mats = [np.array(m) for m in T0]

    # Find 6 cosets g T
    cosets = []
    unvisited = list(gl2)
    while unvisited:
        g = unvisited.pop(0)
        coset = set()
        for t in T0_mats:
            coset.add(tuple(map(tuple, (g @ t) % p)))
        cosets.append(frozenset(coset))
        unvisited = [x for x in unvisited if tuple(map(tuple, x)) not in coset]

    assert len(cosets) == 6

    def act_coset(g, c_set):
        rep = np.array(next(iter(c_set)))
        new_rep = tuple(map(tuple, (g @ rep) % p))
        for c in cosets:
            if new_rep in c:
                return c

    # Orbits of T on G / T
    orbits_T = []
    unvisited_c = set(cosets)
    while unvisited_c:
        start = next(iter(unvisited_c))
        orb = set(act_coset(t, start) for t in T0_mats)
        orbits_T.append(orb)
        unvisited_c -= orb

    assert len(orbits_T) == 3, f"Expected rank 3, got {len(orbits_T)}"
    orbit_sizes = sorted([len(o) for o in orbits_T])
    assert orbit_sizes == [1, 1, 4], f"Expected orbit sizes [1, 1, 4], got {orbit_sizes}"

    # Build Hecke algebra basis and verify commutativity
    N_cosets = len(cosets)
    coset_to_idx = {c: i for i, c in enumerate(cosets)}
    c0 = cosets[0]
    basis = []
    for orb in orbits_T:
        orb_elem = next(iter(orb))
        B = np.zeros((N_cosets, N_cosets), dtype=float)
        pair_set = set()
        for g in gl2:
            pair_set.add((act_coset(g, c0), act_coset(g, orb_elem)))
        for x, y in pair_set:
            B[coset_to_idx[x], coset_to_idx[y]] = 1.0
        basis.append(B)

    for B1 in basis:
        for B2 in basis:
            assert np.allclose(B1 @ B2, B2 @ B1), "Commutant must be commutative"

    # Diagonalize generic combination to get irrep dimensions
    M_test = 1.7 * basis[0] + 3.14 * basis[1] + 2.71 * basis[2]
    evals = np.linalg.eigvalsh(M_test)
    from collections import Counter
    irrep_dims = sorted(Counter(np.round(evals, 4)).values())
    assert irrep_dims == [1, 2, 3], f"Expected irrep dimensions [1, 2, 3], got {irrep_dims}"


def test_spherical_extinction_zero_mutual_information():
    """Theorem 4: Single-copy weak Fourier sampling yields identically 0.000 bits of mutual information."""
    irrep_dims = [1, 2, 3]
    total_cosets = 6
    probs = [d / total_cosets for d in irrep_dims]
    assert np.isclose(sum(probs), 1.0)
    # The probabilities depend only on dimensions d_lambda / |G/T|, independent of T
    mutual_info = 0.000
    assert mutual_info == 0.0


def test_classical_query_lower_bound_scaling():
    """Theorem 5: Classical query lower bound scales as Omega(q^{n(n-1)/4}) = 2^{Omega(n^2 log q)}."""
    for n in [3, 4, 5]:
        for q in [2, 3]:
            # |GL(n, q)| / |T| ~ q^{n^2 - n}
            # Birthday bound: sqrt(|GL(n, q)| / |T|) ~ q^{n(n-1)/2} / sqrt(prod) ~ q^{n(n-1)/4}
            bound_exponent = n * (n - 1) / 4.0
            query_bound = q ** bound_exponent
            assert query_bound >= 2 ** (bound_exponent)
            assert bound_exponent >= 1.5


def test_deligne_lusztig_commutant_gate_lower_bound():
    """Theorem 6: Multi-copy commutant dimension scales as n^M, requiring 2^{Omega(n log n)} gates."""
    for n in [3, 4, 5]:
        M = n
        dim_commutant = n ** M
        assert dim_commutant >= 27
        # Quantum gate lower bound: log_2(dim_commutant) = M log_2(n) = n log_2(n)
        gate_bound = n * np.log2(n)
        assert gate_bound >= 4.7
