import { initFooter, loadJson, setText, showLoadError } from "./common.js";
import { escapeHtml, formatDate, formatNumber } from "./lib/format.js";
import {
  AGENT_LABELS,
  builtHtml,
  checkpointHtml,
  commitChart,
  commitItemHtml,
  commitsInWindow,
  compactCount,
  countText,
  dirtyHtml,
  figureHtml,
  fillDays,
  flaggedSentence,
  formatDuration,
  headFigures,
  inertiaRows,
  latestCommits,
  metricLabel,
  nearestTick,
  readoutText,
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
} from "./lib/cockpit.js";

const DATA_PATH = "site/data/cockpit.json";
const PAGE_SIZE = 25;
const RECENT_DAYS = 14;
const METRIC_ORDER = ["negative_results", "results", "experiments", "blocking_findings", "proof_debts"];
const AGENT_GROUPS = Object.entries(AGENT_LABELS).map(([id, label]) => ({ id, label }));

const state = { data: null, labels: {}, direction: "", agent: "", shown: PAGE_SIZE, rugs: {} };

function plural(n, word) {
  return `${formatNumber(n)} ${word}${n === 1 ? "" : "s"}`;
}

/* ---------- Header figures ---------- */

function renderHead(data) {
  document.getElementById("ck-built").innerHTML = builtHtml(data);
  document.getElementById("ck-figures").innerHTML = headFigures(data)
    .map((item) => figureHtml(item.value, item.label))
    .join("");
  const top = document.getElementById("ck-top-warnings");
  top.innerHTML = warningsHtml(data.warnings);
  top.hidden = !data.warnings.length;
}

/* ---------- Inertia ---------- */

function renderInertia(data) {
  const inertia = data.inertia;
  const registry = data.registry;
  setText("ck-inertia-summary", flaggedSentence(inertia));
  setText("ck-registry", registrySentence(registry, state.labels));
  const body = document.querySelector("#ck-inertia tbody");
  body.innerHTML = inertiaRows(inertia, registry && registry.baseline)
    .map(
      (row) => `<tr>
        <td>${escapeHtml(row.label)}</td>
        <td data-label="Status" class="inline-sm">${
          row.flag ? '<span class="status status-ruled-out">flagged</span>' : '<span class="status status-open">under threshold</span>'
        }</td>
        <td data-label="Sections since its last registry gain" class="num inline-sm">${formatNumber(row.streak)}</td>
        <td data-label="Last registry gain in this direction">${escapeHtml(row.lastGain)}</td>
        <td data-label="Records gained" class="num inline-sm">${formatNumber(row.gained)}</td>
        <td data-label="Latest section" class="inline-sm">${escapeHtml(row.lastSeen)}</td>
        <td data-label="All sections" class="num inline-sm">${formatNumber(row.sections)}</td>
      </tr>`,
    )
    .join("");
  setText(
    "ck-inertia-rule",
    `A direction is flagged once ${plural(inertia.threshold, "section")} of its own have been first committed after the last day ` +
      "on which the negative-results registry gained a record in that direction. Registry gains come from the registry's own git history: " +
      "each record is dated by the first commit that contains it, and its direction comes from the same keyword table as the sections, " +
      "applied to the record's id, claim and tags. Sections first committed on a gain day are not counted, because days are the finest " +
      "grain both histories share. Sections about other directions neither count nor end a run. Other is a catch-all and is never flagged.",
  );
  const runs = inertia.runs.filter((run) => !run.ongoing);
  const box = document.getElementById("ck-runs-box");
  box.hidden = !runs.length;
  if (runs.length) {
    setText("ck-runs-summary", `Earlier runs of ${formatNumber(inertia.threshold)} or more sections (${formatNumber(runs.length)})`);
    document.getElementById("ck-runs").innerHTML = runs.map((run) => runRowHtml(run, state.labels)).join("");
  }
}

/* ---------- Timeline rugs ---------- */

const tipEl = document.getElementById("ck-tip");

function drawRug(id, groups, key, label) {
  const container = document.getElementById(id);
  const width = Math.max(320, Math.round(container.clientWidth));
  const layout = rugLayout({
    sections: state.data.sections,
    groups,
    key,
    width,
    labelWidth: width < 560 ? 168 : 196,
  });
  container.innerHTML = rugChart(layout, label);
  state.rugs[id] = layout;
}

