"""Exact conservative schedule for the proposed class-four quotient-image call.

Arithmetic bounds only: no quantum execution, SDE implementation, source
validity certificate or speedup claim. See CLASS_FOUR_HSP_THEOREM_DRAFT.md.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import json
from math import comb
from pathlib import Path

from theorems.nil3_complete_budget import ceil_log
from theorems.prime_character_opi import ring


def general_quartic_arity(equations):
    """IS Theorem 11 + Section 3.3: G(4,e)^ceil(log2(5)), unrounded."""
    if type(equations) is not int or equations < 0:
        raise ValueError("nonnegative integer equation count required")
    collision_arity = 4**6 * (equations+1)**4
    return collision_arity**3


def quotient_image_budget(p, m, w, z, error=Fraction(1, 3)):
    """Count capped source queries, not total gates or the full arbitrary-H HSP.

    Dimensions alone do not certify a class-four group. The source/rank/
    covariance contracts and correctly implemented capped solvers are premises.
    """
    ring(p)
    if p <= 4 or any(type(n) is not int or n < 1 for n in (m, w, z)):
        raise ValueError("p>4 and positive m,w,z required; w=0 uses the scalar route")
    if not isinstance(error, Fraction) or not 0 < error < 1:
        raise ValueError("exact rational error in (0,1) required")
    D, L = w*(m+1), w*(m+2)
    v = m+D
    hW, hZ = w*comb(m+2, 2), z*comb(m+4, 4)
    P = 1+hW+hZ+hW*(hW+1)//2
    equations = {j: P*comb(v+j-1, j) for j in (1, 2, 3)}
    a1 = equations[1]+1
    a2 = (equations[2]+1)**2
    e3 = equations[3]
    a3 = e3+1 if p % 3 == 2 else (9*e3+1)*(3*e3+1)*(e3+1)
    a4 = (z+1)**2 if p % 4 == 3 else general_quartic_arity(z)
    blocks = 2*L+2
    slots = blocks*a4
    roots = v+ceil_log(p, 4/error)
    leaves = roots*a1*a2*a3
    scalar_merges = roots*(a1*a2+a1+1)
    label_cap = ceil_log(p**z, 100*slots)
    matrix_cap = ceil_log(4, 4*leaves/error)
    # Worst-case bounds for each independently restarted matrix attempt.
    attempt_failure = 3*Fraction(1, 100)+Fraction(1, p)
    failures = {
        "fourier_rank": Fraction(p**v-1, (p-1)*p**roots),
        "matrix_attempt_exhaustion": leaves*Fraction(1, 4)**matrix_cap,
        "scalar_sde_reserved": error/4,
        "joint_instrument_reserved": error/4,
    }
    if (attempt_failure >= Fraction(1, 4) or scalar_merges > leaves
            or any(value > error/4 for value in failures.values())):
        raise ArithmeticError("class-four schedule failed its error/count contract")
    return {
        "status": "conditional-resource-envelope-not-executed-algorithm",
        "p": p, "m": m, "w": w, "z": z,
        "ambient_dimension": m+w+z,
        "jet_dimension": D, "scalar_width": v,
        "base_parameter_counts": {"noncentral": hW, "central": hZ},
        "lifted_parameter_count": P,
        "homogeneous_equation_caps": {str(j): equations[j] for j in equations},
        "scalar_arities": {"linear": a1, "quadratic": a2, "cubic": a3},
        "quartic_relation_arity": a4,
        "quartic_arity_source": "square-root reduction" if p % 4 == 3 else "IS collision recurrence G(4,z)^3",
        "relation_blocks": blocks, "normal_source_slots_per_attempt": slots,
        "erased_fourier_roots": roots, "matrix_scalar_leaf_slots": leaves,
        "scalar_sde_merges": scalar_merges,
        "label_draw_cap_per_slot": label_cap, "matrix_attempt_cap_per_leaf": matrix_cap,
        "block_multiplier_draw_cap": ceil_log(2, 100*blocks),
        "alignment_method": "deterministic-symplectic-isometry-extension",
        "alignment_failure_bound": "0", "alignment_transvection_cap": 2*L,
        "minimum_carrier_qudits": L,
        "matrix_attempt_failure_bound": str(attempt_failure),
        "source_query_cap": leaves*matrix_cap*slots*label_cap,
        "target_error": str(error),
        "failure_terms": {key: str(value) for key, value in failures.items()},
        "failure_union_bound": str(sum(failures.values())),
        "quantum_execution": False, "source_correctness_certified": False,
        "full_hsp_cost_included": False, "speedup_claim_allowed": False,
        "excluded_costs": [
            "Optional black-box Lie-basis acquisition via known abelian HSP",
            "Initial and final known nil-2 HSP calls and their error budgets",
            "Class-three quotient-image completion",
            "Classical field/SDE/symbolic/alignment work and native gate synthesis",
            "Public chart conversion, subgroup/quotient lifts and oracle gate cost",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = {
        "scope": "analytic-envelopes-for-UT5-dimensions-not-quantum-runs",
        "examples": [quotient_image_budget(p, 4, 2, 4) for p in (7, 11, 13, 17)],
    }
    if args.write:
        path = Path(__file__).resolve().parents[1]/"research/reductions/class_four_complete_budget.json"
        path.write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({str(row["p"]): row["source_query_cap"] for row in report["examples"]}, indent=2))


if __name__ == "__main__":
    main()
