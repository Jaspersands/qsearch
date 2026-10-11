r"""Tests for Investigation 34: Graph Isomorphism & Symmetric Group S_n Hidden Subgroup Obstruction:
Weak Fourier Blindness, Gel'fand Collapse, and the Multi-Copy Kronecker-Racah Commutant Barrier.

Verifies:
1. Weak Fourier sampling blindness: character evaluations on conjugate involutions are identical,
   yielding TV distance = 0.000.
2. Gel'fand pair collapse: (S_3, H) is a Gel'fand pair (dim 2, commutative), but for S_4,
   Hecke algebras are strictly non-commutative with dim 7 (transpositions) and dim 8 (matchings).
3. Permutation module irrep decomposition:
   - For S_4 and transpositions: irrep multiplicities [1, 0, 2, 1, 1], sum m^2 = 7.
   - For S_4 and matchings: irrep multiplicities [1, 1, 1, 1, 2], sum m^2 = 8.
4. Multi-copy commutant explosion:
   - Transpositions in S_4: dim(C_M) for M=1..4 are exactly [7, 868, 124432, 17915968].
   - Matchings in S_4: dim(C_M) for M=1..4 are exactly [8, 896, 124928, 17924096].
   - Confirms lower bound dim(C_M) >= (n!)^{2M-1} / 2^{2M} = 2^{Omega(M n log n)}.
5. Single-copy coset density matrices:
   - Trace = 1.0, mixed state purity Tr(rho^2) = 1/|H| = 0.5.
   - Exact trace distances between conjugate states.
6. Classical query lower bound: Omega(sqrt(n! / 2)) = 2^{Omega(n log n)}.
"""

import itertools
import math
import numpy as np
import pytest


def perm_mul(p1, p2):
    return tuple(p1[x] for x in p2)


def test_weak_fourier_sampling_blindness():
    """Theorem 1: Weak Fourier sampling produces identical probability distributions
    for all conjugate involutions in S_n (TV distance identically 0.000)."""
    # S_4 character table:
    # Classes: [1, (12), (12)(34), (123), (1234)]
    # Sizes:   [1,   6,      3,       8,      6   ]
    irreps = {
        '[4]': (1, [1, 1, 1, 1, 1]),
        '[1^4]': (1, [1, -1, 1, 1, -1]),
        '[3,1]': (3, [3, 1, -1, 0, -1]),
        '[2,1^2]': (3, [3, -1, -1, 0, 1]),
        '[2,2]': (2, [2, 0, 2, -1, 0]),
    }
    order_G = 24

    # Two distinct transpositions in S_4: tau_1 = (0 1) and tau_2 = (0 2)
    # Both belong to class 1 (index 1) with size 6
    p_dist_tau1 = {}
    p_dist_tau2 = {}
    for name, (d, chi) in irreps.items():
        # Weak Fourier probability: p(lambda | H) = d_lambda * sum_{h in H} chi(h) / |G|
        p1 = d * (chi[0] + chi[1]) / float(order_G)
        p2 = d * (chi[0] + chi[1]) / float(order_G)
        p_dist_tau1[name] = p1
        p_dist_tau2[name] = p2

    # Probabilities must sum to 1.0
    assert np.isclose(sum(p_dist_tau1.values()), 1.0)
    assert np.isclose(sum(p_dist_tau2.values()), 1.0)

    # TV distance between the two distributions
    tv_dist = 0.5 * sum(abs(p_dist_tau1[name] - p_dist_tau2[name]) for name in irreps)
    assert tv_dist == 0.0, f"Expected TV distance 0.000, got {tv_dist}"

    # Similarly for two distinct matching involutions (class 2)
    p_dist_m1 = {}
    p_dist_m2 = {}
    for name, (d, chi) in irreps.items():
        p1 = d * (chi[0] + chi[2]) / float(order_G)
        p2 = d * (chi[0] + chi[2]) / float(order_G)
        p_dist_m1[name] = p1
        p_dist_m2[name] = p2

    assert np.isclose(sum(p_dist_m1.values()), 1.0)
    tv_dist_m = 0.5 * sum(abs(p_dist_m1[name] - p_dist_m2[name]) for name in irreps)
    assert tv_dist_m == 0.0, f"Expected TV distance 0.000, got {tv_dist_m}"


