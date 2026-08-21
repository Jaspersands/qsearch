"""Relative spectral flatness of hidden-involution orbit synthesis.

For a conjugacy class ``C`` of ``M`` distinct nonidentity involutions, let

    P_h = ((I+R_h)/2)^tensor k,   rank(P_h)=R=|G|^k/2^k.

Define the unnormalized orbit-synthesis map

    S : direct_sum_(h in C) ran(P_h) -> C[G]^tensor k,
    S((v_h)_h) = sum_h v_h.                              (1)

Then ``S S^*=sum_h P_h=M A_k``.  Distinct regular involution projectors have

    Tr(P_h P_g)=|G|^k/4^k=R/2^k.                        (2)

Therefore, with normalized trace on the ``MR``-dimensional synthesis domain,

    E[x]=1,
    E[(x-1)^2]=(M-1)/2^k =: eta,                         (3)

where ``x`` ranges over the eigenvalues of ``S^*S``, including its kernel.
The alternative state is exactly the pushforward of the maximally mixed
domain state:

    rho_C^k = S (I/(MR)) S^*.                            (4)

For ``0<delta<1``, Chebyshev and Cauchy--Schwarz imply

    Pr_alt[|x-1|>delta]
       = E[x 1_bad]
       <= eta(delta^-2 + delta^-1).                     (5)

Taking ``k=ceil(log2(64M))`` and ``delta=1/2`` gives ``eta<=1/64`` and

    Pr_alt[1/2 <= x <= 3/2] >= 29/32.                   (6)

Equivalently, at least ``29/32`` alternative mass has

    1/(2M) <= lambda(A_k) <= 3/(2M),

while the corresponding singular values of the unnormalized synthesis map
lie in ``[1/sqrt(2),sqrt(3/2)]``.  Thus the support is relatively well
conditioned on almost all natural alternative mass after the canonical
rescaling by ``M``.

This is a positive mechanism boundary, not an algorithm.  Standard coherent
orbit preparation exposes only ``S/sqrt(M)`` because erasing an ``M``-valued
branch label has amplitude ``1/sqrt(M)``.  Generic QSVT therefore still sees
the exponentially small absolute scale.  A breakthrough on this route must
compile the polar label-erasure map directly from symmetric/hyperoctahedral
multiplicity structure, or obtain a block encoding of the trimmed
unnormalized ``S`` with constant normalization.  Neither is constructed here.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

from coset_hidden_involution_binary_decision_reduction import (
    involution_class_size,
)
from coset_hidden_involution_orbit_hull_twirl_reduction import (
    orbit_average_candidate_projector,
)
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_orbit_synthesis_flatness.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-ORBIT-SYNTHESIS-FLATNESS"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class OrbitSynthesisFiniteControl:
    n: int
    transposition_count: int
    copy_count: int
    conjugacy_class_size: int
    physical_dimension: int
    candidate_projector_rank: int
    synthesis_domain_dimension: int
    synthesis_support_rank: int
    exact_domain_mean_squared_singular_value: float
    empirical_domain_mean_squared_singular_value: float
    exact_domain_centered_second_moment: float
    empirical_domain_centered_second_moment: float
    mean_identity_residual: float
    second_moment_identity_residual: float
    relative_window_delta: float
    exact_alternative_mass_in_relative_window: float
    certified_alternative_mass_in_relative_window_lower_bound: float
    relative_window_bound_respected: bool
    finite_control_verified: bool
    status: str


@dataclass(frozen=True)
class OrbitSynthesisScalingRecord:
    n: int
    conjugacy_class_size: int
    copy_count: int
    copy_overhead_beyond_log2_class_size: int
    domain_to_physical_dimension_ratio_upper_bound: float
    exact_domain_centered_second_moment: float
    relative_window_delta: float
    certified_alternative_relative_window_mass: float
    rescaled_frame_eigenvalue_lower_bound: float
    rescaled_frame_eigenvalue_upper_bound: float
    unnormalized_synthesis_singular_value_lower_bound: float
    unnormalized_synthesis_singular_value_upper_bound: float
    normalization_one_orbit_encoding_singular_value_upper_scale: float
    relative_conditioning_constant_on_retained_mass: bool
    constant_normalization_unnormalized_synthesis_access_constructed: bool
    polar_label_erasure_compiled: bool
    status: str


@dataclass(frozen=True)
class OrbitSynthesisFlatnessTheorem:
    synthesis_map: str
    pair_overlap_identity: str
    exact_domain_moments: str
    alternative_pushforward: str
    weighted_tail_bound: str
    constant_overhead_consequence: str
    access_boundary: str
    scope_limit: str
    exact_pair_overlap_proved: bool
    exact_synthesis_moments_proved: bool
    alternative_pushforward_proved: bool
    constant_mass_relative_flatness_proved: bool
    constant_normalization_synthesis_access_constructed: bool
    polar_label_erasure_compiled: bool
    polynomial_binary_algorithm_constructed: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class OrbitSynthesisFlatnessReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[OrbitSynthesisFiniteControl]
    scaling_records: list[OrbitSynthesisScalingRecord]
    theorem: OrbitSynthesisFlatnessTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def exact_synthesis_centered_second_moment(
    conjugacy_class_size: int,
    copy_count: int,
) -> Fraction:
    if conjugacy_class_size < 1 or copy_count < 1:
        raise ValueError("class size and copy count must be positive")
    return Fraction(conjugacy_class_size - 1, 1 << copy_count)


def alternative_bad_relative_spectrum_mass_upper_bound(
    conjugacy_class_size: int,
    copy_count: int,
    delta: float,
) -> float:
    if not 0.0 < delta < 1.0:
        raise ValueError("delta must lie in (0,1)")
    eta = float(
        exact_synthesis_centered_second_moment(
            conjugacy_class_size, copy_count
        )
    )
    return min(1.0, eta * (delta**-2 + delta**-1))


def flatness_copy_count(
    conjugacy_class_size: int,
    *,
    inverse_variance: int = 64,
) -> int:
    if conjugacy_class_size < 1 or inverse_variance < 1:
        raise ValueError("class size and inverse_variance must be positive")
    return (inverse_variance * conjugacy_class_size - 1).bit_length()


def audit_orbit_synthesis_control(
    n: int,
    transposition_count: int,
    copy_count: int,
    *,
    delta: float = 0.5,
    tolerance: float = 1e-9,
) -> OrbitSynthesisFiniteControl:
    if not 0.0 < delta < 1.0:
        raise ValueError("delta must lie in (0,1)")
    class_size = involution_class_size(n, transposition_count)
    physical_dimension = math.factorial(n) ** copy_count
    candidate_rank = physical_dimension // (1 << copy_count)
    domain_dimension = class_size * candidate_rank
    average = orbit_average_candidate_projector(
        n, transposition_count, copy_count
    )
    synthesis_frame = class_size * average
    eigenvalues = np.linalg.eigvalsh(
        (synthesis_frame + synthesis_frame.conj().T) / 2.0
    )
    positive = eigenvalues[eigenvalues > tolerance]
    support_rank = len(positive)
    empirical_mean = float(np.sum(positive) / domain_dimension)
    empirical_second = float(
        np.sum((positive - 1.0) ** 2)
        + (domain_dimension - support_rank)
    ) / domain_dimension
    exact_second = exact_synthesis_centered_second_moment(
        class_size, copy_count
    )
    in_window = positive[
        (positive >= 1.0 - delta - tolerance)
        & (positive <= 1.0 + delta + tolerance)
    ]
    alternative_window_mass = float(np.sum(in_window) / domain_dimension)
    lower = 1.0 - alternative_bad_relative_spectrum_mass_upper_bound(
        class_size, copy_count, delta
    )
    mean_residual = abs(empirical_mean - 1.0)
    second_residual = abs(empirical_second - float(exact_second))
    bound_respected = alternative_window_mass + tolerance >= lower
    verified = bool(
        support_rank <= domain_dimension
        and mean_residual <= 100 * tolerance
        and second_residual <= 100 * tolerance
        and bound_respected
    )
    return OrbitSynthesisFiniteControl(
        n=n,
        transposition_count=transposition_count,
        copy_count=copy_count,
        conjugacy_class_size=class_size,
        physical_dimension=physical_dimension,
        candidate_projector_rank=candidate_rank,
        synthesis_domain_dimension=domain_dimension,
        synthesis_support_rank=support_rank,
        exact_domain_mean_squared_singular_value=1.0,
        empirical_domain_mean_squared_singular_value=empirical_mean,
        exact_domain_centered_second_moment=float(exact_second),
        empirical_domain_centered_second_moment=empirical_second,
        mean_identity_residual=mean_residual,
        second_moment_identity_residual=second_residual,
        relative_window_delta=delta,
        exact_alternative_mass_in_relative_window=alternative_window_mass,
        certified_alternative_mass_in_relative_window_lower_bound=lower,
        relative_window_bound_respected=bound_respected,
        finite_control_verified=verified,
        status=(
            "exact-orbit-synthesis-relative-spectrum-verified"
            if verified
            else "orbit-synthesis-flatness-control-failure"
        ),
    )


def orbit_synthesis_scaling_record(
    n: int,
    *,
    inverse_variance: int = 64,
    delta: float = 0.5,
) -> OrbitSynthesisScalingRecord:
    if n < 6 or n % 2:
        raise ValueError("n must be even and at least six")
    if not 0.0 < delta < 1.0:
        raise ValueError("delta must lie in (0,1)")
    size = involution_class_size(n, n // 2)
    copies = flatness_copy_count(size, inverse_variance=inverse_variance)
    baseline = (size - 1).bit_length()
    eta = exact_synthesis_centered_second_moment(size, copies)
    bad = alternative_bad_relative_spectrum_mass_upper_bound(
        size, copies, delta
    )
    retained = 1.0 - bad
    lower = 1.0 - delta
    upper = 1.0 + delta
    return OrbitSynthesisScalingRecord(
        n=n,
        conjugacy_class_size=size,
        copy_count=copies,
        copy_overhead_beyond_log2_class_size=copies - baseline,
        domain_to_physical_dimension_ratio_upper_bound=(
            size / (1 << copies)
        ),
        exact_domain_centered_second_moment=float(eta),
        relative_window_delta=delta,
        certified_alternative_relative_window_mass=retained,
        rescaled_frame_eigenvalue_lower_bound=lower,
        rescaled_frame_eigenvalue_upper_bound=upper,
        unnormalized_synthesis_singular_value_lower_bound=math.sqrt(lower),
        unnormalized_synthesis_singular_value_upper_bound=math.sqrt(upper),
        normalization_one_orbit_encoding_singular_value_upper_scale=(
            math.sqrt(upper / size)
        ),
        relative_conditioning_constant_on_retained_mass=retained >= 29 / 32,
        constant_normalization_unnormalized_synthesis_access_constructed=False,
        polar_label_erasure_compiled=False,
        status=(
            "constant-overhead-relative-flatness-label-erasure-open"
            if retained >= 29 / 32
            else "orbit-synthesis-flatness-scaling-control-failure"
        ),
    )


def build_orbit_synthesis_flatness_report(
    *,
    finite_specs: tuple[tuple[int, int, int], ...] = (
        (3, 1, 1),
        (3, 1, 2),
        (3, 1, 3),
        (4, 2, 2),
    ),
    scaling_n_values: tuple[int, ...] = (6, 8, 16, 32, 64, 128),
) -> OrbitSynthesisFlatnessReport:
    controls = [
        audit_orbit_synthesis_control(n, transpositions, copies)
        for n, transpositions, copies in finite_specs
    ]
    scaling = [orbit_synthesis_scaling_record(n) for n in scaling_n_values]
    finite_verified = all(row.finite_control_verified for row in controls)
    scaling_verified = all(
        row.relative_conditioning_constant_on_retained_mass
        and not row.constant_normalization_unnormalized_synthesis_access_constructed
        and not row.polar_label_erasure_compiled
        for row in scaling
    )
    verified = finite_verified and scaling_verified
    theorem = OrbitSynthesisFlatnessTheorem(
        synthesis_map=(
            "S:direct_sum_h ran(P_h)->H, S((v_h))=sum_h v_h, with "
            "SS^*=sum_h P_h=M A_k."
        ),
        pair_overlap_identity=(
            "For h!=g, Tr(P_h P_g)=|G|^k/4^k=R/2^k."
        ),
        exact_domain_moments=(
            "Under normalized synthesis-domain trace, E[x]=1 and "
            "E[(x-1)^2]=(M-1)/2^k for x in spec(S^*S)."
        ),
        alternative_pushforward=(
            "rho_C^k=S(I/(MR))S^*, so alternative spectral mass is the "
            "x-size-biased synthesis-domain law."
        ),
        weighted_tail_bound=(
            "Pr_alt[|x-1|>delta]<=eta(delta^-2+delta^-1)."
        ),
        constant_overhead_consequence=(
            "At k=ceil(log2(64M)) and delta=1/2, at least 29/32 alternative "
            "mass has x in [1/2,3/2]."
        ),
        access_boundary=(
            "The standard coherent orbit LCU implements S/sqrt(M), not S. "
            "Direct polar label erasure or a constant-normalization trimmed "
            "synthesis encoding remains unconstructed."
        ),
        scope_limit=(
            "Relative flatness is not an efficient block encoding, polar "
            "compiler, hidden-involution decoder, or classical separation."
        ),
        exact_pair_overlap_proved=True,
        exact_synthesis_moments_proved=True,
        alternative_pushforward_proved=True,
        constant_mass_relative_flatness_proved=scaling_verified,
        constant_normalization_synthesis_access_constructed=False,
        polar_label_erasure_compiled=False,
        polynomial_binary_algorithm_constructed=False,
        theorem_verified=verified,
        status=(
            "orbit-synthesis-relative-flatness-proved-label-erasure-open"
            if verified
            else "orbit-synthesis-flatness-control-failure"
        ),
    )
    metrics: dict[str, int | float] = {
        "finite_control_count": len(controls),
        "finite_control_failure_count": sum(
            not row.finite_control_verified for row in controls
        ),
        "exact_pair_overlap_theorem_count": 1,
        "exact_synthesis_moment_theorem_count": 1,
        "constant_mass_relative_flatness_theorem_count": 1 if scaling_verified else 0,
        "minimum_certified_alternative_relative_window_mass": min(
            row.certified_alternative_relative_window_mass for row in scaling
        ),
        "maximum_scaling_domain_centered_second_moment": max(
            row.exact_domain_centered_second_moment for row in scaling
        ),
        "maximum_copy_overhead_beyond_log2_class_size": max(
            row.copy_overhead_beyond_log2_class_size for row in scaling
        ),
        "constant_normalization_synthesis_access_count": 0,
        "polar_label_erasure_compiler_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return OrbitSynthesisFlatnessReport(
        created_at=utc_now(),
        theorem_contract={
            "state_family": (
                "Uniform conjugacy class of distinct nonidentity involutions in "
                "the regular coset-state model; scaling records specialize to "
                "fixed-point-free involutions in S_n."
            ),
            "synthesis_domain": (
                "The orthogonal direct sum of the M candidate projector ranges, "
                "with normalized maximally mixed input."
            ),
            "relative_spectrum": (
                "Eigenvalues x of S^*S, equivalently M times positive "
                "eigenvalues of A_k."
            ),
            "access_model": (
                "Known controlled candidate projectors and coherent uniform class "
                "preparation expose S/sqrt(M); no free unnormalized S oracle."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-POLAR-LABEL-ERASURE",
                "statement": (
                    "Compile the polar of orbit synthesis so the matching-label "
                    "register is erased without amplitude 1/sqrt(M)."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-TRIMMED-SYNTHESIS-ACCESS",
                "statement": (
                    "Construct a constant-normalization block encoding of S on "
                    "the certified relative-flat window, or prove that selecting "
                    "that window itself costs superpolynomially."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-MULTIPLICITY-PATH-COMPILER",
                "statement": (
                    "Express the polar label erasure through coherent "
                    "S_n down to C_2 wr S_(n/2) subduction/multiplicity paths."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-CLASSICAL-SEPARATION",
                "statement": (
                    "Match any completed binary transform to a natural input "
                    "reduction and legal classical query/sample baseline."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "The useful support is intrinsically ill-conditioned.",
                "answer": (
                    "False in relative synthesis units: six extra copies put at "
                    "least 29/32 alternative mass in a constant singular window."
                ),
                "resolved": True,
            },
            {
                "challenge": "Relative flatness removes the QSVT barrier.",
                "answer": (
                    "False for the known encoding, which supplies S/sqrt(M); the "
                    "absolute singular values remain Theta(1/sqrt(M))."
                ),
                "resolved": True,
            },
            {
                "challenge": "Near-isometry means label erasure is automatic.",
                "answer": (
                    "False. Constructing the polar that coherently identifies "
                    "overlapping branch ranges is exactly the missing decoder."
                ),
                "resolved": True,
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "orbit_synthesis_relative_flatness_proved": scaling_verified,
            "constant_alternative_mass_well_conditioned_after_M_rescaling": scaling_verified,
            "standard_orbit_lcu_has_constant_normalization": False,
            "constant_normalization_trimmed_synthesis_access_constructed": False,
            "polar_label_erasure_compiled": False,
            "multiplicity_path_transform_constructed": False,
            "efficient_binary_hidden_involution_algorithm_constructed": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The state geometry is favorable after natural rescaling, but "
                "the only known coherent access divides S by sqrt(M). The core "
                "research problem is now normalization-free polar label erasure."
            ),
        },
        status=theorem.status,
        summary=(
            "Proved exact orbit-synthesis moments and constant-mass relative "
            "flatness with six extra copies. This preserves a high-upside fused "
            "polar route while isolating coherent label erasure, rather than "
            "relative conditioning, as the decisive implementation barrier."
        ),
        falsifiers_triggered=[
            "The logarithmic-copy support is not broadly ill-conditioned after its canonical M rescaling.",
            "The normalization-one low spectrum is caused by coherent orbit-label normalization, not a bad relative spectrum on most alternative mass.",
            "Generic QSVT remains exponential because the available encoding is S/sqrt(M).",
            "No polar label-erasure circuit, decoder, classical separation, or speedup has been constructed.",
        ],
    )


def write_orbit_synthesis_flatness_report(
    output_path: Path = REPORT_PATH,
    **kwargs: Any,
) -> dict[str, Any]:
    payload = asdict(build_orbit_synthesis_flatness_report(**kwargs))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return payload


if __name__ == "__main__":
    report = write_orbit_synthesis_flatness_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
