#!/usr/bin/env node
"use strict";

function mod(a, m) {
  return ((a % m) + m) % m;
}

function repairedPeakProb(tBits, s1, s2, y0, delta, bGuess) {
  const q = 1 << tBits;
  const targetK1 = mod(delta * s1, q);
  let re = 0;
  let im = 0;
  for (let x1 = 0; x1 < q; x1++) {
    const x2 = mod(x1 + delta, q);
    const phi1 = mod(x1 * (s2 + y0) + ((x1 * (x1 - 1)) / 2) * s1, q);
    const phi2 = mod(x2 * (s2 + y0) + ((x2 * (x2 - 1)) / 2) * s1, q);
    const carrySign = bGuess === 1 && x1 + delta >= q ? -1.0 : 1.0;
    const angle = (2 * Math.PI * mod(phi2 - phi1 - x1 * targetK1, q)) / q;
    re += (carrySign * Math.cos(angle)) / q;
    im += (carrySign * Math.sin(angle)) / q;
  }
  return re * re + im * im;
}

for (let delta = 0; delta < 8; delta++) {
  const pRep = repairedPeakProb(3, 5, 3, 6, delta, 1);
  const pWrong = repairedPeakProb(3, 5, 3, 6, delta, 0);
  const cfWrong = Math.pow(1 - (2 * delta) / 8, 2);
  if (Math.abs(pRep - 1.0) > 1e-12 || Math.abs(pWrong - cfWrong) > 1e-12) {
    throw new Error("Cocycle repair peak mismatch");
  }
}

console.log(
  JSON.stringify({
    status: "OK",
    repairedDelta4Peak: repairedPeakProb(3, 5, 3, 6, 4, 1),
    unrepairedDelta4Peak: repairedPeakProb(3, 5, 3, 6, 4, 0),
  })
);
