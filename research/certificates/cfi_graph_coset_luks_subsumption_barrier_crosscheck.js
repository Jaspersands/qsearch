/**
 * Independent shared-edge CFI graph enumeration and corrected-report replay.
 * Checks counts, actual graph permutations, and scope gates. It does not run
 * Luks or a quantum receiver, or infer complexity from a carrier dimension.
 */
'use strict';

const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');

const ROOT = path.resolve(__dirname, '../..');
const REPORT_PATH = path.join(ROOT, 'research/coset_workbench/cfi_graph_coset_luks_subsumption_barrier.json');
const OLD_NEGATIVE_ID = 'NEG-CFI-GRAPH-COSET-LUKS-SUBSUMPTION-BARRIER';
const CLAIM_GATES = {
    speedup_claim_allowed: false,
    universal_cfi_trilemma_barrier_proved: false,
    single_copy_quantum_mutual_information_extinction_proved: false,
    multi_copy_commutant_exponential_intractability_proved: false,
    luks_classical_polynomial_subsumption_certified: true,
    explicit_luks_quartic_bound_proved: false,
    cycle_subgroup_normal_in_full_uncolored_group_proved: false,
    classical_algorithm_executed: false,
    exact_7v_cfi_vertex_identity_proved: true,
    max_degree_four_bounded_valence_proved: true,
};
const REMOVED_ESTIMATES = new Set([
    'luks_polynomial_degree', 'luks_operations_estimate', 'luks_classical_time_log2',
    'single_copy_quantum_mutual_information_log2', 'three_copy_quantum_commutant_dimension_log2',
    'quantum_strictly_harder_than_classical', 'luks_classical_time_log2_at_100_base_vertices',
    'three_copy_commutant_dimension_log2_at_100_base_vertices',
    'quantum_overhead_vs_luks_at_100_base_vertices_log2',
]);

function evenPatterns(degree) {
    let patterns = [[]];
    for (let i = 0; i < degree; i++) {
        patterns = patterns.flatMap(bits => [[...bits, 0], [...bits, 1]]);
    }
    return patterns.filter(bits => bits.reduce((sum, bit) => sum + bit, 0) % 2 === 0)
        .map(bits => bits.reverse());
}

function graphFromEdges(n, inputEdges) {
    assert(Number.isSafeInteger(n) && n > 0);
    const edges = inputEdges.map(([u, v]) => u < v ? [u, v] : [v, u])
        .sort(([u, v], [x, y]) => u - x || v - y);
    const seen = new Set();
    const adjacent = Array.from({length: n}, () => new Set());
    for (const [u, v] of edges) {
        assert(Number.isInteger(u) && Number.isInteger(v) && 0 <= u && u < v && v < n);
        assert(!seen.has(`${u},${v}`), 'duplicate base edge');
        seen.add(`${u},${v}`);
        adjacent[u].add(v);
        adjacent[v].add(u);
    }
    return {n, edges, adjacent};
}

function componentCount(base) {
    const unseen = new Set(base.adjacent.keys());
    let count = 0;
    while (unseen.size) {
        const seed = unseen.values().next().value;
        unseen.delete(seed);
        const stack = [seed];
        count++;
        while (stack.length) {
            for (const v of base.adjacent[stack.pop()]) {
                if (unseen.delete(v)) stack.push(v);
            }
        }
    }
    return count;
}

function enumerateCfi(base) {
    const incident = Array.from({length: base.n}, () => []);
    base.edges.forEach(([u, v], e) => { incident[u].push(e); incident[v].push(e); });
    const labels = [];
    incident.forEach((local, v) => {
        for (const bits of evenPatterns(local.length)) labels.push(['middle', v, bits]);
    });
    const middleCount = labels.length;
    base.edges.forEach((_, e) => { labels.push(['edge', e, 0], ['edge', e, 1]); });
    const index = new Map(labels.map((label, i) => [JSON.stringify(label), i]));
    const adjacent = Array.from({length: labels.length}, () => new Set());
    for (let source = 0; source < middleCount; source++) {
        const [, v, bits] = labels[source];
        incident[v].forEach((e, j) => {
            const target = index.get(JSON.stringify(['edge', e, bits[j]]));
            assert(target >= middleCount && !adjacent[source].has(target));
            adjacent[source].add(target);
            adjacent[target].add(source);
        });
    }
    let twiceEdges = 0;
    for (let v = 0; v < adjacent.length; v++) {
        assert(!adjacent[v].has(v), 'loop in CFI graph');
        for (const w of adjacent[v]) {
            assert(adjacent[w].has(v), 'asymmetric adjacency');
            assert((v < middleCount) !== (w < middleCount), 'unexpected same-part edge');
        }
        twiceEdges += adjacent[v].size;
    }
    assert.equal(twiceEdges % 2, 0);
    const degrees = adjacent.map(neighbors => neighbors.size);
    return {
        labels, index, incident, adjacent, middleCount,
        vertices: labels.length, edges: twiceEdges / 2,
        minDegree: Math.min(...degrees), maxDegree: Math.max(...degrees),
    };
}

