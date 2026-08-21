"""Applicability audit for the code-equivalence hidden-subgroup no-go.

Permutation code equivalence for full-rank k x n matrices reduces first to a
hidden shift over ``GL_k(F_q) x S_n`` and then to an HSP over its wreath product
with Z_2.  Dinh, Moore, and Russell give a sufficient condition under which a
single coset state carries negligible information:

    q^(k^2) <= n^(0.2 n),
    |Aut(C)| <= exp(o(n)),
    minimal_degree(Aut(C)) = Omega(n).

For binary self-dual codes, k=n/2.  The first condition fails
asymptotically because its logarithms scale as Theta(n^2) versus
Theta(n log n).  This failure does not produce a quantum algorithm; it only
means the cited theorem cannot be used to close the high-rate self-dual route.

The module records the exact HSP group and hiding functions, computes group
encoding costs, checks every sufficient-condition gate separately, detects
obvious weight-two transposition automorphisms, and emits the measurement and
decoding obligations that remain open.
"""

from __future__ import annotations

import json
import math
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Sequence

import numpy as np

from code_schur_filtration import row_basis
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from self_dual_code_boundary_search import SELF_DUAL_CODE_BOUNDARY_PATH


SELF_DUAL_HSP_APPLICABILITY_PATH = Path(
    "research/representation/self_dual_code_hsp_applicability.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-CODE-SELF-DUAL-HSP-APPLICABILITY"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class HSPApplicabilitySpec:
    field_size: int = 2
    dimension_condition_constant: float = 0.2


@dataclass(frozen=True)
class ObviousAutomorphismCertificate:
    duplicate_column_class_count: int
    duplicated_coordinate_count: int
    generated_transposition_count: int
    automorphism_group_size_lower_bound: int
    minimal_degree_upper_bound: int | None
    certificate_scope: str


@dataclass(frozen=True)
class HSPFamilyApplicabilityRecord:
    family_id: str
    block_length: int
    code_dimension: int
    rate: float
    log2_dimension_condition_left: float
    log2_dimension_condition_right: float
    dimension_condition_log2_gap: float
    dimension_condition_passes: bool
    log2_general_linear_group_size: float
    log2_symmetric_group_size: float
    log2_hidden_shift_group_size: float
    log2_wreath_hsp_group_size: float
    minimum_group_register_qubits: int
    obvious_transposition_instance_count: int
    automorphism_size_condition_certified: bool
    automorphism_minimal_degree_condition_certified: bool
    single_coset_indistinguishability_theorem_applies: bool
    status: str
    interpretation: str


@dataclass(frozen=True)
class SelfDualHSPApplicabilityReport:
    created_at: str
    spec: HSPApplicabilitySpec
    reduction_contract: dict[str, Any]
    literature_no_go_contract: dict[str, Any]
    family_records: list[HSPFamilyApplicabilityRecord]
    obvious_automorphism_certificates: list[dict[str, Any]]
    open_measurement_program: list[dict[str, Any]]
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


def log2_gl_size(dimension: int, field_size: int = 2) -> float:
    if dimension < 0:
        raise ValueError("dimension must be nonnegative")
    if field_size < 2:
        raise ValueError("field_size must be at least two")
    return sum(
        math.log2(field_size**dimension - field_size**index)
        for index in range(dimension)
    )


def log2_factorial(value: int) -> float:
    if value < 0:
        raise ValueError("value must be nonnegative")
    return math.lgamma(value + 1) / math.log(2)


def dimension_condition(
    block_length: int,
    code_dimension: int,
    field_size: int = 2,
    constant: float = 0.2,
) -> tuple[float, float, float, bool]:
    if block_length < 2:
        raise ValueError("block_length must be at least two")
    left = code_dimension * code_dimension * math.log2(field_size)
    right = constant * block_length * math.log2(block_length)
    return left, right, left - right, left <= right


def obvious_automorphism_certificate(generator: np.ndarray) -> ObviousAutomorphismCertificate:
    code = row_basis(generator)
    values = []
    for coordinate in range(code.shape[1]):
        value = 0
        for row, bit in enumerate(code[:, coordinate].tolist()):
            if bit:
                value |= 1 << row
        values.append(value)
    classes = [count for count in Counter(values).values() if count > 1]
    lower_bound = math.prod(math.factorial(count) for count in classes)
    transpositions = sum(math.comb(count, 2) for count in classes)
    return ObviousAutomorphismCertificate(
        duplicate_column_class_count=len(classes),
        duplicated_coordinate_count=sum(classes),
        generated_transposition_count=transpositions,
        automorphism_group_size_lower_bound=lower_bound,
        minimal_degree_upper_bound=2 if transpositions else None,
        certificate_scope=(
            "Swapping equal generator columns fixes the generator matrix exactly. Absence of duplicate columns does "
            "not certify a trivial automorphism group or a linear minimal degree."
        ),
    )


def _family_record(
    family: dict[str, Any],
    spec: HSPApplicabilitySpec,
) -> tuple[HSPFamilyApplicabilityRecord, list[dict[str, Any]]]:
    family_id = str(family.get("spec", {}).get("id", "unknown-self-dual-family"))
    dimension = int(family.get("spec", {}).get("dimension", 0) or 0)
    length = 2 * dimension
    left, right, gap, condition = dimension_condition(
        length,
        dimension,
        field_size=spec.field_size,
        constant=spec.dimension_condition_constant,
    )
    log_gl = log2_gl_size(dimension, spec.field_size)
    log_sn = log2_factorial(length)
    log_base = log_gl + log_sn
    log_wreath = 2 * log_base + 1
    certificates = []
    for instance in family.get("instances", []):
        certificate = obvious_automorphism_certificate(
            np.asarray(instance["generator"], dtype=np.uint8)
        )
        certificates.append(
            {
                "family_id": family_id,
                "instance_id": str(instance.get("id", "unknown-self-dual-instance")),
                **asdict(certificate),
            }
        )
    transposition_instances = sum(
        certificate["generated_transposition_count"] > 0 for certificate in certificates
    )
    size_certified = False
    minimal_degree_certified = False
    theorem_applies = condition and size_certified and minimal_degree_certified
    return (
        HSPFamilyApplicabilityRecord(
            family_id=family_id,
            block_length=length,
            code_dimension=dimension,
            rate=dimension / length if length else 0.0,
            log2_dimension_condition_left=round(left, 6),
            log2_dimension_condition_right=round(right, 6),
            dimension_condition_log2_gap=round(gap, 6),
            dimension_condition_passes=condition,
            log2_general_linear_group_size=round(log_gl, 6),
            log2_symmetric_group_size=round(log_sn, 6),
            log2_hidden_shift_group_size=round(log_base, 6),
            log2_wreath_hsp_group_size=round(log_wreath, 6),
            minimum_group_register_qubits=math.ceil(log_wreath),
            obvious_transposition_instance_count=transposition_instances,
            automorphism_size_condition_certified=size_certified,
            automorphism_minimal_degree_condition_certified=minimal_degree_certified,
            single_coset_indistinguishability_theorem_applies=theorem_applies,
            status=(
                "published-single-coset-no-go-applies-collective-measurement-proof-debt"
                if theorem_applies
                else (
                    "published-no-go-dimension-gate-fails-open-measurement-proof-debt"
                    if not condition
                    else "published-no-go-automorphism-hypotheses-unproved-proof-debt"
                )
            ),
            interpretation=(
                "The Dinh-Moore-Russell sufficient theorem does not apply because the GL_k dimension term violates "
                "q^(k^2) <= n^(0.2n). This is an applicability gap, not evidence that one coset state is informative."
                if not condition
                else (
                    "The dimension gate passes, but automorphism size and minimal degree still require proof."
                    if not theorem_applies
                    else "Every registered sufficient condition for single-coset indistinguishability is certified."
                )
            ),
        ),
        certificates,
    )


def run_self_dual_hsp_applicability(
    source_path: Path = SELF_DUAL_CODE_BOUNDARY_PATH,
    spec: HSPApplicabilitySpec = HSPApplicabilitySpec(),
) -> SelfDualHSPApplicabilityReport:
    source = _read_json(source_path, {})
    records = []
    certificates = []
    for family in source.get("family_records", []):
        record, family_certificates = _family_record(family, spec)
        records.append(record)
        certificates.extend(family_certificates)
    metrics: dict[str, int | float] = {
        "family_count": len(records),
        "instance_count": len(certificates),
        "maximum_block_length": max((record.block_length for record in records), default=0),
        "maximum_code_dimension": max((record.code_dimension for record in records), default=0),
        "dimension_condition_pass_family_count": sum(record.dimension_condition_passes for record in records),
        "dimension_condition_fail_family_count": sum(not record.dimension_condition_passes for record in records),
        "single_coset_no_go_certified_family_count": sum(
            record.single_coset_indistinguishability_theorem_applies for record in records
        ),
        "obvious_transposition_instance_count": sum(
            certificate["generated_transposition_count"] > 0 for certificate in certificates
        ),
        "automorphism_size_condition_certified_family_count": sum(
            record.automorphism_size_condition_certified for record in records
        ),
        "automorphism_minimal_degree_certified_family_count": sum(
            record.automorphism_minimal_degree_condition_certified for record in records
        ),
        "maximum_dimension_condition_log2_gap": max(
            (record.dimension_condition_log2_gap for record in records),
            default=0.0,
        ),
        "maximum_log2_wreath_hsp_group_size": max(
            (record.log2_wreath_hsp_group_size for record in records),
            default=0.0,
        ),
        "maximum_group_register_qubits": max(
            (record.minimum_group_register_qubits for record in records),
            default=0,
        ),
        "efficient_wreath_product_qft_count": 0,
        "explicit_single_coset_measurement_count": 0,
        "explicit_multicoset_measurement_count": 0,
        "polynomial_hidden_permutation_decoder_count": 0,
        "classical_superpolynomial_lower_bound_count": 0,
    }
    return SelfDualHSPApplicabilityReport(
        created_at=utc_now(),
        spec=spec,
        reduction_contract={
            "problem": "binary permutation code equivalence search",
            "input_promise": "M' = S M P for full-rank k x n generators",
            "hidden_shift_group": "G0 = GL_k(F_2) x S_n",
            "hiding_functions": [
                "f0(A,P) = A^(-1) M P",
                "f1(A,P) = A^(-1) M' P",
            ],
            "shift": "(S^(-1), P) under the source convention",
            "hsp_group": "G0 wr Z_2 = G0^2 semidirect Z_2",
            "base_stabilizer": (
                "H0(M) = {(A,P): A^(-1) M P = M}; for full-row-rank M, projection to PAut(C) has one A per P."
            ),
            "hidden_subgroup": (
                "K = ((H0, s^(-1)H0s),0) union ((H0s, s^(-1)H0),1), with |K|=2|H0|^2."
            ),
            "oracle_access": (
                "Explicit generators make finite-field inversion, matrix multiplication, and coordinate permutation "
                "classically polynomial and reversibly implementable with polynomial overhead."
            ),
        },
        literature_no_go_contract={
            "id": "Dinh-Moore-Russell-2015-single-coset-code-equivalence",
            "theorem_type": "sufficient condition for single-coset-state indistinguishability",
            "hypotheses": [
                "q^(k^2) <= n^(0.2 n)",
                "|PAut(C)| <= exp(o(n))",
                "minimal_degree(PAut(C)) = Omega(n)",
            ],
            "conclusion": (
                "Conjugate hidden subgroups are indistinguishable by strong Fourier sampling; equivalently, no "
                "measurement of one coset state yields useful hidden-permutation information under the paper's definition."
            ),
            "scope_warning": (
                "Failure of any sufficient hypothesis neither refutes the theorem nor proves distinguishability. "
                "The high-rate self-dual family requires a new character/trace-distance analysis."
            ),
            "literature_ids": [
                "Dinh-Moore-Russell-2015-Code-Equivalence-Coset-States",
                "Moore-Russell-Schulman-2008-Symmetric-Group-Fourier",
                "Hallgren-Roetteler-Sen-2010-Coset-State-Limits",
            ],
        },
        family_records=records,
        obvious_automorphism_certificates=certificates,
        open_measurement_program=[
            {
                "priority": 1,
                "hypothesis": (
                    "The high-rate GL_k(F_2) factor creates a measurable one- or few-coset representation sector not "
                    "covered by the low-rate Dinh-Moore-Russell bound."
                ),
                "proof_obligations": [
                    "Derive the one-coset conjugate-state trace distance or accessible information at k=n/2.",
                    "Identify which irreducible sectors of (GL_k(2) x S_n) wr Z_2 carry the signal.",
                    "Prove inverse-polynomial sector mass under natural coset-state preparation.",
                    "Construct a polynomial-size measurement and hidden-permutation decoder.",
                    "Show the same statistic is not a public-generator classical invariant.",
                ],
                "falsifiers": [
                    "A strengthened character bound extends single-coset indistinguishability to k=Theta(n).",
                    "All signal lies in exponentially rare or exponentially large-description sectors.",
                    "The measurement statistic is computable classically from M and M'.",
                    "Decoding still requires exhaustive S_n or GL_k orbit search.",
                ],
            },
            {
                "priority": 2,
                "hypothesis": (
                    "An equivariant low-rate representation of a self-dual code preserves the hidden transporter and "
                    "moves the instance into the proven no-go or a more tractable HSP."
                ),
                "proof_obligations": [
                    "Define the representation without choosing a noncanonical coordinate subset.",
                    "Prove transporter preservation in both directions.",
                    "Charge dimension, oracle preparation, and decoder recovery.",
                ],
                "falsifiers": [
                    "The representation breaks coordinate equivariance.",
                    "The reduced object is classically canonicalizable.",
                    "Recovering the original permutation is exponential or ambiguous.",
                ],
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "code_equivalence_to_wreath_hsp_reduction_formalized": True,
            "published_single_coset_no_go_applies_to_registered_self_dual_families": (
                metrics["single_coset_no_go_certified_family_count"] == metrics["family_count"]
                and metrics["family_count"] > 0
            ),
            "failure_of_sufficient_no_go_hypothesis_is_quantum_evidence": False,
            "efficient_wreath_product_qft_known": False,
            "explicit_measurement_constructed": False,
            "polynomial_hidden_permutation_decoder_constructed": False,
            "classical_superpolynomial_lower_bound_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The standard single-coset code-equivalence no-go does not cover rate-one-half self-dual codes, but "
                "no informative sector, efficient measurement, or decoder has been constructed."
            ),
        },
        status="high-rate-self-dual-hsp-no-go-applicability-gap-open",
        summary=(
            f"The Dinh-Moore-Russell dimension gate fails on "
            f"{metrics['dimension_condition_fail_family_count']}/{metrics['family_count']} family rows; certified "
            f"single-coset no-go rows={metrics['single_coset_no_go_certified_family_count']}, explicit measurements="
            f"{metrics['explicit_single_coset_measurement_count'] + metrics['explicit_multicoset_measurement_count']}."
        ),
        falsifiers_triggered=[
            "The HSP group includes both GL_k(F_2) and S_n; omitting the scrambler factor changes the problem.",
            "Every sufficient hypothesis of a literature no-go is checked separately before applying its conclusion.",
            "Failure of q^(k^2)<=n^(0.2n) is an applicability gap, not evidence that a coset state is informative.",
            "Duplicate-column transpositions disprove large minimal degree only on the instances where they occur.",
            "Absence of duplicate columns does not certify trivial automorphism group or linear minimal degree.",
            "Polynomial group-register qubits do not imply an efficient QFT, measurement, or decoder.",
            "Any proposed quantum statistic must survive the public-generator classical baselines.",
        ],
    )


def write_self_dual_hsp_applicability(
    path: Path = SELF_DUAL_HSP_APPLICABILITY_PATH,
    source_path: Path = SELF_DUAL_CODE_BOUNDARY_PATH,
    spec: HSPApplicabilitySpec = HSPApplicabilitySpec(),
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, Any]:
    payload = asdict(run_self_dual_hsp_applicability(source_path=source_path, spec=spec))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_self_dual_hsp_applicability()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
