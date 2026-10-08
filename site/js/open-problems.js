import { SNAPSHOT_PATH, initCircuitStrip, initFooter, loadJson, setText, showLoadError } from "./common.js";
import { escapeHtml, formatDate, formatNumber, humanizeId, statusMarker } from "./lib/format.js";
import { groupDebts } from "./lib/debts.js";

const FRONTIERS_PATH = "research/frontier_map.json";
const DEBTS_PATH = "research/proof_debt_report.json";
const DEBT_TYPES = {
  dequantization: ["Dequantization", "A classical method may already match the idea."],
  "reduction-route": ["Reduction route", "The link between the idea and the real problem isn't proved yet."],
  falsifier: ["Falsifiers", "A known test already rejects the idea in its current form."],
};

function asList(value) {
  if (Array.isArray(value)) return value;
  return value ? [value] : [];
}

function listItems(values) {
  return values.map((value) => `<li>${escapeHtml(value)}</li>`).join("");
}

function frontierRow(frontier) {
  const needs = asList(frontier.required_new_capability);
  const kills = asList(frontier.kill_criteria);
  return `<details class="row" id="${escapeHtml(frontier.frontier_id)}">
    <summary>
      <span class="row-title">${escapeHtml(humanizeId(frontier.frontier_id))}</span>
      <span class="row-summary clamp">${escapeHtml(frontier.why_it_matters)}</span>
      ${statusMarker("open")}
    </summary>
    <div class="row-body">
      <dl class="facts">
        <dt>Priority</dt><dd class="num">${formatNumber(frontier.priority_score)}</dd>
        <dt>State</dt><dd><code>${escapeHtml(frontier.status)}</code></dd>
        <dt>Next experiment</dt><dd>${escapeHtml(frontier.next_experiment)}</dd>
      </dl>
      ${needs.length ? `<h4>What it needs</h4><ul>${listItems(needs)}</ul>` : ""}
      ${kills.length ? `<details class="sub"><summary>Kill criteria (${kills.length})</summary><ul>${listItems(kills)}</ul></details>` : ""}
      <details class="sub"><summary>Evidence so far</summary><p class="small">${escapeHtml(asList(frontier.evidence).join(" "))}</p></details>
    </div>
  </details>`;
}

function debtRow(debt, sharedResolution) {
  const ownResolution = sharedResolution ? "" : `<p class="small">To close: ${escapeHtml(debt.required_resolution)}</p>`;
  return `<tr>
    <td class="id" data-label="Candidate">${escapeHtml(debt.candidate_id)}</td>
    <td class="inline-sm" data-label="Blocks"><code>${escapeHtml(debt.claim_blocked)}</code></td>
    <td class="num inline-sm" data-label="Priority">${formatNumber(debt.priority_score)}</td>
    <td class="no-label" data-label="Evidence"><details class="sub"><summary>Show evidence</summary><p class="small">${escapeHtml(debt.evidence)}</p></details>${ownResolution}</td>
  </tr>`;
}

function debtGroup(group) {
  const [label, explanation] = DEBT_TYPES[group.type] || [humanizeId(group.type), ""];
  const shared = group.resolution ? ` To close: ${escapeHtml(group.resolution)}` : "";
  return `<section class="debt-group">
    <h3>${escapeHtml(label)} <span class="muted num">${formatNumber(group.debts.length)}</span></h3>
    <p class="muted">${escapeHtml(explanation)}${shared}</p>
    <table class="table">
      <thead><tr><th>Candidate</th><th>Blocks</th><th>Priority</th><th>Evidence</th></tr></thead>
      <tbody>${group.debts.map((debt) => debtRow(debt, group.resolution)).join("")}</tbody>
    </table>
  </section>`;
}

function renderFrontiers(data) {
  const frontiers = [...data.frontiers].sort((a, b) => b.priority_score - a.priority_score);
  setText("frontier-date", formatDate(data.created_at));
  document.getElementById("frontier-rows").innerHTML = frontiers.map(frontierRow).join("");
}

function renderDebts(report) {
  const debts = report.proof_debts;
  const select = document.getElementById("debt-candidate");
  const container = document.getElementById("debt-groups");
  setText("debt-count", formatNumber(debts.length));
  const candidates = [...new Set(debts.map((debt) => debt.candidate_id))].sort();
  select.insertAdjacentHTML(
    "beforeend",
    candidates.map((id) => `<option value="${escapeHtml(id)}">${escapeHtml(id)}</option>`).join(""),
  );
  const render = () => {
    const shown = select.value ? debts.filter((debt) => debt.candidate_id === select.value) : debts;
    container.innerHTML = groupDebts(shown).map(debtGroup).join("");
  };
  select.addEventListener("change", render);
  render();
}

function main() {
  const snapshotPromise = loadJson(SNAPSHOT_PATH);
  initFooter(snapshotPromise);
  initCircuitStrip(snapshotPromise);
  loadJson(FRONTIERS_PATH)
    .then(renderFrontiers)
    .catch(() => showLoadError(document.getElementById("frontier-rows"), FRONTIERS_PATH));
  loadJson(DEBTS_PATH)
    .then(renderDebts)
    .catch(() => showLoadError(document.getElementById("debt-groups"), DEBTS_PATH));
}

main();
