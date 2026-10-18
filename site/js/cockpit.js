import { initFooter, loadJson, setText, showLoadError } from "./common.js";
import { REPO_URL, escapeHtml, formatDate, formatNumber, repoUrl } from "./lib/format.js";
import {
  AGENT_LABELS,
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
} from "./lib/cockpit.js";

const DATA_PATH = "site/data/cockpit.json";
const HANDOFF_PATH = "research/AGENT_HANDOFF.md";
const PAGE_SIZE = 25;
const RECENT_DAYS = 14;
const METRIC_ORDER = ["negative_results", "results", "experiments", "blocking_findings", "proof_debts"];
const AGENT_GROUPS = Object.entries(AGENT_LABELS).map(([id, label]) => ({ id, label }));

const state = { data: null, labels: {}, direction: "", agent: "", shown: PAGE_SIZE, rugs: {} };

function count(value) {
  return value === null || value === undefined ? "–" : formatNumber(value);
}

function plural(n, word) {
  return `${formatNumber(n)} ${word}${n === 1 ? "" : "s"}`;
}

function figure(value, label) {
  return `<div><span class="figure-value">${escapeHtml(value)}</span><span class="figure-label">${escapeHtml(label)}</span></div>`;
}

function facts(rows) {
  return `<dl class="facts">${rows
    .filter(([, value]) => value)
    .map(([label, value]) => `<dt>${escapeHtml(label)}</dt><dd>${value}</dd>`)
    .join("")}</dl>`;
}

function commitLink(sha) {
  return `<a href="${REPO_URL}/commit/${encodeURIComponent(sha)}"><code>${escapeHtml(sha)}</code></a>`;
}

/* ---------- Header figures ---------- */

function renderHead(data) {
  const built = `Built ${formatDate(data.generated_on)}`;
  const head = data.head ? ` from commit ${commitLink(data.head.sha)} of ${escapeHtml(formatDate(data.head.date))}` : "";
  document.getElementById("ck-built").innerHTML = `${built}${head}.`;
  const checkpoint = data.checkpoint;
  document.getElementById("ck-figures").innerHTML = [
    figure(data.dirty ? count(data.dirty.total) : "–", "uncommitted files in this checkout"),
    figure(count(commitsInWindow(data.commits.days, data.generated_on, 7)), "commits in the last 7 days"),
    figure(count(data.inertia.flags.length), "directions flagged for inertia"),
    figure(count(data.coverage.sections), "handoff sections read"),
    figure(checkpoint ? count(checkpoint.days_since_session) : "–", "days since the last checkpoint session"),
  ].join("");
}

/* ---------- Inertia ---------- */

