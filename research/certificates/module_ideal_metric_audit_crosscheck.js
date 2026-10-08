"use strict";
const fs = require("fs"), path = require("path"), crypto = require("crypto");
const {check, same} = require("./cyclotomic_exact.js");
const root = path.join(__dirname, "../..");
const R = JSON.parse(fs.readFileSync(process.argv[2] || path.join(root,
  "research/reductions/module_ideal_metric_audit.json"), "utf8"));
const hash = p => crypto.createHash("sha256").update(fs.readFileSync(path.join(root, p))).digest("hex");
check(R.derivation_sha256 === hash("research/MODULE_IDEAL_METRIC_AUDIT.md"), "pinned metric derivation");
check(R.literature_source_record_sha256 === hash("research/literature_audits/module_ideal_metric_sources.json"), "pinned primary literature claim record");
check(R.status === "EXACT_LITERATURE_BRIDGE_FALSIFIERS_REVIEW_PENDING", "exact falsifier, not accepted attack");
for (const flag of ["speedup_claim_allowed", "candidate_record_accepted", "novelty_claim"])
  check(R[flag] === false, "unsupported literature promotion: " + flag);
for (const flag of ["stated_zeta8_base_case_algebra_falsified", "diagonal_ideal_data_is_not_a_uniform_metric_certificate",
  "homogeneous_short_vector_is_not_an_affine_secret_without_a_reduction"])
  check(R.scopes[flag] === true, "precise falsifier scope: " + flag);
for (const flag of ["all_PIP_or_module_SVP_algorithms_refuted", "random_MLWE_average_case_claim_refuted_by_engineered_metric_examples",
  "real_cryptographic_break_or_security_guarantee_established"])
  check(R.scopes[flag] === false, "no general hardness or cryptographic claim: " + flag);

function mul(a, b) {
  check(a.length === b.length, "equal ring dimension");
  const d = a.length, out = Array(d).fill(0n);
  a.forEach((v, i) => b.forEach((w, j) => {out[(i+j)%d] += (i+j >= d ? -1n : 1n)*v*w;}));
  return out;
}
function power(a, k) {
  let out = a.map((v, i) => i === 0 ? 1n : 0n);
  for (; k; k = Math.floor(k/2)) {if (k%2) out = mul(out, a); a = mul(a, a);}
  return out;
}
function matrix(a) {
  const d = a.length;
  return Array.from({length: d}, (_, i) => Array.from({length: d}, (_, j) =>
    a[(i-j+d)%d]*(i < j ? -1n : 1n)));
}
function determinant(A) {
  const n = A.length;
  if (!n) return 1n;
  if (n === 1) return A[0][0];
  return A[0].reduce((s, v, j) => s+(j%2 ? -1n : 1n)*v*
    determinant(A.slice(1).map(r => r.filter((_, k) => k !== j))), 0n);
}
const I4 = Array.from({length: 4}, (_, i) => Array.from({length: 4}, (_, j) => Number(i === j)));
const field = R.zeta8_base_case_control, a = field.sqrt2_coefficients.map(BigInt), u = field.unit_coefficients.map(BigInt), inverse = field.unit_inverse_coefficients.map(BigInt);
check(field.ring === "Z[x]/(x^4+1)=Z[zeta8]", "correct base cyclotomic ring");
same(a.map(String), ["0", "1", "0", "-1"], "actual sqrt2 in the zeta8 power basis");
same(u.map(String), ["1", "1", "0", "-1"], "genuine 1+sqrt2 unit, not an arbitrary replacement");
same(inverse.map(String), ["-1", "1", "0", "-1"], "genuine sqrt2-1 inverse");
same(field.sqrt2_square, [2, 0, 0, 0], "recorded exact square");
same(mul(a, a).map(String), ["2", "0", "0", "0"], "sqrt2 squared");
same(mul(u, inverse).map(String), ["1", "0", "0", "0"], "explicit algebraic unit inverse");
check(determinant(matrix(a)) === 4n && field.sqrt2_field_norm === "4" && field.sqrt2_is_not_a_unit === true,
  "nonunit norm4, not a claimed unit generator");
