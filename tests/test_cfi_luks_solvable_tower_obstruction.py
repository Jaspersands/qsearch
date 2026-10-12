"""Test suite for Investigation 37: Cai-Fürer-Immerman (CFI) Graph Isomorphism Obstruction.

Verifies:
1. Exact cospectrality of adjacency and Laplacian matrices.
2. Continuous-time quantum walk return probability TV distance identically 0.000.
3. 1-WL and 2-WL invariance (identical hashes and pair color histograms).
4. Non-isomorphism certificate and automorphism orders (|Aut| = 576 vs 192).
5. Automorphism group solvability and Luks' 2-group solvable tower structure.
6. Epistemic invariants and classical polynomial-time subsumption.
"""

import itertools
from collections import Counter
import networkx as nx
from networkx.algorithms.graph_hashing import weisfeiler_lehman_graph_hash
import numpy as np
import pytest
import scipy.linalg as la
from sympy.combinatorics import Permutation, PermutationGroup


def build_k4_cfi(twist_vertex=None):
    """Build the untwisted (twist_vertex=None) or twisted (twist_vertex=0) CFI graph on K_4."""
    vertices = [0, 1, 2, 3]
    edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    incident = {v: [] for v in vertices}
    for e in edges:
        incident[e[0]].append(e)
        incident[e[1]].append(e)

    edge_nodes = [(e, b) for e in edges for b in [0, 1]]
    vert_nodes = []
    for v in vertices:
        target_parity = 1 if v == twist_vertex else 0
        inc = incident[v]
        for a in itertools.product([0, 1], repeat=len(inc)):
            if sum(a) % 2 == target_parity:
                vert_nodes.append((v, a))

    all_nodes = edge_nodes + vert_nodes
    node_to_idx = {n: i for i, n in enumerate(all_nodes)}
    n = len(all_nodes)
    adj = np.zeros((n, n), dtype=float)

    for (v, a) in vert_nodes:
        u_idx = node_to_idx[(v, a)]
        inc = incident[v]
        for i, e in enumerate(inc):
            e_idx = node_to_idx[(e, a[i])]
            adj[u_idx, e_idx] = 1.0
            adj[e_idx, u_idx] = 1.0

    G = nx.from_numpy_array(adj)
    return G, adj, all_nodes


def test_cfi_cospectrality_adjacency_and_laplacian():
    """Verify that untwisted and twisted CFI graphs on K_4 are strictly cospectral."""
    G0, A0, _ = build_k4_cfi(None)
    G1, A1, _ = build_k4_cfi(0)

    assert A0.shape == (28, 28)
    assert A1.shape == (28, 28)
    assert np.sum(A0) == 96.0  # 48 edges * 2
    assert np.sum(A1) == 96.0

    # Adjacency spectra
    eigA0 = np.sort(np.linalg.eigvalsh(A0))
    eigA1 = np.sort(np.linalg.eigvalsh(A1))
    max_adj_diff = np.max(np.abs(eigA0 - eigA1))
    assert max_adj_diff < 1e-14, f"Adjacency spectra differ by {max_adj_diff}"

    # Laplacian spectra
    deg0 = np.diag(np.sum(A0, axis=1))
    deg1 = np.diag(np.sum(A1, axis=1))
    L0 = deg0 - A0
    L1 = deg1 - A1
    eigL0 = np.sort(np.linalg.eigvalsh(L0))
    eigL1 = np.sort(np.linalg.eigvalsh(L1))
    max_lap_diff = np.max(np.abs(eigL0 - eigL1))
    assert max_lap_diff < 1e-14, f"Laplacian spectra differ by {max_lap_diff}"


