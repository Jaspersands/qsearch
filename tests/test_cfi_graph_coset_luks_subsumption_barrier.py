"""Independent graph controls for the scoped CFI classical baseline.

No reports are constructed during collection and no artifact/registry writers
are called. The reference expands even local bit patterns, not audit formulas.
"""

from itertools import combinations, product
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

import numpy as np
import pytest

from theorems import cfi_base_family_search as family
from theorems import cfi_graph_coset_luks_subsumption_barrier as audit


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = ROOT / "research/certificates/cfi_graph_coset_luks_subsumption_barrier_crosscheck.js"
OLD_NEGATIVE_ID = "NEG-CFI-GRAPH-COSET-LUKS-SUBSUMPTION-BARRIER"
CUBIC_BASES = (
    "complete-k4", "triangular-prism", "cube-q3", "mobius-ladder-8",
    "petersen", "heawood-like-14",
)
CLAIM_GATES = {
    "speedup_claim_allowed": False,
    "universal_cfi_trilemma_barrier_proved": False,
    "single_copy_quantum_mutual_information_extinction_proved": False,
    "multi_copy_commutant_exponential_intractability_proved": False,
    "luks_classical_polynomial_subsumption_certified": True,
    "explicit_luks_quartic_bound_proved": False,
    "cycle_subgroup_normal_in_full_uncolored_group_proved": False,
    "classical_algorithm_executed": False,
}
REMOVED_ESTIMATES = {
    "luks_polynomial_degree", "luks_operations_estimate", "luks_classical_time_log2",
    "single_copy_quantum_mutual_information_log2",
    "three_copy_quantum_commutant_dimension_log2", "quantum_strictly_harder_than_classical",
    "luks_classical_time_log2_at_100_base_vertices",
    "three_copy_commutant_dimension_log2_at_100_base_vertices",
    "quantum_overhead_vs_luks_at_100_base_vertices_log2",
}


def _base(n, edges):
    adjacency = np.zeros((n, n), dtype=int)
    for u, v in edges:
        assert u != v and not adjacency[u, v]
        adjacency[u, v] = adjacency[v, u] = 1
    return adjacency


def _small_base(name):
    if name == "isolated":
        return _base(1, [])
    if name == "isolated-pair":
        return _base(2, [])
    if name == "single-edge":
        return _base(2, [(0, 1)])
    if name == "path":
        return _base(5, [(v, v + 1) for v in range(4)])
    if name == "cycle":
        return _base(5, [(v, (v + 1) % 5) for v in range(5)])
    if name == "disconnected":
        return _base(8, [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5)])
    if name == "mixed-2-3-4":
        return _base(5, [(v, (v + 1) % 5) for v in range(5)] + [(0, 2), (0, 3)])
    if name == "degree-four":
        return _base(5, combinations(range(5), 2))
    raise AssertionError(name)


SMALL_BASES = (
    "isolated", "isolated-pair", "single-edge", "path", "cycle",
    "disconnected", "mixed-2-3-4", "degree-four",
)


def _reference_graph(base, twist=None):
    """Build the shared-edge gadget from Cartesian products of local bits."""
    edges = [(u, v) for u, v in combinations(range(len(base)), 2) if base[u, v]]
    incident = [[i for i, edge in enumerate(edges) if v in edge] for v in range(len(base))]
    labels = []
    for v, local in enumerate(incident):
        for bits in product((0, 1), repeat=len(local)):
            if sum(bits) % 2 == 0:
                # Least-significant local edge first, matching constructor labels.
                labels.append(("middle", v, bits[::-1]))
    middle_count = len(labels)
    labels.extend(("edge", i, bit) for i in range(len(edges)) for bit in (0, 1))
    index = {label: i for i, label in enumerate(labels)}
    expanded = np.zeros((len(labels), len(labels)), dtype=int)
    for source, (_, v, bits) in enumerate(labels[:middle_count]):
        for edge_index, bit in zip(incident[v], bits):
            edge = edges[edge_index]
            if edge == twist and v == edge[0]:
                bit = 1 - bit
            target = index[("edge", edge_index, bit)]
            expanded[source, target] = expanded[target, source] = 1
    return expanded, labels, edges, incident, middle_count


