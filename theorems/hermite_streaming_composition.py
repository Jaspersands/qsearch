"""Finite identity controls for the proposed Hermite streaming composition.

The statevectors and stream-promise checks are reference diagnostics, not a
small-space implementation. Large-parameter outputs are arithmetic ledgers.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import json
from math import isqrt, sqrt
from pathlib import Path
import random

import numpy as np

from theorems.hermite_compact_decoder import CompactHermite, decode
from theorems.hermite_pinned_decoder import (
    fraction_record, integer, parameters, pin_budget, pin_failure_bound,
    source_herald,
)
from theorems.prime_character_opi import ring

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/reductions/hermite_streaming_composition.json"


def probability(value, label, *, strict=False):
    if not isinstance(value, (int, Fraction)) or isinstance(value, bool):
        raise ValueError(f"{label} must be an exact rational")
    value = Fraction(value)
    if not (0 < value < 1 if strict else 0 <= value <= 1):
        raise ValueError(f"{label} outside probability interval")
    return value


def source_law(q, ell, lam):
    ring(q)
    integer(ell, 1, q-1, "multiplicity")
    lam = probability(lam, "lambda", strict=True)
    a = Fraction(1, q**ell)
    rho, theta = (1-a)/2, lam*(1-a*a)
    score = float(rho+(1-2*rho)*theta) + 2*sqrt(
        float(theta*(1-theta)*rho*(1-rho)))
    return {"rho": rho, "theta": theta, "score": score,
            "zero_frequency_selector_leak_without_rotation": lam*a*a}


def fourier(values, q, ell, *, inverse=False):
    """Tensor Fourier transform on (F_q)^ell, NOT the cyclic group Z/(q^ell)."""
    shaped = np.asarray(values, dtype=complex).reshape((q,)*ell)
    axes = tuple(range(ell))
    transform = np.fft.ifftn if inverse else np.fft.fftn
    return transform(shaped, axes=axes, norm="ortho").reshape(-1)


def load_one_pass(q, ell, lam, entries, *, cleanup=True):
    """Consume an iterable once; reference-only exhaustive promise validation."""
    law = source_law(q, ell, lam)
    size, n = q**ell, q-1
    if size*n > 65536:
        raise ValueError("bounded statevector diagnostic only")
    states = np.zeros((n, 2, size), dtype=complex)
    states[:, 0, :] = sqrt(float(1-lam)/size)
    states[:, 1, :] = sqrt(float(lam)/size)
    seen, ones, updates = set(), [0]*n, 0
    for i, address, bit in entries:
        integer(i, 0, n-1, "row")
        integer(address, 0, size-1, "address")
        integer(bit, 0, 1, "membership bit")
        if (i, address) in seen:
            raise ValueError("duplicate stream entry")
        seen.add((i, address))
        ones[i] += bit
        states[i, 1, address] *= 1 if bit else -1
        updates += 1
    if updates != n*size or any(count != (size-1)//2 for count in ones):
        raise ValueError("complete odd half-set tables required")
    # Nonzero-frequency selector flip, then a PUBLIC zero-frequency rotation.
    a = float(Fraction(1, size))
    x, y = sqrt(float(1-lam)), -a*sqrt(float(lam))
    norm = sqrt(x*x+y*y)
    rotation = np.array([[x, y], [-y, x]])/norm
    for state in states:
        for selector in range(2):
            state[selector] = fourier(state[selector], q, ell)
        state[:, 1:] = state[::-1, 1:].copy()
        if cleanup:
            state[:, 0] = rotation @ state[:, 0]
    return states, {"entries_consumed": updates, "passes": 1,
                    "promise_validation_uses_full_stream_memory": True,
                    "quantum_space_measured": False,
                    "selector_one_mass": [float(np.vdot(s[1], s[1]).real) for s in states],
                    "theta": fraction_record(law["theta"])}


def bounded_subset(n, count, trials, getrandbits):
    """Uniform subset conditional on success; abort instead of biased fallback."""
    integer(n, 1, 1 << 24, "population")
    integer(count, 0, n, "subset size")
    integer(trials, 1, 4096, "trials per draw")
    pool = list(range(n))
    selected = []
    for j in range(count):
        bound = n-j
        bits = (bound-1).bit_length()
        offset = 0
        if bits:
            for _ in range(trials):
                offset = getrandbits(bits)
                integer(offset, 0, 2**bits-1, "random bit word")
                if offset < bound:
                    break
            else:
                return None
        selected.append(pool[offset])
        pool[offset], pool[bound-1] = pool[bound-1], pool[offset]
    return tuple(sorted(selected))


def sampler_failure(n, count, trials):
    integer(n, 1, 1 << 40, "population")
    integer(count, 0, n, "subset size")
    integer(trials, 1, 4096, "trials per draw")
    success = Fraction(1)
    for bound in range(n-count+1, n+1):
        rejection = Fraction(2**((bound-1).bit_length())-bound,
                             2**((bound-1).bit_length()))
        success *= 1-rejection**trials
    return 1-success


def failure_account(n, gap, rejected, pin_sampler_failure, synthesis_tv):
    """Unconditional upper bound; no division by any per-R acceptance mass."""
    integer(n, 1, 1 << 40, "block count")
    if not isinstance(gap, Fraction):
        raise ValueError("exact rational score gap required")
    rejected = probability(rejected, "rejected mass")
    pin_sampler_failure = probability(pin_sampler_failure, "sampler failure")
    synthesis_tv = probability(synthesis_tv, "total synthesis TV")
    joint = (Fraction(1, 2*n)+2*rejected)/gap**2 if gap > 0 else Fraction(1)
    joint = min(Fraction(1), joint)
    total = min(Fraction(1), pin_sampler_failure+rejected+joint+synthesis_tv)
    return {"accepted_bad_joint_upper": fraction_record(joint),
            "unconditional_total_failure_upper": fraction_record(total),
            "positive_score_gap": gap > 0,
            "conditioning_on_acceptance_used": False}


def composition_ledger(q=1000000007, ell=256, order=15, *,
                       lam=Fraction(21, 50), tau=Fraction(43, 100),
                       target=Fraction(99, 100), security_bits=40):
    lam = probability(lam, "lambda", strict=True)
    tau = probability(tau, "tau", strict=True)
    target = probability(target, "target", strict=True)
    if not lam < tau < Fraction(1, 2):
        raise ValueError("require lambda < tau < 1/2")
    integer(security_bits, 1, 4096, "security bits")
    n = q-1
    source_cap = tau.numerator*n//tau.denominator
    spec = parameters(q, ell, order, source_cap+2)
    pins = pin_budget(n, ell, spec["k"], spec["kernel_dimension_bound"], security_bits)
    pin_failure = pin_failure_bound(n, ell, spec["k"], spec["kernel_dimension_bound"], pins)
    trials = security_bits + max(0, (pins-1).bit_length())
    rng_failure = Fraction(pins, 2**trials)
    radicand, scale = lam*(1-lam), 2**128
    beta_lower = Fraction(1, 2)+Fraction(
        isqrt(radicand.numerator*scale**2//radicand.denominator), scale)
    gap = beta_lower-Fraction(1, q)-target-Fraction(pins, n)
    exponent = 2*(tau-lam)**2*n
    # exp(-x) <= 2^-floor(x); capped deliberately, never rounded downward.
    tail = Fraction(1, 2**min(security_bits, exponent.numerator//exponent.denominator))
    rejected = min(Fraction(1), tail+pin_failure)
    tv = Fraction(1, 2**security_bits)
    return {"kind": "ARITHMETIC_ONLY_REVIEW_PENDING",
            "parameters": spec, "source_cap": source_cap, "guard_radius": source_cap+2,
            "lambda": fraction_record(lam), "tau": fraction_record(tau),
            "target": fraction_record(target), "pins": pins,
            "pin_ambiguity_upper": fraction_record(pin_failure),
            "source_tail_upper": fraction_record(tail),
            "pin_sampler_trials_per_draw": trials,
            "pin_sampler_failure_upper": fraction_record(rng_failure),
            "required_total_synthesis_tv": fraction_record(tv),
            "score_gap_lower": fraction_record(gap),
            **failure_account(n, gap, rejected, rng_failure, tv),
            "classical_decoder_bits": "O_s(q*ell*log(q))",
            "reversible_bits": "O_s(q*ell*log(q)*log(q*ell))",
            "preprocessing_update_postprocessing_time": "poly_s(q,ell)",
            "total_time": "N*poly_s(q,ell), NOT polylog(N)",
            "stream_length": "N=(q-1)*q^ell",
            "stream_updates_exactly_synthesizable": True,
            "approximate_gates_per_stream_entry": 0,
            "approximate_gates_outside_stream": "poly_s(q,ell), before and after only",
            "decoder_requeries_input_table": False,
            "native_quantum_circuit_executed": False,
            "new_quantum_algorithm_claim_allowed": False}


def loader_control(q, ell, lam, seed):
    rng, size = random.Random(seed), q**ell
    tables = [set(rng.sample(range(size), (size-1)//2)) for _ in range(q-1)]
    entries = [(i, z, int(z in tables[i])) for i in range(q-1) for z in range(size)]
    clean, info = load_one_pass(q, ell, lam, iter(entries))
    rng.shuffle(entries)
    shuffled, _ = load_one_pass(q, ell, lam, iter(entries))
    dirty, dirty_info = load_one_pass(q, ell, lam, iter(entries), cleanup=False)
    law = source_law(q, ell, lam)
    residual, scores, theta = 0.0, [], float(law["theta"])
    for i, table in enumerate(tables):
        signs = np.array([1 if z in table else -1 for z in range(size)])
        perpendicular = (signs+1/size)/sqrt(size*(1-1/size**2))
        expected = sqrt(theta)*fourier(perpendicular, q, ell)
        expected[0] += sqrt(1-theta)
        residual = max(residual, float(np.max(np.abs(clean[i, 0]-expected))))
        values = fourier(clean[i, 0], q, ell, inverse=True)
        scores.append(float(sum(abs(values[z])**2 for z in table)))
    return {"q": q, "ell": ell, "lambda": fraction_record(lam), **info,
            "product_formula_max_residual": residual,
            "stream_order_max_residual": float(np.max(np.abs(clean-shuffled))),
            "predicted_good_score": law["score"], "observed_good_scores": scores,
            "omitted_rotation_selector_mass": dirty_info["selector_one_mass"],
            "predicted_omitted_rotation_mass": fraction_record(
                law["zero_frequency_selector_leak_without_rotation"]),
            "dirty_state_differs": bool(np.max(np.abs(clean-dirty)) > 1e-10)}


def instrument_control():
    """Sparse basis audit of the actual decoder, not a full source simulation."""
    code = CompactHermite(13, 8)
    errors = [[0]*code.width for _ in range(3)]
    errors[1][0] = 1
    errors[2][0], errors[2][8] = 1, 1
    pin_blocks = (0, 1)
    images, accepted, statuses, erased = [], [], [], []
    for error in errors:
        syndrome = code.syndrome(error)
        pins = {i: error[i*code.ell:(i+1)*code.ell] for i in pin_blocks}
        result = decode(code, syndrome, pins, order=2, radius=3)
        keep = source_herald(error, result, code.ell, source_cap=1)
        statuses.append(result["status"])
        accepted.append(keep)
        if keep:
            images.append(tuple(syndrome+[x for i in pin_blocks for x in pins[i]]))
            erased.append([(x-y) % code.p for x, y in zip(error, result["error"])])
    if len(set(images)) != len(images) or any(any(row) for row in erased):
        raise ArithmeticError("accepted label erasure is not an isometry")
    kept, count = sum(accepted), len(errors)
    return {"q": code.p, "ell": code.ell, "source_cap": 1, "guard_radius": 3,
            "diagnostic_source": "equal superposition of three explicitly specified labels",
            "not_the_full_product_source": True,
            "accepted": accepted, "decoder_statuses": statuses,
            "herald_failure_mass": fraction_record(Fraction(count-kept, count)),
            "accepted_mass": fraction_record(Fraction(kept, count)),
            "erased_error_registers_all_zero": True,
            "distinct_augmented_syndromes": True,
            "zero_character_probability_denominator": str(code.p**(code.k+code.ell*len(pin_blocks))),
            "clean_zero_character_numerator": fraction_record(Fraction(kept**2, count)),
            "retained_error_register_numerator": fraction_record(Fraction(kept, count)),
            "native_quantum_circuit_executed": False}


def controls():
    return {"status": "COMPOSITION_CONTROLS_AND_THEOREM_REVIEW_PENDING",
            "source_controls": [loader_control(q, ell, Fraction(21, 50), q+ell)
                                for q, ell in ((3, 1), (3, 2), (5, 2))],
            "decoder_instrument": instrument_control(),
            "large_parameter_arithmetic_only": composition_ledger(),
            "source_loader_is_prior_art": True,
            "missing_guard_counterexample_retained_in": "hermite_pinned_decoder.json",
            "proof_and_novelty_independently_reviewed": False,
            "new_quantum_algorithm_claim_allowed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPORT)
    args = parser.parse_args()
    report = controls()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"status": report["status"], "output": str(args.output),
                      "failure_upper_arithmetic_only": report[
                          "large_parameter_arithmetic_only"]["unconditional_total_failure_upper"]["float"]}))


if __name__ == "__main__":
    main()
