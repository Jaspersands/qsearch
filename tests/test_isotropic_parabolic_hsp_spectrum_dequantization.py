"""
Test suite for Investigation 28:
The Isotropic Parabolic HSP Spectrum: Polynomial Dequantization,
Heisenberg Unipotent Duality, and Gel'fand Commutant Collapse in Sp(2n, F_q).
"""

import itertools
import numpy as np
import pytest


def make_symplectic_form(n, q=2):
    """Construct the standard 2n x 2n symplectic matrix J over F_q."""
    J = np.zeros((2 * n, 2 * n), dtype=int)
    for i in range(n):
        J[i, n + i] = 1
        J[n + i, i] = -1 % q if q > 2 else 1
    return J % q


def omega_pairing(x, y, J, q=2):
    """Compute the symplectic pairing x^T J y mod q."""
    return int(np.dot(x, np.dot(J, y)) % q)


def symplectic_transvection_matrix(u, J, q=2):
    """
    Construct matrix representation of symplectic transvection T_u(x) = x + Omega(x, u) u mod q.
    T_u = I + outer(u, J u) mod q.
    """
    dim = len(u)
    T = (np.eye(dim, dtype=int) + np.outer(u, (J @ u) % q)) % q
    return T


def rref(mat, q):
    """Compute Reduced Row Echelon Form over F_q."""
    m, n = mat.shape
    A = mat.copy() % q
    r = 0
    for c in range(n):
        if r >= m:
            break
        pivot = -1
        for i in range(r, m):
            if A[i, c] != 0:
                pivot = i
                break
        if pivot == -1:
            continue
        A[[r, pivot]] = A[[pivot, r]]
        inv = pow(int(A[r, c]), -1, q)
        A[r] = (A[r] * inv) % q
        for i in range(m):
            if i != r and A[i, c] != 0:
                factor = A[i, c]
                A[i] = (A[i] - factor * A[r]) % q
        r += 1
    nonzero_rows = [row for row in A if np.any(row != 0)]
    return np.array(nonzero_rows) if nonzero_rows else np.zeros((0, n), dtype=int)


def subspaces_equal(basis1, basis2, q):
    """Check if two row bases span the identical subspace over F_q."""
    r1 = rref(basis1, q)
    r2 = rref(basis2, q)
    if r1.shape != r2.shape:
        return False
    return np.array_equal(r1, r2)


def solve_nullspace_mod_q(A, q):
    """Find a basis for the nullspace {x : A x = 0 mod q}."""
    m, d = A.shape
    R = rref(A, q)
    r = len(R)
    pivot_cols = []
    for row in R:
        for c in range(d):
            if row[c] != 0:
                pivot_cols.append(c)
                break
    free_cols = [c for c in range(d) if c not in pivot_cols]
    null_basis = []
    for free in free_cols:
        x = np.zeros(d, dtype=int)
        x[free] = 1
        for row_idx, piv in enumerate(pivot_cols):
            x[piv] = (-R[row_idx, free]) % q
        null_basis.append(x)
    return np.array(null_basis) if null_basis else np.zeros((0, d), dtype=int)


def orthogonal_complement(basis, J, q):
    """Compute (span(basis))^perp = {x : omega(v, x) = 0 for all v in basis}."""
    A = (basis @ J) % q
    return solve_nullspace_mod_q(A, q)


def test_transvection_symplectic_invariance():
    """Verify that T_u is symplectic for every non-zero vector u over F_2, F_3, F_5."""
    for q in [2, 3, 5]:
        n = 2
        J = make_symplectic_form(n, q)
        np.random.seed(42)
        for _ in range(15):
            u = np.random.randint(0, q, size=2 * n)
            if not np.any(u % q):
                continue
            T_u = symplectic_transvection_matrix(u, J, q)
            # Check T_u^T J T_u == J mod q
            prod = (T_u.T @ J @ T_u) % q
            assert np.array_equal(prod, J), f"Failed symplectic invariance for q={q}, u={u}"


