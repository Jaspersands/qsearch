const SEARCH_FIELDS = ["id", "claim", "reason", "lesson", "source"];

export function matchesQuery(record, query) {
  const needle = String(query ?? "").trim().toLowerCase();
  if (!needle) return true;
  return SEARCH_FIELDS.some((field) => String(record[field] ?? "").toLowerCase().includes(needle));
}

export function filterRecords(records, { query = "", tag = "" } = {}) {
  return records.filter((record) => (!tag || record.tags.includes(tag)) && matchesQuery(record, query));
}

export function recordIdFromHash(hash) {
  const raw = String(hash ?? "").replace(/^#/, "");
  if (!raw) return "";
  try {
    return decodeURIComponent(raw);
  } catch {
    return raw;
  }
}
