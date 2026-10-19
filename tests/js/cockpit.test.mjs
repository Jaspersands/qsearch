import test from "node:test";
import assert from "node:assert/strict";
import {
  builtHtml,
  checkpointHtml,
  commitChart,
  commitItemHtml,
  commitsInWindow,
  compactCount,
  dirtyHtml,
  fillDays,
  flaggedSentence,
  formatDuration,
  handoffUrl,
  headFigures,
  inertiaRows,
  latestCommits,
  metricLabel,
  nearestTick,
  recentSections,
  registrySentence,
  rugChart,
  rugLayout,
  runPanels,
  runRowHtml,
  sectionDate,
  sectionRowHtml,
  sparkCardsHtml,
  sparkline,
  spendRowHtml,
  spendTotals,
  tokenLabel,
  topicTotals,
  warningsHtml,
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
    line: 10 + index,
    head_line: 10 + index,
    first_committed: "2026-10-01",
    heading_date: null,
    first_quoted_ids: [],
    registry_day: false,
    cues: [],
    direction_weak: false,
    ...extra,
  };
}

const SECTIONS = [
  section(0, 4, "opi", "codex", { first_committed: null, head_line: null }),
  section(1, 3, "dcp", "gemini", { registry_day: true, first_quoted_ids: ["NEG-A"] }),
  section(2, 2, "dcp", "unknown", { first_committed: "2026-09-12" }),
  section(3, 1, "lattice", "codex", { first_committed: "2026-08-30" }),
  section(4, 0, "other", "codex", { first_committed: "2026-08-20", heading: "Resume <commands>" }),
];

const LABELS = { dcp: "DCP / dihedral coset", other: "Other", lattice: "Ternary / lattice", opi: "OPI / prime character" };
const HEAD = { sha: "9d81df33", commit: "9d81df33c22bedd568bb7c572fcea3347c38a149", date: "2026-10-18" };

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
  const svg = commitChart({ days, labels: LABELS });
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

test("rugLayout puts one tick per section in its group's row and marks registry-gain days", () => {
  const groups = [
    { id: "dcp", label: "DCP / dihedral coset" },
    { id: "opi", label: "OPI / prime character" },
    { id: "hdqi", label: "HDQI" },
  ];
  const layout = rugLayout({ sections: SECTIONS, groups, key: "direction", width: 600, labelWidth: 100 });
  assert.equal(layout.rows.length, 3);
  const [dcp, opi, hdqi] = layout.rows;
  assert.deepEqual(dcp.ticks.map((t) => t.index), [2, 1]);
  // Orange ticks follow registry growth, not quoted ids: a quoted id alone does not mark a tick.
  assert.deepEqual(dcp.ticks.map((t) => t.isNew), [false, true]);
  const quotedOnly = rugLayout({
    sections: [section(0, 0, "dcp", "codex", { first_quoted_ids: ["NEG-B"], registry_day: false })],
    groups,
    key: "direction",
  });
  assert.equal(quotedOnly.rows[0].ticks[0].isNew, false);
  assert.equal(dcp.count, 2);
  assert.equal(hdqi.ticks.length, 0);
  // five sections spread evenly over the 500px plot: order 4 sits in the last slot
  assert.equal(opi.ticks[0].x, 100 + 4.5 * 100);
  assert.ok(dcp.ticks[0].x < dcp.ticks[1].x);
  assert.ok(opi.top > dcp.top);
  assert.deepEqual(layout.months.map((m) => m.label), ["Aug", "Sep", "Oct"]);
  assert.equal(layout.months[0].x, 100);
});

