import test from "node:test";
import assert from "node:assert/strict";
import { STAGES, aliveAt, circuitStrip, circuitSvg, wireExtents, wirePlan } from "../../site/js/lib/circuit.js";

const tracks = [
  { title: "Hidden shift / DHSP", short_title: "DHSP", stage: 2, tone: "blocked" },
  { title: "Code equivalence", short_title: "Codes", stage: 1, tone: "blocked" },
  { title: "Nonabelian coset states", short_title: "Cosets", stage: 3, tone: "active" },
];
const gateYs = [40, 300, 600, 900, 1500];

const count = (text, pattern) => (text.match(pattern) || []).length;

test("STAGES lists the five gates in order", () => {
  assert.deepEqual(STAGES, ["hypothesis", "structure", "classical attack", "proof gate", "separation"]);
});

test("wirePlan ends blocked tracks one gate after their stage and keeps active ones open", () => {
  assert.deepEqual(wirePlan(tracks), [
    { label: "DHSP", active: false, solidTo: 3, endsAt: 3 },
    { label: "Codes", active: false, solidTo: 2, endsAt: 2 },
    { label: "Cosets", active: true, solidTo: 3, endsAt: null },
  ]);
});

test("wirePlan caps blocked tracks at the proof gate and falls back to the title", () => {
  assert.deepEqual(wirePlan([{ title: "Late", stage: 3, tone: "blocked" }]), [
    { label: "Late", active: false, solidTo: 3, endsAt: 3 },
  ]);
  assert.deepEqual(wirePlan([{ title: "Odd", stage: "x", tone: "active" }]), [
    { label: "Odd", active: true, solidTo: 0, endsAt: null },
  ]);
});

test("aliveAt keeps ended wires up to and including their last gate", () => {
  const [dhsp, codes, cosets] = wirePlan(tracks);
  assert.equal(aliveAt(codes, 2), true);
  assert.equal(aliveAt(codes, 3), false);
  assert.equal(aliveAt(dhsp, 3), true);
  assert.equal(aliveAt(dhsp, 4), false);
  assert.equal(aliveAt(cosets, 4), true);
});

test("wireExtents spaces wires evenly and ends them at the meter or the last gate", () => {
  assert.deepEqual(wireExtents(wirePlan(tracks), gateYs, 150), [
    { x: 22, end: 930 },
    { x: 75, end: 630 },
    { x: 128, end: 1500 },
  ]);
});

test("circuitSvg draws five gates, a meter per ended wire, one dashed wire, and one dot", () => {
  const plan = wirePlan(tracks);
  const svg = circuitSvg({ plan, gateYs, height: 1560, width: 150 });
  assert.ok(svg.startsWith('<svg viewBox="0 0 150 1560"'));
  assert.equal(count(svg, /class="gate"/g), 5);
  assert.equal(count(svg, /class="meter"/g), 2);
  assert.equal(count(svg, /wire-dash/g), 1);
  assert.equal(count(svg, /class="circuit-dot"/g), 1);
  assert.equal(count(svg, /class="wire-live"/g), 3);
  assert.ok(svg.includes(">classical attack<"));
  assert.ok(svg.includes(">?<"));
  // The proof gate spans only DHSP (x=22) and Cosets (x=128), so 14 px either side.
  assert.ok(svg.includes('<g class="gate" data-gate="3"><rect x="8" y="888" width="134" height="24"'));
});

test("circuitSvg uses single-letter gate labels in a narrow gutter", () => {
  const svg = circuitSvg({ plan: wirePlan(tracks), gateYs, height: 1560, width: 60 });
  assert.ok(svg.includes(">A<"));
  assert.ok(!svg.includes(">classical attack<"));
  assert.ok(svg.includes(">?<"));
  assert.ok(!svg.includes(">DHSP<"), "wire labels would collide in a 60 px gutter");
  assert.ok(svg.includes('x1="12"'), "narrow wires use a 12 px margin");
});

test("circuitStrip draws the same ends horizontally", () => {
  const svg = circuitStrip({ plan: wirePlan(tracks), width: 900 });
  assert.ok(svg.startsWith('<svg viewBox="0 0 900 64"'));
  assert.equal(count(svg, /class="meter"/g), 2);
  assert.equal(count(svg, /wire-dash/g), 1);
  assert.equal(count(svg, /class="strip-q"/g), 1);
  assert.equal(count(svg, /class="strip-stage"/g), 5);
});
