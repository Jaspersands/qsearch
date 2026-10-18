#!/usr/bin/env node
"use strict";

function mod(a, m) {
  return ((a % m) + m) % m;
}

function dyadicPeakProb(tBits, s1, s2, y0, delta) {
  const q = 1 << tBits;
  const targetK1 = mod(delta * s1, q);
  let re = 0;
  let im = 0;
  for (let x1 = 0; x1 < q; x1++) {
    const x2 = mod(x1 + delta, q);
    const phi1 = mod(x1 * (s2 + y0) + ((x1 * (x1 - 1)) / 2) * s1, q);
    const phi2 = mod(x2 * (s2 + y0) + ((x2 * (x2 - 1)) / 2) * s1, q);
    const angle = (2 * Math.PI * mod(phi2 - phi1 - x1 * targetK1, q)) / q;
    re += Math.cos(angle) / q;
    im += Math.sin(angle) / q;
  }
  return re * re + im * im;
}

for (let delta = 0; delta < 8; delta++) {
  const pOdd = dyadicPeakProb(3, 5, 3, 6, delta);
  const cfOdd = Math.pow(1 - (2 * delta) / 8, 2);
  const pEven = dyadicPeakProb(3, 6, 3, 5, delta);
  if (Math.abs(pOdd - cfOdd) > 1e-12 || Math.abs(pEven - 1.0) > 1e-12) {
    throw new Error("Heisenberg dyadic boundary cocycle mismatch");
  }
}

console.log(
  JSON.stringify({
    status: "OK",
    delta1OddPeak: dyadicPeakProb(3, 5, 3, 6, 1),
    delta4OddPeak: dyadicPeakProb(3, 5, 3, 6, 4),
    evenS1Peak: dyadicPeakProb(3, 6, 3, 5, 3),
  })
);
