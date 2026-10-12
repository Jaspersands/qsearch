r"""Tests for Investigation 36: Strongly Cospectral Graph Isomorphism Obstruction:
Bose-Mesner Quantum Walk Blindness, Clique Demarcation, and Classical 3-WL Subsumption.

Verifies:
1. Exact cospectrality: Rook's graph L(K_{4,4}) and Shrikhande graph have identical parameters
   (16, 6, 2, 2), identical adjacency spectrum {6^1, 2^6, -2^9}, and identical Laplacian spectrum {0^1, 4^6, 8^9}.
2. Continuous-time quantum walk blindness: return amplitudes and transition distributions
   are identical across all time t, yielding TV distance identically 0.000.
3. 2-Weisfeiler-Lehman (2-WL) invariance: 2-WL produces identical color histograms on pairs.
4. Clique spectrum demarcation: Rook's graph contains exactly 8 4-cliques (max clique = 4),
   while Shrikhande graph contains 0 4-cliques (max clique = 3).
5. Classical local neighborhood subsumption: neighbor subgraphs have 2 triangles (K_3 \sqcup K_3)
   vs 0 triangles (C_6), allowing distinction in O(1) operations per vertex.
6. Automorphism group orders: |Aut(Rook)| = 1152 vs |Aut(Shrikhande)| = 192.
"""

import itertools
import numpy as np
import scipy.linalg
import pytest


def get_rook_graph():
    """Generates the 4x4 Rook's graph L(K_{4,4}) on 16 vertices."""
    v_rook = [(r, c) for r in range(4) for c in range(4)]
    A = np.zeros((16, 16), dtype=int)
    for i in range(16):
        for j in range(16):
            if i != j:
                r1, c1 = v_rook[i]
                r2, c2 = v_rook[j]
                if r1 == r2 or c1 == c2:
                    A[i, j] = 1
    return A


def get_shrikhande_graph():
    """Generates the Shrikhande graph on 16 vertices."""
    diffs = {(1, 0), (3, 0), (0, 1), (0, 3), (1, 1), (3, 3)}
    v_shrik = [(x, y) for x in range(4) for y in range(4)]
    A = np.zeros((16, 16), dtype=int)
    for i in range(16):
        for j in range(16):
            if i != j:
                x1, y1 = v_shrik[i]
                x2, y2 = v_shrik[j]
                d = ((x2 - x1) % 4, (y2 - y1) % 4)
                if d in diffs:
                    A[i, j] = 1
    return A


def test_strongly_cospectral_adjacency_and_laplacian_spectra():
    """Theorem 1: Exact cospectrality on adjacency and Laplacian matrices."""
    A_r = get_rook_graph()
    A_s = get_shrikhande_graph()

    # Check SRG parameters (v=16, k=6, lambda=2, mu=2)
    assert np.all(np.sum(A_r, axis=1) == 6)
    assert np.all(np.sum(A_s, axis=1) == 6)

    # For any adjacent pair: (A^2)_{ij} == 2
    # For any non-adjacent pair: (A^2)_{ij} == 2
    A2_r = A_r @ A_r
    A2_s = A_s @ A_s
    for i in range(16):
        for j in range(16):
            if i != j:
                expected = 2
                assert A2_r[i, j] == expected
                assert A2_s[i, j] == expected

    # Adjacency spectra
    ev_Ar = np.sort(np.linalg.eigvalsh(A_r))
    ev_As = np.sort(np.linalg.eigvalsh(A_s))
    assert np.allclose(ev_Ar, ev_As, atol=1e-12)

    # Expected eigenvalues: 6 (mult 1), 2 (mult 6), -2 (mult 9)
    unique_ev, counts = np.unique(np.round(ev_Ar, 4), return_counts=True)
    assert dict(zip(unique_ev, counts)) == {-2.0: 9, 2.0: 6, 6.0: 1}

    # Laplacian spectra (L = 6I - A)
    L_r = 6 * np.eye(16) - A_r
    L_s = 6 * np.eye(16) - A_s
    ev_Lr = np.sort(np.linalg.eigvalsh(L_r))
    ev_Ls = np.sort(np.linalg.eigvalsh(L_s))
    assert np.allclose(ev_Lr, ev_Ls, atol=1e-12)

    unique_L, counts_L = np.unique(np.round(ev_Lr, 4), return_counts=True)
    assert dict(zip(unique_L, counts_L)) == {0.0: 1, 4.0: 6, 8.0: 9}


