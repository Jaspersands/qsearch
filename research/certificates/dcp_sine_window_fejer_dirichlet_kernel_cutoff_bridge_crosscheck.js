#!/usr/bin/env node
"use strict";

function dirichlet(phi, P) {
  const half = 0.5 * (P - 1);
  let s = 0;
  for (let z = 0; z < P; z++) {
    s += Math.cos(phi * (z - half));
  }
  return s / P;
}

function sineChar(phi, P) {
  const half = 0.5 * (P - 1);
  let s = 0;
  for (let z = 0; z < P; z++) {
    const w = (2 / P) * Math.pow(Math.sin((Math.PI * (z + 0.5)) / P), 2);
    s += w * Math.cos(phi * (z - half));
  }
  return s;
}

const P = 8;
const phi1 = (2 * Math.PI) / P;
const s1 = sineChar(phi1, P);
const d1 = dirichlet(phi1, P);
const phiTest = 0.37;
const sTest = sineChar(phiTest, P);
const cfTest = dirichlet(phiTest, P) + 0.5 * dirichlet(phiTest + phi1, P) + 0.5 * dirichlet(phiTest - phi1, P);
if (Math.abs(s1 - 0.5) > 1e-12 || Math.abs(d1) > 1e-12 || Math.abs(sTest - cfTest) > 1e-12) {
  throw new Error("Sine window three-Dirichlet identity mismatch");
}
const alias = 2 * Math.PI * 7.5 / P;
const aliasSine = Math.abs(sineChar(alias, P));
const aliasBox = Math.abs(dirichlet(alias, P));
if (!(aliasSine > aliasBox)) throw new Error("Missing aliased-main-lobe countercontrol");
for (let j = 0; j <= 64; j++) {
  const phi = 4 * Math.PI / P + (Math.PI - 4 * Math.PI / P) * j / 64;
  const upper = 2 * Math.pow(Math.sin(Math.PI / P), 2) / (P * Math.pow(Math.sin(phi / 2), 3));
  if (Math.abs(sineChar(phi, P)) > upper + 1e-12) throw new Error("Principal bound violated");
}
console.log(JSON.stringify({ status: "OK", s1, d1, diff: Math.abs(sTest - cfTest), aliasSine, aliasBox }));
