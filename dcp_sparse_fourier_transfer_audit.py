"""Audit sparse-Fourier localization mechanisms against random-label DCP access."""

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


DCP_SPARSE_FOURIER_AUDIT_PATH = Path("research/classical_baselines/dcp_sparse_fourier_transfer_audit.json")
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-SPARSE-FOURIER-TRANSFER-AUDIT"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class FourierMechanismTransfer:
    method_id: str
    supplied_input: str
    required_primitive: str
    access_status: str
    time_class_in_n: str
    memory_class_in_n: str
    obstruction_or_open_bridge: str
    literature_ids: list[str]
    source_locator: str


@dataclass(frozen=True)
class CorrelatedClosureCertificate:
    n_bits: int
    modulus: int
    sample_budget_power: int
    sample_budget: int
    prescribed_offset_count_power: int
    prescribed_offset_count: int
    signed_combination_arity: int
    log2_union_bound: float
    union_bound: float
    inverse_polynomial_coverage_ruled_out: bool
    interpretation: str


@dataclass(frozen=True)
class DCPSparseFourierTransferReport:
    created_at: str
    dcp_access_contract: dict[str, str]
    mechanism_transfers: list[FourierMechanismTransfer]
    closure_certificates: list[CorrelatedClosureCertificate]
    headline_metrics: dict[str, int | float]
    open_adaptation_contract: dict[str, str]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def correlated_closure_certificate(
    n_bits: int,
    sample_budget_power: int = 3,
    prescribed_offset_count_power: int = 2,
    signed_combination_arity: int = 2,
) -> CorrelatedClosureCertificate:
    """Union-bound a constant-arity attempt to synthesize prescribed labels.

    From m public random labels, at most (2m)^r signed ordered expressions of
    arity r are available.  Each nondegenerate expression is uniform in Z_N,
    so coverage of q prescribed offsets is at most q(2m)^r/N.  This is a
    restricted template bound, not a general random-example decoding lower
    bound.
    """
    if n_bits < 2:
        raise ValueError("n_bits must be at least 2")
    if sample_budget_power < 1 or prescribed_offset_count_power < 0:
        raise ValueError("polynomial powers must be nonnegative, with positive sample power")
    if signed_combination_arity < 1:
        raise ValueError("signed_combination_arity must be positive")
    modulus = 1 << n_bits
    samples = n_bits**sample_budget_power
    offsets = max(1, n_bits**prescribed_offset_count_power)
    log2_bound = (
        math.log2(offsets)
        + signed_combination_arity * (1.0 + math.log2(samples))
        - n_bits
    )
    bound = 1.0 if log2_bound >= 0.0 else 2.0**log2_bound
    threshold = 1.0 / n_bits
    ruled_out = log2_bound < math.log2(threshold)
    return CorrelatedClosureCertificate(
        n_bits=n_bits,
        modulus=modulus,
        sample_budget_power=sample_budget_power,
        sample_budget=samples,
        prescribed_offset_count_power=prescribed_offset_count_power,
        prescribed_offset_count=offsets,
        signed_combination_arity=signed_combination_arity,
        log2_union_bound=log2_bound,
        union_bound=bound,
        inverse_polynomial_coverage_ruled_out=ruled_out,
        interpretation=(
            "Polynomial iid labels cannot supply even one of the prescribed correlated offsets through this "
            "constant-arity signed-combination template at inverse-polynomial probability."
            if ruled_out
            else "The finite-size union bound is inconclusive; it is not positive evidence for a decoder."
        ),
    )


