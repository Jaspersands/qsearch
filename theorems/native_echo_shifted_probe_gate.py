"""Exact shifted-probe Gram and weak-trit gate for one partial phase echo.

LOCAL DERIVATION / REVIEW PENDING. Even native IID pairs and a bounded menu
of A-independent lenses only. Full-A calibration is an explicit escape.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import product
import json
from pathlib import Path

from ternary_covariant_noise import _integer, _word, root_digits

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"research/classical_baselines/native_echo_shifted_probe_gate.json"
E=((0,0),(1,0),(0,1))


def minus(a,b):
    return tuple(x-y for x,y in zip(a,b))


def determinant(a,b):
    return a[0]*b[1]-a[1]*b[0]


def quartet_classes():
    classes=[]
    for j,k,l,m in product(range(3),repeat=4):
        r,p=minus(E[j],E[k]),minus(E[l],E[m])
        record={"indices":(j,k,l,m)}
        if (k-j+l-m) % 3:
            record["class"]="cancelled_by_measured_word_Fourier_character"
        elif r==(0,0) and p==(0,0):
            record["class"]="secret_independent_diagonal_background"
        elif r==p:
            record["class"]="equal_secrets_only_same_ordered_simplex_root"
        else:
            d=determinant(r,p)
            if d not in (-1,1):
                raise ArithmeticError("nonparallel surviving native roots do not have a unit determinant")
            ca,cb=minus(E[j],E[l]),tuple(-x for x in minus(E[k],E[m]))
            s=tuple(-determinant(c,p)//d for c in (ca,cb))
            t=tuple(determinant(r,c)//d for c in (ca,cb))
            if {s,t}!={(-1,0),(0,-1)}:
                raise ArithmeticError("shifted-probe off-diagonal exceptions leave the two tested secret guesses")
            record.update({"class":"only_the_two_public_shift_exceptions","unit_root_determinant":d,
                           "exceptional_first_secret_coefficients":s,"exceptional_second_secret_coefficients":t})
        classes.append(record)
    return classes


def cross_probe_moment(q,left,right,s,t):
    """Exact <X_s,X_t> for one A copy, zero settings; generic proof arbitrary settings."""
    root_digits(q)
    n=len(left)
    left,right,s,t=tuple(_word(x,q,"shifted-probe vector",n) for x in (left,right,s,t))
    count=0
    for j,k,l,m in product(range(3),repeat=4):
        if (k-j+l-m) % 3:
            continue
        if all(all(((a+d)*E[j][c]-(a+e)*E[k][c]-(b+d)*E[l][c]+(b+e)*E[m][c]) % q == 0
                   for c in range(2)) for a,b,d,e in zip(s,t,left,right)):
            count+=1
    return Fraction(count,9)


def exact_gram_control(q,left,right,copies):
    _integer(copies,"A source copies",1)
    n=len(left)
    secrets=tuple(product(range(q),repeat=n))
    if len(secrets)>81:
        raise ValueError("complete shifted-probe Gram reference exceeds81 secrets")
    exceptions={tuple(-x % q for x in shift) for shift in (left,right)}
    good=tuple(s for s in secrets if s not in exceptions)
    background=Fraction(1 if left==right else 1,1 if left==right else 3)**copies
    rows=[]
    for s in good:
        row=[]
        for t in good:
            value=cross_probe_moment(q,left,right,s,t)**copies-background
            expected=(Fraction(5,3)**copies-1 if left==right else 1-Fraction(1,3)**copies) if s==t else Fraction()
            if value!=expected:
                raise ArithmeticError("the centered shifted-probe family is not exactly orthogonal away from public guesses")
            row.append(str(value))
        rows.append(row)
    return {"modulus":q,"secret_dimension":n,"left_public_shift":left,"right_public_shift":right,
            "A_source_copies":copies,"all_nonexceptional_secrets":good,
            "secret_independent_background_squared_norm":str(background),
            "full_centered_probe_Gram_exact_rationals":rows,
            "exceptional_secrets":sorted(exceptions),"arbitrary_fixed_public_A_phase_settings_also_covered":True}


def full_A_inverse_calibration_countercontrol(q=9):
    """Exact growing-root off-diagonal Gram, retaining every original row."""
    root_digits(q)
    if not 9<=q<=81:
        raise ValueError("complete calibrated countercontrol requires q9,q27 or q81")
    coefficients=[0]*q
    unit_coefficients=[0]*q
    nonunit_coefficients=[0]*q
    for a,c,z in product(range(q),range(q),range(3)):
        delta=pow(a,-1,q) if a % 3 else 0
        values=(0,a,c)
        probes=[]
        for s in (q//3,2*q//3):
            numerator=[0]*q
            for j,k in product(range(3),repeat=2):
                exponent=(s*values[j]-(s+delta)*values[k]-(q//3)*z*(j-k)) % q
                numerator[exponent]+=1
            for v in values:
                numerator[(-delta*v) % q]-=1
            probes.append(numerator)
        left=tuple((i,value) for i,value in enumerate(probes[0]) if value)
        right=tuple((i,value) for i,value in enumerate(probes[1]) if value)
        for (i,x),(j,y) in product(left,right):
            coefficients[(i-j) % q]+=x*y
            (unit_coefficients if a % 3 else nonunit_coefficients)[(i-j) % q]+=x*y
    def rational_mean(histogram,denominator):
        degree=2*q//3
        reduced=histogram[:degree]
        for i in range(degree,q):
            reduced[i-degree]-=histogram[i]
            reduced[i-q//3]-=histogram[i]
        if any(reduced[1:]):
            raise ArithmeticError("adaptive Gram countercontrol is not a rational scalar")
        return Fraction(reduced[0],denominator)
    value=rational_mean(coefficients,27*q*q)
    unit=rational_mean(unit_coefficients,18*q*q)
    nonunit=rational_mean(nonunit_coefficients,9*q*q)
    if (value,unit,nonunit)!=(Fraction(4,27),Fraction(-1,9),Fraction(2,3)):
        raise ArithmeticError("the full-label calibration escape no longer has its exact off-diagonal witness")
    return {"modulus":q,"A_source_copies":1,"left_shift":0,
            "right_shift_rule":f"inverse(a) modulo{q} if a is a unit, otherwise0",
            "two_nonexceptional_secrets":[q//3,2*q//3],"complete_IID_label_outcome_records":3*q*q,
            "rank_failures_retained":True,"source_labels_rejected":False,
            "root_off_diagonal_numerator_coefficients_ascending":coefficients,
            "exact_nonzero_centered_Gram_entry":str(value),
            "conditional_unit_A_Gram_entry":str(unit),
            "conditional_nonunit_A_zero_fallback_Gram_entry":str(nonunit),
            "A_independent_orthogonality_extension_is_false":True,
            "positive_receiver_or_decoder_follows":False}


def weak_trit_ledger(n,r,copies,mediator_width,policy_count=1):
    for x,name,minimum in ((n,"secret dimension",1),(r,"root digits",1),(copies,"original source copies",2),
                           (mediator_width,"mediator width",1),(policy_count,"precommitted policy count",1)):
        _integer(x,name,minimum)
    if mediator_width>=copies:
        raise ValueError("a nonempty A block is required")
    if mediator_width>512:
        raise ValueError("expanded polynomial-menu coefficient ledger capped at512 mediator trits")
    N=n*r
    W=3**mediator_width
    surplus=copies-N
    return {"secret_dimension":n,"root_digits":r,"original_even_native_level":2*r,
            "original_source_copies":copies,"A_source_copies":copies-mediator_width,
            "mediator_width":mediator_width,"mediator_basis_size":W,
            "precommitted_A_independent_policy_count":policy_count,
            "least_trit_mean_advantage_upper_bound":{
                "cap":"2/3","rare_background_and_public_guess_mass":{"numerator":W*(W-1)+policy_count*W,"denominator":{"base":3,"exponent":N}},
                "centered_probe_term":{"coefficient_squared":policy_count*W*W,
                                       "Gram_variance_bound":{"base":"5/3","exponent":copies-mediator_width,"subtract":1},
                                       "denominator":{"coefficient":2,"base":3,"exponent":N},"outer_operation":"square_root"}},
            "directed_rational_majorant":{
                "cap":"2/3","rare_term_numerator":W*(W-1)+policy_count*W,"rare_term_denominator":{"base":3,"exponent":N},
                "decay_term_coefficient":policy_count*W,"surplus_factor":{"base":"5/3","exponent":(max(surplus,0)+1)//2},
                "exponential_decay":{"base":"3/4","exponent":N}},
            "fixed_menu_selection_using_full_A_labels_covered":True,
            "coupling_values_depending_on_full_A_labels_OUTSIDE_fixed_menu_covered":False,
            "public_couplings_may_use_full_B_labels":True,
            "classical_unknown_secret_postprocessing_unlimited_in_bound":True,
            "wide_mediator_or_large_copy_surplus_ruled_out":False,
            "multiple_interleaved_echo_rounds_ruled_out":False,
            "arbitrary_orbit_coupling_receivers_ruled_out":False}


def run_controls():
    return {"status":"NATIVE_ONE_ECHO_SHIFTED_PROBE_WEAK_TRIT_GATE_REVIEW_PENDING",
            "complete_single_copy_character_quartets":quartet_classes(),
            "exact_centered_Gram_controls":[exact_gram_control(9,(2,),(7,),m) for m in (1,3)]+
                [exact_gram_control(9,(2,),(2,),3),exact_gram_control(3,(1,0),(2,1),2),exact_gram_control(27,(5,),(18,),2)],
            "full_A_inverse_calibration_countercontrol":full_A_inverse_calibration_countercontrol(),
            "growing_root_inverse_calibration_countercontrols":[full_A_inverse_calibration_countercontrol(q) for q in (27,81)],
            "growing_root_adaptive_escape_derivation":{
                "root_digits_minimum":2,"conditional_unit_A_Gram_entry":"-1/9",
                "conditional_nonunit_A_zero_fallback_Gram_entry":"2/3",
                "unit_A_probability":"2/3","nonunit_A_probability":"1/3",
                "unconditional_Gram_entry":"4/27","external_derivation_review_pending":True},
            "growing_weak_trit_ledgers":[weak_trit_ledger(n,r,n*r+2,w,4) for n,r,w in ((1,2,1),(8,8,3),(32,32,6),(128,128,8))],
            "one_echo_with_logarithmic_mediator_and_near_entropy_copies_has_exponentially_small_population_advantage":True,
            "full_A_frequency_inverse_calibration_is_covered":False,
            "large_copy_surplus_or_wide_mediators_ruled_out":False,
            "general_native_weak_learner_ruled_out":False,"novelty_claimed":False}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--write",action="store_true")
    args=p.parse_args()
    out=run_controls()
    if args.write:
        REPORT.write_text(json.dumps(out,indent=2,allow_nan=False)+"\n")
    print(json.dumps({"status":out["status"],"exact_Gram_controls":len(out["exact_centered_Gram_controls"])}))


if __name__=="__main__":
    main()
