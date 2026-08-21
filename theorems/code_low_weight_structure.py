"""Low-weight support hypergraph baseline for code-equivalence rows.

Binary code equivalence is coordinate permutation of a linear-code support
structure.  A nonabelian-HSP/coset candidate built from code equivalence should
not survive merely because weak enumerators or tuple profiles were incomplete.
This module attacks rows with low-weight codeword support hypergraphs, a
matroid-flavoured classical invariant that often exposes hidden coordinate
structure before any quantum observable design is meaningful.

The baseline is deliberately conservative: separations are negative evidence;
matches are proof debt or equivalent controls, never positive quantum evidence.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, is_dataclass
from pathlib import Path
from typing import Any, Iterable

import networkx as nx
import numpy as np

from code_canonicalization_baseline import default_code_canonicalization_pairs
from code_family_search import enumerate_unique_codewords
from research_registry import ExperimentResultRecord, NegativeResultRecord, upsert_experiment_result, upsert_negative_result, utc_now


CODE_EQUIVALENCE_DIR = Path("research/code_equivalence")
CODE_LOW_WEIGHT_STRUCTURE_PATH = CODE_EQUIVALENCE_DIR / "code_low_weight_structure.json"
QUASI_CYCLIC_CODE_SEARCH_PATH = CODE_EQUIVALENCE_DIR / "quasi_cyclic_code_search.json"
QUASI_CYCLIC_CANONICALIZATION_PATH = CODE_EQUIVALENCE_DIR / "quasi_cyclic_canonicalization.json"
QC_INFORMATION_SET_RESOLVER_PATH = CODE_EQUIVALENCE_DIR / "qc_information_set_resolver.json"
CYCLIC_CODE_SEARCH_PATH = CODE_EQUIVALENCE_DIR / "cyclic_code_search.json"
BCH_CODE_SEARCH_PATH = CODE_EQUIVALENCE_DIR / "bch_code_search.json"
GOPPA_CODE_SEARCH_PATH = CODE_EQUIVALENCE_DIR / "goppa_code_search.json"
TANNER_CODE_SEARCH_PATH = CODE_EQUIVALENCE_DIR / "tanner_code_search.json"
REED_MULLER_CODE_SEARCH_PATH = CODE_EQUIVALENCE_DIR / "reed_muller_code_search.json"
RANK_METRIC_CODE_SEARCH_PATH = CODE_EQUIVALENCE_DIR / "rank_metric_code_search.json"
AFFINE_GEOMETRY_CODE_SEARCH_PATH = CODE_EQUIVALENCE_DIR / "affine_geometry_code_search.json"
PROJECTIVE_GEOMETRY_CODE_SEARCH_PATH = CODE_EQUIVALENCE_DIR / "projective_geometry_code_search.json"


@dataclass(frozen=True)
class CodePairInput:
    id: str
    row_id: str
    row_family: str
    source: str
    left: np.ndarray
    right: np.ndarray
    known_equivalent: bool | None


@dataclass(frozen=True)
class LowWeightSignatureSummary:
    evaluated: bool
    reason: str
    length: int
    dimension: int
    minimum_weight: int | None
    max_weight_evaluated: int | None
    support_count: int
    low_weight_spectrum: list[list[int]]
    coordinate_profile_bucket_sizes: list[int]
    low_weight_spectrum_digest: str
    coordinate_profile_digest: str
    pair_profile_digest: str
    incidence_wl_digest: str


@dataclass(frozen=True)
class LowWeightIncidenceCertificate:
    evaluated: bool
    isomorphic: bool | None
    node_count_a: int
    node_count_b: int
    support_count_a: int
    support_count_b: int
    cost_model: str
    interpretation: str


@dataclass(frozen=True)
class LowWeightStructureRecord:
    id: str
    row_id: str
    row_family: str
    source: str
    length: int
    dimension_a: int
    dimension_b: int
    known_equivalent: bool | None
    evaluated: bool
    max_weight: int
    weight_radius: int
    distinguishing_signatures: list[str]
    signature_a: LowWeightSignatureSummary
    signature_b: LowWeightSignatureSummary
    incidence_certificate: LowWeightIncidenceCertificate
    status: str
    interpretation: str


@dataclass(frozen=True)
class LowWeightStructureReport:
    created_at: str
    records: list[LowWeightStructureRecord]
    max_weight: int
    weight_radius: int
    max_codewords: int
    headline_metrics: dict[str, int]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _read_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        return fallback


def _digest(value: Any) -> str:
    encoded = repr(value).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()[:24]


def _support_mask(word: np.ndarray) -> int:
    value = 0
    for index, bit in enumerate(np.asarray(word, dtype=np.uint8).tolist()):
        if bit:
            value |= 1 << index
    return value


def _support_coordinates(mask: int, length: int) -> tuple[int, ...]:
    return tuple(index for index in range(length) if (mask >> index) & 1)


def _weight_histogram(masks: Iterable[int]) -> tuple[tuple[int, int], ...]:
    counts: dict[int, int] = {}
    for mask in masks:
        weight = int(mask.bit_count())
        counts[weight] = counts.get(weight, 0) + 1
    return tuple(sorted(counts.items()))


def _coordinate_profiles(masks: list[int], length: int) -> tuple[tuple[tuple[int, int], ...], ...]:
    profiles = []
    for coordinate in range(length):
        counts: dict[int, int] = {}
        bit = 1 << coordinate
        for mask in masks:
            if mask & bit:
                weight = int(mask.bit_count())
                counts[weight] = counts.get(weight, 0) + 1
        profiles.append(tuple(sorted(counts.items())))
    return tuple(sorted(profiles))


def _pair_profiles(masks: list[int], length: int) -> tuple[tuple[tuple[int, int], ...], ...]:
    profiles = []
    for left in range(length):
        left_bit = 1 << left
        for right in range(left + 1, length):
            both = left_bit | (1 << right)
            counts: dict[int, int] = {}
            for mask in masks:
                if mask & both == both:
                    weight = int(mask.bit_count())
                    counts[weight] = counts.get(weight, 0) + 1
            profiles.append(tuple(sorted(counts.items())))
    return tuple(sorted(profiles))


def _incidence_wl_signature(
    masks: list[int],
    length: int,
    iterations: int = 4,
) -> tuple[str, ...]:
    """Return a 1-WL colour multiset for coordinate/support incidence.

    The graph has one coordinate vertex per coordinate and one support vertex
    per low-weight codeword support, coloured by side and support weight.  This
    is not a complete isomorphism test; it is a cheap invariant that catches
    many matroid shadows and defines proof debt when it matches.
    """

    adjacency: dict[tuple[str, int], list[tuple[str, int]]] = {}
    colours: dict[tuple[str, int], str] = {}
    for coordinate in range(length):
        node = ("c", coordinate)
        adjacency[node] = []
        colours[node] = "coord"
    for support_index, mask in enumerate(sorted(masks)):
        support_node = ("s", support_index)
        adjacency[support_node] = []
        colours[support_node] = f"support:{mask.bit_count()}"
        for coordinate in _support_coordinates(mask, length):
            coord_node = ("c", coordinate)
            adjacency[coord_node].append(support_node)
            adjacency[support_node].append(coord_node)

    for _ in range(iterations):
        raw = {
            node: (colours[node], tuple(sorted(colours[neighbour] for neighbour in adjacency[node])))
            for node in adjacency
        }
        palette = {value: f"c{index}" for index, value in enumerate(sorted(set(raw.values())))}
        colours = {node: palette[value] for node, value in raw.items()}
    return tuple(sorted(colours.values()))


def low_weight_signature_values(
    generator: np.ndarray,
    max_weight: int = 6,
    weight_radius: int = 2,
    max_codewords: int = 32768,
    wl_iterations: int = 4,
) -> tuple[dict[str, Any], LowWeightSignatureSummary]:
    matrix = np.asarray(generator, dtype=np.uint8) & 1
    dimension, length = matrix.shape
    if dimension >= 63 or (1 << dimension) > max_codewords:
        summary = LowWeightSignatureSummary(
            evaluated=False,
            reason=f"Skipped: 2^{dimension} codewords exceed cap {max_codewords}.",
            length=int(length),
            dimension=int(dimension),
            minimum_weight=None,
            max_weight_evaluated=None,
            support_count=0,
            low_weight_spectrum=[],
            coordinate_profile_bucket_sizes=[],
            low_weight_spectrum_digest="skipped",
            coordinate_profile_digest="skipped",
            pair_profile_digest="skipped",
            incidence_wl_digest="skipped",
        )
        return {}, summary

    words = enumerate_unique_codewords(matrix)
    nonzero_masks = sorted({_support_mask(word) for word in words if int(word.sum()) > 0})
    if not nonzero_masks:
        summary = LowWeightSignatureSummary(
            evaluated=True,
            reason="The code has no nonzero codeword supports under enumeration.",
            length=int(length),
            dimension=int(dimension),
            minimum_weight=None,
            max_weight_evaluated=None,
            support_count=0,
            low_weight_spectrum=[],
            coordinate_profile_bucket_sizes=[],
            low_weight_spectrum_digest=_digest(()),
            coordinate_profile_digest=_digest(()),
            pair_profile_digest=_digest(()),
            incidence_wl_digest=_digest(()),
        )
        return {"spectrum": (), "coordinate_profiles": (), "pair_profiles": (), "incidence_wl": ()}, summary

    minimum_weight = min(mask.bit_count() for mask in nonzero_masks)
    threshold = min(max_weight, minimum_weight + weight_radius)
    low_weight_masks = [mask for mask in nonzero_masks if mask.bit_count() <= threshold]
    spectrum = _weight_histogram(low_weight_masks)
    coordinate_profiles = _coordinate_profiles(low_weight_masks, int(length))
    pair_profiles = _pair_profiles(low_weight_masks, int(length))
    incidence_wl = _incidence_wl_signature(low_weight_masks, int(length), iterations=wl_iterations)
    coordinate_bucket_sizes = _coordinate_bucket_sizes_from_profiles(coordinate_profiles)
    values = {
        "minimum_weight": minimum_weight,
        "max_weight_evaluated": threshold,
        "spectrum": spectrum,
        "coordinate_profiles": coordinate_profiles,
        "pair_profiles": pair_profiles,
        "incidence_wl": incidence_wl,
        "support_masks": tuple(low_weight_masks),
    }
    summary = LowWeightSignatureSummary(
        evaluated=True,
        reason=f"Enumerated {len(words)} codeword(s) and retained {len(low_weight_masks)} support(s) up to weight {threshold}.",
        length=int(length),
        dimension=int(dimension),
        minimum_weight=int(minimum_weight),
        max_weight_evaluated=int(threshold),
        support_count=len(low_weight_masks),
        low_weight_spectrum=[[int(weight), int(count)] for weight, count in spectrum],
        coordinate_profile_bucket_sizes=coordinate_bucket_sizes,
        low_weight_spectrum_digest=_digest(spectrum),
        coordinate_profile_digest=_digest(coordinate_profiles),
        pair_profile_digest=_digest(pair_profiles),
        incidence_wl_digest=_digest(incidence_wl),
    )
    return values, summary


def _coordinate_bucket_sizes_from_profiles(profiles: tuple[tuple[tuple[int, int], ...], ...]) -> list[int]:
    counts: dict[tuple[tuple[int, int], ...], int] = {}
    for profile in profiles:
        counts[profile] = counts.get(profile, 0) + 1
    return sorted(counts.values())


def _low_weight_incidence_graph(masks: Iterable[int], length: int) -> nx.Graph:
    graph = nx.Graph()
    for coordinate in range(length):
        graph.add_node(("c", coordinate), side="coordinate", weight=0)
    for support_index, mask in enumerate(sorted(masks)):
        support_node = ("s", support_index)
        graph.add_node(support_node, side="support", weight=int(mask.bit_count()))
        for coordinate in _support_coordinates(mask, length):
            graph.add_edge(("c", coordinate), support_node)
    return graph


def low_weight_incidence_certificate(
    left_values: dict[str, Any],
    right_values: dict[str, Any],
    length: int,
    max_nodes: int = 220,
) -> LowWeightIncidenceCertificate:
    left_masks = tuple(int(mask) for mask in left_values.get("support_masks", ()))
    right_masks = tuple(int(mask) for mask in right_values.get("support_masks", ()))
    left_nodes = int(length + len(left_masks))
    right_nodes = int(length + len(right_masks))
    if left_nodes > max_nodes or right_nodes > max_nodes:
        return LowWeightIncidenceCertificate(
            evaluated=False,
            isomorphic=None,
            node_count_a=left_nodes,
            node_count_b=right_nodes,
            support_count_a=len(left_masks),
            support_count_b=len(right_masks),
            cost_model=f"Skipped exact incidence isomorphism: node counts {left_nodes}/{right_nodes} exceed cap {max_nodes}.",
            interpretation=(
                "Low-weight support signatures match, but exact support-hypergraph isomorphism exceeded the configured cap."
            ),
        )
    left_graph = _low_weight_incidence_graph(left_masks, length)
    right_graph = _low_weight_incidence_graph(right_masks, length)

    def node_match(left: dict[str, Any], right: dict[str, Any]) -> bool:
        return left.get("side") == right.get("side") and left.get("weight") == right.get("weight")

    isomorphic = bool(nx.is_isomorphic(left_graph, right_graph, node_match=node_match))
    return LowWeightIncidenceCertificate(
        evaluated=True,
        isomorphic=isomorphic,
        node_count_a=left_nodes,
        node_count_b=right_nodes,
        support_count_a=len(left_masks),
        support_count_b=len(right_masks),
        cost_model=f"Ran exact colored incidence-graph isomorphism on {left_nodes}/{right_nodes} nodes.",
        interpretation=(
            "Low-weight support incidence hypergraphs are isomorphic; this is still proof debt unless an external "
            "automorphism/canonicalization certificate proves code equivalence."
            if isomorphic
            else "Low-weight support incidence hypergraphs are not isomorphic; the row is classically separated."
        ),
    )


def _status_is_control(status: str) -> bool:
    lower = status.lower()
    if "proof-debt" in lower or "no-equivalence" in lower or "rejected" in lower:
        return False
    return (
        "equivalent-control" in lower
        or lower.startswith("equivalent-under")
        or "all-equivalent-controls" in lower
        or "semilinear-control" in lower
        or "dihedral-control" in lower
        or "automorphism-control" in lower
        or "tanner-graph-isomorphism" in lower
    )


def _qc_control_ids() -> set[str]:
    ids: set[str] = set()
    for path in (QUASI_CYCLIC_CANONICALIZATION_PATH, QC_INFORMATION_SET_RESOLVER_PATH):
        payload = _read_json(path, {})
        for record in payload.get("records", []):
            status = str(record.get("status", ""))
            if _status_is_control(status):
                ids.add(str(record.get("id", "")))
    return {item for item in ids if item}


def _row_from_default_pair(record_id: str, source: str) -> tuple[str, str]:
    if source == "code_family_search":
        return record_id, "random-weak-invariant-family"
    return record_id, "seed-code-pair"


def _artifact_pair_inputs(
    path: Path,
    source: str,
    row_prefix: str,
    row_family: str,
    known_control_ids: set[str] | None = None,
) -> list[CodePairInput]:
    payload = _read_json(path, {})
    control_ids = known_control_ids or set()
    pairs: list[CodePairInput] = []
    for record in payload.get("records", []):
        spec_id = str(dict(record.get("spec", {})).get("id", "unknown-code-family"))
        row_id = f"{row_prefix}{spec_id}"
        for list_key in ("collision_audits", "control_audits"):
            for audit in record.get(list_key, []):
                left = audit.get("generator_a") or []
                right = audit.get("generator_b") or []
                if not left or not right:
                    continue
                status = str(audit.get("status", ""))
                audit_id = str(audit.get("id", f"{spec_id}-{list_key}-{len(pairs)}"))
                known_equivalent = True if list_key == "control_audits" or _status_is_control(status) or audit_id in control_ids else None
                pairs.append(
                    CodePairInput(
                        id=audit_id,
                        row_id=row_id,
                        row_family=row_family,
                        source=source,
                        left=np.asarray(left, dtype=np.uint8),
                        right=np.asarray(right, dtype=np.uint8),
                        known_equivalent=known_equivalent,
                    )
                )
    return pairs


def default_low_weight_structure_pairs(
    include_code_family_search: bool = True,
    include_algebraic_searches: bool = True,
) -> list[CodePairInput]:
    pairs: list[CodePairInput] = []
    for record_id, source, left, right, known_equivalent in default_code_canonicalization_pairs(
        include_code_family_search=include_code_family_search
    ):
        row_id, row_family = _row_from_default_pair(record_id, source)
        pairs.append(
            CodePairInput(
                id=record_id,
                row_id=row_id,
                row_family=row_family,
                source=source,
                left=np.asarray(left, dtype=np.uint8),
                right=np.asarray(right, dtype=np.uint8),
                known_equivalent=known_equivalent,
            )
        )
    if include_algebraic_searches:
        qc_control_ids = _qc_control_ids()
        pairs.extend(
            _artifact_pair_inputs(
                QUASI_CYCLIC_CODE_SEARCH_PATH,
                "quasi_cyclic_code_search",
                "qc-family-",
                "quasi-cyclic-family",
                known_control_ids=qc_control_ids,
            )
        )
        pairs.extend(
            _artifact_pair_inputs(
                CYCLIC_CODE_SEARCH_PATH,
                "cyclic_code_search",
                "cyclic-family-",
                "cyclic-code-family",
            )
        )
        pairs.extend(
            _artifact_pair_inputs(
                BCH_CODE_SEARCH_PATH,
                "bch_code_search",
                "bch-family-",
                "bch-code-family",
            )
        )
        pairs.extend(
            _artifact_pair_inputs(
                GOPPA_CODE_SEARCH_PATH,
                "goppa_code_search",
                "goppa-family-",
                "goppa-code-family",
            )
        )
        pairs.extend(
            _artifact_pair_inputs(
                TANNER_CODE_SEARCH_PATH,
                "tanner_code_search",
                "tanner-family-",
                "tanner-ldpc-family",
            )
        )
        pairs.extend(
            _artifact_pair_inputs(
                REED_MULLER_CODE_SEARCH_PATH,
                "reed_muller_code_search",
                "rm-family-",
                "punctured-reed-muller-family",
            )
        )
        pairs.extend(
            _artifact_pair_inputs(
                RANK_METRIC_CODE_SEARCH_PATH,
                "rank_metric_code_search",
                "rank-metric-family-",
                "binary-expanded-rank-metric-family",
            )
        )
        pairs.extend(
            _artifact_pair_inputs(
                AFFINE_GEOMETRY_CODE_SEARCH_PATH,
                "affine_geometry_code_search",
                "ag-family-",
                "affine-geometry-code-family",
            )
        )
        pairs.extend(
            _artifact_pair_inputs(
                PROJECTIVE_GEOMETRY_CODE_SEARCH_PATH,
                "projective_geometry_code_search",
                "pg-family-",
                "projective-geometry-code-family",
            )
        )

    deduped: dict[tuple[str, str], CodePairInput] = {}
    for pair in pairs:
        deduped[(pair.source, pair.id)] = pair
    return list(deduped.values())


def audit_low_weight_structure_pair(
    pair: CodePairInput,
    max_weight: int = 6,
    weight_radius: int = 2,
    max_codewords: int = 32768,
    wl_iterations: int = 4,
    max_incidence_nodes: int = 220,
) -> LowWeightStructureRecord:
    left = np.asarray(pair.left, dtype=np.uint8) & 1
    right = np.asarray(pair.right, dtype=np.uint8) & 1
    left_values, left_summary = low_weight_signature_values(
        left,
        max_weight=max_weight,
        weight_radius=weight_radius,
        max_codewords=max_codewords,
        wl_iterations=wl_iterations,
    )
    right_values, right_summary = low_weight_signature_values(
        right,
        max_weight=max_weight,
        weight_radius=weight_radius,
        max_codewords=max_codewords,
        wl_iterations=wl_iterations,
    )
    distinguishing: list[str] = []
    evaluated = bool(left_summary.evaluated and right_summary.evaluated)
    if evaluated:
        for name in ("minimum_weight", "max_weight_evaluated", "spectrum", "coordinate_profiles", "pair_profiles", "incidence_wl"):
            if left_values.get(name) != right_values.get(name):
                distinguishing.append(name)
    incidence = (
        low_weight_incidence_certificate(left_values, right_values, length=int(left.shape[1]), max_nodes=max_incidence_nodes)
        if evaluated and not distinguishing
        else LowWeightIncidenceCertificate(
            evaluated=False,
            isomorphic=None,
            node_count_a=int(left.shape[1]) + int(left_summary.support_count),
            node_count_b=int(right.shape[1]) + int(right_summary.support_count),
            support_count_a=int(left_summary.support_count),
            support_count_b=int(right_summary.support_count),
            cost_model="Skipped exact incidence isomorphism because signatures already separate or enumeration failed.",
            interpretation="No incidence-isomorphism certificate needed for this decision.",
        )
    )

    if not evaluated:
        status = "low-weight-matroid-proof-debt"
        interpretation = (
            "Low-weight support enumeration exceeded a cap; this row remains proof debt and must not be "
            "used as positive quantum evidence without a scalable classical lower-bound argument."
        )
    elif distinguishing:
        status = "rejected-by-low-weight-matroid-structure"
        interpretation = (
            "Low-weight codeword support hypergraphs separate this row: " + ", ".join(distinguishing) + "."
        )
    elif incidence.evaluated and incidence.isomorphic is False:
        status = "rejected-by-low-weight-incidence-isomorphism"
        interpretation = "Exact low-weight support incidence-graph isomorphism rejects this row."
    elif pair.known_equivalent:
        status = "low-weight-matroid-equivalent-control"
        interpretation = (
            "Low-weight support hypergraph signatures match on a row already certified as an equivalent/control "
            "case by a source automorphism, information-set, or canonicalization baseline."
        )
    else:
        status = "low-weight-matroid-survivor-proof-debt"
        interpretation = (
            "Low-weight support hypergraphs match under the configured cap. This is proof debt only; "
            "run information-set/canonicalization/automorphism baselines and prove lower bounds before promotion."
        )

    return LowWeightStructureRecord(
        id=pair.id,
        row_id=pair.row_id,
        row_family=pair.row_family,
        source=pair.source,
        length=int(left.shape[1]),
        dimension_a=int(left.shape[0]),
        dimension_b=int(right.shape[0]),
        known_equivalent=pair.known_equivalent,
        evaluated=evaluated,
        max_weight=max_weight,
        weight_radius=weight_radius,
        distinguishing_signatures=distinguishing,
        signature_a=left_summary,
        signature_b=right_summary,
        incidence_certificate=incidence,
        status=status,
        interpretation=interpretation,
    )


def run_low_weight_structure_baseline(
    max_weight: int = 6,
    weight_radius: int = 2,
    max_codewords: int = 32768,
    wl_iterations: int = 4,
    max_incidence_nodes: int = 220,
    include_code_family_search: bool = True,
    include_algebraic_searches: bool = True,
) -> LowWeightStructureReport:
    pairs = default_low_weight_structure_pairs(
        include_code_family_search=include_code_family_search,
        include_algebraic_searches=include_algebraic_searches,
    )
    records = [
        audit_low_weight_structure_pair(
            pair,
            max_weight=max_weight,
            weight_radius=weight_radius,
            max_codewords=max_codewords,
            wl_iterations=wl_iterations,
            max_incidence_nodes=max_incidence_nodes,
        )
        for pair in pairs
    ]
    metrics = {
        "record_count": len(records),
        "low_weight_rejection_count": sum(
            1
            for record in records
            if record.status in {"rejected-by-low-weight-matroid-structure", "rejected-by-low-weight-incidence-isomorphism"}
        ),
        "equivalent_control_count": sum(1 for record in records if record.status == "low-weight-matroid-equivalent-control"),
        "proof_debt_count": sum(
            1
            for record in records
            if record.status in {"low-weight-matroid-proof-debt", "low-weight-matroid-survivor-proof-debt"}
        ),
        "survivor_proof_debt_count": sum(1 for record in records if record.status == "low-weight-matroid-survivor-proof-debt"),
        "cap_proof_debt_count": sum(1 for record in records if record.status == "low-weight-matroid-proof-debt"),
        "minimum_weight_rejection_count": sum(1 for record in records if "minimum_weight" in record.distinguishing_signatures),
        "spectrum_rejection_count": sum(1 for record in records if "spectrum" in record.distinguishing_signatures),
        "coordinate_profile_rejection_count": sum(1 for record in records if "coordinate_profiles" in record.distinguishing_signatures),
        "pair_profile_rejection_count": sum(1 for record in records if "pair_profiles" in record.distinguishing_signatures),
        "incidence_wl_rejection_count": sum(1 for record in records if "incidence_wl" in record.distinguishing_signatures),
        "incidence_isomorphism_rejection_count": sum(1 for record in records if record.status == "rejected-by-low-weight-incidence-isomorphism"),
        "incidence_isomorphism_match_count": sum(
            1 for record in records if record.incidence_certificate.evaluated and record.incidence_certificate.isomorphic is True
        ),
        "incidence_isomorphism_cap_count": sum(
            1 for record in records if record.incidence_certificate.evaluated is False and not record.distinguishing_signatures
        ),
    }
    if metrics["proof_debt_count"]:
        status = "low-weight-matroid-proof-debt"
    elif metrics["low_weight_rejection_count"]:
        status = "code-rows-dequantized-by-low-weight-matroid-structure"
    else:
        status = "low-weight-matroid-controls-only"
    summary = (
        f"Audited {metrics['record_count']} code-equivalence row(s) with low-weight support hypergraph invariants. "
        f"{metrics['low_weight_rejection_count']} row(s) were separated, "
        f"{metrics['equivalent_control_count']} were controls, and "
        f"{metrics['proof_debt_count']} remain proof debt."
    )
    falsifiers = []
    if metrics["low_weight_rejection_count"]:
        falsifiers.append("Low-weight codeword support hypergraphs separate current code-equivalence rows.")
    if metrics["proof_debt_count"]:
        falsifiers.append("Rows matching low-weight support structure remain proof debt, not positive evidence.")
    return LowWeightStructureReport(
        utc_now(),
        records,
        max_weight,
        weight_radius,
        max_codewords,
        metrics,
        status,
        summary,
        falsifiers,
    )


def _json_ready(value: Any) -> Any:
    if is_dataclass(value):
        return _json_ready(asdict(value))
    if isinstance(value, dict):
        return {str(key): _json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_ready(item) for item in value]
    if isinstance(value, tuple):
        return [_json_ready(item) for item in value]
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.bool_):
        return bool(value)
    return value


def _safe_id(value: str) -> str:
    return "".join(ch if ch.isalnum() else "_" for ch in value.upper()).strip("_")


def write_low_weight_structure_negative_results(report: LowWeightStructureReport) -> int:
    written = 0
    for record in report.records:
        if record.status not in {"rejected-by-low-weight-matroid-structure", "rejected-by-low-weight-incidence-isomorphism"}:
            continue
        upsert_negative_result(
            NegativeResultRecord(
                id=f"CODE-LOW-WEIGHT-MATROID-REJECTED-{_safe_id(record.row_id)}-{_safe_id(record.id)}",
                source="code_low_weight_structure.py",
                claim=f"{record.row_id} supplies hard code-equivalence evidence beyond classical low-weight structure.",
                reason_invalid=record.interpretation,
                lesson=(
                    "Code-equivalence rows must survive low-weight support hypergraphs/matroid structure, "
                    "tuple profiles, information-set canonicalization, and automorphism-aware checks before "
                    "motivating nonabelian coset observables."
                ),
                applies_to=["CODE-COSET-COLLECTIVE", "PO-DEQUANTIZATION", "PO-FALSIFIERS"],
                evidence={
                    "record_id": record.id,
                    "row_id": record.row_id,
                    "row_family": record.row_family,
                    "source": record.source,
                    "status": record.status,
                    "distinguishing_signatures": record.distinguishing_signatures,
                    "minimum_weight_a": record.signature_a.minimum_weight,
                    "minimum_weight_b": record.signature_b.minimum_weight,
                },
            )
        )
        written += 1
    return written


def write_code_low_weight_structure(
    output_path: Path = CODE_LOW_WEIGHT_STRUCTURE_PATH,
    max_weight: int = 6,
    weight_radius: int = 2,
    max_codewords: int = 32768,
    wl_iterations: int = 4,
    max_incidence_nodes: int = 220,
    include_code_family_search: bool = True,
    include_algebraic_searches: bool = True,
    write_registry: bool = True,
    registry_experiment_id: str = "EXP-CODE-LOW-WEIGHT-MATROID-BASELINE",
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "RESULT-CODE-LOW-WEIGHT-MATROID-BASELINE-LATEST",
) -> dict[str, Any]:
    report = run_low_weight_structure_baseline(
        max_weight=max_weight,
        weight_radius=weight_radius,
        max_codewords=max_codewords,
        wl_iterations=wl_iterations,
        max_incidence_nodes=max_incidence_nodes,
        include_code_family_search=include_code_family_search,
        include_algebraic_searches=include_algebraic_searches,
    )
    payload = _json_ready(report)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    if write_registry:
        negative_results_written = write_low_weight_structure_negative_results(report)
        metrics = dict(report.headline_metrics)
        metrics["negative_results_written"] = negative_results_written
        upsert_experiment_result(
            ExperimentResultRecord(
                id=registry_result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=report.created_at,
                status=report.status,
                summary=report.summary,
                metrics=metrics,
                falsifiers_triggered=report.falsifiers_triggered,
                artifacts={"code_low_weight_structure": str(output_path)},
            )
        )
    return payload
