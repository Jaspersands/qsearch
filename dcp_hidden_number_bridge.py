"""Formal bridge from random-label DCP measurements to noisy Fourier learning.

The bridge is intentionally one-way.  Measuring a DCP phase state produces a
random-example complex-character record, but it does not provide the chosen
queries required by significant-Fourier-transform algorithms or by standard
chosen-multiplier hidden-number attacks.
"""

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


DCP_HIDDEN_NUMBER_BRIDGE_PATH = Path("research/reductions/dcp_hidden_number_bridge.json")
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-RANDOM-FOURIER-BRIDGE"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class BridgeEdge:
    id: str
    source_model: str
    target_model: str
    direction: str
    status: str
    mapping: str
    assumptions: list[str]
    proof_or_obstruction: str
    literature_ids: list[str]
    consequence: str


@dataclass(frozen=True)
class RandomFourierSampleCertificate:
    n_bits: int
    modulus: int
    bad_register_rate_upper_bound: float
    target_failure_probability: float
    sufficient_sample_count: int
    sample_count_over_n: float
    sample_complexity_class: str
    exhaustive_time_class: str
    exhaustive_memory_class: str
    theorem_statement: str


@dataclass(frozen=True)
class DCPHiddenNumberBridgeReport:
    created_at: str
    observation_model: dict[str, str]
    exact_moment_identities: dict[str, str | float]
    bridge_edges: list[BridgeEdge]
    sample_certificates: list[RandomFourierSampleCertificate]
    headline_metrics: dict[str, int | float]
    proof_obligations: list[dict[str, str]]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def exact_score_expectation(
    n_bits: int,
    hidden_reflection: int,
    candidate_reflection: int,
    good_register_probability: float = 1.0,
) -> float:
    """Return the exact expected quadrature correlation score for one record.

    A good phase register has state (|0> + exp(2 pi i k d/N)|1>)/sqrt(2).
    The measurement basis is uniformly X or Y and its signed outcome is encoded
    as 2z or 2iz.  A bad computational-basis register has zero X/Y expectation.
    """
    if n_bits < 1:
        raise ValueError("n_bits must be positive")
    if not 0.0 <= good_register_probability <= 1.0:
        raise ValueError("good_register_probability must lie in [0, 1]")
    modulus = 1 << n_bits
    difference = (hidden_reflection - candidate_reflection) % modulus
    if difference == 0:
        return good_register_probability
    # Character orthogonality over a uniform public label k in Z_N.
    return 0.0


def sufficient_exhaustive_decoder_samples(
    n_bits: int,
    bad_register_rate_upper_bound: float,
    target_failure_probability: float,
) -> int:
    """Hoeffding/union-bound certificate for exhaustive correlation decoding.

    Each true-minus-false score lies in [-4,4] and has mean at least 1-eta.
    Union bounding over N-1 false frequencies gives
    N exp(-m(1-eta)^2/32) <= delta.
    """
    if n_bits < 1:
        raise ValueError("n_bits must be positive")
    if not 0.0 <= bad_register_rate_upper_bound < 1.0:
        raise ValueError("bad_register_rate_upper_bound must lie in [0, 1)")
    if not 0.0 < target_failure_probability < 1.0:
        raise ValueError("target_failure_probability must lie in (0, 1)")
    gap = 1.0 - bad_register_rate_upper_bound
    log_modulus = n_bits * math.log(2.0)
    return math.ceil(32.0 * (log_modulus + math.log(1.0 / target_failure_probability)) / (gap * gap))


