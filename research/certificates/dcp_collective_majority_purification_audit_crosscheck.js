"use strict";
// Independent exact replay for DCP shifted-box producer, equal-label heralding, and collective majority Helstrom optimality.
const fs = require("fs"), path = require("path"), crypto = require("crypto");
const E = require("./cyclotomic_exact.js");
const L = require("./dcp_physical_bad_register_lineage_crosscheck.js");
const {check, rat, parse, str, add, sub, mul, div, cmp, zero, one} = E;
const ROOT = path.resolve(__dirname, "../..");
const REPORT = path.join(ROOT, "research/phase_workbench/dcp_collective_majority_purification_audit.json");
const enc = x => x <= 9007199254740991n && x >= -9007199254740991n ? Number(x) : String(x);
const canonical = x => Array.isArray(x) ? x.map(canonical) : x && typeof x === "object" ? Object.fromEntries(Object.keys(x).sort().map(k => [k, canonical(x[k])])) : x;
const same = (a, b, msg) => E.same(canonical(a), canonical(b), msg);
const hash = f => crypto.createHash("sha256").update(fs.readFileSync(f)).digest("hex");
const min = (a, b) => cmp(a, b) <= 0n ? a : b;
const absRat = a => a[0] < 0n ? [-a[0], a[1]] : a;

function combBig(n, k) {
  if (k < 0 || k > n) return 0n;
  let num = 1n, den = 1n;
  for (let i = 1; i <= k; i++) {
    num *= BigInt(n - i + 1);
    den *= BigInt(i);
  }
  return num / den;
}

function powRat(a, e) {
  let out = one;
  for (let i = 0; i < e; i++) out = mul(out, a);
  return out;
}

function checkShiftedBox(B) {
  const n = B.dimension_n, M = BigInt(B.box_side_M), shift = B.shift_vector.map(BigInt);
  const N = B.dcp_modulus_N, k = B.measured_Fourier_label;
  check(n === shift.length && M >= 2n && shift.every(v => (v < 0n ? -v : v) < M), "valid shifted box parameters");
  const totalPts = M ** BigInt(n);
  const totalStates = 2n * totalPts;
  const goodPairs = shift.reduce((acc, v) => acc * (M - (v < 0n ? -v : v)), 1n);
  const bad0 = totalPts - goodPairs, bad1 = totalPts - goodPairs;
  const pGood = rat(2n * goodPairs, totalStates);
  const pBad = sub(one, pGood);
  let unionBad = zero;
  shift.forEach(v => { unionBad = add(unionBad, rat(v < 0n ? -v : v, M)); });
  unionBad = min(one, unionBad);
  check(cmp(pBad, unionBad) <= 0n, "p_bad <= additive union bound");
  const audit = B.produced_phase_density_audit;
  check(
    BigInt(B.total_box_cells_M_pow_n) === totalPts &&
    BigInt(B.total_superposition_basis_states_2_M_pow_n) === totalStates &&
    BigInt(B.good_interior_pair_cells_G) === goodPairs &&
    BigInt(B.bad_zero_boundary_cells_B0) === bad0 &&
    BigInt(B.bad_one_boundary_cells_B1) === bad1 &&
    B.translation_symmetry_B0_equals_B1 === true &&
    B.exact_good_register_probability === str(pGood) &&
    B.exact_bad_register_probability === str(pBad) &&
    B.additive_union_bad_probability_upper === str(unionBad) &&
    B.exact_bad_zero_conditional_probability === "1/2" &&
    audit.modulus === N &&
    audit.measured_Fourier_label === k &&
    audit.PRIVATE_density_zero_population === "1/2" &&
    audit.PRIVATE_density_phase_visibility === str(pGood),
    "shifted box intersection and PhaseDensity"
  );
}

