import { escapeHtml, formatDate, formatNumber } from "./format.js";

const DAY_MS = 86400000;
const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

function dayValue(isoDate) {
  const [year, month, day] = String(isoDate).slice(0, 10).split("-").map(Number);
  return Date.UTC(year, month - 1, day);
}

export function niceMax(value) {
  if (!(value > 0)) return 1;
  const magnitude = 10 ** Math.floor(Math.log10(value));
  for (const step of [1, 2, 2.5, 5, 10]) {
    if (step * magnitude >= value) return step * magnitude;
  }
  return 10 * magnitude;
}

export function activityChart({ weeks, points = [], width = 720, height = 240 }) {
  if (!weeks || weeks.length === 0) return "";
  const pad = { top: 20, right: 56, bottom: 28, left: 36 };
  const plotWidth = width - pad.left - pad.right;
  const plotHeight = height - pad.top - pad.bottom;
  const baseline = pad.top + plotHeight;
  const start = dayValue(weeks[0].week);
  const end = Math.max(
    dayValue(weeks[weeks.length - 1].week) + 7 * DAY_MS,
    ...points.map((point) => dayValue(point.date)),
  );
  const x = (time) => pad.left + ((time - start) / (end - start)) * plotWidth;
  const visible = points.filter((point) => dayValue(point.date) >= start);
  const runMax = niceMax(Math.max(...weeks.map((week) => week.runs)));
  const lineMax = niceMax(Math.max(1, ...visible.map((point) => point.negative_results)));
  const yRuns = (value) => baseline - (value / runMax) * plotHeight;
  const yLine = (value) => baseline - (value / lineMax) * plotHeight;
  const barWidth = Math.max(1, x(start + 7 * DAY_MS) - x(start) - 3);
  const parts = [];

  const first = new Date(start);
  let tick = Date.UTC(first.getUTCFullYear(), first.getUTCMonth() + 1, 1);
  while (tick < end) {
    const tickDate = new Date(tick);
    const tx = x(tick).toFixed(1);
    parts.push(`<line class="chart-grid" x1="${tx}" x2="${tx}" y1="${pad.top}" y2="${baseline}"/>`);
    parts.push(`<text class="chart-label" x="${(x(tick) + 4).toFixed(1)}" y="${baseline + 18}">${MONTHS[tickDate.getUTCMonth()]}</text>`);
    tick = Date.UTC(tickDate.getUTCFullYear(), tickDate.getUTCMonth() + 1, 1);
  }

  for (const week of weeks) {
    const top = yRuns(week.runs);
    parts.push(
      `<rect class="chart-bar" x="${(x(dayValue(week.week)) + 1.5).toFixed(1)}" y="${top.toFixed(1)}" ` +
        `width="${barWidth.toFixed(1)}" height="${(baseline - top).toFixed(1)}">` +
        `<title>Week of ${escapeHtml(formatDate(week.week))}: ${formatNumber(week.runs)} runs</title></rect>`,
    );
  }

  if (visible.length) {
    const path = visible
      .map((point, index) => `${index === 0 ? "M" : "L"}${x(dayValue(point.date)).toFixed(1)},${yLine(point.negative_results).toFixed(1)}`)
      .join(" ");
    parts.push(`<path class="chart-line" d="${path}"/>`);
    const last = visible[visible.length - 1];
    parts.push(
      `<text class="chart-label chart-label-strong" x="${x(dayValue(last.date)).toFixed(1)}" ` +
        `y="${(yLine(last.negative_results) - 8).toFixed(1)}" text-anchor="end">${formatNumber(last.negative_results)}</text>`,
    );
    parts.push(`<text class="chart-label chart-label-line" x="${pad.left + plotWidth + 6}" y="${pad.top + 4}">${formatNumber(lineMax)}</text>`);
    parts.push(`<text class="chart-label chart-label-line" x="${pad.left + plotWidth + 6}" y="${baseline}">0</text>`);
  }

  parts.push(`<line class="chart-axis" x1="${pad.left}" x2="${pad.left + plotWidth}" y1="${baseline}" y2="${baseline}"/>`);
  parts.push(`<text class="chart-label" x="${pad.left - 6}" y="${baseline}" text-anchor="end">0</text>`);
  parts.push(`<text class="chart-label" x="${pad.left - 6}" y="${pad.top + 4}" text-anchor="end">${formatNumber(runMax)}</text>`);

  const total = weeks.reduce((sum, week) => sum + week.runs, 0);
  let label = `Experiment runs per week from ${formatDate(weeks[0].week)}: ${formatNumber(total)} runs in total.`;
  if (visible.length) label += ` Ideas ruled out grew to ${formatNumber(visible[visible.length - 1].negative_results)}.`;
  return `<svg viewBox="0 0 ${width} ${height}" role="img" aria-label="${escapeHtml(label)}">${parts.join("")}</svg>`;
}
