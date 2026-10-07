import { SNAPSHOT_PATH, bindCopyButtons, initFooter, loadJson, setText, showLoadError } from "./common.js";
import { bibtexEntry, escapeHtml, formatDate, formatNumber, statusMarker, trackStatusKind } from "./lib/format.js";
import { activityChart } from "./lib/chart.js";
import { circuitSvg, wireExtents, wirePlan } from "./lib/circuit.js";

const ACTIVITY_PATH = "site/data/activity.json";
const CHANGELOG_PATH = "site/data/changelog.json";
const CHANGELOG_PREVIEW = 6;
const GATE_ANCHORS = ["#main .intro h1", "#tracks h2", "#activity h2", "#results h2"];
const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const circuit = { plan: null, extents: [], liveEnds: [], top: 30, active: -1 };

function drawCircuit() {
  const main = document.getElementById("main");
  const holder = document.getElementById("circuit");
  if (!circuit.plan || !main || !holder) return;
  const mainTop = main.getBoundingClientRect().top;
  const gutter = parseFloat(getComputedStyle(document.documentElement).getPropertyValue("--gutter")) || 150;
  const wrap = main.querySelector(".wrap");
  const wrapLeft = wrap.getBoundingClientRect().left - main.getBoundingClientRect().left;
  const basePad = parseFloat(getComputedStyle(wrap).paddingLeft) - gutter;
  const height = main.offsetHeight;
  const gateYs = GATE_ANCHORS.map((selector) => {
    const node = document.querySelector(selector);
    return node ? Math.round(node.getBoundingClientRect().top - mainTop + 18) : 0;
  });
  gateYs.push(height - 48);
  holder.style.left = `${Math.max(0, wrapLeft + basePad - 12)}px`;
  holder.style.height = `${height}px`;
  holder.innerHTML = circuitSvg({ plan: circuit.plan, gateYs, height, width: gutter });
  circuit.extents = wireExtents(circuit.plan, gateYs, gutter);
  // Live overlays stop where each wire's solid part stops; the dot rides the active wire to the end.
  circuit.liveEnds = circuit.plan.map((wire, i) => (wire.active ? gateYs[wire.solidTo] : circuit.extents[i].end));
  circuit.active = circuit.plan.findIndex((wire) => wire.active);
  updateCircuitProgress();
}

function updateCircuitProgress() {
  const main = document.getElementById("main");
  if (!main || !circuit.extents.length) return;
  const progress = reduceMotion ? main.offsetHeight : window.innerHeight * 0.6 - main.getBoundingClientRect().top;
  for (const line of document.querySelectorAll("#circuit .wire-live")) {
    const end = circuit.liveEnds[Number(line.dataset.wire)];
    line.setAttribute("y2", String(Math.max(circuit.top, Math.min(end, progress))));
  }
  const dot = document.querySelector("#circuit .circuit-dot");
  if (dot && circuit.active !== -1) {
    dot.setAttribute("cy", String(Math.max(circuit.top, Math.min(circuit.extents[circuit.active].end, progress))));
  }
}

function initCircuit(snapshot) {
  circuit.plan = wirePlan(snapshot.tracks);
  drawCircuit();
  let timer;
  new ResizeObserver(() => {
    clearTimeout(timer);
    timer = setTimeout(drawCircuit, 80);
  }).observe(document.getElementById("main"));
  if (!reduceMotion) window.addEventListener("scroll", updateCircuitProgress, { passive: true });
}

function renderIntro(snapshot) {
  setText("verdict-title", `${snapshot.verdict.title}.`);
  setText("verdict-detail", snapshot.verdict.detail);
  setText("snapshot-date", formatDate(snapshot.updated_at));
  setText("fig-negatives", formatNumber(snapshot.metrics.negative_results));
  setText("fig-experiments", formatNumber(snapshot.metrics.experiments));
  setText("fig-debts", formatNumber(snapshot.metrics.proof_debts));
}

function trackRow(track) {
  return `<details class="row">
    <summary>
      <span class="row-title">${escapeHtml(track.title)}</span>
      <span class="row-summary">${escapeHtml(track.status)}<span class="row-next">Next: ${escapeHtml(track.next)}</span></span>
      ${statusMarker(trackStatusKind(track.tone))}
    </summary>
    <div class="row-body">
      <p>${escapeHtml(track.summary)}</p>
      <dl class="facts"><dt>Evidence</dt><dd>${escapeHtml(track.evidence)}</dd></dl>
    </div>
  </details>`;
}

function renderMilestones(milestones) {
  document.getElementById("milestones").innerHTML = milestones
    .map((item) => `<li><h3>${escapeHtml(item.title)}</h3><p>${escapeHtml(item.detail)}</p></li>`)
    .join("");
}

function changelogItem(entry) {
  const changes = entry.changes.map((change) => `<li>${escapeHtml(change)}</li>`).join("");
  return `<li><time datetime="${escapeHtml(entry.date)}">${escapeHtml(formatDate(entry.date))}</time><ul>${changes}</ul></li>`;
}

function renderChangelog(changelog) {
  const list = document.getElementById("changelog");
  const button = document.getElementById("changelog-more");
  const entries = changelog.entries;
  const draw = (all) => {
    list.innerHTML = entries.slice(0, all ? entries.length : CHANGELOG_PREVIEW).map(changelogItem).join("");
  };
  draw(false);
  if (entries.length > CHANGELOG_PREVIEW) {
    button.textContent = `Show all ${formatNumber(entries.length)} changes`;
    button.hidden = false;
    button.addEventListener("click", () => {
      draw(true);
      button.hidden = true;
    });
  }
}

function main() {
  bindCopyButtons();
  const snapshotPromise = loadJson(SNAPSHOT_PATH);
  initFooter(snapshotPromise);

  snapshotPromise
    .then((snapshot) => {
      renderIntro(snapshot);
      document.getElementById("track-rows").innerHTML = snapshot.tracks.map(trackRow).join("");
      renderMilestones(snapshot.milestones);
      setText("bibtex", bibtexEntry(snapshot));
      setText("execution-model", snapshot.execution_model);
      initCircuit(snapshot);
    })
    .catch(() => {
      setText("verdict-detail", "The latest snapshot couldn't load.");
      showLoadError(document.getElementById("track-rows"), SNAPSHOT_PATH);
      showLoadError(document.getElementById("milestones"), SNAPSHOT_PATH);
    });

  const changelogPromise = loadJson(CHANGELOG_PATH);
  const chartEl = document.getElementById("activity-chart");
  Promise.all([loadJson(ACTIVITY_PATH), changelogPromise])
    .then(([activity, changelog]) => {
      // Draw at the figure's real width so axis labels stay readable on phones.
      const draw = () => {
        const width = Math.round(Math.min(720, Math.max(320, chartEl.clientWidth)));
        chartEl.innerHTML = activityChart({ weeks: activity.weeks, points: changelog.points, width });
      };
      draw();
      let timer;
      window.addEventListener("resize", () => {
        clearTimeout(timer);
        timer = setTimeout(draw, 150);
      });
    })
    .catch(() => showLoadError(chartEl, ACTIVITY_PATH));
  changelogPromise
    .then(renderChangelog)
    .catch(() => showLoadError(document.getElementById("changelog"), CHANGELOG_PATH));
}

main();
