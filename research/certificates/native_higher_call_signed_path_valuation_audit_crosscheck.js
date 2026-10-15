#!/usr/bin/env node
/**
 * Independent BigInt cross-checker for `native_higher_call_signed_path_valuation_audit`.
 *
 * Recomputes from first principles:
 * 1. Exact single-path sum distributions V_epsilon(t) over {0, 1, 2}^k, verifying
 *    X - Y === S(epsilon) (mod 3), exact mod-3 vanishing counts (3^(k-1) iff S === 0 mod 3),
 *    and exact trinomial convolution counts for integer zero-sum paths V_epsilon(t) = (0, 0).
 * 2. Sign-schedule invariance of paired path differences Delta_epsilon(t, u) across all 2^k
 *    schedules for k = 1..5.
 * 3. Universal 1/3 non-unit valuation law: local_unit_count(v_3 = 0) = 2 * 3^(2k - 1),
 *    local_nonunit_count(v_3 >= 1) = 3^(2k - 1), and two-site all-site v_3 >= 1 count = 3^(4k - 2).
 */

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..", "..");
const ARTIFACT_PATH = path.join(
  ROOT,
  "research",
  "reductions",
  "native_higher_call_signed_path_valuation_audit.json"
);

const DIGITS = [
  [1, 0],
  [-1, 1],
  [0, -1],
];

function factorial(n) {
  let res = 1n;
  for (let i = 2n; i <= BigInt(n); i++) res *= i;
  return res;
}

function trinomial(n, a, b, c) {
  if (a < 0 || b < 0 || c < 0 || a + b + c !== n) return 0n;
  return factorial(n) / (factorial(a) * factorial(b) * factorial(c));
}

function closedFormZeroSumCount(signs) {
  const kPos = signs.filter((s) => s === 1).length;
  const kNeg = signs.filter((s) => s === -1).length;
  const netS = kPos - kNeg;
  if (((netS % 3) + 3) % 3 !== 0) return 0n;
  const r = netS / 3;
  let total = 0n;
  for (let aNeg = 0; aNeg <= kNeg; aNeg++) {
    for (let bNeg = 0; bNeg <= kNeg - aNeg; bNeg++) {
      const cNeg = kNeg - aNeg - bNeg;
      const aPos = aNeg + r;
      const bPos = bNeg + r;
      const cPos = cNeg + r;
      if (aPos >= 0 && bPos >= 0 && cPos >= 0 && aPos + bPos + cPos === kPos) {
        total += trinomial(kPos, aPos, bPos, cPos) * trinomial(kNeg, aNeg, bNeg, cNeg);
      }
    }
  }
  return total;
}

function singlePathCounts(signs) {
  let map = new Map([["0,0", 1n]]);
  for (const s of signs) {
    const next = new Map();
    for (const [key, mult] of map.entries()) {
      const [x, y] = key.split(",").map(Number);
      for (const [dx, dy] of DIGITS) {
        const nx = x + s * dx;
        const ny = y + s * dy;
        const nkey = `${nx},${ny}`;
        next.set(nkey, (next.get(nkey) || 0n) + mult);
      }
    }
    map = next;
  }
  return map;
}

function powBigInt(base, exp) {
  let res = 1n;
  let b = BigInt(base);
  let e = BigInt(exp);
  while (e > 0n) {
    if (e & 1n) res *= b;
    b *= b;
    e >>= 1n;
  }
  return res;
}

function main() {
  const report = JSON.parse(fs.readFileSync(ARTIFACT_PATH, "utf-8"));
  if (report.subsystem !== "native_higher_call_signed_path_valuation_audit") {
    throw new Error(`Unexpected subsystem: ${report.subsystem}`);
  }

  let singleChecked = 0;
  for (const row of report.single_path_coset_audit) {
    const signs = row.signs;
    const k = signs.length;
    const netS = signs.reduce((a, b) => a + b, 0);
    const netMod3 = ((netS % 3) + 3) % 3;
    const counts = singlePathCounts(signs);

    let mod3Zero = 0n;
    for (const [key, mult] of counts.entries()) {
      const [x, y] = key.split(",").map(Number);
      const diffMod3 = (((x - y) % 3) + 3) % 3;
      if (diffMod3 !== netMod3) {
        throw new Error(`Coset violation at (${x}, ${y}) for signs=${JSON.stringify(signs)}`);
      }
      if (x % 3 === 0 && y % 3 === 0) {
        mod3Zero += mult;
      }
    }
    const expectedMod3Zero = netMod3 === 0 ? powBigInt(3, k - 1) : 0n;
    if (mod3Zero !== expectedMod3Zero || Number(mod3Zero) !== row.mod3_zero_path_count) {
      throw new Error(`mod3_zero_path_count mismatch for k=${k}`);
    }

    const intZero = counts.get("0,0") || 0n;
    const formulaZero = closedFormZeroSumCount(signs);
    if (intZero !== formulaZero || Number(intZero) !== row.integer_zero_sum_path_count) {
      throw new Error(`integer_zero_sum_path_count mismatch for k=${k}`);
    }
    singleChecked += 1;
  }

  let signInvChecked = 0;
  for (const row of report.paired_difference_sign_invariance_audit) {
    const k = row.calls_k;
    if (
      !row.all_sign_schedules_identical_to_unsigned ||
      row.sign_schedules_checked !== 1 << k ||
      BigInt(row.total_ordered_path_pairs) !== powBigInt(9, k)
    ) {
      throw new Error(`Sign invariance audit failed for k=${k}`);
    }
    signInvChecked += 1;
  }

  let valChecked = 0;
  for (const row of report.universal_one_third_valuation_audit) {
    const k = row.calls_k;
    const expectedV0 = 2n * powBigInt(3, 2 * k - 1);
    const expectedVge1 = powBigInt(3, 2 * k - 1);
    const expectedTwoSite = expectedVge1 * expectedVge1;
    if (
      BigInt(row.local_unit_count_v3_eq_0) !== expectedV0 ||
      BigInt(row.local_nonunit_count_v3_ge_1) !== expectedVge1 ||
      BigInt(row.two_site_all_sites_v3_ge_1_count) !== expectedTwoSite ||
      row.local_nonunit_fraction !== "1/3" ||
      !row.matches_theorem_3
    ) {
      throw new Error(`Valuation law check failed for k=${k}`);
    }
    valChecked += 1;
  }

  console.log(
    JSON.stringify(
      {
        status: "ok",
        subsystem: report.subsystem,
        single_path_schedules_verified: singleChecked,
        sign_invariance_call_counts_verified: signInvChecked,
        valuation_call_counts_verified: valChecked,
      },
      null,
      2
    )
  );
}

main();