function completeBase(n) {
    const edges = [];
    for (let u = 0; u < n; u++) for (let v = u + 1; v < n; v++) edges.push([u, v]);
    return graphFromEdges(n, edges);
}

function cycleEdges(n) {
    return Array.from({length: n}, (_, v) => [v, (v + 1) % n]);
}

function cubicBase(n) {
    assert(Number.isSafeInteger(n) && n >= 4 && n % 2 === 0);
    return graphFromEdges(n, [...cycleEdges(n), ...Array.from({length: n / 2}, (_, v) => [v, v + n / 2])]);
}

function namedBase(id) {
    switch (id) {
    case 'complete-k4': return completeBase(4);
    case 'complete-k5': return completeBase(5);
    case 'triangular-prism':
        return graphFromEdges(6, [[0, 1], [1, 2], [2, 0], [3, 4], [4, 5], [5, 3], [0, 3], [1, 4], [2, 5]]);
    case 'cube-q3': {
        const edges = [];
        for (let u = 0; u < 8; u++) for (let v = u + 1; v < 8; v++) {
            if ([1, 2, 4].includes(u ^ v)) edges.push([u, v]);
        }
        return graphFromEdges(8, edges);
    }
    case 'mobius-ladder-8': return cubicBase(8);
    case 'heawood-like-14': return cubicBase(14);
    case 'petersen': {
        const edges = [];
        for (let v = 0; v < 5; v++) edges.push([v, (v + 1) % 5], [v, v + 5], [v + 5, 5 + (v + 2) % 5]);
        return graphFromEdges(10, edges);
    }
    default: throw new Error(`No independent base construction for ${id}`);
    }
}

function verifyGeneralCounts(base) {
    const cfi = enumerateCfi(base);
    const degrees = base.adjacent.map(neighbors => neighbors.size);
    const middleCounts = degrees.map(d => d === 0 ? 1 : 2 ** (d - 1));
    assert.equal(cfi.middleCount, middleCounts.reduce((a, b) => a + b, 0));
    assert.equal(cfi.vertices, cfi.middleCount + 2 * base.edges.length);
    assert.equal(cfi.edges, degrees.reduce((sum, d, v) => sum + d * middleCounts[v], 0));
    return cfi;
}

function verifyLocalCounts() {
    for (const degree of [0, 1, 2, 3, 4]) {
        const patterns = evenPatterns(degree);
        assert.equal(patterns.length, degree === 0 ? 1 : 2 ** (degree - 1));
        for (let position = 0; position < degree; position++) {
            if (degree >= 2) for (const bit of [0, 1]) {
                assert.equal(patterns.filter(bits => bits[position] === bit).length, 2 ** (degree - 2));
            }
        }
        verifyGeneralCounts(completeBase(degree + 1));
    }
    verifyGeneralCounts(graphFromEdges(5, cycleEdges(5)));
    verifyGeneralCounts(graphFromEdges(5, [[0, 1], [1, 2], [2, 3], [3, 4]]));
    verifyGeneralCounts(graphFromEdges(8, [[0, 1], [1, 2], [2, 0], [3, 4], [4, 5]]));
    verifyGeneralCounts(graphFromEdges(5, [...cycleEdges(5), [0, 2], [0, 3]]));
    const k5 = verifyGeneralCounts(completeBase(5));
    assert.deepEqual([k5.vertices, k5.edges, k5.minDegree, k5.maxDegree], [60, 160, 4, 8]);
    for (const n of [4, 6, 8, 10, 14, 20, 30, 50, 100, 200, 500, 1000]) {
        const cfi = verifyGeneralCounts(cubicBase(n));
        assert.deepEqual([cfi.vertices, cfi.edges, cfi.minDegree, cfi.maxDegree], [7 * n, 12 * n, 3, 4]);
    }
}