def build_bridge_edges() -> list[BridgeEdge]:
    return [
        BridgeEdge(
            id="EDGE-DCP-TO-RANDOM-COMPLEX-CHARACTER",
            source_model="independent random-label DCP phase states, including hidden computational-basis bad registers",
            target_model="uniform random examples (k,B,z) whose encoded observation has character mean exp(2 pi i k d/N)",
            direction="DCP state samples -> classical random examples",
            status="proved-one-way-measurement-channel",
            mapping="Measure each register in a uniformly random X/Y basis; encode z as 2z for X and 2iz for Y.",
            assumptions=[
                "The public Fourier label k is uniform in Z_N.",
                "Good registers are standard DCP phase qubits.",
                "Bad registers allowed by the f=1 source contract are computational-basis states after label measurement.",
            ],
            proof_or_obstruction=(
                "Conditioned on k, averaging the random basis gives E[y|k,good]=exp(2 pi i k d/N); "
                "a computational-basis bad qubit has E[y|k,bad]=0. Measurement is irreversible, so no reverse "
                "state-preparation reduction is claimed."
            ),
            literature_ids=["regev-lattice-dhsp-2003"],
            consequence="The exact f=1 contamination model attenuates this local score but does not adversarially bias its mean.",
        ),
        BridgeEdge(
            id="EDGE-RANDOM-CHARACTER-TO-EXHAUSTIVE-ML",
            source_model="uniform random complex-character examples with signal attenuation at least 1-eta",
            target_model="complete hidden-reflection recovery",
            direction="random examples -> exhaustive correlation decoder",
            status="proved-polynomial-samples-exponential-time",
            mapping="Score every t in Z_N by Re sum_j y_j exp(-2 pi i k_j t/N) and output the maximum.",
            assumptions=["eta < 1", "independent registers", "all N candidate frequencies are explicitly scored"],
            proof_or_obstruction=(
                "Character orthogonality gives true-versus-false expected gap at least 1-eta. Hoeffding plus a union "
                "bound gives failure at most N exp(-m(1-eta)^2/32). Explicit scoring costs Omega(Nm)."
            ),
            literature_ids=["arxiv:1607.01842"],
            consequence="DCP reflection recovery is information-theoretically sample efficient; the unresolved bottleneck is computation.",
        ),
        BridgeEdge(
            id="EDGE-QUERY-SFT-TO-RANDOM-DCP",
            source_model="query-access significant Fourier transform with correlated chosen inputs",
            target_model="random-label DCP measurement records",
            direction="attempted algorithm transfer",
            status="access-invalid",
            mapping="The attempted transfer substitutes random public labels for adaptively chosen correlated queries.",
            assumptions=["None: the required chosen-query capability is absent."],
            proof_or_obstruction=(
                "The DCP source emits independent random labels and has no chosen-query operation. It cannot request k, k+h, unit vectors, short "
                "intervals, or repeated labels. The SFT literature identifies these algebraic query relations as essential."
            ),
            literature_ids=["arxiv:1607.01842"],
            consequence="Goldreich-Levin, generic SFT, and chosen-multiplier HNP routines cannot be imported as DCP decoders.",
        ),
        BridgeEdge(
            id="EDGE-DCP-TO-CLASSICAL-HNP",
            source_model="random-basis one-bit outcomes with cyclic complex-character mean",
            target_model="classical hidden-number samples revealing deterministic approximate bits or intervals of k d mod N",
            direction="proposed problem reduction",
            status="unproved-structural-analogy",
            mapping="Both models hide a modular product k d, but their observation channels and legal multiplier access differ.",
            assumptions=[
                "A missing channel conversion would preserve inverse-polynomial advantage.",
                "The conversion would use only random multipliers and polynomial resources.",
            ],
            proof_or_obstruction=(
                "A quadrature outcome is a fresh stochastic bit and does not reveal a deterministic interval, MSB, or "
                "LSB of k d. No polynomial reduction in either direction is established."
            ),
            literature_ids=["mvhp-2015-111", "arxiv:1607.01842"],
            consequence="Hidden-number lattice attacks are baselines to test, not evidence that DCP is solved or hard.",
        ),
        BridgeEdge(
            id="EDGE-DCP-TO-LPN-LWE",
            source_model="random examples of a noisy character over Z_(2^n)",
            target_model="LPN/LWE random-example learning",
            direction="hardness analogy",
            status="analogy-only-no-hardness-transfer",
            mapping="All expose a hidden frequency through random noisy samples rather than chosen function queries.",
            assumptions=["A formal average-case reduction would be required for hardness transfer."],
            proof_or_obstruction=(
                "The ambient groups, noise channels, outputs, secret distributions, and verification procedures differ. "
                "The cited random-access SFT limitation does not prove DCP hardness."
            ),
            literature_ids=["arxiv:1607.01842"],
            consequence="Use LPN/LWE algorithms as idea sources while recording every model mismatch and refusing hardness claims.",
        ),
    ]


