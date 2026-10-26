"""Exact register-level audit of the existing balanced codeword filter.

This is a capped exponential mathematical reference, not circuit search or a
scalable receiver. It uses independent FLINT arithmetic, explicit messages and
retained records instead of assuming a physical implementation of coalescence.
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


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/reductions/balanced_filter_channel_audit.json"
NOTE = ROOT / "research/BALANCED_FILTER_CHANNEL_AUDIT.md"


def _integer(value, low, high, name):
    if type(value) is not int or not low <= value <= high:
        raise ValueError(f"{name} must be an integer in [{low}, {high}]")


def _fwht(values):
    values = list(values)
    width = 1
    while width < len(values):
        for start in range(0, len(values), 2*width):
            for j in range(start, start+width):
                a, b = values[j], values[j+width]
                values[j], values[j+width] = a+b, a-b
        width *= 2
    return values


@lru_cache(maxsize=12, typed=True)
def _fixture(bits, length, dimension, radius):
    _integer(bits, 2, 4, "reference field bits")
    q = 1 << bits
    _integer(length, 2, q, "reference length")
    _integer(dimension, 1, length-1, "reference dimension")
    _integer(radius, 0, length-1, "reference radius")
    size, messages = q**length, q**dimension
    if size > 4096 or size*messages > 131_072:
        raise ValueError("exponential channel reference cap exceeded")
    context = fq_default_ctx(2, bits, "z")
    powers = [context.gen()**j for j in range(bits)]
    values = [sum((power for j, power in enumerate(powers) if x >> j & 1), context.zero())
              for x in range(q)]
    encode = lambda x: sum(int(c) << j for j, c in enumerate(x.to_list()))
    pack = lambda xs: sum(x << (bits*i) for i, x in enumerate(xs))
    words = tuple(tuple((x >> (bits*i)) & (q-1) for i in range(length)) for x in range(size))
    predicate = tuple(0 if x == 0 else int((x**-1).trace()) for x in values)
    chars = tuple(tuple(1-2*int((u*x).trace()) for x in values) for u in values)
    spectra = tuple(tuple(sum(char[x] for x in range(q) if predicate[x] == b)
                          for char in chars) for b in (0, 1))
    rows = tuple(tuple(values[i]**j for i in range(length)) for j in range(dimension))
    code = tuple(pack(encode(sum((values[c]*rows[j][i] for j, c in enumerate(coeffs)), context.zero()))
                      for i in range(length)) for coeffs in product(range(q), repeat=dimension))
    if len(set(code)) != messages or any(code[a ^ b] != code[a] ^ code[b]
                                       for a in range(messages) for b in range(messages)):
        raise ArithmeticError("message encoder is not injective binary linear")
    weights = tuple(sum(x != 0 for x in word) for word in words)
    supports = tuple(sum((x != 0) << i for i, x in enumerate(word)) for word in words)
    lists = tuple(tuple(m for m, d in enumerate(code) if weights[z ^ d] <= radius)
                  for z in range(size))
    trace_masks = tuple(sum(int((x*p).trace()) << j for j, p in enumerate(powers)) for x in values)
    dual_indices = tuple(pack(trace_masks[x] for x in word) for word in words)
    if len(set(dual_indices)) != size:
        raise ArithmeticError("trace-pairing readout is not a permutation")
    native_code = tuple(all(sum((row[i]*values[x] for i, x in enumerate(word)), context.zero()) == 0
                            for row in rows) for word in words)
    target_masks = tuple(sum(predicate[x] << i for i, x in enumerate(word)) for word in words)
    return {"q": q, "size": size, "messages": messages, "words": words,
            "spectra": spectra, "code": code, "weights": weights, "supports": supports,
            "lists": lists, "dual": dual_indices, "native_code": native_code,
            "target_masks": target_masks,
            "modulus": tuple(map(int, context.modulus().coeffs()))}


def _fraction(value):
    return [value.numerator, value.denominator]


def exact_pattern_law(targets, fiber_counts, message_count, ambient_size, mask, padding):
    """Exact balanced support-subspace identity, NOT a free quantum channel.

    The physical caller must separately certify complete lists, a legal
    support filter and fixed padding. This calculation can expose impossible
    probabilities if those access/normalization premises are omitted.
    """
    targets, fiber_counts, mask = tuple(targets), tuple(fiber_counts), tuple(mask)
    _integer(len(targets), 1, 16, "finite pattern count exponent")
    patterns = 1 << len(targets)
    if any(type(b) is not int or b not in (0, 1) for b in targets):
        raise ValueError("binary target pattern required")
    if len(fiber_counts) != patterns or any(type(c) is not int or c < 0 for c in fiber_counts):
        raise ValueError("one nonnegative integer count per predicate pattern required")
    for value in (message_count, ambient_size, padding):
        if type(value) is not int or value < 1:
            raise ValueError("positive integer dimensions required")
    if ambient_size % patterns or message_count*sum(fiber_counts) != ambient_size:
        raise ValueError("fiber counts do not partition the native annihilator")
    if padding & (padding-1) or padding > message_count:
        raise ValueError("fixed padding must be a power of two within the message space")
    if len(mask) != patterns or any(type(m) not in (int, Q) or abs(m) > 1 for m in mask):
        raise ValueError("one rational support-mask amplitude of magnitude at most one required")
    kernel = [Q(k, patterns) for k in _fwht(mask)]
    lambdas = [Q(message_count*patterns*c, ambient_size) for c in fiber_counts]
    target = sum(b << i for i, b in enumerate(targets))
    masses = [lam*kernel[target ^ c]**2/padding for c, lam in enumerate(lambdas)]
    return {"kernel": kernel, "relative_fiber_counts": lambdas,
            "pattern_probabilities_per_attempt": masses,
            "herald_probability": sum(masses), "native_success": masses[target],
            "invalid_success": sum(masses)-masses[target],
            "source_filter_mass": sum(Q(m)**2 for m in mask)/patterns,
            "relative_gram_error": max(abs(lam-1) for lam in lambdas),
            "conditional_native_point_probability": Q(1, fiber_counts[target]) if masses[target] else None}


def projection_size(length, dimension, radius, message_count):
    """PUBLIC Johnson cap, not an enumerated or received-word-dependent size."""
    _integer(length, 2, 100_000, "length")
    _integer(dimension, 1, length-1, "dimension")
    _integer(radius, 0, length-1, "radius")
    if type(message_count) is not int or message_count < 2 or message_count & (message_count-1):
        raise ValueError("binary message count must be a positive power of two greater than one")
    agreement = length-radius
    gap = agreement*agreement-length*(dimension-1)
    cap = min(message_count, length*(agreement-dimension+1)//gap) if gap > 0 else message_count
    return 1 << (cap-1).bit_length()


def list_projection_budget(bits, length, dimension, radius):
    """Native inverse-trace bound WITHOUT a point-mass/ambiguity premise."""
    from theorems.inverse_trace_gibbs_target import reciprocal_bound

    beta, eta = reciprocal_bound(bits, length, dimension)
    _integer(radius, 0, length-1, "radius")
    if (length-radius)**2 <= length*(dimension-1):
        raise ValueError("polynomial complete-list guarantee requires strict Johnson agreement")
    padding = projection_size(length, dimension, radius, (1 << bits)**dimension)
    tail = Q(sum(comb(length, j) for j in range(radius+1, length+1)), 1 << length)
    retained = 1-tail
    lower = max(Q(0), (1-eta)*retained**2/padding)
    return {"bits": bits, "length": length, "dimension": dimension, "radius": radius,
            "padding": padding, "beta": beta, "eta": eta, "tail": tail,
            "native_success_per_attempt_lower": lower,
            "invalid_success_per_attempt_upper": min(Q(1), (1+eta)*retained*tail/padding),
            "success_bound": "EXACT_TARGET_FIBER_TIMES_RETAINED_MASS_SQUARED_OVER_PADDING",
            "ideal_output_conditioned_on_native_success_is_uniform": True,
            "uses_unique_decoding_assumption": False,
            "uses_nonzero_symbol_point_mass_assumption": False}


def audit_instance(bits, length, dimension, radius, targets, native_offset=None):
    targets = tuple(targets)
    if len(targets) != length or any(type(b) is not int or b not in (0, 1) for b in targets):
        raise ValueError("one target bit per coordinate required")
    data = _fixture(bits, length, dimension, radius)
    q, size, messages = data["q"], data["size"], data["messages"]
    offset = (0,)*length if native_offset is None else tuple(native_offset)
    if len(offset) != length or any(type(x) is not int or not 0 <= x < q for x in offset):
        raise ValueError("one canonical field label per native offset coordinate required")
    offset_label = sum(x << (bits*i) for i, x in enumerate(offset))
    offset_dual = data["dual"][offset_label]
    source = [prod(data["spectra"][b][x] for b, x in zip(targets, word)) for word in data["words"]]
    # Translate accepted roots by the public offset BEFORE Fourier preparation.
    source = [a*(1-2*((e & offset_dual).bit_count() & 1)) for e, a in enumerate(source)]
    output_patterns = tuple(data["target_masks"][x ^ offset_label] for x in range(size))
    source_scale = Q(1 << length, q**(2*length))
    scale = source_scale/messages
    if source_scale*sum(a*a for a in source) != 1:
        raise ArithmeticError("root-product Fourier source is not normalized")
    modes = ("clean", "which_message", "exact_weight", "exact_support", "phase_stripped", "incomplete_list")
    branches = {mode: {} for mode in modes}
    padding = projection_size(length, dimension, radius, messages)
    padded_lists = []
    for candidates in data["lists"]:
        if len(candidates) > padding:
            raise ArithmeticError("complete list exceeds the PUBLIC padding cap")
        padded = list(candidates)
        for message in range(padding):
            if len(padded) == padding:
                break
            if message not in padded:
                padded.append(message)
        if len(padded) != padding or len(set(padded)) != padding:
            raise ArithmeticError("list padding is not an injective lookup")
        padded_lists.append(tuple(padded))
    projection_branches = [[0]*size for _ in range(padding)]

    def add(mode, record, z, amplitude):
        branch = branches[mode].get(record)
        if branch is None:
            branch = branches[mode][record] = [0]*size
        branch[z] += amplitude

    erased_basis_branches = 0
    for e, amplitude in enumerate(source):
        if data["weights"][e] > radius:
            continue
        for message, d in enumerate(data["code"]):
            z = e ^ d
            candidates = data["lists"][z]
            if message not in candidates:
                raise ArithmeticError("complete radius list omitted original message")
            # Invert the list lookup, apply H^log2(P), retain ALL outcomes.
            index = padded_lists[z].index(message)
            for outcome in range(padding):
                projection_branches[outcome][z] += amplitude*(1-2*((index & outcome).bit_count() & 1))
            # Deliberately faulty list truncation, with its residual STILL retained.
            add("incomplete_list", message ^ candidates[0], z, amplitude)
            if len(candidates) != 1:
                continue
            residual = message ^ candidates[0]
            if residual:
                raise ArithmeticError("complete-singleton erasure left an original message")
            erased_basis_branches += 1
            add("clean", residual, z, amplitude)
            add("which_message", message, z, amplitude)
            add("exact_weight", data["weights"][e], z, amplitude)
            add("exact_support", data["supports"][e], z, amplitude)
            add("phase_stripped", residual, z, abs(amplitude))

    retained = [a if data["weights"][e] <= radius and len(data["lists"][e]) == 1 else 0
                for e, a in enumerate(source)]
    predicted = [sum(retained[z ^ d] for d in data["code"]) for z in range(size)]
    clean = branches["clean"].get(0, [0]*size)
    if clean != predicted:
        raise ArithmeticError("explicit register operations differ from the claimed coalesced state")
    good_mass = source_scale*sum(a*a for a in retained)
    ball_mass = source_scale*sum(a*a for e, a in enumerate(source) if data["weights"][e] <= radius)
    projected = projection_branches[0]
    expected_ball = [sum(source[z ^ d] for d in data["code"] if data["weights"][z ^ d] <= radius)
                     for z in range(size)]
    if projected != expected_ball:
        raise ArithmeticError("padded-list projection did not coherently retain the full ball")
    projection_scale = scale/padding
    projection_mass = projection_scale*sum(a*a for a in projected)
    projection_rejected = projection_scale*sum(a*a for values in projection_branches[1:] for a in values)
    if projection_mass+projection_rejected != ball_mass:
        raise ArithmeticError("list projection hid postselection probability")
    bmask = sum(b << i for i, b in enumerate(targets))
    valid = tuple(in_code and target == bmask for in_code, target in zip(data["native_code"], output_patterns))
    summary, readouts = {}, {}
    for mode, records in branches.items():
        transformed = [_fwht(values) for values in records.values()]
        readout = [sum(values[j]**2 for values in transformed) for j in range(size)]
        readouts[mode] = readout
        herald = scale*sum(a*a for values in records.values() for a in values)
        expected = ball_mass if mode == "incomplete_list" else good_mass
        if herald != expected or scale*sum(readout)/size != herald:
            raise ArithmeticError("stage probability ledger lost mass")
        parity_mass = scale*sum(readout[j] for j, in_code in zip(data["dual"], data["native_code"]) if in_code)/size
        native_mass = scale*sum(readout[j] for j, accepted in zip(data["dual"], valid) if accepted)/size
        summary[mode] = {"herald_probability": _fraction(herald),
                         "parity_valid_probability_per_attempt": _fraction(parity_mass),
                         "native_valid_probability_per_attempt": _fraction(native_mass),
                         "conditional_native_probability": _fraction(native_mass/herald) if herald else None,
                         "retained_record_count": len(records)}
    if any(readouts["clean"][j] != 0 for j, in_code in zip(data["dual"], data["native_code"]) if not in_code):
        raise ArithmeticError("clean erasure failed to enforce native code membership")
    if any(readouts["clean"][j] != messages*readouts["which_message"][j]
           for j, in_code in zip(data["dual"], data["native_code"]) if in_code):
        raise ArithmeticError("which-codeword penalty identity failed")
    false_residual = scale*sum(a*a for residual, values in branches["incomplete_list"].items()
                               if residual for a in values)
    projected_readout = _fwht(projected)
    if any(projected_readout[j] for j, in_code in zip(data["dual"], data["native_code"]) if not in_code):
        raise ArithmeticError("padded-list projection lost native code membership")
    projection_native = projection_scale*sum(projected_readout[j]**2 for j, accepted in zip(data["dual"], valid) if accepted)/size
    if projection_scale*sum(x*x for x in projected_readout)/size != projection_mass:
        raise ArithmeticError("padded-list Fourier normalization failed")
    fiber_counts = [0]*(1 << length)
    for inside, pattern in zip(data["native_code"], output_patterns):
        if inside:
            fiber_counts[pattern] += 1
    mask = [int(s.bit_count() <= radius) for s in range(1 << length)]
    law = exact_pattern_law(targets, fiber_counts, messages, size, mask, padding)
    for j, inside, pattern in zip(data["dual"], data["native_code"], output_patterns):
        expected_amplitude = messages*size*law["kernel"][bmask ^ pattern] if inside else 0
        if projected_readout[j] != expected_amplitude:
            raise ArithmeticError("physical full-list amplitude violates exact predicate-pattern law")
    if projection_native != law["native_success"] or projection_mass != law["herald_probability"]:
        raise ArithmeticError("physical full-list probability violates exact predicate-pattern law")
    summary["padded_list_projection"] = {
        "herald_probability": _fraction(projection_mass),
        "parity_valid_probability_per_attempt": _fraction(projection_mass),
        "native_valid_probability_per_attempt": _fraction(projection_native),
        "conditional_native_probability": _fraction(projection_native/projection_mass) if projection_mass else None,
        "public_padding": padding,
        "projection_rejected_probability": _fraction(projection_rejected),
        "weight_rejected_probability": _fraction(1-ball_mass),
        "unpaid_coalesced_ball_norm_squared": _fraction(projection_mass*padding),
        "all_projection_outcomes_accounted": True,
        "predicate_pattern_probabilities_per_attempt": list(map(_fraction, law["pattern_probabilities_per_attempt"])),
        "relative_predicate_fiber_counts": list(map(_fraction, law["relative_fiber_counts"])),
        "exact_pattern_amplitudes_checked": True,
        "ideal_native_conditional_uniformity_checked": True,
        "conditional_probability_per_native_witness": _fraction(law["conditional_native_point_probability"]) if law["conditional_native_point_probability"] is not None else None,
        "retained_record_count": 1}
    return {"bits": bits, "length": length, "dimension": dimension, "radius": radius,
            "targets": list(targets), "field_modulus_coefficients": list(data["modulus"]),
            "public_native_offset": list(offset),
            "output_coset": "PUBLIC_OFFSET_PLUS_NATIVE_ANNIHILATOR",
            "offset_source_phase_and_final_translation_charged": True,
            "evaluation_points": list(range(length)), "enumerated_error_words": size,
            "enumerated_messages": messages, "erased_basis_branches": erased_basis_branches,
            "maximum_complete_list_size": max(map(len, data["lists"])),
            "within_strict_gs_radius": (length-radius)**2 > length*(dimension-1),
            "native_witness_count": sum(valid), "channels": summary,
            "incomplete_list_nonzero_message_residual_mass": _fraction(false_residual),
            "which_codeword_probability_penalty_exact": messages,
            "code_projection_from_clean_register_operations_checked": True,
            "decoder": "EXHAUSTIVE_INDEPENDENT_REFERENCE_NOT_GS",
            "native_large_receiver_executed": False,
            "reference_has_polynomial_complexity": False}


def report():
    from theorems.inverse_trace_gibbs_target import _ceil_log2, _floor

    cases = [(2, 3, 2, 1), (3, 4, 1, 2), (4, 3, 1, 1)]
    rows = [audit_instance(*case, targets) for case in cases
            for targets in product((0, 1), repeat=case[1])]
    affine_rows = [audit_instance(2, 3, 2, 1, targets, (a, b, 0))
                   for a, b in product(range(4), repeat=2)
                   for targets in product((0, 1), repeat=3)]
    budgets = []
    for n in (17, 31, 61):
        row = list_projection_budget(n, n*n, n*n//8, 3*n*n//5)
        success_lower = Q(*_floor(row["native_success_per_attempt_lower"]))
        budgets.append({"bits": n, "length": n*n, "dimension": n*n//8,
                        "radius": 3*n*n//5, "padding": row["padding"],
                        "native_success_per_attempt_lower": _fraction(success_lower),
                        "invalid_success_per_attempt_power2_upper": _ceil_log2(row["invalid_success_per_attempt_upper"]),
                        "failure_after_128_fresh_attempts_power2_upper": _ceil_log2((1-success_lower)**128),
                        "uses_unique_decoding_assumption": False,
                        "uses_nonzero_symbol_point_mass_assumption": False,
                        "ideal_output_conditioned_on_native_success_is_uniform": True,
                        "native_large_receiver_executed": False})
    return {"status": "REGISTER_COMPOSITION_AND_PAID_FULL_LIST_PROJECTION_REVIEW_PENDING",
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "proof_sha256": hashlib.sha256(NOTE.read_bytes()).hexdigest(),
            "upstream_proof_sha256": hashlib.sha256((ROOT / "research/BALANCED_CODEWORD_FILTER.md").read_bytes()).hexdigest(),
            "mds_bound_source_sha256": hashlib.sha256((ROOT / "theorems/inverse_trace_gibbs_target.py").read_bytes()).hexdigest(),
            "independent_external_proof_review_complete": False,
            "independent_repository_review_incorporated": "research/independent_review_2026_10_22/EXACT_PATTERN_CHANNEL.md",
            "exact_pattern_proof_sha256": hashlib.sha256((ROOT / "research/EXACT_PREDICATE_CHANNEL.md").read_bytes()).hexdigest(),
            "classical_hardness_established": False,
            "scalable_receiver_implemented": False,
            "all_target_inputs_checked": len(rows), "full_list_native_budgets": budgets, "controls": rows,
            "affine_target_syndrome_pairs_checked": len(affine_rows),
            "affine_controls": affine_rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    data = report()
    if args.write:
        REPORT.write_text(json.dumps(data, indent=2)+"\n")
    print(json.dumps({"status": data["status"], "all_target_inputs_checked": data["all_target_inputs_checked"],
                      "affine_target_syndrome_pairs_checked": data["affine_target_syndrome_pairs_checked"],
                      "incomplete_list_fault_detected": any(Q(*r["incomplete_list_nonzero_message_residual_mass"]) > 0
                                                            for r in data["controls"])}, indent=2))


if __name__ == "__main__":
    main()
