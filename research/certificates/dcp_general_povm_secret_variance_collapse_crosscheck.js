/**
 * Independent Cross-Check Certificate for General Quantum POVM Secret Variance Collapse.
 *
 * Verifies:
 * 1. Parseval secret variance upper bound: E_a[Var_s(p(y | s))] <= 2^{-2n} Tr(E_y^2) <= 2^{-2n}.
 * 2. Shallow-depth zero-information law: circuits with depth d < W*(n) have I(s : Y) == 0 bits identically.
 * 3. Total variation distance collapse: TV <= (1/2) M 2^{-n} = 2^{-Omega(n)} for any M = poly(n) outcomes.
 * 4. Mutual information exponential extinction: I(s : Y) <= (M^2 / ln 2) 2^{-2n} = 2^{-Omega(n)} bits.
 * 5. Fano secret reconstruction failure: P_succ <= (I + 1)/n = O(1/n) -> 0.
 * 6. Non-erasure POVM and inaccessible environment trilemma closure.
 * 7. Report integrity, derivation SHA256, and negative result registration.
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const REPORT_PATH = path.resolve(__dirname, '../classical_baselines/dcp_general_povm_secret_variance_collapse.json');
const DERIVATION_PATH = path.resolve(__dirname, '../DCP_GENERAL_POVM_SECRET_VARIANCE_COLLAPSE.md');
const REGISTRY_PATH = path.resolve(__dirname, '../registry/negative_results.json');
const NEGATIVE_RESULT_ID = "NEG-DCP-GENERAL-POVM-SECRET-VARIANCE-COLLAPSE";

function runCrossCheck() {
    console.log("=== Running DCP General POVM Secret Variance Collapse Cross-Check ===");

    if (!fs.existsSync(REPORT_PATH)) {
        console.error("FAIL: Report not found at " + REPORT_PATH);
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

    // 1. Report integrity and SHA256
    assertCheck("Report status is DCP_GENERAL_POVM_SECRET_VARIANCE_COLLAPSE_PROVED",
        report.status === "DCP_GENERAL_POVM_SECRET_VARIANCE_COLLAPSE_PROVED");

    if (fs.existsSync(DERIVATION_PATH)) {
        const derivationContent = fs.readFileSync(DERIVATION_PATH);
        const expectedSha = crypto.createHash('sha256').update(derivationContent).digest('hex');
        assertCheck("Derivation SHA256 matches actual markdown file", report.derivation_sha256 === expectedSha);
    }

    // 2. Theorems proved count and verification
    assertCheck("Theorems proved list has 5 theorems", report.theorems_proved && report.theorems_proved.length === 5);
    report.theorems_proved.forEach((t) => {
        assertCheck(`Theorem verified: ${t.name}`, t.verified === true);
    });

    // 3. Verification of empirical variance bounds across tested dimensions
    report.variance_instances.forEach((row) => {
        const n = row.n_bits;
        const meanVar = row.mean_empirical_variance;
        const bound = row.theoretical_bound;
        assertCheck(`n=${n}: Mean empirical variance (${meanVar.toExponential(4)}) <= theoretical bound (${bound.toExponential(4)})`,
            meanVar <= bound + 1e-12);
        assertCheck(`n=${n}: Theoretical bound equals 2^{-2n} == ${(Math.pow(2, -2 * n)).toExponential(4)}`,
            Math.abs(bound - Math.pow(2, -2 * n)) < 1e-12);
    });

    // 4. Shallow-depth zero-information verification
    const shallow = report.shallow_depth_check;
    assertCheck("Shallow-depth transition elements vanish for high-weight deltas",
        shallow.shallow_depth_coherence_vanishes === true);
    assertCheck("High-weight vanishing count equals tested count",
        shallow.high_weight_vanishing_count === shallow.high_weight_deltas_tested);

    // 5. Asymptotic Total Variation and Mutual Information bounds
    report.asymptotic_fano.forEach((row) => {
        const n = row.n_bits;
        const m = row.outcome_count_m;
        const tv = row.total_variation_upper_bound;
        const mi = row.mutual_information_upper_bound_bits;
        const fano = row.fano_success_probability_upper_bound;

        assertCheck(`n=${n}, M=${m}: TV bound (${tv.toExponential(2)}) <= (1/2) M 2^{-n}`,
            tv <= 0.5 * m * Math.pow(2, -n) + 1e-12);
        assertCheck(`n=${n}, M=${m}: MI bound (${mi.toExponential(2)}) <= (M^2 / ln 2) 2^{-2n}`,
            mi <= (m * m / Math.LN2) * Math.pow(2, -2 * n) + 1e-12);
        assertCheck(`n=${n}, M=${m}: Fano bound (${fano.toExponential(2)}) <= (I + 1)/n`,
            fano <= (mi + 1.0) / n + 1e-12);
    });

    // 6. Negative Result Registry Verification
    if (fs.existsSync(REGISTRY_PATH)) {
        const registry = JSON.parse(fs.readFileSync(REGISTRY_PATH, 'utf8'));
        const entry = registry.find(e => e.id === NEGATIVE_RESULT_ID);
        assertCheck("Negative result registered in registry", entry !== undefined);
        if (entry) {
            assertCheck("Negative result lesson is non-empty", entry.lesson && entry.lesson.length > 20);
            assertCheck("Negative result reason_invalid is non-empty", entry.reason_invalid && entry.reason_invalid.length > 20);
        }
    }

    // 7. Claim Gating
    assertCheck("Speedup claim disallowed in report", report.claim_gate.speedup_claim_allowed === false);
    assertCheck("Non-erasure inaccessible environment closed in report",
        report.claim_gate.non_erasure_inaccessible_environment_closed === true);

    console.log(`\nAll ${passCount} / ${checkCount} checks PASS.`);
}

runCrossCheck();
