"""Exact n=8 repair certificate for an independent commutant generator.

The TC2/TT1 portfolio and its disjoint-transposition extension have exact
repeated-root collisions on the multiplicity-four targets ``(4,4)`` and
``(2,2,2,2)``.  An exact orbit-word contraction for

    TT1 + c * TC1

where TC1 is the transposition/3-cycle intersection-one orbit average,
produces a characteristic polynomial whose discriminant is strictly positive
for every real ``c != 0``.  Sign-twist symmetry transfers the result between
the conjugate targets.

The same exact fourth-order word basis determines every n=8 characteristic
polynomial whose Kronecker multiplicity is at most four.  All six such targets
have positive discriminant for every real ``c != 0``.  This is still only a
finite low-multiplicity audit.  It does not prove the 14 higher-multiplicity
targets, all-n coverage, inverse-polynomial gaps, a coherent transform, or a
hidden-involution decoder.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

import sympy as sp

from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


COSET_TYPICAL_INDEPENDENT_THIRD_GENERATOR_PATH = Path(
    "research/representation/"
    "coset_typical_independent_third_generator_certificate.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-TYPICAL-INDEPENDENT-THIRD-GENERATOR-CERTIFICATE"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

PARAMETER = sp.symbols("c", real=True)
EIGENVALUE = sp.symbols("x", real=True)

SOURCE_PARTITION = (4, 2, 1, 1)
PRIMARY_TARGET = (4, 4)
CONJUGATE_TARGET = (2, 2, 2, 2)
LOW_MULTIPLICITY_TARGET_COUNT = 6
NONTRIVIAL_TARGET_COUNT = 20

EXACT_PRIMARY_POWER_TRACES = (
    sp.Rational(1, 24),
    (192 * PARAMETER**2 + 805) / 141120,
    -(192 * PARAMETER**2 - 5425) / 16934400,
    (67584 * PARAMETER**4 + 474880 * PARAMETER**2 + 2456125)
    / 99574272000,
)

EXPECTED_PRIMARY_CHARACTERISTIC_POLYNOMIAL = sp.factor(
    (
        8 * PARAMETER**4
        - 88200 * PARAMETER**2 * EIGENVALUE**2
        + 4165 * PARAMETER**2 * EIGENVALUE
        + 129654000 * EIGENVALUE**4
        - 5402250 * EIGENVALUE**3
        - 257250 * EIGENVALUE**2
    )
    / 129654000
)

DISCRIMINANT_POSITIVITY_POLYNOMIAL = (
    14155776 * PARAMETER**8
    - 81008640 * PARAMETER**6
    + 2751845760 * PARAMETER**4
    + 46879054250 * PARAMETER**2
    + 17814103125
)
EXPECTED_DISCRIMINANT = sp.factor(
    PARAMETER**4
    * DISCRIMINANT_POSITIVITY_POLYNOMIAL
    / 307443566190200832000000000
)

LOW_MULTIPLICITY_FAMILIES = (
    {
        "primary": (7, 1),
        "conjugate": (2, 1, 1, 1, 1, 1, 1),
        "dimension": 7,
        "multiplicity": 2,
        "power_traces": (
            sp.Rational(1, 21),
            (2 * PARAMETER**2 + 25) / 22050,
        ),
        "expected_discriminant": 2 * PARAMETER**2 / 11025,
        "positivity_proof": "positive-monomial-in-c-squared",
    },
    {
        "primary": (6, 1, 1),
        "conjugate": (3, 1, 1, 1, 1, 1),
        "dimension": 21,
        "multiplicity": 4,
        "power_traces": (
            sp.Rational(29, 336),
            (1024 * PARAMETER**2 + 19825) / 2822400,
            (27648 * PARAMETER**2 + 173525) / 948326400,
            (
                524288 * PARAMETER**4
                + 21401600 * PARAMETER**2
                + 108150625
            )
            / 7965941760000,
        ),
        "expected_discriminant": sp.factor(
            PARAMETER**4
            * (
                8388608 * PARAMETER**6
                + 54476800 * PARAMETER**4
                + 6529740000 * PARAMETER**2
                + 3810515625
            )
            / 2732831699468451840000000000
        ),
        "positivity_proof": "strictly-positive-coefficients-in-c-squared",
    },
    {
        "primary": PRIMARY_TARGET,
        "conjugate": CONJUGATE_TARGET,
        "dimension": 14,
        "multiplicity": 4,
        "power_traces": EXACT_PRIMARY_POWER_TRACES,
        "expected_discriminant": EXPECTED_DISCRIMINANT,
        "positivity_proof": "negative-quadratic-discriminant-decomposition",
    },
)


@dataclass(frozen=True)
class IndependentThirdGeneratorTargetRecord:
    n: int
    source_partition: tuple[int, ...]
    source_dimension: int
    target_partition: tuple[int, ...]
    target_dimension: int
    kronecker_multiplicity: int
    base_generator_id: str
    independent_generator_id: str
    exact_parameterized_power_traces: list[str]
    exact_parameterized_characteristic_polynomial: str
    exact_parameterized_discriminant: str
    discriminant_positivity_proof: str
    discriminant_zero_coefficient_condition: str
    every_nonzero_real_coefficient_simple_spectrum: bool
    sign_twist_transfer_used: bool
    exact_orbit_word_state_counts: list[int]
    exact_contraction_cache_size: int
    finite_collision_repaired: bool
    status: str


@dataclass(frozen=True)
class IndependentThirdGeneratorReport:
    created_at: str
    theorem_contract: dict[str, object]
    positivity_certificate: dict[str, object]
    records: list[IndependentThirdGeneratorTargetRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _newton_characteristic_polynomial(
    power_traces: tuple[sp.Expr, ...],
) -> sp.Expr:
    elementary: list[sp.Expr] = [sp.Integer(1)]
    for degree in range(1, len(power_traces) + 1):
        elementary.append(
            sp.factor(
                sum(
                    (-1) ** (index - 1)
                    * elementary[degree - index]
                    * power_traces[index - 1]
                    for index in range(1, degree + 1)
                )
                / degree
            )
        )
    return sp.factor(
        sum(
            (-1) ** degree
            * elementary[degree]
            * EIGENVALUE ** (len(power_traces) - degree)
            for degree in range(len(power_traces) + 1)
        )
    )


def _positivity_certificate() -> dict[str, object]:
    z = sp.symbols("z", nonnegative=True)
    quadratic_a = 14155776
    quadratic_b = -81008640
    quadratic_c = 2751845760
    quadratic_discriminant = (
        quadratic_b**2 - 4 * quadratic_a * quadratic_c
    )
    rewritten = (
        z**2
        * (quadratic_a * z**2 + quadratic_b * z + quadratic_c)
        + 46879054250 * z
        + 17814103125
    )
    expected = DISCRIMINANT_POSITIVITY_POLYNOMIAL.subs(PARAMETER**2, z)
    if sp.expand(rewritten - expected) != 0:
        raise ArithmeticError("invalid discriminant positivity decomposition")
    if quadratic_discriminant >= 0 or quadratic_a <= 0:
        raise ArithmeticError("quadratic factor is not certified positive")
    return {
        "audited_family_count": len(LOW_MULTIPLICITY_FAMILIES),
        "audited_target_count": LOW_MULTIPLICITY_TARGET_COUNT,
        "positive_monomial_family_count": 1,
        "positive_coefficient_family_count": 1,
        "negative_quadratic_discriminant_family_count": 1,
        "substitution": "z=c^2>=0",
        "positive_quadratic_leading_coefficient": quadratic_a,
        "quadratic_discriminant": quadratic_discriminant,
        "quadratic_positive_for_all_real_z": True,
        "remaining_linear_coefficient": 46879054250,
        "remaining_constant": 17814103125,
        "discriminant_positive_for_every_nonzero_real_c": True,
    }


def _target_record(
    family: dict[str, object],
    target: tuple[int, ...],
) -> IndependentThirdGeneratorTargetRecord:
    primary_target = family["primary"]
    conjugate_target = family["conjugate"]
    primary_traces = family["power_traces"]
    expected_discriminant = family["expected_discriminant"]
    if not isinstance(primary_target, tuple) or not isinstance(
        conjugate_target, tuple
    ):
        raise TypeError("target families must use tuple partitions")
    if not isinstance(primary_traces, tuple):
        raise TypeError("power traces must be an exact tuple")
    primary_polynomial = _newton_characteristic_polynomial(primary_traces)
    if primary_target == PRIMARY_TARGET and sp.expand(
        primary_polynomial - EXPECTED_PRIMARY_CHARACTERISTIC_POLYNOMIAL
    ) != 0:
        raise ArithmeticError("Newton identities did not recover the collision repair")
    primary_discriminant = sp.factor(
        sp.discriminant(primary_polynomial, EIGENVALUE)
    )
    if sp.expand(primary_discriminant - expected_discriminant) != 0:
        raise ArithmeticError("unexpected parameterized discriminant")

    sign_twist = target == conjugate_target
    if target not in {primary_target, conjugate_target}:
        raise ValueError("target is outside the certified conjugate family")
    power_traces = tuple(
        (-1) ** degree * trace if sign_twist else trace
        for degree, trace in enumerate(primary_traces, start=1)
    )
    polynomial = sp.factor(
        primary_polynomial.subs(EIGENVALUE, -EIGENVALUE)
        if sign_twist
        else primary_polynomial
    )
    if sp.expand(
        polynomial - _newton_characteristic_polynomial(power_traces)
    ) != 0:
        raise ArithmeticError("sign-twist trace transfer is inconsistent")
    discriminant = sp.factor(sp.discriminant(polynomial, EIGENVALUE))
    if sp.expand(discriminant - expected_discriminant) != 0:
        raise ArithmeticError("conjugate-target discriminant changed")

    return IndependentThirdGeneratorTargetRecord(
        n=8,
        source_partition=SOURCE_PARTITION,
        source_dimension=90,
        target_partition=target,
        target_dimension=int(family["dimension"]),
        kronecker_multiplicity=int(family["multiplicity"]),
        base_generator_id="ORB-TT-INTERSECTION-1",
        independent_generator_id="ORB-TC-INTERSECTION-1",
        exact_parameterized_power_traces=[
            str(sp.factor(trace)) for trace in power_traces
        ],
        exact_parameterized_characteristic_polynomial=str(polynomial),
        exact_parameterized_discriminant=str(discriminant),
        discriminant_positivity_proof=str(family["positivity_proof"]),
        discriminant_zero_coefficient_condition="c=0",
        every_nonzero_real_coefficient_simple_spectrum=True,
        sign_twist_transfer_used=sign_twist,
        exact_orbit_word_state_counts=[2, 87, 1657, 8193],
        exact_contraction_cache_size=9850,
        finite_collision_repaired=True,
        status="exact-finite-simple-spectrum-for-every-nonzero-real-coefficient",
    )


def build_independent_third_generator_report() -> IndependentThirdGeneratorReport:
    positivity = _positivity_certificate()
    records = [
        _target_record(family, target)
        for family in LOW_MULTIPLICITY_FAMILIES
        for target in (family["primary"], family["conjugate"])
    ]
    metrics: dict[str, int | float] = {
        "independent_third_generator_target_count": len(records),
        "exact_parameterized_characteristic_polynomial_certificate_count": len(
            records
        ),
        "exact_parameterized_four_moment_certificate_count": sum(
            record.kronecker_multiplicity == 4 for record in records
        ),
        "nonzero_coefficient_simple_spectrum_target_count": sum(
            record.every_nonzero_real_coefficient_simple_spectrum
            for record in records
        ),
        "certified_n8_collision_target_repair_count": sum(
            record.finite_collision_repaired
            and record.target_partition in {PRIMARY_TARGET, CONJUGATE_TARGET}
            for record in records
        ),
        "certified_n8_low_multiplicity_target_count": len(records),
        "certified_n8_low_multiplicity_simple_spectrum_target_count": sum(
            record.every_nonzero_real_coefficient_simple_spectrum
            for record in records
        ),
        "n8_nontrivial_multiplicity_target_count": NONTRIVIAL_TARGET_COUNT,
        "n8_unaudited_higher_multiplicity_target_count": (
            NONTRIVIAL_TARGET_COUNT - len(records)
        ),
        "maximum_exactly_audited_kronecker_multiplicity": max(
            record.kronecker_multiplicity for record in records
        ),
        "n8_exact_target_coverage_fraction": len(records)
        / NONTRIVIAL_TARGET_COUNT,
        "all_n_simple_spectrum_theorem_count": 0,
        "all_typical_target_coverage_theorem_count": 0,
        "inverse_polynomial_gap_theorem_count": 0,
        "coherent_typical_multiplicity_transform_count": 0,
        "typical_label_hidden_involution_decoder_count": 0,
    }
    return IndependentThirdGeneratorReport(
        created_at=utc_now(),
        theorem_contract={
            "exact_contraction": (
                "An exact orbit-word dynamic program over TT1 and TC1 computed projected power traces through order four on all six n=8 targets of multiplicity at most four."
            ),
            "newton_recovery": (
                "Newton identities recover the degree-four characteristic polynomial exactly from those traces."
            ),
            "positivity_argument": (
                "After z=c^2, the residual discriminant factor is z^2 times a positive quadratic plus a positive linear term and constant; the quadratic has positive leading coefficient and negative discriminant."
            ),
            "sign_twist_transfer": (
                "The self-conjugate source and parity support imply p_k on the conjugate target equals (-1)^k p_k, hence P_conjugate(x,c)=P_primary(-x,c)."
            ),
            "scope": (
                "S_8 source lambda=(4,2,1,1), all six targets with Kronecker multiplicity at most four, operator TT1+c*TC1"
            ),
            "asymptotic_lower_bound_claimed": False,
            "algorithmic_speedup_claimed": False,
        },
        positivity_certificate=positivity,
        records=records,
        headline_metrics=metrics,
        claim_gate={
            "certified_n8_collision_targets_repaired": True,
            "all_n8_low_multiplicity_targets_simple": True,
            "all_n8_higher_multiplicity_targets_audited": False,
            "independent_third_generator_viable_on_certified_targets": True,
            "all_n_simple_spectrum_proved": False,
            "all_typical_targets_covered": False,
            "inverse_polynomial_joint_gap_proved": False,
            "coherent_transform_proved": False,
            "hidden_involution_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "TC1 repairs all six n=8 targets of multiplicity at most four, including the two exact collisions, but 14 higher-multiplicity targets and every larger n remain open; no normalized gap, coherent implementation, or decoder is known."
            ),
        },
        status="finite-collision-repair-proved-global-obligations-blocked",
        summary=(
            "TT1+c*TC1 has exact simple spectrum on all six n=8 targets of multiplicity at most four for every real c!=0; 14 higher-multiplicity targets and all asymptotic obligations remain open."
        ),
        falsifiers_triggered=[
            "The earlier inference that any bounded-support third generator would preserve the n=8 collision is false.",
            "Four exact moments cannot certify the 14 n=8 targets whose multiplicity exceeds four.",
            "Finite repair does not establish all-n joint separation.",
            "Simple spectrum does not establish an inverse-polynomial normalized gap.",
            "No coherent transform or hidden-involution decoder follows from the spectral certificate.",
        ],
    )


def write_independent_third_generator_report(
    output_path: Path = COSET_TYPICAL_INDEPENDENT_THIRD_GENERATOR_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(build_independent_third_generator_report())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-TYPICAL-FINITE-THIRD-GENERATOR-REPAIR-NOT-UNIFORM-GAP",
                source=str(output_path),
                claim=(
                    "The exact n=8 low-multiplicity TC1 certificates are sufficient evidence for a uniform efficient multiplicity measurement."
                ),
                reason_invalid=(
                    "The certificate covers six of 20 nontrivial targets at n=8 and proves neither the 14 higher-multiplicity targets nor all-n coverage, inverse-polynomial normalized gaps, coherent implementation, or decoding."
                ),
                lesson=(
                    "Retain TC1 as the first surviving third generator, but next develop a higher-multiplicity transfer method, test adjacent n, and bound exact parameterized gaps before any algorithmic interpretation."
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
                    "coset_typical_independent_third_generator_certificate": str(
                        output_path
                    )
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_independent_third_generator_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