function renderInertia(data) {
  const inertia = data.inertia;
  setText("ck-inertia-summary", flaggedSentence(inertia));
  const body = document.querySelector("#ck-inertia tbody");
  body.innerHTML = inertiaRows(inertia)
    .map(
      (row) => `<tr>
        <td>${escapeHtml(row.label)}</td>
        <td data-label="Status" class="inline-sm">${
          row.flag ? '<span class="status status-ruled-out">flagged</span>' : '<span class="status status-open">under threshold</span>'
        }</td>
        <td data-label="Sections since a new entry" class="num inline-sm">${formatNumber(row.streak)}</td>
        <td data-label="Last new registry entry">${escapeHtml(row.lastNew)}</td>
        <td data-label="Latest section" class="inline-sm">${escapeHtml(row.lastSeen)}</td>
        <td data-label="All sections" class="num inline-sm">${formatNumber(row.sections)}</td>
      </tr>`,
    )
    .join("");
  setText(
    "ck-inertia-rule",
    `A direction is flagged after ${plural(inertia.threshold, "section")} of its own in a row with no new registry entry. ` +
      "Sections about other directions in between neither count nor reset the run. Other is a catch-all and is never flagged. " +
      "A new registry entry is an id from the negative-results registry or its quarantine file that a section mentions and no older section did.",
  );
  const runs = inertia.runs.filter((run) => !run.ongoing);
  if (runs.length) {
    document.getElementById("ck-runs-box").hidden = false;
    setText("ck-runs-summary", `Earlier runs of ${formatNumber(inertia.threshold)} or more (${formatNumber(runs.length)})`);
    document.getElementById("ck-runs").innerHTML = runs
      .map(
        (run) => `<tr>
          <td>${escapeHtml(state.labels[run.direction] || run.direction)}</td>
          <td data-label="Sections" class="num">${formatNumber(run.length)}</td>
          <td data-label="From">${escapeHtml(run.from_date ? formatDate(run.from_date) : "not committed yet")}</td>
          <td data-label="To">${escapeHtml(run.to_date ? formatDate(run.to_date) : "not committed yet")}</td>
        </tr>`,
      )
      .join("");
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
  const sections = state.data.sections;
  drawRug(
    "ck-rug-directions",
    state.data.directions,
    "direction",
    `${plural(sections.length, "handoff section")}, oldest first, one row per research direction.`,
  );
  drawRug("ck-rug-agents", AGENT_GROUPS, "agent", `${plural(sections.length, "handoff section")}, oldest first, one row per agent.`);
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
  const ids = section.new_registry_ids.length ? `<span class="ids">New: ${escapeHtml(section.new_registry_ids.join(", "))}</span>` : "";
  tipEl.innerHTML =
    `<code>${escapeHtml(sectionDate(section))} · ${escapeHtml(AGENT_LABELS[section.agent] || section.agent)} · ` +
    `${escapeHtml(state.labels[section.direction] || section.direction)}</code>${escapeHtml(section.heading)}${ids}`;
  tipEl.hidden = false;
  const frame = tipEl.offsetParent || tipEl.parentElement;
  const frameRect = frame.getBoundingClientRect();
  const left = Math.min(event.clientX - frameRect.left + 14, frameRect.width - tipEl.offsetWidth - 4);
  tipEl.style.left = `${Math.max(4, left)}px`;
  tipEl.style.top = `${event.clientY - frameRect.top + 16}px`;
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
    timer = setTimeout(drawRugs, 150);
  });
  const committed = data.sections.filter((section) => section.first_committed).length;
  setText(
    "ck-dating",
    data.settings.history
      ? `Sections carry no reliable dates, so each one is dated by the first commit of the handoff file that contained its heading ` +
          `(${formatNumber(committed)} of ${formatNumber(data.sections.length)} are committed). Sections first committed on the same day keep their file order.`
      : "This build skipped the handoff's git history, so sections are in file order and undated.",
  );
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

function sectionRow(section) {
  const handoff = `${repoUrl(HANDOFF_PATH)}?plain=1#L${section.line}`;
  const cues = section.cues.length ? `<span class="cues">${escapeHtml(section.cues.join(" · "))}</span>` : "";
  const weak = section.direction_weak ? '<span class="cues">weak match</span>' : "";
  const ids = section.new_registry_ids.length
    ? section.new_registry_ids.map(escapeHtml).join("<br>")
    : '<span class="muted">none</span>';
  return `<tr>
    <td data-label="First committed" class="inline-sm">${escapeHtml(sectionDate(section))}</td>
    <td data-label="Agent" class="inline-sm">${escapeHtml(AGENT_LABELS[section.agent] || section.agent)}${cues}</td>
    <td data-label="Direction" class="inline-sm">${escapeHtml(state.labels[section.direction] || section.direction)}${weak}</td>
    <td class="heading no-label"><a href="${handoff}">${escapeHtml(section.heading)}</a></td>
    <td data-label="New registry entries" class="ids">${ids}</td>
  </tr>`;
}

function renderSections() {
  const matches = recentSections(state.data.sections, { direction: state.direction, agent: state.agent });
  const visible = matches.slice(0, state.shown);
  document.getElementById("ck-section-rows").innerHTML = visible.map(sectionRow).join("");
  setText("ck-section-count", `Showing ${formatNumber(visible.length)} of ${plural(matches.length, "section")}`);
  document.getElementById("ck-more").hidden = visible.length >= matches.length;
}

function wireSections() {
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
  renderFilters();
  renderSections();
}

/* ---------- Commits ---------- */

