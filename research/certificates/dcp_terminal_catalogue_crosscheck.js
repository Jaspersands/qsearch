// Independent arithmetic controls, NOT independent theorem verification.
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const assert = require('assert/strict');

const root = path.resolve(__dirname, '../..');
const report = JSON.parse(fs.readFileSync(path.join(root,
  'research/classical_baselines/dcp_subset_sum_terminal_catalogue.json'), 'utf8'));
const bitlen = n => n === 0n ? 0 : n.toString(2).length;
const sqrt = n => {
  let x = 1n << BigInt(Math.ceil(bitlen(n) / 2));
  for (;;) {
    const y = (x + n / x) / 2n;
    if (y >= x) return x;
    x = y;
  }
};
const gcd = (a, b) => {
  while (b) [a, b] = [b, a % b];
  return a;
};
const fraction = (n, d = 1n) => {
  const g = gcd(n, d);
  return [n / g, d / g];
};
const add = (a, b) => fraction(a[0] * b[1] + b[0] * a[1], a[1] * b[1]);
const multiply = (a, b) => fraction(a[0] * b[0], a[1] * b[1]);
const readFraction = x => fraction(BigInt(x.numerator), BigInt(x.denominator));
const lessEqual = (a, b) => a[0] * b[1] <= b[0] * a[1];
const falling = (x, k) => {
  let out = 1n;
  for (let i = 0; i < k; i++) out *= BigInt(Math.max(0, x - i));
  return out;
};

for (const row of report.scaling_rows) {
  const n = row.n_bits, k = row.moment_order, c = row.register_offset, m = n + c;
  let maximum = -Infinity, terms = 0;
  for (let r = 2; r <= Math.min(k, m + 1); r++) {
    const h = sqrt(BigInt(r) ** BigInt(r));
    const g = r - 1 + bitlen(h) - 1;
    const exponent = bitlen(h - 1n) + k * g + r * c - (r === k ? m : 2 * Math.floor(m / 5));
    maximum = Math.max(maximum, exponent);
    terms++;
  }
  assert.equal(maximum + bitlen(BigInt(terms - 1)), row.certified_binary_exponent_upper_bound);
}

// Dynamic convolution is independent of the Python assignment enumeration.
const groups = new Map();
for (const row of report.exact_source_moment_controls) {
  const key = `${row.n_bits},${row.register_offset}`;
  if (!groups.has(key)) {
    const n = row.n_bits, m = n + row.register_offset, N = 2 ** n;
    const histogram = Array(2 ** m + 1).fill(0n);
    for (let source = 0; source < N ** m; source++) {
      let x = source, distribution = Array(N).fill(0n);
      distribution[0] = 1n;
      for (let j = 0; j < m; j++) {
        const a = x % N;
        x = Math.floor(x / N);
        distribution = distribution.map((value, s) => value + distribution[(s - a + N) % N]);
      }
      for (const count of distribution) histogram[Number(count)]++;
    }
    groups.set(key, histogram);
  }
  let numerator = 0n;
  groups.get(key).forEach((count, c) => numerator += count * falling(c, row.moment_order));
  assert.deepEqual(fraction(numerator, BigInt(row.joint_target_count)), readFraction(row.exact_factorial_moment));
  assert.deepEqual(fraction(falling(2 ** (row.n_bits + row.register_offset), row.moment_order),
    BigInt(2 ** row.n_bits) ** BigInt(row.moment_order)), readFraction(row.independent_map_baseline));
}

const bad = (tuple, m) => {
  const k = tuple.length, columns = [(1 << k) - 1];
  for (let j = 0; j < m; j++) columns.push(tuple.reduce((a, b, i) => a | (((b >> j) & 1) << i), 0));
  const basis = {};
  let rank = 0;
  for (let x of columns) while (x) {
    const pivot = 31 - Math.clz32(x);
    if (basis[pivot] === undefined) {
      basis[pivot] = x;
      rank++;
      break;
    }
    x ^= basis[pivot];
  }
  return rank < k;
};
const choose = (a, k, visit, start = 0, prefix = []) => {
  if (prefix.length === k) return visit(prefix);
  for (let i = start; i <= a.length - (k - prefix.length); i++) choose(a, k, visit, i + 1, [...prefix, a[i]]);
};
const factorial = k => {
  let x = 1;
  for (let i = 2; i <= k; i++) x *= i;
  return x;
};
const events = {}, perLabel = {};
for (let k = 2; k <= 4; k++) { events[k] = 0n; perLabel[k] = fraction(0n); }
let inverseSum = fraction(0n), weightedChecks = 0;
for (let source = 0; source < 64; source++) {
  const a = [source % 4, Math.floor(source / 4) % 4, Math.floor(source / 16) % 4];
  const fibers = Array.from({length: 4}, () => []);
  for (let b = 0; b < 8; b++) fibers[a.reduce((s, x, j) => s + ((b >> j & 1) ? x : 0), 0) % 4].push(b);
  const legal = fibers.filter(f => f.length).length;
  inverseSum = add(inverseSum, fraction(4n, BigInt(legal)));
  for (const fiber of fibers) {
    const D = {};
    for (let k = 2; k <= 5; k++) {
      let count = 0;
      choose(fiber, k, tuple => { if (bad(tuple, 3)) count++; });
      D[k] = count * factorial(k);
    }
    for (let k = 2; k <= 4; k++) {
      assert(fiber.length * D[k] <= k * D[k] + D[k + 1]);
      weightedChecks++;
      if (D[k]) {
        events[k]++;
        perLabel[k] = add(perLabel[k], fraction(1n, BigInt(legal)));
      }
    }
  }
}
const inverseMean = multiply(inverseSum, fraction(1n, 64n));
assert.deepEqual(inverseMean, readFraction(report.weighted_bad_tuple_controls.expected_inverse_legal_fraction));
assert(lessEqual(inverseMean, fraction(3n, 2n)));
for (const row of report.weighted_bad_tuple_controls.rows) {
  const eta = fraction(events[row.moment_order], 256n);
  const p = multiply(perLabel[row.moment_order], fraction(1n, 64n));
  assert.deepEqual(eta, readFraction(row.uniform_target_bad_event_probability));
  assert.deepEqual(p, readFraction(row.per_label_uniform_legal_bad_event_probability));
  assert(lessEqual(multiply(p, p), multiply(inverseMean, eta)));
}
assert.equal(weightedChecks, report.weighted_bad_tuple_controls.per_instance_inequality_checks);
for (const [file, hash] of Object.entries(report.dependency_sha256)) {
  assert.equal(crypto.createHash('sha256').update(fs.readFileSync(path.join(root, file))).digest('hex'), hash);
}
assert.equal(report.claim_gate.independent_theorem_review, false);
assert.equal(report.claim_gate.quantum_algorithm, false);
console.log(JSON.stringify({status: 'ARITHMETIC_CROSSCHECK_ONLY',
  integer_scaling_bounds: report.scaling_rows.length,
  independent_source_moments: report.exact_source_moment_controls.length,
  weighted_prefix_inequalities: weightedChecks, per_label_legal_laws: 3,
  dependency_hashes: Object.keys(report.dependency_sha256).length}));
