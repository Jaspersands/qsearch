"""Adversarial arithmetic, actual unitary and independent certificate tests."""
from collections import Counter
from copy import deepcopy
from fractions import Fraction
from itertools import product
import json
import subprocess

import numpy as np
import pytest

from theorems import native_response_path_valuation as P
from ternary_noise_degradation import NoisyLinearRecord


def stored():
    return json.loads(P.REPORT.read_text())


def value(polynomial, root):
    return sum(float(Fraction(c)) * np.exp(2j * np.pi * i / root)
               for i, c in enumerate(reversed(polynomial)))


def node_check(payload):
    return subprocess.run(["node", "-e",
        "const X=require('./research/certificates/native_response_path_valuation_crosscheck.js');"
        "let s='';process.stdin.on('data',x=>s+=x);"
        "process.stdin.on('end',()=>console.log(JSON.stringify(X.verify(JSON.parse(s)))));"],
        input=json.dumps(payload), text=True, capture_output=True, cwd=P.ROOT)


@pytest.mark.parametrize("calls", (1, 2, 3, 4))
def test_compressed_count_matches_bruteforce_ordered_digit_sequences(calls):
    sums = Counter(tuple(sum(d[i] for d in path) for i in range(2))
                   for path in product(P.DIGITS, repeat=calls))
    differences = Counter()
    for (a, b), x in sums.items():
        for (c, d), y in sums.items():
            differences[a - c, b - d] += x * y
    assert P.local_difference_counts(calls) == differences
    assert sum(differences.values()) == 3 ** (2 * calls)


@pytest.mark.parametrize("n,d,sites,calls", ((1, 1, 1, 2), (1, 2, 1, 2),
                                           (2, 1, 1, 3), (1, 1, 2, 2), (1, 2, 1, 3)))
def test_exact_IID_collision_law_matches_complete_public_label_banks(n, d, sites, calls):
    q = 3 ** d
    labels = tuple(product(range(q), repeat=n))
    words = tuple(product(range(3), repeat=sites))
    total = Fraction(0)
    banks = q ** (2 * sites * n)
    for bank in product(labels, repeat=2 * sites):
        one = Counter()
        for word in words:
            beta = tuple(b for t in word for b in P.DIGITS[t])
            frequency = tuple(sum(b * label[i] for b, label in zip(beta, bank)) % q for i in range(n))
            one[frequency] += 1
        convolution = Counter({(0,) * n: 1})
        for _ in range(calls):
            nxt = Counter()
            for f, a in convolution.items():
                for g, b in one.items():
                    nxt[tuple((x + y) % q for x, y in zip(f, g))] += a * b
            convolution = nxt
        total += Fraction(sum(c * c for c in convolution.values()), 3 ** (2 * sites * calls))
    report = P.iid_path_collision_law(n, d, sites, calls)
    assert Fraction(report["exact_IID_expected_collision_density"]) == total / banks


def test_nonunits_and_mod3_collapse_are_not_mislabeled_uniform():
    assert P.local_difference_counts(2)[3, 0] == 2
    law9 = P.iid_path_collision_law(1, 2, 1, 2)
    assert [s["local_count"] for s in law9["ideal_strata"]] == [54, 12, 15]
    assert law9["exact_IID_expected_collision_density"] == "25/81"
    assert Fraction("25/81") != Fraction("67/243")
    law3 = P.iid_path_collision_law(1, 1, 1, 2)
    assert [s["local_count"] for s in law3["ideal_strata"]] == [54, 27]
    assert law3["exact_IID_expected_collision_density"] == "5/9"
    assert not law9["collision_density_is_arbitrary_mixer_acceptance"]


def test_higher_calls_generate_higher_valuation_and_exact_partition():
    law = P.iid_path_collision_law(2, 3, 4, 6)
    assert law["ideal_strata"][2]["local_count"] > 0
    assert sum(s["all_sites_path_pair_count"] for s in law["ideal_strata"]) == law["total_ordered_path_pairs"]
    assert sum(Fraction(s["collision_density_contribution"]) for s in law["ideal_strata"]) == Fraction(law["exact_IID_expected_collision_density"])


@pytest.mark.parametrize("bad", (0, -1, True, 1.5))
def test_exact_integer_inputs_and_caps_fail_without_claiming_negative(bad):
    with pytest.raises(ValueError):
        P.local_difference_counts(bad)
    with pytest.raises(ValueError):
        P.iid_path_collision_law(1, 2, bad, 2)


def test_work_caps_do_not_silently_change_the_law():
    with pytest.raises(ValueError):
        P.local_difference_counts(9, max_work=1)
    with pytest.raises(ValueError):
        P.iid_path_collision_law(128, 128, 16384, 9)


