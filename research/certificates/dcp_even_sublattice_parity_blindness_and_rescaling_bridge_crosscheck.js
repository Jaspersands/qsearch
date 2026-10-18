#!/usr/bin/env node
"use strict";

function mod(a, m) {
  return ((a % m) + m) % m;
}

function effectiveCol(A, v, x0, t) {
  const q = 1 << t;
  return A.map((row) => {
    let acc = 0;
    for (let r = 0; r < v.length; r++) {
      if (v[r]) {
        const sign = 1 - 2 * x0[r];
        acc += sign * row[r];
      }
    }
    return mod(acc, q);
  });
}

function condAdv(cols, h, t) {
  const q = 1 << t;
  const m = cols.length;
  const n = h.length;
  const occ = new Set();
  for (let mask = 0; mask < (1 << m); mask++) {
    const label = [];
    for (let i = 0; i < n; i++) {
      let s = 0;
      for (let j = 0; j < m; j++) {
        if ((mask >> j) & 1) s += cols[j][i];
      }
      label.push(mod(s, q));
    }
    occ.add(label.join(","));
  }
  let hits = 0;
  for (let mask = 0; mask < (1 << m); mask++) {
    const shifted = [];
    for (let i = 0; i < n; i++) {
      let s = h[i];
      for (let j = 0; j < m; j++) {
        if ((mask >> j) & 1) s += cols[j][i];
      }
      shifted.push(mod(s, q));
    }
    if (occ.has(shifted.join(","))) hits++;
  }
  return hits / (1 << m);
}

// Check A = [[2, 0]] mod 4 and A = [[1, 1]] mod 4
let sum20 = 0;
let sum11 = 0;
for (let b0 = 0; b0 < 2; b0++) {
  for (let b1 = 0; b1 < 2; b1++) {
    const c20 = effectiveCol([[2, 0]], [1, 1], [b0, b1], 2);
    const c11 = effectiveCol([[1, 1]], [1, 1], [b0, b1], 2);
    if (c20[0] % 2 !== 0 || c11[0] % 2 !== 0) {
      throw new Error("Effective column not even!");
    }
    sum20 += condAdv([c20], [2], 2);
    sum11 += condAdv([c11], [2], 2);
  }
}
if (Math.abs(sum20 / 4 - 1.0) > 1e-12) throw new Error("A=[[2,0]] mean mismatch");
if (Math.abs(sum11 / 4 - 0.5) > 1e-12) throw new Error("A=[[1,1]] mean mismatch");

console.log(JSON.stringify({ status: "OK", mean_2_0: sum20 / 4, mean_1_1: sum11 / 4 }));
