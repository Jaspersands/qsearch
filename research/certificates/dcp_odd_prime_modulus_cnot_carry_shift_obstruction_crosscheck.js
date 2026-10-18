#!/usr/bin/env node
"use strict";

function mod(a, m) {
  return ((a % m) + m) % m;
}

function zeroFrac(aRow, pMod) {
  const K = aRow.length;
  let hits = 0;
  for (let mask = 0; mask < 1 << K; mask++) {
    let acc = 0;
    for (let r = 0; r < K; r++) {
      const bit = (mask >> r) & 1;
      acc += (1 - 2 * bit) * aRow[r];
    }
    if (mod(acc, pMod) === 0) hits++;
  }
  return hits / (1 << K);
}

const fMin2 = zeroFrac([1, 4], 5);
const fMin3 = zeroFrac([1, 2, 4], 7);
const fComp4 = zeroFrac([1, 4, 2, 3], 5);

if (fMin2 !== 0.5 || fMin3 !== 0.25 || fComp4 !== 0.25) {
  throw new Error("Odd prime zero-sum fraction mismatch");
}

console.log(
  JSON.stringify({
    status: "OK",
    fMin2,
    fMin3,
    fComp4,
  })
);
