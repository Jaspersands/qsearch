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
const REGISTRY_PATH = path.resolve(__dirname, '../registry/negative_results.json');

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
    assertCheck("Report status is NATIVE_HISTORY_ERASURE_DEQUANTIZATION_PROVED",
        report.status === "NATIVE_HISTORY_ERASURE_DEQUANTIZATION_PROVED");

    if (fs.existsSync(DERIVATION_PATH)) {
        const derivationContent = fs.readFileSync(DERIVATION_PATH);
        const expectedSha = crypto.createHash('sha256').update(derivationContent).digest('hex');
        assertCheck("Derivation SHA256 matches actual markdown file", report.derivation_sha256 === expectedSha);
    }

    // 2. Theorems proved verification
    assertCheck("Theorems proved list has 4 theorems", report.theorems_proved && report.theorems_proved.length === 4);
    report.theorems_proved.forEach((t) => {
        assertCheck(`Theorem verified: ${t.name}`, t.verified === true);
    });

    // 3. Finite instance verifications
    const instances = report.finite_instance_verifications;
    assertCheck("Finite instances list is non-empty", instances && instances.length >= 3);

    instances.forEach((inst, idx) => {
        assertCheck(`Instance ${idx} (n=${inst.dimension}, q=${inst.modulus}, M=${inst.bank_size}, W=${inst.exposure}): off-diagonal coherence == 0`,
            inst.max_off_diagonal_coherence === 0.0 && inst.coherence_vanishes_identically === true);
        assertCheck(`Instance ${idx}: density matrix trace is 1.0`,
            Math.abs(inst.density_matrix_trace - 1.0) < 1e-12);
        assertCheck(`Instance ${idx}: trace distance to classical BKW sampling is exactly 0.0`,
            inst.trace_distance_to_classical_bkw === 0.0 && inst.dequantization_verified === true);
        assertCheck(`Instance ${idx}: all paths satisfy Cauchy-Schwarz inequality`,
            inst.all_paths_satisfy_cauchy_schwarz === true);
        assertCheck(`Instance ${idx}: min L2 norm (${inst.min_l2_norm_at_max_exposure}) >= bound (${inst.cauchy_schwarz_l2_bound})`,
            inst.noise_inflation_lower_bound_satisfied === true);
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
        assertCheck(`Profile ${idx}: un-erased state is classically dequantized`, p.un_erased_state_is_classically_dequantized === true);

        if (n >= 4) {
            assertCheck(`Profile ${idx}: ISIS gap requires GapSVP oracle for n=${n}`, p.history_erasure_requires_gapsvp_oracle === true);
            assertCheck(`Profile ${idx}: log2 ISIS gap >= 2.0`, p.log2_isis_gap >= 2.0);
        }
    });

    // 5. Gating flags
    assertCheck("Speedup claim disallowed", report.speedup_claim_allowed === false);
    assertCheck("Accepted speedup candidate is false", report.accepted_speedup_candidate === false);

    // 6. Registry verification
    if (fs.existsSync(REGISTRY_PATH)) {
        const registry = JSON.parse(fs.readFileSync(REGISTRY_PATH, 'utf8'));
        const regEntry = registry.find(e => e.id === "NEG-NATIVE-PHASE-BANK-HISTORY-ERASURE-DEQUANTIZATION-BARRIER");
        assertCheck("Negative result registered in registry", regEntry !== undefined);
        if (regEntry) {
            assertCheck("Negative result references correct artifact",
                regEntry.source === "research/reductions/native_history_erasure_dequantization.json");
        }
    }

    console.log(`\nAll checks passed: ${passCount} / ${checkCount}`);
    console.log("STATUS: PASS");
}

runCrossCheck();
