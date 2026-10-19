import { niceMax } from "./chart.js";
import { REPO_URL, escapeHtml, formatDate, formatNumber } from "./format.js";

const DAY_MS = 86400000;
const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
const HANDOFF_PATH = "research/AGENT_HANDOFF.md";

export const AGENT_LABELS = { codex: "Codex", gemini: "Gemini", unknown: "Unknown" };

const METRIC_LABELS = {
  negative_results: "Negative results",
  results: "Results",
  experiments: "Experiments",
  blocking_findings: "Blocking findings",
  proof_debts: "Proof debts",
};

function dayValue(isoDate) {
  const [year, month, day] = String(isoDate).slice(0, 10).split("-").map(Number);
  return Date.UTC(year, month - 1, day);
}

function isoDay(time) {
  return new Date(time).toISOString().slice(0, 10);
}

function plural(count, word) {
  return `${formatNumber(count)} ${word}${count === 1 ? "" : "s"}`;
}

function listWords(items) {
  if (items.length <= 1) return items.join("");
  return `${items.slice(0, -1).join(", ")} and ${items[items.length - 1]}`;
}

export function metricLabel(key) {
  if (METRIC_LABELS[key]) return METRIC_LABELS[key];
  const words = String(key).replace(/[_-]+/g, " ").trim();
  return words.charAt(0).toUpperCase() + words.slice(1);
}

/* ---------- Small HTML pieces (every value from the data is escaped) ---------- */

export function countText(value) {
  return value === null || value === undefined ? "–" : formatNumber(value);
}

export function figureHtml(value, label) {
  return `<div><span class="figure-value">${escapeHtml(value)}</span><span class="figure-label">${escapeHtml(label)}</span></div>`;
}

// rows are [label, html]; the html must already be escaped. Rows with no value are left out.
export function factsHtml(rows) {
  return `<dl class="facts">${rows
    .filter(([, value]) => value)
    .map(([label, value]) => `<dt>${escapeHtml(label)}</dt><dd>${value}</dd>`)
    .join("")}</dl>`;
}

export function commitLinkHtml(sha, shown = sha) {
  return `<a href="${REPO_URL}/commit/${encodeURIComponent(sha)}"><code>${escapeHtml(String(shown).slice(0, 8))}</code></a>`;
}

export function warningsHtml(warnings) {
  return (warnings || []).map((warning) => `<p class="load-error">${escapeHtml(warning)}</p>`).join("");
}

// Draw each panel on its own, so one panel's error does not blank the others.
export function runPanels(panels, onError) {
  for (const panel of panels) {
    try {
      panel.draw();
    } catch (error) {
      onError(panel, error);
    }
  }
}

/* ---------- Header ---------- */

export function builtHtml(data) {
  const built = `Built ${escapeHtml(formatDate(data.generated_on))} (all dates are UTC days)`;
  if (!data.head) return `${built}.`;
  return (
    `${built}, starting from commit ${commitLinkHtml(data.head.commit || data.head.sha, data.head.sha)} ` +
    `of ${escapeHtml(formatDate(data.head.date))}. The commit that carries this page comes after it.`
  );
}

// The header figures are frozen when the page is built, so each says which moment it describes.
export function headFigures(data) {
  const built = formatDate(data.generated_on);
  const checkpoint = data.checkpoint;
  const commits = data.commits || {};
  const inertia = data.inertia || {};
  return [
    { value: data.dirty ? countText(data.dirty.total) : "unknown", label: "files uncommitted when this page was built" },
    {
      value: commits.complete ? countText(commitsInWindow(commits.days, data.generated_on, 7)) : "unknown",
      label: `commits in the 7 days to ${built}`,
    },
    { value: inertia.available ? countText(inertia.flags.length) : "unknown", label: "directions flagged for inertia" },
    { value: countText(data.coverage.sections), label: "handoff sections read" },
    { value: checkpoint ? countText(checkpoint.days_since_session) : "–", label: `days from the last checkpoint session to ${built}` },
  ];
}

