#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");
const assert = require("assert/strict");
const near = (a, b) => assert(Number.isFinite(a) && Math.abs(a - b) < 1e-10, `${a} != ${b}`);
const fraction = s => Number(s.split("/")[0]) / Number(s.split("/")[1]);
const mod = (x, q) => ((x % q) + q) % q;
const dot = (a, b) => a.reduce((s, x, i) => s + x * b[i], 0);
const weight = a => a.filter(x => x !== 0).length;
function vectors(q, n) {
  return Array.from({length: q ** n}, (_, k) => {
    const a = Array(n);
    for (let j = n - 1; j >= 0; j--) { a[j] = k % q; k = Math.floor(k / q); }
    return a;
  });
}
function geometry(c) {
  const {q, n, generator_matrix: M} = c;
  assert(Number.isInteger(q) && q >= 2 && q <= 127);
  for (let p = 2; p*p <= q; p++) assert(q % p !== 0);
  const V = vectors(q, n), B = new Set();
  for (const a of vectors(q, M.length)) B.add(JSON.stringify(Array.from({length: n}, (_, j) => mod(M.reduce((s, r, i) => s + a[i]*r[j], 0), q))));
  assert.equal(B.size, q ** M.length);
  const dual = V.filter(u => M.every(r => mod(dot(r, u), q) === 0));
  return {V, B, dual};
}

const ROOT = path.resolve(__dirname, "..", "..");
const ARTIFACT_PATH = path.join(
  ROOT,
  "research",
  "reductions",
  "planted_qary_noisy_parity_check_likelihood_bridge.json"
);

function gcdBigInt(a, b) {
  a = a < 0n ? -a : a;
  b = b < 0n ? -b : b;
  while (b !== 0n) {
    const t = a % b;
    a = b;
    b = t;
  }
  return a;
}

function fracStr(num, den) {
  if (den < 0n) {
    num = -num;
    den = -den;
  }
  const g = gcdBigInt(num, den);
  return `${num / g}/${den / g}`;
}

function absBigInt(x) {
  return x < 0n ? -x : x;
}