function drawRugs() {
  const n = plural(state.data.sections.length, "handoff section");
  const order = "in section order, oldest on the left (the horizontal axis is not calendar time)";
  drawRug("ck-rug-directions", state.data.directions, "direction", `${n} ${order}, one row per research direction.`);
  drawRug("ck-rug-agents", AGENT_GROUPS, "agent", `${n} ${order}, one row per agent.`);
}

function hideTip() {
  tipEl.hidden = true;
}

function showRugTip(event) {
  const container = event.currentTarget;
  const layout = state.rugs[container.id];
  const svg = container.querySelector("svg");
  if (!layout || !svg) return;
  const rect = svg.getBoundingClientRect();
  const scale = layout.width / rect.width;
  const x = (event.clientX - rect.left) * scale;
  const y = (event.clientY - rect.top) * scale;
  const row = layout.rows[Math.floor(y / layout.rowHeight)];
  const index = row ? nearestTick(row.ticks, x, Math.max(4, 8 * scale)) : -1;
  if (index === -1) {
    hideTip();
    return;
  }
  const section = row.ticks[index].section;
  const gain = section.registry_day ? '<span class="ids">Registry gained a record in this direction that day</span>' : "";
  tipEl.innerHTML =
    `<code>${escapeHtml(sectionDate(section))} · ${escapeHtml(AGENT_LABELS[section.agent] || section.agent)} · ` +
    `${escapeHtml(state.labels[section.direction] || section.direction)}</code>${escapeHtml(section.heading)}${gain}`;
  tipEl.hidden = false;
  const frame = tipEl.offsetParent || tipEl.parentElement;
  const frameRect = frame.getBoundingClientRect();
  const left = Math.min(event.clientX - frameRect.left + 14, frameRect.width - tipEl.offsetWidth - 4);
  tipEl.style.left = `${Math.max(4, left)}px`;
  tipEl.style.top = `${event.clientY - frameRect.top + 16}px`;
}

function datingText(data) {
  const committed = data.sections.filter((section) => section.first_committed).length;
  if (data.git && data.git.history) {
    return (
      "Sections carry no reliable dates, so each one is dated by the first commit of the handoff file that contained its heading, " +
      `as a UTC day (${formatNumber(committed)} of ${formatNumber(data.sections.length)} are committed). ` +
      "Sections first committed on the same day keep their file order."
    );
  }
  if (data.git && data.git.shallow) return "This checkout is a shallow clone, so sections are in file order and undated.";
  if (data.git && !data.git.available) return "git was not available when this page was built, so sections are in file order and undated.";
  return "This build skipped the git history, so sections are in file order and undated.";
}

function renderTimeline(data) {
  drawRugs();
  for (const id of ["ck-rug-directions", "ck-rug-agents"]) {
    const container = document.getElementById(id);
    container.addEventListener("pointermove", showRugTip);
    container.addEventListener("pointerleave", hideTip);
  }
  let timer;
  window.addEventListener("resize", () => {
    clearTimeout(timer);
    timer = setTimeout(() => {
      try {
        drawRugs();
      } catch (error) {
        console.error(error);
      }
    }, 150);
  });
  setText("ck-dating", datingText(data));
}

/* ---------- Section list ---------- */

function chips(containerId, title, options, current, attr) {
  const chip = (id, label, n) =>
    `<button type="button" class="chip" data-${attr}="${escapeHtml(id)}" aria-pressed="${id === current}">` +
    `${escapeHtml(label)}<span class="count">${formatNumber(n)}</span></button>`;
  const total = state.data.sections.length;
  document.getElementById(containerId).innerHTML =
    `<span class="ck-filter-label">${escapeHtml(title)}</span>` +
    [chip("", "All", total), ...options.filter((o) => o.count > 0).map((o) => chip(o.id, o.label, o.count))].join("");
}

function renderFilters() {
  const sections = state.data.sections;
  const tally = (key, id) => sections.filter((section) => section[key] === id).length;
  chips(
    "ck-direction-filter",
    "Direction",
    state.data.directions.map((d) => ({ ...d, count: tally("direction", d.id) })),
    state.direction,
    "direction",
  );
  chips("ck-agent-filter", "Agent", AGENT_GROUPS.map((a) => ({ ...a, count: tally("agent", a.id) })), state.agent, "agent");
}