/* ---------- Commits ---------- */

export function fillDays(days, to) {
  if (!days || days.length === 0) return [];
  const byDate = new Map(days.map((day) => [day.date, day]));
  const end = Math.max(dayValue(days[days.length - 1].date), to ? dayValue(to) : 0);
  const filled = [];
  for (let time = dayValue(days[0].date); time <= end; time += DAY_MS) {
    const date = isoDay(time);
    filled.push(byDate.get(date) || { date, count: 0, topics: {}, commits: [] });
  }
  return filled;
}

export function commitsInWindow(days, endDate, n) {
  const end = dayValue(endDate);
  const start = end - (n - 1) * DAY_MS;
  return (days || []).reduce((sum, day) => {
    const time = dayValue(day.date);
    return time >= start && time <= end ? sum + day.count : sum;
  }, 0);
}

export function topicTotals(days, endDate, n) {
  const end = dayValue(endDate);
  const start = end - (n - 1) * DAY_MS;
  const totals = new Map();
  for (const day of days || []) {
    const time = dayValue(day.date);
    const recent = time >= start && time <= end;
    for (const [topic, count] of Object.entries(day.topics)) {
      const row = totals.get(topic) || { topic, recent: 0, all: 0 };
      row.all += count;
      if (recent) row.recent += count;
      totals.set(topic, row);
    }
  }
  return [...totals.values()].sort((a, b) => b.all - a.all || b.recent - a.recent || a.topic.localeCompare(b.topic));
}

export function latestCommits(days, n) {
  const commits = [];
  for (let i = (days || []).length - 1; i >= 0 && commits.length < n; i -= 1) {
    for (const commit of days[i].commits) {
      if (commits.length >= n) break;
      commits.push({ ...commit, date: days[i].date });
    }
  }
  return commits;
}

export function commitItemHtml(commit, labels = {}) {
  return `<li>
        <time datetime="${escapeHtml(commit.date)}">${escapeHtml(formatDate(commit.date))}</time>
        <div>${escapeHtml(commit.subject)}<p class="small">${commitLinkHtml(commit.sha)} · ${escapeHtml(labels[commit.topic] || commit.topic)}</p></div>
      </li>`;
}

function topicText(topics, labels) {
  return Object.entries(topics)
    .sort((a, b) => b[1] - a[1] || String(labels[a[0]] || a[0]).localeCompare(String(labels[b[0]] || b[0])))
    .map(([topic, count]) => `${labels[topic] || topic} ${formatNumber(count)}`)
    .join(", ");
}

