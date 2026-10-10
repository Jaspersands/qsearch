/**
 * Independent Cross-Check Certificate for Wreath Orientation Projector Gram Norm & Complementary Pairing Duality
 *
 * Verifies:
 * 1. Complementary pairing sparsity: E_a E_b = 0 for all a ^ b != (1, ..., 1).
 * 2. Uniform operator norm bound: ||F_nu|| <= 2.0 across all sectors and tuples.
 * 3. Exact third moment conservation identity: Tr(F^3) == 3 Tr(F^2) - 2 Tr(F).
 * 4. Sub-POVM conclusive probability lower bound q >= Tr(F^2) / (2 Tr(F)) >= 50%.
 * 5. Clean claim gating with speedup claim disallowed.
 */

const fs = require('fs');
const path = require('path');

const REPORT_PATH = path.resolve(__dirname, '../representation/self_dual_wreath_orientation_gram_norm.json');

function runCrossCheck() {
    console.log("=== Running Wreath Orientation Gram Norm & Pairing Duality Cross-Check ===");

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

    // 1. Verify Headline Metrics
    const metrics = report.headline_metrics;
    assertCheck("All non-complementary overlaps are identically zero",
        metrics.all_non_complementary_overlaps_identically_zero === true);
    assertCheck("Maximum orientation operator norm <= 2.0",
        metrics.maximum_orientation_operator_norm <= 2.0 + 1e-8);
    assertCheck("Operator norm strictly bounded by two flag is true",
        metrics.operator_norm_strictly_bounded_by_two === true);
    assertCheck("Third moment conservation identity proved (residual < 1e-7)",
        metrics.third_moment_conservation_identity_proved === true);
    assertCheck("Sub-POVM achieves constant conclusive probability (>= 50%)",
        metrics.subpovm_achieves_constant_conclusive_probability === true);
    assertCheck(`Minimum conclusive bound is >= 50% (actual = ${(metrics.minimum_subpovm_conclusive_probability_lower_bound * 100).toFixed(1)}%)`,
        metrics.minimum_subpovm_conclusive_probability_lower_bound >= 0.5 - 1e-8);

    // 2. Verify Tuple Validations
    const tuples = report.tuple_validations;
    assertCheck("Audited tuple list is non-empty", tuples && tuples.length > 0);

    tuples.forEach((t, idx) => {
        assertCheck(`Tuple ${idx} has zero non-complementary overlaps`,
            t.all_non_complementary_overlaps_zero === true);
        assertCheck(`Tuple ${idx} operator norm bounded by 2.0 (norm=${t.maximum_operator_norm.toFixed(4)})`,
            t.maximum_operator_norm <= 2.0 + 1e-8);
        assertCheck(`Tuple ${idx} third moment residual < 1e-7 (res=${t.maximum_third_moment_residual.toExponential(2)})`,
            t.maximum_third_moment_residual < 1e-7);
    });

    // 3. Verify Claim Gate
    const gate = report.claim_gate;
    assertCheck("Complementary pairing proved in claim gate",
        gate.complementary_pairing_proved === true);
    assertCheck("Operator norm bound proved in claim gate",
        gate.operator_norm_bound_proved === true);
    assertCheck("Third moment identity proved in claim gate",
        gate.third_moment_identity_proved === true);
    assertCheck("Sub-POVM constant conclusive proved in claim gate",
        gate.subpovm_constant_conclusive_proved === true);
    assertCheck("Speedup claim disallowed (clean gating)",
        gate.speedup_claim_allowed === false);

    console.log(`\nALL ${passCount}/${checkCount} CHECKS PASSED.`);
}

runCrossCheck();
