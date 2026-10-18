#!/usr/bin/env node
"use strict";

const thetas = [Math.PI / 2, Math.PI / 4, (3 * Math.PI) / 4];
let sumProb = 0;
for (let mask = 0; mask < 8; mask++) {
  let p = 1.0;
  for (let j = 0; j < 3; j++) {
    const zj = (mask >> j) & 1;
    const c = Math.cos(0.5 * (thetas[j] - Math.PI * zj));
    p *= c * c;
  }
  sumProb += p;
}
const p0 = thetas.reduce((acc, th) => acc * Math.pow(Math.cos(0.5 * th), 2), 1.0);
if (Math.abs(sumProb - 1.0) > 1e-12) {
  throw new Error("Hadamard product distribution does not sum to 1");
}
console.log(JSON.stringify({ status: "OK", sumProb, tvFromZero: 1.0 - p0 }));