function renderSections() {
  const matches = recentSections(state.data.sections, { direction: state.direction, agent: state.agent });
  const visible = matches.slice(0, state.shown);
  document.getElementById("ck-section-rows").innerHTML = visible
    .map((section) => sectionRowHtml(section, { labels: state.labels, head: state.data.head }))
    .join("");
  setText("ck-section-count", `Showing ${formatNumber(visible.length)} of ${plural(matches.length, "section")}`);
  document.getElementById("ck-more").hidden = visible.length >= matches.length;
}

function wireSections(data) {
  const filterClick = (attr, key) => (event) => {
    const button = event.target.closest(`button[data-${attr}]`);
    if (!button) return;
    state[key] = button.dataset[attr];
    state.shown = PAGE_SIZE;
    renderFilters();
    renderSections();
  };
  document.getElementById("ck-direction-filter").addEventListener("click", filterClick("direction", "direction"));
  document.getElementById("ck-agent-filter").addEventListener("click", filterClick("agent", "agent"));
  document.getElementById("ck-more").addEventListener("click", () => {
    state.shown += PAGE_SIZE;
    renderSections();
  });
  const quotes = data.quotes || {};
  const registry = data.registry;
  setText(
    "ck-quotes-note",
    "The last column lists the registry ids this section quoted in the first committed version of the handoff that quoted them, " +
      "so a later section that only repeats an id gets no credit. " +
      `${formatNumber(quotes.from_history || 0)} ids are credited from history, ${formatNumber(quotes.from_current_text || 0)} from text not committed yet, ` +
      `and ${formatNumber(quotes.lost || 0)} ${quotes.lost === 1 ? "was" : "were"} first quoted by a section that is no longer in the handoff. ` +
      (registry && typeof registry.quoted === "number"
        ? `Most registry records are never quoted (only ${formatNumber(registry.quoted)} of the ${formatNumber(registry.added + (registry.uncommitted || 0))} gained), so this column does not measure registry growth.`
        : "Most registry records are never quoted, so this column does not measure registry growth."),
  );
  renderFilters();
  renderSections();
}

/* ---------- Commits ---------- */

function renderCommits(data) {
  const days = fillDays(data.commits.days, data.generated_on);
  document.getElementById("ck-commit-chart").innerHTML = commitChart({ days, labels: state.labels });
  const partial = data.commits.complete ? "" : " This checkout does not have the full git history, so this is only part of it.";
  if (days.length) {
    const recent = commitsInWindow(data.commits.days, data.generated_on, RECENT_DAYS);
    setText(
      "ck-commit-summary",
      `${plural(data.commits.total, "commit")} on the checked-out branch from ${formatDate(days[0].date)} to ${formatDate(days[days.length - 1].date)}, ` +
        `${formatNumber(recent)} of them in the ${RECENT_DAYS} days to ${formatDate(data.generated_on)}. Days are UTC. ` +
        `Hover a day to see what its commits were about.${partial}`,
    );
  } else {
    setText("ck-commit-summary", `No commits were read when this page was built.${partial}`);
  }
  document.getElementById("ck-topics").innerHTML = topicTotals(data.commits.days, data.generated_on, RECENT_DAYS)
    .map(
      (row) => `<tr>
        <td>${escapeHtml(state.labels[row.topic] || row.topic)}</td>
        <td data-label="Last ${RECENT_DAYS} days" class="num">${formatNumber(row.recent)}</td>
        <td data-label="All time" class="num">${formatNumber(row.all)}</td>
      </tr>`,
    )
    .join("");
  document.getElementById("ck-latest-commits").innerHTML = latestCommits(data.commits.days, 12)
    .map((commit) => commitItemHtml(commit, state.labels))
    .join("");
}

/* ---------- Metrics ---------- */

function metricKeys(metrics) {
  const known = METRIC_ORDER.filter((key) => metrics.keys.includes(key));
  return [...known, ...metrics.keys.filter((key) => !known.includes(key))];
}

