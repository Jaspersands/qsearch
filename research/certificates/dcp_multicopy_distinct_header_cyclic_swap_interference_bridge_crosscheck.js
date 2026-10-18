#!/usr/bin/env node
"use strict";

function cMul(a, b) {
  return [a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]];
}

function cAdd(a, b) {
  return [a[0] + b[0], a[1] + b[1]];
}

function rho(theta, gamma) {
  const c = 0.5 * gamma * Math.cos(theta);
  const s = 0.5 * gamma * Math.sin(theta);
  return [
    [
      [0.5, 0],
      [c, -s],
    ],
    [
      [c, s],
      [0.5, 0],
    ],
  ];
}

function matMul2x2(A, B) {
  const out = [
    [
      [0, 0],
      [0, 0],
    ],
    [
      [0, 0],
      [0, 0],
    ],
  ];
  for (let i = 0; i < 2; i++) {
    for (let j = 0; j < 2; j++) {
      out[i][j] = cAdd(cMul(A[i][0], B[0][j]), cMul(A[i][1], B[1][j]));
    }
  }
  return out;
}

// Verify r=4 cyclic shift trace against closed-form even-flip formula (m=1 pairs + m=2 4-tuple)
const th = [0.15, 0.85, 1.75, 2.65];
const gm = [0.9, 0.85, 0.8, 0.75];

let prod = rho(th[0], gm[0]);
for (let j = 1; j < 4; j++) {
  prod = matMul2x2(prod, rho(th[j], gm[j]));
}
const traceRe = prod[0][0][0] + prod[1][1][0];
const traceIm = prod[0][0][1] + prod[1][1][1];

let cf = 1.0;
for (let j = 0; j < 4; j++) {
  for (let k = j + 1; k < 4; k++) {
    cf += gm[j] * gm[k] * Math.cos(th[j] - th[k]);
  }
}
cf +=
  gm[0] *
  gm[1] *
  gm[2] *
  gm[3] *
  Math.cos(th[0] - th[1] + th[2] - th[3]);
cf /= 8.0;

if (Math.abs(traceRe - cf) > 1e-12 || Math.abs(traceIm) > 1e-12) {
  throw new Error("Cyclic shift even-flip formula mismatch");
}

console.log(
  JSON.stringify({
    status: "OK",
    r4TraceReal: traceRe,
    r4ClosedForm: cf,
  })
);
