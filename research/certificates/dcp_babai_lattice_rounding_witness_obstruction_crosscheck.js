#!/usr/bin/env node
/**
 * Independent Node.js cross-checker for dcp_babai_lattice_rounding_witness_obstruction.
 * Replays small coordinate-rounding controls, fundamental parallelepiped
 * Boolean vertex membership, half-integer l_infinity dichotomy, and forward-SWAP
 * counts and half-integer identities. Arithmetic uses JavaScript Number, NOT
 * arbitrary-precision rationals; this is not a general numerical certificate.
 */

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..", "..");
const ARTIFACT_PATH = path.join(
  ROOT,
  "research",
  "reductions",
  "dcp_babai_lattice_rounding_witness_obstruction.json"
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

// Invert integer matrix B_col with determinant +/- detVal using Gaussian elimination in floats/rationals
// Since det(B_col) = +/- 2^{nt} is a power of 2, 2 * B_col^{-1} * (z - 1/2) = (2^{nt} B_col^{-1}) * (2z - 1) / 2^{nt}
// is exact in dyadic integers!
function invertMatrixFloat(M) {
  const K = M.length;
  const aug = M.map((row, i) => {
    const ext = new Array(K).fill(0);
    ext[i] = 1;
    return row.slice().concat(ext);
  });
  for (let col = 0; col < K; col++) {
    let piv = col;
    for (let r = col + 1; r < K; r++) {
      if (Math.abs(aug[r][col]) > Math.abs(aug[piv][col])) piv = r;
    }
    const tmp = aug[col];
    aug[col] = aug[piv];
    aug[piv] = tmp;
    const div = aug[col][col];
    for (let j = 0; j < 2 * K; j++) aug[col][j] /= div;
    for (let r = 0; r < K; r++) {
      if (r !== col) {
        const factor = aug[r][col];
        for (let j = 0; j < 2 * K; j++) aug[r][j] -= factor * aug[col][j];
      }
    }
  }
  return aug.map((row) => row.slice(K));
}

function main() {
  const report = JSON.parse(fs.readFileSync(ARTIFACT_PATH, "utf-8"));
  if (!report.summary || !report.summary.all_theorems_passed) {
    console.error("FAIL: Summary does not report all_theorems_passed=true");
    process.exit(1);
  }

  for (const inst of report.instances) {
    const { n, t, q, K, A, piv_cols: pivCols, R_piv: rPiv, B_col: bCol } = inst;
    const detVal = Math.pow(q, n);
    if (inst.lattice_determinant !== detVal) {
      console.error(`FAIL [${inst.instance_id}]: Lattice determinant mismatch`);
      process.exit(1);
    }

    const bInvFloat = invertMatrixFloat(bCol);
    // Because det(B_col) = +/- 2^{nt}, adj(B_col) = detVal * B_col^{-1} is an exact integer matrix!
    const scaledInv = bInvFloat.map((row) => row.map((v) => Math.round(v * detVal)));

    function babaiRound(z0) {
      // u_i = sum_r B_col^{-1}[i, r] * (z0_r - 1/2) = (sum_r scaledInv[i, r] * (2*z0_r - 1)) / (2 * detVal)
      // k_i = floor(u_i + 1/2) = floor((sum_r scaledInv[i, r] * (2*z0_r - 1) + detVal) / (2 * detVal))
      const denom = 2 * detVal;
      const k = [];
      for (let i = 0; i < K; i++) {
        let num = detVal;
        for (let r = 0; r < K; r++) {
          num += scaledInv[i][r] * (2 * z0[r] - 1);
        }
        k.push(Math.floor(num / denom));
      }
      const zBabai = [];
      for (let r = 0; r < K; r++) {
        let s = z0[r];
        for (let i = 0; i < K; i++) s -= bCol[r][i] * k[i];
        zBabai.push(s);
      }
      return zBabai;
    }

    function inParallelepiped(x) {
      const denom = 2 * detVal;
      for (let i = 0; i < K; i++) {
        let num = 0;
        for (let r = 0; r < K; r++) {
          num += scaledInv[i][r] * (2 * x[r] - 1);
        }
        if (num < -detVal || num >= detVal) return false;
      }
      return true;
    }

    const allTargets = enumerateTargets(q, n);
    const validSet = new Set();
    let validCount = 0;
    let overflowCount = 0;
    let maxLinfNum = 1;

    for (const tVec of allTargets) {
      const z0 = new Array(K).fill(0);
      for (let i = 0; i < n; i++) {
        let s = 0;
        for (let ell = 0; ell < n; ell++) s += rPiv[i][ell] * tVec[ell];
        z0[pivCols[i]] = ((s % q) + q) % q;
      }
      const zBabai = babaiRound(z0);
      let linfNum = 1;
      for (let r = 0; r < K; r++) {
        const diffNum = Math.abs(2 * zBabai[r] - 1);
        if (diffNum > linfNum) linfNum = diffNum;
      }
      if (linfNum > maxLinfNum) maxLinfNum = linfNum;

      const isBool = zBabai.every((v) => v === 0 || v === 1);
      if ((isBool && linfNum !== 1) || (!isBool && linfNum < 3)) {
        console.error(`FAIL [${inst.instance_id}]: Half-integer dichotomy failed`);
        process.exit(1);
      }
      if (isBool) {
        validCount++;
        validSet.add(tVec.join(","));
      } else {
        overflowCount++;
      }
    }

    let polyVertexCount = 0;
    for (let mask = 0; mask < 1 << K; mask++) {
      const x = [];
      for (let r = 0; r < K; r++) x.push((mask >> r) & 1);
      if (inParallelepiped(x)) polyVertexCount++;
    }

    if (
      validCount !== polyVertexCount ||
      validCount !== inst.valid_boolean_witness_targets ||
      overflowCount !== inst.box_overflow_target_count ||
      `${maxLinfNum}/2` !== inst.max_residual_linf_exact
    ) {
      console.error(`FAIL [${inst.instance_id}]: Babai vertex/overflow counts mismatch`);
      process.exit(1);
    }

    const h = new Array(n).fill(0);
    h[0] = q >> 1;
    let pairedValid = 0;
    for (const tVec of allTargets) {
      if (validSet.has(tVec.join(","))) {
        const partner = tVec.map((v, ell) => (v + h[ell]) % q).join(",");
        if (validSet.has(partner)) pairedValid++;
      }
    }
    if (pairedValid !== inst.paired_valid_targets_for_h) {
      console.error(`FAIL [${inst.instance_id}]: Paired valid target count mismatch`);
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
    `OK: dcp_babai_lattice_rounding_witness_obstruction cross-checked (${report.instances.length} instances, sha256=${report.sha256.slice(0, 16)})`
  );
}

main();
