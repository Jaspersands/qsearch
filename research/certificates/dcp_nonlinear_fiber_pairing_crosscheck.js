#!/usr/bin/env node
"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const {verify:verifyAffine}=require("./dcp_adaptive_affine_packet_receiver_crosscheck.js");
const {normalize,add,capped,readProbability,sameProbability}=require("./dcp_adaptive_direction_rank_gate_crosscheck.js");
const need=(ok,msg)=>{if(!ok)throw new Error(msg);};
const I=x=>{need((typeof x==="number"&&Number.isSafeInteger(x))||typeof x==="string","exact integer");return BigInt(x);};
const mod=(x,q)=>(x%q+q)%q;
const same=(x,y)=>JSON.stringify(x)===JSON.stringify(y);
function binomial(n,k){let v=1n;for(let j=1;j<=k;j++)v=v*BigInt(n-j+1)/BigInt(j);return v;}
function subtractFromOne(...values){
  const total=values.reduce(add,{p:0n,e:0}),one=1n<<BigInt(total.e);
  return total.p>=one?{p:0n,e:0}:normalize(one-total.p,total.e);
}
function compare(a,b){const e=Math.max(a.e,b.e);return (a.p<<BigInt(e-a.e))-(b.p<<BigInt(e-b.e));}
function nativeBound(row){
  const n=row.secret_vector_components,t=row.phase_bits,h=row.descent_bits,m=row.original_copies;
  need([n,t,h,m].every(Number.isSafeInteger)&&n>=1&&m>=1&&t>=3&&h>=1&&h<t,"native dimensions");
  const degree=BigInt(n)*((1n<<BigInt(h))-1n),forced=BigInt(m)>degree;
  const odd=forced?{p:0n,e:0}:capped(normalize(1n,m-h*n));
  const fine=normalize((1n<<BigInt(m))-1n,t*n),collisionLower=subtractFromOne(odd,fine);
  const coarseMass=subtractFromOne(odd),nonzero=normalize((1n<<BigInt((t-h)*n))-1n,(t-h)*n);
  const lower=normalize(coarseMass.p*nonzero.p,coarseMass.e+nonzero.e);
  need(I(row.group_algebra_maximum_nonzero_augmentation_degree)===degree&&
       row.every_coarse_fibre_even_for_every_A===forced,"augmentation degree threshold");
  sameProbability(row.odd_coarse_fibre_fraction_upper_bound,odd.p,odd.e,"odd-fibre bound");
  sameProbability(row.native_mean_fine_collision_endpoint_fraction_upper_bound_uncapped,fine.p,fine.e,"fine collision bound");
  sameProbability(row.native_mean_optimal_useful_pairing_coverage_lower_bound,lower.p,lower.e,"native coverage lower bound");
  sameProbability(row.independent_fine_collision_deletion_lower_bound,collisionLower.p,collisionLower.e,"independent collision lower bound");
  if(forced)sameProbability(row.coarse_only_maximal_pairing_exact_mean_IF_even_fibres,nonzero.p,nonzero.e,"exact mean from parity and higher-label law");
  else need(row.coarse_only_maximal_pairing_exact_mean_IF_even_fibres===null,"unproved exact coverage");
  need(row.coarse_only_uniform_higher_label_source_law_used===true&&compare(lower,collisionLower)>=0n,"coarse lineage bound");
  need(row.coverage_bound_vacuous===(lower.p===0n)&&row.bound_is_for_unconditional_IID_public_A_mean===true&&
       row.efficient_pairing_program_constructed_by_bound===false&&row.optimal_full_label_matching_output_IID_proved===false,"mean/source scope");
  need(row.naive_reference_table_rows.power_of_two===m&&
       row.naive_reference_lookup_comparisons_per_accepted_attempt.coefficient===6&&
       row.naive_reference_lookup_comparisons_per_accepted_attempt.power_of_two===m&&
       row.reference_table_cost_is_not_a_lower_bound_on_structured_programs===true,"symbolic reference cost not free oracle or lower bound");
  if(row.visibility){
    const v=readProbability(row.visibility),den=1n<<BigInt(h*n);
    need(v.p>=0n&&v.p<=(1n<<BigInt(v.e)),"visibility range");
    let remaining=den,upper={p:0n,e:0},saturating=null;
    for(let w=1;w<=m;w++){
      const cap=binomial(m,w),mass=cap<remaining?cap:remaining;
      upper=add(upper,normalize(mass*v.p**BigInt(w),h*n+v.e*w));
      remaining-=mass;if(!remaining){saturating=w;break;}
    }
    sameProbability(row.native_mean_any_pairing_visibility_upper_bound,upper.p,upper.e,"source-width knapsack envelope");
    sameProbability(row.native_mean_optimal_useful_visibility_lower_bound,
                    lower.p*v.p**BigInt(m),lower.e+v.e*m,"useful visibility lower bound");
    need(row.width_capacity_saturating_weight===saturating,"width saturation");
    const radius=Math.floor(m/32);let shortCount=0n;
    for(let w=1;w<=radius;w++)shortCount+=binomial(m,w);
    const short=capped(normalize(shortCount,h*n));
    const tail=capped(add(short,normalize(v.p**BigInt(radius+1),v.e*(radius+1))));
    sameProbability(row.short_width_coverage_upper_bound,short.p,short.e,"short-width coverage");
    sameProbability(row.short_plus_tail_visibility_upper_bound,tail.p,tail.e,"short-tail dual bound");
    need(row.explicit_short_radius===radius&&compare(upper,tail)<=0n&&
         row.envelope_is_achievable_pairing===false&&row.general_quantum_receiver_lower_bound===false&&
         row.noise_promise==="independent balanced ORIGINAL-register dephasing","noise envelope scope");
  }
}
function phase(A,x,q){return A.map(row=>mod(row.reduce((v,a,i)=>v+a*((x>>BigInt(i))&1n),0n),q));}
function valid(A,t,h,x,y){const a=phase(A,x,1n<<BigInt(t)),b=phase(A,y,1n<<BigInt(t)),K=1n<<BigInt(h);
  return a.some((v,j)=>v!==b[j])&&a.every((v,j)=>(b[j]-v)%K===0n);}