@pytest.mark.parametrize("control_index", (0, 1, 2))
def test_exact_readout_matches_dense_actual_unitary_and_same_data_FFT(control_index):
    c = stored()["weighted_unitary_interleaving_controls"][control_index]
    a = c["actual_public_data_readout"]
    D, q = a["word_dimension"], a["modulus"]
    phases = np.exp(2j * np.pi * np.array([r["known_phase"] for r in a["actual_word_rows"]]) / q)
    Fourier = np.exp(2j * np.pi * np.outer(np.arange(D), np.arange(D)) / D) / np.sqrt(D)
    assert np.allclose(Fourier.conj().T @ Fourier, np.eye(D), atol=1e-12)
    psi = Fourier.conj().T @ (phases * (Fourier @ (phases / np.sqrt(D))))
    probabilities = np.abs(psi) ** 2
    exact = np.array([value(p, a["root_order"]) for p in a["exact_all_outcome_probabilities"]])
    assert np.max(np.abs(exact.imag)) < 1e-12
    assert np.allclose(exact.real, probabilities, atol=1e-12)
    assert np.allclose(a["classical_same_data_FFT_probabilities"], probabilities, atol=1e-12)
    assert abs(sum(exact) - 1) < 1e-12
    assert not a["classical_FFT_cost_is_polynomial_in_sites"]
    assert not a["unknown_phase_oracle_or_truth_used"]


@pytest.mark.parametrize("control_index", (0, 1, 2))
def test_weighted_pinching_matches_independent_dense_secret_census(control_index):
    c = stored()["weighted_unitary_interleaving_controls"][control_index]
    a = c["actual_public_data_readout"]
    rows, q, D = a["actual_word_rows"], a["modulus"], a["word_dimension"]
    errors = c["calibration_only"]["original_errors"]
    n = len(rows[0]["frequency"])
    ephase = [sum(b * e for j, t in enumerate(row["word"])
                  for b, e in zip(P.DIGITS[t], errors[2*j:2*j+2])) % q for row in rows]
    Fourier = np.exp(2j * np.pi * np.outer(np.arange(D), np.arange(D)) / D) / np.sqrt(D)
    mean = np.zeros(D)
    for secret in product(range(q), repeat=n):
        phases = np.exp(2j * np.pi * np.array([(sum(x*y for x,y in zip(row["frequency"], secret)) + e) % q
                                            for row, e in zip(rows, ephase)]) / q)
        state = Fourier.conj().T @ (phases * (Fourier @ (phases / np.sqrt(D))))
        mean += np.abs(state) ** 2 / (q ** n)
    exact = [value(p, a["root_order"]).real for p in c["weighted_additive_pinching_all_outcomes"]]
    assert np.allclose(exact, mean, atol=1e-12)
    assert c["weighted_additive_pinching_all_outcomes"] == c["uniform_secret_mean_all_outcomes"]


def test_public_readout_recomputes_without_private_truth_or_error_advice():
    c = stored()["weighted_unitary_interleaving_controls"][0]
    raw = tuple(NoisyLinearRecord(tuple(r["label"]), r["value"], r["modulus"], r["source_id"])
                for r in c["original_records"])
    recomputed = P.fourier_interleaved_readout(raw, c["actual_public_data_readout"]["public_mask"])
    assert P.exact_json(recomputed) == c["actual_public_data_readout"]
    assert "calibration_only" not in recomputed
    with pytest.raises(ValueError):
        P.fourier_interleaved_readout(raw, (True,))
    with pytest.raises(ValueError):
        P.fourier_interleaved_readout(raw + raw, (0,))


def test_two_copy_projection_is_not_single_register_fourier_interleaving():
    raw = (NoisyLinearRecord((1,), 1, 9, "a"), NoisyLinearRecord((2,), 2, 9, "b"))
    a = P.fourier_interleaved_readout(raw, (0,))
    phases = np.exp(2j * np.pi * np.array([r["known_phase"] for r in a["actual_word_rows"]]) / 9)
    two_copy_acceptance = abs(sum(phases)) ** 4 / 3 ** 4
    actual_zero = value(a["exact_all_outcome_probabilities"][0], 9).real
    assert abs(actual_zero - two_copy_acceptance) > 0.01


def test_independent_JS_checker_accepts_report():
    result = node_check(stored())
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["weighted_unitary_controls"] == 3


@pytest.mark.parametrize("kind", ("valuation-count", "collision-mean", "unit-claim", "public-phase",
    "probability", "FFT", "pinching", "calibration", "amplitude-cost", "oracle", "speedup", "hash"))
def test_independent_JS_checker_rejects_tampering(kind):
    report = deepcopy(stored())
    law = report["IID_path_collision_profiles"][1]
    c = report["weighted_unitary_interleaving_controls"][0]
    a = c["actual_public_data_readout"]
    if kind == "valuation-count": law["ideal_strata"][1]["local_count"] += 1
    elif kind == "collision-mean": law["exact_IID_expected_collision_density"] = "67/243"
    elif kind == "unit-claim": law["nonzero_coefficients_assumed_units"] = True
    elif kind == "public-phase": a["actual_word_rows"][0]["known_phase"] ^= 1
    elif kind == "probability": a["exact_all_outcome_probabilities"][0] = ["2"]
    elif kind == "FFT": a["classical_same_data_FFT_probabilities"][0] += 0.1
    elif kind == "pinching": c["weighted_additive_pinching_all_outcomes"][0] = []
    elif kind == "calibration": c["calibration_only"]["original_errors"][0] += 1
    elif kind == "amplitude-cost": a["classical_FFT_cost_is_polynomial_in_sites"] = True
    elif kind == "oracle": a["unknown_phase_oracle_or_truth_used"] = True
    elif kind == "speedup": report["accepted_speedup_candidate"] = True
    else: report["producer_sha256"] = "0" * 64
    assert node_check(report).returncode != 0
