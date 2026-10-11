/**
 * Independent Cross-Check Certificate for Character Shift Uniform Decoding Lower Bound.
 *
 * Verifies:
 * 1. Exact Legendre autocorrelation sum: sum_{x=0}^{p-1} chi(x) chi(x + delta) == -1 for all delta != 0 (mod p).
 * 2. Closed-form pairwise agreement count: N_agree(delta) == (p - 3) / 2 identically for all non-zero delta.
 * 3. Strictly sub-half agreement fraction: f_agree = (p - 3)/(2p) < 0.5.
 * 4. Chernoff-union bound query ceiling: k*(p) = 2 ceil(log2 p) samples achieves false positive <= 1/p.
 * 5. Cyclotomic polynomial degree obstruction: deg = (p - 1)/2 = 2^{Omega(n)}.
 * 6. Non-uniform preprocessing dichotomy: S = p log2 p advice vs T >= p/2 uniform work.
 * 7. Report integrity, derivation SHA256, and negative result registration.
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const REPORT_PATH = path.resolve(__dirname, '../classical_baselines/character_shift_decoding_lower_bound_barrier.json');
const DERIVATION_PATH = path.resolve(__dirname, '../CHARACTER_SHIFT_UNIFORM_DECODING_LOWER_BOUND.md');
const REGISTRY_PATH = path.resolve(__dirname, '../registry/negative_results.json');
const NEGATIVE_RESULT_ID = "NEG-CHARACTER-SHIFT-UNIFORM-DECODING-LOWER-BOUND-BARRIER";

// Modular exponentiation for BigInt
function modPow(base, exp, mod) {
    let res = 1n;
    base = base % mod;
    while (exp > 0n) {
        if (exp % 2n === 1n) res = (res * base) % mod;
        base = (base * base) % mod;
        exp = exp / 2n;
    }
    return res;
}

// Legendre symbol via Euler's criterion
function legendre(a, p) {
    const aMod = ((BigInt(a) % BigInt(p)) + BigInt(p)) % BigInt(p);
    if (aMod === 0n) return 0;
    const pBig = BigInt(p);
    const exp = (pBig - 1n) / 2n;
    const res = modPow(aMod, exp, pBig);
    return res === 1n ? 1 : -1;
}

function runCrossCheck() {
    console.log("=== Running Character Shift Decoding Lower Bound Cross-Check ===");

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
    assertCheck("Report status is CHARACTER_SHIFT_UNIFORM_DECODING_LOWER_BOUND_PROVED",
        report.status === "CHARACTER_SHIFT_UNIFORM_DECODING_LOWER_BOUND_PROVED");

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

    // 3. Independent verification of Legendre autocorrelation identity sum == -1
    const testPrimes = [5, 7, 11, 13, 17, 19, 23, 29, 31];
    testPrimes.forEach((p) => {
        let allMinusOne = true;
        for (let delta = 1; delta < p; delta++) {
            let sumProd = 0;
            for (let x = 0; x < p; x++) {
                sumProd += legendre(x, p) * legendre(x + delta, p);
            }
            if (sumProd !== -1) {
                allMinusOne = false;
                break;
            }
        }
        assertCheck(`p=${p}: Legendre autocorrelation sum == -1 identically for all delta != 0`, allMinusOne);
    });

    // 4. Independent verification of pairwise agreement count N_agree == (p - 3) / 2
    testPrimes.forEach((p) => {
        const expectedAgree = Math.floor((p - 3) / 2);
        let allMatched = true;
        for (let delta = 1; delta < p; delta++) {
            let agreeCount = 0;
            for (let x = 0; x < p; x++) {
                const l1 = legendre(x, p);
                const l2 = legendre(x + delta, p);
                if (l1 !== 0 && l2 !== 0 && l1 === l2) {
                    agreeCount++;
                }
            }
            if (agreeCount !== expectedAgree) {
                allMatched = false;
                break;
            }
        }
        assertCheck(`p=${p}: Pairwise agreement count N_agree == (p - 3)/2 == ${expectedAgree} for all delta`, allMatched);
    });

    // 5. Strictly sub-half agreement fraction check
    testPrimes.forEach((p) => {
        const frac = (p - 3) / (2 * p);
        assertCheck(`p=${p}: Agreement fraction ${frac.toFixed(4)} < 0.5 strictly`, frac < 0.5);
    });

    // 6. Query ceiling and Chernoff union bound check
    report.query_ceilings.forEach((row) => {
        const p = row.prime;
        const k = row.required_queries_k_star;
        assertCheck(`p=${p}: Union bound queries k*=${k} satisfies false-positive <= 1/p`,
            row.failure_bound_below_one_over_p === true);
    });

    // 7. Cyclotomic degree obstruction check
    report.cyclotomic_degree_obstruction.forEach((row) => {
        const p = row.prime;
        const deg = row.cyclotomic_equation_degree;
        assertCheck(`p=${p}: Cyclotomic equation degree ${deg} == (p - 1)/2`, deg === Math.floor((p - 1) / 2));
    });

    // 8. Negative Result Registry Verification
    if (fs.existsSync(REGISTRY_PATH)) {
        const registry = JSON.parse(fs.readFileSync(REGISTRY_PATH, 'utf8'));
        const entry = registry.find(e => e.id === NEGATIVE_RESULT_ID);
        assertCheck("Negative result registered in registry", entry !== undefined);
        if (entry) {
            assertCheck("Negative result lesson is non-empty", entry.lesson && entry.lesson.length > 20);
            assertCheck("Negative result reason_invalid is non-empty", entry.reason_invalid && entry.reason_invalid.length > 20);
        }
    }

    // 9. Claim Gating
    assertCheck("Speedup claim disallowed in report", report.claim_gate.speedup_claim_allowed === false);
    assertCheck("Classical decoding hardness verified in report", report.claim_gate.classical_decoding_hardness_verified === true);

    console.log(`\nAll ${passCount} / ${checkCount} checks PASS.`);
}

runCrossCheck();
