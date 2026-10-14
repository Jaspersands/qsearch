"use strict";
// Independent native characters, complete zero/nonzero laws, Fourier fibres and price.
// The scalable shadow's exact coin decisions are checked, not its entire tensor kernel.
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const E=require("./cyclotomic_exact.js"),{chart}=require("./native_generalized_dihedral_crosscheck.js");
const coherent=require("./known_preparation_coherent_reflection_crosscheck.js"), tensor=require("./known_reflection_tensor_simulation_crosscheck.js");
const {check,same,rat,parse,str,add,sub,mul,div,cmp,one,zero,field}=E;
const ROOT=path.resolve(__dirname,"../.."), REPORT=path.join(ROOT,"research/reductions/native_known_seed_group_workbench.json");
const hash=f=>crypto.createHash("sha256").update(fs.readFileSync(f)).digest("hex");
const mod=(a,q)=>(a%q+q)%q, min=(a,b)=>cmp(a,b)<=0n?a:b, max=(a,b)=>cmp(a,b)>=0n?a:b;
const eq=(s,x,m)=>check(s===str(x),m), words=M=>M?words(M-1).flatMap(w=>[0,1,2].map(t=>[...w,t])):[[]];
function scalar(K,C,recipe,g) {
  const [raw,t]=g,q=K.q,B=recipe.cohorts,M=recipe.sites_per_cohort;
  let result=K.F();
  for(let b=0;b<B;b++) {
    let term=K.unit;
    for(let j=0;j<M;j++) {
      const p=recipe.known_phase_numerators[b][j], label=recipe.public_native_labels[b][j], dual=C.dual(label);
      let local=K.F();
      for(let out=0;out<3;out++) {
        const root=[[1n,0n],[0n,1n],[-1n,-1n]][out];
        const rotated=raw.map(a=>C.mul(a.map(BigInt),root));
        const angle=C.character(dual,C.coordinates(rotated)), scaled=angle[0]*BigInt(q);
        check(scaled%angle[1]===0n,"true carried-group character lies at the declared root");
        const exponent=mod(p[(out+t)%3]-p[out]+Number(scaled/angle[1]),q);
        local=K.plus(local,K.scale(K.powers[exponent],rat(1n,3n)));
      }
      term=K.times(term,local);
    }
    result=K.plus(result,K.scale(term,rat(1n,BigInt(B))));
  }
  return result;
}
function candidate(C,g) {
  if(g[1]===0)return null;
  const inverse=g[1]===1?[1n,0n]:[0n,-1n];
  return g[0].map(a=>C.mul(a.map(x=>-BigInt(x)),inverse).map(Number));
}
function source(recipe) {
  const q=Number(recipe.modulus),B=recipe.cohorts,M=recipe.sites_per_cohort,raw=recipe.source_receipts.original_classical_records,mask=recipe.source_receipts.preparation_random_mask;
  check([3,9].includes(q)&&raw.length===2*B*M&&new Set(raw.map(r=>r.source_id)).size===raw.length,"paid actual finite original records");
  const r=q===3?1:2; let u=-1,v=1;
  for(let j=0;j<(r-1)%6;j++)[u,v]=[u+v,-u];
  for(let b=0;b<B;b++)for(let j=0;j<M;j++){
    const pair=raw.slice(2*(b*M+j),2*(b*M+j)+2);
    const p=[0,...pair.map(a=>mod(a.value+a.label.reduce((s,x,k)=>s+x*mask[k],0),q))];
    same(recipe.known_phase_numerators[b][j],p,"actual original-data point phases");
    const labels=pair[0].label.map((a,k)=>[mod(u*a+v*pair[1].label[k],q),mod((u+v)*a-u*pair[1].label[k],q)]);
    same(recipe.public_native_labels[b][j],labels,"actual even native frequency chart");
  }
  check(recipe.ideal_unknown_state_inverse_supplied===false&&recipe.secret_or_errors_read_by_preparation===false,"legal actual inverse, no secret source gate");
}
function spec(s,recipe) {
  const q=BigInt(recipe.modulus),n=recipe.secret_dimension,L=recipe.native_even_level,B=recipe.cohorts,M=recipe.sites_per_cohort;
  const slice=s.domain==="INTEGER_SECRET_SLICE";
  check(slice||s.domain==="FULL_NATIVE_GROUP","declared domain");
  check(s.uniform_work_size===String(slice?q**BigInt(n):3n*q**BigInt(2*n))&&s.work_coordinate_trits===(slice?n*(L/2):n*L+1),"restricted and full normalization are different");
  check(s.source_preparation_calls===1&&s.actual_source_inverse_calls===1&&s.controlled_qutrit_cyclic_permutations===M&&s.controlled_character_branches_upper===3*B*M&&s.index_comparison_compute_uncompute_pairs_upper===B&&s.original_classical_records_paid_once===2*B*M,"all real source/character controls charged");
  ["arbitrary_chosen_source_label_oracle_supplied","QRAM_supplied","physical_gate_compiler_supplied","postselection_is_free","work_Fourier_interference_is_classically_simulated_by_early_measurement"].forEach(k=>check(s[k]===false,"work recipe scope "+k));
  check(s.point_inverse_uses_original_values_not_secret===true,"original-data access only");
}
function amplification(K,a,p,correct,accepted) {
  check(a.whole_orbit_reflection_is_actual_known_preparation_reflection===true&&a.point_gate_reflection_is_unknown_input_copy_reflection===false&&a.normalization_is_free===false,"actual known A and paid full reflection");
  let prev=K.unit, current=K.plus(K.scale(K.unit,rat(3n)),K.scale(p,rat(-4n)));
  a.iteration_history.forEach((r,j)=>{
    let gain;
    if(j===0)gain=K.unit;
    else if(j===1)gain=current;
    else { const next=K.plus(K.times(K.plus(K.scale(K.unit,rat(2n)),K.scale(p,rat(-4n))),current),K.scale(prev,rat(-1n)));prev=current;current=next;gain=next; }
    const g2=K.times(gain,gain),prob=K.times(p,g2);
    same(r.source_zero_mass_exact,K.encode(prob),"exact two-reflection zero probability");
    same(r.correct_and_zero_mass_exact,K.encode(K.times(correct,g2)),"no hidden signal created by amplification");
    same(r.candidate_and_zero_mass_exact,K.encode(K.times(accepted,g2)),"whole normalized good distribution unchanged");
    check(r.iterations===j&&r.pure_joint_preparation_or_inverse_calls===2*j+1&&r.normalized_good_distribution_changed===false,"all full A/inverse calls charged");
    check(E.sign(K,K.plus(K.scale(p,rat(BigInt((2*j+1)**2))),K.scale(prob,rat(-1n))))>=0,"paid quadratic amplification envelope");
  });
}
function control(c) {
  const r=c.source_recipe,q=Number(r.modulus),n=r.secret_dimension,B=r.cohorts,M=r.sites_per_cohort,K=field(q),C=chart(r.native_even_level,n);
  source(r); coherent.central(c.central_support,r.public_native_labels);
  const sectors=new Set(c.central_support.cohort_central_character_rows.map(JSON.stringify)).size;
  check(c.distinct_central_characters===sectors,"actual central support, not source dimension");
  const truth=c.truth_fixture_only.masked_integer_secret.map(s=>[s,0]);
  const errors=c.truth_fixture_only.errors,rawSource=r.source_receipts.original_classical_records;
  rawSource.forEach((record,i)=>{
    const expected=mod(record.label.reduce((sum,a,j)=>sum+a*truth[j][0],0)+errors[i],q);
    check(r.known_phase_numerators[Math.floor(i/(2*M))][Math.floor(i/2)%M][1+i%2]===expected,"truth/error fixture is consistent with actual prepared values");
  });
  let overlap=K.F();
  for(let b=0;b<B;b++){
    let local=K.unit;
    for(let j=0;j<M;j++){
      const i=2*(b*M+j),single=K.scale(K.plus(K.unit,K.plus(K.powers[mod(errors[i],q)],K.powers[mod(errors[i+1],q)])),rat(1n,3n));
      local=K.times(local,single);
    }
    overlap=K.plus(overlap,K.scale(local,rat(1n,BigInt(B))));
  }
  const error2=K.plus(K.unit,K.scale(K.times(overlap,K.conj(overlap)),rat(-1n)));
  same(c.actual_vs_ideal_pure_trace_distance_squared_exact,K.encode(error2),"actual complete indexed-seed fidelity, not an inferred marginal");
  c.domain_controls.forEach(d=>{
    spec(d.recipe,r);
    const slice=d.recipe.domain==="INTEGER_SECRET_SLICE",expected=[];
    // Generate the complete domain independently from canonical coordinates.
    let values=[[]];for(let j=0;j<(slice?n:2*n);j++)values=values.flatMap(a=>Array.from({length:q},(_,x)=>[...a,x]));
    values.forEach(a=>{
      const v=slice?a.map(x=>[x,0]):Array.from({length:n},(_,j)=>a.slice(2*j,2*j+2));
      (slice?[1]:[0,1,2]).forEach(t=>expected.push([v,t]));
    });
    same(d.group_rows.map(x=>x.group_element),expected,"complete group/work domain, no omitted failures");
    let p=K.F(),correct=K.F(),accepted=K.F();
    d.group_rows.forEach(row=>{
      const m=scalar(K,C,r,row.group_element),prob=K.times(m,K.conj(m)),other=K.plus(K.unit,K.scale(prob,rat(-1n)));
      same(row.source_zero_amplitude_exact,K.encode(m),"actual controlled native character/point inverse amplitude");
      same(row.source_zero_probability_exact,K.encode(prob),"actual zero Born law");
      same(row.source_nonzero_probability_exact,K.encode(other),"all complementary source mass retained");
      check(E.sign(K,other)>=0,"nonnegative nonzero branch");
      const guess=candidate(C,row.group_element),right=guess!==null&&JSON.stringify(guess)===JSON.stringify(truth);
      same(row.decoded_candidate,guess,"correct inverse lambda chart, identity is not decoding");
      check(row.candidate_matches_truth_fixture===right,"full-secret success, not arbitrary subgroup hit");
      const weighted=K.scale(prob,rat(1n,BigInt(expected.length)));
      p=K.plus(p,weighted);if(guess!==null)accepted=K.plus(accepted,weighted);if(right)correct=K.plus(correct,weighted);
    });
    same(d.source_zero_mass_exact,K.encode(p),"unconditional source-zero probability");
    same(d.correct_decoding_and_zero_mass_exact,K.encode(correct),"unconditional correct-and-zero probability");
    same(d.nonidentity_candidate_and_zero_mass_exact,K.encode(accepted),"identity rejection is charged");
    if(!slice){
      const cap=min(one,rat(BigInt(sectors),3n**BigInt(n)));
      eq(d.full_group_central_conditional_correct_upper,cap,"central point-evaluation ceiling");
      check(E.sign(K,K.plus(K.scale(accepted,cap),K.scale(correct,rat(-1n))))>=0,"central ceiling holds also with actual phase noise");
    }else check(d.full_group_central_conditional_correct_upper===null,"no full-group ceiling after public promise restriction");
    check(d.full_group_ceiling_applied_to_integer_slice===false,"integer promise falsifier preserved");
    amplification(K,d.actual_whole_preparation_amplification,p,correct,accepted);
  });
  const kernel=c.integer_kernel,D=B*3**M;
  let grid=[[]];for(let j=0;j<n;j++)grid=grid.flatMap(a=>Array.from({length:q},(_,x)=>[...a,x]));
  const counts=new Map(grid.map(a=>[JSON.stringify(a),0])),coeff=new Map(grid.map(a=>[JSON.stringify(a),K.F()])), expectedWords=[];
  const raw=r.source_receipts.original_classical_records;
  for(let b=0;b<B;b++)for(const word of words(M)){
    const sigma=Array(n).fill(0);let phase=0;
    word.forEach((t,j)=>{
      const a=raw[2*(b*M+j)].label,z=raw[2*(b*M+j)+1].label,p=r.known_phase_numerators[b][j],y=p[1],v=p[2];
      a.forEach((x,k)=>sigma[k]=mod(sigma[k]+[x,z[k]-x,-z[k]][t],q));
      phase=mod(phase+[y,v-y,-v][t],q);
    });
    const key=JSON.stringify(sigma);counts.set(key,counts.get(key)+1);coeff.set(key,K.plus(coeff.get(key),K.scale(K.powers[phase],rat(1n,BigInt(D)))));
    expectedWords.push({cohort:b,word,frequency:sigma,known_phase:phase});
  }
  same(kernel.words,expectedWords,"complete actual weighted frequency/phase words");same(kernel.frequencies,grid,"all integer Fourier labels, including empty fibres");
  same(kernel.pushforward_counts,grid.map(a=>counts.get(JSON.stringify(a))),"public pushforward counts");
  same(kernel.actual_Fourier_coefficients_exact,grid.map(a=>K.encode(coeff.get(JSON.stringify(a)))),"actual complex fibre amplitudes, not sqrt counts");
  const p2=grid.reduce((sum,a)=>add(sum,rat(BigInt(counts.get(JSON.stringify(a))**2),BigInt(D*D))),zero);
  eq(kernel.ideal_collision_mass,p2,"correct absolute collision normalization");
  let zeroMass=K.F();const slice=c.domain_controls[1];
  grid.forEach(k=>{
    const z=coeff.get(JSON.stringify(k));zeroMass=K.plus(zeroMass,K.times(z,K.conj(z)));
    let transformed=K.F();
    slice.group_rows.forEach(row=>{
      const x=row.group_element[0].map(a=>a[0]),exponent=mod(-k.reduce((s,a,j)=>s+a*x[j],0),q);
      transformed=K.plus(transformed,K.scale(K.times(K.decode(row.source_zero_amplitude_exact),K.powers[exponent]),rat(1n,BigInt(grid.length))));
    });
    check(K.eq(transformed,z),"independent full work Fourier law");
    const square=K.times(z,K.conj(z)),weight=rat(BigInt(counts.get(JSON.stringify(k))),BigInt(D));
    check(E.sign(K,K.plus(K.scale(K.unit,mul(weight,weight)),K.scale(square,rat(-1n))))>=0,"phase noise cannot inflate positive fibre envelope");
  });
  same(kernel.actual_source_zero_mass_exact,K.encode(zeroMass),"exact actual Parseval collision mass");
  same(slice.source_zero_mass_exact,K.encode(zeroMass),"Fourier and actual group gate law agree");
  const target=K.scale(K.decode(slice.correct_decoding_and_zero_mass_exact),rat(BigInt(grid.length)));
  check(E.sign(K,K.plus(target,K.plus(K.scale(K.unit,rat(-1n)),K.scale(error2,rat(4n)))))>=0,"true-target quadratic source-error bound without dividing by a rare event");
  check(c.secret_or_errors_used_by_group_compiler===false&&c.accepted_speedup_candidate===false,"fixture truth not a compiler input or speedup");
  return c.domain_controls.reduce((sum,d)=>sum+d.group_rows.length,0);
}
function ledger(l) {
  coherent.budget(l.source_error_bound);
  const n=l.dimension,r=l.root_exponent,B=l.cohorts,M=l.sites_per_cohort,N=3n**BigInt(n*r),D=BigInt(B)*3n**BigInt(M),T=l.two_reflection_iteration_count;
  check(l.integer_secret_count===String(N)&&l.kernel_word_count===String(D)&&l.native_even_level===2*r&&l.native_backend_within_level_cap===(2*r<=512),"actual integer entropy and formal backend cap");
  const e2=parse(l.source_error_bound.mean_pure_trace_distance_squared_upper),p=add(rat(1n,N),rat(N-1n,N*D)),target=div(max(zero,sub(one,mul(rat(4n),e2))),rat(N));
  eq(l.mean_squared_pure_source_error_upper,e2,"source moment bound independently derived");eq(l.mean_ideal_collision_mass_exact,p,"universal random-label collision identity");eq(l.mean_actual_source_zero_upper,p,"source noise positive envelope");
  eq(l.mean_correct_and_zero_lower,target,"true-target quadratic error, scaled by normalization");eq(l.ensemble_conditional_correct_lower,div(target,p),"joint ensemble conditioning, no reciprocal generic trace error");
  eq(l.mean_amplified_zero_success_upper,min(one,mul(rat(BigInt((2*T+1)**2)),p)),"actual paid amplification upper");
  check(l.ensemble_conditioning_is_over_source_draws_and_quantum_outcomes===true&&l.conditional_event_positive_certified_by_source_bound===(cmp(target,zero)>0n),"conditional event positivity and ensemble scope");
  check(l.conditional_correct_lower_is_unamplified_ensemble_statement===true&&l.amplified_ensemble_conditional_correct_lower===null,"per-bank good-state invariance does not prove ensemble invariance");
  const needed=BigInt(l.necessary_iterations_for_half_mean_zero_success),before=needed?needed-1n:0n;
  check(needed>=0n&&cmp(mul(rat((2n*needed+1n)**2n),p),rat(1n,2n))>=0n&&(!needed||cmp(mul(rat((2n*before+1n)**2n),p),rat(1n,2n))<0n)&&l.necessary_iteration_bound_is_sufficient_decoder===false,"minimal necessary fixed-reflection price, not a sufficient algorithm");
  ["conditional_pure_phase_bound_covers_generic_gate_errors","constant_relative_condition_number_implies_free_normalization","two_reflection_bound_is_general_quantum_query_lower_bound","classical_brute_force_is_best_lattice_baseline","efficient_decoder_supplied"].forEach(k=>check(l[k]===false,"ledger scope "+k));
}
function shadow(c) {
  const s=c.shadow,r=c.source_recipe;spec(s.domain_recipe,r);
  const componentCount=s.domain_recipe.domain==="INTEGER_SECRET_SLICE"?r.secret_dimension:2*r.secret_dimension+1;
  check(s.group_coin_decisions.length===componentCount,"every raw group coin included");
  s.group_coin_decisions.forEach(d=>{
    const limit=BigInt(d.range),draws=d.draws.map(BigInt),value=BigInt(d.value),bits=d.coin_bits;
    check(draws.length>0&&draws.length<=s.uniform_coin_attempt_cap&&draws.every(x=>x>=0n&&x<2n**BigInt(bits))&&draws.slice(0,-1).every(x=>x>=limit)&&draws.at(-1)===value&&value<limit,"uniform group coins and every reject charged");
    check(d.status==="UNIFORM_INTEGER"&&value>=0n&&2n**BigInt(bits)>=limit&&(bits===0||2n**BigInt(bits-1)<limit),"minimal uniform group coin range");
  });
  const values=s.group_coin_decisions.map(d=>String(d.value)),slice=s.domain_recipe.domain==="INTEGER_SECRET_SLICE";
  const expected=slice?[values.map(x=>[x,"0"]),1]:[Array.from({length:r.secret_dimension},(_,j)=>values.slice(2*j,2*j+2)),Number(values.at(-1))];
  same([s.group_element[0].map(a=>a.map(String)),s.group_element[1]],expected,"reported group coordinate is the actual sampled coordinate");
  const raw=r.source_receipts.original_classical_records,mask=r.source_receipts.preparation_random_mask.map(BigInt),q=BigInt(r.modulus);
  check(raw.length===2*r.cohorts*r.sites_per_cohort&&new Set(raw.map(a=>a.source_id)).size===raw.length,"all paid high-root original records");
  for(let b=0;b<r.cohorts;b++)for(let j=0;j<r.sites_per_cohort;j++){
    const pair=raw.slice(2*(b*r.sites_per_cohort+j),2*(b*r.sites_per_cohort+j)+2);
    const p=["0",...pair.map(a=>String((BigInt(a.value)+a.label.reduce((sum,x,k)=>sum+BigInt(x)*mask[k],0n))%q))];
    same(r.known_phase_numerators[b][j].map(String),p,"high-root point values still match original data");
  }
  const src=s.source_sample,weights=src.decisions[0].exact_branch_weights.map(parse),norm=weights.reduce(add,zero);
  tensor.coins({recipe:r,final_rational_norm_squared:str(norm),final_computational_sample:src,budget:{coin_attempt_cap_per_factor:s.uniform_coin_attempt_cap}});
  const delta=rat(1n,2n**BigInt(s.approximation_bits)),pow=(x,n)=>{let y=one;for(let j=0;j<n;j++)y=mul(y,x);return y;};
  const e=sub(mul(pow(add(one,delta),3*r.sites_per_cohort+1),pow(add(one,mul(rat(3n),delta)),r.sites_per_cohort)),one),abort=rat(BigInt(componentCount+r.sites_per_cohort+1),2n**BigInt(s.uniform_coin_attempt_cap));
  eq(s.per_conditional_source_relative_error_upper,e,"conditional known tensor gate approximation");eq(s.unconditional_coin_abort_upper,abort,"uniform group and source coin caps");eq(s.whole_joint_readout_TV_or_abort_upper,min(one,add(mul(rat(2n),e),abort)),"whole-shot shadow error includes all aborts");
  check(s.group_measured_early_is_legal_for_this_readout===true&&s.group_Fourier_or_whole_orbit_amplification_covered===false&&s.whole_completion_conditioning_allowed===false&&s.full_group_or_source_table_allocated===false&&s.secret_or_errors_read===false,"early-measurement simulation is not a universal work-register claim");
}
function run(r) {
  check(r.status==="SCOPED_KNOWN_NATIVE_GROUP_COUPLING_AND_POSTSELECTION_REVIEW_PENDING","review-pending actual group work status");
  check(r.producer_sha256===hash(path.join(ROOT,"theorems/native_known_seed_group_workbench.py"))&&r.derivation_sha256===hash(path.join(ROOT,"research/NATIVE_KNOWN_SEED_GROUP_WORKBENCH.md")),"pinned producer and derivation");
  same(Object.keys(r.dependency_sha256).sort(),["native_state_hsp_bridge.py","cyclotomic_rescaling_gate.py","native_noisy_phase_input.py","known_preparation_coherent_reflection.py","known_reflection_tensor_simulation.py","native_noncentral_filter_tradeoff.py","ternary_certified_noise_sampler.py"].sort(),"critical ring, source, sampler and amplification dependencies");
  Object.entries(r.dependency_sha256).forEach(([f,h])=>check(h===hash(path.join(ROOT,"theorems",f)),"pinned ring/source dependency"));
  ["unknown_quantum_only_input_inverse_supplied","integer_slice_excluded_by_full_group_central_ceiling","early_measurement_simulates_arbitrary_group_interference","efficient_full_decoder_supplied","physical_quantum_hardware_executed","hardness_transfer_admitted","accepted_speedup_candidate","new_active_negative_result_created"].forEach(k=>check(r[k]===false,"unsupported promotion "+k));
  check(r.finite_actual_group_controls.length===4&&r.scalable_collision_noise_price_ledgers.length===8&&r.computational_readout_classical_shadows.length===4,"complete finite/scalable/shadow coverage");
  const groupRows=r.finite_actual_group_controls.reduce((sum,c)=>sum+control(c),0);
  r.scalable_collision_noise_price_ledgers.forEach(ledger);r.computational_readout_classical_shadows.forEach(shadow);
  return {status:"PASS",exact_group_rows:groupRows,exact_integer_Fourier_kernels:4,paid_amplification_controls:8,scalable_ledgers:8,shadow_coin_transcripts:4,complete_scalable_shadow_tensor_reconstruction:false,accepted_speedup_candidate:false};
}
if(require.main===module)console.log(JSON.stringify(run(JSON.parse(fs.readFileSync(process.argv[2]||REPORT,"utf8"))),null,2));
module.exports={run,ledger,shadow};
