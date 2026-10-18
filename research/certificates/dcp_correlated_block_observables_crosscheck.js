// Independent complex Born sums and explicit BSC convolution; no FFT reuse.
"use strict";
const fs=require("fs"),path=require("path"),assert=require("assert/strict");
const report=JSON.parse(fs.readFileSync(process.argv[2]||path.join(__dirname,"../phase_workbench/dcp_correlated_block_observables.json"),"utf8"));
const eq=(a,b)=>assert.deepEqual(a,b),near=(a,b)=>assert(Math.abs(a-b)<1e-9,`${a} != ${b}`);
const pop=x=>x.toString(2).split("1").length-1;
const frac=x=>x.includes("/")?Number(x.split("/")[0])/Number(x.split("/")[1]):Number(x);
function metrics(P){
  const K=P.length,L=P[0].length,mean=new Float64Array(L);let mi=0,bayes=0;
  for(const row of P)for(let j=0;j<L;j++)mean[j]+=row[j]/K;
  for(let j=0;j<L;j++){
    let best=0;
    for(const row of P){const p=row[j];best=Math.max(best,p);if(p>1e-30&&mean[j]>0)mi+=p*Math.log2(p/mean[j])/K;}
    bayes+=best/K;
  }
  return {uniform_secret_mutual_information_bits:mi,optimal_one_copy_Bayes_guess_probability:bayes,
    secret_hypotheses_enumerated:K,likelihood_evaluation_is_free_or_polynomial:false};
}
function compareMetrics(actual,expected){
  near(actual.uniform_secret_mutual_information_bits,expected.uniform_secret_mutual_information_bits);
  near(actual.optimal_one_copy_Bayes_guess_probability,expected.optimal_one_copy_Bayes_guess_probability);
  eq(actual.secret_hypotheses_enumerated,expected.secret_hypotheses_enumerated);
  eq(actual.likelihood_evaluation_is_free_or_polynomial,false);
}
function minimumRelation(A){
  const m=A[0].length;let tested=0;
  function supports(w){const result=[];function go(start,ids){if(ids.length===w){result.push(ids);return;}for(let i=start;i<=m-(w-ids.length);i++)go(i+1,[...ids,i]);}go(0,[]);return result;}
  for(let w=1;w<=m;w++)for(const support of supports(w))for(let code=0;code<2**(w-1);code++){
    const signs=[1,...Array.from({length:w-1},(_,i)=>(code>>(w-2-i))&1?1:-1)];tested++;
    if(A.every(row=>support.reduce((s,i,j)=>s+row[i]*signs[j],0)%4===0)){
      const witness=Array(m).fill(0);support.forEach((i,j)=>witness[i]=signs[j]);
      return {minimum_nonzero_signed_support:w,witness,signed_relations_tested:tested,diagnostic_search_is_polynomial:false};
    }
  }
  return {minimum_nonzero_signed_support:null,witness:null,signed_relations_tested:tested,diagnostic_search_is_polynomial:false};
}
eq(report.contract_id,"correlated_block_joint_readout_local_blindness_twirl_baseline_v1");
eq(report.status,"BOUNDED_FULL_OUTCOME_CALIBRATION_AND_LOCAL_DERIVATION_REVIEW_PENDING");
for(const flag of ["selected_controls_are_native_advantage_estimates","accepted_speedup_candidate","novelty_claim","efficient_unknown_secret_inference_implemented"])eq(report[flag],false);
eq(report.source_quantum_preparations_executed,0);eq(report.exponential_fiber_and_secret_enumeration_charged,true);
eq(report.finite_controls.length,3);
let likelihoodEntries=0;
for(const C of report.finite_controls){
  const A=C.full_labels,n=A.length,m=A[0].length,q=2**C.phase_bits,r=q/4,M=2**m,Y=4**n,K=r**n,v=frac(C.visibility_exact),p=(1-v)/2;
  assert(n<=2&&m<=6&&K<=16);
  const groups=Array.from({length:Y},()=>[]),frequencies=[];
  for(let x=0;x<M;x++){
    const f=A.map(row=>row.reduce((s,a,i)=>s+a*((x>>i)&1),0)%q);
    frequencies.push(f);let y=0;f.forEach((a,l)=>y+=(a%4)*4**l);groups[y].push(x);
  }
  const masses=groups.map(g=>g.length/M);masses.forEach((p,y)=>near(p,C.syndrome_probabilities[y]));
  const P=[],discarded=[],secrets=[];
  const errorWeights=Array.from({length:M},(_,e)=>p**pop(e)*(1-p)**(m-pop(e)));
  for(let code=0;code<K;code++){
    let cursor=code;const secret=Array(n);for(let l=n-1;l>=0;l--){secret[l]=cursor%r;cursor=Math.floor(cursor/r);}secrets.push(secret);
    const phase=frequencies.map(f=>2*Math.PI*(f.reduce((s,a,l)=>s+a*secret[l],0)%q)/q);
    const clean=new Float64Array(Y*M),noisy=new Float64Array(Y*M),marginal=new Float64Array(M);
    for(let y=0;y<Y;y++)for(let z=0;z<M;z++){
      let re=0,im=0;
      for(const x of groups[y]){const sign=pop(z&x)%2?-1:1;re+=sign*Math.cos(phase[x]);im+=sign*Math.sin(phase[x]);}
      clean[y*M+z]=(re*re+im*im)/(M*M);
    }
    for(let y=0;y<Y;y++)for(let z=0;z<M;z++){
      let value=0;for(let e=0;e<M;e++)value+=errorWeights[e]*clean[y*M+(z^e)];
      noisy[y*M+z]=value;marginal[z]+=value;
    }
    for(let y=0;y<Y;y++)near(noisy.slice(y*M,(y+1)*M).reduce((a,b)=>a+b,0),masses[y]);
    near(noisy.reduce((a,b)=>a+b,0),1);
    P.push(noisy);discarded.push(marginal);
  }
  compareMetrics(C.joint_syndrome_and_X_information,metrics(P));
  compareMetrics(C.discarded_syndrome_X_information,metrics(discarded));
  const relation=minimumRelation(A),d=relation.minimum_nonzero_signed_support,blind=d===null?m:d-1;
  eq(C.minimum_signed_relation_diagnostic,relation);eq(C.all_X_outcomes_k_wise_uniform_conditional_on_syndrome,blind);
  let lowResidual=0,twirlResidual=0;
  for(let s=0;s<K;s++){
    for(let y=0;y<Y;y++)if(masses[y])for(let u=1;u<M;u++)if(pop(u)<=blind){
      let mean=0;for(let z=0;z<M;z++)mean+=P[s][y*M+z]*(pop(z&u)%2?-1:1)/masses[y];
      lowResidual=Math.max(lowResidual,Math.abs(mean));
    }
    const product=new Float64Array(M);
    for(let dual=0;dual<Y;dual++){
      const means=A[0].map((_,i)=>{
        const theta=2*Math.PI*(A.reduce((sum,row,l)=>sum+row[i]*secrets[s][l],0)%q)/q;
        const shift=Math.PI*(A.reduce((sum,row,l)=>sum+row[i]*((dual>>(2*l))&3),0)%4)/2;
        return v*Math.cos(theta+shift);
      });
      for(let z=0;z<M;z++){
        let value=1/Y;for(let i=0;i<m;i++)value*=(1+(1-2*((z>>i)&1))*means[i])/2;
        product[z]+=value;
      }
    }
    for(let z=0;z<M;z++)twirlResidual=Math.max(twirlResidual,Math.abs(product[z]-discarded[s][z]));
  }
  assert(lowResidual<1e-10&&C.max_nonconstant_parity_bias_through_blind_degree<1e-10);
  assert(twirlResidual<1e-10&&C.product_measurement_twirl_max_probability_residual<1e-10);
  eq(C.source_secret_known_only_for_likelihood_calibration,true);eq(C.twirl_reproduces_joint_syndrome_and_X,false);
  eq(C.twirl_requires_single_qubit_source_measurement_access,true);eq(C.classical_unknown_secret_DCP_simulation_supplied,false);
  eq(C.full_X_outcome_retained_not_independent_marginal_samples,true);eq(C.efficient_decoder_or_quantum_advantage_claimed,false);
  eq(C.full_likelihood_entries_enumerated,K*Y*M);eq(C.basis_addresses_enumerated,M);eq(C.residual_secret_modulus,r);
  assert(C.minimum_probability_before_roundoff_clamp>=-1e-11);
  likelihoodEntries+=K*Y*M;
}
assert(17n**8n<1n<<33n);
eq(report.native_joint_information_blindness_frontiers.length,6);
for(const F of report.native_joint_information_blindness_frontiers){
  const n=F.components,k=Math.floor(n/4),E=2*n-Math.ceil(n/2)-5*k;
  eq(F.original_phase_qubits,4*n);eq(F.blind_local_support_or_X_parity_degree,k);
  eq(F.any_signed_relation_through_degree_k_probability_power_of_two_upper_exponent,E);
  eq(F.simultaneous_local_blindness_and_Holevo_event_exception_power_of_two_upper_exponent,Math.max(0,Math.min(E,n*n)-1));
  eq(F.all_k_local_reduced_states_secret_independent_IF_no_short_relation,true);
  eq(F.full_X_readout_k_wise_uniform_IF_no_short_relation,true);
  eq(F.joint_high_degree_X_correlations_excluded,false);eq(F.local_measurement_circuits_or_full_output_decoders_ruled_out,false);
  eq(F.retained_Holevo_lower_bits_IF_full_injective,Math.max(0,2*n-2*(Math.ceil(Math.log2(n))+3)));
  eq(F.efficient_readout_or_decoder_supplied,false);
}
// Independent complete original-label census. Fixed secret2 is a deliberate
// counterexample to using the primitive-secret formula for the full prior.
eq(report.complete_native_collision_censuses.length,6);
const totals=Array(6).fill(0);
for(let code=0;code<4096;code++){
  const a=[code&15,(code>>4)&15,(code>>8)&15];
  const f=Array.from({length:8},(_,x)=>a.reduce((s,v,i)=>s+v*((x>>i)&1),0)%16);
  for(let j=0;j<2;j++){
    const secret=j+1,clean=new Float64Array(32);
    for(let y=0;y<4;y++)for(let z=0;z<8;z++){
      let re=0,im=0;
      for(let x=0;x<8;x++)if(f[x]%4===y){const sign=pop(x&z)%2?-1:1,theta=2*Math.PI*secret*f[x]/16;re+=sign*Math.cos(theta);im+=sign*Math.sin(theta);}
      clean[8*y+z]=(re*re+im*im)/64;
    }
    for(const [vIndex,v] of [1,.5,0].entries()){
      const p=(1-v)/2;let squared=0;
      for(let y=0;y<4;y++)for(let z=0;z<8;z++){
        let value=0;for(let e=0;e<8;e++)value+=p**pop(e)*(1-p)**(3-pop(e))*clean[y*8+(z^e)];
        squared+=value*value;
      }
      totals[3*j+vIndex]+=32*squared/4096;
    }
  }
}
for(const [i,C] of report.complete_native_collision_censuses.entries()){
  eq(C.components,1);eq(C.width,3);eq(C.phase_bits,4);eq(C.fixed_residual_secret,Math.floor(i/3)+1);
  eq(C.all_original_label_matrices,4096);near(C.native_mean_uniform_reference_collision_multiplier,totals[i]);
  const v=frac(C.visibility_exact);eq(v,[1,.5,0][i%3]);
  if(i<3){
    const M=8,G=4,B=(1+v*v)**3,D=(2+v*v)**3;
    near(frac(C.primitive_secret_formula_exact_rational),G/M+(M+B-2)/M+(D-M-B+1)/(G*M));
    eq(C.even_secret_exception_in_formula,false);
  }else{eq(C.primitive_secret_formula_exact_rational,null);eq(C.even_secret_exception_in_formula,true);}
}
near(totals[0],21/8);near(totals[3],17/4);
assert(27n**5n<1n<<24n);
eq(report.native_fixed_readout_information_frontiers.length,6);
for(const F of report.native_fixed_readout_information_frontiers){
  const n=F.components,t=n+8,ceilLog5n=Math.ceil(Math.log2(5*n)),h=Math.min(Math.floor(n/5)-1,n-ceilLog5n)-1;
  const entropy=n*(t-2),numerator=BigInt(3*entropy-8)*(1n<<BigInt(h)),denominator=4n*((1n<<BigInt(h))+1n);
  const attempts=Number((numerator+denominator-1n)/denominator);
  eq(F.original_phase_qubits_per_batch,3*n);eq(F.original_phase_bits,t);eq(F.residual_secret_entropy_bits,entropy);
  eq(F.mean_information_bits_per_fixed_readout_batch_upper,{integer_part:1,dyadic_correction_exponent:h});
  eq(F.all_even_secret_prior_probability_exponent,n);eq(F.all_even_secret_KL_bits_upper,5*n);
  eq(F.full_secret_identification_ceiling,{half_plus_two_to_negative_exponent:entropy-n+1});
  eq(F.three_quarter_full_secret_identification_target_attainable,false);
  eq(F.Fano_target,"negation orbit under original uniform-secret prior");
  eq(F.three_quarter_negation_orbit_identification_attempt_lower_bound,attempts);
  eq(F.raw_original_qubits_lower_bound_for_that_orbit_target,3*n*attempts);
  eq(F.retained_block_Holevo_lower_bits_IF_full_injective,Math.max(0,n-Math.ceil(3*(Math.ceil(Math.log2(n))+3)/2)));
  eq(F.full_frequency_noninjectivity_probability_upper_exponent,n*n+2*n);
  eq(F.information_upper_is_native_mean_not_pointwise_in_A,true);
  eq(F.only_unrotated_syndrome_then_complete_X_readout_covered,true);
  eq(F.adaptively_secret_aligned_bases_or_other_collective_measurements_covered,false);
  eq(F.source_preparation_or_decoder_implemented,false);eq(F.polynomial_sample_lower_bound_is_a_general_algorithmic_no_go,false);
}
console.log(JSON.stringify({status:"ok",full_outcome_controls_replayed:3,complete_joint_likelihood_entries:likelihoodEntries,
  native_frontiers:6,native_collision_censuses:6,native_information_frontiers:6,
  efficient_decoder:false,classical_unknown_secret_DCP_simulation:false}));
