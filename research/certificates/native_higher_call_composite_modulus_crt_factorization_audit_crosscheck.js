#!/usr/bin/env node
"use strict";

const q1 = 2, q2 = 3, q = 6;
const p1 = [0.75, 0.25];
const p2 = [0.6, 0.2, 0.2];
const pq = Array.from({ length: q }, (_, e) => p1[e % q1] * p2[e % q2]);
const B = [1, 2, 5];

function validProb(probs, m) {
  let tot = 0;
  for (let z0 = 0; z0 < m; z0++) {
    for (let z1 = 0; z1 < m; z1++) {
      for (let z2 = 0; z2 < m; z2++) {
        if ((B[0]*z0 + B[1]*z1 + B[2]*z2) % m === 0) {
          tot += probs[z0] * probs[z1] * probs[z2];
        }
      }
    }
  }
  return tot;
}

const pv6 = validProb(pq, 6);
const pv2 = validProb(p1, 2);
const pv3 = validProb(p2, 3);
if (Math.abs(pv6 - pv2 * pv3) > 1e-12) {
  throw new Error("CRT P_valid factorization mismatch");
}
console.log(JSON.stringify({ status: "OK", pv6, product: pv2 * pv3 }));
