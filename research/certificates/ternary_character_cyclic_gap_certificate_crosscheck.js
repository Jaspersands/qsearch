"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto"),cp=require("child_process");
const reportPath=process.argv[2]||path.join(__dirname,"../classical_baselines/ternary_character_cyclic_gap_certificate.json");
const cyclicPath=path.join(__dirname,"../classical_baselines/ternary_character_cyclic_decoder.json");
const gapPath=path.join(__dirname,"../classical_baselines/ternary_character_sdp_gap_certificate.json");
const sourcePath=path.join(__dirname,"../classical_baselines/ternary_character_sdp_decoder.json");
const R=JSON.parse(fs.readFileSync(reportPath,"utf8")),C=JSON.parse(fs.readFileSync(cyclicPath,"utf8"));
const check=(x,m)=>{if(!x)throw Error(m);},key=JSON.stringify,same=(a,b,m)=>check(key(a)===key(b),m);
const hash=p=>crypto.createHash("sha256").update(fs.readFileSync(p)).digest("hex");
check(R.status==="EXACT_FINITE_NATIVE_CHARACTER_SDP_GAP_RESEARCH_ONLY"&&R.strengthening==="ALL_REPRESENTED_COMPLETE_CYCLIC_POSITIVITY","exact strengthened finite scope");
check(R.cyclic_decoder_report_sha256===hash(cyclicPath)&&R.original_gap_report_sha256===hash(gapPath)&&R.source_report_sha256===hash(sourcePath),"pinned strengthened matrices and original records/census");
check(R.cyclic_derivation_sha256===hash(path.join(__dirname,"../TERNARY_CHARACTER_CYCLIC_DECODER.md"))&&R.derivation_sha256===hash(path.join(__dirname,"../TERNARY_CHARACTER_SDP_GAP_CERTIFICATE.md")),"both pinned derivations");
check(R.asymptotic_impossibility_or_speedup_claim===false&&R.numerical_solver_status_used_as_proof===false&&R.numerical_optimizer_reexecuted===false&&R.new_independent_experiment===false,"exact certification, not another experiment or speedup");
same(R.certificates.map(c=>c.seed),[93017,93018],"complete predeclared survivor cohort set");
function gcd(a,b){a=a<0n?-a:a;while(b)[a,b]=[b,a%b];return a;}
function fraction(a,b){const g=gcd(a,b);return b/g===1n?String(a/g):a/g+"/"+b/g;}
const bound=(a,r,k)=>a*BigInt(r[k+(a>=0n?"_lower":"_upper")]);
let total=0;
for(const c of R.certificates){
  const original=C.controls.find(x=>x.seed===c.seed),audit=c.cyclic_feasibility,w=c.witness,K=c.nodes.length,S=BigInt(w.moment_scale);
  check(original&&c.status==="EXACT_FINITE_SDP_CHARACTER_GAP"&&c.strengthening===R.strengthening,"strengthened positive exact gap");
  same(c.nodes,original.model.nodes,"unchanged public node model");same(c.native_nodes,original.model.native_nodes,"unchanged score linkage");
  same(audit.description,original.model.cyclic_description,"EVERY compiled cyclic law retained");
  check(audit.status==="ALL_COMPLETE_CYCLIC_LAWS_EXACTLY_FEASIBLE"&&audit.all_complete_cyclic_laws_exactly_nonnegative===true&&audit.exact_reality_and_normalization_from_conjugate_powers===true&&audit.global_cross_cycle_character_realizability_certified===false,"local exact probability laws are not a global character mixture");
  check(c.cached_census_requires_independent_verifier_replay===true&&c.certification_uses_truth_or_holdout===false&&c.finite_counterexample_is_population_or_asymptotic_failure===false,"cached census proof and finite claim boundary");
  let minimum=null,location=null,count=0;
  audit.description.groups.forEach((g,gi)=>{
    const m=g.order;check(c.modulus%m===0,"actual root subgroup order");
    const v=g.power_entries.map(entry=>{check(Number.isSafeInteger(entry)&&entry>=0&&entry<K*K,"whole moment entry");return[Math.floor(entry/K),entry%K];});
    let[i,j]=v[0];check(w.matrix_real_integer[i][j]===w.moment_scale&&w.matrix_imag_integer[i][j]===0,"exact law normalization");
    v.forEach(([i,j],k)=>{const[a,b]=v[(m-k)%m];check(w.matrix_real_integer[i][j]===w.matrix_real_integer[a][b]&&w.matrix_imag_integer[i][j]===-w.matrix_imag_integer[a][b],"exact reality from conjugate cyclic powers");});
    for(let t=0;t<m;t++){
      let lower=0n;
      v.forEach(([i,j],k)=>{const r=c.root_intervals[(k*t%m)*c.modulus/m];lower+=bound(BigInt(w.matrix_real_integer[i][j]),r,"cos")+bound(BigInt(w.matrix_imag_integer[i][j]),r,"sin");});
      const den=S*2n**48n*BigInt(m);check(lower>=0n,"EVERY strengthened cyclic probability nonnegative EXACTLY");
      if(minimum===null||lower*minimum[1]<minimum[0]*den){minimum=[lower,den];location={group_index:gi,sector:t,order:m};}count++;
    }
  });
  check(count===audit.description.constraints&&count===audit.complete_cyclic_probabilities_exact_lower_checked&&count>0,"all cyclic probability counts");
  check(audit.minimum_complete_cyclic_probability_lower_exact===fraction(...minimum),"exact smallest probability lower bound");same(audit.minimum_lower_location,location,"exact minimum location");total+=count;
}
// Recompile the complete cyclic models independently; verify their source ancestry.
const cyclicCheck=JSON.parse(cp.execFileSync(process.execPath,[path.join(__dirname,"ternary_character_cyclic_decoder_crosscheck.js"),cyclicPath],{encoding:"utf8"}));
check(cyclicCheck.status==="PASS","independent complete cyclic compiler");
// Reuse the generic exact primal verifier on NEW points, including a NEW full
// all-secret census replay. It does not trust cached upper bounds or SCS status.
const primal=JSON.parse(cp.execFileSync(process.execPath,[path.join(__dirname,"ternary_character_sdp_gap_certificate_crosscheck.js"),reportPath],{encoding:"utf8"}));
check(primal.status==="PASS"&&primal.exact_finite_gaps===2,"independent dyadic PSD and all-character score gaps");
console.log(JSON.stringify({status:"PASS",exact_strengthened_gaps:2,exact_complete_cyclic_probabilities_checked:total,
  exact_moment_entries:primal.exact_moment_entries,full_root_secrets_checked:primal.full_root_secrets_checked,
  numerical_eigenvalues_or_solver_status_trusted:false,population_or_asymptotic_impossibility_certified:false}));