function checkEqualLabelHeralding(H) {
  const N = H.dcp_modulus_N, k = H.colliding_input_label_k;
  const p1 = parse(H.left_bad_probability), p2 = parse(H.right_bad_probability);
  const v1 = sub(one, p1), v2 = sub(one, p2), vProd = mul(v1, v2);
  const plusAcc = div(add(one, vProd), rat(2n)), minusAcc = div(sub(one, vProd), rat(2n));
  check(
    H.left_visibility_v1 === str(v1) &&
    H.right_visibility_v2 === str(v2) &&
    H.product_visibility_v1_v2 === str(vProd) &&
    H.sum_branch_z0.exact_branch_probability === "1/2" &&
    H.sum_branch_z0.output_audit.measured_Fourier_label === (2 * k) % N &&
    H.sum_branch_z0.output_audit.PRIVATE_density_phase_visibility === str(vProd) &&
    H.difference_branch_z1.exact_branch_probability === "1/2" &&
    H.difference_branch_z1.output_audit.measured_Fourier_label === 0 &&
    H.difference_branch_z1.output_audit.PRIVATE_density_phase_visibility === str(vProd) &&
    H.difference_branch_has_zero_label === true &&
    H.difference_branch_X_plus_acceptance === str(plusAcc) &&
    H.difference_branch_X_minus_acceptance === str(minusAcc) &&
    H.difference_branch_estimates_v1_v2_without_secret_s === true &&
    H.difference_branch_carries_hidden_secret_information === false &&
    H.postselecting_difference_branch_leaves_surviving_label_k_copy === false,
    "equal-label collision heralding dichotomy"
  );
}

function checkMajorityHelstrom(M) {
  const R = M.odd_target_copies_R, v = parse(M.single_copy_visibility_v);
  check(R % 2 === 1 && R >= 1 && cmp(v, zero) >= 0n && cmp(v, one) <= 0n, "odd R and valid v");
  const m = (R - 1) / 2;
  const qPlus = div(add(one, v), rat(2n)), qMinus = div(sub(one, v), rat(2n));
  let pMaj = zero;
  for (let j = m + 1; j <= R; j++) {
    const term = mul(rat(combBig(R, j)), mul(powRat(qPlus, j), powRat(qMinus, R - j)));
    pMaj = add(pMaj, term);
  }
  let halfTrace = zero;
  for (let j = 0; j <= R; j++) {
    const diff = sub(mul(powRat(qPlus, j), powRat(qMinus, R - j)), mul(powRat(qMinus, j), powRat(qPlus, R - j)));
    halfTrace = add(halfTrace, mul(rat(combBig(R, j)), absRat(diff)));
  }
  halfTrace = div(halfTrace, rat(2n));
  const pHel = add(rat(1n, 2n), div(halfTrace, rat(2n)));
  const vMaj = sub(mul(rat(2n), pMaj), one);
  const vMajSq = mul(vMaj, vMaj);
  const fvdgSq = sub(one, powRat(sub(one, mul(v, v)), R));
  const linSq = mul(rat(BigInt(R)), mul(v, v));

  same(M, {
    odd_target_copies_R: R,
    single_copy_visibility_v: str(v),
    single_copy_X_plus_probability: str(qPlus),
    exact_majority_vote_success_probability: str(pMaj),
    exact_collective_Helstrom_success_probability: str(pHel),
    purified_majority_visibility_v_maj: str(vMaj),
    half_trace_distance_norm: str(halfTrace),
    product_X_majority_equals_collective_Helstrom_optimum: true,
    v_maj_squared: str(vMajSq),
    fuchs_van_de_graaf_1_minus_fidelity_sq_upper: str(fvdgSq),
    linear_R_v_squared_upper: str(linSq),
    fidelity_chain_inequality_verified: true,
    entangling_collective_POVM_can_beat_X_majority_at_parity_label: false,
  }, "exact majority vote and collective Helstrom equivalence");
  check(cmp(pMaj, pHel) === 0n && cmp(vMaj, halfTrace) === 0n && cmp(vMajSq, fvdgSq) <= 0n && cmp(fvdgSq, linSq) <= 0n, "Helstrom and FvdG inequalities");
}

