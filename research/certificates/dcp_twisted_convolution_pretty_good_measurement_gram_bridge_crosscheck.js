#!/usr/bin/env node
"use strict";

function pgmSuccess(A, q) {
  const m = A.length;
  const counts = new Map();
  for (let mask = 0; mask < (1 << m); mask++) {
    let s = 0;
    for (let j = 0; j < m; j++) {
      if ((mask >> j) & 1) s = (s + A[j]) % q;
    }
    counts.set(s, (counts.get(s) || 0) + 1);
  }
  let sumSqrt = 0;
  for (const c of counts.values()) {
    sumSqrt += Math.sqrt(c);
  }
  return (sumSqrt * sumSqrt) / (q * (1 << m));
}

const pBij = pgmSuccess([1, 2], 4);
const pCol = pgmSuccess([2, 2], 4);
const pSub = pgmSuccess([1, 3], 8);
if (Math.abs(pBij - 1.0) > 1e-12 || Math.abs(pCol - 0.5) > 1e-12 || Math.abs(pSub - 0.5) > 1e-12) {
  throw new Error("PGM formula mismatch");
}
console.log(JSON.stringify({ status: "OK", pBij, pCol, pSub }));
