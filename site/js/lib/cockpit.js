import { niceMax } from "./chart.js";
import { escapeHtml, formatDate, formatNumber } from "./format.js";

const DAY_MS = 86400000;
const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

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
        isNew: (section.new_registry_ids || []).length > 0,
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

/* ---------- Inertia ---------- */

function lastNewText(lastNew) {
  if (!lastNew) return "none in the log";
  const date = lastNew.first_committed ? formatDate(lastNew.first_committed) : "not committed yet";
  const ids = lastNew.ids || [];
  if (!ids.length) return date;
  return `${date} (${ids[0]}${ids.length > 1 ? ` and ${ids.length - 1} more` : ""})`;
}

function lastSeenText(sectionsAgo) {
  if (sectionsAgo === 0) return "latest section";
  return `${plural(sectionsAgo, "section")} ago`;
}

export function inertiaRows(inertia) {
  return inertia.directions
    .map((row) => ({
      direction: row.direction,
      label: row.label,
      sections: row.sections,
      streak: row.streak,
      flag: row.flag,
      lastNew: lastNewText(row.last_new),
      lastSeen: lastSeenText(row.sections_ago),
    }))
    .sort((a, b) => Number(b.flag) - Number(a.flag) || b.streak - a.streak || b.sections - a.sections);
}

export function flaggedSentence({ threshold, flags }) {
  const rule = `${formatNumber(threshold)} or more of`;
  if (!flags.length) return `No direction has run ${rule} its own handoff sections without a new registry entry.`;
  const names = listWords(flags.map((flag) => flag.label));
  if (flags.length === 1) return `${names} has run ${rule} its own handoff sections without a new registry entry.`;
  return `${names} have each run ${rule} their own handoff sections without a new registry entry.`;
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

function sumKnown(days, field) {
  const known = days.map((day) => day[field]).filter((value) => typeof value === "number");
  return known.length ? known.reduce((sum, value) => sum + value, 0) : null;
}

export function spendTotals(spend) {
  const days = (spend && spend.days) || [];
  const cpu = sumKnown(days, "cpu_seconds");
  return {
    days: days.length,
    runs: sumKnown(days, "runs") ?? 0,
    wall_hours: (sumKnown(days, "wall_seconds") ?? 0) / 3600,
    cpu_hours: cpu === null ? null : cpu / 3600,
    negatives_added: sumKnown(days, "negatives_added") ?? 0,
    tokens: sumKnown(days, "tokens"),
  };
}
