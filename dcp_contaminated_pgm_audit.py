"""Audit information robustness of the clean covariant PGM under exact f=1 DCP contamination."""

from __future__ import annotations

import json
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

import numpy as np

from dcp_covariant_pgm_audit import covariant_pgm_success
from dcp_hashed_fiber_measurement_audit import subset_sum_counts
from dcp_reference_projection_audit import subset_sums
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


DCP_CONTAMINATED_PGM_PATH = Path("research/phase_workbench/dcp_contaminated_pgm_audit.json")
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-CONTAMINATED-PGM-AUDIT"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class ContaminatedPGMInstance:
    n_bits: int
    register_count: int
    bad_probability: float
    bad_pattern: str
    clean_pgm_success_probability: float
    all_good_probability: float
    adversarial_product_lower_bound: float
    exact_contaminated_clean_pgm_success: float
    lower_bound_slack: float
    lower_bound_violation: bool
    inverse_polynomial_robust_information_success: bool
    polynomial_measurement_circuit_constructed: bool


@dataclass(frozen=True)
class ContaminationAssumptionRecord:
    assumption_id: str
    status: str
    consequence: str
    failure_mode: str


@dataclass(frozen=True)
class DCPContaminatedPGMReport:
    created_at: str
    theorem_contract_id: str
    robustness_theorem: dict[str, str]
    finite_instances: list[ContaminatedPGMInstance]
    assumptions: list[ContaminationAssumptionRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def clean_pgm_reference(n_bits: int, labels: Sequence[int]) -> np.ndarray:
    sums = subset_sums(n_bits, labels)
    counts = np.bincount(sums, minlength=1 << n_bits)
    return np.asarray([1.0 / math.sqrt((1 << n_bits) * counts[value]) for value in sums], dtype=np.complex128)


def _apply_product_operator(vector: np.ndarray, local_operators: Sequence[np.ndarray]) -> np.ndarray:
    register_count = len(local_operators)
    if vector.shape != (1 << register_count,):
        raise ValueError("vector dimension must match local operators")
    tensor = vector.reshape((2,) * register_count)
    for label_index, operator in enumerate(local_operators):
        if operator.shape != (2, 2):
            raise ValueError("local operators must be 2x2")
        axis = register_count - 1 - label_index
        tensor = np.moveaxis(tensor, axis, 0)
        tensor = np.tensordot(operator, tensor, axes=(1, 0))
        tensor = np.moveaxis(tensor, 0, axis)
    return tensor.reshape(-1)


def contaminated_clean_pgm_success(
    n_bits: int,
    labels: Sequence[int],
    bad_probability: float,
    bad_bits: Sequence[int],
) -> float:
    if not 0.0 <= bad_probability <= 1.0:
        raise ValueError("bad_probability must lie in [0,1]")
    if len(bad_bits) != len(labels) or any(bit not in {0, 1} for bit in bad_bits):
        raise ValueError("bad_bits must contain one computational-basis bit per label")
    reference = clean_pgm_reference(n_bits, labels)
    good_weight = 1.0 - bad_probability
    operators = []
    for bit in bad_bits:
        operator = np.array(
            [
                [good_weight / 2.0 + bad_probability * (bit == 0), good_weight / 2.0],
                [good_weight / 2.0, good_weight / 2.0 + bad_probability * (bit == 1)],
            ],
            dtype=np.complex128,
        )
        operators.append(operator)
    applied = _apply_product_operator(reference, operators)
    success = float(np.real(np.vdot(reference, applied)))
    return min(1.0, max(0.0, success))


def _bad_bits(pattern: str, count: int, seed: int) -> list[int]:
    if pattern == "all-zero":
        return [0] * count
    if pattern == "all-one":
        return [1] * count
    if pattern == "alternating":
        return [index % 2 for index in range(count)]
    if pattern == "seeded-random":
        rng = random.Random(seed)
        return [rng.randrange(2) for _ in range(count)]
    raise ValueError(f"unknown bad pattern: {pattern}")


def analyze_contaminated_pgm_instance(
    n_bits: int,
    labels: Sequence[int],
    bad_pattern: str,
    bad_probability: float | None = None,
    seed: int = 0,
) -> ContaminatedPGMInstance:
    resolved_bad_probability = 1.0 / n_bits if bad_probability is None else bad_probability
    counts = subset_sum_counts(n_bits, labels)
    clean_success = covariant_pgm_success(counts)
    all_good = (1.0 - resolved_bad_probability) ** len(labels)
    lower_bound = all_good * clean_success
    exact = contaminated_clean_pgm_success(
        n_bits,
        labels,
        resolved_bad_probability,
        _bad_bits(bad_pattern, len(labels), seed),
    )
    return ContaminatedPGMInstance(
        n_bits=n_bits,
        register_count=len(labels),
        bad_probability=resolved_bad_probability,
        bad_pattern=bad_pattern,
        clean_pgm_success_probability=clean_success,
        all_good_probability=all_good,
        adversarial_product_lower_bound=lower_bound,
        exact_contaminated_clean_pgm_success=exact,
        lower_bound_slack=exact - lower_bound,
        lower_bound_violation=exact + 1e-12 < lower_bound,
        inverse_polynomial_robust_information_success=lower_bound >= 1.0 / max(2, n_bits**4),
        polynomial_measurement_circuit_constructed=False,
    )


def _assumptions() -> list[ContaminationAssumptionRecord]:
    return [
        ContaminationAssumptionRecord(
            assumption_id="tensor-product-register-source",
            status="required-and-primary-source-matched",
            consequence="The all-good branch has weight product_i(1-epsilon_i).",
            failure_mode="Marginal per-register guarantees without product structure would not imply an all-good lower bound.",
        ),
        ContaminationAssumptionRecord(
            assumption_id="arbitrary-unflagged-basis-bad-states",
            status="covered",
            consequence="Bad-branch success terms are nonnegative, so their basis values cannot reduce the all-good contribution.",
            failure_mode="The theorem gives a success lower bound only; it does not identify bad registers or simplify the circuit.",
        ),
        ContaminationAssumptionRecord(
            assumption_id="clean-pgm-used-without-bad-pattern-knowledge",
            status="covered",
            consequence="The fixed clean covariant POVM is independent of bad bits and bad-event flags.",
            failure_mode="No efficient implementation of that POVM is supplied.",
        ),
        ContaminationAssumptionRecord(
            assumption_id="m-linear-in-logN",
            status="required-for-constant-all-good-weight",
            consequence="For epsilon<=1/n and m<=cn, all-good weight approaches at least exp(-c).",
            failure_mode="Superlinear dependency blocks can make the all-good branch superpolynomially small.",
        ),
    ]


def run_contaminated_pgm_audit(
    n_values: Sequence[int] = (6, 8, 10, 12, 14, 16),
    register_offsets: Sequence[int] = (-2, 0, 2),
    bad_patterns: Sequence[str] = ("all-zero", "all-one", "alternating", "seeded-random"),
    trials_per_row: int = 2,
    seed: int = 0,
) -> DCPContaminatedPGMReport:
    if trials_per_row < 1:
        raise ValueError("trials_per_row must be positive")
    instances: list[ContaminatedPGMInstance] = []
    for n_index, n_bits in enumerate(n_values):
        modulus = 1 << n_bits
        for offset_index, offset in enumerate(register_offsets):
            register_count = n_bits + offset
            if register_count < 1:
                continue
            for trial in range(trials_per_row):
                rng = random.Random(seed + 1_000_003 * n_index + 10_007 * offset_index + trial)
                labels = [rng.randrange(modulus) for _ in range(register_count)]
                for pattern_index, pattern in enumerate(bad_patterns):
                    instances.append(
                        analyze_contaminated_pgm_instance(
                            n_bits,
                            labels,
                            pattern,
                            seed=seed + 101 * pattern_index + trial,
                        )
                    )
    n_register_rows = [item for item in instances if item.register_count == item.n_bits]
    metrics: dict[str, int | float] = {
        "finite_instance_count": len(instances),
        "lower_bound_violation_count": sum(item.lower_bound_violation for item in instances),
        "inverse_polynomial_robust_information_instance_count": sum(
            item.inverse_polynomial_robust_information_success for item in instances
        ),
        "minimum_n_register_all_good_probability": min((item.all_good_probability for item in n_register_rows), default=0.0),
        "minimum_n_register_adversarial_lower_bound": min(
            (item.adversarial_product_lower_bound for item in n_register_rows), default=0.0
        ),
        "minimum_observed_contaminated_success": min(
            (item.exact_contaminated_clean_pgm_success for item in instances), default=0.0
        ),
        "proved_exact_f1_information_robustness_count": 1,
        "proved_exact_f1_robust_pgm_circuit_count": 0,
        "proved_polynomial_pgm_circuit_count": 0,
        "proved_lattice_composition_count": 0,
    }
    return DCPContaminatedPGMReport(
        created_at=utc_now(),
        theorem_contract_id="THM-REGEV-USVP-TO-DCP-2003",
        robustness_theorem={
            "source": "tensor-product DCP registers; register i is good with probability 1-epsilon_i and otherwise an arbitrary basis state",
            "fixed_measurement": "apply the clean covariant PGM, without flags or bad-pattern knowledge",
            "lower_bound": "P_success(contaminated)>=product_i(1-epsilon_i) P_success(clean)",
            "reason": "expand the product mixture by bad-coordinate subsets; the all-good POVM contribution has the stated weight and every other contribution is nonnegative",
            "f1_scaling": "epsilon_i<=1/n and m<=cn imply product_i(1-epsilon_i)>= (1-1/n)^(cn)=Theta(1)",
            "scope": "information robustness of the fixed clean POVM; no efficient measurement implementation or lattice composition",
        },
        finite_instances=instances,
        assumptions=_assumptions(),
        headline_metrics=metrics,
        claim_gate={
            "exact_f1_information_robustness_proved": True,
            "bad_register_flags_used": False,
            "bad_basis_values_known_to_measurement": False,
            "polynomial_pgm_circuit_constructed": False,
            "lattice_composition_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The exact product contamination promise preserves a constant fraction of clean PGM success for m=Theta(n), "
                "but the full-rank normalized-fiber measurement still lacks a polynomial circuit."
            ),
        },
        status="exact-f1-information-robustness-proved-pgm-implementation-open",
        summary=(
            f"Verified {len(instances)} contaminated clean-PGM instances with {metrics['lower_bound_violation_count']} "
            f"all-good lower-bound violations. Exact f=1 information robustness is proved; polynomial robust PGM circuits=0."
        ),
        falsifiers_triggered=[
            "For a global m=Theta(n) measurement, exact f=1 contamination does not destroy information-theoretic PGM success; the all-good branch retains constant weight.",
            "The lower bound uses no bad-register flags and is uniform over arbitrary computational-basis bad values.",
            "This does not rescue deep merge trees whose output validity requires exponentially many good leaves.",
            "The tensor-product source contract is essential; marginal-only contamination promises would not suffice.",
            "Information robustness still does not provide a polynomial implementation of the full-rank PGM.",
        ],
    )


