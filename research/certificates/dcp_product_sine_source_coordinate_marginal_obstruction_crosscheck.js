#!/usr/bin/env node
/**
 * Independent Node.js cross-checker for dcp_product_sine_source_coordinate_marginal_obstruction.
 * Re-computes single-coordinate marginal character sums, K-copy parity density difference
 * pairs, cyclic-vs-product copy thresholds, and auxiliary-zero postselection rates.
 */

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..", "..");
const ARTIFACT_PATH = path.join(
  ROOT,
  "research",
  "reductions",
  "dcp_product_sine_source_coordinate_marginal_obstruction.json"
);

function enumerateVectors(q, n) {
  const res = [];
  function rec(idx, cur) {
    if (idx === n) {
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

function parseFrac(s) {
  if (s.includes("/")) {
    const [a, b] = s.split("/").map(Number);
    return a / b;
  }
  return Number(s);
}

function main() {
  const report = JSON.parse(fs.readFileSync(ARTIFACT_PATH, "utf-8"));
  if (!report.summary || !report.summary.all_theorems_passed) {
    console.error("FAIL: Summary does not report all_theorems_passed=true");
    process.exit(1);
  }

  for (const inst of report.instances) {
    const { n, L, q, K, A } = inst;
    const v = parseFrac(inst.visibility_exact);
    if (q !== 1 << L) {
      console.error(`FAIL [${inst.instance_id}]: q != 2^L`);
      process.exit(1);
    }

    // 1. Verify Theorem 1 (Single-coordinate marginal character erasure)
    const allShifts = enumerateVectors(q, n);
    const allKAux = enumerateVectors(q, n - 1);
    let zeroAuxCount = 0;
    let nonzeroAuxCount = 0;

    for (const h of allShifts) {
      const auxZero = h.slice(1).every((x) => x === 0);
      if (auxZero) zeroAuxCount++;
      else nonzeroAuxCount++;

      for (let k1 = 0; k1 < q; k1++) {
        let reSum = 0.0;
        let imSum = 0.0;
        for (const kAux of allKAux) {
          let dot = k1 * h[0];
          for (let i = 1; i < n; i++) dot += kAux[i - 1] * h[i];
          const angle = (-2.0 * Math.PI * (dot % q)) / q;
          reSum += v * Math.cos(angle);
          imSum += v * Math.sin(angle);
        }
        reSum /= allKAux.length;
        imSum /= allKAux.length;
        const expectedRe = auxZero ? v * Math.cos((-2.0 * Math.PI * ((k1 * h[0]) % q)) / q) : 0.0;
        const expectedIm = auxZero ? v * Math.sin((-2.0 * Math.PI * ((k1 * h[0]) % q)) / q) : 0.0;
        if (Math.abs(reSum - expectedRe) > 1e-11 || Math.abs(imSum - expectedIm) > 1e-11) {
          console.error(`FAIL [${inst.instance_id}]: Marginal off-diagonal mismatch`);
          process.exit(1);
        }
      }
    }
    if (
      zeroAuxCount !== q ||
      nonzeroAuxCount !== Math.pow(q, n) - q ||
      zeroAuxCount !== inst.marginal_audit.zero_aux_shift_count
    ) {
      console.error(`FAIL [${inst.instance_id}]: Marginal shift counts mismatch`);
      process.exit(1);
    }

    // 2. Verify Theorem 2 (K-copy full-vector subset-sum pair counts)
    const dimK = 1 << K;
    const wordFreqs = [];
    for (let x = 0; x < dimK; x++) {
      const f = [];
      for (let ell = 0; ell < n; ell++) {
        let s = 0;
        for (let r = 0; r < K; r++) {
          if ((x >> r) & 1) s += A[ell][r];
        }
        f.push(s % q);
      }
      wordFreqs.push(f);
    }
    let fullTargetPairs = 0;
    let coord1OnlyPairs = 0;
    for (let x = 0; x < dimK; x++) {
      for (let y = 0; y < dimK; y++) {
        const diff = wordFreqs[x].map((v, ell) => (v - wordFreqs[y][ell] + q) % q);
        if (diff[0] === q >> 1) {
          coord1OnlyPairs++;
          if (diff.slice(1).every((z) => z === 0)) {
            fullTargetPairs++;
          }
        }
      }
    }
    if (
      fullTargetPairs !== inst.k_copy_parity_audit.full_vector_target_ordered_pairs ||
      coord1OnlyPairs !== inst.k_copy_parity_audit.coord1_only_target_ordered_pairs ||
      inst.k_copy_parity_audit.cyclic_k_min_for_adv_1_16 !==
        inst.k_copy_parity_audit.product_k_min_for_adv_1_16
    ) {
      console.error(`FAIL [${inst.instance_id}]: K-copy pair counts or K_min invariance mismatch`);
      process.exit(1);
    }

    // 3. Verify Theorem 3 (Auxiliary-zero postselection)
    if (
      inst.postselection_audit.aux_zero_accepted_outcomes !== q ||
      inst.postselection_audit.total_label_outcomes !== Math.pow(q, n)
    ) {
      console.error(`FAIL [${inst.instance_id}]: Postselection count mismatch`);
      process.exit(1);
    }
  }

  for (const row of report.asymptotic_scaling) {
    if (
      row.cyclic_minimum_copies !== row.product_minimum_copies ||
      !row.cyclic_equals_product_minimum_copies ||
      row.aux_zero_postselection_acceptance_neg_log2 !== (row.n - 1) * row.coordinate_bits_L
    ) {
      console.error(`FAIL [asymptotic n=${row.n}]: Scaling invariance mismatch`);
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
    `OK: dcp_product_sine_source_coordinate_marginal_obstruction cross-checked (${report.instances.length} instances, sha256=${report.sha256.slice(0, 16)})`
  );
}

main();
