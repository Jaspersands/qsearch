#!/usr/bin/env node
"use strict";

function mod(a, m) {
  return ((a % m) + m) % m;
}

function linearFrac(aRow, d, t) {
  const q = Math.pow(d, t);
  let lin = 0;
  for (let y0 = 0; y0 < d; y0++) {
    for (let y1 = 0; y1 < d; y1++) {
      const ph = [];
      for (let u = 0; u < d; u++) {
        ph.push(mod(aRow[0] * mod(y0 + u, d) + aRow[1] * mod(y1 + u, d), q));
      }
      const slope = mod(ph[1] - ph[0], q);
      let ok = true;
      for (let u = 0; u < d; u++) {
        if (mod(ph[u] - ph[0], q) !== mod(u * slope, q)) ok = false;
      }
      if (ok) lin++;
    }
  }
  return lin / (d * d);
}

const fQubit = linearFrac([1, 3], 2, 3);
const fQutritOdd = linearFrac([1, 2], 3, 2);
const fQutritDiv = linearFrac([3, 6], 3, 2);

if (
  Math.abs(fQubit - 1.0) > 1e-12 ||
  Math.abs(fQutritOdd - 1.0 / 3.0) > 1e-12 ||
  Math.abs(fQutritDiv - 1.0) > 1e-12
) {
  throw new Error("d-ary qudit linearity fraction mismatch");
}

console.log(JSON.stringify({ status: "OK", fQubit, fQutritOdd, fQutritDiv }));
