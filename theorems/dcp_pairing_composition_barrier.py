"""Two-level fresh pair-compression converse under independent original noise.

Not a general DHSP, correlated-noise, purification or retained-block no-go.
All source promises are explicit assumptions, not natural-source certificates.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import product
import json
from math import comb
from pathlib import Path

from theorems.dcp_adaptive_direction_rank_gate import dyadic, integer

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/dcp_pairing_composition_barrier.json"
CONTRACT = ROOT / "research/hypotheses/dcp_pairing_composition_barrier_contract.json"
PREMISES = {
    "original_noise": "independent-balanced-dephasing-with-visibility-at-most-1-minus-1-over-n",
    "fresh_IID_uniform_coarse_label_pools_before_selection": True,
    "flat_input_diagonal_at_each_pair_projection": True,
    "each_successful_outcome_retains_exactly_one_original_basis_pair": True,
    "retained_pair_channel_is_basis_isometry_with_balanced_phase_density": True,
    "no_intermediate_collective_purification_or_interference_between_pairs": True,
    "latent_error_flags_or_environment_access_supplied": False,
    "second_pool_labels_IID_uniform_given_retained_coarse_records_and_visibility_tags": True,
    "higher_parent_label_transcripts_discarded": True,
    "independent_fresh_batches_no_qubit_reuse": True,
    "all_first_level_attempts_including_failures_and_tag_selection_charged": True,
    "all_second_level_available_parents_included_in_pool_width": True,
    "only_final_phase_qubit_retained_as_secret_bearing_quantum_output": True,
    "all_retained_classical_records_secret_independent": True,
    "zero_replacement_preserves_visibility_not_pure_plus": True,
}


def require_premises(premises):
    if any(type(premises.get(k)) is not type(v) or premises.get(k) != v for k,v in PREMISES.items()):
        raise ValueError("UNKNOWN_OUTSIDE_PAIR_COMPRESSION_MODEL: an essential source/instrument premise is absent")
    return dict(PREMISES)


def short_threshold(n, pool_width):
    integer(n, "secret vector components", 2, 1 << 24)
    integer(pool_width, "complete paid pool width", 2, 1 << 128)
    log = (pool_width-1).bit_length()
    r = min(pool_width, (n+log-1)//log)
    return {"components": n, "pool_width_hex": hex(pool_width),
            "ceil_log2_pool_width": log, "long_mask_minimum_width": r,
            "short_means_weight_strictly_less_than": r,
            "native_short_endpoint_probability_upper": {"one_over_two_exponent": n},
            "counting_exponent_check": log*(r-1) <= n-1,
            "bound_is_pointwise_in_labels": False}


def exact_short_union(n, m, r):
    integer(n, "components", 1, 512)
    integer(m, "finite source width", 1, 4096)
    integer(r, "short/long threshold", 1, m+1)
    return min(Fraction(1), Fraction(sum(comb(m,w) for w in range(1,r)), 1 << (2*n)))


def two_level_bound(n, first_pool, second_pool, first_attempt_budget, final_attempt_budget=1, *, premises):
    require_premises(premises)
    first, second = short_threshold(n,first_pool), short_threshold(n,second_pool)
    integer(first_attempt_budget, "paid first-level raw attempt budget", second_pool)
    integer(final_attempt_budget, "independent final attempts", 1)
    r1, r2 = first["long_mask_minimum_width"], second["long_mask_minimum_width"]
    rare_bits = n-first_attempt_budget.bit_length()  # ceil log2(R+1) for integer R>=1.
    tail_bits = r1*r2//(n-1)
    signal_bits = max(0,min(rare_bits,tail_bits)-1)
    # Q*U/2 trace-distance hybrid; loosen Q to the next power of two.
    readout_bits = max(0,signal_bits-(final_attempt_budget-1).bit_length()+1)
    return {"components": n, "first_pool": first, "second_pool": second,
            "first_level_attempt_budget_hex": hex(first_attempt_budget),
            "final_attempt_budget_hex": hex(final_attempt_budget),
            "original_visibility_upper_exact_rational": str(1-Fraction(1,n)),
            "long_long_original_visibility_exponent_lower": r1*r2,
            "long_long_visibility_power_of_two_upper_exponent": tail_bits,
            "union_of_first_short_or_second_short_probability_bound": "min(1,(R+1)*2^(-n))",
            "unconditional_final_visibility_power_of_two_upper_exponent": signal_bits,
            "joint_output_distance_from_secret_independent_reference_power_of_two_upper_exponent": readout_bits,
            "any_uniform_secret_bit_guess_probability_upper": "min(1,1/2+2^(-readout_exponent))",
            "bound_uses_unconditional_Born_weight_not_free_postselection": True,
            "conditional_visibility_requires_dividing_by_paid_acceptance": True,
            "runtime_or_tree_merge_rule_restricted": False,
            "source_and_pair_output_architecture_restricted": True,
            "assumed_source_promises_not_inferred": dict(PREMISES),
            "actual_natural_source_noise_certified": False,
            "general_DHSP_or_retained_block_no_go": False}


def native_short_census(n,m,r):
    integer(n,"finite components",1,4)
    integer(m,"finite source width",1,8)
    integer(r,"short/long threshold",1,m+1)
    if 4**(n*m)*(1 << m) > 50000:
        raise ValueError("UNKNOWN: complete native short-endpoint census cap")
    masks = [u for u in range(1,1 << m) if u.bit_count() < r]
    events = degree = 0
    total = 4**(n*m)*(1 << m)
    for flat in product(range(4),repeat=n*m):
        A = [flat[l*m:(l+1)*m] for l in range(n)]
        for x in range(1 << m):
            count = sum(all(sum(a*(1-2*(x >> i & 1)) for i,a in enumerate(row) if u >> i & 1)%4 == 0 for row in A) for u in masks)
            degree += count
            events += bool(count)
    upper = Fraction(len(masks),4**n)
    if Fraction(degree,total) != upper or Fraction(events,total) > upper:
        raise ArithmeticError("native short-mask union argument contradicted")
    return {"components":n,"pool_width":m,"short_threshold":r,
            "all_native_label_assignments_and_basis_endpoints":total,
            "short_relation_endpoint_count":events,"sum_short_relation_degrees":degree,
            "short_endpoint_probability":dyadic(Fraction(events,total)),
            "expected_short_degree":dyadic(upper)}


def build_report():
    return {"contract_id":"two_level_fresh_pair_compression_noise_converse_v1",
            "status":"CONDITIONAL_LOCAL_DERIVATION_EXTERNAL_REVIEW_PENDING",
            "native_short_mask_censuses":[native_short_census(1,3,2),native_short_census(2,2,2),native_short_census(2,3,3)],
            "polynomial_budget_frontiers":[two_level_bound(n,n*n,n*n,n**8,n**4,premises=PREMISES)
                                           for n in (64,256,1024,4096,16384,65536,262144,1048576)],
            "scope_countermodels":{
                "pointwise_favorable_zero_coarse_column":{"components":2,"width":2,"full_labels":[[4,1],[0,1]],
                    "phase_bits":3,"short_pair_coverage_at_this_selected_matrix":"1",
                    "unconditional_native_short_union_bound":"1/8","contradicts_mean_bound":False},
                "all_or_none_correlated_original_dephasing":{"same_single_register_visibility":"1/2",
                    "four_bit_pair_visibility":"1/2","independent_four_bit_visibility":"1/16",
                    "covered_by_independent_original_noise_converse":False},
                "inverse_quadratic_original_noise":{"covered":False,"reason":"Visibility may be much larger than1-1/n"},
                "retained_correlated_phase_block":{"covered":False,"reason":"Outcome retains more than one original basis pair"}},
            "accepted_speedup_candidate":False,"new_active_negative_result_created":False,
            "novelty_claim":False,"external_theorem_review_complete":False,
            "source_quantum_preparations_executed":0,"actual_natural_source_noise_certified":False,
            "literature_context":["https://arxiv.org/abs/cs/0304005","https://arxiv.org/abs/quant-ph/0302112","https://arxiv.org/abs/1112.3333"]}


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-write",action="store_true")
    args=parser.parse_args(argv)
    report=build_report()
    if not args.no_write:
        REPORT.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"status":report["status"],"native_censuses":3,"frontiers":8,
                      "general_DHSP_no_go":False,"artifact":str(REPORT)}))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