function renderCommits(data) {
  const days = fillDays(data.commits.days, data.generated_on);
  document.getElementById("ck-commit-chart").innerHTML = commitChart({ days, labels: state.labels });
  if (days.length) {
    const recent = commitsInWindow(data.commits.days, data.generated_on, RECENT_DAYS);
    setText(
      "ck-commit-summary",
      `${plural(data.commits.total, "commit")} on the checked-out branch from ${formatDate(days[0].date)} to ${formatDate(days[days.length - 1].date)}, ` +
        `${formatNumber(recent)} of them in the last ${RECENT_DAYS} days. Hover a day to see what its commits were about.`,
    );
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
    .map(
      (commit) => `<li>
        <time datetime="${escapeHtml(commit.date)}">${escapeHtml(formatDate(commit.date))}</time>
        <div>${escapeHtml(commit.subject)}<p class="small">${commitLink(commit.sha)} · ${escapeHtml(state.labels[commit.topic] || commit.topic)}</p></div>
      </li>`,
    )
    .join("");
}

/* ---------- Metrics ---------- */

function metricKeys(metrics) {
  const known = METRIC_ORDER.filter((key) => metrics.keys.includes(key));
  return [...known, ...metrics.keys.filter((key) => !known.includes(key))];
}

function readout(point) {
  return `${formatNumber(point.value)} on ${formatDate(point.date)}`;
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
  container.innerHTML = charts
    .map(
      (chart) => `<div class="ck-spark">
        <h3>${escapeHtml(metricLabel(chart.key))}</h3>
        <p class="small" data-readout="${escapeHtml(chart.key)}">${escapeHtml(readout(chart.points[chart.points.length - 1]))}</p>
        <div data-spark="${escapeHtml(chart.key)}">${chart.svg}</div>
      </div>`,
    )
    .join("");
  for (const chart of charts) {
    const box = container.querySelector(`[data-spark="${chart.key}"]`);
    const out = container.querySelector(`[data-readout="${chart.key}"]`);
    const latest = readout(chart.points[chart.points.length - 1]);
    box.addEventListener("pointermove", (event) => {
      const svg = box.querySelector("svg");
      const rect = svg.getBoundingClientRect();
      const x = ((event.clientX - rect.left) * svg.viewBox.baseVal.width) / rect.width;
      const index = nearestTick(chart.points, x, Infinity);
      if (index !== -1) out.textContent = readout(chart.points[index]);
    });
    box.addEventListener("pointerleave", () => {
      out.textContent = latest;
    });
  }
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
          .map((key) => `<td class="num" data-label="${escapeHtml(metricLabel(key))}">${count(point.metrics[key])}</td>`)
          .join("")}</tr>`,
    )
    .join("");
  document.getElementById("ck-metrics-table").innerHTML = `${head}<tbody>${rows}</tbody>`;
}

/* ---------- Working tree and checkpoint ---------- */

function renderDirty(data) {
  const box = document.getElementById("ck-dirty");
  const dirty = data.dirty;
  if (!dirty) {
    box.innerHTML = '<p class="load-error">git status was not available when this page was built.</p>';
    return;
  }
  const areas = Object.entries(dirty.by_area).sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
  box.innerHTML =
    facts([
      ["Changed tracked files", formatNumber(dirty.modified)],
      ["Untracked files", formatNumber(dirty.untracked)],
      ["Total", formatNumber(dirty.total)],
    ]) +
    (areas.length
      ? `<table class="table plain"><thead><tr><th>Top-level folder</th><th class="num">Files</th></tr></thead><tbody>${areas
          .map(([area, n]) => `<tr><td><code>${escapeHtml(area)}</code></td><td class="num" data-label="Files">${formatNumber(n)}</td></tr>`)
          .join("")}</tbody></table>`
      : "") +
    '<p class="small">Counted with <code>git status</code> in the checkout that built the page, before the page wrote its own data. File names are left out on purpose.</p>';
}

function renderCheckpoint(data) {
  const box = document.getElementById("ck-checkpoint");
  const checkpoint = data.checkpoint;
  if (!checkpoint) {
    box.innerHTML = '<p class="load-error">No research checkpoint file was found in this checkout.</p>';
    return;
  }
  const review = checkpoint.review || {};
  const last = checkpoint.last_commit;
  const ago = checkpoint.days_since_session;
  box.innerHTML =
    facts([
      ["File", `<code>${escapeHtml(checkpoint.file)}</code>`],
      [
        "Session",
        checkpoint.session_date
          ? `${escapeHtml(formatDate(checkpoint.session_date))}${typeof ago === "number" ? ` (${plural(ago, "day")} before this build)` : ""}`
          : "",
      ],
      ["Active milestone", escapeHtml(checkpoint.active_milestone || "")],
      ["Latest verified subsystem", checkpoint.latest_verified_subsystem ? `<code>${escapeHtml(checkpoint.latest_verified_subsystem)}</code>` : ""],
      ["Verified subsystems", checkpoint.total_verified_subsystems === null ? "" : count(checkpoint.total_verified_subsystems)],
      ["Review", review.status ? `${escapeHtml(review.status)}${review.date ? ` (${escapeHtml(formatDate(review.date))})` : ""}` : ""],
      ["Next decision", escapeHtml(review.next_decision || "")],
      [
        "Last committed",
        last
          ? `${escapeHtml(formatDate(last.date))} in ${commitLink(last.sha)}; ${plural(checkpoint.commits_since, "commit")} since`
          : "not in the git history",
      ],
      ["Uncommitted edits", checkpoint.uncommitted_changes ? "yes, the file has local changes" : "none"],
    ]) +
    '<p class="small">Agents edit this file to record the state of a research session. No code reads it, so its session date shows when a checkpoint was last recorded, not when work last happened.</p>';
}

/* ---------- Spend ---------- */

function renderSpend(data) {
  const spend = data.spend;
  if (!spend) return;
  document.getElementById("spend").hidden = false;
  const totals = spendTotals(spend);
  document.getElementById("ck-spend-summary").innerHTML =
    `Runs and compute per day from <code>${escapeHtml(spend.source)}</code>` +
    (spend.generated_on ? `, generated ${escapeHtml(formatDate(spend.generated_on))}` : "") +
    `, covering ${plural(totals.days, "day")}.`;
  document.getElementById("ck-spend-figures").innerHTML = [
    figure(count(totals.runs), "runs"),
    figure(formatDuration(totals.wall_hours * 3600), "wall-clock time, timed runs only"),
    figure(totals.cpu_hours === null ? "–" : formatDuration(totals.cpu_hours * 3600), "CPU time, timed runs only"),
    figure(count(totals.negatives_added), "negative results added"),
    figure(totals.tokens === null ? "–" : compactCount(totals.tokens), "Codex tokens"),
  ].join("");
  document.getElementById("ck-spend-rows").innerHTML = [...spend.days]
    .reverse()
    .map(
      (day) => `<tr>
        <td>${escapeHtml(formatDate(day.date))}</td>
        <td class="num" data-label="Runs">${count(day.runs)}</td>
        <td class="num" data-label="Wall time">${escapeHtml(formatDuration(day.wall_seconds))}</td>
        <td class="num" data-label="CPU time">${escapeHtml(formatDuration(day.cpu_seconds))}</td>
        <td class="num" data-label="Negatives added">${count(day.negatives_added)}</td>
        <td class="num" data-label="Tokens">${day.tokens === null || day.tokens === undefined ? "not recorded" : count(day.tokens)}</td>
      </tr>`,
    )
    .join("");
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
  document.getElementById("ck-method").innerHTML = [
    `<p><strong>Direction.</strong> Each section is scored against a keyword table: three points for each distinct keyword in its heading, ` +
      `one for each mention in its body (up to twelve). The highest score wins and ties go to the direction listed first. ` +
      `${formatNumber(coverage.by_direction.other || 0)} of ${formatNumber(coverage.sections)} sections (${percent(coverage.other_share)}) match no keyword and count as Other; ` +
      `${formatNumber(coverage.weak)} more are weak matches, won with under three points or on a tie.</p>`,
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
  document.getElementById("ck-warnings").innerHTML = data.warnings.map((warning) => `<p class="load-error">${escapeHtml(warning)}</p>`).join("");
}

/* ---------- Main ---------- */

function main() {
  initFooter();
  loadJson(DATA_PATH)
    .then((data) => {
      state.data = data;
      state.labels = Object.fromEntries(data.directions.map((direction) => [direction.id, direction.label]));
      renderHead(data);
      renderInertia(data);
      renderTimeline(data);
      wireSections();
      renderCommits(data);
      renderMetrics(data);
      renderDirty(data);
      renderCheckpoint(data);
      renderSpend(data);
      renderMethod(data);
    })
    .catch((error) => {
      console.error(error);
      showLoadError(document.getElementById("ck-figures"), DATA_PATH);
    });
}

main();
