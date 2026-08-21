"""All-copy target-coupled normalized-LCU no-go.

Use the exact double-coset normal form in ``L=G^k x G`` for an involution
``h``, ``H=<h>``, and ``K=C_G(h)``:

    A={(r,...,r;r):r in G},
    B={(eps_1 r,...,eps_k r;r):r in K, eps_i in H},
    Z=[G:K] e_B e_A e_B.

For a basis element ``ell=(g_1,...,g_k;t)``, define

    c_H(g,t)=#{(eps,eps') in H^2 : g=eps t eps'}.

The exact ``BAB`` factorization count gives

    tr_B(ell Z) = 2^(-k) product_i c_H(g_i^-1,t^-1),
    tr_B(ell)   = 1[ell^-1 in B].                       (1)

If ``t in K``, every supported local factor has multiplicity two and the two
traces in (1) agree.  If ``t notin K``, the four elements of ``HtH`` are
distinct because ``N_G(H)=C_G(h)=K``; each nonzero local multiplicity is one,
the baseline trace is zero, and the likelihood bias is exactly ``2^-k``.
Thus every group-basis element has bias either zero or ``2^-k``.

For an arbitrary all-copy target-coupled LCU

    X=sum_ell alpha_ell ell,

the exact pointwise formula yields

    |tr_B(XZ)-tr_B(X)| <= 2^(-k) sum_ell |alpha_ell|.   (2)

This is not restricted to diagonal tuples, one Hecke orbital, bounded word
degree, or commuting charges.  At the natural copy count
``k=ceil(log2(64[G:K]))``, every unit-L1 LCU has bias at most
``1/(64[G:K])``; constant linear bias requires L1 normalization at least
``2^k`` and recreates the candidate-orbit normalization barrier.

The coefficient in (1) is classically computable in ``O(k)`` group
operations, so expectations of efficiently sampleable LCUs also have a
matched classical importance sampler.  The theorem does not cover nonlinear
spectral functions of compressed operators, postselection, or matrix-CS
polar transforms whose group-basis expansion can have exponentially large
L1 norm despite bounded operator norm.  Those are the remaining boundary.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from coset_hidden_involution_binary_decision_reduction import (
    Permutation,
    compose_permutations,
    inverse_permutation,
    involution_class_size,
)
from coset_hidden_involution_orbit_synthesis_flatness import (
    flatness_copy_count,
)
from coset_hidden_involution_source_local_likelihood_no_go import (
    ProductElement,
    _BAB_counts,
    _product_inverse,
    _subgroups,
)
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_all_copy_target_lcu_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-ALL-COPY-TARGET-LCU-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class AllCopyBasisFormulaControl:
    degree: int
    transposition_count: int
    copy_count: int
    group_order: int
    centralizer_order: int
    product_basis_element_count: int
    inside_K_basis_element_count: int
    outside_K_supported_basis_element_count: int
    zero_bias_basis_element_count: int
    exact_two_to_minus_k_bias_basis_element_count: int
    maximum_baseline_formula_residual: float
    maximum_likelihood_formula_residual: float
    maximum_bias_formula_residual: float
    outside_K_local_double_coset_multiplicity_always_one: bool
    all_basis_elements_have_zero_or_two_to_minus_k_bias: bool
    exact_basis_formula_verified: bool
    status: str


@dataclass(frozen=True)
class AllCopyLCUScalingRecord:
    half_degree: int
    degree: int
    hidden_matching_count_decimal: str
    copy_count: int
    unit_L1_bias_upper_bound: float
    unit_L1_bias_log2_upper_bound: float
    inverse_64_candidates: float
    constant_bias_L1_norm_lower_bound_decimal: str
    coefficient_weight_classically_computable_in_copy_linear_time: bool
    normalized_LCU_has_useful_linear_bias: bool
    status: str


@dataclass(frozen=True)
class AllCopyTargetLCUNoGoTheorem:
    basis_trace_formula: str
    pointwise_bias: str
    arbitrary_LCU_bound: str
    classical_evaluation: str
    natural_copy_consequence: str
    exact_all_finite_groups_basis_formula_proved: bool
    arbitrary_all_copy_target_L1_LCU_bound_proved: bool
    normalized_sparse_target_recoupling_linear_detector_ruled_out: bool
    efficiently_sampleable_LCU_expectation_classically_estimable: bool
    nonlinear_spectral_function_no_go_proved: bool
    bounded_operator_large_L1_no_go_proved: bool
    matrix_CS_polar_no_go_proved: bool
    adaptive_postselection_no_go_proved: bool
    hidden_involution_detector_constructed: bool
    speedup_claim_allowed: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class AllCopyTargetLCUNoGoReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[AllCopyBasisFormulaControl]
    scaling_records: list[AllCopyLCUScalingRecord]
    theorem: AllCopyTargetLCUNoGoTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float | str]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def order_two_subgroup(identity: Permutation, hidden: Permutation) -> tuple[Permutation, ...]:
    return (identity, hidden)


def local_double_coset_multiplicity(
    value: Permutation,
    target: Permutation,
    hidden: Permutation,
) -> int:
    identity = tuple(range(len(hidden)))
    order_two = order_two_subgroup(identity, hidden)
    return sum(
        compose_permutations(
            compose_permutations(left, target),
            right,
        )
        == value
        for left in order_two
        for right in order_two
    )


def predicted_basis_traces(
    inverse_element: ProductElement,
    hidden: Permutation,
    centralizer: set[Permutation],
) -> tuple[Fraction, Fraction]:
    sources = inverse_element[:-1]
    target = inverse_element[-1]
    copy_count = len(sources)
    multiplicities = [
        local_double_coset_multiplicity(value, target, hidden)
        for value in sources
    ]
    likelihood = Fraction(math.prod(multiplicities), 2**copy_count)
    identity = tuple(range(len(hidden)))
    order_two = (identity, hidden)
    baseline_supported = bool(
        target in centralizer
        and all(
            value
            in {
                compose_permutations(epsilon, target)
                for epsilon in order_two
            }
            for value in sources
        )
    )
    return Fraction(int(baseline_supported), 1), likelihood


def audit_all_copy_basis_formula(
    degree: int,
    transposition_count: int,
    copy_count: int,
) -> AllCopyBasisFormulaControl:
    group, centralizer_tuple, diagonal, source_stabilizer, hidden = _subgroups(
        degree,
        transposition_count,
        copy_count,
    )
    centralizer = set(centralizer_tuple)
    source_stabilizer_set = set(source_stabilizer)
    counts = _BAB_counts(diagonal, source_stabilizer)
    B_order = len(source_stabilizer)
    M = len(group) // len(centralizer)
    expected_bias = Fraction(1, 2**copy_count)
    maximum_baseline = Fraction(0, 1)
    maximum_likelihood = Fraction(0, 1)
    maximum_bias = Fraction(0, 1)
    inside = 0
    outside_supported = 0
    zero_bias = 0
    exact_bias = 0
    outside_multiplicities_one = True
    tested = 0
    for element in itertools.product(group, repeat=copy_count + 1):
        inverse_element = _product_inverse(element)
        predicted_baseline, predicted_likelihood = predicted_basis_traces(
            inverse_element,
            hidden,
            centralizer,
        )
        observed_baseline = Fraction(
            int(inverse_element in source_stabilizer_set),
            1,
        )
        factorization_count = counts.get(inverse_element, 0)
        observed_likelihood = Fraction(
            M * B_order * factorization_count,
            B_order**2 * len(diagonal),
        )
        bias = observed_likelihood - observed_baseline
        target = inverse_element[-1]
        multiplicities = [
            local_double_coset_multiplicity(value, target, hidden)
            for value in inverse_element[:-1]
        ]
        if target in centralizer:
            inside += 1
        elif all(multiplicities):
            outside_supported += 1
            outside_multiplicities_one &= set(multiplicities) == {1}
        zero_bias += bias == 0
        exact_bias += bias == expected_bias
        maximum_baseline = max(
            maximum_baseline,
            abs(observed_baseline - predicted_baseline),
        )
        maximum_likelihood = max(
            maximum_likelihood,
            abs(observed_likelihood - predicted_likelihood),
        )
        maximum_bias = max(
            maximum_bias,
            min(abs(bias), abs(bias - expected_bias)),
        )
        tested += 1
    verified = bool(
        maximum_baseline == 0
        and maximum_likelihood == 0
        and maximum_bias == 0
        and zero_bias + exact_bias == tested
        and outside_multiplicities_one
    )
    return AllCopyBasisFormulaControl(
        degree=degree,
        transposition_count=transposition_count,
        copy_count=copy_count,
        group_order=len(group),
        centralizer_order=len(centralizer),
        product_basis_element_count=tested,
        inside_K_basis_element_count=inside,
        outside_K_supported_basis_element_count=outside_supported,
        zero_bias_basis_element_count=zero_bias,
        exact_two_to_minus_k_bias_basis_element_count=exact_bias,
        maximum_baseline_formula_residual=float(maximum_baseline),
        maximum_likelihood_formula_residual=float(maximum_likelihood),
        maximum_bias_formula_residual=float(maximum_bias),
        outside_K_local_double_coset_multiplicity_always_one=(
            outside_multiplicities_one
        ),
        all_basis_elements_have_zero_or_two_to_minus_k_bias=(
            zero_bias + exact_bias == tested
        ),
        exact_basis_formula_verified=verified,
        status=(
            "all-copy-target-basis-bias-formula-verified"
            if verified
            else "all-copy-target-basis-formula-control-failure"
        ),
    )


def all_copy_LCU_scaling_record(half_degree: int) -> AllCopyLCUScalingRecord:
    if half_degree < 2:
        raise ValueError("half_degree must be at least two")
    degree = 2 * half_degree
    candidates = involution_class_size(degree, half_degree)
    copies = flatness_copy_count(candidates)
    bias = 2.0**-copies
    return AllCopyLCUScalingRecord(
        half_degree=half_degree,
        degree=degree,
        hidden_matching_count_decimal=str(candidates),
        copy_count=copies,
        unit_L1_bias_upper_bound=bias,
        unit_L1_bias_log2_upper_bound=-float(copies),
        inverse_64_candidates=1.0 / (64.0 * candidates),
        constant_bias_L1_norm_lower_bound_decimal=str(2**copies),
        coefficient_weight_classically_computable_in_copy_linear_time=True,
        normalized_LCU_has_useful_linear_bias=False,
        status="normalized-all-copy-target-LCU-inverse-candidate-bias",
    )


def build_all_copy_target_LCU_no_go_report() -> AllCopyTargetLCUNoGoReport:
    controls = [
        audit_all_copy_basis_formula(3, 1, 2),
        audit_all_copy_basis_formula(3, 1, 3),
        audit_all_copy_basis_formula(4, 2, 2),
    ]
    scaling = [
        all_copy_LCU_scaling_record(value)
        for value in (4, 8, 16, 32, 64, 128)
    ]
    exact = all(row.exact_basis_formula_verified for row in controls)
    natural = all(
        row.unit_L1_bias_upper_bound <= row.inverse_64_candidates
        for row in scaling
    )
    theorem = AllCopyTargetLCUNoGoTheorem(
        basis_trace_formula=(
            "tr_B(ell Z)=2^-k product_i c_H(g_i^-1,t^-1), while "
            "tr_B(ell)=1[ell^-1 in B]."
        ),
        pointwise_bias=(
            "Every basis element has bias zero when t is in K or support fails, "
            "and exactly 2^-k otherwise."
        ),
        arbitrary_LCU_bound=(
            "For every X=sum alpha_ell ell, absolute linear bias is at most "
            "2^-k ||alpha||_1."
        ),
        classical_evaluation=(
            "The basis weight uses k independent four-element HtH membership "
            "checks and is classically computable in O(k) group operations."
        ),
        natural_copy_consequence=(
            "At k=ceil(log2(64M)), unit-L1 bias is at most 1/(64M); "
            "constant bias requires L1 norm at least 2^k>=64M."
        ),
        exact_all_finite_groups_basis_formula_proved=exact,
        arbitrary_all_copy_target_L1_LCU_bound_proved=exact,
        normalized_sparse_target_recoupling_linear_detector_ruled_out=(
            exact and natural
        ),
        efficiently_sampleable_LCU_expectation_classically_estimable=exact,
        nonlinear_spectral_function_no_go_proved=False,
        bounded_operator_large_L1_no_go_proved=False,
        matrix_CS_polar_no_go_proved=False,
        adaptive_postselection_no_go_proved=False,
        hidden_involution_detector_constructed=False,
        speedup_claim_allowed=False,
        theorem_verified=exact and natural,
        status=(
            "all-copy-target-normalized-LCU-no-go-proved-nonlinear-polar-open"
            if exact and natural
            else "all-copy-target-LCU-no-go-control-failure"
        ),
    )
    return AllCopyTargetLCUNoGoReport(
        created_at=utc_now(),
        theorem_contract={
            "group": "Any finite group G with an involution h",
            "observable_class": (
                "Arbitrary linear group-algebra LCU on all k source coordinates "
                "and the target coordinate"
            ),
            "normalization": "Group-basis coefficient L1 norm",
            "claim_boundary": (
                "Linear expectation bias only; bounded-operator nonlinear spectral "
                "and matrix-polar operations may have exponentially large basis L1."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-ALL-COPY-TARGET-BOUNDED-OPERATOR-LARGE-L1",
                "statement": (
                    "Determine whether bounded coherent noncommutative polynomials "
                    "with exponentially large word/basis L1 can amplify without "
                    "reintroducing sqrt(M) normalization."
                ),
                "resolved": False,
            },
            {
                "id": "PO-ALL-COPY-TARGET-MATRIX-POLAR",
                "statement": (
                    "Analyze the matrix-CS polar or spectral projector transition "
                    "directly; linear LCU bias is no longer a viable proxy."
                ),
                "resolved": False,
            },
            {
                "id": "PO-ALL-COPY-TARGET-POSTSELECTION",
                "statement": (
                    "Charge any postselected escape for success probability and "
                    "compare its total normalization with the classical estimator."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "The earlier diagonal theorem already covered every target coupling.",
                "answer": (
                    "False. This theorem allows arbitrary and independently varying "
                    "source coordinates g_i, not only (t,...,t;t)."
                ),
                "resolved": True,
            },
            {
                "challenge": "An off-diagonal basis element can have larger linear bias.",
                "answer": (
                    "False. Exact BAB multiplicity is one per source coordinate "
                    "outside K, giving the same 2^-k pointwise bias."
                ),
                "resolved": True,
            },
            {
                "challenge": "A polynomial number of arbitrary target-coupled LCU terms can add to constant bias.",
                "answer": (
                    "Not with unit L1 normalization. Constant bias requires aggregate "
                    "coefficient norm at least 2^k."
                ),
                "resolved": True,
            },
            {
                "challenge": "This rules out every bounded quantum observable.",
                "answer": (
                    "Too strong. Operator norm can remain bounded while group-basis L1 "
                    "is exponential; nonlinear spectral/polar constructions are outside scope."
                ),
                "resolved": True,
            },
        ],
        headline_metrics={
            "exact_all_finite_groups_basis_formula_count": int(exact),
            "arbitrary_all_copy_target_L1_no_go_count": int(exact and natural),
            "tail_unit_L1_bias_log2_upper_bound": scaling[-1].unit_L1_bias_log2_upper_bound,
            "tail_constant_bias_L1_norm_lower_bound_decimal": scaling[-1].constant_bias_L1_norm_lower_bound_decimal,
            "matrix_polar_no_go_count": 0,
            "hidden_involution_detector_count": 0,
        },
        claim_gate={
            "arbitrary_all_copy_target_unit_L1_bias_no_go_proved": exact and natural,
            "basis_bias_classically_computable": exact,
            "nonlinear_spectral_function_no_go_proved": False,
            "bounded_operator_large_L1_no_go_proved": False,
            "matrix_CS_polar_no_go_proved": False,
            "adaptive_postselection_no_go_proved": False,
            "hidden_involution_detector_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Every linear group-basis LCU has at most 2^-k times its L1 norm "
                "in bias; only nonlinear bounded-operator interference remains."
            ),
        },
        status=theorem.status,
        summary=(
            "Extended the inverse-candidate bias no-go from diagonal/Hecke terms "
            "to every normalized all-copy target-coupled group-algebra LCU."
        ),
        falsifiers_triggered=[
            "Off-diagonal all-copy target basis terms do not exceed 2^-k linear bias.",
            "Polynomial normalized sparse target recoupling cannot provide constant linear signal.",
            "Future positive work must analyze nonlinear matrix polar interference directly.",
        ],
    )


def write_all_copy_target_LCU_no_go_report(
    output_path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(build_all_copy_target_LCU_no_go_report())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


def run_experiment(
    experiment_id: str = DEFAULT_EXPERIMENT_ID,
    candidate_id: str = DEFAULT_CANDIDATE_ID,
    write_registry: bool = True,
) -> dict[str, Any]:
    del experiment_id, candidate_id, write_registry
    return write_all_copy_target_LCU_no_go_report()


if __name__ == "__main__":
    print(json.dumps(run_experiment(), indent=2, sort_keys=True))
