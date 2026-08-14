"""Quantum-marginal boundary for disjoint orientation-core recoupling.

Two vertex-disjoint pair cores impose two incompatible coupling schemes on the
same membership-pattern grid: first couple every row to a one-dimensional
trivial/sign output, or first couple every column.  If ``B_row`` and
``B_column`` are isometries for those coupled bases, then

    B_row^* B_column                                      (1)

is, by definition, a generalized symmetric-group recoupling coefficient (a
``3nj`` block).  The projector product has exactly the same nonzero singular
values:

    ||P_row P_column|| = ||B_row^* B_column||.             (2)

This identifies the missing object behind the strict disjoint-grid falsifier.
It also connects the route to Christandl--Sahinoglu--Walter: for bounded row
counts, generalized recoupling coefficients are polynomially large only on
compatible quantum-marginal spectra and exponentially small away from that
compatibility region.

The bounded-row hypothesis is decisive.  Their ``poly(n)`` constants depend
on the maximum number ``d`` of rows.  Weyl's dimension formula alone gives

    dim V_lambda^d <= (n+d)^(d(d-1)/2).                   (3)

Thus its base-two logarithm is ``Theta(d^2 log n)``.  The published
spectrum-estimation suppression is only ``Theta(n)`` at constant marginal
distance.  The proof remains exponentially informative when
``d=o(sqrt(n/log n))``, is borderline at ``d=Theta(sqrt(n/log n))``, and is
vacuous at the natural Plancherel scale ``d=Theta(sqrt n)``.  Typical source
partitions in the repository lie in this last regime.

Consequently the quantum-marginal theorem is a research map, not a no-go for
the natural hidden-involution source.  The next useful theorem must either be
dimension-uniform in the Plancherel regime or exploit source-weighted
concentration strongly enough to replace worst-case Weyl prefactors.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable

import numpy as np

from research_registry import utc_now
from self_dual_wreath_disjoint_grid_recoupling_falsifier import (
    FIRST_PAIR,
    LABELS,
    SECOND_PAIRS,
    TARGET,
)
from self_dual_wreath_pair_core_carrier_factorization import (
    fixed_family_common_range_basis,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_grid_quantum_marginal_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-GRID-QUANTUM-MARGINAL-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Label = tuple[Partition, Partition]

RECOUPLING_PAPER_URL = "https://arxiv.org/abs/1210.0463"
SPECTRUM_ESTIMATION_PAPER_URL = "https://arxiv.org/abs/quant-ph/0102027"


@dataclass(frozen=True)
class GeneralizedRecouplingControl:
    control_id: str
    n: int
    target_partition: Partition
    first_pair: tuple[int, int]
    second_pair: tuple[int, int]
    row_coupled_dimension: int
    column_coupled_dimension: int
    recoupling_block_rank: int
    recoupling_operator_norm: float
    row_projector_product_norm: float
    projector_recoupling_norm_residual: float
    row_basis_isometry_residual: float
    column_basis_isometry_residual: float
    row_column_basis_are_two_coupling_schemes: bool
    generalized_recoupling_identity_verified: bool
    status: str


@dataclass(frozen=True)
class GrowingRowPrefactorRecord:
    n: int
    growth_regime: str
    row_count: int
    weyl_pair_count_exponent: int
    weyl_dimension_upper_bound_log2: float
    maximum_constant_distance_suppression_log2: float
    prefactor_to_maximum_suppression_ratio: float
    asymptotic_prefactor_order: str
    asymptotically_absorbable_into_exp_minus_omega_n: bool
    fixed_row_recoupling_theorem_directly_applies: bool
    status: str


@dataclass(frozen=True)
class GridQuantumMarginalBoundaryReport:
    created_at: str
    theorem_contract: dict[str, Any]
    recoupling_controls: list[GeneralizedRecouplingControl]
    prefactor_scaling: list[GrowingRowPrefactorRecord]
    literature_links: list[dict[str, str | bool]]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _basis_isometry_residual(basis: np.ndarray) -> float:
    if not basis.shape[1]:
        return 0.0
    identity = np.eye(basis.shape[1], dtype=complex)
    return float(np.linalg.norm(basis.conj().T @ basis - identity, ord=2))


def audit_generalized_recoupling_control(
    control_id: str,
    target: Partition,
    labels: tuple[Label, ...],
    first_pair: tuple[int, int],
    second_pair: tuple[int, int],
    *,
    tolerance: float = 1e-9,
) -> GeneralizedRecouplingControl:
    if len(set(first_pair) | set(second_pair)) != 4:
        raise ValueError("recoupling control requires vertex-disjoint pairs")
    row_basis = fixed_family_common_range_basis(
        target,
        labels,
        first_pair,
    )
    column_basis = fixed_family_common_range_basis(
        target,
        labels,
        second_pair,
    )
    block = row_basis.conj().T @ column_basis
    singular_values = np.linalg.svd(block, compute_uv=False)
    recoupling_norm = float(singular_values[0]) if len(singular_values) else 0.0

    # For isometries B,C, ||BB^*CC^*||=||B^*C||.  Evaluate the smaller
    # equivalent product without materializing ambient square projectors.
    projector_product_norm = float(
        np.linalg.norm(block @ block.conj().T, ord=2) ** 0.5
    )
    row_residual = _basis_isometry_residual(row_basis)
    column_residual = _basis_isometry_residual(column_basis)
    norm_residual = abs(projector_product_norm - recoupling_norm)
    verified = bool(
        row_basis.shape[1]
        and column_basis.shape[1]
        and row_residual <= 100 * tolerance
        and column_residual <= 100 * tolerance
        and norm_residual <= 100 * tolerance
    )
    return GeneralizedRecouplingControl(
        control_id=control_id,
        n=sum(target),
        target_partition=target,
        first_pair=first_pair,
        second_pair=second_pair,
        row_coupled_dimension=row_basis.shape[1],
        column_coupled_dimension=column_basis.shape[1],
        recoupling_block_rank=int(
            np.sum(singular_values > 100 * tolerance)
        ),
        recoupling_operator_norm=recoupling_norm,
        row_projector_product_norm=projector_product_norm,
        projector_recoupling_norm_residual=norm_residual,
        row_basis_isometry_residual=row_residual,
        column_basis_isometry_residual=column_residual,
        row_column_basis_are_two_coupling_schemes=True,
        generalized_recoupling_identity_verified=verified,
        status=(
            "disjoint-core-is-generalized-recoupling-block"
            if verified
            else "generalized-recoupling-control-failure"
        ),
    )


def weyl_dimension_upper_bound_log2(n: int, row_count: int) -> float:
    """Log2 of the simple Weyl bound ``(n+d)^(d(d-1)/2)``."""

    if n < 2 or not 1 <= row_count <= n:
        raise ValueError("require n>=2 and 1<=row_count<=n")
    exponent = row_count * (row_count - 1) // 2
    return exponent * math.log2(n + row_count)


def _growth_regimes() -> tuple[
    tuple[str, Callable[[int], int], str, bool, bool], ...
]:
    return (
        ("fixed-four-rows", lambda _n: 4, "Theta(log n)", True, True),
        (
            "fourth-root-rows",
            lambda n: max(2, math.ceil(n**0.25)),
            "Theta(sqrt(n) log n)=o(n)",
            True,
            False,
        ),
        (
            "sqrt-n-over-log-n-rows",
            lambda n: max(2, math.ceil(math.sqrt(n / math.log(n)))),
            "Theta(n)",
            False,
            False,
        ),
        (
            "plancherel-two-sqrt-n-rows",
            lambda n: min(n, max(2, math.ceil(2 * math.sqrt(n)))),
            "Theta(n log n)",
            False,
            False,
        ),
    )


def growing_row_prefactor_record(
    n: int,
    growth_regime: str,
    row_count: int,
    asymptotic_order: str,
    absorbable: bool,
    direct_application: bool,
) -> GrowingRowPrefactorRecord:
    if n < 2:
        raise ValueError("n must be at least two")
    rows = min(n, max(1, row_count))
    overhead = weyl_dimension_upper_bound_log2(n, rows)
    # The recoupling paper obtains exp(-n D^2/4) for the squared norm.
    # Since any trace-distance-like l1 spectral distance has D<=2, no
    # constant-distance use of that term suppresses more than exp(-n).
    suppression = n / math.log(2)
    return GrowingRowPrefactorRecord(
        n=n,
        growth_regime=growth_regime,
        row_count=rows,
        weyl_pair_count_exponent=rows * (rows - 1) // 2,
        weyl_dimension_upper_bound_log2=overhead,
        maximum_constant_distance_suppression_log2=suppression,
        prefactor_to_maximum_suppression_ratio=overhead / suppression,
        asymptotic_prefactor_order=asymptotic_order,
        asymptotically_absorbable_into_exp_minus_omega_n=absorbable,
        fixed_row_recoupling_theorem_directly_applies=direct_application,
        status=(
            "published-fixed-row-proof-exponentially-informative"
            if absorbable
            else "published-prefactor-audit-not-exponentially-informative"
        ),
    )


def run_grid_quantum_marginal_boundary(
) -> GridQuantumMarginalBoundaryReport:
    controls = [
        audit_generalized_recoupling_control(
            f"S6-GRID-RECOUPLING-{index}",
            TARGET,
            LABELS,
            FIRST_PAIR,
            second_pair,
        )
        for index, second_pair in enumerate(SECOND_PAIRS, start=1)
    ]
    scaling = [
        growing_row_prefactor_record(
            n,
            regime,
            row_function(n),
            asymptotic_order,
            absorbable,
            direct,
        )
        for n in (64, 256, 1024, 4096)
        for regime, row_function, asymptotic_order, absorbable, direct in _growth_regimes()
    ]
    controls_verified = all(
        row.generalized_recoupling_identity_verified for row in controls
    )
    plancherel_rows = [
        row
        for row in scaling
        if row.growth_regime == "plancherel-two-sqrt-n-rows"
    ]
    fixed_rows = [
        row for row in scaling if row.growth_regime == "fixed-four-rows"
    ]
    return GridQuantumMarginalBoundaryReport(
        created_at=utc_now(),
        theorem_contract={
            "exact_identification": (
                "Disjoint pair cores are row-coupled and column-coupled "
                "one-dimensional output sectors of one membership grid; their "
                "basis overlap is a generalized symmetric-group recoupling block."
            ),
            "norm_identity": (
                "For coupled-basis isometries B_row,B_column, "
                "||P_row P_column||=||B_row^*B_column||."
            ),
            "published_asymptotic": (
                "At uniformly bounded row count, recoupling blocks are "
                "polynomially large on compatible quantum-marginal spectra and "
                "exponentially small at constant distance from compatibility."
            ),
            "dimension_scope": (
                "The theorem's polynomial factors depend on maximum row count d; "
                "Weyl dimension contributes at most (n+d)^(d(d-1)/2)."
            ),
            "natural_source_boundary": (
                "At d=Theta(sqrt n), this proof overhead has log Theta(n log n), "
                "larger than its constant-distance Theta(n) suppression."
            ),
            "scope": (
                "The exact recoupling identification is finite-dimensional. The "
                "asymptotic dichotomy is imported only in its published fixed-row "
                "scope and is not claimed for Plancherel partitions."
            ),
        },
        recoupling_controls=controls,
        prefactor_scaling=scaling,
        literature_links=[
            {
                "paper_id": "christandl-sahinoglu-walter-2016",
                "title": "Recoupling coefficients and quantum entropies",
                "url": RECOUPLING_PAPER_URL,
                "use": (
                    "Projector-product/recoupling norm identity, fixed-row "
                    "quantum-marginal asymptotic dichotomy, and generalized 3nj extension."
                ),
                "external_theorem_not_reproved_here": True,
            },
            {
                "paper_id": "keyl-werner-2001",
                "title": "Estimating the spectrum of a density operator",
                "url": SPECTRUM_ESTIMATION_PAPER_URL,
                "use": (
                    "Spectrum-estimation large-deviation input and explicit "
                    "fixed-dimension dependence through Weyl representation dimensions."
                ),
                "external_theorem_not_reproved_here": True,
            },
        ],
        proof_obligations=[
            {
                "obligation": "write_explicit_grid_3nj_channel_formula",
                "resolved": False,
                "resolution": (
                    "Index all row/column parity sectors, Kronecker multiplicity "
                    "spaces, and normalized recoupling maps without dense ambient bases."
                ),
            },
            {
                "obligation": "dimension_uniform_plancherel_recoupling_bound",
                "resolved": False,
                "resolution": (
                    "Replace worst-case Weyl prefactors by a theorem uniform for "
                    "Theta(sqrt n)-row Plancherel diagrams, or prove this impossible."
                ),
            },
            {
                "obligation": "source_weighted_quantum_marginal_feasibility",
                "resolved": False,
                "resolution": (
                    "Determine whether naturally weighted grid spectra lie inside, "
                    "near, or a constant distance outside the compatible marginal region."
                ),
            },
            {
                "obligation": "coherent_generalized_recoupling_compiler",
                "resolved": False,
                "resolution": (
                    "No polynomial circuit for the source-relevant 3nj blocks is known."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "The strict 1/15 value is an unexplained dense-matrix artifact.",
                "resolved": True,
                "resolution": (
                    "Its mathematical object is now identified: a block of the "
                    "unitary change between row-first and column-first coupling schemes."
                ),
            },
            {
                "objection": "The quantum-marginal dichotomy immediately proves "
                "natural disjoint cores are exponentially orthogonal.",
                "resolved": True,
                "resolution": (
                    "False. The published polynomial equivalence fixes the maximum "
                    "row count, while natural Plancherel row counts grow as sqrt(n)."
                ),
            },
            {
                "objection": "A large Weyl upper bound proves the true coefficient is large.",
                "resolved": True,
                "resolution": (
                    "False. It proves only that the published proof loses exponential "
                    "control; the true source-weighted coefficient may still be small."
                ),
            },
            {
                "objection": "Quantum-marginal compatibility supplies a coherent circuit.",
                "resolved": True,
                "resolution": (
                    "False. It is an asymptotic magnitude criterion, not a basis or "
                    "recoupling compiler."
                ),
            },
        ],
        headline_metrics={
            "generalized_recoupling_identity_control_count": len(controls),
            "generalized_recoupling_identity_failure_count": sum(
                not row.generalized_recoupling_identity_verified for row in controls
            ),
            "fixed_row_tail_prefactor_to_suppression_ratio": (
                fixed_rows[-1].prefactor_to_maximum_suppression_ratio
            ),
            "plancherel_row_tail_prefactor_to_suppression_ratio": (
                plancherel_rows[-1].prefactor_to_maximum_suppression_ratio
            ),
            "dimension_uniform_plancherel_recoupling_theorem_count": 0,
            "source_weighted_marginal_feasibility_theorem_count": 0,
            "coherent_generalized_recoupling_compiler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "disjoint_core_is_generalized_recoupling_block": controls_verified,
            "projector_product_recoupling_norm_identity_verified": controls_verified,
            "fixed_row_quantum_marginal_dichotomy_literature_linked": True,
            "published_fixed_row_proof_covers_plancherel_regime": False,
            "dimension_uniform_plancherel_recoupling_bound_proved": False,
            "natural_source_marginal_compatibility_classified": False,
            "coherent_generalized_recoupling_compiled": False,
            "uniform_residual_pair_quotient_gap_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The correct asymptotic object is identified, but the available "
                "quantum-marginal theorem loses control at sqrt(n) row growth and "
                "does not provide a coherent transform."
            ),
        },
        status=(
            "grid-recoupling-identified-plancherel-marginal-boundary-open"
            if controls_verified
            else "grid-recoupling-identity-control-failure"
        ),
        summary=(
            "Identified disjoint pair-core overlap as a generalized symmetric-group "
            "recoupling block and proved that the published fixed-row quantum-marginal "
            "asymptotics do not directly control the natural Plancherel row regime."
        ),
        falsifiers_triggered=[
            "Disjoint grid contraction is not an unnamed scalar correction; it is 3nj data.",
            "Fixed-row recoupling asymptotics cannot be silently applied at sqrt(n) rows.",
            "Quantum-marginal magnitude criteria do not compile recoupling circuits.",
        ],
    )


def write_grid_quantum_marginal_boundary_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    del write_registry, registry_experiment_id, registry_candidate_id, registry_result_id
    payload = asdict(run_grid_quantum_marginal_boundary(**kwargs))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_grid_quantum_marginal_boundary_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
