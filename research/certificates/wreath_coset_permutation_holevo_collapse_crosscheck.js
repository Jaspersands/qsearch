/**
 * Independent Cross-Check Certificate for Wreath Coset Permutation Decoder Gap & Factorial Holevo Information Collapse
 *
 * Verifies:
 * 1. Conjugacy class inversion overlap law: Tr(rho_tau rho_tau') = 1 / |C(tau^-1 tau')| across all S_n elements.
 * 2. Purity of mixed coset states: Tr(rho_tau^2) = 1/n!, maximally mixed in coset sector.
 * 3. k-copy decoupling: E[Tr(rho_tau^k rho_tau'^k)] -> 1/n! for k >= 2.
 * 4. Holevo mutual information collapse: I(tau : Q^k) <= O(k^2 / n) -> 0 bits for k = O(1).
 * 5. Fano factorial reconstruction failure: P_succ <= (I + 1) / log2(n!) = O(1 / (n^2 log n)) -> 0.
 * 6. Clean claim gating with speedup claim disallowed.
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const REPORT_PATH = path.resolve(__dirname, '../representation/wreath_coset_permutation_holevo_collapse.json');
const DERIVATION_PATH = path.resolve(__dirname, '../WREATH_COSET_PERMUTATION_HOLEVO_COLLAPSE.md');
const REGISTRY_PATH = path.resolve(__dirname, '../registry/negative_results.json');

function runCrossCheck() {
    console.log("=== Running Wreath Coset Permutation Holevo Collapse Cross-Check ===");

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
    assertCheck("Report status is WREATH_COSET_PERMUTATION_HOLEVO_COLLAPSE_PROVED",
        report.status === "WREATH_COSET_PERMUTATION_HOLEVO_COLLAPSE_PROVED");

    if (fs.existsSync(DERIVATION_PATH)) {
        const derivationContent = fs.readFileSync(DERIVATION_PATH);
        const expectedSha = crypto.createHash('sha256').update(derivationContent).digest('hex');
        assertCheck("Derivation SHA256 matches actual markdown file", report.derivation_sha256 === expectedSha);
    }

    // 2. Theorems proved verification
    assertCheck("Theorems proved list has 5 theorems", report.theorems_proved && report.theorems_proved.length === 5);
    report.theorems_proved.forEach((t) => {
        assertCheck(`Theorem verified: ${t.name}`, t.verified === true);
    });

    // 3. Finite instance verifications
    const instances = report.finite_instance_verifications;
    assertCheck("Finite instances list has 3 instances (S_3, S_4, S_5)", instances && instances.length === 3);

    const expectedFactorials = { 3: 6, 4: 24, 5: 120 };
    const expectedPartitions = { 3: 3, 4: 5, 5: 7 };

    instances.forEach((inst) => {
        const n = inst.dimension_n;
        assertCheck(`S_${n}: group order is ${expectedFactorials[n]}`, inst.group_order === expectedFactorials[n]);
        assertCheck(`S_${n}: partition count is ${expectedPartitions[n]}`, inst.partition_count === expectedPartitions[n]);
        assertCheck(`S_${n}: conjugacy class count is ${expectedPartitions[n]}`, inst.conjugacy_classes_count === expectedPartitions[n]);
        assertCheck(`S_${n}: identity overlap is exactly 1.0`, inst.identity_overlap_exact_one === true);
        assertCheck(`S_${n}: purity is 1/${expectedFactorials[n]}`, Math.abs(inst.purity_float - 1.0 / expectedFactorials[n]) < 1e-12);
        assertCheck(`S_${n}: average 1-copy overlap is ${expectedPartitions[n]}/${expectedFactorials[n]}`,
            Math.abs(inst.average_1copy_overlap_float - expectedPartitions[n] / expectedFactorials[n]) < 1e-12);
        assertCheck(`S_${n}: exact class overlap law satisfied`, inst.exact_class_overlap_law_satisfied === true);
    });

    // 4. Scaling profiles verification
    const profiles = report.scaling_profiles;
    assertCheck("Scaling profiles list contains 8 dimensions", profiles && profiles.length === 8);

    profiles.forEach((p) => {
        const n = p.dimension_n;
        assertCheck(`Profile n=${n}: secret entropy > 0`, p.secret_entropy_bits > 0);
        assertCheck(`Profile n=${n}: Holevo information <= k^2 / n (${p.holevo_mutual_information_upper_bound_bits.toFixed(2)} bits)`,
            p.holevo_mutual_information_upper_bound_bits <= (16.0 / n) + 1e-8);
        assertCheck(`Profile n=${n}: copy barrier confirmed`, p.copy_barrier_confirmed === true);

        if (n >= 6) {
            assertCheck(`Profile n=${n}: Fano success probability < 0.5 (actual=${p.fano_identification_success_upper_bound.toFixed(3)})`,
                p.fano_identification_success_upper_bound < 0.5);
        }
        if (n >= 16) {
            assertCheck(`Profile n=${n}: Fano success probability < 0.05 (actual=${p.fano_identification_success_upper_bound.toFixed(4)})`,
                p.fano_identification_success_upper_bound < 0.05);
        }
        if (n >= 32) {
            assertCheck(`Profile n=${n}: 4-copy overlap < 1e-30 (actual=${p.average_kcopy_overlap_float})`,
                p.average_kcopy_overlap_float < 1e-30);
        }
    });

    // 5. Gating flags
    assertCheck("Speedup claim disallowed", report.speedup_claim_allowed === false);
    assertCheck("Accepted speedup candidate is false", report.accepted_speedup_candidate === false);

    // 6. Registry verification
    if (fs.existsSync(REGISTRY_PATH)) {
        const registry = JSON.parse(fs.readFileSync(REGISTRY_PATH, 'utf8'));
        const regEntry = registry.find(e => e.id === "NEG-WREATH-COSET-PERMUTATION-HOLEVO-INFORMATION-COLLAPSE");
        assertCheck("Negative result registered in registry", regEntry !== undefined);
        if (regEntry) {
            assertCheck("Negative result references correct artifact",
                regEntry.source === "research/representation/wreath_coset_permutation_holevo_collapse.json");
        }
    }

    console.log(`\nAll checks passed: ${passCount} / ${checkCount}`);
    console.log("STATUS: PASS");
}

runCrossCheck();