def build_mechanism_transfers() -> list[FourierMechanismTransfer]:
    return [
        FourierMechanismTransfer(
            method_id="significant-fourier-query-access",
            supplied_input="an evaluator queried at adaptively or nonadaptively selected correlated group elements",
            required_primitive="queries at x and x+h, subgroup restrictions, and repeated evaluation patterns",
            access_status="invalid-for-random-label-dcp",
            time_class_in_n="poly(n) under the stronger query oracle",
            memory_class_in_n="poly(n)",
            obstruction_or_open_bridge="DCP supplies iid labels after state measurement and cannot request the correlated query pattern.",
            literature_ids=["galbraith-laity-shani-fourier-limitations-2016"],
            source_locator="arXiv:1607.01842, random-access/query-access definitions and LPN limitation section",
        ),
        FourierMechanismTransfer(
            method_id="kapralov-hash-to-bins",
            supplied_input="time-domain signal values at locations selected by randomized hash functions and filters",
            required_primitive="filtered HashToBins measurements at shifted locations and randomly correlated sample pairs",
            access_status="invalid-direct-transfer",
            time_class_in_n="poly(n) for one-sparse spectra with legal structured samples",
            memory_class_in_n="poly(n)",
            obstruction_or_open_bridge=(
                "Marginally random locations are insufficient: the locator constructs shared hash functions, shifts, "
                "filters, and correlated pairs. An iid-example estimator for the same bins is not supplied."
            ),
            literature_ids=["kapralov-sparse-fourier-2016"],
            source_locator="arXiv:1604.00845 source algo.tex:6 and preliminaries.tex:128",
        ),
        FourierMechanismTransfer(
            method_id="iid-fourier-compressed-sensing",
            supplied_input="iid random rows of a partial Fourier design with noisy bounded responses",
            required_primitive="solve a one-sparse inverse problem from an unstructured random design",
            access_status="access-compatible-computational-cost-open",
            time_class_in_n="generic solvers are poly(N), not certified poly(n)",
            memory_class_in_n="generic formulations materialize N candidate coordinates",
            obstruction_or_open_bridge=(
                "Random measurement compatibility resolves sample access only. The repository has no certified implicit "
                "solver whose arithmetic and storage are polynomial in n=log2(N)."
            ),
            literature_ids=["kapralov-sparse-fourier-2016"],
            source_locator="comparison class; no direct-transfer theorem claimed",
        ),
        FourierMechanismTransfer(
            method_id="full-periodogram-or-fft",
            supplied_input="iid random DCP quadrature records",
            required_primitive="score all N frequencies or run a length-N transform",
            access_status="legal-but-exponential",
            time_class_in_n="Theta(N log N)=2^Theta(n)",
            memory_class_in_n="Theta(N)=2^Theta(n) for a one-pass score table",
            obstruction_or_open_bridge="It proves information recovery but loses to generic subexponential DCP sieves.",
            literature_ids=["internal:dcp-random-design-decoder"],
            source_locator="dcp_random_design_decoder.py",
        ),
        FourierMechanismTransfer(
            method_id="constant-arity-signed-label-closure",
            supplied_input="m=poly(n) iid public labels and local measurement outcomes",
            required_primitive="post-hoc products or signed combinations intended to synthesize prescribed offsets",
            access_status="legal-template-asymptotically-insufficient",
            time_class_in_n="poly(n) for fixed arity",
            memory_class_in_n="poly(n) for fixed arity",
            obstruction_or_open_bridge=(
                "The number of constant-arity expressions is polynomial and each nondegenerate label is uniform; prescribed "
                "offset coverage remains exponentially small. Products also compound measurement noise."
            ),
            literature_ids=["internal:dcp-multiscale-aliasing"],
            source_locator="exact union-bound certificates in this artifact",
        ),
        FourierMechanismTransfer(
            method_id="target-iid-random-example-localizer",
            supplied_input="iid random labels with bounded stochastic complex-character observations",
            required_primitive="implicit heavy-frequency localization without chosen samples or N-sized candidate state",
            access_status="open-research-target",
            time_class_in_n="target poly(n); no theorem",
            memory_class_in_n="target poly(n); no theorem",
            obstruction_or_open_bridge=(
                "A valid construction must estimate useful hash/alias statistics from iid records, prove variance and "
                "worst-frequency bounds, and remain robust under f=1 bad registers."
            ),
            literature_ids=["kapralov-sparse-fourier-2016", "galbraith-laity-shani-fourier-limitations-2016"],
            source_locator="new adaptation obligation; not present in cited algorithms",
        ),
    ]


