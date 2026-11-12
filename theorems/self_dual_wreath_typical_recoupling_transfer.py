"""Capability transfer audit for typical physical wreath recoupling.

The repository already contains a literature-backed symmetric-group
recoupling capability ledger and a large finite typical-irrep program. This
module maps those capabilities onto the physical four-class wreath-frame
contract. It prevents solved label transforms and block encodings from being
counted as the missing internal recoupling or decoder.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable

from coset_recoupling_capability_ledger import (
    build_recoupling_capability_report,
)
from coset_typical_invariant_contraction import (
    build_invariant_contraction_report,
)
from coset_typical_parity_class_contraction import (
    build_parity_class_contraction_report,
)
from coset_typical_parity_complete_separator import (
    build_parity_complete_separator_report,
)
from coset_typical_source_coverage import (
    build_typical_source_coverage_report,
)
from coset_typical_uniform_source_probe import (
    build_uniform_source_probe_report,
)

from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from self_dual_wreath_equal_commutator_audit import (
    run_self_dual_wreath_equal_commutator_audit,
)
from self_dual_wreath_stable_commutator_rank import (
    run_self_dual_wreath_stable_commutator_rank,
)
from self_dual_wreath_typical_partition_portfolio import (
    run_self_dual_wreath_typical_partition_portfolio,
)


SELF_DUAL_WREATH_TYPICAL_RECOUPLING_TRANSFER_PATH = Path(
    "research/representation/"
    "self_dual_wreath_typical_recoupling_transfer.json"
)
RECOUPLING_CAPABILITY_PATH = Path(
    "research/representation/coset_recoupling_capability_ledger.json"
)
TYPICAL_SOURCE_COVERAGE_PATH = Path(
    "research/representation/coset_typical_source_coverage.json"
)
UNIFORM_SOURCE_PROBE_PATH = Path(
    "research/representation/coset_typical_uniform_source_probe.json"
)
PARITY_COMPLETE_SEPARATOR_PATH = Path(
    "research/representation/coset_typical_parity_complete_separator.json"
)
PARITY_CLASS_CONTRACTION_PATH = Path(
    "research/representation/"
    "coset_typical_parity_class_contraction.json"
)
TYPICAL_INVARIANT_CONTRACTION_PATH = Path(
    "research/representation/coset_typical_invariant_contraction.json"
)
WREATH_COMMUTATOR_AUDIT_PATH = Path(
    "research/representation/self_dual_wreath_equal_commutator_audit.json"
)
WREATH_STABLE_RANK_PATH = Path(
    "research/representation/self_dual_wreath_stable_commutator_rank.json"
)
WREATH_TYPICAL_PORTFOLIO_PATH = Path(
    "research/representation/"
    "self_dual_wreath_typical_partition_portfolio.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-TYPICAL-RECOUPLING-TRANSFER"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class CapabilityTransferRecord:
    id: str
    required_primitive: str
    source_artifact: str
    source_metric: str
    source_count: int
    transfer_status: str
    valid_scope: str
    missing_scope: str
    blocks_decoder: bool


@dataclass(frozen=True)
class SelfDualWreathTypicalRecouplingTransferReport:
    created_at: str
    physical_recoupling_contract: dict[str, Any]
    capability_records: list[CapabilityTransferRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _read_json(
    path: Path,
    builder: Callable[[], Any],
) -> dict[str, Any]:
    if not path.exists():
        built = builder()
        payload = asdict(built)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    else:
        payload = json.loads(path.read_text())
    if not isinstance(payload, dict):
        raise ValueError(f"required artifact is not an object: {path}")
    return payload


def _metric(payload: dict[str, Any], name: str) -> int:
    return int(payload.get("headline_metrics", {}).get(name, 0) or 0)


def run_self_dual_wreath_typical_recoupling_transfer() -> (
    SelfDualWreathTypicalRecouplingTransferReport
):
    capability = _read_json(
        RECOUPLING_CAPABILITY_PATH,
        build_recoupling_capability_report,
    )
    source_coverage = _read_json(
        TYPICAL_SOURCE_COVERAGE_PATH,
        build_typical_source_coverage_report,
    )
    uniform_probe = _read_json(
        UNIFORM_SOURCE_PROBE_PATH,
        build_uniform_source_probe_report,
    )
    parity_complete = _read_json(
        PARITY_COMPLETE_SEPARATOR_PATH,
        build_parity_complete_separator_report,
    )
    parity_holdout = _read_json(
        PARITY_CLASS_CONTRACTION_PATH,
        build_parity_class_contraction_report,
    )
    invariant = _read_json(
        TYPICAL_INVARIANT_CONTRACTION_PATH,
        build_invariant_contraction_report,
    )
    commutator = _read_json(
        WREATH_COMMUTATOR_AUDIT_PATH,
        run_self_dual_wreath_equal_commutator_audit,
    )
    stable = _read_json(
        WREATH_STABLE_RANK_PATH,
        run_self_dual_wreath_stable_commutator_rank,
    )
    portfolio = _read_json(
        WREATH_TYPICAL_PORTFOLIO_PATH,
        run_self_dual_wreath_typical_partition_portfolio,
    )
    records = [
        CapabilityTransferRecord(
            id="TRANSFER-SN-QFT",
            required_primitive="Coherent S_n Fourier/Young labels",
            source_artifact=str(RECOUPLING_CAPABILITY_PATH),
            source_metric="proved_polynomial_primitive_count",
            source_count=_metric(
                capability, "proved_polynomial_primitive_count"
            ),
            transfer_status="available-label-transform-only",
            valid_scope=(
                "Permutation-basis to Young/Fourier labels and matrix indices."
            ),
            missing_scope=(
                "Does not decompose internal V_lambda tensor V_mu "
                "multiplicity spaces or mixed four-class kernels."
            ),
            blocks_decoder=False,
        ),
        CapabilityTransferRecord(
            id="TRANSFER-DIAGONAL-YJM-LABELS",
            required_primitive="Target tableau/Gelfand-Tsetlin labels",
            source_artifact=str(RECOUPLING_CAPABILITY_PATH),
            source_metric="diagonal_jm_label_transform_poly_proof_count",
            source_count=_metric(
                capability,
                "diagonal_jm_label_transform_poly_proof_count",
            ),
            transfer_status="available-target-label-only",
            valid_scope=(
                "Coherently appends target tableau labels at integer spectral gap."
            ),
            missing_scope=(
                "Acts as identity on Kronecker multiplicity registers."
            ),
            blocks_decoder=False,
        ),
        CapabilityTransferRecord(
            id="TRANSFER-BOUNDED-SUPPORT-BLOCK-ENCODING",
            required_primitive="Sparse commutant operator access",
            source_artifact=str(RECOUPLING_CAPABILITY_PATH),
            source_metric=(
                "bounded_support_commutant_block_encoding_poly_proof_count"
            ),
            source_count=_metric(
                capability,
                "bounded_support_commutant_block_encoding_poly_proof_count",
            ),
            transfer_status="available-operator-access-only",
            valid_scope=(
                "Polynomial LCU access to declared bounded-support orbit sums."
            ),
            missing_scope=(
                "No uniform typical-sector gap, eigenbasis, associator, or "
                "four-class contraction."
            ),
            blocks_decoder=False,
        ),
        CapabilityTransferRecord(
            id="TRANSFER-INTERNAL-KRONECKER-BASIS",
            required_primitive=(
                "Arbitrary-source internal Kronecker multiplicity transform"
            ),
            source_artifact=str(RECOUPLING_CAPABILITY_PATH),
            source_metric="internal_kronecker_transform_poly_proof_count",
            source_count=_metric(
                capability,
                "internal_kronecker_transform_poly_proof_count",
            ),
            transfer_status="missing-critical",
            valid_scope="No general primitive is proved.",
            missing_scope=(
                "Uniform basis inside every typical g(lambda,mu,nu) "
                "multiplicity register."
            ),
            blocks_decoder=True,
        ),
        CapabilityTransferRecord(
            id="TRANSFER-KCOPY-ASSOCIATOR",
            required_primitive="Overlapping k-copy Racah/associator transform",
            source_artifact=str(RECOUPLING_CAPABILITY_PATH),
            source_metric="kcopy_associator_poly_proof_count",
            source_count=_metric(
                capability, "kcopy_associator_poly_proof_count"
            ),
            transfer_status="missing-critical",
            valid_scope="No uniform overlapping associator is proved.",
            missing_scope=(
                "Consistent coupling-tree changes across "
                "k=Theta(log n!) physical copies."
            ),
            blocks_decoder=True,
        ),
        CapabilityTransferRecord(
            id="TRANSFER-UNIFORM-TYPICAL-SEPARATOR",
            required_primitive=(
                "Uniform typical multiplicity separator"
            ),
            source_artifact=str(PARITY_COMPLETE_SEPARATOR_PATH),
            source_metric="all_n_square_free_theorem_count",
            source_count=_metric(
                parity_holdout, "all_n_square_free_theorem_count"
            ),
            transfer_status="missing-n8-holdout-falsified",
            valid_scope=(
                "The partition-independent TC2+CT1-2CT2 rule repairs the two "
                "known exact scalar blocks and is collision-free numerically "
                "on all 663 audited blocks through n=7."
            ),
            missing_scope=(
                "Exact class contraction finds 10 scalar n=8 holdout blocks; "
                "no all-n rule, gap, or coherent internal eigenbasis exists."
            ),
            blocks_decoder=True,
        ),
        CapabilityTransferRecord(
            id="TRANSFER-MIXED-FOUR-CLASS-KERNEL",
            required_primitive=(
                "Mixed (r,q,r^-1q,[r,q]) recoupling contraction"
            ),
            source_artifact=str(WREATH_COMMUTATOR_AUDIT_PATH),
            source_metric="mixed_class_commutator_contraction_count",
            source_count=_metric(
                commutator, "mixed_class_commutator_contraction_count"
            ),
            transfer_status="missing-critical",
            valid_scope=(
                "Pure commutator products and finite factorial kernels exist."
            ),
            missing_scope=(
                "Polynomial contracted action on arbitrary typical "
                "physical character portfolios."
            ),
            blocks_decoder=True,
        ),
        CapabilityTransferRecord(
            id="TRANSFER-TYPICAL-SUPPORT-GAP",
            required_primitive=(
                "Uniform typical-sector support conditioning"
            ),
            source_artifact=str(TYPICAL_INVARIANT_CONTRACTION_PATH),
            source_metric="all_n_simple_spectrum_theorem_count",
            source_count=_metric(
                invariant, "all_n_simple_spectrum_theorem_count"
            ),
            transfer_status="missing-finite-numerical-only",
            valid_scope=(
                "Finite numerical typical multiplicity blocks and exact "
                "low-order traces."
            ),
            missing_scope=(
                "All-n minimum positive frame eigenvalue and error budget."
            ),
            blocks_decoder=True,
        ),
        CapabilityTransferRecord(
            id="TRANSFER-NATURAL-TYPICAL-COVERAGE",
            required_primitive="Nonvanishing natural source-label coverage",
            source_artifact=str(WREATH_TYPICAL_PORTFOLIO_PATH),
            source_metric=(
                "constant_mass_polynomial_catalog_no_go_theorem_count"
            ),
            source_count=_metric(
                portfolio,
                "constant_mass_polynomial_catalog_no_go_theorem_count",
            ),
            transfer_status="requires-uniform-rule-not-catalog",
            valid_scope=(
                "Constant-mass portfolios and catalog no-go are quantified."
            ),
            missing_scope=(
                "One uniform partition-description rule; stable branches "
                "have typical coverage count "
                f"{_metric(stable, 'typical_sector_coverage_count')}."
            ),
            blocks_decoder=True,
        ),
        CapabilityTransferRecord(
            id="TRANSFER-HIDDEN-PERMUTATION-DECODER",
            required_primitive="End-to-end hidden permutation decoder",
            source_artifact=str(RECOUPLING_CAPABILITY_PATH),
            source_metric="hidden_involution_decoder_count",
            source_count=_metric(
                capability, "hidden_involution_decoder_count"
            ),
            transfer_status="missing-critical",
            valid_scope="No decoder transfer is available.",
            missing_scope=(
                "Outcome law, coherent processing, and recovery of the "
                "hidden bridge permutation."
            ),
            blocks_decoder=True,
        ),
    ]
    valid_partial = sum(
        record.source_count > 0
        and record.transfer_status.startswith("available-")
        for record in records
    )
    blockers = sum(
        record.blocks_decoder and record.source_count == 0
        for record in records
    )
    exact_collisions = _metric(
        uniform_probe, "exact_scalar_collision_count"
    )
    collision_mass = float(
        uniform_probe.get("headline_metrics", {}).get(
            "maximum_natural_source_pair_mass_with_exact_scalar_collision",
            0,
        )
        or 0
    )
    metrics: dict[str, int | float] = {
        "capability_transfer_record_count": len(records),
        "valid_partial_primitive_transfer_count": valid_partial,
        "decoder_blocking_missing_primitive_count": blockers,
        "internal_kronecker_transform_count": _metric(
            capability, "internal_kronecker_transform_poly_proof_count"
        ),
        "kcopy_associator_count": _metric(
            capability, "kcopy_associator_poly_proof_count"
        ),
        "mixed_four_class_contraction_count": _metric(
            commutator, "mixed_class_commutator_contraction_count"
        ),
        "uniform_typical_separator_rule_count": _metric(
            parity_holdout, "all_n_square_free_theorem_count"
        ),
        "parity_complete_finite_block_count": _metric(
            parity_complete, "all_source_nontrivial_block_count"
        ),
        "parity_complete_finite_collision_count": _metric(
            parity_complete, "best_candidate_collision_count"
        ),
        "parity_complete_all_n_theorem_count": _metric(
            parity_holdout, "all_n_square_free_theorem_count"
        ),
        "parity_complete_n8_exact_scalar_obstruction_count": _metric(
            parity_holdout, "exact_scalar_obstruction_count"
        ),
        "uniform_typical_gap_theorem_count": _metric(
            source_coverage,
            "uniform_arbitrary_source_partition_gap_theorem_count",
        ),
        "fixed_separator_exact_collision_count": exact_collisions,
        "maximum_exact_collision_natural_source_pair_mass": collision_mass,
        "constant_mass_catalog_no_go_theorem_count": _metric(
            portfolio,
            "constant_mass_polynomial_catalog_no_go_theorem_count",
        ),
        "typical_hidden_permutation_decoder_count": 0,
        "new_end_to_end_quantum_algorithm_count": 0,
    }
    return SelfDualWreathTypicalRecouplingTransferReport(
        created_at=utc_now(),
        physical_recoupling_contract={
            "input": (
                "k=Theta(log n!) naturally sampled physical wreath irrep "
                "labels with Plancherel-typical source partitions"
            ),
            "required_transform": (
                "partition-description-uniform internal Kronecker and "
                "overlapping associator network"
            ),
            "required_operator": (
                "mixed four-class recoupling contraction or equivalent "
                "coherent frame block encoding"
            ),
            "required_spectral_theorem": (
                "uniform support projector and inverse-polynomial positive gap"
            ),
            "required_output": (
                "coherent measurement outcome law and polynomial hidden "
                "permutation decoder"
            ),
        },
        capability_records=records,
        headline_metrics=metrics,
        claim_gate={
            "known_label_and_operator_primitives_transferred": valid_partial >= 3,
            "finite_uniform_separator_candidate_available": (
                _metric(
                    parity_holdout, "exact_scalar_obstruction_count"
                )
                == 0
            ),
            "internal_kronecker_basis_transform_available": False,
            "overlapping_kcopy_associator_available": False,
            "mixed_four_class_contraction_available": False,
            "uniform_typical_support_gap_proved": False,
            "hidden_permutation_decoder_proved": False,
            "new_end_to_end_quantum_algorithm_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Known QFT, YJM-label, and block-encoding primitives transfer "
                "only partially. Every capability that touches typical "
                "multiplicity recoupling, conditioning, or decoding remains "
                "missing. The parity-complete discovery-set separator is "
                "falsified by 10 exact scalar blocks at n=8."
            ),
        },
        status=(
            "known-primitives-scope-separated-"
            "parity-holdout-falsified-growing-width-stack-missing"
        ),
        summary=(
            f"Transferred {valid_partial} valid partial primitives and "
            f"identified {blockers} decoder-blocking missing capabilities. "
            f"The old fixed separator has {exact_collisions} exact collision "
            "blocks, and the parity-complete replacement has "
            f"{_metric(parity_holdout, 'exact_scalar_obstruction_count')} "
            "exact n=8 holdout obstructions; no end-to-end algorithm is "
            "present."
        ),
        falsifiers_triggered=[
            "An efficient S_n QFT does not resolve internal Kronecker multiplicity spaces.",
            "YJM target-tableau labels are identity on multiplicity registers.",
            "Block encoding a bounded-support separator does not prove a typical-sector spectral gap.",
            "The old one-sided typical separator has exact scalar collisions on nonzero natural source-pair mass.",
            "Parity completion repairs the discovery-set collisions but has 10 exact scalar obstructions on the n=8 holdout.",
            "Stable-sector transforms and explicit typical catalogs do not provide constant-mass uniform coverage.",
            "No overlapping associator, mixed four-class contraction, support theorem, or hidden-permutation decoder exists.",
        ],
    )


def write_self_dual_wreath_typical_recoupling_transfer(
    path: Path = SELF_DUAL_WREATH_TYPICAL_RECOUPLING_TRANSFER_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, Any]:
    payload = asdict(run_self_dual_wreath_typical_recoupling_transfer())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id=(
                    "NEG-CODE-SELF-DUAL-WREATH-KNOWN-PRIMITIVES-"
                    "NOT-TYPICAL-RECOUPLING"
                ),
                source=str(path),
                claim=(
                    "Known S_n QFT, YJM-label, and block-encoding primitives "
                    "already supply the typical physical wreath decoder."
                ),
                reason_invalid=(
                    "They leave internal multiplicity bases, overlapping "
                    "associators, mixed four-class contraction, support "
                    "conditioning, and output decoding unresolved."
                ),
                lesson=(
                    "Synthesize the first missing typed recoupling primitive "
                    "rather than relabeling known transforms."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=payload["headline_metrics"],
            )
        )
        upsert_experiment_result(
            ExperimentResultRecord(
                id=(
                    registry_result_id
                    or f"RESULT-{registry_experiment_id}-LATEST"
                ),
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=payload["created_at"],
                status=payload["status"],
                summary=payload["summary"],
                metrics=payload["headline_metrics"],
                falsifiers_triggered=payload["falsifiers_triggered"],
                artifacts={
                    "self_dual_wreath_typical_recoupling_transfer": str(path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_self_dual_wreath_typical_recoupling_transfer()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