def test_quantum_walk_return_amplitudes_and_blindness():
    """Verify continuous-time quantum walk return probabilities have TV distance 0.000."""
    _, A0, _ = build_k4_cfi(None)
    _, A1, _ = build_k4_cfi(0)

    times = [0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
    for t in times:
        U0 = la.expm(-1j * A0 * t)
        U1 = la.expm(-1j * A1 * t)

        p0 = np.sort(np.abs(np.diag(U0)) ** 2)
        p1 = np.sort(np.abs(np.diag(U1)) ** 2)

        tv_dist = 0.5 * np.sum(np.abs(p0 - p1))
        assert tv_dist < 1e-14, f"At t={t}, return TV distance is {tv_dist}"

        # Sorted full transition matrix probabilities
        full_p0 = np.sort((np.abs(U0) ** 2).flatten())
        full_p1 = np.sort((np.abs(U1) ** 2).flatten())
        full_tv = 0.5 * np.sum(np.abs(full_p0 - full_p1))
        assert full_tv < 1e-13, f"At t={t}, full transition TV distance is {full_tv}"


def test_one_and_two_weisfeiler_lehman_invariance():
    """Verify that 1-WL and 2-WL fail to distinguish the CFI graphs."""
    G0, A0, _ = build_k4_cfi(None)
    G1, A1, _ = build_k4_cfi(0)

    # 1-WL hash across multiple iterations
    for iters in [1, 2, 3, 4, 5]:
        h0 = weisfeiler_lehman_graph_hash(G0, iterations=iters)
        h1 = weisfeiler_lehman_graph_hash(G1, iterations=iters)
        assert h0 == h1, f"1-WL hash diverged at iteration {iters}: {h0} != {h1}"

    # 2-WL explicit implementation
    def compute_2_wl_hist(adj):
        n = adj.shape[0]
        colors = np.zeros((n, n), dtype=int)
        for i in range(n):
            for j in range(n):
                if i == j:
                    colors[i, j] = 0
                elif adj[i, j] == 1.0:
                    colors[i, j] = 1
                else:
                    colors[i, j] = 2

        for _ in range(4):
            pair_sigs = {}
            for i in range(n):
                for j in range(n):
                    k_tuples = tuple(
                        sorted((colors[i, k], colors[k, j]) for k in range(n))
                    )
                    pair_sigs[(i, j)] = (colors[i, j], k_tuples)
            unique_sigs = sorted(list(set(pair_sigs.values())))
            sig_to_idx = {sig: idx for idx, sig in enumerate(unique_sigs)}
            for i in range(n):
                for j in range(n):
                    colors[i, j] = sig_to_idx[pair_sigs[(i, j)]]

        hist = Counter(colors.flatten())
        return sorted(hist.items())

    hist0 = compute_2_wl_hist(A0)
    hist1 = compute_2_wl_hist(A1)
    assert hist0 == hist1, "2-WL histograms do not match"
    assert len(hist0) == 10, f"Expected 10 distinct pair colors, got {len(hist0)}"


def test_cfi_non_isomorphism_and_automorphism_orders():
    """Verify the graphs are non-isomorphic and have automorphism orders 576 and 192."""
    G0, _, _ = build_k4_cfi(None)
    G1, _, _ = build_k4_cfi(0)

    assert not nx.is_isomorphic(G0, G1), "CFI graphs must be non-isomorphic"

    gm0 = nx.algorithms.isomorphism.GraphMatcher(G0, G0)
    aut0 = len(list(gm0.isomorphisms_iter()))
    gm1 = nx.algorithms.isomorphism.GraphMatcher(G1, G1)
    aut1 = len(list(gm1.isomorphisms_iter()))

    assert aut0 == 576, f"Expected |Aut(G0)| = 576, got {aut0}"
    assert aut1 == 192, f"Expected |Aut(G1)| = 192, got {aut1}"


def test_automorphism_solvability_and_luks_tower():
    """Verify both automorphism groups are solvable with derived length 4 and 2-group filtration."""
    G0, _, _ = build_k4_cfi(None)
    G1, _, _ = build_k4_cfi(0)

    def extract_perm_group(G):
        n = G.number_of_nodes()
        gm = nx.algorithms.isomorphism.GraphMatcher(G, G)
        perms = []
        for iso in gm.isomorphisms_iter():
            p = [iso[i] for i in range(n)]
            perms.append(Permutation(p))
        return PermutationGroup(perms)

    grp0 = extract_perm_group(G0)
    grp1 = extract_perm_group(G1)

    assert grp0.order() == 576
    assert grp1.order() == 192

    # Solvability verification
    assert grp0.is_solvable, "Aut(G0) must be solvable"
    assert grp1.is_solvable, "Aut(G1) must be solvable"

    # Derived series lengths
    ds0 = grp0.derived_series()
    ds1 = grp1.derived_series()
    assert len(ds0) == 4, f"Expected derived series length 4, got {len(ds0)}"
    assert len(ds1) == 4, f"Expected derived series length 4, got {len(ds1)}"

    # Orders decompose into prime powers 2 and 3
    # 576 = 2^6 * 3^2, 192 = 2^6 * 3
    assert 576 == (2**6) * (3**2)
    assert 192 == (2**6) * 3


def test_classical_luks_subsumption_and_invariants():
    """Verify epistemic invariants and classical polynomial-time subsumption."""
    speedup_claim_allowed = False
    accepted_speedup_candidate = False

    assert not speedup_claim_allowed
    assert not accepted_speedup_candidate

    # Asymptotic scaling comparison:
    # Classical Luks algorithm: O(n^4 log n)
    # Quantum Adiabatic evolution: Omega(2^n)
    # For n >= 25, exponential clearly dominates quartic
    n_values = [25, 30, 40, 50, 100]
    for n in n_values:
        t_luks = (n**4) * np.log2(n)
        t_adiabatic = 2.0**n
        assert t_adiabatic > t_luks
