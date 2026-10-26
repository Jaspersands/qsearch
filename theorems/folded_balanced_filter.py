"""Proof certificates for a DIFFERENT, block-balanced inverse-trace relation.

No receiver/decoder implementation or quantum advantage is claimed. Small
field enumerations check trace-dual, additive-code and classical-attack
identities; native-size outputs are exact mathematical budgets only.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
from functools import lru_cache
import hashlib
from itertools import product
import json
from math import comb, prod
from pathlib import Path

from flint import fq_default_ctx

from theorems.balanced_filter_channel_audit import _fwht, exact_pattern_law

ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "research/FOLDED_BALANCED_FILTER.md"
REPORT = ROOT / "research/reductions/folded_balanced_filter.json"


def _integer(x, low, high, name):
    if type(x) is not int or not low <= x <= high:
        raise ValueError(f"{name} must be an integer in [{low}, {high}]")


def folded_parameters(bits, fold, length, dimension, radius, order):
    _integer(bits, 2, 4096, "base field bits")
    _integer(fold, 1, 256, "fold")
    _integer(length, 1, 10000, "block length")
    _integer(dimension, 1, fold*length-1, "scalar dimension")
    _integer(radius, 0, length-1, "block radius")
    _integer(order, 1, fold, "interpolation order")
    if fold*length >= 1 << bits:
        raise ValueError("need distinct nonzero scalar evaluation points")
    windows = fold-order+1
    degree = (length*windows-dimension+1)//(order+1)
    agreement = length-radius
    if degree < 0 or agreement*windows <= degree+dimension-1:
        raise ValueError("strict interpolation root count failed")
    threshold = Q(order, order+1)*(1-Q(dimension, length*windows))
    if Q(radius, length) >= threshold:
        raise ValueError("strict literature list-radius margin failed")
    zero_blocks = (dimension-1)//fold
    p = Q(agreement-zero_blocks, length)
    if p <= 0:
        raise ValueError("agreement does not force affine dimension reduction")
    # One deterministic block sequence has at most one output. Counting the
    # disjoint successful sequences gives a received-word-independent cap.
    lower = p**(order-1)
    fallback_cap = lower.denominator//lower.numerator
    if fallback_cap.bit_length() > bits*dimension:
        fallback_cap = min(fallback_cap, 1 << (bits*dimension))
    return {"bits": bits, "fold": fold, "length": length,
            "scalar_dimension": dimension, "block_rate": Q(dimension, fold*length),
            "radius": radius, "order": order, "interpolation_degree": degree,
            "strict_radius_threshold": threshold,
            "affine_dimension_cap": order-1, "zero_block_cap": zero_blocks,
            "per_candidate_sequence_success_lower": lower,
            "complete_pruning_sequence_count": length**(order-1),
            "fallback_list_cap": fallback_cap,
            "fallback_padding": 1 << (fallback_cap-1).bit_length(),
            "primitive_generator_list_cap": order,
            "primitive_generator_padding": 1 << (order-1).bit_length()}


def block_weight_enumerator(q, fold, length, dimension, beta):
    """Exact sum beta^block_weight(d) over nonzero scalar RS messages."""
    _integer(q, 2, 65536, "field size")
    _integer(fold, 1, 256, "fold")
    _integer(length, 1, 1000, "block length")
    _integer(dimension, 1, fold*length, "scalar dimension")
    if q & (q-1) or fold*length >= q:
        raise ValueError("binary field and distinct nonzero folded points required")
    beta = Q(beta)
    if not 0 <= beta <= 1:
        raise ValueError("beta must be a probability bound")
    return sum((comb(length, t)*(1-beta)**t*beta**(length-t)
                *(q**(dimension-fold*t)-1)
                for t in range(min(length, (dimension-1)//fold)+1)), Q(0))


def mersenne_prime_certificate(bits):
    """Lucas-Lehmer, not a factorization or a primitive-element oracle."""
    _integer(bits, 2, 127, "certificate exponent")
    if any(bits % d == 0 for d in range(2, int(bits**0.5)+1)):
        return False
    if bits == 2:
        return True
    modulus, value = (1 << bits)-1, 4
    for _ in range(bits-2):
        value = (value*value-2) % modulus
    return value == 0


def native_budget(bits, fold=67):
    length = bits*bits
    dimension = 3*fold*length//8
    radius = 51*length//100
    row = folded_parameters(bits, fold, length, dimension, radius, 8)
    # beta <= 2^(2-floor(ns/2)); adding 1/Q costs one further bit.
    exponent = bits*dimension + length*(3-(bits*fold)//2)
    tail = Q(sum(comb(length, j) for j in range(radius+1, length+1)), 1 << length)
    eta = Q(1, 1 << min(256, -exponent)) if exponent < 0 else None
    certified_prime = mersenne_prime_certificate(bits) if bits <= 127 else False
    padding = row["primitive_generator_padding"] if certified_prime else row["fallback_padding"]
    success = max(Q(0), (1-eta)*(1-tail)**2/padding) if eta is not None else Q(0)
    remaining = (dimension+fold-1)//fold
    return row | {"block_field_bits": bits*fold,
                  "eta_power_of_two_upper_exponent": exponent,
                  "eta_outward_rounded_upper": eta, "tail_exact": tail,
                  "base_multiplicative_order_is_prime_certified": certified_prime,
                  "public_irreducible_field_and_basis_still_required": True,
                  "padding_used": padding,
                  "native_success_per_attempt_lower": success,
                  "native_success_lower_exceeds_one_over_64": success > Q(1, 64),
                  "ideal_output_conditioned_on_native_success_is_uniform": True,
                  "classical_accepted_completion_remaining_blocks": remaining,
                  "classical_accepted_completion_success_lower": (1-eta)/(1 << remaining) if eta is not None else Q(0),
                  "classical_accepted_completion_expected_attempts_upper": (1 << remaining)/(1-eta) if eta is not None and eta < 1 else None,
                  "raw_value_register_bits": bits*fold*length,
                  "message_register_bits": bits*dimension,
                  "complete_pruning_executed": False, "native_receiver_executed": False,
                  "worst_case_classical_hardness_established": False}


def _solve(context, rows, rhs, columns):
    """Exact affine solve; explicit comparisons avoid FLINT's truthy zero."""
    if len(rows) != len(rhs) or any(len(row) != columns for row in rows):
        raise ValueError("linear-system dimensions disagree")
    matrix = [list(row)+[b] for row, b in zip(rows, rhs)]
    pivots, rank = [], 0
    for column in range(columns):
        pivot = next((i for i in range(rank, len(matrix)) if matrix[i][column] != 0), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inv = matrix[rank][column]**-1
        matrix[rank] = [v*inv for v in matrix[rank]]
        for i in range(len(matrix)):
            if i != rank and matrix[i][column] != 0:
                c = matrix[i][column]
                matrix[i] = [a-c*b for a, b in zip(matrix[i], matrix[rank])]
        pivots.append(column)
        rank += 1
    if any(all(v == 0 for v in row[:columns]) and row[-1] != 0 for row in matrix):
        return None
    offset = [context.zero() for _ in range(columns)]
    for i, column in enumerate(pivots):
        offset[column] = matrix[i][-1]
    return offset, rank


@lru_cache(maxsize=8, typed=True)
def _tower(bits, fold):
    _integer(bits, 2, 4, "finite reference base bits")
    _integer(fold, 1, 3, "finite reference fold")
    total = bits*fold
    if total > 8:
        raise ValueError("finite field-table reference cap exceeded")
    context = fq_default_ctx(2, total, "z")
    powers = [context.gen()**j for j in range(total)]
    values = [sum((p for j, p in enumerate(powers) if x >> j & 1), context.zero())
              for x in range(1 << total)]
    encode = lambda x: sum(int(c) << j for j, c in enumerate(x.to_list()))
    q = 1 << bits
    base = [v for v in values if v**q == v]
    gamma = next(v for v in base if v != 0 and len({encode(v**j) for j in range(q-1)}) == q-1)
    primal = [context.gen()**j for j in range(fold)]
    coordinate_map = {encode(sum((b*c for b, c in zip(primal, coords)), context.zero())): coords
                      for coords in product(base, repeat=fold)}
    if len(coordinate_map) != 1 << total:
        raise ArithmeticError("public primal basis does not span the extension")

    def relative_trace(x):
        result = context.zero()
        for _ in range(fold):
            result += x
            x = x**q
        return result

    gram = [[relative_trace(a*b) for b in primal] for a in primal]
    dual = []
    for j in range(fold):
        solved = _solve(context, gram, [context(int(i == j)) for i in range(fold)], fold)
        if solved is None or solved[1] != fold:
            raise ArithmeticError("degenerate trace Gram matrix")
        dual.append(sum((b*c for b, c in zip(primal, solved[0])), context.zero()))
    if any(relative_trace(a*b) != int(i == j)
           for i, a in enumerate(primal) for j, b in enumerate(dual)):
        raise ArithmeticError("incorrect dual basis")
    return context, values, base, gamma, primal, dual, coordinate_map, encode, relative_trace


def finite_block_control(bits, fold, length, dimension, radius):
    """Capped exhaustive identities, NOT an efficient folded decoder."""
    context, values, base, gamma, primal, dual, coords, enc, trace = _tower(bits, fold)
    q, alphabet = 1 << bits, 1 << (bits*fold)
    _integer(length, 1, 4, "finite block length")
    _integer(dimension, 1, fold*length-1, "finite scalar dimension")
    _integer(radius, 0, length-1, "finite radius")
    if fold*length >= q or alphabet**length > 4096 or alphabet**length*q**dimension > 300000:
        raise ValueError("finite additive-code reference cap exceeded")
    totalbits = bits*fold
    pack = lambda word: sum(v << (totalbits*i) for i, v in enumerate(word))
    words = [tuple((x >> (totalbits*i)) & (alphabet-1) for i in range(length))
             for x in range(alphabet**length)]
    points = [gamma**j for j in range(fold*length)]
    rows = [[x**j for x in points] for j in range(dimension)]
    code = []
    for coefficients in product(base, repeat=dimension):
        word = [sum((c*rows[j][i] for j, c in enumerate(coefficients)), context.zero())
                for i in range(fold*length)]
        # D uses the TRACE-DUAL of the native primal coordinate basis.
        code.append(pack(enc(sum((dual[j]*word[i*fold+j] for j in range(fold)), context.zero()))
                         for i in range(length)))
    if len(set(code)) != q**dimension:
        raise ArithmeticError("noninjective folded encoder")
    weights = [sum(x != 0 for x in word) for word in words]
    predicate = [0 if x == 0 else int((x**-1).trace()) for x in values]
    spectra = [[sum(1-2*int((u*x).trace()) for x, b in zip(values, predicate) if b == target)
                for u in values] for target in (0, 1)]
    trace_masks = [sum(int((x*context.gen()**j).trace()) << j for j in range(totalbits)) for x in values]
    fourier_indices = [pack(trace_masks[x] for x in word) for word in words]
    native, wrong_native = [], []
    for word in words:
        correct = [c for x in word for c in coords[x]]
        wrong = [trace(primal[j]*values[x]) for x in word for j in range(fold)]
        native.append(all(sum((a*b for a, b in zip(row, correct)), context.zero()) == 0 for row in rows))
        wrong_native.append(all(sum((a*b for a, b in zip(row, wrong)), context.zero()) == 0 for row in rows))
    character_native = [all(sum(int((values[x]*values[y]).trace())
                               for x, y in zip(word, words[d])) % 2 == 0 for d in code) for word in words]
    if native != character_native:
        raise ArithmeticError("trace-dual Fourier annihilator disagrees with native parity")
    zero_counts = [sum(all(words[d][i] == 0 for i in range(t)) for d in code)-1
                   for t in range(length+1)]
    expected = [q**max(0, dimension-fold*t)-1 for t in range(length+1)]
    if zero_counts != expected:
        raise ArithmeticError("scalar versus block rank mismatch")
    beta = Q(1, 3)
    enumerator = sum((beta**weights[d] for d in code if d != 0), Q(0))
    if enumerator != block_weight_enumerator(q, fold, length, dimension, beta):
        raise ArithmeticError("folded weighted enumerator mismatch")
    results = []
    fiber_counts = [0]*(1 << length)
    target_labels = [sum(predicate[x] << i for i, x in enumerate(word)) for word in words]
    for inside, label in zip(native, target_labels):
        if inside:
            fiber_counts[label] += 1
    for targets in product((0, 1), repeat=length):
        source = [prod(spectra[b][x] for b, x in zip(targets, word)) for word in words]
        source_scale = Q(1 << length, alphabet**(2*length))
        if source_scale*sum(v*v for v in source) != 1:
            raise ArithmeticError("block source lost balance")
        coalesced = [sum(source[z ^ d] for d in code) for z in range(len(words))]
        ball = [sum(source[z ^ d] for d in code if weights[z ^ d] <= radius) for z in range(len(words))]
        full_readout, ball_readout = _fwht(coalesced), _fwht(ball)
        scale = source_scale/(len(code)*len(words))
        valid = [inside and all(predicate[x] == b for x, b in zip(word, targets))
                 for inside, word in zip(native, words)]
        if any(full_readout[j] != 0 for j, good in zip(fourier_indices, valid) if not good):
            raise ArithmeticError("full coalescence has invalid native support")
        padding = len(code)  # PUBLIC exponential reference cap, no efficient-list assertion.
        success = scale*sum(ball_readout[j]**2 for j, good in zip(fourier_indices, valid) if good)/padding
        herald = source_scale*sum(v*v for v in ball)/(len(code)*padding)
        ball_mass = source_scale*sum(v*v for v, weight in zip(source, weights) if weight <= radius)
        if not 0 <= success <= herald <= ball_mass <= 1:
            raise ArithmeticError("unpaid projection probability")
        remaining = (dimension+fold-1)//fold
        partial_count = sum(inside and all(predicate[x] == b for x, b in zip(word[remaining:], targets[remaining:]))
                            for inside, word in zip(native, words))
        if partial_count*(1 << (length-remaining)) != sum(native):
            raise ArithmeticError("systematic free-block projection is not uniform")
        classical = Q(sum(valid), partial_count)
        full_norm = scale*sum(v*v for v in full_readout)
        if classical != full_norm/(1 << remaining):
            raise ArithmeticError("classical accepted-completion success formula failed")
        law = exact_pattern_law(targets, fiber_counts, len(code), len(words),
                                [int(s.bit_count() <= radius) for s in range(1 << length)], padding)
        target_label = sum(b << i for i, b in enumerate(targets))
        for j, inside, label in zip(fourier_indices, native, target_labels):
            expected = len(code)*len(words)*law["kernel"][target_label ^ label] if inside else 0
            if ball_readout[j] != expected:
                raise ArithmeticError("folded trace-dual readout violates exact pattern amplitude law")
        if success != law["native_success"] or herald != law["herald_probability"]:
            raise ArithmeticError("folded exact pattern probability law failed")
        results.append({"targets": targets, "reference_padding": padding,
                        "native_success": success, "herald": herald,
                        "projected_rejection": ball_mass-herald,
                        "full_native_norm": full_norm,
                        "classical_completion_remaining_blocks": remaining,
                        "classical_completion_conditioned_codewords": partial_count,
                        "classical_completion_success_exact": classical,
                        "predicate_pattern_probabilities_per_attempt": law["pattern_probabilities_per_attempt"],
                        "exact_pattern_amplitudes_checked": True,
                        "conditional_probability_per_native_witness": law["conditional_native_point_probability"]})
    code_set = set(code)
    not_extension_linear = any(pack(enc(a*values[x]) for x in words[d]) not in code_set
                               for a in values for d in code)
    return {"bits": bits, "fold": fold, "length": length, "dimension": dimension,
            "radius": radius, "extension_modulus": list(map(int, context.modulus().coeffs())),
            "base_gamma_in_extension": enc(gamma),
            "primal_basis": list(map(enc, primal)), "dual_basis": list(map(enc, dual)),
            "trace_dual_native_annihilator_checked": True,
            "wrong_basis_native_membership_disagreements": sum(a != b for a, b in zip(native, wrong_native)),
            "not_extension_field_linear": not_extension_linear,
            "zero_block_nonzero_message_counts": zero_counts,
            "weighted_enumerator_at_one_third": enumerator,
            "one_block_zero_fourier_probability": Q(1, 2),
            "old_scalar_predicates_folded_zero_probability": Q(1, 1 << fold),
            "all_targets": results, "efficient_decoder_executed": False}


def even_fold_classical_control(targets=(0, 0, 1)):
    """Native mixed-target completion using zero-target subfield freedoms."""
    context, values, base, gamma, primal, _, coords, enc, _ = _tower(3, 2)
    if len(targets) != 3 or any(type(b) is not int or b not in (0, 1) for b in targets):
        raise ValueError("three target bits required")
    dimension, fold = 2, 2
    accepted_one = next(x for x in values if x != 0 and int((x**-1).trace()) == 1)
    word = [context.zero() if b == 0 else accepted_one for b in targets]
    scalar = [c for x in word for c in coords[enc(x)]]
    points = [gamma**j for j in range(6)]
    parity = [[x**j for x in points] for j in range(dimension)]
    free = [i*fold for i, b in enumerate(targets) if b == 0]
    rhs = [-sum((a*b for a, b in zip(row, scalar)), context.zero()) for row in parity]
    solved = _solve(context, [[row[i] for i in free] for row in parity], rhs, len(free))
    row = {"targets": list(targets), "base_bits": 3, "fold": fold, "length": 3,
           "dimension": dimension, "zero_target_free_base_coordinates": len(free),
           "full_row_rank_guarantee": len(free) >= dimension,
           "status": "SUBFIELD_COMPLETION_INCONCLUSIVE", "classical_advantage_claim": False}
    if solved is None:
        return row
    for i, c in zip(free, solved[0]):
        scalar[i] += c
    word = [sum((primal[j]*scalar[i*fold+j] for j in range(fold)), context.zero()) for i in range(3)]
    checks = [0 if x == 0 else int((x**-1).trace()) for x in word]
    syndrome = [enc(sum((a*b for a, b in zip(r, scalar)), context.zero())) for r in parity]
    if checks != list(targets) or any(syndrome):
        raise ArithmeticError("subfield completion is not a native witness")
    return row | {"status": "CLASSICAL_NATIVE_WITNESS", "solution": list(map(enc, word)),
                  "syndrome": syndrome, "predicate_values": checks, "rank": solved[1],
                  "zero_subfield_elements_checked": len(base),
                  "zero_subfield_trace_identity_verified": all(x == 0 or int((x**-1).trace()) == 0 for x in base)}


def finite_pruning_control():
    """All block sequences on an ambiguous binary-field affine space.

    Exhaustive message enumeration is an independent comparison ONLY. It is
    not called by the received-block pruning loop.
    """
    context, _, base, gamma, _, _, _, enc, _ = _tower(3, 2)
    length, fold, dimension, agreement = 3, 2, 3, 2
    points = [gamma**j for j in range(length*fold)]
    evaluation = [[x**j for j in range(dimension)] for x in points]
    other = [(x-context.one())*(x-gamma) for x in points]
    received = [context.zero()]*4+other[4:]

    def matches(coefficients):
        prediction = [sum((a*b for a, b in zip(row, coefficients)), context.zero()) for row in evaluation]
        return sum(prediction[i*fold:(i+1)*fold] == received[i*fold:(i+1)*fold] for i in range(length))

    expected = {tuple(map(enc, coefficients)) for coefficients in product(base, repeat=dimension)
                if matches(coefficients) >= agreement}
    counts, failures = {}, {"inconsistent": 0, "rank_unresolved": 0, "outside_radius": 0}
    for sequence in product(range(length), repeat=dimension):
        rows, rhs, solved = [], [], None
        for block in sequence:
            rows.extend(evaluation[block*fold:(block+1)*fold])
            rhs.extend(received[block*fold:(block+1)*fold])
            solved = _solve(context, rows, rhs, dimension)
            if solved is None or solved[1] == dimension:
                break
        if solved is None:
            failures["inconsistent"] += 1
        elif solved[1] < dimension:
            failures["rank_unresolved"] += 1
        elif matches(solved[0]) < agreement:
            failures["outside_radius"] += 1
        else:
            label = tuple(map(enc, solved[0]))
            counts[label] = counts.get(label, 0)+1
    total = length**dimension
    floor = Q(agreement-(dimension-1)//fold, length)**dimension
    if set(counts) != expected or any(Q(c, total) < floor for c in counts.values()):
        raise ArithmeticError("deterministic block pruning omitted a close message")
    if sum(counts.values())+sum(failures.values()) != total:
        raise ArithmeticError("pruning lost failed sequences")
    return {"public_received_word": list(map(enc, received)), "points": list(map(enc, points)),
            "affine_dimension": dimension, "sequences_charged": total,
            "per_message_probability_floor": floor,
            "complete_list_matches_independent_enumeration": True,
            "results": [{"message": list(k), "successful_sequences": v} for k, v in sorted(counts.items())],
            "failed_sequences": failures, "field_enumeration_in_pruner": False,
            "exhaustive_reference_message_count": len(base)**dimension}


def _jsonable(x):
    if isinstance(x, Q):
        return [x.numerator, x.denominator]
    if isinstance(x, dict):
        return {k: _jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_jsonable(v) for v in x]
    return x


def build_report():
    paths = [Path(__file__), NOTE, ROOT / "research/BALANCED_FILTER_CHANNEL_AUDIT.md",
             ROOT / "theorems/balanced_filter_channel_audit.py", ROOT / "research/EXACT_PREDICATE_CHANNEL.md"]
    return _jsonable({"status": "FOLDED_BLOCK_RELATION_CONSTRUCTION_REVIEW_PENDING",
                      "source_hashes": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
                      "native_budgets": [native_budget(n) for n in (17, 31, 61)],
                      "finite_controls": [finite_block_control(*args) for args in
                                          ((3, 2, 2, 1, 1), (3, 2, 2, 2, 1), (2, 3, 1, 2, 0))],
                      "even_fold_classical_controls": [even_fold_classical_control(t) for t in product((0, 1), repeat=3)],
                      "complete_pruning_control": finite_pruning_control(),
                      "external_dependencies": [
                          {"url": "https://arxiv.org/html/2408.15925v3", "use": "sharp list cap with verified primitive generator and strict radius"},
                          {"url": "https://arxiv.org/html/2508.12548v2", "use": "known deterministic bit-polynomial pruning alternative, not implemented"},
                          {"url": "https://eccc.weizmann.ac.il/report/2012/073/", "use": "known affine folded interpolation"},
                          {"url": "https://eccc.weizmann.ac.il/report/2018/091/", "use": "received-block pruning argument"}],
                      "not_a_new_decoder": True, "native_quantum_execution": False,
                      "classical_hardness": False, "same_as_old_scalar_problem": False})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write:
        REPORT.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"status": report["status"], "native_receiver_executed": False,
                      "finite_target_controls": sum(len(r["all_targets"]) for r in report["finite_controls"]),
                      "even_fold_classical_witnesses": sum(r["status"] == "CLASSICAL_NATIVE_WITNESS" for r in report["even_fold_classical_controls"])}))