export function commitChart({ days, labels = {}, width = 720, height = 200 }) {
  if (!days || days.length === 0) return "";
  const pad = { top: 16, right: 12, bottom: 28, left: 36 };
  const plotWidth = width - pad.left - pad.right;
  const plotHeight = height - pad.top - pad.bottom;
  const baseline = pad.top + plotHeight;
  const slot = plotWidth / days.length;
  const barWidth = Math.min(24, Math.max(1, slot - 2));
  const max = niceMax(Math.max(...days.map((day) => day.count)));
  const parts = [];

  days.forEach((day, i) => {
    if (!day.date.endsWith("-01")) return;
    const tx = (pad.left + i * slot).toFixed(1);
    parts.push(`<line class="chart-grid" x1="${tx}" x2="${tx}" y1="${pad.top}" y2="${baseline}"/>`);
    parts.push(`<text class="chart-label" x="${(pad.left + i * slot + 4).toFixed(1)}" y="${baseline + 18}">${MONTHS[Number(day.date.slice(5, 7)) - 1]}</text>`);
  });

  days.forEach((day, i) => {
    if (day.count > 0) {
      const top = baseline - (day.count / max) * plotHeight;
      parts.push(
        `<rect class="chart-bar" x="${(pad.left + i * slot + (slot - barWidth) / 2).toFixed(1)}" y="${top.toFixed(1)}" ` +
          `width="${barWidth.toFixed(1)}" height="${(baseline - top).toFixed(1)}"/>`,
      );
    }
  });

  days.forEach((day, i) => {
    const what = day.count > 0 ? `${plural(day.count, "commit")} (${topicText(day.topics, labels)})` : "no commits";
    parts.push(
      `<rect class="chart-hit" x="${(pad.left + i * slot).toFixed(1)}" y="${pad.top}" width="${slot.toFixed(1)}" height="${plotHeight}">` +
        `<title>${escapeHtml(`${formatDate(day.date)}: ${what}`)}</title></rect>`,
    );
  });

  parts.push(`<line class="chart-axis" x1="${pad.left}" x2="${pad.left + plotWidth}" y1="${baseline}" y2="${baseline}"/>`);
  parts.push(`<text class="chart-label" x="${pad.left - 6}" y="${baseline}" text-anchor="end">0</text>`);
  parts.push(`<text class="chart-label" x="${pad.left - 6}" y="${pad.top + 4}" text-anchor="end">${formatNumber(max)}</text>`);

  const total = days.reduce((sum, day) => sum + day.count, 0);
  const label =
    `Commits per day from ${formatDate(days[0].date)} to ${formatDate(days[days.length - 1].date)}: ` +
    `${plural(total, "commit")} in total.`;
  return `<svg viewBox="0 0 ${width} ${height}" role="img" aria-label="${escapeHtml(label)}">${parts.join("")}</svg>`;
}

/* ---------- Handoff sections ---------- */

export function sectionDate(section) {
  return section.first_committed ? formatDate(section.first_committed) : "not committed yet";
}

export function recentSections(sections, { direction = "", agent = "", limit = Infinity } = {}) {
  return sections
    .filter((section) => (!direction || section.direction === direction) && (!agent || section.agent === agent))
    .sort((a, b) => b.order - a.order)
    .slice(0, limit);
}

// A link to the section's line in the commit the build started from. Line numbers come from that
// commit's own copy of the handoff, so they do not drift when the next handoff commit lands.
export function handoffUrl(section, head) {
  const commit = head && (head.commit || head.sha);
  if (!commit || !section.head_line) return null;
  const path = HANDOFF_PATH.split("/").map(encodeURIComponent).join("/");
  return `${REPO_URL}/blob/${encodeURIComponent(commit)}/${path}?plain=1#L${Number(section.head_line)}`;
}

export function sectionRowHtml(section, { labels = {}, head = null } = {}) {
  const url = handoffUrl(section, head);
  const cues = (section.cues || []).length ? `<span class="cues">${escapeHtml(section.cues.join(" · "))}</span>` : "";
  const weak = section.direction_weak ? '<span class="cues">weak match</span>' : "";
  const ids = (section.first_quoted_ids || []).length
    ? section.first_quoted_ids.map(escapeHtml).join("<br>")
    : '<span class="muted">none</span>';
  const heading = url ? `<a href="${escapeHtml(url)}">${escapeHtml(section.heading)}</a>` : escapeHtml(section.heading);
  return `<tr>
    <td data-label="First committed" class="inline-sm">${escapeHtml(sectionDate(section))}</td>
    <td data-label="Agent" class="inline-sm">${escapeHtml(AGENT_LABELS[section.agent] || section.agent)}${cues}</td>
    <td data-label="Direction" class="inline-sm">${escapeHtml(labels[section.direction] || section.direction)}${weak}</td>
    <td class="heading no-label">${heading}</td>
    <td data-label="Registry ids first quoted here" class="ids">${ids}</td>
  </tr>`;
}

