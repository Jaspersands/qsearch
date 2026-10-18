#!/usr/bin/env node
"use strict";

function bandedPeakProb(m, k0, b) {
  const kBits = [];
  for (let l = 0; l < m; l++) {
    kBits.push((k0 >> (m - 1 - l)) & 1);
  }
  let prod = 1.0;
  for (let j = 0; j < m - b; j++) {
    let angle = 0.0;
    for (let l = j + b; l < m; l++) {
      if (kBits[l]) angle += Math.PI * Math.pow(2, j - 1 - l);
    }
    prod *= Math.pow(Math.cos(angle), 2);
  }
  return prod;
}

const pHalfB1 = bandedPeakProb(4, 8, 1);
const pOddB1 = bandedPeakProb(4, 1, 1);
const pOddB4 = bandedPeakProb(4, 1, 4);

if (
  Math.abs(pHalfB1 - 1.0) > 1e-12 ||
  pOddB1 > 0.42 ||
  pOddB1 < 0.40 ||
  Math.abs(pOddB4 - 1.0) > 1e-12
) {
  throw new Error("Banded QFT peak formula mismatch");
}

console.log(
  JSON.stringify({
    status: "OK",
    pHalfB1,
    pOddB1,
    pOddB4,
  })
);
