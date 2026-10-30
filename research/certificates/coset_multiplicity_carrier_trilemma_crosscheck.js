/**
 * Independent bounded commutator replay and corrected-report consistency checks.
 *
 * Verifies:
 * 1. Exact commutator witness entry [K_12, K_23]_{(0,0,0),(0,0,1)} = n for n >= 3.
 * 2. Independent reimplementation of standard representation and three-copy class sum commutator.
 * Physical states/instruments are independently tested in Python. This script
 * does not prove a general theorem from report booleans or finite examples.
 * No speedup claim is admitted; that is NOT a disproof of all speedups.
 */

const fs = require('fs');
const path = require('path');

const REPORT_PATH = path.resolve(__dirname, '../representation/coset_multiplicity_carrier_trilemma.json');

function standardRepMatrix(perm, n) {
    const dim = n - 1;
    const M = Array.from({ length: dim }, () => Array(dim).fill(0));
    for (let col = 0; col < dim; col++) {
        const pCol = perm[col];
        const pLast = perm[n - 1];
        if (pCol < dim) M[pCol][col] += 1;
        if (pLast < dim) M[pLast][col] -= 1;
    }
    return M;
}

function computeThreeCopyWitnessEntry(n) {
    const dim = n - 1;
    const dim2 = dim * dim;
    const K = Array.from({ length: dim2 }, () => Array(dim2).fill(0));

    // Generate transpositions
    for (let i = 0; i < n; i++) {
        for (let j = i + 1; j < n; j++) {
            const perm = Array.from({ length: n }, (_, idx) => idx);
            perm[i] = j;
            perm[j] = i;
            const V = standardRepMatrix(perm, n);
            // K += V (x) V
            for (let r1 = 0; r1 < dim; r1++) {
                for (let c1 = 0; c1 < dim; c1++) {
                    const v1 = V[r1][c1];
                    if (v1 === 0) continue;
                    for (let r2 = 0; r2 < dim; r2++) {
                        for (let c2 = 0; c2 < dim; c2++) {
                            const v2 = V[r2][c2];
                            if (v2 !== 0) {
                                K[r1 * dim + r2][c1 * dim + c2] += v1 * v2;
                            }
                        }
                    }
                }
            }
        }
    }

    // Compute [K_12, K_23] at row (0,0,0) and col (0,0,1)
    let val = 0;
    const dim3 = dim * dim * dim;
    for (let mid = 0; mid < dim3; mid++) {
        const m1 = Math.floor(mid / (dim * dim));
        const rem = mid % (dim * dim);
        const m2 = Math.floor(rem / dim);
        const m3 = rem % dim;

        const k12_0_mid = (m3 === 0) ? K[0][m1 * dim + m2] : 0;
        const k23_mid_1 = (m1 === 0) ? K[m2 * dim + m3][1] : 0;

        const k23_0_mid = (m1 === 0) ? K[0][m2 * dim + m3] : 0;
        const k12_mid_1 = (m3 === 1) ? K[m1 * dim + m2][0] : 0;

        val += (k12_0_mid * k23_mid_1 - k23_0_mid * k12_mid_1);
    }
    return val;
}

