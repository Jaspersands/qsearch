import { initFooter, loadJson, setText, showLoadError } from "./common.js";
import { escapeHtml, formatNumber, repoUrl } from "./lib/format.js";
import { filterRecords, recordIdFromHash } from "./lib/negatives.js";

const DATA_PATH = "site/data/negatives.json";
const PAGE_SIZE = 40;

const state = { records: [], query: "", tag: "", shown: PAGE_SIZE };
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
  const visible = matches.slice(0, state.shown);
  rowsEl.innerHTML = visible.map(recordRow).join("");
  const filtered = matches.length !== state.records.length;
  setText(
    "nr-count",
    `Showing ${formatNumber(visible.length)} of ${formatNumber(matches.length)}` +
      (filtered ? ` matching results (${formatNumber(state.records.length)} in total)` : " results"),
  );
  moreEl.hidden = visible.length >= matches.length;
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
  initFooter();
  loadJson(DATA_PATH)
    .then((data) => {
      state.records = data.records;
      setText("nr-total", formatNumber(data.count));
      renderTags(data.tags);
      wireControls();
      render();
      openFromHash();
    })
    .catch(() => showLoadError(rowsEl, DATA_PATH));
}

main();
