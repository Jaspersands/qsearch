#!/usr/bin/env node
"use strict";

function mod(a, m) {
  return ((a % m) + m) % m;
}

function checkFrac(A, v, kLevel) {
  const m2k = 1 << kLevel;
  const K = v.length;
  let target = 0;
  for (let r = 0; r < K; r++) if (v[r]) target = mod(target + A[r], m2k);
  let hits = 0;
  for (let mask = 0; mask < (1 << K); mask++) {
    let acc = 0;
    for (let r = 0; r < K; r++) {
      if (v[r]) {
        const x0r = (mask >> r) & 1;
        acc += (1 - 2 * x0r) * A[r];
      }
    }
    if (mod(acc, m2k) === target) hits++;
  }
  return hits / (1 << K);
}

const f1 = checkFrac([1, 3], [1, 1], 1);
const f2Odd = checkFrac([1, 3], [1, 1], 2);
const f2Even = checkFrac([2, 6, 1], [1, 1, 0], 2);
const f3DoublyEven = checkFrac([4, 4, 3], [1, 1, 0], 3);
if (f1 !== 1.0 || f2Odd !== 0.5 || f2Even !== 1.0 || f3DoublyEven !== 1.0) {
  throw new Error("Dyadic hierarchy mismatch");
}
console.log(JSON.stringify({ status: "OK", f1, f2Odd, f2Even, f3DoublyEven }));