export function rugLayout({ sections, groups, key, width = 720, labelWidth = 180, rowHeight = 26, axisHeight = 24 }) {
  const count = Math.max(1, sections.length);
  const plotWidth = width - labelWidth;
  const slot = plotWidth / count;
  const x = (order) => labelWidth + (order + 0.5) * slot;
  const chronological = [...sections].sort((a, b) => a.order - b.order);
  const rows = groups.map((group, i) => {
    const ticks = chronological
      .filter((section) => section[key] === group.id)
      .map((section) => ({
        x: x(section.order),
        index: section.index,
        order: section.order,
        // first committed on a day the registry gained a record in the section's direction
        isNew: Boolean(section.registry_day),
        section,
      }));
    return { id: group.id, label: group.label, count: ticks.length, top: i * rowHeight, ticks };
  });
  const months = [];
  let previous = "";
  for (const section of chronological) {
    if (!section.first_committed) continue;
    const month = section.first_committed.slice(0, 7);
    if (month !== previous) {
      months.push({ x: labelWidth + section.order * slot, label: MONTHS[Number(month.slice(5, 7)) - 1] });
      previous = month;
    }
  }
  return { width, height: groups.length * rowHeight + axisHeight, labelWidth, rowHeight, rows, months };
}

export function rugChart(layout, ariaLabel) {
  const { width, height, labelWidth, rowHeight, rows, months } = layout;
  const plotBottom = rows.length * rowHeight;
  const parts = [];
  for (const month of months) {
    const mx = month.x.toFixed(1);
    parts.push(`<line class="chart-grid" x1="${mx}" x2="${mx}" y1="0" y2="${plotBottom}"/>`);
    parts.push(`<text class="chart-label" x="${(month.x + 4).toFixed(1)}" y="${plotBottom + 16}">${month.label}</text>`);
  }
  for (const row of rows) {
    const base = row.top + rowHeight - 5;
    const middle = row.top + rowHeight / 2 + 4;
    parts.push(`<text class="chart-label rug-label" x="0" y="${middle}">${escapeHtml(row.label)}</text>`);
    parts.push(`<text class="chart-label rug-count" x="${labelWidth - 12}" y="${middle}" text-anchor="end">${formatNumber(row.count)}</text>`);
    parts.push(`<line class="rug-row" x1="${labelWidth}" x2="${width}" y1="${base}" y2="${base}"/>`);
    for (const tick of row.ticks) {
      const tx = tick.x.toFixed(1);
      const top = tick.isNew ? row.top + 3 : row.top + 9;
      parts.push(`<line class="rug-tick${tick.isNew ? " rug-new" : ""}" x1="${tx}" x2="${tx}" y1="${top}" y2="${base}"/>`);
    }
  }
  return `<svg viewBox="0 0 ${width} ${height}" role="img" aria-label="${escapeHtml(ariaLabel)}">${parts.join("")}</svg>`;
}

export function nearestTick(ticks, x, maxDist) {
  let best = -1;
  let bestDist = maxDist;
  ticks.forEach((tick, i) => {
    const dist = Math.abs(tick.x - x);
    if (dist <= bestDist) {
      best = i;
      bestDist = dist;
    }
  });
  return best;
}

/* ---------- Inertia and registry growth ---------- */

function lastGainText(lastGain, baseline) {
  if (!lastGain) return baseline ? `none after ${formatDate(baseline.date)}` : "none recorded";
  const records = plural(lastGain.records, "record");
  return lastGain.date ? `${formatDate(lastGain.date)} (${records})` : `not committed yet (${records})`;
}

function lastSeenText(sectionsAgo) {
  if (sectionsAgo === 0) return "latest section";
  return `${plural(sectionsAgo, "section")} ago`;
}

export function inertiaRows(inertia, baseline = null) {
  return inertia.directions
    .map((row) => ({
      direction: row.direction,
      label: row.label,
      sections: row.sections,
      streak: row.streak,
      flag: row.flag,
      gained: row.gained,
      lastGain: lastGainText(row.last_gain, baseline),
      lastSeen: lastSeenText(row.sections_ago),
    }))
    .sort((a, b) => Number(b.flag) - Number(a.flag) || b.streak - a.streak || b.sections - a.sections);
}

