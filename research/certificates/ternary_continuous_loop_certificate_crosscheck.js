"use strict";
const fs = require("fs"), path = require("path"), crypto = require("crypto");
const {check, same, rat, zero, one, add, mul, div, str, cmp} = require("./cyclotomic_exact.js");
const root = path.join(__dirname, "../..");
const parentPath = path.join(root, "research/phase_workbench/ternary_two_layer_path_transfer.json");
const P = JSON.parse(fs.readFileSync(parentPath, "utf8"));
const R = JSON.parse(fs.readFileSync(process.argv[2] || path.join(root,
  "research/phase_workbench/ternary_continuous_loop_certificate.json"), "utf8"));
const hash = p => crypto.createHash("sha256").update(fs.readFileSync(p)).digest("hex");
check(R.derivation_sha256 === hash(path.join(root, "research/TERNARY_CONTINUOUS_LOOP_CERTIFICATE.md")), "pinned loop derivation");
check(R.parent_artifact_sha256 === hash(parentPath), "pinned parent transfer artifact");
check(R.status === "ALL_CONTINUOUS_LOOPS_CERTIFIED" && R.all_continuous_self_loop_moduli_at_most_one === true,
  "complete exact continuous certificate, not unknown");
for (const flag of ["floating_optimizer_is_only_support_selection", "complete_exact_rational_identities_required"])
  check(R[flag] === true, "exact certification premise: " + flag);
for (const flag of ["general_mixer_or_deeper_circuit_lower_bound", "quantum_speedup_proved", "candidate_record_accepted", "novelty_claim"])
  check(R[flag] === false, "unsupported continuous-loop claim: " + flag);
const key = JSON.stringify;
function cube(q, n) {
  let out = [[]];
  for (let i = 0; i < n; i++) out = out.flatMap(w => Array.from({length: q}, (_, j) => [...w, j]));
  return out;
}
const nodes = cube(3, 2), patterns = cube(3, 4), states = P.complete_integer_lattice_graph;
same(R.polynomial_monomials, nodes, "all nine integer monomials");
check(states.length === 137 && R.complete_lattice_states === 137 && R.loop_certificates.length === 137,
  "all states, no omitted loops");
function square(coefficients) {
  const out = new Map();
  for (const [a, v] of coefficients) for (const [b, w] of coefficients) {
    const e = key([a[0]-b[0], a[1]-b[1]]);
    out.set(e, (out.get(e) || 0n) + v*w);
  }
  return out;
}
function actualLoop(state, index) {
  const coefficients = new Map();
  patterns.forEach(([x, t, xp, tp], k) => {
    if (state.coordinate_pattern_next_states[k] !== index) return;
    const gateCoefficients = [t === 0 ? 2 : -1, t === x ? 2 : -1,
      tp === 0 ? 2 : -1, tp === xp ? 2 : -1];
    for (let mask = 0; mask < 16; mask++) {
      const e = [Number(!!(mask&2))-Number(!!(mask&8)), Number(!!(mask&1))-Number(!!(mask&4))];
      let v = 1n;
      for (let j = 0; j < 4; j++) if (mask&(1<<j)) v *= BigInt(gateCoefficients[j]);
      coefficients.set(key(e), (coefficients.get(key(e)) || 0n)+v);
    }
  });
  return [...coefficients].map(([e, v]) => [JSON.parse(e), v]);
}
let squaresChecked = 0;
const distinctLoops = new Set();
states.forEach((state, i) => {
  const actual = actualLoop(state, i), record = R.loop_certificates[i];
  check(record.state === i && record.certificate.status === "EXACT_TORUS_SOS", "ordered complete exact state certificate");
  const parent = P.signed_transfer_structure_certificate.all_self_loop_Laurent_coefficients[i];
  for (const e of parent.Laurent_coefficients) {
    const v = actual.find(([a]) => a[0] === e.beta1_exponent && a[1] === e.beta2_exponent)?.[1] || 0n;
    check(String(v) === e.coefficient_numerator_over81, "actual gate expansion equals parent coefficients");
  }
  distinctLoops.add(key(actual.map(([e, v]) => [e, String(v)])));
  const product = square(actual), defect = new Map();
  for (const [e, v] of product) defect.set(e, rat(-v));
  defect.set(key([0, 0]), add(defect.get(key([0, 0])) || zero, rat(6561n)));
  const sum = new Map();
  for (const term of record.certificate.squares) {
    const c = require("./cyclotomic_exact.js").parse(term.weight), vector = term.integer_coefficients;
    check(cmp(c, zero) > 0n && vector.length === 9 && vector.every(Number.isSafeInteger)
      && vector.some(Boolean) && vector.reduce((a, b) => a+b, 0) === 0,
    "positive rational weight and zero-sum nonzero integer factor");
    const factor = nodes.map((e, j) => [e, BigInt(vector[j])]);
    for (const [e, v] of square(factor)) sum.set(e, add(sum.get(e) || zero, mul(c, rat(v))));
    squaresChecked++;
  }
  for (const e of new Set([...defect.keys(), ...sum.keys()]))
    check(cmp(defect.get(e) || zero, sum.get(e) || zero) === 0n, "every exact Laurent defect coefficient");
});
check(R.unique_loop_polynomials === distinctLoops.size && distinctLoops.size === 119, "all distinct actual polynomials");

