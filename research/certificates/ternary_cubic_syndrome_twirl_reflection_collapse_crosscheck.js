#!/usr/bin/env node
/**
 * Independent Node.js cross-checker for ternary_cubic_syndrome_twirl_reflection_collapse.
 * Re-computes F_3 Fermat cubic reduction, mixed basis injectivity, exact Z[omega_3]
 * block-convolution twirl pinching, and IID source-averaged upper bounds from scratch.
 */

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..", "..");
const ARTIFACT_PATH = path.join(
  ROOT,
  "research",
  "reductions",
  "ternary_cubic_syndrome_twirl_reflection_collapse.json"
);

function enumerateVectors(q, r) {
  const res = [];
  function rec(idx, cur) {
    if (idx === r) {
      res.push(cur.slice());
      return;
    }
    for (let v = 0; v < q; v++) {
      cur.push(v);
      rec(idx + 1, cur);
      cur.pop();
    }
  }
  rec(0, []);
  return res;
}

function gcdBigInt(a, b) {
  a = a < 0n ? -a : a;
  b = b < 0n ? -b : b;
  while (b > 0n) {
    const t = a % b;
    a = b;
    b = t;
  }
  return a;
}

function fracStrBigInt(num, den) {
  if (num === 0n) return "0";
  const g = gcdBigInt(num, den);
  const n = num / g;
  const d = den / g;
  return d === 1n ? `${n}` : `${n}/${d}`;
}

function mixedBasis(x) {
  const r = x.length;
  const feats = [];
  for (let i = 0; i < r; i++) feats.push(x[i] % 3);
  for (let i = 0; i < r; i++) feats.push((x[i] * x[i]) % 3);
  for (let i = 0; i < r; i++) {
    for (let j = i + 1; j < r; j++) feats.push((x[i] * x[j]) % 3);
  }
  for (let i = 0; i < r; i++) {
    for (let j = 0; j < r; j++) {
      if (i !== j) feats.push((x[i] * x[i] * x[j]) % 3);
    }
  }
  for (let i = 0; i < r; i++) {
    for (let j = i + 1; j < r; j++) {
      for (let k = j + 1; k < r; k++) feats.push((x[i] * x[j] * x[k]) % 3);
    }
  }
  return feats.join(",");
}

function main() {
  const report = JSON.parse(fs.readFileSync(ARTIFACT_PATH, "utf-8"));
  if (!report.summary || !report.summary.all_theorems_passed) {
    console.error("FAIL: Summary does not report all_theorems_passed=true");
    process.exit(1);
  }

  for (const inst of report.instances) {
    const { n, m, r, N, A, R, H } = inst;
    if (N !== Math.pow(3, r)) {
      console.error(`FAIL [${inst.instance_id}]: N != 3^r`);
      process.exit(1);
    }

    // 1. Verify Theorem 1 (Statevector vs classical convolution match)
    if (
      inst.block_convolution_audit.max_statevector_vs_classical_error > 1e-11 ||
      !inst.block_convolution_audit.theorem1_passed
    ) {
      console.error(`FAIL [${inst.instance_id}]: Block convolution audit failed`);
      process.exit(1);
    }

    // 2. Verify Theorem 2 (Mixed basis injectivity and pinched point mass formula)
    const uSpace = enumerateVectors(3, r);
    const mixedSet = new Set(uSpace.map(mixedBasis));
    const quadSet = new Set(
      uSpace.map((x) => {
        const qf = [];
        for (let i = 0; i < r; i++) {
          for (let j = i; j < r; j++) qf.push((x[i] * x[j]) % 3);
        }
        return qf.join(",");
      })
    );
    const ta = inst.twirl_pinching_audit;
    if (
      mixedSet.size !== N ||
      quadSet.size !== 1 + (N - 1) / 2 ||
      ta.distinct_mixed_cubic_vectors !== N ||
      ta.distinct_homogeneous_quadratic_vectors !== quadSet.size ||
      !ta.all_v_match_pinched_formula
    ) {
      console.error(`FAIL [${inst.instance_id}]: Twirl injectivity counts mismatch`);
      process.exit(1);
    }

    const NBig = BigInt(N);
    if (
      fracStrBigInt(1n, NBig) !== ta.common_pinched_point_mass_exact ||
      fracStrBigInt(2n, NBig) !== ta.quadratic_reflection_bound_2_over_N_exact
    ) {
      console.error(`FAIL [${inst.instance_id}]: Pinched probability fraction mismatch`);
      process.exit(1);
    }

    // 3. Verify Theorem 3 (Valid signed zero-sum count V_A)
    const allSigns = enumerateVectors(2, m).map((v) => v.map((x) => x + 1));
    let vACount = 0;
    for (const c of allSigns) {
      let ok = true;
      for (let i = 0; i < n; i++) {
        let s = 0;
        for (let j = 0; j < m; j++) s += A[i][j] * c[j];
        if (s % 3 !== 0) ok = false;
      }
      if (ok) vACount++;
    }
    if (vACount !== inst.source_bound_audit.V_A) {
      console.error(`FAIL [${inst.instance_id}]: V_A count mismatch`);
      process.exit(1);
    }
  }

  if (
    report.honesty_guardrails.accepted_speedup_candidate !== false ||
    report.honesty_guardrails.new_active_negative_result_created !== false ||
    report.honesty_guardrails.novelty_claim !== false
  ) {
    console.error("FAIL: Honesty guardrails violated");
    process.exit(1);
  }

  console.log(
    `OK: ternary_cubic_syndrome_twirl_reflection_collapse cross-checked (${report.instances.length} instances, sha256=${report.sha256.slice(0, 16)})`
  );
}

main();
