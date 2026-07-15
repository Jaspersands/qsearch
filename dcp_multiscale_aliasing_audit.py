"""Access no-go audit for raw-label and pair-difference multiscale DCP decoders."""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


DCP_MULTISCALE_ALIASING_PATH = Path("research/classical_baselines/dcp_multiscale_aliasing_audit.json")
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-MULTISCALE-ALIASING"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class MultiscaleAliasingCertificate:
    n_bits: int
    effective_modulus_bits: int
    required_two_adic_valuation: int
    polynomial_sample_power: int
    polynomial_sample_budget: int
    raw_label_hit_probability: float
    expected_raw_hits: float
    raw_hit_union_bound: float
    expected_pair_hits: float
    pair_hit_union_bound: float
    log2_samples_for_expected_raw_hit: float
    log2_samples_for_expected_pair_hit: float
    raw_polynomial_access_ruled_out: bool
    pair_polynomial_access_ruled_out: bool
    chosen_label_shortcut_legal: bool


@dataclass(frozen=True)
class DCPMultiscaleAliasingReport:
    created_at: str
    access_contract: dict[str, str]
    certificates: list[MultiscaleAliasingCertificate]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def certify_multiscale_aliasing(
    n_bits: int,
    effective_modulus_bits: int,
    polynomial_sample_power: int = 3,
) -> MultiscaleAliasingCertificate:
    if n_bits < 2 or not 1 <= effective_modulus_bits <= n_bits or polynomial_sample_power < 1:
        raise ValueError("invalid multiscale aliasing parameters")
    valuation = n_bits - effective_modulus_bits
    budget = n_bits**polynomial_sample_power
    hit_probability = 2.0 ** (-valuation)
    expected_raw = budget * hit_probability
    pair_count = budget * (budget - 1) / 2.0
    expected_pair = pair_count * hit_probability
    log2_raw = float(valuation)
    # q(q-1)/2 * 2^-valuation ~= 1.
    log2_pair = 0.5 * (valuation + 1.0)
    inverse_polynomial_threshold = n_bits ** (-polynomial_sample_power)
    return MultiscaleAliasingCertificate(
        n_bits=n_bits,
        effective_modulus_bits=effective_modulus_bits,
        required_two_adic_valuation=valuation,
        polynomial_sample_power=polynomial_sample_power,
        polynomial_sample_budget=budget,
        raw_label_hit_probability=hit_probability,
        expected_raw_hits=expected_raw,
        raw_hit_union_bound=min(1.0, expected_raw),
        expected_pair_hits=expected_pair,
        pair_hit_union_bound=min(1.0, expected_pair),
        log2_samples_for_expected_raw_hit=log2_raw,
        log2_samples_for_expected_pair_hit=log2_pair,
        raw_polynomial_access_ruled_out=expected_raw < inverse_polynomial_threshold,
        pair_polynomial_access_ruled_out=expected_pair < inverse_polynomial_threshold,
        chosen_label_shortcut_legal=False,
    )


