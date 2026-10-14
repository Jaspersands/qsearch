"use strict";
// Exact bounded native arithmetic and complete finite source/instrument replay.
// A passing fixture is not certification of IID preparation, noise or speedup.
const fs = require("fs"), path = require("path"), crypto = require("crypto");
const {check, same, rat, str} = require("./cyclotomic_exact.js");
const ROOT = path.resolve(__dirname, "../..");
const REPORT = path.join(ROOT, "research/reductions/native_uniform_descent_receiver.json");
const hash = f => crypto.createHash("sha256").update(fs.readFileSync(f)).digest("hex");
const mod = (a, q) => (a % q + q) % q;
const roots = [[1, 0], [0, 1], [-1, -1]], lambdas = [[0, 0], [1, 0], [1, 1]];
function chart(L) {
  check(Number.isInteger(L) && L >= 1 && L <= 4, "bounded replay level, not scalable enumeration");
  const q = 3**Math.floor(L/2);
  return L % 2 ? [3*q, 2*q, q] : [q, 0, q];
}
function reduce(v, L) {
  check(Array.isArray(v) && v.length === 2 && v.every(Number.isSafeInteger), "exact bounded ring coefficients");
  const [h, c, k] = chart(L), carry = Math.floor(v[1]/k);
  return [mod(v[0]-carry*c, h), mod(v[1], k)];
}
const add = (a, b, L) => reduce([a[0]+b[0], a[1]+b[1]], L);
const mul = (a, b, L) => reduce([a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0]-a[1]*b[1]], L);
const residue = a => mod(a[0]+a[1], 3);
const qroot = L => 3**Math.ceil(L/2);
function quotient(a, L) {
  check(L >= 2 && residue(a) === 0, "actual divisibility by pi required");
  const x = -2*a[0]+a[1], y = -a[0]-a[1];
  check(x % 3 === 0 && y % 3 === 0, "integral pi quotient");
  return reduce([x/3, y/3], L-1);
}
function exponent(a, s, L) {
  const v = mul(a, s, L), q = qroot(L);
  let x = 2, y = -1;
  for (let j = 1; j < L; j++) [x, y] = [-2*x-y, x-y];
  const numerator = q*(x*v[0]+y*v[1]), d = 3**L;
  check(numerator % d === 0, "exact character exponent, no rounded rational");
  return mod(numerator/d, q);
}
function phases(label, secret, L, Q) {
  return lambdas.map(l => mod(label.reduce((z, a, i) => z+exponent(a, mul(secret[i], l, L), L), 0), qroot(L))*Q/qroot(L));
}
function centre(L) {
  let x = reduce([1, 0], L);
  for (let j = 1; j < L; j++) x = mul(x, [-1, 1], L);
  return x;
}
function amplitudes(saved, exact, Q, message) {
  check(saved.length === 3 && saved.every(a => a.length === 2 && a.every(Number.isFinite)), message);
  saved.forEach((a, j) => {
    const theta = 2*Math.PI*exact[j]/Q;
    check(Math.abs(a[0]-Math.cos(theta)/Math.sqrt(3)) < 3e-12 &&
          Math.abs(a[1]-Math.sin(theta)/Math.sqrt(3)) < 3e-12, message);
  });
}
function rank3(rows, n) {
  const A = rows.map(a => a.slice());
  let rank = 0;
  for (let j = 0; j < n; j++) {
    const p = A.findIndex((a, i) => i >= rank && a[j] !== 0);
    if (p < 0) continue;
    [A[rank], A[p]] = [A[p], A[rank]];
    const scale = A[rank][j] === 1 ? 1 : 2;
    A[rank] = A[rank].map(v => mod(v*scale, 3));
    for (let i = 0; i < A.length; i++) if (i !== rank) {
      const c = A[i][j];
      A[i] = A[i].map((v, k) => mod(v-c*A[rank][k], 3));
    }
    rank++;
  }
  return rank;
}
function contract(c) {
  const n = c.dimension, L = c.level, K = c.fresh_digit_samples_per_level, W = (n+1)**2;
  check(Number.isInteger(n) && n >= 1 && Number.isInteger(L) && L >= 1 && K === n+8 && c.coarse_window === W, "committed resource parameters");
  let power = 1n, cap = 0n;
  for (let j = 0; j < L; j++) {cap += BigInt(K)*power; power *= BigInt(W);}
  check(c.original_copy_upper === String(cap), "literal copy recurrence upper bound");
  const num = BigInt(L)*(3n**BigInt(n)-1n), den = 2n*3n**BigInt(K);
  check(c.ideal_IID_rank_failure_upper === str(num >= den ? rat(1n) : rat(num, den)), "exact projective-line union bound");
  check(c.unknown_quantum_buffer_upper === (L-1)*W+L && c.every_fixed_level_is_polynomial === true &&
        c.universal_copy_lower_bound === false && c.hardware_or_noise_error_included === false &&
        c.source_law_requires_coarse_only_selection === true, "scope of fixed-level cost and source assumptions");
}
const ring = L => {
  const [a, , b] = chart(L), out = [];
  for (let i = 0; i < a; i++) for (let j = 0; j < b; j++) out.push([i, j]);
  return out;
};
const idsKey = (L, ids) => L+":"+JSON.stringify(ids);
const sorted = ids => ids.slice().sort((a, b) => a-b);
function run(r) {
  check(r.status === "NATIVE_SOURCE_PRESERVING_DESCENT_AND_REFERENCE_RECOVERY_REVIEW_PENDING", "review-pending source-specific status");
  check(r.derivation_sha256 === hash(path.join(ROOT, "research/NATIVE_UNIFORM_DESCENT_RECEIVER.md")), "pinned derivation");
  const files = ["native_uniform_descent_receiver.py", "nil3_state_hsp_descent_receiver.py", "native_state_hsp_bridge.py",
                 "cyclotomic_rescaling_gate.py", "ternary_cyclic_extractor.py", "vector_centre_state_hsp_receiver.py"];
  same(Object.keys(r.source_sha256).sort(), files.slice().sort(), "all source contract hashes present");
  files.forEach(f => check(r.source_sha256[f] === hash(path.join(ROOT, "theorems", f)), "pinned source dependency "+f));
  ["full_source_and_noise_promises_proved_from_data", "quantum_hardware_executed", "novelty_verified",
   "polynomial_growing_depth_receiver_supplied", "accepted_speedup_candidate"].forEach(k => check(r[k] === false, "unjustified promotion "+k));
  check(r.conditional_uniform_label_censuses.length === 6, "complete six conditional censuses");
  let censusIndex = 0;
  for (const L of [2, 3]) for (let v = 0; v < 3; v++) {
    const c = r.conditional_uniform_label_censuses[censusIndex++], counts = new Map(ring(L-1).map(a => [JSON.stringify(a), 0]));
    check(c.parent_level === L && c.complement_outcome === v, "conditioned census parameters");
    same(c.conditioned_residues, [1, 2], "coarse residues only");
    for (const a of ring(L).filter(a => residue(a) === 1)) for (const b of ring(L).filter(a => residue(a) === 2)) {
      const key = JSON.stringify(quotient(add(a, mul(b, roots[v], L), L), L));
      counts.set(key, counts.get(key)+1);
    }
    check(c.child_label_counts.length === counts.size, "no missing child label");
    same(c.child_label_counts, [...counts].map(([label, count]) => ({label: JSON.parse(label), count})), "exact uniform coset convolution");
    check(new Set(counts.values()).size === 1, "conditional uniformity, not rejection filtering");
  }
  let merges = 0, originalInputs = 0, digitMeasurements = 0;
  const dimensions = [[1, 2], [1, 3], [2, 3], [4, 3], [1, 4]];
  check(r.source_driven_receiver_controls.length === dimensions.length, "all committed source recoveries");
  r.source_driven_receiver_controls.forEach((c, index) => {
    const [n, L] = dimensions[index], out = c.result, Q = qroot(L), truth = c.truth_fixture_only;
    check(c.dimension === n && c.level === L && truth.length === n, "fixture dimension and level");
    truth.forEach(a => same(a, reduce(a, L), "canonical fixture secret"));
    check(out.status === "IDEAL_NATIVE_REFERENCE_SECRET_DECODED" && out.source_exhaustion === null, "actual completed finite reference execution");
    contract(out.resource_contract);
    check(out.resource_contract.dimension === n && out.resource_contract.level === L && BigInt(out.original_inputs_supplied) <= BigInt(out.resource_contract.original_copy_upper), "paid original-copy budget");
    ["receiver_takes_hidden_secret", "quantum_hardware_executed", "general_StateHSP_receiver_supplied", "new_quantum_speedup_established"].forEach(k => check(out[k] === false, "source-specific ideal reference only"));
    const available = new Map(), spent = new Set();
    check(out.complete_original_input_records.length === out.original_inputs_supplied, "complete supplied source trace");
    out.complete_original_input_records.forEach((s, i) => {
      check(s.original_index === i && s.public_label.length === n, "unique supplied originals");
      s.public_label.forEach(a => same(a, reduce(a, L), "canonical supplied labels"));
      const e = phases(s.public_label, truth, L, Q);
      amplitudes(s.supplied_amplitudes, e, Q, "actual original source amplitudes");
      available.set(idsKey(L, [i]), {label: s.public_label, e, ids: [i], level: L});
    });
    check(out.descent_streams.length === L-1, "one measured level drop per descent");
    out.descent_streams.forEach((stream, depth) => {
      const parent = L-depth, child = parent-1, records = stream.complete_output_records;
      check(stream.parent_level === parent && stream.child_level === child && records.length === stream.outputs_emitted, "complete per-level merge trace");
      check(stream.selection_uses_only_coarse_residues === true && stream.higher_label_or_secret_filtering_used === false && stream.child_state_prepared_from_secret === false, "coarse-only source-preserving contract");
      same(stream.first_output_records, records.slice(0, 8), "bounded preview does not replace full replay");
      let gates = 0, included = 0;
      for (const b of records) {
        const B = b.public_input_labels.length, offsets = [0, ...b.measured_complement];
        check(B >= 1 && offsets.length === B && offsets.every(v => Number.isInteger(v) && v >= 0 && v < 3), "all measured complement outcomes, no missing pivot");
        check(b.parent_level === parent && b.child_level === child && b.input_original_lineages.length === B, "merge levels and paid physical inputs");
        const packets = b.input_original_lineages.map((ids, j) => {
          const key = idsKey(parent, ids), packet = available.get(key);
          check(packet && !spent.has(key), "unknown or reused physical input");
          same(packet.label, b.public_input_labels[j], "labels belong to actual supplied registers");
          spent.add(key);
          return packet;
        });
        const lineage = sorted(packets.flatMap(p => p.ids));
        check(new Set(lineage).size === lineage.length, "no reused unknown ancestor");
        same(b.original_source_indices, lineage, "exact original physical lineage");
        for (let j = 0; j < n; j++) check(mod(packets.reduce((z, p) => z+residue(p.label[j]), 0), 3) === 0, "nonempty residue-zero support");
        const A = Array.from({length: n}, (_, j) => packets.reduce((a, p, k) => add(a, mul(p.label[j], roots[offsets[k]], parent), parent), [0, 0]));
        same(b.combined_label_before_division, A, "public rotated label sum");
        const label = A.map(a => quotient(a, parent));
        same(b.child_label, label, "actual ideal division, not convenient child generation");
        const e = [0, 1, 2].map(t => mod(packets.reduce((z, p, k) => z+p.e[(t+offsets[k]) % 3], 0), Q));
        amplitudes(b.retained_amplitudes, e, Q, "literal retained full global phase");
        const expected = phases(label, truth.map(s => reduce(s, child)), child, Q);
        same(e.map(x => mod(x-e[0], Q)), expected, "exact lower-level native family identity");
        same(b.ideal_branch_probability, {base: 3, exponent: 1-B}, "exact uniform complement probability");
        check(Math.abs(b.branch_probability_diagnostic-3**(1-B)) < 3e-12, "branch probability diagnostic");
        const recipe = b.quantum_recipe;
        check(recipe.gates.length === B-1 && recipe.accepted_outcomes === "ALL" && recipe.unknown_inverse_cloning_or_postselection_required === false, "literal known gate recipe only");
        recipe.gates.forEach((g, j) => same(g, {gate: "SUM_inverse_F3", control: 0, target: j+1}, "SUM-inverse instrument"));
        check(b.secret_used_by_merge === false && b.coherent_pointer_transfer_claimed === false, "measured source-specific merge scope");
        const key = idsKey(child, lineage);
        check(!available.has(key), "duplicate child packet");
        available.set(key, {label, e, ids: lineage, level: child});
        included += B; gates += B-1; merges++;
      }
      const coverage = stream.coverage;
      check(stream.known_SUM_gates === gates && stream.complement_measurements === gates && coverage.included_original_inputs === included && coverage.block_count === records.length, "paid SUM/measurement/support ledger");
      check(coverage.zero_sum_window === (n+1)**2 && coverage.maximum_live_conditional_registers <= coverage.zero_sum_window && coverage.original_inputs === included+coverage.leftover_original_indices.length, "bounded retained buffer and all local inputs accounted");
    });
    let learned = null, finalIds = [];
    check(out.completed_digit_stages.length === L, "all prefix stages derived from measurements");
    out.completed_digit_stages.forEach((stage, depth) => {
      const level = depth+1, K = n+8, rows = stage.public_rows, digits = stage.recovered_top_digits;
      check(stage.level === level && stage.unknown_secret_used_by_stage === false && rows.length === K && stage.measured_outcomes.length === K && stage.digit_measurement_original_lineages.length === K && stage.public_input_labels.length === K, "complete paid final digit stage");
      same(stage.learned_lower, learned, "lower prefix came from prior source measurements");
      check(digits.length === n && digits.every(u => Number.isInteger(u) && u >= 0 && u < 3), "canonical top digits");
      stage.digit_measurement_original_lineages.forEach((ids, j) => {
        const key = idsKey(level, ids), packet = available.get(key);
        check(packet && !spent.has(key), "digit measurement uses an unmeasured physical packet");
        spent.add(key); finalIds.push(...ids);
        same(stage.public_input_labels[j], packet.label, "actual label for final measurement");
        const row = packet.label.map(a => {
          const e = exponent(a, centre(level), level), q = qroot(level);
          check((3*e) % q === 0, "central character has order3");
          return mod(3*e/q, 3);
        });
        same(rows[j], row, "exact measured row from native carries");
        const lower = learned || Array.from({length: n}, () => [0, 0]), correction = phases(packet.label, lower, level, Q);
        const residual = packet.e.map((v, k) => mod(v-correction[k]-packet.e[0], Q));
        const outcome = mod(row.reduce((z, a, k) => z+a*digits[k], 0), 3);
        same(residual, [0, Q*outcome/3, mod(2*Q*outcome/3, Q)], "actual corrected state is measured character");
        check(stage.measured_outcomes[j] === outcome, "measured outcome agrees with source, not assigned secret");
        digitMeasurements++;
      });
      check(rank3(rows, n) === n, "full rank, not assumed recovery");
      const lower = learned || Array.from({length: n}, () => [0, 0]);
      learned = lower.map((a, i) => add(a, mul(centre(level), [digits[i], 0], level), level));
    });
    same(learned, out.recovered_native_secret, "actual carry-aware reconstructed secret");
    same(learned, truth, "source fixture result only");
    same(sorted(finalIds), out.measured_original_lineages, "complete measured original lineages");
    const remaining = [...available].filter(([key]) => !spent.has(key)).flatMap(([, p]) => p.ids);
    same(sorted(remaining), out.unconsumed_original_lineages, "all unmeasured registers retained");
    same(sorted([...finalIds, ...remaining]), Array.from({length: out.original_inputs_supplied}, (_, i) => i), "no lost, copied or regenerated original inputs");
    originalInputs += out.original_inputs_supplied;
  });
  check(r.scaling_contracts.length === 12, "complete fixed and growing-depth ledger");
  r.scaling_contracts.forEach((c, i) => {
    const n = [8, 32, 128][Math.floor(i/4)], L = [2, 3, 4, n][i % 4];
    check(c.dimension === n && c.level === L, "committed scaling dimensions");
    contract(c);
  });
  return {status: "PASS", source_driven_recoveries: 5, complete_merge_replays: merges,
          original_inputs_replayed: originalInputs, exact_digit_measurements: digitMeasurements,
          uniform_label_censuses: 6, new_quantum_speedup_established: false};
}
if (require.main === module) console.log(JSON.stringify(run(JSON.parse(fs.readFileSync(process.argv[2] || REPORT, "utf8"))), null, 2));
module.exports = {run, contract};