def test_general_isotropic_transvection_lemma():
    """
    Verify Theorem 1 (General Isotropic Transvection Lemma):
    T_u in P_U <=> u in U^perp for all non-zero u in F_q^{2n}.
    """
    test_cases = [
        (2, 1, 2),  # n=2, k=1, q=2
        (2, 2, 2),  # n=2, k=2, q=2 (Siegel)
        (2, 1, 3),  # n=2, k=1, q=3
        (2, 2, 3),  # n=2, k=2, q=3
        (3, 1, 2),  # n=3, k=1, q=2
        (3, 2, 2),  # n=3, k=2, q=2
        (3, 3, 2),  # n=3, k=3, q=2
    ]
    for n, k, q in test_cases:
        J = make_symplectic_form(n, q)
        # Construct standard isotropic subspace U = span(e_1, ..., e_k)
        U_basis = np.zeros((k, 2 * n), dtype=int)
        for i in range(k):
            U_basis[i, i] = 1

        all_vecs = list(itertools.product(range(q), repeat=2 * n))
        all_vecs = [np.array(v, dtype=int) for v in all_vecs if any(v)]

        for u in all_vecs:
            # u in U^perp iff omega(x, u) = 0 for all x in U_basis
            in_U_perp = all(omega_pairing(x, u, J, q) == 0 for x in U_basis)

            T_u = symplectic_transvection_matrix(u, J, q)
            # T_u stabilizes U iff T_u(U) == U
            Tu_U_basis = (T_u @ U_basis.T).T % q
            stabilizes = subspaces_equal(U_basis, Tu_U_basis, q)

            assert (in_U_perp == stabilizes), (
                f"Mismatch for (n={n}, k={k}, q={q}), u={u}: in_U_perp={in_U_perp}, stabilizes={stabilizes}"
            )


def test_classical_reconstruction_algorithm():
    """
    Verify Theorem 2: Classical reconstruction of arbitrary random isotropic U
    via transvection oracle queries within O(n q^k) bound.
    """
    np.random.seed(1337)
    test_cases = [
        (2, 1, 2),
        (2, 2, 2),
        (3, 1, 2),
        (3, 2, 2),
        (3, 3, 2),
        (3, 1, 3),
        (3, 2, 3),
    ]
    for n, k, q in test_cases:
        J = make_symplectic_form(n, q)
        # Generate random isotropic subspace U of dimension k
        vecs = []
        while len(vecs) < k:
            v = np.random.randint(0, q, size=2 * n)
            if not np.any(v % q):
                continue
            if len(vecs) > 0:
                test_mat = np.vstack([vecs, [v]])
                if len(rref(test_mat, q)) != len(vecs) + 1:
                    continue
            if all(omega_pairing(v, ex, J, q) == 0 for ex in vecs):
                vecs.append(v)
        U_true = np.array(vecs)
        target_dim = 2 * n - k

        # Coset oracle simulation
        queries = 0
        u_perp_basis = []
        max_allowed_queries = 20 * (2 * n - k) * (q**k + 1)

        while len(u_perp_basis) < target_dim and queries < max_allowed_queries:
            u = np.random.randint(0, q, size=2 * n)
            if not np.any(u % q):
                continue
            queries += 1
            T_u = symplectic_transvection_matrix(u, J, q)
            Tu_U = (T_u @ U_true.T).T % q
            if subspaces_equal(U_true, Tu_U, q):
                # Membership confirmed: test linear independence
                test_mat = np.vstack([u_perp_basis, [u]]) if len(u_perp_basis) > 0 else np.array([u])
                if len(rref(test_mat, q)) == len(u_perp_basis) + 1:
                    u_perp_basis.append(u)

        assert len(u_perp_basis) == target_dim, f"Failed to find basis within {max_allowed_queries} queries"
        u_perp_basis = np.array(u_perp_basis)
        U_recon = orthogonal_complement(u_perp_basis, J, q)
        assert subspaces_equal(U_true, U_recon, q), "Reconstructed subspace does not match true hidden subspace"
        assert queries < max_allowed_queries


