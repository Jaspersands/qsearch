import { REPO_URL, escapeHtml, formatDate } from "./lib/format.js";

export const SNAPSHOT_PATH = "research/progress_snapshot.json";

export async function loadJson(path) {
  const response = await fetch(path, { cache: "no-cache" });
  if (!response.ok) throw new Error(`${path}: HTTP ${response.status}`);
  return response.json();
}

export function showLoadError(container, path) {
  if (!container) return;
  container.innerHTML =
    `<p class="load-error">This part of the page couldn't load <code>${escapeHtml(path)}</code>. ` +
    `<a href="${REPO_URL}/blob/main/${escapeHtml(path)}">Read the file on GitHub</a>.</p>`;
}

export function setText(id, value) {
  const node = document.getElementById(id);
  if (node) node.textContent = value;
}

export function bindCopyButtons(root = document) {
  for (const button of root.querySelectorAll("button[data-copy]")) {
    button.addEventListener("click", async () => {
      const source = document.getElementById(button.dataset.copy);
      if (!source) return;
      try {
        await navigator.clipboard.writeText(source.textContent.trim());
        button.textContent = "Copied";
      } catch {
        button.textContent = "Copy failed";
      }
      setTimeout(() => {
        button.textContent = "Copy";
      }, 1600);
    });
  }
}

export function initFooter(snapshotPromise = loadJson(SNAPSHOT_PATH)) {
  snapshotPromise
    .then((snapshot) => {
      for (const node of document.querySelectorAll("[data-updated]")) {
        node.textContent = formatDate(snapshot.updated_at);
        node.setAttribute("datetime", snapshot.updated_at);
      }
    })
    .catch(() => {});
}
