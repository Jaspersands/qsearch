#!/usr/bin/env node
"use strict";

const rOcc = 4;
const dimX = 16;
const qTotal = 4;
const singleRepProb = (rOcc * rOcc) / (dimX * qTotal);
// For A = [1, 1, 2, 2] mod 4: subset sums have counts [4, 4, 4, 4] or let's check:
// (1,1) gives {0:1, 1:2, 2:1}, (2,2) gives {0:2, 2:2} -> convolution gives {0:4, 1:4, 2:4, 3:4}!
// Wait: for [1,1,2,2] mod 4, occ = [4, 4, 4, 4], so sqrtSum = 4 * 2 = 8, fullPGM = 64 / 64 = 1.0!
const fullPgm = Math.pow(4 * Math.sqrt(4), 2) / (dimX * qTotal);

if (Math.abs(singleRepProb - 0.25) > 1e-12 || Math.abs(fullPgm - 1.0) > 1e-12) {
  throw new Error("Fiber erasure comparison mismatch");
}

console.log(JSON.stringify({ status: "OK", singleRepProb, fullPgm }));
