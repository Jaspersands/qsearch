"""Decisive test of nonlinear syndrome correction in the actual ternary filter.

Local derivation/review pending. No novelty, native DCP receiver or speedup claim.
The low-rank block sampler uses exact cyclotomic integer weights, not floating
quasiprobability rejection or postselection on nonzero output coordinates.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction
import hashlib
from itertools import product
import json
from pathlib import Path
import random
import sys

from flint import nmod_mat

from ternary_decoder_filter import _linear_erasure_data, audit_filter, exact, _index

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/reductions/ternary_syndrome_correction.json"


def dot(x,y):
    return sum(a*b for a,b in zip(x,y)) % 3


def canonical_rows(rows, width, name):
    rows = tuple(tuple(row) for row in rows)
    if any(len(row) != width or any(type(x) is not int or x not in (0,1,2) for x in row)
           for row in rows):
        raise ValueError(f"canonical rectangular F3 {name} required")
    return rows


@dataclass(frozen=True)
class SyndromeQuadratic:
    labels: tuple
    kernel_rows: tuple
    coefficients: tuple
    right_inverse: tuple | None = None

    def __post_init__(self):
        A,R = _linear_erasure_data(self.labels,self.right_inverse)
        n,m = len(A),len(A[0])
        H = canonical_rows(self.kernel_rows,m,"kernel rows")
        r = len(H)
        if r > m-n or (H and nmod_mat(H,3).rref()[1] != r):
            raise ValueError("independent kernel rows required; no redundant block coordinates")
        if any(dot(a,h) for a in A for h in H):
            raise ValueError("H A^T=0 required; correction must preserve shift covariance")
        C = canonical_rows(self.coefficients,r*(r+1)//2,"quadratic coefficients")
        if len(C) != n:
            raise ValueError("one quadratic coefficient vector per original secret coordinate required")
        for name,value in (("labels",A),("right_inverse",R),("kernel_rows",H),("coefficients",C)):
            object.__setattr__(self,name,value)

    def quadratic(self,x):
        if len(x) != len(self.kernel_rows) or any(type(v) is not int or v not in (0,1,2) for v in x):
            raise ValueError("canonical public syndrome coordinates required")
        monomials = tuple(x[i]*x[j] % 3 for i in range(len(x)) for j in range(i,len(x)))
        return tuple(dot(row,monomials) for row in self.coefficients)

    def decode(self,observation):
        b = tuple(observation)
        m,n = len(self.labels[0]),len(self.labels)
        if len(b) != m or any(type(v) is not int or v not in (0,1,2) for v in b):
            raise ValueError("canonical observation required; no hidden secret input")
        q = self.quadratic(tuple(dot(h,b) for h in self.kernel_rows))
        return tuple((sum(self.right_inverse[j][i]*b[j] for j in range(m))+q[i]) % 3
                     for i in range(n))

    def public_record(self):
        return {"labels": self.labels,"right_inverse": self.right_inverse,
                "kernel_rows": self.kernel_rows,"upper_triangle_quadratic_coefficients": self.coefficients,
                "syndrome_rank": len(self.kernel_rows),
                "program_construction_or_search_cost_is_free": False,
                "secret_or_true_witness_used": False,
                "full_reversible_gate_export_implemented": False,
                "arithmetic_evaluation_upper_order": "O(n*m+r*m+n*r^2) field operations"}


def _block_geometry(program,signs,cap):
    if not isinstance(program,SyndromeQuadratic):
        raise ValueError("typed public syndrome program required")
    r = len(program.kernel_rows)
    if type(cap) is not int or cap < 1 or r > cap.bit_length() or 3**r > cap:
        raise ValueError("UNKNOWN: exact block cap; growing rank is not proved simulable")
    e = tuple(signs)
    A,R,H = program.labels,program.right_inverse,program.kernel_rows
    if len(e) != len(A[0]) or any(type(v) is not int or v not in (1,2) for v in e):
        raise ValueError("explicit sign coins required")
    Ae = tuple(dot(a,e) for a in A)
    z = tuple(-x % 3 for x in Ae)
    base = tuple((a-dot(row,Ae)) % 3 for a,row in zip(e,R))
    coordinates = tuple(product(range(3),repeat=r))
    shifts = tuple(tuple(sum(u[i]*H[i][j] for i in range(r)) % 3 for j in range(len(e)))
                   for u in coordinates)
    occupied = []
    for u,shift in zip(coordinates,shifts):
        word = tuple((a+b) % 3 for a,b in zip(e,shift))
        if all(word):
            occupied.append((u,(-1)**sum(v == 2 for v in word)))
    N,B = len(coordinates),len(occupied)
    if not B:
        raise ArithmeticError("initial sign word must occupy its block")
    return e,z,base,coordinates,shifts,occupied,N,B


def conditional_block(program,signs,*,cap=243):
    """Exact conditional law, with a block drawn by an initial uniform sign word.

    Blocks are cosets of rowspan(H). Their measured residual-Fourier label is
    z=-A*e. This z is a paid classical coin-derived quantity, not hidden advice.
    """
    e,z,base,coordinates,shifts,occupied,N,B = _block_geometry(program,signs,cap)
    # Exact Z[omega_3] DFT: retain three integer coefficient counts until the
    # final norm a^2-a*b+b^2. No floating clipping or probability renormalization.
    transformed = []
    for x in coordinates:
        counts = [0,0,0]
        for u,sign in occupied:
            counts[-dot(u,x) % 3] += sign
        transformed.append(counts)
    phases = tuple(-dot(z,program.quadratic(x)) % 3 for x in coordinates)
    outcomes = []
    for v,shift in zip(coordinates,shifts):
        counts = [0,0,0]
        for x,values,phase in zip(coordinates,transformed,phases):
            rotation = (dot(v,x)+phase) % 3
            for i,value in enumerate(values):
                counts[(i+rotation) % 3] += value
        a,b = counts[0]-counts[2],counts[1]-counts[2]
        weight = a*a-a*b+b*b
        word = tuple((x+y) % 3 for x,y in zip(base,shift))
        if any(dot(row,word) for row in program.labels):
            raise ArithmeticError("correction left the true nullspace")
        outcomes.append({"word": word,"integer_weight": weight})
    denominator = N*N*B
    if sum(row["integer_weight"] for row in outcomes) != denominator:
        raise ArithmeticError("exact block unitary lost mass; do not renormalize")
    return {"outcomes": outcomes,"weight_denominator": denominator,
            "block_size": N,"occupied_sign_vertices": B,
            "original_sign_coins": len(e),"computed_residual_Fourier_label": z,
            "all_failures_and_zero_coordinates_retained": True}


def twirled_conditional_block(program,signs,*,cap=243):
    """Exact average over IID uniform homogeneous-quadratic coefficients.

    Nonzero z pinches the syndrome Fourier indices to x=y or x=-y. This is
    a coefficient-average calculation, NOT a bound on each optimized program.
    """
    e,z,base,coordinates,shifts,occupied,N,B = _block_geometry(program,signs,cap)
    amplitudes = dict(occupied)
    S = sum(amplitudes.values())
    denominator = N*N*B if any(z) else B
    outcomes = []
    for v,shift in zip(coordinates,shifts):
        if any(z):
            reflection = sum(sign*amplitudes.get(tuple((2*a-b) % 3 for a,b in zip(v,u)),0)
                             for u,sign in occupied)
            weight = N*B+N*reflection-S*S
        else:
            weight = int(v in amplitudes)
        if weight < 0 or (any(z) and weight > 2*N*B):
            raise ArithmeticError("invalid exact quadratic twirl weight")
        outcomes.append({"word": tuple((x+y) % 3 for x,y in zip(base,shift)),
                         "integer_weight": weight})
    if sum(row["integer_weight"] for row in outcomes) != denominator:
        raise ArithmeticError("twirled block lost mass")
    return {"outcomes": outcomes,"weight_denominator": denominator,
            "nonzero_residual_frequency": any(z),"block_size": N}


def sample_classical(program,*,rng=None,cap=243):
    """Exact random-bit sampler, polynomial for r=O(log(n+m)) with paid evaluation."""
    if not isinstance(program,SyndromeQuadratic):
        raise ValueError("typed public syndrome program required")
    rng = random.SystemRandom() if rng is None else rng
    signs = tuple(1+rng.randrange(2) for _ in program.labels[0])
    block = conditional_block(program,signs,cap=cap)
    draw = rng.randrange(block["weight_denominator"])
    for row in block["outcomes"]:
        draw -= row["integer_weight"]
        if draw < 0:
            return {"word": row["word"],"valid_all_nonzero_signed_witness": all(row["word"]),
                    "source_sign_bits_charged": len(signs),
                    "integer_categorical_draw_bound": block["weight_denominator"],
                    "block_size_charged": block["block_size"],
                    "postselection_on_valid_signed_witness": False}
    raise ArithmeticError("exact categorical draw exhausted its mass")


def complete_classical_reference(program,*,sign_cap=256,block_cap=243,average_random_quadratic=False):
    """Exponential small-source census, NOT the efficient sampler's algorithm."""
    m = len(program.labels[0])
    if type(sign_cap) is not int or sign_cap < 1 or m > sign_cap.bit_length() or 2**m > sign_cap:
        raise ValueError("UNKNOWN: complete sign census cap, not a sampler lower bound")
    distribution = defaultdict(Fraction)
    for signs in product((1,2),repeat=m):
        block = (twirled_conditional_block if average_random_quadratic else conditional_block)(program,signs,cap=block_cap)
        for row in block["outcomes"]:
            distribution[row["word"]] += Fraction(row["integer_weight"],block["weight_denominator"]*2**m)
    if sum(distribution.values()) != 1:
        raise ArithmeticError("complete reference lost mass")
    return dict(distribution)


