#!/usr/bin/env node
/**
 * Independent BigInt cross-checker for `planted_qary_offset_pair_mass_frontier_audit`.
 *
 * Recomputes from first principles:
 * 1. Exact cube survival factor P_cube(W, u) = ((W - 1) / W)^s and two-sided rational
 *    enclosure 1 - s/W <= P_cube(W, u) <= W / (W + s).
 * 2. Worst-case multiplicative box survival bound:
 *      P_box^min(M_box, m, s_F) = ((M_box - 1)/M_box)^(s_F - 1) * ((M_box - B_tern)/M_box)^m,
 *    and additive bound 1 - L_box / M_box, where L_box = (s_F - 1) + m * B_tern(s_F).
 * 3. Dyadic schedule bounding intended partner failure, not source validity.
 * 4. Public same-colour collision falsifying the unconditional DCP transfer.
 */

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..", "..");
const ARTIFACT_PATH = path.join(
  ROOT,
  "research",
  "reductions",
  "planted_qary_offset_pair_mass_frontier_audit.json"
);

function gcd(a, b) {
  a = a < 0n ? -a : a;
  b = b < 0n ? -b : b;
  while (b !== 0n) {
    const t = a % b;
    a = b;
    b = t;
  }
  return a;
}

function parseFrac(str) {
  const parts = String(str).split("/");
  if (parts.length === 1) {
    return { num: BigInt(parts[0]), den: 1n };
  }
  return { num: BigInt(parts[0]), den: BigInt(parts[1]) };
}

function formatFrac(num, den) {
  if (den < 0n) {
    num = -num;
    den = -den;
  }
  const g = gcd(num, den);
  return `${(num / g).toString()}/${(den / g).toString()}`;
}

function powBigInt(base, exp) {
  let res = 1n;
  let b = BigInt(base);
  let e = BigInt(exp);
  while (e > 0n) {
    if (e & 1n) res *= b;
    b *= b;
    e >>= 1n;
  }
  return res;
}

function sharpTernaryBound(sF) {
  if (sF <= 1) return 0;
  if (sF === 2) return 1;
  return Math.floor((sF - 1) / 2);
}

function leqFrac(a, b) {
  return a.num * b.den <= b.num * a.den;
}