test("rugChart draws every tick, marks registry-gain days, and escapes labels", () => {
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

test("inertiaRows puts flagged directions first and describes each direction's last registry gain", () => {
  const inertia = {
    threshold: 8,
    available: true,
    directions: [
      { direction: "hdqi", label: "HDQI", sections: 2, streak: 2, flag: false, last_gain: null, gained: 0, sections_ago: 8 },
      { direction: "opi", label: "OPI", sections: 13, streak: 13, flag: true, last_gain: null, gained: 0, sections_ago: 0 },
      {
        direction: "lattice",
        label: "Ternary / lattice",
        sections: 113,
        streak: 22,
        flag: true,
        last_gain: { date: "2026-10-12", records: 1, ids: ["NEG-X"] },
        gained: 2,
        sections_ago: 7,
      },
      { direction: "dcp", label: "DCP", sections: 118, streak: 3, flag: false, last_gain: { date: null, records: 2, ids: ["NEG-Z"] }, gained: 9, sections_ago: 0 },
    ],
  };
  const rows = inertiaRows(inertia, { date: "2026-07-15", records: 464 });
  assert.deepEqual(rows.map((r) => r.direction), ["lattice", "opi", "dcp", "hdqi"]);
  assert.equal(rows[0].lastGain, "Oct 12, 2026 (1 record)");
  assert.equal(rows[1].lastGain, "none after Jul 15, 2026");
  assert.equal(rows[2].lastGain, "not committed yet (2 records)");
  assert.equal(rows[0].gained, 2);
  assert.equal(rows[0].lastSeen, "7 sections ago");
  assert.equal(rows[1].lastSeen, "latest section");
  assert.equal(rows[3].lastSeen, "8 sections ago");
  assert.equal(inertiaRows(inertia, null)[1].lastGain, "none recorded");
});

test("flaggedSentence names the flagged directions and says what is measured", () => {
  const flags = [{ label: "OPI / prime character" }, { label: "BPQM / polar" }, { label: "Ternary / lattice" }];
  assert.equal(
    flaggedSentence({ threshold: 8, flags, available: true }),
    "OPI / prime character, BPQM / polar and Ternary / lattice have each had 8 or more of their own handoff sections " +
      "since the registry last gained a record in their direction.",
  );
  assert.equal(
    flaggedSentence({ threshold: 5, flags: [flags[0]], available: true }),
    "OPI / prime character has had 5 or more of its own handoff sections since the registry last gained a record in its direction.",
  );
  assert.equal(
    flaggedSentence({ threshold: 8, flags: [], available: true }),
    "No direction has had 8 or more of its own handoff sections since the registry last gained a record in its direction.",
  );
  assert.match(flaggedSentence({ threshold: 8, flags: [], available: false }), /not measured/);
});

test("registrySentence reports registry growth by direction and the unclassified count", () => {
  const registry = {
    baseline: { date: "2026-07-15", records: 464 },
    added: 528,
    uncommitted: 0,
    last_gain: "2026-10-12",
    unclassified: 105,
    weak: 49,
    quoted: 72,
    by_direction: { hdqi: 0, opi: 0, dcp: 44, carrier_pgm: 101, lattice: 2, code_equivalence: 276, unclassified: 105 },
  };
  const text = registrySentence(registry, { ...LABELS, carrier_pgm: "Carrier / PGM", code_equivalence: "Code equivalence" });
  assert.equal(
    text,
    "The negative-results registry gained 528 records after its first committed version (Jul 15, 2026, 464 records), " +
      "the last of them on Oct 12, 2026. By direction: Code equivalence 276, Carrier / PGM 101, DCP / dihedral coset 44 " +
      "and Ternary / lattice 2. 105 match no keyword, so they count as unclassified and end no run. " +
      "Only 72 of the 528 are ever quoted in a handoff section.",
  );
  assert.match(registrySentence(null, LABELS), /not read/);
});

test("runRowHtml says which registry gain ended a run and escapes labels", () => {
  const html = runRowHtml(
    { direction: "dcp", length: 12, from_date: "2026-09-27", to_date: null, ended_by_gain: "2026-10-06", ongoing: false },
    { dcp: "DCP <b>" },
  );
  assert.ok(html.includes("DCP &lt;b&gt;"));
  assert.ok(html.includes("Sep 27, 2026"));
  assert.ok(html.includes("not committed yet"));
  assert.ok(html.includes("Oct 6, 2026"));
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

test("sparkCardsHtml escapes metric keys and labels, so no key can break the page", () => {
  const charts = [{ key: 'odd"key<x>', svg: "<svg></svg>", points: [{ date: "2026-10-01", value: 3 }] }];
  const html = sparkCardsHtml(charts);
  assert.equal((html.match(/class="ck-spark"/g) || []).length, 1);
  assert.ok(!html.includes('odd"key'));
  assert.ok(html.includes("Odd&quot;key&lt;x&gt;"));
  assert.ok(html.includes("3 on Oct 1, 2026"));
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

test("spendTotals sums the spend days, counts token days and keeps unknown totals unknown", () => {
  const totals = spendTotals({
    days: [
      { date: "2026-10-17", runs: 1, wall_seconds: null, cpu_seconds: null, negatives_added: 0, tokens: null },
      { date: "2026-10-18", runs: 3, wall_seconds: 3600, cpu_seconds: null, negatives_added: 1, tokens: null },
      { date: "2026-10-19", runs: 2, wall_seconds: 1800, cpu_seconds: null, negatives_added: 0, tokens: 5000 },
    ],
  });
  assert.deepEqual(totals, {
    days: 3,
    runs: 6,
    wall_hours: 1.5,
    cpu_hours: null,
    negatives_added: 1,
    tokens: 5000,
    token_days: 1,
    cached_share: null,
  });
  assert.deepEqual(spendTotals({ days: [] }), {
    days: 0,
    runs: 0,
    wall_hours: null,
    cpu_hours: null,
    negatives_added: 0,
    tokens: null,
    token_days: 0,
    cached_share: null,
  });
  const cached = spendTotals({ days: [{ date: "2026-10-19", tokens: 1000, tokens_uncached: 30 }, { date: "2026-10-20", tokens: null }] });
  assert.equal(cached.cached_share, 0.97);
});

test("tokenLabel says on how many days tokens were recorded and that they include cached input", () => {
  assert.equal(tokenLabel({ tokens: 5, token_days: 71, days: 76, cached_share: null }), "Codex tokens on 71 of 76 days, cached input included");
  assert.equal(tokenLabel({ tokens: 5, token_days: 71, days: 76, cached_share: 0.9712 }), "Codex tokens on 71 of 76 days, 97% of them cached input");
  assert.equal(tokenLabel({ tokens: null, token_days: 0, days: 76, cached_share: null }), "Codex tokens (none recorded)");
});

test("spendRowHtml says not recorded for wall and CPU time on days without timed commands", () => {
  const html = spendRowHtml({ date: "2026-07-06", runs: 0, wall_seconds: null, cpu_seconds: null, negatives_added: 0, tokens: 9438873 });
  assert.equal((html.match(/not recorded/g) || []).length, 2);
  assert.ok(!html.includes("0 s"));
  assert.ok(html.includes("9,438,873"));
});

test("headFigures label build-time figures with the build date and say unknown without history", () => {
  const data = {
    generated_on: "2026-10-19",
    dirty: { modified: 3, untracked: 1, total: 4 },
    commits: { days: DAYS, complete: true },
    inertia: { available: true, flags: [{}, {}] },
    coverage: { sections: 494 },
    checkpoint: { days_since_session: 3 },
  };
  const figures = headFigures({ ...data, generated_on: "2026-10-03" });
  assert.deepEqual(figures.map((f) => f.value), ["4", "6", "2", "494", "3"]);
  assert.ok(figures[1].label.includes("Oct 3, 2026"));
  assert.ok(figures[4].label.includes("Oct 3, 2026"));
  assert.ok(figures[0].label.includes("when this page was built"));
  const unknown = headFigures({ ...data, dirty: null, commits: { days: [], complete: false }, inertia: { available: false, flags: [] }, checkpoint: null });
  assert.deepEqual(unknown.map((f) => f.value), ["unknown", "unknown", "unknown", "494", "–"]);
});

test("builtHtml names the commit the build started from, not the commit that carries the page", () => {
  const html = builtHtml({ generated_on: "2026-10-19", head: HEAD });
  assert.ok(html.includes("Built Oct 19, 2026"));
  assert.ok(html.includes("starting from commit"));
  assert.ok(html.includes(`/commit/${HEAD.commit}`));
  assert.ok(html.includes("comes after it"));
  assert.ok(!builtHtml({ generated_on: "2026-10-19", head: null }).includes("commit/"));
});

test("warningsHtml escapes each warning", () => {
  assert.equal(warningsHtml([]), "");
  assert.equal(warningsHtml(["a <b> & c"]), '<p class="load-error">a &lt;b&gt; &amp; c</p>');
});

test("handoffUrl pins the head commit and its own line numbers", () => {
  assert.equal(
    handoffUrl(SECTIONS[1], HEAD),
    `https://github.com/Jaspersands/qsearch/blob/${HEAD.commit}/research/AGENT_HANDOFF.md?plain=1#L11`,
  );
  assert.equal(handoffUrl(SECTIONS[0], HEAD), null, "a section the head commit does not hold has no line to link");
  assert.equal(handoffUrl(SECTIONS[1], null), null);
});

test("sectionRowHtml escapes the heading, cues and ids and links to the pinned line", () => {
  const evil = section(9, 9, "dcp", "codex", {
    heading: '<img src=x onerror="alert(1)">',
    cues: ["<cue>"],
    first_quoted_ids: ["NEG-<X>"],
    head_line: 42,
  });
  const html = sectionRowHtml(evil, { labels: { dcp: "DCP <d>" }, head: HEAD });
  assert.ok(!html.includes("<img"));
  assert.ok(html.includes("&lt;img src=x onerror=&quot;alert(1)&quot;&gt;"));
  assert.ok(html.includes("&lt;cue&gt;"));
  assert.ok(html.includes("NEG-&lt;X&gt;"));
  assert.ok(html.includes("DCP &lt;d&gt;"));
  assert.ok(html.includes(`blob/${HEAD.commit}/research/AGENT_HANDOFF.md?plain=1#L42`));
  const unlinked = sectionRowHtml(SECTIONS[0], { labels: LABELS, head: HEAD });
  assert.ok(!unlinked.includes("<a "));
  assert.ok(unlinked.includes("none"));
});

test("commitItemHtml escapes commit subjects and links the commit", () => {
  const html = commitItemHtml({ sha: "abc12345", date: "2026-10-18", subject: "Fix <script>alert(1)</script> & co", topic: "dcp" }, LABELS);
  assert.ok(!html.includes("<script>"));
  assert.ok(html.includes("Fix &lt;script&gt;alert(1)&lt;/script&gt; &amp; co"));
  assert.ok(html.includes("/commit/abc12345"));
  assert.ok(html.includes("DCP / dihedral coset"));
});

test("checkpointHtml escapes every checkpoint string and says unknown rather than none", () => {
  const checkpoint = {
    file: ".research_checkpoint.json",
    session_date: "2026-10-16",
    days_since_session: 3,
    active_milestone: "<script>m</script>",
    latest_verified_subsystem: "<b>sub</b>",
    total_verified_subsystems: 66,
    review: { date: "2026-10-16", status: "<i>status</i>", next_decision: 'say "hi" & <go>' },
    last_commit: { sha: "1f7df578", date: "2026-10-18" },
    commits_since: 22,
    uncommitted_changes: null,
  };
  const html = checkpointHtml(checkpoint, { builtOn: "2026-10-19", complete: true });
  for (const raw of ["<script>", "<b>sub", "<i>status", "<go>"]) assert.ok(!html.includes(raw), raw);
  assert.ok(html.includes("&lt;script&gt;m&lt;/script&gt;"));
  assert.ok(html.includes("say &quot;hi&quot; &amp; &lt;go&gt;"));
  assert.ok(html.includes("unknown"));
  assert.ok(!html.includes(">none<"));
  assert.ok(checkpointHtml({ ...checkpoint, uncommitted_changes: false }, { builtOn: "2026-10-19", complete: true }).includes("none when"));
  assert.ok(checkpointHtml({ ...checkpoint, last_commit: null, commits_since: null }, { builtOn: "2026-10-19", complete: false }).includes("unknown"));
  assert.ok(checkpointHtml(null, {}).includes("No research checkpoint"));
});

test("dirtyHtml publishes totals only, labelled as read before the page was committed", () => {
  const html = dirtyHtml({ modified: 3, untracked: 2, total: 5, by_area: { formal: 9 } }, "2026-10-19");
  assert.ok(!html.includes("formal"));
  assert.ok(html.includes("Oct 19, 2026"));
  assert.ok(html.includes("before it was committed"));
  assert.match(dirtyHtml(null, "2026-10-19"), /unknown|not available/);
});

test("runPanels keeps drawing the other panels when one throws", () => {
  const drawn = [];
  const failed = [];
  runPanels(
    [
      { name: "a", draw: () => drawn.push("a") },
      { name: "b", draw: () => { throw new Error("bad metric"); } },
      { name: "c", draw: () => drawn.push("c") },
    ],
    (panel, error) => failed.push([panel.name, error.message]),
  );
  assert.deepEqual(drawn, ["a", "c"]);
  assert.deepEqual(failed, [["b", "bad metric"]]);
});
