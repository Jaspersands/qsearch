"""Attack the BPQM sampling hypothesis with its actual classical competitor.

Exact small-instance mixing controls and seeded random-socket native runs.
No large-instance mixing theorem, classical separation or quantum execution.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.bpqm_gibbs_frontier import (
    XorIsing, affine_jump_geometry, affine_system, cluster_step,
    exact_cluster_kernel, integer, rational,
)
from theorems.xor_factor_reference import ExactXorReference, FactorReferenceLimit

REPORT = ROOT/"research/classical_baselines/affine_cluster_native_probe.json"


def socket_instance(spins, rng, *, variable_degree=3, check_degree=6):
    """Uniform socket matching, modulo-two parallel edges, independent signs.

    No rank, girth, sign or favorable-trajectory rejection is performed.
    The supplied RNG controls reproducibility; a seed is not an IID certificate.
    """
    integer(spins, "native spin count", 1, 100000)
    integer(variable_degree, "clause socket degree", 3, 12)
    integer(check_degree, "spin socket degree", variable_degree+1, 32)
    if spins*check_degree % variable_degree:
        raise ValueError("integral clause count required")
    clauses = spins*check_degree//variable_degree
    right = [spin for spin in range(spins) for _ in range(check_degree)]
    rng.shuffle(right)
    rows = []
    for i in range(clauses):
        mask = 0
        for spin in right[i*variable_degree:(i+1)*variable_degree]:
            mask ^= 1 << spin
        rows.append((mask, rng.randrange(2)))
    model = XorIsing(spins, tuple(rows))
    counts = Counter(right)
    source = {"ensemble": "uniform_regular_socket_matching_mod2_parallel_edges",
              "spins": spins, "clauses": clauses, "variable_degree": variable_degree,
              "check_degree": check_degree, "raw_spin_socket_counts": [counts[i] for i in range(spins)],
              "parallel_pairs_cancelled": sum((variable_degree-a.bit_count())//2 for a, _ in rows),
              "clause_masks_hex_and_signs": [[hex(a), b] for a, b in rows],
              "conditioned_on_rank_girth_sign_or_success": False}
    return model, source


def exact_native_mixing(model, overlap, *, squarings=4):
    """Exact TV and character Rayleigh controls on a bounded full kernel.

    A Rayleigh quotient is an UPPER bound on the gap, not a rapid-mixing bound.
    Exact whole-kernel powers do bound TV, but only for this finite instance.
    """
    if model.spins > 4 or len(model.clauses) > 8:
        raise ValueError("UNKNOWN: full-kernel native calibration capped at four spins/eight clauses")
    integer(squarings, "kernel squaring budget", 0, 6)
    target, kernel = exact_cluster_kernel(model, overlap)
    size = len(target)
    witnesses = []
    for mask in range(1, size):
        values = [1 if (mask & x).bit_count() % 2 == 0 else -1 for x in range(size)]
        mean = sum(p*v for p, v in zip(target, values))
        variance = 1-mean*mean
        energy = sum(target[x]*kernel[x][y]*(values[x]-values[y])**2
                     for x in range(size) for y in range(size))/2
        witnesses.append((energy/variance, mask))
    gap_upper, mode = min(witnesses)
    powers, current, steps = [], kernel, 1
    for level in range(squarings+1):
        distances = [sum(abs(row[y]-target[y]) for y in range(size))/2 for row in current]
        powers.append({"steps": steps, "worst_start_TV_exact": str(max(distances)),
                       "stationary_mean_TV_exact": str(sum(target[x]*distances[x] for x in range(size)))})
        if level < squarings:
            current = tuple(tuple(sum(current[x][z]*current[z][y] for z in range(size))
                                  for y in range(size)) for x in range(size))
            steps *= 2
    return {"spins": model.spins, "clauses": len(model.clauses), "overlap_c_exact": str(rational(overlap)),
            "all_start_TV_controls": powers, "best_character_mask_hex": hex(mode),
            "spectral_gap_upper_from_character_exact": str(gap_upper),
            "spectral_gap_lower_bound_inferred_from_character": False,
            "asymptotic_mixing_proved": False, "full_kernel_enumeration_is_charged": True}


def native_trajectory(model, overlap, *, seed, start, steps=512, burn_in=128):
    integer(steps, "trajectory steps", 1, 10**6)
    integer(burn_in, "burn-in bookkeeping", 0, steps-1)
    integer(start, "starting word", 0, (1 << model.spins)-1)
    rng = random.Random(seed)
    modes = (1, (1 << model.spins)-1)
    word, holding, jumps, selected_rows, dependent_rows, solves = start, 0, 0, 0, 0, 0
    expected_jumps = Fraction(0)
    expected_holds = Fraction(0)
    retained = [0]*len(modes)
    observed_modes = [0]*len(modes)
    energy = 0
    recorded = 0
    for step in range(steps):
        old = word
        result = cluster_step(model, overlap, word, rng, geometry=True, modes=modes)
        word = result["word"]
        solves += 1
        selected_rows += result["selected_count"]
        dependent_rows += result["dependent_rows_retained"]
        if step >= burn_in:
            recorded += 1
            holding += word == old
            jumps += (word ^ old).bit_count()
            expected_holds += Fraction(result["geometry"]["holding_probability_exact"])
            expected_jumps += Fraction(result["geometry"]["expected_hamming_jump_exact"])
            energy += 2*len(model.satisfied(word))-len(model.clauses)
            for i, mask in enumerate(modes):
                retained[i] += result["geometry"]["parity_retained"][i]
                observed_modes[i] += 1 if (mask & word).bit_count() % 2 == 0 else -1
    return {"seed": seed, "initial_word_hex": hex(start), "final_word_hex": hex(word),
            "steps": steps, "burn_in_discarded_but_charged": burn_in,
            "recorded_steps": recorded, "affine_solve_calls": solves,
            "selected_equation_rows_processed": selected_rows, "dependent_rows_not_discarded": dependent_rows,
            "observed_holding_fraction": str(Fraction(holding, recorded)),
            "conditional_holding_fraction_average": str(expected_holds/recorded),
            "mean_hamming_jump": str(Fraction(jumps, recorded)),
            "conditional_mean_hamming_jump": str(expected_jumps/recorded),
            "mean_signed_clause_score": str(Fraction(energy, recorded)),
            "parity_masks_hex": list(map(hex, modes)),
            "conditional_parity_retention_fractions": [str(Fraction(s, recorded)) for s in retained],
            "observed_parity_means": [str(Fraction(s, recorded)) for s in observed_modes],
            "stationary_initialization_claimed": False, "mixing_or_TV_certificate": False,
            "autocorrelated_seeded_replay_not_IID_confidence_certificate": True,
            "no_exponential_Gibbs_table_used": True}


def heatbath_flip_probability(overlap, incident_count, incident_satisfied):
    """Exact conditional flip probability for a signed XOR spin."""
    c = rational(overlap)
    if not 0 <= c < 1:
        raise ValueError("finite nonnegative inverse temperature required")
    integer(incident_count, "incident clauses", 0, 10**6)
    integer(incident_satisfied, "satisfied incident clauses", 0, incident_count)
    odds = ((1+c)/(1-c))**(incident_count-2*incident_satisfied)
    return odds/(1+odds)


def replica_swap_probability(left_c, right_c, left_score, right_score):
    left, right = rational(left_c), rational(right_c)
    if not 0 <= left < 1 or not 0 <= right < 1:
        raise ValueError("finite nonnegative replica temperatures required")
    if type(left_score) is not int or type(right_score) is not int or (right_score-left_score) % 2:
        raise ValueError("integer same-Hamiltonian scores of matching parity required")
    base = ((1+left)/(1-left))/((1+right)/(1-right))
    return min(Fraction(1), base**((right_score-left_score)//2))


def tempering_trajectory(model, *, seed, start, steps=1024, burn_in=256,
                         ladder=("0", "1/5", "2/5", "11/20", "13/20")):
    """Exact-kernel replica exchange; finite seeded diagnostics, not mixing proof."""
    integer(steps, "tempering sweeps", 1, 10**6)
    integer(burn_in, "tempering burn-in", 0, steps-1)
    integer(start, "tempering start", 0, (1 << model.spins)-1)
    temperatures = tuple(map(rational, ladder))
    if len(temperatures) < 2 or any(not 0 <= c < 1 for c in temperatures) or tuple(sorted(set(temperatures))) != temperatures:
        raise ValueError("distinct increasing finite nonnegative temperatures required")
    incident = [[] for _ in range(model.spins)]
    for i, (mask, _) in enumerate(model.clauses):
        residue = mask
        while residue:
            bit = residue & -residue
            incident[bit.bit_length()-1].append(i)
            residue ^= bit
    rng = random.Random(seed)
    words = [start]*len(temperatures)
    scores = [2*len(model.satisfied(start))-len(model.clauses)]*len(temperatures)
    accepted = [0]*(len(temperatures)-1)
    flips = recorded = score_sum = 0
    modes = (1, (1 << model.spins)-1)
    mode_sums = [0]*len(modes)
    for step in range(steps):
        for j, c in enumerate(temperatures):
            order = list(range(model.spins))
            rng.shuffle(order)
            for v in order:
                satisfied = sum((model.clauses[i][0] & words[j]).bit_count() % 2 == model.clauses[i][1]
                                for i in incident[v])
                probability = heatbath_flip_probability(c, len(incident[v]), satisfied)
                if rng.randrange(probability.denominator) < probability.numerator:
                    words[j] ^= 1 << v
                    scores[j] += 2*(len(incident[v])-2*satisfied)
                    flips += 1
        for j in range(len(temperatures)-1):
            probability = replica_swap_probability(temperatures[j], temperatures[j+1], scores[j], scores[j+1])
            if rng.randrange(probability.denominator) < probability.numerator:
                words[j], words[j+1] = words[j+1], words[j]
                scores[j], scores[j+1] = scores[j+1], scores[j]
                accepted[j] += 1
        if step >= burn_in:
            recorded += 1
            score_sum += scores[-1]
            for i, mask in enumerate(modes):
                mode_sums[i] += 1 if (mask & words[-1]).bit_count() % 2 == 0 else -1
    if any(score != 2*len(model.satisfied(word))-len(model.clauses) for score, word in zip(scores, words)):
        raise ArithmeticError("local score cache disagrees with the actual Hamiltonian")
    return {"seed": seed, "start_hex": hex(start), "steps": steps, "burn_in_discarded_but_charged": burn_in,
            "overlap_ladder_exact": list(map(str, temperatures)), "target_overlap_exact": str(temperatures[-1]),
            "target_final_word_hex": hex(words[-1]), "target_final_score": scores[-1],
            "mean_signed_clause_score": str(Fraction(score_sum, recorded)),
            "parity_masks_hex": list(map(hex, modes)), "observed_parity_means": [str(Fraction(s, recorded)) for s in mode_sums],
            "spin_heatbath_proposals": steps*len(temperatures)*model.spins,
            "accepted_spin_flips_all_replicas": flips, "replica_swap_proposals": steps*(len(temperatures)-1),
            "accepted_swaps_by_ladder_edge": accepted,
            "fixed_finite_probe_ladder_not_asymptotically_optimized": True,
            "stationary_initialization_claimed": False, "mixing_or_TV_certificate": False,
            "autocorrelated_seeded_replay_not_IID_confidence_certificate": True,
            "no_exponential_Gibbs_table_used": True}


def run_controls():
    small = []
    for seed in (29, 71):
        model, source = socket_instance(4, random.Random(seed))
        small.append({"seed": seed, "source": source, "exact_mixing": exact_native_mixing(model, "13/20")})
    native = []
    for spins in (16, 32, 64):
        for seed in (29, 71):
            model, source = socket_instance(spins, random.Random(seed))
            traces = [native_trajectory(model, "13/20", seed=seed+123+10000*index, start=start)
                      for index, start in enumerate((0, (1 << spins)-1))]
            native.append({"source_seed": seed, "source": source, "overlap_c_exact": "13/20", "trajectories": traces})
    system = affine_system(tuple(((1 << i) | (1 << (i+1)), 0) for i in range(15)), 16)
    counter = affine_jump_geometry(system, 16, (1, (1 << 16)-1))
    targeted_model, targeted_source = socket_instance(32, random.Random(29))
    targeted = {"source": targeted_source, "source_seed": 29,
                "chosen_after_short_run_discrepancy_not_an_unbiased_ensemble_estimate": True,
                "longer_cluster_replays": [native_trajectory(targeted_model, "13/20", seed=152+10000*i,
                    start=start, steps=8192, burn_in=4096) for i, start in enumerate((0, (1 << 32)-1))],
                "tempering_replays": [tempering_trajectory(targeted_model, seed=347+10000*i,
                    start=start) for i, start in enumerate((0, (1 << 32)-1))]}
    try:
        reference = ExactXorReference(targeted_model, "13/20")
        targeted["exact_factor_reference"] = reference.ledger()
        for key in ("longer_cluster_replays", "tempering_replays"):
            for trace in targeted[key]:
                i = trace["parity_masks_hex"].index("0x1")
                trace["observed_query_mean_minus_exact_reference"] = str(
                    Fraction(trace["observed_parity_means"][i])-reference.query_parity_mean)
                trace["query_mean_discrepancy_is_not_full_law_TV_certificate"] = True
    except FactorReferenceLimit as exc:
        targeted["exact_factor_reference"] = {"status": "UNKNOWN_OPERATIONAL_CAP", "reason": str(exc),
                                              "classical_hardness_inferred": False}
    return {"schema_version": "1.0", "subsystem": "affine_cluster_native_probe",
            "scientific_question": "Does a stronger actual-source classical sampler undermine the BPQM Gibbs hypothesis?",
            "exact_small_native_controls": small, "native_diagnostic_replays": native,
            "one_dimensional_nullspace_global_jump_countercontrol": counter,
            "targeted_stronger_falsifier": targeted,
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "sampler_dependency_sha256": hashlib.sha256((ROOT/"theorems/bpqm_gibbs_frontier.py").read_bytes()).hexdigest(),
            "affine_dependency_sha256": hashlib.sha256((ROOT/"theorems/parity_block_usd_prange.py").read_bytes()).hexdigest(),
            "factor_dependency_sha256": hashlib.sha256((ROOT/"theorems/xor_factor_reference.py").read_bytes()).hexdigest(),
            "large_instance_mixing_certified": False, "classical_hardness_proved": False,
            "quantum_tree_performance_on_these_finite_blocks_claimed": False,
            "quantum_speedup_claim_allowed": False, "new_quantum_algorithm_claimed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = run_controls()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({"small_native": [{"seed": r["seed"], "last_TV_control": r["exact_mixing"]["all_start_TV_controls"][-1]}
                                      for r in result["exact_small_native_controls"]],
                      "native": [{"spins": r["source"]["spins"], "source_seed": r["source_seed"],
                                  "scores": [t["mean_signed_clause_score"] for t in r["trajectories"]],
                                  "holding": [t["observed_holding_fraction"] for t in r["trajectories"]]}
                                 for r in result["native_diagnostic_replays"]],
                      "targeted_scores": {"cluster": [t["mean_signed_clause_score"] for t in result["targeted_stronger_falsifier"]["longer_cluster_replays"]],
                                          "tempering": [t["mean_signed_clause_score"] for t in result["targeted_stronger_falsifier"]["tempering_replays"]]}}, indent=2))


if __name__ == "__main__":
    main()
