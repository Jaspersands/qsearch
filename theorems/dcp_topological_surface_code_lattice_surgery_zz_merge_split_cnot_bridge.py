r"""
Subsystem 155: Topological Surface Code Lattice Surgery ZZ-Merge & XX-Split CNOT Bridge.

Evaluates the Horsman-Fowler-Devitt-Van Meter lattice surgery protocol for executing
fault-tolerant logical CNOT gates between distance-d rotated surface code patches
via actual 3-qubit Kraus projectors on (Control C, Ancilla A, Target T):
  1. Starting from an arbitrary two-qubit input |\psi>_{CT} and ancilla |+>_A,
     a logical CNOT(C -> T) executes three projective measurements with outcomes
     (m_ZZ, m_XX, m_Z) in {0, 1}^3:
       Step 1 (Rough boundary merge): Projective measurement of Z_C Z_A with outcome m_ZZ in {0, 1}.
       Step 2 (Smooth boundary split): Projective measurement of X_A X_T with outcome m_XX in {0, 1}.
       Step 3 (Ancilla patch readout): Destructive Z_A measurement with outcome m_Z in {0, 1}.
  2. Direct Kraus evaluation K(m_ZZ, m_XX, m_Z) = <m_Z|_A P_XX(m_XX) P_ZZ(m_ZZ) |+>_A proves:
       K(m_ZZ, m_XX, m_Z) = (1 / (2 sqrt(2))) (-1)^{m_XX (m_ZZ xor m_Z)} Z_C^{m_XX} X_T^{m_ZZ xor m_Z} CNOT_{C->T}.
     Therefore, the exact Pauli byproduct correction is Z_C^{m_XX} X_T^{m_ZZ xor m_Z}
     (up to the deterministic global phase (-1)^{m_XX (m_ZZ xor m_Z)}), whereas the naive
     two-bit formula Z_C^{m_ZZ} X_T^{m_XX} fails on 6 out of 8 measurement branches!
  3. Resource scaling: Each rotated surface code patch uses d^2 data qubits (3 d^2 data
     qubits across Control, Ancilla, Target) and 2 d syndrome rounds per CNOT, with
     heuristic logical failure scaling p_L(d) = 0.1 (p / p_{th})^{(d+1)/2}.
"""

from __future__ import annotations
from itertools import product
from typing import Any, Dict, List
import numpy as np


