#!/usr/bin/env node
"use strict";

function mod(a, m) {
  return ((a % m) + m) % m;
}

function pgmClosedForm(aRow, qMod) {
  const K = aRow.length;
  const occ = new Array(qMod).fill(0);
  for (let m = 0; m < 1 << K; m++) {
    let s = 0;
    for (let r = 0; r < K; r++) if ((m >> r) & 1) s += aRow[r];
    occ[mod(s, qMod)]++;
  }
  let sqrtSum = 0;
  for (let y = 0; y < qMod; y++) sqrtSum += Math.sqrt(occ[y]);
  return (sqrtSum * sqrtSum) / ((1 << K) * qMod);
}

const pFlat = pgmClosedForm([1, 2, 4], 8);
const pHalf = pgmClosedForm([1, 2], 8);
const pColl = pgmClosedForm([1, 1, 2], 8);

if (
  Math.abs(pFlat - 1.0) > 1e-12 ||
  Math.abs(pHalf - 0.5) > 1e-12 ||
  pColl >= 5.0 / 8.0
) {
  throw new Error("PGM square-root occupancy law mismatch");
}

console.log(JSON.stringify({ status: "OK", pFlat, pHalf, pColl }));
