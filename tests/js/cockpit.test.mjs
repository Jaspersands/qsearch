import test from "node:test";
import assert from "node:assert/strict";
import {
  commitChart,
  commitsInWindow,
  compactCount,
  fillDays,
  flaggedSentence,
  formatDuration,
  inertiaRows,
  latestCommits,
  metricLabel,
  nearestTick,
  recentSections,
  rugChart,
  rugLayout,
  sectionDate,
  sparkline,
  spendTotals,
  topicTotals,
} from "../../site/js/lib/cockpit.js";

const DAYS = [
  { date: "2026-09-29", count: 2, topics: { dcp: 2 }, commits: [] },
  { date: "2026-10-01", count: 3, topics: { dcp: 1, other: 2 }, commits: [] },
  { date: "2026-10-03", count: 1, topics: { lattice: 1 }, commits: [] },
];

function section(index, order, direction, agent, extra = {}) {
  return {
    index,
    order,
    direction,
    agent,
    heading: `Section ${index}`,
    first_committed: "2026-10-01",
    heading_date: null,
    new_registry_ids: [],
    ...extra,
  };
}

const SECTIONS = [
  section(0, 4, "opi", "codex", { first_committed: null }),
  section(1, 3, "dcp", "gemini", { new_registry_ids: ["NEG-A"] }),
  section(2, 2, "dcp", "unknown", { first_committed: "2026-09-12" }),
  section(3, 1, "lattice", "codex", { first_committed: "2026-08-30" }),
  section(4, 0, "other", "codex", { first_committed: "2026-08-20", heading: "Resume <commands>" }),
];

test("fillDays adds the empty days between and after commit days", () => {
  const filled = fillDays(DAYS, "2026-10-05");
  assert.deepEqual(
    filled.map((day) => [day.date, day.count]),
    [
      ["2026-09-29", 2],
      ["2026-09-30", 0],
      ["2026-10-01", 3],
      ["2026-10-02", 0],
      ["2026-10-03", 1],
      ["2026-10-04", 0],
      ["2026-10-05", 0],
    ],
  );
  assert.deepEqual(filled[1].topics, {});
  assert.deepEqual(fillDays([], "2026-10-05"), []);
});

test("commitsInWindow counts commits in the last n days up to and including the end date", () => {
  assert.equal(commitsInWindow(DAYS, "2026-10-03", 3), 4);
  assert.equal(commitsInWindow(DAYS, "2026-10-03", 7), 6);
  assert.equal(commitsInWindow(DAYS, "2026-10-10", 7), 0);
  assert.equal(commitsInWindow(DAYS, "2026-10-10", 8), 1);
  assert.equal(commitsInWindow([], "2026-10-10", 7), 0);
});

test("commitChart draws a bar per commit day, a hover target per day, and month ticks", () => {
  const days = fillDays(DAYS, "2026-10-05");
  const svg = commitChart({ days, labels: { dcp: "DCP / dihedral coset", other: "Other", lattice: "Ternary / lattice" } });
  assert.ok(svg.startsWith("<svg"));
  assert.equal((svg.match(/class="chart-bar"/g) || []).length, 3);
  assert.equal((svg.match(/class="chart-hit"/g) || []).length, 7);
  assert.ok(svg.includes(">Oct<"), "month tick");
  assert.ok(svg.includes("<title>Oct 1, 2026: 3 commits (Other 2, DCP / dihedral coset 1)</title>"));
  assert.ok(svg.includes("<title>Sep 30, 2026: no commits</title>"));
  assert.ok(svg.includes('aria-label="Commits per day from Sep 29, 2026 to Oct 5, 2026: 6 commits in total."'));
  assert.equal(commitChart({ days: [] }), "");
});

test("topicTotals counts commits per topic for a recent window and for all time", () => {
  const totals = topicTotals(DAYS, "2026-10-03", 3);
  assert.deepEqual(totals, [
    { topic: "dcp", recent: 1, all: 3 },
    { topic: "other", recent: 2, all: 2 },
    { topic: "lattice", recent: 1, all: 1 },
  ]);
});

test("latestCommits lists commits newest first across days", () => {
  const days = [
    { date: "2026-10-01", count: 2, topics: {}, commits: [{ sha: "a1" }, { sha: "a2" }] },
    { date: "2026-10-02", count: 1, topics: {}, commits: [{ sha: "b1" }] },
  ];
  assert.deepEqual(latestCommits(days, 2), [
    { sha: "b1", date: "2026-10-02" },
    { sha: "a1", date: "2026-10-01" },
  ]);
  assert.deepEqual(latestCommits([], 5), []);
});

