"""Exact certificates for a balanced-predicate codeword filter.

Known decoded-interference mechanism; the per-instance tail argument is a
local derivation awaiting review. Dense controls are exponentially bounded,
not a scalable quantum decoder. See BALANCED_CODEWORD_FILTER.md.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import product
import hashlib
import json
from math import comb, isqrt, log2, prod
from pathlib import Path

from theorems.explicit_quadratic_opi import element, encoded, field
from theorems.parity_block_usd_prange import affine_system


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/reductions/balanced_codeword_filter.json"


def integer(value, minimum, maximum, name):
    if type(value) is not int or not minimum <= value <= maximum:
        raise ValueError(f"{name} must be an integer in [{minimum}, {maximum}]")


def reciprocal_trace(bits, word):
    integer(bits, 1, 256, "field bits")
    integer(word, 0, (1 << bits)-1, "field element")
    x = element(bits, word)
    return int((x**-1).trace()) if word else 0


def trace_mask(bits, word):
    x = element(bits, word)
    return sum(int((x*element(bits, 1 << j)).trace()) << j for j in range(bits))


def root_spectrum(bits, target):
    """Bounded exact b(u)=sum_{f(x)=target} (-1)^Tr(ux), NOT amplitudes."""
    integer(bits, 1, 6, "reference field bits")
    integer(target, 0, 1, "target bit")
    q = 1 << bits
    roots = tuple(x for x in range(q) if reciprocal_trace(bits, x) == target)
    masks = tuple(trace_mask(bits, u) for u in range(q))
    spectrum = tuple(sum((-1)**((mask & x).bit_count() & 1) for x in roots)
                     for mask in masks)
    assert len(roots) == q//2
    return roots, spectrum


def nonzero_pair_residual(spectrum, displacement):
    """The cancellation is integer-exact, before any square-root normalization."""
    q = len(spectrum)
    integer(displacement, 1, q-1, "nonzero displacement")
    return sum(spectrum[u]*spectrum[u ^ displacement]
               for u in range(q) if u not in (0, displacement))


def filter_budget(bits, length, dimension, radius):
    """Rational sufficient bounds; no field/code/error table is constructed.

    D is the LOW-rate [length, dimension] RS decoder code. Native answers
    lie in C=D^perp. The failure bound excludes gate/decoder compilation
    error, which must be budgeted separately.
    """
    integer(bits, 2, 256, "field bits")
    q = 1 << bits
    integer(length, 2, min(q, 100_000), "RS length")
    integer(dimension, 1, length-1, "decoder dimension")
    integer(radius, 0, length-1, "decoder radius")
    agreement = length-radius
    johnson = agreement**2-length*(dimension-1)
    if johnson <= 0:
        raise ValueError("strict Johnson agreement is required")
    list_cap = length*(agreement-dimension+1)//johnson
    if dimension == 1:
        multiplicity, monomials, constraints = 0, 0, 0
    else:
        multiplicity = length*(dimension-1)//johnson+1
        weighted_degree = multiplicity*agreement-1
        y_degree = weighted_degree//(dimension-1)
        monomials = (y_degree+1)*(weighted_degree+1)-(dimension-1)*y_degree*(y_degree+1)//2
        constraints = length*multiplicity*(multiplicity+1)//2
        assert monomials > constraints
    distance = length-dimension+1
    required_hits = agreement-dimension+1
    tail = Fraction(sum(comb(length, j) for j in range(radius+1, length+1)), 1 << length)
    # inv(0)=0 adds 1 to the nonzero-domain Kloosterman sum.
    ceil_sqrt_q = isqrt(q)
    ceil_sqrt_q += int(ceil_sqrt_q**2 != q)
    beta = min(Fraction(1), Fraction(1+2*ceil_sqrt_q, q))
    point_mass = min(Fraction(1, 2), Fraction(4, q))
    coherence = (q**dimension-1)*beta**distance
    ambiguity = min(Fraction(1), (q**dimension-1)*comb(length, required_hits)
                    *point_mass**required_hits)
    herald_lower = max(Fraction(0), 1-tail-ambiguity)
    failure = min(Fraction(1), 3*tail+(2*list_cap+1)*ambiguity+2*coherence)
    return {"bits": bits, "length": length, "decoder_dimension": dimension,
            "native_dimension": length-dimension, "radius": radius,
            "agreement": agreement, "distance": distance,
            "list_cap": list_cap, "required_nonzero_hits": required_hits,
            "gs_multiplicity": multiplicity, "gs_interpolation_monomials": monomials,
            "gs_interpolation_constraints": constraints,
            "beta_upper": beta, "nonzero_point_mass_upper": point_mass,
            "tail_mass": tail, "coherent_tail_excess": coherence,
            "ambiguous_mass_upper": ambiguity, "herald_lower": herald_lower,
            "ideal_arithmetic_failure_upper": failure,
            "full_quantum_receiver_implemented": False,
            "classical_hardness_established": False,
            "independently_verified": False}


def _fwht(values):
    result = list(values)
    step = 1
    while step < len(result):
        for start in range(0, len(result), 2*step):
            for j in range(start, start+step):
                left, right = result[j], result[j+step]
                result[j], result[j+step] = left+right, left-right
        step *= 2
    return result


def native_word(bits, packed, length):
    return tuple((packed >> (bits*i)) & ((1 << bits)-1) for i in range(length))


def _pack(bits, values):
    return sum(value << (bits*i) for i, value in enumerate(values))


def reference_control(bits=3, length=4, dimension=1, radius=2, targets=None):
    """Full finite linear-code coalescence, herald and native Fourier readout.

    Enumerates q^length and q^dimension. Never used by filter_budget or by
    the claimed scalable circuit. All quantities except report logs are exact.
    """
    integer(bits, 2, 6, "reference bits")
    q = 1 << bits
    integer(length, 2, q, "reference length")
    integer(dimension, 1, length-1, "reference dimension")
    integer(radius, 0, length-1, "reference radius")
    size = q**length
    if size > 65536 or size*q**dimension > 2_000_000:
        raise ValueError("exponential reference cap exceeded")
    targets = tuple(i % 2 for i in range(length)) if targets is None else tuple(targets)
    if len(targets) != length or any(type(b) is not int or b not in (0, 1) for b in targets):
        raise ValueError("one native target bit per coordinate required")
    spectra = [root_spectrum(bits, b)[1] for b in targets]
    points = [element(bits, i) for i in range(length)]
    rows = [[x**j for x in points] for j in range(dimension)]
    code = []
    for coefficients in product(range(q), repeat=dimension):
        code.append(_pack(bits, [encoded(sum((element(bits, c)*rows[j][i]
                                              for j, c in enumerate(coefficients)), field(bits).zero()))
                                for i in range(length)]))
    words = [native_word(bits, packed, length) for packed in range(size)]
    weights = [sum(x != 0 for x in word) for word in words]
    amplitude = [prod(spectra[i][x] for i, x in enumerate(word)) for word in words]
    source_scale = Fraction(2**length, q**(2*length))
    assert source_scale*sum(x*x for x in amplitude) == 1
    list_sizes = [sum(weights[packed ^ d] <= radius for d in code) for packed in range(size)]
    good = [weight <= radius and list_sizes[j] == 1 for j, weight in enumerate(weights)]

    def coalesce(values):
        return [sum(values[j ^ d] for d in code) for j in range(size)]

    def norm(values):
        return source_scale*sum(x*x for x in values)/len(code)

    full = coalesce(amplitude)
    selected = coalesce([a if good[j] else 0 for j, a in enumerate(amplitude)])
    good_mass = source_scale*sum(a*a for j, a in enumerate(amplitude) if good[j])
    tail_mass = source_scale*sum(a*a for j, a in enumerate(amplitude) if weights[j] > radius)
    ambiguous_mass = 1-tail_mass-good_mass
    ball = coalesce([a if weights[j] <= radius else 0 for j, a in enumerate(amplitude)])
    assert norm(selected) == good_mass
    beta = max(Fraction(2*abs(b), q) for spectrum in spectra for b in spectrum[1:])
    distance = min(weights[d] for d in code if d)
    excess = (len(code)-1)*beta**distance
    mask_rows = []
    # Non-radial support parity is included; label-dependent masks are NOT legal.
    masks = [lambda word, w=w: sum(x != 0 for x in word) > w for w in range(length+1)]
    masks += [lambda word: bool((word[0] != 0) ^ (word[-1] != 0))]
    for mask in masks:
        retained = [a if mask(words[j]) else 0 for j, a in enumerate(amplitude)]
        mass = source_scale*sum(a*a for a in retained)
        image_norm = norm(coalesce(retained))
        assert abs(image_norm-mass) <= excess
        mask_rows.append({"source_mass": mass, "coalesced_norm_squared": image_norm})

    full_readout, selected_readout = _fwht(full), _fwht(selected)
    masks_by_element = [trace_mask(bits, x) for x in range(q)]
    valid_weight, valid_count = 0, 0
    for packed, word in enumerate(words):
        valid = all(reciprocal_trace(bits, x) == targets[i] for i, x in enumerate(word))
        valid = valid and all(sum((rows[j][i]*element(bits, x) for i, x in enumerate(word)),
                                 field(bits).zero()) == 0 for j in range(dimension))
        dual = _pack(bits, [masks_by_element[x] for x in word])
        assert full_readout[dual] == (len(code)*size if valid else 0)
        if valid:
            valid_count += 1
            valid_weight += selected_readout[dual]**2
    unconditional_valid = source_scale*valid_weight/(len(code)*size)
    stripped_norm = norm(coalesce([abs(a) for a in amplitude]))
    return {"bits": bits, "length": length, "dimension": dimension, "radius": radius,
            "field_modulus_coefficients": list(map(int, field(bits).modulus().coeffs())),
            "evaluation_points": list(range(length)),
            "targets": targets, "enumerated_error_words": size, "enumerated_codewords": len(code),
            "valid_native_witness_count": valid_count, "herald_probability": good_mass,
            "tail_probability": tail_mass, "ambiguous_source_mass": ambiguous_mass,
            "maximum_complete_list_size": max(list_sizes),
            "retained_ball_mass": 1-tail_mass, "retained_ball_coalesced_norm_squared": norm(ball),
            "valid_output_probability_per_attempt": unconditional_valid,
            "conditional_valid_probability": unconditional_valid/good_mass if good_mass else None,
            "full_filter_norm_squared": norm(full), "support_mask_excess_bound": excess,
            "support_mask_controls": mask_rows, "phase_stripped_norm_squared": stripped_norm,
            "decoder": "EXHAUSTIVE_FINITE_REFERENCE_NOT_GURUSWAMI_SUDAN"}


def projective_line_attack(bits, points, dimension, vector, targets):
    """Solve x=t*v through linear equations in u=1/t, with native verification.

    v is a supplied PUBLIC codeword in ker(Vandermonde). Failure only rules
    out this one projective line, never the original instance.
    """
    integer(bits, 2, 256, "field bits")
    q = 1 << bits
    points, vector, targets = tuple(points), tuple(vector), tuple(targets)
    if not len(points) == len(vector) == len(targets) or len(set(points)) != len(points):
        raise ValueError("distinct points and aligned native words required")
    integer(dimension, 1, len(points)-1, "parity-check dimension")
    for value in points+vector:
        integer(value, 0, q-1, "field element")
    for b in targets:
        integer(b, 0, 1, "target bit")
    if not any(vector):
        raise ValueError("nonzero public codeword required")
    if any(sum((element(bits, a)**j*element(bits, v) for a, v in zip(points, vector)),
               field(bits).zero()) != 0 for j in range(dimension)):
        raise ValueError("the supplied direction is not in the native code")
    equations = []
    for v, b in zip(vector, targets):
        inverse = encoded(element(bits, v)**-1) if v else 0
        equations.append((trace_mask(bits, inverse), b))
    system = affine_system(equations, bits)
    if not system["consistent"]:
        return {"status": "NO_WITNESS_ON_THIS_LINE", "rank": system["rank"]}

    def solution(free_word):
        value = free_word
        for row in system["rref"]:
            if any(row[:-1]):
                pivot = next(j for j, x in enumerate(row[:-1]) if x)
                bit = row[-1] ^ (sum(x*((value >> j) & 1) for j, x in enumerate(row[:-1])) & 1)
                value ^= bit << pivot
        return value

    u = solution(0)
    if not u and system["free"]:
        u = solution(1 << system["free"][0])
    if not u:
        return {"status": "NO_NONZERO_RECIPROCAL_ON_THIS_LINE", "rank": system["rank"]}
    witness = tuple(encoded(element(bits, v)/element(bits, u)) for v in vector)
    assert all(reciprocal_trace(bits, x) == b for x, b in zip(witness, targets))
    assert all(sum((element(bits, a)**j*element(bits, x) for a, x in zip(points, witness)),
                   field(bits).zero()) == 0 for j in range(dimension))
    return {"status": "VERIFIED_CLASSICAL_WITNESS", "rank": system["rank"],
            "witness": witness, "reciprocal_scalar": u}


def ceil_log2_fraction(value):
    """Exact dyadic upper-bound exponent; never a floating-point certificate."""
    if not isinstance(value, Fraction) or value <= 0:
        raise ValueError("positive Fraction required")
    exponent = value.numerator.bit_length()-value.denominator.bit_length()
    power = Fraction(1 << exponent) if exponent >= 0 else Fraction(1, 1 << -exponent)
    return exponent if value <= power else exponent+1


def _serialize(value):
    if isinstance(value, Fraction):
        exponent = None if not value else log2(abs(value.numerator))-log2(value.denominator)
        summary = {"diagnostic_log2_abs": exponent,
                   "exact_upper_power_of_two": ceil_log2_fraction(abs(value)) if value else None,
                   "exact_zero": not value}
        if max(value.numerator.bit_length(), value.denominator.bit_length()) <= 4096:
            summary.update(numerator_hex=hex(value.numerator), denominator_hex=hex(value.denominator))
        else:
            summary["rational_replay"] = "Recompute from recorded parameters; only the rigorous dyadic bound is serialized."
        return summary
    if isinstance(value, dict):
        return {key: _serialize(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_serialize(item) for item in value]
    return value


def report():
    budgets = [filter_budget(n, n*n, (n*n)//8, (3*n*n)//5) for n in (17, 31, 61)]
    vector = (1, 2, 4, 7)
    native = tuple(encoded(element(3, v)/element(3, 3)) for v in vector)
    target = tuple(reciprocal_trace(3, x) for x in native)
    return {"status": "LOCAL_PER_INSTANCE_DERIVATION_REVIEW_PENDING",
            "new_quantum_mechanism": False, "speedup_established": False,
            "generic_decoder_implemented": False,
            "source": "explicit reciprocal trace, not a random oracle or hidden table",
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "proof_sha256": hashlib.sha256((ROOT / "research/BALANCED_CODEWORD_FILTER.md").read_bytes()).hexdigest(),
            "budgets": budgets,
            "finite_controls": [reference_control(radius=w) for w in (1, 2, 3)]
                               +[reference_control(bits=4, length=3, dimension=1, radius=1)],
            "classical_line_control": projective_line_attack(3, (0, 1, 2, 3), 1, vector, target)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = report()
    if args.write:
        REPORT.write_text(json.dumps(_serialize(result), indent=2)+"\n")
    print(json.dumps({"status": result["status"], "finite_controls": len(result["finite_controls"]),
                      "failure_log2": [_serialize(b["ideal_arithmetic_failure_upper"])["diagnostic_log2_abs"]
                                       for b in result["budgets"]],
                      "report": str(REPORT) if args.write else None}, indent=2))


if __name__ == "__main__":
    main()
