"""Literature-backed entanglement-width gate for hidden involutions.

Two primary no-go theorems define the minimum architecture:

* Moore, Russell, and Schulman (2005) rule out efficient recovery by
  single-register strong Fourier sampling, even with an arbitrary POVM on one
  coset state.
* Moore and Russell (2005) prove that nonnegligible information in the
  GI-relevant symmetric-group hidden-involution ensemble requires a
  measurement entangled across ``Omega(n log n)`` coset states.

The second result is an entanglement-width requirement, not merely a sample
count.  Measuring a polynomial number of registers separately and classically
postprocessing the outcomes does not satisfy it.

This module inventories current one-, two-, and three-register mechanisms.
They remain useful local primitives and falsifiers, but none is an end-to-end
candidate until embedded in a uniform growing-width associator/measurement
network with a compressed outcome and decoder.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


REPORT_PATH = Path(
    "research/representation/coset_entanglement_width_gate.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-ENTANGLEMENT-WIDTH-GATE"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class BoundedRegisterMechanismRecord:
    id: str
    artifact: str
    maximum_joint_register_count: int
    proved_role: str
    missing_growing_width_composition: str
    end_to_end_information_eligible: bool
    status: str


@dataclass(frozen=True)
class EntanglementWidthGateReport:
    created_at: str
    literature_theorems: list[dict[str, object]]
    architecture_contract: dict[str, object]
    bounded_register_mechanisms: list[BoundedRegisterMechanismRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _bounded_mechanisms() -> list[BoundedRegisterMechanismRecord]:
    rows = (
        (
            "one-copy-covariant-frame",
            "coset_covariant_frame.py",
            1,
            "Exact central frame and one-copy PGM normalization.",
        ),
        (
            "two-copy-frame",
            "coset_two_copy_frame.py",
            2,
            "Exact average-frame spectrum and PGM spectral bounds.",
        ),
        (
            "two-copy-transition",
            "coset_two_copy_transition_audit.py",
            2,
            "Finite cross-sector transition and PGM reconstruction control.",
        ),
        (
            "same-hidden-target-law",
            "coset_same_hidden_target_law.py",
            2,
            "Exact naturally weighted coupled-target distribution.",
        ),
        (
            "multiplicity-commutant",
            "coset_multiplicity_commutant_search.py",
            2,
            "Bounded-support multiplicity basis/separator primitive.",
        ),
        (
            "parity-complete-separator",
            "coset_typical_parity_complete_separator.py",
            2,
            "Finite all-source separator candidate through n=7.",
        ),
        (
            "carrier-information-search",
            "coset_carrier_information_audit.py",
            2,
            "Finite carrier-sensitive information optimization.",
        ),
        (
            "strong-fourier-information",
            "coset_strong_fourier_information_scaling.py",
            2,
            "Natural one- and two-copy strong Fourier baseline.",
        ),
        (
            "three-copy-recoupling",
            "coset_three_copy_recoupling_obstruction.py",
            3,
            "Overlapping-pair noncommutation and associator obstruction.",
        ),
        (
            "stable-three-copy-frame",
            "coset_stable_three_copy_frame.py",
            3,
            "Conditioned three-copy frame block encoding and gap control.",
        ),
        (
            "stable-three-copy-encoded-tree",
            "coset_stable_encoded_tree_certificate.py",
            3,
            "Finite-branch coherent coupling-tree label interface.",
        ),
    )
    return [
        BoundedRegisterMechanismRecord(
            id=identifier,
            artifact=artifact,
            maximum_joint_register_count=width,
            proved_role=role,
            missing_growing_width_composition=(
                "No uniform Omega(n log n)-register associator/POVM network, "
                "compressed covariant outcome, or decoder is supplied."
            ),
            end_to_end_information_eligible=False,
            status="local-primitive-only-bounded-entanglement-width",
        )
        for identifier, artifact, width, role in rows
    ]


def build_entanglement_width_gate_report() -> EntanglementWidthGateReport:
    mechanisms = _bounded_mechanisms()
    metrics: dict[str, int | float] = {
        "primary_literature_theorem_count": 2,
        "single_register_arbitrary_povm_no_go_theorem_count": 1,
        "omega_n_log_n_entanglement_width_theorem_count": 1,
        "bounded_register_mechanism_count": len(mechanisms),
        "maximum_current_joint_register_count": max(
            mechanism.maximum_joint_register_count
            for mechanism in mechanisms
        ),
        "bounded_mechanism_end_to_end_information_eligible_count": sum(
            mechanism.end_to_end_information_eligible
            for mechanism in mechanisms
        ),
        "growing_entanglement_width_architecture_count": 0,
        "polynomial_growing_associator_circuit_count": 0,
        "compressed_covariant_outcome_count": 0,
        "growing_width_hidden_involution_decoder_count": 0,
    }
    return EntanglementWidthGateReport(
        created_at=utc_now(),
        literature_theorems=[
            {
                "paper_id": "symmetric-defies-fourier-2005",
                "title": (
                    "The Symmetric Group Defies Strong Fourier Sampling: "
                    "Part I"
                ),
                "url": "https://arxiv.org/abs/quant-ph/0501056",
                "authors": [
                    "Cristopher Moore",
                    "Alexander Russell",
                    "Leonard J. Schulman",
                ],
                "theorem_scope": (
                    "GI-relevant symmetric-group HSP cannot be efficiently "
                    "solved by one-register strong Fourier sampling, even "
                    "with an arbitrary POVM on the coset state."
                ),
                "external_theorem_not_reproved_here": True,
            },
            {
                "paper_id": "moore-russell-multiregister-2005",
                "title": (
                    "Tight Results on Multiregister Fourier Sampling: Quantum "
                    "Measurements for Graph Isomorphism Require Entanglement"
                ),
                "url": "https://arxiv.org/abs/quant-ph/0511149",
                "authors": [
                    "Cristopher Moore",
                    "Alexander Russell",
                ],
                "theorem_scope": (
                    "Nonnegligible hidden-involution information requires a "
                    "measurement entangled across Omega(n log n) coset states; "
                    "the bound is tight up to a constant factor."
                ),
                "external_theorem_not_reproved_here": True,
            },
        ],
        architecture_contract={
            "required_entangled_register_width": "Omega(n log n)",
            "sample_count_is_not_enough": (
                "The registers must participate in one joint entangled POVM; "
                "separate measurements plus classical postprocessing do not "
                "meet the theorem's necessary architecture."
            ),
            "required_uniform_components": [
                "growing-copy diagonal-action decomposition",
                "uniform sequence of Kronecker/Racah associators",
                "polynomial state-dependent frame or measurement synthesis",
                "compressed covariant outcome representation",
                "polynomial hidden-involution decoder",
                "natural source and branch probability accounting",
            ],
            "allowed_role_for_bounded_controls": (
                "Local transform, recurrence, conditioning, information, and "
                "dequantization primitives only."
            ),
        },
        bounded_register_mechanisms=mechanisms,
        headline_metrics=metrics,
        claim_gate={
            "bounded_copy_mechanism_is_end_to_end_decoder_candidate": False,
            "omega_n_log_n_entanglement_width_required": True,
            "current_growing_width_architecture_exists": False,
            "polynomial_growing_associator_circuit_proved": False,
            "compressed_covariant_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Every implemented representation mechanism acts jointly on "
                "at most three coset-state registers, while primary no-go "
                "theorems require Omega(n log n)-register entanglement for "
                "nonnegligible information in the target ensemble."
            ),
        },
        status=(
            "bounded-copy-coset-route-quarantined-growing-entanglement-width-architecture-missing"
        ),
        summary=(
            f"Applied two primary Fourier-sampling no-go theorems to "
            f"{len(mechanisms)} current bounded-register mechanisms. Their "
            f"maximum joint width is {metrics['maximum_current_joint_register_count']}; "
            "all remain local primitives pending an Omega(n log n)-width "
            "measurement architecture."
        ),
        falsifiers_triggered=[
            (
                "An arbitrary one-register POVM is not a loophole in the "
                "strong Fourier no-go."
            ),
            (
                "Using polynomially many samples separately is not the same "
                "as an Omega(n log n)-register entangled measurement."
            ),
            (
                "Exact two- or three-copy spectra, gaps, and information "
                "cannot be promoted to nonnegligible full-ensemble information."
            ),
            (
                "A serious architecture must specify growing-copy associators, "
                "outcomes, and decoding rather than extrapolate bounded controls."
            ),
        ],
    )


def write_entanglement_width_gate_report(
    output_path: Path = REPORT_PATH,
    *,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, object]:
    payload = asdict(build_entanglement_width_gate_report())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-BOUNDED-COPY-MECHANISM-AS-GI-DECODER",
                source=str(output_path),
                claim=(
                    "A fixed one-, two-, or three-register representation "
                    "measurement can provide nonnegligible information for "
                    "the GI-relevant hidden-involution family."
                ),
                reason_invalid=(
                    "Primary multiregister lower bounds require entanglement "
                    "across Omega(n log n) coset states."
                ),
                lesson=(
                    "Keep bounded-copy modules as local primitives only and "
                    "require an explicit growing-width measurement network."
                ),
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-MEASUREMENT",
                    "PO-SUCCESS",
                    "PO-NO-GO",
                ],
                evidence=payload["headline_metrics"],
            )
        )
        result_id = (
            registry_result_id
            or f"RESULT-{registry_experiment_id}-COSET"
        )
        upsert_experiment_result(
            ExperimentResultRecord(
                id=result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=str(payload["created_at"]),
                status=str(payload["status"]),
                summary=str(payload["summary"]),
                metrics=dict(payload["headline_metrics"]),
                falsifiers_triggered=list(payload["falsifiers_triggered"]),
                artifacts={"coset_entanglement_width_gate": str(output_path)},
            )
        )
    return payload


if __name__ == "__main__":
    report = write_entanglement_width_gate_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
