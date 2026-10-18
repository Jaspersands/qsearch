r"""DCP symplectic Clifford stabilizer tableau GL_K(F_2) witness compiler bridge.

Establishes the exact symplectic stabilizer tableau transformation of any invertible
CNOT circuit U_CNOT(W) on K wires (W in GL_K(F_2)) and proves how placing m linearly
independent mod-2 kernel basis vectors v_1, ..., v_m in the first m columns of W^{-1}
compiles a unified CNOT tableau whose anchor-zero branch simultaneously extracts all m
even-sublattice witnesses:

1. Exact Symplectic Contragredient Tableau Law:
   Under a reversible CNOT network mapping computational basis states |x> -> |u = W x mod 2>,
   the 2K x 2K binary symplectic Pauli tableau transforms via the block-diagonal matrix:
       S_W = [[W, 0], [0, (W^{-1})^T]] over F_2,
   which identically preserves the canonical symplectic form Omega = [[0, I_K], [I_K, 0]]:
       S_W^T * Omega * S_W == Omega (mod 2).
   In particular, because x = W^{-1} u (mod 2), the j-th compressed wire u_j controls the
   computational support vector v_j = (W^{-1})_{., j} in {0, 1}^K!

2. Simultaneous Multi-Witness Tableau Compilation on the Anchor-Zero Branch:
   Let V_ker = [v_1, ..., v_m] in {0, 1}^{K x m} be any full-rank basis of ker(A mod 2),
   and complete V_ker to an invertible matrix M = W^{-1} = [v_1, ..., v_m, e_{i_1}, ..., e_{i_{K-m}}]
   in GL_K(F_2).
   On the zero-syndrome anchor branch u_{m+1} = ... = u_K = 0:
   - Whenever only a single survivor wire u_j = 1 (and u_{j'} = 0 for j' != j) is excited,
     x = v_j, so wire j carries the exact even-sublattice column sum:
         A v_j in (2 * Z_{2^t})^n   for all j in {1, ..., m}!
   - Moreover, when the supports supp(v_1), ..., supp(v_m) are pairwise disjoint, all m
     survivor wires factorize into an exact tensor product of m independent even-sublattice
     phase states across ALL 2^{K-m} syndromes!
"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, List, Sequence


THEOREM_ID = "dcp_symplectic_clifford_stabilizer_tableau_witness_compiler_bridge"
SCHEMA_VERSION = "dcp-symplectic-clifford-stabilizer-tableau-witness-compiler-bridge-v1"

IntMatrix = List[List[int]]


def _gf2_matmul(a: IntMatrix, b: IntMatrix) -> IntMatrix:
    r = len(a)
    c = len(b[0])
    k_len = len(b)
    return [
        [sum(a[i][k] * b[k][j] for k in range(k_len)) & 1 for j in range(c)]
        for i in range(r)
    ]


def _gf2_transpose(a: IntMatrix) -> IntMatrix:
    r = len(a)
    c = len(a[0])
    return [[a[i][j] for i in range(r)] for j in range(c)]


def _gf2_invert(mat: Sequence[Sequence[int]]) -> IntMatrix:
    n = len(mat)
    aug = [
        [int(mat[i][j]) & 1 for j in range(n)] + [1 if i == j else 0 for j in range(n)]
        for i in range(n)
    ]
    for col in range(n):
        pivot = next((r for r in range(col, n) if aug[r][col] == 1), None)
        if pivot is None:
            raise ValueError("Matrix is singular over GF(2)")
        aug[col], aug[pivot] = aug[pivot], aug[col]
        for r in range(n):
            if r != col and aug[r][col] == 1:
                for c in range(2 * n):
                    aug[r][c] ^= aug[col][c]
    return [row[n:] for row in aug]


def evaluate_symplectic_tableau_witness_compiler(
    a_matrix: Sequence[Sequence[int]],
    q_mod: int,
    w_inv_matrix: Sequence[Sequence[int]],
    m_witnesses: int,
) -> Dict[str, Any]:
    """Verify symplectic preservation S_W^T Omega S_W == Omega mod 2 and even-sublattice extraction for the first m columns of W^{-1}."""
    n_rows = len(a_matrix)
    k_cols = len(a_matrix[0])
    w_inv = [[int(w_inv_matrix[i][j]) & 1 for j in range(k_cols)] for i in range(k_cols)]
    w_mat = _gf2_invert(w_inv)
    w_inv_t = _gf2_transpose(w_inv)

    # 1. Construct 2K x 2K symplectic tableau S_W = [[W, 0], [0, (W^{-1})^T]] and Omega = [[0, I], [I, 0]]:
    s_tab = [[0] * (2 * k_cols) for _ in range(2 * k_cols)]
    omega = [[0] * (2 * k_cols) for _ in range(2 * k_cols)]
    for i in range(k_cols):
        omega[i][k_cols + i] = 1
        omega[k_cols + i][i] = 1
        for j in range(k_cols):
            s_tab[i][j] = w_mat[i][j]
            s_tab[k_cols + i][k_cols + j] = w_inv_t[i][j]

    s_t = _gf2_transpose(s_tab)
    lhs_symp = _gf2_matmul(_gf2_matmul(s_t, omega), s_tab)
    symplectic_preserved = (lhs_symp == omega)

    # 2. Check that the first m_witnesses columns of W^{-1} map A * v_j into (2 * Z_q)^n:
    witness_columns: List[List[int]] = []
    all_even = True
    for j in range(m_witnesses):
        v_j = [w_inv[r][j] for r in range(k_cols)]
        av_j = [
            sum(int(a_matrix[i][r]) * v_j[r] for r in range(k_cols)) % q_mod
            for i in range(n_rows)
        ]
        if any((val % 2) != 0 for val in av_j):
            all_even = False
        witness_columns.append(av_j)

    # Check whether the first m_witnesses columns of W^{-1} have pairwise disjoint supports:
    row_counts = [sum(w_inv[r][j] for j in range(m_witnesses)) for r in range(k_cols)]
    disjoint_supports = all(c <= 1 for c in row_counts)

    return {
        "n_rows": n_rows,
        "K_wires": k_cols,
        "q_mod": q_mod,
        "m_witnesses": m_witnesses,
        "symplectic_form_preserved_mod2": symplectic_preserved,
        "all_m_witnesses_in_even_sublattice": all_even,
        "witness_supports_disjoint": disjoint_supports,
        "extracted_even_sublattice_columns": witness_columns,
        "exact_tableau_laws_verified": symplectic_preserved and all_even,
    }


def generate_dcp_symplectic_clifford_stabilizer_tableau_witness_compiler_certificate() -> Dict[str, Any]:
    """Generate the complete certificate for the symplectic Clifford stabilizer tableau witness compiler bridge."""
    # 1. 4-wire disjoint 2-witness compiler over Z_{16}^2:
    # A = [[1, 3, 5, 7], [2, 4, 1, 3]] mod 16:
    # v_1 = [1, 1, 0, 0]^T -> A v_1 = [4, 6]^T in (2*Z_{16})^2
    # v_2 = [0, 0, 1, 1]^T -> A v_2 = [12, 4]^T in (2*Z_{16})^2
    a_disjoint = [
        [1, 3, 5, 7],
        [2, 4, 1, 3],
    ]
    w_inv_disjoint = [
        [1, 0, 0, 0],
        [1, 0, 1, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 1],
    ]
    disjoint_audit = evaluate_symplectic_tableau_witness_compiler(
        a_matrix=a_disjoint,
        q_mod=16,
        w_inv_matrix=w_inv_disjoint,
        m_witnesses=2,
    )

    # 2. 4-wire coupled 3-witness compiler over Z_8^2:
    # A = [[1, 1, 1, 0], [0, 2, 2, 1]] mod 8:
    # v_1 = [1, 1, 0, 0]^T -> A v_1 = [2, 2]^T
    # v_2 = [0, 1, 1, 0]^T -> A v_2 = [2, 4]^T
    a_coupled = [
        [1, 1, 1, 0],
        [0, 2, 2, 1],
    ]
    w_inv_coupled = [
        [1, 0, 0, 0],
        [1, 1, 1, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
    ]
    coupled_audit = evaluate_symplectic_tableau_witness_compiler(
        a_matrix=a_coupled,
        q_mod=8,
        w_inv_matrix=w_inv_coupled,
        m_witnesses=2,
    )

    all_passed = (
        disjoint_audit["exact_tableau_laws_verified"]
        and disjoint_audit["witness_supports_disjoint"]
        and coupled_audit["exact_tableau_laws_verified"]
        and not coupled_audit["witness_supports_disjoint"]
    )

    payload = {
        "theorem_id": THEOREM_ID,
        "schema_version": SCHEMA_VERSION,
        "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING_NOT_FORMALLY_VERIFIED",
        "scope_constraints": {
            "applies_to": "Symplectic GL_K(F_2) stabilizer tableau compilation S_W = diag(W, (W^{-1})^T) for mod-2 CNOT witness extraction",
            "does_not_claim": "Multi-wire carry independence when columns of W^{-1} share overlapping row supports (see Subsystem 87)",
            "controls_included": "Includes 4-wire disjoint 2-witness compiler over Z_{16}^2 and 4-wire overlapping 2-witness compiler over Z_8^2, verifying S_W^T Omega S_W == Omega mod 2 and exact even-sublattice column extraction.",
        },
        "disjoint_tableau_audit": disjoint_audit,
        "coupled_tableau_audit": coupled_audit,
        "all_checks_passed": all_passed,
        "honesty_guardrails": {
            "accepted_speedup_candidate": False,
            "new_active_negative_result_created": False,
            "novelty_claim": False,
        },
    }
    digest = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()[:16]
    payload["certificate_sha256_16"] = digest
    return payload
