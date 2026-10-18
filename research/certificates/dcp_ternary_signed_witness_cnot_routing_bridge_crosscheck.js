#!/usr/bin/env node
"use strict";

function mod(a, m) {
  return ((a % m) + m) % m;
}

function countWitnesses(aRow, qMod) {
  const K = aRow.length;
  let binCount = 0;
  for (let m = 1; m < 1 << K; m++) {
    let s = 0;
    for (let r = 0; r < K; r++) if ((m >> r) & 1) s += aRow[r];
    if (mod(s, qMod) === 0) binCount++;
  }
  let ternCount = 0;
  const total = Math.pow(3, K);
  for (let idx = 1; idx < total; idx++) {
    let tmp = idx;
    const delta = [];
    for (let r = 0; r < K; r++) {
      const rem = tmp % 3;
      delta.push(rem === 2 ? -1 : rem);
      tmp = Math.floor(tmp / 3);
    }
    const firstNonZero = delta.find((x) => x !== 0);
    if (firstNonZero !== 1) continue;
    let s = 0;
    for (let r = 0; r < K; r++) s += delta[r] * aRow[r];
    if (mod(s, qMod) === 0) ternCount++;
  }
  return { binCount, ternCount };
}

const c5 = countWitnesses([1, 1, 1], 5);
const c8 = countWitnesses([1, 1, 1, 1], 8);

if (
  c5.binCount !== 0 ||
  c5.ternCount !== 3 ||
  c8.binCount !== 0 ||
  c8.ternCount !== 9
) {
  throw new Error("Ternary vs binary witness count mismatch");
}

console.log(JSON.stringify({ status: "OK", c5, c8 }));
