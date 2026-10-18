"""Tests for dcp_bell_conjugate_pair_phase_cancellation_obstruction."""

from __future__ import annotations

import json
import subprocess
import itertools
import math
import random
from pathlib import Path

import pytest

from theorems.dcp_bell_conjugate_pair_phase_cancellation_obstruction import (
    generate_dcp_bell_conjugate_pair_phase_cancellation_certificate,
    verify_bell_measurement_law_and_sign_invariance,
    verify_random_header_transcript_simulation,
    simulate_random_header_bell,
    lift_random_x_observation,
    fixed_header_countercontrol,
    bell_probabilities_explicit_density,
)


@pytest.mark.parametrize("q,n", [(2, 1), (3, 1), (4, 1), (5, 1), (4, 2)])
def test_full_transcript_not_just_marginal_for_every_small_secret(q, n):
    for secret in itertools.product(range(q), repeat=n):
        record = verify_random_header_transcript_simulation(q, secret, 0.8, 0.8, 0.7)
        assert record["full_joint_law_verified"]
        assert record["transcripts_compared"] == 4 * q ** (2 * n)
        assert record["chosen_header_queries"] == 0


@pytest.mark.parametrize("gammas", [(0, 0, 1), (1, 1, 1), (0.25, 0.5, 0.5)])
def test_zero_and_boundary_source_coherence(gammas):
    assert verify_random_header_transcript_simulation(4, [1], *gammas)["full_joint_law_verified"]


def test_actual_sampler_uses_one_observation_and_public_randomness_only():
    calls = []

    def source():
        calls.append(1)
        return [2, 3], 1

    record = simulate_random_header_bell(4, source, random.Random(17), gamma_source=1,
                                         gamma_1=1, gamma_2=1)
    assert calls == [1]
    a1, a2 = record["a1"], record["a2"]
    combined = [(a + b if record["outcome"].startswith("Phi") else a - b) % 4
                for a, b in zip(a1, a2)]
    assert combined == [2, 3]
    assert record["outcome"].endswith("minus")


def test_public_lift_has_no_secret_and_bijects_headers_including_even_moduli():
    for q in (2, 4, 5):
        for branch in (0, 1):
            pairs = set()
            for h, a in itertools.product(range(q), repeat=2):
                r = lift_random_x_observation(q, [h], 0, [a], branch)
                pairs.add((tuple(r["a1"]), tuple(r["a2"])))
            assert len(pairs) == q * q


def test_prespecified_headers_counterexample_is_not_dequantized():
    record = fixed_header_countercontrol()
    assert record["bell_total_variation"] == pytest.approx(1)
    # Both individual X observations are exactly fair for either secret.
    for theta in (math.pi / 2, -math.pi / 2):
        assert (1 + math.cos(theta)) / 2 == pytest.approx(0.5)
    p = bell_probabilities_explicit_density(math.pi / 2, math.pi / 2, 1, 1)
    r = bell_probabilities_explicit_density(math.pi / 2, -math.pi / 2, 1, 1)
    assert sum(abs(p[k] - r[k]) for k in p) / 2 == pytest.approx(1)


@pytest.mark.parametrize("gammas", [(0.1, 1, 1), (-1, 0, 1), (float("nan"), 0, 1)])
def test_simulator_does_not_invent_coherence(gammas):
    with pytest.raises(ValueError):
        simulate_random_header_bell(4, lambda: ([1], 0), random.Random(1),
                                    gamma_source=gammas[0], gamma_1=gammas[1], gamma_2=gammas[2])


def test_bell_measurement_law_and_sign_invariance() -> None:
    res = verify_bell_measurement_law_and_sign_invariance(
        q=8, a1=[1, 3], a2=[2, 5], s_vec=[3, 1], gamma_1=0.8, gamma_2=0.7
    )
    assert res["exact_law_and_sign_invariance"] is True


def test_certificate_and_reduction_artifact_match() -> None:
    cert = generate_dcp_bell_conjugate_pair_phase_cancellation_certificate()
    assert cert["all_checks_passed"] is True
    artifact_path = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "reductions"
        / "dcp_bell_conjugate_pair_phase_cancellation_obstruction.json"
    )
    on_disk = json.loads(artifact_path.read_text(encoding="utf-8"))
    assert cert == on_disk


def test_nodejs_crosscheck() -> None:
    script = (
        Path(__file__).resolve().parent.parent
        / "research"
        / "certificates"
        / "dcp_bell_conjugate_pair_phase_cancellation_obstruction_crosscheck.js"
    )
    proc = subprocess.run(["node", str(script)], capture_output=True, text=True, check=True)
    data = json.loads(proc.stdout.strip())
    assert data["status"] == "OK"
