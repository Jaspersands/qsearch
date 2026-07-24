"""Exact orbit-state transfer for higher-multiplicity typical commutants.

For the fixed n=8 source ``(4,2,1,1)``, the simultaneous-conjugacy action on
pairs of permutations has only 43,206 states.  The companion exact C++ kernel
propagates the normalized operator

    H = TT1 + TC1

through degree 17 without enumerating operator words separately.  Character
contraction then recovers complete characteristic polynomials for every
nontrivial target of the n=8 source.

All 20 targets have square-free exact characteristic polynomials.  This is a
coefficient-1 finite certificate, not a parameterized theorem, an all-n gap
result, a coherent transform, or a decoder.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import shutil
import subprocess
import tempfile
from collections import defaultdict
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path

import numpy as np
import sympy as sp

from coset_typical_commutant_moment_audit import (
    _group_workspace,
    _right_product_type_ids,
)
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from symmetric_character import symmetric_character


COSET_TYPICAL_HIGH_MULTIPLICITY_TRANSFER_PATH = Path(
    "research/representation/coset_typical_high_multiplicity_transfer.json"
)
TRANSFER_KERNEL_PATH = Path("tools/pair_orbit_transfer.cpp")
DEFAULT_EXPERIMENT_ID = "EXP-COSET-TYPICAL-HIGH-MULTIPLICITY-TRANSFER"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

N = 8
SOURCE_PARTITION = (4, 2, 1, 1)
NONTRIVIAL_TARGET_COUNT = 20
EIGENVALUE = sp.symbols("x", real=True)

TRANSFER_STATE_COUNTS = {
    1: 2,
    2: 87,
    3: 1657,
    4: 8193,
    5: 16492,
    **{
        degree: 21614 if degree % 2 == 0 else 21592
        for degree in range(6, 18)
    },
}
TRANSFER_TOTAL_WEIGHTS = {
    degree: 2 * 3360 ** (degree - 1) for degree in range(1, 18)
}


def _fractions(*values: str) -> tuple[Fraction, ...]:
    return tuple(Fraction(value) for value in values)


PRIMARY_TARGET_CERTIFICATES = (
    {
        "primary": (7, 1),
        "conjugate": (2, 1, 1, 1, 1, 1, 1),
        "dimension": 7,
        "multiplicity": 2,
        "traces": _fractions("1/21", "3/2450"),
    },
    {
        "primary": (6, 2),
        "conjugate": (2, 2, 1, 1, 1, 1),
        "dimension": 20,
        "multiplicity": 5,
        "traces": _fractions(
            "9/112",
            "23621/2822400",
            "4631/35123200",
            "171764657/7965941760000",
            "206219633/535311286272000",
        ),
    },
    {
        "primary": (6, 1, 1),
        "conjugate": (3, 1, 1, 1, 1, 1),
        "dimension": 21,
        "multiplicity": 4,
        "traces": _fractions(
            "29/336",
            "20849/2822400",
            "28739/135475200",
            "18582359/1137991680000",
        ),
    },
    {
        "primary": (5, 3),
        "conjugate": (2, 2, 2, 1, 1),
        "dimension": 28,
        "multiplicity": 6,
        "traces": _fractions(
            "13/336",
            "9091/940800",
            "43759/135475200",
            "251217329/7965941760000",
            "902837389/535311286272000",
            "329198685793/2498119335936000000",
        ),
    },
    {
        "primary": (5, 1, 1, 1),
        "conjugate": (4, 1, 1, 1, 1),
        "dimension": 35,
        "multiplicity": 6,
        "traces": _fractions(
            "37/336",
            "59809/2822400",
            "904957/948326400",
            "152746103/1137991680000",
            "5445665081/535311286272000",
            "25913815286497/22483074023424000000",
        ),
    },
    {
        "primary": (4, 4),
        "conjugate": (2, 2, 2, 2),
        "dimension": 14,
        "multiplicity": 4,
        "traces": _fractions(
            "1/24",
            "997/141120",
            "5233/16934400",
            "2998589/99574272000",
        ),
    },
)

HIGH_MULTIPLICITY_TARGET_CERTIFICATES = (
    {
        "primary": (5, 2, 1),
        "conjugate": (3, 2, 1, 1, 1),
        "dimension": 64,
        "multiplicity": 13,
        "traces": _fractions(
            "53/336",
            "77299/2822400",
            "652541/948326400",
            "830148787/7965941760000",
            "703525351/178437095424000",
            "10979172159379/22483074023424000000",
            "185642516660101/7554312871870464000000",
            "164218169710111331/63456228123711897600000000",
            "3357804172238006657/21321292649567197593600000000",
            "887122340859039803473/59699619418788153262080000000000",
            "6808990705636387216037/6686357374904273165352960000000000",
            "45404841009149057261304211/505488617542763051300683776000000000000",
            "374105461738874744923005139/56614725164789461745676582912000000000000",
        ),
    },
    {
        "primary": (4, 3, 1),
        "conjugate": (3, 2, 2, 1),
        "dimension": 70,
        "multiplicity": 14,
        "traces": _fractions(
            "31/336",
            "78637/2822400",
            "936013/948326400",
            "1000958801/7965941760000",
            "4237852433/535311286272000",
            "17592479620081/22483074023424000000",
            "459173394718853/7554312871870464000000",
            "50405815320776311/9065175446244556800000000",
            "9971686108313411413/21321292649567197593600000000",
            "2498740641590611370779/59699619418788153262080000000000",
            "218980502424147063362981/60177216374138458488176640000000000",
            "163939945527687991236692321/505488617542763051300683776000000000000",
            "4863638575468891551064345333/169844175494368385237029748736000000000000",
            "3645672647874824084900580505201/1426691074152694435991049889382400000000000000",
        ),
    },
    {
        "primary": (4, 2, 2),
        "conjugate": (3, 3, 1, 1),
        "dimension": 56,
        "multiplicity": 12,
        "traces": _fractions(
            "5/336",
            "7807/188160",
            "-248387/189665280",
            "503176327/1137991680000",
            "-5389467913/178437095424000",
            "36581802937/5664669696000000",
            "-1505411636653109/2518104290623488000000",
            "2188538321406730763/21152076041237299200000000",
            "-47617392964267363019/4264258529913439518720000000",
            "8811974289712208598563/5117110235896127422464000000000",
            "-12179282681851655537490703/60177216374138458488176640000000000",
            "14777021708363523619544563633/505488617542763051300683776000000000000",
        ),
    },
    {
        "primary": (4, 2, 1, 1),
        "conjugate": (4, 2, 1, 1),
        "dimension": 90,
        "multiplicity": 17,
        "traces": _fractions(
            "0",
            "5147/94080",
            "0",
            "2029850177/3982970880000",
            "0",
            "918878628377/138784407552000000",
            "0",
            "2983003177994099809/31728114061855948800000000",
            "0",
            "4897063092039010267841/3581977165127289195724800000000",
            "0",
            "5057671627159827630415730321/252744308771381525650341888000000000000",
            "0",
            "4651917016693079627299475507533/15852123046141049288789443215360000000000000",
            "0",
            "8669227952639728062499416054620773057/2013346443844282388070569603896442880000000000000000",
            "0",
        ),
    },
    {
        "primary": (3, 3, 2),
        "conjugate": (3, 3, 2),
        "dimension": 42,
        "multiplicity": 8,
        "traces": _fractions(
            "0",
            "11003/352800",
            "0",
            "74011361/248935680000",
            "0",
            "599144691287/175649015808000000",
            "0",
            "5000784785569889/123937945554124800000000",
        ),
    },
)

TARGET_CERTIFICATES = (
    *PRIMARY_TARGET_CERTIFICATES,
    *HIGH_MULTIPLICITY_TARGET_CERTIFICATES,
)


def _family_targets(family: dict[str, object]) -> tuple[tuple[int, ...], ...]:
    primary = family["primary"]
    conjugate = family["conjugate"]
    if not isinstance(primary, tuple) or not isinstance(conjugate, tuple):
        raise TypeError("certificate targets must be tuple partitions")
    return (primary,) if primary == conjugate else (primary, conjugate)


@dataclass(frozen=True)
class HighMultiplicityTargetRecord:
    n: int
    source_partition: tuple[int, ...]
    target_partition: tuple[int, ...]
    target_dimension: int
    kronecker_multiplicity: int
    coefficient_rule: dict[str, int]
    exact_power_traces: list[str]
    exact_characteristic_polynomial: str
    exact_discriminant: str
    exact_square_free_gcd: str
    characteristic_polynomial_square_free: bool
    sign_twist_transfer_used: bool
    exact_transfer_recomputed: bool
    status: str


@dataclass(frozen=True)
class HighMultiplicityTransferReport:
    created_at: str
    theorem_contract: dict[str, object]
    transfer_kernel: dict[str, object]
    records: list[HighMultiplicityTargetRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _characteristic_polynomial(power_traces: tuple[Fraction, ...]) -> sp.Expr:
    elementary = [Fraction(1)]
    for degree in range(1, len(power_traces) + 1):
        elementary.append(
            sum(
                (-1) ** (index - 1)
                * elementary[degree - index]
                * power_traces[index - 1]
                for index in range(1, degree + 1)
            )
            / degree
        )
    return sp.factor(
        sum(
            (-1) ** degree
            * sp.Rational(value.numerator, value.denominator)
            * EIGENVALUE ** (len(power_traces) - degree)
            for degree, value in enumerate(elementary)
        )
    )


def _unpack_pair(key: int) -> tuple[tuple[int, ...], tuple[int, ...]]:
    left = tuple((key >> (4 * index)) & 15 for index in range(N))
    right = tuple((key >> (4 * N + 4 * index)) & 15 for index in range(N))
    return left, right


def run_exact_transfer_kernel(
    max_degree: int = 17,
    n: int = N,
    threads: int | None = None,
    cache_path: Path | None = None,
) -> tuple[dict[int, dict[int, int]], str]:
    if max_degree < 1 or max_degree > 32:
        raise ValueError("the arbitrary-precision kernel supports degrees 1 through 32")
    if n not in {8, 9, 10}:
        raise ValueError("the audited exact kernel currently supports n=8, n=9, or n=10")
    if not TRANSFER_KERNEL_PATH.exists():
        raise FileNotFoundError(TRANSFER_KERNEL_PATH)
    thread_count = threads or max(1, min(8, os.cpu_count() or 1))
    if thread_count < 1 or thread_count > 64:
        raise ValueError("threads must be between 1 and 64")
    kernel_digest = hashlib.sha256(TRANSFER_KERNEL_PATH.read_bytes()).hexdigest()
    metadata_path = (
        cache_path.with_suffix(cache_path.suffix + ".meta.json")
        if cache_path is not None
        else None
    )
    cache_valid = False
    if cache_path is not None and cache_path.exists() and metadata_path is not None:
        try:
            metadata = json.loads(metadata_path.read_text())
            cache_valid = (
                metadata.get("n") == n
                and int(metadata.get("maximum_degree", 0)) >= max_degree
                and metadata.get("kernel_sha256") == kernel_digest
            )
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            cache_valid = False

    if cache_valid:
        diagnostics = f"loaded exact transfer cache {cache_path}"
        lines = cache_path.open()
    else:
        compiler = (
            os.environ.get("CXX") or shutil.which("clang++") or shutil.which("g++")
        )
        if not compiler:
            raise RuntimeError("an available C++17 compiler is required for recomputation")
        with tempfile.TemporaryDirectory(prefix="qsearch-pair-transfer-") as directory:
            binary = Path(directory) / "pair_orbit_transfer"
            subprocess.run(
                [
                    compiler,
                    "-std=c++17",
                    "-O3",
                    "-DNDEBUG",
                    "-pthread",
                    f"-DQSEARCH_N={n}",
                    str(TRANSFER_KERNEL_PATH),
                    "-o",
                    str(binary),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            command = [
                str(binary),
                "--max-degree",
                str(max_degree),
                "--threads",
                str(thread_count),
            ]
            if cache_path is None:
                completed = subprocess.run(
                    command,
                    check=True,
                    capture_output=True,
                    text=True,
                )
                diagnostics = completed.stderr
                lines = completed.stdout.splitlines()
            else:
                cache_path.parent.mkdir(parents=True, exist_ok=True)
                with cache_path.open("w") as output:
                    completed = subprocess.run(
                        command,
                        check=True,
                        stdout=output,
                        stderr=subprocess.PIPE,
                        text=True,
                    )
                metadata_path.write_text(
                    json.dumps(
                        {
                            "n": n,
                            "maximum_degree": max_degree,
                            "kernel_sha256": kernel_digest,
                            "threads": thread_count,
                        },
                        indent=2,
                        sort_keys=True,
                    )
                )
                diagnostics = completed.stderr
                lines = cache_path.open()
    distributions: defaultdict[int, dict[int, int]] = defaultdict(dict)
    try:
        for line in lines:
            degree_text, key_text, weight_text = line.rstrip().split("\t")
            degree = int(degree_text)
            if degree <= max_degree:
                distributions[degree][int(key_text, 16)] = int(weight_text)
    finally:
        if hasattr(lines, "close"):
            lines.close()
    if max(distributions, default=0) != max_degree:
        raise ArithmeticError("exact transfer output is missing the requested degree")
    known_state_counts = {
        8: TRANSFER_STATE_COUNTS,
        9: {1: 2, 2: 87, 3: 2070, 4: 26062},
        10: {1: 2, 2: 87},
    }[n]
    orbit_size = n * (n - 1) * (n - 2) * (n - 3)
    for degree, distribution in distributions.items():
        if degree in known_state_counts and len(distribution) != known_state_counts[degree]:
            raise ArithmeticError(f"unexpected exact state count at degree {degree}")
        if sum(distribution.values()) != 2 * (2 * orbit_size) ** (degree - 1):
            raise ArithmeticError(f"unexpected exact transfer weight at degree {degree}")
    return dict(distributions), diagnostics


def contract_transfer_traces(
    distributions: dict[int, dict[int, int]],
) -> dict[tuple[int, ...], tuple[Fraction, ...]]:
    targets = tuple(
        target
        for family in TARGET_CERTIFICATES
        for target in _family_targets(family)
    )
    cycle_types, _, _, group_type_ids = _group_workspace(N)
    source_characters = np.array(
        [symmetric_character(SOURCE_PARTITION, value) for value in cycle_types],
        dtype=np.int64,
    )
    target_characters = np.array(
        [
            [symmetric_character(target, value) for value in cycle_types]
            for target in targets
        ],
        dtype=np.int64,
    )
    all_keys = set().union(*(set(rows) for rows in distributions.values()))
    contraction_cache: dict[int, tuple[int, ...]] = {}
    for key in all_keys:
        left, right = _unpack_pair(key)
        left_types = _right_product_type_ids(N, left)
        right_types = _right_product_type_ids(N, right)
        weights = source_characters[left_types] * source_characters[right_types]
        class_sums = np.bincount(
            group_type_ids,
            weights=weights,
            minlength=len(cycle_types),
        ).astype(np.int64)
        contraction_cache[key] = tuple(
            int(value) for value in target_characters @ class_sums
        )

    traces: dict[tuple[int, ...], tuple[Fraction, ...]] = {}
    for target_index, (target, family) in enumerate(
        (target, family)
        for family in TARGET_CERTIFICATES
        for target in _family_targets(family)
    ):
        multiplicity = int(family["multiplicity"])
        rows = []
        for degree in range(1, multiplicity + 1):
            numerator = sum(
                weight * contraction_cache[key][target_index]
                for key, weight in distributions[degree].items()
            )
            rows.append(
                Fraction(
                    numerator,
                    math.factorial(N) * 1680 ** (degree - 1),
                )
            )
        traces[target] = tuple(rows)
    _right_product_type_ids.cache_clear()
    return traces


def _stored_traces() -> dict[tuple[int, ...], tuple[Fraction, ...]]:
    rows: dict[tuple[int, ...], tuple[Fraction, ...]] = {}
    for family in TARGET_CERTIFICATES:
        primary = family["primary"]
        conjugate = family["conjugate"]
        traces = family["traces"]
        rows[primary] = traces
        if conjugate != primary:
            rows[conjugate] = tuple(
                (-1) ** degree * value
                for degree, value in enumerate(traces, start=1)
            )
    return rows


def build_high_multiplicity_transfer_report(
    recompute: bool = False,
) -> HighMultiplicityTransferReport:
    transfer_stderr = "stored exact transfer certificate"
    if recompute:
        distributions, transfer_stderr = run_exact_transfer_kernel(max_degree=17)
        traces_by_target = contract_transfer_traces(distributions)
        if traces_by_target != _stored_traces():
            raise ArithmeticError("recomputed transfer traces differ from certificate")
    else:
        traces_by_target = _stored_traces()

    records: list[HighMultiplicityTargetRecord] = []
    for family in TARGET_CERTIFICATES:
        for target in _family_targets(family):
            traces = traces_by_target[target]
            polynomial = _characteristic_polynomial(traces)
            polynomial_object = sp.Poly(polynomial, EIGENVALUE)
            square_free_gcd = sp.gcd(
                polynomial_object,
                polynomial_object.diff(),
            )
            square_free = square_free_gcd.degree() == 0
            if not square_free:
                raise ArithmeticError(f"exact repeated root found on target {target}")
            discriminant = (
                str(sp.factor(sp.discriminant(polynomial, EIGENVALUE)))
                if int(family["multiplicity"]) <= 6
                else "nonzero-certified-by-exact-gcd"
            )
            records.append(
                HighMultiplicityTargetRecord(
                    n=N,
                    source_partition=SOURCE_PARTITION,
                    target_partition=target,
                    target_dimension=int(family["dimension"]),
                    kronecker_multiplicity=int(family["multiplicity"]),
                    coefficient_rule={
                        "ORB-TT-INTERSECTION-1": 1,
                        "ORB-TC-INTERSECTION-1": 1,
                    },
                    exact_power_traces=[str(value) for value in traces],
                    exact_characteristic_polynomial=str(polynomial),
                    exact_discriminant=discriminant,
                    exact_square_free_gcd=str(square_free_gcd.as_expr()),
                    characteristic_polynomial_square_free=square_free,
                    sign_twist_transfer_used=(
                        target == family["conjugate"]
                        and family["primary"] != family["conjugate"]
                    ),
                    exact_transfer_recomputed=recompute,
                    status="exact-coefficient-one-simple-spectrum",
                )
            )
    metrics: dict[str, int | float] = {
        "maximum_exact_transfer_degree": 17,
        "maximum_exact_transfer_state_count": max(TRANSFER_STATE_COUNTS.values()),
        "total_simultaneous_conjugacy_pair_state_count": 43206,
        "certified_n8_target_count": len(records),
        "certified_n8_simple_spectrum_target_count": sum(
            record.characteristic_polynomial_square_free for record in records
        ),
        "n8_nontrivial_multiplicity_target_count": NONTRIVIAL_TARGET_COUNT,
        "n8_unaudited_multiplicity_above_six_target_count": 0,
        "n8_unaudited_target_count": NONTRIVIAL_TARGET_COUNT - len(records),
        "maximum_certified_kronecker_multiplicity": max(
            record.kronecker_multiplicity for record in records
        ),
        "n8_exact_target_coverage_fraction": len(records)
        / NONTRIVIAL_TARGET_COUNT,
        "exact_transfer_recomputed_count": int(recompute),
        "all_n8_fixed_coefficient_simple_spectrum_theorem_count": int(
            len(records) == NONTRIVIAL_TARGET_COUNT
            and all(record.characteristic_polynomial_square_free for record in records)
        ),
        "parameterized_all_coefficient_theorem_count": 0,
        "all_n_simple_spectrum_theorem_count": 0,
        "inverse_polynomial_gap_theorem_count": 0,
        "coherent_typical_multiplicity_transform_count": 0,
        "typical_label_hidden_involution_decoder_count": 0,
    }
    return HighMultiplicityTransferReport(
        created_at=utc_now(),
        theorem_contract={
            "transfer_identity": (
                "At coefficient c=1, use integer transition 5*sum(TT1 orbit)+sum(TC1 orbit) with denominator 1680 per additional power."
            ),
            "state_quotient": (
                "Canonicalize permutation pairs under simultaneous conjugation; S_8 has exactly 43,206 such states."
            ),
            "character_contraction": (
                "Contract each exact transfer distribution with the target central character projector and recover the characteristic polynomial by Newton identities."
            ),
            "scope": (
                "One n=8 source, fixed coefficient c=1, all 20 nontrivial Kronecker multiplicity targets through multiplicity 17."
            ),
            "parameterized_claimed": False,
            "asymptotic_claimed": False,
            "algorithmic_speedup_claimed": False,
        },
        transfer_kernel={
            "source": str(TRANSFER_KERNEL_PATH),
            "language": "C++17",
            "integer_width": "boost::multiprecision::cpp_int through degree 17",
            "state_counts": TRANSFER_STATE_COUNTS,
            "total_weights": TRANSFER_TOTAL_WEIGHTS,
            "recomputed": recompute,
            "diagnostics": transfer_stderr.strip(),
        },
        records=records,
        headline_metrics=metrics,
        claim_gate={
            "fixed_coefficient_c1_viable_through_multiplicity_six": True,
            "fixed_coefficient_c1_viable_on_all_n8_targets": True,
            "all_n8_targets_audited": True,
            "parameterized_common_coefficient_proved": False,
            "all_n_simple_spectrum_proved": False,
            "inverse_polynomial_gap_proved": False,
            "coherent_transform_proved": False,
            "hidden_involution_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Coefficient c=1 has exact simple spectrum on all 20 n=8 targets, but parameter robustness, adjacent sizes, all-n normalized gaps, implementation, and decoding remain open."
            ),
        },
        status="fixed-coefficient-exactly-separates-all-n8-targets-asymptotic-obligations-open",
        summary=(
            "Exact orbit-state transfer proves TT1+TC1 has simple spectrum on all 20 nontrivial n=8 targets through multiplicity 17; no asymptotic or algorithmic claim follows."
        ),
        falsifiers_triggered=[
            "The tested fixed coefficient does not fail on any n=8 multiplicity block through multiplicity 17.",
            "Parameterized nonzero-coefficient robustness is not established beyond multiplicity four.",
            "A complete n=8 finite theorem does not establish adjacent-size or all-n behavior.",
            "Finite square-freeness does not prove a normalized gap, coherent transform, decoder, or speedup.",
        ],
    )


def write_high_multiplicity_transfer_report(
    output_path: Path = COSET_TYPICAL_HIGH_MULTIPLICITY_TRANSFER_PATH,
    recompute: bool = False,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(build_high_multiplicity_transfer_report(recompute=recompute))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-TYPICAL-N8-FULL-SEPARATION-NOT-ASYMPTOTIC-GAP",
                source=str(output_path),
                claim=(
                    "A fixed coefficient exactly separating every n=8 target establishes a uniform typical-irrep resolver."
                ),
                reason_invalid=(
                    "The theorem covers one source size and coefficient; parameter robustness, adjacent sizes, all-n normalized gaps, coherent implementation, and decoding are absent."
                ),
                lesson=(
                    "Move immediately to n=9 and coefficient perturbations. Reject the mechanism on the first repeated root or superpolynomial normalized-gap trend."
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
                    "coset_typical_high_multiplicity_transfer": str(output_path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_high_multiplicity_transfer_report(recompute=True)
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
