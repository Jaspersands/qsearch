import { escapeHtml } from "./format.js";

export const STAGES = ["hypothesis", "structure", "classical attack", "proof gate", "separation"];
const SHORT_STAGES = ["H", "S", "A", "P", "?"];
const PROOF_GATE = 3;
const LAST = STAGES.length - 1;
const TOP = 30;
const METER_GAP = 30;

function clampStage(stage) {
  const value = Number(stage);
  return Number.isFinite(value) ? Math.max(0, Math.min(PROOF_GATE, Math.trunc(value))) : 0;
}

/** Where each track's wire runs and ends, from its snapshot stage and tone. */
export function wirePlan(tracks) {
  return tracks.map((track) => {
    const label = track.short_title || track.title;
    const stage = clampStage(track.stage);
    if (track.tone === "active") return { label, active: true, solidTo: stage, endsAt: null };
    const end = Math.min(stage + 1, PROOF_GATE);
    return { label, active: false, solidTo: end, endsAt: end };
  });
}

export function aliveAt(wire, gate) {
  return wire.active || gate <= wire.endsAt;
}

export function wireExtents(plan, gateYs, width) {
  const margin = width < 100 ? 12 : 22;
  const span = width - 2 * margin;
  return plan.map((wire, i) => ({
    x: plan.length === 1 ? width / 2 : margin + (i * span) / (plan.length - 1),
    end: wire.active ? gateYs[LAST] : gateYs[wire.endsAt] + METER_GAP,
  }));
}

function meter(x, top, w = 24, h = 20) {
  const base = top + h - 5;
  const r = w / 2 - 5;
  return (
    `<g class="meter"><rect x="${x - w / 2}" y="${top}" width="${w}" height="${h}" rx="2"/>` +
    `<path d="M ${x - r} ${base} A ${r} ${r} 0 0 1 ${x + r} ${base}"/>` +
    `<line x1="${x}" y1="${base}" x2="${x + r - 2}" y2="${top + 5}"/></g>`
  );
}

/** Vertical circuit for the home page gutter. */
export function circuitSvg({ plan, gateYs, height, width = 150 }) {
  const extents = wireExtents(plan, gateYs, width);
  const narrow = width < 100;
  const labels = narrow ? SHORT_STAGES : [...STAGES.slice(0, LAST), "?"];
  const gatePad = narrow ? 9 : 14;
  const parts = [];

  plan.forEach((wire, i) => {
    const { x, end } = extents[i];
    const solidEnd = wire.active ? gateYs[wire.solidTo] : end;
    if (!narrow) parts.push(`<text class="wire-label" x="${x}" y="${TOP - 12}">${escapeHtml(wire.label)}</text>`);
    parts.push(`<line class="wire" x1="${x}" x2="${x}" y1="${TOP}" y2="${solidEnd}"/>`);
    if (wire.active) parts.push(`<line class="wire wire-dash" x1="${x}" x2="${x}" y1="${solidEnd}" y2="${end}"/>`);
    parts.push(`<line class="wire-live" data-wire="${i}" x1="${x}" x2="${x}" y1="${TOP}" y2="${TOP}"/>`);
    if (!wire.active) parts.push(meter(x, end));
  });

  STAGES.forEach((_, gate) => {
    const xs = plan.map((wire, i) => (aliveAt(wire, gate) ? extents[i].x : null)).filter((x) => x !== null);
    if (!xs.length) return;
    const left = Math.min(...xs) - gatePad;
    const boxWidth = Math.max(...xs) + gatePad - left;
    const y = gateYs[gate];
    parts.push(
      `<g class="gate" data-gate="${gate}"><rect x="${left}" y="${y - 12}" width="${boxWidth}" height="24" rx="2"/>` +
        `<text x="${left + boxWidth / 2}" y="${y + 1}">${labels[gate]}</text></g>`,
    );
  });

  const firstActive = plan.findIndex((wire) => wire.active);
  if (firstActive !== -1) parts.push(`<circle class="circuit-dot" r="4.5" cx="${extents[firstActive].x}" cy="${TOP}"/>`);
  return `<svg viewBox="0 0 ${width} ${height}" aria-hidden="true">${parts.join("")}</svg>`;
}

/** Horizontal strip for the other pages: the same plan as a compact progress map. */
export function circuitStrip({ plan, width, height = 64 }) {
  const x0 = 72;
  const x4 = width - 20;
  const gx = (gate) => x0 + (gate * (x4 - x0)) / LAST;
  const rowY = (i) => 24 + i * 16;
  const parts = [];

  STAGES.forEach((name, gate) => {
    parts.push(`<line class="strip-tick" x1="${gx(gate)}" x2="${gx(gate)}" y1="16" y2="${height - 2}"/>`);
    parts.push(`<text class="strip-stage" x="${gx(gate)}" y="10">${name}</text>`);
  });

  plan.forEach((wire, i) => {
    const y = rowY(i);
    parts.push(`<text class="wire-label strip-label" x="0" y="${y + 3}">${escapeHtml(wire.label)}</text>`);
    if (wire.active) {
      parts.push(`<line class="wire wire-strong" x1="${x0 - 8}" x2="${gx(wire.solidTo)}" y1="${y}" y2="${y}"/>`);
      parts.push(`<line class="wire wire-dash" x1="${gx(wire.solidTo)}" x2="${x4 - 8}" y1="${y}" y2="${y}"/>`);
      parts.push(`<g class="strip-q"><rect x="${x4 - 8}" y="${y - 7}" width="16" height="14" rx="2"/><text x="${x4}" y="${y + 1}">?</text></g>`);
    } else {
      const end = gx(wire.endsAt);
      parts.push(`<line class="wire wire-strong" x1="${x0 - 8}" x2="${end - 8}" y1="${y}" y2="${y}"/>`);
      parts.push(meter(end, y - 6, 16, 12));
    }
  });
  return `<svg viewBox="0 0 ${width} ${height}" aria-hidden="true">${parts.join("")}</svg>`;
}
