#!/usr/bin/env node
"use strict";

// Independent finite source replay and exact random-matrix union arithmetic.
// This checks certificates, not external proof review or a quantum lower bound.
const fs = require("fs");
const path = require("path");

function need(condition, message) {
  if (!condition) throw new Error(message);
}
function parity(x) {
  let p = 0;
  for (; x; x &= x - 1n) p ^= 1;
  return p;
}
function reduced(rows, width) {
  const a = rows.slice();
  const pivots = [];
  let used = 0;
  // Low pivots, unlike the Python implementation's high-pivot dictionary.
  for (let j = 0; j < width; j++) {
    const bit = 1n << BigInt(j);
    let k = used;
    while (k < a.length && !(a[k] & bit)) k++;
    if (k === a.length) continue;
    [a[k], a[used]] = [a[used], a[k]];
    for (let i = 0; i < a.length; i++) {
      if (i !== used && (a[i] & bit)) a[i] ^= a[used];
    }
    pivots.push(j);
    used++;
  }
  return {rows: a.slice(0, used), pivots};
}
function rank(rows, width) { return reduced(rows, width).rows.length; }
function kernel(rows, width) {
  const rr = reduced(rows, width);
  const result = [];
  for (let f = 0; f < width; f++) {
    if (rr.pivots.includes(f)) continue;
    let x = 1n << BigInt(f);
    rr.rows.forEach((row, i) => {
      if (row & (1n << BigInt(f))) x |= 1n << BigInt(rr.pivots[i]);
    });
    result.push(x);
  }
  return result;
}
function map(rows, x) {
  return rows.reduce((y, b, j) => y | (BigInt(parity(b & x)) << BigInt(j)), 0n);
}
function normalize(p, e) {
  need(Number.isSafeInteger(e), "noninteger dyadic exponent");
  if (e < 0) { p <<= BigInt(-e); e = 0; }
  if (p === 0n) return {p: 0n, e: 0};
  while (e && !(p & 1n)) { p >>= 1n; e--; }
  return {p, e};
}
function readProbability(record) {
  need(record && /^0x[0-9a-f]+$/.test(record.numerator_hex), "invalid numerator");
  need(Number.isSafeInteger(record.denominator_binary_exponent) &&
       record.denominator_binary_exponent >= 0, "invalid exponent");
  return normalize(BigInt(record.numerator_hex), record.denominator_binary_exponent);
}
function sameProbability(record, p, e, message) {
  const a = readProbability(record), b = normalize(p, e);
  need(a.p === b.p && a.e === b.e, message);
}
function add(a, b) {
  const e = Math.max(a.e, b.e);
  return normalize((a.p << BigInt(e - a.e)) + (b.p << BigInt(e - b.e)), e);
}
function capped(a) {
  return a.p >= (1n << BigInt(a.e)) ? {p: 1n, e: 0} : a;
}
function choose(n, k) {
  let p = 1n;
  for (let j = 1; j <= k; j++) p = p * BigInt(n - j + 1) / BigInt(j);
  return p;
}
function checkNative(row) {
  const n = row.dimension, m = 3 * n;
  const w = Math.floor(m / 32), r = Math.floor(w / 2);
  need(Number.isInteger(n) && n >= 32 && n <= 4096, "invalid source dimension");
  need(row.original_registers === m && row.minimum_kernel_support_and_complement === w &&
       row.uniform_cut_rank_lower_bound === r, "source cutoffs");
  const E = (n - r + 1) * (w - r + 1);
  need(row.rank_pair_exponent_minimum === E, "rank-pair exponent");
  const rankFail = normalize((1n << BigInt(n)) - 1n, m);
  let count = 0n;
  for (let j = 0; j < w; j++) count += choose(m, j);
  const supportFail = normalize(2n * count - 1n, n);
  const cutFail = capped(normalize(16n * BigInt(n + 1)**2n, E - m));
  const fail = capped(add(add(rankFail, supportFail), cutFail));
  const mean = normalize((1n << BigInt(fail.e)) + (fail.p << BigInt(r)) - fail.p, fail.e + r);
  sameProbability(row.full_rank_failure_upper_bound, rankFail.p, rankFail.e, "full-rank bound");
  sameProbability(row.small_or_near_full_kernel_support_failure_upper_bound,
                  supportFail.p, supportFail.e, "support bound");
  sameProbability(row.small_cut_rank_and_full_rank_failure_upper_bound,
                  cutFail.p, cutFail.e, "cut bound");
  sameProbability(row.bad_low_matrix_probability_upper_bound, fail.p, fail.e, "bad B bound");
  sameProbability(row.extra_descent_probability_given_good_B_upper_bound, 1n, r, "good B bound");
  sameProbability(row.native_source_mean_extra_descent_upper_bound, mean.p, mean.e, "source mean");
  need(row.source_bound_vacuous === (fail.p === 1n && fail.e === 0), "vacuity flag");
  need(row.uniform_over_every_precomplement_full_label_selector === true &&
       row.good_B_bound_uniform_over_initial_parity_syndrome === true &&
       row.native_mean_before_source_or_syndrome_postselection === true &&
       row.post_complement_direction_selection_covered === false &&
       row.quantum_query_lower_bound === false, "source scope");
}
function checkLaw(control) {
  const law = control.law;
  const A = law.public_labels_hex.map(row => row.map(BigInt));
  const n = A.length, m = A[0].length, t = law.phase_bits;
  need(n > 0 && m > 0 && m <= 10 && n <= 10 && t >= 3 && t <= 4096, "finite replay cap");
  const q = 1n << BigInt(t), Q = q / 2n;
  need(A.every(row => row.length === m && row.every(a => a >= 0n && a < q)), "labels out of range");
  const B = A.map(row => row.reduce((v, a, i) => v | ((a & 1n) << BigInt(i)), 0n));
  const u = BigInt(law.physical_direction_hex), x0 = BigInt(law.physical_origin_hex);
  const full = (1n << BigInt(m)) - 1n;
  need(u > 0n && u <= full && x0 >= 0n && x0 <= full && map(B, u) === 0n, "direction/origin");
  need(law.component_count === n && law.original_registers === m, "law dimensions");
  need(JSON.stringify(B.map(b => b.toString())) ===
       JSON.stringify(law.low_rows_hex.map(b => BigInt(b).toString())), "low B labels");
  const K = kernel(B, m), inputRank = rank(B, m);
  const storedK = law.kernel_basis_hex.map(BigInt);
  need(storedK.length === m - inputRank && rank(storedK, m) === m - inputRank &&
       storedK.every(v => v > 0n && v <= full && map(B, v) === 0n), "kernel certificate");
  const Trows = B.map(b => b & u), images = K.map(v => map(Trows, v));
  const r = rank(images, n);
  const cutRank = rank(B.map(b => b & u), m) + rank(B.map(b => b & (full ^ u)), m) - inputRank;
  need(cutRank === r && law.posterior_rank === r && law.matroid_connectivity_rank === r &&
       law.low_matrix_rank === inputRank && law.complement_outcome_bits === K.length - 1,
       "posterior/cut rank identity");
  const storedImage = law.kernel_image_basis_hex.map(BigInt);
  need(storedImage.every(v => v > 0n && v < (1n << BigInt(n))) && storedImage.length === r &&
       rank(storedImage, n) === r && rank(storedImage.concat(images), n) === r, "image basis");
  let offset = 0n;
  A.forEach((row, j) => {
    let sum = 0n;
    row.forEach((a, i) => { if (u & (1n << BigInt(i))) sum += a; });
    need(sum % 2n === 0n, "nonintegral output label");
    const bit = Number(sum / 2n & 1n) ^ parity(B[j] & u & x0);
    offset |= BigInt(bit) << BigInt(j);
  });
  need(BigInt(law.affine_low_output_offset_hex) === offset, "affine offset");
  const dual = law.dual_constraints.map(c => BigInt(c.mask_hex));
  need(dual.length === n - r && rank(dual, n) === n - r &&
       dual.every(v => v > 0n && v < (1n << BigInt(n)) && images.every(y => !parity(v & y))),
       "dual annihilator");
  law.dual_constraints.forEach(c => need(c.target === parity(BigInt(c.mask_hex) & offset), "dual target"));
  const hist = new Map(), pairs = [];
  const syndrome = map(B, x0);
  for (let x = 0n; x <= full; x++) {
    const y = x ^ u;
    if (x > y || map(B, x) !== syndrome) continue;
    const labels = A.map(row => {
      let difference = 0n;
      row.forEach((a, i) => {
        difference += a * (((y >> BigInt(i)) & 1n) - ((x >> BigInt(i)) & 1n));
      });
      need(difference % 2n === 0n, "original phase parity");
      return ((difference / 2n) % Q + Q) % Q;
    });
    const low = labels.reduce((v, a, j) => v | ((a & 1n) << BigInt(j)), 0n);
    need(rank(images.concat([low ^ offset]), n) === r, "affine support");
    hist.set(low.toString(), (hist.get(low.toString()) || 0) + 1);
    pairs.push({x_hex: `0x${x.toString(16)}`, x_xor_u_hex: `0x${y.toString(16)}`,
                output_label_hex: labels.map(a => `0x${a.toString(16)}`)});
  }
  need(pairs.length === 2**(K.length - 1) && hist.size === 2**r &&
       [...hist.values()].every(v => v === pairs.length / hist.size), "nonuniform complement image");
  const census = control.direct_census;
  need(JSON.stringify(pairs) === JSON.stringify(census.physical_complement_pairs), "original physical pair labels");
  const expectedHist = [...hist].map(([k, v]) => [BigInt(k), v]).sort((a,b) => a[0] < b[0] ? -1 : 1);
  need(JSON.stringify(expectedHist.map(([k,v]) => [`0x${k.toString(16)}`, v])) ===
       JSON.stringify(Object.entries(census.low_output_histogram)), "output histogram");
  const possible = hist.has("0");
  need(law.all_even_output_attainable === possible, "affine target consistency");
  sameProbability(law.extra_descent_probability, possible ? 1n : 0n, r, "posterior probability");
  sameProbability(census.extra_descent_probability, possible ? 1n : 0n, r, "census probability");
  need(law.selection_model === "all-public-labels-before-complement-Z" &&
       law.noise_model === "pure-flat-native-phase-packet" &&
       law.uniform_pushforward_from_quotient_D_mod_u === true &&
       law.success_means_shift_recovery === false && law.mixed_noise_law_supplied === false,
       "posterior instrument scope");
}
function checkMinima(records) {
  let count = 0;
  for (let n = 2; n < 10; n++) for (let w = 1; w <= Math.floor(n / 2); w++) {
    for (let r = 1; r <= w; r++) {
      let best = Infinity;
      for (let s = w; s <= 3*n-w; s++) for (let a = 0; a <= Math.min(n,s); a++) {
        for (let b = 0; b <= Math.min(n,3*n-s); b++) if (a+b >= n && a+b < n+r) {
          best = Math.min(best, (n-a)*(s-a)+(n-b)*(3*n-s-b));
        }
      }
      const row = records[count++];
      need(row && row.n === n && row.w === w && row.r === r &&
           row.exhaustive_integer_minimum === best && best === (n-r+1)*(w-r+1), "rank-pair minimum");
    }
  }
  need(count === records.length, "extra minimization records");
}
function checkExhaustive(record) {
  need(JSON.stringify(record.all_binary_matrices_shapes) === "[[1,3],[2,4]]", "rank identity scope");
  let count = 0;
  for (const [n,m] of [[1,3],[2,4]]) {
    const full = (1 << m) - 1;
    for (let matrix = 0; matrix < 2**(n*m); matrix++) {
      const rows = Array.from({length:n}, (_,i) => BigInt((matrix >> (m*i)) & full));
      const K = kernel(rows,m), baseRank = rank(rows,m);
      for (let mask = 1; mask <= full; mask++) {
        const u = BigInt(mask);
        if (map(rows,u) !== 0n) continue;
        const imageRank = rank(K.map(x => map(rows.map(b=>b&u),x)), n);
        const cutRank = rank(rows.map(b=>b&u),m)+rank(rows.map(b=>b&(BigInt(full)^u)),m)-baseRank;
        need(imageRank === cutRank, "exhaustive rank identity");
        count++;
      }
    }
  }
  need(record.nonzero_kernel_directions_checked === count, "rank identity count");
}
function verify(report) {
  need(report.contract_id === "precomplement_full_label_single_direction_rank_gate_v1" &&
       report.accepted_speedup_candidate === false && report.novelty_claim === false &&
       report.efficient_quantum_receiver_supplied === false &&
       report.source_quantum_preparations_executed === 0, "claim admission");
  const scope = report.scope;
  need(scope.noisy_mixed_packets_covered === false && scope.post_complement_selection_covered === false &&
       scope.multi_output_collective_measurements_covered === false && scope.general_DCP_lower_bound === false &&
       scope.all_even_event_implies_secret_recovery === false && scope.postselected_source_resupply_is_free === false &&
       scope.n_is_secret_vector_component_count_not_log_cyclic_modulus === true &&
       scope.native_mean_bound_before_source_or_syndrome_postselection === true, "scope expansion");
  need(JSON.stringify(report.native_source_bounds.map(b=>b.dimension)) === "[32,64,128,256,512,1024]", "scaling coverage");
  report.native_source_bounds.forEach(checkNative);
  need(report.physical_controls.length === 28, "physical control coverage");
  report.physical_controls.forEach(checkLaw);
  checkMinima(report.rank_pair_minimization_controls);
  checkExhaustive(report.exhaustive_connectivity_controls);
  need(report.provisional_negative_result.status === "LOCAL_DERIVATION_NOT_CENTRALLY_PROMOTED" &&
       report.provisional_negative_result.general_DCP_lower_bound === false, "negative promotion");
  return {status:"ok", physical_controls:report.physical_controls.length,
          source_dimensions:report.native_source_bounds.length,
          rank_minima:report.rank_pair_minimization_controls.length,
          general_DCP_lower_bound:false};
}
module.exports = {verify, parity, map, readProbability, sameProbability, normalize, add, capped};
if (require.main === module) {
  const file = process.argv[2] || path.resolve(__dirname,"../phase_workbench/dcp_adaptive_direction_rank_gate.json");
  console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(file,"utf8")))));
}
