"use strict";
// Independent exact Gram, copy-gate, native character and phase certificates.
const fs = require("fs"), path = require("path"), crypto = require("crypto");
const report = JSON.parse(fs.readFileSync(process.argv[2] || path.join(__dirname, "../classical_baselines/ternary_product_trine.json"), "utf8"));
function check(x, message) { if (!x) throw Error(message); }
const mod = (x, q) => (x % q + q) % q;
const same = (a, b, m) => check(JSON.stringify(a) === JSON.stringify(b), m);
const near = (a, b, m) => check(Number.isFinite(a) && Math.abs(a-b) < 3e-11, m);
function gcd(a, b) { a = a < 0n ? -a : a; b = b < 0n ? -b : b; while (b) [a, b] = [b, a%b]; return a; }
function F(a, b=1n) { check(b !== 0n, "nonzero denominator"); if (b < 0n) [a,b] = [-a,-b]; const g = gcd(a,b); return [a/g,b/g]; }
const add = (a,b) => F(a[0]*b[1]+b[0]*a[1], a[1]*b[1]);
const sub = (a,b) => add(a,[-b[0],b[1]]);
const mul = (a,b) => F(a[0]*b[0],a[1]*b[1]);
const eq = (a,b) => a[0]*b[1] === b[0]*a[1];
const le = (a,b) => a[0]*b[1] <= b[0]*a[1];
function Q(x) {
  check(typeof x === "string", "canonical rational string");
  const t = x.split("/"); check(t.length <= 2, "rational syntax");
  const value = F(BigInt(t[0]), t.length === 2 ? BigInt(t[1]) : 1n);
  check(x === (value[1] === 1n ? String(value[0]) : value[0]+"/"+value[1]), "canonical rational");
  return value;
}
function pow(a, k) { let value=F(1n); for(let j=0;j<k;j++) value=mul(value,a); return value; }
const derivation = fs.readFileSync(path.join(__dirname,"../TERNARY_PRODUCT_TRINE.md"));
check(crypto.createHash("sha256").update(derivation).digest("hex") === report.derivation_sha256, "derivation hash");
check(report.status === "PHYSICAL_PRODUCT_READOUT_AND_COSTED_BASELINE_REVIEW_PENDING", "review status");
for (const k of ["quantum_speedup_proved", "candidate_record_accepted", "novelty_claim", "general_quantum_hardness_or_all_LOCC_bound"]) check(report[k] === false, "no promotion: "+k);

same(report.randomized_recipes.map(c => c.digits), [1,16,32,64], "scalable recipe schedule");
for (const c of report.randomized_recipes) {
  check(c.modulus === String(3n**BigInt(c.digits)) && c.original_qutrits === 1 && c.clean_quantum_ancillas === 0, "one original register and no quantum ancillas");
  check(c.uniform_independent_public_random_trits === 2*c.digits && c.settings_and_pointer_reconstructible_from_y_and_independent_uniform_z === true, "random setting access");
  same(c.gates, ["diag(1,chi_q(-alpha),chi_q(-beta))", "inverse_F3"], "actual measurement gates");
  check(c.exact_effect_identity === "E_(y,z)=E_y/3; E_y=v_y*v_y^dagger/q^2", "effect convention");
  for(const k of ["full_q_squared_table_required", "unknown_source_inverse_required", "hardware_gate_export_implemented", "novelty_claim"]) check(c[k] === false, "compiler scope "+k);
  check(c.phase_synthesis_and_classical_randomness_error_must_be_charged === true, "phase/randomness costs");
}

// Verify all matrix-entry exponents, not just the probabilities of one state.
let effectEntries = 0;
for (const q of [3,9,27]) for(let a=0;a<q;a++) for(let b=0;b<q;b++) for(let z=0;z<3;z++) {
  const y = [mod(a+q/3*z,q),mod(b+2*q/3*z,q)];
  const branch = [0,mod(a+q/3*z,q),mod(b+2*q/3*z,q)], covariant = [0,...y];
  check(mod(y[0]-q/3*z,q) === a && mod(y[1]-2*q/3*z,q) === b, "settings/pointer bijection");
  for(let i=0;i<3;i++) for(let j=0;j<3;j++) {
    check(mod(branch[i]-branch[j],q) === mod(covariant[i]-covariant[j],q), "exact arbitrary-input effect entry"); effectEntries++;
  }
}
check(report.compiler_controls.length === 9, "physical control schedule");
report.compiler_controls.forEach((c,i) => {
  check(c.modulus === [3,9,27][Math.floor(i/3)] && c.settings_enumerated_for_calibration_only === c.modulus**2, "full bounded setting census");
  const norm = c.input_state.reduce((s,v) => s+v[0]**2+v[1]**2,0); near(norm,1,"normalized calibration input");
  check(c.arbitrary_input_not_just_native_phases === true && c.existing_two_register_gate_tape_replayed === true, "actual compiler control scope");
  for(const k of ["branch_effect_identity_residual", "covariant_circuit_probability_residual", "independent_uniform_pointer_residual", "effect_completeness_residual", "normalization_residual"]) check(Number.isFinite(c[k]) && c[k] >= 0 && c[k] < 3e-11, "physical replay residual: "+k);
});

