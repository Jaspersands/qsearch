#!/usr/bin/env node
"use strict";

const th = Math.PI / 3.0;
const gm = 0.85;
const tier1X = gm * Math.pow(Math.sin(0.5 * th), 2);
const tier2Tilted = gm * Math.abs(Math.sin(0.5 * th));

if (Math.abs(tier1X - 0.2125) > 1e-12 || Math.abs(tier2Tilted - 0.425) > 1e-12) {
  throw new Error("Single-packet tilted vs X bias mismatch");
}

// A separate pure-state/coin calculation falsifies the old universal ordering.
const angles = [Math.PI / 2, 17 * Math.PI / 32];
const overlapSquared = angles.reduce((p, t) => p * Math.cos(t / 2) ** 2, 1);
const counterexampleX = 1 - overlapSquared;
const counterexampleTilted = Math.max(...angles.map(t => Math.sin(t / 2)));
const counterexampleCollective = Math.sqrt(1 - overlapSquared);
if (!(counterexampleCollective > counterexampleX && counterexampleX > counterexampleTilted)) {
  throw new Error("Product-order counterexample failed");
}

console.log(
  JSON.stringify({
    status: "OK",
    tier1X,
    tier2Tilted,
    counterexampleX,
    counterexampleTilted,
    counterexampleCollective,
  })
);
