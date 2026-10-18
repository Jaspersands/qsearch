#!/usr/bin/env node
"use strict";

const B = [
  [1, 0, 1, 2],
  [0, 1, 1, 1],
];
const q = 3;
const d = 2;
const n = 4;
const gamma = 0.25;

const Aw = Array(n + 1).fill(0);
for (let u0 = 0; u0 < q; u0++) {
  for (let u1 = 0; u1 < q; u1++) {
    let wt = 0;
    for (let c = 0; c < n; c++) {
      const v = (u0 * B[0][c] + u1 * B[1][c]) % q;
      if (v !== 0) wt++;
    }
    Aw[wt]++;
  }
}

const Aperp = Array(n + 1).fill(0);
for (let z0 = 0; z0 < q; z0++) {
  for (let z1 = 0; z1 < q; z1++) {
    for (let z2 = 0; z2 < q; z2++) {
      for (let z3 = 0; z3 < q; z3++) {
        const z = [z0, z1, z2, z3];
        const s0 = (B[0][0]*z0 + B[0][1]*z1 + B[0][2]*z2 + B[0][3]*z3) % q;
        const s1 = (B[1][0]*z0 + B[1][1]*z1 + B[1][2]*z2 + B[1][3]*z3) % q;
        if (s0 === 0 && s1 === 0) {
          const wt = z.filter((x) => x !== 0).length;
          Aperp[wt]++;
        }
      }
    }
  }
}

const p0 = 1.0 - gamma * (q - 1) / q;
const perr = gamma / q;
let pDual = 0;
let pPrimal = 0;
for (let k = 0; k <= n; k++) {
  pDual += Aperp[k] * Math.pow(p0, n - k) * Math.pow(perr, k);
  pPrimal += Aw[k] * Math.pow(1.0 - gamma, k) / Math.pow(q, d);
}
if (Math.abs(pDual - pPrimal) > 1e-12) {
  throw new Error("MacWilliams noisy QFT bridge mismatch");
}
console.log(JSON.stringify({ status: "OK", pDual, pPrimal }));
