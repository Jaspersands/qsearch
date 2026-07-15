const $ = (selector) => document.querySelector(selector);

function text(value, fallback = "Not specified") {
    if (value === undefined || value === null || value === "") return fallback;
    return String(value);
}

function short(value, limit = 170) {
    const raw = text(value, "");
    return raw.length > limit ? `${raw.slice(0, limit - 1)}...` : raw;
}

function tag(label) {
    return `<span class="tag">${label}</span>`;
}

async function loadJson(path, fallback) {
    try {
        const response = await fetch(`${path}?v=${Date.now()}`);
        if (!response.ok) throw new Error(`${path}: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error(error);
        return fallback;
    }
}

function renderDiagnosis(agenda) {
    const items = agenda?.diagnosis?.blunt_diagnosis || [];
    $("#diagnosis-list").innerHTML = items.map((item) => `<li>${item}</li>`).join("");
    $("#mission-text").textContent = agenda?.mission || "Research agenda unavailable.";
}

function renderCounts(candidates, experiments, results, dequantization, proofStatus, negatives, rejected, obligations) {
    $("#count-candidates").textContent = candidates.length;
    $("#count-experiments").textContent = experiments.length;
    $("#count-results").textContent = results.length;
    $("#count-dequantization").textContent = dequantization.length;
    $("#count-proof-status").textContent = proofStatus.length;
    $("#count-negative").textContent = negatives.length;
    $("#count-rejected").textContent = rejected.length;
    $("#count-obligations").textContent = obligations.length;
}

function renderArchitecture(audit) {
    const architecture = audit?.new_architecture || {};
    $("#architecture-list").innerHTML = Object.entries(architecture)
        .map(([key, value]) => `
            <div class="stack-item">
                <strong>${key.replace(/^\d+_/, "").replaceAll("_", " ")}</strong>
                <p>${value}</p>
            </div>
        `)
        .join("");
}

function renderInterventions(interventions) {
    $("#intervention-list").innerHTML = interventions.slice(0, 12).map((item, index) => `
        <article class="ranked-item">
            <div class="rank">${index + 1}</div>
            <div class="rank-body">
                <div class="rank-title">
                    <h4>${item.title}</h4>
                    <span class="lift">${Number(item.expected_breakthrough_lift).toFixed(1)}</span>
                </div>
                <p>${item.why_it_matters}</p>
                <div class="meta-row">
                    ${tag(item.category)}
                    ${tag(item.difficulty)}
                    ${item.dependencies?.slice(0, 3).map(tag).join("") || ""}
                </div>
                <details>
                    <summary>Failure modes and falsifiers</summary>
                    <p><strong>Likely failure:</strong> ${item.likely_failure_modes?.join(" ") || "Not listed."}</p>
                    <p><strong>Falsify if:</strong> ${item.falsifying_evidence?.join(" ") || "Not listed."}</p>
                    <p><strong>Status:</strong> ${item.implementation_status}</p>
                </details>
            </div>
        </article>
    `).join("");
}

function renderLeads(candidates) {
    $("#lead-list").innerHTML = candidates.map((lead, index) => `
        <article class="lead-card">
            <div class="lead-top">
                <span class="rank-badge">#${index + 1}</span>
                <span class="score">${lead.status}</span>
            </div>
            <h4>${lead.title}</h4>
            <p>${short(lead.problem_family, 220)}</p>
            <div class="meta-row">${lead.ontology_node_ids?.map(tag).join("") || ""}</div>
            <details>
                <summary>Proof-gated record</summary>
                <p><strong>Mechanism:</strong> ${lead.quantum_mechanism}</p>
                <p><strong>Classical baseline:</strong> ${lead.classical_baseline}</p>
                <p><strong>Falsifiers:</strong> ${lead.falsifiers?.join(" ")}</p>
                <p><strong>Literature:</strong> ${lead.literature_ids?.join(", ")}</p>
            </details>
        </article>
    `).join("");
}

function renderExperiments(experiments) {
    $("#experiment-list").innerHTML = experiments.map((experiment) => `
        <article class="lead-card">
            <div class="lead-top">
                <span class="rank-badge">${experiment.candidate_id}</span>
                <span class="score">${experiment.status}</span>
            </div>
            <h4>${experiment.title}</h4>
            <p>${experiment.hypothesis}</p>
            <div class="meta-row">${experiment.metrics?.slice(0, 4).map(tag).join("") || ""}</div>
            <details>
                <summary>Protocol and falsifiers</summary>
                <p><strong>Protocol:</strong> ${experiment.protocol}</p>
                <p><strong>Positive signal:</strong> ${experiment.positive_signal}</p>
                <p><strong>Falsifiers:</strong> ${experiment.falsifiers?.join(" ")}</p>
                <p><strong>Next:</strong> ${experiment.next_actions?.join(" ")}</p>
            </details>
        </article>
    `).join("");
}

function renderResults(results) {
    $("#result-list").innerHTML = results.map((result) => `
        <article class="lead-card">
            <div class="lead-top">
                <span class="rank-badge">${result.experiment_id}</span>
                <span class="score">${result.status}</span>
            </div>
            <h4>${result.id}</h4>
            <p>${short(result.summary, 260)}</p>
            <div class="meta-row">${Object.keys(result.metrics || {}).slice(0, 4).map(tag).join("")}</div>
            <details>
                <summary>Metrics and falsifiers</summary>
                <p><strong>Metrics:</strong> ${JSON.stringify(result.metrics || {})}</p>
                <p><strong>Falsifiers:</strong> ${result.falsifiers_triggered?.join(" ") || "None triggered."}</p>
                <p><strong>Artifacts:</strong> ${Object.values(result.artifacts || {}).join(", ")}</p>
            </details>
        </article>
    `).join("");
}

function renderDequantization(findings) {
    $("#dequantization-list").innerHTML = findings.slice(0, 18).map((finding) => `
        <article class="negative-item">
            <h4>${finding.target_id}</h4>
            <p><strong>${finding.severity}:</strong> ${finding.claim_under_test}</p>
            <p><strong>Evidence:</strong> ${finding.evidence}</p>
            <p><strong>Required:</strong> ${finding.required_action}</p>
        </article>
    `).join("");
}

function renderProofStatus(records) {
    const visible = records.filter((record) => record.status !== "text-present").slice(0, 24);
    $("#proof-status-list").innerHTML = visible.map((record) => `
        <article class="negative-item">
            <h4>${record.candidate_id} ${record.obligation_id}</h4>
            <p><strong>Status:</strong> ${record.status}</p>
            <p><strong>Evidence:</strong> ${record.evidence}</p>
            <p><strong>Next:</strong> ${record.next_action}</p>
        </article>
    `).join("");
}

function renderNegativeResults(negatives) {
    $("#negative-list").innerHTML = negatives.slice(0, 18).map((item) => `
        <article class="negative-item">
            <h4>${item.claim}</h4>
            <p><strong>Invalid because:</strong> ${item.reason_invalid}</p>
            <p><strong>Lesson:</strong> ${item.lesson}</p>
            <div class="meta-row">${item.applies_to?.map(tag).join("") || ""}</div>
        </article>
    `).join("");
}

function renderRejectedCandidates(rejected) {
    $("#rejected-list").innerHTML = rejected.slice(0, 18).map((item) => `
        <article class="negative-item">
            <h4>${item.title}</h4>
            <p><strong>ID:</strong> ${item.id}</p>
            <p><strong>Rejected because:</strong> ${(item.issues || []).map((issue) => `${issue.obligation_id}: ${issue.message}`).join(" ")}</p>
            <div class="meta-row">${item.ontology_node_ids?.map(tag).join("") || ""}</div>
        </article>
    `).join("");
}

function renderProofGate(obligations) {
    $("#proof-list").innerHTML = obligations.map((item) => `
        <article class="proof-card">
            <span>${item.id}</span>
            <h4>${item.obligation}</h4>
            <p>${item.why_required}</p>
        </article>
    `).join("");
}

function renderBarriers(ontology) {
    $("#barrier-list").innerHTML = (ontology.barriers || []).map((barrier) => `
        <div class="stack-item">
            <strong>${barrier.id}</strong>
            <p>${barrier.barrier}</p>
            <p><em>Avoid by:</em> ${barrier.avoid_by}</p>
            <div class="meta-row">${barrier.applies_to?.map(tag).join("") || ""}</div>
        </div>
    `).join("");
}

function renderPapers(literatureRecords, literatureIndex) {
    const papers = literatureRecords.length ? literatureRecords : (literatureIndex.seed_papers || []);
    $("#paper-list").innerHTML = papers.slice(0, 10).map((paper) => `
        <a class="paper-item" href="${paper.url}" target="_blank" rel="noreferrer">
            <span>${paper.year || "n/a"}</span>
            <strong>${paper.title}</strong>
            <p>${short(paper.mechanism || paper.why_it_matters, 130)}</p>
        </a>
    `).join("");
}

function renderModules(audit) {
    $("#module-list").innerHTML = (audit.module_decisions || []).map((item) => `
        <div class="module-row">
            <code>${item.path}</code>
            <strong>${item.decision}</strong>
            <p>${item.reason}</p>
            <span>${item.replacement}</span>
        </div>
    `).join("");
}

async function main() {
    const [agenda, audit, interventions, obligations, literature, literatureRecords, ontology, candidates, experiments, results, dequantization, proofStatus, negatives, rejected] = await Promise.all([
        loadJson("research/agenda.json", {}),
        loadJson("research/exhaustive_audit.json", {}),
        loadJson("research/interventions.json", []),
        loadJson("research/proof_obligations.json", []),
        loadJson("research/literature_index.json", {}),
        loadJson("research/literature_records.json", []),
        loadJson("research/problem_ontology.json", {}),
        loadJson("research/registry/candidates.json", []),
        loadJson("research/registry/experiments.json", []),
        loadJson("research/registry/experiment_results.json", []),
        loadJson("research/registry/dequantization_checks.json", []),
        loadJson("research/registry/proof_status.json", []),
        loadJson("research/registry/negative_results.json", []),
        loadJson("research/registry/rejected_candidates.json", []),
    ]);

    renderDiagnosis(agenda);
    renderCounts(candidates, experiments, results, dequantization, proofStatus, negatives, rejected, obligations);
    renderArchitecture(audit);
    renderInterventions(interventions);
    renderLeads(candidates);
    renderExperiments(experiments);
    renderResults(results);
    renderDequantization(dequantization);
    renderProofStatus(proofStatus);
    renderNegativeResults(negatives);
    renderRejectedCandidates(rejected);
    renderProofGate(obligations);
    renderBarriers(ontology);
    renderPapers(literatureRecords, literature);
    renderModules(audit);
}

document.addEventListener("DOMContentLoaded", main);