def random_full_syndrome_success_bound(n,m,attempt_budget=1):
    """Full-rank H and random Q: exponential SOURCE-AVERAGE success upper bound.

    R,H may depend on A but must be chosen before IID uniform Q coefficients.
    attempt_budget pays (#candidate draws)*(maximum repetitions of a selected
    candidate), even if an oracle selects the best sampled candidate. Actual
    receiver calls alone do not pay for an adaptive public program search.
    Arbitrarily optimized/structured coefficients are NOT covered.
    """
    if (type(n) is not int or type(m) is not int or not 1 <= n <= m
            or type(attempt_budget) is not int or attempt_budget < 1):
        raise ValueError("1<=n<=m and positive integer paid attempt budget required")
    raw = Fraction(1,3**n)+2*Fraction(2,3)**m
    # Union over the (3^n-1)/2 projective left-kernel vectors bounds rank loss.
    rank_failure = Fraction(3**n-1,2*3**m)
    conditional = min(Fraction(1),2*attempt_budget*raw)
    unconditional = min(Fraction(1),attempt_budget*raw+rank_failure)
    exponent = (unconditional.denominator//unconditional.numerator).bit_length()-1
    return {"dimension": n,"columns": m,"syndrome_rank": m-n,
            "paid_program_draw_times_repetition_budget": attempt_budget,
            "conditional_full_row_rank_source_success_upper": exact(conditional),
            "unconditional_IID_source_success_upper_including_arbitrary_rank_failure_fallback": exact(unconditional),
            "unconditional_success_at_most_two_to_minus": exponent,
            "rank_failure_upper": exact(rank_failure),
            "uniform_Q_coefficients_chosen_after_public_R_and_H": True,
            "arbitrary_optimized_or_structured_Q_covered": False,
            "coherent_repetitions_or_amplitude_amplification_covered": False,
            "large_quantum_circuit_executed": False,
            "classical_hardness_or_general_quantum_no_go": False}


def physical_comparison(program):
    row = audit_filter(program.labels,decoder_mode="quadratic-syndrome",
                       syndrome_correction=program,include_table=True)
    distribution = complete_classical_reference(program)
    probabilities = row["actual_quantum_word_probabilities"]
    residual = max(abs(probabilities[_index(word)]-float(distribution.get(word,0)))
                   for word in product(range(3),repeat=len(program.labels[0])))
    if residual > 1e-12:
        raise ArithmeticError("nonlinear physical filter is NOT matched by the block sampler")
    linear = SyndromeQuadratic(program.labels,(),tuple(() for _ in program.labels),program.right_inverse)
    baseline = complete_classical_reference(linear)
    success = sum((p for word,p in distribution.items() if all(word)),Fraction())
    linear_success = sum((p for word,p in baseline.items() if all(word)),Fraction())
    return {"actual_quantum_control": row,"exact_classical_output_distribution": [
                {"word": word,"probability": exact(p)} for word,p in sorted(distribution.items()) if p],
            "exact_classical_signed_success": exact(success),
            "linear_free_sign_baseline_success": exact(linear_success),
            "actual_full_output_max_error": residual,
            "finite_gain_over_linear_baseline": exact(success-linear_success),
            "quantum_advantage_from_this_gain": False}


def canonical_kernel_rows(labels):
    """Public systematic nullspace basis, with O(m^2*n) arithmetic/storage paid."""
    A,R = _linear_erasure_data(labels)
    m = len(A[0])
    free = [j for j,row in enumerate(R) if not any(row)]
    return tuple(tuple((int(k == j)-sum(R[k][i]*A[i][j] for i in range(len(A)))) % 3
                       for k in range(m)) for j in free)


def fixed_cross_correction(labels):
    """One prespecified public rule, not optimization using a planted witness."""
    H = canonical_kernel_rows(labels)[:2]
    if len(H) != 2:
        raise ValueError("two kernel coordinates required by this particular rule")
    return SyndromeQuadratic(labels,H,((0,1,0),)+((0,0,0),)*(len(labels)-1))


def complete_one_row_source_census():
    """All IID one-row width3 labels, including the rank-deficient zero source."""
    cases = []
    mean,linear_mean = Fraction(),Fraction()
    for a in product(range(3),repeat=3):
        if any(a):
            comparison = physical_comparison(fixed_cross_correction((a,)))
            def fraction(item):
                return Fraction(item["numerator"],item["denominator"])
            success = fraction(comparison["exact_classical_signed_success"])
            baseline = fraction(comparison["linear_free_sign_baseline_success"])
            residual = comparison["actual_full_output_max_error"]
        else:
            control = audit_filter((a,),decoder_mode="constant-zero")
            success,baseline = Fraction(1),Fraction(1)
            residual = abs(control["executed_valid_signed_zero_sum_probability"]-1)
            if residual > 1e-12:
                raise ArithmeticError("rank-zero source fallback failed")
        mean += success/27
        linear_mean += baseline/27
        cases.append({"labels": (a,),"rank_zero_classical_fallback": not any(a),
                      "unconditional_success": exact(success),"linear_success": exact(baseline),
                      "actual_quantum_comparison_error": residual})
    return {"all_IID_label_matrices": 27,"all_source_cases": cases,
            "mean_success": exact(mean),"linear_mean_success": exact(linear_mean),
            "favorable_source_selection": False,"large_rank_success_proved": False}


def run_controls():
    programs = (
        SyndromeQuadratic(((1,1,1),),((1,2,0),),((1,),)),
        SyndromeQuadratic(((1,1,1),),((1,2,0),(1,0,2)),((1,1,2),)),
        SyndromeQuadratic(((1,1,1),),((1,2,0),(1,0,2)),((0,1,0),)),
        SyndromeQuadratic(((1,0,1,2),(0,1,2,2)),((2,1,1,0),),((1,),(2,))),
    )
    controls = [physical_comparison(program) for program in programs]
    policies = []
    for C in product(range(3),repeat=3):
        program = SyndromeQuadratic(((1,1,1),),((1,2,0),(1,0,2)),(C,))
        distribution = complete_classical_reference(program)
        success = sum((p for word,p in distribution.items() if all(word)),Fraction())
        policies.append({"public_coefficients": C,"success": exact(success)})
    return {"status": "NONLINEAR_SYNDROME_CORRECTION_WITH_EXACT_LOW_RANK_CLASSICAL_SAMPLER",
            "proof_status": "LOCAL_DERIVATION_REVIEW_PENDING",
            "controls": controls,"classical_per_sample_upper_order": "O(poly(n,m,r)*9^r)",
            "complete_one_row_IID_source_census": complete_one_row_source_census(),
            "all_27_quadratic_policies_on_one_easy_control": policies,
            "random_full_syndrome_quadratic_source_bounds": [
                random_full_syndrome_success_bound(n,m,budget)
                for n in (16,32,64,128) for m in (2*n,4*n) for budget in (1,n*n)],
            "easy_control_has_deterministic_classical_signed_witness": (1,1,1),
            "quadratic_policy_optimization_is_free_or_scalable": False,
            "all_growing_rank_quadratic_filters_dequantized": False,
            "published_nonlinear_quotient_decoder_dequantized": False,
            "rank_or_nonstabilizer_input_alone_establishes_quantum_advantage": False,
            "coherent_output_channel_simulated_by_classical_word_sampler": False,
            "accepted_speedup_candidate": False,"new_active_negative_result_created": False,
            "novelty_claim": False,
            "dependency_sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                                  for p in (Path(__file__),ROOT/"theorems/ternary_decoder_filter.py",
                                            ROOT/"theorems/ternary_quotient_decoder.py")}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write",action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.write:
        REPORT.write_text(json.dumps(report,indent=2,allow_nan=False)+"\n")
    print(json.dumps({"status": report["status"],"controls": len(report["controls"]),
                      "gains": [c["finite_gain_over_linear_baseline"] for c in report["controls"]],
                      "accepted_speedup_candidate": False}))


if __name__ == "__main__":
    sys.modules["ternary_syndrome_correction"] = sys.modules[__name__]
    main()
