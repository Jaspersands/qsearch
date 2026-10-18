#!/usr/bin/env node
"use strict";

function mod(a, m) {
  return ((a % m) + m) % m;
}

const cands = [2, 6];
let unrect = 0;
let rect = 0;
for (const a1 of cands) {
  for (const a2 of cands) {
    if (mod(a1 + a2, 8) === 0) unrect++;
    const a2Rect = a1 === a2 ? mod(-a2, 8) : a2;
    if (mod(a1 + a2Rect, 8) === 0) rect++;
  }
}

if (unrect !== 2 || rect !== 4) {
  throw new Error("Pauli-X sign rectification mismatch");
}

console.log(
  JSON.stringify({
    status: "OK",
    unrectifiedFraction: unrect / 4,
    rectifiedFraction: rect / 4,
  })
);
