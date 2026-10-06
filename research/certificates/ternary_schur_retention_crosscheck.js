"use strict";
// Direct projective kernel enumeration and exact BigInt source bounds.
const fs=require("fs"),path=require("path");
const report=JSON.parse(fs.readFileSync(path.join(__dirname,"../phase_workbench/ternary_schur_retention_bound.json"),"utf8"));
function check(v,m){if(!v)throw Error(m);}
function same(a,b,m){check(JSON.stringify(a)===JSON.stringify(b),m);}
function mod(x){return((x%3)+3)%3;}
function dot(a,b){return mod(a.reduce((s,x,i)=>s+x*b[i],0));}
function weight(w){return w.filter(x=>x!==0).length;}
function words(m){return Array.from({length:3**m},(_,i)=>Array.from({length:m},(_,j)=>Math.floor(i/3**(m-j-1))%3));}
function projective(m){return words(m).filter(w=>w.find(x=>x!==0)===1);}
function choose(m,k){let value=1n;for(let i=1;i<=k;i++)value=value*BigInt(m-i+1)/BigInt(i);return value;}
function fraction(c){return[BigInt(c.numerator),BigInt(c.denominator)];}
let certifiedWords=0,sourceMatrices=0,sourceEnvelopes=0;
function verifyBound(c){
  const s=c.nonzero_physical_support,L=c.required_odd_Schur_degree,d=c.kernel_distance_lower_bound,t=Math.min(L,d),k=1+Math.floor((s-d)/t);
  check(c.product_Singleton_power_used===t && c.maximum_admitted_frame_dimension===k,"product-Singleton arithmetic");
  const [a,b]=fraction(c.maximum_retained_support_fraction);check(a*BigInt(s)===b*BigInt(k),"retention fraction");
  check(c.requires_certified_kernel_distance_and_all_mixed_admission && c.valid_for_source_adaptively_selected_linear_frames &&
    !c.requires_projective_saturation && !c.distance_certified_by_this_arithmetic_ledger && !c.nonlinear_or_arbitrary_quantum_receiver_no_go,"retention scope");
}
function verifySource(c){
  const n=c.secret_dimension,m=c.physical_width,d=c.kernel_distance_lower_bound,q=3n**BigInt(n);
  let count=0n;for(let w=1;w<d;w++)count+=choose(m,w)*2n**BigInt(w-1);
  check(BigInt(c.projective_short_words)===count && BigInt(c.each_projective_word_kernel_probability_denominator)===q,"projective source union count");
  const [a,b]=fraction(c.distance_failure_probability_upper_bound),[x,y]=fraction(c.distance_success_probability_lower_bound);
  const clipped=count>q ? q : count;check(a*q===b*clipped && x*q===y*(q-clipped),"exact source bounds");
  check(c.IID_uniform_low_native_A_required && !c.conditions_on_full_row_rank && c.simultaneous_for_all_source_adaptive_frames &&
    !c.certifies_this_particular_matrix && !c.postselected_or_correlated_source_transfer_proved,"source probability promoted");sourceEnvelopes++;
}
for(const c of [report.sharp_disjoint_restriction_control,report.full_kernel_retention_countercontrol]){
  const cert=c.distance_certificate,A=cert.native_low_rows,m=A[0].length,all=projective(m).filter(w=>A.every(a=>dot(a,w)===0)),hist={};
  all.forEach(w=>{hist[weight(w)]=(hist[weight(w)]||0)+1;});
  same(cert.projective_weight_histogram,hist,"ambient exact kernel census");certifiedWords+=all.length;
  check(cert.minimum_distance===Math.min(...all.map(weight)) && cert.projective_kernel_words_enumerated===all.length,"matrix distance certificate");
  check(A.every(a=>dot(a,cert.minimum_weight_witness)===0) && weight(cert.minimum_weight_witness)===cert.minimum_distance,"distance witness");
  check(cert.bounded_exhaustive_certificate_not_scalable_distance_algorithm,"distance census promoted");
  const restriction=c.restriction_admission,W=restriction.physical_frame_columns,L=restriction.odd_degree,s=W[0].filter((_,i)=>W.some(w=>w[i])).length;
  let admitted=true;
  for(let i=0;i<W.length;i++)for(let j=0;j<W.length;j++)for(let k=0;k<W.length;k++){
    const w=W[0].map((_,a)=>mod(W[i][a]*W[j][a]*W[k][a]));admitted=admitted && A.every(a=>dot(a,w)===0);
  }
  check(L===3 && restriction.higher_Schur_admission===admitted,"cubic admission");
  const b=c.retention_bound;verifyBound(b);check(b.nonzero_physical_support===s && b.kernel_distance_lower_bound===cert.minimum_distance,"wrong support/distance");
  check(c.high_retention_claim_excluded_by_bound===(W.length>b.maximum_admitted_frame_dimension),"retention falsifier");
  if(admitted)check(W.length<=b.maximum_admitted_frame_dimension,"admitted frame violates theorem");
  check(c.exact_source_distance_certificate_supplied && !c.full_phase_instrument_or_decoder_supplied,"receiver promoted");
}
for(const c of report.complete_IID_source_controls){
  const n=c.secret_dimension,m=c.physical_width,hist={},basis=projective(m).sort((a,b)=>weight(a)-weight(b));
  for(const flat of words(n*m)){
    const A=Array.from({length:n},(_,i)=>flat.slice(m*i,m*i+m)),w=basis.find(w=>A.every(a=>dot(a,w)===0));check(w,"missing nonzero kernel");
    const d=weight(w);hist[d]=(hist[d]||0)+1;sourceMatrices++;
  }
  same(c.minimum_distance_histogram,hist,"complete IID source distance census");check(c.all_source_matrices_enumerated===3**(n*m),"filtered source");
  for(const d of c.distance_checks){
    verifySource(d.envelope);const failure=Object.entries(hist).reduce((s,[w,count])=>s+(Number(w)<d.distance ? count : 0),0),[a,b]=fraction(d.actual_failure_probability);
    check(a*BigInt(3**(n*m))===b*BigInt(failure),"source failure mass");
    const [x,y]=fraction(d.envelope.distance_failure_probability_upper_bound);check(a*y<=x*b,"union bound false");
  }
}
for(const c of report.growing_source_retention_envelopes){
  verifySource(c.source_distance_envelope);verifyBound(c.simultaneous_adaptive_frame_retention_bound);
  const [a,b]=fraction(c.source_distance_envelope.distance_failure_probability_upper_bound),[x,y]=fraction(c.required_failure_budget);check(a*y<=x*b,"failure budget");
  check(!c.individual_matrix_distance_certificate_supplied && !c.complete_algorithm_sample_complexity_bound,"statistical bound promoted");
}
check(Object.values(report.claim_gate).every(v=>v===false),"candidate promotion");
console.log(JSON.stringify({status:"independent_replay_passed",exact_kernel_words:certifiedWords,
  exhaustive_low_source_matrices:sourceMatrices,source_probability_envelopes:sourceEnvelopes,new_algorithm:false}));
