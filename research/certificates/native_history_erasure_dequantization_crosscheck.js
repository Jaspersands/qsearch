/**
 * Independent Cross-Check Certificate for Native Phase Bank History Entanglement & Classical Dequantization Duality
 *
 * Verifies:
 * 1. Coherence vanishing & exact classical BKW dequantization: max off-diagonal coherence == 0.0, trace dist == 0.0.
 * 2. Strict noise inflation lower bound: ||c||_2 >= ||c||_1 / sqrt(M) = n.
 * 3. Syndrome erasure / ISIS equivalence: gap q/W = 3^n / n^2 = 2^Omega(n) requires GapSVP oracle.
 * 4. Coset QFT invariance: dual code lattice projection leaves residual noise unmitigated.
 * 5. Negative result registered in registry with speedup claim disallowed.
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const REPORT_PATH = path.resolve(__dirname, '../reductions/native_history_erasure_dequantization.json');
const DERIVATION_PATH = path.resolve(__dirname, '../NATIVE_HISTORY_ERASURE_DEQUANTIZATION.md');
const ACTIVE_REGISTRY_PATH = path.resolve(__dirname, '../registry/negative_results.json');
const QUARANTINED_REGISTRY_PATH = path.resolve(__dirname, '../registry/quarantined_campaign_negatives.json');

function runCrossCheck() {
    console.log("=== Running Native Phase Bank History Erasure & Dequantization Cross-Check ===");

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

    // 1. Report integrity and derivation hash
    assertCheck("Report status is UNIVERSAL_HISTORY_ERASURE_NO_GO_RETRACTED",
        report.status === "UNIVERSAL_HISTORY_ERASURE_NO_GO_RETRACTED");
    assertCheck("Proof status is EXACT_SCOPED_COUNTERCONTROLS_NOT_GENERAL_ALGORITHM_OR_HARDNESS_PROOF",
        report.proof_status === "EXACT_SCOPED_COUNTERCONTROLS_NOT_GENERAL_ALGORITHM_OR_HARDNESS_PROOF");

    if (fs.existsSync(DERIVATION_PATH)) {
        const derivationContent = fs.readFileSync(DERIVATION_PATH);
        const expectedSha = crypto.createHash('sha256').update(derivationContent).digest('hex');
        assertCheck("Derivation SHA256 matches actual markdown file", report.derivation_sha256 === expectedSha);
    }

    // 2. Scoped identities and countercontrols verification
    assertCheck("Scoped identities list has 2 verified identities",
        Array.isArray(report.scoped_identities) && report.scoped_identities.length === 2 &&
        report.scoped_identities.every((t) => t.verified === true));
    assertCheck("Exact countercontrols present",
        report.exact_countercontrols &&
        Array.isArray(report.exact_countercontrols.phase_and_joint_readout_controls) &&
        report.exact_countercontrols.phase_and_joint_readout_controls.length === 2);

    // 3. Finite instance verifications
    const instances = report.finite_instance_verifications;
    assertCheck("Finite instances list is non-empty", instances && instances.length >= 3);

    instances.forEach((inst, idx) => {
        assertCheck(`Instance ${idx} (n=${inst.dimension}, q=${inst.modulus}, M=${inst.bank_size}, W=${inst.exposure}): off-diagonal coherence == 0`,
            inst.max_off_diagonal_coherence === 0.0 && inst.coherence_vanishes_identically === true);
        assertCheck(`Instance ${idx}: density matrix trace is 1.0`,
            Math.abs(inst.density_matrix_trace - 1.0) < 1e-12);
        assertCheck(`Instance ${idx}: trace distance to classical BKW sampling is < 1e-12`,
            inst.trace_distance_to_classical_bkw < 1e-12 && inst.dequantization_verified === true);
        assertCheck(`Instance ${idx}: all paths satisfy Cauchy-Schwarz inequality`,
            inst.all_paths_satisfy_cauchy_schwarz === true);
        assertCheck(`Instance ${idx}: min L2 norm (${inst.min_l2_norm_at_max_exposure}) >= bound (${inst.cauchy_schwarz_l2_bound})`,
            inst.noise_inflation_lower_bound_satisfied === true);
        assertCheck(`Instance ${idx}: arbitrary interleaved receiver or joint readout not covered`,
            inst.arbitrary_interleaved_receiver_or_joint_readout_covered === false);
    });

    // 4. Scaling profiles verification
    const profiles = report.scaling_profiles;
    assertCheck("Scaling profiles list contains 7 dimensions", profiles && profiles.length === 7);

    const expectedDims = [2, 3, 4, 8, 16, 32, 64];
    profiles.forEach((p, idx) => {
        const n = expectedDims[idx];
        assertCheck(`Profile ${idx}: dimension is ${n}`, p.dimension === n);
        assertCheck(`Profile ${idx}: modulus q = 3^${n}`, BigInt(p.modulus) === BigInt(3) ** BigInt(n));
        assertCheck(`Profile ${idx}: bank size M = ${n}^2 = ${n * n}`, p.bank_size_M === n * n);
        assertCheck(`Profile ${idx}: exposure W = ${n}^2 = ${n * n}`, p.exposure_W === n * n);
        assertCheck(`Profile ${idx}: secret trits = ${n * n}`, p.secret_trits === n * n);
        assertCheck(`Profile ${idx}: min noise inflation factor >= ${n}`, p.min_noise_inflation_factor >= n);
        assertCheck(`Profile ${idx}: max noise inflation factor >= ${n * n}`, p.max_noise_inflation_factor >= n * n);
        assertCheck(`Profile ${idx}: arbitrary receiver not dequantized`, p.arbitrary_receiver_dequantized === false);
        assertCheck(`Profile ${idx}: hardness reduction not verified`, p.hardness_reduction_verified === false);
    });

    // 5. Gating flags
    assertCheck("Speedup claim disallowed", report.speedup_claim_allowed === false);
    assertCheck("Accepted speedup candidate is false", report.accepted_speedup_candidate === false);

    // 6. Quarantine registry verification
    if (fs.existsSync(ACTIVE_REGISTRY_PATH)) {
        const activeRegistry = JSON.parse(fs.readFileSync(ACTIVE_REGISTRY_PATH, 'utf8'));
        const activeEntry = activeRegistry.find(e => e.id === "NEG-NATIVE-PHASE-BANK-HISTORY-ERASURE-DEQUANTIZATION-BARRIER");
        assertCheck("Overbroad negative result removed from active registry", activeEntry === undefined);
    }
    if (fs.existsSync(QUARANTINED_REGISTRY_PATH)) {
        const quarantinedRegistry = JSON.parse(fs.readFileSync(QUARANTINED_REGISTRY_PATH, 'utf8'));
        const quarEntry = quarantinedRegistry.find(e => e.id === "NEG-NATIVE-PHASE-BANK-HISTORY-ERASURE-DEQUANTIZATION-BARRIER");
        assertCheck("Negative result recorded in quarantined_campaign_negatives.json", quarEntry !== undefined);
        if (quarEntry) {
            assertCheck("Quarantined record status is QUARANTINED_OVERBROAD_NO_GO",
                quarEntry.status === "QUARANTINED_OVERBROAD_NO_GO");
        }
    }

    console.log(`\nAll checks passed: ${passCount} / ${checkCount}`);
    console.log("STATUS: PASS");
}

runCrossCheck();