function assertNoOldEstimates(value) {
    if (value === null || typeof value !== 'object') return;
    for (const [key, nested] of Object.entries(value)) {
        assert(!REMOVED_ESTIMATES.has(key), `unsupported estimate ${key}`);
        assertNoOldEstimates(nested);
    }
}

function verifyCycleWitnesses(record, base, cfi) {
    const components = componentCount(base);
    const beta = base.edges.length - base.n + components;
    assert.equal(record.component_count, components);
    assert.equal(record.cycle_space_dimension, beta);
    assert.equal(record.cycle_generator_count, beta);
    assert.equal(record.cycle_generators_preserve_adjacency, true);
    assert.equal(record.cycle_subgroup_normal_in_full_uncolored_group_proved, false);
    assert.equal(record.cycle_generators.length, beta);
    const pivots = new Map();
    for (const witness of record.cycle_generators) {
        const flipped = new Set(witness.flipped_edge_indices);
        assert(flipped.size > 0 && flipped.size === witness.flipped_edge_indices.length);
        for (const e of flipped) assert(Number.isInteger(e) && e >= 0 && e < base.edges.length);
        for (const local of cfi.incident) assert.equal(local.filter(e => flipped.has(e)).length % 2, 0);
        const expected = cfi.labels.map(([kind, v, bits]) => {
            const changed = kind === 'middle'
                ? bits.map((bit, j) => bit ^ Number(flipped.has(cfi.incident[v][j])))
                : bits ^ Number(flipped.has(v));
            return cfi.index.get(JSON.stringify([kind, v, changed]));
        });
        assert.deepEqual(witness.permutation, expected, 'wrong cycle action');
        assert.equal(new Set(expected).size, cfi.vertices);
        expected.forEach((image, v) => {
            assert.equal(expected[image], v, 'not an involution');
            for (const w of cfi.adjacent[v]) assert(cfi.adjacent[image].has(expected[w]), 'not an automorphism');
        });
        assert.equal(witness.preserves_adjacency, true);
        assert.equal(witness.is_involution, true);
        const residual = new Set(flipped);
        while (residual.size) {
            const pivot = Math.min(...residual);
            if (!pivots.has(pivot)) { pivots.set(pivot, new Set(residual)); break; }
            for (const e of pivots.get(pivot)) {
                if (!residual.delete(e)) residual.add(e);
            }
        }
        assert(residual.size > 0, 'dependent cycle generators');
    }
}

