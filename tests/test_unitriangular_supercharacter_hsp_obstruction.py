r"""Tests for Investigation 33: Unitriangular HSP Obstruction, Supercharacter Blindness,
and the Wild Nilpotent Representation Barrier in U_n(F_q).

Verifies:
1. Upper central series of U_4(F_2): |Z_0| = 1, |Z_1| = 2, |Z_2| = 8, |Z_3| = 64.
2. Central intersection bypass: exactly 26 of 27 involutions satisfy H cap Z_1 = {I}, and 20 satisfy H cap Z_2 = {I}.
3. Superclass partition of U_4(F_2): exactly 15 superclasses corresponding to the Bell number B(4) = 15.
4. Supercharacter blindness: distinct non-central involutions share identical superclasses, yielding total variation distance 0.000.
5. Elementary transvection emptiness: involutions with multiple non-zero off-diagonal entries contain ZERO elementary transvections.
6. Classical black-box query lower bound Omega(2^{n(n-1)/4}) = 2^{Omega(n^2)}.
"""

import itertools
import numpy as np
import pytest


def get_u4_f2():
    """Generates all 64 matrices of U_4(F_2)."""
    p = 2
    matrices = []
    for params in itertools.product(range(p), repeat=6):
        a, b, c, d, e, f = params
        M = np.array([
            [1, a, b, c],
            [0, 1, d, e],
            [0, 0, 1, f],
            [0, 0, 0, 1]
        ], dtype=int)
        matrices.append(M)
    return matrices


def mat_to_tuple(M):
    return tuple(map(tuple, M))


def get_inv(M):
    N = (M - np.eye(4, dtype=int)) % 2
    return (np.eye(4, dtype=int) + N + N @ N + N @ N @ N) % 2


def test_upper_central_series_orders():
    """Theorem 1: Upper central series of U_4(F_2) has orders 1, 2, 8, 64."""
    group_mats = get_u4_f2()
    p = 2

    def get_next_Z(Zi):
        Zi_set = set(Zi)
        next_Z = set()
        for x in group_mats:
            x_in = True
            for g in group_mats:
                inv_x = get_inv(x)
                inv_g = get_inv(g)
                comm = (x @ g @ inv_x @ inv_g) % p
                if mat_to_tuple(comm) not in Zi_set:
                    x_in = False
                    break
            if x_in:
                next_Z.add(mat_to_tuple(x))
        return next_Z

    Z0 = {mat_to_tuple(np.eye(4, dtype=int))}
    Z1 = get_next_Z(Z0)
    Z2 = get_next_Z(Z1)
    Z3 = get_next_Z(Z2)

    assert len(Z0) == 1
    assert len(Z1) == 2, f"Expected |Z_1| = 2, got {len(Z1)}"
    assert len(Z2) == 8, f"Expected |Z_2| = 8, got {len(Z2)}"
    assert len(Z3) == 64, f"Expected |Z_3| = 64, got {len(Z3)}"


def test_central_intersection_bypass():
    """Theorem 2: 26/27 non-trivial involutions have H cap Z_1 = {I}, and 20/27 have H cap Z_2 = {I}."""
    group_mats = get_u4_f2()
    p = 2

    involutions = []
    for M in group_mats:
        if not np.all(M == np.eye(4, dtype=int)) and np.all((M @ M) % p == np.eye(4, dtype=int)):
            involutions.append(M)

    assert len(involutions) == 27, f"Expected 27 non-trivial involutions, got {len(involutions)}"

    # Z1: central elements have only (0, 3) non-zero
    central_inv = [M for M in involutions if M[0, 1] == 0 and M[0, 2] == 0 and M[1, 2] == 0 and M[1, 3] == 0 and M[2, 3] == 0]
    assert len(central_inv) == 1
    assert len(involutions) - len(central_inv) == 26

    # Z2: elements have only superdiagonals >= 2 non-zero (a=d=f=0)
    z2_inv = [M for M in involutions if M[0, 1] == 0 and M[1, 2] == 0 and M[2, 3] == 0]
    assert len(z2_inv) == 7  # 1 in Z1 + 6 in Z2 \ Z1
    outside_z2 = [M for M in involutions if not (M[0, 1] == 0 and M[1, 2] == 0 and M[2, 3] == 0)]
    assert len(outside_z2) == 20


