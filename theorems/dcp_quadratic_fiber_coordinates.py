"""Exact Clifford compression and structured quadratic coordinates for mod4 fibers.

Only measured linear constraints are cleared. The remaining quadratic fiber,
higher phases and correlated noise are preserved; no compact fiber inverse.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.dcp_adaptive_direction_rank_gate import integer
from theorems.dcp_affine_fiber_rigidity import matrix
from theorems.dcp_correlated_phase_block import density
from theorems.dcp_nonlinear_fiber_pairing import phase_value

REPORT = ROOT / "research/phase_workbench/dcp_quadratic_fiber_coordinates.json"


def coordinate_plan(labels, phase_bits, syndrome, *, coarse_bits=2):
    A = matrix(labels)
    n,m = len(A),len(A[0])
    integer(phase_bits,"original phase bits",3,4096)
    integer(coarse_bits,"actually measured coarse bits",1,2)
    if n*m > 100000 or m > 1024:
        raise ValueError("UNKNOWN: explicit quadratic-coordinate export cap")
    if any(a >= 1 << phase_bits for row in A for a in row):
        raise ValueError("canonical full original labels required")
    y = tuple(syndrome)
    if len(y) != n:
        raise ValueError("one mod4 measured syndrome per row required")
    for s in y:
        integer(s,"actually measured coarse syndrome",0,(1 << coarse_bits)-1)
    low = [sum((a&1) << i for i,a in enumerate(row)) for row in A]
    high = [sum(((a >> 1)&1) << i for i,a in enumerate(row)) for row in A]
    rows = [b | ((s&1) << m) for b,s in zip(low,y)]
    pivots = []
    for p in range(m):
        selected = next((i for i in range(len(pivots),n) if rows[i] >> p & 1),None)
        if selected is None:
            continue
        r = len(pivots)
        rows[r],rows[selected] = rows[selected],rows[r]
        for i in range(n):
            if i != r and rows[i] >> p & 1:
                rows[i] ^= rows[r]
        pivots.append(p)
    if any((row & ((1 << m)-1)) == 0 and row >> m for row in rows):
        raise ValueError("inconsistent measured low syndrome")
    free = [i for i in range(m) if i not in pivots]
    k = len(free)
    if coarse_bits==2 and n*k*k > 2000000:
        raise ValueError("UNKNOWN: explicit quadratic coefficient cap")
    x0 = sum(((rows[r] >> m)&1) << p for r,p in enumerate(pivots))
    V = [(1 << f) | sum(((rows[r] >> f)&1) << p for r,p in enumerate(pivots)) for f in free]
    gates = []
    for r,p in enumerate(pivots):
        gates.extend([["CX",f,p] for f in free if rows[r] >> f & 1])
        if rows[r] >> m & 1:
            gates.append(["X",p])
    equations = []
    for b,c,s in zip(low,high,y) if coarse_bits==2 else ():
        def high_bit(x):
            return ((c&x).bit_count()+((b&x).bit_count()//2))&1
        offset = high_bit(x0)
        linear = [j for j,v in enumerate(V) if high_bit(x0^v)^offset]
        # B*V=0 eliminates the outer-product term in the carry Hessian.
        pairs = [[i,j] for i in range(k) for j in range(i+1,k)
                 if (b&V[i]&V[j]).bit_count()%2]
        equations.append({"constant": offset ^ (s >> 1), "linear_variables": linear,
                          "quadratic_pairs": pairs, "equation_rhs": 0})
    return {"full_labels": [list(r) for r in A], "original_phase_bits": phase_bits,
            "actually_measured_coarse_bits_per_component":coarse_bits,
            "higher_syndrome_constraints_not_measured_or_imposed":coarse_bits==1,
            "complete_measured_parity_fiber_affine_index_compiled":coarse_bits==1,
            "measured_syndrome": list(y), "original_phase_wires": m,
            "binary_low_syndrome_rank": len(pivots), "cleared_pivot_wires": pivots,
            "retained_free_wires": free, "retained_quantum_wires": k,
            "affine_origin_hex": hex(x0), "kernel_direction_hex": [hex(v) for v in V],
            "Clifford_gates_after_measured_syndrome": gates, "extra_zero_work_qubits": 0,
            "quadratic_high_syndrome_equations": equations,
            "full_fiber_enumeration_used_by_compiler": False,
            "remaining_quadratic_fiber_inverse_supplied": False,
            "higher_phase_linearity_in_free_bits_assumed": False,
            "fresh_independent_phase_qubits_supplied": False,
            "original_independent_Z_noise_may_be_correlated_in_free_coordinates": True,
            "noise_kernel": "v^popcount(XOR_j ((u_j XOR u'_j)*V_j))",
            "noise_kernel_formula_requires_original_independent_Z_faults": True,
            "unitary_coordinate_change_increases_information": False,
            "hardware_transpilation_or_execution_performed": False}


def lift_free_word(plan,u):
    integer(u,"free coordinate word",0,(1 << plan["retained_quantum_wires"])-1)
    x = int(plan["affine_origin_hex"],16)
    for i,v in enumerate(plan["kernel_direction_hex"]):
        if u >> i & 1:
            x ^= int(v,16)
    return x


def satisfies_quadratics(plan,u):
    integer(u,"free coordinate word",0,(1 << plan["retained_quantum_wires"])-1)
    return all((e["constant"] + sum(u >> j & 1 for j in e["linear_variables"])
                + sum((u >> i & 1)*(u >> j & 1) for i,j in e["quadratic_pairs"])) % 2 == 0
               for e in plan["quadratic_high_syndrome_equations"])


def noise_overlap(plan,u,v,visibility):
    rate = Fraction(visibility)
    if not 0 <= rate <= 1:
        raise ValueError("visibility must lie in [0,1]")
    return rate**((lift_free_word(plan,u)^lift_free_word(plan,v)).bit_count())


def finite_density_control(labels,t,y,secret,visibility):
    plan = coordinate_plan(labels,t,y)
    m,k = plan["original_phase_wires"],plan["retained_quantum_wires"]
    if m > 8:
        raise ValueError("UNKNOWN: finite source-density replay cap")
    allowed = [u for u in range(1 << k) if satisfies_quadratics(plan,u)]
    if not allowed:
        raise ValueError("zero-probability full syndrome")
    original = [lift_free_word(plan,u) for u in allowed]
    rho = density(labels,t,secret,visibility)[np.ix_(original,original)]*(1 << m)/len(allowed)
    fs = [phase_value(labels,x,1 << t) for x in original]
    phases = [np.exp(2j*np.pi*sum(a*b for a,b in zip(f,secret))/(1 << t)) for f in fs]
    expected = np.array([[a*b.conjugate()*float(noise_overlap(plan,u,v,visibility))/len(allowed)
                          for b,v in zip(phases,allowed)] for a,u in zip(phases,allowed)])
    residual = float(np.max(np.abs(rho-expected)))
    if residual > 1e-11 or abs(np.trace(rho)-1) > 1e-11:
        raise ArithmeticError("compressed phase/noise law disagrees with original density")
    return {"plan": plan, "visibility_exact": str(Fraction(visibility)),
            "secret_used_only_for_bounded_density_calibration": list(secret),
            "allowed_free_words": allowed, "original_fiber_assignments": original,
            "full_Born_syndrome_probability_exact": str(Fraction(len(allowed),1 << m)),
            "max_original_density_residual": residual,
            "actual_same_packet_noise_overlap_matrix_exact": [[str(noise_overlap(plan,u,v,visibility)) for v in allowed] for u in allowed],
            "independent_noise_oracle_or_state_inverse_supplied": False,
            "quadratic_equations_solved_only_by_bounded_control_enumeration": True}


def build_report():
    return {"status": "EXACT_CLIFFORD_COORDINATES_QUADRATIC_FIBER_DECODING_OPEN",
            "finite_controls": [finite_density_control(A,t,y,s,v) for A,t,y,s,v in (
                (((1,5,9),),4,(1,),(1,),Fraction(3,4)),
                (((1,0,5,1),(0,1,1,2)),4,(1,1),(1,2),Fraction(7,8)),
                (((2,0,2),(0,2,2)),4,(2,0),(1,1),Fraction(1,2)))],
            "rank_failure_bounds_at_width_3n": [{"components": n,
                "binary_rank_less_than_n_probability_power_of_two_upper_exponent": 2*n,
                "retained_free_wires_IF_full_rank": 2*n,
                "CNOT_gate_count_upper": 2*n*n, "X_gate_count_upper": n}
                for n in (8,32,128,512)],
            "compiles_the_actual_mod4_fiber_not_arbitrary_MQ": True,
            "coherent_remaining_fiber_enumeration_or_inverse": False,
            "source_noise_becomes_independent_after_compression": False,
            "accepted_speedup_candidate": False, "new_active_negative_result_created": False,
            "novelty_claim": False, "actual_natural_source_noise_certified": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write",action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write:
        REPORT.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"status": report["status"], "finite_controls": len(report["finite_controls"]),
                      "remaining_fiber_decoder": False}))


if __name__ == "__main__":
    main()