function choose(n, k) {let v = 1n; for (let j = 0; j < k; j++) v = v*BigInt(n-j)/BigInt(j+1); return v;}
function capped(a) {return cmp(a, one) < 0n ? a : one;}
function isqrt(a) {
  if (a < 2n) return a;
  let x = 1n << BigInt(Math.ceil(a.toString(2).length/2));
  for (;;) {const y = (x+a/x)/2n; if (y >= x) return x; x = y;}
}
function sqrtUpper(a) {
  const scale = 1n << 80n, value = a[0]*a[1]*scale*scale, x = isqrt(value);
  return rat(x*x === value ? x : x+1n, scale*a[1]);
}
function born(s, n, q, M) {return capped(add(s, sqrtUpper(mul(rat(q**BigInt(n)-1n, 3n**BigInt(M)), s))));}
check(R.sharpened_population_envelopes.length === 4, "all specified growing envelopes");
for (const c of R.sharpened_population_envelopes) {
  const n = c.dimension, q = BigInt(c.modulus), M = c.original_native_inputs, G = q**BigInt(n);
  let s = zero;
  for (let j = 0; j <= Math.min(5, M); j++) s = add(s, rat(choose(M, j)*18n**BigInt(j), G));
  s = capped(s);
  const m = BigInt(c.implicit_four_angle_net_axis_points), inverse = (s[1]+s[0]-1n)/s[0];
  check((m-1n)**5n < inverse && m**5n >= inverse, "exact fifth-root net size");
  const error = rat(BigInt(88*(n+M)), 7n*m), tuned = capped(add(mul(rat(m**4n), s), error));
  check(c.continuous_loop_growth_upper === "1" && c.strict_path_depth === 5 && c.off_diagonal_weight_row_norm_upper === "18",
    "certified continuous transfer constants");
  check(c.all_fixed_continuous_angles_uniform_success_upper === str(s)
    && c.all_fixed_continuous_angles_Born_success_upper === str(born(s, n, q, M))
    && c.implicit_four_angle_net_total_points === String(m**4n)
    && c.implicit_net_rounding_probability_error_upper === str(error)
    && c.public_adaptive_four_angle_uniform_success_upper === str(tuned)
    && c.public_adaptive_four_angle_Born_success_upper === str(born(tuned, n, q, M)), "sharpened exact bounds and source correction");
  for (const flag of ["requires_all_137_exact_loop_certificates_and_parent_transfer_premises",
    "fixed_coordinate_dependent_mixer_angles_covered", "arbitrary_fixed_residual_phase_functions_covered",
    "label_trained_coordinate_angles_or_residual_functions_not_covered", "adaptive_four_angle_bound_requires_original_mismatch_cost_template",
    "Born_decay_depends_on_original_input_count", "other_mixer_shapes_deeper_circuits_and_other_receivers_not_covered"])
    check(c[flag] === true, "fixed/adaptive scope: " + flag);
}

