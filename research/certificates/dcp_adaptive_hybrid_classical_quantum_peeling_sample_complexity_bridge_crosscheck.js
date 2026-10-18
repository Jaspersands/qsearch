#!/usr/bin/env node
"use strict";

function mod(a, m) {
  return ((a % m) + m) % m;
}

let hits = 0;
for (let mask = 0; mask < 8; mask++) {
  let s = 0;
  for (let r = 0; r < 3; r++) {
    const bit = (mask >> r) & 1;
    s += (1 - 2 * bit) * 1;
  }
  const res = mod(s, 8);
  if (res === 3 || res === 5) hits++;
}
const pMatch = hits / 8;
if (Math.abs(pMatch - 0.25) > 1e-12) {
  throw new Error("Weight-3 pMatch mismatch");
}
// Independent X parity on |+i> tensor |+i> is zero, not cos(pi)=-1.
const productX = Math.cos(Math.PI/2)**2;
const cosineSum = Math.cos(Math.PI);
if (Math.abs(productX) > 1e-14 || Math.abs(cosineSum+1) > 1e-14) {
  throw new Error("Native classical-bias counterexample failed");
}
// Actual three-outcome erasure law, parameterized by target cosine mu at0.
const gamma = (4/5)**3;
const masses = [pMatch/2, pMatch/2, 1-pMatch];
const derivatives = [pMatch*gamma/2, -pMatch*gamma/2, 0];
const fisher = masses.reduce((s, p, i) => s+derivatives[i]**2/p, 0);
if (Math.abs(fisher-pMatch*gamma**2) > 1e-14) throw new Error("Flagged Fisher law failed");
console.log(JSON.stringify({status:"OK", pMatch, productX, cosineSum,
  flaggedLocalFisher:fisher, flaggedPenalty:1/pMatch, fairCoinPenalty:1/pMatch**2,
  classicalDominanceRetracted:true}));