function verifyCase(c) {
  const {V, B, dual} = geometry(c);
  assert.equal(c.d, c.generator_matrix.length);
  assert.equal(c.R, new Set(c.window).size);
  const gamma = fraction(c.gamma_exact), p0 = 1 - (c.q-1)*gamma/c.q, p1 = gamma/c.q;
  const px = V.map(x => [...B].reduce((s, b) => {
    const v = JSON.parse(b), w = weight(x.map((a, i) => mod(a-v[i], c.q)));
    return s + p0**(c.n-w)*p1**w/B.size;
  }, 0));
  let maxBias = 0;
  for (const u of V) {
    let real = 0, imag = 0, accept = 0;
    V.forEach((x, i) => {
      const d = mod(dot(u, x), c.q), theta = 2*Math.PI*d/c.q;
      real += px[i]*Math.cos(theta); imag += px[i]*Math.sin(theta);
      if (c.window.includes(d)) accept += px[i];
    });
    const inDual = dual.some(v => JSON.stringify(v) === JSON.stringify(u));
    near(real, inDual ? (1-gamma)**weight(u) : 0); near(imag, 0);
    near(accept, c.R/c.q + (inDual ? (1-gamma)**weight(u)*((c.window.includes(0) ? 1 : 0)-c.R/c.q) : 0));
    if (weight(u)) maxBias = Math.max(maxBias, Math.abs(accept-c.R/c.q));
  }
  near(maxBias, fraction(c.max_nonzero_probe_bias_exact));
  const nonzeroDual = dual.filter(u => weight(u));
  assert.equal(c.dual_minimum_distance_d_perp, nonzeroDual.length ? Math.min(...nonzeroDual.map(weight)) : null);
  const q = BigInt(c.q);
  const R = BigInt(c.R);
  const zeroInWindow = c.zero_in_window;
  const [gNumStr, gDenStr] = c.gamma_exact.split("/");
  const gNum = BigInt(gNumStr);
  const gDen = BigInt(gDenStr);

  const omgNum = gDen - gNum;
  const omgDen = gDen;

  if (c.max_character_residual > 1e-12) {
    throw new Error(`Case ${c.case_id}: max_character_residual > 1e-12`);
  }
  if (!c.off_dual_invariance_holds || !c.on_dual_weight_law_holds) {
    throw new Error(`Case ${c.case_id}: Theorem 2 invariance/weight law failed`);
  }

  for (const s of c.dual_weight_strata) {
    const w = BigInt(s.hamming_weight);
    const charNum = omgNum ** w;
    const charDen = omgDen ** w;
    const expectedCharStr = fracStr(charNum, charDen);
    if (s.character_expectation_exact !== expectedCharStr) {
      throw new Error(
        `Case ${c.case_id}, w=${w}: character_expectation_exact mismatch`
      );
    }

    // p_W = R/q + (1-gamma)^w * (1_{0 in W} - R/q)
    const diffNum = (zeroInWindow ? q : 0n) - R;
    const accNum = R * charDen + charNum * diffNum;
    const accDen = q * charDen;
    const expectedAccStr = fracStr(accNum, accDen);
    if (s.window_acceptance_prob_exact !== expectedAccStr) {
      throw new Error(
        `Case ${c.case_id}, w=${w}: window_acceptance_prob_exact mismatch`
      );
    }

    const biasNum = absBigInt(charNum * diffNum);
    const biasDen = q * charDen;
    const expectedBiasStr = fracStr(biasNum, biasDen);
    if (s.distinguishing_bias_exact !== expectedBiasStr) {
      throw new Error(
        `Case ${c.case_id}, w=${w}: distinguishing_bias_exact mismatch`
      );
    }
  }

  const dPerp = BigInt(c.dual_minimum_distance_d_perp);
  const diffNum = absBigInt((zeroInWindow ? q : 0n) - R);
  const maxBiasNum = (omgNum ** dPerp) * diffNum;
  const maxBiasDen = q * (omgDen ** dPerp);
  const expectedMaxBiasStr = fracStr(maxBiasNum, maxBiasDen);
  if (c.max_nonzero_probe_bias_exact !== expectedMaxBiasStr) {
    throw new Error(`Case ${c.case_id}: max_nonzero_probe_bias_exact mismatch`);
  }
}