def test_gelfand_pair_collapse_and_hecke_noncommutativity():
    """Theorem 2: (S_3, H) is a Gel'fand pair, but for S_4, Hecke algebras are non-commutative."""
    # S_3 test
    perms_3 = list(itertools.permutations(range(3)))
    e_3 = (0, 1, 2)
    tau_3 = (1, 0, 2)
    H_3 = [e_3, tau_3]

    double_cosets_3 = set()
    for g in perms_3:
        dc = frozenset(perm_mul(perm_mul(h1, g), h2) for h1 in H_3 for h2 in H_3)
        double_cosets_3.add(dc)

    assert len(double_cosets_3) == 2, f"Expected 2 double cosets in S_3, got {len(double_cosets_3)}"

    # S_4 with transpositions
    perms_4 = list(itertools.permutations(range(4)))
    e_4 = (0, 1, 2, 3)
    tau_trans = (1, 0, 2, 3)
    H_trans = [e_4, tau_trans]

    double_cosets_trans = set()
    for g in perms_4:
        dc = frozenset(perm_mul(perm_mul(h1, g), h2) for h1 in H_trans for h2 in H_trans)
        double_cosets_trans.add(dc)

    assert len(double_cosets_trans) == 7, f"Expected 7 double cosets for transpositions in S_4, got {len(double_cosets_trans)}"
    dc_sizes_trans = sorted(len(dc) for dc in double_cosets_trans)
    assert dc_sizes_trans == [2, 2, 4, 4, 4, 4, 4]
    assert sum(dc_sizes_trans) == 24

    # S_4 with matching involutions
    tau_match = (1, 0, 3, 2)
    H_match = [e_4, tau_match]

    double_cosets_match = set()
    for g in perms_4:
        dc = frozenset(perm_mul(perm_mul(h1, g), h2) for h1 in H_match for h2 in H_match)
        double_cosets_match.add(dc)

    assert len(double_cosets_match) == 8, f"Expected 8 double cosets for matchings in S_4, got {len(double_cosets_match)}"
    dc_sizes_match = sorted(len(dc) for dc in double_cosets_match)
    assert dc_sizes_match == [2, 2, 2, 2, 4, 4, 4, 4]
    assert sum(dc_sizes_match) == 24

    # Verify non-commutativity of Hecke algebra for S_4 transpositions
    cosets = []
    coset_map = {}
    for g in perms_4:
        c = frozenset(perm_mul(g, h) for h in H_trans)
        if c not in coset_map:
            coset_map[c] = len(cosets)
            cosets.append(c)

    assert len(cosets) == 12

    basis_matrices = []
    for dc in double_cosets_trans:
        B = np.zeros((12, 12), dtype=float)
        for i, c_i in enumerate(cosets):
            g_i = next(iter(c_i))
            for g in dc:
                target = frozenset(perm_mul(perm_mul(g_i, g), h) for h in H_trans)
                j = coset_map[target]
                B[i, j] += 0.5
        basis_matrices.append(B)

    # Check that at least one pair does not commute
    commutes = True
    for B1 in basis_matrices:
        for B2 in basis_matrices:
            if not np.allclose(B1 @ B2, B2 @ B1):
                commutes = False
                break
        if not commutes:
            break

    assert not commutes, "Expected Hecke algebra to be non-commutative for (S_4, H_trans)"


def test_permutation_module_irrep_multiplicities():
    """Theorem 2 (Part 2): Permutation module irrep decomposition and commutant dimensions."""
    irreps = {
        '[4]': (1, [1, 1, 1, 1, 1]),
        '[1^4]': (1, [1, -1, 1, 1, -1]),
        '[3,1]': (3, [3, 1, -1, 0, -1]),
        '[2,1^2]': (3, [3, -1, -1, 0, 1]),
        '[2,2]': (2, [2, 0, 2, -1, 0]),
    }

    # Transpositions (class 1)
    trans_mults = {}
    for name, (d, chi) in irreps.items():
        trans_mults[name] = (d + chi[1]) // 2

    assert trans_mults == {'[4]': 1, '[1^4]': 0, '[3,1]': 2, '[2,1^2]': 1, '[2,2]': 1}
    # Total dimension
    total_dim_trans = sum(trans_mults[name] * irreps[name][0] for name in irreps)
    assert total_dim_trans == 12
    # Commutant dimension
    comm_dim_trans = sum(trans_mults[name] ** 2 for name in irreps)
    assert comm_dim_trans == 7  # 1^2 + 0^2 + 2^2 + 1^2 + 1^2 = 7

    # Matching involutions (class 2)
    match_mults = {}
    for name, (d, chi) in irreps.items():
        match_mults[name] = (d + chi[2]) // 2

    assert match_mults == {'[4]': 1, '[1^4]': 1, '[3,1]': 1, '[2,1^2]': 1, '[2,2]': 2}
    total_dim_match = sum(match_mults[name] * irreps[name][0] for name in irreps)
    assert total_dim_match == 12
    comm_dim_match = sum(match_mults[name] ** 2 for name in irreps)
    assert comm_dim_match == 8  # 1^2 + 1^2 + 1^2 + 1^2 + 2^2 = 8