def _component_count(base):
    remaining = set(range(len(base)))
    count = 0
    while remaining:
        pending = [remaining.pop()]
        count += 1
        while pending:
            vertex = pending.pop()
            neighbors = {v for v in remaining if base[vertex, v]}
            remaining -= neighbors
            pending.extend(neighbors)
    return count


def _assert_no_old_estimates(value):
    if isinstance(value, dict):
        assert not REMOVED_ESTIMATES.intersection(value)
        for nested in value.values():
            _assert_no_old_estimates(nested)
    elif isinstance(value, list):
        for nested in value:
            _assert_no_old_estimates(nested)


def _assert_finite_record(record, base):
    graph, labels, edges, incident, middle_count = _reference_graph(base)
    np.testing.assert_array_equal(family.cfi_parity_graph_from_base(base), graph)
    assert np.array_equal(graph, graph.T)
    assert not np.any(np.diag(graph))
    assert set(np.unique(graph)) <= {0, 1}
    assert not graph[:middle_count, :middle_count].any()
    assert not graph[middle_count:, middle_count:].any()
    degrees = graph.sum(axis=1)
    base_degrees = [len(local) for local in incident]
    expected_vertices = sum(1 if d == 0 else 2 ** (d - 1) for d in base_degrees) + 2 * len(edges)
    expected_edges = sum(d * 2 ** (d - 1) for d in base_degrees if d > 0)
    assert len(graph) == expected_vertices
    assert int(graph.sum()) // 2 == expected_edges
    assert record["base_vertex_count"] == len(base)
    assert record["base_edge_count"] == len(edges)
    assert record["base_degrees"] == base_degrees
    assert record["is_3_regular"] is all(d == 3 for d in base_degrees)
    assert record["cfi_vertex_count"] == record["expected_cfi_vertex_count"] == expected_vertices
    assert record["cfi_edge_count"] == record["expected_cfi_edge_count"] == expected_edges
    assert record["vertex_count_identity_verified"] is True
    assert record["edge_count_identity_verified"] is True
    assert record["cfi_min_degree"] == int(degrees.min())
    assert record["cfi_max_degree"] == int(degrees.max())
    assert record["degree_bounded_by_four"] is bool(degrees.max() <= 4)
    assert record["classical_subsumption_status"] == "solvable_in_polynomial_time_by_luks_1982"
    assert record["classical_algorithm_executed"] is False

    components = _component_count(base)
    beta = len(edges) - len(base) + components
    assert record["component_count"] == components
    assert record["cycle_space_dimension"] == record["cycle_generator_count"] == beta
    assert record["cycle_generators_preserve_adjacency"] is True
    assert record["cycle_subgroup_normal_in_full_uncolored_group_proved"] is False
    witnesses = record["cycle_generators"]
    assert len(witnesses) == beta
    label_index = {label: i for i, label in enumerate(labels)}
    pivots = {}
    permutations = []
    for witness in witnesses:
        flipped = set(witness["flipped_edge_indices"])
        assert len(flipped) == len(witness["flipped_edge_indices"])
        assert flipped and flipped <= set(range(len(edges)))
        assert all(len(flipped.intersection(local)) % 2 == 0 for local in incident)
        expected_permutation = []
        for kind, v, bits in labels:
            if kind == "middle":
                changed = tuple(bit ^ int(e in flipped) for bit, e in zip(bits, incident[v]))
            else:
                changed = bits ^ int(v in flipped)
            expected_permutation.append(label_index[(kind, v, changed)])
        permutation = witness["permutation"]
        assert permutation == expected_permutation
        assert sorted(permutation) == list(range(len(graph)))
        assert any(i != p for i, p in enumerate(permutation))
        assert all(permutation[permutation[i]] == i for i in range(len(graph)))
        np.testing.assert_array_equal(graph[np.ix_(permutation, permutation)], graph)
        assert witness["preserves_adjacency"] is True
        assert witness["is_involution"] is True
        permutations.append(np.asarray(permutation))
        # Set elimination checks independence without the producer's bit RREF.
        residual = flipped.copy()
        while residual and min(residual) in pivots:
            residual ^= pivots[min(residual)]
        assert residual, "dependent cycle generators"
        pivots[min(residual)] = residual
    for left, right in combinations(permutations, 2):
        np.testing.assert_array_equal(left[right], right[left])
    _assert_no_old_estimates(record)


