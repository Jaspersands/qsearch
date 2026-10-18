#!/usr/bin/env node
"use strict";

function mod(a, m) {
  return ((a % m) + m) % m;
}

function minWeightKernel1D(b0, b1) {
  if (mod(b0, 2) === 0) return [1, 0];
  if (mod(b1, 2) === 0) return [0, 1];
  return [1, 1];
}

function evalCascade(aRow, gamma0) {
  const qMod = 8;
  let adaptHits = 0;
  let wtSum = 0;
  let visSum = 0;

  for (let mask = 0; mask < 16; mask++) {
    const y1 = [mask & 1, (mask >> 1) & 1, (mask >> 2) & 1, (mask >> 3) & 1];
    const s1Cols = [0, 1, 2, 3].map((j) =>
      mod(aRow[2 * j] + (1 - 2 * y1[j]) * aRow[2 * j + 1], qMod)
    );
    const b1 = s1Cols.map((c) => Math.floor(mod(c, 4) / 2));
    const w2A = minWeightKernel1D(b1[0], b1[1]);
    const w2B = minWeightKernel1D(b1[2], b1[3]);

    let branchOk = true;
    let branchWt = 0;
    let branchVis = 0;

    for (let d2A = 0; d2A < 2; d2A++) {
      const col2A =
        w2A[0] === 1 && w2A[1] === 0
          ? s1Cols[0]
          : w2A[0] === 0 && w2A[1] === 1
          ? s1Cols[1]
          : mod(s1Cols[0] + (1 - 2 * d2A) * s1Cols[1], qMod);
      const wt2A = w2A[0] + w2A[1] === 1 ? 2 : 4;

      for (let d2B = 0; d2B < 2; d2B++) {
        const col2B =
          w2B[0] === 1 && w2B[1] === 0
            ? s1Cols[2]
            : w2B[0] === 0 && w2B[1] === 1
            ? s1Cols[3]
            : mod(s1Cols[2] + (1 - 2 * d2B) * s1Cols[3], qMod);
        const wt2B = w2B[0] + w2B[1] === 1 ? 2 : 4;

        const b2A = Math.floor(mod(col2A, 8) / 4);
        const b2B = Math.floor(mod(col2B, 8) / 4);
        const w3 = minWeightKernel1D(b2A, b2B);

        for (let d3 = 0; d3 < 2; d3++) {
          const col3 =
            w3[0] === 1 && w3[1] === 0
              ? col2A
              : w3[0] === 0 && w3[1] === 1
              ? col2B
              : mod(col2A + (1 - 2 * d3) * col2B, qMod);
          const wt3 =
            w3[0] === 1 && w3[1] === 0
              ? wt2A
              : w3[0] === 0 && w3[1] === 1
              ? wt2B
              : wt2A + wt2B;
          if (mod(col3, 8) !== 0) branchOk = false;
          branchWt += wt3 / 8;
          branchVis += Math.pow(gamma0, wt3) / 8;
        }
      }
    }
    if (branchOk) adaptHits++;
    wtSum += branchWt;
    visSum += branchVis;
  }
  return {
    adaptFrac: adaptHits / 16,
    meanWt: wtSum / 16,
    meanVis: visSum / 16,
  };
}

const gamma0 = 0.85;
const cAll0 = evalCascade([1, 7, 3, 5, 1, 7, 3, 5], gamma0);
const cAll4 = evalCascade([1, 3, 5, 7, 1, 5, 3, 7], gamma0);

let ensWt = 0;
let ensVis = 0;
const pairs = [
  [1, 7],
  [1, 3],
];
for (let m = 0; m < 16; m++) {
  const row = [];
  for (let j = 0; j < 4; j++) {
    const p = pairs[(m >> j) & 1];
    row.push(p[0], p[1]);
  }
  const r = evalCascade(row, gamma0);
  if (r.adaptFrac !== 1.0) throw new Error("Mod 8 cascade failed");
  ensWt += r.meanWt / 16;
  ensVis += r.meanVis / 16;
}

const v1 = Math.pow(gamma0, 2);
const v2 = 0.75 * v1 + 0.25 * v1 * v1;
const v3 = 0.75 * v2 + 0.25 * v2 * v2;

if (
  Math.abs(cAll0.meanWt - 2.375) > 1e-12 ||
  Math.abs(cAll4.meanWt - 4.4375) > 1e-12 ||
  Math.abs(ensWt - 3.125) > 1e-12 ||
  Math.abs(ensVis - v3) > 1e-12
) {
  throw new Error("Cascaded dyadic weight pruning mismatch");
}

console.log(
  JSON.stringify({
    status: "OK",
    adaptiveMod8ZeroFraction: 1.0,
    meanWtAll0: cAll0.meanWt,
    meanWtAll4: cAll4.meanWt,
    ensembleMeanWt: ensWt,
    ensembleMeanVis: ensVis,
  })
);
