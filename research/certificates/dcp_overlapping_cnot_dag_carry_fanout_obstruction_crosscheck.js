#!/usr/bin/env node
"use strict";

function mod(a, m) {
  return ((a % m) + m) % m;
}

function directCrossCount(A, V, q) {
  const k = V.length, m = V[0].length;
  let count = 0;
  for (let anchor = 0; anchor < 2**k; anchor++) {
    for (let u = 0; u < 2**m; u++) {
      let direct = 0, linear = 0;
      for (let r = 0; r < k; r++) {
        const x = (anchor >> r) & 1;
        let active = 0;
        for (let j = 0; j < m; j++) active += V[r][j]*((u >> j)&1);
        direct += A[r]*(x ^ (active&1));
        linear += A[r]*(x+(1-2*x)*active);
      }
      if (mod(direct-linear, q) !== 0) count++;
    }
  }
  return count;
}
const nonZeroCross = directCrossCount([3,1,5], [[1,0],[1,1],[0,1]], 8);
if (nonZeroCross !== 8) {
  throw new Error("Expected 8 non-zero quadratic cross-term evaluations");
}
const cancellationCross = directCrossCount([1,1,3,5], [[1,1],[1,1],[1,0],[0,1]], 4);
if (cancellationCross !== 0) throw new Error("Aggregate cancellation lost");
console.log(JSON.stringify({status: "OK", nonZeroCross, cancellationCross,
  oldTermwiseNecessityRetracted: true}));