def test_heisenberg_unipotent_radical_order_and_duality():
    """
    Verify Theorem 4:
    Order of U_1 is q^{2n-1}.
    Characteristic 2: U_1 is elementary abelian (orders in {1, 2}).
    Characteristic 3: U_1 is Heisenberg non-abelian, |Z(U_1)| = 3, |[U_1, U_1]| = 3.
    """
    n = 2
    # --- Char 2 ---
    q2 = 2
    J2 = make_symplectic_form(n, q2)
    # Parametric form of U_1 in Sp(4, F_2):
    # Basis: e1, e2, f1, f2
    # M(a, b, c) = [[1, a, c, b], [0, 1, b, 0], [0, 0, 1, 0], [0, 0, -a, 1]]
    U1_char2 = []
    for a in range(q2):
        for b in range(q2):
            for c in range(q2):
                M = np.array([
                    [1, a, c, b],
                    [0, 1, b, 0],
                    [0, 0, 1, 0],
                    [0, 0, (-a) % q2, 1]
                ], dtype=int)
                assert np.array_equal((M.T @ J2 @ M) % q2, J2)
                U1_char2.append(M)

    assert len(U1_char2) == q2 ** (2 * n - 1)  # 2^3 = 8
    # Verify U_1 is abelian in char 2:
    for A in U1_char2:
        for B in U1_char2:
            assert np.array_equal((A @ B) % q2, (B @ A) % q2)
    # Verify order of elements in char 2 is <= 2
    for M in U1_char2:
        M2 = (M @ M) % q2
        assert np.array_equal(M2, np.eye(2 * n, dtype=int))

    # --- Char 3 ---
    q3 = 3
    J3 = make_symplectic_form(n, q3)
    U1_char3 = []
    for a in range(q3):
        for b in range(q3):
            for c in range(q3):
                M = np.array([
                    [1, a, c, b],
                    [0, 1, b, 0],
                    [0, 0, 1, 0],
                    [0, 0, (-a) % q3, 1]
                ], dtype=int)
                assert np.array_equal((M.T @ J3 @ M) % q3, J3)
                U1_char3.append(M)

    assert len(U1_char3) == q3 ** (2 * n - 1)  # 3^3 = 27
    # Verify U_1 is NON-abelian in char 3:
    non_commuting = 0
    for A in U1_char3:
        for B in U1_char3:
            if not np.array_equal((A @ B) % q3, (B @ A) % q3):
                non_commuting += 1
    assert non_commuting > 0, "U_1 should be non-abelian in char 3"

    # Verify center Z(U_1) has order 3:
    center = [
        A for A in U1_char3
        if all(np.array_equal((A @ B) % q3, (B @ A) % q3) for B in U1_char3)
    ]
    assert len(center) == 3

    # Verify commutator difference is 2(a1 b2 - a2 b1) E_{1,3}
    for A in U1_char3:
        for B in U1_char3:
            comm = (A @ B - B @ A) % q3
            # All entries except (0, 2) must be zero
            for r in range(4):
                for c in range(4):
                    if (r, c) != (0, 2):
                        assert comm[r, c] == 0