def run_hidden_number_bridge_report(
    n_values: Sequence[int] = (32, 64, 128, 256, 512, 1024),
    target_failure_probability: float = 1.0 / 3.0,
) -> DCPHiddenNumberBridgeReport:
    certificates: list[RandomFourierSampleCertificate] = []
    for n_bits in n_values:
        if n_bits < 2:
            raise ValueError("all n_values must be at least 2")
        bad_rate = 1.0 / n_bits
        samples = sufficient_exhaustive_decoder_samples(n_bits, bad_rate, target_failure_probability)
        certificates.append(
            RandomFourierSampleCertificate(
                n_bits=n_bits,
                modulus=1 << n_bits,
                bad_register_rate_upper_bound=bad_rate,
                target_failure_probability=target_failure_probability,
                sufficient_sample_count=samples,
                sample_count_over_n=samples / n_bits,
                sample_complexity_class="O((log N + log(1/delta))/(1-eta)^2)",
                exhaustive_time_class="Theta(N m)=2^Theta(n)",
                exhaustive_memory_class="O(m) streaming scores only with N passes; Theta(N) for one-pass score table",
                theorem_statement=(
                    "For independent f=1 DCP registers measured in random X/Y bases, exhaustive correlation returns d "
                    f"with failure at most {target_failure_probability:g} using m={samples} samples."
                ),
            )
        )

    edges = build_bridge_edges()
    exact_or_proved = [edge for edge in edges if edge.status.startswith("proved")]
    invalid = [edge for edge in edges if edge.status == "access-invalid"]
    analogies = [edge for edge in edges if "analogy" in edge.status]
    metrics: dict[str, int | float] = {
        "bridge_edge_count": len(edges),
        "proved_one_way_edge_count": len(exact_or_proved),
        "access_invalid_transfer_count": len(invalid),
        "analogy_only_edge_count": len(analogies),
        "polynomial_sample_certificate_count": len(certificates),
        "maximum_sample_count_over_n": max((row.sample_count_over_n for row in certificates), default=0.0),
        "proved_exact_f1_sample_robustness_count": 1,
        "proved_polynomial_time_decoder_count": 0,
        "proved_hnp_reduction_count": 0,
        "proved_lpn_lwe_reduction_count": 0,
        "complete_lattice_composition_count": 0,
    }
    obligations = [
        {
            "id": "PO-DCP-RANDOM-LABEL-LOCALIZATION",
            "claim": "Localize the hidden frequency in poly(log N) time and memory from random-label quadrature records.",
            "success_criterion": "A uniform decoder avoids enumerating N frequencies and uses no chosen/repeated labels or evaluator.",
            "falsifier": "The method hides an N-sized table, score oracle, preprocessing advice, or subexponential collimation cost.",
        },
        {
            "id": "PO-DCP-HNP-CHANNEL-REDUCTION",
            "claim": "Convert DCP quadrature outcomes to a standard random-multiplier hidden-number observation model.",
            "success_criterion": "A polynomial, advantage-preserving channel reduction with explicit modulus, noise, and success map.",
            "falsifier": "The conversion assumes deterministic bits, chosen multipliers, interval conditioning, or secret verification.",
        },
        {
            "id": "PO-DCP-F1-END-TO-END-DECODER",
            "claim": "Lift sample-level contamination tolerance to an efficient full reflection decoder and Regev lattice composition.",
            "success_criterion": "Polynomial resources and bounded error on every exact f=1 promised instance.",
            "falsifier": "Only the exhaustive decoder is robust, or an efficient decoder amplifies bad registers adversarially.",
        },
    ]
    falsifiers = [
        "Query-access SFT requires chosen correlated inputs that random-label DCP does not supply.",
        "The exact sample theorem uses exhaustive scoring over N frequencies and therefore is not an efficient DCP decoder.",
        "Hidden-number and LPN/LWE connections remain analogies until explicit channel reductions are proved.",
        "Sample-level f=1 robustness does not establish robustness of a future compressed or collective decoder.",
    ]
    return DCPHiddenNumberBridgeReport(
        created_at=utc_now(),
        observation_model={
            "good_state": "|psi_(k,d)>=(|0>+exp(2 pi i k d/N)|1>)/sqrt(2), with uniform public k",
            "measurement": "choose B uniformly from {X,Y}; observe z in {-1,+1}",
            "encoding": "y=2z for X and y=2iz for Y",
            "good_moment": "E[y|k,good]=exp(2 pi i k d/N)",
            "bad_moment": "E[y|k,bad computational-basis state]=0",
            "access_excluded": "chosen labels, repeated labels, coherent evaluator, truth table, verification oracle",
        },
        exact_moment_identities={
            "true_score_expectation_good": 1.0,
            "false_score_expectation_uniform_label": 0.0,
            "true_score_expectation_f1_lower_bound": "1-1/log2(N)",
            "false_score_expectation_f1": 0.0,
            "exhaustive_failure_bound": "N exp(-m(1-eta)^2/32)",
        },
        bridge_edges=edges,
        sample_certificates=certificates,
        headline_metrics=metrics,
        proof_obligations=obligations,
        claim_gate={
            "random_label_access_respected": True,
            "exact_f1_sample_robustness_proved": True,
            "polynomial_sample_recovery_proved": True,
            "polynomial_time_decoder_proved": False,
            "hidden_number_reduction_proved": False,
            "lpn_lwe_hardness_transfer_proved": False,
            "complete_lattice_composition_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The bridge proves a clean polynomial-sample theorem and exact contamination attenuation, but every "
                "known complete decoder still enumerates N frequencies or uses a stronger access model."
            ),
        },
        status="sample-theorem-proved-computational-bridge-open",
        summary=(
            f"Classified {len(edges)} DCP/Fourier/HNP bridge edges and proved {len(certificates)} scaling "
            "certificates for polynomial-sample exhaustive recovery under f=1 contamination; zero polynomial-time "
            "decoders or hardness reductions were established."
        ),
        falsifiers_triggered=falsifiers,
    )


