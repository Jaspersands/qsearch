#!/usr/bin/env node
"use strict";

function prodLaw(thetas, K) {
  const m = thetas.length;
  let p = 1.0;
  for (let j = 0; j < m; j++) {
    const ang = 0.5 * thetas[j] - (Math.PI * K) / (1 << (m - j));
    const c = Math.cos(ang);
    p *= c * c;
  }
  return p;
}

const k0 = 5;
const dyadic = [0, 1, 2].map((j) => (2 * Math.PI * (1 << j) * k0) / 8);
const pPeak = prodLaw(dyadic, k0);
if (Math.abs(pPeak - 1.0) > 1e-12) {
  throw new Error("Dyadic peak mismatch");
}
console.log(JSON.stringify({ status: "OK", pPeak }));
