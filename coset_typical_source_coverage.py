"""Natural-input coverage audit for the typical-irrep separator program.

Finite separator certificates currently fix one maximum-dimension source
partition at each ``n``.  That is useful for mechanism discovery but does not
by itself cover a natural weak-Fourier sample.  This module accounts for both
parts of the resulting postselection:

* the probability of observing the pre-certified source label on independent
  involution coset states;
* the dimension-weighted Kronecker coupling reference mass of target blocks
  whose internal multiplicity is either trivial or exactly certified by the
  current separator ladder.

The asymptotic source obstruction is literature-backed.  Aggarwal and Elboim
(arXiv:2605.25995) prove

    max_lambda dim(lambda)
      = sqrt(n!) exp(-(d + o(1)) sqrt(n)),  d > 0.

Consequently the largest Plancherel atom is stretched-exponentially small.
Since an involution weak-Fourier probability is at most twice its Plancherel
mass, any polynomial-size catalog of pre-certified source partitions has
superpolynomially small natural mass.  A viable route must therefore be
uniform and label-adaptive on sampled typical partitions.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path

from coset_typical_irrep_transfer_audit import _maximum_dimension_partition
from representation_obstruction import (
    conjugate_partition,
    hook_length_dimension,
    integer_partitions,
)
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from symmetric_character import kronecker_coefficient
from weak_fourier_signal import character_on_involution, involution_specs_for_n


REPORT_PATH = Path(
    "research/representation/coset_typical_source_coverage.json"
)
N8_REPORT_PATH = Path(
    "research/representation/coset_typical_high_multiplicity_transfer.json"
)
N9_REPORT_PATH = Path(
    "research/representation/coset_typical_n9_full_transfer.json"
)
N10_FEASIBILITY_PATH = Path(
    "research/representation/coset_typical_n10_feasibility.json"
)
N10_MODULAR_PATH = Path(
    "research/representation/coset_typical_modular_yjm_contraction.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-TYPICAL-SOURCE-COVERAGE"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
MAXIMAL_DIMENSION_PAPER_ID = "aggarwal-elboim-maximal-dimension-2026"
MAXIMAL_DIMENSION_PAPER_URL = "https://arxiv.org/abs/2605.25995"


@dataclass(frozen=True)
class TypicalSourceCoverageRecord:
    n: int
    involution_type: str
    transposition_count: int
    source_partition: tuple[int, ...]
    source_dimension: int
    exact_source_plancherel_mass: str
    source_plancherel_mass: float
    source_character: int
    exact_source_weak_fourier_probability: str
    source_weak_fourier_probability: float
    exact_two_copy_source_probability: str
    two_copy_source_probability: float
    exact_three_copy_source_probability: str
    three_copy_source_probability: float
    supported_target_count: int
    nontrivial_multiplicity_target_count: int
    automatically_resolved_target_count: int
    exactly_certified_nontrivial_target_count: int
    exact_certified_target_coupling_mass: str
    certified_target_coupling_mass: float
    exact_dimension_weighted_coverage_reference: str
    dimension_weighted_coverage_reference: float
    largest_unresolved_target_partition: tuple[int, ...] | None
    largest_unresolved_target_multiplicity: int
    largest_unresolved_target_coupling_mass: float
    finite_certificate_only: bool
    status: str


@dataclass(frozen=True)
class TypicalSourceCoverageReport:
    created_at: str
    literature_linked_theorem: dict[str, object]
    probability_contract: dict[str, object]
    certificate_contract: dict[str, object]
    records: list[TypicalSourceCoverageRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _read_json(path: Path) -> dict:
    resolved = path
    if not resolved.exists():
        resolved = Path(__file__).resolve().parent / path
    if not resolved.exists():
        raise FileNotFoundError(f"required certificate is missing: {path}")
    payload = json.loads(resolved.read_text())
    if not isinstance(payload, dict):
        raise ValueError(f"required certificate is not an object: {path}")
    return payload


def _square_free_targets(path: Path) -> set[tuple[int, ...]]:
    payload = _read_json(path)
    targets: set[tuple[int, ...]] = set()
    for record in payload.get("records", []):
        if record.get("characteristic_polynomial_square_free", False):
            targets.add(tuple(record["target_partition"]))
    return targets


def certified_nontrivial_targets(n: int) -> set[tuple[int, ...]]:
    """Return target blocks with exact simple-spectrum certificates."""

    if n == 8:
        targets = _square_free_targets(N8_REPORT_PATH)
    elif n == 9:
        targets = _square_free_targets(N9_REPORT_PATH)
    elif n == 10:
        targets = _square_free_targets(N10_FEASIBILITY_PATH)
        modular = _read_json(N10_MODULAR_PATH)
        direct = {
            tuple(record["target_partition"])
            for record in modular.get("n10_prime_certificates", [])
            if record.get(
                "rational_characteristic_polynomial_square_free_consequence",
                False,
            )
        }
        targets.update(direct)
        targets.update(conjugate_partition(target) for target in direct)
    else:
        raise ValueError("exact source-coverage audit is available only for n=8,9,10")
    return targets


def _target_coverage(
    source: tuple[int, ...],
    certified: set[tuple[int, ...]],
) -> dict[str, object]:
    source_dimension = hook_length_dimension(source)
    rows: list[tuple[Fraction, tuple[int, ...], int, bool]] = []
    automatic_count = 0
    certified_nontrivial_count = 0
    certified_mass = Fraction()
    nontrivial_count = 0
    for target in integer_partitions(sum(source)):
        multiplicity = kronecker_coefficient(source, source, target)
        if not multiplicity:
            continue
        target_dimension = hook_length_dimension(target)
        mass = Fraction(
            multiplicity * target_dimension,
            source_dimension**2,
        )
        automatic = multiplicity <= 1
        exact = automatic or target in certified
        if automatic:
            automatic_count += 1
        else:
            nontrivial_count += 1
            certified_nontrivial_count += int(target in certified)
        if exact:
            certified_mass += mass
        rows.append((mass, target, multiplicity, exact))
    if sum((row[0] for row in rows), Fraction()) != 1:
        raise ArithmeticError("Kronecker coupling masses do not sum to one")
    unresolved = sorted(
        (row for row in rows if not row[3]),
        key=lambda row: (-row[0], row[1]),
    )
    largest = unresolved[0] if unresolved else None
    return {
        "supported_target_count": len(rows),
        "nontrivial_count": nontrivial_count,
        "automatic_count": automatic_count,
        "certified_nontrivial_count": certified_nontrivial_count,
        "certified_mass": certified_mass,
        "largest_unresolved_target": largest[1] if largest else None,
        "largest_unresolved_multiplicity": largest[2] if largest else 0,
        "largest_unresolved_mass": float(largest[0]) if largest else 0.0,
    }


def audit_typical_source_coverage(
    n: int,
    transposition_count: int,
    involution_type: str,
) -> TypicalSourceCoverageRecord:
    source = _maximum_dimension_partition(n)
    source_dimension = hook_length_dimension(source)
    group_order = math.factorial(n)
    plancherel = Fraction(source_dimension**2, group_order)
    character = character_on_involution(source, transposition_count)
    weak_probability = Fraction(
        source_dimension * (source_dimension + character),
        group_order,
    )
    if weak_probability < 0 or weak_probability > 2 * plancherel:
        raise ArithmeticError("weak-Fourier probability violates character bound")
    two_copy_source = weak_probability**2
    three_copy_source = weak_probability**3
    target = _target_coverage(source, certified_nontrivial_targets(n))
    certified_mass = target["certified_mass"]
    if not isinstance(certified_mass, Fraction):
        raise TypeError("certified target mass must be exact")
    coverage_reference = two_copy_source * certified_mass
    complete_target_coverage = certified_mass == 1
    return TypicalSourceCoverageRecord(
        n=n,
        involution_type=involution_type,
        transposition_count=transposition_count,
        source_partition=source,
        source_dimension=source_dimension,
        exact_source_plancherel_mass=str(plancherel),
        source_plancherel_mass=float(plancherel),
        source_character=character,
        exact_source_weak_fourier_probability=str(weak_probability),
        source_weak_fourier_probability=float(weak_probability),
        exact_two_copy_source_probability=str(two_copy_source),
        two_copy_source_probability=float(two_copy_source),
        exact_three_copy_source_probability=str(three_copy_source),
        three_copy_source_probability=float(three_copy_source),
        supported_target_count=int(target["supported_target_count"]),
        nontrivial_multiplicity_target_count=int(target["nontrivial_count"]),
        automatically_resolved_target_count=int(target["automatic_count"]),
        exactly_certified_nontrivial_target_count=int(
            target["certified_nontrivial_count"]
        ),
        exact_certified_target_coupling_mass=str(certified_mass),
        certified_target_coupling_mass=float(certified_mass),
        exact_dimension_weighted_coverage_reference=str(coverage_reference),
        dimension_weighted_coverage_reference=float(coverage_reference),
        largest_unresolved_target_partition=target[
            "largest_unresolved_target"
        ],
        largest_unresolved_target_multiplicity=int(
            target["largest_unresolved_multiplicity"]
        ),
        largest_unresolved_target_coupling_mass=float(
            target["largest_unresolved_mass"]
        ),
        finite_certificate_only=True,
        status=(
            "fixed-source-all-target-finite-control-asymptotically-inaccessible"
            if complete_target_coverage
            else "fixed-source-partial-target-control-asymptotically-inaccessible"
        ),
    )


def build_typical_source_coverage_report(
    n_values: tuple[int, ...] = (8, 9, 10),
) -> TypicalSourceCoverageReport:
    records = [
        audit_typical_source_coverage(n, transpositions, label)
        for n in n_values
        for label, transpositions in involution_specs_for_n(n)
        if label != "single_transposition_control"
    ]
    n10_records = [record for record in records if record.n == 10]
    n10_reference = n10_records[0]
    metrics: dict[str, int | float] = {
        "source_coverage_record_count": len(records),
        "literature_linked_maximal_dimension_theorem_count": 1,
        "polynomial_precertified_source_catalog_no_go_theorem_count": 1,
        "uniform_arbitrary_source_partition_separator_count": 0,
        "uniform_arbitrary_source_partition_gap_theorem_count": 0,
        "uniform_arbitrary_source_partition_coherent_transform_count": 0,
        "n8_exact_target_coupling_mass": next(
            record.certified_target_coupling_mass
            for record in records
            if record.n == 8
        ),
        "n9_exact_target_coupling_mass": next(
            record.certified_target_coupling_mass
            for record in records
            if record.n == 9
        ),
        "n10_exactly_certified_nontrivial_target_count": (
            n10_reference.exactly_certified_nontrivial_target_count
        ),
        "n10_nontrivial_multiplicity_target_count": (
            n10_reference.nontrivial_multiplicity_target_count
        ),
        "n10_certified_target_coupling_mass": (
            n10_reference.certified_target_coupling_mass
        ),
        "n10_largest_unresolved_target_coupling_mass": (
            n10_reference.largest_unresolved_target_coupling_mass
        ),
        "maximum_finite_dimension_weighted_coverage_reference": max(
            record.dimension_weighted_coverage_reference for record in records
        ),
        "minimum_finite_dimension_weighted_coverage_reference": min(
            record.dimension_weighted_coverage_reference for record in records
        ),
        "same_hidden_involution_target_outcome_law_count": 0,
        "natural_input_inverse_polynomial_coverage_theorem_count": 0,
        "typical_label_hidden_involution_decoder_count": 0,
    }
    return TypicalSourceCoverageReport(
        created_at=utc_now(),
        literature_linked_theorem={
            "paper_id": MAXIMAL_DIMENSION_PAPER_ID,
            "title": (
                "On the maximal dimension of an irreducible representation "
                "of the symmetric group"
            ),
            "authors": ["Amol Aggarwal", "Dor Elboim"],
            "year": 2026,
            "url": MAXIMAL_DIMENSION_PAPER_URL,
            "source_theorem": (
                "d_n^max=sqrt(n!)*exp(-(d+o(1))*sqrt(n)) for a constant d>0"
            ),
            "derived_plancherel_consequence": (
                "max_lambda dim(lambda)^2/n!"
                "=exp(-(2d+o(1))*sqrt(n))"
            ),
            "weak_fourier_consequence": (
                "For every involution h, p_h(lambda)="
                "[dim(lambda)^2/n!]*(1+chi_lambda(h)/dim(lambda)) "
                "is at most twice the maximal Plancherel atom."
            ),
            "catalog_no_go": (
                "Any polynomial-size pre-certified source catalog has "
                "stretched-exponentially small weak-Fourier mass."
            ),
            "external_theorem_not_reproved_here": True,
        },
        probability_contract={
            "source_model": (
                "Independent natural involution coset states followed by weak "
                "Fourier label measurement."
            ),
            "target_model": (
                "Maximally mixed dimension-weighted diagonal decomposition of "
                "V_lambda tensor V_lambda, with reference mass "
                "g(lambda,lambda,nu)d_nu/d_lambda^2."
            ),
            "dimension_weighted_coverage_reference": (
                "p_h(lambda)^2 times the exactly resolved dimension-weighted "
                "target coupling mass."
            ),
            "not_a_target_outcome_probability": (
                "For two copies sharing hidden h, the conditional target law "
                "contains the correlated pair class operator "
                "E_h[rho_lambda(h) tensor rho_lambda(h)]. The dimension-"
                "weighted coupling mass is neither asserted as that law nor "
                "as an upper or lower bound."
            ),
            "interpretation_limit": (
                "The reference ranks structural certificate coverage only. A "
                "same-hidden-involution target outcome law, frame, decoder, "
                "and classical separation remain mandatory."
            ),
        },
        certificate_contract={
            "n8": str(N8_REPORT_PATH),
            "n9": str(N9_REPORT_PATH),
            "n10_low_multiplicity": str(N10_FEASIBILITY_PATH),
            "n10_modular_and_sign_dual": str(N10_MODULAR_PATH),
            "multiplicity_one_blocks": (
                "Counted as automatically resolved because no internal "
                "multiplicity basis is required."
            ),
            "numerical_only_targets_counted": 0,
        },
        records=records,
        headline_metrics=metrics,
        claim_gate={
            "fixed_maximum_dimension_source_is_naturally_accessible": False,
            "polynomial_precertified_source_catalog_is_naturally_accessible": (
                False
            ),
            "n8_and_n9_target_coverage_complete_for_fixed_source": True,
            "n10_target_coupling_coverage_complete": False,
            "uniform_label_adaptive_typical_source_resolver_proved": False,
            "natural_input_inverse_polynomial_coverage_proved": False,
            "same_hidden_involution_target_outcome_law_proved": False,
            "hidden_involution_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The current certificates are pinned to one source partition. "
                "A 2026 maximal-dimension theorem makes every polynomial "
                "pre-certified source catalog naturally negligible, and the "
            "n=10 low-multiplicity ladder also resolves only a small "
                "fraction of dimension-weighted target coupling mass."
            ),
        },
        status=(
            "fixed-source-typical-ladder-falsified-as-natural-input-route-"
            "uniform-label-adaptation-required"
        ),
        summary=(
            "Combined exact source probabilities and dimension-weighted target "
            "coverage with the 2026 maximal-irrep-dimension theorem. The fixed-source "
            f"n=10 ladder resolves {n10_reference.certified_target_coupling_mass:.3%} "
            "of dimension-weighted coupling mass, while any polynomial source "
            "catalog is asymptotically stretched-exponentially rare."
        ),
        falsifiers_triggered=[
            (
                "Choosing the maximum-dimension source does not make a fixed "
                "source label naturally accessible asymptotically."
            ),
            (
                "A polynomial catalog of finite source certificates cannot "
                "cover inverse-polynomial weak-Fourier mass."
            ),
            (
                "The current n=10 low-multiplicity ladder covers less than two "
                "percent of the fixed source's target coupling mass."
            ),
            (
                "The largest unresolved n=10 target is the source-shaped "
                "multiplicity-117 block and alone carries over fifteen percent "
                "of coupling mass."
            ),
            (
                "Finite simple spectra do not provide a natural-input decoder "
                "without uniform sampled-label adaptation."
            ),
        ],
    )


def write_typical_source_coverage_report(
    output_path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(build_typical_source_coverage_report())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-TYPICAL-FIXED-SOURCE-CATALOG-COVERAGE",
                source=str(output_path),
                claim=(
                    "A polynomial catalog of fixed-source typical-irrep "
                    "separator certificates has inverse-polynomial natural "
                    "weak-Fourier coverage."
                ),
                reason_invalid=(
                    "The maximal Plancherel atom is "
                    "exp(-Theta(sqrt(n))) by arXiv:2605.25995, and involution "
                    "weak-Fourier atoms are at most twice as large."
                ),
                lesson=(
                    "Stop extending one-source finite ladders as algorithmic "
                    "coverage. Require a uniform resolver whose circuit and "
                    "gap guarantees accept arbitrary sampled partitions."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
                evidence=payload["headline_metrics"],
            )
        )
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-TYPICAL-N10-LOW-MULTIPLICITY-TARGET-MASS",
                source=str(output_path),
                claim=(
                    "The exact n=10 low-multiplicity collision ladder covers "
                    "most dimension-weighted target mass for its fixed source."
                ),
                reason_invalid=(
                    "The 12 exactly certified nontrivial targets plus "
                    "multiplicity-one targets cover only "
                    f"{payload['headline_metrics']['n10_certified_target_coupling_mass']:.3%} "
                    "of exact Kronecker coupling mass."
                ),
                lesson=(
                    "Prioritize source-shaped and other high-mass growing-"
                    "multiplicity blocks, or derive a uniform structural "
                    "theorem that handles them collectively."
                ),
                applies_to=[registry_candidate_id, registry_experiment_id],
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
                created_at=payload["created_at"],
                status=payload["status"],
                summary=payload["summary"],
                metrics=payload["headline_metrics"],
                falsifiers_triggered=payload["falsifiers_triggered"],
                artifacts={"coset_typical_source_coverage": str(output_path)},
            )
        )
    return payload


if __name__ == "__main__":
    report = write_typical_source_coverage_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
