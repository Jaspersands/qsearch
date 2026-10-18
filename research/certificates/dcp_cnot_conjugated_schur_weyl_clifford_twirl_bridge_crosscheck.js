#!/usr/bin/env node
"use strict";

function popcount(x) {
  let c = 0;
  while (x > 0) {
    c += x & 1;
    x >>= 1;
  }
  return c;
}

function wStar(x, r) {
  const x0 = (x >> (r - 1)) & 1;
  const mapped = x0 === 0 ? x : x ^ ((1 << (r - 1)) - 1);
  return popcount(mapped);
}

for (const r of [2, 3, 4, 5]) {
  const dim = 1 << r;
  const allOnes = dim - 1;
  for (let x = 0; x < dim; x++) {
    const x0 = (x >> (r - 1)) & 1;
    const wx = wStar(x, r);
    const wBar = wStar(x ^ allOnes, r);
    if (wBar !== wx + (1 - 2 * x0)) {
      throw new Error("Complement weight shift mismatch");
    }
    for (let y = 0; y < dim; y++) {
      if (wStar(y, r) === wx) {
        const dist = popcount(x ^ y);
        if (dist >= r) {
          throw new Error("Degree-r harmonic not excluded");
        }
        if (r % 2 === 1 && dist % 2 !== 0) {
          throw new Error("Odd-r coupled distance not even");
        }
      }
    }
  }
}

const t0 = 0.35,
  t1 = 1.15,
  t2 = 2.25;
const g0 = 0.9,
  g1 = 0.8,
  g2 = 0.7;
const cf =
  0.5 +
  (g1 * g2 * Math.cos(t1 - t2) +
    g0 * Math.cos(t0) * (g1 * Math.cos(t1) + g2 * Math.cos(t2))) /
    6.0;

console.log(
  JSON.stringify({
    status: "OK",
    r3ClosedFormProb: cf,
  })
);