function renderMetrics(data) {
  const metrics = data.metrics;
  const keys = metricKeys(metrics);
  const container = document.getElementById("ck-sparks");
  if (!metrics.points.length) {
    container.innerHTML = '<p class="load-error">No committed versions of the progress snapshot were found.</p>';
    return;
  }
  const charts = keys.map((key) => ({ key, ...sparkline({ points: metrics.points, key }) })).filter((chart) => chart.points.length);
  container.innerHTML = sparkCardsHtml(charts);
  // Cards are matched to charts by position; no selector is ever built from a metric key.
  container.querySelectorAll(".ck-spark").forEach((card, i) => {
    const chart = charts[i];
    const box = card.querySelector(".ck-spark-chart");
    const out = card.querySelector(".ck-readout");
    const latest = readoutText(chart.points[chart.points.length - 1]);
    box.addEventListener("pointermove", (event) => {
      const svg = box.querySelector("svg");
      const rect = svg.getBoundingClientRect();
      const x = ((event.clientX - rect.left) * svg.viewBox.baseVal.width) / rect.width;
      const index = nearestTick(chart.points, x, Infinity);
      if (index !== -1) out.textContent = readoutText(chart.points[index]);
    });
    box.addEventListener("pointerleave", () => {
      out.textContent = latest;
    });
  });
  const first = metrics.points[0];
  const last = metrics.points[metrics.points.length - 1];
  setText(
    "ck-metrics-summary",
    `The headline counts from ${plural(metrics.points.length, "dated version")} of the progress snapshot, ${formatDate(first.date)} to ${formatDate(last.date)}. ` +
      "Each chart has its own scale, starting at zero. Hover a chart to read a date.",
  );
  const head = `<thead><tr><th>Date</th>${keys.map((key) => `<th class="num">${escapeHtml(metricLabel(key))}</th>`).join("")}</tr></thead>`;
  const rows = [...metrics.points]
    .reverse()
    .map(
      (point) =>
        `<tr><td>${escapeHtml(formatDate(point.date))}</td>${keys
          .map((key) => `<td class="num" data-label="${escapeHtml(metricLabel(key))}">${countText(point.metrics[key])}</td>`)
          .join("")}</tr>`,
    )
    .join("");
  document.getElementById("ck-metrics-table").innerHTML = `${head}<tbody>${rows}</tbody>`;
}

/* ---------- Working tree and checkpoint ---------- */

function renderDirty(data) {
  document.getElementById("ck-dirty").innerHTML = dirtyHtml(data.dirty, data.generated_on);
}

function renderCheckpoint(data) {
  document.getElementById("ck-checkpoint").innerHTML = checkpointHtml(data.checkpoint, {
    builtOn: data.generated_on,
    complete: data.commits.complete,
  });
}

/* ---------- Spend ---------- */

function renderSpend(data) {
  const spend = data.spend;
  if (!spend) return;
  document.getElementById("spend").hidden = false;
  const totals = spendTotals(spend);
  document.getElementById("ck-spend-summary").innerHTML =
    `Experiment runs and compute per UTC day from <code>${escapeHtml(spend.source)}</code>` +
    (spend.generated_on ? `, generated ${escapeHtml(formatDate(spend.generated_on))}` : "") +
    `, covering ${plural(totals.days, "day")}. Wall and CPU time come from timed commands only; ` +
    "a day with none says not recorded. Token totals include cached input tokens unless a cached share is shown.";
  document.getElementById("ck-spend-figures").innerHTML = [
    figureHtml(countText(totals.runs), "experiment runs"),
    figureHtml(totals.wall_hours === null ? "not recorded" : formatDuration(totals.wall_hours * 3600), "wall-clock time of timed commands"),
    figureHtml(totals.cpu_hours === null ? "not recorded" : formatDuration(totals.cpu_hours * 3600), "CPU time of timed commands"),
    figureHtml(countText(totals.negatives_added), "retained negative results, the registry's first version included"),
    figureHtml(totals.tokens === null ? "–" : compactCount(totals.tokens), tokenLabel(totals)),
  ].join("");
  document.getElementById("ck-spend-rows").innerHTML = [...spend.days].reverse().map(spendRowHtml).join("");
}

/* ---------- Method ---------- */

function percent(share) {
  return `${(share * 100).toFixed(1)}%`;
}

