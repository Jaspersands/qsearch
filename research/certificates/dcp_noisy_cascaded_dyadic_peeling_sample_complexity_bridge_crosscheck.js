#!/usr/bin/env node
"use strict";

function evalBudget(tBits, gamma0) {
  let vPruned = gamma0;
  let cumPruned = 0;
  let cumUnpruned = 0;
  for (let ell = 1; ell <= tBits; ell++) {
    const rawWires = 1 << (ell - 1);
    if (ell === 1) vPruned = gamma0;
    else if (ell === 2) vPruned = gamma0 * gamma0;
    else vPruned = 0.75 * vPruned + 0.25 * vPruned * vPruned;

    const vUnpruned = Math.pow(gamma0, rawWires);
    cumPruned += rawWires / (vPruned * vPruned);
    cumUnpruned += rawWires / (vUnpruned * vUnpruned);
  }
  return { cumPruned, cumUnpruned, ratio: cumUnpruned / cumPruned };
}

const bNoiseless = evalBudget(5, 1.0);
const bT5 = evalBudget(5, 0.85);
const bT6 = evalBudget(6, 0.85);

if (
  Math.abs(bNoiseless.cumPruned - 31) > 1e-12 ||
  bT5.ratio < 35.0 ||
  bT6.ratio < 4800.0
) {
  throw new Error("Noisy cascaded peeling budget mismatch");
}

console.log(
  JSON.stringify({
    status: "OK",
    noiselessT5: bNoiseless.cumPruned,
    t5Ratio: bT5.ratio,
    t6Ratio: bT6.ratio,
  })
);
