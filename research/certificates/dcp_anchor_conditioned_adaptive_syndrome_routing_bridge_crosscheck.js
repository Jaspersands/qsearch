#!/usr/bin/env node
"use strict";

function mod(a, m) {
  return ((a % m) + m) % m;
}

function effCol(aRow, vCol, x0, qMod) {
  let acc = 0;
  for (let r = 0; r < vCol.length; r++) {
    if (vCol[r]) {
      const sign = 1 - 2 * x0[r];
      acc += sign * aRow[r];
    }
  }
  return mod(acc, qMod);
}

// 1. Verify coset-gauge sign equivariance mod 8 and mod 4 coset invariance on A = [1, 3, 5, 7], V = [[1,0],[1,0],[0,1],[0,1]]
const aRow = [1, 3, 5, 7];
const vCols = [
  [1, 1, 0, 0],
  [0, 0, 1, 1],
];
const nonPivots = [1, 3];
const qMod = 8;

let blindHits = 0;
let selectHits = 0;
let adaptHits = 0;

for (let synMask = 0; synMask < 4; synMask++) {
  const tildeY = [0, synMask & 1, 0, (synMask >> 1) & 1];
  const baseCols = [
    effCol(aRow, vCols[0], tildeY, qMod),
    effCol(aRow, vCols[1], tildeY, qMod),
  ];
  const b0 = Math.floor(mod(baseCols[0], 4) / 2);
  const b1 = Math.floor(mod(baseCols[1], 4) / 2);

  if (mod(baseCols[0] + baseCols[1], 4) === 0) blindHits++;
  if (b0 === 0 || b1 === 0) selectHits++;

  let wAdapt = null;
  if (b0 === 0) wAdapt = [1, 0];
  else if (b1 === 0) wAdapt = [0, 1];
  else wAdapt = [1, 1];

  // Check all 4 coset representatives wCoset in {0,1}^2
  for (let wMask = 0; wMask < 4; wMask++) {
    const w0 = wMask & 1;
    const w1 = (wMask >> 1) & 1;
    const x0 = [
      tildeY[0] ^ w0,
      tildeY[1] ^ w0,
      tildeY[2] ^ w1,
      tildeY[3] ^ w1,
    ];
    const c0 = effCol(aRow, vCols[0], x0, qMod);
    const c1 = effCol(aRow, vCols[1], x0, qMod);
    const exp0 = mod((w0 ? -1 : 1) * baseCols[0], qMod);
    const exp1 = mod((w1 ? -1 : 1) * baseCols[1], qMod);
    if (c0 !== exp0 || c1 !== exp1) {
      throw new Error("Coset sign equivariance failed");
    }
    if (mod(c0, 4) !== mod(baseCols[0], 4) || mod(c1, 4) !== mod(baseCols[1], 4)) {
      throw new Error("Mod-4 coset invariance failed");
    }
    const routed = mod(wAdapt[0] * c0 + wAdapt[1] * c1, 4);
    if (routed !== 0) {
      throw new Error("Adaptive routing failed mod 4");
    }
  }
  adaptHits++;
}

if (blindHits !== 2 || selectHits !== 3 || adaptHits !== 4) {
  throw new Error("Unexpected routing fractions");
}

console.log(
  JSON.stringify({
    status: "OK",
    blindFraction: blindHits / 4,
    selectFraction: selectHits / 4,
    adaptiveFraction: adaptHits / 4,
  })
);
