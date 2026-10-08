"""Exact modulo-two shadows of actual native integer-prefix continuations.

LOCAL DERIVATION / REVIEW PENDING. This is a discrete falsification baseline,
not a native solver, a source-hardness theorem or a new quantum algorithm.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import random
import time

from flint import nmod_mat
from ternary_pair_collimation import LowProblem
from ternary_pair_lattice import word_coordinates
from ternary_repair_catalog import FIXTURE, frozen_policy
from ternary_adaptive_shell import compile_adaptive
from ternary_prefix_integrality import frontier_geometry, REPORT as PREFIX_REPORT

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/ternary_prefix_modular.json"


def _matrix(rows, width):
    # Reduce arbitrary-size native integers before passing them to FLINT.
    if any(len(row) != width or any(type(x) is not int for x in row) for row in rows):
        raise ValueError("exact integer rows of the declared native width required")
    return nmod_mat(len(rows), width, [x % 2 for row in rows for x in row], 2)


def binary_shadow(geometry):
    """Eliminate all two-choice domains exactly in the modulo-two image.

    Every two-choice block contributes {0,difference}, a whole F2 line.
    Their sum is their span W. The remaining test is in F2^d/(K_prefix+W).
    This equivalence holds for the MODULAR shadow only, not integer membership.
    """
    d = 2 * geometry["problem"].width
    domains = geometry["domains"]
    if len(domains) != d // 2 or any(not D or tuple(D) != tuple(sorted(set(D))) or
            any(type(x) is not int or x not in (0, 1, 2) for x in D) for D in domains):
        raise ValueError("canonical nonempty native digit domains required")
    baseline = tuple(D[0] for D in domains)
    z_base = word_coordinates(baseline)
    K = geometry["kernel_prefix"]
    if len(K) != geometry["bottom"] or len(geometry["z_anchor"]) != d or any(type(x) is not int for x in geometry["z_anchor"]):
        raise ValueError("complete original prefix and anchor required")
    directions = []
    for j, D in enumerate(domains):
        if len(D) != 2:
            continue
        delta = [0] * d
        for digit, sign in ((D[1], 1), (D[0], -1)):
            if digit:
                delta[2*j + digit - 1] += sign
        directions.append(tuple(delta))
    original_rank = _matrix(K, d).rank()
    span = _matrix((*K, *directions), d)
    H, nullity = span.nullspace()
    rows = tuple(tuple(int(H[j,i]) for j in range(d)) for i in range(nullity))
    delta = tuple(a - c for a, c in zip(geometry["z_anchor"], z_base))

    def syndrome(z):
        return sum((sum(a*x for a, x in zip(h, z)) % 2) << i for i, h in enumerate(rows))

    full = []
    for j, D in enumerate(domains):
        if len(D) == 3:
            u = sum(h[2*j] << i for i, h in enumerate(rows))
            v = sum(h[2*j+1] << i for i, h in enumerate(rows))
            full.append({"block": j, "choices": (0, u, v)})
    return {"field_prime": 2, "native_coordinate_count": d,
        "original_prefix_rank_mod2": original_rank,
        "original_shadow_dimension": d-original_rank,
        "eliminated_binary_span_rank": span.rank()-original_rank,
        "quotient_dimension": len(rows), "quotient_annihilator": rows,
        "baseline_word": baseline, "binary_blocks": [j for j,D in enumerate(domains) if len(D)==2],
        "singleton_blocks": [j for j,D in enumerate(domains) if len(D)==1],
        "full_blocks": full, "target_syndrome": syndrome(delta),
        "exact_binary_elimination_not_valid_over_F3": True}


def support_dp(shadow, max_states=65_536):
    """Complete support, unless preflight forbids the whole ambient group.

    A full support at ANY stage remains full under subsequent nonempty-domain
    convolutions. Early saturation therefore proves every final syndrome legal.
    A reachable syndrome is never promoted to an integer native completion.
    """
    if type(max_states) is not int or max_states < 1:
        raise ValueError("positive full-support preflight budget required")
    r = shadow["quotient_dimension"]
    if type(r) is not int or r < 0:
        raise ValueError("nonnegative binary quotient dimension required")
    size = 1 << r
    target = shadow["target_syndrome"]
    if type(target) is not int or not 0 <= target < size:
        raise ValueError("target syndrome outside declared quotient")
    blocks = shadow["full_blocks"]
    for block in blocks:
        if not block["choices"] or any(type(x) is not int or not 0 <= x < size for x in block["choices"]):
            raise ValueError("nonempty correctly sized block support required")
    cost = {"xor_transitions": 0, "peak_support_states": 0, "blocks_processed": 0,
            "ambient_states": str(size), "preflight_budget": max_states}
    if size > max_states:
        return {"status": "SHADOW_PREFLIGHT_UNKNOWN", "target_reachable": None,
            "support_saturated": False, "cost": cost, "support_history": []}
    support = {0}; history = [1]; cost["peak_support_states"] = 1
    for block in blocks:
        if len(support) == size:
            break
        choices = set(block["choices"])
        cost["xor_transitions"] += len(support)*len(choices)
        support = {x ^ c for x in support for c in choices}
        cost["blocks_processed"] += 1
        cost["peak_support_states"] = max(cost["peak_support_states"], len(support))
        history.append(len(support))
    saturated = len(support) == size
    reachable = target in support
    return {"status": "ALL_MOD2_PREFIX_PREDICATES_POWERLESS" if saturated else
        "MOD2_NATIVE_PREFIX_OBSTRUCTION" if not reachable else "MOD2_TARGET_REACHABLE_NOT_NATIVE",
        "target_reachable": reachable, "support_saturated": saturated,
        "final_support_size": len(support), "support_history": history, "cost": cost,
        "early_saturation_preserves_all_later_nonempty_domains": saturated,
        "integer_completion_proved": False}


def fourier_support_bound(shadow, max_characters=65_536):
    """Exact triangle bound on EVERY syndrome probability, not a float signal.

    For a ternary block {0,u,v}, every binary character has absolute mean
    either 1 or 1/3. If B=sum_{h!=0}3^{-block_weight(h)}<1, Fourier inversion
    proves full support. Failure of this SUFFICIENT condition says nothing.
    """
    if type(max_characters) is not int or max_characters < 1:
        raise ValueError("positive Fourier preflight budget required")
    r = shadow["quotient_dimension"]
    if type(r) is not int or r < 0:
        raise ValueError("nonnegative binary quotient dimension required")
    size = 1 << r
    blocks = shadow["full_blocks"]
    if any(len(b["choices"])!=3 or b["choices"][0]!=0 or
           any(type(x) is not int or not 0<=x<size for x in b["choices"]) for b in blocks):
        raise ValueError("exact three-choice {0,u,v} binary block images required")
    if size > max_characters:
        return {"status": "FOURIER_PREFLIGHT_UNKNOWN", "characters_checked": 0,
                "proves_full_support": False, "ambient_characters": str(size)}
    F = len(blocks); histogram = [0]*(F+1)
    operations = 0
    for h in range(1, size):
        weight = 0
        for block in blocks:
            _, u, v = block["choices"]
            weight += bool((h & u).bit_count()%2 or (h & v).bit_count()%2)
            operations += 2
        histogram[weight] += 1
    denominator = 3**F
    numerator = sum(n * 3**(F-w) for w,n in enumerate(histogram))
    lower_numerator = max(0, denominator-numerator)
    return {"status": "EXACT_FOURIER_FULL_SUPPORT" if numerator < denominator else "FOURIER_BOUND_INCONCLUSIVE",
        "proves_full_support": numerator < denominator, "nonzero_character_weight_histogram": histogram,
        "absolute_nontrivial_mass_numerator": str(numerator), "common_denominator": str(denominator),
        "every_syndrome_probability_lower_bound": [str(lower_numerator), str(size*denominator)],
        "characters_checked": size-1, "parity_evaluations": operations,
        "bound_failure_is_not_missing_support": True}


def _affine_binary(rows, rhs, width):
    """FLINT exact affine solve with packed homogeneous directions."""
    augmented = nmod_mat(len(rows),width+1,[x%2 for row,t in zip(rows,rhs) for x in (*row,t)],2)
    reduced, _ = augmented.rref()
    particular = 0
    for i in range(reduced.nrows()):
        pivot = next((j for j in range(width) if reduced[i,j]),None)
        if pivot is None:
            if reduced[i,width]: return None
        else:
            particular |= int(reduced[i,width]) << pivot
    kernel, nullity = _matrix(rows,width).nullspace()
    directions = tuple(sum(int(kernel[j,i])<<j for j in range(width)) for i in range(nullity))
    return particular, directions


def verify_modular_word(geometry, word, coefficients):
    """Pointwise original-coordinate proof, independent of proposal/quotient."""
    if len(word)!=geometry["problem"].width or any(type(x) is not int or x not in D for x,D in zip(word,geometry["domains"])):
        raise ValueError("original native word respecting every retained domain required")
    if len(coefficients)!=geometry["bottom"] or any(type(x) is not int or x not in (0,1) for x in coefficients):
        raise ValueError("complete binary original-prefix coefficient array required")
    z = word_coordinates(word)
    valid = all((x-a-sum(c*row[j] for c,row in zip(coefficients,geometry["kernel_prefix"])))%2==0
                for j,(x,a) in enumerate(zip(z,geometry["z_anchor"])))
    return {"valid":valid,"native_word":tuple(word),"prefix_coefficients_mod2":tuple(coefficients),
        "original_target_matches":geometry["problem"].value(word)==geometry["target"],
        "integer_prefix_membership_proved":False,"field_prime":2,
        "certificate_only_proves_mod2_feasibility":True}


def propose_modular_word(geometry, shadow, max_attempts=16_384, seed=420761):
    """Uniform affine proposals; never mistake failed rejection for hardness.

    Binary domains are eliminated exactly first. Remaining two bits per full
    triangle are uniformly sampled from the exact affine GF2 solution space.
    The forbidden (1,1) is rejected, then eliminated binary choices recovered.
    Acceptance may be exponentially small; the trial cap is NOT a runtime theorem.
    """
    if type(max_attempts) is not int or max_attempts < 1 or type(seed) is not int:
        raise ValueError("positive proposal budget and public integer seed required")
    F = len(shadow["full_blocks"]); r = shadow["quotient_dimension"]
    rows = [tuple((block["choices"][digit]>>i)&1 for block in shadow["full_blocks"] for digit in (1,2)) for i in range(r)]
    rhs = tuple((shadow["target_syndrome"]>>i)&1 for i in range(r))
    system = _affine_binary(rows,rhs,2*F)
    cost = {"affine_proposals":0,"native_digit_checks":0,"random_nullspace_xors":0,
            "recovery_affine_solves":0,"proposal_budget":max_attempts,"seed":seed}
    if system is None:
        return {"status":"EXACT_AFFINE_MOD2_OBSTRUCTION","certificate":None,"cost":cost}
    particular, directions = system; cost["affine_free_bits"] = len(directions)
    rng = random.Random(seed)
    for _ in range(max_attempts):
        cost["affine_proposals"] += 1
        bits = particular; random_bits = rng.getrandbits(len(directions))
        while random_bits:
            k = (random_bits & -random_bits).bit_length()-1
            bits ^= directions[k]; random_bits &= random_bits-1
            cost["random_nullspace_xors"] += 1
        legal = True
        for j in range(F):
            cost["native_digit_checks"] += 1
            if (bits>>(2*j))&3 == 3:
                legal = False; break
        if not legal: continue
        word = list(shadow["baseline_word"])
        for j,block in enumerate(shadow["full_blocks"]):
            pair = (bits>>(2*j))&3
            word[block["block"]] = 1 if pair==1 else 2 if pair==2 else 0
        z = word_coordinates(word); d = len(z); K = geometry["kernel_prefix"]
        Drows = []
        for j in shadow["binary_blocks"]:
            D = geometry["domains"][j]; delta = [0]*d
            for digit,sign in ((D[1],1),(D[0],-1)):
                if digit: delta[2*j+digit-1] += sign
            Drows.append(tuple(delta))
        combined = (*K,*Drows)
        equations = [tuple(row[j] for row in combined) for j in range(d)]
        recovery = _affine_binary(equations,tuple(x-a for x,a in zip(z,geometry["z_anchor"])),len(combined))
        cost["recovery_affine_solves"] += 1
        if recovery is None: raise ArithmeticError("quotient witness failed exact binary-domain recovery")
        solution = recovery[0]; b = len(K)
        for i,j in enumerate(shadow["binary_blocks"]):
            if solution>>(b+i)&1: word[j] = geometry["domains"][j][1]
        coefficients = tuple((solution>>i)&1 for i in range(b))
        certificate = verify_modular_word(geometry,tuple(word),coefficients)
        if not certificate["valid"]: raise ArithmeticError("recovered modular word violates original prefix")
        return {"status":"EXACT_NATIVE_MOD2_WORD_NOT_INTEGER_CONTINUATION","certificate":certificate,"cost":cost}
    return {"status":"MODULAR_PROPOSAL_CAP_UNKNOWN","certificate":None,"cost":cost,
        "failure_is_not_modular_or_integer_infeasibility":True}


def analyze_geometry(geometry, max_states=65_536, max_attempts=16_384, seed=420761):
    shadow = binary_shadow(geometry)
    start = time.perf_counter()
    dp = support_dp(shadow, max_states)
    fourier = fourier_support_bound(shadow, max_states)
    witness = propose_modular_word(geometry,shadow,max_attempts,seed)
    if fourier["proves_full_support"] and not dp["support_saturated"]:
        raise ArithmeticError("exact Fourier and complete support certificates disagree")
    if dp["target_reachable"] is False and witness["certificate"]:
        raise ArithmeticError("complete support and modular witness contradict each other")
    return {"shadow": shadow, "support": dp, "fourier": fourier, "modular_witness":witness,
            "analysis_wall_seconds": time.perf_counter()-start,
            "basis_and_quotient_preparation_excluded_from_wall_seconds": True}


def build_report(max_states=65_536,max_attempts=16_384):
    source = json.loads(FIXTURE.read_text())
    prefix = json.loads(PREFIX_REPORT.read_text()); cases = []
    for old_case in prefix["cases"]:
        old = source["planted_geometry_probes"][old_case["fixture_probe_index"]]
        A = tuple(map(int,old["labels"])); Q = int(old["modulus"])
        problem = LowProblem((Q,),tuple(((a,),(c,)) for a,c in zip(A[::2],A[1::2])),0)
        policy = frozen_policy(problem,old["prepared"]); compiled = compile_adaptive(policy)
        trials = []
        for t in old_case["trials"]:
            # Already linearly obstructed branches do not test the new mechanism.
            if not t.get("prefix_primal",{}).get("certificate"):
                continue
            saved = t["frontier"]
            checkpoint = {"unassigned_rows": saved["unassigned_rows"],
                "partial_coefficients": tuple(map(int,saved["partial_coefficients"])),
                "assigned_squared_energy": saved["assigned_squared_energy"]}
            g = frontier_geometry(problem,(int(t["target"]),),policy,compiled,checkpoint)
            result = analyze_geometry(g,max_states,max_attempts,int(t["target"])+420761)
            if result["support"]["target_reachable"] is False and t["native_truth"]["native_prefix_words"]:
                raise ArithmeticError("modular obstruction rejected an actual native word")
            # Packed syndromes may exceed JavaScript's lossless integer range.
            result["shadow"]["target_syndrome"] = str(result["shadow"]["target_syndrome"])
            for block in result["shadow"]["full_blocks"]:
                block["choices"] = [str(x) for x in block["choices"]]
            trials.append({"target":t["target"],"prefix_audit_status":t["status"],
                "native_truth_known": t["native_truth"]["native_prefix_words"] is not None,
                "integer_winding_gap":t["status"]=="EXACT_WINDING_PREFIX_INTEGRALITY_GAP",**result})
        cases.append({"fixture_probe_index":old_case["fixture_probe_index"],
            "root_digits":old_case["root_digits"],"fingerprint":old_case["fingerprint"],"trials":trials})
    return {"status":"EXACT_DISCRETE_MOD2_PREFIX_AUDIT_NOT_NATIVE_SOLVER",
        "source_prefix_report":str(PREFIX_REPORT.relative_to(ROOT)),
        "local_derivations_review_pending":True,"novelty_claim":False,
        "polynomial_pair_finder_proved":False,"population_obstruction_proved":False,
        "full_annihilator_used_not_selected_low_rank_projection":True,
        "conditional_saved_frontiers_not_population_samples":True,"cases":cases}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write",action="store_true")
    parser.add_argument("--max-states",type=int,default=65_536)
    parser.add_argument("--max-attempts",type=int,default=16_384)
    args = parser.parse_args(); report = build_report(args.max_states,args.max_attempts)
    if args.write:
        REPORT.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"status":report["status"],"roots":[{"root_digits":r,
        "statuses":dict(Counter(t["support"]["status"] for c in report["cases"] if c["root_digits"]==r for t in c["trials"])),
        "witnesses":dict(Counter(t["modular_witness"]["status"] for c in report["cases"] if c["root_digits"]==r for t in c["trials"])),
        "quotient_dimensions":[t["shadow"]["quotient_dimension"] for c in report["cases"] if c["root_digits"]==r for t in c["trials"]]}
        for r in (16,24,32)]},indent=2))