export function flaggedSentence({ threshold, flags, available = true }) {
  if (!available) {
    return "Inertia is not measured in this build: it needs the full git history of the handoff and of the registry.";
  }
  const rule = `${formatNumber(threshold)} or more of`;
  const since = "handoff sections since the registry last gained a record in";
  if (!flags.length) return `No direction has had ${rule} its own ${since} its direction.`;
  const names = listWords(flags.map((flag) => flag.label));
  if (flags.length === 1) return `${names} has had ${rule} its own ${since} its direction.`;
  return `${names} have each had ${rule} their own ${since} their direction.`;
}

export function registrySentence(registry, labels = {}) {
  if (!registry) return "Registry growth was not read: this build had no full git history of the registry.";
  const baseline = registry.baseline;
  const parts = [
    `The negative-results registry gained ${plural(registry.added, "record")} after its first committed version ` +
      `(${formatDate(baseline.date)}, ${plural(baseline.records, "record")})` +
      (registry.last_gain ? `, the last of them on ${formatDate(registry.last_gain)}.` : "."),
  ];
  if (registry.uncommitted) parts.push(`${plural(registry.uncommitted, "more record")} are in the working tree, not committed yet.`);
  const named = Object.entries(registry.by_direction || {})
    .filter(([id, n]) => id !== "unclassified" && n > 0)
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .map(([id, n]) => `${labels[id] || id} ${formatNumber(n)}`);
  if (named.length) parts.push(`By direction: ${listWords(named)}.`);
  if (registry.unclassified) {
    parts.push(`${formatNumber(registry.unclassified)} match no keyword, so they count as unclassified and end no run.`);
  }
  if (typeof registry.quoted === "number") {
    const total = registry.added + (registry.uncommitted || 0);
    const only = registry.quoted * 2 < total ? "Only " : "";
    parts.push(`${only}${formatNumber(registry.quoted)} of the ${formatNumber(total)} are ever quoted in a handoff section.`);
  }
  return parts.join(" ");
}

export function runRowHtml(run, labels = {}) {
  const day = (date) => (date ? formatDate(date) : "not committed yet");
  let ended = "still running";
  if (!run.ongoing) ended = run.ended_by_gain ? formatDate(run.ended_by_gain) : "records not committed yet";
  return `<tr>
          <td>${escapeHtml(labels[run.direction] || run.direction)}</td>
          <td data-label="Sections" class="num">${formatNumber(run.length)}</td>
          <td data-label="From">${escapeHtml(day(run.from_date))}</td>
          <td data-label="To">${escapeHtml(day(run.to_date))}</td>
          <td data-label="Ended by a registry gain on">${escapeHtml(ended)}</td>
        </tr>`;
}

/* ---------- Metrics ---------- */

export function sparkline({ points, key, width = 240, height = 64 }) {
  const series = (points || [])
    .filter((point) => typeof point.metrics[key] === "number")
    .map((point) => ({ date: point.date, value: point.metrics[key] }));
  if (!series.length) return { svg: "", points: [] };
  const pad = { top: 8, right: 52, bottom: 6, left: 6 };
  const plotWidth = width - pad.left - pad.right;
  const baseline = height - pad.bottom;
  const start = dayValue(series[0].date);
  const span = dayValue(series[series.length - 1].date) - start || 1;
  const max = niceMax(Math.max(...series.map((point) => point.value)));
  const placed = series.map((point) => ({
    ...point,
    x: pad.left + ((dayValue(point.date) - start) / span) * plotWidth,
    y: baseline - (point.value / max) * (baseline - pad.top),
  }));
  const path = placed.map((point, i) => `${i === 0 ? "M" : "L"}${point.x.toFixed(1)},${point.y.toFixed(1)}`).join(" ");
  const last = placed[placed.length - 1];
  const first = placed[0];
  const label = metricLabel(key);
  const parts = [
    `<line class="chart-grid" x1="${pad.left}" x2="${pad.left + plotWidth}" y1="${baseline}" y2="${baseline}"/>`,
    `<path class="chart-line" d="${path}"/>`,
    `<circle class="spark-dot" cx="${last.x.toFixed(1)}" cy="${last.y.toFixed(1)}" r="4"/>`,
    `<text class="chart-label chart-label-strong" x="${(last.x + 9).toFixed(1)}" y="${(last.y + 4).toFixed(1)}">${formatNumber(last.value)}</text>`,
  ];
  const aria =
    `${label}: ${formatNumber(first.value)} on ${formatDate(first.date)}, ` +
    `${formatNumber(last.value)} on ${formatDate(last.date)}.`;
  return {
    svg: `<svg viewBox="0 0 ${width} ${height}" role="img" aria-label="${escapeHtml(aria)}">${parts.join("")}</svg>`,
    points: placed,
  };
}

