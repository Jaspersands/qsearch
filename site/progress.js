const snapshotPath = "research/progress_snapshot.json";

function escapeHtml(value) {
    return String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

function setText(id, value) {
    const node = document.getElementById(id);
    if (node) node.textContent = value;
}

function renderMetrics(metrics) {
    setText("metric-experiments", metrics.experiments);
    setText("metric-results", metrics.results);
    setText("metric-blockers", metrics.blocking_findings);
    setText("metric-negatives", metrics.negative_results);
    setText("metric-debts", metrics.proof_debts);
}

function renderTracks(tracks) {
    const container = document.getElementById("track-list");
    container.innerHTML = tracks.map((track) => `
        <article class="track-row">
            <div class="track-title">
                <h3>${escapeHtml(track.title)}</h3>
                <span class="status-label ${escapeHtml(track.tone)}">${escapeHtml(track.status)}</span>
            </div>
            <div class="track-summary">
                <p>${escapeHtml(track.summary)}</p>
                <p><strong>Evidence:</strong> ${escapeHtml(track.evidence)}</p>
            </div>
            <div class="track-next">
                <strong>Next proof target</strong>
                ${escapeHtml(track.next)}
            </div>
        </article>
    `).join("");
}

function renderMilestones(milestones) {
    const container = document.getElementById("milestone-list");
    container.innerHTML = milestones.map((item, index) => `
        <article class="milestone">
            <span class="milestone-index">${String(index + 1).padStart(2, "0")}</span>
            <div>
                <h3>${escapeHtml(item.title)}</h3>
                <p>${escapeHtml(item.detail)}</p>
            </div>
        </article>
    `).join("");
}

function renderConjecture(conjecture) {
    setText("conjecture-summary", conjecture.summary);
    const facts = document.getElementById("conjecture-facts");
    facts.innerHTML = conjecture.facts.map((fact) => `
        <div><dt>${escapeHtml(fact.label)}</dt><dd>${escapeHtml(fact.value)}</dd></div>
    `).join("");
}

function renderNext(actions) {
    const container = document.getElementById("next-list");
    container.innerHTML = actions.map((action) => `
        <li><strong>${escapeHtml(action.title)}</strong><p>${escapeHtml(action.detail)}</p></li>
    `).join("");
}

function drawProgressMap(tracks) {
    const canvas = document.getElementById("signal-canvas");
    const rect = canvas.getBoundingClientRect();
    const ratio = window.devicePixelRatio || 1;
    canvas.width = Math.max(1, Math.round(rect.width * ratio));
    canvas.height = Math.max(1, Math.round(rect.height * ratio));
    const ctx = canvas.getContext("2d");
    ctx.scale(ratio, ratio);

    const width = rect.width;
    const height = rect.height;
    const left = width < 520 ? 78 : 116;
    const right = 20;
    const top = 40;
    const rowGap = (height - 70) / Math.max(1, tracks.length);
    const stageGap = (width - left - right) / 4;

    ctx.clearRect(0, 0, width, height);
    ctx.font = width < 520 ? "500 10px Inter" : "600 12px Inter";
    ctx.textBaseline = "middle";

    tracks.forEach((track, row) => {
        const y = top + rowGap * row + rowGap / 2;
        ctx.fillStyle = "#454a43";
        const label = width < 520 ? track.short_title : track.title;
        ctx.fillText(label, 0, y);

        ctx.strokeStyle = "#d8ddd4";
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(left, y);
        ctx.lineTo(width - right, y);
        ctx.stroke();

        const activeEnd = left + stageGap * track.stage;
        ctx.strokeStyle = "#176c4a";
        ctx.lineWidth = 4;
        ctx.beginPath();
        ctx.moveTo(left, y);
        ctx.lineTo(activeEnd, y);
        ctx.stroke();

        for (let stage = 0; stage < 5; stage += 1) {
            const x = left + stageGap * stage;
            ctx.beginPath();
            ctx.arc(x, y, stage <= track.stage ? 5 : 4, 0, Math.PI * 2);
            ctx.fillStyle = stage <= track.stage ? "#176c4a" : "#ffffff";
            ctx.fill();
            ctx.strokeStyle = stage <= track.stage ? "#176c4a" : "#aeb5ac";
            ctx.lineWidth = 2;
            ctx.stroke();
        }

        if (track.stage < 4) {
            const blockedX = left + stageGap * (track.stage + 1);
            ctx.strokeStyle = "#a43d2b";
            ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.moveTo(blockedX - 5, y - 5);
            ctx.lineTo(blockedX + 5, y + 5);
            ctx.moveTo(blockedX + 5, y - 5);
            ctx.lineTo(blockedX - 5, y + 5);
            ctx.stroke();
        }
    });
}

async function main() {
    try {
        const response = await fetch(`${snapshotPath}?v=${Date.now()}`);
        if (!response.ok) throw new Error(`Snapshot request failed: ${response.status}`);
        const snapshot = await response.json();
        setText("verdict-title", snapshot.verdict.title);
        setText("verdict-detail", snapshot.verdict.detail);
        setText("last-updated", `Research snapshot ${snapshot.updated_at}`);
        setText("overview-copy", snapshot.overview);
        setText("execution-copy", snapshot.execution_model);
        renderMetrics(snapshot.metrics);
        renderTracks(snapshot.tracks);
        renderMilestones(snapshot.milestones);
        renderConjecture(snapshot.active_conjecture);
        renderNext(snapshot.next_actions);
        drawProgressMap(snapshot.tracks);
        window.addEventListener("resize", () => drawProgressMap(snapshot.tracks));
    } catch (error) {
        console.error(error);
        setText("verdict-title", "Progress snapshot unavailable");
        setText("verdict-detail", "The raw research artifacts remain available through the repository links.");
    }
}

document.addEventListener("DOMContentLoaded", main);