def run_sparse_fourier_transfer_report(
    n_values: Sequence[int] = (64, 128, 256, 512, 1024),
    arities: Sequence[int] = (2, 3, 4),
    sample_budget_power: int = 3,
    prescribed_offset_count_power: int = 2,
) -> DCPSparseFourierTransferReport:
    certificates = [
        correlated_closure_certificate(
            n_bits,
            sample_budget_power=sample_budget_power,
            prescribed_offset_count_power=prescribed_offset_count_power,
            signed_combination_arity=arity,
        )
        for n_bits in n_values
        for arity in arities
    ]
    transfers = build_mechanism_transfers()
    tail = [row for row in certificates if row.n_bits >= 256]
    metrics: dict[str, int | float] = {
        "mechanism_count": len(transfers),
        "direct_access_invalid_count": sum("invalid" in row.access_status for row in transfers),
        "legal_but_exponential_count": sum(row.access_status == "legal-but-exponential" for row in transfers),
        "open_random_example_localizer_count": sum(row.access_status == "open-research-target" for row in transfers),
        "closure_certificate_count": len(certificates),
        "tail_certificate_count": len(tail),
        "tail_inverse_polynomial_coverage_ruled_out_count": sum(
            row.inverse_polynomial_coverage_ruled_out for row in tail
        ),
        "maximum_tail_union_bound": max((row.union_bound for row in tail), default=1.0),
        "proved_polylog_random_example_decoder_count": 0,
        "proved_general_random_example_lower_bound_count": 0,
        "proved_sparse_fft_transfer_count": 0,
    }
    falsifiers = [
        "Existing significant-Fourier and HashToBins algorithms construct chosen, shifted, or correlated sample schedules absent from DCP.",
        "Marginal randomness of a sparse-FFT query schedule does not make its joint distribution iid.",
        "Constant-arity signed closure of polynomially many iid labels does not cover polynomially many prescribed offsets asymptotically.",
        "Generic compressed sensing and full periodograms preserve random access but hide N-dimensional time or memory.",
        "The restricted closure bound is not a general lower bound against a new random-example estimator.",
    ]
    return DCPSparseFourierTransferReport(
        created_at=utc_now(),
        dcp_access_contract={
            "labels": "independent uniform k in Z_(2^n), supplied rather than chosen",
            "observations": "one stochastic X/Y outcome per phase register",
            "available_postprocessing": "polynomial-time classical processing of public labels and outcomes",
            "unavailable": "evaluator, repeated labels, chosen shifts, filter queries, coherent score oracle",
        },
        mechanism_transfers=transfers,
        closure_certificates=certificates,
        headline_metrics=metrics,
        open_adaptation_contract={
            "input": "iid records (k,B,z) from the exact DCP measurement channel",
            "output": "the complete d in Z_(2^n) with bounded error",
            "resources": "poly(n) states, time, memory, and bit precision",
            "required_novelty": "estimate and decode multiscale hash statistics from iid records without reconstructing missing query pairs",
            "robustness": "retain bounded error with hidden computational-basis bad registers at rate at most 1/n",
            "kill_test": "reject if any data structure, loop, oracle, preprocessing table, or advice has size N^Omega(1)",
        },
        claim_gate={
            "known_sparse_fft_directly_transfers": False,
            "constant_arity_query_schedule_synthesis_survives": False,
            "polylog_random_example_decoder_proved": False,
            "general_random_example_lower_bound_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Known polylog sparse-Fourier runtimes rely on structured sample schedules. Constant-arity attempts to "
                "recover those schedules from iid labels fail, while a genuinely new iid estimator remains open."
            ),
        },
        status="known-sparse-fourier-transfer-blocked-random-example-adaptation-open",
        summary=(
            f"Audited {len(transfers)} Fourier-localization mechanisms and {len(certificates)} constant-arity closure "
            f"certificates; {int(metrics['tail_inverse_polynomial_coverage_ruled_out_count'])}/"
            f"{int(metrics['tail_certificate_count'])} tail certificates rule out the tested schedule-synthesis template, "
            "with zero polylog iid decoders and zero general lower bounds proved."
        ),
        falsifiers_triggered=falsifiers,
    )


def write_sparse_fourier_transfer_report(
    path: Path = DCP_SPARSE_FOURIER_AUDIT_PATH,
    n_values: Sequence[int] = (64, 128, 256, 512, 1024),
    arities: Sequence[int] = (2, 3, 4),
    sample_budget_power: int = 3,
    prescribed_offset_count_power: int = 2,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    report = run_sparse_fourier_transfer_report(
        n_values=n_values,
        arities=arities,
        sample_budget_power=sample_budget_power,
        prescribed_offset_count_power=prescribed_offset_count_power,
    )
    payload = asdict(report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-SPARSE-FFT-CORRELATED-SAMPLE-TRANSFER",
                source=str(path),
                claim="A polylogarithmic sparse Fourier transform directly decodes iid random-label DCP records.",
                reason_invalid=(
                    "The audited SFT and HashToBins mechanisms construct chosen shifted, filtered, or correlated sample "
                    "locations. DCP supplies only iid labels and one stochastic outcome per label."
                ),
                lesson="Audit the joint sample schedule and primitive measurements, not only sample count and asymptotic runtime.",
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence={
                    "direct_access_invalid_count": payload["headline_metrics"]["direct_access_invalid_count"],
                    "proved_sparse_fft_transfer_count": 0,
                },
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-CONSTANT-ARITY-CORRELATED-SCHEDULE-SYNTHESIS",
                source=str(path),
                claim="A fixed number of signed combinations of polynomially many iid DCP labels synthesizes the prescribed sparse-FFT query offsets.",
                reason_invalid=(
                    "For the audited constant arities, q(2m)^r/N is negligible throughout the asymptotic tail. This "
                    "does not exclude a fundamentally different iid estimator."
                ),
                lesson="Do not mutate pair closure into triple or quadruple closure without checking exponential label-space coverage.",
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence={
                    "tail_certificate_count": payload["headline_metrics"]["tail_certificate_count"],
                    "tail_inverse_polynomial_coverage_ruled_out_count": payload["headline_metrics"][
                        "tail_inverse_polynomial_coverage_ruled_out_count"
                    ],
                    "proved_general_random_example_lower_bound_count": 0,
                },
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-DCP-SPARSE-FOURIER-TRANSFER"
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
                artifacts={"dcp_sparse_fourier_transfer_audit": str(path)},
            )
        )
    return payload