export function readoutText(point) {
  return `${formatNumber(point.value)} on ${formatDate(point.date)}`;
}

// One card per chart. Cards are found again by position (.ck-spark, .ck-readout, .ck-spark-chart),
// never by a selector built from a metric key, so no key can break the page.
export function sparkCardsHtml(charts) {
  return charts
    .map(
      (chart) => `<div class="ck-spark">
        <h3>${escapeHtml(metricLabel(chart.key))}</h3>
        <p class="small ck-readout">${escapeHtml(readoutText(chart.points[chart.points.length - 1]))}</p>
        <div class="ck-spark-chart">${chart.svg}</div>
      </div>`,
    )
    .join("");
}

/* ---------- Working tree and checkpoint ---------- */

export function dirtyHtml(dirty, builtOn) {
  if (!dirty) return '<p class="load-error">Unknown: git status was not available when this page was built.</p>';
  return (
    factsHtml([
      ["Changed tracked files", formatNumber(dirty.modified)],
      ["Untracked files", formatNumber(dirty.untracked)],
      ["Total", formatNumber(dirty.total)],
    ]) +
    `<p class="small">Counted with <code>git status</code> when this page was built (${escapeHtml(formatDate(builtOn))}), ` +
    "before it was committed, so the counts include the files that the page's own commit then added. " +
    "File and folder names are left out on purpose.</p>"
  );
}

function localEditsText(changes) {
  if (changes === null || changes === undefined) return "unknown: git status was not available";
  return changes ? "yes, the file had local changes when this page was built" : "none when this page was built";
}

export function checkpointHtml(checkpoint, { builtOn, complete = true } = {}) {
  if (!checkpoint) return '<p class="load-error">No research checkpoint file was found in this checkout.</p>';
  const review = checkpoint.review || {};
  const last = checkpoint.last_commit;
  const ago = checkpoint.days_since_session;
  let lastCommitted = complete ? "not in the git history" : "unknown: this checkout has no full git history";
  if (last) {
    lastCommitted = `${escapeHtml(formatDate(last.date))} in ${commitLinkHtml(last.sha)}`;
    if (typeof checkpoint.commits_since === "number") lastCommitted += `; ${plural(checkpoint.commits_since, "commit")} since`;
  }
  return (
    factsHtml([
      ["File", `<code>${escapeHtml(checkpoint.file)}</code>`],
      [
        "Session",
        checkpoint.session_date
          ? `${escapeHtml(formatDate(checkpoint.session_date))}${
              typeof ago === "number" ? ` (${plural(ago, "day")} before the build on ${escapeHtml(formatDate(builtOn))})` : ""
            }`
          : "",
      ],
      ["Active milestone", escapeHtml(checkpoint.active_milestone || "")],
      ["Latest verified subsystem", checkpoint.latest_verified_subsystem ? `<code>${escapeHtml(checkpoint.latest_verified_subsystem)}</code>` : ""],
      ["Verified subsystems", checkpoint.total_verified_subsystems === null ? "" : escapeHtml(countText(checkpoint.total_verified_subsystems))],
      ["Review", review.status ? `${escapeHtml(review.status)}${review.date ? ` (${escapeHtml(formatDate(review.date))})` : ""}` : ""],
      ["Next decision", escapeHtml(review.next_decision || "")],
      ["Last committed", lastCommitted],
      ["Uncommitted edits", escapeHtml(localEditsText(checkpoint.uncommitted_changes))],
    ]) +
    '<p class="small">Agents edit this file to record the state of a research session. No code reads it, so its session date shows when a checkpoint was last recorded, not when work last happened.</p>'
  );
}