function runCrossCheck() {
    console.log("=== Scoped coset checks; broad trilemma retracted ===");

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

    // 1. Verify Core Headline Metrics
    assertCheck("All commutator witnesses verified", report.headline_metrics.all_commutator_witnesses_verified === true);
    assertCheck("All commutant zero-information checks verified", report.headline_metrics.all_commutant_zero_information_verified === true);
    assertCheck("Tail commutator witness matches n=16", report.headline_metrics.tail_commutator_witness === 16);
    assertCheck("Tail identity-term dimension bound uses exact factorial", Math.abs(report.headline_metrics.tail_dimension_lower_bound_log2_numeric - 80.77035858958996) < 1e-10);
    assertCheck("Speedup claim not admitted", report.headline_metrics.speedup_claim_allowed === false);
    assertCheck("Accepted speedup candidate is false", report.headline_metrics.accepted_speedup_candidate === false);
    assertCheck("Broad negative quarantined", report.negative_result_status === 'QUARANTINED_OVERBROAD_NO_GO');
    assertCheck("No exhaustive trilemma claimed", report.headline_metrics.exhaustive_trilemma_proved === false);
    assertCheck("No general circuit lower bound claimed", report.headline_metrics.general_circuit_lower_bound_proved === false);

    // 2. Independent Algebraic Replay of Three-Copy Commutator Entries
    [3, 4, 5, 6].forEach(n => {
        const computedWitness = computeThreeCopyWitnessEntry(n);
        assertCheck(`JS computed commutator entry [K_12, K_23]_{(0,0,0),(0,0,1)} = ${n} (exact=${computedWitness})`, computedWitness === n);
    });

    // 3. Verify Small Commutator Audits from Report
    report.small_commutator_audits.forEach((audit, idx) => {
        assertCheck(`Commutator audit [${idx}] n=${audit.n}: observed matches theoretical`, audit.observed_witness_entry === audit.theoretical_witness_entry);
        assertCheck(`Commutator audit [${idx}] n=${audit.n}: matches closed form n`, audit.entry_matches_closed_form === true);
        assertCheck(`Commutator audit [${idx}] n=${audit.n}: strictly non-commuting`, audit.is_strictly_noncommuting === true);
    });

    // 4. Verify Small Zero-Information Audits from Report
    report.small_zero_information_audits.forEach((audit, idx) => {
        assertCheck(`Born audit [${idx}] n=${audit.n}: variation < 1e-12`, audit.probability_variation < 1e-12);
        assertCheck(`Zero-info audit [${idx}] n=${audit.n}: is constant across class`, audit.is_constant_across_class === true);
        assertCheck(`Born audit [${idx}]: physical-state check recorded`, audit.physical_states_and_probabilities_verified === true);
        let information = 0;
        const rows = audit.conditional_born_probabilities;
        const marginal = [0, 1].map(y => rows.reduce((sum, row) => sum + row[y], 0) / rows.length);
        for (const row of rows) {
            assertCheck(`Born audit [${idx}]: normalized binary law`, row.every(p => p >= 0 && p <= 1) && Math.abs(row[0] + row[1] - 1) < 1e-12);
            row.forEach((p, y) => { if (p > 0) information += p * Math.log2(p / marginal[y]) / rows.length; });
        }
        assertCheck(`Born audit [${idx}]: Shannon MI recomputed`, Math.abs(information - audit.mutual_information_bits_numeric) < 1e-12);
    });

    // 5. Verify Asymptotic Scaling Profiles
    report.scaling_profiles.forEach((prof, idx) => {
        assertCheck(`Scaling row [${idx}] n=${prof.n}: commutator matches n`, prof.commutator_matches_n === true);
        assertCheck(`Scaling row [${idx}]: no numerical information signal`, Math.abs(prof.commutant_mutual_information_bits) < 1e-12);
        assertCheck(`Scaling row [${idx}]: dimension not treated as circuit bound`, prof.general_circuit_lower_bound_proved === false && !('racah_complexity_exponential' in prof));
        const [numerator, denominator = '1'] = prof.identity_term_dimension_lower_bound_exact.split('/');
        let factorial = 1n;
        for (let n = 2; n <= prof.n; n++) factorial *= BigInt(n);
        assertCheck(`Scaling row [${idx}]: exact identity summand`, BigInt(numerator) * factorial === BigInt(denominator) * BigInt(prof.n - 1) ** BigInt(2 * prof.n));
    });

    console.log("======================================================================");
    console.log(`ALL ${checkCount} / ${checkCount} CHECKS PASSED.`);
    console.log("Bounded replay and report consistency passed; no general receiver or circuit lower bound proved.");
    console.log("======================================================================");
}

runCrossCheck();
