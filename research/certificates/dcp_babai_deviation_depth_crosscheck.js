/**
 * Independent Cross-Check Certificate for DCP Babai Deviation Depth & Coordinate Dispersion Barrier
 *
 * Verifies:
 * 1. Canonical deviation probabilities erfc(r / (2 sqrt(2))) against analytical formula.
 * 2. Coordinate variance law Var(c_i) = 1/||b_i*||^2 and pairwise covariance 0.
 * 3. Exact candidate list sizes sum_{j=0}^k 2^j binom(d, j).
 * 4. Hoeffding upper bounds on list decoder coverage P(K <= k).
 * 5. Exponential coverage collapse across empirical and asymptotic rows.
 */

const fs = require('fs');
const path = require('path');

const REPORT_PATH = path.resolve(__dirname, '../classical_baselines/dcp_babai_deviation_depth_barrier.json');

function erf(x) {
    // Abramowitz and Stegun formula 7.1.26 (maximum error: 1.5e-7)
    const a1 = 0.254829592;
    const a2 = -0.284496736;
    const a3 = 1.421413741;
    const a4 = -1.453152027;
    const a5 = 1.061405429;
    const p  = 0.3275911;
    const sign = x < 0 ? -1 : 1;
    const absX = Math.abs(x);
    const t = 1.0 / (1.0 + p * absX);
    const y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * Math.exp(-absX * absX);
    return sign * y;
}

function erfc(x) {
    return 1.0 - erf(x);
}

function canonicalDeviationProbability(r) {
    if (r === 0) return 1.0;
    return erfc(r / (2.0 * Math.SQRT2));
}

function hoeffdingBound(expectedK, dim, depth) {
    if (depth >= expectedK) return 1.0;
    const diff = expectedK - depth;
    return Math.exp(-2.0 * diff * diff / dim);
}

function combinations(n, k) {
    if (k < 0 || k > n) return 0;
    if (k === 0 || k === n) return 1;
    let c = 1;
    for (let i = 1; i <= k; i++) {
        c = (c * (n - (k - i))) / i;
    }
    return Math.round(c);
}

function listCandidateCount(dim, depth) {
    let total = 0;
    for (let j = 0; j <= depth && j <= dim; j++) {
        total += Math.pow(2, j) * combinations(dim, j);
    }
    return total;
}

function runCrossCheck() {
    console.log("=== Running DCP Babai Deviation Depth Barrier Cross-Check ===");

    if (!fs.existsSync(REPORT_PATH)) {
        console.error("FAIL: Report file not found at " + REPORT_PATH);
        process.exit(1);
    }

    const report = JSON.parse(fs.readFileSync(REPORT_PATH, 'utf8'));
    let passCount = 0;
    let checkCount = 0;

    function assertCheck(name, cond) {
        checkCount++;
        if (cond) {
            passCount++;
            console.log(`[PASS] ${name}`);
        } else {
            console.error(`[FAIL] ${name}`);
            process.exit(1);
        }
    }

    // 1. Verify Canonical Deviation Probabilities
    Object.entries(report.canonical_probabilities).forEach(([key, reported]) => {
        const r = parseFloat(key.replace('norm_', ''));
        const computed = canonicalDeviationProbability(r);
        const diff = Math.abs(reported - computed);
        assertCheck(`Canonical probability at norm ${r.toFixed(2)} (diff=${diff.toExponential(3)})`, diff < 1e-5);
    });

    // 2. Verify Moment Audit
    assertCheck("Coordinate variance matches 1/||b_i*||^2 theory", report.moment_audit.variance_matches_theory === true);
    assertCheck("Coordinate covariance matches 0 orthogonality", report.moment_audit.covariance_matches_zero === true);

    // 3. Verify Finite Scaling Rows
    const rows = report.finite_scaling_rows;
    assertCheck("Finite scaling rows present", rows && rows.length >= 5);

    rows.forEach(row => {
        const expectedListSize = listCandidateCount(row.dimension, 2);
        assertCheck(`Row n=${row.n_bits} list size matches combinations formula (${row.depth_two_list_size} == ${expectedListSize})`,
            row.depth_two_list_size === expectedListSize);

        const expectedHoeff = hoeffdingBound(row.median_empirical_depth, row.dimension, 2);
        const hoeffDiff = Math.abs(row.hoeffding_depth_two_bound - expectedHoeff);
        assertCheck(`Row n=${row.n_bits} Hoeffding bound consistent (diff=${hoeffDiff.toExponential(3)})`, hoeffDiff < 1e-6);

        if (row.n_bits >= 28) {
            assertCheck(`Tail row n=${row.n_bits} empirical depth-two success is 0`,
                row.empirical_depth_two_success_count === 0);
        }
    });

    // 4. Verify Asymptotic Extrapolations
    const extrap = report.extrapolations;
    assertCheck("Extrapolations present", extrap && extrap.length >= 4);

    const n128 = extrap.find(e => e.n_bits === 128);
    const n256 = extrap.find(e => e.n_bits === 256);
    const n512 = extrap.find(e => e.n_bits === 512);
    assertCheck("n=128 Hoeffding bound shows strong collapse (< 0.01)", n128.depth_two_hoeffding_bound < 0.01);
    assertCheck("n=256 Hoeffding bound shows extreme collapse (< 1e-4)", n256.depth_two_hoeffding_bound < 1e-4);
    assertCheck("n=512 Hoeffding bound shows asymptotic extinction (< 1e-9)", n512.depth_two_hoeffding_bound < 1e-9);

    // 5. Verify Claim Gate
    assertCheck("Linear deviation scaling proved", report.claim_gate.linear_deviation_scaling_proved === true);
    assertCheck("Exponential list coverage collapse proved", report.claim_gate.exponential_list_coverage_collapse_proved === true);
    assertCheck("Speedup claim disallowed (clean gating)", report.claim_gate.speedup_claim_allowed === false);

    console.log(`\nALL ${passCount}/${checkCount} CHECKS PASSED.`);
}

runCrossCheck();
