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
    setText("metric-experiments", Number(metrics.experiments).toLocaleString());
    setText("metric-results", Number(metrics.results).toLocaleString());
    setText("metric-blockers", Number(metrics.blocking_findings).toLocaleString());
    setText("metric-negatives", Number(metrics.negative_results).toLocaleString());
    setText("metric-debts", Number(metrics.proof_debts).toLocaleString());
}

/* =============================================================
   COMPONENT A: INTERACTIVE RESEARCH WORKBENCH
   ============================================================= */

const trackExtendedMetadata = {
    "Nonabelian coset states": {
        domain: "Symmetric Group (S_n) HSP & Graph Isomorphism",
        mechanism: "Two-QFT subgroup carrier extraction with implicit copy preservation and synthesized third commutant generator $T_{T1} + c T_{C1}$ ($c \\neq 0$).",
        attackSuite: "Weisfeiler-Leman graph invariants, character table contraction, and weak-Fourier trace decay audit.",
        barrier: "Natural weak-Fourier mass vanishes factorially ($O(n^9 / (n!)^3)$). Postselecting fixed sectors is obstructed; must adapt across typical high-dimensional partitions.",
        reproduceCmd: 'pytest tests/ -k "coset or commutant"'
    },
    "Hidden shift / DHSP": {
        domain: "Dihedral Group (D_N) Hidden Subgroup Problem",
        mechanism: "Gowers-sieve coset state nearest-plane lattice decoding for reflection vector recovery.",
        attackSuite: "Sieve accounting, random-label LLL basis reduction, and brute-force target censuses ($16.7\\times 10^6$ assignments).",
        barrier: "Fixed-depth nearest-plane lists collapse exponentially at scale. Small-n success was a finite dimension artifact.",
        reproduceCmd: 'pytest tests/test_classical_baseline_suite.py -k "dhs"'
    },
    "Code equivalence": {
        domain: "Permutation Code Equivalence (Goppa / McEliece Cryptosystems)",
        mechanism: "High-weight syzygy collective quantum invariants and dual code commutant projectors.",
        attackSuite: "Hull projector reduction, Schur product invariants, and classical information-set decoding.",
        barrier: "An automated classical hull-projector attack resolved Goppa syzygy collisions in polynomial classical time ($O(n^3)$), fully dequantizing the mechanism.",
        reproduceCmd: 'pytest tests/test_classical_baseline_suite.py -k "code"'
    }
};

let currentTracksData = [];

function selectWorkbenchTrack(index) {
    const track = currentTracksData[index];
    if (!track) return;

    // Update tab active states
    const tabBtns = document.querySelectorAll(".track-tab-btn");
    tabBtns.forEach((btn, i) => {
        if (i === index) {
            btn.classList.add("active");
        } else {
            btn.classList.remove("active");
        }
    });

    const meta = trackExtendedMetadata[track.title] || {
        domain: "Quantum Algorithmic Target",
        mechanism: track.summary,
        attackSuite: "Classical baseline falsification suites.",
        barrier: "Empirical complexity bounds.",
        reproduceCmd: "pytest tests/"
    };

    const isBlocked = track.tone === "blocked";
    const statusClass = isBlocked ? "blocked" : "active";

    const dossierContainer = document.getElementById("workbench-dossier");
    if (!dossierContainer) return;

    dossierContainer.innerHTML = `
        <div class="dossier-top">
            <div class="dossier-heading">
                <h3>${escapeHtml(track.title)}</h3>
                <span class="dossier-domain">${escapeHtml(meta.domain)}</span>
            </div>
            <span class="status-label ${statusClass}">${escapeHtml(track.status)}</span>
        </div>

        <div class="dossier-sections-grid">
            <div class="dossier-block">
                <span class="dossier-block-label">Candidate Quantum Mechanism</span>
                <p>${meta.mechanism}</p>
            </div>
            <div class="dossier-block">
                <span class="dossier-block-label">Classical Attack Suite</span>
                <p>${meta.attackSuite}</p>
            </div>
        </div>

        <div class="dossier-highlight-box ${isBlocked ? 'danger' : 'success'}">
            <span class="dossier-block-label" style="color: ${isBlocked ? 'var(--rust)' : 'var(--green)'};">
                ${isBlocked ? 'Falsification Barrier & Dequantization Verdict' : 'Certified Empirical Evidence & Open Proof Debt'}
            </span>
            <p style="font-size: 0.92rem; margin-top: 4px;">
                ${isBlocked ? meta.barrier : escapeHtml(track.evidence)}
            </p>
        </div>

        <div class="dossier-block" style="margin-bottom: 24px;">
            <span class="dossier-block-label">Next Formal Proof Obligation</span>
            <p style="font-size: 0.92rem; color: var(--ink-prose);">${escapeHtml(track.next)}</p>
        </div>

        <div class="dossier-action-row">
            <div class="dossier-command-snippet">
                <code>${escapeHtml(meta.reproduceCmd)}</code>
                <button class="copy-cmd-btn" onclick="copySnippet('${escapeHtml(meta.reproduceCmd)}', this)">Copy</button>
            </div>
            <span style="font-family: var(--mono); font-size: 0.72rem; color: var(--muted-light);">
                Stage ${track.stage} of 4 &bull; ${isBlocked ? 'Survival Cut' : 'Surviving Active'}
            </span>
        </div>
    `;

    triggerKaTeX();
}

