"""Generate the scoped negative-transfer receipt; no central registry writes."""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
from itertools import product
import json
from pathlib import Path

from native_sketch import (NativeRecord, dot, exact_quarter_turn_probability,
                           finite_channel_control, resource_ledger, support_bound,
                           ternary_correlation)

ROOT = Path(__file__).resolve().parent


def encode(value):
    if isinstance(value, F):
        return str(value)
    raise TypeError(type(value).__name__)


def build_receipt():
    secret = (2, 1)
    labels = tuple(product(range(3), repeat=2))
    noiseless = tuple(NativeRecord(a, dot(a, secret) % 3, 3, str(j)) for j, a in enumerate(labels[:5]))
    balanced = tuple(NativeRecord(a, (dot(a, secret)+e) % 3, 3, f"{j}:{k}")
                     for j, a in enumerate(labels) for k, e in enumerate((0, 0, 0, 0, 1, -1)))
    classical = ternary_correlation(balanced)
    sources = ["native_sketch.py", "test_native_sketch.py", "replay.py", "ORACLE_SKETCH_ACCESS.md", "HANDOFF.md"]
    return {"status": "SOURCE_TRANSFER_REJECTED_FOR_POLYNOMIAL_NATIVE_RECOVERY",
            "scope": "address-local oracle sketch plus branch-1 Fourier recovery on original noisy-linear records",
            "literature": {"id": "arxiv:2604.07639v2", "url": "https://arxiv.org/abs/2604.07639v2",
                           "pdf_sha256": "b6b34b46e241c842e82d2576aff893fe46ec1f46fa4c15bec9a564a981c13f2f",
                           "sections": ["Algorithm 1 p50", "Theorem D.12 pp53-55", "Theorem D.16 pp60-62"]},
            "proof_status": "LOCAL_DERIVATION_NOT_INDEPENDENTLY_REVIEWED_OR_FORMALIZED",
            "native_authority": "theorems/native_noisy_phase_input.py:prepare_inputs",
            "native_authority_read_only_sha256_2026_10_24": {
                "theorems/native_noisy_phase_input.py": "d88c46217853fe1c264322fbbea1e94f58cd1aec28bc6875a1bd70cf7cb8bf7f",
                "research/NATIVE_NOISY_PHASE_INPUT.md": "8a26ef6a7d9f825b1298cce2fca04e5f9109d21ae87d92428c9802b5b735b423",
                "theorems/ternary_noise_degradation.py": "def0aebaf71b7bbd0a659993c3181b28c10b2ae26563cb4dbd7a74f26fd4fde4"},
            "new_source_oracle_granted": False, "copy_only_receiver_implemented": False,
            "quantum_gates_executed": 0, "accepted_speedup_candidate": False,
            "all_native_algorithms_ruled_out": False, "source_paper_refuted": False,
            "linear_compression_scope": "first harmonic survives exactly on annihilator of fixed projection kernel",
            "vanishing_first_harmonic_proves_no_other_information": False,
            "control_fixture_is_hard_instance": False,
            "noiseless_equality_control": {"q": 3, "n": 2, "visited": 5,
                "diagnostic_secret_not_processor_input": secret,
                "exact_joint_probability_cyclotomic_coefficients": exact_quarter_turn_probability(noiseless, secret),
                "frozen_19_replay_joint_probability_cyclotomic_coefficients": exact_quarter_turn_probability(noiseless, secret, 19),
                "support_bounds": support_bound(3, 2, 5)},
            "balanced_noise_classical_control": {"fixture_law": "deterministic balanced counts, NOT an IID sample run",
                "records": len(balanced), "maximizers": classical["maximizers"],
                "true_score": classical["scores"][secret],
                "all_wrong_scores": sorted(set(score for s, score in classical["scores"].items() if s != secret)),
                "hypotheses_enumerated": classical["hypotheses_enumerated"]},
            "floating_point_channel_controls_not_proofs": [finite_channel_control(
                3, 1, (2,), {0: F(2, 3), 1: F(1, 6), 2: F(1, 6)}, M) for M in [3, 12, 48, 192]],
            "favorable_visibility_one_cost_ledgers_not_hard_instances": [
                resource_ledger(3**(2*n), n, F(1)) for n in [8, 16, 32]],
            "falsifier": "constant correct-herald Fourier success with v=o(q^n) under the exact local-update scope",
            "reopen_only_for": "a specified different native mechanism with proved end-to-end cost and matched classical comparison",
            "sha256": {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in sources}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rendered = json.dumps(build_receipt(), default=encode, sort_keys=True, indent=2)+"\n"
    if args.output:
        args.output.write_text(rendered)
        print(args.output.resolve())
    else:
        print(rendered, end="")
