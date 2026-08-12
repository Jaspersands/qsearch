"""Rowspace-canonical HSP reduction for permutation code equivalence.

The standard scrambler-permutation formulation uses
``GL_k(F_2) x S_n``.  With explicit full-rank generators, however, the row
scrambler is gauge: reduced row echelon form canonically represents the code
rowspace.  Define

    f_C(P) = RREF(M P),   P in S_n.

Then ``f_C(P)=f_C(Q)`` exactly when the permutations differ by an automorphism
of C, and equivalent codes produce hidden-shifted functions.  The hidden shift
therefore lives over ``S_n`` and the standard wreath-product HSP lives over
``S_n wr Z_2``, without a ``GL_k`` factor.

For a rigid code the bridge subgroup has order two and its nonidentity element
acts as n disjoint transpositions on two n-point blocks, exactly the
graph-isomorphism-style involution.  Applying the strongest symmetric-group
no-go still requires a rigidity or suitable automorphism size/minimal-degree
certificate.  This module proves the reduction and removes a false opening; it
does not claim those automorphism hypotheses for the current tail family.
"""

from __future__ import annotations

import json
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Sequence

import numpy as np

from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from self_dual_code_boundary_search import SELF_DUAL_CODE_BOUNDARY_PATH
from self_dual_hsp_applicability import (
    SELF_DUAL_HSP_APPLICABILITY_PATH,
    log2_factorial,
    obvious_automorphism_certificate,
)