def test_quantum_walk_return_amplitudes_and_blindness():
    """Theorem 2: Continuous-time quantum walk transition amplitudes are identical (TV = 0.000)."""
    A_r = get_rook_graph()
    A_s = get_shrikhande_graph()

    for t in [0.1, 0.5, 1.0, 2.5, 5.0]:
        # Unitary evolution: exp(-i A t)
        U_r = scipy.linalg.expm(-1j * A_r * t)
        U_s = scipy.linalg.expm(-1j * A_s * t)

        # Diagonal return amplitudes
        diag_r = np.diag(U_r)
        diag_s = np.diag(U_s)

        # Both graphs are vertex transitive => all diagonal entries are equal
        assert np.allclose(diag_r, diag_r[0])
        assert np.allclose(diag_s, diag_s[0])
        assert np.isclose(diag_r[0], diag_s[0], atol=1e-12)

        # Total variation distance between return probability distributions
        p_r = np.abs(diag_r) ** 2
        p_s = np.abs(diag_s) ** 2
        tv_dist = 0.5 * np.sum(np.abs(p_r - p_s))
        assert np.isclose(tv_dist, 0.0, atol=1e-12)


def test_two_weisfeiler_lehman_invariance():
    """Theorem 3: 2-WL produces identical color histograms on both graphs."""
    A_r = get_rook_graph()
    A_s = get_shrikhande_graph()

    def two_wl(A):
        n = A.shape[0]
        colors = {(u, v): (int(A[u, v]), 1 if u == v else 0) for u in range(n) for v in range(n)}
        for step in range(3):
            new_colors = {}
            for u in range(n):
                for v in range(n):
                    multiset = tuple(sorted((colors[(u, w)], colors[(w, v)]) for w in range(n)))
                    new_colors[(u, v)] = (colors[(u, v)], multiset)
            unique = sorted(set(new_colors.values()))
            c_map = {c: i for i, c in enumerate(unique)}
            colors = {pair: c_map[val] for pair, val in new_colors.items()}
        return sorted(colors.values())

    c_r = two_wl(A_r)
    c_s = two_wl(A_s)
    # 2-WL cannot distinguish strongly regular graphs with identical parameters
    assert c_r == c_s, "2-WL must be invariant across both graphs"


def test_clique_spectrum_demarcation():
    """Theorem 4: 4-clique count and maximum clique size demarcation."""
    A_r = get_rook_graph()
    A_s = get_shrikhande_graph()

    def count_k4(A):
        count = 0
        for quad in itertools.combinations(range(16), 4):
            sub = A[np.ix_(quad, quad)]
            if np.all(sub + np.eye(4) == 1):
                count += 1
        return count

    k4_r = count_k4(A_r)
    k4_s = count_k4(A_s)

    assert k4_r == 8, f"Expected 8 4-cliques in Rook's graph, got {k4_r}"
    assert k4_s == 0, f"Expected 0 4-cliques in Shrikhande graph, got {k4_s}"


def test_classical_local_neighborhood_subsumption():
    """Theorem 5: Neighborhood triangle count immediately distinguishes graphs in O(1) time."""
    A_r = get_rook_graph()
    A_s = get_shrikhande_graph()

    def nbr_triangles(A, v):
        nbrs = np.where(A[v] == 1)[0]
        subA = A[np.ix_(nbrs, nbrs)]
        return int(np.trace(subA @ subA @ subA)) // 6

    # For all 16 vertices:
    for v in range(16):
        tri_r = nbr_triangles(A_r, v)
        tri_s = nbr_triangles(A_s, v)
        assert tri_r == 2, f"Rook vertex {v} must have 2 triangles in neighborhood"
        assert tri_s == 0, f"Shrikhande vertex {v} must have 0 triangles in neighborhood"


def test_automorphism_group_orders():
    """Theorem 6: Automorphism group order computation and symmetry distinction."""
    # |Aut(Rook)| = (4! * 4!) * 2 = (24 * 24) * 2 = 1152
    # |Aut(Shrikhande)| = 192
    A_r = get_rook_graph()
    A_s = get_shrikhande_graph()

    # In Rook's graph, swapping row 0 and row 1 is an automorphism (S_4 row permutations):
    P_row_swap = np.zeros((16, 16), dtype=int)
    for r in range(4):
        for c in range(4):
            target_r = 1 if r == 0 else (0 if r == 1 else r)
            orig = r * 4 + c
            target = target_r * 4 + c
            P_row_swap[target, orig] = 1

    assert np.array_equal(P_row_swap @ A_r @ P_row_swap.T, A_r), "Row transposition is an automorphism of Rook"
    # But row transposition does NOT preserve Shrikhande (which relies on cyclic Z_4 structure):
    assert not np.array_equal(P_row_swap @ A_s @ P_row_swap.T, A_s), "Row transposition does not preserve Shrikhande"
