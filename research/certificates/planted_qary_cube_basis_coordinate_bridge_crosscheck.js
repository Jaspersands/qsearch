#!/usr/bin/env node
/**
 * Independent BigInt cross-checker for `planted_qary_cube_basis_coordinate_bridge`.
 *
 * Recomputes from first principles:
 * 1. Centered RREF pivot/free basis coordinate decomposition:
 *      d_free[j] = u[F_j],
 *      d_piv[i]  = (u[P_i] + sum_j C[i][j] * u[F_j]) / q
 *    using exact BigInt arithmetic.
 * 2. Fixed-q sharp ternary bound floor((1+s_F*(q-1)/2)/q),
 *    with q-independent envelope 0, 1, floor((s_F-1)/2),
 *    and coarse bound floor(U * s_F / 2).
 * 3. Partner box difference delta on the hitting free coordinate j_hit:
 *      delta[j_hit] = (1 - 1)/3 = 0, ||delta||_1 = ||d||_1 - 1,
 *    and exact rational box bad fraction:
 *      p_bad_box = 1 - prod_i (M_box - |delta_i|) / M_box^n <= ||delta||_1 / M_box.
 * 4. Ternary outer-guessing collapse: at least one free coordinate j in {m, ..., n-1}
 *    has d_j !== 0 (mod 3).
 */

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..", "..");
const ARTIFACT_PATH = path.join(
  ROOT,
  "research",
  "reductions",
  "planted_qary_cube_basis_coordinate_bridge.json"
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

function reduceFrac(num, den) {
  if (den < 0n) {
    num = -num;
    den = -den;
  }
  const g = gcd(num, den);
  return `${(num / g).toString()}/${(den / g).toString()}`;
}

function sharpTernaryPivotBound(sF) {
  if (sF <= 1) return 0;
  if (sF === 2) return 1;
  return Math.floor((sF - 1) / 2);
}

function fixedQBound(sF, modulus) {
  const q = BigInt(modulus);
  return Number((1n + BigInt(sF) * ((q - 1n) / 2n)) / q);
}

function verifyAnalysisBlock(analysis) {
  const m = analysis.m;
  const n = analysis.n;
  const q = BigInt(analysis.q);
  const halfQ = (q - 1n) / 2n;
  const pivCols = analysis.pivot_cols;
  const freeCols = analysis.free_cols;
  const C = analysis.C_centered;
  const u = analysis.u_vec.map((x) => BigInt(x));

  const dPiv = [];
  for (let i = 0; i < m; i++) {
    let numer = u[pivCols[i]];
    for (let j = 0; j < n - m; j++) {
      const cVal = BigInt(C[i][j]);
      if (cVal < -halfQ || cVal > halfQ) {
        throw new Error(`C[${i}][${j}] = ${cVal} out of centered range [-${halfQ}, ${halfQ}]`);
      }
      numer += cVal * u[freeCols[j]];
    }
    if (numer % q !== 0n) {
      throw new Error(`Row ${i} numerator ${numer} not divisible by q=${q}`);
    }
    dPiv.push(Number(numer / q));
  }
  const dFree = freeCols.map((f) => Number(u[f]));
  const dFull = dPiv.concat(dFree);

  if (JSON.stringify(dFull) !== JSON.stringify(analysis.d_full)) {
    throw new Error(
      `Mismatch in d_full: expected ${JSON.stringify(analysis.d_full)}, got ${JSON.stringify(dFull)}`
    );
  }
}

function main() {
  const report = JSON.parse(fs.readFileSync(process.argv[2] || ARTIFACT_PATH, "utf-8"));

  if (report.subsystem !== "planted_qary_cube_basis_coordinate_bridge") {
    throw new Error(`Unexpected subsystem: ${report.subsystem}`);
  }

  let plantedChecked = 0;
  for (const row of report.planted_instance_audit) {
    const m = row.m;
    const n = row.n;
    const mBox = BigInt(row.M_box);
    const dShift = row.d_shift_analytical;
    if (JSON.stringify(dShift) !== JSON.stringify(row.d_shift_public_lattice)) {
      throw new Error("Analytical d_shift does not match public_lattice d_shift");
    }

    const dFree = dShift.slice(m);
    const dPiv = dShift.slice(0, m);
    const sF = dFree.filter((v) => v !== 0).length;
    if (sF !== row.free_support_s_F || sF < 1) {
      throw new Error(`Invalid free support s_F=${sF}`);
    }

    const maxAbsPiv = dPiv.reduce((acc, v) => Math.max(acc, Math.abs(v)), 0);
    // q may exceed binary64 precision in older artifacts. The envelope remains
    // safe there; exact fixed-q checks below use the small-modulus witnesses.
    const sharpPiv = Number.isSafeInteger(row.q) ? fixedQBound(sF, row.q) : sharpTernaryPivotBound(sF);
    if (maxAbsPiv > sharpPiv || sharpPiv !== row.sharp_ternary_piv_bound) {
      throw new Error(`Pivot bound violation: maxAbsPiv=${maxAbsPiv}, sharpPiv=${sharpPiv}`);
    }

    const dL1 = dShift.reduce((acc, v) => acc + Math.abs(v), 0);
    const sharpL1 = sF + m * sharpPiv;
    if (dL1 !== row.d_l1 || dL1 > sharpL1 || sharpL1 !== row.sharp_ternary_l1_bound) {
      throw new Error(`L1 bound violation: dL1=${dL1}, sharpL1=${sharpL1}`);
    }

    const delta = row.delta_partner_on_hit_coord;
    const deltaL1 = delta.reduce((acc, v) => acc + Math.abs(v), 0);
    const sharpDeltaL1 = (sF - 1) + m * sharpPiv;
    if (deltaL1 !== dL1 - 1 || deltaL1 !== row.delta_l1 || deltaL1 > sharpDeltaL1) {
      throw new Error(`Delta L1 violation: deltaL1=${deltaL1}, dL1=${dL1}, sharpDeltaL1=${sharpDeltaL1}`);
    }

    // Recompute exact box bad fraction 1 - prod_i (M_box - |delta_i|) / M_box^n
    let goodCount = 1n;
    let totalCount = 1n;
    for (const dVal of delta) {
      goodCount *= mBox - BigInt(Math.abs(dVal));
      totalCount *= mBox;
    }
    const badCount = totalCount - goodCount;
    const badFracStr = reduceFrac(badCount, totalCount);
    if (badFracStr !== row.exact_box_p_bad_fraction) {
      throw new Error(
        `Bad fraction mismatch: expected ${row.exact_box_p_bad_fraction}, got ${badFracStr}`
      );
    }

    // Check p_bad <= sharpDeltaL1 / M_box
    if (badCount * mBox > BigInt(sharpDeltaL1) * totalCount) {
      throw new Error(`p_bad exceeds sharp upper bound ${sharpDeltaL1}/${mBox}`);
    }

    // Check mod-3 free coordinate hit
    const hits = [];
    for (let j = m; j < n; j++) {
      if (dShift[j] % 3 !== 0) {
        hits.push(j);
      }
    }
    if (hits.length < 1 || JSON.stringify(hits) !== JSON.stringify(row.free_coordinate_hits_mod_3)) {
      throw new Error(`Free coordinate mod-3 hit mismatch`);
    }
    if (delta[row.first_hit_basis_coordinate] !== 0) {
      throw new Error("Expected zero partner shift on hitting free coordinate");
    }
    plantedChecked += 1;
  }

  let satChecked = 0;
  for (const rec of report.ternary_saturation_family) {
    const expectedSharp = fixedQBound(rec.s_F, rec.q);
    verifyAnalysisBlock(rec.analysis);
    if (rec.q_independent_envelope !== sharpTernaryPivotBound(rec.s_F)) {
      throw new Error("Uniform ternary envelope mismatch");
    }
    const H = rec.public_matrix_H;
    const u = rec.analysis.u_vec;
    for (let i = 0; i < rec.m; ++i) {
      if (H[i].length !== u.length || H[i].slice(0, rec.m).some((x, j) => x !== Number(i === j))) {
        throw new Error("Witness matrix is not full-row-rank systematic");
      }
      let dot = 0n;
      for (let j = 0; j < u.length; ++j) dot += BigInt(H[i][j]) * BigInt(u[j]);
      if (dot % BigInt(rec.q) !== 0n) throw new Error("Saturation witness not in public kernel");
      for (let j = 0; j < rec.s_F; ++j) {
        const c = BigInt(rec.analysis.C_centered[i][j]);
        if ((c - BigInt(H[i][rec.m + j])) % BigInt(rec.q) !== 0n) {
          throw new Error("Witness H and coordinate analysis disagree");
        }
      }
    }
    if (u.some(x => ![-1, 0, 1].includes(x)) || u.slice(rec.m).filter(x => x !== 0).length !== rec.s_F) {
      throw new Error("Witness is not ternary with stated free support");
    }
    if (rec.sharp_ternary_bound !== expectedSharp || rec.achieved_d_piv_0 !== expectedSharp) {
      throw new Error(`Ternary saturation witness failed for q=${rec.q}, s_F=${rec.s_F}`);
    }
    satChecked += 1;
  }

  console.log(
    JSON.stringify(
      {
        status: "ok",
        subsystem: report.subsystem,
        planted_instances_verified: plantedChecked,
        ternary_saturation_witnesses_verified: satChecked,
      },
      null,
      2
    )
  );
}

main();
