"""Conditional noisy native-source restoration, not a natural-source certificate.

Retain public visibility, discard higher parent labels, use independent fresh
batches. Pure |+> replacement does not preserve the noisy CQ source law.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
from itertools import product
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.dcp_adaptive_direction_rank_gate import dyadic, integer
from theorems.dcp_affine_packet_noise import MODEL, validate_visibilities
from theorems.dcp_disjoint_kernel_pairing import make_program, partner

REPORT = ROOT / "research/phase_workbench/dcp_noise_matched_source.json"
CONTRACT = ROOT / "research/hypotheses/dcp_noise_matched_source_contract.json"
CONTRACT_ID = "noise_matched_zero_label_conditional_native_source_restoration_v1"
PREMISES = {
    "original_noise_model": MODEL,
    "public_visibility_independent_of_fresh_higher_labels": True,
    "pair_selection_reads_only_coarse_labels": True,
    "original_diagonal_is_flat": True,
    "original_higher_label_transcript_discarded": True,
    "fresh_independent_batches_per_attempt": True,
    "joint_input_state_factors_conditioned_on_fixed_unknown_secret": True,
}


def require_premises(premises):
    if any(premises.get(k) != v or type(premises.get(k)) is not type(v) for k,v in PREMISES.items()):
        raise ValueError("UNRESOLVED: conditional native-source premise missing or contradicted")
    return dict(PREMISES)


def replacement_actions(visibility, output_phase_bits, components, *, premises):
    """Executable stochastic channel recipe, with no secret/state inverse.

    An actual backend must implement discard, prepare |+>, and the public Z
    coin. This returns exact instructions; it does not claim hardware execution.
    """
    require_premises(premises)
    visibility = validate_visibilities((visibility,))[0]
    integer(output_phase_bits,"output phase bits",1,4096)
    integer(components,"components",1,4096)
    if output_phase_bits*components > 1000000:
        raise ValueError("UNKNOWN: public coin precision cap")
    zero = Fraction(1,1 << (output_phase_bits*components))
    return {
        "visibility":dyadic(visibility),"zero_label_coin_probability":dyadic(zero),
        "keep_paid_nonzero_qubit_probability":dyadic(1-zero),
        "replacement_plus_probability_including_zero_coin":dyadic(zero*(1+visibility)/2),
        "replacement_minus_probability_including_zero_coin":dyadic(zero*(1-visibility)/2),
        "conditional_Z_flip_probability":dyadic((1-visibility)/2),
        "actions":["draw public zero coin", "keep nonzero qubit unless coin is zero",
                   "on zero: discard paid qubit, prepare plus, apply public Z coin, label zero"],
        "paid_qubit_consumed_before_zero_coin":True,
        "public_visibility_record_retained":True,
        "unknown_preparation_inverse_used":False,"hardware_backend_executed":False,
    }


def product_source_certificate(counts, modulus, base_visibility, *, premises):
    """Exact finite CQ certificate from raw (label, visibility-exponent) masses.

    Global higher-label independence is a theorem premise, not inferred from
    a finite histogram. This checks the finite consequence and rejects failures.
    """
    require_premises(premises)
    integer(modulus,"finite output modulus",2,16)
    if modulus & (modulus-1):
        raise ValueError("power-of-two output modulus required")
    base = validate_visibilities((base_visibility,))[0]
    if not counts or any(type(c) is not int or c <= 0 for c in counts.values()):
        raise ValueError("positive exact census multiplicities required")
    for (label,exponent) in counts:
        integer(label,"canonical finite label",0,modulus-1)
        integer(exponent,"original visibility exponent",1,128)
    total = sum(counts.values())
    tags = sorted({e for _,e in counts})
    for e in tags:
        if len({counts.get((label,e),0) for label in range(modulus)}) != 1:
            raise ValueError("UNRESOLVED: label and public visibility are correlated")
    nonzero_total = sum(c for (label,_),c in counts.items() if label)
    if Fraction(nonzero_total,total) != 1-Fraction(1,modulus):
        raise ArithmeticError("incorrect charged zero rejection")
    restored = Counter()
    input_rows = []
    for (label,e),c in sorted(counts.items()):
        if not label:
            continue
        conditional = Fraction(c,nonzero_total)
        input_rows.append({"label":label,"visibility_exponent":e,"conditional_probability":str(conditional)})
        restored[label,e] += conditional*(1-Fraction(1,modulus))
        restored[0,e] += conditional/Fraction(modulus)
    target = {(label,e):Fraction(c,total) for (label,e),c in counts.items()}
    if dict(restored) != target:
        raise ArithmeticError("matched visibility channel did not restore joint CQ masses")
    rows = [{"label":label,"visibility_exponent":e,"raw_count":counts[label,e],
             "target_probability":str(target[label,e]),"restored_probability":str(restored[label,e])}
            for label,e in sorted(target)]
    return {
        "output_modulus":modulus,"base_visibility":dyadic(base),"raw_census_total":total,
        "joint_label_visibility_rows":rows,"accepted_nonzero_input_rows":input_rows,
        "charged_nonzero_admission_probability":str(Fraction(nonzero_total,total)),
        "replacement_recipes_by_exponent":[{"visibility_exponent":e,
            "recipe":replacement_actions(base**e,modulus.bit_length()-1,1,premises=premises)} for e in tags],
        "exact_joint_label_visibility_law_restored":True,
        "pure_replacement_matches_noisy_zero_blocks":all(base**e==1 for e in tags),
        "original_higher_labels_retained":False,"source_theorem_inferred_from_finite_histogram":False,
    }


def first_level_census():
    coarse = ((1,1,1,1),)
    P = make_program(coarse)
    pairs = [(x,partner(P,x)) for x in range(16) if x<partner(P,x)]
    counts = Counter()
    for lifts in product(range(8),repeat=4):
        full = [1+4*z for z in lifts]
        for x,y in pairs:
            delta = sum(a*((y >> i & 1)-(x >> i & 1)) for i,a in enumerate(full))
            counts[delta//4 % 8,(x^y).bit_count()] += 1
    return counts


def second_level_census():
    """ALL first-level IID labels/tags; integer masses, not Monte Carlo."""
    counts = Counter()
    cache = {}
    for row in product(range(8),repeat=4):
        coarse = tuple(a%4 for a in row)
        if coarse not in cache:
            P = make_program((coarse,))
            cache[coarse] = [(x,partner(P,x)) for x in range(16) if x<partner(P,x)]
        for x,y in cache[coarse]:
            direction = x^y
            delta = sum(a*((y >> i & 1)-(x >> i & 1)) for i,a in enumerate(row))
            if delta%4:
                raise ArithmeticError("second-level original pair fails descent")
            for tags in product((2,4),repeat=4):
                exponent = sum(e for i,e in enumerate(tags) if direction >> i & 1)
                # First-level tag2 has probability3/4; tag4 probability1/4.
                multiplicity = 3**tags.count(2)
                counts[delta//4 % 2,exponent] += multiplicity
    return counts


def build_report():
    premises = dict(PREMISES)
    first = product_source_certificate(first_level_census(),8,Fraction(3,4),premises=premises)
    second = product_source_certificate(second_level_census(),2,Fraction(3,4),premises=premises)
    return {
        "contract_id":CONTRACT_ID,"status":"CONDITIONAL_LOCAL_DERIVATION_EXTERNAL_REVIEW_PENDING",
        "accepted_speedup_candidate":False,"novelty_claim":False,"actual_natural_source_noise_certified":False,
        "external_theorem_review_complete":False,"source_quantum_preparations_executed":0,
        "assumed_not_inferred_premises":premises,"two_level_exact_censuses":[first,second],
        "implemented_wrapper_supply":{
            "original_qubits_per_first_level_raw_attempt":4,
            "first_level_original_qubits_per_restored_output":"32/7",
            "first_level_outputs_per_second_level_restored_output":"8",
            "original_qubits_per_second_level_restored_output":"256/7",
            "ideal_no_failure_two_level_original_qubits":16,
            "these_costs_are_universal_lower_bounds":False,
            "zero_coin_is_drawn_only_after_a_paid_nonzero_output":True,
        },
        "scope":{
            "abstract_balanced_product_source_family_closed_under_this_channel":True,
            "induction_requires_fresh_independent_batches_and_label_visibility_independence":True,
            "all_joint_natural_lattice_noise_models_covered":False,
            "correlated_original_faults_covered_by_marginal_visibility":False,
            "old_full_higher_label_transcript_may_be_retained":False,
            "exponential_recursive_supply_or_visibility_loss_removed":False,
            "hardware_reset_or_Z_coin_backend_implemented":False,
        },
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-write",action="store_true")
    args = parser.parse_args(argv)
    report = build_report()
    if not args.no_write:
        REPORT.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"status":report["status"],"exact_levels":2,
                      "abstract_noisy_source_closed":True,"actual_natural_source_certified":False,
                      "artifact":str(REPORT)}))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
