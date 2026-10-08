"""Scalable affine-erasure ceiling, with named minimum-error benchmarks.

Exact marginal duals close collective flat-affine erasure improvements on
product pure-state channels. Neither Holevo nor Helstrom rates construct an
efficient decoder or establish a computational quantum speedup.
"""
from __future__ import annotations

import argparse
import hashlib
from itertools import combinations, product
import json
import math
from pathlib import Path

from flint import fmpq, nmod_mat

from native_gaussian_bank_robustness import logarithm_box
from ternary_certified_noise_sampler import rational, sqrt_box
from ternary_measured_lattice_decoder import exact_json, integer
from linear_erasure_prange_duality import AffineBranch, all_local_spaces, span

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT/"research/PRODUCT_CHANNEL_ERASURE_CEILING.md"
REPORT = ROOT/"research/classical_baselines/product_channel_erasure_ceiling.json"
PRIMES = (2, 3, 5, 7)


def distribution(values):
    q = tuple(rational(v, "exact coordinate probability") for v in values)
    if len(q) not in PRIMES or any(v < 0 for v in q) or sum(q) != 1:
        raise ValueError("normalized nonnegative distribution over a supported prime field required")
    return q


def coordinate_recipe(values):
    q = distribution(values)
    p, m = len(q), min(q)
    return {"probabilities": tuple(map(str, q)), "minimum_symbol": q.index(m),
            "uniform_branch_weight": str(p*m), "point_branch_weights": tuple(str(v-m) for v in q),
            "optimal_revealed_symbols": str(p*m), "optimal_unknown_symbols": str(1-p*m),
            "affine_point_branch_phases_retained": True}


def entropy_box(values, base, bits=64):
    q = tuple(rational(v, "entropy probability") for v in values)
    if any(v < 0 for v in q) or sum(q) != 1:
        raise ValueError("normalized nonnegative entropy law required")
    integer(base, "entropy base greater than1", 2)
    integer(bits, "entropy interval precision", 1)
    lower, upper, terms = fmpq(0), fmpq(0), []
    for v in q:
        if not v:
            terms.append(None)
            continue
        a, b = logarithm_box(int(v.denominator), bits), logarithm_box(int(v.numerator), bits)
        lower += v*(fmpq(a["lower"])-fmpq(b["upper"]))
        upper += v*(fmpq(a["upper"])-fmpq(b["lower"]))
        terms.append({"denominator_log": a, "numerator_log": b})
    normalization = logarithm_box(base, bits)
    lo = max(fmpq(0), lower/fmpq(normalization["upper"]))
    hi = max(fmpq(0), upper/fmpq(normalization["lower"]))
    return {"probabilities": tuple(map(str, q)), "base": base, "bits": bits,
            "log_certificates": terms, "base_log_certificate": normalization,
            "lower": str(lo), "upper": str(hi)}


def helstrom_hard_decision(values, bits=64):
    q = distribution(values)
    if len(q) != 2:
        raise ValueError("named binary Helstrom benchmark requires two symbols")
    c = abs(q[0]-q[1])
    lo, hi = sqrt_box(1-c*c, bits)
    e_lo, e_hi = max(fmpq(0), (1-hi)/2), min(fmpq(1, 2), (1-lo)/2)
    left, right = entropy_box((e_lo, 1-e_lo), 2, bits), entropy_box((e_hi, 1-e_hi), 2, bits)
    return {"binary_overlap": str(c), "bits": bits, "sqrt_argument": str(1-c*c),
            "sqrt_lower": str(lo), "sqrt_upper": str(hi),
            "crossover_lower": str(e_lo), "crossover_upper": str(e_hi),
            "left_entropy": left, "right_entropy": right,
            "named_hard_decision_rate_lower": str(max(fmpq(0), 1-fmpq(right["upper"]))),
            "named_hard_decision_rate_upper": str(min(fmpq(1), 1-fmpq(left["lower"]))),
            "efficient_code_decoder_supplied": False,
            "all_adaptive_or_collective_measurements_bounded": False}