function validateReport(report) {
    assert.equal(report.status, 'CFI_BOUNDED_VALENCE_BASELINE_SCOPED');
    const sources = {
        producer_sha256: 'theorems/cfi_graph_coset_luks_subsumption_barrier.py',
        derivation_sha256: 'research/CFI_GRAPH_COSET_LUKS_SUBSUMPTION_BARRIER.md',
        graph_constructor_sha256: 'theorems/cfi_base_family_search.py',
    };
    for (const [key, filename] of Object.entries(sources)) {
        const digest = crypto.createHash('sha256').update(fs.readFileSync(path.join(ROOT, filename))).digest('hex');
        assert.equal(report[key], digest, `stale source hash: ${key}`);
    }
    for (const [key, expected] of Object.entries(CLAIM_GATES)) assert.equal(report.claim_gate[key], expected, key);
    assert.equal(report.headline_metrics.speedup_claim_allowed, false);
    assert(!report.falsifiers_triggered.includes(OLD_NEGATIVE_ID));
    assert(report.retracted_negative_ids.includes(OLD_NEGATIVE_ID));
    assertNoOldEstimates(report);
    assert(Array.isArray(report.audited_bases) && report.audited_bases.length > 0);
    const ids = new Set(report.audited_bases.map(row => row.base_id));
    assert.equal(ids.size, report.audited_bases.length, 'duplicate audited base');
    for (const id of ['complete-k5', 'triangular-prism', 'cube-q3', 'mobius-ladder-8', 'petersen', 'heawood-like-14']) {
        assert(ids.has(id), `missing finite control ${id}`);
    }
    for (const row of report.audited_bases) {
        const base = namedBase(row.base_id);
        const cfi = verifyGeneralCounts(base);
        assert.equal(row.base_vertex_count, base.n);
        assert.equal(row.base_edge_count, base.edges.length);
        assert.deepEqual(row.base_degrees, base.adjacent.map(neighbors => neighbors.size));
        assert.equal(row.is_3_regular, base.adjacent.every(neighbors => neighbors.size === 3));
        assert.equal(row.cfi_vertex_count, cfi.vertices);
        assert.equal(row.expected_cfi_vertex_count, cfi.vertices);
        assert.equal(row.cfi_edge_count, cfi.edges);
        assert.equal(row.expected_cfi_edge_count, cfi.edges);
        assert.equal(row.vertex_count_identity_verified, true);
        assert.equal(row.edge_count_identity_verified, true);
        assert.equal(row.cfi_min_degree, cfi.minDegree);
        assert.equal(row.cfi_max_degree, cfi.maxDegree);
        assert.equal(row.degree_bounded_by_four, cfi.maxDegree <= 4);
        assert.equal(row.classical_subsumption_status, 'solvable_in_polynomial_time_by_luks_1982');
        assert.equal(row.classical_algorithm_executed, false);
        verifyCycleWitnesses(row, base, cfi);
    }
    assert(Array.isArray(report.scaling_profiles) && report.scaling_profiles.length > 0);
    const sizes = new Set();
    for (const row of report.scaling_profiles) {
        const n = row.base_vertex_count;
        assert(Number.isSafeInteger(n) && n >= 4 && n % 2 === 0, 'impossible cubic base size');
        assert(!sizes.has(n), 'duplicate scaling row');
        sizes.add(n);
        const expected = {
            base_vertex_count: n, base_edge_count: 3 * n / 2,
            cfi_vertex_count: 7 * n, cfi_edge_count: 12 * n, max_degree: 4,
            cycle_space_dimension_beta_1: n / 2 + 1, automorphism_subgroup_order_log2: n / 2 + 1,
        };
        assert.deepEqual(Object.keys(row).sort(), [...Object.keys(expected), 'mode', 'classical_baseline'].sort());
        for (const [key, value] of Object.entries(expected)) assert.equal(row[key], value, key);
        assert.equal(row.mode, 'SYMBOLIC_COUNTS_NOT_RUNTIME_BENCHMARK');
        assert(row.classical_baseline.includes('exponent not specified'));
        // Reconstruct feasible cubic bases at the finite sizes used in this report.
        assert(n <= 1000, 'scaling replay cap exceeded; extend the certificate explicitly');
        const cfi = verifyGeneralCounts(cubicBase(n));
        assert.equal(row.cfi_vertex_count, cfi.vertices);
        assert.equal(row.cfi_edge_count, cfi.edges);
    }
    for (const n of [6, 100, 1000]) assert(sizes.has(n), `missing scaling control ${n}`);
    assert.equal(report.headline_metrics.audited_base_count, ids.size);
    for (const key of ['all_cubic_bases_satisfy_7v_identity', 'all_cubic_cfi_graphs_have_max_degree_four',
        'all_general_vertex_and_edge_counts_match', 'all_cycle_generator_actions_verified']) {
        assert.equal(report.headline_metrics[key], true, key);
    }
}

module.exports = {verifyLocalCounts, validateReport};

if (require.main === module) {
    try {
        assert(process.argv.length === 2 || (process.argv.length === 3 && process.argv[2] === '--local-only'));
        verifyLocalCounts();
        if (process.argv[2] === '--local-only') {
            console.log('PASS: independent local parity counts and cubic constructions; live report not read.');
        } else {
            validateReport(JSON.parse(fs.readFileSync(REPORT_PATH, 'utf8')));
            console.log('PASS: independent CFI graph counts, cycle actions, and corrected live-report gates.');
            console.log('Scoped classical baseline only; no quantum information or circuit lower bound certified.');
        }
    } catch (error) {
        console.error(`FAIL: ${error.message}`);
        process.exitCode = 1;
    }
}
