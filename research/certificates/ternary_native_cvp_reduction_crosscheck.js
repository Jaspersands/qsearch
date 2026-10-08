"use strict";
const fs = require("fs"), path = require("path"), crypto = require("crypto");
const r = JSON.parse(fs.readFileSync(process.argv[2] || path.join(__dirname, "../reductions/ternary_native_cvp_reduction.json"), "utf8"));
const check = (x, m) => { if (!x) throw Error(m); }, same = (a, b, m) => check(JSON.stringify(a) === JSON.stringify(b), m);
const B = x => { check(typeof x === "string" || typeof x === "bigint" || Number.isSafeInteger(x), "exact integer encoding"); return BigInt(x); };
const mod = (a, q) => (a % q+q) % q;
function gcd(a, b) { while (b) [a, b] = [b, a % b]; return a; }
function fraction(a, b = 1n) { const g = gcd(a, b); return b/g === 1n ? String(a/g) : (a/g)+"/"+(b/g); }
const parse = s => { const a = s.split("/").map(BigInt); return [a[0], a[1] || 1n]; };
check(r.status === "SOURCE_SPECIFIC_NEAR_EXACT_CVP_REDUCTION_REVIEW_PENDING" && !r.native_measurement_source_classically_simulated && !r.near_exact_CVP_solver_supplied && !r.accepted_speedup_candidate, "conditional reduction, not solver or source dequantization");
check(r.derivation_sha256 === crypto.createHash("sha256").update(fs.readFileSync(path.join(__dirname, "../TERNARY_NATIVE_CVP_REDUCTION.md"))).digest("hex"), "pinned CVP derivation");
same(r.source_controls.map(c => c.modulus), [3, 9, 27], "all bounded native root controls");
let modes = 0, pairs = 0;
for (const c of r.source_controls) {
  const q = c.modulus, h = (q-1)/2, center = x => mod(x+h, q)-h, points = [[0, 0], [1, 0], [0, 1]];
  const spectrum = new Map();
  for (const a of points) for (const b of points) {
    const key = JSON.stringify(a.map((x, j) => mod(x-b[j], q)));
    spectrum.set(key, (spectrum.get(key) || 0)+1);
  }
  let normalization = 0, mean = 0;
  for (let a = 0; a < q; a++) for (let b = 0; b < q; b++) {
    const re = 1+Math.cos(2*Math.PI*a/q)+Math.cos(2*Math.PI*b/q), im = Math.sin(2*Math.PI*a/q)+Math.sin(2*Math.PI*b/q);
    const p = (re*re+im*im)/(3*q*q); normalization += p; mean += p*(center(a)**2+center(b)**2); pairs++;
  }
  const uniform = (q*q-1)/6, gap = 2*Math.cos(Math.PI/q)/(3*Math.sin(Math.PI/q)**2);
  check(Math.abs(normalization-1) < 2e-12 && Math.abs(mean-(uniform-gap)) < 2e-11 && Math.abs(mean-c.direct_Born_true_pair_cost_diagnostic) < 2e-11, "actual full-root Born law and finite centered moment formula");
  const e = c.expected_costs;
  check(B(e.modulus) === BigInt(q) && e.uniform_pair_cost === fraction(BigInt(q*q-1), 6n) && Math.abs(e.true_pair_cost_diagnostic-mean) < 2e-11 && Math.abs(e.gap_over_modulus_squared_diagnostic-gap/(q*q)) < 2e-12 && gap/(q*q) >= 4/81-1e-14 && e.gap_over_modulus_squared_lower_bound === "4/81" && !e.diagnostic_floats_are_proof_certificates, "exact mean representation and analytic-bound diagnostic");
  let count = 0;
  for (let delta = 1; delta < q; delta++) {
    const order = q/Number(gcd(BigInt(q), BigInt(delta)));
    for (let u = 0; u < q; u++) for (let v = 0; v < q; v++) {
      const numerator = u % order || v % order ? 0 : spectrum.get(JSON.stringify([u, v])) || 0;
      check(numerator === (u === 0 && v === 0 ? 3 : 0), "all wrong-secret joint error characters vanish, including nonprimitive differences"); count++;
    }
  }
  check(c.complete_noise_pairs === q*q && c.all_nonzero_secret_differences_and_dual_pairs_checked === count && c.nonprimitive_differences_included, "complete bounded source scan counts"); modes += count;
}
same(r.population_ledgers.map(x => [x.secret_dimension, x.root_digits]), [[2, 2], [4, 8], [8, 16], [32, 64], [64, 128]], "growing dimension/root analytic regimes");
same(r.accuracy_copy_tradeoffs.map(x => [x.normalized_concentration_slack, x.sufficient_norm_approximation_factor]), [["1/81", "13/12"], ["1/128", "9/8"], ["1/4096", "19/16"]], "explicit approximation/copy tradeoff menu");
check(r.population_ledgers.every(x => x.normalized_concentration_slack === "1/128" && x.sufficient_norm_approximation_factor === "9/8"), "balanced profile at every growing regime");
for (const x of [...r.population_ledgers, ...r.accuracy_copy_tradeoffs]) {
  const n = x.secret_dimension, digits = x.root_digits, k = x.confidence_bits, [a, b] = parse(x.normalized_concentration_slack), [g, h] = parse(x.sufficient_norm_approximation_factor);
  check(a > 0n && 81n*a < 2n*b, "strict legal slack interval");
  const multiplier = (b*b+8n*a*a-1n)/(8n*a*a), M = Number(multiplier)*(2*n*digits+k+1), q = 3n**BigInt(digits);
  check(B(x.modulus) === q && x.secret_count_symbolic === "3^"+(n*digits) && x.original_measured_qutrits === M && x.full_Euclidean_lattice_dimension === 2*M, "full charged original-source and CVP dimensions");
  same(x.normalized_per_pair_cost_range, ["0", "1/2"], "bounded paired costs, not independent scalar samples");
  check(x.normalized_true_wrong_mean_gap_lower_bound === "4/81" && x.per_pair_Hoeffding_exponent_coefficient === fraction(8n*a*a, b*b) && B(x.integer_copy_multiplier) === multiplier, "analytic concentration/copy constants");
  const upperA = 162n*(b-6n*a), upperB = 6n*(19n*b+162n*a);
  check(x.squared_approximation_factor_strict_upper === fraction(upperA, upperB) && g*g*upperB < h*h*upperA, "strict norm-versus-squared approximation requirement");
  check(x.absolute_squared_radius_threshold === fraction(BigInt(M)*((q*q-1n)*b-6n*q*q*a), 6n*b) && x.ideal_failure_probability_upper === fraction(1n, 2n**BigInt(k)) && x.joint_input_trace_error === "0" && x.complete_failure_probability_upper === x.ideal_failure_probability_upper, "exact raw radius and failure budgets");
  check(!x.approximate_CVP_solver_supplied && !x.large_lattice_materialized && x.failure_bound_conditional_on_correct_CVP_approximation_promise && !x.CVP_solver_failure_probability_included && !x.polynomial_original_copy_budget_proves_polynomial_time && x.IID_full_native_labels_and_same_shared_secret_required && !x.wrong_secret_difference_must_be_primitive && !x.original_source_acquisition_cost_and_gate_errors_resolved && !x.accepted_speedup_candidate, "all unresolved approximation/access debts retained");
}
check(81n*1297n < 64n*1647n, "balanced rational approximation certificate");
console.log(JSON.stringify({status: "PASS", complete_Born_noise_pairs: pairs, exact_wrong_secret_dual_checks: modes, population_ledgers: r.population_ledgers.length, near_exact_CVP_solver_supplied: false}, null, 2));
