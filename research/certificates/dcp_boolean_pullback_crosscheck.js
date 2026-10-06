// Exact physical branch phases and source counts, not independent theorem review.
const fs = require('fs');
const path = require('path');
const assert = require('assert/strict');
const crypto = require('crypto');
const root = path.resolve(__dirname, '../..');
const report = JSON.parse(fs.readFileSync(path.join(root, 'research/phase_workbench/dcp_boolean_phase_pullback.json'), 'utf8'));
const mod = (a, q) => (a % q + q) % q;
const evaluate = (terms, z) => terms.reduce((value, mask) => value ^ Number((BigInt(z) & BigInt(mask)) === BigInt(mask)), 0);
let instrumentChecks = 0;
for (const row of report.physical_instruments) {
  let count = 0;
  for (let theta = 0; theta < row.modulus; theta++) for (let b = 0; b < 2; b++)
    for (let fx = 0; fx < 2; fx++) for (let fy = 0; fy < 2; fy++) {
      assert.equal(mod(theta * ((b ^ fx) - (b ^ fy)), row.modulus), mod((b ? -1 : 1) * theta * (fx - fy), row.modulus));
      count++;
    }
  assert.equal(count, row.exact_density_phase_identities);
  assert.equal(row.every_branch_kraus_norm_squared.sign, 1);
  assert.equal(BigInt(row.every_branch_kraus_norm_squared.numerator_hex), 1n);
  assert.equal(BigInt(row.every_branch_kraus_norm_squared.denominator_hex), 2n);
  instrumentChecks += count;
}
const control = report.complete_nonlinear_packet_pullback;
let branchChecks = 0;
const counts = new Map();
for (let code = 0; code < 64; code++) {
  const a = [1 + 2 * (code % 4), 2 * (Math.floor(code / 4) % 4), 1 + 2 * (Math.floor(code / 16) % 4)];
  for (let b = 0; b < 8; b++) {
    const updated = a.map((x, i) => mod((b >> i & 1) ? -x : x, 8));
    const key = updated.join(','); counts.set(key, (counts.get(key) || 0) + 1);
    for (let secret = 0; secret < 8; secret++) for (let z = 0; z < 4; z++) {
      const f = control.compiled_functions_hex.map(terms => evaluate(terms, z));
      const h = control.map_anf_hex.map(terms => evaluate(terms, z));
      assert.deepEqual(f, [h[1], h[0], h[1]]);
      const branch = a.reduce((sum, x, i) => sum + x * ((b >> i & 1) ^ f[i]), 0);
      const global = a.reduce((sum, x, i) => sum + x * (b >> i & 1), 0);
      const pullback = updated.reduce((sum, x, i) => sum + x * f[i], 0);
      assert.equal(mod(secret * (branch - global - pullback), 8), 0);
      assert.equal(pullback % 2, 0);
      branchChecks++;
    }
  }
}
assert.equal(branchChecks, control.exact_branch_and_packet_pullback_checks);
assert.equal(counts.size, control.all_updated_higher_label_tables);
for (const value of counts.values()) assert.equal(value, control.updated_table_multiplicity_from_all_branches);
const image = Array.from({length: 4}, (_, z) => control.map_anf_hex.map(terms => evaluate(terms, z)).join(','));
assert(new Set(image).size < 4);
assert.equal(control.public_map_inverse_required, false);
const plan = control.resource_plan, terms = plan.public_boolean_anf_functions_hex.flat();
const wt = x => { let count = 0; while (x) { x &= x - 1n; count++; } return count; };
const toffoli = terms.reduce((sum, x) => sum + 4 * Math.max(0, wt(BigInt(x)) - 1), 0);
assert.equal(toffoli, plan.public_evaluator_resources.compute_uncompute_toffoli_upper_bound);
assert.equal(2 * terms.filter(x => BigInt(x) !== 0n).length, plan.public_evaluator_resources.compute_uncompute_cnot_upper_bound);
assert.equal(plan.program_phase_states_consumed, plan.public_boolean_anf_functions_hex.length);
assert.equal(plan.same_program_or_phase_function_reusable, false);
const source = report.selector_source_controls;
const unconditional = Array(8).fill(0), safe = Array(8).fill(0), unsafe = Array(8).fill(0);
for (let a = 0; a < 8; a++) for (let b = 0; b < 2; b++) {
  const updated = mod(b ? -a : a, 8), before = Math.min(a, mod(-a, 8));
  assert.equal(before, Math.min(updated, mod(-updated, 8)));
  unconditional[updated]++;
  if (before === 3) safe[updated]++;
  if (a < 4) unsafe[updated]++;
}
assert.deepEqual(unconditional, source.unconditional_updated_label_counts);
assert.deepEqual(safe, source.safe_sign_orbit_selected_3_counts);
assert.deepEqual(unsafe, source.unsafe_original_label_less_than_4_counts);
assert.equal(report.sign_orbit_selector_source.conditional_higher_labels_are_iid_uniform, false);
report.source_gates.forEach((row, i) => {
  assert.equal(row.native_updated_source_certified_as_declared, i === 0);
  assert.equal(row.repeated_same_function_queries_available, false);
});
let literalFunctions = 0;
for (let mask = 0; mask < 16; mask++) {
  const terms = Array.from({length: 4}, (_, i) => i).filter(i => mask >> i & 1).map(x => '0x' + x.toString(16));
  const f = Array.from({length: 4}, (_, z) => evaluate(terms, z));
  const derivative = f[3] - f[1] - f[2] + f[0];
  const variables = terms.map(BigInt).filter(x => x !== 0n);
  const literal = variables.length <= 1 && variables.every(x => (x & (x - 1n)) === 0n);
  assert.equal(literal, mod(derivative, 4) === 0);
  literalFunctions += Number(literal);
}
assert.equal(literalFunctions, 6);
assert.equal(report.nonlinear_product_falsifier.source_universal_phase_product, false);
assert.deepEqual(report.nonlinear_product_falsifier.nonliteral_physical_coordinate_functions, [1]);
assert.equal(report.nonlinear_product_falsifier.high_label_adaptive_or_sign_orbit_selected_functions_covered, false);
let originChecks = 0;
for (const q of [8, 16, 128]) for (let syndrome = 0; syndrome < 4; syndrome++) for (let z = 0; z < 4; z++) {
  const rows = [3, 1, 1, 2], origin = [syndrome & 1, syndrome >> 1, 0, 0];
  const parity = x => (x & 1) ^ (x >> 1 & 1);
  for (const component of [[1, 2, 3, 1], [2, 1, 3, 0]]) {
    const original = component.reduce((s, a, i) => s + a * ((origin[i] ^ parity(rows[i] & z)) - origin[i]), 0);
    const normalized = component.reduce((s, a, i) => s + (origin[i] ? -a : a) * parity(rows[i] & z), 0);
    assert.equal(mod(original, q), mod(normalized, q));
  }
  originChecks++;
}
for (const [file, expected] of Object.entries(report.dependency_sha256))
  assert.equal(crypto.createHash('sha256').update(fs.readFileSync(path.join(root, file))).digest('hex'), expected);
assert.equal(report.claim_gate.speedup_claim_allowed, false);
assert.equal(report.claim_gate.novelty_claim, false);
console.log(JSON.stringify({status: 'BOUNDED_PHYSICAL_AND_SOURCE_CROSSCHECK_ONLY',
  physical_kraus_density_identities: instrumentChecks, nonlinear_packet_branch_checks: branchChecks,
  complete_updated_higher_source_tables: counts.size, sign_orbit_selector_source_pairs: 16,
  boolean_product_criterion_functions_checked: 16, product_functions_admitted: literalFunctions,
  affine_origin_sign_normalizations: originChecks,
  resource_gate_bounds_checked: true, dependency_hashes: Object.keys(report.dependency_sha256).length}));