def profile(values, length, code_dimension, bits=64, protocol="terminal_affine_erasure"):
    q = distribution(values)
    integer(length, "positive channel block length", 1)
    integer(code_dimension, "positive actual code dimension", 1)
    if code_dimension > length:
        raise ValueError("code dimension exceeds channel block length")
    if protocol != "terminal_affine_erasure":
        return {"status": "ERASURE_CEILING_NOT_APPLICABLE_TO_COHERENT_OR_MINIMUM_ERROR_POSTPROCESSING",
                "affine_isometry_itself_loses_information": False, "quantum_receiver_excluded": False}
    p, recipe = len(q), coordinate_recipe(q)
    information = length*p*min(q)
    H = entropy_box(q, p, bits)
    ln2, lnp = logarithm_box(2, bits), logarithm_box(p, bits)
    allowance = fmpq(ln2["upper"])/fmpq(lnp["lower"])
    if p == 2:
        allowance = fmpq(1)
    affine_error = max(fmpq(0), 1-(information+allowance)/code_dimension)
    quantum_error = max(fmpq(0), 1-(length*fmpq(H["upper"])+allowance)/code_dimension)
    rate = fmpq(code_dimension, length)
    local = helstrom_hard_decision(q, bits) if p == 2 else None
    if rate > fmpq(H["upper"]):
        status = "HOLEVO_EXCLUDES_VANISHING_ERROR_AT_THIS_RATE"
    elif rate > p*min(q) and rate < fmpq(H["lower"]):
        if local is not None and rate < fmpq(local["named_hard_decision_rate_lower"]):
            status = "ERASURE_RATE_EXCEEDED_NAMED_LOCAL_HELSTROM_COMPATIBLE_NOT_DECODER"
        elif local is not None and rate > fmpq(local["named_hard_decision_rate_upper"]):
            status = "NAMED_LOCAL_HELSTROM_RATE_EXCEEDED_HOLEVO_COMPATIBLE_NOT_DECODER"
        else:
            status = "ERASURE_RATE_EXCEEDED_HOLEVO_COMPATIBLE_NO_NAMED_LOCAL_DECODER"
    else:
        status = "NO_RATE_SEPARATION_CERTIFIED"
    return {"status": status, "prime": p, "length": length, "actual_code_dimension_contract": code_dimension,
            "code_rate": str(rate), "bits": bits, "coordinate_recipe": recipe,
            "optimal_terminal_affine_revealed_symbols": str(information),
            "optimal_affine_mean_unknown_symbols": str(length-information),
            "channel_Holevo_symbols": H, "named_local_Helstrom": local,
            "ln2_certificate": ln2, "lnprime_certificate": lnp, "Fano_allowance_symbols_upper": str(allowance),
            "terminal_affine_decoder_error_lower": str(affine_error),
            "all_quantum_decoder_error_Holevo_lower": str(quantum_error),
            "terminal_branch_and_linear_readout_only": True,
            "retained_coherent_branch_postprocessing_excluded": False,
            "naive_incidence_matrix_full_rank_assumed": False,
            "rate_contract_is_an_executed_code_family": False,
            "efficient_decoder_supplied": False, "classical_computational_lower_bound_supplied": False,
            "new_quantum_speedup_established": False}


def finite_affine_duals(values, width):
    q, p = distribution(values), len(values)
    integer(width, "bounded local dual width", 1)
    if p**width > 32:
        raise ValueError("complete affine dual controls capped at32 points")
    vectors = tuple(product(range(p), repeat=width))
    zero = (0,)*width
    spaces = {(zero,): ()}
    for rank in range(1, width+1):
        for candidate in combinations(tuple(v for v in vectors if v != zero), rank):
            rref, r = nmod_mat(candidate, p).rref()
            if r != rank:
                continue
            basis = tuple(tuple(map(int, row)) for row in rref.tolist() if any(row))
            members = tuple(sorted({tuple(sum(t[j]*basis[j][i] for j in range(rank)) % p for i in range(width)) for t in product(range(p), repeat=rank)}))
            spaces[members] = basis
    affine = {}
    for S, basis in spaces.items():
        for a in vectors:
            members = tuple(sorted(tuple((y[i]+a[i]) % p for i in range(width)) for y in S))
            affine.setdefault(members, (basis, a))
    a_min = q.index(min(q))
    records = []
    for S in sorted(affine, key=lambda S: (len(S), S)):
        basis, offset = affine[S]
        varying = sum(any(b[i] for b in basis) for i in range(width))
        avg = fmpq(sum(width-p*sum(y[i] == a_min for i in range(width)) for y in S), len(S))
        cost = width-len(basis)
        if avg > cost or len(basis) > varying:
            raise ArithmeticError("coordinate marginal dual failed on an affine subspace")
        records.append({"basis": basis, "offset": offset, "members": S, "dimension": len(basis),
                        "varying_coordinates": varying, "unknown_symbols": cost, "dual_average": str(avg)})
    return {"prime": p, "width": width, "coordinate_recipe": coordinate_recipe(q),
            "all_affine_subspaces": records, "dual_expectation": str(width*(1-p*min(q))),
            "factored_primal_expected_unknown_symbols": str(width*(1-p*min(q))),
            "optimal_among_arbitrary_correlated_affine_flat_mixtures": True,
            "all_quantum_measurements_excluded": False}