check(field.unit_power_controls.length === 5, "all exponent controls");
for (const row of field.unit_power_controls) {
  const v = power(u, row.exponent), b = power(inverse, row.exponent);
  same(v.map(String), row.coefficients, "actual exact unit power");
  same(b.map(String), row.inverse_coefficients, "actual exact inverse power");
  same(mul(v, b).map(String), ["1", "0", "0", "0"], "integral inverses prove unit ideal, not just determinant fit");
  check(determinant(matrix(v)) === 1n && row.field_norm === "1" && row.ideal_norm === "1", "unchanged norm of all unit ideals");
  same(row.principal_ideal_integer_HNF, I4, "unit ideal has identity integer HNF");
}
for (const row of field.nonunit_principal_ideal_controls) {
  const b = BigInt(row.rational_generator);
  check(b > 1n && row.ideal_norm === String(b**4n) && row.cannot_be_generated_by_a_unit_power === true, "genuine nonunit ideal");
}
for (const flag of ["exponent_is_not_determined_by_ideal_or_ideal_norm", "claimed_zeta8_base_case_as_stated_falsified"])
  check(field[flag] === true, "base falsifier scope: " + flag);
check(field.general_PIP_algorithms_or_repair_of_the_paper_excluded === false, "other PIP algorithms remain open");

function mm(A, B) {return A.map(row => B[0].map((_, j) => row.reduce((s, v, k) => s+v*B[k][j], 0n)));}
function decode(A) {return A.map(row => row.map(BigInt));}
const serialize = A => A.map(row => row.map(String));
check(R.module_metric_controls.length === 5, "all growing module controls");
for (const c of R.module_metric_controls) {
  const d = c.ring_degree, K = BigInt(c.shear), N = K*K+1n;
  check(Number.isSafeInteger(d) && d >= 2 && !(d&(d-1)) && K >= 1n, "valid cyclotomic family");
  check(c.ring === `Z[x]/(x^${d}+1)` && c.ring_module_rank === 2, "same actual ring and module rank");
  const B = [[N, K], [0n, 1n]], U = [[0n, 1n], [1n, -K]], C = [[K, 1n], [1n, -K]];
  same(serialize(B), c.hard_shape_ring_basis, "original coupled module basis");
  same(serialize([[N, 0n], [0n, 1n]]), c.easy_shape_ring_basis, "diagonal comparison module");
  same(serialize(mm(B, U)), serialize(C), "exact original metric lift");
  check(determinant(U) === -1n, "integer unit basis change, not metric isometry");
  same(serialize(mm(C, C)), serialize([[N, 0n], [0n, N]]), "exact squared Gram, shortest vector theorem");
  // Independent Smith reduction: U*B*swap = diag(1,N), all transforms
  // integral unimodular. Coefficient blocks repeat once per ring coordinate.
  same(serialize(mm(mm(U, B), [[0n, 1n], [1n, 0n]])), serialize([[1n, 0n], [0n, N]]), "full Smith certificate");
  same(c.same_integer_Smith_invariants, [...Array(d).fill("1"), ...Array(d).fill(String(N))], "same integer Smith data");
  same(c.same_successive_diagonal_ideals, [String(N), "1"], "same known principal diagonal ideals");
  check(c.scalar_modulus === String(N) && c.same_determinant_ideal === String(N)
    && c.integer_lattice_determinant_absolute_hex === (N**BigInt(d)).toString(16)
    && c.hard_shape_shortest_coefficient_norm_squared_exact === String(N)
    && c.easy_shape_shortest_coefficient_norm_squared_exact === "1"
    && c.shortest_length_ratio_squared_exact === String(N)
    && c.canonical_all_embeddings_norm_squared_multiplier === d, "exact growing metric separation and volume");
  same(serialize(U), c.unimodular_ring_basis_change, "charged public unimodular map");
  same(serialize(C), c.orthogonal_ring_basis, "explicit easy classical basis");
  check(c.coefficient_Gram_of_orthogonal_basis === `${N}*I_${2*d}`, "coefficient block Gram");
  if (c.exact_coefficient_basis_matrices) {
    const original = decode(c.exact_coefficient_basis_matrices.original), transform = decode(c.exact_coefficient_basis_matrices.unimodular_change);
    const orthogonal = decode(c.exact_coefficient_basis_matrices.orthogonal);
    check(original.length === 2*d && original.every(r => r.length === 2*d), "whole bounded coefficient matrices");
    for (let i = 0; i < 2*d; i++) for (let j = 0; j < 2*d; j++) {
      const row = Math.floor(i/d), col = Math.floor(j/d), t = i%d === j%d;
      check(original[i][j] === (t ? B[row][col] : 0n) && transform[i][j] === (t ? U[row][col] : 0n)
        && orthogonal[i][j] === (t ? C[row][col] : 0n), "every actual coefficient matrix entry");
    }
    same(serialize(mm(original, transform)), serialize(orthogonal), "full bounded module basis equality");
  }
  check(c.explicit_metric_lifting_counterexample_not_random_MLWE_source === true
    && c.both_families_have_polynomial_time_classical_short_bases === true && c.general_module_SVP_hardness_proved === false,
  "engineered geometry is not random-source hardness");
}
const source = R.native_public_kernel_source_theorem;
check(source.public_module_rank === "k+ell" && source.known_determinant_ideal === "(q^k)"
  && source.known_shortest_determinant_generators === "q^k times signed ring monomials", "actual public kernel determinant theorem");
