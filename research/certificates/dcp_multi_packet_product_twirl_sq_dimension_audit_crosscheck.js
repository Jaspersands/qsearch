#!/usr/bin/env node
"use strict";

const q = 5;
const n = 2;
let maxOffDiag = 0;
const vecs = [];
for (let x = 0; x < q; x++) {
  for (let y = 0; y < q; y++) {
    vecs.push([x, y]);
  }
}

function phi(a, s) {
  const dot = (a[0] * s[0] + a[1] * s[1]) % q;
  return Math.cos((2 * Math.PI * dot) / q);
}

const reps = [];
const seen = new Set();
for (const s of vecs) {
  if (s[0] === 0 && s[1] === 0) continue;
  const k = s.join(",");
  if (seen.has(k)) continue;
  const ns = [((q - s[0]) % q), ((q - s[1]) % q)];
  seen.add(k);
  seen.add(ns.join(","));
  reps.push(s);
}

for (let i = 0; i < reps.length; i++) {
  for (let j = i + 1; j < reps.length; j++) {
    let ip = 0;
    for (const a of vecs) {
      ip += phi(a, reps[i]) * phi(a, reps[j]);
    }
    ip /= vecs.length;
    if (Math.abs(ip) > maxOffDiag) maxOffDiag = Math.abs(ip);
  }
}

if (reps.length !== 12 || maxOffDiag > 1e-12) {
  throw new Error("Cosine orthogonality check failed");
}
console.log(JSON.stringify({ status: "OK", sq_dim: reps.length, maxOffDiag }));
