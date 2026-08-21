"""Exact common-outlier deflation for fixed-point-free orbit synthesis.

Let ``C`` be the fixed-point-free involution class in ``S_n`` and

    P_h=((I+R_h)/2)^tensor k.

The intersection of all candidate ranges is determined by the normal closure
``N=<C>``.  A vector belongs to every ``ran(P_h)`` iff it is invariant under
right multiplication by every ``h in C`` independently on every register;
hence

    intersection_(h in C) ran(P_h) = C[S_n/N]^tensor k. (1)

For even ``n>=6``, simplicity of ``A_n`` gives

    N=S_n  when n/2 is odd,
    N=A_n  when n/2 is even.                             (2)

Thus the common dimension is ``a^k`` with ``a=[S_n:N]`` equal to one or two.
On this space the unnormalized orbit frame ``S S^*=sum_h P_h`` has eigenvalue
``M=|C|``.  This is the exact top singular outlier.

The outlier is efficiently recognizable: in each regular register,
``S_n``-invariants are the trivial Fourier sector, while ``A_n``-invariants
are the direct sum of the trivial and sign sectors.  A symmetric-group QFT can
therefore coherently flag and deflate it.

It is also negligible under the actual alternative state.  If
``R=|S_n|^k/2^k`` is one candidate rank, then

    Pr_alt[common] = a^k/R = (2a/|S_n|)^k.               (3)

Its fraction of the exact centered synthesis-domain second moment is

    ((M-1)/M) (4a/|S_n|)^k.                             (4)

Both are super-exponentially small at ``k=Theta(log M)``.  Therefore the
universal eigenvalue-``M`` block is a removable operator-norm obstruction but
does not carry the binary signal or explain the bulk relative variance.

This theorem does not bound the operator norm after deflation.  Pairwise and
higher intersection spaces can leave further large singular values.  A useful
next result must recursively classify those intersections or construct a
trimmed synthesis encoding; deleting only trivial/sign sectors is not yet a
polar label-erasure algorithm.
"""

from __future__ import annotations

import json
import math
from collections import deque
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from coset_hidden_involution_binary_decision_reduction import (
    Permutation,
    compose_permutations,
    involution_class_size,
    involution_conjugacy_class,
)
from coset_hidden_involution_orbit_synthesis_flatness import flatness_copy_count
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_common_outlier_deflation.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-COMMON-OUTLIER-DEFLATION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class NormalClosureFiniteControl:
    n: int
    transposition_count: int
    involution_class_size: int
    involution_parity: int
    generated_subgroup_order: int
    symmetric_group_order: int
    generated_subgroup_index: int
    expected_normal_closure: str
    expected_normal_closure_index: int
    exact_normal_closure_verified: bool
    status: str


@dataclass(frozen=True)
class CommonOutlierScalingRecord:
    n: int
    half_degree_parity: str
    conjugacy_class_size: int
    copy_count: int
    normal_closure: str
    normal_closure_index: int
    common_intersection_dimension_decimal: str
    common_frame_eigenvalue: int
    common_synthesis_singular_value: float
    common_alternative_mass_log2: float
    common_centered_variance_fraction_log2_upper_bound: float
    coherent_common_outlier_flag_available: bool
    common_outlier_deflation_removes_non_negligible_signal: bool
    post_deflation_operator_norm_bounded: bool
    status: str


