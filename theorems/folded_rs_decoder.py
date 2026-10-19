"""Executed known folded-RS interpolation and pruning, not a quantum algorithm.

Uses only the public received word. In particular no error support, message,
free list oracle or q^r enumeration is supplied to the decoder.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import random
import sys

from flint import fmpz_mod_ctx, fmpz_mod_mat

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.bpqm_gibbs_frontier import integer
from theorems.prime_character_capacity_source import rational
from theorems.prime_character_opi import ring

REPORT = ROOT / "research/classical_baselines/folded_rs_decoder.json"


def affine_solution(p, rows, rhs, width):
    """Exact affine system over F_p, including inconsistency and free columns."""
    ring(p)
    integer(width, "affine system width", 1, 1 << 20)
    if len(rows) != len(rhs) or any(len(row) != width for row in rows):
        raise ValueError("rectangular coefficient system required")
    if not rows:
        return {"offset": [0] * width,
                "basis": [[int(i == j) for i in range(width)] for j in range(width)]}
    reduced, _ = fmpz_mod_mat([list(row) + [value] for row, value in zip(rows, rhs)], fmpz_mod_ctx(p)).rref()
    pivots = []
    for i in range(reduced.nrows()):
        pivot = next((j for j in range(width) if reduced[i, j]), None)
        if pivot is None:
            if reduced[i, width]:
                return None
        else:
            pivots.append((i, pivot))
    offset = [0] * width
    for i, j in pivots:
        offset[j] = int(reduced[i, width])
    free = sorted(set(range(width)) - {j for _, j in pivots})
    basis = []
    for j in free:
        v = [0] * width
        v[j] = 1
        for i, pivot in pivots:
            v[pivot] = -int(reduced[i, j]) % p
        basis.append(v)
    if any(sum(a*b for a, b in zip(row, offset)) % p != value % p for row, value in zip(rows, rhs)):
        raise ArithmeticError("affine offset does not solve the original system")
    if any(sum(a*b for a, b in zip(row, v)) % p for row in rows for v in basis):
        raise ArithmeticError("affine direction does not solve the original homogeneous system")
    return {"offset": offset, "basis": basis}


def evaluate(p, coefficients, x):
    result = 0
    for a in reversed(coefficients):
        result = (result * x + a) % p
    return result


def parameters(p, n, m, k, gamma, t, s):
    ring(p)
    integer(n, "folded block count", 1, 4096)
    integer(m, "folding factor", 1, 256)
    integer(k, "DECODED polynomial dimension, not original syndrome rank", 1, n*m)
    integer(t, "maximum erroneous blocks", 0, n - 1)
    integer(s, "linear interpolation order", 1, m)
    integer(gamma, "public folding generator", 1, p - 1)
    points = [pow(gamma, j, p) for j in range(n*m)]
    if len(set(points)) != n*m:
        raise ValueError("folding powers are not distinct; generator order is too small")
    C = n * (m - s + 1)
    D = (C - k + 1) // (s + 1)
    if D < 0 or (n - t) * (m - s + 1) <= D + k - 1:
        raise ValueError("parameters do not satisfy the strict interpolation root guarantee")
    return points, D


def interpolation_space(p, n, m, k, gamma, received, t, s):
    """Construct Q and solve its polynomial identity; no assumed output list."""
    points, D = parameters(p, n, m, k, gamma, t, s)
    if len(received) != n*m or any(type(a) is not int or not 0 <= a < p for a in received):
        raise ValueError("canonical complete folded received word required")
    rows, sizes = [], [D + k] + [D + 1] * s
    for block in range(n):
        for j in range(m - s + 1):
            index = block*m + j
            x = points[index]
            powers = [pow(x, a, p) for a in range(D + k)]
            row = list(powers)
            for shift in range(s):
                row += [a * received[index + shift] % p for a in powers[:D + 1]]
            rows.append(row)
    homogeneous = affine_solution(p, rows, [0] * len(rows), sum(sizes))
    if homogeneous is None or not homogeneous["basis"]:
        raise ArithmeticError("dimension count did not produce a nonzero interpolant")
    vector, pieces, start = homogeneous["basis"][0], [], 0
    for size in sizes:
        pieces.append(vector[start:start + size])
        start += size
    if not any(a for poly in pieces[1:] for a in poly):
        raise ArithmeticError("interpolant has no message-dependent coefficient")
    equations = []
    for h in range(D + k):
        row = []
        for i in range(k):
            v = h - i
            row.append(sum(pieces[j + 1][v] * pow(gamma, j*i, p) for j in range(s)) % p
                       if 0 <= v <= D else 0)
        equations.append(row)
    space = affine_solution(p, equations, [(-a) % p for a in pieces[0]], k)
    if space is not None and len(space["basis"]) > s - 1:
        raise ArithmeticError("solution dimension exceeds the folded power-root bound")
    return {"points": points, "D": D, "interpolant_coefficients_A0_through_As": pieces,
            "interpolation_equations": len(rows), "interpolation_unknowns": sum(sizes),
            "message_identity_equations": len(equations), "affine_space": space}


def prune(p, points, m, space, received, t, *, seed=4703, trials=128):
    """Known received-block pruning with paid failures; never enumerate F_p^r."""
    ring(p)
    integer(m, "folding factor", 1, 256)
    integer(trials, "independent pruning trial budget", 1, 100000)
    if not points or len(points) % m or len(set(points)) != len(points):
        raise ValueError("distinct complete folded evaluation points required")
    if len(received) != len(points) or any(type(a) is not int or not 0 <= a < p for a in list(points) + list(received)):
        raise ValueError("canonical received symbols and evaluation points required")
    integer(t, "maximum erroneous blocks", 0, len(points) // m - 1)
    if space is None:
        return {"candidates": [], "transcript": [], "status": "EMPTY_POLYNOMIAL_IDENTITY_SPACE",
                "per_candidate_miss_upper_exact": "0", "list_completeness_certified": False}
    n, k, r = len(points) // m, len(space["offset"]), len(space["basis"])
    if len(received) != len(points) or len(points) % m or n - t <= (k - 1) // m:
        raise ValueError("complete blocks and positive pruning agreement gap required")
    if any(len(v) != k for v in space["basis"]):
        raise ValueError("affine polynomial directions have inconsistent dimensions")
    if not k or any(type(a) is not int or not 0 <= a < p for v in [space["offset"]] + space["basis"] for a in v):
        raise ValueError("canonical affine polynomial coefficients required")
    if r:
        homogeneous = affine_solution(p, [[v[i] for v in space["basis"]] for i in range(k)], [0] * k, r)
        if homogeneous["basis"]:
            raise ValueError("pruning requires independent affine directions")
    rng, candidates, transcript = random.Random(seed), {}, []
    rounds = trials if r else 1
    for _ in range(rounds):
        rows, rhs, current, selected = [], [], None, []
        for _ in range(r):
            block = rng.randrange(n)
            selected.append(block)
            for j in range(block*m, (block + 1)*m):
                rows.append([evaluate(p, v, points[j]) for v in space["basis"]])
                rhs.append((received[j] - evaluate(p, space["offset"], points[j])) % p)
            current = affine_solution(p, rows, rhs, r)
            if current is None or not current["basis"]:
                break
        if r and (current is None or current["basis"]):
            transcript.append({"blocks_sampled": selected,
                               "status": "INCONSISTENT" if current is None else "RANK_NOT_RESOLVED"})
            continue
        coefficients = [(a + sum(current["offset"][j] * space["basis"][j][i] for j in range(r))) % p
                        for i, a in enumerate(space["offset"])]
        predicted = [evaluate(p, coefficients, x) for x in points]
        bad = [i for i in range(n) if predicted[i*m:(i + 1)*m] != received[i*m:(i + 1)*m]]
        accepted = len(bad) <= t
        if accepted:
            candidates[tuple(coefficients)] = {"polynomial_coefficients": coefficients,
                                                "disagreeing_blocks": bad, "codeword": predicted}
        transcript.append({"blocks_sampled": selected, "status": "VERIFIED_CLOSE_WORD" if accepted else "DISTANCE_REJECTED",
                           "disagreeing_blocks_count": len(bad)})
    delta = Fraction(n - t - (k - 1) // m, n)
    miss = (1 - delta ** r) ** rounds
    return {"candidates": [candidates[key] for key in sorted(candidates)], "transcript": transcript,
            "status": "VERIFIED_CLOSE_WORDS_NOT_A_SPEEDUP" if candidates else "PRUNING_BUDGET_INCONCLUSIVE_NOT_HARDNESS",
            "affine_dimension": r, "pruning_agreement_gap_exact": rational(delta),
            "per_candidate_per_trial_success_lower_exact": rational(delta ** r),
            "per_candidate_miss_upper_exact": rational(miss),
            "uniform_block_draws_charged": sum(len(t["blocks_sampled"]) for t in transcript),
            "candidate_distance_checks_charged": sum("disagreeing_blocks_count" in t for t in transcript),
            "list_completeness_certified": False, "coefficient_field_enumeration_used": False,
            "guarantee_premise": "supplied affine space contains the target; fresh independent uniform blocks; original received word; no known-correct-block oracle"}


def decode(p, n, m, k, gamma, received, t, s, *, seed=4703, trials=128):
    intermediate = interpolation_space(p, n, m, k, gamma, received, t, s)
    result = prune(p, intermediate["points"], m, intermediate["affine_space"], received, t, seed=seed, trials=trials)
    return {"p_decimal": str(p), "n_blocks": n, "m_fold": m, "decoded_dimension_k": k,
            "gamma": gamma, "t_block_errors": t, "interpolation_order_s": s,
            "public_received_word": list(received), **intermediate, **result,
            "hidden_error_support_given_to_decoder": False,
            "resource_model": "explicit polynomial-sized modular matrices and RREF; at most r sampled blocks and r*m constraints per pruning trial; original full-word evaluation per candidate; no p^r loop",
            "seed_is_replay_not_empirical_confidence": True}


def vandermonde_syndrome(p, points, error, rank):
    values, powers = [0] * rank, [1] * len(points)
    for j in range(rank):
        values[j] = sum(a*b for a, b in zip(powers, error)) % p
        powers = [a*b % p for a, b in zip(powers, points)]
    return values


def dual_multipliers(p, points):
    """Actual inverses of product_(j!=i)(a_i-a_j), not free GRS advice."""
    multipliers = []
    for i, x in enumerate(points):
        denominator = 1
        for j, y in enumerate(points):
            if i != j:
                denominator = denominator*(x - y) % p
        multipliers.append(pow(denominator, -1, p))
    return multipliers


def decode_syndrome(p, n, m, K, gamma, syndrome, t, s, *, seed=4703, trials=128):
    """Native H[j,i]=a_i^j; return verified sparse BLOCK errors, not uniqueness."""
    integer(K, "original scalar syndrome rank", 1, n*m - 1)
    points, _ = parameters(p, n, m, n*m - K, gamma, t, s)
    if len(syndrome) != K or any(type(a) is not int or not 0 <= a < p for a in syndrome):
        raise ValueError("canonical ORIGINAL rank-K syndrome required")
    system = [[pow(x, j, p) for x in points[:K]] for j in range(K)]
    particular = affine_solution(p, system, syndrome, K)
    if particular is None or particular["basis"]:
        raise ArithmeticError("distinct-point Vandermonde particular solve failed")
    y = particular["offset"] + [0] * (n*m - K)
    multipliers = dual_multipliers(p, points)
    received = [a * pow(v, -1, p) % p for a, v in zip(y, multipliers)]
    ordinary = decode(p, n, m, n*m - K, gamma, received, t, s, seed=seed, trials=trials)
    errors = []
    for candidate in ordinary["candidates"]:
        e = [(a - v*c) % p for a, v, c in zip(y, multipliers, candidate["codeword"])]
        bad = [i for i in range(n) if any(e[i*m:(i + 1)*m])]
        if len(bad) > t or vandermonde_syndrome(p, points, e, K) != list(syndrome):
            raise ArithmeticError("decoded error fails ORIGINAL syndrome or block-weight bound")
        errors.append({"error_word": e, "nonzero_blocks": bad,
                       "ordinary_RS_polynomial": candidate["polynomial_coefficients"]})
    return {"p_decimal": str(p), "n_blocks": n, "m_fold": m,
            "ORIGINAL_scalar_syndrome_rank_K": K, "syndrome": list(syndrome),
            "points": points, "computed_GRS_multipliers": multipliers,
            "computed_public_particular_word": y, "ordinary_decoder": ordinary,
            "verified_error_candidates": errors,
            "unique_source_erasure_or_complete_list_certified": False,
            "hidden_error_or_support_input": False,
            "GRS_conversion_field_inverse_calls_charged": 2*n*m,
            "GRS_multiplier_product_factors_charged": n*m*(n*m - 1),
            "original_syndrome_scalar_terms_checked": K*n*m*len(errors),
            "resource_model": "PAID rank-K Vandermonde solve, O((nm)^2) multiplier products and 2nm GRS conversion field inversions, actual folded decoder/pruning and direct original syndrome checks"}


def run_controls():
    rows = []
    for p, n, m, k, gamma, t, s in ((1019, 10, 15, 60, 2, 4, 3),
                                   ((1 << 61) - 1, 25, 31, 465, 3, 6, 4)):
        rng = random.Random(4721 + n)
        points, _ = parameters(p, n, m, k, gamma, t, s)
        message = [rng.randrange(p) for _ in range(k)]
        clean = [evaluate(p, message, x) for x in points]
        received = list(clean)
        support = sorted(rng.sample(range(n), t))
        for block in support:
            error = [rng.randrange(1, p) for _ in range(m)]
            for r, a in enumerate(error):
                received[block*m + r] = (received[block*m + r] + a) % p
        result = decode(p, n, m, k, gamma, received, t, s)
        recovered = any(c["polynomial_coefficients"] == message for c in result["candidates"])
        rows.append({"calibration_true_message": message, "calibration_hidden_error_support": support,
                     "target_recovered": recovered, "MDS_guaranteed_unique_block_radius": (n*m - k) // (2*m),
                     "beyond_guaranteed_unique_radius": t > (n*m - k) // (2*m), **result})
    # This received word is close to TWO actual folded codewords. A decoder
    # finding one must never be mistaken for proof of unique source erasure.
    p, n, m, k, gamma, t, s = 1019, 10, 15, 60, 2, 4, 3
    points, _ = parameters(p, n, m, k, gamma, t, s)
    R = ring(p)
    polynomial = R([1])
    zero_blocks = (k - 1) // m
    for x in points[(n - zero_blocks)*m:]:
        polynomial *= R([-x % p, 1])
    other = [int(polynomial[i]) for i in range(k)]
    other_values = [evaluate(p, other, x) for x in points]
    received = [a if i // m < t else 0 for i, a in enumerate(other_values)]
    ambiguous = decode(p, n, m, k, gamma, received, t, s)
    ambiguous["calibration_two_close_messages"] = [[0] * k, other]
    ambiguous["both_declared_close_words_recovered"] = all(
        any(c["polynomial_coefficients"] == message for c in ambiguous["candidates"])
        for message in ambiguous["calibration_two_close_messages"])
    native = []
    for row in rows:
        p, n, m, k = int(row["p_decimal"]), row["n_blocks"], row["m_fold"], row["decoded_dimension_k"]
        multipliers = dual_multipliers(p, row["points"])
        expected = [v*(a - evaluate(p, row["calibration_true_message"], x)) % p
                    for v, a, x in zip(multipliers, row["public_received_word"], row["points"])]
        K = n*m - k
        syn = vandermonde_syndrome(p, row["points"], expected, K)
        result = decode_syndrome(p, n, m, K, row["gamma"], syn, row["t_block_errors"], row["interpolation_order_s"])
        native.append({"calibration_true_error": expected,
                       "source_error_recovered": any(e["error_word"] == expected for e in result["verified_error_candidates"]), **result})
    return {"schema_version": "folded-rs-decoder-v1", "controls": rows,
            "ambiguous_whole_block_countercontrol": ambiguous,
            "native_syndrome_controls": native,
            "known_algorithm_not_a_new_quantum_candidate": True,
            "norm_character_source_or_quantum_receiver_implemented": False,
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "dependency_sha256": {name: hashlib.sha256((ROOT / "theorems" / name).read_bytes()).hexdigest()
                                  for name in ("bpqm_gibbs_frontier.py", "prime_character_capacity_source.py", "prime_character_opi.py")},
            "literature": ["https://eccc.weizmann.ac.il/report/2012/073/download/",
                           "https://eccc.weizmann.ac.il/report/2018/091/revision/1/download"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.write:
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"controls": [{"p": r["p_decimal"], "n": r["n_blocks"], "m": r["m_fold"],
                                   "t": r["t_block_errors"], "unique_radius": r["MDS_guaranteed_unique_block_radius"],
                                   "affine_dimension": len(r["affine_space"]["basis"]) if r["affine_space"] else None,
                                   "recovered": r["target_recovered"]} for r in report["controls"]],
                      "ambiguous_countercontrol": {key: report["ambiguous_whole_block_countercontrol"][key]
                                                   for key in ("affine_dimension", "both_declared_close_words_recovered", "list_completeness_certified")}}, indent=2))


if __name__ == "__main__":
    main()
