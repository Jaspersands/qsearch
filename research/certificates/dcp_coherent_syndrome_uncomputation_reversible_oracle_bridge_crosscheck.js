#!/usr/bin/env node
"use strict";

// Independent explicit real state vectors: |++> and CZ|++>.
const left = [.5, .5, .5, .5];
const right = [.5, .5, .5, -.5];
const inner = left.reduce((s, x, i) => s + x*right[i], 0);
const coherentDistance = Math.sqrt(1-inner*inner);
const dephasedDistance = .5;
if (Math.abs(coherentDistance-Math.sqrt(3)/2) > 1e-14 ||
    !(coherentDistance > dephasedDistance)) {
  throw new Error("Coherent/dephased counterexample failed");
}
// Relative syndrome phase alone can change orthogonal coherent states,
// while all their conditional target density matrices remain identical.
const other = [.5, .5, -.5, -.5];
const orthogonalInner = left.reduce((s, x, i) => s+x*other[i], 0);
if (orthogonalInner !== 0) throw new Error("Lost relative branch phase");
console.log(JSON.stringify({status: "OK", coherentDistance, dephasedDistance,
  oldCoherentUpperBoundRetracted: true}));
