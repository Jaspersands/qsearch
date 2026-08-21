"""Constant hard mass inside proper hidden-involution multiplicity sectors.

For the fixed-point-free involution class in ``S_n``, let
``T=supp(A_k)`` be the logarithmic-copy support-span test and decompose it
under simultaneous conjugation as

    T = direct_sum_nu I_(V_nu) tensor S_nu.

Put ``t_nu=rank(S_nu)/dim(M_nu)``.  Under the null isotypic law ``p`` and the
alternative law ``q``, the support-rank bound and the all-n isotypic theorem
give

    E_p[t_nu] = rank(T)/dim(H) <= M/2^k <= 1/4,
    TV(p,q) <= epsilon <= 1/9.                            (1)

Since ``0<=t_nu<=1``, ``E_q[t_nu]<=1/4+epsilon``.  Markov therefore implies

    q{t_nu <= 1/2} >= 1 - 2(1/4+epsilon) >= 5/18.        (2)

Thus proper multiplicity support is not confined to a negligible witness:
at least ``5/18`` of alternative mass lies in sectors excluding at least half
of their multiplicity directions.

The global support-spectrum theorem puts at least ``3/4`` of alternative mass
on eigenvalues of ``A_k`` at most ``5/M``.  Both events are diagonal in the
same isotypic/spectral decomposition, so the union bound gives

    Pr_alt[t_nu<=1/2 and lambda(A_k)<=5/M] >= 1/36.       (3)

This is a uniform all-n hard-mass theorem for every even ``n>=6``.  It rules
out strategies that delete a negligible collection of proper sectors and then
apply a generic normalized support filter.  It does not rule out a coherent
transform that directly identifies ``supp(S_nu)`` or fuses its polar action
with state preparation; no circuit lower bound or speedup is claimed.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from coset_hidden_involution_binary_decision_reduction import involution_class_size
from coset_hidden_involution_isotypic_support_no_go import (
    class_count_isotypic_tv_upper_bound,
    elementary_isotypic_tv_upper_bound,
    fixed_point_free_threshold_copy_count,
)
from coset_hidden_involution_multiplicity_support_obstruction import (
    audit_multiplicity_support_control,
)
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_multiplicity_hard_mass.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-MULTIPLICITY-HARD-MASS"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class MultiplicityMassFiniteControl:
    n: int
    transposition_count: int
    copy_count: int
    sector_count: int
    support_null_mass: float
    alternative_average_support_fraction: float
    isotypic_total_variation: float
    expectation_transfer_upper_bound: float
    expectation_transfer_residual: float
    support_fraction_threshold: float
    observed_alternative_mass_at_or_below_threshold: float
    markov_lower_bound: float
    markov_bound_residual: float
    finite_control_verified: bool
    status: str


@dataclass(frozen=True)
class MultiplicityHardMassScalingRecord:
    n: int
    conjugacy_class_size: int
    copy_count: int
    support_null_mass_upper_bound: float
    isotypic_total_variation_upper_bound: float
    elementary_isotypic_total_variation_upper_bound: float
    support_fraction_threshold: float
    alternative_mass_in_half_support_sectors_lower_bound: float
    uniform_half_support_mass_lower_bound: float
    alternative_low_spectrum_mass_lower_bound: float
    low_spectrum_eigenvalue_upper_bound_times_class_size: float
    simultaneous_half_support_and_low_spectrum_mass_lower_bound: float
    uniform_simultaneous_hard_mass_lower_bound: float
    negligible_proper_sector_escape_possible: bool
    fused_multiplicity_transform_ruled_out: bool
    status: str


@dataclass(frozen=True)
class MultiplicityHardMassTheorem:
    support_fraction_identity: str
    distribution_transfer: str
    proper_sector_mass_bound: str
    low_spectrum_intersection: str
    compiler_consequence: str
    scope_limit: str
    support_fraction_identity_proved: bool
    constant_proper_sector_mass_proved: bool
    constant_proper_low_spectrum_intersection_proved: bool
    negligible_exceptional_sector_escape_refuted: bool
    fused_multiplicity_transform_refuted: bool
    arbitrary_circuit_lower_bound_proved: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class MultiplicityHardMassReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[MultiplicityMassFiniteControl]
    scaling_records: list[MultiplicityHardMassScalingRecord]
    theorem: MultiplicityHardMassTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def transferred_expectation_upper_bound(
    null_expectation: float,
    total_variation: float,
) -> float:
    if not 0.0 <= null_expectation <= 1.0:
        raise ValueError("null_expectation must lie in [0,1]")
    if not 0.0 <= total_variation <= 1.0:
        raise ValueError("total_variation must lie in [0,1]")
    return min(1.0, null_expectation + total_variation)


def threshold_mass_lower_bound(
    mean_upper_bound: float,
    threshold: float,
) -> float:
    """Return ``Pr[X<=threshold] >= 1-E[X]/threshold`` for ``X>=0``."""

    if mean_upper_bound < 0.0:
        raise ValueError("mean_upper_bound must be nonnegative")
    if not 0.0 < threshold <= 1.0:
        raise ValueError("threshold must lie in (0,1]")
    return max(0.0, 1.0 - mean_upper_bound / threshold)


def audit_multiplicity_mass_control(
    n: int,
    transposition_count: int,
    copy_count: int,
    *,
    support_fraction_threshold: float = 0.5,
) -> MultiplicityMassFiniteControl:
    row = audit_multiplicity_support_control(
        n, transposition_count, copy_count
    )
    support_null_mass = row.support_rank / row.data_dimension
    alternative_mean = sum(
        sector.alternative_irrep_probability * sector.support_fraction
        for sector in row.sectors
    )
    transferred = transferred_expectation_upper_bound(
        support_null_mass, row.irrep_label_total_variation
    )
    observed_mass = sum(
        sector.alternative_irrep_probability
        for sector in row.sectors
        if sector.support_fraction <= support_fraction_threshold + 1e-12
    )
    markov = threshold_mass_lower_bound(
        transferred, support_fraction_threshold
    )
    expectation_residual = max(0.0, alternative_mean - transferred)
    markov_residual = max(0.0, markov - observed_mass)
    verified = bool(
        row.finite_control_verified
        and expectation_residual <= 1e-9
        and markov_residual <= 1e-9
    )
    return MultiplicityMassFiniteControl(
        n=n,
        transposition_count=transposition_count,
        copy_count=copy_count,
        sector_count=row.irrep_sector_count,
        support_null_mass=support_null_mass,
        alternative_average_support_fraction=alternative_mean,
        isotypic_total_variation=row.irrep_label_total_variation,
        expectation_transfer_upper_bound=transferred,
        expectation_transfer_residual=expectation_residual,
        support_fraction_threshold=support_fraction_threshold,
        observed_alternative_mass_at_or_below_threshold=observed_mass,
        markov_lower_bound=markov,
        markov_bound_residual=markov_residual,
        finite_control_verified=verified,
        status=(
            "multiplicity-support-mass-transfer-verified"
            if verified
            else "multiplicity-support-mass-control-failure"
        ),
    )


def multiplicity_hard_mass_scaling_record(
    n: int,
) -> MultiplicityHardMassScalingRecord:
    if n < 6 or n % 2:
        raise ValueError("n must be even and at least six")
    size = involution_class_size(n, n // 2)
    copies = fixed_point_free_threshold_copy_count(n)
    null_upper = Fraction(size, 1 << copies)
    exact_tv_upper = class_count_isotypic_tv_upper_bound(n)
    elementary_tv = elementary_isotypic_tv_upper_bound(n)
    half_mass = threshold_mass_lower_bound(
        float(null_upper + exact_tv_upper), 0.5
    )
    uniform_half_mass = Fraction(5, 18)
    low_spectrum_mass = Fraction(3, 4)
    intersection = max(0.0, half_mass + float(low_spectrum_mass) - 1.0)
    uniform_intersection = Fraction(1, 36)
    verified = bool(
        exact_tv_upper <= elementary_tv
        and null_upper <= Fraction(1, 4)
        and half_mass >= float(uniform_half_mass)
        and intersection >= float(uniform_intersection)
    )
    return MultiplicityHardMassScalingRecord(
        n=n,
        conjugacy_class_size=size,
        copy_count=copies,
        support_null_mass_upper_bound=float(null_upper),
        isotypic_total_variation_upper_bound=float(exact_tv_upper),
        elementary_isotypic_total_variation_upper_bound=float(elementary_tv),
        support_fraction_threshold=0.5,
        alternative_mass_in_half_support_sectors_lower_bound=half_mass,
        uniform_half_support_mass_lower_bound=float(uniform_half_mass),
        alternative_low_spectrum_mass_lower_bound=float(low_spectrum_mass),
        low_spectrum_eigenvalue_upper_bound_times_class_size=5.0,
        simultaneous_half_support_and_low_spectrum_mass_lower_bound=intersection,
        uniform_simultaneous_hard_mass_lower_bound=float(uniform_intersection),
        negligible_proper_sector_escape_possible=False,
        fused_multiplicity_transform_ruled_out=False,
        status=(
            "constant-proper-low-spectrum-mass-proved-fused-transform-open"
            if verified
            else "multiplicity-hard-mass-scaling-proof-failure"
        ),
    )


def build_multiplicity_hard_mass_report(
    *,
    finite_specs: tuple[tuple[int, int, int], ...] = (
        (3, 1, 2),
        (3, 1, 3),
        (4, 2, 2),
    ),
    scaling_n_values: tuple[int, ...] = (6, 8, 16, 32, 64),
) -> MultiplicityHardMassReport:
    controls = [
        audit_multiplicity_mass_control(n, transpositions, copies)
        for n, transpositions, copies in finite_specs
    ]
    scaling = [
        multiplicity_hard_mass_scaling_record(n) for n in scaling_n_values
    ]
    finite_verified = all(row.finite_control_verified for row in controls)
    scaling_verified = all(
        not row.negligible_proper_sector_escape_possible
        and row.simultaneous_half_support_and_low_spectrum_mass_lower_bound
        >= row.uniform_simultaneous_hard_mass_lower_bound
        for row in scaling
    )
    verified = finite_verified and scaling_verified
    theorem = MultiplicityHardMassTheorem(
        support_fraction_identity=(
            "For T=direct_sum I_Vnu tensor S_nu and "
            "t_nu=rank(S_nu)/dim(M_nu), E_p[t_nu]=rank(T)/dim(H)<=M/2^k."
        ),
        distribution_transfer=(
            "For 0<=t_nu<=1, E_q[t_nu]<=E_p[t_nu]+TV(p,q)."
        ),
        proper_sector_mass_bound=(
            "At k=ceil(log2(4M)), q{t_nu<=1/2}>=5/18 for every even n>=6."
        ),
        low_spectrum_intersection=(
            "At least 1/36 alternative mass simultaneously has t_nu<=1/2 "
            "and lambda(A_k)<=5/M."
        ),
        compiler_consequence=(
            "Deleting exceptional proper sectors cannot regularize the generic "
            "normalization-one support filter; constant hard mass remains inside "
            "genuinely multiplicity-selective sectors."
        ),
        scope_limit=(
            "The theorem does not lower-bound a source-controlled transform that "
            "directly compiles each S_nu support or fuses the polar operation."
        ),
        support_fraction_identity_proved=True,
        constant_proper_sector_mass_proved=scaling_verified,
        constant_proper_low_spectrum_intersection_proved=scaling_verified,
        negligible_exceptional_sector_escape_refuted=scaling_verified,
        fused_multiplicity_transform_refuted=False,
        arbitrary_circuit_lower_bound_proved=False,
        theorem_verified=verified,
        status=(
            "constant-multiplicity-hard-mass-proved-fused-transform-open"
            if verified
            else "multiplicity-hard-mass-control-failure"
        ),
    )
    metrics: dict[str, int | float] = {
        "finite_control_count": len(controls),
        "finite_control_failure_count": sum(
            not row.finite_control_verified for row in controls
        ),
        "constant_proper_sector_mass_theorem_count": 1 if scaling_verified else 0,
        "constant_proper_low_spectrum_intersection_theorem_count": 1 if scaling_verified else 0,
        "minimum_alternative_half_support_mass_lower_bound": min(
            row.alternative_mass_in_half_support_sectors_lower_bound
            for row in scaling
        ),
        "minimum_simultaneous_proper_low_spectrum_mass_lower_bound": min(
            row.simultaneous_half_support_and_low_spectrum_mass_lower_bound
            for row in scaling
        ),
        "uniform_simultaneous_hard_mass_lower_bound": float(Fraction(1, 36)),
        "fused_multiplicity_transform_no_go_count": 0,
        "arbitrary_circuit_lower_bound_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return MultiplicityHardMassReport(
        created_at=utc_now(),
        theorem_contract={
            "family": "Fixed-point-free involutions in S_n, every even n>=6.",
            "copy_threshold": "k=ceil(log2(4(n-1)!!)).",
            "hard_sector": (
                "An isotypic sector in which the support occupies at most half "
                "of the global multiplicity space."
            ),
            "hard_spectrum": (
                "An A_k eigenvalue at most 5/M under the actual alternative "
                "spectral law."
            ),
            "outside_scope": (
                "Coherent support-specific transforms within multiplicity blocks."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-TYPICAL-MULTIPLICITY-BASIS",
                "statement": (
                    "Find a uniform basis or succinct relation description for "
                    "the proper support on the constant-mass typical sectors."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-FUSED-POLAR-COMPILER",
                "statement": (
                    "Construct or obstruct a fused polar/support isometry that "
                    "does not expose a standalone inverse at scale 1/M."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-END-TO-END-SEPARATION",
                "statement": (
                    "Provide a structured input reduction, polynomial gate audit, "
                    "and legal classical lower bound for any surviving transform."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "Only negligible alternative mass sees proper support.",
                "answer": (
                    "False: at least 5/18 lies in sectors with support fraction "
                    "at most one half."
                ),
                "resolved": True,
            },
            {
                "challenge": "The low spectrum may occur only in full sectors.",
                "answer": (
                    "False: the two mass bounds force at least 1/36 in their "
                    "intersection."
                ),
                "resolved": True,
            },
            {
                "challenge": "Constant hard mass proves the support is inefficient.",
                "answer": (
                    "False. It makes multiplicity-side structure unavoidable but "
                    "does not bound a structured coherent transform."
                ),
                "resolved": True,
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "constant_alternative_mass_in_proper_multiplicity_sectors_proved": scaling_verified,
            "constant_alternative_mass_simultaneously_proper_and_low_spectrum_proved": scaling_verified,
            "exceptional_proper_sector_deflation_rescues_generic_filter": False,
            "fused_multiplicity_support_transform_constructed": False,
            "fused_multiplicity_support_transform_refuted": False,
            "efficient_binary_hidden_involution_algorithm_constructed": False,
            "classical_separation_proved": False,
            "arbitrary_quantum_lower_bound_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The hard multiplicity and low-spectrum structure has constant "
                "natural mass, but no theorem yet constructs or excludes a fused "
                "multiplicity-support transform."
            ),
        },
        status=theorem.status,
        summary=(
            "Proved that proper multiplicity support is a constant-mass, not "
            "exceptional, phenomenon and that at least 1/36 of alternative mass "
            "is simultaneously proper and at O(1/M) spectral scale."
        ),
        falsifiers_triggered=[
            "The all-n proper-support theorem is not driven by one negligible isotypic sector.",
            "Removing exceptional multiplicity sectors cannot eliminate all low-spectrum alternative mass.",
            "A surviving compiler must handle constant natural mass inside proper multiplicity support.",
            "No arbitrary-circuit lower bound or speedup follows from the constant hard-mass theorem.",
        ],
    )


def write_multiplicity_hard_mass_report(
    output_path: Path = REPORT_PATH,
    **kwargs: Any,
) -> dict[str, Any]:
    payload = asdict(build_multiplicity_hard_mass_report(**kwargs))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return payload


if __name__ == "__main__":
    report = write_multiplicity_hard_mass_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
