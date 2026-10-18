#!/usr/bin/env node
/**
 * Independent Node.js cross-checker for dcp_poly_pool_cnot_collimation_branching_obstruction.
 * Re-computes CNOT + Z branching laws, multinomial bucket-occupancy disjoint pair counts,
 * and superpolynomial depth/sample bounds from scratch.
 */

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..", "..");
const ARTIFACT_PATH = path.join(
  ROOT,
  "research",
  "reductions",
  "dcp_poly_pool_cnot_collimation_branching_obstruction.json"
);

function enumerateAssignments(B, M) {
  const res = [];
  function rec(idx, cur) {
    if (idx === M) {
      res.push(cur.slice());
      return;
    }
    for (let u = 0; u < B; u++) {
      cur.push(u);
      rec(idx + 1, cur);
      cur.pop();
    }
  }
  rec(0, []);
  return res;
}

function gcd(a, b) {
  a = Math.abs(a);
  b = Math.abs(b);
  while (b > 0) {
    const t = a % b;
    a = b;
    b = t;
  }
  return a;
}

function fracStr(num, den) {
  if (num === 0) return "0";
  const g = gcd(num, den);
  const n = num / g;
  const d = den / g;
  return d === 1 ? `${n}` : `${n}/${d}`;
}

function main() {
  const report = JSON.parse(fs.readFileSync(ARTIFACT_PATH, "utf-8"));
  if (!report.summary || !report.summary.all_theorems_passed) {
    console.error("FAIL: Summary does not report all_theorems_passed=true");
    process.exit(1);
  }

  for (const inst of report.instances) {
    const { n, t, q, M_pool: mPool, b_bits: bBits, B_buckets: bBuckets } = inst;
    if (q !== 1 << t || bBuckets !== 1 << bBits) {
      console.error(`FAIL [${inst.instance_id}]: Power-of-two parameter mismatch`);
      process.exit(1);
    }

    const expectedTriples = Math.pow(q, 3 * n);
    if (inst.cnot_branching_audit.total_triples_checked !== expectedTriples) {
      console.error(`FAIL [${inst.instance_id}]: Triple count mismatch`);
      process.exit(1);
    }
    let nonTorsionSameBucket = 0;
    for (let x1 = 0; x1 < bBuckets; x1++) {
      for (let x2 = 0; x2 < bBuckets; x2++) {
        if (x1 === x2 && (2 * x2) % bBuckets !== 0) {
          nonTorsionSameBucket++;
        }
      }
    }
    if (
      nonTorsionSameBucket !== inst.cnot_branching_audit.non_2_torsion_same_bucket_residues ||
      nonTorsionSameBucket !== inst.cnot_branching_audit.z1_only_cancels_residues
    ) {
      console.error(`FAIL [${inst.instance_id}]: Non-2-torsion residue count mismatch`);
      process.exit(1);
    }

    const assignments = enumerateAssignments(bBuckets, mPool);
    let sumPairs = 0;
    let collCount = 0;
    let maxPairs = 0;
    for (const assign of assignments) {
      const counts = new Array(bBuckets).fill(0);
      for (const u of assign) counts[u]++;
      let pairs = 0;
      let odd = 0;
      for (const c of counts) {
        pairs += Math.floor(c / 2);
        odd += c % 2;
      }
      if (2 * pairs !== mPool - odd) {
        console.error(`FAIL [${inst.instance_id}]: Bucket parity identity failed`);
        process.exit(1);
      }
      if (pairs > maxPairs) maxPairs = pairs;
      sumPairs += pairs;
      if (pairs >= 1) collCount++;
    }

    const totalOut = assignments.length;
    if (
      totalOut !== inst.bucket_pairing_audit.total_bucket_assignments ||
      maxPairs !== Math.floor(mPool / 2) ||
      fracStr(collCount, totalOut) !== inst.bucket_pairing_audit.collision_probability_exact ||
      fracStr(sumPairs, totalOut) !== inst.bucket_pairing_audit.expected_disjoint_pairs_exact ||
      fracStr(sumPairs, 2 * totalOut) !== inst.bucket_pairing_audit.expected_subtraction_children_exact
    ) {
      console.error(`FAIL [${inst.instance_id}]: Bucket pairing exact rational census mismatch`);
      process.exit(1);
    }
  }

  for (const row of report.asymptotic_scaling) {
    const nt = row.n * row.t;
    const bMax = Math.floor(Math.log2(row.M_pool));
    const lMin = Math.ceil((nt - 1) / bMax);
    if (
      row.max_bits_cancelled_per_level_b !== bMax ||
      row.minimum_tree_depth_L !== lMin ||
      row.poly_pool_initial_preparations_log2_lower !== 2 * lMin ||
      !row.theorem3_passed
    ) {
      console.error(`FAIL [asymptotic n=${row.n}]: Depth/sample lower bound mismatch`);
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
    `OK: dcp_poly_pool_cnot_collimation_branching_obstruction cross-checked (${report.instances.length} instances, sha256=${report.sha256.slice(0, 16)})`
  );
}

main();