test("sectionDate prefers the first commit date and says when a section is not committed", () => {
  assert.equal(sectionDate(SECTIONS[1]), "Oct 1, 2026");
  assert.equal(sectionDate(SECTIONS[0]), "not committed yet");
});

test("recentSections lists newest first and filters by direction and agent", () => {
  assert.deepEqual(recentSections(SECTIONS, {}).map((s) => s.index), [0, 1, 2, 3, 4]);
  assert.deepEqual(recentSections(SECTIONS, { limit: 2 }).map((s) => s.index), [0, 1]);
  assert.deepEqual(recentSections(SECTIONS, { direction: "dcp" }).map((s) => s.index), [1, 2]);
  assert.deepEqual(recentSections(SECTIONS, { agent: "codex" }).map((s) => s.index), [0, 3, 4]);
  assert.deepEqual(recentSections(SECTIONS, { direction: "dcp", agent: "gemini" }).map((s) => s.index), [1]);
});

test("rugLayout puts one tick per section in its group's row, in chronological order", () => {
  const groups = [
    { id: "dcp", label: "DCP / dihedral coset" },
    { id: "opi", label: "OPI / prime character" },
    { id: "hdqi", label: "HDQI" },
  ];
  const layout = rugLayout({ sections: SECTIONS, groups, key: "direction", width: 600, labelWidth: 100 });
  assert.equal(layout.rows.length, 3);
  const [dcp, opi, hdqi] = layout.rows;
  assert.deepEqual(dcp.ticks.map((t) => t.index), [2, 1]);
  assert.deepEqual(dcp.ticks.map((t) => t.isNew), [false, true]);
  assert.equal(dcp.count, 2);
  assert.equal(hdqi.ticks.length, 0);
  // five sections spread evenly over the 500px plot: order 4 sits in the last slot
  assert.equal(opi.ticks[0].x, 100 + 4.5 * 100);
  assert.ok(dcp.ticks[0].x < dcp.ticks[1].x);
  assert.ok(opi.top > dcp.top);
  assert.deepEqual(layout.months.map((m) => m.label), ["Aug", "Sep", "Oct"]);
  assert.equal(layout.months[0].x, 100);
});

test("rugChart draws every tick, marks new registry entries, and escapes labels", () => {
  const groups = [
    { id: "codex", label: "Codex" },
    { id: "gemini", label: "Gemini <g>" },
  ];
  const layout = rugLayout({ sections: SECTIONS, groups, key: "agent", width: 600, labelWidth: 100 });
  const svg = rugChart(layout, "Handoff sections by agent");
  assert.ok(svg.startsWith("<svg"));
  assert.equal((svg.match(/class="rug-tick( rug-new)?"/g) || []).length, 4);
  assert.equal((svg.match(/class="rug-tick rug-new"/g) || []).length, 1);
  assert.ok(svg.includes("Gemini &lt;g&gt;"));
  assert.ok(svg.includes('aria-label="Handoff sections by agent"'));
});

test("nearestTick finds the closest tick within a distance, or -1", () => {
  const ticks = [{ x: 10 }, { x: 30 }, { x: 31 }, { x: 80 }];
  assert.equal(nearestTick(ticks, 29, 6), 1);
  assert.equal(nearestTick(ticks, 32, 6), 2);
  assert.equal(nearestTick(ticks, 55, 6), -1);
  assert.equal(nearestTick([], 10, 6), -1);
});

test("inertiaRows puts flagged directions first, longest streak first", () => {
  const inertia = {
    threshold: 8,
    directions: [
      { direction: "hdqi", label: "HDQI", sections: 2, streak: 2, flag: false, last_new: null, sections_ago: 8 },
      { direction: "opi", label: "OPI", sections: 13, streak: 13, flag: true, last_new: null, sections_ago: 0 },
      {
        direction: "lattice",
        label: "Ternary / lattice",
        sections: 113,
        streak: 22,
        flag: true,
        last_new: { index: 120, ids: ["NEG-X", "NEG-Y"], first_committed: "2026-10-12", heading: "h" },
        sections_ago: 7,
      },
      { direction: "dcp", label: "DCP", sections: 118, streak: 3, flag: false, last_new: { ids: ["NEG-Z"], first_committed: null }, sections_ago: 0 },
    ],
  };
  const rows = inertiaRows(inertia);
  assert.deepEqual(rows.map((r) => r.direction), ["lattice", "opi", "dcp", "hdqi"]);
  assert.equal(rows[0].lastNew, "Oct 12, 2026 (NEG-X and 1 more)");
  assert.equal(rows[1].lastNew, "none in the log");
  assert.equal(rows[2].lastNew, "not committed yet (NEG-Z)");
  assert.equal(rows[0].lastSeen, "7 sections ago");
  assert.equal(rows[1].lastSeen, "latest section");
  assert.equal(rows[3].lastSeen, "8 sections ago");
});