for (const flag of ["shortest_determinant_generator_projected_log_embedding_is_exactly_zero",
  "valid_for_every_public_matrix_not_a_sampling_fit", "same_fact_for_any_unimodular_basis_change_of_this_kernel",
  "different_source_specific_target_ideals_or_decoding_reductions_not_excluded"])
  check(source[flag] === true, "public-source premise: " + flag);
check(R.native_public_kernel_controls.length === 4, "all native public source controls");
for (const c of R.native_public_kernel_controls) {
  const d = c.ring_degree, q = BigInt(c.modulus), A = c.canonical_public_A.map(BigInt), M = matrix(A), B = decode(c.exact_coefficient_basis);
  check(A.length === d && d >= 2 && !(d&(d-1)) && q >= 2n && A.every(x => x >= 0n && x < q), "canonical actual public label");
  check(B.length === 2*d && B.every(r => r.length === 2*d), "complete coefficient public basis");
  for (let i = 0; i < 2*d; i++) for (let j = 0; j < 2*d; j++) {
    const v = i < d ? (j < d ? (i === j ? q : 0n) : M[i][j-d]) : (j >= d && i === j ? 1n : 0n);
    check(B[i][j] === v, "every actual q-ary kernel entry");
  }
  check(c.determinant_ideal_scalar_generator === String(q)
    && c.determinant_ideal_shortest_coefficient_generator_squared_norm === String(q*q)
    && c.public_integer_lattice_determinant_absolute_hex === (q**BigInt(d)).toString(16), "known scalar determinant, not random iid matrix determinant");
  same(c.public_ring_basis, [[String(q), "A"], ["0", "1"]], "public ring basis source");
  check(c.kernel_relation === "g=A*f modq" && c.ring_module_rank === 2
    && c.shortest_determinant_generator_projected_log_embedding_is_exactly_zero === true
    && c.determinant_ideal_contains_no_public_A_information === true
    && c.iid_small_entry_module_matrix_is_not_this_public_kernel_source === true
    && c.arbitrary_module_decoder_or_lattice_attack_refuted === false, "source mismatch is not general hardness");
}
check(R.rectangular_public_kernel_controls.length === 2, "rectangular source controls retained");
for (const c of R.rectangular_public_kernel_controls) {
  const q = BigInt(c.modulus), d = c.ring_degree, k = c.public_rows, ell = c.public_columns;
  const A = c.canonical_public_A.map(row => row.map(v => v.map(BigInt))), B = decode(c.exact_coefficient_basis), size = (k+ell)*d;
  check(k > 0 && ell > 0 && A.length === k && A.every(r => r.length === ell), "actual rectangular module matrix");
  check(B.length === size && B.every(r => r.length === size), "whole rectangular kernel coefficient basis");
  for (let i = 0; i < size; i++) for (let j = 0; j < size; j++) {
    let v = 0n;
    if (i < k*d) v = j < k*d ? (i === j ? q : 0n)
      : -matrix(A[Math.floor(i/d)][Math.floor((j-k*d)/d)])[i%d][(j-k*d)%d];
    else if (i === j) v = 1n;
    check(B[i][j] === v, "every rectangular public kernel basis entry");
  }
  check(c.known_determinant_ideal_scalar_generator === String(q**BigInt(k))
    && c.coefficient_lattice_determinant_absolute_hex === (q**BigInt(k*d)).toString(16), "rank-dependent known scalar determinant ideal");
  for (const flag of ["complete_homogeneous_syndrome_basis_verified", "shortest_determinant_generator_projected_log_embedding_is_exactly_zero", "secret_short_basis_not_supplied"])
    check(c[flag] === true, "no unknown small basis in public source");
}
check(R.homogeneous_affine_controls.length === 3, "all affine controls");
for (const c of R.homogeneous_affine_controls) {
  const q = BigInt(c.modulus), v = c.exact_SVP_output.map(BigInt), s = c.short_secret_in_affine_coset.map(BigInt);
  const mod = x => ((x%q)+q)%q, norm = v => v.reduce((n, a) => n+a*a, 0n);
  check(q >= 5n && q%2n === 1n && c.public_A === 1 && c.public_target === 2, "exact affine source control");
  check(mod(v[0]+v[1]) === 0n && norm(v) === 2n && mod(s[0]+s[1]) === 2n && norm(s) === 2n,
    "short kernel vector is not the affine secret");
  const possibilities = [];
  for (let x = -1n; x <= 1n; x++) for (let y = -1n; y <= 1n; y++) if (mod(x+y) === 2n) possibilities.push([String(x), String(y)]);
  same(possibilities, [s.map(String)], "unique bounded affine secret");
  for (const w of [[1n, 0n], [-1n, 0n], [0n, 1n], [0n, -1n]]) check(mod(w[0]+w[1]) !== 0n, "no norm-one kernel vector");
  check(c.kernel_shortest_squared_norm === "2" && c.SVP_approximation_factor === "1" && c.factor_less_than_q_over_two === true,
    "exact SVP satisfies numerical factor threshold");
  same(c.kernel_basis, [[String(q), "-1"], ["0", "1"]], "public homogeneous lattice basis");
  for (const flag of ["unique_secret_under_coordinate_bound_one", "direct_SVP_vector_identification_is_not_secret_recovery",
    "a_separate_BDD_or_embedding_reduction_is_required"]) check(c[flag] === true, "separate affine decoding obligation");
  check(c.SVP_output_syndrome === 0 && c.secret_syndrome === 2
    && c.random_MLWE_failure_probability_or_cryptographic_hardness_proved === false, "no transfer to random-source security");
}
console.log(JSON.stringify({status: "PASS", exact_unit_power_controls: 5, module_metric_families: 5, native_public_kernel_controls: 6,
  homogeneous_affine_controls: 3, stated_base_case_counterexample: true, cryptographic_break_or_hardness_claimed: false}));
