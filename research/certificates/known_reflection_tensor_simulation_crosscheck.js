"use strict";
// Independent source, error/resource ledgers and exact finite-coin decisions.
// This checker does NOT independently reconstruct the complete tensor program.
const fs = require("fs"), path = require("path"), crypto = require("crypto");
const E = require("./cyclotomic_exact.js"), {check, same, rat, parse, add, sub, mul, div, cmp, str, one} = E;
const ROOT = path.resolve(__dirname, "../.."), REPORT = path.join(ROOT, "research/classical_baselines/known_reflection_tensor_simulation.json");
const hash = f => crypto.createHash("sha256").update(fs.readFileSync(f)).digest("hex");
const min = (a,b) => cmp(a,b) <= 0n ? a : b;
const eq = (s,x,m) => check(s === str(x), m);
function power(x,n) { let r=one; while(n) { if(n%2) r=mul(r,x); n=Math.floor(n/2); if(n) x=mul(x,x); } return r; }
function budget(b) {
  const B=b.cohorts, M=b.sites_per_cohort, T=b.reflection_cap, G=b.local_gate_cap, h=b.approximation_bits;
  check(Number.isSafeInteger(B)&&B>0&&(BigInt(B)&(BigInt(B)-1n))===0n&&Number.isSafeInteger(M)&&M>0&&Number.isInteger(T)&&T>=0&&Number.isInteger(G)&&G>=0&&h>0, "committed finite known-program resource shape");
  const delta=rat(1n,2n**BigInt(h)), e=sub(power(add(one,delta),M),one), eta=add(mul(rat(4n),e),mul(rat(2n),mul(e,e)));
  const error=sub(mul(mul(add(one,e),power(add(one,mul(rat(3n),delta)),G)),power(add(one,eta),T)),one);
  const attempts=b.sampling_failure_bits+M.toString(2).length, abort=rat(BigInt(M+1),2n**BigInt(attempts));
  eq(b.per_qutrit_vector_error_upper,delta,"source vector approximation");
  eq(b.seed_relative_vector_error_upper,e,"orthogonal cohort approximation, not dimension explosion");
  eq(b.reflection_operator_error_upper,eta,"actual approximate projector reflection error");
  eq(b.final_relative_vector_error_upper,error,"near-unitary whole-program hybrid");
  eq(b.logical_measurement_TV_upper,min(one,mul(rat(2n),error)),"normalized output measurement error");
  eq(b.unconditional_coin_abort_upper,abort,"all finite rejection caps charged");
  eq(b.complete_logical_sampling_TV_or_abort_upper,min(one,add(mul(rat(2n),error),abort)),"unconditional approximation plus abort");
  const p=3*h+32;
  check(b.max_tensor_terms===B*(T+1)&&b.coin_attempt_cap_per_factor===attempts&&b.dyadic_entry_denominator_exponent_upper===p&&b.factor_denominator_exponent_upper===(G+1)*p&&b.coefficient_denominator_exponent_upper===T*(M*(G+2)*p+Math.log2(B)),"polynomial rank and dyadic bit ledgers");
  ["source_noise_law_or_independence_required","normalized_approximation_is_exact_ideal_quantum_program","subsystem_reflections_or_entangled_work_covered","quantum_only_unknown_source_covered","conditioning_away_coin_abort_allowed"].forEach(k=>check(b[k]===false,"classical counterpart scope "+k));
}
function dyadic(s) {
  check(typeof s==="string", "exact encoded rational weight");
  const p=s.split("/"); check(p.length<=2,"weight syntax");
  const n=BigInt(p[0]),d=p.length===1?1n:BigInt(p[1]);
  check(n>=0n&&d>0n&&(d&(d-1n))===0n&&(d===1n||(n&1n)===1n),"canonical nonnegative dyadic weight");
  return [n,d];
}
function source(c) {
  const r=c.recipe, q=BigInt(c.modulus), B=r.cohorts, M=r.sites_per_cohort, src=r.source_receipts, raw=src.original_classical_records, mask=src.preparation_random_mask.map(BigInt);
  check(String(r.modulus)===String(q)&&raw.length===2*B*M&&new Set(raw.map(a=>a.source_id)).size===raw.length,"actual paid raw source bank");
  for(let b=0;b<B;b++) for(let j=0;j<M;j++) {
    const pair=raw.slice(2*(b*M+j),2*(b*M+j)+2);
    const phases=pair.map(a=>{check(BigInt(a.modulus)===q&&a.label.length===mask.length,"actual source modulus and mask dimension"); return (BigInt(a.value)+a.label.reduce((s,x,k)=>s+BigInt(x)*mask[k],0n))%q;});
    same(r.known_phase_numerators[b][j].map(String),["0",...phases.map(String)],"known noisy phases, no secret reconstruction");
  }
  check(c.hidden_secret_or_error_used===false&&c.unknown_state_regenerated===false&&c.scalable_path_builds_root_table===false,"no unknown regeneration or root table");
}
function coins(c) {
  let norm=dyadic(c.final_rational_norm_squared);
  const s=c.final_computational_sample, decisions=s.decisions;
  check(decisions.length===c.recipe.sites_per_cohort+1&&s.status==="CERTIFIED_RATIONAL_POINT_SAMPLE", "complete recorded finite samples");
  check(s.conditional_on_completion_is_exact_rational_program_law===false&&s.conditional_on_completion_is_exact_ideal_quantum_law===false,"whole-completion conditioning is not a free exact channel");
  decisions.forEach((d,slot)=>{
    const weights=d.exact_branch_weights.map(dyadic), scale=BigInt(d.integer_weight_scale), counts=d.integer_weights.map(BigInt), total=BigInt(d.uniform_integer_total);
    check(d.slot===slot&&counts.length===(slot===0?c.recipe.cohorts:3)&&scale>0n&&(scale&(scale-1n))===0n,"actual local measurement slots and integer scale");
    weights.forEach((w,j)=>check(w[0]*scale===counts[j]*w[1]&&counts[j]>=0n,"exact integer branch conversion"));
    check(counts.reduce((a,b)=>a+b,0n)===total&&total>0n&&total*norm[1]===norm[0]*scale,"prefix Gram weights sum, no branch normalization loss");
    const draws=d.coin_draws.map(BigInt), cap=c.budget.coin_attempt_cap_per_factor, bits=d.coin_bits_per_attempt, chosen=d.selected_outcome;
    check(draws.length>0&&draws.length<=cap&&2n**BigInt(bits)>=total&&(bits===0||2n**BigInt(bits-1)<total),"minimal uniform-bit range and committed attempt cap");
    check(draws.every(x=>x>=0n&&x<2n**BigInt(bits))&&draws.slice(0,-1).every(x=>x>=total),"all rejected coin blocks retained");
    const lower=counts.slice(0,chosen).reduce((a,b)=>a+b,0n), upper=lower+counts[chosen], accepted=draws.at(-1);
    check(Number.isInteger(chosen)&&chosen>=0&&chosen<counts.length&&accepted>=lower&&accepted<upper,"actual accepted coin lies inside selected nonzero outcome");
    check(s.outcomes[slot]===chosen,"recorded final outcome"); norm=weights[chosen];
  });
}
function run(r) {
  check(r.status==="SCOPED_KNOWN_FULL_SYSTEM_REFLECTION_TENSOR_SIMULATION_REVIEW_PENDING","scoped simulation review status");
  check(r.producer_sha256===hash(path.join(ROOT,"theorems/known_reflection_tensor_simulation.py"))&&r.derivation_sha256===hash(path.join(ROOT,"research/KNOWN_REFLECTION_TENSOR_SIMULATION.md")),"pinned producer and derivation");
  same(Object.keys(r.dependency_sha256).sort(),["known_preparation_coherent_reflection.py","known_preparation_packet_simulation.py","native_noisy_phase_input.py","ternary_certified_noise_sampler.py"].sort(),"critical source and precision dependencies");
  Object.entries(r.dependency_sha256).forEach(([name,h])=>check(h===hash(path.join(ROOT,"theorems",name)),"pinned source/precision dependency"));
  ["generic_quantum_classical_simulation_proved","opaque_HSP_inputs_dequantized","subsystem_reflection_programs_dequantized","accepted_speedup_candidate","new_active_negative_result_created"].forEach(k=>check(r[k]===false,"unsupported simulation promotion "+k));
  same(r.controls.map(c=>[c.recipe.cohorts,c.recipe.sites_per_cohort,c.budget.reflection_cap]),[[1,3,4],[2,2,6],[2,16,3],[1,32,3]],"finite and high-root closure controls");
  r.controls.forEach(c=>{
    source(c); budget(c.budget); coins(c);
    check(c.final_tensor_terms===c.budget.max_tensor_terms&&c.largest_coefficient_denominator_exponent<=c.budget.coefficient_denominator_exponent_upper&&c.largest_factor_denominator_exponent<=c.budget.factor_denominator_exponent_upper,"actual polynomial rank/precision caps");
    c.program_history.forEach((s,t)=>check(s.step===t&&s.tensor_terms===c.recipe.cohorts*(t+2),"one paid bank added per full-system reflection"));
  });
  return {status:"PASS",source_controls:4,ledger_controls:4,exact_coin_transcripts:4,complete_tensor_arithmetic_independently_reconstructed:false,accepted_speedup_candidate:false};
}
if(require.main===module) console.log(JSON.stringify(run(JSON.parse(fs.readFileSync(process.argv[2]||REPORT,"utf8"))),null,2));
module.exports={run,budget,coins};