function renderWorkbench(tracks) {
    currentTracksData = tracks;
    const tabContainer = document.getElementById("workbench-tabs");
    if (!tabContainer) return;

    tabContainer.innerHTML = tracks.map((track, index) => {
        const isBlocked = track.tone === "blocked";
        return `
            <button class="track-tab-btn ${index === 0 ? 'active' : ''} ${isBlocked ? 'tone-blocked' : ''}" 
                    onclick="selectWorkbenchTrack(${index})" 
                    role="tab" 
                    aria-selected="${index === 0}">
                <div class="tab-title">${escapeHtml(track.title)}</div>
                <div class="tab-meta">
                    <span class="status-label ${isBlocked ? 'blocked' : 'active'}">${escapeHtml(track.short_title)}</span>
                    <span class="stage-pill">Stage ${track.stage}/4</span>
                </div>
            </button>
        `;
    }).join("");

    // Automatically select the active track (or the first one)
    const activeIndex = tracks.findIndex(t => t.tone === "active");
    selectWorkbenchTrack(activeIndex !== -1 ? activeIndex : 0);
}

/* =============================================================
   COMPONENT B: FALSIFICATION MATRIX FILTER
   ============================================================= */

function filterMatrix(category, buttonNode) {
    const buttons = document.querySelectorAll(".matrix-filter-btn");
    buttons.forEach(b => b.classList.remove("active"));
    if (buttonNode) buttonNode.classList.add("active");

    const rows = document.querySelectorAll("#matrix-tbody tr");
    rows.forEach(row => {
        const group = row.getAttribute("data-group");
        if (category === "all" || group === category) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }
    });
}
window.filterMatrix = filterMatrix;

/* =============================================================
   COMPONENT C: VECTOR SVG PIPELINE MAP
   ============================================================= */

function renderVectorPipeline(tracks) {
    const svg = document.getElementById("pipeline-svg");
    if (!svg) return;

    const width = 1000;
    const height = 240;
    const leftMargin = 220;
    const rightMargin = 60;
    const usableWidth = width - leftMargin - rightMargin;
    const stageGap = usableWidth / 4;
    const rowGap = height / (tracks.length + 1);

    let content = `
        <defs>
            <linearGradient id="activeGrad" x1="0" y1="0" x2="1" y2="0">
                <stop offset="0%" stop-color="#0E5B37" stop-opacity="0.3"/>
                <stop offset="100%" stop-color="#0E5B37" stop-opacity="1"/>
            </linearGradient>
            <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="3" result="glow"/>
                <feComposite in="SourceGraphic" in2="glow" operator="over"/>
            </filter>
        </defs>
    `;

    tracks.forEach((track, rowIdx) => {
        const y = rowGap * (rowIdx + 1);
        const isBlocked = track.tone === "blocked";
        const survivedX = leftMargin + stageGap * track.stage;

        // Track Name & Status
        content += `
            <text x="20" y="${y + 4}" font-family="'Newsreader', Georgia, serif" font-size="15" font-weight="600" fill="#121514">
                ${escapeHtml(track.title)}
            </text>
            <text x="20" y="${y + 18}" font-family="'IBM Plex Mono', monospace" font-size="9.5" fill="#768078">
                ${isBlocked ? 'Route Falsified' : 'Active Frontier'}
            </text>
        `;

        // Baseline Track Line
        content += `
            <line x1="${leftMargin}" y1="${y}" x2="${width - rightMargin}" y2="${y}" 
                  stroke="#E4E1D7" stroke-width="2" stroke-linecap="round"/>
        `;

        // Surviving Green Segment
        content += `
            <line x1="${leftMargin}" y1="${y}" x2="${survivedX}" y2="${y}" 
                  stroke="#0E5B37" stroke-width="4" stroke-linecap="round"/>
        `;

        // Stage Nodes
        for (let stage = 0; stage < 5; stage++) {
            const x = leftMargin + stageGap * stage;
            const isPassed = stage <= track.stage;
            const isCurrent = stage === track.stage;

            if (isPassed) {
                content += `
                    <circle cx="${x}" cy="${y}" r="6" fill="#0E5B37" stroke="#FFFFFF" stroke-width="2"/>
                `;
                if (isCurrent && !isBlocked) {
                    content += `
                        <circle cx="${x}" cy="${y}" r="11" fill="none" stroke="#0E5B37" stroke-width="1.5" opacity="0.6">
                            <animate attributeName="r" values="7;13;7" dur="2.4s" repeatCount="indefinite"/>
                            <animate attributeName="opacity" values="0.8;0;0.8" dur="2.4s" repeatCount="indefinite"/>
                        </circle>
                    `;
                }
            } else {
                content += `
                    <circle cx="${x}" cy="${y}" r="4.5" fill="#FFFFFF" stroke="#CFCBC0" stroke-width="1.5"/>
                `;
            }
        }

        // Falsified Red Cross at stage + 1
        if (isBlocked && track.stage < 4) {
            const blockedX = leftMargin + stageGap * (track.stage + 1);
            content += `
                <g stroke="#9E2A2B" stroke-width="2.5" stroke-linecap="round">
                    <line x1="${blockedX - 6}" y1="${y - 6}" x2="${blockedX + 6}" y2="${y + 6}"/>
                    <line x1="${blockedX + 6}" y1="${y - 6}" x2="${blockedX - 6}" y2="${y + 6}"/>
                </g>
                <text x="${blockedX}" y="${y + 18}" text-anchor="middle" font-family="'IBM Plex Mono', monospace" font-size="8.5" font-weight="600" fill="#9E2A2B">
                    FALSIFIED
                </text>
            `;
        }
    });

    svg.innerHTML = content;
}