function main() {
  const report = JSON.parse(fs.readFileSync(process.argv[2] || ARTIFACT_PATH, "utf-8"));
  if (report.subsystem !== "planted_qary_offset_pair_mass_frontier_audit") {
    throw new Error(`Unexpected subsystem: ${report.subsystem}`);
  }

  let checked = 0;
  for (const row of report.planted_instance_frontier_audit) {
    const n = row.n;
    const m = row.m;
    const s = row.support_s;
    const sF = row.free_support_s_F;
    const sched = row.schedule;
    const bTern = sharpTernaryBound(sF);
    const lBox = (sF - 1) + m * bTern;

    if (sched.B_tern_s_F !== bTern || sched.L_box_ceiling !== lBox) {
      throw new Error(`B_tern or L_box mismatch for n=${n}, m=${m}`);
    }

    const b = sched.b_box_exponent;
    const mBox = BigInt(sched.M_box);
    const w = sched.w_width_exponent;
    const width = BigInt(sched.width_W);
    const ell = BigInt(n * (b + 1));

    if (mBox !== 1n << BigInt(b) || width !== 1n << BigInt(w) || BigInt(sched.ell_position_wires) !== ell) {
      throw new Error("Dyadic schedule power mismatch");
    }

    // Theorem 1: P_cube = ((W - 1)/W)^s
    const pCubeNum = powBigInt(width - 1n, s);
    const pCubeDen = powBigInt(width, s);
    const pCubeStr = formatFrac(pCubeNum, pCubeDen);
    if (pCubeStr !== row.P_cube_actual_fraction || pCubeStr !== sched.P_cube_exact_fraction) {
      throw new Error(`P_cube mismatch: expected ${pCubeStr}, got ${row.P_cube_actual_fraction}`);
    }

    // Theorem 2: P_box^min = ((M_box - 1)/M_box)^(s_F - 1) * ((M_box - bTern)/M_box)^m
    const pBoxMinNum = powBigInt(mBox - 1n, sF - 1) * powBigInt(mBox - BigInt(bTern), m);
    const pBoxMinDen = powBigInt(mBox, (sF - 1) + m);
    const pBoxMinStr = formatFrac(pBoxMinNum, pBoxMinDen);
    if (pBoxMinStr !== sched.P_box_min_multiplicative_fraction) {
      throw new Error(`P_box_min mismatch: expected ${pBoxMinStr}, got ${sched.P_box_min_multiplicative_fraction}`);
    }

    const pBoxActual = parseFrac(row.P_box_actual_fraction);
    const pBoxMin = { num: pBoxMinNum, den: pBoxMinDen };
    if (!leqFrac(pBoxMin, pBoxActual)) {
      throw new Error("P_box_actual < P_box_min violation");
    }

    // Partner failure is NOT a source bad-register certificate.
    const pBadActual = parseFrac(row.intended_partner_failure_fraction);
    const pBadMult = parseFrac(sched.partner_failure_multiplicative_upper_fraction);
    const pBadAdd = parseFrac(sched.partner_failure_additive_upper_fraction);
    const f1Budget = { num: 1n, den: ell };

    if (!leqFrac(pBadActual, pBadMult) || !leqFrac(pBadMult, pBadAdd) || !leqFrac(pBadAdd, f1Budget)) {
      throw new Error(`Partner-failure chain inequality failed for n=${n}, m=${m}`);
    }
    const expectedMult = formatFrac(pBoxMinDen * pCubeDen - pBoxMinNum * pCubeNum, pBoxMinDen * pCubeDen);
    const expectedAdd = formatFrac(BigInt(lBox) * width + BigInt(s) * mBox, mBox * width);
    if (expectedMult !== sched.partner_failure_multiplicative_upper_fraction || expectedAdd !== sched.partner_failure_additive_upper_fraction) {
      throw new Error("Stored failure bounds were not derived from product factors");
    }
    const survival = parseFrac(row.intended_partner_survival_fraction);
    if (survival.num * pBoxActual.den * pCubeDen !== survival.den * pBoxActual.num * pCubeNum ||
        pBadActual.num * survival.den !== pBadActual.den * (survival.den - survival.num)) {
      throw new Error("Intended partner survival/failure mismatch");
    }
    const geometry = row.geometry_obligation;
    const diameter2 = BigInt(n) * (width - 1n) ** 2n;
    const norm2 = 4n * BigInt(s);
    if (BigInt(geometry.same_cell_squared_distance_upper) !== diameter2 ||
        BigInt(geometry.assumed_nonparallel_squared_norm_lower) !== norm2 ||
        geometry.nonparallel_exclusion_inequality_satisfied !== (norm2 > diameter2) ||
        geometry.conditional_geometry_inequalities_satisfied !== (norm2 > diameter2) ||
        geometry.nonparallel_norm_lower_bound_verified !== false || geometry.source_geometry_certified !== false ||
        row.source_bad_register_rate_certified !== false || row.source_bad_register_rate !== null ||
        sched.source_bad_register_rate_certified !== false || sched.requires_independent_two_point_geometry !== true ||
        row.schedule_and_hitting_trial_selected_with_private_witness !== true || row.all_public_coordinate_trials_executed !== false) {
      throw new Error("Geometry/public-access obligation was promoted or corrupted");
    }

    checked += 1;
  }

  const c = report.source_geometry_counterexample;
  const src = c.public_source;
  if (c.same_colour !== 0 || src.coordinate !== 1 || src.residue_guess !== 1 || src.prime - 1 < src.cube_width) {
    throw new Error("Invalid collision control parameters");
  }
  const cells = c.distinct_positions.map(a => {
    if (a.length !== src.basis_rows.length || a.some(x => !Number.isSafeInteger(x) || x < 0 || x >= src.box)) {
      throw new Error("Counterexample input outside public domain");
    }
    const coeff = a.map((x, j) => BigInt(x) * (j === src.coordinate ? BigInt(src.prime) : 1n));
    const point = a.map((_, j) => coeff.reduce((acc, x, i) => acc + x * BigInt(src.basis_rows[i][j]), 0n));
    return point.map((x, j) => {
      const z = x - BigInt(src.offsets[j]);
      const w = BigInt(src.cube_width);
      return Number(z >= 0n ? z / w : -((-z + w - 1n) / w));
    });
  });
  if (JSON.stringify(c.distinct_positions[0]) === JSON.stringify(c.distinct_positions[1]) ||
      JSON.stringify(cells[0]) !== JSON.stringify(cells[1]) || JSON.stringify(cells) !== JSON.stringify(c.cells) ||
      c.two_point_source_promise_falsified !== true || c.same_colour_collision_verified !== true ||
      report.guardrails.source_geometry_certified !== false || report.guardrails.unconditional_dcp_bad_register_budget_certified !== false) {
    throw new Error("Counterexample or source-validity guardrail failed");
  }

  console.log(
    JSON.stringify(
      {
        status: "ok",
        subsystem: report.subsystem,
        instances_verified: checked,
      },
      null,
      2
    )
  );
}

main();
