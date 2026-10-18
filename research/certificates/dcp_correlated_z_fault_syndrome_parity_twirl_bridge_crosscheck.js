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

function walshParity(dist) {
  let acc = 0;
  for (let e = 0; e < 8; e++) {
    const sign = popcount(e) % 2 === 1 ? -1 : 1;
    acc += dist[e] * sign;
  }
  return acc;
}

const evenDist = [0, 1, 2, 3, 4, 5, 6, 7].map((e) =>
  popcount(e) % 2 === 0 ? 0.25 : 0.0
);
const singleCollapseDist = [0, 1, 2, 3, 4, 5, 6, 7].map((e) =>
  e === 0 ? 0.5 : popcount(e) === 1 ? 1 / 6 : 0.0
);

const visEven = walshParity(evenDist);
const visCollapse = walshParity(singleCollapseDist);

if (Math.abs(visEven - 1.0) > 1e-12 || Math.abs(visCollapse - 0.0) > 1e-12) {
  throw new Error("Correlated Z-fault Walsh parity mismatch");
}

console.log(
  JSON.stringify({
    status: "OK",
    visEven,
    visCollapse,
  })
);