@pytest.mark.parametrize("base_id", CUBIC_BASES + ("complete-k5",))
def test_named_base_counts_and_actual_cycle_actions(base_id):
    _, base = family.base_graph_by_id(base_id)
    record = audit.audit_finite_cfi_base(base_id)
    _assert_finite_record(record, base)
    assert record["base_id"] == base_id
    if base_id in CUBIC_BASES:
        assert record["cfi_vertex_count"] == 7 * len(base)
        assert record["cfi_edge_count"] == 12 * len(base)
        assert record["cfi_min_degree"] == 3
        assert record["cfi_max_degree"] == 4
    else:
        assert (record["cfi_vertex_count"], record["cfi_edge_count"]) == (60, 160)
        assert record["cfi_min_degree"] == 4
        assert record["cfi_max_degree"] == 8
        assert record["degree_bounded_by_four"] is False


@pytest.mark.parametrize("name", SMALL_BASES)
def test_general_adjacency_counts_components_and_cycle_actions(name):
    base = _small_base(name)
    record = audit.audit_base_adjacency(base, base_id=name, base_description="independent control")
    _assert_finite_record(record, base)
    assert record["base_id"] == name
    assert record["base_description"] == "independent control"


@pytest.mark.parametrize("name", SMALL_BASES)
def test_twisted_constructor_matches_local_parity_graph(name):
    base = _small_base(name)
    _, _, edges, _, _ = _reference_graph(base)
    for twist in [None, *edges]:
        expected, _, _, _, _ = _reference_graph(base, twist)
        np.testing.assert_array_equal(family.cfi_parity_graph_from_base(base, twist), expected)
        assert np.array_equal(expected, expected.T)
        assert not np.diag(expected).any()


@pytest.mark.parametrize("bad", [
    [], [[]], np.zeros((0, 0)), np.zeros((2, 3)), np.zeros((2, 2, 1)),
    [[0, 1], [0, 0]], [[1, 0], [0, 0]], [[0, 2], [2, 0]],
    [[0, -1], [-1, 0]], [[0, 0.5], [0.5, 0]],
    [[0, float("nan")], [float("nan"), 0]],
    [[0, float("inf")], [float("inf"), 0]], [[0], [0, 0]],
])
def test_non_simple_adjacency_is_rejected(bad):
    with pytest.raises(ValueError):
        audit.audit_base_adjacency(bad)