def run_multiscale_aliasing_report(
    n_values: Sequence[int] = (32, 64, 128, 256, 512, 1024),
    effective_bit_multipliers: Sequence[float] = (1.0, 2.0),
    polynomial_sample_power: int = 3,
) -> DCPMultiscaleAliasingReport:
    certificates = []
    for n_bits in n_values:
        for multiplier in effective_bit_multipliers:
            effective_bits = min(n_bits, max(1, int(math.ceil(multiplier * math.log2(n_bits)))))
            certificates.append(
                certify_multiscale_aliasing(n_bits, effective_bits, polynomial_sample_power)
            )
    asymptotic_tail = [item for item in certificates if item.n_bits >= 128]
    metrics: dict[str, int | float] = {
        "certificate_count": len(certificates),
        "asymptotic_tail_count": len(asymptotic_tail),
        "raw_polynomial_access_ruled_out_count": sum(item.raw_polynomial_access_ruled_out for item in certificates),
        "pair_polynomial_access_ruled_out_count": sum(item.pair_polynomial_access_ruled_out for item in certificates),
        "tail_raw_polynomial_access_ruled_out_count": sum(
            item.raw_polynomial_access_ruled_out for item in asymptotic_tail
        ),
        "tail_pair_polynomial_access_ruled_out_count": sum(
            item.pair_polynomial_access_ruled_out for item in asymptotic_tail
        ),
        "minimum_tail_log2_raw_samples": min(
            (item.log2_samples_for_expected_raw_hit for item in asymptotic_tail), default=0.0
        ),
        "minimum_tail_log2_pair_samples": min(
            (item.log2_samples_for_expected_pair_hit for item in asymptotic_tail), default=0.0
        ),
        "proved_general_random_label_decoder_lower_bound_count": 0,
    }
    falsifiers = [
        "A raw random Fourier label has valuation at least n-b with probability exactly 2^-(n-b); polynomial samples do not expose b=O(log n) effective moduli asymptotically.",
        "A pair difference has the same valuation probability, so birthday pairing needs about 2^((n-b)/2) labels before one useful collision is expected.",
        "Requesting powers-of-two or repeated high-valuation labels changes the DCP access model.",
        "The certificate rules out raw-label and one-pair aliasing templates only; deeper quantum collimation and other global decoders remain outside its scope."
    ]
    claim_gate = {
        "raw_label_multiscale_polynomial": False,
        "pair_difference_multiscale_polynomial": False,
        "chosen_label_phase_estimation_legal": False,
        "general_random_label_decoder_lower_bound_proved": False,
        "speedup_claim_allowed": False,
        "reason": (
            "Simple raw and pairwise multiscale aliasing are exponentially sample-limited for logarithmic effective "
            "moduli. This does not rule out deeper global decoding architectures."
        ),
    }
    summary = (
        f"Certified {len(certificates)} random-label multiscale rows. In the n>=128 tail, raw-label access is ruled "
        f"out in {int(metrics['tail_raw_polynomial_access_ruled_out_count'])}/{len(asymptotic_tail)} rows and pair access "
        f"in {int(metrics['tail_pair_polynomial_access_ruled_out_count'])}/{len(asymptotic_tail)}; no general decoder lower bound was claimed."
    )
    return DCPMultiscaleAliasingReport(
        created_at=utc_now(),
        access_contract={
            "labels": "independent uniform k in Z_(2^n)",
            "raw_aliasing_event": "k divisible by 2^(n-b), giving an effective modulus at most 2^b",
            "pair_aliasing_event": "k_i-k_j divisible by 2^(n-b)",
            "illegal_shortcut": "request a chosen high-valuation or repeated label",
        },
        certificates=certificates,
        headline_metrics=metrics,
        claim_gate=claim_gate,
        status="raw-and-pair-multiscale-decoders-obstructed",
        summary=summary,
        falsifiers_triggered=falsifiers,
    )


def write_multiscale_aliasing_report(
    path: Path = DCP_MULTISCALE_ALIASING_PATH,
    n_values: Sequence[int] = (32, 64, 128, 256, 512, 1024),
    effective_bit_multipliers: Sequence[float] = (1.0, 2.0),
    polynomial_sample_power: int = 3,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    report = run_multiscale_aliasing_report(
        n_values=n_values,
        effective_bit_multipliers=effective_bit_multipliers,
        polynomial_sample_power=polynomial_sample_power,
    )
    payload = asdict(report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-RANDOM-LABEL-RAW-PAIR-MULTISCALE-ALIASING",
                source=str(path),
                claim="Polynomially many random DCP labels directly supply the high-valuation aliases needed for bitwise phase estimation.",
                reason_invalid=(
                    "Raw useful labels occur with probability 2^-(n-b), and useful pair differences require birthday "
                    "sample scale 2^((n-b)/2) for b=O(log n)."
                ),
                lesson="Reject chosen-label shortcuts and simple pair aliasing; search deeper global random-label decoders.",
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=payload["headline_metrics"],
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-DCP-MULTISCALE-ALIASING"
        upsert_experiment_result(
            ExperimentResultRecord(
                id=result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=payload["created_at"],
                status=payload["status"],
                summary=payload["summary"],
                metrics=payload["headline_metrics"],
                falsifiers_triggered=payload["falsifiers_triggered"],
                artifacts={"dcp_multiscale_aliasing": str(path)},
            )
        )
    return payload
