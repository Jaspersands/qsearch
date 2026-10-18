#!/usr/bin/env node
"use strict";

function cfMeanMPair(n, K) {
  const twoN = Math.pow(2, n);
  const base = 1.0 - Math.pow(2, 1 - n);
  return (
    0.5 * K +
    K / (2.0 * twoN) -
    ((twoN - 1.0) / 4.0) * (1.0 - Math.pow(base, K))
  );
}

const m14 = cfMeanMPair(1, 4);
const m24 = cfMeanMPair(2, 4);

if (Math.abs(m14 - 2.75) > 1e-12 || Math.abs(m24 - 115.0 / 64.0) > 1e-12) {
  throw new Error("Bucket pair expectation mismatch");
}

console.log(
  JSON.stringify({
    status: "OK",
    n1K4Mean: m14,
    n2K4Mean: m24,
  })
);
