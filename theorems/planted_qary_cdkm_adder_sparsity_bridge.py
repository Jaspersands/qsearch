"""Planted q-ary CDKM adder sparsity bridge: q-independent free-column cell widths and gate compression.

Connects `theorems/planted_qary_usvp_source.py` (`PublicQaryLattice`, `generate_source`) and
`theorems/lattice_cube_source_circuit.py` (`cube_resource_estimate`, `compile_cube_evaluator`) by proving:
1. Theorem 1 (Centered-RREF Sparsity and Exact CDKM Addition Count):
   For any `PublicQaryLattice(q, H)` with dimension `n` and rows `m`, its public row basis `B` has
   `nnz(B) = n + nnz(C) <= n + m*(n - m)`. In `CubeCosetSource` with `box = 2^b` and free splitting
   row `j_coord = m + j_0`, the exact number of CDKM constant additions (including uncompute) is
   `N_add = 2 * (b * nnz(B) + (1 + nnz(C_{*, j_0})) + n)`, compared to `2 * (b * n^2 + 2 * n)` for a
   dense `n x n` basis.
2. Theorem 2 (Modulus-Independence of Free-Column Cell Output Widths):
   In `CubeCosetSource.clean_arithmetic_plan()`, every non-split free column `F_j` (`j != j_0`) has
   exact signed point bound `(M_box - 1) + W` and the split free column `F_{j_0}` has exact signed
   point bound `p_split * (M_box - 1) + g_res + W`, both completely independent of `q` and `n`.
3. Theorem 3 (Closed-Form Gate Count on Non-Split Free Columns):
   Every non-split free column `F_j` contributes `adds(F_j) = b + 1` and
   `popcount_sum(F_j) = b + w - popcount(offsets_{F_j} - 1)` to `cube_resource_estimate(source)`.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from sympy import nextprime

from theorems.lattice_cube_coset_source import CubeCosetSource
from theorems.lattice_cube_source_circuit import compile_cube_evaluator, cube_resource_estimate
from theorems.planted_qary_cube_basis_coordinate_bridge import (
    basis_coordinates_from_public_lattice,
    extract_centered_rref_structure,
)
from theorems.planted_qary_usvp_source import generate_source


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "research" / "hypotheses" / "planted_qary_cdkm_adder_sparsity_bridge_contract.json"
ARTIFACT_PATH = ROOT / "research" / "reductions" / "planted_qary_cdkm_adder_sparsity_bridge.json"
DOC_PATH = ROOT / "research" / "PLANTED_QARY_CDKM_ADDER_SPARSITY_BRIDGE.md"


def analyze_qary_cube_circuit_sparsity(
    n: int,
    m: int,
    q: int,
    support: int,
    seed: int,
    m_box: int,
    width: int,
    compile_circuit: bool = False,
) -> dict[str, Any]:
    """Audit centered-RREF basis sparsity, free-column widths, and CDKM resource compression."""
    gen = generate_source(
        n=n,
        m=m,
        q=q,
        gap=2,
        support=support,
        plant_seed=seed,
        matrix_seed=seed + 200,
    )
    problem = gen.problem
    planted_u = gen.private.plant
    d_coords = basis_coordinates_from_public_lattice(problem, planted_u)
    rref_struct = extract_centered_rref_structure(problem)
    C = rref_struct["C_centered"]
    pivots = problem.pivots
    free = problem.free

    j0 = next(j for j in range(n - m) if d_coords[m + j] != 0)
    j_coord = m + j0
    p_split = int(nextprime(width))
    g_res = 1
    offsets = tuple(1 for _ in range(n))

    source = CubeCosetSource(
        basis=problem.basis,
        prime=p_split,
        residue_guess=g_res,
        coordinate=j_coord,
        box=m_box,
        width=width,
        offsets=offsets,
    )
    plan = source.clean_arithmetic_plan()
    est = cube_resource_estimate(source)

    b = m_box.bit_length() - 1
    shift = width.bit_length() - 1
    w = int(est["max_signed_adder_bits"])

    nnz_C = sum(1 for i in range(m) for j in range(n - m) if C[i][j] != 0)
    nnz_C_col_j0 = sum(1 for i in range(m) if C[i][j0] != 0)
    nnz_B_actual = sum(1 for row in problem.basis for x in row if x != 0)
    nnz_B_formula = n + nnz_C

    free_col_nnz = [sum(1 for r in range(n) if problem.basis[r][f_col] != 0) for f_col in free]
    piv_col_nnz = [sum(1 for r in range(n) if problem.basis[r][p_col] != 0) for p_col in pivots]
    piv_col_nnz_formula = [1 + sum(1 for j in range(n - m) if C[i][j] != 0) for i in range(m)]

    expected_forward_adds = b * nnz_B_formula + (1 + nnz_C_col_j0) + n
    expected_total_adds = 2 * expected_forward_adds
    dense_total_adds = 2 * (b * (n * n) + 2 * n)
    saved_adds_vs_dense = dense_total_adds - expected_total_adds
    min_guaranteed_saved_adds = 2 * b * ((n - m) * (n - m - 1) + m * (m - 1)) + 2 * (n - m - 1)

    certs = plan["coordinate_width_certificates"]
    expected_split_free_bound = p_split * (m_box - 1) + g_res + width
    expected_nonsplit_free_bound = (m_box - 1) + width
    expected_split_free_bits = max(expected_split_free_bound.bit_length() + 1, shift + 1) - shift
    expected_nonsplit_free_bits = max(expected_nonsplit_free_bound.bit_length() + 1, shift + 1) - shift

    free_bounds_match = True
    free_cell_bits_list: list[int] = []
    for j, f_col in enumerate(free):
        cert = certs[f_col]
        exp_bound = expected_split_free_bound if j == j0 else expected_nonsplit_free_bound
        exp_cell_bits = expected_split_free_bits if j == j0 else expected_nonsplit_free_bits
        if cert["absolute_point_minus_offset_bound"] != exp_bound or cert["signed_cell_output_bits"] != exp_cell_bits:
            free_bounds_match = False
        free_cell_bits_list.append(int(cert["signed_cell_output_bits"]))

    piv_cell_bits_list = [int(certs[p_col]["signed_cell_output_bits"]) for p_col in pivots]

    nonsplit_popcount_matches = True
    for j, f_col in enumerate(free):
        if j == j0:
            continue
        col_adds = 0
        col_pop = 0
        for r_idx, row in enumerate(source.basis):
            coeff = (source.prime if r_idx == source.coordinate else 1) * row[f_col]
            if coeff:
                col_adds += b
                col_pop += (
                    b * coeff.bit_count()
                    if coeff > 0
                    else b * w - b * (b - 1) // 2 - b * ((-coeff) - 1).bit_count()
                )
        colour = source.residue_guess * source.basis[source.coordinate][f_col]
        if colour:
            col_adds += 1
            col_pop += colour.bit_count() if colour > 0 else w - ((-colour) - 1).bit_count()
        col_adds += 1
        col_pop += w - (source.offsets[f_col] - 1).bit_count()

        exp_col_adds = b + 1
        exp_col_pop = b + w - (source.offsets[f_col] - 1).bit_count()
        if col_adds != exp_col_adds or col_pop != exp_col_pop:
            nonsplit_popcount_matches = False

    compiled_matches_estimate = None
    if compile_circuit:
        compiled = compile_cube_evaluator(source)
        rec = compiled.resource_record()
        compiled_matches_estimate = bool(
            rec["compiled_qubits"] == est["compiled_qubits"]
            and rec["constant_additions_including_uncompute"] == expected_total_adds
            and rec["logical_instruction_count"] == est["logical_instruction_count"]
        )

    return {
        "n": n,
        "m": m,
        "n_minus_m": n - m,
        "q": int(q),
        "M_box": m_box,
        "b_box_bits": b,
        "width": width,
        "p_split": p_split,
        "g_res": g_res,
        "j0_free_index": j0,
        "j_coord_basis_row": j_coord,
        "nnz_C": nnz_C,
        "nnz_C_col_j0": nnz_C_col_j0,
        "nnz_B_actual": nnz_B_actual,
        "nnz_B_formula": nnz_B_formula,
        "free_col_nnz_all_equal_1": bool(all(x == 1 for x in free_col_nnz)),
        "piv_col_nnz_matches_formula": bool(piv_col_nnz == piv_col_nnz_formula),
        "actual_constant_additions_including_uncompute": int(est["constant_additions_including_uncompute"]),
        "formula_constant_additions_including_uncompute": int(expected_total_adds),
        "dense_basis_constant_additions": int(dense_total_adds),
        "saved_constant_additions_vs_dense": int(saved_adds_vs_dense),
        "min_guaranteed_saved_additions": int(min_guaranteed_saved_adds),
        "expected_split_free_point_bound": int(expected_split_free_bound),
        "expected_nonsplit_free_point_bound": int(expected_nonsplit_free_bound),
        "expected_split_free_cell_bits": int(expected_split_free_bits),
        "expected_nonsplit_free_cell_bits": int(expected_nonsplit_free_bits),
        "free_column_cell_bits": free_cell_bits_list,
        "pivot_column_cell_bits": piv_cell_bits_list,
        "max_signed_adder_bits_w": w,
        "compiled_qubits": int(est["compiled_qubits"]),
        "logical_instruction_count": int(est["logical_instruction_count"]),
        "theorem_1_addition_count_matches": bool(
            nnz_B_actual == nnz_B_formula
            and est["constant_additions_including_uncompute"] == expected_total_adds
            and saved_adds_vs_dense >= min_guaranteed_saved_adds
        ),
        "theorem_2_free_bounds_and_widths_match": bool(free_bounds_match),
        "theorem_3_nonsplit_free_popcount_matches": bool(nonsplit_popcount_matches),
        "compiled_qiskit_circuit_matches_estimate": compiled_matches_estimate,
    }


def audit_modulus_scaling_at_fixed_geometry() -> dict[str, Any]:
    """Audit fixed (n=8, m=4, M_box=16, W=4) across primes from q=257 to q > 2^80."""
    moduli = [257, 65537, 1000003, 1000000007, int(nextprime(2**80))]
    records: list[dict[str, Any]] = []
    for idx, q in enumerate(moduli):
        rec = analyze_qary_cube_circuit_sparsity(
            n=8,
            m=4,
            q=q,
            support=5,
            seed=50 + idx,
            m_box=16,
            width=4,
            compile_circuit=(idx == 0),
        )
        records.append(rec)

    split_bits_set = {r["expected_split_free_cell_bits"] for r in records}
    nonsplit_bits_set = {r["expected_nonsplit_free_cell_bits"] for r in records}
    total_free_cell_qubits_set = {sum(r["free_column_cell_bits"]) for r in records}

    return {
        "fixed_n": 8,
        "fixed_m": 4,
        "fixed_M_box": 16,
        "fixed_width": 4,
        "moduli_tested": [int(q) for q in moduli],
        "records": records,
        "split_free_cell_bits_constant_across_all_q": bool(len(split_bits_set) == 1),
        "nonsplit_free_cell_bits_constant_across_all_q": bool(len(nonsplit_bits_set) == 1),
        "total_free_column_cell_qubits_constant_across_all_q": bool(len(total_free_cell_qubits_set) == 1),
    }


def audit_dimension_family() -> list[dict[str, Any]]:
    """Audit centered-RREF CDKM sparsity across dimensions n = 4, 6, 8, 10, 12."""
    configs = [
        {"n": 4, "m": 2, "q": 257, "support": 3, "seed": 11, "m_box": 8, "width": 4, "compile": True},
        {"n": 6, "m": 3, "q": 1009, "support": 4, "seed": 17, "m_box": 16, "width": 4, "compile": False},
        {"n": 8, "m": 4, "q": 65537, "support": 5, "seed": 23, "m_box": 16, "width": 8, "compile": False},
        {"n": 10, "m": 5, "q": 1000003, "support": 6, "seed": 29, "m_box": 32, "width": 8, "compile": False},
        {"n": 12, "m": 6, "q": 1000003, "support": 8, "seed": 37, "m_box": 32, "width": 8, "compile": False},
    ]
    return [
        analyze_qary_cube_circuit_sparsity(
            n=c["n"],
            m=c["m"],
            q=c["q"],
            support=c["support"],
            seed=c["seed"],
            m_box=c["m_box"],
            width=c["width"],
            compile_circuit=c["compile"],
        )
        for c in configs
    ]


def build_planted_qary_cdkm_adder_sparsity_bridge_report() -> dict[str, Any]:
    """Build the complete JSON artifact for Subsystem 11."""
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    modulus_scaling = audit_modulus_scaling_at_fixed_geometry()
    dimension_family = audit_dimension_family()

    all_records = modulus_scaling["records"] + dimension_family
    t1_ok = all(
        r["free_col_nnz_all_equal_1"]
        and r["piv_col_nnz_matches_formula"]
        and r["theorem_1_addition_count_matches"]
        for r in all_records
    )
    t2_ok = (
        modulus_scaling["split_free_cell_bits_constant_across_all_q"]
        and modulus_scaling["nonsplit_free_cell_bits_constant_across_all_q"]
        and modulus_scaling["total_free_column_cell_qubits_constant_across_all_q"]
        and all(r["theorem_2_free_bounds_and_widths_match"] for r in all_records)
    )
    t3_ok = all(r["theorem_3_nonsplit_free_popcount_matches"] for r in all_records)
    compiled_ok = bool(
        modulus_scaling["records"][0]["compiled_qiskit_circuit_matches_estimate"]
        and dimension_family[0]["compiled_qiskit_circuit_matches_estimate"]
    )

    return {
        "schema_version": "1.0.0",
        "subsystem": "planted_qary_cdkm_adder_sparsity_bridge",
        "contract_id": contract["contract_id"],
        "doc_path": str(DOC_PATH.relative_to(ROOT)),
        "summary_of_theorems": {
            "T1_centered_rref_sparsity_and_addition_count": (
                "nnz(B) = n + nnz(C) <= n + m*(n - m), and total CDKM constant additions (with uncompute) "
                "equal N_add = 2 * (b * nnz(B) + (1 + nnz(C_{*, j_0})) + n)."
            ),
            "T2_modulus_independent_free_column_cell_widths": (
                "Every non-split free column F_j has point bound (M_box - 1) + W and the split free column "
                "F_{j_0} has point bound p_split*(M_box - 1) + g_res + W, both independent of q and n."
            ),
            "T3_closed_form_nonsplit_free_column_popcount": (
                "Every non-split free column F_j contributes adds(F_j) = b + 1 and "
                "popcount_sum(F_j) = b + w - popcount(offsets_{F_j} - 1)."
            ),
        },
        "modulus_scaling_audit": modulus_scaling,
        "dimension_family_audit": dimension_family,
        "verification": {
            "theorem_1_sparsity_and_addition_compression_verified": bool(t1_ok),
            "theorem_2_modulus_independent_free_cell_widths_verified": bool(t2_ok),
            "theorem_3_nonsplit_free_popcount_verified": bool(t3_ok),
            "compiled_qiskit_cdkm_circuits_match_closed_form": bool(compiled_ok),
        },
        "guardrails": contract["guardrails"],
    }


def write_planted_qary_cdkm_adder_sparsity_bridge_report(
    path: Path = ARTIFACT_PATH,
) -> dict[str, Any]:
    report = build_planted_qary_cdkm_adder_sparsity_bridge_report()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Write JSON artifact to research/reductions/.")
    parser.add_argument("--no-write", action="store_true", help="Build and validate report without writing.")
    args = parser.parse_args(argv)

    if args.write and not args.no_write:
        report = write_planted_qary_cdkm_adder_sparsity_bridge_report()
    else:
        report = build_planted_qary_cdkm_adder_sparsity_bridge_report()

    print(
        json.dumps(
            {
                "subsystem": report["subsystem"],
                "verification": report["verification"],
                "modulus_scaling_configs_checked": len(report["modulus_scaling_audit"]["records"]),
                "dimension_family_configs_checked": len(report["dimension_family_audit"]),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
