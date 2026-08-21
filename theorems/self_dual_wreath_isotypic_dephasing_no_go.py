"""Exact hidden-label identification no-go after isotypic dephasing.

Let a finite group ``G`` act as

    R(g) = direct_sum_nu rho_nu(g) tensor I_(M_nu)

and let ``rho_g=R(g)rho_eR(g)^*`` be a uniform covariant state ensemble.  If
the irrep label is measured or dephased, the seed becomes block diagonal.
Symmetrizing any decoder gives a covariant POVM without changing its average
success.  In sector ``nu``, its seed effect ``E_nu`` obeys

    Tr_(V_nu)(E_nu) = d_nu/|G| I_(M_nu).

For every positive operator ``X`` on ``C^d tensor M``,

    X <= d I_d tensor Tr_(C^d)(X).

Therefore ``E_nu <= d_nu^2/|G| I`` and every decoder after dephasing has

    p_success <= sum_nu p_nu d_nu^2/|G|
              <= max_nu d_nu^2/|G|.                          (1)

For ``G=S_n``, the right side is the largest Plancherel atom.  Aggarwal and
Elboim prove

    max_nu d_nu = sqrt(n!) exp(-(d+o(1))sqrt(n)), d>0,

so (1) is ``exp(-(2d+o(1))sqrt(n))``.  It cannot support constant exact
hidden-permutation identification.

This theorem does not rule out a coherent isotypic transform.  The coherent
label register retains cross-sector terms of every individual hidden state,
even though the average frame is block diagonal.  Those coherences are now a
necessary algorithmic resource: the orientation filter and final decoder must
preserve and exploit them.  Any implementation that samples ``nu``
classically, runs independent sector decoders, or discards the label is closed.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_isotypic_dephasing_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-ISOTYPIC-DEPHASING-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
MAXIMAL_DIMENSION_PAPER_ID = "aggarwal-elboim-maximal-dimension-2026"
MAXIMAL_DIMENSION_PAPER_URL = "https://arxiv.org/abs/2605.25995"


@dataclass(frozen=True)
class PartialTraceDominationControl:
    control_id: str
    irrep_dimension: int
    multiplicity_dimension: int
    operator_rank: int
    minimum_domination_eigenvalue: float
    domination_residual: float
    partial_trace_domination_verified: bool
    status: str


@dataclass(frozen=True)
class SymmetricGroupDephasingScalingRecord:
    n: int
    partition_count: int
    group_order_decimal: str
    maximum_irrep_partition: tuple[int, ...]
    maximum_irrep_dimension_decimal: str
    maximum_plancherel_atom: float
    exact_identification_success_upper_bound: float
    log2_identification_success_upper_bound: float
    exact_dimension_square_sum_verified: bool
    constant_success_ruled_out_at_this_scale: bool
    status: str


@dataclass(frozen=True)
class IsotypicDephasingNoGoReport:
    created_at: str
    theorem_contract: dict[str, Any]
    operator_controls: list[PartialTraceDominationControl]
    scaling_records: list[SymmetricGroupDephasingScalingRecord]
    proof_obligations: list[dict[str, bool | str]]
    adversarial_audit: list[dict[str, bool | str]]
    literature_links: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def partial_trace_first(
    operator: np.ndarray,
    first_dimension: int,
) -> np.ndarray:
    if operator.ndim != 2 or operator.shape[0] != operator.shape[1]:
        raise ValueError("operator must be square")
    if first_dimension < 1 or operator.shape[0] % first_dimension:
        raise ValueError("first dimension must divide operator dimension")
    second_dimension = operator.shape[0] // first_dimension
    tensor = operator.reshape(
        first_dimension,
        second_dimension,
        first_dimension,
        second_dimension,
    )
    return np.trace(tensor, axis1=0, axis2=2)


def audit_partial_trace_domination(
    first_dimension: int,
    second_dimension: int,
    rank: int,
    *,
    control_id: str,
    seed: int,
    tolerance: float = 1e-10,
) -> PartialTraceDominationControl:
    if first_dimension < 1 or second_dimension < 1:
        raise ValueError("tensor dimensions must be positive")
    total = first_dimension * second_dimension
    if not 1 <= rank <= total:
        raise ValueError("rank must lie within the total dimension")
    rng = np.random.default_rng(seed)
    factor = rng.normal(size=(total, rank)) + 1j * rng.normal(
        size=(total, rank)
    )
    operator = factor @ factor.T.conj()
    operator /= float(np.trace(operator).real)
    marginal = partial_trace_first(operator, first_dimension)
    domination = (
        first_dimension * np.kron(np.eye(first_dimension), marginal)
        - operator
    )
    minimum = float(np.linalg.eigvalsh((domination + domination.T.conj()) / 2)[0])
    residual = max(0.0, -minimum)
    verified = residual <= tolerance
    return PartialTraceDominationControl(
        control_id=control_id,
        irrep_dimension=first_dimension,
        multiplicity_dimension=second_dimension,
        operator_rank=rank,
        minimum_domination_eigenvalue=minimum,
        domination_residual=residual,
        partial_trace_domination_verified=verified,
        status=(
            "partial-trace-domination-verified"
            if verified
            else "partial-trace-domination-validation-failure"
        ),
    )


def symmetric_group_dephasing_record(
    n: int,
) -> SymmetricGroupDephasingScalingRecord:
    if n < 2:
        raise ValueError("n must be at least two")
    partitions = integer_partitions(n)
    dimensions = tuple(
        (partition, hook_length_dimension(partition))
        for partition in partitions
    )
    maximizing_partition, maximum_dimension = max(
        dimensions,
        key=lambda row: (row[1], row[0]),
    )
    order = math.factorial(n)
    atom = maximum_dimension * maximum_dimension / order
    square_sum = sum(dimension * dimension for _, dimension in dimensions)
    return SymmetricGroupDephasingScalingRecord(
        n=n,
        partition_count=len(partitions),
        group_order_decimal=str(order),
        maximum_irrep_partition=maximizing_partition,
        maximum_irrep_dimension_decimal=str(maximum_dimension),
        maximum_plancherel_atom=atom,
        exact_identification_success_upper_bound=atom,
        log2_identification_success_upper_bound=math.log2(atom),
        exact_dimension_square_sum_verified=square_sum == order,
        constant_success_ruled_out_at_this_scale=atom < 1 / 16,
        status=(
            "exact-isotypic-dephasing-identification-upper-bound"
            if square_sum == order
            else "symmetric-group-dimension-identity-failure"
        ),
    )


def run_isotypic_dephasing_no_go() -> IsotypicDephasingNoGoReport:
    controls = [
        audit_partial_trace_domination(2, 3, 1, control_id="D2-M3-R1", seed=11),
        audit_partial_trace_domination(3, 2, 4, control_id="D3-M2-R4", seed=17),
        audit_partial_trace_domination(4, 5, 9, control_id="D4-M5-R9", seed=23),
    ]
    scaling = [
        symmetric_group_dephasing_record(n)
        for n in (3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 28, 32)
    ]
    control_failures = sum(
        not row.partial_trace_domination_verified for row in controls
    )
    dimension_failures = sum(
        not row.exact_dimension_square_sum_verified for row in scaling
    )
    verified = control_failures == 0 and dimension_failures == 0
    constant_ruled = [
        row for row in scaling if row.constant_success_ruled_out_at_this_scale
    ]
    proof_obligations: list[dict[str, bool | str]] = [
        {
            "obligation": "covariant_povm_symmetrization",
            "resolved": True,
            "resolution": (
                "Uniform group priors permit averaging any POVM over the group "
                "without changing exact-label success."
            ),
        },
        {
            "obligation": "sector_seed_effect_partial_trace",
            "resolved": True,
            "resolution": (
                "Schur averaging of POVM completeness gives "
                "Tr_V(E_nu)=d_nu/|G| I on every multiplicity space."
            ),
        },
        {
            "obligation": "positive_partial_trace_domination",
            "resolved": verified,
            "resolution": (
                "For X>=0 on C^d tensor M, block-matrix Cauchy-Schwarz gives "
                "X<=d I_d tensor Tr_C^d(X)."
            ),
        },
        {
            "obligation": "dephased_identification_success_bound",
            "resolved": verified,
            "resolution": (
                "Each sector effect is at most d_nu^2/|G| times identity; "
                "weighting by sector probability gives max_nu d_nu^2/|G|."
            ),
        },
        {
            "obligation": "symmetric_group_asymptotic_decay",
            "resolved": True,
            "resolution": (
                "Aggarwal-Elboim's maximal-dimension theorem makes the largest "
                "Plancherel atom exp(-(2d+o(1))sqrt(n)), d>0."
            ),
        },
        {
            "obligation": "coherent_cross_sector_decoder",
            "resolved": False,
            "resolution": (
                "No circuit yet preserves, transforms, and decodes the necessary "
                "cross-nu coherences into a hidden permutation."
            ),
        },
    ]
    return IsotypicDephasingNoGoReport(
        created_at=utc_now(),
        theorem_contract={
            "uniform_covariant_ensemble": (
                "rho_g=R(g)rho_eR(g)^* with prior uniform over G."
            ),
            "isotypic_dephasing": (
                "Delta(rho)=sum_nu Pi_nu rho Pi_nu removes every cross-irrep block."
            ),
            "covariant_seed_constraint": (
                "Tr_(V_nu)(E_nu)=d_nu/|G| I_(M_nu)."
            ),
            "operator_inequality": (
                "X<=d I_d tensor Tr_(C^d)(X) for every X>=0."
            ),
            "identification_upper_bound": (
                "p_success(Delta(rho_g))<=max_nu d_nu^2/|G|, independent "
                "of multiplicity dimensions and all later channels."
            ),
            "data_processing": (
                "Once nu is dephased, no subsequent filter, unitary, ancilla, "
                "or measurement can exceed the bound."
            ),
            "symmetric_group_consequence": (
                "For G=S_n the bound is the largest Plancherel atom, which is "
                "exp(-(2d+o(1))sqrt(n))."
            ),
            "surviving_architecture": (
                "Use a coherent isotypic transform, retain the nu register, and "
                "make the final decoder interfere different nu sectors."
            ),
        },
        operator_controls=controls,
        scaling_records=scaling,
        proof_obligations=proof_obligations,
        adversarial_audit=[
            {
                "objection": "Large multiplicity spaces evade the d_nu^2/|G| bound.",
                "resolved": True,
                "resolution": (
                    "The partial-trace constraint is identity on the entire "
                    "multiplicity space, and the operator inequality removes its "
                    "dimension from the upper bound."
                ),
            },
            {
                "objection": "A noncovariant decoder can do better.",
                "resolved": True,
                "resolution": (
                    "Uniform-prior symmetrization preserves success and produces "
                    "a covariant decoder satisfying the same completeness."
                ),
            },
            {
                "objection": "The bound also rules out coherent isotypic transforms.",
                "resolved": False,
                "resolution": (
                    "No. It assumes the cross-nu blocks are dephased. A coherent "
                    "label isometry stores those blocks in label-carrier coherence."
                ),
            },
            {
                "objection": "Decision versions are automatically ruled out.",
                "resolved": False,
                "resolution": (
                    "The theorem concerns exact conjugate-label identification. "
                    "A coarser invariant or trivial-vs-nontrivial decision may "
                    "require less information."
                ),
            },
        ],
        literature_links=[
            {
                "paper_id": MAXIMAL_DIMENSION_PAPER_ID,
                "title": (
                    "On the maximal dimension of an irreducible representation "
                    "of the symmetric group"
                ),
                "url": MAXIMAL_DIMENSION_PAPER_URL,
                "use": (
                    "Converts the exact largest-Plancherel-atom decoder bound "
                    "into exp(-Omega(sqrt(n))) asymptotic decay."
                ),
                "external_theorem_not_reproved_here": True,
            }
        ],
        headline_metrics={
            "covariant_povm_symmetrization_theorem_count": 1,
            "positive_partial_trace_domination_theorem_count": 1,
            "isotypic_dephasing_identification_no_go_theorem_count": 1,
            "data_processing_extension_theorem_count": 1,
            "operator_control_count": len(controls),
            "operator_control_failure_count": control_failures,
            "exact_symmetric_group_scaling_record_count": len(scaling),
            "dimension_square_sum_failure_count": dimension_failures,
            "finite_constant_success_ruled_out_count": len(constant_ruled),
            "tail_n": scaling[-1].n,
            "tail_exact_success_upper_bound": (
                scaling[-1].exact_identification_success_upper_bound
            ),
            "tail_log2_success_upper_bound": (
                scaling[-1].log2_identification_success_upper_bound
            ),
            "coherent_cross_sector_decoder_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "isotypic_dephasing_identification_no_go_proved": verified,
            "classical_isotypic_outcome_decoder_viable_for_constant_identification": False,
            "independent_sector_decoders_viable_for_constant_identification": False,
            "coherent_isotypic_transform_ruled_out": False,
            "cross_sector_coherence_required_for_constant_identification": verified,
            "coherent_cross_sector_decoder_proved": False,
            "decision_version_ruled_out": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Any dephased-isotypic exact-label decoder has exp(-Omega(sqrt(n))) "
                "success. Coherent cross-sector processing is necessary but no "
                "efficient coherent decoder or classical separation is known."
            ),
        },
        status=(
            "isotypic-dephasing-identification-falsified-coherent-decoder-open"
            if verified
            else "isotypic-dephasing-no-go-validation-failure"
        ),
        summary=(
            "Proved that dephasing diagonal S_n irrep labels caps exact hidden-"
            "permutation success by the largest Plancherel atom, hence by "
            "exp(-Omega(sqrt(n))); cross-sector coherence is mandatory."
        ),
        falsifiers_triggered=[
            (
                "Measuring nu classically and decoding each sector independently "
                "cannot yield constant exact hidden-permutation success."
            ),
            (
                "Multiplicity-space dimension does not evade the no-go."
            ),
            (
                "The coherent isotypic label in the orientation filter is an "
                "essential information resource, not optional bookkeeping."
            ),
            (
                "The theorem does not rule out coherent cross-sector decoding or "
                "coarser decision problems."
            ),
        ],
    )


def write_isotypic_dephasing_no_go_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-ISOTYPIC-DEPHASING-NO-GO"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_isotypic_dephasing_no_go())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    return payload


if __name__ == "__main__":
    report = write_isotypic_dephasing_no_go_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