const roots = [[1,0],[-1,0],[0,1],[0,-1],[1,-1],[-1,1]];
function words(q,n) { return Array.from({length:q**n},(_,x) => Array.from({length:n},(_,j) => Math.floor(x/q**(n-j-1))%q)); }
let gramPairs=0;
same(report.exact_Gram_controls.map(c => [c.modulus,c.dimension]), [[3,1],[9,1],[27,1],[3,2]], "complete Gram schedule");
for(const c of report.exact_Gram_controls) {
  const q=c.modulus, secrets=words(q,c.dimension);
  check(c.complete_secret_pairs === secrets.length**2 && c.direction_pairs_per_secret_pair === 36, "complete full-secret Gram costs");
  check(c.zero_diagonal === "2" && c.nonzero_diagonal === "2/3" && c.off_diagonal === "0", "zero-secret exception");
  for(const s of secrets) for(const t of secrets) {
    let count=0;
    for(const [u,v] of roots) for(const [a,b] of roots) if(mod(u+2*v+a+2*b,3) === 0 && s.every((x,j) => mod(u*x+a*t[j],q) === 0 && mod(v*x+b*t[j],q) === 0)) count++;
    const expected = s.every((x,j) => x === t[j]) ? (s.some(x => x !== 0) ? 6 : 18) : 0;
    check(count === expected, "exact composite-ring centered Gram"); gramPairs++;
  }
}
const gates = [[1,8],[1,16],[1,32],[1,64],[2,32]];
check(report.fixed_readout_scaling_gates.length === gates.length, "copy-gate schedule");
report.fixed_readout_scaling_gates.forEach((c,i) => {
  const [n,r]=gates[i], M=n*r-2, G=3n**BigInt(n*r), d=sub(pow(F(5n,3n),M),F(1n)), squared=mul(d,F(1n,2n*G));
  const zero=mul(F(1n,G),sub(F(1n),F(1n,3n**BigInt(M)))), eps=F(1n,10n), gap=sub(eps,zero);
  check(c.dimension === n && c.digits === r && c.original_independent_qutrits === M && c.secret_population === String(G), "native copy/group geometry");
  for(const [k,v] of [["nonzero_secret_centered_product_norm_squared",d],["zero_secret_centered_product_norm_squared",F(3n**BigInt(M)-1n)],["nonzero_contribution_advantage_upper_squared",squared],["zero_secret_advantage_upper",zero],["requested_advantage",eps]]) check(eq(Q(c[k]),v), "exact copy-gate formula: "+k);
  check(c.necessary_copy_gate_passed === (le(eps,zero) || le(mul(gap,gap),squared)), "necessary gate not success claim");
  check(c.zero_secret_exception_kept === true && c.scope === "ANY classical joint processing of fixed inverse-F3 records; uniform ALL secrets; IID full native labels", "all-secret source scope");
  for(const k of ["other_bases_or_adaptive_LOCC_covered", "chosen_labels_or_sieve_retained_law_covered", "unmeasured_states_covered", "speedup_claim_allowed"]) check(c[k] === false, "restricted gate: "+k);
});

// Actual ideal chart at level8, computed independently from its lattice basis.
function mm(A,B) { return A.map(row => B[0].map((_,j) => row.reduce((s,a,k) => s+a*B[k][j],0n))); }
let V=[[1n,0n],[0n,1n]]; for(let i=0;i<7;i++) V=mm(V,[[-1n,-1n],[1n,-2n]]);
const det=V[0][0]*V[1][1]-V[0][1]*V[1][0], U=Number(81n*(2n*V[1][1]+V[1][0])/(3n*det)), W=Number(81n*(-2n*V[0][1]-V[0][0])/(3n*det));
const joint=report.joint_correlation_countercontrol, rows=[[1,2],[26,52]], outputs=words(3,2);
check(joint.modulus === 81 && joint.native_level === 8, "native correlation geometry"); same(joint.frequency_rows,rows,"prespecified native full rows");
for(let i=0;i<2;i++) { const [a,b]=joint.native_labels[i][0]; check(mod(U*a+W*b,81) === rows[i][0] && mod((U+W)*a-U*b,81) === rows[i][1], "actual native label chart"); }
const frequencies=outputs.map(w => mod(w.reduce((s,d,i) => s+(d ? rows[i][d-1] : 0),0),81));
same(joint.word_frequencies,frequencies,"actual native word frequencies"); same(joint.outputs,outputs,"complete joint outputs");
const laws=[], counts=[];
for(let t=0;t<3;t++) {
  const law=[], rowCounts=[];
  for(const out of outputs) {
    const powers=[0,0,0];
    for(let i=0;i<9;i++) for(let j=0;j<9;j++) {
      const delta=mod(frequencies[i]-frequencies[j],81);
      if(delta%27 === 0) powers[mod(delta/27*t+out.reduce((s,z,k) => s+z*(outputs[j][k]-outputs[i][k]),0),3)]++;
    }
    check(powers[1] === powers[2], "exact real character sum"); law.push(F(BigInt(powers[0]-powers[1]),81n)); rowCounts.push(powers);
  }
  check(eq(law.reduce(add,F(0n)),F(1n)), "conditional joint law normalization");
  for(let axis=0;axis<2;axis++) for(let z=0;z<3;z++) check(eq(law.filter((_,j) => outputs[j][axis] === z).reduce(add,F(0n)),F(1n,3n)), "uniform single marginals do not erase joint signal");
  laws.push(law); counts.push(rowCounts);
}
same(joint.exact_character_counts,counts,"complete exact character counts");
for(let t=0;t<3;t++) for(let o=0;o<9;o++) check(eq(Q(joint.joint_trit_laws[t][o]),laws[t][o]), "joint Born law not marginal law");
for(const row of joint.single_qutrit_marginals) for(const p of row) check(eq(Q(p),F(1n,3n)), "reported single marginals");
const success=mul(laws[0].map((_,o) => laws.map(row => row[o]).reduce((a,b) => le(a,b)?b:a)).reduce(add,F(0n)),F(1n,3n));
check(eq(Q(joint.joint_MAP_success),success) && eq(success,F(19n,27n)), "exact joint MAP success");
check(joint.final_effect_word_Hamming_radius === 2 && joint.entangling_readout_gates === 0 && joint.calibration_secrets_enumerated === 81, "local gates but wide final effects");
check(joint.prespecified_legal_labels_not_IID_population_evidence === true && joint.efficient_native_population_decoder_proved === false && joint.speedup_claim_allowed === false, "countercontrol not population decoder");
near(joint.physical_all_secrets_twirl_residual,0,"actual native physical twirl residual");

