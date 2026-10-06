"use strict";
// Independent integer geometry, witness/cost replay; NOT an independent LLL search.
const fs = require("fs"), path = require("path");
const report = JSON.parse(fs.readFileSync(path.join(__dirname, "../phase_workbench/ternary_pair_lattice.json"), "utf8"));
function check(x, m) { if (!x) throw Error(m); }
const mod = (x, q) => ((x % q) + q) % q;
const dot = (a, b) => a.reduce((s, x, i) => s + x * b[i], 0n);
const big = x => x.map(BigInt);
function same(a, b, message) { check(a.length === b.length && a.every((x, i) => x === b[i]), message); }
function E(z) { const result = []; for (let i = 0; i < z.length; i += 2) result.push(z[i] + z[i+1], -z[i], -z[i+1]); return result; }
function norm(z) { const v = E(z.map(x => 3n*x - 1n)); return dot(v, v); }
function value(A, w, Q) { return mod(w.reduce((s, x, i) => s + (x ? A[2*i+x-1] : 0n), 0n), Q); }
function words(M) { let result = [[]]; for (let i = 0; i < M; i++) result = result.flatMap(w => [0, 1, 2].map(x => [...w, x])); return result; }
function points(d, lower, upper) { let result = [[]]; for (let i = 0; i < d; i++) result = result.flatMap(w => Array.from({length: upper-lower+1}, (_, j) => [...w, BigInt(lower+j)])); return result; }
function det(matrix) {
  const a = matrix.map(row => [...row]), n = a.length; let last = 1n, sign = 1n;
  for (let k = 0; k < n-1; k++) {
    if (!a[k][k]) { const p = a.findIndex((row, i) => i > k && row[k]); if (p < 0) return 0n; [a[p], a[k]] = [a[k], a[p]]; sign = -sign; }
    const pivot = a[k][k];
    for (let i = k+1; i < n; i++) for (let j = k+1; j < n; j++) {
      const numerator = pivot*a[i][j]-a[i][k]*a[k][j]; check(numerator % last === 0n, "exact Bareiss determinant division"); a[i][j] = numerator/last;
    }
    for (let i = k+1; i < n; i++) a[i][k] = 0n;
    last = pivot;
  }
  return sign*a[n-1][n-1];
}
function fracEqual(text, a, b, message) { const parts = text.split("/").map(BigInt); check(parts[0]*b === a*(parts[1] || 1n), message); }
function legalPair(A, Q, target, pair) {
  check(pair.length === 2 && pair[0].join(",") !== pair[1].join(","), "two distinct native words");
  for (const w of pair) { check(w.length*2 === A.length && w.every(x => Number.isInteger(x) && x >= 0 && x <= 2), "original native alphabet"); check(value(A, w, Q) === target, "original modular target"); }
}
let localPoints = 0, globalPoints = 0, cosetPoints = 0, acceptedTraces = 0, censusPairs = 0, sweepPairs = 0, deflatedPairs = 0;
for (const [a, b] of points(2, -9, 9)) {
  const N = a*a+a*b+b*b-a-b;
  check(N >= 0n && norm([a, b]) === 18n*N+6n, "exact local A2 identity");
  const legal = (a === 0n && b === 0n) || (a === 1n && b === 0n) || (a === 0n && b === 1n);
  check((N === 0n) === legal && (legal || norm([a, b]) >= 24n), "local shell and invalid gap"); localPoints++;
}
for (const z of points(6, -1, 2)) {
  const legal = [0, 2, 4].every(i => (z[i] === 0n && z[i+1] === 0n) || (z[i] === 1n && z[i+1] === 0n) || (z[i] === 0n && z[i+1] === 1n));
  check((norm(z) === 18n) === legal && (legal || norm(z) >= 36n), "global shell/gap"); globalPoints++;
}
const control = report.independent_replay_control, g = control.geometry;
const A = big(control.labels), Q = BigInt(control.modulus), B = g.kernel_rows.map(big), L = g.embedded_rows.map(big), d = A.length;
check(det(B) === Q || det(B) === -Q, "complete scalar kernel index");
for (let i = 0; i < d; i++) { same(L[i], E(B[i]).map(x => 3n*x), "integer embedding"); check(mod(dot(A, B[i]), Q) === 0n, "kernel congruence"); }
const gram = L.map(left => L.map(right => dot(left, right)));
check(det(gram) === 3n**BigInt(5*d/2)*Q*Q, "exact rectangular Gram determinant");
for (const basis of control.bases) {
  const U = basis.transform.map(big), R = basis.rows.map(big), determinant = det(U);
  check(determinant === 1n || determinant === -1n, "unimodular basis transform");
  for (let i = 0; i < d; i++) same(R[i], L[0].map((_, j) => U[i].reduce((s, x, k) => s+x*L[k][j], 0n)), "exact reduced basis identity");
}
for (const c of control.targets) {
  const t = BigInt(c.target), z0 = big(c.z0), T = big(c.target_row);
  check(mod(dot(A, z0), Q) === t, "particular coset solution");
  same(T, E(Array(d).fill(1n)).map((x, i) => x-3n*E(z0)[i]), "exact CVP target");
  for (const z of points(d, -2, 2)) {
    const l = z.map((x, i) => x-z0[i]), P = E(l).map(x => 3n*x), residual = P.map((x, i) => x-T[i]);
    check(dot(residual, residual) === norm(z), "coset norm identity");
    if (mod(dot(A, z), Q) === t) {
      const coeff = [...l], p = g.pivot;
      const remainder = l[p]-l.reduce((s, x, j) => s+(j === p ? 0n : x*B[j][p]), 0n);
      check(remainder % Q === 0n, "kernel completeness pivot division"); coeff[p] = remainder/Q;
      same(l, A.map((_, j) => coeff.reduce((s, x, i) => s+x*B[i][j], 0n)), "bounded full kernel/coset bijection"); cosetPoints++;
    }
  }
  if (c.pair.length) legalPair(A, Q, t, c.pair);
  for (const trace of c.attempts) {
    const N = BigInt(trace.exact_original_norm);
    check(trace.word ? N === 6n*BigInt(d/2) : N >= 6n*BigInt(d/2)+18n, "every candidate original-shell status");
    if (trace.integer_coset_coordinates) {
      const z = big(trace.integer_coset_coordinates), P = big(trace.embedded_lattice_point), coeff = big(trace.reduced_basis_coefficients);
      const rows = control.bases[trace.basis].rows.map(big);
      same(P, T.map((_, j) => coeff.reduce((s, x, i) => s+x*rows[i][j], 0n)), "accepted nearest-plane lattice coefficients");
      same(P, E(z.map((x, i) => x-z0[i])).map(x => 3n*x), "inverse lattice point extraction");
      check(norm(z) === N && value(A, trace.word, Q) === t, "accepted exact norm/congruence"); acceptedTraces++;
    }
  }
}
let truthPairs = 0, impossible = 0, uniformDecodes = 0n, weightedDecodes = 0n;
for (const c of report.exact_census.all_cases) {
  const labels = big(c.labels), target = BigInt(c.target), fiber = words(1).filter(w => value(labels, w, 9n) === target);
  check(fiber.length === c.fiber_size, "complete original nuisance fiber truth");
  truthPairs += fiber.length >= 2;
  if (c.pair.length) { legalPair(labels, 9n, target, c.pair); censusPairs++; }
  if (c.status === "DIVISIBILITY_CERTIFIED_EMPTY_TARGET") { check(fiber.length === 0, "gcd certified emptiness"); impossible++; }
  uniformDecodes += BigInt(c.decodes); weightedDecodes += BigInt(c.decodes*fiber.length);
}
check(truthPairs === 25 && censusPairs === 25 && impossible === 56, "all small-source pair targets including nonunits");
fracEqual(report.exact_census.uniform_pair_coverage_exact, 25n, 729n, "actual uniform coverage");
fracEqual(report.exact_census.exact_source_average_informative_acceptance, 100n, 729n, "exact native pair transfer");
fracEqual(report.exact_census.exact_source_average_raw_least_trit_success, 829n, 2187n, "all-failure raw trit score");
fracEqual(report.exact_census.decode_work_uniform_average, uniformDecodes, 729n, "uniform runtime statistic");
fracEqual(report.exact_census.decode_work_Born_average, 3n*weightedDecodes, 729n, "size-biased runtime statistic");
for (const trial of report.scaling.trials) {
  const labels = big(trial.labels), q = BigInt(trial.modulus), t = BigInt(trial.target), M = trial.width;
  check(labels.length === 2*M && M === trial.root_digits-2 && q === 3n**BigInt(trial.root_digits-1), "real source scaling");
  for (const w of trial.witnesses) check(value(labels, w, q) === t, "scaling original modular witness");
  if (trial.pair.length) { legalPair(labels, q, t, trial.pair); sweepPairs++; }
  check(trial.cost.candidate_decodes <= trial.cost.decode_cap && trial.cost.rounding_steps === 2*M*trial.cost.candidate_decodes, "every decode charged");
  const sub = trial.deflated_second_witness;
  if (sub) {
    check(sub.cost.slice_calls <= 2*M && sub.cost.lll_calls <= sub.cost.slice_calls, "deflation calls/costs charged");
    for (const attempt of sub.attempts) {
      if (attempt.candidate) check(value(labels, attempt.candidate, q) === t && attempt.candidate[attempt.fixed_coordinate] === attempt.fixed_digit, "original-word coordinate deflation");
    }
    if (sub.pair.length) { legalPair(labels, q, t, sub.pair); deflatedPairs++; }
  }
}
check(!report.polynomial_pair_finder_proved && !report.new_algorithm_claim && !report.quantum_secret_given_to_attack, "claims stay blocked");
console.log(JSON.stringify({status: "independent_integer_replay_passed", localPoints, globalPoints, cosetPoints,
  acceptedTraces, censusPairs, sweepPairs, deflatedPairs, scalingTrials: report.scaling.trials.length,
  independentLLLSearch: false, asymptoticCoverageProved: false}));
