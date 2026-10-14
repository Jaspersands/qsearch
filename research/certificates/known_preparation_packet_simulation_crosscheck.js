"use strict";
// Independent rational enclosure replay and exact Q(zeta9) adaptive channels.
const fs = require("fs"), path = require("path"), crypto = require("crypto");
const E = require("./cyclotomic_exact.js");
const {check, same, rat, parse, str, add, sub, mul, div, cmp, field, matrices} = E;
const ROOT = path.resolve(__dirname, "../.."), REPORT = path.join(ROOT, "research/classical_baselines/known_preparation_packet_simulation.json");
const ACCESS = "ORIGINAL_CLASSICAL_RECORDS_AND_PREPARATION_RANDOMNESS";
const hash = f => crypto.createHash("sha256").update(fs.readFileSync(f)).digest("hex");
const min = (a, b) => cmp(a, b) <= 0n ? a : b, max = (a, b) => cmp(a, b) >= 0n ? a : b;
const abs = a => a[0] < 0n ? [-a[0], a[1]] : a;
const mod = (a, q) => (a % q + q) % q;
function integer(v) {
  check((typeof v === "number" && Number.isSafeInteger(v)) || (typeof v === "string" && /^-?(0|[1-9][0-9]*)$/.test(v)), "exact integer encoding, not a float or Boolean");
  return BigInt(v);
}
function root(q) {
  let r = q, n = 0;
  while (r % 3n === 0n) {r /= 3n; n++;}
  check(r === 1n && n >= 1, "actual ternary-power phase modulus");
  return n;
}
function packet(q, phases, ids) {
  root(q);
  check([2, 3].includes(phases.length) && phases.every(x => x >= 0n && x < q) && ids.length >= 1 && new Set(ids).size === ids.length, "explicit known point descriptor and paid ancestry");
  return {q, phases, ids: ids.slice().sort()};
}
const savedPacket = p => ({modulus: String(p.q), phase_numerators: p.phases.map(String), original_sources: p.ids, phase_access: ACCESS});
const cmerge = (left, right, v) => packet(left.q, [0, 1, 2].map(t => mod(left.phases[t]+right.phases[(t+v) % 3], left.q)), [...left.ids, ...right.ids]);
const bproject = p => packet(p.q, p.phases.slice(0, 2), p.ids);
const bmerge = (left, right, bit) => packet(left.q, [0, 1].map(t => mod(left.phases[t]+right.phases[t ^ bit], left.q)), [...left.ids, ...right.ids]);
const diagonal = (p, offsets) => packet(p.q, p.phases.map((x, j) => mod(x+offsets[j], p.q)), p.ids);
function source(s) {
  const q = integer(s.modulus), digits = root(q), n = s.dimension, raw = s.original_classical_records, mask = s.preparation_random_mask.map(integer);
  check(s.phase_access === ACCESS && n === 2 && mask.length === n && mask.every(m => m >= 0n && m < q) && raw.length === s.original_record_count && raw.length % 2 === 0, "same complete original classical records and known mask");
  check(s.source_error_law_required_for_simulation === false && s.source_states_or_hidden_secret_read === false, "actual point preparation, not a guessed hidden secret or error");
  check(new Set(raw.map(r => r.source_id)).size === raw.length, "distinct declared original records");
  raw.forEach(r => {
    check(integer(r.modulus) === q && r.label.length === n && r.label.map(integer).every(a => a >= 0n && a < q) && integer(r.value) >= 0n && integer(r.value) < q, "canonical original noisy-linear record");
  });
  check(s.known_source_receipts.length*2 === raw.length, "one prepared qutrit per actual original pair");
  // Derive the even-native trace row without copying the Python frequency helper.
  let u = 2n, v = -1n;
  for (let j = 1; j < 2*digits; j++) [u, v] = [-2n*u-v, u-v];
  const denominator = 3n**BigInt(2*digits);
  check(u*q % denominator === 0n && v*q % denominator === 0n, "exact native trace row");
  u = u*q/denominator; v = v*q/denominator;
  check(u*u+u*v+v*v === 1n, "unimodular original phase-frequency map");
  return s.known_source_receipts.map((r, j) => {
    const pair = raw.slice(2*j, 2*j+2), ids = pair.map(a => a.source_id);
    const values = pair.map(a => mod(integer(a.value)+a.label.map(integer).reduce((sum, x, i) => sum+x*mask[i], 0n), q));
    same(r.raw_source_ids, ids, "actual classical input ancestry");
    same(r.known_phase_values, values.map(String), "phase values computed from original records, not secret/errors");
    const labels = Array.from({length: n}, (_, i) => [mod(u*integer(pair[0].label[i])+v*integer(pair[1].label[i]), q),
                                                   mod((u+v)*integer(pair[0].label[i])-u*integer(pair[1].label[i]), q)]);
    same(r.public_native_ring_label.map(a => a.map(x => String(integer(x)))), labels.map(a => a.map(String)), "correct existing native public label chart");
    const p = packet(q, [0n, ...values], ids);
    same(r.packet, savedPacket(p), "explicit known point state descriptor");
    check(r.hidden_secret_or_errors_used === false, "same-original-data access, no hidden phase oracle");
    return p;
  });
}
const piCache = new Map(), cosineCache = new Map();
function piBox(bits) {
  if (piCache.has(bits)) return piCache.get(bits);
  const tolerance = rat(1n, 2n**BigInt(bits+10));
  function atanBox(d) {
    let total = E.zero, power = BigInt(d), k = 0;
    while (true) {
      total = add(total, rat(k % 2 ? -1n : 1n, BigInt(2*k+1)*power));
      k++; power *= BigInt(d*d);
      const next = rat(k % 2 ? -1n : 1n, BigInt(2*k+1)*power);
      if (cmp(abs(next), tolerance) <= 0n) return [min(total, add(total, next)), max(total, add(total, next))];
    }
  }
  const a = atanBox(5), b = atanBox(239);
  const result = [sub(mul(rat(16n), a[0]), mul(rat(4n), b[1])), sub(mul(rat(16n), a[1]), mul(rat(4n), b[0]))];
  piCache.set(bits, result); return result;
}
function cosine(q, k, bits) {
  k = mod(k, q);
  if (k === 0n) return [E.one, E.one];
  if (k === q/3n || k === 2n*q/3n) return [rat(-1n, 2n), rat(-1n, 2n)];
  k = k < q-k ? k : q-k;
  const key = `${q}:${k}:${bits}`;
  if (cosineCache.has(key)) return cosineCache.get(key);
  const [piL, piH] = piBox(bits), angle = mul(rat(k, q), add(piL, piH)), angleError = mul(rat(k, q), sub(piH, piL));
  const tolerance = rat(1n, 2n**BigInt(bits+8));
  let term = E.one, total = E.one, remainder = rat(8n), j = 0;
  while (cmp(remainder, tolerance) > 0n) {
    j++;
    term = div(mul(term, mul(rat(-1n), mul(angle, angle))), rat(BigInt((2*j-1)*(2*j))));
    total = add(total, term);
    remainder = mul(remainder, rat(16n, BigInt((2*j+1)*(2*j+2))));
  }
  const error = add(remainder, angleError), result = [max(rat(-1n), sub(total, error)), min(E.one, add(total, error))];
  check(cmp(sub(result[1], result[0]), rat(1n, 2n**BigInt(bits))) <= 0n, "full rational cosine enclosure width");
  cosineCache.set(key, result); return result;
}
function born(p, kind, bits) {
  if (kind === "anti_trine") return [0, 1, 2].map(b => {
    const [lo, hi] = cosine(p.q, p.phases[1]-p.phases[0]-(p.q/3n)*BigInt(b), bits);
    return [div(sub(E.one, hi), rat(3n)), div(sub(E.one, lo), rat(3n))];
  });
  check(kind === "inverse_F3" && p.phases.length === 3, "specified small-packet local readout only");
  return [0, 1, 2].map(b => {
    let lo = E.zero, hi = E.zero;
    for (let t = 0; t < 3; t++) for (let u = 0; u < t; u++) {
      const c = cosine(p.q, p.phases[t]-p.phases[u]-(p.q/3n)*BigInt(b*(t-u)), bits);
      lo = add(lo, c[0]); hi = add(hi, c[1]);
    }
    return [max(E.zero, div(add(rat(3n), mul(rat(2n), lo)), rat(9n))),
            min(E.one, div(add(rat(3n), mul(rat(2n), hi)), rat(9n)))];
  });
}
function budget(b, calls, failureBits) {
  const precision = failureBits+(8n*calls-1n).toString(2).length;
  check(integer(b.max_stochastic_calls) === calls && b.target_failure_bits === failureBits && b.per_call_precision_bits === precision, "all adaptive stochastic calls and finite precision charged");
  check(b.adaptive_unconditional_transcript_error_upper === str(min(E.one, rat(8n*calls, 2n**BigInt(precision)))) && b.conditioning_away_abort_allowed === false && b.private_phase_access === ACCESS && b.arbitrary_wide_quantum_circuit_covered === false && b.unknown_quantum_only_source_covered === false, "unconditional coupling budget and source/circuit scope");
  return precision;
}
function sample(s, boxProvider, outcomes, precision) {
  check(s.max_bits === precision && s.unconditional_sampling_error_or_abort_upper === str(min(E.one, rat(8n, 2n**BigInt(precision)))) && s.conditional_on_no_abort_is_the_exact_channel === false, "explicit unconditional precision/abort budget");
  let prefix = 0n, previousBits = 0, result = null;
  check(s.decisions.length >= 1, "complete coin decision trace");
  s.decisions.forEach((d, index) => {
    const bits = Math.min(previousBits+8, precision), width = bits-previousBits, next = integer(d.coin_prefix);
    check(d.bits === bits && next >= 0n && next < 2n**BigInt(bits) && (next >> BigInt(width)) === prefix && result === null, "consistent finite private random-bit prefix");
    prefix = next; previousBits = bits;
    const boxes = boxProvider(bits), encoded = boxes.map(a => a.map(str));
    same(d.probability_boxes, encoded, "independent Machin/Taylor or exact constant Born boxes");
    check(boxes.length === outcomes && boxes.every(([lo, hi]) => cmp(lo, E.zero) >= 0n && cmp(hi, E.one) <= 0n && cmp(lo, hi) <= 0n && cmp(sub(hi, lo), rat(1n, 2n**BigInt(bits))) <= 0n), "certified physical probability box widths");
    const cumulative = [[E.zero, E.zero]];
    for (let j = 1; j < outcomes; j++) cumulative.push([boxes.slice(0, j).reduce((x, y) => add(x, y[0]), E.zero), boxes.slice(0, j).reduce((x, y) => add(x, y[1]), E.zero)]);
    cumulative.push([E.one, E.one]);
    const coinL = rat(prefix, 2n**BigInt(bits)), coinH = rat(prefix+1n, 2n**BigInt(bits));
    result = null;
    for (let j = 0; j < outcomes; j++) if (cmp(coinL, cumulative[j][1]) >= 0n && cmp(coinH, cumulative[j+1][0]) <= 0n) {result = j; break;}
    check(d.outcome === result && d.decision === (result === null ? "REFINE" : "CERTIFIED"), "actual interval decision, no guessed or free outcome");
    check(index === s.decisions.length-1 || result === null, "no further bits after a certified event");
  });
  check(s.random_bits_read === previousBits && s.outcome === result && s.status === (result === null ? "EXPLICIT_COIN_PRECISION_ABORT" : "CERTIFIED_OUTCOME"), "correct finite sampling terminal status");
  if (result === null) check(previousBits === precision, "abort occurs only at precision cap");
  return result;
}
function completeLaw(c) {
  const packets = source(c.source), K = field(9), M = matrices(K), oneThird = rat(1n, 3n);
  const rho = p => p.phases.map(a => p.phases.map(b => K.scale(K.powers[Number(mod(a-b, p.q))], rat(1n, BigInt(p.phases.length)))));
  const left = rho(packets[0]), right = rho(packets[1]), original = M.zeroM(9, 9);
  for (let t = 0; t < 3; t++) for (let v = 0; v < 3; v++) for (let u = 0; u < 3; u++) for (let w = 0; w < 3; w++) original[3*t+v][3*u+w] = K.times(left[t][u], right[v][w]);
  const SUM = M.zeroM(9, 9);
  for (let t = 0; t < 3; t++) for (let v = 0; v < 3; v++) SUM[3*t+((v-t+3) % 3)][3*t+v] = K.unit;
  const measured = M.times(M.times(SUM, original), M.star(SUM));
  check(c.complete_paths === 72 && c.paths.length === 72 && c.public_controller_reads_private_phase_values === false && c.counterfactual_paths_are_simultaneous_physical_outputs === false, "complete alternative adaptive channel paths only");
  let total = K.F(), lowerTotal = E.zero, upperTotal = E.zero, index = 0;
  for (let v = 0; v < 3; v++) {
    const pivot = cmerge(packets[0], packets[1], v), corrected = diagonal(pivot, [0n, BigInt(v)*3n, BigInt(v*v)*3n]);
    const actual = M.zeroM(3, 3);
    for (let t = 0; t < 3; t++) for (let u = 0; u < 3; u++) actual[t][u] = K.scale(measured[3*t+v][3*u+v], rat(3n));
    check(M.eq(actual, rho(pivot)), "literal measured SUM channel matches exact compact phases");
    const pFirst = [0, 1, 2].map(f => {
      let amplitudeSquared = K.F();
      for (let t = 0; t < 3; t++) for (let u = 0; u < 3; u++) amplitudeSquared = K.plus(amplitudeSquared, K.scale(K.powers[Number(mod(corrected.phases[t]-corrected.phases[u]-3n*BigInt(f*(t-u)), 9n))], rat(1n, 9n)));
      return amplitudeSquared;
    });
    for (let f = 0; f < 3; f++) {
      const exacts = [K.scale(pFirst[f], rat(1n, 9n)), K.scale(pFirst[f], rat(2n, 27n))];
      for (let bit = 0; bit < 2; bit++) {
        const child = diagonal(bmerge(bproject(packets[2]), bproject(packets[3]), bit), [0n, 3n*BigInt(f)]);
        const before = [bproject(packets[2]), bproject(packets[3])], densities = before.map(rho), retained = M.zeroM(2, 2);
        for (let t = 0; t < 2; t++) for (let u = 0; u < 2; u++) retained[t][u] = K.scale(K.times(densities[0][t][u], densities[1][t ^ bit][u ^ bit]), rat(2n));
        check(M.eq(retained, rho(bmerge(...before, bit))), "literal measured binary CNOT channel");
        for (let outcome = 0; outcome < 3; outcome++) {
          const k = Number(mod(child.phases[1]-child.phases[0]-3n*BigInt(outcome), 9n));
          const cosine = K.scale(K.plus(K.powers[k], K.powers[(9-k) % 9]), rat(1n, 2n));
          const pAnti = K.scale(K.plus(K.unit, K.scale(cosine, rat(-1n))), oneThird);
          exacts.push(K.scale(K.times(pFirst[f], pAnti), rat(2n, 27n)));
        }
      }
      const fBoxes = born(corrected, "inverse_F3", 24)[f];
      for (let j = 0; j < 8; j++) {
        const row = c.paths[index++];
        check(row.complement === v && row.first_F3_outcome === f, "actual public adaptive history order");
        same(row.feedback_gate_numerators, [0, 3*v, 3*v*v], "controller settings depend only on measured complement");
        let boxes;
        if (j < 2) {
          check(row.terminal === ["LEFT_PROJECTION_REJECT", "RIGHT_PROJECTION_REJECT"][j], "all projection rejects retained in full channel");
          boxes = fBoxes.map(x => mul(x, j === 0 ? rat(1n, 9n) : rat(2n, 27n)));
        } else {
          const bit = Math.floor((j-2)/3), outcome = (j-2) % 3;
          check(row.terminal === "ANTI_TRINE" && row.binary_complement === bit && row.anti_trine_outcome === outcome, "actual measured sign and anti-trine branch");
          const child = diagonal(bmerge(bproject(packets[2]), bproject(packets[3]), bit), [0n, 3n*BigInt(f)]), anti = born(child, "anti_trine", 24)[outcome];
          same(row.retained_packet_before_readout, savedPacket(child), "retained exact known phases and original ancestry");
          boxes = [mul(rat(2n, 27n), mul(fBoxes[0], anti[0])), mul(rat(2n, 27n), mul(fBoxes[1], anti[1]))];
        }
        same(row.joint_probability_box, boxes.map(str), "independent complete adaptive probability enclosure");
        check(E.sign(K, K.plus(exacts[j], K.scale(K.unit, mul(rat(-1n), boxes[0])))) >= 0 && E.sign(K, K.plus(K.scale(K.unit, boxes[1]), K.scale(exacts[j], rat(-1n)))) >= 0, "exact quantum path inside declared rational box");
        total = K.plus(total, exacts[j]); lowerTotal = add(lowerTotal, boxes[0]); upperTotal = add(upperTotal, boxes[1]);
      }
    }
  }
  check(K.eq(total, K.unit) && c.lower_total === str(lowerTotal) && c.upper_total === str(upperTotal) && cmp(lowerTotal, E.one) <= 0n && cmp(upperTotal, E.one) >= 0n, "all72 physical paths normalize, no postselection");
}
function run(r) {
  check(r.status === "SCOPED_SAME_ORIGINAL_DATA_MEASURED_PACKET_SIMULATION_REVIEW_PENDING", "scoped local simulation result");
  check(r.producer_sha256 === hash(path.join(ROOT, "theorems/known_preparation_packet_simulation.py")) && r.derivation_sha256 === hash(path.join(ROOT, "research/KNOWN_PREPARATION_PACKET_SIMULATION.md")), "pinned source and derivation");
  const dependencies = ["native_noisy_phase_input.py", "ternary_certified_noise_sampler.py"];
  same(Object.keys(r.dependency_sha256).sort(), dependencies.slice().sort(), "required preparation and interval dependencies");
  dependencies.forEach(f => check(r.dependency_sha256[f] === hash(path.join(ROOT, "theorems", f)), "pinned dependency "+f));
  check(r.original_classical_preparation_access_required === true && r.specified_measured_compression_family_has_a_classical_simulator === true, "specific known preparation access and primitive family");
  ["unknown_HSP_phase_source_dequantized", "arbitrary_known_preparation_quantum_circuits_dequantized", "persistent_coherent_phase_vectors_covered", "physical_hardware_error_certified", "general_LWE_quantum_algorithms_ruled_out", "accepted_speedup_candidate"].forEach(k => check(r[k] === false, "unjustified broadening "+k));
  completeLaw(r.complete_adaptive_law_control);
  check(r.certified_sample_controls.length === 4, "all scalable-source transcript controls");
  r.certified_sample_controls.forEach((c, index) => {
    const packets = source(c.source), q = packets[0].q;
    check(q === 3n**BigInt([1, 2, 16, 64][index]) && packets.length === 6 && c.status === "CERTIFIED_ADAPTIVE_TRANSCRIPT" && c.classical_hidden_secret_used === false && c.unknown_quantum_input_simulated === false, "scalable known raw-phase source controls");
    const precision = budget(c.budget, 16n, 24);
    check(c.transcript.length <= 16, "all stochastic calls counted");
    let j = 0;
    const v = [0, 1].map(() => {
      const t = c.transcript[j++];
      check(t.instrument === "common_index_complement_coordinate", "actual measured complement coordinate");
      return sample(t.sampling, () => Array.from({length: 3}, () => [rat(1n, 3n), rat(1n, 3n)]), 3, precision);
    });
    const pivot = packet(q, [0, 1, 2].map(t => mod(packets[0].phases[t]+packets[1].phases[(t+v[0]) % 3]+packets[2].phases[(t+v[1]) % 3], q)), packets.slice(0, 3).flatMap(p => p.ids));
    const first = c.transcript[j++];
    check(first.instrument === "common_index_then_inverse_F3", "compact measured merge then destructive F3");
    same(first.packet_before_readout, savedPacket(pivot), "actual scalar phase update, no secret-character replacement");
    same(first.merge.complement, v, "actual sampled offsets");
    same(first.merge.original_sources, pivot.ids, "complete paid merged ancestry");
    same(first.merge.exact_branch_probability_compact, {base: 3, exponent: -2}, "uniform exact measured block probability");
    check(first.merge.retained_packets === 1 && first.merge.unknown_state_inverse_used === false && first.merge.dense_3_to_the_block_size_table_built === false, "factorized primitive, not arbitrary wide circuit simulation");
    const f = sample(first.sampling, bits => born(pivot, "inverse_F3", bits), 3, precision), accepted = [];
    for (let p = 3; p < 6; p++) {
      const t = c.transcript[j++];
      check(t.instrument === "project_basis01", "every original projection charged");
      same(t.packet_before_projection, savedPacket(packets[p]), "actual original prepared packet");
      const event = sample(t.sampling, () => [[rat(2n, 3n), rat(2n, 3n)], [rat(1n, 3n), rat(1n, 3n)]], 2, precision);
      if (event === 0) accepted.push(bproject(packets[p]));
    }
    if (accepted.length >= 2) {
      const sign = c.transcript[j++];
      check(sign.instrument === "CNOT_complement_bit", "actual measured binary sign, not a desired branch");
      const bit = sample(sign.sampling, () => [[rat(1n, 2n), rat(1n, 2n)], [rat(1n, 2n), rat(1n, 2n)]], 2, precision), t = c.transcript[j++];
      check(t.instrument === "measured_CNOT_then_feedback_anti_trine" && t.binary_complement === bit && t.complement_probability_exact === "1/2", "costed one-child sign merge");
      const child = diagonal(bmerge(accepted[0], accepted[1], bit), [0n, (q/3n)*BigInt(f)]);
      same(t.packet_before_readout, savedPacket(child), "feedback uses only prior public outcome, not private unknown secret");
      sample(t.sampling, bits => born(child, "anti_trine", bits), 3, precision);
    }
    check(j === c.transcript.length, "no omitted or unaccounted transcript operation");
  });
  check(r.scaling_contracts.length === 4, "all asymptotic precision contracts");
  r.scaling_contracts.forEach((b, i) => budget(b, [16n, 2n**20n, 2n**64n, 2n**128n][i], 32));
  return {status: "PASS", complete_adaptive_paths: 72, certified_sample_controls: 4,
          unknown_quantum_only_source_dequantized: false, general_quantum_LWE_impossibility_established: false};
}
if (require.main === module) console.log(JSON.stringify(run(JSON.parse(fs.readFileSync(process.argv[2] || REPORT, "utf8"))), null, 2));
module.exports = {run};
