function byPriorityThenCandidate(a, b) {
  return b.priority_score - a.priority_score || a.candidate_id.localeCompare(b.candidate_id);
}

export function groupDebts(debts) {
  const groups = new Map();
  for (const debt of debts) {
    if (!groups.has(debt.debt_type)) {
      groups.set(debt.debt_type, { type: debt.debt_type, resolution: debt.required_resolution, debts: [] });
    }
    const group = groups.get(debt.debt_type);
    if (group.resolution !== debt.required_resolution) group.resolution = null;
    group.debts.push(debt);
  }
  const topPriority = (group) => Math.max(...group.debts.map((debt) => debt.priority_score));
  return [...groups.values()]
    .map((group) => ({ ...group, debts: [...group.debts].sort(byPriorityThenCandidate) }))
    .sort((a, b) => topPriority(b) - topPriority(a) || a.type.localeCompare(b.type));
}
