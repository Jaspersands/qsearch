import { SNAPSHOT_PATH, initCircuitStrip, initFooter, loadJson, setText, showLoadError } from "./common.js";
import { escapeHtml, formatNumber, repoUrl } from "./lib/format.js";
import { filterRecords, recordIdFromHash } from "./lib/negatives.js";
import { TRACK_COLORS, nearestIndex, projectPoints, trackOf } from "./lib/map.js";

const DATA_PATH = "site/data/negatives.json";
const MAP_PATH = "site/data/negative_map.json";
const MAP_PAD = 24;
const PAGE_SIZE = 40;

const state = { records: [], query: "", tag: "", shown: PAGE_SIZE, matchIds: new Set() };
const map = { points: [], regions: [], screen: [], hover: -1 };
const rowsEl = document.getElementById("nr-rows");
const tagsEl = document.getElementById("nr-tags");
const searchEl = document.getElementById("nr-search");
const moreEl = document.getElementById("nr-more");

function fileLink(path) {
  return `<a href="${repoUrl(path)}"><code>${escapeHtml(path)}</code></a>`;
}

function recordRow(record) {
  const facts = [
    ["Why it failed", escapeHtml(record.reason)],
    ["Lesson", escapeHtml(record.lesson)],
    ["Source", record.source_path ? fileLink(record.source_path) : `<code>${escapeHtml(record.source)}</code>`],
    ["Derivation", record.derivation_path ? fileLink(record.derivation_path) : ""],
    ["Data", record.artifact_path ? fileLink(record.artifact_path) : ""],
    ["Review", escapeHtml(record.review_status)],
  ];
  const list = facts
    .filter(([, value]) => value)
    .map(([label, value]) => `<dt>${label}</dt><dd>${value}</dd>`)
    .join("");
  return `<details class="row" id="${escapeHtml(record.id)}" data-id="${escapeHtml(record.id)}">
    <summary>
      <span class="row-title mono">${escapeHtml(record.id)}</span>
      <span class="row-summary clamp">${escapeHtml(record.claim)}</span>
    </summary>
    <div class="row-body">
      <dl class="facts">${list}</dl>
      <p class="small"><a href="#${encodeURIComponent(record.id)}">Link to this result</a></p>
    </div>
  </details>`;
}

function render() {
  const matches = filterRecords(state.records, state);
  state.matchIds = new Set(matches.map((record) => record.id));
  const visible = matches.slice(0, state.shown);
  rowsEl.innerHTML = visible.map(recordRow).join("");
  const filtered = matches.length !== state.records.length;
  setText(
    "nr-count",
    `Showing ${formatNumber(visible.length)} of ${formatNumber(matches.length)}` +
      (filtered ? ` matching results (${formatNumber(state.records.length)} in total)` : " results"),
  );
  moreEl.hidden = visible.length >= matches.length;
  drawMap();
}

/* ---------- Map ---------- */

const mapEl = document.getElementById("nr-map");
const tipEl = document.getElementById("nr-map-tip");

function sizeMap() {
  if (!map.points.length) return;
  const ratio = window.devicePixelRatio || 1;
  mapEl.width = Math.round(mapEl.clientWidth * ratio);
  mapEl.height = Math.round(mapEl.clientHeight * ratio);
  mapEl.getContext("2d").setTransform(ratio, 0, 0, ratio, 0, 0);
  map.screen = projectPoints(map.points, mapEl.clientWidth, mapEl.clientHeight, MAP_PAD);
  drawMap();
}

function drawMap() {
  if (!map.points.length || !map.screen.length) return;
  const ctx = mapEl.getContext("2d");
  const width = mapEl.clientWidth;
  const height = mapEl.clientHeight;
  ctx.clearRect(0, 0, width, height);
  const filtering = state.matchIds.size !== state.records.length;
  // Draw dimmed points first so matches sit on top.
  for (const pass of [false, true]) {
    map.points.forEach((point, i) => {
      const matched = state.matchIds.has(point.id);
      if (matched !== pass) return;
      ctx.globalAlpha = matched ? 0.85 : 0.12;
      ctx.fillStyle = TRACK_COLORS[point.track];
      ctx.beginPath();
      ctx.arc(map.screen[i][0], map.screen[i][1], matched && filtering ? 3.2 : 2.6, 0, 2 * Math.PI);
      ctx.fill();
    });
  }
  ctx.globalAlpha = 1;
  ctx.font = "600 13px 'Schibsted Grotesk', sans-serif";
  ctx.textAlign = "center";
  ctx.lineJoin = "round";
  for (const region of map.regions) {
    if (!region.label) continue;
    const [x, y] = projectPoints([region], width, height, MAP_PAD)[0];
    ctx.lineWidth = 4;
    ctx.strokeStyle = "rgba(255, 255, 255, 0.92)";
    ctx.strokeText(region.label, x, y);
    ctx.fillStyle = "#111111";
    ctx.fillText(region.label, x, y);
  }
  if (map.hover !== -1) {
    const [x, y] = map.screen[map.hover];
    ctx.beginPath();
    ctx.arc(x, y, 7, 0, 2 * Math.PI);
    ctx.strokeStyle = "#111111";
    ctx.lineWidth = 1.2;
    ctx.stroke();
  }
}

function pointAt(event, maxDist) {
  const rect = mapEl.getBoundingClientRect();
  return nearestIndex(map.screen, event.clientX - rect.left, event.clientY - rect.top, (i) => state.matchIds.has(map.points[i].id), maxDist);
}