function f(P,x){
  if(P.kind==="PUBLIC_SINGLE_FLIP")return x^I(P.mask);
  need(P.kind==="EXPONENTIAL_LOOKUP_REFERENCE","program kind");
  const value=P.table[Number(x)];return value===null?null:I(value);
}
function wires(word,P,A,t,h,ordering){
  const m=P.width,M=1n<<BigInt(m),mask=M-1n,us=BigInt(m),vs=BigInt(2*m+1),az=BigInt(3*m+2),ez=az+1n;
  let x=word&mask,u=(word>>us)&(2n*M-1n),v=(word>>vs)&(2n*M-1n),a=(word>>az)&1n,e=(word>>ez)&1n;
  const F=x=>{const y=f(P,x);return y===null?0n:M+y;};
  if(!ordering){
    u^=F(x);v^=F(u&mask);
    if(u>=M&&v>=M&&(v&mask)===x&&valid(A,t,h,x,u&mask))a^=1n;
    v^=F(u&mask);u^=F(x);
  }else{
    u^=F(x);e^=BigInt(x>(u&mask));
    if(e){const old=x;x=u&mask;u=(u&~mask)|old;}
    u^=F(x);
  }
  return x|(u<<us)|(v<<vs)|(a<<az)|(e<<ez);
}
function compiler(C){
  const A=C.public_labels_hex.map(row=>row.map(I)),n=A.length,m=A[0].length,t=C.phase_bits,h=C.descent_bits;
  const q=1n<<BigInt(t),K=1n<<BigInt(h),M=2**m,P=C.program;
  need(m<=12&&n>0&&h>=1&&h<t&&A.every(row=>row.length===m&&row.every(a=>a>=0n&&a<q))&&P.width===m,"compiler source");
  need(P.table_lookup_is_a_free_coherent_oracle===false,"free lookup rejected");
  if(P.kind==="EXPONENTIAL_LOOKUP_REFERENCE")need(P.table.length===M&&
    P.table.every(y=>y===null||(Number.isSafeInteger(y)&&y>=0&&y<M))&&
    P.preprocessing_full_assignments===M&&P.preprocessing_pair_tests_upper_bound===M*(M-1)/2&&
    P.row_address_comparisons_per_XOR_F===M&&P.uniform_efficient_program_supplied===false,"exponential work accounting");
  else need(P.kind==="PUBLIC_SINGLE_FLIP"&&I(P.mask)>0n&&(I(P.mask)&(I(P.mask)-1n))===0n&&
    I(P.mask)<BigInt(M)&&P.CNOT_gates_per_XOR_F===m&&P.X_gates_per_XOR_F===2,"explicit efficient countercontrol program");
  const accepted=[],pairs=[];
  for(let x=0;x<M;x++){
    const xb=BigInt(x),y=f(P,xb);
    const good=y!==null&&y>=0n&&y<BigInt(M)&&f(P,y)===xb&&valid(A,t,h,xb,y);
    const output=wires(xb,P,A,t,h,false),az=BigInt(3*m+2),ez=az+1n;
    need(output===(xb|(BigInt(good)<<az)),"clean reciprocal acceptance wires");
    if(!good)continue;
    accepted.push(x);
    const ordered=wires(output,P,A,t,h,true),r=ordered&BigInt(M-1),e=(ordered>>ez)&1n;
    need(ordered===(r|(1n<<az)|(e<<ez))&&r<(f(P,r))&&
         (r===xb||f(P,r)===xb),"accepted endpoint cleanup");
    if(!e){
      const partner=f(P,r),first=phase(A,r,q),second=phase(A,partner,q);
      const label=first.map((a,j)=>mod(second[j]-a,q)/K);
      need(label.some(a=>a!==0n),"zero label not useful");
      let width=0;for(let mask=r^partner;mask;mask&=mask-1n)width++;
      pairs.push({first:Number(r),second:Number(partner),descended_label_hex:label.map(a=>"0x"+a.toString(16)),physical_Hamming_width:width});
    }
  }
  need(same(C.accepted_assignments,accepted)&&C.pairs.length===pairs.length,"all accepted outcomes retained");
  C.pairs.forEach((saved,i)=>{
    const expected=pairs[i];Object.keys(expected).forEach(k=>need(same(saved[k],expected[k]),"pair label/Hamming data"));
    sameProbability(saved.unconditional_pair_probability,2n,m,"unconditional physical pair mass");
  });
  sameProbability(C.useful_descent_probability,BigInt(accepted.length),m,"useful descent probability");
  need(C.accepted_XOR_F_calls===6&&C.failed_XOR_F_calls===4&&C.original_unknown_phase_qubits_per_attempt===m&&
       C.compiler_qubits_excluding_F_internal_work===3*m+4&&
       C.output_qubits_on_accepted_attempt===1&&C.pair_list_is_measurement_outcomes_not_parallel_outputs===true&&
       C.basis_wire_permutations_and_clean_accepted_workspace_implemented===true&&
       C.hardware_gate_export_backend_implemented===false&&C.secret_or_phase_evaluator_is_program_input===false&&
       C.fresh_descended_labels_IID_certified===false&&C.same_A_source_resupply_or_inverse_supplied===false,"compiler resource/access scope");
  return {A,t,h,M,accepted,pairs};
}
function parityCertificate(C){
  const A=C.public_labels_hex.map(row=>row.map(I)),n=A.length,m=A[0].length,h=C.descent_bits,K=2**h;
  need(K**n<=4096&&m<=12&&C.copies===m&&C.maximum_augmentation_degree===n*(K-1),"finite parity cap");
  const counts=new Map();
  for(let x=0;x<2**m;x++){const key=phase(A,BigInt(x),BigInt(K)).map(Number).join(",");counts.set(key,(counts.get(key)||0)+1);}
  const sort=arr=>arr.sort((x,y)=>{for(let i=0;i<x.length;i++)if(x[i]!==y[i])return x[i]-y[i];return 0;});
  const odd=sort([...counts].filter(([,v])=>v%2).map(([k])=>k.split(",").map(Number)));
  need(same(C.odd_coarse_fibres,odd)&&C.all_fibres_even===(odd.length===0),"original subset fibre parity");
  const savedCounts=C.full_coarse_fibre_counts;
  need(savedCounts.length===counts.size&&savedCounts.every(row=>counts.get(row.residue.join(","))===row.count)&&
       new Set(savedCounts.map(row=>row.residue.join(","))).size===counts.size,"all coarse fibre counts");
  // Independent X-to-Y binomial transform, not the producer's factor multiplication.
  const Y=new Set();
  for(const b of odd){
    function visit(prefix,j){
      if(j===n){const key=prefix.join(",");if(Y.has(key))Y.delete(key);else Y.add(key);return;}
      for(let e=0;e<=b[j];e++)if((e&b[j])===e)visit([...prefix,e],j+1);
    }
    visit([],0);
  }
  const terms=sort([...Y].map(k=>k.split(",").map(Number)));
  need(same(terms,C.nonzero_Y_monomials)&&terms.every(e=>e.reduce((a,b)=>a+b,0)>=m),"augmentation polynomial certificate");
  if(m>n*(K-1))need(Y.size===0,"nilpotency threshold");
}
function counting(C){
  const clauses=C.clauses,V=C.original_variables,pad=C.padding_variables,n=clauses.length,m=V+pad;
  need(pad===Math.max(1,3*n+1-V)&&m<=10,"polynomial padding");
  const A=Array.from({length:n},()=>Array(m).fill(0n));
  clauses.forEach((clause,j)=>{need(clause.length===3,"exact-one relation arity");clause.forEach(i=>{need(Number.isInteger(i)&&i>=0&&i<V,"Boolean index");A[j][i]++;});});
  A[0][V]=4n;
  need(same(C.public_labels_hex.map(row=>row.map(x=>I(x).toString())),A.map(row=>row.map(String))),"constraint multiplicities and padding encoding");
  let direct=0,count=0;
  for(let x=0;x<2**V;x++)if(clauses.every(clause=>clause.reduce((s,i)=>s+((x>>i)&1),0)===1))direct++;
  for(let x=0;x<2**m;x++)if(phase(A,BigInt(x),4n).every(a=>a===1n))count++;
  need(C.exact_one_satisfying_assignments===direct&&C.coarse_target_fibre_count===count&&
       count===direct*2**pad&&C.known_count_multiplier===2**pad&&same(C.coarse_target,Array(n).fill(1)),"counting reduction");
  compiler(C.simple_useful_pairing);
  need(same(C.simple_useful_pairing.public_labels_hex,C.public_labels_hex)&&
       C.simple_useful_pairing.phase_bits===3&&C.simple_useful_pairing.descent_bits===2&&
       I(C.simple_useful_pairing.program.mask)===(1n<<BigInt(V)),"same counting/pairing source");
  sameProbability(C.simple_useful_pairing.useful_descent_probability,1n,0,"simple useful pairing despite counting route");
  need(C.counting_hardness_implies_general_pairing_hardness===false&&
       C.native_IID_average_case_hardness_reduction_supplied===false&&C.pairing_solves_exact_one_counting===false&&
       C.this_countercontrol_is_a_candidate_algorithm===false,"no counting-to-pairing hardness shortcut");
}
function higherSource(C){
  const B=C.coarse_labels,t=C.phase_bits,h=C.descent_bits,n=B.length,m=B[0].length,K=2**h,R=2**(t-h),M=2**m;
  need(m<=6&&R**(n*m)<=4096&&B.every(row=>row.length===m&&row.every(a=>Number.isInteger(a)&&a>=0&&a<K)),"higher-label source cap");
  const groups=new Map();
  for(let x=0;x<M;x++){
    const key=phase(B.map(row=>row.map(BigInt)),BigInt(x),BigInt(K)).map(String).join(",");
    if(!groups.has(key))groups.set(key,[]);groups.get(key).push(x);
  }
  const table=Array(M).fill(null),pairs=[];
  for(const vertices of groups.values())for(let i=0;i+1<vertices.length;i+=2){
    table[vertices[i]]=vertices[i+1];table[vertices[i+1]]=vertices[i];
  }
  for(let x=0;x<M;x++)if(table[x]!==null&&x<table[x])pairs.push([x,table[x]]);
  const P=C.program_fixed_before_higher_lifts;
  need(same(P.table,table)&&P.selection_access==="coarse-public-labels-only"&&
       P.selection_does_not_read_higher_bits_by_this_construction===true&&P.uniform_efficient_program_supplied===false,
       "coarse-only reference program reconstruction");
  const hist=pairs.map(()=>new Map()),lifts=R**(n*m),q=1n<<BigInt(t);
  for(let code=0;code<lifts;code++){
    let value=code;const z=[];
    for(let i=0;i<n*m;i++){z.push(value%R);value=Math.floor(value/R);}
    const A=B.map((row,j)=>row.map((b,i)=>BigInt(b+K*z[j*m+i])));
    pairs.forEach(([x,y],index)=>{
      const a=phase(A,BigInt(x),q),b=phase(A,BigInt(y),q);
      const output=a.map((v,j)=>Number(mod(b[j]-v,q)/BigInt(K))),key=output.join(",");
      hist[index].set(key,(hist[index].get(key)||0)+1);
    });
  }
  need(C.higher_label_lifts_enumerated===lifts&&C.per_pair_output_histograms.length===pairs.length,"complete high-label lift enumeration");
  C.per_pair_output_histograms.forEach((record,i)=>{
    need(same(record.endpoints,pairs[i])&&record.counts.length===R**n&&hist[i].size===R**n,"uniform label support per pair");
    const keys=new Set();record.counts.forEach(row=>{
      const key=row.label.join(",");need(!keys.has(key)&&hist[i].get(key)===row.count&&
        row.count===lifts/(R**n),"original higher-lift output histogram");keys.add(key);
    });
  });
  sameProbability(C.coarse_admission_probability,BigInt(2*pairs.length),m,"coarse admission mass");
  sameProbability(C.joint_coarse_admission_and_nonzero_label_probability,
                  BigInt(2*pairs.length)*((1n<<BigInt((t-h)*n))-1n),m+(t-h)*n,"charged zero filter");
  need(C.uniform_output_before_zero_filter===true&&C.uniform_nonzero_output_after_charged_zero_filter===true&&
       C.pure_input_uniform_native_source_restorable_by_public_zero_injection===true&&
       C.fresh_independent_source_batches_required===true&&
       C.native_output_interface_discards_original_higher_label_transcript===true&&
       C.uniformity_is_conditioned_on_old_full_A===false&&C.public_zero_injection_channel_implemented===false&&
       C.noisy_zero_injection_automatically_matches_exact_visibility===false&&
       C.full_label_dependent_programs_inherit_this_law===false&&C.efficient_program_supplied===false,"conditional native-source law scope");
}
function verify(report,raw){
  need(report.contract_id==="native_nonlinear_fibre_pairing_supply_compilation_and_noise_frontier_v1"&&
       report.accepted_speedup_candidate===false&&report.efficient_native_receiver_supplied===false&&
       report.external_theorem_review_complete===false&&
       report.source_quantum_preparations_executed===0&&report.novelty_claim===false,"global admission");
  need(report.source_affine_artifact==="research/phase_workbench/dcp_adaptive_affine_packet_receiver.json"&&
       report.source_affine_sha256===crypto.createHash("sha256").update(raw).digest("hex"),"source provenance");
  const source=JSON.parse(raw);verifyAffine(source);
  const parents=[source.source_controls[2],source.source_controls[5],source.affine_grammar_gap_counterexample];
  need(report.nonlinear_reference_controls.length===3,"reference coverage");
  report.nonlinear_reference_controls.forEach((C,i)=>{
    const result=compiler(C),parent=parents[i];
    need(same(C.public_labels_hex,parent.public_labels_hex)&&C.phase_bits===4&&C.descent_bits===2,"native reference source binding");
    const parentMass=readProbability(parent.arbitrary_basis_pairing_useful_descent_upper_bound);
    sameProbability(C.useful_descent_probability,parentMass.p,parentMass.e,"full reference attains previous pairing bound");
    need(C.source_control===["unfiltered-seed-2","unfiltered-seed-5","SELECTED-grammar-gap-94"][i],"source selection scope");
    need(same(C.source_affine_useful_descent_probability,parent.optimal_feedback_useful_descent_probability)&&
         same(C.source_arbitrary_pairing_upper_bound,parent.arbitrary_basis_pairing_useful_descent_upper_bound),"fair affine comparison");
  });
  need(report.augmentation_parity_controls.length===5&&report.native_growing_parameter_frontiers.length===15&&
       report.joint_growing_parameter_frontiers.length===5&&report.one_extra_copy_parity_frontiers.length===5&&
       report.many_level_existence_only.length===3,"frontier coverage");
  report.augmentation_parity_controls.forEach(parityCertificate);
  [...report.native_growing_parameter_frontiers,...report.joint_growing_parameter_frontiers,
   ...report.one_extra_copy_parity_frontiers,...report.many_level_existence_only].forEach(nativeBound);
  report.native_growing_parameter_frontiers.forEach((r,i)=>{
    const n=[32,64,128,256,512][Math.floor(i/3)];
    need(r.secret_vector_components===n&&r.phase_bits===64&&r.descent_bits===2&&r.original_copies===3*n,"native growing grid");
    const v=[[1n,2],[3n,2],[63n,6]][i%3];sameProbability(r.visibility,v[0],v[1],"native visibility grid");
  });
  report.one_extra_copy_parity_frontiers.forEach((r,i)=>{const n=[32,64,128,256,512][i];
    need(r.secret_vector_components===n&&r.phase_bits===64&&r.descent_bits===2&&r.original_copies===3*n+1,"extra-copy grid");});
  report.many_level_existence_only.forEach((r,i)=>{const n=[32,64,128][i];
    need(r.secret_vector_components===n&&r.phase_bits===64&&r.descent_bits===62&&r.original_copies===63*n,"many-level existence grid");});
  report.joint_growing_parameter_frontiers.forEach((r,i)=>{const n=[32,64,128,256,512][i];
    need(r.secret_vector_components===n&&r.phase_bits===n&&r.descent_bits===2&&r.original_copies===3*n,"joint growing grid");
    sameProbability(r.visibility,BigInt(n-1),Math.log2(n),"joint inverse-dimension noise");});
  need(report.counting_route_falsifiers.length===2,"counting route scope");report.counting_route_falsifiers.forEach(counting);
  need(report.coarse_only_higher_label_source_controls.length===2,"higher source coverage");
  report.coarse_only_higher_label_source_controls.forEach(higherSource);
  const s=report.scope;
  ["uniform_native_efficient_matching_program_supplied","lookup_reference_is_free_coherent_oracle",
   "postselected_label_sources_inherit_unconditional_mean_bound","full_label_optimized_reference_descended_label_distribution_proved_IID",
   "source_resupply_or_unknown_preparation_inverse_provided","width_noise_bound_is_general_quantum_lower_bound",
   "worst_case_fibre_counting_hardness_is_pairing_hardness","worst_case_counting_hardness_is_native_average_case_hardness",
   "zero_output_labels_receive_credit","hardware_gate_export_implemented"].forEach(k=>need(s[k]===false,"scope expansion: "+k));
  return {status:"ok",nonlinear_reference_controls:3,native_frontiers:28,
          selected_counterexample_useful_descent:"11/16 versus affine 9/16",efficient_native_receiver_supplied:false};
}
module.exports={verify};
if(require.main===module){
  const root=path.resolve(__dirname,"../..");
  const file=process.argv[2]||path.join(root,"research/phase_workbench/dcp_nonlinear_fiber_pairing.json");
  const raw=fs.readFileSync(path.join(root,"research/phase_workbench/dcp_adaptive_affine_packet_receiver.json"));
  console.log(JSON.stringify(verify(JSON.parse(fs.readFileSync(file,"utf8")),raw)));
}
