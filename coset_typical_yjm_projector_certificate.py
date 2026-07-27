"""Exact YJM-projector trace identity and explicit-evaluator scaling audit.

The diagonal Jucys-Murphy spectrum gives an exact rank-one tableau projector
inside every diagonal ``S_n`` irrep.  If a separator ``H`` commutes with the
diagonal action, then

    Tr(P_T H^d) = Tr(M_nu^d),

where ``M_nu`` is the separator's Kronecker-multiplicity block.  This module
certifies that identity over rational group algebra on two controls and keeps
the implementation's factorial pair-state growth separate from the theorem.
"""

from __future__ import annotations

import hashlib
import json
import math
import time
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path

from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from symmetric_character import kronecker_coefficient
from symmetric_yjm_projector_trace import (
    exact_yjm_projector_power_traces,
)


CERTIFICATE_PATH = Path(
    "research/certificates/coset_typical_yjm_projector_certificate.json"
)
REPORT_PATH = Path(
    "research/representation/coset_typical_yjm_projector_certificate.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-TYPICAL-YJM-PROJECTOR-TRACE"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
DEPENDENCY_PATHS = (
    Path("symmetric_yjm_projector_trace.py"),
    Path("coset_jucys_murphy_label_transform.py"),
    Path("coset_typical_class_contraction_scaling.py"),
    Path("coset_typical_commutant_moment_audit.py"),
    Path("symmetric_character.py"),
)
CONTROL_SPECS = (
    ((3, 1, 1), (3, 2), 2),
    ((4, 2), (4, 2), 2),
)


@dataclass(frozen=True)
class ExactProjectorControlRecord:
    n: int
    source_partition: list[int]
    target_partition: list[int]
    kronecker_multiplicity: int
    tableau_index: int
    tableau_content_vector: list[int]
    projector_trace: str
    projector_state_counts_by_label: list[int]
    projector_state_count: int
    power_traces: list[str]
    power_state_counts: list[int]
    explicit_pair_state_space_size: int
    separator_term_count: int
    characteristic_polynomial_coefficients: list[str]
    discriminant: str
    exact_minimum_gap: str
    square_free: bool


@dataclass(frozen=True)
class YJMProjectorCertificateReport:
    created_at: str
    theorem_contract: dict[str, object]
    records: list[ExactProjectorControlRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _dependency_hashes() -> dict[str, str]:
    root = Path(__file__).resolve().parent
    return {
        str(path): hashlib.sha256((root / path).read_bytes()).hexdigest()
        for path in DEPENDENCY_PATHS
    }


def _quadratic_certificate(
    first_trace: Fraction,
    second_trace: Fraction,
) -> dict[str, object]:
    determinant = (first_trace * first_trace - second_trace) / 2
    discriminant = first_trace * first_trace - 4 * determinant
    if discriminant <= 0:
        raise ArithmeticError("control block does not have two distinct real roots")
    numerator_root = math.isqrt(discriminant.numerator)
    denominator_root = math.isqrt(discriminant.denominator)
    exact_square = (
        numerator_root * numerator_root == discriminant.numerator
        and denominator_root * denominator_root == discriminant.denominator
    )
    if exact_square:
        exact_gap = str(Fraction(numerator_root, denominator_root))
    else:
        numerator_text = (
            str(numerator_root)
            if numerator_root * numerator_root == discriminant.numerator
            else f"sqrt({discriminant.numerator})"
        )
        denominator_text = (
            str(denominator_root)
            if denominator_root * denominator_root == discriminant.denominator
            else f"sqrt({discriminant.denominator})"
        )
        exact_gap = f"{numerator_text}/{denominator_text}"
    return {
        "characteristic_polynomial_coefficients": [
            "1",
            str(-first_trace),
            str(determinant),
        ],
        "discriminant": str(discriminant),
        "exact_minimum_gap": exact_gap,
        "square_free": discriminant != 0,
    }


def _serialize_control(raw: dict[str, object]) -> dict[str, object]:
    traces = tuple(raw["power_traces"])
    if len(traces) != 2:
        raise ArithmeticError("quadratic control requires two power traces")
    quadratic = _quadratic_certificate(traces[0], traces[1])
    return {
        "n": raw["n"],
        "source_partition": list(raw["source_partition"]),
        "target_partition": list(raw["target_partition"]),
        "kronecker_multiplicity": int(raw["projector_trace"]),
        "tableau_index": raw["tableau_index"],
        "tableau_content_vector": list(raw["tableau_content_vector"]),
        "projector_trace": str(raw["projector_trace"]),
        "projector_state_counts_by_label": list(
            raw["projector_state_counts_by_label"]
        ),
        "projector_state_count": raw["projector_state_count"],
        "power_traces": [str(value) for value in traces],
        "power_state_counts": list(raw["power_state_counts"]),
        "explicit_pair_state_space_size": (
            raw["explicit_pair_state_space_size"]
        ),
        "separator_term_count": raw["separator_term_count"],
        **quadratic,
    }


def write_exact_projector_certificate(
    path: Path = CERTIFICATE_PATH,
) -> dict[str, object]:
    """Generate exact rational controls; n=6 takes roughly one minute."""

    started = time.perf_counter()
    records = []
    for source, target, multiplicity in CONTROL_SPECS:
        if kronecker_coefficient(source, source, target) != multiplicity:
            raise ArithmeticError("control multiplicity changed")
        raw = exact_yjm_projector_power_traces(
            source,
            target,
            maximum_degree=multiplicity,
        )
        if raw["projector_trace"] != multiplicity:
            raise ArithmeticError("YJM projector missed the multiplicity")
        records.append(_serialize_control(raw))
    payload = {
        "certificate_contract": {
            "dependency_sha256": _dependency_hashes(),
            "arithmetic": "fractions.Fraction exact pair-group algebra",
            "scope": (
                "Exact controls for the YJM projector identity; explicit "
                "pair expansion is not a scalable evaluator."
            ),
            "elapsed_seconds": time.perf_counter() - started,
        },
        "records": records,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


def _load_certificate(path: Path = CERTIFICATE_PATH) -> dict[str, object]:
    resolved = path
    if not resolved.exists():
        resolved = Path(__file__).resolve().parent / path
    payload = json.loads(resolved.read_text())
    if payload.get("certificate_contract", {}).get(
        "dependency_sha256"
    ) != _dependency_hashes():
        raise ArithmeticError("YJM-projector dependency hash changed")
    return payload


def _validated_records(
    certificate: dict[str, object],
) -> list[ExactProjectorControlRecord]:
    records = [
        ExactProjectorControlRecord(**row)
        for row in certificate.get("records", [])
    ]
    if len(records) != len(CONTROL_SPECS):
        raise ArithmeticError("YJM-projector control count changed")
    for record, (source, target, multiplicity) in zip(records, CONTROL_SPECS):
        if tuple(record.source_partition) != source:
            raise ArithmeticError("YJM-projector source control changed")
        if tuple(record.target_partition) != target:
            raise ArithmeticError("YJM-projector target control changed")
        if record.kronecker_multiplicity != multiplicity:
            raise ArithmeticError("YJM-projector multiplicity changed")
        if Fraction(record.projector_trace) != multiplicity:
            raise ArithmeticError("projector trace is not the multiplicity")
        traces = [Fraction(value) for value in record.power_traces]
        quadratic = _quadratic_certificate(traces[0], traces[1])
        if quadratic["characteristic_polynomial_coefficients"] != (
            record.characteristic_polynomial_coefficients
        ):
            raise ArithmeticError("stored characteristic polynomial is inconsistent")
        if quadratic["discriminant"] != record.discriminant:
            raise ArithmeticError("stored discriminant is inconsistent")
        if not record.square_free:
            raise ArithmeticError("control separator is not square-free")
        if record.power_state_counts[-1] > record.explicit_pair_state_space_size:
            raise ArithmeticError("pair-state count exceeds its state space")
    return records


def build_yjm_projector_certificate_report() -> YJMProjectorCertificateReport:
    records = _validated_records(_load_certificate())
    n6 = records[-1]
    saturation = (
        n6.power_state_counts[-1] / n6.explicit_pair_state_space_size
    )
    n10_pair_space = math.factorial(10) ** 2
    metrics: dict[str, int | float] = {
        "exact_yjm_projector_trace_identity_theorem_count": 1,
        "exact_control_count": len(records),
        "exact_projector_trace_count": len(records),
        "exact_power_trace_count": sum(
            len(record.power_traces) for record in records
        ),
        "exact_square_free_control_count": sum(
            int(record.square_free) for record in records
        ),
        "n6_degree2_pair_state_count": n6.power_state_counts[-1],
        "n6_explicit_pair_state_space_size": (
            n6.explicit_pair_state_space_size
        ),
        "n6_degree2_pair_state_saturation_fraction": saturation,
        "n10_explicit_pair_state_space_size": n10_pair_space,
        "explicit_pair_algebra_scaling_falsification_count": int(
            saturation > 0.9
        ),
        "young_tower_compressed_exact_trace_evaluator_count": 0,
        "exact_n10_multiplicity6_power_trace_count": 0,
        "exact_n10_multiplicity6_characteristic_polynomial_count": 0,
        "polynomial_exact_trace_evaluator_count": 0,
        "coherent_typical_multiplicity_transform_count": 0,
        "typical_label_hidden_involution_decoder_count": 0,
    }
    return YJMProjectorCertificateReport(
        created_at=utc_now(),
        theorem_contract={
            "decomposition": (
                "Under the diagonal S_n action, V_lambda tensor V_lambda "
                "decomposes as a direct sum of V_nu tensor M_nu."
            ),
            "joint_spectrum": (
                "Diagonal Jucys-Murphy elements have simple joint content "
                "spectrum indexed by standard tableaux across all irreps."
            ),
            "projector": (
                "The product of univariate Lagrange projectors for one content "
                "vector is |T><T| tensor identity on M_nu and vanishes on every "
                "other tableau line."
            ),
            "commutant": (
                "A diagonal-S_n-commuting separator H restricts to identity "
                "on V_nu tensor a multiplicity operator M_nu."
            ),
            "trace_identity": (
                "Therefore Tr(P_T H^d)=Tr(M_nu^d) exactly for every d>=0."
            ),
            "control_arithmetic": (
                "The n=5 and n=6 controls expand P_T and H over rational "
                "pair-group algebra and recover exact square-free quadratics."
            ),
            "scaling_boundary": (
                "The identity is exact, but literal pair-group expansion has "
                "(n!)^2 states and nearly saturates that space by degree two "
                "at n=6. A Young-tower or centralizer recurrence is still required."
            ),
        },
        records=records,
        headline_metrics=metrics,
        claim_gate={
            "exact_yjm_projector_trace_identity_proved": True,
            "exact_controls_reproduced": True,
            "control_spectra_square_free": True,
            "explicit_pair_algebra_scales_polynomially": False,
            "young_tower_compressed_evaluator_constructed": False,
            "n10_multiplicity6_exactly_certified": False,
            "all_n_simple_spectrum_proved": False,
            "coherent_transform_proved": False,
            "hidden_involution_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The projector identity turns the exact-certificate target into "
                "a trace-evaluation problem, but the implemented exact evaluator "
                "is factorial and has not reached the n=10 multiplicity-six block."
            ),
        },
        status=(
            "exact-projector-trace-identity-proved-explicit-evaluator-falsified"
        ),
        summary=(
            "An exact YJM tableau projector reduces multiplicity-block moments "
            "to ordinary representation traces. Rational n=5 and n=6 controls "
            "verify the construction, while 93.5% pair-state saturation at n=6 "
            "kills literal group-algebra expansion as the scalable route."
        ),
        falsifiers_triggered=[
            "The exact projector identity does not make its literal pair-group expansion efficient.",
            "At n=6 and degree two, the evaluator already occupies more than 93% of the full pair state space.",
            "The n=10 multiplicity-six numerical spectrum remains uncertified.",
            "No Young-tower recurrence, all-n gap theorem, coherent transform, or decoder is supplied.",
        ],
    )


def write_yjm_projector_certificate_report(
    output_path: Path = REPORT_PATH,
    *,
    recompute: bool = False,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, object]:
    if recompute:
        write_exact_projector_certificate()
    payload = asdict(build_yjm_projector_certificate_report())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-TYPICAL-YJM-PROJECTOR-PAIR-ALGEBRA-SATURATION",
                source=str(output_path),
                claim=(
                    "Exact YJM-projector power traces can be evaluated at "
                    "typical n by literal rational pair-group expansion."
                ),
                reason_invalid=(
                    "The degree-two n=6 control reaches 484,912 of 518,400 "
                    "possible pair states; the ambient state space is (n!)^2."
                ),
                lesson=(
                    "Preserve the exact projector identity but replace pair "
                    "expansion with a Young-tower, centralizer, or tensor-network "
                    "recurrence before attempting the n=10 multiplicity-six block."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=payload["headline_metrics"],
            )
        )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-LATEST"
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
                artifacts={
                    "coset_typical_yjm_projector_certificate": str(output_path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    print(
        json.dumps(
            write_yjm_projector_certificate_report()["headline_metrics"],
            indent=2,
            sort_keys=True,
        )
    )
