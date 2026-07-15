"""Exact volume geometry for standard and low-bit carry-sliced embeddings.

At density one, the standard modular subset-sum embedding has covolume

  2^m * (2 s 2^n),

where m=n+c and s is the embedding scale.  Its determinant root tends to 4 for
subexponential s.  The planted binary witness has norm sqrt(m+1), so its ratio
to the Gaussian volume scale tends to sqrt(2*pi*e)/4, slightly above one.

For a carry-sliced embedding with low labels l_i, exact low sum L, high modulus
Q=2^(n-b), and low scale t, Cauchy-Binet gives

  covolume^2 = [2^m (2 s Q)]^2
      * [1 + t^2 (sum_i l_i^2 + (2L-sum_i l_i)^2)].

When b=O(log n) and scales are polynomial, the bracket contributes only
o(n) to log covolume.  The determinant root and planted/volume ratio therefore
have the same limits.  This rules out an asymptotic separation argument based
only on lattice volume.  It does not rule out local Gram-Schmidt structure,
atypical short-vector counts, or a non-volume LLL/BKZ decoder theorem.
"""

from __future__ import annotations

import json
import math
import random
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


DCP_SUBSET_SUM_EMBEDDING_VOLUME_PATH = Path(
    "research/classical_baselines/dcp_subset_sum_embedding_volume_theorem.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-SUBSET-SUM-EMBEDDING-VOLUME-THEOREM"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class EmbeddingVolumeTheoremCertificate:
    standard_covolume_formula: str
    carry_sliced_covolume_squared_formula: str
    standard_determinant_root_limit: float
    carry_sliced_determinant_root_limit: float
    planted_witness_to_gaussian_scale_limit: float
    standard_volume_only_separation_ruled_out: bool
    logarithmic_slice_volume_only_separation_ruled_out: bool
    cauchy_binet_proved: bool
    proof: str
    limitations: list[str]


@dataclass(frozen=True)
class EmbeddingVolumeScalingRow:
    n_bits: int
    register_offset: int
    register_count: int
    constrained_low_bits: int
    embedding_scale: int
    low_constraint_scale: int
    standard_log2_covolume: float
    carry_sliced_log2_covolume: float
    standard_determinant_root: float
    carry_sliced_determinant_root: float
    planted_witness_norm: float
    standard_witness_to_gaussian_scale_ratio: float
    carry_sliced_witness_to_gaussian_scale_ratio: float
    carry_slice_log2_root_change: float
    finite_row_is_asymptotic_theorem: bool


@dataclass(frozen=True)
class DCPSubsetSumEmbeddingVolumeReport:
    created_at: str
    theorem_contract: dict[str, str]
    theorem_certificate: EmbeddingVolumeTheoremCertificate
    rows: list[EmbeddingVolumeScalingRow]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def standard_embedding_covolume(
    n_bits: int,
    register_count: int,
    embedding_scale: int,
) -> int:
    if min(n_bits, register_count, embedding_scale) < 1:
        raise ValueError("embedding parameters must be positive")
    return (1 << register_count) * 2 * embedding_scale * (1 << n_bits)


def carry_sliced_covolume_squared(
    n_bits: int,
    low_bits: int,
    low_labels: Sequence[int],
    target_low_sum: int,
    embedding_scale: int,
    low_constraint_scale: int,
) -> int:
    if not 0 < low_bits < n_bits:
        raise ValueError("low_bits must lie strictly between zero and n_bits")
    if min(embedding_scale, low_constraint_scale) < 1:
        raise ValueError("embedding scales must be positive")
    low_modulus = 1 << low_bits
    if any(label < 0 or label >= low_modulus for label in low_labels):
        raise ValueError("low label outside the low modulus")
    register_count = len(low_labels)
    high_modulus = 1 << (n_bits - low_bits)
    base = (1 << register_count) * 2 * embedding_scale * high_modulus
    correction = 1 + low_constraint_scale**2 * (
        sum(int(label) ** 2 for label in low_labels)
        + (2 * int(target_low_sum) - sum(int(label) for label in low_labels)) ** 2
    )
    return base * base * correction


def gaussian_volume_scale(dimension: int, log2_covolume: float) -> float:
    return math.sqrt(dimension / (2 * math.pi * math.e)) * 2 ** (
        log2_covolume / dimension
    )


def run_embedding_volume_theorem(
    n_values: Sequence[int] = (16, 32, 64, 128, 256),
    register_offset: int = 2,
    log_multiplier: int = 1,
    embedding_scale: int = 4,
    low_constraint_scale: int = 4,
    seed: int = 0,
) -> DCPSubsetSumEmbeddingVolumeReport:
    rows = []
    for index, n_bits in enumerate(n_values):
        if n_bits < 4:
            raise ValueError("n values must be at least four")
        register_count = n_bits + register_offset
        low_bits = min(
            n_bits - 1,
            max(1, math.ceil(log_multiplier * math.log2(n_bits))),
        )
        low_modulus = 1 << low_bits
        rng = random.Random(seed + 1_000_003 * index)
        low_labels = [rng.randrange(low_modulus) for _ in range(register_count)]
        planted = [rng.randrange(2) for _ in range(register_count)]
        target_low_sum = sum(
            label * bit for label, bit in zip(low_labels, planted)
        )
        standard_volume = standard_embedding_covolume(
            n_bits, register_count, embedding_scale
        )
        carry_volume_squared = carry_sliced_covolume_squared(
            n_bits,
            low_bits,
            low_labels,
            target_low_sum,
            embedding_scale,
            low_constraint_scale,
        )
        standard_log = math.log2(standard_volume)
        carry_log = 0.5 * math.log2(carry_volume_squared)
        dimension = register_count + 2
        standard_root = 2 ** (standard_log / dimension)
        carry_root = 2 ** (carry_log / dimension)
        witness_norm = math.sqrt(register_count + 1)
        rows.append(
            EmbeddingVolumeScalingRow(
                n_bits=n_bits,
                register_offset=register_offset,
                register_count=register_count,
                constrained_low_bits=low_bits,
                embedding_scale=embedding_scale,
                low_constraint_scale=low_constraint_scale,
                standard_log2_covolume=standard_log,
                carry_sliced_log2_covolume=carry_log,
                standard_determinant_root=standard_root,
                carry_sliced_determinant_root=carry_root,
                planted_witness_norm=witness_norm,
                standard_witness_to_gaussian_scale_ratio=(
                    witness_norm / gaussian_volume_scale(dimension, standard_log)
                ),
                carry_sliced_witness_to_gaussian_scale_ratio=(
                    witness_norm / gaussian_volume_scale(dimension, carry_log)
                ),
                carry_slice_log2_root_change=(carry_log - standard_log) / dimension,
                finite_row_is_asymptotic_theorem=False,
            )
        )
    limiting_ratio = math.sqrt(2 * math.pi * math.e) / 4
    certificate = EmbeddingVolumeTheoremCertificate(
        standard_covolume_formula="2^m * (2*s*2^n)",
        carry_sliced_covolume_squared_formula=(
            "[2^m*(2*s*2^(n-b))]^2 * [1+t^2*(sum l_i^2+(2L-sum l_i)^2)]"
        ),
        standard_determinant_root_limit=4.0,
        carry_sliced_determinant_root_limit=4.0,
        planted_witness_to_gaussian_scale_limit=limiting_ratio,
        standard_volume_only_separation_ruled_out=True,
        logarithmic_slice_volume_only_separation_ruled_out=True,
        cauchy_binet_proved=True,
        proof=(
            "Expand the square standard determinant along the marker and modulus rows. For the rectangular sliced "
            "basis, Cauchy-Binet leaves the low-column-deleted minor, one minor for each deleted binary coordinate, "
            "and the marker-deleted minor; their squared ratios are 1, t^2 l_i^2, and "
            "t^2(2L-sum l_i)^2. With m=n+c, b=O(log n), and polynomial scales, both log covolumes equal "
            "2n+o(n), so both determinant roots tend to four."
        ),
        limitations=[
            "The Gaussian scale is a volume benchmark, not a theorem about the actual shortest vector.",
            "The result rules out volume-only asymptotic separation, not local Gram-Schmidt structure.",
            "BKZ/LLL behavior can depend on correlations not represented by covolume.",
            "No average-case short-vector count or decoding lower bound is proved.",
        ],
    )
    tail = rows[-1]
    metrics: dict[str, int | float] = {
        "row_count": len(rows),
        "exact_standard_covolume_theorem_count": 1,
        "exact_carry_sliced_covolume_theorem_count": 1,
        "volume_only_asymptotic_separation_ruled_out_count": 2,
        "limiting_witness_to_gaussian_scale_ratio": limiting_ratio,
        "tail_standard_witness_to_gaussian_scale_ratio": tail.standard_witness_to_gaussian_scale_ratio,
        "tail_carry_sliced_witness_to_gaussian_scale_ratio": tail.carry_sliced_witness_to_gaussian_scale_ratio,
        "tail_carry_slice_log2_root_change": tail.carry_slice_log2_root_change,
        "proved_local_reduced_basis_separation_count": 0,
        "proved_average_case_short_vector_gap_count": 0,
        "polynomial_witness_decoder_count": 0,
    }
    return DCPSubsetSumEmbeddingVolumeReport(
        created_at=utc_now(),
        theorem_contract={
            "embeddings": "standard centered modular embedding and exact carry-sliced low/high embedding",
            "regime": "m=n+c, b=O(log n), polynomial embedding scales",
            "proved": "exact covolumes and determinant-root limits",
            "not_proved": "actual shortest-vector law, local reduced-basis behavior, or decoder complexity",
        },
        theorem_certificate=certificate,
        rows=rows,
        headline_metrics=metrics,
        claim_gate={
            "standard_volume_only_gap_exists": False,
            "logarithmic_slice_volume_only_gap_exists": False,
            "local_reduced_basis_gap_proved": False,
            "average_case_short_vector_gap_proved": False,
            "polynomial_witness_decoder_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The planted witness remains on the Gaussian volume scale in both embeddings. Any surviving lattice "
                "route must prove a non-volume local basis event, short-vector count separation, and decoder coverage."
            ),
        },
        status="standard-and-log-sliced-volume-only-lattice-gap-obstructed",
        summary=(
            f"Proved exact covolumes for standard and carry-sliced embeddings. Both determinant roots tend to 4 and "
            f"the planted/Gaussian scale ratio tends to {limiting_ratio:.6g}; no volume-only asymptotic gap exists."
        ),
        falsifiers_triggered=[
            "The standard density-one planted witness is not asymptotically below the volume scale.",
            "O(log n) carry slicing changes covolume only subexponentially and cannot create a volume-root gap.",
            "Finite LLL success cannot be explained as an asymptotic determinant separation.",
            "The theorem leaves local reduced-basis and average short-vector count mechanisms open.",
        ],
    )