def write_contaminated_pgm_audit(
    path: Path = DCP_CONTAMINATED_PGM_PATH,
    n_values: Sequence[int] = (6, 8, 10, 12, 14, 16),
    register_offsets: Sequence[int] = (-2, 0, 2),
    bad_patterns: Sequence[str] = ("all-zero", "all-one", "alternating", "seeded-random"),
    trials_per_row: int = 2,
    seed: int = 0,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    report = run_contaminated_pgm_audit(n_values, register_offsets, bad_patterns, trials_per_row, seed)
    payload = asdict(report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-F1-CONTAMINATION-AS-CLEAN-PGM-INFORMATION-BARRIER",
                source=str(path),
                claim="The exact f=1 bad-register rate by itself destroys global clean-PGM information at m=Theta(log N).",
                reason_invalid=(
                    "Under the primary-source tensor-product contract, the all-good component has constant weight for "
                    "m=Theta(log N), and every other POVM success contribution is nonnegative."
                ),
                lesson=(
                    "Do not cite f=1 contamination as the information barrier for global linear-size measurements. The "
                    "remaining obstruction is efficient normalized-fiber implementation and end-to-end composition."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence={
                    "lower_bound_violation_count": payload["headline_metrics"]["lower_bound_violation_count"],
                    "proved_exact_f1_information_robustness_count": 1,
                    "proved_exact_f1_robust_pgm_circuit_count": 0,
                },
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-DCP-CONTAMINATED-PGM"
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
                artifacts={"dcp_contaminated_pgm_audit": str(path)},
            )
        )
    return payload
