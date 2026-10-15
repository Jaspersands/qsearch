"""Exact higher-call collision ideals and actual response/Fourier interleaving.

Path counts are not acceptance probabilities for arbitrary quantum mixers.
Only IID original labels justify the ideal-weighted population collision law.
Public noisy-linear responses prepare phases; no unknown-phase oracle is granted.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
from itertools import product
import json
from math import gcd
from pathlib import Path

import numpy as np

from native_basis_lottery import original_bank
from native_full_root_slice import source_data
from native_word_span_decision import root_polynomial
from ternary_measured_lattice_decoder import exact_json, integer

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/reductions/native_response_path_valuation.json"
DERIVATION = ROOT / "research/NATIVE_RESPONSE_PATH_VALUATION.md"
CONTRACT = ROOT / "research/hypotheses/native_response_path_valuation_contract.json"
DIGITS = ((1, 0), (-1, 1), (0, -1))


def local_difference_counts(calls, max_work=1_000_000):
    """Count ordered signed path pairs via their two-dimensional integer sums."""
    integer(calls, "positive response calls", 1)
    integer(max_work, "positive compressed work cap", 1)
    if calls > 32 or ((calls + 1) * (calls + 2) // 2) ** 2 > max_work:
        raise ValueError("compressed local path census cap exceeded")
    sums = Counter({(0, 0): 1})
    for _ in range(calls):
        nxt = Counter()
        for (x, y), multiplicity in sums.items():
            for dx, dy in DIGITS:
                nxt[x + dx, y + dy] += multiplicity
        sums = nxt
    differences = Counter()
    for (x, y), a in sums.items():
        for (u, v), b in sums.items():
            differences[x - u, y - v] += a * b
    if sum(differences.values()) != 3 ** (2 * calls):
        raise ArithmeticError("ordered path census lost mass")
    return differences


def iid_path_collision_law(n, d, sites, calls, max_work=1_000_000):
    """Exact ideal-stratified E_A collision density of calls positive word copies.

    This is a population combinatorial diagnostic, not a query lower bound.
    Counts are compressed rather than allocating 3^(2*calls*sites) paths.
    """
    for value, name in ((n, "dimension"), (d, "root digits"), (sites, "sites")):
        integer(value, "positive " + name, 1)
    integer(calls, "positive calls", 1)
    if d > 32 or n * d > 1024 or 2 * calls * sites > 4096:
        raise ValueError("exact integer ledger cap exceeded; no negative conclusion")
    differences = local_difference_counts(calls, max_work)
    q = 3 ** d
    total_local = 3 ** (2 * calls)
    local = Counter()
    for (x, y), count in differences.items():
        g = gcd(q, x, y)
        valuation = 0
        while g > 1:
            g //= 3
            valuation += 1
        local[valuation] += count
    # All-site ideal is the minimum local valuation, including zero mod q at d.
    survival = [sum(c for v, c in local.items() if v >= h) for h in range(d + 1)]
    total = total_local ** sites
    strata = []
    expected = Fraction(0)
    for h in range(d + 1):
        count = survival[h] ** sites
        if h < d:
            count -= survival[h + 1] ** sites
        probability = Fraction(1, 3 ** ((d - h) * n))
        contribution = Fraction(count, total) * probability
        expected += contribution
        strata.append({"valuation": h, "local_count": local[h],
                       "all_sites_path_pair_count": count,
                       "IID_label_collision_probability": str(probability),
                       "collision_density_contribution": str(contribution)})
    if sum(s["all_sites_path_pair_count"] for s in strata) != total:
        raise ArithmeticError("ideal strata do not partition path pairs")
    return {"dimension": n, "root_digits": d, "modulus": q, "word_sites": sites,
            "positive_response_calls": calls, "compressed_integer_sum_count": (calls + 1) * (calls + 2) // 2,
            "local_ordered_path_pairs": total_local, "total_ordered_path_pairs": total,
            "local_zero_over_integers_count": differences[0, 0], "ideal_strata": strata,
            "exact_IID_expected_collision_density": str(expected),
            "nonzero_coefficients_assumed_units": False,
            "local_nonzero_modq_nonunit_count": sum(local[h] for h in range(1, d)),
            "collision_density_is_arbitrary_mixer_acceptance": False,
            "IID_uniform_original_labels_required": True,
            "quantum_query_lower_bound_supplied": False}


def word_rows(records, mask):
    """Only actual public labels/values and a known mask enter word construction."""
    raw = original_bank(records)
    q, n = raw[0].modulus, len(raw[0].label)
    mask = tuple(mask)
    if len(raw) % 2 or len(mask) != n:
        raise ValueError("paired original rows and full public mask required")
    if any(type(x) is not int or not 0 <= x < q for x in mask):
        raise ValueError("canonical public mask required")
    sites = len(raw) // 2
    D = 3 ** sites
    if q > 27 or D > 9 or q ** n > 27:
        raise ValueError("complete exact measured-readout cap exceeded")
    rows = []
    for word in product(range(3), repeat=sites):
        beta = tuple(b for t in word for b in DIGITS[t])
        f = tuple(sum(b * r.label[i] for b, r in zip(beta, raw)) % q for i in range(n))
        phase = (sum(b * r.value for b, r in zip(beta, raw)) + sum(a * z for a, z in zip(f, mask))) % q
        rows.append({"word": word, "frequency": f, "known_phase": phase})
    return tuple(rows)


def _histogram_probability(hist, root, denominator):
    coefficients = [Fraction(0)] * root
    for a, ca in hist.items():
        for b, cb in hist.items():
            coefficients[(a - b) % root] += Fraction(ca * cb, denominator)
    return coefficients


def fourier_interleaved_readout(records, mask):
    """Full Born law for F_D^dag D_y F_D D_y |+_D>, with both actual phase calls.

    F_D uses positive Fourier exponents. All D outcomes are returned. The
    classical FFT replay uses the SAME explicit public data, costs O(D log D),
    and is exponential in sites, not efficient general dequantization.
    """
    raw = original_bank(records)
    rows = word_rows(raw, mask)
    D, q = len(rows), raw[0].modulus
    root = max(D, q)
    phase_scale, fourier_scale = root // q, root // D
    readout = []
    for x in range(D):
        hist = Counter((phase_scale * (rw["known_phase"] + rv["known_phase"])
                        + fourier_scale * v * (w - x)) % root
                       for w, rw in enumerate(rows) for v, rv in enumerate(rows))
        readout.append(root_polynomial(_histogram_probability(hist, root, D ** 3), root))
    phases = np.exp(2j * np.pi * np.array([r["known_phase"] for r in rows]) / q)
    mid = np.fft.ifft(phases / np.sqrt(D)) * np.sqrt(D)
    out = np.fft.fft(phases * mid) / np.sqrt(D)
    return {"modulus": q, "word_dimension": D, "root_order": root,
            "public_mask": tuple(mask), "actual_word_rows": rows,
            "schedule": "F_D_DAGGER D_y F_D D_y |PLUS_D>",
            "exact_all_outcome_probabilities": tuple(readout),
            "classical_same_data_FFT_probabilities": tuple(float(abs(z) ** 2) for z in out),
            "public_response_phase_calls": 2,
            "classical_FFT_amplitudes_stored": D,
            "classical_FFT_cost_is_polynomial_in_sites": False,
            "hardware_circuit_compiled": False,
            "unknown_phase_oracle_or_truth_used": False,
            "normalized_fibre_oracle_used": False}


def weighted_interleaving_control(parameters):
    """Calibration-only secret census and independent weighted-path pinching."""
    raw, mask, truth, errors = source_data(*parameters)
    raw = original_bank(raw)
    actual = fourier_interleaved_readout(raw, mask)
    rows = actual["actual_word_rows"]
    D, q, root = len(rows), raw[0].modulus, actual["root_order"]
    n = len(raw[0].label)
    secrets = tuple(product(range(q), repeat=n))
    error_phases = tuple(sum(b * e for t, pair in zip(r["word"], zip(errors[::2], errors[1::2]))
                             for b, e in zip(DIGITS[t], pair)) % q for r in rows)
    mean, pinched = [], []
    for x in range(D):
        sweep = [Fraction(0)] * root
        for s in secrets:
            hist = Counter()
            for w, rw in enumerate(rows):
                for v, rv in enumerate(rows):
                    phase = sum((a + b) * t for a, b, t in zip(rw["frequency"], rv["frequency"], s))
                    exponent = ((root // q) * (phase + error_phases[w] + error_phases[v])
                                + (root // D) * v * (w - x)) % root
                    hist[exponent] += 1
            term = _histogram_probability(hist, root, D ** 3 * len(secrets))
            sweep = [a + b for a, b in zip(sweep, term)]
        grouped = {}
        for w, rw in enumerate(rows):
            for v, rv in enumerate(rows):
                tau = tuple((a + b) % q for a, b in zip(rw["frequency"], rv["frequency"]))
                exponent = ((root // q) * (error_phases[w] + error_phases[v])
                            + (root // D) * v * (w - x)) % root
                grouped.setdefault(tau, Counter())[exponent] += 1
        exact = [Fraction(0)] * root
        for hist in grouped.values():
            term = _histogram_probability(hist, root, D ** 3)
            exact = [a + b for a, b in zip(exact, term)]
        a, b = root_polynomial(sweep, root), root_polynomial(exact, root)
        if a != b:
            raise ArithmeticError("weighted path pinching disagrees with complete secret sweep")
        mean.append(a)
        pinched.append(b)
    return {"original_records": tuple(r.public() for r in raw),
            "calibration_only": {"masked_secret": truth, "original_errors": errors},
            "actual_public_data_readout": actual, "secret_population": len(secrets),
            "uniform_secret_mean_all_outcomes": tuple(mean),
            "weighted_additive_pinching_all_outcomes": tuple(pinched),
            "all_outcomes_retained": True, "weights_from_actual_unitary": True,
            "raw_collision_count_used_as_quantum_probability": False,
            "efficient_secret_decoder_supplied": False}


def build_report():
    profiles = tuple(iid_path_collision_law(n, d, sites, calls)
                     for n, d, sites, calls in ((1, 1, 1, 2), (1, 2, 1, 2), (2, 2, 2, 2))
                     + tuple((8, 8, 76, k) for k in (1, 2, 3, 4, 6, 9))
                     + ((32, 4, 140, 6), (128, 1, 140, 9)))
    controls = tuple(weighted_interleaving_control(p) for p in
                     ((1, 2, 1, False, 99201), (1, 1, 2, True, 99202), (2, 1, 1, False, 99203)))
    return {"status": "HIGHER_RESPONSE_PATH_IDEALS_AND_WEIGHTED_UNITARY_READOUT_REVIEW_PENDING",
            "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "contract_sha256": hashlib.sha256(CONTRACT.read_bytes()).hexdigest(),
            "dependency_sha256": {f: hashlib.sha256((ROOT / "theorems" / f).read_bytes()).hexdigest()
                                  for f in ("native_basis_lottery.py", "native_full_root_slice.py",
                                            "native_word_span_decision.py", "ternary_measured_lattice_decoder.py")},
            "IID_path_collision_profiles": profiles, "weighted_unitary_interleaving_controls": controls,
            "false_unit_assumption_counterexample": {"modulus": 9, "coefficient_difference": (3, 0),
                                                      "actual_collision_probability": "1/3",
                                                      "false_uniform_prediction": "1/9",
                                                      "two_call_M1_exact_mean": "25/81",
                                                      "old_two_call_M1_prediction": "67/243"},
            "accepted_speedup_candidate": False, "new_active_negative_result_created": False,
            "general_quantum_lower_bound": False, "novelty_claim": False,
            "research_decision": "SEARCH_WEIGHTED_UNITARY_PATHS_NOT_UNWEIGHTED_COLLISION_COUNTS"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report), indent=2) + "\n")
    print(json.dumps({"status": report["status"], "collision_profiles": len(report["IID_path_collision_profiles"]),
                      "weighted_controls": len(report["weighted_unitary_interleaving_controls"]),
                      "accepted_speedup_candidate": False}, indent=2))


if __name__ == "__main__":
    main()
