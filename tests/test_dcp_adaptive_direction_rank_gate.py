"""Original phase, exhaustive GF(2), rank-bound and scope falsifiers."""
from collections import Counter
from copy import deepcopy
from fractions import Fraction
from itertools import product
import json
import math
from pathlib import Path
import subprocess
import sys

import numpy as np
import pytest
from sympy import symbols, expand

from theorems.dcp_adaptive_direction_rank_gate import (
    CONTRACT, REPORT, SELECTION, binary_basis, binary_kernel, binary_map,
    build_report, connectivity_rank, decode_dyadic, direct_complement_census,
    native_bound, posterior_law, rank_pair_exponent,
)
from theorems.dcp_carry_packets import compile_packet

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "research/certificates/dcp_adaptive_direction_rank_gate_crosscheck.js"


@pytest.fixture(scope="module")
def report():
    return build_report()


def test_complete_small_original_phase_labels_not_only_affine_formula():
    checked = 0
    for row in product(range(8), repeat=3):
        B = sum((a & 1) << i for i, a in enumerate(row))
        for u in range(1, 8):
            if (B & u).bit_count() & 1:
                continue
            for x0 in range(8):
                law = posterior_law((row,), 3, u, x0)
                census = direct_complement_census((row,), 3, u, x0)
                assert law["extra_descent_probability"] == census["extra_descent_probability"]
                hist = census["low_output_histogram"]
                assert len(hist) == 1 << law["posterior_rank"]
                assert len(set(hist.values())) == 1
                checked += 1
    assert checked == 14336