/* ---------- Spend ---------- */

export function formatDuration(seconds) {
  if (typeof seconds !== "number") return "not recorded";
  if (seconds < 90) return `${formatNumber(Math.round(seconds))} s`;
  if (seconds < 90 * 60) return `${formatNumber(Math.round(seconds / 60))} min`;
  return `${formatNumber(Math.round(seconds / 360) / 10)} h`;
}

// Three significant figures with a word, so a ten-digit token total fits a figure box.
export function compactCount(value) {
  const n = Number(value);
  if (Math.abs(n) < 10000) return formatNumber(n);
  const units = [[1e3, "thousand"], [1e6, "million"], [1e9, "billion"]];
  for (const [i, [size, word]] of units.entries()) {
    const scaled = Number((n / size).toPrecision(3));
    // 999,950 rounds to 1000 thousand; move up a unit instead.
    if (Math.abs(scaled) < 1000 || i === units.length - 1) return `${scaled} ${word}`;
  }
}

function known(days, field) {
  return days.map((day) => day[field]).filter((value) => typeof value === "number");
}

function sumKnown(days, field) {
  const values = known(days, field);
  return values.length ? values.reduce((sum, value) => sum + value, 0) : null;
}

export function spendTotals(spend) {
  const days = (spend && spend.days) || [];
  const cpu = sumKnown(days, "cpu_seconds");
  const wall = sumKnown(days, "wall_seconds");
  // The cached share needs both counts on the same days; the spend summary may not carry them.
  const paired = days.filter((day) => typeof day.tokens === "number" && typeof day.tokens_uncached === "number");
  const pairedTokens = paired.reduce((sum, day) => sum + day.tokens, 0);
  const pairedUncached = paired.reduce((sum, day) => sum + day.tokens_uncached, 0);
  return {
    days: days.length,
    runs: sumKnown(days, "runs") ?? 0,
    wall_hours: wall === null ? null : wall / 3600,
    cpu_hours: cpu === null ? null : cpu / 3600,
    negatives_added: sumKnown(days, "negatives_added") ?? 0,
    tokens: sumKnown(days, "tokens"),
    token_days: known(days, "tokens").length,
    cached_share: pairedTokens > 0 ? (pairedTokens - pairedUncached) / pairedTokens : null,
  };
}

export function tokenLabel(totals) {
  if (totals.tokens === null) return "Codex tokens (none recorded)";
  const days = `on ${formatNumber(totals.token_days)} of ${plural(totals.days, "day")}`;
  if (typeof totals.cached_share === "number") return `Codex tokens ${days}, ${Math.round(totals.cached_share * 100)}% of them cached input`;
  return `Codex tokens ${days}, cached input included`;
}

export function spendRowHtml(day) {
  return `<tr>
        <td>${escapeHtml(formatDate(day.date))}</td>
        <td class="num" data-label="Experiment runs">${countText(day.runs)}</td>
        <td class="num" data-label="Wall time">${escapeHtml(formatDuration(day.wall_seconds))}</td>
        <td class="num" data-label="CPU time">${escapeHtml(formatDuration(day.cpu_seconds))}</td>
        <td class="num" data-label="Negatives added">${countText(day.negatives_added)}</td>
        <td class="num" data-label="Tokens">${typeof day.tokens === "number" ? countText(day.tokens) : "not recorded"}</td>
      </tr>`;
}