def binary_code_information_controls():
    c, k = fmpq(1, 2), 3
    branches = []
    for mask in range(8):
        basis = tuple(1 << j for j in range(k) if (mask >> j)&1)
        branches.append(AffineBranch(k, basis, (1-c)**len(basis)*c**(k-len(basis))))
    records = []
    for C in all_local_spaces(k):
        basis = []
        for d in C:
            if d not in span(basis):
                basis.append(d)
        info, outcomes = fmpq(0), []
        for b in branches:
            rows = [[(v&d).bit_count() % 2 for d in basis] for v in b.basis]
            rank = nmod_mat(rows, 2).rref()[1] if rows and basis else 0
            info += b.weight*rank
            outcomes.append({"revealed_coordinate_basis": b.basis, "branch_weight": str(b.weight), "restricted_report_rank": rank})
        if info > k*(1-c):
            raise ArithmeticError("coded terminal information exceeds marginal ceiling")
        records.append({"code_members": C, "code_dimension": len(basis), "branches": outcomes,
                        "terminal_mutual_information_bits": str(info), "unrestricted_rank_budget_bits": "3/2"})
    return records


def correlated_countercontrol():
    q = tuple(map(fmpq, ("2/5", "1/10", "1/10", "2/5")))
    dual = tuple(map(fmpq, ("1", "-1", "-1", "1")))
    from linear_erasure_prange_duality import all_affine_spaces
    inequalities = [{"members": S, "unknown_bits": 2-(len(S).bit_length()-1),
                     "dual_average": str(sum(dual[y] for y in S)/len(S))} for S in all_affine_spaces(2)]
    return {"joint_frequency_probabilities": tuple(map(str, q)), "both_coordinate_marginals": ("1/2", "1/2"),
            "marginal_unknown_lower": "0", "optimal_unknown_bits": "3/5",
            "exact_dual_coefficients": tuple(map(str, dual)), "all_affine_subspaces": inequalities,
            "primal_full_space_weight": "2/5", "primal_diagonal_line_weight": "3/5",
            "product_assumption_satisfied": False, "marginal_lower_bound_is_always_achievable": False}


def build_report():
    controls = [profile(("3/4", "1/4"), n, (n*r+19)//20) for n in (64, 256, 4096, 1048576) for r in (12, 15, 18)]
    controls += [profile(("1/2", "1/3", "1/6"), 4096, 3072),
                 profile(("3/5", "1/10", "1/10", "1/10", "1/10"), 4096, 3072),
                 profile(("1/2", "1/2"), 64, 64), profile(("1", "0"), 64, 32)]
    return {"status": "PRODUCT_TERMINAL_AFFINE_ERASURE_CEILING_EXTERNAL_REVIEW_PENDING",
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "scalable_rate_controls": controls,
            "complete_affine_dual_controls": [finite_affine_duals(q, k) for q, k in ((("3/4", "1/4"), 3), (("1/2", "1/3", "1/6"), 2), (("3/5", "1/10", "1/10", "1/10", "1/10"), 2))],
            "complete_binary_code_information_controls": binary_code_information_controls(),
            "correlated_marginal_countercontrol": correlated_countercontrol(),
            "retained_coherence_countercontract": profile(("3/4", "1/4"), 4096, 3072, protocol="retained_coherent_branches"),
            "general_quantum_algorithm_impossibility_claimed": False,
            "capacity_compatible_rates_are_efficient_decoders": False,
            "accepted_speedup_candidate": False, "novelty_verified": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report), indent=2)+"\n")
    print(json.dumps({"status": report["status"], "rate_controls": len(report["scalable_rate_controls"]),
                      "complete_affine_duals": sum(len(c["all_affine_subspaces"]) for c in report["complete_affine_dual_controls"]),
                      "complete_binary_code_controls": 16, "largest_length": 1048576,
                      "efficient_quantum_decoder_supplied": False}, indent=2))


if __name__ == "__main__":
    main()
