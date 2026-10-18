#!/usr/bin/env node
"use strict";

function closedFormPairs(M, B) {
  return 0.5 * M - 0.25 * B * (1.0 - Math.pow(1.0 - 2.0 / B, M));
}

const M = 6, B = 4;
const total = Math.pow(B, M);
let sumPairs = 0;
for (let x = 0; x < total; x++) {
  let tmp = x;
  const counts = [0, 0, 0, 0];
  for (let i = 0; i < M; i++) {
    counts[tmp % B]++;
    tmp = Math.floor(tmp / B);
  }
  for (let b = 0; b < B; b++) {
    sumPairs += Math.floor(counts[b] / 2);
  }
}
const exh = sumPairs / total;
const cf = closedFormPairs(M, B);
if (Math.abs(exh - cf) > 1e-12) {
  throw new Error("Bucket pairing identity mismatch");
}
// Independent full enumeration, not f(E[M]) between rounds.
function poolLaw(m, b) {
  const counts = new Map();
  for (let x = 0; x < Math.pow(b, m); x++) {
    let tmp = x;
    const occupancy = Array(b).fill(0);
    for (let i = 0; i < m; i++) {
      occupancy[tmp % b]++;
      tmp = Math.floor(tmp / b);
    }
    const pairs = occupancy.reduce((sum, c) => sum + Math.floor(c / 2), 0);
    counts.set(pairs, (counts.get(pairs) || 0) + 1 / Math.pow(b, m));
  }
  return counts;
}
function twoLayerMean(m, b1, b2) {
  let mean = 0;
  for (const [first, p1] of poolLaw(m, b1)) {
    for (const [second, p2] of poolLaw(first, b2)) mean += second * p1 * p2;
  }
  return mean;
}
const smallCounterexampleMean = twoLayerMean(2, 2, 2);
const sixStateMean = twoLayerMean(6, 3, 2);
if (smallCounterexampleMean !== 0) throw new Error("Extinct pool was resurrected");
console.log(JSON.stringify({ status: "OK", exh, cf, smallCounterexampleMean, sixStateMean }));