function verifyQuantum(c) {
  const {q, n} = c, {V, B, dual} = geometry(c), N = V.length;
  assert(N <= 128);
  const gamma = fraction(c.gamma_exact), p0 = 1-(q-1)*gamma/q, p1 = gamma/q;
  const weights = V.map(e => p0**(n-weight(e))*p1**weight(e));
  assert.deepEqual(c.vector_order, V); assert.deepEqual(c.dual_vectors, dual);
  assert.equal(c.enumerated_density_dimension, N);
  assert.equal(c.classical_samples_determine_quantum_Fourier_readout, false);
  assert.equal(c.coherent_state_preparation_from_classical_samples_supplied, false);
  assert.equal(c.scalable_state_preparation, false);
  assert.equal(c.same_computational_marginal_for_all_three_sources, true);
  const rho = Array.from({length: N}, () => Array(N).fill(0));
  const translatedSupports = V.map(e => V.map((x, i) => B.has(JSON.stringify(x.map((a, j) => mod(a-e[j], q)))) ? i : -1).filter(i => i >= 0));
  for (let e = 0; e < N; e++) for (const x of translatedSupports[e]) for (const y of translatedSupports[e]) rho[x][y] += weights[e]/B.size;
  const actualX = Array(N).fill(0), actualXZ = Array(N).fill(0);
  // Actual Born amplitudes after X^e and Z^f, not the disputed convolution.
  for (let e = 0; e < N; e++) for (let u = 0; u < N; u++) for (let f = 0; f < N; f++) {
    let re = 0, im = 0;
    for (const x of translatedSupports[e]) {
      const phase = 2*Math.PI*dot(V[u].map((a, j) => a+V[f][j]), V[x])/q;
      re += Math.cos(phase); im += Math.sin(phase);
    }
    const born = (re*re+im*im)/(N*B.size);
    actualXZ[u] += weights[e]*weights[f]*born;
    if (f === 0) actualX[u] += weights[e]*born;
  }
  const expectedX = V.map(u => dual.some(v => JSON.stringify(u) === JSON.stringify(v)) ? 1/dual.length : 0);
  const expectedXZ = V.map(u => dual.reduce((s, v) => {
    const w = weight(u.map((a, j) => mod(a-v[j], q)));
    return s + p0**(n-w)*p1**w/dual.length;
  }, 0));
  const modes = ["coherent_random_translation", "coherent_translation_and_phase_noise", "incoherent_classical_samples"];
  const targets = [expectedX, expectedXZ, Array(N).fill(1/N)], borns = [actualX, actualXZ, Array(N).fill(1/N)];
  modes.forEach((name, mode) => {
    const m = c.modes[name]; assert.equal(m.Born_probabilities.length, N); assert.equal(m.target_probabilities_exact.length, N);
    let outside = 0, purity = 0, residual = 0;
    for (let u = 0; u < N; u++) {
      near(m.Born_probabilities[u], borns[mode][u]); near(fraction(m.target_probabilities_exact[u]), targets[mode][u]);
      residual = Math.max(residual, Math.abs(m.Born_probabilities[u]-targets[mode][u]));
      if (!dual.some(v => JSON.stringify(v) === JSON.stringify(V[u]))) outside += targets[mode][u];
      for (let x = 0; x < N; x++) {
        const d = weight(V[u].map((a, j) => mod(a-V[x][j], q)));
        const entry = mode === 0 ? rho[u][x] : mode === 1 ? rho[u][x]*(1-gamma)**d : u === x ? rho[u][u] : 0;
        purity += entry*entry;
      }
    }
    near(m.purity, purity); near(fraction(m.outside_dual_mass_exact), outside); near(m.max_Born_residual, residual);
  });
  assert.equal(c.translation_only_equals_claimed_phase_convolution, gamma === 0);
  assert.equal(c.all_physical_laws_verified, true);
}

function main() {
  const raw = fs.readFileSync(process.argv[2] || ARTIFACT_PATH, "utf8");
  const payload = JSON.parse(raw);
  assert.equal(payload.schema_version, "2026-10-16.planted-qary-noisy-parity-check-likelihood-bridge.v2");
  assert.equal(payload.summary.translation_noise_convolution_claim_retracted, true);
  assert.equal(payload.guardrails.coherent_source_from_classical_samples_supplied, false);
  assert.equal(payload.guardrails.natural_problem_reduction_noise_certified, false);
  assert.equal(payload.guardrails.finite_checks_are_asymptotic_proof, false);
  assert.equal(payload.quantum_source_controls.length, 9);
  assert.equal(payload.summary.quantum_source_control_count, 9);
  for (const c of payload.quantum_source_controls) verifyQuantum(c);

  if (
    payload.status !== "VERIFIED_EXACT_NOISY_PARITY_CHECK_WEIGHT_POWER_LAWS"
  ) {
    throw new Error(`Unexpected status: ${payload.status}`);
  }
  if (
    payload.guardrails.accepted_speedup_candidate !== false ||
    payload.guardrails.new_active_negative_result_created !== false ||
    payload.guardrails.novelty_claim !== false
  ) {
    throw new Error("Guardrail violation");
  }

  for (const c of payload.cases) {
    verifyCase(c);
  }

  console.log(
    JSON.stringify(
      {
        status: "CROSSCHECK_PASSED",
        case_count: payload.cases.length,
        quantum_source_control_count: payload.quantum_source_controls.length,
        certificate_sha256: payload.certificate_sha256,
      },
      null,
      2
    )
  );
}

main();
