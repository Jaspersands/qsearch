#!/usr/bin/env node
"use strict";

function gammaSinCF(delta, P) {
  const frac = delta / P;
  const angle = Math.PI * frac;
  const sinPiP = Math.sin(Math.PI / P);
  return (1.0 - frac) * Math.cos(angle) + (1.0 / P) * (Math.sin(angle) / sinPiP);
}

const g1 = gammaSinCF(1, 32);
const c1 = (1.0 - 1.0 / 32.0) * Math.cos(Math.PI / 32) + 1.0 / 32.0;
if (Math.abs(g1 - c1) > 1e-12) {
  throw new Error("Sine window unit-shift identity mismatch");
}

console.log(JSON.stringify({ status: "OK", P32Delta1: g1 }));