function renderMethod(data) {
  const coverage = data.coverage;
  const attribution = data.attribution;
  const check = attribution.check;
  const agents = attribution.by_agent;
  const registry = data.registry;
  document.getElementById("ck-method").innerHTML = [
    `<p><strong>Direction.</strong> Each section is scored against a keyword table: three points for each distinct keyword in its heading, ` +
      `one for each mention in its body (up to twelve). The highest score wins and ties go to the direction listed first. ` +
      `${formatNumber(coverage.by_direction.other || 0)} of ${formatNumber(coverage.sections)} sections (${percent(coverage.other_share)}) match no keyword and count as Other; ` +
      `${formatNumber(coverage.weak)} more are weak matches, won with under three points or on a tie.</p>`,
    registry
      ? `<p><strong>Registry records.</strong> Each record the registry gained gets a direction from the same table, with its id as the heading ` +
        `and its claim and tags as the body. ${formatNumber(registry.unclassified)} of ${formatNumber(registry.added + (registry.uncommitted || 0))} ` +
        `match no keyword and stay unclassified, so they move no direction's inertia; ${formatNumber(registry.weak)} more are weak matches.</p>`
      : "",
    `<p><strong>Agent.</strong> Codex and the Gemini agents write differently. Codex hard-wraps its prose, writes words like NOT and SAME in capitals, ` +
      `says "No GPT commit" and refers to Gemini in the third person. Gemini titles sections "Investigation N Proved", uses dashes and ampersands in headings, ` +
      `bold text, inline LaTeX and long unwrapped lines. A section needs a clear lead in these cues to get a label: ` +
      `${formatNumber(agents.codex)} read as Codex, ${formatNumber(agents.gemini)} as Gemini and ${formatNumber(agents.unknown)} stay unknown. ` +
      `The two Gemini agents write alike, so they share one label.</p>`,
    `<p><strong>How well that holds up.</strong> ${formatNumber(check.explicit_sections)} sections name their author outright. ` +
      `With those explicit cues removed, the style cues alone agree with the named author on ${formatNumber(check.agree)}, ` +
      `disagree on ${formatNumber(check.disagree)} and abstain on ${formatNumber(check.abstain)}. Abstaining is the expected failure: ` +
      `older sections are written in a plainer style that neither agent owns.</p>`,
  ].join("");
  document.getElementById("ck-cues").innerHTML = attribution.cues
    .map(
      (cue) => `<tr>
        <td>${escapeHtml(cue.name)}${cue.explicit ? ' <span class="muted">(names an agent)</span>' : ""}</td>
        <td data-label="Points to">${escapeHtml(AGENT_LABELS[cue.agent] || cue.agent)} +${formatNumber(cue.weight)}</td>
        <td class="num" data-label="Sections">${formatNumber(cue.sections)}</td>
      </tr>`,
    )
    .join("");
  document.getElementById("ck-warnings").innerHTML = warningsHtml(data.warnings);
}

/* ---------- Main ---------- */

function panelError(panel, error) {
  console.error(`cockpit: the ${panel.name} panel failed`, error);
  const box = document.getElementById(panel.box);
  if (box) {
    box.insertAdjacentHTML(
      "afterbegin",
      `<p class="load-error">This panel could not be drawn from the data (${escapeHtml(error && error.message ? error.message : error)}). The rest of the page is unaffected.</p>`,
    );
  }
}

function render(data) {
  state.data = data;
  state.labels = Object.fromEntries(data.directions.map((direction) => [direction.id, direction.label]));
  runPanels(
    [
      { name: "header", box: "ck-figures", draw: () => renderHead(data) },
      { name: "inertia", box: "ck-inertia-box", draw: () => renderInertia(data) },
      { name: "timeline", box: "ck-timeline-box", draw: () => renderTimeline(data) },
      { name: "sections", box: "ck-sections-box", draw: () => wireSections(data) },
      { name: "commits", box: "ck-commits-box", draw: () => renderCommits(data) },
      { name: "metrics", box: "ck-sparks", draw: () => renderMetrics(data) },
      { name: "working tree", box: "ck-dirty", draw: () => renderDirty(data) },
      { name: "checkpoint", box: "ck-checkpoint", draw: () => renderCheckpoint(data) },
      { name: "spend", box: "ck-spend-figures", draw: () => renderSpend(data) },
      { name: "method", box: "ck-method", draw: () => renderMethod(data) },
    ],
    panelError,
  );
}

function main() {
  initFooter();
  // Only a failure to fetch or parse the data says so; a panel that fails to draw reports itself.
  loadJson(DATA_PATH)
    .then(render, (error) => {
      console.error(error);
      showLoadError(document.getElementById("ck-figures"), DATA_PATH);
    })
    .catch((error) => console.error("cockpit: the page could not be drawn", error));
}

main();
