"use strict";
// Independent rational budgets and exact visibility powers; no hardware claim.
const fs = require("fs"), path = require("path"), crypto = require("crypto");
const E = require("./cyclotomic_exact.js"), native = require("./native_uniform_descent_crosscheck.js");
const {check, same, rat, parse, str, add, sub, mul, div, cmp, one, zero} = E;
const ROOT = path.resolve(__dirname, "../.."), REPORT = path.join(ROOT, "research/reductions/native_descent_noise_composition.json");
const RECEIVER = path.join(ROOT, "research/reductions/native_uniform_descent_receiver.json");
const hash = f => crypto.createHash("sha256").update(fs.readFileSync(f)).digest("hex");
const min = (a, b) => cmp(a, b) <= 0n ? a : b, max = (a, b) => cmp(a, b) >= 0n ? a : b;
const scale = (a, n) => mul(a, rat(n));
const eq = (encoded, expected, message) => check(encoded === str(expected), message);
function power(x, exponent) {
  let result = one;
  while (exponent) {
    if (exponent % 2) result = mul(result, x);
    exponent = Math.floor(exponent/2);
    if (exponent) x = mul(x, x);
  }
  return result;
}
function budget(b) {
  native.contract(b.resource_contract);
  const C = BigInt(b.resource_contract.original_copy_upper), L = BigInt(b.resource_contract.level), K = BigInt(b.resource_contract.fresh_digit_samples_per_level);
  check(b.original_copy_cap === String(C), "original-copy cap, not an attractive ideal-run count");
  const SUM = (L-1n)*C, digit = (2n*L-1n)*K, measured = SUM+L*K;
  check(b.known_SUM_gate_upper === String(SUM) && b.known_digit_gate_upper === String(digit) && b.measurement_upper === String(measured), "all SUM, correction, Fourier and measurement calls charged");
  const delta = parse(b.per_original_trace_promise), gate = parse(b.per_unitary_operator_error_promise), meas = parse(b.per_measurement_half_diamond_promise);
  [delta, gate, meas].forEach(e => check(cmp(e, zero) >= 0n && cmp(e, one) <= 0n, "bounded promised error"));
  const source = min(one, scale(delta, C)), unitary = min(one, scale(gate, SUM+digit)), instrument = min(one, scale(meas, measured));
  const total = min(one, add(add(source, unitary), instrument)), rank = parse(b.resource_contract.ideal_IID_rank_failure_upper);
  eq(b.original_source_loss_upper, source, "joint independent input trace error");
  eq(b.gate_loss_upper, unitary, "unitary hybrid error");
  eq(b.measurement_loss_upper, instrument, "measurement instrument hybrid error");
  eq(b.total_implementation_loss_upper, total, "adaptive CPTP error, no rare-branch division");
  eq(b.ideal_rank_failure_upper, rank, "ideal rank error unchanged");
  eq(b.full_correct_recovery_lower, max(zero, sub(sub(one, rank), total)), "conditional full recovery lower bound");
  ["promises_established_from_sample_values", "marginal_bounds_cover_correlated_sources", "actual_success_predicted_by_vacuous_upper", "universal_noise_lower_bound"].forEach(k => check(b[k] === false, "error promise scope "+k));
}
function run(r) {
  check(r.status === "SCOPED_NATIVE_DESCENT_NOISE_COMPOSITION_EXTERNAL_REVIEW_PENDING", "scoped review-pending noise status");
  check(r.producer_sha256 === hash(path.join(ROOT, "theorems/native_descent_noise_composition.py")) &&
        r.derivation_sha256 === hash(path.join(ROOT, "research/NATIVE_DESCENT_NOISE_COMPOSITION.md")) &&
        r.receiver_artifact_sha256 === hash(RECEIVER), "pinned producer, derivation and source transcript");
  ["growing_depth_robust_receiver_supplied", "noise_proves_universal_impossibility", "dephasing_is_the_Gaussian_source", "accepted_speedup_candidate"].forEach(k => check(r[k] === false, "unjustified noise or speedup promotion"));
  const receiver = JSON.parse(fs.readFileSync(RECEIVER, "utf8"));
  native.run(receiver);
  const parameters = [[4, 1, zero], [4, 1, rat(1n, 4n**10n)],
                      ...[[4, 1], [8, 2], [8, 8], [32, 32], [128, 128]].map(([n, d]) => [n, d, rat(1n, BigInt(n)**6n)])];
  check(r.even_input_compositions.length === parameters.length, "all noisy-input compositions and positive controls");
  r.even_input_compositions.forEach((c, i) => {
    const [n, exponent, moment] = parameters[i], q = 3n**BigInt(exponent), b = c.receiver_budget, input = c.native_input_bound;
    check(c.dimension === n && c.root_exponent === exponent && c.native_even_level === 2*exponent && b.resource_contract.dimension === n && b.resource_contract.level === 2*exponent, "actual even native input level");
    eq(c.normalized_integer_error_second_moment, moment, "V/q^2 assumption");
    const C = BigInt(b.resource_contract.original_copy_upper), bits = 64+(2n*C-1n).toString(2).length, prep = rat(2n, 2n**BigInt(bits));
    check(input.gate_budget.failure_bits === 64 && input.gate_budget.local_gate_precision_bits === bits, "paid C-register preparation precision");
    eq(input.gate_budget.per_state_preparation_trace_error_upper, min(one, prep), "native preparation error");
    eq(input.gate_budget.M_state_preparation_trace_error_upper, min(one, scale(prep, C)), "all preparation errors");
    eq(input.source_integer_second_moment_upper, scale(moment, q*q), "actual integer moment V");
    eq(input.per_state_averaged_trace_distance_upper, min(one, scale(moment, 20n)), "averaged symmetric-source trace theorem, not every realization");
    eq(input.M_state_success_loss_before_source_rounding_upper, min(one, add(scale(min(one, scale(moment, 20n)), C), min(one, scale(prep, C)))), "original-source loss with preparation");
    eq(b.per_original_trace_promise, min(one, add(scale(moment, 20n), prep)), "composed per-original promise");
    check(c.classical_original_records_upper === String(2n*C) && String(input.input_classical_originals_required) === String(2n*C) && String(input.independent_native_qutrits_supplied_in_gate_model) === String(C), "paid original classical-pair count");
    check(c.source_rounding_loss_included === false && c.growing_depth_noise_robustness_established === false && c.classical_original_data_hardness_established === false, "source rounding and hardness remain open");
    budget(b);
  });
  check(r.dephasing_exposure_contracts.length === 12, "all compact original-ancestry contracts");
  r.dephasing_exposure_contracts.forEach((c, i) => {
    const n = BigInt([8, 32, 128][Math.floor(i/4)]), B = [n, n*n, n**4n, n**(2n*n)][i % 4], eta = rat(1n, n**6n);
    check(c.original_ancestors === String(B), "ancestry is a declared exposure, not a claimed typical copy cost");
    eq(c.per_original_dephasing, eta, "independent phase-dephasing probability");
    eq(c.per_original_trace_distance_exact, div(scale(eta, 2n), rat(3n)), "exact dephasing trace distance");
    same(c.retained_visibility_exact_compact, {base: str(sub(one, eta)), exponent: String(B)}, "compact exact product contrast, no huge-power materialization");
    const lower = max(zero, sub(one, scale(eta, B))), upper = div(one, add(one, scale(eta, B)));
    eq(c.retained_visibility_lower, lower, "Bernoulli lower contrast");
    eq(c.retained_visibility_upper, upper, "inverse-Bernoulli upper contrast");
    eq(c.correct_character_probability_upper, div(add(one, scale(upper, 2n)), rat(3n)), "correct-character probability");
    eq(c.correct_character_advantage_above_chance_upper, div(scale(upper, 2n), rat(3n)), "contrast above chance");
    check(c.bound_applies_to_this_measured_compression === true && c.all_receivers_excluded === false && c.Gaussian_noise_identified_with_dephasing === false, "specific instrument and explicit noise family only");
  });
  let transcriptControls = 0;
  check(r.source_transcript_controls.length === 5, "all independently replayed source controls");
  r.source_transcript_controls.forEach((c, i) => {
    const original = receiver.source_driven_receiver_controls[i];
    check(c.dimension === original.dimension && c.level === original.level && c.conditional_noise_losses.length === 4, "fixed source transcript dimensions");
    const counts = new Map();
    original.result.completed_digit_stages.forEach(s => s.digit_measurement_original_lineages.forEach(ids => counts.set(ids.length, (counts.get(ids.length) || 0)+1)));
    c.conditional_noise_losses.forEach((f, j) => {
      const eta = parse(["0", "1/1000", "1/100", "1/10"][j]), factors = [];
      eq(f.per_original_dephasing, eta, "predeclared dephasing control");
      let p = one;
      for (const [B, count] of [...counts].sort((a, b) => a[0]-b[0])) {
        const v = power(sub(one, eta), B), correct = div(add(one, scale(v, 2n)), rat(3n));
        factors.push({original_ancestors: B, measured_packets: count, visibility_exact: str(v), correct_character_probability_exact: str(correct)});
        p = mul(p, power(correct, count));
      }
      same(f.packet_ancestry_factors, factors, "actual independent physical ancestry, not free lower samples");
      eq(f.conditional_all_correct_readouts_exact, p, "exact fixed-transcript correct-readout event");
      eq(f.conditional_readout_failure_exact, sub(one, p), "fixed-transcript noise loss");
      check(f.noisy_receiver_executed === false && f.error_correcting_decoder_supplied === false && f.fresh_lower_prefix_guessed === false && f.new_quantum_speedup_established === false, "no simulated noisy decoder or universal noise guarantee");
      transcriptControls++;
    });
  });
  let symmetricControls = 0;
  check(r.symmetric_error_transcript_controls.length === 5, "all symmetric-error original-source controls");
  r.symmetric_error_transcript_controls.forEach((c, i) => {
    const original = receiver.source_driven_receiver_controls[i], out = original.result, counts = new Map();
    check(c.dimension === original.dimension && c.level === original.level && c.conditional_noise_losses.length === 3, "symmetric-error source dimensions");
    const key = (L, ids) => L+":"+JSON.stringify(ids);
    for (let j = 0; j < out.original_inputs_supplied; j++) counts.set(key(c.level, [j]), [1, 0, 0]);
    for (const stream of out.descent_streams) for (const b of stream.complete_output_records) {
      const sum = [0, 0, 0], offsets = [0, ...b.measured_complement];
      b.input_original_lineages.forEach((ids, j) => {
        const parent = counts.get(key(stream.parent_level, ids));
        check(parent, "original offset lineage exists");
        parent.forEach((n, t) => sum[(t+offsets[j]) % 3] += n);
      });
      check(sum.reduce((a, b) => a+b, 0) === b.original_source_indices.length, "all original error offsets retained");
      counts.set(key(stream.child_level, b.original_source_indices), sum);
    }
    c.conditional_noise_losses.forEach((f, j) => {
      const gamma = parse(["9/10", "99/100", "999/1000"][j]), factors = [];
      eq(f.symmetric_error_characteristic, gamma, "symmetric-error characteristic promise");
      check(f.original_kernel === "[[1,gamma,gamma],[gamma,1,gamma^2],[gamma,gamma^2,1]]", "actual two-independent-error kernel, not isotropic noise");
      let p = one;
      for (const stage of out.completed_digit_stages) for (const ids of stage.digit_measurement_original_lineages) {
        const offsetCounts = counts.get(key(stage.level, ids)), B = ids.length;
        check(offsetCounts && offsetCounts.reduce((a, b) => a+b, 0) === B, "final original error ancestry");
        const contrasts = offsetCounts.map(n => power(gamma, B+n));
        const correct = add(rat(1n, 3n), mul(rat(2n, 9n), contrasts.reduce(add, zero)));
        factors.push({level: stage.level, original_lineage: ids, original_offset_counts_mod3: offsetCounts,
                      unordered_offdiagonal_contrasts_exact: contrasts.map(str), correct_character_probability_exact: str(correct)});
        p = mul(p, correct);
      }
      same(f.packet_factors, factors, "exact transported original offsets and anisotropic Schur contrasts");
      eq(f.conditional_all_correct_readouts_exact, p, "fixed-transcript symmetric noise correct-readout event");
      check(f.original_error_characteristic_is_a_source_promise === true && f.noisy_receiver_executed === false &&
            f.Gaussian_density_identified_from_moment === false && f.error_correcting_decoder_supplied === false &&
            f.new_quantum_speedup_established === false, "no fabricated source law or robust noisy receiver");
      symmetricControls++;
    });
  });
  check(r.fixed_tree_mean_controls.length === 4, "fixed unfiltered tree mean controls");
  r.fixed_tree_mean_controls.forEach((c, i) => {
    const B = [1, 4, 16, 64][i], g = rat(999n, 1000n);
    check(c.original_ancestors === B && c.characteristic === str(g) && c.adaptive_tree_average_law_proved === false, "fixed unfiltered tree only, not adaptive posterior");
    eq(c.uniform_offset_mean_visibility_exact, power(div(mul(g, add(rat(2n), g)), rat(3n)), B), "exact fixed-tree multinomial mean contrast");
  });
  return {status: "PASS", source_compositions: 7, dephasing_exposures: 12,
          transcript_noise_controls: transcriptControls, symmetric_error_controls: symmetricControls,
          universal_impossibility_established: false};
}
if (require.main === module) console.log(JSON.stringify(run(JSON.parse(fs.readFileSync(process.argv[2] || REPORT, "utf8"))), null, 2));
module.exports = {run};
