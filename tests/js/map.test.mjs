import test from "node:test";
import assert from "node:assert/strict";
import { TRACK_COLORS, nearestIndex, projectPoints, trackOf } from "../../site/js/lib/map.js";

test("trackOf prefers the smaller literature tracks, then the sieve, then codes", () => {
  assert.equal(trackOf(["CODE-COSET-COLLECTIVE", "HYP-LIT-COSET-OBSERVABLES"]), "HYP-LIT-COSET-OBSERVABLES");
  assert.equal(trackOf(["CODE-COSET-COLLECTIVE", "DHS-GOWERS-SIEVE"]), "DHS-GOWERS-SIEVE");
  assert.equal(trackOf(["CODE-COSET-COLLECTIVE"]), "CODE-COSET-COLLECTIVE");
  assert.equal(trackOf(["SOMETHING-ELSE"]), "OTHER");
  assert.equal(trackOf([]), "OTHER");
});

test("every track has a color", () => {
  for (const key of ["CODE-COSET-COLLECTIVE", "DHS-GOWERS-SIEVE", "HYP-LIT-HIDDEN-SHIFT-SIEVE", "HYP-LIT-COSET-OBSERVABLES", "OTHER"]) {
    assert.match(TRACK_COLORS[key], /^#[0-9a-f]{6}$/);
  }
});

test("projectPoints maps the unit square into the padded canvas", () => {
  assert.deepEqual(projectPoints([{ x: 0, y: 0 }, { x: 1, y: 1 }, { x: 0.5, y: 0.25 }], 220, 120, 10), [
    [10, 10],
    [210, 110],
    [110, 35],
  ]);
});

test("nearestIndex finds the closest included point within range", () => {
  const screen = [[10, 10], [50, 50], [52, 52]];
  assert.equal(nearestIndex(screen, 51, 51.6, () => true), 2);
  assert.equal(nearestIndex(screen, 51, 51.6, (i) => i !== 2), 1);
  assert.equal(nearestIndex(screen, 200, 200, () => true), -1);
  assert.equal(nearestIndex(screen, 30, 30, () => true, 40), 0);
});
