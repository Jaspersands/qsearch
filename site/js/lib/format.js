export const REPO_URL = "https://github.com/Jaspersands/qsearch";

const ESCAPES = { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" };

export function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, (ch) => ESCAPES[ch]);
}

export function formatNumber(value) {
  return Number(value).toLocaleString("en-US");
}

export function formatDate(isoDate) {
  const [year, month, day] = String(isoDate).slice(0, 10).split("-").map(Number);
  return new Date(Date.UTC(year, month - 1, day)).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
    timeZone: "UTC",
  });
}

export function repoUrl(path) {
  return `${REPO_URL}/blob/main/${String(path).split("/").map(encodeURIComponent).join("/")}`;
}

const STATUS_LABELS = { open: "open", "ruled-out": "ruled out", active: "active" };

export function statusMarker(kind) {
  return `<span class="status status-${kind}">${STATUS_LABELS[kind]}</span>`;
}

export function trackStatusKind(tone) {
  return tone === "active" ? "active" : "open";
}

const ACRONYMS = new Set(["cfi", "dcp", "dhsp", "hsp", "pgm", "qft", "wl"]);

export function humanizeId(id) {
  const words = String(id)
    .replace(/[-_]+/g, " ")
    .trim()
    .toLowerCase()
    .split(/\s+/)
    .map((word) => (ACRONYMS.has(word) ? word.toUpperCase() : word))
    .join(" ");
  return words.charAt(0).toUpperCase() + words.slice(1);
}

export function bibtexEntry(snapshot) {
  return [
    "@misc{sands2026qsearch,",
    "  author       = {Sands, Jasper},",
    "  title        = {Q-Search: an open search for structural quantum speedups},",
    "  year         = {2026},",
    "  howpublished = {\\url{https://qsearch.jaspersands.com}},",
    `  note         = {Snapshot of ${snapshot.updated_at}; ${formatNumber(snapshot.metrics.negative_results)} negative results recorded}`,
    "}",
  ].join("\n");
}