@pytest.mark.parametrize("base", [_base(65, []), _base(7, combinations(range(7), 2))])
def test_finite_caps_reject_before_gadget_allocation(base, monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("expanded a graph before checking the finite verification caps")

    monkeypatch.setattr(family, "cfi_parity_graph_from_base", forbidden)
    with pytest.raises(ValueError):
        audit.audit_base_adjacency(base)


def test_finite_caps_accept_boundary_sizes():
    _assert_finite_record(audit.audit_base_adjacency(_base(64, [])), _base(64, []))
    edges = list(combinations(range(6), 2)) + list(combinations(range(6, 12), 2))
    base = _base(16, edges)  # Two K6 gadgets (126 each) and four isolated vertices.
    record = audit.audit_base_adjacency(base)
    assert record["cfi_vertex_count"] == 256
    _assert_finite_record(record, base)


@pytest.mark.parametrize("bad", [
    True, False, None, "6", 4.0, 6.5, float("nan"), float("inf"),
    -10, -1, 0, 1, 2, 3, 5, 7, 101,
])
def test_impossible_cubic_scaling_inputs_are_rejected(bad):
    with pytest.raises(ValueError):
        audit.evaluate_scaling_cfi_luks_barrier(bad)


def _assert_scaling_record(record, n):
    expected_counts = {
        "base_vertex_count": n, "base_edge_count": 3 * n // 2,
        "cfi_vertex_count": 7 * n, "cfi_edge_count": 12 * n, "max_degree": 4,
        "cycle_space_dimension_beta_1": n // 2 + 1,
        "automorphism_subgroup_order_log2": n // 2 + 1,
    }
    assert set(record) == set(expected_counts) | {"mode", "classical_baseline"}
    for key, value in expected_counts.items():
        assert type(record[key]) is int
        assert record[key] == value
    assert record["mode"] == "SYMBOLIC_COUNTS_NOT_RUNTIME_BENCHMARK"
    assert "exponent not specified" in record["classical_baseline"]
    _assert_no_old_estimates(record)


@pytest.mark.parametrize("n", [4, 6, 8, 10, 14, 20, 50, 100, 200, 1000, 10**100])
def test_scaling_contains_only_exact_symbolic_graph_counts(n, monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("symbolic scaling must not instantiate a finite graph")

    monkeypatch.setattr(family, "cfi_parity_graph_from_base", forbidden)
    monkeypatch.setattr(audit, "audit_base_adjacency", forbidden)
    _assert_scaling_record(audit.evaluate_scaling_cfi_luks_barrier(n), n)


def _assert_report_contract(report):
    assert report["status"] == "CFI_BOUNDED_VALENCE_BASELINE_SCOPED"
    for key, path in {
        "producer_sha256": Path(audit.__file__),
        "derivation_sha256": audit.DERIVATION,
        "graph_constructor_sha256": Path(family.__file__),
    }.items():
        assert report[key] == hashlib.sha256(path.read_bytes()).hexdigest(), key
    for key, expected in CLAIM_GATES.items():
        assert report["claim_gate"][key] is expected
    assert report["claim_gate"]["exact_7v_cfi_vertex_identity_proved"] is True
    assert report["claim_gate"]["max_degree_four_bounded_valence_proved"] is True
    assert report["headline_metrics"]["speedup_claim_allowed"] is False
    assert OLD_NEGATIVE_ID not in report["falsifiers_triggered"]
    assert OLD_NEGATIVE_ID in report["retracted_negative_ids"]
    _assert_no_old_estimates(report)
    records = report["audited_bases"]
    by_id = {row["base_id"]: row for row in records}
    assert len(by_id) == len(records)
    assert set(CUBIC_BASES[1:]) | {"complete-k5"} <= set(by_id)
    for base_id, record in by_id.items():
        _, base = family.base_graph_by_id(base_id)
        _assert_finite_record(record, base)
    profiles = report["scaling_profiles"]
    sizes = [row["base_vertex_count"] for row in profiles]
    assert sizes and len(set(sizes)) == len(sizes)
    assert {6, 100, 1000} <= set(sizes)
    for row in profiles:
        n = row["base_vertex_count"]
        assert type(n) is int and n >= 4 and n % 2 == 0
        _assert_scaling_record(row, n)


def test_built_report_corrected_scope_and_negative_gates():
    _assert_report_contract(audit.build_report())
    assert not hasattr(audit, "register_negative_result")


def test_live_report_corrected_scope_and_negative_gates():
    _assert_report_contract(json.loads(audit.REPORT.read_text(encoding="utf-8")))


def test_live_nonnormality_witness_is_an_actual_conjugated_automorphism():
    report = json.loads(audit.REPORT.read_text(encoding="utf-8"))
    witness = report["uncolored_normality_counterexample"]
    _, base = family.base_graph_by_id("complete-k4")
    graph, _, _, _, _ = _reference_graph(base)
    p = np.asarray(witness["public_automorphism"])
    k = np.asarray(witness["cycle_flip"])
    conjugate = np.asarray(witness["conjugate"])
    for permutation in (p, k, conjugate):
        assert sorted(permutation) == list(range(28))
        np.testing.assert_array_equal(graph, graph[np.ix_(permutation, permutation)])
    np.testing.assert_array_equal(conjugate, p[k[np.argsort(p)]])
    assert witness["original_shared_edge_pair"] == [16, 17]
    assert conjugate[16] == witness["conjugate_image_of_16"] == 26
    assert witness["all_three_preserve_adjacency"] is True
    assert witness["conjugate_is_outside_edge_flip_subgroup"] is True


def test_registry_does_not_reactivate_old_universal_negative():
    records = json.loads(audit.REGISTRY.read_text(encoding="utf-8"))
    assert all(record.get("id") != OLD_NEGATIVE_ID for record in records)


def test_certificate_accepts_live_report_and_rejects_corrupted_claims():
    node = shutil.which("node")
    if node is None:
        pytest.skip("Node is required for the independent JavaScript certificate")
    source = r"""
const assert = require('node:assert/strict');
const fs = require('node:fs');
const certificate = require(process.argv[1]);
const report = JSON.parse(fs.readFileSync(0, 'utf8'));
certificate.verifyLocalCounts();
certificate.validateReport(report);
const mutations = [];
for (const key of Object.keys(report.claim_gate)) {
    if (typeof report.claim_gate[key] === 'boolean') {
        mutations.push(r => { r.claim_gate[key] = !r.claim_gate[key]; });
    }
}
mutations.push(
    r => { r.producer_sha256 = '0'.repeat(64); },
    r => { r.derivation_sha256 = '0'.repeat(64); },
    r => { r.graph_constructor_sha256 = '0'.repeat(64); },
    r => { r.status = 'CFI_GRAPH_COSET_LUKS_SUBSUMPTION_BARRIER_PROVED'; },
    r => { delete r.claim_gate.explicit_luks_quartic_bound_proved; },
    r => { r.claim_gate.speedup_claim_allowed = 0; },
    r => { r.audited_bases.find(b => b.base_id === 'complete-k5').degree_bounded_by_four = true; },
    r => { r.audited_bases[0].cfi_vertex_count++; },
    r => { r.audited_bases[0].cfi_edge_count++; },
    r => { r.audited_bases[0].edge_count_identity_verified = false; },
    r => { r.audited_bases[0].cycle_generators[0].permutation.reverse(); },
    r => { r.audited_bases[0].cycle_generators[0].flipped_edge_indices = []; },
    r => { r.audited_bases = []; },
    r => { r.scaling_profiles = []; },
    r => { r.scaling_profiles[0].base_vertex_count = 5; },
    r => { r.scaling_profiles[0].cfi_edge_count++; },
    r => { r.scaling_profiles[0].luks_classical_time_log2 = 4; },
    r => { r.headline_metrics.quantum_overhead_vs_luks_at_100_base_vertices_log2 = 1; },
    r => { r.falsifiers_triggered.push('NEG-CFI-GRAPH-COSET-LUKS-SUBSUMPTION-BARRIER'); }
);
for (const mutate of mutations) {
    const broken = structuredClone(report);
    mutate(broken);
    assert.throws(() => certificate.validateReport(broken));
}
console.log(`${mutations.length} malformed report controls rejected`);
"""
    result = subprocess.run(
        [node, "-e", source, str(CERTIFICATE)], input=audit.REPORT.read_text(encoding="utf-8"),
        text=True, capture_output=True, timeout=60, check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
