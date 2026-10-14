"use strict";
// Actual all-root block map, paired-source correlation, paid search and original data.
// Statistical/noise premises stay conditional and exponential compilation is charged.
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const E=require("./cyclotomic_exact.js"),D=require("./native_carry_diagonal_slice_crosscheck.js"),R=require("./native_choice_mitm_crosscheck.js"),H=require("./native_short_preimage_crosscheck.js");
const {check,same,rat,str,parse,add,div,mul,cmp}=E;
const ROOT=path.resolve(__dirname,"../.."),REPORT=path.join(ROOT,"research/classical_baselines/native_full_root_slice.json");
const hash=f=>crypto.createHash("sha256").update(fs.readFileSync(f)).digest("hex"),mod=(x,q)=>(x%q+q)%q;
const encode=x=>x<=9007199254740991n&&x>=-9007199254740991n?Number(x):String(x);
const canonical=x=>Array.isArray(x)?x.map(canonical):x&&typeof x==="object"?Object.fromEntries(Object.keys(x).sort().map(k=>[k,canonical(x[k])])):x;
const digest=x=>crypto.createHash("sha256").update(JSON.stringify(canonical(x))).digest("hex");
const tuples=t=>t?tuples(t-1).flatMap(a=>[0,1,2].map(x=>[...a,x])):[[]];
function model(c) {
  const s=c.raw_carry,N=c.output_normalization,S=c.diagonal_slice,W=c.whole_root_problem,context=D.publicCircuit(s),{P,rhs,n,k,q}=context;
  D.normalization(s,N);D.restriction(s,N,S);
  const baseWord=P.solve(rhs,Array(k).fill(0)),base=H.frequency(s.public_family,s.cohort,baseWord),m=q/3n,target=s.target.map((x,i)=>mod(BigInt(x)-BigInt(base[i]),q));
  check(target.every(x=>x%3n===0n),"actual full-root target has the chosen low prefix");
  const choices=[],aSums=[];
  S.directions.forEach(v=>{
    const column=[Array(n).fill(0)],sum=Array(n).fill(0n);
    s.prefix_recipe.free_columns.forEach((site,l)=>{if(v[l])s.public_family.paired_labels[s.cohort][site][0].forEach((a,i)=>sum[i]+=BigInt(a));});
    for(const z of [1,2]){
      const delta=Array(n).fill(0n);
      s.prefix_recipe.free_columns.forEach((site,l)=>{
        const t=v[l]*z%3;if(!t)return;
        const [a,b]=s.public_family.paired_labels[s.cohort][site];
        for(let i=0;i<n;i++)delta[i]+=t===1?BigInt(b[i])-2n*BigInt(a[i]):-BigInt(b[i])-BigInt(a[i]);
      });
      const actual=delta.map(x=>mod(x,q));check(actual.every(x=>x%3n===0n),"integer division by3 is justified for every original block");column.push(actual.map(x=>encode(x/3n)));
    }
    const aSum=sum.map(x=>encode(mod(x,m)));check(column[1].every((x,i)=>mod(BigInt(x)+BigInt(column[2][i])+BigInt(aSum[i]),m)===0n),"actual paired choice correlation, not independent random vectors");choices.push(column);aSums.push(aSum);
  });
  same(W,{diagonal_slice_sha256:digest(S),original_modulus:String(q),remaining_modulus:String(m),original_target:s.target,base_frequency:base,remaining_target:target.map(x=>encode(x/3n)),remaining_choices:choices,parameters:S.parameters,active_block_original_a_sums:aSums,paired_choice_sum_is_minus_original_a_sum:true,independent_ring_choice_distribution_assumed:false,actual_original_word_map_used:true,later_unrestricted_carries_assumed_cubic:false,full_normalized_row_is_supplied:false},"complete original-root block problem");
  return {...context,s,S,W,m,free:z=>Array.from({length:k},(_,l)=>S.directions.reduce((v,a,j)=>v+a[l]*z[j],0)%3),predict:z=>base.map((a,i)=>encode(mod(BigInt(a)+3n*choices.reduce((v,col,j)=>v+BigInt(col[z[j]][i]),0n),q)))};
}
function verifySearch(c,solver) {
  const M=model(c),z=R.replay(M.W.remaining_choices,M.W.remaining_target,M.m,solver);
  if(z===null){
    check(solver.whole_root_target_matched===false&&solver.absence_of_other_original_preimages_inferred===false&&["SEARCH_CAP_EXCEEDED_NOT_NO_SOLUTION","COMPLETE_SEARCH_NO_FULL_ROOT_SOLUTION_ON_THIS_SLICE"].includes(solver.status),"restricted failure is not absence of original preimages");return M;
  }
  const free=M.free(z),word=M.P.solve(M.rhs,free),actual=H.frequency(M.s.public_family,M.s.cohort,word);
  same(actual,M.s.target,"actual ORIGINAL modulus target matched");same(actual,M.predict(z),"all-root block map");same(solver.free_trits,free,"actual slice injection");same(solver.native_word,word,"actual native preimage");same(solver.actual_frequency,actual,"original source frequency");
  check(solver.status==="VERIFIED_CLASSICAL_WHOLE_ROOT_SLICE_WITNESS"&&solver.whole_root_target_matched===true&&solver.coherent_uniform_full_row_sampler===false,"witness is not a uniform row");return M;
}
function moments(L) {
  const n=L.dimension,r=L.root_digits,k=L.prefix_free_trits,t=L.slice_parameters;check([n,r,k,t].every(Number.isSafeInteger)&&n>0&&r>=2&&k>=t&&t>=0,"whole-root population dimensions");
  const E=n*(r-1),s=t-E,short=Math.abs(s)<=512;
  check(L.remaining_group_trits===E&&L.slice_entropy_surplus===s,"remaining FULL group entropy");
  same(L.mean_whole_root_solution_count,{base:3,exponent:s},"whole-root mean not mod9 mean");same(L.variance_factor,{one_minus_base:3,negative_exponent:E},"pairwise-original-frequency variance");
  same(L.solution_existence_upper,{base:3,exponent:Math.min(0,s)},"Markov existence upper");same(L.no_solution_upper,{base:3,exponent:Math.min(0,-s)},"conservative Chebyshev absence upper");
  const mu=short?rat(3n**BigInt(Math.max(0,s)),3n**BigInt(Math.max(0,-s))):null;
  check(L.solution_existence_lower_formula==="mu/(mu+1)"&&L.solution_existence_lower_if_short===(short?str(div(mu,add(mu,rat(1n)))):null),"short exact second-moment existence lower");
  check(L.word_pair_unit_minor==="actual distinct selector coefficient pairs have determinant +/-1"&&L.IID_uniform_entire_higher_original_label_vectors_conditioned_on_low_labels_required===true&&L.full_low_prefix_rank_and_fixed_low_only_target_slice_required===true,"actual ORIGINAL coefficient/source premises");
  ["derived_choices_assumed_independent","population_promises_established_by_artifact","repeated_slices_or_queries_on_same_data_assumed_independent","statistics_construct_a_polynomial_solver_or_coherent_row"].forEach(key=>check(L[key]===false,"population scope "+key));
}
function control(c) {
  const M=verifySearch(c,c.solver),t=M.S.parameters;
  let points;
  if(c.slice_exhaustively_enumerated)points=tuples(t);
  else {
    const all=[Array(t).fill(0),Array.from({length:t},(_,j)=>j%3),Array(t).fill(2)];
    for(let j=0;j<t;j++)for(const z of [1,2]){const p=Array(t).fill(0);p[j]=z;all.push(p);}
    points=[...new Map(all.map(p=>[JSON.stringify(p),p])).values()].sort((a,b)=>{for(let j=0;j<t;j++)if(a[j]!==b[j])return a[j]-b[j];return 0;});
  }
  check(points.length===c.native_word_checks.length&&points.length<=729,"declared finite full-root checks");
  let hits=0;points.forEach((z,j)=>{
    const word=M.P.solve(M.rhs,M.free(z)),actual=H.frequency(M.s.public_family,M.s.cohort,word),predicted=M.predict(z),hit=actual.every((x,i)=>BigInt(x)===BigInt(M.s.target[i]));same(predicted,actual,"exact block additivity at ORIGINAL q");
    same(c.native_word_checks[j],{parameters:z,actual_frequency:actual,is_whole_root_solution:hit},"actual whole-root diagnostic word");hits+=Number(hit);
  });
  check(c.whole_root_solution_count===(c.slice_exhaustively_enumerated?hits:null)&&c.whole_root_model_is_an_unrestricted_row===false,"nonexhaustive verification is not a root count or full row");moments(c.population_ledger);return points.length;
}
function reconstruction(c) {
  const raw=c.original_records,mask=c.known_mask,result=c.result,f=result.public_family,q=BigInt(f.modulus),n=f.dimension,M=f.sites;
  check(raw.length===2*M&&f.cohorts===1&&mask.length===n&&new Set(raw.map(r=>r.source_id)).size===raw.length,"paid original data and mask");
  same(f.paired_labels,[Array.from({length:M},(_,j)=>raw.slice(2*j,2*j+2).map(r=>r.label))],"same original labels for helper and responses");check(result.public_family_sha256===digest(f),"actual family hash");
  const plan=H.plan(n,q),calls=c.helper_cost.calls,probes=result.completed_probe_receipts;check(calls.length===plan.length&&probes.length===plan.length,"complete actual helper batch");same(result.planned_probes,plan,"nonadaptive original-data probes");
  let assignments=0,peak=0;
  calls.forEach((call,j)=>{
    same(call.target,plan[j].frequency,"helper target fixed before responses");check(call.status==="VERIFIED_CLASSICAL_WHOLE_ROOT_SLICE_WITNESS"&&call.whole_root_target_matched===true,"full-root helper success, not mod9");
    const modelData=call.slice_model; same(modelData.raw_carry.public_family,f,"helper preprocessing model uses ORIGINAL labels");same(modelData.raw_carry.target,call.target,"same preprocessed target");
    const context=model(modelData),probe=probes[j],receipt=probe.receipt;const free=context.s.prefix_recipe.free_columns.map(i=>receipt.word[i]);
    const parameters=context.S.directions.map(v=>free[v.findIndex(x=>x===1)]);same(context.free(parameters),free,"word actually belongs to recorded slice");same(context.P.solve(context.rhs,free),receipt.word,"actual prefix inverse matches helper word");
    const solver={status:call.status,parameters,cost:call.cost,assignments_evaluated:call.assignments_evaluated,stored_entries:call.stored_entries,whole_root_target_matched:true,free_trits:free,native_word:receipt.word,actual_frequency:H.frequency(f,receipt.cohort,receipt.word),coherent_uniform_full_row_sampler:false};verifySearch(modelData,solver);
    check(call.parameters===context.S.parameters&&receipt.public_family_sha256===digest(f)&&receipt.cohort===0,"full helper model/receipt binding");same(receipt.target,plan[j].frequency,"receipt requested target");same(probe.requested_frequency,plan[j].frequency,"actual evaluated target");
    const beta=receipt.word.flatMap(t=>[[1,0],[-1,1],[0,-1]][t]),ids=raw.filter((r,i)=>beta[i]).map(r=>r.source_id);
    const value=raw.reduce((s,r,i)=>s+BigInt(beta[i])*(BigInt(r.value)+r.label.reduce((v,a,k)=>v+BigInt(a)*BigInt(mask[k]),0n)),0n);
    same(probe.signed_original_coefficients,beta,"original signed response coefficients");same(probe.active_original_source_IDs,ids,"same original ancestors reused");check(probe.coefficient_squared_norm===beta.reduce((s,b)=>s+b*b,0)&&probe.derived_masked_response===encode(mod(value,q))&&probe.fresh_original_errors_created===false,"actual masked response, no fresh noise");assignments+=call.assignments_evaluated;peak=Math.max(peak,call.stored_entries);
  });
  const d=H.decode(probes,n,q),original=d.masked.map((x,i)=>encode(mod(BigInt(x)-BigInt(mask[i]),q)));
  same(result.masked_secret,d.masked,"exact reconstructed masked secret");same(result.decisions,d.decisions,"actual complete trit decisions");same(result.original_secret,original,"known mask removed");
  check(result.status==="COMPLETE_RECEIPT_CHECKED_CLASSICAL_RECONSTRUCTION"&&result.helper_calls===plan.length&&result.original_records_paid_once===raw.length&&result.correctness_requires_the_stated_noise_bound===true,"conditional original-data decoder, not proof from small outputs");
  ["helper_classical_polynomial_runtime_proved_by_receipts","helper_label_only_independence_proved_by_API","new_quantum_algorithm_or_speedup"].forEach(key=>check(result[key]===false,"generic decoder scope "+key));
  raw.forEach((r,i)=>check(mod(r.label.reduce((s,a,j)=>s+BigInt(a)*BigInt(c.truth_fixture_only.original_secret[j]),0n)+BigInt(c.truth_fixture_only.original_errors[i]),q)===BigInt(r.value),"actual calibration source errors"));
  check(c.matches_truth_fixture===(JSON.stringify(original)===JSON.stringify(c.truth_fixture_only.original_secret))&&c.secret_or_errors_used_by_helper_or_decoder===false&&c.noise_correctness_inferred_from_small_outputs===false,"truth is fixture only");
  const cost=c.helper_cost;check(cost.total_assignments_evaluated===assignments&&cost.peak_stored_entries===peak&&cost.public_label_elements_per_query===2*n*M,"actual whole-batch work and original public data");same(cost.prefix_matrix_dimensions_per_query,[n,M],"per-query matrix preprocessing");
  check(cost.matrix_and_block_preprocessing_arithmetic_order==="O(n^2*M+n^3) per query with O(log(q))-bit operands"&&cost.search_is_exponential===true&&cost.left_table_is_rebuilt_and_charged_per_query===true,"no free preprocessing or uncharged reuse");
  ["preprocessing_or_search_is_free","matrix_preprocessing_is_free","polynomial_classical_helper_supplied","coherent_uniform_full_row_sampler_supplied","best_classical_runtime_bound_proved"].forEach(key=>check(cost[key]===false,"helper cost scope "+key));return assignments;
}
function tradeoff(T) {
  const n=T.dimension,r=T.root_digits,E=n*(r-1);let e=0,p=1;while(p<n*r+1){p*=3;e++;}const s=e+6,t=E+s,M=(n+1)*t+n;
  check(T.sites===M&&T.original_classical_records===2*M&&T.guaranteed_slice_parameters===t&&T.entropy_surplus===s&&T.nonadaptive_original_probes===n*r,"exact larger-bank entropy and all-original-data counts");
  check(T.conditional_batch_absence_probability_upper_if_complete_search===str(rat(BigInt(n*r),3n**BigInt(s)))&&T.rank_failure_upper_used_in_budget===str(rat(1n,3n**BigInt(s)))&&T.whole_batch_helper_failure_upper_if_complete_search===str(rat(BigInt(n*r+1),3n**BigInt(s)))&&T.meet_in_middle_left_assignment_trits===Math.floor(t/2)&&T.meet_in_middle_right_assignment_trits===t-Math.floor(t/2)&&T.full_prefix_projection_loss_trits===M-n-t,"statistical union, rank failure, exponential work and lost mass distinct");moments(T.whole_root_population);
  same(T.rank_failure_upper_compact,{hyperplanes_numerator_base:3,hyperplanes_numerator_exponent:n,hyperplanes_numerator_subtract:1,hyperplanes_denominator:2,single_hyperplane_probability_base:3,single_hyperplane_probability_negative_exponent:M},"uniform low-slope projective hyperplane rank bound");check(M-n>=s,"conservative rank budget is justified");
  const L=T.original_secret_noise_ledger_if_complete_helper,q=3n**BigInt(r),V=add(rat(q*q,3n*BigInt(n)**6n),rat(1n,2n));check(L.true_original_second_moment_upper===str(V)&&L.dimension===n&&BigInt(L.modulus)===q&&L.cohorts===1&&L.sites===M&&L.whole_batch_helper_failure_upper===T.whole_batch_helper_failure_upper_if_complete_search,"same true source/noise/helper premises");H.ledger(L);
  check(T.complete_exponential_search_is_assumed_low_rank_failure_is_charged===true&&T.IID_uniform_original_low_and_higher_labels_required===true&&T.live_caps_proved_sufficient_for_scalable_search===false&&T.true_original_noise_model_established_by_artifact===false&&T.statistical_or_noise_feasibility_is_polynomial_runtime===false,"feasibility is not an implemented scalable decoder");
}
function verify(p) {
  check(p.status==="EXACT_ALL_ROOT_NATIVE_SLICE_AND_EXPONENTIAL_ORIGINAL_DATA_BASELINE_REVIEW_PENDING","review-pending all-root baseline");check(p.producer_sha256===hash(path.join(ROOT,"theorems/native_full_root_slice.py"))&&p.derivation_sha256===hash(path.join(ROOT,"research/NATIVE_FULL_ROOT_SLICE.md")),"current code and derivation");
  const deps=["native_carry_diagonal_slice.py","native_choice_mitm.py","native_prefix_carry_lift.py","native_affine_fibre_relaxation.py","native_known_seed_group_workbench.py","native_short_preimage_reduction.py","ternary_covariant_noise.py","ternary_measured_lattice_decoder.py","ternary_noise_degradation.py"];
  same(Object.keys(p.dependency_sha256).sort(),deps.sort(),"all direct source dependencies");deps.forEach(f=>check(p.dependency_sha256[f]===hash(path.join(ROOT,"theorems",f)),"dependency "+f));
  check(p.whole_root_slice_controls.length===5&&p.original_data_reconstruction_controls.length===3&&p.quadratic_bank_whole_root_ledgers.length===4&&p.larger_bank_tradeoffs.length===4,"declared live coverage");
  const points=p.whole_root_slice_controls.map(control),work=p.original_data_reconstruction_controls.map(reconstruction);p.quadratic_bank_whole_root_ledgers.forEach(moments);p.larger_bank_tradeoffs.forEach(tradeoff);
  ["accepted_speedup_candidate","new_active_negative_result_created","polynomial_full_root_preimage_helper_or_uniform_coherent_row_supplied"].forEach(key=>check(p[key]===false,"report scope "+key));
  return {verified:true,original_root_word_checks:points.reduce((a,b)=>a+b,0),original_data_reconstructions:3,paid_helper_assignments:work.reduce((a,b)=>a+b,0),scaling_ledgers:8,polynomial_solver_or_coherent_row_supplied:false};
}
module.exports={verify,model,moments,reconstruction,tradeoff};
if(require.main===module)console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(process.argv[2]||REPORT))),null,2));
