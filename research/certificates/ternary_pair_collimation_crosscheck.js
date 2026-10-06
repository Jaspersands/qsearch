"use strict";
// Independent full-word solver, native-root amplitudes, and exact source averages.
const fs = require("fs"), path = require("path");
const report = JSON.parse(fs.readFileSync(path.join(__dirname, "../phase_workbench/ternary_pair_collimation.json"), "utf8"));
function check(x, m) { if (!x) throw Error(m); }
function same(a, b, m) { check(JSON.stringify(a) === JSON.stringify(b), m); }
const mod = (x, q) => ((x % q) + q) % q;
function words(width) {
  let result = [[]]; for (let i = 0; i < width; i++) result = result.flatMap(w => [0, 1, 2].map(x => [...w, x])); return result;
}
function groupWords(moduli) {
  let result = [[]]; for (const q of moduli) result = result.flatMap(w => Array.from({length: q}, (_, x) => [...w, x])); return result;
}
function fraction(x) { const parts = x.split("/").map(BigInt); return [parts[0], parts[1] || 1n]; }
function equalFraction(x, numerator, denominator, message) { const [a, b] = fraction(x); check(a * denominator === b * numerator, message); }
function frequencies(labels, L) {
  let u = -1, v = 1; for (let j = 2; j < L; j += 2) [u, v] = [u + v, -u];
  const q = 3 ** (L / 2);
  return labels.map(register => [register.map(([a, b]) => mod(u * a + v * b, q)), register.map(([a, b]) => mod((u + v) * a - u * b, q))]);
}
function value(f, word, moduli) { return moduli.map((q, j) => mod(word.reduce((s, x, i) => s + (x ? f[i][x - 1][j] : 0), 0), q)); }
function pairByFullEnumeration(f, moduli, target) {
  const M = f.length, split = Math.floor(M / 2), answers = []; let rightVisited = 0;
  // Different implementation: no MITM table or fiber counter; bounded full words.
  for (const right of words(M - split)) {
    rightVisited++;
    for (const left of words(split)) {
      const word = [...left, ...right];
      if (JSON.stringify(value(f, word, moduli)) === JSON.stringify(target)) answers.push(word);
      if (answers.length === 2) return {pair: answers, rightVisited};
    }
  }
  return {pair: [], rightVisited};
}
function applyWord(word, recipe) {
  word = [...word];
  for (const g of recipe.gates) {
    if (g.gate === "ADD_F3") word[g.target] = mod(word[g.target] + g.coefficient, 3);
    else if (g.gate === "SCALE_F3") word[g.target] = mod(word[g.target] * g.coefficient, 3);
    else { check(g.gate === "SUM_F3", "explicit finite pair gates only"); word[g.target] = mod(word[g.target] + g.coefficient * word[g.control], 3); }
  }
  return word;
}
let bornBranches = 0, goodPairs = 0, basisWords = 0, reversibleAncillaWords = 0;
for (const c of report.native_full_root_physical_controls) {
  const f = frequencies(c.native_labels, c.original_even_level), q = Number(c.original_modulus), M = f.length, D = 3 ** M, j = c.target_coordinate;
  const moduli = f[0][0].map((_, l) => l === j ? q / 3 : q), low = f.map(pair => pair.map(row => row.map((x, l) => mod(x, moduli[l]))));
  same(moduli, c.low_solver_view.moduli, "target-only reduction leaves other coordinates full root"); same(low, c.low_solver_view.frequencies, "stripped actual native labels");
  const all = words(M), buckets = new Map();
  for (const w of all) { const key = value(low, w, moduli).join(","); if (!buckets.has(key)) buckets.set(key, []); buckets.get(key).push(w); }
  check(buckets.size === c.all_nonempty_syndrome_branches.length, "no nonempty syndrome omitted");
  const recipe = c.syndrome_recipe, expectedTape = [];
  low.forEach((pair, i) => pair.forEach((row, digit) => row.forEach((x, l) => {
    if (moduli[l] > 1 && x) expectedTape.push({gate: "digit_controlled_constant_modular_ADD", source_wire: i,
      source_digit: digit + 1, target_component: l, constant: x, modulus: moduli[l]});
  })));
  same(recipe.constant_addition_tape, expectedTape, "known modular addition recipe, not inverse function");
  check(recipe.clean_syndrome_qutrits === Math.round(Math.log(moduli.reduce((a, b) => a * b, 1)) / Math.log(3)), "syndrome register space");
  check(recipe.original_phase_register_retained_while_solver_runs && recipe.solver_runs_in_separate_workspace_not_controlled_by_unknown_word, "ordinary independent solver workspace");
  for (const w of all) for (const ancilla of groupWords(moduli)) {
    const out = [...ancilla];
    for (const g of expectedTape) if (w[g.source_wire] === g.source_digit) out[g.target_component] = mod(out[g.target_component] + g.constant, g.modulus);
    same(out, ancilla.map((x, l) => mod(x + value(low, w, moduli)[l], moduli[l])), "all-input reversible syndrome computation");
    for (const g of [...expectedTape].reverse()) if (w[g.source_wire] === g.source_digit) out[g.target_component] = mod(out[g.target_component] - g.constant, g.modulus);
    same(out, ancilla, "all ancillas inverse, not only initialized zero"); reversibleAncillaWords++;
  }
  let accepted = 0;
  const phase = F => { const angle = 2 * Math.PI * mod(F.reduce((s, x, l) => s + x * c.calibration_secret_only[l], 0), q) / q;
    return [Math.cos(angle) / Math.sqrt(D), Math.sin(angle) / Math.sqrt(D)]; };
  for (const b of c.all_nonempty_syndrome_branches) {
    const fiber = buckets.get(b.target.join(",")); check(fiber && fiber.length === b.reference_fiber_size_not_used_by_solver, "actual native fiber");
    equalFraction(b.syndrome_probability, BigInt(fiber.length), BigInt(D), "Born size-biased syndrome weight"); bornBranches++;
    const brute = pairByFullEnumeration(low, moduli, b.target); same(brute.pair, b.solver.pair, "independent ordinary pair finder");
    const cost = b.solver.cost, split = Math.floor(M / 2);
    same(cost.raw_half_assignments, [String(3 ** split), String(3 ** (M - split))], "reference exponential half cost");
    check(cost.left_words_enumerated === 3 ** split && cost.right_words_enumerated === brute.rightVisited && cost.right_hash_lookups === brute.rightVisited, "all actual solver enumeration charged");
    check(cost.uses_only_LowProblem && !cost.polynomial_witness_finder, "not a polynomial arithmetic breakthrough");
    if (!brute.pair.length) { check(!b.recipe && b.informative_projection_probability_unconditional === "0", "singleton/empty are not pairs"); continue; }
    const [u, v] = brute.pair, F0 = value(f, u, f[0][0].map(() => q)), F1 = value(f, v, f[0][0].map(() => q));
    const difference = F1.map((x, l) => mod(x - F0[l], q)); same(difference, b.relative_full_frequency, "actual original frequency difference");
    check(difference.every((x, l) => l === j ? x % (q / 3) === 0 : x === 0), "isolate requested secret, not a nuisance mixture");
    const delta = difference[j] / (q / 3); check(delta === b.target_trit_multiplier, "exact trit multiplier");
    equalFraction(b.selected_pair_projection_probability_given_syndrome, 2n, BigInt(fiber.length), "two-word coherent projector mass");
    if (!delta) { check(!b.recipe && b.informative_projection_probability_unconditional === "0" && b.rejection.includes("ZERO_TARGET"), "high-zero pair rejected without replacement"); continue; }
    const tape = b.recipe, permutation = all.map(w => applyWord(w, tape));
    same(permutation, b.reference_whole_basis_permutation, "entire basis pair compression");
    check(new Set(permutation.map(w => w.join(","))).size === D, "pair compression is unitary permutation"); basisWords += D;
    same(applyWord(u, tape), Array(M).fill(0), "first endpoint zero");
    same(applyWord(v, tape), Array.from({length: M}, (_, l) => Number(l === tape.pivot)), "second endpoint digit1");
    same(F0, b.original_anchor_phase_frequency, "original unknown anchor phase retained on measured branch");
    check(tape.projector.do_not_measure_which_endpoint && !tape.unknown_state_preparation_inverse_cloning_or_fiber_counter_required && !tape.identically_labeled_unknown_copies_required, "no endpoint measurement/free inverse/clones/matched copies");
    const amps = [phase(F0), phase(F1), [0, 0]];
    for (let k = 0; k < 3; k++) check(amps[k].every((x, l) => Math.abs(x - b.unnormalized_pivot_amplitudes[k][l]) < 2e-12), "original-root Born amplitudes");
    const probabilities = [0, 1, 2].map(y => {
      let re = 0, im = 0;
      for (let k = 0; k < 3; k++) { const angle = -2 * Math.PI * y * k / 3, [a, b] = amps[k]; re += a * Math.cos(angle) - b * Math.sin(angle); im += a * Math.sin(angle) + b * Math.cos(angle); }
      return (re * re + im * im) / 3 / (2 / D);
    });
    check(probabilities.every((x, k) => Math.abs(x - b.inverse_F3_probabilities[k]) < 2e-12), "actual inverse_F3 readout");
    const correct = mod(delta * c.calibration_secret_only[j], 3);
    check(probabilities.every((x, y) => Math.abs(x - (y === correct ? 2 / 3 : 1 / 6)) < 2e-12), "trit estimator, not purity diagnostic");
    equalFraction(b.informative_projection_probability_unconditional, 2n, BigInt(D), "all-failure raw projection probability"); accepted++; goodPairs++;
  }
  equalFraction(c.informative_acceptance, BigInt(2 * accepted), BigInt(D), "complete original-source acceptance");
  equalFraction(c.all_rejections_and_projection_failures, BigInt(D - 2 * accepted), BigInt(D), "all failure branches charged");
  equalFraction(c.unconditional_correct_including_uniform_failure_guess, BigInt(D + 2 * accepted), BigInt(3 * D), "uniform failure guess included");
  check(c.source_qutrits_consumed_per_attempt === M && !c.polynomial_witness_finder_or_full_depth_algorithm, "all original source inputs charged");
}
let unitMinorTriples = 0;
for (let M = 1; M <= 3; M++) {
  const all = words(M);
  for (const x of all) for (const y of all) for (const z of all) {
    if (new Set([x.join(","), y.join(","), z.join(",")]).size !== 3) continue;
    const A = x.flatMap((_, i) => [1, 2].map(d => Number(y[i] === d) - Number(x[i] === d))), B = x.flatMap((_, i) => [1, 2].map(d => Number(z[i] === d) - Number(x[i] === d)));
    let unit = false; for (let a = 0; a < 2 * M; a++) for (let b = a + 1; b < 2 * M; b++) if (Math.abs(A[a] * B[b] - A[b] * B[a]) === 1) unit = true;
    check(unit, "complete native simplex unit-minor census"); unitMinorTriples++;
  }
}
check(unitMinorTriples === report.all_native_pointed_triples_unit_minor_checks, "pointed-triple report");
const census = report.complete_original_source_census, law = [0, 0, 0, 0]; let pairs = 0, singletons = 0, naturalTwoNumerator = 0, highLifts = 0, informativeLifts = 0;
for (let a = 0; a < 9; a++) for (let c = 0; c < 9; c++) for (let y = 0; y < 9; y++) {
  const fiber = [0, a, c].flatMap((x, i) => x === y ? [i] : []); law[fiber.length]++;
  if (fiber.length === 1) singletons++;
  if (fiber.length === 2) naturalTwoNumerator += 2;
  if (fiber.length < 2) continue; pairs++;
  for (let ha = 0; ha < 3; ha++) for (let hc = 0; hc < 3; hc++) {
    const F = [0, a + 9 * ha, c + 9 * hc], delta = mod(F[fiber[1]] - F[fiber[0]], 27);
    check(delta % 9 === 0, "actual native high lift difference"); highLifts++; if (delta) informativeLifts++;
  }
}
same(law, [0, 1, 2, 3].map(k => census.fiber_size_instance_counts[k]), "entire low-target occupancy law");
equalFraction(census.uniform_target_pair_success_beta, BigInt(pairs), 729n, "uniform-target two-witness coverage");
equalFraction(census.informative_acceptance_exact, BigInt(2 * informativeLifts), 2187n, "full native source acceptance");
check(informativeLifts * 3 === highLifts * 2 && 2 * informativeLifts === 12 * pairs, "exact4*beta with uniform high trits");
equalFraction(census.raw_least_trit_success_exact, BigInt(2187 + 2 * informativeLifts), 6561n, "raw success including all rejected attempts");
equalFraction(census.natural_two_element_mass_exact, BigInt(naturalTwoNumerator), 243n, "source-weighted two-element mass");
equalFraction(census.singleton_only_single_witness_uniform_success, BigInt(singletons), 729n, "one-witness success is not pair coverage");
check(census.singleton_only_two_witness_success === "0" && highLifts === census.verified_pair_high_lifts && informativeLifts === census.informative_pair_high_lifts, "no single-to-two-witness shortcut");
let boundaryNativeLabelArrays = 0;
for (const c of report.constant_boundary_root_source_censuses) {
  const H = c.nuisance_group_size, law = [0, 0, 0, 0]; let pairs = 0;
  for (let a = 0; a < H; a++) for (let b = 0; b < H; b++) for (let y = 0; y < H; y++) {
    const size = [0, a, b].filter(x => x === y).length; law[size]++; if (size >= 2) pairs++;
  }
  check(H <= 3 && c.native_input_registers === 1 && c.dimension * Math.round(Math.log(c.original_modulus) / Math.log(3)) <= 2, "bounded terminal roots only");
  for (let k = 0; k < 4; k++) check((c.fiber_size_instance_counts[k] || 0) === law[k], "complete boundary native group occupancy law");
  equalFraction(c.uniform_target_pair_success_beta, BigInt(pairs), BigInt(H ** 3), "boundary ordinary pair coverage");
  equalFraction(c.informative_acceptance_exact, BigInt(4 * pairs), BigInt(9 * H * H), "generalized4H/(3D) transfer, not4*beta");
  equalFraction(c.raw_least_trit_success_exact, BigInt(9 * H * H + 4 * pairs), BigInt(27 * H * H), "complete boundary raw weak learner");
  check(c.full_native_label_arrays === 9 * H * H, "all boundary original labels"); boundaryNativeLabelArrays += c.full_native_label_arrays;
}
for (const c of report.underfull_solver_contracts) {
  const M = c.dimension * c.root_digits - 2, D = 3n ** BigInt(M), H = 3n * D, massNumerator = (D - 1n) * (H - D + 2n), massDenominator = H * H;
  check(BigInt(c.word_space_size) === D && BigInt(c.nuisance_group_size) === H && c.original_native_inputs_per_call === M, "original underfull entropy parameters");
  equalFraction(c.natural_mass_of_exactly_two_word_fibers_lower, massNumerator, massDenominator, "exact native two-element lower bound");
  const [xiA, xiB] = fraction(c.pointwise_distinct_pair_solver_success_required);
  equalFraction(c.uniform_target_pair_success_beta_lower, xiA * massNumerator, xiB * massDenominator * 6n, "conditional pair coverage lower");
  const [a, b] = fraction(c.uniform_target_pair_success_beta_lower);
  equalFraction(c.source_mean_informative_acceptance_lower, 4n * a, b, "four-beta source acceptance");
  equalFraction(c.source_mean_least_trit_advantage_lower, 4n * a, 3n * b, "conditional weak advantage, not supplied solver");
  equalFraction(c.expected_binary_phase_inputs_if_fresh_IID_vector_phases_available, BigInt(8 * M), 3n, "correct original binary acquisition cost");
  same(c.MITM_raw_half_assignment_bounds, [String(3n ** BigInt(Math.floor(M / 2))), String(3n ** BigInt(M - Math.floor(M / 2)))], "exponential MITM scaling");
  check(!c.pointwise_solver_guarantee_is_supplied && !c.polynomial_full_depth_algorithm && !c.cyclic_DHSP_natural_source_reduction_for_n_greater_than_one_supplied, "conditional solver/source reduction gates");
}
const sourceReport = JSON.parse(fs.readFileSync(path.join(__dirname, "../phase_workbench/cyclotomic_fiber_receiver.json"), "utf8"));
let directionalCostControls = 0;
for (const c of sourceReport.general_prime_source_and_charged_onehot_controls) {
  const cost = c.expected_binary_samples_per_native_qudit, yieldRate = c.expected_native_qudits_yield_per_forward_binary_input;
  check(BigInt(cost.numerator) * BigInt(yieldRate.numerator) === BigInt(cost.denominator) * BigInt(yieldRate.denominator), "forward source cost and yield have reciprocal units");
  const reverse = c.expected_native_qudits_per_binary_sample;
  check(2n * BigInt(reverse.numerator) === BigInt(c.prime) * BigInt(reverse.denominator), "reverse projection cost is p/2, not forward yield");
  const cycle = c.forward_then_reverse_expected_binary_cost_per_binary_output, d = c.prime - 1;
  check(BigInt(cycle.numerator) === BigInt(cycle.denominator) * BigInt(d) * 2n ** BigInt(d - 1), "lossy round-trip acquisition costs do not cancel");
  check(Math.abs(c.reverse_two_word_projection_probability - 2 / c.prime) < 2e-12 && c.reverse_cost_is_not_the_forward_yield, "different-direction projection losses");
  same(c.reverse_accepted_native_digits, [0, 1], "actual reverse projection support");
  const input = c.conditional_native_qudit_amplitudes, output = c.reverse_conditional_binary_amplitudes;
  check(output.every((z, j) => z.every((x, k) => Math.abs(x - input[j][k] / Math.sqrt(2 / c.prime)) < 2e-12)), "physical reverse projection amplitudes"); directionalCostControls++;
}
check(!report.accepted_candidate && !report.novelty_claim && !report.polynomial_witness_finder && !report.new_full_depth_quantum_algorithm && !report.quantum_state_oracle_inverse_cloning_fiber_counter_or_identical_copies_granted, "global no-free-oracle / no-speedup gates");
process.stdout.write(JSON.stringify({status: "independent_replay_passed", native_syndrome_branches: bornBranches,
  informative_pair_branches: goodPairs, complete_pair_basis_words: basisWords, all_syndrome_ancilla_inputs: reversibleAncillaWords,
  simplex_unit_minor_triples: unitMinorTriples, uniform_target_instances: 729, native_high_lift_pairs: highLifts,
  informative_high_lift_pairs: informativeLifts, directional_onehot_source_controls: directionalCostControls,
  boundary_native_label_arrays: boundaryNativeLabelArrays,
  polynomial_pair_finder: false}) + "\n");