def write_hidden_number_bridge_report(
    path: Path = DCP_HIDDEN_NUMBER_BRIDGE_PATH,
    n_values: Sequence[int] = (32, 64, 128, 256, 512, 1024),
    target_failure_probability: float = 1.0 / 3.0,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    report = run_hidden_number_bridge_report(n_values, target_failure_probability)
    payload = asdict(report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-QUERY-SFT-ACCESS-TRANSFER",
                source=str(path),
                claim="A query-access significant Fourier transform or chosen-multiplier hidden-number algorithm transfers to random-label DCP.",
                reason_invalid=(
                    "Those algorithms construct correlated chosen queries. DCP supplies independent uniform labels and "
                    "does not supply an evaluator, repeats, interval conditioning, or chosen multipliers."
                ),
                lesson="Classify Fourier algorithms by access model before using their runtime or recovery guarantees.",
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence={
                    "access_invalid_transfer_count": payload["headline_metrics"]["access_invalid_transfer_count"],
                    "literature_ids": ["arxiv:1607.01842"],
                },
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-HNP-LPN-LWE-ANALOGY-NOT-REDUCTION",
                source=str(path),
                claim="A structural analogy to hidden-number, LPN, or LWE samples transfers either an algorithm or a hardness result to DCP.",
                reason_invalid="No advantage-preserving channel reduction matches the groups, noise, outputs, access, and verification models.",
                lesson="Use adjacent learning problems to generate decoder hypotheses, but require a formal reduction before transferring claims.",
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence={
                    "proved_hnp_reduction_count": 0,
                    "proved_lpn_lwe_reduction_count": 0,
                },
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-DCP-RANDOM-FOURIER-BRIDGE"
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
                artifacts={"dcp_hidden_number_bridge": str(path)},
            )
        )
    return payload