const Z = [0n, 0n], O = [1n, 0n], Q = [[1n, 0n], [0n, -1n], [-1n, 0n], [0n, 1n]];
const ca = (a, b) => [a[0]+b[0], a[1]+b[1]], cm = (a, b) => [a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0]];
const conj = a => [a[0], -a[1]];
function gate(b, equal) {const a = Q[b]; return equal ? [1n+2n*a[0], 2n*a[1]] : [1n-a[0], -a[1]];}
function edges(b1, b2) {
  return states.map(s => {
    const out = new Map();
    patterns.forEach(([x, t, xp, tp], k) => {
      const w = cm(cm(gate(b2, t === 0), gate(b1, t === x)), conj(cm(gate(b2, tp === 0), gate(b1, tp === xp))));
      const j = s.coordinate_pattern_next_states[k]; out.set(j, ca(out.get(j) || Z, w));
    });
    return [...out].filter(([, a]) => a[0] || a[1]);
  });
}
let nativeTargets = 0;
check(R.complete_fixed_function_native_controls.length === 3, "all full-root native regression controls");
for (const c of R.complete_fixed_function_native_controls) {
  const n = c.dimension, q = Number(c.modulus), M = c.original_native_inputs, G = q**n;
  const words = cube(3, M), targets = cube(q, n), D = words.length, code = v => v.reduce((s, a) => q*s+a, 0);
  const b1 = c.coordinate_beta1_quarters, b2 = c.coordinate_beta2_quarters, f1 = c.full_root_phase1_quarters, f2 = c.full_root_phase2_quarters;
  check(f1.length === G && f2.length === G && b1.length === M && b2.length === M, "complete phase tables and coordinate schedules");
  let actual = zero, actualBorn = zero, labels = 0;
  for (const rows of cube(q, 2*M*n)) {
    const F = words.map(w => Array.from({length: n}, (_, j) => w.reduce((s, t, i) => s+(t ? rows[(2*i+t-1)*n+j] : 0), 0)%q));
    for (const y of targets) {
      const residual = F.map(v => code(v.map((a, j) => (a-y[j]+q)%q)));
      let state = words.map(() => O);
      for (const [schedule, f] of [[b1, f1], [b2, f2]]) {
        state = state.map((a, i) => cm(a, Q[f[residual[i]]]));
        for (let axis = 0; axis < M; axis++) state = words.map(w => {
          let a = Z;
          for (let t = 0; t < 3; t++) {const v = w.slice(); v[axis] = t;
            a = ca(a, cm(gate(schedule[axis], t === w[axis]), state[v.reduce((s, t) => 3*s+t, 0)]));}
          return a;
        });
      }
      const marked = F.map((v, i) => key(v) === key(y) ? i : -1).filter(i => i >= 0);
      const raw = rat(marked.reduce((s, i) => s+state[i][0]**2n+state[i][1]**2n, 0n), BigInt(D)*81n**BigInt(M));
      actual = add(actual, div(raw, rat(BigInt(G)))); actualBorn = add(actualBorn, mul(raw, rat(BigInt(marked.length), BigInt(D))));
    }
    labels++;
  }
  actual = div(actual, rat(BigInt(labels))); actualBorn = div(actualBorn, rat(BigInt(labels)));
  let W = new Map([[0, O]]);
  for (let axis = 0; axis < M; axis++) {
    const E = edges(b1[axis], b2[axis]), next = new Map();
    for (const [i, a] of W) for (const [j, b] of E[i]) next.set(j, ca(next.get(j) || Z, cm(a, b)));
    W = new Map([...next].filter(([, a]) => a[0] || a[1]));
  }
  let predicted = zero, imaginary = zero;
  for (const [i, weight] of W) {
    const basis = states[i].basis_columns, rank = basis.length; let moment = Z;
    for (const coefficients of cube(q, rank*n)) {
      const d = Array.from({length: 4}, (_, branch) => code(Array.from({length: n}, (_, j) =>
        ((basis.reduce((s, column, k) => s+column[branch]*coefficients[j*rank+k], 0)%q)+q)%q)));
      const phase = ((f1[d[0]]+f2[d[1]]-f1[d[2]]-f2[d[3]])%4+4)%4;
      moment = ca(moment, Q[phase]);
    }
    const numerator = cm(weight, moment), denominator = BigInt(q)**BigInt(rank*n)*81n**BigInt(M)*BigInt(G);
    predicted = add(predicted, rat(numerator[0], denominator)); imaginary = add(imaginary, rat(numerator[1], denominator));
  }
  check(cmp(imaginary, zero) === 0n && cmp(actual, predicted) === 0n
    && c.actual_direct_circuit_uniform_mean_exact === str(actual) && c.actual_direct_circuit_Born_mean_exact === str(actualBorn)
    && c.arbitrary_residual_lattice_transfer_mean_exact === str(predicted)
    && c.entire_IID_label_matrices === labels && c.complete_uniform_target_cases === labels*G,
  "independent complete arbitrary-residual law and native circuit census");
  check(c.fixed_before_labels_and_target === true && c.capped_census_is_not_a_compiled_receiver === true, "native control scope");
  nativeTargets += labels*G;
}
console.log(JSON.stringify({status: "PASS", continuous_loops: 137, exact_positive_squares: squaresChecked,
  all_Laurent_coefficients_verified: true, growing_envelopes: 4, complete_native_target_controls: nativeTargets}));
