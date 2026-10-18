#!/usr/bin/env node
"use strict";

const q = 8;
const a1 = [1, 3], a2 = [2, 5], s = [3, 1];
const g1 = 0.8, g2 = 0.7;
const th1 = (2 * Math.PI * ((a1[0]*s[0] + a1[1]*s[1]) % q)) / q;
const th2 = (2 * Math.PI * ((a2[0]*s[0] + a2[1]*s[1]) % q)) / q;

const pPhiPlus = 0.25 * (1 + g1 * g2 * Math.cos(th1 + th2));
const pPhiMinus = 0.25 * (1 - g1 * g2 * Math.cos(th1 + th2));
const pPsiPlus = 0.25 * (1 + g1 * g2 * Math.cos(th1 - th2));
const pPsiMinus = 0.25 * (1 - g1 * g2 * Math.cos(th1 - th2));

if (Math.abs((pPhiPlus + pPhiMinus + pPsiPlus + pPsiMinus) - 1.0) > 1e-12) {
  throw new Error("Bell probabilities do not sum to 1");
}
// Check the FULL (a1,a2,branch,sign) law of a one-random-X-sample lift.
const modulus = 4, secret = 1, sourceGamma = 0.8, targetGamma = g1 * g2;
const ratio = targetGamma / sourceGamma;
const mod = x => ((x % modulus) + modulus) % modulus;
const joint = new Map();
for (let h = 0; h < modulus; h++) {
  for (let bit = 0; bit < 2; bit++) {
    const sourceMass = (1 + (1 - 2 * bit) * sourceGamma * Math.cos(2 * Math.PI * h * secret / modulus)) / (2 * modulus);
    for (let anchor = 0; anchor < modulus; anchor++) {
      for (let branch = 0; branch < 2; branch++) {
        const other = mod(branch === 0 ? h - anchor : anchor - h);
        for (let flip = 0; flip < 2; flip++) {
          const key = [anchor, other, branch, bit ^ flip].join(",");
          const mass = sourceMass * (1 + (1 - 2 * flip) * ratio) / (4 * modulus);
          joint.set(key, (joint.get(key) || 0) + mass);
        }
      }
    }
  }
}
let fullJointError = 0;
for (const [key, mass] of joint) {
  const [a, b, branch, bit] = key.split(",").map(Number);
  const phase = 2 * Math.PI * (branch === 0 ? a + b : a - b) * secret / modulus;
  const expected = (1 + (1 - 2 * bit) * targetGamma * Math.cos(phase)) / (4 * modulus * modulus);
  fullJointError = Math.max(fullJointError, Math.abs(mass - expected));
}
if (fullJointError > 1e-12 || joint.size !== 4 * modulus * modulus) throw new Error("Transcript mismatch");
console.log(JSON.stringify({ status: "OK", pPhiPlus, pPsiPlus, fullJointError }));