@dataclass(frozen=True)
class CommonOutlierDeflationTheorem:
    common_intersection: str
    symmetric_group_normal_closure: str
    common_dimension: str
    outlier_eigenvalue: str
    coherent_deflation: str
    alternative_mass: str
    variance_share: str
    scope_limit: str
    common_intersection_proved: bool
    exact_normal_closure_proved: bool
    common_outlier_eigenvalue_proved: bool
    coherent_trivial_sign_deflation_available: bool
    common_outlier_natural_mass_negligible: bool
    post_deflation_operator_norm_bound_proved: bool
    polar_label_erasure_compiled: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class CommonOutlierDeflationReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[NormalClosureFiniteControl]
    scaling_records: list[CommonOutlierScalingRecord]
    theorem: CommonOutlierDeflationTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def permutation_parity(permutation: Permutation) -> int:
    inversions = sum(
        permutation[left] > permutation[right]
        for left in range(len(permutation))
        for right in range(left + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


def generated_subgroup(
    n: int,
    generators: tuple[Permutation, ...],
) -> frozenset[Permutation]:
    if not generators or any(len(generator) != n for generator in generators):
        raise ValueError("matching nonempty degree-n generators are required")
    identity = tuple(range(n))
    seen = {identity}
    queue: deque[Permutation] = deque([identity])
    while queue:
        current = queue.popleft()
        for generator in generators:
            product = compose_permutations(current, generator)
            if product not in seen:
                seen.add(product)
                queue.append(product)
    return frozenset(seen)


def expected_normal_closure_index(
    n: int,
    transposition_count: int,
) -> int:
    if n < 5:
        raise ValueError("the S_n/A_n normal-closure theorem requires n>=5")
    if transposition_count < 1 or 2 * transposition_count > n:
        raise ValueError("invalid involution class")
    return 1 if transposition_count % 2 else 2


def audit_normal_closure(
    n: int,
    transposition_count: int,
) -> NormalClosureFiniteControl:
    conjugacy_class = involution_conjugacy_class(n, transposition_count)
    subgroup = generated_subgroup(n, conjugacy_class)
    order = math.factorial(n)
    index = order // len(subgroup)
    expected_index = expected_normal_closure_index(n, transposition_count)
    parity = permutation_parity(conjugacy_class[0])
    expected_name = "S_n" if expected_index == 1 else "A_n"
    verified = bool(
        len(subgroup) * index == order
        and index == expected_index
        and parity == (-1 if transposition_count % 2 else 1)
        and all(permutation_parity(element) == 1 for element in subgroup)
        == (expected_index == 2)
    )
    return NormalClosureFiniteControl(
        n=n,
        transposition_count=transposition_count,
        involution_class_size=len(conjugacy_class),
        involution_parity=parity,
        generated_subgroup_order=len(subgroup),
        symmetric_group_order=order,
        generated_subgroup_index=index,
        expected_normal_closure=expected_name,
        expected_normal_closure_index=expected_index,
        exact_normal_closure_verified=verified,
        status=(
            "involution-class-normal-closure-verified"
            if verified
            else "normal-closure-control-failure"
        ),
    )


def common_outlier_scaling_record(n: int) -> CommonOutlierScalingRecord:
    if n < 6 or n % 2:
        raise ValueError("n must be even and at least six")
    transpositions = n // 2
    size = involution_class_size(n, transpositions)
    copies = flatness_copy_count(size)
    index = expected_normal_closure_index(n, transpositions)
    order = math.factorial(n)
    common_dimension = index**copies
    mass_log2 = copies * math.log2((2 * index) / order)
    variance_fraction_log2 = (
        math.log2((size - 1) / size)
        + copies * math.log2((4 * index) / order)
    )
    negligible = mass_log2 <= -20 and variance_fraction_log2 <= -20
    return CommonOutlierScalingRecord(
        n=n,
        half_degree_parity=("odd" if transpositions % 2 else "even"),
        conjugacy_class_size=size,
        copy_count=copies,
        normal_closure=("S_n" if index == 1 else "A_n"),
        normal_closure_index=index,
        common_intersection_dimension_decimal=str(common_dimension),
        common_frame_eigenvalue=size,
        common_synthesis_singular_value=math.sqrt(size),
        common_alternative_mass_log2=mass_log2,
        common_centered_variance_fraction_log2_upper_bound=(
            variance_fraction_log2
        ),
        coherent_common_outlier_flag_available=True,
        common_outlier_deflation_removes_non_negligible_signal=not negligible,
        post_deflation_operator_norm_bounded=False,
        status=(
            "common-outlier-efficiently-deflatable-negligible-mass-"
            "post-deflation-norm-open"
            if negligible
            else "common-outlier-finite-scaling-control"
        ),
    )


def build_common_outlier_deflation_report(
    *,
    finite_specs: tuple[tuple[int, int], ...] = (
        (5, 1),
        (5, 2),
        (6, 3),
    ),
    scaling_n_values: tuple[int, ...] = (6, 8, 16, 32, 64),
) -> CommonOutlierDeflationReport:
    controls = [
        audit_normal_closure(n, transpositions)
        for n, transpositions in finite_specs
    ]
    scaling = [common_outlier_scaling_record(n) for n in scaling_n_values]
    finite_verified = all(row.exact_normal_closure_verified for row in controls)
    scaling_verified = all(
        row.coherent_common_outlier_flag_available
        and not row.common_outlier_deflation_removes_non_negligible_signal
        and not row.post_deflation_operator_norm_bounded
        for row in scaling
    )
    verified = finite_verified and scaling_verified
    theorem = CommonOutlierDeflationTheorem(
        common_intersection=(
            "intersection_h ran(P_h)=C[S_n/<C>]^tensor k because every "
            "right involution acts trivially on every register."
        ),
        symmetric_group_normal_closure=(
            "For even n>=6, the fixed-point-free class normally generates S_n "
            "when n/2 is odd and A_n when n/2 is even."
        ),
        common_dimension=(
            "The common dimension is [S_n:<C>]^k, hence 1 or 2^k."
        ),
        outlier_eigenvalue=(
            "sum_h P_h equals M times identity on the common intersection, so "
            "the synthesis singular value is sqrt(M)."
        ),
        coherent_deflation=(
            "S_n QFT flags the per-register trivial sector for <C>=S_n and "
            "the trivial-plus-sign sectors for <C>=A_n."
        ),
        alternative_mass=(
            "The exact common alternative mass is (2[S_n:<C>]/n!)^k."
        ),
        variance_share=(
            "Its share of the centered synthesis variance is "
            "((M-1)/M)(4[S_n:<C>]/n!)^k."
        ),
        scope_limit=(
            "Removing the common block does not bound the remaining operator "
            "norm; pairwise/higher intersections and polar label erasure remain open."
        ),
        common_intersection_proved=True,
        exact_normal_closure_proved=True,
        common_outlier_eigenvalue_proved=True,
        coherent_trivial_sign_deflation_available=True,
        common_outlier_natural_mass_negligible=scaling_verified,
        post_deflation_operator_norm_bound_proved=False,
        polar_label_erasure_compiled=False,
        theorem_verified=verified,
        status=(
            "common-outlier-deflation-compiled-post-deflation-spectrum-open"
            if verified
            else "common-outlier-deflation-control-failure"
        ),
    )
    metrics: dict[str, int | float] = {
        "finite_normal_closure_control_count": len(controls),
        "finite_control_failure_count": sum(
            not row.exact_normal_closure_verified for row in controls
        ),
        "all_n_common_intersection_theorem_count": 1,
        "coherent_common_outlier_deflation_count": 1 if scaling_verified else 0,
        "maximum_common_alternative_mass_log2": max(
            row.common_alternative_mass_log2 for row in scaling
        ),
        "maximum_common_variance_fraction_log2": max(
            row.common_centered_variance_fraction_log2_upper_bound
            for row in scaling
        ),
        "post_deflation_operator_norm_theorem_count": 0,
        "polar_label_erasure_compiler_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return CommonOutlierDeflationReport(
        created_at=utc_now(),
        theorem_contract={
            "family": "Fixed-point-free involutions in S_n, every even n>=6.",
            "synthesis_operator": "SS^*=sum_h P_h=M A_k.",
            "outlier": (
                "The exact intersection of every candidate range, not an "
                "empirically selected high-eigenvalue sector."
            ),
            "deflation_primitive": (
                "Coherent per-register S_n Fourier tests for trivial, or "
                "trivial-plus-sign, right-invariant sectors."
            ),
            "outside_scope": (
                "The spectrum on the orthogonal complement and recursive "
                "pairwise/higher-intersection deflation."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-POST-COMMON-DEFLATION-NORM",
                "statement": (
                    "Bound or exhibit the largest synthesis singular value after "
                    "removing the common trivial/sign intersection."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-INTERSECTION-HIERARCHY",
                "statement": (
                    "Classify pairwise and higher candidate-range intersections "
                    "by generated dihedral/subgroup type and quantify their mass."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-HIDDEN-INVOLUTION-TRIMMED-LABEL-ERASURE",
                "statement": (
                    "Turn the recursively trimmed orbit synthesis into a coherent "
                    "constant-normalization polar map."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "The eigenvalue-M outlier is mysterious or inaccessible.",
                "answer": (
                    "False: it is exactly the normal-closure invariant space and "
                    "is coherently recognizable by trivial/sign Fourier labels."
                ),
                "resolved": True,
            },
            {
                "challenge": "The common outlier carries the binary signal.",
                "answer": (
                    "False: its exact alternative mass is (2a/n!)^k and is "
                    "super-exponentially negligible at threshold."
                ),
                "resolved": True,
            },
            {
                "challenge": "Removing it yields a constant-norm synthesis map.",
                "answer": (
                    "Not proved. Other subgroup intersections can support further "
                    "large singular values."
                ),
                "resolved": True,
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "common_intersection_exactly_classified": True,
            "common_eigenvalue_M_outlier_coherently_deflatable": scaling_verified,
            "common_outlier_carries_non_negligible_alternative_mass": False,
            "post_common_deflation_operator_norm_bounded": False,
            "recursive_intersection_deflation_constructed": False,
            "polar_label_erasure_compiled": False,
            "efficient_binary_hidden_involution_algorithm_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The obvious top outlier can be removed at negligible signal cost, "
                "but no norm bound or polar compiler exists for the remaining "
                "pairwise and higher intersection hierarchy."
            ),
        },
        status=theorem.status,
        summary=(
            "Classified and made coherently deflatable the exact eigenvalue-M "
            "common intersection. Its natural mass and variance share are "
            "negligible, leaving the post-deflation intersection hierarchy as "
            "the next spectral and compiler frontier."
        ),
        falsifiers_triggered=[
            "The universal top synthesis outlier is not an unknown multiplicity phenomenon.",
            "Trivial/sign deflation removes negligible, not decisive, alternative mass.",
            "The common outlier does not explain the bulk relative synthesis variance.",
            "No post-deflation norm bound, recursive trim, polar compiler, or speedup has been proved.",
        ],
    )


def write_common_outlier_deflation_report(
    output_path: Path = REPORT_PATH,
    **kwargs: Any,
) -> dict[str, Any]:
    payload = asdict(build_common_outlier_deflation_report(**kwargs))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return payload


if __name__ == "__main__":
    report = write_common_outlier_deflation_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