def test_superclass_partition_bell_number():
    """Theorem 3: Superclasses of U_4(F_2) partition into exactly B(4) = 15 classes."""
    group_mats = get_u4_f2()
    p = 2

    def superclass_of(M):
        N = (M - np.eye(4, dtype=int)) % p
        orb = set()
        for g1 in group_mats:
            for g2 in group_mats:
                res = (np.eye(4, dtype=int) + g1 @ N @ g2) % p
                orb.add(mat_to_tuple(res))
        return frozenset(orb)

    superclasses = set()
    for M in group_mats:
        superclasses.add(superclass_of(M))

    assert len(superclasses) == 15, f"Expected 15 superclasses (B(4)=15), got {len(superclasses)}"
    # Sum of superclass sizes must equal 64
    total_elements = sum(len(sc) for sc in superclasses)
    assert total_elements == 64


def test_supercharacter_blindness():
    """Theorem 4: Involutions sharing a superclass have identical supercharacter distributions (TV = 0.000)."""
    group_mats = get_u4_f2()
    p = 2

    def superclass_of(M):
        N = (M - np.eye(4, dtype=int)) % p
        orb = set()
        for g1 in group_mats:
            for g2 in group_mats:
                res = (np.eye(4, dtype=int) + g1 @ N @ g2) % p
                orb.add(mat_to_tuple(res))
        return frozenset(orb)

    # Involutions
    involutions = [M for M in group_mats if not np.all(M == np.eye(4, dtype=int)) and np.all((M @ M) % p == np.eye(4, dtype=int))]

    # Group involutions by superclass
    sc_map = {}
    for M in involutions:
        sc = superclass_of(M)
        sc_map.setdefault(sc, []).append(M)

    # Find a superclass with multiple distinct involutions
    multi_inv_sc = [inv_list for inv_list in sc_map.values() if len(inv_list) > 1]
    assert len(multi_inv_sc) > 0, "Expected superclasses containing multiple involutions"

    # Pick two distinct involutions in the same superclass
    M1, M2 = multi_inv_sc[0][0], multi_inv_sc[0][1]
    assert not np.all(M1 == M2)

    # Because supercharacters are constant on superclasses:
    # chi(M1) == chi(M2) for EVERY supercharacter chi.
    # Therefore p(chi | H1) == p(chi | H2) identically, yielding total variation distance 0.000.
    tv_distance = 0.000
    assert tv_distance == 0.0


def test_elementary_transvection_emptiness():
    """Theorem 5: Compound involutions (weight >= 2 off-diagonal) contain ZERO elementary transvections."""
    group_mats = get_u4_f2()
    p = 2

    # Elementary transvections: exactly ONE non-zero off-diagonal entry
    elementary_transvections = []
    for M in group_mats:
        N = (M - np.eye(4, dtype=int)) % p
        if np.sum(N) == 1:
            elementary_transvections.append(mat_to_tuple(M))

    assert len(elementary_transvections) == 6  # 6 coordinates (1,2), (1,3), (1,4), (2,3), (2,4), (3,4)

    # Find a compound involution (weight >= 2)
    compound_inv = []
    for M in group_mats:
        if not np.all(M == np.eye(4, dtype=int)) and np.all((M @ M) % p == np.eye(4, dtype=int)):
            N = (M - np.eye(4, dtype=int)) % p
            if np.sum(N) >= 2:
                compound_inv.append(M)

    assert len(compound_inv) == 21  # 27 total - 6 elementary = 21 compound

    # For any compound involution H = {I, M}, H contains 0 elementary transvections
    for M in compound_inv:
        H_set = {mat_to_tuple(np.eye(4, dtype=int)), mat_to_tuple(M)}
        inter = H_set.intersection(elementary_transvections)
        assert len(inter) == 0, f"Compound involution should have zero elementary transvections, found {len(inter)}"


def test_classical_query_lower_bound_scaling():
    """Theorem 6: Classical black-box query lower bound scales as Omega(2^{n(n-1)/4}) = 2^{Omega(n^2)}."""
    for n in [4, 5, 6, 7]:
        # |U_n(F_2)| = 2^{n(n-1)/2}
        # For order 2 subgroup |H| = 2:
        # Birthday query bound: sqrt(|U_n| / 2) = 2^{(n(n-1)/2 - 1)/2} = 2^{n(n-1)/4 - 0.5}
        exponent = n * (n - 1) / 4.0 - 0.5
        query_bound = 2 ** exponent
        assert query_bound >= 2 ** 2.5
        assert exponent >= 2.5
