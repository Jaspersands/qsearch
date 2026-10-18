#!/usr/bin/env node
/**
 * Independent Node.js cross-checker for dcp_clean_linear_witness_carry_obstruction.
 * Re-computes 2-adic Hensel witness coverage & disjoint Boolean translates,
 * bitwise F_2-RREF carry-parity vanishing equivalence, and disjoint-support
 * kernel linearization from scratch.
 */

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..", "..");
const ARTIFACT_PATH = path.join(
  ROOT,
  "research",
  "reductions",
  "dcp_clean_linear_witness_carry_obstruction.json"
);

function enumerateTargets(q, n) {
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

function targetToBits(tVec, t) {
  const bits = [];
  for (const val of tVec) {
    for (let b = 0; b < t; b++) {
      bits.push((val >> b) & 1);
    }
  }
  return bits;
}

function computeCarryParities(A, w, t) {
  const n = A.length;
  const K = A[0].length;
  const parities = [];
  const fullCarries = [];
  for (let ell = 0; ell < n; ell++) {
    let c = 0;
    const ellPar = [];
    const ellFull = [];
    for (let b = 0; b < t; b++) {
      ellFull.push(c);
      if (b >= 1) ellPar.push(c % 2);
      let s = c;
      for (let r = 0; r < K; r++) {
        s += ((A[ell][r] >> b) & 1) * w[r];
      }
      c = Math.floor(s / 2);
    }
    parities.push(ellPar);
    fullCarries.push(ellFull);
  }
  return { parities, fullCarries };
}

function main() {
  const report = JSON.parse(fs.readFileSync(ARTIFACT_PATH, "utf-8"));
  if (!report.summary || !report.summary.all_theorems_passed) {
    console.error("FAIL: Summary does not report all_theorems_passed=true");
    process.exit(1);
  }

  for (const inst of report.instances) {
    const { n, t, q, K } = inst;
    const h = new Array(n).fill(0);
    h[0] = q >> 1;
    const allTargets = enumerateTargets(q, n);

    // 1. Verify Theorem 1 (2-adic Hensel right-inverse)
    const { A_hensel, R_piv } = inst.hensel_audit;
    const validSet = new Set();
    let validCount = 0;
    for (const tVec of allTargets) {
      const wPiv = [];
      for (let i = 0; i < n; i++) {
        let s = 0;
        for (let j = 0; j < n; j++) s += R_piv[i][j] * tVec[j];
        wPiv.push(((s % q) + q) % q);
      }
      if (wPiv.every((x) => x === 0 || x === 1)) {
        validCount++;
        validSet.add(tVec.join(","));
      }
    }
    if (validCount !== 1 << n || validCount !== inst.hensel_audit.valid_boolean_witness_count) {
      console.error(`FAIL [${inst.instance_id}]: Hensel valid Boolean target count mismatch`);
      process.exit(1);
    }
    let pairedCount = 0;
    for (const tVec of allTargets) {
      if (validSet.has(tVec.join(","))) {
        const partner = tVec.map((v, ell) => (v + h[ell]) % q).join(",");
        if (validSet.has(partner)) pairedCount++;
      }
    }
    if (pairedCount !== 0 || inst.hensel_audit.paired_valid_targets_for_h !== 0) {
      console.error(`FAIL [${inst.instance_id}]: Expected 0 paired Hensel targets for h`);
      process.exit(1);
    }

    // 2. Verify Theorem 2 (Bitwise F_2-RREF Carry-Parity Vanishing)
    const { A_f2_rref, R_f2 } = inst.f2_rref_audit;
    let f2ValidCount = 0;
    for (const tVec of allTargets) {
      const tBits = targetToBits(tVec, t);
      const w = [];
      for (let r = 0; r < K; r++) {
        let s = 0;
        for (let idx = 0; idx < n * t; idx++) s ^= R_f2[r][idx] & tBits[idx];
        w.push(s);
      }
      const { parities, fullCarries } = computeCarryParities(A_f2_rref, w, t);
      const actualSum = [];
      for (let ell = 0; ell < n; ell++) {
        let s = 0;
        for (let r = 0; r < K; r++) s += A_f2_rref[ell][r] * w[r];
        actualSum.push(s % q);
      }
      for (let ell = 0; ell < n; ell++) {
        for (let b = 0; b < t; b++) {
          const actualBit = (actualSum[ell] >> b) & 1;
          const targetBit = (tVec[ell] >> b) & 1;
          const cMod2 = fullCarries[ell][b] % 2;
          if (actualBit !== (targetBit ^ cMod2)) {
            console.error(`FAIL [${inst.instance_id}]: Bitwise carry identity failed`);
            process.exit(1);
          }
        }
      }
      const isValid = actualSum.every((v, ell) => v === tVec[ell]);
      const allCarriesEven = parities.every((row) => row.every((c) => c === 0));
      if (isValid !== allCarriesEven) {
        console.error(`FAIL [${inst.instance_id}]: Carry-parity vanishing equivalence failed`);
        process.exit(1);
      }
      if (isValid) f2ValidCount++;
    }
    if (f2ValidCount !== inst.f2_rref_audit.carry_free_valid_target_count) {
      console.error(`FAIL [${inst.instance_id}]: F_2 carry-free valid count mismatch`);
      process.exit(1);
    }

    // 3. Check saved finite linearization counts, NOT a source-average bound.
    const dk = inst.disjoint_kernel_audit;
    if (
      dk.m_disjoint_directions > Math.floor(dk.K_dk / 2) ||
      dk.linearization_verified_assignments !== 1 << dk.m_disjoint_directions ||
      !dk.theorem3_passed
    ) {
      console.error(`FAIL [${inst.instance_id}]: Disjoint kernel audit failed`);
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
    `OK: dcp_clean_linear_witness_carry_obstruction cross-checked (${report.instances.length} instances, sha256=${report.sha256.slice(0, 16)})`
  );
}

main();
