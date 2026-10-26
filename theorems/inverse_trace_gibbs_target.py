"""Native inverse-trace Gibbs target: a conditional classical attack reduction.

Known character orthogonality/MDS identities, specialized in the accompanying
note. Small fixed binary blocks have a worst-initial-state mixing obstruction,
not a uniform-initial-state witness-hitting lower bound. Enumeration below is
explicitly capped and exponential. The local derivation needs external review.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
import hashlib
from itertools import combinations, product
import json
from math import comb, isqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/classical_baselines/inverse_trace_gibbs_target.json"


def integer(value, minimum, maximum, name):
    if type(value) is not int or not minimum <= value <= maximum:
        raise ValueError(f"{name} must be an integer in [{minimum}, {maximum}]")


def _parameters(bits, length, checks):
    integer(bits, 2, 128, "field bits")
    integer(length, 2, min(1 << bits, 100_000), "length")
    integer(checks, 1, length-1, "parity checks")


def mds_character_bound(bits, length, checks, beta, *, exact=False):
    """Bound sum_{d in RS, d!=0} beta^wt(d), without enumerating codewords.

    exact=True evaluates this positive weight-enumerator expression exactly.
    Otherwise use the smaller of the distance and closed binomial bounds.
    beta is an ASSUMED uniform normalized nonzero Fourier bound, not inferred.
    """
    _parameters(bits, length, checks)
    if not isinstance(beta, Q) or not 0 <= beta <= 1:
        raise ValueError("rational Fourier bound in [0,1] required")
    q = 1 << bits
    if exact:
        return sum((comb(length, t)*(1-beta)**t*beta**(length-t)
                    *(q**(checks-t)-1) for t in range(checks)), Q(0))
    distance = (q**checks-1)*beta**(length-checks+1)
    binomial = q**checks*(beta+(1-beta)/q)**length
    return min(distance, binomial)


def reciprocal_bound(bits, length, checks):
    """Uniform every-target/every-syndrome bound from zero-extended Kloosterman."""
    _parameters(bits, length, checks)
    q = 1 << bits
    root = isqrt(q)
    root += int(root*root != q)
    beta = min(Q(1), Q(1+2*root, q))
    return beta, mds_character_bound(bits, length, checks, beta)


def gibbs_success_bound(length, eta, *, inverse_temperature_base=None, sampler_tv=Q(0)):
    """Success assuming a sampler within TV of the ideal law including ABORT.

    Weights are M^-defects. sampler_tv must cover clock failures, floating
    error, and mixing error jointly, on C union {ABORT}; no renormalization.
    """
    integer(length, 2, 100_000, "length")
    if not isinstance(eta, Q) or eta < 0:
        raise ValueError("nonnegative rational relative fiber bound required")
    if not isinstance(sampler_tv, Q) or not 0 <= sampler_tv <= 1:
        raise ValueError("rational sampler TV in [0,1] required")
    base = 1 << (length-1).bit_length() if inverse_temperature_base is None else inverse_temperature_base
    integer(base, length, 1 << 30, "inverse-temperature base M")
    ideal = max(Q(0), (1-eta)/(1+eta))*Q(base, base+1)**length
    return {"M": base, "ideal_native_success_lower": ideal,
            "assumed_sampler_tv_upper": sampler_tv,
            "conditional_native_success_lower": max(Q(0), ideal-sampler_tv),
            "polynomial_mixing_proved": False}


def _ceil_log2(value):
    if value == 0:
        return None
    if value < 0:
        raise ValueError("nonnegative value required")
    exponent = value.numerator.bit_length()-value.denominator.bit_length()
    power = Q(1 << exponent) if exponent >= 0 else Q(1, 1 << -exponent)
    return exponent if value <= power else exponent+1


def _floor(value, precision=128):
    scale = 1 << precision
    result = Q(value.numerator*scale//value.denominator, scale)
    return [result.numerator, result.denominator]


def _ceiling(value, precision=128):
    scale = 1 << precision
    result = Q(-(-value.numerator*scale//value.denominator), scale)
    return [result.numerator, result.denominator]


def _pair_bounds(bits, r):
    integer(bits, 2, 128, "field bits")
    if not isinstance(r, Q) or not 0 < r <= 1:
        raise ValueError("rational positive defect weight at most one required")
    q = 1 << bits
    root = isqrt(q)
    root += int(root*root != q)
    single = 1+2*root
    delta = min(Q(1), Q(3+2*root, q))
    mu_min = (1+r-(1-r)*delta)/4
    theta = (1+r+(1-r)*delta)/2
    beta = min(Q(1), (1-r/2)*single/(q*mu_min))
    return delta, theta, beta


def heatbath_escape_bound(bits, length, checks, *, block_bits=3):
    """Worst-start TV obstruction for state-independent binary heat-bath blocks.

    All blocks are subspaces of C=ker H of dimension at most block_bits.
    This does NOT bound first-witness hitting from a uniform codeword. The
    two MDS distances differ: C has distance K+1; C^perp has N-K+1.
    """
    _parameters(bits, length, checks)
    integer(block_bits, 1, bits*(length-checks), "binary block size")
    base = 1 << (length-1).bit_length()
    _, eta = reciprocal_bound(bits, length, checks)
    delta, theta, beta = _pair_bounds(bits, Q(1, base))
    pair_eta = mds_character_bound(bits, length, checks, beta)
    escape, mass_upper = Q(1), Q(1)
    if eta < 1:
        escape = min(Q(1), ((1 << block_bits)-1)*(1+pair_eta)/(1-eta)*theta**(checks+1))
        mass_upper = min(Q(1), (1+eta)/(1-eta)*Q(base, base+1)**length)
    threshold = max(Q(0), Q(3, 4)-mass_upper)/escape
    lower = -(-threshold.numerator//threshold.denominator)
    return {"fiber_eta": eta, "pair_eta": pair_eta, "pair_beta": beta,
            "correlation_delta": delta, "overlap_factor": theta,
            "M": base, "escape_upper": escape, "stationary_success_upper": mass_upper,
            "worst_start_tv_quarter_steps_lower": lower,
            "nontrivial_mixing_obstruction": lower > 1}


def heatbath_mixing_certificate(bits, length, checks, *, block_bits=3):
    row = heatbath_escape_bound(bits, length, checks, block_bits=block_bits)
    return {"bits": bits, "length": length, "checks": checks,
            "block_bits": block_bits, "M": row["M"],
            "native_displacement_distance": checks+1,
            "pair_beta_upper": _ceiling(row["pair_beta"]),
            "overlap_factor_upper": _ceiling(row["overlap_factor"]),
            "pair_relative_error_power2_upper": _ceil_log2(row["pair_eta"]),
            "mean_solution_escape_power2_upper": _ceil_log2(row["escape_upper"]),
            "stationary_native_success_upper": _ceiling(row["stationary_success_upper"]),
            "worst_start_tv_quarter_steps_lower": row["worst_start_tv_quarter_steps_lower"],
            "nontrivial_mixing_obstruction": row["nontrivial_mixing_obstruction"],
            "mixing_scope": "WORST_INITIAL_STATE_ONLY",
            "uniform_all_targets_and_distinct_evaluation_points": True,
            "requires_state_independent_block_selection": True,
            "uniform_initial_witness_hitting_lower_bound": False,
            "all_classical_algorithms_excluded": False,
            "native_large_chain_executed": False}


def native_certificate(bits):
    integer(bits, 5, 128, "native field bits")
    length, checks = bits*bits, bits*bits//8
    beta, eta = reciprocal_bound(bits, length, checks)
    row = gibbs_success_bound(length, eta, sampler_tv=Q(1, 10))
    return {"bits": bits, "length": length, "checks": checks,
            "beta_upper": [beta.numerator, beta.denominator],
            "fiber_relative_error_power2_upper": _ceil_log2(eta),
            "M": row["M"],
            "ideal_native_success_lower": _floor(row["ideal_native_success_lower"]),
            "assumed_sampler_tv_upper": [1, 10],
            "conditional_native_success_lower": _floor(row["conditional_native_success_lower"]),
            "uniform_all_targets_and_syndromes": True,
            "polynomial_mixing_proved": False,
            "native_large_chain_executed": False}


def _predicate_table(bits):
    from theorems.balanced_codeword_filter import root_spectrum

    roots, _ = root_spectrum(bits, 0)
    zero = set(roots)
    return tuple(int(x not in zero) for x in range(1 << bits))


def _syndrome_columns(bits, points, checks):
    from theorems.explicit_quadratic_opi import element, encoded

    return [[sum(encoded(element(bits, x)*element(bits, a)**j) << (bits*j)
                 for j in range(checks)) for x in range(1 << bits)] for a in points]


def finite_pair_spectrum(bits):
    """All displacements/frequencies, INCLUDING both zero-extension endpoints.

    Squared integer inequalities check the sharp genus-one/two Hasse budgets
    before applying the deliberately rounded envelopes in the certificate.
    """
    integer(bits, 2, 6, "exponential pair-spectrum reference bits")
    from flint import fq_default_ctx

    q = 1 << bits
    context = fq_default_ctx(2, bits, "z")
    powers = [context.gen()**j for j in range(bits)]
    values = [sum((power for j, power in enumerate(powers) if x >> j & 1), context.zero())
              for x in range(q)]
    predicate = [0 if x == 0 else int((x**-1).trace()) for x in values]
    chars = [[1-2*int((u*x).trace()) for x in values] for u in values]
    max_correlation = max_twisted = 0
    for v in range(1, q):
        signs = [1-2*(predicate[x] ^ predicate[x ^ v]) for x in range(q)]
        correlation = sum(signs)
        max_correlation = max(max_correlation, abs(correlation))
        excluded = sum(signs[x] for x in range(q) if x not in (0, v))
        if (excluded+1)**2 > 4*q or correlation != excluded+2*(1-2*predicate[v]):
            raise ArithmeticError("two-pole genus-one or endpoint identity failed")
        for u in range(q):
            twisted = sum(a*b for a, b in zip(signs, chars[u]))
            if u:
                excluded = sum(signs[x]*chars[u][x] for x in range(q) if x not in (0, v))
                if excluded**2 > 16*q or twisted != excluded+(1-2*predicate[v])*(1+chars[u][v]):
                    raise ArithmeticError("three-pole genus-two or endpoint identity failed")
                max_twisted = max(max_twisted, abs(twisted))
        for r in (Q(1), Q(1, 4), Q(1, 32)):
            delta, theta, beta = _pair_bounds(bits, r)
            for b in (0, 1):
                h = [int(predicate[x] == b)*(r+(1-r)*int(predicate[x ^ v] == b))
                     for x in range(q)]
                mean = sum(h)/q
                if mean != (1+r+(1-r)*Q(correlation, q))/4:
                    raise ArithmeticError("weighted overlap mass identity failed")
                if not (1+r-(1-r)*delta)/4 <= mean <= theta/2:
                    raise ArithmeticError("weighted overlap mass bound failed")
                if any(abs(sum(a*c for a, c in zip(h, chars[u]))) > q*mean*beta
                       for u in range(1, q)):
                    raise ArithmeticError("normalized weighted Fourier bound failed")
    return {"bits": bits, "field_size": q, "displacement_frequency_pairs": q*(q-1),
            "public_reference_modulus": str(context.modulus()),
            "backend": "independent FLINT finite-field reference, not native solver",
            "weighted_displacement_target_controls": 6*(q-1),
            "maximum_absolute_correlation": max_correlation,
            "maximum_absolute_twisted_sum": max_twisted,
            "zero_extensions_and_infinity_terms_checked": True,
            "reference_is_polynomial_in_field_bits": False}


def finite_fiber_audit(bits, length, checks):
    """Enumerate ALL words, targets AND syndromes; no selected easy target."""
    _parameters(bits, length, checks)
    q = 1 << bits
    if bits > 5 or q**length > 65_536:
        raise ValueError("exponential fiber reference cap exceeded")
    from theorems.balanced_codeword_filter import root_spectrum

    predicate = _predicate_table(bits)
    columns = _syndrome_columns(bits, tuple(range(length)), checks)
    counts = [[0]*(1 << length) for _ in range(q**checks)]
    for word in product(range(q), repeat=length):
        syndrome, target = 0, 0
        for i, x in enumerate(word):
            syndrome ^= columns[i][x]
            target |= predicate[x] << i
        counts[syndrome][target] += 1
    mean = Q(q**(length-checks), 1 << length)
    _, spectrum = root_spectrum(bits, 0)
    beta = max(Q(abs(2*x), q) for x in spectrum[1:])
    eta = mds_character_bound(bits, length, checks, beta, exact=True)
    deviation = max(abs(Q(c)/mean-1) for row in counts for c in row)
    if deviation > eta:
        raise ArithmeticError("all-target/all-syndrome count violates MDS bound")
    return {"bits": bits, "length": length, "checks": checks,
            "words_enumerated": q**length,
            "target_syndrome_pairs": q**checks*(1 << length),
            "exact_mean_count": [mean.numerator, mean.denominator],
            "actual_beta": [beta.numerator, beta.denominator],
            "exact_mds_envelope": [eta.numerator, eta.denominator],
            "maximum_relative_deviation": [deviation.numerator, deviation.denominator],
            "minimum_fiber_count": min(map(min, counts)),
            "maximum_fiber_count": max(map(max, counts)),
            "all_fiber_counts": counts,
            "reference_is_polynomial_in_field_bits": False}


def reference_heatbath(bits, length, checks, targets, *, block_bits=1):
    """Exact finite bit-block kernel on systematic coordinates, NOT q-ary blocks.

    Every transition, including stays, has exact rational probabilities. The
    complete transition matrix is only an audit of the proposed legal move.
    It is NOT the scalable sampler and proves no asymptotic mixing claim.
    """
    _parameters(bits, length, checks)
    width = bits*(length-checks)
    if width > 6:
        raise ValueError("exponential transition reference cap exceeded")
    integer(block_bits, 1, min(3, width), "binary block size")
    targets = tuple(targets)
    if len(targets) != length or any(type(b) is not int or b not in (0, 1) for b in targets):
        raise ValueError("one target bit per native coordinate required")
    from theorems.explicit_quadratic_opi import element, encoded
    from theorems.inverse_trace_quadratic_closure import support_word

    points = tuple(range(length))
    directions = []
    for free in range(checks, length):
        v = support_word(bits, points, checks, tuple(range(checks))+(free,), free)
        for bit in range(bits):
            directions.append(tuple(encoded(element(bits, x)*element(bits, 1 << bit)) for x in v))
    words = [(0,)*length]
    for label in range(1, 1 << width):
        low = label & -label
        words.append(tuple(a ^ b for a, b in zip(words[label ^ low], directions[low.bit_length()-1])))
    columns = _syndrome_columns(bits, points, checks)
    for word in words:
        residual = 0
        for i, x in enumerate(word):
            residual ^= columns[i][x]
        if residual:
            raise ArithmeticError("systematic proposal escaped the native code")
    if len(set(words)) != len(words):
        raise ArithmeticError("systematic coordinates are not injective")
    predicate = _predicate_table(bits)
    defects = [sum(predicate[x] != b for x, b in zip(word, targets)) for word in words]
    base = 1 << (length-1).bit_length()
    weights = [base**(length-d) for d in defects]
    blocks = tuple(combinations(range(width), block_bits))
    matrix = [[Q(0)]*len(words) for _ in words]
    for i in range(len(words)):
        for block in blocks:
            cleared = i & ~sum(1 << bit for bit in block)
            neighbors = [cleared | sum(((t >> j) & 1) << bit for j, bit in enumerate(block))
                         for t in range(1 << block_bits)]
            normalizer = len(blocks)*sum(weights[j] for j in neighbors)
            for j in neighbors:
                matrix[i][j] += Q(weights[j], normalizer)
    if any(sum(row) != 1 for row in matrix):
        raise ArithmeticError("transition row lost probability mass")
    if any(weights[i]*matrix[i][j] != weights[j]*matrix[j][i]
           for i in range(len(words)) for j in range(len(words))):
        raise ArithmeticError("detailed balance failed")
    # Every one-bit neighbor and every stay must have positive probability.
    if any(matrix[i][i] <= 0 or any(matrix[i][i ^ (1 << b)] <= 0 for b in range(width))
           for i in range(len(words))):
        raise ArithmeticError("irreducibility/self-loop control failed")
    stationary_success = Q(sum(w for w, d in zip(weights, defects) if d == 0), sum(weights))
    witnesses = defects.count(0)
    escape = (sum((matrix[i][j] for i, di in enumerate(defects) if di == 0
                   for j, dj in enumerate(defects) if dj != 0), Q(0))/witnesses
              if witnesses else None)
    return {"bits": bits, "length": length, "checks": checks, "targets": list(targets),
            "block_bits": block_bits, "M": base, "binary_coordinate_count": width,
            "states_enumerated": len(words), "native_witnesses_enumerated": defects.count(0),
            "stationary_native_success": [stationary_success.numerator, stationary_success.denominator],
            "mean_solution_escape": None if escape is None else [escape.numerator, escape.denominator],
            "candidates_per_update": 1 << block_bits,
            "full_field_block_would_cost": (1 << bits)**block_bits,
            "detailed_balance_exact": True, "irreducible_and_aperiodic": True,
            "polynomial_mixing_proved": False, "reference_is_scalable_sampler": False}


def report(*, include_finite=True, include_pair=True):
    return {"status": "CONDITIONAL_GIBBS_ATTACK_SMALL_BLOCK_WORST_CASE_MIXING_OBSTRUCTED",
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "proof_sha256": hashlib.sha256((ROOT / "research/INVERSE_TRACE_GIBBS_TARGET.md").read_bytes()).hexdigest(),
            "full_native_classical_solver_established": False,
            "quantum_speedup_established": False,
            "sampler_total_variation_bound_proved": False,
            "local_mixing_derivation_external_review_pending": True,
            "native_finite_controls_executed": include_finite,
            "independent_pair_controls_executed": include_pair,
            "native_certificates": [native_certificate(n) for n in (17, 31, 61)],
            "small_block_mixing_certificates": [heatbath_mixing_certificate(n, n*n, n*n//8) for n in (17, 31, 61)],
            "pair_spectrum_controls": [finite_pair_spectrum(n) for n in (2, 3, 4, 5)] if include_pair else [],
            "all_fiber_controls": [finite_fiber_audit(*p) for p in ((2, 3, 1), (3, 4, 2), (4, 4, 1))] if include_finite else [],
            "kernel_controls": [reference_heatbath(3, 3, 1, (1, 0, 1), block_bits=k) for k in (1, 2, 3)] if include_finite else []}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--bounds-only", action="store_true",
                        help="exact rational certificates only; explicitly omit finite-field controls")
    parser.add_argument("--skip-native-controls", action="store_true",
                        help="omit native-backend replays; retain independent scalar pair controls")
    args = parser.parse_args()
    data = report(include_finite=not (args.bounds_only or args.skip_native_controls),
                  include_pair=not args.bounds_only)
    if args.write:
        REPORT.write_text(json.dumps(data, indent=2)+"\n")
    print(json.dumps({"status": data["status"], "native_certificates": data["native_certificates"],
                      "small_block_mixing_certificates": data["small_block_mixing_certificates"],
                      "native_finite_controls_executed": data["native_finite_controls_executed"],
                      "independent_pair_controls_executed": data["independent_pair_controls_executed"],
                      "scalar_displacement_frequency_pairs_checked": sum(r["displacement_frequency_pairs"] for r in data["pair_spectrum_controls"]),
                      "finite_fiber_inputs_checked": sum(r["target_syndrome_pairs"] for r in data["all_fiber_controls"]),
                      "kernel_controls": len(data["kernel_controls"])}, indent=2))


if __name__ == "__main__":
    main()