def evaluate_lattice_surgery_cnot_resources_and_fidelity(
    code_distances: List[int] = [3, 5, 7, 9, 11],
    physical_error_p: float = 0.001,
    threshold_p_th: float = 0.01,
    cnot_tree_gates: int = 15,
) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for d in code_distances:
        data_qubits_per_patch = d * d
        three_patch_cnot_data_qubits = 3 * data_qubits_per_patch
        syndrome_rounds_per_cnot = 2 * d
        logical_err_per_cnot = 0.1 * ((physical_error_p / threshold_p_th) ** ((d + 1) // 2))
        tree_logical_fidelity = (1.0 - logical_err_per_cnot) ** cnot_tree_gates
        rows.append({
            "code_distance_d": int(d),
            "data_qubits_per_rotated_patch": int(data_qubits_per_patch),
            "three_patch_cnot_footprint_qubits": int(three_patch_cnot_data_qubits),
            "syndrome_rounds_per_logical_cnot": int(syndrome_rounds_per_cnot),
            "logical_error_per_cnot": float(logical_err_per_cnot),
            "fifteen_cnot_tree_logical_fidelity": float(tree_logical_fidelity),
        })
    return rows


def verify_lattice_surgery_pauli_byproduct_truth_table() -> Dict[str, Any]:
    """
    Construct the actual 8x8 projectors on (C, A, T) and verify all 8 measurement
    branches (m_ZZ, m_XX, m_Z) in {0, 1}^3 on:
      - Full 4x4 Kraus operators against CNOT_{C->T} (Choi / entangled reference check),
      - Arbitrary complex two-qubit superposition states,
      - Explicit countercontrol demonstrating that the naive two-bit formula
        Z_C^{m_ZZ} X_T^{m_XX} fails on 6 of the 8 branches.
    """
    I2 = np.eye(2, dtype=complex)
    X = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
    Z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
    CNOT = np.array(
        [[1, 0, 0, 0],
         [0, 1, 0, 0],
         [0, 0, 0, 1],
         [0, 0, 1, 0]],
        dtype=complex,
    )

    # Embed 2-qubit state |psi>_{CT} into 3-qubit |psi>_{C,A,T} with ancilla A in |+>_A
    plus_A = np.array([1.0, 1.0], dtype=complex) / np.sqrt(2.0)
    embed = np.zeros((8, 4), dtype=complex)
    for c, a, t in product((0, 1), repeat=3):
        row_cat = (c << 2) | (a << 1) | t
        col_ct = (c << 1) | t
        embed[row_cat, col_ct] = plus_A[a]

    ZZ_CA = np.kron(np.kron(Z, Z), I2)
    XX_AT = np.kron(np.kron(I2, X), X)
    I8 = np.eye(8, dtype=complex)

    # Arbitrary complex 2-qubit test state and 4-qubit maximally entangled Choi state
    psi_test = np.array([0.3 - 0.4j, -0.5 + 0.1j, 0.2 + 0.6j, -0.1 - 0.3j], dtype=complex)
    psi_test = psi_test / np.linalg.norm(psi_test)
    target_psi = CNOT @ psi_test

    # 4-qubit Choi state (I_4 \otimes CNOT) |\Phi^+_4>
    choi_input = np.eye(4, dtype=complex).reshape(16) / 2.0
    choi_target = (np.kron(np.eye(4, dtype=complex), CNOT) @ choi_input)

    completeness = np.zeros((4, 4), dtype=complex)
    branch_rows: List[Dict[str, Any]] = []
    all_three_bit_exact = True
    naive_two_bit_failures = 0

    for m_zz, m_xx, m_z in product((0, 1), repeat=3):
        P_zz = 0.5 * (I8 + ((-1) ** m_zz) * ZZ_CA)
        P_xx = 0.5 * (I8 + ((-1) ** m_xx) * XX_AT)
        # Project ancilla A onto <m_z|_A
        proj_m_z = np.zeros((4, 8), dtype=complex)
        for c, t in product((0, 1), repeat=2):
            proj_m_z[(c << 1) | t, (c << 2) | (m_z << 1) | t] = 1.0

        K = proj_m_z @ P_xx @ P_zz @ embed
        completeness += K.conj().T @ K
        branch_prob = float(np.real(np.vdot(K @ psi_test, K @ psi_test)))

        # True 3-bit Pauli correction: Z_C^{m_XX} X_T^{m_ZZ ^ m_Z}
        corr_3bit = np.kron(np.linalg.matrix_power(Z, m_xx), np.linalg.matrix_power(X, m_zz ^ m_z))
        global_phase = (-1) ** (m_xx * (m_zz ^ m_z))
        effective_unitary = (2.0 * np.sqrt(2.0)) * global_phase * (corr_3bit @ K)
        op_residual = float(np.linalg.norm(effective_unitary - CNOT, ord="fro"))

        # Check on arbitrary complex 2-qubit input and 4-qubit entangled Choi state
        corrected_psi = (corr_3bit @ (K @ psi_test)) / np.sqrt(branch_prob)
        psi_residual = float(np.linalg.norm(global_phase * corrected_psi - target_psi))
        choi_branch = np.kron(np.eye(4, dtype=complex), (2.0 * np.sqrt(2.0)) * global_phase * (corr_3bit @ K)) @ choi_input
        choi_residual = float(np.linalg.norm(choi_branch - choi_target))

        if op_residual > 1e-12 or psi_residual > 1e-12 or choi_residual > 1e-12 or abs(branch_prob - 0.125) > 1e-12:
            all_three_bit_exact = False

        # Naive 2-bit correction countercontrol: Z_C^{m_ZZ} X_T^{m_XX}
        corr_naive = np.kron(np.linalg.matrix_power(Z, m_zz), np.linalg.matrix_power(X, m_xx))
        naive_unitary = (2.0 * np.sqrt(2.0)) * (corr_naive @ K)
        # Check distance up to any global phase e^{i theta}
        overlap = abs(np.trace(naive_unitary.conj().T @ CNOT)) / 4.0
        naive_matches = bool(abs(overlap - 1.0) < 1e-12)
        if not naive_matches:
            naive_two_bit_failures += 1

        branch_rows.append({
            "m_ZZ": int(m_zz),
            "m_XX": int(m_xx),
            "m_Z": int(m_z),
            "branch_probability": branch_prob,
            "correction_operator": f"Z_C^{m_xx} X_T^{m_zz ^ m_z}",
            "global_phase_sign": int(global_phase),
            "kraus_operator_residual": op_residual,
            "entangled_choi_residual": choi_residual,
            "naive_two_bit_correction_matches_up_to_phase": naive_matches,
        })

    completeness_residual = float(np.linalg.norm(completeness - np.eye(4, dtype=complex), ord="fro"))
    return {
        "outcomes_checked": 8,
        "byproduct_law": "Z_C^{m_XX} X_T^{m_ZZ xor m_Z}",
        "byproduct_sign_cancellation_exact": bool(all_three_bit_exact and completeness_residual < 1e-12),
        "kraus_completeness_residual": completeness_residual,
        "naive_two_bit_formula_failing_branches": int(naive_two_bit_failures),
        "branches": branch_rows,
    }


def generate_dcp_topological_surface_code_lattice_surgery_zz_merge_split_cnot_certificate() -> Dict[str, Any]:
    """Generate the Subsystem 155 verification certificate."""
    byproduct = verify_lattice_surgery_pauli_byproduct_truth_table()
    sweep = evaluate_lattice_surgery_cnot_resources_and_fidelity([3, 5, 7, 9, 11], physical_error_p=0.001)

    d7_row = [r for r in sweep if r["code_distance_d"] == 7][0]
    theorem_checks = {
        "lattice_surgery_byproduct_cancels_all_measurement_signs": bool(
            byproduct["byproduct_sign_cancellation_exact"]
            and byproduct["outcomes_checked"] == 8
            and byproduct["naive_two_bit_formula_failing_branches"] == 6
        ),
        "logical_error_suppresses_exponentially_with_code_distance_d": bool(
            all(sweep[i]["logical_error_per_cnot"] > sweep[i + 1]["logical_error_per_cnot"] for i in range(len(sweep) - 1))
        ),
        "distance_7_achieves_above_99_98pct_15_cnot_tree_fidelity": bool(
            d7_row["fifteen_cnot_tree_logical_fidelity"] > 0.9998
        ),
        "rotated_surface_code_3_patch_footprint_equals_3_d_squared": bool(
            all(r["three_patch_cnot_footprint_qubits"] == 3 * (r["code_distance_d"] ** 2) for r in sweep)
        ),
    }

    return {
        "subsystem_id": "dcp_topological_surface_code_lattice_surgery_zz_merge_split_cnot_bridge",
        "subsystem_number": 155,
        "domain": "topological_quantum_error_correction_surface_code_lattice_surgery",
        "byproduct_verification": byproduct,
        "distance_scaling_sweep": sweep,
        "theorem_checks": theorem_checks,
        "all_checks_passed": bool(all(theorem_checks.values())),
        "falsification_status": {
            "accepted_speedup_candidate": False,
            "new_active_negative_result_created": False,
            "novelty_claim": False,
        },
    }
