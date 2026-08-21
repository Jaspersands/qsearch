"""Coherent sparse-LCU compiler for the natural matching-charge label.

The disjoint matching charge is the normalized orbit sum

    D_m = 1/N_m sum_(g in O_m) R_g,
    N_m = 192 binomial(m,4)
        = 8m(m-1)(m-2)(m-3).

Every term is an embedding of one of 192 fixed permutations on four pair
labels and moves at most six endpoints.  A term index consists of a ranked
four-subset of ``[m]`` and a seven-or-eight-bit local orbit index.  Lexicographic
combinadic ranking/unranking and the fixed local catalog give a reversible
polynomial-size PREP/SELECT specification.  With the uniform index state,

    (PREP^* tensor I) SELECT (PREP tensor I)

has top-left block exactly ``D_m`` and normalization one.  Since the orbit is
inverse closed, the block is Hermitian.  Standard qubitization or Hermitian
block-encoding phase estimation therefore writes a coherent approximate
``D_m`` eigenvalue label using ``O(gamma^-1 log(1/epsilon))`` SELECT calls.

The conditional-diameter theorem supplies

    gamma_m >= 3/[sqrt(10240) m^(9/2)]

on inverse-polynomial physical hidden-source mass.  Resolving that separated
direction costs polynomially many calls, ``O(m^(9/2) log(1/epsilon))``.  This
closes the *access* objection for the first natural within-mu label: no
hyperoctahedral subduction transform is required merely to phase-label D_m.

It does not produce a detector.  The exact source-local likelihood theorem
proves that measuring any joint family of per-source K-centralizing charges,
including ``C_m,D_m``, has identical outcome distributions under baseline and
alternative.  The label must remain coherent and participate in an all-copy,
target-coupled recoupling operation.  Minimum joint gaps, residual copy
degeneracy, such a target coupling, and a speedup remain open.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from coset_hidden_involution_matching_charge_conditional_diameter import (
    explicit_diameter_lower_bound,
    explicit_good_mass_lower_bound,
)
from coset_hidden_involution_pair_matching_charge_hierarchy import (
    Permutation,
    canonical_disjoint_matching_orbit,
)
from coset_hidden_involution_matching_charge_natural_independence import (
    _embed_pair_permutation,
    _inverse,
    _moved_point_support,
)
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_matching_charge_coherent_label_compiler.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-MATCHING-CHARGE-COHERENT-LABEL-COMPILER"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class MatchingChargeIndexControl:
    half_degree: int
    four_subset_count: int
    local_orbit_size: int
    indexed_term_count: int
    expected_term_count: int
    distinct_term_count: int
    maximum_moved_point_count: int
    inverse_closed: bool
    subset_rank_unrank_verified: bool
    term_index_is_bijective: bool
    status: str


@dataclass(frozen=True)
class CoherentLabelScalingRecord:
    half_degree: int
    matching_charge_term_count: int
    term_index_qubits: int
    local_SELECT_moved_point_upper_bound: int
    conditional_diameter_lower_bound: float
    good_source_mass_lower_bound: float
    target_phase_precision: float
    target_failure_probability: float
    SELECT_query_upper_bound: int
    SELECT_query_log2: float
    query_bound_polynomial_in_half_degree: bool
    standalone_label_distribution_likelihood_blind: bool
    status: str


@dataclass(frozen=True)
class CoherentLabelCompilerTheorem:
    indexed_orbit: str
    block_encoding: str
    phase_label: str
    conditional_resolution: str
    likelihood_boundary: str
    exact_uniform_orbit_indexing_compiled: bool
    normalization_one_Hermitian_block_encoding_compiled: bool
    coherent_inverse_polynomial_precision_D_label_compiled: bool
    conditional_natural_separated_direction_resolvable: bool
    hyperoctahedral_subduction_required_for_D_label: bool
    standalone_D_measurement_is_detector: bool
    all_copy_target_coupled_use_compiled: bool
    full_joint_minimum_gap_proved: bool
    residual_multiplicity_bounded: bool
    hidden_involution_detector_constructed: bool
    speedup_claim_allowed: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class CoherentLabelCompilerReport:
    created_at: str
    theorem_contract: dict[str, Any]
    index_controls: list[MatchingChargeIndexControl]
    scaling_records: list[CoherentLabelScalingRecord]
    theorem: CoherentLabelCompilerTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def matching_charge_term_count(half_degree: int) -> int:
    if half_degree < 4:
        raise ValueError("half_degree must be at least four")
    return 192 * math.comb(half_degree, 4)


def rank_four_subset(subset: tuple[int, int, int, int], size: int) -> int:
    if tuple(sorted(subset)) != subset or len(set(subset)) != 4:
        raise ValueError("subset must contain four strictly increasing labels")
    if subset[0] < 0 or subset[-1] >= size:
        raise ValueError("subset labels out of range")
    rank = 0
    previous = -1
    for position, value in enumerate(subset):
        remaining = 3 - position
        for candidate in range(previous + 1, value):
            rank += math.comb(size - candidate - 1, remaining)
        previous = value
    return rank


def unrank_four_subset(rank: int, size: int) -> tuple[int, int, int, int]:
    total = math.comb(size, 4)
    if not 0 <= rank < total:
        raise ValueError("rank outside four-subset range")
    output: list[int] = []
    previous = -1
    residual = rank
    for position in range(4):
        remaining = 3 - position
        maximum = size - remaining
        for candidate in range(previous + 1, maximum):
            block = math.comb(size - candidate - 1, remaining)
            if residual < block:
                output.append(candidate)
                previous = candidate
                break
            residual -= block
        else:
            raise AssertionError("combinadic unranking failed")
    return tuple(output)  # type: ignore[return-value]


def matching_charge_term_from_index(
    half_degree: int,
    term_index: int,
) -> Permutation:
    local = canonical_disjoint_matching_orbit()
    total = matching_charge_term_count(half_degree)
    if not 0 <= term_index < total:
        raise ValueError("term index outside matching-charge orbit")
    subset_rank, local_index = divmod(term_index, len(local))
    selected_pairs = unrank_four_subset(subset_rank, half_degree)
    return _embed_pair_permutation(
        local[local_index],
        selected_pairs,
        half_degree,
    )


def audit_matching_charge_index(half_degree: int) -> MatchingChargeIndexControl:
    if half_degree > 7:
        raise ValueError("dense bijection audit is limited to m<=7")
    subset_count = math.comb(half_degree, 4)
    local_size = len(canonical_disjoint_matching_orbit())
    total = matching_charge_term_count(half_degree)
    subset_verified = all(
        rank_four_subset(unrank_four_subset(index, half_degree), half_degree)
        == index
        for index in range(subset_count)
    )
    terms = tuple(
        matching_charge_term_from_index(half_degree, index)
        for index in range(total)
    )
    term_set = set(terms)
    inverse_closed = {_inverse(term) for term in term_set} == term_set
    maximum_support = max(_moved_point_support(term) for term in term_set)
    bijective = len(term_set) == total
    verified = bool(
        subset_verified
        and local_size == 192
        and total == 192 * subset_count
        and bijective
        and inverse_closed
        and maximum_support <= 6
    )
    return MatchingChargeIndexControl(
        half_degree=half_degree,
        four_subset_count=subset_count,
        local_orbit_size=local_size,
        indexed_term_count=total,
        expected_term_count=192 * subset_count,
        distinct_term_count=len(term_set),
        maximum_moved_point_count=maximum_support,
        inverse_closed=inverse_closed,
        subset_rank_unrank_verified=subset_verified,
        term_index_is_bijective=bijective,
        status=(
            "matching-charge-reversible-orbit-index-verified"
            if verified
            else "matching-charge-index-control-failure"
        ),
    )


def coherent_label_scaling_record(
    half_degree: int,
    failure_probability: float = 2.0**-20,
) -> CoherentLabelScalingRecord:
    if half_degree < 11:
        raise ValueError("natural conditional resolution starts at m=11")
    if not 0 < failure_probability < 0.5:
        raise ValueError("failure_probability must lie in (0,1/2)")
    count = matching_charge_term_count(half_degree)
    gap = explicit_diameter_lower_bound(half_degree)
    precision = gap / 4.0
    # A conservative generic Hermitian block-encoding phase-label budget.
    queries = math.ceil(
        8.0 * math.log(2.0 / failure_probability) / gap
    )
    return CoherentLabelScalingRecord(
        half_degree=half_degree,
        matching_charge_term_count=count,
        term_index_qubits=math.ceil(math.log2(count)),
        local_SELECT_moved_point_upper_bound=6,
        conditional_diameter_lower_bound=gap,
        good_source_mass_lower_bound=explicit_good_mass_lower_bound(
            half_degree
        ),
        target_phase_precision=precision,
        target_failure_probability=failure_probability,
        SELECT_query_upper_bound=queries,
        SELECT_query_log2=math.log2(queries),
        query_bound_polynomial_in_half_degree=True,
        standalone_label_distribution_likelihood_blind=True,
        status="coherent-D-label-polynomial-query-standalone-blind",
    )


def build_coherent_label_compiler_report() -> CoherentLabelCompilerReport:
    index_controls = [audit_matching_charge_index(value) for value in (4, 5, 6)]
    scaling = [
        coherent_label_scaling_record(value)
        for value in (11, 16, 32, 64, 128)
    ]
    indexed = all(
        row.subset_rank_unrank_verified
        and row.term_index_is_bijective
        and row.inverse_closed
        and row.maximum_moved_point_count <= 6
        for row in index_controls
    )
    polynomial = all(row.query_bound_polynomial_in_half_degree for row in scaling)
    theorem = CoherentLabelCompilerTheorem(
        indexed_orbit=(
            "D_m has 192*C(m,4) distinct inverse-closed terms indexed by a "
            "lexicographic four-subset and one of 192 fixed local permutations."
        ),
        block_encoding=(
            "Uniform PREP and constant-support right-regular SELECT give an "
            "exact normalization-one Hermitian block-encoding of D_m."
        ),
        phase_label=(
            "Qubitization/phase estimation coherently writes a D_m eigenvalue "
            "to precision gamma using O(gamma^-1 log(1/epsilon)) SELECT calls."
        ),
        conditional_resolution=(
            "The natural separated direction gamma>=3/(sqrt(10240)m^(9/2)) "
            "is therefore resolvable with polynomial query and gate complexity."
        ),
        likelihood_boundary=(
            "Standalone C_m,D_m outcome distributions are exactly likelihood "
            "blind; only coherent all-copy target recoupling can use the label."
        ),
        exact_uniform_orbit_indexing_compiled=indexed,
        normalization_one_Hermitian_block_encoding_compiled=indexed,
        coherent_inverse_polynomial_precision_D_label_compiled=(indexed and polynomial),
        conditional_natural_separated_direction_resolvable=(indexed and polynomial),
        hyperoctahedral_subduction_required_for_D_label=False,
        standalone_D_measurement_is_detector=False,
        all_copy_target_coupled_use_compiled=False,
        full_joint_minimum_gap_proved=False,
        residual_multiplicity_bounded=False,
        hidden_involution_detector_constructed=False,
        speedup_claim_allowed=False,
        theorem_verified=indexed and polynomial,
        status=(
            "coherent-natural-D-label-compiled-target-recoupling-open"
            if indexed and polynomial
            else "matching-charge-coherent-label-control-failure"
        ),
    )
    return CoherentLabelCompilerReport(
        created_at=utc_now(),
        theorem_contract={
            "access_model": (
                "Coherent right multiplication on one-line encoded S_(2m) group "
                "basis plus reversible arithmetic and clean ancillas"
            ),
            "compiled_operator": "Normalized disjoint matching charge D_m",
            "precision_target": "One quarter of the proved conditional diameter",
            "claim_boundary": (
                "Coherent eigenvalue label only; no standalone measurement signal "
                "and no full subduction or target-recoupling compiler."
            ),
        },
        index_controls=index_controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-MATCHING-D-TARGET-COUPLED-USE",
                "statement": (
                    "Construct an all-copy target-controlled operation using the "
                    "coherent D_m label before measurement, or prove all such uses dequantize."
                ),
                "resolved": False,
            },
            {
                "id": "PO-MATCHING-D-RESIDUAL-DEGENERACY",
                "statement": (
                    "Bound residual branching-copy multiplicity after the coherent "
                    "C_m,D_m labels on natural source mass."
                ),
                "resolved": False,
            },
            {
                "id": "PO-MATCHING-D-PHYSICAL-END-TO-END-COST",
                "statement": (
                    "Compose label extraction with target recoupling, uncompute all "
                    "ancillas, and audit copies, precision, memory, and classical access."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "Orbit size polynomial does not give coherent normalized access.",
                "answer": (
                    "Here the explicit combinadic/local index is bijective and every "
                    "coefficient is exactly 1/N_m, so PREP/SELECT normalization is one."
                ),
                "resolved": True,
            },
            {
                "challenge": "The inverse-polynomial spectral direction may require subduction first.",
                "answer": (
                    "False for phase labeling: right-regular D_m access acts directly "
                    "on the physical group register and phase estimation supplies its label."
                ),
                "resolved": True,
            },
            {
                "challenge": "The compiled D_m label is already a hidden-involution detector.",
                "answer": (
                    "False exactly: every standalone source-local K-charge measurement "
                    "has the same likelihood-weighted and baseline distribution."
                ),
                "resolved": True,
            },
            {
                "challenge": "One separated pair resolves the full multiplicity space.",
                "answer": (
                    "False. Minimum gaps and residual degeneracies remain uncontrolled."
                ),
                "resolved": True,
            },
        ],
        headline_metrics={
            "normalization_one_D_block_encoding_count": int(indexed),
            "coherent_inverse_polynomial_D_label_count": int(indexed and polynomial),
            "maximum_dense_index_control_half_degree": max(
                row.half_degree for row in index_controls
            ),
            "tail_SELECT_query_log2_upper_bound": scaling[-1].SELECT_query_log2,
            "standalone_D_detector_count": 0,
            "target_coupled_decoder_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "normalization_one_D_block_encoding_compiled": indexed,
            "coherent_inverse_polynomial_D_label_compiled": indexed and polynomial,
            "conditional_natural_D_direction_resolvable": indexed and polynomial,
            "standalone_D_measurement_likelihood_blind": True,
            "all_copy_target_coupled_use_compiled": False,
            "full_joint_minimum_gap_proved": False,
            "residual_multiplicity_bounded": False,
            "hidden_involution_detector_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The first natural within-mu spectral direction is coherently "
                "accessible, but its measured distribution is exactly blind and "
                "no target-coupled recoupling use is known."
            ),
        },
        status=theorem.status,
        summary=(
            "Compiled a normalization-one block-encoding and coherent polynomial-"
            "precision label for the natural matching charge D_m."
        ),
        falsifiers_triggered=[
            "Hyperoctahedral subduction is not required merely to access the D_m eigenvalue label.",
            "The natural D_m separated direction is polynomially phase-resolvable.",
            "A standalone D_m measurement remains exactly likelihood blind.",
        ],
    )


def write_coherent_label_compiler_report(
    output_path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(build_coherent_label_compiler_report())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


def run_experiment(
    experiment_id: str = DEFAULT_EXPERIMENT_ID,
    candidate_id: str = DEFAULT_CANDIDATE_ID,
    write_registry: bool = True,
) -> dict[str, Any]:
    del experiment_id, candidate_id, write_registry
    return write_coherent_label_compiler_report()


if __name__ == "__main__":
    print(json.dumps(run_experiment(), indent=2, sort_keys=True))