@pytest.mark.parametrize("t", [3, 4])
@pytest.mark.parametrize("secret", [(0, 0), (1, 0), (0, 1), (3, 5)])
def test_physical_chart_measurement_flatness_and_actual_conditional_density(t, secret):
    labels = ((1, 0, 3, 5), (0, 1, 1, 2))
    q = 1 << t
    first = compile_packet(labels, q)
    m, rank = first.input_qubits, len(first.pivots)
    for syndrome in range(1 << rank):
        packet = compile_packet(labels, q, syndrome)
        assignments = [sum(bit << i for i, bit in enumerate(packet.assignment(z)))
                       for z in range(1 << packet.retained_qubits)]
        chart_mass = Fraction(len(assignments), 1 << m)
        assert chart_mass == Fraction(1, 1 << rank)
        origin = sum(bit << i for i, bit in enumerate(packet.origin))
        for logical in range(1, 1 << packet.retained_qubits):
            physical = sum(((row & logical).bit_count() & 1) << i
                           for i, row in enumerate(packet.kernel_rows))
            law = posterior_law(labels, t, physical, origin)
            census = direct_complement_census(labels, t, physical, origin)
            assert len(census["physical_complement_pairs"]) == 1 << (packet.retained_qubits - 1)
            mass = 0.0
            for pair in census["physical_complement_pairs"]:
                x, y = int(pair["x_hex"], 16), int(pair["x_xor_u_hex"], 16)
                assert x in assignments and y in assignments
                def original_amplitude(z):
                    phase = sum(s * a * ((z >> i) & 1)
                                for s, row in zip(secret, labels) for i, a in enumerate(row)) % q
                    return np.exp(2j * math.pi * phase / q) / math.sqrt(1 << m)
                amplitudes = np.array([original_amplitude(x), original_amplitude(y)])
                raw_mass = float(np.vdot(amplitudes, amplitudes).real)
                assert raw_mass == pytest.approx(2 / (1 << m))
                mass += raw_mass / float(chart_mass)
                state = amplitudes / math.sqrt(raw_mass)
                output = tuple(int(v, 16) for v in pair["output_label_hex"])
                angle = 2 * math.pi * (sum(s * v for s, v in zip(secret, output)) % (q // 2)) / (q // 2)
                predicted = np.array([1, np.exp(1j * angle)]) / math.sqrt(2)
                assert np.allclose(np.outer(state, state.conj()),
                                   np.outer(predicted, predicted.conj()), atol=2e-14)
            assert mass == pytest.approx(1.0)
            assert law["extra_descent_probability"] == census["extra_descent_probability"]


def test_high_label_selector_really_changes_direction_and_zero_background_does_not_force_descent(report):
    controls = [c for c in report["physical_controls"]
                if c["selector"].startswith("min(") and c["law"]["physical_origin_hex"] == "0x0"]
    assert len({c["law"]["physical_direction_hex"] for c in controls}) > 1
    assert len({tuple(c["law"]["low_rows_hex"]) for c in controls}) == 1
    for c in controls:
        law = c["law"]
        assert law["affine_low_output_offset_hex"] == "0x0"
        assert 0 < decode_dyadic(law["extra_descent_probability"]) < 1


def test_rank_zero_exceptions_and_inconsistent_affine_targets_are_not_discarded(report):
    laws = [c["law"] for c in report["physical_controls"]]
    assert any(l["posterior_rank"] == 0 and decode_dyadic(l["extra_descent_probability"]) == 1 for l in laws)
    assert any(not l["all_even_output_attainable"] and decode_dyadic(l["extra_descent_probability"]) == 0 for l in laws)
    # The all-one kernel direction has T_u=B|ker B=0, even for nonzero B.
    law = posterior_law(((1, 1, 1, 1),), 3, 15)
    assert law["posterior_rank"] == 0
    assert decode_dyadic(law["extra_descent_probability"]) == 1


def test_rank_probability_count_bound_against_every_small_matrix():
    for n in range(1, 4):
        for s in range(1, 5):
            counts = Counter(len(binary_basis(rows, s)) for rows in product(range(1 << s), repeat=n))
            for a in range(min(n, s) + 1):
                cdf = Fraction(sum(v for r, v in counts.items() if r <= a), 1 << (n * s))
                assert cdf <= 4 * Fraction(1, 1 << ((n - a) * (s - a)))


def test_rank_pair_minimization_proof_polynomial_identities():
    n, s, k, a = symbols("n s k a")
    E = rank_pair_exponent(n, s, a, n + k - a)
    boundary = (n - k) * (s - k)
    vertex = s / 2 + k / 2 - n / 4
    interior = (n - k) * (2 * n - k) / 2 - (3 * n / 2 - s)**2 / 2
    assert expand(E - boundary - (a - k) * (2 * a + n - 2 * s)) == 0
    assert expand(E - interior - 2 * (a - vertex)**2) == 0
    assert expand(boundary.subs(s, n / 2 + k) - interior.subs(s, n / 2 + k)) == 0
    assert expand(interior.diff(s) - (3 * n / 2 - s)) == 0


def test_native_bound_exact_scaling_vacuity_and_scope(report):
    rows = report["native_source_bounds"]
    assert rows[0]["source_bound_vacuous"] is True
    for row in rows[1:]:
        n, r = row["dimension"], row["uniform_cut_rank_lower_bound"]
        fail = decode_dyadic(row["bad_low_matrix_probability_upper_bound"])
        mean = decode_dyadic(row["native_source_mean_extra_descent_upper_bound"])
        assert 0 <= fail < Fraction(1, 1000000)
        assert mean == fail + (1 - fail) * Fraction(1, 1 << r)
        assert row["native_mean_before_source_or_syndrome_postselection"] is True
        assert n >= 64
    assert rows[-1]["uniform_cut_rank_lower_bound"] == 48
    assert decode_dyadic(rows[-1]["native_source_mean_extra_descent_upper_bound"]) < Fraction(1, 1 << 47)
    assert report["scope"]["n_is_secret_vector_component_count_not_log_cyclic_modulus"] is True


@pytest.mark.parametrize("kwargs", [
    {"selection_model": "after-complement"}, {"noise_model": "mixed-noisy"},
    {"direction": 0}, {"direction": True}, {"direction": 1},
    {"origin": -1}, {"phase_bits": 2}, {"labels": ((1.0, 1.0),)},
])
def test_missing_lineage_or_model_mismatch_cannot_inherit_certificate(kwargs):
    args = dict(labels=((1, 1),), phase_bits=3, direction=3)
    args.update(kwargs)
    with pytest.raises(ValueError):
        posterior_law(**args)


def test_binary_certificate_handles_large_masks_without_number_rounding():
    width = 256
    rows = ((1 << 255) | 1, (1 << 200) | 2)
    kernel = binary_kernel(rows, width)
    assert len(kernel) == 254
    assert all(binary_map(rows, w) == 0 for w in kernel)
    assert len(binary_basis(kernel, width)) == 254
    assert connectivity_rank(rows, width, (1 << 255) | 1) == 0


def check_js(payload, tmp_path):
    target = tmp_path / "certificate.json"
    target.write_text(json.dumps(payload))
    return subprocess.run(["node", str(CHECKER), str(target)], capture_output=True, text=True)


def test_independent_replay_and_live_artifact_provenance(report, tmp_path):
    assert json.loads(REPORT.read_text()) == report
    assert json.loads(CONTRACT.read_text())["accepted_speedup_candidate"] is False
    result = check_js(report, tmp_path)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["rank_minima"] == 40


@pytest.mark.parametrize("mutation", ["image", "probability", "pair", "scope", "exponent", "target", "kernel", "negative"])
def test_independent_replay_rejects_corrupted_certificates(report, tmp_path, mutation):
    broken = deepcopy(report)
    law = broken["physical_controls"][0]["law"]
    if mutation == "image":
        law["kernel_image_basis_hex"] = []
    elif mutation == "probability":
        law["extra_descent_probability"]["numerator_hex"] = "0x0"
    elif mutation == "pair":
        broken["physical_controls"][0]["direct_census"]["physical_complement_pairs"][0]["output_label_hex"][0] = "0x7"
    elif mutation == "scope":
        broken["scope"]["post_complement_selection_covered"] = True
    elif mutation == "exponent":
        broken["native_source_bounds"][1]["rank_pair_exponent_minimum"] += 1
    elif mutation == "target":
        law["affine_low_output_offset_hex"] = "0x1"
    elif mutation == "kernel":
        law["kernel_basis_hex"][0] = "0x0"
    else:
        broken["provisional_negative_result"]["status"] = "PROVED_GENERAL_NO_GO"
    assert check_js(broken, tmp_path).returncode != 0


def test_cli_read_only_mode_does_not_rewrite_artifact():
    before = REPORT.read_bytes()
    result = subprocess.run([sys.executable, "qsearch.py", "dcp-adaptive-direction-rank-gate", "--no-write"],
                            cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["accepted_speedup_candidate"] is False
    assert REPORT.read_bytes() == before


@pytest.mark.parametrize("n,w,r", [(1, None, None), (True, None, None), (64, 40, 1), (64, 6, 7), (64, 6, 0)])
def test_bad_native_bound_parameters_rejected(n, w, r):
    with pytest.raises(ValueError):
        native_bound(n, w, r)