test("flaggedSentence names the flagged directions and the threshold", () => {
  const flags = [{ label: "OPI / prime character" }, { label: "BPQM / polar" }, { label: "Ternary / lattice" }];
  assert.equal(
    flaggedSentence({ threshold: 8, flags }),
    "OPI / prime character, BPQM / polar and Ternary / lattice have each run 8 or more of their own handoff sections without a new registry entry.",
  );
  assert.equal(
    flaggedSentence({ threshold: 5, flags: [flags[0]] }),
    "OPI / prime character has run 5 or more of its own handoff sections without a new registry entry.",
  );
  assert.equal(flaggedSentence({ threshold: 8, flags: [] }), "No direction has run 8 or more of its own handoff sections without a new registry entry.");
});

test("sparkline draws one line through every point and labels the last value", () => {
  const points = [
    { date: "2026-07-17", metrics: { negative_results: 464 } },
    { date: "2026-08-12", metrics: { negative_results: 700 } },
    { date: "2026-10-15", metrics: { negative_results: 976 } },
    { date: "2026-10-16", metrics: {} },
  ];
  const chart = sparkline({ points, key: "negative_results", width: 240, height: 64 });
  assert.equal(chart.points.length, 3);
  assert.match(chart.svg, /<path class="chart-line" d="M[\d.]+,[\d.]+ L[\d.]+,[\d.]+ L[\d.]+,[\d.]+"/);
  assert.ok(chart.svg.includes(">976<"));
  assert.ok(chart.svg.includes('aria-label="Negative results: 464 on Jul 17, 2026, 976 on Oct 15, 2026."'));
  assert.ok(chart.points[0].x < chart.points[2].x);
  assert.ok(chart.points[0].y > chart.points[2].y, "bigger values sit higher");
  assert.equal(sparkline({ points: [], key: "results" }).svg, "");
});

test("metricLabel names the snapshot metrics in plain words", () => {
  assert.equal(metricLabel("negative_results"), "Negative results");
  assert.equal(metricLabel("proof_debts"), "Proof debts");
  assert.equal(metricLabel("something_new"), "Something new");
});

test("formatDuration picks seconds, minutes or hours and admits unknown values", () => {
  assert.equal(formatDuration(45), "45 s");
  assert.equal(formatDuration(1800), "30 min");
  assert.equal(formatDuration(5400), "1.5 h");
  assert.equal(formatDuration(0), "0 s");
  assert.equal(formatDuration(null), "not recorded");
});

test("compactCount keeps large totals short enough for a figure", () => {
  assert.equal(compactCount(598), "598");
  assert.equal(compactCount(9999), "9,999");
  assert.equal(compactCount(12345), "12.3 thousand");
  assert.equal(compactCount(9438873), "9.44 million");
  assert.equal(compactCount(173000000), "173 million");
  assert.equal(compactCount(5471259754), "5.47 billion");
  assert.equal(compactCount(999950), "1 million");
});

test("spendTotals sums the spend days and keeps unknown totals unknown", () => {
  const totals = spendTotals({
    days: [
      { date: "2026-10-18", runs: 3, wall_seconds: 3600, cpu_seconds: null, negatives_added: 1, tokens: null },
      { date: "2026-10-19", runs: 2, wall_seconds: 1800, cpu_seconds: null, negatives_added: 0, tokens: 5000 },
    ],
  });
  assert.deepEqual(totals, { days: 2, runs: 5, wall_hours: 1.5, cpu_hours: null, negatives_added: 1, tokens: 5000 });
  assert.deepEqual(spendTotals({ days: [] }), { days: 0, runs: 0, wall_hours: 0, cpu_hours: null, negatives_added: 0, tokens: null });
});
