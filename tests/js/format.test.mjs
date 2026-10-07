import test from "node:test";
import assert from "node:assert/strict";
import {
  REPO_URL, bibtexEntry, escapeHtml, formatDate, formatNumber, humanizeId,
  repoUrl, statusMarker, trackStatusKind,
} from "../../site/js/lib/format.js";

test("escapeHtml escapes markup characters", () => {
  assert.equal(escapeHtml(`<a href="x">&'`), "&lt;a href=&quot;x&quot;&gt;&amp;&#39;");
  assert.equal(escapeHtml(null), "");
});

test("formatNumber groups thousands", () => {
  assert.equal(formatNumber(1326), "1,326");
  assert.equal(formatNumber(24), "24");
});

test("formatDate reads date-only and full timestamps the same", () => {
  assert.equal(formatDate("2026-09-23"), "Sep 23, 2026");
  assert.equal(formatDate("2026-09-23T04:10:00+00:00"), "Sep 23, 2026");
});

test("repoUrl encodes each path segment", () => {
  assert.equal(repoUrl("research/a b.json"), `${REPO_URL}/blob/main/research/a%20b.json`);
});

test("status markers use the three-word vocabulary", () => {
  assert.equal(statusMarker("ruled-out"), '<span class="status status-ruled-out">ruled out</span>');
  assert.equal(statusMarker("open"), '<span class="status status-open">open</span>');
  assert.equal(statusMarker("active"), '<span class="status status-active">active</span>');
  assert.equal(trackStatusKind("active"), "active");
  assert.equal(trackStatusKind("blocked"), "open");
});

test("humanizeId turns registry ids into sentence case", () => {
  assert.equal(humanizeId("code-equivalence-hard-family-search"), "Code equivalence hard family search");
});

test("bibtexEntry fills date and count from the snapshot", () => {
  const entry = bibtexEntry({ updated_at: "2026-09-23", metrics: { negative_results: 1934 } });
  assert.ok(entry.startsWith("@misc{sands2026qsearch,"));
  assert.ok(entry.includes("Snapshot of 2026-09-23; 1,934 negative results recorded"));
  assert.ok(entry.endsWith("}"));
});
