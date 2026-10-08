import test from "node:test";
import assert from "node:assert/strict";
import { filterRecords, matchesQuery, recordIdFromHash } from "../../site/js/lib/negatives.js";

const records = [
  { id: "GOPPA-SYZYGY", claim: "Goppa syzygies resist attacks", reason: "Hull projector", lesson: "", source: "x.py", tags: ["CODE-COSET-COLLECTIVE"] },
  { id: "SIEVE-DEPTH", claim: "Fixed depth lists work", reason: "Collapse at scale", lesson: "Use growing depth", source: "y.py", tags: ["DHS-GOWERS-SIEVE"] },
];

test("matchesQuery searches id, claim, reason, lesson, and source case-insensitively", () => {
  assert.equal(matchesQuery(records[0], "goppa"), true);
  assert.equal(matchesQuery(records[0], "HULL"), true);
  assert.equal(matchesQuery(records[1], "growing"), true);
  assert.equal(matchesQuery(records[1], "y.py"), true);
  assert.equal(matchesQuery(records[1], "goppa"), false);
  assert.equal(matchesQuery(records[1], "   "), true);
});

test("filterRecords combines tag and query", () => {
  assert.deepEqual(filterRecords(records, {}).map((r) => r.id), ["GOPPA-SYZYGY", "SIEVE-DEPTH"]);
  assert.deepEqual(filterRecords(records, { tag: "DHS-GOWERS-SIEVE" }).map((r) => r.id), ["SIEVE-DEPTH"]);
  assert.deepEqual(filterRecords(records, { tag: "DHS-GOWERS-SIEVE", query: "goppa" }), []);
});

test("recordIdFromHash decodes the fragment", () => {
  assert.equal(recordIdFromHash("#SIEVE-DEPTH"), "SIEVE-DEPTH");
  assert.equal(recordIdFromHash("#A%20B"), "A B");
  assert.equal(recordIdFromHash(""), "");
  assert.equal(recordIdFromHash("#%E0%A4%A"), "%E0%A4%A");
});
