import test from "node:test";
import assert from "node:assert/strict";
import { groupDebts } from "../../site/js/lib/debts.js";

const debt = (candidate_id, debt_type, priority_score, required_resolution = `fix ${debt_type}`) =>
  ({ candidate_id, debt_type, priority_score, required_resolution });

test("groups by type, highest-priority group first, rows sorted", () => {
  const groups = groupDebts([
    debt("B", "reduction-route", 98),
    debt("C", "dequantization", 100),
    debt("A", "dequantization", 100),
    debt("A", "reduction-route", 99),
  ]);
  assert.deepEqual(groups.map((g) => g.type), ["dequantization", "reduction-route"]);
  assert.deepEqual(groups[0].debts.map((d) => d.candidate_id), ["A", "C"]);
  assert.deepEqual(groups[1].debts.map((d) => d.candidate_id), ["A", "B"]);
  assert.equal(groups[0].resolution, "fix dequantization");
});

test("resolution is null when a group's debts disagree", () => {
  const [group] = groupDebts([debt("A", "falsifier", 90, "one"), debt("B", "falsifier", 90, "two")]);
  assert.equal(group.resolution, null);
});

test("empty input gives no groups", () => {
  assert.deepEqual(groupDebts([]), []);
});