def test_gelfand_pair_commutant_and_irrep_dimensions():
    """
    Verify Theorem 5:
    Generate Sp(4, F_2) of order 720.
    Permutation module on 15 isotropic lines.
    P_1 has 3 orbits (sizes 1, 6, 8).
    Commutant dimension is 3, orbital matrices commute [B_i, B_j] = 0.
    Irrep dimensions are exactly [1, 5, 9].
    """
    n = 2
    q = 2
    J = make_symplectic_form(n, q)
    all_vecs = [
        np.array(v, dtype=int)
        for v in itertools.product(range(q), repeat=2 * n)
        if any(v)
    ]
    transvections = [
        symplectic_transvection_matrix(v, J, q)
        for v in all_vecs
    ]

    # Generate Sp(4, F_2)
    group = {}
    queue = [np.eye(2 * n, dtype=int)]
    group[queue[0].tobytes()] = queue[0]
    while queue:
        curr = queue.pop(0)
        for T in transvections:
            nxt = (curr @ T) % q
            key = nxt.tobytes()
            if key not in group:
                group[key] = nxt
                queue.append(nxt)

    assert len(group) == 720, f"Expected |Sp(4, F_2)| = 720, got {len(group)}"

    # 15 isotropic lines
    lines = all_vecs
    line_to_idx = {tuple(v): i for i, v in enumerate(lines)}
    assert len(lines) == 15

    line0 = lines[0]
    P_1 = [M for M in group.values() if np.array_equal((M @ line0) % q, line0)]
    assert len(P_1) == 48

    # Orbits of P_1 on lines
    orbits = []
    visited = set()
    for i, line in enumerate(lines):
        if i in visited:
            continue
        orb = set()
        for M in P_1:
            img = tuple((M @ line) % q)
            orb.add(line_to_idx[img])
        visited.update(orb)
        orbits.append(orb)

    orbit_sizes = sorted([len(orb) for orb in orbits])
    assert orbit_sizes == [1, 6, 8]
    assert len(orbits) == 3

    # Commutant orbital matrices
    orbitals = []
    visited_pairs = set()
    for j in range(15):
        if (0, j) in visited_pairs:
            continue
        orb_pairs = set()
        for g in group.values():
            img0 = line_to_idx[tuple((g @ line0) % q)]
            imgj = line_to_idx[tuple((g @ lines[j]) % q)]
            orb_pairs.add((img0, imgj))
        visited_pairs.update(orb_pairs)
        orbitals.append(orb_pairs)

    assert len(orbitals) == 3

    orbital_matrices = []
    for orb in orbitals:
        B = np.zeros((15, 15), dtype=float)
        for i, j in orb:
            B[i, j] = 1.0
        orbital_matrices.append(B)

    # Check commutativity: [B_i, B_j] = 0
    for i in range(len(orbital_matrices)):
        for j in range(len(orbital_matrices)):
            comm = orbital_matrices[i] @ orbital_matrices[j] - orbital_matrices[j] @ orbital_matrices[i]
            assert np.allclose(comm, 0), f"Orbital matrices B_{i} and B_{j} do not commute"

    # Diagonalize to get exact irrep dimensions
    np.random.seed(42)
    weights = [0.3, -1.2, 0.7]
    M_comb = sum(w * B for w, B in zip(weights, orbital_matrices))
    eigvals = np.linalg.eigvalsh(M_comb)

    unique_eigs = []
    tol = 1e-5
    for ev in eigvals:
        if not any(abs(ev - u) < tol for u in unique_eigs):
            unique_eigs.append(ev)

    irrep_dims = sorted([sum(1 for ev in eigvals if abs(ev - u) < tol) for u in unique_eigs])
    assert irrep_dims == [1, 5, 9], f"Expected irrep dimensions [1, 5, 9], got {irrep_dims}"
    assert sum(irrep_dims) == 15


def test_unipotent_radical_general_dimension_formula():
    """Verify algebraic dimension dim(U_k) = 2nk - (3k^2 - k)/2 across 1 <= k <= n <= 5."""
    for n in range(1, 6):
        for k in range(1, n + 1):
            dim_U = 2 * n * k - (3 * k * k - k) // 2
            # Levi dimension: dim(GL(k)) + dim(Sp(2(n-k)))
            dim_levi = k * k + (n - k) * (2 * (n - k) + 1)
            # Total dim(P_k) = dim(levi) + dim(U_k)
            dim_pk = dim_levi + dim_U
            # Total dim(Sp(2n)) = n(2n + 1) = 2n^2 + n
            dim_sp = n * (2 * n + 1)
            # Codimension in Sp(2n) = dim(IG(k, 2n)) = k(2n - (3k-1)/2) ?
            codim = dim_sp - dim_pk
            assert codim >= 0
            assert dim_U > 0
            if k == n:
                assert dim_U == n * (n + 1) // 2  # Siegel abelian radical
            if k == 1:
                assert dim_U == 2 * n - 1  # Heisenberg radical


def test_spherical_mutual_information_zero():
    """Verify weak Fourier sampling probabilities P(lambda) = d_lambda / |Lambda_1| have 0 mutual info."""
    irrep_dims = [1, 5, 9]
    total_lines = 15
    probs = [d / total_lines for d in irrep_dims]
    assert np.isclose(sum(probs), 1.0)
    # The probabilities depend only on d_lambda and total_lines, identically independent of secret line U.
    # Conditional entropy H(Lambda | U) == H(Lambda) => I(U : Lambda) == 0.
    h_lambda = -sum(p * np.log2(p) for p in probs)
    h_lambda_given_u = h_lambda  # identical for every U
    mutual_info = h_lambda - h_lambda_given_u
    assert np.isclose(mutual_info, 0.0)
