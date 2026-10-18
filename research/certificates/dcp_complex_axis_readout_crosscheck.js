// Independent complex Born sums, exact rational coarse counts and native Gram.
"use strict";
const fs=require("fs"),path=require("path"),assert=require("assert/strict");
const report=JSON.parse(fs.readFileSync(process.argv[2]||path.join(__dirname,"../phase_workbench/dcp_complex_axis_readout.json"),"utf8"));
const eq=(a,b)=>assert.deepEqual(a,b),near=(a,b)=>assert(Math.abs(a-b)<1e-9,`${a} != ${b}`);
const pop=x=>x.toString(2).split("1").length-1;
const frac=x=>x.includes("/")?Number(x.split("/")[0])/Number(x.split("/")[1]):Number(x);
const bits=x=>x===0n?0:x.toString(2).length;
const gcd=(a,b)=>b===0n?a:gcd(b,a%b);
const rational=(a,b=1n)=>{const g=gcd(a,b);return [a/g,b/g];};
const add=(a,b)=>rational(a[0]*b[1]+b[0]*a[1],a[1]*b[1]);
const textFraction=f=>f[1]===1n?`${f[0]}`:`${f[0]}/${f[1]}`;
function secrets(q,n){return Array.from({length:q**n},(_,code)=>{const s=Array(n);for(let i=n-1;i>=0;i--){s[i]=code%q;code=Math.floor(code/q);}return s;});}
function beta(A,y,on){return A[0].map((_,i)=>on?(A.reduce((s,row,l)=>s+(((y>>(2*l))&3)+1)*(row[i]%8),0)+i)%8:0);}
function geometry(A,t){
  const n=A.length,m=A[0].length,M=2**m,Y=4**n,q=2**t,f=[],groups=Array.from({length:Y},()=>[]);
  for(let x=0;x<M;x++){
    const row=A.map(r=>r.reduce((s,a,i)=>s+a*((x>>i)&1),0)%q);f.push(row);
    const y=row.reduce((s,a,l)=>s+(a%4)*4**l,0);groups[y].push(x);
  }
  return {n,m,M,Y,q,f,groups};
}
function channel(A,t,v,r,feedback){
  const G=geometry(A,t),S=secrets(G.q/4,G.n),p=(1-v)/2;
  const weights=Array.from({length:G.M},(_,e)=>p**pop(e)*(1-p)**(G.m-pop(e)));
  const P=S.map(s=>{
    const clean=new Float64Array(G.Y*G.M),noisy=new Float64Array(G.Y*G.M);
    for(let y=0;y<G.Y;y++){
      const b=beta(A,y,feedback);
      for(let z=0;z<G.M;z++){
        let re=0,im=0;
        for(const x of G.groups[y]){
          const theta=2*Math.PI*(G.f[x].reduce((a,f,l)=>a+f*s[l],0)%G.q)/G.q+
            Math.PI*b.reduce((a,c,i)=>a+c*((x>>i)&1),0)/4-Math.PI*pop(r&x)/2;
          const sign=pop(z&x)%2?-1:1;re+=sign*Math.cos(theta);im+=sign*Math.sin(theta);
        }
        clean[y*G.M+z]=(re*re+im*im)/(G.M*G.M);
      }
    }
    for(let y=0;y<G.Y;y++)for(let z=0;z<G.M;z++)for(let e=0;e<G.M;e++)noisy[y*G.M+z]+=weights[e]*clean[y*G.M+(z^e)];
    near(noisy.reduce((a,b)=>a+b,0),1);return noisy;
  });
  return {G,S,P};
}
function ensemble(A,t,v,feedback){
  const G=geometry(A,t),S=secrets(G.q/4,G.n),P=S.map(()=>new Float64Array(G.M*G.Y*G.M));
  for(let r=0;r<G.M;r++){
    const C=channel(A,t,v,r,feedback);
    for(let s=0;s<S.length;s++)for(let i=0;i<G.Y*G.M;i++)P[s][r*G.Y*G.M+i]=C.P[s][i]/G.M;
  }
  return {G,S,P};
}
function metrics(P){
  const K=P.length,L=P[0].length,mean=new Float64Array(L);let mi=0,bayes=0;
  for(const row of P)for(let j=0;j<L;j++)mean[j]+=row[j]/K;
  for(let j=0;j<L;j++){
    let best=0;for(const row of P){const p=row[j];best=Math.max(best,p);if(p>1e-30&&mean[j]>0)mi+=p*Math.log2(p/mean[j])/K;}bayes+=best/K;
  }
  return {uniform_secret_mutual_information_bits:mi,optimal_one_copy_Bayes_guess_probability:bayes,secret_hypotheses_enumerated:K,likelihood_evaluation_is_free_or_polynomial:false};
}
function compareMetrics(a,b){near(a.uniform_secret_mutual_information_bits,b.uniform_secret_mutual_information_bits);near(a.optimal_one_copy_Bayes_guess_probability,b.optimal_one_copy_Bayes_guess_probability);eq(a.secret_hypotheses_enumerated,b.secret_hypotheses_enumerated);eq(a.likelihood_evaluation_is_free_or_polynomial,false);}
function aliases(P,S,Q){
  const close=(a,b)=>a.every((v,i)=>Math.abs(v-b[i])<1e-11);
  const groups=P.map(row=>P.map((other,j)=>close(row,other)?j:-1).filter(j=>j>=0));
  let diff=0;
  for(let i=0;i<S.length;i++){
    const neg=S[i].map(a=>(Q-a)%Q),j=S.findIndex(s=>s.every((a,l)=>a===neg[l]));
    for(let k=0;k<P[i].length;k++)diff=Math.max(diff,Math.abs(P[i][k]-P[j][k]));
  }
  return {all_secret_laws_distinct_on_this_selected_matrix:groups.every(g=>g.length===1),
    number_of_distinct_likelihood_classes:new Set(groups.map(g=>g[0])).size,
    maximum_negation_pair_probability_difference:diff,complete_likelihood_comparisons_are_exponential:true,aliases_by_secret_index:groups};
}
function compareAliases(a,b){for(const k of Object.keys(b)){if(k==="maximum_negation_pair_probability_difference")near(a[k],b[k]);else eq(a[k],b[k]);}}
function exactNorm(vstr){
  const split=vstr.split("/"),v=[BigInt(split[0]),BigInt(split[1]||"1")];let result=[0n,1n];
  for(let code=0;code<16;code++){
    const a=[code&3,(code>>2)&3],f=Array.from({length:4},(_,x)=>a[0]*(x&1)+a[1]*((x>>1)&1)).map(x=>x%4);
    const counts=Array.from({length:4},(_,y)=>f.filter(x=>x===y).length);
    for(let x=0;x<4;x++)for(let z=0;z<4;z++)if(f[x]===f[z])for(let w=0;w<4;w++){
      if((w&(x^z))!==w||f[x^w]!==f[x]||f[z^w]!==f[x])continue;
      const e=BigInt(2*pop(w));result=add(result,rational(v[0]**e,v[1]**e*BigInt(counts[f[x]]*4*16)));
    }
  }
  return result;
}
eq(report.contract_id,"public_complex_axes_native_Gram_and_inference_contract_v1");eq(report.status,"COMPLEX_GATE_READOUT_EXACT_KERNEL_REVIEW_PENDING");
for(const f of ["accepted_speedup_candidate","novelty_claim","actual_natural_source_noise_certified","same_state_copy_source_or_unknown_inverse_required","random_axes_guarantee_per_attempt_information_improvement","reference_is_an_exact_classical_sampler_for_real_data"])eq(report[f],false);
eq(report.source_quantum_preparations_executed,0);eq(report.identifiability_does_not_prove_efficient_learning,true);
eq(report.selected_controls.length,4);
for(const C of report.selected_controls){
  const A=C.full_labels,t=C.phase_bits,v=frac(C.visibility_exact),on=C.public_source_syndrome_T_feedback_used;
  const E=ensemble(A,t,v,on),B=channel(A,t,v,0,false),G=E.G;
  compareMetrics(C.fixed_X_information,metrics(B.P));compareMetrics(C.public_random_XY_information,metrics(E.P));
  compareAliases(C.fixed_X_aliases,aliases(B.P,E.S,G.q/4));compareAliases(C.random_XY_aliases,aliases(E.P,E.S,G.q/4));
  eq(C.all_public_masks_calibrated,G.M);eq(C.likelihood_entries_enumerated,E.S.length*G.M*G.Y*G.M);eq(C.residual_secret_modulus,G.q/4);
  for(const f of ["selected_matrix_is_native_average_evidence","higher_mutual_information_than_fixed_X_guaranteed","decoder_or_speedup_candidate_supplied"])eq(C[f],false);
  const plan=C.exported_readout_plan,r=Number(plan.public_Y_axis_mask_hex),y=plan.measured_syndrome_index,b=beta(A,y,on),gates=[];
  for(let i=0;i<G.m;i++){for(let j=0;j<b[i];j++)gates.push(["T",i]);if((r>>i)&1)gates.push(["SDG",i]);gates.push(["H",i]);}
  eq(plan.T_grid_feedback_coefficients,b);eq(plan.terminal_gates_after_syndrome_measurement,gates);
  eq(plan.terminal_Z_measurement_wires,Array.from({length:G.m},(_,i)=>i));eq(plan.public_uniform_mask_bits_per_attempt,G.m);
  eq(plan.mask_is_retained_in_classical_record,true);eq(plan.source_quantum_preparations_per_attempt,G.m);
  eq(plan.quantum_samples_multiplied_by_number_of_calibrated_masks,false);eq(plan.unknown_source_inverse_or_duplicate_packet_used,false);
  eq(plan.feedback_computed_only_for_realized_syndrome,true);eq(plan.full_feedback_table_is_calibration_only,true);eq(plan.hardware_transpilation_or_execution_performed,false);
  const expected=[];for(let l=0;l<G.n;l++)for(let i=0;i<G.m;i++){
    const lo=G.m+2*l,hi=lo+1,a=A[l][i]%4;
    if(a===1)expected.push(["CCX",i,lo,hi],["CX",i,lo]);if(a===2)expected.push(["CX",i,hi]);if(a===3)expected.push(["CX",i,lo],["CCX",i,lo,hi]);
  }
  eq(plan.syndrome_circuit.gates,expected);eq(plan.syndrome_circuit.total_qubits,G.m+2*G.n);
}
eq(report.complete_native_Gram_censuses.length,5);
for(const C of report.complete_native_Gram_censuses){
  eq(C.components,1);eq(C.physical_width,2);assert(C.phase_bits===3||C.phase_bits===4);
  const q=2**C.phase_bits,Q=q/4,v=frac(C.visibility_exact),on=C.public_source_syndrome_T_feedback_used;
  const gram=Array.from({length:Q},()=>Array(Q).fill(0));
  for(let a=0;a<q;a++)for(let b=0;b<q;b++){
    const A=[[a,b]],E=ensemble(A,C.phase_bits,v,on),M=4;
    for(let r=0;r<4;r++)for(let y=0;y<4;y++){
      const D=E.G.groups[y].length;if(!D)continue;
      const ref=D/(M*M*M);
      for(let z=0;z<4;z++){const i=r*16+y*4+z;for(let s=0;s<Q;s++)for(let t=0;t<Q;t++)gram[s][t]+=E.P[s][i]*E.P[t][i]/ref/(q*q);}
    }
  }
  const norm=exactNorm(C.visibility_exact),value=Number(norm[0])/Number(norm[1]);
  eq(C.exact_common_diagonal_from_coarse_parallelogram_census,textFraction(norm));
  for(let s=0;s<Q;s++)for(let t=0;t<Q;t++){near(gram[s][t],s===t?value:1);near(C.full_Gram_observed[s][t],gram[s][t]);}
  eq(C.all_original_label_matrices,q*q);eq(C.all_public_axis_masks,4);eq(C.all_residual_secrets,Q);eq(C.exact_off_diagonal,"1");
  eq(C.includes_zero_and_order_two_secrets,true);eq(C.source_family_identifiable_in_L2,norm[0]>norm[1]);
  eq(C.efficient_inference_or_TV_lower_bound_proved,false);eq(C.fiber_sizes_enumerated_only_for_bounded_control,true);
}
eq(report.native_inference_frontiers.length,6);
for(const F of report.native_inference_frontiers){
  const n=F.components,H=n*(n+6),max=6n*BigInt(n)**4n,num=BigInt(n*n)*max+1n;
  eq(F.original_phase_bits,n+8);eq(F.physical_width,3*n);eq(F.all_residual_secret_count_binary_exponent,H);
  eq(F.centered_density_squared_norm_upper,"6");eq(F.every_distinct_secret_pair_source_kernel_exact,"1");eq(F.unavoidable_negation_alias_after_public_XY_mask,false);
  eq(F.max_secrets_distinguished_per_query_hex,"0x"+max.toString(16));eq(F.statistical_queries,n*n);eq(frac(F.absolute_SQ_tolerance),1/(n*n));
  eq(F.SQ_uniform_identification_probability_power_of_two_upper_exponent,Math.max(0,H-bits(num-1n)));
  eq(F.positive_norm_lower_factors_at_inverse_n_noise,[{base_numerator:n-1,base_denominator:n,exponent:6*n},{one_minus_two_to_negative:n}]);
  eq(F.any_public_source_syndrome_local_phase_feedback_before_random_mask_covered,true);
  eq(F.random_axes_may_depend_on_secret_history_instead_of_fresh_uniform_coins,false);
  eq(F.adaptive_phase_feedback_transcript_information_bits_upper_per_fresh_batch,"3");
  eq(F.Pauli_importance_estimator_second_moment_at_weight_floor_n_over_four,{power_of_two:Math.floor(n/4)});
  for(const f of ["reference_sampler_needs_fiber_sizes_or_secret","SQ_query_evaluation_time_restricted","raw_sample_learning_or_joint_multi_record_queries_ruled_out","efficient_decoder_or_classical_simulator_supplied","all_source_theorems_external_review_complete"])eq(F[f],false);
}
console.log(JSON.stringify({status:"ok",selected_complex_readouts:4,complete_native_Gram_censuses:5,native_inference_frontiers:6,efficient_decoder:false}));
