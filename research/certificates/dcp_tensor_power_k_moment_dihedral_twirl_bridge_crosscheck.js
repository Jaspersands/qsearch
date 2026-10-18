#!/usr/bin/env node
"use strict";

function mod(a, m) {
  return ((a % m) + m) % m;
}

function ternaryFrobSq(aCols, qMod, gammas) {
  const r = aCols.length;
  let acc = 0;
  const total = Math.pow(3, r);
  for (let idx = 1; idx < total; idx++) {
    let tmp = idx;
    const delta = [];
    for (let j = 0; j < r; j++) {
      const rem = tmp % 3;
      delta.push(rem === 2 ? -1 : rem);
      tmp = Math.floor(tmp / 3);
    }
    let dot = 0;
    for (let j = 0; j < r; j++) dot += delta[j] * aCols[j];
    if (mod(dot, qMod) === 0) {
      let term = 1.0;
      for (let j = 0; j < r; j++) {
        if (delta[j] !== 0) term *= 0.5 * gammas[j] * gammas[j];
      }
      acc += term;
    }
  }
  return acc / Math.pow(2, r);
}

const fFree = ternaryFrobSq([1, 3], 8, [0.85, 0.75]);
const fColl = ternaryFrobSq([1, 2, 3], 8, [0.9, 0.8, 0.7]);

const g3 = [0.8, 0.7, 0.6];
let ensAcc = 0;
for (let a0 = 0; a0 < 4; a0++) {
  for (let a1 = 0; a1 < 4; a1++) {
    for (let a2 = 0; a2 < 4; a2++) {
      ensAcc += ternaryFrobSq([a0, a1, a2], 4, g3) / 64.0;
    }
  }
}
const cfEns =
  ((1 + 0.64) * (1 + 0.49) * (1 + 0.36) - 1.0) / (8.0 * 4.0);

if (
  Math.abs(fFree) > 1e-12 ||
  fColl < 0.005 ||
  Math.abs(ensAcc - cfEns) > 1e-12
) {
  throw new Error("Ternary twirl Frobenius identity mismatch");
}

console.log(
  JSON.stringify({
    status: "OK",
    collisionFreeFrobSq: fFree,
    activeCollisionFrobSq: fColl,
    ensembleMeanFrobSq: ensAcc,
  })
);
