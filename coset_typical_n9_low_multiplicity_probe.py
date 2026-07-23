"""Exact n=9 low-multiplicity probe for the fixed TT1+TC1 separator.

The quotient transfer is compiled at degree nine and propagated through order
seven.  A vectorized exact right-translation contraction over S_9 recovers the
complete characteristic polynomial for every target whose Kronecker
multiplicity is at most seven.  All 11 such targets are square-free at the
fixed coefficient c=1.

This audits only 11 of 27 nontrivial n=9 targets.  The other 16 have
multiplicities up to 28 and remain the dominant collision risk.
"""

from __future__ import annotations

import itertools
import json
import math
import tempfile
from collections import defaultdict
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path

import numpy as np
import sympy as sp

from coset_typical_commutant_moment_audit import _cycle_type
from coset_typical_high_multiplicity_transfer import (
    EIGENVALUE,
    run_exact_transfer_kernel,
)
from representation_obstruction import integer_partitions
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from symmetric_character import symmetric_character


COSET_TYPICAL_N9_LOW_MULTIPLICITY_PATH = Path(
    "research/representation/coset_typical_n9_low_multiplicity_probe.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-COSET-TYPICAL-N9-LOW-MULTIPLICITY-PROBE"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

N = 9
SOURCE_PARTITION = (4, 3, 1, 1)
SOURCE_DIMENSION = 216
NONTRIVIAL_TARGET_COUNT = 27
ORBIT_DENOMINATOR = 3024
STATE_COUNTS = {
    1: 2,
    2: 87,
    3: 2070,
    4: 26062,
    5: 78328,
    6: 148830,
    7: 189168,
}


def _fractions(*values: str) -> tuple[Fraction, ...]:
    return tuple(Fraction(value) for value in values)


TARGET_CERTIFICATES = (
    {
        "target": (8, 1),
        "dimension": 8,
        "multiplicity": 2,
        "traces": _fractions("-35/432", "30613/9144576"),
    },
    {
        "target": (7, 1, 1),
        "dimension": 28,
        "multiplicity": 4,
        "traces": _fractions(
            "-439/3024",
            "84185/9144576",
            "-4797229/6913299456",
            "4717802669/83623270219776",
        ),
    },
    {
        "target": (3, 1, 1, 1, 1, 1, 1),
        "dimension": 28,
        "multiplicity": 4,
        "traces": _fractions(
            "1/16",
            "575/338688",
            "101113/2304433152",
            "1265029/1032386052096",
        ),
    },
    {
        "target": (2, 2, 1, 1, 1, 1, 1),
        "dimension": 27,
        "multiplicity": 3,
        "traces": _fractions(
            "11/144",
            "7675/3048192",
            "60541/658409472",
        ),
    },
    {
        "target": (7, 2),
        "dimension": 27,
        "multiplicity": 5,
        "traces": _fractions(
            "-593/3024",
            "118589/9144576",
            "-13669345/13826598912",
            "772572109/9291474468864",
            "-928039245139/126438384572301312",
        ),
    },
    {
        "target": (3, 3, 3),
        "dimension": 42,
        "multiplicity": 5,
        "traces": _fractions(
            "-17/3024",
            "36907/9144576",
            "-2727815/27653197824",
            "668649955/83623270219776",
            "-81833607287/252876769144602624",
        ),
    },
    {
        "target": (2, 2, 2, 2, 1),
        "dimension": 42,
        "multiplicity": 5,
        "traces": _fractions(
            "65/432",
            "65749/9144576",
            "394385/987614208",
            "2034216869/83623270219776",
            "21871678825/14048709396922368",
        ),
    },
    {
        "target": (5, 4),
        "dimension": 42,
        "multiplicity": 6,
        "traces": _fractions(
            "-463/3024",
            "26983/3048192",
            "-2851609/6913299456",
            "1800456173/83623270219776",
            "-7972991533/7024354698461184",
            "7885141027861/127449891648879722496",
        ),
    },
    {
        "target": (2, 2, 2, 1, 1, 1),
        "dimension": 48,
        "multiplicity": 6,
        "traces": _fractions(
            "211/1008",
            "106307/9144576",
            "3338455/4608866304",
            "444560315/9291474468864",
            "414412930019/126438384572301312",
            "88147235976301/382349674946639167488",
        ),
    },
    {
        "target": (6, 3),
        "dimension": 48,
        "multiplicity": 7,
        "traces": _fractions(
            "-91/432",
            "40333/3048192",
            "-11381039/13826598912",
            "4809923123/83623270219776",
            "-176934650687/42146128190767104",
            "40422855270283/127449891648879722496",
            "-4040560362624449/165175059576948120354816",
        ),
    },
    {
        "target": (6, 1, 1, 1),
        "dimension": 56,
        "multiplicity": 7,
        "traces": _fractions(
            "-7/72",
            "32251/2286144",
            "-1893491/3072577536",
            "1574114807/20905817554944",
            "-1319228477149/252876769144602624",
            "407646498356059/764699349893278334976",
            "-14323074914699167/330350119153896240709632",
        ),
    },
)


@dataclass(frozen=True)
class N9LowMultiplicityTargetRecord:
    target_partition: tuple[int, ...]
    target_dimension: int
    kronecker_multiplicity: int
    exact_power_traces: list[str]
    exact_characteristic_polynomial: str
    exact_square_free_gcd: str
    certified_minimum_raw_gap_lower_bound: float
    certified_minimum_raw_gap_upper_bound: float
    characteristic_polynomial_square_free: bool
    exact_transfer_recomputed: bool
    status: str


@dataclass(frozen=True)
class N9LowMultiplicityReport:
    created_at: str
    theorem_contract: dict[str, object]
    records: list[N9LowMultiplicityTargetRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _characteristic_polynomial(traces: tuple[Fraction, ...]) -> sp.Expr:
    elementary = [Fraction(1)]
    for degree in range(1, len(traces) + 1):
        elementary.append(
            sum(
                (-1) ** (index - 1)
                * elementary[degree - index]
                * traces[index - 1]
                for index in range(1, degree + 1)
            )
            / degree
        )
    return sp.factor(
        sum(
            (-1) ** degree
            * sp.Rational(value.numerator, value.denominator)
            * EIGENVALUE ** (len(traces) - degree)
            for degree, value in enumerate(elementary)
        )
    )


def _unpack_pair(key: int) -> tuple[tuple[int, ...], tuple[int, ...]]:
    left = tuple((key >> (4 * index)) & 15 for index in range(N))
    right = tuple((key >> (4 * N + 4 * index)) & 15 for index in range(N))
    return left, right


def _exact_translation_contraction(
    distributions: dict[int, dict[int, int]],
) -> dict[tuple[int, ...], tuple[Fraction, ...]]:
    targets = tuple(item["target"] for item in TARGET_CERTIFICATES)
    keys = set().union(*(set(rows) for rows in distributions.values()))
    pairs = {key: _unpack_pair(key) for key in keys}
    lefts = sorted({left for left, _ in pairs.values()})
    rights = sorted({right for _, right in pairs.values()})
    right_indices = {right: index for index, right in enumerate(rights)}

    permutations = np.array(
        list(itertools.permutations(range(N))),
        dtype=np.uint8,
    )
    cycle_types = tuple(integer_partitions(N))
    cycle_type_ids = {value: index for index, value in enumerate(cycle_types)}
    group_type_ids = np.fromiter(
        (cycle_type_ids[_cycle_type(tuple(row))] for row in permutations),
        dtype=np.uint8,
        count=len(permutations),
    )
    source_by_type = np.array(
        [symmetric_character(SOURCE_PARTITION, value) for value in cycle_types],
        dtype=np.int16,
    )
    source_by_group = source_by_type[group_type_ids]
    target_by_group = np.array(
        [
            [symmetric_character(target, value) for value in cycle_types]
            for target in targets
        ],
        dtype=np.int16,
    )[:, group_type_ids].astype(np.int64)
    factorial_weights = np.array(
        [math.factorial(N - index - 1) for index in range(N)],
        dtype=np.int64,
    )

    def translated_source_characters(right: tuple[int, ...]) -> np.ndarray:
        translated = permutations[:, right]
        ranks = np.zeros(len(permutations), dtype=np.int64)
        for index in range(N - 1):
            ranks += (
                np.sum(
                    translated[:, index, None]
                    > translated[:, index + 1 :],
                    axis=1,
                )
                * factorial_weights[index]
            )
        return source_by_group[ranks]

    with tempfile.TemporaryDirectory(prefix="qsearch-n9-characters-") as directory:
        character_path = Path(directory) / "right_characters.dat"
        right_characters = np.memmap(
            character_path,
            dtype=np.int16,
            mode="w+",
            shape=(len(rights), len(permutations)),
        )
        for index, right in enumerate(rights):
            right_characters[index] = translated_source_characters(right)
        right_characters.flush()

        pairs_by_left: defaultdict[
            tuple[int, ...], list[tuple[int, int]]
        ] = defaultdict(list)
        for key, (left, right) in pairs.items():
            pairs_by_left[left].append((key, right_indices[right]))
        contractions: dict[int, tuple[int, ...]] = {}
        for left in lefts:
            left_characters = translated_source_characters(left).astype(np.int64)
            rows = pairs_by_left[left]
            weighted_targets = [
                left_characters * target_characters
                for target_characters in target_by_group
            ]
            for start in range(0, len(rows), 128):
                chunk = rows[start : start + 128]
                selected = right_characters[[index for _, index in chunk]]
                values = [selected @ weighted for weighted in weighted_targets]
                for row_index, (key, _) in enumerate(chunk):
                    contractions[key] = tuple(
                        int(values[target_index][row_index])
                        for target_index in range(len(targets))
                    )

    result: dict[tuple[int, ...], tuple[Fraction, ...]] = {}
    for target_index, item in enumerate(TARGET_CERTIFICATES):
        traces = []
        for degree in range(1, int(item["multiplicity"]) + 1):
            numerator = sum(
                weight * contractions[key][target_index]
                for key, weight in distributions[degree].items()
            )
            traces.append(
                Fraction(
                    numerator,
                    math.factorial(N) * ORBIT_DENOMINATOR ** (degree - 1),
                )
            )
        result[item["target"]] = tuple(traces)
    return result


def _stored_traces() -> dict[tuple[int, ...], tuple[Fraction, ...]]:
    return {item["target"]: item["traces"] for item in TARGET_CERTIFICATES}


def build_n9_low_multiplicity_report(
    recompute: bool = False,
) -> N9LowMultiplicityReport:
    if recompute:
        distributions, _ = run_exact_transfer_kernel(max_degree=7, n=N)
        traces_by_target = _exact_translation_contraction(distributions)
        if traces_by_target != _stored_traces():
            raise ArithmeticError("n=9 recomputed traces differ from certificate")
    else:
        traces_by_target = _stored_traces()

    records: list[N9LowMultiplicityTargetRecord] = []
    for item in TARGET_CERTIFICATES:
        target = item["target"]
        traces = traces_by_target[target]
        polynomial = _characteristic_polynomial(traces)
        polynomial_object = sp.Poly(polynomial, EIGENVALUE)
        gcd = sp.gcd(polynomial_object, polynomial_object.diff())
        intervals = polynomial_object.intervals(eps=sp.Rational(1, 10**12))
        bounds = [interval for interval, _ in intervals]
        lower = min(
            right[0] - left[1] for left, right in zip(bounds, bounds[1:])
        )
        upper = min(
            right[1] - left[0] for left, right in zip(bounds, bounds[1:])
        )
        square_free = gcd.degree() == 0 and all(
            multiplicity == 1 for _, multiplicity in intervals
        )
        if not square_free:
            raise ArithmeticError(f"n=9 repeated root on target {target}")
        records.append(
            N9LowMultiplicityTargetRecord(
                target_partition=target,
                target_dimension=int(item["dimension"]),
                kronecker_multiplicity=int(item["multiplicity"]),
                exact_power_traces=[str(value) for value in traces],
                exact_characteristic_polynomial=str(polynomial),
                exact_square_free_gcd=str(gcd.as_expr()),
                certified_minimum_raw_gap_lower_bound=float(lower),
                certified_minimum_raw_gap_upper_bound=float(upper),
                characteristic_polynomial_square_free=square_free,
                exact_transfer_recomputed=recompute,
                status="exact-n9-low-multiplicity-simple-spectrum",
            )
        )
    global_gap = min(
        record.certified_minimum_raw_gap_lower_bound for record in records
    )
    metrics: dict[str, int | float] = {
        "n": N,
        "maximum_exact_transfer_degree": 7,
        "maximum_exact_transfer_state_count": max(STATE_COUNTS.values()),
        "low_multiplicity_target_count": len(records),
        "low_multiplicity_simple_spectrum_target_count": sum(
            record.characteristic_polynomial_square_free for record in records
        ),
        "n9_nontrivial_multiplicity_target_count": NONTRIVIAL_TARGET_COUNT,
        "n9_unaudited_higher_multiplicity_target_count": (
            NONTRIVIAL_TARGET_COUNT - len(records)
        ),
        "maximum_certified_kronecker_multiplicity": 7,
        "maximum_n9_kronecker_multiplicity": 28,
        "n9_exact_target_coverage_fraction": len(records)
        / NONTRIVIAL_TARGET_COUNT,
        "certified_low_multiplicity_minimum_raw_gap_lower_bound": global_gap,
        "certified_low_multiplicity_minimum_lcu_normalized_gap_lower_bound": (
            global_gap / 2
        ),
        "degree6_unique_left_translation_count": 2734,
        "degree6_unique_right_translation_count": 6587,
        "degree6_temporary_character_table_bytes": 4780581120,
        "degree7_unique_left_translation_count": 3559,
        "degree7_unique_right_translation_count": 9611,
        "degree7_temporary_character_table_bytes": 6975279360,
        "maximum_in_memory_character_chunk_rows": 128,
        "maximum_in_memory_character_chunk_bytes": 92897280,
        "bounded_memory_n9_character_contraction_count": 1,
        "scalable_n9_character_contraction_count": 0,
        "exact_transfer_recomputed_count": int(recompute),
        "all_n9_target_simple_spectrum_theorem_count": 0,
        "all_n_simple_spectrum_theorem_count": 0,
        "inverse_polynomial_normalized_gap_theorem_count": 0,
    }
    return N9LowMultiplicityReport(
        created_at=utc_now(),
        theorem_contract={
            "operator": "H_9=average(TT1)+average(TC1)",
            "source": "lambda=(4,3,1,1), dimension 216",
            "transfer": "exact simultaneous-conjugacy quotient through degree seven",
            "contraction": (
                "Exact integer S_9 character contraction grouped by translations; degree seven requires 3559 unique left and 9611 unique right rows."
            ),
            "implementation_boundary": (
                "The degree-seven memory-mapped right-character table uses 6.98 GB on disk; 128-row chunks cap each in-memory character slice near 93 MB, but disk growth is not a scalable all-n architecture."
            ),
            "scope": "all 11 n=9 targets of Kronecker multiplicity at most seven",
            "all_target_claimed": False,
            "asymptotic_claimed": False,
        },
        records=records,
        headline_metrics=metrics,
        claim_gate={
            "all_n9_low_multiplicity_targets_simple": True,
            "all_n9_targets_audited": False,
            "fixed_coefficient_survives_first_adjacent_size_probe": True,
            "inverse_polynomial_normalized_gap_proved": False,
            "coherent_transform_proved": False,
            "hidden_involution_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The fixed coefficient survives all 11 n=9 blocks of multiplicity at most seven, but 16 higher-multiplicity targets through multiplicity 28 remain unaudited."
            ),
        },
        status="n9-through-multiplicity-seven-survives-higher-blocks-open",
        summary=(
            "Exact n=9 quotient transfer proves TT1+TC1 has simple spectrum on all 11 targets of multiplicity at most seven; 16 higher-multiplicity targets remain open."
        ),
        falsifiers_triggered=[
            "The first adjacent-size transfer through multiplicity seven does not produce a repeated root.",
            "Low-multiplicity coverage is only 11 of 27 nontrivial n=9 targets.",
            "The n=9 source is not self-conjugate, so conjugate-target sign transfer cannot replace direct contraction.",
            "No all-target, all-n, coherent-transform, decoder, or speedup claim is allowed.",
        ],
    )


def write_n9_low_multiplicity_report(
    output_path: Path = COSET_TYPICAL_N9_LOW_MULTIPLICITY_PATH,
    recompute: bool = False,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(build_n9_low_multiplicity_report(recompute=recompute))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-COSET-TYPICAL-N9-LOW-MULTIPLICITY-SURVIVAL-NOT-ALL-TARGET",
                source=str(output_path),
                claim=(
                    "Survival on every n=9 target of multiplicity at most seven establishes adjacent-size robustness."
                ),
                reason_invalid=(
                    "Sixteen n=9 targets of multiplicity 8 through 28 remain unaudited and may contain collisions or much smaller gaps."
                ),
                lesson=(
                    "Move next to multiplicity eight with the bounded-memory contraction, then stop immediately on a repeated root."
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
                artifacts={"coset_typical_n9_low_multiplicity_probe": str(output_path)},
            )
        )
    return payload


if __name__ == "__main__":
    report = write_n9_low_multiplicity_report(recompute=True)
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
