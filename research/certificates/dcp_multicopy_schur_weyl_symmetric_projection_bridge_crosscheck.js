#!/usr/bin/env node
"use strict";

function comb(n, k) {
  if (k < 0 || k > n) return 0;
  let res = 1;
  for (let i = 1; i <= k; i++) {
    res = (res * (n - i + 1)) / i;
  }
  return res;
}

function symProbClosedForm(r, gamma) {
  const pPlus = 0.5 * (1 + gamma);
  const pMinus = 0.5 * (1 - gamma);
  let sum = 0;
  for (let k = 0; k <= r; k++) {
    sum += Math.pow(pPlus, r - k) * Math.pow(pMinus, k);
  }
  return sum;
}

function popcount(x) {
  let c = 0;
  while (x > 0) {
    c += x & 1;
    x >>= 1;
  }
  return c;
}

// Verify explicit Dicke trace on rho(theta, gamma)^{\otimes r} matches closed form and is independent of theta
function symProbExplicit(r, theta, gamma) {
  const dim = 1 << r;
  let total = 0;
  for (let w = 0; w <= r; w++) {
    const norm2 = comb(r, w);
    let blockSum = 0;
    for (let x = 0; x < dim; x++) {
      if (popcount(x) !== w) continue;
      for (let y = 0; y < dim; y++) {
        if (popcount(y) !== w) continue;
        const d = popcount(x ^ y);
        // Since wt(x) == wt(y) == w, phase e^{-i(wt(y)-wt(x))*theta} == 1!
        blockSum += Math.pow(gamma, d) / Math.pow(2, r);
      }
    }
    total += blockSum / norm2;
  }
  return total;
}

for (const r of [2, 3, 4]) {
  for (const gamma of [0.0, 0.6, 0.8, 1.0]) {
    const cf = symProbClosedForm(r, gamma);
    const ex0 = symProbExplicit(r, 0.0, gamma);
    const ex1 = symProbExplicit(r, 1.234, gamma);
    if (Math.abs(cf - ex0) > 1e-12 || Math.abs(cf - ex1) > 1e-12) {
      throw new Error("Symmetric projection probability mismatch");
    }
  }
}

// Verify r=2 match with (3 + gamma^2)/4
const g = 0.8;
if (Math.abs(symProbClosedForm(2, g) - (3 + g * g) / 4) > 1e-12) {
  throw new Error("r=2 singlet complement mismatch");
}

console.log(
  JSON.stringify({
    status: "OK",
    r2_gamma_0_8: symProbClosedForm(2, 0.8),
    r3_gamma_0_75: symProbClosedForm(3, 0.75),
  })
);