function showTip(index) {
  if (index === -1) {
    tipEl.hidden = true;
    return;
  }
  const point = map.points[index];
  tipEl.innerHTML = `<code>${escapeHtml(point.id)}</code>${escapeHtml(point.claim)}`;
  tipEl.hidden = false;
  const [x, y] = map.screen[index];
  const left = Math.min(x + 14, mapEl.clientWidth - tipEl.offsetWidth - 4);
  const below = y + 14 + tipEl.offsetHeight <= mapEl.clientHeight;
  tipEl.style.left = `${Math.max(4, left)}px`;
  tipEl.style.top = `${below ? y + 14 : y - tipEl.offsetHeight - 14}px`;
}

function selectRecord(id) {
  const matches = filterRecords(state.records, state);
  const index = matches.findIndex((record) => record.id === id);
  history.replaceState(null, "", `#${encodeURIComponent(id)}`);
  if (index === -1) {
    openFromHash();
    return;
  }
  state.shown = Math.max(state.shown, Math.ceil((index + 1) / PAGE_SIZE) * PAGE_SIZE);
  render();
  const row = document.getElementById(id);
  if (row) {
    row.open = true;
    row.scrollIntoView({ block: "start", behavior: "smooth" });
  }
}

function initMap(layout) {
  const byId = new Map(state.records.map((record) => [record.id, record]));
  map.points = layout.points
    .filter((point) => byId.has(point.id))
    .map((point) => {
      const record = byId.get(point.id);
      return { ...point, claim: record.claim, track: trackOf(record.tags) };
    });
  map.regions = layout.regions;
  const missing = state.records.length - map.points.length;
  if (missing > 0) {
    setText("nr-map-missing", ` ${formatNumber(missing)} newer ${missing === 1 ? "record isn't" : "records aren't"} on the map yet.`);
  }
  document.getElementById("map").hidden = false;
  mapEl.addEventListener("mousemove", (event) => {
    const index = pointAt(event, 10);
    if (index !== map.hover) {
      map.hover = index;
      drawMap();
    }
    mapEl.style.cursor = index === -1 ? "crosshair" : "pointer";
    showTip(index);
  });
  mapEl.addEventListener("mouseleave", () => {
    map.hover = -1;
    showTip(-1);
    drawMap();
  });
  mapEl.addEventListener("click", (event) => {
    const index = pointAt(event, 14);
    if (index !== -1) selectRecord(map.points[index].id);
  });
  let timer;
  window.addEventListener("resize", () => {
    clearTimeout(timer);
    timer = setTimeout(sizeMap, 120);
  });
  sizeMap();
  if (location.hash === "#map") document.getElementById("map").scrollIntoView({ block: "start" });
}

function setTag(tag) {
  state.tag = tag;
  for (const chip of tagsEl.querySelectorAll("button[data-tag]")) {
    chip.setAttribute("aria-pressed", String(chip.dataset.tag === tag));
  }
}

function renderTags(tags) {
  const chip = (id, label, count) =>
    `<button type="button" class="chip" data-tag="${escapeHtml(id)}" aria-pressed="${id === state.tag}">` +
    (TRACK_COLORS[id] ? `<span class="swatch" style="background:${TRACK_COLORS[id]}"></span>` : "") +
    `${escapeHtml(label)}<span class="count">${formatNumber(count)}</span></button>`;
  tagsEl.innerHTML = [chip("", "All", state.records.length), ...tags.map((t) => chip(t.id, t.label, t.count))].join("");
  tagsEl.addEventListener("click", (event) => {
    const button = event.target.closest("button[data-tag]");
    if (!button) return;
    setTag(button.dataset.tag);
    state.shown = PAGE_SIZE;
    render();
  });
}

function openFromHash() {
  const id = recordIdFromHash(location.hash);
  const index = state.records.findIndex((record) => record.id === id);
  if (index === -1) return;
  state.query = "";
  searchEl.value = "";
  setTag("");
  state.shown = Math.max(state.shown, Math.ceil((index + 1) / PAGE_SIZE) * PAGE_SIZE);
  render();
  const row = document.getElementById(id);
  if (row) {
    row.open = true;
    row.scrollIntoView({ block: "start" });
  }
}

function wireControls() {
  let timer;
  searchEl.addEventListener("input", () => {
    clearTimeout(timer);
    timer = setTimeout(() => {
      state.query = searchEl.value;
      state.shown = PAGE_SIZE;
      render();
    }, 120);
  });
  moreEl.addEventListener("click", () => {
    state.shown += PAGE_SIZE;
    render();
  });
  rowsEl.addEventListener(
    "toggle",
    (event) => {
      const row = event.target;
      if (row.matches("details.row") && row.open) {
        history.replaceState(null, "", `#${encodeURIComponent(row.dataset.id)}`);
      }
    },
    true,
  );
  window.addEventListener("hashchange", openFromHash);
}

function main() {
  const snapshotPromise = loadJson(SNAPSHOT_PATH);
  initFooter(snapshotPromise);
  initCircuitStrip(snapshotPromise);
  loadJson(DATA_PATH)
    .then((data) => {
      state.records = data.records;
      setText("nr-total", formatNumber(data.count));
      renderTags(data.tags);
      wireControls();
      render();
      openFromHash();
      loadJson(MAP_PATH)
        .then(initMap)
        .catch(() => {
          document.getElementById("map").hidden = true;
        });
    })
    .catch(() => showLoadError(rowsEl, DATA_PATH));
}

main();