def write_embedding_volume_theorem(
    path: Path = DCP_SUBSET_SUM_EMBEDDING_VOLUME_PATH,
    n_values: Sequence[int] = (16, 32, 64, 128, 256),
    register_offset: int = 2,
    log_multiplier: int = 1,
    embedding_scale: int = 4,
    low_constraint_scale: int = 4,
    seed: int = 0,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    report = run_embedding_volume_theorem(
        n_values=n_values,
        register_offset=register_offset,
        log_multiplier=log_multiplier,
        embedding_scale=embedding_scale,
        low_constraint_scale=low_constraint_scale,
        seed=seed,
    )
    payload = asdict(report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-SUBSET-SUM-VOLUME-ONLY-LATTICE-GAP",
                source=str(path),
                claim=(
                    "The standard or O(log n) carry-sliced density-one embedding creates an asymptotic planted "
                    "short-vector separation visible from covolume alone."
                ),
                reason_invalid=(
                    "Both exact determinant roots tend to four, placing the planted witness at limiting ratio "
                    "sqrt(2*pi*e)/4 to the Gaussian volume scale."
                ),
                lesson=(
                    "Require an explicit local Gram-Schmidt event, average short-vector count theorem, and decoder "
                    "coverage. Do not cite determinant or finite LLL recovery as the missing gap."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=payload["headline_metrics"],
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-EMBEDDING-VOLUME-THEOREM"
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
                artifacts={"dcp_subset_sum_embedding_volume_theorem": str(path)},
            )
        )
    return payload