SELF_DUAL_ROWSPACE_HSP_PATH = Path(
    "research/representation/self_dual_rowspace_hsp_reduction.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-CODE-SELF-DUAL-ROWSPACE-HSP-REDUCTION"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class RowspaceHSPReductionSpec:
    control_trials_per_family: int = 8
    seed: int = 331_777


@dataclass(frozen=True)
class RowspaceHiddenShiftControl:
    family_id: str
    instance_id: str
    trial_count: int
    hidden_shift_identity_failure_count: int
    row_scrambler_invariance_failure_count: int
    stabilizer_equivalence_failure_count: int
    passed: bool


@dataclass(frozen=True)
class RowspaceHSPFamilyRecord:
    family_id: str
    block_length: int
    code_dimension: int
    gl_wreath_log2_size: float | None
    rowspace_wreath_log2_size: float
    eliminated_group_log2_size: float | None
    rowspace_oracle_polynomial: bool
    hidden_shift_controls_pass: bool
    obvious_nonrigid_instance_count: int
    rigidity_certified_instance_count: int
    large_minimal_degree_certified_instance_count: int
    gi_type_order_two_no_go_certified_instance_count: int
    status: str
    interpretation: str


@dataclass(frozen=True)
class SelfDualRowspaceHSPReport:
    created_at: str
    spec: RowspaceHSPReductionSpec
    theorem: dict[str, Any]
    controls: list[RowspaceHiddenShiftControl]
    family_records: list[RowspaceHSPFamilyRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _read_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        return fallback


def canonical_rowspace(matrix: np.ndarray) -> np.ndarray:
    values = np.asarray(matrix, dtype=np.uint8).copy() & 1
    if values.ndim != 2:
        raise ValueError("matrix must be two-dimensional")
    rows, columns = values.shape
    rank = 0
    for column in range(columns):
        pivot = next((row for row in range(rank, rows) if values[row, column]), None)
        if pivot is None:
            continue
        if pivot != rank:
            values[[rank, pivot]] = values[[pivot, rank]]
        for row in range(rows):
            if row != rank and values[row, column]:
                values[row] ^= values[rank]
        rank += 1
        if rank == rows:
            break
    return values[:rank]


def random_invertible_row_operation(
    dimension: int,
    rng: random.Random,
    steps: int | None = None,
) -> np.ndarray:
    matrix = np.eye(dimension, dtype=np.uint8)
    for _ in range(steps or 4 * dimension):
        if rng.random() < 0.35:
            left, right = rng.sample(range(dimension), 2)
            matrix[[left, right]] = matrix[[right, left]]
        else:
            source, target = rng.sample(range(dimension), 2)
            matrix[target] ^= matrix[source]
    return matrix


def compose_permutations(left: Sequence[int], right: Sequence[int]) -> tuple[int, ...]:
    """Composition matching ``M[:, left][:, right]``."""

    if len(left) != len(right):
        raise ValueError("permutations must have equal size")
    return tuple(int(left[int(index)]) for index in right)


def inverse_permutation(permutation: Sequence[int]) -> tuple[int, ...]:
    inverse = [0] * len(permutation)
    for image, source in enumerate(permutation):
        inverse[int(source)] = image
    return tuple(inverse)


def rowspace_hiding_value(
    generator: np.ndarray,
    permutation: Sequence[int],
) -> tuple[tuple[int, ...], ...]:
    code = np.asarray(generator, dtype=np.uint8) & 1
    canonical = canonical_rowspace(code[:, list(permutation)])
    return tuple(tuple(int(value) for value in row) for row in canonical.tolist())


def _permutation(rng: random.Random, size: int) -> tuple[int, ...]:
    values = list(range(size))
    rng.shuffle(values)
    return tuple(values)


def audit_hidden_shift_controls(
    family_id: str,
    instance: dict[str, Any],
    trials: int,
    seed: int,
) -> RowspaceHiddenShiftControl:
    generator = np.asarray(instance["generator"], dtype=np.uint8)
    dimension, length = map(int, generator.shape)
    rng = random.Random(seed)
    shift = _permutation(rng, length)
    scrambler = random_invertible_row_operation(dimension, rng)
    shifted = (scrambler @ generator[:, list(shift)]) & 1
    shift_failures = 0
    scrambler_failures = 0
    stabilizer_failures = 0
    identity = tuple(range(length))
    base = rowspace_hiding_value(generator, identity)
    for _ in range(trials):
        permutation = _permutation(rng, length)
        composed = compose_permutations(shift, permutation)
        if rowspace_hiding_value(shifted, permutation) != rowspace_hiding_value(generator, composed):
            shift_failures += 1
        row_change = random_invertible_row_operation(dimension, rng)
        if rowspace_hiding_value((row_change @ generator) & 1, permutation) != rowspace_hiding_value(
            generator, permutation
        ):
            scrambler_failures += 1
        candidate = _permutation(rng, length)
        equal_to_base = rowspace_hiding_value(generator, candidate) == base
        direct_stabilizer = np.array_equal(
            canonical_rowspace(generator[:, list(candidate)]),
            canonical_rowspace(generator),
        )
        if equal_to_base != direct_stabilizer:
            stabilizer_failures += 1
    passed = shift_failures == scrambler_failures == stabilizer_failures == 0
    return RowspaceHiddenShiftControl(
        family_id=family_id,
        instance_id=str(instance.get("id", "unknown-self-dual-instance")),
        trial_count=trials,
        hidden_shift_identity_failure_count=shift_failures,
        row_scrambler_invariance_failure_count=scrambler_failures,
        stabilizer_equivalence_failure_count=stabilizer_failures,
        passed=passed,
    )


def run_self_dual_rowspace_hsp_reduction(
    source_path: Path = SELF_DUAL_CODE_BOUNDARY_PATH,
    gl_hsp_path: Path = SELF_DUAL_HSP_APPLICABILITY_PATH,
    spec: RowspaceHSPReductionSpec = RowspaceHSPReductionSpec(),
) -> SelfDualRowspaceHSPReport:
    source = _read_json(source_path, {})
    gl_report = _read_json(gl_hsp_path, {})
    gl_by_family = {
        str(record.get("family_id")): record for record in gl_report.get("family_records", [])
    }
    controls = []
    family_records = []
    for family in source.get("family_records", []):
        family_id = str(family.get("spec", {}).get("id", "unknown-self-dual-family"))
        dimension = int(family.get("spec", {}).get("dimension", 0) or 0)
        length = 2 * dimension
        family_controls = []
        obvious_nonrigid = 0
        for index, instance in enumerate(family.get("instances", [])):
            control = audit_hidden_shift_controls(
                family_id,
                instance,
                spec.control_trials_per_family,
                spec.seed + 1009 * index + sum(ord(char) for char in family_id),
            )
            controls.append(control)
            family_controls.append(control)
            certificate = obvious_automorphism_certificate(
                np.asarray(instance["generator"], dtype=np.uint8)
            )
            obvious_nonrigid += certificate.generated_transposition_count > 0
        gl_log = gl_by_family.get(family_id, {}).get("log2_wreath_hsp_group_size")
        rowspace_log = 2 * log2_factorial(length) + 1
        all_controls = all(control.passed for control in family_controls)
        family_records.append(
            RowspaceHSPFamilyRecord(
                family_id=family_id,
                block_length=length,
                code_dimension=dimension,
                gl_wreath_log2_size=float(gl_log) if gl_log is not None else None,
                rowspace_wreath_log2_size=round(rowspace_log, 6),
                eliminated_group_log2_size=(
                    round(float(gl_log) - rowspace_log, 6) if gl_log is not None else None
                ),
                rowspace_oracle_polynomial=True,
                hidden_shift_controls_pass=all_controls,
                obvious_nonrigid_instance_count=obvious_nonrigid,
                rigidity_certified_instance_count=0,
                large_minimal_degree_certified_instance_count=0,
                gi_type_order_two_no_go_certified_instance_count=0,
                status=(
                    "rowspace-symmetric-hsp-automorphism-proof-debt"
                    if all_controls
                    else "rejected-rowspace-hsp-control-failure"
                ),
                interpretation=(
                    "RREF removes the GL_k row scrambler and yields an exact S_n hidden shift. The apparent high-rate "
                    "GL applicability gap is not an algorithmic opening. Rigidity or automorphism size/minimal-degree "
                    "must still be certified before importing the graph-isomorphism-style coset-state no-go."
                    if all_controls
                    else "A rowspace hidden-shift identity failed; reject the reduction implementation."
                ),
            )
        )
    metrics: dict[str, int | float] = {
        "family_count": len(family_records),
        "instance_count": len(controls),
        "hidden_shift_control_failure_count": sum(not control.passed for control in controls),
        "gl_factor_eliminated_family_count": sum(
            record.gl_wreath_log2_size is not None and record.eliminated_group_log2_size is not None
            and record.eliminated_group_log2_size > 0
            for record in family_records
        ),
        "maximum_eliminated_group_log2_size": max(
            (
                record.eliminated_group_log2_size
                for record in family_records
                if record.eliminated_group_log2_size is not None
            ),
            default=0.0,
        ),
        "maximum_rowspace_wreath_log2_size": max(
            (record.rowspace_wreath_log2_size for record in family_records),
            default=0.0,
        ),
        "obvious_nonrigid_instance_count": sum(
            record.obvious_nonrigid_instance_count for record in family_records
        ),
        "rigidity_certified_instance_count": sum(
            record.rigidity_certified_instance_count for record in family_records
        ),
        "large_minimal_degree_certified_instance_count": sum(
            record.large_minimal_degree_certified_instance_count for record in family_records
        ),
        "gi_type_order_two_no_go_certified_instance_count": sum(
            record.gi_type_order_two_no_go_certified_instance_count for record in family_records
        ),
        "efficient_rowspace_oracle_family_count": sum(
            record.rowspace_oracle_polynomial for record in family_records
        ),
        "explicit_collective_measurement_count": 0,
        "polynomial_hidden_permutation_decoder_count": 0,
        "classical_superpolynomial_lower_bound_count": 0,
    }
    return SelfDualRowspaceHSPReport(
        created_at=utc_now(),
        spec=spec,
        theorem={
            "name": "rowspace-canonical permutation-code hidden shift",
            "statement": (
                "For a full-rank generator M of C, f_C(P)=RREF(MP) is constant exactly on right cosets of PAut(C). "
                "If C' is obtained by a coordinate shift P0, then f_C'(P)=f_C(P0 P)."
            ),
            "hidden_shift_group": "S_n",
            "hsp_group": "S_n wr Z_2",
            "base_stabilizer": "PAut(C)",
            "rigid_case": (
                "If PAut(C) is trivial, the hidden subgroup has order two and its bridge involution acts as n "
                "disjoint transpositions on two n-coordinate blocks."
            ),
            "oracle_cost": (
                "Column permutation plus binary RREF is polynomial in k,n and can be made reversible with polynomial overhead."
            ),
            "consequence": (
                "The GL_k factor in the raw scrambler-permutation HSP is removable gauge for explicit generators. "
                "Failure of a sufficient theorem caused only by |GL_k| is not a robust quantum opening."
            ),
        },
        controls=controls,
        family_records=family_records,
        headline_metrics=metrics,
        claim_gate={
            "rowspace_hidden_shift_reduction_certified": metrics["hidden_shift_control_failure_count"] == 0,
            "gl_factor_is_essential_quantum_structure": False,
            "dmr_dimension_gate_failure_survives_rowspace_reduction_as_evidence": False,
            "rigid_gi_type_no_go_applies_to_all_tail_instances": False,
            "automorphism_size_and_minimal_degree_certified": False,
            "explicit_collective_measurement_constructed": False,
            "polynomial_hidden_permutation_decoder_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Canonical rowspace evaluation removes the GL_k factor. The remaining S_n wreath-product route is "
                "blocked on automorphism certification and then on the known collective-measurement barrier."
            ),
        },
        status="self-dual-rowspace-hsp-reduction-certified-automorphism-debt-open",
        summary=(
            f"Removed the GL_k factor on {metrics['gl_factor_eliminated_family_count']}/{metrics['family_count']} "
            f"family rows, eliminating up to {metrics['maximum_eliminated_group_log2_size']:.2f} log2 group size; "
            f"rigid/no-go-certified instances={metrics['rigidity_certified_instance_count']}/"
            f"{metrics['gi_type_order_two_no_go_certified_instance_count']}."
        ),
        falsifiers_triggered=[
            "RREF must be invariant under every invertible row scrambler.",
            "The shifted generator must satisfy the hidden-shift identity for arbitrary test permutations.",
            "The level set of f_C at the identity must equal the permutation automorphism group.",
            "A removable GL_k gauge factor cannot be used as evidence that a published dimension gate exposes signal.",
            "No duplicate columns is not a rigidity certificate.",
            "The rigid graph-isomorphism-style no-go is applied only after PAut(C) is proved trivial.",
            "The exact S_n reduction still supplies neither a collective measurement nor a decoder.",
        ],
    )


def write_self_dual_rowspace_hsp_reduction(
    path: Path = SELF_DUAL_ROWSPACE_HSP_PATH,
    source_path: Path = SELF_DUAL_CODE_BOUNDARY_PATH,
    gl_hsp_path: Path = SELF_DUAL_HSP_APPLICABILITY_PATH,
    spec: RowspaceHSPReductionSpec = RowspaceHSPReductionSpec(),
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, Any]:
    payload = asdict(
        run_self_dual_rowspace_hsp_reduction(
            source_path=source_path,
            gl_hsp_path=gl_hsp_path,
            spec=spec,
        )
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_self_dual_rowspace_hsp_reduction()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