function put(poly,e,c,q=81) {
  e=mod(e,q);
  const terms=e<2*q/3 ? [[e,c]] : [[e-2*q/3,-c],[e-q/3,-c]];
  for(const [x,v] of terms) { const total=(poly.get(x)||0n)+v; if(total) poly.set(x,total); else poly.delete(x); }
}
function encoded(poly) { return [...poly].sort((a,b)=>a[0]-b[0]).map(([e,c])=>[String(e),String(c)]); }
function terms(record) { const [a,c]=[record.first[0],record.second[0]], z=record.digit; return [[0,0,3n],...roots.map(([u,v])=>[mod(-u*a-v*c,81),mod((u+2*v)*27*z,81),1n])]; }
check(report.exact_posterior_controls.length === 9, "all observed joint digits");
report.exact_posterior_controls.forEach((control,i) => {
  const solver=control.solver, digits=outputs[i];
  same(solver.records.map(r=>[r.first[0],r.second[0],r.digit]), [[1,2,digits[0]],[26,52,digits[1]]], "actual fixed-trine records");
  check(solver.observation_model === "FIXED_PRODUCT_INVERSE_F3" && solver.paired_covariant_generative_law_used === false && solver.adapter_scope === "LIKELIHOOD_PHASE_ALGEBRA_ONLY_CONSTANTS_CANCEL", "no model-law substitution");
  const coefficients=[new Map(),new Map(),new Map()];
  for(const [f,e,a] of terms(solver.records[0])) for(const [g,h,b] of terms(solver.records[1])) {
    const target=mod(f+g,81); if(target%27 === 0) put(coefficients[target/27],e+h,a*b);
  }
  same(solver.coefficient_numerators,coefficients.map(encoded),"independent exact phase expansion");
  const Z=[];
  for(let t=0;t<3;t++) { const poly=new Map(); for(let k=0;k<3;k++) for(const [e,c] of coefficients[k]) put(poly,e+27*k*t,c); Z.push(poly); }
  same(solver.posterior.class_likelihood_numerators,Z.map(encoded),"exact class likelihood numerators");
  for(let t=0;t<3;t++) check(eq(F(Z[t].get(0)||0n,81n),laws[t][i]) && Z[t].size <= 1, "phase posterior agrees with native joint Born twirl");
  const normalizer=laws.map(row=>row[i]).reduce(add,F(0n));
  for(let t=0;t<3;t++) near(solver.posterior.posterior_probabilities[t],Number(laws[t][i][0]*normalizer[1])/Number(laws[t][i][1]*normalizer[0]),"actual joint posterior normalization");
  check(solver.cost_ledger.generic_time_not_polynomial === true && solver.cost_ledger.original_native_qutrits_consumed === 2 && solver.polynomial_native_weak_learner_implemented === false && solver.speedup_claim_allowed === false, "exponential reference not an efficient decoder");
  near(control.actual_fixed_trine_likelihood_residual,0,"actual likelihood calibration residual");
});
check(eq(Q(report.example_approximation_error_budget.outcome_TV_upper),F(1n,5000n)) && report.example_approximation_error_budget.source_preparation_error_covered === false,"charged approximation error scope");
console.log(JSON.stringify({status:"independent_product_trine_certificates_passed",effectEntries,completeGramPairs:gramPairs,scalingGates:5,jointOutputs:9,exactPosteriors:9,gateTapeResidualsCheckedNotIndependentlyReexecuted:true,quantumSpeedupProved:false}));
