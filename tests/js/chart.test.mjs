import test from "node:test";
import assert from "node:assert/strict";
import { activityChart, niceMax } from "../../site/js/lib/chart.js";

test("niceMax rounds up to 1, 2, 2.5, or 5 times a power of ten", () => {
  assert.equal(niceMax(0), 1);
  assert.equal(niceMax(7), 10);
  assert.equal(niceMax(43), 50);
  assert.equal(niceMax(120), 200);
  assert.equal(niceMax(240), 250);
});

test("activityChart draws one bar per week, the line, and month ticks", () => {
  const weeks = [
    { week: "2026-07-06", runs: 4 },
    { week: "2026-07-13", runs: 0 },
    { week: "2026-07-20", runs: 9 },
    { week: "2026-07-27", runs: 2 },
    { week: "2026-08-03", runs: 5 },
  ];
  const points = [
    { date: "2026-07-17", negative_results: 464 },
    { date: "2026-08-05", negative_results: 520 },
  ];
  const svg = activityChart({ weeks, points });
  assert.ok(svg.startsWith("<svg"));
  assert.equal((svg.match(/class="chart-bar"/g) || []).length, 5);
  assert.match(svg, /<path class="chart-line" d="M[\d.]+,[\d.]+ L[\d.]+,[\d.]+"/);
  assert.ok(svg.includes(">Aug<"));
  assert.ok(svg.includes(">520<"));
  assert.ok(svg.includes('class="chart-label chart-label-line" x="670" y="24">1,000<'), "line scale labelled on the right");
  assert.ok(svg.includes('class="chart-label" x="30" y="24" text-anchor="end">10<'), "run scale labelled on the left");
  assert.ok(svg.includes('aria-label="Experiment runs per week from Jul 6, 2026: 20 runs in total. Ideas ruled out grew to 520."'));
});

test("activityChart returns an empty string without weeks", () => {
  assert.equal(activityChart({ weeks: [], points: [] }), "");
});