/* =============================================================
   COMPONENT E: TERMINAL TABS & COPY ACTIONS
   ============================================================= */

const terminalCommands = {
    fast: {
        text: `# 1. Fast smoke check of classical dequantization baselines\ngit clone https://github.com/Jaspersands/qsearch.git\ncd qsearch && pip install -r requirements.txt\npytest tests/test_classical_baseline_suite.py -k "smoke"`,
        raw: `pytest tests/test_classical_baseline_suite.py -k "smoke"`
    },
    baseline: {
        text: `# 2. Run the complete automated classical attack suite\npytest tests/test_classical_baseline_suite.py`,
        raw: `pytest tests/test_classical_baseline_suite.py`
    },
    coset: {
        text: `# 3. Verify nonabelian commutant operator separation (n=8, 9)\npytest tests/ -k "coset or commutant"`,
        raw: `pytest tests/ -k "coset or commutant"`
    },
    negatives: {
        text: `# 4. Validate the 914 machine-readable negative result records\npython3 -m pytest tests/ -k "negative"`,
        raw: `python3 -m pytest tests/ -k "negative"`
    }
};

let activeTermKey = "fast";

function switchTermTab(key, btn) {
    activeTermKey = key;
    const tabBtns = document.querySelectorAll(".term-tab-btn");
    tabBtns.forEach(b => b.classList.remove("active"));
    if (btn) btn.classList.add("active");

    const display = document.getElementById("terminal-code-display");
    if (!display) return;

    const data = terminalCommands[key];
    if (data) {
        display.innerHTML = escapeHtml(data.text)
            .replace(/^#.+$/gm, '<span class="t-comment">$&</span>')
            .replace(/(pytest|python3|git|cd|pip install)/g, '<span class="t-cmd">$1</span>');
    }
}
window.switchTermTab = switchTermTab;

function copyActiveTermCommand() {
    const data = terminalCommands[activeTermKey];
    if (!data) return;

    navigator.clipboard.writeText(data.raw).then(() => {
        const btn = document.getElementById("copy-term-btn");
        if (btn) {
            const old = btn.textContent;
            btn.textContent = "Copied!";
            setTimeout(() => { btn.textContent = old; }, 2000);
        }
    }).catch(err => {
        console.error("Clipboard copy failed:", err);
    });
}
window.copyActiveTermCommand = copyActiveTermCommand;

function copySnippet(text, btn) {
    navigator.clipboard.writeText(text).then(() => {
        if (btn) {
            const old = btn.textContent;
            btn.textContent = "Copied!";
            setTimeout(() => { btn.textContent = old; }, 1800);
        }
    });
}
window.copySnippet = copySnippet;

function copyBibtex() {
    const node = document.getElementById("bibtex-text");
    if (!node) return;
    navigator.clipboard.writeText(node.textContent).then(() => {
        const btn = document.querySelector(".citation-header .copy-cmd-btn");
        if (btn) {
            const old = btn.textContent;
            btn.textContent = "Copied!";
            setTimeout(() => { btn.textContent = old; }, 2000);
        }
    });
}
window.copyBibtex = copyBibtex;

/* =============================================================
   MILESTONES, CONJECTURE & KATEX
   ============================================================= */

const milestoneMetadata = {
    "The stable coupling-tree interface is complete": {
        takeaway: "Constructed an exact polynomial-time coordinate mapping for all 25 encoded labels across both coupling trees.",
        category: "Algebraic Interface",
        badgeClass: "active"
    },
    "The stable three-copy frame is filterable": {
        takeaway: "Proved an exact inverse-polynomial spectral gap between involution families: $\\lambda_{\\min}(F) \\ge \\frac{71}{825}n^{-5}$.",
        category: "Spectral Gap",
        badgeClass: "active"
    },
    "Natural access kills the fixed stable branch": {
        takeaway: "Disproved natural-access state preparation: weak-Fourier sampling mass decays factorially as $\\frac{25}{3}\\frac{n^9}{(n!)^3}$, ruling out generic amplification.",
        category: "No-Go Theorem",
        badgeClass: "blocked"
    },
    "Every fixed bounded-tail route is cut": {
        takeaway: "Proved that bounded-tail Fourier mass vanishes factorially, mandating uniform adaptation across typical high-dimensional partitions.",
        category: "Obstruction",
        badgeClass: "blocked"
    },
    "An independent third generator repairs the known finite collisions": {
        takeaway: "Coupling an independent third generator $T_{T1} + c T_{C1}$ breaks all known spectral degeneracies at $n=8$ ($20/20$ targets) and $n=9$ ($27/27$ targets).",
        category: "Active Invariant",
        badgeClass: "active"
    }
};

function renderMilestones(milestones) {
    const container = document.getElementById("milestone-list");
    if (!container) return;
    container.innerHTML = milestones.map((item, index) => {
        const meta = milestoneMetadata[item.title];
        return `
            <div style="background: var(--paper-card); border: 1px solid var(--line); border-radius: var(--radius-sm); padding: 18px 20px; margin-bottom: 14px; box-shadow: var(--shadow-sm);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <h4 style="font-family: var(--serif); font-size: 1.15rem; font-weight: 600; color: var(--ink-display); margin: 0;">
                        ${escapeHtml(item.title)}
                    </h4>
                    ${meta ? `<span class="status-label ${meta.badgeClass}">${escapeHtml(meta.category)}</span>` : ''}
                </div>
                <p style="font-size: 0.90rem; color: var(--ink-prose); margin-bottom: 8px;">
                    ${meta ? meta.takeaway : escapeHtml(item.detail)}
                </p>
                <details style="font-size: 0.82rem; color: var(--muted); border-top: 1px solid var(--line-subtle); padding-top: 6px;">
                    <summary style="font-family: var(--mono); cursor: pointer; color: var(--muted-light);">Formal Mathematical Bounds</summary>
                    <p style="margin-top: 6px;">${escapeHtml(item.detail)}</p>
                </details>
            </div>
        `;
    }).join("");
}

function renderConjecture(conjecture) {
    setText("conjecture-summary", conjecture.summary);
    const facts = document.getElementById("conjecture-facts");
    if (!facts) return;
    facts.innerHTML = conjecture.facts.map((fact) => `
        <div style="display: flex; justify-content: space-between; border-bottom: 1px solid var(--line-subtle); padding-bottom: 4px;">
            <span style="color: var(--muted-light);">${escapeHtml(fact.label)}</span>
            <strong style="color: var(--ink);">${escapeHtml(fact.value)}</strong>
        </div>
    `).join("");
}

function triggerKaTeX() {
    if (window.renderMathInElement) {
        try {
            renderMathInElement(document.body, {
                delimiters: [
                    {left: "$$", right: "$$", display: true},
                    {left: "$", right: "$", display: false}
                ],
                throwOnError: false
            });
        } catch (e) {
            console.warn("KaTeX rendering warning:", e);
        }
    }
}

/* =============================================================
   INITIALIZATION
   ============================================================= */

async function main() {
    try {
        const response = await fetch(`${snapshotPath}?v=${Date.now()}`);
        if (!response.ok) throw new Error(`Snapshot request failed: ${response.status}`);
        const snapshot = await response.json();

        setText("verdict-title", snapshot.verdict.title);
        setText("verdict-detail", snapshot.verdict.detail);
        setText("last-updated", `Certified snapshot ${snapshot.updated_at}`);
        setText("execution-copy", snapshot.execution_model);

        renderMetrics(snapshot.metrics);
        renderWorkbench(snapshot.tracks);
        renderVectorPipeline(snapshot.tracks);
        renderMilestones(snapshot.milestones);
        renderConjecture(snapshot.active_conjecture);

        triggerKaTeX();
    } catch (error) {
        console.error(error);
        setText("verdict-title", "Progress snapshot unavailable");
        setText("verdict-detail", "Raw research artifacts remain accessible directly via the repository.");
    }
}

document.addEventListener("DOMContentLoaded", () => {
    main();
    setTimeout(triggerKaTeX, 600);
});
