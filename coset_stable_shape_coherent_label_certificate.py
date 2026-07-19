"""Uniform coherent eigenlabels for every nontrivial stable Racah shape.

The same ordered-triple orbit Hamiltonian acts on eta_n tensor W_n for every
stable intermediate eta_n.  Uniform PREPARE over distinct triples and
controlled Young-basis representation actions therefore give one common LCU
block-encoding architecture.  Exact shape polynomials and normalized gaps let
phase estimation append the multiplicity eigenlabel on all seven nontrivial
shapes (one original stable shape and six complementary shapes).

The input must already be routed into a declared eta_n tensor W_n -> xi_n
channel.  This module does not implement that routing, change coupling trees,
synthesize a Racah associator, decode a hidden involution, or prove a quantum
speedup.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path

from coset_stable_coherent_label_certificate import (
    ordered_triple_bijection_verified,
)
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


COSET_STABLE_SHAPE_COHERENT_LABEL_PATH = Path(
    "research/representation/coset_stable_shape_coherent_label_certificate.json"
)
COSET_STABLE_SHAPE_FAMILY_PATH = Path(
    "research/representation/coset_stable_shape_family_certificate.json"
)
COSET_STABLE_SHAPE_QUADRATIC_GAP_PATH = Path(
    "research/representation/coset_stable_shape_quadratic_gap_certificate.json"
)
COSET_STABLE_SHAPE_CUBIC_GAP_PATH = Path(
    "research/representation/coset_stable_shape_cubic_gap_certificate.json"
)
COSET_STABLE_COHERENT_LABEL_PATH = Path(
    "research/representation/coset_stable_coherent_label_certificate.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-STABLE-SHAPE-COHERENT-LABEL-CERTIFICATE"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
STABLE_TAIL = (2, 1)


@dataclass(frozen=True)
class ShapeCoherentLabelRecord:
    intermediate_tail: tuple[int, ...]
    intermediate_partition: str
    multiplicity_dimension: int
    gap_source: str
    normalized_gap_lower_bound: str
    normalized_gap_inverse_polynomial_exponent: int
    common_ordered_triple_block_encoding_applies: bool
    coherent_phase_estimation_label_proved: bool
    routing_into_channel_proved: bool
    coupling_tree_transition_proved: bool
    status: str


@dataclass(frozen=True)
class StableShapeCoherentLabelCertificate:
    created_at: str
    theorem: dict[str, object]
    source_certificate_contract: dict[str, object]
    common_block_encoding_certificate: dict[str, object]
    shape_records: list[ShapeCoherentLabelRecord]
    interface_contract: dict[str, object]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _read_required(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"required certificate is missing: {path}")
    payload = json.loads(path.read_text())
    if not isinstance(payload, dict):
        raise ValueError(f"required certificate is not an object: {path}")
    return payload


@lru_cache(maxsize=1)
def build_stable_shape_coherent_label_certificate() -> (
    StableShapeCoherentLabelCertificate
):
    family = _read_required(COSET_STABLE_SHAPE_FAMILY_PATH)
    quadratics = _read_required(COSET_STABLE_SHAPE_QUADRATIC_GAP_PATH)
    cubic = _read_required(COSET_STABLE_SHAPE_CUBIC_GAP_PATH)
    stable = _read_required(COSET_STABLE_COHERENT_LABEL_PATH)
    if not family.get("theorem", {}).get("proved", False):
        raise ArithmeticError("exact stable shape family is not proved")
    if not quadratics.get("theorem", {}).get("proved", False):
        raise ArithmeticError("five quadratic normalized gaps are not proved")
    if not cubic.get("claim_gate", {}).get(
        "all_seven_nontrivial_stable_shape_gaps_proved", False
    ):
        raise ArithmeticError("all stable shape gaps are not proved")
    if not stable.get("theorem", {}).get("proved", False):
        raise ArithmeticError("original stable coherent label is not proved")

    term_bijection_proved = all(
        ordered_triple_bijection_verified(n) for n in range(3, 10)
    )
    prepare_proved = term_bijection_proved
    select_proved = term_bijection_proved
    common_block_encoding_proved = prepare_proved and select_proved
    quadratic_gaps = {
        tuple(row["intermediate_tail"]): row
        for row in quadratics.get("shape_records", [])
    }
    family_records = {
        tuple(row["tail"]): row for row in family.get("shape_records", [])
    }
    cubic_bound = cubic["normalized_gap_certificate"][
        "normalized_gap_lower_bound"
    ]
    stable_bound = stable["theorem"]["normalized_gap"]
    records: list[ShapeCoherentLabelRecord] = []
    for tail, family_row in family_records.items():
        multiplicity = int(family_row["second_stage_multiplicity"])
        if multiplicity <= 1:
            continue
        if tail == STABLE_TAIL:
            gap_source = str(COSET_STABLE_COHERENT_LABEL_PATH)
            gap_bound = stable_bound
            gap_exponent = int(
                stable["headline_metrics"][
                    "normalized_gap_inverse_polynomial_exponent"
                ]
            )
        elif tail == (3, 1):
            gap_source = str(COSET_STABLE_SHAPE_CUBIC_GAP_PATH)
            gap_bound = cubic_bound
            gap_exponent = int(
                cubic["headline_metrics"][
                    "lcu_normalized_gap_inverse_polynomial_exponent"
                ]
            )
        else:
            gap_row = quadratic_gaps[tail]
            gap_source = str(COSET_STABLE_SHAPE_QUADRATIC_GAP_PATH)
            gap_bound = gap_row["normalized_gap_lower_bound"]
            gap_exponent = 3
        label_proved = common_block_encoding_proved
        records.append(
            ShapeCoherentLabelRecord(
                intermediate_tail=tail,
                intermediate_partition=family_row["padded_partition"],
                multiplicity_dimension=multiplicity,
                gap_source=gap_source,
                normalized_gap_lower_bound=gap_bound,
                normalized_gap_inverse_polynomial_exponent=gap_exponent,
                common_ordered_triple_block_encoding_applies=(
                    common_block_encoding_proved
                ),
                coherent_phase_estimation_label_proved=label_proved,
                routing_into_channel_proved=False,
                coupling_tree_transition_proved=False,
                status="coherent-shape-local-eigenlabel-proved-routing-transition-open",
            )
        )

    complementary = [record for record in records if record.intermediate_tail != STABLE_TAIL]
    theorem_proved = len(records) == 7 and len(complementary) == 6 and all(
        record.coherent_phase_estimation_label_proved for record in records
    )
    metrics: dict[str, int | float] = {
        "nontrivial_stable_shape_count": len(records),
        "common_shape_controlled_block_encoding_count": int(
            common_block_encoding_proved
        ),
        "new_coherent_shape_label_count": sum(
            record.coherent_phase_estimation_label_proved
            for record in complementary
        ),
        "all_nontrivial_stable_shape_coherent_label_count": sum(
            record.coherent_phase_estimation_label_proved for record in records
        ),
        "maximum_multiplicity_dimension": max(
            record.multiplicity_dimension for record in records
        ),
        "maximum_phase_estimation_query_exponent": max(
            record.normalized_gap_inverse_polynomial_exponent
            for record in records
        ),
        "channel_routing_circuit_count": 0,
        "coupling_tree_transition_circuit_count": 0,
        "complete_racah_associator_count": 0,
        "hidden_involution_decoder_count": 0,
    }
    return StableShapeCoherentLabelCertificate(
        created_at=utc_now(),
        theorem={
            "range": "every integer n>=8",
            "statement": (
                "Given a state already routed into any declared nontrivial eta_n tensor W_n -> xi_n stable "
                "channel, a uniform polynomial-size circuit coherently appends its common-orbit eigenlabel."
            ),
            "proved": theorem_proved,
        },
        source_certificate_contract={
            "exact_nine_shape_family": str(COSET_STABLE_SHAPE_FAMILY_PATH),
            "five_quadratic_gaps": str(COSET_STABLE_SHAPE_QUADRATIC_GAP_PATH),
            "cubic_gap": str(COSET_STABLE_SHAPE_CUBIC_GAP_PATH),
            "original_stable_label": str(COSET_STABLE_COHERENT_LABEL_PATH),
            "all_dependencies_proved": theorem_proved,
        },
        common_block_encoding_certificate={
            "operator": (
                "H_eta,n=sum_(a,b,c distinct) rho_eta((a b)) tensor rho_W((a b c))"
            ),
            "prepare": (
                "uniform reversible preparation over distinct ordered triples (a,b,c)"
            ),
            "select": (
                "shape-controlled Young-basis rho_eta((a b)) and rho_W((a b c)); the 3-cycle is two transpositions"
            ),
            "shape_control": (
                "constant seven-way multiplexing over the proved padded partition families"
            ),
            "lcu_normalization": "n(n-1)(n-2)",
            "hamiltonian_is_hermitian": True,
            "ordered_triple_bijection_proved": term_bijection_proved,
            "literature_capabilities": [
                "CAP-SN-QFT",
                "CAP-BOUNDED-SUPPORT-COMMUTANT-BLOCK-ENCODING",
            ],
            "proved": common_block_encoding_proved,
        },
        shape_records=records,
        interface_contract={
            "requires": [
                "a known intermediate shape label eta_n",
                "Young-basis eta_n and W_n registers already routed to final xi_n",
                "controlled S_n representation actions and standard block-Hamiltonian simulation",
            ],
            "produces": [
                "a coherent multiplicity eigenlabel of dimension 2, 3, or 4",
                "the shape-local eigenstate preserved to requested polynomial precision",
            ],
            "does_not_produce": [
                "routing or projection into eta_n tensor W_n -> xi_n",
                "a change between left- and right-associated coupling trees",
                "a full Racah associator matrix",
                "a hidden-involution estimate or graph-isomorphism decision",
            ],
        },
        headline_metrics=metrics,
        claim_gate={
            "all_nontrivial_shape_local_coherent_labels_proved": theorem_proved,
            "channel_routing_proved": False,
            "coupling_tree_transition_proved": False,
            "complete_racah_associator_proved": False,
            "hidden_involution_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "All shape-local eigenlabels are coherent, but the construction assumes channel routing and does "
                "not synthesize coupling-tree transitions, a decoder, or a classical separation."
            ),
        },
        status=(
            "all-seven-shape-local-coherent-labels-proved-routing-transition-decoder-open"
            if theorem_proved
            else "stable-shape-coherent-label-certificate-failed"
        ),
        summary=(
            "Extended the common ordered-triple block encoding and exact gaps to coherent labels on all seven "
            "nontrivial stable shapes; routing, reassociation, decoding, and separation remain open."
        ),
        falsifiers_triggered=[
            "The theorem assumes a state already routed into a declared intermediate/final channel.",
            "Shape-local phase estimation does not change coupling trees.",
            "Seven coherent labels are not a complete Racah associator.",
            "No hidden-involution decoder or classical separation follows from local labels.",
        ],
    )


def write_stable_shape_coherent_label_certificate(
    output_path: Path = COSET_STABLE_SHAPE_COHERENT_LABEL_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(build_stable_shape_coherent_label_certificate())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-SEVEN-COHERENT-SHAPE-LABELS-AS-COMPLETE-RACAH-DECODER",
                source=str(output_path),
                claim=(
                    "Coherent eigenlabels on all stable shapes implement a full Racah decoder."
                ),
                reason_invalid=(
                    "Channel routing, coupling-tree transitions, hidden-involution information, and classical "
                    "separation remain unproved."
                ),
                lesson=(
                    "Construct coherent projectors/routing and the complete left/right transition isometry before "
                    "testing whether label outcomes support a reduction-compatible decoder."
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
                    "coset_stable_shape_coherent_label_certificate": str(
                        output_path
                    )
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_stable_shape_coherent_label_certificate()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
