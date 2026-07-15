"""Exact marker-coset equivalence for modular subset-sum embeddings.

The marker coordinate maps either embedding lattice onto the integers.  Its
kernel contains all target-independent relation vectors; desired witnesses lie
in the affine marker ``-1`` coset.  If every constraint-coordinate quantum is
larger than ``sqrt(m+1)``, a marker-minus-one vector of norm at most
``sqrt(m+1)`` must have zero constraint coordinates and all binary coordinates
equal to ``+/-1``.  It therefore decodes to a binary subset-sum witness, and
every witness gives such a vector.

Thus marker-aware bounded-distance search is an exact reformulation, not a
decoder.  Marker coordinates of any lattice basis have gcd one, so extended
gcd constructs some marker-one vector in polynomial time, but supplies no norm
bound.  The remaining short affine-coset problem is precisely the hard step.
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


DCP_SUBSET_SUM_MARKER_COSET_PATH = Path(
    "research/reductions/dcp_subset_sum_marker_coset_theorem.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-SUBSET-SUM-MARKER-COSET-THEOREM"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"


@dataclass(frozen=True)
class MarkerCosetTheoremCertificate:
    embedding: str
    affine_coset_formula: str
    sufficient_scale_condition: str
    witness_radius_squared_formula: str
    marker_projection_surjective: bool
    basis_marker_gcd_one_proved: bool
    radius_search_equivalent_to_binary_subset_sum: bool
    polynomial_marker_one_vector_without_norm_bound: bool
    polynomial_short_marker_one_decoder_proved: bool
    proof: str
    limitations: list[str]


@dataclass(frozen=True)
class MarkerCosetScalingRow:
    n_bits: int
    register_offset: int
    register_count: int
    embedding_scale: int
    low_constraint_scale: int
    witness_radius_squared: int
    minimum_standard_constraint_quantum_squared: int
    minimum_sliced_constraint_quantum_squared: int
    standard_scale_condition_satisfied: bool
    carry_sliced_scale_condition_satisfied: bool
    standard_radius_equivalence_proved: bool
    carry_sliced_radius_equivalence_proved: bool
    finite_row_is_asymptotic_theorem: bool


@dataclass(frozen=True)
class DCPSubsetSumMarkerCosetReport:
    created_at: str
    reduction_contract: dict[str, str]
    theorem_certificates: list[MarkerCosetTheoremCertificate]
    rows: list[MarkerCosetScalingRow]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def standard_marker_coset_vector(
    coefficients: Sequence[int],
    labels: Sequence[int],
    target: int,
    modulus: int,
    embedding_scale: int,
    modulus_multiple: int = 0,
) -> list[int]:
    if len(coefficients) != len(labels):
        raise ValueError("coefficient and label lengths differ")
    if modulus <= 0 or embedding_scale <= 0:
        raise ValueError("modulus and scale must be positive")
    return [
        *(2 * int(value) - 1 for value in coefficients),
        2
        * embedding_scale
        * (
            sum(int(value) * int(label) for value, label in zip(coefficients, labels))
            + modulus_multiple * modulus
            - int(target)
        ),
        -1,
    ]


def carry_sliced_marker_coset_vector(
    coefficients: Sequence[int],
    low_labels: Sequence[int],
    high_labels: Sequence[int],
    target_low_sum: int,
    target_high_residue: int,
    high_modulus: int,
    embedding_scale: int,
    low_constraint_scale: int,
    high_modulus_multiple: int = 0,
) -> list[int]:
    if len(coefficients) != len(low_labels) or len(coefficients) != len(high_labels):
        raise ValueError("coefficient and label lengths differ")
    if min(high_modulus, embedding_scale, low_constraint_scale) <= 0:
        raise ValueError("modulus and scales must be positive")
    return [
        *(2 * int(value) - 1 for value in coefficients),
        2
        * embedding_scale
        * (
            sum(int(value) * int(label) for value, label in zip(coefficients, high_labels))
            + high_modulus_multiple * high_modulus
            - int(target_high_residue)
        ),
        2
        * low_constraint_scale
        * (
            sum(int(value) * int(label) for value, label in zip(coefficients, low_labels))
            - int(target_low_sum)
        ),
        -1,
    ]


def decode_short_standard_marker_vector(
    vector: Sequence[int],
    labels: Sequence[int],
    target: int,
    modulus: int,
) -> list[int] | None:
    if len(vector) != len(labels) + 2 or int(vector[-1]) != -1 or int(vector[-2]) != 0:
        return None
    if any(int(value) not in {-1, 1} for value in vector[:-2]):
        return None
    witness = [(int(value) + 1) // 2 for value in vector[:-2]]
    return (
        witness
        if sum(label * bit for label, bit in zip(labels, witness)) % modulus == target % modulus
        else None
    )


def run_marker_coset_theorem(
    n_values: Sequence[int] = (16, 32, 64, 128, 256),
    register_offset: int = 2,
    embedding_scale: int | None = None,
    low_constraint_scale: int | None = None,
) -> DCPSubsetSumMarkerCosetReport:
    rows: list[MarkerCosetScalingRow] = []
    for n_bits in n_values:
        if n_bits < 4:
            raise ValueError("n values must be at least four")
        register_count = n_bits + register_offset
        radius_squared = register_count + 1
        default_scale = math.floor(math.sqrt(radius_squared) / 2) + 1
        standard_scale = embedding_scale or default_scale
        sliced_scale = low_constraint_scale or default_scale
        standard_ok = (2 * standard_scale) ** 2 > radius_squared
        sliced_ok = min((2 * standard_scale) ** 2, (2 * sliced_scale) ** 2) > radius_squared
        rows.append(
            MarkerCosetScalingRow(
                n_bits=n_bits,
                register_offset=register_offset,
                register_count=register_count,
                embedding_scale=standard_scale,
                low_constraint_scale=sliced_scale,
                witness_radius_squared=radius_squared,
                minimum_standard_constraint_quantum_squared=(2 * standard_scale) ** 2,
                minimum_sliced_constraint_quantum_squared=min(
                    (2 * standard_scale) ** 2, (2 * sliced_scale) ** 2
                ),
                standard_scale_condition_satisfied=standard_ok,
                carry_sliced_scale_condition_satisfied=sliced_ok,
                standard_radius_equivalence_proved=standard_ok,
                carry_sliced_radius_equivalence_proved=sliced_ok,
                finite_row_is_asymptotic_theorem=False,
            )
        )

    common_proof = (
        "A marker-minus-one vector has odd binary coordinates, each of squared magnitude at least one, and marker "
        "square one. If a nonzero constraint coordinate has quantum larger than sqrt(m+1), it cannot occur inside "
        "the witness radius. The remaining m+1 coordinates already attain the radius lower bound, forcing every odd "
        "coordinate to be +/-1 and hence every row coefficient to be binary. Conversely every binary witness gives "
        "the radius vector. Marker projection is onto Z, so every basis has marker gcd one; Bezout controls the marker "
        "but not the norm."
    )
    certificates = [
        MarkerCosetTheoremCertificate(
            embedding="standard centered modular embedding",
            affine_coset_formula="(2z-1, 2s(<a,z>-t+k*2^n), -1)",
            sufficient_scale_condition="(2s)^2 > m+1",
            witness_radius_squared_formula="m+1",
            marker_projection_surjective=True,
            basis_marker_gcd_one_proved=True,
            radius_search_equivalent_to_binary_subset_sum=True,
            polynomial_marker_one_vector_without_norm_bound=True,
            polynomial_short_marker_one_decoder_proved=False,
            proof=common_proof,
            limitations=[
                "The theorem is an equivalence, not an efficient affine-CVP algorithm.",
                "It does not imply uniqueness when the target has multiple binary witnesses.",
                "Bezout marker normalization can create exponentially long vectors.",
            ],
        ),
        MarkerCosetTheoremCertificate(
            embedding="exact low/high carry-sliced embedding for a fixed carry",
            affine_coset_formula=(
                "(2z-1, 2s(<a_hi,z>-t_hi+kQ), 2u(<a_lo,z>-L), -1)"
            ),
            sufficient_scale_condition="min((2s)^2,(2u)^2) > m+1",
            witness_radius_squared_formula="m+1",
            marker_projection_surjective=True,
            basis_marker_gcd_one_proved=True,
            radius_search_equivalent_to_binary_subset_sum=True,
            polynomial_marker_one_vector_without_norm_bound=True,
            polynomial_short_marker_one_decoder_proved=False,
            proof=common_proof,
            limitations=[
                "Equivalence holds for each fixed enumerated carry and does not choose the winning carry.",
                "The theorem is an affine-CVP reformulation, not an efficient decoder.",
                "Marker-zero relation counts do not decide marker-coset nearest-vector complexity.",
            ],
        ),
    ]
    metrics: dict[str, int | float] = {
        "row_count": len(rows),
        "exact_marker_kernel_affine_coset_decomposition_count": 2,
        "basis_marker_gcd_one_theorem_count": 2,
        "exact_witness_radius_equivalence_theorem_count": 2,
        "polynomial_unbounded_marker_one_vector_theorem_count": 2,
        "standard_scale_condition_row_count": sum(row.standard_scale_condition_satisfied for row in rows),
        "carry_sliced_scale_condition_row_count": sum(
            row.carry_sliced_scale_condition_satisfied for row in rows
        ),
        "polynomial_short_marker_one_decoder_count": 0,
        "proved_affine_cvp_easier_than_subset_sum_count": 0,
    }
    return DCPSubsetSumMarkerCosetReport(
        created_at=utc_now(),
        reduction_contract={
            "input": "public density-one modular subset-sum instance",
            "output": "short vector in marker-minus-one affine lattice coset",
            "equivalence": "radius sqrt(m+1) search is exactly binary witness search under explicit scale conditions",
            "resource_warning": "marker gcd normalization is polynomial but has no useful norm guarantee",
        },
        theorem_certificates=certificates,
        rows=rows,
        headline_metrics=metrics,
        claim_gate={
            "marker_filter_is_algorithm": False,
            "short_marker_coset_search_equivalent_to_subset_sum": True,
            "marker_zero_competitors_alone_rule_out_affine_decoder": False,
            "polynomial_short_marker_decoder_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The marker separates the relation kernel from the witness coset but does not solve nearest-vector "
                "search in that coset. A speedup requires an actual affine-CVP algorithm with source coverage."
            ),
        },
        status="marker-filter-reduced-to-original-subset-sum-search",
        summary=(
            "Proved exact standard and carry-sliced marker-coset radius equivalences. Marker normalization is easy; "
            "short marker-one extraction remains exactly the binary subset-sum search problem."
        ),
        falsifiers_triggered=[
            "Filtering reduced rows by marker coordinate is not a decoder theorem.",
            "Marker-zero competitors do not by themselves prove affine-CVP failure.",
            "Extended-gcd marker normalization has no shortness guarantee.",
            "Any claimed rescue must provide source coverage and complexity for short affine-coset search.",
        ],
    )


def write_marker_coset_theorem(
    path: Path = DCP_SUBSET_SUM_MARKER_COSET_PATH,
    n_values: Sequence[int] = (16, 32, 64, 128, 256),
    register_offset: int = 2,
    embedding_scale: int | None = None,
    low_constraint_scale: int | None = None,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(
        run_marker_coset_theorem(
            n_values=n_values,
            register_offset=register_offset,
            embedding_scale=embedding_scale,
            low_constraint_scale=low_constraint_scale,
        )
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-DCP-SUBSET-SUM-MARKER-FILTER-AS-DECODER",
                source=str(path),
                claim="Selecting marker-one lattice vectors supplies a polynomial subset-sum witness decoder.",
                reason_invalid=(
                    "Marker-one normalization is easy without a norm bound, while finding one at witness radius is "
                    "exactly equivalent to the original binary subset-sum search."
                ),
                lesson=(
                    "Specify and analyze an affine-CVP algorithm; marker filtering or Bezout normalization alone is "
                    "not algorithmic progress."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=payload["headline_metrics"],
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-MARKER-COSET-THEOREM"
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
                artifacts={"dcp_subset_sum_marker_coset_theorem": str(path)},
            )
        )
    return payload