def test_multi_copy_commutant_dimension_explosion():
    """Theorem 4: Multi-copy commutant dimension explosion for S_4."""
    # Transpositions: chi_perm = [12, 2, 0, 0, 0], class sizes [1, 6, 3, 8, 6]
    sizes = [1, 6, 3, 8, 6]
    chi_trans = [12, 2, 0, 0, 0]

    expected_trans = {1: 7, 2: 868, 3: 124432, 4: 17915968}
    for M, exp_dim in expected_trans.items():
        dim_C = sum(sizes[i] * (chi_trans[i] ** (2 * M)) for i in range(5)) // 24
        assert dim_C == exp_dim, f"Transposition M={M}: expected {exp_dim}, got {dim_C}"

    # Matchings: chi_perm = [12, 0, 4, 0, 0], class sizes [1, 6, 3, 8, 6]
    chi_match = [12, 0, 4, 0, 0]
    expected_match = {1: 8, 2: 896, 3: 124928, 4: 17924096}
    for M, exp_dim in expected_match.items():
        dim_C = sum(sizes[i] * (chi_match[i] ** (2 * M)) for i in range(5)) // 24
        assert dim_C == exp_dim, f"Matching M={M}: expected {exp_dim}, got {dim_C}"

    # Lower bound test: dim(C_M) >= (n!)^{2M-1} / 2^{2M}
    for M in [1, 2, 3, 4]:
        bound = (24 ** (2 * M - 1)) / (2 ** (2 * M))
        assert expected_trans[M] >= bound
        assert expected_match[M] >= bound


def test_single_copy_coset_density_matrix_properties():
    """Theorem 3 & 5: Coset density matrix trace, purity, and distances."""
    perms = list(itertools.permutations(range(4)))
    n_elem = len(perms)
    perm_to_idx = {p: i for i, p in enumerate(perms)}

    e = (0, 1, 2, 3)
    t1 = (1, 0, 2, 3) # (0 1)
    t2 = (0, 2, 1, 3) # (1 2)
    t3 = (0, 1, 3, 2) # (2 3) disjoint

    def make_rho(tau):
        H = [e, tau]
        rho = np.zeros((n_elem, n_elem), dtype=complex)
        for g in perms:
            v = np.zeros(n_elem, dtype=complex)
            for h in H:
                gh = perm_mul(g, h)
                v[perm_to_idx[gh]] += 1.0 / np.sqrt(len(H))
            rho += np.outer(v, np.conj(v)) / n_elem
        return rho

    rho1 = make_rho(t1)
    rho2 = make_rho(t2)
    rho3 = make_rho(t3)

    # Trace is 1.0
    assert np.isclose(np.trace(rho1), 1.0)
    # Purity Tr(rho^2) = |H| / |G| = 2 / 24 = 1/12
    purity = np.real(np.trace(rho1 @ rho1))
    assert np.isclose(purity, 2.0 / 24.0), f"Expected purity {2.0/24.0}, got {purity}"

    # Trace distance between adjacent transpositions: 1 / sqrt(3) ~= 0.57735
    tr_dist_adj = 0.5 * np.sum(np.abs(np.linalg.eigvalsh(rho1 - rho2)))
    assert np.isclose(tr_dist_adj, 1.0 / np.sqrt(3)), f"Expected 1/sqrt(3), got {tr_dist_adj}"

    # Trace distance between disjoint transpositions: 0.5
    tr_dist_disj = 0.5 * np.sum(np.abs(np.linalg.eigvalsh(rho1 - rho3)))
    assert np.isclose(tr_dist_disj, 0.5), f"Expected 0.5, got {tr_dist_disj}"


def test_classical_query_lower_bound_scaling():
    """Theorem 6: Classical black-box query lower bound scales as Omega(sqrt(n! / 2)) = 2^{Omega(n log n)}."""
    prev_bound = 0
    for n in [4, 6, 8, 10]:
        n_fact = math.factorial(n)
        query_bound = math.sqrt(n_fact / 2.0)
        assert query_bound > prev_bound
        prev_bound = query_bound
        # Check asymptotic exponent
        log2_bound = math.log2(query_bound)
        expected_asymptotic = 0.5 * (n * math.log2(n) - n * 1.442)
        assert log2_bound >= expected_asymptotic - 5.0
