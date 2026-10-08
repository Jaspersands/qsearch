"use strict";
const fs = require("fs"), path = require("path"), crypto = require("crypto");
const R = require("./cyclotomic_exact.js");
const {rat, parse, str, add, sub, mul, div, cmp, zero, one, field} = R;
const pow = (a,n) => {let s=one;while(n--)s=mul(s,a);return s;};
const report = JSON.parse(fs.readFileSync(process.argv[2] || path.join(__dirname, "../reductions/cyclic_centre_state_hsp_receiver.json"), "utf8"));
const check = (x,m) => { if (!x) throw Error(m); };
const same = (a,b,m) => check(JSON.stringify(a) === JSON.stringify(b),m);
const mod = (x,p) => (x%p+p)%p;
const dot = (a,b) => a.reduce((s,x,i) => s+x*b[i],0);
const words = (d,p=3) => Array.from({length:p**d}, (_,j) => Array.from({length:d}, (_,i) => Math.floor(j/p**(d-i-1))%p));
const ceil = a => (a[0]+a[1]-1n)/a[1];
const number = a => Number(a[0])/Number(a[1]);
const near = (a,b,m) => check(Number.isFinite(a) && Math.abs(a-b) < 2e-11,m);
const bits = n => { let b=0,x=1; while (x<n) {x*=2;b++;} return b; };
const prime = p => p>=3 && p%2===1 && Array.from({length:Math.max(0,Math.floor(Math.sqrt(p))-1)},(_,i)=>i+2).every(d=>p%d!==0);
function ledger(r) {
  const p=r.p,d=r.quotient_dimension,k=r.failure_bits;
  check(prime(p) && Number.isInteger(d) && d>0 && Number.isInteger(k) && k>0,"valid source ledger");
  const e=parse(r.original_gap_lower); check(cmp(e,zero)>0n && cmp(e,one)<=0n,"original gap");
  const h=bits(p),u=bits(p-1),delta=rat(1n,16n*BigInt(p*p));
  const m=32n*BigInt(p*p)*BigInt(d*h+k+2+u),C=BigInt(p)*m;
  const w=div(e,rat(BigInt(2*(p-1))));
  const N=ceil(div(rat(2n*C+8n*BigInt(k+2)),w));
  const M=ceil(div(rat(BigInt(2*((d+1)*h+k+2))),e));
  const exact = {ceil_log2_p:h,data_selected_sector_union_bits:u,
    conditional_modulus_defect_threshold:str(delta),commutator_norm_squared_upper:str(mul(rat(32n),delta)),
    nontrivial_root_distance_squared_lower:str(rat(16n,BigInt(p*p))),tensor_copies_per_Fourier_experiment:p,
    sector_Fourier_experiments:Number(m),selected_sector_copy_quota:Number(C),
    one_nonzero_sector_weight_lower_if_centre_not_fixed:str(w),original_centre_acquisition_cap:Number(N),
    fresh_original_final_copy_cap:Number(M),total_original_copy_cap:Number(N+M),
    known_controlled_R_call_cap:Number(N+C+M),conditional_bucket_memory_cap:Number(BigInt(p-1)*C)};
  for(const [a,b] of Object.entries(exact)) same(r[a],b,"exact cost or commutator margin: "+a);
  const eta=rat(1n,2n**BigInt(k+2));
  for(const key of ["quota_failure_upper","all_selected_sector_overgroup_failure_upper","final_decoder_failure_upper"]) same(r[key],str(eta),"individual failure ledger");
  same(r.total_ideal_failure_upper,str(mul(rat(3n),eta)),"total failure ledger");
  check(cmp(mul(rat(N),w),rat(2n*C+8n*BigInt(k+2)))>=0n,"paid binomial quota bound");
  check(cmp(mul(rat(32n),delta),rat(16n,BigInt(p*p)))<0n,"strict finite phase rigidity");
  check(r.minimum_conditional_gap_required===false && r.iid_copies_of_one_original_state_required===true && r.polylog_group_order_at_arbitrary_binary_encoded_prime===false && r.approximate_source_or_gate_error_certified===false,"source and efficiency scope");
}
function kernel(A,d,p=3) {
  A=A.map(row=>row.slice()); let r=0; const pivots=[];
  for(let j=0;j<d && r<A.length;j++) {
    const index=A.findIndex((row,i)=>i>=r && row[j]); if(index<0)continue;
    [A[r],A[index]]=[A[index],A[r]];
    const inv=Array.from({length:p-1},(_,i)=>i+1).find(a=>a*A[r][j]%p===1);
    A[r]=A[r].map(x=>x*inv%p);
    for(let i=0;i<A.length;i++) if(i!==r) {const c=A[i][j]; A[i]=A[i].map((x,k)=>mod(x-c*A[r][k],p));}
    pivots.push(j); r++;
  }
  return Array.from({length:d},(_,j)=>j).filter(j=>!pivots.includes(j)).map(j=>{
    const v=Array(d).fill(0);v[j]=1;pivots.forEach((q,i)=>v[q]=mod(-A[i][j],p));return v;
  });
}
const K=field(3), qwords=words(2);
const root = n => K.powers[mod(n,3)];
const scalar = a => K.scale(K.unit,a);
const asRat = a => {check(cmp(a[1],zero)===0n,"rational physical probability");return a[0];};
function fourier(points,moments) {
  return points.map(y=>asRat(K.scale(points.reduce((s,x,i)=>K.plus(s,K.times(root(-dot(y,x)),moments[i])),K.F()),rat(1n,BigInt(points.length)))));
}
function sector(c) {
  check(c.central_character===1 || c.central_character===2,"faithful central sector");
  const lam=c.central_character,eta=parse(c.contamination_eta),lift=c.calibration_central_lift;
  let diagonal=[zero,zero,zero];
  if(c.source_kind==="tiny-conditional-gap") diagonal=lam===1 ? [sub(one,mul(rat(2n,3n),eta)),div(eta,rat(3n)),div(eta,rat(3n))] : [rat(1n,3n),rat(1n,3n),rat(1n,3n)];
  else diagonal[mod(-lift,3)]=one;
  const phi=qwords.map(([a,b])=>a ? K.F() : diagonal.reduce((s,w,t)=>K.plus(s,K.scale(root(lam*b*t),w)),K.F()));
  const cubic=phi.map(z=>K.times(K.times(z,z),z)), expected=fourier(qwords,cubic);
  same(c.full_character_words,qwords,"all sector control characters");
  expected.forEach((a,i)=>near(c.tensor_moment_Fourier_probabilities[i],number(a),"sector character-law probability"));
  // Literal known monomial actions, applied to every diagonal tensor input.
  const literal=qwords.map(()=>zero);
  for(const t of words(3)) {
    const weight=t.reduce((s,x)=>mul(s,diagonal[x]),one); if(!weight[0])continue;
    for(let yi=0;yi<9;yi++) {
      const y=qwords[yi],v=new Map();
      for(const [a,b] of qwords) {
        const out=t.map(x=>(x+a)%3).join(",");
        const amplitude=K.scale(root(lam*b*t.reduce((s,x)=>s+x,0)-y[0]*a-y[1]*b),rat(1n,9n));
        v.set(out,K.plus(v.get(out)||K.F(),amplitude));
      }
      let norm=zero;for(const a of v.values())norm=add(norm,asRat(K.times(K.conj(a),a)));
      literal[yi]=add(literal[yi],mul(weight,norm));
    }
  }
  literal.forEach((a,i)=>{same(str(a),str(expected[i]),"independent exact whole Kraus identity");near(c.literal_Kraus_probabilities[i],number(a),"literal recorded branch probability");});
  check(c.input_qutrit_copies_consumed===3 && c.known_controlled_R_calls===3 && c.every_outcome_retained===true && c.selected_sector_supplied_for_free===false && c.nonabelian_QFT_or_unknown_inverse_used===false && c.full_unconditioned_tensor_action_claimed_linear===false,"paid source and exact sector scope");
}
function nonstabilizer(c) {
  const v=c.nonstabilizer_integer_amplitudes,lam=c.central_character;
  check(v.length===3 && v.every(Number.isInteger) && [1,2].includes(lam),"actual nonstabilizer input amplitudes");
  const D=v.reduce((s,x)=>s+x*x,0);check(D===c.integer_amplitude_squared_norm && D>0,"exact integer source norm");
  const phi=qwords.map(([a,b])=>v.reduce((s,x,t)=>K.plus(s,K.scale(root(lam*b*t),rat(BigInt(x*v[(t+a)%3]),BigInt(D)))),K.F()));
  const law=fourier(qwords,phi.map(z=>K.times(K.times(z,z),z)));
  const physical=[];
  for(const y of qwords) {
    const out=Array.from({length:27},()=>K.F());
    for(const t of words(3))for(const [a,b] of qwords) {
      const index=t.map(x=>(x+a)%3).reduce((s,x)=>3*s+x,0);
      const coefficient=BigInt(t.reduce((s,x)=>s*v[x],1));
      const z=K.scale(root(lam*b*t.reduce((s,x)=>s+x,0)-y[0]*a-y[1]*b),rat(coefficient));
      out[index]=K.plus(out[index],z);
    }
    const norm=out.reduce((s,z)=>add(s,asRat(K.times(K.conj(z),z))),zero);
    physical.push(div(norm,rat(81n*BigInt(D)**3n)));
  }
  physical.forEach((a,i)=>{
    same(str(a),str(law[i]),"exact non-diagonal pure-state Kraus instrument");
    near(c.one_component_instrument.literal_Kraus_probabilities[i],number(a),"nonstabilizer local tensor outcomes");
  });
  const points=words(4);same(c.full_character_words,points,"ALL81 nonstabilizer full-sector characters");
  points.forEach(([a1,a2,b1,b2],i)=>{
    const expected=b1===0 ? div(law[3*a2+b2],rat(3n)) : zero;
    near(c.complete_literal_probabilities[i],number(expected),"six-qutrit full tensor operation");
    near(c.tensor_moment_Fourier_probabilities[i],number(expected),"full-dimensional character law");
  });
  check(c.actual_conditional_input_copies===3 && c.physical_qutrits_in_three_copies===6 && c.conditional_full_quotient_dimension===4 && c.density_table_is_an_algorithm_input===false && c.source_is_a_new_toy_oracle_problem===false,"nonstabilizer source/accounting scope");
}
const comm = (x,y,p=3) => mod(x[1]*y[0]-y[1]*x[0],p);
function chart(frame,t,p=3) {
  const x=[0,1].map(i=>mod(frame.reduce((s,v,j)=>s+v[i]*t[j],0),p));
  return [x,mod(t[frame.length]+((p+1)/2)*x[0]*x[1],p)];
}
function sourceMoment(g,r) {
  const [x,z]=g,[a,b]=x,c=r.calibration_central_lift,e=parse(r.contamination_eta);
  if(r.source_kind==="tiny-conditional-gap") {
    if(a)return K.F(); if(!b)return z ? K.F() : K.unit;
    return K.scale(root(z),div(sub(one,e),rat(3n)));
  }
  if(a)return K.F();
  if(r.source_kind==="centre-fixed")return K.unit;
  if(z===mod(c*b,3))return K.unit;
  return r.source_kind==="rare-central-sector" ? scalar(sub(one,e)) : K.F();
}
function receiver(r) {
  ledger(r.ledger);check(r.status==="RECOVERED","all declared complete receivers succeed");
  const L=r.ledger,counts=r.centre_bucket_counts,selected=r.selected_nonzero_sector;
  check(counts.length===3 && counts.every(x=>Number.isInteger(x)&&x>=0) && counts.reduce((s,x)=>s+x,0)===r.actual_original_centre_draws,"actual centre bucket accounting");
  check(r.actual_original_centre_draws<=L.original_centre_acquisition_cap,"source cap");
  check(r.actual_total_original_copies===r.actual_original_centre_draws+L.fresh_original_final_copy_cap,"actual total copies");
  check(r.actual_known_controlled_R_calls===r.actual_total_original_copies+(selected===null?0:L.selected_sector_copy_quota),"actual controlled action calls");
  const frame=r.recovered_quotient_overgroup_frame;
  check(frame.every(x=>x.length===2 && x.every(a=>Number.isInteger(a)&&a>=0&&a<3)) && frame.every(x=>frame.every(y=>comm(x,y)===0)),"actual commuting overgroup");
  check(r.actual_abelian_overgroup_used===(selected!==null) && r.centre_fixed_quotient_action_linear_on_support===(selected===null) && r.centre_fixed_section_claimed_linear_on_full_workspace===false,"exact whole-group versus state-support quotient scope");
  check(r.quotient_overgroup_commutator_zero===(selected===null?null:true),"centre-trivial branch is NOT an abelian whole-group overgroup");
  if(selected!==null) {
    check([1,2].includes(selected) && counts[selected]===L.selected_sector_copy_quota,"selected bucket reaches PAID quota");
    const observed=qwords.filter((_,i)=>r.tensor_sample_histogram[i]);
    check(r.tensor_sample_histogram.length===9 && r.tensor_sample_histogram.reduce((s,x)=>s+x,0)===L.sector_Fourier_experiments,"all tensor experiments charged");
    same(r.tensor_observed_character_words,observed,"observed characters");same(frame,kernel(observed,2),"actual character-kernel overgroup");
  } else check(r.source_kind==="centre-fixed" && r.successful_centre_fixed_branch===true && r.actual_original_centre_draws===L.original_centre_acquisition_cap && counts[0]===r.actual_original_centre_draws,"centre-trivial quotient only on correct source");
  const f=r.final_instrument,points=words(f.dimension);
  same(f.character_words,points,"all final character outcomes");
  const elements=points.map(t=>selected===null?[t,0]:chart(frame,t));same(f.group_chart_elements,elements,"public half-quadratic group chart");
  const law=fourier(points,elements.map(g=>sourceMoment(g,r)));
  law.forEach((a,i)=>{near(f.probabilities[i],number(a),"final original-state character law");near(f.literal_Kraus_probabilities[i],number(a),"full original-state Kraus law");});
  check(f.uses_fresh_original_state_not_the_selected_sector_state===true,"final phase correction uses ORIGINAL copies");
  const histogram=r.final_sample_histogram;check(histogram.length===points.length && histogram.reduce((s,x)=>s+x,0)===L.fresh_original_final_copy_cap,"all final copies charged");
  const basis=kernel(points.filter((_,i)=>histogram[i]),f.dimension);same(r.recovered_final_kernel_basis,basis,"final learned subgroup, not pi(S)");
  const recovered=words(basis.length).flatMap(t=>{
    const u=Array.from({length:f.dimension},(_,i)=>mod(basis.reduce((s,v,j)=>s+t[j]*v[i],0),3));
    return selected===null?[0,1,2].map(z=>[u,z]):[chart(frame,u)];
  }).sort((a,b)=>a[0][0]-b[0][0]||a[0][1]-b[0][1]||a[1]-b[1]);
  let target;
  if(r.source_kind==="tiny-conditional-gap")target=[[[0,0],0]];
  else if(r.source_kind==="centre-fixed")target=words(2).map(([b,z])=>[[0,b],z]);
  else target=[0,1,2].map(b=>[[0,b],mod(r.calibration_central_lift*b,3)]);
  same(r.recovered_Bose_subgroup_elements,recovered,"literal learned full Bose subgroup");same(recovered,target,"source-specific true subgroup");same(r.actual_Bose_subgroup_elements,target,"actual target scope");
  check(r.one_original_source_state_copied_or_reused===false && r.density_tables_required_by_uniform_quantum_recipe===false && r.finite_reference_simulation_is_scalable_quantum_hardware_execution===false,"no free simulator or unknown oracle");
}
const hash=crypto.createHash("sha256").update(fs.readFileSync(path.join(__dirname,"../CYCLIC_CENTRE_STATE_HSP_RECEIVER.md"))).digest("hex");
check(report.status==="CONSTRUCTIVE_ODD_PRIME_CYCLIC_CENTRE_STATE_HSP_REVIEW_PENDING" && report.derivation_sha256===hash,"pinned constructive derivation");
for(const flag of ["arbitrary_mixed_state_conditional_gap_assumed","all_central_extensions_solved","native_DHSP_source_reduction_supplied","new_classical_HSP_speedup_claimed","candidate_record_accepted","novelty_claimed","Shor_level_result_claimed"])check(report[flag]===false,"scope flag: "+flag);
same(report.bilinear_extension_form,{p:3,B:[[0,0],[1,0]]},"actual calibration extension");
check(report.complete_literal_sector_instruments.length===18 && report.capped_complete_reference_receivers.length===10 && report.growing_integer_resource_ledgers.length===16,"complete prespecified corpus");
report.complete_literal_sector_instruments.forEach(sector);
check(report.nonstabilizer_two_qudit_instruments.length===4,"both nonstabilizer states, both faithful sectors");
report.nonstabilizer_two_qudit_instruments.forEach(nonstabilizer);
report.capped_complete_reference_receivers.forEach(receiver);
report.growing_integer_resource_ledgers.forEach(ledger);
const c=report.tiny_conditional_gap_countercontrol,e=rat(1n,2n**40n),a=pow(sub(one,e),3);
same(c.conditional_exact_gap_of_Z_direction,str(e),"genuinely tiny conditional gap");
same(c.exact_tensor_probability_if_second_character_zero,str(div(add(one,mul(rat(2n),a)),rat(9n))),"exact tiny-gap majority law");
same(c.exact_tensor_probability_if_second_character_nonzero,str(div(sub(one,a),rat(9n))),"nonzero rare outcomes NOT rounded to zero");
same(c.final_original_probability_yb0_yz1,str(div(sub(rat(3n),mul(rat(2n),e)),rat(9n))),"final original mass");
same(c.final_original_probability_yb_nonzero_yz1,str(div(e,rat(9n))),"tiny but nonzero final outcomes");
same(c.final_original_probability_yz_not_one,"1/9","remaining final outcomes");
check(c.conditional_nontrivial_exact_anyonic_symmetry===false && c.approximate_commuting_overgroup_may_retain_Z_direction===true,"overgroup, NOT exact conditional learner");
const tiny=report.capped_complete_reference_receivers.find(r=>r.source_kind==="tiny-conditional-gap" && r.contamination_eta===str(e));
check(tiny.selected_nonzero_sector===1,"tiny-gap sector actually exercised");same(tiny.recovered_quotient_overgroup_frame,[[0,1]],"almost symmetry retained without invalid exact claim");
console.log(JSON.stringify({status:"PASS",exact_literal_sector_outcomes:18*9,nonstabilizer_six_qutrit_outcomes:4*81,capped_complete_receivers:10,growing_resource_ledgers:16,tiny_conditional_gap_actual_selected_sector:true,novelty_or_Shor_level_claimed:false}));