function checkPurifiedProfile(P) {
  L.lineage(P.base_lineage_ledger);
  const vUpper = parse(P.single_target_visibility_upper);
  const vTarg = parse(P.target_purified_visibility);
  check(P.single_target_visibility_upper === P.base_lineage_ledger.output_phase_visibility_upper, "single target visibility matches lineage");
  const leavesPerCopy = BigInt(P.base_lineage_ledger.disjoint_original_state_leaves);
  const ratio = div(mul(vTarg, vTarg), mul(vUpper, vUpper));
  let minCopies = (ratio[0] + ratio[1] - 1n) / ratio[1];
  if (minCopies % 2n === 0n) minCopies += 1n;
  const totalLeaves = minCopies * leavesPerCopy;
  check(
    BigInt(P.disjoint_leaves_per_target_copy) === leavesPerCopy &&
    BigInt(P.minimum_odd_target_copies_by_fvdg_bound) === minCopies &&
    BigInt(P.minimum_total_disjoint_original_leaves) === totalLeaves &&
    P.collective_entangling_parity_readout_reduces_copy_requirement === false,
    "end-to-end purified lineage copy and leaf bounds"
  );
}

function verify(R) {
  check(
    R.status === "DCP_SHIFTED_BOX_PRODUCER_AND_COLLECTIVE_MAJORITY_AUDIT_REVIEW_PENDING" &&
    R.producer_sha256 === hash(path.join(ROOT, "theorems/dcp_collective_majority_purification_audit.py")) &&
    R.derivation_sha256 === hash(path.join(ROOT, "research/DCP_COLLECTIVE_MAJORITY_PURIFICATION_AUDIT.md")) &&
    R.contract_sha256 === hash(path.join(ROOT, "research/hypotheses/dcp_collective_majority_purification_audit_contract.json")),
    "producer, derivation, and contract hashes"
  );
  const deps = [
    "dcp_physical_bad_register_lineage.py",
    "native_basis_lottery.py",
    "native_small_multiple_completion.py",
    "ternary_measured_lattice_decoder.py",
  ];
  same(Object.keys(R.dependency_sha256).sort(), deps.sort(), "direct scientific dependencies");
  deps.forEach(f => check(R.dependency_sha256[f] === hash(path.join(ROOT, "theorems", f)), "dependency " + f));

  check(R.shifted_box_source_controls.length === 3, "3 shifted-box controls");
  R.shifted_box_source_controls.forEach(checkShiftedBox);
  check(
    R.shifted_box_source_controls[0].explicit_cell_intersection_verified === true &&
    R.shifted_box_source_controls[1].explicit_cell_intersection_verified === true,
    "explicit shifted-box set intersection verified on finite controls"
  );

  check(R.equal_label_heralding_controls.length === 3, "3 equal-label heralding controls");
  R.equal_label_heralding_controls.forEach(checkEqualLabelHeralding);

  check(R.collective_majority_helstrom_controls.length === 5, "5 collective majority Helstrom controls");
  R.collective_majority_helstrom_controls.forEach(checkMajorityHelstrom);

  check(R.end_to_end_purified_lineage_profiles.length === 4, "4 purified lineage profiles");
  R.end_to_end_purified_lineage_profiles.forEach(checkPurifiedProfile);

  check(
    R.finite_shifted_box_lattice_producer_implemented === true &&
    R.general_dcp_or_dhsp_no_go_claimed === false &&
    R.full_bad_register_dcp_solver_supplied === false &&
    R.accepted_speedup_candidate === false &&
    R.new_active_negative_result_created === false &&
    R.novelty_claim === false,
    "honesty guardrails"
  );

  return {
    verified: true,
    shifted_box_controls: R.shifted_box_source_controls.length,
    heralding_controls: R.equal_label_heralding_controls.length,
    majority_helstrom_controls: R.collective_majority_helstrom_controls.length,
    purified_lineage_profiles: R.end_to_end_purified_lineage_profiles.length,
    full_dcp_solver_supplied: false,
  };
}

module.exports = {
  verify,
  checkShiftedBox,
  checkEqualLabelHeralding,
  checkMajorityHelstrom,
  checkPurifiedProfile,
};

if (require.main === module) {
  console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(process.argv[2] || REPORT, "utf8"))), null, 2));
}
